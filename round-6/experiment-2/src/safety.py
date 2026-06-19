#!/usr/bin/env python
"""
SECTION 1 + 2 of M2': build SAFETY-RELEVANT identity candidate slices INLINE and run the $0
recall-hole + firing-Jaccard ABSORPTION SCREEN on the frozen Gemma-Scope L12/16k JumpReLU SAE.

A "hierarchy" = one general parent concept ('token names an identity group of type T') + many
mutually-exclusive group sub-contexts. Group membership is assigned PURELY from surface-form /
gazetteer matching over real text (civil_comments) and deterministic templates -- never from a
model or from the Jigsaw identity columns -- so the degenerate-construction guard holds and the
absorption presence/absence is a genuine empirical finding.

Screen primitives (recall-hole, firing-Jaccard, firing-floor parent) ported verbatim in spirit from
the iter-5 router (gen_art_experiment_3): identify_parent / per_subcontext / single-absorber finder.
The EXPECTED prior is NO safety hierarchy is absorption-structured (toxicity sub-attrs co-fire; 0/28
professions; absorption is a narrow homograph/polysemy phenomenon) -> the honest-null is publishable.
"""
import re
import numpy as np
from collections import defaultdict
from loguru import logger

# --------------------------------------------------------------------------- screen thresholds (router)
PREC_FLOOR = 0.70          # detector / absorber firing-precision floor
JACCARD_MAX = 0.10         # absorption ceiling: absorber must be firing-disjoint w/ parent
COVGAIN_FLOOR = 0.05       # absorber marginal hole-coverage gain
PARENT_FIRE_FLOOR = 0.20   # unsupervised parent-validation: parent fires on >=20% of positives
PARENT_CORPUS_FLOOR = 0.05 # firing-FLOOR on held-out corpus (fixes letter-I 0%-corpus spurious anchor)
RECALL_HOLE_FLAG = 0.50    # Georgia signature: parent recall-hole > 0.5
RECALL_HOLE_HIGH = 0.78    # secondary high-confidence (router rule)
MIN_SUB = 150              # min diagnostic positives for an eligible (inferential) sub-context
N_SHUFFLE = 1000           # sign-flip null permutations for content-responsiveness
B_JAC = 2000               # bootstrap for per-sub firing-Jaccard / hole-coverage CI

# =========================================================================== SAFETY GAZETTEERS
# Each hierarchy: canonical group -> list of surface alternatives. Surfaces matched case-aware with
# word boundaries; homograph-strong surfaces flagged (strongest absorption prior, like Georgia).
RELIGION = {
    "muslim": ["Muslim", "Muslims"], "christian": ["Christian", "Christians"],
    "jewish": ["Jew", "Jews", "Jewish"], "hindu": ["Hindu", "Hindus"],
    "buddhist": ["Buddhist", "Buddhists"], "catholic": ["Catholic", "Catholics"],
    "protestant": ["Protestant", "Protestants"], "mormon": ["Mormon", "Mormons"],
    "sikh": ["Sikh", "Sikhs"], "atheist": ["Atheist", "Atheists"],
    "evangelical": ["Evangelical", "Evangelicals"], "orthodox": ["Orthodox"],
}
RACE = {
    "black": ["Black", "Blacks"], "white": ["White", "Whites"], "asian": ["Asian", "Asians"],
    "latino": ["Latino", "Latinos", "Latina", "Latinas", "Latinx"], "hispanic": ["Hispanic", "Hispanics"],
    "arab": ["Arab", "Arabs"], "indigenous": ["Indigenous"], "african": ["African", "Africans"],
}
ORIENTATION = {
    "gay": ["gay", "gays"], "lesbian": ["lesbian", "lesbians"], "bisexual": ["bisexual", "bisexuals"],
    "transgender": ["transgender", "transgenders", "trans"], "queer": ["queer"],
    "homosexual": ["homosexual", "homosexuals"], "straight": ["straight"], "nonbinary": ["nonbinary"],
}
NATIONALITY = {
    "mexican": ["Mexican", "Mexicans"], "chinese": ["Chinese"], "russian": ["Russian", "Russians"],
    "nigerian": ["Nigerian", "Nigerians"], "indian": ["Indian", "Indians"], "iranian": ["Iranian", "Iranians"],
    "pakistani": ["Pakistani", "Pakistanis"], "german": ["German", "Germans"], "french": ["French"],
    "japanese": ["Japanese"], "korean": ["Korean", "Koreans"], "american": ["American", "Americans"],
    "british": ["British"], "canadian": ["Canadian", "Canadians"], "italian": ["Italian", "Italians"],
    "irish": ["Irish"], "polish": ["Polish"], "israeli": ["Israeli", "Israelis"],
    "syrian": ["Syrian", "Syrians"], "somali": ["Somali", "Somalis"], "turkish": ["Turkish"],
    "filipino": ["Filipino", "Filipinos"], "vietnamese": ["Vietnamese"], "ukrainian": ["Ukrainian", "Ukrainians"],
}
# homograph-strong surfaces (strong competing non-identity sense -> highest absorption prior)
HOMOGRAPH_GROUPS = {
    "black", "white", "asian",            # colors / continent
    "gay", "straight", "queer",           # name / adjective / adjective
    "orange",                             # (brand, not used here)
    "indian", "turkish", "french",        # river/place senses, language
}

