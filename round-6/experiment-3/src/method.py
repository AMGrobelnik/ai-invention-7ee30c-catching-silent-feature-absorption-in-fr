#!/usr/bin/env python
"""
M4 — EXPAND THE RECALL-HOLE ROUTER PROSPECTIVE SET ON THE HOMOGRAPH ENTITY TESTBED
       (validate-or-demote)  +  M7 ABSORPTION-BREADTH COUNT

This is a THIN extension of the iter-5 a-priori SAE firing-structure router. The router itself
(core.py) is the iter-5 method.py copied VERBATIM; we import every function from it and add only:
  (i)   a homograph-hierarchy loader (build_homograph) over the FOUR is-a hierarchies
        cities / months / given-names / brands (~93 homograph entities),
  (ii)  a per-entity PREDICT-then-MEASURE router (regime is PREDICTED with the FROZEN
        recall-hole-alone rule and LOGGED *before* the per-entity outcome is measured),
  (iii) the prospective aggregation (Wilson-CI ROUTER_VALIDATED / ROUTER_DEMOTED verdict) and
        the M7 absorption-breadth count + named NEW suppressed-parent homographs.

DERIVATION (the 12 frozen concepts) stays IDENTICAL to iter-5 and is NEVER counted prospective:
  spelling L/O/T/I/D, numeric, taxonomic, toxicity {threat, identity_attack, insult, obscene,
  sexual_explicit}. tau_h_alone (PRIMARY), the combined (tau_j, tau_h) ablation and the
  jaccard-alone ablation threshold are fit ONLY on derivation.

PRIMARY rule (frozen):    predict ABSORPTION-regime iff (parent recall-hole > tau_h_alone)
Ground-truth regime PRIMARY = sign(auc_unit - auc_a): does the LABEL-FREE grouped CCRG unit beat
the best single RAW SAE latent (a)?  hit = (predicted == ground_truth).

M4 verdict: ROUTER_VALIDATED iff a PROSPECTIVE Wilson 95% CI EXCLUDES 0.5 (absorption-predicted
stratum, or that stratum combined with the 7 internal new-spelling letters); else ROUTER_DEMOTED
(honest 'exploratory diagnostic, not a validated a-priori predictor').

M7 breadth: over all homograph entities with a stable recall-hole estimate (n_all >= 30), how many
are absorption-STRUCTURED (recall_hole > 0.5 AND firing-Jaccard < 0.1), and which are NEW
suppressed-parent homographs (beyond Georgia/Jordan, which live in the taxonomic derivation set).

SAE  = google/gemma-scope-2b-pt-res layer_12/width_16k/average_l0_82 (JumpReLU, canonical).
Model= unsloth/gemma-2-2b. firing := encode>0. Single GPU. SEED=1234. $0 LLM (the router is $0).

Usage:
  uv run method.py --smoke                  # load+gating+BOS assert + derivation(smoke) + city hier (few entities)
  uv run method.py --scale mini             # derivation(mini) + 7 spelling + 1-2 entities/hier subset
  uv run method.py --scale full             # derivation(full) + 7 spelling + all 4 hierarchies, all entities
"""
import os, sys, json, argparse, gc
from pathlib import Path
from collections import defaultdict

import numpy as np

import core  # iter-5 router copied verbatim; configures logging + DATA paths on import
from core import (logger, el, SEED, MIN_SUB_SENT, MIN_SUB_TOKEN, PARENT_FIRE_FLOOR,
                  TAU_H_GRID, TAU_J_GRID, DERIVATION, NEW_LETTERS, PROSPECTIVE_SPELLING,
                  set_mem_limits, _load, _sanitize, _json_default, _gpu_name,
                  identify_parent, firing_jaccard, cols_auc, _outcome_core,
                  derive_combined, derive_single, loo_single, loo_combined,
                  predict_recall_hole_alone, predict_combined, predict_jaccard_alone,
                  wilson_ci, balanced_accuracy)

HERE = Path(__file__).resolve().parent

# ---------------- numerical-stability patches (core.py stays VERBATIM) ----------------
# Gemma-2 has "massive activation" residual dims whose per-token mean can exceed the float16 range
# (65504) and store as +/-inf; core's non-SAE probe (baseline d) then hits inf/inf -> NaN, which
# roc_auc_score rejects. Two surgical, plan-faithful fixes (they touch ONLY baseline (d) / the AUC
# wrapper, never the SAE-latent unit or the frozen rule): sanitize the residual probe at the source,
# and make core.auc NaN/inf-safe. Both are belt-and-suspenders so a single outlier dim cannot kill a
# long run. The label-free CCRG unit, baselines (a)/(h) and the paired bootstrap all run on bounded
# JumpReLU latents (>=0, finite) and are untouched.
def _safe_nonsae_probe_score(res_pos_tr, res_neg_tr, res_te):
    pos = np.nan_to_num(res_pos_tr.astype(np.float32), nan=0.0, posinf=0.0, neginf=0.0)
    neg = np.nan_to_num(res_neg_tr.astype(np.float32), nan=0.0, posinf=0.0, neginf=0.0)
    rte = np.nan_to_num(res_te.astype(np.float32), nan=0.0, posinf=0.0, neginf=0.0)
    sd = np.concatenate([pos, neg], 0).std(0) + 1e-6
    d = (pos.mean(0) - neg.mean(0)) / sd
    nrm = np.linalg.norm(d) + 1e-9
    out = (rte / sd) @ (d / nrm)
    return np.nan_to_num(out, nan=0.0, posinf=0.0, neginf=0.0)


def _safe_auc(scores, labels):
    from sklearn.metrics import roc_auc_score
    labels = np.asarray(labels)
    if len(set(labels.tolist())) < 2:
        return float("nan")
    scores = np.nan_to_num(np.asarray(scores, dtype=np.float64), nan=0.0, posinf=0.0, neginf=0.0)
    return float(roc_auc_score(labels, scores))


core.nonsae_probe_score = _safe_nonsae_probe_score   # _outcome_core resolves this in core's namespace
core.auc = _safe_auc
core.B_BOOT = 2000   # paired-bootstrap CI width only; point estimates / frozen tau unaffected (plan: >=2000)

# ---------------- homograph testbed (art_2xQn686KUmV5) ----------------
HOMOGRAPH_DATA_DEFAULT = HERE / "homograph_build" / "full_data_out.json"
HIERARCHY_DATASET = {
    "city": "city_homograph_absorption",
    "month": "month_name_absorption",
    "given_name": "given_name_absorption",
    "brand": "brand_homograph_absorption",
}
HIERARCHIES = ["city", "month", "given_name", "brand"]
# Georgia / Jordan are taxonomic-derivation homographs (dataset_2), NOT in this testbed; any
# suppressed-parent homograph found HERE is therefore a NEW named case for the paper.
PRIOR_NAMED_SUPPRESSED = ["Georgia", "Jordan"]

# per-entity corpus caps (encode the hierarchy corpus ONCE, slice per entity)
CAP_POS_PER_ENTITY = {"smoke": 20, "mini": 60, "full": 300}
CAP_NEG_PER_HIER = {"smoke": 60, "mini": 600, "full": 4000}
STABLE_N = 30          # M7 breadth: min positives for a 'stable' recall-hole estimate (descriptive)
ABS_HOLE = 0.5         # M7 absorption-structured recall-hole flag
ABS_JAC = 0.1          # M7 absorption-structured firing-Jaccard flag


