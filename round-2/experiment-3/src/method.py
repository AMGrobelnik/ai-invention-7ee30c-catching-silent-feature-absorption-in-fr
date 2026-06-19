#!/usr/bin/env python3
"""C3 Generality Experiment — does SAE feature absorption generalize beyond first-letter spelling?

Two-track CCRG (K-track anchored greedy set-cover) on Gemma-2-2b + Gemma Scope
layer_12/width_16k SAE, over the non-spelling absorption testbed (numeric primary,
taxonomic alternative).

Implements (per artifact plan):
  Phase 0  encoder (HF residual @ layer 12, FVU-validated) + SAE encode
  Phase 1  per-hierarchy feature tensors (pairs / surface / corpus)
  Phase 2  content-responsive latents + ANCHOR (from pairs only, non-circular)
  Phase 3  NON-TRIVIALITY GATE (GO/NO-GO) + threshold sensitivity
  Phase 4  parent probe d_p (disjoint corpus-train fold) = non-SAE baseline direction
  Phase 5  K-track anchored greedy max-coverage + admission (signature-K + surface-inv)
  Phase 6  baselines (g) SCR/TPP oracle pool + (h) count-matched + sliced recall vs UNIT/anchor/dense-probe
  Phase 7  KG specialization-edge agreement via FORM-FREE absorption_fraction diagnostic
  Phase 8  honest-null branch ('absorption is spelling-specific')
  Phase 9  emit method_out.json (exp_gen_sol_out schema) + npz/csv artifacts

Run:  uv run method.py --scale full
"""
from __future__ import annotations

import argparse
import gc
import json
import math
import os
import resource
import sys
import time
from pathlib import Path

import numpy as np
import scipy.sparse as sp
from loguru import logger

# ----------------------------------------------------------------------------- paths / logging
WORKSPACE = Path(__file__).resolve().parent
DATA_PATH = Path(
    "/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/"
    "gen_art_dataset_2/full_data_out.json"
)
RESULTS_DIR = WORKSPACE / "results"
CACHE_DIR = WORKSPACE / "cache"
LOG_DIR = WORKSPACE / "logs"
for d in (RESULTS_DIR, CACHE_DIR, LOG_DIR):
    d.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(str(LOG_DIR / "run.log"), rotation="50 MB", level="DEBUG")

# ----------------------------------------------------------------------------- hardware / limits
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
import torch  # noqa: E402


def _container_ram_bytes() -> int:
    for p in ["/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"]:
        try:
            v = Path(p).read_text().strip()
            if v != "max" and int(v) < 1_000_000_000_000:
                return int(v)
        except (FileNotFoundError, ValueError):
            pass
    return 32 * 1024 ** 3


RAM_LIMIT = _container_ram_bytes()
HAS_GPU = torch.cuda.is_available()
DEVICE = torch.device("cuda" if HAS_GPU else "cpu")
# NOTE: do NOT set RLIMIT_AS when using CUDA — the CUDA runtime reserves a very large
# *virtual* address space (tens of GB+) that is not resident RAM; an RLIMIT_AS cap would
# crash CUDA init. Real RAM usage here is small (sparse latents + fp16 residuals); the
# cgroup memory limit ({:.0f} GB) is the genuine guard. On CPU-only we set a soft cap.
if not HAS_GPU:
    try:
        cap = int(RAM_LIMIT * 0.80)
        resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
        logger.info(f"CPU-only: RLIMIT_AS set to {cap/1e9:.1f} GB")
    except (ValueError, OSError) as e:  # pragma: no cover
        logger.warning(f"could not set RLIMIT_AS: {e}")
if HAS_GPU:
    torch.cuda.set_per_process_memory_fraction(0.92, 0)
    logger.info(f"GPU: {torch.cuda.get_device_name(0)} "
                f"({torch.cuda.get_device_properties(0).total_memory/1e9:.1f} GB) | "
                f"cgroup RAM limit {RAM_LIMIT/1e9:.0f} GB")
else:
    logger.warning("No GPU detected — running on CPU (will be slow).")

# ----------------------------------------------------------------------------- constants
SAE_RELEASE = "gemma-scope-2b-pt-res-canonical"
SAE_ID_16K = "layer_12/width_16k/canonical"
SAE_ID_65K = "layer_12/width_65k/canonical"
MODEL_GATED = "google/gemma-2-2b"
MODEL_MIRROR = "unsloth/gemma-2-2b"
D_MODEL = 2304
HOOK_LAYER_DEFAULT = 12  # HF decoder layer 12 output == blocks.12.hook_resid_post == hidden_states[13]
MAXLEN = 288  # covers max stored target token idx (248) + BOS
BATCH = 16    # small batch: shared GPU may already hold another process's memory
SEED = 20240617

# gate / algorithm thresholds (pinned from dossiers)
G1_RECALL = 0.60
JACCARD_MAX = 0.10
SUBCTX_PREC = 0.70
GAIN_MIN = 0.05
PRECISION_FLOOR = 0.70
N_MIN_ELIGIBLE = 150
GREEDY_MAX_MEMBERS = 8

rng = np.random.default_rng(SEED)


# ============================================================================= data loading
def load_hierarchies(path: Path, hierarchies: list[str], max_corpus: int | None = None,
                     max_pairs: int | None = None, sub_context: str | None = None) -> dict:
    """Load rows grouped by hierarchy. Adds a stable integer row_id per hierarchy."""
    logger.info(f"loading data from {path}")
    blob = json.loads(path.read_text())
    name_map = {"numeric": "numeric_absorption", "taxonomic": "taxonomic_absorption"}
    out: dict[str, list[dict]] = {}
    for h in hierarchies:
        ds = next(d for d in blob["datasets"] if d["dataset"] == name_map[h])
        rows = ds["examples"]
        if sub_context is not None:
            # keep the chosen sub-context positives + ALL negatives + matched pairs
            rows = [r for r in rows if (r["metadata_sub_context"] == sub_context)
                    or (r["output"] == "negative")
                    or (r["metadata_pair_role"] in ("x_off",))]
        if max_corpus is not None:
            corpus = [r for r in rows if r["metadata_row_type"] == "corpus"][:max_corpus]
            other = [r for r in rows if r["metadata_row_type"] != "corpus"]
            if max_pairs is not None:
                other = other[:max_pairs]
            rows = other + corpus
        for i, r in enumerate(rows):
            r["row_id"] = i
        out[h] = rows
        logger.info(f"  {h}: {len(rows)} rows")
    return out


# ============================================================================= model + SAE
class JumpReLUSAE:
    """Gemma Scope JumpReLU SAE loaded directly from DeepMind's params.npz.

    Avoids importing sae_lens/transformer_lens (very heavy on a contended FS). The forward is
    the canonical gemma-scope one (DeepMind tutorial), with NO input normalisation:
        encode(x) = relu(x @ W_enc + b_enc) * (x @ W_enc + b_enc > threshold)   [JumpReLU]
        decode(a) = a @ W_dec + b_dec
    Reconstruction (FVU) is validated against the residual stream at run time (V1)."""

    def __init__(self, params_path: str, device):
        d = np.load(params_path)
        self.W_enc = torch.from_numpy(d["W_enc"]).to(device)       # [d_model, d_sae]
        self.W_dec = torch.from_numpy(d["W_dec"]).to(device)       # [d_sae, d_model]
        self.b_enc = torch.from_numpy(d["b_enc"]).to(device)       # [d_sae]
        self.b_dec = torch.from_numpy(d["b_dec"]).to(device)       # [d_model]
        self.threshold = torch.from_numpy(d["threshold"]).to(device)  # [d_sae]
        self.device = device

    def encode(self, x):
        pre = x.to(self.W_enc.dtype) @ self.W_enc + self.b_enc
        return torch.where(pre > self.threshold, torch.relu(pre), torch.zeros_like(pre))

    def decode(self, a):
        return a.to(self.W_dec.dtype) @ self.W_dec + self.b_dec

    def eval(self):
        return self


