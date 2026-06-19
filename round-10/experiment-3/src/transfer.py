#!/usr/bin/env python
"""
M2''''' — GENUINE CROSS-DEPLOYMENT ZERO-LABEL TRANSFER + BREAK-EVEN K* + SELECTION-INDEPENDENT KL
         LOCALIZATION + AMAZON INSTRUMENT-DISAGREEMENT DIAGNOSIS  (iter-10).

Additive driver on the iter-9 LABEL-SCARCE engine (core.py + method.py + label_scarce.py copied VERBATIM
into this dir with only WORK changed + an additive _ls_stash_v2 transfer-partition stash on each setup_*).

WHAT WE ARE FIXING (R1). iter-9's 'where-to-gate win' was CIRCULAR: the SAE handle's absorber id is a
hard-coded constant discovered in PRIOR iterations with FULL per-sub-context labels + an oracle, while the
dense gate was restricted to n labels; worse, BOTH gates were scored on the SAME eval fold (deployment
A == deployment B), so the claimed label saving was never realized across a DIFFERENT deployment. iter-10
demonstrates GENUINE cross-deployment zero-label transfer (absorber FIXED on A; on a DISJOINT deployment B
the fixed-id SAE firing gate beats a FRESH n-label dense gate fit on B's OWN labels) and/or reports a small
break-even K* = D/n*, OR cleanly DROPS the where-to-gate thesis.

FOUR pieces:
  (A) transfer curves on B (corpus_fold_B = disjoint eval-fold halves split by doc-hash) and C
      (carrier_shift_C = fit on TEMPLATED content pairs -> deploy on NATURAL eval corpus); plus the
      same-deployment A_eval contrast (== iter-9 reproduction).
  (B) break-even K* = D_full / n* per case (D = one-time discovery labels paid on A; n* = dense labels to
      match the fixed-id SAE handle on B); also a tighter honest D_min (smallest A-subsample on which a
      precision-argmax re-discovers the SAME absorber).
  (C) selection-INDEPENDENT next-token behavioral-KL targeting (KL_X - KL_S under the absorber's firing-gated
      ablation, with a random-latent shuffle null).  $0 GPU forward.
  (D) Amazon adv_joint-vs-adv_pres instrument-disagreement diagnosis at MATCHED behavioral forget (LLM-judged).

FORK:
  REAL_WHERE_TO_GATE_SAVING : ANY powered case is TRANSFER_CONFIRMED on B (low n CI separation) OR
                              TRANSFER_VIA_BREAKEVEN (small K*) on axis corpus_fold_B.
  DROP_WHERE_TO_GATE        : neither -> publishable boundary/tool paper standing on M1''''' averted-cost +
                              localization + confinement screen (HONEST, reportable negative).

Usage:
  .venv/bin/python transfer.py --smoke
  .venv/bin/python transfer.py --cases taxonomic_georgia,named_entity_amazon --no_judge   # mini ($0)
  .venv/bin/python transfer.py                                                             # FULL
  .venv/bin/python make_variants.py method_out.json
"""
import os, sys, json, gc, argparse
from pathlib import Path

import numpy as np

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")

from core import (
    logger, el, load_sae, ModelBundle, paired_bootstrap_diff, bootstrap_mean_ci,
    set_limits, read_canonical_units, save_json, forward_pos_logprobs, kl_rows,
    DEVICE, SEED, D_MODEL, B_BOOT,
)
from method import (
    setup_first_letter, setup_named_entity, setup_taxonomic, NE_ABSORBERS,
    resolve_second_judge, PRIMARY_JUDGE,
)
import method as M
import label_scarce as LS
from label_scarce import (
    build_dense_route_at_n, sae_gate_balacc, _balacc_bootstrap, run_edit_arm,
    run_localization_arm, subsample_idx, _diffmeans_gate, _hash_n, MIN_FOR_LOGISTIC,
)

WORK = Path("/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_10/gen_art/gen_art_experiment_3")

# -------------------------------------------------------------------------- config
N_GRID_T = [1, 5, 20, "full"]          # label budgets for the dense route on a deployment
K_LOC = 30                              # label resamples for the $0 transfer localization arm
KL_SCALES = [1.0, 2.0]                  # absorber ablation strengths for the behavioral-KL targeting
KL_NULL_DRAWS = 8                       # random-latent shuffle-null draws (90th-pct permutation bar)
KL_CAP = 60                            # held-out eval rows/side used for the behavioral-KL forward
K_STAR_SMALL = 3.0                     # K* threshold below which break-even alone counts as a saving
MATERIAL_THR = 0.30                    # |forget_gap| below this (on the 0-2 scale) => IMMATERIAL (piece D)
rng = np.random.default_rng(SEED)


# ========================================================================== generalized refit over masks
def build_dense_route(torch, cs, n, seed, fit_pos, fit_sib, eval_pos, eval_sib):
    """label_scarce.build_dense_route_at_n GENERALIZED to ARBITRARY (fit,eval) index arrays into cs.ls_resid.
    Fit u_sub(n) + d_sub(n) on n rows/side sampled from (fit_pos,fit_sib) (logistic n>=5, else diff-of-means +
    midpoint); score balanced-accuracy on (eval_pos,eval_sib). Returns the iter-9-shaped dict or None."""
    if n == 0:
        return None
    pos_all = np.asarray(fit_pos); sib_all = np.asarray(fit_sib)
    if len(pos_all) == 0 or len(sib_all) == 0:
        return None
    pos_idx, cap_p = subsample_idx(pos_all, n, seed)
    sib_idx, cap_s = subsample_idx(sib_all, n, seed + 1)
    pos = cs.ls_resid[pos_idx].astype(np.float32)
    sib = cs.ls_resid[sib_idx].astype(np.float32)
    mu = pos.mean(0) - sib.mean(0)
    u = (mu / (np.linalg.norm(mu) + 1e-9)).astype(np.float32)
    u_sub_t = torch.tensor(u, device=DEVICE)
    want_logistic = (n == "full") or (n >= MIN_FOR_LOGISTIC)
    if want_logistic and len(pos) >= MIN_FOR_LOGISTIC and len(sib) >= MIN_FOR_LOGISTIC:
        try:
            from sklearn.linear_model import LogisticRegression
            X = np.concatenate([pos, sib], 0)
            y = np.concatenate([np.ones(len(pos)), np.zeros(len(sib))])
            clf = LogisticRegression(max_iter=3000, C=1.0, class_weight="balanced").fit(X, y)
            w = clf.coef_[0].astype(np.float32); b = float(clf.intercept_[0]); thr = 0.0
            gate_kind = "logistic"
        except Exception:
            w, b, thr, gate_kind = _diffmeans_gate(u, pos, sib)
    else:
        w, b, thr, gate_kind = _diffmeans_gate(u, pos, sib)
    ep = cs.ls_resid[np.asarray(eval_pos)].astype(np.float32)
    es = cs.ls_resid[np.asarray(eval_sib)].astype(np.float32)
    tpr = float(((ep @ w + b) > thr).mean()) if len(ep) else float("nan")
    tnr = float(((es @ w + b) <= thr).mean()) if len(es) else float("nan")
    balacc = 0.5 * (tpr + tnr)
    return {"u_sub_t": u_sub_t, "w_t": torch.tensor(w, device=DEVICE), "w": w, "b": b, "thr": float(thr),
            "balacc_eval": float(balacc), "tpr": float(tpr), "tnr": float(tnr), "gate_kind": gate_kind,
            "n_pos": int(len(pos)), "n_sib": int(len(sib)), "capped": bool(cap_p or cap_s)}


