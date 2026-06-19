#!/usr/bin/env python3
"""
M3/M4/M8 (+M5/M7) Integrity-Lock Consolidation evaluation (iter-6).

PURE CPU-only re-analysis ($0, no GPU, no encoding, no LLM) over THREE existing
experiment JSONs plus the iter-5 consolidation eval. We RECOMPUTE the reviewer-flagged
headline numbers and LOCK them as cross-checked, drop-in paper wording.

REVIEWER MANDATE LABELS (this file):
  M3 = cross-dictionary selectivity-artifact (NEW load-bearing: 65k divide-by-epsilon)
  M4 = router out-of-sample Wilson-CI restatement (NEW: demote to exploratory diagnostic)
  M8 = honest counting (carry from D4 iter-5 eval, RE-VERIFY selectivity from D2)
  M5 = United-States consistency (drop-in)
  M7 = grouping -> label-free discovery procedure (drop-in)

NOTE on label mapping: the iter-5 consolidation eval (D4) used DIFFERENT internal
labels (its M3=honest-counting, M4=selectivity, M5=control, M8=transparency). We map by
CONTENT, not letter-number. Source experiment JSONs (D1/D2/D3) are ground truth; we
COMPUTE every value then COMPARE to the stored/expected value and report mismatches.

Output: eval_out.json (schema exp_eval_sol_out: metrics_agg + datasets; the rich
M3/M4/M8/M5/M7/cross_checks blocks live under metadata).
"""
from __future__ import annotations

import gc
import glob
import json
import os
import resource
import sys
from pathlib import Path

import numpy as np
from loguru import logger
from scipy.stats import spearmanr

os.environ.setdefault("HF_HUB_OFFLINE", "1")  # defensive; no network is used

# --------------------------------------------------------------------------- logging
WS = Path("/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_evaluation_1")
(WS / "logs").mkdir(exist_ok=True)
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(str(WS / "logs" / "run.log"), rotation="30 MB", level="DEBUG")

# Modest RAM cap (we load one ~1.4MB json at a time; 6GB is ample in a 29GB box).
_RAM = 6 * 1024**3
resource.setrlimit(resource.RLIMIT_AS, (_RAM * 3, _RAM * 3))

# --------------------------------------------------------------------------- inputs
# depends_on may stage each dependency's full_method_out.json into our workspace;
# prefer the staged copy, fall back to the absolute source path.
SRC = {
    "D1": {  # iter-5 exp2 cross-dictionary 65k  [crossdict-selectivity]
        "id": "art_4L1MZxvWYlGd",
        "abs": "/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_2/full_method_out.json",
        "staged_glob": "D1_*full_method_out.json",
    },
    "D2": {  # iter-4 exp2 surgical 16k          [surgical-selectivity]
        "id": "art_0CZwPjG2YMCf",
        "abs": "/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_2/full_method_out.json",
        "staged_glob": "D2_*full_method_out.json",
    },
    "D3": {  # iter-5 exp3 router                [router-ci]
        "id": "art_4q5Om8wdqZuz",
        "abs": "/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_3/full_method_out.json",
        "staged_glob": "D3_*full_method_out.json",
    },
    "D4": {  # iter-5 consolidation eval         [honest-counting template]
        "id": "art_-k4Yg-l4NaNO",
        "abs": "/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_evaluation_1/full_eval_out.json",
        "staged_glob": "D4_*full_eval_out.json",
    },
}

# numerical-precision floors for the floor-limited lower-bound reporting (M3.3)
PRECISION_REPORT_FLOOR = 1e-4   # conservative next-token-KL collateral precision bound
REF_16K_COLLATERAL = 2.876e-5   # smallest reliably-MEASURED collateral (16k Georgia)
EPS_DENOM = 1e-8                # the divide-by-epsilon denominator used in the stored ratios

GAPS: list[dict] = []
SRC_FILE_USED: dict[str, str] = {}
CROSS: list[dict] = []


# --------------------------------------------------------------------------- helpers
def load_dep(tag: str) -> dict:
    cfg = SRC[tag]
    # prefer a staged copy in the workspace
    for cand in sorted(WS.glob(cfg["staged_glob"])):
        logger.info(f"[{tag}] loading STAGED {cand.name}")
        SRC_FILE_USED[tag] = str(cand)
        return json.loads(cand.read_text())
    p = Path(cfg["abs"])
    if p.exists():
        logger.info(f"[{tag}] loading {p}")
        SRC_FILE_USED[tag] = str(p)
        return json.loads(p.read_text())
    raise FileNotFoundError(f"No method_out json found for {tag} ({cfg['id']})")


def approx(a, b, tol=1e-2) -> bool:
    try:
        return abs(float(a) - float(b)) <= tol
    except (TypeError, ValueError):
        return False


def num(x):
    if isinstance(x, bool):
        return int(x)
    return x


def xcheck(name: str, computed, expected, match: bool, note: str = ""):
    CROSS.append({"name": name, "computed": computed, "expected": expected,
                  "match": bool(match), "note": note})
    if not match:
        logger.warning(f"  MISMATCH {name}: computed={computed} expected={expected} :: {note}")


def includes_half(ci) -> bool:
    try:
        return float(ci[0]) <= 0.5 <= float(ci[1])
    except (TypeError, ValueError, IndexError):
        return False


