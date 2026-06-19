#!/usr/bin/env python3
"""Pipeline orchestrator for the Safety-Relevant Identity Absorption Testbed (M2' building block).

Generates templated content/surface pairs for FOUR safety-relevant identity hierarchies (nationality /
religion / ethnicity_identity / named_entity_safety), streams the pinned pile-uncopyrighted diagnostic
corpus with a high-precision identity-sense classifier (IDENTITY positive / HOMOGRAPH-DISTRACTOR
competing-sense negative / EASY no-identity negative), optionally streams an identity-rich CC0
civil_comments supplement, optionally augments+judges with OpenRouter LLMs (a DIFFERENT-family judge
extended with a `sense_correct` bool + a corpus sense-precision sample), precomputes gemma-2-2b token
indices, assigns frozen folds, validates, and writes full_data_out.json (exp_sel_data_out schema) +
manifest.json (with the absorption_readiness block).

Usage:
  python3 pipeline.py --scale smoke              # tiny caps, limited LLM, ~1-3 min (logic check)
  python3 pipeline.py --scale full               # full caps + LLM augment/judge/precision (Pile only)
  python3 pipeline.py --scale full --no-llm      # full templated+corpus, skip all LLM
  python3 pipeline.py --scale full --with-civil  # additionally harvest the CC0 civil_comments supplement
"""
from __future__ import annotations

import argparse
import asyncio
import io
import json
import os
import random
import re
import resource
import time
from collections import Counter, defaultdict
from pathlib import Path

import requests
import zstandard
from loguru import logger

import build_dataset as B
from build_dataset import (
    CONTENT_FRAMES, CONTENT_FRAMES_OTHER, DATASET_NAME, ENT_BY_CANON, ENTITIES, GLOSS, HIERARCHIES,
    HOMOGRAPH, JUDGE_CONCEPT, OFF_POOLS, PARENT_CONCEPT, SAFETY_RELEVANT, SEED, STRENGTH,
    SURFACE_FRAMES, COLLISIONS, _ent_fields, any_token, build_content_pair, build_surface_pair,
    detect_competitors, detect_targets, find_slot, make_row,
)

HERE = Path(__file__).resolve().parent
OR_URL = "https://openrouter.ai/api/v1/chat/completions"
COST = {"gen_in": 0, "gen_out": 0, "judge_in": 0, "judge_out": 0,
        "gen_calls": 0, "judge_calls": 0, "calls": 0, "usd": 0.0}


def _usd():
    return (COST["gen_in"] * B.GEN_PRICE_IN + COST["gen_out"] * B.GEN_PRICE_OUT
            + COST["judge_in"] * B.JUDGE_PRICE_IN + COST["judge_out"] * B.JUDGE_PRICE_OUT)