# ============================================================================ DERIVATION
def run_derivation(enc, scale, rng, keep):
    """Re-run the 12 DERIVATION concepts EXACTLY as iter-5 (core.py builders + run_concept). These
    are where the frozen rule is fit; they are NEVER counted prospective."""
    res = []
    for L in ["L", "O", "T", "I", "D"]:
        if keep("spelling_%s" % L):
            C = core.build_spelling(L, enc, scale)
            res.append(core.run_concept(C, rng)); del C; gc.collect()
    for hier in ["numeric", "taxonomic"]:
        if keep(hier):
            C = core.build_nonspell(hier, enc, scale)
            res.append(core.run_concept(C, rng)); del C; gc.collect()
    core._cuda_empty()
    tox_deriv = ["toxicity_%s" % s for s in ["threat", "identity_attack", "insult",
                                             "obscene", "sexual_explicit"]]
    if any(keep(t) for t in tox_deriv):
        fam = core.build_toxicity(enc, scale)
        res += [r for r in core.run_toxicity_concepts(fam, rng) if keep(r["concept"])]
        del fam; gc.collect()
    core._cuda_empty()
    derivation = [r for r in res if r["concept"] in DERIVATION]
    return res, derivation


# ============================================================================ SPELLING PROSPECTIVE
def run_spelling_prospective(enc, scale, FROZEN, rng, want_letters):
    """Re-run the 7 internal new-letter spelling concepts (B,C,F,M,P,R,W) — guaranteed
    ABSORPTION-regime prospective members + the documented recall-hole=1.0 over-prediction
    counterexample (F/M/W). Predicted with the FROZEN PRIMARY rule before the outcome is measured."""
    out = []
    if not want_letters:
        return out, []
    by_letter, id_to_word = core._spelling_vocab(enc.tok)
    corpus_scan = core.scan_corpus_positives(enc, id_to_word, want_letters, scale)
    usability = []
    for L in want_letters:
        C, usab = core.build_spelling_prospective(L, enc, scale, by_letter, corpus_scan)
        usability.append(usab)
        r = core.run_concept(C, rng, frozen=FROZEN)
        # attach the frozen-rule predictions (assemble_and_save does this in core; do it here)
        _attach_predictions(r, FROZEN)
        out.append(r); del C; gc.collect()
    del by_letter, id_to_word, corpus_scan; gc.collect()
    core._cuda_empty()
    return out, usability


def _attach_predictions(r, FROZEN):
    cpred = {"jaccard_median": r["jaccard_median"], "recall_hole_max": r["recall_hole_max"]}
    r["predicted_regime"] = predict_recall_hole_alone(cpred, FROZEN["tau_h_alone"])
    r["predicted_regime_combined"] = predict_combined(cpred, FROZEN["tau_j"], FROZEN["tau_h"])
    r["predicted_regime_jaccard"] = predict_jaccard_alone(cpred, FROZEN["tau_j_alone"])
    r["hit_vs_a"] = bool(r["predicted_regime"] == r["ground_truth_regime"])
    r["hit_vs_a_combined"] = bool(r["predicted_regime_combined"] == r["ground_truth_regime"])
    r["hit_vs_a_jaccard"] = bool(r["predicted_regime_jaccard"] == r["ground_truth_regime"])
    r["hit_vs_h"] = bool(r["predicted_regime"] == r["ground_truth_regime_vs_h"])


# ============================================================================ HOMOGRAPH LOADER
def build_homograph(hier_key, enc, scale, full):
    """Adapt core.build_nonspell to the homograph testbed. Identify the ONE broad parent per
    hierarchy on content pairs + ALL corpus positives; encode the hierarchy corpus ONCE (capped per
    entity) and return per-row entity/sense/fold arrays so the per-entity router can slice it."""
    g = next(d for d in full["datasets"] if d["dataset"] == HIERARCHY_DATASET[hier_key])["examples"]
    content = defaultdict(dict); corpus_pos = []; corpus_neg = []
    strength = {}; comp_gloss = {}
    for r in g:
        rt = r.get("metadata_row_type")
        if rt == "content_pair":
            content[r["metadata_pair_id"]][r["metadata_pair_role"]] = r
        elif rt == "corpus":
            if r.get("metadata_concept_present"):
                # positives carry target_sense == hierarchy (NOT 'competitor')
                if r.get("metadata_target_sense") == hier_key:
                    corpus_pos.append(r)
            else:
                corpus_neg.append(r)
        ent = r.get("metadata_entity")
        if ent is not None:
            if r.get("metadata_homograph_strength") is not None:
                strength[ent] = r.get("metadata_homograph_strength")
            if r.get("metadata_competitor_sense") is not None:
                comp_gloss[ent] = r.get("metadata_competitor_sense")
    content = {k: v for k, v in content.items() if "x_on" in v and "x_off" in v}
    pids = sorted(content)
    if scale == "mini":
        pids = pids[:120]
    elif scale == "smoke":
        pids = pids[:24]
    on = [content[p]["x_on"] for p in pids]; off = [content[p]["x_off"] for p in pids]

    def tok_enc(rows, want_resid=False):
        if not rows:
            empty = np.zeros((0, enc.sae.d_sae), np.float16)
            return (empty, np.zeros((0, enc.d_model), np.float16)) if want_resid else empty
        return enc.encode_token([r["input"] for r in rows],
                                [(r["metadata_target_char_start"], r["metadata_target_char_end"]) for r in rows],
                                token_idx_lists=[r.get("metadata_target_token_indices") for r in rows],
                                want_resid=want_resid)

    on_lat, on_res = tok_enc(on, want_resid=True)
    off_lat, off_res = tok_enc(off, want_resid=True)

    # subsample corpus positives per ENTITY (bound size; keep diagnostic-fold positives intact)
    cap_pos = CAP_POS_PER_ENTITY[scale]; cap_neg = CAP_NEG_PER_HIER[scale]
    by_ent = defaultdict(list)
    for r in corpus_pos:
        by_ent[r["metadata_entity"]].append(r)
    krng = np.random.default_rng(SEED)
    keep = []
    for ent, rows in by_ent.items():
        if len(rows) > cap_pos:
            idx = krng.permutation(len(rows))[:cap_pos]
            keep += [rows[int(i)] for i in idx]
        else:
            keep += rows
    if len(corpus_neg) > cap_neg:
        nidx = krng.permutation(len(corpus_neg))[:cap_neg]
        corpus_neg = [corpus_neg[int(i)] for i in nidx]

    pos_lat, pos_res = tok_enc(keep, want_resid=True)
    neg_lat, neg_res = tok_enc(corpus_neg, want_resid=True)
    pos_entity = np.array([r["metadata_entity"] for r in keep], dtype=object)
    pos_sense = np.array([r.get("metadata_target_sense") for r in keep], dtype=object)
    pos_fold = np.array([r.get("metadata_fold") for r in keep], dtype=object)   # train | diagnostic
    neg_fold = np.array([0 if r.get("metadata_fold") == "train" else 1 for r in corpus_neg], dtype=int)
    logger.info(f"{el()} build_homograph {hier_key}: {len(pids)} content pairs, "
                f"{pos_lat.shape[0]} corpus positives over {len(by_ent)} entities, "
                f"{neg_lat.shape[0]} corpus negatives")
    return dict(hier=hier_key, on_lat=on_lat, off_lat=off_lat, on_res=on_res, off_res=off_res,
                pos_lat=pos_lat, pos_res=pos_res, pos_entity=pos_entity, pos_sense=pos_sense,
                pos_fold=pos_fold, neg_lat=neg_lat, neg_res=neg_res, neg_fold=neg_fold,
                strength=strength, comp_gloss=comp_gloss, n_content_pairs=len(pids))


