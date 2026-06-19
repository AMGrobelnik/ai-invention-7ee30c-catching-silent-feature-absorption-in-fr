#!/usr/bin/env python
"""
screen.py  —  M3'''' LABEL-FREE ABSORPTION-COVERAGE SCREEN  (the shipped practitioner deliverable).

WHAT IT DOES
------------
Given a FROZEN SAE, a candidate token X, and raw corpus windows containing X (plus surface-matched
sibling windows of the same parent concept), this module decides — WITHOUT any diagnostic probe, any
Chanin absorption diagnostic, and any sub-context labels — whether the parent concept is *suppressed*
on X and *re-encoded* by a single, mutually-exclusive, precise "absorber" latent (the Georgia /
first-letter-spelling 'large' signature).  It assigns one of four labels:

    ABSORPTION_STRUCTURED  parent recall-hole on X is large, a firing-disjoint precise absorber covers
                           the hole with a bootstrap-CI-positive coverage gain, and X has enough
                           positives for an inferential claim (n_eligible >= 150).
    CO_FIRING              there is a recall-hole but no clean mutually-exclusive absorber (the
                           sub-attribute co-fires with the parent) -> NOT absorption-structured.
    NO_HOLE                the parent latent fires on X just like on its siblings (no suppression).
    DESCRIPTIVE_ONLY       fewer than N_ELIGIBLE_MIN positives -> reported for breadth, not inference.

LABEL-FREE GUARANTEE
--------------------
The four-way flag uses ONLY model-internal firing statistics (recall, firing-Jaccard, firing-precision,
hole-coverage gain) computed from a frozen SAE on raw text.  The optional form-free decoder-projection
ORACLE (`absorption_fraction_oracle`, SAEBench / Chanin A.13) is *corroboration only*: it needs a dense
parent-probe direction d_p fit on a DISJOINT fold (never a single latent, never used to flag), and is
known to be concept-tuned — it confirms lexical / named-entity homograph absorbers strongly but under-fires
for the taxonomic 'country' direction (Georgia's decoder is near-orthogonal to the generic country
direction), so it must NOT gate the structured flag.

The screen logic here is exercised by method.py over a wide multi-hierarchy candidate pool to produce a
COVERAGE TABLE (one fraction-structured per hierarchy, with Wilson + bootstrap CIs).  The same
`screen_token` entry point is the standalone CLI tool (see __main__).

CLI
---
    python screen.py --token Georgia --windows windows.jsonl --siblings siblings.jsonl
        windows.jsonl / siblings.jsonl : one JSON object per line, each {"input": "<text with the token>"}
        (optionally "span": [char_start, char_end] to pin the token; else the first occurrence is used).
"""
import os, sys, json, argparse
import numpy as np

import core
from core import logger, el, ParentProbe, DEVICE, SEED

# ----------------------------------------------------------------------------- screen thresholds
RECALL_HOLE_MIN = 0.50    # parent recall-hole floor (suppressed parent)
JAC_MAX         = 0.10    # firing-Jaccard(parent, absorber) ceiling (mutual exclusivity)
PREC_MIN        = 0.70    # absorber sub-context firing-precision floor
GAIN_MIN        = 0.05    # hole-coverage-gain floor (also requires bootstrap CI excl 0)
N_ELIGIBLE_MIN  = 150     # min fit/diagnostic-fold X-positives for the STRICT (inferential) gate
DECODER_COS_MIN = 0.025   # canonical Chanin / SAEBench probe_cos_sim_threshold on W_dec (oracle)
MIN_FIRE_DIAG   = 5       # absorber must fire on >= this many fit-fold X-positive rows to be considered
PARENT_FIRE_FLOOR = 0.05  # (CLI) parent latent must fire on >= this fraction of sibling windows
B_BOOT_GAIN     = 5000    # bootstrap reps for the hole-coverage-gain CI

ENUM = ("ABSORPTION_STRUCTURED", "CO_FIRING", "NO_HOLE", "DESCRIPTIVE_ONLY")

rng = np.random.default_rng(SEED)


# ============================================================================= small stats
def firing_jaccard_bool(a_bool, b_bool):
    a = a_bool.astype(bool); b = b_bool.astype(bool)
    inter = int((a & b).sum()); union = int((a | b).sum())
    return (inter / union) if union > 0 else 0.0


