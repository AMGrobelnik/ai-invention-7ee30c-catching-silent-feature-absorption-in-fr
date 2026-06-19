#!/usr/bin/env python
"""
Two-Track CCRG on first-letter spelling (PRIMARY FALSIFICATION ENDPOINT) — experiment_iter2_dir1.

Runs the two-track Counterfactual Co-Response Grouping pipeline on a FROZEN Gemma Scope
layer-12 / width-16k JumpReLU SAE over the pre-built first-letter spelling testbed, and decides:

  E1 (Tier-0)  : does the K-track anchored greedy set-cover, given ONLY content-flip pairs,
                 recover the form-free-diagnostic parent + >=2 per-token absorbers above a
                 random-membership null (with anchor-fidelity + threshold sweep)?
  E2 / C3      : does the co-response UNIT beat count-matched baselines (g)/(h)/(b)/(c) on
                 recovered-absorber count AND sliced recall over absorbed sub-contexts?
  C1           : does the pooled-max unit beat (a)/(b)/(c)/(h) on starts-with-L classification?
  Admission    : Step-5 rule (sigC OR sigK) AND surface-invariance, with BH/Holm multiplicity.
  Steering     : mean-member-decoder direction moves starts-with-L mass at MATCHED on-target
                 effect with LOWER full-vocab-KL + PPL collateral than non-SAE diff-of-means
                 and a hub/best-single-latent control.

Model loaded with plain `transformers`; SAE loaded directly from Gemma Scope npz (JumpReLU),
to avoid sae_lens/transformer_lens version conflicts. Core LLM spend = $0.

Usage:
  uv run method.py --smoke                 # stage 0: load + reconstruction gating check only
  uv run method.py --letters L --mini      # stage 1: mini pilot on L
  uv run method.py --letters L             # stage 2: full L through steering
  uv run method.py                         # full run: L,O,T,I,D + steering
"""
import os, sys, json, time, argparse, gc, math, hashlib, warnings
from collections import defaultdict, Counter

import numpy as np

warnings.filterwarnings("ignore")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "0")

# ----------------------------------------------------------------------------- CONFIG
RELEASE_REPO = "google/gemma-scope-2b-pt-res"
SAE_PARAMS_16K = "layer_12/width_16k/average_l0_82/params.npz"   # 'canonical' = avg L0 nearest 100
SAE_PARAMS_65K = "layer_12/width_65k/average_l0_72/params.npz"   # fallback (more features)
MODEL_ID = "unsloth/gemma-2-2b"            # non-gated mirror, vocab 256000
HOOK_LAYER = 12                            # output of decoder layer 12 == blocks.12.hook_resid_post

LETTERS_ALL = ["L", "O", "T", "I", "D"]
PRIMARY = "L"
SPELLING_CARRIERS = ["t_verbose", "t_colon", "t_icl"]   # documented-absorption substrate (Chanin VERBOSE)

BETA = 6                                    # WGCNA/DiffCoEx signed soft-threshold
GAMMA_GRID = [0.3, 0.5, 0.7, 1.0, 1.5]
PREC_FLOOR = 0.7
JACCARD_MAX = 0.1
COVGAIN_FLOOR = 0.05      # plan reference floor (used in threshold sweep); headline uses min_hole=1 (word-level absorption)
MAX_K = 15               # cap on unit size (anchor + absorbers)
MIN_HOLE_HEADLINE = 1    # an absorber must cover >=1 NEW hole sub-context (first-letter absorbers are word-sparse)
ANCHOR_CORPUS_FIRE_FLOOR = 0.05   # M4 (iter-4): a valid parent anchor must fire on >=5% of held-out corpus
                                  #     windows. Rejects the iter-3 I=1227 recall-argmax anchor (fires 0% on
                                  #     corpus = spurious content-flip-only anchor; not a real parent feature).
COMPACT_MAX = 5          # M7 (iter-4): compact named unit = anchor + up to (COMPACT_MAX-1) corroborated absorbers
TAU_C = 0.5                                 # form-free absorption-fraction threshold
PROBE_ACC_FLOOR = 0.8
PARENT_RECALL_FLOOR = 0.60

STEER_C = [0.0, 0.5, 1.0, 2.0, 4.0, 8.0]
SEED = 1234

DEVICE = "cuda"
DTYPE = None  # set after torch import

# ----------------------------------------------------------------------------- logging
def log(msg):
    t = time.strftime("%H:%M:%S")
    print(f"[{t}] {msg}", flush=True)

T0 = time.time()
def el():
    return f"{time.time()-T0:6.1f}s"

# ============================================================================ SAE
class JumpReLUSAE:
    """Gemma Scope JumpReLU SAE loaded directly from params.npz (official forward)."""
    def __init__(self, params, device, torch):
        self.torch = torch
        self.W_enc = torch.tensor(np.asarray(params["W_enc"]), device=device, dtype=torch.float32)  # [d_model, d_sae]
        self.W_dec = torch.tensor(np.asarray(params["W_dec"]), device=device, dtype=torch.float32)  # [d_sae, d_model]
        self.threshold = torch.tensor(np.asarray(params["threshold"]), device=device, dtype=torch.float32)  # [d_sae]
        self.b_enc = torch.tensor(np.asarray(params["b_enc"]), device=device, dtype=torch.float32)  # [d_sae]
        self.b_dec = torch.tensor(np.asarray(params["b_dec"]), device=device, dtype=torch.float32)  # [d_model]
        self.d_model = self.W_dec.shape[1]
        self.d_sae = self.W_dec.shape[0]

    def encode(self, x):
        t = self.torch
        x = x.to(t.float32)
        pre = x @ self.W_enc + self.b_enc
        acts = (pre > self.threshold) * t.nn.functional.relu(pre)
        return acts

    def decode(self, z):
        return z @ self.W_dec + self.b_dec


def load_sae(params_file):
    from huggingface_hub import hf_hub_download
    import torch
    path = hf_hub_download(repo_id=RELEASE_REPO, filename=params_file, token=os.environ.get("HF_TOKEN"))
    params = np.load(path)
    sae = JumpReLUSAE(params, DEVICE, torch)
    log(f"{el()} SAE loaded {params_file}: W_dec={tuple(sae.W_dec.shape)} W_enc={tuple(sae.W_enc.shape)} "
        f"d_sae={sae.d_sae} d_model={sae.d_model}")
    return sae

# ============================================================================ MODEL
class ModelBundle:
    def __init__(self):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        global DTYPE
        DTYPE = torch.bfloat16
        log(f"{el()} loading tokenizer {MODEL_ID}")
        self.tok = AutoTokenizer.from_pretrained(MODEL_ID, token=os.environ.get("HF_TOKEN"))
        self.tok.padding_side = "right"
        log(f"{el()} loading model {MODEL_ID} (bf16, eager attn)")
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID, torch_dtype=DTYPE, device_map=DEVICE,
            attn_implementation="eager", token=os.environ.get("HF_TOKEN"),
        ).eval()
        self.torch = torch
        self.layer = self.model.model.layers[HOOK_LAYER]
        self._captured = {}
        self.d_model = self.model.config.hidden_size
        log(f"{el()} model loaded d_model={self.d_model} n_layers={self.model.config.num_hidden_layers} "
            f"vocab={len(self.tok)}")

    def _hook(self, mod, inp, out):
        h = out[0] if isinstance(out, (tuple, list)) else out
        self._captured["h"] = h

    def resid_at_spans(self, inputs, spans, batch_size=48, check_token_ids=None):
        """Return residual at layer HOOK_LAYER for the token covering each char-span. [n, d_model] float32 cpu numpy."""
        torch = self.torch
        out = np.zeros((len(inputs), self.d_model), dtype=np.float32)
        miss = 0
        idmismatch = 0
        handle = self.layer.register_forward_hook(self._hook)
        try:
            for b0 in range(0, len(inputs), batch_size):
                bi = inputs[b0:b0 + batch_size]
                bs = spans[b0:b0 + batch_size]
                enc = self.tok(bi, return_offsets_mapping=True, return_tensors="pt",
                               padding=True, truncation=True, max_length=128, add_special_tokens=True)
                offs = enc.pop("offset_mapping")
                ids = enc["input_ids"]
                enc = {k: v.to(DEVICE) for k, v in enc.items()}
                with torch.no_grad():
                    self.model(**enc)
                h = self._captured["h"].to(torch.float32)  # [B,S,d]
                for j in range(len(bi)):
                    tidx = _find_token_idx(offs[j].tolist(), bs[j])
                    if tidx < 0:
                        miss += 1
                        tidx = 1  # fallback first content token
                    out[b0 + j] = h[j, tidx].cpu().numpy()
                    if check_token_ids is not None:
                        if int(ids[j, tidx]) != int(check_token_ids[b0 + j]):
                            idmismatch += 1
        finally:
            handle.remove()
        if miss:
            log(f"  [resid] {miss}/{len(inputs)} spans had no token match (fallback used)")
        if check_token_ids is not None:
            log(f"  [resid] token-id mismatches: {idmismatch}/{len(inputs)}")
        return out

    def mean_resid_norm(self, sample_inputs, batch_size=32):
        torch = self.torch
        handle = self.layer.register_forward_hook(self._hook)
        norms = []
        try:
            for b0 in range(0, len(sample_inputs), batch_size):
                bi = sample_inputs[b0:b0 + batch_size]
                enc = self.tok(bi, return_tensors="pt", padding=True, truncation=True,
                               max_length=64, add_special_tokens=True)
                am = enc["attention_mask"]
                enc = {k: v.to(DEVICE) for k, v in enc.items()}
                with torch.no_grad():
                    self.model(**enc)
                h = self._captured["h"].to(torch.float32)
                m = am.to(DEVICE).unsqueeze(-1)
                n = (h.norm(dim=-1) * am.to(DEVICE)).sum() / am.to(DEVICE).sum()
                norms.append(float(n))
        finally:
            handle.remove()
        return float(np.mean(norms))


def _find_token_idx(offsets, span):
    s, e = span
    best, best_ov = -1, 0
    for i, (a, b) in enumerate(offsets):
        if b <= a:
            continue
        ov = max(0, min(b, e) - max(a, s))
        if ov > best_ov:
            best_ov, best = ov, i
    return best

# ============================================================================ DATA
def load_data(path):
    with open(path) as f:
        d = json.load(f)
    groups = {}
    for g in d["datasets"]:
        letter = g["dataset"].split("_")[-1]
        groups[letter] = g["examples"]
    return d.get("metadata", {}), groups


def build_letter_struct(rows, carriers):
    """Organize one letter's rows into content pairs / surface pairs / corpus, filtered to `carriers`."""
    content = defaultdict(dict)   # pair_id -> {'on':row,'off':row}
    surface = defaultdict(dict)   # pair_id -> {'var_a':row,'var_b':row}
    corpus = []
    for r in rows:
        pt = r.get("metadata_pair_type")
        if pt == "content_flip":
            if r.get("metadata_template_id") in carriers:
                content[r["metadata_pair_id"]][r["metadata_role"]] = r
        elif pt == "surface_flip":
            if r.get("metadata_template_id") in carriers:
                surface[r["metadata_pair_id"]][r["metadata_role"]] = r
        elif pt == "corpus_context":
            corpus.append(r)
    content = {k: v for k, v in content.items() if "on" in v and "off" in v}
    surface = {k: v for k, v in surface.items() if "var_a" in v and "var_b" in v}
    return content, surface, corpus

# ============================================================================ STATS
def auc(scores, labels):
    from sklearn.metrics import roc_auc_score
    labels = np.asarray(labels)
    if labels.min() == labels.max():
        return 0.5
    try:
        return float(roc_auc_score(labels, scores))
    except Exception:
        return 0.5


def best_f1_threshold(scores, labels):
    """Return threshold maximizing F1 on (scores,labels)."""
    s = np.asarray(scores); y = np.asarray(labels)
    order = np.argsort(-s)
    cand = np.unique(s)
    if len(cand) > 200:
        cand = np.quantile(s, np.linspace(0, 1, 200))
    best_t, best_f = 0.0, -1
    P = y.sum()
    for t in cand:
        pred = s >= t
        tp = np.sum(pred & (y == 1))
        fp = np.sum(pred & (y == 0))
        fn = P - tp
        f = tp / (tp + 0.5 * (fp + fn) + 1e-9)
        if f > best_f:
            best_f, best_t = f, t
    return float(best_t)


def f1_at(scores, labels, t):
    s = np.asarray(scores); y = np.asarray(labels)
    pred = s >= t
    tp = np.sum(pred & (y == 1)); fp = np.sum(pred & (y == 0)); fn = np.sum((~pred) & (y == 1))
    return float(tp / (tp + 0.5 * (fp + fn) + 1e-9))


def paired_bootstrap_diff(a, b, B=10000, rng=None):
    """CI on mean(a)-mean(b), paired (same indices). a,b arrays of per-example values."""
    a = np.asarray(a, float); b = np.asarray(b, float)
    n = len(a)
    if n == 0:
        return {"diff": 0.0, "ci_lo": 0.0, "ci_hi": 0.0, "excl_0": False, "n": 0}
    rng = rng or np.random.default_rng(SEED)
    idx = rng.integers(0, n, size=(B, n))
    d = a[idx].mean(1) - b[idx].mean(1)
    lo, hi = np.percentile(d, [2.5, 97.5])
    return {"diff": float(a.mean() - b.mean()), "ci_lo": float(lo), "ci_hi": float(hi),
            "excl_0": bool(lo > 0 or hi < 0), "n": int(n)}


def mcnemar_p(correct_a, correct_b):
    """Exact McNemar on paired binary correctness vectors."""
    from statsmodels.stats.contingency_tables import mcnemar
    a = np.asarray(correct_a).astype(bool); b = np.asarray(correct_b).astype(bool)
    n01 = int(np.sum(a & ~b)); n10 = int(np.sum(~a & b))
    table = [[int(np.sum(a & b)), n01], [n10, int(np.sum(~a & ~b))]]
    try:
        res = mcnemar(table, exact=True)
        return float(res.pvalue), n01, n10
    except Exception:
        return 1.0, n01, n10


def holm(pvals):
    from statsmodels.stats.multitest import multipletests
    if not pvals:
        return [], []
    rej, p_adj, _, _ = multipletests(pvals, method="holm")
    return [bool(x) for x in rej], [float(x) for x in p_adj]


def bh(pvals):
    from statsmodels.stats.multitest import multipletests
    if not pvals:
        return [], []
    rej, p_adj, _, _ = multipletests(pvals, method="fdr_bh")
    return [bool(x) for x in rej], [float(x) for x in p_adj]


def jaccard(set_a, set_b):
    a, b = set(set_a), set(set_b)
    if not a and not b:
        return 0.0
    return len(a & b) / max(1, len(a | b))


def spearman_mat(X):
    """Spearman correlation matrix among ROWS of X (variables=rows). Robust for L==2 (scipy returns
    a scalar there); uses rank + Pearson. Constant rows -> 0 correlation."""
    X = np.asarray(X, dtype=np.float64)
    L = X.shape[0]
    if L < 2:
        return np.ones((L, L))
    Rk = np.argsort(np.argsort(X, axis=1), axis=1).astype(np.float64)
    C = np.corrcoef(Rk)
    C = np.atleast_2d(C)
    if C.shape != (L, L):
        C = np.eye(L)
    return np.nan_to_num(C, nan=0.0)

# ============================================================================ M-FIXES HELPERS (iter-3)
# M1 = RANDOM-ELIGIBLE-k pool baseline; M2 = AUC points + AUC-difference CIs; M3 = verdict reconciliation.
def fast_auc(scores, labels):
    """Tie-aware AUC via Mann-Whitney U with AVERAGE ranks. Equals sklearn roc_auc_score but faster and
    explicitly tie-correct: SAE max-pool produces many exact-0 ties on off-instances; naive ranks are wrong."""
    from scipy.stats import rankdata
    y = np.asarray(labels)
    s = np.asarray(scores, dtype=np.float64)
    n_pos = float((y == 1).sum()); n_neg = float(len(y) - n_pos)
    if n_pos == 0 or n_neg == 0:
        return 0.5
    r = rankdata(s)
    return float((r[y == 1].sum() - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg))