# =========================================================================== M3
def compute_M3(d1: dict, d2: dict) -> dict:
    rt = d1["metadata"]["replication_tables"]
    sg = rt["65k"]["surgical"]
    cases_raw = sg["cases"]
    regime_split = rt["65k"]["regime_split"]
    ref16 = sg["ref_16k_georgia"]

    # ---- M3.1/M3.2 per-case classification
    table = []
    for c in cases_raw:
        kg_coll = c.get("kg_collateral")
        verdict = c.get("verdict")
        regime = c.get("regime")
        floor_limited = (kg_coll == 0.0)
        no_on_target = (verdict == "NO_ON_TARGET_EFFECT")
        exclude = floor_limited or no_on_target
        on_target_recovered = (c.get("selectivity_ratio") * EPS_DENOM) if floor_limited else None
        row = {
            "family": c.get("family"),
            "subcontext": c.get("subcontext"),
            "absorber": c.get("absorber"),
            "verdict": verdict,
            "regime": regime,
            "selectivity_ratio": c.get("selectivity_ratio"),
            "kg_collateral": kg_coll,
            "dense_collateral": c.get("dense_collateral"),
            "kg_offtarget_footprint": c.get("kg_offtarget_footprint"),
            "firing_jaccard": c.get("firing_jaccard"),
            "parent_recall_hole": c.get("parent_recall_hole"),
            "floor_limited": bool(floor_limited),
            "no_on_target": bool(no_on_target),
            "exclude_from_stats": bool(exclude),
            "on_target_recovered": on_target_recovered,
        }
        # floor-limited lower bounds
        if floor_limited:
            row["floor_bound_at_1e-4"] = on_target_recovered / PRECISION_REPORT_FLOOR
            row["floor_bound_ref_16k"] = on_target_recovered / REF_16K_COLLATERAL
        table.append(row)

    n_floor_limited = sum(1 for r in table if r["floor_limited"])
    n_floor_limited_with_on_target = sum(
        1 for r in table if r["floor_limited"] and r["verdict"] != "NO_ON_TARGET_EFFECT")
    n_no_on_target = sum(1 for r in table if r["no_on_target"])
    n_excluded = sum(1 for r in table if r["exclude_from_stats"])

    # ---- M3.4 corrected regime mean/median over ABSORPTION-regime cases
    absorption_cases = [r for r in table if r["regime"] == "absorption"]
    # PRIMARY: exclude floor_limited OR no_on_target
    kept_primary = [r for r in absorption_cases if not r["exclude_from_stats"]]
    sel_primary = [r["selectivity_ratio"] for r in kept_primary]
    mean_primary = float(np.mean(sel_primary)) if sel_primary else None
    median_primary = float(np.median(sel_primary)) if sel_primary else None
    # SECONDARY: exclude ONLY the two divide-by-epsilon artifacts {46143, 60904}
    artifacts = {46143, 60904}
    kept_secondary = [r for r in absorption_cases if r["absorber"] not in artifacts]
    sel_secondary = [r["selectivity_ratio"] for r in kept_secondary]
    mean_secondary = float(np.mean(sel_secondary)) if sel_secondary else None
    median_secondary = float(np.median(sel_secondary)) if sel_secondary else None

    # ---- recompute the stored regime mean to confirm the divide-by-epsilon inflation
    sel_all_absorption = [r["selectivity_ratio"] for r in absorption_cases]
    recomputed_stored_mean = float(np.mean(sel_all_absorption)) if sel_all_absorption else None

    # ---- M3.5 comparably-surgical figures
    geo65 = next(r for r in table if r["absorber"] == 46143)
    geo16_d1 = float(ref16["selectivity_ratio"])
    geo16_d2 = next(c["headline_selectivity_ratio"] for c in d2["metadata"]["per_case"]
                    if c.get("target_subcontext") == "Georgia" and c.get("absorber_latent") == 16009)
    georgia_floor_1e4 = geo65["floor_bound_at_1e-4"]
    georgia_floor_ref = geo65["floor_bound_ref_16k"]

    # ---- l9 partial note (honest layer-dependence)
    l9 = rt.get("l9_16k", {})
    l9_holes = l9.get("homograph_holes", {}).get("per_country", {})
    l9_surgical_cases = {f"{c['subcontext']}/{c['absorber']}": c for c in l9.get("surgical", {}).get("cases", [])}
    l9_note = {
        "georgia_recall_hole": l9_holes.get("Georgia", {}).get("recall_hole"),
        "jordan_recall_hole": l9_holes.get("Jordan", {}).get("recall_hole"),
        "jordan_surgical_selectivity": next(
            (c["selectivity_ratio"] for c in l9.get("surgical", {}).get("cases", [])
             if c["subcontext"] == "Jordan"), None),
        "interpretation": (
            "Layer-9 width-16k is a DIFFERENT (layer,width) point: a cleaner layer-9 parent "
            "means Georgia LOSES its absorption hole (recall-hole ~0.003) while Jordan KEEPS "
            "its hole (recall-hole ~0.536) and yields a confirmed surgical edit (~2376x). This "
            "is honest (layer,width)-dependence of WHICH token absorbs, not a contradiction of "
            "the layer-12 65k result."),
    }

    comparably_surgical_statement = (
        f"16k Georgia ({geo16_d1:.2f}x, collateral {REF_16K_COLLATERAL:.3g}) and 65k Georgia "
        f"(collateral exactly 0.0, below numerical precision; on-target {geo65['on_target_recovered']:.5f} "
        f"recovered as selectivity*1e-8, matching its dense collateral {geo65['dense_collateral']:.5f}) "
        f"are COMPARABLY surgical -- both have collateral at/below ~1e-5 precision. The 3.7e6x-vs-"
        f"{geo16_d1:.0f}x gap is a divide-by-epsilon artifact, not a real ~2000x improvement.")

    paper_wording = (
        f"On the 4x-wider 65k SAE the absorption single-absorber edits remain surgical, but two "
        f"of nine cases are divide-by-epsilon artifacts: the Georgia absorber (46143) and a Jordan "
        f"candidate (60904) have kg_collateral=0 exactly, so the stored ratios "
        f"({geo65['selectivity_ratio']:.0f}x; "
        f"{next(r['selectivity_ratio'] for r in table if r['absorber'] == 60904):.0f}x with NO "
        f"measurable on-target effect) reduce to on_target/1e-8. Excluding floor-limited (collateral "
        f"below numerical precision) and no-on-target-effect cases, the corrected 65k absorption mean "
        f"selectivity is {mean_primary:.1f}x (median {median_primary:.1f}x, n={len(kept_primary)}), "
        f"not {regime_split['absorption_mean_selectivity']:.0f}x; the more lenient rule that keeps the "
        f"tiny null cases gives mean {mean_secondary:.1f}x (median {median_secondary:.1f}x, "
        f"n={len(kept_secondary)}). The 65k Georgia edit (collateral below precision; reported as "
        f"floor-limited >= ~{georgia_floor_1e4:.0f}x at a 1e-4 collateral floor, or >= "
        f"~{georgia_floor_ref:.0f}x referenced to the smallest reliably-measured 16k collateral "
        f"2.9e-5) is COMPARABLY surgical to the 16k Georgia edit ({geo16_d1:.0f}x, collateral 2.9e-5) "
        f"-- the dictionaries are comparably surgical, not 2000x apart.")

    # ---- cross-checks (integrity lock)
    xcheck("M3_65k_regime_split.absorption_mean_selectivity==466996.718",
           regime_split["absorption_mean_selectivity"], 466996.718,
           approx(regime_split["absorption_mean_selectivity"], 466996.718, tol=1e-2),
           "stored inflated regime mean (divide-by-epsilon)")
    xcheck("M3_65k_n_absorption==8", regime_split["n_absorption"], 8,
           regime_split["n_absorption"] == 8, "stored absorption-regime case count")
    xcheck("M3_recomputed_stored_mean_matches_stored",
           round(recomputed_stored_mean, 3), 466996.718,
           approx(recomputed_stored_mean, 466996.718, tol=1.0),
           "we reproduce the stored 466997x by averaging ALL 8 absorption selectivity_ratios "
           "(incl. the two divide-by-epsilon artifacts), confirming it is an artifact")
    xcheck("M3_Georgia46143_kg_collateral==0.0", geo65["kg_collateral"], 0.0,
           geo65["kg_collateral"] == 0.0, "floor-limited trigger")
    xcheck("M3_Georgia46143_selectivity==3710589.05", round(geo65["selectivity_ratio"], 2), 3710589.05,
           approx(geo65["selectivity_ratio"], 3710589.05, tol=0.5), "stored 65k Georgia ratio")
    jordan = next(r for r in table if r["absorber"] == 60904)
    xcheck("M3_Jordan60904_verdict==NO_ON_TARGET_EFFECT", jordan["verdict"], "NO_ON_TARGET_EFFECT",
           jordan["verdict"] == "NO_ON_TARGET_EFFECT", "floor-limited + no-on-target")
    xcheck("M3_Jordan60904_kg_collateral==0.0", jordan["kg_collateral"], 0.0,
           jordan["kg_collateral"] == 0.0, "floor-limited trigger")
    xcheck("M3_Georgia_on_target_recovery_matches_dense",
           round(geo65["on_target_recovered"], 5), round(geo65["dense_collateral"], 5),
           approx(geo65["on_target_recovered"], geo65["dense_collateral"], tol=1e-4),
           "on_target = selectivity*1e-8 == dense_collateral confirms the epsilon denominator")
    xcheck("M3_corrected_65k_mean_PRIMARY~721.7", round(mean_primary, 2), 721.72,
           approx(mean_primary, 721.7, tol=1.0),
           f"ACTUAL computed over n={len(kept_primary)} kept absorption cases "
           f"{[r['absorber'] for r in kept_primary]}")
    xcheck("M3_corrected_65k_median_PRIMARY~676.3", round(median_primary, 2), 676.33,
           approx(median_primary, 676.3, tol=1.0), "median of the n=4 PRIMARY kept set")
    xcheck("M3_corrected_65k_mean_SECONDARY~483", round(mean_secondary, 2), 483.06,
           approx(mean_secondary, 483.0, tol=1.5),
           f"exclude ONLY the 2 artifacts {{46143,60904}}, keep tiny nulls; n={len(kept_secondary)}")
    xcheck("M3_corrected_65k_median_SECONDARY~184.6", round(median_secondary, 2), 184.61,
           approx(median_secondary, 184.6, tol=1.0), "median of the n=6 SECONDARY kept set")
    xcheck("M3_16k_Georgia_selectivity==1722.46_D1andD2_agree",
           [round(geo16_d1, 2), round(geo16_d2, 2)], [1722.46, 1722.46],
           approx(geo16_d1, 1722.46, tol=0.5) and approx(geo16_d2, 1722.46, tol=0.5),
           "D1.ref_16k_georgia and D2.per_case both report 1722.46")
    xcheck("M3_n_no_on_target==3", n_no_on_target, 3, n_no_on_target == 3,
           "NO_ON_TARGET_EFFECT cases: Jordan/60904, O-on/54546, T-take/26458")
    # HONEST CORRECTION vs plan metrics-anchor of 1:
    xcheck("M3_n_floor_limited==1 (plan anchor)", n_floor_limited, 1, n_floor_limited == 1,
           f"ACTUAL = {n_floor_limited}: BOTH Georgia/46143 AND Jordan/60904 have kg_collateral==0.0 "
           f"(the plan's metrics-anchor of 1 counts only the floor-limited case that ALSO retains a "
           f"measurable on-target effect, i.e. Georgia; the honest kg_collateral==0 count is 2). "
           f"n_floor_limited_with_on_target_effect={n_floor_limited_with_on_target}.")
    xcheck("M3_n_excluded_from_stats==4", n_excluded, 4, n_excluded == 4,
           "union of floor_limited{46143,60904} and no_on_target{60904,54546,26458} = "
           "{46143,60904,54546,26458}")

    logger.info(f"M3: corrected PRIMARY mean={mean_primary:.2f} median={median_primary:.2f} "
                f"(n={len(kept_primary)}); SECONDARY mean={mean_secondary:.2f} "
                f"median={median_secondary:.2f} (n={len(kept_secondary)}); "
                f"floor_limited={n_floor_limited} no_on_target={n_no_on_target} excluded={n_excluded}")

    return {
        "source_path": f"D1 {SRC['D1']['id']} metadata.replication_tables['65k'] + "
                       f"D2 {SRC['D2']['id']} metadata.per_case (16k Georgia)",
        "per_case_table": table,
        "n_cases": len(table),
        "n_floor_limited": n_floor_limited,
        "n_floor_limited_with_on_target_effect": n_floor_limited_with_on_target,
        "n_no_on_target": n_no_on_target,
        "n_excluded_from_stats": n_excluded,
        "stored_regime_split": regime_split,
        "recomputed_stored_absorption_mean": recomputed_stored_mean,
        "corrected_primary": {
            "rule": "exclude floor_limited OR no_on_target from absorption-regime cases",
            "kept_absorbers": [r["absorber"] for r in kept_primary],
            "selectivities": sel_primary, "n": len(kept_primary),
            "mean": mean_primary, "median": median_primary},
        "corrected_secondary": {
            "rule": "exclude ONLY the two divide-by-epsilon artifacts {46143, 60904}",
            "kept_absorbers": [r["absorber"] for r in kept_secondary],
            "selectivities": sel_secondary, "n": len(kept_secondary),
            "mean": mean_secondary, "median": median_secondary},
        "floor_limited_bounds": {
            "Georgia_46143": {
                "on_target_recovered": geo65["on_target_recovered"],
                "dense_collateral": geo65["dense_collateral"],
                "floor_bound_at_1e-4_collateral_floor": georgia_floor_1e4,
                "floor_bound_ref_16k_collateral_2.876e-5": georgia_floor_ref},
            "Jordan_60904": {
                "on_target_recovered": jordan["on_target_recovered"],
                "dense_collateral": jordan["dense_collateral"],
                "note": "negligible on-target (consistent with NO_ON_TARGET_EFFECT)"}},
        "comparably_surgical": {
            "georgia_16k_selectivity_D1": geo16_d1,
            "georgia_16k_selectivity_D2": geo16_d2,
            "georgia_16k_collateral": REF_16K_COLLATERAL,
            "georgia_65k_collateral": 0.0,
            "statement": comparably_surgical_statement},
        "l9_partial_note": l9_note,
        "paper_wording": paper_wording,
    }


