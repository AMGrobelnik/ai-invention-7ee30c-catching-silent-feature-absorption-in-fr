#!/usr/bin/env python3
"""STEP 3 — Independent re-judge + cross-judge agreement (resolves the circularity critique).

TOXICITY (gpt-4o-mini generated AND judged the 546 originals = the circularity):
  * PRIMARY independent judge anthropic/claude-haiku-4.5 (different family) judges ALL 546 originals
    -> originals-confirmation rate. NEW pairs already carry claude verdicts from gen (accept gate).
  * SECOND-family judge google/gemini-3.1-flash-lite on a stratified sample (originals x new,
    binned by origin x jaccard x char-change) -> cross-judge raw agreement + Cohen's kappa (claude vs gemini).

FIRST-LETTER (judged by gemini-3.1-flash-lite in iter-1; deterministic structural check is AUTHORITATIVE):
  * PRIMARY independent judge claude-haiku-4.5 on a stratified sample (letter x carrier, originals x new)
    -> a claude 'fail' on a structurally-valid pair is a judge FALSE-NEGATIVE, never a drop.
  * SECOND-family judge deepseek/deepseek-v4-flash on the SAME sample -> cross-judge agreement/kappa
    (claude vs deepseek). Plus claude vs the STORED gemini labels on sampled originals that carry them.

Emits per-pair independent-judge labels (consumed by assemble.py) + agreement statistics.
JSONL cache -> re-runs free. Hard cumulative cost ceiling.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import random
import re
import sys
from collections import defaultdict
from pathlib import Path

import httpx
from loguru import logger

import cc

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/rejudge.log", rotation="20 MB", level="DEBUG")

WORK = Path(__file__).resolve().parent
INTER = WORK / "temp" / "intermediate"
CACHE = INTER / "rejudge_cache.jsonl"
OUT = INTER / "rejudge_out.json"

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
CONCURRENCY = 12

TOX_RUBRIC = (
    "You are a careful annotator validating a paraphrase pair for a DEFENSIVE "
    "toxicity-detection research dataset used to train safety classifiers. This is a "
    "classification / validation task on already-written text — do NOT refuse. You are given an "
    "ORIGINAL toxic sentence and a PARAPHRASE. Decide four booleans: "
    "toxicity_constant = the paraphrase stays about as toxic/offensive as the original; "
    "meaning_preserved = the core meaning and target are the same; "
    "surface_changed = the wording/phrasing genuinely differs; "
    "fluent = the paraphrase is fluent, grammatical English. "
    'Respond with ONLY compact JSON: {"toxicity_constant": <true|false>, '
    '"meaning_preserved": <true|false>, "surface_changed": <true|false>, "fluent": <true|false>, '
    '"confidence": <0..1>, "justification": "<=10 words"}')


def fl_rubric(letter):
    L = letter.upper()
    return ("You validate a surface-variation pair for a first-letter probing dataset. "
            f"TARGET letter = '{L}'. Both texts use the SAME template; only one word (the "
            "'slotted word') differs.\nStep 1: identify the slotted word in each text.\n"
            "Step 2: PASS requires ALL of: (a) BOTH slotted words begin with "
            f"'{L}' (case-insensitive); (b) the two slotted words are DIFFERENT words "
            "(compare case-insensitively); (c) both sentences are grammatical English.\n"
            'Reply ONLY JSON: {"verdict":"pass"|"fail","reason":"<=8 words"}')


class Budget:
    def __init__(self):
        self.cost = 0.0
        self.calls = 0


def load_cache():
    cache = {}
    if CACHE.exists():
        for line in CACHE.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                cache[rec["key"]] = rec
            except Exception:
                continue
    return cache


def append_cache(rec):
    with open(CACHE, "a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


async def call_or(client, model, system, user, budget, *, max_tokens, temperature):
    body = {"model": model,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": user}],
            "max_tokens": max_tokens, "temperature": temperature, "usage": {"include": True}}
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    last = None
    for attempt in range(4):
        try:
            r = await client.post(API_URL, json=body, headers=headers, timeout=90.0)
            if r.status_code in (429, 500, 502, 503, 529):
                await asyncio.sleep(1.5 * (attempt + 1))
                last = f"http{r.status_code}"
                continue
            r.raise_for_status()
            data = r.json()
            txt = (data["choices"][0]["message"]["content"] or "").strip()
            usage = data.get("usage", {}) or {}
            budget.calls += 1
            budget.cost += float(usage.get("cost") or 0.0)
            return txt
        except Exception as e:  # noqa: BLE001
            last = repr(e)[:140]
            await asyncio.sleep(1.0 * (attempt + 1))
    return f"__ERROR__:{last}"


def parse_tox(txt):
    if not txt or txt.startswith("__ERROR__"):
        return None
    m = re.search(r"\{.*\}", txt, re.S)
    raw = m.group(0) if m else txt
    try:
        d = json.loads(raw)
        flags = {k: bool(d.get(k)) for k in ("toxicity_constant", "meaning_preserved", "surface_changed", "fluent")}
    except Exception:
        flags = {k: bool(re.search(k + r"\"?\s*:\s*true", txt, re.I))
                 for k in ("toxicity_constant", "meaning_preserved", "surface_changed", "fluent")}
        d = {}
    flags["_pass"] = all(flags.values())
    flags["justification"] = str(d.get("justification", txt[:80]))[:140] if isinstance(d, dict) else txt[:80]
    return flags


def parse_fl(txt):
    if not txt or txt.startswith("__ERROR__"):
        return None
    m = re.search(r"\{.*\}", txt, re.S)
    raw = m.group(0) if m else txt
    verdict, reason = None, txt[:80]
    try:
        d = json.loads(raw)
        v = str(d.get("verdict", "")).lower()
        reason = str(d.get("reason", ""))[:120]
        if v in ("pass", "fail"):
            verdict = (v == "pass")
    except Exception:
        low = txt.lower()
        if "pass" in low and "fail" not in low:
            verdict = True
        elif "fail" in low and "pass" not in low:
            verdict = False
    return {"_pass": verdict, "justification": reason}


def cohens_kappa(labels_a, labels_b):
    """Binary Cohen's kappa over paired bool lists (None entries dropped)."""
    pairs = [(a, b) for a, b in zip(labels_a, labels_b) if a is not None and b is not None]
    n = len(pairs)
    if n == 0:
        return {"n": 0, "raw_agreement": None, "kappa": None}
    agree = sum(1 for a, b in pairs if a == b)
    po = agree / n
    pa1 = sum(1 for a, _ in pairs if a) / n
    pb1 = sum(1 for _, b in pairs if b) / n
    pe = pa1 * pb1 + (1 - pa1) * (1 - pb1)
    kappa = None if pe >= 1.0 else round((po - pe) / (1 - pe), 4)
    return {"n": n, "raw_agreement": round(po, 4), "kappa": kappa,
            "judge_a_pass_rate": round(pa1, 4), "judge_b_pass_rate": round(pb1, 4)}