def wilson_ci(k, n, z=1.96):
    """Wilson score interval for a binomial proportion."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1.0 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = (z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / d
    return (float(max(0.0, centre - half)), float(min(1.0, centre + half)))


def bootstrap_fraction_ci(flags, B=10000, seed=SEED):
    """Percentile bootstrap of the mean of a 0/1 array (coverage fraction)."""
    flags = np.asarray(flags, dtype=float)
    n = len(flags)
    if n == 0:
        return (0.0, 0.0)
    r = np.random.default_rng(seed)
    idx = r.integers(0, n, size=(B, n))
    bs = flags[idx].mean(1)
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return (float(lo), float(hi))


def cohen_kappa(a, b):
    """Cohen's kappa between two binary label arrays."""
    a = np.asarray(a, dtype=int); b = np.asarray(b, dtype=int)
    n = len(a)
    if n == 0:
        return float("nan")
    po = float((a == b).mean())
    pa1 = a.mean(); pb1 = b.mean()
    pe = pa1 * pb1 + (1 - pa1) * (1 - pb1)
    if abs(1 - pe) < 1e-12:
        return 1.0 if po == 1.0 else 0.0
    return float((po - pe) / (1 - pe))


# ============================================================================= form-free oracle
def absorption_fraction_oracle(resid_rows, z_abs, w_dec_abs, d_p, tau_c=0.0):
    """FORM-FREE absorption diagnostic (SAEBench `absorption_fraction`, Chanin et al. 2024 App. A.13) —
    strictly NON-CIRCULAR: never used to flag, only to corroborate a flagged edge.

    A latent l absorbs the parent concept on a row iff its decoder contribution carries the parent-probe
    direction d_p by more than tau_c of the full activation's projection:
        (a_hat_l . d_p) / (a . d_p) > tau_c,   a_hat_l = z_l * W_dec[l],  a = residual,  d_p = parent dir.
    d_p MUST be trained on data disjoint from this fold.  Returns (fraction_of_rows, n_valid)."""
    a = np.asarray(resid_rows, dtype=np.float32)
    a_dot = a @ d_p
    ahat_dot = (np.asarray(z_abs, dtype=np.float32)[:, None] * w_dec_abs[None, :]) @ d_p
    valid = a_dot > 1e-6
    if int(valid.sum()) == 0:
        return float("nan"), 0
    ratio = ahat_dot[valid] / a_dot[valid]
    return float((ratio > tau_c).mean()), int(valid.sum())


# ============================================================================= the enum
def classify(recall_hole, jac, precision, gain, gain_lo, n_eligible):
    """The four-way label-free verdict + strict/relaxed structured flags."""
    eligible = (n_eligible is not None and int(n_eligible) >= N_ELIGIBLE_MIN)
    sig = (recall_hole is not None and recall_hole > RECALL_HOLE_MIN and
           jac is not None and jac < JAC_MAX and
           precision is not None and precision >= PREC_MIN and
           gain is not None and gain >= GAIN_MIN and
           gain_lo is not None and gain_lo > 0)
    strict = bool(sig and eligible)
    relaxed = bool(sig)                      # signature minus the n_eligible>=150 requirement
    if not eligible:
        predict = "DESCRIPTIVE_ONLY"
    elif strict:
        predict = "ABSORPTION_STRUCTURED"
    elif recall_hole is None or recall_hole <= RECALL_HOLE_MIN:
        predict = "NO_HOLE"
    else:
        predict = "CO_FIRING"
    return predict, strict, relaxed, eligible