# ============================================================================ PER-ENTITY ROUTER
def run_homograph_hierarchy(hier_key, H, rng, FROZEN, scale):
    """Identify the broad parent ONCE, then for each entity: PREDICT regime with the frozen rule,
    LOG it BEFORE measuring, then MEASURE the per-entity outcome (label-free unit vs a / h / d)."""
    th_alone = FROZEN["tau_h_alone"]
    if H["pos_lat"].shape[0] == 0:
        logger.warning(f"{el()} {hier_key}: no corpus positives -> hierarchy skipped")
        return None, dict(parent_unresolved=True, n_responsive=0), []
    parent, resp, precision, pos_fire_rate, null95, pinfo = identify_parent(
        H["on_lat"], H["off_lat"], H["pos_lat"], rng)
    logger.info(f"\n===== HIERARCHY {hier_key} (parent={parent}, "
                f"parent_pos_firing={pinfo['parent_pos_firing']:.3f}, "
                f"unresolved={pinfo['parent_unresolved']}, n_responsive={pinfo['n_responsive']}) =====")
    fires_pos_all = H["pos_lat"] > 0
    elig_lat = np.array([l for l in resp if l != parent], dtype=int)
    entities = sorted(set(H["pos_entity"].tolist()))
    erows = []
    for E in entities:
        mE = H["pos_entity"] == E
        nE_all = int(mE.sum())
        nE_diag = int((mE & (H["pos_fold"] == "diagnostic")).sum())
        if nE_all == 0:
            continue
        parent_recall_E = float((H["pos_lat"][mE][:, parent] > 0).mean())
        recall_hole_E = float(1.0 - parent_recall_E)
        # detector: best-AUC non-parent eligible latent, E-positives vs hierarchy negatives
        if len(elig_lat) and H["neg_lat"].shape[0] >= 2:
            sc = np.concatenate([H["pos_lat"][mE][:, elig_lat], H["neg_lat"][:, elig_lat]], 0).astype(np.float32)
            yy = np.concatenate([np.ones(nE_all), np.zeros(H["neg_lat"].shape[0])])
            aucs = cols_auc(sc, yy)
            det = int(elig_lat[np.nanargmax(aucs)]) if np.isfinite(aucs).any() else int(elig_lat[0])
            det_auc = float(np.nanmax(aucs)) if np.isfinite(aucs).any() else float("nan")
        else:
            det = parent; det_auc = float("nan")
        # firing-Jaccard(parent, detector) over ALL hierarchy positives (matches per_subcontext)
        jaccard_E = firing_jaccard(fires_pos_all[:, parent], fires_pos_all[:, det])

        # ---- PREDICT with the FROZEN rule, LOG BEFORE measuring the outcome (audit trail) ----
        cpred = {"jaccard_median": jaccard_E, "recall_hole_max": recall_hole_E}
        predicted_regime = predict_recall_hole_alone(cpred, th_alone)            # PRIMARY
        predicted_regime_combined = predict_combined(cpred, FROZEN["tau_j"], FROZEN["tau_h"])
        predicted_regime_jaccard = predict_jaccard_alone(cpred, FROZEN["tau_j_alone"])
        eligible = bool(nE_diag >= MIN_SUB_SENT)
        logger.info(f"{el()} {hier_key}/{E}: n_all={nE_all} n_diag={nE_diag} elig={eligible} "
                    f"recall_hole={recall_hole_E:.3f} jaccard={jaccard_E:.3f} >>> PREDICT "
                    f"(recall_hole>{th_alone:.3f})={predicted_regime} [logged BEFORE outcome measurement]")

        # ---- MEASURE outcome: E-positives vs hierarchy negatives, held-out (diagnostic=test) ----
        pos_fold01 = (H["pos_fold"][mE] == "diagnostic").astype(int)
        out = _outcome_core(parent, resp, precision,
                            full_pos_lat=H["pos_lat"][mE],
                            pos_lat=H["pos_lat"][mE], pos_fold=pos_fold01,
                            neg_lat=H["neg_lat"], neg_fold=H["neg_fold"],
                            res_pos=H["pos_res"][mE], res_neg=H["neg_res"],
                            s_name=f"{hier_key}_{E}", rng=rng)
        ground_truth_regime = "absorption" if out["delta"] > 0 else "co_firing"
        ground_truth_regime_vs_h = "absorption" if out["delta_vs_h"] > 0 else "co_firing"
        hit_vs_a = bool(predicted_regime == ground_truth_regime)
        hit_vs_a_combined = bool(predicted_regime_combined == ground_truth_regime)
        hit_vs_a_jaccard = bool(predicted_regime_jaccard == ground_truth_regime)
        hit_vs_h = bool(predicted_regime == ground_truth_regime_vs_h)
        absorption_structured = bool(recall_hole_E > ABS_HOLE and jaccard_E < ABS_JAC)
        logger.info(f"{el()} {hier_key}/{E}: OUTCOME k={out['k']} auc_unit={out['auc_unit']:.3f} "
                    f"auc_a={out['auc_a']:.3f} auc_h={out['auc_h']:.3f} delta_vs_a={out['delta']:+.3f} "
                    f"-> truth={ground_truth_regime} hit={hit_vs_a} abs_struct={absorption_structured}")
        erows.append(dict(
            hierarchy=hier_key, entity=E, n_all=nE_all, n_diag=nE_diag, eligible=eligible,
            parent_latent=int(parent), parent_unresolved=bool(pinfo["parent_unresolved"]),
            detector_latent=int(det), detector_auc=det_auc,
            recall_hole=recall_hole_E, jaccard=float(jaccard_E),
            homograph_strength=H["strength"].get(E), competitor_sense=H["comp_gloss"].get(E),
            predicted_regime=predicted_regime, predicted_regime_combined=predicted_regime_combined,
            predicted_regime_jaccard=predicted_regime_jaccard,
            auc_unit=out["auc_unit"], auc_a=out["auc_a"], auc_h=out["auc_h"], auc_d=out["auc_d"],
            delta_vs_a=out["delta"], delta_vs_a_ci=out["delta_ci"],
            delta_vs_h=out["delta_vs_h"], delta_vs_h_ci=out["delta_vs_h_ci"],
            k=out["k"], unit_members=out["unit_members"], h_members=out["h_members"],
            a_latent=out["a_latent"], n_test_pos=out["n_test_pos"], n_test_neg=out["n_test_neg"],
            ground_truth_regime=ground_truth_regime, ground_truth_regime_vs_h=ground_truth_regime_vs_h,
            hit_vs_a=hit_vs_a, hit_vs_a_combined=hit_vs_a_combined, hit_vs_a_jaccard=hit_vs_a_jaccard,
            hit_vs_h=hit_vs_h, is_prospective_hit=hit_vs_a, absorption_structured=absorption_structured,
            power_flag=("inferential" if eligible else "descriptive_only")))
    return int(parent), pinfo, erows