# =========================================================================== M4
def compute_M4(d3: dict) -> dict:
    md = d3["metadata"]
    php = md["prospective_hitrate_primary"]
    ph = md.get("prospective_hitrate", {})

    strata = {}
    for key in ("absorption_predicted", "cofiring_predicted", "combined_all"):
        s = php[key]
        strata[key] = {
            "hits": s["hits"], "n": s["n"], "rate": s["rate"],
            "wilson_ci": s["wilson_ci"], "includes_half": includes_half(s["wilson_ci"]),
        }

    vs_h = ph.get("combined_all_vs_h", {})
    vs_h_block = {
        "hits": vs_h.get("hits"), "n": vs_h.get("n"), "rate": vs_h.get("rate"),
        "wilson_ci": vs_h.get("wilson_ci"), "includes_half": includes_half(vs_h.get("wilson_ci", [])),
        "flag": "SECONDARY / NON-PRIMARY: uses unit-beats-h-pool ground truth, NOT the primary "
                "sign(auc_unit - auc_a). Do NOT cherry-pick this as 'the router works'.",
    }

    # ---- F/M/W over-prediction (new spelling letters)
    new_letters = []
    for r in md.get("new_letter_report", []):
        new_letters.append({
            "letter": r.get("letter"),
            "predicted_regime": r.get("predicted_regime"),
            "ground_truth_regime": r.get("ground_truth_regime"),
            "recall_hole_max": r.get("recall_hole_max"),
            "jaccard_median": r.get("jaccard_median"),
            "delta_vs_a": r.get("delta_vs_a"),
            "hit_vs_a": r.get("hit_vs_a"),
        })
    over_pred = [r["letter"] for r in new_letters
                 if r["predicted_regime"] == "absorption" and r["ground_truth_regime"] == "co_firing"]
    correct_abs = [r["letter"] for r in new_letters
                   if r["predicted_regime"] == "absorption" and r["ground_truth_regime"] == "absorption"]

    primary_rule = md.get("primary_rule", {})
    tau_h = primary_rule.get("tau_h_alone")
    bal_acc = primary_rule.get("balanced_acc")

    # ---- demote-or-validated fork: scan iter-6 run tree for a prospective-expansion experiment
    scan_root = "/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art"
    validated_artifact = None
    scanned = sorted(glob.glob(f"{scan_root}/*/full_method_out.json"))
    for fp in scanned:
        try:
            j = json.loads(Path(fp).read_text())
            ap = (j.get("metadata", {}).get("prospective_hitrate_primary", {})
                  .get("absorption_predicted", {}))
            ci = ap.get("wilson_ci")
            if ci and not includes_half(ci):  # CI EXCLUDES 0.5 -> validated
                validated_artifact = {"path": fp, "absorption_predicted": ap}
                break
        except (json.JSONDecodeError, OSError):
            continue
    decision = "VALIDATED" if validated_artifact else "DEMOTE"

    if decision == "DEMOTE":
        paper_wording = (
            f"The recall-hole router is derivation-perfect (balanced accuracy {bal_acc:.1f} on 12 "
            f"derivation concepts) but OUT-OF-SAMPLE-UNVALIDATED: on the held-out prospective set the "
            f"absorption-predicted hit-rate is exactly chance "
            f"({strata['absorption_predicted']['hits']}/{strata['absorption_predicted']['n']}="
            f"{strata['absorption_predicted']['rate']:.2f}, Wilson 95% CI "
            f"[{strata['absorption_predicted']['wilson_ci'][0]:.3f},"
            f"{strata['absorption_predicted']['wilson_ci'][1]:.3f}]) and the combined rate is "
            f"{strata['combined_all']['hits']}/{strata['combined_all']['n']}="
            f"{strata['combined_all']['rate']:.2f} (Wilson [{strata['combined_all']['wilson_ci'][0]:.3f},"
            f"{strata['combined_all']['wilson_ci'][1]:.3f}]) -- both CIs INCLUDE 0.5 -- and recall-hole=1.0 "
            f"over-predicts absorption on new spelling letters {'/'.join(over_pred)} (which measure "
            f"co-firing). We therefore report it as an EXPLORATORY screening DIAGNOSTIC, not a validated "
            f"a-priori predictor.")
    else:
        ap = validated_artifact["absorption_predicted"]
        paper_wording = (
            f"The recall-hole router is derivation-perfect (balanced accuracy {bal_acc:.1f}) AND "
            f"out-of-sample VALIDATED: on an expanded prospective set the absorption-predicted hit-rate "
            f"is {ap.get('hits')}/{ap.get('n')}={ap.get('rate'):.2f} with Wilson 95% CI "
            f"[{ap['wilson_ci'][0]:.3f},{ap['wilson_ci'][1]:.3f}] EXCLUDING 0.5 "
            f"(artifact: {validated_artifact['path']}).")

    # ---- cross-checks
    xcheck("M4_absorption_predicted_rate==0.5", strata["absorption_predicted"]["rate"], 0.5,
           approx(strata["absorption_predicted"]["rate"], 0.5, tol=1e-9), "3/6 exact chance")
    xcheck("M4_absorption_predicted_ci_includes_0.5", int(strata["absorption_predicted"]["includes_half"]),
           1, strata["absorption_predicted"]["includes_half"],
           f"Wilson CI {strata['absorption_predicted']['wilson_ci']}")
    xcheck("M4_absorption_predicted_ci_lo==0.1876",
           round(strata["absorption_predicted"]["wilson_ci"][0], 4), 0.1876,
           approx(strata["absorption_predicted"]["wilson_ci"][0], 0.1876, tol=1e-3), "Wilson lower")
    xcheck("M4_absorption_predicted_ci_hi==0.8124",
           round(strata["absorption_predicted"]["wilson_ci"][1], 4), 0.8124,
           approx(strata["absorption_predicted"]["wilson_ci"][1], 0.8124, tol=1e-3), "Wilson upper")
    xcheck("M4_cofiring_predicted_ci_includes_0.5", int(strata["cofiring_predicted"]["includes_half"]),
           1, strata["cofiring_predicted"]["includes_half"],
           f"8/12={strata['cofiring_predicted']['rate']:.4f}, CI {strata['cofiring_predicted']['wilson_ci']}")
    xcheck("M4_combined_rate==0.6111", round(strata["combined_all"]["rate"], 4), 0.6111,
           approx(strata["combined_all"]["rate"], 0.6111, tol=1e-3), "11/18")
    xcheck("M4_combined_ci_includes_0.5", int(strata["combined_all"]["includes_half"]), 1,
           strata["combined_all"]["includes_half"], f"Wilson CI {strata['combined_all']['wilson_ci']}")
    xcheck("M4_vs_h_EXCLUDES_0.5_secondary", int(vs_h_block["includes_half"]), 0,
           vs_h_block["includes_half"] is False,
           f"14/19={vs_h.get('rate'):.4f} CI {vs_h.get('wilson_ci')} -- SECONDARY vs-h ground truth, "
           f"explicitly NOT the headline; flagged non-primary so the paper does not cherry-pick it")
    xcheck("M4_FMW_over_predict_absorption_measure_cofiring",
           "/".join(sorted(over_pred)), "F/M/W", set(over_pred) == {"F", "M", "W"},
           f"recall-hole=1.0 predicts absorption but ground-truth co-firing; correct absorption "
           f"wins on {'/'.join(sorted(correct_abs))}")
    xcheck("M4_tau_h_alone==0.77949", round(tau_h, 5), 0.77949, approx(tau_h, 0.7794871794871795, tol=1e-4),
           "frozen recall-hole threshold")
    xcheck("M4_derivation_balanced_acc==1.0", bal_acc, 1.0, approx(bal_acc, 1.0, tol=1e-9),
           "recall-hole-alone balanced accuracy on 12 derivation concepts")
    xcheck("M4_demote_decision (no iter6 expansion CI-excludes-0.5)",
           decision, "DEMOTE", decision == "DEMOTE",
           f"scanned {len(scanned)} iter-6 full_method_out.json; "
           f"{'found validated expansion' if validated_artifact else 'no expansion experiment with an '
           'absorption-predicted Wilson CI excluding 0.5 -> DEMOTE is correct/default'}")

    logger.info(f"M4: abs_pred 3/6=0.5 incl_half={strata['absorption_predicted']['includes_half']} | "
                f"combined 11/18=0.611 incl_half={strata['combined_all']['includes_half']} | "
                f"vs_h 14/19 incl_half={vs_h_block['includes_half']} | over_pred={over_pred} | "
                f"decision={decision} (scanned {len(scanned)})")

    return {
        "source_path": f"D3 {SRC['D3']['id']} metadata.prospective_hitrate_primary / "
                       f"prospective_hitrate / new_letter_report / primary_rule",
        "prospective_strata_primary": strata,
        "vs_h_secondary": vs_h_block,
        "new_letter_directionality": new_letters,
        "over_prediction_letters": over_pred,
        "correct_absorption_letters": correct_abs,
        "router_wrong_in_both_directions": True,
        "derivation": {"tau_h_alone": tau_h, "balanced_acc": bal_acc,
                       "definition": primary_rule.get("definition_string"),
                       "conjunction_beats_primary_out_of_sample":
                           md.get("conjunction_beats_primary_out_of_sample")},
        "demote_or_validated": {
            "decision": decision,
            "scanned_n_files": len(scanned),
            "validated_artifact": validated_artifact,
            "note": "depends_on does NOT include a prospective-expansion experiment; the iter-6 run "
                    "tree contains no completed full_method_out.json with an absorption-predicted "
                    "Wilson CI excluding 0.5, so DEMOTE is the default and correct outcome."},
        "paper_wording": paper_wording,
    }