# ============================================================================= core signature engine
def compute_signature(*, token, hierarchy, parent, anchor, lat_csr, resid, cr,
                      fit_Xpos, eval_Xpos, fit_corpus, eval_corpus_pos, sub_eval,
                      W_dec_np, sae=None, probe=None, n_eligible, known_absorber=None,
                      compute_oracle=False, par_fire=None, cand_fire=None):
    """Compute the full absorption signature for candidate `token` on pre-encoded family arrays.

    Parameters (all row-index arrays index into lat_csr/resid):
      anchor            : the parent latent (KG anchor, or data-derived highest-recall content latent)
      cr                : content-responsive candidate latent ids (the absorber search pool)
      fit_Xpos          : fit/diagnostic-fold rows that are X-positive (absorber chosen here)
      eval_Xpos         : eval-fold rows that are X-positive (recall-hole / gain scored here)
      fit_corpus        : fit-fold corpus rows (all sub-contexts pos + negatives; precision_diag denom)
      eval_corpus_pos   : eval-fold corpus-positive rows across ALL sub-contexts (held-out precision pool)
      sub_eval          : per-row sub-context label aligned to lat_csr rows (object array)
      probe             : core.ParentProbe (only needed when compute_oracle=True); d_p = probe.d_mu
    Returns a flat dict row (JSON-friendly)."""
    N = lat_csr.shape[0]
    anchor = int(anchor) if anchor is not None and anchor >= 0 else -1
    if par_fire is None:
        par_fire = (np.asarray(lat_csr[:, anchor].todense()).ravel() > 0) if anchor >= 0 else np.zeros(N, bool)

    # ---- (a) recall-hole on held-out X rows ----
    recall_hole = (1.0 - float(par_fire[eval_Xpos].mean())) if len(eval_Xpos) else None

    # ---- (b) absorber via K-track-lite on the FIT (diagnostic) fold ----
    cr_arr = np.asarray([int(c) for c in cr], dtype=int)
    keep = cr_arr != anchor
    cand = cr_arr[keep]
    absorber = None
    absorber_meta = {}
    if len(cand) and len(fit_Xpos):
        C = cand_fire[:, keep] if cand_fire is not None else np.asarray((lat_csr[:, cand] > 0).todense())
        Cd_X = C[fit_Xpos]
        Cd_corp = C[fit_corpus] if len(fit_corpus) else C[fit_Xpos]
        fires_fitXpos = Cd_X.sum(0)
        fires_fitcorp = Cd_corp.sum(0)
        precision_diag = fires_fitXpos / np.maximum(fires_fitcorp, 1)
        inter = (C & par_fire[:, None]).sum(0)
        union = (C | par_fire[:, None]).sum(0)
        jac = inter / np.maximum(union, 1)
        par_silent = ~par_fire[fit_Xpos]
        cover = Cd_X[par_silent].mean(0) if par_silent.sum() else np.zeros(len(cand))
        qualify = ((precision_diag >= PREC_MIN) & (jac < JAC_MAX) & (cover > 0) &
                   (fires_fitXpos >= MIN_FIRE_DIAG))
        if qualify.any():
            qidx = np.where(qualify)[0]
            best = qidx[int(np.argmax(cover[qidx]))]
            absorber = int(cand[best])
            absorber_meta = {"qualified": True, "precision_diag": float(precision_diag[best]),
                             "jaccard_diag": float(jac[best]), "hole_cover_diag": float(cover[best]),
                             "n_fire_fitXpos": int(fires_fitXpos[best])}
        else:
            mex = np.where((jac < JAC_MAX) & (fires_fitXpos >= MIN_FIRE_DIAG))[0]
            if len(mex):
                best = mex[int(np.argmax(cover[mex]))]
                absorber = int(cand[best])
                absorber_meta = {"qualified": False, "precision_diag": float(precision_diag[best]),
                                 "jaccard_diag": float(jac[best]), "hole_cover_diag": float(cover[best]),
                                 "n_fire_fitXpos": int(fires_fitXpos[best])}
        del C, Cd_X, Cd_corp
    if known_absorber is not None:
        absorber = int(known_absorber)
        absorber_meta["known_absorber_override"] = True

    base = {"token": token, "hierarchy": hierarchy, "parent": parent,
            "anchor": anchor, "parent_latent": anchor, "n_eligible": int(n_eligible),
            "n_x_fit": int(len(fit_Xpos)), "n_x_eval": int(len(eval_Xpos)),
            "recall_hole": (round(recall_hole, 4) if recall_hole is not None else None)}

    if absorber is None:
        predict, strict, relaxed, eligible = classify(recall_hole, None, None, None, None, n_eligible)
        base.update({"absorber_latent": None, "firing_jaccard": None, "precision": None,
                     "hole_coverage_gain": None, "gain_ci_lo": None, "gain_ci_hi": None,
                     "random_latent_gain": None, "oracle_decoder_cos": None,
                     "oracle_absorption_fraction": None, "oracle_corroborates": False,
                     "predict_absorption": predict, "absorption_structured_strict": False,
                     "absorption_structured_relaxed": False, "eligible": eligible,
                     "absorber_meta": absorber_meta, "note": "no_absorber_candidate"})
        return base

    ab_fire = np.asarray(lat_csr[:, absorber].todense()).ravel() > 0
    union = int((par_fire | ab_fire).sum())
    firing_jaccard = int((par_fire & ab_fire).sum()) / max(union, 1)

    # ---- (c) held-out precision: fraction of absorber-firing eval corpus-pos rows whose sub == token ----
    if len(eval_corpus_pos):
        ev_fire = eval_corpus_pos[ab_fire[eval_corpus_pos]]
    else:
        ev_fire = np.array([], int)
    if len(ev_fire) >= 3:
        precision = float(np.mean([sub_eval[i] == token for i in ev_fire]))
        n_ev_fire = int(len(ev_fire))
    else:
        precision = float(absorber_meta.get("precision_diag", 0.0)); n_ev_fire = int(len(ev_fire))

    # ---- (d) hole-coverage gain (+ bootstrap CI) on held-out X rows ----
    gain = gain_lo = gain_hi = None; rand_gain = None
    if len(eval_Xpos) >= 8:
        par_x = par_fire[eval_Xpos].astype(float)
        comb_x = (par_fire[eval_Xpos] | ab_fire[eval_Xpos]).astype(float)
        gain = float(comb_x.mean() - par_x.mean())
        n = len(eval_Xpos)
        idx = rng.integers(0, n, size=(B_BOOT_GAIN, n))
        gains = comb_x[idx].mean(1) - par_x[idx].mean(1)
        gain_lo, gain_hi = [float(v) for v in np.percentile(gains, [2.5, 97.5])]
        # random content-responsive latent control (firing-rate matched)
        try:
            rl, _ = core.pick_random_latents(lat_csr, absorber,
                                             [int(c) for c in cr], {int(absorber), anchor}, n=1)
            if rl:
                rfire = np.asarray(lat_csr[:, int(rl[0])].todense()).ravel() > 0
                rcomb = (par_fire[eval_Xpos] | rfire[eval_Xpos]).astype(float)
                rand_gain = float(rcomb.mean() - par_x.mean())
        except Exception:
            rand_gain = None

    # ---- (e) FORM-FREE oracle (corroboration only) ----
    oracle_cos = oracle_frac = None
    oracle_corroborates = False
    if compute_oracle and probe is not None:
        wdec_ab = W_dec_np[absorber].astype(np.float64)
        wdec_ab_u = wdec_ab / (np.linalg.norm(wdec_ab) + 1e-9)
        d_p = probe.d_mu.astype(np.float64); d_p = d_p / (np.linalg.norm(d_p) + 1e-9)
        oracle_cos = float(wdec_ab_u @ d_p)
        oracle_corroborates = bool(oracle_cos >= DECODER_COS_MIN)
        hole_rows = eval_Xpos[~par_fire[eval_Xpos]] if len(eval_Xpos) else np.array([], int)
        if len(hole_rows) >= 3:
            z_abs = np.asarray(lat_csr[hole_rows][:, absorber].todense()).ravel().astype(np.float32)
            frac, _ = absorption_fraction_oracle(resid[hole_rows], z_abs,
                                                 W_dec_np[absorber].astype(np.float32),
                                                 d_p.astype(np.float32), tau_c=0.0)
            oracle_frac = None if (frac != frac) else float(frac)

    predict, strict, relaxed, eligible = classify(recall_hole, firing_jaccard, precision,
                                                  gain, gain_lo, n_eligible)
    base.update({
        "absorber_latent": int(absorber), "firing_jaccard": round(float(firing_jaccard), 4),
        "precision": round(float(precision), 4), "n_absorber_fire_heldout": n_ev_fire,
        "hole_coverage_gain": (round(gain, 4) if gain is not None else None),
        "gain_ci_lo": (round(gain_lo, 4) if gain_lo is not None else None),
        "gain_ci_hi": (round(gain_hi, 4) if gain_hi is not None else None),
        "random_latent_gain": (round(rand_gain, 4) if rand_gain is not None else None),
        "oracle_decoder_cos": (round(oracle_cos, 4) if oracle_cos is not None else None),
        "oracle_absorption_fraction": (round(oracle_frac, 4) if oracle_frac is not None else None),
        "oracle_corroborates": bool(oracle_corroborates),
        "predict_absorption": predict, "absorption_structured_strict": strict,
        "absorption_structured_relaxed": relaxed, "eligible": eligible,
        "absorber_meta": absorber_meta})
    return base


