#!/usr/bin/env python
"""
M2 — CROSS-DICTIONARY REPLICATION of the iter-4 auditability spine on a SECOND Gemma-Scope SAE
dictionary of the SAME frozen model (google/gemma-2-2b).

Primary dictionary  : width-65k canonical at layer 12  (gemma-scope-2b-pt-res, average_l0 ~72)
Secondary (reduced) : an earlier residual layer (layer 9) at width-16k

The single most important difference vs iter-4: latent indices are DICTIONARY-SPECIFIC, so anchors AND
absorbers MUST be RE-DERIVED on each new dictionary (the 16k Georgia->16009 / Jordan->540,8347 IDs do NOT
carry over). Output is, per dictionary, a REPLICATION TABLE with honest deltas vs the 16k counts and a
REPLICATES / PARTIAL / DICTIONARY-DEPENDENT verdict per spine piece.

The four spine pieces replicated (all model-internal, $0 LLM for the core):
  (A) HOMOGRAPH RECALL-HOLES + firing-Jaccard router signals (re-derived anchor, per-country hole/jaccard)
  (B) BROAD K-track KG-repair loop -> recall recovery vs a random-single-latent control, paired bootstrap
      one-sided p, Benjamini-Hochberg FDR<=0.05 over ALL concepts; honest deltas vs the 16k survivor counts.
  (C) KG-localized SURGICAL sub-concept edit (KG-ABL single re-derived absorber) vs DENSE parent erasure
      (baseline f) vs RAND, next-token-KL on_target/collateral at matched effect, paired-bootstrap CIs.
  (D) ROUTER threshold transfer: apply FROZEN 16k thresholds (tau_h recall-hole lead, tau_j firing-Jaccard
      corroborating) WITHOUT refit + re-derive 65k-optimal; report balanced-accuracy + whether they transfer.

Reuses (copied + parametrized over the SAE) iter-4 experiment_1 (broad KG repair + BH FDR + member-labeling),
iter-4 experiment_2 (edit operators + behavioral side-effects + run_case), iter-3 experiment_4 (firing_jaccard
+ recall-hole + derive_1d router). The ONLY thing that changes vs iter-4 is the SAE config (release/width/layer)
and the fact that anchors/absorbers are re-derived per dictionary.

Usage:
  uv run method.py --smoke                                  # load 65k SAE + gating only
  uv run method.py --dicts 65k --families taxonomic --cap 40 --kl_prompts 16   # 65k taxonomic mini
  uv run method.py --dicts 65k                              # full 65k spine ($0 LLM)
  uv run method.py --dicts 65k,l9_16k                       # + reduced secondary-layer replication
  uv run method.py --dicts 65k --member_labeling            # + optional M7 member labeling (LLM, budget-gated)
"""
import os, sys, json, time, gc, argparse, hashlib, resource, glob, re
from pathlib import Path
from collections import defaultdict, Counter

import numpy as np

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "0")

from loguru import logger

# --------------------------------------------------------------------------- read-only inputs
ROOT = Path("/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop")
D1 = ROOT / "iter_1/gen_art/gen_art_dataset_1/full_data_out.json"           # first-letter spelling
D2 = ROOT / "iter_1/gen_art/gen_art_dataset_2/full_data_out.json"           # numeric + taxonomic
D2_MANIFEST = ROOT / "iter_1/gen_art/gen_art_dataset_2/manifest.json"       # absorption_readiness
D3 = ROOT / "iter_1/gen_art/gen_art_dataset_3/full_data_out.json"           # toxicity

WORK = Path("/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_2")
RESULTS = WORK / "results"
CACHE = WORK / "cache"
LOGS = WORK / "logs"
for d in (RESULTS, CACHE, LOGS):
    d.mkdir(exist_ok=True)

# --------------------------------------------------------------------------- SAE / model config
RELEASE_REPO = "google/gemma-scope-2b-pt-res"
MODEL_GATED = "google/gemma-2-2b"
MODEL_MIRROR = "unsloth/gemma-2-2b"                       # ungated mirror, vocab 256000
D_MODEL = 2304
MAXLEN = 192
BATCH = 16
SEED = 1234

# Per-DICTIONARY config. l0_target=100 => "canonical" (avg L0 closest to 100). hidden_search = candidate
# hidden_states indices to probe for the best SAE reconstruction (layer L -> hidden_states[L+1]).
DICTS = {
    "65k":     {"layer": 12, "width": "65k", "l0_target": 100, "expect_l0": 72,
                "hidden_search": (11, 12, 13, 14), "expect_hidden": 13, "expect_dsae": 65536,
                "reduced": False},
    "l9_16k":  {"layer": 9,  "width": "16k", "l0_target": 100, "expect_l0": None,
                "hidden_search": (8, 9, 10, 11), "expect_hidden": 10, "expect_dsae": 16384,
                "reduced": True},
    "l6_16k":  {"layer": 6,  "width": "16k", "l0_target": 100, "expect_l0": None,
                "hidden_search": (5, 6, 7, 8), "expect_hidden": 7, "expect_dsae": 16384,
                "reduced": True},
}

# --------------------------------------------------------------------------- thresholds (iter-4 verbatim)
N_MIN_EVAL = 30
N_MIN_RELAX = 15
N_MIN_SEL = 10
HOLE_RECALL_MAX = 0.60
B_BOOT = 10000
N_SHUFFLE = 2000
KG_JACCARD_MAX = 0.10
KG_PREC_MIN = 0.70
SPURIOUS_FIRE_FLOOR = 0.01
FDR_ALPHA = 0.05
EPS = 1e-8

# --------------------------------------------------------------------------- 16k REFERENCE (iter-4 results)
REF_16K = {
    "gating_cosine": 0.9189, "gating_L0": 87.9, "gating_layer_idx": 13,
    "per_family_survive_FDR": {"spelling": 14, "homograph_taxonomic": 6, "numeric": 10},
    "n_repairs_tested": 69, "n_holes": 54, "n_survive_FDR": 30,
    "router_tau_h": 0.7774337479718767, "router_tau_j": 0.05,
    "router_recall_hole_balanced_acc": 1.0, "router_firing_jaccard_balanced_acc": 0.9167,
    "surgical_georgia": {"verdict": "SURGICAL_EDIT_CONFIRMED", "selectivity_ratio": 1722.46,
                         "kg_collateral": 2.876e-05, "dense_collateral": 0.04955, "firing_jaccard": 0.012,
                         "parent_recall_hole": 0.77},
    "surgical_jordan": {"selectivity_ratio": 2722.0, "kg_collateral": 0.0, "dense_collateral": 0.0721,
                        "firing_jaccard": 0.014, "parent_recall_hole": 0.68},
    "regime_router_map": {"absorption_mean_selectivity": 1452.47, "absorption_mean_firing_jaccard": 0.0141,
                          "co_firing_mean_selectivity": 2.377, "co_firing_mean_firing_jaccard": 0.8776},
    "member_labeling_agreement": 0.7303, "member_labeling_gap": 0.6344,
}

# --------------------------------------------------------------------------- LLM (optional member-labeling)
J_ENSEMBLE = 3
LLM_MODEL = "anthropic/claude-haiku-4.5"
LLM_FALLBACKS = ["google/gemini-3.1-flash-lite", "deepseek/deepseek-v3.2-exp"]
LLM_PRICE = {
    "anthropic/claude-haiku-4.5": (1.00e-6, 5.00e-6),
    "google/gemini-3.1-flash-lite": (0.25e-6, 1.50e-6),
    "deepseek/deepseek-v3.2-exp": (0.20e-6, 0.40e-6),
}
LLM_HARD_STOP = 10.0
LLM_TARGET = 0.5

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
        avail = 48 * 1024**3
        resource.setrlimit(resource.RLIMIT_AS, (avail * 3, avail * 3))
    except Exception as e:  # noqa: BLE001
        logger.warning(f"could not set RLIMIT_AS: {e}")


# =========================================================================== SAE (parametrized by dict)
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
        return (pre > self.threshold) * t.nn.functional.relu(pre)   # JumpReLU: fire iff pre>threshold

    def decode(self, z):
        return z @ self.W_dec + self.b_dec


def resolve_sae_path(cfg):
    """Find params.npz for layer{cfg.layer}/width{cfg.width}, avg L0 closest to cfg.l0_target.
    Checks local HF cache first; else lists the repo tree and downloads the closest-to-target file."""
    layer, width, target = cfg["layer"], cfg["width"], cfg["l0_target"]
    base = os.path.expanduser(f"~/.cache/huggingface/hub/models--{RELEASE_REPO.replace('/','--')}")
    pats = glob.glob(f"{base}/snapshots/*/layer_{layer}/width_{width}/average_l0_*/params.npz")
    if pats:
        chosen = min(pats, key=lambda p: abs(_l0_of(p) - target))
        return chosen, _l0_of(chosen), "cache"
    # list repo tree -> pick closest-to-target l0 -> download exactly that file
    from huggingface_hub import HfApi, hf_hub_download
    api = HfApi()
    files = api.list_repo_files(RELEASE_REPO, token=os.environ.get("HF_TOKEN"))
    cands = [f for f in files if re.match(rf"layer_{layer}/width_{width}/average_l0_\d+/params\.npz$", f)]
    if not cands:
        raise RuntimeError(f"no params.npz for layer_{layer}/width_{width} in {RELEASE_REPO}")
    l0s = sorted({_l0_of(f) for f in cands})
    best_l0 = min(l0s, key=lambda v: abs(v - target))
    sae_id = f"layer_{layer}/width_{width}/average_l0_{best_l0}/params.npz"
    logger.info(f"{el()} available L0s for layer_{layer}/width_{width}: {l0s} -> picking {best_l0} (closest to {target})")
    path = hf_hub_download(RELEASE_REPO, sae_id, token=os.environ.get("HF_TOKEN"))
    return path, best_l0, "download"


def _l0_of(p):
    m = re.search(r"average_l0_(\d+)", str(p))
    return int(m.group(1)) if m else 99999