# =========================================================================== M8
def compute_M8(d2: dict, d4: dict) -> dict:
    """RE-VERIFY selectivity from D2 (source); CARRY counting/control/transparency from D4."""
    md4 = d4["metadata"]
    d4_count = md4["M3_honest_counting"]
    d4_sel = md4["M4_selectivity"]
    d4_ctrl = md4["M5_control_wording"]
    d4_trans = md4["M8_transparency"]

    # ---------- (c)/(d) RE-VERIFY selectivity directly from D2 per_case ----------
    per_case = d2["metadata"]["per_case"]
    cases = [{
        "family": c.get("family"), "subcontext": c.get("target_subcontext"),
        "absorber": c.get("absorber_latent"), "precision": c.get("absorber_precision"),
        "selectivity": c.get("headline_selectivity_ratio"), "verdict": c.get("verdict"),
        "regime": c.get("regime"),
    } for c in per_case]
    absorption6 = [c for c in cases if c["regime"] == "absorption"]
    surgical5 = [c for c in cases if c["verdict"] == "SURGICAL_EDIT_CONFIRMED"]
    abs_sel = [c["selectivity"] for c in absorption6]
    sur_sel = [c["selectivity"] for c in surgical5]
    abs_mean = float(np.mean(abs_sel)); abs_med = float(np.median(abs_sel))
    sur_mean = float(np.mean(sur_sel)); sur_med = float(np.median(sur_sel))

    def sp(group):
        if len(group) < 3:
            return {"rho": None, "p": None, "n": len(group)}
        r = spearmanr([g["precision"] for g in group], [g["selectivity"] for g in group])
        return {"rho": float(r.statistic), "p": float(r.pvalue), "n": len(group)}
    taxonomic5 = [c for c in cases if c["family"] == "taxonomic"]
    sp_all = sp(cases); sp_abs = sp(absorption6); sp_tax = sp(taxonomic5)

    # ---------- (a)/(b) CARRY counting (depends on iter-4 exp1 NOT in iter-6 deps) ----------
    n_tested = d4_count["n_variants_tested"]
    n_survive = d4_count["n_variants_survive"]
    n_distinct = d4_count["n_distinct_holes"]
    n_double = len(d4_count["double_counted_subcontexts"])
    n_nonhole = len(d4_count["non_hole_survivors"])
    recon = d4_count["reconciliation_identity"]
    per_family = d4_count["per_family"]

    # ---------- (f) CARRY member-labeling ----------
    ml = d4_trans["member_labeling_summary"]

    # ---------- (e) CARRY control (random SINGLE-latent) ----------
    n_p95 = d4_ctrl["n_exceed_p95"]; n_p99 = d4_ctrl["n_exceed_p99"]
    n_surv_hole = d4_ctrl["n_surviving_hole_variants"]

    # ---------- (g) numeric below-gate ----------
    numeric_below_gate = {"digit_token_cosine": 0.876, "gate": 0.90, "below_gate": True,
                          "note": "numeric absorption testbed is eligibility+pooling only; the form-free "
                                  "absorption diagnostic is unconfirmed because digit-token cosine 0.876 "
                                  "< 0.90 gating threshold (carried; recorded descriptively in D1 65k "
                                  "gating as well)."}

    # ---------- paper wording: count + selectivity (reuse D4 verbatim) ----------
    pw_count = d4_count["paper_wording"]
    pw_sel = d4_sel["paper_wording"]
    pw_softened = d4_sel["softened_verdict"]

    # ---------- cross-checks: identity + re-verified selectivity ----------
    xcheck("M8_22==30-6-2", n_distinct, n_survive - n_double - n_nonhole,
           n_distinct == n_survive - n_double - n_nonhole,
           f"{n_distinct} == {n_survive} - {n_double} double-count-redundant - {n_nonhole} non-hole "
           f"(carried from D4; the iter-5 eval already honestly corrected the original plan's ~23 to 22 "
           f"and 1 non-hole to 2)")
    xcheck("M8_per_family_distinct_spelling13_tax3_num6",
           [per_family["spelling"]["n_distinct_holes"], per_family["taxonomic"]["n_distinct_holes"],
            per_family["numeric"]["n_distinct_holes"]], [13, 3, 6],
           per_family["spelling"]["n_distinct_holes"] == 13
           and per_family["taxonomic"]["n_distinct_holes"] == 3
           and per_family["numeric"]["n_distinct_holes"] == 6, "carried per-family distinct holes")
    xcheck("M8_per_family_survive_spelling14_tax6_num10",
           [per_family["spelling"]["n_variants_survive"], per_family["taxonomic"]["n_variants_survive"],
            per_family["numeric"]["n_variants_survive"]], [14, 6, 10],
           per_family["spelling"]["n_variants_survive"] == 14
           and per_family["taxonomic"]["n_variants_survive"] == 6
           and per_family["numeric"]["n_variants_survive"] == 10, "carried per-family FDR survivors")
    xcheck("M8_absorption6_mean==1452.47 (re-verified from D2)", round(abs_mean, 2), 1452.47,
           approx(abs_mean, 1452.4715, tol=1e-2), "recomputed mean of n=6 absorption set from D2 per_case")
    xcheck("M8_absorption6_median==1262.21 (re-verified from D2)", round(abs_med, 2), 1262.21,
           approx(abs_med, 1262.21, tol=0.5), "recomputed median (avg of 801.96, 1722.46)")
    xcheck("M8_surgical5_median==1722.46 (re-verified from D2)", round(sur_med, 2), 1722.46,
           approx(sur_med, 1722.4595, tol=0.5), "recomputed median of n=5 surgical set from D2")
    xcheck("M8_mean_not_median_clarification", round(abs_mean, 2), 1452.47,
           approx(abs_mean, 1452.4715, tol=1e-2),
           "the draft's '1452x median' is in fact the MEAN of the n=6 absorption set")
    xcheck("M8_taxonomic5_rho==0.90 (NOT 1.0)", round(sp_tax["rho"], 4), 0.9,
           approx(sp_tax["rho"], 0.9, tol=1e-3),
           f"recomputed within-taxonomic Spearman rho={sp_tax['rho']:.4f}, p={sp_tax['p']:.4f}; NOT 1.0 "
           f"because US-846 (prec 0.973) has lower selectivity (213.5) than Georgia (prec 0.955 -> 1722.5)")
    xcheck("M8_all7_rho==0.679 (re-verified)", round(sp_all["rho"], 4), 0.6786,
           approx(sp_all["rho"], 0.6786, tol=1e-3), f"p={sp_all['p']:.4f}")
    xcheck("M8_absorption6_rho==0.714 (re-verified)", round(sp_abs["rho"], 4), 0.7143,
           approx(sp_abs["rho"], 0.7143, tol=1e-3), f"p={sp_abs['p']:.4f}")
    xcheck("M8_member_labeling_gap==0.6344", round(ml["gap"], 4), 0.6344,
           approx(ml["gap"], 0.6344, tol=1e-2),
           f"agreement {ml['overall_agreement']:.3f} vs shuffle null {ml['shuffle_null']:.3f}")
    xcheck("M8_member_labeling_gap_CI==[0.545,0.724]",
           [round(ml["gap_ci_lo"], 3), round(ml["gap_ci_hi"], 3)], [0.545, 0.724],
           approx(ml["gap_ci_lo"], 0.5445, 1e-2) and approx(ml["gap_ci_hi"], 0.7243, 1e-2),
           "carried gap bootstrap CI (excludes 0)")
    xcheck("M8_control_28_of_28_exceed_p95", [n_p95, n_surv_hole], [28, 28],
           n_p95 == 28 and n_surv_hole == 28,
           "random SINGLE content-responsive-latent control: 28/28 surviving hole-variants exceed p95")
    xcheck("M8_control_23_of_28_exceed_p99", n_p99, 23, n_p99 == 23,
           "23/28 exceed p99 of the single-latent-addition gain distribution (NOT a union/max-pool)")

    logger.info(f"M8: re-verified abs_mean={abs_mean:.2f} abs_med={abs_med:.2f} sur_med={sur_med:.2f} "
                f"rho_tax={sp_tax['rho']:.4f}; carried distinct_holes={n_distinct} gap={ml['gap']:.4f}")

    return {
        "source_path": f"counting/control/transparency CARRIED from D4 {SRC['D4']['id']}; "
                       f"selectivity RE-VERIFIED from D2 {SRC['D2']['id']} metadata.per_case",
        "counting": {
            "n_variants_tested": n_tested, "n_variants_survive": n_survive,
            "n_distinct_holes": n_distinct, "n_double_counted_subcontexts": n_double,
            "n_nonhole_survivors": n_nonhole, "reconciliation_identity": recon,
            "double_counted_subcontexts": d4_count["double_counted_subcontexts"],
            "non_hole_survivors": d4_count["non_hole_survivors"], "per_family": per_family,
            "carried_from": SRC["D4"]["id"]},
        "selectivity_reverified": {
            "source": "D2 per_case (recomputed, not carried)",
            "absorption_set_n6": {"members": [f"{c['subcontext']}/{c['absorber']}" for c in absorption6],
                                  "n": len(absorption6), "mean": abs_mean, "median": abs_med,
                                  "selectivities": abs_sel},
            "surgical_set_n5": {"members": [f"{c['subcontext']}/{c['absorber']}" for c in surgical5],
                                "n": len(surgical5), "mean": sur_mean, "median": sur_med,
                                "selectivities": sur_sel},
            "mean_vs_median_clarification": "the previously reported '1452x median' is the MEAN of the "
                                            "n=6 absorption set; the median is 1262.21x.",
            "spearman_all7": sp_all, "spearman_absorption6": sp_abs, "spearman_taxonomic5": sp_tax,
            "cross_family_counterexample": "spelling 'large' (prec 0.571 -> 802x) BEATS taxonomic "
                                           "US-4760 (prec 0.709 -> 7.8x): precision predicts selectivity "
                                           "only WITHIN family"},
        "control_random_single_latent": {
            "implemented_control": d4_ctrl["implemented_control"],
            "n_surviving_hole_variants": n_surv_hole, "n_exceed_p95": n_p95, "n_exceed_p99": n_p99,
            "corrected_wording": d4_ctrl["corrected_wording"],
            "drop_phrasing": "DROP 'full random-addition population' / 'adds every other latent'; it is "
                             "the percentile within the SINGLE-latent-addition gain distribution"},
        "member_labeling": ml,
        "transparency_paper_table": d4_trans.get("paper_table"),
        "numeric_below_gate": numeric_below_gate,
        "paper_wording_count": pw_count,
        "paper_wording_selectivity": pw_sel,
        "paper_wording_softened_precision": pw_softened,
    }


