#!/usr/bin/env python3
"""
experiment_iter2_dir2 : TOXICITY SAE-latent firing-structure (MAJOR-2) + C1 count-matched
classification + selection-criterion ordering on frozen Gemma Scope SAEs.

Two-Track Counterfactual Co-Response Grouping (CCRG) on gemma-scope-2b-pt-res-canonical
(layer_12/width_16k), encoding the ParaDetox + civil_comments toxicity family
(art_8QO7pl6Pd8UQ) through gemma-2-2b (unsloth mirror, eager attention for gemma-2 softcap).

Priority order (truncation-safe): (1) encode + firing-Jaccard + recall-holes + K-necessity
verdict [MAJOR-2, cheap+decisive, ALWAYS produced]; (2) two-track unit + C1 (unit vs raw
latent (a), co-activation (b), decoder-geometry (c), SCR/TPP raw-dir (h)); (3) selection
ordering (f)<(g)/(h)<unit + reweight slope; (4) admission + multiplicity + surface null.

Both K-confirm and K-refute outcomes are publishable; success is NOT staked on a K-track
absorber win on toxicity (that is the sibling first-letter experiment).
"""
from __future__ import annotations
import os, sys, json, gc, time, math, hashlib, argparse, resource
from pathlib import Path

HERE = Path(__file__).resolve().parent
os.environ.setdefault("HF_HOME", str(HERE / "hf_cache"))
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")

import numpy as np
from loguru import logger

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(str(HERE / "logs" / "run.log"), rotation="50 MB", level="DEBUG")

# ----------------------------------------------------------------------------- CONFIG
CONFIG = dict(
    release="gemma-scope-2b-pt-res-canonical",
    sae_id="layer_12/width_16k/canonical",
    model="unsloth/gemma-2-2b",
    tl_model_name="gemma-2-2b",
    hook="blocks.12.hook_resid_post",
    layer=12,
    d_model=2304,
    d_sae=16384,
    max_tok=128,
    batch=32,
    pool="max",                 # per-example firing = max over content tokens (SAEBench convention)
    seed=0,
    b_boot=10000,               # headline (toxicity) C1 gaps
    b_boot_aux=2000,            # sub-attributes, reweight slope, admission nulls
    n_min=150,
    tau_prec=0.7,               # per-latent content-response precision floor
    jaccard_max=0.10,           # firing-Jaccard ceiling for disjointness / K-track add
    gain_min=0.05,              # marginal hole-coverage gain floor
    beta=6,                     # WGCNA/DiffCoEx soft-threshold exponent
    n_shuffle=300,              # content-response shuffle null permutations
    b_ari=30,                   # bootstrap-ARI stability resamples
    leiden_gammas=[0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0],
    max_unit_size=40,           # human-auditable unit cap; ARI-stability alone collapses to 1 giant cluster
    c_track_node_cap=400,       # cap C-track nodes for tractability (keep g)
    scr_pool_sizes=[5, 10, 20, 50],
    scr_default_N=20,
    reweight_w=[1, 2, 4, 8],
    target_fpr=0.10,            # operating point for worst-sub-context recall
    infer_subs=["obscene", "threat", "insult", "identity_attack", "sexual_explicit"],
    disjoint_subs=["threat", "identity_attack"],
    desc_only=["severe_toxicity"],
    sub_order=["severe_toxicity", "obscene", "threat", "insult", "identity_attack", "sexual_explicit"],
    # label-Jaccard matrix copied verbatim from dataset data_summary.json (subcontext_jaccard_overlap@0.5)
    label_jaccard={
        "obscene": {"obscene": 1.0, "threat": 0.015, "insult": 0.245, "identity_attack": 0.012, "sexual_explicit": 0.185},
        "threat": {"obscene": 0.015, "threat": 1.0, "insult": 0.044, "identity_attack": 0.022, "sexual_explicit": 0.009},
        "insult": {"obscene": 0.245, "threat": 0.044, "insult": 1.0, "identity_attack": 0.125, "sexual_explicit": 0.1},
        "identity_attack": {"obscene": 0.012, "threat": 0.022, "insult": 0.125, "identity_attack": 1.0, "sexual_explicit": 0.017},
        "sexual_explicit": {"obscene": 0.185, "threat": 0.009, "insult": 0.1, "identity_attack": 0.017, "sexual_explicit": 1.0},
    },
)

SEED = CONFIG["seed"]
CACHE = HERE / "cache"
CACHE.mkdir(exist_ok=True)
(HERE / "logs").mkdir(exist_ok=True)


def set_seeds():
    import random
    random.seed(SEED)
    np.random.seed(SEED)
    try:
        import torch
        torch.manual_seed(SEED)
        torch.cuda.manual_seed_all(SEED)
    except Exception:
        pass


def set_mem_limits(ram_gb: float = 44.0):
    """Container limit is 56GB; cap virtual memory generously but fail before OOM-killing."""
    try:
        soft = int(ram_gb * 1024 ** 3)
        resource.setrlimit(resource.RLIMIT_AS, (soft * 3, soft * 3))
        logger.info(f"RLIMIT_AS set to {ram_gb*3:.0f}GB virtual")
    except (ValueError, OSError) as e:
        logger.warning(f"could not set RLIMIT_AS: {e}")


# ----------------------------------------------------------------------------- DATA
def load_family(data_path: Path):
    """Flatten datasets[*].examples and split by metadata_record_type."""
    logger.info(f"Loading toxicity family from {data_path}")
    obj = json.loads(data_path.read_text())
    content, surface, cls = [], [], []
    for ds in obj["datasets"]:
        for ex in ds["examples"]:
            rt = ex.get("metadata_record_type")
            if rt == "content_pair":
                on, off = ex.get("metadata_text_on"), ex.get("metadata_text_off")
                if on and off:
                    content.append(dict(id=ex["metadata_id"], on=on, off=off,
                                        origin=ex.get("metadata_origin_source"),
                                        fold=ex.get("metadata_fold")))
            elif rt == "surface_pair":
                x, xp = ex.get("input"), ex.get("metadata_text_paired")
                if x and xp:
                    surface.append(dict(id=ex["metadata_id"], x=x, xpar=xp,
                                        origin=ex.get("metadata_origin_source"),
                                        fold=ex.get("metadata_fold")))
            elif rt == "classification":
                sub = ex.get("metadata_subcontext_labels") or {}
                cls.append(dict(id=ex["metadata_id"], text=ex["input"],
                                y=int(ex.get("metadata_toxicity_label") or 0),
                                fold=ex.get("metadata_fold"),
                                sub={k: (int(v) if v is not None else 0) for k, v in sub.items()}))
    logger.info(f"content_pair={len(content)} surface_pair={len(surface)} classification={len(cls)}")
    return content, surface, cls