# ============================================================================ AGGREGATION / VERDICT
def _excludes_half(ci):
    lo, hi = ci["wilson_ci"]
    return (lo is not None and lo > 0.5) or (hi is not None and hi < 0.5)


def aggregate_and_verdict(entity_rows, spelling_results):
    """M4: prospective hit-rate STRATIFIED by PRIMARY predicted regime with Wilson 95% CIs +
    validate-or-demote verdict; M7: absorption-breadth count + named new suppressed-parent homographs."""
    inf = [e for e in entity_rows if e["eligible"]]

    def strat(rows, pred_key, hit_key):
        absn = [r for r in rows if r[pred_key] == "absorption"]
        cof = [r for r in rows if r[pred_key] == "co_firing"]
        return dict(absorption_predicted=wilson_ci(sum(1 for r in absn if r[hit_key]), len(absn)),
                    cofiring_predicted=wilson_ci(sum(1 for r in cof if r[hit_key]), len(cof)),
                    combined_all=wilson_ci(sum(1 for r in rows if r[hit_key]), len(rows)))

    prospective_hitrate_primary = strat(inf, "predicted_regime", "hit_vs_a")
    prospective_hitrate_ablation_combined = strat(inf, "predicted_regime_combined", "hit_vs_a_combined")
    prospective_hitrate_ablation_jaccard = strat(inf, "predicted_regime_jaccard", "hit_vs_a_jaccard")
    prospective_hitrate_vs_h = strat(inf, "predicted_regime", "hit_vs_h")

    # combine homograph absorption-predicted entities WITH the 7 internal spelling letters (each one
    # prospective unit) to MAXIMIZE the absorption-predicted arm's n -> best chance to exclude 0.5.
    sp_abs = [r for r in spelling_results if r.get("predicted_regime") == "absorption"]
    abs_inf = [r for r in inf if r["predicted_regime"] == "absorption"]
    hits_plus = sum(1 for r in abs_inf if r["hit_vs_a"]) + sum(1 for r in sp_abs if r["hit_vs_a"])
    n_plus = len(abs_inf) + len(sp_abs)
    wilson_abs_plus = wilson_ci(hits_plus, n_plus)
    # also: ALL inferential prospective (homograph entities + spelling letters)
    hits_allp = sum(1 for r in inf if r["hit_vs_a"]) + sum(1 for r in spelling_results if r.get("hit_vs_a"))
    n_allp = len(inf) + len(spelling_results)
    wilson_all_plus = wilson_ci(hits_allp, n_allp)

    wilson_abs = prospective_hitrate_primary["absorption_predicted"]
    wilson_cof = prospective_hitrate_primary["cofiring_predicted"]
    verdict = ("ROUTER_VALIDATED" if (_excludes_half(wilson_abs) or _excludes_half(wilson_abs_plus))
               else "ROUTER_DEMOTED")
    rationale = (
        f"absorption-predicted homograph stratum Wilson95={np.round(wilson_abs['wilson_ci'],3).tolist()} "
        f"(n={wilson_abs['n']}); homograph+spelling absorption stratum Wilson95="
        f"{np.round(wilson_abs_plus['wilson_ci'],3).tolist()} (n={wilson_abs_plus['n']}). "
        + ("At least one prospective CI EXCLUDES 0.5 -> the recall-hole router is a VALIDATED a-priori "
           "predictor on this stratum." if verdict == "ROUTER_VALIDATED" else
           "No prospective CI excludes 0.5 -> the router is reported as an EXPLORATORY DIAGNOSTIC, not a "
           "validated a-priori predictor (honest negative)."))
    logger.info(f"{el()} M4 VERDICT={verdict}: {rationale}")

    # ---------------- M7 absorption breadth count ----------------
    stable = [e for e in entity_rows if e["n_all"] >= STABLE_N]
    elig_struct = [e for e in entity_rows if e["eligible"]]
    abs_struct_stable = [e for e in stable if e["absorption_structured"]]
    abs_struct_elig = [e for e in elig_struct if e["absorption_structured"]]
    abs_struct_sorted = sorted(abs_struct_stable, key=lambda e: -e["recall_hole"])
    per_hier = {}
    for h in HIERARCHIES:
        hs = [e for e in stable if e["hierarchy"] == h]
        ha = [e for e in hs if e["absorption_structured"]]
        per_hier[h] = dict(n_entities_stable=len(hs), n_absorption_structured=len(ha),
                           examples=[dict(entity=e["entity"], recall_hole=round(e["recall_hole"], 3),
                                          jaccard=round(e["jaccard"], 3)) for e in
                                     sorted(ha, key=lambda e: -e["recall_hole"])[:8]])
    new_suppressed = [dict(hierarchy=e["hierarchy"], entity=e["entity"],
                           recall_hole=round(e["recall_hole"], 3), jaccard=round(e["jaccard"], 3),
                           homograph_strength=e["homograph_strength"],
                           competitor_sense=e["competitor_sense"],
                           ground_truth_regime=e["ground_truth_regime"], eligible=e["eligible"])
                      for e in abs_struct_sorted
                      if e["entity"] not in PRIOR_NAMED_SUPPRESSED]
    # DOWNSTREAM-CONFIRMED absorption: entities where the label-free CCRG unit ACTUALLY beats the best
    # raw latent (ground_truth_regime == absorption), i.e. grouping genuinely helps downstream. This is
    # a DIFFERENT lens from the structural flag: a month can be structurally-absorption-shaped (high
    # recall-hole + firing-disjoint detector) yet co_firing downstream, and vice-versa.
    downstream_abs = sorted([e for e in entity_rows if e["ground_truth_regime"] == "absorption"],
                            key=lambda e: -e["delta_vs_a"])
    downstream_confirmed = [dict(hierarchy=e["hierarchy"], entity=e["entity"],
                                 recall_hole=round(e["recall_hole"], 3), jaccard=round(e["jaccard"], 3),
                                 delta_vs_a=round(e["delta_vs_a"], 4), delta_vs_a_ci=e["delta_vs_a_ci"],
                                 auc_unit=round(e["auc_unit"], 3), auc_a=round(e["auc_a"], 3),
                                 absorption_structured=e["absorption_structured"], eligible=e["eligible"],
                                 predicted_regime=e["predicted_regime"])
                            for e in downstream_abs]
    breadth = dict(
        n_entities_total=len(entity_rows),
        n_entities_with_stable_estimate=len(stable),
        n_entities_eligible=len(elig_struct),
        absorption_structured_definition=f"recall_hole > {ABS_HOLE} AND firing_Jaccard < {ABS_JAC}",
        n_absorption_structured_stable=len(abs_struct_stable),
        n_absorption_structured_eligible=len(abs_struct_elig),
        absorption_structured_entities=[
            dict(hierarchy=e["hierarchy"], entity=e["entity"], recall_hole=round(e["recall_hole"], 3),
                 jaccard=round(e["jaccard"], 3), homograph_strength=e["homograph_strength"],
                 eligible=e["eligible"], ground_truth_regime=e["ground_truth_regime"])
            for e in abs_struct_sorted],
        per_hierarchy=per_hier,
        new_suppressed_parent_homographs=new_suppressed,
        prior_named_suppressed_parents_elsewhere=PRIOR_NAMED_SUPPRESSED,
        n_downstream_confirmed_absorption=len(downstream_confirmed),
        downstream_confirmed_absorption_entities=downstream_confirmed,
        structural_vs_downstream_note=(
            "absorption_structured (recall-hole>0.5 AND firing-Jaccard<0.1) is a STRUCTURAL flag; "
            "ground_truth_regime=='absorption' (label-free unit beats best raw latent (a)) is the "
            "DOWNSTREAM benefit. They can disagree: structurally-absorption-shaped months can still be "
            "co_firing downstream, and the strongest downstream-absorption case can have high firing-"
            "Jaccard. Both lenses are reported."))
    logger.info(f"{el()} M7 BREADTH: {len(abs_struct_stable)}/{len(stable)} stable homograph entities are "
                f"absorption-structured ({len(abs_struct_elig)} of them eligible); "
                f"{len(new_suppressed)} NEW named suppressed-parent homographs.")

    agg = dict(
        prospective_hitrate_primary=prospective_hitrate_primary,
        prospective_hitrate_ablation_combined=prospective_hitrate_ablation_combined,
        prospective_hitrate_ablation_jaccard=prospective_hitrate_ablation_jaccard,
        prospective_hitrate_vs_h=prospective_hitrate_vs_h,
        prospective_hitrate_combined_with_spelling=dict(
            absorption_predicted=wilson_abs_plus, combined_all=wilson_all_plus,
            n_homograph_absorption=len(abs_inf), n_spelling_absorption=len(sp_abs)),
        router_verdict=verdict, router_verdict_rationale=rationale,
        n_inferential_entities=len(inf), n_entities_total=len(entity_rows))
    return agg, breadth, prospective_hitrate_primary