def sae_gate_balacc_rows(cs, eval_pos, eval_sib):
    """FLAT (n-independent) label-free SAE handle: 'fires where cs.absorber fires' on the PASSED eval rows."""
    col = np.asarray(cs.ls_lat_csr[:, cs.absorber].todense()).ravel() > 0
    ep = np.asarray(eval_pos); es = np.asarray(eval_sib)
    tpr = float(col[ep].mean()) if len(ep) else float("nan")
    tnr = float((~col[es]).mean()) if len(es) else float("nan")
    return {"balacc": 0.5 * (tpr + tnr), "tpr": tpr, "tnr": tnr,
            "n_eval_pos": int(len(ep)), "n_eval_sib": int(len(es))}


def sae_balacc_ci_rows(cs, eval_pos, eval_sib):
    col = np.asarray(cs.ls_lat_csr[:, cs.absorber].todense()).ravel() > 0
    hitX = col[np.asarray(eval_pos)].astype(float)
    missSib = (~col[np.asarray(eval_sib)]).astype(float)
    return _balacc_bootstrap(hitX, missSib)


def dense_eval_ci_rows(cs, d, eval_pos, eval_sib):
    ep = cs.ls_resid[np.asarray(eval_pos)].astype(np.float32)
    es = cs.ls_resid[np.asarray(eval_sib)].astype(np.float32)
    hitX = ((ep @ d["w"] + d["b"]) > d["thr"]).astype(float)
    missSib = ((es @ d["w"] + d["b"]) <= d["thr"]).astype(float)
    return _balacc_bootstrap(hitX, missSib)


# ========================================================================== PIECE B helper: D_min
def discovery_cost_min(cs, n_grid=(5, 10, 20, 40, 80)):
    """Tighter honest discovery cost: smallest labeled A (diagnostic) subsample on which a LABEL-FRUGAL
    precision-argmax over content-responsive latents re-discovers the SAME absorber id cs.absorber.
    precision(latent) on the subsample = (#fires on n X-pos) / (#fires on n X-pos + #fires on n siblings).
    Returns the smallest n where argmax == cs.absorber (or D_full if never), plus the per-n match trace."""
    lat = cs.ls_lat_csr
    pos_all = np.where(cs.ls_pos_mask)[0]
    sib_all = np.where(cs.ls_sib_mask)[0]
    if len(pos_all) == 0 or len(sib_all) == 0:
        return {"D_min": cs.D_full, "trace": {}, "note": "no_diag_pool"}
    # candidate latents = those that fire on >=1 diagnostic X-pos row (cheap, label-free firing set)
    fired = np.asarray((lat[pos_all] > 0).sum(0)).ravel()
    cand = np.where(fired >= 1)[0]
    fire_pos = np.asarray((lat[pos_all][:, cand] > 0).todense())   # [Npos, C]
    fire_sib = np.asarray((lat[sib_all][:, cand] > 0).todense())   # [Nsib, C]
    abs_local = int(np.where(cand == cs.absorber)[0][0]) if cs.absorber in cand else -1
    trace = {}; D_min = cs.D_full
    found = False
    for n in n_grid:
        np_ = min(n, len(pos_all)); ns_ = min(n, len(sib_all))
        # average over a few subsamples to stabilize
        matches = 0; trials = 5
        for t in range(trials):
            r = np.random.default_rng(SEED + 31 * n + t)
            pi = r.choice(len(pos_all), np_, replace=False)
            si = r.choice(len(sib_all), ns_, replace=False)
            fp = fire_pos[pi].sum(0).astype(float); fs = fire_sib[si].sum(0).astype(float)
            prec = np.where((fp + fs) > 0, fp / np.maximum(fp + fs, 1), 0.0)
            # K-track-lite re-discovery: among PRECISE latents (prec>=0.7, >=2 X-fires) pick MAX coverage (X-fires)
            elig = np.where((prec >= 0.70) & (fp >= 2))[0]
            arg = int(elig[np.argmax(fp[elig])]) if len(elig) else -1
            if arg == abs_local:
                matches += 1
        rate = matches / trials
        trace[str(n)] = {"match_rate": rate, "n_pos": np_, "n_sib": ns_}
        if rate >= 0.6 and not found:
            D_min = int(2 * n); found = True                       # n per side -> 2n labels
    return {"D_min": D_min, "trace": trace, "absorber_in_candidates": bool(abs_local >= 0),
            "rediscovered": found}