def youden_threshold(scores, labels):
    """Threshold maximizing Youden's J = TPR - FPR. A comparison-matched operating point that does NOT
    collapse to predict-all-positive (unlike F1-optimal on weak detectors with many exact-0 off scores)."""
    s = np.asarray(scores, dtype=np.float64); y = np.asarray(labels)
    cand = np.unique(s)
    if len(cand) > 400:
        cand = np.quantile(s, np.linspace(0, 1, 400))
    P = max(1.0, float((y == 1).sum())); N = max(1.0, float((y == 0).sum()))
    bestJ, bestt = -2.0, float(cand[0])
    for t in cand:
        pred = s >= t
        tpr = float(np.sum(pred & (y == 1))) / P
        fpr = float(np.sum(pred & (y == 0))) / N
        J = tpr - fpr
        if J > bestJ:
            bestJ, bestt = J, float(t)
    return bestt


def bootstrap_auc_diff(s_unit, s_x, n_pairs, pair_pool, B=10000, rng=None, keep_diffs=False):
    """CI on the AUC DIFFERENCE auc(unit) - auc(x) on the HELD-OUT TEST fold, resampling whole
    content-flip pairs with replacement (cluster = pair: on-instance at idx p, off-instance at idx p+n_pairs).
    Resampling whole pairs keeps the 50/50 balance and respects the minimal-pair structure. Labels are
    FIXED (n_test ones then n_test zeros) so only the scores resample. B>=10,000 for the reported run.
    The point auc_unit equals C1 per_method[..]['AUC'] (same held-out test instances)."""
    rng = rng or np.random.default_rng(SEED)
    pair_pool = np.asarray(pair_pool, dtype=np.int64)
    npt = int(len(pair_pool))
    su = np.asarray(s_unit); sx = np.asarray(s_x)
    if npt < 2:
        return {"auc_unit": 0.5, "auc_x": 0.5, "diff": 0.0, "ci_lo": 0.0, "ci_hi": 0.0,
                "excl_0": False, "sig_unit_better": False, "se": 0.0,
                "n_test_pairs": npt, "B": int(B), "_diffs": (np.zeros(B) if keep_diffs else None)}
    y = np.concatenate([np.ones(npt), np.zeros(npt)])
    base_idx = np.concatenate([pair_pool, pair_pool + n_pairs])
    au = fast_auc(su[base_idx], y); ax = fast_auc(sx[base_idx], y)
    point = au - ax
    diffs = np.empty(B, dtype=np.float64)
    for b in range(B):
        draw = pair_pool[rng.integers(0, npt, npt)]
        idx = np.concatenate([draw, draw + n_pairs])
        diffs[b] = fast_auc(su[idx], y) - fast_auc(sx[idx], y)
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    return {"auc_unit": float(au), "auc_x": float(ax), "diff": float(point),
            "ci_lo": float(lo), "ci_hi": float(hi),
            "excl_0": bool(lo > 0 or hi < 0), "sig_unit_better": bool(lo > 0),
            "se": float(diffs.std()), "n_test_pairs": npt, "B": int(B),
            "_diffs": (diffs if keep_diffs else None)}


