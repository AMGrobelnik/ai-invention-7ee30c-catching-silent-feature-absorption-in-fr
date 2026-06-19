#!/usr/bin/env python3
"""Pipeline orchestrator for the Non-Spelling Absorption Testbed.

Generates templated pairs, streams the pile-uncopyrighted diagnostic corpus, optionally
augments+judges with an OpenRouter LLM, precomputes gemma-2-2b token indices, assigns
frozen folds, validates, and writes data_out.json (exp_sel_data_out schema) + schema.json + manifest.json.

Usage:
  python3 pipeline.py --scale smoke         # tiny caps, no/limited LLM, ~1 min  (logic check)
  python3 pipeline.py --scale full          # full caps + LLM augment/judge
  python3 pipeline.py --scale full --no-llm # full templated+corpus, skip all LLM
"""
from __future__ import annotations

import argparse
import asyncio
import io
import json
import os
import random
import re
import time
from collections import Counter, defaultdict
from pathlib import Path

import requests
import zstandard
from loguru import logger

import build_dataset as B
from build_dataset import (
    ALL_COUNTRIES, AMBIG_SET, CITIES, MULTI_SET, NUM_FRAMES, NUM_SURFACE_FRAMES,
    OTHER_ENTITIES, PRIMARY_NUM_SUBS, RE_ANY_DIGIT, SEED, TAX_FRAMES, TAX_SURFACE_FRAMES,
    build_content_pair, build_surface_pair, classify_numbers, find_cities, find_countries,
    find_slot, make_row,
)

HERE = Path(__file__).resolve().parent
OR_URL = "https://openrouter.ai/api/v1/chat/completions"
COST = {"in_tok": 0, "out_tok": 0, "calls": 0, "usd": 0.0, "gen_calls": 0, "judge_calls": 0}

# ----------------------------------------------------------------------------- on-filler pools
def build_on_pools(rng):
    pools = {}
    years = [str(y) for y in range(1500, 2100)]
    rng.shuffle(years)
    pools["year"] = years[:90]
    pcts = ([f"{i}%" for i in range(1, 100)] + ["2.5%", "12.5%", "0.5%", "8.5%", "3.5%",
            "33.3%", "0.1%", "150%", "99.9%"])
    rng.shuffle(pcts)
    pools["percent"] = pcts[:80]
    cur = []
    for sym in ["$", "€", "£", "¥"]:
        for amt in ["15", "45", "99", "240", "750", "1,200", "5,000", "12,500", "87", "9.99",
                    "2,000", "350", "64", "1,050", "120"]:
            cur.append(f"{sym}{amt}")
    cur += ["$2 million", "$3.5 million", "€800,000", "£1.2 billion", "50 dollars", "30 euros"]
    rng.shuffle(cur)
    pools["currency"] = cur[:80]
    months = ["January", "February", "March", "April", "May", "June", "July", "August",
              "September", "October", "November", "December"]
    dates = []
    for _ in range(120):
        m = rng.choice(months); d = rng.randint(1, 28); y = rng.randint(1950, 2024)
        dates.append(f"{m} {d}, {y}")
        dates.append(f"{rng.randint(1,12):02d}/{rng.randint(1,28):02d}/{y}")
        dates.append(f"{y}-{rng.randint(1,12):02d}-{rng.randint(1,28):02d}")
    dates = list(dict.fromkeys(dates))
    rng.shuffle(dates)
    pools["date"] = dates[:90]
    dec = []
    for _ in range(200):
        dec.append(f"{rng.randint(0,99)}.{rng.randint(1,99)}")
    dec = list(dict.fromkeys(dec)); rng.shuffle(dec)
    pools["decimal"] = dec[:60]
    ints = [str(i) for i in range(2, 600) if not (1500 <= i <= 2099)]
    rng.shuffle(ints)
    pools["integer"] = ints[:80]
    commas = []
    for _ in range(200):
        commas.append(f"{rng.randint(1,999)},{rng.randint(0,999):03d}")
        commas.append(f"{rng.randint(1,9)},{rng.randint(0,999):03d},{rng.randint(0,999):03d}")
    commas = list(dict.fromkeys(commas)); rng.shuffle(commas)
    pools["comma_number"] = commas[:60]
    ords = []
    for i in range(1, 200):
        s = "th" if 10 <= i % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(i % 10, "th")
        ords.append(f"{i}{s}")
    rng.shuffle(ords)
    pools["ordinal"] = ords[:60]
    return pools