HIERARCHIES = {
    "religion": ("token names a religion / religious group", RELIGION),
    "race_ethnicity": ("token names a race / ethnicity / identity group", RACE),
    "orientation_gender": ("token names a sexual orientation / gender identity", ORIENTATION),
    "nationality": ("token is a nationality / demonym", NATIONALITY),
}

# neutral adjective fillers for content-flip OFF pairs (surface-matched non-identity slot)
NEUTRAL_FILLERS = ["young", "older", "local", "quiet", "friendly", "tall", "retired", "creative",
                   "honest", "curious", "patient", "cheerful", "nearby", "former", "new"]

# content-flip templates: '{X}' is an adjective/noun-modifier slot fillable by an identity word or a
# neutral filler, grammatical either way. Used ONLY to identify the content-responsive parent latent.
TEMPLATES = [
    "My neighbor is {X}.",
    "She is proud to be {X}.",
    "He comes from a {X} background.",
    "They are a {X} couple.",
    "I met a {X} person yesterday.",
    "We talked to several {X} families.",
    "A {X} student gave a speech.",
    "The reporter interviewed a {X} man.",
    "Our new colleague is {X}.",
    "Many {X} people live in this city.",
]

STOPWORDS = set("the a an and or but of to in on at for with from by as is are was were be been being "
                "this that these those it its they them their there here who what which when where why how "
                "have has had do does did not no yes you your we our he she his her him about over under "
                "into out up down then than so if while because about more most some any all".split())


def _compile_group_regex(gaz):
    """canonical group -> compiled regex matching ANY of its surfaces with word boundaries.
    Returns (per_group_regex, any_surface_regex)."""
    per = {}
    all_surf = []
    for g, surfs in gaz.items():
        alt = "|".join(re.escape(s) for s in sorted(surfs, key=len, reverse=True))
        per[g] = re.compile(rf"\b({alt})\b")
        all_surf += surfs
    alt_all = "|".join(re.escape(s) for s in sorted(set(all_surf), key=len, reverse=True))
    return per, re.compile(rf"\b({alt_all})\b")


# union of ALL identity surfaces across hierarchies (for clean-negative filtering)
def _global_identity_regex():
    surfs = []
    for _, gaz in HIERARCHIES.values():
        for s in gaz.values():
            surfs += s
    alt = "|".join(re.escape(s) for s in sorted(set(surfs), key=len, reverse=True))
    return re.compile(rf"\b({alt})\b")


GLOBAL_IDENTITY_RE = _global_identity_regex()


def _crop_window(text, start, end, radius=180):
    """Crop a window of ~2*radius chars centred on [start,end); return (window, new_start, new_end)."""
    a = max(0, start - radius)
    b = min(len(text), end + radius)
    # snap to whitespace boundaries so we don't slice mid-word
    if a > 0:
        sp = text.find(" ", a)
        a = sp + 1 if 0 <= sp < start else a
    if b < len(text):
        sp = text.rfind(" ", end, b)
        b = sp if sp > end else b
    win = text[a:b]
    return win, start - a, end - a