# ========================================================================== PIECES A+B: transfer arm
def transfer_arm(torch, cs, axis):
    """For deployment `axis`: the FLAT label-free fixed-id SAE handle (zero deployment labels) vs the dense
    fair gate fit FRESH on n deployment labels, scored on the deployment's own held-out eval. Returns the
    transfer curve, n_breakeven, D_full/D_min, and K*."""
    if axis == "corpus_fold_B":
        fit_pos, fit_sib = cs.lsB_fit_pos, cs.lsB_fit_sib
        eval_pos, eval_sib = cs.lsB_eval_pos, cs.lsB_eval_sib
        powered = bool(cs.transfer_powered_B)
    elif axis == "carrier_shift_C":
        fit_pos, fit_sib = cs.lsC_fit_pos, cs.lsC_fit_sib
        eval_pos, eval_sib = cs.lsC_eval_pos, cs.lsC_eval_sib
        powered = bool(cs.transfer_powered_C)
    else:
        raise ValueError(axis)

    sae = sae_gate_balacc_rows(cs, eval_pos, eval_sib)
    sae_lo, sae_hi = sae_balacc_ci_rows(cs, eval_pos, eval_sib)

    dense_curve = {}
    for n in N_GRID_T:
        if n == "full":
            d = build_dense_route(torch, cs, "full", SEED, fit_pos, fit_sib, eval_pos, eval_sib)
            if d is None:
                continue
            lo, hi = dense_eval_ci_rows(cs, d, eval_pos, eval_sib)
            dense_curve["full"] = {"value": d["balacc_eval"], "ci_lo": lo, "ci_hi": hi, "tpr": d["tpr"],
                                   "tnr": d["tnr"], "n_resamples": 1, "gate_kind": d["gate_kind"],
                                   "capped": bool(d["capped"]), "n_pos": d["n_pos"], "n_sib": d["n_sib"]}
            continue
        vals, ds = [], []
        for k in range(K_LOC):
            d = build_dense_route(torch, cs, n, SEED + 1000 * _hash_n(n) + 7 * k,
                                  fit_pos, fit_sib, eval_pos, eval_sib)
            if d is None:
                continue
            vals.append(d["balacc_eval"]); ds.append(d)
        if not vals:
            continue
        point = float(np.mean(vals))
        if np.std(vals) < 1e-9:
            lo, hi = dense_eval_ci_rows(cs, ds[-1], eval_pos, eval_sib)
        else:
            lo, hi = float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))
        dense_curve[n] = {"value": point, "ci_lo": lo, "ci_hi": hi, "n_resamples": len(vals),
                          "gate_kind": ds[-1]["gate_kind"], "capped": bool(ds[-1]["capped"]),
                          "mean_tpr": float(np.mean([d["tpr"] for d in ds])),
                          "mean_tnr": float(np.mean([d["tnr"] for d in ds]))}

    # n_breakeven = smallest n whose dense CI OVERLAPS the SAE flat value (dense "catches up")
    sep, n_breakeven = {}, None
    for n in N_GRID_T:
        if n not in dense_curve:
            continue
        dc = dense_curve[n]
        overlap = not (dc["ci_hi"] < sae_lo or dc["ci_lo"] > sae_hi)
        sep[str(n)] = {"overlap": bool(overlap), "dense_below_sae": bool(dc["ci_hi"] < sae_lo)}
        if overlap and n_breakeven is None:
            n_breakeven = n

    D_full = int(cs.D_full)
    n_star = n_breakeven if isinstance(n_breakeven, int) else None
    K_star = (D_full / max(n_star, 1)) if n_star else None
    n5 = dense_curve.get(5, {}).get("value")
    n1_gate = dense_curve.get(1, {}).get("gate_kind")
    n1_artifact = bool(n1_gate == "diffmeans_midpoint")

    low_n_sep = any(sep.get(str(n), {}).get("dense_below_sae") for n in (1, 5))
    sae_strong = bool(np.isfinite(sae["balacc"]) and sae["balacc"] >= 0.70)
    if not powered:
        verdict = "UNDERPOWERED"
    elif not sae_strong:
        verdict = "SAE_WEAK_DESCRIPTIVE"
    elif low_n_sep:
        verdict = "TRANSFER_CONFIRMED"
    elif (n_star is not None and n_star >= 5 and K_star is not None and K_star <= K_STAR_SMALL):
        verdict = "TRANSFER_VIA_BREAKEVEN"
    else:
        verdict = "NO_TRANSFER"

    return {"axis": axis, "powered": powered, "sae": {"value": sae["balacc"], "ci_lo": sae_lo, "ci_hi": sae_hi,
            "tpr": sae["tpr"], "tnr": sae["tnr"], "n_eval_pos": sae["n_eval_pos"], "n_eval_sib": sae["n_eval_sib"]},
            "dense": dense_curve, "ci_separation": sep, "n_breakeven": n_breakeven, "K_star": K_star,
            "D_full": D_full, "n_star": n_star, "n5_honest": n5, "n1_midpoint_artifact": n1_artifact,
            "verdict": verdict,
            "fit_pool": {"n_fit_pos": int(len(fit_pos)), "n_fit_sib": int(len(fit_sib))}}


# ========================================================================== PIECE C: behavioral-KL targeting
def _two_sample_boot(a, b, B=B_BOOT):
    a = np.asarray(a, float); b = np.asarray(b, float)
    if len(a) == 0 or len(b) == 0:
        return {"diff": 0.0, "ci_lo": 0.0, "ci_hi": 0.0, "excl_0": False}
    ia = rng.integers(0, len(a), size=(B, len(a))); ib = rng.integers(0, len(b), size=(B, len(b)))
    d = a[ia].mean(1) - b[ib].mean(1)
    lo, hi = np.percentile(d, [2.5, 97.5])
    return {"diff": float(a.mean() - b.mean()), "ci_lo": float(lo), "ci_hi": float(hi),
            "excl_0": bool(lo > 0 or hi < 0)}


def kl_targeting(torch, sae, mb, cs, scales=KL_SCALES, n_null=KL_NULL_DRAWS):
    """SELECTION-INDEPENDENT next-token behavioral-KL TARGETING on HELD-OUT eval rows (disjoint from the
    diagnostic fold the absorber was SELECTED on). The absorber was chosen by FIRING precision (~ balacc);
    behavioral KL is a DIFFERENT axis (the downstream next-token effect of ablating it). targeting =
    mean(KL_X) - mean(KL_S) > 0 == localized behavioral effect; compared to a RANDOM content-responsive
    latent shuffle null. metadata states the balacc ~ firing-precision coincidence explicitly."""
    posrows = cs.kl_pos_rows[:KL_CAP]; sibrows = cs.kl_sib_rows[:KL_CAP]
    if len(posrows) < 8 or len(sibrows) < 8:
        return {"status": "underpowered", "n_pos": len(posrows), "n_sib": len(sibrows)}
    baseX, _ = forward_pos_logprobs(mb, sae, posrows)
    baseS, _ = forward_pos_logprobs(mb, sae, sibrows)
    rand_lats = [int(x) for x in (cs.rand_latents or [])][:n_null]
    by_scale = {}
    for sc in scales:
        editX, _ = forward_pos_logprobs(mb, sae, posrows, kind="abl_latent", l=int(cs.absorber), scale=sc)
        editS, _ = forward_pos_logprobs(mb, sae, sibrows, kind="abl_latent", l=int(cs.absorber), scale=sc)
        KLX = kl_rows(editX, baseX); KLS = kl_rows(editS, baseS)
        targeting = float(KLX.mean() - KLS.mean())
        ci = _two_sample_boot(KLX, KLS)
        nulls = []
        for rl in rand_lats:
            eX, _ = forward_pos_logprobs(mb, sae, posrows, kind="abl_latent", l=rl, scale=sc)
            eS, _ = forward_pos_logprobs(mb, sae, sibrows, kind="abl_latent", l=rl, scale=sc)
            nulls.append(float(kl_rows(eX, baseX).mean() - kl_rows(eS, baseS).mean()))
        null_mean = float(np.mean(nulls)) if nulls else 0.0
        null_hi = float(np.max(nulls)) if nulls else 0.0
        # robust empirical-null bar: 90th percentile of the random-latent shuffle null (stable as draws grow,
        # unlike max-of-N). frac_null_ge = one-sided permutation p-value (fraction of random latents that match
        # or beat the absorber's targeting).
        null_p90 = float(np.percentile(nulls, 90)) if nulls else 0.0
        frac_null_ge = (float(np.mean([1.0 if x >= targeting else 0.0 for x in nulls])) if nulls else 1.0)
        localized = bool(targeting > 0 and ci["excl_0"] and targeting > null_p90 and frac_null_ge <= 0.10)
        by_scale[str(sc)] = {"targeting": targeting, "ci_lo": ci["ci_lo"], "ci_hi": ci["ci_hi"],
                             "excl_0": ci["excl_0"], "KL_X_mean": float(KLX.mean()),
                             "KL_S_mean": float(KLS.mean()), "null_mean": null_mean, "null_p90": null_p90,
                             "null_hi": null_hi, "frac_null_ge_targeting": frac_null_ge,
                             "null_draws": [round(x, 5) for x in nulls], "n_null": len(nulls),
                             "verdict": ("KL_LOCALIZED" if localized else "KL_NULL_DESCRIPTIVE")}
        logger.info(f"{el()} KL {cs.case_id} scale={sc}: targeting={targeting:.4f} ci=[{ci['ci_lo']:.4f},"
                    f"{ci['ci_hi']:.4f}] null_p90={null_p90:.4f} null_hi={null_hi:.4f} frac_ge={frac_null_ge:.2f}"
                    f" -> {by_scale[str(sc)]['verdict']}")
    any_loc = any(v["verdict"] == "KL_LOCALIZED" for v in by_scale.values())
    return {"status": "ok", "n_pos": len(posrows), "n_sib": len(sibrows), "rand_latents": rand_lats,
            "by_scale": by_scale, "verdict": ("KL_LOCALIZED" if any_loc else "KL_NULL_DESCRIPTIVE"),
            "selection_caveat": ("balanced-accuracy ~ the firing-precision selection criterion; the "
                                 "localization claim leans on held-out generalization (eval fold, disjoint "
                                 "from the diagnostic fold the absorber was selected on) + this "
                                 "selection-independent behavioral-KL targeting.")}