# =========================================================================== M5
def compute_M5(d2: dict) -> dict:
    # verify the 846 single-absorber 16k selectivity from D2 (the rest are carried facts)
    us846 = next((c for c in d2["metadata"]["per_case"]
                  if c.get("target_subcontext") == "United States" and c.get("absorber_latent") == 846),
                 None)
    sel846 = us846["headline_selectivity_ratio"] if us846 else None

    paper_wording = (
        "United States is classified as CO-FIRING (aggregate parent recall-hole 0.20-0.23 < 0.5; router "
        "threshold tau_h 0.78), yet its narrow absorber 846 still yields a surgical single-sub-context "
        f"edit ({sel846:.0f}x at 16k). We present US as a router FALSE-NEGATIVE: CCRG helps even where "
        "the aggregate router predicted it should not. The firing-Jaccard discrepancy (0.04 for the "
        "specific absorber 846 vs 0.20 for the aggregate detector the router uses) reflects that a "
        "precise specialist can exist inside an aggregate that reads co-firing.")

    xcheck("M5_US846_16k_selectivity==213.53", round(sel846, 2), 213.53,
           approx(sel846, 213.5291, tol=0.5), "single narrow absorber 846 surgical edit at 16k (D2)")

    logger.info(f"M5: US846 16k selectivity={sel846:.2f} -> classified CO-FIRING (router false-negative)")
    return {
        "source_path": f"classification carried (M1 recall-hole 0.197 / aggregate 0.23, tau_h 0.78); "
                       f"846 selectivity verified from D2 {SRC['D2']['id']}",
        "classification": "co-firing",
        "aggregate_parent_recall_hole": "0.20-0.23",
        "router_threshold_tau_h": 0.78,
        "narrow_absorber_846_selectivity_16k": sel846,
        "router_false_negative": True,
        "firing_jaccard_specific_846": 0.04,
        "firing_jaccard_aggregate_detector": 0.20,
        "paper_wording": paper_wording,
    }


