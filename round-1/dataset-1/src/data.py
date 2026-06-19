#!/usr/bin/env python3
"""Build the First-Letter-Spelling Absorption Testbed.

Three linked components per target letter, merged into ONE schema-standardised
data_out.json (schema = exp_sel_data_out: {"metadata":{...}, "datasets":[{"dataset","examples":[...]}]}):

  (A) CONTENT-FLIP minimal pairs   : (x_on, x_off) in an identical carrier; x_on slots a word
      STARTING WITH the target letter, x_off a surface-matched word that does NOT.
  (B) SURFACE-FLIP minimal pairs   : (x_a, x_b) in an identical carrier; BOTH words start with the
      target letter but differ in surface form (concept held constant, surface varies).
  (C) FROZEN PILE CORPUS           : real in-context windows of slot-eligible word-initial tokens
      starting with each target letter, + a per-token occurrence table (dataset-level metadata).

Sources (verified, non-circular, frozen):
  - Words  : unsloth/gemma-2-2b tokenizer (ungated mirror of gated google/gemma-2-2b; vocab==256000),
             via the exact sae-spelling get_alpha_tokens slot-eligibility recipe.
  - Corpus : monology/pile-uncopyrighted at PINNED revision 3be90335... ('3be9033').
  - Judge  : OpenRouter cheap model (cost-tracked, hard-stop budget); pairs are largely
             self-validating (mechanically constructed against the tokenizer), the judge checks
             grammaticality + that the content flip / surface flip holds.

Pure CPU/data task: NO SAE, NO model weights, NO GPU. Tokenizer + pile text + LLM-judge only.
"""

from __future__ import annotations

import argparse
import asyncio
import gc
import hashlib
import json
import math
import os
import pickle
import resource
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
from loguru import logger

# ----------------------------------------------------------------------------- config / constants
WORKDIR = Path(__file__).resolve().parent
CACHE_DIR = WORKDIR / "cache"
LOG_DIR = WORKDIR / "logs"
CACHE_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

TOKENIZER_ID = "unsloth/gemma-2-2b"          # ungated mirror; identical vocab to google/gemma-2-2b
EXPECTED_VOCAB = 256000
PILE_REPO = "monology/pile-uncopyrighted"
PILE_REV_FULL = "3be90335b66f24456a5d6659d9c8d208c0357119"
PILE_REV_SHORT = "3be9033"

ALL_ALPHA_LETTERS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
GEMMA_SPACE = "▁"                        # '▁' sentencepiece word-initial marker

# Window sizing for corpus contexts
WIN_LEFT, WIN_RIGHT = 32, 16                  # ~48-token windows
WINDOWS_PER_WORD_CAP = 60
WINDOWS_PER_LETTER_CAP = 2500
OCC_TABLE_TOPK = 2000                         # top word-types per letter kept in dataset metadata

N_FOLDS = 5
SEED = 1234

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(str(LOG_DIR / "build.log"), rotation="30 MB", level="DEBUG")


def set_mem_limit(gb: float = 24.0) -> None:
    try:
        b = int(gb * 1024 ** 3)
        resource.setrlimit(resource.RLIMIT_AS, (b, b))
        logger.info(f"RLIMIT_AS set to {gb} GB")
    except (ValueError, OSError) as e:
        logger.warning(f"Could not set RLIMIT_AS ({e!r}); continuing without it")


# ----------------------------------------------------------------------------- helpers
def fold_of(key: str, n: int = N_FOLDS) -> int:
    h = hashlib.md5(key.encode("utf-8")).hexdigest()
    return int(h, 16) % n


def carriers():
    """(template_id, prefix, suffix). text = prefix + word + suffix.

    Mirrors sae-spelling prompting.py (VERBOSE_FIRST_LETTER_TEMPLATE, '{word}:', ICL) plus neutral
    natural-sentence carriers so cover-sets span multiple contexts, not only the spelling prompt.
    The ICL block is built per-letter (no slotted-word contamination) and injected as a prefix.
    """
    # Mention-style neutral carriers are word-class-agnostic (grammatical for ANY token: noun, verb,
    # adjective, function word) — frequency-ranked on-words are mixed POS, so noun-assuming sentences
    # ("I saw a {word}") would be ungrammatical. Mention contexts keep the first-letter token cleanly
    # slotted and grammatical, and stay close to the documented spelling-probe regime.
    return [
        ("t_verbose", "", " has the first letter:"),         # sae-spelling VERBOSE_FIRST_LETTER_TEMPLATE
        ("t_colon", "", ":"),                                # sae-spelling default '{word}:'
        ("t_mention_word", "The word ", " appears in the text."),
        ("t_mention_term", "Consider the term ", " for a moment."),
        ("t_mention_example", "Here is an example word: ", "."),
        ("t_mention_spelled", "Let us spell out the word ", "."),
    ]


# Fixed ICL pool: common words used ONLY as in-context spelling examples (never slotted as on/off).
ICL_POOL = [
    ("apple", "A"), ("river", "R"), ("table", "T"), ("garden", "G"), ("music", "M"),
    ("window", "W"), ("yellow", "Y"), ("planet", "P"), ("camera", "C"), ("forest", "F"),
]


def build_icl_block(rng: np.random.Generator, k: int = 4, exclude=frozenset()) -> str:
    pool = [(w, L) for (w, L) in ICL_POOL if w not in exclude]
    idx = rng.permutation(len(pool))[:k]
    lines = [f"{pool[i][0]} has the first letter: {pool[i][1]}" for i in idx]
    return "\n".join(lines) + "\n"