# ============================================================================ EMIT
def _entity_card(e, th_alone):
    role = "prospective"
    return {
        "input": (f"Homograph entity '{e['entity']}' (hierarchy={e['hierarchy']}, is-a-{e['hierarchy']}, "
                  f"{role}): parent latent {e['parent_latent']}, parent recall-hole={e['recall_hole']:.4f}, "
                  f"firing-Jaccard(detector,parent)={e['jaccard']:.4f}. PRIMARY a-priori screen "
                  f"(recall-hole>{th_alone:.3f}): route to absorption-repair (CCRG grouping) or marginal "
                  f"attribution?"),
        "output": e["ground_truth_regime"],
        "predict_router": e["predicted_regime"],
        "metadata_kind": "homograph_entity",
        "metadata_role": role,
        "metadata_hierarchy": e["hierarchy"],
        "metadata_entity": e["entity"],
        "metadata_n_all": e["n_all"],
        "metadata_n_diagnostic": e["n_diag"],
        "metadata_eligible": e["eligible"],
        "metadata_power_flag": e["power_flag"],
        "metadata_parent_latent": e["parent_latent"],
        "metadata_parent_unresolved": e["parent_unresolved"],
        "metadata_detector_latent": e["detector_latent"],
        "metadata_recall_hole": e["recall_hole"],
        "metadata_jaccard": e["jaccard"],
        "metadata_homograph_strength": e["homograph_strength"],
        "metadata_competitor_sense": e["competitor_sense"],
        "metadata_predicted_regime": e["predicted_regime"],
        "metadata_predicted_regime_combined": e["predicted_regime_combined"],
        "metadata_predicted_regime_jaccard": e["predicted_regime_jaccard"],
        "metadata_ground_truth_regime": e["ground_truth_regime"],
        "metadata_ground_truth_regime_vs_h": e["ground_truth_regime_vs_h"],
        "metadata_outcome_auc_unit": e["auc_unit"],
        "metadata_outcome_auc_a_rawlatent": e["auc_a"],
        "metadata_outcome_auc_h_attribution": e["auc_h"],
        "metadata_outcome_auc_d_nonsae": e["auc_d"],
        "metadata_outcome_delta_vs_a": e["delta_vs_a"],
        "metadata_outcome_delta_vs_a_ci": e["delta_vs_a_ci"],
        "metadata_outcome_delta_vs_h": e["delta_vs_h"],
        "metadata_outcome_delta_vs_h_ci": e["delta_vs_h_ci"],
        "metadata_outcome_k": e["k"],
        "metadata_unit_members": e["unit_members"],
        "metadata_h_members": e["h_members"],
        "metadata_a_latent": e["a_latent"],
        "metadata_hit_vs_a": e["hit_vs_a"],
        "metadata_hit_vs_a_combined": e["hit_vs_a_combined"],
        "metadata_hit_vs_a_jaccard": e["hit_vs_a_jaccard"],
        "metadata_hit_vs_h": e["hit_vs_h"],
        "metadata_is_prospective_hit": e["is_prospective_hit"],
        "metadata_absorption_structured": e["absorption_structured"],
    }


def _concept_card(r, role, th_alone):
    o = r["outcome"]
    return {
        "input": (f"Concept '{r['concept']}' ({r['granularity']}, {role}): parent latent "
                  f"{r['parent_latent']}, parent recall-hole={r['recall_hole_max']:.4f}, "
                  f"firing-Jaccard(detector,parent) median={r['jaccard_median']:.4f}. PRIMARY a-priori "
                  f"screen (recall-hole>{th_alone:.3f}): route to absorption-repair or marginal attribution?"),
        "output": r["ground_truth_regime"],
        "predict_router": r.get("predicted_regime", "co_firing"),
        "metadata_kind": ("derivation_concept" if role == "derivation" else "spelling_prospective"),
        "metadata_role": role,
        "metadata_concept": r["concept"],
        "metadata_granularity": r["granularity"],
        "metadata_parent_latent": r["parent_latent"],
        "metadata_parent_unresolved": r.get("parent_unresolved", False),
        "metadata_recall_hole": r["recall_hole_max"],
        "metadata_jaccard": r["jaccard_median"],
        "metadata_predicted_regime": r.get("predicted_regime"),
        "metadata_predicted_regime_combined": r.get("predicted_regime_combined"),
        "metadata_predicted_regime_jaccard": r.get("predicted_regime_jaccard"),
        "metadata_ground_truth_regime": r["ground_truth_regime"],
        "metadata_ground_truth_regime_vs_h": r["ground_truth_regime_vs_h"],
        "metadata_outcome_auc_unit": o["auc_unit"],
        "metadata_outcome_auc_a_rawlatent": o.get("auc_a"),
        "metadata_outcome_auc_h_attribution": o["auc_h"],
        "metadata_outcome_auc_d_nonsae": o.get("auc_d"),
        "metadata_outcome_delta_vs_a": o["delta"],
        "metadata_outcome_delta_vs_a_ci": o["delta_ci"],
        "metadata_outcome_k": o["k"],
        "metadata_hit_vs_a": r.get("hit_vs_a"),
        "metadata_is_prospective_hit": (bool(r.get("hit_vs_a")) if role == "prospective" else None),
        "metadata_power_flag": "inferential",
    }