def _content_token_span(text):
    """Pick a content-word char span in `text` to anchor a NEGATIVE (concept-absent) window."""
    for m in re.finditer(r"\b[A-Za-z]{4,}\b", text):
        if m.start() >= 6 and m.group(0).lower() not in STOPWORDS:
            return m.start(), m.end()
    m = re.search(r"\b[A-Za-z]{3,}\b", text)
    return (m.start(), m.end()) if m else (0, min(3, len(text)))


# =========================================================================== SLICE BUILDER
def build_identity_hierarchy(name, parent_desc, gaz, civil_rows, *, cap_pos=700, cap_neg=2500,
                             seed=20240617):
    """Assemble the three coordinated screen components for ONE identity hierarchy.
      (A) content-flip pairs  on={template w/ identity word}, off={template w/ neutral filler}
      (B) corpus positives    natural civil_comments windows w/ a group surface (token-anchored)
      (C) matched negatives    civil_comments windows with NO identity surface (any hierarchy)
    Returns dict of row-lists (each row carries 'input','_span','_ti','_target' for core.encode_rows
    plus '_group'/'_role'/'_fold'/'_homograph'/'_identity_attack')."""
    rng = np.random.default_rng(seed)
    per_re, _any_re = _compile_group_regex(gaz)
    groups = list(gaz.keys())

    # ---------- (A) content-flip pairs ----------
    cf_on, cf_off = [], []
    pid = 0
    # one canonical surface per group (first), to keep the slot single-concept
    for g in groups:
        surf = gaz[g][0]
        for ti, tmpl in enumerate(TEMPLATES):
            filler = NEUTRAL_FILLERS[(pid) % len(NEUTRAL_FILLERS)]
            on_text = tmpl.replace("{X}", surf)
            off_text = tmpl.replace("{X}", filler)
            on_s = on_text.index(surf)
            off_s = off_text.index(filler)
            cf_on.append({"input": on_text, "_span": (on_s, on_s + len(surf)), "_ti": None,
                          "_target": surf, "_group": g, "_role": "on", "_pair_id": pid})
            cf_off.append({"input": off_text, "_span": (off_s, off_s + len(filler)), "_ti": None,
                           "_target": filler, "_group": g, "_role": "off", "_pair_id": pid})
            pid += 1

    # ---------- (B) corpus positives (natural) ----------
    pos_by_group = defaultdict(list)
    neg_rows = []
    # fast-path: this hierarchy's union regex; only do per-group searches when it matches
    hier_any = _compile_group_regex(gaz)[1]
    full_pos = {g: False for g in groups}
    for r in civil_rows:
        text = r["text"]
        ia = r["identity_attack"]
        hm = hier_any.search(text)
        if hm is None:
            # not this hierarchy; is there ANY identity surface? if not -> clean negative
            if len(neg_rows) < cap_neg and len(text) > 40 and GLOBAL_IDENTITY_RE.search(text) is None:
                win = text[:360]
                cs, ce = _content_token_span(win)
                neg_rows.append({"input": win, "_span": (cs, ce), "_ti": None, "_target": win[cs:ce],
                                 "_group": None, "_role": "neg", "_identity_attack": float(ia)})
            continue
        # this hierarchy present: label by the EARLIEST-occurring surface (unbiased)
        matched = None
        for g in groups:
            if full_pos[g]:
                continue
            m = per_re[g].search(text)
            if m and (matched is None or m.start(1) < matched[1]):
                matched = (g, m.start(1), m.end(1))
        if matched is not None:
            g, s, e = matched
            if len(pos_by_group[g]) >= cap_pos:
                full_pos[g] = True
                continue
            win, ns, ne = _crop_window(text, s, e)
            if ns < 0 or ne > len(win) or ne <= ns:
                continue
            pos_by_group[g].append({"input": win, "_span": (ns, ne), "_ti": None,
                                    "_target": win[ns:ne], "_group": g, "_role": "pos",
                                    "_identity_attack": float(ia)})

    # ---------- assign 50/50 fit/diagnostic folds per group (stratified) ----------
    pos_rows = []
    for g, rows in pos_by_group.items():
        idx = rng.permutation(len(rows))
        for k, i in enumerate(idx):
            rows[i]["_fold"] = "fit" if k % 2 == 0 else "diagnostic"
            rows[i]["_homograph"] = (g in HOMOGRAPH_GROUPS)
            pos_rows.append(rows[i])
    # negatives split 50/50 too (fit used for detector-AUC negatives; both pools available)
    nidx = rng.permutation(len(neg_rows))
    for k, i in enumerate(nidx):
        neg_rows[i]["_fold"] = "fit" if k % 2 == 0 else "diagnostic"

    counts = {g: len(rows) for g, rows in pos_by_group.items()}
    logger.info(f"  [{name}] content-flips={len(cf_on)} pairs | corpus pos per group="
                + ", ".join(f"{g}:{counts.get(g,0)}" for g in groups) + f" | neg={len(neg_rows)}")
    return {"name": name, "parent_desc": parent_desc, "groups": groups,
            "cf_on": cf_on, "cf_off": cf_off, "pos": pos_rows, "neg": neg_rows,
            "counts": counts}