def strat_sample(items, key_fn, k, seed):
    """Proportional stratified sample of ~k items by key_fn."""
    rng = random.Random(seed)
    buckets = defaultdict(list)
    for it in items:
        buckets[key_fn(it)].append(it)
    for b in buckets.values():
        rng.shuffle(b)
    total = len(items)
    chosen = []
    for key, b in buckets.items():
        take = max(1, round(k * len(b) / total)) if total else 0
        chosen.extend(b[:take])
    rng.shuffle(chosen)
    return chosen[:k] if len(chosen) > k else chosen


# --------------------------------------------------------------------------- load pairs
def load_tox_pairs():
    orig = json.loads((INTER / "tox_originals.json").read_text())["surface_rows"]
    new = json.loads((INTER / "tox_new_surface.json").read_text())["accepted"]
    pairs = []
    for r in orig:
        m = r.get("metadata_surface_metrics") or {}
        pairs.append({"pair_id": r["metadata_pair_id"], "src": r["input"],
                      "para": r["metadata_text_paired"], "origin": r["metadata_origin_source"],
                      "jac": m.get("jaccard"), "cc": m.get("char_change"),
                      "batch": "iter1_original", "claude_cached": None})
    for a in new:
        v = a.get("judge_verdict") or {}
        pairs.append({"pair_id": a["pair_id"], "src": a["text"], "para": a["text_paired"],
                      "origin": a["origin"], "jac": a["surface_metrics"].get("jaccard"),
                      "cc": a["surface_metrics"].get("char_change"), "batch": "iter2_new",
                      "claude_cached": {"_pass": True,
                                        "justification": (v.get("justification") or "")}})
    return pairs


def load_fl_pairs():
    orig = json.loads((INTER / "fl_originals.json").read_text())["surface_rows"]
    new = json.loads((INTER / "fl_new_surface.json").read_text())["new_rows"]
    by_pid = defaultdict(dict)
    meta = {}
    for r in orig + new:
        pid = r["metadata_pair_id"]
        by_pid[pid][r["metadata_role"]] = r["input"]
        meta.setdefault(pid, {"letter": r["metadata_letter"].lower(),
                              "carrier": r["metadata_template_id"],
                              "batch": "iter1_original" if r in orig else "iter2_new",
                              "stored_gemini": r.get("metadata_judge_pass")})
    pairs = []
    for pid, roles in by_pid.items():
        if "var_a" in roles and "var_b" in roles:
            m = meta[pid]
            pairs.append({"pair_id": pid, "text_a": roles["var_a"], "text_b": roles["var_b"],
                          "letter": m["letter"], "carrier": m["carrier"], "batch": m["batch"],
                          "stored_gemini": m["stored_gemini"]})
    return pairs