def assemble_and_save(derivation, deriv_results, spelling_results, entity_rows, hierarchy_parents,
                      frozen, FROZEN, bacc_h, bacc_j, agg, breadth, php, gating, spelling_usability,
                      args, scale, homograph_data_path, full_meta):
    th_alone = FROZEN["tau_h_alone"]; tj_alone = FROZEN["tau_j_alone"]
    tau_j, tau_h = frozen["tau_j"], frozen["tau_h"]

    # attach frozen-rule predictions to derivation rows (in-sample display)
    for r in deriv_results:
        _attach_predictions(r, FROZEN)

    # LOO on derivation (matches iter-5)
    loo_h_acc, loo_h_rows = loo_single(derivation, "recall_hole_max", False, TAU_H_GRID)
    loo_j_acc, loo_j_rows = loo_single(derivation, "jaccard_median", True, TAU_J_GRID)
    loo_comb_acc, loo_comb_rows = loo_combined(derivation)
    logger.info(f"{el()} LOO derivation: recall-hole-alone={loo_h_acc:.3f} (PRIMARY) "
                f"jaccard-alone={loo_j_acc:.3f} combined={loo_comb_acc:.3f}")

    # derivation reproduction block vs iter-5 reference (0.7795 / balanced_acc 1.0 / LOO ~0.833)
    reproduction = dict(
        tau_h_alone_actual=float(th_alone), tau_h_alone_iter5_reference=0.7795,
        tau_h_alone_drift=float(abs(th_alone - 0.7795)),
        derivation_balanced_acc_recall_hole_alone=float(bacc_h),
        derivation_balanced_acc_iter5_reference=1.0,
        loo_recall_hole_alone_actual=float(loo_h_acc), loo_iter5_reference=0.833,
        n_derivation=len(derivation),
        note=("Frozen rule = whatever derivation yields; tiny drift from iter-5 is reported, not a hard "
              "failure. tau_h_alone is fit ONLY on the 12 derivation concepts BEFORE any prospective "
              "(homograph / spelling) outcome is measured (predict-then-measure integrity)."))
    logger.info(f"{el()} REPRODUCTION tau_h_alone={th_alone:.4f} (ref 0.7795, drift "
                f"{reproduction['tau_h_alone_drift']:.4f}) bacc={bacc_h:.3f} LOO={loo_h_acc:.3f}")

    # counterexamples (verbatim honest disclosures)
    dmap = {r["concept"]: r for r in derivation}
    counterexamples = []
    if "numeric" in dmap:
        r = dmap["numeric"]
        counterexamples.append(
            f"numeric: firing-Jaccard={r['jaccard_median']:.3f} HIGH yet ground-truth="
            f"{r['ground_truth_regime']} -> jaccard-alone MISLABELS it; the recall-hole gate "
            f"(recall_hole={r['recall_hole_max']:.3f}) routes it correctly.")
    if "taxonomic" in dmap:
        r = dmap["taxonomic"]
        counterexamples.append(
            f"taxonomic (aggregated): firing-Jaccard={r['jaccard_median']:.3f} LOW yet ground-truth="
            f"{r['ground_truth_regime']}: the parent already fires on {r['parent_pos_firing']:.2f} of "
            f"positives (recall_hole={r['recall_hole_max']:.3f}) so there are no holes -> recall-hole gate "
            f"correctly routes co_firing where jaccard-alone would mislabel absorption.")
    # F/M/W over-prediction counterexample, re-confirmed on the new spelling letters
    fmw = [r for r in spelling_results if r["concept"] in ("spelling_F", "spelling_M", "spelling_W")]
    fmw_miss = [r for r in fmw if r.get("predicted_regime") == "absorption" and not r.get("hit_vs_a")]
    if fmw_miss:
        counterexamples.append(
            "recall-hole≈1.0 OVER-predicts absorption on new spelling letters " +
            ",".join(r["concept"].split("_")[1] for r in fmw_miss) +
            " (false-absorption misses) — re-confirmed here.")

    honest = []
    honest.append(f"M4 VERDICT = {agg['router_verdict']}. {agg['router_verdict_rationale']}")
    honest.append(
        "PRIMARY rule = RECALL-HOLE-ALONE (predict absorption iff parent recall-hole > "
        f"{th_alone:.3f}); fit ONLY on the 12 frozen DERIVATION concepts (balanced_acc={bacc_h:.3f}, "
        f"LOO={loo_h_acc:.3f}). The homograph entities + the 7 internal spelling letters are the "
        "truly-PROSPECTIVE set: every entity's regime is PREDICTED and LOGGED ('[logged BEFORE outcome "
        "measurement]') before its per-entity outcome is measured.")
    honest.append(
        "GROUND-TRUTH regime PRIMARY = sign(auc_unit - auc_a): the label-free CCRG unit is built on the "
        "parent's recall HOLES, so a hit means grouping helps exactly where the recall-hole rule said it "
        "would. SECONDARY vs (h) the supervised attribution pool frequently beats the unit on GENERAL "
        "classification even in true absorption (the absorption advantage lives on absorbed-slice recall); "
        "(d) is the required non-SAE residual diff-of-means probe. (a)/(h)/(d) reported in every entity row.")
    honest.append(
        f"M7 BREADTH: of {breadth['n_entities_with_stable_estimate']} homograph entities with a stable "
        f"recall-hole estimate (n_all>={STABLE_N}), {breadth['n_absorption_structured_stable']} are "
        f"absorption-structured ({breadth['absorption_structured_definition']}); "
        f"{breadth['n_absorption_structured_eligible']} of those are inferential (n_diag>={MIN_SUB_SENT}). "
        f"This directly quantifies how narrow absorption is across the homograph entity space and answers "
        f"the 'absorption is n=1-2' critique. NEW named suppressed-parent homographs (beyond "
        f"Georgia/Jordan, which live in the taxonomic derivation set): "
        + (", ".join(f"{x['entity']}({x['hierarchy']},hole {x['recall_hole']})"
                     for x in breadth['new_suppressed_parent_homographs'][:12]) or "none found"))
    honest.append(
        "SANITY: the absorption-PREDICTED rule (recall_hole>tau_h_alone~0.78) is a stricter recall-hole gate "
        "than the recall_hole>0.5 used in the structural flag, so #(recall_hole>0.78) <= #(recall_hole>0.5); "
        "the absorption-STRUCTURED count additionally requires firing-Jaccard<0.1, so it is not strictly "
        "nested with the predicted-absorption set. All counts are reported.")
    dc = breadth.get("downstream_confirmed_absorption_entities", [])
    if dc:
        top = dc[0]
        honest.append(
            f"STRUCTURAL != DOWNSTREAM: {breadth['n_downstream_confirmed_absorption']} eligible-or-stable "
            f"entities are DOWNSTREAM-confirmed absorption (label-free unit beats best raw latent (a)); the "
            f"strongest is {top['hierarchy']}/{top['entity']} (delta_vs_a={top['delta_vs_a']:+.3f}, recall_hole="
            f"{top['recall_hole']:.3f}, jaccard={top['jaccard']:.3f}). Note the structurally-absorption-shaped "
            f"months (recall-hole>0.5 AND jaccard<0.1) can be co_firing DOWNSTREAM and the strongest downstream "
            f"win can have high firing-Jaccard — structural shape does not guarantee a grouping benefit.")
    honest += counterexamples
    for h in HIERARCHIES:
        if h in hierarchy_parents and hierarchy_parents[h].get("parent_unresolved"):
            honest.append(f"{h}: parent_unresolved (no responsive latent cleared the "
                          f"{PARENT_FIRE_FLOOR:.0%} positive-firing floor) -> entities default co_firing.")
    for e in entity_rows:
        if e["eligible"] and not e["hit_vs_a"]:
            honest.append(f"PROSPECTIVE MISS {e['hierarchy']}/{e['entity']}: predicted "
                          f"{e['predicted_regime']} but ground-truth(vs-a) {e['ground_truth_regime']} "
                          f"(delta_vs_a={e['delta_vs_a']:+.3f}).")

    # entity table
    entity_table = [dict(hierarchy=e["hierarchy"], entity=e["entity"], n_all=e["n_all"],
                         n_diag=e["n_diag"], eligible=e["eligible"], power_flag=e["power_flag"],
                         parent_latent=e["parent_latent"], recall_hole=e["recall_hole"],
                         jaccard=e["jaccard"], homograph_strength=e["homograph_strength"],
                         predicted_regime=e["predicted_regime"],
                         ground_truth_regime=e["ground_truth_regime"],
                         auc_unit=e["auc_unit"], auc_a=e["auc_a"], auc_h=e["auc_h"], auc_d=e["auc_d"],
                         delta_vs_a=e["delta_vs_a"], delta_vs_a_ci=e["delta_vs_a_ci"], k=e["k"],
                         hit_vs_a=e["hit_vs_a"], absorption_structured=e["absorption_structured"])
                    for e in entity_rows]
    spelling_table = [dict(concept=r["concept"], recall_hole=r["recall_hole_max"],
                           jaccard=r["jaccard_median"], predicted_regime=r.get("predicted_regime"),
                           ground_truth_regime=r["ground_truth_regime"],
                           auc_unit=r["outcome"]["auc_unit"], auc_a=r["outcome"].get("auc_a"),
                           delta_vs_a=r["outcome"]["delta"], hit_vs_a=r.get("hit_vs_a"))
                      for r in spelling_results]
    derivation_table = [dict(concept=r["concept"], recall_hole=r["recall_hole_max"],
                             jaccard=r["jaccard_median"], predicted_regime=r.get("predicted_regime"),
                             ground_truth_regime=r["ground_truth_regime"],
                             auc_unit=r["outcome"]["auc_unit"], auc_a=r["outcome"].get("auc_a"),
                             delta_vs_a=r["outcome"]["delta"], hit_vs_a=r.get("hit_vs_a"))
                        for r in derivation]

    metadata = dict(
        method_name="M4 Recall-Hole Router — Homograph Prospective Expansion (validate-or-demote) + M7 breadth",
        description=(
            "Reuses the iter-5 a-priori SAE firing-structure router VERBATIM (core.py) and applies the "
            "FROZEN recall-hole-alone rule (absorption iff parent recall-hole > tau_h_alone, fit ONLY on "
            "the 12 frozen derivation concepts) to a much larger truly-prospective set: ~93 homograph "
            "entities across 4 is-a hierarchies (cities/months/given-names/brands) + the 7 internal "
            "new-spelling letters. Each entity's regime is PREDICTED and LOGGED before its per-entity "
            "outcome (label-free CCRG unit vs best raw latent (a) / attribution pool (h) / non-SAE probe "
            "(d)) is measured; hit = (predicted == sign(auc_unit-auc_a)). M4 = per-predicted-regime "
            "prospective Wilson CIs + ROUTER_VALIDATED (CI excludes 0.5) / ROUTER_DEMOTED verdict. M7 = "
            "systematic absorption-breadth count over the homograph entities + named NEW suppressed-parent "
            "homographs. Reported as a screening heuristic with measured error, not a validated oracle."),
        baselines=dict(
            a="best single raw SAE latent (highest train AUC, content-responsive) — the individual latent to beat",
            h="supervised SAE standardized diff-of-means attribution pool (top-k, AxBench/SCR-TPP proxy)",
            d="non-SAE standardized diff-of-means probe on the raw layer-12 residual (required non-SAE baseline)",
            unit="label-free CCRG K-track-lite: parent anchor + firing-disjoint hole-covering absorbers"),
        sae_release=core.RELEASE_REPO, sae_id=core.SAE_PARAMS_16K, hook="blocks.12.hook_resid_post",
        model=core.MODEL_ID, seed=SEED, scale=scale, accelerator=_gpu_name(),
        firing_convention="encode>0 (JumpReLU)", gating=gating,
        homograph_data_path=str(homograph_data_path), homograph_build_metadata=full_meta,
        frozen_rule=dict(
            recommended="recall_hole_alone",
            tau_h_alone=float(th_alone), derivation_balanced_acc=float(bacc_h),
            tau_j=float(tau_j), tau_h=float(tau_h),
            combined_balanced_acc=float(frozen["balanced_acc"]),
            tau_j_alone=float(tj_alone), jaccard_alone_balanced_acc=float(bacc_j),
            definition_string=(f"predict ABSORPTION-regime iff (parent recall-hole > {th_alone:.4f}); "
                               f"else CO-FIRING-regime"),
            loo=dict(recall_hole_alone_acc=float(loo_h_acc), jaccard_alone_acc=float(loo_j_acc),
                     combined_acc=float(loo_comb_acc),
                     recall_hole_alone_per_concept=loo_h_rows,
                     jaccard_alone_per_concept=loo_j_rows, combined_per_concept=loo_comb_rows)),
        reproduction_check=reproduction,
        router_verdict=agg["router_verdict"], router_verdict_rationale=agg["router_verdict_rationale"],
        prospective_hitrate_primary=agg["prospective_hitrate_primary"],
        prospective_hitrate_combined_with_spelling=agg["prospective_hitrate_combined_with_spelling"],
        prospective_hitrate_ablation_combined=agg["prospective_hitrate_ablation_combined"],
        prospective_hitrate_ablation_jaccard=agg["prospective_hitrate_ablation_jaccard"],
        prospective_hitrate_vs_h=agg["prospective_hitrate_vs_h"],
        n_inferential_entities=agg["n_inferential_entities"], n_entities_total=agg["n_entities_total"],
        absorption_breadth=breadth,
        hierarchy_parents={h: dict(parent_latent=hierarchy_parents[h].get("parent"),
                                   parent_pos_firing=hierarchy_parents[h].get("parent_pos_firing"),
                                   parent_unresolved=hierarchy_parents[h].get("parent_unresolved"),
                                   n_responsive=hierarchy_parents[h].get("n_responsive"))
                           for h in hierarchy_parents},
        counterexamples=counterexamples, honest_notes=honest,
        derivation_concepts=[r["concept"] for r in derivation],
        prospective_spelling=[r["concept"] for r in spelling_results],
        prospective_entities=[f"{e['hierarchy']}/{e['entity']}" for e in entity_rows],
        derivation_table=derivation_table, spelling_prospective_table=spelling_table,
        entity_table=entity_table, spelling_usability=spelling_usability,
        n_concepts=len(deriv_results) + len(spelling_results) + len(entity_rows),
        n_derivation=len(derivation), n_prospective_spelling=len(spelling_results),
        n_prospective_homograph=len(entity_rows))

    # ---------------- exp_gen_sol_out cards ----------------
    examples = []
    for r in derivation:
        examples.append(_concept_card(r, "derivation", th_alone))
    for r in spelling_results:
        examples.append(_concept_card(r, "prospective", th_alone))
    for e in entity_rows:
        examples.append(_entity_card(e, th_alone))
    out = {"metadata": metadata, "datasets": [{"dataset": "m4_router_prospective_concepts",
                                               "examples": examples}]}
    Path(args.out).write_text(json.dumps(_sanitize(out), indent=2, default=_json_default, allow_nan=False))
    logger.info(f"{el()} wrote {args.out} ({Path(args.out).stat().st_size/1e6:.3f} MB, "
                f"{len(examples)} cards)")
    _print_summary(agg, breadth, reproduction, php)
    return out


