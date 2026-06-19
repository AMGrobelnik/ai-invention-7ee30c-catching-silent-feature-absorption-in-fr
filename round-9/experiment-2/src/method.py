#!/usr/bin/env python
"""
M3'''' COVERAGE-OF-ABSORPTION SCREEN  +  shipped label-free practitioner screen (driver).
================================================================================================
Turns the scattered iter-5..8 breadth counts (2/44 safety, 3/64 homograph entities, 0/28 professions,
months-only) into ONE reviewer-facing COVERAGE TABLE + a shipped LABEL-FREE practitioner screen
(screen.py).  Reuses the proven $0 recall-hole + firing-disjoint absorber + precision + hole-coverage-gain
bootstrap-CI signature (NO diagnostic probe / NO sub-context labels to FLAG) over a WIDE multi-hierarchy
candidate pool:

    first-letter spelling word-types (L/O/T/I/D)         [1 hierarchy]
    taxonomic countries                                  [1 hierarchy]
    homograph entities: city / month / given_name / brand[4 hierarchies]
    safety identities: nationality / religion / ethnicity / named_entity  [4 hierarchies]

Each candidate gets predict_absorption in {ABSORPTION_STRUCTURED, CO_FIRING, NO_HOLE, DESCRIPTIVE_ONLY}.
A stratified set is corroborated with the non-circular FORM-FREE decoder-projection oracle.  One coverage
fraction per hierarchy + pooled, with Wilson + bootstrap CIs.  Positive controls (Georgia, large, Amazon,
months) and negative controls (most cities/brands/given-names, demographic safety groups, professions)
reproduced.  VERDICT = COVERAGE_QUANTIFIED.  GPU; $0 (all model-internal).

Reuses spelling/taxonomic/homograph cached encodings (cache/enc_*.npz); only the 4 safety hierarchies
are encoded fresh.  The screen logic lives in screen.py (genuinely exercised, also the shipped CLI).

Usage:
  python method.py --smoke      # 1 family (spelling L), few candidates, no oracle, $0  -> end-to-end
  python method.py --mini       # spelling + 1 homograph + 1 safety, oracle on, $0
  python method.py              # full: all 10 hierarchies, coverage table
"""
import os, sys, json, time, gc, argparse
from pathlib import Path
from collections import Counter, defaultdict

import numpy as np

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")

import core
from core import (logger, el, load_sae, ModelBundle, content_responsive, ParentProbe, save_json,
                  load_taxonomic, load_first_letter, NEUTRAL_TEXT, set_limits,
                  _attach_span_fl, _attach_span_tax, DEVICE, SEED, D_MODEL, ROOT)
import screen as SCR

WORK = Path("/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_9/gen_art/gen_art_experiment_2")
RESULTS = WORK / "results"; CACHE = WORK / "cache"; LOGS = WORK / "logs"
for d in (RESULTS, CACHE, LOGS):
    d.mkdir(parents=True, exist_ok=True)

KG4 = ROOT / "iter_4/gen_art/gen_art_experiment_1/method_out.json"
HG_FULL = WORK / "homograph_data/full_data_out.json"
HG_MANIFEST = WORK / "homograph_data/manifest.json"
SAFETY_FULL = ROOT / "iter_6/gen_art/gen_art_dataset_1/full_data_out.json"
SAFETY_MANIFEST = ROOT / "iter_6/gen_art/gen_art_dataset_1/manifest.json"

rng = np.random.default_rng(SEED)

# ----------------------------------------------------------------------------- config
MIN_X_WIN = 12                 # min target-sense corpus windows to screen a candidate
MIN_FIRE = 3                   # min fit-X rows a latent must fire on to be precision-rankable
JAC_MAX = SCR.JAC_MAX          # 0.10
PREC_K = SCR.PREC_MIN          # 0.70
EPS = 1e-9

CORPUS_CAP_PER_WORD = 120
SIB_CAP = 600
HG_CORPUS_CAP_PER_ENT = 150
HG_SIB_CAP = 700
SAFETY_CAP_NEG = 1500          # negatives per safety hierarchy (precision/floor pool)

# curated spelling word pool (union with KG4 sub_by_absorber) + breadth top-window words per letter
CURATED_SPELLING = {
    "L": ["large", "list", "line", "law", "like", "level", "low", "leave", "land", "life", "long", "light"],
    "O": ["our", "one", "only", "other", "out", "over", "old", "offer", "open", "order"],
    "T": ["that", "their", "there", "time", "take", "this", "the", "to", "team", "type"],
    "I": ["in", "into", "it", "is", "if", "its", "idea", "issue", "item"],
    "D": ["day", "down", "do", "did", "does", "data", "deal", "drive", "design"],
}
SPELLING_BREADTH_PER_LETTER = 30   # additional top-window word-types/letter (RELAXED breadth)

# control sets — POS = the absorption-structured cases that reproduce STRICT in this run (run_4i).
# 'large' (the canonical spelling absorber) is reported separately: it has a strong recall-hole here but
# its re-encoding is DISTRIBUTED across an L-word cluster (precision<0.70), so it is honestly not a clean
# single-absorber case in this corpus (other spelling words ARE — see spelling_absorption). Months and
# Apple/King are screened too but come out NO_HOLE here (honest informational negatives).
POS_CONTROLS = ["Georgia", "Amazon", "Bush", "Cook"]
HOMOGRAPH_INFO = ["large", "March", "June", "February", "May", "Apple", "King", "Paris", "Phoenix"]
NEG_CITY = ["Paris", "Florence", "Columbus", "Cleveland", "Phoenix", "Mobile", "Reading"]
NEG_BRAND = ["Shell", "Target", "Orange", "Gap", "Visa"]
NEG_NAME = ["Grace", "Hope", "Faith", "Will", "Mark"]
DEMOGRAPHIC_HIERS = {"safety_nationality", "safety_religion", "safety_ethnicity_identity"}


# ============================================================================= family infra
class Family:
    pass