# =========================================================================== M7
def compute_M7(d2: dict) -> dict:
    # the wins trace to individual latents; verify those 16k absorbers exist in D2
    pc = d2["metadata"]["per_case"]
    geo = any(c.get("absorber_latent") == 16009 for c in pc)
    large = any(c.get("absorber_latent") == 8463 for c in pc)
    us = any(c.get("absorber_latent") == 846 for c in pc)

    paper_wording = (
        "We position the two-track algorithm as a TRAINING-FREE, LABEL-FREE DISCOVERY PROCEDURE: its "
        "demonstrated value is PROPOSING the single precise absorber latent that a marginal-attribution "
        "ranking silently drops (Georgia 16009, large 8463, US 846), not multi-member classification -- "
        "the C-track ties weak baselines (toxicity AUC 0.762 vs (a) 0.765) and set-cover-specific "
        "selection appears on only three slices (first-letter I, D, and taxonomic Georgia).")

    xcheck("M7_discovered_absorbers_present_in_D2", int(geo and large and us), 1, geo and large and us,
           "individual absorbers 16009/8463/846 (the source of the wins) are present in D2 per_case")

    logger.info(f"M7: individual absorbers present geo={geo} large={large} us={us}")
    return {
        "source_path": f"wins trace to individual absorbers in D2 {SRC['D2']['id']} per_case; "
                       f"C-track / set-cover facts carried from prior experiments",
        "wins_trace_to_individual_latents": ["Georgia/16009", "large/8463", "US/846"],
        "ctrack_ties_weak_baselines": {"toxicity_ctrack_auc": 0.762, "baseline_a_auc": 0.765},
        "set_cover_specific_slices": ["first_letter_I", "first_letter_D", "taxonomic_Georgia"],
        "paper_wording": paper_wording,
    }