# ----------------------------------------------------------------------------- templated generators
def gen_numeric_content(rng, targets, on_pools):
    frames_by_sub = defaultdict(list)
    for fr in NUM_FRAMES:
        frames_by_sub[fr[1]].append(fr)
    rows = []
    seen_inputs = set()
    counts = Counter()
    for sub, n_target in targets.items():
        frames = frames_by_sub[sub]
        pool = on_pools[sub][:]
        rng.shuffle(pool)
        made = 0
        for i, on in enumerate(pool):
            if made >= n_target:
                break
            fid, fsub, tmpl, ons, offs = frames[i % len(frames)]
            off = offs[(i // len(frames)) % len(offs)]
            x_on = tmpl.replace("{S}", on)
            if x_on in seen_inputs:
                continue
            seen_inputs.add(x_on)
            pid = f"num_cp_{sub}_{made:04d}"
            rows += build_content_pair(hierarchy="numeric", sub_context=sub, template=tmpl,
                                       on_filler=on, off_filler=off, pair_id=pid,
                                       source="templated", template_id=fid)
            made += 1
            counts[sub] += 1
        logger.info(f"[num content] {sub}: {made}/{n_target} pairs")
    return rows, counts


def gen_taxonomic_content(rng, n_target, on_countries):
    rows = []
    seen = set()
    counts = Counter()
    countries = on_countries[:]
    rng.shuffle(countries)
    frames = TAX_FRAMES[:]
    pid_n = 0
    # iterate frame-major over a country rotation so we spread across many countries
    pairs_per_country = max(1, (n_target // len(countries)) + 1)
    for ci, country in enumerate(countries):
        if pid_n >= n_target:
            break
        chosen = rng.sample(frames, min(pairs_per_country, len(frames)))
        for (fid, tmpl, negfam) in chosen:
            if pid_n >= n_target:
                break
            x_on = tmpl.replace("{S}", country)
            if x_on in seen:
                continue
            seen.add(x_on)
            off = rng.choice(CITIES) if negfam == "city" else rng.choice(OTHER_ENTITIES)
            multi = country in MULTI_SET
            note = "ambiguous_homograph" if country in AMBIG_SET else None
            pid = f"tax_cp_{pid_n:04d}"
            rows += build_content_pair(hierarchy="taxonomic", sub_context=country, template=tmpl,
                                       on_filler=country, off_filler=off, pair_id=pid,
                                       source="templated", template_id=fid, neg_family=negfam,
                                       multi_token=multi, notes=note)
            pid_n += 1
            counts[country] += 1
    logger.info(f"[tax content] {pid_n} pairs across {len(counts)} countries")
    return rows, counts


def gen_numeric_surface(rng, on_pools, per_sub=8):
    rows = []
    seen = set()
    counts = Counter()
    pid_n = 0
    for sub, frames in NUM_SURFACE_FRAMES.items():
        vals = on_pools[sub][:per_sub]
        for v in vals:
            # two disjoint frame pairs from the 4 surface frames -> 2 pairs per value
            fp = [(frames[0], frames[1]), (frames[2], frames[3])]
            for (fa, fb) in fp:
                ta, tb = fa.replace("{S}", v), fb.replace("{S}", v)
                if ta in seen or tb in seen:
                    continue
                seen.add(ta); seen.add(tb)
                pid = f"num_sp_{sub}_{pid_n:04d}"; pid_n += 1
                rows += build_surface_pair(hierarchy="numeric", sub_context=sub, frame_a=fa,
                                           frame_b=fb, value=v, pair_id=pid, source="templated")
                counts[sub] += 1
    logger.info(f"[num surface] {pid_n} pairs")
    return rows, counts


def gen_taxonomic_surface(rng, on_countries, n_target=120):
    rows = []
    seen = set()
    counts = Counter()
    countries = on_countries[:]
    rng.shuffle(countries)
    pid_n = 0
    frames = TAX_SURFACE_FRAMES
    for country in countries:
        if pid_n >= n_target:
            break
        # 3 disjoint frame pairs use all 6 frames once -> no (country,frame) reuse
        idx = list(range(len(frames)))
        rng.shuffle(idx)
        for k in range(0, len(idx) - 1, 2):
            if pid_n >= n_target:
                break
            fa, fb = frames[idx[k]], frames[idx[k + 1]]
            ta, tb = fa.replace("{S}", country), fb.replace("{S}", country)
            if ta in seen or tb in seen:
                continue
            seen.add(ta); seen.add(tb)
            multi = country in MULTI_SET
            pid = f"tax_sp_{pid_n:04d}"; pid_n += 1
            rows += build_surface_pair(hierarchy="taxonomic", sub_context=country, frame_a=fa,
                                       frame_b=fb, value=country, pair_id=pid, source="templated",
                                       multi_token=multi)
            counts[country] += 1
    logger.info(f"[tax surface] {pid_n} pairs across {len(counts)} countries")
    return rows, counts


# ----------------------------------------------------------------------------- corpus streaming
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
WORD_RE = re.compile(r"[A-Za-z]{4,}")


def windows_from_text(text, max_chars=400, max_windows=8):
    text = text[:4000]
    sents = SENT_SPLIT.split(text)
    out = []
    cur = ""
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


def stream_pile_corpus(scale_caps, max_records, rng):
    nc = scale_caps
    num_pos_cap = nc["num_pos"]
    num_pos_cnt = Counter()
    num_neg_cap = nc["num_neg"]; num_neg_cnt = 0
    tax_pos_cap = nc["tax_pos_per_country"]; tax_pos_cnt = Counter()
    tax_pos_total_target = nc["tax_pos_total"]
    tax_top_target = nc["tax_top_target"]
    tax_negc_cap = nc["tax_neg_city"]; tax_negc_cnt = 0
    tax_nege_cap = nc["tax_neg_easy"]; tax_nege_cnt = 0
    rows = []
    seen_hash = set()
    scanned = 0
    t0 = time.time()
    dctx = zstandard.ZstdDecompressor()

    def n_countries_at_cap():
        return sum(1 for c, v in tax_pos_cnt.items() if v >= tax_pos_cap)

    def all_primary_full():
        if any(num_pos_cnt[s] < num_pos_cap[s] for s in num_pos_cap):
            return False
        if num_neg_cnt < num_neg_cap or tax_negc_cnt < tax_negc_cap or tax_nege_cnt < tax_nege_cap:
            return False
        # taxonomic: enough top countries reached the per-country cap, OR overall target hit
        if n_countries_at_cap() < tax_top_target and sum(tax_pos_cnt.values()) < tax_pos_total_target:
            return False
        return True

    stop = False
    for shard in B.PILE_SHARDS:
        if stop:
            break
        url = f"https://huggingface.co/datasets/{B.PILE_REPO}/resolve/{B.PILE_REV}/{shard}"
        logger.info(f"[corpus] opening shard {shard}")
        try:
            r = requests.get(url, stream=True, timeout=120)
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
                    logger.info(f"[corpus] scanned={scanned} rows={len(rows)} "
                                f"num_pos={dict(num_pos_cnt)} num_neg={num_neg_cnt} "
                                f"tax_pos_total={sum(tax_pos_cnt.values())} "
                                f"tax_negc={tax_negc_cnt} tax_nege={tax_nege_cnt} "
                                f"({scanned/(time.time()-t0):.0f} rec/s)")
                if scanned >= max_records or all_primary_full():
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
                # Positives have ABSOLUTE priority over negatives (negatives are abundant and
                # fill from leftover docs). Numeric subs use prefer-rarest (spread -> all eligible);
                # taxonomic countries use prefer-MOST-filled (concentrate -> top ~20 reach the cap).
                best_pos = None
                best_neg = None
                for win in windows_from_text(text):
                    if len(win) < 40:
                        continue
                    alpha = sum(c.isalpha() for c in win)
                    if alpha / max(1, len(win)) < 0.4:
                        continue
                    h = hash(win)
                    if h in seen_hash:
                        continue
                    nums = classify_numbers(win)
                    has_digit = bool(RE_ANY_DIGIT.search(win))
                    countries = find_countries(win)
                    cities = find_cities(win)
                    # ---- positive candidates ----
                    if nums:
                        present = {}
                        for (s, e, sub) in nums:
                            present.setdefault(sub, (s, e))
                        bsub = None
                        for sub, (s, e) in present.items():
                            rem = num_pos_cap[sub] - num_pos_cnt[sub]
                            if rem > 0:
                                need = rem / num_pos_cap[sub]  # prefer rarest (least filled)
                                if bsub is None or need > bsub[0]:
                                    bsub = (need, sub, s, e)
                        if bsub:
                            cand = (bsub[0], "num_pos", win, (bsub[1], bsub[2], bsub[3]), psn, h)
                            if best_pos is None or cand[0] > best_pos[0]:
                                best_pos = cand
                    if countries and sum(tax_pos_cnt.values()) < tax_pos_total_target:
                        bc = None  # (count, need, c, s, e) -> prefer MOST-filled under-cap country
                        for (c, s, e) in countries:
                            rem = tax_pos_cap - tax_pos_cnt[c]
                            if rem > 0:
                                cnt = tax_pos_cnt[c]
                                if bc is None or cnt > bc[0]:
                                    bc = (cnt, rem / tax_pos_cap, c, s, e)
                        if bc:
                            cand = (bc[1], "tax_pos", win, (bc[2], bc[3], bc[4]), psn, h)
                            if best_pos is None or cand[0] > best_pos[0]:
                                best_pos = cand
                    # ---- negative candidates (used only when the doc yields no positive) ----
                    if not has_digit:
                        rem = num_neg_cap - num_neg_cnt
                        if rem > 0:
                            cand = (rem / num_neg_cap, "num_neg", win, None, psn, h)
                            if best_neg is None or cand[0] > best_neg[0]:
                                best_neg = cand
                    if cities and not countries:
                        rem = tax_negc_cap - tax_negc_cnt
                        if rem > 0:
                            c, s, e = cities[0]
                            cand = (rem / tax_negc_cap, "tax_neg_city", win, (c, s, e), psn, h)
                            if best_neg is None or cand[0] > best_neg[0]:
                                best_neg = cand
                    if not countries and not cities:
                        rem = tax_nege_cap - tax_nege_cnt
                        if rem > 0:
                            cand = (rem / tax_nege_cap, "tax_neg_easy", win, None, psn, h)
                            if best_neg is None or cand[0] > best_neg[0]:
                                best_neg = cand
                best = best_pos if best_pos is not None else best_neg
                if best is None:
                    continue
                _, cat, win, payload, psn, h = best
                seen_hash.add(h)
                if cat == "num_pos":
                    sub, s, e = payload
                    rows.append(make_row(input_text=win, output="positive", hierarchy="numeric",
                                row_type="corpus", sub_context=sub, pair_id=None, pair_role=None,
                                target_text=win[s:e], target_char_start=s, target_char_end=e,
                                source="pile_uncopyrighted", pile_set_name=psn))
                    num_pos_cnt[sub] += 1
                elif cat == "num_neg":
                    w, s, e = longest_word_span(win)
                    rows.append(make_row(input_text=win, output="negative", hierarchy="numeric",
                                row_type="corpus", sub_context=None, pair_id=None, pair_role=None,
                                target_text=w, target_char_start=s, target_char_end=e,
                                source="pile_uncopyrighted", pile_set_name=psn, notes="no_digit_negative"))
                    num_neg_cnt += 1
                elif cat == "tax_pos":
                    c, s, e = payload
                    rows.append(make_row(input_text=win, output="positive", hierarchy="taxonomic",
                                row_type="corpus", sub_context=c, pair_id=None, pair_role=None,
                                target_text=win[s:e], target_char_start=s, target_char_end=e,
                                source="pile_uncopyrighted", pile_set_name=psn,
                                multi_token=(c in MULTI_SET),
                                notes="ambiguous_homograph" if c in AMBIG_SET else None))
                    tax_pos_cnt[c] += 1
                elif cat == "tax_neg_city":
                    c, s, e = payload
                    rows.append(make_row(input_text=win, output="negative", hierarchy="taxonomic",
                                row_type="corpus", sub_context=None, pair_id=None, pair_role=None,
                                target_text=win[s:e], target_char_start=s, target_char_end=e,
                                source="pile_uncopyrighted", pile_set_name=psn, neg_family="city",
                                notes=f"city_negative={c}"))
                    tax_negc_cnt += 1
                else:  # tax_neg_easy
                    w, s, e = longest_word_span(win)
                    rows.append(make_row(input_text=win, output="negative", hierarchy="taxonomic",
                                row_type="corpus", sub_context=None, pair_id=None, pair_role=None,
                                target_text=w, target_char_start=s, target_char_end=e,
                                source="pile_uncopyrighted", pile_set_name=psn, neg_family="easy",
                                notes="no_country_negative"))
                    tax_nege_cnt += 1
        logger.info(f"[corpus] finished shard {shard}; scanned={scanned} rows={len(rows)}")
    logger.info(f"[corpus] DONE scanned={scanned} rows={len(rows)} in {time.time()-t0:.0f}s")
    fills = {"num_pos": dict(num_pos_cnt), "num_neg": num_neg_cnt, "tax_pos": dict(tax_pos_cnt),
             "tax_neg_city": tax_negc_cnt, "tax_neg_easy": tax_nege_cnt, "scanned": scanned}
    return rows, fills


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


async def call_llm(session, sem, prompt, kind, max_tokens=900, temperature=0.7, retries=4):
    if COST["usd"] >= B.LLM_BUDGET_STOP:
        return None
    async with sem:
        import aiohttp
        for attempt in range(retries):
            try:
                body = {"model": B.LLM_MODEL,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": temperature, "max_tokens": max_tokens}
                async with session.post(OR_URL, json=body,
                                        headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
                                        timeout=aiohttp.ClientTimeout(total=120)) as resp:
                    data = await resp.json()
                if "choices" not in data:
                    raise ValueError(str(data)[:160])
                txt = data["choices"][0]["message"]["content"]
                u = data.get("usage", {}) or {}
                COST["in_tok"] += u.get("prompt_tokens", 0)
                COST["out_tok"] += u.get("completion_tokens", 0)
                COST["calls"] += 1
                COST[f"{kind}_calls"] += 1
                COST["usd"] = COST["in_tok"] * B.LLM_PRICE_IN + COST["out_tok"] * B.LLM_PRICE_OUT
                return txt
            except Exception as e:
                if attempt == retries - 1:
                    logger.warning(f"LLM {kind} failed: {repr(e)[:140]}")
                    return None
                await asyncio.sleep(1.2 * (attempt + 1))


NUM_SUBDESC = {
    "year": "a 4-digit calendar year such as 1989",
    "percent": "a percentage such as 12% or 3.5%",
    "currency": "a currency amount such as $240 or €1,500",
    "date": "a full calendar date such as March 5, 2021 or 12/25/2020",
}


async def llm_generate_and_judge(content_pairs_for_judge, surface_pairs_for_judge, on_pools,
                                 on_countries, rng, gen_caps):
    import aiohttp
    new_rows = []
    sem = asyncio.Semaphore(16)
    async with aiohttp.ClientSession() as session:
        # ---- generation: numeric carriers ----
        gen_tasks = []
        for sub in PRIMARY_NUM_SUBS:
            p = (f"You write short, natural English sentence templates for a linguistics dataset. "
                 f"Produce {gen_caps['num_carriers']} DIVERSE one-sentence carriers, each containing exactly "
                 f"one slot written as {{S}} where {NUM_SUBDESC[sub]} will be inserted. For each, also give an "
                 f"'off' word: a NON-NUMERIC word or short phrase (NO digits) that fits the SAME slot "
                 f"grammatically so the sentence stays natural when the number is removed. Vary domains "
                 f"(finance, sports, science, news, history, everyday). Return ONLY a strict JSON array of "
                 f'objects: [{{"template": "...{{S}}...", "off": "..."}}]. No prose.')
            gen_tasks.append(("num", sub, call_llm(session, sem, p, "gen", temperature=0.9)))
        # taxonomic carriers
        ptax = (f"Produce {gen_caps['tax_carriers']} diverse one-sentence English carriers, each with exactly one "
                f"slot {{S}} where a COUNTRY name will be inserted. For each, give an 'off' entity that is NOT a "
                f"country (a city, a person, or a company) which fits the same slot grammatically. Vary domains "
                f"(travel, news, sport, economics, history). Return ONLY a strict JSON array: "
                f'[{{"template": "...{{S}}...", "off": "...", "off_type": "city|person|company"}}]. No prose.')
        gen_tasks.append(("tax", None, call_llm(session, sem, ptax, "gen", temperature=0.9)))

        results = await asyncio.gather(*[t[2] for t in gen_tasks])
        gen_meta = [(t[0], t[1]) for t in gen_tasks]

        num_made = 0
        tax_made = 0
        seen_inputs = set()
        for (kind, sub), txt in zip(gen_meta, results):
            parsed = extract_json(txt)
            if not isinstance(parsed, list):
                continue
            if kind == "num":
                pool = on_pools[sub][:]
                rng.shuffle(pool)
                pi = 0
                for obj in parsed:
                    if num_made >= gen_caps["num_total"]:
                        break
                    if not isinstance(obj, dict):
                        continue
                    tmpl = str(obj.get("template", "")).strip()
                    off = str(obj.get("off", "")).strip()
                    if "{S}" not in tmpl or not off or re.search(r"\d", off):
                        continue
                    on = pool[pi % len(pool)]; pi += 1
                    x_on = tmpl.replace("{S}", on)
                    if x_on in seen_inputs:
                        continue
                    seen_inputs.add(x_on)
                    pid = f"num_cp_llm_{sub}_{num_made:04d}"
                    pr = build_content_pair(hierarchy="numeric", sub_context=sub, template=tmpl,
                                            on_filler=on, off_filler=off, pair_id=pid,
                                            source="llm_generated", template_id=f"llm_{sub}")
                    new_rows += pr
                    content_pairs_for_judge.append(pr)
                    num_made += 1
            else:  # taxonomic
                countries = on_countries[:]; rng.shuffle(countries)
                ci = 0
                for obj in parsed:
                    if tax_made >= gen_caps["tax_total"]:
                        break
                    if not isinstance(obj, dict):
                        continue
                    tmpl = str(obj.get("template", "")).strip()
                    off = str(obj.get("off", "")).strip()
                    if "{S}" not in tmpl or not off:
                        continue
                    country = countries[ci % len(countries)]; ci += 1
                    x_on = tmpl.replace("{S}", country)
                    if x_on in seen_inputs:
                        continue
                    seen_inputs.add(x_on)
                    negfam = "city" if obj.get("off_type") == "city" else "other"
                    pid = f"tax_cp_llm_{tax_made:04d}"
                    pr = build_content_pair(hierarchy="taxonomic", sub_context=country, template=tmpl,
                                            on_filler=country, off_filler=off, pair_id=pid,
                                            source="llm_generated", template_id="llm_tax",
                                            neg_family=negfam, multi_token=(country in MULTI_SET))
                    new_rows += pr
                    content_pairs_for_judge.append(pr)
                    tax_made += 1
        logger.info(f"[llm] generated numeric={num_made} taxonomic={tax_made} pairs "
                    f"(cost so far ${COST['usd']:.4f})")

        # ---- judging ----
        async def judge_content(pair):
            x_on = next(r for r in pair if r["metadata_pair_role"] == "x_on")
            x_off = next(r for r in pair if r["metadata_pair_role"] == "x_off")
            concept = ("a number / numeric token (one or more digits)"
                       if x_on["metadata_hierarchy"] == "numeric" else "a country name")
            p = (f"You validate a minimal pair for a dataset. Concept = {concept}. x_on should CONTAIN the "
                 f"concept; x_off should NOT contain it, with everything else surface-matched.\n"
                 f"x_on: {x_on['input']}\nx_off: {x_off['input']}\n"
                 f'Return ONLY strict JSON: {{"content_flipped": <bool true iff x_on has the concept and x_off '
                 f'does not>, "surface_preserved": <bool true iff only the target slot differs>, '
                 f'"grammatical": <bool true iff both sentences are grammatical>, "score": <float 0..1>}}.')
            txt = await call_llm(session, sem, p, "judge", max_tokens=120, temperature=0.0)
            return pair, extract_json(txt)

        async def judge_surface(pair):
            a = next(r for r in pair if r["metadata_pair_role"] == "surface_a")
            b = next(r for r in pair if r["metadata_pair_role"] == "surface_b")
            concept = ("a number / numeric token" if a["metadata_hierarchy"] == "numeric" else "a country name")
            p = (f"Both sentences should CONTAIN the concept ({concept}) and differ only in surface phrasing.\n"
                 f"A: {a['input']}\nB: {b['input']}\n"
                 f'Return ONLY strict JSON: {{"content_flipped": <bool true iff BOTH contain the concept>, '
                 f'"surface_preserved": <bool true iff the phrasing genuinely differs>, "grammatical": <bool>, '
                 f'"score": <float 0..1>}}.')
            txt = await call_llm(session, sem, p, "judge", max_tokens=120, temperature=0.0)
            return pair, extract_json(txt)

        jobs = ([judge_content(p) for p in content_pairs_for_judge]
                + [judge_surface(p) for p in surface_pairs_for_judge])
        logger.info(f"[llm] judging {len(jobs)} pairs ...")
        judged = await asyncio.gather(*jobs)
        n_pass = 0
        for pair, verdict in judged:
            if not isinstance(verdict, dict):
                continue
            cf = bool(verdict.get("content_flipped"))
            sp = bool(verdict.get("surface_preserved"))
            gr = bool(verdict.get("grammatical"))
            sc = verdict.get("score")
            try:
                sc = float(sc)
            except Exception:
                sc = None
            passed = cf and sp and gr
            n_pass += int(passed)
            for r in pair:
                r["metadata_llm_judge_pass"] = passed
                r["metadata_llm_judge_score"] = sc
        logger.info(f"[llm] judged {len(judged)} pairs, pass={n_pass} "
                    f"({n_pass/max(1,len(judged))*100:.1f}%), cost ${COST['usd']:.4f}")
    return new_rows


# ----------------------------------------------------------------------------- tokenization
def add_token_indices(rows):
    try:
        from transformers import AutoTokenizer
        tok = AutoTokenizer.from_pretrained(B.GEMMA_TOKENIZER, token=os.environ.get("HF_TOKEN"))
    except Exception as e:
        logger.warning(f"[token] gemma tokenizer unavailable ({repr(e)[:100]}); token_indices=null")
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
                continue
            if e <= s:  # zero-width (x_off slot): token covering position s
                idxs = [k for k, (a, b) in enumerate(offs) if a <= s < b]
            else:
                idxs = [k for k, (a, b) in enumerate(offs) if a < e and b > s]
            r["metadata_target_token_indices"] = idxs or None
    logger.info(f"[token] gemma-2-2b token indices computed for {len(rows)} rows")
    return True


# ----------------------------------------------------------------------------- folds
def assign_folds(rows, rng):
    # pairs: by pair_id, 70/30 train/test, stratified by (hierarchy, sub_context)
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
    # corpus: 50/50 train/diagnostic stratified by (hierarchy, sub_context|neg_family, output)
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


# ----------------------------------------------------------------------------- main
SCALES = {
    "smoke": dict(
        num_content={"year": 12, "percent": 12, "currency": 12, "date": 12, "decimal": 8,
                     "integer": 10, "comma_number": 6, "ordinal": 6},
        tax_content=40, num_surface_per_sub=2, tax_surface=20,
        corpus=dict(num_pos={"year": 60, "percent": 50, "currency": 50, "date": 50, "decimal": 40,
                             "integer": 60, "comma_number": 30, "ordinal": 30},
                    num_neg=200, tax_pos_per_country=40, tax_pos_total=600,
                    tax_top_target=3, tax_neg_city=120, tax_neg_easy=120),
        max_records=120000,
        gen_caps=dict(num_carriers=4, tax_carriers=6, num_total=16, tax_total=12),
    ),
    "full": dict(
        num_content={"year": 60, "percent": 60, "currency": 60, "date": 60, "decimal": 45,
                     "integer": 60, "comma_number": 35, "ordinal": 35},
        tax_content=260, num_surface_per_sub=8, tax_surface=120,
        corpus=dict(num_pos={"year": 600, "percent": 500, "currency": 500, "date": 500,
                             "decimal": 400, "integer": 600, "comma_number": 300, "ordinal": 300},
                    num_neg=3500, tax_pos_per_country=300, tax_pos_total=15000,
                    tax_top_target=20, tax_neg_city=1800, tax_neg_easy=2400),
        max_records=900_000,
        gen_caps=dict(num_carriers=12, tax_carriers=14, num_total=120, tax_total=80),
    ),
}


@logger.catch(reraise=True)
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scale", choices=["smoke", "full"], default="full")
    ap.add_argument("--no-llm", action="store_true")
    ap.add_argument("--no-corpus", action="store_true")
    args = ap.parse_args()
    cfg = SCALES[args.scale]
    rng = random.Random(SEED)
    logger.info(f"=== BUILD scale={args.scale} no_llm={args.no_llm} seed={SEED} pile_rev={B.PILE_REV} ===")

    on_pools = build_on_pools(rng)
    on_countries = list(ALL_COUNTRIES)

    # ---- templated pairs ----
    rows = []
    numc, numc_counts = gen_numeric_content(rng, cfg["num_content"], on_pools)
    taxc, taxc_counts = gen_taxonomic_content(rng, cfg["tax_content"], on_countries)
    nums, nums_counts = gen_numeric_surface(rng, on_pools, per_sub=cfg["num_surface_per_sub"])
    taxs, taxs_counts = gen_taxonomic_surface(rng, on_countries, n_target=cfg["tax_surface"])
    rows += numc + taxc + nums + taxs

    # gather pairs for judging
    def pairs_of(rows_list, role_on, role_off):
        groups = defaultdict(list)
        for r in rows_list:
            groups[r["metadata_pair_id"]].append(r)
        return list(groups.values())

    content_pairs = pairs_of(numc + taxc, "x_on", "x_off")
    surface_pairs = pairs_of(nums + taxs, "surface_a", "surface_b")
    # spot-judge 20% of templated content + surface
    rng.shuffle(content_pairs); rng.shuffle(surface_pairs)
    content_judge = content_pairs[: max(1, int(0.20 * len(content_pairs)))]
    surface_judge = surface_pairs[: max(1, int(0.20 * len(surface_pairs)))]

    # ---- LLM augment + judge ----
    if not args.no_llm:
        try:
            new_rows = asyncio.run(llm_generate_and_judge(content_judge, surface_judge, on_pools,
                                                          on_countries, rng, cfg["gen_caps"]))
            rows += new_rows
        except Exception as e:
            logger.warning(f"[llm] pipeline error, continuing templated-only: {repr(e)[:160]}")
    else:
        logger.info("[llm] skipped (--no-llm)")

    # ---- corpus ----
    corpus_fills = {}
    if not args.no_corpus:
        crows, corpus_fills = stream_pile_corpus(cfg["corpus"], cfg["max_records"], rng)
        rows += crows
    else:
        logger.info("[corpus] skipped (--no-corpus)")

    # ---- dedup pairs with duplicate POSITIVE inputs (x_off/negatives may legitimately repeat) ----
    rows = dedup_pairs(rows)

    # ---- tokenization ----
    tok_ok = add_token_indices(rows)

    # ---- folds ----
    assign_folds(rows, rng)

    # ---- sanity asserts ----
    run_asserts(rows)

    # ---- assemble + write ----
    write_outputs(rows, args, cfg, corpus_fills, tok_ok, numc_counts, taxc_counts,
                  nums_counts, taxs_counts)
    logger.info(f"=== DONE total_rows={len(rows)} llm_cost=${COST['usd']:.4f} "
                f"(gen={COST['gen_calls']} judge={COST['judge_calls']} calls) ===")


def dedup_pairs(rows):
    """Drop any pair whose POSITIVE input duplicates an already-kept positive input
    (within row_type+hierarchy). x_off / negative carriers MAY legitimately repeat
    (a shared negative anchor across positive variants), so they are not deduped."""
    pg = defaultdict(list)
    others = []
    for r in rows:
        if r["metadata_pair_id"]:
            pg[r["metadata_pair_id"]].append(r)
        else:
            others.append(r)
    seen_pos = set()
    kept = []
    dropped = 0
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
    # pair integrity: exactly the right two roles per pair_id
    pg = defaultdict(list)
    for r in rows:
        if r["metadata_pair_id"]:
            pg[r["metadata_pair_id"]].append(r)
    for pid, grp in pg.items():
        roles = sorted(g["metadata_pair_role"] for g in grp)
        assert roles in (["x_off", "x_on"], ["surface_a", "surface_b"]), (pid, roles)
    # positives have a real target span
    miss = [r for r in rows if r["output"] == "positive"
            and (r["metadata_target_char_start"] is None or r["metadata_target_char_start"] < 0)]
    assert not miss, f"{len(miss)} positives without target span"
    # sub_context null on x_off / pure negatives
    for r in rows:
        if r["output"] == "negative" and r["metadata_pair_role"] in (None, "x_off"):
            assert r["metadata_sub_context"] is None, r
    # POSITIVE inputs unique within (row_type, hierarchy)
    seen_pos = set()
    for r in rows:
        if r["output"] == "positive":
            k = (r["metadata_row_type"], r["metadata_hierarchy"], r["input"])
            assert k not in seen_pos, f"dup positive input: {k[:2]} {r['input'][:60]!r}"
            seen_pos.add(k)
    # (pair_id, pair_role) unique
    seen_pr = set()
    for r in rows:
        if r["metadata_pair_id"]:
            k = (r["metadata_pair_id"], r["metadata_pair_role"])
            assert k not in seen_pr, f"dup (pair_id,role): {k}"
            seen_pr.add(k)
    # target span correctness
    for r in rows:
        if r["metadata_target_text"] and r["metadata_target_char_start"] is not None and r["metadata_target_char_start"] >= 0:
            s, e = r["metadata_target_char_start"], r["metadata_target_char_end"]
            assert r["input"][s:e] == r["metadata_target_text"], \
                (r["input"][s:e], r["metadata_target_text"])
    dup_xoff = len([1 for r in rows if r["metadata_pair_role"] == "x_off"]) - \
        len({r["input"] for r in rows if r["metadata_pair_role"] == "x_off"})
    logger.info(f"[assert] OK ({len(rows)} rows, {len(pg)} pairs; informational: {dup_xoff} repeated x_off carriers)")


def write_outputs(rows, args, cfg, corpus_fills, tok_ok, numc_counts, taxc_counts,
                  nums_counts, taxs_counts):
    # split into 2 datasets by hierarchy
    by_h = defaultdict(list)
    for r in rows:
        by_h[r["metadata_hierarchy"]].append(r)
    datasets = []
    for h in ["numeric", "taxonomic"]:
        if by_h[h]:
            datasets.append({"dataset": f"{h}_absorption", "examples": by_h[h]})

    # per-sub diagnostic readiness
    diag = defaultdict(Counter)
    for r in rows:
        if r["metadata_row_type"] == "corpus" and r["output"] == "positive" and r["metadata_fold"] == "diagnostic":
            diag[r["metadata_hierarchy"]][r["metadata_sub_context"]] += 1
    readiness = {}
    for h, cnts in diag.items():
        readiness[h] = {sub: {"diagnostic_positives": n, "status": ("eligible" if n >= 150 else "descriptive_only")}
                        for sub, n in sorted(cnts.items(), key=lambda x: -x[1])}

    # counts
    def count_by(pred, key):
        c = Counter()
        for r in rows:
            if pred(r):
                c[key(r)] += 1
        return dict(c)

    fold_counts = count_by(lambda r: True, lambda r: r["metadata_fold"])
    type_counts = count_by(lambda r: True, lambda r: (r["metadata_hierarchy"], r["metadata_row_type"]))
    type_counts = {f"{k[0]}/{k[1]}": v for k, v in type_counts.items()}
    corpus_sub_counts = count_by(lambda r: r["metadata_row_type"] == "corpus" and r["output"] == "positive",
                                 lambda r: f"{r['metadata_hierarchy']}/{r['metadata_sub_context']}")
    source_counts = count_by(lambda r: True, lambda r: r["metadata_source"])
    pile_set_counts = count_by(lambda r: r["metadata_source"] == "pile_uncopyrighted",
                               lambda r: r["metadata_pile_set_name"])

    # llm pass rates
    judged = [r for r in rows if r["metadata_llm_judge_pass"] is not None and r["metadata_pair_role"] in ("x_on", "surface_a")]
    pass_rate = (sum(1 for r in judged if r["metadata_llm_judge_pass"]) / len(judged)) if judged else None

    top_meta = {
        "artifact": "non_spelling_absorption_testbed",
        "description": ("Two-hierarchy (NUMERIC + TAXONOMIC) SAE feature-absorption testbed. Each hierarchy "
                        "ships content-flip pairs, surface-flip pairs, and a pile-uncopyrighted diagnostic "
                        "corpus labelled by frozen, model-independent sub-context. No SAE/model computation."),
        "schema": "exp_sel_data_out (flat metadata_* keys); see schema.json for the logical (nested) view",
        "scale": args.scale,
        "seed": SEED,
        "pile_repo": B.PILE_REPO,
        "pile_revision": B.PILE_REV,
        "gemma_tokenizer": B.GEMMA_TOKENIZER,
        "token_indices_present": tok_ok,
        "llm_model": B.LLM_MODEL,
        "llm_cost_usd": round(COST["usd"], 5),
        "llm_calls": COST["calls"],
        "total_rows": len(rows),
    }
    out = {"metadata": top_meta, "datasets": datasets}
    out_path = HERE / "full_data_out.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False))
    logger.info(f"[write] {out_path} ({out_path.stat().st_size/1e6:.2f} MB)")
    # mini/preview are produced by data.py via the aii-json format script (datasets-grouped slicing)

    manifest = {
        **top_meta,
        "fold_counts": fold_counts,
        "rows_by_hierarchy_and_type": type_counts,
        "templated_content_counts": {"numeric": dict(numc_counts), "taxonomic": dict(taxc_counts)},
        "templated_surface_counts": {"numeric": dict(nums_counts), "taxonomic": dict(taxs_counts)},
        "corpus_positive_counts_by_sub": corpus_sub_counts,
        "corpus_fill_summary": corpus_fills,
        "source_counts": source_counts,
        "pile_set_name_counts": pile_set_counts,
        "llm_pair_pass_rate": pass_rate,
        "llm_cost_breakdown": {k: COST[k] for k in ("in_tok", "out_tok", "calls", "gen_calls", "judge_calls", "usd")},
        "absorption_readiness": readiness,
        "design_note": ("Sub-context labels are assigned purely from surface form / regex / gazetteer, "
                        "independent of any SAE latent or model behaviour. Absorption presence/absence is an "
                        "iter-2 empirical finding, NOT baked into this data. The same labelled corpus equally "
                        "supports the honest 'absorption is spelling-specific' null (uniform high parent-probe "
                        "recall across sub-contexts) and a positive finding (sub-context-specific parent holes)."),
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    logger.info("[write] manifest.json")


if __name__ == "__main__":
    main()