# ============================================================================= standalone CLI tool
def _encode_windows(mb, sae, rows):
    """Encode raw window rows -> (lat_csr, resid).  Each row must carry input/_span/_ti/_target."""
    lat_csr, resid, _ = mb.encode_rows(rows, sae)
    return lat_csr, resid


def _attach_window(r):
    """Attach the (_span,_ti,_target) core.encode_rows expects, given {"input","span"?,"token"?}."""
    r = dict(r)
    txt = r["input"]
    tok = r.get("token") or r.get("_target")
    span = r.get("span") or r.get("_span")
    if span is None and tok:
        i = txt.find(tok)
        span = (i, i + len(tok)) if i >= 0 else None
    r["_span"] = tuple(span) if span else None
    r["_ti"] = None
    r["_target"] = tok
    return r


def screen_token(sae, mb, token, x_windows, sibling_windows, compute_oracle=True,
                 parent_latent=None, known_absorber=None):
    """STANDALONE label-free screen for one token from raw windows (the shipped practitioner entry point).

    x_windows / sibling_windows : lists of {"input": text, "span"?: [s,e]} — windows where the token
        appears in its target parent sense (x) and windows of sibling members of the SAME parent concept.
    parent_latent : optional pinned parent/concept latent id (e.g. from Neuronpedia or a user probe). If
        given it is used as the anchor directly (the rigorous mode used by the coverage table). If omitted,
        the parent is identified UNSUPERVISED as the highest-recall latent over the SIBLING windows that
        clears a firing floor (independent of X) — an honest but conservative heuristic that can miss holes
        for concepts whose broadest co-detector also fires on the absorbed token (then it reports NO_HOLE).
    Returns the compute_signature row dict."""
    xr = [_attach_window(r) for r in x_windows]
    sr = [_attach_window(r) for r in sibling_windows]
    rows = xr + sr
    nX = len(xr)
    lat_csr, resid = _encode_windows(mb, sae, rows)
    W_dec_np = sae.W_dec.detach().cpu().numpy().astype(np.float32)
    x_idx = np.arange(nX)
    sib_idx = np.arange(nX, len(rows))
    if parent_latent is not None:
        anchor = int(parent_latent)
    else:
        # unsupervised parent = highest sibling-recall latent firing on >= floor of sibling windows
        sib_fire = np.asarray((lat_csr[sib_idx] > 0).mean(0)).ravel() if len(sib_idx) else np.zeros(lat_csr.shape[1])
        cand_anchor = np.where(sib_fire >= PARENT_FIRE_FLOOR)[0]
        anchor = int(cand_anchor[int(np.argmax(sib_fire[cand_anchor]))]) if len(cand_anchor) else -1
    # candidate absorber pool = latents that fire on X (content-responsive proxy, label-free)
    x_fire = np.asarray((lat_csr[x_idx] > 0).mean(0)).ravel() if len(x_idx) else np.zeros(lat_csr.shape[1])
    cr = np.where(x_fire > 0)[0]
    # all corpus rows act as both fit and eval here (single pool); precision pool = sibling+x rows
    sub_lab = np.array([token] * nX + ["_sibling"] * len(sib_idx), dtype=object)
    probe = None
    if compute_oracle and len(x_idx) >= 8 and len(sib_idx) >= 8:
        probe = ParentProbe(mb.torch, resid[x_idx].astype(np.float32), resid[sib_idx].astype(np.float32))
    row = compute_signature(
        token=token, hierarchy="cli", parent="cli_parent", anchor=anchor, lat_csr=lat_csr, resid=resid,
        cr=cr, fit_Xpos=x_idx, eval_Xpos=x_idx, fit_corpus=np.arange(len(rows)),
        eval_corpus_pos=np.arange(len(rows)), sub_eval=sub_lab, W_dec_np=W_dec_np, sae=sae,
        probe=probe, n_eligible=len(x_idx), known_absorber=known_absorber,
        compute_oracle=(probe is not None))
    return row