# ----------------------------------------------------------------------------- MODEL + SAE
class Encoder:
    """gemma-2-2b (HF unsloth mirror) + Gemma-Scope SAE, manual forward hook on layer 12 output.

    Validates the hook point via SAE reconstruction cosine and JumpReLU L0 sparsity.
    Pooling: per-example latent activation = max / mean over CONTENT tokens (real, non-BOS).
    """

    def __init__(self):
        import torch
        self.torch = torch
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._load()

    def _load(self):
        import torch
        from sae_lens import SAE
        logger.info(f"Loading SAE {CONFIG['release']} / {CONFIG['sae_id']}")
        ret = SAE.from_pretrained(CONFIG["release"], CONFIG["sae_id"], device=self.device)
        sae = ret[0] if isinstance(ret, tuple) else ret
        self.sae = sae.to(torch.float32).eval()
        hk = getattr(self.sae.cfg, "hook_name", None)
        logger.info(f"SAE hook_name={hk} normalize={getattr(self.sae.cfg,'normalize_activations',None)} "
                    f"W_dec={tuple(self.sae.W_dec.shape)}")
        assert tuple(self.sae.W_dec.shape) == (CONFIG["d_sae"], CONFIG["d_model"]), \
            f"unexpected W_dec {tuple(self.sae.W_dec.shape)}"
        if hk is not None and hk != CONFIG["hook"]:
            logger.warning(f"SAE cfg hook_name {hk} != configured {CONFIG['hook']} (using layer-{CONFIG['layer']} output)")

        from transformers import AutoModelForCausalLM, AutoTokenizer
        logger.info(f"Loading model {CONFIG['model']} (eager attn -> correct gemma-2 softcap)")
        self.tok = AutoTokenizer.from_pretrained(CONFIG["model"])
        self.tok.padding_side = "right"
        self.model = AutoModelForCausalLM.from_pretrained(
            CONFIG["model"], torch_dtype=torch.bfloat16, attn_implementation="eager",
        ).to(self.device).eval()
        self._captured = {}
        self._hook_handle = self.model.model.layers[CONFIG["layer"]].register_forward_hook(self._fwd_hook)
        logger.info(f"Model loaded: n_layers={self.model.config.num_hidden_layers} d={self.model.config.hidden_size}")

    def _fwd_hook(self, module, inp, out):
        self._captured["resid"] = (out[0] if isinstance(out, tuple) else out).detach()

    def validate(self, texts):
        import torch
        ids = self.tok(texts, return_tensors="pt", padding=True, truncation=True,
                       max_length=CONFIG["max_tok"]).to(self.device)
        with torch.no_grad():
            self.model(**ids)
            resid = self._captured["resid"].float()
            feats = self.sae.encode(resid)
            recon = self.sae.decode(feats)
        mask = ids["attention_mask"].bool()
        rh, rc = resid[mask], recon[mask]
        cos = torch.nn.functional.cosine_similarity(rh, rc, dim=-1)
        l0 = (feats > 0)[mask].float().sum(-1)
        info = dict(recon_cos_mean=float(cos.mean()), recon_cos_min=float(cos.min()),
                    l0_mean=float(l0.mean()), l0_median=float(l0.median()), l0_max=float(l0.max()))
        logger.info(f"VALIDATE recon_cos_mean={info['recon_cos_mean']:.4f} "
                    f"recon_cos_min={info['recon_cos_min']:.4f} L0 mean={info['l0_mean']:.1f} "
                    f"median={info['l0_median']:.0f} max={info['l0_max']:.0f}")
        return info

    def encode(self, texts, want_max=True, want_mean=True, want_resid=True, batch=None):
        """Return dict with float16 arrays: act_max[N,16384], act_mean[N,16384], resid_mean[N,2304]."""
        import torch
        bs = batch or CONFIG["batch"]
        N = len(texts)
        out = {}
        if want_max: out["act_max"] = np.zeros((N, CONFIG["d_sae"]), dtype=np.float16)
        if want_mean: out["act_mean"] = np.zeros((N, CONFIG["d_sae"]), dtype=np.float16)
        if want_resid: out["resid_mean"] = np.zeros((N, CONFIG["d_model"]), dtype=np.float16)
        t0 = time.time()
        for s in range(0, N, bs):
            chunk = [t if (t and t.strip()) else " " for t in texts[s:s + bs]]
            ids = self.tok(chunk, return_tensors="pt", padding=True, truncation=True,
                           max_length=CONFIG["max_tok"]).to(self.device)
            with torch.no_grad():
                self.model(**ids)
                resid = self._captured["resid"].float()        # [b,T,2304]
                feats = self.sae.encode(resid)                  # [b,T,16384] (JumpReLU post-threshold)
            mask = ids["attention_mask"].bool().clone()
            mask[:, 0] = False                                  # exclude BOS
            none_left = mask.sum(1) == 0
            if none_left.any():                                 # 1-token edge case: fall back to all real tokens
                am = ids["attention_mask"].bool()
                mask[none_left] = am[none_left]
            fm = mask.unsqueeze(-1)
            cnt = mask.sum(1, keepdim=True).clamp(min=1).float()
            if want_resid:
                rm = (resid * fm).sum(1) / cnt
                out["resid_mean"][s:s + bs] = rm.to(torch.float16).cpu().numpy()
            feats_m = feats.masked_fill(~fm, float("-inf"))
            if want_max:
                am_ = feats_m.max(dim=1).values
                am_ = torch.where(torch.isinf(am_), torch.zeros_like(am_), am_).clamp(min=0)
                out["act_max"][s:s + bs] = am_.to(torch.float16).cpu().numpy()
            if want_mean:
                feats_pos = feats.masked_fill(~fm, 0.0)
                mn = feats_pos.sum(1) / cnt
                out["act_mean"][s:s + bs] = mn.to(torch.float16).cpu().numpy()
            del resid, feats, feats_m
            if s % (bs * 50) == 0:
                torch.cuda.empty_cache()
                logger.debug(f"encoded {s+len(chunk)}/{N}")
        logger.info(f"encoded {N} texts in {time.time()-t0:.1f}s")
        return out

    @property
    def W_dec(self):
        return self.sae.W_dec.detach().float().cpu().numpy()  # [16384,2304]

    def free_model(self):
        import torch
        try:
            self._hook_handle.remove()
        except Exception:
            pass
        del self.model
        gc.collect()
        torch.cuda.empty_cache()


def _cfg_hash(extra=""):
    key = f"{CONFIG['release']}|{CONFIG['sae_id']}|{CONFIG['model']}|{CONFIG['max_tok']}|{extra}"
    return hashlib.md5(key.encode()).hexdigest()[:10]


def encode_group(enc, name, texts, arrays, force=False):
    """Encode a named group with disk caching keyed by (config, text-content-hash)."""
    h = hashlib.md5(("||".join(texts)).encode()).hexdigest()[:12]
    tag = f"{name}_{_cfg_hash()}_{h}_{len(texts)}"
    paths = {a: CACHE / f"{tag}_{a}.npy" for a in arrays}
    if not force and all(p.exists() for p in paths.values()):
        logger.info(f"[cache hit] {name} ({len(texts)} texts)")
        return {a: np.load(p, mmap_mode=None) for a, p in paths.items()}
    res = enc.encode(texts, want_max=("act_max" in arrays), want_mean=("act_mean" in arrays),
                     want_resid=("resid_mean" in arrays))
    out = {}
    for a in arrays:
        np.save(paths[a], res[a])
        out[a] = res[a]
    return out


# =============================================================================
# STATISTICS HELPERS
# =============================================================================
from scipy.stats import rankdata


def auc_1d(scores, y):
    """Tie-aware AUC (Mann-Whitney) for a 1-D score vector."""
    y = np.asarray(y).astype(bool)
    npos = int(y.sum()); nneg = int((~y).sum())
    if npos == 0 or nneg == 0:
        return float("nan")
    r = rankdata(scores)
    return float((r[y].sum() - npos * (npos + 1) / 2.0) / (npos * nneg))


def cols_auc(scores, y):
    """Tie-aware AUC per column. scores [m,K], y [m] -> [K]."""
    y = np.asarray(y).astype(bool)
    npos = int(y.sum()); nneg = int((~y).sum())
    if npos == 0 or nneg == 0:
        return np.full(scores.shape[1], np.nan)
    r = rankdata(scores, axis=0)
    s = r[y].sum(axis=0)
    return (s - npos * (npos + 1) / 2.0) / (npos * nneg)


def best_threshold_f1(scores, y):
    """Threshold (predict score>=thr) maximizing F1."""
    s = np.asarray(scores, dtype=np.float64); y = np.asarray(y).astype(int)
    if y.sum() == 0 or y.sum() == len(y):
        return float(np.median(s)), 0.0
    order = np.argsort(-s, kind="mergesort")
    ys = y[order]; ss = s[order]
    tp = np.cumsum(ys); fp = np.cumsum(1 - ys)
    P = int(y.sum())
    prec = tp / np.maximum(tp + fp, 1)
    rec = tp / P
    f1 = np.where(prec + rec > 0, 2 * prec * rec / (prec + rec + 1e-12), 0.0)
    i = int(np.argmax(f1))
    return float(ss[i]), float(f1[i])


def f1_score_simple(pred, y):
    pred = np.asarray(pred).astype(bool); y = np.asarray(y).astype(bool)
    tp = int((pred & y).sum()); fp = int((pred & ~y).sum()); fn = int((~pred & y).sum())
    return 2 * tp / max(2 * tp + fp + fn, 1)


def paired_bootstrap(score_u, score_m, pred_u, pred_m, y, B, rng):
    """Paired bootstrap over examples for AUC-diff and F1-diff (unit minus method)."""
    n = len(y)
    idx = rng.integers(0, n, size=(B, n), dtype=np.int64)
    pu = np.asarray(pred_u).astype(bool); pm = np.asarray(pred_m).astype(bool); yy = np.asarray(y).astype(bool)
    # F1 vectorized
    def f1_boot(pred):
        p = pred[idx]; yb = yy[idx]
        tp = (p & yb).sum(1).astype(np.float64)
        fp = (p & ~yb).sum(1).astype(np.float64)
        fn = (~p & yb).sum(1).astype(np.float64)
        return 2 * tp / np.maximum(2 * tp + fp + fn, 1)
    f1d = f1_boot(pu) - f1_boot(pm)
    # AUC loop (tie-aware), reusing the same resamples
    su = np.asarray(score_u, dtype=np.float64); sm = np.asarray(score_m, dtype=np.float64)
    aucd = np.empty(B)
    for b in range(B):
        ii = idx[b]; yb = yy[ii]
        aucd[b] = auc_1d(su[ii], yb) - auc_1d(sm[ii], yb)
    return dict(
        auc_diff_ci=[float(np.nanpercentile(aucd, 2.5)), float(np.nanpercentile(aucd, 97.5))],
        f1_diff_ci=[float(np.percentile(f1d, 2.5)), float(np.percentile(f1d, 97.5))],
        auc_diff_mean=float(np.nanmean(aucd)), f1_diff_mean=float(np.mean(f1d)),
    )


def mcnemar_p(pred_u, pred_m, y):
    from statsmodels.stats.contingency_tables import mcnemar
    cu = (np.asarray(pred_u).astype(bool) == np.asarray(y).astype(bool))
    cm = (np.asarray(pred_m).astype(bool) == np.asarray(y).astype(bool))
    b = int((cu & ~cm).sum()); c = int((~cu & cm).sum())
    a = int((cu & cm).sum()); d = int((~cu & ~cm).sum())
    table = [[a, b], [c, d]]
    try:
        res = mcnemar(table, exact=True)
        return float(res.pvalue), table
    except Exception:
        return float("nan"), table


def holm_adjust(pdict):
    from statsmodels.stats.multitest import multipletests
    keys = [k for k, v in pdict.items() if v is not None and not (isinstance(v, float) and math.isnan(v))]
    if not keys:
        return {}
    pv = [pdict[k] for k in keys]
    rej, padj, _, _ = multipletests(pv, method="holm")
    return {k: float(p) for k, p in zip(keys, padj)}


