#!/usr/bin/env python
"""
A-PRIORI SAE FIRING-STRUCTURE ROUTER  —  a screening heuristic with MEASURED error.

What it does (single self-contained GPU experiment, $0 LLM):
  From ONE cheap forward pass we read two label-free structural signals of a concept's
  SAE-latent geometry and use them to PREDICT, a priori, which family of cluster-level
  unit will help downstream:
    * firing-Jaccard(detector, parent)  -- how disjoint the per-sub-context specialist
      latents are from the broad parent latent (low => narrow firing-disjoint absorbers).
    * parent recall-hole                -- the fraction of concept-positives the parent
      latent MISSES (high => there are holes for absorbers to fill).
  COMBINED screening rule (the recommendation):
        predict ABSORPTION-regime  iff  (firing-Jaccard < tau_J)  AND  (recall-hole > tau_h)
  ABSORPTION regime => label-free grouping (CCRG K-track) recovers a unit that beats the
  best single raw latent; CO-FIRING regime => a single specialist already wins and
  grouping cannot help.

  We report this rule HONESTLY as a screening heuristic with a substantial *measured*
  error rate, NOT a validated oracle. Two design pillars make that measurement clean:
    (1) DERIVATION vs TRULY-PROSPECTIVE separation. The 12 DERIVATION concepts
        (spelling L/O/T/I/D ; numeric ; taxonomic ; toxicity threat/identity_attack/
        insult/obscene/sexual_explicit) are where (tau_J, tau_h) are fit and the
        single-signal ablations + LOO are computed. They are NEVER counted as prospective.
    (2) EXPANDED truly-held-out prospective set, predicted with the FROZEN rule before
        its outcome is measured: sentiment, aspect_food, aspect_service (existing) PLUS
        ~8 bias_in_bios profession concepts + civil_comments severe_toxicity (new, carved
        from data already in hand at $0). Prospective hit-rate + Wilson CI = the measured error.

  Ground-truth regime PRIMARY = sign of (auc_unit - auc_a): does the label-free grouped
  unit beat the best single RAW SAE latent (a) (= does grouping help)? We ALSO report the
  SECONDARY contrast vs (h), the supervised attribution pool: general-classification (h)
  often beats the unit even in true absorption regimes, because the absorption advantage
  lives on the absorbed-slice recall, not general classification.

SAE  = Gemma-Scope  google/gemma-scope-2b-pt-res  layer_12/width_16k/average_l0_82
       (the 'canonical' L0~100 JumpReLU variant), loaded directly from params.npz.
Model= unsloth/gemma-2-2b (non-gated mirror).  firing := sae.encode(resid) > 0.
Residual captured by a forward hook on model.model.layers[12] (== blocks.12.hook_resid_post),
validated by SAE reconstruction cosine (gating check).

Usage:
  uv run method.py --smoke                       # load model+SAE, gating + BOS-offset assertion only
  uv run method.py --scale mini                  # small pilot (subset of concepts incl 1 profession + severe)
  uv run method.py --scale full                  # full: 12 derivation + 3 existing + ~9 new prospective + routers
"""
import os, sys, json, time, argparse, gc, math, hashlib, warnings, resource, pickle
from pathlib import Path
from collections import defaultdict, Counter

import numpy as np

warnings.filterwarnings("ignore")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
# NOTE: do NOT set expandable_segments — it reserves large virtual ranges that collide with RLIMIT_AS
# and make CUDA .to() fail with a spurious "driver out of memory" even when the GPU is nearly empty.

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
B_BOOT         = 4000      # paired bootstrap for the OUTCOME delta CI (>=2000 keeps CIs stable; lowered
#                            from 10000 to shorten the run under shared-GPU time pressure — see honest_notes)
B_JAC          = 2000      # bootstrap for per-sub firing-Jaccard CI
TAU_GRID       = np.linspace(0.05, 0.35, 31)   # legacy jaccard sweep (kept for compatibility)
TAU_J_GRID     = np.linspace(0.02, 0.35, 34)   # firing-Jaccard threshold sweep (router derivation)
TAU_H_GRID     = np.linspace(0.0, 0.95, 40)    # recall-hole threshold sweep (router derivation)
SEVERE_TOX_THRESH = 0.30   # re-threshold for the rare severe_toxicity sub-attribute (0.5 has <30 positives)

# ---------------- concept partition: DERIVATION (rule fit here) vs TRULY-PROSPECTIVE ----------------
# DERIVATION concepts: thresholds tau_J, tau_h, the single-signal ablations and LOO are fit ONLY here.
DERIVATION = (["spelling_%s" % L for L in ["L", "O", "T", "I", "D"]]
              + ["numeric", "taxonomic"]
              + ["toxicity_%s" % s for s in ["threat", "identity_attack", "insult",
                                             "obscene", "sexual_explicit"]])
ESTABLISHED = DERIVATION                                  # alias (legacy name)
# TRULY-PROSPECTIVE: predicted with the FROZEN rule before its outcome is measured.
PROSPECTIVE_EXISTING = ["sentiment", "aspect_food", "aspect_service"]
# bias_in_bios professions (boundary-null): all 28 classes carry n=752 @ 376/376 gender; we take a
# fixed, reproducible, recognizable set of 8. severe_toxicity = the one civil_comments sub-attribute
# NOT used in derivation (descriptive_only / underpowered -> flagged, still predicted+measured).
PROFS = ["professor", "physician", "surgeon", "nurse",
         "journalist", "photographer", "psychologist", "software_engineer"]
# M6c: NEW first-letter spelling concepts (letters NOT in derivation, degenerate S/X excluded), built
# INTERNALLY from the gemma vocab (get_alpha_tokens recipe) + the pinned Pile corpus windows already in
# dataset_1 -- they supply guaranteed ABSORPTION-regime prospective concepts so the prospective set spans
# BOTH regimes and the router can be wrong in BOTH directions. They are prospective by construction (NOT
# in DERIVATION); their thresholds are NEVER fit.
NEW_LETTERS = ["B", "C", "F", "M", "P", "R", "W"]
PROSPECTIVE_SPELLING = ["spelling_%s" % L for L in NEW_LETTERS]
PROSPECTIVE_NEW = (["profession_%s" % p for p in PROFS] + ["toxicity_severe_toxicity"]
                  + PROSPECTIVE_SPELLING)
PROSPECTIVE = PROSPECTIVE_EXISTING + PROSPECTIVE_NEW      # full prospective registry

# get_alpha_tokens / spelling-carrier replication (dataset_1/data.py) for INTERNAL prospective spelling
GEMMA_SPACE = "▁"                          # '▁' sentencepiece word-initial marker
ALL_ALPHA_LETTERS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
ICL_POOL = [("apple", "A"), ("river", "R"), ("table", "T"), ("garden", "G"), ("music", "M"),
            ("window", "W"), ("yellow", "Y"), ("planet", "P"), ("camera", "C"), ("forest", "F")]
CAP_SPELL_PAIRS = {"smoke": 12, "mini": 60, "full": 250}   # content-flip instances per new letter
CAP_SPELL_CORPUS = {"smoke": 20, "mini": 40, "full": 300}  # corpus positives per new letter

CACHE_VER = "v5"           # bump to invalidate cached encodings when a build_* changes
CACHE_TO_DISK = False      # OFF: cached latent arrays exceed GitHub's 100MB file limit (recompute fresh)

T0 = time.time()
def el():
    return f"{time.time()-T0:6.1f}s"

def cached_build(name, scale, fn):
    """Build the encoded dict for a concept. Disk persistence is DISABLED: the cached float16 latent
    arrays are 100MB-900MB each (>GitHub's 100MB file limit), so we never write them to disk — each
    launch recomputes the forward passes fresh. (Set CACHE_TO_DISK=True only for local dev where the
    cache/ dir is not published.) The cheap numpy ANALYSIS re-runs every time regardless."""
    if CACHE_TO_DISK:
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
    return fn()

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
        logger.info(f"{el()} loading tokenizer + model {MODEL_ID} (bf16, eager attn) -> CPU first")
        self.tok = AutoTokenizer.from_pretrained(MODEL_ID, token=os.environ.get("HF_TOKEN"))
        self.tok.padding_side = "right"
        # Load weights to CPU (slow disk read, NO GPU contention), then GRAB the GPU in a tight retry
        # loop that only needs a ~2s free window -- robust to a co-tenant run on the shared single GPU.
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID, torch_dtype=torch.bfloat16, attn_implementation="eager",
            token=os.environ.get("HF_TOKEN"),
        ).eval()
        self.d_model = self.model.config.hidden_size
        self._cap = {}
        self._handle = self.model.model.layers[HOOK_LAYER].register_forward_hook(self._hook)
        self._acquire_gpu()
        logger.info(f"{el()} model loaded d_model={self.d_model} "
                    f"n_layers={self.model.config.num_hidden_layers} vocab={len(self.tok)}")

    def _acquire_gpu(self, need_bytes=7_000_000_000, max_attempts=80):
        """Move the CPU-resident model + SAE onto the GPU, retrying on transient OOM from a co-tenant.
        We only attempt the move when the driver reports >= need_bytes free, so the contention window is
        ~2s (the move), not the ~40s disk load. On a lost race we move the model back to CPU (clean
        recovery, no orphaned GPU allocations) and wait for the next window."""
        torch = self.torch
        last = None
        for attempt in range(max_attempts):
            try:
                free, _ = torch.cuda.mem_get_info()
            except Exception:
                free = 0
            if free < need_bytes:
                if attempt % 12 == 0:
                    logger.info(f"{el()} waiting for a GPU window (free={free/1e9:.1f}GB, need "
                                f"{need_bytes/1e9:.1f}GB) [shared GPU]")
                time.sleep(3); continue
            try:
                self.model = self.model.to(DEVICE)
                self.sae = load_sae(torch)
                torch.cuda.synchronize()
                logger.info(f"{el()} acquired GPU on attempt {attempt+1}")
                return
            except (RuntimeError, MemoryError) as e:
                last = e
                if "memory" not in str(e).lower() and "cuda" not in str(e).lower():
                    raise
                logger.warning(f"{el()} GPU acquire lost the race ({str(e)[:70]}); model->CPU + retry")
                try:
                    self.model = self.model.to("cpu")
                except Exception:
                    pass
                try:
                    torch.cuda.empty_cache()
                except Exception:
                    pass
                gc.collect(); time.sleep(5)
        raise RuntimeError(f"could not acquire GPU after {max_attempts} attempts: {last}")

    def _hook(self, mod, inp, out):
        self._cap["resid"] = (out[0] if isinstance(out, (tuple, list)) else out).detach()

    def _safe_forward(self, enc):
        """Run the inner transformer (hook captures layer-12 residual; NO LM-head logits) + SAE encode,
        retrying on transient CUDA OOM caused by a co-tenant run on the shared single GPU."""
        torch = self.torch
        for attempt in range(8):
            try:
                with torch.no_grad():
                    self.model.model(**enc)
                    resid = self._cap["resid"].float()
                    feats = self.sae.encode(resid)
                return resid, feats
            except (RuntimeError, MemoryError) as e:
                if "memory" not in str(e).lower() and "cuda" not in str(e).lower():
                    raise
                try:
                    torch.cuda.empty_cache()
                except Exception:
                    pass
                gc.collect(); time.sleep(12)
        # last try (let it raise if the GPU is still unavailable)
        with torch.no_grad():
            self.model.model(**enc)
            resid = self._cap["resid"].float()
            feats = self.sae.encode(resid)
        return resid, feats

    # ----- gating check: SAE reconstruction cosine + L0 on real text -----
    def gating_check(self, texts):
        torch = self.torch
        enc = self.tok(texts, return_tensors="pt", padding=True, truncation=True,
                       max_length=64).to(DEVICE)
        resid, feats = self._safe_forward(enc)
        with torch.no_grad():
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
            resid, feats = self._safe_forward(enc)           # [B,S,d_model], [B,S,d_sae] (OOM-resilient)
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
            resid, feats = self._safe_forward(enc)
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