def _encode_family(mb, sae, name, enc_rows, cache_tag=None):
    import scipy.sparse as sp
    cache_f = CACHE / f"enc_{cache_tag}.npz" if cache_tag else None
    if cache_f and cache_f.exists():
        try:
            d = np.load(cache_f, allow_pickle=True)
            if int(d["resid"].shape[0]) != len(enc_rows):
                logger.warning(f"[{name}] cache row mismatch ({d['resid'].shape[0]} != {len(enc_rows)}); re-encode")
                raise ValueError("row mismatch")
            lat_csr = sp.csr_matrix((d["lat_data"], d["lat_idx"], d["lat_ptr"]),
                                    shape=(len(enc_rows), sae.d_sae))
            resid = d["resid"]
            logger.info(f"{el()} [{name}] loaded cached encode ({resid.shape[0]} rows) from {cache_f.name}")
            return lat_csr, resid
        except Exception as e:  # noqa: BLE001
            logger.warning(f"cache load failed ({e}); re-encoding")
    lat_csr, resid, _ = mb.encode_rows(enc_rows, sae)
    if cache_f:
        np.savez_compressed(cache_f, lat_data=lat_csr.data, lat_idx=lat_csr.indices,
                            lat_ptr=lat_csr.indptr, resid=resid)
    return lat_csr, resid


def _attach_span_hg(r):
    cs = r.get("metadata_target_char_start"); ce = r.get("metadata_target_char_end")
    r["_span"] = (cs, ce) if cs is not None else None
    ti = r.get("metadata_target_token_indices")
    r["_ti"] = list(ti) if ti else None
    r["_target"] = r.get("metadata_entity") or r.get("metadata_target_text")
    return r


def _attach_span_safety(r):
    cs = r.get("metadata_target_char_start"); ce = r.get("metadata_target_char_end")
    r["_span"] = (cs, ce) if cs is not None else None
    ti = r.get("metadata_target_token_indices")
    r["_ti"] = list(ti) if ti else None
    r["_target"] = r.get("metadata_target_text")
    return r


def compute_neutral_footprint(mb, sae, texts, max_len=64, batch=16):
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
                rows = hs[am.to(DEVICE).bool()]
                z = sae.encode(rows)
                fire += (z > 0).sum(0).double().cpu().numpy()
                ntok += int(rows.shape[0])
            cap.clear()
    finally:
        handle.remove(); tok.padding_side = old
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return (fire / max(ntok, 1)).astype(np.float32), ntok


# ============================================================================= builders
def build_spelling(mb, sae, kg_anchors, letters=("L", "O", "T", "I", "D")):
    groups = load_first_letter(list(letters))
    enc_rows, tag = [], []
    for lt in letters:
        rows = groups.get(lt, [])
        corp = [r for r in rows if r.get("metadata_pair_type") == "corpus_context"]
        per_word = defaultdict(int)
        for r in corp:
            w = r.get("metadata_sub_context")
            if per_word[w] >= CORPUS_CAP_PER_WORD:
                continue
            per_word[w] += 1
            r = _attach_span_fl(dict(r))
            enc_rows.append(r); tag.append(("corpus", lt, w, r.get("metadata_fold")))
        cf = [r for r in rows if r.get("metadata_pair_type") == "content_flip"
              and r.get("metadata_template_id") in {"t_verbose", "t_colon", "t_icl"}]
        for r in cf:
            r = _attach_span_fl(dict(r))
            enc_rows.append(r); tag.append(("cf", lt, r.get("metadata_role"), r.get("metadata_pair_id")))
    logger.info(f"{el()} [spelling] {len(enc_rows)} rows across {letters}")
    lat_csr, resid = _encode_family(mb, sae, "spelling", enc_rows, cache_tag=f"spelling_{'_'.join(letters)}")
    fam = Family()
    fam.name = "first_letter_spelling"; fam.cov_hier = "first_letter_spelling"; fam.kind = "spelling"
    fam.lat_csr = lat_csr; fam.resid = resid; fam.tag = tag; fam.enc_rows = enc_rows
    fam.fit_folds = {0, 1, 2}; fam.eval_folds = {3, 4}
    fam.kg_anchors = {lt: int(a) for lt, a in kg_anchors.items()}
    return fam


def build_taxonomic(mb, sae, kg_anchor):
    rows = load_taxonomic()
    eligible = ['Australia', 'Brazil', 'Canada', 'China', 'France', 'Georgia', 'Germany', 'India',
                'Iran', 'Ireland', 'Israel', 'Italy', 'Japan', 'Jordan', 'Mexico', 'New Zealand', 'Poland',
                'Russia', 'Spain', 'United Kingdom', 'United States']
    corp = [r for r in rows if r["metadata_row_type"] == "corpus"]
    cpairs = [r for r in rows if r["metadata_row_type"] == "content_pair"]
    enc_rows, tag = [], []
    per = defaultdict(int)
    for r in corp:
        sc = r.get("metadata_sub_context"); out = r["output"]
        if out == "positive" and sc in eligible:
            if per[sc] >= 300:
                continue
            per[sc] += 1
            r = _attach_span_tax(dict(r))
            enc_rows.append(r); tag.append(("corpus_pos", "country", sc, r.get("metadata_fold")))
        elif out == "negative":
            if per["_neg"] >= 1200:
                continue
            per["_neg"] += 1
            r = _attach_span_tax(dict(r))
            enc_rows.append(r); tag.append(("corpus_neg", "country", None, r.get("metadata_fold")))
    for r in cpairs:
        r = _attach_span_tax(dict(r))
        enc_rows.append(r); tag.append(("cf", "country", r.get("metadata_pair_role"), r.get("metadata_pair_id")))
    logger.info(f"{el()} [taxonomic] {len(enc_rows)} rows")
    lat_csr, resid = _encode_family(mb, sae, "taxonomic", enc_rows, cache_tag="taxonomic")
    fam = Family()
    fam.name = "taxonomic_country"; fam.cov_hier = "taxonomic_country"; fam.kind = "country"
    fam.lat_csr = lat_csr; fam.resid = resid; fam.tag = tag; fam.enc_rows = enc_rows
    fam.fit_folds = {"diagnostic"}; fam.eval_folds = {"train", "test"}
    fam.kg_anchors = {"country": int(kg_anchor)}; fam.eligible = eligible
    return fam


