#!/usr/bin/env python
"""Post-run self-check for the M6 router artifact (Step 6). Asserts the integrity + completeness
conditions from the plan. Usage: uv run self_check.py [method_out.json]"""
import sys, json

path = sys.argv[1] if len(sys.argv) > 1 else "method_out.json"
d = json.load(open(path))
m = d["metadata"]
ex = d["datasets"][0]["examples"]
scale = m.get("scale")
fail = []


def ck(cond, msg):
    print(("  OK  " if cond else " FAIL ") + msg)
    if not cond:
        fail.append(msg)


print(f"=== self-check {path} (scale={scale}, {len(ex)} concepts) ===")
roles = [e["metadata_role"] for e in ex]
n_deriv = sum(1 for r in roles if r == "derivation")
n_pro = sum(1 for r in roles if r == "prospective")
ck(scale == "full", f"scale == 'full' (got {scale})")
ck(len(ex) >= 26, f"len(examples) >= 26 (got {len(ex)})")
ck(n_deriv == 12, f"exactly 12 derivation concepts (got {n_deriv})")

# recommended = recall_hole_alone; recall-hole-alone bacc >= combined bacc on derivation
ck(m.get("recommended") == "recall_hole_alone" and m["router"]["recommended"] == "recall_hole_alone",
   f"router.recommended == 'recall_hole_alone' (got {m.get('recommended')})")
ssa = m["single_signal_ablations"]
ba_h = ssa["recall_hole_alone"]["balanced_acc"]
ba_comb = m["combined_rule"]["balanced_acc"]
ck(ba_h is not None and ba_comb is not None and ba_h >= ba_comb - 1e-9,
   f"recall-hole-alone bacc ({ba_h}) >= combined bacc ({ba_comb})")

# BOTH regimes present in PRIMARY prospective prediction
pro = [e for e in ex if e["metadata_role"] == "prospective"]
pro_inf = [e for e in pro if e["metadata_power_flag"] != "descriptive_only"]
pred_abs = [e for e in pro_inf if e["metadata_predicted_regime"] == "absorption"]
pred_cof = [e for e in pro_inf if e["metadata_predicted_regime"] == "co_firing"]
ck(len(pred_abs) >= 1, f">=1 prospective concept predicted 'absorption' (got {len(pred_abs)})")
ck(len(pred_cof) >= 1, f">=1 prospective concept predicted 'co_firing' (got {len(pred_cof)})")
new_spell = [e for e in pro if e["metadata_concept"].startswith("spelling_")]
ck(len(new_spell) >= 4, f">=4 NEW spelling prospective concepts built (got {len(new_spell)})")
n_spell_abs_truth = sum(1 for e in new_spell if e["metadata_ground_truth_regime"] == "absorption")
ck(n_spell_abs_truth >= 2, f">=2 new spelling letters land in absorption ground-truth (got {n_spell_abs_truth})")

# per-regime Wilson CIs populate
php = m["prospective_hitrate_primary"]
ck(php["absorption_predicted"]["n"] >= 1, "prospective_hitrate_primary.absorption_predicted non-empty")
ck(php["cofiring_predicted"]["n"] >= 1, "prospective_hitrate_primary.cofiring_predicted non-empty")
ck("wilson_ci" in php["absorption_predicted"], "absorption_predicted has a Wilson CI")
ck("wilson_ci" in php["cofiring_predicted"], "cofiring_predicted has a Wilson CI")

# new spelling letters are role==prospective and NOT in DERIVATION
ck(all(e["metadata_role"] == "prospective" for e in new_spell),
   "all new spelling concepts are role==prospective")
ck(all(e["metadata_concept"] not in m["derivation_concepts"] for e in new_spell),
   "no new spelling concept is in the derivation registry")

# two honest counterexamples present
cx = " ".join(m["counterexamples"])
ck("numeric" in cx and "taxonomic" in cx, "both honest counterexamples (numeric, taxonomic) emitted")

# ablation prediction fields present on every card
ck(all("metadata_predicted_regime_combined" in e and "metadata_predicted_regime_jaccard" in e for e in ex),
   "every card has combined + jaccard ablation predictions")
ck(all("metadata_hit_vs_a_combined" in e and "metadata_hit_vs_a_jaccard" in e for e in ex),
   "every card has combined + jaccard ablation hits")

# every prospective card is a predict-then-measure (predicted_regime set + is_prospective_hit set)
ck(all(e["metadata_predicted_regime"] in ("absorption", "co_firing") for e in pro),
   "every prospective card has a frozen-rule predicted_regime")

print("\n=== RESULT:", "ALL CHECKS PASSED" if not fail else f"{len(fail)} FAILURES", "===")
if fail:
    for f in fail:
        print("  FAIL:", f)
    sys.exit(1)