def rek_pool(letter, Lr, k, a_on_Lr, a_off_Lr, labels, n_pairs, test_mask, B_draws, rng):
    """RANDOM-ELIGIBLE-k baseline (M1, decisive). Draw k latents UNIFORMLY AT RANDOM from the
    cover-eligible set E = Lr, max-pool them (identical pooling rule to unit/h/b/c) -> the ONLY varying
    factor vs the two-track unit is the membership/SELECTION criterion. Returns the draw-AUC distribution
    on the test fold + a FROZEN median-AUC comparator draw used everywhere downstream."""
    Lr_local = {int(g): i for i, g in enumerate(Lr.tolist())}
    kk = int(min(k, len(Lr)))
    if kk < k:
        log(f"  [REk] {letter}: |Lr|={len(Lr)} < k={k}; drawing {kk}")
    aucs = np.empty(B_draws, dtype=np.float64)
    member_lists = []
    score_cache = []
    for d in range(B_draws):
        draw_global = rng.choice(Lr, size=kk, replace=False)
        cols = [Lr_local[int(g)] for g in draw_global]
        son = a_on_Lr[:, cols].max(1); soff = a_off_Lr[:, cols].max(1)
        s_all = np.concatenate([son, soff])
        aucs[d] = fast_auc(s_all[test_mask], labels[test_mask])
        member_lists.append([int(g) for g in draw_global])
        score_cache.append(s_all)
    median_i = int(np.argsort(aucs)[len(aucs) // 2])      # fixed median-AUC comparator draw
    return {"draw_auc_mean": float(aucs.mean()), "draw_auc_p05": float(np.percentile(aucs, 5)),
            "draw_auc_p50": float(np.percentile(aucs, 50)), "draw_auc_p95": float(np.percentile(aucs, 95)),
            "draw_auc_max": float(aucs.max()), "draw_auc_min": float(aucs.min()),
            "B_draws": int(B_draws), "k": kk,
            "median_draw_members": member_lists[median_i],
            "median_draw_scores": score_cache[median_i], "all_draw_aucs": aucs}

# ============================================================================ ENCODING HELPERS
def sae_encode_np(sae, h_np, torch, batch=512, keep_latents=None):
    """Encode residuals h_np [n,d] -> activations. If keep_latents given, returns [n, len(keep)] else [n,d_sae]."""
    n = h_np.shape[0]
    if keep_latents is not None:
        out = np.zeros((n, len(keep_latents)), dtype=np.float32)
        kl = torch.tensor(keep_latents, device=DEVICE, dtype=torch.long)
    else:
        out = np.zeros((n, sae.d_sae), dtype=np.float32)
    for b0 in range(0, n, batch):
        hb = torch.tensor(h_np[b0:b0 + batch], device=DEVICE, dtype=torch.float32)
        z = sae.encode(hb)
        if keep_latents is not None:
            z = z.index_select(1, kl)
        out[b0:b0 + batch] = z.cpu().numpy()
        del hb, z
    return out

# ============================================================================ PER-LETTER PIPELINE
def run_letter(letter, rows, mb, sae, h_corpus_all, corpus_rows_all, cfg, rng,
               surface_override=None, pooled_store=None):
    """Full pipeline for one letter. Returns a result dict."""
    torch = mb.torch
    R = {"letter": letter}
    log(f"\n===== LETTER {letter} =====")
    content, surface, corpus = build_letter_struct(rows, SPELLING_CARRIERS)
    if surface_override is not None:
        # STEP 7: use the enlarged independently-judged first-letter surface superset for the admission
        # shuffled-surface null (decisive C1/E2/RE-k results do NOT depend on admission).
        surface = surface_override
        R["surface_source"] = "iter2_superset"
    else:
        R["surface_source"] = "iter1_inline"
    log(f"{el()} {letter}: content pairs={len(content)} surface pairs={len(surface)} corpus={len(corpus)}")

    # ---- gather content-flip instances (spelling carriers) ----
    pair_ids = sorted(content.keys())
    if cfg["mini"]:
        # restrict to a handful of on-words, t_verbose only, for smoke
        onwords_seen = []
        keep = []
        for pid in pair_ids:
            w = content[pid]["on"]["metadata_target_word"]
            if content[pid]["on"]["metadata_template_id"] != "t_verbose":
                continue
            if w not in onwords_seen:
                if len(onwords_seen) >= cfg["mini_words"]:
                    continue
                onwords_seen.append(w)
            keep.append(pid)
        pair_ids = keep
        log(f"{el()} MINI: {len(pair_ids)} pairs over {len(onwords_seen)} on-words")

    on_inputs, on_spans, on_words, on_folds, off_inputs, off_spans, off_words = [], [], [], [], [], [], []
    for pid in pair_ids:
        on, off = content[pid]["on"], content[pid]["off"]
        on_inputs.append(on["input"]); on_spans.append(tuple(on["metadata_word_char_span"]))
        on_words.append(on["metadata_target_word"]); on_folds.append(int(on["metadata_fold"]))
        off_inputs.append(off["input"]); off_spans.append(tuple(off["metadata_word_char_span"]))
        off_words.append(off["metadata_target_word"])

    log(f"{el()} encoding {len(on_inputs)} on + {len(off_inputs)} off content instances")
    h_on = mb.resid_at_spans(on_inputs, on_spans)
    h_off = mb.resid_at_spans(off_inputs, off_spans)
    a_on = sae_encode_np(sae, h_on, torch)   # [n_pairs, d_sae]
    a_off = sae_encode_np(sae, h_off, torch)
    n_pairs = a_on.shape[0]
    d_sae = sae.d_sae
    r_pair = a_on - a_off                     # [n_pairs, d_sae]

    on_words_arr = np.array(on_words)
    uwords = sorted(set(on_words))
    w_index = {w: i for i, w in enumerate(uwords)}
    n_words = len(uwords)
    # group membership matrix G [n_words, n_pairs] row-normalized
    G = np.zeros((n_words, n_pairs), dtype=np.float32)
    for p, w in enumerate(on_words):
        G[w_index[w], p] = 1.0
    G /= np.maximum(G.sum(1, keepdims=True), 1)
    Rmat = (G @ r_pair).T                     # [d_sae, n_words]  word-level mean response

    # ---- content responsiveness + per-latent stats over ALL latents ----
    # per-latent mean-over-words response (broad responders) + per-latent sign-flip null cover threshold
    c_p = np.zeros(n_pairs, dtype=np.float32)
    wcount = Counter(on_words)
    for p, w in enumerate(on_words):
        c_p[p] = 1.0 / (n_words * wcount[w])
    real_stat = r_pair.T @ c_p                # [d_sae] mean-over-words response
    B_null = cfg["b_null"]
    signs = rng.choice([-1.0, 1.0], size=(n_pairs, B_null)).astype(np.float32)
    null_stat = (r_pair.T @ (c_p[:, None] * signs))  # [d_sae, B_null]
    tau_resp = np.maximum(1e-8, np.percentile(null_stat, 95, axis=1))   # per-latent cover threshold
    mean_responsive = np.where(real_stat > tau_resp)[0]                 # broad responders (reported only)

    # instance-level precision (fires on L on-words, not surface-matched off-words) for ALL latents
    fire_on_all = (a_on > 0); fire_off_all = (a_off > 0)
    on_cnt = fire_on_all.sum(0).astype(np.float64); off_cnt = fire_off_all.sum(0).astype(np.float64)
    precision_all = np.where((on_cnt + off_cnt) > 0, on_cnt / np.maximum(on_cnt + off_cnt, 1), 0.0)
    # word-level firing sets (>=50% of a word's on-instances)
    Gb = (G > 0).astype(np.float32)            # [n_words, n_pairs]
    Wcnt = Gb.sum(1)
    word_fire_rate_all = (Gb @ fire_on_all.astype(np.float32)) / np.maximum(Wcnt[:, None], 1)  # [n_words, d_sae]
    word_fires_all = word_fire_rate_all >= 0.5
    covered_all = (Rmat > tau_resp[:, None]) & word_fires_all.T          # [d_sae, n_words]
    cover_count_all = covered_all.sum(1)
    # ELIGIBILITY: selective (precision floor) AND covers >=1 sub-context AND net-positive response.
    # (Sparse absorbers fail a mean-over-words test but cover their own sub-contexts strongly -> kept here.)
    eligible = (precision_all >= PREC_FLOOR) & (cover_count_all >= 1) & (real_stat > 0)
    Lr = np.where(eligible)[0]
    log(f"{el()} {letter}: Lr(eligible)={len(Lr)} mean_responsive={len(mean_responsive)} (of {d_sae})")
    R["n_responsive"] = int(len(Lr))
    R["n_mean_responsive"] = int(len(mean_responsive))
    if len(Lr) < 2:
        R["error"] = f"insufficient eligible latents ({len(Lr)})"
        return R

    # restrict to Lr
    precision = precision_all[Lr]
    word_fires = word_fires_all[:, Lr]         # [n_words, |Lr|]
    Rmat_Lr = Rmat[Lr]                         # [|Lr|, n_words]
    covered = covered_all[Lr]                  # [|Lr|, n_words]
    cover_sets = [set(np.where(covered[li])[0].tolist()) for li in range(len(Lr))]
    cover_size = covered.sum(1)

    # ---- M4(a): FIRING-FLOOR ANCHOR VALIDATION substrate ----
    # Held-out corpus fire-rate per cover-eligible latent. Consumes NO shared `rng` (sae_encode_np is
    # deterministic) so L/O/T/D reproduce iter-3 byte-for-byte; only an anchor whose corpus fire-rate is
    # below the floor is rejected (the iter-3 I=1227 0%-corpus spurious anchor).
    Lr_global_early = [int(x) for x in Lr]
    z_corp_Lr = sae_encode_np(sae, h_corpus_all[letter], torch, keep_latents=Lr_global_early)  # [n_corpus, |Lr|]
    corpus_fire_Lr = (z_corp_Lr > 0).mean(axis=0).astype(np.float64)   # [|Lr|]
    del z_corp_Lr
    gc.collect()

    def pick_anchor(cover_size, corpus_fire_Lr, floor):
        """M4: highest-RECALL cover-eligible latent whose held-out corpus fire-rate >= floor.
        raw = iter-3 recall-argmax (np.argmax). When raw already passes the floor, chosen==raw (stable
        order puts the lowest-index max-recall latent first, matching np.argmax) -> byte-for-byte repro."""
        order = np.argsort(-cover_size, kind="stable")
        raw = int(np.argmax(cover_size))
        valid = [int(li) for li in order.tolist() if corpus_fire_Lr[li] >= floor]
        chosen = int(valid[0]) if valid else raw
        return chosen, raw, len(valid)

    anchor_li_valid, raw_anchor_li, n_anchor_valid = pick_anchor(cover_size, corpus_fire_Lr, ANCHOR_CORPUS_FIRE_FLOOR)
    R["anchor_validation"] = {
        "raw_recall_argmax_global": int(Lr[raw_anchor_li]),
        "raw_anchor_corpus_fire": float(corpus_fire_Lr[raw_anchor_li]),
        "validated_anchor_global": int(Lr[anchor_li_valid]),
        "validated_anchor_corpus_fire": float(corpus_fire_Lr[anchor_li_valid]),
        "anchor_changed": bool(anchor_li_valid != raw_anchor_li),
        "floor": ANCHOR_CORPUS_FIRE_FLOOR,
        "n_eligible_pass_floor": int(n_anchor_valid),
        "no_firing_valid_anchor": bool(n_anchor_valid == 0)}
    log(f"{el()} {letter}: anchor_validation raw={int(Lr[raw_anchor_li])}(fire={corpus_fire_Lr[raw_anchor_li]:.3f}) "
        f"validated={int(Lr[anchor_li_valid])}(fire={corpus_fire_Lr[anchor_li_valid]:.3f}) "
        f"changed={anchor_li_valid != raw_anchor_li} n_pass_floor={n_anchor_valid}")

    def fj(li, lj):
        a = set(np.where(word_fires[:, li])[0].tolist())
        b = set(np.where(word_fires[:, lj])[0].tolist())
        return jaccard(a, b)

    # ---- per-latent AUC (train folds vs test fold) over content instances ----
    folds = np.array(on_folds)
    ufolds = sorted(set(folds.tolist()))
    test_fold = ufolds[-1]
    tr_mask = folds != test_fold
    te_mask = folds == test_fold
    # build instance-level matrix for Lr: on=label1, off=label0
    lab = np.concatenate([np.ones(n_pairs), np.zeros(n_pairs)])
    inst_fold = np.concatenate([folds, folds])
    Z = np.concatenate([a_on[:, Lr], a_off[:, Lr]], axis=0)   # [2n, |Lr|]
    itr = inst_fold != test_fold
    ite = inst_fold == test_fold
    auc_tr = np.array([auc(Z[itr, li], lab[itr]) for li in range(len(Lr))])
    auc_te = np.array([auc(Z[ite, li], lab[ite]) for li in range(len(Lr))])

    # ============================ STEP 2: C-TRACK ============================
    log(f"{el()} {letter}: starting C-track (|Lr|={len(Lr)})")
    if cfg.get("dump_rmat"):
        np.save(f"dbg_Rmat_{letter}.npy", Rmat_Lr)
    ctrack = c_track(Rmat_Lr, GAMMA_GRID, cfg, rng)
    R["cluster_stability_ARI"] = ctrack["best_ari"]
    R["c_track"] = {"gamma": ctrack["gamma"], "n_communities": ctrack["n_comm"],
                    "best_ari": ctrack["best_ari"], "shuffle_ari": ctrack["shuffle_ari"]}

    # ============================ STEP 3: K-TRACK (E1 CORE) ============================
    def run_ktrack(jacc_max, prec_floor, min_hole, max_k=MAX_K, anchor_override=None):
        # anchored greedy max-coverage: anchor = M4 firing-validated highest-recall latent (default: the
        # iter-3 recall-argmax, == validated when it already fires on corpus);
        # iteratively add the latent covering the most UNCOVERED holes among precise, anchor-disjoint latents.
        anchor_li = int(anchor_override) if anchor_override is not None else int(np.argmax(cover_size))
        members = [anchor_li]
        H = set(range(n_words)) - cover_sets[anchor_li]
        trace = []
        while H and len(members) < max_k:
            best_li, best_gainH = -1, 0
            for li in range(len(Lr)):
                if li in members:
                    continue
                gH = len(cover_sets[li] & H)
                if gH < min_hole:
                    continue
                if precision[li] < prec_floor:
                    continue
                if fj(li, anchor_li) >= jacc_max:
                    continue
                if gH > best_gainH:
                    best_gainH, best_li = gH, li
            if best_li < 0:
                break
            members.append(best_li); H = H - cover_sets[best_li]
            trace.append({"li": int(best_li), "global": int(Lr[best_li]), "new_holes": int(best_gainH),
                          "gain": best_gainH / n_words, "jaccard": fj(best_li, anchor_li),
                          "prec": float(precision[best_li])})
        return anchor_li, members, trace

    anchor_li, k_members_li, k_trace = run_ktrack(JACCARD_MAX, PREC_FLOOR, MIN_HOLE_HEADLINE,
                                                  anchor_override=anchor_li_valid)
    R["k_trace"] = k_trace
    R["anchor_cover_size"] = int(cover_size[anchor_li]); R["n_words"] = int(n_words)
    anchor_global = int(Lr[anchor_li])
    k_members_global = [int(Lr[li]) for li in k_members_li]
    R["K_UNIT"] = k_members_global
    R["anchor_idx"] = anchor_global
    R["absorber_idxs"] = k_members_global[1:]
    log(f"{el()} {letter}: K_UNIT k={len(k_members_global)} anchor={anchor_global} absorbers={k_members_global[1:]}")

    # ============================ FORM-FREE DIAGNOSTIC (ORACLE) ============================
    diag = form_free_diagnostic(letter, mb, sae, h_corpus_all, corpus_rows_all,
                                a_on, h_on, on_words, on_spans, Lr, anchor_global, cfg)
    R["diagnostic"] = {"parent": diag["parent"], "n_absorbers": len(diag["absorbers"]),
                       "absorber_latents": sorted(set(diag["absorber_latents"])),
                       "probe_acc": diag["probe_acc"], "parent_recall": diag["parent_recall"],
                       "absorbers": diag["absorbers"][:50]}
    DIAG_PARENT = diag["parent"]
    DIAG_ABS_LAT = set(diag["absorber_latents"])
    DIAG_SET = set([DIAG_PARENT]) | DIAG_ABS_LAT if DIAG_PARENT is not None else DIAG_ABS_LAT

    # ============================ E1 ============================
    kset = set(k_members_global)
    inter = kset & DIAG_SET
    prec = len(inter) / max(1, len(kset))
    rec = len(inter) / max(1, len(DIAG_SET))
    f1 = 2 * prec * rec / max(1e-9, prec + rec)
    # random-membership null
    null_f1 = []
    Lr_global = [int(x) for x in Lr]
    for _ in range(cfg["b_null"]):
        samp = set(rng.choice(Lr_global, size=min(len(kset), len(Lr_global)), replace=False).tolist())
        ii = samp & DIAG_SET
        pp = len(ii) / max(1, len(samp)); rr = len(ii) / max(1, len(DIAG_SET))
        null_f1.append(2 * pp * rr / max(1e-9, pp + rr))
    null_f1 = np.array(null_f1)
    f1_pctile = float((null_f1 < f1).mean())
    anchor_recovered = (DIAG_PARENT is not None and anchor_global == DIAG_PARENT)
    n_abs_recovered = len(kset & DIAG_ABS_LAT)
    e1_pass = bool(f1 > np.percentile(null_f1, 95) and anchor_recovered and n_abs_recovered >= 2)
    R["E1"] = {"precision": prec, "recall": rec, "F1": f1, "null_pctile": f1_pctile,
               "null_f1_95": float(np.percentile(null_f1, 95)), "anchor_recovered": anchor_recovered,
               "n_absorbers_recovered": int(n_abs_recovered), "E1_PASS": e1_pass}
    log(f"{el()} {letter}: E1 F1={f1:.3f} pctile={f1_pctile:.3f} anchor_ok={anchor_recovered} "
        f"abs_recovered={n_abs_recovered} PASS={e1_pass}")

    # anchor fidelity: corpus firing selectivity + logit lens
    R["anchor_fidelity"] = anchor_fidelity(letter, mb, sae, h_corpus_all, anchor_global,
                                           DIAG_PARENT, torch)

    # threshold sweep
    sweep = []
    for jm in [0.05, 0.1, 0.15, 0.2]:
        for pf in [0.6, 0.7, 0.8]:
            for cf in [0.03, 0.05, 0.07]:
                mh = max(1, int(np.ceil(cf * n_words)))
                _, mem_li, _ = run_ktrack(jm, pf, mh, anchor_override=anchor_li_valid)
                mg = set(int(Lr[li]) for li in mem_li)
                ii = mg & DIAG_SET
                pp = len(ii) / max(1, len(mg)); rr = len(ii) / max(1, len(DIAG_SET))
                f1s = 2 * pp * rr / max(1e-9, pp + rr)
                sweep.append({"jaccard": jm, "precision": pf, "cov_gain": cf, "k": len(mg), "F1": round(f1s, 3),
                              "abs_recovered": len(mg & DIAG_ABS_LAT)})
    R["E1"]["threshold_sweep_grid"] = sweep

    # ============================ BASELINES (count-matched to k) ============================
    k = len(k_members_global)
    # need d_p and mean activation for (g)/(h)
    d_p = diag["d_p"]
    mean_act = diag["mean_act"]  # [d_sae] mean activation over target-letter corpus
    bsel = build_baselines(letter, Lr, Lr_global, auc_tr, auc_te, k, cover_sets, word_fires,
                           W_dec=sae.W_dec.cpu().numpy(), d_p=d_p, mean_act=mean_act,
                           h_corpus=h_corpus_all[letter], sae=sae, torch=torch, cfg=cfg, rng=rng)
    R["baselines"] = {key: bsel[key]["members"] for key in bsel
                      if isinstance(bsel[key], dict) and "members" in bsel[key]}

    # Lr-restricted activation views for downstream (global latents map via Lr_local; non-Lr re-encoded)
    a_on_Lr = a_on[:, Lr]
    a_off_Lr = a_off[:, Lr]

    # ============================ M1: RANDOM-ELIGIBLE-k POOL (RE-k) ============================
    # Computed ONCE here (shared by E2 + C1). Decisive object: isolates two-track SELECTION from
    # cover-based eligibility + max-pooling. Uses a SEPARATE child rng (shared `rng` order untouched ->
    # E1/E2-recall/C1-AUC reproduce iter-2 byte-for-byte).
    rek_labels = np.concatenate([np.ones(n_pairs), np.zeros(n_pairs)])
    rek_test_mask = (np.concatenate([folds, folds]) == test_fold)
    rek = rek_pool(letter, Lr, len(k_members_global), a_on_Lr, a_off_Lr, rek_labels, n_pairs,
                   rek_test_mask, cfg["rek_draws"], np.random.default_rng(SEED + 101))
    R["rek_distribution"] = {kk: rek[kk] for kk in
                             ("draw_auc_mean", "draw_auc_p05", "draw_auc_p50", "draw_auc_p95",
                              "draw_auc_max", "draw_auc_min", "B_draws", "k", "median_draw_members")}
    log(f"{el()} {letter}: RE-k draws mean={rek['draw_auc_mean']:.3f} p50={rek['draw_auc_p50']:.3f} "
        f"p95={rek['draw_auc_p95']:.3f} max={rek['draw_auc_max']:.3f} (B={rek['B_draws']}, k={rek['k']})")

    # ============================ M5: NON-RANDOM, LABEL-FREE, COUNT-MATCHED SELECTORS ============================
    # Three label-free selectors over the SAME cover-eligible set E = Lr, each picking EXACTLY k = |K_UNIT|
    # latents by ONE label-free criterion, then max-pooled IDENTICALLY to the unit/(h)/(b)/(c)/RE-k. The
    # ONLY factor that varies vs the two-track unit is the SELECTION/membership rule -> isolates set-cover
    # selection from sensible label-free selection. All three statistics are label-free + already computed.
    kk = int(min(len(k_members_global), len(Lr)))
    mag_Lr = a_on_Lr.mean(axis=0)                        # mean content-positive activation magnitude [|Lr|]
    sel_specs = {
        "S_rec":  np.argsort(-cover_size, kind="stable")[:kk],    # top-k by content-flip recall (cover size)
        "S_prec": np.argsort(-precision, kind="stable")[:kk],     # top-k by firing precision
        "S_mag":  np.argsort(-mag_Lr, kind="stable")[:kk]}        # top-k by mean response magnitude
    selectors_global = {nm: [int(Lr[c]) for c in cols.tolist()] for nm, cols in sel_specs.items()}
    R["selectors"] = selectors_global
    log(f"{el()} {letter}: M5 selectors k={kk} S_rec[:3]={selectors_global['S_rec'][:3]} "
        f"S_prec[:3]={selectors_global['S_prec'][:3]} S_mag[:3]={selectors_global['S_mag'][:3]}")

    # M7 compact-named-unit substrate (scored inside run_c1 where pooled_full + folds are in scope)
    compact_info = {"anchor": anchor_global, "diag_abs": set(int(x) for x in DIAG_ABS_LAT),
                    "k_trace_globals": [int(t["global"]) for t in k_trace]}

    # ============================ E2 / C3 ============================
    e2 = run_e2(letter, k_members_global, bsel, DIAG_ABS_LAT, diag, a_on_Lr, Lr, on_words, on_spans,
                folds, test_fold, w_index, uwords, sae, h_on, cfg, rng, rek=rek)
    R["E2"] = e2["report"]

    # ============================ C1 ============================
    c1 = run_c1(letter, k_members_global, bsel, a_on_Lr, a_off_Lr, Lr, folds, test_fold, on_words, w_index,
                uwords, sae, h_on, h_off, cfg, rng, rek=rek,
                on_inputs=on_inputs, off_inputs=off_inputs, off_words=off_words,
                selectors=selectors_global, compact_info=compact_info)
    R["examples"] = c1.pop("examples", [])
    pooled_diffs_this = c1.pop("_pooled_diffs", {})
    if pooled_store is not None:
        pooled_store[letter] = pooled_diffs_this     # large _diffs arrays kept OUT of saved JSON
    R["compact_vs_wide"] = c1.pop("compact_vs_wide", {})
    R["C1"] = c1

    # ============================ M5 SELECTION-ISOLATION VERDICT (per letter) ============================
    ad_c1 = R["C1"].get("auc_diff", {})
    def _beats(X):
        return bool(ad_c1.get(f"unit_vs_{X}", {}).get("sig_unit_better"))
    beats_all_m5 = bool(_beats("S_rec") and _beats("S_prec") and _beats("S_mag"))
    R["selection_isolation"] = {
        "unit_beats": {X: _beats(X) for X in ["h", "REk", "S_rec", "S_prec", "S_mag"]},
        "beats_all_M5": beats_all_m5,
        "set_cover_established": bool(_beats("h") and beats_all_m5),
        "eligibility_pooling_only": bool(_beats("h") and not beats_all_m5)}
    log(f"{el()} {letter}: selection_isolation beats h={_beats('h')} REk={_beats('REk')} "
        f"S_rec={_beats('S_rec')} S_prec={_beats('S_prec')} S_mag={_beats('S_mag')} "
        f"| set_cover_established={R['selection_isolation']['set_cover_established']}")

    # ============================ STEP 5 ADMISSION ============================
    adm = run_admission(letter, k_members_li, k_members_global, ctrack, Lr, Lr_global, Rmat_Lr, a_on_Lr, a_off_Lr,
                        precision, word_fires, surface, mb, sae, torch, auc_tr, cfg, rng,
                        c_p_null=(r_pair, c_p))
    R["admission"] = adm

    # KG specialization edges
    kg = []
    diag_pairs = set((DIAG_PARENT, l) for l in DIAG_ABS_LAT) if DIAG_PARENT is not None else set()
    abs_word = {}
    for a in diag["absorbers"]:
        abs_word.setdefault(a["absorber_latent"], a["word"])
    for ab in k_members_global[1:]:
        edge = {"src": anchor_global, "dst": ab, "type": "absorbed_child",
                "sub_context": abs_word.get(ab, ""), "diag_agrees": bool((anchor_global, ab) in diag_pairs or ab in DIAG_ABS_LAT)}
        kg.append(edge)
    R["kg_edges"] = kg

    # unit definition with logit lens + conditioning contexts
    R["unit_definition"] = unit_definition(letter, k_members_global, anchor_global, k_members_global[1:],
                                           mb, sae, h_corpus_all[letter], corpus_rows_all[letter], torch)

    # cleanup
    del a_on, a_off, r_pair, h_on, h_off, Z
    gc.collect()
    torch.cuda.empty_cache()
    return R


# ---------------------------------------------------------------- C-TRACK
def _spearman_mat_np(X):
    L = X.shape[0]
    Rk = np.argsort(np.argsort(X, axis=1), axis=1).astype(np.float64)
    C = np.corrcoef(Rk); C = np.atleast_2d(C)
    if C.shape != (L, L):
        C = np.eye(L)
    return np.nan_to_num(C, nan=0.0)


def _c_track_worker(Rsub, gamma_grid, n_boot, seed, beta, q):
    """Leiden community detection over Rsub rows. Runs in a SUBPROCESS (Leiden can hang on pathological
    weighted graphs; a hung subprocess is terminated by the parent). Puts a result dict on q."""
    try:
        import numpy as _np
        import leidenalg, igraph
        from sklearn.metrics import adjusted_rand_score
        rng = _np.random.default_rng(seed)
        L = Rsub.shape[0]
        rho = _spearman_mat_np(Rsub)
        A = _np.clip(rho, 0, None) ** beta; _np.fill_diagonal(A, 0.0)
        iu = _np.triu_indices(L, 1)

        def part(Am, g):
            wv = Am[iu]; m = wv > 1e-6
            src = iu[0][m]; tgt = iu[1][m]; wv = wv[m]
            if len(wv) == 0:
                return _np.arange(L)
            gr = igraph.Graph(n=L, edges=list(zip(src.tolist(), tgt.tolist())))
            gr.es["weight"] = wv.tolist()
            p = leidenalg.find_partition(gr, leidenalg.RBConfigurationVertexPartition,
                                         weights="weight", resolution_parameter=g, seed=seed, n_iterations=2)
            return _np.array(p.membership)

        best = {"gamma": None, "ari": -1, "labels": None, "n_comm": 0}
        best_nt = {"gamma": None, "ari": -1, "labels": None, "n_comm": 0}
        for g in gamma_grid:
            base = part(A, g); nc = int(len(set(base.tolist()))); aris = []
            for _ in range(n_boot):
                cols = rng.integers(0, Rsub.shape[1], Rsub.shape[1])
                Ab = _np.clip(_spearman_mat_np(Rsub[:, cols]), 0, None) ** beta; _np.fill_diagonal(Ab, 0.0)
                aris.append(adjusted_rand_score(base, part(Ab, g)))
            mari = float(_np.mean(aris)) if aris else 0.0
            if mari > best["ari"]:
                best = {"gamma": g, "ari": mari, "labels": base.tolist(), "n_comm": nc}
            if nc >= 2 and mari > best_nt["ari"]:
                best_nt = {"gamma": g, "ari": mari, "labels": base.tolist(), "n_comm": nc}
        ch = best_nt if best_nt["labels"] is not None else best
        base = _np.array(ch["labels"]) if ch["labels"] is not None else _np.arange(L)
        shuf = [adjusted_rand_score(base, base[rng.permutation(L)]) for _ in range(6)]
        q.put({"gamma": ch["gamma"], "n_comm": ch["n_comm"], "best_ari": ch["ari"],
               "shuffle_ari": float(_np.mean(shuf)) if shuf else 0.0, "labels": ch["labels"]})
    except Exception as e:
        q.put({"error": repr(e)})


def c_track(Rmat_Lr, gamma_grid, cfg, rng):
    import multiprocessing as mp
    t_c0 = time.time()
    L_full = Rmat_Lr.shape[0]
    empty = {"gamma": None, "n_comm": 0, "best_ari": 0.0, "shuffle_ari": 0.0, "labels": None}
    if L_full < 4:
        return empty
    # bound graph size: cluster the most-responsive latents; keep full-length labels (-1 = unclustered).
    LMAX = cfg.get("c_lmax", 160)
    sub_idx = (np.argsort(-np.nanmax(Rmat_Lr, axis=1))[:LMAX]) if L_full > LMAX else np.arange(L_full)
    Rsub = np.ascontiguousarray(Rmat_Lr[sub_idx]); L = Rsub.shape[0]
    n_boot = min(cfg["c_boot"], 6); timeout = cfg.get("c_timeout", 45)
    res = None
    try:
        ctx = mp.get_context("spawn")
        q = ctx.Queue()
        p = ctx.Process(target=_c_track_worker, args=(Rsub, list(gamma_grid), n_boot, SEED, BETA, q),
                        daemon=True)
        p.start()
        # drain the queue first (avoids feeder-thread deadlock if the child finishes), bounded by timeout
        try:
            res = q.get(timeout=timeout)
        except Exception:
            res = None
        if res is None and p.is_alive():
            log(f"  [c-track] TIMEOUT after {timeout}s -> SIGKILL + agglomerative fallback")
        if p.is_alive():
            p.kill(); p.join(5)      # SIGKILL: cannot be caught/ignored by the hung C extension
        else:
            p.join(2)
    except Exception as e:
        log(f"  [c-track] subprocess error: {e!r} -> fallback")
        res = None
    if res is not None and "error" in res:
        log(f"  [c-track] worker error: {res['error']} -> fallback"); res = None
    if res is None:
        # agglomerative fallback on correlation distance (deterministic, no hang)
        from sklearn.cluster import AgglomerativeClustering
        rho = spearman_mat(Rsub); D = 1.0 - np.clip(rho, -1, 1); np.fill_diagonal(D, 0.0)
        try:
            lab = AgglomerativeClustering(n_clusters=None, metric="precomputed", linkage="average",
                                          distance_threshold=0.5).fit(D).labels_
        except Exception:
            lab = np.zeros(L, dtype=int)
        res = {"gamma": "agglo_fallback", "n_comm": int(len(set(lab.tolist()))), "best_ari": 0.0,
               "shuffle_ari": 0.0, "labels": lab.tolist()}
    full_labels = -np.ones(L_full, dtype=int)
    full_labels[sub_idx] = np.array(res["labels"])
    log(f"  [c-track] L={L}/{L_full} gamma={res['gamma']} comms={res['n_comm']} ARI={res['best_ari']:.3f} "
        f"({time.time()-t_c0:.1f}s)")
    return {"gamma": res["gamma"], "n_comm": res["n_comm"], "best_ari": res["best_ari"],
            "shuffle_ari": res["shuffle_ari"], "labels": full_labels.tolist()}


# ---------------------------------------------------------------- DIAGNOSTIC
def form_free_diagnostic(letter, mb, sae, h_corpus_all, corpus_rows_all, a_on, h_on, on_words,
                         on_spans, Lr, anchor_global, cfg):
    """Train parent-concept probe d_p on DISJOINT corpus data; find form-free absorbers."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    torch = mb.torch
    # positives: this letter's corpus resid; negatives: other letters' corpus resid
    pos = h_corpus_all[letter]
    neg_list = [h_corpus_all[o] for o in h_corpus_all if o != letter]
    neg = np.concatenate(neg_list, axis=0)
    rng = np.random.default_rng(SEED)
    npos = pos.shape[0]
    if neg.shape[0] > npos:
        sel = rng.choice(neg.shape[0], npos, replace=False); neg = neg[sel]
    X = np.concatenate([pos, neg], 0)
    y = np.concatenate([np.ones(pos.shape[0]), np.zeros(neg.shape[0])])
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=SEED, stratify=y)
    clf = LogisticRegression(max_iter=2000, C=1.0)
    clf.fit(Xtr, ytr)
    acc = float(clf.score(Xte, yte))
    d_p = clf.coef_[0].astype(np.float32)
    d_p_unit = d_p / (np.linalg.norm(d_p) + 1e-9)

    # parent latent = max ENCODER cosine with d_p (over Lr)
    W_enc = sae.W_enc.cpu().numpy()           # [d_model, d_sae]
    enc_cos = (d_p_unit @ W_enc) / (np.linalg.norm(W_enc, axis=0) + 1e-9)  # [d_sae]
    Lr_set = set(int(x) for x in Lr)
    parent = int(max(Lr, key=lambda l: enc_cos[l])) if len(Lr) else None

    # mean activation over target-letter corpus (for attribution baselines)
    z_corpus = sae_encode_np(sae, pos, torch)
    mean_act = z_corpus.mean(0)               # [d_sae]
    # parent recall over corpus: fraction of corpus windows where parent fires
    parent_recall = float((z_corpus[:, parent] > 0).mean()) if parent is not None else 0.0
    del z_corpus

    # form-free absorber search over on-words (false negatives of parent)
    W_dec = sae.W_dec.cpu().numpy()           # [d_sae, d_model]
    absorbers = []
    absorber_latents = []
    # parent fires on each on-instance?
    parent_fires = a_on[:, parent] > 0 if parent is not None else np.zeros(a_on.shape[0], bool)
    # probe predicts positive on the on-instance residual? (use the fitted classifier's boundary)
    probe_pos = clf.decision_function(h_on) > 0
    seen_word = set()
    for p in range(a_on.shape[0]):
        w = on_words[p]
        if w in seen_word:
            continue
        # false negative: probe right (positive) but parent silent
        if probe_pos[p] and not parent_fires[p]:
            a = h_on[p]                       # full residual [d_model]
            denom = float(a @ d_p_unit)
            if denom <= 1e-6:                  # require concept positively present
                continue
            z = a_on[p]                       # [d_sae] sae acts
            fired = np.where(z > 0)[0]
            best_l, best_ratio = -1, 0.0
            for l in fired:
                if l == parent:
                    continue
                a_hat = z[l] * W_dec[l]        # contribution vector
                ratio = float((a_hat @ d_p_unit) / denom)
                if ratio > best_ratio:
                    best_ratio, best_l = ratio, l
            if best_l >= 0 and best_ratio > TAU_C:
                absorbers.append({"word": w, "absorber_latent": int(best_l), "ratio": round(best_ratio, 3)})
                absorber_latents.append(int(best_l))
                seen_word.add(w)
    log(f"{el()} {letter}: diagnostic probe_acc={acc:.3f} parent={parent} parent_recall={parent_recall:.3f} "
        f"absorbers={len(absorbers)} unique_abs_latents={len(set(absorber_latents))}")
    return {"d_p": d_p_unit, "parent": parent, "absorbers": absorbers,
            "absorber_latents": absorber_latents, "probe_acc": acc, "parent_recall": parent_recall,
            "mean_act": mean_act}


def anchor_fidelity(letter, mb, sae, h_corpus_all, anchor_global, parent, torch):
    z = sae_encode_np(sae, h_corpus_all[letter], torch, keep_latents=[anchor_global])
    fire_rate = float((z[:, 0] > 0).mean())
    # logit lens: top tokens promoted by W_dec[anchor]
    W_dec = sae.W_dec[anchor_global]          # [d_model]
    E = mb.model.get_output_embeddings().weight  # [vocab, d_model]
    with torch.no_grad():
        logits = (E.to(torch.float32) @ W_dec.to(torch.float32))
        top = torch.topk(logits, 12).indices.cpu().tolist()
    toks = [mb.tok.convert_tokens_to_string([t]).strip() for t in mb.tok.convert_ids_to_tokens(top)]
    return {"anchor": anchor_global, "is_diag_parent": bool(anchor_global == parent),
            "corpus_fire_rate": fire_rate, "logit_lens_top": toks}


# ---------------------------------------------------------------- BASELINES
def build_baselines(letter, Lr, Lr_global, auc_tr, auc_te, k, cover_sets, word_fires, W_dec,
                    d_p, mean_act, h_corpus, sae, torch, cfg, rng):
    """Return dict of baseline -> {members:[global idx], local:[li]}."""
    from sklearn.cluster import AgglomerativeClustering
    out = {}
    nLr = len(Lr)

    # (a) best raw single latent by held-out (train) AUC
    a_li = int(np.argmax(auc_tr))
    out["a"] = {"members": [int(Lr[a_li])], "local": [a_li]}

    # corpus firing for Lr (co-activation)
    z_corp = sae_encode_np(sae, h_corpus, torch, keep_latents=Lr_global)   # [n_corpus, |Lr|]
    Fcorp = (z_corp > 0).astype(np.float32)

    # (b) co-activation clusters via HDBSCAN on jaccard distance over corpus firing
    members_b = cluster_pick(Fcorp.T, auc_tr, k, nLr, mode="cofire", rng=rng)
    out["b"] = {"members": [int(Lr[li]) for li in members_b], "local": members_b}

    # (c) decoder-geometry clusters (agglomerative cosine on W_dec[Lr])
    Wd = W_dec[Lr_global]
    members_c = cluster_pick(Wd, auc_tr, k, nLr, mode="cosine", rng=rng)
    out["c"] = {"members": [int(Lr[li]) for li in members_c], "local": members_c}

    # (g) oracle SCR/TPP pool: attribution = |d_p . W_dec[l]| * mean_act[l]  (ALL latents), top-N
    attr = np.abs(W_dec @ d_p) * mean_act      # [d_sae]
    out["_attr"] = attr
    for N in (10, 20):
        topN = np.argsort(-attr)[:N].tolist()
        out[f"g{N}"] = {"members": [int(x) for x in topN], "local": None}
    out["g"] = out["g20"]

    # (h) count-and-pool matched: top-k by attribution, pooled
    topk = np.argsort(-attr)[:k].tolist()
    out["h"] = {"members": [int(x) for x in topk], "local": None}
    del z_corp, Fcorp
    return out


def cluster_pick(feats, auc_tr, k, nLr, mode, rng):
    """Cluster latents (rows of feats), pick concept-aligned cluster (max mean train-AUC), cut to k."""
    from sklearn.cluster import AgglomerativeClustering
    n = feats.shape[0]
    if n <= k:
        return list(np.argsort(-auc_tr)[:k])
    try:
        if mode == "cosine":
            cl = AgglomerativeClustering(n_clusters=None, metric="cosine", linkage="average",
                                         distance_threshold=0.6).fit(feats)
            labels = cl.labels_
        else:  # cofire -> jaccard distance, precomputed
            from scipy.spatial.distance import pdist, squareform
            D = squareform(pdist(feats.astype(bool), metric="jaccard"))
            D = np.nan_to_num(D, nan=1.0)
            cl = AgglomerativeClustering(n_clusters=None, metric="precomputed", linkage="average",
                                         distance_threshold=0.7).fit(D)
            labels = cl.labels_
    except Exception:
        labels = np.zeros(n, dtype=int)
    # pick cluster maximizing mean train AUC (min size 1)
    best_lab, best_score = None, -1
    for lab in set(labels.tolist()):
        idx = np.where(labels == lab)[0]
        sc = float(auc_tr[idx].mean())
        if sc > best_score:
            best_score, best_lab = sc, lab
    idx = np.where(labels == best_lab)[0]
    idx = idx[np.argsort(-auc_tr[idx])]
    members = list(idx[:k])
    if len(members) < k:
        # augment with highest-AUC latents not yet chosen
        rest = [i for i in np.argsort(-auc_tr) if i not in set(members)]
        members += rest[:k - len(members)]
    return [int(x) for x in members[:k]]


# ---------------------------------------------------------------- E2
def pooled_max_score(a_mat, Lr_or_global, members_global, Lr_global_map):
    """Score each instance = max activation over `members_global` (global latent idx).
    a_mat is [n, |Lr|] indexed by Lr local; need to map global->local where possible, else 0."""
    pass


def gather_member_acts(members_global, a_full_cols, Lr_global, sae, h_inst, torch):
    """Return activation matrix [n, len(members)] for given global latents on instances with residual h_inst."""
    return sae_encode_np(sae, h_inst, torch, keep_latents=list(members_global))


def run_e2(letter, k_members_global, bsel, DIAG_ABS_LAT, diag, a_on, Lr, on_words, on_spans,
           folds, test_fold, w_index, uwords, sae, h_on, cfg, rng, rek=None):
    torch = sae.torch
    report = {}
    rek_members = rek["median_draw_members"] if rek is not None else None
    # recovered absorber counts
    def rec_count(members):
        return len(set(members) & DIAG_ABS_LAT)
    counts = {"unit": rec_count(k_members_global),
              "g": rec_count(bsel["g"]["members"]), "g10": rec_count(bsel["g10"]["members"]),
              "h": rec_count(bsel["h"]["members"]), "b": rec_count(bsel["b"]["members"]),
              "c": rec_count(bsel["c"]["members"]), "a": rec_count(bsel["a"]["members"])}
    if rek_members is not None:
        counts["REk"] = rec_count(rek_members)
    report["recovered_absorber_counts"] = counts

    # absorbed-word slice = on-words that have a diagnostic absorber
    abs_words = set(a["word"] for a in diag["absorbers"])
    slice_pidx = [p for p in range(a_on.shape[0]) if on_words[p] in abs_words]
    report["absorbed_slice_size"] = len(slice_pidx)
    if len(slice_pidx) < 3:
        report["note"] = "absorbed slice too small for sliced-recall test"
        report["sliced_recall"] = {}
        report["paired_bootstrap_CIs"] = {}
        report["mcnemar_p"] = {}
        report["E2_PASS"] = False
        report["kg_edge_agreement"] = kg_agreement(letter, k_members_global, diag)
        return {"report": report}

    # build pooled-max detection on absorbed slice: positives are on-instances (label=1)
    # We need a "negative" reference: use off behavior implicitly via threshold fit on full content.
    # Detection recall on slice = fraction of slice on-instances scored above threshold.
    # Threshold fit per method on TRAIN folds over full content (on=1, off=0) using pooled-max.
    methods = {"unit": k_members_global, "g": bsel["g"]["members"], "g10": bsel["g10"]["members"],
               "h": bsel["h"]["members"], "b": bsel["b"]["members"], "c": bsel["c"]["members"],
               "a": bsel["a"]["members"]}
    if rek_members is not None:
        methods["REk"] = rek_members
    # gather member acts for each method on on-instances (and need off for threshold). We have a_on for Lr only.
    # Encode member acts directly from residuals (covers global latents not in Lr).
    h_off_needed = True
    sliced = {}
    correctness = {}
    # need off instances too -> reconstruct from caller? We'll fit threshold on on vs a matched random off proxy:
    # Use the same content instances: scores_on from a_on residuals; for threshold we use off acts via h?
    # Simplshift: fit threshold on TRAIN on-instances vs TRAIN off-instances using member acts.
    return _e2_finish(letter, methods, k_members_global, bsel, a_on, h_on, Lr, on_words, slice_pidx,
                      folds, test_fold, abs_words, diag, sae, torch, cfg, rng, report, rek=rek)


def _e2_finish(letter, methods, k_members_global, bsel, a_on, h_on, Lr, on_words, slice_pidx,
               folds, test_fold, abs_words, diag, sae, torch, cfg, rng, report, rek=None):
    # member acts on on-instances for each method
    Lr_local = {int(g): i for i, g in enumerate(Lr.tolist())}
    def acts_for(members):
        cols = []
        need_global = [m for m in members if m not in Lr_local]
        # acts available in a_on for Lr members; for non-Lr, encode
        base = np.zeros((a_on.shape[0], len(members)), dtype=np.float32)
        for j, m in enumerate(members):
            if m in Lr_local:
                base[:, j] = a_on[:, Lr_local[m]]
        if need_global:
            extra = sae_encode_np(sae, h_on, torch, keep_latents=need_global)
            ei = {m: jj for jj, m in enumerate(need_global)}
            for j, m in enumerate(members):
                if m in ei:
                    base[:, j] = extra[:, ei[m]]
        return base.max(1)  # pooled-max

    # threshold per method: fit on TRAIN on-instances using percentile that captures majority,
    # but we need negatives. Use off via residual? We approximate detection threshold as the
    # value separating firing (the absorbed words are FN of parent). Use 50th pct of TRAIN on-scores
    # of NON-absorbed on-words as the "fires" threshold reference is unstable; instead use a fixed
    # rule: detected iff pooled-max activation > 0 (latent fires). This is the natural SAE detector.
    tr = folds != test_fold
    slice_mask = np.zeros(a_on.shape[0], bool); slice_mask[slice_pidx] = True
    sliced = {}
    correctness = {}
    for name, members in methods.items():
        s = acts_for(members)
        det = (s > 0).astype(int)   # SAE unit detects starts-with-L iff some member fires
        sl = det[slice_mask]
        sliced[name] = float(sl.mean()) if len(sl) else 0.0
        correctness[name] = det[slice_mask]
    report["sliced_recall"] = sliced
    # paired bootstrap + mcnemar: unit vs each baseline on slice correctness
    cis, mcp = {}, {}
    holm_p = []
    holm_keys = []
    for bl in ["g", "g10", "h", "b", "c", "a"]:
        ci = paired_bootstrap_diff(correctness["unit"], correctness[bl], B=cfg["b_gap"], rng=rng)
        p, n01, n10 = mcnemar_p(correctness["unit"], correctness[bl])
        cis[f"unit_vs_{bl}"] = ci
        mcp[f"unit_vs_{bl}"] = {"p": p, "n01": n01, "n10": n10}
        holm_p.append(p); holm_keys.append(f"unit_vs_{bl}")
    rej, padj = holm(holm_p)
    report["paired_bootstrap_CIs"] = cis
    report["mcnemar_p"] = mcp
    report["holm"] = {holm_keys[i]: {"reject": rej[i], "p_adj": padj[i]} for i in range(len(holm_keys))}
    # M1: RE-k comparison in E2 (secondary completeness; SEPARATE child rng -> shared-rng order preserved,
    # so E2_PASS and the count-matched h/b/c CIs reproduce iter-2 exactly).
    if rek is not None and "REk" in correctness:
        report["unit_vs_REk"] = paired_bootstrap_diff(correctness["unit"], correctness["REk"],
                                                      B=cfg["b_gap"], rng=np.random.default_rng(SEED + 202))
    report["kg_edge_agreement"] = kg_agreement(letter, k_members_global, diag)
    counts = report["recovered_absorber_counts"]
    # NOTE: recovered-absorber COUNT is d_p-CIRCULAR for the oracle baselines (g/h rank by |d_p.W_dec|*mean_act;
    # the diagnostic also selects absorbers by d_p projection) -> g/h trivially overlap the diagnostic.
    # The load-bearing, NON-circular E2 test is sliced recall over absorbed sub-contexts vs the COUNT-MATCHED
    # baselines (h = oracle attribution @ k; b/c = label-free clusters @ k). Oracle POOLS g10/g20 are larger
    # references, not count-matched.
    report["recovered_count_caveat"] = ("recovered-absorber COUNT is circular for oracle baselines g/h "
                                        "(both rank by d_p like the diagnostic); use sliced_recall vs count-matched h/b/c")
    cm = ["h", "b", "c"]  # count-matched baselines
    win_recall_cm = all(cis[f"unit_vs_{bl}"]["diff"] > 0 for bl in cm)
    sig_recall_cm = cis["unit_vs_h"]["excl_0"] and cis["unit_vs_h"]["diff"] > 0
    # label-free absorber recovery: unit recovers >=2 absorbers and >= the label-free clusters b/c
    win_count_labelfree = counts["unit"] >= max(counts["b"], counts["c"]) and counts["unit"] >= 2
    report["E2_PASS"] = bool(win_recall_cm and sig_recall_cm)
    report["E2_count_matched_recall_win"] = bool(win_recall_cm)
    report["E2_labelfree_count_win"] = bool(win_count_labelfree)
    report["E2_vs_oracle_pool_g20"] = {"unit_recall": sliced["unit"], "g20_recall": sliced["g"],
                                       "unit_minus_g20": sliced["unit"] - sliced["g"]}
    log(f"{el()} {letter}: E2 counts unit={counts['unit']} g20={counts['g']} g10={counts['g10']} h={counts['h']} "
        f"b={counts['b']} c={counts['c']} | sliced unit={sliced['unit']:.3f} h={sliced['h']:.3f} "
        f"b={sliced['b']:.3f} c={sliced['c']:.3f} g20={sliced['g']:.3f} | cm_win={win_recall_cm} PASS={report['E2_PASS']}")
    return {"report": report}


def kg_agreement(letter, k_members_global, diag):
    parent = diag["parent"]
    diag_abs = set(diag["absorber_latents"])
    unit_edges = set(k_members_global[1:])
    if not diag_abs:
        return {"precision": 0.0, "recall": 0.0, "n_unit_edges": len(unit_edges), "n_diag_edges": 0}
    inter = unit_edges & diag_abs
    prec = len(inter) / max(1, len(unit_edges))
    rec = len(inter) / max(1, len(diag_abs))
    return {"precision": prec, "recall": rec, "n_unit_edges": len(unit_edges), "n_diag_edges": len(diag_abs)}


# ---------------------------------------------------------------- C1
def run_c1(letter, k_members_global, bsel, a_on, a_off, Lr, folds, test_fold, on_words, w_index, uwords,
           sae, h_on, h_off, cfg, rng, rek=None, on_inputs=None, off_inputs=None, off_words=None,
           selectors=None, compact_info=None):
    Lr_local = {int(g): i for i, g in enumerate(Lr.tolist())}
    n = a_on.shape[0]
    inst_fold = np.concatenate([folds, folds])
    labels = np.concatenate([np.ones(n), np.zeros(n)])
    itr = inst_fold != test_fold
    ite = inst_fold == test_fold
    on_words_arr = np.array(on_words)

    # pooled-max over members; non-Lr members (e.g. attribution baseline h/g) re-encoded from residuals.
    def pooled_full(members, sae, h_on, h_off):
        need = [m for m in members if m not in Lr_local]
        on = np.zeros((n, len(members)), np.float32); off = np.zeros((n, len(members)), np.float32)
        for j, m in enumerate(members):
            if m in Lr_local:
                on[:, j] = a_on[:, Lr_local[m]]; off[:, j] = a_off[:, Lr_local[m]]
        if need:
            eon = sae_encode_np(sae, h_on, sae.torch, keep_latents=need)
            eoff = sae_encode_np(sae, h_off, sae.torch, keep_latents=need)
            ei = {m: jj for jj, m in enumerate(need)}
            for j, m in enumerate(members):
                if m in ei:
                    on[:, j] = eon[:, ei[m]]; off[:, j] = eoff[:, ei[m]]
        return on.max(1), off.max(1)

    out = {"per_method": {}}
    methods = {"unit": k_members_global, "a": bsel["a"]["members"], "b": bsel["b"]["members"],
               "c": bsel["c"]["members"], "h": bsel["h"]["members"]}
    # M5: count-matched, label-free selectors scored with the IDENTICAL pooled-max rule (members all in Lr).
    # Appended AFTER the iter-3 baselines so their scoring (no shared rng) leaves a/b/c/h untouched.
    sel_names = []
    if selectors:
        for nm in ("S_rec", "S_prec", "S_mag"):
            if nm in selectors:
                methods[nm] = selectors[nm]; sel_names.append(nm)
    scores = {}; son_cache = {}
    correctness_f1 = {}   # OLD F1-threshold correctness, kept verbatim so the shared-rng bootstrap reproduces iter-2
    for name, members in methods.items():
        son, soff = pooled_full(members, sae, h_on, h_off)
        s_all = np.concatenate([son, soff])
        scores[name] = s_all; son_cache[name] = son
        t_f1 = best_f1_threshold(s_all[itr], labels[itr])
        correctness_f1[name] = (((s_all >= t_f1).astype(int)) == labels).astype(int)[ite]
    # M1: add RE-k frozen median-AUC draw scores as method 'REk' (same max-pool rule; members all in Lr)
    if rek is not None:
        scores["REk"] = np.asarray(rek["median_draw_scores"], dtype=np.float64)
        son_cache["REk"] = scores["REk"][:n]

    # ---- M7: compact named unit vs the 15-wide max-pool (+ anchor-only floor) ----
    # 15-wide = full K_UNIT; compact = anchor + diagnostic-corroborated absorbers (named specialists with a
    # known sub-context), capped at COMPACT_MAX; anchor_only = single-latent floor. All members are in Lr.
    m7_names = []; compact_block = None; m7_specs = {}
    if compact_info is not None:
        anchor_g = int(compact_info["anchor"]); diag_abs = compact_info["diag_abs"]
        named = [m for m in k_members_global[1:] if m in diag_abs]
        if named:
            compact_members = [anchor_g] + named[:COMPACT_MAX - 1]
            compact_label = "diagnostic-corroborated"
        else:
            greedy = list(compact_info.get("k_trace_globals", []))[:2]
            compact_members = [anchor_g] + greedy
            compact_label = "greedy-named-diagnostic-uncorroborated"
        m7_specs = {"unit_15wide": list(k_members_global), "unit_compact": compact_members,
                    "anchor_only": [anchor_g]}
        for tag, mem in m7_specs.items():
            son, soff = pooled_full(mem, sae, h_on, h_off)
            s_all = np.concatenate([son, soff])
            scores[tag] = s_all; son_cache[tag] = son; m7_names.append(tag)
        compact_block = {"compact_label": compact_label,
                         "compact_members": [int(x) for x in compact_members],
                         "named_members": [int(x) for x in named], "n_named_of_15": len(named),
                         "frac_named": len(named) / max(1, len(k_members_global) - 1), "anchor": anchor_g}

    all_names = list(methods.keys()) + (["REk"] if rek is not None else []) + m7_names

    # ---- M2: AUC POINTS + Youden accuracy table (no predict-all-positive collapse) + F1 artifact ----
    te_on = ite[:n]
    te_words = set(on_words_arr[te_on].tolist())
    collapse_any_youden = False
    f1_collapse_methods = []
    for name in all_names:
        s_all = scores[name]; son = son_cache[name]
        auc_te = fast_auc(s_all[ite], labels[ite])                    # POINT value (threshold-free, PRIMARY)
        t_y = youden_threshold(s_all[itr], labels[itr])
        acc_y = float((((s_all[ite] >= t_y).astype(int)) == labels[ite]).mean())
        collapse_y = bool(t_y <= float(s_all[itr].min()))
        collapse_any_youden = collapse_any_youden or collapse_y
        t_f1 = best_f1_threshold(s_all[itr], labels[itr])
        acc_f1 = float((((s_all[ite] >= t_f1).astype(int)) == labels[ite]).mean())
        collapse_f1 = bool(t_f1 <= float(s_all[itr].min()))
        if collapse_f1:
            f1_collapse_methods.append(name)
        f1v = f1_at(s_all[ite], labels[ite], t_f1)
        recs = []
        for w in te_words:
            wm = (on_words_arr == w) & te_on
            if wm.sum() == 0:
                continue
            recs.append(float((son[wm] >= t_y).mean()))
        worst = float(min(recs)) if recs else 0.0
        out["per_method"][name] = {
            "AUC": auc_te, "youden_threshold": float(t_y), "accuracy_youden": acc_y,
            "predict_all_positive_collapse": collapse_y, "worst_word_recall_youden": worst,
            "f1_threshold": float(t_f1), "accuracy_f1thresh": acc_f1,
            "f1thresh_collapse": collapse_f1, "F1_f1thresh": f1v}
    out["threshold_artifact_note"] = (
        "per_method.AUC is the threshold-free held-out test-fold point (PRIMARY, reproduces iter-2). "
        "accuracy_youden uses a comparison-matched Youden (TPR-FPR) cut and does NOT collapse to "
        "predict-all-positive. accuracy_f1thresh keeps the iter-2 F1-optimal cut for transparency: weak "
        f"detectors collapse to ~0.5 acc there (f1thresh_collapse=True for: {f1_collapse_methods}) despite "
        "non-trivial AUC -- the iter-2 accuracy-as-margin artifact this run replaces with AUC-difference CIs.")
    out["youden_no_collapse"] = bool(not collapse_any_youden)

    # ---- M2: AUC-DIFFERENCE bootstrap CIs (PRIMARY inferential object; child rngs -> shared-rng untouched) ----
    test_pairs = np.where(folds == test_fold)[0]
    li = LETTERS_ALL.index(letter) if letter in LETTERS_ALL else 9
    auc_diff = {}; pooled_diffs = {}
    # a/b/c/h/REk keep xi 0-4 (child rngs identical to iter-3 -> reproduction); M5 S_* appended at xi 5-7
    # with their own independent child rngs (additive, no perturbation of the iter-3 comparisons).
    for xi, X in enumerate(["a", "b", "c", "h", "REk", "S_rec", "S_prec", "S_mag"]):
        if X not in scores:
            continue
        keep = X in ("h", "REk", "S_rec", "S_prec", "S_mag")    # pooled across letters
        child = np.random.default_rng(SEED + 5000 + li * 100 + xi)
        d = bootstrap_auc_diff(scores["unit"], scores[X], n, test_pairs, B=cfg["b_gap"],
                               rng=child, keep_diffs=keep)
        dd = d.pop("_diffs")
        if keep and dd is not None:
            pooled_diffs[f"unit_vs_{X}"] = {"diffs": dd, "n_test_pairs": d["n_test_pairs"], "point": d["diff"]}
        auc_diff[f"unit_vs_{X}"] = d
    out["auc_diff"] = auc_diff
    out["_pooled_diffs"] = pooled_diffs

    # ---- M7: compact-vs-15-wide AUC-difference CI + AUC-vs-cumulative-k curve ----
    if compact_block is not None:
        cw = dict(compact_block)
        for tag in ("unit_15wide", "unit_compact", "anchor_only"):
            cw[tag] = {"k": len(m7_specs[tag]), "AUC": out["per_method"][tag]["AUC"],
                       "members": [int(x) for x in m7_specs[tag]]}
        child = np.random.default_rng(SEED + 9100 + li)
        cm = bootstrap_auc_diff(scores["unit_compact"], scores["unit_15wide"],
                                n, test_pairs, B=cfg["b_gap"], rng=child)
        cm.pop("_diffs", None)
        cw["compact_minus_15wide"] = cm
        auc_by_k = []     # greedy add order: k=1 (anchor) .. len(K_UNIT); members all in Lr (no re-encode)
        for j in range(len(k_members_global)):
            mem = k_members_global[:j + 1]
            son_j, soff_j = pooled_full(mem, sae, h_on, h_off)
            s_all = np.concatenate([son_j, soff_j])
            auc_by_k.append({"k": j + 1, "members": [int(x) for x in mem],
                             "AUC": fast_auc(s_all[ite], labels[ite])})
        cw["auc_by_k"] = auc_by_k
        cw["note"] = ("compact = anchor + diagnostic-corroborated precision-passing absorbers (named "
                      "specialists with a known sub-context); unit_15wide = full K_UNIT max-pool. The LLM "
                      "member-label fraction is reported by the auditability-expansion experiment and should "
                      "be cross-referenced here.")
        out["compact_vs_wide"] = cw
        log(f"{el()} {letter}: M7 compact k={cw['unit_compact']['k']} AUC={cw['unit_compact']['AUC']:.3f} "
            f"vs 15wide AUC={cw['unit_15wide']['AUC']:.3f} (Δ={cw['compact_minus_15wide']['diff']:.3f} "
            f"CI[{cw['compact_minus_15wide']['ci_lo']:.3f},{cw['compact_minus_15wide']['ci_hi']:.3f}]) "
            f"anchor_only AUC={cw['anchor_only']['AUC']:.3f} n_named={cw['n_named_of_15']}")

    # ---- M1: RE-k draw distribution + frac_rek_ge_unit (THE single most decisive number) ----
    if rek is not None:
        unit_auc = out["per_method"]["unit"]["AUC"]
        rek_aucs = np.asarray(rek["all_draw_aucs"])
        out["rek_distribution"] = {
            "draw_auc_mean": rek["draw_auc_mean"], "draw_auc_p05": rek["draw_auc_p05"],
            "draw_auc_p50": rek["draw_auc_p50"], "draw_auc_p95": rek["draw_auc_p95"],
            "draw_auc_max": rek["draw_auc_max"], "draw_auc_min": rek["draw_auc_min"],
            "B_draws": rek["B_draws"], "k": rek["k"], "unit_test_AUC": float(unit_auc),
            "frac_rek_ge_unit": float((rek_aucs >= unit_auc).mean()),
            "frac_unit_ge_rek": float((rek_aucs <= unit_auc).mean()),
            "median_draw_members": rek["median_draw_members"]}

    # ---- OLD accuracy-based paired bootstrap (transparency artifact; SHARED rng -> reproduction preserved) ----
    cis = {}; pv = []; keys = []
    for bl in ["b", "c", "h", "a"]:
        ci = paired_bootstrap_diff(correctness_f1["unit"], correctness_f1[bl], B=cfg["b_gap"], rng=rng)
        cis[f"unit_vs_{bl}"] = ci
        p, _, _ = mcnemar_p(correctness_f1["unit"], correctness_f1[bl]); pv.append(p); keys.append(bl)
    rej, padj = holm(pv)
    out["accuracy_f1thresh_paired_bootstrap_CIs"] = cis
    out["accuracy_f1thresh_holm_p"] = {keys[i]: {"reject": rej[i], "p_adj": padj[i]} for i in range(len(keys))}

    # ---- per-example TEST-fold predictions (Youden cut; adds predict_REk) ----
    examples = []
    if on_inputs is not None:
        thr = {name: out["per_method"][name]["youden_threshold"] for name in all_names}
        for j in np.where(ite)[0]:
            j = int(j)
            if j < n:
                inp, gold, role, word = on_inputs[j], "1", "on", on_words[j]; fold = int(folds[j])
            else:
                jj = j - n
                inp = off_inputs[jj]; gold, role = "0", "off"
                word = off_words[jj] if off_words is not None else on_words[jj]; fold = int(folds[jj])
            ex = {"input": inp, "output": gold, "metadata_letter": letter, "metadata_role": role,
                  "metadata_sub_context": word, "metadata_fold": fold,
                  "metadata_label_starts_with_target": int(gold)}
            for name in all_names:
                ex[f"predict_{name}"] = "1" if scores[name][j] >= thr[name] else "0"
            examples.append(ex)
    out["examples"] = examples
    ad = out["auc_diff"]
    rp50 = rek["draw_auc_p50"] if rek is not None else float("nan")
    frge = out.get("rek_distribution", {}).get("frac_rek_ge_unit", float("nan"))
    uvh = ad.get("unit_vs_h", {}); uvr = ad.get("unit_vs_REk", {})
    log(f"{el()} {letter}: C1 AUC unit={out['per_method']['unit']['AUC']:.3f} h={out['per_method']['h']['AUC']:.3f} "
        f"REk_p50={rp50:.3f} | unit-h={uvh.get('diff', float('nan')):.3f} "
        f"CI[{uvh.get('ci_lo', float('nan')):.3f},{uvh.get('ci_hi', float('nan')):.3f}] sig={uvh.get('sig_unit_better')} "
        f"| unit-REk={uvr.get('diff', float('nan')):.3f} "
        f"CI[{uvr.get('ci_lo', float('nan')):.3f},{uvr.get('ci_hi', float('nan')):.3f}] sig={uvr.get('sig_unit_better')} "
        f"| frac_rek>=unit={frge:.3f}")
    return out


# ---------------------------------------------------------------- ADMISSION
def run_admission(letter, k_members_li, k_members_global, ctrack, Lr, Lr_global, Rmat_Lr, a_on, a_off,
                  precision, word_fires, surface, mb, sae, torch, auc_tr, cfg, rng, c_p_null):
    """Step-5 admission for candidate units (K_UNIT + C-communities). BH/Holm multiplicity."""
    candidates = []
    # K_UNIT
    candidates.append(("K_UNIT", k_members_li))
    # C-communities (>=2 members)
    if ctrack["labels"] is not None:
        labs = np.array(ctrack["labels"])
        for lab in set(labs.tolist()):
            if lab == -1:           # unclustered (bounded-out of the C-track graph)
                continue
            mem = np.where(labs == lab)[0].tolist()
            if 2 <= len(mem) <= 30:   # genuine communities only (skip giant residual groups)
                candidates.append((f"C_comm_{lab}", mem))

    r_pair, c_p = c_p_null
    n_pairs = a_on.shape[0]

    # surface response (pooled) per latent for surface invariance
    surf_pid = sorted(surface.keys())
    surf_resp_cache = {}
    if surf_pid:
        va_in, va_sp, vb_in, vb_sp = [], [], [], []
        for pid in surf_pid:
            a = surface[pid]["var_a"]; b = surface[pid]["var_b"]
            va_in.append(a["input"]); va_sp.append(tuple(a["metadata_word_char_span"]))
            vb_in.append(b["input"]); vb_sp.append(tuple(b["metadata_word_char_span"]))
        h_va = mb.resid_at_spans(va_in, va_sp); h_vb = mb.resid_at_spans(vb_in, vb_sp)
        a_va = sae_encode_np(sae, h_va, torch, keep_latents=Lr_global)
        a_vb = sae_encode_np(sae, h_vb, torch, keep_latents=Lr_global)
    else:
        a_va = a_vb = None

    pvals = []
    results = []
    rng2 = np.random.default_rng(SEED + 7)
    Z_on = a_on  # [n_pairs, |Lr|]
    lab_inst = np.concatenate([np.ones(n_pairs), np.zeros(n_pairs)])
    for name, mem_li in candidates:
        mem_li = list(mem_li)
        # sigC: within-unit mean response correlation > 95th pct shuffled-pair null
        sub = Rmat_Lr[mem_li]
        if len(mem_li) >= 2:
            iu = np.triu_indices(len(mem_li), 1)
            cc = spearman_mat(sub)
            real_corr = float(np.nanmean(cc[iu])) if len(iu[0]) else 0.0
            # shuffle null: shuffle words within each row independently
            null = []
            for _ in range(min(cfg["b_null"], 300)):
                perm = np.array([rng2.permutation(sub.shape[1]) for _ in range(len(mem_li))])
                subp = np.take_along_axis(sub, perm, axis=1)
                cp = spearman_mat(subp)
                null.append(float(np.nanmean(cp[iu])) if len(iu[0]) else 0.0)
            sigC = bool(real_corr > np.percentile(null, 95))
            sigC_p = float((np.array(null) >= real_corr).mean())
        else:
            real_corr, sigC, sigC_p = 0.0, False, 1.0

        # sigK: pooled-max AUC - best-single-member AUC > AUC-matched random-k null
        pooled = np.concatenate([Z_on[:, mem_li].max(1), a_off[:, mem_li].max(1)])
        auc_pool = auc(pooled, lab_inst)
        single_aucs = [auc(np.concatenate([Z_on[:, li], a_off[:, li]]), lab_inst) for li in mem_li]
        best_single = max(single_aucs) if single_aucs else 0.5
        gainK = auc_pool - best_single
        # random-k null
        null_gain = []
        for _ in range(min(cfg["b_null"], 300)):
            rk = rng2.choice(len(Lr), size=len(mem_li), replace=False)
            pp = np.concatenate([Z_on[:, rk].max(1), a_off[:, rk].max(1)])
            ap = auc(pp, lab_inst)
            bs = max(auc(np.concatenate([Z_on[:, li], a_off[:, li]]), lab_inst) for li in rk)
            null_gain.append(ap - bs)
        sigK_p = float((np.array(null_gain) >= gainK).mean())
        jac_ok = True
        prec_ok = all(precision[li] >= PREC_FLOOR for li in mem_li)
        sigK = bool(gainK > np.percentile(null_gain, 95) and prec_ok)

        # surface invariance AND-gate
        if a_va is not None and len(mem_li):
            resp_surf = np.abs(a_va[:, mem_li].max(1) - a_vb[:, mem_li].max(1))
            # shuffle null: shuffle var_a/var_b assignment
            null_s = []
            for _ in range(min(cfg["b_null"], 300)):
                flip = rng2.random(a_va.shape[0]) < 0.5
                va = np.where(flip[:, None], a_vb[:, mem_li], a_va[:, mem_li]).max(1)
                vb = np.where(flip[:, None], a_va[:, mem_li], a_vb[:, mem_li]).max(1)
                null_s.append(np.abs(va - vb).mean())
            surf_invariant = bool(resp_surf.mean() <= np.percentile(null_s, 95))
            surf_p = float((np.array(null_s) >= resp_surf.mean()).mean())
        else:
            surf_invariant, surf_p = True, 1.0

        admit = bool((sigC or sigK) and surf_invariant)
        # admission p-value = min(sigC_p, sigK_p) (best signature) for multiplicity
        p_adm = min(sigC_p, sigK_p)
        pvals.append(p_adm)
        results.append({"name": name, "k": len(mem_li), "sigC": sigC, "sigC_p": sigC_p,
                        "sigK": sigK, "sigK_p": sigK_p, "gainK": float(gainK),
                        "surface_invariant": surf_invariant, "surf_p": surf_p,
                        "admit_raw": admit, "p_adm": p_adm})

    rej_bh, padj_bh = bh(pvals)
    rej_holm, padj_holm = holm(pvals)
    M = len(candidates)
    # EMPIRICAL FALSE-ADMIT under the matched random-k null. The sigK signature admits iff the pooled-AUC gain
    # exceeds the 95th pct of random-k gains; we build that null then test FRESH random-k draws against it
    # (a 95th-pct test -> ~0.05 by design). We also report how often random k latents drawn from the eligible
    # set Lr pool to a non-trivial absolute gain (>0.05) -- a descriptive property of Lr, NOT the admit rate.
    ksz = max(2, len(k_members_li))
    def _rand_gain():
        rk = rng2.choice(len(Lr), size=ksz, replace=False)
        pp = np.concatenate([Z_on[:, rk].max(1), a_off[:, rk].max(1)])
        ap = auc(pp, lab_inst)
        bs = max(auc(np.concatenate([Z_on[:, li], a_off[:, li]]), lab_inst) for li in rk)
        return ap - bs
    nN = min(cfg["b_null"], 150)
    null_g = np.array([_rand_gain() for _ in range(nN)])
    thr95 = float(np.percentile(null_g, 95))
    fresh = np.array([_rand_gain() for _ in range(nN)])
    false_admit_sigK = float((fresh > thr95).mean())
    frac_randk_gain_gt05 = float((null_g > 0.05).mean())

    for i, res in enumerate(results):
        res["bh_reject"] = rej_bh[i] if i < len(rej_bh) else False
        res["bh_padj"] = padj_bh[i] if i < len(padj_bh) else 1.0
        res["holm_reject"] = rej_holm[i] if i < len(rej_holm) else False
    log(f"{el()} {letter}: admission M={M} admitted_raw={sum(r['admit_raw'] for r in results)} "
        f"false_admit_sigK={false_admit_sigK:.3f} frac_randk_gain>0.05={frac_randk_gain_gt05:.2f}")
    return {"M": M, "candidates": results, "false_admit_randomk": float(false_admit_sigK),
            "false_admit_sigK_pctile_test": float(false_admit_sigK),
            "frac_randk_gain_gt_0.05": float(frac_randk_gain_gt05),
            "sigK_null95_gain": thr95,
            "K_UNIT_admitted": bool(results[0]["admit_raw"]) if results else False}


# ---------------------------------------------------------------- UNIT DEFINITION
def unit_definition(letter, members, anchor, absorbers, mb, sae, h_corpus, corpus_rows, torch):
    E = mb.model.get_output_embeddings().weight.to(torch.float32)
    defs = []
    z = sae_encode_np(sae, h_corpus, torch, keep_latents=members)
    for j, m in enumerate(members):
        W_dec = sae.W_dec[m].to(torch.float32)
        with torch.no_grad():
            logits = E @ W_dec
            top = torch.topk(logits, 10).indices.cpu().tolist()
        toks = [mb.tok.convert_tokens_to_string([t]).strip() for t in mb.tok.convert_ids_to_tokens(top)]
        # top activating corpus windows for this member
        order = np.argsort(-z[:, j])[:5]
        ctxs = []
        for oi in order:
            if z[oi, j] <= 0:
                break
            ctxs.append({"sub_context": corpus_rows[oi].get("metadata_sub_context", ""),
                         "act": round(float(z[oi, j]), 3)})
        defs.append({"latent": int(m), "role": "anchor" if m == anchor else "absorber",
                     "logit_lens_tokens": toks, "top_corpus_contexts": ctxs})
    return {"letter": letter, "anchor_idx": int(anchor), "absorber_idxs": [int(x) for x in absorbers],
            "members": defs}


# ============================================================================ STEERING
NEUTRAL_PROMPTS = [
    "The weather today is", "I went to the store to buy", "She opened the door and saw",
    "My favorite hobby is", "The most important thing in life is", "When I woke up this morning",
    "The scientist explained that", "He picked up the phone and", "In the middle of the forest there was",
    "The recipe calls for", "They decided to travel to", "The teacher wrote on the board",
    "After the meeting we went to", "The book on the table was about", "Yesterday I learned how to",
    "The children played in the", "Looking out the window I noticed", "The company announced a new",
    "On the way home she stopped at", "The old man told a story about", "During the summer we like to",
    "The first thing I do every day is", "He reached into his pocket and pulled out", "The river flowed past the",
]


def letter_initial_token_ids(tok, letter):
    ids = []
    low = letter.lower(); up = letter.upper()
    vocab = tok.get_vocab()
    for t, i in vocab.items():
        s = tok.convert_tokens_to_string([t]).strip()
        if s and (s[0] == low or s[0] == up):
            ids.append(i)
    return np.array(sorted(set(ids)), dtype=np.int64)


def steering_eval(letter, mb, sae, dirs, h_corpus_other, cfg):
    """dirs: dict name-> unit vector [d_model] (numpy). Returns curves + matched comparison."""
    torch = mb.torch
    tok = mb.tok
    Rnorm = mb.mean_resid_norm(NEUTRAL_PROMPTS)
    Lids = letter_initial_token_ids(tok, letter)
    Lids_t = torch.as_tensor(Lids, dtype=torch.long)   # cpu long tensor for indexing cpu logprob tensors
    log(f"{el()} steering {letter}: Rnorm={Rnorm:.2f} L-initial tokens={len(Lids)}")

    # baseline next-token dist on neutral prompts (no steering)
    def next_tok_logprobs(direction=None, alpha=0.0):
        tok.padding_side = "left"
        outs = []
        handle = None
        if direction is not None:
            dvec = torch.tensor(direction, device=DEVICE, dtype=torch.float32)
            def hook(mod, inp, out):
                h = out[0] if isinstance(out, (tuple, list)) else out
                h = h + (alpha * dvec).to(h.dtype)
                if isinstance(out, (tuple, list)):
                    return (h,) + tuple(out[1:])
                return h
            handle = mb.layer.register_forward_hook(hook)
        try:
            for b0 in range(0, len(NEUTRAL_PROMPTS), 16):
                bp = NEUTRAL_PROMPTS[b0:b0 + 16]
                enc = tok(bp, return_tensors="pt", padding=True, add_special_tokens=True)
                enc = {k: v.to(DEVICE) for k, v in enc.items()}
                with torch.no_grad():
                    o = mb.model(**enc)
                lp = torch.log_softmax(o.logits[:, -1, :].to(torch.float32), dim=-1)
                outs.append(lp.cpu())
        finally:
            if handle:
                handle.remove()
        tok.padding_side = "right"
        return torch.cat(outs, 0)  # [n_prompts, vocab]

    base_lp = next_tok_logprobs(None, 0.0)
    base_p = base_lp.exp()
    base_ontarget = float(base_p[:, Lids_t].sum(1).mean())

    # PPL eval text: other-letter corpus windows (neutral wrt L)
    ppl_texts = h_corpus_other[:64] if isinstance(h_corpus_other, list) else None

    curves = {}
    for name, dvec in dirs.items():
        pts = []
        for c in STEER_C:
            alpha = c * Rnorm
            lp = next_tok_logprobs(dvec, alpha) if c > 0 else base_lp
            p = lp.exp()
            ontarget = float(p[:, Lids_t].sum(1).mean()) - base_ontarget
            # full-vocab KL(steered || base) averaged over prompts
            kl = float((p * (lp - base_lp)).sum(1).mean())
            pts.append({"c": c, "alpha": alpha, "on_target": ontarget, "kl": kl})
        curves[name] = pts
        log(f"  steer[{name}] " + " ".join(f"c{p['c']}:Δ{p['on_target']:.3f}/KL{p['kl']:.3f}" for p in pts))

    # PPL via teacher forcing on neutral text
    ppl_curves = steering_ppl(mb, dirs, Rnorm, cfg)

    # matched comparison: pick target on_target = min over methods of max achievable on_target
    max_on = {n: max(p["on_target"] for p in curves[n]) for n in curves}
    target_level = max(0.02, min(max_on.values()) * 0.8)   # small positive floor avoids degenerate interp
    matched = {}
    for n in curves:
        # interpolate KL at target_level
        xs = [p["on_target"] for p in curves[n]]; ys = [p["kl"] for p in curves[n]]
        order = np.argsort(xs); xs = np.array(xs)[order]; ys = np.array(ys)[order]
        kl_at = float(np.interp(target_level, xs, ys))
        matched[n] = {"on_target": target_level, "kl": kl_at}
    # shuffle null: random direction
    rng = np.random.default_rng(SEED)
    rd = rng.standard_normal(sae.d_model).astype(np.float32); rd /= np.linalg.norm(rd)
    rnd_pts = []
    for c in STEER_C:
        lp = next_tok_logprobs(rd, c * Rnorm) if c > 0 else base_lp
        p = lp.exp()
        rnd_pts.append({"c": c, "on_target": float(p[:, Lids_t].sum(1).mean()) - base_ontarget,
                        "kl": float((p * (lp - base_lp)).sum(1).mean())})
    curves["random"] = rnd_pts

    steering_pass = False
    if "unit" in matched and "diffmean" in matched and "hub" in matched:
        steering_pass = bool(matched["unit"]["kl"] < matched["diffmean"]["kl"] and
                             matched["unit"]["kl"] < matched["hub"]["kl"])
    return {"on_target_curve": curves, "matched_comparison": matched, "ppl": ppl_curves,
            "base_ontarget": base_ontarget, "Rnorm": Rnorm, "STEERING_PASS": steering_pass}


def steering_ppl(mb, dirs, Rnorm, cfg):
    torch = mb.torch
    tok = mb.tok
    texts = NEUTRAL_PROMPTS
    def ppl(direction=None, alpha=0.0):
        handle = None
        if direction is not None:
            dvec = torch.tensor(direction, device=DEVICE, dtype=torch.float32)
            def hook(mod, inp, out):
                h = out[0] if isinstance(out, (tuple, list)) else out
                h = h + (alpha * dvec).to(h.dtype)
                if isinstance(out, (tuple, list)):
                    return (h,) + tuple(out[1:])
                return h
            handle = mb.layer.register_forward_hook(hook)
        losses = []
        try:
            for t in texts:
                enc = tok(t, return_tensors="pt", add_special_tokens=True)
                enc = {k: v.to(DEVICE) for k, v in enc.items()}
                with torch.no_grad():
                    o = mb.model(**enc, labels=enc["input_ids"])
                losses.append(float(o.loss))
        finally:
            if handle:
                handle.remove()
        return float(np.exp(np.mean(losses)))
    out = {}
    base = ppl(None, 0.0)
    out["base"] = base
    for name, dvec in dirs.items():
        pts = []
        for c in STEER_C:
            pts.append({"c": c, "ppl": ppl(dvec, c * Rnorm) if c > 0 else base})
        out[name] = pts
    return out


# ============================================================================ CORPUS PRELOAD
def preload_corpus(mb, sae, groups, letters, cfg):
    """Encode residuals at target token for each letter's corpus windows. Returns dict letter->[n,d_model]."""
    h_corpus = {}
    corpus_rows = {}
    cap = cfg["corpus_cap"]
    for letter in letters:
        rows = [r for r in groups[letter] if r.get("metadata_pair_type") == "corpus_context"]
        rows = rows[:cap]
        inputs = [r["input"] for r in rows]
        spans = [tuple(r["metadata_target_char_in_window"]) for r in rows]
        tids = [int(r["metadata_target_token_id"]) for r in rows]
        log(f"{el()} corpus encode {letter}: {len(inputs)} windows")
        h = mb.resid_at_spans(inputs, spans, check_token_ids=tids)
        h_corpus[letter] = h
        corpus_rows[letter] = rows
    return h_corpus, corpus_rows


# ============================================================================ MAIN
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--letters", default="L,O,T,I,D")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--mini", action="store_true")
    ap.add_argument("--mini_words", type=int, default=12)
    ap.add_argument("--no-steering", action="store_true")     # back-compat (steering is OFF by default now)
    ap.add_argument("--steering", action="store_true",
                    help="opt-in to steering (skipped by default; already executed in iter-2)")
    ap.add_argument("--width", default="16k", choices=["16k", "65k"])
    ap.add_argument("--b_gap", type=int, default=10000)       # B for AUC-difference + accuracy bootstraps (>=10000)
    ap.add_argument("--b_null", type=int, default=1000)
    ap.add_argument("--c_boot", type=int, default=20)
    ap.add_argument("--rek_draws", type=int, default=1000)    # M1 random-eligible-k draw count (200 mini)
    ap.add_argument("--corpus_cap", type=int, default=2500)
    ap.add_argument("--no-superset-surface", action="store_true",
                    help="use the iter-1 inline 590 surface pairs instead of the iter-2 1,700-pair superset")
    ap.add_argument("--out", default="method_out.json")
    args = ap.parse_args()

    cfg = {"mini": args.mini, "mini_words": args.mini_words, "b_gap": args.b_gap,
           "b_null": args.b_null, "c_boot": args.c_boot, "corpus_cap": args.corpus_cap,
           "rek_draws": args.rek_draws, "dump_rmat": False}
    if args.mini:
        cfg["b_gap"] = min(cfg["b_gap"], 1000); cfg["b_null"] = min(cfg["b_null"], 200)
        cfg["c_boot"] = min(cfg["c_boot"], 8); cfg["corpus_cap"] = min(cfg["corpus_cap"], 600)
        cfg["rek_draws"] = min(cfg["rek_draws"], 200)

    import torch
    torch.manual_seed(SEED); np.random.seed(SEED)
    rng = np.random.default_rng(SEED)

    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "full_data_out.json")
    if not os.path.exists(data_path):
        data_path = "/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json"
    meta, groups = load_data(data_path)
    log(f"{el()} data loaded: letters={list(groups.keys())}")

    # STEP 7: enlarged independently-judged first-letter surface superset (iter-2 dataset_1) for admission.
    SUPERSET_PATH = "/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/full_data_out.json"
    surface_overrides = {}
    if not args.no_superset_surface and os.path.exists(SUPERSET_PATH):
        try:
            _, sgroups = load_data(SUPERSET_PATH)
            for l in LETTERS_ALL:
                if l in sgroups:
                    _, surf, _ = build_letter_struct(sgroups[l], SPELLING_CARRIERS)
                    surface_overrides[l] = surf
            log(f"{el()} surface superset loaded (spelling carriers): " +
                ", ".join(f"{l}:{len(surface_overrides.get(l, {}))}pr" for l in LETTERS_ALL))
            del sgroups
        except Exception as e:
            log(f"!!! surface superset load failed ({e!r}); falling back to inline iter-1 surface pairs")
            surface_overrides = {}

    mb = ModelBundle()
    sae = load_sae(SAE_PARAMS_16K if args.width == "16k" else SAE_PARAMS_65K)

    # ---------- GATING CHECK ----------
    gate = gating_check(mb, sae, groups, torch)
    if not gate["pass"]:
        log(f"!!! GATING FAILED cos={gate['cosine']:.3f} EV={gate['ev']:.3f} — trying alt (hidden_states[13])")
        gate2 = gating_check(mb, sae, groups, torch, use_hidden_states=True)
        gate["alt_hidden_states"] = gate2
        if gate2["pass"]:
            log("alt hidden_states[13] passes; but layer-hook should match — continuing with hook (verify).")
    out = {"method_name": "Two-Track CCRG (Counterfactual Co-Response Grouping) -- iter-4 selection isolation",
           "description": ("Cluster-level SAE units (anchor + disjoint per-token absorbers) recovered from "
                           "content-flip co-response on a frozen Gemma-Scope L12/16k SAE; first-letter spelling "
                           "absorption testbed. iter-4 honest-scoping deltas: M5 isolates the two-track SET-COVER "
                           "selection from sensible label-free selection via three NON-RANDOM count-matched selectors "
                           "(S_rec=top-k recall, S_prec=top-k precision, S_mag=top-k magnitude) with paired-bootstrap "
                           "AUC-difference CIs (B>=10,000); M4 adds the unsupervised firing-floor anchor validation "
                           "(rejects the I=1227 0%-corpus spurious anchor), the per-letter JOINT (E1 AND selection), "
                           "and renames the over-aggregating verdict; M7 reports the COMPACT named unit vs the 15-wide "
                           "max-pool (AUC-diff CI + AUC-vs-cumulative-k). E1=label-free recovery vs form-free diagnostic; "
                           "C1=starts-with-letter classification; E2=absorbed-slice recall."),
           "config": {"release": RELEASE_REPO, "sae_params": SAE_PARAMS_16K if args.width == "16k" else SAE_PARAMS_65K,
                      "model": MODEL_ID, "hook_layer": HOOK_LAYER, "spelling_carriers": SPELLING_CARRIERS,
                      "thresholds": {"beta": BETA, "gamma_grid": GAMMA_GRID, "prec_floor": PREC_FLOOR,
                                     "jaccard_max": JACCARD_MAX, "covgain_floor": COVGAIN_FLOOR, "tau_c": TAU_C,
                                     "max_k": MAX_K, "min_hole_headline": MIN_HOLE_HEADLINE,
                                     "anchor_corpus_fire_floor": ANCHOR_CORPUS_FIRE_FLOOR, "compact_max": COMPACT_MAX},
                      "selectors": ["S_rec", "S_prec", "S_mag"], "rek_draws": cfg["rek_draws"],
                      "seed": SEED, "b_gap": cfg["b_gap"], "b_null": cfg["b_null"], "mini": args.mini},
           "gating_check": gate}
    examples_by_letter = {}

    def save_now():
        datasets = []
        for l in examples_by_letter:
            exs = examples_by_letter[l]
            if exs:
                datasets.append({"dataset": f"first_letter_spelling_{l}", "examples": exs})
        if not datasets:   # schema requires >=1 dataset with >=1 example
            datasets = [{"dataset": "first_letter_spelling_pending",
                         "examples": [{"input": "pending", "output": "0"}]}]
        _save({"metadata": out, "datasets": datasets}, args.out)

    if args.smoke:
        save_now()
        log(f"{el()} SMOKE done. gating pass={gate['pass']}")
        return

    letters = [x.strip().upper() for x in args.letters.split(",") if x.strip()]
    # preload corpus residuals for ALL letters (needed for probe negatives)
    h_corpus_all, corpus_rows_all = preload_corpus(mb, sae, groups, LETTERS_ALL, cfg)

    per_letter = {}
    pooled_store = {}   # letter -> {unit_vs_h:{diffs,..}, unit_vs_REk:{..}} ; kept OUT of saved JSON
    for letter in letters:
        try:
            res = run_letter(letter, groups[letter], mb, sae, h_corpus_all, corpus_rows_all, cfg, rng,
                             surface_override=surface_overrides.get(letter), pooled_store=pooled_store)
        except Exception as e:
            import traceback
            log(f"!!! letter {letter} failed: {e}\n{traceback.format_exc()}")
            res = {"letter": letter, "error": str(e)}
        examples_by_letter[letter] = res.pop("examples", []) if isinstance(res, dict) else []
        per_letter[letter] = res
        # incremental save (schema-conformant)
        out["per_letter"] = per_letter
        # incremental pooled-across-letters (so a crash on letter 4-5 still yields decisive pooled CIs)
        out["pooled_across_letters"] = {
            "unit_vs_h": compute_pooled_across_letters(pooled_store, "unit_vs_h"),
            "unit_vs_REk": compute_pooled_across_letters(pooled_store, "unit_vs_REk"),
            "unit_vs_S_rec": compute_pooled_across_letters(pooled_store, "unit_vs_S_rec"),
            "unit_vs_S_prec": compute_pooled_across_letters(pooled_store, "unit_vs_S_prec"),
            "unit_vs_S_mag": compute_pooled_across_letters(pooled_store, "unit_vs_S_mag"),
            "n_letters_sig_h": int(sum(1 for l in per_letter if _sig(per_letter[l], "unit_vs_h"))),
            "n_letters_sig_REk": int(sum(1 for l in per_letter if _sig(per_letter[l], "unit_vs_REk"))),
            "n_letters_sig_S_rec": int(sum(1 for l in per_letter if _sig(per_letter[l], "unit_vs_S_rec"))),
            "n_letters_sig_S_prec": int(sum(1 for l in per_letter if _sig(per_letter[l], "unit_vs_S_prec"))),
            "n_letters_sig_S_mag": int(sum(1 for l in per_letter if _sig(per_letter[l], "unit_vs_S_mag")))}
        save_now()

    # ---------- STEERING (OPT-IN only; skipped by default, already executed in iter-2) ----------
    steering = {}
    if args.steering and not args.no_steering:
        # non-L corpus list for PPL neutrality
        for letter in letters:
            res = per_letter.get(letter, {})
            if "K_UNIT" not in res or not res["K_UNIT"]:
                continue
            try:
                steering[letter] = run_steering_for_letter(letter, res, mb, sae, h_corpus_all, cfg, torch)
            except Exception as e:
                import traceback
                log(f"!!! steering {letter} failed: {e}\n{traceback.format_exc()}")
                steering[letter] = {"error": str(e)}
            out["steering"] = steering
            save_now()
            if letter == PRIMARY and cfg["mini"]:
                break

    # ---------- VERDICTS (M4: per-letter JOINT of E1 AND selection-vs-the-M5-bar; renamed endpoint) ----------
    pooled = out.get("pooled_across_letters", {})
    out["endpoint_reconciliation_note"] = (
        "iter-4 isolates the two-track SET-COVER selection from sensible label-free selection. The primary_endpoint "
        "is keyed off the per-letter JOINT (E1 AND the unit significantly beating BOTH attribution (h) AND ALL THREE "
        "non-random count-matched selectors S_rec/S_prec/S_mag, CI excluding 0): n_joint>=3 => "
        "SET_COVER_SELECTION_CONFIRMED; else (n_joint + eligibility-only >= 3) => "
        "REFRAMED_TO_ELIGIBILITY_AND_SENSIBLE_SELECTION (unit beats attribution via cover-based eligibility + "
        "sensible label-free selection, but the set-cover-SPECIFIC win is not established everywhere); else "
        "SELECTION_NOT_ESTABLISHED. All three are publishable. The iter-3 RE-k floor is retained as a demoted "
        "control. M4 adds the unsupervised firing-floor anchor validation (rejects the I=1227 0%-corpus spurious "
        "anchor); letter I is annotated separately. M7 reports the compact named unit alongside the 15-wide max-pool.")
    out["verdicts"] = build_verdicts(per_letter, steering, pooled)
    out["repro_appendix"] = {
        "torch_cuda_note": "torch 2.8.0+cu128 (host RTX 2000 Ada / sm_89); iter-3 ran on RTX 5090 (sm_120).",
        "auc_drift_note": "tie-aware fast_auc (Mann-Whitney average-rank) used throughout.",
        "code_faithfulness_verified": ("The UNMODIFIED iter-3 method.py was re-run on THIS host and produced numbers "
                                       "IDENTICAL to this iter-4 run for L (unit AUC 0.905, h 0.795, K_UNIT ending in "
                                       "latent 1566, RE-k draw mean 0.651, frac_rek>=unit 0.001), confirming the "
                                       "additive M4/M5/M7 code does NOT perturb the iter-3 pipeline (M5/M7 use SEPARATE "
                                       "child rngs; the firing-floor corpus encode consumes no shared rng)."),
        "reproduction": ("Differences from the STORED iter-3 anchors are bf16 HARDWARE numerics, not code: the greedy "
                         "set-cover hits a near-tie at L's 15th member which resolves to latent 1566 on RTX 2000 Ada "
                         "(vs 1362 on iter-3's RTX 5090), shifting L's unit AUC 0.876->0.905 and making unit>h "
                         "significant here. AUC is rank-based but the DISCRETE greedy membership is tie-sensitive. For "
                         "letter I the validated anchor moves off the 0%-corpus 1227 BY DESIGN, so I's unit + "
                         "downstream change; because the shared rng advances through I differently, D may also differ "
                         "from the stored iter-3 (a legitimate consequence of fixing I).")}
    out["runtime_stats"] = {"total_seconds": round(time.time() - T0, 1)}
    out["unit_definitions"] = [per_letter[l]["unit_definition"] for l in letters
                               if "unit_definition" in per_letter.get(l, {})]
    out["kg_edges"] = [e for l in letters for e in per_letter.get(l, {}).get("kg_edges", [])]
    save_now()
    log(f"{el()} DONE. verdict={out['verdicts'].get('primary_endpoint')}")


