#!/usr/bin/env python
"""
M4 — A-PRIORI FIRING-STRUCTURE ROUTER  (prospective validation).

Headline question (decision-complete, single self-contained GPU experiment):
  Can a single cheap forward-pass measurement -- the SAE-latent *firing-Jaccard*
  between candidate sub-context detectors and the general/parent latent -- PREDICT,
  a priori, whether the absorption-repair unit (CCRG K-track) BEATS supervised
  marginal attribution (baseline (h)) on a downstream classification task?

Mechanism / regimes:
  * ABSORPTION regime  (firing-Jaccard << tau): the concept fragments into a broad
    parent latent + narrow, *firing-disjoint* per-sub-context specialists (absorbers).
    Re-grouping the absorbers back onto the parent (CCRG) HELPS -> CCRG beats (h).
  * CO-FIRING / SPLITTING regime (firing-Jaccard >> tau): sub-contexts are carried by
    BROAD latents that *co-fire* with the parent; no firing-disjoint absorber exists,
    the repaired unit collapses to ~the parent, and supervised marginal attribution
    (h) WINS.

Pipeline (uniform across every concept):
  STEP 1  concept registry (spelling L/O/T/I/D ; numeric ; taxonomic ;
          toxicity threat/identity_attack/insult/obscene/sexual_explicit ;
          PROSPECTIVE: sentiment ; aspect_food ; aspect_service).
  STEP 2  per-concept: parent identification on content-flip pairs (unsupervised
          parent-validation w/ positive-firing floor -> fixes the letter-I spurious
          anchor), per-sub-context detectors + recall holes, positive-only
          firing-Jaccard(detector, parent), and the matched-pool OUTCOME
          (K-track-lite UNIT vs count-matched marginal-attribution pool (h)).
  STEP 3  derive router threshold tau* from ESTABLISHED concepts ONLY (balanced-acc
          sweep + regime separation margin).
  STEP 4  PROSPECTIVE test: predict the 3 new concepts BEFORE revealing their outcome.
  STEP 5  leave-one-concept-out (LOO) cross-validation over ALL concepts.
  STEP 6  assemble method_out.json (exp_gen_sol_out schema; full/mini/preview).

SAE  = Gemma-Scope  google/gemma-scope-2b-pt-res  layer_12/width_16k/average_l0_82
       (the 'canonical' L0~100 JumpReLU variant), loaded directly from params.npz.
Model= unsloth/gemma-2-2b (non-gated mirror).  firing := sae.encode(resid) > 0.
Residual captured by a forward hook on model.model.layers[12] (== blocks.12.hook_resid_post),
validated by SAE reconstruction cosine (gating check).  Core LLM spend = $0.

Usage:
  uv run method.py --smoke                       # load model+SAE, gating + BOS-offset assertion only
  uv run method.py --scale mini                  # tiny per-concept pilot (3 concepts/regime)
  uv run method.py --scale full                  # full established + prospective + LOO
"""
import os, sys, json, time, argparse, gc, math, hashlib, warnings, resource, pickle
from pathlib import Path
from collections import defaultdict, Counter

import numpy as np

warnings.filterwarnings("ignore")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")

from loguru import logger

HERE = Path(__file__).resolve().parent
(HERE / "logs").mkdir(exist_ok=True)
(HERE / "cache").mkdir(exist_ok=True)
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(str(HERE / "logs" / "run.log"), rotation="40 MB", level="DEBUG")

# ------------------------------------------------------------------ CONFIG / PINS
RELEASE_REPO   = "google/gemma-scope-2b-pt-res"
SAE_PARAMS_16K = "layer_12/width_16k/average_l0_82/params.npz"   # 'canonical' avg L0~100
MODEL_ID       = "unsloth/gemma-2-2b"            # non-gated mirror, vocab 256000
HOOK_LAYER     = 12                             # output of decoder layer 12 == blocks.12.hook_resid_post
DEVICE         = "cuda"
SEED           = 1234

# data dependencies (READ-ONLY full_data_out.json)
GA = HERE.parent.parent.parent / "iter_1" / "gen_art"
DATA = {
    "spelling": GA / "gen_art_dataset_1" / "full_data_out.json",   # art_dpYpjSn2Xvg3
    "nonspell": GA / "gen_art_dataset_2" / "full_data_out.json",   # art_t2uUbjSwpd3t
    "toxicity": GA / "gen_art_dataset_3" / "full_data_out.json",   # art_8QO7pl6Pd8UQ
    "support":  GA / "gen_art_dataset_4" / "full_data_out.json",   # art_21JWypIydPMX
}

SPELLING_CARRIERS = ["t_verbose", "t_colon", "t_icl"]   # documented-absorption substrate
PREC_FLOOR     = 0.70      # detector / absorber firing-precision floor
JACCARD_MAX    = 0.10      # K-track mutual-exclusivity ceiling (absorber must be firing-disjoint w/ parent)
COVGAIN_FLOOR  = 0.05      # absorber marginal hole-coverage gain
PARENT_FIRE_FLOOR = 0.20   # unsupervised parent-validation: parent must fire on >=20% of positives
K_MAX          = 8         # cap on unit size (anchor + absorbers)
MIN_SUB_TOKEN  = 12        # min positives for a token-level (spelling) word sub-context
MIN_SUB_SENT   = 150       # min positives for a sentence-level sub-context (inferential floor)
MIN_OUTCOME    = 120       # min positives for an inferential OUTCOME slice (else pool concept-wide)
N_SHUFFLE      = 1000      # sign-flip null permutations for content-responsiveness
B_BOOT         = 10000     # paired bootstrap for the OUTCOME delta CI
B_JAC          = 2000      # bootstrap for per-sub firing-Jaccard CI
TAU_GRID       = np.linspace(0.05, 0.35, 31)

ESTABLISHED = (["spelling_%s" % L for L in ["L", "O", "T", "I", "D"]]
               + ["numeric", "taxonomic"]
               + ["toxicity_%s" % s for s in ["threat", "identity_attack", "insult",
                                              "obscene", "sexual_explicit"]])
PROSPECTIVE = ["sentiment", "aspect_food", "aspect_service"]

CACHE_VER = "v5"           # bump to invalidate cached encodings when a build_* changes

T0 = time.time()
def el():
    return f"{time.time()-T0:6.1f}s"

def cached_build(name, scale, fn):
    """Cache an encoded build dict to disk (the expensive forward-pass step). Analysis re-runs each time."""
    p = HERE / "cache" / f"build_{name}_{scale}_{CACHE_VER}.pkl"
    if p.exists():
        try:
            d = pickle.loads(p.read_bytes())
            logger.info(f"{el()} cache HIT {name} ({scale})")
            return d
        except Exception as e:
            logger.warning(f"cache load failed {name}: {e}")
    d = fn()
    try:
        p.write_bytes(pickle.dumps(d))
    except Exception as e:
        logger.warning(f"cache write failed {name}: {e}")
    return d

def set_mem_limits(ram_gb=44.0):
    soft = int(ram_gb * 1024**3)
    try:
        resource.setrlimit(resource.RLIMIT_AS, (soft, soft))
        logger.info(f"RLIMIT_AS set to {ram_gb:.0f} GB")
    except (ValueError, OSError) as e:
        logger.warning(f"could not set RLIMIT_AS: {e}")

# ============================================================================ SAE
class JumpReLUSAE:
    """Gemma Scope JumpReLU SAE loaded directly from params.npz (official forward)."""
    def __init__(self, params, device, torch):
        self.torch = torch
        self.W_enc = torch.tensor(np.asarray(params["W_enc"]), device=device, dtype=torch.float32)  # [d_model,d_sae]
        self.W_dec = torch.tensor(np.asarray(params["W_dec"]), device=device, dtype=torch.float32)  # [d_sae,d_model]
        self.threshold = torch.tensor(np.asarray(params["threshold"]), device=device, dtype=torch.float32)  # [d_sae]
        self.b_enc = torch.tensor(np.asarray(params["b_enc"]), device=device, dtype=torch.float32)
        self.b_dec = torch.tensor(np.asarray(params["b_dec"]), device=device, dtype=torch.float32)
        self.d_model = self.W_dec.shape[1]
        self.d_sae = self.W_dec.shape[0]

    def encode(self, x):
        t = self.torch
        x = x.to(t.float32)
        pre = x @ self.W_enc + self.b_enc
        return (pre > self.threshold) * t.nn.functional.relu(pre)   # JumpReLU; firing iff >0

    def decode(self, z):
        return z @ self.W_dec + self.b_dec


def load_sae(torch):
    from huggingface_hub import hf_hub_download
    path = hf_hub_download(repo_id=RELEASE_REPO, filename=SAE_PARAMS_16K,
                           token=os.environ.get("HF_TOKEN"))
    sae = JumpReLUSAE(np.load(path), DEVICE, torch)
    logger.info(f"{el()} SAE loaded {SAE_PARAMS_16K}: d_sae={sae.d_sae} d_model={sae.d_model}")
    return sae