# ========================================================================== PIECE D: Amazon caveat
def amazon_caveat(torch, sae, mb, cs, edit_args, second_judge):
    """Diagnose the iter-9 Amazon adv_joint(+0.52)-vs-adv_pres(~0) instrument disagreement at the MATCHED
    behavioral-forget point on HELD-OUT FORGET probes. Reuse run_edit_arm (n_grid=['full']) -> extract the
    FORGET-role judged forget quality for KG vs the FULL fair gate; forget_gap = fq_kg - fq_fair with a
    paired bootstrap CI; materiality threshold MATERIAL_THR on the 0-2 scale."""
    r = run_edit_arm(torch, mb, sae, cs, edit_args, second_judge)
    if r.get("status") != "ok":
        return {"status": r.get("status"), "edit": r}
    cv = r["curve"].get("full", {})
    fq_kg = r.get("forget_quality_kg"); fq_fair = cv.get("forget_quality_fair")
    gen = r["gen"]; judged = r["judged"]
    op_fair = (r["fair_meta"].get("full") or [{}])[0].get("opname")
    kgF = [j["content_pres"] for j in judged.get("FORGET", {}).get("KG-ABL", []) if j is not None]
    faF = ([j["content_pres"] for j in judged.get("FORGET", {}).get(op_fair, []) if j is not None]
           if op_fair else [])
    m = min(len(kgF), len(faF))
    gap_ci = paired_bootstrap_diff(np.array(kgF[:m]), np.array(faF[:m])) if m >= 4 else None
    forget_gap = (fq_kg - fq_fair) if (fq_kg is not None and fq_fair is not None) else None
    both_forget = bool(fq_kg is not None and fq_fair is not None and fq_kg >= 1.0 and fq_fair >= 1.0)
    immaterial = bool(forget_gap is not None and abs(forget_gap) < MATERIAL_THR)
    verdict = "ISOLATED_IMMATERIAL" if immaterial else "MATERIAL_REPORT_BOTH"
    adv_pres = cv.get("adv_pres") or {}; adv_joint = cv.get("adv_joint") or {}
    logger.info(f"{el()} AMAZON-CAVEAT {cs.case_id}: fq_kg={fq_kg} fq_fair={fq_fair} gap={forget_gap} "
                f"both_forget={both_forget} -> {verdict}")
    return {"status": "ok", "fq_kg": fq_kg, "fq_fair": fq_fair, "forget_gap": forget_gap,
            "forget_gap_ci": gap_ci, "both_forget_well": both_forget, "material_threshold": MATERIAL_THR,
            "adv_pres": {"diff": adv_pres.get("diff"), "ci_lo": adv_pres.get("ci_lo"),
                         "ci_hi": adv_pres.get("ci_hi"), "excl_0": adv_pres.get("excl_0")},
            "adv_joint": {"diff": adv_joint.get("diff"), "ci_lo": adv_joint.get("ci_lo"),
                          "ci_hi": adv_joint.get("ci_hi"), "excl_0": adv_joint.get("excl_0")},
            "adv_joint_full_offset": r.get("adv_joint_full_offset"), "verdict": verdict, "edit": r}


# ========================================================================== aggregate + fork
def aggregate(transferB, transferC, kl_res):
    confirmed = [cid for cid, r in transferB.items()
                 if r.get("verdict") in ("TRANSFER_CONFIRMED", "TRANSFER_VIA_BREAKEVEN")]
    overall = "REAL_WHERE_TO_GATE_SAVING" if confirmed else "DROP_WHERE_TO_GATE"
    tallyB, tallyC, tallyKL = {}, {}, {}
    for cid, r in transferB.items():
        tallyB.setdefault(r["verdict"], []).append(cid)
    for cid, r in transferC.items():
        tallyC.setdefault(r["verdict"], []).append(cid)
    for cid, r in kl_res.items():
        tallyKL.setdefault(r.get("verdict", r.get("status")), []).append(cid)
    return {"overall_transfer_fork_verdict": overall, "transfer_confirmed_on_B": confirmed,
            "transferB_tally": tallyB, "transferC_tally": tallyC, "kl_tally": tallyKL}


def build_honest_negatives(agg, transferB, transferC, kl_res, amazon_res):
    neg = []
    if agg["overall_transfer_fork_verdict"] == "DROP_WHERE_TO_GATE":
        neg.append("DROP_WHERE_TO_GATE (publishable honest negative): on the genuine cross-deployment test B "
                   "(absorber FIXED on A, dense gate fit fresh on B's OWN labels, both scored on a DISJOINT "
                   "B_eval) NO powered case is TRANSFER_CONFIRMED and all break-even K* are large -> no "
                   "realized SAE-specific where-to-gate label saving. The paper stands on the M1''''' "
                   "averted-cost capability + localization + the confinement screen + the absorber catalog.")
    for cid, r in transferB.items():
        if r["verdict"] == "UNDERPOWERED":
            neg.append(f"{cid} (corpus_fold_B): UNDERPOWERED — the eval-fold doc-hash split leaves "
                       f"B_eval_pos={r['sae']['n_eval_pos']} (<10) / fit_pos={r['fit_pool']['n_fit_pos']}; "
                       f"the decisive transfer claim rests on the corpus-rich powered cases (carrier_shift_C "
                       f"reported descriptively for this case).")
        if r["verdict"] == "SAE_WEAK_DESCRIPTIVE":
            neg.append(f"{cid} (corpus_fold_B): the fixed-id SAE firing gate has LOW balanced-accuracy "
                       f"({r['sae']['value']:.3f}) on this DISTRIBUTED sense at deployment B — descriptive "
                       f"localization point only; no transfer-saving claim.")
        if r["verdict"] == "NO_TRANSFER":
            neg.append(f"{cid} (corpus_fold_B): the dense gate MATCHES the fixed-id SAE handle even at low n "
                       f"on the held-out deployment B (n_breakeven={r['n_breakeven']}, K*={r['K_star']}) — no "
                       f"SAE-specific saving for this case.")
    for cid, r in kl_res.items():
        if r.get("verdict") == "KL_NULL_DESCRIPTIVE" and r.get("status") == "ok":
            neg.append(f"{cid} (behavioral-KL): single-absorber ablation has NO localized next-token effect "
                       f"(targeting CI includes 0 or <= the random-latent null) — an HONEST split: firing "
                       f"balanced-accuracy localizes this sense, but behavioral-KL localizes only where the "
                       f"sense is lexically CONCENTRATED. The localization claim rests on firing-balacc + "
                       f"held-out generalization for this case.")
    for cid, r in amazon_res.items():
        if r.get("status") != "ok":
            continue
        if r.get("verdict") == "MATERIAL_REPORT_BOTH":
            neg.append(f"{cid} (edit, honest caveat): at MATCHED behavioral forget the judged forget gap "
                       f"(KG - fair = {r.get('forget_gap')}) EXCEEDS {MATERIAL_THR} -> report BOTH adv_pres "
                       f"and adv_joint and SOFTEN 'demonstrated' to 'preservation-advantage-only at matched "
                       f"forget' for the Amazon edit arm.")
        elif r.get("verdict") == "ISOLATED_IMMATERIAL":
            neg.append(f"{cid} (edit, honest caveat): the iter-9 adv_joint full-offset is ISOLATED and "
                       f"IMMATERIAL — both routes forget well (fq_kg={r.get('fq_kg')}, fq_fair={r.get('fq_fair')}) "
                       f"and the residual judged forget gap ({r.get('forget_gap')}) is below {MATERIAL_THR}; "
                       f"adv_pres (preservation at matched forget) stands as primary, 'demonstrated' kept.")
    return neg


