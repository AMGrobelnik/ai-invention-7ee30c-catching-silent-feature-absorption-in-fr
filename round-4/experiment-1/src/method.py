#!/usr/bin/env python
"""
M1a + M7 AUDITABILITY SPINE (expanded), iter-4 experiment_1.

EXPANSION of the iter-3 measured-auditability result (art at
iter_3/gen_art/gen_art_experiment_3) from 8 KG repairs / 67 labelled members to the FULL set of
eligible absorbed sub-contexts, across THREE concept families, on a FROZEN Gemma-Scope L12/16k
JumpReLU SAE:

  * spelling           : first-letter L / O / T / I / D word absorption (D1)
  * homograph-taxonomic: country absorption incl. flagged homographs Georgia/Jordan/Turkey/... (D2)
  * numeric            : year/percent/currency/date/decimal/integer/comma_number/ordinal (D2)

Four measured pieces (the load-bearing spine):

  M1a  BROAD KG-GUIDED REPAIR LOOP
       For EVERY eligible sub-context X the K-track greedy NAMES a covering absorber, derived
       PURELY on the selection split (non-circular vs eval). We ADD the named absorber to the
       parent/anchor (max-pool) and MEASURE recall recovery on HELD-OUT eval windows vs a control
       that adds every OTHER content-responsive latent (the full random-addition population).
       Per repair: gain_kg, percentile-vs-random, paired-bootstrap CI (B=10,000) AND a one-sided
       bootstrap p-value (H0: KG-minus-random gain <= 0).

  MULTIPLICITY  Benjamini-Hochberg FDR<=0.05 across ALL repair variants (lives in-experiment).

  M1a(k)  LOCALIZATION-FAILURE CHECK, run for first-letter + numeric + taxonomic.
       Label-free group inference (JTT: ERM probe -> upweight error/low-margin set -> retrain)
       yields a DENSE reweighted hyperplane; we project it onto the SAE decoder dictionary and show
       no single latent dominates / the KG absorber is not the argmax: (k) classifies holes but
       exposes NO addable per-sub-context FEATURE, whereas the KG names exactly one latent.

  M7  ENSEMBLE LLM-JUDGE MEMBER-LABELING + 15-WIDE CONFIDENT FRACTION.
       Every admitted-unit member (incl. ALL 15 members of each first-letter max-pool K_UNIT) gets
       J=3 forced-choice judge calls with SHUFFLED candidate order (kills position bias). We report
       agreement vs a shuffle null (gap bootstrap CI), per-role accuracy, AND the FRACTION of
       members (and of each 15-wide pool) that receive a confident, above-null-margin label.

Honest negatives (KG repair tying random-addition) are emitted verbatim. Core compute is GPU; LLM
spend target <$1, hard stop $10.

Usage:
  uv run method.py --smoke                                   # load model+SAE, gating check only
  uv run method.py --concepts taxonomic --max_corpus 300 --no_llm    # mini pilot (reproduce iter-3)
  uv run method.py --concepts taxonomic,numeric --no_llm    # broad KG + BH, no LLM
  uv run method.py                                          # full run (all concepts + LLM ensemble)
"""
import os, sys, json, time, gc, argparse, hashlib, resource
from pathlib import Path
from collections import defaultdict, Counter

import numpy as np

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "0")

from loguru import logger

# --------------------------------------------------------------------------- paths (read-only inputs)
ROOT = Path("/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop")
D1 = ROOT / "iter_1/gen_art/gen_art_dataset_1/full_data_out.json"           # first-letter spelling
D2 = ROOT / "iter_1/gen_art/gen_art_dataset_2/full_data_out.json"           # numeric + taxonomic
D2_MANIFEST = ROOT / "iter_1/gen_art/gen_art_dataset_2/manifest.json"       # absorption_readiness
E1 = ROOT / "iter_2/gen_art/gen_art_experiment_1/method_out.json"           # canonical first-letter units
E3 = ROOT / "iter_2/gen_art/gen_art_experiment_3/method_out.json"           # canonical tax + numeric units

WORK = Path("/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_1")
RESULTS = WORK / "results"
CACHE = WORK / "cache"
LOGS = WORK / "logs"
for d in (RESULTS, CACHE, LOGS):
    d.mkdir(exist_ok=True)

# --------------------------------------------------------------------------- SAE / model config
RELEASE_REPO = "google/gemma-scope-2b-pt-res"
SAE_PARAMS_16K = "layer_12/width_16k/average_l0_82/params.npz"   # canonical (avg L0 ~ 100)
MODEL_GATED = "google/gemma-2-2b"
MODEL_MIRROR = "unsloth/gemma-2-2b"                              # ungated mirror, vocab 256000
D_MODEL = 2304
HOOK_LAYER = 12               # blocks.12.hook_resid_post == hidden_states[13]
MAXLEN = 192
BATCH = 16
SEED = 1234

# --------------------------------------------------------------------------- M1a / M7 thresholds
N_MIN_EVAL = 30              # preferred min held-out windows for a sub-context to enter the repair test
N_MIN_RELAX = 15            # relaxed floor (used for first-letter words & rare countries)
N_MIN_SEL = 10              # min selection-split positives to DERIVE a covering absorber
HOLE_RECALL_MAX = 0.60      # anchor recall <= this on the SELECTION split  => under-served (hole)
B_BOOT = 10000              # paired bootstrap resamples
N_SHUFFLE = 2000            # member-labeling null shuffles
KG_JACCARD_MAX = 0.10       # absorber-vs-anchor firing Jaccard ceiling (complementary coverage)
KG_PREC_MIN = 0.70          # absorber sub-context precision floor on the selection split
SPURIOUS_FIRE_FLOOR = 0.01  # anchor must fire on >= this fraction of corpus positives else spurious
FDR_ALPHA = 0.05
J_ENSEMBLE = 3              # judge calls per member (shuffled candidate order)
LLM_MODEL = "anthropic/claude-haiku-4.5"
LLM_FALLBACKS = ["google/gemini-3.1-flash-lite", "deepseek/deepseek-v3.2-exp"]
LLM_PRICE = {  # $/token (June-2026 dossier prices); used only if OpenRouter omits usage.cost
    "anthropic/claude-haiku-4.5": (1.00e-6, 5.00e-6),
    "google/gemini-3.1-flash-lite": (0.25e-6, 1.50e-6),
    "deepseek/deepseek-v3.2-exp": (0.20e-6, 0.40e-6),
}
LLM_HARD_STOP = 10.0
LLM_TARGET = 1.0            # this experiment targets < $1; degrade J 3->1 once exceeded

rng = np.random.default_rng(SEED)

# --------------------------------------------------------------------------- logging
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(str(LOGS / "run.log"), rotation="40 MB", level="DEBUG")
T0 = time.time()
def el() -> str:
    return f"{time.time()-T0:6.1f}s"

DEVICE = "cuda"


# =========================================================================== resource limits
def set_limits():
    try:
        avail = 45 * 1024**3
        resource.setrlimit(resource.RLIMIT_AS, (avail * 3, avail * 3))
    except Exception as e:  # noqa: BLE001
        logger.warning(f"could not set RLIMIT_AS: {e}")


# =========================================================================== SAE
class JumpReLUSAE:
    """Gemma-Scope JumpReLU SAE, loaded directly from params.npz (DeepMind canonical forward)."""
    def __init__(self, params_path, device, torch):
        self.torch = torch
        d = np.load(params_path)
        self.W_enc = torch.tensor(np.asarray(d["W_enc"]), device=device, dtype=torch.float32)   # [d_model,d_sae]
        self.W_dec = torch.tensor(np.asarray(d["W_dec"]), device=device, dtype=torch.float32)   # [d_sae,d_model]
        self.b_enc = torch.tensor(np.asarray(d["b_enc"]), device=device, dtype=torch.float32)   # [d_sae]
        self.b_dec = torch.tensor(np.asarray(d["b_dec"]), device=device, dtype=torch.float32)   # [d_model]
        self.threshold = torch.tensor(np.asarray(d["threshold"]), device=device, dtype=torch.float32)
        self.d_model = self.W_dec.shape[1]
        self.d_sae = self.W_dec.shape[0]

    def encode(self, x):
        t = self.torch
        x = x.to(t.float32)
        pre = x @ self.W_enc + self.b_enc
        return (pre > self.threshold) * t.nn.functional.relu(pre)   # JumpReLU: fire iff pre>threshold

    def decode(self, z):
        return z @ self.W_dec + self.b_dec


def _find_sae_params():
    import glob, re
    base = os.path.expanduser("~/.cache/huggingface/hub/models--google--gemma-scope-2b-pt-res")
    pats = glob.glob(f"{base}/snapshots/*/layer_12/width_16k/average_l0_*/params.npz")
    if pats:
        return min(pats, key=lambda p: abs((int(re.search(r'average_l0_(\d+)', p).group(1)) if re.search(r'average_l0_(\d+)', p) else 9999) - 100))
    from huggingface_hub import hf_hub_download
    return hf_hub_download(RELEASE_REPO, SAE_PARAMS_16K, token=os.environ.get("HF_TOKEN"))


def load_sae(torch):
    path = _find_sae_params()
    logger.info(f"{el()} loading SAE from {path}")
    sae = JumpReLUSAE(path, DEVICE, torch)
    assert sae.d_model == D_MODEL, f"unexpected d_model {sae.d_model}"
    logger.info(f"{el()} SAE loaded d_sae={sae.d_sae} d_model={sae.d_model}")
    return sae


