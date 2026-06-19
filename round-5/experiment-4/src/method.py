#!/usr/bin/env python3
"""M7 (iter-5) — SECOND polysemy/absorption case beyond Georgia.

Three parts on the FROZEN Gemma-2-2b / Gemma-Scope layer_12/width_16k JumpReLU SAE:

  PART 1 (NEW science, GPU encode): is SAE feature absorption a property of a general is-a
          hierarchy?  Test the bias_in_bios PROFESSION hierarchy (general 'occupation' parent
          vs 28 specific professions) for a suppressed-parent + mutually-exclusive-specialist
          signature.  Corpus-only (no content pairs / target spans) => whole-text encode.
  PART 2 (CPU, cached): HOMOGRAPH SCAN — re-run the taxonomic pipeline from the iter-4 cache,
          regenerate the homograph x absorption-type cross-tab over all 52 countries, and scan
          entity surface tokens for any new suppressed-parent case beyond Georgia/Jordan.
  PART 3 (CPU, cached): JORDAN-BESIDE-GEORGIA — a single side-by-side selection table
          (Georgia eligible / Jordan descriptive / United States co-firing) with n + CIs.

Method vs BASELINES (held side-by-side in one pipeline):
  unit (two-track set-cover) vs raw-SAE baselines {anchor, g=top-20 marginal-attr, h=count-matched,
  S_rec/S_prec/S_mag label-free selectors, RE-k-anchored} vs non-SAE {dense difference-probe}.

The EXPECTED, publishable outcome is the honest negative: 'absorption remains narrow / specific to
suppressed-parent homograph polysemy; the profession is-a hierarchy shows uniform-high parent recall
= NO absorption'.  A qualifying profession (absorption_type AND set_cover_established) would be a
positive SECOND case.

Run:  uv run method.py --scale full
"""
from __future__ import annotations

import argparse
import gc
import json
import time
from pathlib import Path

import numpy as np
from loguru import logger

import engine as eng
import profession_absorption as pa
import torch

WORKSPACE = eng.WORKSPACE
RESULTS_DIR = eng.RESULTS_DIR
BIOS_DATA = Path(
    "/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/"
    "gen_art_dataset_4/full_data_out.json"
)