# =========================================================================== datasets
def build_datasets(M3, M4, M8, d4: dict) -> list:
    ds = []

    # 1) M3_selectivity_cases: 9 (65k) + 7 (16k) = 16 rows
    ex = []
    for r in M3["per_case_table"]:
        ex.append({
            "input": f"65k case: {r['family']}/{r['subcontext']}/{r['absorber']} "
                     f"selectivity={r['selectivity_ratio']:.2f} kg_collateral={r['kg_collateral']:.3e}",
            "output": r["verdict"],
            "predict_floor_limited": "yes" if r["floor_limited"] else "no",
            "predict_no_on_target": "yes" if r["no_on_target"] else "no",
            "predict_excluded_from_stats": "yes" if r["exclude_from_stats"] else "no",
            "predict_regime": r["regime"],
            "metadata_dictionary": "65k",
            "metadata_dense_collateral": r["dense_collateral"],
            "metadata_firing_jaccard": r["firing_jaccard"],
            "metadata_on_target_recovered": r["on_target_recovered"],
            "eval_selectivity_ratio": float(r["selectivity_ratio"]),
            "eval_kg_collateral": float(r["kg_collateral"]),
            "eval_excluded": int(r["exclude_from_stats"]),
        })
    for c in d4["metadata"]["M4_selectivity"]["cases"]:  # the 7 16k reference cases (from D2 via D4)
        ex.append({
            "input": f"16k reference case: {c['family']}/{c['target_subcontext']}/{c['absorber_latent']} "
                     f"selectivity={c['headline_selectivity_ratio']:.2f}",
            "output": c["verdict"],
            "predict_floor_limited": "no",
            "predict_no_on_target": "no",
            "predict_excluded_from_stats": "no",
            "predict_regime": c["regime"],
            "metadata_dictionary": "16k",
            "metadata_absorber_precision": c.get("absorber_precision"),
            "eval_selectivity_ratio": float(c["headline_selectivity_ratio"]),
            "eval_kg_collateral": -1.0,
            "eval_excluded": 0,
        })
    ds.append({"dataset": "M3_selectivity_cases", "examples": ex})

    # 2) M4_router_prospective_strata: 3 primary strata + vs-h secondary = 4 rows
    ex = []
    for key, s in M4["prospective_strata_primary"].items():
        ex.append({
            "input": f"M4 prospective stratum: {key} hits={s['hits']}/{s['n']} "
                     f"Wilson CI [{s['wilson_ci'][0]:.3f},{s['wilson_ci'][1]:.3f}]",
            "output": f"rate={s['rate']:.4f}",
            "predict_includes_half": "yes" if s["includes_half"] else "no",
            "predict_stratum_role": "primary",
            "metadata_hits": s["hits"], "metadata_n": s["n"],
            "metadata_wilson_ci": s["wilson_ci"],
            "eval_rate": float(s["rate"]),
            "eval_includes_half": int(s["includes_half"]),
        })
    vh = M4["vs_h_secondary"]
    ex.append({
        "input": f"M4 SECONDARY (non-primary) stratum: combined_all_vs_h hits={vh['hits']}/{vh['n']} "
                 f"Wilson CI [{vh['wilson_ci'][0]:.3f},{vh['wilson_ci'][1]:.3f}]",
        "output": f"rate={vh['rate']:.4f}",
        "predict_includes_half": "yes" if vh["includes_half"] else "no",
        "predict_stratum_role": "secondary_vs_h",
        "metadata_hits": vh["hits"], "metadata_n": vh["n"], "metadata_wilson_ci": vh["wilson_ci"],
        "metadata_flag": vh["flag"],
        "eval_rate": float(vh["rate"]),
        "eval_includes_half": int(vh["includes_half"]),
    })
    ds.append({"dataset": "M4_router_prospective_strata", "examples": ex})

    # 3) M4_new_letter_directionality: 7 new spelling letters (router wrong in both directions)
    ex = []
    for r in M4["new_letter_directionality"]:
        if r["predicted_regime"] == r["ground_truth_regime"]:
            outcome = "absorption_hit" if r["ground_truth_regime"] == "absorption" else "cofiring_hit"
        else:
            outcome = "miss"
        ex.append({
            "input": f"new spelling letter {r['letter']}: recall_hole_max={r['recall_hole_max']:.3f} "
                     f"predicted={r['predicted_regime']}",
            "output": r["ground_truth_regime"],
            "predict_router_outcome": outcome,
            "predict_regime": r["predicted_regime"],
            "metadata_jaccard_median": r["jaccard_median"],
            "metadata_hit_vs_a": r["hit_vs_a"],
            "eval_recall_hole_max": float(r["recall_hole_max"]),
            "eval_delta_vs_a": float(r["delta_vs_a"]) if r["delta_vs_a"] is not None else 0.0,
        })
    ds.append({"dataset": "M4_new_letter_directionality", "examples": ex})

    # 4) M8_distinct_hole_survivors: reuse D4's 30-survivor table verbatim (schema-valid already)
    d4_surv = next((d["examples"] for d in d4["datasets"] if d["dataset"] == "M3_survivor_table"), None)
    if d4_surv:
        ds.append({"dataset": "M8_distinct_hole_survivors", "examples": d4_surv})
    else:
        GAPS.append({"missing": "D4 M3_survivor_table dataset", "label": "M8_distinct_hole_survivors"})

    # 5) M8_selectivity_reverify: the 7 16k cases (re-verified selectivity from D2 via D4)
    ex = []
    for c in d4["metadata"]["M4_selectivity"]["cases"]:
        in_abs = c["regime"] == "absorption"
        ex.append({
            "input": f"16k selectivity re-verify: {c['target_subcontext']}/{c['absorber_latent']} "
                     f"precision={c['absorber_precision']:.4f}",
            "output": c["verdict"],
            "predict_in_absorption_set": "yes" if in_abs else "no",
            "predict_in_surgical_set": "yes" if c["verdict"] == "SURGICAL_EDIT_CONFIRMED" else "no",
            "metadata_family": c["family"],
            "eval_selectivity": float(c["headline_selectivity_ratio"]),
            "eval_precision": float(c["absorber_precision"]),
        })
    ds.append({"dataset": "M8_selectivity_reverify", "examples": ex})

    return ds