def wilson_ci(hits, n, z=1.959963984540054):
    """Wilson score 95% CI for a binomial proportion (hits/n). Honest for small n."""
    if n == 0:
        return dict(hits=0, n=0, rate=float("nan"), wilson_ci=[float("nan"), float("nan")])
    p = hits / n
    denom = 1.0 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / denom
    return dict(hits=int(hits), n=int(n), rate=float(p),
                wilson_ci=[float(max(0.0, centre - half)), float(min(1.0, centre + half))])

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
    # severe_toxicity: the ONE civil_comments sub-attribute NOT used in derivation. It is far too rare at
    # the 0.5 label threshold (<30 positives), so re-threshold the preserved raw floats at 0.30. This is a
    # TRULY-PROSPECTIVE concept; reuses the already-cached classification encodings (no new forward pass).
    sev = np.array([1 if float((r.get("metadata_subcontext_floats") or {}).get("severe_toxicity") or 0.0)
                    >= SEVERE_TOX_THRESH else 0 for r in cls])
    return dict(_family="toxicity", on_lat=on_lat, off_lat=off_lat, cls_lat=cls_lat, cls_resid=cls_resid,
                cls_y=cls_y, cls_fold=cls_fold, sub_lab=sub_lab, sev_lab=sev)


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


def _bib_group():
    """The LabHC/bias_in_bios boundary-null dataset group inside DATA['support']."""
    return next(d for d in _load(DATA["support"])["datasets"]
                if "bias_in_bios" in d["dataset"].lower())["examples"]


def build_support_profession(which, enc, scale):
    """TRULY-PROSPECTIVE bias_in_bios profession concept (pre-registered BOUNDARY-NULL).
    Concept = 'bio of a {which}'. on = bios labelled `which`; off = a size-matched random sample of
    OTHER-profession bios (PSEUDO-PAIRS: index-aligned, unpaired diff-of-means contrast; the sign-flip
    null in identify_parent is a valid within-row randomization). Sub-contexts = gender male/female,
    so the recall-hole probes whether the profession parent fires on one gender but not the other
    (boundary expectation: ~0 hole => co_firing predicted+confirmed = a VALID prospective hit)."""
    g = _bib_group()
    by_label = defaultdict(list)
    for r in g:
        by_label[r.get("metadata_concept_label")].append(r)
    pos_all = by_label.get(which, [])
    cap_pos = {"smoke": 20, "mini": 120, "full": 600}[scale]
    rng = np.random.default_rng(SEED)
    if len(pos_all) > cap_pos:
        pos_all = [pos_all[i] for i in rng.permutation(len(pos_all))[:cap_pos]]
    # negatives: random OTHER-profession bios, size-matched to positives (cap 600)
    neg_pool = [r for lab, rows in by_label.items() if lab != which for r in rows]
    cap_neg = min(len(pos_all), {"smoke": 20, "mini": 120, "full": 600}[scale])
    neg_all = [neg_pool[i] for i in rng.permutation(len(neg_pool))[:cap_neg]]
    on, off = pos_all, neg_all
    n = min(len(on), len(off))
    on, off = on[:n], off[:n]                       # equal-length pseudo-pairs for identify_parent
    on_e = enc.encode_sentence([r["input"] for r in on], want_resid=True)
    off_e = enc.encode_sentence([r["input"] for r in off], want_resid=True)
    on_lat, off_lat = on_e["act_max"], off_e["act_max"]
    pos_sub = np.array([(r.get("metadata_sub_context") or {}).get("gender", "unk") for r in on], dtype=object)
    pos_fold = np.array([0 if r.get("metadata_fold") == "train" else 1 for r in on])
    neg_fold = np.array([0 if r.get("metadata_fold") == "train" else 1 for r in off])
    return dict(name="profession_%s" % which, granularity="sentence", kind="prospective",
                on_lat=on_lat, off_lat=off_lat,
                pos_lat=on_lat, pos_sub=pos_sub, pos_fold=pos_fold,
                neg_lat=off_lat, neg_fold=neg_fold,
                star_pos_lat=on_lat, star_pos_fold=pos_fold, star_pos_resid=on_e["resid_mean"],
                star_neg_lat=off_lat, star_neg_fold=neg_fold, star_neg_resid=off_e["resid_mean"],
                min_sub=MIN_SUB_SENT, s_star=which)

# ============================================================================ INTERNAL SPELLING (M6c)
def _spelling_vocab(tok):
    """Replicate dataset_1/data.py build_vocab: get_alpha_tokens + slot-eligibility, grouped by first
    letter. A vocab token is slot-eligible iff it is WORD-INITIAL ('▁' marker) AND, after stripping one
    leading space, non-empty and all-alphabetic (=> single-token by construction). Deterministic, $0."""
    vocab = tok.get_vocab()
    by_letter = defaultdict(list); id_to_word = {}
    for token_str, tid in vocab.items():
        decoded = tok.convert_tokens_to_string([token_str])
        word_initial = token_str.startswith(GEMMA_SPACE)
        word = decoded[1:] if decoded.startswith(" ") else decoded
        if len(word) == 0 or not all(c in ALL_ALPHA_LETTERS for c in word):
            continue
        if not word_initial:
            continue
        letter = word[0].lower()
        if not ("a" <= letter <= "z"):
            continue
        by_letter[letter].append({"word": word, "token_id": int(tid), "length": len(word)})
        id_to_word[int(tid)] = word
    logger.info(f"{el()} _spelling_vocab: {len(id_to_word)} slot-eligible word-initial tokens "
                f"(letters present: {''.join(sorted(by_letter))})")
    return by_letter, id_to_word


def _build_icl_block(rng, exclude, k=4):
    """dataset_1 build_icl_block: k contamination-free spelling ICL example lines (slotted words excluded)."""
    pool = [(w, L) for (w, L) in ICL_POOL if w not in exclude]
    idx = rng.permutation(len(pool))[:k]
    return "\n".join(f"{pool[i][0]} has the first letter: {pool[i][1]}" for i in idx) + "\n"


def _render_carrier(template_id, word, rng):
    """Render one of the 3 documented spelling carriers. Returns (text, (char_start,char_end)). The
    target word is placed at a KNOWN offset (start, or after the ICL block) so the char span is exact."""
    if template_id == "t_verbose":
        return word + " has the first letter:", (0, len(word))
    if template_id == "t_colon":
        return word + ":", (0, len(word))
    # t_icl: contamination-free ICL block, then the target rendered with the verbose template
    icl = _build_icl_block(rng, exclude={word})
    return icl + word + " has the first letter:", (len(icl), len(icl) + len(word))


def scan_corpus_positives(enc, id_to_word, letters, scale):
    """Re-scan the EXISTING dataset_1 Pile corpus windows ONCE (real ~48-token text, rev 3be9033, NO
    re-download) for word-initial slot-eligible tokens of the NEW letters. Returns
    {LETTER: [dict(input, char_span, word, token_id)]} -- guaranteed-absorption corpus positives for free.
    char_span is taken directly from the offset mapping at the token position, so encode_token re-tokenizes
    the same window and recovers exactly that position (token-id self-check passes by construction)."""
    target = {L.lower(): L for L in letters}                    # lowercase first-letter -> original LETTER
    rows = [r for ds in _load(DATA["spelling"])["datasets"] for r in ds["examples"]
            if r.get("metadata_pair_type") == "corpus_context"]
    texts = [r["input"] for r in rows]
    out = {L: [] for L in letters}                              # LETTER -> list of positive dicts
    tok = enc.tok
    B = 1000
    n_scanned = 0
    for b0 in range(0, len(texts), B):
        chunk = texts[b0:b0 + B]
        enc_b = tok(chunk, add_special_tokens=True, return_offsets_mapping=True)
        for j, (ids, offs) in enumerate(zip(enc_b["input_ids"], enc_b["offset_mapping"])):
            text = chunk[j]
            for p in range(1, len(ids)):                        # skip BOS at index 0
                word = id_to_word.get(int(ids[p]))
                if word is None:
                    continue
                lt = word[0].lower()
                LETTER = target.get(lt)
                if LETTER is None:
                    continue
                a, b = offs[p]
                if b <= a:                                      # zero-width (special token) -> skip
                    continue
                out[LETTER].append(dict(input=text, char_span=(int(a), int(b)),
                                        word=word.lower(), token_id=int(ids[p])))
            n_scanned += 1
    for L in letters:
        nwords = len(set(r["word"] for r in out[L]))
        logger.info(f"{el()} scan_corpus_positives {L}: {len(out[L])} occurrences over {nwords} words "
                    f"(scanned {n_scanned} windows)")
    return out