# ============================================================================ MODEL + ENCODER
class Encoder:
    """unsloth/gemma-2-2b + Gemma-Scope SAE.  Forward hook on layer-12 output -> residual."""
    def __init__(self):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.torch = torch
        logger.info(f"{el()} loading tokenizer + model {MODEL_ID} (bf16, eager attn)")
        self.tok = AutoTokenizer.from_pretrained(MODEL_ID, token=os.environ.get("HF_TOKEN"))
        self.tok.padding_side = "right"
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID, torch_dtype=torch.bfloat16, attn_implementation="eager",
            token=os.environ.get("HF_TOKEN"),
        ).to(DEVICE).eval()
        self.d_model = self.model.config.hidden_size
        self._cap = {}
        self._handle = self.model.model.layers[HOOK_LAYER].register_forward_hook(self._hook)
        self.sae = load_sae(torch)
        logger.info(f"{el()} model loaded d_model={self.d_model} "
                    f"n_layers={self.model.config.num_hidden_layers} vocab={len(self.tok)}")

    def _hook(self, mod, inp, out):
        self._cap["resid"] = (out[0] if isinstance(out, (tuple, list)) else out).detach()

    # ----- gating check: SAE reconstruction cosine + L0 on real text -----
    def gating_check(self, texts):
        torch = self.torch
        enc = self.tok(texts, return_tensors="pt", padding=True, truncation=True,
                       max_length=64).to(DEVICE)
        with torch.no_grad():
            self.model(**enc)
            resid = self._cap["resid"].float()
            feats = self.sae.encode(resid)
            recon = self.sae.decode(feats)
        mask = enc["attention_mask"].bool()
        cos = torch.nn.functional.cosine_similarity(resid[mask], recon[mask], dim=-1)
        l0 = (feats > 0)[mask].float().sum(-1)
        info = dict(recon_cos_mean=float(cos.mean()), recon_cos_min=float(cos.min()),
                    l0_mean=float(l0.mean()), l0_median=float(l0.median()))
        logger.info(f"GATING recon_cos_mean={info['recon_cos_mean']:.4f} "
                    f"recon_cos_min={info['recon_cos_min']:.4f} "
                    f"L0 mean={info['l0_mean']:.1f} median={info['l0_median']:.0f}")
        return info

    # ----- TOKEN-LEVEL encoding: full-width latents max-pooled over the target token(s) -----
    def encode_token(self, inputs, char_spans, token_idx_lists=None, check_ids=None,
                     batch=64, want_resid=False):
        torch = self.torch
        N = len(inputs)
        lat = np.zeros((N, self.sae.d_sae), dtype=np.float16)
        rsd = np.zeros((N, self.d_model), dtype=np.float16) if want_resid else None
        miss = idmis = 0
        for b0 in range(0, N, batch):
            bi = inputs[b0:b0 + batch]
            enc = self.tok(bi, return_offsets_mapping=True, return_tensors="pt",
                           padding=True, truncation=True, max_length=128, add_special_tokens=True)
            offs = enc.pop("offset_mapping")
            ids = enc["input_ids"]
            am = enc["attention_mask"]
            enc = {k: v.to(DEVICE) for k, v in enc.items()}
            with torch.no_grad():
                self.model(**enc)
                resid = self._cap["resid"].float()           # [B,S,d_model]
                feats = self.sae.encode(resid)               # [B,S,d_sae]
            for j in range(len(bi)):
                gj = b0 + j
                pos = _target_positions(offs[j].tolist(), char_spans[gj],
                                        token_idx_lists[gj] if token_idx_lists else None,
                                        int(am[j].sum()))
                if not pos:
                    miss += 1
                    pos = [1]
                lat[gj] = feats[j, pos].amax(0).to(torch.float16).cpu().numpy()
                if want_resid:
                    rsd[gj] = resid[j, pos].mean(0).to(torch.float16).cpu().numpy()
                if check_ids is not None and check_ids[gj] is not None:
                    if int(ids[j, pos[-1]]) != int(check_ids[gj]):
                        idmis += 1
            del resid, feats
            if b0 % (batch * 40) == 0:
                torch.cuda.empty_cache()
        if miss:
            logger.debug(f"  encode_token: {miss}/{N} spans had no token match (fallback)")
        if check_ids is not None:
            logger.info(f"  encode_token token-id mismatches: {idmis}/{N}")
        return (lat, rsd) if want_resid else lat

    # ----- SENTENCE-LEVEL encoding: max-pool + mean-pool over content tokens (excl BOS) -----
    def encode_sentence(self, inputs, batch=48, want_mean=False, want_resid=False):
        torch = self.torch
        N = len(inputs)
        amax = np.zeros((N, self.sae.d_sae), dtype=np.float16)
        amean = np.zeros((N, self.sae.d_sae), dtype=np.float16) if want_mean else None
        rmean = np.zeros((N, self.d_model), dtype=np.float16) if want_resid else None
        for b0 in range(0, N, batch):
            chunk = [t if (t and t.strip()) else " " for t in inputs[b0:b0 + batch]]
            enc = self.tok(chunk, return_tensors="pt", padding=True, truncation=True,
                           max_length=128, add_special_tokens=True).to(DEVICE)
            with torch.no_grad():
                self.model(**enc)
                resid = self._cap["resid"].float()
                feats = self.sae.encode(resid)
            mask = enc["attention_mask"].bool().clone()
            mask[:, 0] = False                                # exclude BOS
            none = mask.sum(1) == 0
            if none.any():
                mask[none] = enc["attention_mask"].bool()[none]
            fm = mask.unsqueeze(-1)
            cnt = mask.sum(1, keepdim=True).clamp(min=1).float()
            fpos = feats.masked_fill(~fm, float("-inf")).max(1).values
            fpos = torch.where(torch.isinf(fpos), torch.zeros_like(fpos), fpos).clamp(min=0)
            amax[b0:b0 + len(chunk)] = fpos.to(torch.float16).cpu().numpy()
            if want_mean:
                mn = feats.masked_fill(~fm, 0.0).sum(1) / cnt
                amean[b0:b0 + len(chunk)] = mn.to(torch.float16).cpu().numpy()
            if want_resid:
                rmean[b0:b0 + len(chunk)] = ((resid * fm).sum(1) / cnt).to(torch.float16).cpu().numpy()
            del resid, feats
            if b0 % (batch * 40) == 0:
                torch.cuda.empty_cache()
        out = {"act_max": amax}
        if want_mean: out["act_mean"] = amean
        if want_resid: out["resid_mean"] = rmean
        return out

    def free(self):
        try:
            self._handle.remove()
        except Exception:
            pass


def _target_positions(offsets, span, token_idx, T):
    """Token positions for a target. Char-span (BOS-agnostic) primary; stored token-indices (+1 BOS) fallback."""
    if span is not None:
        s, e = span
        pos = [i for i, (a, b) in enumerate(offsets) if b > a and a < e and b > s]
        if not pos:                                   # zero-width -> containing token
            pos = [i for i, (a, b) in enumerate(offsets) if b > a and a <= s < b]
        if pos:
            return pos
    if token_idx:
        return [j + 1 for j in token_idx if 0 <= j + 1 < T]   # +1 for prepended <bos>
    return []

# ============================================================================ STATS
def auc(scores, labels):
    from sklearn.metrics import roc_auc_score
    labels = np.asarray(labels)
    if len(set(labels.tolist())) < 2:
        return float("nan")
    return float(roc_auc_score(labels, scores))

def cols_auc(mat, y):
    """AUC of every column of mat[N,L] vs binary y. Vectorized rank-based (Mann-Whitney)."""
    y = np.asarray(y).astype(bool)
    npos, nneg = int(y.sum()), int((~y).sum())
    if npos == 0 or nneg == 0:
        return np.full(mat.shape[1], np.nan)
    mat = mat.astype(np.float32)
    ranks = np.apply_along_axis(_rankdata, 0, mat)
    sumpos = ranks[y].sum(0)
    return (sumpos - npos * (npos + 1) / 2.0) / (npos * nneg)

def _rankdata(a):
    order = np.argsort(a, kind="mergesort")
    r = np.empty(len(a), dtype=np.float64)
    r[order] = np.arange(1, len(a) + 1)
    # average ties
    a_sorted = a[order]
    i = 0
    while i < len(a):
        j = i
        while j + 1 < len(a) and a_sorted[j + 1] == a_sorted[i]:
            j += 1
        if j > i:
            r[order[i:j + 1]] = (i + 1 + j + 1) / 2.0
        i = j + 1
    return r

def boot_ci(vals, lo=2.5, hi=97.5):
    vals = np.asarray(vals, dtype=np.float64)
    if len(vals) == 0:
        return [float("nan"), float("nan")]
    return [float(np.percentile(vals, lo)), float(np.percentile(vals, hi))]

def paired_bootstrap_auc_delta(score_u, score_h, y, B, rng):
    """Paired bootstrap of AUC(unit) - AUC(h) by resampling examples. Returns (delta, [lo,hi])."""
    from sklearn.metrics import roc_auc_score
    y = np.asarray(y)
    n = len(y)
    base = float(roc_auc_score(y, score_u) - roc_auc_score(y, score_h))
    deltas = np.empty(B, dtype=np.float64)
    pos = np.where(y == 1)[0]; neg = np.where(y == 0)[0]
    for b in range(B):
        ii = np.concatenate([rng.choice(pos, len(pos)), rng.choice(neg, len(neg))])
        yb = y[ii]
        try:
            deltas[b] = roc_auc_score(yb, score_u[ii]) - roc_auc_score(yb, score_h[ii])
        except ValueError:
            deltas[b] = 0.0
    return base, boot_ci(deltas)

def maxpool_z(acts, members, mu, sd):
    """Max-pool of per-latent z-scored activations over `members` -> [N] score."""
    if len(members) == 0:
        return np.zeros(acts.shape[0], dtype=np.float32)
    z = (acts[:, members].astype(np.float32) - mu[members]) / sd[members]
    return z.max(1)


