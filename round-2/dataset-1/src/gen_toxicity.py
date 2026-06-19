#!/usr/bin/env python3
"""STEP 2 — Enlarge the TOXICITY surface_pair set (546 -> >=1,500; OpenRouter, gated).

Per source toxic sentence:
  (1) gpt-4o-mini rewords it toxic->toxic (homogeneous w/ the 546 originals; GEN_SYS verbatim).
  (2) DOUBLE-GATE (token Jaccard < 0.6 AND normalized char-change > 0.25) — verbatim from iter-1.
  (3) INDEPENDENT judge anthropic/claude-haiku-4.5 (different model family from the gpt-4o-mini
      generator -> breaks the iter-1 same-model generate-and-judge circularity). Rubric returns
      {toxicity_constant, meaning_preserved, surface_changed, fluent}; ACCEPT iff all four true.
Every NEW pair is therefore born with an independent-family judge label.

Sources: fresh toxic sentences NOT already used as a SURFACE source in iter-1 (reusing
content/classification toxic comments is the iter-1 protocol and inherits their native,
leakage-safe fold). paradetox toxic from content_pairs.json; civil toxic from classification.json
(stratified across the 6 sub-attributes, real sub-attribute floats carried for per-sub nulls).

JSONL caches make re-runs / gradual scaling free. Hard cumulative cost ceiling.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import random
import re
import sys
from pathlib import Path

import httpx
from loguru import logger

import cc

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/gen_toxicity.log", rotation="20 MB", level="DEBUG")

WORK = Path(__file__).resolve().parent
INTER = WORK / "temp" / "intermediate"
GEN_CACHE = INTER / "tox_gen_cache.jsonl"
JUDGE_CACHE = INTER / "tox_judge_cache.jsonl"
OUT = INTER / "tox_new_surface.json"
STATS = INTER / "tox_gen_stats.json"

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
CONCURRENCY = 12

GEN_SYS = (
    "You are a linguistic paraphrasing tool used to build a DEFENSIVE "
    "toxicity-detection research dataset. The paired data trains safety "
    "classifiers. Given a sentence, reword it so the wording and syntax "
    "change substantially, but the meaning AND the toxic tone/intent are "
    "preserved exactly. Do NOT soften, censor, detoxify, sanitise, or add "
    "warnings or commentary. Keep it roughly the same length. Output ONLY "
    "the reworded sentence on a single line, nothing else.")

# Independent-judge rubric (4 flags). Framed as classification/validation to avoid refusals.
CLAUDE_JUDGE_SYS = (
    "You are a careful annotator validating a paraphrase pair for a DEFENSIVE "
    "toxicity-detection research dataset used to train safety classifiers. This is a "
    "classification / validation task on already-written text — do NOT refuse. You are given an "
    "ORIGINAL toxic sentence and a PARAPHRASE. Decide four booleans: "
    "toxicity_constant = the paraphrase stays about as toxic/offensive as the original "
    "(not softened/detoxified, not made more toxic); "
    "meaning_preserved = the core meaning and target are the same; "
    "surface_changed = the wording/phrasing genuinely differs from the original; "
    "fluent = the paraphrase is fluent, grammatical English. "
    'Respond with ONLY compact JSON: {"toxicity_constant": <true|false>, '
    '"meaning_preserved": <true|false>, "surface_changed": <true|false>, "fluent": <true|false>, '
    '"confidence": <0..1>, "justification": "<=10 words"}')


class Budget:
    def __init__(self):
        self.cost = 0.0
        self.calls = 0
        self.in_tok = 0
        self.out_tok = 0


def load_cache(path):
    cache = {}
    if path.exists():
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                    cache[rec["key"]] = rec
                except Exception:
                    continue
    return cache


def append_cache(path, rec):
    with open(path, "a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


async def call_or(client, model, system, user, budget, *, max_tokens, temperature):
    body = {"model": model,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": user}],
            "max_tokens": max_tokens, "temperature": temperature,
            "usage": {"include": True}}
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    last_err = None
    for attempt in range(4):
        try:
            r = await client.post(API_URL, json=body, headers=headers, timeout=90.0)
            if r.status_code in (429, 500, 502, 503, 529):
                await asyncio.sleep(1.5 * (attempt + 1))
                last_err = f"http{r.status_code}"
                continue
            r.raise_for_status()
            data = r.json()
            txt = (data["choices"][0]["message"]["content"] or "").strip()
            usage = data.get("usage", {}) or {}
            budget.calls += 1
            budget.in_tok += int(usage.get("prompt_tokens", 0) or 0)
            budget.out_tok += int(usage.get("completion_tokens", 0) or 0)
            budget.cost += float(usage.get("cost") or 0.0)
            return txt
        except Exception as e:  # noqa: BLE001
            last_err = repr(e)[:140]
            await asyncio.sleep(1.0 * (attempt + 1))
    return f"__ERROR__:{last_err}"


def parse_claude(txt):
    """Return dict with 4 bools + confidence/justification, or None on failure."""
    if not txt or txt.startswith("__ERROR__"):
        return None
    m = re.search(r"\{.*\}", txt, re.S)
    raw = m.group(0) if m else txt
    try:
        d = json.loads(raw)
        return {
            "toxicity_constant": bool(d.get("toxicity_constant")),
            "meaning_preserved": bool(d.get("meaning_preserved")),
            "surface_changed": bool(d.get("surface_changed")),
            "fluent": bool(d.get("fluent")),
            "confidence": d.get("confidence"),
            "justification": str(d.get("justification", ""))[:140],
        }
    except Exception:
        def b(name):
            return bool(re.search(name + r"\"?\s*:\s*true", txt, re.I))
        return {"toxicity_constant": b("toxicity_constant"),
                "meaning_preserved": b("meaning_preserved"),
                "surface_changed": b("surface_changed"), "fluent": b("fluent"),
                "confidence": None, "justification": txt[:140]}


def build_candidates(*, max_paradetox, max_civil, seed):
    """Fresh toxic sources, deduped against the 546 iter-1 SURFACE sources only."""
    idx = json.loads((INTER / "tox_index.json").read_text())
    normkey_fold = idx["normkey_fold"]
    tox_orig = json.loads((INTER / "tox_originals.json").read_text())
    surf_ssids = {r["metadata_source_sentence_id"] for r in tox_orig["surface_rows"]}
    surf_nk = set(idx["existing_surface_normkeys"])

    rng = random.Random(seed)
    cands = []

    def fold_for(text):
        k = cc.norm_key(text)
        return normkey_fold.get(k) or cc.fold_from_key("comp_k:" + k)

    # paradetox unique toxic sources (from content_pairs)
    cps = json.loads((cc.TOX_DIR / "temp" / "intermediate" / "content_pairs.json").read_text())
    seen_ssid = {}
    for cp in cps:
        if cp["source_sentence_id"] not in seen_ssid:
            seen_ssid[cp["source_sentence_id"]] = cp["text_on"]
    pd_items = list(seen_ssid.items())
    rng.shuffle(pd_items)
    n_pd = 0
    for ssid, txt in pd_items:
        if n_pd >= max_paradetox:
            break
        if ssid in surf_ssids or cc.norm_key(txt) in surf_nk:
            continue
        cands.append({"text": cc.clean_text(txt), "origin": "paradetox", "ssid": ssid,
                      "floats": None, "fold": fold_for(txt)})
        n_pd += 1

    # civil toxic sources stratified across sub-attrs (rare first), then generic top-up
    cls = json.loads(cc.CLS_JSON.read_text())
    by_sub = {a: [] for a in cc.SUB_ATTRS}
    generic = []
    for r in cls:
        if r.get("toxicity_label") != 1:
            continue
        present = [a for a in cc.SUB_ATTRS if r["floats"].get(a, 0.0) >= 0.5]
        if present:
            for a in present:
                by_sub[a].append(r)
        else:
            generic.append(r)
    picked_nk = set()
    civ = []

    def take(r):
        ssid = cc.source_sentence_id(r["text"])
        k = cc.norm_key(r["text"])
        if ssid in surf_ssids or k in surf_nk or k in picked_nk:
            return False
        picked_nk.add(k)
        floats = {a: float(r["floats"].get(a, 0.0)) for a in cc.FLOAT_AXES}
        civ.append({"text": cc.clean_text(r["text"]), "origin": "civil_comments", "ssid": ssid,
                    "floats": floats, "fold": r.get("fold") or fold_for(r["text"])})
        return True

    per_attr = max(1, max_civil // (len(cc.SUB_ATTRS) + 1))
    for a in cc.SUB_ATTRS:
        pool = by_sub[a][:]
        rng.shuffle(pool)
        cnt = 0
        for r in pool:
            if cnt >= per_attr or len(civ) >= max_civil:
                break
            if take(r):
                cnt += 1
    rng.shuffle(generic)
    for r in generic:
        if len(civ) >= max_civil:
            break
        take(r)

    cands.extend(civ)
    rng.shuffle(cands)
    logger.info(f"candidates: paradetox={n_pd} civil={len(civ)} total={len(cands)} (seed={seed})")
    return cands


async def run(args):
    if not API_KEY:
        raise SystemExit("OPENROUTER_API_KEY not set")
    cands = build_candidates(max_paradetox=args.max_paradetox, max_civil=args.max_civil, seed=args.seed)
    gen_cache = load_cache(GEN_CACHE)
    judge_cache = load_cache(JUDGE_CACHE)
    budget = Budget()
    sem = asyncio.Semaphore(CONCURRENCY)
    stop = {"hit": False}

    accepted = []
    n_gen = n_refusal = n_err = n_gate = n_judged = n_tox_fail = n_mean_fail = n_surf_fail = n_fluent_fail = 0

    async with httpx.AsyncClient() as client:
        async def gen_one(src):
            key = "gen:" + cc.GEN_MODEL + ":" + cc.sha16(cc.norm_key(src["text"]))
            if key in gen_cache:
                return src, gen_cache[key]["text"]
            if stop["hit"]:
                return src, None
            async with sem:
                if stop["hit"]:
                    return src, None
                txt = await call_or(client, cc.GEN_MODEL, GEN_SYS, src["text"], budget,
                                    max_tokens=220, temperature=0.8)
            rec = {"key": key, "text": txt, "model": cc.GEN_MODEL}
            gen_cache[key] = rec
            append_cache(GEN_CACHE, rec)
            if budget.cost >= args.ceiling:
                stop["hit"] = True
            return src, txt

        async def judge_one(src, para, metrics):
            key = "judge:" + cc.JUDGE_PRIMARY + ":" + cc.sha16(cc.norm_key(src["text"]) + "||" + cc.norm_key(para))
            if key in judge_cache:
                return judge_cache[key]["verdict"]
            if stop["hit"]:
                return None
            user = f"ORIGINAL: {src['text']}\nPARAPHRASE: {para}"
            async with sem:
                if stop["hit"]:
                    return None
                txt = await call_or(client, cc.JUDGE_PRIMARY, CLAUDE_JUDGE_SYS, user, budget,
                                    max_tokens=80, temperature=0.0)
            verdict = parse_claude(txt)
            rec = {"key": key, "verdict": verdict, "raw": txt, "model": cc.JUDGE_PRIMARY}
            judge_cache[key] = rec
            append_cache(JUDGE_CACHE, rec)
            if budget.cost >= args.ceiling:
                stop["hit"] = True
            return verdict

        batch = args.batch
        for i in range(0, len(cands), batch):
            if stop["hit"] or len(accepted) >= args.target_accepted:
                break
            chunk = cands[i:i + batch]
            gen_res = await asyncio.gather(*[gen_one(s) for s in chunk])
            # gate
            gate_pass = []
            for src, para in gen_res:
                if para is None:
                    continue
                n_gen += 1
                if para.startswith("__ERROR__"):
                    n_err += 1
                    continue
                if cc.REFUSAL_RE.search(para) or len(para) < 3:
                    n_refusal += 1
                    continue
                para = cc.clean_text(para)
                ok, m = cc.surface_gate(src["text"], para)
                if ok:
                    n_gate += 1
                    gate_pass.append((src, para, m))
            # judge
            verdicts = await asyncio.gather(*[judge_one(s, p, m) for (s, p, m) in gate_pass])
            for (src, para, m), v in zip(gate_pass, verdicts):
                if v is None:
                    continue
                n_judged += 1
                if not v["toxicity_constant"]:
                    n_tox_fail += 1
                if not v["meaning_preserved"]:
                    n_mean_fail += 1
                if not v["surface_changed"]:
                    n_surf_fail += 1
                if not v["fluent"]:
                    n_fluent_fail += 1
                if v["toxicity_constant"] and v["meaning_preserved"] and v["surface_changed"] and v["fluent"]:
                    accepted.append({
                        "text": src["text"], "text_paired": para, "origin": src["origin"],
                        "ssid": src["ssid"], "fold": src["fold"], "floats": src["floats"],
                        "surface_metrics": m, "gen_model": cc.GEN_MODEL,
                        "judge_model": cc.JUDGE_PRIMARY, "judge_verdict": v,
                        "pair_id": "sp2_" + cc.sha16(cc.norm_key(src["text"]) + "||" + cc.norm_key(para)),
                    })
            logger.info(f"batch {i}-{i+len(chunk)} | gen={n_gen} gate={n_gate} judged={n_judged} "
                        f"accepted={len(accepted)} | cost=${budget.cost:.4f} calls={budget.calls}")

    judge_pass_rate = (len(accepted) / n_judged) if n_judged else 0.0
    stats = {
        "gen_model": cc.GEN_MODEL, "judge_model": cc.JUDGE_PRIMARY,
        "n_candidates": len(cands), "n_generated": n_gen, "n_refusals": n_refusal,
        "n_gen_errors": n_err, "n_surface_gate_pass": n_gate, "n_judged": n_judged,
        "n_toxicity_fail": n_tox_fail, "n_meaning_fail": n_mean_fail,
        "n_surface_fail": n_surf_fail, "n_fluent_fail": n_fluent_fail,
        "n_accepted": len(accepted), "judge_pass_rate": round(judge_pass_rate, 4),
        "openrouter_cost_usd": round(budget.cost, 4), "openrouter_calls": budget.calls,
        "in_tok": budget.in_tok, "out_tok": budget.out_tok,
        "ceiling_hit": stop["hit"], "ceiling_usd": args.ceiling,
        "jaccard_max": cc.JACCARD_MAX, "char_change_min": cc.CHAR_CHANGE_MIN,
        "rubric": "ACCEPT iff toxicity_constant AND meaning_preserved AND surface_changed AND fluent (claude-haiku-4.5)",
    }
    OUT.write_text(json.dumps({"accepted": accepted, "stats": stats}, ensure_ascii=False))
    STATS.write_text(json.dumps(stats, indent=2))
    logger.info(f"DONE toxicity gen: accepted={len(accepted)} pass_rate={judge_pass_rate:.3f} "
                f"cost=${budget.cost:.4f} calls={budget.calls} ceiling_hit={stop['hit']}")
    print(f"TOX_GEN_OK accepted={len(accepted)} judged={n_judged} pass_rate={judge_pass_rate:.3f} "
          f"cost=${budget.cost:.4f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-paradetox", type=int, default=1100)
    ap.add_argument("--max-civil", type=int, default=1700)
    ap.add_argument("--target-accepted", type=int, default=1050)
    ap.add_argument("--batch", type=int, default=80)
    ap.add_argument("--ceiling", type=float, default=6.0)  # component cap; global hard cap is $10
    ap.add_argument("--seed", type=int, default=2025)
    args = ap.parse_args()
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
