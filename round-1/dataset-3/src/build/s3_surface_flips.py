"""STEP 3 — Surface-flip pairs (toxic -> toxic paraphrase) via OpenRouter.

No human toxic->toxic paraphrase corpus exists, so generate. Each accepted
pair (x, x') is two toxic sentences with the SAME content but substantially
different surface wording, used downstream for the unit-level surface-
invariance control (a valid unit's pooled surface-response must not exceed
the shuffled-surface null).

3-step ParaDetox/ParaDeHate-style protocol:
  (1) generate a reworded variant (low-refusal instruction model, defensive
      research framing);
  (2) PROGRAMMATIC surface-change gate (token Jaccard < 0.6 AND normalized
      char edit distance above a floor) -- guarantees a genuine surface flip;
  (3) LLM-JUDGE gate returning {toxicity_preserved, meaning_preserved}.
Accept iff (2) AND both flags in (3).

All LLM calls go through OpenRouter only. Generations and judgements are
cached to JSONL so re-runs never re-pay. A hard cumulative-cost ceiling stops
the run well under the global $10 budget.

Output: temp/intermediate/surface_pairs.json + temp/intermediate/s3_stats.json
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import random
import re

import httpx

from common import (SUB_ATTRS, clean_text, get_logger, norm_key, sha16,
                    source_sentence_id)

LOG = get_logger("s3_surface")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INTER = os.path.join(ROOT, "temp", "intermediate")
CONTENT_JSON = os.path.join(INTER, "content_pairs.json")
CLS_JSON = os.path.join(INTER, "classification.json")
GEN_CACHE = os.path.join(INTER, "gen_cache.jsonl")
JUDGE_CACHE = os.path.join(INTER, "judge_cache.jsonl")
OUT = os.path.join(INTER, "surface_pairs.json")
STATS = os.path.join(INTER, "s3_stats.json")
COST_LOG = os.path.join(ROOT, "logs", "openrouter_cost.json")

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
HARD_CEILING = 5.0          # USD for THIS component (global budget is $10)
CONCURRENCY = 12

JACCARD_MAX = 0.6           # surface gate: token overlap must be below this
CHAR_CHANGE_MIN = 0.25      # surface gate: normalized edit distance floor

REFUSAL_RE = re.compile(
    r"\b(i can('?|no)t|i cannot|i'm sorry|i am sorry|i won'?t|i will not|"
    r"as an ai|i apologi|unable to (help|assist|comply)|i must decline|"
    r"cannot (assist|help|comply|fulfil|fulfill)|against my)\b", re.I)

GEN_SYS = (
    "You are a linguistic paraphrasing tool used to build a DEFENSIVE "
    "toxicity-detection research dataset. The paired data trains safety "
    "classifiers. Given a sentence, reword it so the wording and syntax "
    "change substantially, but the meaning AND the toxic tone/intent are "
    "preserved exactly. Do NOT soften, censor, detoxify, sanitise, or add "
    "warnings or commentary. Keep it roughly the same length. Output ONLY "
    "the reworded sentence on a single line, nothing else.")

JUDGE_SYS = (
    "You are a careful annotator for a toxicity-detection dataset. You are "
    "given an ORIGINAL sentence and a PARAPHRASE. Decide two booleans: "
    "toxicity_preserved = the paraphrase is about as toxic/offensive as the "
    "original (not softened, not made more toxic); meaning_preserved = the "
    "core meaning is the same. Respond with ONLY compact JSON: "
    '{"toxicity_preserved": <true|false>, "meaning_preserved": <true|false>}')


# --------------------------------------------------------------------------- #
# Surface-change metrics
# --------------------------------------------------------------------------- #

def _tok(s: str):
    return [t for t in re.split(r"\W+", s.lower()) if t]


def token_jaccard(a: str, b: str) -> float:
    sa, sb = set(_tok(a)), set(_tok(b))
    if not sa and not sb:
        return 1.0
    return len(sa & sb) / max(1, len(sa | sb))


def norm_edit_distance(a: str, b: str) -> float:
    """Levenshtein distance normalized by the longer string (0..1)."""
    a, b = a.lower(), b.lower()
    if not a and not b:
        return 0.0
    la, lb = len(a), len(b)
    if la == 0 or lb == 0:
        return 1.0
    prev = list(range(lb + 1))
    for i in range(1, la + 1):
        cur = [i] + [0] * lb
        ca = a[i - 1]
        for j in range(1, lb + 1):
            cost = 0 if ca == b[j - 1] else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
        prev = cur
    return prev[lb] / max(la, lb)


def surface_gate(src: str, para: str):
    if not para or norm_key(para) == norm_key(src):
        return False, {"jaccard": 1.0, "char_change": 0.0, "reason": "empty_or_identical"}
    jac = token_jaccard(src, para)
    ced = norm_edit_distance(src, para)
    ok = (jac < JACCARD_MAX) and (ced > CHAR_CHANGE_MIN)
    return ok, {"jaccard": round(jac, 3), "char_change": round(ced, 3), "reason": "ok" if ok else "too_similar"}


# --------------------------------------------------------------------------- #
# JSONL cache helpers
# --------------------------------------------------------------------------- #

def load_cache(path):
    cache = {}
    if os.path.exists(path):
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
        f.write(json.dumps(rec) + "\n")


# --------------------------------------------------------------------------- #
# OpenRouter async call
# --------------------------------------------------------------------------- #

class Budget:
    def __init__(self):
        self.cost = 0.0
        self.calls = 0
        self.in_tok = 0
        self.out_tok = 0


async def call_or(client, model, system, user, budget, max_tokens=220, temperature=0.8):
    body = {
        "model": model,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "usage": {"include": True},
    }
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
            cost = usage.get("cost")
            budget.calls += 1
            budget.in_tok += int(usage.get("prompt_tokens", 0) or 0)
            budget.out_tok += int(usage.get("completion_tokens", 0) or 0)
            if cost is None:
                cost = 0.0
            budget.cost += float(cost)
            return txt, float(cost)
        except Exception as e:  # noqa
            last_err = repr(e)[:120]
            await asyncio.sleep(1.0 * (attempt + 1))
    return f"__ERROR__:{last_err}", 0.0


# --------------------------------------------------------------------------- #
# Source selection
# --------------------------------------------------------------------------- #

def pick_sources(n_paradetox, n_civil, seed=42):
    rng = random.Random(seed)
    sources = []  # dict: text, source, ssid, subcontext_floats(optional), sub_present

    # ParaDetox unique toxic sentences
    with open(CONTENT_JSON) as f:
        cps = json.load(f)
    seen_ssid = {}
    for cp in cps:
        ssid = cp["source_sentence_id"]
        if ssid not in seen_ssid:
            seen_ssid[ssid] = cp["text_on"]
    pd_items = list(seen_ssid.items())
    rng.shuffle(pd_items)
    for ssid, txt in pd_items[:n_paradetox]:
        sources.append({"text": txt, "source": "paradetox", "ssid": ssid,
                        "floats": None, "sub_present": []})

    # civil_comments toxic positives, stratified across sub-attributes (rare first)
    civil_by_sub = {a: [] for a in SUB_ATTRS}
    civil_generic = []
    if os.path.exists(CLS_JSON):
        with open(CLS_JSON) as f:
            cls = json.load(f)
        for r in cls:
            if r.get("toxicity_label") != 1:
                continue
            present = [a for a in SUB_ATTRS if (r["floats"].get(a, 0.0) >= 0.5)]
            if present:
                # add to the rarest-attr bucket it satisfies (stratify toward rare)
                for a in present:
                    civil_by_sub[a].append((r["text"], r["floats"], present))
            else:
                civil_generic.append((r["text"], r["floats"], []))
    # round-robin across sub-attrs to balance coverage of rare contexts
    per_attr = max(1, n_civil // (len(SUB_ATTRS) + 1))
    picked_keys = set()
    for a in SUB_ATTRS:
        pool = civil_by_sub[a]
        rng.shuffle(pool)
        cnt = 0
        for txt, fl, present in pool:
            k = norm_key(txt)
            if k in picked_keys:
                continue
            picked_keys.add(k)
            sources.append({"text": txt, "source": "civil_comments",
                            "ssid": source_sentence_id(txt), "floats": fl,
                            "sub_present": present})
            cnt += 1
            if cnt >= per_attr:
                break
    # top up with generic toxic
    rng.shuffle(civil_generic)
    for txt, fl, present in civil_generic:
        if len([s for s in sources if s["source"] == "civil_comments"]) >= n_civil:
            break
        k = norm_key(txt)
        if k in picked_keys:
            continue
        picked_keys.add(k)
        sources.append({"text": txt, "source": "civil_comments",
                        "ssid": source_sentence_id(txt), "floats": fl, "sub_present": present})

    rng.shuffle(sources)
    return sources


# --------------------------------------------------------------------------- #
# Main async pipeline
# --------------------------------------------------------------------------- #

async def run(gen_model, judge_model, n_paradetox, n_civil, seed):
    if not API_KEY:
        raise SystemExit("OPENROUTER_API_KEY not set")
    sources = pick_sources(n_paradetox, n_civil, seed)
    LOG.info("Selected %d source sentences (paradetox=%d civil=%d) for gen_model=%s",
             len(sources), sum(s["source"] == "paradetox" for s in sources),
             sum(s["source"] == "civil_comments" for s in sources), gen_model)

    gen_cache = load_cache(GEN_CACHE)
    judge_cache = load_cache(JUDGE_CACHE)
    budget = Budget()
    sem = asyncio.Semaphore(CONCURRENCY)
    stop = {"hit": False}

    async with httpx.AsyncClient() as client:
        # ---- Phase A: generate ----
        async def gen_one(src):
            key = "gen:" + gen_model + ":" + sha16(norm_key(src["text"]))
            if key in gen_cache:
                return src, gen_cache[key]["text"]
            if stop["hit"]:
                return src, None
            async with sem:
                if stop["hit"]:
                    return src, None
                txt, _ = await call_or(client, gen_model, GEN_SYS, src["text"], budget)
            rec = {"key": key, "text": txt, "model": gen_model}
            gen_cache[key] = rec
            append_cache(GEN_CACHE, rec)
            if budget.cost >= HARD_CEILING:
                stop["hit"] = True
                LOG.warning("HARD CEILING $%.2f reached during generation; stopping new calls", HARD_CEILING)
            return src, txt

        gen_results = []
        batch = 64
        for i in range(0, len(sources), batch):
            chunk = sources[i:i + batch]
            res = await asyncio.gather(*[gen_one(s) for s in chunk])
            gen_results.extend(res)
            LOG.info("GEN batch %d-%d | cumulative cost $%.4f calls=%d (in=%d out=%d)",
                     i, i + len(chunk), budget.cost, budget.calls, budget.in_tok, budget.out_tok)
            _write_cost(budget, "generation")
            if stop["hit"]:
                LOG.warning("Stopping generation early (ceiling).")
                break

        # ---- Phase A.5: programmatic surface gate + refusal detection ----
        refusals = 0
        errors = 0
        gate_pass = []
        for src, para in gen_results:
            if para is None:
                continue
            if para.startswith("__ERROR__"):
                errors += 1
                continue
            if REFUSAL_RE.search(para) or len(para) < 3:
                refusals += 1
                continue
            para = clean_text(para)
            ok, m = surface_gate(src["text"], para)
            if ok:
                gate_pass.append((src, para, m))
        LOG.info("Generated=%d | refusals=%d errors=%d | surface-gate pass=%d",
                 len(gen_results), refusals, errors, len(gate_pass))

        # ---- Phase B: LLM judge on gate-passing pairs ----
        async def judge_one(item):
            src, para, m = item
            key = "judge:" + judge_model + ":" + sha16(norm_key(src["text"]) + "||" + norm_key(para))
            if key in judge_cache:
                return item, judge_cache[key]["verdict"]
            if stop["hit"]:
                return item, None
            user = f"ORIGINAL: {src['text']}\nPARAPHRASE: {para}"
            async with sem:
                if stop["hit"]:
                    return item, None
                txt, _ = await call_or(client, judge_model, JUDGE_SYS, user, budget, max_tokens=40, temperature=0.0)
            verdict = _parse_judge(txt)
            rec = {"key": key, "verdict": verdict, "raw": txt, "model": judge_model}
            judge_cache[key] = rec
            append_cache(JUDGE_CACHE, rec)
            if budget.cost >= HARD_CEILING:
                stop["hit"] = True
            return item, verdict

        judged = []
        for i in range(0, len(gate_pass), batch):
            chunk = gate_pass[i:i + batch]
            res = await asyncio.gather(*[judge_one(it) for it in chunk])
            judged.extend(res)
            LOG.info("JUDGE batch %d-%d | cumulative cost $%.4f calls=%d", i, i + len(chunk), budget.cost, budget.calls)
            _write_cost(budget, "judge")
            if stop["hit"]:
                LOG.warning("Stopping judging early (ceiling).")
                break

    # ---- assemble accepted pairs ----
    accepted = []
    n_judged = 0
    n_tox_fail = n_mean_fail = 0
    for item, verdict in judged:
        if verdict is None:
            continue
        n_judged += 1
        src, para, m = item
        tp = bool(verdict.get("toxicity_preserved"))
        mp = bool(verdict.get("meaning_preserved"))
        if not tp:
            n_tox_fail += 1
        if not mp:
            n_mean_fail += 1
        passed = tp and mp
        floats = src["floats"]
        sub_labels = None
        if floats is not None:
            sub_labels = {a: (1 if floats.get(a, 0.0) >= 0.5 else 0) for a in SUB_ATTRS}
        rec = {
            "record_type": "surface_pair",
            "source": "generated_paraphrase",
            "text": src["text"],          # original toxic (x)
            "text_paired": para,          # reworded toxic (x')
            "pair_id": "sp_" + sha16(norm_key(src["text"]) + "||" + norm_key(para)),
            "source_sentence_id": src["ssid"],
            "origin_source": src["source"],
            "gen_model": gen_model,
            "judge_pass": passed,
            "surface_metrics": m,
            "subcontext_labels": sub_labels,
            "subcontext_floats": floats,
        }
        if passed:
            accepted.append(rec)

    judge_pass_rate = (len(accepted) / n_judged) if n_judged else 0.0
    refusal_rate = (refusals / max(1, len([g for g in gen_results if g[1] is not None])))
    stats = {
        "gen_model": gen_model,
        "judge_model": judge_model,
        "n_sources": len(sources),
        "n_generated": len(gen_results),
        "n_refusals": refusals,
        "n_gen_errors": errors,
        "refusal_rate": round(refusal_rate, 4),
        "n_surface_gate_pass": len(gate_pass),
        "n_judged": n_judged,
        "n_toxicity_fail": n_tox_fail,
        "n_meaning_fail": n_mean_fail,
        "n_accepted": len(accepted),
        "judge_pass_rate": round(judge_pass_rate, 4),
        "openrouter_cost_usd": round(budget.cost, 4),
        "openrouter_calls": budget.calls,
        "ceiling_hit": stop["hit"],
        "jaccard_max": JACCARD_MAX,
        "char_change_min": CHAR_CHANGE_MIN,
    }
    with open(OUT, "w") as f:
        json.dump(accepted, f)
    with open(STATS, "w") as f:
        json.dump(stats, f, indent=2)
    _write_cost(budget, "final")
    LOG.info("ACCEPTED %d surface pairs | judge_pass_rate=%.3f refusal_rate=%.3f cost=$%.4f",
             len(accepted), judge_pass_rate, refusal_rate, budget.cost)
    LOG.info("Stats: %s", json.dumps(stats))
    return stats


def _parse_judge(txt):
    if not txt or txt.startswith("__ERROR__"):
        return {"toxicity_preserved": False, "meaning_preserved": False, "_err": True}
    m = re.search(r"\{.*\}", txt, re.S)
    raw = m.group(0) if m else txt
    try:
        d = json.loads(raw)
        return {"toxicity_preserved": bool(d.get("toxicity_preserved")),
                "meaning_preserved": bool(d.get("meaning_preserved"))}
    except Exception:
        tp = bool(re.search(r"toxicity_preserved\"?\s*:\s*true", txt, re.I))
        mp = bool(re.search(r"meaning_preserved\"?\s*:\s*true", txt, re.I))
        return {"toxicity_preserved": tp, "meaning_preserved": mp}


def _write_cost(budget, phase):
    os.makedirs(os.path.dirname(COST_LOG), exist_ok=True)
    with open(COST_LOG, "w") as f:
        json.dump({"phase": phase, "cost_usd": round(budget.cost, 5),
                   "calls": budget.calls, "in_tok": budget.in_tok,
                   "out_tok": budget.out_tok, "ceiling": HARD_CEILING}, f, indent=2)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--gen-model", default="openai/gpt-4o-mini")
    ap.add_argument("--judge-model", default="openai/gpt-4o-mini")
    ap.add_argument("--n-paradetox", type=int, default=400)
    ap.add_argument("--n-civil", type=int, default=300)
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()
    asyncio.run(run(a.gen_model, a.judge_model, a.n_paradetox, a.n_civil, a.seed))