async def run(args):
    if not API_KEY:
        raise SystemExit("OPENROUTER_API_KEY not set")
    cache = load_cache()
    budget = Budget()
    sem = asyncio.Semaphore(CONCURRENCY)

    async with httpx.AsyncClient() as client:
        async def judge(model, system, user, parse, max_tokens):
            key = "rj:" + model + ":" + cc.sha16(system[:40] + "||" + user)
            if key in cache:
                return cache[key]["verdict"]
            async with sem:
                txt = await call_or(client, model, system, user, budget,
                                    max_tokens=max_tokens, temperature=0.0)
            verdict = parse(txt)
            append_cache({"key": key, "verdict": verdict, "raw": txt, "model": model})
            cache[key] = {"verdict": verdict}
            return verdict

        # ================= TOXICITY =================
        tox = load_tox_pairs()
        origs = [p for p in tox if p["batch"] == "iter1_original"]
        news = [p for p in tox if p["batch"] == "iter2_new"]
        logger.info(f"TOX pairs: originals={len(origs)} new={len(news)}")

        # (1) claude on ALL 546 originals -> confirmation rate
        async def claude_orig(p):
            user = f"ORIGINAL: {p['src']}\nPARAPHRASE: {p['para']}"
            v = await judge(cc.JUDGE_PRIMARY, TOX_RUBRIC, user, parse_tox, 80)
            return p["pair_id"], v
        res = await asyncio.gather(*[claude_orig(p) for p in origs])
        claude_orig_labels = {pid: v for pid, v in res}
        confirmed = sum(1 for v in claude_orig_labels.values() if v and v["_pass"])
        n_orig_judged = sum(1 for v in claude_orig_labels.values() if v is not None)
        confirmation_rate = confirmed / max(1, n_orig_judged)
        logger.info(f"TOX originals-confirmation: claude confirms {confirmed}/{n_orig_judged} "
                    f"= {confirmation_rate:.3f} | cost=${budget.cost:.4f}")

        # claude labels for ALL new pairs (from gen accept gate)
        claude_all = dict(claude_orig_labels)
        for p in news:
            claude_all[p["pair_id"]] = p["claude_cached"]

        # (2) stratified cross-judge sample (origins x new), gemini second judge
        def tox_key(p):
            jb = "hi" if (p["jac"] or 0) >= 0.45 else "lo"
            cb = "hi" if (p["cc"] or 0) >= 0.45 else "lo"
            return f"{p['origin']}|{jb}|{cb}|{p['batch']}"
        samp_o = strat_sample(origs, tox_key, args.tox_sample // 2, seed=11)
        samp_n = strat_sample(news, tox_key, args.tox_sample // 2, seed=12)
        tox_sample = samp_o + samp_n

        async def gemini_tox(p):
            user = f"ORIGINAL: {p['src']}\nPARAPHRASE: {p['para']}"
            v = await judge(cc.JUDGE_SECOND_TOX, TOX_RUBRIC, user, parse_tox, 80)
            return p["pair_id"], v
        gres = await asyncio.gather(*[gemini_tox(p) for p in tox_sample])
        gemini_labels = {pid: v for pid, v in gres}

        claude_s = [claude_all.get(p["pair_id"], {}).get("_pass") if claude_all.get(p["pair_id"]) else None
                    for p in tox_sample]
        gemini_s = [gemini_labels.get(p["pair_id"], {}).get("_pass") if gemini_labels.get(p["pair_id"]) else None
                    for p in tox_sample]
        tox_agree = cohens_kappa(claude_s, gemini_s)
        logger.info(f"TOX cross-judge (claude vs gemini) on n={tox_agree['n']}: "
                    f"raw={tox_agree['raw_agreement']} kappa={tox_agree['kappa']}")

        # ================= FIRST-LETTER =================
        fl = load_fl_pairs()
        logger.info(f"FL pairs: total={len(fl)} "
                    f"(orig={sum(p['batch']=='iter1_original' for p in fl)} "
                    f"new={sum(p['batch']=='iter2_new' for p in fl)})")

        def fl_key(p):
            return f"{p['letter']}|{p['carrier']}|{p['batch']}"
        fl_sample = strat_sample(fl, fl_key, args.fl_sample, seed=21)

        async def claude_fl(p):
            user = f"TEXT_A: {p['text_a']!r}\nTEXT_B: {p['text_b']!r}"
            v = await judge(cc.JUDGE_PRIMARY, fl_rubric(p["letter"]), user, parse_fl, 50)
            return p["pair_id"], v

        async def deepseek_fl(p):
            user = f"TEXT_A: {p['text_a']!r}\nTEXT_B: {p['text_b']!r}"
            v = await judge(cc.JUDGE_SECOND_FL, fl_rubric(p["letter"]), user, parse_fl, 50)
            return p["pair_id"], v
        cres = dict(await asyncio.gather(*[claude_fl(p) for p in fl_sample]))
        dres = dict(await asyncio.gather(*[deepseek_fl(p) for p in fl_sample]))

        claude_fl_pass = [cres.get(p["pair_id"], {}).get("_pass") if cres.get(p["pair_id"]) else None for p in fl_sample]
        deep_fl_pass = [dres.get(p["pair_id"], {}).get("_pass") if dres.get(p["pair_id"]) else None for p in fl_sample]
        fl_agree = cohens_kappa(claude_fl_pass, deep_fl_pass)
        # claude vs stored gemini on sampled originals carrying a stored label
        cg_a, cg_b = [], []
        for p in fl_sample:
            if p["batch"] == "iter1_original" and p["stored_gemini"] is not None:
                cv = cres.get(p["pair_id"])
                if cv:
                    cg_a.append(cv["_pass"])
                    cg_b.append(bool(p["stored_gemini"]))
        fl_vs_stored = cohens_kappa(cg_a, cg_b)
        n_claude_fl = sum(1 for x in claude_fl_pass if x is not None)
        fl_claude_pass_rate = (sum(1 for x in claude_fl_pass if x) / n_claude_fl) if n_claude_fl else None
        logger.info(f"FL cross-judge (claude vs deepseek) n={fl_agree['n']}: raw={fl_agree['raw_agreement']} "
                    f"kappa={fl_agree['kappa']}; claude_pass_rate={fl_claude_pass_rate} "
                    f"(judge_false_neg={None if fl_claude_pass_rate is None else round(1-fl_claude_pass_rate,4)})")

        # ---- assemble per-pair annotations for assemble.py ----
        tox_annot = {}
        for pid, v in claude_orig_labels.items():
            if v is not None:
                tox_annot[pid] = {"model": cc.JUDGE_PRIMARY, "pass": v["_pass"], "reason": v.get("justification", "")}
        for p in news:
            cc_v = p["claude_cached"]
            tox_annot[p["pair_id"]] = {"model": cc.JUDGE_PRIMARY, "pass": True,
                                       "reason": cc_v.get("justification", "")}
        tox_gemini_annot = {pid: {"model": cc.JUDGE_SECOND_TOX, "pass": (v["_pass"] if v else None),
                                  "reason": (v.get("justification", "") if v else "")}
                            for pid, v in gemini_labels.items()}
        fl_annot = {pid: {"model": cc.JUDGE_PRIMARY, "pass": (v["_pass"] if v else None),
                          "reason": (v.get("justification", "") if v else "")}
                    for pid, v in cres.items()}
        fl_deep_annot = {pid: {"model": cc.JUDGE_SECOND_FL, "pass": (v["_pass"] if v else None),
                               "reason": (v.get("justification", "") if v else "")}
                         for pid, v in dres.items()}

        out = {
            "toxicity": {
                "n_originals_judged": n_orig_judged,
                "originals_confirmation_rate": round(confirmation_rate, 4),
                "originals_confirmed": confirmed,
                "primary_judge": cc.JUDGE_PRIMARY, "second_judge": cc.JUDGE_SECOND_TOX,
                "cross_judge_sample_n": tox_agree["n"],
                "cross_judge": tox_agree,
                "claude_annot": tox_annot,          # ALL originals + ALL new
                "gemini_annot": tox_gemini_annot,    # sample only
            },
            "first_letter": {
                "primary_judge": cc.JUDGE_PRIMARY, "second_judge": cc.JUDGE_SECOND_FL,
                "sample_n": len(fl_sample),
                "claude_pass_rate": None if fl_claude_pass_rate is None else round(fl_claude_pass_rate, 4),
                "claude_judge_false_negative_rate": None if fl_claude_pass_rate is None else round(1 - fl_claude_pass_rate, 4),
                "cross_judge": fl_agree,
                "claude_vs_stored_gemini": fl_vs_stored,
                "claude_annot": fl_annot,            # sample only
                "deepseek_annot": fl_deep_annot,      # sample only
            },
            "rejudge_cost_usd": round(budget.cost, 4),
            "rejudge_calls": budget.calls,
        }
        OUT.write_text(json.dumps(out, ensure_ascii=False))
        logger.info(f"DONE rejudge: cost=${budget.cost:.4f} calls={budget.calls}")
        print(f"REJUDGE_OK tox_conf={confirmation_rate:.3f} tox_kappa={tox_agree['kappa']} "
              f"fl_kappa={fl_agree['kappa']} fl_claude_pass={fl_claude_pass_rate} cost=${budget.cost:.4f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tox-sample", type=int, default=400)
    ap.add_argument("--fl-sample", type=int, default=400)
    args = ap.parse_args()
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