# ----------------------------------------------------------------------------- step 1: vocab
def build_vocab(tok):
    """Replicate sae-spelling get_alpha_tokens + slot-eligibility, grouped by first letter.

    A vocab token is SLOT-ELIGIBLE iff it is WORD-INITIAL (raw token carries the '▁' marker, i.e.
    convert_tokens_to_string yields a leading space) AND, after stripping exactly one leading space,
    is non-empty and every char is alphabetic. Each such word is single-token by construction.
    """
    vocab = tok.get_vocab()  # token_str -> id
    by_letter = defaultdict(list)            # letter -> list of dict(word, token_id, length)
    id_to_word = {}                          # token_id -> word  (slot-eligible only)
    word_to_id = {}                          # word(lower-normalised key uses exact word) -> token_id
    n_alpha = 0
    for token_str, tid in vocab.items():
        decoded = tok.convert_tokens_to_string([token_str])
        word_initial = token_str.startswith(GEMMA_SPACE)
        word = decoded
        if word.startswith(" "):
            word = word[1:]                  # strip exactly ONE leading space
        if len(word) == 0:
            continue
        if not all(c in ALL_ALPHA_LETTERS for c in word):
            continue
        n_alpha += 1
        if not word_initial:
            continue                         # only word-initial tokens carry clean first-letter semantics
        letter = word[0].lower()
        if not ("a" <= letter <= "z"):
            continue
        info = {"word": word, "token_id": int(tid), "length": len(word)}
        by_letter[letter].append(info)
        id_to_word[int(tid)] = word
        word_to_id[word] = int(tid)
    logger.info(f"get_alpha_tokens: {n_alpha} alpha tokens; {len(id_to_word)} slot-eligible word-initial")
    return by_letter, id_to_word, word_to_id


# ----------------------------------------------------------------------------- step 2: pile corpus
def _pile_stream(n_docs: int, max_chars: int):
    """Yield (doc_id, text) for the first n_docs pile docs at the pinned revision.

    Primary: datasets streaming. Fallback: hf_hub_download single shard + zstandard line read.
    """
    try:
        from datasets import load_dataset
        ds = load_dataset(PILE_REPO, split="train", streaming=True, revision=PILE_REV_FULL)
        logger.info("pile: streaming via datasets.load_dataset")
        for i, ex in enumerate(ds):
            if i >= n_docs:
                break
            yield i, (ex["text"] or "")[:max_chars]
        return
    except Exception as e:  # noqa: BLE001
        logger.warning(f"pile streaming failed ({e!r}); falling back to shard download")

    import zstandard as zstd
    from huggingface_hub import hf_hub_download
    shard = hf_hub_download(PILE_REPO, "train/00.jsonl.zst", repo_type="dataset", revision=PILE_REV_FULL)
    logger.info(f"pile: reading shard {shard}")
    dctx = zstd.ZstdDecompressor()
    with open(shard, "rb") as fh, dctx.stream_reader(fh) as reader:
        import io
        text_stream = io.TextIOWrapper(reader, encoding="utf-8")
        for i, line in enumerate(text_stream):
            if i >= n_docs:
                break
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            yield i, (obj.get("text") or "")[:max_chars]


def build_corpus(tok, id_to_word, target_letters, n_docs, max_chars, batch_docs=200):
    """Stream the pile, count global slot-eligible word frequencies, and sample context windows
    for target-letter tokens. Returns (counts[vocab], windows, target_token_ids info)."""
    cache_path = CACHE_DIR / f"corpus_n{n_docs}_mc{max_chars}_{''.join(sorted(target_letters))}.pkl"
    if cache_path.exists():
        logger.info(f"corpus: loading cache {cache_path.name}")
        with open(cache_path, "rb") as f:
            return pickle.load(f)

    os.environ["TOKENIZERS_PARALLELISM"] = "true"
    counts = np.zeros(EXPECTED_VOCAB, dtype=np.int64)

    # boolean mask of target-letter slot-eligible token ids
    is_target = np.zeros(EXPECTED_VOCAB, dtype=bool)
    tid_letter = {}
    for tid, word in id_to_word.items():
        lt = word[0].lower()
        if lt in target_letters:
            is_target[tid] = True
            tid_letter[tid] = lt

    windows = []                                  # list of dict
    win_per_word = defaultdict(int)
    win_per_letter = defaultdict(int)
    target_word_count = defaultdict(lambda: defaultdict(int))  # letter -> word -> count

    t0 = time.time()
    batch_texts, batch_ids = [], []
    docs_done = 0

    def flush():
        nonlocal counts
        if not batch_texts:
            return
        enc = tok(batch_texts, add_special_tokens=False, return_offsets_mapping=True)
        all_ids = enc["input_ids"]
        all_offsets = enc["offset_mapping"]
        # global frequency via bincount over the whole batch
        flat = np.fromiter((t for seq in all_ids for t in seq), dtype=np.int64)
        if flat.size:
            counts += np.bincount(flat, minlength=EXPECTED_VOCAB)
        # window sampling for target tokens
        for ids, offsets, doc_id in zip(all_ids, all_offsets, batch_ids):
            ids_arr = np.asarray(ids, dtype=np.int64)
            if ids_arr.size == 0:
                continue
            hit_mask = is_target[ids_arr]
            if not hit_mask.any():
                continue
            for p in np.nonzero(hit_mask)[0]:
                tid = int(ids_arr[p])
                word = id_to_word[tid]
                lt = tid_letter[tid]
                target_word_count[lt][word] += 1
                if win_per_letter[lt] >= WINDOWS_PER_LETTER_CAP:
                    continue
                if win_per_word[word] >= WINDOWS_PER_WORD_CAP:
                    continue
                s = max(0, int(p) - WIN_LEFT)
                e = min(len(ids), int(p) + WIN_RIGHT + 1)
                win_ids = ids[s:e]
                rel = int(p) - s
                text = tok.decode(win_ids)
                cs = offsets[s][0]
                ce = offsets[e - 1][1]
                # robust char span of the target word WITHIN the decoded window text (indexes `text`)
                approx = len(tok.decode(win_ids[:rel]))
                ws = text.find(word, max(0, approx - 2))
                if ws == -1:
                    ws = text.find(word)
                in_span = [ws, ws + len(word)] if ws != -1 else None
                windows.append({
                    "letter": lt, "word": word, "token_id": tid,
                    "text": text, "rel_token_position": rel,
                    "source_doc_id": int(doc_id), "window_char_span": [int(cs), int(ce)],
                    "in_window_char_span": in_span,
                })
                win_per_word[word] += 1
                win_per_letter[lt] += 1

    for doc_id, text in _pile_stream(n_docs, max_chars):
        batch_texts.append(text)
        batch_ids.append(doc_id)
        if len(batch_texts) >= batch_docs:
            flush()
            docs_done += len(batch_texts)
            batch_texts, batch_ids = [], []
            if docs_done % 2000 == 0:
                rate = docs_done / max(1e-9, time.time() - t0)
                logger.info(f"corpus: {docs_done}/{n_docs} docs ({rate:.0f}/s) "
                            f"windows={len(windows)} per-letter={dict(win_per_letter)}")
    flush()
    docs_done += len(batch_texts)

    result = {
        "counts": counts,
        "windows": windows,
        "target_word_count": {lt: dict(d) for lt, d in target_word_count.items()},
        "n_docs_actual": docs_done,
        "elapsed_s": round(time.time() - t0, 1),
    }
    with open(cache_path, "wb") as f:
        pickle.dump(result, f)
    logger.info(f"corpus: done {docs_done} docs in {result['elapsed_s']}s, {len(windows)} windows; cached")
    return result