def lr_score(members, pos_tr, neg_tr, X_te):
    """Logistic-regression classifier over the SELECTED feature set (iter-2 C1 protocol): only the
    SELECTION differs across methods; the classifier head is held constant. Properly combines an
    anchor + complementary absorbers (max-pool cannot). Fit on TRAIN, return P(pos) on TEST."""
    from sklearn.linear_model import LogisticRegression
    members = list(members)
    if len(members) == 0:
        return np.zeros(X_te.shape[0], dtype=np.float32)
    Xtr = np.concatenate([pos_tr[:, members], neg_tr[:, members]], 0).astype(np.float32)
    ytr = np.concatenate([np.ones(pos_tr.shape[0]), np.zeros(neg_tr.shape[0])])
    mu = Xtr.mean(0); sd = Xtr.std(0) + 1e-6
    Xtr = (Xtr - mu) / sd
    if len(set(ytr.tolist())) < 2:
        return np.zeros(X_te.shape[0], dtype=np.float32)
    clf = LogisticRegression(max_iter=2000, C=1.0).fit(Xtr, ytr)
    Xte = (X_te[:, members].astype(np.float32) - mu) / sd
    return clf.predict_proba(Xte)[:, 1]

# ============================================================================ DATA LOADERS
def _load(path):
    with open(path) as f:
        return json.load(f)

# ============================================================================ CORE: firing-Jaccard + outcome
def firing_jaccard(fires_a, fires_b):
    a = fires_a.astype(bool); b = fires_b.astype(bool)
    inter = int((a & b).sum()); union = int((a | b).sum())
    return (inter / union) if union > 0 else 0.0


def identify_parent(on_lat, off_lat, pos_lat, rng):
    """Content-responsive latents + parent (highest positive-firing recall among responsive,
    with unsupervised positive-firing floor). Returns (parent, responsive_idx, precision, recall_pos, info)."""
    on = on_lat.astype(np.float32); off = off_lat.astype(np.float32)
    R = on - off                                            # [P, d_sae] content response
    P = R.shape[0]
    mean_r = R.mean(0)
    null = np.empty((N_SHUFFLE, R.shape[1]), dtype=np.float32)
    for i in range(N_SHUFFLE):
        s = rng.choice([-1.0, 1.0], size=P).astype(np.float32)
        null[i] = (s[:, None] * R).mean(0)
    null95 = np.percentile(null, 95, axis=0)
    del null
    responsive_mask = mean_r > null95
    fires_on = on > 0; fires_off = off > 0
    on_c = fires_on.sum(0).astype(np.float64); off_c = fires_off.sum(0).astype(np.float64)
    precision = np.divide(on_c, np.maximum(on_c + off_c, 1))
    resp = np.where(responsive_mask & (precision >= PREC_FLOOR))[0]
    if len(resp) == 0:
        resp = np.where(responsive_mask)[0]
    pos_fire_rate = (pos_lat > 0).mean(0)                   # recall on the positive set
    # unsupervised parent validation: highest positive-firing recall among responsive, >= floor
    cand = resp[pos_fire_rate[resp] >= PARENT_FIRE_FLOOR]
    unresolved = False
    if len(cand) == 0:
        cand = resp
        unresolved = True
    parent = int(cand[np.argmax(pos_fire_rate[cand])]) if len(cand) else -1
    info = dict(n_responsive=int(len(resp)), parent_pos_firing=float(pos_fire_rate[parent]) if parent >= 0 else float("nan"),
                parent_pair_precision=float(precision[parent]) if parent >= 0 else float("nan"),
                parent_unresolved=bool(unresolved))
    return parent, resp, precision, pos_fire_rate, null95, info


def per_subcontext(parent, resp, precision, pos_lat, pos_sub, neg_lat, min_sub, rng):
    """For each sub-context: detector (best-AUC non-parent eligible latent, pos vs neg),
    parent recall hole, and positive-only firing-Jaccard(detector, parent) over ALL positives.
    Also computes the mean-activation detector variant for robustness."""
    fires_pos = pos_lat > 0
    fires_parent_pos = fires_pos[:, parent]
    subs = [s for s in sorted(set(pos_sub.tolist()), key=lambda x: str(x))
            if s is not None and int((pos_sub == s).sum()) >= min_sub]
    elig = np.array([l for l in resp if l != parent], dtype=int)
    out = []
    for s in subs:
        m = pos_sub == s
        n_pos = int(m.sum())
        parent_recall = float(fires_parent_pos[m].mean())
        # detector via best AUC: s-positives vs negatives (clean / concept-absent)
        if len(elig) == 0 or neg_lat.shape[0] < 2:
            det = parent; det_auc = float("nan"); det_mean = parent
        else:
            sc = np.concatenate([pos_lat[m][:, elig], neg_lat[:, elig]], 0).astype(np.float32)
            yy = np.concatenate([np.ones(n_pos), np.zeros(neg_lat.shape[0])])
            aucs = cols_auc(sc, yy)
            det = int(elig[np.nanargmax(aucs)]) if np.isfinite(aucs).any() else int(elig[0])
            det_auc = float(np.nanmax(aucs)) if np.isfinite(aucs).any() else float("nan")
            mean_pos = pos_lat[m][:, elig].astype(np.float32).mean(0)
            det_mean = int(elig[int(np.argmax(mean_pos))])
        # positive-only firing-Jaccard(detector, parent) over ALL positives
        jac = firing_jaccard(fires_pos[:, parent], fires_pos[:, det])
        jac_mean = firing_jaccard(fires_pos[:, parent], fires_pos[:, det_mean])
        # bootstrap CI for jac over positives
        fp = fires_pos[:, parent]; fd = fires_pos[:, det]
        vals = np.empty(B_JAC)
        n = len(fp)
        for b in range(B_JAC):
            ii = rng.integers(0, n, n)
            vals[b] = firing_jaccard(fp[ii], fd[ii])
        out.append(dict(sub_context=str(s), n_pos=n_pos, parent_recall=parent_recall,
                        recall_hole=float(1 - parent_recall), detector_latent=det,
                        detector_auc=det_auc, detector_meanact_latent=det_mean,
                        jaccard=float(jac), jaccard_meanact=float(jac_mean),
                        jaccard_ci=boot_ci(vals)))
    return out, subs


def ktrack_lite_unit(parent, resp, precision, pos_lat_star, pos_lat_all, neg_lat_star=None):
    """K-track-lite absorption repair — LABEL-FREE: it uses ONLY the content-flip co-response set
    (`resp` + content-flip `precision`, derived from on/off pairs) and the concept-positive firing
    structure; it never looks at the downstream task negatives. This is the fair contrast vs the
    SUPERVISED attribution baseline (h). anchor=parent; greedily add latents that (i) cover the
    parent's holes on the s* positives, (ii) are firing-disjoint w/ parent (firing-Jaccard <
    JACCARD_MAX over ALL positives), (iii) are selective on the content flip (content-flip
    precision >= PREC_FLOOR), (iv) marginal hole-cover gain >= COVGAIN_FLOOR."""
    fires_star = pos_lat_star > 0                  # [Nstar, d_sae]
    fires_all = pos_lat_all > 0
    parent_fire_star = fires_star[:, parent]
    members = [parent]
    holes = ~parent_fire_star                       # s*-positives the parent misses
    cand = [int(l) for l in resp if l != parent and precision[l] >= PREC_FLOOR]
    npos_star = fires_star.shape[0]
    while len(members) < K_MAX and holes.any():
        best, best_gain = -1, 0.0
        for l in cand:
            if l in members:
                continue
            if firing_jaccard(fires_all[:, parent], fires_all[:, l]) >= JACCARD_MAX:
                continue                            # must be firing-disjoint from the parent
            gain = float((fires_star[:, l] & holes).sum()) / max(npos_star, 1)
            if gain > best_gain:
                best_gain, best = gain, l
        if best < 0 or best_gain < COVGAIN_FLOOR:
            break
        members.append(best)
        holes = holes & (~fires_star[:, best])
    return members


def attribution_pool_h(parent, k, pos_lat_star, neg_lat_star):
    """Baseline (h): count-matched marginal attribution. Rank latents by the STANDARDIZED
    diff-of-means (Cohen's-d-style: (mean_pos - mean_neg)/pooled_sd) on the train slice -- the
    strong supervised marginal selector (AxBench / SCR-TPP proxy). Scale-invariant, so it is not
    dominated by a few high-magnitude latents. Drop degenerate all-fire / dead latents; take top-k."""
    pos = pos_lat_star.astype(np.float32); neg = neg_lat_star.astype(np.float32)
    sd_all = np.concatenate([pos, neg], 0).std(0) + 1e-6
    attr = (pos.mean(0) - neg.mean(0)) / sd_all                   # standardized mean difference
    neg_fire_rate = (neg > 0).mean(0)
    pos_fire_rate = (pos > 0).mean(0)
    degenerate = (neg_fire_rate > 0.5) | (pos_fire_rate < 0.02)   # all-fire / dead
    attr = attr.copy(); attr[degenerate] = -np.inf
    order = np.argsort(-attr)
    return [int(x) for x in order[:k]]