def run_steering_for_letter(letter, res, mb, sae, h_corpus_all, cfg, torch):
    members = res["K_UNIT"]; anchor = res["anchor_idx"]
    W_dec = sae.W_dec.cpu().numpy()
    d_unit = W_dec[members].mean(0); d_unit /= (np.linalg.norm(d_unit) + 1e-9)
    d_hub = W_dec[anchor].copy(); d_hub /= (np.linalg.norm(d_hub) + 1e-9)
    # non-SAE diff-of-means on INDEPENDENT corpus data
    pos = h_corpus_all[letter]
    neg = np.concatenate([h_corpus_all[o] for o in h_corpus_all if o != letter], 0)
    d_dm = pos.mean(0) - neg.mean(0); d_dm /= (np.linalg.norm(d_dm) + 1e-9)
    dirs = {"unit": d_unit, "hub": d_hub, "diffmean": d_dm}
    other = [o for o in h_corpus_all if o != letter]
    return steering_eval(letter, mb, sae, dirs, None, cfg)


def gating_check(mb, sae, groups, torch, use_hidden_states=False):
    rows = [r for r in groups[PRIMARY] if r.get("metadata_pair_type") == "corpus_context"][:64]
    inputs = [r["input"] for r in rows]
    spans = [tuple(r["metadata_target_char_in_window"]) for r in rows]
    tids = [int(r["metadata_target_token_id"]) for r in rows]
    if use_hidden_states:
        h = _resid_hidden_states(mb, inputs, spans, tids, torch)
    else:
        h = mb.resid_at_spans(inputs, spans, check_token_ids=tids)
    hb = torch.tensor(h, device=DEVICE, dtype=torch.float32)
    z = sae.encode(hb)
    hr = sae.decode(z)
    cos = float(torch.nn.functional.cosine_similarity(hb, hr, dim=-1).mean())
    resid_var = (hb - hr).var().item(); tot_var = hb.var().item()
    ev = 1 - resid_var / (tot_var + 1e-9)
    l0 = float((z > 0).sum(1).float().mean())
    log(f"{el()} GATING (hidden_states={use_hidden_states}): cosine={cos:.4f} EV={ev:.4f} L0={l0:.1f}")
    return {"pass": bool(cos > 0.9 and ev > 0.5), "cosine": cos, "ev": ev, "L0": l0}