# ----------------------------------------------------------------------------- templated generators
def gen_content(hierarchy, n_target, rng):
    """Content-flip pairs: x_on = identity token (positive), x_off = non-identity filler (negative)."""
    frames = CONTENT_FRAMES[hierarchy]
    entities = [e["surface"] for e in ENTITIES[hierarchy]]
    rng.shuffle(entities)
    rows, seen, counts = [], set(), Counter()
    pid = 0
    per_ent = max(1, n_target // max(1, len(entities)) + 1)
    for ent in entities:
        if pid >= n_target:
            break
        chosen = rng.sample(frames, min(per_ent, len(frames)))
        for (fid, tmpl, negfam) in chosen:
            if pid >= n_target:
                break
            x_on = tmpl.replace("{S}", ent)
            if x_on in seen:
                continue
            seen.add(x_on)
            off = rng.choice(OFF_POOLS[hierarchy])
            pr = build_content_pair(hierarchy=hierarchy, entity=ent, template=tmpl, off_filler=off,
                                    pair_id=f"{hierarchy}_cp_{pid:04d}", source="templated",
                                    template_id=fid, neg_family=negfam)
            rows += pr
            counts[ent] += 1
            pid += 1
    logger.info(f"[content {hierarchy}] {pid} pairs across {len(counts)} entities")
    return rows, counts


def gen_other_group(hierarchy, n_target, rng):
    """Parent-specificity hard negatives: x_on = this hierarchy's identity token (positive);
    x_off = an identity token from ANOTHER hierarchy (negative for THIS parent, read at the filler)."""
    if hierarchy not in CONTENT_FRAMES_OTHER:
        return [], Counter()
    fid, tmpl = CONTENT_FRAMES_OTHER[hierarchy]
    slot = find_slot(tmpl)
    others = OFF_POOLS[f"other_group_for_{hierarchy}"]
    entities = [e["surface"] for e in ENTITIES[hierarchy]]
    rng.shuffle(entities)
    rows, seen, counts = [], set(), Counter()
    pid = 0
    for ent in entities:
        if pid >= n_target:
            break
        other = rng.choice(others)
        x_on = tmpl.replace("{S}", ent)
        x_off = tmpl.replace("{S}", other)
        if x_on in seen or x_off in seen:
            continue
        seen.add(x_on); seen.add(x_off)
        ef = _ent_fields(hierarchy, ent)
        coll = COLLISIONS.get(ent)
        note_on = f"collision: {coll}" if coll else None
        pid_str = f"{hierarchy}_og_{pid:04d}"
        rows.append(make_row(input_text=x_on, output="positive", hierarchy=hierarchy,
                    row_type="content_pair", sub_context=ent, pair_id=pid_str, pair_role="x_on",
                    target_text=ent, target_char_start=slot, target_char_end=slot + len(ent),
                    source="templated", template_id=fid, neg_family="other_group", entity=ent,
                    target_sense=hierarchy, notes=note_on, **ef))
        rows.append(make_row(input_text=x_off, output="negative", hierarchy=hierarchy,
                    row_type="content_pair", sub_context=None, pair_id=pid_str, pair_role="x_off",
                    target_text=other, target_char_start=slot, target_char_end=slot + len(other),
                    source="templated", template_id=fid, neg_family="other_group", entity=None,
                    target_sense=None, homograph_sense=None, dominant_other_sense=None,
                    homograph_strength_val=None, multi_token=(" " in other),
                    notes=f"other_group_filler={other!r} (identity word, NOT a member of "
                          f"'{PARENT_CONCEPT[hierarchy]}')"))
        counts[ent] += 1
        pid += 1
    logger.info(f"[other_group {hierarchy}] {pid} parent-specificity pairs")
    return rows, counts


def gen_surface(hierarchy, n_target, rng):
    frames = SURFACE_FRAMES[hierarchy]
    entities = [e["surface"] for e in ENTITIES[hierarchy]]
    rng.shuffle(entities)
    rows, seen, counts = [], set(), Counter()
    pid = 0
    for ent in entities:
        if pid >= n_target:
            break
        idx = list(range(len(frames)))
        rng.shuffle(idx)
        for k in range(0, len(idx) - 1, 2):
            if pid >= n_target:
                break
            fa, fb = frames[idx[k]], frames[idx[k + 1]]
            ta, tb = fa.replace("{S}", ent), fb.replace("{S}", ent)
            if ta in seen or tb in seen:
                continue
            seen.add(ta); seen.add(tb)
            rows += build_surface_pair(hierarchy=hierarchy, entity=ent, frame_a=fa, frame_b=fb,
                                       pair_id=f"{hierarchy}_sp_{pid:04d}", source="templated")
            counts[ent] += 1
            pid += 1
    logger.info(f"[surface {hierarchy}] {pid} pairs across {len(counts)} entities")
    return rows, counts


# ----------------------------------------------------------------------------- corpus streaming
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
WORD_RE = re.compile(r"[A-Za-z]{4,}")


def windows_from_text(text, max_chars=400, max_windows=8):
    text = text[:4000]
    sents = SENT_SPLIT.split(text)
    out, cur = [], ""
    for s in sents:
        s = s.strip()
        if not s:
            continue
        if len(s) > max_chars:
            cut = s[:max_chars]
            sp = cut.rfind(" ")
            out.append(cut[:sp] if sp > 40 else cut)
        elif len(cur) + len(s) + 1 <= max_chars:
            cur = (cur + " " + s).strip()
        else:
            if cur:
                out.append(cur)
            cur = s
        if len(out) >= max_windows:
            break
    if cur and len(out) < max_windows:
        out.append(cur)
    return out[:max_windows]


def longest_word_span(win):
    best = ""
    for m in WORD_RE.finditer(win):
        if len(m.group(0)) > len(best):
            best = m.group(0)
    if not best:
        return "", -1, -1
    s = win.find(best)
    return best, s, s + len(best)


def _corpus_note(canon, extra=None):
    coll = COLLISIONS.get(canon)
    parts = [extra, (f"collision: {coll}" if coll else None)]
    return "; ".join([x for x in parts if x]) or None


def _make_pos(win, h, canon, txt, s, e, source, psn, identity_label_source=None, extra_note=None):
    ef = _ent_fields(h, canon)
    return make_row(input_text=win, output="positive", hierarchy=h, row_type="corpus",
                    sub_context=canon, pair_id=None, pair_role=None, target_text=txt,
                    target_char_start=s, target_char_end=e, source=source, pile_set_name=psn,
                    entity=canon, target_sense=h, identity_label_source=identity_label_source,
                    notes=_corpus_note(canon, extra_note), **ef)


def _make_comp(win, h, canon, txt, s, e, source, psn):
    # competitor (homograph_distractor) row: homograph_sense True by definition; keep gloss/strength
    return make_row(input_text=win, output="negative", hierarchy=h, row_type="corpus",
                    sub_context=None, pair_id=None, pair_role=None, target_text=txt,
                    target_char_start=s, target_char_end=e, source=source, pile_set_name=psn,
                    neg_family="homograph_distractor", entity=canon, target_sense="competitor",
                    homograph_sense=True, dominant_other_sense=GLOSS.get((h, canon)),
                    homograph_strength_val=STRENGTH.get((h, canon)), multi_token=(" " in canon),
                    notes=_corpus_note(canon, f"competing_sense_token={txt!r}"))


def _make_easy(win, h, source, psn):
    w, s, e = longest_word_span(win)
    if s < 0:
        return None
    return make_row(input_text=win, output="negative", hierarchy=h, row_type="corpus",
                    sub_context=None, pair_id=None, pair_role=None, target_text=w,
                    target_char_start=s, target_char_end=e, source=source, pile_set_name=psn,
                    neg_family="easy", entity=None, target_sense=None, homograph_sense=None,
                    dominant_other_sense=None, homograph_strength_val=None, multi_token=False,
                    notes="no_identity_negative")


def _process_window(win, psn, source, caps, pos_cnt, comp_cnt, comp_ent_cnt, easy_cnt,
                    identity_label_source=None):
    """Classify one window into at most one row (positive > distractor > easy). Returns row or None."""
    per_pos = caps["per_entity_pos"]
    comp_cap = caps["comp_pool_per_h"]
    easy_cap = caps["easy_pool_per_h"]
    targets = detect_targets(win)
    # ---- POSITIVE (absolute priority): rarest under-cap identity entity ----
    best_pos = None
    for (h, canon, txt, s, e) in targets:
        c = pos_cnt[(h, canon)]
        if c < per_pos and (best_pos is None or c < best_pos[0]):
            best_pos = (c, h, canon, txt, s, e)
    if best_pos is not None:
        _, h, canon, txt, s, e = best_pos
        pos_cnt[(h, canon)] += 1
        return _make_pos(win, h, canon, txt, s, e, source, psn, identity_label_source)
    # ---- HOMOGRAPH-DISTRACTOR negative (matched hard control: same token, competing sense) ----
    comps = detect_competitors(win)
    best_comp = None
    for (h, canon, txt, s, e) in comps:
        if comp_cnt[h] < comp_cap:
            ec = comp_ent_cnt[(h, canon)]
            if best_comp is None or ec < best_comp[0]:
                best_comp = (ec, h, canon, txt, s, e)
    if best_comp is not None:
        _, h, canon, txt, s, e = best_comp
        comp_cnt[h] += 1
        comp_ent_cnt[(h, canon)] += 1
        return _make_comp(win, h, canon, txt, s, e, source, psn)
    # ---- EASY negative (no identity/competitor token of ANY hierarchy) ----
    if not any_token(win):
        h = min(HIERARCHIES, key=lambda hh: easy_cnt[hh])
        if easy_cnt[h] < easy_cap:
            row = _make_easy(win, h, source, psn)
            if row is not None:
                easy_cnt[h] += 1
                return row
    return None


def stream_pile_corpus(caps, max_records, wall_clock, rng):
    per_pos = caps["per_entity_pos"]
    comp_cap = caps["comp_pool_per_h"]
    easy_cap = caps["easy_pool_per_h"]
    pos_cnt, comp_cnt, comp_ent_cnt, easy_cnt = Counter(), Counter(), Counter(), Counter()
    rows, seen_hash, scanned = [], set(), 0
    t0 = time.time()
    dctx = zstandard.ZstdDecompressor()
    all_entities = [(h, e["surface"]) for h in HIERARCHIES for e in ENTITIES[h]]
    n_entities = len(all_entities)
    pos_total_target = caps["pos_total_target"]

    def negatives_full():
        return all(comp_cnt[h] >= comp_cap and easy_cnt[h] >= easy_cap for h in HIERARCHIES)

    def positives_saturated():
        n_at_cap = sum(1 for k in all_entities if pos_cnt[k] >= per_pos)
        return n_at_cap >= int(0.90 * n_entities) or sum(pos_cnt.values()) >= pos_total_target

    stop = False
    for shard in B.PILE_SHARDS:
        if stop:
            break
        url = f"https://huggingface.co/datasets/{B.PILE_REPO}/resolve/{B.PILE_REV}/{shard}"
        logger.info(f"[corpus] opening shard {shard}")
        try:
            r = requests.get(url, stream=True, timeout=120,
                             headers={"Authorization": f"Bearer {os.environ.get('HF_TOKEN','')}"}
                             if os.environ.get("HF_TOKEN") else None)
            r.raise_for_status()
        except Exception as e:
            logger.warning(f"[corpus] shard {shard} open failed: {repr(e)[:120]}")
            continue
        with dctx.stream_reader(r.raw) as reader:
            tr = io.TextIOWrapper(reader, encoding="utf-8", errors="replace")
            for line in tr:
                if not line.strip():
                    continue
                scanned += 1
                if scanned % 50000 == 0:
                    el = time.time() - t0
                    logger.info(f"[corpus] scanned={scanned} rows={len(rows)} "
                                f"pos_total={sum(pos_cnt.values())} ent_at_cap="
                                f"{sum(1 for k in all_entities if pos_cnt[k] >= per_pos)}/{n_entities} "
                                f"comp={dict(comp_cnt)} easy={dict(easy_cnt)} ({scanned/max(1,el):.0f} rec/s)")
                if scanned >= max_records or (time.time() - t0) > wall_clock:
                    logger.info(f"[corpus] stop: scanned={scanned} elapsed={time.time()-t0:.0f}s")
                    stop = True
                    break
                if negatives_full() and positives_saturated():
                    logger.info("[corpus] stop: pools saturated")
                    stop = True
                    break
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                text = rec.get("text", "")
                psn = (rec.get("meta") or {}).get("pile_set_name")
                if not text or len(text) < 40:
                    continue
                for win in windows_from_text(text):
                    if len(win) < 40:
                        continue
                    alpha = sum(c.isalpha() for c in win)
                    if alpha / max(1, len(win)) < 0.4:
                        continue
                    hsh = hash(win)
                    if hsh in seen_hash:
                        continue
                    row = _process_window(win, psn, "pile_uncopyrighted", caps,
                                          pos_cnt, comp_cnt, comp_ent_cnt, easy_cnt)
                    if row is not None:
                        seen_hash.add(hsh)
                        rows.append(row)
        logger.info(f"[corpus] finished shard {shard}; scanned={scanned} rows={len(rows)}")
    logger.info(f"[corpus] DONE scanned={scanned} rows={len(rows)} in {time.time()-t0:.0f}s")
    fills = {"pos_by_entity": {f"{h}/{c}": pos_cnt[(h, c)] for (h, c) in all_entities if pos_cnt[(h, c)]},
             "comp_by_hierarchy": dict(comp_cnt), "easy_by_hierarchy": dict(easy_cnt),
             "scanned": scanned, "elapsed_s": round(time.time() - t0, 1)}
    return rows, fills


def stream_civil_corpus(caps, max_records, wall_clock, pos_cnt_seed, rng):
    """OPTIONAL safety-relevant CC0 supplement (google/civil_comments). Identity-rich real comments;
    sub_context STILL assigned by surface form (the toxicity columns are recorded as a corroborating
    metadata_identity_label_source only). Non-blocking: any failure -> return [] and the Pile corpus
    (already sufficient + reproducible) stands alone."""
    try:
        from datasets import load_dataset
    except Exception as e:
        logger.warning(f"[civil] `datasets` unavailable ({repr(e)[:80]}); skipping civil supplement")
        return [], {"loaded": False, "reason": "datasets_unavailable"}
    rows = []
    pos_cnt = Counter(pos_cnt_seed)  # continue filling toward the same per-entity caps as Pile
    comp_cnt, comp_ent_cnt, easy_cnt = Counter(), Counter(), Counter()
    t0 = time.time()
    scanned = 0
    civil_caps = dict(caps)
    civil_caps["easy_pool_per_h"] = 0          # do not harvest easy negatives from comments
    civil_caps["comp_pool_per_h"] = caps["comp_pool_per_h"] // 4
    try:
        ds = load_dataset(B.CIVIL_REPO, split="train", streaming=True)
        for rec in ds:
            scanned += 1
            if scanned >= max_records or (time.time() - t0) > wall_clock:
                logger.info(f"[civil] stop: scanned={scanned} elapsed={time.time()-t0:.0f}s")
                break
            text = (rec.get("text") or "").strip()
            if not text or len(text) < 40:
                continue
            tox = float(rec.get("toxicity") or 0.0)
            ids = "civil_comments:toxicity>=0.5" if tox >= 0.5 else "civil_comments:text"
            for win in windows_from_text(text, max_windows=2):
                if len(win) < 40:
                    continue
                alpha = sum(c.isalpha() for c in win)
                if alpha / max(1, len(win)) < 0.4:
                    continue
                row = _process_window(win, None, "civil_comments", civil_caps,
                                      pos_cnt, comp_cnt, comp_ent_cnt, easy_cnt,
                                      identity_label_source=ids)
                if row is not None and row["output"] == "positive":
                    rows.append(row)   # keep only positives from civil (identity-rich) + a few distractors
                elif row is not None and row["metadata_neg_family"] == "homograph_distractor":
                    rows.append(row)
            if scanned % 20000 == 0:
                logger.info(f"[civil] scanned={scanned} kept={len(rows)} ({scanned/max(1,time.time()-t0):.0f} rec/s)")
    except Exception as e:
        logger.warning(f"[civil] streaming error ({repr(e)[:120]}); keeping {len(rows)} civil rows")
    logger.info(f"[civil] DONE scanned={scanned} kept={len(rows)} in {time.time()-t0:.0f}s")
    return rows, {"loaded": True, "scanned": scanned, "kept": len(rows),
                  "elapsed_s": round(time.time() - t0, 1)}


# ----------------------------------------------------------------------------- LLM (async)
def extract_json(txt):
    if txt is None:
        return None
    t = txt.strip()
    t = re.sub(r"^```(?:json)?", "", t).strip()
    t = re.sub(r"```$", "", t).strip()
    for opener, closer in (("[", "]"), ("{", "}")):
        i = t.find(opener)
        if i >= 0:
            j = t.rfind(closer)
            if j > i:
                try:
                    return json.loads(t[i:j + 1])
                except Exception:
                    pass
    try:
        return json.loads(t)
    except Exception:
        return None


async def call_llm(session, sem, prompt, kind, model, price_in, price_out,
                   max_tokens=900, temperature=0.7, retries=4):
    if _usd() >= B.LLM_BUDGET_STOP:
        return None
    import aiohttp
    async with sem:
        for attempt in range(retries):
            try:
                body = {"model": model, "messages": [{"role": "user", "content": prompt}],
                        "temperature": temperature, "max_tokens": max_tokens}
                async with session.post(OR_URL, json=body,
                                        headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
                                        timeout=aiohttp.ClientTimeout(total=120)) as resp:
                    data = await resp.json()
                if "choices" not in data:
                    raise ValueError(str(data)[:160])
                txt = data["choices"][0]["message"]["content"]
                u = data.get("usage", {}) or {}
                COST[f"{kind}_in"] += u.get("prompt_tokens", 0)
                COST[f"{kind}_out"] += u.get("completion_tokens", 0)
                COST["calls"] += 1
                COST[f"{kind}_calls"] += 1
                COST["usd"] = _usd()
                return txt
            except Exception as e:
                if attempt == retries - 1:
                    logger.warning(f"LLM {kind} ({model}) failed: {repr(e)[:140]}")
                    return None
                await asyncio.sleep(1.2 * (attempt + 1))


GEN_DESC = {
    "nationality": ("a NATIONALITY / demonym used to describe people of a country (e.g. American, "
                    "Polish, Chinese), in its nationality sense",
                    "a NON-nationality filler adjective (e.g. 'local', 'regional', 'modern') grammatical "
                    "in the same slot"),
    "religion": ("a RELIGION or religious-identity group (e.g. Muslim, Christian, Buddhist), in its "
                 "religious sense",
                 "a NON-religion filler (e.g. 'local', 'online', 'rural') grammatical in the same slot"),
    "ethnicity_identity": ("a RACE / ETHNICITY / identity-group term (e.g. Black, White, Asian, Latino, "
                           "Jewish), used in its people/identity sense",
                           "a NON-identity filler adjective (e.g. 'local', 'rural', 'young') grammatical "
                           "in the same slot"),
    "named_entity_safety": ("a well-known PUBLIC FIGURE or ORGANIZATION whose name is also a common word "
                            "(e.g. Apple, Bush, Swift, Amazon), forced into the named-entity sense",
                            "a generic non-named referent (e.g. 'The agency', 'The mayor') grammatical as "
                            "the same subject"),
}


async def llm_generate_and_judge(content_judge, surface_judge, corpus_sample, rng, gen_caps):
    import aiohttp
    new_rows = []
    sem = asyncio.Semaphore(12)
    gkw = dict(model=B.GEN_MODEL, price_in=B.GEN_PRICE_IN, price_out=B.GEN_PRICE_OUT)
    jkw = dict(model=B.JUDGE_MODEL, price_in=B.JUDGE_PRICE_IN, price_out=B.JUDGE_PRICE_OUT)
    async with aiohttp.ClientSession() as session:
        # ---- generation: extra naturalistic carriers per hierarchy ----
        gen_tasks = []
        for h in HIERARCHIES:
            xdesc, offdesc = GEN_DESC[h]
            p = (f"You write short, natural English sentence templates for a linguistics dataset about "
                 f"identifying {JUDGE_CONCEPT[h]}. Produce {gen_caps['carriers']} DIVERSE one-sentence "
                 f"carriers, each containing exactly one slot written as {{S}} where {xdesc} will be "
                 f"inserted, and the surrounding words must FORCE that reading (disambiguate it from "
                 f"other senses of the word). For each, also give an 'off' filler: {offdesc}. Vary "
                 f"domains (news, politics, community, business, everyday). Return ONLY a strict JSON "
                 f'array: [{{"template": "...{{S}}...", "off": "..."}}]. No prose.')
            gen_tasks.append((h, call_llm(session, sem, p, "gen", temperature=0.9, **gkw)))
        results = await asyncio.gather(*[t[1] for t in gen_tasks])

        seen_inputs, made = set(), Counter()
        for (h, _), txt in zip(gen_tasks, results):
            parsed = extract_json(txt)
            if not isinstance(parsed, list):
                continue
            entities = [e["surface"] for e in ENTITIES[h]]
            rng.shuffle(entities)
            ei = 0
            for obj in parsed:
                if made[h] >= gen_caps["per_hierarchy"]:
                    break
                if not isinstance(obj, dict):
                    continue
                tmpl = str(obj.get("template", "")).strip()
                off = str(obj.get("off", "")).strip()
                if "{S}" not in tmpl or not off:
                    continue
                ent = entities[ei % len(entities)]; ei += 1
                x_on = tmpl.replace("{S}", ent)
                if x_on in seen_inputs:
                    continue
                seen_inputs.add(x_on)
                pid = f"{h}_cp_llm_{made[h]:04d}"
                pr = build_content_pair(hierarchy=h, entity=ent, template=tmpl, off_filler=off,
                                        pair_id=pid, source="llm_generated", template_id=f"llm_{h}",
                                        neg_family="non_identity")
                new_rows += pr
                content_judge.append(pr)
                made[h] += 1
        logger.info(f"[llm] generated {dict(made)} content pairs (cost ${_usd():.4f})")

        # ---- judging: content + surface pairs (rubric extended with sense_correct) ----
        async def judge_content(pair):
            x_on = next(r for r in pair if r["metadata_pair_role"] == "x_on")
            x_off = next(r for r in pair if r["metadata_pair_role"] == "x_off")
            h = x_on["metadata_hierarchy"]
            concept = JUDGE_CONCEPT[h]
            p = (f"You validate a minimal pair for a dataset. Concept = '{concept}'. x_on should CONTAIN "
                 f"the concept at the target word; x_off should NOT, with everything else surface-matched.\n"
                 f"target word in x_on = {x_on['metadata_target_text']!r}\n"
                 f"x_on: {x_on['input']}\nx_off: {x_off['input']}\n"
                 f'Return ONLY strict JSON: {{"content_flipped": <bool true iff x_on has the concept and '
                 f'x_off does not>, "surface_preserved": <bool true iff only the target slot differs>, '
                 f'"grammatical": <bool true iff both are grammatical>, "sense_correct": <bool true iff '
                 f'the target word in x_on is UNAMBIGUOUSLY {concept} given the carrier (not a competing '
                 f'sense)>, "score": <float 0..1>}}.')
            txt = await call_llm(session, sem, p, "judge", max_tokens=160, temperature=0.0, **jkw)
            return ("content", pair, extract_json(txt))

        async def judge_surface(pair):
            a = next(r for r in pair if r["metadata_pair_role"] == "surface_a")
            b = next(r for r in pair if r["metadata_pair_role"] == "surface_b")
            h = a["metadata_hierarchy"]
            concept = JUDGE_CONCEPT[h]
            p = (f"Both sentences should CONTAIN the concept '{concept}' at the word "
                 f"{a['metadata_target_text']!r} and differ only in surface phrasing.\n"
                 f"A: {a['input']}\nB: {b['input']}\n"
                 f'Return ONLY strict JSON: {{"content_flipped": <bool true iff BOTH contain the concept>, '
                 f'"surface_preserved": <bool true iff the phrasing genuinely differs>, "grammatical": '
                 f'<bool>, "sense_correct": <bool true iff the word is in its {concept} sense in BOTH>, '
                 f'"score": <float 0..1>}}.')
            txt = await call_llm(session, sem, p, "judge", max_tokens=160, temperature=0.0, **jkw)
            return ("surface", pair, extract_json(txt))

        jobs = [judge_content(p) for p in content_judge] + [judge_surface(p) for p in surface_judge]
        logger.info(f"[llm] judging {len(jobs)} pairs with {B.JUDGE_MODEL} ...")
        judged = await asyncio.gather(*jobs)
        n_pass = 0
        for _kind, pair, verdict in judged:
            if not isinstance(verdict, dict):
                continue
            passed = (bool(verdict.get("content_flipped")) and bool(verdict.get("surface_preserved"))
                      and bool(verdict.get("grammatical")) and bool(verdict.get("sense_correct")))
            sc = verdict.get("score")
            try:
                sc = float(sc)
            except Exception:
                sc = None
            n_pass += int(passed)
            for r in pair:
                r["metadata_llm_judge_pass"] = passed
                r["metadata_llm_judge_score"] = sc
        logger.info(f"[llm] judged {len(judged)} pairs, pass={n_pass} "
                    f"({n_pass/max(1,len(judged))*100:.1f}%), cost ${_usd():.4f}")

        # ---- corpus sense-precision validation sample (MEASURES heuristic precision; never relabels) ----
        prec = {}
        if corpus_sample:
            async def judge_sense(row):
                h = row["metadata_hierarchy"]
                concept = JUDGE_CONCEPT[h]
                p = (f"In the passage below, is the token {row['metadata_target_text']!r} used as "
                     f"{concept} (its identity/target sense), as opposed to a competing sense (a common "
                     f"word, a colour, a place, a person's name, an object)? Passage:\n{row['input']}\n"
                     f'Return ONLY strict JSON: {{"sense_correct": <bool>}}.')
                txt = await call_llm(session, sem, p, "judge", max_tokens=40, temperature=0.0, **jkw)
                return h, extract_json(txt)

            res = await asyncio.gather(*[judge_sense(r) for r in corpus_sample])
            agg = defaultdict(lambda: [0, 0])
            for h, v in res:
                if not isinstance(v, dict) or "sense_correct" not in v:
                    continue
                agg[h][1] += 1
                agg[h][0] += int(bool(v.get("sense_correct")))
            for h, (c, t) in agg.items():
                prec[h] = {"n": t, "n_correct": c, "precision": round(c / t, 3) if t else None}
            logger.info(f"[llm] corpus sense-precision sample: {prec} (cost ${_usd():.4f})")
    return new_rows, prec


# ----------------------------------------------------------------------------- tokenization
def add_token_indices(rows):
    try:
        from transformers import AutoTokenizer
        try:
            tok = AutoTokenizer.from_pretrained(B.GEMMA_TOKENIZER, token=os.environ.get("HF_TOKEN"))
        except Exception:
            tok = AutoTokenizer.from_pretrained("unsloth/gemma-2-2b", token=os.environ.get("HF_TOKEN"))
    except Exception as e:
        logger.warning(f"[token] gemma tokenizer unavailable ({repr(e)[:100]}); token_indices=null")
        for r in rows:
            if r["metadata_multi_token"] is None:
                r["metadata_multi_token"] = (" " in (r["metadata_target_text"] or ""))
        return False
    inputs = [r["input"] for r in rows]
    B_SZ = 512
    for i in range(0, len(inputs), B_SZ):
        chunk = inputs[i:i + B_SZ]
        enc = tok(chunk, return_offsets_mapping=True, add_special_tokens=False)
        for j, offs in enumerate(enc["offset_mapping"]):
            r = rows[i + j]
            s = r["metadata_target_char_start"]; e = r["metadata_target_char_end"]
            if s is None or s < 0:
                r["metadata_multi_token"] = False
                continue
            if e <= s:  # zero-width (x_off slot): token covering position s
                idxs = [k for k, (a, b) in enumerate(offs) if a <= s < b]
            else:
                idxs = [k for k, (a, b) in enumerate(offs) if a < e and b > s]
            r["metadata_target_token_indices"] = idxs or None
            r["metadata_multi_token"] = bool(idxs and len(idxs) > 1)
    logger.info(f"[token] gemma-2-2b token indices computed for {len(rows)} rows")
    return True


# ----------------------------------------------------------------------------- folds
def assign_folds(rows, rng):
    pair_groups = defaultdict(list)
    corpus_rows = []
    for r in rows:
        if r["metadata_pair_id"]:
            pair_groups[r["metadata_pair_id"]].append(r)
        else:
            corpus_rows.append(r)
    strata = defaultdict(list)
    for pid, grp in pair_groups.items():
        on = next((g for g in grp if g["metadata_pair_role"] in ("x_on", "surface_a")), grp[0])
        key = (on["metadata_hierarchy"], on["metadata_sub_context"], on["metadata_row_type"])
        strata[key].append(pid)
    for key, pids in strata.items():
        rng.shuffle(pids)
        ntrain = int(round(0.70 * len(pids)))
        for i, pid in enumerate(pids):
            fold = "train" if i < ntrain else "test"
            for r in pair_groups[pid]:
                r["metadata_fold"] = fold
    # corpus: 50/50 train/diagnostic stratified by (hierarchy, sub_context | NEG_negfam, output)
    cstr = defaultdict(list)
    for r in corpus_rows:
        key = (r["metadata_hierarchy"],
               r["metadata_sub_context"] or ("NEG_" + (r["metadata_neg_family"] or "x")),
               r["output"])
        cstr[key].append(r)
    for key, grp in cstr.items():
        rng.shuffle(grp)
        half = len(grp) // 2
        for i, r in enumerate(grp):
            r["metadata_fold"] = "train" if i < half else "diagnostic"


# ----------------------------------------------------------------------------- dedup + asserts
def dedup_pairs(rows):
    pg = defaultdict(list)
    others = []
    for r in rows:
        if r["metadata_pair_id"]:
            pg[r["metadata_pair_id"]].append(r)
        else:
            others.append(r)
    seen_pos, kept, dropped = set(), [], 0
    for pid, grp in pg.items():
        pos_keys = [(g["metadata_row_type"], g["metadata_hierarchy"], g["input"])
                    for g in grp if g["output"] == "positive"]
        if any(k in seen_pos for k in pos_keys):
            dropped += 1
            continue
        seen_pos.update(pos_keys)
        kept.extend(grp)
    logger.info(f"[dedup] dropped {dropped} pairs with duplicate positive inputs; "
                f"{len(kept)} pair-rows + {len(others)} corpus-rows kept")
    return others + kept


def run_asserts(rows):
    logger.info("[assert] running sanity checks ...")
    for r in rows:
        assert r["output"] in ("positive", "negative"), r["output"]
        assert r["metadata_concept_present"] == (r["output"] == "positive")
        assert r["metadata_parent_concept"] == PARENT_CONCEPT[r["metadata_hierarchy"]]
        assert r["metadata_safety_relevant"] is True
    pg = defaultdict(list)
    for r in rows:
        if r["metadata_pair_id"]:
            pg[r["metadata_pair_id"]].append(r)
    for pid, grp in pg.items():
        roles = sorted(g["metadata_pair_role"] for g in grp)
        assert roles in (["x_off", "x_on"], ["surface_a", "surface_b"]), (pid, roles)
    miss = [r for r in rows if r["output"] == "positive"
            and (r["metadata_target_char_start"] is None or r["metadata_target_char_start"] < 0)]
    assert not miss, f"{len(miss)} positives without target span"
    for r in rows:
        if r["output"] == "negative" and r["metadata_pair_role"] in (None, "x_off"):
            assert r["metadata_sub_context"] is None, r
    # positive corpus/pair char spans match target_text exactly
    for r in rows:
        if r["metadata_target_text"] and r["metadata_target_char_start"] is not None and r["metadata_target_char_start"] >= 0:
            s, e = r["metadata_target_char_start"], r["metadata_target_char_end"]
            if e > s:
                assert r["input"][s:e] == r["metadata_target_text"], (r["input"][s:e], r["metadata_target_text"])
    # positives carry an entity + target_sense; homograph_distractor negatives carry entity + 'competitor'
    for r in rows:
        if r["output"] == "positive":
            assert r["metadata_entity"] and r["metadata_target_sense"] in HIERARCHIES, r
        if r["metadata_neg_family"] == "homograph_distractor":
            assert r["metadata_entity"] and r["metadata_target_sense"] == "competitor", r
    # no duplicate positive inputs within a (row_type, hierarchy); no duplicate (pair_id, role)
    seen_pos, seen_pr = set(), set()
    for r in rows:
        if r["output"] == "positive":
            k = (r["metadata_row_type"], r["metadata_hierarchy"], r["input"])
            assert k not in seen_pos, f"dup positive: {k[:2]} {r['input'][:50]!r}"
            seen_pos.add(k)
        if r["metadata_pair_id"]:
            k = (r["metadata_pair_id"], r["metadata_pair_role"])
            assert k not in seen_pr, f"dup (pair_id,role): {k}"
            seen_pr.add(k)
    # required string-enum metadata is never null (validator forbids missing required keys)
    for r in rows:
        for key in ("metadata_hierarchy", "metadata_row_type", "metadata_source", "metadata_parent_concept"):
            assert isinstance(r[key], str) and r[key], (key, r)
    logger.info(f"[assert] OK ({len(rows)} rows, {len(pg)} pairs)")


# ----------------------------------------------------------------------------- scales
SCALES = {
    "smoke": dict(
        content={"nationality": 24, "religion": 18, "ethnicity_identity": 18, "named_entity_safety": 18},
        other_group={"nationality": 10, "religion": 8, "ethnicity_identity": 8, "named_entity_safety": 0},
        surface={"nationality": 16, "religion": 12, "ethnicity_identity": 12, "named_entity_safety": 12},
        corpus=dict(per_entity_pos=30, comp_pool_per_h=150, easy_pool_per_h=150, pos_total_target=1200),
        max_records=150_000, wall_clock=420,
        gen_caps=dict(carriers=4, per_hierarchy=6), corpus_precision_sample=120,
        civil_max_records=20_000, civil_wall_clock=180,
    ),
    "full": dict(
        content={"nationality": 90, "religion": 60, "ethnicity_identity": 70, "named_entity_safety": 70},
        other_group={"nationality": 28, "religion": 22, "ethnicity_identity": 22, "named_entity_safety": 0},
        surface={"nationality": 56, "religion": 40, "ethnicity_identity": 44, "named_entity_safety": 44},
        corpus=dict(per_entity_pos=300, comp_pool_per_h=2400, easy_pool_per_h=2000, pos_total_target=24000),
        max_records=1_900_000, wall_clock=2100,
        gen_caps=dict(carriers=12, per_hierarchy=30), corpus_precision_sample=220,
        civil_max_records=400_000, civil_wall_clock=600,
    ),
}


@logger.catch(reraise=True)
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scale", choices=["smoke", "full"], default="full")
    ap.add_argument("--no-llm", action="store_true")
    ap.add_argument("--no-corpus", action="store_true")
    ap.add_argument("--with-civil", action="store_true",
                    help="additionally harvest the CC0 google/civil_comments identity-rich supplement")
    args = ap.parse_args()
    try:
        resource.setrlimit(resource.RLIMIT_AS, (24 * 1024**3, 24 * 1024**3))
    except Exception as e:
        logger.warning(f"[rlimit] could not set RLIMIT_AS: {repr(e)[:80]}")
    cfg = SCALES[args.scale]
    rng = random.Random(SEED)
    logger.info(f"=== BUILD scale={args.scale} no_llm={args.no_llm} with_civil={args.with_civil} "
                f"seed={SEED} pile_rev={B.PILE_REV} ===")

    # ---- templated pairs ----
    rows = []
    content_counts, surface_counts = {}, {}
    content_pairs, surface_pairs = [], []
    for h in HIERARCHIES:
        cr, cc = gen_content(h, cfg["content"][h], rng)
        og, ogc = gen_other_group(h, cfg["other_group"][h], rng)
        sr, sc = gen_surface(h, cfg["surface"][h], rng)
        rows += cr + og + sr
        merged = Counter(cc); merged.update(ogc)
        content_counts[h] = dict(merged)
        surface_counts[h] = dict(sc)

        def group(rs):
            g = defaultdict(list)
            for r in rs:
                g[r["metadata_pair_id"]].append(r)
            return list(g.values())
        content_pairs += group(cr) + group(og)
        surface_pairs += group(sr)

    rng.shuffle(content_pairs); rng.shuffle(surface_pairs)
    content_judge = content_pairs[: max(1, int(0.20 * len(content_pairs)))]
    surface_judge = surface_pairs[: max(1, int(0.20 * len(surface_pairs)))]

    # ---- corpus (Pile + optional civil_comments) ----
    corpus_fills, corpus_rows, civil_fills = {}, [], {"loaded": False}
    if not args.no_corpus:
        corpus_rows, corpus_fills = stream_pile_corpus(cfg["corpus"], cfg["max_records"],
                                                       cfg["wall_clock"], rng)
        rows += corpus_rows
        if args.with_civil:
            pos_seed = {(h, c): n for k, n in corpus_fills["pos_by_entity"].items()
                        for h, c in [k.split("/", 1)]}
            civil_rows, civil_fills = stream_civil_corpus(cfg["corpus"], cfg["civil_max_records"],
                                                          cfg["civil_wall_clock"], pos_seed, rng)
            rows += civil_rows
            corpus_rows += civil_rows
    else:
        logger.info("[corpus] skipped (--no-corpus)")

    # ---- LLM augment + judge + corpus sense-precision ----
    sense_precision = {}
    if not args.no_llm:
        pos_by_he = defaultdict(list)
        for r in corpus_rows:
            if r["output"] == "positive":
                pos_by_he[(r["metadata_hierarchy"], r["metadata_entity"])].append(r)
        sample, keys = [], list(pos_by_he.keys())
        rng.shuffle(keys)
        n_target = cfg["corpus_precision_sample"]
        if keys:
            per_key = max(1, n_target // len(keys))
            for k in keys:
                grp = pos_by_he[k]; rng.shuffle(grp)
                sample += grp[:per_key]
            rng.shuffle(sample)
            sample = sample[:n_target]
        try:
            new_rows, sense_precision = asyncio.run(
                llm_generate_and_judge(content_judge, surface_judge, sample, rng, cfg["gen_caps"]))
            rows += new_rows
        except Exception as e:
            logger.warning(f"[llm] pipeline error, continuing templated-only: {repr(e)[:160]}")
    else:
        logger.info("[llm] skipped (--no-llm)")

    rows = dedup_pairs(rows)
    tok_ok = add_token_indices(rows)
    assign_folds(rows, rng)
    run_asserts(rows)
    write_outputs(rows, args, cfg, corpus_fills, civil_fills, tok_ok, content_counts, surface_counts,
                  sense_precision)
    logger.info(f"=== DONE total_rows={len(rows)} llm_cost=${_usd():.4f} "
                f"(gen={COST['gen_calls']} judge={COST['judge_calls']} calls) ===")


def write_outputs(rows, args, cfg, corpus_fills, civil_fills, tok_ok, content_counts, surface_counts,
                  sense_precision):
    by_h = defaultdict(list)
    for r in rows:
        by_h[r["metadata_hierarchy"]].append(r)
    datasets = [{"dataset": DATASET_NAME[h], "examples": by_h[h]} for h in HIERARCHIES if by_h[h]]

    # per-entity diagnostic readiness (>=150 diagnostic-fold identity positives => eligible)
    diag = defaultdict(Counter)
    for r in rows:
        if r["metadata_row_type"] == "corpus" and r["output"] == "positive" and r["metadata_fold"] == "diagnostic":
            diag[r["metadata_hierarchy"]][r["metadata_entity"]] += 1
    readiness, eligible_per_h = {}, Counter()
    for h in HIERARCHIES:
        cnts = diag[h]
        readiness[h] = {}
        for e in ENTITIES[h]:
            ent = e["surface"]
            n = cnts.get(ent, 0)
            status = "eligible" if n >= 150 else "descriptive_only"
            if status == "eligible":
                eligible_per_h[h] += 1
            readiness[h][ent] = {"diagnostic_positives": n, "status": status,
                                 "homograph_sense": e["homograph"],
                                 "dominant_other_sense": e["gloss"],
                                 "homograph_strength": e["strength"]}
        readiness[h] = dict(sorted(readiness[h].items(), key=lambda kv: -kv[1]["diagnostic_positives"]))

    def count_by(pred, key):
        c = Counter()
        for r in rows:
            if pred(r):
                c[key(r)] += 1
        return dict(c)

    fold_counts = count_by(lambda r: True, lambda r: r["metadata_fold"])
    tc = count_by(lambda r: True, lambda r: (r["metadata_hierarchy"], r["metadata_row_type"]))
    type_counts = {f"{k[0]}/{k[1]}": v for k, v in tc.items()}
    corpus_sub_counts = count_by(lambda r: r["metadata_row_type"] == "corpus" and r["output"] == "positive",
                                 lambda r: f"{r['metadata_hierarchy']}/{r['metadata_entity']}")
    neg_family_counts = count_by(lambda r: r["output"] == "negative",
                                 lambda r: f"{r['metadata_hierarchy']}/{r['metadata_neg_family']}")
    source_counts = count_by(lambda r: True, lambda r: r["metadata_source"])
    pile_set_counts = count_by(lambda r: r["metadata_source"] == "pile_uncopyrighted",
                               lambda r: r["metadata_pile_set_name"])
    ids_counts = count_by(lambda r: r["metadata_identity_label_source"] is not None,
                          lambda r: r["metadata_identity_label_source"])

    judged = [r for r in rows if r["metadata_llm_judge_pass"] is not None
              and r["metadata_pair_role"] in ("x_on", "surface_a")]
    pass_rate = (sum(1 for r in judged if r["metadata_llm_judge_pass"]) / len(judged)) if judged else None

    top_meta = {
        "artifact": "safety_relevant_identity_absorption_testbed",
        "description": ("FOUR-hierarchy (NATIONALITY / RELIGION / ETHNICITY-IDENTITY / NAMED-ENTITY) "
                        "safety-relevant identity feature-absorption testbed; a strict structural drop-in "
                        "of the iter-1 taxonomic testbed (gen_art_dataset_2) and the iter-5 homograph "
                        "testbed. Each hierarchy ships content-flip pairs, surface-flip pairs, and a "
                        "pile-uncopyrighted diagnostic corpus labelled by frozen, model-independent "
                        "surface-derived sub-context, PLUS a homograph_distractor matched-negative family "
                        "(same surface token in its competing NON-identity sense) and parent-specificity "
                        "other_group negatives. No SAE/model/activation computation."),
        "BUILDING_BLOCK_NOTE": ("NEXT-ITERATION (M2') BUILDING BLOCK — NOT consumed by this iteration's "
                                "parallel experiments. It lets iteration-6+ answer the safety-relevance "
                                "gate (does feature absorption appear on safety-relevant identity "
                                "attributes?) on a proper corpus instead of rough inline slices."),
        "schema": "exp_sel_data_out (flat metadata_* keys); see schema.json for the logical (nested) view",
        "scale": args.scale,
        "seed": SEED,
        "pile_repo": B.PILE_REPO,
        "pile_revision": B.PILE_REV,
        "civil_supplement_repo": B.CIVIL_REPO,
        "civil_supplement_used": bool(civil_fills.get("loaded")),
        "gemma_tokenizer": B.GEMMA_TOKENIZER,
        "token_indices_present": tok_ok,
        "wordfreq_available": B.WORDFREQ_OK,
        "gen_model": B.GEN_MODEL,
        "judge_model": B.JUDGE_MODEL,
        "llm_cost_usd": round(_usd(), 5),
        "llm_calls": COST["calls"],
        "total_rows": len(rows),
    }
    out = {"metadata": top_meta, "datasets": datasets}
    out_path = HERE / "full_data_out.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False))
    logger.info(f"[write] {out_path} ({out_path.stat().st_size/1e6:.2f} MB)")

    manifest = {
        **top_meta,
        "eligible_entities_per_hierarchy": dict(eligible_per_h),
        "fold_counts": fold_counts,
        "rows_by_hierarchy_and_type": type_counts,
        "templated_content_counts": content_counts,
        "templated_surface_counts": surface_counts,
        "corpus_positive_counts_by_entity": corpus_sub_counts,
        "negative_family_counts": neg_family_counts,
        "corpus_fill_summary": corpus_fills,
        "civil_supplement_summary": civil_fills,
        "source_counts": source_counts,
        "pile_set_name_counts": pile_set_counts,
        "identity_label_source_counts": ids_counts,
        "llm_pair_pass_rate": pass_rate,
        "llm_corpus_sense_precision": sense_precision,
        "llm_cost_breakdown": {k: COST[k] for k in
                               ("gen_in", "gen_out", "judge_in", "judge_out", "gen_calls", "judge_calls", "calls")},
        "llm_cost_usd": round(_usd(), 5),
        "absorption_readiness": readiness,
        "entities_per_hierarchy": {h: [e["surface"] for e in ENTITIES[h]] for h in HIERARCHIES},
        "homograph_entities_per_hierarchy": {h: [e["surface"] for e in ENTITIES[h] if e["homograph"]]
                                             for h in HIERARCHIES},
        "parent_concepts": PARENT_CONCEPT,
        "cross_hierarchy_collisions": COLLISIONS,
        "design_note": ("Sub-context / target-sense / competitor labels are assigned PURELY from surface "
                        "form / gazetteer / high-precision disambiguating local context, independent of any "
                        "SAE latent or model. Absorption presence/absence is an iteration-6+ EMPIRICAL "
                        "finding, NOT baked into this data: the same labelled corpus equally supports the "
                        "honest 'no safety attribute is absorption-structured' null (uniform high parent "
                        "recall across identity sub-contexts) and a positive finding (sub-context-specific "
                        "parent recall holes concentrated on high-strength homographs such as Black / White "
                        "/ Polish). The homograph_distractor family is the matched hard control (the SAME "
                        "token in its competing non-identity sense) that makes a suppressed parent visible; "
                        "other_group negatives are an identity-but-wrong-parent specificity control. "
                        "llm_corpus_sense_precision MEASURES the heuristic identity-sense precision per "
                        "hierarchy on a stratified sample; it does NOT relabel the corpus. The CC0 "
                        "civil_comments supplement (optional) is identity-rich real text whose sub_context "
                        "is STILL surface-derived; its toxicity column is recorded only as "
                        "metadata_identity_label_source corroboration."),
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    logger.info(f"[write] manifest.json  eligible/hierarchy={dict(eligible_per_h)}")


if __name__ == "__main__":
    main()