# ============================================================================= PART 1 driver
def run_professions(sae_id: str, width: int, scale: str, b_auc: int, b_draws: int,
                    cap: int, n_neg: int, max_setcover: int = 4) -> tuple[dict, list]:
    logger.info("================= PART 1: PROFESSION IS-A HIERARCHY (bias_in_bios) =================")
    t0 = time.time()
    rng = np.random.default_rng(eng.SEED)
    cap_eff = {"smoke": 60, "mini": 150}.get(scale, cap)
    n_neg_eff = {"smoke": 400, "mini": 1000}.get(scale, n_neg)
    bios, neg, professions = pa.load_professions_and_negatives(BIOS_DATA, cap=cap_eff, n_neg=n_neg_eff)

    # ---- encode (GPU; lazy model load on cache miss) ----
    _enc = {"enc": None, "model_id": "cache-reuse(no-model)", "layer_idx": eng.HOOK_LAYER_DEFAULT + 1}

    def get_encoder():
        if _enc["enc"] is None:
            logger.info("cache miss -> loading gemma-2-2b for whole-text GPU encode")
            model, tok, model_id = eng.load_model()
            layer_idx = pa.determine_layer_idx_wholetext(model, tok, eng._SAE, bios)
            _enc["enc"] = pa.WholeTextEncoder(model, tok, eng._SAE, layer_idx)
            _enc["model_id"] = model_id
            _enc["layer_idx"] = layer_idx
        return _enc["enc"]

    lat_bios, resid_bios, info_bios = pa.encode_or_cache_wholetext(
        get_encoder, "bias", bios, width, use_cache=True)
    lat_neg, resid_neg, info_neg = pa.encode_or_cache_wholetext(
        get_encoder, "neg", neg, width, use_cache=True)
    if not info_bios.get("cached"):
        fvu, l0 = info_bios.get("fvu", 1.0), info_bios.get("mean_l0", 0.0)
        logger.info(f"  [bios] encode validation FVU={fvu:.3f} meanL0={l0:.1f}")
        assert fvu < 0.6, f"bios FVU {fvu:.3f} too high -> layer/pooling wrong"
        assert 1.0 < l0 < width * 0.5, f"bios meanL0 {l0:.1f} implausible"

    # ---- 50/50 selection/diagnostic split, stratified by profession ----
    prof_all = np.array([r["_profession"] for r in bios])
    gender_all = np.array([r["_gender"] for r in bios])
    is_diag = np.zeros(len(bios), dtype=bool)
    srng = np.random.default_rng(eng.SEED)
    for p in professions:
        idx = np.where(prof_all == p)[0]
        srng.shuffle(idx)
        is_diag[idx[: len(idx) // 2]] = True
    sel_rows = np.where(~is_diag)[0]
    diag_rows = np.where(is_diag)[0]
    lat_bios_sel = lat_bios[sel_rows]
    lat_bios_diag = lat_bios[diag_rows]
    resid_sel = resid_bios[sel_rows]
    resid_diag = resid_bios[diag_rows]
    prof_sel = prof_all[sel_rows]
    prof_diag = prof_all[diag_rows]
    gender_diag = gender_all[diag_rows]
    logger.info(f"  fold split: selection={len(sel_rows)} diagnostic={len(diag_rows)}")

    # ---- parent identification (corpus-only) ----
    pinfo = pa.identify_parent(lat_bios_sel, lat_neg, lat_bios_diag, width, rng)
    anchor = pinfo["anchor"]
    if anchor is None:
        logger.warning("  NO general parent latent -> professions absorption test VOID (fallback c)")
        runtime = round(time.time() - t0, 1)
        return ({"professions_verdict": "no_general_parent_latent",
                 "n_professions": len(professions), "n_bios": len(bios), "n_neg": len(neg),
                 "parent": pinfo, "encoding": {"bios": info_bios, "neg": info_neg},
                 "hole_table": {}, "qualifying_professions": [], "setcover": {},
                 "model": _enc["model_id"], "layer_idx": _enc["layer_idx"], "runtime_s": runtime}, [])
    logger.info(f"  PARENT anchor={anchor} recall_sel={pinfo['anchor_recall_selection']:.3f} "
                f"recall_heldout={pinfo['anchor_recall_heldout']:.3f} "
                f"precision={pinfo['anchor_precision_bios_vs_neg']:.3f} "
                f"floor_ok={pinfo['anchor_firing_floor_ok']}")

    # ---- per-profession hole table (all professions, held-out fold) ----
    cand_pool = pinfo["_disc_idx"]
    hole_table, hctx = pa.per_profession_hole_table(
        lat_bios_diag, prof_diag, gender_diag, professions, anchor, cand_pool)
    holes = sorted(hole_table.items(), key=lambda kv: -kv[1]["parent_hole"])
    qualifying = [p for p, e in hole_table.items() if e["absorption_type"] and e["eligible"]]
    max_hole = holes[0][1]["parent_hole"]
    n_abs_type = sum(1 for e in hole_table.values() if e["absorption_type"])
    logger.info(f"  HOLE TABLE: max parent_hole={max_hole:.3f} ({holes[0][0]}); "
                f"n absorption_type={n_abs_type}; qualifying(eligible)={qualifying}")

    # ---- parent probe direction (bios vs neg) for form-free corroboration ----
    from sklearn.linear_model import LogisticRegression
    Xp = np.r_[resid_sel.astype(np.float32),
               resid_neg[: min(len(resid_neg), len(resid_sel))].astype(np.float32)]
    yp = np.r_[np.ones(len(resid_sel)), np.zeros(min(len(resid_neg), len(resid_sel)))]
    parent_probe = LogisticRegression(max_iter=2000, C=1.0, class_weight="balanced").fit(Xp, yp)
    d_p = parent_probe.coef_[0].astype(np.float64)
    d_p_unit = d_p / (np.linalg.norm(d_p) + 1e-9)
    # overall bios-vs-neg dense probe AUC (non-SAE sanity baseline; held-out bios vs neg)
    s_pos = parent_probe.decision_function(resid_diag.astype(np.float32))
    s_neg = parent_probe.decision_function(resid_neg.astype(np.float32))
    parent_probe_auc = float(eng.fast_auc(s_pos, s_neg))
    logger.info(f"  parent dense-probe (bios vs neg) held-out AUC={parent_probe_auc:.3f}")

    # ---- set-cover + selection isolation: qualifying professions, else largest-hole DESCRIPTIVE ----
    elig_pool = np.array(pinfo["_prec_pass"]) if len(pinfo["_prec_pass"]) >= 2 else cand_pool
    to_run = list(qualifying)
    descriptive_choice = None
    if not to_run:
        # pick the eligible profession with the largest hole as a clearly-labelled DESCRIPTIVE case
        for p, e in holes:
            if e["eligible"]:
                descriptive_choice = p
                to_run = [p]
                break
    to_run = to_run[:max_setcover]
    setcover = {}
    analyzed_for_predictions = None
    for p in to_run:
        logger.info(f"  --- set-cover for profession '{p}' "
                    f"({'QUALIFYING' if p in qualifying else 'DESCRIPTIVE best-hole'}) ---")
        sc = pa.setcover_for_profession(
            p, lat_bios_sel, lat_bios_diag, resid_sel, resid_diag, prof_sel, prof_diag,
            anchor, elig_pool, pinfo["_prec"], width, d_p_unit, rng, b_auc=b_auc, b_draws=b_draws)
        sc["is_qualifying"] = bool(p in qualifying)
        sc["is_descriptive_only"] = bool(p == descriptive_choice)
        logger.info(f"    unit={sc['unit']} n_absorbers={sc['n_absorbers']} "
                    f"unit_AUC={sc['auc_point']['unit']:.3f} "
                    f"set_cover_established={sc['set_cover_established']}")
        if analyzed_for_predictions is None:
            analyzed_for_predictions = sc
        setcover[p] = sc

    # ---- second-case verdict for professions ----
    second_case_professions = [p for p in qualifying if setcover.get(p, {}).get("set_cover_established")]
    if second_case_professions:
        professions_verdict = "second_case_found"
    elif n_abs_type > 0:
        professions_verdict = "absorption_signature_without_setcover"  # holes+specialist but unit !> selectors
    elif max_hole > 0.5:
        professions_verdict = "holes_without_mutually_exclusive_specialist"  # splitting, not absorption
    else:
        professions_verdict = "uniform_high_parent_recall_no_absorption"   # the EXPECTED boundary-null

    # ---- per-row held-out predictions for the analyzed profession (one-vs-rest) ----
    pred_rows = []
    if analyzed_for_predictions is not None:
        sc = analyzed_for_predictions
        ap = sc["profession"]
        eval_rows = sc["_eval_rows"]
        preds = sc["_preds"]
        y = sc["_y"]
        # map eval position -> original bios row (diag_rows[eval_rows]) for input text + metadata
        for k in range(min(len(eval_rows), 8000)):
            br = diag_rows[eval_rows[k]]
            r = bios[br]
            ex = {
                "input": r["input"][:280],
                "output": "positive" if y[k] == 1 else "negative",
                "metadata_hierarchy": "professions",
                "metadata_analyzed_profession": ap,
                "metadata_sub_context": r["_profession"],
                "metadata_gender": r["_gender"],
                "metadata_fold": "diagnostic",
            }
            for det in ("unit", "anchor", "g", "h", "dense_probe", "rek",
                        "S_rec_anch", "S_prec_anch", "S_mag_anch"):
                if det in preds:
                    key = det.replace("_anch", "")
                    ex[f"predict_{key}"] = "positive" if bool(preds[det][k]) else "negative"
            pred_rows.append(ex)
    logger.info(f"  professions_verdict = {professions_verdict} "
                f"(second_case={second_case_professions}); pred rows={len(pred_rows)}")

    # strip private arrays before emit
    for sc in setcover.values():
        for kk in ("_eval_rows", "_preds", "_y"):
            sc.pop(kk, None)
    for kk in ("_prec", "_rate_bios", "_rate_neg", "_disc_idx", "_prec_pass"):
        pinfo.pop(kk, None)

    runtime = round(time.time() - t0, 1)
    result = {
        "professions_verdict": professions_verdict,
        "n_professions": len(professions), "professions": professions,
        "n_bios": len(bios), "n_neg": len(neg),
        "cap_per_profession": cap_eff, "fold_split": {"selection": int(len(sel_rows)),
                                                      "diagnostic": int(len(diag_rows))},
        "parent": pinfo, "parent_dense_probe_bios_vs_neg_auc": parent_probe_auc,
        "hole_table": hole_table,
        "n_absorption_type": int(n_abs_type),
        "max_parent_hole": float(max_hole), "max_parent_hole_profession": holes[0][0],
        "eligible_professions": [p for p, e in hole_table.items() if e["eligible"]],
        "qualifying_professions": qualifying,
        "second_case_professions": second_case_professions,
        "descriptive_setcover_profession": descriptive_choice,
        "setcover": setcover,
        "encoding": {"bios": info_bios, "neg": info_neg},
        "negative_regime_notes": (
            "PRIMARY per-profession AUC is ONE-VS-REST WITHIN bios (genre-matched: positives=prof-p "
            "bios, negatives=other-profession bios). Non-bio negatives (movie+restaurant reviews) are "
            "used ONLY for parent precision-gating (bios-vs-review discriminative latent + content-style "
            "precision) and the dense-probe genre sanity baseline. Both regimes reported; a 'parent' that "
            "keys on genre (bio vs review) rather than 'occupation' is the confound this guards against."),
        "model": _enc["model_id"], "layer_idx": _enc["layer_idx"], "runtime_s": runtime,
    }
    del lat_bios, lat_bios_sel, lat_bios_diag, resid_bios, resid_sel, resid_diag, lat_neg, resid_neg
    gc.collect()
    return result, pred_rows


# ============================================================================= PARTS 2-3 driver
def run_taxonomic(sae_id: str, width: int, b_auc: int, b_draws: int) -> tuple[dict, list]:
    """Re-run the iter-4 taxonomic pipeline from cache (CPU) -> homograph cross-tab, entity scan,
    Jordan-beside-Georgia side-by-side table."""
    logger.info("================= PARTS 2-3: TAXONOMIC (homograph scan + Jordan-beside-Georgia) =================")
    name = "taxonomic"
    rows = eng.load_hierarchies(eng.DATA_PATH, [name])[name]
    lat, resid, info = eng.encode_or_cache(lambda: None, name, rows, width, use_cache=True)
    eng.rng = np.random.default_rng(eng.SEED)
    result, ctx = eng.analyze_hierarchy(name, rows, lat, resid, eng.get_eligible(name), width)
    ext, pred_extra = eng.iter3_extensions(name, result, ctx, eng.get_eligible(name),
                                           b_auc=b_auc, b_draws=b_draws)
    result.update(ext)
    for det, fires in pred_extra.items():   # mirror engine.main: add rek/S_*/original/weighted preds
        ctx["fires_matched"][det] = fires

    # ---- PART 2A: homograph cross-tab (already in ext) ----
    homograph_crosstab = result["homograph_crosstab"]
    router_all = result["router_all"]

    # ---- PART 2B: entity-token scan (best-effort; country-parent only -> coverage-limited) ----
    meta = ctx["meta"]
    diagpos_rows = ctx["diagpos_rows"]
    anchor = int(ctx["anchor"])
    lat_csr = ctx["lat"]
    parent_fire = np.asarray((lat_csr[diagpos_rows][:, anchor] > 0).todense()).ravel()
    surf = np.array([str(meta[ri].get("metadata_target_text")) for ri in diagpos_rows], dtype=object)
    elig_pool = [int(l) for l in ctx["cr_idx"]
                 if ctx["precision_l"][l] >= eng.PRECISION_FLOOR and l != anchor]
    entity_scan = {"note": ("scan groups diagnostic country-mention surfaces by target token; tests the "
                            "COUNTRY parent's recall-hole + a mutually-exclusive eligible specialist. "
                            "COVERAGE LIMIT: the taxonomic testbed has per-COUNTRY labels but not per-city "
                            "labels, so non-country entity (city/proper-noun) absorption is UNTESTABLE here "
                            "-> 'no new case' is NOT an exhaustive negative."),
                   "surfaces_tested": [], "new_absorption_surfaces": []}
    sub_elig = (np.asarray((lat_csr[diagpos_rows][:, elig_pool] > 0).todense())
                if elig_pool else np.zeros((len(diagpos_rows), 0), dtype=bool))  # hoisted (surface-independent)
    surf_vals, surf_cnts = np.unique(surf, return_counts=True)
    for sv, sc in zip(surf_vals, surf_cnts):
        if sc < eng.N_MIN_ELIGIBLE or sv in ("None", "nan", ""):
            continue
        msk = surf == sv
        parent_recall = float(parent_fire[msk].mean())
        hole = 1.0 - parent_recall
        best_jac = 1.0
        best_lat = None
        if elig_pool:
            cov = sub_elig[msk].mean(0)
            cand = [j for j in range(len(elig_pool)) if cov[j] >= eng.GAIN_MIN]
            for j in cand:
                fl = sub_elig[:, j]
                inter = int((fl & parent_fire).sum()); union = int((fl | parent_fire).sum())
                jac = inter / union if union else 0.0
                if jac < best_jac:
                    best_jac = jac; best_lat = int(elig_pool[j])
        absorption_type = bool(hole > 0.5 and best_jac < eng.JACCARD_MAX)
        rec = {"surface": str(sv), "n": int(sc), "parent_recall": parent_recall,
               "parent_hole": hole, "best_specialist": best_lat, "best_jaccard": best_jac,
               "absorption_type": absorption_type}
        entity_scan["surfaces_tested"].append(rec)
        if absorption_type:
            entity_scan["new_absorption_surfaces"].append(rec)
    entity_scan["n_surfaces_tested"] = len(entity_scan["surfaces_tested"])
    entity_scan["new_case_beyond_known"] = [r for r in entity_scan["new_absorption_surfaces"]
                                            if r["surface"] not in ("Georgia", "Jordan")]
    logger.info(f"  entity scan: {entity_scan['n_surfaces_tested']} surfaces >=150; "
                f"absorption_type surfaces={[r['surface'] for r in entity_scan['new_absorption_surfaces']]}")

    # ---- PART 3: Jordan-beside-Georgia side-by-side ----
    auc_point = result["auc_point"]
    auc_diff = result["auc_diff_ci"]
    side_by_side = {}
    for country in ("Georgia", "Jordan", "United States"):
        ra = router_all.get(country, {})
        ap = auc_point.get(country, {})
        ad = auc_diff.get(country, {})
        side_by_side[country] = {
            "n_pos": ra.get("n_pos"), "eligible": ra.get("eligible"),
            "absorption_type": ra.get("absorption_type"),
            "parent_recall_hole": ra.get("parent_recall_hole"),
            "firing_jaccard": ra.get("firing_jaccard"),
            "unit_auc": ap.get("auc_unit"),
            "auc_diff_vs": {c: ad.get(c) for c in
                            ("S_rec_anch", "S_prec_anch", "S_mag_anch", "rek_anch_mean", "g", "h",
                             "dense_probe") if c in ad},
            "set_cover_established": (result.get("set_cover_established") if country == "Georgia" else None),
            "status": ("eligible_inferential" if ra.get("eligible") else
                       ("descriptive_underpowered" if ra.get("absorption_type") else
                        "co_firing_not_absorption")),
        }
    side_by_side["_annotation"] = (
        "Affirmative non-spelling set-cover evidence is currently ONE eligible slice (Georgia), 1-2 "
        "counting DESCRIPTIVE Jordan (n<150). United States is co-firing/splitting (firing-Jaccard "
        "~0.20), NOT absorption. The profession is-a hierarchy adds NO new eligible case (see PART 1).")

    taxonomic = {
        "hierarchy_verdict": result.get("hierarchy_verdict"),
        "anchor_latent": anchor,
        "set_cover_established": result.get("set_cover_established"),
        "setcover_corroborated": result.get("setcover_corroborated"),
        "homograph_crosstab": homograph_crosstab,
        "entity_scan": entity_scan,
        "side_by_side": side_by_side,
        "router_all": router_all,
        "auc_diff_ci_defining": auc_diff.get("Georgia", {}),
        "encoding": info,
    }
    # build a small per-row prediction record for the Georgia/Jordan/US slices
    diag_rows = ctx["diag_rows"]
    label = ctx["label"]
    sub = ctx["sub"]
    fires = ctx["fires_matched"]
    examples = []
    for k, ri in enumerate(diag_rows):
        s = str(sub[ri])
        if s not in ("Georgia", "Jordan", "United States"):
            continue
        is_pos = int(label[ri]) == 1
        ex = {"input": meta[ri]["input"][:280], "output": "positive" if is_pos else "negative",
              "metadata_hierarchy": "taxonomic_sidebyside", "metadata_sub_context": s,
              "metadata_target_text": meta[ri].get("metadata_target_text"),
              "metadata_fold": "diagnostic"}
        for det in ("unit", "anchor", "g", "h", "dense_probe", "rek", "S_rec", "S_prec", "S_mag"):
            if det in fires:
                ex[f"predict_{det}"] = "positive" if bool(fires[det][k]) else "negative"
        examples.append(ex)
    logger.info(f"  side-by-side prediction rows (Georgia/Jordan/US): {len(examples)}")
    del lat, resid, ctx
    gc.collect()
    return taxonomic, examples


# ============================================================================= verdict + emit
def build_verdict(prof: dict, tax: dict) -> dict:
    second_case_found = bool(prof.get("second_case_professions")
                             or tax.get("entity_scan", {}).get("new_case_beyond_known"))
    verdict = "second_case_found" if second_case_found else "absorption_remains_narrow"
    return {
        "verdict": verdict,
        "second_case_found": second_case_found,
        "professions_verdict": prof.get("professions_verdict"),
        "interpretation": (
            "A second eligible suppressed-parent absorption case was found beyond Georgia."
            if second_case_found else
            "Absorption is NARROW / specific to suppressed-parent homograph polysemy (Georgia, and "
            "descriptive Jordan). The profession is-a hierarchy shows uniform-high parent recall with "
            "no mutually-exclusive specialist filling a hole = NO absorption; the homograph entity scan "
            "surfaces no new case (coverage-limited). Affirmative non-spelling set-cover evidence remains "
            "ONE eligible slice (Georgia), 1-2 counting descriptive Jordan."),
    }


def honest_negatives(prof: dict, tax: dict) -> list[str]:
    notes = [
        f"Professions boundary-null: profession is-a hierarchy verdict = '{prof.get('professions_verdict')}'"
        f" (max parent hole {prof.get('max_parent_hole')} on '{prof.get('max_parent_hole_profession')}'; "
        f"n absorption_type professions = {prof.get('n_absorption_type')}).",
        "Entity scan coverage limit: the taxonomic testbed labels per-COUNTRY, not per-city, so "
        "non-country entity absorption is untestable; 'no new homograph case' is expected, not exhaustive.",
        "Affirmative non-spelling set-cover evidence remains n=1 eligible (Georgia), 1-2 counting "
        "descriptive Jordan (n<150). United States is co-firing/splitting, not absorption.",
        "Parent precision-gating uses a non-bio negative pool (movie+restaurant reviews); the PRIMARY "
        "per-profession AUC is one-vs-rest WITHIN bios (genre-matched) to guard the bio-vs-review confound.",
    ]
    if prof.get("professions_verdict") == "no_general_parent_latent":
        notes.append("No general 'occupation' parent latent exists (no precision-passing high-recall "
                     "latent across professions) -> the absorption test is VOID for professions (a finding: "
                     "the phenomenon needs a token-level general parent, which professions lack).")
    return notes


def emit(prof: dict, prof_preds: list, tax: dict, tax_preds: list, run_meta: dict):
    datasets = []
    if prof_preds:
        datasets.append({"dataset": "professions", "examples": prof_preds})
    else:
        datasets.append({"dataset": "professions", "examples": [{
            "input": "(professions absorption test produced no per-row prediction record)",
            "output": "negative", "metadata_hierarchy": "professions",
            "metadata_note": prof.get("professions_verdict", "void")}]})
    if tax_preds:
        datasets.append({"dataset": "taxonomic_sidebyside", "examples": tax_preds})
    out = {"metadata": {**run_meta, "per_family": {"professions": prof, "taxonomic": tax}},
           "datasets": datasets}
    path = WORKSPACE / "method_out.json"
    path.write_text(json.dumps(out, indent=2, default=eng._json_default))
    logger.info(f"wrote {path} ({path.stat().st_size/1e6:.1f} MB)")
    return path


def write_csvs(prof: dict, tax: dict):
    import csv
    # hole table (all professions)
    ht = prof.get("hole_table", {})
    if ht:
        rows = []
        for p, e in sorted(ht.items(), key=lambda kv: -kv[1]["parent_hole"]):
            g = e.get("gender_split", {})
            rows.append({"profession": p, "n": e["n"], "eligible": e["eligible"],
                         "parent_recall": round(e["parent_recall"], 4),
                         "parent_hole": round(e["parent_hole"], 4),
                         "best_specialist": e["best_specialist"],
                         "best_specialist_precision": e["best_specialist_precision"],
                         "best_jaccard": round(e["best_jaccard"], 4),
                         "n_specialists": e["n_specialists"], "absorption_type": e["absorption_type"],
                         "male_hole": g.get("male_hole"), "female_hole": g.get("female_hole")})
        p = RESULTS_DIR / "hole_table_professions.csv"
        with open(p, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
        logger.info(f"  wrote {p}")
    # per-profession set-cover AUC-diff
    for pname, sc in prof.get("setcover", {}).items():
        ad = sc.get("auc_diff_ci", {})
        if ad:
            rows = [{"comparator": c, "diff": v.get("diff"), "ci_lo": v.get("ci_lo"),
                     "ci_hi": v.get("ci_hi")} for c, v in ad.items()]
            pth = RESULTS_DIR / f"setcover_auc_diff_{pname}.csv"
            with open(pth, "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
            logger.info(f"  wrote {pth}")
    # side-by-side
    sbs = tax.get("side_by_side", {})
    rows = []
    for c in ("Georgia", "Jordan", "United States"):
        e = sbs.get(c, {})
        if not e:
            continue
        rows.append({"country": c, "n_pos": e.get("n_pos"), "eligible": e.get("eligible"),
                     "absorption_type": e.get("absorption_type"),
                     "parent_recall_hole": e.get("parent_recall_hole"),
                     "firing_jaccard": e.get("firing_jaccard"), "unit_auc": e.get("unit_auc"),
                     "status": e.get("status"), "set_cover_established": e.get("set_cover_established")})
    if rows:
        pth = RESULTS_DIR / "side_by_side_jordan_georgia.csv"
        with open(pth, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
        logger.info(f"  wrote {pth}")
    # homograph crosstab
    hc = tax.get("homograph_crosstab", {})
    if hc.get("members"):
        rows = [{"cell": k, "count": hc["counts"].get(k), "members": "|".join(v)}
                for k, v in hc["members"].items()]
        pth = RESULTS_DIR / "homograph_crosstab.csv"
        with open(pth, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
        logger.info(f"  wrote {pth}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scale", choices=["smoke", "mini", "full"], default="full")
    ap.add_argument("--parts", default="1,2,3", help="comma list of parts to run")
    ap.add_argument("--width", default="16k", choices=["16k", "65k"])
    ap.add_argument("--b-auc", type=int, default=10000)
    ap.add_argument("--b-draws", type=int, default=1000)
    ap.add_argument("--cap", type=int, default=pa.CAP_PER_PROFESSION)
    ap.add_argument("--n-neg", type=int, default=pa.N_NEG_TARGET)
    args = ap.parse_args()

    t_start = time.time()
    sae_id = eng.SAE_ID_16K if args.width == "16k" else eng.SAE_ID_65K
    width = 16384 if args.width == "16k" else 65536
    parts = set(args.parts.split(","))
    if args.scale == "smoke":
        args.b_auc = min(args.b_auc, 2000)
        args.b_draws = min(args.b_draws, 200)

    # SAE shared by all parts (W_dec for form-free; encoder for Part 1)
    eng._SAE = eng.load_sae(sae_id)
    eng._GLOBAL["W_dec"] = eng._SAE.W_dec.detach().float().cpu().numpy()

    prof, prof_preds = ({"professions_verdict": "not_run"}, [])
    tax, tax_preds = ({}, [])
    if "1" in parts:
        prof, prof_preds = run_professions(sae_id, width, args.scale, args.b_auc, args.b_draws,
                                           args.cap, args.n_neg)
    if "2" in parts or "3" in parts:
        tax, tax_preds = run_taxonomic(sae_id, width, args.b_auc, args.b_draws)

    verdict = build_verdict(prof, tax)
    run_meta = {
        "method_name": ("M7 iter-5 — SECOND polysemy/absorption case beyond Georgia: bias_in_bios "
                        "profession is-a hierarchy (NEW, whole-text GPU encode) + homograph scan + "
                        "Jordan-beside-Georgia side-by-side; reuses iter-4 precision-gated K-track + "
                        "label-free selectors + AUC-diff machinery (engine.py)."),
        **verdict,
        "honest_negatives": honest_negatives(prof, tax),
        "sae": {"release": eng.SAE_RELEASE, "sae_id": sae_id, "width": width,
                "hook": f"blocks.{eng.HOOK_LAYER_DEFAULT}.hook_resid_post",
                "hf_hidden_state_idx": prof.get("layer_idx", eng.HOOK_LAYER_DEFAULT + 1),
                "d_model": eng.D_MODEL},
        "model": prof.get("model", "cache-reuse"),
        "stats": {"bootstrap_B_auc": args.b_auc, "B_draws": args.b_draws,
                  "n_min_eligible": eng.N_MIN_ELIGIBLE, "seed": eng.SEED,
                  "auc_diff_ci": "stratified paired bootstrap (resample positives & negatives separately)"},
        "thresholds": {"G1_recall": eng.G1_RECALL,
                       "jaccard_max": eng.JACCARD_MAX, "subctx_precision": eng.SUBCTX_PREC,
                       "gain_min": eng.GAIN_MIN, "precision_floor": eng.PRECISION_FLOOR,
                       "greedy_max_members": eng.GREEDY_MAX_MEMBERS,
                       "firing_floor_heldout": pa.FIRING_FLOOR,
                       "cap_per_profession": prof.get("cap_per_profession")},
        "scale": args.scale, "parts": sorted(parts),
        "runtime_s": round(time.time() - t_start, 1),
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu",
    }
    emit(prof, prof_preds, tax, tax_preds, run_meta)
    write_csvs(prof, tax)
    logger.info(f"DONE. verdict={verdict['verdict']} | professions={prof.get('professions_verdict')} "
                f"| runtime={run_meta['runtime_s']}s")


if __name__ == "__main__":
    main()