def boot_ci(vals, lo=2.5, hi=97.5):
    vals = np.asarray(vals, dtype=np.float64)
    vals = vals[~np.isnan(vals)]
    if len(vals) == 0:
        return [float("nan"), float("nan")]
    return [float(np.percentile(vals, lo)), float(np.percentile(vals, hi))]


def standardize_cols(X, mu, sd):
    return (X.astype(np.float32) - mu) / np.maximum(sd, 1e-6)


def maxpool_score(actmax_rows, members, mu, sd):
    """max over members of z-scored SAE codes."""
    if len(members) == 0:
        return np.zeros(actmax_rows.shape[0], dtype=np.float32)
    cols = actmax_rows[:, members].astype(np.float32)
    z = (cols - mu[members]) / np.maximum(sd[members], 1e-6)
    return z.max(axis=1)


# =============================================================================
# STAGE 3 : MAJOR-2 FIRING STRUCTURE
# =============================================================================
def stage3_firing_structure(arrs, cls, content, rng):
    log_stage("STAGE 3 : MAJOR-2 firing structure")
    cfg = CONFIG
    cls_y = np.array([c["y"] for c in cls], dtype=np.int8)
    subs = cfg["infer_subs"]
    cls_sub = {s: np.array([int(c["sub"].get(s, 0) or 0) for c in cls], dtype=np.int8) for s in cfg["sub_order"]}

    # --- 3a content-response on ParaDetox pairs ---
    on_mean = arrs["content_on"]["act_mean"].astype(np.float32)    # [P,16384]
    off_mean = arrs["content_off"]["act_mean"].astype(np.float32)
    on_max = arrs["content_on"]["act_max"]
    R = on_mean - off_mean                                          # response matrix
    P = R.shape[0]
    mean_r = R.mean(axis=0)                                         # [16384]
    # shuffle null: random sign flips per pair
    nperm = cfg["n_shuffle"]
    null_mean = np.empty((nperm, R.shape[1]), dtype=np.float32)
    for i in range(nperm):
        signs = rng.choice([-1.0, 1.0], size=P).astype(np.float32)
        null_mean[i] = (signs[:, None] * R).mean(axis=0)
    null95 = np.percentile(null_mean, 95, axis=0)                   # [16384]
    del null_mean
    content_responsive_mask = mean_r > null95
    # cover sets / precision / recall
    fires_on = (on_max > 0)                                         # [P,16384] bool
    responds = R > null95[None, :]                                  # response above null
    cover = responds & fires_on
    cov_count = cover.sum(axis=0).astype(np.float64)                # |C_l|
    fires_on_count = fires_on.sum(axis=0).astype(np.float64)
    precision = np.divide(cov_count, np.maximum(fires_on_count, 1))
    recall = cov_count / P
    cr_idx = np.where(content_responsive_mask & (precision >= cfg["tau_prec"]))[0]
    if len(cr_idx) == 0:  # degenerate fallback (smoke): relax precision
        cr_idx = np.where(content_responsive_mask)[0]
    if len(cr_idx) == 0:
        cr_idx = np.argsort(-recall)[:50]
    g = int(cr_idx[np.argmax(recall[cr_idx])])
    logger.info(f"content_responsive={int(content_responsive_mask.sum())} candidates(prec>=tau)={len(cr_idx)} "
                f"| general latent g={g} recall_pairs={recall[g]:.3f} precision={precision[g]:.3f}")

    # --- firing matrices on CLS ---
    cls_max = arrs["cls"]["act_max"]
    fires_cls = (cls_max > 0)                                       # [Ncls,16384] bool
    toxic_mask = cls_y == 1
    fires_g_cls = fires_cls[:, g]
    general_recall_toxic = float(fires_g_cls[toxic_mask].mean()) if toxic_mask.any() else float("nan")

    # CLS-derived general latent (robustness): standardized mean-diff toxic vs clean among AUC>0.5
    neg_mask = cls_y == 0
    g_cls = g
    if toxic_mask.sum() > 1 and neg_mask.sum() > 1:
        mu_t = cls_max[toxic_mask].astype(np.float32).mean(0)
        mu_c = cls_max[neg_mask].astype(np.float32).mean(0)
        sd_all = cls_max.astype(np.float32).std(0) + 1e-6
        d = (mu_t - mu_c) / sd_all
        g_cls = int(np.argmax(d))
    general_recall_toxic_cls = float(fires_cls[:, g_cls][toxic_mask].mean()) if toxic_mask.any() else float("nan")

    # --- 3b per-sub-attribute detectors ---
    detectors = {}
    for s in subs:
        pos = cls_sub[s] == 1
        neg = cls_y == 0
        sub_rows = np.where(pos | neg)[0]
        if pos.sum() < 2 or neg.sum() < 2:
            detectors[s] = dict(idx=g, auc=float("nan"), mean_act=float("nan"), n_pos=int(pos.sum()), note="too_few")
            continue
        sc = cls_max[sub_rows].astype(np.float32)
        ylab = pos[sub_rows].astype(int)
        aucs = cols_auc(sc, ylab)
        mean_pos = cls_max[pos].astype(np.float32).mean(0)
        # PRIMARY detector = best single-latent detector for s (highest AUC vs clean negatives).
        # The argmax-mean-activation variant (plan's literal spec) is confounded by base firing
        # rate and yields near-chance latents; we additionally report it for completeness.
        det = int(np.nanargmax(aucs))
        top5 = np.argsort(-np.nan_to_num(aucs))[:5].tolist()
        cand = np.where(aucs > 0.5)[0]
        det_mean = int(cand[np.argmax(mean_pos[cand])]) if len(cand) > 0 else det
        detectors[s] = dict(idx=det, auc=float(aucs[det]), mean_act=float(mean_pos[det]),
                            top5_by_auc=top5, det_meanact_idx=det_mean,
                            det_meanact_auc=float(aucs[det_mean]), n_pos=int(pos.sum()))
    for s in subs:
        logger.info(f"  detector[{s}] idx={detectors[s]['idx']} auc={detectors[s]['auc']:.3f} "
                    f"meanact_idx={detectors[s]['det_meanact_idx']} n_pos={detectors[s]['n_pos']}")

    # --- 3c firing-Jaccard over U = {g} + detectors ---
    U = [("general", g)] + [(s, detectors[s]["idx"]) for s in subs]
    names = [u[0] for u in U]
    idxs = [u[1] for u in U]
    def jaccard_matrix(rows_mask):
        F = fires_cls[rows_mask][:, idxs]  # [m, |U|] bool
        m = F.shape[1]
        J = np.eye(m)
        for i in range(m):
            for j in range(i + 1, m):
                inter = int((F[:, i] & F[:, j]).sum())
                union = int((F[:, i] | F[:, j]).sum())
                J[i, j] = J[j, i] = (inter / union) if union > 0 else 0.0
        return J
    J_all = jaccard_matrix(np.ones(fires_cls.shape[0], dtype=bool))
    J_tox = jaccard_matrix(toxic_mask) if toxic_mask.sum() > 1 else J_all
    # bootstrap CI for general-vs-detector jaccard (toxic rows)
    jac_cis = {}
    tox_rows = np.where(toxic_mask)[0]
    Bj = cfg["b_boot_aux"]
    if len(tox_rows) > 5:
        Fg = fires_cls[tox_rows][:, g]
        for s in subs:
            Fd = fires_cls[tox_rows][:, detectors[s]["idx"]]
            vals = np.empty(Bj)
            for b in range(Bj):
                ii = rng.integers(0, len(tox_rows), len(tox_rows))
                a = Fg[ii]; d2 = Fd[ii]
                u = int((a | d2).sum())
                vals[b] = (int((a & d2).sum()) / u) if u > 0 else 0.0
            jac_cis[s] = boot_ci(vals)

    # --- 3d recall holes per sub ---
    recall_holes = {}
    for s in subs:
        pos = cls_sub[s] == 1
        if pos.sum() < 1:
            recall_holes[s] = dict(recall=float("nan"), hole=float("nan"), ci=[float("nan")] * 2, n_pos=0)
            continue
        rg = fires_cls[:, g][pos]
        rec = float(rg.mean())
        vals = np.array([rg[rng.integers(0, len(rg), len(rg))].mean() for _ in range(cfg["b_boot_aux"])])
        recall_holes[s] = dict(recall=rec, hole=float(1 - rec), ci=boot_ci(vals),
                               n_pos=int(pos.sum()))

    # --- 3e K-necessity verdict ---
    cover_frac = {}
    for s in subs:
        pos = cls_sub[s] == 1
        silent = pos & (~fires_cls[:, g])
        det = detectors[s]["idx"]
        cover_frac[s] = float(fires_cls[:, det][silent].mean()) if silent.sum() > 0 else 0.0
    # decision over disjoint subs
    confirms = []
    for s in cfg["disjoint_subs"]:
        hole = recall_holes[s]["hole"]
        cf = cover_frac[s]
        jac = float(J_tox[0, names.index(s)])
        cond = (hole is not None and hole > 0.3) and (cf >= 0.3) and (jac < cfg["jaccard_max"])
        confirms.append((s, cond, hole, cf, jac))
    n_conf = sum(1 for _, c, *_ in confirms if c)
    if n_conf == len(cfg["disjoint_subs"]):
        verdict = "CONFIRMED"
    elif n_conf == 0:
        verdict = "REFUTED"
    else:
        verdict = "MIXED"
    rationale = build_verdict_rationale(verdict, confirms, general_recall_toxic, recall_holes, J_tox, names, cfg)
    logger.info(f"K-NECESSITY VERDICT = {verdict} (general toxic recall={general_recall_toxic:.3f})")

    fs = dict(
        n_pairs=int(P), n_cls=int(len(cls)),
        general_latent_idx=g, general_recall_pairs=float(recall[g]), general_precision_pairs=float(precision[g]),
        general_recall_toxic=general_recall_toxic,
        general_latent_idx_cls_derived=g_cls, general_recall_toxic_cls_derived=general_recall_toxic_cls,
        n_content_responsive=int(content_responsive_mask.sum()), n_candidates=int(len(cr_idx)),
        detector_idx_per_sub={s: detectors[s]["idx"] for s in subs},
        detector_auc_per_sub={s: detectors[s]["auc"] for s in subs},
        detector_top5_by_auc_per_sub={s: detectors[s].get("top5_by_auc", []) for s in subs},
        detector_meanact_idx_per_sub={s: detectors[s].get("det_meanact_idx") for s in subs},
        detector_meanact_auc_per_sub={s: detectors[s].get("det_meanact_auc") for s in subs},
        firing_jaccard_labels=names,
        firing_jaccard_matrix_all=np.round(J_all, 4).tolist(),
        firing_jaccard_matrix_toxiconly=np.round(J_tox, 4).tolist(),
        jaccard_general_vs_detector_ci=jac_cis,
        recall_holes_per_sub=recall_holes,
        cover_frac_detector_over_g_holes_per_sub=cover_frac,
        label_jaccard_matrix=cfg["label_jaccard"],
        k_necessity_verdict=verdict,
        k_necessity_rationale=rationale,
    )
    state = dict(R=R, cr_idx=cr_idx, g=g, cover=cover, cov_count=cov_count, precision=precision,
                 recall=recall, fires_cls=fires_cls, cls_y=cls_y, cls_sub=cls_sub,
                 toxic_mask=toxic_mask, detectors=detectors, null95=null95)
    del on_mean, off_mean
    gc.collect()
    return fs, state