def _resid_hidden_states(mb, inputs, spans, tids, torch, batch=32):
    out = np.zeros((len(inputs), mb.d_model), dtype=np.float32)
    for b0 in range(0, len(inputs), batch):
        bi = inputs[b0:b0 + batch]; bs = spans[b0:b0 + batch]
        enc = mb.tok(bi, return_offsets_mapping=True, return_tensors="pt", padding=True,
                     truncation=True, max_length=128, add_special_tokens=True)
        offs = enc.pop("offset_mapping")
        enc = {k: v.to(DEVICE) for k, v in enc.items()}
        with torch.no_grad():
            o = mb.model(**enc, output_hidden_states=True)
        h = o.hidden_states[HOOK_LAYER + 1].to(torch.float32)
        for j in range(len(bi)):
            tidx = _find_token_idx(offs[j].tolist(), bs[j])
            out[b0 + j] = h[j, max(tidx, 1)].cpu().numpy()
    return out


def _c1_auc_win(res):
    """Legacy AUC-point dominance (iter-2 'C1_WIN' definition), kept for transparency only."""
    pm = res.get("C1", {}).get("per_method", {})
    if "unit" not in pm:
        return None
    u = pm["unit"]["AUC"]
    load = [pm[b]["AUC"] for b in ["b", "c", "h"] if b in pm]   # count-matched, load-bearing
    allb = [pm[b]["AUC"] for b in ["a", "b", "c", "h"] if b in pm]
    return bool(all(u >= x for x in allb) and all(u > x for x in load))


