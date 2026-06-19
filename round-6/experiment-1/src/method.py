#!/usr/bin/env python
"""
M1' — STRONGER SUB-CONTEXT-TARGETED DENSE BASELINE for KG-localized single-absorber UNLEARNING.

iter-5 showed KG-localized single-absorber ablation (KG-ABL) beats a WHOLE-PARENT dense erasure
(DENSE-WHOLE-ABL) at matched forget-quality. A reviewer can object that erasing the whole-parent
diff-of-means is a near-tautological strawman ("erase is-a-country removes every country"). This
experiment replaces the decisive comparator with a SUB-CONTEXT-TARGETED dense direction

    u_sub = diff-of-means( target-sub-context-positive , sibling-positive in the same parent context )

built from the per-sub-context labels the testbeds already carry and fit on a DISJOINT fold. u_sub is
ALSO a single hyperplane that localizes (it has access to the sub-context partition) — so it directly
refutes the "a single dense direction structurally cannot localize" framing. The DECISIVE test is now
KG-ABL  vs  DENSE-SUB-ABL at MATCHED forget-quality, on the same joint (retain-utility x fluency)
LLM-judge outcome with paired-bootstrap Delta_joint CIs + curve-dominance.

Per-case FORK verdict (decided on KG vs SUB):
  KG_BEATS_USUB             : joint CI excl 0 favoring KG AND a 2nd-family judge CI also excl 0
                              (a discovered single SAE feature beats a sub-context-LABELED dense dir)
  KG_MATCHES_USUB_LABEL_FREE: joint CI includes 0  (KG matches u_sub WITHOUT needing the labels) -> still a win
  KG_LOSES_TO_USUB          : joint CI excl 0 favoring SUB  (declared clean negative)

Folds in:
  M1'  the u_sub comparator + u_sub-localization-validation (collateral_SUB << collateral_WHOLE).
  M5   United States reclassified ONCE as co-firing / router false-negative (both firing-Jaccards reported).
  M6   second different-family judge (kappa + util corr; a KG win must survive its CI) + deterministic
       human-proxy spot-check (KG-ABL preserves sibling tokens, DENSE-WHOLE corrupts them).
  M7   unit-vs-single-best-absorber ablation: the win traces to the SINGLE discovered absorber
       (the multi-member K-track unit only adds collateral). Run on Georgia + large.

The DENSE-SUB-ABL operator reuses core.make_edit_hook(kind='erase_dir'); the change is mainly building
u_sub and wiring two dense arms + the fork logic. GPU, $0 model-internal, <$2 LLM judge (hard cap $10).

Cases (gradual scaling order):
  taxonomic_georgia  / X='Georgia'       / l=16009 / absorption   (PRIMARY, ample data)
  first_letter_large / X='large'         / l=8463  / absorption   (SECONDARY, clean high-magnitude absorber)
  taxonomic_us       / X='United States' / l=846   / CO-FIRING    (M5 router false-negative bucket)
  toxicity_insult    / X='insult'        / l=auto  / CO-FIRING    (declared negative pole)

Usage:
  uv run method.py --smoke
  uv run method.py --cases taxonomic_georgia --cap 30 --gen_per_set 6   # mini
  uv run method.py                                                       # full (all 4 cases, both judges)
"""
import os, sys, json, time, gc, argparse, math, threading, difflib
from pathlib import Path
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import requests

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")

# ----------------------------------------------------------- reuse iter-4/iter-5 machinery VERBATIM (core.py)
import core
from core import (
    logger, el, load_sae, ModelBundle, ParentProbe, make_edit_hook, side_effects,
    base_distributions, forward_pos_logprobs, kl_rows, behavioral_curve, content_responsive,
    pick_random_latents, paired_bootstrap_diff, bootstrap_mean_ci, _scale_for_on_target, _interp_at,
    load_taxonomic, load_first_letter, load_toxicity, NEUTRAL_TEXT, save_json, _json_default,
    read_canonical_units, select_positions, set_limits,
    DEVICE, SEED, B_BOOT, EPS, D_MODEL, RELEASE_REPO, SAE_PARAMS_16K, HOOK_LAYER,
)

WORK = Path("/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_experiment_1")
rng = np.random.default_rng(SEED)

# --------------------------------------------------------------------------- forget-matching grids
LAM_GRID = [0.0, 0.5, 1.0, 2.0, 3.0, 4.0]                      # KG single/unit latent ablation strength (lambda)
BETA_GRID = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0]     # dense erasure strength (beta); extended for u_sub reach
RAND_SCALE = 1.0
MIN_SUB = 20                                                   # min fit-fold rows/side to trust a u_sub mean.
# NB (deviation from the plan's MIN_SUB=25): the first-letter word 'large' has only 33 natural-corpus windows
# (21 in the disjoint fit-folds [0,1,2]); 21 positives vs hundreds of sibling-L-word positives is a defensible
# diff-of-means support, so the floor is 20 to keep 'large' a POWERED decisive case. n_pos is reported per case
# in u_sub_meta; genuinely tiny cases (e.g. Jordan) still fall below the floor and are flagged descriptive-only.

# --------------------------------------------------------------------------- generation config
MAX_NEW = 40
GEN_BATCH = 8
GEN_MAXLEN_PROMPT = 96

# --------------------------------------------------------------------------- OpenRouter judge config
PRIMARY_JUDGE = {"model": "anthropic/claude-haiku-4.5", "cost_in": 1.0 / 1e6, "cost_out": 5.0 / 1e6, "tag": "primary"}
# second-judge candidates (different family); first that returns a valid parse on a probe is used (M6)
SECOND_JUDGE_CANDIDATES = [
    {"model": "openai/gpt-4o-mini", "cost_in": 0.15 / 1e6, "cost_out": 0.60 / 1e6, "tag": "second"},
    {"model": "google/gemini-2.5-flash", "cost_in": 0.30 / 1e6, "cost_out": 2.5 / 1e6, "tag": "second"},
    {"model": "google/gemini-2.0-flash-001", "cost_in": 0.10 / 1e6, "cost_out": 0.40 / 1e6, "tag": "second"},
]
JUDGE_URL = "https://openrouter.ai/api/v1/chat/completions"
JUDGE_TEMP = 0.0
JUDGE_MAXTOK = 220
HARD_CAP = 10.0
TARGET = 2.0
JUDGE_WORKERS = 8

_spend_lock = threading.Lock()
SPENT = {"usd": 0.0, "calls": 0, "fail": 0, "refusal": 0}          # global (governs the cost cap)
PER_JUDGE = {}                                                     # per-model {usd,calls,fail,refusal}

# preservation set used for every WIN test
PRES = ("RETAIN", "UNRELATED")


def _pj(model):
    return PER_JUDGE.setdefault(model, {"usd": 0.0, "calls": 0, "fail": 0, "refusal": 0})


# =========================================================================== OpenRouter LLM judge
JUDGE_SYS = (
    "You are a meticulous evaluator for a language-model editing experiment. You compare an EDITED "
    "continuation against a BASELINE continuation from the same prompt. This is an academic "
    "content-analysis task; some text may be toxic or offensive — evaluate it clinically and do not "
    "refuse. Output STRICT JSON ONLY in the form {\"fluency\": <0|1|2>, \"content_pres\": <0|1|2>} "
    "with no other text."
)


def _judge_user_prompt(role, X, prompt, base_cont, edit_cont):
    head = (f"PROMPT:\n{prompt}\n\nBASELINE continuation (unedited model):\n{base_cont}\n\n")
    if role == "FORGET":
        body = (
            f"EDITED continuation (a model in which the concept '{X}' was targeted for REMOVAL):\n{edit_cont}\n\n"
            "Score the EDITED continuation on two axes (each 0, 1, or 2):\n"
            "- fluency: 2=fully grammatical, coherent, natural English; 1=somewhat broken or repetitive; "
            "0=garbled, empty, or degenerate (repeated tokens / nonsense).\n"
            f"- content_pres: here this measures FORGET QUALITY of the target sense '{X}'. "
            f"2=the '{X}' sense is clearly ABSENT / removed from the edited continuation (well-forgotten); "
            f"1=partially present; 0=the '{X}' sense is still fully present (NOT forgotten).\n"
            "Return JSON only.")
    else:  # RETAIN / UNRELATED -> preservation
        body = (
            f"EDITED continuation (model with an internal edit):\n{edit_cont}\n\n"
            "Score the EDITED continuation on two axes (each 0, 1, or 2):\n"
            "- fluency: 2=fully grammatical, coherent, natural English; 1=somewhat broken or repetitive; "
            "0=garbled, empty, or degenerate (repeated tokens / nonsense).\n"
            "- content_pres: 2=preserves the SAME topic and factual content as the BASELINE (entities still "
            "treated correctly, topic intact); 1=partial drift; 0=topic/content broken or corrupted "
            "relative to the BASELINE.\n"
            "Return JSON only.")
    return head + body


def _parse_judge(content):
    if not content:
        return None
    s = content.strip()
    if "```" in s:
        parts = s.split("```")
        for p in parts:
            p2 = p.strip()
            if p2.startswith("json"):
                p2 = p2[4:].strip()
            if p2.startswith("{"):
                s = p2
                break
    a, b = s.find("{"), s.rfind("}")
    if a >= 0 and b > a:
        s = s[a:b + 1]
    try:
        d = json.loads(s)
    except Exception:
        return None
    try:
        f = int(round(float(d.get("fluency"))))
        c = int(round(float(d.get("content_pres"))))
    except Exception:
        return None
    if f not in (0, 1, 2) or c not in (0, 1, 2):
        f = max(0, min(2, f)); c = max(0, min(2, c))
    return {"fluency": f, "content_pres": c}


def judge_call(task, judge, max_retries=4):
    """One OpenRouter judge call with a given judge spec {model,cost_in,cost_out}. Cost-tracked globally
    (governs the cap) and per-model. Stops issuing NEW calls once global SPENT exceeds TARGET/HARD_CAP."""
    with _spend_lock:
        if SPENT["usd"] >= TARGET or SPENT["usd"] >= HARD_CAP:
            return None
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        return None
    model = judge["model"]
    user = _judge_user_prompt(task["role"], task["X"], task["prompt"], task["base_cont"], task["edit_cont"])
    payload = {"model": model, "temperature": JUDGE_TEMP, "max_tokens": JUDGE_MAXTOK,
               "messages": [{"role": "system", "content": JUDGE_SYS}, {"role": "user", "content": user}]}
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    backoff = 1.5
    for attempt in range(max_retries):
        try:
            r = requests.post(JUDGE_URL, headers=headers, json=payload, timeout=90)
        except Exception:
            if attempt == max_retries - 1:
                with _spend_lock:
                    SPENT["fail"] += 1; _pj(model)["fail"] += 1
                return None
            time.sleep(backoff ** attempt)
            continue
        if r.status_code in (429, 500, 502, 503, 529):
            if attempt == max_retries - 1:
                with _spend_lock:
                    SPENT["fail"] += 1; _pj(model)["fail"] += 1
                return None
            time.sleep(backoff ** attempt)
            continue
        if r.status_code != 200:
            with _spend_lock:
                SPENT["fail"] += 1; _pj(model)["fail"] += 1
            return None
        try:
            j = r.json()
        except Exception:
            with _spend_lock:
                SPENT["fail"] += 1; _pj(model)["fail"] += 1
            return None
        usage = j.get("usage", {}) or {}
        pin = int(usage.get("prompt_tokens", 0)); pout = int(usage.get("completion_tokens", 0))
        cost = pin * judge["cost_in"] + pout * judge["cost_out"]
        with _spend_lock:
            SPENT["usd"] += cost; SPENT["calls"] += 1
            pjd = _pj(model); pjd["usd"] += cost; pjd["calls"] += 1
        try:
            content = j["choices"][0]["message"]["content"]
        except Exception:
            with _spend_lock:
                SPENT["refusal"] += 1; _pj(model)["refusal"] += 1
            return None
        parsed = _parse_judge(content)
        if parsed is None:
            with _spend_lock:
                SPENT["refusal"] += 1; _pj(model)["refusal"] += 1
            return None
        return parsed
    return None


def run_judge_batch(tasks, judge):
    if not tasks:
        return []
    results = [None] * len(tasks)
    with ThreadPoolExecutor(max_workers=JUDGE_WORKERS) as ex:
        futs = {ex.submit(judge_call, t, judge): i for i, t in enumerate(tasks)}
        for fut in futs:
            i = futs[fut]
            try:
                results[i] = fut.result()
            except Exception:
                results[i] = None
    return results


def resolve_second_judge():
    """Probe second-judge candidates with one tiny call; return the first that parses, else None."""
    if not os.environ.get("OPENROUTER_API_KEY"):
        return None
    probe_task = {"role": "RETAIN", "X": "test", "prompt": "The capital of France is",
                  "base_cont": "Paris, a large city.", "edit_cont": "Paris, a large city."}
    for cand in SECOND_JUDGE_CANDIDATES:
        try:
            r = judge_call(probe_task, cand)
        except Exception:
            r = None
        if r is not None:
            logger.info(f"{el()} second judge resolved -> {cand['model']}")
            return cand
        logger.warning(f"{el()} second-judge candidate failed: {cand['model']}")
    return None


def harmonic_mean(f, c):
    f = float(f); c = float(c)
    if f <= 0 and c <= 0:
        return 0.0
    return (2.0 * f * c) / (f + c + 1e-9)


# =========================================================================== GENERATION under edit hook
def generate_under_edit(mb, sae, prompts, kind=None, l=None, u=None, v=None, scale=0.0,
                        max_new=MAX_NEW, batch=GEN_BATCH, clamp_norm=False):
    """Greedy continuations under an optional forward edit hook installed at the edit layer."""
    torch = mb.torch; tok = mb.tok
    handle = None
    if kind:
        handle = mb.edit_layer().register_forward_hook(
            _make_clamped_hook(torch, sae, kind, l=l, u=u, v=v, scale=scale) if clamp_norm
            else make_edit_hook(torch, sae, kind, l=l, u=u, v=v, scale=scale))
    old = tok.padding_side; tok.padding_side = "left"
    pad_id = tok.pad_token_id if tok.pad_token_id is not None else tok.eos_token_id
    outs = []
    try:
        for b0 in range(0, len(prompts), batch):
            bp = prompts[b0:b0 + batch]
            enc = tok(bp, return_tensors="pt", padding=True, truncation=True,
                      max_length=GEN_MAXLEN_PROMPT, add_special_tokens=True)
            enc = {k: vv.to(DEVICE) for k, vv in enc.items()}
            plen = enc["input_ids"].shape[1]
            with torch.no_grad():
                gen = mb.model.generate(**enc, max_new_tokens=max_new, do_sample=False,
                                        use_cache=True, pad_token_id=pad_id)
            for i in range(len(bp)):
                new_ids = gen[i, plen:]
                txt = tok.decode(new_ids, skip_special_tokens=True).strip()
                outs.append(txt)
            del gen
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
    finally:
        if handle:
            handle.remove()
        tok.padding_side = old
    return outs


