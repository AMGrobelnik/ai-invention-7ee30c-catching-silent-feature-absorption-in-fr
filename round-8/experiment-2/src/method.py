#!/usr/bin/env python
"""
iter-8 M2''' + M3''' : Base-Widener + Concentration-vs-Absorption Population Test
================================================================================
Two-track Counterfactual Co-Response Grouping (CCRG) auditability spine, iter-8.

iter-7 established that ONE KG-named SAE absorber latent beats a footprint-matched gated-dense control
at meaningful forget -- but ONLY for the spelling word 'large' (concentrated), while the distributed
country senses Georgia/Jordan could not forget at all (NO_MEANINGFUL_FORGET). The open questions:

  M2'''  (BASE WIDTH): screening a WIDER vocabulary of candidate tokens (spelling word-absorbers across
         L/O/T/I/D + homograph entities: brands / given-names / months / cities), how many clear the
         fair-control bar at MEANINGFUL forget? -> verdict BASE_REACHES_4_PLUS vs BASE_STAYS_THIN_RETARGET.
  M3'''  (PREDICTOR): does a candidate's CONTINUOUS lexical-CONCENTRATION score (per-sub-context firing
         precision x sparse global footprint) predict its edit-win / meaningful-forget outcome BETTER than
         its BINARY absorption-regime label? (The decisive population evidence for the reframe.)
  M5'''  (SET-COVER INERTNESS): per candidate, does the anchored precision-selected absorber EQUAL the
         unconstrained max-precision latent? (If yes for most -> the K-track set-cover step is inert and
         the method reduces to precise-latent discovery -- an honest negative.)

UNIFIED FAIR OPERATOR (the only new edit code; added to core.make_edit_hook):
  DENSE-SUB-ABL-GATED-FAIR:  h <- h - min(beta,1)*(h.u_sub)*u_sub   applied ONLY where d_sub(h) > gate_thresh
  where u_sub is the labeled sub-direction (diff-of-means) and d_sub is the PRECISE supervised sub-probe
  (AUC~1.0). vs iter-7's crude |h.u_sub|>tau magnitude gate (which forced beta~3 over-erasure), this uses
  the high-AUC detector to decide WHERE to erase and caps erasure at full removal (beta<=1) -> the
  genuinely FAIR conditional-dense control.

Reuses iter-7 core.py / method.py (-> method_lib.py) VERBATIM for the SAE pipeline, edit operators, judges,
u_sub / d_sub, and the $0 meaningful-forget proof. Adds: a $0 concentration screen, a budget-bounded edit
loop, and the population correlation. GPU (gemma-2-2b + Gemma-Scope L12/16k). LLM judge target <$3, cap $10.

Usage:
  uv run method.py --smoke                              # logic check (2 cands, judges off), $0
  uv run method.py --unit                               # operator unit checks on 'large', $0
  uv run method.py --mini                               # 5 cands, both judges, reduced prompts, <$0.5
  uv run method.py                                       # full screen + budget-bounded edits
"""
import os, sys, json, time, gc, argparse, math
from pathlib import Path
from collections import Counter, defaultdict

import numpy as np

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")

import core
from core import (
    logger, el, load_sae, ModelBundle, content_responsive, paired_bootstrap_diff, bootstrap_mean_ci,
    load_taxonomic, load_first_letter, NEUTRAL_TEXT, save_json, select_positions, set_limits,
    _attach_span_fl, _attach_span_tax, DEVICE, SEED, B_BOOT, D_MODEL, ROOT,
)
import method_lib as M
from method_lib import (
    build_u_sub, fit_sub_probe, subprobe_positive_rate, read_resid_under_edit, last_tok_logprobs,
    generate_under_edit, harmonic_mean, run_judge_batch, resolve_second_judge, build_prompts,
    _gold_token_id, PRIMARY_JUDGE, SPENT, TARGET, HARD_CAP, PER_JUDGE,
)

WORK = Path("/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_2")
RESULTS = WORK / "results"; CACHE = WORK / "cache"; LOGS = WORK / "logs"
for d in (RESULTS, CACHE, LOGS):
    d.mkdir(parents=True, exist_ok=True)
KG4 = ROOT / "iter_4/gen_art/gen_art_experiment_1/method_out.json"
HG_FULL = WORK / "homograph_data/full_data_out.json"
HG_MANIFEST = WORK / "homograph_data/manifest.json"

rng = np.random.default_rng(SEED)

# ----------------------------------------------------------------------------- config / grids
LAM_GRID = [0.0, 0.5, 1.0, 2.0, 3.0, 4.0]               # KG / max-prec single-latent ablation lambda
BETA_GRID = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0]   # ungated dense u_sub erasure beta
FAIR_BETA_GRID = [0.0, 0.25, 0.5, 0.75, 1.0]            # BOUNDED fair gated dense (beta<=1)
FORGET_FLOOR = 0.10                                     # meaningful-forget sub-probe-drop floor
MIN_SUB = 20                                            # min fit rows/side for a trustworthy u_sub/d_sub
MIN_X_WIN = 12                                          # min target-sense corpus windows to screen a candidate
MIN_FIRE = 3                                            # min rows_X a latent must fire on to be precision-rankable
JAC_MAX = 0.10                                          # K-track anchor-disjointness Jaccard ceiling
PREC_K = 0.70                                           # K-track minimum balanced precision
HOLE_ABS = 0.60                                         # absorption_structured recall-hole threshold
EPS = 1e-9

# screen / encode caps (bound GPU wall-clock; cached)
CORPUS_CAP_PER_WORD = 120
SIB_CAP = 600
HG_CORPUS_CAP_PER_ENT = 150
HG_SIB_CAP = 700

# edit / judge caps
EDIT_TOPK = 14                                          # top concentration candidates to attempt to edit
N_FORGET = 18; N_RETAIN = 12; N_UNREL = 12
N_FORGET_MINI = 8; N_RETAIN_MINI = 6; N_UNREL_MINI = 6

# curated spelling word-absorber pool (plan C1); UNION with KG4 non-empty sub_by_absorber words
CURATED_SPELLING = {
    "L": ["large", "list", "line", "law", "like", "level", "low", "leave", "land", "life", "long", "light"],
    "O": ["our", "one", "only", "other", "out", "over", "old", "offer"],
    "T": ["that", "their", "there", "time", "take", "this", "the", "to"],
    "I": ["in", "into", "it", "is", "if", "its"],
    "D": ["day", "down", "do", "did", "does", "data"],
}
# reviewer-named homograph must-include + iter-7 positive-control anchors
CURATED_HG = {
    "brand": ["Apple", "Shell", "Target", "Orange", "Amazon"],
    "given_name": ["Grace", "Hope", "Mark", "Will"],
    "month": ["March", "June", "May"],
    "city": ["Bush", "Cook"],   # 'Bush'/'Cook' are surname/verb homographs in given_name/city per manifest
}
POSITIVE_CONTROLS = {"large"}            # the ONLY iter-7-established absorption KG_BEATS win
DISTRIBUTED_ANCHORS = {"Georgia", "Jordan"}   # iter-7 NO_MEANINGFUL_FORGET losers (low-concentration anchors)


# ============================================================================= attach span (homograph)
def _attach_span_hg(r):
    cs = r.get("metadata_target_char_start"); ce = r.get("metadata_target_char_end")
    r["_span"] = (cs, ce) if cs is not None else None
    ti = r.get("metadata_target_token_indices")
    r["_ti"] = list(ti) if ti else None
    r["_target"] = r.get("metadata_entity") or r.get("metadata_target_text")
    return r


# ============================================================================= neutral footprint
def compute_neutral_footprint(mb, sae, texts, max_len=64, batch=16):
    """Per-latent TOKEN-LEVEL firing rate over a broad neutral pool -> [d_sae] float32 in [0,1].
    footprint(l) = fraction of neutral tokens where z[l]>0 (global sparsity = how 'concentrated' l is)."""
    torch = mb.torch; tok = mb.tok
    cap = {}
    def cap_hook(_m, _i, o):
        cap["r"] = o[0] if isinstance(o, (tuple, list)) else o
    handle = mb.edit_layer().register_forward_hook(cap_hook)
    old = tok.padding_side; tok.padding_side = "right"
    fire = np.zeros(sae.d_sae, dtype=np.float64); ntok = 0
    try:
        for b0 in range(0, len(texts), batch):
            bp = [t for t in texts[b0:b0 + batch] if isinstance(t, str) and t.strip()]
            if not bp:
                continue
            enc = tok(bp, return_tensors="pt", add_special_tokens=True, padding=True,
                      truncation=True, max_length=max_len)
            am = enc["attention_mask"]
            enc = {k: vv.to(DEVICE) for k, vv in enc.items()}
            with torch.no_grad():
                mb.model.model(**enc)
                hs = cap["r"].to(torch.float32)
                mask = am.to(DEVICE).bool()
                rows = hs[mask]                      # [tokens, d_model]
                z = sae.encode(rows)                 # [tokens, d_sae]
                fire += (z > 0).sum(0).double().cpu().numpy()
                ntok += int(rows.shape[0])
            cap.clear()
    finally:
        handle.remove(); tok.padding_side = old
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    foot = (fire / max(ntok, 1)).astype(np.float32)
    logger.info(f"{el()} neutral footprint over {ntok} tokens (pool={len(texts)} texts)")
    return foot, ntok