def _read_jsonl(path):
    out = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def main():
    ap = argparse.ArgumentParser(description="Label-free SAE absorption screen for one token.")
    ap.add_argument("--token", required=True)
    ap.add_argument("--windows", required=True, help="JSONL of windows containing the token (target sense)")
    ap.add_argument("--siblings", required=True, help="JSONL of sibling-concept windows (precision denom)")
    ap.add_argument("--parent_latent", type=int, default=None,
                    help="optional pinned parent/concept latent id (e.g. from Neuronpedia); else unsupervised")
    ap.add_argument("--known_absorber", type=int, default=None, help="optional pinned absorber latent id")
    ap.add_argument("--no_oracle", action="store_true")
    args = ap.parse_args()
    torch = __import__("torch")
    sae = core.load_sae(torch)
    mb = core.ModelBundle(torch)
    mb.determine_layer_idx([core._attach_span_tax(dict(r)) for r in core.load_taxonomic()
                            if r["metadata_row_type"] == "corpus"][:32], sae)
    xw = _read_jsonl(args.windows); sw = _read_jsonl(args.siblings)
    logger.info(f"screening '{args.token}': {len(xw)} target windows + {len(sw)} sibling windows"
                + (f" | pinned parent={args.parent_latent}" if args.parent_latent is not None else ""))
    row = screen_token(sae, mb, args.token, xw, sw, compute_oracle=not args.no_oracle,
                       parent_latent=args.parent_latent, known_absorber=args.known_absorber)
    print(json.dumps(row, indent=2, default=core._json_default))


if __name__ == "__main__":
    main()