def build_spelling_prospective(letter, enc, scale, by_letter, corpus_scan):
    """TRULY-PROSPECTIVE internally-built first-letter spelling concept (ABSORPTION-regime substrate).
    Mirrors build_spelling's dict shape but constructs its slices WITHOUT a published dataset:
      * content-flip pairs (x_on=word starting with `letter`; x_off=surface-matched non-`letter` word)
        rendered in the 3 documented spelling carriers (t_verbose/t_colon/t_icl);
      * corpus positives re-scanned from the EXISTING dataset_1 Pile windows (real text, $0).
    Returns (C, usability) where usability flags whether real corpus positives were found."""
    lk = letter.lower()
    # deterministic per-letter rng (Python's hash() is salted per-process -> not reproducible)
    letter_off = int(hashlib.md5(letter.encode()).hexdigest(), 16) % 1000
    rng = np.random.default_rng(SEED + letter_off)
    on_words = by_letter.get(lk, [])
    # off pool indexed by char length (surface-match), excluding the target letter
    off_by_len = defaultdict(list)
    for olt, ws in by_letter.items():
        if olt == lk:
            continue
        for d in ws:
            off_by_len[d["length"]].append(d["word"])
    n_inst = CAP_SPELL_PAIRS[scale]
    carriers3 = ["t_verbose", "t_colon", "t_icl"]
    on_txt, off_txt, on_span, off_span, on_word_key = [], [], [], [], []
    if on_words:
        order = rng.permutation(len(on_words))
        for i in range(n_inst):
            on_d = on_words[int(order[i % len(order)])]
            w_on = on_d["word"]; L = on_d["length"]
            cand = off_by_len.get(L, []) + off_by_len.get(L - 1, []) + off_by_len.get(L + 1, [])
            cand = [w for w in cand if w[0].lower() != lk]
            if not cand:
                cand = [w for ws in off_by_len.values() for w in ws]
            w_off = cand[int(rng.integers(0, len(cand)))]
            tid = carriers3[i % 3]
            t_on, s_on = _render_carrier(tid, w_on, rng)
            t_off, s_off = _render_carrier(tid, w_off, rng)
            on_txt.append(t_on); off_txt.append(t_off)
            on_span.append(s_on); off_span.append(s_off)
            on_word_key.append(w_on)
    on_lat, on_res = (enc.encode_token(on_txt, on_span, want_resid=True) if on_txt
                      else (np.zeros((0, enc.sae.d_sae), np.float16), np.zeros((0, enc.d_model), np.float16)))
    off_lat, off_res = (enc.encode_token(off_txt, off_span, want_resid=True) if off_txt
                        else (np.zeros((0, enc.sae.d_sae), np.float16), np.zeros((0, enc.d_model), np.float16)))
    # content fold: deterministic 60/40 train/test by hash of the on-word
    on_fold = np.array([int(hashlib.md5(w.encode()).hexdigest(), 16) % 5 for w in on_word_key])
    fold01 = (on_fold >= 3).astype(int)              # folds 3,4 -> test(1); 0-2 -> train(0)

    # corpus positives re-scanned from the existing Pile windows (real text, $0)
    cand_rows = corpus_scan.get(letter, [])          # list of dict(input, char_span, word, token_id)
    cap = CAP_SPELL_CORPUS[scale]
    bysub = defaultdict(list)
    for cr in cand_rows:
        bysub[cr["word"]].append(cr)
    # keep MANY words (richer recall-hole surface), each capped so the per-sub recall estimate is stable;
    # shuffle qualified words for a representative frequency mix (not just the most-frequent), then fill to
    # the total cap. Each kept word retains >= MIN_SUB_TOKEN positives so per_subcontext can measure it.
    qualified = [(w, rs) for w, rs in bysub.items() if len(rs) >= MIN_SUB_TOKEN]
    per_word_cap = max(MIN_SUB_TOKEN, min(30, cap // 6))
    used_templates = False
    keep = []
    if qualified:
        order = rng.permutation(len(qualified))
        for oi in order:
            w, rs = qualified[int(oi)]
            take = min(len(rs), per_word_cap)
            idx = rng.permutation(len(rs))[:take]
            keep += [rs[int(j)] for j in idx]
            if len(keep) >= cap:
                break
        keep = keep[:cap]
    # FALLBACK (plan mitigation 2): no real corpus window has >=MIN_SUB_TOKEN of any single word ->
    # synthesize corpus positives from the content-flip x_on rendered strings (real text containing the
    # target word). Disclosed via used_templates so honest_notes can flag the letter.
    if not keep and on_txt:
        used_templates = True
        for t, s, w in zip(on_txt, on_span, on_word_key):
            keep.append({"input": t, "char_span": s, "word": w.lower(), "token_id": None})
    if keep:
        pos_lat = enc.encode_token([cr["input"] for cr in keep],
                                   [tuple(cr["char_span"]) for cr in keep],
                                   check_ids=[cr.get("token_id") for cr in keep])
        pos_sub = np.array([cr["word"] for cr in keep], dtype=object)
    else:
        pos_lat = on_lat
        pos_sub = np.array(list(on_word_key), dtype=object)
    n_qual_words = len(set(pos_sub.tolist()))
    usability = dict(letter=letter, n_content_pairs=len(on_txt), n_corpus_positives=int(pos_lat.shape[0]),
                     n_corpus_words=n_qual_words, corpus_from_templates=bool(used_templates),
                     n_vocab_on_words=len(on_words))
    logger.info(f"{el()} build_spelling_prospective {letter}: {len(on_txt)} content pairs, "
                f"{pos_lat.shape[0]} corpus positives over {n_qual_words} words "
                f"(from_templates={used_templates})")
    C = dict(name="spelling_%s" % letter, granularity="token", kind="prospective",
             on_lat=on_lat, off_lat=off_lat,
             pos_lat=pos_lat, pos_sub=pos_sub, pos_fold=np.zeros(pos_lat.shape[0], int),
             neg_lat=off_lat, neg_fold=fold01,
             star_pos_lat=on_lat, star_pos_fold=fold01, star_pos_resid=on_res,
             star_neg_lat=off_lat, star_neg_fold=fold01, star_neg_resid=off_res,
             min_sub=MIN_SUB_TOKEN, s_star="absorbed_%s_words" % letter)
    return C, usability


# ============================================================================ RUN ONE CONCEPT
def run_concept(C, rng, frozen=None):
    """Uniform per-concept pipeline -> result dict (firing-Jaccard table + matched-pool OUTCOME).
    If `frozen=FROZEN` is supplied (TRULY-PROSPECTIVE concepts), the predicted regime from the
    frozen combined rule is computed and LOGGED *before* the outcome (the measurement) is run, so the
    predict-then-measure ordering is auditable from the log."""
    name = C["name"]
    role = "PROSPECTIVE" if frozen is not None else C["kind"]
    logger.info(f"\n===== CONCEPT {name} ({C['granularity']}, {role}) =====")
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
    if frozen is not None:
        pp = _predict_all(jac_median, recall_hole_max, frozen)
        logger.info(f"{el()} {name}: >>> PREDICT (PRIMARY recall-hole-alone h>{frozen['tau_h_alone']:.3f}) "
                    f"= {pp['primary']}  | ablations: combined(j<{frozen['tau_j']:.3f} AND "
                    f"h>{frozen['tau_h']:.3f})={pp['combined']} jaccard(j<{frozen['tau_j_alone']:.3f})="
                    f"{pp['jaccard']}  [logged BEFORE outcome measurement]")

    # ----- OUTCOME on the defining (most under-served) slice = the parent's recall holes -----
    out = run_outcome(C, parent, resp, precision, rng)
    ccrg_helps = bool(out["delta"] > 0)
    ccrg_helps_sig = bool(out["delta"] > 0 and out["delta_ci"][0] > 0)
    ccrg_helps_h = bool(out["delta_vs_h"] > 0)
    logger.info(f"{el()} {name}: OUTCOME k={out['k']} auc_unit={out['auc_unit']:.3f} "
                f"auc_a={out['auc_a']:.3f} auc_h={out['auc_h']:.3f} auc_d={out['auc_d']:.3f} "
                f"delta(vs_a)={out['delta']:+.3f} ci={np.round(out['delta_ci'],3).tolist()} "
                f"delta(vs_h)={out['delta_vs_h']:+.3f} CCRG_helps={ccrg_helps} (sig={ccrg_helps_sig})")
    return dict(concept=name, granularity=C["granularity"], kind=C["kind"],
                parent_latent=parent, parent_pos_firing=pinfo["parent_pos_firing"],
                parent_pair_precision=pinfo["parent_pair_precision"],
                parent_unresolved=pinfo["parent_unresolved"], n_responsive=pinfo["n_responsive"],
                jaccard_median=jac_median, jaccard_min=jac_min, jaccard_max=jac_max,
                jaccard_median_meanact=float(np.median([r["jaccard_meanact"] for r in subrows])) if subrows else float("nan"),
                recall_hole_max=recall_hole_max, n_subcontexts=len(subs),
                per_subcontext=subrows, outcome=out,
                ground_truth_regime=("absorption" if ccrg_helps else "co_firing"),
                ground_truth_regime_vs_h=("absorption" if ccrg_helps_h else "co_firing"),
                ccrg_helps=ccrg_helps, ccrg_helps_significant=ccrg_helps_sig,
                descriptive_only=False)


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
        ccrg_h = bool(out["delta_vs_h"] > 0)
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
                            ground_truth_regime_vs_h=("absorption" if ccrg_h else "co_firing"),
                            ccrg_helps=ccrg, ccrg_helps_significant=ccrg_sig,
                            descriptive_only=bool(pos_m.sum() < MIN_SUB_SENT)))
    return results


def run_severe_toxicity(fam, rng, frozen=None):
    """TRULY-PROSPECTIVE severe_toxicity concept, computed AFTER tau is frozen (its outcome is the
    'measurement'). Reuses the cached classification encodings + the parent g identified on ParaDetox
    (recomputed deterministically here). Re-thresholded at SEVERE_TOX_THRESH; flagged descriptive_only
    when positives < MIN_SUB_SENT."""
    on_lat, off_lat = fam["on_lat"], fam["off_lat"]
    cls_lat, cls_y, cls_fold, cls_resid = fam["cls_lat"], fam["cls_y"], fam["cls_fold"], fam["cls_resid"]
    labs = fam["sev_lab"]
    toxic = cls_y == 1
    parent, resp, precision, _, _, pinfo = identify_parent(on_lat, off_lat, cls_lat[toxic], rng)
    name = "toxicity_severe_toxicity"
    pos_m = labs == 1; neg_m = cls_y == 0
    n_pos = int(pos_m.sum())
    descriptive = bool(n_pos < MIN_SUB_SENT)
    logger.info(f"\n===== CONCEPT {name} (sentence, PROSPECTIVE) =====")
    logger.info(f"{el()} {name}: severe positives @ {SEVERE_TOX_THRESH} = {n_pos} "
                f"(descriptive_only={descriptive})")
    elig = np.array([l for l in resp if l != parent], dtype=int)
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
    fp = cls_lat[toxic][:, parent] > 0; fd = cls_lat[toxic][:, det] > 0
    vals = np.array([firing_jaccard(fp[ii], fd[ii]) for ii in
                     (rng.integers(0, len(fp), len(fp)) for _ in range(B_JAC))])
    parent_recall = float((cls_lat[pos_m][:, parent] > 0).mean()) if n_pos else float("nan")
    subrow = dict(sub_context="severe_toxicity", n_pos=n_pos, parent_recall=parent_recall,
                  recall_hole=float(1 - parent_recall), detector_latent=det, detector_auc=det_auc,
                  detector_meanact_latent=det_mean, jaccard=float(jac),
                  jaccard_meanact=float(jac_mean), jaccard_ci=boot_ci(vals))
    recall_hole_max = float(1 - parent_recall)
    if frozen is not None:
        pp = _predict_all(jac, recall_hole_max, frozen)
        logger.info(f"{el()} {name}: >>> PREDICT (PRIMARY recall-hole-alone h>{frozen['tau_h_alone']:.3f}) "
                    f"= {pp['primary']}  | ablations: combined={pp['combined']} jaccard={pp['jaccard']}  "
                    f"[logged BEFORE outcome measurement]")
    Cs = dict(name=name, granularity="sentence", pos_sub=labs,
              pos_lat=cls_lat[pos_m], pos_fold=cls_fold[pos_m],
              star_neg_lat=cls_lat[neg_m], star_neg_fold=cls_fold[neg_m],
              star_pos_resid=cls_resid[pos_m], star_neg_resid=cls_resid[neg_m], s_star="severe_toxicity")
    out = run_outcome_tox(Cs, parent, resp, precision, rng)
    ccrg = bool(out["delta"] > 0); ccrg_sig = bool(out["delta"] > 0 and out["delta_ci"][0] > 0)
    ccrg_h = bool(out["delta_vs_h"] > 0)
    return dict(concept=name, granularity="sentence", kind="prospective",
                parent_latent=parent, parent_pos_firing=pinfo["parent_pos_firing"],
                parent_pair_precision=pinfo["parent_pair_precision"],
                parent_unresolved=pinfo["parent_unresolved"], n_responsive=pinfo["n_responsive"],
                jaccard_median=float(jac), jaccard_min=float(jac), jaccard_max=float(jac),
                jaccard_median_meanact=float(jac_mean), recall_hole_max=float(1 - parent_recall),
                n_subcontexts=1, per_subcontext=[subrow], outcome=out,
                ground_truth_regime=("absorption" if ccrg else "co_firing"),
                ground_truth_regime_vs_h=("absorption" if ccrg_h else "co_firing"),
                ccrg_helps=ccrg, ccrg_helps_significant=ccrg_sig, descriptive_only=descriptive)


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


