#!/usr/bin/env python3
"""STEP 4-5 — Assemble the surface-pair SUPERSET (exp_sel_data_out schema) + null-size report.

ONE full_data_out.json with 7 dataset groups (5 first-letter + 2 toxicity), surface rows ONLY
(the frozen iter-1 content/classification rows stay canonical at their iter-1 paths). iter-1
originals are byte-identical except for 4 additive uniformity keys:
  metadata_enlargement_batch in {iter1_original, iter2_new}
  metadata_independent_judge_model / _pass / _reason  (claude-haiku-4.5; null if not re-judged)

Verifies superset guarantee, re-runs the deterministic first-letter validator + the toxicity
double-gate over the whole assembled set, enforces no cross-fold leakage, and writes the
per-concept surface-response null-distribution sizes to data_summary.json.
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from loguru import logger

import cc

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")

WORK = Path(__file__).resolve().parent
INTER = WORK / "temp" / "intermediate"
FL_LETTERS = ["l", "o", "t", "i", "d"]

IND_KEYS = ("metadata_independent_judge_model", "metadata_independent_judge_pass",
            "metadata_independent_judge_reason")


def add_keys(row, batch, annot):
    row = dict(row)
    row["metadata_enlargement_batch"] = batch
    a = annot.get(row["metadata_pair_id"]) if annot else None
    row["metadata_independent_judge_model"] = a["model"] if a else None
    row["metadata_independent_judge_pass"] = a["pass"] if a else None
    row["metadata_independent_judge_reason"] = a["reason"] if a else None
    return row


def tox_new_row(rid, rec, claude_annot):
    origin = rec["origin"]
    floats = rec["floats"]
    if floats is not None:
        floats = {a: float(floats.get(a, 0.0)) for a in cc.FLOAT_AXES}
        sub_labels = {a: (1 if floats.get(a, 0.0) >= cc.PRIMARY_THRESHOLD else 0) for a in cc.SUB_ATTRS}
        thr = cc.PRIMARY_THRESHOLD
    else:
        floats = {a: None for a in cc.FLOAT_AXES}
        sub_labels = {a: None for a in cc.SUB_ATTRS}
        thr = None
    row = {
        "input": rec["text"], "output": "toxic",
        "metadata_id": rid, "metadata_fold": rec["fold"],
        "metadata_record_type": "surface_pair", "metadata_source": "generated_paraphrase",
        "metadata_origin_source": origin, "metadata_toxicity_label": 1,
        "metadata_text_on": None, "metadata_text_off": None,
        "metadata_text_paired": rec["text_paired"], "metadata_pair_id": rec["pair_id"],
        "metadata_source_sentence_id": rec["ssid"],
        "metadata_is_content_pair": False, "metadata_is_surface_pair": True,
        "metadata_subcontext_labels": sub_labels, "metadata_subcontext_floats": floats,
        "metadata_subcontext_threshold": thr, "metadata_judge_pass": True,
        "metadata_gen_model": rec["gen_model"], "metadata_surface_metrics": rec["surface_metrics"],
    }
    return add_keys(row, "iter2_new", claude_annot)


# --------------------------------------------------------------------------- FL validation
def fl_validate(rows):
    pid_rows = defaultdict(list)
    for r in rows:
        pid_rows[r["metadata_pair_id"]].append(r)
    violations = 0
    for pid, rs in pid_rows.items():
        letter = rs[0]["metadata_letter"].lower()
        a = next((x for x in rs if x["metadata_role"] == "var_a"), None)
        b = next((x for x in rs if x["metadata_role"] == "var_b"), None)

        def span_ok(r):
            s, e = r["metadata_word_char_span"]
            return r["input"][s:e] == r["metadata_target_word"]
        ok = (len(rs) == 2 and a and b
              and a["metadata_first_letter"] == letter and b["metadata_first_letter"] == letter
              and a["metadata_target_word"].lower() != b["metadata_target_word"].lower()
              and span_ok(a) and span_ok(b))
        if not ok:
            violations += 1
    return violations


def main():
    rj = json.loads((INTER / "rejudge_out.json").read_text())
    fl_claude = rj["first_letter"]["claude_annot"]
    fl_deep = rj["first_letter"]["deepseek_annot"]
    tox_claude = rj["toxicity"]["claude_annot"]
    tox_gemini = rj["toxicity"]["gemini_annot"]

    # ===================== FIRST-LETTER =====================
    fl_orig = json.loads((INTER / "fl_originals.json").read_text())["surface_rows"]
    fl_new = json.loads((INTER / "fl_new_surface.json").read_text())["new_rows"]
    fl_groups = {lt: [] for lt in FL_LETTERS}
    for r in fl_orig:
        fl_groups[r["metadata_letter"].lower()].append(add_keys(r, "iter1_original", fl_claude))
    for r in fl_new:
        fl_groups[r["metadata_letter"].lower()].append(add_keys(r, "iter2_new", fl_claude))

    fl_all_rows = [r for g in fl_groups.values() for r in g]
    fl_viol = fl_validate(fl_all_rows)
    assert fl_viol == 0, f"FL structural violations={fl_viol}"
    # superset guarantee: every iter-1 FL surface pair_id present
    orig_fl_pids = {r["metadata_pair_id"] for r in fl_orig}
    asm_fl_pids = {r["metadata_pair_id"] for r in fl_all_rows}
    assert orig_fl_pids <= asm_fl_pids, "FL superset violated (missing original pair_id)"

    # ===================== TOXICITY =====================
    tox_orig = json.loads((INTER / "tox_originals.json").read_text())["surface_rows"]
    tox_acc = json.loads((INTER / "tox_new_surface.json").read_text())["accepted"]
    # dedupe new by pair_id; assign continuing metadata_id in sorted order
    seen_pid = {r["metadata_pair_id"] for r in tox_orig}
    uniq_new = {}
    for rec in tox_acc:
        if rec["pair_id"] in seen_pid or rec["pair_id"] in uniq_new:
            continue
        # verify gate bounds (authoritative)
        m = rec["surface_metrics"]
        assert m["jaccard"] < cc.JACCARD_MAX and m["char_change"] > cc.CHAR_CHANGE_MIN, \
            f"gate violation {rec['pair_id']}: {m}"
        uniq_new[rec["pair_id"]] = rec
    new_sorted = sorted(uniq_new.values(), key=lambda r: r["pair_id"])

    tox_groups = {"paradetox": [], "civil_comments": []}
    for r in tox_orig:
        tox_groups[r["metadata_origin_source"]].append(add_keys(r, "iter1_original", tox_claude))
    next_id = 546  # continue tox_sp counter past the 0..545 originals
    n_leak_drop = 0
    # leakage guard: build norm_key->fold over originals first
    nk_fold = defaultdict(set)
    for r in tox_orig:
        for t in (r["input"], r.get("metadata_text_paired")):
            if t:
                nk_fold[cc.norm_key(t)].add(r["metadata_fold"])
    for rec in new_sorted:
        ksrc, kpar = cc.norm_key(rec["text"]), cc.norm_key(rec["text_paired"])
        folds = nk_fold[ksrc] | nk_fold[kpar]
        if folds and rec["fold"] not in folds:
            n_leak_drop += 1
            continue
        rid = f"tox_sp_{next_id:06d}"; next_id += 1
        row = tox_new_row(rid, rec, tox_claude)
        tox_groups[rec["origin"]].append(row)
        nk_fold[ksrc].add(rec["fold"])
        nk_fold[kpar].add(rec["fold"])

    # final leakage assertion over ALL toxicity surface rows
    leaks = [k for k, v in nk_fold.items() if len(v) > 1]
    assert not leaks, f"{len(leaks)} toxicity surface texts span folds (leakage)"
    tox_all_rows = [r for g in tox_groups.values() for r in g]
    orig_tox_pids = {r["metadata_pair_id"] for r in tox_orig}
    asm_tox_pids = {r["metadata_pair_id"] for r in tox_all_rows}
    assert orig_tox_pids <= asm_tox_pids, "TOX superset violated"

    # ===================== NULL-SIZE REPORT =====================
    # first-letter: pairs = rows/2, per letter x carrier, orig vs new
    fl_report = {}
    fl_total_pairs = 0
    for lt in FL_LETTERS:
        rows = fl_groups[lt]
        by_pid = defaultdict(list)
        for r in rows:
            by_pid[r["metadata_pair_id"]].append(r)
        n_pairs = len(by_pid)
        fl_total_pairs += n_pairs
        carrier = Counter()
        batch = Counter()
        for pid, rs in by_pid.items():
            carrier[rs[0]["metadata_template_id"]] += 1
            batch[rs[0]["metadata_enlargement_batch"]] += 1
        fl_report[lt.upper()] = {"total_pairs": n_pairs, "rows": len(rows),
                                 "by_carrier_pairs": dict(carrier),
                                 "orig_pairs": batch.get("iter1_original", 0),
                                 "new_pairs": batch.get("iter2_new", 0)}

    # toxicity: 1 row per pair, per origin, per sub-attribute, orig vs new
    tox_report = {}
    tox_total = 0
    sub_counts_total = {a: 0 for a in cc.SUB_ATTRS}
    for origin in ("paradetox", "civil_comments"):
        rows = tox_groups[origin]
        tox_total += len(rows)
        batch = Counter(r["metadata_enlargement_batch"] for r in rows)
        sub = {a: 0 for a in cc.SUB_ATTRS}
        for r in rows:
            lbls = r.get("metadata_subcontext_labels") or {}
            for a in cc.SUB_ATTRS:
                if lbls.get(a) == 1:
                    sub[a] += 1
                    sub_counts_total[a] += 1
        fold = Counter(r["metadata_fold"] for r in rows)
        tox_report[origin] = {"total_pairs": len(rows),
                              "orig_pairs": batch.get("iter1_original", 0),
                              "new_pairs": batch.get("iter2_new", 0),
                              "by_fold": dict(fold),
                              "by_sub_attribute_pairs": sub}

    # both-judges-pass high-confidence subset sizes (where a 2nd judge label exists)
    tox_both_pass = sum(1 for pid, g in tox_gemini.items()
                        if g and g.get("pass") and tox_claude.get(pid, {}).get("pass"))
    fl_both_pass = sum(1 for pid, d in fl_deep.items()
                       if d and d.get("pass") and fl_claude.get(pid, {}).get("pass"))

    gen_stats = json.loads((INTER / "tox_gen_stats.json").read_text())
    total_llm_cost = round(gen_stats["openrouter_cost_usd"] + rj["rejudge_cost_usd"], 4)

    summary = {
        "title": "Enlarged & Independently Re-Judged Surface-Invariance Pair Sets (First-Letter + Toxicity)",
        "purpose": "Drop-in SUPERSET of the two iter-1 surface-flip pair sets for the Step-5 admission "
                   "AND-gate's shuffled-surface null. Surface rows ONLY; the frozen iter-1 "
                   "content_flip/content_pair/classification/corpus rows remain canonical at their iter-1 paths.",
        "merge_contract": {
            "first_letter": "merge by metadata_pair_id + metadata_role in {var_a,var_b}; "
                            "iter-1 content_flip/corpus rows live at iter_1/gen_art/gen_art_dataset_1/full_data_out.json",
            "toxicity": "one row per surface pair (input=source toxic, metadata_text_paired=toxic paraphrase); "
                        "iter-1 content_pair/classification rows live at iter_1/gen_art/gen_art_dataset_3/full_data_out.json",
        },
        "circularity_fixed": ("iter-1 generated AND judged the 546 toxicity surface pairs with the SAME model "
                              "(openai/gpt-4o-mini). Every NEW toxicity pair is judged by a DIFFERENT family "
                              "(anthropic/claude-haiku-4.5); a stratified sample of both concepts is re-judged "
                              "by a family different from BOTH the generator and the iter-1 judge."),
        "model_families": {
            "toxicity_generator": cc.GEN_MODEL,
            "toxicity_independent_judge_primary": cc.JUDGE_PRIMARY,
            "toxicity_second_family_judge": cc.JUDGE_SECOND_TOX,
            "first_letter_iter1_judge": "google/gemini-3.1-flash-lite",
            "first_letter_independent_judge_primary": cc.JUDGE_PRIMARY,
            "first_letter_second_family_judge": cc.JUDGE_SECOND_FL,
        },
        "gate_constants": {"jaccard_max": cc.JACCARD_MAX, "char_change_min": cc.CHAR_CHANGE_MIN,
                           "comparators": "token_jaccard < jaccard_max AND norm_edit_distance > char_change_min (strict)"},
        "first_letter_null_sizes": {
            "definition": "one surface-response per pair (r_ell pooled over both same-letter words in a fixed carrier)",
            "total_pairs": fl_total_pairs, "total_rows": len(fl_all_rows),
            "orig_pairs": 590, "new_pairs": fl_total_pairs - 590,
            "per_letter": fl_report,
            "deterministic_violations": fl_viol,
            "carriers": [c[0] for c in cc.SURFACE_CARRIERS],
        },
        "toxicity_null_sizes": {
            "definition": "one surface-response per pair (toxic source vs toxic paraphrase)",
            "total_pairs": tox_total, "orig_pairs": 546, "new_pairs": tox_total - 546,
            "per_origin": tox_report,
            "per_sub_attribute_total_pairs": sub_counts_total,
            "leakage_dropped_new": n_leak_drop,
        },
        "independent_rejudge": {
            "toxicity": {
                "originals_confirmation_rate": rj["toxicity"]["originals_confirmation_rate"],
                "originals_confirmed": rj["toxicity"]["originals_confirmed"],
                "n_originals_judged": rj["toxicity"]["n_originals_judged"],
                "cross_judge_claude_vs_gemini": rj["toxicity"]["cross_judge"],
                "both_judges_pass_in_sample": tox_both_pass,
            },
            "first_letter": {
                "claude_pass_rate": rj["first_letter"]["claude_pass_rate"],
                "claude_judge_false_negative_rate": rj["first_letter"]["claude_judge_false_negative_rate"],
                "cross_judge_claude_vs_deepseek": rj["first_letter"]["cross_judge"],
                "claude_vs_stored_gemini": rj["first_letter"]["claude_vs_stored_gemini"],
                "both_judges_pass_in_sample": fl_both_pass,
                "note": "deterministic structural check is AUTHORITATIVE; a claude/deepseek 'fail' on a "
                        "structurally-valid pair is a judge false-negative, NOT a drop.",
            },
        },
        "generation_stats": gen_stats,
        "rejudge_cost_usd": rj["rejudge_cost_usd"], "rejudge_calls": rj["rejudge_calls"],
        "total_openrouter_cost_usd": total_llm_cost,
        "iter1_provenance": {
            "first_letter": "iter_1/gen_art/gen_art_dataset_1 (gemini-3.1-flash-lite secondary judge; "
                            "unsloth/gemma-2-2b tokenizer vocab 256000; get_alpha_tokens slot-eligible single-token words)",
            "toxicity": "iter_1/gen_art/gen_art_dataset_3 (s-nlp/paradetox openrail++; google/civil_comments CC0; "
                        "gpt-4o-mini generate+judge)",
        },
    }

    # ===================== EMIT =====================
    datasets = []
    for lt in FL_LETTERS:
        datasets.append({"dataset": f"first_letter_spelling_{lt.upper()}", "examples": fl_groups[lt]})
    for origin in ("paradetox", "civil_comments"):
        datasets.append({"dataset": origin, "examples": tox_groups[origin]})

    out = {"metadata": summary, "datasets": datasets}
    (WORK / "full_data_out.json").write_text(json.dumps(out, ensure_ascii=False))
    (WORK / "data_summary.json").write_text(json.dumps(summary, indent=2))

    logger.info(f"FL: {fl_total_pairs} pairs ({len(fl_all_rows)} rows), 0 violations")
    logger.info(f"TOX: {tox_total} pairs (orig 546 + new {tox_total-546}); leak_drop={n_leak_drop}")
    logger.info(f"per-letter pairs: { {k: v['total_pairs'] for k, v in fl_report.items()} }")
    logger.info(f"per-origin pairs: { {k: v['total_pairs'] for k, v in tox_report.items()} }")
    logger.info(f"tox sub-attr pairs: {sub_counts_total}")
    logger.info(f"tox confirmation={rj['toxicity']['originals_confirmation_rate']} "
                f"tox kappa={rj['toxicity']['cross_judge']['kappa']} "
                f"fl kappa={rj['first_letter']['cross_judge']['kappa']}")
    logger.info(f"TOTAL OpenRouter cost=${total_llm_cost}")
    print(f"ASSEMBLE_OK fl_pairs={fl_total_pairs} tox_pairs={tox_total} "
          f"groups={len(datasets)} cost=${total_llm_cost}")


if __name__ == "__main__":
    main()