# ========================================================================== output assembly
def _s(x, n=300):
    s = "" if x is None else str(x)
    return s if len(s) <= n else s[:n]


def _rnd(x, k=4):
    try:
        return _s(round(float(x), k))
    except (TypeError, ValueError):
        return "NA"


def assemble_outputs(out, A_eval, transferB, transferC, kl_res, amazon_res):
    rows = []

    def _emit_deploy(cid, axis, dep, r):
        sae = r["sae"]
        rows.append({
            "input": f"[transfer|{cid}|{axis}|gate_balacc|{dep}] fixed-id SAE absorber-firing gate (0 deploy labels)",
            "output": r["verdict"],
            "predict_value": _rnd(sae["value"]), "predict_ci_lo": _rnd(sae["ci_lo"]),
            "predict_ci_hi": _rnd(sae["ci_hi"]),
            "metadata_case": cid, "metadata_axis": axis, "metadata_deployment": dep, "metadata_metric": "gate_balacc",
            "metadata_route": "SAE", "metadata_n": "flat", "metadata_label_free": True,
            "metadata_balacc_tpr": round(sae["tpr"], 4), "metadata_balacc_tnr": round(sae["tnr"], 4),
            "metadata_n_eval_pos": sae["n_eval_pos"], "metadata_n_eval_sib": sae["n_eval_sib"],
            "metadata_powered": r["powered"], "metadata_verdict": r["verdict"],
            "metadata_n_breakeven": _s(r["n_breakeven"]), "metadata_K_star": _s(r.get("K_star")),
            "metadata_D_full": r.get("D_full"), "metadata_D_min": r.get("D_min"),
            "metadata_n5_honest": _s(r.get("n5_honest")), "metadata_n1_midpoint_artifact": r.get("n1_midpoint_artifact"),
        })
        for n, dc in r["dense"].items():
            rows.append({
                "input": f"[transfer|{cid}|{axis}|gate_balacc|{dep}] dense fair d_sub-gate fit on n={n} deploy labels",
                "output": r["verdict"],
                "predict_value": _rnd(dc["value"]), "predict_ci_lo": _rnd(dc["ci_lo"]),
                "predict_ci_hi": _rnd(dc["ci_hi"]),
                "metadata_case": cid, "metadata_axis": axis, "metadata_deployment": dep,
                "metadata_metric": "gate_balacc", "metadata_route": "DENSE", "metadata_n": _s(n),
                "metadata_n_resamples": dc["n_resamples"], "metadata_gate_kind": dc.get("gate_kind"),
                "metadata_capped": dc.get("capped"),
                "metadata_dense_below_sae": r["ci_separation"].get(str(n), {}).get("dense_below_sae"),
                "metadata_overlaps_sae": r["ci_separation"].get(str(n), {}).get("overlap"),
                "metadata_verdict": r["verdict"],
            })

    # A_eval contrast (== iter-9 reproduction): SAE flat + dense per-n on the SAME eval fold
    for cid, la in A_eval.items():
        sp = la["sae"]
        rows.append({
            "input": f"[transfer|{cid}|same_deployment_A|gate_balacc|A_eval] fixed-id SAE handle (iter-9 reproduction)",
            "output": la["verdict"],
            "predict_value": _rnd(sp["value"]), "predict_ci_lo": _rnd(sp["ci_lo"]), "predict_ci_hi": _rnd(sp["ci_hi"]),
            "metadata_case": cid, "metadata_axis": "same_deployment_A", "metadata_deployment": "A_eval",
            "metadata_metric": "gate_balacc", "metadata_route": "SAE", "metadata_n": "flat",
            "metadata_balacc_tpr": round(sp["tpr"], 4), "metadata_balacc_tnr": round(sp["tnr"], 4),
            "metadata_label_free": True, "metadata_iter9_contrast": True, "metadata_verdict": la["verdict"],
            "metadata_n_breakeven": _s(la["n_breakeven"]),
        })
        for n, dc in la["dense"].items():
            rows.append({
                "input": f"[transfer|{cid}|same_deployment_A|gate_balacc|A_eval] dense gate fit on diagnostic n={n} (iter-9)",
                "output": la["verdict"],
                "predict_value": _rnd(dc["value"]), "predict_ci_lo": _rnd(dc["ci_lo"]), "predict_ci_hi": _rnd(dc["ci_hi"]),
                "metadata_case": cid, "metadata_axis": "same_deployment_A", "metadata_deployment": "A_eval",
                "metadata_metric": "gate_balacc", "metadata_route": "DENSE", "metadata_n": _s(n),
                "metadata_n_resamples": dc["n_resamples"], "metadata_gate_kind": dc.get("gate_kind"),
                "metadata_dense_below_sae": la["ci_separation"].get(str(n), {}).get("dense_below_sae"),
                "metadata_overlaps_sae": la["ci_separation"].get(str(n), {}).get("overlap"),
                "metadata_iter9_contrast": True, "metadata_verdict": la["verdict"],
            })

    for cid, r in transferB.items():
        _emit_deploy(cid, "corpus_fold_B", "B_corpus", r)
    for cid, r in transferC.items():
        _emit_deploy(cid, "carrier_shift_C", "C_carrier", r)

    # KL targeting rows
    for cid, r in kl_res.items():
        if r.get("status") != "ok":
            rows.append({"input": f"[kl_targeting|{cid}] status", "output": r.get("status"),
                         "predict_value": _s(r.get("status")), "predict_ci_lo": "NA", "predict_ci_hi": "NA",
                         "metadata_case": cid, "metadata_metric": "kl_targeting", "metadata_route": "SAE"})
            continue
        for sc, v in r["by_scale"].items():
            rows.append({
                "input": f"[kl_targeting|{cid}|scale={sc}] next-token KL(absorbed X) - KL(sibling) under absorber ablation",
                "output": v["verdict"],
                "predict_value": _rnd(v["targeting"]), "predict_ci_lo": _rnd(v["ci_lo"]), "predict_ci_hi": _rnd(v["ci_hi"]),
                "metadata_case": cid, "metadata_metric": "kl_targeting", "metadata_route": "SAE",
                "metadata_scale": sc, "metadata_kl_x_mean": round(v["KL_X_mean"], 5),
                "metadata_kl_s_mean": round(v["KL_S_mean"], 5), "metadata_kl_null_mean": round(v["null_mean"], 5),
                "metadata_kl_null_p90": round(v.get("null_p90", 0.0), 5), "metadata_kl_null_hi": round(v["null_hi"], 5),
                "metadata_frac_null_ge": v.get("frac_null_ge_targeting"), "metadata_n_null": v.get("n_null"),
                "metadata_excl_0": v["excl_0"], "metadata_kl_verdict": v["verdict"],
                "metadata_selection_independent": True,
            })

    # Amazon / large caveat rows
    for cid, r in amazon_res.items():
        if r.get("status") != "ok":
            rows.append({"input": f"[amazon_caveat|{cid}] status", "output": _s(r.get("status")),
                         "predict_value": _s(r.get("status")), "predict_ci_lo": "NA", "predict_ci_hi": "NA",
                         "metadata_case": cid, "metadata_metric": "instrument_disagreement", "metadata_route": "STATUS"})
            continue
        ap = r["adv_pres"]; aj = r["adv_joint"]; gc_ = r.get("forget_gap_ci") or {}
        rows.append({
            "input": f"[amazon_caveat|{cid}|instrument_disagreement] judged FORGET gap KG-ABL minus dense fair (matched forget)",
            "output": r["verdict"],
            "predict_value": _rnd(r.get("forget_gap")), "predict_ci_lo": _rnd(gc_.get("ci_lo")),
            "predict_ci_hi": _rnd(gc_.get("ci_hi")),
            "metadata_case": cid, "metadata_metric": "instrument_disagreement", "metadata_route": "DIAGNOSTIC",
            "metadata_fq_kg": r.get("fq_kg"), "metadata_fq_fair": r.get("fq_fair"),
            "metadata_both_forget_well": r.get("both_forget_well"), "metadata_material_threshold": MATERIAL_THR,
            "metadata_adv_pres_diff": ap.get("diff"), "metadata_adv_pres_excl0": ap.get("excl_0"),
            "metadata_adv_joint_diff": aj.get("diff"), "metadata_adv_joint_excl0": aj.get("excl_0"),
            "metadata_adv_joint_full_offset": r.get("adv_joint_full_offset"), "metadata_verdict": r["verdict"],
        })

    # edit_per_prompt continuations (Amazon + large re-judge)
    epp = []
    for cid, r in amazon_res.items():
        if r.get("status") != "ok":
            continue
        ed = r["edit"]; gen = ed["gen"]; judged = ed["judged"]; judged2 = ed.get("judged2") or {}
        op_fair = (ed["fair_meta"].get("full") or [{}])[0].get("opname")
        for role in ed["roles"]:
            g = gen[role]
            jr_kg = judged.get(role, {}).get("KG-ABL", [])
            jr_f = judged.get(role, {}).get(op_fair, []) if op_fair else []
            jr_kg2 = judged2.get(role, {}).get("KG-ABL", []) if judged2 else []
            for j, p in enumerate(g["prompts"]):
                jk = jr_kg[j] if j < len(jr_kg) else None
                jf = jr_f[j] if j < len(jr_f) else None
                jk2 = jr_kg2[j] if j < len(jr_kg2) else None
                epp.append({
                    "input": f"[{cid}|n=full|{role}] {_s(p, 240)}",
                    "output": role,
                    "predict_kg_abl": _s((g.get("KG-ABL") or [""] * (j + 1))[j] or "EMPTY", 200),
                    "predict_dense_fair": _s((g.get(op_fair) or [""] * (j + 1))[j] if op_fair else "EMPTY", 200) or "EMPTY",
                    "predict_noop": _s((g.get("NOOP") or [""] * (j + 1))[j] or "EMPTY", 200),
                    "metadata_case": cid, "metadata_role": role,
                    "metadata_judge_primary_fluency_kg": (jk["fluency"] if jk else None),
                    "metadata_judge_primary_content_pres_kg": (jk["content_pres"] if jk else None),
                    "metadata_judge_primary_fluency_fair": (jf["fluency"] if jf else None),
                    "metadata_judge_primary_content_pres_fair": (jf["content_pres"] if jf else None),
                    "metadata_judge_second_content_pres_kg": (jk2["content_pres"] if jk2 else None),
                    "metadata_kg_beta": round(ed["kg_beta"], 4), "metadata_matched_target": round(ed["matched_target"], 4),
                })

    if not rows:
        rows = [{"input": "none", "output": "NONE", "predict_value": "NONE"}]
    if not epp:
        epp = [{"input": "none", "output": "NONE", "predict_kg_abl": "NONE"}]
    out["datasets"] = [
        {"dataset": "transfer_curve", "examples": rows},
        {"dataset": "edit_per_prompt", "examples": epp},
    ]