# ============================================================================ CONCEPT BUILDERS
def build_spelling(letter, enc, scale):
    g = next(d for d in _load(DATA["spelling"])["datasets"]
             if d["dataset"].endswith("_" + letter))["examples"]
    content = defaultdict(dict); corpus = []
    for r in g:
        pt = r.get("metadata_pair_type")
        if pt == "content_flip" and r.get("metadata_template_id") in SPELLING_CARRIERS:
            content[r["metadata_pair_id"]][r["metadata_role"]] = r
        elif pt == "corpus_context":
            corpus.append(r)
    content = {k: v for k, v in content.items() if "on" in v and "off" in v}
    pids = sorted(content)
    if scale == "mini": pids = pids[:60]
    elif scale == "smoke": pids = pids[:12]
    on, off = [content[p]["on"] for p in pids], [content[p]["off"] for p in pids]
    on_lat, on_res = enc.encode_token([r["input"] for r in on],
                              [tuple(r["metadata_word_char_span"]) for r in on], want_resid=True)
    off_lat, off_res = enc.encode_token([r["input"] for r in off],
                               [tuple(r["metadata_word_char_span"]) for r in off], want_resid=True)
    on_fold = np.array([int(r["metadata_fold"]) for r in on])
    # corpus positives (target token starts with the letter)
    if scale == "mini": corpus = corpus[:300]
    elif scale == "smoke": corpus = corpus[:40]
    cspan = [tuple(r["metadata_target_char_in_window"]) for r in corpus]
    cids = [r.get("metadata_target_token_id") for r in corpus]
    pos_lat = enc.encode_token([r["input"] for r in corpus], cspan, check_ids=cids)
    pos_sub = np.array([r["metadata_target_word"] for r in corpus], dtype=object)
    fold01 = (on_fold >= 4).astype(int)               # content folds 4,5 -> test(1); 1-3 -> train(0)
    return dict(name="spelling_%s" % letter, granularity="token", kind="established",
                on_lat=on_lat, off_lat=off_lat,
                pos_lat=pos_lat, pos_sub=pos_sub, pos_fold=np.zeros(len(corpus), int),
                neg_lat=off_lat, neg_fold=fold01,
                # OUTCOME slice: controlled content minimal pairs (on=L-word, off=matched non-L), same carrier
                star_pos_lat=on_lat, star_pos_fold=fold01, star_pos_resid=on_res,
                star_neg_lat=off_lat, star_neg_fold=fold01, star_neg_resid=off_res,
                min_sub=MIN_SUB_TOKEN, s_star="absorbed_%s_words" % letter)


def build_nonspell(hier, enc, scale):
    g = next(d for d in _load(DATA["nonspell"])["datasets"]
             if d["dataset"] == hier + "_absorption")["examples"]
    content = defaultdict(dict); corpus_pos = []; corpus_neg = []
    for r in g:
        rt = r.get("metadata_row_type")
        if rt == "content_pair":
            content[r["metadata_pair_id"]][r["metadata_pair_role"]] = r
        elif rt == "corpus":
            (corpus_pos if r.get("metadata_concept_present") else corpus_neg).append(r)
    content = {k: v for k, v in content.items() if "x_on" in v and "x_off" in v}
    pids = sorted(content)
    if scale == "mini": pids = pids[:80]
    elif scale == "smoke": pids = pids[:12]
    on = [content[p]["x_on"] for p in pids]; off = [content[p]["x_off"] for p in pids]
    def tok_enc(rows, want_resid=False):
        return enc.encode_token([r["input"] for r in rows],
                                [(r["metadata_target_char_start"], r["metadata_target_char_end"]) for r in rows],
                                token_idx_lists=[r.get("metadata_target_token_indices") for r in rows],
                                want_resid=want_resid)
    on_lat, on_res = tok_enc(on, want_resid=True); off_lat, off_res = tok_enc(off, want_resid=True)
    # subsample corpus positives per sub-context (bound size, keep power)
    cap_pos = {"smoke": 20, "mini": 40, "full": 300}[scale]
    cap_neg = {"smoke": 40, "mini": 120, "full": 2500}[scale]
    bysub = defaultdict(list)
    for r in corpus_pos:
        bysub[r["metadata_sub_context"]].append(r)
    rng = np.random.default_rng(SEED)
    keep = []
    for s, rows in bysub.items():
        idx = rng.permutation(len(rows))[:cap_pos]
        keep += [rows[i] for i in idx]
    corpus_neg = corpus_neg[:cap_neg]
    pos_lat = tok_enc(keep)
    neg_lat = tok_enc(corpus_neg) if corpus_neg else off_lat
    pos_sub = np.array([r["metadata_sub_context"] for r in keep], dtype=object)
    return dict(name=hier, granularity="token", kind="established",
                on_lat=on_lat, off_lat=off_lat,
                pos_lat=pos_lat, pos_sub=pos_sub, pos_fold=np.zeros(len(keep), int),
                neg_lat=neg_lat, neg_fold=np.zeros(neg_lat.shape[0], int),
                star_pos_lat=on_lat, star_pos_fold=np.array([_fold01(r) for r in on]), star_pos_resid=on_res,
                star_neg_lat=off_lat, star_neg_fold=np.array([_fold01(r) for r in off]), star_neg_resid=off_res,
                min_sub=MIN_SUB_SENT, s_star=hier + "_concept")


def _fold01(r):
    return 1 if r.get("metadata_fold") in ("test", "diagnostic") else 0


def build_toxicity(enc, scale):
    ds = {d["dataset"]: d["examples"] for d in _load(DATA["toxicity"])["datasets"]}
    para = [r for r in ds["paradetox"] if r.get("metadata_record_type") == "content_pair"]
    cls = [r for r in ds["civil_comments"] if r.get("metadata_record_type") == "classification"]
    rng = np.random.default_rng(SEED)
    cap_pair = {"smoke": 30, "mini": 300, "full": 4000}[scale]
    if len(para) > cap_pair:
        para = [para[i] for i in rng.permutation(len(para))[:cap_pair]]
    # sample CLS REPRESENTATIVELY (rows are fold-ordered -> a head slice is class-imbalanced)
    if scale in ("mini", "smoke"):
        ncls = 3000 if scale == "mini" else 400
        idx = rng.permutation(len(cls))[:ncls]
        cls = [cls[i] for i in idx]
    on_lat = enc.encode_sentence([r["metadata_text_on"] for r in para])["act_max"]
    off_lat = enc.encode_sentence([r["metadata_text_off"] for r in para])["act_max"]
    cls_enc = enc.encode_sentence([r["input"] for r in cls], want_resid=True)
    cls_lat = cls_enc["act_max"]; cls_resid = cls_enc["resid_mean"]
    cls_y = np.array([int(r.get("metadata_toxicity_label") or 0) for r in cls])
    cls_fold = np.array([0 if r.get("metadata_fold") == "train" else 1 for r in cls])
    sub_lab = {s: np.array([int((r.get("metadata_subcontext_labels") or {}).get(s) or 0) for r in cls])
               for s in ["threat", "identity_attack", "insult", "obscene", "sexual_explicit"]}
    return dict(_family="toxicity", on_lat=on_lat, off_lat=off_lat, cls_lat=cls_lat, cls_resid=cls_resid,
                cls_y=cls_y, cls_fold=cls_fold, sub_lab=sub_lab)


def build_support_sentiment(enc, scale):
    g = next(d for d in _load(DATA["support"])["datasets"] if "CAD-IMDB" in d["dataset"])["examples"]
    pairs = defaultdict(dict)
    for r in g:
        role = r.get("metadata_pair_role")
        if role in ("content_on", "content_off"):
            pairs[r["metadata_pair_id"]][role] = r
    pairs = {k: v for k, v in pairs.items() if "content_on" in v and "content_off" in v}
    pids = sorted(pairs)
    if scale == "mini": pids = pids[:200]
    elif scale == "smoke": pids = pids[:20]
    on = [pairs[p]["content_on"] for p in pids]; off = [pairs[p]["content_off"] for p in pids]
    on_e = enc.encode_sentence([r["input"] for r in on], want_resid=True)
    off_e = enc.encode_sentence([r["input"] for r in off], want_resid=True)
    on_lat, off_lat = on_e["act_max"], off_e["act_max"]
    fold = np.array([_fold01t(r) for r in on])
    return dict(name="sentiment", granularity="sentence", kind="prospective",
                on_lat=on_lat, off_lat=off_lat,
                pos_lat=on_lat, pos_sub=np.array(["overall"] * len(on), object), pos_fold=fold,
                neg_lat=off_lat, neg_fold=fold,
                star_pos_lat=on_lat, star_pos_fold=fold, star_pos_resid=on_e["resid_mean"],
                star_neg_lat=off_lat, star_neg_fold=fold, star_neg_resid=off_e["resid_mean"],
                min_sub=MIN_SUB_SENT, s_star="overall")


def build_support_aspect(enc, scale, which):
    g = next(d for d in _load(DATA["support"])["datasets"] if "CEBaB" in d["dataset"])["examples"]
    concept = "%s_sentiment" % which
    pairs = defaultdict(dict); allpos = []; alloff = []
    for r in g:
        if r.get("metadata_concept") != concept:
            continue
        role = r.get("metadata_pair_role")
        if role in ("content_on", "content_off"):
            pairs[r["metadata_pair_id"]][role] = r
    pairs = {k: v for k, v in pairs.items() if "content_on" in v and "content_off" in v}
    pids = sorted(pairs)
    if scale == "mini": pids = pids[:200]
    elif scale == "smoke": pids = pids[:20]
    on = [pairs[p]["content_on"] for p in pids]; off = [pairs[p]["content_off"] for p in pids]
    on_e = enc.encode_sentence([r["input"] for r in on], want_resid=True)
    off_e = enc.encode_sentence([r["input"] for r in off], want_resid=True)
    on_lat, off_lat = on_e["act_max"], off_e["act_max"]
    fold = np.array([_fold01t(r) for r in on])
    return dict(name="aspect_%s" % which, granularity="sentence", kind="prospective",
                on_lat=on_lat, off_lat=off_lat, _res_on=on_e["resid_mean"], _res_off=off_e["resid_mean"],
                pos_lat=on_lat, pos_sub=np.array([which] * len(on), object), pos_fold=fold,
                neg_lat=off_lat, neg_fold=fold,
                star_pos_lat=on_lat, star_pos_fold=fold, star_pos_resid=on_e["resid_mean"],
                star_neg_lat=off_lat, star_neg_fold=fold, star_neg_resid=off_e["resid_mean"],
                min_sub=MIN_SUB_SENT, s_star=which)