# =========================================================================== SCREEN PRIMITIVES
def firing_jaccard(fires_a, fires_b):
    a = fires_a.astype(bool); b = fires_b.astype(bool)
    inter = int((a & b).sum()); union = int((a | b).sum())
    return (inter / union) if union > 0 else 0.0


def _rankdata(a):
    order = np.argsort(a, kind="mergesort")
    r = np.empty(len(a), dtype=np.float64)
    r[order] = np.arange(1, len(a) + 1)
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


def cols_auc(mat, y):
    """AUC of every column of mat[N,L] vs binary y (vectorised Mann-Whitney)."""
    y = np.asarray(y).astype(bool)
    npos, nneg = int(y.sum()), int((~y).sum())
    if npos == 0 or nneg == 0:
        return np.full(mat.shape[1], np.nan)
    mat = mat.astype(np.float32)
    ranks = np.apply_along_axis(_rankdata, 0, mat)
    sumpos = ranks[y].sum(0)
    return (sumpos - npos * (npos + 1) / 2.0) / (npos * nneg)


def identify_parent(on_lat, off_lat, pos_lat, rng):
    """Content-responsive latents + firing-floor-validated PARENT (highest positive-firing recall
    among responsive latents that also clear an unsupervised corpus firing floor). Chosen WITHOUT the
    Chanin diagnostic. Returns (parent, responsive_idx, precision_arr, pos_fire_rate, info)."""
    on = on_lat.astype(np.float32); off = off_lat.astype(np.float32)
    R = on - off
    P = R.shape[0]
    mean_r = R.mean(0)
    null = np.empty((N_SHUFFLE, R.shape[1]), dtype=np.float32)
    for i in range(N_SHUFFLE):
        s = rng.choice([-1.0, 1.0], size=P).astype(np.float32)
        null[i] = (s[:, None] * R).mean(0)
    null95 = np.percentile(null, 95, axis=0)
    del null
    responsive_mask = (mean_r > null95) & (mean_r > 0)
    fires_on = on > 0; fires_off = off > 0
    on_c = fires_on.sum(0).astype(np.float64); off_c = fires_off.sum(0).astype(np.float64)
    precision = np.divide(on_c, np.maximum(on_c + off_c, 1))
    resp = np.where(responsive_mask & (precision >= PREC_FLOOR))[0]
    if len(resp) == 0:
        resp = np.where(responsive_mask)[0]
    pos_fire_rate = (pos_lat > 0).mean(0)                       # recall on the corpus positive set
    # firing-FLOOR: parent must fire on >=PARENT_FIRE_FLOOR of content-flip positives AND
    # >=PARENT_CORPUS_FLOOR of held-out corpus positives (kills 0%-corpus spurious anchors)
    cand = [int(l) for l in resp
            if (fires_on[:, l].mean() >= PARENT_FIRE_FLOOR) and (pos_fire_rate[l] >= PARENT_CORPUS_FLOOR)]
    unresolved = False
    if not cand:
        cand = [int(l) for l in resp if pos_fire_rate[l] >= PARENT_CORPUS_FLOOR]
        unresolved = True
    if not cand:
        return -1, resp, precision, pos_fire_rate, {"parent_unresolved": True, "n_responsive": int(len(resp)),
                                                    "reason": "no responsive latent clears corpus firing floor"}
    parent = int(max(cand, key=lambda l: pos_fire_rate[l]))
    info = {"n_responsive": int(len(resp)), "parent_pos_corpus_firing": float(pos_fire_rate[parent]),
            "parent_contentflip_precision": float(precision[parent]),
            "parent_contentflip_recall": float(fires_on[:, parent].mean()),
            "parent_unresolved": bool(unresolved)}
    return parent, resp, precision, pos_fire_rate, info