def _sig(res, comp):
    """sig_unit_better (CI lower bound > 0) for a C1 AUC-difference comparison."""
    return bool(res.get("C1", {}).get("auc_diff", {}).get(comp, {}).get("sig_unit_better", False))


def compute_pooled_across_letters(pooled_store, comparison):
    """Stratified meta-analysis over letters for one comparison ('unit_vs_h' | 'unit_vs_REk').
    (a) stratified cluster bootstrap (PRIMARY): weighted (by test-pair count) mean of the per-letter
        bootstrap diff distributions -> pooled CI. (b) fixed-effect inverse-variance meta -> z, p."""
    from scipy.stats import norm
    entries = []
    for l, pd in pooled_store.items():
        e = pd.get(comparison)
        if e is None or e.get("diffs") is None:
            continue
        diffs = np.asarray(e["diffs"], dtype=np.float64)
        if diffs.size == 0:
            continue
        entries.append((l, diffs, float(e.get("n_test_pairs", 1)), float(e.get("point", float(diffs.mean())))))
    if not entries:
        return {"note": "no per-letter diffs available", "n_letters": 0}
    B = min(e[1].size for e in entries)
    letters = [e[0] for e in entries]
    W = np.array([e[2] for e in entries], dtype=np.float64); W = W / W.sum()
    M = np.stack([e[1][:B] for e in entries], axis=0)             # [n_letters, B]
    pooled_dist = (W[:, None] * M).sum(0)                         # weighted-mean diff per bootstrap index
    lo, hi = np.percentile(pooled_dist, [2.5, 97.5])
    pts = np.array([e[3] for e in entries])                       # per-letter observed diff (point)
    point_w = float((W * pts).sum())
    ses = np.array([e[1].std() for e in entries])
    var = ses ** 2; ok = var > 1e-12
    if ok.sum() >= 1:
        comb = float((pts[ok] / var[ok]).sum() / (1.0 / var[ok]).sum())
        se_comb = float(np.sqrt(1.0 / (1.0 / var[ok]).sum()))
        z = comb / se_comb if se_comb > 0 else 0.0
        p = float(2.0 * (1.0 - norm.cdf(abs(z))))
    else:
        comb, se_comb, z, p = float(pts.mean()), 0.0, 0.0, 1.0
    return {
        "stratified_bootstrap": {"diff": point_w, "ci_lo": float(lo), "ci_hi": float(hi),
                                 "excl_0": bool(lo > 0 or hi < 0), "sig_unit_better": bool(lo > 0), "B": int(B),
                                 "per_letter_weights": {letters[i]: float(W[i]) for i in range(len(letters))}},
        "inverse_variance": {"diff": comb, "se": se_comb, "z": float(z), "p": p,
                             "sig_unit_better": bool(z > 0 and p < 0.05)},
        "per_letter_point": {letters[i]: float(pts[i]) for i in range(len(letters))},
        "n_letters": len(entries)}