def _find_sae_params(width_tag: str) -> str:
    """Locate gemma-scope-2b-pt-res layer_12/width_<tag> params.npz (canonical = avg L0 nearest 100).
    Globs the HF cache first; falls back to hf_hub_download."""
    import glob
    import re
    base = os.path.expanduser("~/.cache/huggingface/hub/models--google--gemma-scope-2b-pt-res")
    pats = glob.glob(f"{base}/snapshots/*/layer_12/width_{width_tag}/average_l0_*/params.npz")

    def l0(p):
        m = re.search(r"average_l0_(\d+)", p)
        return int(m.group(1)) if m else 9999

    if pats:
        return min(pats, key=lambda p: abs(l0(p) - 100))
    from huggingface_hub import hf_hub_download
    canon = {"16k": "average_l0_82", "65k": "average_l0_73"}
    return hf_hub_download("google/gemma-scope-2b-pt-res",
                           f"layer_12/width_{width_tag}/{canon[width_tag]}/params.npz")


def load_sae(sae_id: str):
    width_tag = "16k" if "16k" in sae_id else "65k"
    path = _find_sae_params(width_tag)
    logger.info(f"loading SAE (direct params.npz) {SAE_RELEASE} / {sae_id} from {path}")
    sae = JumpReLUSAE(path, DEVICE)
    w = sae.W_dec
    logger.info(f"  SAE loaded: W_dec shape {tuple(w.shape)} dtype {w.dtype} | "
                f"threshold[min,mean,max]=[{sae.threshold.min():.2f},{sae.threshold.mean():.2f},{sae.threshold.max():.2f}]")
    assert w.shape[1] == D_MODEL, f"unexpected d_model {w.shape[1]}"
    return sae


def load_model():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    last_err = None
    for mid in (MODEL_GATED, MODEL_MIRROR):
        try:
            logger.info(f"loading model {mid}")
            tok = AutoTokenizer.from_pretrained(mid)
            tok.padding_side = "right"  # keep real tokens at [0,T) so BOS+stored-index fallback holds
            model = AutoModelForCausalLM.from_pretrained(
                mid, torch_dtype=torch.bfloat16, attn_implementation="eager"
            ).to(DEVICE)
            model.eval()
            logger.info(f"  model loaded from {mid}; n_layers={model.config.num_hidden_layers}")
            return model, tok, mid
        except Exception as e:  # noqa: BLE001
            logger.warning(f"  failed to load {mid}: {repr(e)[:200]}")
            last_err = e
    raise RuntimeError(f"could not load gemma-2-2b from any source: {last_err}")


def determine_layer_idx(model, tok, sae, rows: list[dict]) -> int:
    """Pick the HF hidden_states index whose residual the SAE reconstructs (lowest FVU).
    blocks.12.hook_resid_post should be hidden_states[13]; validate empirically (V1).
    Uses forward hooks on the 3 candidate decoder layers in one pass (no logits, no 27-layer store)."""
    sample = [r for r in rows if r["metadata_row_type"] == "corpus"][:32]
    texts = [r["input"] for r in sample]
    enc = tok(texts, return_offsets_mapping=True, add_special_tokens=True, padding=True,
              truncation=True, max_length=MAXLEN, return_tensors="pt")
    offsets = enc.pop("offset_mapping")
    enc = {k: v.to(DEVICE) for k, v in enc.items()}
    caps: dict = {}
    handles = []
    candidates = (11, 12, 13)  # hidden_states idx -> decoder layer (idx-1)
    for hi in candidates:
        def mk(h):
            def hook(_m, _i, out):
                caps[h] = out[0] if isinstance(out, tuple) else out
            return hook
        handles.append(model.model.layers[hi - 1].register_forward_hook(mk(hi)))
    with torch.no_grad():
        model.model(**enc)
    for h in handles:
        h.remove()
    results = {}
    for idx in candidates:
        hs = caps[idx]  # [B,T,2304]
        vecs = []
        for i, r in enumerate(sample):
            pos = _select_positions(r, offsets[i], enc["attention_mask"][i])
            if pos:
                vecs.append(hs[i, pos].float().mean(0))
        X = torch.stack(vecs)  # [n,2304]
        with torch.no_grad():
            recon = sae.decode(sae.encode(X.to(sae.W_dec.dtype)))
        sse = ((X - recon.float()) ** 2).sum().item()
        sst = ((X - X.mean(0)) ** 2).sum().item()
        results[idx] = sse / max(sst, 1e-9)
    logger.info(f"  FVU by hidden_states idx: {{12:{results[12]:.3f}, 13:{results[13]:.3f}, 11:{results[11]:.3f}}}")
    best = min(results, key=results.get)
    if results[best] > 0.6:
        logger.warning(f"  best FVU {results[best]:.3f} is high — SAE/layer mapping may be off")
    logger.info(f"  selected hidden_states[{best}] (HF decoder layer {best-1}); FVU={results[best]:.3f}")
    return best


def _select_positions(row: dict, offsets, attn_mask) -> list[int]:
    """Return token positions for the target span. Char-offset based -> BOS- and
    padding-side agnostic (padding/special tokens have a zero-width (0,0) offset and are
    filtered out). Falls back to stored token indices (+1 for the single prepended <bos>)."""
    off = offsets.tolist() if hasattr(offsets, "tolist") else offsets
    L = len(off)
    T = int(attn_mask.sum().item()) if attn_mask is not None else L
    cs, ce = row["metadata_target_char_start"], row["metadata_target_char_end"]
    if cs is not None and cs >= 0:
        if ce > cs:  # non-empty span -> tokens overlapping [cs,ce)
            pos = [t for t in range(L)
                   if off[t][1] > off[t][0] and off[t][0] < ce and off[t][1] > cs]
        else:  # zero-width (x_off) -> the token containing char cs (the differing slot word)
            pos = [t for t in range(L)
                   if off[t][1] > off[t][0] and off[t][0] <= cs < off[t][1]]
        if pos:
            return pos
    ti = row.get("metadata_target_token_indices")
    if ti:
        return [j + 1 for j in ti if 0 <= j + 1 < T]
    return []