def build_verdict_rationale(verdict, confirms, grt, holes, J_tox, names, cfg):
    parts = []
    gi = names.index("general") if "general" in names else 0
    if verdict == "REFUTED":
        parts.append(f"K-track premise REFUTED on toxicity: the general latent g fires on {grt:.0%} of toxic "
                     f"comments and its per-sub-context recall holes are small")
    elif verdict == "CONFIRMED":
        parts.append(f"K-track premise CONFIRMED on toxicity: disjoint sub-attributes are carried by detector "
                     f"latents firing on g's recall holes while remaining firing-disjoint from g")
    else:
        parts.append("K-track premise MIXED on toxicity")
    for s, cond, hole, cf, jac in confirms:
        parts.append(f"[{s}] hole={hole:.2f} detector-covers-g-holes={cf:.2f} firing-Jaccard(g,det)={jac:.3f} "
                     f"=> {'absorption-like' if cond else 'not absorption-like'}")
    # SAE firing vs label structure
    lj = cfg["label_jaccard"]
    io_lab = lj["obscene"]["insult"]
    io_fire = float(J_tox[names.index("obscene"), names.index("insult")]) if "obscene" in names and "insult" in names else float("nan")
    parts.append(f"Label-Jaccard insult-obscene={io_lab:.3f} (shared-support) vs SAE-firing-Jaccard(obscene-detector,"
                 f"insult-detector)={io_fire:.3f}; threat/identity_attack labels are <0.05-disjoint. "
                 f"SAE firing structure {'MIRRORS' if abs(io_fire-io_lab)<0.15 else 'DEPARTS from'} the label co-occurrence structure.")
    return " ".join(parts)


def log_stage(msg):
    logger.info("=" * 70)
    logger.info(msg)
    logger.info("=" * 70)


# =============================================================================
# STAGE 4 : TWO-TRACK UNIT CONSTRUCTION
# =============================================================================
def _affinity_from_ranks(Rc):
    ranks = rankdata(Rc, axis=0)
    corr = np.corrcoef(ranks, rowvar=False)
    corr = np.nan_to_num(corr)
    A = np.power(np.clip(corr, 0.0, None), CONFIG["beta"]).astype(np.float64)
    np.fill_diagonal(A, 0.0)
    return A, corr


def leiden_or_fallback(A, gamma):
    n = A.shape[0]
    if n <= 1:
        return np.zeros(n, dtype=int)
    try:
        import igraph as ig
        import leidenalg as la
        iu, ju = np.triu_indices(n, k=1)
        w = A[iu, ju]
        keep = w > 1e-9
        edges = list(zip(iu[keep].tolist(), ju[keep].tolist()))
        graph = ig.Graph(n=n, edges=edges)
        graph.es["weight"] = w[keep].tolist()
        if len(edges) == 0:
            return np.arange(n)
        part = la.find_partition(graph, la.RBConfigurationVertexPartition,
                                 weights="weight", resolution_parameter=gamma, seed=SEED)
        return np.array(part.membership)
    except Exception as e:
        logger.warning(f"leidenalg unavailable ({e}); using networkx greedy modularity fallback")
        import networkx as nx
        G = nx.Graph()
        G.add_nodes_from(range(n))
        iu, ju = np.triu_indices(n, k=1)
        for i, j in zip(iu, ju):
            if A[i, j] > 1e-9:
                G.add_edge(int(i), int(j), weight=float(A[i, j]))
        comms = nx.algorithms.community.greedy_modularity_communities(G, weight="weight")
        memb = np.zeros(n, dtype=int)
        for ci, c in enumerate(comms):
            for v in c:
                memb[v] = ci
        return memb