def load_sae(torch, cfg, name):
    path, l0, src = resolve_sae_path(cfg)
    logger.info(f"{el()} [{name}] loading SAE ({src}) avg_l0={l0} from {path}")
    sae = JumpReLUSAE(path, DEVICE, torch)
    assert sae.d_model == D_MODEL, f"unexpected d_model {sae.d_model}"
    if cfg.get("expect_dsae"):
        assert sae.d_sae == cfg["expect_dsae"], f"expected d_sae {cfg['expect_dsae']} got {sae.d_sae}"
    if cfg.get("expect_l0") is not None and l0 != cfg["expect_l0"]:
        logger.warning(f"[{name}] resolved avg_l0={l0} != expected {cfg['expect_l0']}")
    logger.info(f"{el()} [{name}] SAE loaded d_sae={sae.d_sae} d_model={sae.d_model} avg_l0={l0}")
    sae.avg_l0 = l0
    sae.sae_id = f"layer_{cfg['layer']}/width_{cfg['width']}/average_l0_{l0}"
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
        self.layer_idx = 13
        self._cap = {}
        self._handle = None
        logger.info(f"{el()} model loaded ({self.model_id}) d_model={self.d_model} "
                    f"n_layers={self.model.config.num_hidden_layers} vocab={len(self.tok)}")

    def edit_layer(self):
        return self.model.model.layers[self.layer_idx - 1]

    def _install_hook(self, layer_idx):
        if self._handle is not None:
            self._handle.remove()
        def _hook(_m, _i, out):
            self._cap["resid"] = out[0] if isinstance(out, (tuple, list)) else out
        self._handle = self.model.model.layers[layer_idx - 1].register_forward_hook(_hook)
        self.layer_idx = layer_idx

    def determine_layer_idx(self, rows, sae, hidden_search):
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
        for hi in hidden_search:
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
            if not vecs:
                continue
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
                    pos = [t for t in range(T) if offs[i][t][1] > offs[i][t][0]]
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
            if (b0 // BATCH) % 80 == 0:
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


# =========================================================================== encoding cache (per-dict)
def encode_cached(dict_name, sae, mb, concept_key, rows, whole_sentence=False):
    import scipy.sparse as sp
    fp = hashlib.sha1(
        ("|".join(r["input"][:24] for r in rows[:: max(1, len(rows) // 64)])).encode("utf-8")
    ).hexdigest()[:12]
    key = f"enc_{dict_name}_{sae.sae_id.replace('/', '_')}_{concept_key}_{len(rows)}_ws{int(whole_sentence)}_{fp}"
    npz = CACHE / f"{key}.npz"
    meta = CACHE / f"{key}.json"
    if npz.exists() and meta.exists():
        try:
            d = np.load(str(npz), allow_pickle=False)
            lat = sp.csr_matrix((d["lat_data"], d["lat_idx"], d["lat_ptr"]), shape=(len(rows), sae.d_sae))
            m = json.loads(meta.read_text())
            logger.info(f"{el()} [cache HIT] {dict_name}/{concept_key} n={len(rows)} align={m.get('align')}")
            return lat, d["resid"], float(m.get("align", 1.0))
        except Exception as e:  # noqa: BLE001
            logger.warning(f"  cache load failed ({e}); re-encoding")
    lat, resid, align = mb.encode_rows(rows, sae, whole_sentence=whole_sentence)
    try:
        np.savez(str(npz), lat_data=lat.data, lat_idx=lat.indices, lat_ptr=lat.indptr, resid=resid)
        meta.write_text(json.dumps({"n": len(rows), "model": mb.model_id, "align": align}))
    except Exception as e:  # noqa: BLE001
        logger.warning(f"  cache save failed ({e})")
    return lat, resid, align


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
        sp_ = r.get("metadata_target_char_in_window")
        r["_span"] = tuple(sp_) if sp_ else None
        tp = r.get("metadata_token_position")
        r["_ti"] = [int(tp)] if tp is not None else None
    else:
        sp_ = r.get("metadata_word_char_span")
        r["_span"] = tuple(sp_) if sp_ else None
        r["_ti"] = None
    r["_target"] = r.get("metadata_target_word")
    return r


def load_d2(dataset_name):
    blob = json.loads(D2.read_text())
    ds = next(d for d in blob["datasets"] if d["dataset"] == dataset_name)
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
                rr = dict(r); rr["_span"] = None; rr["_ti"] = None; rr["_target"] = None
                rows.append(rr)
    return rows


def load_readiness():
    try:
        m = json.loads(D2_MANIFEST.read_text())
        return m.get("absorption_readiness", {})
    except Exception:  # noqa: BLE001
        return {}


# =========================================================================== stats
def paired_bootstrap_diff_items(diff_per_item, B=B_BOOT):
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
        return {"mean": 0.0, "ci_lo": 0.0, "ci_hi": 0.0, "n": 0, "excl_0": False}
    idx = rng.integers(0, n, size=(B, n))
    bs = v[idx].mean(1)
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return {"mean": float(v.mean()), "ci_lo": float(lo), "ci_hi": float(hi), "n": int(n),
            "excl_0": bool(lo > 0 or hi < 0)}


def benjamini_hochberg(pvals, alpha=FDR_ALPHA):
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


def firing_jaccard(fires_a, fires_b):
    a = np.asarray(fires_a).astype(bool); b = np.asarray(fires_b).astype(bool)
    inter = int((a & b).sum()); union = int((a | b).sum())
    return (inter / union) if union > 0 else 0.0


def _auc(scores, labels):
    from sklearn.metrics import roc_auc_score
    labels = np.asarray(labels)
    if labels.min() == labels.max():
        return 0.5
    try:
        return float(roc_auc_score(labels, scores))
    except Exception:  # noqa: BLE001
        return 0.5


def cols_auc(mat, y):
    """Per-column AUC (mat [n,k], y [n]) via rank-sum; returns [k]."""
    from scipy.stats import rankdata
    y = np.asarray(y).astype(bool)
    n1 = int(y.sum()); n0 = int((~y).sum())
    if n1 == 0 or n0 == 0:
        return np.full(mat.shape[1], np.nan)
    out = np.empty(mat.shape[1])
    for j in range(mat.shape[1]):
        col = mat[:, j]
        if np.all(col == col[0]):
            out[j] = 0.5; continue
        ranks = rankdata(col)
        out[j] = (ranks[y].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
    return out


# =========================================================================== ANCHOR re-derivation
def rederive_anchor(cr, prec, A_on, lat_csr_corpus_pos):
    """Re-derive the parent anchor on THIS dictionary: highest content-flip coverage among precision>=0.7
    content-responsive latents, validated by the unsupervised corpus firing-floor (>= SPURIOUS_FIRE_FLOOR).
    Returns (anchor|None, info). lat_csr_corpus_pos = corpus-positive sub-matrix (rows x d_sae) for the floor."""
    if len(cr) == 0:
        return None, {"reason": "no_content_responsive"}
    cover = (A_on > 0).sum(0)                                   # content-flip recall proxy
    pool = cr[prec[cr] >= 0.7]
    if len(pool) == 0:
        pool = cr
    order = pool[np.argsort(-cover[pool])]                      # highest coverage first
    # corpus firing-floor validation (kills letter-I-1227 spurious anchors)
    ncorp = lat_csr_corpus_pos.shape[0] if lat_csr_corpus_pos is not None else 0
    tried = []
    for cand in order[:25]:
        if ncorp:
            fire = float((np.asarray(lat_csr_corpus_pos[:, [int(cand)]].todense()) > 0).mean())
        else:
            fire = 1.0
        tried.append({"latent": int(cand), "content_cover": int(cover[cand]),
                      "content_prec": float(prec[cand]), "corpus_fire": fire})
        if fire >= SPURIOUS_FIRE_FLOOR:
            return int(cand), {"anchor": int(cand), "content_cover": int(cover[cand]),
                               "content_prec": float(prec[cand]), "corpus_fire_rate": fire,
                               "firing_floor_validated": True, "candidates_tried": tried[:8]}
    # none cleared the floor
    best = int(order[0])
    return best, {"anchor": best, "firing_floor_validated": False,
                  "reason": "no_candidate_cleared_corpus_firing_floor",
                  "corpus_fire_rate": tried[0]["corpus_fire"] if tried else 0.0,
                  "candidates_tried": tried[:8]}


# =========================================================================== BROAD K-track KG derivation
def derive_broad_kg(anchor, cr, lat_csr, sub_arr, label_arr, sel_mask, eligible_X,
                    jaccard_max=KG_JACCARD_MAX, prec_min=KG_PREC_MIN, min_sel=N_MIN_SEL):
    """For EVERY eligible sub-context X, NAME a covering absorber via the K-track greedy on the SELECTION
    split (non-circular vs eval): argmax recall over content-responsive latents with jaccard(l,anchor)<max
    and subctx-precision>=prec_min."""
    cr = np.asarray([int(l) for l in cr if int(l) != int(anchor)], dtype=np.int64)
    sel_pos = np.where(sel_mask & (label_arr == 1))[0]
    if len(sel_pos) == 0 or len(cr) == 0:
        return {}, {}
    F = (np.asarray(lat_csr[sel_pos][:, cr.tolist()].todense()) > 0)
    anchor_fire = (np.asarray(lat_csr[sel_pos][:, [int(anchor)]].todense()) > 0).ravel()
    sub_sel = np.asarray(sub_arr)[sel_pos]
    inter = (F & anchor_fire[:, None]).sum(0).astype(np.float64)
    union = (F | anchor_fire[:, None]).sum(0).astype(np.float64)
    jac = np.where(union > 0, inter / np.maximum(union, 1.0), 1.0)
    fire_count = F.sum(0).astype(np.float64)
    per_X, anchor_recall_by_X = {}, {}
    for X in eligible_X:
        xmask = (sub_sel == X)
        n_x = int(xmask.sum())
        if n_x < min_sel:
            per_X[X] = {"kg_absorber": None, "reason": f"too_few_selection_positives({n_x})", "n_sel_pos": n_x}
            continue
        anchor_recall_by_X[X] = float(anchor_fire[xmask].mean())
        x_fire = F[xmask].sum(0).astype(np.float64)
        recall_X = x_fire / n_x
        prec_X = np.where(fire_count > 0, x_fire / np.maximum(fire_count, 1.0), 0.0)
        ok = (jac < jaccard_max) & (prec_X >= prec_min) & (fire_count > 0)
        if not ok.any():
            per_X[X] = {"kg_absorber": None, "reason": "no_low_jaccard_high_precision_covering_latent",
                        "n_sel_pos": n_x, "anchor_recall_selection": anchor_recall_by_X[X]}
            continue
        cand = np.where(ok)[0]
        best = cand[int(np.argmax(recall_X[cand]))]
        per_X[X] = {"kg_absorber": int(cr[best]), "recall_on_X_selection": float(recall_X[best]),
                    "subctx_precision_selection": float(prec_X[best]), "jaccard_anchor": float(jac[best]),
                    "n_sel_pos": n_x, "anchor_recall_selection": anchor_recall_by_X[X]}
    del F
    return per_X, anchor_recall_by_X


def derive_diagnostic_absorber(X, anchor, cr, lat_csr, resid, probe_dir, sub_arr, label_arr, sel_mask, W_dec_np):
    """FORM-FREE (Chanin A.13 / SAEBench absorption_fraction) second naming: among content-responsive
    latents, the one whose reconstruction contribution z_l*W_dec[l] projects most onto the parent probe
    direction at X-positive HOLE tokens (where the anchor does not fire). Independent of the K-track."""
    cr = np.asarray([int(l) for l in cr if int(l) != int(anchor)], dtype=np.int64)
    if len(cr) == 0:
        return None
    x_rows = np.where((np.asarray(sub_arr) == X) & (label_arr == 1) & sel_mask)[0]
    if len(x_rows) < N_MIN_SEL:
        return None
    anchor_fire = (np.asarray(lat_csr[x_rows][:, [int(anchor)]].todense()) > 0).ravel()
    hole_rows = x_rows[~anchor_fire]
    if len(hole_rows) < 5:
        hole_rows = x_rows
    Z = np.asarray(lat_csr[hole_rows][:, cr.tolist()].todense())          # [n_hole, |cr|] (max-pooled act)
    proj = (W_dec_np[cr] @ probe_dir)                                     # [|cr|] decoder dir . probe dir
    score = Z.mean(0) * proj                                              # mean activation * projection
    if not np.isfinite(score).any() or score.max() <= 0:
        return None
    return int(cr[int(np.argmax(score))])


# =========================================================================== M1a REPAIR LOOP
def repair_loop(concept, anchor, candidates, lat_csr, sub_arr, label_arr, responsive, member_set,
                sel_mask, eval_mask):
    resp = np.asarray(responsive)
    resp_ctrl = np.array([int(l) for l in resp if int(l) not in member_set], dtype=np.int64)
    out = {"per_subcontext": {}, "honest_negatives": [], "n_measured_successful_repairs": 0,
           "n_control_latents": int(len(resp_ctrl))}

    def fire(rows_idx, lat_ids):
        if len(rows_idx) == 0 or len(lat_ids) == 0:
            return np.zeros((len(rows_idx), len(lat_ids)), dtype=bool)
        return (np.asarray(lat_csr[rows_idx][:, list(lat_ids)].todense()) > 0)

    sel_pos_rows = np.where(sel_mask & (label_arr == 1))[0]
    overall_anchor_sel = float(fire(sel_pos_rows, [anchor])[:, 0].mean()) if len(sel_pos_rows) else 1.0
    out["overall_anchor_recall_selection"] = overall_anchor_sel

    for cand in candidates:
        X = cand["X"]
        x_mask = (np.asarray(sub_arr) == X) & (label_arr == 1)
        sel_rows = np.where(x_mask & sel_mask)[0]
        eval_rows = np.where(x_mask & eval_mask)[0]
        n_eval = len(eval_rows); n_sel = len(sel_rows)
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
                 "n_eval_ge_pref": bool(n_eval >= N_MIN_EVAL), "kg_derivation": cand.get("derivation"),
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
            ci = paired_bootstrap_diff_items(diff_perwin)
            succ = bool(ci["excl_0"] and ci["diff"] > 0)
            entry["variants"][vname] = {
                "absorber_latent": int(latid), "recall_anchor_plus_kg": kg_recall, "gain_kg": float(gain_kg),
                "kg_percentile_vs_random": pct, "paired_bootstrap_CI_kg_minus_random": ci,
                "p_value_one_sided": ci["p_one_sided"], "measured_success": succ,
                "same_as_ktrack": bool(vname == "kg_diagnostic" and latid == cand.get("kg_absorber")),
                "bh_q": None, "survives_FDR": None}
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
                    f"rand_p95={entry['random_gain']['p95']:.3f} n_eval={n_eval}")
    return out


# =========================================================================== (k) localization check
def k_localization_check(concept, resid, label, fold, sae_W_dec, anchor, kg_absorbers, eval_rows_by_X, lam=20.0):
    from sklearn.linear_model import LogisticRegression
    tr = np.where(fold == "selection")[0]
    if len(tr) < 20 or len(np.unique(label[tr])) < 2:
        return {"status": "not_run", "reason": "insufficient selection rows / single class for (k) probe"}
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
    anchor_rank = int(np.where(order == int(anchor))[0][0]) + 1
    ranks = {}
    for c, latid in kg_absorbers.items():
        r = int(np.where(order == int(latid))[0][0]) + 1
        ranks[str(c)] = {"latent": int(latid), "cos": float(cos[int(latid)]), "rank_by_abscos": r}
    dominates = bool(top_abs >= 0.5 and top_abs >= 2.0 * max(second_abs, 1e-9))
    kg_is_argmax = any(int(latid) == argmax_lat for latid in kg_absorbers.values())
    return {"status": "run", "variant": "JTT(ERM->upweight error set lambda=%g->retrain)" % lam,
            "n_train": int(len(tr)), "erm_train_acc": float((pred == ytr).mean()),
            "error_set_size": int(err.sum()), "projection_argmax_latent": argmax_lat,
            "projection_top_abscos": top_abs, "projection_second_abscos": second_abs,
            "single_latent_dominates": dominates, "anchor_projection_rank_by_abscos": anchor_rank,
            "argmax_is_anchor": bool(argmax_lat == int(anchor)), "kg_absorber_is_argmax": bool(kg_is_argmax),
            "kg_absorber_projection_ranks": ranks,
            "conclusion": ("KG names exactly one addable auditable latent per sub-context; the (k) "
                           "example-reweighting probe yields a dense hyperplane that does NOT localize to "
                           "any single SAE latent -> no per-sub-context handle.")}


# =========================================================================== PROBE + EDIT OPERATORS (R2)
class ParentProbe:
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
        self.u_t = torch.tensor(self.d_mu, device=DEVICE)
        wn = self.w / (np.linalg.norm(self.w) + 1e-9)
        self.cos_probe_dmu = float(wn @ self.d_mu)

    def margin(self, H):
        return H @ self.w_t + self.b_t

    def score(self, H):
        return self.torch.sigmoid(self.margin(H))


def edit_detection_curve(torch, sae, probe, H, op, l=None, u=None, v=None, scales=None, sign=+1):
    H = H.to(torch.float32)
    m_before = probe.margin(H); p_before = torch.sigmoid(m_before)
    if op == "abl_latent":
        z = sae.encode(H)
        base = z[:, l:l+1] * sae.W_dec[l].unsqueeze(0); sgn_h = -1.0
    elif op == "erase_dir":
        base = (H @ u).unsqueeze(1) * u.unsqueeze(0); sgn_h = -1.0
    elif op == "add_latent":
        base = v.unsqueeze(0); sgn_h = +1.0
    elif op == "add_dir":
        base = u.unsqueeze(0); sgn_h = -1.0
    else:
        raise ValueError(op)
    eff_m, eff_p = [], []
    for s in scales:
        Ha = H + (sgn_h * s) * base
        m_after = probe.margin(Ha)
        eff_m.append((sign * (m_before - m_after)).cpu().numpy())
        eff_p.append((sign * (p_before - torch.sigmoid(m_after))).cpu().numpy())
    return np.stack(eff_m, 1), np.stack(eff_p, 1)


def make_edit_hook(torch, sae, kind, l=None, u=None, v=None, scale=0.0, counter=None):
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
    torch = mb.torch; tok = mb.tok
    layer = mb.edit_layer()
    counter = {"edited": 0, "total": 0}
    hook = make_edit_hook(torch, sae, kind, l=l, u=u, v=v, scale=scale, counter=counter)
    handle = layer.register_forward_hook(hook)
    try:
        tok.padding_side = "left"
        kls = []
        for b0 in range(0, len(U_texts), 16):
            bp = U_texts[b0:b0 + 16]
            enc = tok(bp, return_tensors="pt", padding=True, truncation=True, max_length=64, add_special_tokens=True)
            enc = {k: vv.to(DEVICE) for k, vv in enc.items()}
            with torch.no_grad():
                o = mb.model(**enc)
            lp = torch.log_softmax(o.logits[:, -1, :].to(torch.float32), dim=-1).cpu()
            blp = base_lp[b0:b0 + len(bp)]
            p = lp.exp()
            kl = (p * (lp - blp)).sum(1)
            kls.append(kl.numpy())
        tok.padding_side = "right"
        kl_mean = float(np.concatenate(kls).mean())
        losses = []
        for t in U_texts:
            enc = tok(t, return_tensors="pt", truncation=True, max_length=64, add_special_tokens=True)
            enc = {k: vv.to(DEVICE) for k, vv in enc.items()}
            with torch.no_grad():
                o = mb.model(**enc, labels=enc["input_ids"])
            losses.append(float(o.loss))
        ppl = float(np.exp(np.mean(losses)))
    finally:
        handle.remove(); tok.padding_side = "right"
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


def forward_pos_logprobs(mb, sae, rows, kind=None, l=None, u=None, v=None, scale=0.0,
                         whole_sentence=False, max_len=96, batch=8):
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


def behavioral_curve(mb, sae, rows, base_lp, kind, l=None, u=None, v=None, scales=None, whole_sentence=False):
    cols = [np.zeros(len(rows))]; foots = [0.0]
    for s in scales[1:]:
        elp, foot = forward_pos_logprobs(mb, sae, rows, kind=kind, l=l, u=u, v=v, scale=s,
                                         whole_sentence=whole_sentence)
        cols.append(kl_rows(elp, base_lp)); foots.append(foot)
    return np.stack(cols, 1), foots


def _interp_at(xs, ys, x0):
    xs = np.asarray(xs, float); ys = np.asarray(ys, float)
    order = np.argsort(xs)
    return float(np.interp(x0, xs[order], ys[order]))


def _scale_for_on_target(scales, on_curve, target):
    s = np.asarray(scales, float); o = np.asarray(on_curve, float)
    order = np.argsort(o)
    return float(np.interp(target, o[order], s[order]))


DET_GRID_ABL = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0]
BEH_ABL = [0.0, 0.5, 1.0, 2.0]
BEH_ADD = [0.0, 1.0, 4.0]


def pick_random_latents(lat_csr, absorber, responsive, member_set, n=12):
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
    sel = rng.choice(cand, size=n, replace=False) if len(cand) > n else cand
    return [int(x) for x in sel], float(target_rate)


def run_case(*, torch, sae, mb, family, X, absorber, absorber_precision, regime, probe,
             H_target, H_siblings, sibling_names, H_broad, target_rows, sibling_rows, U_texts, base_lp,
             base_ppl, rand_latents, parent_latent, lat_csr_for_jaccard, target_rows_for_jaccard,
             whole_sentence=False, beh_target_cap=60, beh_sib_cap=180):
    logger.info(f"\n{el()} --- CASE {family} / X={X} / absorber={absorber} ({regime}) ---")
    Wdec_l_unit = sae.W_dec_unit[absorber]
    trows = target_rows[:beh_target_cap]; srows = sibling_rows[:beh_sib_cap]
    base_t, _ = forward_pos_logprobs(mb, sae, trows, whole_sentence=whole_sentence)
    base_s, _ = forward_pos_logprobs(mb, sae, srows, whole_sentence=whole_sentence)
    curves = {}; beh = {}

    def run_beh(method, kind, scales, l=None, u=None, v=None):
        on_kl, foot_on = behavioral_curve(mb, sae, trows, base_t, kind, l=l, u=u, v=v, scales=scales,
                                          whole_sentence=whole_sentence)
        sib_kl, foot_sib = behavioral_curve(mb, sae, srows, base_s, kind, l=l, u=u, v=v, scales=scales,
                                            whole_sentence=whole_sentence)
        beh[method] = {"on": on_kl, "sib": sib_kl, "scales": scales, "footprint_on": foot_on,
                       "footprint_sib": foot_sib}
        curves[method] = {"scales": scales, "beh_on_target": on_kl.mean(0).tolist(),
                          "beh_collateral": sib_kl.mean(0).tolist(), "footprint_on_target_ctx": foot_on,
                          "footprint_sibling_ctx": foot_sib}

    run_beh("KG-ABL", "abl_latent", BEH_ABL, l=absorber)
    run_beh("DENSE-ABL", "erase_dir", BEH_ABL, u=probe.u_t)
    z_typ = float(sae.encode(H_target.to(torch.float32))[:, absorber].mean()) if H_target.shape[0] else 1.0
    wnorm = float(sae.W_dec[absorber].norm())
    add_scales = [c * max(z_typ, 1e-3) * wnorm for c in BEH_ADD]
    run_beh("KG-ADD", "add_latent", add_scales, v=Wdec_l_unit)
    curves["KG-ADD"]["alpha"] = add_scales
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
    beh["RAND"] = {"on": rand_on, "sib": rand_sib, "scales": [0.0, 1.0], "footprint_on": rfoot_on,
                   "footprint_sib": rfoot_sib}
    curves["RAND"] = {"scales": [0.0, 1.0], "beh_on_target": rand_on.mean(0).tolist(),
                      "beh_collateral": rand_sib.mean(0).tolist(), "footprint_on_target_ctx": rfoot_on,
                      "footprint_sibling_ctx": rfoot_sib, "n_draws": nd}

    pm = {}
    for m, (op, kw) in {"KG-ABL": ("abl_latent", {"l": absorber}),
                        "DENSE-ABL": ("erase_dir", {"u": probe.u_t})}.items():
        et, etp = edit_detection_curve(torch, sae, probe, H_target, op, scales=DET_GRID_ABL, sign=+1, **kw)
        es, _ = edit_detection_curve(torch, sae, probe, H_siblings, op, scales=DET_GRID_ABL, sign=+1, **kw)
        pm[m] = {"scales": DET_GRID_ABL, "on_target_margin": et.mean(0).tolist(),
                 "collateral_margin": es.mean(0).tolist(), "on_target_prob": etp.mean(0).tolist()}
    curves["KG-ABL"]["probe_margin"] = pm["KG-ABL"]; curves["DENSE-ABL"]["probe_margin"] = pm["DENSE-ABL"]

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

    target_on = max(1e-4, min(float(max(curves["KG-ABL"]["beh_on_target"])),
                              float(max(curves["DENSE-ABL"]["beh_on_target"]))) * 0.8)
    s_kg = _scale_for_on_target(BEH_ABL, curves["KG-ABL"]["beh_on_target"], target_on)
    s_de = _scale_for_on_target(BEH_ABL, curves["DENSE-ABL"]["beh_on_target"], target_on)

    def per_ctx_at(arr, scales, s0):
        return np.array([np.interp(s0, scales, arr[i]) for i in range(arr.shape[0])])
    kg_on_at = per_ctx_at(beh["KG-ABL"]["on"], BEH_ABL, s_kg)
    kg_sib_at = per_ctx_at(beh["KG-ABL"]["sib"], BEH_ABL, s_kg)
    de_sib_at = per_ctx_at(beh["DENSE-ABL"]["sib"], BEH_ABL, s_de)

    matched = {}
    for m in ("KG-ABL", "DENSE-ABL", "RAND", "KG-ADD"):
        on_c = curves[m]["beh_on_target"]; col_c = curves[m]["beh_collateral"]
        reaches = bool(max(on_c) >= target_on)
        col = _interp_at(on_c, col_c, target_on)
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

    on_ci = bootstrap_mean_ci(kg_on_at)
    kg_col_ci = bootstrap_mean_ci(kg_sib_at)
    de_col_ci = bootstrap_mean_ci(de_sib_at)
    col_diff_ci = paired_bootstrap_diff(de_sib_at, kg_sib_at)

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
    sel_kg = float(matched["KG-ABL"]["selectivity"])
    on_ok = bool(on_ci.get("excl_0") and on_ci["mean"] > 0)
    dominates = bool(col_diff_ci["excl_0"] and col_diff_ci["diff"] > 0)
    fp_off = matched["KG-ABL"].get("token_footprint_offtarget", 1.0)
    clean = bool(sel_kg >= 20 and fp_off < 0.05 and ratio >= 20)
    if on_ok and dominates and clean:
        verdict = "SURGICAL_EDIT_CONFIRMED"
    elif on_ok and dominates:
        verdict = "PARTIAL_CO_FIRING_AS_PREDICTED" if regime == "co-firing" else "PARTIAL_SURGICAL"
    elif on_ok and not dominates:
        verdict = "NO_SELECTIVITY_ADVANTAGE"
    else:
        verdict = "NO_ON_TARGET_EFFECT"
    logger.info(f"  {family}/{X}: beh_on={on_ci['mean']:.4f}(CI {on_ci['ci_lo']:.4f}..{on_ci['ci_hi']:.4f}) "
                f"KG_col={kg_col_ci['mean']:.5f} DE_col={de_col_ci['mean']:.5f} sel_KG={sel_kg:.1f} "
                f"ratio={ratio:.1f} fpoff={fp_off:.4f} jac={fj} hole={hole} -> {verdict}")

    i1 = BEH_ABL.index(1.0)
    kg_on_1 = beh["KG-ABL"]["on"][:, i1]; kg_sib_1 = beh["KG-ABL"]["sib"][:, i1]
    de_on_1 = beh["DENSE-ABL"]["on"][:, i1]; de_sib_1 = beh["DENSE-ABL"]["sib"][:, i1]
    rand_on_1 = beh["RAND"]["on"][:, 1] if beh["RAND"]["on"].shape[0] else np.zeros(0)
    rand_sib_1 = beh["RAND"]["sib"][:, 1] if beh["RAND"]["sib"].shape[0] else np.zeros(0)
    noise = np.concatenate([kg_sib_1, rand_sib_1, rand_on_1]) if len(kg_sib_1) else np.zeros(1)
    tau = max(2e-3, 4.0 * float(np.percentile(noise, 90)))
    def _lab(vv):
        return "AFFECTED" if float(vv) > tau else "UNAFFECTED"
    pred_rows = []
    for i in range(min(len(trows), 30)):
        pred_rows.append({
            "input": f"[{family}|{X}] edit-locality probe (target): {trows[i]['input'][:200]}",
            "output": "ON_TARGET", "predict_kg_abl": _lab(kg_on_1[i]), "predict_dense_abl": _lab(de_on_1[i]),
            "metadata_family": family, "metadata_subcontext": str(X), "metadata_role": "target",
            "metadata_absorber_latent": int(absorber), "metadata_regime": regime,
            "metadata_kl_kg_abl": round(float(kg_on_1[i]), 6), "metadata_kl_dense_abl": round(float(de_on_1[i]), 6),
            "metadata_kl_threshold": round(float(tau), 6),
            "metadata_kg_correct": bool(kg_on_1[i] > tau), "metadata_dense_correct": bool(de_on_1[i] > tau)})
    for i in range(min(len(srows), 30)):
        pred_rows.append({
            "input": f"[{family}|sibling-of-{X}] edit-locality probe (sibling): {srows[i]['input'][:200]}",
            "output": "OFF_TARGET_SIBLING", "predict_kg_abl": _lab(kg_sib_1[i]), "predict_dense_abl": _lab(de_sib_1[i]),
            "metadata_family": family, "metadata_subcontext": str(X), "metadata_role": "sibling",
            "metadata_absorber_latent": int(absorber), "metadata_regime": regime,
            "metadata_kl_kg_abl": round(float(kg_sib_1[i]), 6), "metadata_kl_dense_abl": round(float(de_sib_1[i]), 6),
            "metadata_kl_threshold": round(float(tau), 6),
            "metadata_kg_correct": bool(kg_sib_1[i] <= tau), "metadata_dense_correct": bool(de_sib_1[i] <= tau)})

    return {"prediction_rows": pred_rows, "decision_threshold_tau": float(tau), "family": family,
            "target_subcontext": X, "absorber_latent": int(absorber), "absorber_precision": absorber_precision,
            "regime": regime, "probe_train_auc": probe.train_auc, "probe_cos_with_diffmean": probe.cos_probe_dmu,
            "firing_jaccard_with_parent": fj, "parent_recall_hole": hole, "n_target_ctx": len(trows),
            "n_sibling_ctx": len(srows), "siblings": sibling_names,
            "primary_measure": "behavioral_next_token_KL_at_edited_token_position", "curves": curves,
            "matched": matched, "matched_scale_kg": s_kg, "matched_scale_dense": s_de,
            "selectivity_CIs": {"KG-ABL_on_target": on_ci, "KG-ABL_collateral": kg_col_ci,
                                "DENSE-ABL_collateral": de_col_ci, "dense_minus_kg_collateral": col_diff_ci},
            "verdict": verdict, "headline_selectivity_ratio": ratio}


# =========================================================================== ROUTER (R3)
def balanced_accuracy(pred, truth):
    pred = np.asarray(pred); truth = np.asarray(truth)
    accs = []
    for cls in ["absorption", "co_firing"]:
        m = truth == cls
        if m.sum() == 0:
            continue
        accs.append((pred[m] == cls).mean())
    return float(np.mean(accs)) if accs else float("nan")


def derive_1d(concepts, key, lt):
    vals = np.array([c[key] for c in concepts], float)
    truth = np.array([c["ground_truth_regime"] for c in concepts])
    if len(vals) == 0 or not np.isfinite(vals).any():
        return float("nan"), float("nan"), []
    grid = np.linspace(float(np.nanmin(vals)), float(np.nanmax(vals)), 41)
    sweep = []
    for tau in grid:
        pred = np.where(vals < tau if lt else vals > tau, "absorption", "co_firing")
        sweep.append({"tau": float(tau), "balanced_acc": balanced_accuracy(pred, truth)})
    best = max(sweep, key=lambda r: r["balanced_acc"])
    return best["tau"], best["balanced_acc"], sweep


def apply_frozen_threshold(concepts, key, tau, lt):
    vals = np.array([c[key] for c in concepts], float)
    truth = np.array([c["ground_truth_regime"] for c in concepts])
    pred = np.where(vals < tau if lt else vals > tau, "absorption", "co_firing")
    return balanced_accuracy(pred, truth), pred.tolist()


# =========================================================================== router per-concept signals
def concept_router_signals(anchor, cr, lat_csr, sub_arr, label_arr, pos_mask, neg_rows, min_sub=15):
    """Per-sub-context recall_hole (1 - anchor recall) + positive-only firing-Jaccard(anchor, detector).
    detector = best-AUC non-anchor content-responsive latent (X-positives vs negatives)."""
    pos_rows = np.where(pos_mask)[0]
    if len(pos_rows) == 0:
        return [], {"recall_hole_max": float("nan"), "firing_jaccard_median": float("nan")}
    fires_anchor_pos = (np.asarray(lat_csr[pos_rows][:, [anchor]].todense()) > 0).ravel()
    sub_pos = np.asarray(sub_arr)[pos_rows]
    elig = np.array([int(l) for l in cr if int(l) != int(anchor)], dtype=int)
    neg_lat = np.asarray(lat_csr[neg_rows][:, elig.tolist()].todense()) if (len(neg_rows) and len(elig)) else np.zeros((0, len(elig)))
    out = []
    subs = [s for s in sorted(set(sub_pos.tolist()), key=lambda x: str(x))
            if s is not None and int((sub_pos == s).sum()) >= min_sub]
    for s in subs:
        m = sub_pos == s
        n_pos = int(m.sum())
        parent_recall = float(fires_anchor_pos[m].mean())
        if len(elig) == 0 or neg_lat.shape[0] < 2:
            det = anchor; det_auc = float("nan")
        else:
            pos_lat_s = np.asarray(lat_csr[pos_rows[m]][:, elig.tolist()].todense())
            sc = np.concatenate([pos_lat_s, neg_lat], 0).astype(np.float32)
            yy = np.concatenate([np.ones(n_pos), np.zeros(neg_lat.shape[0])])
            aucs = cols_auc(sc, yy)
            det = int(elig[np.nanargmax(aucs)]) if np.isfinite(aucs).any() else int(elig[0])
            det_auc = float(np.nanmax(aucs)) if np.isfinite(aucs).any() else float("nan")
        fires_det_pos = (np.asarray(lat_csr[pos_rows][:, [det]].todense()) > 0).ravel()
        jac = firing_jaccard(fires_anchor_pos, fires_det_pos)
        out.append({"sub_context": str(s), "n_pos": n_pos, "parent_recall": parent_recall,
                    "recall_hole": float(1 - parent_recall), "detector_latent": int(det),
                    "detector_auc": det_auc, "firing_jaccard": float(jac)})
    rh = [r["recall_hole"] for r in out]
    jc = [r["firing_jaccard"] for r in out]
    agg = {"recall_hole_max": float(np.max(rh)) if rh else float("nan"),
           "firing_jaccard_median": float(np.median(jc)) if jc else float("nan"),
           "n_subcontexts": len(out)}
    return out, agg


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


# =========================================================================== LLM judge (optional M7)
class LLMJudge:
    def __init__(self, enabled=False):
        self.enabled = enabled
        self.cost = 0.0; self.calls = 0; self.errors = 0; self.parse_fails = 0
        import requests
        self.requests = requests
        self.key = os.environ.get("OPENROUTER_API_KEY", "")

    def _call(self, model, system, user, max_retries=3):
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"}
        payload = {"model": model, "temperature": 0,
                   "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
                   "max_tokens": 20, "usage": {"include": True}}
        last = None
        for attempt in range(max_retries):
            try:
                resp = self.requests.post(url, headers=headers, json=payload, timeout=90)
                if resp.status_code != 200:
                    last = f"HTTP {resp.status_code}: {resp.text[:160]}"; time.sleep(2 * (attempt + 1)); continue
                j = resp.json()
                txt = j["choices"][0]["message"]["content"]
                usage = j.get("usage", {}) or {}
                cost = usage.get("cost")
                if cost is None:
                    pin, pout = LLM_PRICE.get(model, (1e-6, 5e-6))
                    cost = usage.get("prompt_tokens", 0) * pin + usage.get("completion_tokens", 0) * pout
                self.cost += float(cost); self.calls += 1
                return txt
            except Exception as e:  # noqa: BLE001
                last = repr(e)[:160]; time.sleep(2 * (attempt + 1))
        self.errors += 1; logger.warning(f"  LLM call failed: {last}")
        return None

    def judge_once(self, evidence, candidates):
        if not self.enabled or self.cost >= LLM_HARD_STOP:
            return -1, "", LLM_MODEL
        opts = "\n".join(f"  [{i}] {c}" for i, c in enumerate(candidates))
        wins = "\n".join(f"  - {w}" for w in evidence["top_windows"][:5]) or "  (no strong activating window)"
        system = ("You are an interpretability analyst. A feature inside a language model is described by the "
                  "output tokens it most promotes and the text snippets where it fires most strongly (the firing "
                  "token is wrapped in **double asterisks**). Identify the SINGLE most specific concept it detects. "
                  "Reply with ONLY the integer index of the best option, nothing else.")
        user = (f"Top promoted tokens: {', '.join(evidence['logit_lens_tokens'])}\n\n"
                f"Strongest firing snippets:\n{wins}\n\n"
                f"Which ONE option best describes the specific concept/sub-context this feature detects?\n{opts}\n\n"
                f"Answer with exactly one integer index:")
        for model in [LLM_MODEL] + LLM_FALLBACKS:
            txt = self._call(model, system, user)
            if txt is None:
                continue
            idx = _parse_index(txt, len(candidates))
            if idx < 0:
                self.parse_fails += 1
            return idx, (txt or "").strip()[:40], model
        return -1, "", LLM_MODEL


def _parse_index(txt, n):
    if not txt:
        return -1
    m = re.search(r"-?\d+", txt)
    if not m:
        return -1
    v = int(m.group())
    return v if 0 <= v < n else -1


def mark_target(text, span, maxchars=300):
    if not span or span[0] is None:
        return text[:maxchars]
    cs, ce = span
    if ce is None or ce <= cs:
        ce = cs + 1
    marked = text[:cs] + "**" + text[cs:ce] + "**" + text[ce:]
    lo = max(0, cs - maxchars // 2); hi = min(len(marked), ce + 4 + maxchars // 2)
    return ("" if lo == 0 else "...") + marked[lo:hi] + ("" if hi >= len(marked) else "...")


def build_member_evidence(member, role, gt_sub, lat_csc, rows, rows_idx, mb, sae, torch, span_of, top_k=5):
    E = mb.model.get_output_embeddings().weight.to(torch.float32)
    Wd = sae.W_dec[member].to(torch.float32)
    with torch.no_grad():
        logits = E @ Wd
        top = torch.topk(logits, 10).indices.cpu().tolist()
    toks = [mb.tok.convert_tokens_to_string([t]).strip() for t in mb.tok.convert_ids_to_tokens(top)]
    toks = [t for t in toks if t]
    col = np.asarray(lat_csc[rows_idx, member].todense()).ravel() if len(rows_idx) else np.array([])
    windows = []
    if col.size:
        order = np.argsort(-col)[:top_k]
        for oi in order:
            if col[oi] <= 0:
                break
            r = rows[rows_idx[oi]]
            windows.append(mark_target(r["input"], span_of(r)))
    return {"member": int(member), "role": role, "ground_truth_subcontext": gt_sub,
            "logit_lens_tokens": toks, "top_windows": windows}


def label_member_ensemble(judge, payload, J=J_ENSEMBLE):
    cands = payload["candidates"]; gt = payload["gt_index"]; n = len(cands)
    eff_J = J if judge.cost < LLM_TARGET else 1
    votes, calls = [], []
    for _ in range(eff_J):
        perm = rng.permutation(n)
        ordered = [cands[p] for p in perm]
        loc, raw, model = judge.judge_once(payload["evidence"], ordered)
        canon = int(perm[loc]) if loc >= 0 else -1
        votes.append(canon); calls.append({"canonical_idx": canon, "raw": raw, "model": model})
    valid = [v for v in votes if v >= 0]
    majority, maj_count = (Counter(valid).most_common(1)[0] if valid else (-1, 0))
    agree_rate = maj_count / max(eff_J, 1); chance = 1.0 / n
    confident = bool(majority >= 1 and agree_rate >= (2.0 / 3.0) and agree_rate > chance)
    correct = bool(majority == gt and majority >= 0)
    return {"majority": majority, "n_calls": eff_J, "agree_rate": float(agree_rate),
            "confident": confident, "correct": correct, "chance": float(chance), "calls": calls}


def member_labeling(judge, payloads):
    results = []
    for mp in payloads:
        ens = label_member_ensemble(judge, mp)
        idx = ens["majority"]
        results.append({"concept": mp["concept"], "member": mp["evidence"]["member"], "role": mp["evidence"]["role"],
                        "ground_truth": mp["gt_index"],
                        "ground_truth_label": mp["candidates"][mp["gt_index"]] if 0 <= mp["gt_index"] < len(mp["candidates"]) else "?",
                        "judge_index": idx, "judge_label": mp["candidates"][idx] if 0 <= idx < len(mp["candidates"]) else "PARSE_FAIL",
                        "n_candidates": len(mp["candidates"]), "correct": ens["correct"], "confident": ens["confident"],
                        "agree_rate": ens["agree_rate"], "model": ens["calls"][0]["model"] if ens["calls"] else LLM_MODEL})
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
            gts = np.array([r["ground_truth"] for r in rs]); perm = rng.permutation(len(rs))
            for i, r in enumerate(rs):
                tot += 1 if (r["judge_index"] == gts[perm[i]]) else 0; n += 1
        null_means.append(tot / max(n, 1))
    null_mean = float(np.mean(null_means))
    n = len(valid); idx = rng.integers(0, n, size=(B_BOOT, n))
    boot_agree = corr[idx].mean(1); gap = boot_agree - null_mean
    lo, hi = np.percentile(gap, [2.5, 97.5])
    role_acc = {}
    for role in ("anchor", "absorber"):
        rs = [r for r in valid if r["role"] == role]
        role_acc[role] = {"n": len(rs), "acc": float(np.mean([r["correct"] for r in rs])) if rs else None}
    overall_conf = float(np.mean([1.0 if r["confident"] else 0.0 for r in results]))
    return {"status": "scored", "agreement": agreement, "null_mean_shuffle": null_mean,
            "gap": float(agreement - null_mean), "gap_bootstrap_CI": {"lo": float(lo), "hi": float(hi), "excl_0": bool(lo > 0)},
            "n_members": n, "n_total_members": len(results), "per_role_accuracy": role_acc,
            "overall_confident_fraction": overall_conf}


# =========================================================================== D2 concept runner (per dict)
def run_d2_concept(concept, dataset_name, dict_name, sae, mb, W_dec_np, args, member_payloads, torch,
                   do_surgical=False, surgical_targets=None):
    logger.info(f"\n{el()} ===== [{dict_name}] {concept.upper()} ({dataset_name}) =====")
    rows = load_d2(dataset_name)
    if args.cap:
        corp = [r for r in rows if r["metadata_row_type"] == "corpus"][:args.cap * 40]
        rows = [r for r in rows if r["metadata_row_type"] != "corpus"] + corp
    for i, r in enumerate(rows):
        r["row_id"] = i
    lat_csr, resid, align = encode_cached(dict_name, sae, mb, f"{concept}_cap{args.cap}", rows)
    rt = np.array([r["metadata_row_type"] for r in rows])
    role = np.array([r.get("metadata_pair_role") for r in rows], dtype=object)
    fold = np.array([r["metadata_fold"] for r in rows], dtype=object)
    label = np.array([1 if r["output"] == "positive" else 0 for r in rows])
    sub = np.array([r.get("metadata_sub_context") for r in rows], dtype=object)
    pid = np.array([r.get("metadata_pair_id") for r in rows], dtype=object)

    cp = (rt == "content_pair") & (fold == "train")
    pairs = defaultdict(dict)
    for i in np.where(cp)[0]:
        pairs[pid[i]][role[i]] = i
    pl = [p for p, d in pairs.items() if "x_on" in d and "x_off" in d]
    if not pl:
        logger.warning(f"[{dict_name}] {concept}: no content pairs; skipping")
        del lat_csr, resid; gc.collect(); torch.cuda.empty_cache()
        return None
    on_idx = np.array([pairs[p]["x_on"] for p in pl]); off_idx = np.array([pairs[p]["x_off"] for p in pl])
    A_on = np.asarray(lat_csr[on_idx].todense()); A_off = np.asarray(lat_csr[off_idx].todense())
    cr, prec, _ = content_responsive(A_on, A_off)

    corp_pos = (rt == "corpus") & (label == 1)
    corp_pos_rows = np.where(corp_pos)[0]
    anchor, anchor_info = rederive_anchor(cr, prec, A_on, lat_csr[corp_pos_rows] if len(corp_pos_rows) else None)
    del A_on, A_off
    logger.info(f"{el()} [{dict_name}/{concept}] responsive={len(cr)} re-derived anchor={anchor} "
                f"(corpus_fire={anchor_info.get('corpus_fire_rate')}, floor_ok={anchor_info.get('firing_floor_validated')})")

    sel_mask = (rt == "corpus") & (fold == "train")
    eval_mask = (rt == "corpus") & (fold == "diagnostic")
    eligible_X, elig_meta = [], {}
    for X in sorted(set(sub[corp_pos].tolist())):
        if X is None:
            continue
        n_sel = int(((sub == X) & sel_mask & (label == 1)).sum())
        n_eval = int(((sub == X) & eval_mask & (label == 1)).sum())
        if n_sel >= N_MIN_SEL and n_eval >= N_MIN_RELAX:
            eligible_X.append(X); elig_meta[X] = {"n_sel": n_sel, "n_eval": n_eval}

    anchor_fire_corpus = anchor_info.get("corpus_fire_rate", 0.0) if anchor is not None else 0.0
    spurious = (anchor is None) or (not anchor_info.get("firing_floor_validated", False)) or anchor_fire_corpus < SPURIOUS_FIRE_FLOOR

    # probe direction for the form-free diagnostic absorber
    fit_pos = np.where((rt == "corpus") & (label == 1) & (fold == "diagnostic"))[0]
    fit_neg = np.where((rt == "corpus") & (label == 0) & (fold == "diagnostic"))[0]
    probe_dir = None
    if len(fit_pos) >= 10 and len(fit_neg) >= 10:
        from sklearn.linear_model import LogisticRegression
        Xp = resid[fit_pos].astype(np.float64); Xn = resid[fit_neg].astype(np.float64)
        clf = LogisticRegression(max_iter=2000, C=1.0, class_weight="balanced").fit(
            np.concatenate([Xp, Xn]), np.concatenate([np.ones(len(Xp)), np.zeros(len(Xn))]))
        probe_dir = clf.coef_[0].astype(np.float64); probe_dir /= (np.linalg.norm(probe_dir) + 1e-9)

    broad_kg = {}
    if not spurious:
        broad_kg, _ = derive_broad_kg(anchor, cr, lat_csr, sub, label, sel_mask, eligible_X)
        if probe_dir is not None:
            for X in eligible_X:
                d = broad_kg.get(X, {})
                d["diag_absorber"] = derive_diagnostic_absorber(X, anchor, cr, lat_csr, resid, probe_dir,
                                                                sub, label, sel_mask, W_dec_np)
    n_named = sum(1 for x in broad_kg.values() if x.get("kg_absorber") is not None)
    logger.info(f"{el()} [{dict_name}/{concept}] eligible={len(eligible_X)} named_absorbers={n_named} spurious={spurious}")

    cands = [{"X": X, "kg_absorber": broad_kg.get(X, {}).get("kg_absorber"),
              "diag_absorber": broad_kg.get(X, {}).get("diag_absorber"),
              "derivation": {k: broad_kg.get(X, {}).get(k) for k in
                             ("recall_on_X_selection", "subctx_precision_selection", "jaccard_anchor",
                              "n_sel_pos", "reason") if k in broad_kg.get(X, {})}} for X in eligible_X]
    member_set = ({anchor} | set(int(c["kg_absorber"]) for c in cands if c["kg_absorber"] is not None)
                  | set(int(c["diag_absorber"]) for c in cands if c.get("diag_absorber") is not None))
    if spurious:
        rep = {"status": "N/A_spurious_anchor", "per_subcontext": {}, "honest_negatives": [],
               "n_measured_successful_repairs": 0,
               "note": f"{concept} re-derived anchor {anchor} fires {anchor_fire_corpus} on corpus (spurious/unvalidated)"}
    else:
        rep = repair_loop(concept, anchor, cands, lat_csr, sub, label, cr, member_set, sel_mask, eval_mask)

    # router signals (recall_hole + firing_jaccard) over ALL corpus positives, negatives for detector AUC
    neg_rows = np.where((rt == "corpus") & (label == 0))[0]
    router_ps, router_agg = ([], {"recall_hole_max": float("nan"), "firing_jaccard_median": float("nan")})
    if anchor is not None:
        router_ps, router_agg = concept_router_signals(anchor, cr, lat_csr, sub, label, corp_pos, neg_rows)

    # (k) localization
    kfold = np.where(sel_mask, "selection", np.where(eval_mask, "eval", "other")).astype(object)
    eval_rows_by_X = {c["X"]: np.where((sub == c["X"]) & (label == 1) & eval_mask)[0] for c in cands}
    kg_abs_map = {c["X"]: c["kg_absorber"] for c in cands if c["kg_absorber"] is not None}
    kcheck = ({"status": "not_run", "reason": "spurious anchor"} if (spurious or anchor is None) else
              k_localization_check(concept, resid, label, kfold, W_dec_np, anchor, kg_abs_map, eval_rows_by_X))

    # member-labeling payloads (anchor + named absorbers)
    if args.member_labeling and not spurious:
        lat_csc = lat_csr.tocsc()
        subs_sorted = sorted(set(eligible_X))
        cands_list = [f"GENERAL parent ({'any country name' if concept=='taxonomic' else 'any numeric token'})"] + subs_sorted
        span_of = lambda r: r.get("_span")
        members_for_label = [("anchor", anchor, cands_list[0])]
        for c in cands:
            if c.get("kg_absorber") is not None:
                members_for_label.append(("absorber", c["kg_absorber"], c["X"]))
        seen = set()
        for role_name, m, gt_label in members_for_label:
            if int(m) in seen:
                continue
            seen.add(int(m))
            ev = build_member_evidence(int(m), role_name, gt_label, lat_csc, rows, corp_pos_rows, mb, sae, torch, span_of)
            gi = cands_list.index(gt_label) if gt_label in cands_list else 0
            member_payloads.append({"concept": f"{dict_name}:{concept}", "evidence": ev, "candidates": cands_list, "gt_index": gi})
        del lat_csc

    # ---- SURGICAL EDITS (taxonomic only) ----
    surgical_cases = []
    if do_surgical and not spurious:
        Rnorm = mb.mean_resid_norm(NEUTRAL_TEXT)
        probe = ParentProbe(torch, resid[fit_pos].astype(np.float32), resid[fit_neg].astype(np.float32))
        sib_pool = [c for c in eligible_X]
        neg_idx = np.where((rt == "corpus") & (label == 0) & (fold == "train"))[0]
        U_texts = [rows[i]["input"][:300] for i in neg_idx[:args.kl_prompts]] or NEUTRAL_TEXT[:args.kl_prompts]
        base_lp, base_ppl = base_distributions(mb, U_texts)
        for X in (surgical_targets or []):
            d = broad_kg.get(X, {})
            absorber = d.get("kg_absorber")
            if absorber is None:
                surgical_cases.append({"family": concept, "target_subcontext": X, "regime": "absorption",
                                       "verdict": "NON_REPLICATED_NO_PRECISE_ABSORBER", "absorber_latent": -1,
                                       "reason": d.get("reason", "no precision>=0.70 absorber on this dictionary"),
                                       "note": "KEY dictionary-dependence outcome: wider/different SAE did not expose a clean "
                                               "high-precision absorber for this sub-context"})
                continue
            eval_fold = "train"
            t_idx = np.where((rt == "corpus") & (label == 1) & (sub == X) & (fold == eval_fold))[0]
            if len(t_idx) < 8:
                t_idx = np.where((rt == "corpus") & (label == 1) & (sub == X))[0]
            sib_names = [c for c in sib_pool if c != X]
            s_idx = np.where((rt == "corpus") & (label == 1) & (sub != X) & np.isin(sub, sib_names) & (fold == eval_fold))[0]
            if len(t_idx) < 8 or len(s_idx) < 8:
                surgical_cases.append({"family": concept, "target_subcontext": X, "regime": "absorption",
                                       "verdict": "NOT_RUN_TOO_FEW_CONTEXTS", "absorber_latent": int(absorber),
                                       "n_target": int(len(t_idx)), "n_sibling": int(len(s_idx))})
                continue
            H_t = torch.tensor(resid[t_idx].astype(np.float32), device=DEVICE)
            H_s = torch.tensor(resid[s_idx].astype(np.float32), device=DEVICE)
            rand_lat, trate = pick_random_latents(lat_csr, absorber, cr, member_set)
            tgt_rows = np.where((rt == "corpus") & (label == 1) & (sub == X))[0]
            case = run_case(torch=torch, sae=sae, mb=mb, family=concept, X=X, absorber=int(absorber),
                            absorber_precision=float(d.get("subctx_precision_selection", 0.0)), regime="absorption",
                            probe=probe, H_target=H_t, H_siblings=H_s, sibling_names=sib_names[:12], H_broad=H_s,
                            target_rows=[rows[i] for i in t_idx], sibling_rows=[rows[i] for i in s_idx],
                            U_texts=U_texts, base_lp=base_lp, base_ppl=base_ppl, rand_latents=rand_lat,
                            parent_latent=anchor, lat_csr_for_jaccard=lat_csr, target_rows_for_jaccard=tgt_rows)
            surgical_cases.append(case)
            del H_t, H_s; torch.cuda.empty_cache()

    result = {"concept": concept, "dictionary": dict_name, "anchor": anchor, "anchor_info": anchor_info,
              "spurious_anchor": bool(spurious), "n_content_responsive": int(len(cr)),
              "eligible_subcontexts": eligible_X, "eligibility": elig_meta, "n_named_absorber": n_named,
              "broad_kg": broad_kg, "repair": rep, "router_per_subcontext": router_ps, "router_agg": router_agg,
              "k_localization": kcheck, "surgical_cases": surgical_cases, "regime": "absorption"}
    del lat_csr, resid; gc.collect(); torch.cuda.empty_cache()
    return result


# =========================================================================== first-letter runner (per dict)
def run_first_letter(letters, dict_name, sae, mb, W_dec_np, args, member_payloads, torch, do_surgical=False):
    logger.info(f"\n{el()} ===== [{dict_name}] FIRST-LETTER {letters} =====")
    groups = load_first_letter(letters)
    results = {}
    for lt in letters:
        rows = groups[lt]
        if args.cap:
            corp = [r for r in rows if r.get("metadata_pair_type") == "corpus_context"][:args.cap * 40]
            rows = [r for r in rows if r.get("metadata_pair_type") != "corpus_context"] + corp
        for i, r in enumerate(rows):
            r["row_id"] = i
        carriers = {"t_verbose", "t_colon", "t_icl"}
        pt = np.array([r.get("metadata_pair_type") for r in rows], dtype=object)
        tmpl = np.array([r.get("metadata_template_id") for r in rows], dtype=object)
        rl = np.array([r.get("metadata_role") for r in rows], dtype=object)
        pidL = np.array([r.get("metadata_pair_id") for r in rows], dtype=object)
        foldL = np.array([r.get("metadata_fold") for r in rows])
        subL = np.array([r.get("metadata_sub_context") for r in rows], dtype=object)
        keep_idx = [i for i in range(len(rows))
                    if pt[i] == "corpus_context" or (pt[i] == "content_flip" and tmpl[i] in carriers)]
        sub_rows = [rows[i] for i in keep_idx]
        lat_csr, resid, align = encode_cached(dict_name, sae, mb, f"FL{lt}_cap{args.cap}", sub_rows)
        gpt = pt[keep_idx]; grole = rl[keep_idx]; gpid = pidL[keep_idx]; gfold = foldL[keep_idx]; gsub = subL[keep_idx]
        is_corpus = (gpt == "corpus_context")
        cpairs = defaultdict(dict)
        for j in np.where(gpt == "content_flip")[0]:
            cpairs[gpid[j]][grole[j]] = j
        pl = [p for p, d in cpairs.items() if "on" in d and "off" in d]
        cr = np.array([], int); anchor = None; anchor_info = {"reason": "no_content_pairs"}
        if pl:
            on_idx = np.array([cpairs[p]["on"] for p in pl]); off_idx = np.array([cpairs[p]["off"] for p in pl])
            A_on = np.asarray(lat_csr[on_idx].todense()); A_off = np.asarray(lat_csr[off_idx].todense())
            cr, prec, _ = content_responsive(A_on, A_off)
            corp_rows_idx = np.where(is_corpus)[0]
            anchor, anchor_info = rederive_anchor(cr, prec, A_on, lat_csr[corp_rows_idx] if len(corp_rows_idx) else None)
            del A_on, A_off
        anchor_fire_corpus = anchor_info.get("corpus_fire_rate", 0.0) if anchor is not None else 0.0
        spurious = (anchor is None) or (not anchor_info.get("firing_floor_validated", False))
        sel_mask = is_corpus & np.isin(gfold, [0, 1, 2])
        eval_mask = is_corpus & np.isin(gfold, [3, 4])
        label_all = np.ones(len(sub_rows), dtype=int)
        eligible_X, elig_meta = [], {}
        for X in sorted(set(gsub[is_corpus].tolist())):
            if X is None:
                continue
            n_sel = int(((gsub == X) & sel_mask).sum()); n_eval = int(((gsub == X) & eval_mask).sum())
            if n_sel >= N_MIN_SEL and n_eval >= N_MIN_RELAX:
                eligible_X.append(X); elig_meta[X] = {"n_sel": n_sel, "n_eval": n_eval}
        broad_kg = {}
        if not spurious:
            broad_kg, _ = derive_broad_kg(anchor, cr, lat_csr, gsub, label_all, sel_mask, eligible_X)
        n_named = sum(1 for x in broad_kg.values() if x.get("kg_absorber") is not None)
        cands = [{"X": X, "kg_absorber": broad_kg.get(X, {}).get("kg_absorber"), "diag_absorber": None,
                  "derivation": {k: broad_kg.get(X, {}).get(k) for k in
                                 ("recall_on_X_selection", "subctx_precision_selection", "jaccard_anchor",
                                  "n_sel_pos", "reason") if k in broad_kg.get(X, {})}} for X in eligible_X]
        member_set = ({anchor} if anchor is not None else set()) | set(
            int(c["kg_absorber"]) for c in cands if c["kg_absorber"] is not None)
        if spurious or not cands or not len(cr):
            rep = {"status": "N/A_spurious_or_no_named", "per_subcontext": {}, "honest_negatives": [],
                   "n_measured_successful_repairs": 0,
                   "note": f"letter {lt} anchor={anchor} fire={anchor_fire_corpus} spurious={spurious}"}
        else:
            rep = repair_loop(f"first_letter_{lt}", anchor, cands, lat_csr, gsub, label_all, cr, member_set, sel_mask, eval_mask)
        # router signals: positives = corpus L-words; negatives = none available within letter -> use content-flip off
        router_ps, router_agg = ([], {"recall_hole_max": float("nan"), "firing_jaccard_median": float("nan")})
        if anchor is not None and pl:
            neg_rows = np.array([cpairs[p]["off"] for p in pl])
            router_ps, router_agg = concept_router_signals(anchor, cr, lat_csr, gsub, label_all, is_corpus, neg_rows, min_sub=15)
        # one surgical on best held-out precision absorber (spelling)
        surgical_cases = []
        if do_surgical and not spurious and cands:
            best = None
            for X in eligible_X:
                ab = broad_kg.get(X, {}).get("kg_absorber")
                if ab is None:
                    continue
                prec_sel = broad_kg.get(X, {}).get("subctx_precision_selection", 0.0)
                if best is None or prec_sel > best[2]:
                    best = (X, ab, prec_sel)
            if best is not None:
                from sklearn.linear_model import LogisticRegression  # noqa
                Xw, ab, precv = best
                # probe: L word tokens (folds 0-2) vs non-target via off-pairs
                fit_pos = np.where(is_corpus & np.isin(gfold, [0, 1, 2]))[0]
                fit_neg = np.array([cpairs[p]["off"] for p in pl])
                if len(fit_pos) >= 10 and len(fit_neg) >= 10:
                    probe = ParentProbe(torch, resid[fit_pos].astype(np.float32), resid[fit_neg].astype(np.float32))
                    t_idx = np.where(is_corpus & (gsub == Xw))[0]
                    sib_words = [w for w in eligible_X if w != Xw]
                    s_idx = np.where(is_corpus & np.isin(gsub, sib_words) & (gsub != Xw))[0]
                    if len(s_idx) > 300:
                        s_idx = rng.choice(s_idx, 300, replace=False)
                    if len(t_idx) >= 8 and len(s_idx) >= 8:
                        U_texts = NEUTRAL_TEXT[:args.kl_prompts]
                        base_lp, base_ppl = base_distributions(mb, U_texts)
                        H_t = torch.tensor(resid[t_idx].astype(np.float32), device=DEVICE)
                        H_s = torch.tensor(resid[s_idx].astype(np.float32), device=DEVICE)
                        rand_lat, _ = pick_random_latents(lat_csr, ab, cr, member_set)
                        case = run_case(torch=torch, sae=sae, mb=mb, family=f"first_letter_{lt}", X=Xw, absorber=int(ab),
                                        absorber_precision=float(precv), regime="absorption", probe=probe,
                                        H_target=H_t, H_siblings=H_s, sibling_names=sib_words[:12], H_broad=H_s,
                                        target_rows=[sub_rows[i] for i in t_idx], sibling_rows=[sub_rows[i] for i in s_idx],
                                        U_texts=U_texts, base_lp=base_lp, base_ppl=base_ppl, rand_latents=rand_lat,
                                        parent_latent=anchor, lat_csr_for_jaccard=lat_csr, target_rows_for_jaccard=t_idx)
                        surgical_cases.append(case)
                        del H_t, H_s; torch.cuda.empty_cache()
        for X, e in rep.get("per_subcontext", {}).items():
            pass
        results[lt] = {"concept": f"first_letter_{lt}", "dictionary": dict_name, "anchor": anchor,
                       "anchor_info": anchor_info, "spurious_anchor": bool(spurious),
                       "n_content_responsive": int(len(cr)), "eligible_subcontexts": eligible_X,
                       "eligibility": elig_meta, "n_named_absorber": n_named, "broad_kg": broad_kg, "repair": rep,
                       "router_per_subcontext": router_ps, "router_agg": router_agg,
                       "surgical_cases": surgical_cases, "regime": "absorption"}
        logger.info(f"{el()} [{dict_name}/{lt}] anchor={anchor} eligible={len(eligible_X)} named={n_named} "
                    f"spurious={spurious} surgical={len(surgical_cases)}")
        del lat_csr, resid; gc.collect(); torch.cuda.empty_cache()
    return results


# =========================================================================== toxicity runner (negative pole)
def run_toxicity(dict_name, sae, mb, W_dec_np, args, torch):
    logger.info(f"\n{el()} ===== [{dict_name}] TOXICITY (co-firing pole) =====")
    rows = load_toxicity()
    cap = args.cap or 400
    subs = ["insult", "obscene", "threat", "identity_attack"]
    def subval(r, name):
        sf = r.get("metadata_subcontext_floats") or {}
        return float(sf.get(name, 0.0))
    toxic = [r for r in rows if r.get("metadata_toxicity_label") == 1]
    neutral = [r for r in rows if r.get("metadata_toxicity_label") == 0]
    rng.shuffle(toxic); rng.shuffle(neutral)
    n = min(len(toxic), len(neutral), cap * 6)
    enc_rows = toxic[:n] + neutral[:n]
    lat_csr, resid, _ = encode_cached(dict_name, sae, mb, f"tox_cap{cap}", enc_rows, whole_sentence=True)
    label = np.array([1 if r.get("metadata_toxicity_label") == 1 else 0 for r in enc_rows])
    fold = np.array([r.get("metadata_fold") for r in enc_rows], dtype=object)
    subm = {s: np.array([1 if subval(r, s) >= 0.5 else 0 for r in enc_rows]) for s in subs}
    fit_mask = (fold == "train"); eval_mask = np.isin(fold, ["test", "val"])
    fp = np.where(fit_mask & (label == 1))[0]; fn = np.where(fit_mask & (label == 0))[0]
    probe = ParentProbe(torch, resid[fp].astype(np.float32), resid[fn].astype(np.float32))
    toxrows = np.where((label == 1) & fit_mask)[0]
    fire_tox = np.asarray((lat_csr[toxrows] > 0).sum(0)).ravel() / max(len(toxrows), 1)
    parent_latent = int(np.argmax(fire_tox))
    from sklearn.metrics import roc_auc_score
    tox_fit = np.where((label == 1) & fit_mask)[0]
    # per-subattribute co-firing signature: recall_hole (parent fires on subattr positives?) + firing jaccard
    router_ps = []
    cls_lat_tox = np.asarray(lat_csr[tox_fit].todense())
    fires_parent = cls_lat_tox[:, parent_latent] > 0
    firefrac = (cls_lat_tox > 0).mean(0)
    cand_lat = np.where(firefrac > 0.02)[0]
    insult_latent, insult_auc = None, 0.5
    for s in subs:
        ys = subm[s][tox_fit]
        if ys.sum() < 15 or (len(ys) - ys.sum()) < 15:
            continue
        parent_recall = float(fires_parent[ys == 1].mean()) if (ys == 1).sum() else float("nan")
        best_l, best_a = None, 0.5
        for c in cand_lat:
            try:
                a = roc_auc_score(ys, cls_lat_tox[:, c])
            except Exception:  # noqa: BLE001
                continue
            if a > best_a:
                best_a, best_l = a, int(c)
        det = best_l if best_l is not None else parent_latent
        jac = firing_jaccard(fires_parent, cls_lat_tox[:, det] > 0)
        router_ps.append({"sub_context": s, "n_pos": int(ys.sum()), "parent_recall": parent_recall,
                          "recall_hole": float(1 - parent_recall) if np.isfinite(parent_recall) else float("nan"),
                          "detector_latent": int(det), "detector_auc": float(best_a), "firing_jaccard": float(jac)})
        if s == "insult":
            insult_latent, insult_auc = det, best_a
    rh = [r["recall_hole"] for r in router_ps if np.isfinite(r["recall_hole"])]
    jc = [r["firing_jaccard"] for r in router_ps]
    router_agg = {"recall_hole_max": float(np.max(rh)) if rh else float("nan"),
                  "firing_jaccard_median": float(np.median(jc)) if jc else float("nan"),
                  "n_subcontexts": len(router_ps)}

    surgical_cases = []
    if insult_latent is not None:
        U_texts = [enc_rows[i]["input"][:200] for i in np.where((label == 0) & eval_mask)[0][:args.kl_prompts]] or NEUTRAL_TEXT[:args.kl_prompts]
        base_lp, base_ppl = base_distributions(mb, U_texts)
        t_idx = np.where(eval_mask & (label == 1) & (subm["insult"] == 1))[0]
        sib_mask = eval_mask & (label == 1) & (subm["insult"] == 0) & (
            (subm["obscene"] == 1) | (subm["threat"] == 1) | (subm["identity_attack"] == 1))
        s_idx = np.where(sib_mask)[0]
        if len(t_idx) > 300:
            t_idx = rng.choice(t_idx, 300, replace=False)
        if len(s_idx) > 300:
            s_idx = rng.choice(s_idx, 300, replace=False)
        if len(t_idx) >= 8 and len(s_idx) >= 8:
            H_t = torch.tensor(resid[t_idx].astype(np.float32), device=DEVICE)
            H_s = torch.tensor(resid[s_idx].astype(np.float32), device=DEVICE)
            responsive_tox = np.where(fire_tox > 0.05)[0]
            rand_lat, _ = pick_random_latents(lat_csr, insult_latent, responsive_tox, {insult_latent, parent_latent})
            tgt_rows = np.where((label == 1) & (subm["insult"] == 1))[0]
            case = run_case(torch=torch, sae=sae, mb=mb, family="toxicity", X="insult", absorber=int(insult_latent),
                            absorber_precision=float(insult_auc), regime="co-firing", probe=probe, H_target=H_t,
                            H_siblings=H_s, sibling_names=["obscene", "threat", "identity_attack"], H_broad=H_s,
                            target_rows=[enc_rows[i] for i in t_idx], sibling_rows=[enc_rows[i] for i in s_idx],
                            U_texts=U_texts, base_lp=base_lp, base_ppl=base_ppl, rand_latents=rand_lat,
                            parent_latent=parent_latent, lat_csr_for_jaccard=lat_csr, target_rows_for_jaccard=tgt_rows,
                            whole_sentence=True)
            surgical_cases.append(case)
            del H_t, H_s; torch.cuda.empty_cache()
    logger.info(f"{el()} [{dict_name}/toxicity] parent={parent_latent} insult_latent={insult_latent} auc={insult_auc:.3f} "
                f"recall_hole_max={router_agg['recall_hole_max']} jaccard_med={router_agg['firing_jaccard_median']}")
    result = {"concept": "toxicity", "dictionary": dict_name, "anchor": parent_latent, "parent_latent": parent_latent,
              "insult_latent": insult_latent, "insult_auc": float(insult_auc), "spurious_anchor": False,
              "router_per_subcontext": router_ps, "router_agg": router_agg, "surgical_cases": surgical_cases,
              "regime": "co-firing", "repair": {"status": "co-firing pole; repair N/A", "per_subcontext": {},
                                                "honest_negatives": [], "n_measured_successful_repairs": 0}}
    del lat_csr, resid; gc.collect(); torch.cuda.empty_cache()
    return result


# =========================================================================== multiplicity (BH across all)
def family_of(concept):
    if concept == "taxonomic":
        return "homograph_taxonomic"
    if concept == "numeric":
        return "numeric"
    return "spelling"


def apply_multiplicity(concept_results):
    """BH FDR across ALL measured repair variants from all concepts of ONE dictionary. M3 honest counting:
    de-duplicate kg_diagnostic variants that name the SAME latent as kg_ktrack."""
    rows = []
    for res in concept_results:
        concept = res["concept"]
        rep = res.get("repair", {})
        for X, e in rep.get("per_subcontext", {}).items():
            if e.get("status") != "measured":
                continue
            for vname, v in e.get("variants", {}).items():
                rows.append((concept, X, vname, v))
    pvals = [v["p_value_one_sided"] for (_, _, _, v) in rows]
    q, n_sig = benjamini_hochberg(pvals, FDR_ALPHA)
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
    distinct = defaultdict(set)            # family -> set of (X, latent) distinct holes that survive
    n_meas_succ = 0
    for i, (concept, X, vname, v) in enumerate(rows):
        v["bh_q"] = float(q[i]); v["survives_FDR"] = bool(q[i] <= FDR_ALPHA)
        f = family_of(concept.replace("first_letter_", "FL_") if concept.startswith("first_letter") else concept)
        fam[f] += 1
        if v["survives_FDR"]:
            fam_sig[f] += 1
            distinct[f].add((concept, str(X), int(v["absorber_latent"])))
        if v["measured_success"]:
            n_meas_succ += 1
    n_hole = sum(1 for res in concept_results for X, e in res.get("repair", {}).get("per_subcontext", {}).items()
                 if e.get("status") == "measured" and e.get("is_hole"))
    distinct_count = {k: len(v) for k, v in distinct.items()}
    return {"method": "Benjamini-Hochberg FDR", "alpha": FDR_ALPHA, "n_repairs_tested": len(rows), "n_holes": n_hole,
            "n_measured_success_uncorrected": n_meas_succ, "n_survive_FDR": n_sig,
            "statsmodels_crosscheck_matches": sm_ok, "per_family_tested": fam, "per_family_survive_FDR": fam_sig,
            "distinct_hole_count_survive_FDR": distinct_count,
            "distinct_total_survive_FDR": int(sum(distinct_count.values()))}


# =========================================================================== router transfer (STAGE 4)
def router_transfer(concept_results, tox_result):
    """Build the per-concept router set (absorption concepts + toxicity co-firing sub-attributes), apply the
    FROZEN 16k thresholds (recall-hole lead tau_h, firing-Jaccard corroborating tau_j) WITHOUT refit, and
    re-derive 65k-optimal thresholds. transfer = frozen thresholds still give high balanced-accuracy."""
    concepts = []
    for res in concept_results:
        agg = res.get("router_agg", {})
        if not np.isfinite(agg.get("recall_hole_max", float("nan"))):
            continue
        concepts.append({"concept": res["concept"], "ground_truth_regime": "absorption",
                         "recall_hole_max": agg["recall_hole_max"], "firing_jaccard_median": agg["firing_jaccard_median"]})
    if tox_result is not None:
        for r in tox_result.get("router_per_subcontext", []):
            if np.isfinite(r.get("recall_hole", float("nan"))):
                concepts.append({"concept": f"toxicity:{r['sub_context']}", "ground_truth_regime": "co_firing",
                                 "recall_hole_max": r["recall_hole"], "firing_jaccard_median": r["firing_jaccard"]})
    if len(concepts) < 3 or len({c["ground_truth_regime"] for c in concepts}) < 2:
        return {"status": "insufficient_concepts", "n_concepts": len(concepts), "concepts": concepts}
    frozen_h_bacc, frozen_h_pred = apply_frozen_threshold(concepts, "recall_hole_max", REF_16K["router_tau_h"], lt=False)
    frozen_j_bacc, frozen_j_pred = apply_frozen_threshold(concepts, "firing_jaccard_median", REF_16K["router_tau_j"], lt=True)
    tau_h_65, bacc_h_65, sweep_h = derive_1d(concepts, "recall_hole_max", lt=False)
    tau_j_65, bacc_j_65, sweep_j = derive_1d(concepts, "firing_jaccard_median", lt=True)
    return {"status": "derived", "n_concepts": len(concepts), "concepts": concepts,
            "lead_signal": "recall_hole_alone (firing-Jaccard corroborating, per M6)",
            "frozen_16k_thresholds": {"tau_h": REF_16K["router_tau_h"], "tau_j": REF_16K["router_tau_j"]},
            "frozen_16k_recall_hole_balanced_acc": frozen_h_bacc,
            "frozen_16k_firing_jaccard_balanced_acc": frozen_j_bacc,
            "rederived_65k_tau_h": tau_h_65, "rederived_65k_recall_hole_balanced_acc": bacc_h_65,
            "rederived_65k_tau_j": tau_j_65, "rederived_65k_firing_jaccard_balanced_acc": bacc_j_65,
            "balanced_acc_recall_hole_alone": frozen_h_bacc, "balanced_acc_combined": max(frozen_h_bacc, frozen_j_bacc),
            "tau_h": tau_h_65, "tau_j": tau_j_65,
            "transfers": bool(frozen_h_bacc >= 0.8), "tau_h_close_to_16k": bool(abs(tau_h_65 - REF_16K["router_tau_h"]) < 0.2)}


# =========================================================================== replication table + verdicts
def _find_sub(router_ps, name):
    for r in router_ps:
        if str(r["sub_context"]) == name:
            return r
    return None


def build_replication_table(dict_name, cfg, sae, gating, concept_results, tox_result, multiplicity, router_xfer):
    tax = next((r for r in concept_results if r["concept"] == "taxonomic"), None)
    # ---- piece A: homograph recall-holes ----
    homo = {}
    geo = jor = None
    if tax is not None:
        for r in tax.get("router_per_subcontext", []):
            if r["sub_context"] in ("Georgia", "Jordan", "United States", "Turkey", "Chile", "Iran"):
                homo[r["sub_context"]] = {"recall_hole": r["recall_hole"], "firing_jaccard": r["firing_jaccard"],
                                          "n_pos": r["n_pos"], "detector_latent": r["detector_latent"]}
        geo = _find_sub(tax.get("router_per_subcontext", []), "Georgia")
        jor = _find_sub(tax.get("router_per_subcontext", []), "Jordan")
    geo_hole_ok = bool(geo and geo["recall_hole"] > 0.5 and geo["firing_jaccard"] < 0.1)
    jor_hole_ok = bool(jor and jor["recall_hole"] > 0.5 and jor["firing_jaccard"] < 0.1)
    holes_replicate = geo_hole_ok or jor_hole_ok
    piece_A = "REPLICATES" if (geo_hole_ok and jor_hole_ok) else ("PARTIAL" if holes_replicate else "DICTIONARY_DEPENDENT")

    reduced = cfg.get("reduced", False)
    # ---- piece B: repair FDR ----
    fam_sig = multiplicity.get("per_family_survive_FDR", {})
    deltas = {f: fam_sig.get(f, 0) - REF_16K["per_family_survive_FDR"].get(f, 0)
              for f in REF_16K["per_family_survive_FDR"]}
    tax_repairs_survive = fam_sig.get("homograph_taxonomic", 0) >= 1
    any_family_survives = any(v >= 1 for v in fam_sig.values())
    if reduced:
        # reduced run tests ONLY the taxonomic family -> judge on homograph-taxonomic alone
        piece_B = "REPLICATES" if tax_repairs_survive else ("PARTIAL" if any_family_survives else "DICTIONARY_DEPENDENT")
    else:
        piece_B = ("REPLICATES" if (tax_repairs_survive and sum(fam_sig.values()) >= 3) else
                   ("PARTIAL" if any_family_survives else "DICTIONARY_DEPENDENT"))

    # ---- piece C: surgical ----
    surg_cases = []
    for res in concept_results:
        surg_cases.extend(res.get("surgical_cases", []))
    if tox_result is not None:
        surg_cases.extend(tox_result.get("surgical_cases", []))   # include the co-firing negative pole
    absn = [c for c in surg_cases if c.get("regime") == "absorption" and "matched" in c]
    confirmed = [c for c in absn if c.get("verdict") == "SURGICAL_EDIT_CONFIRMED"]
    best_surg = max(absn, key=lambda c: c.get("headline_selectivity_ratio", 0), default=None)
    surg_clean = [c for c in absn if c.get("headline_selectivity_ratio", 0) >= 20
                  and c.get("selectivity_CIs", {}).get("dense_minus_kg_collateral", {}).get("excl_0")]
    piece_C = ("REPLICATES" if confirmed else ("PARTIAL" if surg_clean else "DICTIONARY_DEPENDENT"))
    surgical_summary = []
    for c in surg_cases:
        ci = c.get("selectivity_CIs", {})
        surgical_summary.append({
            "family": c.get("family"), "subcontext": c.get("target_subcontext"), "absorber": c.get("absorber_latent"),
            "verdict": c.get("verdict"), "selectivity_ratio": c.get("headline_selectivity_ratio"),
            "kg_collateral": ci.get("KG-ABL_collateral", {}).get("mean"),
            "dense_collateral": ci.get("DENSE-ABL_collateral", {}).get("mean"),
            "dense_minus_kg_excl0": ci.get("dense_minus_kg_collateral", {}).get("excl_0"),
            "kg_offtarget_footprint": c.get("matched", {}).get("KG-ABL", {}).get("token_footprint_offtarget"),
            "firing_jaccard": c.get("firing_jaccard_with_parent"), "parent_recall_hole": c.get("parent_recall_hole"),
            "regime": c.get("regime")})

    # ---- piece D: router ----
    router_transfers = bool(router_xfer.get("transfers", False))
    if router_xfer.get("status") != "derived":
        # reduced run / too few concepts to test the multi-concept router threshold transfer
        piece_D = "NOT_RUN_REDUCED"
    else:
        piece_D = ("REPLICATES" if router_xfer.get("frozen_16k_recall_hole_balanced_acc", 0) >= 0.8 else
                   ("PARTIAL" if router_xfer.get("rederived_65k_recall_hole_balanced_acc", 0) >= 0.8 else "DICTIONARY_DEPENDENT"))

    # ---- regime split ----
    cofn = [c for c in surg_cases if c.get("regime") == "co-firing" and "matched" in c]
    def _mean(xs):
        xs = [x for x in xs if x is not None]
        return float(np.mean(xs)) if xs else None
    regime_split = {
        "absorption_mean_selectivity": _mean([c.get("headline_selectivity_ratio") for c in absn]),
        "absorption_mean_firing_jaccard": _mean([c.get("firing_jaccard_with_parent") for c in absn]),
        "co_firing_mean_selectivity": _mean([c.get("headline_selectivity_ratio") for c in cofn]),
        "co_firing_mean_firing_jaccard": _mean([c.get("firing_jaccard_with_parent") for c in cofn]),
        "n_absorption": len(absn), "n_co_firing": len(cofn)}

    pieces = {"homograph_holes": piece_A, "repair_fdr": piece_B, "surgical": piece_C, "router": piece_D}
    # overall verdict over only the pieces actually RUN (a reduced run excludes NOT_RUN_REDUCED pieces)
    vlist = [v for v in pieces.values() if v != "NOT_RUN_REDUCED"]
    if vlist and all(v == "REPLICATES" for v in vlist):
        overall = "full"
    elif vlist and all(v == "DICTIONARY_DEPENDENT" for v in vlist):
        overall = "dictionary_dependent"
    else:
        overall = "partial"

    return {
        "dictionary": dict_name, "layer": cfg["layer"], "width": cfg["width"], "sae_id": sae.sae_id,
        "avg_l0": sae.avg_l0, "gating": gating, "reduced_run": cfg.get("reduced", False),
        "re_derived_anchors": {res["concept"]: {"anchor": res.get("anchor"),
                                                "firing_floor_validated": res.get("anchor_info", {}).get("firing_floor_validated"),
                                                "corpus_fire_rate": res.get("anchor_info", {}).get("corpus_fire_rate"),
                                                "spurious": res.get("spurious_anchor")}
                               for res in concept_results},
        "homograph_holes": {"per_country": homo, "Georgia": {"hole_ok": geo_hole_ok, **(geo or {})},
                            "Jordan": {"hole_ok": jor_hole_ok, **(jor or {})}, "verdict": piece_A},
        "repair_fdr": {"per_family_survivors": fam_sig, "deltas_vs_16k": deltas,
                       "n_repairs_tested": multiplicity.get("n_repairs_tested"),
                       "n_survive_FDR": multiplicity.get("n_survive_FDR"),
                       "distinct_hole_count": multiplicity.get("distinct_hole_count_survive_FDR"),
                       "distinct_total": multiplicity.get("distinct_total_survive_FDR"),
                       "statsmodels_crosscheck": multiplicity.get("statsmodels_crosscheck_matches"),
                       "ref_16k": REF_16K["per_family_survive_FDR"], "verdict": piece_B},
        "surgical": {"n_cases": len(surg_cases), "n_confirmed": len(confirmed),
                     "best_selectivity_ratio": best_surg.get("headline_selectivity_ratio") if best_surg else None,
                     "cases": surgical_summary, "ref_16k_georgia": REF_16K["surgical_georgia"], "verdict": piece_C},
        "router": {"frozen_16k_recall_hole_balanced_acc": router_xfer.get("frozen_16k_recall_hole_balanced_acc"),
                   "frozen_16k_firing_jaccard_balanced_acc": router_xfer.get("frozen_16k_firing_jaccard_balanced_acc"),
                   "rederived_65k_tau_h": router_xfer.get("rederived_65k_tau_h"),
                   "rederived_65k_recall_hole_balanced_acc": router_xfer.get("rederived_65k_recall_hole_balanced_acc"),
                   "tau_h": router_xfer.get("tau_h"), "tau_j": router_xfer.get("tau_j"),
                   "balanced_acc_recall_hole_alone": router_xfer.get("balanced_acc_recall_hole_alone"),
                   "balanced_acc_combined": router_xfer.get("balanced_acc_combined"),
                   "transfers": router_transfers, "ref_16k_tau_h": REF_16K["router_tau_h"], "verdict": piece_D},
        "regime_split": regime_split, "per_piece_verdicts": pieces, "overall_verdict": overall}


# =========================================================================== dataset rows
def replication_dataset_rows(table):
    """One exp_gen_sol_out example per (dictionary x piece x sub_context). input=descriptor, output=verdict."""
    dn = table["dictionary"]; ex = []
    # piece A homograph holes
    for country, d in table["homograph_holes"]["per_country"].items():
        rh = d.get("recall_hole"); jac = d.get("firing_jaccard")
        verdict = "HOLE_REPLICATES" if (rh is not None and rh > 0.5 and jac is not None and jac < 0.1) else "NO_HOLE"
        ex.append({"input": f"[{dn}|homograph_hole|{country}] does the parent recall-hole + low firing-Jaccard reappear on this dictionary?",
                   "output": verdict, "predict_hole_recall": (f"{float(rh):.4f}" if rh is not None else "NA"),
                   "metadata_dictionary": dn, "metadata_layer": table["layer"], "metadata_width": table["width"],
                   "metadata_piece": "homograph_holes", "metadata_subcontext": country,
                   "metadata_recall_hole": rh, "metadata_firing_jaccard": jac})
    # piece B repair fdr (per concept x X x variant from the concept results is huge; summarize per family)
    for fam, n in table["repair_fdr"]["per_family_survivors"].items():
        ex.append({"input": f"[{dn}|repair_fdr|{fam}] how many KG-repairs survive BH FDR<=0.05 vs 16k?",
                   "output": str(int(n)), "predict_delta_vs_16k": str(table["repair_fdr"]["deltas_vs_16k"].get(fam)),
                   "metadata_dictionary": dn, "metadata_piece": "repair_fdr", "metadata_subcontext": fam,
                   "metadata_survivors": int(n), "metadata_ref_16k": REF_16K["per_family_survive_FDR"].get(fam),
                   "metadata_delta_vs_16k": table["repair_fdr"]["deltas_vs_16k"].get(fam)})
    # piece C surgical (per case)
    for c in table["surgical"]["cases"]:
        ex.append({"input": f"[{dn}|surgical|{c['family']}/{c['subcontext']}] KG-ABL single re-derived absorber {c['absorber']}; surgical edit verdict?",
                   "output": c["verdict"], "predict_selectivity_ratio": (f"{c['selectivity_ratio']:.2f}" if c.get("selectivity_ratio") is not None else "NA"),
                   "metadata_dictionary": dn, "metadata_piece": "surgical", "metadata_subcontext": str(c["subcontext"]),
                   "metadata_family": c["family"], "metadata_absorber_latent": c["absorber"], "metadata_regime": c["regime"],
                   "metadata_selectivity_ratio": c["selectivity_ratio"], "metadata_kg_collateral": c["kg_collateral"],
                   "metadata_dense_collateral": c["dense_collateral"], "metadata_dense_minus_kg_excl0": c["dense_minus_kg_excl0"],
                   "metadata_firing_jaccard": c["firing_jaccard"], "metadata_parent_recall_hole": c["parent_recall_hole"]})
    # piece D router
    ex.append({"input": f"[{dn}|router] do FROZEN 16k thresholds (recall-hole lead) still classify absorption vs co-firing?",
               "output": "TRANSFERS" if table["router"]["transfers"] else "DICTIONARY_SPECIFIC",
               "predict_balanced_acc": (f"{table['router']['frozen_16k_recall_hole_balanced_acc']:.4f}"
                                        if table["router"].get("frozen_16k_recall_hole_balanced_acc") is not None else "NA"),
               "metadata_dictionary": dn, "metadata_piece": "router", "metadata_subcontext": "ALL",
               "metadata_frozen_16k_balanced_acc": table["router"]["frozen_16k_recall_hole_balanced_acc"],
               "metadata_rederived_65k_balanced_acc": table["router"]["rederived_65k_recall_hole_balanced_acc"],
               "metadata_tau_h": table["router"]["tau_h"]})
    # overall
    ex.append({"input": f"[{dn}|OVERALL] cross-dictionary replication verdict for the auditability spine",
               "output": table["overall_verdict"].upper(), "predict_overall_verdict": table["overall_verdict"].upper(),
               "metadata_dictionary": dn, "metadata_piece": "overall", "metadata_subcontext": "ALL",
               "metadata_per_piece": json.dumps(table["per_piece_verdicts"])})
    return ex


def repair_dataset_rows(dict_name, concept_results):
    ex = []
    for res in concept_results:
        concept = res["concept"]; anchor = res.get("anchor")
        for X, e in res.get("repair", {}).get("per_subcontext", {}).items():
            if e.get("status") != "measured":
                continue
            for vn, v in e.get("variants", {}).items():
                out_label = ("survives_FDR" if v.get("survives_FDR") else
                             ("repair_significant" if v["measured_success"] else "tie_with_random"))
                ex.append({"input": f"[{dict_name}] {concept} | sub-context '{X}' | add re-derived KG absorber "
                                    f"{v['absorber_latent']} ({vn}) to re-derived anchor {anchor}",
                           "output": out_label,
                           "predict_kg_repair": ("REPAIR" if v["measured_success"] else "NO_REPAIR"),
                           "predict_random_baseline": "NO_REPAIR",
                           "metadata_dictionary": dict_name, "metadata_concept": concept,
                           "metadata_subcontext": str(X), "metadata_variant": vn, "metadata_is_hole": e.get("is_hole"),
                           "metadata_recall_anchor_eval": e["recall_anchor_eval"], "metadata_gain_kg": v["gain_kg"],
                           "metadata_kg_percentile_vs_random": v["kg_percentile_vs_random"],
                           "metadata_p_value": v["p_value_one_sided"], "metadata_bh_q": v.get("bh_q"),
                           "metadata_survives_FDR": v.get("survives_FDR"), "metadata_n_eval": e["n_eval"]})
    return ex


# =========================================================================== gating
def run_gating(dict_name, cfg, sae, mb, torch):
    tax_src = load_d2("taxonomic_absorption")
    gate_rows = [r for r in tax_src if r["metadata_row_type"] == "corpus"][:64]
    layer_idx, fvu = mb.determine_layer_idx(gate_rows, sae, cfg["hidden_search"])
    lat_g, resid_g, align_g = mb.encode_rows(gate_rows, sae)
    hb = torch.tensor(resid_g.astype(np.float32), device=DEVICE)
    z = sae.encode(hb); hr = sae.decode(z)
    cos = float(torch.nn.functional.cosine_similarity(hb, hr, dim=-1).mean())
    l0 = float((z > 0).sum(1).float().mean())
    del hb, z, hr
    # spelling cosine (descriptive)
    spell_cos = None
    try:
        gl = load_first_letter(["L"])
        srows = [r for r in gl["L"] if r.get("metadata_pair_type") == "corpus_context"][:48]
        _, sresid, _ = mb.encode_rows(srows, sae)
        hs = torch.tensor(sresid.astype(np.float32), device=DEVICE)
        zs = sae.encode(hs)
        spell_cos = float(torch.nn.functional.cosine_similarity(hs, sae.decode(zs), dim=-1).mean())
        del hs, zs
    except Exception as e:  # noqa: BLE001
        logger.warning(f"spelling cosine failed: {e}")
    # numeric digit-token cosine (descriptive)
    num_cos = None
    try:
        num_src = load_d2("numeric_absorption")
        nrows = [r for r in num_src if r["metadata_row_type"] == "corpus"][:48]
        _, nresid, _ = mb.encode_rows(nrows, sae)
        hn = torch.tensor(nresid.astype(np.float32), device=DEVICE)
        zn = sae.encode(hn)
        num_cos = float(torch.nn.functional.cosine_similarity(hn, sae.decode(zn), dim=-1).mean())
        del hn, zn
    except Exception as e:  # noqa: BLE001
        logger.warning(f"numeric cosine failed: {e}")
    gating = {"pass": bool(cos > 0.9), "cosine": cos, "L0": l0, "align": align_g, "layer_idx": int(layer_idx),
              "expected_layer_idx": cfg.get("expect_hidden"), "spelling_cosine_descriptive": spell_cos,
              "numeric_digit_cosine_descriptive": num_cos, "avg_l0": sae.avg_l0,
              "gate_concept": "taxonomic (global SAE/layer mapping check)",
              "fvu_by_idx": {str(k): v for k, v in fvu.items()},
              "delta_cosine_vs_16k": float(cos - REF_16K["gating_cosine"])}
    logger.info(f"{el()} [{dict_name}] GATING cosine={cos:.4f} L0={l0:.1f} layer_idx={layer_idx} "
                f"spell_cos={spell_cos} num_cos={num_cos} (16k ref cosine={REF_16K['gating_cosine']})")
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return gating


# =========================================================================== MAIN
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dicts", default="65k", help="comma list of dictionaries (65k,l9_16k,l6_16k)")
    ap.add_argument("--families", default="taxonomic,spelling,toxicity,numeric")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--cap", type=int, default=0, help="cap corpus rows per sub-context/fold (0=all)")
    ap.add_argument("--kl_prompts", type=int, default=24)
    ap.add_argument("--member_labeling", action="store_true", help="run optional M7 LLM member-labeling (budget-gated)")
    ap.add_argument("--out", default=str(WORK / "method_out.json"))
    args = ap.parse_args()
    set_limits()

    import torch
    torch.manual_seed(SEED)
    if torch.cuda.is_available():
        try:
            torch.cuda.set_per_process_memory_fraction(0.9)
        except Exception:  # noqa: BLE001
            pass
    logger.info(f"{el()} torch {torch.__version__} cuda={torch.cuda.is_available()} device={DEVICE}")

    mb = ModelBundle(torch)
    dict_names = [d.strip() for d in args.dicts.split(",") if d.strip()]
    fams = [f.strip() for f in args.families.split(",") if f.strip()]
    member_payloads = []

    out = {"metadata": {
        "method_name": "M2 — Cross-Dictionary Replication of the iter-4 auditability spine on a second Gemma-Scope SAE",
        "description": ("Re-run the homograph recall-holes + KG-repair FDR survivors + Georgia/Jordan surgical edits + "
                        "recall-hole/firing-Jaccard router on a SECOND Gemma-Scope SAE dictionary of the SAME frozen "
                        "gemma-2-2b (PRIMARY width-65k layer-12 canonical; SECONDARY reduced layer-9 width-16k), with "
                        "anchors AND absorbers RE-DERIVED per dictionary (16k latent ids do not carry over). Per-piece "
                        "REPLICATES / PARTIAL / DICTIONARY-DEPENDENT verdict + honest deltas vs the 16k counts."),
        "model": mb.model_id, "seed": SEED, "B_boot": B_BOOT, "release": RELEASE_REPO,
        "thresholds": {"N_MIN_EVAL": N_MIN_EVAL, "N_MIN_RELAX": N_MIN_RELAX, "N_MIN_SEL": N_MIN_SEL,
                       "HOLE_RECALL_MAX": HOLE_RECALL_MAX, "KG_JACCARD_MAX": KG_JACCARD_MAX,
                       "KG_PREC_MIN": KG_PREC_MIN, "SPURIOUS_FIRE_FLOOR": SPURIOUS_FIRE_FLOOR, "FDR_ALPHA": FDR_ALPHA},
        "reference_16k_iter4": REF_16K, "dictionaries": {}, "replication_tables": {},
        "router_transfer": {}, "per_dictionary_concept_results": {}, "verdict": {}},
        "datasets": []}

    all_repl_rows = []
    all_repair_rows = []
    all_pred_rows = []
    per_dict_overall = {}

    for dict_name in dict_names:
        if dict_name not in DICTS:
            logger.warning(f"unknown dict {dict_name}; skipping")
            continue
        cfg = DICTS[dict_name]
        logger.info(f"\n{el()} ################# DICTIONARY {dict_name} (layer {cfg['layer']} width {cfg['width']}) #################")
        sae = load_sae(torch, cfg, dict_name)
        W_dec_np = sae.W_dec.cpu().numpy()
        gating = run_gating(dict_name, cfg, sae, mb, torch)
        out["metadata"]["dictionaries"][dict_name] = {"layer": cfg["layer"], "width": cfg["width"],
                                                      "sae_id": sae.sae_id, "avg_l0": sae.avg_l0,
                                                      "expect_dsae": cfg.get("expect_dsae"), "d_sae": int(sae.d_sae),
                                                      "gating": gating, "reduced": cfg.get("reduced", False)}
        if args.smoke:
            del sae, W_dec_np; gc.collect(); torch.cuda.empty_cache()
            continue
        if not gating["pass"]:
            logger.warning(f"[{dict_name}] GATING cosine {gating['cosine']:.4f}<=0.9 — demote spelling/numeric to descriptive, continue")

        reduced = cfg.get("reduced", False)
        concept_results = []
        tox_result = None
        # taxonomic (always; NEVER-DROP)
        if "taxonomic" in fams:
            tax = run_d2_concept("taxonomic", "taxonomic_absorption", dict_name, sae, mb, W_dec_np, args,
                                 member_payloads, torch, do_surgical=True,
                                 surgical_targets=["Georgia", "Jordan", "United States"])
            if tax:
                concept_results.append(tax)
        if not reduced:
            if "numeric" in fams:
                num = run_d2_concept("numeric", "numeric_absorption", dict_name, sae, mb, W_dec_np, args,
                                     member_payloads, torch, do_surgical=False)
                if num:
                    concept_results.append(num)
            if "spelling" in fams:
                fl = run_first_letter(["L", "O", "T", "I", "D"], dict_name, sae, mb, W_dec_np, args,
                                      member_payloads, torch, do_surgical=True)
                for lt, r in fl.items():
                    concept_results.append(r)
            if "toxicity" in fams:
                tox_result = run_toxicity(dict_name, sae, mb, W_dec_np, args, torch)

        multiplicity = apply_multiplicity(concept_results)
        rxfer = router_transfer(concept_results, tox_result)
        table = build_replication_table(dict_name, cfg, sae, gating, concept_results, tox_result, multiplicity, rxfer)
        out["metadata"]["replication_tables"][dict_name] = table
        out["metadata"]["router_transfer"][dict_name] = rxfer
        # store compact concept results (drop heavy per-case curves to keep json small)
        compact = []
        for res in concept_results + ([tox_result] if tox_result else []):
            rc = {k: v for k, v in res.items() if k != "surgical_cases"}
            rc["surgical_cases"] = [{kk: vv for kk, vv in c.items() if kk not in ("curves", "prediction_rows")}
                                    for c in res.get("surgical_cases", [])]
            compact.append(rc)
            for c in res.get("surgical_cases", []):
                all_pred_rows.extend(c.get("prediction_rows", []))
        out["metadata"]["per_dictionary_concept_results"][dict_name] = compact
        out["metadata"]["dictionaries"][dict_name]["multiplicity"] = multiplicity
        all_repl_rows.extend(replication_dataset_rows(table))
        all_repair_rows.extend(repair_dataset_rows(dict_name, concept_results))
        per_dict_overall[dict_name] = table["overall_verdict"]
        logger.info(f"{el()} [{dict_name}] OVERALL VERDICT = {table['overall_verdict']} pieces={table['per_piece_verdicts']}")
        del sae, W_dec_np; gc.collect(); torch.cuda.empty_cache()

    if args.smoke:
        out["datasets"] = [{"dataset": "smoke", "examples": [{"input": "smoke", "output": "ok"}]}]
        save_json(out, args.out)
        logger.info(f"{el()} SMOKE done dicts={dict_names}")
        return

    # optional member labeling across all dicts
    if args.member_labeling and member_payloads:
        judge = LLMJudge(enabled=True)
        logger.info(f"\n{el()} ===== MEMBER-LABELING ({len(member_payloads)} members) =====")
        label_results = member_labeling(judge, member_payloads)
        scoring = score_labeling(label_results)
        out["metadata"]["member_labeling"] = {"scoring": scoring, "llm_cost_usd": round(judge.cost, 5),
                                               "llm_calls": judge.calls, "n_members": len(member_payloads),
                                               "per_member": label_results}
        member_examples = [{"input": f"{r['concept']} member {r['member']} ({r['role']})",
                            "output": r["ground_truth_label"], "predict_judge": r["judge_label"],
                            "metadata_concept": r["concept"], "metadata_correct": r["correct"],
                            "metadata_confident": r["confident"]} for r in label_results]
    else:
        out["metadata"]["member_labeling"] = {"status": "skipped (core spine is $0 LLM; run with --member_labeling)"}
        member_examples = []

    # overall cross-dictionary verdict
    primary = "65k" if "65k" in per_dict_overall else (dict_names[0] if dict_names else None)
    cross = per_dict_overall.get(primary, "not_run")
    out["metadata"]["verdict"] = {
        "cross_dictionary_replicates": cross, "per_dictionary": per_dict_overall, "primary_dictionary": primary,
        "n_dictionaries": len(per_dict_overall),
        "notes": ("Per-piece REPLICATES/PARTIAL/DICTIONARY-DEPENDENT for homograph-holes, repair-FDR, surgical edit, "
                  "and router transfer on each dictionary; anchors+absorbers re-derived per dictionary. A clean "
                  "non-replication is the publishable wider-SAE-absorbs-more (dictionary-dependence) finding.")}

    _empty = [{"input": "none", "output": "NONE", "predict_none": "NONE"}]
    datasets = [{"dataset": "cross_dictionary_replication", "examples": all_repl_rows or _empty},
                {"dataset": "kg_repair_loop", "examples": all_repair_rows or _empty},
                {"dataset": "edit_locality_per_context", "examples": all_pred_rows or _empty}]
    if member_examples:
        datasets.append({"dataset": "member_labeling", "examples": member_examples})
    out["datasets"] = datasets

    save_json(out, args.out)
    logger.info(f"{el()} SAVED {args.out}")
    logger.info(f"{el()} CROSS-DICTIONARY VERDICT={cross} per_dict={per_dict_overall}")
    for dn, table in out["metadata"]["replication_tables"].items():
        logger.info(f"  [{dn}] pieces={table['per_piece_verdicts']} overall={table['overall_verdict']}")


if __name__ == "__main__":
    main()