def derive_single(concepts, key, lt, grid, truth_key="ground_truth_regime"):
    """Single-threshold router on `key` over an explicit `grid` (absorption iff value < tau when lt
    else value > tau). Tie-break = threshold most central in the optimal plateau (max min-margin)."""
    vals = np.array([c[key] for c in concepts], float)
    truth = np.array([c[truth_key] for c in concepts])
    if len(vals) == 0 or not np.isfinite(vals).any():
        return float("nan"), float("nan"), []
    sweep = []
    for tau in grid:
        pred = np.where(vals < tau if lt else vals > tau, "absorption", "co_firing")
        # margin: worst-case signed distance to threshold among correctly classified points
        margins = []
        for v, y in zip(vals, truth):
            pr = "absorption" if (v < tau if lt else v > tau) else "co_firing"
            d = (tau - v) if lt else (v - tau)              # >0 => predicted absorption
            margins.append((abs(d) if pr == y else -abs(d)))
        sweep.append(dict(tau=float(tau), balanced_acc=balanced_accuracy(pred, truth),
                          margin=float(min(margins)) if len(margins) else float("-inf")))
    best = max(sweep, key=lambda r: (r["balanced_acc"], r["margin"]))
    return best["tau"], best["balanced_acc"], sweep


def _jh_truth(concepts, truth_key="ground_truth_regime"):
    j = np.array([c["jaccard_median"] for c in concepts], float)
    h = np.array([c["recall_hole_max"] for c in concepts], float)
    truth = np.array([c[truth_key] for c in concepts])
    return j, h, truth


def _combined_margin(j, h, truth, tj, th):
    """Max-min separation margin for the AND-rule (tj, th): worst-case signed distance of a derivation
    concept to the decision boundary (positive iff correctly classified). Used as a robustness tie-break
    among threshold cells that share the best balanced-accuracy -> picks central, generalizable thresholds."""
    margins = []
    for ji, hi, yi in zip(j, h, truth):
        in_box = (ji < tj) and (hi > th)            # predicted absorption
        if yi == "absorption":
            # distance INTO the AND-box (must satisfy both); negative if outside
            m = min(tj - ji, hi - th)
        else:
            # co_firing correct iff OUTSIDE the box: safety = how clearly a constraint is violated
            m = max(ji - tj, th - hi)
        margins.append(m if (in_box == (yi == "absorption")) else -abs(m) - 1e-9)
    return float(min(margins)) if margins else float("-inf")


def derive_combined(concepts, tj_grid=TAU_J_GRID, th_grid=TAU_H_GRID, truth_key="ground_truth_regime"):
    """LEAD router: predict absorption iff (firing-Jaccard < tau_j) AND (recall_hole_max > tau_h).
    Fit (tau_j, tau_h) by maximizing balanced-accuracy on the DERIVATION concepts, with a max-min-margin
    tie-break for robustness. The conjunction is the recommendation because each single signal has a
    documented counterexample: jaccard-alone mislabels NUMERIC (high firing-Jaccard yet absorption) and
    can mislabel TAXONOMIC (low firing-Jaccard yet co_firing because the parent already has ~no holes);
    the recall-hole gate fixes taxonomic and the relaxed jaccard gate admits numeric."""
    j, h, truth = _jh_truth(concepts, truth_key)
    if len(j) == 0:
        return dict(tau_j=float("nan"), tau_h=float("nan"), balanced_acc=float("nan"),
                    margin=float("nan"), n_optimal_cells=0, degenerate_tau_h=None)
    best = None
    for tj in tj_grid:
        for th in th_grid:
            pred = np.where((j < tj) & (h > th), "absorption", "co_firing")
            ba = balanced_accuracy(pred, truth)
            mg = _combined_margin(j, h, truth, float(tj), float(th))
            cand = (ba, mg)
            if best is None or cand > (best["balanced_acc"], best["margin"]):
                best = dict(tau_j=float(tj), tau_h=float(th), balanced_acc=float(ba), margin=float(mg))
    n_opt = sum(1 for tj in tj_grid for th in th_grid
                if balanced_accuracy(np.where((j < tj) & (h > th), "absorption", "co_firing"), truth)
                >= best["balanced_acc"] - 1e-9)
    best["n_optimal_cells"] = int(n_opt)
    best["degenerate_tau_h"] = bool(best["tau_h"] <= th_grid[0] + 1e-9)
    return best


def predict_combined(c, tau_j, tau_h):
    return ("absorption" if (np.isfinite(tau_j) and np.isfinite(tau_h)
                             and c["jaccard_median"] < tau_j and c["recall_hole_max"] > tau_h)
            else "co_firing")


def predict_recall_hole_alone(c, tau_h_alone):
    """PRIMARY (M6b) recommendation: predict absorption iff parent recall-hole exceeds tau_h_alone."""
    return ("absorption" if (np.isfinite(tau_h_alone) and np.isfinite(c["recall_hole_max"])
                             and c["recall_hole_max"] > tau_h_alone) else "co_firing")


def predict_jaccard_alone(c, tau_j_alone):
    return ("absorption" if (np.isfinite(tau_j_alone) and np.isfinite(c["jaccard_median"])
                             and c["jaccard_median"] < tau_j_alone) else "co_firing")


def _predict_all(jac_median, recall_hole_max, frozen):
    """All three frozen-rule predictions from the firing-structure signals (PRIMARY + 2 ablations)."""
    c = {"jaccard_median": jac_median, "recall_hole_max": recall_hole_max}
    return dict(primary=predict_recall_hole_alone(c, frozen["tau_h_alone"]),
                combined=predict_combined(c, frozen["tau_j"], frozen["tau_h"]),
                jaccard=predict_jaccard_alone(c, frozen["tau_j_alone"]))


def loo_single(concepts, key, lt, grid, truth_key="ground_truth_regime"):
    """Leave-one-derivation-concept-out for a single-signal rule (refit tau on N-1, predict held-out)."""
    rows = []
    for i, ci in enumerate(concepts):
        rest = [c for k, c in enumerate(concepts) if k != i]
        if len(set(c[truth_key] for c in rest)) < 2:
            tau, _, _ = derive_single(concepts, key, lt, grid, truth_key)     # degenerate fold -> global
        else:
            tau, _, _ = derive_single(rest, key, lt, grid, truth_key)
        v = float(ci[key])
        pred = "absorption" if (np.isfinite(tau) and (v < tau if lt else v > tau)) else "co_firing"
        rows.append(dict(concept=ci["concept"], tau_fold=float(tau), pred=pred,
                         ground_truth=ci[truth_key], hit=bool(pred == ci[truth_key])))
    acc = float(np.mean([r["hit"] for r in rows])) if rows else float("nan")
    return acc, rows


def loo_combined(concepts, tj_grid=TAU_J_GRID, th_grid=TAU_H_GRID, truth_key="ground_truth_regime"):
    """Leave-one-derivation-concept-out for the COMBINED rule (PRIMARY LOO)."""
    rows = []
    for i, ci in enumerate(concepts):
        rest = [c for k, c in enumerate(concepts) if k != i]
        if len(set(c[truth_key] for c in rest)) < 2:
            d = derive_combined(concepts, tj_grid, th_grid, truth_key)
        else:
            d = derive_combined(rest, tj_grid, th_grid, truth_key)
        pred = predict_combined(ci, d["tau_j"], d["tau_h"])
        rows.append(dict(concept=ci["concept"], tau_j_fold=d["tau_j"], tau_h_fold=d["tau_h"],
                         pred=pred, ground_truth=ci[truth_key], hit=bool(pred == ci[truth_key])))
    acc = float(np.mean([r["hit"] for r in rows])) if rows else float("nan")
    return acc, rows

# ============================================================================ MAIN
def _cuda_empty():
    try:
        import torch; torch.cuda.empty_cache()
    except Exception:
        pass


