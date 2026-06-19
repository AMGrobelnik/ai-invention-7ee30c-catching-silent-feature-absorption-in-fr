#!/usr/bin/env python
"""
M1 DOWNSTREAM WIN: KG-LOCALIZED SINGLE-ABSORBER UNLEARNING vs DENSE PARENT ERASURE.

Converts iter-4's "surgical selectivity" capability into a DOWNSTREAM WIN on an outcome that
matters: SELECTIVE SUB-CONCEPT UNLEARNING. We ablate ONE KG-named absorber latent (Georgia->16009,
first-letter 'large'->8463, toxicity insult co-firing case) and ask whether, AT MATCHED FORGET-QUALITY,
the localized KG ablation (KG-ABL) yields STRICTLY LOWER sibling+parent collateral AND BETTER preserved
fluency than the dense diff-of-means / LEACE parent erasure (DENSE-ABL, baseline f), with a paired
bootstrap CI on the JOINT (retain-quality x fluency) outcome difference that EXCLUDES 0.

WIN <=> at matched forget, KG-ABL has LOWER collateral AND BETTER fluency than DENSE-ABL, joint
KG-minus-dense CI excl 0. A clean dense-wins-everywhere result is the publishable
'auditability without a better outcome' limitation.

NEW machinery vs iter-4 (reused verbatim via `core`):
  1. forget-quality matching via a lambda/beta sweep (model-internal next-token KL on FORGET windows),
  2. GENERATION under each edit hook (greedy model.generate with the forward edit installed),
  3. an AxBench-style OpenRouter LLM judge (anthropic/claude-haiku-4.5, temp 0, harmonic-mean 0-2 rubric),
  4. a retain-quality x fluency JOINT composite + KG-minus-dense paired-bootstrap CIs,
  5. model-internal corroboration (high-n retain next-token KL collateral + continuation perplexity),
  6. curve-level dominance across the achievable forget range.

Cases (gradual scaling order):
  C1 taxonomic   / X='Georgia' / l=16009 / regime='absorption'   (PRIMARY, dense structurally over-shoots)
  C2 first_letter/ X='large'   / l=8463  / regime='absorption'   (SECONDARY, cleaner higher-magnitude absorber)
  C3 toxicity    / X='insult'  / l=~auto / regime='co-firing'    (HONEST: KG PREDICTED TO LOSE -> router-consistent)

Usage:
  uv run method.py --smoke
  uv run method.py --cases taxonomic_georgia --cap 30 --gen_per_set 6   # mini
  uv run method.py                                                       # full (all 3 cases)
"""
import os, sys, json, time, gc, argparse, math, threading
from pathlib import Path
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import requests

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")

# ----------------------------------------------------------- reuse iter-4 machinery VERBATIM (core.py)
import core
from core import (
    logger, el, load_sae, ModelBundle, ParentProbe, make_edit_hook, side_effects,
    base_distributions, forward_pos_logprobs, kl_rows, behavioral_curve, content_responsive,
    pick_random_latents, paired_bootstrap_diff, bootstrap_mean_ci, _scale_for_on_target, _interp_at,
    load_taxonomic, load_first_letter, load_toxicity, NEUTRAL_TEXT, save_json, _json_default,
    read_canonical_units, select_positions, set_limits,
    DEVICE, SEED, B_BOOT, EPS, D_MODEL, RELEASE_REPO, SAE_PARAMS_16K, HOOK_LAYER,
)

WORK = Path("/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_1")
rng = np.random.default_rng(SEED)

# --------------------------------------------------------------------------- forget-matching grids
LAM_GRID = [0.0, 0.5, 1.0, 2.0, 3.0, 4.0]          # KG single-latent ablation strength (lambda)
BETA_GRID = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0]    # dense parent-erasure strength (beta)
RAND_SCALE = 1.0

# --------------------------------------------------------------------------- generation config
MAX_NEW = 40
GEN_BATCH = 8
GEN_MAXLEN_PROMPT = 96

# --------------------------------------------------------------------------- OpenRouter judge config
MODEL_JUDGE = "anthropic/claude-haiku-4.5"
JUDGE_URL = "https://openrouter.ai/api/v1/chat/completions"
JUDGE_TEMP = 0.0
JUDGE_MAXTOK = 220
COST_IN = 1.0 / 1e6      # $/input token
COST_OUT = 5.0 / 1e6     # $/output token
HARD_CAP = 10.0
TARGET = 2.0
JUDGE_WORKERS = 8

_spend_lock = threading.Lock()
SPENT = {"usd": 0.0, "calls": 0, "fail": 0, "refusal": 0}


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
    """Extract {fluency, content_pres} ints in {0,1,2} from a model JSON response (tolerant)."""
    if not content:
        return None
    s = content.strip()
    if "```" in s:
        # strip code fences
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


def judge_call(task, max_retries=4):
    """One OpenRouter judge call. task carries role/X/prompt/base_cont/edit_cont. Returns dict or None.
    Cost-tracked; stops issuing NEW calls once SPENT exceeds TARGET (those pairs fall back to model-internal)."""
    with _spend_lock:
        if SPENT["usd"] >= TARGET or SPENT["usd"] >= HARD_CAP:
            return None
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        return None
    user = _judge_user_prompt(task["role"], task["X"], task["prompt"], task["base_cont"], task["edit_cont"])
    payload = {"model": MODEL_JUDGE, "temperature": JUDGE_TEMP, "max_tokens": JUDGE_MAXTOK,
               "messages": [{"role": "system", "content": JUDGE_SYS}, {"role": "user", "content": user}]}
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    backoff = 1.5
    for attempt in range(max_retries):
        try:
            r = requests.post(JUDGE_URL, headers=headers, json=payload, timeout=90)
        except Exception as e:  # noqa: BLE001
            if attempt == max_retries - 1:
                with _spend_lock:
                    SPENT["fail"] += 1
                return None
            time.sleep(backoff ** attempt)
            continue
        if r.status_code in (429, 500, 502, 503, 529):
            if attempt == max_retries - 1:
                with _spend_lock:
                    SPENT["fail"] += 1
                return None
            time.sleep(backoff ** attempt)
            continue
        if r.status_code != 200:
            with _spend_lock:
                SPENT["fail"] += 1
            return None
        try:
            j = r.json()
        except Exception:
            with _spend_lock:
                SPENT["fail"] += 1
            return None
        usage = j.get("usage", {}) or {}
        pin = int(usage.get("prompt_tokens", 0)); pout = int(usage.get("completion_tokens", 0))
        with _spend_lock:
            SPENT["usd"] += pin * COST_IN + pout * COST_OUT
            SPENT["calls"] += 1
        try:
            content = j["choices"][0]["message"]["content"]
        except Exception:
            with _spend_lock:
                SPENT["refusal"] += 1
            return None
        parsed = _parse_judge(content)
        if parsed is None:
            with _spend_lock:
                SPENT["refusal"] += 1
            return None
        return parsed
    return None


def run_judge_batch(tasks):
    """Threaded judge over a list of tasks -> list of dict|None aligned to tasks. Cost-bounded."""
    if not tasks:
        return []
    results = [None] * len(tasks)
    with ThreadPoolExecutor(max_workers=JUDGE_WORKERS) as ex:
        futs = {ex.submit(judge_call, t): i for i, t in enumerate(tasks)}
        for fut in futs:
            i = futs[fut]
            try:
                results[i] = fut.result()
            except Exception:
                results[i] = None
    return results