def _make_clamped_hook(torch, sae, kind, l=None, u=None, v=None, scale=0.0):
    """Fallback edit hook that clamps the edited residual norm to the unedited per-token norm
    (prevents bf16 blow-ups / NaNs during free generation). Supports list-of-latents for the unit op."""
    def hook(_m, _i, out):
        h = out[0] if isinstance(out, (tuple, list)) else out
        hf = h.to(torch.float32)
        n_before = hf.norm(dim=-1, keepdim=True)
        if kind == "abl_latent":
            z = sae.encode(hf)
            if isinstance(l, (list, tuple, np.ndarray)):
                contrib = None
                for m in l:
                    m = int(m)
                    cm = z[..., m:m + 1] * sae.W_dec[m].view(1, 1, -1)
                    contrib = cm if contrib is None else contrib + cm
            else:
                contrib = z[..., l:l + 1] * sae.W_dec[l].view(1, 1, -1)
            hf = hf - scale * contrib
        elif kind == "erase_dir":
            dot = (hf @ u)
            hf = hf - scale * dot.unsqueeze(-1) * u.view(1, 1, -1)
        elif kind == "add_latent":
            hf = hf + scale * v.view(1, 1, -1)
        n_after = hf.norm(dim=-1, keepdim=True)
        scale_back = torch.clamp(n_before / (n_after + 1e-6), max=1.0)
        hf = hf * scale_back
        h = hf.to(h.dtype)
        if isinstance(out, (tuple, list)):
            return (h,) + tuple(out[1:])
        return h
    return hook


def continuation_ppl(mb, texts, batch=8):
    """Self-perplexity of each continuation under the UNEDITED base model (lower=more fluent)."""
    torch = mb.torch; tok = mb.tok
    out = np.full(len(texts), np.nan)
    idx_valid = [i for i, t in enumerate(texts) if len(t.strip()) > 0]
    for b0 in range(0, len(idx_valid), batch):
        bidx = idx_valid[b0:b0 + batch]
        bt = [texts[i] for i in bidx]
        enc = tok(bt, return_tensors="pt", padding=True, truncation=True, max_length=64,
                  add_special_tokens=True)
        ids = enc["input_ids"].to(DEVICE); am = enc["attention_mask"].to(DEVICE)
        labels = ids.clone(); labels[am == 0] = -100
        with torch.no_grad():
            o = mb.model(input_ids=ids, attention_mask=am)
        logits = o.logits[:, :-1, :].to(torch.float32)
        tgt = labels[:, 1:]
        logp = torch.log_softmax(logits, dim=-1)
        tgt_clamped = tgt.clamp(min=0)
        tok_lp = logp.gather(-1, tgt_clamped.unsqueeze(-1)).squeeze(-1)
        mask = (tgt != -100).float()
        per_row = -(tok_lp * mask).sum(1) / mask.sum(1).clamp(min=1)
        ppl = torch.exp(per_row.clamp(max=20)).cpu().numpy()
        for k, i in enumerate(bidx):
            n_real = float(mask[k].sum().item())
            out[i] = float(ppl[k]) if n_real >= 1 else np.nan
        del o, logits, logp
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return out


def last_tok_logprobs(mb, sae, texts, kind=None, l=None, u=None, v=None, scale=0.0, batch=8):
    """Next-token log-probs at the LAST real token of each prompt, under an optional edit hook -> [N,V] fp16."""
    torch = mb.torch; tok = mb.tok; V = len(tok)
    N = len(texts); lp_out = np.zeros((N, V), dtype=np.float16)
    handle = (mb.edit_layer().register_forward_hook(
        make_edit_hook(torch, sae, kind, l=l, u=u, v=v, scale=scale)) if kind else None)
    old = tok.padding_side; tok.padding_side = "right"
    try:
        for b0 in range(0, N, batch):
            bt = texts[b0:b0 + batch]
            enc = tok(bt, return_tensors="pt", padding=True, truncation=True,
                      max_length=GEN_MAXLEN_PROMPT, add_special_tokens=True)
            am = enc["attention_mask"]
            enc = {k: vv.to(DEVICE) for k, vv in enc.items()}
            with torch.no_grad():
                o = mb.model(**enc)
            logits = o.logits
            for i in range(len(bt)):
                T = int(am[i].sum()); pos = max(T - 1, 0)
                lp = torch.log_softmax(logits[i, pos].float(), -1)
                lp_out[b0 + i] = lp.half().cpu().numpy()
            del o, logits
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
    finally:
        if handle:
            handle.remove()
        tok.padding_side = old
    return lp_out


# =========================================================================== prompt builders
def _prefix_before_span(text, span, min_chars=15):
    if span and span[0] is not None and int(span[0]) >= min_chars:
        cut = int(span[0]); pre = text[:cut].rstrip()
        if len(pre) >= min_chars:
            return pre
    cut = max(min_chars, int(len(text) * 0.6)); pre = text[:cut]
    sp = pre.rfind(" ")
    if sp > min_chars:
        pre = pre[:sp]
    return pre.rstrip() or text[:min_chars]


def build_prompts(rows, role, n, use_span=True):
    prompts, meta = [], []
    for r in rows[:n]:
        text = r["input"]
        pre = _prefix_before_span(text, r.get("_span")) if use_span else _prefix_before_span(text, None)
        if len(pre.strip()) < 8:
            continue
        prompts.append(pre)
        meta.append({"sub_context": r.get("metadata_sub_context") or r.get("metadata_target_word"),
                     "full": text[:240]})
    return prompts, meta