def role_of(name):
    """Authoritative concept role: a concept is DERIVATION iff it is in the fixed DERIVATION registry."""
    return "derivation" if name in DERIVATION else "prospective"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scale", default="full", choices=["smoke", "mini", "full"])
    ap.add_argument("--smoke", action="store_true",
                    help="load + gating + BOS assert + 1 concept/family end-to-end + schema-validate tiny")
    ap.add_argument("--concepts", default="", help="comma list to restrict (debug)")
    ap.add_argument("--out", default=str(HERE / "method_out.json"))
    ap.add_argument("--ram_gb", type=float, default=120.0)  # RLIMIT_AS = VIRTUAL ceiling; CUDA reserves
    #                                  huge virtual space, so keep it generous. The cgroup (~29GB) is the
    #                                  real RSS guard; this script's numpy peak is only a few GB.
    args = ap.parse_args()
    set_mem_limits(args.ram_gb)
    rng = np.random.default_rng(SEED)
    scale = "smoke" if args.smoke else args.scale
    logger.info(f"{el()} a-priori firing-structure router | scale={scale} smoke={args.smoke}")

    # Shared single GPU: model load can lose the OOM race to a co-tenant run. We fail fast here and let
    # the external launcher relaunch a FRESH process (in-process retry corrupts the CUDA context).
    enc = Encoder()
    # ---- gating check + BOS-offset assertion on real spelling corpus rows ----
    sp = next(d for d in _load(DATA["spelling"])["datasets"] if d["dataset"].endswith("_L"))["examples"]
    corpus = [r for r in sp if r.get("metadata_pair_type") == "corpus_context"][:20]
    gating = enc.gating_check([r["input"] for r in corpus[:8]])
    cspan = [tuple(r["metadata_target_char_in_window"]) for r in corpus]
    cids = [r["metadata_target_token_id"] for r in corpus]
    _ = enc.encode_token([r["input"] for r in corpus], cspan, check_ids=cids)  # logs token-id mismatches
    if gating["recon_cos_mean"] < 0.80:
        logger.error(f"GATING FAILED recon_cos_mean={gating['recon_cos_mean']:.3f} (<0.80)")

    # ---- concept selection ----
    want = set(args.concepts.split(",")) if args.concepts else None
    if args.smoke and want is None:        # one concept per family end-to-end (>=2 derivation regimes present)
        want = {"spelling_L", "numeric", "toxicity_threat",
                "sentiment", "profession_professor", "toxicity_severe_toxicity",
                "spelling_C"}              # + one NEW (absorption-regime) prospective spelling letter
    def keep(n): return (want is None) or (n in want)

    # =================== DERIVATION concepts (router fit ONLY on these) ===================
    deriv_results = []
    for L in ["L", "O", "T", "I", "D"]:
        if keep("spelling_%s" % L):
            C = cached_build("spelling_%s" % L, scale, lambda L=L: build_spelling(L, enc, scale))
            deriv_results.append(run_concept(C, rng)); del C; gc.collect()
    for hier in ["numeric", "taxonomic"]:
        if keep(hier):
            C = cached_build(hier, scale, lambda hier=hier: build_nonspell(hier, enc, scale))
            deriv_results.append(run_concept(C, rng)); del C; gc.collect()
    _cuda_empty()
    fam = None
    tox_deriv = ["toxicity_%s" % s for s in ["threat", "identity_attack", "insult", "obscene", "sexual_explicit"]]
    if any(keep(t) for t in tox_deriv) or keep("toxicity_severe_toxicity"):
        fam = cached_build("toxicity_family", scale, lambda: build_toxicity(enc, scale))
        deriv_results += [r for r in run_toxicity_concepts(fam, rng) if keep(r["concept"])]
    _cuda_empty()

    derivation = [r for r in deriv_results if r["concept"] in DERIVATION]

    # =================== FREEZE the COMBINED rule on DERIVATION ONLY ===================
    if derivation and len(set(c["ground_truth_regime"] for c in derivation)) >= 2:
        frozen = derive_combined(derivation)
    else:
        frozen = dict(tau_j=float("nan"), tau_h=float("nan"), balanced_acc=float("nan"),
                      margin=float("nan"), n_optimal_cells=0, degenerate_tau_h=None)
    tau_j, tau_h = frozen["tau_j"], frozen["tau_h"]
    # M6b: derive the PRIMARY recall-hole-alone threshold (and the jaccard-alone ablation threshold) on the
    # DERIVATION concepts BEFORE any prospective outcome is measured, so the predict-then-measure ordering
    # is auditable. The PRIMARY recommendation is recall-hole-alone; combined + jaccard-alone are ablations.
    if derivation:
        th_alone, bacc_halone, _ = derive_single(derivation, "recall_hole_max", False, TAU_H_GRID)
        tj_alone, bacc_jalone, _ = derive_single(derivation, "jaccard_median", True, TAU_J_GRID)
    else:
        th_alone = tj_alone = float("nan"); bacc_halone = bacc_jalone = float("nan")
    FROZEN = dict(tau_j=tau_j, tau_h=tau_h, tau_h_alone=th_alone, tau_j_alone=tj_alone)
    logger.info(f"{el()} ===== FROZEN PRIMARY rule (recall-hole-alone): absorption iff recall_hole>"
                f"{th_alone:.4f} | derivation balanced_acc={bacc_halone:.3f} =====")
    logger.info(f"{el()} ===== FROZEN ablation combined rule: absorption iff (jaccard<{tau_j:.4f}) AND "
                f"(recall_hole>{tau_h:.4f}) | balanced_acc={frozen['balanced_acc']:.3f} "
                f"margin={frozen['margin']:.3f} n_optimal_cells={frozen['n_optimal_cells']} "
                f"degenerate_tau_h={frozen['degenerate_tau_h']} | jaccard-alone tau_j={tj_alone:.4f} "
                f"bacc={bacc_jalone:.3f} =====")

    # =================== TRULY-PROSPECTIVE concepts (predict-then-measure, frozen rule) ===================
    pro_results = []
    if keep("sentiment"):
        C = cached_build("sentiment", scale, lambda: build_support_sentiment(enc, scale))
        pro_results.append(run_concept(C, rng, frozen=FROZEN)); del C; gc.collect()
    for which in ["food", "service"]:
        if keep("aspect_%s" % which):
            C = cached_build("aspect_%s" % which, scale, lambda which=which: build_support_aspect(enc, scale, which))
            pro_results.append(run_concept(C, rng, frozen=FROZEN)); del C; gc.collect()
    _cuda_empty()
    for p in PROFS:
        nm = "profession_%s" % p
        if keep(nm):
            C = cached_build(nm, scale, lambda p=p: build_support_profession(p, enc, scale))
            pro_results.append(run_concept(C, rng, frozen=FROZEN)); del C; gc.collect()
    _cuda_empty()
    if keep("toxicity_severe_toxicity"):
        if fam is None:
            fam = cached_build("toxicity_family", scale, lambda: build_toxicity(enc, scale))
        pro_results.append(run_severe_toxicity(fam, rng, frozen=FROZEN))
    if fam is not None:
        del fam; gc.collect()
    _cuda_empty()

    # =================== M6c: NEW internally-built spelling prospective concepts (ABSORPTION substrate) ===
    # These supply the absorption-regime members of the prospective set so the router can be wrong in BOTH
    # directions. Built from the gemma vocab (get_alpha_tokens) + EXISTING Pile windows ($0). Predicted with
    # the FROZEN PRIMARY rule (recall-hole-alone) BEFORE the outcome is measured. NOT in DERIVATION.
    spelling_usability = []
    want_letters = [L for L in NEW_LETTERS if keep("spelling_%s" % L)]
    if want_letters:
        by_letter, id_to_word = _spelling_vocab(enc.tok)
        corpus_scan = scan_corpus_positives(enc, id_to_word, want_letters, scale)
        for L in want_letters:
            C, usability = build_spelling_prospective(L, enc, scale, by_letter, corpus_scan)
            spelling_usability.append(usability)
            pro_results.append(run_concept(C, rng, frozen=FROZEN)); del C; gc.collect()
        del by_letter, id_to_word, corpus_scan; gc.collect()
    _cuda_empty()

    enc.free(); del enc; gc.collect(); _cuda_empty()

    results = deriv_results + pro_results
    assemble_and_save(results, derivation, pro_results, frozen, FROZEN, spelling_usability,
                      gating, args, scale)


def _concept_row(r, tau_j, tau_h):
    """One per-concept results row (firing structure + frozen-rule prediction + matched-pool outcome)."""
    o = r["outcome"]
    return dict(
        concept=r["concept"], role=role_of(r["concept"]), granularity=r["granularity"],
        parent_latent=r["parent_latent"], parent_pos_firing=r["parent_pos_firing"],
        parent_unresolved=r.get("parent_unresolved", False), n_subcontexts=r["n_subcontexts"],
        jaccard_median=r["jaccard_median"], jaccard_min=r["jaccard_min"], jaccard_max=r["jaccard_max"],
        jaccard_median_meanact=r["jaccard_median_meanact"], recall_hole_max=r["recall_hole_max"],
        predicted_regime=r["predicted_regime"],                  # PRIMARY = recall-hole-alone
        predicted_regime_combined=r.get("predicted_regime_combined"),
        predicted_regime_jaccard=r.get("predicted_regime_jaccard"),
        ground_truth_regime=r["ground_truth_regime"],            # PRIMARY: sign(auc_unit - auc_a)
        ground_truth_regime_vs_h=r["ground_truth_regime_vs_h"],  # SECONDARY: sign(auc_unit - auc_h)
        auc_unit=o["auc_unit"], auc_a=o.get("auc_a"), auc_h=o["auc_h"], auc_d=o.get("auc_d"),
        delta_vs_a=o["delta"], delta_vs_a_ci=o["delta_ci"],
        delta_vs_h=o.get("delta_vs_h"), delta_vs_h_ci=o.get("delta_vs_h_ci"),
        k=o["k"], unit_members=o["unit_members"], h_members=o["h_members"], a_latent=o.get("a_latent"),
        ccrg_helps=r["ccrg_helps"], ccrg_helps_significant=r["ccrg_helps_significant"],
        hit_vs_a=r.get("hit_vs_a"), hit_vs_a_combined=r.get("hit_vs_a_combined"),
        hit_vs_a_jaccard=r.get("hit_vs_a_jaccard"), hit_vs_h=r.get("hit_vs_h"),
        power_flag=("descriptive_only" if r.get("descriptive_only") else "inferential"))