# ----------------------------------------------------------------------------- step 3/4: pairs
KNOWN_ABSORBERS = {
    "l": ["lion", "London", "little", "life", "love", "line", "land", "light", "left", "long"],
    "o": ["one", "open", "over", "order", "office", "ocean"],
    "t": ["time", "the", "table", "tree", "town", "table"],
    "i": ["it", "image", "island", "idea", "iron", "info"],
    "d": ["day", "door", "data", "dog", "down", "design"],
}


def select_on_words(letter, by_letter, counts, *, n_on, min_len=3, min_freq=20):
    """Pick natural, common, single-token on-words for a letter: highest pile frequency, length>=3."""
    cands = []
    for info in by_letter.get(letter, []):
        w, tid, ln = info["word"], info["token_id"], info["length"]
        if ln < min_len:
            continue
        f = int(counts[tid])
        if f < min_freq:
            continue
        cands.append((w, tid, ln, f))
    cands.sort(key=lambda x: -x[3])            # by frequency desc
    chosen = cands[:n_on]
    return chosen


def build_offpool(by_letter, counts, target_letters):
    """slot-eligible single-token words NOT starting with any target letter, grouped by length,
    sorted by frequency. Used as content-flip counterparts."""
    by_len = defaultdict(list)
    for lt, infos in by_letter.items():
        for info in infos:
            w, tid, ln = info["word"], info["token_id"], info["length"]
            if ln < 3:
                continue
            f = int(counts[tid])
            if f < 5:
                continue
            # off-pool must not start with the letter it will counter; we keep all and filter at use
            by_len[ln].append((w, tid, ln, f, w[0].lower()))
    for ln in by_len:
        by_len[ln].sort(key=lambda x: -x[3])
    return by_len


def pick_off_word(on_word, on_len, on_freq, target_letter, off_by_len, used_off):
    """closest length (±1), not starting with target letter, closest log-frequency, prefer unused."""
    log_on = math.log10(on_freq + 1)
    best = None
    best_key = None
    for dl in (0, 1, -1, 2, -2):
        ln = on_len + dl
        for (w, tid, wl, f, fl) in off_by_len.get(ln, []):
            if fl == target_letter:
                continue
            score = abs(math.log10(f + 1) - log_on) + abs(dl) * 0.5 + (5.0 if w in used_off else 0.0)
            if best is None or score < best_key:
                best, best_key = (w, tid, wl, f), score
        if best is not None and dl == 0 and best_key < 0.4:
            break
    return best