# ============================================================================= family loaders
class Family:
    """One family-level encode (corpus + content pairs). Candidates are sliced by sub_context/entity."""
    pass


def _encode_family(mb, sae, name, enc_rows, whole_sentence=False, cache_tag=None):
    import scipy.sparse as sp
    cache_f = CACHE / f"enc_{cache_tag}.npz" if cache_tag else None
    if cache_f and cache_f.exists():
        try:
            d = np.load(cache_f, allow_pickle=True)
            if int(d["resid"].shape[0]) != len(enc_rows):
                logger.warning(f"[{name}] cache row mismatch ({d['resid'].shape[0]} != {len(enc_rows)}); re-encoding")
                raise ValueError("row mismatch")
            lat_csr = sp.csr_matrix((d["lat_data"], d["lat_idx"], d["lat_ptr"]),
                                    shape=(len(enc_rows), sae.d_sae))
            resid = d["resid"]
            logger.info(f"{el()} [{name}] loaded cached encode ({resid.shape[0]} rows) from {cache_f.name}")
            return lat_csr, resid
        except Exception as e:  # noqa: BLE001
            logger.warning(f"cache load/validate failed ({e}); re-encoding")
    lat_csr, resid, _ = mb.encode_rows(enc_rows, sae, whole_sentence=whole_sentence)
    if cache_f:
        np.savez_compressed(cache_f, lat_data=lat_csr.data, lat_idx=lat_csr.indices,
                            lat_ptr=lat_csr.indptr, resid=resid)
    return lat_csr, resid


def _content_responsive_set(lat_csr, on_idx, off_idx):
    if not on_idx or not off_idx:
        return np.array([], dtype=int), np.zeros(lat_csr.shape[1])
    n = min(len(on_idx), len(off_idx))
    A_on = np.asarray(lat_csr[on_idx[:n]].todense())
    A_off = np.asarray(lat_csr[off_idx[:n]].todense())
    cr, prec, _ = content_responsive(A_on, A_off)
    del A_on, A_off
    return cr, prec


def build_spelling(mb, sae, kg_anchors, cap=None, letters=("L", "O", "T", "I", "D")):
    """One encode over all requested letters' corpus + content-flip pairs. Candidate = a word; siblings =
    other words of the SAME letter (in target spelling-context). Anchor = KG4 per-letter parent latent."""
    groups = load_first_letter(list(letters))
    enc_rows, tag = [], []   # tag = (kind, key)
    word_counts = {}
    for lt in letters:
        rows = groups.get(lt, [])
        corp = [r for r in rows if r.get("metadata_pair_type") == "corpus_context"]
        wc = Counter(r.get("metadata_sub_context") for r in corp)
        word_counts[lt] = wc
        # per-word cap to bound encode; keep all if under cap
        per_word = defaultdict(int)
        for r in corp:
            w = r.get("metadata_sub_context")
            cc = cap or CORPUS_CAP_PER_WORD
            if per_word[w] >= cc:
                continue
            per_word[w] += 1
            r = _attach_span_fl(dict(r))
            enc_rows.append(r); tag.append(("corpus", lt, w, r.get("metadata_fold")))
        cf = [r for r in rows if r.get("metadata_pair_type") == "content_flip"
              and r.get("metadata_template_id") in {"t_verbose", "t_colon", "t_icl"}]
        for r in cf:
            r = _attach_span_fl(dict(r))
            enc_rows.append(r); tag.append(("cf", lt, r.get("metadata_role"), r.get("metadata_pair_id")))
    logger.info(f"{el()} [spelling] encoding {len(enc_rows)} rows across {letters}")
    lat_csr, resid = _encode_family(mb, sae, "spelling", enc_rows, cache_tag=f"spelling_{'_'.join(letters)}")
    fam = Family()
    fam.name = "first_letter_spelling"; fam.enc_rows = enc_rows; fam.lat_csr = lat_csr; fam.resid = resid
    fam.tag = tag; fam.whole_sentence = False
    fam.fit_folds = {0, 1, 2}; fam.eval_folds = {3, 4}
    fam.kg_anchors = kg_anchors           # {letter: anchor_latent}
    fam.word_counts = word_counts
    fam.kind = "spelling"
    return fam


def build_taxonomic(mb, sae, kg_anchor, cap=None):
    rows = load_taxonomic()
    eligible = ['Australia', 'Brazil', 'Canada', 'China', 'France', 'Georgia', 'Germany', 'India',
                'Iran', 'Ireland', 'Israel', 'Italy', 'Japan', 'Jordan', 'Mexico', 'New Zealand', 'Poland',
                'Russia', 'Spain', 'United Kingdom', 'United States']  # +Jordan (iter-7 distributed anchor)
    corp = [r for r in rows if r["metadata_row_type"] == "corpus"]
    cpairs = [r for r in rows if r["metadata_row_type"] == "content_pair"]
    enc_rows, tag = [], []
    per = defaultdict(int)
    for r in corp:
        sc = r.get("metadata_sub_context"); out = r["output"]
        if out == "positive" and sc in eligible:
            cc = cap or 300
            if per[sc] >= cc:
                continue
            per[sc] += 1
            r = _attach_span_tax(dict(r))
            enc_rows.append(r); tag.append(("corpus_pos", "country", sc, r.get("metadata_fold")))
        elif out == "negative":
            cc = (cap or 300)
            if per["_neg"] >= cc * 4:
                continue
            per["_neg"] += 1
            r = _attach_span_tax(dict(r))
            enc_rows.append(r); tag.append(("corpus_neg", "country", None, r.get("metadata_fold")))
    for r in cpairs:
        r = _attach_span_tax(dict(r))
        enc_rows.append(r); tag.append(("cf", "country", r.get("metadata_pair_role"), r.get("metadata_pair_id")))
    logger.info(f"{el()} [taxonomic] encoding {len(enc_rows)} rows")
    lat_csr, resid = _encode_family(mb, sae, "taxonomic", enc_rows, cache_tag="taxonomic")
    fam = Family()
    fam.name = "taxonomic_country"; fam.enc_rows = enc_rows; fam.lat_csr = lat_csr; fam.resid = resid
    fam.tag = tag; fam.whole_sentence = False
    fam.fit_folds = {"diagnostic"}; fam.eval_folds = {"train", "test"}
    fam.kg_anchors = {"country": kg_anchor}
    fam.eligible = eligible
    fam.kind = "taxonomic"
    return fam