# =========================================================================== main
@logger.catch(reraise=True)
def main():
    logger.info("Loading dependency JSONs (D1 cross-dict, D2 surgical, D3 router, D4 iter5-eval)")
    d1 = load_dep("D1")
    d2 = load_dep("D2")
    d3 = load_dep("D3")
    d4 = load_dep("D4")

    logger.info("Computing M3 (cross-dictionary selectivity artifact)")
    M3 = compute_M3(d1, d2)
    logger.info("Computing M4 (router out-of-sample Wilson-CI)")
    M4 = compute_M4(d3)
    logger.info("Computing M8 (honest counting; re-verify selectivity)")
    M8 = compute_M8(d2, d4)
    logger.info("Computing M5 (US consistency)")
    M5 = compute_M5(d2)
    logger.info("Computing M7 (grouping -> label-free discovery)")
    M7 = compute_M7(d2)

    datasets = build_datasets(M3, M4, M8, d4)

    del d1, d3
    gc.collect()

    all_pass = all(c["match"] for c in CROSS)
    n_pass = sum(1 for c in CROSS if c["match"])

    sp_tax = M8["selectivity_reverified"]["spearman_taxonomic5"]
    sp_all = M8["selectivity_reverified"]["spearman_all7"]
    sp_abs = M8["selectivity_reverified"]["spearman_absorption6"]
    ml = M8["member_labeling"]
    geo_bounds = M3["floor_limited_bounds"]["Georgia_46143"]
    abs6 = M8["selectivity_reverified"]["absorption_set_n6"]
    sur5 = M8["selectivity_reverified"]["surgical_set_n5"]

    metrics_agg = {
        # ---- M3 (NEW load-bearing) ----
        "m3_65k_stored_regime_mean": 466996.718,
        "m3_65k_recomputed_stored_mean": round(M3["recomputed_stored_absorption_mean"], 3),
        "m3_65k_corrected_regime_mean_primary": round(M3["corrected_primary"]["mean"], 4),
        "m3_65k_corrected_regime_median_primary": round(M3["corrected_primary"]["median"], 4),
        "m3_65k_corrected_regime_mean_secondary": round(M3["corrected_secondary"]["mean"], 4),
        "m3_65k_corrected_regime_median_secondary": round(M3["corrected_secondary"]["median"], 4),
        "m3_n_floor_limited": M3["n_floor_limited"],
        "m3_n_floor_limited_with_on_target": M3["n_floor_limited_with_on_target_effect"],
        "m3_n_no_on_target": M3["n_no_on_target"],
        "m3_n_excluded_from_stats": M3["n_excluded_from_stats"],
        "m3_n_kept_primary": M3["corrected_primary"]["n"],
        "m3_georgia_16k_selectivity": 1722.46,
        "m3_georgia_65k_floor_bound_1e4": round(geo_bounds["floor_bound_at_1e-4_collateral_floor"], 2),
        "m3_georgia_65k_floor_bound_ref16k": round(geo_bounds["floor_bound_ref_16k_collateral_2.876e-5"], 2),
        # ---- M4 (NEW) ----
        "m4_absorption_predicted_rate": 0.5,
        "m4_absorption_predicted_ci_lo": round(M4["prospective_strata_primary"]["absorption_predicted"]["wilson_ci"][0], 4),
        "m4_absorption_predicted_ci_hi": round(M4["prospective_strata_primary"]["absorption_predicted"]["wilson_ci"][1], 4),
        "m4_absorption_predicted_includes_half": int(M4["prospective_strata_primary"]["absorption_predicted"]["includes_half"]),
        "m4_cofiring_predicted_rate": round(M4["prospective_strata_primary"]["cofiring_predicted"]["rate"], 4),
        "m4_cofiring_predicted_includes_half": int(M4["prospective_strata_primary"]["cofiring_predicted"]["includes_half"]),
        "m4_combined_rate": round(M4["prospective_strata_primary"]["combined_all"]["rate"], 4),
        "m4_combined_ci_lo": round(M4["prospective_strata_primary"]["combined_all"]["wilson_ci"][0], 4),
        "m4_combined_ci_hi": round(M4["prospective_strata_primary"]["combined_all"]["wilson_ci"][1], 4),
        "m4_combined_includes_half": int(M4["prospective_strata_primary"]["combined_all"]["includes_half"]),
        "m4_vs_h_rate": round(M4["vs_h_secondary"]["rate"], 4),
        "m4_vs_h_includes_half": int(M4["vs_h_secondary"]["includes_half"]),
        "m4_router_demoted": int(M4["demote_or_validated"]["decision"] == "DEMOTE"),
        "m4_tau_h_alone": round(M4["derivation"]["tau_h_alone"], 5),
        "m4_derivation_balanced_acc": M4["derivation"]["balanced_acc"],
        "m4_n_over_prediction_letters": len(M4["over_prediction_letters"]),
        # ---- M8 (carry + re-verify) ----
        "m8_n_variants_tested": M8["counting"]["n_variants_tested"],
        "m8_n_variants_survive": M8["counting"]["n_variants_survive"],
        "m8_n_distinct_holes": M8["counting"]["n_distinct_holes"],
        "m8_n_double_counted": M8["counting"]["n_double_counted_subcontexts"],
        "m8_n_nonhole": M8["counting"]["n_nonhole_survivors"],
        "m8_absorption_mean": round(abs6["mean"], 4),
        "m8_absorption_median": round(abs6["median"], 4),
        "m8_surgical_mean": round(sur5["mean"], 4),
        "m8_surgical_median": round(sur5["median"], 4),
        "m8_taxonomic5_rho": round(sp_tax["rho"], 4),
        "m8_taxonomic5_p": round(sp_tax["p"], 4),
        "m8_all7_rho": round(sp_all["rho"], 4),
        "m8_absorption6_rho": round(sp_abs["rho"], 4),
        "m8_member_labeling_agreement": round(ml["overall_agreement"], 4),
        "m8_member_labeling_shuffle_null": round(ml["shuffle_null"], 4),
        "m8_member_labeling_gap": round(ml["gap"], 4),
        "m8_member_labeling_gap_ci_lo": round(ml["gap_ci_lo"], 4),
        "m8_member_labeling_gap_ci_hi": round(ml["gap_ci_hi"], 4),
        "m8_control_exceed_p95": M8["control_random_single_latent"]["n_exceed_p95"],
        "m8_control_exceed_p99": M8["control_random_single_latent"]["n_exceed_p99"],
        "m8_control_n_surviving_holes": M8["control_random_single_latent"]["n_surviving_hole_variants"],
        "m8_numeric_digit_cosine": 0.876,
        "m8_numeric_below_gate": 1,
        # ---- M5 / M7 ----
        "m5_us_846_selectivity_16k": round(M5["narrow_absorber_846_selectivity_16k"], 2),
        "m5_us_classified_cofiring": 1,
        "m7_ctrack_toxicity_auc": 0.762,
        "m7_ctrack_baseline_a_auc": 0.765,
        # ---- integrity lock ----
        "n_cross_checks": len(CROSS),
        "n_cross_checks_pass": n_pass,
        "all_cross_checks_pass": int(all_pass),
    }

    out = {
        "metadata": {
            "meta": {
                "artifact": "evaluation_iter6_dir5",
                "objective": "M3/M4/M8 (+M5/M7) integrity-lock consolidation: selectivity "
                             "divide-by-epsilon correction, router Wilson-CI restatement, "
                             "honest-counting drop-in paper wording",
                "sources": {"M3": [SRC["D1"]["id"], SRC["D2"]["id"]], "M4": SRC["D3"]["id"],
                            "M8": SRC["D4"]["id"], "M5": SRC["D2"]["id"], "M7": SRC["D2"]["id"]},
                "label_mapping_note": "Reviewer mandate labels: M3=selectivity-artifact, M4=router-CI, "
                                      "M8=honest-counting, M5=US-consistency, M7=grouping-reframe. The "
                                      "iter-5 eval (D4) used DIFFERENT internal labels (its M3=counting, "
                                      "M4=selectivity, M5=control, M8=transparency); mapped by CONTENT.",
                "compute": "cpu-only, $0, no GPU, no encoding, no LLM",
                "source_file_used": SRC_FILE_USED,
            },
            "M3_selectivity_artifact": M3,
            "M4_router_ci": M4,
            "M8_honest_counting": M8,
            "M5_us_consistency": M5,
            "M7_grouping_reframe": M7,
            "cross_checks": CROSS,
            "gaps": GAPS,
            "validation": {"all_cross_checks_pass": bool(all_pass), "n_cross_checks": len(CROSS),
                           "n_pass": n_pass, "n_gaps": len(GAPS)},
        },
        "metrics_agg": {k: num(v) for k, v in metrics_agg.items()},
        "datasets": datasets,
    }

    out_path = WS / "eval_out.json"
    out_path.write_text(json.dumps(out, indent=2))
    size = out_path.stat().st_size
    out["metadata"]["validation"]["output_bytes"] = size
    out["metadata"]["validation"]["under_100mb"] = size < 100 * 1024**2
    out_path.write_text(json.dumps(out, indent=2))

    del d2, d4
    gc.collect()

    logger.info(f"WROTE {out_path} ({size/1024:.1f} KB)")
    logger.info(f"CROSS-CHECKS: {n_pass}/{len(CROSS)} pass; all_pass={all_pass}; gaps={len(GAPS)}")
    logger.info(f"datasets: {[(d['dataset'], len(d['examples'])) for d in datasets]}")
    for c in CROSS:
        if not c["match"]:
            logger.warning(f"  HONEST MISMATCH {c['name']}: computed={c['computed']} "
                           f"expected={c['expected']} :: {c['note'][:160]}")


if __name__ == "__main__":
    main()