# =========================================================================== u_sub (the M1' comparator)
def build_u_sub(torch, resid, pos_mask, sib_mask, u_whole_np, fb_pos_mask=None, fb_sib_mask=None):
    """SUB-CONTEXT-TARGETED dense direction: diff-of-means(target-sub-positive, sibling-positive) on the
    DISJOINT fit fold. A second single hyperplane (like u_whole) but built from the sub-context partition,
    so it CAN localize. Returns (unit-tensor, meta). Falls back to all-non-eval folds when underpowered."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    pos = resid[pos_mask].astype(np.float32); sib = resid[sib_mask].astype(np.float32)
    used_fallback = False
    if ((len(pos) < MIN_SUB) or (len(sib) < MIN_SUB)) and fb_pos_mask is not None:
        pos = resid[fb_pos_mask].astype(np.float32); sib = resid[fb_sib_mask].astype(np.float32)
        used_fallback = True
    still_under = (len(pos) < MIN_SUB) or (len(sib) < MIN_SUB)
    if len(pos) == 0 or len(sib) == 0:
        # degenerate guard: return whole-parent direction so downstream never crashes (flagged underpowered)
        u = (u_whole_np / (np.linalg.norm(u_whole_np) + 1e-9)).astype(np.float32)
        return torch.tensor(u, device=DEVICE), {"n_pos": int(len(pos)), "n_sib": int(len(sib)),
                                                "underpowered": True, "used_fallback": bool(used_fallback),
                                                "sub_probe_auc": 0.5, "cos_with_whole_parent": 1.0,
                                                "degenerate_fallback_to_whole": True}
    mu = pos.mean(0) - sib.mean(0)
    u_sub = (mu / (np.linalg.norm(mu) + 1e-9)).astype(np.float32)
    try:
        Xp = np.concatenate([pos, sib], 0)
        yp = np.concatenate([np.ones(len(pos)), np.zeros(len(sib))])
        clf = LogisticRegression(max_iter=2000, C=1.0, class_weight="balanced").fit(Xp, yp)
        auc = float(roc_auc_score(yp, clf.decision_function(Xp)))
    except Exception:
        auc = 0.5
    uw = u_whole_np / (np.linalg.norm(u_whole_np) + 1e-9)
    cos_whole = float(u_sub @ uw)
    meta = {"n_pos": int(len(pos)), "n_sib": int(len(sib)), "underpowered": bool(still_under),
            "used_fallback": bool(used_fallback), "sub_probe_auc": auc,
            "cos_with_whole_parent": cos_whole, "degenerate_fallback_to_whole": False}
    return torch.tensor(u_sub, device=DEVICE), meta


def _router_anchors(lat_csr, parent_latent, absorber, target_rows_for_jaccard):
    fj = hole = None
    if lat_csr is not None and parent_latent is not None:
        col_par = np.asarray(lat_csr[:, parent_latent].todense()).ravel() > 0
        col_abs = np.asarray(lat_csr[:, absorber].todense()).ravel() > 0
        union = int((col_par | col_abs).sum())
        fj = int((col_par & col_abs).sum()) / max(union, 1)
        if target_rows_for_jaccard is not None and len(target_rows_for_jaccard):
            par_on_X = np.asarray(lat_csr[target_rows_for_jaccard, parent_latent].todense()).ravel() > 0
            hole = 1.0 - float(par_on_X.mean())
    return fj, hole


# =========================================================================== CASE SETUP
class CaseSpec:
    pass


def setup_taxonomic(torch, sae, mb, canon, args, Rnorm, target=("Georgia", 16009, 0.955),
                    case_id="taxonomic_georgia", regime="absorption", run_m7=False):
    X, absorber, precision = target
    logger.info(f"\n{el()} ===== SETUP taxonomic / {X} (absorber {absorber}, regime={regime}) =====")
    rows = load_taxonomic()
    corp = [r for r in rows if r["metadata_row_type"] == "corpus"]
    cpairs = [r for r in rows if r["metadata_row_type"] == "content_pair"]
    eligible = ['Australia', 'Brazil', 'Canada', 'China', 'France', 'Georgia', 'Germany', 'India',
                'Iran', 'Ireland', 'Israel', 'Italy', 'Japan', 'Mexico', 'New Zealand', 'Poland',
                'Russia', 'Spain', 'United Kingdom', 'United States']
    encode_countries = set(eligible) | {X}
    cap = args.cap
    enc_rows, tag = [], []
    for r in corp:
        sc = r.get("metadata_sub_context")
        if r["output"] == "positive" and sc in encode_countries:
            if cap and sc in eligible and sum(1 for t in tag if t == ("pos", sc, r["metadata_fold"])) >= cap:
                continue
            enc_rows.append(r); tag.append(("pos", sc, r["metadata_fold"]))
        elif r["output"] == "negative":
            if cap and sum(1 for t in tag if t[0] == "neg" and t[2] == r["metadata_fold"]) >= cap * 4:
                continue
            enc_rows.append(r); tag.append(("neg", None, r["metadata_fold"]))
    n_corp = len(enc_rows)
    for r in cpairs:
        enc_rows.append(r); tag.append(("cp", r.get("metadata_pair_role"), r.get("metadata_pair_id")))
    logger.info(f"{el()} taxonomic encoding {len(enc_rows)} rows ({n_corp} corpus + {len(cpairs)} cp)")
    lat_csr, resid, _ = mb.encode_rows(enc_rows, sae)
    tag = np.array(tag, dtype=object)
    kind = np.array([t[0] for t in tag], dtype=object)
    sub = np.array([t[1] for t in tag], dtype=object)
    fold = np.array([t[2] for t in tag], dtype=object)

    pairs = {}
    for i in np.where(kind == "cp")[0]:
        pairs.setdefault(tag[i][2], {})[tag[i][1]] = i
    pl = [p for p, d in pairs.items() if "x_on" in d and "x_off" in d]
    cr = np.array([], int)
    if pl:
        A_on = np.asarray(lat_csr[[pairs[p]["x_on"] for p in pl]].todense())
        A_off = np.asarray(lat_csr[[pairs[p]["x_off"] for p in pl]].todense())
        cr, _, _ = content_responsive(A_on, A_off)
        del A_on, A_off

    fit_pos = np.where((kind == "pos") & (fold == "diagnostic"))[0]
    fit_neg = np.where((kind == "neg") & (fold == "diagnostic"))[0]
    probe = ParentProbe(torch, resid[fit_pos].astype(np.float32), resid[fit_neg].astype(np.float32))
    probe._Rnorm = Rnorm
    logger.info(f"{el()} taxonomic probe train_auc={probe.train_auc:.3f} cos(probe,dmu)={probe.cos_probe_dmu:.3f}")

    anchor = canon["taxonomic"]["anchor"]
    ev = "train"
    sib_names = [c for c in eligible if c != X]
    forget_idx = np.where((kind == "pos") & (sub == X) & (fold == ev))[0]
    if len(forget_idx) < 8:
        forget_idx = np.where((kind == "pos") & (sub == X))[0]
    retain_idx = np.where((kind == "pos") & (sub != X) & np.isin(sub, sib_names) & (fold == ev))[0]
    unrel_idx = np.where((kind == "neg") & (fold == ev))[0]

    # ----- u_sub: target-sub-positive vs sibling-positive on the DISJOINT (diagnostic) fit fold -----
    pos_mask = (kind == "pos") & (sub == X) & (fold == "diagnostic")
    sib_mask = (kind == "pos") & (sub != X) & np.isin(sub, sib_names) & (fold == "diagnostic")
    noneval = (fold != ev)
    fb_pos = (kind == "pos") & (sub == X) & noneval
    fb_sib = (kind == "pos") & (sub != X) & np.isin(sub, sib_names) & noneval
    u_sub_t, u_sub_meta = build_u_sub(torch, resid, pos_mask, sib_mask, probe.d_mu, fb_pos, fb_sib)
    logger.info(f"{el()} u_sub: n_pos={u_sub_meta['n_pos']} n_sib={u_sub_meta['n_sib']} "
                f"auc={u_sub_meta['sub_probe_auc']:.3f} cos_whole={u_sub_meta['cos_with_whole_parent']:.3f} "
                f"underpowered={u_sub_meta['underpowered']}")

    member_set = set(canon["taxonomic"]["k_track_unit"]) | \
        set(a["latent"] for a in canon["taxonomic"]["diag_absorbers"])
    rand_lat, trate = pick_random_latents(lat_csr, absorber, cr, member_set)

    # M5: report BOTH firing-Jaccards — the specific absorber vs the aggregate parent detector
    tgt_for_j = np.where((kind == "pos") & (sub == X))[0]
    fj_abs, hole_abs = _router_anchors(lat_csr, anchor, absorber, tgt_for_j)
    # aggregate "parent detector" = the C-track anchor unit OR'd into a single column-ish detector
    col_par_any = None
    for m in canon["taxonomic"]["k_track_unit"]:
        c = np.asarray(lat_csr[:, int(m)].todense()).ravel() > 0
        col_par_any = c if col_par_any is None else (col_par_any | c)
    col_abs = np.asarray(lat_csr[:, absorber].todense()).ravel() > 0
    union = int((col_par_any | col_abs).sum())
    fj_aggregate = int((col_par_any & col_abs).sum()) / max(union, 1)

    cs = CaseSpec()
    cs.case_id = case_id; cs.family = "taxonomic"; cs.X = X; cs.absorber = absorber
    cs.absorber_precision = precision; cs.anchor = anchor; cs.regime = regime
    cs.probe = probe; cs.u = probe.u_t; cs.u_sub = u_sub_t; cs.u_sub_meta = u_sub_meta
    cs.forget_rows = [enc_rows[i] for i in forget_idx]
    cs.retain_rows = [enc_rows[i] for i in retain_idx]
    cs.unrel_rows = [enc_rows[i] for i in unrel_idx]
    cs.siblings = sib_names; cs.rand_latents = rand_lat; cs.rand_rate = trate
    cs.firing_jaccard = fj_abs; cs.parent_recall_hole = hole_abs
    cs.firing_jaccard_aggregate = float(fj_aggregate)
    cs.whole_sentence = False; cs.use_span = True
    cs.neutral_unrel = list(NEUTRAL_TEXT)
    cs.kg_unit = sorted(set(int(m) for m in canon["taxonomic"]["k_track_unit"]) | {int(absorber)})
    cs.run_m7 = run_m7
    del lat_csr, resid
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return cs


def setup_first_letter(torch, sae, mb, canon, args, Rnorm):
    logger.info(f"\n{el()} ===== SETUP first_letter / large =====")
    letters = ["L", "O", "T", "I", "D"]
    groups = load_first_letter(letters)
    unit = canon["first_letter"]["L"]; anchor = unit["anchor"]
    cap = args.cap
    enc_rows, tag = [], []
    Lcorp = [r for r in groups["L"] if r.get("metadata_pair_type") == "corpus_context"]
    for r in Lcorp:
        enc_rows.append(r); tag.append(("L", r.get("metadata_sub_context"), r.get("metadata_fold")))
    neg_letters = ["O", "T", "I", "D"]
    per_neg = (cap or 250)
    for lt in neg_letters:
        cc = [r for r in groups[lt] if r.get("metadata_pair_type") == "corpus_context"][:per_neg]
        for r in cc:
            enc_rows.append(r); tag.append((lt, r.get("metadata_sub_context"), r.get("metadata_fold")))
    Lpairs = [r for r in groups["L"] if r.get("metadata_pair_type") == "content_flip"
              and r.get("metadata_template_id") in {"t_verbose", "t_colon", "t_icl"}]
    for r in Lpairs:
        enc_rows.append(r); tag.append(("cp", r.get("metadata_role"), r.get("metadata_pair_id")))
    logger.info(f"{el()} first-letter encoding {len(enc_rows)} rows")
    lat_csr, resid, _ = mb.encode_rows(enc_rows, sae)
    tag = np.array(tag, dtype=object)
    letter = np.array([t[0] for t in tag], dtype=object)
    sub = np.array([t[1] for t in tag], dtype=object)
    fold = np.array([t[2] for t in tag], dtype=object)

    pairs = {}
    for i in np.where(letter == "cp")[0]:
        pairs.setdefault(tag[i][2], {})[tag[i][1]] = i
    pl = [p for p, d in pairs.items() if "on" in d and "off" in d]
    cr = np.array([], int)
    if pl:
        A_on = np.asarray(lat_csr[[pairs[p]["on"] for p in pl]].todense())
        A_off = np.asarray(lat_csr[[pairs[p]["off"] for p in pl]].todense())
        cr, _, _ = content_responsive(A_on, A_off)
        del A_on, A_off

    is_corpus = np.isin(letter, ["L"] + neg_letters)
    fit_mask = is_corpus & np.isin(fold, [0, 1, 2])
    eval_mask = is_corpus & np.isin(fold, [3, 4])
    fit_pos = np.where(fit_mask & (letter == "L"))[0]
    fit_neg = np.where(fit_mask & (letter != "L") & is_corpus)[0]
    probe = ParentProbe(torch, resid[fit_pos].astype(np.float32), resid[fit_neg].astype(np.float32))
    probe._Rnorm = Rnorm
    logger.info(f"{el()} first-letter probe train_auc={probe.train_auc:.3f}")

    X = "large"; absorber = 8463
    forget_idx = np.where(eval_mask & (letter == "L") & (sub == X))[0]
    if len(forget_idx) < 8:
        forget_idx = np.where((letter == "L") & (sub == X))[0]
    sib_words = [w for w in Counter(sub[(letter == "L")]).keys() if w and w != X]
    retain_idx = np.where((letter == "L") & np.isin(sub, sib_words) & (sub != X))[0]
    if len(retain_idx) > 400:
        retain_idx = rng.choice(retain_idx, 400, replace=False)
    unrel_idx = np.array([], int)

    # ----- u_sub: 'large' L-tokens vs sibling-L-word tokens on the DISJOINT fit folds [0,1,2] -----
    fitf = np.isin(fold, [0, 1, 2])
    pos_mask = (letter == "L") & (sub == X) & fitf
    sib_mask = (letter == "L") & np.isin(sub, sib_words) & (sub != X) & fitf
    noneval = is_corpus & ~np.isin(fold, [3, 4])
    fb_pos = (letter == "L") & (sub == X) & noneval
    fb_sib = (letter == "L") & np.isin(sub, sib_words) & (sub != X) & noneval
    u_sub_t, u_sub_meta = build_u_sub(torch, resid, pos_mask, sib_mask, probe.d_mu, fb_pos, fb_sib)
    logger.info(f"{el()} u_sub: n_pos={u_sub_meta['n_pos']} n_sib={u_sub_meta['n_sib']} "
                f"auc={u_sub_meta['sub_probe_auc']:.3f} cos_whole={u_sub_meta['cos_with_whole_parent']:.3f}")

    member_set = set(unit["members"])
    rand_lat, trate = pick_random_latents(lat_csr, absorber, cr, member_set)
    fj, hole = _router_anchors(lat_csr, anchor, absorber, np.where((letter == "L") & (sub == X))[0])

    cs = CaseSpec()
    cs.case_id = "first_letter_large"; cs.family = "first_letter"; cs.X = X; cs.absorber = absorber
    cs.absorber_precision = 1.0; cs.anchor = anchor; cs.regime = "absorption"
    cs.probe = probe; cs.u = probe.u_t; cs.u_sub = u_sub_t; cs.u_sub_meta = u_sub_meta
    cs.forget_rows = [enc_rows[i] for i in forget_idx]
    cs.retain_rows = [enc_rows[i] for i in retain_idx]
    cs.unrel_rows = []
    cs.siblings = sib_words[:12]; cs.rand_latents = rand_lat; cs.rand_rate = trate
    cs.firing_jaccard = fj; cs.parent_recall_hole = hole; cs.firing_jaccard_aggregate = fj
    cs.whole_sentence = False; cs.use_span = True
    cs.neutral_unrel = list(NEUTRAL_TEXT)
    cs.kg_unit = sorted(set(int(m) for m in unit["members"]) | {int(absorber)})
    cs.run_m7 = True
    del lat_csr, resid
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return cs


def setup_toxicity(torch, sae, mb, canon, args, Rnorm):
    logger.info(f"\n{el()} ===== SETUP toxicity / insult (co-firing, KG predicted to LOSE) =====")
    from sklearn.metrics import roc_auc_score
    rows = load_toxicity()
    cap = args.cap or 400
    subs = ["insult", "obscene", "threat", "identity_attack"]

    def sv(r, n):
        sf = r.get("metadata_subcontext_floats") or {}
        return float(sf.get(n, 0.0))

    toxic = [r for r in rows if r.get("metadata_toxicity_label") == 1]
    neutral = [r for r in rows if r.get("metadata_toxicity_label") == 0]
    rng.shuffle(toxic); rng.shuffle(neutral)
    n = min(len(toxic), len(neutral), cap * 6)
    enc_rows = toxic[:n] + neutral[:n]
    folds = [r.get("metadata_fold") for r in enc_rows]
    logger.info(f"{el()} toxicity encoding {len(enc_rows)} sentences (whole-sentence pooling)")
    lat_csr, resid, _ = mb.encode_rows(enc_rows, sae, whole_sentence=True)
    label = np.array([1 if r.get("metadata_toxicity_label") == 1 else 0 for r in enc_rows])
    fold = np.array(folds, dtype=object)
    subm = {s: np.array([1 if sv(r, s) >= 0.5 else 0 for r in enc_rows]) for s in subs}

    fit_mask = (fold == "train"); eval_mask = np.isin(fold, ["test", "val"])
    fp = np.where(fit_mask & (label == 1))[0]; fn = np.where(fit_mask & (label == 0))[0]
    probe = ParentProbe(torch, resid[fp].astype(np.float32), resid[fn].astype(np.float32))
    probe._Rnorm = Rnorm
    logger.info(f"{el()} toxicity probe train_auc={probe.train_auc:.3f}")

    toxrows = np.where((label == 1) & fit_mask)[0]
    fire_tox = np.asarray((lat_csr[toxrows] > 0).sum(0)).ravel() / max(len(toxrows), 1)
    parent_latent = int(np.argmax(fire_tox))
    tox_fit = np.where((label == 1) & fit_mask)[0]
    yins = subm["insult"][tox_fit]
    best_lat, best_auc = None, 0.5
    if yins.sum() >= 20 and (len(yins) - yins.sum()) >= 20:
        cols = np.asarray(lat_csr[tox_fit].todense())
        firefrac = (cols > 0).mean(0)
        cand = np.where(firefrac > 0.02)[0]
        for c in cand:
            try:
                a = roc_auc_score(yins, cols[:, c])
            except Exception:
                continue
            if a > best_auc:
                best_auc, best_lat = a, int(c)
    if best_lat is None:
        logger.warning("toxicity: no insult sub-attribute latent found")
        del lat_csr, resid; gc.collect()
        return None
    absorber = best_lat
    logger.info(f"{el()} toxicity insult latent={absorber} AUC={best_auc:.3f} parent={parent_latent}")

    forget_idx = np.where(eval_mask & (label == 1) & (subm["insult"] == 1))[0]
    sib_mask_idx = eval_mask & (label == 1) & (subm["insult"] == 0) & (
        (subm["obscene"] == 1) | (subm["threat"] == 1) | (subm["identity_attack"] == 1))
    retain_idx = np.where(sib_mask_idx)[0]
    unrel_idx = np.where((label == 0) & eval_mask)[0]
    if len(forget_idx) > 400:
        forget_idx = rng.choice(forget_idx, 400, replace=False)
    if len(retain_idx) > 400:
        retain_idx = rng.choice(retain_idx, 400, replace=False)

    # ----- u_sub: insult-positive toxic vs sibling-toxic insult-negative on the TRAIN (fit) fold -----
    pos_mask = (label == 1) & (subm["insult"] == 1) & fit_mask
    sib_mask = (label == 1) & (subm["insult"] == 0) & (
        (subm["obscene"] == 1) | (subm["threat"] == 1) | (subm["identity_attack"] == 1)) & fit_mask
    u_sub_t, u_sub_meta = build_u_sub(torch, resid, pos_mask, sib_mask, probe.d_mu)
    logger.info(f"{el()} u_sub(insult): n_pos={u_sub_meta['n_pos']} n_sib={u_sub_meta['n_sib']} "
                f"auc={u_sub_meta['sub_probe_auc']:.3f} cos_whole={u_sub_meta['cos_with_whole_parent']:.3f}")

    member_set = {absorber, parent_latent}
    responsive_tox = np.where(fire_tox > 0.05)[0]
    rand_lat, trate = pick_random_latents(lat_csr, absorber, responsive_tox, member_set)
    fj, hole = _router_anchors(lat_csr, parent_latent, absorber,
                               np.where((label == 1) & (subm["insult"] == 1))[0])

    cs = CaseSpec()
    cs.case_id = "toxicity_insult"; cs.family = "toxicity"; cs.X = "insult"; cs.absorber = absorber
    cs.absorber_precision = float(best_auc); cs.anchor = parent_latent; cs.regime = "co-firing"
    cs.probe = probe; cs.u = probe.u_t; cs.u_sub = u_sub_t; cs.u_sub_meta = u_sub_meta
    cs.forget_rows = [enc_rows[i] for i in forget_idx]
    cs.retain_rows = [enc_rows[i] for i in retain_idx]
    cs.unrel_rows = [enc_rows[i] for i in unrel_idx]
    cs.siblings = ["obscene", "threat", "identity_attack"]; cs.rand_latents = rand_lat; cs.rand_rate = trate
    cs.firing_jaccard = fj; cs.parent_recall_hole = hole; cs.firing_jaccard_aggregate = fj
    cs.whole_sentence = True; cs.use_span = False
    cs.neutral_unrel = []
    cs.insult_auc = float(best_auc)
    cs.kg_unit = None; cs.run_m7 = False
    del lat_csr, resid
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return cs


# =========================================================================== edit-kwargs helper
def op_kwargs(cs, op, scales):
    """Map an operator name -> edit kwargs (kind/l/u/scale) given the resolved per-op scale dict."""
    if op == "NOOP":
        return {"kind": None}
    if op == "KG-ABL":
        return {"kind": "abl_latent", "l": cs.absorber, "scale": scales["KG-ABL"]}
    if op == "DENSE-SUB-ABL":
        return {"kind": "erase_dir", "u": cs.u_sub, "scale": scales["DENSE-SUB-ABL"]}
    if op == "DENSE-WHOLE-ABL":
        return {"kind": "erase_dir", "u": cs.u, "scale": scales["DENSE-WHOLE-ABL"]}
    if op == "RAND":
        rl = int(cs.rand_latents[0]) if cs.rand_latents else None
        return {"kind": "abl_latent", "l": rl, "scale": RAND_SCALE} if rl is not None else {"kind": None}
    if op == "KG-ABL-UNIT":
        return {"kind": "abl_latent", "l": cs.kg_unit, "scale": scales["KG-ABL-UNIT"]}
    raise ValueError(op)


# =========================================================================== the UNLEARNING experiment (M1')
def run_unlearning_case(torch, sae, mb, cs, args, primary_judge=PRIMARY_JUDGE, second_judge=None):
    logger.info(f"\n{el()} ##### UNLEARN CASE {cs.case_id} (absorber={cs.absorber}, regime={cs.regime}) #####")
    ws = cs.whole_sentence
    l = cs.absorber; u_whole = cs.u; u_sub = cs.u_sub

    n_forget = min(len(cs.forget_rows), args.forget_cap)
    n_retain_curve = min(len(cs.retain_rows), args.retain_curve_cap)
    n_retain_collat = min(len(cs.retain_rows), args.retain_collat_cap)
    forget_rows = cs.forget_rows[:n_forget]
    retain_curve_rows = cs.retain_rows[:n_retain_curve]
    retain_collat_rows = cs.retain_rows[:n_retain_collat]
    unrel_rows = cs.unrel_rows[:args.unrel_curve_cap] if cs.unrel_rows else []

    # =================== FORGET-QUALITY MATCHING (model-internal next-token KL on FORGET) ================
    base_forget, _ = forward_pos_logprobs(mb, sae, forget_rows, whole_sentence=ws)
    forget_kg_kl, foot_kg = behavioral_curve(mb, sae, forget_rows, base_forget, "abl_latent",
                                             l=l, scales=LAM_GRID, whole_sentence=ws)
    forget_sub_kl, foot_sub = behavioral_curve(mb, sae, forget_rows, base_forget, "erase_dir",
                                               u=u_sub, scales=BETA_GRID, whole_sentence=ws)
    forget_whl_kl, foot_whl = behavioral_curve(mb, sae, forget_rows, base_forget, "erase_dir",
                                               u=u_whole, scales=BETA_GRID, whole_sentence=ws)
    forget_kg_curve = forget_kg_kl.mean(0); forget_sub_curve = forget_sub_kl.mean(0)
    forget_whl_curve = forget_whl_kl.mean(0)
    max_kg = float(forget_kg_curve.max()); max_sub = float(forget_sub_curve.max())
    max_whl = float(forget_whl_curve.max())
    # DECISIVE pair is KG vs SUB -> match to 0.8*min(max_kg, max_sub)
    matched_target = max(1e-4, 0.8 * min(max_kg, max_sub))
    s_kg = _scale_for_on_target(LAM_GRID, forget_kg_curve.tolist(), matched_target)
    s_sub = _scale_for_on_target(BETA_GRID, forget_sub_curve.tolist(), matched_target)
    s_whl = _scale_for_on_target(BETA_GRID, forget_whl_curve.tolist(), matched_target)
    scales = {"KG-ABL": s_kg, "DENSE-SUB-ABL": s_sub, "DENSE-WHOLE-ABL": s_whl}
    sub_reaches = bool(max_sub >= matched_target)
    logger.info(f"{el()} FORGET match: max_kg={max_kg:.4f} max_sub={max_sub:.4f} max_whl={max_whl:.4f} "
                f"target={matched_target:.4f} s_kg={s_kg:.3f} s_sub={s_sub:.3f} s_whl={s_whl:.3f}")

    # M7 unit forget curve / scale (matched to SAME target)
    s_unit = None; forget_unit_curve = None; foot_unit = None
    if cs.run_m7 and cs.kg_unit:
        forget_unit_kl, foot_unit = behavioral_curve(mb, sae, forget_rows, base_forget, "abl_latent",
                                                     l=cs.kg_unit, scales=LAM_GRID, whole_sentence=ws)
        forget_unit_curve = forget_unit_kl.mean(0)
        s_unit = _scale_for_on_target(LAM_GRID, forget_unit_curve.tolist(), matched_target)
        scales["KG-ABL-UNIT"] = s_unit
        logger.info(f"{el()} M7 unit forget: max_unit={forget_unit_curve.max():.4f} s_unit={s_unit:.3f} "
                    f"unit_members={cs.kg_unit}")
    del base_forget

    # =================== MODEL-INTERNAL COLLATERAL: high-n retain next-token KL at matched =============
    base_retain_c, _ = forward_pos_logprobs(mb, sae, retain_collat_rows, whole_sentence=ws)
    retain_kl = {}
    collat_ops = ["KG-ABL", "DENSE-SUB-ABL", "DENSE-WHOLE-ABL"] + (["KG-ABL-UNIT"] if s_unit is not None else [])
    for op in collat_ops:
        kw = op_kwargs(cs, op, scales)
        elp, _ = forward_pos_logprobs(mb, sae, retain_collat_rows, whole_sentence=ws, **kw)
        retain_kl[op] = kl_rows(elp, base_retain_c)
        del elp
    del base_retain_c
    retain_kl_kg = retain_kl["KG-ABL"]; retain_kl_sub = retain_kl["DENSE-SUB-ABL"]
    retain_kl_whl = retain_kl["DENSE-WHOLE-ABL"]
    # DECISIVE collateral diff: KG vs SUB (>0 => KG less collateral than the sub-context dense dir)
    collat_diff_CI_KG_vs_SUB = paired_bootstrap_diff(retain_kl_sub, retain_kl_kg)
    collat_diff_CI_KG_vs_WHOLE = paired_bootstrap_diff(retain_kl_whl, retain_kl_kg)   # secondary
    # u_sub LOCALIZATION VALIDATION (proves the reviewer's point) — at the KG-PINNED matched-forget point.
    # NB: this point can be tiny (KG single-latent ablation has a small max next-token KL), where BOTH dense
    # erasures barely act; the ROBUST localization claim is the curve-based one below (over the achievable
    # dense forget range, not KG's ceiling).
    localizes_better_at_matched = bool(retain_kl_sub.mean() < retain_kl_whl.mean())
    sub_vs_whole_collat_CI = paired_bootstrap_diff(retain_kl_whl, retain_kl_sub)       # >0 => SUB localizes better
    m7_collat_CI = (paired_bootstrap_diff(retain_kl["KG-ABL-UNIT"], retain_kl_kg)
                    if s_unit is not None else None)                                    # >0 => single less collateral
    logger.info(f"{el()} retain collateral KL (n={len(retain_kl_kg)}): KG={retain_kl_kg.mean():.5f} "
                f"SUB={retain_kl_sub.mean():.5f} WHOLE={retain_kl_whl.mean():.5f} "
                f"localizes_at_matched(SUB<WHOLE)={localizes_better_at_matched} "
                f"KGvsSUB_excl0={collat_diff_CI_KG_vs_SUB['excl_0']}")

    # =================== CURVE-LEVEL DOMINANCE (model-internal, $0) ====================================
    base_retain_cu, _ = forward_pos_logprobs(mb, sae, retain_curve_rows, whole_sentence=ws)
    retain_kg_grid, _ = behavioral_curve(mb, sae, retain_curve_rows, base_retain_cu, "abl_latent",
                                         l=l, scales=LAM_GRID, whole_sentence=ws)
    retain_sub_grid, _ = behavioral_curve(mb, sae, retain_curve_rows, base_retain_cu, "erase_dir",
                                          u=u_sub, scales=BETA_GRID, whole_sentence=ws)
    retain_whl_grid, _ = behavioral_curve(mb, sae, retain_curve_rows, base_retain_cu, "erase_dir",
                                          u=u_whole, scales=BETA_GRID, whole_sentence=ws)
    retain_kg_mean = retain_kg_grid.mean(0); retain_sub_mean = retain_sub_grid.mean(0)
    retain_whl_mean = retain_whl_grid.mean(0)
    unrel_kg_mean = unrel_sub_mean = unrel_whl_mean = None
    if len(unrel_rows) >= 4:
        base_unrel, _ = forward_pos_logprobs(mb, sae, unrel_rows, whole_sentence=ws)
        uk, _ = behavioral_curve(mb, sae, unrel_rows, base_unrel, "abl_latent", l=l, scales=LAM_GRID, whole_sentence=ws)
        us, _ = behavioral_curve(mb, sae, unrel_rows, base_unrel, "erase_dir", u=u_sub, scales=BETA_GRID, whole_sentence=ws)
        uw, _ = behavioral_curve(mb, sae, unrel_rows, base_unrel, "erase_dir", u=u_whole, scales=BETA_GRID, whole_sentence=ws)
        unrel_kg_mean = uk.mean(0); unrel_sub_mean = us.mean(0); unrel_whl_mean = uw.mean(0)
    dom_kg_vs_sub = _curve_dominance(forget_kg_curve, retain_kg_mean, unrel_kg_mean, LAM_GRID,
                                     forget_sub_curve, retain_sub_mean, unrel_sub_mean, BETA_GRID)
    dom_kg_vs_whole = _curve_dominance(forget_kg_curve, retain_kg_mean, unrel_kg_mean, LAM_GRID,
                                       forget_whl_curve, retain_whl_mean, unrel_whl_mean, BETA_GRID)
    # ROBUST u_sub localization validation: over SHARED forget targets across the achievable DENSE range
    # (where both u_sub and u_whole actually act), is u_sub's sibling collateral < u_whole's?
    dense_loc = _dense_localization(forget_sub_curve, retain_sub_mean, forget_whl_curve, retain_whl_mean)
    localizes_better = bool(dense_loc["frac_sub_lt_whole"] >= 0.5)
    loc_info = {"localizes_better": localizes_better,
                "localizes_better_at_matched": localizes_better_at_matched,
                "dense_localization": dense_loc}
    logger.info(f"{el()} curve-dominance KG-vs-SUB={dom_kg_vs_sub['dominance_fraction']:.3f} "
                f"KG-vs-WHOLE={dom_kg_vs_whole['dominance_fraction']:.3f} | u_sub localizes better than whole "
                f"(curve frac)={dense_loc['frac_sub_lt_whole']:.2f} at_matched={localizes_better_at_matched}")

    # =================== GENERATION under each edit hook (NOOP/KG/SUB/WHOLE/RAND [+UNIT]) ===============
    gp_forget, _ = build_prompts(forget_rows, "FORGET", args.gen_per_set, use_span=cs.use_span)
    gp_retain, _ = build_prompts(cs.retain_rows, "RETAIN", args.gen_per_set, use_span=cs.use_span)
    if cs.unrel_rows:
        gp_unrel, _ = build_prompts(cs.unrel_rows, "UNRELATED", args.gen_per_set, use_span=cs.use_span)
    else:
        gp_unrel = list(cs.neutral_unrel)[:args.gen_per_set]
    if cs.neutral_unrel and cs.unrel_rows:
        gp_unrel = (gp_unrel + list(cs.neutral_unrel))[:args.gen_per_set + min(8, len(cs.neutral_unrel))]
    logger.info(f"{el()} gen prompts: forget={len(gp_forget)} retain={len(gp_retain)} unrel={len(gp_unrel)}")

    gen_ops = ["NOOP", "KG-ABL", "DENSE-SUB-ABL", "DENSE-WHOLE-ABL", "RAND"] + (["KG-ABL-UNIT"] if s_unit is not None else [])
    gen = {}
    for role, prompts in (("FORGET", gp_forget), ("RETAIN", gp_retain), ("UNRELATED", gp_unrel)):
        gen[role] = {"prompts": prompts}
        if not prompts:
            for op in gen_ops:
                gen[role][op] = []
            continue
        for op in gen_ops:
            kw = op_kwargs(cs, op, scales)
            conts = generate_under_edit(mb, sae, prompts, **kw)
            # degenerate guard for the two dense erasures (large beta can blow up bf16) -> norm-clamp retry
            if op in ("DENSE-SUB-ABL", "DENSE-WHOLE-ABL", "KG-ABL-UNIT") and _degenerate(conts):
                logger.warning(f"{el()} {role}/{op}: degenerate generation -> retry with norm-clamp")
                conts = generate_under_edit(mb, sae, prompts, clamp_norm=True, **kw)
            gen[role][op] = conts

    # ---- model-internal per-gen-prompt signals (collateral last-tok KL vs NOOP + continuation PPL) ----
    mi = {}
    for role in ("FORGET", "RETAIN", "UNRELATED"):
        prompts = gen[role]["prompts"]
        if not prompts:
            mi[role] = {}
            continue
        base_lp = last_tok_logprobs(mb, sae, prompts, kind=None)
        m = {}
        for op in gen_ops:
            if op == "NOOP":
                continue
            kw = op_kwargs(cs, op, scales)
            if kw.get("kind") is None:
                m[f"kl_{op}"] = np.zeros(len(prompts))
            else:
                elp = last_tok_logprobs(mb, sae, prompts, **kw)
                m[f"kl_{op}"] = kl_rows(elp, base_lp); del elp
            m[f"ppl_{op}"] = continuation_ppl(mb, gen[role][op])
        m["ppl_NOOP"] = continuation_ppl(mb, gen[role]["NOOP"])
        mi[role] = m
        del base_lp

    # =================== PRIMARY LLM JUDGE (AxBench harmonic-mean 0-2) =================================
    judge_ops = ["KG-ABL", "DENSE-SUB-ABL", "DENSE-WHOLE-ABL", "RAND"] + (["KG-ABL-UNIT"] if s_unit is not None else [])
    judged = _judge_ops(mb, gen, cs, judge_ops, primary_judge, roles=("FORGET", "RETAIN", "UNRELATED"),
                        label="PRIMARY")

    # =================== SECOND-FAMILY JUDGE on a STRATIFIED PRES subsample (M6) =======================
    judged2 = None; second_info = {"model": "unavailable"}
    if second_judge is not None and os.environ.get("OPENROUTER_API_KEY"):
        sub_idx = _stratified_pres_subsample(gen, cap_per_role=args.second_judge_cap)
        judged2 = _judge_ops_subset(mb, gen, cs, ["KG-ABL", "DENSE-SUB-ABL", "DENSE-WHOLE-ABL"],
                                    second_judge, sub_idx, label="SECOND")
        second_info = {"model": second_judge["model"], "subsample_idx": sub_idx,
                       "spend_usd": _pj(second_judge["model"])["usd"],
                       "calls": _pj(second_judge["model"])["calls"]}

    # =================== JOINT OUTCOME + FORK VERDICT =================================================
    res_out = _joint_and_fork(cs, gen, mi, judged, judged2, second_judge, second_info,
                              collat_diff_CI_KG_vs_SUB, collat_diff_CI_KG_vs_WHOLE, sub_vs_whole_collat_CI,
                              loc_info, dom_kg_vs_sub, dom_kg_vs_whole, scales, matched_target,
                              forget_kg_curve, forget_sub_curve, forget_whl_curve, forget_unit_curve,
                              foot_kg, foot_sub, foot_whl, foot_unit,
                              retain_kl_kg, retain_kl_sub, retain_kl_whl,
                              retain_kl.get("KG-ABL-UNIT"), m7_collat_CI, sub_reaches, max_kg, max_sub, max_whl)
    res_out["case_id"] = cs.case_id
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return res_out, gen, mi, judged, judged2


def _judge_ops(mb, gen, cs, ops, judge, roles, label):
    """Issue judge calls for the given ops over the given roles (all prompts). Returns judged[role][op]."""
    judged = {role: {op: [] for op in ops} for role in roles}
    if judge is None or not os.environ.get("OPENROUTER_API_KEY"):
        return judged
    tasks, locs = [], []
    for role in roles:
        g = gen[role]
        for j, p in enumerate(g["prompts"]):
            for op in ops:
                tasks.append({"role": role, "X": cs.X, "prompt": p[:700],
                              "base_cont": g["NOOP"][j][:500], "edit_cont": g[op][j][:500]})
                locs.append((role, op, j))
    logger.info(f"{el()} [{label} {judge['model']}] issuing {len(tasks)} judge calls (SPENT=${SPENT['usd']:.4f})")
    res = run_judge_batch(tasks, judge)
    tmp = {role: {op: {} for op in ops} for role in roles}
    for (role, op, j), r in zip(locs, res):
        tmp[role][op][j] = r
    for role in roles:
        npr = len(gen[role]["prompts"])
        for op in ops:
            judged[role][op] = [tmp[role][op].get(j) for j in range(npr)]
    logger.info(f"{el()} [{label}] done: model_calls={_pj(judge['model'])['calls']} "
                f"SPENT=${SPENT['usd']:.4f}")
    return judged


def _judge_ops_subset(mb, gen, cs, ops, judge, sub_idx, label):
    """Judge only the (role,j) pairs in sub_idx, for the given ops. Returns judged[role][op] (list aligned)."""
    roles = list(sub_idx.keys())
    judged = {role: {op: [None] * len(gen[role]["prompts"]) for op in ops} for role in roles}
    tasks, locs = [], []
    for role in roles:
        g = gen[role]
        for j in sub_idx[role]:
            for op in ops:
                tasks.append({"role": role, "X": cs.X, "prompt": g["prompts"][j][:700],
                              "base_cont": g["NOOP"][j][:500], "edit_cont": g[op][j][:500]})
                locs.append((role, op, j))
    logger.info(f"{el()} [{label} {judge['model']}] issuing {len(tasks)} subsample judge calls")
    res = run_judge_batch(tasks, judge)
    for (role, op, j), r in zip(locs, res):
        judged[role][op][j] = r
    return judged


def _stratified_pres_subsample(gen, cap_per_role=20):
    """Balanced PRES (RETAIN+UNRELATED) prompt-index subsample for the second judge."""
    out = {}
    for role in PRES:
        npr = len(gen[role]["prompts"])
        if npr == 0:
            continue
        k = min(cap_per_role, npr)
        out[role] = list(range(k))   # deterministic first-k (prompts already shuffled upstream)
    return out


def _degenerate(conts):
    if not conts:
        return False
    bad = 0
    for c in conts:
        cc = c.strip()
        if len(cc) == 0:
            bad += 1
        else:
            toks = cc.split()
            if len(toks) >= 4 and len(set(toks)) <= 2:
                bad += 1
    return bad / max(len(conts), 1) > 0.5


def _curve_dominance(fk, rk, uk, lam, fd, rd, ud, beta):
    """Fraction of achievable KG forget levels where KG has strictly LOWER collateral (and lower unrelated
    perturbation, if available) than the comparator at the SAME forget level (interpolated)."""
    fk = np.asarray(fk); rk = np.asarray(rk); fd = np.asarray(fd); rd = np.asarray(rd)
    levels = [i for i in range(len(fk)) if fk[i] > 1e-4]
    if not levels:
        return {"dominance_fraction": 0.0, "n_levels": 0, "area_between_collateral": 0.0}
    order = np.argsort(fd)
    n_dom = 0; areas = []
    for i in levels:
        f0 = fk[i]; kg_col = rk[i]
        de_col = float(np.interp(f0, fd[order], rd[order]))
        better = kg_col < de_col
        if uk is not None and ud is not None:
            kg_u = np.asarray(uk)[i]
            de_u = float(np.interp(f0, fd[order], np.asarray(ud)[order]))
            better = better and (kg_u < de_u)
        if better:
            n_dom += 1
        areas.append(de_col - kg_col)
    return {"dominance_fraction": float(n_dom / len(levels)), "n_levels": len(levels),
            "area_between_collateral": float(np.mean(areas)),
            "kg_forget_grid": fk.tolist(), "kg_collateral_grid": rk.tolist(),
            "comparator_forget_grid": fd.tolist(), "comparator_collateral_grid": rd.tolist()}


def _dense_localization(fs, csub, fw, cwhl, n=9):
    """u_sub localization validation evaluated where BOTH dense directions ACTUALLY act: at SHARED forget
    targets spanning the overlapping achievable dense forget range (NOT KG's tiny ceiling). Returns the
    fraction of those levels where u_sub's sibling collateral < u_whole's, plus a representative mid point."""
    fs = np.asarray(fs); csub = np.asarray(csub); fw = np.asarray(fw); cwhl = np.asarray(cwhl)
    hi = float(min(fs.max(), fw.max()))
    if hi <= 1e-4:
        return {"frac_sub_lt_whole": 0.0, "n_levels": 0, "targets": [], "sub_collat": [], "whole_collat": [],
                "mid_forget": None, "mid_sub_collat": None, "mid_whole_collat": None}
    targets = np.linspace(hi * 0.1, hi * 0.9, n)
    os_ = np.argsort(fs); ow = np.argsort(fw)
    sc = [float(np.interp(t, fs[os_], csub[os_])) for t in targets]
    wc = [float(np.interp(t, fw[ow], cwhl[ow])) for t in targets]
    frac = float(np.mean([s < w for s, w in zip(sc, wc)]))
    mid = len(targets) // 2
    return {"frac_sub_lt_whole": frac, "n_levels": int(n), "targets": [float(t) for t in targets],
            "sub_collat": sc, "whole_collat": wc, "mid_forget": float(targets[mid]),
            "mid_sub_collat": sc[mid], "mid_whole_collat": wc[mid]}


def _paired_util(judged, gen, opA, opB, roles=PRES):
    """Paired per-prompt (utility, fluency) arrays for opA vs opB over the given roles (skip unjudged)."""
    a, b, fa, fb = [], [], [], []
    for role in roles:
        if role not in judged:
            continue
        npr = len(gen[role]["prompts"])
        ja = judged[role].get(opA, []); jb = judged[role].get(opB, [])
        for j in range(npr):
            ra = ja[j] if j < len(ja) else None
            rb = jb[j] if j < len(jb) else None
            if ra is None or rb is None:
                continue
            a.append(harmonic_mean(ra["fluency"], ra["content_pres"]))
            b.append(harmonic_mean(rb["fluency"], rb["content_pres"]))
            fa.append(ra["fluency"]); fb.append(rb["fluency"])
    return np.array(a), np.array(b), np.array(fa), np.array(fb)


def _mean_forget_quality(judged, gen, op):
    cp = []
    for j in range(len(gen["FORGET"]["prompts"])):
        jj = judged.get("FORGET", {}).get(op, [])
        r = jj[j] if j < len(jj) else None
        if r is not None:
            cp.append(r["content_pres"])
    return (float(np.mean(cp)) if cp else None), len(cp)


def _mi_joint(mi, gen, op, roles=PRES):
    """Model-internal per-prompt joint utility for op = harmonic_mean(2*fluency_proxy, 2*retain_proxy)."""
    out = []
    for role in roles:
        m = mi.get(role, {})
        if not m:
            continue
        npr = len(gen[role]["prompts"])
        klv = m.get(f"kl_{op}"); pplv = m.get(f"ppl_{op}")
        for j in range(npr):
            kl = float(klv[j]) if klv is not None and j < len(klv) else 0.0
            ppl = float(pplv[j]) if pplv is not None and j < len(pplv) else np.nan
            rq = 1.0 / (1.0 + kl)
            fl = 1.0 / (1.0 + math.log1p(ppl)) if np.isfinite(ppl) else 0.3
            out.append(harmonic_mean(2 * fl, 2 * rq))
    return np.array(out)


def _favors_kg(ci):
    return bool(ci is not None and ci.get("excl_0") and ci.get("diff", 0) > 0)


def _joint_and_fork(cs, gen, mi, judged, judged2, second_judge, second_info,
                    collat_KG_SUB, collat_KG_WHOLE, sub_vs_whole_collat, loc_info,
                    dom_kg_vs_sub, dom_kg_vs_whole, scales, matched_target,
                    fk_curve, fs_curve, fw_curve, fu_curve, foot_kg, foot_sub, foot_whl, foot_unit,
                    retain_kl_kg, retain_kl_sub, retain_kl_whl, retain_kl_unit, m7_collat_CI,
                    sub_reaches, max_kg, max_sub, max_whl):
    # ---------- PRIMARY judge joint (KG vs SUB decisive; KG vs WHOLE secondary) ----------
    uK_s, uS_s, fK_s, fS_s = _paired_util(judged, gen, "KG-ABL", "DENSE-SUB-ABL")
    uK_w, uW_w, fK_w, fW_w = _paired_util(judged, gen, "KG-ABL", "DENSE-WHOLE-ABL")
    n_judge = len(uK_s)
    judge_available = n_judge >= max(6, int(0.3 * sum(len(gen[r]["prompts"]) for r in PRES)))

    joint_diff_CI_KG_vs_SUB = paired_bootstrap_diff(uK_s, uS_s) if judge_available else None
    fluency_diff_CI_KG_vs_SUB = paired_bootstrap_diff(fK_s, fS_s) if judge_available else None
    joint_diff_CI_KG_vs_WHOLE = paired_bootstrap_diff(uK_w, uW_w) if len(uK_w) >= 6 else None

    # ---------- SECOND judge joint (subsample), for KG-vs-SUB only ----------
    joint_diff_CI_KG_vs_SUB_2 = None; kappa = None; pear = None; spear = None; n_judge2 = 0
    if judged2 is not None:
        uK2, uS2, _, _ = _paired_util(judged2, gen, "KG-ABL", "DENSE-SUB-ABL")
        n_judge2 = len(uK2)
        if n_judge2 >= 6:
            joint_diff_CI_KG_vs_SUB_2 = paired_bootstrap_diff(uK2, uS2)
        kappa, pear, spear = _judge_agreement(judged, judged2, gen,
                                              ["KG-ABL", "DENSE-SUB-ABL", "DENSE-WHOLE-ABL"])

    # ---------- model-internal joint (fallback / corroboration) ----------
    mik = _mi_joint(mi, gen, "KG-ABL"); mis = _mi_joint(mi, gen, "DENSE-SUB-ABL")
    miw = _mi_joint(mi, gen, "DENSE-WHOLE-ABL")
    mi_joint_KG_vs_SUB = paired_bootstrap_diff(mik, mis)
    mi_joint_KG_vs_WHOLE = paired_bootstrap_diff(mik, miw)
    mi_collat_KG_vs_SUB = paired_bootstrap_diff(retain_kl_sub, retain_kl_kg)  # same as collat_KG_SUB (genset n high)

    # ---------- choose primary basis ----------
    if judge_available:
        primary_joint = joint_diff_CI_KG_vs_SUB; primary_basis = "llm_judge"
    else:
        primary_joint = mi_joint_KG_vs_SUB; primary_basis = "model_internal_fallback"

    # ---------- FORK VERDICT (decided on KG vs SUB) ----------
    p_excl0 = bool(primary_joint is not None and primary_joint.get("excl_0"))
    p_favors_kg = _favors_kg(primary_joint)
    p_favors_sub = bool(p_excl0 and not p_favors_kg)
    second_available = joint_diff_CI_KG_vs_SUB_2 is not None
    s_favors_kg = _favors_kg(joint_diff_CI_KG_vs_SUB_2) if second_available else None

    judge_robustness_unverified = False
    judge_sensitivity_flag = False
    if p_excl0 and p_favors_kg:
        if second_available:
            if s_favors_kg:
                fork = "KG_BEATS_USUB"
            else:
                fork = "KG_MATCHES_USUB_LABEL_FREE"; judge_sensitivity_flag = True
        else:
            fork = "KG_BEATS_USUB"; judge_robustness_unverified = True
    elif not p_excl0:
        fork = "KG_MATCHES_USUB_LABEL_FREE"
    else:  # excl 0 and favors SUB
        fork = "KG_LOSES_TO_USUB"

    # ---------- judged forget confirmation (matched at generation level) ----------
    jfq_kg, n_fk = _mean_forget_quality(judged, gen, "KG-ABL")
    jfq_sub, n_fs = _mean_forget_quality(judged, gen, "DENSE-SUB-ABL")
    jfq_whl, n_fw = _mean_forget_quality(judged, gen, "DENSE-WHOLE-ABL")

    # ---------- M7 unit-vs-single joint (judge) ----------
    m7 = None
    if "KG-ABL-UNIT" in (judged.get("RETAIN", {}) or {}):
        uS_single, uS_unit, _, _ = _paired_util(judged, gen, "KG-ABL", "KG-ABL-UNIT")
        m7 = {
            "unit_members": cs.kg_unit, "scale_unit": scales.get("KG-ABL-UNIT"),
            "n_paired_joint": len(uS_single),
            "joint_diff_CI_single_minus_unit": paired_bootstrap_diff(uS_single, uS_unit) if len(uS_single) >= 6 else None,
            "collateral_diff_CI_unit_minus_single": m7_collat_CI,
            "retain_kl_single_mean": float(retain_kl_kg.mean()),
            "retain_kl_unit_mean": float(retain_kl_unit.mean()) if retain_kl_unit is not None else None,
            "single_joint_utility_mean": float(np.mean(uS_single)) if len(uS_single) else None,
            "unit_joint_utility_mean": float(np.mean(uS_unit)) if len(uS_unit) else None,
            "win_traces_to_single_absorber": bool(
                (m7_collat_CI is not None and m7_collat_CI.get("diff", 0) > 0) or
                (retain_kl_unit is not None and retain_kl_unit.mean() >= retain_kl_kg.mean())),
        }

    logger.info(f"{el()} FORK {cs.case_id}: {fork} (basis={primary_basis}; primary_excl0={p_excl0} "
                f"favors_kg={p_favors_kg}; second={'NA' if not second_available else s_favors_kg}; "
                f"localizes_better={loc_info['localizes_better']})")

    return {
        "family": cs.family, "target_subcontext": cs.X, "absorber_latent": int(cs.absorber),
        "parent_anchor": int(cs.anchor), "absorber_precision": cs.absorber_precision, "regime": cs.regime,
        "probe_train_auc": cs.probe.train_auc, "probe_cos_with_diffmean": cs.probe.cos_probe_dmu,
        "u_sub_meta": cs.u_sub_meta,
        "firing_jaccard_with_parent": cs.firing_jaccard,
        "firing_jaccard_aggregate_parent": getattr(cs, "firing_jaccard_aggregate", None),
        "parent_recall_hole": cs.parent_recall_hole,
        "matched_target_forget_kl": float(matched_target),
        "max_forget_kg": float(max_kg), "max_forget_sub": float(max_sub), "max_forget_whole": float(max_whl),
        "sub_reaches_matched_target": bool(sub_reaches),
        "scale_kg_lambda": float(scales["KG-ABL"]), "scale_sub_beta": float(scales["DENSE-SUB-ABL"]),
        "scale_whole_beta": float(scales["DENSE-WHOLE-ABL"]),
        "forget_kg_curve": fk_curve.tolist(), "forget_sub_curve": fs_curve.tolist(),
        "forget_whole_curve": fw_curve.tolist(),
        "forget_kg_footprints": foot_kg, "forget_sub_footprints": foot_sub, "forget_whole_footprints": foot_whl,
        "lam_grid": LAM_GRID, "beta_grid": BETA_GRID,
        "n_forget_gen": len(gen["FORGET"]["prompts"]),
        "n_retain_collateral": len(retain_kl_kg),
        "retain_collateral_kl_kg_mean": float(retain_kl_kg.mean()),
        "retain_collateral_kl_sub_mean": float(retain_kl_sub.mean()),
        "retain_collateral_kl_whole_mean": float(retain_kl_whl.mean()),
        # DECISIVE
        "collateral_diff_CI_KG_vs_SUB": collat_KG_SUB,
        "joint_diff_CI_KG_vs_SUB": joint_diff_CI_KG_vs_SUB,
        "fluency_diff_CI_KG_vs_SUB": fluency_diff_CI_KG_vs_SUB,
        "curve_dominance_KG_vs_SUB": dom_kg_vs_sub,
        # SECONDARY (clearly labeled)
        "collateral_diff_CI_KG_vs_WHOLE_secondary": collat_KG_WHOLE,
        "joint_diff_CI_KG_vs_WHOLE_secondary": joint_diff_CI_KG_vs_WHOLE,
        "curve_dominance_KG_vs_WHOLE_secondary": dom_kg_vs_whole,
        # u_sub localization validation
        "u_sub_localizes_better_than_whole": loc_info["localizes_better"],
        "u_sub_localizes_better_at_matched_point": loc_info["localizes_better_at_matched"],
        "dense_localization_curve": loc_info["dense_localization"],
        "sub_vs_whole_collateral_CI": sub_vs_whole_collat,
        # judge bookkeeping
        "judge_available": judge_available, "n_judged_preservation_pairs": int(n_judge),
        "primary_outcome_basis": primary_basis,
        "kg_joint_utility_mean": float(np.mean(uK_s)) if len(uK_s) else None,
        "sub_joint_utility_mean": float(np.mean(uS_s)) if len(uS_s) else None,
        "whole_joint_utility_mean": float(np.mean(uW_w)) if len(uW_w) else None,
        "judged_forget_quality": {"kg": jfq_kg, "sub": jfq_sub, "whole": jfq_whl,
                                  "n_kg": n_fk, "n_sub": n_fs, "n_whole": n_fw},
        # second judge (M6)
        "second_judge": {**second_info, "n_paired": int(n_judge2),
                         "joint_diff_CI_KG_vs_SUB": joint_diff_CI_KG_vs_SUB_2,
                         "cohen_kappa_vs_primary": kappa, "pearson_util": pear, "spearman_util": spear},
        "judge_robustness_unverified": bool(judge_robustness_unverified),
        "judge_sensitivity_downgrade": bool(judge_sensitivity_flag),
        # model-internal corroboration
        "model_internal_joint": {
            "joint_diff_CI_KG_vs_SUB": mi_joint_KG_vs_SUB,
            "joint_diff_CI_KG_vs_WHOLE": mi_joint_KG_vs_WHOLE,
            "collateral_diff_CI_KG_vs_SUB": mi_collat_KG_vs_SUB,
            "kg_mi_joint_mean": float(np.mean(mik)) if len(mik) else None,
            "sub_mi_joint_mean": float(np.mean(mis)) if len(mis) else None,
            "whole_mi_joint_mean": float(np.mean(miw)) if len(miw) else None},
        # M7
        "m7_unit_vs_single": m7,
        "fork_verdict": fork,
    }


def _judge_agreement(judged, judged2, gen, ops):
    """Cohen kappa on discretized utility + Pearson/Spearman of per-prompt utility, on overlapping
    (role,op,j) judged by BOTH judges."""
    from sklearn.metrics import cohen_kappa_score
    from scipy.stats import pearsonr, spearmanr
    a, b = [], []
    for role in judged2:
        npr = len(gen[role]["prompts"])
        for op in ops:
            j1 = judged.get(role, {}).get(op, []); j2 = judged2.get(role, {}).get(op, [])
            for j in range(npr):
                r1 = j1[j] if j < len(j1) else None
                r2 = j2[j] if j < len(j2) else None
                if r1 is None or r2 is None:
                    continue
                a.append(harmonic_mean(r1["fluency"], r1["content_pres"]))
                b.append(harmonic_mean(r2["fluency"], r2["content_pres"]))
    if len(a) < 4:
        return None, None, None
    a = np.array(a); b = np.array(b)
    def disc(x):
        return np.where(x < 0.67, 0, np.where(x <= 1.33, 1, 2))
    try:
        kappa = float(cohen_kappa_score(disc(a), disc(b)))
    except Exception:
        kappa = None
    try:
        pear = float(pearsonr(a, b)[0]) if np.std(a) > 0 and np.std(b) > 0 else None
    except Exception:
        pear = None
    try:
        spear = float(spearmanr(a, b)[0]) if np.std(a) > 0 and np.std(b) > 0 else None
    except Exception:
        spear = None
    return kappa, pear, spear


# =========================================================================== M6 human-proxy spot-check
HUMAN_PROXY = {
    "taxonomic_georgia": {
        "forget_ref": [("Georgia is a country in", "the Caucasus / Europe / Asia")],
        "sibling_ref": [("France is a country in", "Europe"), ("The capital of Germany is", "Berlin"),
                        ("Spain is a country located in", "Europe"), ("Italy is a country in", "Europe"),
                        ("The capital of Japan is", "Tokyo"), ("Brazil is a country in", "South America"),
                        ("Canada is a country in", "North America"), ("The capital of Russia is", "Moscow")],
    },
    "first_letter_large": {
        "forget_ref": [("large starts with the letter", "L")],
        "sibling_ref": [("lemon starts with the letter", "L"), ("london starts with the letter", "L"),
                        ("level starts with the letter", "L"), ("little starts with the letter", "L"),
                        ("lion starts with the letter", "L"), ("light starts with the letter", "L"),
                        ("local starts with the letter", "L"), ("line starts with the letter", "L")],
    },
}


def run_human_proxy(mb, sae, cs, s_kg, s_whl):
    """Deterministic ($0) check: KG-ABL preserves SIBLING continuations (close to NOOP) while DENSE-WHOLE
    corrupts them. Returns a dict with per-prompt similarity + pass flags."""
    spec = HUMAN_PROXY.get(cs.case_id)
    if spec is None:
        return None
    sib = spec["sibling_ref"]
    prompts = [p for p, _ in sib]
    noop = generate_under_edit(mb, sae, prompts, kind=None)
    kg = generate_under_edit(mb, sae, prompts, kind="abl_latent", l=cs.absorber, scale=s_kg)
    whl = generate_under_edit(mb, sae, prompts, kind="erase_dir", u=cs.u, scale=s_whl)

    def ratio(a, b):
        return float(difflib.SequenceMatcher(None, a.strip().lower(), b.strip().lower()).ratio())

    rows = []
    kg_pres_flags, whole_corrupt_flags = [], []
    for j, (p, expect) in enumerate(sib):
        r_kg = ratio(kg[j], noop[j]); r_wh = ratio(whl[j], noop[j])
        # KG preserves sibling: continuation close to NOOP OR still contains the expected token
        kg_pres = bool(r_kg >= 0.6 or expect.split("/")[0].strip().lower() in kg[j].lower())
        # WHOLE corrupts sibling: noticeably less similar to NOOP than KG is
        whole_corrupt = bool(r_wh < r_kg - 0.1 or r_wh < 0.5)
        kg_pres_flags.append(kg_pres); whole_corrupt_flags.append(whole_corrupt)
        rows.append({"prompt": p, "expect": expect, "noop": noop[j][:80], "kg": kg[j][:80],
                     "whole": whl[j][:80], "kg_noop_ratio": round(r_kg, 3),
                     "whole_noop_ratio": round(r_wh, 3), "kg_preserves": kg_pres,
                     "whole_corrupts": whole_corrupt})
    res = {"n": len(sib), "kg_preserve_rate": float(np.mean(kg_pres_flags)) if kg_pres_flags else 0.0,
           "whole_corrupt_rate": float(np.mean(whole_corrupt_flags)) if whole_corrupt_flags else 0.0,
           "passed": bool((np.mean(kg_pres_flags) >= 0.6) and (np.mean(whole_corrupt_flags) >= 0.5)),
           "rows": rows}
    logger.info(f"{el()} HUMAN-PROXY {cs.case_id}: kg_preserve={res['kg_preserve_rate']:.2f} "
                f"whole_corrupt={res['whole_corrupt_rate']:.2f} passed={res['passed']}")
    return res


# =========================================================================== gating
def gating_check(torch, sae, mb):
    tax_rows = load_taxonomic()
    gate_rows = [r for r in tax_rows if r["metadata_row_type"] == "corpus"][:64]
    layer_idx, fvu = mb.determine_layer_idx(gate_rows, sae)
    _, resid_g, align_g = mb.encode_rows(gate_rows, sae)
    hb = torch.tensor(resid_g.astype(np.float32), device=DEVICE)
    z = sae.encode(hb); hr = sae.decode(z)
    cos = float(torch.nn.functional.cosine_similarity(hb, hr, dim=-1).mean())
    l0 = float((z > 0).sum(1).float().mean())
    Rnorm = mb.mean_resid_norm(NEUTRAL_TEXT)
    gating = {"pass": bool(cos > 0.9), "cosine": cos, "L0": l0, "align": align_g,
              "layer_idx": int(layer_idx), "fvu_by_idx": {str(k): v for k, v in fvu.items()}, "Rnorm": Rnorm}
    logger.info(f"{el()} GATING cosine={cos:.4f} L0={l0:.1f} layer_idx={layer_idx} Rnorm={Rnorm:.1f}")
    assert cos > 0.85, f"gating cosine {cos:.4f} too low — SAE/layer mapping wrong"
    del hb, z, hr, resid_g
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return gating, Rnorm, tax_rows


# =========================================================================== SMOKE
def run_smoke(torch, sae, mb, canon, gating, tax_rows, out):
    logger.info(f"{el()} ===== SMOKE =====")
    corp = [r for r in tax_rows if r["metadata_row_type"] == "corpus"]
    geo = [r for r in corp if r.get("metadata_sub_context") == "Georgia" and r["output"] == "positive"][:4]
    fra = [r for r in corp if r.get("metadata_sub_context") == "France" and r["output"] == "positive"][:4]
    neg = [r for r in corp if r["output"] == "negative"][:6]
    rows_s = geo + fra + neg
    ng, nf = len(geo), len(fra)
    _, resid_s, _ = mb.encode_rows(rows_s, sae)
    z = sae.encode(torch.tensor(resid_s.astype(np.float32), device=DEVICE))
    zg = float(z[:ng, 16009].mean()); zf = float(z[ng:ng + nf, 16009].mean())
    locality_ok = bool(zg > zf)
    # WHOLE-parent probe: country (geo+fra) vs NON-country negatives -> the "is-a-country" direction
    probe = ParentProbe(torch, resid_s[:ng + nf].astype(np.float32), resid_s[ng + nf:].astype(np.float32))
    # u_sub: Georgia(pos) vs France(sibling) -> a GENUINELY DIFFERENT contrast (Georgia-not-France)
    pos_mask = np.zeros(len(rows_s), bool); pos_mask[:ng] = True
    sib_mask = np.zeros(len(rows_s), bool); sib_mask[ng:ng + nf] = True
    u_sub_t, u_sub_meta = build_u_sub(torch, resid_s, pos_mask, sib_mask, probe.d_mu)
    cos_sw = u_sub_meta["cos_with_whole_parent"]
    norm_ok = abs(float(np.linalg.norm(u_sub_t.cpu().numpy())) - 1.0) < 1e-3
    prompt = _prefix_before_span(geo[0]["input"], geo[0].get("_span"))
    base_c = generate_under_edit(mb, sae, [prompt], kind=None)[0]
    kg_c = generate_under_edit(mb, sae, [prompt], kind="abl_latent", l=16009, scale=2.0)[0]
    sub_c = generate_under_edit(mb, sae, [prompt], kind="erase_dir", u=u_sub_t, scale=2.0)[0]
    whl_c = generate_under_edit(mb, sae, [prompt], kind="erase_dir", u=probe.u_t, scale=2.0)[0]
    # unit ablation (list of latents) sanity
    unit = sorted(set(int(m) for m in canon["taxonomic"]["k_track_unit"]) | {16009})
    unit_c = generate_under_edit(mb, sae, [prompt], kind="abl_latent", l=unit, scale=1.0)[0]
    bd = base_distributions(mb, NEUTRAL_TEXT[:6])
    kg_foot = side_effects(mb, sae, NEUTRAL_TEXT[:6], *bd, "abl_latent", l=16009, scale=1.0)["token_footprint"]
    sub_foot = side_effects(mb, sae, NEUTRAL_TEXT[:6], *bd, "erase_dir", u=u_sub_t, scale=1.0)["token_footprint"]
    gen_diff = bool(kg_c != base_c or sub_c != base_c or whl_c != base_c)
    sub_distinct = bool(sub_c != base_c and sub_c != whl_c)
    logger.info(f"{el()} SMOKE gen base='{base_c[:50]}' kg='{kg_c[:50]}' sub='{sub_c[:50]}' whole='{whl_c[:50]}'")
    logger.info(f"{el()} SMOKE u_sub norm_ok={norm_ok} cos_with_whole={cos_sw:.3f} sub_distinct={sub_distinct} "
                f"unit_gen='{unit_c[:50]}'")
    logger.info(f"{el()} SMOKE footprint KG={kg_foot:.5f} SUB={sub_foot:.5f}")
    jr = jr2 = None
    if os.environ.get("OPENROUTER_API_KEY"):
        jr = judge_call({"role": "RETAIN", "X": "Georgia", "prompt": prompt,
                         "base_cont": base_c[:300], "edit_cont": sub_c[:300]}, PRIMARY_JUDGE)
        sj = resolve_second_judge()
        if sj is not None:
            jr2 = judge_call({"role": "RETAIN", "X": "Georgia", "prompt": prompt,
                              "base_cont": base_c[:300], "edit_cont": whl_c[:300]}, sj)
    out["metadata"]["smoke"] = {
        "z_georgia_16009": zg, "z_france_16009": zf, "token_locality_ok": locality_ok,
        "u_sub_norm_ok": norm_ok, "u_sub_cos_with_whole": cos_sw, "u_sub_abs_cos_lt_1": bool(abs(cos_sw) < 1.0),
        "u_sub_n_pos": u_sub_meta["n_pos"], "u_sub_n_sib": u_sub_meta["n_sib"],
        "gen_base": base_c[:120], "gen_kg": kg_c[:120], "gen_sub": sub_c[:120], "gen_whole": whl_c[:120],
        "gen_unit": unit_c[:120], "gen_diff": gen_diff, "sub_distinct_from_noop_and_whole": sub_distinct,
        "kg_footprint": kg_foot, "sub_footprint": sub_foot, "footprint_kg_lt_sub": bool(kg_foot < sub_foot),
        "judge_result_primary": jr, "judge_result_second": jr2, "judge_spent_usd": SPENT["usd"],
        "judge_ok": bool(jr is not None)}
    out["datasets"] = [{"dataset": "smoke", "examples": [{"input": "smoke", "output": "ok",
                       "predict_kg_abl": kg_c[:80] or "EMPTY", "predict_dense_sub_abl": sub_c[:80] or "EMPTY"}]}]
    assert gating["cosine"] > 0.85, "gating failed"
    assert locality_ok, "token locality failed (16009 not Georgia-specific)"
    assert gen_diff, "edit hooks did not change generation"
    assert norm_ok, "u_sub not unit norm"
    assert abs(cos_sw) < 1.0, "u_sub not distinct from whole-parent direction"
    assert sub_distinct, "DENSE-SUB generation not distinct from NOOP and DENSE-WHOLE"
    assert kg_foot < sub_foot, "KG footprint not < SUB footprint"
    if os.environ.get("OPENROUTER_API_KEY"):
        assert jr is not None and jr["fluency"] in (0, 1, 2), "primary judge call/parse failed"
        assert SPENT["usd"] < 0.02, f"smoke judge cost too high ${SPENT['usd']}"
    logger.info(f"{el()} SMOKE PASS")


# =========================================================================== output assembly
def _s(x):
    """Coerce any value to a non-empty string for predict_* fields (schema requires string)."""
    if x is None:
        return "NA"
    s = str(x)
    return s if s.strip() else "NA"


def assemble_outputs(out, case_results):
    per_prompt = []
    per_case = []
    for (res, gen, mi, judged, judged2) in case_results:
        cid = res["case_id"]
        for role in ("FORGET", "RETAIN", "UNRELATED"):
            g = gen[role]; m = mi.get(role, {})
            j2 = judged2 if judged2 is not None else {}
            for j, p in enumerate(g["prompts"]):
                def js(jd, op):
                    r = jd.get(role, {}).get(op, []) if jd else []
                    return r[j] if (r and j < len(r)) else None
                jk = js(judged, "KG-ABL"); jsub = js(judged, "DENSE-SUB-ABL")
                jwh = js(judged, "DENSE-WHOLE-ABL"); jrnd = js(judged, "RAND")
                jk2 = js(j2, "KG-ABL"); jsub2 = js(j2, "DENSE-SUB-ABL")
                row = {
                    "input": f"[{res['family']}|{role}|forget='{res['target_subcontext']}'] {p[:200]}",
                    "output": role,
                    "predict_kg_abl": _s(g["KG-ABL"][j][:160] or "EMPTY"),
                    "predict_dense_sub_abl": _s(g["DENSE-SUB-ABL"][j][:160] or "EMPTY"),
                    "predict_dense_whole_abl": _s(g["DENSE-WHOLE-ABL"][j][:160] or "EMPTY"),
                    "predict_rand": _s((g.get("RAND") or [""] * (j + 1))[j][:160] or "EMPTY"),
                    "predict_noop": _s(g["NOOP"][j][:160] or "EMPTY"),
                    "metadata_case": cid, "metadata_role": role,
                    "metadata_absorber_latent": int(res["absorber_latent"]),
                    "metadata_regime": res["regime"],
                    "metadata_fluency_kg": (jk["fluency"] if jk else None),
                    "metadata_fluency_sub": (jsub["fluency"] if jsub else None),
                    "metadata_fluency_whole": (jwh["fluency"] if jwh else None),
                    "metadata_content_pres_kg": (jk["content_pres"] if jk else None),
                    "metadata_content_pres_sub": (jsub["content_pres"] if jsub else None),
                    "metadata_content_pres_whole": (jwh["content_pres"] if jwh else None),
                    "metadata_utility_kg": (round(harmonic_mean(jk["fluency"], jk["content_pres"]), 4) if jk else None),
                    "metadata_utility_sub": (round(harmonic_mean(jsub["fluency"], jsub["content_pres"]), 4) if jsub else None),
                    "metadata_utility_whole": (round(harmonic_mean(jwh["fluency"], jwh["content_pres"]), 4) if jwh else None),
                    "metadata_utility_rand": (round(harmonic_mean(jrnd["fluency"], jrnd["content_pres"]), 4) if jrnd else None),
                    "metadata_utility_kg_judge2": (round(harmonic_mean(jk2["fluency"], jk2["content_pres"]), 4) if jk2 else None),
                    "metadata_utility_sub_judge2": (round(harmonic_mean(jsub2["fluency"], jsub2["content_pres"]), 4) if jsub2 else None),
                }
                if "KG-ABL-UNIT" in g:
                    row["predict_kg_abl_unit"] = _s(g["KG-ABL-UNIT"][j][:160] or "EMPTY")
                if m:
                    row["metadata_mi_lastkl_kg"] = round(float(m["kl_KG-ABL"][j]), 6) if "kl_KG-ABL" in m else None
                    row["metadata_mi_lastkl_sub"] = round(float(m["kl_DENSE-SUB-ABL"][j]), 6) if "kl_DENSE-SUB-ABL" in m else None
                    row["metadata_mi_lastkl_whole"] = round(float(m["kl_DENSE-WHOLE-ABL"][j]), 6) if "kl_DENSE-WHOLE-ABL" in m else None
                    if "ppl_KG-ABL" in m:
                        row["metadata_mi_contppl_kg"] = (round(float(m["ppl_KG-ABL"][j]), 3) if np.isfinite(m["ppl_KG-ABL"][j]) else None)
                    if "ppl_DENSE-SUB-ABL" in m:
                        row["metadata_mi_contppl_sub"] = (round(float(m["ppl_DENSE-SUB-ABL"][j]), 3) if np.isfinite(m["ppl_DENSE-SUB-ABL"][j]) else None)
                per_prompt.append(row)
        # DS2: one row per case
        regime = res["regime"]
        expected = "WIN_EXPECTED" if regime == "absorption" else "LOSS_EXPECTED"
        cj = res.get("collateral_diff_CI_KG_vs_SUB") or {}
        jj = res.get("joint_diff_CI_KG_vs_SUB") or {}
        sj = (res.get("second_judge") or {}).get("joint_diff_CI_KG_vs_SUB") or {}
        m7 = res.get("m7_unit_vs_single")
        per_case.append({
            "input": (f"{res['family']} | selectively UNLEARN sub-context '{res['target_subcontext']}' by "
                      f"ablating KG-named absorber {res['absorber_latent']} ({regime}); DECISIVE KG-ABL vs "
                      f"DENSE-SUB-ABL (sub-context diff-of-means, baseline) at MATCHED forget on a joint "
                      f"retain-quality x fluency outcome"),
            "output": expected,
            "predict_kg_abl": _s(res["fork_verdict"]),
            "predict_dense_sub_abl": _s(f"joint_util={res.get('sub_joint_utility_mean')}"),
            "predict_dense_whole_abl": _s(f"joint_util={res.get('whole_joint_utility_mean')}"),
            "predict_model_internal": _s(res["model_internal_joint"]["joint_diff_CI_KG_vs_SUB"].get("diff")),
            "metadata_case": res["case_id"], "metadata_regime": regime,
            "metadata_fork_verdict": res["fork_verdict"],
            "metadata_scale_kg_lambda": round(res["scale_kg_lambda"], 4),
            "metadata_scale_sub_beta": round(res["scale_sub_beta"], 4),
            "metadata_scale_whole_beta": round(res["scale_whole_beta"], 4),
            "metadata_matched_target_forget_kl": round(res["matched_target_forget_kl"], 6),
            "metadata_collateral_KGvsSUB_diff": cj.get("diff"),
            "metadata_collateral_KGvsSUB_ci_lo": cj.get("ci_lo"), "metadata_collateral_KGvsSUB_ci_hi": cj.get("ci_hi"),
            "metadata_collateral_KGvsSUB_excl0": cj.get("excl_0"),
            "metadata_joint_KGvsSUB_diff": jj.get("diff"), "metadata_joint_KGvsSUB_ci_lo": jj.get("ci_lo"),
            "metadata_joint_KGvsSUB_ci_hi": jj.get("ci_hi"), "metadata_joint_KGvsSUB_excl0": jj.get("excl_0"),
            "metadata_joint_KGvsSUB_judge2_diff": sj.get("diff"), "metadata_joint_KGvsSUB_judge2_excl0": sj.get("excl_0"),
            "metadata_kg_joint_utility": res.get("kg_joint_utility_mean"),
            "metadata_sub_joint_utility": res.get("sub_joint_utility_mean"),
            "metadata_whole_joint_utility": res.get("whole_joint_utility_mean"),
            "metadata_u_sub_localizes_better_than_whole": res["u_sub_localizes_better_than_whole"],
            "metadata_u_sub_localizes_frac_sub_lt_whole": (res.get("dense_localization_curve") or {}).get("frac_sub_lt_whole"),
            "metadata_u_sub_localizes_at_matched_point": res.get("u_sub_localizes_better_at_matched_point"),
            "metadata_u_sub_probe_auc": res["u_sub_meta"].get("sub_probe_auc"),
            "metadata_u_sub_cos_with_whole": res["u_sub_meta"].get("cos_with_whole_parent"),
            "metadata_u_sub_underpowered": res["u_sub_meta"].get("underpowered"),
            "metadata_curve_dominance_KGvsSUB": res["curve_dominance_KG_vs_SUB"]["dominance_fraction"],
            "metadata_firing_jaccard_absorber": res["firing_jaccard_with_parent"],
            "metadata_firing_jaccard_aggregate": res["firing_jaccard_aggregate_parent"],
            "metadata_parent_recall_hole": res["parent_recall_hole"],
            "metadata_primary_basis": res["primary_outcome_basis"],
            "metadata_cohen_kappa_judges": (res.get("second_judge") or {}).get("cohen_kappa_vs_primary"),
            "metadata_m7_win_traces_to_single": (m7.get("win_traces_to_single_absorber") if m7 else None),
        })
    if not per_prompt:
        per_prompt = [{"input": "none", "output": "NONE", "predict_kg_abl": "NONE"}]
    if not per_case:
        per_case = [{"input": "none", "output": "NONE", "predict_kg_abl": "NONE"}]
    out["datasets"] = [
        {"dataset": "unlearn_per_prompt", "examples": per_prompt},
        {"dataset": "kg_vs_dense_per_case", "examples": per_case},
    ]


# =========================================================================== honest negatives
def _mi_corroborates(r):
    """Does the $0 model-internal joint CI agree with the LLM-judge fork direction (KG vs SUB)?"""
    mi = (r.get("model_internal_joint") or {}).get("joint_diff_CI_KG_vs_SUB") or {}
    fork = r.get("fork_verdict")
    if fork == "KG_BEATS_USUB":
        return bool(mi.get("excl_0") and mi.get("diff", 0) > 0)
    if fork == "KG_LOSES_TO_USUB":
        return bool(mi.get("excl_0") and mi.get("diff", 0) < 0)
    return bool(mi and not mi.get("excl_0"))   # MATCHES -> MI corroborates if it also includes 0


def build_honest_negatives(summaries, second_judge_available):
    """Derive the honest-negatives list from the per-case results (mutates each r to add
    mi_corroborates_fork). Pure post-processing — callable on cached results without re-running."""
    honest = [
        "HEADLINE REFRAMED: 'beats WHOLE-parent erasure' is RETIRED as the headline — the decisive comparator is "
        "now DENSE-SUB-ABL (a sub-context-labeled diff-of-means). WHOLE-parent erasure is reported only as a "
        "secondary reference.",
        "DELETED FRAMING: the claim that 'a single dense hyperplane structurally cannot localize' / 'erasing "
        "is-a-country removes all countries' is FALSE and removed — u_sub is itself a single dense direction that "
        "localizes (sub-probe AUC ~1.0); KG-ABL is compared against it. KG's surgical edge is SPARSE-FIRING GATING "
        "(token footprint -> 0 for absorption), NOT the dense direction failing to localize.",
        "The win (where present) traces to the SINGLE discovered absorber, not to multi-member grouping (M7): the "
        "two-track algorithm is the label-free DISCOVERY PROCEDURE that surfaces the precise single absorber.",
        "Absorption regime is NARROW (documented ~only for these structured sub-contexts); numeric sub-contexts "
        "sit below the SAE-reconstruction gate (taxonomic cosine ~0.876 region) and are out of scope here.",
        "REGIME SPLIT (mechanism, reported INDEPENDENTLY of the KG-vs-u_sub joint verdict): absorption sub-contexts "
        "give a CLEAN surgical KG edit (token-footprint ~0.01-0.03, firing-Jaccard ~0.002-0.04, high parent "
        "recall-hole); co-firing sub-contexts (toxicity insult; US under M5) do NOT — the single latent fires on a "
        "large token fraction (footprint up to ~0.17) and co-fires with the parent (Jaccard ~0.88, no recall-hole). "
        "A KG-vs-u_sub joint 'win' in a co-firing case is therefore NOT a surgical win.",
    ]
    if not second_judge_available:
        honest.append("SECOND JUDGE UNAVAILABLE: M6 judge-robustness is UNVERIFIED — any KG_BEATS_USUB rests on the "
                      "single primary judge and is flagged judge_robustness_unverified=true.")
    for r in summaries:
        v = r["fork_verdict"]; cid = r["case_id"]; reg = r.get("regime")
        r["mi_corroborates_fork"] = _mi_corroborates(r)
        dl = r.get("dense_localization_curve") or {}
        foot = max(r.get("forget_kg_footprints") or [0.0])
        if v == "KG_LOSES_TO_USUB":
            honest.append(f"{cid}: KG_LOSES_TO_USUB — declared clean NEGATIVE: the discovered single absorber does "
                          f"NOT clear the stronger sub-context-labeled dense bar on the joint outcome (joint CI "
                          f"excludes 0 favoring u_sub). Reported, not hidden.")
        elif v == "KG_MATCHES_USUB_LABEL_FREE":
            honest.append(f"{cid}: KG_MATCHES_USUB_LABEL_FREE — KG-ABL MATCHES u_sub (joint CI includes 0) WITHOUT "
                          f"needing the sub-context partition/labels that u_sub requires (a label-free parity win, "
                          f"not a strict beat).")
        elif v == "KG_BEATS_USUB" and r.get("judge_robustness_unverified"):
            honest.append(f"{cid}: KG_BEATS_USUB but on a SINGLE judge (second-judge CI unavailable) — robustness "
                          f"unverified.")
        if reg == "co-firing":
            extra = ""
            if cid == "taxonomic_us":
                extra = (f" M5 ROUTER-FALSE-NEGATIVE: the per-absorber firing-Jaccard "
                         f"{round(r['firing_jaccard_with_parent'], 4)} (and aggregate "
                         f"{round(r['firing_jaccard_aggregate_parent'], 4)}) are LOW and would naively suggest "
                         f"absorption, but the parent RECALL-HOLE {round(r['parent_recall_hole'], 3)} (< 0.5) "
                         f"correctly flags co-firing: the parent detector already covers US, leaving no clean hole "
                         f"for a single absorber to fill (hence reclassified out of the absorption win-set).")
            corrob = ("the $0 MODEL-INTERNAL joint does NOT corroborate it (CI includes 0) and u_sub itself fails to "
                      "localize in co-firing, so this is a WEAK judge-only edge at a tiny KG-limited matched forget — "
                      "NOT a surgical win"
                      if (v == "KG_BEATS_USUB" and not r["mi_corroborates_fork"])
                      else "consistent across the LLM-judge and the $0 model-internal joint"
                      if r["mi_corroborates_fork"] else "reported exactly as computed")
            surg_txt = ("the single latent fires on a LARGE token fraction so the edit is NOT a clean surgical "
                        "handle (co-firing MECHANISM prediction HOLDS)" if foot > 0.05 else
                        "the absorber's token-footprint is actually LOW (surgical-looking): this is a ROUTER "
                        "FALSE-NEGATIVE — co-firing is flagged by the SMALL parent recall-hole, not by footprint")
            honest.append(f"{cid} (CO-FIRING: firing-Jaccard {round(r['firing_jaccard_with_parent'], 4)}, parent "
                          f"recall-hole {round(r['parent_recall_hole'], 3)}, KG token-footprint {foot:.3f}) — "
                          f"{surg_txt}.{extra} Its KG-vs-u_sub fork is {v}; {corrob}. It is NOT counted toward the "
                          f"absorption M1' gate.")
        if r["u_sub_meta"].get("underpowered"):
            honest.append(f"{cid}: u_sub UNDERPOWERED (n_pos={r['u_sub_meta']['n_pos']}, "
                          f"n_sib={r['u_sub_meta']['n_sib']} < {MIN_SUB}); KG-vs-SUB for this case is descriptive-only.")
        if reg == "absorption" and v == "KG_BEATS_USUB" and not r["mi_corroborates_fork"]:
            honest.append(f"{cid}: the KG_BEATS_USUB verdict rests on the pre-registered LLM-judge joint (BOTH the "
                          f"primary and the 2nd-family judge CIs exclude 0); the noisier $0 model-internal joint "
                          f"(continuation-PPL + retain-KL) is INCONCLUSIVE here (CI includes 0) — reported, not hidden.")
        if reg == "absorption" and not r["u_sub_localizes_better_than_whole"]:
            honest.append(f"{cid}: over the achievable dense forget range u_sub did NOT localize better than "
                          f"whole-parent (frac_sub<whole={dl.get('frac_sub_lt_whole')}); the sub-context direction "
                          f"is not cleanly separable here, weakening the 'stronger baseline' framing for this case "
                          f"(recorded; the KG-vs-SUB decisive joint outcome still stands).")
    return honest


# =========================================================================== MAIN
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default="taxonomic_georgia,first_letter_large,taxonomic_us,toxicity_insult")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--cap", type=int, default=0)
    ap.add_argument("--gen_per_set", type=int, default=18)
    ap.add_argument("--forget_cap", type=int, default=40)
    ap.add_argument("--retain_collat_cap", type=int, default=150)
    ap.add_argument("--retain_curve_cap", type=int, default=60)
    ap.add_argument("--unrel_curve_cap", type=int, default=40)
    ap.add_argument("--second_judge_cap", type=int, default=20)
    ap.add_argument("--no_judge", action="store_true")
    ap.add_argument("--no_second_judge", action="store_true")
    ap.add_argument("--out", default=str(WORK / "method_out.json"))
    args = ap.parse_args()
    set_limits()

    import torch
    torch.manual_seed(SEED)
    if torch.cuda.is_available():
        try:
            torch.cuda.set_per_process_memory_fraction(0.85)
        except Exception:
            pass
    logger.info(f"{el()} torch {torch.__version__} cuda={torch.cuda.is_available()} device={DEVICE}")

    sae = load_sae(torch)
    mb = ModelBundle(torch)
    canon = read_canonical_units()
    gating, Rnorm, tax_rows = gating_check(torch, sae, mb)

    out = {"metadata": {
        "method_name": "M1' KG-Localized Single-Absorber Unlearning vs SUB-CONTEXT-Targeted Dense Erasure",
        "description": ("DECISIVE comparison: at MATCHED forget-quality, ablate ONE KG-named absorber latent "
                        "(KG-ABL, label-free/discovered) vs erase a SUB-CONTEXT-targeted diff-of-means direction "
                        "u_sub (DENSE-SUB-ABL, built from the per-sub-context labels on a disjoint fold). WHOLE-"
                        "parent erasure (DENSE-WHOLE-ABL) is a clearly-labeled SECONDARY reference. Per-case FORK "
                        "verdict KG_BEATS_USUB / KG_MATCHES_USUB_LABEL_FREE / KG_LOSES_TO_USUB on a paired-bootstrap "
                        "joint (retain-utility x fluency) CI + 2nd-family judge confirmation. Folds in u_sub "
                        "localization validation (M1'), US-as-co-firing (M5), second-judge + human-proxy (M6), "
                        "unit-vs-single (M7)."),
        "sae": {"release": RELEASE_REPO, "sae_params": SAE_PARAMS_16K, "width": int(sae.d_sae),
                "d_model": int(sae.d_model), "hook": f"blocks.{HOOK_LAYER}.hook_resid_post"},
        "model": mb.model_id, "seed": SEED, "B_boot": B_BOOT, "Rnorm": Rnorm,
        "gating_check": gating,
        "forget_grids": {"LAM_GRID": LAM_GRID, "BETA_GRID": BETA_GRID, "MIN_SUB": MIN_SUB},
        "judge": {"primary_model": PRIMARY_JUDGE["model"], "temp": JUDGE_TEMP,
                  "target_usd": TARGET, "hard_cap_usd": HARD_CAP},
        "canonical_units_used": {
            "taxonomic_anchor": canon["taxonomic"]["anchor"], "taxonomic_k_track_unit": canon["taxonomic"]["k_track_unit"],
            "georgia_absorber": 16009, "us_absorber": 846,
            "first_letter_L_anchor": canon["first_letter"]["L"]["anchor"],
            "first_letter_L_members": canon["first_letter"]["L"]["members"], "large_absorber": 8463},
    }, "datasets": []}

    if args.smoke:
        run_smoke(torch, sae, mb, canon, gating, tax_rows, out)
        out["metadata"]["judge"]["spent_usd"] = SPENT["usd"]
        out["metadata"]["judge"]["per_model"] = PER_JUDGE
        save_json(out, args.out)
        logger.info(f"{el()} SMOKE saved -> {args.out}")
        return

    second_judge = None
    if not args.no_judge and not args.no_second_judge:
        second_judge = resolve_second_judge()
        if second_judge is None:
            logger.warning(f"{el()} second judge UNAVAILABLE — M6 judge-robustness will be unverified")

    requested = [c.strip() for c in args.cases.split(",") if c.strip()]
    setup_fns = {
        "taxonomic_georgia": lambda *a: setup_taxonomic(*a, target=("Georgia", 16009, 0.955),
                                                        case_id="taxonomic_georgia", regime="absorption", run_m7=True),
        "taxonomic_us": lambda *a: setup_taxonomic(*a, target=("United States", 846, 0.973),
                                                   case_id="taxonomic_us", regime="co-firing", run_m7=False),
        "taxonomic_jordan": lambda *a: setup_taxonomic(*a, target=("Jordan", 540, 0.975),
                                                       case_id="taxonomic_jordan", regime="absorption", run_m7=False),
        "first_letter_large": setup_first_letter,
        "toxicity_insult": setup_toxicity}
    case_results = []
    summaries = []
    human_proxy = {}
    for cid in requested:
        if cid not in setup_fns:
            logger.warning(f"unknown case {cid}; skip"); continue
        try:
            cs = setup_fns[cid](torch, sae, mb, canon, args, Rnorm)
        except Exception as e:  # noqa: BLE001
            logger.exception(f"setup failed for {cid}: {e}")
            continue
        if cs is None:
            logger.warning(f"setup returned None for {cid}; skip"); continue
        pj = None if args.no_judge else PRIMARY_JUDGE
        sj = None if (args.no_judge or args.no_second_judge) else second_judge
        res, gen, mi, judged, judged2 = run_unlearning_case(torch, sae, mb, cs, args,
                                                            primary_judge=pj, second_judge=sj)
        # M6 human-proxy deterministic check (Georgia + large)
        if cs.case_id in HUMAN_PROXY:
            hp = run_human_proxy(mb, sae, cs, res["scale_kg_lambda"], res["scale_whole_beta"])
            res["human_proxy"] = hp
            human_proxy[cs.case_id] = hp
        case_results.append((res, gen, mi, judged, judged2))
        summaries.append(res)
        logger.info(f"{el()} ${SPENT['usd']:.4f} spent after case {cid}")
        if SPENT["usd"] >= HARD_CAP:
            logger.error("HARD CAP reached; stopping judge for remaining cases")
        del cs
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    # ---------- SUMMARY ----------
    abs_cases = [r for r in summaries if r["regime"] == "absorption"]
    beats = [r for r in abs_cases if r["fork_verdict"] == "KG_BEATS_USUB"]
    matches = [r for r in abs_cases if r["fork_verdict"] == "KG_MATCHES_USUB_LABEL_FREE"]
    loses = [r for r in abs_cases if r["fork_verdict"] == "KG_LOSES_TO_USUB"]
    cof = [r for r in summaries if r["regime"] == "co-firing"]
    router_fn = [r["case_id"] for r in cof if r["case_id"] == "taxonomic_us"]
    summary = {
        "n_cases": len(summaries), "n_absorption": len(abs_cases),
        "n_KG_BEATS_USUB": len(beats), "n_KG_MATCHES_USUB_LABEL_FREE": len(matches),
        "n_KG_LOSES_TO_USUB": len(loses),
        "kg_beats_usub_cases": [r["case_id"] for r in beats],
        "kg_matches_usub_cases": [r["case_id"] for r in matches],
        "kg_loses_to_usub_cases": [r["case_id"] for r in loses],
        "router_false_negatives": router_fn,
        "m1prime_gate_passed": bool(len(beats) >= 1 or len(matches) >= 1),
        "all_localize_better_than_whole": bool(all(r["u_sub_localizes_better_than_whole"] for r in summaries)) if summaries else None,
        "cofiring_cases": [{"case_id": r["case_id"], "fork_verdict": r["fork_verdict"],
                            "firing_jaccard_absorber": r["firing_jaccard_with_parent"],
                            "firing_jaccard_aggregate": r["firing_jaccard_aggregate_parent"],
                            "parent_recall_hole": r["parent_recall_hole"]} for r in cof],
        "per_case_fork": [{"case_id": r["case_id"], "regime": r["regime"], "fork_verdict": r["fork_verdict"],
                           "joint_diff_CI_KG_vs_SUB": r["joint_diff_CI_KG_vs_SUB"],
                           "second_judge_CI": (r.get("second_judge") or {}).get("joint_diff_CI_KG_vs_SUB"),
                           "collateral_diff_CI_KG_vs_SUB": r["collateral_diff_CI_KG_vs_SUB"],
                           "u_sub_localizes_better_than_whole": r["u_sub_localizes_better_than_whole"],
                           "curve_dominance_KG_vs_SUB": r["curve_dominance_KG_vs_SUB"]["dominance_fraction"],
                           "m7": r.get("m7_unit_vs_single")} for r in summaries],
        "human_proxy_passed": {cid: (hp.get("passed") if hp else None) for cid, hp in human_proxy.items()},
    }

    # ---------- HONEST NEGATIVES (mutates each summary to add mi_corroborates_fork) ----------
    honest = build_honest_negatives(summaries, second_judge is not None)

    out["metadata"]["judge"]["spent_usd"] = SPENT["usd"]
    out["metadata"]["judge"]["n_calls"] = SPENT["calls"]
    out["metadata"]["judge"]["n_fail"] = SPENT["fail"]
    out["metadata"]["judge"]["n_refusal_or_parsefail"] = SPENT["refusal"]
    out["metadata"]["judge"]["per_model"] = PER_JUDGE
    out["metadata"]["judge"]["second_judge_model"] = (second_judge["model"] if second_judge else "unavailable")
    out["metadata"]["per_case"] = summaries
    out["metadata"]["summary"] = summary
    out["metadata"]["honest_negatives"] = honest

    assemble_outputs(out, case_results)
    save_json(out, args.out)
    logger.info(f"{el()} SAVED {args.out}")
    logger.info(f"{el()} SUMMARY: n_cases={len(summaries)} BEATS={len(beats)} MATCHES={len(matches)} "
                f"LOSES={len(loses)} gate={summary['m1prime_gate_passed']} judge_spent=${SPENT['usd']:.4f}")
    for r in summaries:
        logger.info(f"  {r['case_id']}: {r['fork_verdict']} | localizes_better={r['u_sub_localizes_better_than_whole']} "
                    f"| dom_KGvsSUB={r['curve_dominance_KG_vs_SUB']['dominance_fraction']:.2f} "
                    f"| 2nd={(r.get('second_judge') or {}).get('model')}")


if __name__ == "__main__":
    main()
