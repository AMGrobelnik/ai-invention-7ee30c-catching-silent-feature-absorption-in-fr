# Averted-Cost Auditing of SAE Feature Absorption in Compact Classifiers and Steerers

`demo/` — Self-contained demo (Colab-ready notebook or markdown). Run without setup.  
`src/` — Full source code, data, and outputs from the experiment execution.

**Type:** experiment  
**ID:** `art_DBUOXsYIIirp`

## Layman Summary

Shows that bundling SAE features into a small auditable unit can silently miss a concept (e.g. Georgia as a country); a cheap label-free screen catches the gap and naming the one missing feature fixes it.

## Full Summary

M1''''' Averted-Cost Auditing Scenario — EXECUTED on a single L4 GPU, $0 model-internal core + $0.0104 optional LLM judge. Overall verdict: AVERTED_COST_DEMONSTRATED (3/4 arms). This artifact converts the iter-9 label-free absorption screen (screen.py) from a reassurance instrument into an actionable reliability tool with a MEASURED averted cost, directly answering the reviewer's demand that cluster/group-level SAE units beat raw latents on concrete downstream tasks.

SETUP: a practitioner ships two downstream artifacts built on frozen Gemma-Scope L12/16k JumpReLU SAE latents over gemma-2-2b — a parent-concept CLASSIFIER (logistic head on the pooled top-N latents) and a parent-concept STEERING handle — both selected by SAEBench SCR/TPP marginal-attribution (|probe weight| x mean positive activation; the standard raw-latent practice). Four arms: georgia_classifier (primary, taxonomic), amazon_classifier (named-entity), amazon_steer (primary steer), large_steer (secondary). Each arm runs the end-to-end averted-cost chain with paired/two-sample bootstrap CIs (B=10,000).

HEADLINE RESULTS (per averted_cost_table; headline compact unit N=5, full N-curve {1,2,5,10,20} reported): (a) SILENT FAILURE — at compact, human-auditable sizes the absorbed slice is silently missed: Georgia country-recall 0.107 vs sibling 0.969 (gap +0.86 CI excl 0); Amazon org-recall 0.087 vs 0.760 (gap +0.67); Amazon steer on-target margin-drop 1.09 vs sibling 2.96 (gap +1.87). (b) STANDARD PRACTICE MISSES IT — the absorber is buried deep in the SCR/TPP attribution ranking (Georgia 16009 rank 42, Amazon 6846 rank 14) AND the form-free decoder-projection oracle scores Georgia clean (decoder-cos -0.024, |.|<0.025, corroborates=False) while it DOES corroborate Amazon (cos 0.116) — the predicted contrast that the screen is robust exactly where the concept-tuned oracle is blind. (c) SCREEN CATCHES IT — screen.py flags ABSORPTION_STRUCTURED (recall_hole 0.73/0.62, firing-disjoint absorber) and NAMES the latent with zero sub-context labels. (d) NAMED-ABSORBER REPAIR — adding the screen-named absorber lifts the compact classifier to ~1.0 (KG-minus-baseline +0.89/+0.91 CI excl 0) and the steer on-target to 6.83 (+5.74), with negligible sibling collateral. KEY HONEST FINDING: the hole closes by N>=10 (hole_closes_at_N=10), so the averted cost is the LOST AUDITABILITY (you need a larger, less-interpretable raw-latent ensemble) or the SHIPPED HOLE, not a permanent information loss.

BASELINES (reviewer-required): (i) raw SAE latents = the SCR/TPP top-N classifier AND the single parent latent (both carry the hole; Georgia single-latent recall 0.27); (ii) non-SAE = a dense diff-of-means parent probe on the residual (core.ParentProbe) which has NO slice hole (Georgia 0.99/1.0) — proving the hole is an SAE-selection artifact and the named-absorber repair recovers the compact, auditable SAE unit to match the dense baseline while staying sparse. STEER SIDE-EFFECTS: on unrelated text the repaired handle's KL/PPL/token-footprint are identical to the baseline handle (0.0108, within a firing-rate-matched shuffle null) — the repair is free off-target; a behavioral next-token KL (0.04->0.24, CI excl 0) and an optional anthropic/claude-haiku-4.5 judge (harmonic-mean 0.733->0.783) confirm it. HONEST NULL: large_steer = HN_SCREEN_DESCRIPTIVE_ONLY — the hole+repair mechanism is present (gap +0.96, repair +0.57, both CI excl 0) but only ~12 eval windows exist, so the screen correctly DECLINES to strict-certify (predict=DESCRIPTIVE_ONLY); it abstains, it does not miss.

FILES: method.py (new driver: scr_tpp_select + classifier_arm + steer_arm + classify_arm FORK + averted_cost_table); core.py/screen.py/m9.py reused verbatim from iter-4..9 (SAE engine + edit operators; shipped screen; family builders + screen_candidate); make_variants.py; README.md; pyproject.toml (65 pinned deps, cu124). Output method_out.json (exp_gen_sol_out) with datasets averted_cost_per_slice (30 examples: absorbed + sibling slices, gold RECALL_HOLE/STEER_HOLE/NO_HOLE, predict_marginal_attr/predict_repaired/predict_dense_probe) and averted_cost_per_case (4 examples, one per arm, predict_verdict = arm FORK); full/mini/preview all validate, all <=53KB. metadata carries the full averted_cost_table, per_arm_fork, n-curves, steer side-effects, judge, anchors, and honest_negatives (oracle concept-tuned/blind to Georgia; firing-signature != edit-handle; dense probe matches/beats raw latents; absorption homograph/named-entity-confined; the multi-member clustering hypothesis did not pay off — the shipped value is the label-free WHERE-screen + the named-absorber 2-member repair unit). GOTCHAS for downstream reuse: absorber pinned to the canonical KG id (the label-free re-derivation prefers a weaker split sibling, e.g. Georgia 4697 vs 16009, reported as discovered_label_free); in_topN computed before excluding the absorber; collateral magnitude tolerance avoids large-n CI hypersensitivity.

## Dependencies

- `art_t2uUbjSwpd3t` — taxonomic-data
- `art_KNPsfjByyxiS` — entity-data
- `art_dpYpjSn2Xvg3` — spelling-data
- `art_2xQn686KUmV5` — homograph-data
- `art_RidEJtBC7gPT` — method-dossier
- `art_I2MrezW41iQo` — diagnostic

## Output Files

- `method.py`
- `full_method_out.json`
- `mini_method_out.json`
- `preview_method_out.json`

## Demo Files

- **method.py** — Research methodology implementation

---
*Generated by AI Inventor Pipeline*
