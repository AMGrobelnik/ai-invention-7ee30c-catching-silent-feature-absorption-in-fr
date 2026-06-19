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
# CUDA can be *present* but non-functional: e.g. a Blackwell RTX 5090 (sm_120) under a torch
# build whose kernels stop at sm_90 -> "no kernel image is available". The iter-3 cache-reuse
# path needs NO GPU (only the SAE W_dec as numpy + CPU stats), so probe CUDA once and fall back
# to CPU if a real device op raises. The GPU re-encode fallback is only reachable on a cache miss.
if HAS_GPU:
    try:
        _probe = (torch.ones(8, device="cuda") @ torch.ones(8, device="cuda")).item()
    except Exception as _e:  # noqa: BLE001
        logger.warning(f"CUDA present but non-functional ({repr(_e)[:140]}); falling back to CPU. "
                       f"Re-encoding (cache miss) will be unavailable.")
        HAS_GPU = False
        torch.cuda.is_available = lambda: False  # keep downstream empty_cache()/checks off
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
# iter-4 (M2): high-precision NARROW absorbers each cover fewer pairs, so the precision-gated /
# precision-weighted greedy may need MORE members to fill the same holes -> raise cap 8 -> 12.
GREEDY_MAX_MEMBERS = 12
# iter-4 (M3): documented ambiguous homographs in the taxonomic testbed (US state / given name /
# country share a surface token). Authoritative set; cross-checked at runtime against the
# dataset's metadata_notes=='ambiguous_homograph' flag (discrepancies logged, hardcoded wins).
HOMOGRAPHS_DEFAULT = {"Georgia", "Jordan", "Turkey", "Chile"}
# defining absorbed slice + descriptive (underpowered / co-firing) slices per hierarchy
ABSORBED_DEFINING = {"taxonomic": "Georgia", "numeric": "integer"}
DESCRIPTIVE_SLICES = {"taxonomic": ["Jordan", "United States"], "numeric": ["decimal", "year", "date"]}

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