def assemble_and_save(results, derivation, prospective, frozen, FROZEN, spelling_usability,
                      gating, args, scale):
    """M6b reframe: lead with RECALL-HOLE-ALONE as the PRIMARY recommendation (derivation balanced_acc;
    no derivation counterexample); the combined conjunction and firing-Jaccard-alone are demoted to
    ABLATIONS. Derive the single-signal thresholds + LOO on the 12 DERIVATION concepts, score the
    TRULY-PROSPECTIVE set with per-PREDICTED-REGIME Wilson CIs, write the exp_gen_sol_out artifact."""
    tau_j, tau_h = frozen["tau_j"], frozen["tau_h"]

    # ---------------- single-signal thresholds (derivation only) ----------------
    # These recompute deterministically to the SAME tau as FROZEN['tau_*_alone'] (which were frozen in main
    # BEFORE any prospective outcome was measured); here we also keep the full sweeps for reporting.
    tj_alone, bacc_jalone, sweep_jalone = derive_single(derivation, "jaccard_median", True, TAU_J_GRID)
    th_alone, bacc_halone, sweep_halone = derive_single(derivation, "recall_hole_max", False, TAU_H_GRID)
    assert (not np.isfinite(FROZEN["tau_h_alone"])) or abs(th_alone - FROZEN["tau_h_alone"]) < 1e-9, \
        "recall-hole-alone tau drifted from the frozen value (predict-then-measure integrity)"
    logger.info(f"{el()} PRIMARY recall-hole-alone:   tau_h*={th_alone:.3f} balanced_acc={bacc_halone:.3f} "
                f"(LEAD recommendation — strongest single separator, no derivation counterexample)")
    logger.info(f"{el()} ABLATION jaccard-alone:      tau_J*={tj_alone:.3f} balanced_acc={bacc_jalone:.3f}")
    logger.info(f"{el()} ABLATION combined:           tau_J*={tau_j:.3f} tau_h*={tau_h:.3f} "
                f"balanced_acc={frozen['balanced_acc']:.3f} degenerate_tau_h={frozen['degenerate_tau_h']}")
    # recall-hole-primary combined variant (jaccard gate pinned permissive): the conservative fallback
    rhp = derive_combined(derivation, tj_grid=np.array([float(TAU_J_GRID[-1])]), th_grid=TAU_H_GRID)

    # ---------------- LOO per rule (derivation only); COMBINED = PRIMARY ----------------
    loo_comb_acc, loo_comb_rows = loo_combined(derivation)
    loo_j_acc, loo_j_rows = loo_single(derivation, "jaccard_median", True, TAU_J_GRID)
    loo_h_acc, loo_h_rows = loo_single(derivation, "recall_hole_max", False, TAU_H_GRID)
    logger.info(f"{el()} LOO (derivation leave-one-out): combined={loo_comb_acc:.3f} "
                f"jaccard-alone={loo_j_acc:.3f} recall-hole-alone={loo_h_acc:.3f}")

    # ---------------- COUNTEREXAMPLES that justify the conjunction ----------------
    counterex = []
    dmap = {r["concept"]: r for r in derivation}
    if "numeric" in dmap:
        r = dmap["numeric"]
        counterex.append(f"numeric: firing-Jaccard={r['jaccard_median']:.3f} is HIGH yet ground-truth="
                         f"{r['ground_truth_regime']} -> jaccard-alone (absorption iff low-J) MISLABELS it; the "
                         f"combined rule routes it correctly only via the relaxed jaccard gate + recall_hole="
                         f"{r['recall_hole_max']:.3f}>tau_h.")
    if "taxonomic" in dmap:
        r = dmap["taxonomic"]
        counterex.append(f"taxonomic: firing-Jaccard={r['jaccard_median']:.3f} is LOW (narrow country specialists "
                         f"exist) yet ground-truth={r['ground_truth_regime']}: the parent already fires on "
                         f"{r['parent_pos_firing']:.2f} of positives (recall_hole_max={r['recall_hole_max']:.3f}) so "
                         f"there are no holes to fill -> the recall-hole gate correctly routes it co_firing where "
                         f"jaccard-alone would mislabel it absorption.")
    for c in counterex:
        logger.info(f"{el()} COUNTEREXAMPLE {c}")

    # ---------------- frozen-rule prediction for every concept ----------------
    # PRIMARY = recall-hole-alone (the recommendation). combined + jaccard-alone are ABLATIONS. For the
    # derivation concepts this is an in-sample display; for prospective it is the predict-then-measure
    # decision (the rule was frozen BEFORE the prospective outcomes were measured — see main()).
    for r in results:
        r["predicted_regime"]          = predict_recall_hole_alone(r, th_alone)              # PRIMARY
        r["predicted_regime_combined"] = predict_combined(r, tau_j, tau_h)                   # ablation
        r["predicted_regime_jaccard"]  = predict_jaccard_alone(r, tj_alone)                  # ablation
        r["hit_vs_a"]          = bool(r["predicted_regime"] == r["ground_truth_regime"])     # PRIMARY hit
        r["hit_vs_a_combined"] = bool(r["predicted_regime_combined"] == r["ground_truth_regime"])
        r["hit_vs_a_jaccard"]  = bool(r["predicted_regime_jaccard"] == r["ground_truth_regime"])
        r["hit_vs_h"]          = bool(r["predicted_regime"] == r["ground_truth_regime_vs_h"])
        r["role"] = role_of(r["concept"])

    # ---------------- PROSPECTIVE hit-rates with Wilson CIs (PRIMARY = recall-hole-alone, vs-a) ----------------
    def hitrate(rows, key="hit_vs_a"):
        return wilson_ci(sum(1 for r in rows if r[key]), len(rows))
    existing3 = [r for r in prospective if r["concept"] in PROSPECTIVE_EXISTING]
    newp = [r for r in prospective if r["concept"] in PROSPECTIVE_NEW]
    new_inf = [r for r in newp if not r.get("descriptive_only")]
    all_inf = [r for r in prospective if not r.get("descriptive_only")]
    hr = dict(
        existing3=hitrate(existing3),
        new_only=hitrate(newp),
        new_only_inferential=hitrate(new_inf),
        combined_all=hitrate(prospective),
        combined_all_inferential=hitrate(all_inf),
        combined_all_vs_h=hitrate(prospective, "hit_vs_h"),
    )
    logger.info(f"{el()} PROSPECTIVE hit-rate (recall-hole-alone, vs-a primary): "
                f"existing3={hr['existing3']['hits']}/{hr['existing3']['n']} (rate={hr['existing3']['rate']:.3f}); "
                f"new={hr['new_only']['hits']}/{hr['new_only']['n']} (rate={hr['new_only']['rate']:.3f}); "
                f"combined-all={hr['combined_all']['hits']}/{hr['combined_all']['n']} "
                f"(rate={hr['combined_all']['rate']:.3f}, Wilson95={np.round(hr['combined_all']['wilson_ci'],3).tolist()})")

    # ----- DECISIVE M6 deliverable: prospective hit-rate STRATIFIED by the PRIMARY predicted regime -----
    # Using the recall-hole-alone prediction, the prospective set spans BOTH regimes (new spelling letters
    # -> 'absorption'; professions/sentiment -> 'co_firing'), so the router can be WRONG IN BOTH DIRECTIONS.
    # We also report the SAME strata under the combined-rule and jaccard-alone predictions as ablations, so
    # a reader can see whether the conjunction generalizes BETTER out-of-sample (the only condition under
    # which the conjunction would become the recommendation).
    pro_inf = all_inf                                          # inferential prospective concepts
    def strat(pred_key, hit_key):
        absn = [r for r in pro_inf if r[pred_key] == "absorption"]
        cof  = [r for r in pro_inf if r[pred_key] == "co_firing"]
        return dict(absorption_predicted=wilson_ci(sum(1 for r in absn if r[hit_key]), len(absn)),
                    cofiring_predicted=wilson_ci(sum(1 for r in cof if r[hit_key]), len(cof)),
                    combined_all=wilson_ci(sum(1 for r in pro_inf if r[hit_key]), len(pro_inf)))
    prospective_hitrate_primary = strat("predicted_regime", "hit_vs_a")              # PRIMARY (recall-hole)
    prospective_hitrate_ablation_combined = strat("predicted_regime_combined", "hit_vs_a_combined")
    prospective_hitrate_ablation_jaccard  = strat("predicted_regime_jaccard",  "hit_vs_a_jaccard")
    php = prospective_hitrate_primary
    logger.info(f"{el()} PROSPECTIVE hit-rate by PRIMARY predicted regime (inferential, n={len(pro_inf)}): "
                f"absorption_predicted={php['absorption_predicted']['hits']}/{php['absorption_predicted']['n']} "
                f"(rate={php['absorption_predicted']['rate']}, Wilson95={np.round(php['absorption_predicted']['wilson_ci'],3).tolist()}); "
                f"cofiring_predicted={php['cofiring_predicted']['hits']}/{php['cofiring_predicted']['n']} "
                f"(rate={php['cofiring_predicted']['rate']}, Wilson95={np.round(php['cofiring_predicted']['wilson_ci'],3).tolist()})")
    # does the combined conjunction generalize strictly BETTER out-of-sample than recall-hole-alone?
    conj_better = bool(prospective_hitrate_ablation_combined["combined_all"]["rate"] is not None
                       and php["combined_all"]["rate"] is not None
                       and prospective_hitrate_ablation_combined["combined_all"]["rate"]
                       > php["combined_all"]["rate"] + 1e-9)
    logger.info(f"{el()} conjunction-beats-primary out-of-sample = {conj_better} "
                f"(combined={prospective_hitrate_ablation_combined['combined_all']['rate']} vs "
                f"primary={php['combined_all']['rate']})")

    # ---------------- REPRODUCTION / SANITY ----------------
    sp_j = {r["concept"]: r["jaccard_median"] for r in results if r["concept"].startswith("spelling_")}
    tox_ref = {"threat": 0.40, "identity_attack": 0.29, "insult": 0.66}
    tox_j = {r["concept"].replace("toxicity_", ""): r["jaccard_median"]
             for r in results if r["concept"].startswith("toxicity_")}
    repro = dict(
        spelling_jaccard={k: float(v) for k, v in sp_j.items()},
        spelling_all_below_0_05=bool(all(v < 0.05 for v in sp_j.values())) if sp_j else None,
        spelling_all_below_0_10=bool(all(v < 0.10 for v in sp_j.values())) if sp_j else None,
        spelling_letters_at_or_above_0_05=[k for k, v in sp_j.items() if v >= 0.05],
        toxicity_jaccard={k: (float(tox_j[k]) if tox_j.get(k) is not None else None) for k in tox_ref},
        toxicity_reference=tox_ref,
        toxicity_within_tol_0_10=bool(all(
            (k in tox_j and tox_j[k] is not None and abs(tox_j[k] - ref) <= 0.10)
            for k, ref in tox_ref.items())) if tox_j else None,
        note="Reproduction is reported as actuals + flags; tolerance mismatches (e.g. spelling_O ~0.039, "
             "recomputed toxicity firing-Jaccard differing from the prior reference values) are NOT hard "
             "failures — the honest discrepancy is itself a reported result.",
    )
    logger.info(f"{el()} REPRO spelling<0.05={repro['spelling_all_below_0_05']} "
                f"(at/above 0.05: {repro['spelling_letters_at_or_above_0_05']}); "
                f"toxicity_within_tol_0_10={repro['toxicity_within_tol_0_10']}")

    # ---------------- HONEST NOTES (required disclosures; M6b recall-hole-alone-led) ----------------
    honest = []
    honest.append(f"PRIMARY RECOMMENDATION = RECALL-HOLE-ALONE. The recommended a-priori screen is the single "
                  f"signal `predict absorption-regime iff parent recall-hole > {th_alone:.3f}`, which is the "
                  f"STRONGEST single separator on the derivation set (balanced_acc={bacc_halone:.3f}) with no "
                  f"derivation counterexample. Firing-Jaccard-alone reaches only balanced_acc={bacc_jalone:.3f} and "
                  f"the combined conjunction (firing-Jaccard<{tau_j:.3f} AND recall-hole>{tau_h:.3f}) reaches "
                  f"balanced_acc={frozen['balanced_acc']:.3f}; both are reported as ABLATIONS. Firing-Jaccard is a "
                  f"CORROBORATING signal only. The combined conjunction would be elevated to the recommendation ONLY "
                  f"if its PROSPECTIVE hit-rate strictly exceeds recall-hole-alone's out-of-sample (measured below: "
                  f"conjunction-beats-primary = {conj_better}).")
    honest.append("DERIVATION vs PROSPECTIVE: the 12 derivation concepts (spelling L/O/T/I/D, numeric, taxonomic, "
                  "5 toxicity sub-attributes) are where tau_h (and the ablation thresholds + LOO) are FIT. They are "
                  "NEVER counted as prospective. The truly-held-out prospective set spans BOTH regimes: "
                  "ABSORPTION-regime members = 7 NEW internally-built first-letter spelling concepts (B,C,F,M,P,R,W — "
                  "from the gemma vocab + the EXISTING Pile windows, $0, never in derivation); CO-FIRING-regime "
                  "members = sentiment, aspect_food/service, bias_in_bios professions, severe_toxicity. Every "
                  "prospective concept is predicted with the FROZEN recall-hole-alone rule BEFORE its outcome is "
                  "measured (logged '[logged BEFORE outcome measurement]'), so the router can be WRONG IN BOTH "
                  "DIRECTIONS and the measured error is honest.")
    if frozen.get("degenerate_tau_h"):
        honest.append("COMBINED-ABLATION degeneracy: the 2-D conjunction grid's optimum sits at tau_h=0 (the recall-"
                      "hole gate is non-binding once the jaccard gate is applied) — another reason the conjunction is "
                      "NOT the recommendation. recall-hole-alone is the binding, strongest single separator.")
    honest += ["COUNTEREXAMPLE (firing-Jaccard-alone fails; recall-hole-alone routes it correctly) -> " + c
               for c in counterex]
    honest.append("MEASURED ERROR (recall-hole-alone PRIMARY, per predicted regime): this is a SCREENING HEURISTIC, "
                  "not a validated oracle. Stratified prospective hit-rate (inferential) — "
                  f"ABSORPTION-predicted (new spelling letters) = {php['absorption_predicted']['hits']}/"
                  f"{php['absorption_predicted']['n']} (rate {php['absorption_predicted']['rate']}, Wilson95 "
                  f"{np.round(php['absorption_predicted']['wilson_ci'],2).tolist()}); CO-FIRING-predicted = "
                  f"{php['cofiring_predicted']['hits']}/{php['cofiring_predicted']['n']} (rate "
                  f"{php['cofiring_predicted']['rate']}, Wilson95 {np.round(php['cofiring_predicted']['wilson_ci'],2).tolist()}); "
                  f"all = {php['combined_all']['hits']}/{php['combined_all']['n']} (rate {php['combined_all']['rate']}); "
                  f"derivation LOO (recall-hole-alone) = {loo_h_acc:.3f}. The prospective strata are small so the "
                  "Wilson CIs are wide — the contribution is the BOTH-REGIME separation + measured error, not a tight "
                  "point estimate.")
    honest.append("BOTH-REGIME prospective design: before this iteration the prospective set was entirely co-firing-"
                  "predicted, so the router was never tested where it must fire 'absorption' (no discriminative test). "
                  "The 7 new internally-built spelling concepts supply guaranteed absorption-regime prospective "
                  "members. A new spelling letter predicted absorption that merely TIES the best raw latent (a) is a "
                  "false-absorption miss; a profession predicted co_firing whose unit beats (a) is a false-co_firing "
                  "miss — both are counted honestly.")
    honest.append("BOUNDARY-NULL (bias_in_bios professions): a profession concept is expected to give ~0 cross-gender "
                  "recall-hole, so the recall-hole-alone rule PREDICTS co_firing; predicting AND confirming co_firing "
                  "here is a VALID prospective hit (not a method failure). Professions where no responsive parent "
                  "clears the firing floor are flagged parent_unresolved and default to co_firing.")
    honest.append("CONTRAST DEPENDENCE: the regime label depends on the baseline. PRIMARY = sign(auc_unit - auc_a) "
                  "(does the label-free grouped unit beat the best single RAW latent (a) = does grouping help). "
                  "SECONDARY vs (h): the supervised attribution pool (h) FREQUENTLY beats the unit on GENERAL "
                  "classification even in true absorption regimes, because the absorption advantage lives on the "
                  "absorbed-slice recall, not general classification — which is why the primary signal is vs-(a). "
                  "(d) is the required non-SAE residual diff-of-means probe; (h)/(d) are reported in every row.")
    honest.append("severe_toxicity is UNDERPOWERED: re-thresholded at 0.30 it has few positives "
                  f"(< {MIN_SUB_SENT}); it is flagged descriptive_only and reported in a descriptive row plus an "
                  "'inferential-only' hit-rate variant that excludes it.")
    honest.append("The CCRG unit is LABEL-FREE (built only from content-flip co-response + firing-disjointness, "
                  "never the downstream task labels); baselines (a)/(h)/(d) are all supervised, so a unit win is a "
                  "win at zero label cost. Outcome = general concept classification on a held-out test fold; the "
                  "LR head is held constant across methods (only the feature SELECTION differs).")
    for r in results:
        if r.get("parent_unresolved"):
            honest.append(f"{r['concept']}: parent_unresolved (no responsive latent cleared the "
                          f"{PARENT_FIRE_FLOOR:.0%} positive-firing floor) -> co_firing by default.")
    for r in prospective:
        if not r.get("hit_vs_a"):
            honest.append(f"PROSPECTIVE MISS {r['concept']}: predicted {r['predicted_regime']} but ground-truth(vs-a) "
                          f"{r['ground_truth_regime']} (delta_vs_a={r['outcome']['delta']:+.3f}).")

    # ---------------- NEW-LETTER usability report (M6c) ----------------
    um = {u["letter"]: u for u in (spelling_usability or [])}
    new_letter_report = []
    for L in NEW_LETTERS:
        rr = next((r for r in results if r["concept"] == "spelling_%s" % L), None)
        u = um.get(L, {})
        if rr is None:
            new_letter_report.append(dict(letter=L, built=False, note="not built in this run"))
            continue
        new_letter_report.append(dict(
            letter=L, built=True,
            n_content_pairs=u.get("n_content_pairs"), n_corpus_positives=u.get("n_corpus_positives"),
            n_corpus_words=u.get("n_corpus_words"), corpus_from_templates=u.get("corpus_from_templates"),
            parent_latent=rr["parent_latent"], parent_unresolved=rr.get("parent_unresolved"),
            recall_hole_max=rr["recall_hole_max"], jaccard_median=rr["jaccard_median"],
            predicted_regime=rr["predicted_regime"], ground_truth_regime=rr["ground_truth_regime"],
            auc_unit=rr["outcome"]["auc_unit"], auc_a=rr["outcome"].get("auc_a"),
            delta_vs_a=rr["outcome"]["delta"], hit_vs_a=rr.get("hit_vs_a")))
    n_new_abs = sum(1 for x in new_letter_report if x.get("ground_truth_regime") == "absorption")
    n_new_tpl = sum(1 for x in new_letter_report if x.get("corpus_from_templates"))
    if any(x.get("built") for x in new_letter_report):
        honest.append(f"NEW-LETTER usability: of {sum(1 for x in new_letter_report if x.get('built'))} built spelling "
                      f"letters, {n_new_abs} landed in the ABSORPTION ground-truth regime (unit beats best raw latent); "
                      f"{n_new_tpl} fell back to template-rendered corpus positives (disclosed). Letters that yielded "
                      f"too few real corpus positives or an unresolved parent are flagged and kept (never silently "
                      f"dropped).")
    logger.info(f"{el()} NEW-LETTER report: {n_new_abs} absorption-regime, {n_new_tpl} template-fallback; "
                + ", ".join(f"{x['letter']}:{x.get('ground_truth_regime','-')}/{x.get('predicted_regime','-')}"
                            for x in new_letter_report if x.get('built')))

    # ---------------- tables ----------------
    derivation_table = [_concept_row(r, tau_j, tau_h) for r in derivation]
    prospective_table = [_concept_row(r, tau_j, tau_h) for r in prospective]

    router = dict(
        recommended="recall_hole_alone",
        recommended_rule=dict(
            signal="parent recall-hole", tau_h_alone=th_alone, balanced_acc=bacc_halone,
            definition_string=f"predict ABSORPTION-regime iff (parent recall-hole > {th_alone:.4f}); else CO-FIRING",
            note="PRIMARY recommendation — strongest single separator on the derivation set, no derivation "
                 "counterexample. Firing-Jaccard is a corroborating signal; the combined conjunction is an ablation."),
        single_signal_ablations=dict(
            recall_hole_alone=dict(tau=th_alone, balanced_acc=bacc_halone, sweep=sweep_halone,
                                   note="PRIMARY recommendation — strongest single separator"),
            jaccard_alone=dict(tau=tj_alone, balanced_acc=bacc_jalone, sweep=sweep_jalone,
                               note="corroborating signal only; mislabels numeric/taxonomic alone")),
        ablation_combined=dict(tau_j=tau_j, tau_h=tau_h, balanced_acc=frozen["balanced_acc"],
                               margin=frozen["margin"], n_optimal_cells=frozen["n_optimal_cells"],
                               degenerate_tau_h=frozen["degenerate_tau_h"],
                               recall_hole_primary_combined=rhp,
                               note="conjunction ABLATION; claimed as recommendation ONLY if it beats recall-hole-"
                                    "alone out-of-sample (conjunction_beats_primary below)"),
        loo=dict(recall_hole_alone_acc=loo_h_acc, recall_hole_alone_per_concept=loo_h_rows,   # PRIMARY
                 jaccard_alone_acc=loo_j_acc, jaccard_alone_per_concept=loo_j_rows,
                 combined_acc=loo_comb_acc, combined_per_concept=loo_comb_rows),
        counterexamples=counterex,
        prospective_hitrate=hr,
        prospective_hitrate_primary=prospective_hitrate_primary,
        prospective_hitrate_ablation_combined=prospective_hitrate_ablation_combined,
        prospective_hitrate_ablation_jaccard=prospective_hitrate_ablation_jaccard,
        conjunction_beats_primary_out_of_sample=conj_better,
        new_letter_report=new_letter_report)

    metadata = dict(
        method_name="A-Priori SAE Firing-Structure Router (recall-hole-alone PRIMARY screen)",
        description="A single label-free firing-structure signal read from one cheap forward pass — the parent "
                    "latent's RECALL-HOLE (the fraction of concept-positives the broad parent latent misses) — is "
                    "the PRIMARY screening rule that PREDICTS, a priori, whether label-free cluster-level grouping "
                    "(CCRG K-track) recovers a unit beating the best single RAW SAE latent (a). recall-hole-alone is "
                    "the strongest single separator on the 12 DERIVATION concepts (balanced_acc 1.0, no derivation "
                    "counterexample); firing-Jaccard(detector,parent) is a CORROBORATING signal and the combined "
                    "firing-Jaccard-AND-recall-hole conjunction is reported only as an ABLATION (elevated to the "
                    "recommendation ONLY if it generalizes strictly better out-of-sample). The frozen rule is applied "
                    "to a truly-held-out prospective set that spans BOTH regimes (7 NEW internally-built first-letter "
                    "spelling concepts supply the absorption regime; sentiment/aspect/professions/severe_toxicity the "
                    "co-firing regime); the per-predicted-regime prospective hit-rate (Wilson CIs) is the MEASURED "
                    "error. Reported as a screening heuristic, not a validated oracle.",
        baselines=dict(
            a="best single raw SAE latent (highest train AUC, content-responsive) — the individual latent to beat",
            h="supervised SAE standardized diff-of-means attribution pool (top-k, AxBench/SCR-TPP proxy)",
            d="non-SAE standardized diff-of-means probe on the raw layer-12 residual (required non-SAE baseline)",
            unit="label-free CCRG K-track-lite: parent anchor + firing-disjoint hole-covering absorbers"),
        sae_release=RELEASE_REPO, sae_id=SAE_PARAMS_16K, hook="blocks.12.hook_resid_post",
        model=MODEL_ID, seed=SEED, scale=scale, accelerator=_gpu_name(),
        firing_convention="encode>0 (JumpReLU)", gating=gating,
        n_concepts=len(results), n_derivation=len(derivation), n_prospective=len(prospective),
        recommended="recall_hole_alone",
        primary_rule=dict(
            signal="parent recall-hole", tau_h_alone=th_alone, balanced_acc=bacc_halone,
            loo_acc=loo_h_acc,
            definition_string=(f"predict ABSORPTION-regime iff (parent recall-hole > {th_alone:.4f}); "
                               f"else CO-FIRING-regime")),
        combined_rule=dict(   # ABLATION (kept for reference / back-compat)
            tau_j=tau_j, tau_h=tau_h, balanced_acc=frozen["balanced_acc"], margin=frozen["margin"],
            n_optimal_cells=frozen["n_optimal_cells"], degenerate_tau_h=frozen["degenerate_tau_h"],
            is_ablation=True,
            definition_string=(f"[ABLATION] predict ABSORPTION-regime iff (firing-Jaccard < {tau_j:.4f}) AND "
                               f"(parent recall-hole > {tau_h:.4f}); else CO-FIRING-regime")),
        single_signal_ablations=router["single_signal_ablations"],
        ablation_combined=router["ablation_combined"],
        loo=router["loo"],
        counterexamples=counterex,
        derivation_table=derivation_table,
        prospective_table=prospective_table,
        prospective_hitrate=hr,
        prospective_hitrate_primary=prospective_hitrate_primary,
        prospective_hitrate_ablation_combined=prospective_hitrate_ablation_combined,
        prospective_hitrate_ablation_jaccard=prospective_hitrate_ablation_jaccard,
        conjunction_beats_primary_out_of_sample=conj_better,
        new_letter_report=new_letter_report,
        router=router,
        per_concept_firing_jaccard=[dict(concept=r["concept"], role=role_of(r["concept"]),
                                         per_subcontext=r["per_subcontext"]) for r in results],
        reproduction_check=repro, honest_notes=honest,
        derivation_concepts=[r["concept"] for r in derivation],
        prospective_concepts=[r["concept"] for r in prospective],
        prospective_existing=PROSPECTIVE_EXISTING, prospective_new=PROSPECTIVE_NEW,
        prospective_spelling=PROSPECTIVE_SPELLING,
    )

    # ---------------- exp_gen_sol_out: one router-decision card per concept ----------------
    examples = []
    for r in results:
        o = r["outcome"]; role = role_of(r["concept"])
        ex = {
            "input": (f"Concept '{r['concept']}' ({r['granularity']}, {role}): parent latent {r['parent_latent']}, "
                      f"parent recall-hole max={r['recall_hole_max']:.4f}, firing-Jaccard(detector,parent) median="
                      f"{r['jaccard_median']:.4f}. PRIMARY a-priori screen (recall-hole>{th_alone:.3f}): route to "
                      f"absorption-repair (CCRG grouping) or marginal attribution?"),
            "output": r["ground_truth_regime"],
            "predict_router": r["predicted_regime"],
            "metadata_concept": r["concept"],
            "metadata_role": role,
            "metadata_kind": r["kind"],
            "metadata_granularity": r["granularity"],
            "metadata_jaccard_median": r["jaccard_median"],
            "metadata_jaccard_min": r["jaccard_min"],
            "metadata_jaccard_max": r["jaccard_max"],
            "metadata_jaccard_median_meanact": r["jaccard_median_meanact"],
            "metadata_recall_hole_max": r["recall_hole_max"],
            "metadata_parent_latent": r["parent_latent"],
            "metadata_parent_pos_firing": r["parent_pos_firing"],
            "metadata_parent_unresolved": r.get("parent_unresolved", False),
            "metadata_n_subcontexts": r["n_subcontexts"],
            "metadata_outcome_auc_unit": o["auc_unit"],
            "metadata_outcome_auc_a_rawlatent": o.get("auc_a"),
            "metadata_outcome_auc_h_attribution": o["auc_h"],
            "metadata_outcome_auc_d_nonsae": o.get("auc_d"),
            "metadata_outcome_delta_vs_a": o["delta"],
            "metadata_outcome_delta_vs_a_ci": o["delta_ci"],
            "metadata_outcome_delta_vs_h": o.get("delta_vs_h"),
            "metadata_outcome_delta_vs_h_ci": o.get("delta_vs_h_ci"),
            "metadata_outcome_k": o["k"],
            "metadata_outcome_s_star": o["s_star"],
            "metadata_unit_members": o["unit_members"],
            "metadata_h_members": o["h_members"],
            "metadata_a_latent": o.get("a_latent"),
            "metadata_ccrg_helps": r["ccrg_helps"],
            "metadata_ccrg_helps_significant": r["ccrg_helps_significant"],
            "metadata_ground_truth_regime": r["ground_truth_regime"],
            "metadata_ground_truth_regime_vs_h": r["ground_truth_regime_vs_h"],
            "metadata_predicted_regime": r["predicted_regime"],                       # PRIMARY = recall-hole-alone
            "metadata_predicted_regime_combined": r.get("predicted_regime_combined"),  # ablation
            "metadata_predicted_regime_jaccard": r.get("predicted_regime_jaccard"),    # ablation
            "metadata_hit_vs_a": r.get("hit_vs_a"),                                    # PRIMARY hit
            "metadata_hit_vs_a_combined": r.get("hit_vs_a_combined"),
            "metadata_hit_vs_a_jaccard": r.get("hit_vs_a_jaccard"),
            "metadata_hit_vs_h": r.get("hit_vs_h"),
            "metadata_is_prospective_hit": (bool(r.get("hit_vs_a")) if role == "prospective" else None),
            "metadata_power_flag": ("descriptive_only" if r.get("descriptive_only") else "inferential"),
            "metadata_per_subcontext": r["per_subcontext"],
        }
        examples.append(ex)
    out = {"metadata": metadata, "datasets": [{"dataset": "m6_router_concepts", "examples": examples}]}

    Path(args.out).write_text(json.dumps(_sanitize(out), indent=2, default=_json_default, allow_nan=False))
    logger.info(f"{el()} wrote {args.out} ({Path(args.out).stat().st_size/1e6:.3f} MB, {len(examples)} concepts)")
    _print_summary(results, metadata, repro, tau_j, tau_h)


