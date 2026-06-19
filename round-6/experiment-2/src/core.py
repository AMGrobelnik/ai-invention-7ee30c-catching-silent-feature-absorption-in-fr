#!/usr/bin/env python
"""
M1b: KG-LOCALIZED SURGICAL SUB-CONCEPT EDIT with SIDE-EFFECT MEASUREMENT.

The downstream payoff of the auditability-first two-track CCRG units: using the emitted feature
knowledge-graph, edit EXACTLY ONE sub-context by ablating its single NAMED absorber latent and show
HIGH on-target effect with LOW collateral on sibling sub-contexts and low KL / PPL on unrelated text.

Compared, at MATCHED on-target effect, against:
  (i)  DENSE-ABL  : a diff-of-means parent-concept hyperplane erasure (ONE direction for the WHOLE
                    parent -> cannot separate the sub-context -> high collateral)  [non-SAE baseline (f)]
  (ii) RAND       : random-latent ablation control (matched mean firing rate; on-target ~0)
  (iii)(k)        : label-free JTT probe that exposes NO per-sub-context latent handle (structural)

Edit operators (the only genuinely-new code; everything else reused from iter-2/iter-3):
  KG-ABL   single-latent surgical ablation   h <- h - lambda * z[l] * W_dec[l]   (token-localised)
  KG-ADD   steering-toward                    h <- h + alpha   * unit(W_dec[l])
  DENSE-ABL parent erasure (baseline f)       h <- h - beta  * (h.u) u            (u = diff-of-means)
  DENSE-ADD parent suppression                h <- h - alpha * u
  RAND     random content-responsive latent ablation (>=10 draws, firing-rate matched)

Measurement (per family, per target sub-context X):
  on_target(X)  = detection-score drop of a FROZEN dense parent probe on held-out X contexts
  collateral    = same drop averaged over SIBLING sub-contexts (and a broad parent-positive pool)
  KL / PPL      = full-vocab KL(edited||base) + teacher-forcing PPL ratio on UNRELATED text
  token_footprint = fraction of tokens the edit actually perturbs (tiny for KG-ABL, ~1 for dense)
SURGICAL SELECTIVITY = on_target / collateral at matched on_target, with paired bootstrap CIs.

A TOXICITY negative pole (X=insult) ties the result to the firing-Jaccard router: because toxicity
sub-attributes CO-FIRE with the parent, the single-latent ablation is NOT surgical (high collateral,
selectivity ~1) -- editability is regime-scoped exactly as the router predicts.

Detection on_target/collateral are computed analytically on the captured (pooled) residual at the
SAME layer the SAE reads (the edit modifies that residual), so they need no extra forward pass; only
KL/PPL/footprint require the editing forward-hook. $0 LLM spend (all measurement is model-internal).

Usage:
  uv run method.py --smoke
  uv run method.py --families taxonomic --cap 30 --kl_prompts 20      # mini
  uv run method.py                                                    # full
"""
import os, sys, json, time, gc, argparse, resource
from pathlib import Path
from collections import defaultdict, Counter

import numpy as np

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")

from loguru import logger

# --------------------------------------------------------------------------- read-only inputs
ROOT = Path("/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop")
D1 = ROOT / "iter_1/gen_art/gen_art_dataset_1/full_data_out.json"     # first-letter spelling
D2 = ROOT / "iter_1/gen_art/gen_art_dataset_2/full_data_out.json"     # numeric + taxonomic
D3 = ROOT / "iter_1/gen_art/gen_art_dataset_3/full_data_out.json"     # toxicity
ITER3_OUT = ROOT / "iter_3/gen_art/gen_art_experiment_3/method_out.json"   # canonical units + KG

WORK = Path("/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_experiment_2")
RESULTS = WORK / "results"
CACHE = WORK / "cache"
LOGS = WORK / "logs"
for d in (RESULTS, CACHE, LOGS):
    d.mkdir(exist_ok=True)

# --------------------------------------------------------------------------- SAE / model config
RELEASE_REPO = "google/gemma-scope-2b-pt-res"
SAE_PARAMS_16K = "layer_12/width_16k/average_l0_82/params.npz"
MODEL_GATED = "google/gemma-2-2b"
MODEL_MIRROR = "unsloth/gemma-2-2b"
D_MODEL = 2304
HOOK_LAYER = 12               # blocks.12.hook_resid_post == hidden_states[13]
MAXLEN = 192
BATCH = 16
SEED = 1234

# scale grids
DET_GRID_ABL = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0]   # lambda (1.0 = full single-latent ablation)
KL_GRID_ABL = [0.5, 1.0, 2.0]                          # forward-pass subset of DET_GRID_ABL
STEER_C = [0.0, 0.5, 1.0, 2.0, 4.0, 8.0]               # add-direction scale (* Rnorm)
KL_GRID_ADD = [1.0, 4.0, 8.0]
N_RAND_DRAWS = 12
B_BOOT = 10000
EPS = 1e-8

rng = np.random.default_rng(SEED)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(str(LOGS / "run.log"), rotation="40 MB", level="DEBUG")
T0 = time.time()
def el() -> str:
    return f"{time.time()-T0:6.1f}s"

DEVICE = "cuda"


def set_limits():
    try:
        avail = 40 * 1024**3
        resource.setrlimit(resource.RLIMIT_AS, (avail * 3, avail * 3))
    except Exception as e:  # noqa: BLE001
        logger.warning(f"could not set RLIMIT_AS: {e}")


# =========================================================================== SAE (iter-2/iter-3 verbatim)
class JumpReLUSAE:
    """Gemma-Scope JumpReLU SAE loaded directly from params.npz (DeepMind canonical forward)."""
    def __init__(self, params_path, device, torch):
        self.torch = torch
        d = np.load(params_path)
        self.W_enc = torch.tensor(np.asarray(d["W_enc"]), device=device, dtype=torch.float32)   # [d_model,d_sae]
        self.W_dec = torch.tensor(np.asarray(d["W_dec"]), device=device, dtype=torch.float32)   # [d_sae,d_model]
        self.b_enc = torch.tensor(np.asarray(d["b_enc"]), device=device, dtype=torch.float32)
        self.b_dec = torch.tensor(np.asarray(d["b_dec"]), device=device, dtype=torch.float32)
        self.threshold = torch.tensor(np.asarray(d["threshold"]), device=device, dtype=torch.float32)
        self.d_model = self.W_dec.shape[1]
        self.d_sae = self.W_dec.shape[0]
        self.W_dec_unit = self.W_dec / (self.W_dec.norm(dim=-1, keepdim=True) + 1e-9)

    def encode(self, x):
        t = self.torch
        x = x.to(t.float32)
        pre = x @ self.W_enc + self.b_enc
        return (pre > self.threshold) * t.nn.functional.relu(pre)

    def decode(self, z):
        return z @ self.W_dec + self.b_dec


def _find_sae_params():
    import glob, re
    base = os.path.expanduser("~/.cache/huggingface/hub/models--google--gemma-scope-2b-pt-res")
    pats = glob.glob(f"{base}/snapshots/*/layer_12/width_16k/average_l0_*/params.npz")
    if pats:
        return min(pats, key=lambda p: abs((int(re.search(r'average_l0_(\d+)', p).group(1))
                                            if re.search(r'average_l0_(\d+)', p) else 9999) - 100))
    from huggingface_hub import hf_hub_download
    return hf_hub_download(RELEASE_REPO, SAE_PARAMS_16K, token=os.environ.get("HF_TOKEN"))


def load_sae(torch):
    path = _find_sae_params()
    logger.info(f"{el()} loading SAE from {path}")
    sae = JumpReLUSAE(path, DEVICE, torch)
    assert sae.d_model == D_MODEL, f"unexpected d_model {sae.d_model}"
    logger.info(f"{el()} SAE loaded d_sae={sae.d_sae} d_model={sae.d_model}")
    return sae