def _print_summary(agg, breadth, repro, php):
    logger.info("\n================= M4 / M7 SUMMARY =================")
    logger.info(f"FROZEN tau_h_alone={repro['tau_h_alone_actual']:.4f} (iter5 ref 0.7795, drift "
                f"{repro['tau_h_alone_drift']:.4f}); derivation bacc="
                f"{repro['derivation_balanced_acc_recall_hole_alone']:.3f} LOO="
                f"{repro['loo_recall_hole_alone_actual']:.3f}")
    a = php["absorption_predicted"]; c = php["cofiring_predicted"]; al = php["combined_all"]
    logger.info(f"PROSPECTIVE hit-rate by PRIMARY predicted regime (inferential homograph entities, "
                f"n={al['n']}): absorption_predicted={a['hits']}/{a['n']} "
                f"(rate={a['rate']}, Wilson95={np.round(a['wilson_ci'],3).tolist()}); "
                f"cofiring_predicted={c['hits']}/{c['n']} (rate={c['rate']}, "
                f"Wilson95={np.round(c['wilson_ci'],3).tolist()})")
    p = agg["prospective_hitrate_combined_with_spelling"]["absorption_predicted"]
    logger.info(f"absorption-predicted + 7 spelling letters: {p['hits']}/{p['n']} "
                f"(Wilson95={np.round(p['wilson_ci'],3).tolist()})")
    logger.info(f"ROUTER VERDICT = {agg['router_verdict']}")
    logger.info(f"M7 absorption-structured: {breadth['n_absorption_structured_stable']}/"
                f"{breadth['n_entities_with_stable_estimate']} stable entities; NEW named suppressed "
                f"parents = {[x['entity'] for x in breadth['new_suppressed_parent_homographs'][:12]]}")