def build_homograph(mb, sae, cap=None):
    if not HG_FULL.exists():
        logger.warning(f"{el()} homograph full_data_out.json absent -> skipping homograph family")
        return []
    blob = json.loads(HG_FULL.read_text())
    manifest = json.loads(HG_MANIFEST.read_text()) if HG_MANIFEST.exists() else {}
    readiness = manifest.get("absorption_readiness", {}) or {}
    fams = []
    for ds in blob["datasets"]:
        hname = ds["dataset"]; rows = ds["examples"]
        # detect hierarchy from first row
        hier = None
        for r in rows:
            if r.get("metadata_hierarchy"):
                hier = r["metadata_hierarchy"]; break
        if hier is None:
            continue
        corp = [r for r in rows if r.get("metadata_row_type") == "corpus"]
        cpairs = [r for r in rows if r.get("metadata_row_type") == "content_pair"]
        enc_rows, tag = [], []
        per = defaultdict(int)
        for r in corp:
            out = r["output"]; ent = r.get("metadata_entity"); ts = r.get("metadata_target_sense")
            if out == "positive" and ent and ts == hier:
                cc = cap or HG_CORPUS_CAP_PER_ENT
                if per[ent] >= cc:
                    continue
                per[ent] += 1
                r = _attach_span_hg(dict(r))
                enc_rows.append(r); tag.append(("corpus_pos", hier, ent, r.get("metadata_fold")))
            elif out == "negative":
                cc = (cap or HG_CORPUS_CAP_PER_ENT)
                if per["_neg"] >= cc * 8:
                    continue
                per["_neg"] += 1
                r = _attach_span_hg(dict(r))
                enc_rows.append(r); tag.append(("corpus_neg", hier, r.get("metadata_entity"),
                                                r.get("metadata_fold")))
        for r in cpairs:
            r = _attach_span_hg(dict(r))
            role = r.get("metadata_pair_role")
            enc_rows.append(r); tag.append(("cf", hier, role, r.get("metadata_pair_id")))
        if sum(1 for t in tag if t[0] == "corpus_pos") < MIN_X_WIN:
            logger.warning(f"{el()} [homograph/{hier}] too few target-sense positives -> skip")
            continue
        logger.info(f"{el()} [homograph/{hier}] encoding {len(enc_rows)} rows")
        lat_csr, resid = _encode_family(mb, sae, f"hg_{hier}", enc_rows, cache_tag=f"hg_{hier}")
        fam = Family()
        fam.name = f"homograph_{hier}"; fam.enc_rows = enc_rows; fam.lat_csr = lat_csr; fam.resid = resid
        fam.tag = tag; fam.whole_sentence = False
        # homograph corpus folds (mirror dataset_2): fit=diagnostic, eval=train/test; robust fallback below
        present_folds = set(t[3] for t in tag if t[0] == "corpus_pos")
        if "diagnostic" in present_folds:
            fam.fit_folds = {"diagnostic"}; fam.eval_folds = present_folds - {"diagnostic"}
        else:
            sf = sorted(str(x) for x in present_folds)
            fam.fit_folds = set(sf[:max(1, len(sf) // 2)]); fam.eval_folds = set(sf[max(1, len(sf) // 2):])
        fam.kg_anchors = {}            # homograph: anchor computed from data (no KG4)
        fam.hier = hier; fam.readiness = readiness; fam.kind = "homograph"
        fams.append(fam)
    return fams


# ============================================================================= per-family helpers
def _fam_arrays(fam):
    tag = fam.tag
    kind = np.array([t[0] for t in tag], dtype=object)
    sub = np.array([t[2] for t in tag], dtype=object)
    fold = np.array([t[3] for t in tag], dtype=object)
    return kind, sub, fold


def _firing_col(fam, l):
    """Boolean firing column for latent l over all family rows (CSC-backed + cached for speed)."""
    l = int(l)
    if not hasattr(fam, "_csc"):
        fam._csc = fam.lat_csr.tocsc(); fam._fcol_cache = {}
    c = fam._fcol_cache.get(l)
    if c is None:
        c = (np.asarray(fam._csc[:, l].todense()).ravel() > 0)
        fam._fcol_cache[l] = c
    return c


def _jaccard(a_bool, b_bool):
    inter = int((a_bool & b_bool).sum()); union = int((a_bool | b_bool).sum())
    return inter / max(union, 1)


def _family_candidates(fam):
    """Return {token: dict(x_idx_all, sib_idx_all)} for each screenable candidate in the family."""
    kind, sub, fold = _fam_arrays(fam)
    out = {}
    if fam.kind == "spelling":
        for lt in fam.kg_anchors.keys():
            # words in this letter with enough corpus windows
            mask_lt = np.array([(t[0] == "corpus" and t[1] == lt) for t in fam.tag])
            words = [w for w, c in Counter(sub[mask_lt]).items() if w and c >= MIN_X_WIN]
            for w in words:
                x_idx = np.where(mask_lt & (sub == w))[0]
                sib_idx = np.where(mask_lt & (sub != w))[0]
                if len(sib_idx) > SIB_CAP:
                    sib_idx = rng.choice(sib_idx, SIB_CAP, replace=False)
                out[w] = {"x_idx": x_idx, "sib_idx": sib_idx, "letter": lt, "hierarchy": f"first_letter_{lt}",
                          "parent": lt}
    elif fam.kind == "taxonomic":
        mask_pos = (kind == "corpus_pos")
        for c in fam.eligible:
            x_idx = np.where(mask_pos & (sub == c))[0]
            if len(x_idx) < MIN_X_WIN:
                continue
            sib_idx = np.where(mask_pos & (sub != c))[0]
            if len(sib_idx) > SIB_CAP:
                sib_idx = rng.choice(sib_idx, SIB_CAP, replace=False)
            out[c] = {"x_idx": x_idx, "sib_idx": sib_idx, "letter": None, "hierarchy": "taxonomic_country",
                      "parent": "country"}
    elif fam.kind == "homograph":
        mask_pos = (kind == "corpus_pos")
        ents = [e for e, c in Counter(sub[mask_pos]).items() if e and c >= MIN_X_WIN]
        for e in ents:
            x_idx = np.where(mask_pos & (sub == e))[0]
            sib_idx = np.where(mask_pos & (sub != e))[0]
            if len(sib_idx) > HG_SIB_CAP:
                sib_idx = rng.choice(sib_idx, HG_SIB_CAP, replace=False)
            out[e] = {"x_idx": x_idx, "sib_idx": sib_idx, "letter": None,
                      "hierarchy": f"homograph_{fam.hier}", "parent": fam.hier}
    return out


def _family_cr(fam):
    """content-responsive latent set + pair precision at the FAMILY/parent level (cached on fam)."""
    if hasattr(fam, "_cr"):
        return fam._cr, fam._cr_prec
    tag = fam.tag
    pairs = {}
    for i, t in enumerate(tag):
        if t[0] == "cf":
            role = t[2]
            rn = "on" if role in ("on", "x_on") else ("off" if role in ("off", "x_off") else None)
            if rn:
                pairs.setdefault(t[3], {})[rn] = i
    on_idx = [d["on"] for d in pairs.values() if "on" in d and "off" in d]
    off_idx = [d["off"] for d in pairs.values() if "on" in d and "off" in d]
    cr, prec = _content_responsive_set(fam.lat_csr, on_idx, off_idx)
    fam._cr = cr; fam._cr_prec = prec
    logger.info(f"{el()} [{fam.name}] content-responsive latents: {len(cr)} (from {len(on_idx)} pairs)")
    return cr, prec


def _family_anchor(fam):
    """Parent/anchor latent: KG4 when available (spelling/taxonomic), else highest-recall content-responsive
    latent over ALL target-sense positives in the family (homograph)."""
    if hasattr(fam, "_anchor_by_parent"):
        return fam._anchor_by_parent
    cr, _ = _family_cr(fam)
    kind, sub, fold = _fam_arrays(fam)
    by_parent = {}
    if fam.kind == "spelling":
        by_parent = {lt: int(a) for lt, a in fam.kg_anchors.items()}
    elif fam.kind == "taxonomic":
        by_parent = {"country": int(fam.kg_anchors["country"])}
    elif fam.kind == "homograph":
        pos_idx = np.where(kind == "corpus_pos")[0]
        if len(cr) and len(pos_idx):
            sub_csr = fam.lat_csr[pos_idx][:, cr]
            recall = np.asarray((sub_csr > 0).mean(0)).ravel()
            anc = int(cr[int(np.argmax(recall))])
        else:
            anc = -1
        by_parent = {fam.hier: anc}
    fam._anchor_by_parent = by_parent
    return by_parent


# ============================================================================= STEP D: concentration screen
def _capture_fraction(fam, x_idx, sib_idx, latent, W_dec_np):
    """$0 analytic forget proxy: fraction of the average X-context's frozen sub-probe (d_sub) MARGIN removed
    by ablating `latent` once. capture = mean_X(z_latent * (W_dec[latent].w_dsub)) / mean_X(margin). High =>
    the sub-context's detectable signal is CONCENTRATED in the single latent (editable, like spelling 'large');
    low => DISTRIBUTED across many latents (Georgia/Jordan country sense). Returns (capture, d_sub_auc) or
    (None, None) if d_sub cannot be fit (too few rows)."""
    if latent is None:
        return None, None
    N = fam.lat_csr.shape[0]
    pm = np.zeros(N, bool); pm[x_idx] = True
    sm = np.zeros(N, bool); sm[sib_idx] = True
    ds = fit_sub_probe(fam.resid, pm, sm)
    if ds is None:
        return None, None
    w = ds["w"].astype(np.float32); b = float(ds["b"])
    margin = fam.resid[x_idx].astype(np.float32) @ w + b
    z_abs = np.asarray(fam.lat_csr[x_idx][:, int(latent)].todense()).ravel().astype(np.float32)
    dmargin = z_abs * float(W_dec_np[int(latent)] @ w)
    mm = float(np.mean(margin))
    cap = float(np.mean(dmargin) / mm) if abs(mm) > 1e-6 else 0.0
    return float(np.clip(cap, 0.0, 1.5)), round(float(ds["auc"]), 4)


def screen_candidate(fam, token, info, neutral_foot, W_dec_np):
    """$0 lexical-concentration screen for one candidate. Never gates on absorption structure.

    PRIMARY concentration_score = d_sub-margin CAPTURE fraction (single-latent share of the sub-direction;
    discriminates editable spelling absorbers from distributed country senses). The plan's literal firing
    formula precision*(1-footprint) SATURATES (~0.98 for any candidate with a precise sparse latent) so it is
    reported as the secondary `concentration_firing` only -- see metadata.honest_negatives."""
    lat_csr = fam.lat_csr
    cr, _ = _family_cr(fam)
    anchor = _family_anchor(fam).get(info["parent"], -1)
    x_idx = info["x_idx"]; sib_idx = info["sib_idx"]
    if len(cr) == 0:
        cr = np.arange(lat_csr.shape[1])
    # per-candidate firing stats over cr latents
    Xc = np.asarray((lat_csr[x_idx][:, cr] > 0).mean(0)).ravel()        # recall/coverage on rows_X
    Sc = np.asarray((lat_csr[sib_idx][:, cr] > 0).mean(0)).ravel() if len(sib_idx) else np.zeros(len(cr))
    prec_bal = Xc / (Xc + Sc + EPS)                                     # class-balanced precision P(X|fires)
    fire_count_X = np.asarray((lat_csr[x_idx][:, cr] > 0).sum(0)).ravel()
    # anchor firing column + recall hole
    anc_bool = _firing_col(fam, anchor) if anchor >= 0 else np.zeros(lat_csr.shape[0], dtype=bool)
    recall_hole = 1.0 - float(anc_bool[x_idx].mean()) if anchor >= 0 else 1.0
    # K-track anchored absorber: jaccard(l,anchor)<JAC_MAX AND prec_bal>=PREC_K, maximize coverage(recall)
    absorber = None
    best_cov = -1.0
    for j, l in enumerate(cr):
        if fire_count_X[j] < MIN_FIRE:
            continue
        if prec_bal[j] < PREC_K:
            continue
        jac = _jaccard(_firing_col(fam, l), anc_bool) if anchor >= 0 else 0.0
        if jac >= JAC_MAX:
            continue
        if Xc[j] > best_cov:
            best_cov = Xc[j]; absorber = int(l)
    # unconstrained max-precision latent (M3'''/M5''' baseline; no anchor/jaccard constraint)
    elig = np.where(fire_count_X >= MIN_FIRE)[0]
    max_prec_latent = int(cr[elig[int(np.argmax(prec_bal[elig]))]]) if len(elig) else None
    chosen = absorber if absorber is not None else max_prec_latent
    if chosen is None:
        precision = 0.0; footprint = 1.0; coverage = 0.0
    else:
        jj = int(np.where(cr == chosen)[0][0])
        precision = float(prec_bal[jj]); coverage = float(Xc[jj])
        footprint = float(neutral_foot[chosen])
    concentration_firing = float(precision * (1.0 - footprint))
    capture, dsub_auc = _capture_fraction(fam, x_idx, sib_idx, chosen, W_dec_np)
    concentration = float(capture) if capture is not None else 0.0
    firing_jaccard = (_jaccard(_firing_col(fam, absorber), anc_bool)
                      if (absorber is not None and anchor >= 0) else
                      (_jaccard(_firing_col(fam, chosen), anc_bool) if (chosen is not None and anchor >= 0) else 1.0))
    absorption_structured = bool(recall_hole >= HOLE_ABS and firing_jaccard < JAC_MAX)
    set_cover_eq = bool(absorber is not None and absorber == max_prec_latent)
    return {
        "token": token, "hierarchy": info["hierarchy"], "parent": info["parent"], "family": fam.name,
        "n_x": int(len(x_idx)), "n_sib": int(len(sib_idx)), "anchor": int(anchor),
        "precision": round(precision, 4), "footprint": round(footprint, 6), "coverage": round(coverage, 4),
        "concentration_score": round(concentration, 4), "concentration_firing": round(concentration_firing, 4),
        "screen_dsub_auc": dsub_auc, "recall_hole": round(float(recall_hole), 4),
        "firing_jaccard": round(float(firing_jaccard), 4),
        "absorber": absorber, "max_prec_latent": max_prec_latent,
        "set_cover_eq_max_precision": set_cover_eq, "absorption_structured": absorption_structured,
        "structure_absent": bool(absorber is None),
    }


# ============================================================================= STEP F helpers
def _split_idx(fam, idx):
    """Split row indices into (fit, eval) by the family's fold sets; fallback deterministic if no overlap."""
    _, _, fold = _fam_arrays(fam)
    fit = np.array([i for i in idx if fold[i] in fam.fit_folds], dtype=int)
    ev = np.array([i for i in idx if fold[i] in fam.eval_folds], dtype=int)
    if len(fit) < 5 or len(ev) < 5:   # fallback: deterministic 60/40 by position (still disjoint)
        idx = np.asarray(idx)
        k = max(1, int(len(idx) * 0.6))
        fit = idx[:k]; ev = idx[k:]
    return fit, ev


def _completion_probes(fam, token):
    """Templated target-sense completion probes -> list of (prompt, gold_string) or [] if none."""
    if fam.kind == "spelling":
        L = token[0].upper()
        return [(f"{token} starts with the letter", L),
                (f"The first letter of the word {token} is", L),
                (f"The word {token} begins with the letter", L),
                (f"{token} is spelled starting with", L),
                (f'"{token}" starts with the letter', L)]
    if fam.kind == "taxonomic":
        caps = {"Georgia": "Tbilisi", "Jordan": "Amman"}
        if token in caps:
            g = caps[token]
            return [(f"The capital of {token} is", g), (f"{token}'s capital city is", g),
                    (f"The largest city in {token} is", g)]
        return []
    if fam.kind == "homograph" and fam.hier == "month":
        order = ["January", "February", "March", "April", "May", "June", "July", "August",
                 "September", "October", "November", "December"]
        if token in order:
            i = order.index(token); prev = order[(i - 1) % 12]
            return [(f"The month after {prev} is", token), (f"The month that comes after {prev} is", token)]
        return []
    return []


def _completion_drop(mb, sae, probes, op_kwargs_map):
    """logp of gold continuation token under each op at its s_op; drop = logp_NOOP - logp_op (+CI)."""
    if not probes:
        return None
    prompts = [p for p, _ in probes]
    golds = [_gold_token_id(mb.tok, g) for _, g in probes]
    base = last_tok_logprobs(mb, sae, prompts, kind=None)
    base_lp = np.array([float(base[i, golds[i]]) for i in range(len(prompts))])
    out = {"NOOP": {"mean_logp": float(base_lp.mean()), "drop": 0.0, "drop_ci": None}}
    for op, kw in op_kwargs_map.items():
        lp = last_tok_logprobs(mb, sae, prompts, **kw)
        op_lp = np.array([float(lp[i, golds[i]]) for i in range(len(prompts))])
        ci = paired_bootstrap_diff(base_lp, op_lp) if len(base_lp) >= 3 else None
        out[op] = {"mean_logp": float(op_lp.mean()), "drop": float(base_lp.mean() - op_lp.mean()),
                   "drop_ci": ci}
    return out


def _op_edit_kwargs(op, absorber, max_prec, u_sub_t, dsub, scale, gate_thresh=0.0):
    if op == "KG-ABL":
        return {"kind": "abl_latent", "l": int(absorber), "scale": scale}
    if op == "MAX-PREC-ABL":
        return {"kind": "abl_latent", "l": int(max_prec), "scale": scale}
    if op == "DENSE-SUB-ABL":
        return {"kind": "erase_dir", "u": u_sub_t, "scale": scale}
    if op == "DENSE-SUB-ABL-GATED-FAIR":
        return {"kind": "erase_dir_gated_fair", "u": u_sub_t, "scale": scale,
                "gw": dsub["w_t"], "gb": dsub["b"], "gate_thresh": gate_thresh}
    raise ValueError(op)


def _subdrop_curve(mb, sae, x_eval_rows, dsub, base_rate, op, absorber, max_prec, u_sub_t, grid,
                   gate_thresh=0.0):
    """Behavioral forget curve: sub-probe positive-rate DROP at each scale (M4''': behavior, not KL)."""
    sds = [0.0]
    for s in grid[1:]:
        kw = _op_edit_kwargs(op, absorber, max_prec, u_sub_t, dsub, s, gate_thresh)
        kw2 = {k: v for k, v in kw.items() if k in ("kind", "l", "u", "scale", "gw", "gb", "gate_thresh")}
        resid_e = read_resid_under_edit(mb, sae, x_eval_rows, **kw2)
        sds.append(float(base_rate - subprobe_positive_rate(dsub, resid_e)))
    return sds


def _scale_at(grid, curve, target):
    """smallest scale whose interpolated drop reaches target; (None, saturated) if unreachable."""
    g = np.asarray(grid, float); c = np.asarray(curve, float)
    if c.max() < target:
        return float(g[int(np.argmax(c))]), True
    order = np.argsort(c)
    return float(np.interp(target, c[order], g[order])), False


def _collect_joint(judged, gen, op, pair_op=None):
    """Per-prompt joint = HM(fluency, content_pres) across FORGET (forget-quality) + RETAIN/UNREL (preserve).
    If pair_op given, return aligned (a_op, a_pairop) arrays over prompts BOTH judged (for paired bootstrap)."""
    a, b = [], []
    for role in ("FORGET", "RETAIN", "UNRELATED"):
        if role not in gen or role not in judged:
            continue
        npr = len(gen[role]["prompts"])
        ja = judged[role].get(op, [])
        jb = judged[role].get(pair_op, []) if pair_op else None
        for j in range(npr):
            ra = ja[j] if j < len(ja) else None
            if ra is None:
                continue
            if pair_op is not None:
                rb = jb[j] if (jb and j < len(jb)) else None
                if rb is None:
                    continue
                b.append(harmonic_mean(rb["fluency"], rb["content_pres"]))
            a.append(harmonic_mean(ra["fluency"], ra["content_pres"]))
    if pair_op is not None:
        return np.array(a), np.array(b)
    return np.array(a)


# ============================================================================= STEP F: edit one candidate
def edit_candidate(mb, sae, fam, scr, judges, prompt_caps, do_maxprec_judge=False):
    """Build u_sub/d_sub, sweep operators, find matched meaningful-forget point, judge joint, fork.
    Returns (edit_summary_dict, list_of_prediction_rows). edit_summary['status'] in:
       concentrated_win / meaningful_no_win / no_meaningful_forget / descriptive_only / structure_absent."""
    torch = mb.torch
    token = scr["token"]; info = fam._cand_info[token]
    x_idx = info["x_idx"]; sib_idx = info["sib_idx"]
    absorber = scr["absorber"]; max_prec = scr["max_prec_latent"]
    out = dict(scr)  # carry screen fields
    preds = []
    if absorber is None and max_prec is None:
        out["status"] = "structure_absent"; out["meaningful_forget"] = False
        return out, preds
    edit_latent = absorber if absorber is not None else max_prec

    # ---- folds + masks
    x_fit, x_eval = _split_idx(fam, x_idx)
    s_fit, s_eval = _split_idx(fam, sib_idx)
    N = len(fam.tag)
    pos_mask = np.zeros(N, bool); pos_mask[x_fit] = True
    sib_mask = np.zeros(N, bool); sib_mask[s_fit] = True
    fb_pos = np.zeros(N, bool); fb_pos[x_idx] = True
    fb_sib = np.zeros(N, bool); fb_sib[sib_idx] = True
    resid = fam.resid
    # whole-parent direction for degenerate fallback
    par_pos = resid[x_idx].astype(np.float32).mean(0)
    kind, sub, fold = _fam_arrays(fam)
    neg_idx = np.where((kind == "corpus_neg"))[0]
    par_neg = resid[neg_idx].astype(np.float32).mean(0) if len(neg_idx) else resid[sib_idx].astype(np.float32).mean(0)
    u_whole = (par_pos - par_neg)

    u_sub_t, u_meta = build_u_sub(torch, resid, pos_mask, sib_mask, u_whole, fb_pos, fb_sib)
    dsub = fit_sub_probe(resid, pos_mask, sib_mask)
    out["u_sub_n_pos"] = u_meta["n_pos"]; out["u_sub_n_sib"] = u_meta["n_sib"]
    out["u_sub_auc"] = round(float(u_meta["sub_probe_auc"]), 4)
    out["u_sub_underpowered"] = bool(u_meta["underpowered"])
    out["d_sub_auc"] = round(float(dsub["auc"]), 4) if dsub else None
    if u_meta["underpowered"] or dsub is None or dsub.get("auc", 0) < 0.85:
        out["status"] = "descriptive_only"; out["meaningful_forget"] = False
        return out, preds
    dsub["w_t"] = torch.tensor(dsub["w"], device=DEVICE)

    # ---- eval rows for sub_drop + prompts
    x_eval_rows = [fam.enc_rows[i] for i in x_eval][:max(prompt_caps["forget"] * 2, 24)]
    base_rate = subprobe_positive_rate(dsub, resid[x_eval])
    out["subprobe_base_rate"] = round(float(base_rate), 4)

    # ---- sub_drop curves (behavioral forget; $0)
    curves = {}
    curves["KG-ABL"] = _subdrop_curve(mb, sae, x_eval_rows, dsub, base_rate, "KG-ABL", absorber, max_prec, u_sub_t, LAM_GRID)
    curves["DENSE-SUB-ABL"] = _subdrop_curve(mb, sae, x_eval_rows, dsub, base_rate, "DENSE-SUB-ABL", absorber, max_prec, u_sub_t, BETA_GRID)
    curves["DENSE-SUB-ABL-GATED-FAIR"] = _subdrop_curve(mb, sae, x_eval_rows, dsub, base_rate, "DENSE-SUB-ABL-GATED-FAIR", absorber, max_prec, u_sub_t, FAIR_BETA_GRID)
    if max_prec is not None:
        curves["MAX-PREC-ABL"] = _subdrop_curve(mb, sae, x_eval_rows, dsub, base_rate, "MAX-PREC-ABL", absorber, max_prec, u_sub_t, LAM_GRID)
    grids = {"KG-ABL": LAM_GRID, "DENSE-SUB-ABL": BETA_GRID, "DENSE-SUB-ABL-GATED-FAIR": FAIR_BETA_GRID,
             "MAX-PREC-ABL": LAM_GRID}
    maxsd = {op: float(np.max(c)) for op, c in curves.items()}
    out["max_subdrop"] = {op: round(v, 4) for op, v in maxsd.items()}
    out["subdrop_curves"] = {op: [round(x, 4) for x in c] for op, c in curves.items()}

    kg_max = maxsd["KG-ABL"]
    out["kg_max_subdrop"] = round(kg_max, 4)
    meaningful_forget = bool(kg_max >= FORGET_FLOOR)

    # ---- matched meaningful-forget target + per-op scale
    pair_ops = ["KG-ABL", "DENSE-SUB-ABL", "DENSE-SUB-ABL-GATED-FAIR"]
    matched_target = max(FORGET_FLOOR, 0.8 * min(maxsd[o] for o in pair_ops))
    out["matched_target"] = round(float(matched_target), 4)
    s_op = {}; saturated = {}
    judge_ops = ["KG-ABL", "DENSE-SUB-ABL", "DENSE-SUB-ABL-GATED-FAIR"]
    if do_maxprec_judge and "MAX-PREC-ABL" in curves:
        judge_ops.append("MAX-PREC-ABL")
    for op in judge_ops:
        s, sat = _scale_at(grids[op], curves[op], matched_target)
        s_op[op] = s; saturated[op] = sat
    out["s_op"] = {o: round(float(s_op[o]), 4) for o in s_op}
    out["fair_saturated"] = bool(saturated.get("DENSE-SUB-ABL-GATED-FAIR", False))

    # ---- completion-accuracy drop (deterministic $0)
    probes = _completion_probes(fam, token)
    comp_kwmap = {}
    for op in ("KG-ABL", "DENSE-SUB-ABL-GATED-FAIR"):
        kw = _op_edit_kwargs(op, absorber, max_prec, u_sub_t, dsub, s_op[op],
                             gate_thresh=0.0)
        comp_kwmap[op] = {k: v for k, v in kw.items() if k in ("kind", "l", "u", "scale", "gw", "gb", "gate_thresh")}
    comp = _completion_drop(mb, sae, probes, comp_kwmap) if probes else None
    if comp is not None:
        kg_comp = comp.get("KG-ABL", {})
        ci = kg_comp.get("drop_ci")
        out["completion_drop_kg"] = round(float(kg_comp.get("drop", 0.0)), 4)
        out["completion_ci_excl0"] = bool(ci["excl_0"]) if ci else False
        if out["completion_ci_excl0"] and kg_comp.get("drop", 0) > 0:
            meaningful_forget = True
    else:
        out["completion_drop_kg"] = None; out["completion_ci_excl0"] = False
    out["meaningful_forget"] = bool(meaningful_forget)

    # ---- judged joint at the matched point (2 judges) ----
    primary, second = judges
    if primary is None:   # judges disabled (smoke)
        out["status"] = ("meaningful_no_win" if meaningful_forget else "no_meaningful_forget")
        out["judges_disabled"] = True
        return out, preds

    fp = build_prompts([fam.enc_rows[i] for i in x_eval], "FORGET", prompt_caps["forget"], use_span=True)[0]
    rp = build_prompts([fam.enc_rows[i] for i in s_eval], "RETAIN", prompt_caps["retain"], use_span=True)[0]
    up = list(NEUTRAL_TEXT)[:prompt_caps["unrel"]]
    gen = {"FORGET": {"prompts": fp}, "RETAIN": {"prompts": rp}, "UNRELATED": {"prompts": up}}
    # NOOP + per-op continuations
    conts = {}
    for role in ("FORGET", "RETAIN", "UNRELATED"):
        prompts = gen[role]["prompts"]
        conts[role] = {"NOOP": generate_under_edit(mb, sae, prompts, kind=None)}
        for op in judge_ops:
            kw = _op_edit_kwargs(op, absorber, max_prec, u_sub_t, dsub, s_op[op], gate_thresh=0.0)
            kw2 = {k: v for k, v in kw.items() if k in ("kind", "l", "u", "scale", "gw", "gb", "gate_thresh")}
            conts[role][op] = generate_under_edit(mb, sae, prompts, clamp_norm=True, **kw2)

    # ---- prediction rows (per prompt) ----
    op2pred = {"KG-ABL": "predict_kg_abl", "DENSE-SUB-ABL": "predict_dense_sub_abl",
               "DENSE-SUB-ABL-GATED-FAIR": "predict_dense_sub_gated_fair", "MAX-PREC-ABL": "predict_max_precision"}
    for role in ("FORGET", "RETAIN", "UNRELATED"):
        prompts = gen[role]["prompts"]
        for j, p in enumerate(prompts):
            row = {"input": p, "output": role,
                   "predict_noop": str(conts[role]["NOOP"][j])[:300],
                   "predict_kg_abl": "NA", "predict_dense_sub_abl": "NA",
                   "predict_dense_sub_gated_fair": "NA", "predict_max_precision": "NA",
                   "metadata_token": token, "metadata_role": role, "metadata_family": fam.name,
                   "metadata_hierarchy": scr["hierarchy"]}
            for op in judge_ops:
                row[op2pred[op]] = str(conts[role][op][j])[:300]
            preds.append(row)

    # ---- judge ----
    def _judge_all(judge):
        judged = {}
        for role in ("FORGET", "RETAIN", "UNRELATED"):
            prompts = gen[role]["prompts"]
            judged[role] = {}
            for op in judge_ops:
                tasks = [{"role": role, "X": token, "prompt": prompts[j],
                          "base_cont": conts[role]["NOOP"][j], "edit_cont": conts[role][op][j]}
                         for j in range(len(prompts))]
                judged[role][op] = run_judge_batch(tasks, judge)
        return judged

    judged_p = _judge_all(primary)
    judged_s = _judge_all(second) if second else None

    def _deltas(judged):
        res = {}
        for op in ("DENSE-SUB-ABL", "DENSE-SUB-ABL-GATED-FAIR"):
            a, b = _collect_joint(judged, gen, "KG-ABL", pair_op=op)
            res[op] = paired_bootstrap_diff(a, b) if len(a) else None
        # per-op mean joint
        res["_joint"] = {op: (float(np.mean(_collect_joint(judged, gen, op))) if len(_collect_joint(judged, gen, op)) else None)
                         for op in judge_ops}
        return res

    dp = _deltas(judged_p)
    ds = _deltas(judged_s) if judged_s else None
    out["joint_primary"] = {o: (round(v, 4) if v is not None else None) for o, v in dp["_joint"].items()}
    if ds:
        out["joint_second"] = {o: (round(v, 4) if v is not None else None) for o, v in ds["_joint"].items()}

    def _ci_pack(ci):
        if ci is None:
            return None
        return {"diff": round(ci["diff"], 4), "ci_lo": round(ci["ci_lo"], 4), "ci_hi": round(ci["ci_hi"], 4),
                "excl_0": bool(ci["excl_0"]), "n": ci["n"]}
    out["delta_joint_vs_ungated_primary"] = _ci_pack(dp["DENSE-SUB-ABL"])
    out["delta_joint_vs_fair_primary"] = _ci_pack(dp["DENSE-SUB-ABL-GATED-FAIR"])
    if ds:
        out["delta_joint_vs_ungated_second"] = _ci_pack(ds["DENSE-SUB-ABL"])
        out["delta_joint_vs_fair_second"] = _ci_pack(ds["DENSE-SUB-ABL-GATED-FAIR"])

    def _favors_kg(ci):
        return bool(ci is not None and ci["excl_0"] and ci["diff"] > 0)
    kg_beats_ungated = _favors_kg(dp["DENSE-SUB-ABL"]) and (ds is None or _favors_kg(ds["DENSE-SUB-ABL"]))
    kg_beats_fair = _favors_kg(dp["DENSE-SUB-ABL-GATED-FAIR"]) and (ds is None or _favors_kg(ds["DENSE-SUB-ABL-GATED-FAIR"]))
    out["kg_beats_ungated"] = bool(kg_beats_ungated)
    out["kg_beats_fair"] = bool(kg_beats_fair)
    concentrated_win = bool(meaningful_forget and kg_beats_fair)
    out["concentrated_win"] = concentrated_win
    out["status"] = ("concentrated_win" if concentrated_win else
                     ("meaningful_no_win" if meaningful_forget else "no_meaningful_forget"))
    logger.info(f"{el()} EDIT {token}: status={out['status']} mf={meaningful_forget} "
                f"kg_beats_fair={kg_beats_fair} dJ_fair_p={out.get('delta_joint_vs_fair_primary')}")
    return out, preds


# ============================================================================= STEP H: population predictor
def _spearman_ci(x, y, B=2000):
    from scipy.stats import spearmanr
    x = np.asarray(x, float); y = np.asarray(y, float)
    n = len(x)
    if n < 4:
        return {"rho": None, "ci_lo": None, "ci_hi": None, "n": int(n), "excl_0": False}
    rho = float(spearmanr(x, y).correlation)
    bs = []
    for _ in range(B):
        idx = rng.integers(0, n, n)
        if len(np.unique(x[idx])) < 2 or len(np.unique(y[idx])) < 2:
            continue
        bs.append(float(spearmanr(x[idx], y[idx]).correlation))
    if not bs:
        return {"rho": rho, "ci_lo": None, "ci_hi": None, "n": int(n), "excl_0": False}
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return {"rho": round(rho, 4), "ci_lo": round(float(lo), 4), "ci_hi": round(float(hi), 4),
            "n": int(n), "excl_0": bool(lo > 0 or hi < 0)}


def _pointbiserial_ci(binary, cont, B=2000):
    """Correlation between a binary var and a continuous var (point-biserial = Pearson)."""
    b = np.asarray(binary, float); c = np.asarray(cont, float)
    n = len(b)
    if n < 4 or len(np.unique(b)) < 2:
        return {"r": None, "ci_lo": None, "ci_hi": None, "n": int(n), "excl_0": False}
    def _r(bb, cc):
        if len(np.unique(bb)) < 2 or np.std(cc) < 1e-9:
            return 0.0
        return float(np.corrcoef(bb, cc)[0, 1])
    r = _r(b, c)
    bs = []
    for _ in range(B):
        idx = rng.integers(0, n, n)
        bs.append(_r(b[idx], c[idx]))
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return {"r": round(r, 4), "ci_lo": round(float(lo), 4), "ci_hi": round(float(hi), 4),
            "n": int(n), "excl_0": bool(lo > 0 or hi < 0)}


def population_predictor(edited):
    """C=concentration (continuous), S=absorption_structured (binary). Outcomes Ymag=delta_joint(KG vs fair)
    diff (continuous), Ywin=concentrated_win (binary). Decide CONCENTRATION_PREDICTS vs ABSORPTION_PREDICTS."""
    rows = [e for e in edited if e.get("delta_joint_vs_fair_primary") is not None]
    if len(rows) < 4:
        return {"predictor_verdict": "TIE/UNDERPOWERED", "n": len(rows),
                "note": "fewer than 4 edited candidates with a Delta_joint; cannot identify the contrast"}
    C = [e["concentration_score"] for e in rows]
    S = [1.0 if e["absorption_structured"] else 0.0 for e in rows]
    Ymag = [e["delta_joint_vs_fair_primary"]["diff"] for e in rows]
    Ywin = [1.0 if e.get("concentrated_win") else 0.0 for e in rows]
    res = {
        "n": len(rows),
        "spearman_conc_mag": _spearman_ci(C, Ymag),
        "pb_conc_win": _pointbiserial_ci(Ywin, C),
        "pb_absorp_mag": _pointbiserial_ci(S, Ymag),
        "pb_absorp_win": _pointbiserial_ci(S, Ywin),
    }
    conc_sig = res["spearman_conc_mag"]["excl_0"] or res["pb_conc_win"]["excl_0"]
    absorp_sig = res["pb_absorp_mag"]["excl_0"] or res["pb_absorp_win"]["excl_0"]
    if conc_sig and not absorp_sig:
        res["predictor_verdict"] = "CONCENTRATION_PREDICTS"
    elif absorp_sig and not conc_sig:
        res["predictor_verdict"] = "ABSORPTION_PREDICTS"
    else:
        res["predictor_verdict"] = "TIE/UNDERPOWERED"
    return res


# ============================================================================= gating
def gating_check(mb, sae):
    tax_rows = load_taxonomic()
    gate_rows = [_attach_span_tax(dict(r)) for r in tax_rows if r["metadata_row_type"] == "corpus"][:64]
    layer_idx, fvu = mb.determine_layer_idx(gate_rows, sae)
    _, resid_g, align_g = mb.encode_rows(gate_rows, sae)
    torch = mb.torch
    hb = torch.tensor(resid_g.astype(np.float32), device=DEVICE)
    z = sae.encode(hb); hr = sae.decode(z)
    cos = float(torch.nn.functional.cosine_similarity(hb, hr, dim=-1).mean())
    l0 = float((z > 0).sum(1).float().mean())
    gating = {"pass": bool(cos > 0.9), "cosine": round(cos, 4), "L0": round(l0, 1),
              "align": round(float(align_g), 4), "layer_idx": int(layer_idx),
              "fvu_by_idx": {str(k): round(float(v), 4) for k, v in fvu.items()}}
    logger.info(f"{el()} GATING cosine={cos:.4f} L0={l0:.1f} layer_idx={layer_idx}")
    assert cos > 0.85, f"gating cosine {cos:.4f} too low"
    del hb, z, hr, resid_g; gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return gating


# ============================================================================= output assembly
def _human_desc(scr):
    return (f"Candidate '{scr['token']}' ({scr['hierarchy']}): concentration={scr['concentration_score']}, "
            f"precision={scr['precision']}, footprint={scr['footprint']}, recall_hole={scr['recall_hole']}, "
            f"absorber={scr['absorber']}, max_prec={scr['max_prec_latent']}, "
            f"set_cover_eq={scr['set_cover_eq_max_precision']}, absorption_structured={scr['absorption_structured']}")


def _screen_example(scr, edit=None):
    """One concentration_screen dataset row (carries the 5 predict_* keys as STRINGS per validator)."""
    e = edit or {}
    status = e.get("status", "screen_only")
    ex = {
        "input": _human_desc(scr),
        "output": status,
        "predict_kg_abl": "NA", "predict_dense_sub_abl": "NA", "predict_dense_sub_gated_fair": "NA",
        "predict_max_precision": "NA", "predict_noop": "NA",
        "metadata_token": scr["token"], "metadata_hierarchy": scr["hierarchy"],
        "metadata_family": scr["family"], "metadata_parent": scr["parent"],
        "metadata_n_x": scr["n_x"], "metadata_n_sib": scr["n_sib"], "metadata_anchor": scr["anchor"],
        "metadata_precision": scr["precision"], "metadata_footprint": scr["footprint"],
        "metadata_concentration_score": scr["concentration_score"], "metadata_recall_hole": scr["recall_hole"],
        "metadata_firing_jaccard": scr["firing_jaccard"], "metadata_absorber": scr["absorber"],
        "metadata_max_prec_latent": scr["max_prec_latent"],
        "metadata_set_cover_eq_max_precision": scr["set_cover_eq_max_precision"],
        "metadata_absorption_structured": scr["absorption_structured"],
        "metadata_structure_absent": scr["structure_absent"],
        "metadata_meaningful_forget": e.get("meaningful_forget"),
        "metadata_kg_beats_ungated": e.get("kg_beats_ungated"),
        "metadata_kg_beats_fair": e.get("kg_beats_fair"),
        "metadata_fair_saturated": e.get("fair_saturated"),
        "metadata_kg_max_subdrop": e.get("kg_max_subdrop"),
        "metadata_completion_drop_kg": e.get("completion_drop_kg"),
        "metadata_u_sub_auc": e.get("u_sub_auc"), "metadata_d_sub_auc": e.get("d_sub_auc"),
        "metadata_delta_joint_vs_fair_primary": json.dumps(e.get("delta_joint_vs_fair_primary")),
        "metadata_delta_joint_vs_fair_second": json.dumps(e.get("delta_joint_vs_fair_second")),
        "metadata_delta_joint_vs_ungated_primary": json.dumps(e.get("delta_joint_vs_ungated_primary")),
    }
    # set predict_* to the relevant op tag (string) so each example carries them meaningfully
    if status in ("concentrated_win", "meaningful_no_win", "no_meaningful_forget"):
        ex["predict_kg_abl"] = "KG-ABL"; ex["predict_dense_sub_abl"] = "DENSE-SUB-ABL"
        ex["predict_dense_sub_gated_fair"] = "DENSE-SUB-ABL-GATED-FAIR"
        ex["predict_max_precision"] = ("MAX-PREC-ABL" if scr["max_prec_latent"] is not None else "NA")
        ex["predict_noop"] = "NOOP"
    return ex


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--unit", action="store_true")
    ap.add_argument("--mini", action="store_true")
    ap.add_argument("--cap", type=int, default=None)
    ap.add_argument("--max_edit", type=int, default=EDIT_TOPK)
    ap.add_argument("--families", default="spelling,taxonomic,homograph")
    ap.add_argument("--no_judge", action="store_true")
    args = ap.parse_args()

    set_limits()
    t0 = time.time()
    logger.info(f"{el()} ===== iter-8 M2'''+M3''' base-widener / concentration-vs-absorption =====")
    torch = __import__("torch")
    sae = load_sae(torch)
    mb = ModelBundle(torch)
    gating = gating_check(mb, sae)
    W_dec_np = sae.W_dec.detach().cpu().numpy().astype(np.float32)

    kg = json.loads(KG4.read_text())["metadata"]["canonical_units"]
    spell_anchors = {lt: int(kg["first_letter"][lt]["anchor"]) for lt in ("L", "O", "T", "I", "D")}
    tax_anchor = int(kg["taxonomic"]["anchor"])

    fam_sel = set(args.families.split(","))
    cap = args.cap
    if args.smoke:
        fam_sel = {"spelling", "taxonomic"}; cap = cap or 20
    families = []
    if "spelling" in fam_sel:
        letters = ("L",) if args.smoke else ("L", "O", "T", "I", "D")
        families.append(build_spelling(mb, sae, spell_anchors, cap=cap, letters=letters))
    if "taxonomic" in fam_sel:
        families.append(build_taxonomic(mb, sae, tax_anchor, cap=cap))
    if "homograph" in fam_sel and not args.smoke:
        families.extend(build_homograph(mb, sae, cap=cap))

    # neutral footprint pool: NEUTRAL_TEXT + broad sample of corpus windows across families (true background)
    neut_texts = list(NEUTRAL_TEXT)
    for fam in families:
        idx = rng.choice(len(fam.enc_rows), min(300, len(fam.enc_rows)), replace=False)
        neut_texts += [fam.enc_rows[i]["input"] for i in idx]
    neutral_foot, n_neut_tok = compute_neutral_footprint(mb, sae, neut_texts)

    # ---- candidate pool + concentration screen ($0) ----
    screen_rows = []
    for fam in families:
        fam._cand_info = _family_candidates(fam)
        # restrict pool: curated + KG4 (spelling) / curated + eligible (homograph) / all (taxonomic)
        if fam.kind == "spelling":
            allow = set()
            for lt in spell_anchors:
                allow |= set(CURATED_SPELLING.get(lt, []))
                for la, w in kg["first_letter"][lt].get("sub_by_absorber", {}).items():
                    if w:
                        allow.add(w)
            cand_tokens = [t for t in fam._cand_info if t in allow]
        elif fam.kind == "homograph":
            ready_h = (fam.readiness.get(fam.hier, {}) if isinstance(fam.readiness, dict) else {})
            curated = set(CURATED_HG.get(fam.hier, []))
            cand_tokens = []
            for t in fam._cand_info:
                rd = ready_h.get(t, {}) if isinstance(ready_h, dict) else {}
                dp = rd.get("diagnostic_positives", 0)
                if t in curated or rd.get("status") == "eligible" or dp >= 120:
                    cand_tokens.append(t)
            if not cand_tokens:   # readiness keys may differ -> fall back to any with enough windows
                cand_tokens = list(fam._cand_info.keys())
        else:
            cand_tokens = list(fam._cand_info.keys())
        for t in cand_tokens:
            scr = screen_candidate(fam, t, fam._cand_info[t], neutral_foot, W_dec_np)
            scr["_fam"] = fam.name
            scr["uid"] = f"{fam.name}::{t}"   # unique id (token 'Jordan' exists as both city & country)
            screen_rows.append(scr)
        logger.info(f"{el()} [{fam.name}] screened {len(cand_tokens)} candidates")

    # rank by concentration
    screen_rows.sort(key=lambda r: r["concentration_score"], reverse=True)
    fam_by_name = {f.name: f for f in families}
    logger.info(f"{el()} TOTAL screened candidates: {len(screen_rows)}")
    for r in screen_rows[:20]:
        logger.info(f"    {r['token']:>14} {r['hierarchy']:>22} conc={r['concentration_score']:.3f} "
                    f"prec={r['precision']:.2f} foot={r['footprint']:.4f} absorb_struct={r['absorption_structured']} "
                    f"set_cover_eq={r['set_cover_eq_max_precision']}")

    # ---- edit set selection (by UNIQUE uid: token 'Jordan' is both a city-homograph and a country) ----
    by_uid = {r["uid"]: r for r in screen_rows}
    curated_hg_tokens = set(t for v in CURATED_HG.values() for t in v)
    forced_tokens = (POSITIVE_CONTROLS | DISTRIBUTED_ANCHORS | curated_hg_tokens |
                     {"Amazon", "Bush", "Cook", "Paris", "Phoenix", "Jackson"})  # reviewer-named + eligible homograph
    # guarantee homograph breadth in the population test even if their capture-concentration is mid-ranked
    # LOAD-BEARING priority first: the iter-7 anchors in their CANONICAL family, then most-concentrated breadth,
    # then remaining plan-named confirmatory anchors -- the budget fallback must never drop these.
    priority_specs = [("first_letter_spelling", "large"), ("taxonomic_country", "Georgia"),
                      ("taxonomic_country", "Jordan")]
    priority = [f"{fam}::{tok}" for fam, tok in priority_specs if f"{fam}::{tok}" in by_uid]
    topk = [r["uid"] for r in screen_rows[:args.max_edit]]
    other_forced = [r["uid"] for r in screen_rows if r["token"] in forced_tokens]
    edit_order = priority + topk + other_forced
    # dedupe preserving order
    seen = set(); edit_order = [u for u in edit_order if not (u in seen or seen.add(u))]

    if args.smoke or args.no_judge:
        judges = (None, None)
    else:
        judges = (PRIMARY_JUDGE, resolve_second_judge())
    prompt_caps = ({"forget": N_FORGET_MINI, "retain": N_RETAIN_MINI, "unrel": N_UNREL_MINI}
                   if (args.mini or args.smoke) else
                   {"forget": N_FORGET, "retain": N_RETAIN, "unrel": N_UNREL})

    # ---- edit loop (budget-bounded, breadth-first) ----
    edited = {}; pred_rows = []
    n_edit_target = (2 if args.smoke else (5 if args.mini else min(len(edit_order), 36)))
    for ti, uid in enumerate(edit_order):
        if ti >= n_edit_target:
            break
        scr = by_uid.get(uid)
        if scr is None:
            continue
        token = scr["token"]; fam = fam_by_name.get(scr["_fam"])
        budget_left = SPENT["usd"] < TARGET
        if not budget_left and judges[0] is not None:
            logger.info(f"{el()} BUDGET reached (${SPENT['usd']:.2f}) -> remaining candidates screen-only")
            scr_e = dict(scr); scr_e["status"] = "budget_skipped"; edited[uid] = scr_e
            continue
        logger.info(f"{el()} === EDIT {ti+1}/{n_edit_target}: {uid} (conc={scr['concentration_score']:.3f}) "
                    f"spent=${SPENT['usd']:.3f} ===")
        try:
            e, preds = edit_candidate(mb, sae, fam, scr, judges, prompt_caps)
        except Exception as ex:  # noqa: BLE001
            logger.exception(f"edit failed for {uid}: {ex}")
            e = dict(scr); e["status"] = "edit_error"; e["error"] = repr(ex)[:200]; preds = []
        edited[uid] = e; pred_rows.extend(preds)
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    # ---- verdict (M2''' base count) ----
    edited_list = list(edited.values())
    new_wins = sorted({e["token"] for e in edited_list
                       if e.get("concentrated_win") and e["token"] not in POSITIVE_CONTROLS})
    known_wins = sorted({e["token"] for e in edited_list
                         if e.get("concentrated_win") and e["token"] in POSITIVE_CONTROLS})
    total_wins = len(set(known_wins) | set(new_wins))
    verdict = "BASE_REACHES_4_PLUS" if total_wins >= 4 else "BASE_STAYS_THIN_RETARGET"

    # positive-control reproduction check (look up by token across uids)
    pc_repro = {}
    for pc in POSITIVE_CONTROLS:
        hit = next((e for e in edited_list if e.get("token") == pc), None)
        if hit is not None:
            pc_repro[pc] = bool(hit.get("kg_beats_fair"))

    # ---- population predictor (M3''') ----
    pop = population_predictor(edited_list)

    # ---- set-cover inertness (M5''') over ALL screened candidates with an absorber ----
    with_abs = [r for r in screen_rows if r["absorber"] is not None]
    set_cover_inert = (float(np.mean([1.0 if r["set_cover_eq_max_precision"] else 0.0 for r in with_abs]))
                       if with_abs else None)

    # ---- honest negatives ----
    honest = []
    if total_wins < 4:
        honest.append(f"BASE_STAYS_THIN: only {total_wins} independent concentrated win(s) "
                      f"({sorted(set(known_wins)|set(new_wins))}) cleared the fair bar -> paper retargets to "
                      f"localization+editing of homograph-polysemy/spelling absorption.")
    if set_cover_inert is not None and set_cover_inert >= 0.5:
        honest.append(f"SET-COVER INERT: anchored absorber == unconstrained max-precision latent for "
                      f"{set_cover_inert:.0%} of candidates with a structure -> the K-track set-cover step is "
                      f"largely inert; the method reduces to precise-latent discovery.")
    if pop.get("predictor_verdict") != "CONCENTRATION_PREDICTS":
        honest.append(f"PREDICTOR: concentration does NOT out-predict absorption-structure "
                      f"(verdict={pop.get('predictor_verdict')}, n={pop.get('n')}) -> reframe unsupported / "
                      f"underpowered; reported as-is with CIs.")
    no_mf = [e["token"] for e in edited_list if e.get("status") == "no_meaningful_forget"]
    if no_mf:
        honest.append(f"NO_MEANINGFUL_FORGET candidates (single-latent ablation can't forget at full strength): "
                      f"{sorted(no_mf)} -- carries the iter-7 Georgia/Jordan distributed-sense finding.")
    if any(e.get("fair_saturated") for e in edited_list):
        sat = [e["token"] for e in edited_list if e.get("fair_saturated")]
        honest.append(f"FAIR-GATED SATURATES below meaningful forget at beta<=1 for {sorted(sat)} -> KG wins on "
                      f"forget by construction there; joint compared at the common achievable forget.")
    honest.append("PLAN-NAMED 'Amazon known win' was NOT established by iter-7 (iter-7 ran no homograph case); "
                  "Amazon/Bush/Cook are evaluated FRESH here, never pre-counted as load-bearing wins.")
    honest.append("Fair-gated control uses the SAME labeled u_sub + a precise d_sub gate: where it MATCHES KG, "
                  "the value is label-free WHERE-to-gate discovery (gating is prior art CAST/GSS/GUARD-IT/SADI), "
                  "not SAE magic.")
    if not HG_FULL.exists():
        honest.append("HOMOGRAPH dataset not shipped on disk -> rebuilt from iter-5 builder; if rebuild failed, "
                      "base-widener ran on spelling words alone (fallback).")

    # ---- assemble ----
    meta = {
        "method_name": "Base-Widener + Concentration-vs-Absorption Population Test (iter-8 M2'''/M3'''/M5''')",
        "description": ("Screen a wide vocabulary (spelling L/O/T/I/D word-absorbers + homograph entities) for "
                        "lexical CONCENTRATION (precision x sparse footprint), then run the UNIFIED fair gated "
                        "edit (DENSE-SUB-ABL-GATED-FAIR: u_sub gated by precise d_sub, bounded beta<=1) on the "
                        "most-concentrated candidates; count independent concentrated wins, test whether "
                        "continuous concentration out-predicts the binary absorption label, and whether the "
                        "anchored absorber equals the unconstrained max-precision latent."),
        "sae": {"release": "google/gemma-scope-2b-pt-res", "sae_params": "layer_12/width_16k/average_l0_82",
                "width": 16384, "d_model": D_MODEL, "hook": "blocks.12.hook_resid_post"},
        "model": mb.model_id, "seed": SEED, "B_boot": B_BOOT,
        "gating_check": gating,
        "forget_grids": {"LAM_GRID": LAM_GRID, "BETA_GRID": BETA_GRID, "FAIR_BETA_GRID": FAIR_BETA_GRID,
                         "FORGET_FLOOR": FORGET_FLOOR, "MIN_SUB": MIN_SUB},
        "fair_gate_spec": {"operator": "erase_dir_gated_fair", "beta_cap": 1.0, "gate_thresh_primary": 0.0,
                           "gate_uses": "precise supervised d_sub logit (h@w_sub + b_sub) > 0",
                           "rationale": "labeled u_sub + precise d_sub where-to-edit, no over-erasure (beta<=1)"},
        "neutral_footprint_tokens": int(n_neut_tok),
        "judge": {"models": [PRIMARY_JUDGE["model"], (judges[1]["model"] if judges[1] else None)],
                  "target_usd": TARGET, "hard_cap": HARD_CAP, "spent_usd": round(SPENT["usd"], 4),
                  "calls": SPENT["calls"], "per_judge": PER_JUDGE},
        "concentration_screen_table": [{k: v for k, v in r.items() if not k.startswith("_")} for r in screen_rows],
        "base_count": {"known_wins": known_wins, "new_wins": new_wins,
                       "total_independent_concentrated_wins": total_wins, "verdict": verdict,
                       "positive_control_reproduces": pc_repro},
        "population_predictor": pop,
        "set_cover_inertness_rate": (round(set_cover_inert, 4) if set_cover_inert is not None else None),
        "set_cover_n_with_absorber": len(with_abs),
        "edit_results": {t: {k: v for k, v in e.items() if not k.startswith("_")} for t, e in edited.items()},
        "honest_negatives": honest,
        "config": {"edit_topk": args.max_edit, "prompt_caps": prompt_caps, "smoke": args.smoke,
                   "mini": args.mini, "families": sorted(fam_sel), "n_edited": len(edited)},
        "runtime_sec": round(time.time() - t0, 1),
    }

    screen_examples = [_screen_example(r, edited.get(r["uid"])) for r in screen_rows]
    if not pred_rows:
        pred_rows = [{"input": "no edits performed (screen-only run)", "output": "none",
                      "predict_kg_abl": "NA", "predict_dense_sub_abl": "NA",
                      "predict_dense_sub_gated_fair": "NA", "predict_max_precision": "NA", "predict_noop": "NA",
                      "metadata_note": "no judged edits in this run"}]
    out = {"metadata": meta, "datasets": [
        {"dataset": "concentration_screen", "examples": screen_examples},
        {"dataset": "edit_predictions", "examples": pred_rows},
    ]}
    save_json(out, WORK / "method_out.json")
    logger.info(f"{el()} verdict={verdict} total_wins={total_wins} predictor={pop.get('predictor_verdict')} "
                f"set_cover_inert={set_cover_inert} spent=${SPENT['usd']:.3f} runtime={time.time()-t0:.0f}s")
    print(json.dumps({"verdict": verdict, "total_wins": total_wins, "known": known_wins, "new": new_wins,
                      "predictor": pop.get("predictor_verdict"), "set_cover_inert": set_cover_inert,
                      "n_screened": len(screen_rows), "n_edited": len(edited),
                      "spent_usd": round(SPENT["usd"], 4)}, indent=1))


def screen_rows_token_order(screen_rows, forced):
    """tokens in `forced` that exist in the screen, ordered by concentration desc."""
    present = [r["token"] for r in screen_rows if r["token"] in forced]
    return present


if __name__ == "__main__":
    main()