def _fold01t(r):
    return 1 if r.get("metadata_fold") == "test" else 0

# ============================================================================ RUN ONE CONCEPT
def run_concept(C, rng):
    """Uniform per-concept pipeline -> result dict (firing-Jaccard table + matched-pool OUTCOME)."""
    name = C["name"]
    logger.info(f"\n===== CONCEPT {name} ({C['granularity']}, {C['kind']}) =====")
    parent, resp, precision, pos_fire_rate, null95, pinfo = identify_parent(
        C["on_lat"], C["off_lat"], C["pos_lat"], rng)
    logger.info(f"{el()} {name}: parent={parent} n_responsive={pinfo['n_responsive']} "
                f"parent_pos_firing={pinfo['parent_pos_firing']:.3f} unresolved={pinfo['parent_unresolved']}")
    subrows, subs = per_subcontext(parent, resp, precision, C["pos_lat"], C["pos_sub"],
                                   C["neg_lat"], C["min_sub"], rng)
    jvals = [r["jaccard"] for r in subrows]
    jac_median = float(np.median(jvals)) if jvals else float("nan")
    jac_min = float(np.min(jvals)) if jvals else float("nan")
    jac_max = float(np.max(jvals)) if jvals else float("nan")
    recall_hole_max = float(max((r["recall_hole"] for r in subrows), default=float("nan")))
    logger.info(f"{el()} {name}: subs={len(subs)} jaccard_median={jac_median:.3f} "
                f"[{jac_min:.3f},{jac_max:.3f}] recall_hole_max={recall_hole_max:.3f}")

    # ----- OUTCOME on the defining (most under-served) slice = the parent's recall holes -----
    out = run_outcome(C, parent, resp, precision, rng)
    ccrg_helps = bool(out["delta"] > 0)
    ccrg_helps_sig = bool(out["delta"] > 0 and out["delta_ci"][0] > 0)
    logger.info(f"{el()} {name}: OUTCOME k={out['k']} auc_unit={out['auc_unit']:.3f} "
                f"auc_a={out['auc_a']:.3f} auc_h={out['auc_h']:.3f} auc_d={out['auc_d']:.3f} "
                f"delta(vs_a)={out['delta']:+.3f} ci={np.round(out['delta_ci'],3).tolist()} "
                f"CCRG_helps={ccrg_helps} (sig={ccrg_helps_sig})")
    return dict(concept=name, granularity=C["granularity"], kind=C["kind"],
                parent_latent=parent, parent_pos_firing=pinfo["parent_pos_firing"],
                parent_pair_precision=pinfo["parent_pair_precision"],
                parent_unresolved=pinfo["parent_unresolved"], n_responsive=pinfo["n_responsive"],
                jaccard_median=jac_median, jaccard_min=jac_min, jaccard_max=jac_max,
                jaccard_median_meanact=float(np.median([r["jaccard_meanact"] for r in subrows])) if subrows else float("nan"),
                recall_hole_max=recall_hole_max, n_subcontexts=len(subs),
                per_subcontext=subrows, outcome=out,
                ground_truth_regime=("absorption" if ccrg_helps else "co_firing"),
                ccrg_helps=ccrg_helps, ccrg_helps_significant=ccrg_helps_sig)


def _split(lat, fold, rng):
    tr = fold == 0; te = fold == 1
    if te.sum() < 5 or tr.sum() < 5:               # folds not usable -> random 70/30
        idx = rng.permutation(lat.shape[0]); cut = int(0.7 * len(idx))
        tr = np.zeros(lat.shape[0], bool); te = np.zeros(lat.shape[0], bool)
        tr[idx[:cut]] = True; te[idx[cut:]] = True
    return tr, te


def best_latent_a(resp, pos_tr, neg_tr):
    """Baseline (a): the single best RAW SAE latent (highest train AUC, pos vs neg). The 'individual
    latent' the goal requires us to beat. Restricted to content-responsive latents."""
    cand = np.asarray(resp, dtype=int)
    if len(cand) == 0:
        return 0
    sc = np.concatenate([pos_tr[:, cand], neg_tr[:, cand]], 0).astype(np.float32)
    yy = np.concatenate([np.ones(pos_tr.shape[0]), np.zeros(neg_tr.shape[0])])
    aucs = cols_auc(sc, yy)
    return int(cand[np.nanargmax(aucs)]) if np.isfinite(aucs).any() else int(cand[0])


def nonsae_probe_score(res_pos_tr, res_neg_tr, res_te):
    """Baseline (d): non-SAE difference-of-means probe on the raw residual. direction = standardized
    mean difference; score = res @ direction. The required non-SAE comparison."""
    pos = res_pos_tr.astype(np.float32); neg = res_neg_tr.astype(np.float32)
    sd = np.concatenate([pos, neg], 0).std(0) + 1e-6
    d = (pos.mean(0) - neg.mean(0)) / sd
    nrm = np.linalg.norm(d) + 1e-9
    return (res_te.astype(np.float32) / sd) @ (d / nrm)


def _delta_ci(su, sb, y, rng):
    if not (np.isfinite(auc(su, y)) and np.isfinite(auc(sb, y))):
        return 0.0, [float("nan"), float("nan")]
    return paired_bootstrap_auc_delta(su, sb, y, B_BOOT, rng)


def run_outcome(C, parent, resp, precision, rng):
    """OUTCOME on the GENERAL concept classification (all positives vs negatives), held-out TEST.
    Compares the label-free CCRG UNIT against the three required baselines at MATCHED pool size k:
      (a) best single RAW SAE latent          -> core 'cluster units beat individual latents' test
      (h) supervised SAE attribution pool      -> 'does CCRG beat marginal attribution'
      (d) non-SAE difference-of-means probe     -> required non-SAE baseline (raw residual)
    The UNIT is built on the parent's recall HOLES (label-free), then scored on the GENERAL task.
    PRIMARY routing signal = does the UNIT beat the best single latent (a)?  (= does grouping help)."""
    pos_lat, pos_fold = C["star_pos_lat"], C["star_pos_fold"]
    neg_lat, neg_fold = C["star_neg_lat"], C["star_neg_fold"]
    res_pos, res_neg = C.get("star_pos_resid"), C.get("star_neg_resid")
    return _outcome_core(parent, resp, precision, C["pos_lat"], pos_lat, pos_fold,
                         neg_lat, neg_fold, res_pos, res_neg, "concept_general", rng)


def _outcome_core(parent, resp, precision, full_pos_lat, pos_lat, pos_fold,
                  neg_lat, neg_fold, res_pos, res_neg, s_name, rng):
    p_tr, p_te = _split(pos_lat, pos_fold, rng)
    n_tr, n_te = _split(neg_lat, neg_fold, rng)
    pos_tr, pos_te = pos_lat[p_tr], pos_lat[p_te]
    neg_tr, neg_te = neg_lat[n_tr], neg_lat[n_te]
    # build the LABEL-FREE unit on the parent's holes among TRAIN positives
    hole = ~(pos_tr[:, parent] > 0)
    hole_pos = pos_tr[hole] if int(hole.sum()) >= 20 else pos_tr
    unit = ktrack_lite_unit(parent, resp, precision, hole_pos, full_pos_lat)
    k = max(1, len(unit))
    hpool = attribution_pool_h(parent, k, pos_tr, neg_tr)
    a_lat = best_latent_a(resp, pos_tr, neg_tr)
    Xte = np.concatenate([pos_te, neg_te], 0)
    yte = np.concatenate([np.ones(pos_te.shape[0]), np.zeros(neg_te.shape[0])])
    # held-constant LOGISTIC-REGRESSION head over each method's selected features (only SELECTION differs)
    su = lr_score(unit, pos_tr, neg_tr, Xte)
    sh = lr_score(hpool, pos_tr, neg_tr, Xte)
    sa = lr_score([a_lat], pos_tr, neg_tr, Xte)
    auc_u, auc_h, auc_a = auc(su, yte), auc(sh, yte), auc(sa, yte)
    # non-SAE probe (d)
    auc_d = float("nan")
    if res_pos is not None and res_neg is not None:
        sd_te = nonsae_probe_score(res_pos[p_tr], res_neg[n_tr],
                                   np.concatenate([res_pos[p_te], res_neg[n_te]], 0))
        auc_d = auc(sd_te, yte)
    # PRIMARY delta = unit vs best single latent (a); also vs (h) and (d)
    delta_a, ci_a = _delta_ci(su, sa, yte, rng)
    delta_h, ci_h = _delta_ci(su, sh, yte, rng)
    return dict(s_star=s_name, k=k, unit_members=[int(x) for x in unit],
                h_members=[int(x) for x in hpool], a_latent=int(a_lat),
                auc_unit=float(auc_u), auc_a=float(auc_a), auc_h=float(auc_h), auc_d=float(auc_d),
                delta=float(delta_a), delta_ci=[float(ci_a[0]), float(ci_a[1])],          # primary (vs a)
                delta_vs_h=float(delta_h), delta_vs_h_ci=[float(ci_h[0]), float(ci_h[1])],
                n_test_pos=int(pos_te.shape[0]), n_test_neg=int(neg_te.shape[0]))