# ============================================================================ MAIN
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scale", default="full", choices=["smoke", "mini", "full"])
    ap.add_argument("--smoke", action="store_true",
                    help="load + gating + BOS assert + derivation(smoke) + city hierarchy (few entities)")
    ap.add_argument("--hierarchies", default="", help="comma list of hierarchies (debug)")
    ap.add_argument("--letters", default="", help="comma list of spelling letters (debug)")
    ap.add_argument("--max_entities", type=int, default=0, help="cap entities/hierarchy (debug; 0=all)")
    ap.add_argument("--homograph_data", default=str(HOMOGRAPH_DATA_DEFAULT))
    ap.add_argument("--out", default=str(HERE / "method_out.json"))
    ap.add_argument("--ram_gb", type=float, default=120.0)
    args = ap.parse_args()
    set_mem_limits(args.ram_gb)
    rng = np.random.default_rng(SEED)
    scale = "smoke" if args.smoke else args.scale
    logger.info(f"{el()} M4 homograph-prospective router | scale={scale} smoke={args.smoke}")

    enc = core.Encoder()
    # ---- gating + BOS-offset assertion on real spelling corpus rows (reuse core's substrate) ----
    sp = next(d for d in _load(core.DATA["spelling"])["datasets"]
              if d["dataset"].endswith("_L"))["examples"]
    corpus = [r for r in sp if r.get("metadata_pair_type") == "corpus_context"][:20]
    gating = enc.gating_check([r["input"] for r in corpus[:8]])
    cspan = [tuple(r["metadata_target_char_in_window"]) for r in corpus]
    cids = [r["metadata_target_token_id"] for r in corpus]
    _ = enc.encode_token([r["input"] for r in corpus], cspan, check_ids=cids)
    if gating["recon_cos_mean"] < 0.80:
        logger.error(f"GATING recon_cos_mean={gating['recon_cos_mean']:.3f} (<0.80)")

    # ---- DERIVATION (frozen rule fit ONLY here) ----
    # smoke restricts derivation to a 2-regime subset (spelling_L+numeric=absorption, taxonomic=co_firing)
    # to skip the 57MB toxicity load — pure CODE-PATH validation; full/mini run all 12 concepts.
    deriv_keep = ((lambda n: n in {"spelling_L", "numeric", "taxonomic"}) if args.smoke
                  else (lambda n: True))
    deriv_results, derivation = run_derivation(enc, scale, rng, keep=deriv_keep)
    if not derivation or len(set(c["ground_truth_regime"] for c in derivation)) < 2:
        logger.error("derivation has <2 regimes; cannot freeze a rule");
    frozen = derive_combined(derivation)
    th_alone, bacc_h, _ = derive_single(derivation, "recall_hole_max", False, TAU_H_GRID)
    tj_alone, bacc_j, _ = derive_single(derivation, "jaccard_median", True, TAU_J_GRID)
    FROZEN = dict(tau_j=frozen["tau_j"], tau_h=frozen["tau_h"], tau_h_alone=th_alone, tau_j_alone=tj_alone)
    logger.info(f"{el()} ===== FROZEN PRIMARY rule: absorption iff recall_hole>{th_alone:.4f} "
                f"| derivation balanced_acc={bacc_h:.3f} (combined tau_j={frozen['tau_j']:.3f} "
                f"tau_h={frozen['tau_h']:.3f} bacc={frozen['balanced_acc']:.3f}; jaccard-alone "
                f"tau_j={tj_alone:.4f} bacc={bacc_j:.3f}) =====")

    # ---- PROSPECTIVE SPELLING (absorption-regime members + F/M/W counterexample) ----
    want_letters = NEW_LETTERS
    if args.letters:
        want_letters = [L for L in NEW_LETTERS if L in args.letters.split(",")]
    if args.smoke:
        want_letters = ["C", "F"]
    spelling_results, spelling_usability = run_spelling_prospective(enc, scale, FROZEN, rng, want_letters)

    # ---- HOMOGRAPH HIERARCHIES (per-entity predict-then-measure) ----
    homograph_path = Path(args.homograph_data)
    full = _load(homograph_path)
    full_meta = full.get("metadata", {})
    hiers = HIERARCHIES
    if args.hierarchies:
        hiers = [h for h in HIERARCHIES if h in args.hierarchies.split(",")]
    if args.smoke:
        hiers = ["city"]
    entity_rows = []; hierarchy_parents = {}
    for h in hiers:
        H = build_homograph(h, enc, scale, full)
        parent, pinfo, erows = run_homograph_hierarchy(h, H, rng, FROZEN, scale)
        if args.max_entities and len(erows) > args.max_entities:
            erows = erows[:args.max_entities]
        hierarchy_parents[h] = dict(parent=parent, parent_pos_firing=pinfo.get("parent_pos_firing"),
                                    parent_unresolved=pinfo.get("parent_unresolved"),
                                    n_responsive=pinfo.get("n_responsive"))
        entity_rows += erows
        del H; gc.collect(); core._cuda_empty()

    enc.free(); del enc; gc.collect(); core._cuda_empty()

    # ---- M4 aggregation + verdict + M7 breadth ----
    agg, breadth, php = aggregate_and_verdict(entity_rows, spelling_results)
    assemble_and_save(derivation, deriv_results, spelling_results, entity_rows, hierarchy_parents,
                      frozen, FROZEN, bacc_h, bacc_j, agg, breadth, php, gating, spelling_usability,
                      args, scale, homograph_path, full_meta)


if __name__ == "__main__":
    main()