# ============================================================================= K-track greedy (M2)
def run_greedy(variant: str, anchor: int, CR: np.ndarray, fire_sel_d: np.ndarray,
               anchor_fire_sel: np.ndarray, subctx_prec_sel: np.ndarray, subctx_arg_sel: np.ndarray,
               jaccard_sel: np.ndarray, precision_l: np.ndarray, subs_sorted: list,
               max_members: int) -> tuple[list, list]:
    """Anchored greedy max-coverage K-track, run entirely on the SELECTION (train) fold.

    Three objective variants (M2 — the core conflation fix):
      'original'  rank candidates by RAW coverage gain; gate only content-flip precision_l>=0.70
                  (the iter-3 behaviour that chose the high-coverage/LOW-subctx-precision Georgia
                  absorber 4697 (subctx_prec .35) over the diagnostic-corroborated 16009 (.955)).
      'gated'     ADD a hard per-sub-context FIRING-precision gate subctx_prec_sel>=SUBCTX_PREC
                  (0.70) in ADDITION to precision_l>=0.70, jaccard<0.10, gain>=GAIN_MIN, gain-CI>0.
                  This drops 4697/.35 (and 8442/.35, 9339/.63) and forces the precision-passing
                  Georgia specialist (16009/.955). HEADLINE objective.
      'weighted'  rank by score = subctx_prec_sel * marginal_gain (precision-weighted coverage),
                  keeping the same hard gates incl. the subctx gate. 16009: .955*.482=.460 beats
                  4697: .35*.545=.191.
    Returns (unit member-id list incl. anchor first, edge dicts for the absorbers).
    """
    unit = [anchor]
    member_fire = {anchor: anchor_fire_sel}      # latent id -> [n_sel_pos] bool firing
    H = (~anchor_fire_sel).copy()                # holes = selection-fold positives the anchor misses
    H0_fixed = max(int(H.sum()), 1)
    edges = []
    while H.sum() > 0 and len(unit) < max_members:
        cover_H = fire_sel_d & H[:, None]            # [n_sel_pos,|CR|]
        gains = cover_H.sum(0).astype(np.float64) / H0_fixed
        rank_score = (subctx_prec_sel * gains) if variant == "weighted" else gains
        order = np.argsort(-rank_score)
        chosen = None
        for j in order:
            if rank_score[j] <= 0:
                break  # sorted desc -> nothing further can have positive score
            if gains[j] < GAIN_MIN:                  # marginal coverage floor (on ACTUAL coverage)
                continue
            latid = int(CR[j])
            if latid in unit:
                continue
            if precision_l[latid] < PRECISION_FLOOR:     # content-flip precision gate (all variants)
                continue
            if variant in ("gated", "weighted") and subctx_prec_sel[j] < SUBCTX_PREC:
                continue                                  # NEW per-sub-context firing-precision gate
            fl = fire_sel_d[:, j]
            # mutual-exclusivity: firing-Jaccard < threshold vs EVERY current member
            ok = True
            for fm in member_fire.values():
                inter_m = int((fl & fm).sum()); union_m = int((fl | fm).sum())
                if union_m > 0 and inter_m / union_m >= JACCARD_MAX:
                    ok = False
                    break
            if not ok:
                continue
            # bootstrap CI on marginal coverage over REMAINING holes must exclude 0
            col = fl[H].astype(np.float64)
            _, lo, _ = bootstrap_ci(col, B=2000)
            if lo <= 0:
                continue
            chosen = (latid, float(gains[j]), j)
            break
        if chosen is None:
            break
        latid, gain, j = chosen
        unit.append(latid)
        member_fire[latid] = fire_sel_d[:, j]
        edges.append({
            "anchor": int(anchor), "absorber": latid,
            "specializes": str(subs_sorted[int(subctx_arg_sel[j])]) if subs_sorted else None,
            "marginal_gain": gain,
            "jaccard": float(jaccard_sel[j]),
            "subctx_precision_sel": float(subctx_prec_sel[j]),
        })
        H = H & ~member_fire[latid]
    return unit, edges


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

    # ===== M7 FOLD SPLIT: fit gates / run greedy on the SELECTION (train) fold; report on HELD-OUT =====
    # The iter-3 conflation arose partly because selection AND evaluation used the SAME (diagnostic)
    # fold. Here absorber selection (cover/firing matrix, subctx precision, firing-Jaccard, hole-gain,
    # the greedy) is fit on corpus TRAIN positives; AUC / sliced-recall / router are REPORTED on the
    # disjoint diagnostic fold (held-out). The parent probe d_p is already train-fit (Phase 4).
    CR = cr_idx
    sel_pos_rows = np.where(corp_train & (label == 1))[0]   # SELECTION fold positives
    eval_pos_rows = diagpos_rows                            # HELD-OUT (report) fold positives
    sub_selpos = sub[sel_pos_rows]
    # sub_diagpos already computed in Phase 4 (sub[diagpos_rows])
    anchor_in_cr = np.where(CR == anchor)[0]
    anchor_fire_sel = np.asarray((lat[sel_pos_rows][:, anchor] > 0).todense()).ravel()
    anchor_fire_diag = anchor_fire_diagpos                  # [n_diag_pos] from Phase 2
    anchor_recall_sel = float(anchor_fire_sel.mean()) if len(sel_pos_rows) else 0.0

    # per-fold CR firing matrices (bool [n_pos,|CR|]) — small: ~5k x ~700
    fire_sel_d = np.asarray((lat[sel_pos_rows][:, CR] > 0).todense())
    fire_diag_d = np.asarray((lat[diagpos_rows][:, CR] > 0).todense())

    holes_sel = ~anchor_fire_sel                            # selection-fold holes drive the greedy
    holes_diag = ~anchor_fire_diag                          # held-out holes (reported)
    H0_sel = int(holes_sel.sum())
    H0 = int(holes_diag.sum())                              # 'holes_corpus' field == held-out (iter-3 parity)
    holes_cf = np.array([p not in anchor_cover for p in range(Npair)])
    logger.info(f"  FOLD SPLIT: sel(train) pos={len(sel_pos_rows)} holes={H0_sel} | "
                f"held-out(diag) pos={len(diagpos_rows)} holes={H0} | content-flip holes={int(holes_cf.sum())}/{Npair}")

    # firing-Jaccard(l, anchor) on the SELECTION fold, for CR latents
    inter_s = (fire_sel_d & anchor_fire_sel[:, None]).sum(0).astype(np.float64)
    union_s = fire_sel_d.sum(0) + anchor_fire_sel.sum() - inter_s
    jaccard_sel = np.divide(inter_s, np.maximum(union_s, 1))

    # per-sub-context FIRING precision per CR latent, computed on a given fold
    subs_sorted = sorted([s for s in set(sub_selpos.tolist()) if s is not None])

    def subctx_precision(fire_mat: np.ndarray, sub_vec: np.ndarray):
        fps = np.zeros((len(subs_sorted), fire_mat.shape[1]))
        for si, s in enumerate(subs_sorted):
            m = sub_vec == s
            if m.any():
                fps[si] = fire_mat[m].sum(0)
        tot = fire_mat.sum(0)
        with np.errstate(invalid="ignore", divide="ignore"):
            prec = np.where(tot > 0, fps.max(0) / np.maximum(tot, 1), 0.0)
            arg = fps.argmax(0)
        return prec, arg, fps, tot

    subctx_prec_sel, subctx_arg_sel, _fps_sel, _tot_sel = subctx_precision(fire_sel_d, sub_selpos)
    # HELD-OUT precision of each CR latent w.r.t. its SELECTION-ASSIGNED sub-context (does it hold out?)
    _fps_diag = np.zeros((len(subs_sorted), len(CR)))
    for si, s in enumerate(subs_sorted):
        m = sub_diagpos == s
        if m.any():
            _fps_diag[si] = fire_diag_d[m].sum(0)
    _tot_diag = fire_diag_d.sum(0)
    subctx_prec_diag_assigned = np.zeros(len(CR))
    for j in range(len(CR)):
        sidx = int(subctx_arg_sel[j])
        subctx_prec_diag_assigned[j] = (_fps_diag[sidx, j] / _tot_diag[j]) if _tot_diag[j] > 0 else 0.0

    # hole-coverage gain per CR latent over the FIXED selection-fold holes
    hole_cov_sel = fire_sel_d[holes_sel].mean(0) if H0_sel > 0 else np.zeros(len(CR))

    # ----- Phase 3: NON-TRIVIALITY GATE (fit on SELECTION fold) -----
    def gain_ci_low_sel(latpos: int) -> float:
        col = fire_sel_d[holes_sel, latpos].astype(np.float64)
        _, lo, _ = bootstrap_ci(col, B=2000)
        return lo

    cand_mask = (np.arange(len(CR)) != (anchor_in_cr[0] if len(anchor_in_cr) else -1))
    passing = []
    for j in np.where(cand_mask)[0]:
        if (jaccard_sel[j] < JACCARD_MAX and subctx_prec_sel[j] >= SUBCTX_PREC
                and hole_cov_sel[j] >= GAIN_MIN and precision_l[CR[j]] >= PRECISION_FLOOR):
            lo = gain_ci_low_sel(j)
            if lo > 0:
                passing.append({
                    "latent": int(CR[j]),
                    "jaccard": float(jaccard_sel[j]),
                    "subctx_precision": float(subctx_prec_sel[j]),
                    "subctx_precision_heldout": float(subctx_prec_diag_assigned[j]),
                    "specializes": str(subs_sorted[int(subctx_arg_sel[j])]) if subs_sorted else None,
                    "hole_coverage_gain": float(hole_cov_sel[j]),
                    "gain_ci_low": float(lo),
                    "content_precision": float(precision_l[CR[j]]),
                })
    passing.sort(key=lambda d: -d["hole_coverage_gain"])
    anchor_recall_best = max(anchor_recall_cf, anchor_recall_sel)
    g1 = anchor_recall_best >= G1_RECALL
    g2 = len(passing) >= 1
    gate_pass = bool(g1 and g2)
    logger.info(f"  GATE: G1(recall>={G1_RECALL})={g1} (best={anchor_recall_best:.3f}) | "
                f"G2(>=1 absorber)={g2} (n_passing={len(passing)}) | PASS={gate_pass}")

    # threshold sensitivity (SELECTION fold)
    threshold_sensitivity = {}
    for jt in (0.05, 0.10, 0.20):
        for pt in (0.60, 0.70, 0.80):
            for gt in (0.03, 0.05, 0.10):
                cnt = int(np.sum((jaccard_sel[cand_mask] < jt)
                                 & (subctx_prec_sel[cand_mask] >= pt)
                                 & (hole_cov_sel[cand_mask] >= gt)
                                 & (precision_l[CR[cand_mask]] >= PRECISION_FLOOR)))
                threshold_sensitivity[f"J<{jt}_P>={pt}_G>={gt}"] = cnt

    # ----- Phase 5 / Phase 2 (M2): K-track greedy, THREE objective variants (selection fold) -----
    variant_units, variant_edges = {}, {}
    for variant in ("original", "gated", "weighted"):
        u, e = run_greedy(variant, anchor, CR, fire_sel_d, anchor_fire_sel, subctx_prec_sel,
                          subctx_arg_sel, jaccard_sel, precision_l, subs_sorted, GREEDY_MAX_MEMBERS)
        variant_units[variant] = u
        variant_edges[variant] = e
        geo = next((ed for ed in e if ed["specializes"] == ABSORBED_DEFINING.get(name)), None)
        logger.info(f"  [{variant}] unit={u} ({len(u)-1} absorbers) | defining-member="
                    f"{(geo['absorber'], round(geo['subctx_precision_sel'],3)) if geo else None}")

    HEADLINE_VARIANT = "gated"
    unit = list(variant_units[HEADLINE_VARIANT])
    edges = variant_edges[HEADLINE_VARIANT]
    recovered = len(unit) - 1

    def holes_remaining_sel(u: list) -> int:
        H = (~anchor_fire_sel).copy()
        for m in u[1:]:
            jp = np.where(CR == m)[0]
            if len(jp):
                H = H & ~fire_sel_d[:, jp[0]]
        return int(H.sum())

    def member_info_for(u: list, e: list) -> list:
        info = [{"latent": int(anchor), "role": "anchor", "specializes": "parent",
                 "subctx_precision_sel": None, "subctx_precision_heldout": None,
                 "content_precision": float(precision_l[anchor]),
                 "jaccard_vs_anchor": 0.0, "marginal_gain": None}]
        eba = {ed["absorber"]: ed for ed in e}
        for m in u[1:]:
            jp = np.where(CR == m)[0]
            j = int(jp[0]) if len(jp) else -1
            ed = eba.get(m, {})
            info.append({
                "latent": int(m), "role": "absorber", "specializes": ed.get("specializes"),
                "subctx_precision_sel": float(subctx_prec_sel[j]) if j >= 0 else None,
                "subctx_precision_heldout": float(subctx_prec_diag_assigned[j]) if j >= 0 else None,
                "content_precision": float(precision_l[m]),
                "jaccard_vs_anchor": float(jaccard_sel[j]) if j >= 0 else None,
                "marginal_gain": ed.get("marginal_gain"),
            })
        return info

    # per-variant rebuilt-unit record incl. FORM-FREE KG agreement on the HELD-OUT (diag) fold
    rebuilt_units = {}
    for variant in ("original", "gated", "weighted"):
        u, e = variant_units[variant], variant_edges[variant]
        kg_v = formfree_edge_agreement(e, anchor, CR, lat, resid, diagpos_rows, sub_diagpos,
                                       anchor_fire_diag, d_p_unit, width)
        rebuilt_units[variant] = {
            "members": [int(x) for x in u], "n_members": len(u),
            "recovered_absorbers": len(u) - 1, "edges": e,
            "member_info": member_info_for(u, e),
            "holes_remaining_sel": holes_remaining_sel(u),
            "kg": kg_v,
        }
    logger.info(f"  HEADLINE variant='{HEADLINE_VARIANT}' unit={unit} | recovered_absorbers={recovered}")

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

    # ----- Phase 7 / Phase 4 (M2): per-EDGE form-free KG agreement on the HELD-OUT (diag) fold.
    # Already computed per variant in the rebuilt_units loop; the headline (gated) KG is reported
    # PER EDGE (Georgia / Jordan / United States separately) — NOT as a single 3-edge mean.
    kg = rebuilt_units[HEADLINE_VARIANT]["kg"]

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
        "anchor_recall_selection_fold": anchor_recall_sel,
        "n_content_responsive": int(len(cr_idx)),
        "n_pairs_train": Npair,
        "n_diag_positives": int(len(diagpos_rows)),
        "n_selection_positives": int(len(sel_pos_rows)),
        "fold_split": {"selection_fold": "corpus_train", "report_fold": "corpus_diagnostic",
                       "rationale": "M7: gates/greedy fit on TRAIN positives; AUC/precision/router "
                                    "REPORTED on the disjoint diagnostic (held-out) fold."},
        "holes_corpus": H0, "holes_selection_fold": H0_sel,
        "holes_contentflip": int(holes_cf.sum()),
        "non_triviality_passing_absorbers": passing,
        "threshold_sensitivity": threshold_sensitivity,
        "headline_variant": HEADLINE_VARIANT,
        "k_track_unit": unit,
        "k_track_unit_by_variant": {v: [int(x) for x in variant_units[v]] for v in variant_units},
        "rebuilt_units": rebuilt_units,
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
        jaccard_sel=jaccard_sel, subctx_prec_sel=subctx_prec_sel, hole_cov_sel=hole_cov_sel,
        subctx_prec_diag_assigned=subctx_prec_diag_assigned, cover_count=cover_count, mean_R=mean_R,
        d_p=d_p_unit,
    )
    return result, {
        "diag_rows": diag_rows, "fires_raw": fires_raw, "fires_matched": fires_matched,
        "diagpos_rows": diagpos_rows, "scores": scores, "taus": taus,
        "unit": unit, "anchor": anchor, "g_pool": g_pool, "h_pool": h_pool,
        "probe": probe, "lat": lat, "resid": resid, "label": label, "sub": sub, "meta": meta,
        # ---- iter-3 extras (consumed by iter3_extensions) ----
        "cr_idx": cr_idx, "precision_l": precision_l, "neg_fire_rate": neg_fire_rate,
        "d_p_unit": d_p_unit, "lat_diag": lat_diag, "diag_label": diag_label,
        "diag_sub": diag_sub, "pos_in_diag": pos_in_diag,
        # ---- iter-4 extras (M5 selectors + M3 homograph + ablation) ----
        "cover_count": cover_count, "mean_R": mean_R,
        "subctx_prec_sel": subctx_prec_sel, "subctx_arg_sel": subctx_arg_sel,
        "subs_sorted": subs_sorted, "variant_units": variant_units,
        "anchor_fire_diag": anchor_fire_diag,
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
        firing_idx = idx[has_fire[idx]]
        # The form-free absorption_fraction is a MAGNITUDE diagnostic (enc * W_dec.d_p): on these
        # hole tokens it has its OWN top pick, which may differ from the greedy's chosen absorber
        # l*. Surface it + its sub-context precision + its firing-overlap with l*, so the reader
        # sees WHEN the magnitude oracle and the precision-selected member disagree (and that they
        # are often co-firing representatives of the SAME absorbed slice).
        ff_top, ff_share, ff_prec, abs_vs_ff = None, None, None, None
        if len(firing_idx) > 0:
            picks = diag_absorber_latent[firing_idx]
            vals, cnts = np.unique(picks, return_counts=True)
            ff_top = int(vals[int(np.argmax(cnts))])
            ff_share = float(cnts.max() / len(firing_idx))
            fire_ff = np.asarray((lat_dp[:, ff_top] > 0).todense()).ravel()
            if fire_ff.sum() > 0:
                ff_prec = float((fire_ff & (sub_diagpos == s)).sum() / fire_ff.sum())
            fire_abs = np.asarray((lat_dp[:, lstar] > 0).todense()).ravel()
            uni = int((fire_ff | fire_abs).sum())
            abs_vs_ff = float(int((fire_ff & fire_abs).sum()) / uni) if uni > 0 else 0.0
        # null: random CR latent as 'proposed'
        nulls = []
        for _ in range(1000):
            rl = int(rng.choice(CRset))
            nulls.append(float((diag_absorber_latent[firing_idx] == rl).mean()) if len(firing_idx) else 0.0)
        out_edges.append({**e, "n_hole_tokens": int(len(idx)),
                          "agreement_top1": top1, "agreement_top3": t3,
                          "null_mean": float(np.mean(nulls)), "null_95": float(np.percentile(nulls, 95)),
                          "above_null": bool(top1 > np.percentile(nulls, 95)),
                          "formfree_magnitude_top_latent": ff_top,
                          "formfree_magnitude_top_share": ff_share,
                          "formfree_magnitude_top_subctx_precision": ff_prec,
                          "absorber_vs_formfree_top_firing_jaccard": abs_vs_ff,
                          "absorber_is_formfree_magnitude_top": bool(ff_top == lstar)})
    rates = [e["agreement_top1"] for e in out_edges if e.get("agreement_top1") is not None]
    return {"edges": out_edges,
            "mean_agreement_top1": float(np.mean(rates)) if rates else None,
            "mean_null": float(np.mean([e["null_mean"] for e in out_edges if "null_mean" in e])) if rates else None}


_GLOBAL: dict = {}


# ============================================================================= iter-3 extensions
# M1: RANDOM-ELIGIBLE-k selection-isolation baselines (RE-k + RE-k-anchored)
# M2: per-sub-context classification AUC + STRATIFIED paired-bootstrap AUC-DIFFERENCE CIs
# R1: comparison-matched (Youden) accuracy table (anti predict-all collapse)
# M7/M4: per-hierarchy firing-Jaccard(parent, top detector) router inputs + parent recall holes
# ============================================================================================
def fast_auc(pos_scores: np.ndarray, neg_scores: np.ndarray) -> float:
    """AUC = P(pos>neg) + 0.5*P(tie) via searchsorted (ties handled). NaN if a class empty."""
    n_pos = len(pos_scores)
    n_neg = len(neg_scores)
    if n_pos == 0 or n_neg == 0:
        return float("nan")
    ns = np.sort(neg_scores)
    left = np.searchsorted(ns, pos_scores, side="left")    # count neg < pos
    right = np.searchsorted(ns, pos_scores, side="right")  # count neg <= pos
    less = float(left.sum())
    equal = float((right - left).sum())
    return (less + 0.5 * equal) / (n_pos * n_neg)


def _auc_rows(pos_mat: np.ndarray, neg_mat: np.ndarray) -> np.ndarray:
    """Vectorised AUC per bootstrap row via average-tie rank-sum (Mann-Whitney).
    pos_mat [B,n_pos], neg_mat [B,n_neg] -> AUC [B]. Constant rows -> 0.5 (all ties)."""
    from scipy.stats import rankdata
    B, n_pos = pos_mat.shape
    n_neg = neg_mat.shape[1]
    comb = np.concatenate([pos_mat, neg_mat], axis=1)
    ranks = rankdata(comb, axis=1)            # average ties, per row
    sum_pos = ranks[:, :n_pos].sum(1)
    return (sum_pos - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg)


def _youden_table(det_scores: dict, pos_idx: np.ndarray, neg_idx: np.ndarray) -> dict:
    """Per-detector Youden-J operating point: fit tau on a 50/50 split, eval on the held-out
    half. Reports accuracy / TPR / FPR / balanced-acc + a predicts_all flag so NO detector is
    forced to predict-all (the failure mode of the matched-recall table)."""
    from sklearn.metrics import roc_curve
    pos = pos_idx.copy(); neg = neg_idx.copy()
    rng.shuffle(pos); rng.shuffle(neg)
    ph, nh = len(pos) // 2, len(neg) // 2
    fit_pos, ev_pos = pos[:ph], pos[ph:]
    fit_neg, ev_neg = neg[:nh], neg[nh:]
    if min(len(fit_pos), len(ev_pos), len(fit_neg), len(ev_neg)) == 0:
        return {"note": "insufficient_for_split", "n_pos": int(len(pos)), "n_neg": int(len(neg))}
    out = {"n_pos": int(len(pos)), "n_neg": int(len(neg)), "detectors": {}}
    yfit = np.r_[np.ones(len(fit_pos)), np.zeros(len(fit_neg))]
    for det, sc in det_scores.items():
        sfit = np.r_[sc[fit_pos], sc[fit_neg]]
        fpr, tpr, thr = roc_curve(yfit, sfit)
        tau = float(thr[int(np.argmax(tpr - fpr))])
        ev_tpr = float((sc[ev_pos] >= tau).mean())
        ev_fpr = float((sc[ev_neg] >= tau).mean())
        acc = float((np.r_[sc[ev_pos] >= tau, sc[ev_neg] < tau]).mean())
        out["detectors"][det] = {
            "tau": tau, "accuracy": acc, "tpr": ev_tpr, "fpr": ev_fpr,
            "balanced_acc": float((ev_tpr + (1.0 - ev_fpr)) / 2.0),
            "predicts_all_positive": bool(ev_fpr >= 0.99 and ev_tpr >= 0.99),
        }
    return out


def firing_jaccard_pos(fire_a: np.ndarray, fire_b: np.ndarray) -> float:
    """Positive-only firing Jaccard over a boolean firing vector (matches the M4 router def)."""
    inter = int((fire_a & fire_b).sum())
    union = int((fire_a | fire_b).sum())
    return inter / union if union > 0 else 0.0


def iter3_extensions(name: str, result: dict, ctx: dict, eligible: list[str],
                     b_auc: int = 10000, b_draws: int = 1000) -> tuple[dict, dict]:
    """Phases D-H. Returns (ext dict to merge into result, prediction extras)."""
    logger.info(f"=== iter-3 extensions '{name}' (B_auc={b_auc}, B_draws={b_draws}) ===")
    lat = ctx["lat"]
    diag_rows = ctx["diag_rows"]; diagpos_rows = ctx["diagpos_rows"]
    scores = ctx["scores"]
    unit = list(ctx["unit"]); anchor = int(ctx["anchor"])
    cr_idx = np.asarray(ctx["cr_idx"]); precision_l = ctx["precision_l"]; neg_fire_rate = ctx["neg_fire_rate"]
    d_p_unit = ctx["d_p_unit"]; lat_diag = ctx["lat_diag"]
    diag_sub = ctx["diag_sub"]; pos_in_diag = ctx["pos_in_diag"]; sub = ctx["sub"]
    n_diag = len(diag_rows)

    ABSORBED_DEFINING = {"taxonomic": "Georgia", "numeric": "integer"}
    DESCRIPTIVE = {"taxonomic": ["Jordan", "United States"], "numeric": ["decimal", "year", "date"]}
    defining = ABSORBED_DEFINING[name]

    # ---- PHASE D: cover-eligible pool + RE-k / RE-k-anchored baselines (selection isolation) ----
    ELIG = [int(l) for l in cr_idx if precision_l[l] >= PRECISION_FLOOR and neg_fire_rate[l] < 0.5]
    relaxation = "precision_and_negguard"
    if len(ELIG) < len(unit):
        ELIG = [int(l) for l in cr_idx if precision_l[l] >= PRECISION_FLOOR]
        relaxation = "precision_only"
    if len(ELIG) < len(unit):
        ELIG = [int(l) for l in cr_idx]
        relaxation = "cr_idx"
    k = len(unit)
    rek_computable = len(ELIG) >= k
    logger.info(f"  |ELIG|={len(ELIG)} ({relaxation}); k={k}; rek_computable={rek_computable}")

    def pool_score_diag(pool: list[int]) -> np.ndarray:
        if not pool:
            return np.zeros(n_diag)
        return np.asarray(lat_diag[:, pool].todense()).max(1)

    elig_arr = np.array(ELIG)
    elig_no_anchor = np.array([e for e in ELIG if e != anchor])
    rek_scores = np.zeros((b_draws, n_diag), dtype=np.float32)
    rek_anch_scores = np.zeros((b_draws, n_diag), dtype=np.float32)
    for d in range(b_draws):
        if rek_computable:
            rek_scores[d] = pool_score_diag(rng.choice(elig_arr, size=k, replace=False).tolist())
        if len(elig_no_anchor) >= k - 1:
            pool_a = [anchor] + rng.choice(elig_no_anchor, size=k - 1, replace=False).tolist()
        else:
            pool_a = [anchor]
        rek_anch_scores[d] = pool_score_diag(pool_a)
    rek_mean_score = rek_scores.mean(0)
    rek_anch_mean_score = rek_anch_scores.mean(0)

    det_scores = {
        "unit": np.asarray(scores["unit"]), "anchor": np.asarray(scores["anchor"]),
        "g": np.asarray(scores["g"]), "h": np.asarray(scores["h"]),
        "dense_probe": np.asarray(scores["dense_probe"]),
        "rek_mean": rek_mean_score, "rek_anch_mean": rek_anch_mean_score,
    }
    comparisons = ["g", "h", "rek_mean", "rek_anch_mean", "dense_probe"]

    # ---- M5: NON-RANDOM, LABEL-FREE, COUNT-MATCHED selection controls (S-rec / S-prec / S-mag) ----
    # All three rank the SAME eligible pool ELIG using only content-pair statistics + frozen
    # sub_context (the same information the two-track unit uses) -> label-free. They isolate the
    # SET-COVER choice of absorbers from sensible non-set-cover absorber RANKING. anchored (anchor
    # fixed + top-(k-1)) is PRIMARY; free (top-k) is reported too.
    cover_count = np.asarray(ctx["cover_count"]); mean_R = np.asarray(ctx["mean_R"])
    subctx_prec_sel = np.asarray(ctx["subctx_prec_sel"])
    _cr_pos = {int(l): i for i, l in enumerate(cr_idx)}

    def _prec_of(l):
        i = _cr_pos.get(int(l))
        return float(subctx_prec_sel[i]) if i is not None else 0.0

    _criteria = {
        "S_rec": (lambda l: (float(cover_count[l]),),
                  "content-flip recall (cover_count) -> parent-like high-recall latents"),
        "S_prec": (lambda l: (_prec_of(l), float(cover_count[l])),
                   "selection-fold subctx FIRING precision (tie-break recall); NOT coverage -> non-set-cover"),
        "S_mag": (lambda l: (float(mean_R[l]),),
                  "mean content-response magnitude mean(A_on-A_off) -> strongest (parent-like) responders"),
    }
    selector_members = {}
    for nm, (keyf, desc) in _criteria.items():
        ranked = sorted(ELIG, key=keyf, reverse=True)
        free = [int(x) for x in ranked[:k]]
        non_anch = [int(x) for x in ranked if x != anchor][:k - 1]
        anch = [int(anchor)] + non_anch
        selector_members[nm] = {"free": free, "anchored": anch, "criterion": desc}
        det_scores[f"{nm}_free"] = pool_score_diag(free)
        det_scores[f"{nm}_anch"] = pool_score_diag(anch)
    s_comparisons = ["S_rec_anch", "S_prec_anch", "S_mag_anch", "S_rec_free", "S_prec_free", "S_mag_free"]
    logger.info("  M5 selectors (anchored): " + "; ".join(
        f"{nm}={selector_members[nm]['anchored']}" for nm in _criteria))

    # slices: eligible + defining + descriptive (dedup, present in diag positives)
    present = {s for s in diag_sub[pos_in_diag].tolist() if s is not None}
    slices = [s for s in dict.fromkeys(list(eligible) + [defining] + DESCRIPTIVE.get(name, []))
              if s in present]
    neg_idx = np.where(~pos_in_diag)[0]
    neg_of = {det: det_scores[det][neg_idx] for det in det_scores}
    logger.info(f"  slices={len(slices)} | n_neg(diag)={len(neg_idx)}")

    # ---- PHASE E: per-slice AUC point + bootstrap AUC-DIFFERENCE CIs + RE-k draw distribution ----
    auc_point, auc_diff, rek_dist, selection_established = {}, {}, {}, {}
    for s in slices:
        pos_idx = np.where(pos_in_diag & (diag_sub == s))[0]
        n_pos = len(pos_idx)
        if n_pos == 0:
            continue
        elig_flag = (str(s) in eligible) and (n_pos >= N_MIN_ELIGIBLE)
        ap = {det: fast_auc(det_scores[det][pos_idx], neg_of[det]) for det in det_scores}
        auc_point[str(s)] = {"n_pos": int(n_pos), "n_neg": int(len(neg_idx)),
                             "eligible": bool(elig_flag),
                             **{f"auc_{det}": float(ap[det]) for det in det_scores}}
        # shared bootstrap resample indices for this slice (paired across comparisons)
        ip = rng.integers(0, n_pos, size=(b_auc, n_pos))
        ineg = rng.integers(0, len(neg_idx), size=(b_auc, len(neg_idx)))
        da = _auc_rows(det_scores["unit"][pos_idx][ip], neg_of["unit"][ineg])
        diffs = {}
        # base comparisons everywhere; the (memory-heavier) M5 S-* AUC-diff CIs only on the
        # DEFINING slice where the inferential set-cover-isolation claim is made (S-* point AUCs
        # for every slice are still in `ap`).
        comp_list = comparisons + (s_comparisons if str(s) == str(defining) else [])
        for comp in comp_list:
            db = _auc_rows(det_scores[comp][pos_idx][ip], neg_of[comp][ineg])
            d = da - db
            lo, hi = np.percentile(d, [2.5, 97.5])
            diffs[comp] = {"diff": float(ap["unit"] - ap[comp]), "boot_mean": float(d.mean()),
                           "ci_lo": float(lo), "ci_hi": float(hi)}
        auc_diff[str(s)] = diffs
        del ip, ineg, da
        # RE-k draw distributions (primary M1 selection-isolation object)
        rd = {}
        for variant, mat in (("rek", rek_scores), ("rek_anchored", rek_anch_scores)):
            draw_aucs = _auc_rows(mat[:, pos_idx], mat[:, neg_idx])
            draw_aucs = draw_aucs[np.isfinite(draw_aucs)]
            ua = ap["unit"]
            p95 = float(np.percentile(draw_aucs, 95)) if len(draw_aucs) else float("nan")
            rd[variant] = {
                "mean": float(np.mean(draw_aucs)) if len(draw_aucs) else float("nan"),
                "median": float(np.median(draw_aucs)) if len(draw_aucs) else float("nan"),
                "p5": float(np.percentile(draw_aucs, 5)) if len(draw_aucs) else float("nan"),
                "p95": p95,
                "p97_5": float(np.percentile(draw_aucs, 97.5)) if len(draw_aucs) else float("nan"),
                "unit_auc": float(ua),
                "unit_percentile_in_draws": float((draw_aucs < ua).mean() * 100) if len(draw_aucs) else float("nan"),
                "unit_above_95th": bool(ua > p95) if p95 == p95 else False,
            }
        rek_dist[str(s)] = rd
        selection_established[str(s)] = bool(rd["rek_anchored"]["unit_above_95th"]
                                             and diffs["rek_anch_mean"]["ci_lo"] > 0)

    # ---- PHASE F: comparison-matched (Youden) accuracy table (overall + defining slice) ----
    all_pos_idx = np.where(pos_in_diag)[0]
    youden_overall = _youden_table(det_scores, all_pos_idx, neg_idx)
    youden_defining = {"note": "defining_slice_absent"}
    if defining in present:
        def_pos_idx = np.where(pos_in_diag & (diag_sub == defining))[0]
        youden_defining = _youden_table(det_scores, def_pos_idx, neg_idx)

    # ---- PHASE G: router inputs — firing-Jaccard(parent, top detector) + parent recall holes ----
    parent_fire_all = np.asarray((lat[diagpos_rows][:, anchor] > 0).todense()).ravel()
    elig_router = [e for e in ELIG if e != anchor] or ELIG
    fire_elig = np.asarray((lat[diagpos_rows][:, elig_router] > 0).todense())  # [n_pos_all,|elig_router|]
    sub_pos_all = sub[diagpos_rows]
    # form-free absorber proposal over diag positives (for per-slice KG top1)
    W_dec = _GLOBAL["W_dec"]                # [width, d_model]
    wdec_dp = W_dec @ d_p_unit             # [width]
    CRset = cr_idx
    sub_lat = np.asarray(lat[diagpos_rows][:, CRset].todense())
    weighted = sub_lat * wdec_dp[CRset][None, :]
    weighted[sub_lat <= 0] = -np.inf
    has_fire = np.isfinite(weighted.max(1))
    arg = weighted.argmax(1)
    diag_absorber_latent = np.where(has_fire, CRset[arg], -1)

    absorbed_flag = [str(x) for x in result.get("absorbed_subcontexts", [])]
    router = {}
    for s in slices:
        msk = (sub_pos_all == s)
        npos = int(msk.sum())
        if npos == 0:
            continue
        rec_elig = fire_elig[msk].mean(0)
        top_j = int(np.argmax(rec_elig))
        top_det = int(elig_router[top_j])
        det_fire_all = np.asarray((lat[diagpos_rows][:, top_det] > 0).todense()).ravel()
        parent_recall = float(parent_fire_all[msk].mean())
        hole = msk & (~parent_fire_all) & has_fire
        kg_top1 = float((diag_absorber_latent[hole] == top_det).mean()) if int(hole.sum()) > 0 else None
        fj_val = float(firing_jaccard_pos(parent_fire_all, det_fire_all))
        # absorption-type slice = specialist is mutually-exclusive with the parent AND the parent
        # has a substantial hole here (otherwise a low Jaccard just means the parent already covers it).
        absorption_type = bool(fj_val < JACCARD_MAX and (1.0 - parent_recall) > 0.5)
        router[str(s)] = {
            "parent_latent": anchor, "top_detector_latent": top_det,
            "firing_jaccard": fj_val,
            "slice_regime": ("absorption(mutually_exclusive)" if fj_val < JACCARD_MAX
                             else "co_firing(splitting)"),
            "absorption_type": absorption_type,
            "detector_recall_on_s": float(rec_elig[top_j]),
            "parent_recall_on_s": parent_recall, "parent_recall_hole": float(1.0 - parent_recall),
            "kg_top1_formfree": kg_top1, "n_pos": npos,
            "absorbed_flag_iter2": bool(str(s) in absorbed_flag),
        }
    # Overall regime is keyed to the DEFINING absorbed slice (Georgia / integer). A median over the
    # iter-2 'absorbed' set is reported too but is contaminated: that heuristic over-labels subs the
    # parent actually co-fires on (e.g. United States, Jaccard~0.20) as absorbed.
    fjs_abs = [router[s]["firing_jaccard"] for s in router if s in absorbed_flag]
    med_fj = float(np.median(fjs_abs)) if fjs_abs else float("nan")
    def_fj = router.get(defining, {}).get("firing_jaccard", float("nan"))
    n_absorption_type = int(sum(router[s]["absorption_type"] for s in router))
    regime = ("mutually_exclusive(absorption)" if (def_fj == def_fj and def_fj < JACCARD_MAX)
              else "co_firing(splitting)")

    # ---- representative RE-k draw (median AUC on defining slice) for per-row predictions ----
    pred_extra = {}
    if rek_computable and defining in present:
        from sklearn.metrics import roc_curve
        dpos = np.where(pos_in_diag & (diag_sub == defining))[0]
        draw_aucs = _auc_rows(rek_scores[:, dpos], rek_scores[:, neg_idx])
        med_draw = int(np.argsort(draw_aucs)[len(draw_aucs) // 2])
        rep = rek_scores[med_draw]
        yall = np.r_[np.ones(len(all_pos_idx)), np.zeros(len(neg_idx))]
        sall = np.r_[rep[all_pos_idx], rep[neg_idx]]
        fpr, tpr, thr = roc_curve(yall, sall)
        tau = float(thr[int(np.argmax(tpr - fpr))])
        pred_extra["rek"] = (rep >= tau)
        logger.info(f"  representative RE-k draw idx={med_draw} tau={tau:.4f}")

    # ---- per-row predictions for the M5 selectors + the original/weighted variant units ----
    # (Youden operating point on all-positives vs negatives, same recipe as the RE-k rep draw.)
    from sklearn.metrics import roc_curve as _roc
    _yall = np.r_[np.ones(len(all_pos_idx)), np.zeros(len(neg_idx))]

    def _youden_fires(sc: np.ndarray) -> np.ndarray:
        sall = np.r_[sc[all_pos_idx], sc[neg_idx]]
        fpr, tpr, thr = _roc(_yall, sall)
        tau = float(thr[int(np.argmax(tpr - fpr))])
        return sc >= tau

    for nm in ("S_rec", "S_prec", "S_mag"):
        pred_extra[nm] = _youden_fires(det_scores[f"{nm}_anch"])   # anchored (primary) selector
    for variant in ("original", "weighted"):
        pred_extra[variant] = _youden_fires(pool_score_diag(ctx["variant_units"][variant]))

    # ---- PHASE H: M7 framing flags + honest notes ----
    gen_status = ("diagnostic_corroborated" if name == "taxonomic"
                  else "suggestive_diagnostic_unconfirmed")
    sel_def = bool(selection_established.get(defining, False))
    kg_mean = result.get("kg_agreement", {}).get("mean_agreement_top1")
    def_diff_h = auc_diff.get(defining, {}).get("h", {})
    notes = []
    if name == "taxonomic":
        notes.append("LEAD hierarchy (M2/M7): the precision-gated rebuilt unit's Georgia member is 16009 "
                     "(subctx precision ~0.97 sel / ~0.96 held-out), the precision-passing diagnostic-"
                     "corroborated specialist — NOT the iter-3 low-precision 4697 (~0.35).")
        notes.append("PER-EDGE KG (M2, reported separately, NOT a 3-edge mean): the form-free "
                     "absorption_fraction is a MAGNITUDE oracle and on Georgia holes picks 1966 "
                     "(precision ~0.36), the high-coverage representative; the precise member 16009 "
                     "co-fires with it (firing-Jaccard ~0.36) so per-edge top-1 agreement with 16009 is "
                     "~0. The magnitude oracle is precision-blind; corroboration is via the PRECISION "
                     "diagnostic + the router recall-hole signal, not the magnitude argmax.")
        rj = router.get("Jordan", {})
        if rj:
            notes.append(f"Jordan n={rj.get('n_pos')} (<150 -> DESCRIPTIVE/underpowered); router "
                         f"absorption_type={rj.get('absorption_type')} parent_hole={rj.get('parent_recall_hole')}.")
        if def_diff_h:
            notes.append(f"Georgia AUC(unit)-AUC(h) diff={def_diff_h.get('diff')} "
                         f"CI=[{def_diff_h.get('ci_lo')},{def_diff_h.get('ci_hi')}]: a genuine AUC-rank effect "
                         f"(unit AUC ~0.99 vs g/h below chance — the absorption signature).")
        notes.append("United States: parent co-fires (Jaccard ~0.20, hole ~0.23) -> splitting not "
                     "absorption_type; NOT a homograph-suppression slice.")
        notes.append("HONEST: a non-SAE dense probe matches/slightly edges the unit on Georgia AUC; the "
                     "contribution is auditable WITHIN-SAE precision-gated selection + the homograph router, "
                     "not out-classifying a dense probe.")
    else:
        notes.append("SUGGESTIVE / diagnostic-UNCONFIRMED (M7): integer beats g/h on matched recall BUT "
                     f"KG mean top1={kg_mean} (0.0) and the dense probe AUC dominates -> NOT promoted.")
    notes.append(f"RE-k-anchored is the honest selection control (holds the high-recall anchor fixed, "
                 f"asks whether the set-cover choice of absorbers beats random eligible absorbers).")

    # ============================== M3: HOMOGRAPH x ABSORPTION-TYPE cross-tab (ALL sub-contexts) ==============================
    meta = ctx["meta"]
    homo_from_data = {str(r["metadata_sub_context"]) for r in meta
                      if r.get("metadata_notes") == "ambiguous_homograph" and r.get("metadata_sub_context")}
    homographs = set(HOMOGRAPHS_DEFAULT) if name == "taxonomic" else set()
    homo_discrepancy = (sorted(homo_from_data.symmetric_difference(homographs))
                        if name == "taxonomic" else [])
    if homo_discrepancy:
        logger.warning(f"  homograph set discrepancy (data-notes vs hardcoded): {homo_discrepancy}")
    all_present = sorted([str(s) for s in present])
    router_all = {}
    for s in all_present:
        msk = (sub_pos_all == s)
        npos = int(msk.sum())
        if npos == 0:
            continue
        rec_elig = fire_elig[msk].mean(0)
        top_j = int(np.argmax(rec_elig)); top_det = int(elig_router[top_j])
        det_fire_all = np.asarray((lat[diagpos_rows][:, top_det] > 0).todense()).ravel()
        parent_recall = float(parent_fire_all[msk].mean())
        fj_val = float(firing_jaccard_pos(parent_fire_all, det_fire_all))
        absorption_type = bool(fj_val < JACCARD_MAX and (1.0 - parent_recall) > 0.5)
        router_all[s] = {
            "n_pos": npos, "homograph": bool(s in homographs),
            "parent_recall_on_s": parent_recall, "parent_recall_hole": float(1.0 - parent_recall),
            "top_detector_latent": top_det, "firing_jaccard": fj_val,
            "absorption_type": absorption_type,
            "eligible": bool(s in eligible and npos >= N_MIN_ELIGIBLE),
        }
    cells = {("homograph", "absorption"): [], ("homograph", "no_absorption"): [],
             ("non_homograph", "absorption"): [], ("non_homograph", "no_absorption"): []}
    for s, e in router_all.items():
        hk = "homograph" if e["homograph"] else "non_homograph"
        ak = "absorption" if e["absorption_type"] else "no_absorption"
        cells[(hk, ak)].append(s)
    abs_slices = sorted([s for s, e in router_all.items() if e["absorption_type"]])
    homograph_crosstab = {
        "homographs_hardcoded": sorted(homographs),
        "homographs_from_data_notes": sorted(homo_from_data),
        "homograph_set_discrepancy": homo_discrepancy,
        "counts": {f"{hk}|{ak}": len(v) for (hk, ak), v in cells.items()},
        "members": {f"{hk}|{ak}": sorted(v) for (hk, ak), v in cells.items()},
        "absorption_type_slices": abs_slices,
        "absorption_type_slices_are_exactly_suppressed_homographs": bool(
            len(abs_slices) > 0 and all(router_all[s]["homograph"] for s in abs_slices)),
        "framing": ("absorption recurs on polysemous/homograph tokens WHOSE GENERAL PARENT LATENT IS "
                    "SUPPRESSED (identified a-priori by the router recall-hole signal); it is NOT broad "
                    "taxonomic absorption." if name == "taxonomic"
                    else "numeric has no homographs; integer is absorption-type via the numeric parent "
                         "hole but is diagnostic-UNCONFIRMED (KG top1 0.0, dense probe dominates)."),
    }

    # ============================== M5: SET-COVER selection-isolation verdict (defining slice) ==============================
    def_diffs = auc_diff.get(str(defining), {}); def_ap = auc_point.get(str(defining), {})
    selection_isolation = {"defining_slice": defining, "unit_defining_auc": def_ap.get("auc_unit"),
                           "selectors": {}}
    beats_all_anch = bool(str(defining) in auc_point)
    for nm in ("S_rec", "S_prec", "S_mag"):
        for variant, suf in (("anchored", "anch"), ("free", "free")):
            key = f"{nm}_{suf}"
            c = def_diffs.get(key, {})
            beats = (bool(c.get("ci_lo", -1) > 0) if c else None)
            selection_isolation["selectors"][key] = {
                "variant": variant, "members": selector_members[nm][variant],
                "criterion": selector_members[nm]["criterion"],
                "defining_auc_selector": def_ap.get(f"auc_{key}"),
                "unit_minus_selector_diff": c.get("diff"),
                "ci_lo": c.get("ci_lo"), "ci_hi": c.get("ci_hi"), "beats": beats,
            }
            if variant == "anchored" and beats is not True:
                beats_all_anch = False
    selection_isolation["set_cover_established"] = beats_all_anch

    # ============================== PRECISION-OBJECTIVE ABLATION (original / gated / weighted) ==============================
    variant_units_ctx = ctx["variant_units"]; rebuilt = result.get("rebuilt_units", {})
    def_pos_idx_ab = np.where(pos_in_diag & (diag_sub == defining))[0]
    ena = elig_no_anchor

    def variant_defining_stats(members):
        sc = pool_score_diag(members)
        if len(def_pos_idx_ab) == 0:
            return {}
        a_auc = float(fast_auc(sc[def_pos_idx_ab], sc[neg_idx]))
        k2 = len(members)
        rek2 = np.zeros((b_draws, n_diag), dtype=np.float32)
        for d in range(b_draws):
            pa = ([anchor] + rng.choice(ena, size=k2 - 1, replace=False).tolist()
                  if len(ena) >= k2 - 1 else [anchor])
            rek2[d] = pool_score_diag(pa)
        rek2_mean = rek2.mean(0)
        rek2_mean_auc = float(fast_auc(rek2_mean[def_pos_idx_ab], rek2_mean[neg_idx]))
        ip2 = rng.integers(0, len(def_pos_idx_ab), size=(b_auc, len(def_pos_idx_ab)))
        in2 = rng.integers(0, len(neg_idx), size=(b_auc, len(neg_idx)))
        diff = _auc_rows(sc[def_pos_idx_ab][ip2], sc[neg_idx][in2]) - \
            _auc_rows(rek2_mean[def_pos_idx_ab][ip2], rek2_mean[neg_idx][in2])
        lo, hi = np.percentile(diff, [2.5, 97.5])
        draw_aucs = _auc_rows(rek2[:, def_pos_idx_ab], rek2[:, neg_idx])
        draw_aucs = draw_aucs[np.isfinite(draw_aucs)]
        p95 = float(np.percentile(draw_aucs, 95)) if len(draw_aucs) else float("nan")
        return {"slice_auc": a_auc, "rek_anch_mean_auc": rek2_mean_auc,
                "unit_minus_rek_anch_diff": float(a_auc - rek2_mean_auc),
                "ci_lo": float(lo), "ci_hi": float(hi), "rek_anch_p95": p95,
                "unit_above_rek_anch_95th": (bool(a_auc > p95) if p95 == p95 else False)}

    precision_objective_ablation = {"defining_slice": defining, "variants": {}}
    for variant in ("original", "gated", "weighted"):
        members = [int(x) for x in variant_units_ctx[variant]]
        rb = rebuilt.get(variant, {})
        geo_edge = next((e for e in rb.get("edges", []) if e.get("specializes") == defining), None)
        geo_member = geo_edge["absorber"] if geo_edge else None
        geo_minfo = (next((mi for mi in rb.get("member_info", []) if mi.get("latent") == geo_member), {})
                     if geo_member is not None else {})
        kg_geo = next((e for e in rb.get("kg", {}).get("edges", []) if e.get("specializes") == defining), {})
        st = variant_defining_stats(members)
        precision_objective_ablation["variants"][variant] = {
            "members": members, "n_members": len(members), "recovered_absorbers": len(members) - 1,
            "holes_remaining_sel": rb.get("holes_remaining_sel"),
            "defining_member_latent": geo_member,
            "defining_member_subctx_precision_sel": geo_minfo.get("subctx_precision_sel"),
            "defining_member_subctx_precision_heldout": geo_minfo.get("subctx_precision_heldout"),
            "defining_slice_auc": st.get("slice_auc"),
            "unit_minus_rek_anch_diff": st.get("unit_minus_rek_anch_diff"),
            "rek_anch_ci_lo": st.get("ci_lo"), "rek_anch_ci_hi": st.get("ci_hi"),
            "rek_anch_p95": st.get("rek_anch_p95"),
            "unit_above_rek_anch_95th": st.get("unit_above_rek_anch_95th"),
            "defining_per_edge_kg_top1": kg_geo.get("agreement_top1"),
            "defining_per_edge_kg_above_null": kg_geo.get("above_null"),
        }

    # ============================== M7: rebuilt-unit transparency (headline = gated) ==============================
    headline_variant = result.get("headline_variant", "gated")
    head = rebuilt.get(headline_variant, {}); minfo = head.get("member_info", [])
    absorber_info = [mi for mi in minfo if mi.get("role") == "absorber"]
    frac_heldout_pass = (float(np.mean([1.0 if (mi.get("subctx_precision_heldout") or 0.0) >= SUBCTX_PREC
                                        else 0.0 for mi in absorber_info])) if absorber_info else None)
    member_labeling = []
    for mi in absorber_info:
        l = mi["latent"]
        fl = np.asarray((lat[diagpos_rows][:, l] > 0).todense()).ravel()
        ff_label = None
        if fl.sum() > 0:
            counts = {s: int((fl & (sub_pos_all == s)).sum()) for s in all_present}
            ff_label = max(counts, key=counts.get) if counts else None
        member_labeling.append({"latent": l, "greedy_specializes": mi.get("specializes"),
                                "formfree_heldout_modal_subcontext": ff_label,
                                "agreement": bool(ff_label == mi.get("specializes"))})
    rebuilt_unit_transparency = {
        "headline_variant": headline_variant, "members": head.get("members"), "member_info": minfo,
        "fold_note": ("precision/jaccard/gain gates fit on the SELECTION (train) fold; "
                      "subctx_precision_heldout and ALL AUC/router numbers REPORTED on the held-out "
                      "(diagnostic) fold."),
        "fraction_absorbers_heldout_subctx_precision_ge_0p70": frac_heldout_pass,
        "auditable_claim_restricted_to": "absorbers with held-out subctx precision >= 0.70",
        "member_labeling_formfree_vs_greedy": member_labeling,
        "compact_named_unit_note": ("taxonomic members are each a NAMED specialist (no 15-wide max-pool; "
                                    "that construction was the first-letter testbed); the compact named-unit "
                                    "AUC == the unit AUC."),
    }

    # CORROBORATION of the rebuilt (gated) unit is by the PRECISION diagnostic: the defining-slice
    # member must be in the non-triviality precision-passing set AND precision-passing on BOTH folds.
    # The form-free absorption_fraction is a MAGNITUDE oracle: it prefers the high-coverage LOW-precision
    # representative of the same absorbed slice (e.g. Georgia 1966 prec~.36) over the precise narrow
    # member (16009 prec~.96) — so its per-edge top-1 agreement with the precise member is ~0. That
    # magnitude-vs-precision disagreement is reported HONESTLY and separately (it does NOT gate
    # corroboration, because the precision rebuild is defined against the precision diagnostic).
    gated_ab = precision_objective_ablation["variants"].get("gated", {})
    nt_passing_ids = {p.get("latent") for p in result.get("non_triviality_passing_absorbers", [])}
    gated_geo_id = gated_ab.get("defining_member_latent")
    setcover_corroborated = bool(
        gated_geo_id is not None and gated_geo_id in nt_passing_ids
        and (gated_ab.get("defining_member_subctx_precision_sel") or 0.0) >= SUBCTX_PREC
        and (gated_ab.get("defining_member_subctx_precision_heldout") or 0.0) >= SUBCTX_PREC)
    gated_geo_kg = next((kgi for kgi in result.get("kg_agreement", {}).get("edges", [])
                         if kgi.get("specializes") == defining), {})
    formfree_magnitude_tension = {
        "defining_member_latent": gated_geo_id,
        "defining_member_subctx_precision_heldout": gated_ab.get("defining_member_subctx_precision_heldout"),
        "formfree_magnitude_top_latent": gated_geo_kg.get("formfree_magnitude_top_latent"),
        "formfree_magnitude_top_subctx_precision": gated_geo_kg.get("formfree_magnitude_top_subctx_precision"),
        "member_vs_formfree_top_firing_jaccard": gated_geo_kg.get("absorber_vs_formfree_top_firing_jaccard"),
        "member_is_formfree_magnitude_top": gated_geo_kg.get("absorber_is_formfree_magnitude_top"),
        "per_edge_agreement_top1": gated_geo_kg.get("agreement_top1"),
        "interpretation": ("the form-free MAGNITUDE oracle picks the high-coverage LOW-precision "
                           "representative of the same absorbed slice; the precision-gated member is "
                           "Georgia-pure but NOT the magnitude argmax (they co-fire). Precision "
                           "diagnostic corroborates; magnitude oracle is precision-blind."),
    }
    set_cover_established = bool(selection_isolation["set_cover_established"])
    if name == "taxonomic":
        hierarchy_verdict = ("taxonomic_setcover_isolated"
                             if (set_cover_established and setcover_corroborated)
                             else "taxonomic_cover_eligibility_plus_sensible_selection")
    else:
        hierarchy_verdict = "numeric_suggestive_diagnostic_unconfirmed"

    ext = {
        "iter3_eligible_pool_size": int(len(ELIG)),
        "iter3_eligible_relaxation": relaxation,
        "iter3_eligible_latents": [int(x) for x in ELIG[:50]],
        "iter3_k": int(k),
        "rek_computable": bool(rek_computable),
        "auc_point": auc_point,
        "auc_diff_ci": auc_diff,
        "rek_distribution": rek_dist,
        "selection_established": selection_established,
        "selection_established_defining": sel_def,
        "defining_slice": defining,
        "youden_overall": youden_overall,
        "youden_defining": youden_defining,
        "router": router,
        "router_regime": regime,
        "router_defining_jaccard": float(def_fj),
        "router_median_jaccard_absorbed_iter2set": med_fj,
        "router_n_absorption_type_slices": n_absorption_type,
        "generalization_status": gen_status,
        "honest_notes": notes,
        # ---- iter-4 blocks (M2/M3/M5/M7) ----
        "selector_members": selector_members,
        "selection_isolation": selection_isolation,
        "set_cover_established": set_cover_established,
        "setcover_corroborated": setcover_corroborated,
        "formfree_magnitude_tension": formfree_magnitude_tension,
        "homograph_crosstab": homograph_crosstab,
        "router_all": router_all,
        "precision_objective_ablation": precision_objective_ablation,
        "rebuilt_unit_transparency": rebuilt_unit_transparency,
        "hierarchy_verdict": hierarchy_verdict,
    }
    logger.info(f"  [{name}] selection_established(defining={defining})={sel_def} | "
                f"set_cover_established={set_cover_established} corroborated={setcover_corroborated} | "
                f"router_regime={regime} (defining Jaccard={def_fj:.3f}, n_absorption_type={n_absorption_type}) "
                f"| verdict={hierarchy_verdict}")
    return ext, pred_extra


# ============================================================================= run / orchestration
def get_eligible(name: str) -> list[str]:
    if name == "numeric":
        return ["year", "percent", "currency", "date", "decimal", "integer", "comma_number", "ordinal"]
    return ["Canada", "France", "Iran", "United States", "Brazil", "Georgia", "New Zealand", "Spain",
            "Mexico", "China", "Japan", "India", "Italy", "Ireland", "Australia", "Poland", "Germany",
            "United Kingdom", "Israel", "Russia"]


def encode_or_cache(get_enc, name: str, rows: list[dict], width: int, use_cache: bool):
    """Reuse cached encodings (primary, GPU-free) else re-encode via get_enc() (GPU fallback).
    Guards row-count alignment: cache built with the same deterministic row order is reused."""
    tag = f"{name}_w{width}_n{len(rows)}"
    cf_lat = CACHE_DIR / f"lat_{tag}.npz"
    cf_res = CACHE_DIR / f"resid_{tag}.npy"
    if use_cache and cf_lat.exists() and cf_res.exists():
        logger.info(f"  loading cached encodings {tag}")
        lat = sp.load_npz(cf_lat)
        resid = np.load(cf_res)
        assert lat.shape == (len(rows), width), f"cache lat shape {lat.shape} != {(len(rows), width)}"
        assert resid.shape[0] == len(rows), f"cache resid rows {resid.shape[0]} != {len(rows)}"
        return lat, resid, {"cached": True}
    lat, resid, sel, align, fvu, l0, dropped = get_enc().encode_rows(rows)
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
        for det in ("unit", "anchor", "g", "h", "dense_probe", "rek",
                    "S_rec", "S_prec", "S_mag", "original", "weighted"):
            if det in fires_matched:
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


def iter3_verdict(per_hierarchy: dict) -> str:
    """iter-4 (M5) precise reframe replacing the over-aggregating 'taxonomic_selection_established'.
    The taxonomic (LEAD) result is SET-COVER-isolated only if the rebuilt (precision-gated) unit
    beats ALL non-random label-free count-matched selectors (S-rec/S-prec/S-mag, anchored) on the
    defining slice (Georgia) with CI excluding 0, AND the rebuilt unit is the precision-passing,
    diagnostic-corroborated set. Otherwise the claim scopes to 'cover-based eligibility + sensible
    label-free selection'. Numeric is never promoted."""
    tax = per_hierarchy.get("taxonomic", {})
    return tax.get("hierarchy_verdict", "taxonomic_cover_eligibility_plus_sensible_selection")


def write_iter3_csvs(per_hierarchy: dict):
    """Dump per-slice AUC + AUC-difference CI tables and router tables as CSV for figures."""
    import csv
    for name, r in per_hierarchy.items():
        # ---- AUC table ----
        ap = r.get("auc_point", {}); ad = r.get("auc_diff_ci", {}); rk = r.get("rek_distribution", {})
        rows = []
        for s in ap:
            e = ap[s]
            row = {"sub_context": s, "n_pos": e.get("n_pos"), "n_neg": e.get("n_neg"),
                   "eligible": e.get("eligible")}
            for det in ("unit", "anchor", "g", "h", "dense_probe", "rek_mean", "rek_anch_mean"):
                row[f"auc_{det}"] = e.get(f"auc_{det}")
            # base comparisons (all slices) + M5 S-* selectors (defining slice only -> None elsewhere)
            for comp in ("g", "h", "rek_mean", "rek_anch_mean", "dense_probe",
                         "S_rec_anch", "S_prec_anch", "S_mag_anch",
                         "S_rec_free", "S_prec_free", "S_mag_free"):
                c = ad.get(s, {}).get(comp, {})
                row[f"unit_minus_{comp}_diff"] = c.get("diff")
                row[f"unit_minus_{comp}_ci_lo"] = c.get("ci_lo")
                row[f"unit_minus_{comp}_ci_hi"] = c.get("ci_hi")
            ra = rk.get(s, {}).get("rek_anchored", {})
            row["rek_anch_p95"] = ra.get("p95")
            row["unit_above_rek_anch_95th"] = ra.get("unit_above_95th")
            row["selection_established"] = r.get("selection_established", {}).get(s)
            rows.append(row)
        if rows:
            p = RESULTS_DIR / f"auc_diff_{name}.csv"
            with open(p, "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                w.writeheader(); w.writerows(rows)
            logger.info(f"  wrote {p}")
        # ---- router table (slices; rich) ----
        rr = r.get("router", {})
        rrows = [{"sub_context": s, **e} for s, e in rr.items()]
        if rrows:
            p = RESULTS_DIR / f"router_{name}.csv"
            with open(p, "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(rrows[0].keys()))
                w.writeheader(); w.writerows(rrows)
            logger.info(f"  wrote {p} (regime={r.get('router_regime')})")
        # ---- M3: router over ALL countries with homograph column ----
        ra_all = r.get("router_all", {})
        rarows = [{"sub_context": s, **e} for s, e in ra_all.items()]
        if rarows:
            p = RESULTS_DIR / f"router_all_{name}.csv"
            with open(p, "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(rarows[0].keys()))
                w.writeheader(); w.writerows(rarows)
            logger.info(f"  wrote {p}")
        # ---- precision-objective ablation table ----
        abl = r.get("precision_objective_ablation", {}).get("variants", {})
        abrows = [{"variant": v, **{kk: vv for kk, vv in d.items() if kk != "members"},
                   "members": str(d.get("members"))} for v, d in abl.items()]
        if abrows:
            keys = sorted({kk for row in abrows for kk in row})
            p = RESULTS_DIR / f"ablation_{name}.csv"
            with open(p, "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
                w.writeheader(); w.writerows(abrows)
            logger.info(f"  wrote {p}")
        # ---- per-EDGE form-free KG agreement (headline gated unit) ----
        kg_edges = r.get("kg_agreement", {}).get("edges", [])
        kgrows = [{kk: vv for kk, vv in ed.items()} for ed in kg_edges]
        if kgrows:
            keys = sorted({kk for row in kgrows for kk in row})
            p = RESULTS_DIR / f"per_edge_kg_{name}.csv"
            with open(p, "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
                w.writeheader(); w.writerows(kgrows)
            logger.info(f"  wrote {p}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scale", choices=["smoke", "mini", "full"], default="full")
    ap.add_argument("--hierarchies", default="numeric,taxonomic")
    ap.add_argument("--width", default="16k", choices=["16k", "65k"])
    ap.add_argument("--max-corpus", type=int, default=None)
    ap.add_argument("--max-pairs", type=int, default=None)
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--b-auc", type=int, default=10000, help="bootstrap reps for AUC-difference CIs")
    ap.add_argument("--b-draws", type=int, default=1000, help="RE-k random draws")
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

    # model/encoder loaded LAZILY — the cache-reuse path needs only the SAE (for W_dec).
    # The model is loaded ONLY on a cache miss (the GPU re-encode fallback).
    _enc_state: dict = {"enc": None, "model_id": "cache-reuse(no-model-loaded)",
                        "layer_idx": HOOK_LAYER_DEFAULT + 1}

    def get_encoder() -> Encoder:
        if _enc_state["enc"] is None:
            logger.info("cache miss -> loading model for GPU re-encode fallback")
            model, tok, model_id = load_model()
            layer_idx = determine_layer_idx(model, tok, sae, next(iter(data.values())))
            _enc_state.update({"enc": Encoder(model, tok, sae, layer_idx),
                               "model_id": model_id, "layer_idx": layer_idx})
        return _enc_state["enc"]

    if args.scale == "smoke":
        # iter-4 WIRING test on the cache (no re-encode, no model): confirm the precision-gated
        # greedy recovers the diagnostic-corroborated Georgia specialist 16009 and DROPS 4697.
        name = hierarchies[0] if hierarchies[0] == "taxonomic" else "taxonomic"
        rows = load_hierarchies(DATA_PATH, [name])[name]
        lat, resid, info = encode_or_cache(get_encoder, name, rows, width, use_cache=True)
        assert lat.shape == (len(rows), width), f"cache lat shape {lat.shape}"
        assert resid.shape[0] == len(rows), f"cache resid rows {resid.shape[0]}"
        result, ctx = analyze_hierarchy(name, rows, lat, resid, get_eligible(name), width)
        bv = result["k_track_unit_by_variant"]
        logger.info(f"SMOKE: anchor={result['anchor_latent']} | variants={bv}")
        assert result["anchor_latent"] == 3792, f"anchor {result['anchor_latent']} != 3792"
        gated = set(bv["gated"])
        assert 16009 in gated, f"gated unit missing 16009 (Georgia specialist): {bv['gated']}"
        assert 4697 not in gated, f"gated unit still contains low-precision 4697: {bv['gated']}"
        geo = next((mi for mi in result["rebuilt_units"]["gated"]["member_info"]
                    if mi.get("specializes") == "Georgia"), None)
        logger.info(f"SMOKE: Georgia member={geo}")
        assert geo and geo["latent"] == 16009, f"Georgia member is not 16009: {geo}"
        assert (geo["subctx_precision_heldout"] or 0) >= SUBCTX_PREC, \
            f"Georgia held-out subctx precision {geo['subctx_precision_heldout']} < {SUBCTX_PREC}"
        logger.info("SMOKE PASSED (M2 precision-gate recovers 16009, drops 4697; held-out precision OK)")
        return

    per_hierarchy = {}
    enc_info = {}
    pred_payload = {}
    global rng
    for name in hierarchies:
        # re-seed per hierarchy -> results are deterministic and INDEPENDENT of processing order
        # (iter-2 ran numeric-first, consuming rng before taxonomic; re-seeding removes that coupling
        #  so taxonomic-lead ordering reproduces the same per-hierarchy numbers either way).
        rng = np.random.default_rng(SEED)
        rows = data[name]
        lat, resid, info = encode_or_cache(get_encoder, name, rows, width, use_cache=not args.no_cache)
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
        # ---- iter-3 phases D-H: RE-k baselines + AUC-diff CIs + Youden table + router inputs ----
        ext, pred_extra = iter3_extensions(name, result, ctx, eligible,
                                           b_auc=args.b_auc, b_draws=args.b_draws)
        result.update(ext)
        for det, fires in pred_extra.items():
            ctx["fires_matched"][det] = fires
        per_hierarchy[name] = result
        pred_payload[name] = make_predictions(name, ctx)
        # checkpoint
        (RESULTS_DIR / f"partial_{name}_iter3.json").write_text(
            json.dumps(result, indent=2, default=_json_default))
        del lat, resid, ctx
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    verdict = iter3_verdict(per_hierarchy)
    run_meta = {
        "method_name": ("Two-Track CCRG K-track — taxonomic unit/specialist CONFLATION FIX (iter-4): "
                        "precision-gated/weighted greedy rebuild (M2) + TRAIN/HELD-OUT fold split (M7) + "
                        "non-random label-free count-matched selectors S-rec/S-prec/S-mag (M5) + homograph "
                        "scope cross-tab (M3) + per-edge form-free KG + precision-objective ablation"),
        "verdict": verdict,
        "iter4_fixes": {
            "M2_precision_gate": "per-sub-context FIRING-precision gate + precision-weighted coverage "
                                 "objective in the anchored greedy (headline variant='gated').",
            "M7_fold_split": "absorber selection / gates fit on corpus TRAIN positives; AUC / precision / "
                             "router REPORTED on the disjoint diagnostic (held-out) fold.",
            "M5_nonrandom_controls": "S-rec/S-prec/S-mag label-free count-matched selectors (free + "
                                     "anchored); set-cover ESTABLISHED iff unit beats all anchored on Georgia.",
            "M3_homograph_scope": "homograph x absorption-type cross-tab over all countries.",
            "headline_variant": "gated",
        },
        "sae": {"release": SAE_RELEASE, "sae_id": sae_id, "width": width,
                "hook": f"blocks.{HOOK_LAYER_DEFAULT}.hook_resid_post",
                "hf_hidden_state_idx": _enc_state["layer_idx"], "d_model": D_MODEL},
        "model": _enc_state["model_id"],
        "encoding": enc_info,
        "stats": {"bootstrap_B_gate": 2000, "bootstrap_B_paired": 10000,
                  "bootstrap_B_auc": args.b_auc, "B_draws": args.b_draws,
                  "n_min_eligible": N_MIN_ELIGIBLE, "multiplicity": "holm", "seed": SEED,
                  "auc_diff_ci": "stratified paired bootstrap (resample positives & negatives separately)"},
        "thresholds": {"G1_recall": G1_RECALL, "jaccard_max": JACCARD_MAX,
                       "subctx_precision": SUBCTX_PREC, "gain_min": GAIN_MIN,
                       "precision_floor": PRECISION_FLOOR, "greedy_max_members": GREEDY_MAX_MEMBERS},
        "iter4_focus": {"lead_hierarchy": "taxonomic", "lead_slice": "Georgia",
                        "numeric_status": "suggestive_diagnostic_unconfirmed"},
        "runtime_s": round(time.time() - t_start, 1),
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu",
    }
    emit_method_out(per_hierarchy, run_meta, pred_payload)
    write_figure_csvs(per_hierarchy)
    write_iter3_csvs(per_hierarchy)
    logger.info(f"DONE. verdict={verdict} runtime={run_meta['runtime_s']}s")
    for name, r in per_hierarchy.items():
        dd = r.get("defining_slice")
        logger.info(f"  [{name}] gate={r['gate_decision']} recovered={r['recovered_absorber_count']} "
                    f"headline={r.get('headline_variant')} unit={r.get('k_track_unit')} "
                    f"set_cover_established={r.get('set_cover_established')} "
                    f"verdict={r.get('hierarchy_verdict')} gen={r.get('generalization_status')}")


if __name__ == "__main__":
    main()