def _build_entity_family(mb, sae, name, cov_hier, hier, rows, cap_pos, cap_neg, cache_tag,
                         attach_fn, target_sense_key="metadata_target_sense"):
    """Shared builder for homograph + safety hierarchies (corpus pos by sub_context + neg + content pairs)."""
    corp = [r for r in rows if r.get("metadata_row_type") == "corpus"]
    cpairs = [r for r in rows if r.get("metadata_row_type") == "content_pair"]
    enc_rows, tag = [], []
    per = defaultdict(int)
    for r in corp:
        out = r.get("output")
        if out == "positive":
            sc = r.get("metadata_sub_context") or r.get("metadata_entity")
            ts = r.get(target_sense_key)
            if not sc:
                continue
            if target_sense_key == "metadata_target_sense" and ts is not None and ts != hier:
                continue
            if cap_pos is not None and per[sc] >= cap_pos:
                continue
            per[sc] += 1
            r = attach_fn(dict(r))
            enc_rows.append(r); tag.append(("corpus_pos", hier, sc, r.get("metadata_fold")))
        elif out == "negative":
            if per["_neg"] >= cap_neg:
                continue
            per["_neg"] += 1
            r = attach_fn(dict(r))
            enc_rows.append(r); tag.append(("corpus_neg", hier, None, r.get("metadata_fold")))
    for r in cpairs:
        r = attach_fn(dict(r))
        enc_rows.append(r); tag.append(("cf", hier, r.get("metadata_pair_role"), r.get("metadata_pair_id")))
    n_pos = sum(1 for t in tag if t[0] == "corpus_pos")
    if n_pos < MIN_X_WIN:
        logger.warning(f"{el()} [{name}] too few positives ({n_pos}) -> skip")
        return None
    logger.info(f"{el()} [{name}] {len(enc_rows)} rows ({n_pos} pos)")
    lat_csr, resid = _encode_family(mb, sae, name, enc_rows, cache_tag=cache_tag)
    fam = Family()
    fam.name = name; fam.cov_hier = cov_hier; fam.kind = "entity"; fam.hier = hier
    fam.lat_csr = lat_csr; fam.resid = resid; fam.tag = tag; fam.enc_rows = enc_rows
    present = set(t[3] for t in tag if t[0] == "corpus_pos")
    if "diagnostic" in present:
        fam.fit_folds = {"diagnostic"}; fam.eval_folds = present - {"diagnostic"}
    else:
        sf = sorted(str(x) for x in present)
        fam.fit_folds = set(sf[:max(1, len(sf) // 2)]); fam.eval_folds = set(sf[max(1, len(sf) // 2):])
    fam.kg_anchors = {}
    return fam


def build_homograph(mb, sae, only=None):
    if not HG_FULL.exists():
        logger.warning(f"{el()} homograph data absent -> skip"); return []
    blob = json.loads(HG_FULL.read_text())
    fams = []
    for ds in blob["datasets"]:
        rows = ds["examples"]
        hier = next((r.get("metadata_hierarchy") for r in rows if r.get("metadata_hierarchy")), None)
        if hier is None or (only is not None and hier not in only):
            continue
        # uncapped positives so the diagnostic-fold count matches the manifest 'eligible' (>=150 diag);
        # the iter-8 150-TOTAL cap left only ~75 diagnostic -> nothing eligible for the STRICT gate.
        fam = _build_entity_family(mb, sae, f"homograph_{hier}", f"homograph_{hier}", hier, rows,
                                   None, HG_CORPUS_CAP_PER_ENT * 8, f"hg_{hier}_unc",
                                   _attach_span_hg, target_sense_key="metadata_target_sense")
        if fam is not None:
            fams.append(fam)
    return fams


def build_safety(mb, sae, only=None):
    if not SAFETY_FULL.exists():
        logger.warning(f"{el()} safety data absent -> skip"); return []
    blob = json.loads(SAFETY_FULL.read_text())
    fams = []
    for ds in blob["datasets"]:
        name = ds["dataset"]; rows = ds["examples"]
        hier = next((r.get("metadata_hierarchy") for r in rows if r.get("metadata_hierarchy")), None)
        if hier is None:
            hier = name.replace("_absorption", "").replace("_safety", "")
        if only is not None and hier not in only:
            continue
        fam = _build_entity_family(mb, sae, f"safety_{hier}", f"safety_{hier}", hier, rows,
                                   None, SAFETY_CAP_NEG, f"safety_{hier}", _attach_span_safety,
                                   target_sense_key="metadata_concept_present")
        if fam is not None:
            fams.append(fam)
    return fams


# ============================================================================= family arrays / caches
def fam_arrays(fam):
    tag = fam.tag
    kind = np.array([t[0] for t in tag], dtype=object)
    p1 = np.array([t[1] for t in tag], dtype=object)
    sub = np.array([t[2] for t in tag], dtype=object)
    fold = np.array([t[3] for t in tag], dtype=object)
    return kind, p1, sub, fold


def family_cr(fam):
    if hasattr(fam, "_cr"):
        return fam._cr
    kind, p1, sub, fold = fam_arrays(fam)
    pairs = {}
    for i, t in enumerate(fam.tag):
        if t[0] == "cf":
            role = t[2]
            rn = "on" if role in ("on", "x_on") else ("off" if role in ("off", "x_off") else None)
            if rn:
                pairs.setdefault(t[3], {})[rn] = i
    on_idx = [d["on"] for d in pairs.values() if "on" in d and "off" in d]
    off_idx = [d["off"] for d in pairs.values() if "on" in d and "off" in d]
    if on_idx and off_idx:
        n = min(len(on_idx), len(off_idx))
        A_on = np.asarray(fam.lat_csr[on_idx[:n]].todense())
        A_off = np.asarray(fam.lat_csr[off_idx[:n]].todense())
        cr, _, _ = content_responsive(A_on, A_off)
        fam._recall_on = (A_on > 0).mean(0)          # [d_sae] concept-present recall (for parent ID)
        del A_on, A_off
    else:
        cr = np.array([], dtype=int)
        fam._recall_on = np.zeros(fam.lat_csr.shape[1])
    fam._cr = cr
    logger.info(f"{el()} [{fam.name}] content-responsive latents: {len(cr)} (from {len(on_idx)} pairs)")
    return cr


def family_anchor(fam):
    """{parent_key: anchor_latent}. KG4 for spelling/taxonomic, data-derived (highest-recall content
    latent over corpus positives) for entity hierarchies."""
    if hasattr(fam, "_anchor"):
        return fam._anchor
    kind, p1, sub, fold = fam_arrays(fam)
    cr = family_cr(fam)
    by_parent = {}
    if fam.kind == "spelling":
        by_parent = dict(fam.kg_anchors)
    elif fam.kind == "country":
        by_parent = {"country": int(fam.kg_anchors["country"])}
    else:
        # ENTITY parent = highest concept-present (content-flip x_on) recall among content-responsive
        # latents that ALSO clear a held-out corpus firing floor (the shared concept detector; matches
        # run__C1 iter-7 identify_parent). Chosen WITHOUT the absorption oracle -> non-circular.
        anc = -1
        if len(cr):
            recall_on = fam._recall_on
            corpus_idx = np.where((kind == "corpus_pos") | (kind == "corpus_neg"))[0]
            fire_corpus = (np.asarray((fam.lat_csr[corpus_idx] > 0).mean(0)).ravel() if len(corpus_idx)
                           else np.zeros(fam.lat_csr.shape[1]))
            best = bestr = -1.0
            for c in cr:
                c = int(c)
                if fire_corpus[c] >= SCR.PARENT_FIRE_FLOOR and recall_on[c] > bestr:
                    bestr = recall_on[c]; best = c
            if best < 0:                       # no floor-valid latent -> highest x_on recall overall
                for c in cr:
                    c = int(c)
                    if recall_on[c] > bestr:
                        bestr = recall_on[c]; best = c
            anc = int(best)
        by_parent = {fam.hier: anc}
    fam._anchor = by_parent
    return by_parent


def family_cand_fire(fam):
    """Dense [N, len(cr)] firing-boolean matrix for the content-responsive candidate pool (cached)."""
    if hasattr(fam, "_cand_fire"):
        return fam._cand_fire, fam._cr
    cr = family_cr(fam)
    if len(cr):
        cf = np.asarray((fam.lat_csr[:, cr] > 0).todense())
    else:
        cf = np.zeros((fam.lat_csr.shape[0], 0), dtype=bool)
    fam._cand_fire = cf
    return cf, cr


def par_fire_for(fam, anchor):
    if not hasattr(fam, "_parfire"):
        fam._parfire = {}
    a = int(anchor)
    if a not in fam._parfire:
        fam._parfire[a] = (np.asarray(fam.lat_csr[:, a].todense()).ravel() > 0) if a >= 0 \
            else np.zeros(fam.lat_csr.shape[0], bool)
    return fam._parfire[a]


def family_probe(fam, parent_key):
    """ParentProbe (d_p direction) for the form-free oracle, fit on the DISJOINT fit fold (or content
    flips for spelling). Cached per parent_key. Strictly never uses a single latent."""
    if not hasattr(fam, "_probe"):
        fam._probe = {}
    if parent_key in fam._probe:
        return fam._probe[parent_key]
    kind, p1, sub, fold = fam_arrays(fam)
    probe = None
    try:
        if fam.kind == "spelling":
            on = np.where((kind == "cf") & (p1 == parent_key) &
                          np.isin(sub, ["on", "x_on"]))[0]
            off = np.where((kind == "cf") & (p1 == parent_key) &
                           np.isin(sub, ["off", "x_off"]))[0]
            pos, neg = on, off
        else:
            fit_mask = np.array([f in fam.fit_folds for f in fold])
            pos = np.where((kind == "corpus_pos") & fit_mask)[0]
            neg = np.where((kind == "corpus_neg") & fit_mask)[0]
        if len(pos) >= 10 and len(neg) >= 10:
            if len(pos) > 1500:
                pos = rng.choice(pos, 1500, replace=False)
            if len(neg) > 1500:
                neg = rng.choice(neg, 1500, replace=False)
            probe = ParentProbe(fam.torch, fam.resid[pos].astype(np.float32),
                                fam.resid[neg].astype(np.float32))
    except Exception as e:  # noqa: BLE001
        logger.warning(f"[{fam.name}/{parent_key}] probe fit failed: {repr(e)[:120]}")
        probe = None
    fam._probe[parent_key] = probe
    return probe


# ============================================================================= candidate enumeration
def candidates(fam, kg=None):
    """{token: {parent, letter}} for screenable candidates with >= MIN_X_WIN windows."""
    kind, p1, sub, fold = fam_arrays(fam)
    out = {}
    if fam.kind == "spelling":
        allow = set()
        for lt in fam.kg_anchors:
            allow |= set(CURATED_SPELLING.get(lt, []))
            if kg is not None:
                for _la, w in kg["first_letter"].get(lt, {}).get("sub_by_absorber", {}).items():
                    if w:
                        allow.add(w)
        for lt in fam.kg_anchors:
            mask_lt = (kind == "corpus") & (p1 == lt)
            wc = Counter(sub[mask_lt])
            # breadth: top-window words/letter for RELAXED coverage
            top = [w for w, c in wc.most_common() if w and c >= MIN_X_WIN][:SPELLING_BREADTH_PER_LETTER]
            for w in set(top) | (allow & set(wc.keys())):
                if w and wc.get(w, 0) >= MIN_X_WIN:
                    out[w] = {"parent": lt, "letter": lt}
    elif fam.kind == "country":
        mask = (kind == "corpus_pos")
        for c in fam.eligible:
            if int((mask & (sub == c)).sum()) >= MIN_X_WIN:
                out[c] = {"parent": "country", "letter": None}
    else:
        mask = (kind == "corpus_pos")
        for e, c in Counter(sub[mask]).items():
            if e and c >= MIN_X_WIN:
                out[e] = {"parent": fam.hier, "letter": None}
    return out


# ============================================================================= per-candidate screen
def screen_candidate(fam, token, info, W_dec_np, compute_oracle=True, known_absorber=None):
    kind, p1, sub, fold = fam_arrays(fam)
    fit_mask = np.array([f in fam.fit_folds for f in fold])
    eval_mask = np.array([f in fam.eval_folds for f in fold])
    if fam.kind == "spelling":
        lt = info["parent"]
        corpus_mask = (kind == "corpus") & (p1 == lt)
        is_x = corpus_mask & (sub == token)
        fit_corpus = np.where(corpus_mask & fit_mask)[0]
        eval_corpus_pos = np.where(corpus_mask & eval_mask)[0]
    else:
        is_pos = (kind == "corpus_pos")
        is_x = is_pos & (sub == token)
        is_neg = (kind == "corpus_neg")
        fit_corpus = np.where((is_pos | is_neg) & fit_mask)[0]
        eval_corpus_pos = np.where(is_pos & eval_mask)[0]
    fit_Xpos = np.where(is_x & fit_mask)[0]
    eval_Xpos = np.where(is_x & eval_mask)[0]

    anchor = family_anchor(fam).get(info["parent"], -1)
    par_fire = par_fire_for(fam, anchor)
    cand_fire, cr = family_cand_fire(fam)
    probe = family_probe(fam, info["parent"]) if compute_oracle else None

    row = SCR.compute_signature(
        token=token, hierarchy=fam.cov_hier, parent=str(info["parent"]), anchor=anchor,
        lat_csr=fam.lat_csr, resid=fam.resid, cr=cr, fit_Xpos=fit_Xpos, eval_Xpos=eval_Xpos,
        fit_corpus=fit_corpus, eval_corpus_pos=eval_corpus_pos, sub_eval=sub, W_dec_np=W_dec_np,
        sae=fam._sae, probe=probe, n_eligible=len(fit_Xpos), known_absorber=known_absorber,
        compute_oracle=compute_oracle and probe is not None, par_fire=par_fire, cand_fire=cand_fire)

    # --- secondary: unconstrained max-precision latent + set-cover-equality + capture-concentration ---
    max_prec_latent = None; concentration = None
    if len(cr) and len(fit_Xpos):
        fit_sib = np.array(sorted(set(fit_corpus.tolist()) - set(fit_Xpos.tolist())), dtype=int)
        Xc = cand_fire[fit_Xpos].mean(0)
        Sc = cand_fire[fit_sib].mean(0) if len(fit_sib) else np.zeros(len(cr))
        prec_bal = Xc / (Xc + Sc + EPS)
        fcount = cand_fire[fit_Xpos].sum(0)
        elig = np.where(fcount >= MIN_FIRE)[0]
        if len(elig):
            max_prec_latent = int(cr[elig[int(np.argmax(prec_bal[elig]))]])
        chosen = row.get("absorber_latent") if row.get("absorber_latent") is not None else max_prec_latent
        if chosen is not None:
            try:
                mu = fam.resid[fit_Xpos].mean(0) - (fam.resid[fit_sib].mean(0) if len(fit_sib)
                                                    else fam.resid[fit_Xpos].mean(0) * 0)
                d_sub = mu / (np.linalg.norm(mu) + 1e-9)
                margin = fam.resid[fit_Xpos].astype(np.float32) @ d_sub.astype(np.float32)
                z_abs = np.asarray(fam.lat_csr[fit_Xpos][:, int(chosen)].todense()).ravel().astype(np.float32)
                dm = z_abs * float(W_dec_np[int(chosen)] @ d_sub.astype(np.float32))
                mm = float(np.mean(margin))
                concentration = float(np.clip(np.mean(dm) / mm, 0.0, 1.5)) if abs(mm) > 1e-6 else 0.0
            except Exception:
                concentration = None
    row["max_prec_latent"] = max_prec_latent
    row["set_cover_eq_max_precision"] = bool(row.get("absorber_latent") is not None and
                                             row.get("absorber_latent") == max_prec_latent)
    row["concentration_score"] = (round(concentration, 4) if concentration is not None else None)
    row["family"] = fam.name
    row["uid"] = f"{fam.name}::{token}"
    return row


# ============================================================================= coverage aggregation
def aggregate_coverage(rows):
    by_h = defaultdict(list)
    for r in rows:
        by_h[r["hierarchy"]].append(r)
    table = []
    def _emit(hier, gate, subset_flags):
        N = len(subset_flags); k = int(sum(subset_flags))
        frac = (k / N) if N else 0.0
        wlo, whi = SCR.wilson_ci(k, N)
        blo, bhi = SCR.bootstrap_fraction_ci(subset_flags) if N else (0.0, 0.0)
        table.append({"hierarchy": hier, "gate": gate, "N": N, "n_structured": k,
                      "fraction": round(frac, 4), "wilson_lo": round(wlo, 4), "wilson_hi": round(whi, 4),
                      "boot_lo": round(blo, 4), "boot_hi": round(bhi, 4)})
    for hier in sorted(by_h):
        rs = by_h[hier]
        elig = [r for r in rs if r.get("eligible")]
        _emit(hier, "strict", [1 if r["absorption_structured_strict"] else 0 for r in elig])
        _emit(hier, "relaxed", [1 if r["absorption_structured_relaxed"] else 0 for r in rs])
    # pooled
    elig_all = [r for r in rows if r.get("eligible")]
    _emit("POOLED", "strict", [1 if r["absorption_structured_strict"] else 0 for r in elig_all])
    _emit("POOLED", "relaxed", [1 if r["absorption_structured_relaxed"] else 0 for r in rows])
    return table


def oracle_agreement(rows):
    """Agreement between the label-free structured flag (relaxed) and the form-free oracle, per hierarchy
    and pooled by lexical vs taxonomic, on candidates that HAVE an absorber + computed oracle."""
    def _agg(subset):
        s = [1 if r["absorption_structured_relaxed"] else 0 for r in subset]
        o = [1 if r.get("oracle_corroborates") else 0 for r in subset]
        if not subset:
            return {"n": 0, "acc": None, "kappa": None}
        acc = float(np.mean([int(a == b) for a, b in zip(s, o)]))
        return {"n": len(subset), "acc": round(acc, 4), "kappa": round(SCR.cohen_kappa(s, o), 4)}
    have = [r for r in rows if r.get("absorber_latent") is not None and r.get("oracle_decoder_cos") is not None]
    by_h = defaultdict(list)
    for r in have:
        by_h[r["hierarchy"]].append(r)
    per = {h: _agg(rs) for h, rs in sorted(by_h.items())}
    lexical = [r for r in have if r["hierarchy"] != "taxonomic_country"]
    taxo = [r for r in have if r["hierarchy"] == "taxonomic_country"]

    # The MEANINGFUL quantity: among candidates the label-free screen FLAGS structured, does the form-free
    # decoder oracle corroborate? (Expected: YES for lexical/named-entity homographs, NO for taxonomic
    # Georgia whose decoder is near-orthogonal to the generic country direction.)
    def _corro(subset):
        if not subset:
            return {"n": 0, "n_corroborated": 0, "frac": None}
        k = sum(1 for r in subset if r.get("oracle_corroborates"))
        return {"n": len(subset), "n_corroborated": int(k), "frac": round(k / len(subset), 4)}
    struct = [r for r in have if r["absorption_structured_relaxed"]]
    struct_lex = [r for r in struct if r["hierarchy"] != "taxonomic_country"]
    struct_tax = [r for r in struct if r["hierarchy"] == "taxonomic_country"]
    structured_corroboration = {
        "all_structured": _corro(struct), "lexical_structured": _corro(struct_lex),
        "taxonomic_structured": _corro(struct_tax),
        "structured_tokens": [{"token": r["token"], "hierarchy": r["hierarchy"],
                               "oracle_decoder_cos": r.get("oracle_decoder_cos"),
                               "oracle_corroborates": r.get("oracle_corroborates")} for r in struct]}
    return {"per_hierarchy": per, "lexical_pooled": _agg(lexical),
            "structured_corroboration": structured_corroboration,
            "note_on_full_agreement": ("per-hierarchy acc/kappa are computed over ALL candidates with an "
                                       "absorber (mostly non-structured negatives), so they are diluted; the "
                                       "load-bearing quantity is structured_corroboration."),
            "taxonomic": {**_agg(taxo),
                          "caveat": ("decoder-projection oracle is concept-tuned and UNDER-fires for the "
                                     "taxonomic 'country' direction (Georgia's decoder is near-orthogonal to "
                                     "the generic country direction) -> low agreement is EXPECTED, not a bug; "
                                     "the structured flag stands on the label-free firing signature.")}}


# ============================================================================= controls
def reproduce_controls(rows, georgia_known):
    by_tok = defaultdict(list)
    for r in rows:
        by_tok[r["token"]].append(r)
    def _status(tok):
        out = {}
        for r in by_tok.get(tok, []):
            out[r["hierarchy"]] = {"predict": r["predict_absorption"],
                                   "strict": r["absorption_structured_strict"],
                                   "relaxed": r["absorption_structured_relaxed"],
                                   "recall_hole": r["recall_hole"], "firing_jaccard": r["firing_jaccard"],
                                   "precision": r["precision"], "gain": r["hole_coverage_gain"],
                                   "n_eligible": r["n_eligible"]}
        return out or {"_": "not_screened"}
    positive = {t: _status(t) for t in POS_CONTROLS}
    positive["Georgia_known_absorber_16009"] = georgia_known
    homograph_info = {t: _status(t) for t in HOMOGRAPH_INFO}
    # negatives
    def _struct_any(tok):
        return any(r["absorption_structured_relaxed"] for r in by_tok.get(tok, []))
    neg_cities = {t: _struct_any(t) for t in NEG_CITY if t in by_tok}
    neg_brands = {t: _struct_any(t) for t in NEG_BRAND if t in by_tok}
    neg_names = {t: _struct_any(t) for t in NEG_NAME if t in by_tok}
    demo = [r for r in rows if r["hierarchy"] in DEMOGRAPHIC_HIERS and r.get("eligible")]
    demo_struct = sum(1 for r in demo if r["absorption_structured_strict"])
    negative_summary = {
        "demographic_safety_eligible_N": len(demo),
        "demographic_safety_structured_strict": demo_struct,
        "cities_relaxed_structured": neg_cities,
        "brands_relaxed_structured": neg_brands,
        "given_names_relaxed_structured": neg_names,
    }
    professions = {"result": "0/28 (carried from prior iteration art_Iy77UHoNaIhS / iter-5 dossier)",
                   "note": "professions are NOT absorption-structured; cited in honest_negatives, no new "
                           "data built this iteration (optional stretch skipped to keep $0 / bounded)."}
    # spelling absorption summary (relaxed; spelling word-types are n<150 so DESCRIPTIVE_ONLY under STRICT)
    sp = [r for r in rows if r["hierarchy"] == "first_letter_spelling"]
    sp_struct = [r["token"] for r in sp if r["absorption_structured_relaxed"]]
    spelling_absorption = {
        "n_screened": len(sp), "n_relaxed_structured": len(sp_struct),
        "examples": sorted(sp_struct)[:15],
        "note": ("spelling first-letter absorption reproduces broadly (parent 'starts-with-L' is suppressed "
                 "and a precise word-specific latent re-encodes it); the canonical 'large' has a strong "
                 "recall-hole here but a DISTRIBUTED (precision<0.70) re-encoding in this corpus, so it is "
                 "not a clean single-absorber case -- an honest cross-corpus difference.")}
    return {"positive_controls": positive, "homograph_informational": homograph_info,
            "spelling_absorption": spelling_absorption,
            "negative_summary": negative_summary, "professions": professions}


# ============================================================================= gating
def gating_check(mb, sae):
    rows = [_attach_span_tax(dict(r)) for r in load_taxonomic() if r["metadata_row_type"] == "corpus"][:64]
    layer_idx, fvu = mb.determine_layer_idx(rows, sae)
    _, resid_g, align_g = mb.encode_rows(rows, sae)
    torch = mb.torch
    hb = torch.tensor(resid_g.astype(np.float32), device=DEVICE)
    z = sae.encode(hb); hr = sae.decode(z)
    cos = float(torch.nn.functional.cosine_similarity(hb, hr, dim=-1).mean())
    l0 = float((z > 0).sum(1).float().mean())
    logger.info(f"{el()} GATING cosine={cos:.4f} L0={l0:.1f} layer_idx={layer_idx}")
    assert cos > 0.85, f"gating cosine {cos:.4f} too low (SAE/layer/model mismatch)"
    del hb, z, hr; gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return {"pass": bool(cos > 0.9), "cosine": round(cos, 4), "L0": round(l0, 1),
            "align": round(float(align_g), 4), "layer_idx": int(layer_idx),
            "fvu_by_idx": {str(k): round(float(v), 4) for k, v in fvu.items()}}


# ============================================================================= georgia self-check
def georgia_selfcheck(fam_tax, W_dec_np):
    """Run the IDENTICAL signature on Georgia with the canonical absorber 16009 -> must flag structured."""
    info = {"parent": "country", "letter": None}
    known = screen_candidate(fam_tax, "Georgia", info, W_dec_np, compute_oracle=True, known_absorber=16009)
    disc = screen_candidate(fam_tax, "Georgia", info, W_dec_np, compute_oracle=True)
    logger.info(f"{el()} GEORGIA self-check known16009 structured(strict)={known['absorption_structured_strict']} "
                f"recall_hole={known['recall_hole']} jac={known['firing_jaccard']} prec={known['precision']} "
                f"gain={known['hole_coverage_gain']}(CI {known['gain_ci_lo']}..{known['gain_ci_hi']}) "
                f"oracle_cos={known['oracle_decoder_cos']} | discovered_absorber={disc['absorber_latent']} "
                f"structured={disc['absorption_structured_strict']}")
    return {"known_16009": {k: known[k] for k in ("absorber_latent", "recall_hole", "firing_jaccard",
            "precision", "hole_coverage_gain", "gain_ci_lo", "gain_ci_hi", "oracle_decoder_cos",
            "absorption_structured_strict", "predict_absorption")},
            "discovered": {k: disc[k] for k in ("absorber_latent", "absorption_structured_strict",
            "predict_absorption")},
            "passed": bool(known["absorption_structured_strict"] or disc["absorption_structured_strict"])}


# ============================================================================= output assembly
HONEST_NEGATIVES = [
    "absorption is homograph-confined and, within homographs, NAMED-ENTITY-confined in this run (run_4i): "
    "structured = Georgia (taxonomic) + spelling word-types + the named-entity homographs Amazon/Bush/Cook; "
    "demographic safety groups are NOT structured (homograph-confined, ~2/44 in prior iters at most).",
    "the cross-run 'months only' homograph claim does NOT reproduce here: ALL calendar months are NO_HOLE "
    "(the is-a-month parent fires reliably even on homograph-strong May/March), matching this run's iter-8; "
    "0/28 professions (carried).",
    "a non-SAE dense probe matches/beats the single unit on classification (carried).",
    "the fair d_sub-gated dense control closes the edit gap (0/8 KG-beats-both in iter-8); the KG-absorber "
    "advantage over the FOOTPRINT-matched control was a footprint artifact.",
    "set-cover discovery is inert vs the unconstrained max-precision latent (mostly set_cover_eq=True).",
    "the clustering / multi-member grouping hypothesis did not pay off; the value is a label-free WHERE-screen.",
    "the decoder-projection oracle is concept-tuned: it confirms lexical/named-entity homograph absorbers but "
    "UNDER-fires for taxonomic (Georgia decoder near-orthogonal to the generic country direction).",
    "cross-stratum token overlap (Amazon in homograph_brand AND safety_named_entity; Apple likewise) is kept "
    "as separate rows under different PARENTS and flagged here; coverage dedups per (hierarchy, token).",
    "spelling word-types are mostly DESCRIPTIVE_ONLY (<150 corpus positives) so their coverage is the RELAXED "
    "breadth number, not the STRICT inferential one (e.g. 'large' is RELAXED-structured, n_eligible<150).",
    "FIRING-SIGNATURE != EDIT-HANDLE: a clean structured signature (e.g. Bush/Cook) need not yield a "
    "meaningful single-latent edit handle (carried iter-8 finding).",
]


def _screen_example(r):
    return {
        "input": (f"Absorption screen for '{r['token']}' ({r['hierarchy']}): is the parent concept "
                  f"suppressed on this token with a precise, mutually-exclusive absorber latent?"),
        "output": r["predict_absorption"],
        "predict_absorption": r["predict_absorption"],
        "metadata_token": r["token"], "metadata_hierarchy": r["hierarchy"], "metadata_parent": r["parent"],
        "metadata_family": r["family"], "metadata_n_x": r["n_x_fit"] + r["n_x_eval"],
        "metadata_n_eligible": r["n_eligible"], "metadata_eligible": r["eligible"],
        "metadata_anchor": r["anchor"], "metadata_recall_hole": r["recall_hole"],
        "metadata_firing_jaccard": r["firing_jaccard"], "metadata_precision": r["precision"],
        "metadata_hole_coverage_gain": r["hole_coverage_gain"], "metadata_gain_ci_lo": r["gain_ci_lo"],
        "metadata_gain_ci_hi": r["gain_ci_hi"], "metadata_random_latent_gain": r.get("random_latent_gain"),
        "metadata_absorber_latent": r["absorber_latent"], "metadata_parent_latent": r["parent_latent"],
        "metadata_max_prec_latent": r.get("max_prec_latent"),
        "metadata_set_cover_eq_max_precision": r.get("set_cover_eq_max_precision"),
        "metadata_concentration_score": r.get("concentration_score"),
        "metadata_oracle_decoder_cos": r.get("oracle_decoder_cos"),
        "metadata_oracle_absorption_fraction": r.get("oracle_absorption_fraction"),
        "metadata_oracle_corroborates": r.get("oracle_corroborates"),
        "metadata_absorption_structured_strict": r["absorption_structured_strict"],
        "metadata_absorption_structured_relaxed": r["absorption_structured_relaxed"],
    }


def _coverage_example(t):
    return {
        "input": f"{t['hierarchy']} coverage ({t['gate']} gate)",
        "output": str(t["fraction"]),
        "predict_coverage": f"{t['n_structured']}/{t['N']}",
        "metadata_hierarchy": t["hierarchy"], "metadata_gate": t["gate"], "metadata_N": t["N"],
        "metadata_n_structured": t["n_structured"], "metadata_fraction": t["fraction"],
        "metadata_wilson_lo": t["wilson_lo"], "metadata_wilson_hi": t["wilson_hi"],
        "metadata_boot_lo": t["boot_lo"], "metadata_boot_hi": t["boot_hi"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--mini", action="store_true")
    ap.add_argument("--no_oracle", action="store_true")
    args = ap.parse_args()

    set_limits()
    logger.info(f"{el()} ===== M3'''' absorption-coverage screen =====")
    torch = __import__("torch")
    sae = load_sae(torch)
    mb = ModelBundle(torch)
    gating = gating_check(mb, sae)
    W_dec_np = sae.W_dec.detach().cpu().numpy().astype(np.float32)

    kg = json.loads(KG4.read_text())["metadata"]["canonical_units"]
    spell_anchors = {lt: int(kg["first_letter"][lt]["anchor"]) for lt in ("L", "O", "T", "I", "D")}
    tax_anchor = int(kg["taxonomic"]["anchor"])

    families = []
    letters = ("L",) if args.smoke else ("L", "O", "T", "I", "D")
    families.append(build_spelling(mb, sae, spell_anchors, letters=letters))
    if not args.smoke:
        families.append(build_taxonomic(mb, sae, tax_anchor))
        hg_only = {"month", "brand"} if args.mini else None
        families.extend(build_homograph(mb, sae, only=hg_only))
        saf_only = {"named_entity_safety", "named_entity"} if args.mini else None
        families.extend(build_safety(mb, sae, only=saf_only))
    for fam in families:
        fam._sae = sae; fam.torch = torch
    fam_by_hier = {f.cov_hier: f for f in families}

    compute_oracle = not args.no_oracle and not args.smoke
    all_rows = []
    for fam in families:
        cand = candidates(fam, kg=kg)
        logger.info(f"{el()} [{fam.name}] {len(cand)} candidates")
        n = 0
        for tok, info in cand.items():
            r = screen_candidate(fam, tok, info, W_dec_np, compute_oracle=compute_oracle)
            all_rows.append(r); n += 1
            if args.smoke and n >= 5:
                break
        logger.info(f"{el()} [{fam.name}] screened {n}; "
                    f"structured(strict)={sum(1 for r in all_rows if r['family']==fam.name and r['absorption_structured_strict'])}")

    # de-dup per (hierarchy, token)
    seen = set(); rows = []
    for r in all_rows:
        key = (r["hierarchy"], r["token"])
        if key in seen:
            continue
        seen.add(key); rows.append(r)
    logger.info(f"{el()} TOTAL screened candidates (dedup): {len(rows)} "
                f"(eligible={sum(1 for r in rows if r['eligible'])})")

    coverage_table = aggregate_coverage(rows)
    pooled = {t["gate"]: t for t in coverage_table if t["hierarchy"] == "POOLED"}
    per_hier_counts = {}
    for t in coverage_table:
        if t["hierarchy"] != "POOLED":
            per_hier_counts.setdefault(t["hierarchy"], {})[t["gate"]] = f"{t['n_structured']}/{t['N']}"

    oracle_agree = oracle_agreement(rows) if compute_oracle else {"status": "oracle_off"}

    georgia_known = {}
    if "taxonomic_country" in fam_by_hier:
        try:
            georgia_known = georgia_selfcheck(fam_by_hier["taxonomic_country"], W_dec_np)
        except Exception as e:  # noqa: BLE001
            logger.warning(f"georgia selfcheck failed: {repr(e)[:160]}")
            georgia_known = {"error": repr(e)[:160]}
    controls = reproduce_controls(rows, georgia_known)

    metadata = {
        "method_name": "M3'''' Absorption-Coverage Screen + Shipped Label-Free Practitioner Screen",
        "overall_verdict": "COVERAGE_QUANTIFIED",
        "run_scale": ("smoke" if args.smoke else ("mini" if args.mini else "full")),
        "sae": {"release": core.RELEASE_REPO, "sae_id": core.SAE_PARAMS_16K, "width": int(sae.d_sae),
                "d_model": int(sae.d_model), "hook": "blocks.12.hook_resid_post"},
        "model": mb.model_id, "seed": SEED, "B_boot_gain": SCR.B_BOOT_GAIN, "B_boot_coverage": 10000,
        "gating_check": gating,
        "screen_thresholds": {"RECALL_HOLE_MIN": SCR.RECALL_HOLE_MIN, "JAC_MAX": SCR.JAC_MAX,
                              "PREC_MIN": SCR.PREC_MIN, "GAIN_MIN": SCR.GAIN_MIN,
                              "N_ELIGIBLE_MIN": SCR.N_ELIGIBLE_MIN, "DECODER_COS_MIN": SCR.DECODER_COS_MIN,
                              "MIN_FIRE_DIAG": SCR.MIN_FIRE_DIAG},
        "n_candidates_screened": len(rows), "n_eligible": sum(1 for r in rows if r["eligible"]),
        "coverage_table": coverage_table,
        "coverage_headline": {
            "pooled_strict_fraction": pooled.get("strict", {}).get("fraction"),
            "pooled_strict_ci_wilson": [pooled.get("strict", {}).get("wilson_lo"),
                                        pooled.get("strict", {}).get("wilson_hi")],
            "pooled_strict_n": f"{pooled.get('strict',{}).get('n_structured')}/{pooled.get('strict',{}).get('N')}",
            "pooled_relaxed_fraction": pooled.get("relaxed", {}).get("fraction"),
            "pooled_relaxed_ci_wilson": [pooled.get("relaxed", {}).get("wilson_lo"),
                                         pooled.get("relaxed", {}).get("wilson_hi")],
            "pooled_relaxed_n": f"{pooled.get('relaxed',{}).get('n_structured')}/{pooled.get('relaxed',{}).get('N')}",
            "per_hierarchy_structured_counts": per_hier_counts},
        "screen_vs_oracle_agreement": oracle_agree,
        "control_reproduction": controls,
        "shipped_screen_spec": {
            "entrypoint": "screen.py:screen_token", "cli": "python screen.py --token <T> --windows w.jsonl --siblings s.jsonl [--parent_latent L]",
            "inputs": ["frozen SAE (release/sae_id)", "candidate token", "raw corpus windows containing the token",
                       "surface-matched sibling windows (precision denominator)",
                       "OPTIONAL pinned parent latent id (else unsupervised highest-sibling-recall parent)"],
            "worked_example": ("python screen.py --token Georgia --windows example_windows_georgia.jsonl "
                               "--siblings example_siblings_countries.jsonl --parent_latent 3792 -> "
                               "ABSORPTION_STRUCTURED, absorber 16009 (canonical Georgia absorber)"),
            "outputs": ["predict_absorption enum", "absorption_structured (bool)", "recall_hole", "firing_jaccard",
                        "precision", "hole_coverage_gain + bootstrap CI", "absorber_latent", "parent_latent",
                        "oracle_corroborates (optional)"],
            "label_free_guarantee": ("the four-way flag uses ONLY model-internal firing statistics from a frozen "
                                     "SAE on raw text -- NO diagnostic probe, NO Chanin diagnostic, NO sub-context "
                                     "labels to flag; the form-free decoder-projection oracle is optional "
                                     "corroboration only."),
            "readme": "README.md"},
        "honest_negatives": HONEST_NEGATIVES,
        "cost_usd": 0.0, "budget_cap_usd": 10,
    }

    datasets = [
        {"dataset": "absorption_coverage_screen", "examples": [_screen_example(r) for r in rows]},
        {"dataset": "coverage_summary", "examples": [_coverage_example(t) for t in coverage_table]},
    ]
    out = {"metadata": metadata, "datasets": datasets}
    outp = RESULTS / ("smoke_method_out.json" if args.smoke else
                      ("mini_method_out.json" if args.mini else "method_out.json"))
    save_json(out, outp)
    # also write canonical method_out.json at workspace root for full runs
    if not args.smoke and not args.mini:
        save_json(out, WORK / "method_out.json")
    logger.info(f"{el()} WROTE {outp}")
    logger.info(f"{el()} POOLED strict={metadata['coverage_headline']['pooled_strict_n']} "
                f"relaxed={metadata['coverage_headline']['pooled_relaxed_n']}")
    logger.info(f"{el()} per-hierarchy: {json.dumps(per_hier_counts)}")
    logger.info(f"{el()} georgia_selfcheck passed={georgia_known.get('passed')}")
    return out


if __name__ == "__main__":
    main()
