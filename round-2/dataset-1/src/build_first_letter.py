#!/usr/bin/env python3
"""STEP 1 — Enlarge the FIRST-LETTER surface_flip set (590 -> >=1,500; deterministic, $0).

A first-letter surface pair = two DISTINCT single-token slot-eligible words that BOTH start
with the target letter, slotted into an identical carrier template. Concept ('starts-with-X')
is held constant; surface (word + token id) varies. The deterministic structural check is
AUTHORITATIVE.

Word pool: the iter-1 occurrence_tables (already the tokenizer get_alpha_tokens slot-eligible,
single-token, word-initial target-letter set, ranked by pile frequency). New word-pairs are
formed as consecutive disjoint pairs over the ranked pool, skipping any (wa,wb) set already used
by the 590 frozen originals. Each word-pair is emitted in the SAME 5 carriers as iter-1
(carriers()[:5]) -> balanced across carriers by construction. Fold by target_word (fold_of(wa)),
both members in one fold, byte-faithful to iter-1.
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from loguru import logger

import cc

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")

WORK = Path(__file__).resolve().parent
INTER = WORK / "temp" / "intermediate"

TARGET_PER_LETTER = 340     # >= 300 required; 5 letters -> >=1700 total (>=1500 with margin)
MIN_LEN = 3                 # matches iter-1 select_on_words min_len (drops junk subwords)
MIN_FREQ = 20               # matches iter-1 select_on_words min_freq (naturalness)


def fl_row(*, text, output, letter, pair_id, role, sub_context, target_word,
           counterpart_word, template_id, first_letter, fold, word_char_span):
    """Mirror iter-1 first-letter data.py _row() for a surface_flip row."""
    return {
        "input": text,
        "output": output,
        "metadata_dataset": "first_letter_spelling",
        "metadata_letter": letter.upper(),
        "metadata_pair_id": pair_id,
        "metadata_pair_type": "surface_flip",
        "metadata_role": role,
        "metadata_sub_context": sub_context,
        "metadata_target_word": target_word,
        "metadata_counterpart_word": counterpart_word,
        "metadata_template_id": template_id,
        "metadata_label_starts_with_target": 1,
        "metadata_is_single_token": True,
        "metadata_is_slot_eligible": True,
        "metadata_first_letter": first_letter,
        "metadata_fold": int(fold),
        "metadata_word_char_span": word_char_span,
    }


def ranked_pool(entries, letter):
    """Deduped (by lowercase) ranked word list: len>=MIN_LEN, count>=MIN_FREQ, first char==letter.
    Falls back to lower freq floors if the pool would be too small."""
    for min_freq in (MIN_FREQ, 5, 1, 0):
        words, seen = [], set()
        for e in entries:  # entries already sorted by count desc in occurrence_tables
            w = e["word"]
            if len(w) < MIN_LEN:
                continue
            if w[0].lower() != letter:
                continue
            if e["count"] < min_freq:
                continue
            lw = w.lower()
            if lw in seen:
                continue
            seen.add(lw)
            words.append(w)
        if len(words) >= 200:
            logger.info(f"  letter '{letter}': pool={len(words)} (min_freq={min_freq})")
            return words
    logger.info(f"  letter '{letter}': pool={len(words)} (min_freq={min_freq}, floor reached)")
    return words


def make_new_pairs(letter, words, orig_sets, need_wordpairs):
    """Consecutive disjoint word-pairs over the ranked pool, skipping sets already in originals."""
    used = set(orig_sets)
    new_rows = []
    n = 0
    i = 0
    made = 0
    while made < need_wordpairs and i + 1 < len(words):
        wa, wb = words[i], words[i + 1]
        i += 2
        if wa.lower() == wb.lower():
            continue
        fs = frozenset({wa.lower(), wb.lower()})
        if fs in used:
            continue
        used.add(fs)
        made += 1
        fold = cc.fold_of(wa)
        for (template_id, prefix, suffix) in cc.SURFACE_CARRIERS:
            n += 1
            pair_id = f"{letter.upper()}_s2_{n:04d}"
            for role, word, partner in (("var_a", wa, wb), ("var_b", wb, wa)):
                text = prefix + word + suffix
                span = [len(prefix), len(prefix) + len(word)]
                new_rows.append(fl_row(
                    text=text, output=word[0].upper(), letter=letter, pair_id=pair_id,
                    role=role, sub_context=f"{wa}|{wb}", target_word=word,
                    counterpart_word=partner, template_id=template_id,
                    first_letter=word[0].lower(), fold=fold, word_char_span=span))
    return new_rows, made


def validate(new_rows, letters):
    """Authoritative deterministic check on every NEW pair (mirror iter-1 mechanical_validate)."""
    pid_rows = defaultdict(list)
    for r in new_rows:
        pid_rows[r["metadata_pair_id"]].append(r)
    stats = defaultdict(lambda: {"checked": 0, "ok": 0, "violations": 0})

    def span_ok(r):
        s, e = r["metadata_word_char_span"]
        return r["input"][s:e] == r["metadata_target_word"]

    violations = 0
    for pid, rs in pid_rows.items():
        letter = rs[0]["metadata_letter"].lower()
        key = f"{rs[0]['metadata_letter']}_surface_flip"
        stats[key]["checked"] += 1
        a = next((x for x in rs if x["metadata_role"] == "var_a"), None)
        b = next((x for x in rs if x["metadata_role"] == "var_b"), None)
        ok = (len(rs) == 2 and a is not None and b is not None
              and a["metadata_first_letter"] == letter
              and b["metadata_first_letter"] == letter
              and a["metadata_target_word"].lower() != b["metadata_target_word"].lower()
              and span_ok(a) and span_ok(b))
        if ok:
            stats[key]["ok"] += 1
        else:
            stats[key]["violations"] += 1
            violations += 1
    return violations, {k: dict(v) for k, v in stats.items()}


def main():
    fl_orig = json.loads((INTER / "fl_originals.json").read_text())
    pools = json.loads((INTER / "fl_wordpools.json").read_text())
    letters = fl_orig["letters"]
    orig_counts = fl_orig["per_letter_counts"]
    orig_pairsets = {lt: {frozenset(s) for s in sets} for lt, sets in pools["orig_pairsets"].items()}

    all_new = []
    per_letter_new = {}
    for lt in letters:
        orig_pairs = orig_counts[lt]["pairs"]
        words = ranked_pool(pools["wordpools"][lt], lt)
        need_pairs = max(0, TARGET_PER_LETTER - orig_pairs)
        need_wp = -(-need_pairs // len(cc.SURFACE_CARRIERS))  # ceil
        new_rows, made = make_new_pairs(lt, words, orig_pairsets.get(lt, set()), need_wp)
        all_new.extend(new_rows)
        new_pairs = len(new_rows) // 2
        per_letter_new[lt] = {
            "orig_pairs": orig_pairs, "new_wordpairs": made, "new_pairs": new_pairs,
            "total_pairs": orig_pairs + new_pairs, "new_rows": len(new_rows),
            "pool_size": len(words),
        }
        logger.info(f"letter '{lt}': orig={orig_pairs} +new_wp={made} -> +{new_pairs} pairs "
                    f"= {orig_pairs + new_pairs} total")

    violations, vstats = validate(all_new, letters)
    logger.info(f"deterministic validation: violations={violations} | {json.dumps(vstats)}")
    assert violations == 0, f"STRUCTURAL VIOLATIONS={violations} (must be 0 by construction)"

    total_new_pairs = sum(v["new_pairs"] for v in per_letter_new.values())
    total_pairs = sum(v["total_pairs"] for v in per_letter_new.values())
    (INTER / "fl_new_surface.json").write_text(json.dumps({
        "new_rows": all_new,
        "per_letter_new": per_letter_new,
        "violations": violations,
        "validation_stats": vstats,
        "carriers_used": [c[0] for c in cc.SURFACE_CARRIERS],
        "params": {"target_per_letter": TARGET_PER_LETTER, "min_len": MIN_LEN, "min_freq": MIN_FREQ},
    }, ensure_ascii=False))
    logger.info(f"DONE first-letter: +{total_new_pairs} new pairs; superset total={total_pairs} pairs")
    print(f"FL_OK new_pairs={total_new_pairs} total_pairs={total_pairs} violations={violations}")


if __name__ == "__main__":
    main()