# ========================================================================== MAIN
class _Args:
    pass


def _parse_cases(s):
    return [c.strip() for c in s.split(",") if c.strip()]


def main():
    global K_LOC
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default="taxonomic_georgia,taxonomic_jordan,taxonomic_us,"
                                       "named_entity_amazon,first_letter_large")
    ap.add_argument("--edit_cases", default="named_entity_amazon,first_letter_large")
    ap.add_argument("--axes", default="corpus_fold_B,carrier_shift_C")
    ap.add_argument("--K_LOC", type=int, default=K_LOC)
    ap.add_argument("--kl_null", type=int, default=KL_NULL_DRAWS)
    ap.add_argument("--cap", type=int, default=150)
    ap.add_argument("--gen_per_set", type=int, default=8)
    ap.add_argument("--K_EDIT", type=int, default=4)
    ap.add_argument("--second_judge_cap", type=int, default=16)
    ap.add_argument("--no_kl", action="store_true")
    ap.add_argument("--no_judge", action="store_true")
    ap.add_argument("--no_second_judge", action="store_true")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--out", default=str(WORK / "method_out.json"))
    a = ap.parse_args()
    set_limits()
    K_LOC = a.K_LOC

    import torch
    torch.manual_seed(SEED)
    if torch.cuda.is_available():
        try:
            torch.cuda.set_per_process_memory_fraction(0.85)
        except Exception:
            pass
    logger.info(f"{el()} torch {torch.__version__} cuda={torch.cuda.is_available()} device={DEVICE}")

    sae = load_sae(torch)
    mb = ModelBundle(torch)
    canon = read_canonical_units()
    gating, Rnorm, tax_rows = M.gating_check(torch, sae, mb)

    setup_args = _Args()
    setup_args.cap = a.cap; setup_args.gen_per_set = a.gen_per_set
    setup_args.forget_cap = 40; setup_args.retain_collat_cap = 150
    setup_args.retain_curve_cap = 60; setup_args.unrel_curve_cap = 40

    setup_fns = {
        "first_letter_large": setup_first_letter,
        "named_entity_amazon": lambda *x: setup_named_entity(*x, entity="Amazon",
                                  hard_absorber=NE_ABSORBERS["Amazon"], case_id="named_entity_amazon", run_m7=False),
        "taxonomic_georgia": lambda *x: setup_taxonomic(*x, target=("Georgia", 16009, 0.955),
                                  case_id="taxonomic_georgia", regime="absorption"),
        "taxonomic_jordan": lambda *x: setup_taxonomic(*x, target=("Jordan", 540, 0.975),
                                  case_id="taxonomic_jordan", regime="absorption"),
        "taxonomic_us": lambda *x: setup_taxonomic(*x, target=("United States", 846, 0.973),
                                  case_id="taxonomic_us", regime="co-firing"),
    }

    if a.smoke:
        run_smoke(torch, sae, mb, canon, setup_args)
        return

    axes = [x.strip() for x in a.axes.split(",") if x.strip()]
    cases = _parse_cases(a.cases)
    edit_cases = set(_parse_cases(a.edit_cases)) if not a.no_judge else set()

    second_judge = None
    if not a.no_judge and not a.no_second_judge:
        second_judge = resolve_second_judge()
        if second_judge is None:
            logger.warning(f"{el()} second judge UNAVAILABLE — edit-arm robustness primary-only")

    A_eval, transferB, transferC, kl_res, amazon_res, dmin_res = {}, {}, {}, {}, {}, {}
    n_grid_A = [0, 1, 5, 20, "full"]
    for cid in cases:
        if cid not in setup_fns:
            logger.warning(f"unknown case {cid}; skip"); continue
        try:
            cs = setup_fns[cid](torch, sae, mb, canon, setup_args, Rnorm)
        except Exception as e:  # noqa: BLE001
            logger.exception(f"setup failed for {cid}: {e}"); continue
        if cs is None or getattr(cs, "ls_resid", None) is None:
            logger.warning(f"{cid}: no transfer stash; skip"); continue
        assert cs.ls_fold_disjoint and cs.transfer_disjoint, f"{cid}: NON-DISJOINT folds (transfer invalid)"
        # A_eval contrast (iter-9 reproduction)
        try:
            A_eval[cid] = run_localization_arm(torch, cs, n_grid_A, a.K_LOC)
        except Exception as e:  # noqa: BLE001
            logger.exception(f"A_eval failed {cid}: {e}")
        # D_min
        try:
            dmin_res[cid] = discovery_cost_min(cs)
        except Exception as e:  # noqa: BLE001
            logger.exception(f"D_min failed {cid}: {e}"); dmin_res[cid] = {"D_min": cs.D_full}
        # transfer arms
        if "corpus_fold_B" in axes:
            try:
                transferB[cid] = transfer_arm(torch, cs, "corpus_fold_B")
                transferB[cid]["D_min"] = dmin_res[cid].get("D_min")
                if transferB[cid].get("n_star"):
                    transferB[cid]["K_star_dmin"] = dmin_res[cid].get("D_min") / max(transferB[cid]["n_star"], 1)
                logger.info(f"{el()} TRANSFER-B {cid}: verdict={transferB[cid]['verdict']} "
                            f"sae={transferB[cid]['sae']['value']:.3f} n*={transferB[cid]['n_breakeven']} "
                            f"K*={transferB[cid]['K_star']}")
            except Exception as e:  # noqa: BLE001
                logger.exception(f"transfer-B failed {cid}: {e}")
        if "carrier_shift_C" in axes:
            try:
                transferC[cid] = transfer_arm(torch, cs, "carrier_shift_C")
                transferC[cid]["D_min"] = dmin_res[cid].get("D_min")
                logger.info(f"{el()} TRANSFER-C {cid}: verdict={transferC[cid]['verdict']} "
                            f"sae={transferC[cid]['sae']['value']:.3f} n*={transferC[cid]['n_breakeven']}")
            except Exception as e:  # noqa: BLE001
                logger.exception(f"transfer-C failed {cid}: {e}")
        # KL targeting
        if not a.no_kl:
            try:
                kl_res[cid] = kl_targeting(torch, sae, mb, cs, n_null=a.kl_null)
            except Exception as e:  # noqa: BLE001
                logger.exception(f"KL failed {cid}: {e}")
        # Amazon caveat (edit)
        if cid in edit_cases and M.SPENT["usd"] < M.TARGET:
            edit_args = _Args()
            edit_args.n_grid = ["full"]; edit_args.K_EDIT = a.K_EDIT; edit_args.gen_per_set = a.gen_per_set
            edit_args.second_judge_cap = a.second_judge_cap
            try:
                amazon_res[cid] = amazon_caveat(torch, sae, mb, cs, edit_args, second_judge)
                logger.info(f"{el()} CAVEAT {cid}: {amazon_res[cid].get('verdict')} SPENT=${M.SPENT['usd']:.4f}")
            except Exception as e:  # noqa: BLE001
                logger.exception(f"amazon_caveat failed {cid}: {e}")
                amazon_res[cid] = {"status": f"error:{e}"}
        del cs
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    agg = aggregate(transferB, transferC, kl_res)
    honest = build_honest_negatives(agg, transferB, transferC, kl_res, amazon_res)

    out = {"metadata": {
        "experiment": "M2prime5_genuine_cross_deployment_zero_label_transfer",
        "method_name": "M2''''' Genuine Cross-Deployment Zero-Label Transfer + Break-Even K* + "
                       "Selection-Independent KL Localization + Amazon Caveat",
        "description": ("Fix the SAE absorber id ONCE on deployment A (diagnostic fold; discovered with full "
                        "labels+oracle in prior iters); on a DISJOINT deployment B (eval-fold halves split by "
                        "doc-hash) + a template->natural carrier-shift deployment C, score the n-INDEPENDENT "
                        "fixed-id SAE firing gate vs an n-label dense gate fit FRESH on the deployment's OWN "
                        "labels. Net out the one-time discovery cost D and report break-even K*=D/n*. Add the "
                        "selection-independent next-token behavioral-KL targeting (random-latent null) and "
                        "diagnose the Amazon adv_joint-vs-adv_pres instrument disagreement at matched forget."),
        "overall_transfer_fork_verdict": agg["overall_transfer_fork_verdict"],
        "transfer_confirmed_on_B": agg["transfer_confirmed_on_B"],
        "transferB_tally": agg["transferB_tally"], "transferC_tally": agg["transferC_tally"],
        "kl_tally": agg["kl_tally"],
        "r1_fix": ("GENUINE cross-deployment: the dense gate is fit FRESH on B's OWN labels and BOTH gates are "
                   "scored on a B_eval DISJOINT from the A discovery fold AND from B_fit — so the label saving "
                   "is realized on a DIFFERENT deployment, not the same eval fold (iter-9 circularity removed)."),
        "deployments": {
            "same_deployment_A": "fit dense on diagnostic fold -> score eval fold (== iter-9 reproduction/contrast)",
            "corpus_fold_B": "split eval fold into DISJOINT B_fit/B_eval by stable doc-hash (DECISIVE transfer)",
            "carrier_shift_C": "fit dense on TEMPLATED content x_on pairs -> deploy on NATURAL eval corpus"},
        "per_case": {cid: {
            "transferB": _case_summary(transferB.get(cid)),
            "transferC": _case_summary(transferC.get(cid)),
            "A_eval_contrast": _A_summary(A_eval.get(cid)),
            "discovery_cost": {"D_full": (transferB.get(cid) or {}).get("D_full"),
                               "D_min": (dmin_res.get(cid) or {}).get("D_min"),
                               "D_min_trace": (dmin_res.get(cid) or {}).get("trace"),
                               "rediscovered": (dmin_res.get(cid) or {}).get("rediscovered")},
            "kl_targeting": kl_res.get(cid),
            "amazon_caveat": _caveat_summary(amazon_res.get(cid)),
        } for cid in cases if cid in setup_fns},
        "n_grid": [_s(x) for x in N_GRID_T], "K_LOC": a.K_LOC, "K_STAR_SMALL": K_STAR_SMALL,
        "kl_scales": KL_SCALES, "kl_null_draws": a.kl_null, "kl_cap": KL_CAP, "material_threshold": MATERIAL_THR,
        "primary_edit_metric": "adv_pres",
        "sae_handle_label_caveat": ("The fixed-id SAE handle uses ZERO labels AT DEPLOYMENT (the absorber id is "
                                    "discovered ONCE on A). The discovery cost D is paid once and amortized over "
                                    "redeployments (break-even K*=D/n*); the handle is transferable label-free at "
                                    "deployment, NOT zero-label end-to-end."),
        "kl_selection_caveat": ("balanced-accuracy ~ the firing-precision selection criterion (mild circularity); "
                                "the localization claim leans on (i) held-out generalization to the eval fold "
                                "(disjoint from the diagnostic fold the absorber was selected on) and (ii) the "
                                "selection-independent next-token behavioral-KL targeting reported here."),
        "sae": {"release": "google/gemma-scope-2b-pt-res", "sae_params": "layer_12/width_16k/average_l0_82",
                "d_model": D_MODEL, "hook": "blocks.12.hook_resid_post"},
        "model": mb.model_id, "seed": SEED, "B_boot": B_BOOT, "Rnorm": Rnorm, "gating_check": gating,
        "cost": {"usd_spent": round(M.SPENT["usd"], 4), "calls": M.SPENT["calls"], "fail": M.SPENT["fail"],
                 "refusal": M.SPENT["refusal"], "primary_judge": PRIMARY_JUDGE["model"],
                 "second_judge": (second_judge or {}).get("model"), "per_model": M.PER_JUDGE,
                 "target_usd": M.TARGET, "hard_cap_usd": M.HARD_CAP},
        "honest_negatives": honest,
    }, "datasets": []}

    assemble_outputs(out, A_eval, transferB, transferC, kl_res, amazon_res)
    save_json(out, a.out)
    logger.info(f"{el()} SAVED -> {a.out} | fork={agg['overall_transfer_fork_verdict']} | "
                f"B={agg['transferB_tally']} KL={agg['kl_tally']} SPENT=${M.SPENT['usd']:.4f}")