# =========================================================================== MODEL (iter-3 + edit hooks)
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
        self.layer_idx = HOOK_LAYER + 1
        self._cap = {}
        self._handle = None
        logger.info(f"{el()} model loaded ({self.model_id}) d_model={self.d_model} "
                    f"n_layers={self.model.config.num_hidden_layers} vocab={len(self.tok)}")

    def edit_layer(self):
        """The decoder layer whose OUTPUT residual the SAE reads / we edit."""
        return self.model.model.layers[self.layer_idx - 1]

    def _install_hook(self, layer_idx):
        if self._handle is not None:
            self._handle.remove()
        def _hook(_m, _i, out):
            self._cap["resid"] = out[0] if isinstance(out, (tuple, list)) else out
        self._handle = self.model.model.layers[layer_idx - 1].register_forward_hook(_hook)
        self.layer_idx = layer_idx

    def determine_layer_idx(self, rows, sae):
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

    def encode_rows(self, rows, sae, whole_sentence=False):
        """Encode rows -> (lat_csr [N,d_sae] max-pooled, resid [N,d_model] fp16 mean-pooled, align)."""
        import scipy.sparse as sp
        torch = self.torch
        N = len(rows)
        resid = np.zeros((N, D_MODEL), dtype=np.float16)
        row_nz = {}
        n_align_ok = n_align_tot = dropped = 0
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
                hs = self._cap["resid"]
            row_vecs, keep = [], []
            for i, r in enumerate(batch):
                gid = b0 + i
                T = int(am[i].sum())
                if whole_sentence:
                    pos = [t for t in range(T) if offs[i][t][1] > offs[i][t][0]]  # all real content tokens
                else:
                    pos = select_positions(offs[i].tolist(), T, r["_span"], r.get("_ti"))
                if not pos:
                    dropped += 1
                    continue
                keep.append((gid, len(pos)))
                row_vecs.append(hs[i, pos].float())
                tgt = r.get("_target")
                if tgt and not whole_sentence:
                    ids = enc["input_ids"][i, pos].tolist()
                    s = self.tok.decode(ids).strip()
                    n_align_tot += 1
                    if s.replace(" ", "").lower() == tgt.replace(" ", "").lower():
                        n_align_ok += 1
            if row_vecs:
                allres = torch.cat(row_vecs, 0)
                with torch.no_grad():
                    lat = sae.encode(allres)
                m0 = 0
                for (gid, npos) in keep:
                    sl = lat[m0:m0 + npos]
                    sr = allres[m0:m0 + npos]
                    pooled = sl.max(0).values
                    resid[gid] = sr.mean(0).half().cpu().numpy()
                    nz = torch.nonzero(pooled > 0).squeeze(-1)
                    row_nz[gid] = (nz.cpu().numpy().astype(np.int32), pooled[nz].cpu().numpy().astype(np.float32))
                    m0 += npos
                del allres, lat
            self._cap.clear(); del hs
            if (b0 // BATCH) % 60 == 0:
                logger.info(f"    encoded {min(b0+BATCH,N)}/{N} ({time.time()-t0:.0f}s)")
        lat_ptr = np.zeros(N + 1, dtype=np.int64)
        for gid in range(N):
            lat_ptr[gid + 1] = lat_ptr[gid] + (len(row_nz[gid][0]) if gid in row_nz else 0)
        total = int(lat_ptr[-1])
        lat_idx = np.zeros(total, dtype=np.int32); lat_data = np.zeros(total, dtype=np.float32)
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
        return lat_csr, resid, align

    def mean_resid_norm(self, sample_inputs, batch_size=16):
        torch = self.torch
        norms = []
        layer = self.edit_layer()
        def hook(_m, _i, out):
            self._cap["rn"] = out[0] if isinstance(out, (tuple, list)) else out
        h = layer.register_forward_hook(hook)
        try:
            for b0 in range(0, len(sample_inputs), batch_size):
                bi = sample_inputs[b0:b0 + batch_size]
                enc = self.tok(bi, return_tensors="pt", padding=True, truncation=True,
                               max_length=64, add_special_tokens=True)
                am = enc["attention_mask"].to(DEVICE)
                enc = {k: v.to(DEVICE) for k, v in enc.items()}
                with torch.no_grad():
                    self.model(**enc)
                hh = self._cap["rn"].to(torch.float32)
                n = (hh.norm(dim=-1) * am).sum() / am.sum()
                norms.append(float(n))
        finally:
            h.remove(); self._cap.pop("rn", None)
        return float(np.mean(norms))


def select_positions(offsets, T, span, ti=None):
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


# =========================================================================== DATA loaders
def _attach_span_tax(r):
    cs = r.get("metadata_target_char_start"); ce = r.get("metadata_target_char_end")
    r["_span"] = (cs, ce) if cs is not None else None
    ti = r.get("metadata_target_token_indices")
    r["_ti"] = list(ti) if ti else None
    r["_target"] = r.get("metadata_target_text")
    return r


def _attach_span_fl(r):
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


def load_taxonomic():
    blob = json.loads(D2.read_text())
    ds = next(d for d in blob["datasets"] if d["dataset"] == "taxonomic_absorption")
    return [_attach_span_tax(dict(r)) for r in ds["examples"]]


def load_first_letter(letters):
    blob = json.loads(D1.read_text())
    groups = {}
    for g in blob["datasets"]:
        lt = g["dataset"].split("_")[-1]
        if lt in letters:
            groups[lt] = [_attach_span_fl(dict(r)) for r in g["examples"]]
    return groups


def load_toxicity():
    blob = json.loads(D3.read_text())
    rows = []
    for g in blob["datasets"]:
        for r in g["examples"]:
            if r.get("metadata_record_type") == "classification":
                rows.append(dict(r))
    return rows


# =========================================================================== stats
def paired_bootstrap_diff(a, b, B=B_BOOT):
    a = np.asarray(a, float); b = np.asarray(b, float)
    n = len(a)
    if n == 0:
        return {"diff": 0.0, "ci_lo": 0.0, "ci_hi": 0.0, "excl_0": False, "n": 0}
    idx = rng.integers(0, n, size=(B, n))
    d = a[idx].mean(1) - b[idx].mean(1)
    lo, hi = np.percentile(d, [2.5, 97.5])
    return {"diff": float(a.mean() - b.mean()), "ci_lo": float(lo), "ci_hi": float(hi),
            "excl_0": bool(lo > 0 or hi < 0), "n": int(n)}


def bootstrap_mean_ci(values, B=B_BOOT):
    v = np.asarray(values, float); n = len(v)
    if n == 0:
        return {"mean": 0.0, "ci_lo": 0.0, "ci_hi": 0.0, "n": 0}
    idx = rng.integers(0, n, size=(B, n))
    bs = v[idx].mean(1)
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return {"mean": float(v.mean()), "ci_lo": float(lo), "ci_hi": float(hi), "n": int(n),
            "excl_0": bool(lo > 0 or hi < 0)}


def content_responsive(A_on, A_off, b_null=1000):
    R = A_on - A_off
    npair = R.shape[0]
    mean_R = R.mean(0)
    signs = rng.integers(0, 2, size=(npair, b_null)) * 2 - 1
    null95 = np.percentile((R.T @ signs) / npair, 95, axis=1)
    cr = np.where((mean_R > null95) & (mean_R > 0))[0]
    fire_on = (A_on > 0).sum(0).astype(np.float64)
    prec = np.where(fire_on > 0, ((A_on > 0) & ~(A_off > 0)).sum(0) / np.maximum(fire_on, 1), 0.0)
    return cr, prec, mean_R


# =========================================================================== canonical units (iter-3)
def read_canonical_units():
    blob = json.loads(ITER3_OUT.read_text())
    return blob["metadata"]["canonical_units"]


# =========================================================================== (k) localization (iter-3)
def k_localization_check(resid, label, fold_sel_mask, sae_W_dec, kg_absorbers, lam=20.0):
    """JTT: ERM probe -> upweight error set -> retrain; show the dense direction does NOT localize
    to any single SAE latent (KG absorber not the decoder-projection argmax)."""
    from sklearn.linear_model import LogisticRegression
    tr = np.where(fold_sel_mask)[0]
    if len(tr) < 20 or len(np.unique(label[tr])) < 2:
        return {"status": "not_run", "reason": "insufficient rows"}
    Xtr = resid[tr].astype(np.float32); ytr = label[tr].astype(int)
    erm = LogisticRegression(max_iter=2000, C=1.0, class_weight="balanced").fit(Xtr, ytr)
    pred = erm.predict(Xtr); err = (pred != ytr)
    df = erm.decision_function(Xtr); margin = np.where(ytr == 1, df, -df)
    hard = err.copy()
    if hard.sum() == 0:
        hard = margin <= np.percentile(margin, 20)
    w = np.ones(len(ytr)); w[hard] = lam
    jtt = LogisticRegression(max_iter=2000, C=1.0).fit(Xtr, ytr, sample_weight=w)
    w_k = jtt.coef_[0].astype(np.float64); w_k /= (np.linalg.norm(w_k) + 1e-9)
    cos = (sae_W_dec @ w_k) / (np.linalg.norm(sae_W_dec, axis=1) + 1e-9)
    order = np.argsort(-np.abs(cos))
    argmax_lat = int(order[0]); top_abs = float(abs(cos[order[0]]))
    second_abs = float(abs(cos[order[1]])) if len(order) > 1 else 0.0
    ranks = {}
    for c, latid in kg_absorbers.items():
        r = int(np.where(order == int(latid))[0][0]) + 1
        ranks[str(c)] = {"latent": int(latid), "cos": float(cos[int(latid)]), "rank_by_abscos": r}
    dominates = bool(top_abs >= 0.5 and top_abs >= 2.0 * max(second_abs, 1e-9))
    kg_is_argmax = any(int(latid) == argmax_lat for latid in kg_absorbers.values())
    return {"status": "run", "variant": "JTT(ERM->upweight error set lambda=%g->retrain)" % lam,
            "erm_train_acc": float((pred == ytr).mean()), "error_set_size": int(err.sum()),
            "projection_argmax_latent": argmax_lat, "projection_top_abscos": top_abs,
            "projection_second_abscos": second_abs, "single_latent_dominates": dominates,
            "kg_absorber_is_argmax": bool(kg_is_argmax), "kg_absorber_projection_ranks": ranks,
            "conclusion": ("The KG names exactly one addable/ablatable auditable latent per sub-context; "
                           "the label-free (k) reweighting probe yields a dense hyperplane that does NOT "
                           "localize to any single SAE latent -> no per-sub-context handle to edit.")}


# =========================================================================== PROBES
class ParentProbe:
    """Frozen dense parent detector: logistic score s(h)=sigmoid(w.h+b) (measurement instrument) +
    diff-of-means direction d_mu (the DENSE-ABL/ADD edit direction). Fit on a disjoint split."""
    def __init__(self, torch, Xpos, Xneg):
        from sklearn.linear_model import LogisticRegression
        X = np.concatenate([Xpos, Xneg], 0).astype(np.float64)
        y = np.concatenate([np.ones(len(Xpos)), np.zeros(len(Xneg))])
        clf = LogisticRegression(max_iter=3000, C=1.0, class_weight="balanced").fit(X, y)
        self.w = clf.coef_[0].astype(np.float32)
        self.b = float(clf.intercept_[0])
        self.train_auc = _auc(clf.decision_function(X), y)
        mu = Xpos.mean(0) - Xneg.mean(0)
        self.d_mu = (mu / (np.linalg.norm(mu) + 1e-9)).astype(np.float32)
        self.torch = torch
        self.w_t = torch.tensor(self.w, device=DEVICE)
        self.b_t = torch.tensor(self.b, device=DEVICE)
        self.u_t = torch.tensor(self.d_mu, device=DEVICE)        # unit diff-of-means
        # cosine between probe direction and diff-of-means (transparency: not identical => non-degenerate)
        wn = self.w / (np.linalg.norm(self.w) + 1e-9)
        self.cos_probe_dmu = float(wn @ self.d_mu)

    def margin(self, H):  # H: torch [N,d] fp32 -> probe logit (decision score) [N]; linear, NOT saturated
        return H @ self.w_t + self.b_t

    def score(self, H):   # probability [N] (saturated when probe separates perfectly -> secondary readout only)
        return self.torch.sigmoid(self.margin(H))


def _auc(scores, labels):
    from sklearn.metrics import roc_auc_score
    labels = np.asarray(labels)
    if labels.min() == labels.max():
        return 0.5
    try:
        return float(roc_auc_score(labels, scores))
    except Exception:
        return 0.5


# =========================================================================== EDIT OPERATORS (analytic, layer-local)
def edit_detection_curve(torch, sae, probe, H, op, l=None, u=None, v=None, scales=None, sign=+1):
    """Per-context detection EFFECT for each scale, in PROBE-MARGIN (logit) units (primary, linear,
    non-saturated) and in PROBABILITY units (secondary readout).
    op in {abl_latent, erase_dir, add_latent, add_dir}. effect = sign*(before - after).
    sign=+1 for ablation (suppression -> positive drop); sign=-1 for add (amplification -> positive)."""
    H = H.to(torch.float32)
    m_before = probe.margin(H); p_before = torch.sigmoid(m_before)
    if op == "abl_latent":
        z = sae.encode(H)
        base = z[:, l:l+1] * sae.W_dec[l].unsqueeze(0)          # contrib; h_after = H - s*base
        sgn_h = -1.0
    elif op == "erase_dir":
        base = (H @ u).unsqueeze(1) * u.unsqueeze(0)            # projection; h_after = H - s*base
        sgn_h = -1.0
    elif op == "add_latent":
        base = v.unsqueeze(0)                                    # h_after = H + s*v
        sgn_h = +1.0
    elif op == "add_dir":
        base = u.unsqueeze(0)                                    # h_after = H - s*u (suppress parent)
        sgn_h = -1.0
    else:
        raise ValueError(op)
    eff_m, eff_p = [], []
    for s in scales:
        Ha = H + (sgn_h * s) * base
        m_after = probe.margin(Ha)
        eff_m.append((sign * (m_before - m_after)).cpu().numpy())
        eff_p.append((sign * (p_before - torch.sigmoid(m_after))).cpu().numpy())
    return np.stack(eff_m, 1), np.stack(eff_p, 1)               # each [N, n_scale]


# =========================================================================== KL/PPL/footprint (forward hook)
def make_edit_hook(torch, sae, kind, l=None, u=None, v=None, scale=0.0, counter=None):
    """Forward hook editing the FULL residual [B,S,d] at the edit layer."""
    def hook(_m, _i, out):
        h = out[0] if isinstance(out, (tuple, list)) else out
        hf = h.to(torch.float32)
        if kind == "abl_latent":
            z = sae.encode(hf)
            fire = (z[..., l] > 0)
            contrib = z[..., l:l+1] * sae.W_dec[l].view(1, 1, -1)
            hf = hf - scale * contrib
            if counter is not None:
                counter["edited"] += int(fire.sum().item()); counter["total"] += int(fire.numel())
        elif kind == "erase_dir":
            dot = (hf @ u)
            hf = hf - scale * dot.unsqueeze(-1) * u.view(1, 1, -1)
            if counter is not None:
                counter["edited"] += int((dot.abs() > 1e-4).sum().item()); counter["total"] += int(dot.numel())
        elif kind == "add_latent":
            hf = hf + scale * v.view(1, 1, -1)
            if counter is not None:
                counter["edited"] += int(hf[..., 0].numel()); counter["total"] += int(hf[..., 0].numel())
        elif kind == "add_dir":
            hf = hf - scale * u.view(1, 1, -1)
            if counter is not None:
                counter["edited"] += int(hf[..., 0].numel()); counter["total"] += int(hf[..., 0].numel())
        h = hf.to(h.dtype)
        if isinstance(out, (tuple, list)):
            return (h,) + tuple(out[1:])
        return h
    return hook


def side_effects(mb, sae, U_texts, base_lp, base_ppl, kind, l=None, u=None, v=None, scale=0.0):
    """KL(edited||base) on last-token dist + PPL ratio + token footprint, over UNRELATED prompts U."""
    torch = mb.torch; tok = mb.tok
    layer = mb.edit_layer()
    counter = {"edited": 0, "total": 0}
    hook = make_edit_hook(torch, sae, kind, l=l, u=u, v=v, scale=scale, counter=counter)
    handle = layer.register_forward_hook(hook)
    try:
        # KL on last-token next-token distribution (left padded)
        tok.padding_side = "left"
        kls = []
        for bi, b0 in enumerate(range(0, len(U_texts), 16)):
            bp = U_texts[b0:b0 + 16]
            enc = tok(bp, return_tensors="pt", padding=True, truncation=True, max_length=64,
                      add_special_tokens=True)
            enc = {k: vv.to(DEVICE) for k, vv in enc.items()}
            with torch.no_grad():
                o = mb.model(**enc)
            lp = torch.log_softmax(o.logits[:, -1, :].to(torch.float32), dim=-1).cpu()
            blp = base_lp[b0:b0 + len(bp)]                       # aligned base for this batch
            p = lp.exp()
            kl = (p * (lp - blp)).sum(1)                         # [B]
            kls.append(kl.numpy())
        tok.padding_side = "right"
        kl_mean = float(np.concatenate(kls).mean())
        # PPL (teacher forcing) ratio
        losses = []
        for t in U_texts:
            enc = tok(t, return_tensors="pt", truncation=True, max_length=64, add_special_tokens=True)
            enc = {k: vv.to(DEVICE) for k, vv in enc.items()}
            with torch.no_grad():
                o = mb.model(**enc, labels=enc["input_ids"])
            losses.append(float(o.loss))
        ppl = float(np.exp(np.mean(losses)))
    finally:
        handle.remove()
        tok.padding_side = "right"
    foot = counter["edited"] / max(counter["total"], 1)
    return {"kl": kl_mean, "ppl": ppl, "ppl_ratio": ppl / max(base_ppl, 1e-9), "token_footprint": foot}


def base_distributions(mb, U_texts):
    torch = mb.torch; tok = mb.tok
    tok.padding_side = "left"
    lps = []
    for b0 in range(0, len(U_texts), 16):
        bp = U_texts[b0:b0 + 16]
        enc = tok(bp, return_tensors="pt", padding=True, truncation=True, max_length=64, add_special_tokens=True)
        enc = {k: vv.to(DEVICE) for k, vv in enc.items()}
        with torch.no_grad():
            o = mb.model(**enc)
        lps.append(torch.log_softmax(o.logits[:, -1, :].to(torch.float32), dim=-1).cpu())
    tok.padding_side = "right"
    base_lp = torch.cat(lps, 0)
    losses = []
    for t in U_texts:
        enc = tok(t, return_tensors="pt", truncation=True, max_length=64, add_special_tokens=True)
        enc = {k: vv.to(DEVICE) for k, vv in enc.items()}
        with torch.no_grad():
            o = mb.model(**enc, labels=enc["input_ids"])
        losses.append(float(o.loss))
    return base_lp, float(np.exp(np.mean(losses)))


# =========================================================================== BEHAVIORAL on-target/collateral
# PRIMARY effect measure (steering/ablation with side-effect): per-context next-token KL divergence at the
# edited target token's position. KG-ABL fires only on its own sub-context's tokens -> localized behavioral
# change; DENSE parent erasure changes EVERY parent-positive token -> broad collateral.
def forward_pos_logprobs(mb, sae, rows, kind=None, l=None, u=None, v=None, scale=0.0,
                         whole_sentence=False, max_len=96, batch=8):
    """Log-probs of the next token at each row's TARGET token position (or last token if whole_sentence),
    optionally under an edit hook. Returns (lp [N,V] fp16, token_footprint)."""
    torch = mb.torch; tok = mb.tok; V = len(tok)
    N = len(rows); lp_out = np.zeros((N, V), dtype=np.float16)
    counter = {"edited": 0, "total": 0}
    handle = (mb.edit_layer().register_forward_hook(
        make_edit_hook(torch, sae, kind, l=l, u=u, v=v, scale=scale, counter=counter)) if kind else None)
    old = tok.padding_side; tok.padding_side = "right"
    try:
        for b0 in range(0, N, batch):
            bt = rows[b0:b0 + batch]; texts = [r["input"] for r in bt]
            enc = tok(texts, return_offsets_mapping=True, add_special_tokens=True, padding=True,
                      truncation=True, max_length=max_len, return_tensors="pt")
            offs = enc.pop("offset_mapping"); am = enc["attention_mask"]
            enc = {k: vv.to(DEVICE) for k, vv in enc.items()}
            with torch.no_grad():
                o = mb.model(**enc)
            logits = o.logits
            for i, r in enumerate(bt):
                T = int(am[i].sum())
                if whole_sentence:
                    pos = T - 1
                else:
                    ps = select_positions(offs[i].tolist(), T, r.get("_span"), r.get("_ti"))
                    pos = max(ps) if ps else T - 1
                pos = min(max(pos, 0), T - 1)
                lp = torch.log_softmax(logits[i, pos].float(), -1)
                lp_out[b0 + i] = lp.half().cpu().numpy()
            del logits, o
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
    finally:
        if handle:
            handle.remove()
        tok.padding_side = old
    return lp_out, counter["edited"] / max(counter["total"], 1)


def kl_rows(edited_lp, base_lp, chunk=16):
    N = edited_lp.shape[0]; out = np.zeros(N)
    for c0 in range(0, N, chunk):
        e = edited_lp[c0:c0 + chunk].astype(np.float32); b = base_lp[c0:c0 + chunk].astype(np.float32)
        out[c0:c0 + chunk] = (np.exp(e) * (e - b)).sum(1)
    return np.maximum(out, 0.0)


def behavioral_curve(mb, sae, rows, base_lp, kind, l=None, u=None, v=None, scales=None,
                     whole_sentence=False):
    """[N, n_scale] per-context KL. scales[0] assumed 0.0 (no edit -> KL 0). Returns (kl[N,nscale], footprints)."""
    cols = [np.zeros(len(rows))]
    foots = [0.0]
    for s in scales[1:]:
        elp, foot = forward_pos_logprobs(mb, sae, rows, kind=kind, l=l, u=u, v=v, scale=s,
                                         whole_sentence=whole_sentence)
        cols.append(kl_rows(elp, base_lp)); foots.append(foot)
    return np.stack(cols, 1), foots


# =========================================================================== matched comparison
def _interp_at(xs, ys, x0):
    xs = np.asarray(xs, float); ys = np.asarray(ys, float)
    order = np.argsort(xs)
    return float(np.interp(x0, xs[order], ys[order]))


def _scale_for_on_target(scales, on_curve, target):
    """smallest scale whose interpolated on_target reaches `target` (monotone-ish)."""
    s = np.asarray(scales, float); o = np.asarray(on_curve, float)
    order = np.argsort(o)
    return float(np.interp(target, o[order], s[order]))


BEH_ABL = [0.0, 0.5, 1.0, 2.0]
BEH_ADD = [0.0, 1.0, 4.0]


# =========================================================================== per-case runner
def run_case(*, torch, sae, mb, family, X, absorber, absorber_precision, regime, probe,
             H_target, H_siblings, sibling_names, H_broad, target_rows, sibling_rows,
             U_texts, base_lp, base_ppl, rand_latents, parent_latent, lat_csr_for_jaccard,
             target_rows_for_jaccard, W_dec_np, whole_sentence=False,
             beh_target_cap=60, beh_sib_cap=180):
    """PRIMARY = behavioral next-token KL at the edited token's position (on_target on X contexts,
    collateral on sibling contexts). SECONDARY = dense parent-probe margin drop (shows DENSE's broad
    collateral; insensitive to single-latent edits due to redundancy). Matched effect + bootstrap CIs."""
    logger.info(f"\n{el()} --- CASE {family} / X={X} / absorber={absorber} ({regime}) ---")
    Wdec_l_unit = sae.W_dec_unit[absorber]
    Rnorm = getattr(probe, "_Rnorm", 1.0)

    # cap behavioral context sets (cost/memory); probe-margin secondary uses full H
    trows = target_rows[:beh_target_cap]
    srows = sibling_rows[:beh_sib_cap]
    base_t, _ = forward_pos_logprobs(mb, sae, trows, whole_sentence=whole_sentence)
    base_s, _ = forward_pos_logprobs(mb, sae, srows, whole_sentence=whole_sentence)

    curves = {}
    beh = {}   # behavioral per-ctx KL arrays {method: {"on":[N,nscale], "sib":[M,nscale], "scales":..}}

    def run_beh(method, kind, scales, l=None, u=None, v=None):
        on_kl, foot_on = behavioral_curve(mb, sae, trows, base_t, kind, l=l, u=u, v=v,
                                          scales=scales, whole_sentence=whole_sentence)
        sib_kl, foot_sib = behavioral_curve(mb, sae, srows, base_s, kind, l=l, u=u, v=v,
                                            scales=scales, whole_sentence=whole_sentence)
        beh[method] = {"on": on_kl, "sib": sib_kl, "scales": scales,
                       "footprint_on": foot_on, "footprint_sib": foot_sib}
        curves[method] = {"scales": scales, "beh_on_target": on_kl.mean(0).tolist(),
                          "beh_collateral": sib_kl.mean(0).tolist(),
                          "footprint_on_target_ctx": foot_on, "footprint_sibling_ctx": foot_sib}

    run_beh("KG-ABL", "abl_latent", BEH_ABL, l=absorber)
    run_beh("DENSE-ABL", "erase_dir", BEH_ABL, u=probe.u_t)
    # KG-ADD scaled by the absorber's NATURAL contribution magnitude (z_typ * ||W_dec[l]||) so c=1 ~ doubling
    z_typ = float(sae.encode(H_target.to(torch.float32))[:, absorber].mean()) if H_target.shape[0] else 1.0
    wnorm = float(sae.W_dec[absorber].norm())
    add_scales = [c * max(z_typ, 1e-3) * wnorm for c in BEH_ADD]
    run_beh("KG-ADD", "add_latent", add_scales, v=Wdec_l_unit)
    curves["KG-ADD"]["alpha"] = add_scales
    curves["KG-ADD"]["note"] = ("additive steer applies to EVERY token (footprint~1) -> not gated by firing; "
                                "contrast with KG-ABL whose surgical locality comes from the latent's own sparse firing")
    # RAND behavioral: average KL over a few random latents at lambda 0/1
    rand_on = np.zeros((len(trows), 2)); rand_sib = np.zeros((len(srows), 2))
    rfoot_on = [0.0, 0.0]; rfoot_sib = [0.0, 0.0]; nd = 0
    for rl in rand_latents[:3]:
        o, fo = behavioral_curve(mb, sae, trows, base_t, "abl_latent", l=int(rl), scales=[0.0, 1.0],
                                 whole_sentence=whole_sentence)
        s, fs = behavioral_curve(mb, sae, srows, base_s, "abl_latent", l=int(rl), scales=[0.0, 1.0],
                                 whole_sentence=whole_sentence)
        rand_on += o; rand_sib += s; rfoot_on[1] += fo[1]; rfoot_sib[1] += fs[1]; nd += 1
    if nd:
        rand_on /= nd; rand_sib /= nd; rfoot_on[1] /= nd; rfoot_sib[1] /= nd
    beh["RAND"] = {"on": rand_on, "sib": rand_sib, "scales": [0.0, 1.0],
                   "footprint_on": rfoot_on, "footprint_sib": rfoot_sib}
    curves["RAND"] = {"scales": [0.0, 1.0], "beh_on_target": rand_on.mean(0).tolist(),
                      "beh_collateral": rand_sib.mean(0).tolist(),
                      "footprint_on_target_ctx": rfoot_on, "footprint_sibling_ctx": rfoot_sib,
                      "n_draws": nd}

    # ---------- SECONDARY: dense parent-probe margin drop (analytic, full H) ----------
    pm = {}
    for m, (op, kw) in {"KG-ABL": ("abl_latent", {"l": absorber}),
                        "DENSE-ABL": ("erase_dir", {"u": probe.u_t})}.items():
        et, etp = edit_detection_curve(torch, sae, probe, H_target, op, scales=DET_GRID_ABL, sign=+1, **kw)
        es, _ = edit_detection_curve(torch, sae, probe, H_siblings, op, scales=DET_GRID_ABL, sign=+1, **kw)
        eb, _ = edit_detection_curve(torch, sae, probe, H_broad, op, scales=DET_GRID_ABL, sign=+1, **kw)
        pm[m] = {"scales": DET_GRID_ABL, "on_target_margin": et.mean(0).tolist(),
                 "collateral_margin": es.mean(0).tolist(),
                 "parent_broad_collateral_margin": eb.mean(0).tolist(),
                 "on_target_prob": etp.mean(0).tolist()}
    curves["KG-ABL"]["probe_margin"] = pm["KG-ABL"]
    curves["DENSE-ABL"]["probe_margin"] = pm["DENSE-ABL"]

    # ---------- general side-effects on UNRELATED text (KL / PPL / token footprint) ----------
    kl_ppl = {}
    kl_ppl["KG-ABL"] = side_effects(mb, sae, U_texts, base_lp, base_ppl, "abl_latent", l=absorber, scale=1.0)
    kl_ppl["DENSE-ABL"] = side_effects(mb, sae, U_texts, base_lp, base_ppl, "erase_dir", u=probe.u_t, scale=1.0)
    rse = [side_effects(mb, sae, U_texts, base_lp, base_ppl, "abl_latent", l=int(rl), scale=1.0)
           for rl in rand_latents[:2]]
    if rse:
        kl_ppl["RAND"] = {"kl": float(np.mean([x["kl"] for x in rse])),
                          "ppl_ratio": float(np.mean([x["ppl_ratio"] for x in rse])),
                          "token_footprint": float(np.mean([x["token_footprint"] for x in rse]))}
    for m in curves:
        if m in kl_ppl:
            curves[m]["unrelated_side_effects"] = kl_ppl[m]

    # ---------- MATCHED behavioral comparison (KG-ABL vs DENSE-ABL) ----------
    kg_on_c = np.array(curves["KG-ABL"]["beh_on_target"]); de_on_c = np.array(curves["DENSE-ABL"]["beh_on_target"])
    target_on = max(1e-4, min(float(kg_on_c.max()), float(de_on_c.max())) * 0.8)
    s_kg = _scale_for_on_target(BEH_ABL, curves["KG-ABL"]["beh_on_target"], target_on)
    s_de = _scale_for_on_target(BEH_ABL, curves["DENSE-ABL"]["beh_on_target"], target_on)

    def per_ctx_at(arr, scales, s0):
        return np.array([np.interp(s0, scales, arr[i]) for i in range(arr.shape[0])])
    kg_on_at = per_ctx_at(beh["KG-ABL"]["on"], BEH_ABL, s_kg)
    kg_sib_at = per_ctx_at(beh["KG-ABL"]["sib"], BEH_ABL, s_kg)
    de_sib_at = per_ctx_at(beh["DENSE-ABL"]["sib"], BEH_ABL, s_de)
    de_on_at = per_ctx_at(beh["DENSE-ABL"]["on"], BEH_ABL, s_de)

    matched = {}
    for m in ("KG-ABL", "DENSE-ABL", "RAND", "KG-ADD"):
        on_c = curves[m]["beh_on_target"]; col_c = curves[m]["beh_collateral"]
        reaches = bool(max(on_c) >= target_on)   # can this method actually attain the matched on-target?
        col = _interp_at(on_c, col_c, target_on)
        # off-target token footprint on natural SIBLING text at scale 1.0 (index where scale==1.0)
        sc = beh.get(m, {}).get("scales", [0.0]); fsib = beh.get(m, {}).get("footprint_sib", [0.0])
        idx_one = sc.index(1.0) if 1.0 in sc else len(sc) - 1
        fp_sib = float(fsib[idx_one]) if idx_one < len(fsib) else float(fsib[-1])
        matched[m] = {"on_target": target_on, "collateral": float(col), "reaches_matched": reaches,
                      "max_on_target": float(max(on_c)),
                      "selectivity": float(target_on / (abs(col) + EPS)),
                      "token_footprint_offtarget": fp_sib}
        if m in kl_ppl:
            matched[m].update({"unrelated_kl": kl_ppl[m].get("kl"),
                               "unrelated_ppl_ratio": kl_ppl[m].get("ppl_ratio"),
                               "token_footprint_unrelated": kl_ppl[m].get("token_footprint")})

    # ---------- BOOTSTRAP CIs (behavioral) ----------
    on_ci = bootstrap_mean_ci(kg_on_at)
    kg_col_ci = bootstrap_mean_ci(kg_sib_at)
    de_col_ci = bootstrap_mean_ci(de_sib_at)
    col_diff_ci = paired_bootstrap_diff(de_sib_at, kg_sib_at)   # dense - kg collateral (>0 => KG surgical)
    n_on = len(kg_on_at); n_sib = len(kg_sib_at)
    sel_diff = {}
    if n_on and n_sib:
        oi = rng.integers(0, n_on, size=(B_BOOT, n_on))
        si = rng.integers(0, n_sib, size=(B_BOOT, n_sib))
        on_bs = kg_on_at[oi].mean(1)
        kg_col_bs = np.abs(kg_sib_at[si].mean(1)); de_col_bs = np.abs(de_sib_at[si].mean(1))
        diff = on_bs / (kg_col_bs + EPS) - on_bs / (de_col_bs + EPS)
        lo, hi = np.percentile(diff, [2.5, 97.5])
        sel_diff = {"diff": float(diff.mean()), "ci_lo": float(lo), "ci_hi": float(hi),
                    "excl_0": bool(lo > 0 or hi < 0), "favors_kg": bool(lo > 0)}

    # ---------- firing-Jaccard + parent recall hole (router anchors) ----------
    fj, hole = None, None
    if lat_csr_for_jaccard is not None and parent_latent is not None:
        col_par = np.asarray(lat_csr_for_jaccard[:, parent_latent].todense()).ravel() > 0
        col_abs = np.asarray(lat_csr_for_jaccard[:, absorber].todense()).ravel() > 0
        union = int((col_par | col_abs).sum())
        fj = int((col_par & col_abs).sum()) / max(union, 1)
        if target_rows_for_jaccard is not None and len(target_rows_for_jaccard):
            par_on_X = np.asarray(lat_csr_for_jaccard[target_rows_for_jaccard, parent_latent].todense()).ravel() > 0
            hole = 1.0 - float(par_on_X.mean())

    ratio = float(matched["KG-ABL"]["selectivity"] / max(matched["DENSE-ABL"]["selectivity"], EPS))
    sel_kg = float(matched["KG-ABL"]["selectivity"])                 # on_target / kg_collateral
    on_ok = bool(on_ci.get("excl_0") and on_ci["mean"] > 0)          # KG edit has a real on-target effect
    dominates = bool(col_diff_ci["excl_0"] and col_diff_ci["diff"] > 0)  # KG strictly less collateral than dense
    fp_off = matched["KG-ABL"].get("token_footprint_offtarget", 1.0)
    # CLEAN surgical edit: KG collateral is a negligible fraction of its on-target effect (selectivity high),
    # tiny off-target footprint, and a large advantage over dense. NB: behavioral KL is non-negative, so a
    # collateral CI excluding 0 is uninformative -- cleanliness is judged by the SELECTIVITY magnitude.
    clean = bool(sel_kg >= 20 and fp_off < 0.05 and ratio >= 20)
    # The co-firing regime is EXPECTED to be non-clean (router prediction): positive-pole vs negative-pole map.
    if on_ok and dominates and clean:
        verdict = "SURGICAL_EDIT_CONFIRMED"
    elif on_ok and dominates:
        verdict = "PARTIAL_CO_FIRING_AS_PREDICTED" if regime == "co-firing" else "PARTIAL_SURGICAL"
    elif on_ok and not dominates:
        verdict = "NO_SELECTIVITY_ADVANTAGE"
    else:
        verdict = "NO_ON_TARGET_EFFECT"
    surgical = (verdict == "SURGICAL_EDIT_CONFIRMED")
    logger.info(f"  {family}/{X}: beh_on_target={on_ci['mean']:.4f} (CI {on_ci['ci_lo']:.4f}..{on_ci['ci_hi']:.4f}) "
                f"KG_col={kg_col_ci['mean']:.4f} DENSE_col={de_col_ci['mean']:.4f} "
                f"sel_KG={matched['KG-ABL']['selectivity']:.2f} sel_DE={matched['DENSE-ABL']['selectivity']:.2f} "
                f"ratio={ratio:.1f} fpoff_KG={matched['KG-ABL'].get('token_footprint_offtarget'):.4f} "
                f"fpoff_DE={matched['DENSE-ABL'].get('token_footprint_offtarget'):.4f} "
                f"jac={fj} hole={hole} diff_excl0={col_diff_ci['excl_0']} -> {verdict}")

    # ---------- PER-CONTEXT PREDICTION ROWS (one labeled example per held-out context) ----------
    # Classification framing: "does the edit affect THIS context?" Ground truth = ON_TARGET (an X-context, a
    # surgical edit SHOULD change it) vs OFF_TARGET_SIBLING (a sibling context, it should NOT). Each operator is
    # applied at its NATURAL full edit (lambda=1 = full single-latent ablation / beta=1 = full parent erasure),
    # and predict_<method> = AFFECTED / UNAFFECTED from the behavioral KL at the edited token. KG-ABL agrees with
    # the ground truth (AFFECTED on the target contexts its named feature fires on, UNAFFECTED on siblings =
    # surgical); DENSE-ABL says AFFECTED on BOTH (siblings wrongly affected = collateral); RAND ~ UNAFFECTED.
    i1 = BEH_ABL.index(1.0)
    kg_on_1 = beh["KG-ABL"]["on"][:, i1]; kg_sib_1 = beh["KG-ABL"]["sib"][:, i1]
    de_on_1 = beh["DENSE-ABL"]["on"][:, i1]; de_sib_1 = beh["DENSE-ABL"]["sib"][:, i1]
    rand_on_1 = beh["RAND"]["on"][:, 1] if beh["RAND"]["on"].shape[0] else np.zeros(0)
    rand_sib_1 = beh["RAND"]["sib"][:, 1] if beh["RAND"]["sib"].shape[0] else np.zeros(0)
    # tau = "a noticeable next-token shift": floor at the off-target (KG-sibling + RAND) noise ceiling.
    noise = np.concatenate([kg_sib_1, rand_sib_1, rand_on_1]) if len(kg_sib_1) else np.zeros(1)
    tau = max(2e-3, 4.0 * float(np.percentile(noise, 90)))
    def _lab(v):
        return "AFFECTED" if float(v) > tau else "UNAFFECTED"
    pred_rows = []
    for i in range(min(len(trows), 30)):
        pred_rows.append({
            "input": f"[{family}|{X}] edit-locality probe (target context): {trows[i]['input'][:220]}",
            "output": "ON_TARGET",
            "predict_kg_abl": _lab(kg_on_1[i]), "predict_dense_abl": _lab(de_on_1[i]),
            "predict_rand": _lab(rand_on_1[i]) if i < len(rand_on_1) else "UNAFFECTED",
            "metadata_family": family, "metadata_subcontext": str(X), "metadata_role": "target",
            "metadata_absorber_latent": int(absorber), "metadata_regime": regime,
            "metadata_kl_kg_abl": round(float(kg_on_1[i]), 6), "metadata_kl_dense_abl": round(float(de_on_1[i]), 6),
            "metadata_kl_rand": round(float(rand_on_1[i]) if i < len(rand_on_1) else 0.0, 6),
            "metadata_kl_threshold": round(float(tau), 6),
            "metadata_kg_correct": bool(kg_on_1[i] > tau), "metadata_dense_correct": bool(de_on_1[i] > tau)})
    for i in range(min(len(srows), 30)):
        pred_rows.append({
            "input": f"[{family}|sibling-of-{X}] edit-locality probe (sibling context): {srows[i]['input'][:220]}",
            "output": "OFF_TARGET_SIBLING",
            "predict_kg_abl": _lab(kg_sib_1[i]), "predict_dense_abl": _lab(de_sib_1[i]),
            "predict_rand": _lab(rand_sib_1[i]) if i < len(rand_sib_1) else "UNAFFECTED",
            "metadata_family": family, "metadata_subcontext": str(X), "metadata_role": "sibling",
            "metadata_absorber_latent": int(absorber), "metadata_regime": regime,
            "metadata_kl_kg_abl": round(float(kg_sib_1[i]), 6), "metadata_kl_dense_abl": round(float(de_sib_1[i]), 6),
            "metadata_kl_rand": round(float(rand_sib_1[i]) if i < len(rand_sib_1) else 0.0, 6),
            "metadata_kl_threshold": round(float(tau), 6),
            "metadata_kg_correct": bool(kg_sib_1[i] <= tau), "metadata_dense_correct": bool(de_sib_1[i] <= tau)})

    return {
        "prediction_rows": pred_rows, "decision_threshold_tau": float(tau),
        "per_context_label_scale": "full_edit_lambda1_beta1",
        "family": family, "target_subcontext": X, "absorber_latent": int(absorber),
        "absorber_precision": absorber_precision, "regime": regime,
        "probe_train_auc": probe.train_auc, "probe_cos_with_diffmean": probe.cos_probe_dmu,
        "firing_jaccard_with_parent": fj, "parent_recall_hole": hole,
        "n_target_ctx": len(trows), "n_sibling_ctx": len(srows), "siblings": sibling_names,
        "primary_measure": "behavioral_next_token_KL_at_edited_token_position",
        "curves": curves,
        "matched": matched, "matched_scale_kg": s_kg, "matched_scale_dense": s_de,
        "selectivity_CIs": {
            "KG-ABL_on_target": on_ci, "KG-ABL_collateral": kg_col_ci, "DENSE-ABL_collateral": de_col_ci,
            "dense_minus_kg_collateral": col_diff_ci, "KG_minus_dense_selectivity": sel_diff},
        "k_probe": {"note": "no per-sub-context handle (see metadata.k_localization_check)"},
        "verdict": verdict, "headline_selectivity_ratio": ratio,
    }


# =========================================================================== json io
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


# =========================================================================== family builders
def pick_random_latents(lat_csr, absorber, responsive, member_set, n=N_RAND_DRAWS, tol=0.5):
    """Random content-responsive latents matched on overall firing rate to the absorber, excl members."""
    N = lat_csr.shape[0]
    fire_rate = np.asarray((lat_csr > 0).sum(0)).ravel() / max(N, 1)
    target_rate = fire_rate[absorber]
    pool = [int(l) for l in responsive if l not in member_set and l != absorber]
    if not pool:
        pool = [l for l in range(lat_csr.shape[1]) if l not in member_set and fire_rate[l] > 0]
    pool = np.array(pool)
    diffs = np.abs(fire_rate[pool] - target_rate)
    order = pool[np.argsort(diffs)]
    cand = order[:max(n * 3, n)]
    if len(cand) > n:
        sel = rng.choice(cand, size=n, replace=False)
    else:
        sel = cand
    return [int(x) for x in sel], float(target_rate)


def run_taxonomic(torch, sae, mb, canon, W_dec_np, args, out):
    logger.info(f"\n{el()} ========== TAXONOMIC ==========")
    rows = load_taxonomic()
    corp = [r for r in rows if r["metadata_row_type"] == "corpus"]
    cpairs = [r for r in rows if r["metadata_row_type"] == "content_pair"]
    eligible = ['Australia', 'Brazil', 'Canada', 'China', 'France', 'Georgia', 'Germany', 'India',
                'Iran', 'Ireland', 'Israel', 'Italy', 'Japan', 'Mexico', 'New Zealand', 'Poland',
                'Russia', 'Spain', 'United Kingdom', 'United States']
    cap = args.cap
    # homograph target countries (incl Jordan which has <150 diag positives but strong diagnostic absorbers)
    target_countries = ["Georgia", "Jordan", "United States"]
    encode_countries = set(eligible) | set(target_countries)
    # encode: corpus (positives for encode countries + negatives) + content pairs (responsive set)
    enc_rows, tag = [], []
    for r in corp:
        sc = r.get("metadata_sub_context")
        if r["output"] == "positive" and sc in encode_countries:
            # cap only the high-count eligible countries; keep ALL homograph-target contexts
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
    lat_csr, resid, align = mb.encode_rows(enc_rows, sae)
    tag = np.array(tag, dtype=object)
    kind = np.array([t[0] for t in tag], dtype=object)
    sub = np.array([t[1] for t in tag], dtype=object)
    fold = np.array([t[2] for t in tag], dtype=object)

    # responsive set from content pairs
    pairs = defaultdict(dict)
    for i in np.where(kind == "cp")[0]:
        pairs[tag[i][2]][tag[i][1]] = i
    pl = [p for p, d in pairs.items() if "x_on" in d and "x_off" in d]
    A_on = np.asarray(lat_csr[[pairs[p]["x_on"] for p in pl]].todense())
    A_off = np.asarray(lat_csr[[pairs[p]["x_off"] for p in pl]].todense())
    cr, prec, _ = content_responsive(A_on, A_off)
    logger.info(f"{el()} taxonomic responsive latents={len(cr)}")

    anchor = canon["taxonomic"]["anchor"]
    # PROBE: fit on diagnostic fold (pos eligible countries vs negatives); eval on TRAIN fold (disjoint)
    fit_pos = np.where((kind == "pos") & (fold == "diagnostic"))[0]
    fit_neg = np.where((kind == "neg") & (fold == "diagnostic"))[0]
    probe = ParentProbe(torch, resid[fit_pos].astype(np.float32), resid[fit_neg].astype(np.float32))
    probe._Rnorm = out["metadata"]["Rnorm"]
    logger.info(f"{el()} taxonomic probe train_auc={probe.train_auc:.3f} cos(probe,dmu)={probe.cos_probe_dmu:.3f}")

    # (k) localization check on fit split
    label_all = (kind == "pos").astype(int)
    sel_mask = (fold == "diagnostic") & ((kind == "pos") | (kind == "neg"))
    kg_abs_map = {c: canon["taxonomic"]["kg_by_country"][c] for c in canon["taxonomic"]["kg_by_country"]}
    out["metadata"]["k_localization_check"]["taxonomic"] = k_localization_check(
        resid, label_all, sel_mask, W_dec_np, kg_abs_map)

    # U = unrelated negative windows (no-country), held out
    neg_idx = np.where((kind == "neg") & (fold == "train"))[0]
    U_texts = [enc_rows[i]["input"][:300] for i in neg_idx[:args.kl_prompts]]
    base_lp, base_ppl = base_distributions(mb, U_texts)

    member_set = set(canon["taxonomic"]["k_track_unit"]) | \
        set(a["latent"] for a in canon["taxonomic"]["diag_absorbers"])

    # targets: Georgia (primary, diag 16009), Jordan (540, 8347)
    diag_by_country = {}
    for a in canon["taxonomic"]["diag_absorbers"]:
        diag_by_country.setdefault(a["specializes"], []).append(a)
    targets = [("Georgia", 16009, 0.955)]
    for c in ("Jordan", "United States"):
        for a in diag_by_country.get(c, [])[:2]:
            targets.append((c, int(a["latent"]), float(a["subctx_precision"])))

    eval_fold = "train"   # disjoint from probe-fit (diagnostic)
    cases = []
    for X, absrb, precv in targets:
        t_idx = np.where((kind == "pos") & (sub == X) & (fold == eval_fold))[0]
        sib_names = [c for c in eligible if c != X]
        s_idx = np.where((kind == "pos") & (sub != X) & np.isin(sub, sib_names) & (fold == eval_fold))[0]
        broad_idx = s_idx  # all-country pool excluding X
        if len(t_idx) < 8:
            out.setdefault("_honest", []).append(f"taxonomic/{X}: too few eval contexts ({len(t_idx)})")
            continue
        H_t = torch.tensor(resid[t_idx].astype(np.float32), device=DEVICE)
        H_s = torch.tensor(resid[s_idx].astype(np.float32), device=DEVICE)
        H_b = torch.tensor(resid[broad_idx].astype(np.float32), device=DEVICE)
        rand_lat, trate = pick_random_latents(lat_csr, absrb, cr, member_set)
        # rows used for jaccard/hole = corpus positives of X (any fold)
        tgt_rows = np.where((kind == "pos") & (sub == X))[0]
        case = run_case(torch=torch, sae=sae, mb=mb, family="taxonomic", X=X, absorber=absrb,
                        absorber_precision=precv, regime="absorption", probe=probe,
                        H_target=H_t, H_siblings=H_s, sibling_names=sib_names[:12], H_broad=H_b,
                        target_rows=[enc_rows[i] for i in t_idx], sibling_rows=[enc_rows[i] for i in s_idx],
                        U_texts=U_texts, base_lp=base_lp, base_ppl=base_ppl, rand_latents=rand_lat,
                        parent_latent=anchor, lat_csr_for_jaccard=lat_csr, target_rows_for_jaccard=tgt_rows,
                        W_dec_np=W_dec_np)
        case["random_latent_firing_rate"] = trate
        cases.append(case)
        del H_t, H_s, H_b; torch.cuda.empty_cache()
    del lat_csr, resid, A_on, A_off
    gc.collect(); torch.cuda.empty_cache()
    return cases


def run_first_letter(torch, sae, mb, canon, W_dec_np, args, out):
    logger.info(f"\n{el()} ========== FIRST-LETTER L ==========")
    letters = ["L", "O", "T", "I", "D"]
    groups = load_first_letter(letters)
    unit = canon["first_letter"]["L"]
    anchor = unit["anchor"]
    # build corpus rows: L positives + other-letter negatives (non-L word tokens)
    enc_rows, tag = [], []   # tag = (letter, sub_context, fold)
    cap = args.cap
    Lcorp = [r for r in groups["L"] if r.get("metadata_pair_type") == "corpus_context"]
    for r in Lcorp:
        enc_rows.append(r); tag.append(("L", r.get("metadata_sub_context"), r.get("metadata_fold")))
    neg_letters = ["O", "T", "I", "D"]
    per_neg = (cap or 250)
    for lt in neg_letters:
        cc = [r for r in groups[lt] if r.get("metadata_pair_type") == "corpus_context"][:per_neg]
        for r in cc:
            enc_rows.append(r); tag.append((lt, r.get("metadata_sub_context"), r.get("metadata_fold")))
    # content pairs for responsive set
    Lpairs = [r for r in groups["L"] if r.get("metadata_pair_type") == "content_flip"
              and r.get("metadata_template_id") in {"t_verbose", "t_colon", "t_icl"}]
    n_corp = len(enc_rows)
    for r in Lpairs:
        enc_rows.append(r); tag.append(("cp", r.get("metadata_role"), r.get("metadata_pair_id")))
    logger.info(f"{el()} first-letter encoding {len(enc_rows)} rows ({n_corp} corpus + {len(Lpairs)} cp)")
    lat_csr, resid, align = mb.encode_rows(enc_rows, sae)
    tag = np.array(tag, dtype=object)
    letter = np.array([t[0] for t in tag], dtype=object)
    sub = np.array([t[1] for t in tag], dtype=object)
    fold = np.array([t[2] for t in tag], dtype=object)

    pairs = defaultdict(dict)
    for i in np.where(letter == "cp")[0]:
        pairs[tag[i][2]][tag[i][1]] = i
    pl = [p for p, d in pairs.items() if "on" in d and "off" in d]
    cr = np.array([], int)
    if pl:
        A_on = np.asarray(lat_csr[[pairs[p]["on"] for p in pl]].todense())
        A_off = np.asarray(lat_csr[[pairs[p]["off"] for p in pl]].todense())
        cr, prec, _ = content_responsive(A_on, A_off)
        del A_on, A_off
    logger.info(f"{el()} first-letter responsive latents={len(cr)}")

    # PROBE: L-word tokens vs non-L word tokens. fit on a deterministic split (folds 0,1,2 of corpus);
    # eval on folds 3,4 (disjoint). Negatives split same way.
    is_corpus = np.isin(letter, ["L"] + neg_letters)
    fit_mask = is_corpus & np.isin(fold, [0, 1, 2])
    eval_mask = is_corpus & np.isin(fold, [3, 4])
    fit_pos = np.where(fit_mask & (letter == "L"))[0]
    fit_neg = np.where(fit_mask & (letter != "L") & is_corpus)[0]
    probe = ParentProbe(torch, resid[fit_pos].astype(np.float32), resid[fit_neg].astype(np.float32))
    probe._Rnorm = out["metadata"]["Rnorm"]
    logger.info(f"{el()} first-letter probe train_auc={probe.train_auc:.3f} cos(probe,dmu)={probe.cos_probe_dmu:.3f}")

    # (k) check
    label_all = (letter == "L").astype(int)
    sel_mask = fit_mask
    # pick the highest-precision L absorber on held-out 'word' contexts among named absorbers
    named = [(int(ab), unit["sub_by_absorber"].get(str(ab), unit["sub_by_absorber"].get(ab, "")))
             for ab in unit["absorbers"]]
    named = [(ab, nm) for ab, nm in named if nm and not nm.startswith("latent_")]
    # held-out precision: among eval L-corpus, fraction of absorber-firing rows whose word==nm
    def heldout_word_precision(ab, nm):
        col = np.asarray(lat_csr[:, ab].todense()).ravel() > 0
        rows_fire = np.where(col & eval_mask & (letter == "L"))[0]
        if len(rows_fire) < 5:
            return 0.0, len(rows_fire)
        hit = sum(1 for i in rows_fire if sub[i] == nm)
        return hit / len(rows_fire), len(rows_fire)
    scored = []
    for ab, nm in named:
        p, nf = heldout_word_precision(ab, nm)
        scored.append((ab, nm, p, nf))
    scored.sort(key=lambda x: -x[2])
    out["metadata"]["first_letter_absorber_scan"] = [{"absorber": a, "word": w, "heldout_precision": p, "n_fire": n}
                                                     for a, w, p, n in scored]
    kg_abs_map = {nm: ab for ab, nm, p, n in scored[:5]}
    out["metadata"]["k_localization_check"]["first_letter_L"] = k_localization_check(
        resid, label_all, sel_mask, W_dec_np, kg_abs_map)

    if not scored or scored[0][2] < 0.5:
        out.setdefault("_honest", []).append(
            f"first-letter L: no absorber clears held-out word-precision 0.5 (best={scored[0] if scored else None}); "
            f"descriptive only (token-space footprint + (k)-no-handle still hold)")
    primary = scored[0] if scored else None
    if primary is None:
        del lat_csr, resid; gc.collect(); torch.cuda.empty_cache()
        return []
    ab, nm, precv, nf = primary
    logger.info(f"{el()} first-letter primary absorber={ab} word='{nm}' heldout_prec={precv:.3f} n_fire={nf}")

    # U = other-letter corpus windows (non-L => unrelated wrt the L-probe? they're still words; use generic neutral)
    U_texts = NEUTRAL_TEXT[:args.kl_prompts]
    base_lp, base_ppl = base_distributions(mb, U_texts)
    member_set = set(unit["members"])

    X = nm
    t_idx = np.where(eval_mask & (letter == "L") & (sub == X))[0]
    # if too few in eval, use ALL L corpus of that word
    if len(t_idx) < 8:
        t_idx = np.where((letter == "L") & (sub == X))[0]
    sib_words = [w for w in Counter(sub[(letter == "L")]).keys() if w and w != X]
    s_idx = np.where((letter == "L") & np.isin(sub, sib_words[:30]) & (sub != X))[0]
    if len(s_idx) > 400:
        s_idx = rng.choice(s_idx, 400, replace=False)
    H_t = torch.tensor(resid[t_idx].astype(np.float32), device=DEVICE)
    H_s = torch.tensor(resid[s_idx].astype(np.float32), device=DEVICE)
    rand_lat, trate = pick_random_latents(lat_csr, ab, cr, member_set)
    tgt_rows = np.where((letter == "L") & (sub == X))[0]
    case = run_case(torch=torch, sae=sae, mb=mb, family="first_letter", X=X, absorber=ab,
                    absorber_precision=precv, regime="absorption", probe=probe,
                    H_target=H_t, H_siblings=H_s, sibling_names=sib_words[:12], H_broad=H_s,
                    target_rows=[enc_rows[i] for i in t_idx], sibling_rows=[enc_rows[i] for i in s_idx],
                    U_texts=U_texts, base_lp=base_lp, base_ppl=base_ppl, rand_latents=rand_lat,
                    parent_latent=anchor, lat_csr_for_jaccard=lat_csr, target_rows_for_jaccard=tgt_rows,
                    W_dec_np=W_dec_np)
    case["random_latent_firing_rate"] = trate
    del lat_csr, resid, H_t, H_s
    gc.collect(); torch.cuda.empty_cache()
    return [case]


def run_toxicity(torch, sae, mb, canon, W_dec_np, args, out):
    logger.info(f"\n{el()} ========== TOXICITY (negative pole) ==========")
    rows = load_toxicity()
    cap = args.cap or 400
    subs = ["insult", "obscene", "threat", "identity_attack"]
    def subval(r, name):
        sf = r.get("metadata_subcontext_floats") or {}
        return float(sf.get(name, 0.0))
    # encode: balanced toxic (label1) + neutral (label0); keep sub floats
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
    subm = {s: np.array([1 if subval(r, s) >= 0.5 else 0 for r in enc_rows]) for s in subs}

    # PROBE toxic vs neutral, fit on train fold, eval on test/val
    fit_mask = (fold == "train")
    eval_mask = np.isin(fold, ["test", "val"])
    fp = np.where(fit_mask & (label == 1))[0]; fn = np.where(fit_mask & (label == 0))[0]
    probe = ParentProbe(torch, resid[fp].astype(np.float32), resid[fn].astype(np.float32))
    probe._Rnorm = out["metadata"]["Rnorm"]
    logger.info(f"{el()} toxicity probe train_auc={probe.train_auc:.3f}")

    # responsive set: toxic vs neutral content pairs not available here; use per-latent AUC for sub-attrs.
    # parent latent = highest-recall latent on toxic rows
    toxrows = np.where((label == 1) & fit_mask)[0]
    fire_tox = np.asarray((lat_csr[toxrows] > 0).sum(0)).ravel() / max(len(toxrows), 1)
    parent_latent = int(np.argmax(fire_tox))
    # insult sub-attribute latent: highest AUC discriminating insult among toxic rows (fit fold)
    from sklearn.metrics import roc_auc_score
    tox_fit = np.where((label == 1) & fit_mask)[0]
    yins = subm["insult"][tox_fit]
    best_lat, best_auc = None, 0.5
    if yins.sum() >= 20 and (len(yins) - yins.sum()) >= 20:
        cols = np.asarray(lat_csr[tox_fit].todense())
        # restrict to latents that fire enough
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
        out.setdefault("_honest", []).append("toxicity: no insult sub-attribute latent (AUC<=0.5) -> "
                                              "co-firing regime offers no localizable handle (router-consistent)")
        del lat_csr, resid; gc.collect(); torch.cuda.empty_cache()
        return [{"family": "toxicity", "target_subcontext": "insult", "regime": "co-firing",
                 "verdict": "NO_LOCALIZABLE_HANDLE", "absorber_latent": -1,
                 "note": "no sub-attribute latent separates insult among toxic rows"}]
    absorber = best_lat
    logger.info(f"{el()} toxicity insult sub-attr latent={absorber} AUC={best_auc:.3f} parent_latent={parent_latent}")

    U_texts = [enc_rows[i]["input"][:200] for i in np.where((label == 0) & eval_mask)[0][:args.kl_prompts]]
    if len(U_texts) < 5:
        U_texts = NEUTRAL_TEXT[:args.kl_prompts]
    base_lp, base_ppl = base_distributions(mb, U_texts)

    # eval contexts: insult-positive (target) vs sibling-positive-but-insult-negative
    t_idx = np.where(eval_mask & (label == 1) & (subm["insult"] == 1))[0]
    sib_mask = eval_mask & (label == 1) & (subm["insult"] == 0) & (
        (subm["obscene"] == 1) | (subm["threat"] == 1) | (subm["identity_attack"] == 1))
    s_idx = np.where(sib_mask)[0]
    if len(t_idx) > 400:
        t_idx = rng.choice(t_idx, 400, replace=False)
    if len(s_idx) > 400:
        s_idx = rng.choice(s_idx, 400, replace=False)
    H_t = torch.tensor(resid[t_idx].astype(np.float32), device=DEVICE)
    H_s = torch.tensor(resid[s_idx].astype(np.float32), device=DEVICE)
    member_set = {absorber, parent_latent}
    responsive_tox = np.where(fire_tox > 0.05)[0]
    rand_lat, trate = pick_random_latents(lat_csr, absorber, responsive_tox, member_set)
    tgt_rows = np.where((label == 1) & (subm["insult"] == 1))[0]
    case = run_case(torch=torch, sae=sae, mb=mb, family="toxicity", X="insult", absorber=absorber,
                    absorber_precision=float(best_auc), regime="co-firing", probe=probe,
                    H_target=H_t, H_siblings=H_s, sibling_names=["obscene", "threat", "identity_attack"],
                    H_broad=H_s, target_rows=[enc_rows[i] for i in t_idx], sibling_rows=[enc_rows[i] for i in s_idx],
                    U_texts=U_texts, base_lp=base_lp, base_ppl=base_ppl, rand_latents=rand_lat,
                    parent_latent=parent_latent, lat_csr_for_jaccard=lat_csr, target_rows_for_jaccard=tgt_rows,
                    W_dec_np=W_dec_np, whole_sentence=True)
    case["random_latent_firing_rate"] = trate
    case["insult_latent_auc"] = float(best_auc)
    del lat_csr, resid, H_t, H_s
    gc.collect(); torch.cuda.empty_cache()
    return [case]


NEUTRAL_TEXT = [
    "The weather today is", "I went to the store to buy", "She opened the door and saw",
    "My favorite hobby is", "The most important thing in life is", "When I woke up this morning",
    "The scientist explained that", "He picked up the phone and", "In the middle of the forest there was",
    "The recipe calls for", "They decided to travel to", "The teacher wrote on the board",
    "After the meeting we went to", "The book on the table was about", "Yesterday I learned how to",
    "The children played in the", "Looking out the window I noticed", "The company announced a new",
    "On the way home she stopped at", "The old man told a story about", "During the summer we like to",
    "The first thing I do every day is", "He reached into his pocket and pulled out", "The river flowed past the",
]


# =========================================================================== MAIN
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--families", default="taxonomic,first_letter,toxicity")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--cap", type=int, default=0, help="cap contexts per sub-context/fold (0=all)")
    ap.add_argument("--kl_prompts", type=int, default=40)
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
    logger.info(f"{el()} torch {torch.__version__} cuda={torch.cuda.is_available()} device={DEVICE}")

    sae = load_sae(torch)
    mb = ModelBundle(torch)
    W_dec_np = sae.W_dec.cpu().numpy()
    canon = read_canonical_units()

    # gating: determine layer + cosine on taxonomic corpus sample
    tax_rows = load_taxonomic()
    gate_rows = [r for r in tax_rows if r["metadata_row_type"] == "corpus"][:64]
    layer_idx, fvu = mb.determine_layer_idx(gate_rows, sae)
    lat_g, resid_g, align_g = mb.encode_rows(gate_rows, sae)
    hb = torch.tensor(resid_g.astype(np.float32), device=DEVICE)
    z = sae.encode(hb); hr = sae.decode(z)
    cos = float(torch.nn.functional.cosine_similarity(hb, hr, dim=-1).mean())
    l0 = float((z > 0).sum(1).float().mean())
    Rnorm = mb.mean_resid_norm(NEUTRAL_TEXT)
    gating = {"pass": bool(cos > 0.9), "cosine": cos, "L0": l0, "align": align_g,
              "layer_idx": int(layer_idx), "fvu_by_idx": {str(k): v for k, v in fvu.items()}, "Rnorm": Rnorm}
    logger.info(f"{el()} GATING cosine={cos:.4f} L0={l0:.1f} layer_idx={layer_idx} Rnorm={Rnorm:.1f}")
    assert cos > 0.85, f"gating cosine {cos:.4f} too low — SAE/layer mapping wrong"
    del hb, z, hr, resid_g, lat_g; gc.collect(); torch.cuda.empty_cache()

    out = {"metadata": {
        "method_name": "M1b KG-Localized Surgical Sub-Concept Edit with Side-Effect Measurement",
        "description": ("Single named-absorber ablation (KG-ABL) vs dense diff-of-means parent erasure "
                        "(DENSE-ABL, baseline f) vs random-latent (RAND) vs label-free (k); on_target/"
                        "collateral via a frozen dense parent probe at matched effect, with KL/PPL/"
                        "token-footprint side-effects and a toxicity co-firing negative pole."),
        "sae": {"release": RELEASE_REPO, "sae_params": SAE_PARAMS_16K, "width": int(sae.d_sae),
                "d_model": int(sae.d_model), "hook": f"blocks.{HOOK_LAYER}.hook_resid_post"},
        "model": mb.model_id, "seed": SEED, "B_boot": B_BOOT, "Rnorm": Rnorm,
        "gating_check": gating, "canonical_units": canon,
        "scale_grids": {"DET_GRID_ABL": DET_GRID_ABL, "KL_GRID_ABL": KL_GRID_ABL,
                        "STEER_C": STEER_C, "N_RAND_DRAWS": N_RAND_DRAWS},
        "k_localization_check": {}, "_base_neutral": base_distributions(mb, NEUTRAL_TEXT)},
        "datasets": []}

    if args.smoke:
        # token-space locality sanity: ablate Georgia 16009; assert it fires on Georgia not France
        geo = [r for r in tax_rows if r["metadata_row_type"] == "corpus" and r["metadata_sub_context"] == "Georgia"][:2]
        fra = [r for r in tax_rows if r["metadata_row_type"] == "corpus" and r["metadata_sub_context"] == "France"][:2]
        lat_s, resid_s, _ = mb.encode_rows(geo + fra, sae)
        z = sae.encode(torch.tensor(resid_s.astype(np.float32), device=DEVICE))
        zg = float(z[:2, 16009].mean()); zf = float(z[2:, 16009].mean())
        logger.info(f"{el()} SMOKE Georgia-absorber 16009: z(Georgia)={zg:.3f} z(France)={zf:.3f}")
        out["metadata"]["smoke"] = {"z_georgia_16009": zg, "z_france_16009": zf,
                                    "token_locality_ok": bool(zg > zf)}
        out["metadata"].pop("_base_neutral", None)
        out["datasets"] = [{"dataset": "smoke", "examples": [{"input": "smoke", "output": "ok"}]}]
        save_json(out, args.out)
        logger.info(f"{el()} SMOKE done gating={gating['pass']} locality_ok={zg>zf}")
        return

    fams = [f.strip() for f in args.families.split(",") if f.strip()]
    all_cases = []
    if "taxonomic" in fams:
        all_cases += run_taxonomic(torch, sae, mb, canon, W_dec_np, args, out)
    if "first_letter" in fams:
        all_cases += run_first_letter(torch, sae, mb, canon, W_dec_np, args, out)
    if "toxicity" in fams:
        all_cases += run_toxicity(torch, sae, mb, canon, W_dec_np, args, out)

    out["metadata"].pop("_base_neutral", None)

    # ---------- SUMMARY ----------
    surg = [c for c in all_cases if c.get("verdict") == "SURGICAL_EDIT_CONFIRMED"]
    geo = next((c for c in all_cases if c["family"] == "taxonomic" and c["target_subcontext"] == "Georgia"), None)
    flp = next((c for c in all_cases if c["family"] == "first_letter"), None)
    tox = next((c for c in all_cases if c["family"] == "toxicity"), None)
    def _mean(xs):
        xs = [x for x in xs if x is not None]
        return float(np.mean(xs)) if xs else None
    absn = [c for c in all_cases if c.get("regime") == "absorption" and "matched" in c]
    cofn = [c for c in all_cases if c.get("regime") == "co-firing" and "matched" in c]
    summary = {
        "n_cases": len(all_cases), "n_surgical_confirmed": len(surg),
        "surgical_cases": [f"{c['family']}/{c['target_subcontext']}" for c in surg],
        "taxonomic_primary_georgia": {
            "verdict": geo["verdict"], "on_target": geo["selectivity_CIs"]["KG-ABL_on_target"]["mean"],
            "kg_collateral": geo["selectivity_CIs"]["KG-ABL_collateral"]["mean"],
            "dense_collateral": geo["selectivity_CIs"]["DENSE-ABL_collateral"]["mean"],
            "selectivity_ratio": geo["headline_selectivity_ratio"],
            "kg_offtarget_footprint": geo["matched"]["KG-ABL"].get("token_footprint_offtarget"),
            "dense_offtarget_footprint": geo["matched"]["DENSE-ABL"].get("token_footprint_offtarget"),
            "dense_minus_kg_collateral_CI": geo["selectivity_CIs"]["dense_minus_kg_collateral"]} if geo else None,
        "first_letter_primary": {"verdict": flp["verdict"], "X": flp["target_subcontext"],
                                 "absorber": flp["absorber_latent"],
                                 "selectivity_ratio": flp["headline_selectivity_ratio"]} if flp else None,
        "toxicity_negative_pole": {
            "verdict": tox.get("verdict"), "selectivity_KG": tox.get("matched", {}).get("KG-ABL", {}).get("selectivity"),
            "selectivity_ratio_vs_dense": tox.get("headline_selectivity_ratio"),
            "kg_collateral": tox.get("selectivity_CIs", {}).get("KG-ABL_collateral", {}).get("mean"),
            "kg_offtarget_footprint": tox.get("matched", {}).get("KG-ABL", {}).get("token_footprint_offtarget"),
            "firing_jaccard_with_parent": tox.get("firing_jaccard_with_parent"),
            "parent_recall_hole": tox.get("parent_recall_hole")} if tox else None,
        # ROUTER MAP: absorption (low firing-Jaccard, clean parent hole) -> CLEAN surgical;
        # co-firing (high firing-Jaccard) -> NOT clean. Selectivity ratio + footprint should split the regimes.
        "regime_router_map": {
            "absorption": {"n": len(absn), "mean_selectivity_ratio": _mean([c["headline_selectivity_ratio"] for c in absn]),
                           "mean_firing_jaccard": _mean([c["firing_jaccard_with_parent"] for c in absn]),
                           "mean_kg_offtarget_footprint": _mean([c["matched"]["KG-ABL"].get("token_footprint_offtarget") for c in absn]),
                           "mean_kg_collateral": _mean([c["selectivity_CIs"]["KG-ABL_collateral"]["mean"] for c in absn])},
            "co_firing": {"n": len(cofn), "mean_selectivity_ratio": _mean([c["headline_selectivity_ratio"] for c in cofn]),
                          "mean_firing_jaccard": _mean([c["firing_jaccard_with_parent"] for c in cofn]),
                          "mean_kg_offtarget_footprint": _mean([c["matched"]["KG-ABL"].get("token_footprint_offtarget") for c in cofn]),
                          "mean_kg_collateral": _mean([c["selectivity_CIs"]["KG-ABL_collateral"]["mean"] for c in cofn])}},
        "headline_selectivity_ratio": geo["headline_selectivity_ratio"] if geo else None,
    }
    honest = out.pop("_honest", [])
    # derive honest graded-outcome notes from the per-case verdicts (no fabrication; strictly from results)
    for c in all_cases:
        v = c.get("verdict")
        if v == "PARTIAL_SURGICAL":
            honest.append(f"{c['family']}/{c['target_subcontext']} (absorber {c['absorber_latent']}, "
                          f"precision {c.get('absorber_precision')}): only PARTIAL_SURGICAL "
                          f"(selectivity ratio {c.get('headline_selectivity_ratio'):.1f}) — a lower-precision "
                          f"absorber gives a weaker, less clean edit; absorber precision predicts surgicality.")
        elif v == "PARTIAL_CO_FIRING_AS_PREDICTED":
            honest.append(f"{c['family']}/{c['target_subcontext']} (CO-FIRING regime, firing-Jaccard "
                          f"{c.get('firing_jaccard_with_parent'):.3f}, parent recall-hole "
                          f"{c.get('parent_recall_hole')}): single-latent ablation is NOT cleanly surgical "
                          f"(ratio {c.get('headline_selectivity_ratio'):.1f}, off-target footprint "
                          f"{c['matched']['KG-ABL'].get('token_footprint_offtarget'):.3f}) — editability is "
                          f"regime-scoped exactly as the firing-Jaccard router predicts (declared negative pole).")
        elif v in ("NO_SELECTIVITY_ADVANTAGE", "NO_ON_TARGET_EFFECT", "NO_LOCALIZABLE_HANDLE"):
            honest.append(f"{c['family']}/{c['target_subcontext']}: {v} — localized single-latent ablation did "
                          f"not yield a measurable surgical edit here (reported, not hidden).")
    # ---------- DATASET 1: per-context edit-locality predictions (input/output + predict_<method>) ----------
    # Pull the per-context prediction rows out of each case (so per_case stays compact) and flatten them.
    per_context_examples = []
    for c in all_cases:
        per_context_examples.extend(c.pop("prediction_rows", []))
    out["metadata"]["per_case"] = all_cases
    out["metadata"]["summary"] = summary
    out["metadata"]["honest_negatives"] = honest

    # ---------- DATASET 2: per-case surgical-edit verdicts (each with predict_* per method) ----------
    case_examples = []
    for c in all_cases:
        ci = c.get("selectivity_CIs", {})
        mt = c.get("matched", {})
        expected = "SURGICAL_EXPECTED" if c.get("regime") == "absorption" else "NON_SURGICAL_EXPECTED"
        case_examples.append({
            "input": (f"{c['family']} | surgically ablate KG-named absorber {c['absorber_latent']} for sub-context "
                      f"'{c['target_subcontext']}' ({c['regime']}); KG-ABL vs DENSE-ABL at matched on-target effect"),
            "output": expected,                               # ground truth expected by the firing-Jaccard router
            "predict_kg_abl": c.get("verdict", "NA"),         # KG single-latent ablation outcome
            "predict_dense_abl": ("HIGH_COLLATERAL" if (mt.get("DENSE-ABL", {}).get("selectivity", 0) < 5)
                                  else "LOW_COLLATERAL"),     # dense parent erasure (baseline f) outcome
            "predict_kg_selectivity": f"{mt.get('KG-ABL', {}).get('selectivity', 0):.2f}",
            "predict_dense_selectivity": f"{mt.get('DENSE-ABL', {}).get('selectivity', 0):.2f}",
            "metadata_family": c["family"], "metadata_subcontext": str(c["target_subcontext"]),
            "metadata_absorber_latent": c["absorber_latent"], "metadata_regime": c["regime"],
            "metadata_on_target": ci.get("KG-ABL_on_target", {}).get("mean"),
            "metadata_kg_collateral": ci.get("KG-ABL_collateral", {}).get("mean"),
            "metadata_dense_collateral": ci.get("DENSE-ABL_collateral", {}).get("mean"),
            "metadata_selectivity_ratio": c.get("headline_selectivity_ratio"),
            "metadata_kg_offtarget_footprint": mt.get("KG-ABL", {}).get("token_footprint_offtarget"),
            "metadata_dense_offtarget_footprint": mt.get("DENSE-ABL", {}).get("token_footprint_offtarget"),
            "metadata_dense_minus_kg_ci_lo": ci.get("dense_minus_kg_collateral", {}).get("ci_lo"),
            "metadata_dense_minus_kg_ci_hi": ci.get("dense_minus_kg_collateral", {}).get("ci_hi"),
            "metadata_firing_jaccard_with_parent": c.get("firing_jaccard_with_parent"),
            "metadata_parent_recall_hole": c.get("parent_recall_hole"),
        })
    if not per_context_examples:
        per_context_examples = [{"input": "no contexts", "output": "NONE", "predict_kg_abl": "NONE"}]
    if not case_examples:
        case_examples = [{"input": "no cases", "output": "NONE", "predict_kg_abl": "NONE"}]
    out["datasets"] = [
        {"dataset": "edit_locality_per_context", "examples": per_context_examples},
        {"dataset": "kg_surgical_edit_per_case", "examples": case_examples},
    ]
    logger.info(f"{el()} datasets: {len(per_context_examples)} per-context + {len(case_examples)} per-case examples")

    save_json(out, args.out)
    logger.info(f"{el()} SAVED {args.out}")
    logger.info(f"{el()} SUMMARY n_cases={len(all_cases)} n_surgical={len(surg)} "
                f"headline_ratio={summary['headline_selectivity_ratio']}")
    for c in all_cases:
        logger.info(f"  CASE {c['family']}/{c['target_subcontext']}: {c.get('verdict')} "
                    f"ratio={c.get('headline_selectivity_ratio')}")


if __name__ == "__main__":
    main()