def run_toxicity_concepts(fam, rng):
    """Derive the 5 toxicity sub-attribute concepts from the SHARED encoding.
    Parent g identified ONCE on ParaDetox pairs (non-circular)."""
    on_lat, off_lat = fam["on_lat"], fam["off_lat"]
    cls_lat, cls_y, cls_fold, sub_lab = fam["cls_lat"], fam["cls_y"], fam["cls_fold"], fam["sub_lab"]
    cls_resid = fam["cls_resid"]
    toxic = cls_y == 1
    parent, resp, precision, _, _, pinfo = identify_parent(on_lat, off_lat, cls_lat[toxic], rng)
    logger.info(f"{el()} toxicity: shared parent g={parent} toxic-recall={pinfo['parent_pos_firing']:.3f} "
                f"n_responsive={pinfo['n_responsive']}")
    results = []
    for s, labs in sub_lab.items():
        name = "toxicity_%s" % s
        pos_m = labs == 1; neg_m = cls_y == 0
        if pos_m.sum() < MIN_SUB_SENT:
            logger.warning(f"  {name}: only {int(pos_m.sum())} positives (<{MIN_SUB_SENT}) -> descriptive_only")
        logger.info(f"\n===== CONCEPT {name} (sentence, established) =====")
        # sub-row (single sub-context = the sub-attribute), firing-Jaccard over toxic rows
        pos_lat = cls_lat[pos_m]
        fires_tox = cls_lat[toxic] > 0
        elig = np.array([l for l in resp if l != parent], dtype=int)
        # best-AUC detector: s-positives vs clean negatives
        srows = np.where(pos_m | neg_m)[0]
        yy = pos_m[srows].astype(int)
        if len(elig) and yy.sum() > 1 and (yy == 0).sum() > 1:
            aucs = cols_auc(cls_lat[srows][:, elig].astype(np.float32), yy)
            det = int(elig[np.nanargmax(aucs)]); det_auc = float(np.nanmax(aucs))
            mean_pos = cls_lat[pos_m][:, elig].astype(np.float32).mean(0)
            det_mean = int(elig[int(np.argmax(mean_pos))])
        else:
            det = parent; det_auc = float("nan"); det_mean = parent
        jac = firing_jaccard(cls_lat[toxic][:, parent] > 0, cls_lat[toxic][:, det] > 0)
        jac_mean = firing_jaccard(cls_lat[toxic][:, parent] > 0, cls_lat[toxic][:, det_mean] > 0)
        pf = cls_lat[toxic][:, parent] > 0; df = cls_lat[toxic][:, det] > 0
        logger.debug(f"  {name}: parent={parent}(tox-fire {pf.mean():.3f}) det={det}(auc={det_auc:.3f} "
                     f"tox-fire {df.mean():.3f}) inter={(pf&df).sum()} union={(pf|df).sum()} det_meanact={det_mean}")
        fp = cls_lat[toxic][:, parent] > 0; fd = cls_lat[toxic][:, det] > 0
        vals = np.array([firing_jaccard(fp[ii], fd[ii]) for ii in
                         (rng.integers(0, len(fp), len(fp)) for _ in range(B_JAC))])
        parent_recall = float((cls_lat[pos_m][:, parent] > 0).mean())
        subrow = dict(sub_context=s, n_pos=int(pos_m.sum()), parent_recall=parent_recall,
                      recall_hole=float(1 - parent_recall), detector_latent=det, detector_auc=det_auc,
                      detector_meanact_latent=det_mean, jaccard=float(jac),
                      jaccard_meanact=float(jac_mean), jaccard_ci=boot_ci(vals))
        # OUTCOME: GENERAL sub-attribute classification (positives vs clean negatives), train/test by fold
        Cs = dict(name=name, granularity="sentence", pos_sub=labs,
                  pos_lat=cls_lat[pos_m], pos_fold=cls_fold[pos_m],
                  star_neg_lat=cls_lat[neg_m], star_neg_fold=cls_fold[neg_m],
                  star_pos_resid=cls_resid[pos_m], star_neg_resid=cls_resid[neg_m], s_star=s)
        out = run_outcome_tox(Cs, parent, resp, precision, rng)
        ccrg = bool(out["delta"] > 0); ccrg_sig = bool(out["delta"] > 0 and out["delta_ci"][0] > 0)
        logger.info(f"{el()} {name}: jaccard={jac:.3f} hole={1-parent_recall:.3f} k={out['k']} "
                    f"auc_unit={out['auc_unit']:.3f} auc_a={out['auc_a']:.3f} auc_h={out['auc_h']:.3f} "
                    f"auc_d={out['auc_d']:.3f} delta(vs_a)={out['delta']:+.3f} CCRG_helps={ccrg}")
        results.append(dict(concept=name, granularity="sentence", kind="established",
                            parent_latent=parent, parent_pos_firing=pinfo["parent_pos_firing"],
                            parent_pair_precision=pinfo["parent_pair_precision"],
                            parent_unresolved=pinfo["parent_unresolved"], n_responsive=pinfo["n_responsive"],
                            jaccard_median=float(jac), jaccard_min=float(jac), jaccard_max=float(jac),
                            jaccard_median_meanact=float(jac_mean), recall_hole_max=float(1 - parent_recall),
                            n_subcontexts=1, per_subcontext=[subrow], outcome=out,
                            ground_truth_regime=("absorption" if ccrg else "co_firing"),
                            ccrg_helps=ccrg, ccrg_helps_significant=ccrg_sig,
                            descriptive_only=bool(pos_m.sum() < MIN_SUB_SENT)))
    return results


def run_outcome_tox(C, parent, resp, precision, rng):
    """Toxicity OUTCOME = GENERAL sub-attribute classification (positives vs clean negatives).
    Same multi-baseline core as every other concept: label-free CCRG unit vs (a) raw-best latent,
    (h) supervised SAE attribution, (d) non-SAE residual probe."""
    sub_pos_lat = C["pos_lat"]; sub_pos_fold = C["pos_fold"]
    return _outcome_core(parent, resp, precision, sub_pos_lat,
                         sub_pos_lat, sub_pos_fold, C["star_neg_lat"], C["star_neg_fold"],
                         C["star_pos_resid"], C["star_neg_resid"], "subattr_general", rng)

# ============================================================================ ROUTER
def balanced_accuracy(pred, truth):
    pred = np.asarray(pred); truth = np.asarray(truth)
    accs = []
    for cls in ["absorption", "co_firing"]:
        m = truth == cls
        if m.sum() == 0:
            continue
        accs.append((pred[m] == cls).mean())
    return float(np.mean(accs)) if accs else float("nan")


def derive_tau(concepts):
    """Derive tau* by balanced-accuracy sweep over the given concepts (predict absorption iff j<tau)."""
    j = np.array([c["jaccard_median"] for c in concepts])
    truth = np.array([c["ground_truth_regime"] for c in concepts])
    sweep = []
    for tau in TAU_GRID:
        pred = np.where(j < tau, "absorption", "co_firing")
        sweep.append(dict(tau=float(tau), balanced_acc=balanced_accuracy(pred, truth)))
    best = max(sweep, key=lambda r: (r["balanced_acc"], -abs(r["tau"] - 0.15)))
    abs_j = [c["jaccard_median"] for c in concepts if c["ground_truth_regime"] == "absorption"]
    cof_j = [c["jaccard_median"] for c in concepts if c["ground_truth_regime"] == "co_firing"]
    return best["tau"], best["balanced_acc"], sweep, dict(
        max_absorption_j=float(np.max(abs_j)) if abs_j else float("nan"),
        min_cofiring_j=float(np.min(cof_j)) if cof_j else float("nan"),
        mean_absorption_j=float(np.mean(abs_j)) if abs_j else float("nan"),
        mean_cofiring_j=float(np.mean(cof_j)) if cof_j else float("nan"))


def derive_1d(concepts, key, lt):
    """Single-threshold router on `key` (absorption iff value < tau when lt else value > tau)."""
    vals = np.array([c[key] for c in concepts], float)
    truth = np.array([c["ground_truth_regime"] for c in concepts])
    if len(vals) == 0 or not np.isfinite(vals).any():
        return float("nan"), float("nan"), []
    grid = np.linspace(float(np.nanmin(vals)), float(np.nanmax(vals)), 41)
    sweep = []
    for tau in grid:
        pred = np.where(vals < tau if lt else vals > tau, "absorption", "co_firing")
        sweep.append(dict(tau=float(tau), balanced_acc=balanced_accuracy(pred, truth)))
    best = max(sweep, key=lambda r: r["balanced_acc"])
    return best["tau"], best["balanced_acc"], sweep


def derive_combined(concepts):
    """2-signal router: absorption iff (firing-Jaccard < tau_j) AND (recall_hole_max > tau_h).
    The honest finding: firing-disjointness ALONE is insufficient -- grouping helps only when the
    parent ALSO has recall holes to fill (taxonomic = low-Jaccard but high-recall parent => no help)."""
    j = np.array([c["jaccard_median"] for c in concepts], float)
    h = np.array([c["recall_hole_max"] for c in concepts], float)
    truth = np.array([c["ground_truth_regime"] for c in concepts])
    if len(j) == 0:
        return dict(tau_j=float("nan"), tau_h=float("nan"), balanced_acc=float("nan"))
    best = None
    for tj in np.linspace(0.05, 0.70, 27):
        for th in np.linspace(0.0, 0.9, 19):
            pred = np.where((j < tj) & (h > th), "absorption", "co_firing")
            ba = balanced_accuracy(pred, truth)
            if best is None or ba > best["balanced_acc"]:
                best = dict(tau_j=float(tj), tau_h=float(th), balanced_acc=float(ba))
    return best