def _case_summary(r):
    if not r:
        return None
    return {"verdict": r["verdict"], "powered": r["powered"], "sae_balacc": r["sae"]["value"],
            "sae_ci": [r["sae"]["ci_lo"], r["sae"]["ci_hi"]],
            "dense": {str(n): {"value": dc["value"], "ci": [dc["ci_lo"], dc["ci_hi"]],
                               "dense_below_sae": r["ci_separation"].get(str(n), {}).get("dense_below_sae"),
                               "gate_kind": dc.get("gate_kind"), "capped": dc.get("capped")}
                      for n, dc in r["dense"].items()},
            "n_breakeven": r["n_breakeven"], "n_star": r.get("n_star"), "K_star": r.get("K_star"),
            "K_star_dmin": r.get("K_star_dmin"), "D_full": r.get("D_full"), "D_min": r.get("D_min"),
            "n5_honest": r.get("n5_honest"), "n1_midpoint_artifact": r.get("n1_midpoint_artifact"),
            "fit_pool": r.get("fit_pool")}


def _A_summary(la):
    if not la:
        return None
    return {"verdict": la["verdict"], "sae_balacc": la["sae"]["value"], "n_breakeven": la["n_breakeven"],
            "dense": {str(n): la["dense"][n]["value"] for n in la["dense"]}}