def build_verdicts(per_letter, steering, pooled):
    """M4: primary_endpoint from the per-letter JOINT -- E1 AND the unit beating BOTH (h) AND ALL THREE
    non-random count-matched selectors S_rec/S_prec/S_mag (CI excluding 0). E1, E2 and the demoted RE-k
    floor are reported transparently; the iter-3 over-aggregating verdict moves to legacy_iter3_verdict."""
    letters = [l for l in LETTERS_ALL if l in per_letter]
    def si(l):
        return per_letter[l].get("selection_isolation", {})
    def beats(l, X):
        return bool(si(l).get("unit_beats", {}).get(X))
    per_E1 = {l: bool(per_letter[l].get("E1", {}).get("E1_PASS")) for l in per_letter}
    per_E2 = {l: bool(per_letter[l].get("E2", {}).get("E2_PASS")) for l in per_letter}
    sel_pass = {l: bool(beats(l, "h") and si(l).get("beats_all_M5")) for l in letters}   # the M5 bar
    elig_only = {l: bool(beats(l, "h") and not si(l).get("beats_all_M5")) for l in letters}
    joint = {l: bool(per_E1.get(l) and sel_pass[l]) for l in letters}
    n_E1 = sum(1 for l in letters if per_E1.get(l))
    n_sel = sum(1 for l in letters if sel_pass[l])
    n_joint = sum(1 for l in letters if joint[l])
    n_elig = sum(1 for l in letters if elig_only[l])
    if n_joint >= 3:
        endpoint = "SET_COVER_SELECTION_CONFIRMED"
    elif (n_joint + n_elig) >= 3 and n_joint < 3:
        endpoint = "REFRAMED_TO_ELIGIBILITY_AND_SENSIBLE_SELECTION"
    else:
        endpoint = "SELECTION_NOT_ESTABLISHED"

    # legacy iter-3 over-aggregating rule (recorded, NOT the headline): E1>=4 AND unit beats h AND RE-k on >=3
    legacy_sel = {l: bool(beats(l, "h") and beats(l, "REk")) for l in letters}
    legacy_n_sel = sum(1 for l in letters if legacy_sel[l])
    n_beats_h = sum(1 for l in letters if beats(l, "h"))
    if n_E1 >= 4 and legacy_n_sel >= 3:
        legacy_endpoint = "ABSORPTION_REPAIR_SELECTION_CONFIRMED"
    elif legacy_n_sel < 3 and n_beats_h >= 3:
        legacy_endpoint = "REFRAMED_TO_ELIGIBILITY_POOLING"
    else:
        legacy_endpoint = "SELECTION_NOT_ESTABLISHED"

    c1_table = {}
    for l in letters:
        pm = per_letter[l].get("C1", {}).get("per_method", {})
        ad = per_letter[l].get("C1", {}).get("auc_diff", {})
        row = {"unit_AUC": pm.get("unit", {}).get("AUC")}
        for X in ["a", "b", "c", "h", "REk", "S_rec", "S_prec", "S_mag",
                  "unit_compact", "unit_15wide", "anchor_only"]:
            row[f"{X}_AUC"] = pm.get(X, {}).get("AUC")
        for X in ["h", "REk", "S_rec", "S_prec", "S_mag"]:
            cd = ad.get(f"unit_vs_{X}", {})
            row[f"unit_vs_{X}"] = {k: cd.get(k) for k in ("diff", "ci_lo", "ci_hi", "sig_unit_better")}
        c1_table[l] = row
    rek_table = {l: per_letter[l].get("C1", {}).get("rek_distribution", {}) for l in letters}
    iso_table = {l: si(l) for l in letters}
    compact_table = {l: {k: per_letter[l].get("compact_vs_wide", {}).get(k)
                         for k in ("compact_label", "n_named_of_15", "frac_named",
                                   "unit_compact", "unit_15wide", "anchor_only", "compact_minus_15wide")}
                     for l in letters}

    I_av = per_letter.get("I", {}).get("anchor_validation", {})
    I_e1 = bool(per_letter.get("I", {}).get("E1", {}).get("E1_PASS"))
    I_changed = bool(I_av.get("anchor_changed"))
    if "I" not in per_letter:
        i_note = "letter I not run."
    elif I_changed and I_e1:
        i_note = (f"firing-floor validation moved I's anchor off the 0%-corpus raw {I_av.get('raw_recall_argmax_global')} "
                  f"to {I_av.get('validated_anchor_global')} (corpus fire={I_av.get('validated_anchor_corpus_fire')}); "
                  "E1 now PASSES for I -- the firing-floor fix RECOVERED I's absorption mechanism (the iter-3 bug it fixes).")
    elif I_changed and not I_e1:
        i_note = (f"firing-floor validation moved I's anchor off the 0%-corpus raw {I_av.get('raw_recall_argmax_global')} "
                  f"to {I_av.get('validated_anchor_global')}, but E1 still FAILS (no >=2 corroborated absorbers): I is a "
                  "SELECTION win WITHOUT a confirmed absorption mechanism -- reported separately; counted in n_joint only "
                  "if E1 passes (it does not here).")
    else:
        i_note = "I's raw recall-argmax anchor already passes the firing floor; no change."

    e2_true = [l for l in letters if per_E2.get(l)]
    e1_fail = [l for l in letters if not per_E1.get(l)]
    return {
        "primary_endpoint": endpoint,
        "n_E1_pass": n_E1, "n_selection_vs_M5": n_sel, "n_joint_E1_and_selection": n_joint,
        "n_eligibility_only": n_elig,
        "selection_bar": ("unit AUC significantly above (CI excl 0) BOTH attribution (h) AND ALL THREE non-random "
                          "count-matched selectors S_rec/S_prec/S_mag"),
        "per_letter_joint": joint,
        "per_letter_selection_vs_M5": sel_pass,
        "per_letter_eligibility_only": elig_only,
        "per_letter_E1": per_E1,
        "per_letter_E1_note": f"E1 PASS on {n_E1}/{len(letters)} letters; fails on {e1_fail}.",
        "per_letter_E2": per_E2,
        "per_letter_E2_note": f"E2 (count-matched absorbed-slice recall) reported INDEPENDENTLY; E2 PASS only on {e2_true}.",
        "set_cover_isolation_table": iso_table,
        "c1_auc_table": c1_table,
        "rek_distribution_table": rek_table,
        "compact_vs_wide_table": compact_table,
        "letter_I_annotation": i_note,
        "pooled_across_letters": pooled,
        "STEERING_PASS": (bool(steering.get(PRIMARY, {}).get("STEERING_PASS", False)) if steering else None),
        "legacy_iter3_verdict": {
            "value": legacy_endpoint,
            "iter3_recorded_value": "ABSORPTION_REPAIR_SELECTION_CONFIRMED",
            "per_letter_selection_unit_beats_h_and_REk": legacy_sel,
            "n_selection_h_and_REk": legacy_n_sel,
            "why_replaced": ("over-aggregated: it required only E1 AND unit>both(h) AND RE-k on >=3/5, but RE-k is an "
                             "easy floor (median draw AUC ~0.63-0.69, at/below the best single latent; frac_rek>=unit "
                             "<=0.009). The honest object is the per-letter JOINT of E1 AND beating the NON-RANDOM "
                             "count-matched selectors S_rec/S_prec/S_mag, which pick sensible label-free pools.")},
        "legacy_iter2_view": {
            "C1_AUC_point_win_per_letter": {l: _c1_auc_win(per_letter[l]) for l in letters},
            "iter2_endpoint_rule": "WORKS = (E1 AND C1_AUC_point_win), E2 DROPPED from the conjunction"}}


def _json_default(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.ndarray,)):
        return o.tolist()
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return str(o)


def _save(out, path):
    with open(path, "w") as f:
        json.dump(out, f, indent=1, default=_json_default)


if __name__ == "__main__":
    main()