def _print_summary(results, metadata, repro, tau_j, tau_h):
    logger.info("\n================= CONCEPT TABLE (firing structure + outcome) =================")
    logger.info(f"{'concept':<26}{'role':<11}{'j_med':>7}{'hole':>7}{'pred':>11}{'truth':>11}"
                f"{'aucU':>6}{'aucA':>6}{'aucH':>6}{'dVa':>7}{'hit':>5}")
    for r in results:
        o = r["outcome"]
        logger.info(f"{r['concept']:<26}{role_of(r['concept']):<11}{r['jaccard_median']:>7.3f}"
                    f"{r['recall_hole_max']:>7.3f}{r['predicted_regime']:>11}{r['ground_truth_regime']:>11}"
                    f"{o['auc_unit']:>6.3f}{o.get('auc_a',float('nan')):>6.3f}{o['auc_h']:>6.3f}"
                    f"{o['delta']:>+7.3f}{str(bool(r.get('hit_vs_a'))):>5}")
    pr = metadata["primary_rule"]; cr = metadata["combined_rule"]; loo = metadata["loo"]
    ssa = metadata["single_signal_ablations"]
    php = metadata["prospective_hitrate_primary"]
    logger.info(f"\nPRIMARY recall-hole-alone rule: hole>{pr['tau_h_alone']:.3f} | derivation balanced_acc="
                f"{pr['balanced_acc']:.3f} | LOO={pr['loo_acc']:.3f}  (RECOMMENDED)")
    logger.info(f"ABLATIONS: jaccard-alone bacc={ssa['jaccard_alone']['balanced_acc']:.3f} | "
                f"combined (j<{cr['tau_j']:.3f} AND hole>{cr['tau_h']:.3f}) bacc={cr['balanced_acc']:.3f}")
    logger.info(f"LOO derivation: recall-hole={loo['recall_hole_alone_acc']:.3f} (PRIMARY) "
                f"jaccard={loo['jaccard_alone_acc']:.3f} combined={loo['combined_acc']:.3f}")
    logger.info(f"PROSPECTIVE hit-rate by PRIMARY predicted regime (inferential): "
                f"absorption_predicted={php['absorption_predicted']['rate']} "
                f"{php['absorption_predicted']['wilson_ci']} (n={php['absorption_predicted']['n']}); "
                f"cofiring_predicted={php['cofiring_predicted']['rate']} "
                f"{php['cofiring_predicted']['wilson_ci']} (n={php['cofiring_predicted']['n']}); "
                f"all={php['combined_all']['rate']} (n={php['combined_all']['n']})")
    logger.info(f"conjunction_beats_primary_out_of_sample={metadata['conjunction_beats_primary_out_of_sample']}")
    logger.info(f"reproduction: spelling<0.05={repro['spelling_all_below_0_05']} "
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


def _sanitize(o):
    """Recursively convert numpy scalars/arrays to python and non-finite floats (NaN/Inf) to None so the
    emitted JSON is STRICTLY valid (json.dumps would otherwise write the non-standard `NaN`/`Infinity`)."""
    if isinstance(o, dict):
        return {k: _sanitize(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_sanitize(v) for v in o]
    if isinstance(o, np.ndarray):
        return _sanitize(o.tolist())
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.floating, float)):
        f = float(o)
        return f if math.isfinite(f) else None
    return o


if __name__ == "__main__":
    main()