def _caveat_summary(r):
    if not r or r.get("status") != "ok":
        return ({"status": (r or {}).get("status")} if r else None)
    return {"verdict": r["verdict"], "fq_kg": r["fq_kg"], "fq_fair": r["fq_fair"],
            "forget_gap": r["forget_gap"], "forget_gap_ci": r.get("forget_gap_ci"),
            "both_forget_well": r["both_forget_well"], "adv_pres": r["adv_pres"], "adv_joint": r["adv_joint"],
            "adv_joint_full_offset": r.get("adv_joint_full_offset")}


# ========================================================================== SMOKE
def run_smoke(torch, sae, mb, canon, setup_args):
    logger.info(f"{el()} ===== SMOKE (taxonomic_georgia: stash v2 + transfer arms + KL) =====")
    cs = setup_taxonomic(torch, sae, mb, canon, setup_args, mb.mean_resid_norm(["The capital of France is Paris."]),
                         target=("Georgia", 16009, 0.955), case_id="taxonomic_georgia", regime="absorption")
    assert cs.ls_fold_disjoint, "diagnostic/eval folds NOT disjoint"
    assert cs.transfer_disjoint, "A/B deployments NOT disjoint"
    logger.info(f"{el()} SMOKE disjoint OK; B_eval_pos={len(cs.lsB_eval_pos)} B_fit_pos={len(cs.lsB_fit_pos)} "
                f"B_eval_sib={len(cs.lsB_eval_sib)} C_fit_pos={len(cs.lsC_fit_pos)} powered_B={cs.transfer_powered_B}")
    assert cs.transfer_powered_B, "Georgia B should be powered"
    rB = transfer_arm(torch, cs, "corpus_fold_B")
    logger.info(f"{el()} SMOKE transfer-B: sae={rB['sae']['value']:.3f} dense_n1={rB['dense'].get(1,{}).get('value')} "
                f"dense_full={rB['dense'].get('full',{}).get('value')} verdict={rB['verdict']} "
                f"n1_gate={rB['dense'].get(1,{}).get('gate_kind')} n*={rB['n_breakeven']} K*={rB['K_star']}")
    assert 0.0 <= rB["sae"]["value"] <= 1.0
    rC = transfer_arm(torch, cs, "carrier_shift_C")
    logger.info(f"{el()} SMOKE transfer-C: sae={rC['sae']['value']:.3f} dense_full={rC['dense'].get('full',{}).get('value')} "
                f"verdict={rC['verdict']}")
    dm = discovery_cost_min(cs)
    logger.info(f"{el()} SMOKE D_full={cs.D_full} D_min={dm['D_min']} rediscovered={dm['rediscovered']}")
    kl = kl_targeting(torch, sae, mb, cs, n_null=2)
    logger.info(f"{el()} SMOKE KL verdict={kl.get('verdict')} by_scale_1.0={kl.get('by_scale',{}).get('1.0')}")
    # A_eval contrast reproduces iter-9
    la = run_localization_arm(torch, cs, [0, 1, 5, 20, "full"], 8)
    logger.info(f"{el()} SMOKE A_eval(iter9) sae={la['sae']['value']:.3f} dense_full={la['dense'].get('full',{}).get('value')}")
    logger.info(f"{el()} ===== SMOKE OK =====")


if __name__ == "__main__":
    main()