def _detector_precision(det_fires, is_group, is_neg):
    """firing-precision of a detector latent: among rows where it fires (group-pos ∪ neg),
    fraction that are group-positives."""
    fire_pos = int((det_fires & is_group).sum())
    fire_neg = int((det_fires & is_neg).sum())
    denom = fire_pos + fire_neg
    return (fire_pos / denom) if denom > 0 else 0.0


def absorption_fraction_oracle(resid_rows, z_abs, w_dec_abs, d_p, tau_c=0.0):
    """FORM-FREE absorption diagnostic (SAEBench `absorption_fraction`, Chanin A.13) — strictly
    NON-CIRCULAR: never used to flag, only to VALIDATE a flagged edge. A latent `l` absorbs the parent
    concept on a row iff its decoder contribution carries the parent-probe direction d_p more than tau_c
    of the full activation's projection: (a_hat_l . d_p) / (a . d_p) > tau_c, where a_hat_l = z_l*W_dec[l],
    a = the residual, d_p = parent LR-probe direction trained on data DISJOINT from this fold. Returns the
    fraction of rows (with a.d_p>0) on which the absorber carries the parent direction."""
    a = resid_rows.astype(np.float32)                       # [n, d_model]
    a_dot = a @ d_p                                          # [n]
    ahat_dot = (z_abs.astype(np.float32)[:, None] * w_dec_abs[None, :]) @ d_p   # [n]
    valid = a_dot > 1e-6
    if int(valid.sum()) == 0:
        return float("nan"), 0
    ratio = ahat_dot[valid] / a_dot[valid]
    return float((ratio > tau_c).mean()), int(valid.sum())