def build_content_pairs(letter, on_words, off_by_len, word_to_id, rng):
    rows = []
    used_off = set()
    icl = build_icl_block(rng, k=4, exclude={w for w, *_ in on_words})
    cars = carriers()
    pid = 0
    for (w, tid, ln, f) in on_words:
        off = pick_off_word(w, ln, f, letter, off_by_len, used_off)
        if off is None:
            continue
        ow, otid, oln, of_ = off
        used_off.add(ow)
        for (template_id, prefix, suffix) in cars:
            pre = prefix
            pid += 1
            pair_id = f"{letter.upper()}_c_{pid:04d}"
            for role, word, is_on, this_off in (("on", w, 1, ow), ("off", ow, 0, w)):
                first_letter = word[0].lower()
                text = pre + word + suffix
                span = [len(pre), len(pre) + len(word)]
                rows.append(_row(
                    text=text, output=first_letter.upper(), letter=letter, pair_id=pair_id,
                    pair_type="content_flip", role=role, sub_context=w, target_word=word,
                    counterpart_word=this_off, template_id=template_id,
                    label=is_on, first_letter=first_letter, word_char_span=span,
                    fold=fold_of(w),
                ))
        # ICL carrier (separate template id), counterpart preserved
        pid += 1
        pair_id = f"{letter.upper()}_c_{pid:04d}"
        for role, word, is_on, this_off in (("on", w, 1, ow), ("off", ow, 0, w)):
            first_letter = word[0].lower()
            pre = icl                                   # ICL block uses '{w} has the first letter: {L}'
            text = pre + word + " has the first letter:"  # query matches the ICL example format
            span = [len(pre), len(pre) + len(word)]
            rows.append(_row(
                text=text, output=first_letter.upper(), letter=letter, pair_id=pair_id,
                pair_type="content_flip", role=role, sub_context=w, target_word=word,
                counterpart_word=this_off, template_id="t_icl", label=is_on,
                first_letter=first_letter, word_char_span=span, fold=fold_of(w),
            ))
    return rows