def harmonic_mean(f, c):
    f = float(f); c = float(c)
    if f <= 0 and c <= 0:
        return 0.0
    return (2.0 * f * c) / (f + c + 1e-9)


# =========================================================================== GENERATION under edit hook
def generate_under_edit(mb, sae, prompts, kind=None, l=None, u=None, v=None, scale=0.0,
                        max_new=MAX_NEW, batch=GEN_BATCH, clamp_norm=False):
    """Greedy continuations under an optional forward edit hook installed at the edit layer.
    KG-ABL (kind='abl_latent') fires only when latent l is active at a decoded token (surgical);
    DENSE-ABL (kind='erase_dir') perturbs every token along the parent direction u."""
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
    (prevents bf16 blow-ups / NaNs during free generation)."""
    def hook(_m, _i, out):
        h = out[0] if isinstance(out, (tuple, list)) else out
        hf = h.to(torch.float32)
        n_before = hf.norm(dim=-1, keepdim=True)
        if kind == "abl_latent":
            z = sae.encode(hf)
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
    """Self-perplexity of each continuation string under the UNEDITED base model (lower=more fluent).
    Model-internal fluency proxy. Empty / 1-token texts -> NaN (judge handles those)."""
    torch = mb.torch; tok = mb.tok
    out = np.full(len(texts), np.nan)
    idx_valid = [i for i, t in enumerate(texts) if len(t.strip()) > 0]
    for b0 in range(0, len(idx_valid), batch):
        bidx = idx_valid[b0:b0 + batch]
        bt = [texts[i] for i in bidx]
        enc = tok(bt, return_tensors="pt", padding=True, truncation=True, max_length=64,
                  add_special_tokens=True)
        ids = enc["input_ids"].to(DEVICE); am = enc["attention_mask"].to(DEVICE)
        labels = ids.clone()
        labels[am == 0] = -100
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
    """Next-token log-probs at the LAST real token of each prompt, under an optional edit hook.
    Returns [N,V] fp16. Used for per-gen-prompt model-internal collateral (KL vs base)."""
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
                T = int(am[i].sum())
                pos = max(T - 1, 0)
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
    """Prefix of `text` ending just BEFORE the labeled target token (char span). Falls back to a
    natural mid-point if the span is missing or too early."""
    if span and span[0] is not None and int(span[0]) >= min_chars:
        cut = int(span[0])
        pre = text[:cut].rstrip()
        if len(pre) >= min_chars:
            return pre
    # fallback: truncate at ~60% on a whitespace boundary
    cut = max(min_chars, int(len(text) * 0.6))
    pre = text[:cut]
    sp = pre.rfind(" ")
    if sp > min_chars:
        pre = pre[:sp]
    return pre.rstrip() or text[:min_chars]


def build_prompts(rows, role, n, use_span=True):
    """Build up to n generation prefixes from rows (dicts with 'input' and optional _span)."""
    prompts, meta = [], []
    for r in rows[:n]:
        text = r["input"]
        if use_span:
            pre = _prefix_before_span(text, r.get("_span"))
        else:
            # whole-sentence rows (toxicity): keep first ~60%
            pre = _prefix_before_span(text, None)
        if len(pre.strip()) < 8:
            continue
        prompts.append(pre)
        meta.append({"sub_context": r.get("metadata_sub_context") or r.get("metadata_target_word"),
                     "full": text[:240]})
    return prompts, meta


# =========================================================================== CASE SETUP (encode + probe + roles)
class CaseSpec:
    pass


def setup_taxonomic(torch, sae, mb, canon, args, Rnorm, target=("Georgia", 16009, 0.955), case_id="taxonomic_georgia"):
    X, absorber, precision = target
    logger.info(f"\n{el()} ===== SETUP taxonomic / {X} (absorber {absorber}) =====")
    rows = load_taxonomic()
    corp = [r for r in rows if r["metadata_row_type"] == "corpus"]
    cpairs = [r for r in rows if r["metadata_row_type"] == "content_pair"]
    eligible = ['Australia', 'Brazil', 'Canada', 'China', 'France', 'Georgia', 'Germany', 'India',
                'Iran', 'Ireland', 'Israel', 'Italy', 'Japan', 'Mexico', 'New Zealand', 'Poland',
                'Russia', 'Spain', 'United Kingdom', 'United States']
    encode_countries = set(eligible) | {X}   # ensure target country is encoded even if not in `eligible`
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

    # responsive set (content pairs)
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

    # PROBE: fit on diagnostic fold (parent-positive vs negatives); eval roles on TRAIN fold (disjoint)
    fit_pos = np.where((kind == "pos") & (fold == "diagnostic"))[0]
    fit_neg = np.where((kind == "neg") & (fold == "diagnostic"))[0]
    probe = ParentProbe(torch, resid[fit_pos].astype(np.float32), resid[fit_neg].astype(np.float32))
    probe._Rnorm = Rnorm
    logger.info(f"{el()} taxonomic probe train_auc={probe.train_auc:.3f} cos(probe,dmu)={probe.cos_probe_dmu:.3f}")

    anchor = canon["taxonomic"]["anchor"]
    ev = "train"
    forget_idx = np.where((kind == "pos") & (sub == X) & (fold == ev))[0]
    if len(forget_idx) < 8:
        forget_idx = np.where((kind == "pos") & (sub == X))[0]
    sib_names = [c for c in eligible if c != X]
    retain_idx = np.where((kind == "pos") & (sub != X) & np.isin(sub, sib_names) & (fold == ev))[0]
    unrel_idx = np.where((kind == "neg") & (fold == ev))[0]

    member_set = set(canon["taxonomic"]["k_track_unit"]) | \
        set(a["latent"] for a in canon["taxonomic"]["diag_absorbers"])
    rand_lat, trate = pick_random_latents(lat_csr, absorber, cr, member_set)

    # firing-jaccard + parent recall hole (router anchors)
    fj, hole = _router_anchors(lat_csr, anchor, absorber, np.where((kind == "pos") & (sub == X))[0])

    cs = CaseSpec()
    cs.case_id = case_id; cs.family = "taxonomic"; cs.X = X; cs.absorber = absorber
    cs.absorber_precision = precision; cs.anchor = anchor; cs.regime = "absorption"
    cs.probe = probe; cs.u = probe.u_t
    cs.forget_rows = [enc_rows[i] for i in forget_idx]
    cs.retain_rows = [enc_rows[i] for i in retain_idx]
    cs.unrel_rows = [enc_rows[i] for i in unrel_idx]
    cs.siblings = sib_names; cs.rand_latents = rand_lat; cs.rand_rate = trate
    cs.firing_jaccard = fj; cs.parent_recall_hole = hole
    cs.whole_sentence = False; cs.use_span = True
    cs.neutral_unrel = list(NEUTRAL_TEXT)
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
    unrel_idx = np.array([], int)  # UNRELATED = NEUTRAL_TEXT for first-letter

    member_set = set(unit["members"])
    rand_lat, trate = pick_random_latents(lat_csr, absorber, cr, member_set)
    fj, hole = _router_anchors(lat_csr, anchor, absorber, np.where((letter == "L") & (sub == X))[0])

    cs = CaseSpec()
    cs.case_id = "first_letter_large"; cs.family = "first_letter"; cs.X = X; cs.absorber = absorber
    cs.absorber_precision = 1.0; cs.anchor = anchor; cs.regime = "absorption"
    cs.probe = probe; cs.u = probe.u_t
    cs.forget_rows = [enc_rows[i] for i in forget_idx]
    cs.retain_rows = [enc_rows[i] for i in retain_idx]
    cs.unrel_rows = []
    cs.siblings = sib_words[:12]; cs.rand_latents = rand_lat; cs.rand_rate = trate
    cs.firing_jaccard = fj; cs.parent_recall_hole = hole
    cs.whole_sentence = False; cs.use_span = True
    cs.neutral_unrel = list(NEUTRAL_TEXT)
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
    sib_mask = eval_mask & (label == 1) & (subm["insult"] == 0) & (
        (subm["obscene"] == 1) | (subm["threat"] == 1) | (subm["identity_attack"] == 1))
    retain_idx = np.where(sib_mask)[0]
    unrel_idx = np.where((label == 0) & eval_mask)[0]
    if len(forget_idx) > 400:
        forget_idx = rng.choice(forget_idx, 400, replace=False)
    if len(retain_idx) > 400:
        retain_idx = rng.choice(retain_idx, 400, replace=False)

    member_set = {absorber, parent_latent}
    responsive_tox = np.where(fire_tox > 0.05)[0]
    rand_lat, trate = pick_random_latents(lat_csr, absorber, responsive_tox, member_set)
    fj, hole = _router_anchors(lat_csr, parent_latent, absorber,
                               np.where((label == 1) & (subm["insult"] == 1))[0])

    cs = CaseSpec()
    cs.case_id = "toxicity_insult"; cs.family = "toxicity"; cs.X = "insult"; cs.absorber = absorber
    cs.absorber_precision = float(best_auc); cs.anchor = parent_latent; cs.regime = "co-firing"
    cs.probe = probe; cs.u = probe.u_t
    cs.forget_rows = [enc_rows[i] for i in forget_idx]
    cs.retain_rows = [enc_rows[i] for i in retain_idx]
    cs.unrel_rows = [enc_rows[i] for i in unrel_idx]
    cs.siblings = ["obscene", "threat", "identity_attack"]; cs.rand_latents = rand_lat; cs.rand_rate = trate
    cs.firing_jaccard = fj; cs.parent_recall_hole = hole
    cs.whole_sentence = True; cs.use_span = False
    cs.neutral_unrel = []
    cs.insult_auc = float(best_auc)
    del lat_csr, resid
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return cs


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


# =========================================================================== the UNLEARNING experiment
def run_unlearning_case(torch, sae, mb, cs, args, do_judge=True):
    logger.info(f"\n{el()} ##### UNLEARN CASE {cs.case_id} (absorber={cs.absorber}, regime={cs.regime}) #####")
    ws = cs.whole_sentence
    l = cs.absorber; u = cs.u

    # ---- caps ----
    n_forget = min(len(cs.forget_rows), args.forget_cap)
    n_retain_curve = min(len(cs.retain_rows), args.retain_curve_cap)
    n_retain_collat = min(len(cs.retain_rows), args.retain_collat_cap)
    forget_rows = cs.forget_rows[:n_forget]
    retain_curve_rows = cs.retain_rows[:n_retain_curve]
    retain_collat_rows = cs.retain_rows[:n_retain_collat]
    unrel_rows = cs.unrel_rows[:args.unrel_curve_cap] if cs.unrel_rows else []

    # =================== (4) FORGET-QUALITY MATCHING (model-internal next-token KL on FORGET) ===========
    base_forget, _ = forward_pos_logprobs(mb, sae, forget_rows, whole_sentence=ws)
    forget_kg_kl, foot_kg = behavioral_curve(mb, sae, forget_rows, base_forget, "abl_latent",
                                             l=l, scales=LAM_GRID, whole_sentence=ws)
    forget_de_kl, foot_de = behavioral_curve(mb, sae, forget_rows, base_forget, "erase_dir",
                                             u=u, scales=BETA_GRID, whole_sentence=ws)
    forget_kg_curve = forget_kg_kl.mean(0); forget_de_curve = forget_de_kl.mean(0)
    max_kg = float(forget_kg_curve.max()); max_de = float(forget_de_curve.max())
    matched_target = 0.8 * min(max_kg, max_de)
    matched_target = max(matched_target, 1e-4)
    s_kg = _scale_for_on_target(LAM_GRID, forget_kg_curve.tolist(), matched_target)
    s_de = _scale_for_on_target(BETA_GRID, forget_de_curve.tolist(), matched_target)
    logger.info(f"{el()} FORGET match: max_kg={max_kg:.4f} max_de={max_de:.4f} target={matched_target:.4f} "
                f"s_kg={s_kg:.3f} s_de={s_de:.3f} foot_kg={foot_kg} foot_de={foot_de}")

    # =================== (5) MODEL-INTERNAL COLLATERAL: high-n retain next-token KL at matched ==========
    base_retain_c, _ = forward_pos_logprobs(mb, sae, retain_collat_rows, whole_sentence=ws)
    elp_kg, _ = forward_pos_logprobs(mb, sae, retain_collat_rows, kind="abl_latent", l=l, scale=s_kg,
                                     whole_sentence=ws)
    elp_de, _ = forward_pos_logprobs(mb, sae, retain_collat_rows, kind="erase_dir", u=u, scale=s_de,
                                     whole_sentence=ws)
    retain_kl_kg = kl_rows(elp_kg, base_retain_c)
    retain_kl_de = kl_rows(elp_de, base_retain_c)
    del elp_kg, elp_de, base_retain_c
    collateral_diff_CI = paired_bootstrap_diff(retain_kl_de, retain_kl_kg)  # >0 => KG less collateral
    logger.info(f"{el()} retain collateral KL (n={len(retain_kl_kg)}): KG={retain_kl_kg.mean():.5f} "
                f"DENSE={retain_kl_de.mean():.5f} diff_excl0={collateral_diff_CI['excl_0']}")

    # =================== (9) CURVE-LEVEL DOMINANCE (model-internal, $0) ==================================
    base_retain_cu, _ = forward_pos_logprobs(mb, sae, retain_curve_rows, whole_sentence=ws)
    retain_kg_grid, _ = behavioral_curve(mb, sae, retain_curve_rows, base_retain_cu, "abl_latent",
                                         l=l, scales=LAM_GRID, whole_sentence=ws)
    retain_de_grid, _ = behavioral_curve(mb, sae, retain_curve_rows, base_retain_cu, "erase_dir",
                                         u=u, scales=BETA_GRID, whole_sentence=ws)
    retain_kg_mean = retain_kg_grid.mean(0); retain_de_mean = retain_de_grid.mean(0)
    # internal fluency proxy: next-token KL on UNRELATED windows (or neutral text rows) across the grid
    unrel_kg_mean = unrel_de_mean = None
    if len(unrel_rows) >= 4:
        base_unrel, _ = forward_pos_logprobs(mb, sae, unrel_rows, whole_sentence=ws)
        unrel_kg_grid, _ = behavioral_curve(mb, sae, unrel_rows, base_unrel, "abl_latent",
                                            l=l, scales=LAM_GRID, whole_sentence=ws)
        unrel_de_grid, _ = behavioral_curve(mb, sae, unrel_rows, base_unrel, "erase_dir",
                                            u=u, scales=BETA_GRID, whole_sentence=ws)
        unrel_kg_mean = unrel_kg_grid.mean(0); unrel_de_mean = unrel_de_grid.mean(0)
    dom = _curve_dominance(forget_kg_curve, retain_kg_mean, unrel_kg_mean, LAM_GRID,
                           forget_de_curve, retain_de_mean, unrel_de_mean, BETA_GRID)
    logger.info(f"{el()} curve-dominance fraction (KG strictly better collateral [+fluency]) = "
                f"{dom['dominance_fraction']:.3f} over {dom['n_levels']} forget levels")

    # =================== (6) GENERATION under each edit hook =============================================
    gp_forget, _ = build_prompts(forget_rows, "FORGET", args.gen_per_set, use_span=cs.use_span)
    gp_retain, _ = build_prompts(cs.retain_rows, "RETAIN", args.gen_per_set, use_span=cs.use_span)
    if cs.unrel_rows:
        gp_unrel, _ = build_prompts(cs.unrel_rows, "UNRELATED", args.gen_per_set, use_span=cs.use_span)
    else:
        gp_unrel = list(cs.neutral_unrel)[:args.gen_per_set]
    # also include some neutral text as universal UNRELATED anchor
    if cs.neutral_unrel and cs.unrel_rows:
        gp_unrel = (gp_unrel + list(cs.neutral_unrel))[:args.gen_per_set + min(8, len(cs.neutral_unrel))]
    logger.info(f"{el()} gen prompts: forget={len(gp_forget)} retain={len(gp_retain)} unrel={len(gp_unrel)}")

    rand_l = int(cs.rand_latents[0]) if cs.rand_latents else None
    rng_norm_clamp = False
    gen = {}
    for role, prompts in (("FORGET", gp_forget), ("RETAIN", gp_retain), ("UNRELATED", gp_unrel)):
        if not prompts:
            gen[role] = {"prompts": [], "NOOP": [], "KG-ABL": [], "DENSE-ABL": [], "RAND": []}
            continue
        base_c = generate_under_edit(mb, sae, prompts, kind=None)
        kg_c = generate_under_edit(mb, sae, prompts, kind="abl_latent", l=l, scale=s_kg, clamp_norm=rng_norm_clamp)
        de_c = generate_under_edit(mb, sae, prompts, kind="erase_dir", u=u, scale=s_de, clamp_norm=rng_norm_clamp)
        rd_c = (generate_under_edit(mb, sae, prompts, kind="abl_latent", l=rand_l, scale=RAND_SCALE)
                if rand_l is not None else [""] * len(prompts))
        # NaN/garbage guard: if KG or DENSE collapse to empty/degenerate, retry that op with norm-clamp
        if _degenerate(kg_c) or _degenerate(de_c):
            logger.warning(f"{el()} {role}: degenerate generation detected -> retry with norm-clamp")
            kg_c = generate_under_edit(mb, sae, prompts, kind="abl_latent", l=l, scale=s_kg, clamp_norm=True)
            de_c = generate_under_edit(mb, sae, prompts, kind="erase_dir", u=u, scale=s_de, clamp_norm=True)
        gen[role] = {"prompts": prompts, "NOOP": base_c, "KG-ABL": kg_c, "DENSE-ABL": de_c, "RAND": rd_c}

    # ---- model-internal per-gen-prompt signals (collateral = last-tok KL vs base; fluency = cont. PPL) ----
    mi = {}
    for role in ("FORGET", "RETAIN", "UNRELATED"):
        prompts = gen[role]["prompts"]
        if not prompts:
            mi[role] = {}
            continue
        base_lp = last_tok_logprobs(mb, sae, prompts, kind=None)
        kg_lp = last_tok_logprobs(mb, sae, prompts, kind="abl_latent", l=l, scale=s_kg)
        de_lp = last_tok_logprobs(mb, sae, prompts, kind="erase_dir", u=u, scale=s_de)
        mi[role] = {
            "kl_kg": kl_rows(kg_lp, base_lp), "kl_de": kl_rows(de_lp, base_lp),
            "ppl_noop": continuation_ppl(mb, gen[role]["NOOP"]),
            "ppl_kg": continuation_ppl(mb, gen[role]["KG-ABL"]),
            "ppl_de": continuation_ppl(mb, gen[role]["DENSE-ABL"]),
            "ppl_rand": continuation_ppl(mb, gen[role]["RAND"]),
        }
        del base_lp, kg_lp, de_lp

    # =================== (7) LLM JUDGE (AxBench harmonic-mean 0-2) =======================================
    judged = {role: {"KG-ABL": [], "DENSE-ABL": [], "RAND": []} for role in ("FORGET", "RETAIN", "UNRELATED")}
    if do_judge and os.environ.get("OPENROUTER_API_KEY"):
        tasks, locs = [], []
        for role in ("FORGET", "RETAIN", "UNRELATED"):
            g = gen[role]
            for j, p in enumerate(g["prompts"]):
                for op in ("KG-ABL", "DENSE-ABL", "RAND"):
                    tasks.append({"role": role, "X": cs.X, "prompt": p[:700],
                                  "base_cont": g["NOOP"][j][:500], "edit_cont": g[op][j][:500]})
                    locs.append((role, op, j))
        logger.info(f"{el()} issuing {len(tasks)} judge calls (SPENT=${SPENT['usd']:.4f})")
        res = run_judge_batch(tasks)
        # reshape into judged[role][op] aligned by prompt index j
        tmp = {role: {op: {} for op in ("KG-ABL", "DENSE-ABL", "RAND")}
               for role in ("FORGET", "RETAIN", "UNRELATED")}
        for (role, op, j), r in zip(locs, res):
            tmp[role][op][j] = r
        for role in judged:
            npr = len(gen[role]["prompts"])
            for op in ("KG-ABL", "DENSE-ABL", "RAND"):
                judged[role][op] = [tmp[role][op].get(j) for j in range(npr)]
        logger.info(f"{el()} judge done: SPENT=${SPENT['usd']:.4f} calls={SPENT['calls']} "
                    f"fail={SPENT['fail']} refusal={SPENT['refusal']}")

    # =================== (8) JOINT OUTCOME + KG-MINUS-DENSE WIN TEST =====================================
    res_out = _joint_and_verdict(cs, gen, mi, judged, collateral_diff_CI, dom,
                                 s_kg, s_de, matched_target, forget_kg_curve, forget_de_curve,
                                 foot_kg, foot_de, retain_kl_kg, retain_kl_de,
                                 retain_kg_mean, retain_de_mean, unrel_kg_mean, unrel_de_mean)
    res_out["case_id"] = cs.case_id
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return res_out, gen, mi, judged


def _degenerate(conts):
    """True if a large fraction of continuations are empty or single-token repetition (NaN/blowup symptom)."""
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
    """Fraction of achievable forget levels where KG has strictly LOWER collateral (and lower unrelated
    perturbation, if available) than DENSE at the SAME forget. Compares on a common forget grid by
    interpolating DENSE's collateral/unrel at KG's forget levels."""
    fk = np.asarray(fk); rk = np.asarray(rk); fd = np.asarray(fd); rd = np.asarray(rd)
    # KG forget levels with a real edit
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
            "dense_forget_grid": fd.tolist(), "dense_collateral_grid": rd.tolist()}


def _joint_and_verdict(cs, gen, mi, judged, collateral_diff_CI, dom, s_kg, s_de, matched_target,
                       forget_kg_curve, forget_de_curve, foot_kg, foot_de,
                       retain_kl_kg, retain_kl_de, retain_kg_mean, retain_de_mean,
                       unrel_kg_mean, unrel_de_mean):
    PRES = ("RETAIN", "UNRELATED")  # preservation set for the WIN test
    # ---------- judge-based joint over preservation set ----------
    jk_joint, jd_joint, jk_flu, jd_flu = [], [], [], []
    per_role_judge = {}
    for role in ("FORGET", "RETAIN", "UNRELATED"):
        jk = judged[role].get("KG-ABL", []); jd = judged[role].get("DENSE-ABL", [])
        npr = len(gen[role]["prompts"])
        role_kg_u, role_de_u = [], []
        for j in range(npr):
            rk = jk[j] if j < len(jk) else None
            rd = jd[j] if j < len(jd) else None
            if rk is None or rd is None:
                continue
            uk = harmonic_mean(rk["fluency"], rk["content_pres"])
            ud = harmonic_mean(rd["fluency"], rd["content_pres"])
            role_kg_u.append(uk); role_de_u.append(ud)
            if role in PRES:
                jk_joint.append(uk); jd_joint.append(ud)
                jk_flu.append(rk["fluency"]); jd_flu.append(rd["fluency"])
        per_role_judge[role] = {
            "n_paired": len(role_kg_u),
            "kg_utility_mean": float(np.mean(role_kg_u)) if role_kg_u else None,
            "dense_utility_mean": float(np.mean(role_de_u)) if role_de_u else None}
    n_judge = len(jk_joint)
    judge_available = n_judge >= max(6, int(0.3 * sum(len(gen[r]["prompts"]) for r in PRES)))

    joint_diff_CI = paired_bootstrap_diff(jk_joint, jd_joint) if judge_available else None
    fluency_diff_CI = paired_bootstrap_diff(jk_flu, jd_flu) if judge_available else None

    # ---------- judged forget confirmation (matched at generation level) ----------
    jf_kg = per_role_judge.get("FORGET", {}).get("kg_utility_mean")
    jf_de = per_role_judge.get("FORGET", {}).get("dense_utility_mean")
    # forget quality = content_pres (inverted in rubric) -> use mean content_pres directly
    fkg_cp, fde_cp = [], []
    for j in range(len(gen["FORGET"]["prompts"])):
        rk = judged["FORGET"]["KG-ABL"][j] if j < len(judged["FORGET"]["KG-ABL"]) else None
        rd = judged["FORGET"]["DENSE-ABL"][j] if j < len(judged["FORGET"]["DENSE-ABL"]) else None
        if rk is not None:
            fkg_cp.append(rk["content_pres"])
        if rd is not None:
            fde_cp.append(rd["content_pres"])
    judged_forget = {"kg_mean_forget_quality": float(np.mean(fkg_cp)) if fkg_cp else None,
                     "dense_mean_forget_quality": float(np.mean(fde_cp)) if fde_cp else None,
                     "n_kg": len(fkg_cp), "n_dense": len(fde_cp)}

    # ---------- MODEL-INTERNAL joint over preservation gen-prompts (fallback / corroboration) ----------
    mik_kl, mid_kl, mik_ppl, mid_ppl = [], [], [], []
    mik_joint, mid_joint = [], []
    noop_ppls = []
    for role in PRES:
        m = mi.get(role, {})
        if not m:
            continue
        npr = len(gen[role]["prompts"])
        for j in range(npr):
            klk = float(m["kl_kg"][j]); kld = float(m["kl_de"][j])
            pk = float(m["ppl_kg"][j]); pd = float(m["ppl_de"][j]); pn = float(m["ppl_noop"][j])
            mik_kl.append(klk); mid_kl.append(kld)
            if np.isfinite(pk) and np.isfinite(pd):
                mik_ppl.append(pk); mid_ppl.append(pd)
            if np.isfinite(pn):
                noop_ppls.append(pn)
            # per-prompt MI utility = harmonic_mean(fluency_score, retain_quality_score), both in (0,1]
            rq_k = 1.0 / (1.0 + klk); rq_d = 1.0 / (1.0 + kld)
            fl_k = 1.0 / (1.0 + math.log1p(pk)) if np.isfinite(pk) else 0.3
            fl_d = 1.0 / (1.0 + math.log1p(pd)) if np.isfinite(pd) else 0.3
            mik_joint.append(harmonic_mean(2 * fl_k, 2 * rq_k))   # scale to 0-2 for comparability
            mid_joint.append(harmonic_mean(2 * fl_d, 2 * rq_d))
    mi_collateral_diff_CI = paired_bootstrap_diff(mid_kl, mik_kl)    # >0 => KG less collateral (gen set)
    mi_fluency_diff_CI = paired_bootstrap_diff(mid_ppl, mik_ppl)     # >0 => KG lower ppl => more fluent
    mi_joint_diff_CI = paired_bootstrap_diff(mik_joint, mid_joint)   # >0 => KG higher joint utility

    # ---------- WIN VERDICT (pre-registered) ----------
    def _favors_kg(ci):
        return bool(ci is not None and ci.get("excl_0") and ci.get("diff", 0) > 0)

    collat_win = _favors_kg(collateral_diff_CI)
    if judge_available:
        joint_win = _favors_kg(joint_diff_CI)
        fluency_win = _favors_kg(fluency_diff_CI)
        primary_joint_CI = joint_diff_CI; primary_fluency_CI = fluency_diff_CI
        primary_basis = "llm_judge"
    else:
        joint_win = _favors_kg(mi_joint_diff_CI)
        fluency_win = _favors_kg(mi_fluency_diff_CI)
        primary_joint_CI = mi_joint_diff_CI; primary_fluency_CI = mi_fluency_diff_CI
        primary_basis = "model_internal_fallback"

    n_subdim = int(collat_win) + int(fluency_win)
    if cs.regime == "co-firing":
        high_jaccard = (cs.firing_jaccard is not None and cs.firing_jaccard > 0.3)
        no_hole = (cs.parent_recall_hole is not None and cs.parent_recall_hole < 0.1)
        if not joint_win and (high_jaccard or no_hole):
            verdict = "EXPECTED_LOSS_ROUTER_CONSISTENT"
        elif joint_win and collat_win and fluency_win:
            verdict = "UNEXPECTED_WIN"
        else:
            verdict = "LOSS_NOT_ROUTER_FLAGGED"
    else:  # absorption
        if joint_win and collat_win and fluency_win:
            verdict = "DOWNSTREAM_WIN_CONFIRMED"
        elif joint_win and n_subdim >= 1:
            verdict = "PARTIAL_WIN"
        elif joint_win:
            verdict = "PARTIAL_WIN"
        else:
            verdict = "AUDITABILITY_NO_BETTER_OUTCOME"

    # model-internal-only verdict (robustness, judge-independent)
    mi_collat_win = _favors_kg(collateral_diff_CI)
    mi_flu_win = _favors_kg(mi_fluency_diff_CI)
    mi_joint_win = _favors_kg(mi_joint_diff_CI)
    if cs.regime == "co-firing":
        verdict_mi = "EXPECTED_LOSS_ROUTER_CONSISTENT" if not mi_joint_win else "UNEXPECTED_WIN"
    else:
        if mi_joint_win and mi_collat_win and mi_flu_win:
            verdict_mi = "DOWNSTREAM_WIN_CONFIRMED"
        elif mi_joint_win:
            verdict_mi = "PARTIAL_WIN"
        else:
            verdict_mi = "AUDITABILITY_NO_BETTER_OUTCOME"

    logger.info(f"{el()} VERDICT {cs.case_id}: {verdict} (basis={primary_basis}; joint_win={joint_win} "
                f"collat_win={collat_win} fluency_win={fluency_win}) | MI-verdict={verdict_mi}")

    return {
        "family": cs.family, "target_subcontext": cs.X, "absorber_latent": int(cs.absorber),
        "parent_anchor": int(cs.anchor), "absorber_precision": cs.absorber_precision, "regime": cs.regime,
        "probe_train_auc": cs.probe.train_auc, "probe_cos_with_diffmean": cs.probe.cos_probe_dmu,
        "firing_jaccard_with_parent": cs.firing_jaccard, "parent_recall_hole": cs.parent_recall_hole,
        "matched_target_forget_kl": float(matched_target), "scale_kg_lambda": float(s_kg),
        "scale_dense_beta": float(s_de),
        "forget_kg_curve": forget_kg_curve.tolist(), "forget_dense_curve": forget_de_curve.tolist(),
        "forget_kg_footprints": foot_kg, "forget_dense_footprints": foot_de,
        "lam_grid": LAM_GRID, "beta_grid": BETA_GRID,
        "n_forget": len(gen["FORGET"]["prompts"]),
        "n_retain_collateral": len(retain_kl_kg),
        "retain_collateral_kl_kg_mean": float(retain_kl_kg.mean()),
        "retain_collateral_kl_dense_mean": float(retain_kl_de.mean()),
        "collateral_diff_CI": collateral_diff_CI,                # dense - kg retain KL (>0 => KG wins)
        "curve_dominance": dom,
        "judge_available": judge_available, "n_judged_preservation_pairs": n_judge,
        "primary_outcome_basis": primary_basis,
        "joint_diff_CI": joint_diff_CI, "fluency_diff_CI": fluency_diff_CI,
        "per_role_judge": per_role_judge, "judged_forget_confirmation": judged_forget,
        "kg_joint_utility_mean": float(np.mean(jk_joint)) if jk_joint else None,
        "dense_joint_utility_mean": float(np.mean(jd_joint)) if jd_joint else None,
        "model_internal_joint": {
            "collateral_diff_CI_genset": mi_collateral_diff_CI,
            "fluency_diff_CI_ppl": mi_fluency_diff_CI,
            "joint_diff_CI": mi_joint_diff_CI,
            "kg_genset_kl_mean": float(np.mean(mik_kl)) if mik_kl else None,
            "dense_genset_kl_mean": float(np.mean(mid_kl)) if mid_kl else None,
            "kg_cont_ppl_mean": float(np.mean(mik_ppl)) if mik_ppl else None,
            "dense_cont_ppl_mean": float(np.mean(mid_ppl)) if mid_ppl else None,
            "noop_cont_ppl_mean": float(np.mean(noop_ppls)) if noop_ppls else None,
            "verdict_model_internal": verdict_mi},
        "win_verdict": verdict,
    }


# =========================================================================== gating (reuse core funcs)
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
    geo = [r for r in tax_rows if r["metadata_row_type"] == "corpus"
           and r["metadata_sub_context"] == "Georgia"][:3]
    fra = [r for r in tax_rows if r["metadata_row_type"] == "corpus"
           and r["metadata_sub_context"] == "France"][:3]
    _, resid_s, _ = mb.encode_rows(geo + fra, sae)
    z = sae.encode(torch.tensor(resid_s.astype(np.float32), device=DEVICE))
    zg = float(z[:len(geo), 16009].mean()); zf = float(z[len(geo):, 16009].mean())
    locality_ok = bool(zg > zf)
    logger.info(f"{el()} SMOKE token-locality 16009: z(Georgia)={zg:.3f} z(France)={zf:.3f} ok={locality_ok}")
    # generation diff + footprint
    probe = ParentProbe(torch, resid_s[:len(geo)].astype(np.float32), resid_s[len(geo):].astype(np.float32))
    prompt = _prefix_before_span(geo[0]["input"], geo[0].get("_span"))
    base_c = generate_under_edit(mb, sae, [prompt], kind=None)[0]
    kg_c = generate_under_edit(mb, sae, [prompt], kind="abl_latent", l=16009, scale=2.0)[0]
    de_c = generate_under_edit(mb, sae, [prompt], kind="erase_dir", u=probe.u_t, scale=2.0)[0]
    kg_foot = side_effects(mb, sae, NEUTRAL_TEXT[:6], *base_distributions(mb, NEUTRAL_TEXT[:6]),
                           "abl_latent", l=16009, scale=1.0)["token_footprint"]
    de_foot = side_effects(mb, sae, NEUTRAL_TEXT[:6], *base_distributions(mb, NEUTRAL_TEXT[:6]),
                           "erase_dir", u=probe.u_t, scale=1.0)["token_footprint"]
    gen_diff = bool(kg_c != base_c or de_c != base_c)
    logger.info(f"{el()} SMOKE gen base='{base_c[:60]}' kg='{kg_c[:60]}' de='{de_c[:60]}'")
    logger.info(f"{el()} SMOKE footprint KG={kg_foot:.5f} DENSE={de_foot:.5f} gen_diff={gen_diff}")
    # one judge call
    jr = None
    if os.environ.get("OPENROUTER_API_KEY"):
        jr = judge_call({"role": "RETAIN", "X": "Georgia", "prompt": prompt,
                         "base_cont": base_c[:300], "edit_cont": de_c[:300]})
    logger.info(f"{el()} SMOKE judge result={jr} SPENT=${SPENT['usd']:.5f}")
    out["metadata"]["smoke"] = {
        "z_georgia_16009": zg, "z_france_16009": zf, "token_locality_ok": locality_ok,
        "gen_base": base_c[:120], "gen_kg": kg_c[:120], "gen_dense": de_c[:120], "gen_diff": gen_diff,
        "kg_footprint": kg_foot, "dense_footprint": de_foot, "footprint_kg_lt_dense": bool(kg_foot < de_foot),
        "judge_result": jr, "judge_spent_usd": SPENT["usd"], "judge_ok": bool(jr is not None)}
    out["datasets"] = [{"dataset": "smoke", "examples": [{"input": "smoke", "output": "ok",
                       "predict_kg_abl": kg_c[:80] or "EMPTY"}]}]
    assert gating["cosine"] > 0.85, "gating failed"
    assert locality_ok, "token locality failed (16009 not Georgia-specific)"
    assert gen_diff, "edit hooks did not change generation"
    assert kg_foot < de_foot, "KG footprint not < DENSE footprint"
    if os.environ.get("OPENROUTER_API_KEY"):
        assert jr is not None and jr["fluency"] in (0, 1, 2), "judge call/parse failed"
        assert SPENT["usd"] < 0.01, f"smoke judge cost too high ${SPENT['usd']}"
    logger.info(f"{el()} SMOKE PASS")


# =========================================================================== output assembly
def assemble_outputs(out, case_results):
    per_prompt = []
    per_case = []
    for (res, gen, mi, judged) in case_results:
        cid = res["case_id"]
        # DS1: one row per (case, gen prompt)
        for role in ("FORGET", "RETAIN", "UNRELATED"):
            g = gen[role]; m = mi.get(role, {})
            for j, p in enumerate(g["prompts"]):
                def js(op):
                    r = judged[role].get(op, [])
                    rr = r[j] if j < len(r) else None
                    return rr
                jk = js("KG-ABL"); jd = js("DENSE-ABL"); jrnd = js("RAND")
                row = {
                    "input": f"[{res['family']}|{role}|forget='{res['target_subcontext']}'] {p[:200]}",
                    "output": role,
                    "predict_kg_abl": (g["KG-ABL"][j][:160] or "EMPTY"),
                    "predict_dense_abl": (g["DENSE-ABL"][j][:160] or "EMPTY"),
                    "predict_rand": (g["RAND"][j][:160] or "EMPTY"),
                    "predict_noop": (g["NOOP"][j][:160] or "EMPTY"),
                    "metadata_case": cid, "metadata_role": role,
                    "metadata_absorber_latent": int(res["absorber_latent"]),
                    "metadata_regime": res["regime"],
                    "metadata_fluency_kg": (jk["fluency"] if jk else None),
                    "metadata_fluency_dense": (jd["fluency"] if jd else None),
                    "metadata_content_pres_kg": (jk["content_pres"] if jk else None),
                    "metadata_content_pres_dense": (jd["content_pres"] if jd else None),
                    "metadata_utility_kg": (round(harmonic_mean(jk["fluency"], jk["content_pres"]), 4) if jk else None),
                    "metadata_utility_dense": (round(harmonic_mean(jd["fluency"], jd["content_pres"]), 4) if jd else None),
                    "metadata_utility_rand": (round(harmonic_mean(jrnd["fluency"], jrnd["content_pres"]), 4) if jrnd else None),
                }
                if m:
                    row["metadata_mi_lastkl_kg"] = round(float(m["kl_kg"][j]), 6)
                    row["metadata_mi_lastkl_dense"] = round(float(m["kl_de"][j]), 6)
                    row["metadata_mi_contppl_kg"] = (round(float(m["ppl_kg"][j]), 3)
                                                     if np.isfinite(m["ppl_kg"][j]) else None)
                    row["metadata_mi_contppl_dense"] = (round(float(m["ppl_de"][j]), 3)
                                                        if np.isfinite(m["ppl_de"][j]) else None)
                per_prompt.append(row)
        # DS2: one row per case
        regime = res["regime"]
        expected = "WIN_EXPECTED" if regime == "absorption" else "LOSS_EXPECTED"
        cj = res.get("collateral_diff_CI") or {}
        jj = res.get("joint_diff_CI") or {}
        per_case.append({
            "input": (f"{res['family']} | selectively UNLEARN sub-context '{res['target_subcontext']}' by "
                      f"ablating KG-named absorber {res['absorber_latent']} ({regime}); KG-ABL vs DENSE-ABL "
                      f"(baseline f) at MATCHED forget-quality on a joint retain-quality x fluency outcome"),
            "output": expected,
            "predict_kg_abl": res["win_verdict"],
            "predict_dense_abl": (f"joint_util={res.get('dense_joint_utility_mean')}"
                                  if res.get("dense_joint_utility_mean") is not None
                                  else f"retain_KL={res.get('retain_collateral_kl_dense_mean'):.5f}"),
            "predict_model_internal": res["model_internal_joint"]["verdict_model_internal"],
            "metadata_case": res["case_id"], "metadata_regime": regime,
            "metadata_scale_kg_lambda": round(res["scale_kg_lambda"], 4),
            "metadata_scale_dense_beta": round(res["scale_dense_beta"], 4),
            "metadata_matched_target_forget_kl": round(res["matched_target_forget_kl"], 6),
            "metadata_collateral_diff_ci_lo": cj.get("ci_lo"), "metadata_collateral_diff_ci_hi": cj.get("ci_hi"),
            "metadata_collateral_diff_excl0": cj.get("excl_0"),
            "metadata_joint_diff": jj.get("diff"), "metadata_joint_diff_ci_lo": jj.get("ci_lo"),
            "metadata_joint_diff_ci_hi": jj.get("ci_hi"), "metadata_joint_diff_excl0": jj.get("excl_0"),
            "metadata_kg_joint_utility": res.get("kg_joint_utility_mean"),
            "metadata_dense_joint_utility": res.get("dense_joint_utility_mean"),
            "metadata_curve_dominance_fraction": res["curve_dominance"]["dominance_fraction"],
            "metadata_firing_jaccard_with_parent": res["firing_jaccard_with_parent"],
            "metadata_parent_recall_hole": res["parent_recall_hole"],
            "metadata_primary_basis": res["primary_outcome_basis"],
        })
    if not per_prompt:
        per_prompt = [{"input": "none", "output": "NONE", "predict_kg_abl": "NONE"}]
    if not per_case:
        per_case = [{"input": "none", "output": "NONE", "predict_kg_abl": "NONE"}]
    out["datasets"] = [
        {"dataset": "unlearn_per_prompt", "examples": per_prompt},
        {"dataset": "kg_vs_dense_per_case", "examples": per_case},
    ]


# =========================================================================== MAIN
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default="taxonomic_georgia,first_letter_large,toxicity_insult")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--cap", type=int, default=0, help="cap contexts per sub-context/fold (0=all)")
    ap.add_argument("--gen_per_set", type=int, default=20)
    ap.add_argument("--forget_cap", type=int, default=40)
    ap.add_argument("--retain_collat_cap", type=int, default=150)
    ap.add_argument("--retain_curve_cap", type=int, default=60)
    ap.add_argument("--unrel_curve_cap", type=int, default=40)
    ap.add_argument("--no_judge", action="store_true")
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
        "method_name": "M1 KG-Localized Single-Absorber Unlearning vs Dense Parent Erasure (joint collateral+fluency)",
        "description": ("At MATCHED forget-quality, ablate ONE KG-named absorber latent (KG-ABL) vs erase the "
                        "dense diff-of-means parent direction (DENSE-ABL, baseline f). WIN <=> KG-ABL has lower "
                        "sibling/parent collateral AND better fluency on a joint retain-quality x fluency outcome, "
                        "with a paired-bootstrap KG-minus-dense CI excluding 0. Toxicity insult co-firing case is "
                        "the honest negative pole (KG predicted to lose, router-consistent)."),
        "sae": {"release": RELEASE_REPO, "sae_params": SAE_PARAMS_16K, "width": int(sae.d_sae),
                "d_model": int(sae.d_model), "hook": f"blocks.{HOOK_LAYER}.hook_resid_post"},
        "model": mb.model_id, "seed": SEED, "B_boot": B_BOOT, "Rnorm": Rnorm,
        "gating_check": gating,
        "forget_grids": {"LAM_GRID": LAM_GRID, "BETA_GRID": BETA_GRID},
        "judge": {"model": MODEL_JUDGE, "temp": JUDGE_TEMP, "target_usd": TARGET, "hard_cap_usd": HARD_CAP},
        "canonical_units_used": {
            "taxonomic_anchor": canon["taxonomic"]["anchor"],
            "georgia_absorber": 16009, "first_letter_L_anchor": canon["first_letter"]["L"]["anchor"],
            "large_absorber": 8463},
    }, "datasets": []}

    if args.smoke:
        run_smoke(torch, sae, mb, canon, gating, tax_rows, out)
        out["metadata"]["judge"]["spent_usd"] = SPENT["usd"]
        out["metadata"]["judge"]["n_calls"] = SPENT["calls"]
        save_json(out, args.out)
        logger.info(f"{el()} SMOKE saved -> {args.out}")
        return

    requested = [c.strip() for c in args.cases.split(",") if c.strip()]
    setup_fns = {
        "taxonomic_georgia": lambda *a: setup_taxonomic(*a, target=("Georgia", 16009, 0.955),
                                                        case_id="taxonomic_georgia"),
        "taxonomic_us": lambda *a: setup_taxonomic(*a, target=("United States", 846, 0.973),
                                                   case_id="taxonomic_us"),
        "taxonomic_jordan": lambda *a: setup_taxonomic(*a, target=("Jordan", 540, 0.975),
                                                       case_id="taxonomic_jordan"),
        "first_letter_large": setup_first_letter,
        "toxicity_insult": setup_toxicity}
    case_results = []
    summaries = []
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
        res, gen, mi, judged = run_unlearning_case(torch, sae, mb, cs, args, do_judge=(not args.no_judge))
        case_results.append((res, gen, mi, judged))
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
    wins = [r for r in abs_cases if r["win_verdict"] == "DOWNSTREAM_WIN_CONFIRMED"]
    partial = [r for r in abs_cases if r["win_verdict"] == "PARTIAL_WIN"]
    no_better = [r for r in abs_cases if r["win_verdict"] == "AUDITABILITY_NO_BETTER_OUTCOME"]
    cof = [r for r in summaries if r["regime"] == "co-firing"]
    summary = {
        "n_cases": len(summaries), "n_absorption": len(abs_cases),
        "n_downstream_win_confirmed": len(wins),
        "win_cases": [r["case_id"] for r in wins],
        "partial_win_cases": [r["case_id"] for r in partial],
        "no_better_outcome_cases": [r["case_id"] for r in no_better],
        "m1_gate_passed": bool(len(wins) >= 1),
        "cofiring_cases": [{"case_id": r["case_id"], "verdict": r["win_verdict"],
                            "firing_jaccard": r["firing_jaccard_with_parent"],
                            "parent_recall_hole": r["parent_recall_hole"]} for r in cof],
        "per_case_verdicts": [{"case_id": r["case_id"], "verdict": r["win_verdict"],
                               "verdict_model_internal": r["model_internal_joint"]["verdict_model_internal"],
                               "joint_diff_CI": r["joint_diff_CI"],
                               "collateral_diff_CI": r["collateral_diff_CI"],
                               "fluency_diff_CI": r["fluency_diff_CI"],
                               "curve_dominance_fraction": r["curve_dominance"]["dominance_fraction"]}
                              for r in summaries],
    }
    # honest negatives
    honest = []
    if not wins:
        honest.append("NO absorption case cleared the M1 win gate on the LLM-judge joint outcome: "
                      "localization buys auditability/editability but did not beat the dense baseline on "
                      "the joint retain-quality x fluency outcome at matched forget (HEADLINE LIMITATION).")
    for r in summaries:
        v = r["win_verdict"]
        if v == "AUDITABILITY_NO_BETTER_OUTCOME":
            honest.append(f"{r['case_id']}: AUDITABILITY_NO_BETTER_OUTCOME — at matched forget the dense parent "
                          f"erasure matched/beat KG on the joint outcome (joint CI incl 0 or favors dense). "
                          f"Model-internal collateral favored KG={r['collateral_diff_CI'].get('excl_0')}, "
                          f"curve-dominance={r['curve_dominance']['dominance_fraction']:.2f}.")
        elif v == "PARTIAL_WIN":
            honest.append(f"{r['case_id']}: PARTIAL_WIN — joint CI excludes 0 favoring KG but not both "
                          f"sub-dimensions (collateral / fluency) are individually significant.")
        elif v == "EXPECTED_LOSS_ROUTER_CONSISTENT":
            honest.append(f"{r['case_id']}: EXPECTED_LOSS_ROUTER_CONSISTENT — co-firing regime (firing-Jaccard "
                          f"{r['firing_jaccard_with_parent']}, parent recall-hole {r['parent_recall_hole']}); "
                          f"single-latent ablation is NOT a clean handle, dense is the right tool — predicted in advance.")
        elif v in ("LOSS_NOT_ROUTER_FLAGGED", "UNEXPECTED_WIN"):
            honest.append(f"{r['case_id']}: {v} — reported verbatim (not predicted by the router).")
    if all(r.get("judge_available") for r in summaries) is False:
        honest.append("Some/all cases fell back to the model-internal joint (PPL + retain-KL) because the LLM "
                      "judge was budget-limited or unavailable; the win claim then rests on PPL+KL with the "
                      "judge as corroboration where present (substitution stated explicitly).")

    out["metadata"]["judge"]["spent_usd"] = SPENT["usd"]
    out["metadata"]["judge"]["n_calls"] = SPENT["calls"]
    out["metadata"]["judge"]["n_fail"] = SPENT["fail"]
    out["metadata"]["judge"]["n_refusal_or_parsefail"] = SPENT["refusal"]
    out["metadata"]["per_case"] = summaries
    out["metadata"]["summary"] = summary
    out["metadata"]["honest_negatives"] = honest

    assemble_outputs(out, case_results)
    save_json(out, args.out)
    logger.info(f"{el()} SAVED {args.out}")
    logger.info(f"{el()} SUMMARY: n_cases={len(summaries)} wins={len(wins)} "
                f"m1_gate={summary['m1_gate_passed']} judge_spent=${SPENT['usd']:.4f}")
    for r in summaries:
        logger.info(f"  {r['case_id']}: {r['win_verdict']} | MI={r['model_internal_joint']['verdict_model_internal']} "
                    f"| collat_excl0={r['collateral_diff_CI'].get('excl_0')} "
                    f"| dom={r['curve_dominance']['dominance_fraction']:.2f}")


if __name__ == "__main__":
    main()