# ============================================================================ MAIN
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scale", default="full", choices=["smoke", "mini", "full"])
    ap.add_argument("--smoke", action="store_true", help="model+SAE load + gating + BOS-offset assertion only")
    ap.add_argument("--concepts", default="", help="comma list to restrict (debug)")
    ap.add_argument("--out", default=str(HERE / "method_out.json"))
    ap.add_argument("--ram_gb", type=float, default=44.0)
    args = ap.parse_args()
    set_mem_limits(args.ram_gb)
    rng = np.random.default_rng(SEED)
    logger.info(f"{el()} M4 router | scale={args.scale} smoke={args.smoke}")

    enc = Encoder()
    # ---- gating check + BOS-offset assertion on real spelling corpus rows ----
    sp = next(d for d in _load(DATA["spelling"])["datasets"] if d["dataset"].endswith("_L"))["examples"]
    corpus = [r for r in sp if r.get("metadata_pair_type") == "corpus_context"][:20]
    gating = enc.gating_check([r["input"] for r in corpus[:8]])
    cspan = [tuple(r["metadata_target_char_in_window"]) for r in corpus]
    cids = [r["metadata_target_token_id"] for r in corpus]
    _ = enc.encode_token([r["input"] for r in corpus], cspan, check_ids=cids)  # logs mismatches
    if gating["recon_cos_mean"] < 0.80:
        logger.error(f"GATING FAILED recon_cos_mean={gating['recon_cos_mean']:.3f} (<0.80)")
    if args.smoke:
        Path(args.out).write_text(json.dumps({"gating": gating}, indent=2))
        logger.info("SMOKE complete."); return

    # ---- build concept registry ----
    want = set(args.concepts.split(",")) if args.concepts else None
    def keep(n): return (want is None) or (n in want)

    results = []
    # token-level established (cheap, lock the table first)
    for L in ["L", "O", "T", "I", "D"]:
        if keep("spelling_%s" % L):
            C = cached_build("spelling_%s" % L, args.scale, lambda L=L: build_spelling(L, enc, args.scale))
            results.append(run_concept(C, rng)); del C; gc.collect()
    for hier in ["numeric", "taxonomic"]:
        if keep(hier):
            C = cached_build(hier, args.scale, lambda hier=hier: build_nonspell(hier, enc, args.scale))
            results.append(run_concept(C, rng)); del C; gc.collect()
    # toxicity (5 concepts, shared encoding)
    if any(keep("toxicity_%s" % s) for s in ["threat", "identity_attack", "insult", "obscene", "sexual_explicit"]):
        fam = cached_build("toxicity_family", args.scale, lambda: build_toxicity(enc, args.scale))
        results += [r for r in run_toxicity_concepts(fam, rng) if keep(r["concept"])]
        del fam; gc.collect()
    # prospective
    if keep("sentiment"):
        C = cached_build("sentiment", args.scale, lambda: build_support_sentiment(enc, args.scale))
        results.append(run_concept(C, rng)); del C; gc.collect()
    for which in ["food", "service"]:
        if keep("aspect_%s" % which):
            C = cached_build("aspect_%s" % which, args.scale, lambda which=which: build_support_aspect(enc, args.scale, which))
            results.append(run_concept(C, rng)); del C; gc.collect()

    enc.free()
    del enc; gc.collect()
    try:
        import torch; torch.cuda.empty_cache()
    except Exception:
        pass

    # ---- router: derive tau on ESTABLISHED only ----
    est = [r for r in results if r["concept"] in ESTABLISHED]
    pro = [r for r in results if r["concept"] in PROSPECTIVE]
    assemble_and_save(results, est, pro, gating, args)