def build_surface_pairs(letter, on_words, rng, n_wordpairs):
    rows = []
    cars = carriers()[:5]                     # 5 carriers (verbose, colon, + 3 mention-style)
    # dedupe by lowercase so the two words in a surface flip are genuinely DIFFERENT words
    # (not case-only variants like 'list'/'List', which a judge correctly rejects as the same word)
    words, seen = [], set()
    for (w, *_rest) in on_words:
        if w.lower() in seen:
            continue
        seen.add(w.lower())
        words.append(w)
    pid = 0
    npairs = min(n_wordpairs, len(words) // 2)
    for i in range(npairs):
        wa, wb = words[2 * i], words[2 * i + 1]
        for (template_id, prefix, suffix) in cars:
            pid += 1
            pair_id = f"{letter.upper()}_s_{pid:04d}"
            for role, word, partner in (("var_a", wa, wb), ("var_b", wb, wa)):
                first_letter = word[0].lower()
                text = prefix + word + suffix
                span = [len(prefix), len(prefix) + len(word)]
                rows.append(_row(
                    text=text, output=first_letter.upper(), letter=letter, pair_id=pair_id,
                    pair_type="surface_flip", role=role, sub_context=f"{wa}|{wb}",
                    target_word=word, counterpart_word=partner, template_id=template_id,
                    label=1, first_letter=first_letter, word_char_span=span,
                    fold=fold_of(wa),
                ))
    return rows


def _row(*, text, output, letter, pair_id, pair_type, role, sub_context, target_word,
         counterpart_word, template_id, label, first_letter, fold,
         word_char_span=None, source_doc_id=None, token_position=None,
         window_char_span=None, in_window_char_span=None, target_token_id=None):
    r = {
        "input": text,
        "output": output,
        "metadata_dataset": "first_letter_spelling",
        "metadata_letter": letter.upper(),
        "metadata_pair_id": pair_id,
        "metadata_pair_type": pair_type,
        "metadata_role": role,
        "metadata_sub_context": sub_context,
        "metadata_target_word": target_word,
        "metadata_counterpart_word": counterpart_word,
        "metadata_template_id": template_id,
        "metadata_label_starts_with_target": int(label),
        "metadata_is_single_token": True,
        "metadata_is_slot_eligible": True,
        "metadata_first_letter": first_letter,
        "metadata_fold": int(fold),
    }
    if pair_type in ("content_flip", "surface_flip"):
        # char span of the slotted word within `input`  (pair-only locator)
        r["metadata_word_char_span"] = word_char_span
    else:  # corpus_context
        r["metadata_source_doc_id"] = int(source_doc_id)
        r["metadata_pile_revision"] = PILE_REV_SHORT
        r["metadata_token_position"] = int(token_position)         # target token index WITHIN window ids
        r["metadata_target_token_id"] = int(target_token_id)       # gemma-2-2b token id of the target
        r["metadata_window_char_span"] = window_char_span          # doc-relative char span (provenance)
        r["metadata_target_char_in_window"] = in_window_char_span  # char span of word within `input`
        r["metadata_judge_pass"] = True
    return r


def corpus_rows(windows):
    rows = []
    for w in windows:
        word = w["word"]
        fl = word[0].lower()
        rows.append(_row(
            text=w["text"], output=fl.upper(), letter=w["letter"], pair_id=f"{w['letter'].upper()}_corpus_{len(rows):05d}",
            pair_type="corpus_context", role="occurrence", sub_context=word, target_word=word,
            counterpart_word="", template_id="pile_window", label=1, first_letter=fl,
            fold=fold_of(f"doc{w['source_doc_id']}"),
            source_doc_id=w["source_doc_id"], token_position=w["rel_token_position"],
            window_char_span=w["window_char_span"], in_window_char_span=w.get("in_window_char_span"),
            target_token_id=w["token_id"],
        ))
    return rows


# ----------------------------------------------------------------------------- deterministic validation
def mechanical_validate(all_rows, target_letters):
    """Authoritative, deterministic check of the flip property + span correctness on EVERY pair.
    The flip is guaranteed by construction (first letters come straight from the tokenizer), so
    violations should be ~0; any violation is dropped. Returns (drop_pids, stats)."""
    from collections import defaultdict as _dd
    pid_rows = _dd(list)
    for r in all_rows:
        if r["metadata_pair_type"] in ("content_flip", "surface_flip"):
            pid_rows[r["metadata_pair_id"]].append(r)

    drop_pids = set()
    stats = _dd(lambda: {"checked": 0, "ok": 0, "violations": 0})

    def span_ok(r):
        s, e = r["metadata_word_char_span"]
        return r["input"][s:e] == r["metadata_target_word"]

    for pid, rs in pid_rows.items():
        letter = rs[0]["metadata_letter"].lower()
        ptype = rs[0]["metadata_pair_type"]
        key = f"{rs[0]['metadata_letter']}_{ptype}"
        stats[key]["checked"] += 1
        ok = (len(rs) == 2)
        if ok and ptype == "content_flip":
            on = next((x for x in rs if x["metadata_role"] == "on"), None)
            off = next((x for x in rs if x["metadata_role"] == "off"), None)
            ok = (on is not None and off is not None
                  and on["metadata_first_letter"] == letter
                  and off["metadata_first_letter"] != letter
                  and on["metadata_target_word"].lower() != off["metadata_target_word"].lower()
                  and span_ok(on) and span_ok(off))
        elif ok:  # surface_flip
            a = next((x for x in rs if x["metadata_role"] == "var_a"), None)
            b = next((x for x in rs if x["metadata_role"] == "var_b"), None)
            ok = (a is not None and b is not None
                  and a["metadata_first_letter"] == letter
                  and b["metadata_first_letter"] == letter
                  and a["metadata_target_word"].lower() != b["metadata_target_word"].lower()
                  and span_ok(a) and span_ok(b))
        if ok:
            stats[key]["ok"] += 1
        else:
            stats[key]["violations"] += 1
            drop_pids.add(pid)

    # corpus rows: verify first letter + within-window span
    corpus_stats = {"checked": 0, "ok": 0, "violations": 0}
    for r in all_rows:
        if r["metadata_pair_type"] != "corpus_context":
            continue
        corpus_stats["checked"] += 1
        fl = r["metadata_first_letter"]
        sp = r.get("metadata_target_char_in_window")
        span_good = (sp is not None and r["input"][sp[0]:sp[1]] == r["metadata_target_word"])
        if fl in target_letters and fl == r["metadata_target_word"][0].lower() and span_good:
            corpus_stats["ok"] += 1
        else:
            corpus_stats["violations"] += 1
    stats["corpus_context"] = corpus_stats
    return drop_pids, {k: dict(v) for k, v in stats.items()}


# ----------------------------------------------------------------------------- step 5: LLM judge
async def _fetch_pricing(session, model):
    try:
        async with session.get("https://openrouter.ai/api/v1/models", timeout=30) as resp:
            data = await resp.json()
        for m in data.get("data", []):
            if m.get("id") == model:
                p = m.get("pricing", {})
                return float(p.get("prompt", 0)), float(p.get("completion", 0))
    except Exception as e:  # noqa: BLE001
        logger.warning(f"pricing fetch failed: {e!r}")
    return 0.15e-6, 0.60e-6           # gpt-4o-mini-ish fallback ($/token)


def _judge_prompt(pair_type, letter, x_on, x_off):
    L = letter.upper()
    if pair_type == "content_flip":
        return (f"You validate a minimal pair for a first-letter probing dataset. TARGET letter = '{L}'.\n"
                f"Both texts use the SAME template; only one word (the 'slotted word') differs.\n"
                f"TEXT_ON: {x_on!r}\nTEXT_OFF: {x_off!r}\n"
                f"Step 1: identify the slotted word in each text.\n"
                f"Step 2: PASS requires ALL of:\n"
                f"  (a) the TEXT_ON slotted word begins with '{L}' (case-insensitive);\n"
                f"  (b) the TEXT_OFF slotted word does NOT begin with '{L}' — it may begin with ANY "
                f"other letter, and that is EXPECTED and CORRECT, not a failure;\n"
                f"  (c) both sentences are grammatical English.\n"
                f'Reply ONLY JSON: {{"on_word":"..","off_word":"..","verdict":"pass"|"fail","reason":"<=8 words"}}')
    return (f"You validate a surface-variation pair for a first-letter probing dataset. TARGET letter = '{L}'.\n"
            f"Both texts use the SAME template; only one word (the 'slotted word') differs.\n"
            f"TEXT_A: {x_on!r}\nTEXT_B: {x_off!r}\n"
            f"Step 1: identify the slotted word in each text.\n"
            f"Step 2: PASS requires ALL of:\n"
            f"  (a) BOTH slotted words begin with '{L}' (case-insensitive);\n"
            f"  (b) the two slotted words are DIFFERENT words (compare case-insensitively);\n"
            f"  (c) both sentences are grammatical English.\n"
            f'Reply ONLY JSON: {{"word_a":"..","word_b":"..","verdict":"pass"|"fail","reason":"<=8 words"}}')


async def judge_pairs(pairs_by_pid, sample, model, budget_usd, api_key):
    """pairs_by_pid: dict pid -> dict(pair_type, letter, on_text, off_text). Returns
    dict pid->bool(pass), pass_rate stats, cost."""
    import aiohttp

    pids = list(sample)
    results = {}
    cost = {"prompt_tok": 0, "completion_tok": 0, "usd": 0.0, "n_calls": 0}
    sem = asyncio.Semaphore(12)
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    async with aiohttp.ClientSession(headers=headers) as session:
        pin, pout = await _fetch_pricing(session, model)
        logger.info(f"judge pricing {model}: in=${pin*1e6:.3f}/M out=${pout*1e6:.3f}/M")
        stop = asyncio.Event()

        async def one(pid):
            if stop.is_set():
                return
            info = pairs_by_pid[pid]
            prompt = _judge_prompt(info["pair_type"], info["letter"], info["on_text"], info["off_text"])
            body = {"model": model, "temperature": 0, "max_tokens": 60,
                    "messages": [{"role": "system", "content": "You are a strict data-validation judge."},
                                 {"role": "user", "content": prompt}]}
            for attempt in range(3):
                try:
                    async with sem:
                        async with session.post("https://openrouter.ai/api/v1/chat/completions",
                                                 json=body, timeout=90) as resp:
                            data = await resp.json()
                    if "choices" not in data:
                        logger.debug(f"judge no choices pid={pid}: {str(data)[:160]}")
                        await asyncio.sleep(1.5 * (attempt + 1))
                        continue
                    txt = data["choices"][0]["message"]["content"]
                    usage = data.get("usage", {})
                    cost["prompt_tok"] += usage.get("prompt_tokens", 0)
                    cost["completion_tok"] += usage.get("completion_tokens", 0)
                    cost["usd"] = cost["prompt_tok"] * pin + cost["completion_tok"] * pout
                    cost["n_calls"] += 1
                    verdict, reason = _parse_verdict(txt)
                    results[pid] = (verdict, reason)
                    if cost["usd"] >= budget_usd:
                        logger.warning(f"judge budget ${budget_usd} hit (${cost['usd']:.4f}); stopping")
                        stop.set()
                    return
                except Exception as e:  # noqa: BLE001
                    logger.debug(f"judge err pid={pid} attempt={attempt}: {e!r}")
                    await asyncio.sleep(1.5 * (attempt + 1))
            results[pid] = (None, "request_failed")

        # launch in chunks so the budget event can short-circuit
        tasks = [asyncio.create_task(one(pid)) for pid in pids]
        await asyncio.gather(*tasks, return_exceptions=True)

    return results, cost


def _parse_verdict(txt: str):
    """Return (verdict_bool_or_None, reason_str)."""
    t = txt.strip()
    try:
        start = t.index("{")
        end = t.rindex("}") + 1
        obj = json.loads(t[start:end])
        v = str(obj.get("verdict", "")).lower()
        reason = str(obj.get("reason", ""))[:120]
        if v in ("pass", "fail"):
            return (v == "pass"), reason
    except (ValueError, json.JSONDecodeError):
        pass
    low = t.lower()
    if "pass" in low and "fail" not in low:
        return True, t[:120]
    if "fail" in low and "pass" not in low:
        return False, t[:120]
    return None, t[:120]


# ----------------------------------------------------------------------------- assemble
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--letters", default="l,o,t,i,d")
    ap.add_argument("--n_docs", type=int, default=2000)
    ap.add_argument("--max_chars", type=int, default=20000)
    ap.add_argument("--n_on_primary", type=int, default=70)     # on-words for L
    ap.add_argument("--n_on_secondary", type=int, default=45)
    ap.add_argument("--surf_wordpairs_primary", type=int, default=35)
    ap.add_argument("--surf_wordpairs_secondary", type=int, default=22)
    ap.add_argument("--judge_per", type=int, default=0, help="judge sample per (letter,pair_type); 0=skip")
    ap.add_argument("--judge_model", default="openai/gpt-4o-mini")
    ap.add_argument("--judge_budget", type=float, default=3.0)
    ap.add_argument("--out", default="full_data_out.json")
    args = ap.parse_args()

    set_mem_limit(24.0)
    target_letters = [c.strip().lower() for c in args.letters.split(",") if c.strip()]
    primary = target_letters[0]
    rng = np.random.default_rng(SEED)

    from transformers import AutoTokenizer
    logger.info(f"loading tokenizer {TOKENIZER_ID}")
    tok = AutoTokenizer.from_pretrained(TOKENIZER_ID)
    assert tok.vocab_size == EXPECTED_VOCAB, f"vocab {tok.vocab_size} != {EXPECTED_VOCAB}"
    logger.info(f"tokenizer ok, vocab_size={tok.vocab_size}")

    by_letter, id_to_word, word_to_id = build_vocab(tok)
    for lt in target_letters:
        logger.info(f"letter '{lt}': {len(by_letter.get(lt, []))} slot-eligible word-types")

    corpus = build_corpus(tok, id_to_word, target_letters, args.n_docs, args.max_chars)
    counts = corpus["counts"]
    off_by_len = build_offpool(by_letter, counts, target_letters)

    all_rows = []
    per_letter_counts = {}
    on_words_by_letter = {}
    absorber_candidates = {}
    occ_tables = {}

    for lt in target_letters:
        n_on = args.n_on_primary if lt == primary else args.n_on_secondary
        n_sp = args.surf_wordpairs_primary if lt == primary else args.surf_wordpairs_secondary
        on_words = select_on_words(lt, by_letter, counts, n_on=n_on)
        on_words_by_letter[lt] = [w for (w, *_r) in on_words]
        if len(on_words) < 4:
            logger.warning(f"letter '{lt}' degenerate ({len(on_words)} on-words); skipping pairs")
            continue
        c_rows = build_content_pairs(lt, on_words, off_by_len, word_to_id, rng)
        s_rows = build_surface_pairs(lt, on_words, rng, n_sp)
        all_rows.extend(c_rows)
        all_rows.extend(s_rows)
        per_letter_counts[lt] = {
            "content_flip_rows": len(c_rows), "content_flip_pairs": len(c_rows) // 2,
            "surface_flip_rows": len(s_rows), "surface_flip_pairs": len(s_rows) // 2,
            "n_on_words": len(on_words),
        }
        # occurrence table (top-K) + empirical absorber candidates
        twc = corpus["target_word_count"].get(lt, {})
        top = sorted(twc.items(), key=lambda kv: -kv[1])[:OCC_TABLE_TOPK]
        occ_tables[lt] = [{"word": w, "count": c, "token_id": word_to_id.get(w)} for w, c in top]
        emp = [w for (w, c) in top if len(w) >= 3][:15]
        absorber_candidates[lt] = sorted(set(emp) | set(KNOWN_ABSORBERS.get(lt, [])))

    c_corpus = corpus_rows(corpus["windows"])
    all_rows.extend(c_corpus)
    corpus_per_letter = defaultdict(int)
    for r in c_corpus:
        corpus_per_letter[r["metadata_letter"]] += 1

    logger.info(f"rows: pairs+corpus total={len(all_rows)} (corpus={len(c_corpus)})")

    # ---- deterministic validation (authoritative; drop true violations) -------------------
    mech_drop, mech_stats = mechanical_validate(all_rows, target_letters)
    if mech_drop:
        all_rows = [r for r in all_rows if r["metadata_pair_id"] not in mech_drop]
    logger.info(f"mechanical validation: {json.dumps(mech_stats)} | dropped {len(mech_drop)} pairs")

    # ---- LLM judge (optional, SECONDARY grammaticality/independent audit) ------------------
    judge_stats = {}
    judge_cost = {"usd": 0.0, "n_calls": 0, "prompt_tok": 0, "completion_tok": 0}
    if args.judge_per > 0:
        api_key = os.environ.get("OPENROUTER_API_KEY", "")
        # group rows by pid for content/surface pairs
        pid_rows = defaultdict(list)
        for r in all_rows:
            if r["metadata_pair_type"] in ("content_flip", "surface_flip"):
                pid_rows[r["metadata_pair_id"]].append(r)
        pairs_by_pid = {}
        for pid, rs in pid_rows.items():
            if len(rs) != 2:
                continue
            a = next((x for x in rs if x["metadata_role"] in ("on", "var_a")), rs[0])
            b = next((x for x in rs if x["metadata_role"] in ("off", "var_b")), rs[1])
            pairs_by_pid[pid] = {
                "pair_type": a["metadata_pair_type"], "letter": a["metadata_letter"],
                "on_text": a["input"], "off_text": b["input"],
            }
        # sample per (letter, pair_type)
        buckets = defaultdict(list)
        for pid, info in pairs_by_pid.items():
            buckets[(info["letter"], info["pair_type"])].append(pid)
        sample = []
        for key, pids in buckets.items():
            rng.shuffle(pids)
            sample.extend(pids[:args.judge_per])
        logger.info(f"judging {len(sample)} pairs (model={args.judge_model}, budget=${args.judge_budget})")
        results, judge_cost = asyncio.run(
            judge_pairs(pairs_by_pid, sample, args.judge_model, args.judge_budget, api_key))
        # All judged survivors already passed the deterministic flip check, so a judge "fail" on the
        # flip criteria is a judge FALSE-NEGATIVE. We report the judge pass rate + false-negative rate
        # as a secondary grammaticality/naturalness audit, annotate rows, and do NOT drop on the judge
        # alone (the deterministic validator is authoritative for the flip property).
        bstats = defaultdict(lambda: {"judged": 0, "pass": 0, "fail": 0, "unparsed": 0,
                                      "fail_examples": []})
        alive = {r["metadata_pair_id"] for r in all_rows}
        for pid, (verdict, reason) in results.items():
            if pid not in alive:
                continue
            info = pairs_by_pid[pid]
            k = f"{info['letter']}_{info['pair_type']}"
            bstats[k]["judged"] += 1
            if verdict is True:
                bstats[k]["pass"] += 1
            elif verdict is False:
                bstats[k]["fail"] += 1     # judge false-negative (pair is mechanically valid)
                if len(bstats[k]["fail_examples"]) < 6:
                    bstats[k]["fail_examples"].append(
                        {"on": info["on_text"], "off": info["off_text"], "reason": reason})
            else:
                bstats[k]["unparsed"] += 1
        for k, s in bstats.items():
            denom = max(1, s["pass"] + s["fail"])
            s["pass_rate"] = round(s["pass"] / denom, 4)
            s["judge_false_negative_rate"] = round(s["fail"] / max(1, s["judged"]), 4)
        judge_stats = dict(bstats)
        for r in all_rows:
            pid = r["metadata_pair_id"]
            if pid in results and r["metadata_pair_type"] in ("content_flip", "surface_flip"):
                v = results[pid][0]
                r["metadata_judge_pass"] = bool(v) if v is not None else None
        logger.info(f"judge: secondary audit done (no drops; deterministic is authoritative); "
                    f"cost ${judge_cost['usd']:.4f}")

    # ---- assemble final object ------------------------------------------------------------
    dataset_meta = {
        "name": "first_letter_spelling_absorption_testbed",
        "description": "First-letter-spelling absorption testbed: content-flip + surface-flip minimal "
                       "pairs (tokenizer-anchored) + frozen pile letter-occurrence corpus.",
        "schema_note": "Row metadata is flattened to metadata_* keys (exp_sel_data_out compliant). "
                       "Pairs link via metadata_pair_id + metadata_role; reconstruct (x_on,x_off) to "
                       "compute r_l = a_l(x_on)-a_l(x_off). output = first letter (uppercase).",
        "target_letters": [c.upper() for c in target_letters],
        "primary_letter": primary.upper(),
        "components": {
            "A_content_flip": "starts-with-<L> present vs surface-matched absent (Tier-0 K-proposal + C3 spine)",
            "B_surface_flip": "two different same-first-letter words (unit-level surface-invariance check)",
            "C_corpus": "frozen pile windows + per-token occurrence table (form-free/Chanin diagnostic substrate)",
        },
        "generation_config": {
            "tokenizer_id": TOKENIZER_ID, "expected_vocab": EXPECTED_VOCAB,
            "pile_repo": PILE_REPO, "pile_revision_full": PILE_REV_FULL, "pile_revision_short": PILE_REV_SHORT,
            "n_docs_requested": args.n_docs, "n_docs_actual": corpus["n_docs_actual"],
            "max_chars_per_doc": args.max_chars, "corpus_elapsed_s": corpus["elapsed_s"],
            "get_alpha_tokens": {"allow_leading_space": True, "alpha_set": "a-zA-Z",
                                 "slot_eligible": "word-initial ('▁') AND alpha", "single_token": True},
            "window": {"left": WIN_LEFT, "right": WIN_RIGHT, "per_word_cap": WINDOWS_PER_WORD_CAP,
                       "per_letter_cap": WINDOWS_PER_LETTER_CAP},
            "carriers": [c[0] for c in carriers()] + ["t_icl"],
            "n_folds": N_FOLDS, "fold_rule": "minimal pairs by target_word; corpus by source_doc_id",
            "seed": SEED,
            "usage_contract": {
                "datasets_grouping": "one dataset group per target letter (first_letter_spelling_<L>); "
                                     "each group holds that letter's content_flip + surface_flip + "
                                     "corpus_context rows. Shared tables live in top-level metadata.",
                "pairs": "Group rows by metadata_pair_id; metadata_role in {on,off} (content_flip) or "
                         "{var_a,var_b} (surface_flip). r_l(prompt)=a_l(x_on)-a_l(x_off). "
                         "metadata_word_char_span indexes the slotted word in `input`.",
                "corpus": "metadata_token_position is the target-token index within "
                          "tok(input, add_special_tokens=False) (verified exact on sampled rows: "
                          "ids[token_position]==metadata_target_token_id). metadata_window_char_span is "
                          "the doc-relative provenance span; metadata_target_char_in_window indexes `input`.",
                "output_field": "first letter (uppercase): target letter for on/surface/corpus rows, the "
                                "off-word's actual first letter for off rows; binary in "
                                "metadata_label_starts_with_target.",
            },
        },
        "achieved_counts": {
            "total_examples": len(all_rows),
            "per_letter_pairs": per_letter_counts,
            "corpus_contexts_per_letter": dict(corpus_per_letter),
            "occurrence_table_sizes": {lt: len(v) for lt, v in occ_tables.items()},
        },
        "absorber_candidates": absorber_candidates,
        "on_words_by_letter": on_words_by_letter,
        "occurrence_tables": occ_tables,
        "mechanical_validation": {
            "note": "AUTHORITATIVE deterministic check on every pair: on-word begins with target & off-word "
                    "does not (content_flip); both begin with target & differ (surface_flip); plus "
                    "input[word_char_span]==target_word. The flip is guaranteed by construction (first "
                    "letters taken straight from the gemma-2-2b tokenizer), so violations are dropped.",
            "per_bucket": mech_stats, "pairs_dropped": len(mech_drop),
        },
        "llm_judge": {
            "enabled": args.judge_per > 0, "model": args.judge_model, "per_bucket_sample": args.judge_per,
            "role": "SECONDARY grammaticality/naturalness + independent audit. Survivors already pass the "
                    "deterministic check, so judge 'fail' = judge false-negative; pairs are NOT dropped "
                    "on the judge alone. judge_false_negative_rate quantifies judge unreliability on this "
                    "short-prompt task.",
            "pass_rates": judge_stats, "total_usd": round(judge_cost["usd"], 4),
            "n_calls": judge_cost["n_calls"], "budget_usd": args.judge_budget,
        },
    }
    # Group examples into one dataset per TARGET LETTER (L primary, then O/T/I/D) so the `datasets`
    # array matches target_num_datasets=5; each group holds that letter's content_flip + surface_flip
    # + corpus_context rows. Shared dataset-level tables live in the top-level `metadata`.
    groups = defaultdict(list)
    for r in all_rows:
        groups[r["metadata_letter"]].append(r)
    datasets_list = []
    for lt in target_letters:
        rows = groups.get(lt.upper())
        if rows:
            datasets_list.append({"dataset": f"first_letter_spelling_{lt.upper()}", "examples": rows})
    out = {"metadata": dataset_meta, "datasets": datasets_list}

    out_path = WORKDIR / args.out
    out_path.write_text(json.dumps(out, ensure_ascii=False))
    sz = out_path.stat().st_size / 1e6
    logger.info(f"WROTE {out_path.name}: {len(all_rows)} examples across {len(datasets_list)} "
                f"per-letter datasets ({[d['dataset'] for d in datasets_list]}), {sz:.1f} MB")
    logger.info(f"per-letter pairs: {json.dumps(per_letter_counts)}")
    logger.info(f"corpus contexts: {dict(corpus_per_letter)}")
    print(f"DONE examples={len(all_rows)} size_mb={sz:.1f} judge_usd={judge_cost['usd']:.4f}")


if __name__ == "__main__":
    main()