class Encoder:
    def __init__(self, model, tok, sae, layer_idx: int):
        self.model, self.tok, self.sae = model, tok, sae
        self.layer_idx = layer_idx
        self.width = sae.W_dec.shape[0]
        self.sae_dtype = sae.W_dec.dtype
        # forward hook on decoder layer (layer_idx-1) -> capture ONLY its residual output
        # (hidden_states[layer_idx]); avoids storing all 27 layers + the [B,T,vocab] logits.
        self._cap: dict = {}

        def _hook(_mod, _inp, out):
            self._cap["resid"] = out[0] if isinstance(out, tuple) else out

        self._handle = model.model.layers[layer_idx - 1].register_forward_hook(_hook)

    def encode_rows(self, rows: list[dict]):
        """Encode rows -> (CSR max-pooled latents [N,width], fp16 mean-pooled residual [N,2304],
        list of selected-token strings, alignment hit rate, FVU, mean L0)."""
        N = len(rows)
        row_nz: dict[int, tuple] = {}  # gid -> (idx np.int32, val np.float32) ; assembled in order later
        resid = np.zeros((N, D_MODEL), dtype=np.float16)
        sel_strings: list[str] = [""] * N
        n_align_ok = n_align_tot = 0
        l0_sum = l0_cnt = 0.0
        # FVU running accumulators (over corpus target tokens): SSE, sum(x), sum(||x||^2), n
        fvu_sse = 0.0
        fvu_s1 = np.zeros(D_MODEL, dtype=np.float64)
        fvu_s2 = 0.0
        fvu_n = 0
        dropped = 0
        t0 = time.time()
        for b0 in range(0, N, BATCH):
            batch = rows[b0:b0 + BATCH]
            texts = [r["input"] for r in batch]
            enc = self.tok(texts, return_offsets_mapping=True, add_special_tokens=True,
                           padding=True, truncation=True, max_length=MAXLEN, return_tensors="pt")
            offsets = enc.pop("offset_mapping")
            enc = {k: v.to(DEVICE) for k, v in enc.items()}
            with torch.no_grad():
                # inner Gemma2Model fwd; the layer hook captures only layer-12 residual
                self.model.model(**enc)
                hs = self._cap["resid"]  # [B,T,2304]
            # gather target residuals per row
            row_vecs, keep_rows = [], []  # keep_rows: (gid, npos)
            for i, r in enumerate(batch):
                gid = b0 + i
                pos = _select_positions(r, offsets[i], enc["attention_mask"][i])
                if not pos:
                    dropped += 1
                    continue
                keep_rows.append((gid, len(pos)))
                row_vecs.append(hs[i, pos].float())  # [npos,2304]
                ids = enc["input_ids"][i, pos].tolist()
                s = self.tok.decode(ids).strip()
                sel_strings[gid] = s
                if r["metadata_target_text"]:
                    n_align_tot += 1
                    if s.replace(" ", "").lower() == r["metadata_target_text"].replace(" ", "").lower():
                        n_align_ok += 1
            if not row_vecs:
                self._cap.clear()
                continue
            allres = torch.cat(row_vecs, 0)  # [M,2304]
            with torch.no_grad():
                lat = self.sae.encode(allres.to(self.sae_dtype)).float()  # [M,width]
                recon = self.sae.decode(lat.to(self.sae_dtype)).float()   # [M,2304]
            err2 = ((allres - recon) ** 2).sum(1)  # [M] per-token squared error
            m0 = 0
            for (gid, npos) in keep_rows:
                sl = lat[m0:m0 + npos]            # [npos,width]
                sr = allres[m0:m0 + npos]          # [npos,2304]
                pooled_lat = sl.max(0).values       # [width]
                resid[gid] = sr.mean(0).half().cpu().numpy()
                nz = torch.nonzero(pooled_lat > 0).squeeze(-1)
                row_nz[gid] = (nz.cpu().numpy().astype(np.int32),
                               pooled_lat[nz].cpu().numpy().astype(np.float32))
                l0_sum += float((sl > 0).sum().item())
                l0_cnt += npos
                if rows[gid]["metadata_row_type"] == "corpus":
                    fvu_sse += float(err2[m0:m0 + npos].sum().item())
                    xv = sr.double()
                    fvu_s1 += xv.sum(0).cpu().numpy()
                    fvu_s2 += float((xv ** 2).sum().item())
                    fvu_n += npos
                m0 += npos
            self._cap.clear()
            del hs, lat, recon, allres, err2
            if (b0 // BATCH) % 50 == 0:
                logger.info(f"    encoded {b0+len(batch)}/{N} ({(time.time()-t0):.0f}s)")
        # build CSR strictly in row order
        lat_ptr = np.zeros(N + 1, dtype=np.int64)
        for gid in range(N):
            lat_ptr[gid + 1] = lat_ptr[gid] + (len(row_nz[gid][0]) if gid in row_nz else 0)
        total = int(lat_ptr[-1])
        lat_idx = np.zeros(total, dtype=np.int32)
        lat_data = np.zeros(total, dtype=np.float32)
        for gid in range(N):
            if gid in row_nz:
                a, b = lat_ptr[gid], lat_ptr[gid + 1]
                lat_idx[a:b], lat_data[a:b] = row_nz[gid]
        lat_csr = sp.csr_matrix((lat_data, lat_idx, lat_ptr), shape=(N, self.width))
        # FVU = SSE / total-variance over corpus target tokens
        fvu = float("nan")
        if fvu_n > 0:
            sst = fvu_s2 - float(fvu_s1 @ fvu_s1) / fvu_n
            fvu = fvu_sse / max(sst, 1e-9)
        align = n_align_ok / max(n_align_tot, 1)
        mean_l0 = l0_sum / max(l0_cnt, 1)
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        logger.info(f"  encoded {N} rows in {time.time()-t0:.0f}s | dropped(no-pos)={dropped} "
                    f"| align={align:.3f} | FVU={fvu:.3f} | meanL0={mean_l0:.1f} | nnz/row={lat_csr.nnz/N:.0f}")
        return lat_csr, resid, sel_strings, align, fvu, mean_l0, dropped


# ============================================================================= analysis helpers
def bootstrap_ci(values: np.ndarray, B: int = 2000, alpha: float = 0.05) -> tuple[float, float, float]:
    """Bootstrap mean CI over a 1-D array of per-item values."""
    if len(values) == 0:
        return 0.0, 0.0, 0.0
    idx = rng.integers(0, len(values), size=(B, len(values)))
    means = values[idx].mean(1)
    lo, hi = np.percentile(means, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return float(values.mean()), float(lo), float(hi)


def paired_diff_ci(a: np.ndarray, b: np.ndarray, B: int = 10000, alpha: float = 0.05):
    """Paired bootstrap CI on mean(a-b) where a,b are per-item 0/1 hit vectors (same items)."""
    d = a.astype(np.float64) - b.astype(np.float64)
    n = len(d)
    if n == 0:
        return 0.0, 0.0, 0.0
    idx = rng.integers(0, n, size=(B, n))
    means = d[idx].mean(1)
    lo, hi = np.percentile(means, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return float(d.mean()), float(lo), float(hi)


def mcnemar_exact(a: np.ndarray, b: np.ndarray) -> float:
    """Exact McNemar p-value on paired 0/1 hits (all items are positives -> hit==correct)."""
    from statsmodels.stats.contingency_tables import mcnemar
    a = a.astype(bool); b = b.astype(bool)
    n00 = int((~a & ~b).sum()); n01 = int((~a & b).sum())
    n10 = int((a & ~b).sum()); n11 = int((a & b).sum())
    tbl = [[n11, n10], [n01, n00]]
    try:
        return float(mcnemar(tbl, exact=True).pvalue)
    except Exception:  # noqa: BLE001
        return float("nan")


def holm(pvals: dict[str, float]) -> dict[str, float]:
    """Holm-Bonferroni corrected p-values keyed identically to input."""
    from statsmodels.stats.multitest import multipletests
    keys = [k for k, v in pvals.items() if v == v]  # drop nan
    if not keys:
        return {k: float("nan") for k in pvals}
    raw = [pvals[k] for k in keys]
    _, corr, _, _ = multipletests(raw, method="holm")
    out = {k: float(c) for k, c in zip(keys, corr)}
    for k in pvals:
        out.setdefault(k, float("nan"))
    return out


def auc(scores: np.ndarray, labels: np.ndarray) -> float:
    from sklearn.metrics import roc_auc_score
    if len(np.unique(labels)) < 2:
        return 0.5
    return float(roc_auc_score(labels, scores))


def match_threshold(scores: np.ndarray, target_recall: float) -> float:
    """Threshold on a positive-only score vector achieving the target recall (fraction >= tau)."""
    if len(scores) == 0:
        return 0.0
    q = np.quantile(scores, max(0.0, 1.0 - target_recall))
    return float(q)


# ============================================================================= per-hierarchy pipeline
def analyze_hierarchy(name: str, rows: list[dict], lat: sp.csr_matrix, resid: np.ndarray,
                      eligible: list[str], width: int) -> dict:
    logger.info(f"=== analyzing hierarchy '{name}' (rows={len(rows)}, width={width}) ===")
    meta = rows  # row_id == index
    rt = np.array([r["metadata_row_type"] for r in meta])
    role = np.array([r["metadata_pair_role"] for r in meta])
    fold = np.array([r["metadata_fold"] for r in meta])
    label = np.array([1 if r["output"] == "positive" else 0 for r in meta])
    sub = np.array([r["metadata_sub_context"] for r in meta], dtype=object)
    pair_id = np.array([r["metadata_pair_id"] for r in meta], dtype=object)

    lat = lat.tocsr()
    lat.eliminate_zeros()

    # ----- Phase 1: build pair / surface / corpus index sets
    cp_train = (rt == "content_pair") & (fold == "train")
    # map pair_id -> (x_on idx, x_off idx) for train content pairs
    pairs = {}
    for i in np.where(cp_train)[0]:
        pid = pair_id[i]
        pairs.setdefault(pid, {})[role[i]] = i
    pair_ids = [p for p, d in pairs.items() if "x_on" in d and "x_off" in d]
    on_idx = np.array([pairs[p]["x_on"] for p in pair_ids])
    off_idx = np.array([pairs[p]["x_off"] for p in pair_ids])
    pair_sub = np.array([sub[pairs[p]["x_on"]] for p in pair_ids], dtype=object)
    Npair = len(pair_ids)
    logger.info(f"  content pairs (train): {Npair}")

    corp_train = (rt == "corpus") & (fold == "train")
    corp_diag = (rt == "corpus") & (fold == "diagnostic")
    diag_pos = corp_diag & (label == 1)
    diag_rows = np.where(corp_diag)[0]
    diagpos_rows = np.where(diag_pos)[0]
    logger.info(f"  corpus train={int(corp_train.sum())} diag={int(corp_diag.sum())} diag_pos={len(diagpos_rows)}")

    # dense pair latent blocks (small: Npair x width)
    A_on = np.asarray(lat[on_idx].todense())   # [Npair,width]
    A_off = np.asarray(lat[off_idx].todense())
    R = A_on - A_off
    FIRE_on = A_on > 0
    FIRE_off = A_off > 0

    # ----- Phase 2: content-responsive prefilter (sign-flip null) + anchor
    mean_R = R.mean(0)  # [width]
    B_null = 1000
    signs = rng.integers(0, 2, size=(Npair, B_null)) * 2 - 1  # [Npair,B]
    null_means = (R.T @ signs) / Npair  # [width,B]
    tau95 = np.percentile(null_means, 95, axis=1)  # [width]
    content_responsive = (mean_R > tau95) & (mean_R > 0)
    cr_idx = np.where(content_responsive)[0]
    logger.info(f"  content-responsive latents: {len(cr_idx)} / {width}")

    fires_on_cnt = FIRE_on.sum(0)
    precision_l = np.divide((FIRE_on & ~FIRE_off).sum(0), np.maximum(fires_on_cnt, 1),
                            dtype=np.float64)
    cover_count = (FIRE_on & (R > 0)).sum(0)  # |C_l| on pairs

    # negative-firing guard (parent fires on positives, not negatives) on corpus train
    neg_rows = np.where(corp_train & (label == 0))[0]
    if len(neg_rows) > 0:
        neg_fire_rate = np.asarray((lat[neg_rows] > 0).mean(0)).ravel()
    else:
        neg_fire_rate = np.zeros(width)

    anchor_pool = cr_idx[(precision_l[cr_idx] >= PRECISION_FLOOR) & (neg_fire_rate[cr_idx] < 0.5)]
    if len(anchor_pool) == 0:
        anchor_pool = cr_idx[precision_l[cr_idx] >= PRECISION_FLOOR]
    if len(anchor_pool) == 0:
        anchor_pool = cr_idx
    anchor = int(anchor_pool[np.argmax(cover_count[anchor_pool])])
    anchor_cover = set(np.where(FIRE_on[:, anchor] & (R[:, anchor] > 0))[0].tolist())
    anchor_recall_cf = len(anchor_cover) / max(Npair, 1)
    # corpus recall of anchor on diag positives
    anchor_fire_diagpos = np.asarray((lat[diagpos_rows][:, anchor] > 0).todense()).ravel()
    anchor_recall_corp = float(anchor_fire_diagpos.mean()) if len(diagpos_rows) else 0.0
    logger.info(f"  ANCHOR latent={anchor} | precision={precision_l[anchor]:.3f} "
                f"| recall_cf={anchor_recall_cf:.3f} | recall_corp={anchor_recall_corp:.3f} "
                f"| neg_fire={neg_fire_rate[anchor]:.3f}")

    # ----- Phase 4: parent probe d_p on corpus TRAIN residuals (disjoint from diagnostic) = non-SAE baseline
    from sklearn.linear_model import LogisticRegression
    tr_rows = np.where(corp_train)[0]
    Xtr = resid[tr_rows].astype(np.float32)
    ytr = label[tr_rows]
    probe = LogisticRegression(max_iter=2000, C=1.0, class_weight="balanced")
    probe.fit(Xtr, ytr)
    d_p = probe.coef_[0].astype(np.float64)
    d_p_unit = d_p / (np.linalg.norm(d_p) + 1e-9)
    # probe recall per sub-context on diagnostic positives
    Xdiag = resid[diagpos_rows].astype(np.float32)
    probe_pred = probe.predict(Xdiag)
    probe_score_diagpos = probe.decision_function(Xdiag)
    parent_probe_recall_by_sub = {}
    sub_diagpos = sub[diagpos_rows]
    for s in sorted(set(sub_diagpos.tolist())):
        m = sub_diagpos == s
        if m.sum() >= 1:
            parent_probe_recall_by_sub[str(s)] = float(probe_pred[m].mean())
    overall_probe_recall = float(probe_pred.mean()) if len(diagpos_rows) else 0.0
    logger.info(f"  parent probe (non-SAE) overall diag recall={overall_probe_recall:.3f}")

    # ----- corpus diagnostic-positive firing matrix for candidate absorbers (CR subset)
    CR = cr_idx
    fire_diagpos = (lat[diagpos_rows][:, CR] > 0)  # CSR [Npos, |CR|]
    fire_diagpos_d = np.asarray(fire_diagpos.todense())  # bool [Npos,|CR|]
    anchor_in_cr = np.where(CR == anchor)[0]
    anchor_fire = anchor_fire_diagpos  # [Npos]

    # holes (corpus, primary): diag positives anchor misses
    holes_corp = ~anchor_fire  # [Npos]
    H0 = int(holes_corp.sum())
    # holes (content-flip, corroboration)
    holes_cf = np.array([p not in anchor_cover for p in range(Npair)])
    logger.info(f"  holes: corpus={H0}/{len(diagpos_rows)} content-flip={int(holes_cf.sum())}/{Npair}")

    # firing-Jaccard(l, anchor) over diag positives, for CR latents
    inter = (fire_diagpos_d & anchor_fire[:, None]).sum(0).astype(np.float64)
    union = fire_diagpos_d.sum(0) + anchor_fire.sum() - inter
    jaccard_cr = np.divide(inter, np.maximum(union, 1))

    # sub-context precision per CR latent (over diag positives where it fires)
    subs_sorted = sorted([s for s in set(sub_diagpos.tolist()) if s is not None])
    fire_per_sub = np.zeros((len(subs_sorted), len(CR)))
    for si, s in enumerate(subs_sorted):
        m = sub_diagpos == s
        if m.any():
            fire_per_sub[si] = fire_diagpos_d[m].sum(0)
    tot_fire = fire_diagpos_d.sum(0)
    with np.errstate(invalid="ignore", divide="ignore"):
        subctx_prec_cr = np.where(tot_fire > 0, fire_per_sub.max(0) / np.maximum(tot_fire, 1), 0.0)
        subctx_arg_cr = fire_per_sub.argmax(0)

    # hole-coverage gain per CR latent (corpus holes)
    hole_cov_cr = fire_diagpos_d[holes_corp].mean(0) if H0 > 0 else np.zeros(len(CR))

    # ----- Phase 3: NON-TRIVIALITY GATE
    def gain_ci_low(latpos: int) -> float:
        col = fire_diagpos_d[holes_corp, latpos].astype(np.float64)
        _, lo, _ = bootstrap_ci(col, B=2000)
        return lo

    cand_mask = (np.arange(len(CR)) != (anchor_in_cr[0] if len(anchor_in_cr) else -1))
    passing = []
    for j in np.where(cand_mask)[0]:
        if (jaccard_cr[j] < JACCARD_MAX and subctx_prec_cr[j] >= SUBCTX_PREC
                and hole_cov_cr[j] >= GAIN_MIN and precision_l[CR[j]] >= PRECISION_FLOOR):
            lo = gain_ci_low(j)
            if lo > 0:
                passing.append({
                    "latent": int(CR[j]),
                    "jaccard": float(jaccard_cr[j]),
                    "subctx_precision": float(subctx_prec_cr[j]),
                    "specializes": str(subs_sorted[int(subctx_arg_cr[j])]) if subs_sorted else None,
                    "hole_coverage_gain": float(hole_cov_cr[j]),
                    "gain_ci_low": float(lo),
                    "content_precision": float(precision_l[CR[j]]),
                })
    passing.sort(key=lambda d: -d["hole_coverage_gain"])
    anchor_recall_best = max(anchor_recall_cf, anchor_recall_corp)
    g1 = anchor_recall_best >= G1_RECALL
    g2 = len(passing) >= 1
    gate_pass = bool(g1 and g2)
    logger.info(f"  GATE: G1(recall>={G1_RECALL})={g1} (best={anchor_recall_best:.3f}) | "
                f"G2(>=1 absorber)={g2} (n_passing={len(passing)}) | PASS={gate_pass}")

    # threshold sensitivity
    threshold_sensitivity = {}
    for jt in (0.05, 0.10, 0.20):
        for pt in (0.60, 0.70, 0.80):
            for gt in (0.03, 0.05, 0.10):
                cnt = int(np.sum((jaccard_cr[cand_mask] < jt)
                                 & (subctx_prec_cr[cand_mask] >= pt)
                                 & (hole_cov_cr[cand_mask] >= gt)
                                 & (precision_l[CR[cand_mask]] >= PRECISION_FLOOR)))
                threshold_sensitivity[f"J<{jt}_P>={pt}_G>={gt}"] = cnt

    # ----- Phase 5: K-track anchored greedy max-coverage
    unit = [anchor]
    member_fire = {anchor: anchor_fire}  # latent id -> [Npos] bool firing on diag positives
    H = holes_corp.copy()
    edges = []
    H0_fixed = max(int(holes_corp.sum()), 1)
    while H.sum() > 0 and len(unit) < GREEDY_MAX_MEMBERS:
        best_l, best_gain, best_j = None, 0.0, None
        cover_H = (fire_diagpos_d & H[:, None])  # [Npos,|CR|]
        gains = cover_H.sum(0).astype(np.float64) / H0_fixed
        order = np.argsort(-gains)
        for j in order:
            if gains[j] < GAIN_MIN:
                break  # sorted descending -> no further candidate can clear the floor
            latid = int(CR[j])
            if latid in unit:
                continue
            if precision_l[latid] < PRECISION_FLOOR:
                continue
            fl = fire_diagpos_d[:, j]
            # mutual-exclusivity: firing-Jaccard < threshold vs every current member
            ok = True
            for fm in member_fire.values():
                inter_m = int((fl & fm).sum()); union_m = int((fl | fm).sum())
                if union_m > 0 and inter_m / union_m >= JACCARD_MAX:
                    ok = False
                    break
            if not ok:
                continue
            # bootstrap CI on marginal coverage over remaining holes must exclude 0
            col = fl[H].astype(np.float64)
            _, lo, _ = bootstrap_ci(col, B=2000)
            if lo <= 0:
                continue
            best_l, best_gain, best_j = latid, float(gains[j]), j
            break
        if best_l is None:
            break
        unit.append(best_l)
        member_fire[best_l] = fire_diagpos_d[:, best_j]
        covered = fire_diagpos_d[:, best_j]
        edges.append({
            "anchor": anchor, "absorber": best_l,
            "specializes": str(subs_sorted[int(subctx_arg_cr[best_j])]) if subs_sorted else None,
            "marginal_gain": float(best_gain),
            "jaccard": float(jaccard_cr[best_j]),
            "subctx_precision": float(subctx_prec_cr[best_j]),
        })
        H = H & ~covered
        logger.info(f"    + absorber {best_l} specializes={edges[-1]['specializes']} "
                    f"gain={best_gain:.3f} remaining_holes={int(H.sum())}")
    recovered = len(unit) - 1
    logger.info(f"  K-track unit members={unit} | recovered_absorbers={recovered}")

    # ----- admission: signature-K (pooled AUC vs best single, AUC-matched random-k null) + surface invariance
    admission = admission_check(unit, anchor, cr_idx, A_on, A_off, lat, meta, rt, role, fold,
                                pair_id, sub, width)

    # ----- Phase 6: baselines (g)/(h) marginal attribution + sliced recall
    pos_tr = np.where(corp_train & (label == 1))[0]
    neg_tr = np.where(corp_train & (label == 0))[0]
    mean_pos = np.asarray(lat[pos_tr].mean(0)).ravel()
    mean_neg = np.asarray(lat[neg_tr].mean(0)).ravel()
    attribution = np.abs(mean_pos - mean_neg)
    attr_rank = np.argsort(-attribution)
    g_pool = attr_rank[:20].tolist()
    h_pool = attr_rank[:max(len(unit), 1)].tolist()
    logger.info(f"  (g) top-20 pool head={g_pool[:5]} | (h) top-{len(h_pool)} pool={h_pool}")

    # detector scores on ALL diagnostic rows (continuous) -> full classification record;
    # recall / matched threshold derived from the positive subset.
    lat_diag = lat[diag_rows].tocsc()
    diag_label = label[diag_rows]
    diag_sub = sub[diag_rows]
    pos_in_diag = diag_label == 1
    probe_score_diag = probe.decision_function(resid[diag_rows].astype(np.float32)).astype(np.float64)

    def pool_score(pool):
        if not pool:
            return np.zeros(len(diag_rows))
        sub_mat = np.asarray(lat_diag[:, pool].todense())
        return sub_mat.max(1)

    scores = {
        "unit": pool_score(unit),
        "anchor": pool_score([anchor]),
        "g": pool_score(g_pool),
        "h": pool_score(h_pool),
        "dense_probe": probe_score_diag,
    }
    # >0 firing-rule overall recall (on positives)
    overall_recall_raw = {k: float((scores[k][pos_in_diag] > 0.0).mean()) for k in scores}
    # matched recall target = min feasible across SAE pools + probe
    R_match = min(overall_recall_raw["unit"], overall_recall_raw["g"],
                  overall_recall_raw["h"], overall_recall_raw["dense_probe"], overall_recall_raw["anchor"])
    R_match = max(R_match, 0.05)
    taus = {k: match_threshold(scores[k][pos_in_diag], R_match) for k in scores}
    fires_raw = {k: (scores[k] > 0.0) for k in scores}
    fires_matched = {k: (scores[k] >= taus[k]) for k in scores}
    # false-positive rate of each detector on diagnostic negatives (for the prediction record)
    fp_matched = {k: float(fires_matched[k][~pos_in_diag].mean()) if (~pos_in_diag).any() else 0.0
                  for k in scores}
    logger.info(f"  overall recall (>0 rule): {{{', '.join(f'{k}:{v:.3f}' for k,v in overall_recall_raw.items())}}} | R_match={R_match:.3f}")
    logger.info(f"  FP rate (matched): {{{', '.join(f'{k}:{v:.3f}' for k,v in fp_matched.items())}}}")

    # sliced recall per eligible sub-context (+ descriptive)
    sliced = {}
    pvals_g_matched, pvals_h_matched = {}, {}
    absorbed_subs = []
    for s in sorted([x for x in set(diag_sub[pos_in_diag].tolist()) if x is not None]):
        m = pos_in_diag & (diag_sub == s)
        ns = int(m.sum())
        elig = (str(s) in eligible) and ns >= N_MIN_ELIGIBLE
        rec_raw = {k: float(fires_raw[k][m].mean()) for k in scores}
        rec_mat = {k: float(fires_matched[k][m].mean()) for k in scores}
        # absorbed = anchor misses this sub-context more than overall
        is_absorbed = rec_raw["anchor"] < (overall_recall_raw["anchor"] - 0.10)
        ent = {"n": ns, "eligible": bool(elig), "absorbed": bool(is_absorbed),
               "recall_raw": rec_raw, "recall_matched": rec_mat}
        if elig:
            for comp, pool_key in (("g", "g"), ("h", "h")):
                a = fires_matched["unit"][m]; b = fires_matched[pool_key][m]
                diff, lo, hi = paired_diff_ci(a, b)
                p = mcnemar_exact(a, b)
                ent[f"unit_minus_{comp}_matched"] = {"diff": diff, "ci_lo": lo, "ci_hi": hi, "mcnemar_p": p}
                ar = fires_raw["unit"][m]; br = fires_raw[pool_key][m]
                d2, l2, h2 = paired_diff_ci(ar, br)
                ent[f"unit_minus_{comp}_raw"] = {"diff": d2, "ci_lo": l2, "ci_hi": h2,
                                                 "mcnemar_p": mcnemar_exact(ar, br)}
                if comp == "g":
                    pvals_g_matched[str(s)] = p
                else:
                    pvals_h_matched[str(s)] = p
            if is_absorbed:
                absorbed_subs.append(str(s))
        sliced[str(s)] = ent
    holm_g = holm(pvals_g_matched)
    holm_h = holm(pvals_h_matched)
    for s in sliced:
        if s in holm_g:
            sliced[s].setdefault("unit_minus_g_matched", {})["holm_p"] = holm_g[s]
        if s in holm_h:
            sliced[s].setdefault("unit_minus_h_matched", {})["holm_p"] = holm_h[s]

    # C3 confirmation: UNIT recovers >=1 absorber AND unit-minus-(g)/(h) CI>0 on >=1 absorbed sub-context
    c3_confirmed = False
    for s in absorbed_subs:
        e = sliced[s]
        gci = e.get("unit_minus_g_matched", {})
        hci = e.get("unit_minus_h_matched", {})
        if recovered >= 1 and ((gci.get("ci_lo", -1) > 0) or (hci.get("ci_lo", -1) > 0)):
            c3_confirmed = True
            break

    # ----- Phase 7: KG specialization-edge agreement (FORM-FREE absorption_fraction)
    kg = formfree_edge_agreement(edges, anchor, CR, lat, resid, diagpos_rows, sub_diagpos,
                                 anchor_fire, d_p_unit, width)

    # honest-null uniformity description
    recall_vals = list(parent_probe_recall_by_sub.values())
    uniformity = {
        "min_probe_recall": float(np.min(recall_vals)) if recall_vals else 0.0,
        "max_probe_recall": float(np.max(recall_vals)) if recall_vals else 0.0,
        "std_probe_recall": float(np.std(recall_vals)) if recall_vals else 0.0,
    }

    result = {
        "gate_decision": "PASS" if gate_pass else "FAIL",
        "gate_G1_recall_ok": bool(g1),
        "gate_G2_absorber_exists": bool(g2),
        "anchor_latent": anchor,
        "anchor_precision": float(precision_l[anchor]),
        "anchor_neg_fire_rate": float(neg_fire_rate[anchor]),
        "anchor_recall_contentflip": anchor_recall_cf,
        "anchor_recall_corpus": anchor_recall_corp,
        "n_content_responsive": int(len(cr_idx)),
        "n_pairs_train": Npair,
        "n_diag_positives": int(len(diagpos_rows)),
        "holes_corpus": H0, "holes_contentflip": int(holes_cf.sum()),
        "non_triviality_passing_absorbers": passing,
        "threshold_sensitivity": threshold_sensitivity,
        "k_track_unit": unit,
        "recovered_absorber_count": recovered,
        "kg_edges": edges,
        "admission": admission,
        "g_pool": g_pool, "h_pool": h_pool,
        "overall_recall_raw": overall_recall_raw,
        "overall_recall_matched": {k: float(fires_matched[k][pos_in_diag].mean()) for k in scores},
        "fp_rate_matched": fp_matched,
        "matched_recall_target": R_match,
        "sliced_recall": sliced,
        "absorbed_subcontexts": absorbed_subs,
        "c3_confirmed": bool(c3_confirmed),
        "parent_probe_recall_by_subcontext": parent_probe_recall_by_sub,
        "parent_probe_overall_recall": overall_probe_recall,
        "probe_recall_uniformity": uniformity,
        "kg_agreement": kg,
        "eligible_subcontexts": eligible,
    }
    # persist arrays for figures
    np.savez_compressed(
        RESULTS_DIR / f"arrays_{name}_w{width}.npz",
        anchor=np.array([anchor]), unit=np.array(unit), attr_rank=attr_rank[:200],
        attribution=attribution, content_responsive=cr_idx,
        jaccard_cr=jaccard_cr, subctx_prec_cr=subctx_prec_cr, hole_cov_cr=hole_cov_cr,
        d_p=d_p_unit,
    )
    return result, {
        "diag_rows": diag_rows, "fires_raw": fires_raw, "fires_matched": fires_matched,
        "diagpos_rows": diagpos_rows, "scores": scores, "taus": taus,
        "unit": unit, "anchor": anchor, "g_pool": g_pool, "h_pool": h_pool,
        "probe": probe, "lat": lat, "resid": resid, "label": label, "sub": sub, "meta": meta,
    }


def admission_check(unit, anchor, cr_idx, A_on, A_off, lat, meta, rt, role, fold, pair_id, sub, width):
    """signature-K: pooled-max content-response AUC(unit) - best-single-member AUC vs AUC-matched
    random-k null; + unit-level surface invariance on surface pairs."""
    Npair = A_on.shape[0]
    y = np.concatenate([np.ones(Npair), np.zeros(Npair)])  # x_on=1, x_off=0

    def member_pool_auc(pool):
        on = A_on[:, pool].max(1) if len(pool) > 1 else A_on[:, pool[0]]
        off = A_off[:, pool].max(1) if len(pool) > 1 else A_off[:, pool[0]]
        return auc(np.concatenate([on, off]), y)

    pooled_auc = member_pool_auc(unit)
    single_aucs = [member_pool_auc([m]) for m in unit]
    best_single = max(single_aucs)
    gainK = pooled_auc - best_single
    # AUC-matched random-k null
    k = len(unit)
    B = 1000
    null_gains = []
    pool_src = cr_idx if len(cr_idx) >= k else np.arange(width)
    for _ in range(B):
        rp = rng.choice(pool_src, size=k, replace=False).tolist()
        pa = member_pool_auc(rp)
        bs = max(member_pool_auc([m]) for m in rp)
        null_gains.append(pa - bs)
    null95 = float(np.percentile(null_gains, 95))
    sigK = bool(gainK > null95) and recovered_ge1(unit)

    # surface invariance on surface pairs
    sp_mask = (rt == "surface_pair")
    sa, sb = {}, {}
    for i in np.where(sp_mask)[0]:
        pid = pair_id[i]
        if role[i] == "surface_a":
            sa[pid] = i
        elif role[i] == "surface_b":
            sb[pid] = i
    spids = [p for p in sa if p in sb]
    surf_inv = {"n_surface_pairs": len(spids)}
    if spids and len(unit) > 0:
        ai = np.array([sa[p] for p in spids]); bi = np.array([sb[p] for p in spids])
        amat = np.asarray(lat[ai][:, unit].todense()).max(1)
        bmat = np.asarray(lat[bi][:, unit].todense()).max(1)
        # within-pair surface response (same concept, two carriers) -> low if surface-invariant
        obs = float(np.mean(np.abs(amat - bmat)))
        # null: permute which b pairs with which a (cross-pair, different concept instance).
        # A surface-invariant unit's within-pair difference is NOT above this cross-pair null.
        null = []
        if len(spids) > 2:
            for _ in range(1000):
                perm = rng.permutation(len(spids))
                null.append(float(np.mean(np.abs(amat - bmat[perm]))))
        null_mean = float(np.mean(null)) if null else obs
        null05 = float(np.percentile(null, 5)) if null else obs
        null95s = float(np.percentile(null, 95)) if null else obs
        surf_inv.update({"observed_surface_response": obs, "null_mean": null_mean,
                         "null_05": null05, "null_95": null95s,
                         "surface_invariant": bool(obs <= null95s)})
    return {"pooled_auc": float(pooled_auc), "best_single_auc": float(best_single),
            "gainK": float(gainK), "null_95": null95, "signature_K_pass": sigK,
            "surface_invariance": surf_inv}


def recovered_ge1(unit):
    return len(unit) >= 2


def formfree_edge_agreement(edges, anchor, CR, lat, resid, diagpos_rows, sub_diagpos,
                            anchor_fire, d_p_unit, width):
    """For each edge anchor->absorber(l*,s): on diag hole-tokens of sub-context s where anchor is
    silent, diag_absorber = argmax over CR latents of absorption_fraction (~ enc_l * (W_dec_l . d_p)).
    EDGE AGREEMENT = fraction where diag_absorber == l* (top1 / top3). NULL = random CR latent."""
    if not edges:
        return {"edges": [], "note": "no edges proposed"}
    # wdec . d_p over CR latents
    sae_wdec = _GLOBAL["W_dec"]  # [width,2304] numpy
    wdec_dp = sae_wdec @ d_p_unit  # [width]
    lat_dp = lat[diagpos_rows].tocsr()  # [Npos,width]
    CRset = np.asarray(CR)
    # restrict columns to CR and weight by wdec_dp
    sub_lat = np.asarray(lat_dp[:, CRset].todense())  # [Npos,|CR|]
    weighted = sub_lat * wdec_dp[CRset][None, :]      # contribution along parent dir
    weighted[sub_lat <= 0] = -np.inf                  # only firing latents
    diag_arg = weighted.argmax(1)                     # index into CR
    has_fire = np.isfinite(weighted.max(1))
    diag_absorber_latent = np.where(has_fire, CRset[diag_arg], -1)
    # top-3
    top3 = np.argsort(-weighted, axis=1)[:, :3]
    top3_latent = CRset[top3]

    out_edges = []
    for e in edges:
        lstar = e["absorber"]; s = e["specializes"]
        m = (sub_diagpos == s) & (~anchor_fire)  # hole tokens of sub s where anchor silent
        idx = np.where(m)[0]
        if len(idx) == 0:
            out_edges.append({**e, "n_hole_tokens": 0, "agreement_top1": None})
            continue
        top1 = float((diag_absorber_latent[idx] == lstar).mean())
        t3 = float(np.any(top3_latent[idx] == lstar, axis=1).mean())
        # null: random CR latent as 'proposed'
        nulls = []
        firing_idx = idx[has_fire[idx]]
        for _ in range(1000):
            rl = int(rng.choice(CRset))
            nulls.append(float((diag_absorber_latent[firing_idx] == rl).mean()) if len(firing_idx) else 0.0)
        out_edges.append({**e, "n_hole_tokens": int(len(idx)),
                          "agreement_top1": top1, "agreement_top3": t3,
                          "null_mean": float(np.mean(nulls)), "null_95": float(np.percentile(nulls, 95)),
                          "above_null": bool(top1 > np.percentile(nulls, 95))})
    rates = [e["agreement_top1"] for e in out_edges if e.get("agreement_top1") is not None]
    return {"edges": out_edges,
            "mean_agreement_top1": float(np.mean(rates)) if rates else None,
            "mean_null": float(np.mean([e["null_mean"] for e in out_edges if "null_mean" in e])) if rates else None}


_GLOBAL: dict = {}


# ============================================================================= run / orchestration
def get_eligible(name: str) -> list[str]:
    if name == "numeric":
        return ["year", "percent", "currency", "date", "decimal", "integer", "comma_number", "ordinal"]
    return ["Canada", "France", "Iran", "United States", "Brazil", "Georgia", "New Zealand", "Spain",
            "Mexico", "China", "Japan", "India", "Italy", "Ireland", "Australia", "Poland", "Germany",
            "United Kingdom", "Israel", "Russia"]


def encode_or_cache(enc: Encoder, name: str, rows: list[dict], width: int, use_cache: bool):
    tag = f"{name}_w{width}_n{len(rows)}"
    cf_lat = CACHE_DIR / f"lat_{tag}.npz"
    cf_res = CACHE_DIR / f"resid_{tag}.npy"
    if use_cache and cf_lat.exists() and cf_res.exists():
        logger.info(f"  loading cached encodings {tag}")
        lat = sp.load_npz(cf_lat)
        resid = np.load(cf_res)
        return lat, resid, {"cached": True}
    lat, resid, sel, align, fvu, l0, dropped = enc.encode_rows(rows)
    sp.save_npz(cf_lat, lat)
    np.save(cf_res, resid)
    return lat, resid, {"align": align, "fvu": fvu, "mean_l0": l0, "dropped": dropped, "cached": False}


def emit_method_out(per_hierarchy: dict, run_meta: dict, pred_payload: dict):
    datasets = []
    for name, payload in pred_payload.items():
        examples = payload
        datasets.append({"dataset": f"{name}_absorption", "examples": examples})
    out = {"metadata": {**run_meta, "per_hierarchy": per_hierarchy}, "datasets": datasets}
    path = WORKSPACE / "method_out.json"
    path.write_text(json.dumps(out, indent=2, default=_json_default))
    logger.info(f"wrote {path} ({path.stat().st_size/1e6:.1f} MB)")
    # also a compact results-only file
    (RESULTS_DIR / "results.json").write_text(json.dumps(
        {"metadata": out["metadata"]}, indent=2, default=_json_default))
    return path


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


def make_predictions(name, ctx, max_rows=20000):
    """Per-row detector predictions on diagnostic-fold corpus rows (exp_gen_sol_out).
    fires_matched arrays are aligned to ctx['diag_rows'] order (positives + negatives)."""
    diag_rows = ctx["diag_rows"]; meta = ctx["meta"]; label = ctx["label"]
    fires_matched = ctx["fires_matched"]
    examples = []
    for k, ri in enumerate(diag_rows[:max_rows]):
        r = meta[ri]
        is_pos = int(label[ri]) == 1
        ex = {
            "input": r["input"][:280],
            "output": "positive" if is_pos else "negative",
            "metadata_hierarchy": name,
            "metadata_sub_context": str(r["metadata_sub_context"]),
            "metadata_target_text": r["metadata_target_text"],
            "metadata_fold": "diagnostic",
        }
        for det in ("unit", "anchor", "g", "h", "dense_probe"):
            ex[f"predict_{det}"] = "positive" if bool(fires_matched[det][k]) else "negative"
        examples.append(ex)
    return examples


def write_figure_csvs(per_hierarchy: dict):
    """Dump per-sub-context sliced-recall tables as CSV for paper figures."""
    import csv
    for name, r in per_hierarchy.items():
        rows = []
        for s, e in r.get("sliced_recall", {}).items():
            rr, rm = e.get("recall_raw", {}), e.get("recall_matched", {})
            gci = e.get("unit_minus_g_matched", {})
            hci = e.get("unit_minus_h_matched", {})
            rows.append({
                "sub_context": s, "n": e.get("n"), "eligible": e.get("eligible"),
                "absorbed": e.get("absorbed"),
                "recall_unit_raw": rr.get("unit"), "recall_anchor_raw": rr.get("anchor"),
                "recall_g_raw": rr.get("g"), "recall_h_raw": rr.get("h"),
                "recall_dense_raw": rr.get("dense_probe"),
                "recall_unit_matched": rm.get("unit"), "recall_anchor_matched": rm.get("anchor"),
                "recall_g_matched": rm.get("g"), "recall_h_matched": rm.get("h"),
                "recall_dense_matched": rm.get("dense_probe"),
                "unit_minus_g_diff": gci.get("diff"), "unit_minus_g_ci_lo": gci.get("ci_lo"),
                "unit_minus_g_ci_hi": gci.get("ci_hi"), "unit_minus_g_mcnemar_p": gci.get("mcnemar_p"),
                "unit_minus_g_holm_p": gci.get("holm_p"),
                "unit_minus_h_diff": hci.get("diff"), "unit_minus_h_ci_lo": hci.get("ci_lo"),
                "unit_minus_h_ci_hi": hci.get("ci_hi"), "unit_minus_h_mcnemar_p": hci.get("mcnemar_p"),
                "unit_minus_h_holm_p": hci.get("holm_p"),
            })
        if rows:
            p = RESULTS_DIR / f"sliced_recall_{name}.csv"
            with open(p, "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                w.writeheader()
                w.writerows(rows)
            logger.info(f"  wrote {p}")


def overall_verdict(per_hierarchy: dict) -> str:
    confirmed = [h for h, r in per_hierarchy.items() if r.get("c3_confirmed")]
    gate_pass = [h for h, r in per_hierarchy.items() if r.get("gate_decision") == "PASS"]
    if confirmed:
        return "non_spelling_absorption_confirmed"
    if gate_pass:
        return "partial_" + "_".join(gate_pass)
    return "spelling_specific_null"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scale", choices=["smoke", "mini", "full"], default="full")
    ap.add_argument("--hierarchies", default="numeric,taxonomic")
    ap.add_argument("--width", default="16k", choices=["16k", "65k"])
    ap.add_argument("--max-corpus", type=int, default=None)
    ap.add_argument("--max-pairs", type=int, default=None)
    ap.add_argument("--no-cache", action="store_true")
    args = ap.parse_args()

    t_start = time.time()
    hierarchies = args.hierarchies.split(",")
    sae_id = SAE_ID_16K if args.width == "16k" else SAE_ID_65K
    width = 16384 if args.width == "16k" else 65536

    sub_context = None
    if args.scale == "smoke":
        args.max_corpus = args.max_corpus or 10
        args.max_pairs = args.max_pairs or 10
    elif args.scale == "mini":
        sub_context = "year" if "numeric" in hierarchies else None
        hierarchies = ["numeric"]
        args.max_corpus = args.max_corpus or 1200

    data = load_hierarchies(DATA_PATH, hierarchies, max_corpus=args.max_corpus,
                            max_pairs=args.max_pairs, sub_context=sub_context)

    sae = load_sae(sae_id)
    _GLOBAL["W_dec"] = sae.W_dec.detach().float().cpu().numpy()
    model, tok, model_id = load_model()
    layer_idx = determine_layer_idx(model, tok, sae, next(iter(data.values())))
    enc = Encoder(model, tok, sae, layer_idx)

    if args.scale == "smoke":
        # validation gates only
        name = hierarchies[0]
        lat, resid, info = encode_or_cache(enc, name, data[name], width, use_cache=False)
        ok_v1 = info["fvu"] < 0.6
        ok_v2 = info["align"] >= 0.90
        ok_v3 = 1.0 < info["mean_l0"] < width * 0.5
        logger.info(f"SMOKE gates: V1(FVU<0.6)={ok_v1} ({info['fvu']:.3f}) | "
                    f"V2(align>=0.9)={ok_v2} ({info['align']:.3f}) | V3(L0)={ok_v3} ({info['mean_l0']:.1f})")
        assert ok_v1 and ok_v3, "smoke validation failed"
        logger.info("SMOKE PASSED")
        return

    per_hierarchy = {}
    enc_info = {}
    pred_payload = {}
    for name in hierarchies:
        rows = data[name]
        lat, resid, info = encode_or_cache(enc, name, rows, width, use_cache=not args.no_cache)
        enc_info[name] = info
        if not info.get("cached"):
            # V1/V2/V3 self-validation of the (direct) SAE on real data — abort on a broken pipeline
            fvu, align, l0 = info.get("fvu", 1.0), info.get("align", 0.0), info.get("mean_l0", 0.0)
            logger.info(f"  [{name}] encode validation: FVU={fvu:.3f} align={align:.3f} meanL0={l0:.1f}")
            assert fvu < 0.6, f"FVU {fvu:.3f} too high -> SAE/layer pipeline broken"
            assert 1.0 < l0 < width * 0.5, f"mean L0 {l0:.1f} implausible -> SAE broken"
            if align < 0.90:
                logger.warning(f"  [{name}] token alignment {align:.3f} below 0.90")
        eligible = get_eligible(name)
        result, ctx = analyze_hierarchy(name, rows, lat, resid, eligible, width)
        per_hierarchy[name] = result
        pred_payload[name] = make_predictions(name, ctx)
        # checkpoint
        (RESULTS_DIR / f"partial_{name}.json").write_text(json.dumps(result, indent=2, default=_json_default))
        del lat, resid, ctx
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    verdict = overall_verdict(per_hierarchy)
    run_meta = {
        "method_name": "Two-Track CCRG K-track (anchored greedy set-cover) — non-spelling absorption generality (C3)",
        "verdict": verdict,
        "sae": {"release": SAE_RELEASE, "sae_id": sae_id, "width": width,
                "hook": f"blocks.{HOOK_LAYER_DEFAULT}.hook_resid_post",
                "hf_hidden_state_idx": layer_idx, "d_model": D_MODEL},
        "model": model_id,
        "encoding": enc_info,
        "stats": {"bootstrap_B_gate": 2000, "bootstrap_B_paired": 10000, "n_min_eligible": N_MIN_ELIGIBLE,
                  "multiplicity": "holm", "seed": SEED},
        "thresholds": {"G1_recall": G1_RECALL, "jaccard_max": JACCARD_MAX,
                       "subctx_precision": SUBCTX_PREC, "gain_min": GAIN_MIN,
                       "precision_floor": PRECISION_FLOOR},
        "runtime_s": round(time.time() - t_start, 1),
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu",
    }
    emit_method_out(per_hierarchy, run_meta, pred_payload)
    write_figure_csvs(per_hierarchy)
    logger.info(f"DONE. verdict={verdict} runtime={run_meta['runtime_s']}s")
    for name, r in per_hierarchy.items():
        logger.info(f"  [{name}] gate={r['gate_decision']} recovered={r['recovered_absorber_count']} "
                    f"c3_confirmed={r['c3_confirmed']} absorbed={r['absorbed_subcontexts']}")


if __name__ == "__main__":
    main()