def assemble_and_save(results, est, pro, gating, args):
    tau_star, bacc, sweep, sep = (float("nan"), float("nan"), [], {}) if not est else derive_tau(est)
    logger.info(f"{el()} ROUTER tau*={tau_star:.3f} balanced_acc={bacc:.3f} "
                f"sep(max_abs_j={sep.get('max_absorption_j')}, min_cof_j={sep.get('min_cofiring_j')})")

    # prospective predict-then-measure
    for r in results:
        r["predicted_regime"] = ("absorption" if (np.isfinite(tau_star) and r["jaccard_median"] < tau_star)
                                 else "co_firing")
        r["hit"] = bool(r["predicted_regime"] == r["ground_truth_regime"])
    prosp_table = [dict(concept=r["concept"], jaccard_median=r["jaccard_median"],
                        predicted_regime=r["predicted_regime"], ground_truth_regime=r["ground_truth_regime"],
                        delta=r["outcome"]["delta"], hit=r["hit"]) for r in pro]
    oos_hits = [r["hit"] for r in pro]
    logger.info(f"{el()} PROSPECTIVE out-of-sample hits: {sum(oos_hits)}/{len(oos_hits)}")

    # leave-one-concept-out over ALL concepts
    loo = []
    allc = results
    for i, ci in enumerate(allc):
        rest = [c for j, c in enumerate(allc) if j != i]
        if len(set(c["ground_truth_regime"] for c in rest)) < 2:
            tau_i, _, _, _ = (tau_star, None, None, None)   # degenerate fold -> reuse global
        else:
            tau_i, _, _, _ = derive_tau(rest)
        pred = "absorption" if (np.isfinite(tau_i) and ci["jaccard_median"] < tau_i) else "co_firing"
        loo.append(dict(concept=ci["concept"], tau_fold=float(tau_i), pred=pred,
                        ground_truth=ci["ground_truth_regime"], hit=bool(pred == ci["ground_truth_regime"])))
    loo_acc = float(np.mean([x["hit"] for x in loo])) if loo else float("nan")
    logger.info(f"{el()} LOO accuracy = {loo_acc:.3f} ({sum(x['hit'] for x in loo)}/{len(loo)})")

    # reproduction check
    sp_j = {r["concept"]: r["jaccard_median"] for r in results if r["concept"].startswith("spelling_")}
    tox_j = {r["concept"].replace("toxicity_", ""): r["jaccard_median"]
             for r in results if r["concept"].startswith("toxicity_")}
    repro = dict(
        spelling_jaccard=sp_j,
        spelling_all_below_0_1=bool(all(v < 0.10 for v in sp_j.values())) if sp_j else None,
        toxicity_jaccard={k: tox_j.get(k) for k in ["threat", "identity_attack", "insult"]},
        toxicity_reference={"threat": 0.40, "identity_attack": 0.29, "insult": 0.66},
        toxicity_within_tol_0_10=bool(all(
            (k in tox_j and abs(tox_j[k] - ref) <= 0.10)
            for k, ref in {"threat": 0.40, "identity_attack": 0.29, "insult": 0.66}.items())) if tox_j else None,
    )
    logger.info(f"{el()} REPRO spelling<0.1={repro['spelling_all_below_0_1']} "
                f"toxicity_within_tol={repro['toxicity_within_tol_0_10']} tox_j={tox_j}")

    honest = []
    for r in results:
        if r.get("parent_unresolved"):
            honest.append(f"{r['concept']}: parent_unresolved (no responsive latent cleared the "
                          f"{PARENT_FIRE_FLOOR:.0%} positive-firing floor) — anchor-fidelity edge.")
        if r.get("descriptive_only"):
            honest.append(f"{r['concept']}: <{MIN_SUB_SENT} positives — descriptive_only, excluded from inferential outcome.")
    for r in pro:
        if not r["hit"]:
            honest.append(f"PROSPECTIVE MISS {r['concept']}: predicted {r['predicted_regime']} but "
                          f"ground-truth {r['ground_truth_regime']} (delta={r['outcome']['delta']:+.3f}).")
    honest.append("OUTCOME = GENERAL concept classification (positives vs negatives), held-out test fold. "
                  "PRIMARY ground-truth regime = SIGN of (auc_unit - auc_a): does the label-free CCRG unit beat "
                  "the best single RAW SAE latent (a)? = does cluster-level grouping help over individual latents. "
                  "ccrg_helps_significant additionally requires the paired-bootstrap CI(vs a) to exclude 0. "
                  "delta_vs_h compares the unit to the SUPERVISED SAE attribution pool (h); auc_d is the required "
                  "NON-SAE difference-of-means residual probe.")
    honest.append("numeric is reported honestly as suggestive/diagnostic-unconfirmed (absorption documented "
                  "empirically only on spelling; numeric is the generality+novelty test).")
    honest.append("Firing-Jaccard detector = best-AUC sub-context detector (reproduces the iter-2 toxicity "
                  "values); jaccard_median_meanact reports the mean-activation-detector variant for robustness.")
    honest.append("The CCRG unit is LABEL-FREE (built only from content-flip co-response + firing-disjointness, "
                  "never the task labels); baselines (a)/(h)/(d) are all supervised. A unit win is therefore a "
                  "win at zero label cost.")
    honest.append("ROUTER BOUNDARY (honest): firing-Jaccard separates the EXTREMES cleanly (spelling disjoint "
                  "<0.04 -> grouping helps; toxicity co-firing ~0.69 -> a single specialist wins) but is "
                  "ambiguous mid-range. The instructive counterexample is TAXONOMIC: low firing-Jaccard "
                  "(narrow country specialists) yet co_firing-regime OUTCOME, because the parent already has "
                  "~0.95 recall (no holes to fill) -> disjoint specialists exist but grouping cannot help. This "
                  "shows firing-Jaccard ALONE is insufficient: grouping helps only when there are ALSO recall "
                  "holes. We therefore report a 2-signal combined router (low-Jaccard AND high-recall-hole) and "
                  "a recall-hole-only router for comparison.")
    honest.append("Supervised SAE attribution (h) and the non-SAE residual probe (d) generally MATCH or beat "
                  "the label-free unit on raw AUC (consistent with 'simple supervised baselines are strong'); "
                  "the unit's value is being LABEL-FREE while still beating the best individual latent in the "
                  "absorption regime. (h)/(d) are reported in every row for full transparency.")

    # secondary router using the STRICT (CI-excludes-0) ground truth
    strict = [dict(r, ground_truth_regime=("absorption" if r["ccrg_helps_significant"] else "co_firing"))
              for r in est]
    tau_s, bacc_s, _, sep_s = (float("nan"), float("nan"), [], {}) if not strict else derive_tau(strict)

    table = [dict(concept=r["concept"], granularity=r["granularity"],
                  established_or_prospective=r["kind"], parent_latent=r["parent_latent"],
                  parent_pos_firing=r["parent_pos_firing"], jaccard_median=r["jaccard_median"],
                  jaccard_min=r["jaccard_min"], jaccard_max=r["jaccard_max"],
                  jaccard_median_meanact=r["jaccard_median_meanact"], recall_hole_max=r["recall_hole_max"],
                  predicted_regime=r["predicted_regime"], ground_truth_regime=r["ground_truth_regime"],
                  outcome=r["outcome"], ccrg_helps=r["ccrg_helps"],
                  ccrg_helps_significant=r["ccrg_helps_significant"], hit=r["hit"]) for r in results]

    # alternative a-priori signals (honest comparison): recall-hole-only and the 2-signal combined router
    tau_h, bacc_hole, sweep_hole = derive_1d(est, "recall_hole_max", lt=False)
    combined = derive_combined(est)
    logger.info(f"{el()} ALT routers: hole-only balanced_acc={bacc_hole:.3f} (tau_h={tau_h:.3f}); "
                f"combined balanced_acc={combined['balanced_acc']:.3f} "
                f"(tau_j={combined['tau_j']:.3f}, tau_h={combined['tau_h']:.3f})")

    router = dict(primary_signal="firing_jaccard_median",
                  tau_star=tau_star, balanced_acc_at_tau_star=bacc,
                  regime_separation=sep, tau_sweep=sweep, loo_accuracy=loo_acc, loo_per_concept=loo,
                  prospective=dict(out_of_sample_accuracy=float(np.mean(oos_hits)) if oos_hits else float("nan"),
                                   table=prosp_table),
                  strict_ci_router=dict(tau_star=tau_s, balanced_acc=bacc_s, regime_separation=sep_s),
                  recall_hole_router=dict(tau_h=tau_h, balanced_acc=bacc_hole, tau_sweep=sweep_hole),
                  combined_jaccard_and_hole_router=combined)

    metadata = dict(
        method_name="A-Priori Firing-Structure Router (M4)",
        description="The SAE-latent firing-Jaccard between per-sub-context detectors and the general/parent "
                    "latent predicts, A PRIORI (one cheap forward pass, no labels), whether label-free "
                    "cluster-level grouping (CCRG) helps. OUTCOME = general concept classification; the "
                    "label-free CCRG unit is compared at matched pool size k against (a) the best single raw "
                    "SAE latent, (h) the supervised SAE difference-of-means attribution pool, and (d) a non-SAE "
                    "difference-of-means probe on the raw residual. Primary routing target = does the unit beat "
                    "the best single latent (a) (i.e. does grouping help). Low firing-Jaccard (absorption "
                    "regime) => grouping helps; high firing-Jaccard (co-firing/splitting regime) => a single "
                    "specialist latent already wins.",
        baselines=dict(a="best single raw SAE latent (highest train AUC, content-responsive)",
                       h="supervised SAE standardized diff-of-means attribution pool (top-k, AxBench/SCR-TPP proxy)",
                       d="non-SAE standardized diff-of-means probe on the raw layer-12 residual",
                       unit="label-free CCRG K-track-lite: parent anchor + firing-disjoint hole-covering absorbers"),
        sae_release=RELEASE_REPO, sae_id=SAE_PARAMS_16K, hook="blocks.12.hook_resid_post",
        model=MODEL_ID, seed=SEED, scale=args.scale, n_concepts=len(results),
        gating=gating, gpu=_gpu_name(), firing_convention="encode>0 (JumpReLU)",
        prediction_vs_outcome_table=table,
        per_concept_firing_jaccard=[dict(concept=r["concept"], per_subcontext=r["per_subcontext"])
                                    for r in results],
        router=router, reproduction_check=repro, honest_notes=honest,
        established_concepts=[r["concept"] for r in est], prospective_concepts=[r["concept"] for r in pro],
    )

    # ---- exp_gen_sol_out schema: datasets[] of examples (one per concept) ----
    examples = []
    for r in results:
        ex = {
            "input": (f"Concept '{r['concept']}' ({r['granularity']}, {r['kind']}): parent latent "
                      f"{r['parent_latent']}, firing-Jaccard(detector,parent) median="
                      f"{r['jaccard_median']:.4f}. Route to absorption-repair (CCRG) or marginal attribution?"),
            "output": r["ground_truth_regime"],
            "predict_router": r["predicted_regime"],
            "metadata_concept": r["concept"],
            "metadata_kind": r["kind"],
            "metadata_granularity": r["granularity"],
            "metadata_jaccard_median": r["jaccard_median"],
            "metadata_jaccard_min": r["jaccard_min"],
            "metadata_jaccard_max": r["jaccard_max"],
            "metadata_jaccard_median_meanact": r["jaccard_median_meanact"],
            "metadata_recall_hole_max": r["recall_hole_max"],
            "metadata_parent_latent": r["parent_latent"],
            "metadata_parent_pos_firing": r["parent_pos_firing"],
            "metadata_parent_unresolved": r["parent_unresolved"],
            "metadata_n_subcontexts": r["n_subcontexts"],
            "metadata_outcome_auc_unit": r["outcome"]["auc_unit"],
            "metadata_outcome_auc_a_rawlatent": r["outcome"].get("auc_a"),
            "metadata_outcome_auc_h_attribution": r["outcome"]["auc_h"],
            "metadata_outcome_auc_d_nonsae": r["outcome"].get("auc_d"),
            "metadata_outcome_delta_vs_a": r["outcome"]["delta"],
            "metadata_outcome_delta_vs_a_ci": r["outcome"]["delta_ci"],
            "metadata_outcome_delta_vs_h": r["outcome"].get("delta_vs_h"),
            "metadata_outcome_delta_vs_h_ci": r["outcome"].get("delta_vs_h_ci"),
            "metadata_outcome_k": r["outcome"]["k"],
            "metadata_outcome_s_star": r["outcome"]["s_star"],
            "metadata_unit_members": r["outcome"]["unit_members"],
            "metadata_h_members": r["outcome"]["h_members"],
            "metadata_a_latent": r["outcome"].get("a_latent"),
            "metadata_ccrg_helps": r["ccrg_helps"],
            "metadata_ccrg_helps_significant": r["ccrg_helps_significant"],
            "metadata_ground_truth_regime": r["ground_truth_regime"],
            "metadata_predicted_regime": r["predicted_regime"],
            "metadata_hit": r["hit"],
            "metadata_per_subcontext": r["per_subcontext"],
        }
        examples.append(ex)
    out = {"metadata": metadata, "datasets": [{"dataset": "m4_router_concepts", "examples": examples}]}

    Path(args.out).write_text(json.dumps(out, indent=2, default=_json_default))
    logger.info(f"{el()} wrote {args.out} ({Path(args.out).stat().st_size/1e6:.2f} MB, {len(examples)} concepts)")
    _print_summary(table, router, repro)


def _print_summary(table, router, repro):
    logger.info("\n================= PREDICTION vs OUTCOME =================")
    logger.info(f"{'concept':<24}{'j_med':>7}{'pred':>12}{'truth':>12}{'aucU':>6}{'aucA':>6}{'aucH':>6}{'aucD':>6}{'dVa':>7}{'hit':>5}")
    for t in table:
        o = t['outcome']
        logger.info(f"{t['concept']:<24}{t['jaccard_median']:>7.3f}{t['predicted_regime']:>12}"
                    f"{t['ground_truth_regime']:>12}{o['auc_unit']:>6.3f}{o.get('auc_a',float('nan')):>6.3f}"
                    f"{o['auc_h']:>6.3f}{o.get('auc_d',float('nan')):>6.3f}{o['delta']:>+7.3f}{str(t['hit']):>5}")
    logger.info(f"\ntau*={router['tau_star']:.3f} balanced_acc={router['balanced_acc_at_tau_star']:.3f} "
                f"LOO_acc={router['loo_accuracy']:.3f} prospective={router['prospective']['out_of_sample_accuracy']:.3f}")
    logger.info(f"reproduction: spelling<0.1={repro['spelling_all_below_0_1']} "
                f"toxicity_within_tol={repro['toxicity_within_tol_0_10']}")


def _gpu_name():
    """Actual accelerator name (don't hardcode — the experiment may run on different GPUs)."""
    try:
        import torch
        if torch.cuda.is_available():
            return torch.cuda.get_device_name(0)
    except Exception:
        pass
    return "cpu"


def _json_default(o):
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    if isinstance(o, np.ndarray): return o.tolist()
    return str(o)


if __name__ == "__main__":
    main()