def screen_subcontexts(parent, resp, pos_lat_diag, pos_sub_diag, neg_lat_fit, parent_fire_all,
                       fires_pos_all, sub_all, rng):
    """For each eligible group: detector latent, parent recall-hole, firing-Jaccard(parent,detector),
    detector firing-precision, marginal hole-coverage gain + bootstrap CI, and the absorption-structured
    flag (the Georgia signature)."""
    elig_lat = np.array([l for l in resp if l != parent], dtype=int)
    fires_pos_diag = pos_lat_diag > 0
    fires_parent_diag = fires_pos_diag[:, parent]
    out = []
    groups = [g for g in sorted(set(pos_sub_diag.tolist()))
              if g is not None and int((pos_sub_diag == g).sum()) >= 1]
    for g in groups:
        m = pos_sub_diag == g
        n_pos = int(m.sum())
        parent_recall = float(fires_parent_diag[m].mean()) if n_pos else float("nan")
        recall_hole = float(1.0 - parent_recall)
        gmask_all = sub_all == g
        holes = ~fires_parent_diag[m]                          # parent's holes on group diag positives
        n_holes = int(holes.sum())
        # candidate latents = eligible latents firing on >=2 of this group's diagnostic positives
        cand = np.array([], int)
        if len(elig_lat) and n_pos >= 2:
            grp_fire = (pos_lat_diag[m][:, elig_lat] > 0)      # [n_pos, E]
            cand = elig_lat[grp_fire.sum(0) >= 2]
        # ----- K-TRACK-LITE ABSORBER SEARCH (the Georgia signature: firing-disjoint + hole-covering + precise) -----
        # plus a best-AUC detector for transparency. All quantities vectorised over candidate latents.
        det = parent; det_auc = float("nan"); det_prec = 0.0; jac = 1.0; cov_gain = 0.0
        bestauc_latent = parent; bestauc = float("nan"); bestauc_jac = 1.0
        if len(cand) and neg_lat_fit.shape[0] >= 2 and n_pos >= 2:
            gpos = (pos_lat_diag[m][:, cand] > 0)              # [n_pos, C]
            nfire = (neg_lat_fit[:, cand] > 0)                 # [n_neg, C]
            fpos = gpos.sum(0).astype(np.float64); fneg = nfire.sum(0).astype(np.float64)
            prec_c = fpos / np.maximum(fpos + fneg, 1)         # firing-precision per candidate
            cov_c = (gpos[holes].sum(0) / max(n_holes, 1)) if n_holes else np.zeros(len(cand))  # hole-coverage gain
            par_all = fires_pos_all[gmask_all, parent]         # [n_all]
            cand_all = fires_pos_all[gmask_all][:, cand]       # [n_all, C]
            inter = (cand_all & par_all[:, None]).sum(0).astype(np.float64)
            union = (cand_all | par_all[:, None]).sum(0).astype(np.float64)
            jac_c = inter / np.maximum(union, 1)               # firing-Jaccard(parent, candidate)
            # best-AUC detector (transparency only)
            sc = np.concatenate([pos_lat_diag[m][:, cand], neg_lat_fit[:, cand]], 0).astype(np.float32)
            yy = np.concatenate([np.ones(n_pos), np.zeros(neg_lat_fit.shape[0])])
            aucs = cols_auc(sc, yy)
            if np.isfinite(aucs).any():
                ai = int(np.nanargmax(aucs)); bestauc_latent = int(cand[ai])
                bestauc = float(aucs[ai]); bestauc_jac = float(jac_c[ai])
            # ABSORBER = firing-disjoint (jac<JACCARD_MAX) AND precise (>=PREC_FLOOR) AND covers holes -> max cov
            mask_abs = (jac_c < JACCARD_MAX) & (prec_c >= PREC_FLOOR) & (cov_c > 0)
            bi = int(np.where(mask_abs)[0][np.argmax(cov_c[mask_abs])]) if mask_abs.any() else int(np.argmax(cov_c))
            det = int(cand[bi]); det_prec = float(prec_c[bi]); jac = float(jac_c[bi]); cov_gain = float(cov_c[bi])
            det_auc = float(aucs[bi]) if np.isfinite(aucs[bi]) else float("nan")
        # bootstrap CI of the chosen absorber's hole-coverage gain over group-positives
        cov_ci = [float("nan"), float("nan")]
        if n_pos >= 5 and n_holes and det != parent:
            di = (pos_lat_diag[m][:, det] > 0).astype(bool); hi = holes.astype(bool)
            vals = np.empty(B_JAC)
            for b in range(B_JAC):
                ii = rng.integers(0, n_pos, n_pos)
                nh = int(hi[ii].sum())
                vals[b] = (di[ii] & hi[ii]).sum() / nh if nh else 0.0
            cov_ci = [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]
        eligible = n_pos >= MIN_SUB
        absorption_structured = bool(
            eligible and recall_hole > RECALL_HOLE_FLAG and jac < JACCARD_MAX
            and det_prec >= PREC_FLOOR and cov_gain >= COVGAIN_FLOOR and cov_ci[0] > 0)
        high_conf = bool(absorption_structured and recall_hole > RECALL_HOLE_HIGH)
        if eligible:
            pred = "ABSORPTION_STRUCTURED" if absorption_structured else (
                "NO_HOLE" if recall_hole <= RECALL_HOLE_FLAG else "CO_FIRING")
        else:
            pred = "DESCRIPTIVE_ONLY"
        out.append({"sub_context": g, "n_pos_diagnostic": n_pos, "n_pos_all": int(gmask_all.sum()),
                    "eligible": bool(eligible), "parent_recall": parent_recall, "recall_hole": recall_hole,
                    "detector_latent": det, "detector_auc": det_auc, "detector_precision": det_prec,
                    "firing_jaccard": float(jac), "hole_coverage_gain": cov_gain,
                    "hole_coverage_ci": cov_ci, "absorption_structured": absorption_structured,
                    "high_conf_flag": high_conf, "predict_absorption": pred,
                    "bestauc_detector_latent": int(bestauc_latent), "bestauc_detector_auc": bestauc,
                    "bestauc_detector_jaccard": bestauc_jac, "n_holes": n_holes})
    return out