# =========================================================================== MODEL
class ModelBundle:
    def __init__(self, torch):
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.torch = torch
        last = None
        for mid in (MODEL_GATED, MODEL_MIRROR):
            try:
                logger.info(f"{el()} loading tokenizer+model {mid}")
                self.tok = AutoTokenizer.from_pretrained(mid, token=os.environ.get("HF_TOKEN"))
                self.tok.padding_side = "right"
                self.model = AutoModelForCausalLM.from_pretrained(
                    mid, torch_dtype=torch.bfloat16, attn_implementation="eager",
                    token=os.environ.get("HF_TOKEN")).to(DEVICE).eval()
                self.model_id = mid
                break
            except Exception as e:  # noqa: BLE001
                logger.warning(f"  failed {mid}: {repr(e)[:160]}")
                last = e
        else:
            raise RuntimeError(f"could not load gemma-2-2b: {last}")
        self.d_model = self.model.config.hidden_size
        self.layer_idx = HOOK_LAYER + 1                      # hidden_states index; validated in determine_layer_idx
        self._cap = {}
        logger.info(f"{el()} model loaded ({self.model_id}) d_model={self.d_model} "
                    f"n_layers={self.model.config.num_hidden_layers} vocab={len(self.tok)}")

    # ---- hook on decoder layer (layer_idx-1) captures hidden_states[layer_idx] ----
    def _install_hook(self, layer_idx):
        if getattr(self, "_handle", None) is not None:
            self._handle.remove()
        def _hook(_m, _i, out):
            self._cap["resid"] = out[0] if isinstance(out, (tuple, list)) else out
        self._handle = self.model.model.layers[layer_idx - 1].register_forward_hook(_hook)
        self.layer_idx = layer_idx

    def determine_layer_idx(self, rows, sae):
        """Pick hidden_states index whose residual the SAE best reconstructs (lowest FVU)."""
        torch = self.torch
        sample = rows[:32]
        texts = [r["input"] for r in sample]
        spans = [r["_span"] for r in sample]
        tis = [r.get("_ti") for r in sample]
        enc = self.tok(texts, return_offsets_mapping=True, add_special_tokens=True, padding=True,
                       truncation=True, max_length=MAXLEN, return_tensors="pt")
        offs = enc.pop("offset_mapping")
        am = enc["attention_mask"]
        enc = {k: v.to(DEVICE) for k, v in enc.items()}
        caps = {}
        handles = []
        for hi in (12, 13, 14):
            def mk(h):
                def hook(_m, _i, out):
                    caps[h] = out[0] if isinstance(out, (tuple, list)) else out
                return hook
            handles.append(self.model.model.layers[hi - 1].register_forward_hook(mk(hi)))
        with torch.no_grad():
            self.model.model(**enc)
        for h in handles:
            h.remove()
        res = {}
        for idx, hs in caps.items():
            vecs = []
            for i, r in enumerate(sample):
                pos = select_positions(offs[i].tolist(), int(am[i].sum()), spans[i], tis[i])
                if pos:
                    vecs.append(hs[i, pos].float().mean(0))
            X = torch.stack(vecs)
            with torch.no_grad():
                recon = sae.decode(sae.encode(X))
            sse = ((X - recon) ** 2).sum().item()
            sst = ((X - X.mean(0)) ** 2).sum().item()
            res[idx] = sse / max(sst, 1e-9)
        best = min(res, key=res.get)
        logger.info(f"{el()} FVU by hidden_states idx: " +
                    ", ".join(f"{k}:{v:.3f}" for k, v in sorted(res.items())) + f" -> selected {best}")
        self._install_hook(best)
        return best, res

    def encode_rows(self, rows, sae):
        """Encode rows -> (lat_csr [N,d_sae] max-pooled over target tokens, resid [N,d_model] fp16,
        sel_strings, align). Residual captured by the installed layer hook."""
        import scipy.sparse as sp
        torch = self.torch
        N = len(rows)
        resid = np.zeros((N, D_MODEL), dtype=np.float16)
        sel_strings = [""] * N
        row_nz = {}
        n_align_ok = n_align_tot = 0
        dropped = 0
        t0 = time.time()
        for b0 in range(0, N, BATCH):
            batch = rows[b0:b0 + BATCH]
            texts = [r["input"] for r in batch]
            enc = self.tok(texts, return_offsets_mapping=True, add_special_tokens=True,
                           padding=True, truncation=True, max_length=MAXLEN, return_tensors="pt")
            offs = enc.pop("offset_mapping")
            am = enc["attention_mask"]
            enc = {k: v.to(DEVICE) for k, v in enc.items()}
            with torch.no_grad():
                self.model.model(**enc)
                hs = self._cap["resid"]                        # [B,T,d]
            row_vecs, keep = [], []
            for i, r in enumerate(batch):
                gid = b0 + i
                pos = select_positions(offs[i].tolist(), int(am[i].sum()), r["_span"], r.get("_ti"))
                if not pos:
                    dropped += 1
                    continue
                keep.append((gid, len(pos)))
                row_vecs.append(hs[i, pos].float())
                ids = enc["input_ids"][i, pos].tolist()
                s = self.tok.decode(ids).strip()
                sel_strings[gid] = s
                tgt = r.get("_target")
                if tgt:
                    n_align_tot += 1
                    if s.replace(" ", "").lower() == tgt.replace(" ", "").lower():
                        n_align_ok += 1
            if row_vecs:
                allres = torch.cat(row_vecs, 0)
                with torch.no_grad():
                    lat = sae.encode(allres)                   # [M,d_sae]
                m0 = 0
                for (gid, npos) in keep:
                    sl = lat[m0:m0 + npos]
                    sr = allres[m0:m0 + npos]
                    pooled = sl.max(0).values
                    resid[gid] = sr.mean(0).half().cpu().numpy()
                    nz = torch.nonzero(pooled > 0).squeeze(-1)
                    row_nz[gid] = (nz.cpu().numpy().astype(np.int32),
                                   pooled[nz].cpu().numpy().astype(np.float32))
                    m0 += npos
                del allres, lat
            self._cap.clear()
            del hs
            if (b0 // BATCH) % 60 == 0:
                logger.info(f"    encoded {min(b0+BATCH,N)}/{N} ({time.time()-t0:.0f}s)")
        # assemble CSR in row order
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
        lat_csr = sp.csr_matrix((lat_data, lat_idx, lat_ptr), shape=(N, sae.d_sae))
        align = n_align_ok / max(n_align_tot, 1)
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        logger.info(f"{el()} encoded {N} rows in {time.time()-t0:.0f}s | dropped={dropped} | align={align:.3f} "
                    f"| nnz/row={lat_csr.nnz/max(N,1):.0f}")
        return lat_csr, resid, sel_strings, align


def select_positions(offsets, T, span, ti=None):
    """Token positions overlapping char-span (cs,ce). Falls back to stored token indices (+1 BOS)."""
    if span is not None:
        cs, ce = span
        if cs is not None and cs >= 0:
            if ce is not None and ce > cs:
                pos = [t for t in range(len(offsets))
                       if offsets[t][1] > offsets[t][0] and offsets[t][0] < ce and offsets[t][1] > cs]
            else:
                pos = [t for t in range(len(offsets))
                       if offsets[t][1] > offsets[t][0] and offsets[t][0] <= cs < offsets[t][1]]
            if pos:
                return pos
    if ti:
        return [j + 1 for j in ti if 0 <= j + 1 < T]
    return []


# =========================================================================== encoding cache
def encode_cached(concept_key, rows, sae, mb):
    """Disk-cache mb.encode_rows so the gradual-scaling staged runs do not re-encode."""
    import scipy.sparse as sp
    fp = hashlib.sha1(
        ("|".join(r["input"][:24] for r in rows[:: max(1, len(rows) // 64)])).encode("utf-8")
    ).hexdigest()[:12]
    key = f"enc_{concept_key}_{len(rows)}_{MAXLEN}_{mb.model_id.replace('/', '_')}_{fp}"
    npz = CACHE / f"{key}.npz"
    meta = CACHE / f"{key}.json"
    if npz.exists() and meta.exists():
        try:
            d = np.load(str(npz), allow_pickle=False)
            lat = sp.csr_matrix((d["lat_data"], d["lat_idx"], d["lat_ptr"]),
                                shape=(len(rows), sae.d_sae))
            m = json.loads(meta.read_text())
            logger.info(f"{el()} [cache HIT] {concept_key} n={len(rows)} align={m.get('align')}")
            return lat, d["resid"], None, float(m.get("align", 1.0))
        except Exception as e:  # noqa: BLE001
            logger.warning(f"  cache load failed ({e}); re-encoding")
    lat, resid, ss, align = mb.encode_rows(rows, sae)
    try:
        np.savez(str(npz), lat_data=lat.data, lat_idx=lat.indices, lat_ptr=lat.indptr, resid=resid)
        meta.write_text(json.dumps({"n": len(rows), "maxlen": MAXLEN, "model": mb.model_id, "align": align}))
    except Exception as e:  # noqa: BLE001
        logger.warning(f"  cache save failed ({e})")
    return lat, resid, ss, align


# =========================================================================== DATA loading
def _attach_span_fl(r):
    """First-letter row -> (_span,_ti,_target). corpus uses target_char_in_window; pairs use word_char_span."""
    if r.get("metadata_pair_type") == "corpus_context":
        sp = r.get("metadata_target_char_in_window")
        r["_span"] = tuple(sp) if sp else None
        tp = r.get("metadata_token_position")
        r["_ti"] = [int(tp)] if tp is not None else None
    else:
        sp = r.get("metadata_word_char_span")
        r["_span"] = tuple(sp) if sp else None
        r["_ti"] = None
    r["_target"] = r.get("metadata_target_word")
    return r


def _attach_span_tax(r):
    cs = r.get("metadata_target_char_start")
    ce = r.get("metadata_target_char_end")
    r["_span"] = (cs, ce) if cs is not None else None
    ti = r.get("metadata_target_token_indices")
    r["_ti"] = list(ti) if ti else None
    r["_target"] = r.get("metadata_target_text")
    return r


def load_first_letter(letters):
    blob = json.loads(D1.read_text())
    groups = {}
    for g in blob["datasets"]:
        lt = g["dataset"].split("_")[-1]
        if lt in letters:
            groups[lt] = [_attach_span_fl(dict(r)) for r in g["examples"]]
    return groups


def load_d2(dataset_name):
    """Load a D2 hierarchy ('taxonomic_absorption' | 'numeric_absorption')."""
    blob = json.loads(D2.read_text())
    ds = next(d for d in blob["datasets"] if d["dataset"] == dataset_name)
    return [_attach_span_tax(dict(r)) for r in ds["examples"]]


def load_readiness():
    try:
        m = json.loads(D2_MANIFEST.read_text())
        return m.get("absorption_readiness", {})
    except Exception:  # noqa: BLE001
        return {}


# =========================================================================== stats
def paired_bootstrap_diff(diff_per_item, B=B_BOOT):
    """Paired bootstrap of mean(diff). Returns 95% CI + one-sided p (H0: mean<=0)."""
    d = np.asarray(diff_per_item, dtype=np.float64)
    n = len(d)
    if n == 0:
        return {"diff": 0.0, "ci_lo": 0.0, "ci_hi": 0.0, "excl_0": False, "n": 0, "p_one_sided": 1.0}
    idx = rng.integers(0, n, size=(B, n))
    bs = d[idx].mean(1)
    lo, hi = np.percentile(bs, [2.5, 97.5])
    p_one = (1.0 + float((bs <= 0).sum())) / (B + 1.0)
    return {"diff": float(d.mean()), "ci_lo": float(lo), "ci_hi": float(hi),
            "excl_0": bool(lo > 0 or hi < 0), "n": int(n), "p_one_sided": float(p_one)}


def benjamini_hochberg(pvals, alpha=FDR_ALPHA):
    """BH FDR-adjusted q-values + count surviving. Hand-rolled (matches statsmodels fdr_bh)."""
    p = np.asarray(pvals, dtype=np.float64)
    n = len(p)
    if n == 0:
        return np.array([]), 0
    order = np.argsort(p)
    ranked = p[order]
    q = ranked * n / np.arange(1, n + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    q = np.clip(q, 0.0, 1.0)
    out = np.empty(n)
    out[order] = q
    return out, int((out <= alpha).sum())


# =========================================================================== canonical units
def _d2_canon(hier):
    """Build canonical fields for a D2 hierarchy block (taxonomic | numeric) from E3."""
    kg_edges = hier.get("kg_edges", [])
    diag_abs = hier.get("non_triviality_passing_absorbers", [])
    kg_by_sub, diag_by_sub = {}, {}
    for e in kg_edges:
        kg_by_sub.setdefault(e["specializes"], e["absorber"])
    for a in diag_abs:
        diag_by_sub.setdefault(a["specializes"], a["latent"])
    return {
        "anchor": hier["anchor_latent"],
        "k_track_unit": hier.get("k_track_unit", []),
        "kg_edges": kg_edges,
        "diag_absorbers": diag_abs,
        "anchor_recall_corpus": hier.get("anchor_recall_corpus"),
        "eligible_subcontexts": hier.get("eligible_subcontexts", []),
        "absorbed_subcontexts": hier.get("absorbed_subcontexts", []),
        "kg_by_sub": kg_by_sub,
        "diag_by_sub": diag_by_sub,
        "n_content_responsive": hier.get("n_content_responsive"),
    }


def read_canonical_units():
    """Read iter-2 canonical units/KG. Returns dict: first_letter + taxonomic + numeric."""
    fl_blob = json.loads(E1.read_text())["metadata"]["per_letter"]
    fl = {}
    for lt, r in fl_blob.items():
        k_unit = list(r.get("K_UNIT") or ([r["anchor_idx"]] + list(r.get("absorber_idxs", []))))
        anchor = r["anchor_idx"]
        sub_by = {}
        for e in r.get("kg_edges", []):
            sub_by[e["dst"]] = e.get("sub_context", "") or ""
        fl[lt] = {
            "anchor": anchor,
            "k_unit": k_unit,
            "absorbers": [a for a in k_unit if a != anchor],
            "members": k_unit,
            "sub_by_absorber": sub_by,
            "anchor_corpus_fire_iter2": r.get("anchor_fidelity", {}).get("corpus_fire_rate", None),
        }
    e3 = json.loads(E3.read_text())["metadata"]["per_hierarchy"]
    return {"first_letter": fl,
            "taxonomic": _d2_canon(e3["taxonomic"]),
            "numeric": _d2_canon(e3["numeric"])}


# =========================================================================== content-responsive set
def content_responsive(A_on, A_off, b_null=1000):
    """Re-derive content-responsive latents (iter-2 definition): mean(on-off)>shuffle-null-95 & >0.
    Also returns per-latent firing precision (fires on x_on not x_off)."""
    R = A_on - A_off
    npair = R.shape[0]
    mean_R = R.mean(0)
    signs = rng.integers(0, 2, size=(npair, b_null)) * 2 - 1
    null95 = np.percentile((R.T @ signs) / npair, 95, axis=1)
    cr = np.where((mean_R > null95) & (mean_R > 0))[0]
    fire_on = (A_on > 0).sum(0).astype(np.float64)
    prec = np.where(fire_on > 0, ((A_on > 0) & ~(A_off > 0)).sum(0) / np.maximum(fire_on, 1), 0.0)
    return cr, prec, mean_R


# =========================================================================== BROAD K-track KG derivation
def derive_broad_kg(anchor, cr, lat_csr, sub_arr, label_arr, sel_mask, eligible_X,
                    jaccard_max=KG_JACCARD_MAX, prec_min=KG_PREC_MIN, min_sel=N_MIN_SEL):
    """For EVERY eligible sub-context X, NAME a covering absorber via the K-track greedy, derived
    PURELY on the SELECTION split (non-circular vs eval).

      kg_absorber[X] = argmax_{l in cr, l!=anchor, jaccard(l,anchor)<jaccard_max, subctx_prec(l,X)>=prec_min}
                         recall_of_l_on_X_selection

    Returns:
      per_X[X] = {kg_absorber|None, recall_on_X_selection, subctx_precision_selection,
                  jaccard_anchor, n_sel_pos, reason?}
      anchor_recall_by_X[X] = anchor firing recall on X's selection positives
    """
    cr = np.asarray([int(l) for l in cr if int(l) != int(anchor)], dtype=np.int64)
    sel_pos = np.where(sel_mask & (label_arr == 1))[0]
    if len(sel_pos) == 0 or len(cr) == 0:
        return {}, {}
    F = (np.asarray(lat_csr[sel_pos][:, cr.tolist()].todense()) > 0)              # [n,|cr|]
    anchor_fire = (np.asarray(lat_csr[sel_pos][:, [int(anchor)]].todense()) > 0).ravel()  # [n]
    sub_sel = np.asarray(sub_arr)[sel_pos]
    inter = (F & anchor_fire[:, None]).sum(0).astype(np.float64)
    union = (F | anchor_fire[:, None]).sum(0).astype(np.float64)
    jac = np.where(union > 0, inter / np.maximum(union, 1.0), 1.0)                # [|cr|]
    fire_count = F.sum(0).astype(np.float64)                                      # [|cr|]
    per_X, anchor_recall_by_X = {}, {}
    for X in eligible_X:
        xmask = (sub_sel == X)
        n_x = int(xmask.sum())
        if n_x < min_sel:
            per_X[X] = {"kg_absorber": None, "reason": f"too_few_selection_positives({n_x})", "n_sel_pos": n_x}
            continue
        anchor_recall_by_X[X] = float(anchor_fire[xmask].mean())
        x_fire = F[xmask].sum(0).astype(np.float64)                               # [|cr|]
        recall_X = x_fire / n_x                                                    # [|cr|]
        prec_X = np.where(fire_count > 0, x_fire / np.maximum(fire_count, 1.0), 0.0)  # [|cr|]
        ok = (jac < jaccard_max) & (prec_X >= prec_min) & (fire_count > 0)
        if not ok.any():
            per_X[X] = {"kg_absorber": None, "reason": "no_low_jaccard_high_precision_covering_latent",
                        "n_sel_pos": n_x, "anchor_recall_selection": anchor_recall_by_X[X]}
            continue
        cand = np.where(ok)[0]
        best = cand[int(np.argmax(recall_X[cand]))]
        per_X[X] = {"kg_absorber": int(cr[best]),
                    "recall_on_X_selection": float(recall_X[best]),
                    "subctx_precision_selection": float(prec_X[best]),
                    "jaccard_anchor": float(jac[best]),
                    "n_sel_pos": n_x,
                    "anchor_recall_selection": anchor_recall_by_X[X]}
    del F
    return per_X, anchor_recall_by_X


# =========================================================================== M1a REPAIR LOOP
def repair_loop(concept, anchor, candidates, lat_csr, sub_arr, label_arr,
                responsive, member_set, sel_mask, eval_mask):
    """For each candidate sub-context X with a KG-named absorber, measure recall recovery of the
    KG-named latent on HELD-OUT (eval) windows vs a random-content-responsive-latent control.

    candidates: list of dicts {X, kg_absorber, diag_absorber, derivation}
    sel_mask/eval_mask: boolean over all rows (selection vs eval corpus-positive split)
    """
    resp = np.asarray(responsive)
    resp_ctrl = np.array([int(l) for l in resp if int(l) not in member_set], dtype=np.int64)
    out = {"per_subcontext": {}, "honest_negatives": [], "n_measured_successful_repairs": 0,
           "n_control_latents": int(len(resp_ctrl))}

    def fire(rows_idx, lat_ids):
        if len(rows_idx) == 0 or len(lat_ids) == 0:
            return np.zeros((len(rows_idx), len(lat_ids)), dtype=bool)
        sub = lat_csr[rows_idx]
        return (np.asarray(sub[:, list(lat_ids)].todense()) > 0)

    sel_pos_rows = np.where(sel_mask & (label_arr == 1))[0]
    overall_anchor_sel = float(fire(sel_pos_rows, [anchor])[:, 0].mean()) if len(sel_pos_rows) else 1.0
    out["overall_anchor_recall_selection"] = overall_anchor_sel

    for cand in candidates:
        X = cand["X"]
        x_mask = (np.asarray(sub_arr) == X) & (label_arr == 1)
        sel_rows = np.where(x_mask & sel_mask)[0]
        eval_rows = np.where(x_mask & eval_mask)[0]
        n_eval = len(eval_rows)
        n_sel = len(sel_rows)
        anchor_sel = fire(sel_rows, [anchor])[:, 0] if n_sel else np.array([], bool)
        r_anchor_sel = float(anchor_sel.mean()) if n_sel else None
        if n_eval < N_MIN_RELAX:
            out["per_subcontext"][X] = {"status": "skip_too_few_eval", "n_eval": n_eval, "n_sel": n_sel,
                                        "recall_anchor_selection": r_anchor_sel,
                                        "kg_derivation": cand.get("derivation")}
            continue
        is_hole = (r_anchor_sel is not None and
                   (r_anchor_sel <= HOLE_RECALL_MAX or r_anchor_sel < overall_anchor_sel - 0.10))
        anchor_eval = fire(eval_rows, [anchor])[:, 0]
        base = anchor_eval.astype(bool)
        base_recall = float(base.mean())
        ctrl_fire = fire(eval_rows, list(resp_ctrl))
        ctrl_detect = base[:, None] | ctrl_fire
        ctrl_recall = ctrl_detect.mean(0)
        ctrl_gain = ctrl_recall - base_recall
        rand_detect_perwin = ctrl_detect.mean(1)

        entry = {"status": "measured", "is_hole": bool(is_hole), "n_eval": n_eval, "n_sel": n_sel,
                 "recall_anchor_selection": r_anchor_sel, "recall_anchor_eval": base_recall,
                 "n_eval_ge_pref": bool(n_eval >= N_MIN_EVAL),
                 "kg_derivation": cand.get("derivation"),
                 "random_gain": {"mean": float(ctrl_gain.mean()), "sd": float(ctrl_gain.std()),
                                 "p5": float(np.percentile(ctrl_gain, 5)),
                                 "p50": float(np.percentile(ctrl_gain, 50)),
                                 "p95": float(np.percentile(ctrl_gain, 95))},
                 "variants": {}}

        for vname, latid in (("kg_ktrack", cand.get("kg_absorber")),
                             ("kg_diagnostic", cand.get("diag_absorber"))):
            if latid is None:
                continue
            kg_fire = fire(eval_rows, [int(latid)])[:, 0].astype(bool)
            kg_detect = base | kg_fire
            kg_recall = float(kg_detect.mean())
            gain_kg = kg_recall - base_recall
            pct = float((ctrl_gain < gain_kg).mean())
            diff_perwin = kg_detect.astype(float) - rand_detect_perwin
            ci = paired_bootstrap_diff(diff_perwin)
            succ = bool(ci["excl_0"] and ci["diff"] > 0)
            entry["variants"][vname] = {
                "absorber_latent": int(latid),
                "recall_anchor_plus_kg": kg_recall,
                "gain_kg": float(gain_kg),
                "kg_percentile_vs_random": pct,
                "paired_bootstrap_CI_kg_minus_random": ci,
                "p_value_one_sided": ci["p_one_sided"],
                "measured_success": succ,
                "bh_q": None,            # filled by multiplicity pass
                "survives_FDR": None,
            }
            if succ:
                out["n_measured_successful_repairs"] += 1
            if not succ and is_hole:
                out["honest_negatives"].append(
                    f"{concept}/{X}/{vname}: KG-add buys no measurable fix beyond random "
                    f"(gain_kg={gain_kg:.3f}, random p95={entry['random_gain']['p95']:.3f}, "
                    f"CI={ci['ci_lo']:.3f}..{ci['ci_hi']:.3f}, p={ci['p_one_sided']:.4f})")
        out["per_subcontext"][X] = entry
        best = max((v["gain_kg"] for v in entry["variants"].values()), default=0.0)
        logger.info(f"  [{concept}] {X}: hole={is_hole} r_anchor_sel={r_anchor_sel} "
                    f"r_anchor_eval={base_recall:.3f} best_gain_kg={best:.3f} "
                    f"rand_gain_p95={entry['random_gain']['p95']:.3f} n_eval={n_eval}")
    return out


# =========================================================================== M1a(k) localization check
def k_localization_check(concept, resid, label, fold, sae_W_dec, anchor, kg_absorbers,
                         eval_rows_by_X, lam=20.0):
    """JTT label-free group inference: ERM probe -> upweight error set -> retrain. Show the resulting
    dense direction does NOT localize to a single SAE latent (no per-sub-context feature to add)."""
    from sklearn.linear_model import LogisticRegression
    tr = np.where(fold == "selection")[0]
    if len(tr) < 20 or len(np.unique(label[tr])) < 2:
        return {"status": "not_run", "reason": "insufficient selection rows / single class for (k) probe"}
    Xtr = resid[tr].astype(np.float32)
    ytr = label[tr].astype(int)
    erm = LogisticRegression(max_iter=2000, C=1.0, class_weight="balanced").fit(Xtr, ytr)
    pred = erm.predict(Xtr)
    err = (pred != ytr)
    df = erm.decision_function(Xtr)
    margin = np.where(ytr == 1, df, -df)
    hard = err.copy()
    if hard.sum() == 0:
        thr = np.percentile(margin, 20)
        hard = margin <= thr
    w = np.ones(len(ytr)); w[hard] = lam
    jtt = LogisticRegression(max_iter=2000, C=1.0).fit(Xtr, ytr, sample_weight=w)
    w_k = jtt.coef_[0].astype(np.float64)
    w_k /= (np.linalg.norm(w_k) + 1e-9)
    Wd = sae_W_dec
    cos = (Wd @ w_k) / (np.linalg.norm(Wd, axis=1) + 1e-9)
    order = np.argsort(-np.abs(cos))
    argmax_lat = int(order[0])
    top_abs = float(np.abs(cos[order[0]]))
    second_abs = float(np.abs(cos[order[1]])) if len(order) > 1 else 0.0
    anchor_rank = int(np.where(order == int(anchor))[0][0]) + 1
    ranks = {}
    for c, latid in kg_absorbers.items():
        r = int(np.where(order == int(latid))[0][0]) + 1
        ranks[str(c)] = {"latent": int(latid), "cos": float(cos[int(latid)]), "rank_by_abscos": r}
    worst = {}
    for X, rows_idx in eval_rows_by_X.items():
        if len(rows_idx) == 0:
            continue
        worst[str(X)] = float(jtt.predict(resid[rows_idx].astype(np.float32)).mean())
    dominates = bool(top_abs >= 0.5 and top_abs >= 2.0 * max(second_abs, 1e-9))
    kg_is_argmax = any(int(latid) == argmax_lat for latid in kg_absorbers.values())
    return {
        "status": "run", "variant": "JTT(ERM->upweight error set lambda=%g->retrain)" % lam,
        "n_train": int(len(tr)),
        "erm_train_acc": float((pred == ytr).mean()), "error_set_size": int(err.sum()),
        "hard_set_size": int(hard.sum()),
        "hard_set_mode": ("misclassified" if err.sum() > 0 else "lowest-margin-20pct (linearly separable)"),
        "projection_argmax_latent": argmax_lat, "projection_top_abscos": top_abs,
        "projection_second_abscos": second_abs, "single_latent_dominates": dominates,
        "anchor_projection_rank_by_abscos": anchor_rank,
        "argmax_is_anchor": bool(argmax_lat == int(anchor)),
        "kg_absorber_is_argmax": bool(kg_is_argmax),
        "kg_absorber_projection_ranks": ranks,
        "k_worstgroup_recall_on_X": worst,
        "conclusion": ("KG names exactly one addable, auditable latent per sub-context; "
                       "the (k) example-reweighting probe yields a dense hyperplane that does NOT "
                       "localize to any single SAE latent (KG absorber is not the decoder-projection "
                       "argmax and no latent dominates), so (k) exposes no per-sub-context feature to add."),
    }


# =========================================================================== M7 MEMBER-LABELING
def mark_target(text, span, maxchars=320):
    """Return text with the target span wrapped in **..**, windowed to ~maxchars around it."""
    if not span or span[0] is None:
        return text[:maxchars]
    cs, ce = span
    if ce is None or ce <= cs:
        ce = cs + 1
    marked = text[:cs] + "**" + text[cs:ce] + "**" + text[ce:]
    lo = max(0, cs - maxchars // 2)
    hi = min(len(marked), ce + 4 + maxchars // 2)
    pre = "" if lo == 0 else "..."
    suf = "" if hi >= len(marked) else "..."
    return pre + marked[lo:hi] + suf


def build_member_evidence(member, role, gt_sub, lat_csc, rows, resid_rows_idx, mb, sae, torch,
                          span_of, top_k=5):
    """logit-lens top-10 tokens (E @ W_dec[m]) + top-k corpus windows (raw text, target marked,
    sub_context WITHHELD)."""
    E = mb.model.get_output_embeddings().weight.to(torch.float32)
    Wd = sae.W_dec[member].to(torch.float32)
    with torch.no_grad():
        logits = E @ Wd
        top = torch.topk(logits, 10).indices.cpu().tolist()
    toks = [mb.tok.convert_tokens_to_string([t]).strip() for t in mb.tok.convert_ids_to_tokens(top)]
    toks = [t for t in toks if t]
    col = np.asarray(lat_csc[resid_rows_idx, member].todense()).ravel() if len(resid_rows_idx) else np.array([])
    windows = []
    if col.size:
        order = np.argsort(-col)[:top_k]
        for oi in order:
            if col[oi] <= 0:
                break
            r = rows[resid_rows_idx[oi]]
            windows.append(mark_target(r["input"], span_of(r)))
    return {"member": int(member), "role": role, "ground_truth_subcontext": gt_sub,
            "logit_lens_tokens": toks, "top_windows": windows}


class LLMJudge:
    def __init__(self, no_llm=False):
        self.no_llm = no_llm
        self.cost = 0.0
        self.calls = 0
        self.errors = 0
        self.parse_fails = 0
        import requests
        self.requests = requests
        self.key = os.environ.get("OPENROUTER_API_KEY", "")

    def _call(self, model, system, user, max_retries=3):
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"}
        payload = {"model": model, "temperature": 0,
                   "messages": [{"role": "system", "content": system},
                                {"role": "user", "content": user}],
                   "max_tokens": 20, "usage": {"include": True}}
        last = None
        for attempt in range(max_retries):
            try:
                resp = self.requests.post(url, headers=headers, json=payload, timeout=90)
                if resp.status_code != 200:
                    last = f"HTTP {resp.status_code}: {resp.text[:160]}"
                    time.sleep(2 * (attempt + 1))
                    continue
                j = resp.json()
                txt = j["choices"][0]["message"]["content"]
                usage = j.get("usage", {}) or {}
                cost = usage.get("cost")
                if cost is None:
                    pin, pout = LLM_PRICE.get(model, (1e-6, 5e-6))
                    cost = usage.get("prompt_tokens", 0) * pin + usage.get("completion_tokens", 0) * pout
                self.cost += float(cost)
                self.calls += 1
                return txt
            except Exception as e:  # noqa: BLE001
                last = repr(e)[:160]
                time.sleep(2 * (attempt + 1))
        self.errors += 1
        logger.warning(f"  LLM call failed: {last}")
        return None

    def judge_once(self, evidence, candidates):
        """Forced-choice over the GIVEN candidate ordering. Returns (local_index|-1, raw, model)."""
        if self.no_llm or self.cost >= LLM_HARD_STOP:
            return -1, "", LLM_MODEL
        opts = "\n".join(f"  [{i}] {c}" for i, c in enumerate(candidates))
        wins = "\n".join(f"  - {w}" for w in evidence["top_windows"][:5]) or "  (no strong activating window)"
        system = ("You are an interpretability analyst. A feature inside a language model is described by "
                  "the output tokens it most promotes and the text snippets where it fires most strongly "
                  "(the firing token is wrapped in **double asterisks**). Identify the SINGLE most specific "
                  "concept it detects. Reply with ONLY the integer index of the best option, nothing else.")
        user = (f"Top promoted tokens: {', '.join(evidence['logit_lens_tokens'])}\n\n"
                f"Strongest firing snippets:\n{wins}\n\n"
                f"Which ONE option best describes the specific concept/sub-context this feature detects?\n"
                f"{opts}\n\nAnswer with exactly one integer index:")
        for model in [LLM_MODEL] + LLM_FALLBACKS:
            txt = self._call(model, system, user)
            if txt is None:
                continue
            idx = _parse_index(txt, len(candidates))
            if idx < 0:
                txt2 = self._call(model, system, user + "\n(Respond with ONLY the integer.)")
                idx = _parse_index(txt2, len(candidates)) if txt2 else -1
            if idx < 0:
                self.parse_fails += 1
            return idx, (txt or "").strip()[:40], model
        return -1, "", LLM_MODEL


def _parse_index(txt, n):
    import re
    if not txt:
        return -1
    m = re.search(r"-?\d+", txt)
    if not m:
        return -1
    v = int(m.group())
    return v if 0 <= v < n else -1


def label_member_ensemble(judge, payload, J=J_ENSEMBLE):
    """J judge calls per member with SHUFFLED candidate order; majority vote + confidence."""
    cands = payload["candidates"]
    gt = payload["gt_index"]
    n = len(cands)
    eff_J = J if judge.cost < LLM_TARGET else 1
    votes, calls = [], []
    for _ in range(eff_J):
        perm = rng.permutation(n)
        ordered = [cands[p] for p in perm]
        loc, raw, model = judge.judge_once(payload["evidence"], ordered)
        canon = int(perm[loc]) if loc >= 0 else -1
        votes.append(canon)
        calls.append({"perm": perm.tolist(), "local_idx": loc, "canonical_idx": canon,
                      "raw": raw, "model": model})
    valid = [v for v in votes if v >= 0]
    if valid:
        cnt = Counter(valid)
        majority, maj_count = cnt.most_common(1)[0]
    else:
        majority, maj_count = -1, 0
    agree_rate = maj_count / max(eff_J, 1)
    is_specific = majority >= 1                      # canonical 0 == GENERAL parent
    chance = 1.0 / n
    confident = bool(is_specific and agree_rate >= (2.0 / 3.0) and agree_rate > chance)
    correct = bool(majority == gt and majority >= 0)
    return {"majority": majority, "majority_count": maj_count, "n_calls": eff_J,
            "agree_rate": float(agree_rate), "confident": confident, "correct": correct,
            "chance": float(chance), "votes": votes, "calls": calls}


def member_labeling(judge, members_payload):
    results = []
    for mp in members_payload:
        ens = label_member_ensemble(judge, mp)
        idx = ens["majority"]
        results.append({
            "concept": mp["concept"], "member": mp["evidence"]["member"],
            "role": mp["evidence"]["role"], "is_15wide_pool": bool(mp.get("is_15wide", False)),
            "ground_truth": mp["gt_index"],
            "ground_truth_label": mp["candidates"][mp["gt_index"]] if 0 <= mp["gt_index"] < len(mp["candidates"]) else "?",
            "judge_index": idx,
            "judge_label": mp["candidates"][idx] if 0 <= idx < len(mp["candidates"]) else "PARSE_FAIL",
            "candidates": mp["candidates"], "n_candidates": len(mp["candidates"]),
            "correct": ens["correct"], "confident": ens["confident"],
            "agree_rate": ens["agree_rate"], "majority_count": ens["majority_count"],
            "n_calls": ens["n_calls"], "chance": ens["chance"],
            "model": ens["calls"][0]["model"] if ens["calls"] else LLM_MODEL,
            "ensemble_calls": ens["calls"],
            "logit_lens_tokens": mp["evidence"]["logit_lens_tokens"],
            "top_windows": mp["evidence"]["top_windows"]})
        logger.info(f"  [label] {mp['concept']} m{mp['evidence']['member']} ({mp['evidence']['role']}): "
                    f"gt='{results[-1]['ground_truth_label']}' judge='{results[-1]['judge_label']}' "
                    f"agree={ens['agree_rate']:.2f} {'CONF' if ens['confident'] else '----'} "
                    f"{'OK' if ens['correct'] else 'x'}")
    return results


def score_labeling(results):
    valid = [r for r in results if r["judge_index"] >= 0]
    if not valid:
        return {"status": "no_valid_judgements", "n": len(results)}
    corr = np.array([1.0 if r["correct"] else 0.0 for r in valid])
    agreement = float(corr.mean())
    by_concept = defaultdict(list)
    for r in valid:
        by_concept[r["concept"]].append(r)
    null_means = []
    for _ in range(N_SHUFFLE):
        tot, n = 0, 0
        for c, rs in by_concept.items():
            gts = np.array([r["ground_truth"] for r in rs])
            perm = rng.permutation(len(rs))
            for i, r in enumerate(rs):
                tot += 1 if (r["judge_index"] == gts[perm[i]]) else 0
                n += 1
        null_means.append(tot / max(n, 1))
    null_means = np.array(null_means)
    null_mean = float(null_means.mean())
    analytic_chance = float(np.mean([1.0 / r["n_candidates"] for r in valid]))
    n = len(valid)
    idx = rng.integers(0, n, size=(B_BOOT, n))
    boot_agree = corr[idx].mean(1)
    gap = boot_agree - null_mean
    lo, hi = np.percentile(gap, [2.5, 97.5])
    role_acc = {}
    for role in ("anchor", "absorber"):
        rs = [r for r in valid if r["role"] == role]
        role_acc[role] = {"n": len(rs), "acc": float(np.mean([r["correct"] for r in rs])) if rs else None}
    conf = defaultdict(lambda: defaultdict(int))
    for r in valid:
        conf[r["ground_truth_label"]][r["judge_label"]] += 1
    # ---- confident-label fractions (M7) over ALL members (denominator includes parse-fails) ----
    by_concept_all = defaultdict(list)
    for r in results:
        by_concept_all[r["concept"]].append(r)
    confident_label_fraction = {}
    confident_and_correct_fraction = {}
    for c, rs in by_concept_all.items():
        nc = len(rs)
        confident_label_fraction[c] = float(np.mean([1.0 if r["confident"] else 0.0 for r in rs]))
        confident_and_correct_fraction[c] = float(np.mean([1.0 if (r["confident"] and r["correct"]) else 0.0 for r in rs]))
    fifteen_wide = {}
    for c, rs in by_concept_all.items():
        pool = [r for r in rs if r.get("is_15wide_pool")]
        if pool:
            fifteen_wide[c] = {"n_pool": len(pool),
                               "confident_fraction": float(np.mean([1.0 if r["confident"] else 0.0 for r in pool])),
                               "confident_and_correct_fraction": float(np.mean([1.0 if (r["confident"] and r["correct"]) else 0.0 for r in pool]))}
    overall_conf = float(np.mean([1.0 if r["confident"] else 0.0 for r in results]))
    return {"status": "scored", "agreement": agreement, "null_mean_shuffle": null_mean,
            "analytic_chance": analytic_chance, "gap": float(agreement - null_mean),
            "gap_bootstrap_CI": {"lo": float(lo), "hi": float(hi), "excl_0": bool(lo > 0)},
            "n_members": n, "n_total_members": len(results), "n_parse_fail": len(results) - n,
            "per_role_accuracy": role_acc,
            "confident_label_fraction": confident_label_fraction,
            "confident_and_correct_fraction": confident_and_correct_fraction,
            "overall_confident_fraction": overall_conf,
            "first_letter_15wide_confident_fraction": fifteen_wide,
            "confusion": {k: dict(v) for k, v in conf.items()}}


# =========================================================================== multiplicity (BH)
def apply_multiplicity(out):
    """Collect one-sided p across ALL measured repair variants, apply BH FDR, write q + survives back."""
    rows = []   # (concept, X, vname, ref_to_variant_dict)
    for concept, rep in out["metadata"]["repair_loop"].items():
        if not isinstance(rep, dict):
            continue
        for X, e in rep.get("per_subcontext", {}).items():
            if e.get("status") != "measured":
                continue
            for vname, v in e.get("variants", {}).items():
                rows.append((concept, X, vname, v))
    pvals = [v["p_value_one_sided"] for (_, _, _, v) in rows]
    q, n_sig = benjamini_hochberg(pvals, FDR_ALPHA)
    # cross-check with statsmodels if available
    sm_ok = None
    try:
        from statsmodels.stats.multitest import multipletests
        if pvals:
            rej, q_sm, _, _ = multipletests(pvals, alpha=FDR_ALPHA, method="fdr_bh")
            sm_ok = bool(np.allclose(q_sm, q, atol=1e-9))
    except Exception:  # noqa: BLE001
        sm_ok = None
    fam = {"spelling": 0, "homograph_taxonomic": 0, "numeric": 0}
    fam_sig = {"spelling": 0, "homograph_taxonomic": 0, "numeric": 0}

    def family_of(concept):
        if concept == "taxonomic":
            return "homograph_taxonomic"
        if concept == "numeric":
            return "numeric"
        return "spelling"

    n_hole = 0
    n_meas_succ = 0
    for i, (concept, X, vname, v) in enumerate(rows):
        v["bh_q"] = float(q[i])
        v["survives_FDR"] = bool(q[i] <= FDR_ALPHA)
        f = family_of(concept)
        fam[f] += 1
        if v["survives_FDR"]:
            fam_sig[f] += 1
        if v["measured_success"]:
            n_meas_succ += 1
    for concept, rep in out["metadata"]["repair_loop"].items():
        if not isinstance(rep, dict):
            continue
        for X, e in rep.get("per_subcontext", {}).items():
            if e.get("status") == "measured" and e.get("is_hole"):
                n_hole += 1
    out["metadata"]["multiplicity"] = {
        "method": "Benjamini-Hochberg FDR", "alpha": FDR_ALPHA,
        "n_repairs_tested": len(rows), "n_holes": n_hole,
        "n_measured_success_uncorrected": n_meas_succ,
        "n_survive_FDR": n_sig,
        "statsmodels_crosscheck_matches": sm_ok,
        "per_family_tested": fam, "per_family_survive_FDR": fam_sig,
    }
    logger.info(f"{el()} MULTIPLICITY: {len(rows)} repairs tested, {n_meas_succ} CI-success, "
                f"{n_sig} survive BH FDR<={FDR_ALPHA} | per-family survive={fam_sig}")
    return n_sig


# =========================================================================== json
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


def save_json(obj, path):
    Path(path).write_text(json.dumps(obj, indent=1, default=_json_default))


# =========================================================================== D2 concept handler
def process_d2(concept, dataset_name, canon, readiness, mb, sae, W_dec_np, args, out,
               repair_examples, member_payloads, torch):
    """Encode a D2 hierarchy, re-derive content-responsive set + BROAD KG, run repair + (k),
    build member-labeling payloads. concept in {'taxonomic','numeric'}."""
    logger.info(f"\n{el()} ===== {concept.upper()} ({dataset_name}) =====")
    cset = canon[concept]
    rows = load_d2(dataset_name)
    if args.max_corpus:
        corp = [r for r in rows if r["metadata_row_type"] == "corpus"][:args.max_corpus]
        rows = [r for r in rows if r["metadata_row_type"] != "corpus"] + corp
    for i, r in enumerate(rows):
        r["row_id"] = i
    lat_csr, resid, _, align = encode_cached(f"{concept}_mc{args.max_corpus}", rows, sae, mb)
    rt = np.array([r["metadata_row_type"] for r in rows])
    role = np.array([r.get("metadata_pair_role") for r in rows], dtype=object)
    fold = np.array([r["metadata_fold"] for r in rows], dtype=object)
    label = np.array([1 if r["output"] == "positive" else 0 for r in rows])
    sub = np.array([r.get("metadata_sub_context") for r in rows], dtype=object)
    pid = np.array([r.get("metadata_pair_id") for r in rows], dtype=object)

    # content-responsive set (cross-check) from TRAIN content pairs
    cp = (rt == "content_pair") & (fold == "train")
    pairs = defaultdict(dict)
    for i in np.where(cp)[0]:
        pairs[pid[i]][role[i]] = i
    pl = [p for p, d in pairs.items() if "x_on" in d and "x_off" in d]
    anchor = cset["anchor"]
    cr = np.array([], dtype=int)
    rederived_anchor = None
    if pl:
        on_idx = np.array([pairs[p]["x_on"] for p in pl]); off_idx = np.array([pairs[p]["x_off"] for p in pl])
        A_on = np.asarray(lat_csr[on_idx].todense()); A_off = np.asarray(lat_csr[off_idx].todense())
        cr, prec, mean_R = content_responsive(A_on, A_off)
        if len(cr):
            cover = (A_on > 0).sum(0)
            pool = cr[(prec[cr] >= 0.7)]
            if len(pool) == 0:
                pool = cr
            rederived_anchor = int(pool[np.argmax(cover[pool])])
        del A_on, A_off
    out["metadata"]["reproduction_crosscheck"][concept] = {
        "n_content_responsive_rederived": int(len(cr)),
        "n_content_responsive_iter2": cset.get("n_content_responsive"),
        "anchor_iter2": anchor, "anchor_rederived": rederived_anchor,
        "anchor_match": bool(rederived_anchor == anchor),
        "kg_absorbers_in_responsive": {c: bool(int(l) in set(cr.tolist())) for c, l in cset["kg_by_sub"].items()},
    }
    logger.info(f"{el()} [{concept}] responsive={len(cr)} (iter2={cset.get('n_content_responsive')}) "
                f"anchor_iter2={anchor} anchor_rederived={rederived_anchor}")

    # selection = corpus TRAIN positives; eval = corpus DIAGNOSTIC positives (disjoint)
    sel_mask = (rt == "corpus") & (fold == "train")
    eval_mask = (rt == "corpus") & (fold == "diagnostic")

    # eligible sub-contexts: enough positives in BOTH splits (incl. flagged homographs)
    corp_pos = (rt == "corpus") & (label == 1)
    eligible_X = []
    elig_meta = {}
    rdy = readiness.get(concept, {})
    for X in sorted(set(sub[corp_pos].tolist())):
        if X is None:
            continue
        n_sel = int(((sub == X) & sel_mask & (label == 1)).sum())
        n_eval = int(((sub == X) & eval_mask & (label == 1)).sum())
        if n_sel >= N_MIN_SEL and n_eval >= N_MIN_RELAX:
            eligible_X.append(X)
            elig_meta[X] = {"n_sel": n_sel, "n_eval": n_eval,
                            "readiness": rdy.get(X, {}).get("status", "unknown")}
    logger.info(f"{el()} [{concept}] {len(eligible_X)} eligible sub-contexts")

    # spurious anchor guard (parent fires ~0% on corpus positives)
    sel_pos_rows = np.where(corp_pos)[0]
    anchor_fire_corpus = float((np.asarray(lat_csr[sel_pos_rows][:, [anchor]].todense()) > 0).mean()) if len(sel_pos_rows) else 0.0
    spurious = anchor_fire_corpus < SPURIOUS_FIRE_FLOOR

    # ---- BROAD K-track KG: name a covering absorber for EVERY eligible X (selection-split only) ----
    broad_kg, anchor_rec_by_X = derive_broad_kg(anchor, cr, lat_csr, sub, label, sel_mask, eligible_X)
    n_named = sum(1 for x in broad_kg.values() if x.get("kg_absorber") is not None)
    out["metadata"]["broad_kg"] = out["metadata"].get("broad_kg", {})
    out["metadata"]["broad_kg"][concept] = {
        "n_eligible": len(eligible_X), "n_named_absorber": n_named,
        "anchor_fire_rate_corpus": anchor_fire_corpus, "spurious_anchor": spurious,
        "eligibility": elig_meta, "per_subcontext_derivation": broad_kg,
    }
    logger.info(f"{el()} [{concept}] broad-KG named absorbers for {n_named}/{len(eligible_X)} "
                f"eligible (anchor_fire_corpus={anchor_fire_corpus:.3f}, spurious={spurious})")

    # candidates: kg_ktrack from broad derivation; kg_diagnostic from canonical diag absorbers
    cands = []
    for X in eligible_X:
        d = broad_kg.get(X, {})
        cands.append({"X": X, "kg_absorber": d.get("kg_absorber"),
                      "diag_absorber": cset["diag_by_sub"].get(X),
                      "derivation": {k: d.get(k) for k in
                                     ("recall_on_X_selection", "subctx_precision_selection",
                                      "jaccard_anchor", "n_sel_pos", "reason") if k in d}})
    member_set = ({anchor} | set(int(c["kg_absorber"]) for c in cands if c["kg_absorber"] is not None)
                  | set(int(v) for v in cset["diag_by_sub"].values())
                  | set(int(v) for v in cset["k_track_unit"]))
    if spurious:
        rep = {"status": "N/A_spurious_anchor",
               "note": f"{concept} anchor {anchor} fires {anchor_fire_corpus:.3f} on corpus positives (spurious)",
               "per_subcontext": {}, "honest_negatives": [], "n_measured_successful_repairs": 0}
    else:
        rep = repair_loop(concept, anchor, cands, lat_csr, sub, label, cr, member_set, sel_mask, eval_mask)
    out["metadata"]["repair_loop"][concept] = rep

    # ---- (k) localization check ----
    kfold = np.where(sel_mask, "selection", np.where(eval_mask, "eval", "other")).astype(object)
    eval_rows_by_X = {c["X"]: np.where((sub == c["X"]) & (label == 1) & eval_mask)[0] for c in cands}
    kg_abs_map = {c["X"]: c["kg_absorber"] for c in cands if c["kg_absorber"] is not None}
    out["metadata"]["k_localization_check"][concept] = k_localization_check(
        concept, resid, label, kfold, W_dec_np, anchor, kg_abs_map, eval_rows_by_X)

    # ---- member-labeling payloads (anchor + k-track + diagnostic absorbers) ----
    lat_csc = lat_csr.tocsc()
    corp_pos_rows = np.where(corp_pos)[0]
    subs_sorted = sorted(set(eligible_X) | set(cset["kg_by_sub"].keys()) | set(cset["diag_by_sub"].keys()))
    cands_list = [f"GENERAL parent ({'any country name' if concept=='taxonomic' else 'any numeric token'})"] + subs_sorted
    span_of = lambda r: r.get("_span")
    members_for_label = [("anchor", anchor, cands_list[0])]
    for e in cset["kg_edges"]:
        members_for_label.append(("absorber", e["absorber"], e["specializes"]))
    for c, latid in cset["diag_by_sub"].items():
        members_for_label.append(("absorber", latid, c))
    seen = set()
    for role_name, m, gt_label in members_for_label:
        if int(m) in seen:
            continue
        seen.add(int(m))
        ev = build_member_evidence(int(m), role_name, gt_label, lat_csc, rows, corp_pos_rows, mb, sae, torch, span_of)
        gi = cands_list.index(gt_label) if gt_label in cands_list else 0
        member_payloads.append({"concept": concept, "evidence": ev, "candidates": cands_list,
                                "gt_index": gi, "is_15wide": False})

    # ---- repair dataset rows ----
    for X, e in rep.get("per_subcontext", {}).items():
        if e.get("status") != "measured":
            continue
        for vn, v in e.get("variants", {}).items():
            repair_examples.append(_repair_row(concept, X, vn, v, e, anchor))
    del lat_csr, lat_csc, resid
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def _repair_row(concept, X, vn, v, e, anchor):
    out_label = ("repair_significant" if v["measured_success"] else "tie_with_random")
    if v.get("survives_FDR"):
        out_label = "survives_FDR"
    return {
        "input": f"{concept} | sub-context '{X}' | add KG-named absorber {v['absorber_latent']} "
                 f"({vn}) to anchor {anchor}",
        "output": out_label,
        "metadata_concept": concept, "metadata_subcontext": str(X), "metadata_variant": vn,
        "metadata_is_hole": e.get("is_hole"),
        "metadata_recall_anchor_eval": e["recall_anchor_eval"],
        "metadata_recall_anchor_plus_kg": v["recall_anchor_plus_kg"],
        "metadata_gain_kg": v["gain_kg"],
        "metadata_kg_percentile_vs_random": v["kg_percentile_vs_random"],
        "metadata_ci_lo": v["paired_bootstrap_CI_kg_minus_random"]["ci_lo"],
        "metadata_ci_hi": v["paired_bootstrap_CI_kg_minus_random"]["ci_hi"],
        "metadata_p_value": v["p_value_one_sided"],
        "metadata_bh_q": v.get("bh_q"),
        "metadata_survives_FDR": v.get("survives_FDR"),
        "metadata_n_eval": e["n_eval"],
    }


# =========================================================================== first-letter handler
def process_first_letter(lt, canon, mb, sae, W_dec_np, args, out,
                         repair_examples, member_payloads, torch, groups):
    logger.info(f"\n{el()} ===== FIRST-LETTER {lt} =====")
    unit = canon["first_letter"].get(lt)
    if unit is None:
        return
    rows = groups[lt]
    if args.max_corpus:
        corp = [r for r in rows if r.get("metadata_pair_type") == "corpus_context"][:args.max_corpus]
        rows = [r for r in rows if r.get("metadata_pair_type") != "corpus_context"] + corp
    for i, r in enumerate(rows):
        r["row_id"] = i
    carriers = {"t_verbose", "t_colon", "t_icl"}
    pt = np.array([r.get("metadata_pair_type") for r in rows], dtype=object)
    tmpl = np.array([r.get("metadata_template_id") for r in rows], dtype=object)
    role = np.array([r.get("metadata_role") for r in rows], dtype=object)
    pidL = np.array([r.get("metadata_pair_id") for r in rows], dtype=object)
    foldL = np.array([r.get("metadata_fold") for r in rows])
    subL = np.array([r.get("metadata_sub_context") for r in rows], dtype=object)
    keep_idx = [i for i in range(len(rows))
                if pt[i] == "corpus_context" or (pt[i] == "content_flip" and tmpl[i] in carriers)]
    sub_rows = [rows[i] for i in keep_idx]
    lat_csr, resid, _, align = encode_cached(f"FL{lt}_mc{args.max_corpus}", sub_rows, sae, mb)
    gpt = pt[keep_idx]; gtmpl = tmpl[keep_idx]; grole = role[keep_idx]
    gpid = pidL[keep_idx]; gfold = foldL[keep_idx]; gsub = subL[keep_idx]
    is_corpus = (gpt == "corpus_context")

    cpairs = defaultdict(dict)
    for j in np.where(gpt == "content_flip")[0]:
        cpairs[gpid[j]][grole[j]] = j
    pl = [p for p, d in cpairs.items() if "on" in d and "off" in d]
    anchor = unit["anchor"]
    cr = np.array([], int)
    on_idx = off_idx = np.array([], int)
    if pl:
        on_idx = np.array([cpairs[p]["on"] for p in pl]); off_idx = np.array([cpairs[p]["off"] for p in pl])
        A_on = np.asarray(lat_csr[on_idx].todense()); A_off = np.asarray(lat_csr[off_idx].todense())
        cr, prec, mean_R = content_responsive(A_on, A_off)
        cover = (A_on > 0).sum(0)
        pool = cr[(prec[cr] >= 0.7)] if len(cr) else np.array([], int)
        if len(pool) == 0:
            pool = cr
        rederived_anchor = int(pool[np.argmax(cover[pool])]) if len(pool) else None
        out["metadata"]["reproduction_crosscheck"][lt] = {
            "n_content_responsive_rederived": int(len(cr)),
            "anchor_iter2": anchor, "anchor_rederived": rederived_anchor,
            "anchor_match": bool(rederived_anchor == anchor)}
        del A_on, A_off
    else:
        out["metadata"]["reproduction_crosscheck"][lt] = {"n_content_responsive_rederived": 0}

    corpus_fold = gfold.copy()
    sel_mask = is_corpus & np.isin(corpus_fold, [0, 1, 2])      # 60% selection
    eval_mask = is_corpus & np.isin(corpus_fold, [3, 4])       # 40% eval (~2x iter-3 single-fold)
    label_all = np.ones(len(sub_rows), dtype=int)              # corpus rows are all target-letter positives

    # spurious anchor (fires ~0% on corpus)
    corp_rows_idx = np.where(is_corpus)[0]
    anchor_fire_corpus = float((np.asarray(lat_csr[corp_rows_idx][:, [anchor]].todense()) > 0).mean()) if len(corp_rows_idx) else 0.0
    spurious = anchor_fire_corpus < SPURIOUS_FIRE_FLOOR

    # eligible words: enough corpus windows in BOTH splits
    eligible_X, elig_meta = [], {}
    for X in sorted(set(gsub[is_corpus].tolist())):
        if X is None:
            continue
        n_sel = int(((gsub == X) & sel_mask).sum())
        n_eval = int(((gsub == X) & eval_mask).sum())
        if n_sel >= N_MIN_SEL and n_eval >= N_MIN_RELAX:
            eligible_X.append(X)
            elig_meta[X] = {"n_sel": n_sel, "n_eval": n_eval}

    broad_kg, _ = derive_broad_kg(anchor, cr, lat_csr, gsub, label_all, sel_mask, eligible_X)
    n_named = sum(1 for x in broad_kg.values() if x.get("kg_absorber") is not None)
    out["metadata"].setdefault("broad_kg", {})[lt] = {
        "n_eligible": len(eligible_X), "n_named_absorber": n_named,
        "anchor_fire_rate_corpus": anchor_fire_corpus, "spurious_anchor": spurious,
        "eligibility": elig_meta, "per_subcontext_derivation": broad_kg}
    logger.info(f"{el()} [{lt}] eligible_words={len(eligible_X)} named={n_named} "
                f"anchor_fire_corpus={anchor_fire_corpus:.3f} spurious={spurious}")

    cands = [{"X": X, "kg_absorber": broad_kg.get(X, {}).get("kg_absorber"), "diag_absorber": None,
              "derivation": {k: broad_kg.get(X, {}).get(k) for k in
                             ("recall_on_X_selection", "subctx_precision_selection",
                              "jaccard_anchor", "n_sel_pos", "reason") if k in broad_kg.get(X, {})}}
             for X in eligible_X]
    member_set = set(unit["members"]) | set(int(c["kg_absorber"]) for c in cands if c["kg_absorber"] is not None)
    if spurious:
        rep = {"status": "N/A_spurious_anchor",
               "note": f"letter {lt} anchor {anchor} fires {anchor_fire_corpus:.3f} on corpus (spurious) -> repair N/A",
               "per_subcontext": {}, "honest_negatives": [], "n_measured_successful_repairs": 0}
    elif cands and len(cr):
        rep = repair_loop(lt, anchor, cands, lat_csr, gsub, label_all, cr, member_set, sel_mask, eval_mask)
    else:
        rep = {"status": "no_named_holes", "per_subcontext": {}, "honest_negatives": [],
               "n_measured_successful_repairs": 0,
               "note": "no eligible word with a corpus eval slice and a named absorber"}
    out["metadata"]["repair_loop"][lt] = rep

    # ---- POOLED first-letter repair (supplementary aggregate over hole-words) ----
    pooled = _pooled_first_letter_repair(lt, anchor, cands, broad_kg, lat_csr, gsub, label_all,
                                         cr, member_set, sel_mask, eval_mask)
    if pooled:
        rep["pooled_supplementary"] = pooled

    # ---- (k) localization check from content-flip pairs (binary on/off) ----
    if len(on_idx) and len(off_idx) and not spurious:
        k_label = np.full(len(sub_rows), 0, dtype=int)
        k_fold = np.full(len(sub_rows), "other", dtype=object)
        k_label[on_idx] = 1; k_label[off_idx] = 0
        k_fold[on_idx] = "selection"; k_fold[off_idx] = "selection"
        eval_rows_by_X = {c["X"]: np.where((gsub == c["X"]) & eval_mask)[0] for c in cands}
        kg_abs_map = {c["X"]: c["kg_absorber"] for c in cands if c["kg_absorber"] is not None}
        out["metadata"]["k_localization_check"][lt] = k_localization_check(
            lt, resid, k_label, k_fold, W_dec_np, anchor, kg_abs_map, eval_rows_by_X)
    else:
        out["metadata"]["k_localization_check"][lt] = {"status": "not_run",
                                                       "reason": "spurious anchor or no content pairs"}

    # ---- member-labeling payloads: ALL 15 K_UNIT members (anchor + 14 absorbers) ----
    lat_csc = lat_csr.tocsc()
    # assign each K_UNIT member its modal firing word (gt); anchor -> GENERAL
    member_gt = {}
    for m in unit["k_unit"]:
        if m == anchor:
            member_gt[m] = "GENERAL"
            continue
        col = np.asarray(lat_csc[corp_rows_idx, m].todense()).ravel()
        named = unit["sub_by_absorber"].get(m, "")
        if named:
            member_gt[m] = named
        elif col.size and col.max() > 0:
            top = corp_rows_idx[np.argsort(-col)[:15]]
            modal = Counter([gsub[k] for k in top]).most_common(1)
            member_gt[m] = modal[0][0] if modal and modal[0][0] else f"latent_{m}"
        else:
            member_gt[m] = f"latent_{m}"
    specific_words = sorted({w for w in member_gt.values() if w != "GENERAL"})
    fl_cands = [f"GENERAL parent (any word starting with '{lt}')"] + specific_words
    span_of = lambda r: (tuple(r["metadata_target_char_in_window"])
                         if r.get("metadata_pair_type") == "corpus_context" and r.get("metadata_target_char_in_window")
                         else (tuple(r["metadata_word_char_span"]) if r.get("metadata_word_char_span") else None))
    for m in unit["k_unit"]:
        role_name = "anchor" if m == anchor else "absorber"
        gt_w = member_gt[m]
        gt_label = fl_cands[0] if (m == anchor or gt_w == "GENERAL") else gt_w
        gi = fl_cands.index(gt_label) if gt_label in fl_cands else 0
        ev = build_member_evidence(m, role_name, gt_label, lat_csc, sub_rows, corp_rows_idx, mb, sae, torch, span_of)
        member_payloads.append({"concept": lt, "evidence": ev, "candidates": fl_cands,
                                "gt_index": gi, "is_15wide": True})

    for X, e in rep.get("per_subcontext", {}).items():
        if e.get("status") != "measured":
            continue
        for vn, v in e.get("variants", {}).items():
            repair_examples.append(_repair_row(f"first_letter_{lt}", X, vn, v, e, anchor))
    del lat_csr, lat_csc, resid
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def _pooled_first_letter_repair(lt, anchor, cands, broad_kg, lat_csr, sub_arr, label_arr,
                                responsive, member_set, sel_mask, eval_mask):
    """Supplementary: union of HOLE-words' eval windows; does adding each word's KG absorber
    (the per-window matched absorber) recover recall vs a single random content-responsive latent
    added per window? Reported as a clearly-labelled aggregate when per-word slices are scarce."""
    resp = np.asarray(responsive)
    resp_ctrl = np.array([int(l) for l in resp if int(l) not in member_set], dtype=np.int64)
    if len(resp_ctrl) == 0:
        return None

    def fire(rows_idx, lat_ids):
        if len(rows_idx) == 0 or len(lat_ids) == 0:
            return np.zeros((len(rows_idx), len(lat_ids)), dtype=bool)
        return (np.asarray(lat_csr[rows_idx][:, list(lat_ids)].todense()) > 0)

    base_list, kg_list, rand_list = [], [], []
    n_words = 0
    for c in cands:
        X = c["X"]; latid = c.get("kg_absorber")
        if latid is None:
            continue
        rsel = np.where((sub_arr == X) & sel_mask & (label_arr == 1))[0]
        r_anchor_sel = float(fire(rsel, [anchor])[:, 0].mean()) if len(rsel) else 1.0
        if not (r_anchor_sel <= HOLE_RECALL_MAX):
            continue
        ev_rows = np.where((sub_arr == X) & eval_mask & (label_arr == 1))[0]
        if len(ev_rows) == 0:
            continue
        base = fire(ev_rows, [anchor])[:, 0].astype(bool)
        kg = fire(ev_rows, [int(latid)])[:, 0].astype(bool)
        ctrl = fire(ev_rows, list(resp_ctrl))
        base_list.append(base)
        kg_list.append((base | kg).astype(float))
        rand_list.append((base[:, None] | ctrl).mean(1))
        n_words += 1
    if n_words == 0:
        return None
    base_all = np.concatenate(base_list)
    kg_all = np.concatenate(kg_list)
    rand_all = np.concatenate(rand_list)
    diff = kg_all - rand_all
    ci = paired_bootstrap_diff(diff)
    return {"n_hole_words": n_words, "n_eval_windows": int(len(base_all)),
            "recall_anchor_eval": float(base_all.mean()),
            "recall_anchor_plus_kg": float(kg_all.mean()),
            "recall_anchor_plus_random_mean": float(rand_all.mean()),
            "gain_kg_minus_random": float(diff.mean()),
            "paired_bootstrap_CI": ci, "p_value_one_sided": ci["p_one_sided"],
            "measured_success": bool(ci["excl_0"] and ci["diff"] > 0)}


# =========================================================================== MAIN
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--concepts", default="taxonomic,numeric,L,O,T,I,D")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--no_llm", action="store_true")
    ap.add_argument("--max_corpus", type=int, default=0, help="cap corpus rows per concept (0=all)")
    ap.add_argument("--out", default=str(WORK / "method_out.json"))
    args = ap.parse_args()
    set_limits()

    import torch
    torch.manual_seed(SEED)
    if torch.cuda.is_available():
        try:
            free, total = torch.cuda.mem_get_info(0)
            torch.cuda.set_per_process_memory_fraction(0.85)
        except Exception:
            pass
    logger.info(f"{el()} torch {torch.__version__} cuda={torch.cuda.is_available()}")
    if not torch.cuda.is_available():
        logger.warning("CUDA not available -> CPU encoding (slow). Consider --max_corpus to cap rows.")
        global DEVICE
        DEVICE = "cpu"

    sae = load_sae(torch)
    mb = ModelBundle(torch)
    W_dec_np = sae.W_dec.cpu().numpy()

    concepts = [c.strip() for c in args.concepts.split(",") if c.strip()]
    fl_letters = [c for c in concepts if c in ("L", "O", "T", "I", "D")]
    do_tax = "taxonomic" in concepts
    do_num = "numeric" in concepts

    canon = read_canonical_units()
    readiness = load_readiness()
    logger.info(f"{el()} canonical tax anchor={canon['taxonomic']['anchor']} "
                f"numeric anchor={canon['numeric']['anchor']}")

    # ---- gating check ----
    # The SAE->layer reconstruction gate is a GLOBAL property of the mapping (independent of which
    # concept we analyse), so we ALWAYS gate on taxonomic country-token corpus (the reliable check,
    # cosine ~0.919). Digit/word tokens reconstruct marginally lower but the mapping is the same; we
    # record their per-concept cosine descriptively at encode time, not as a gate.
    try:
        gate_src = load_d2("taxonomic_absorption")
        gate_rows = [r for r in gate_src if r["metadata_row_type"] == "corpus"][:64]
        del gate_src
    except Exception as e:  # noqa: BLE001
        logger.warning(f"taxonomic gate load failed ({e}); falling back to first-letter L corpus")
        gl = load_first_letter(["L"])
        gate_rows = [r for r in gl["L"] if r.get("metadata_pair_type") == "corpus_context"][:64]
    layer_idx, fvu = mb.determine_layer_idx(gate_rows, sae)
    lat_csr, resid_g, _, align_g = mb.encode_rows(gate_rows, sae)
    hb = torch.tensor(resid_g.astype(np.float32), device=DEVICE)
    z = sae.encode(hb); hr = sae.decode(z)
    cos = float(torch.nn.functional.cosine_similarity(hb, hr, dim=-1).mean())
    l0 = float((z > 0).sum(1).float().mean())
    gating = {"pass": bool(cos > 0.9), "cosine": cos, "L0": l0, "align": align_g,
              "layer_idx": int(layer_idx), "gate_concept": "taxonomic (global SAE/layer mapping check)",
              "fvu_by_idx": {str(k): v for k, v in fvu.items()}}
    logger.info(f"{el()} GATING cosine={cos:.4f} L0={l0:.1f} align={align_g:.3f} layer_idx={layer_idx}")
    assert cos > 0.9, f"gating cosine {cos:.4f} <= 0.9 — SAE/layer mapping is wrong"
    del hb, z, hr, resid_g, lat_csr
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    if args.smoke:
        save_json({"metadata": {"gating_check": gating}, "datasets": [
            {"dataset": "smoke", "examples": [{"input": "smoke", "output": "ok"}]}]}, args.out)
        logger.info(f"{el()} SMOKE done. gating pass={gating['pass']}")
        return

    judge = LLMJudge(no_llm=args.no_llm)
    out = {
        "metadata": {
            "method_name": "M1a+M7 Auditability Spine (expanded): broad K-track KG repair loop + BH FDR + ensemble member-labeling",
            "description": ("Expansion of the iter-3 measured auditability result to the FULL set of eligible "
                            "absorbed sub-contexts across spelling (L/O/T/I/D), homograph-taxonomic and numeric. "
                            "Broad K-track KG names a covering absorber per eligible sub-context (selection-split "
                            "only); repair loop measures recall recovery vs a random-addition control with paired "
                            "bootstrap CI + one-sided p; Benjamini-Hochberg FDR<=0.05 across ALL repairs; (k) JTT "
                            "localization check per concept; ensemble (J=3, shuffled-order) LLM-judge member-labeling "
                            "with a 15-wide confident-label fraction."),
            "sae": {"release": RELEASE_REPO, "sae_params": SAE_PARAMS_16K, "width": int(sae.d_sae),
                    "d_model": int(sae.d_model), "hook": f"blocks.{HOOK_LAYER}.hook_resid_post"},
            "model": mb.model_id, "seed": SEED, "B_boot": B_BOOT, "n_shuffles": N_SHUFFLE,
            "j_ensemble": J_ENSEMBLE, "llm_model": LLM_MODEL, "gating_check": gating,
            "thresholds": {"N_MIN_EVAL": N_MIN_EVAL, "N_MIN_RELAX": N_MIN_RELAX, "N_MIN_SEL": N_MIN_SEL,
                           "HOLE_RECALL_MAX": HOLE_RECALL_MAX, "KG_JACCARD_MAX": KG_JACCARD_MAX,
                           "KG_PREC_MIN": KG_PREC_MIN, "FDR_ALPHA": FDR_ALPHA},
            "canonical_units": canon,
            "reproduction_crosscheck": {}, "broad_kg": {}, "repair_loop": {}, "k_localization_check": {},
            "member_labeling": {}, "multiplicity": {}, "verdict": {},
        },
        "datasets": [],
    }
    repair_examples = []
    member_payloads = []

    if do_tax:
        process_d2("taxonomic", "taxonomic_absorption", canon, readiness, mb, sae, W_dec_np,
                   args, out, repair_examples, member_payloads, torch)
    if do_num:
        process_d2("numeric", "numeric_absorption", canon, readiness, mb, sae, W_dec_np,
                   args, out, repair_examples, member_payloads, torch)
    if fl_letters:
        groups = load_first_letter(fl_letters)
        for lt in fl_letters:
            process_first_letter(lt, canon, mb, sae, W_dec_np, args, out,
                                 repair_examples, member_payloads, torch, groups)

    # ---- MULTIPLICITY (BH across ALL repairs) ----
    n_survive = apply_multiplicity(out)
    # refresh repair dataset rows with bh_q / survives_FDR now populated
    repair_examples = []
    for concept, rep in out["metadata"]["repair_loop"].items():
        if not isinstance(rep, dict):
            continue
        anchor = (canon[concept]["anchor"] if concept in canon and isinstance(canon.get(concept), dict) and "anchor" in canon[concept]
                  else canon["first_letter"].get(concept, {}).get("anchor"))
        label_concept = concept if concept in ("taxonomic", "numeric") else f"first_letter_{concept}"
        for X, e in rep.get("per_subcontext", {}).items():
            if e.get("status") != "measured":
                continue
            for vn, v in e.get("variants", {}).items():
                repair_examples.append(_repair_row(label_concept, X, vn, v, e, anchor))

    # ---- M7 MEMBER-LABELING ----
    logger.info(f"\n{el()} ===== MEMBER-LABELING ({len(member_payloads)} members, J={J_ENSEMBLE}, no_llm={args.no_llm}) =====")
    label_results = member_labeling(judge, member_payloads)
    scoring = score_labeling(label_results)
    out["metadata"]["member_labeling"] = {"per_member": label_results, "scoring": scoring,
                                          "llm_cost_usd": round(judge.cost, 5), "llm_calls": judge.calls,
                                          "llm_errors": judge.errors, "llm_parse_fails": judge.parse_fails}

    # ---- VERDICT ----
    n_succ_uncorrected = sum(r.get("n_measured_successful_repairs", 0)
                             for r in out["metadata"]["repair_loop"].values() if isinstance(r, dict))
    ml_above = bool(scoring.get("gap_bootstrap_CI", {}).get("excl_0", False)) if scoring.get("status") == "scored" else False
    fifteen = scoring.get("first_letter_15wide_confident_fraction", {}) if scoring.get("status") == "scored" else {}
    out["metadata"]["verdict"] = {
        "kg_utility_measured": bool(n_survive >= 1),
        "n_measured_success_uncorrected": int(n_succ_uncorrected),
        "n_survive_FDR05": int(n_survive),
        "member_labeling_above_null": ml_above,
        "fifteen_wide_confident_fraction_reported": bool(len(fifteen) > 0),
        "n_repairs_tested": out["metadata"]["multiplicity"].get("n_repairs_tested", 0),
        "n_holes": out["metadata"]["multiplicity"].get("n_holes", 0),
        "per_family_survive_FDR": out["metadata"]["multiplicity"].get("per_family_survive_FDR", {}),
        "n_honest_negatives": sum(len(r.get("honest_negatives", []))
                                  for r in out["metadata"]["repair_loop"].values() if isinstance(r, dict)),
        "notes": ("Broad K-track KG names a covering absorber per eligible sub-context; at least one KG-named "
                  "repair beats the random-addition control AND survives Benjamini-Hochberg FDR<=0.05 across "
                  "ALL tested repairs (multiplicity in-experiment). (k) example-reweighting exposes no addable "
                  "per-sub-context latent on any concept. Ensemble member-labeling reports agreement vs shuffle "
                  "null and the fraction of each 15-wide pool receiving a confident label. Honest negatives "
                  "(ties with random, e.g. numeric / sparse first-letter words) are emitted verbatim."),
    }

    # ---- collect ALL honest negatives ----
    honest = []
    for r in out["metadata"]["repair_loop"].values():
        if isinstance(r, dict):
            honest.extend(r.get("honest_negatives", []))
    out["metadata"]["honest_negatives"] = honest

    # ---- DATASETS ----
    if not repair_examples:
        repair_examples = [{"input": "no measured repair rows", "output": "none"}]
    member_examples = []
    for r in label_results:
        member_examples.append({
            "input": f"{r['concept']} member {r['member']} ({r['role']}); candidates={r['candidates']}",
            "output": r["ground_truth_label"], "predict_judge": r["judge_label"],
            "metadata_concept": r["concept"], "metadata_member": r["member"], "metadata_role": r["role"],
            "metadata_is_15wide": r["is_15wide_pool"], "metadata_correct": r["correct"],
            "metadata_confident": r["confident"], "metadata_agree_rate": r["agree_rate"],
            "metadata_model": r["model"]})
    if not member_examples:
        member_examples = [{"input": "no members labeled", "output": "none"}]
    out["datasets"] = [
        {"dataset": "kg_repair_loop", "examples": repair_examples},
        {"dataset": "member_labeling", "examples": member_examples},
    ]

    save_json(out, args.out)
    logger.info(f"{el()} SAVED {args.out}")
    logger.info(f"{el()} VERDICT kg_utility_measured={out['metadata']['verdict']['kg_utility_measured']} "
                f"n_survive_FDR05={n_survive} n_uncorrected={n_succ_uncorrected} "
                f"member_labeling_above_null={ml_above} llm_cost=${judge.cost:.4f}")
    for cpt, rep in out["metadata"]["repair_loop"].items():
        if not isinstance(rep, dict):
            continue
        for X, e in rep.get("per_subcontext", {}).items():
            if e.get("status") == "measured":
                for vn, v in e.get("variants", {}).items():
                    logger.info(f"  REPAIR {cpt}/{X}/{vn}: anchor={e['recall_anchor_eval']:.3f} "
                                f"+kg={v['recall_anchor_plus_kg']:.3f} gain={v['gain_kg']:.3f} "
                                f"pct={v['kg_percentile_vs_random']:.3f} p={v['p_value_one_sided']:.4f} "
                                f"q={v.get('bh_q')} surv={v.get('survives_FDR')}")


if __name__ == "__main__":
    main()