def bootstrap_ari(Rc, gamma, base_memb, rng, b_ari):
    from sklearn.metrics import adjusted_rand_score
    P = Rc.shape[0]
    aris = []
    for _ in range(b_ari):
        ii = rng.integers(0, P, P)
        A2, _ = _affinity_from_ranks(Rc[ii])
        m2 = leiden_or_fallback(A2, gamma)
        aris.append(adjusted_rand_score(base_memb, m2))
    # null: column-shuffled (structure destroyed)
    nulls = []
    for _ in range(max(5, b_ari // 3)):
        Rs = np.column_stack([Rc[rng.permutation(P), j] for j in range(Rc.shape[1])])
        A3, _ = _affinity_from_ranks(Rs)
        m3 = leiden_or_fallback(A3, gamma)
        nulls.append(adjusted_rand_score(base_memb, m3))
    return float(np.mean(aris)), boot_ci(aris), float(np.mean(nulls))


def stage4_two_track(state, rng):
    log_stage("STAGE 4 : two-track unit construction")
    cfg = CONFIG
    R = state["R"]; cr = state["cr_idx"]; g = state["g"]
    # cap C-track node set for tractability (keep g)
    cap = cfg["c_track_node_cap"]
    if len(cr) > cap:
        order = np.argsort(-state["recall"][cr])[:cap]
        cr_c = cr[order]
        if g not in cr_c:
            cr_c = np.append(cr_c, g)
    else:
        cr_c = cr
    Rc = R[:, cr_c].astype(np.float32)
    A, corr = _affinity_from_ranks(Rc)
    g_pos = int(np.where(cr_c == g)[0][0])
    # tune gamma by bootstrap-ARI stability, but constrain to a NON-TRIVIAL, human-auditable unit:
    # ARI-stability alone is maximised by the degenerate single-giant-cluster partition, so we
    # select the most stable gamma whose g-community is non-trivial (2..max_unit_size).
    cands = []
    for gamma in cfg["leiden_gammas"]:
        memb = leiden_or_fallback(A, gamma)
        ncomm = len(set(memb.tolist()))
        gsize = int((memb == memb[g_pos]).sum())
        ari_mean, ari_ci, null = bootstrap_ari(Rc, gamma, memb, rng, cfg["b_ari"])
        cands.append(dict(gamma=gamma, memb=memb, ncomm=ncomm, gsize=gsize,
                          ari_mean=ari_mean, ari_ci=ari_ci, null=null, score=ari_mean - null))
        logger.info(f"  gamma={gamma} ncomm={ncomm} g_comm_size={gsize} ARI={ari_mean:.3f} null={null:.3f}")
    MAXU = cfg["max_unit_size"]
    valid = [c for c in cands if c["ncomm"] > 1 and 2 <= c["gsize"] <= MAXU and c["score"] > 0.05]
    if valid:
        best = max(valid, key=lambda c: c["score"])
    else:
        nz = [c for c in cands if c["gsize"] >= 2]
        best = min(nz, key=lambda c: c["gsize"]) if nz else cands[-1]
    memb = best["memb"]
    c_community_local = np.where(memb == memb[g_pos])[0]
    unit_C = [int(cr_c[i]) for i in c_community_local]
    logger.info(f"  C-track community of g: {len(unit_C)} latents (gamma={best['gamma']}, "
                f"ncomm={best['ncomm']}, ARI={best['ari_mean']:.3f})")

    # K-track anchored greedy max-coverage
    added, unit_members = k_track(state, unit_C, rng)
    unit_members = sorted(set(unit_members))
    k = len(unit_members)
    track = "C" if not added else ("hybrid" if unit_C else "K")
    logger.info(f"  K-track added {len(added)} absorbers; final unit k={k} track={track}")

    # candidate units (for admission): non-singleton C-communities (capped to 30 largest) + K-cover
    comm_sizes = [(cid, int((memb == cid).sum())) for cid in set(memb.tolist())]
    comm_sizes = sorted([c for c in comm_sizes if c[1] >= 2], key=lambda x: -x[1])[:30]
    candidate_units = []
    for cid, _ in comm_sizes:
        local = np.where(memb == cid)[0]
        candidate_units.append(dict(name=f"C{cid}", members=[int(cr_c[i]) for i in local], track="C"))
    candidate_units.append(dict(name="Kcover", members=sorted(set([g] + [a[0] for a in added])), track="K"))

    unit = dict(
        members=unit_members, k=int(k), track=track, anchor=int(g),
        c_track_members=unit_C, k_track_added=[dict(idx=int(l), gain=float(gn)) for l, gn in added],
        pooling="max", gamma=float(best["gamma"]),
    )
    stability = dict(gamma=float(best["gamma"]), ncomm=int(best["ncomm"]),
                     bootstrap_ari_mean=float(best["ari_mean"]), bootstrap_ari_ci=best["ari_ci"],
                     shuffle_null_ari=float(best["null"]),
                     gamma_sweep=[dict(gamma=float(c["gamma"]), ncomm=int(c["ncomm"]),
                                       g_comm_size=int(c["gsize"]), ari_mean=float(c["ari_mean"]),
                                       null=float(c["null"])) for c in cands],
                     selection_rule="max bootstrap-ARI among non-trivial partitions with "
                                    "2<=g_community_size<=max_unit_size (ARI-stability alone "
                                    "collapses to one giant cluster)")
    state["unit_members"] = unit_members
    state["candidate_units"] = candidate_units
    state["c_community"] = unit_C
    return unit, stability, candidate_units


def _max_jaccard(fires, l, members):
    if not members:
        return 0.0
    a = fires[:, l]
    best = 0.0
    asum = int(a.sum())
    for m in members:
        bcol = fires[:, m]
        inter = int((a & bcol).sum())
        union = asum + int(bcol.sum()) - inter
        j = (inter / union) if union > 0 else 0.0
        best = max(best, j)
    return best


def k_track(state, unit_C, rng):
    cfg = CONFIG
    cover = state["cover"]; g = state["g"]; prec = state["precision"]
    fires_cls = state["fires_cls"]
    P = cover.shape[0]
    members = list(dict.fromkeys([g] + list(unit_C)))
    # holes = pairs not covered by ANY current member
    holes = ~cover[:, members].any(axis=1)
    added = []
    elig = (prec >= cfg["tau_prec"])
    for _ in range(20):
        if holes.sum() == 0:
            break
        gain_all = (cover & holes[:, None]).sum(0).astype(np.float64) / P
        gain_all[~elig] = -1.0
        gain_all[members] = -1.0
        order = np.argsort(-gain_all)
        chosen = -1
        for l in order[:50]:
            if gain_all[l] < cfg["gain_min"]:
                break
            if _max_jaccard(fires_cls, int(l), members) >= cfg["jaccard_max"]:
                continue
            # bootstrap CI of marginal gain excludes 0
            cl_h = cover[:, l] & holes
            vals = np.array([cl_h[rng.integers(0, P, P)].mean() for _ in range(cfg["b_boot_aux"] // 4)])
            if boot_ci(vals)[0] <= 0:
                continue
            chosen = int(l)
            break
        if chosen < 0:
            break
        members.append(chosen)
        added.append((chosen, float(gain_all[chosen])))
        holes = holes & ~cover[:, chosen]
    return added, members


# =============================================================================
# STAGE 5 : C1 COUNT-MATCHED CLASSIFICATION
# =============================================================================
def _attribution(actmax, train_mask, y_target, mu, sd):
    """Signed standardized mean-activation difference (SCR/TPP max-mean-difference reimpl)."""
    pos = train_mask & (y_target == 1)
    neg = train_mask & (y_target == 0)
    if pos.sum() < 1 or neg.sum() < 1:
        return np.zeros(actmax.shape[1])
    mp = actmax[pos].astype(np.float32).mean(0)
    mn = actmax[neg].astype(np.float32).mean(0)
    return (mp - mn) / np.maximum(sd, 1e-6)


def _proj_scores(resid, idxs, W_dec, train_mask):
    """Raw decoder-direction projections, standardized per direction by train stats, max-pooled."""
    if len(idxs) == 0:
        return np.zeros(resid.shape[0], dtype=np.float32)
    D = W_dec[idxs].astype(np.float32)          # [k,d]
    proj = resid.astype(np.float32) @ D.T        # [N,k]
    mu = proj[train_mask].mean(0); sd = proj[train_mask].std(0) + 1e-6
    z = (proj - mu) / sd
    return z.max(axis=1)


def _feat_sae(cls_max, members):
    if len(members) == 0:
        return np.zeros((cls_max.shape[0], 1), np.float32)
    return cls_max[:, members].astype(np.float32)


def _feat_dir(cls_resid, idxs, W_dec):
    if len(idxs) == 0:
        return np.zeros((cls_resid.shape[0], 1), np.float32)
    return cls_resid.astype(np.float32) @ W_dec[idxs].astype(np.float32).T


def lr_feature_score(feat, train_mask, y_t):
    """PRIMARY C1 classifier: L2 logistic regression on standardized selected features.
    Held constant across methods so only the feature SELECTION differs (feature-based classification)."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    Xtr = feat[train_mask]; ytr = y_t[train_mask]
    if feat.shape[1] == 0 or len(set(ytr.tolist())) < 2:
        return np.zeros(feat.shape[0], np.float32)
    scaler = StandardScaler().fit(Xtr)
    clf = LogisticRegression(max_iter=500, C=1.0).fit(scaler.transform(Xtr), ytr)
    return clf.decision_function(scaler.transform(feat))


def stage5_c1(state, arrs, W_dec, folds, rng):
    log_stage("STAGE 5 : C1 count-matched classification")
    cfg = CONFIG
    cls_max = arrs["cls"]["act_max"]
    cls_resid = arrs["cls"]["resid_mean"]
    cls_y = state["cls_y"]; cls_sub = state["cls_sub"]
    g = state["g"]; unit_members = state["unit_members"]; k = max(1, len(unit_members))
    tr, va, te = folds["train"], folds["val"], folds["test"]
    mu = cls_max[tr].astype(np.float32).mean(0)
    sd = cls_max[tr].astype(np.float32).std(0) + 1e-6
    fires_tr = (cls_max[tr] > 0)

    # toxicity-anchored neighbor sets (b),(c) — fixed across targets
    a_g = fires_tr[:, g]
    inter = fires_tr[a_g].sum(0).astype(np.float64)
    union = int(a_g.sum()) + fires_tr.sum(0).astype(np.float64) - inter
    cofire = np.divide(inter, np.maximum(union, 1))
    cofire[g] = -1
    b_members = [g] + np.argsort(-cofire)[:k - 1].tolist()
    Wn = W_dec / (np.linalg.norm(W_dec, axis=1, keepdims=True) + 1e-8)
    dcos = Wn @ Wn[g]
    dcos[g] = -1
    c_members = [g] + np.argsort(-dcos)[:k - 1].tolist()
    logger.info(f"k={k} | (b) co-firing members={b_members[:6]}... (c) decoder-cos members={c_members[:6]}...")

    targets = ["toxicity"] + cfg["infer_subs"]
    results = {}
    tox_preds = {}  # for predictions dataset
    for t in targets:
        if t == "toxicity":
            elig = np.ones(len(cls_y), dtype=bool)
            y_t = cls_y.astype(int)
        else:
            pos = cls_sub[t] == 1
            neg = cls_y == 0
            elig = pos | neg
            y_t = pos.astype(int)
        tr_e = tr & elig; va_e = va & elig; te_e = te & elig
        if (y_t[te_e].sum() < 5) or (y_t[te_e].sum() == te_e.sum()) or (y_t[va_e].sum() < 2):
            results[t] = dict(note="insufficient_positives", n_test_pos=int(y_t[te_e].sum()))
            continue
        attr = _attribution(cls_max, tr_e, y_t, mu, sd)
        g_members = np.argsort(-attr)[:cfg["scr_default_N"]].tolist()
        h_idx = np.argsort(-attr)[:k].tolist()
        # best single latent (a) by val AUC
        va_auc = cols_auc(cls_max[va_e].astype(np.float32), y_t[va_e])
        a_idx = int(np.nanargmax(va_auc))

        # PRIMARY scoring: logistic regression on each method's selected features (same classifier,
        # different SELECTION). SAE-code methods use member act_max columns; (h)/unit_rawdir use raw
        # decoder-direction projections; (d)/(e) are non-SAE residual baselines.
        feat_map = {
            "unit": _feat_sae(cls_max, unit_members),
            "a": _feat_sae(cls_max, [a_idx]),
            "b": _feat_sae(cls_max, b_members),
            "c": _feat_sae(cls_max, c_members),
            "g": _feat_sae(cls_max, g_members),
            "h": _feat_dir(cls_resid, h_idx, W_dec),
            "unit_rawdir": _feat_dir(cls_resid, unit_members, W_dec),
        }
        method_scores = {n: lr_feature_score(f, tr_e, y_t) for n, f in feat_map.items()}
        method_scores["d"] = _diff_of_means(cls_resid, tr_e, y_t)
        method_scores["e"] = _lr_resid(cls_resid, tr_e, y_t)
        # SECONDARY (descriptive): parameter-free max-pool of z-scored SAE codes
        mp_members = dict(unit=unit_members, a=[a_idx], b=b_members, c=c_members, g=g_members)
        mp_auc = {n: auc_1d(maxpool_score(cls_max, m, mu, sd)[te_e], y_t[te_e]) for n, m in mp_members.items()}

        per_method = {}
        thr = {}
        preds_te = {}
        for name, sc in method_scores.items():
            t_thr, _ = best_threshold_f1(sc[va_e], y_t[va_e])
            thr[name] = t_thr
            pte = sc[te_e] >= t_thr
            preds_te[name] = pte
            per_method[name] = dict(
                auc=auc_1d(sc[te_e], y_t[te_e]),
                f1=f1_score_simple(pte, y_t[te_e]),
                auc_maxpoolz=mp_auc.get(name),
                k=(len(unit_members) if name in ("unit", "unit_rawdir") else
                   1 if name == "a" else len(g_members) if name == "g" else
                   k if name in ("b", "c", "h") else None),
            )
        # paired bootstrap unit vs each + McNemar
        B = cfg["b_boot"] if t == "toxicity" else cfg["b_boot_aux"]
        comps = {}
        su = method_scores["unit"][te_e]; pu = preds_te["unit"]; yte = y_t[te_e]
        for name in ["a", "b", "c", "g", "h", "d", "e", "unit_rawdir"]:
            bs = paired_bootstrap(su, method_scores[name][te_e], pu, preds_te[name], yte, B, rng)
            mp, table = mcnemar_p(pu, preds_te[name], yte)
            comps[name] = dict(**bs, mcnemar_p=mp, mcnemar_table=table)
        results[t] = dict(n_test=int(te_e.sum()), n_test_pos=int(yte.sum()),
                          per_method=per_method, unit_minus=comps,
                          selected_idx=dict(a=a_idx, g=g_members[:10], h=h_idx[:10]))
        logger.info(f"  [{t}] n_test={int(te_e.sum())} unit AUC={per_method['unit']['auc']:.3f} "
                    f"a={per_method['a']['auc']:.3f} b={per_method['b']['auc']:.3f} "
                    f"c={per_method['c']['auc']:.3f} h={per_method['h']['auc']:.3f}")
        if t == "toxicity":
            tox_preds = {name: preds_te[name] for name in ["unit", "a", "b", "c", "h", "d", "e"]}
            tox_preds["_rows"] = np.where(te_e)[0]

    # Holm across targets for the unit-vs-(h) gap (primary selection contrast) and unit-vs-(b)
    for comp_key in ["h", "b", "c", "a"]:
        pdict = {t: results[t]["unit_minus"][comp_key]["mcnemar_p"]
                 for t in targets if "unit_minus" in results.get(t, {})}
        adj = holm_adjust(pdict)
        for t, p in adj.items():
            results[t]["unit_minus"][comp_key]["mcnemar_p_holm"] = p

    return results, dict(b_members=b_members, c_members=c_members, k=k), tox_preds


def _diff_of_means(resid, train_mask, y_t):
    pos = train_mask & (y_t == 1); neg = train_mask & (y_t == 0)
    if pos.sum() < 1 or neg.sum() < 1:
        return np.zeros(resid.shape[0], dtype=np.float32)
    d = resid[pos].astype(np.float32).mean(0) - resid[neg].astype(np.float32).mean(0)
    d = d / (np.linalg.norm(d) + 1e-8)
    return resid.astype(np.float32) @ d


def _lr_resid(resid, train_mask, y_t):
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    Xtr = resid[train_mask].astype(np.float32); ytr = y_t[train_mask]
    if len(set(ytr.tolist())) < 2:
        return np.zeros(resid.shape[0], dtype=np.float32)
    sc = StandardScaler().fit(Xtr)
    clf = LogisticRegression(max_iter=500, C=1.0).fit(sc.transform(Xtr), ytr)
    return clf.decision_function(sc.transform(resid.astype(np.float32)))


# =============================================================================
# STAGE 6 : SELECTION-CRITERION ORDERING + REWEIGHT SLOPE
# =============================================================================
def fit_leace_probe(on_r, off_r, sx_r, sxp_r, cls_r):
    import torch
    from sklearn.linear_model import LogisticRegression
    Xtr = np.concatenate([on_r, off_r], 0).astype(np.float32)
    ytr = np.concatenate([np.ones(len(on_r)), np.zeros(len(off_r))]).astype(int)
    surf_delta = (sx_r.astype(np.float32) - sxp_r.astype(np.float32))
    r = int(min(10, max(1, surf_delta.shape[0] - 1), surf_delta.shape[1]))
    sd = surf_delta - surf_delta.mean(0, keepdims=True)
    try:
        _, _, Vt = np.linalg.svd(sd, full_matrices=False)
        B = Vt[:r].T.astype(np.float32)                    # [d,r] surface subspace basis
    except np.linalg.LinAlgError:
        B = np.zeros((Xtr.shape[1], 1), np.float32)
    used = "leace"
    try:
        from concept_erasure import LeaceEraser
        Z = (Xtr @ B).astype(np.float32)
        er = LeaceEraser.fit(torch.from_numpy(Xtr), torch.from_numpy(Z))
        Xc = er(torch.from_numpy(Xtr)).numpy()
        cls_c = er(torch.from_numpy(cls_r.astype(np.float32))).numpy()
    except Exception as e:
        logger.warning(f"concept_erasure failed ({e}); projection-erasure fallback")
        used = "projection"
        Xc = Xtr - (Xtr @ B) @ B.T
        cls_c = cls_r.astype(np.float32) - (cls_r.astype(np.float32) @ B) @ B.T
    clf = LogisticRegression(max_iter=1000, C=1.0).fit(Xc, ytr)
    return clf.decision_function(cls_c.astype(np.float32)), used, r


def _worst_subctx_recall(score, val_neg_mask, cls_sub, te_mask, subs, fpr, rng=None, B=0):
    thr = float(np.quantile(score[val_neg_mask], 1 - fpr)) if val_neg_mask.sum() > 0 else 0.0
    per = {}
    for s in subs:
        pos = te_mask & (cls_sub[s] == 1)
        per[s] = float((score[pos] >= thr).mean()) if pos.sum() > 0 else float("nan")
    vals = [per[s] for s in subs if not math.isnan(per[s])]
    worst = float(np.min(vals)) if vals else float("nan")
    ci = [float("nan"), float("nan")]
    if B and rng is not None:
        te_rows = np.where(te_mask)[0]
        boot = []
        for _ in range(B):
            ridx = te_rows[rng.integers(0, len(te_rows), len(te_rows))]
            ws = []
            for s in subs:
                p = ridx[cls_sub[s][ridx] == 1]
                if len(p) > 0:
                    ws.append((score[p] >= thr).mean())
            if ws:
                boot.append(min(ws))
        ci = boot_ci(boot)
    return worst, per, thr, ci


def stage6_selection(state, arrs, W_dec, folds, rng):
    log_stage("STAGE 6 : selection-criterion ordering + reweight slope")
    cfg = CONFIG
    cls_max = arrs["cls"]["act_max"]; cls_resid = arrs["cls"]["resid_mean"]
    cls_y = state["cls_y"]; cls_sub = state["cls_sub"]
    g = state["g"]; unit_members = state["unit_members"]; k = max(1, len(unit_members))
    tr, va, te = folds["train"], folds["val"], folds["test"]
    mu = cls_max[tr].astype(np.float32).mean(0); sd = cls_max[tr].astype(np.float32).std(0) + 1e-6
    subs = cfg["infer_subs"]

    # attribution ranking for toxicity (g/h selection)
    attr = _attribution(cls_max, tr, cls_y.astype(int), mu, sd)
    g_members = np.argsort(-attr)[:cfg["scr_default_N"]].tolist()
    h_idx = np.argsort(-attr)[:k].tolist()

    # (f) LEACE surface-invariant probe
    try:
        f_scores, leace_used, leace_r = fit_leace_probe(
            arrs["content_on"]["resid_mean"], arrs["content_off"]["resid_mean"],
            arrs["surface_x"]["resid_mean"], arrs["surface_xpar"]["resid_mean"], cls_resid)
    except Exception as e:
        logger.error(f"LEACE probe failed: {e}")
        f_scores = _lr_resid(cls_resid, tr, cls_y.astype(int)); leace_used = "lr_fallback"; leace_r = 0

    yc = cls_y.astype(int)
    scores = {
        "f": f_scores,
        "g": lr_feature_score(_feat_sae(cls_max, g_members), tr, yc),
        "h": lr_feature_score(_feat_dir(cls_resid, h_idx, W_dec), tr, yc),
        "unit": lr_feature_score(_feat_sae(cls_max, unit_members), tr, yc),
    }
    val_neg = va & (cls_y == 0)
    worst = {}; per_sub = {}; thr = {}; cis = {}
    for m, sc in scores.items():
        w, per, t_thr, ci = _worst_subctx_recall(sc, val_neg, cls_sub, te, subs, cfg["target_fpr"],
                                                  rng=rng, B=cfg["b_boot_aux"])
        worst[m] = w; per_sub[m] = per; thr[m] = t_thr; cis[m] = ci
        logger.info(f"  worst-subctx-recall[{m}]={w:.3f} CI={ci}")
    gh_worst = np.nanmean([worst["g"], worst["h"]])
    ordering_holds = bool((worst["f"] <= gh_worst + 1e-9) and (gh_worst <= worst["unit"] + 1e-9))

    # unit-minus-(g/h) gap with bootstrap
    te_rows = np.where(te)[0]
    gaps = []
    for _ in range(cfg["b_boot_aux"]):
        ridx = te_rows[rng.integers(0, len(te_rows), len(te_rows))]
        wu = []
        wgh = []
        for s in subs:
            p = ridx[cls_sub[s][ridx] == 1]
            if len(p) > 0:
                wu.append((scores["unit"][p] >= thr["unit"]).mean())
                wgh.append(0.5 * ((scores["g"][p] >= thr["g"]).mean() + (scores["h"][p] >= thr["h"]).mean()))
        if wu and wgh:
            gaps.append(min(wu) - min(wgh))
    gap_ci = boot_ci(gaps)

    # ---- reweight slope (the inferential object) ----
    pos_te = te & (cls_y == 1)
    pos_rows = np.where(pos_te)[0]
    disj = np.zeros(len(pos_rows), dtype=bool)
    for s in cfg["disjoint_subs"]:
        disj |= (cls_sub[s][pos_rows] == 1)
    submemb = {s: (cls_sub[s][pos_rows] == 1) for s in subs}
    detect = {m: (scores[m][pos_rows] >= thr[m]) for m in ["unit", "g", "h"]}

    def mixdist(weights):
        mass = np.array([(weights * submemb[s]).sum() for s in subs], dtype=np.float64)
        tot = mass.sum()
        return mass / tot if tot > 0 else mass

    base_w = np.ones(len(pos_rows))
    p_base = mixdist(base_w)
    mags, gapw, recw_unit, recw_gh = [], [], [], []
    for w in cfg["reweight_w"]:
        weights = np.where(disj, float(w), 1.0)
        p_w = mixdist(weights)
        mag = 0.5 * float(np.abs(p_w - p_base).sum())
        ru = float((weights * detect["unit"]).sum() / weights.sum())
        rgh = float((weights * (0.5 * (detect["g"] + detect["h"]))).sum() / weights.sum())
        mags.append(mag); recw_unit.append(ru); recw_gh.append(rgh); gapw.append(ru - rgh)
    slope = float(np.polyfit(mags, gapw, 1)[0]) if len(set(mags)) > 1 else float("nan")
    # bootstrap slope
    slopes = []
    npos = len(pos_rows)
    for _ in range(cfg["b_boot_aux"]):
        bi = rng.integers(0, npos, npos)
        dj = disj[bi]
        sm = {s: submemb[s][bi] for s in subs}
        dt = {m: detect[m][bi] for m in ["unit", "g", "h"]}
        def md(wt):
            mass = np.array([(wt * sm[s]).sum() for s in subs], np.float64); tt = mass.sum()
            return mass / tt if tt > 0 else mass
        pb = md(np.ones(npos)); mg = []; gp = []
        for w in cfg["reweight_w"]:
            wt = np.where(dj, float(w), 1.0)
            mg.append(0.5 * float(np.abs(md(wt) - pb).sum()))
            ru = (wt * dt["unit"]).sum() / wt.sum()
            rgh = (wt * (0.5 * (dt["g"] + dt["h"]))).sum() / wt.sum()
            gp.append(ru - rgh)
        if len(set(mg)) > 1:
            slopes.append(np.polyfit(mg, gp, 1)[0])
    slope_ci = boot_ci(slopes)

    sel = dict(
        worst_subctx_recall={m: worst[m] for m in scores},
        worst_subctx_recall_ci=cis, worst_subctx_per_sub=per_sub,
        ordering_holds=ordering_holds, ordering="(f) <= (g)/(h) <= unit",
        unit_minus_gh_gap=float(worst["unit"] - gh_worst), unit_minus_gh_gap_ci=gap_ci,
        unit_minus_f_gap=float(worst["unit"] - worst["f"]), unit_minus_f_caveat="conceded as pooling, not selection",
        reweight_magnitudes=[float(x) for x in mags], gap_by_w=[float(x) for x in gapw],
        recall_by_w_unit=[float(x) for x in recw_unit], recall_by_w_gh=[float(x) for x in recw_gh],
        reweight_w=cfg["reweight_w"], slope=slope, slope_ci=slope_ci,
        slope_excludes_0=bool((slope_ci[0] > 0) or (slope_ci[1] < 0)) if not any(math.isnan(x) for x in slope_ci) else False,
        leace_method=leace_used, leace_subspace_dim=int(leace_r),
        g_members=g_members[:10], h_idx=h_idx[:10],
        note="realistic toxicity outcome may be (f)~=(g)/(h)~=unit (a single dense invariant probe suffices) -> reported honestly",
    )
    return sel


# =============================================================================
# STAGE 7 : ADMISSION + MULTIPLICITY + SURFACE NULL
# =============================================================================
def _within_unit_corr(R, members):
    if len(members) < 2:
        return 0.0
    Rc = R[:, members].astype(np.float32)
    ranks = rankdata(Rc, axis=0)
    C = np.corrcoef(ranks, rowvar=False)
    iu = np.triu_indices(len(members), 1)
    return float(np.nan_to_num(C[iu]).mean())


def stage7_admission(state, arrs, W_dec, folds, rng):
    log_stage("STAGE 7 : admission + multiplicity + surface null")
    cfg = CONFIG
    R = state["R"]; cls_max = arrs["cls"]["act_max"]; cls_y = state["cls_y"]
    fires_cls = state["fires_cls"]
    tr, te = folds["train"], folds["test"]
    mu = cls_max[tr].astype(np.float32).mean(0); sd = cls_max[tr].astype(np.float32).std(0) + 1e-6
    cls_max_te = cls_max[te].astype(np.float32)   # precompute test slice once (hot loops)
    te_tox_y = cls_y[te].astype(int)
    cand = state["candidate_units"]
    # pool of latents for null sampling: content-responsive set (fallback all firing)
    pool = state["cr_idx"]
    if len(pool) < 20:
        pool = np.where(state["recall"] > 0)[0]
    # surface arrays
    sx = arrs["surface_x"]["act_max"].astype(np.float32)
    sxp = arrs["surface_xpar"]["act_max"].astype(np.float32)
    surf_resp_all = np.abs(sx - sxp)  # [Nsp,16384]

    def pooled_auc(members):
        sc = maxpool_score(cls_max_te, members, mu, sd)
        return auc_1d(sc, te_tox_y)

    def best_single_auc(members):
        return max(auc_1d(cls_max_te[:, m], te_tox_y) for m in members)

    def surf_resp(members):
        return float(surf_resp_all[:, members].max(1).mean()) if len(members) else 0.0

    # null distributions by random-k
    def null_dists(kk, n=200):
        au, sr, cc = [], [], []
        for _ in range(n):
            ms = rng.choice(pool, size=min(kk, len(pool)), replace=False).tolist()
            au.append(pooled_auc(ms)); sr.append(surf_resp(ms)); cc.append(_within_unit_corr(R, ms))
        return np.array(au), np.array(sr), np.array(cc)

    results = []
    pvals = []
    for u in cand:
        members = [int(m) for m in u["members"]]
        if len(members) < 1:
            continue
        kk = len(members)
        au_null, sr_null, cc_null = null_dists(kk, n=cfg["b_boot_aux"] // 10 if cfg["b_boot_aux"] >= 200 else 50)
        obs_corr = _within_unit_corr(R, members)
        obs_auc = pooled_auc(members)
        obs_gain = obs_auc - (best_single_auc(members) if len(members) >= 1 else 0)
        obs_surf = surf_resp(members)
        p_C = float((cc_null >= obs_corr).mean())
        p_K = float((au_null >= obs_auc).mean())
        sr95 = float(np.percentile(sr_null, 95))
        surface_ok = bool(obs_surf <= sr95)
        jac_ok = all(_max_jaccard(fires_cls, members[i], members[:i]) < cfg["jaccard_max"]
                     for i in range(1, len(members))) if len(members) > 1 else True
        p_min = min(1.0, 2.0 * min(p_C, p_K))  # Bonferroni over the 2 signatures tested per unit (C OR K)
        admit_raw = bool((p_min < 0.05) and surface_ok)
        results.append(dict(name=u["name"], k=kk, members=members[:25], track=u["track"],
                            within_unit_corr=obs_corr, pooled_auc=obs_auc, pooled_gain=obs_gain,
                            surf_response=obs_surf, surf_null95=sr95, surface_ok=surface_ok,
                            firing_jaccard_ok=jac_ok, p_C=p_C, p_K=p_K, p_min=p_min, admit_raw=admit_raw,
                            cleared_signature=("C" if p_C < 0.05 else "") + ("K" if p_K < 0.05 else "")))
        pvals.append(p_min)

    # multiplicity (BH) over candidate-unit min-p
    from statsmodels.stats.multitest import multipletests
    if pvals:
        rej, padj, _, _ = multipletests(pvals, method="fdr_bh")
        for r_, pa, rj in zip(results, padj, rej):
            r_["p_bh"] = float(pa)
            r_["admit_bh"] = bool(rj and r_["surface_ok"])

    # empirical family-wise false-admit on random-k null (run admission on random units)
    n_null_units = 200
    false_admits = 0
    if len(pool) >= 2:
        for _ in range(n_null_units):
            kk = rng.integers(2, max(3, min(8, len(pool))))
            ms = rng.choice(pool, size=kk, replace=False).tolist()
            au_null, sr_null, cc_null = null_dists(kk, n=50)
            p_C = float((cc_null >= _within_unit_corr(R, ms)).mean())
            p_K = float((au_null >= pooled_auc(ms)).mean())
            so = bool(surf_resp(ms) <= float(np.percentile(sr_null, 95)))
            pm = min(1.0, 2.0 * min(p_C, p_K))
            if (pm < 0.05) and so:
                false_admits += 1
    far = false_admits / n_null_units

    adm = dict(
        M=len(results), candidate_units=results,
        admitted_units=[r["name"] for r in results if r.get("admit_bh", r["admit_raw"])],
        false_admit_rate_random_k=float(far),
        surface_null_size=int(sx.shape[0]),
        surface_caveat="surface pairs (n=546) were BOTH generated and judged by gpt-4o-mini "
                       "(judge pass 70.6%); same-model circularity is a limitation. An enlarged, "
                       "independently-judged surface set arrives via the sibling dataset artifact.",
        multiplicity="Benjamini-Hochberg over M candidate-unit min(p_C,p_K); separate from the "
                     "across-targets Holm in STAGE 5/6.",
    )
    return adm


# =============================================================================
# EMIT
# =============================================================================
def to_native(o):
    if isinstance(o, dict):
        return {str(k): to_native(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [to_native(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return None if (math.isnan(float(o)) or math.isinf(float(o))) else float(o)
    if isinstance(o, np.ndarray):
        return to_native(o.tolist())
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, float):
        return None if (math.isnan(o) or math.isinf(o)) else o
    return o


def build_predictions_dataset(cls, tox_preds):
    examples = []
    if tox_preds and "_rows" in tox_preds:
        rows = tox_preds["_rows"]
        names = [n for n in tox_preds if n != "_rows"]
        for j, ri in enumerate(rows[:6000]):
            c = cls[ri]
            ex = dict(
                input=(c["text"] or "")[:1000], output=("toxic" if c["y"] == 1 else "non_toxic"),
                metadata_id=c["id"], metadata_fold=c["fold"], metadata_toxicity_label=int(c["y"]),
            )
            for s in CONFIG["sub_order"]:
                ex[f"metadata_sub_{s}"] = int(c["sub"].get(s, 0) or 0)
            for n in names:
                ex[f"predict_{n}"] = "toxic" if bool(tox_preds[n][j]) else "non_toxic"
            examples.append(ex)
    if not examples:  # guarantee minItems>=1
        examples = [dict(input="(no test classification rows in this run)", output="non_toxic",
                         metadata_note="degenerate_or_smoke_run")]
    return dict(dataset="civil_comments_test_predictions", examples=examples)


# Internal keys that hold large numpy state and must NEVER be JSON-serialized.
_PRIVATE_KEYS = ("_state", "_tox_preds", "_candidates")


def _public(results):
    return {k: v for k, v in results.items() if k not in _PRIVATE_KEYS}


def emit(results, cls, tox_preds, out_path):
    datasets = [build_predictions_dataset(cls, tox_preds)]
    payload = dict(metadata=to_native(_public(results)), datasets=datasets)
    Path(out_path).write_text(json.dumps(payload, indent=2))
    logger.info(f"wrote {out_path} ({Path(out_path).stat().st_size/1e6:.2f} MB)")


def checkpoint(results, out_path):
    try:
        Path(out_path).write_text(json.dumps(dict(metadata=to_native(_public(results)),
                                                   datasets=[dict(dataset="checkpoint",
                                                                  examples=[dict(input="checkpoint", output="partial")])]),
                                             indent=2))
    except Exception as e:
        logger.warning(f"checkpoint write failed: {e}")


# =============================================================================
# MAIN
# =============================================================================
def build_folds(cls):
    fold = np.array([c["fold"] for c in cls])
    return dict(train=(fold == "train"), val=(fold == "val"), test=(fold == "test"))


def run_stage(name, fn, results, key, out_path, strict):
    t0 = time.time()
    try:
        out = fn()
        if isinstance(key, tuple):
            for k_, v_ in zip(key, out):
                results[k_] = v_
        elif key is not None:
            results[key] = out
        results.setdefault("_timings", {})[name] = round(time.time() - t0, 1)
        checkpoint(results, out_path)
        return out
    except Exception as e:
        logger.exception(f"STAGE {name} FAILED: {e}")
        results[f"_error_{name}"] = f"{type(e).__name__}: {e}"
        checkpoint(results, out_path)
        if strict:
            raise
        return None


@logger.catch(reraise=True)
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(Path("/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_3/full_data_out.json")))
    ap.add_argument("--mini", action="store_true")
    ap.add_argument("--max-cls", type=int, default=0)
    ap.add_argument("--max-pairs", type=int, default=0)
    ap.add_argument("--max-surface", type=int, default=0)
    ap.add_argument("--out", default=str(HERE / "method_out.json"))
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--max-stage", type=int, default=7)
    args = ap.parse_args()

    set_seeds(); set_mem_limits()
    rng = np.random.default_rng(SEED)
    t_start = time.time()
    data_path = Path(args.data)
    if args.mini:
        data_path = data_path.with_name("mini_data_out.json")
    content, surface, cls = load_family(data_path)
    if args.max_pairs and len(content) > args.max_pairs:
        sel = rng.choice(len(content), args.max_pairs, replace=False)
        content = [content[i] for i in sorted(sel)]
    if args.max_surface and len(surface) > args.max_surface:
        sel = rng.choice(len(surface), args.max_surface, replace=False)
        surface = [surface[i] for i in sorted(sel)]
    if args.max_cls and len(cls) > args.max_cls:
        # stratify by fold so val/test (and positives) are present in the subsample
        by_fold = {}
        for i, c in enumerate(cls):
            by_fold.setdefault(c["fold"], []).append(i)
        keep = []
        for f, idxs in by_fold.items():
            n_f = max(1, round(args.max_cls * len(idxs) / len(cls)))
            sel = rng.choice(idxs, min(n_f, len(idxs)), replace=False)
            keep.extend(sel.tolist())
        cls = [cls[i] for i in sorted(keep)]
    logger.info(f"using content={len(content)} surface={len(surface)} cls={len(cls)}")

    enc = Encoder()
    val_texts = ([c["text"] for c in cls if c["y"] == 1][:50] + [c["text"] for c in cls if c["y"] == 0][:50]) or \
                [c["on"] for c in content[:8]]
    val_info = enc.validate(val_texts)

    arrs = {}
    arrs["cls"] = encode_group(enc, "cls", [c["text"] for c in cls], ["act_max", "resid_mean"])
    arrs["content_on"] = encode_group(enc, "content_on", [c["on"] for c in content], ["act_max", "act_mean", "resid_mean"])
    arrs["content_off"] = encode_group(enc, "content_off", [c["off"] for c in content], ["act_mean", "resid_mean"])
    if surface:
        arrs["surface_x"] = encode_group(enc, "surface_x", [s["x"] for s in surface], ["act_max", "resid_mean"])
        arrs["surface_xpar"] = encode_group(enc, "surface_xpar", [s["xpar"] for s in surface], ["act_max", "resid_mean"])
    else:
        arrs["surface_x"] = dict(act_max=np.zeros((1, CONFIG["d_sae"]), np.float16), resid_mean=np.zeros((1, CONFIG["d_model"]), np.float16))
        arrs["surface_xpar"] = dict(act_max=np.zeros((1, CONFIG["d_sae"]), np.float16), resid_mean=np.zeros((1, CONFIG["d_model"]), np.float16))
    W_dec = enc.W_dec
    enc.free_model()
    del enc; gc.collect()
    import torch; torch.cuda.empty_cache()

    folds = build_folds(cls)
    results = dict(config={**{k: CONFIG[k] for k in ["release", "sae_id", "model", "hook", "layer",
                    "d_model", "d_sae", "pool", "seed", "b_boot", "b_boot_aux", "n_min", "tau_prec",
                    "jaccard_max", "gain_min", "beta", "n_shuffle", "max_tok", "target_fpr",
                    "infer_subs", "disjoint_subs", "scr_default_N", "reweight_w"]}},
                   validation=val_info,
                   provenance=dict(n_content=len(content), n_surface=len(surface), n_cls=len(cls),
                                   gpu=torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu"))
    out_path = args.out

    fs_state = run_stage("3_firing", lambda: stage3_firing_structure(arrs, cls, content, rng),
                         results, ("firing_structure", "_state"), out_path, args.strict)
    state = results.get("_state")
    if state is None:
        logger.error("STAGE 3 failed; emitting partial."); results.pop("_state", None)
        emit(results, cls, {}, out_path); return

    if args.max_stage >= 4:
        run_stage("4_unit", lambda: stage4_two_track(state, rng),
                  results, ("unit", "stability", "_candidates"), out_path, args.strict)
        results.pop("_candidates", None)
    if args.max_stage >= 5 and "unit_members" in state:
        run_stage("5_c1", lambda: _wrap_c1(state, arrs, W_dec, folds, rng, results),
                  results, None, out_path, args.strict)
    if args.max_stage >= 6 and "unit_members" in state:
        run_stage("6_selection", lambda: stage6_selection(state, arrs, W_dec, folds, rng),
                  results, "selection", out_path, args.strict)
    if args.max_stage >= 7 and "candidate_units" in state:
        run_stage("7_admission", lambda: stage7_admission(state, arrs, W_dec, folds, rng),
                  results, "admission", out_path, args.strict)

    tox_preds = results.pop("_tox_preds", {})
    results.pop("_state", None)
    results["provenance"]["runtime_s"] = round(time.time() - t_start, 1)
    emit(results, cls, tox_preds, out_path)
    logger.info("DONE")


def _wrap_c1(state, arrs, W_dec, folds, rng, results):
    c1, c1meta, tox_preds = stage5_c1(state, arrs, W_dec, folds, rng)
    results["c1"] = c1
    results["c1_meta"] = c1meta
    results["_tox_preds"] = tox_preds
    return None


if __name__ == "__main__":
    main()


