# Coverage-Quantified Label-Free SAE Feature-Absorption Screen + Shipped Tool

`demo/` — Self-contained demo (Colab-ready notebook or markdown). Run without setup.  
`src/` — Full source code, data, and outputs from the experiment execution.

**Type:** experiment  
**ID:** `art_NIxb2uUvT-ze`

## Layman Summary

A reusable tool that uses only a frozen sparse autoencoder and raw text to map which concepts a language model garbles into token-specific 'absorber' features, finding the problem rare and mostly limited to homographs.

## Full Summary

M3'''' executes a $0, label-free feature-absorption COVERAGE SCREEN over a frozen Gemma-Scope L12/width-16k JumpReLU SAE (gemma-2-2b) across 10 concept hierarchies (first-letter spelling; taxonomic country; 4 homograph-entity: city/month/given-name/brand; 4 safety-identity: nationality/religion/ethnicity/named-entity) and ships it as a reusable practitioner tool (screen.py + README.md). Each candidate token is assigned predict_absorption in {ABSORPTION_STRUCTURED, CO_FIRING, NO_HOLE, DESCRIPTIVE_ONLY} from a purely model-internal firing signature: parent recall-hole>0.5, firing-disjoint absorber (Jaccard<0.1), absorber precision>=0.7, hole-coverage gain>=0.05 with a bootstrap CI excluding 0, plus n_eligible>=150 for the STRICT (inferential) gate. NO diagnostic probe / Chanin diagnostic / sub-context labels are used to FLAG; the form-free decoder-projection oracle (absorption_fraction, Chanin App. A.13) is independent corroboration only.

RESULT (overall_verdict=COVERAGE_QUANTIFIED, $0): 336 candidates screened, 110 eligible. Pooled STRICT coverage = 6/110 = 5.5% (Wilson [0.025,0.114]); pooled RELAXED = 31/336 = 9.2% (Wilson [0.066,0.128]). Absorption is homograph- and NAMED-ENTITY-confined: STRICT-structured = Georgia (taxonomic, absorber latent 16009 reproduced; data-derived 4697), Amazon/Bush/Cook (safety named-entity, absorbers 6846/9751/15631 matching prior runs), and borderline British/Greek (nationality, recall_hole~0.52, competing senses). Demographic religion 0/10 and ethnicity 0/10 are NOT structured (White/Black/Muslim all NO_HOLE); calendar months 0/12 are NO_HOLE (the cross-run 'months-only' claim does NOT reproduce here — the is-a-month parent fires reliably even on May/March, matching this run's iter-8); cities, given-names, and most brands 0; professions 0/28 (carried). First-letter spelling absorption reproduces broadly: 20/154 RELAXED-structured (own/that/light/long/only...; the 'starts-with-L' anchor 205 fires on 35.7% of L-words, so the holes are genuine), although the canonical 'large' has a strong recall-hole but a DISTRIBUTED (precision 0.57) re-encoding in this corpus and so is honestly not a clean single-absorber case. The form-free oracle corroborates 27/31 structured candidates (lexical 26/29 = 90%); Georgia is the documented exception (decoder cos 0.012, near-orthogonal to the generic 'country' direction), so oracle agreement is reported separately for lexical (high) vs taxonomic (low, with caveat).

DELIVERABLES: method.py (driver — builds all 10 hierarchies incl. new build_safety, runs the screen, coverage aggregation with Wilson+bootstrap CIs, positive/negative control reproduction, Georgia self-check). screen.py (the SHIPPED label-free screen — compute_signature + absorption_fraction_oracle + classify enum + Wilson/bootstrap-CI helpers + a CLI with optional --parent_latent; the CLI on Georgia with parent 3792 reproduces absorber 16009 -> ABSORPTION_STRUCTURED). README.md documents the label-free guarantee, enum semantics, the >=150 threshold, the decoder-oracle caveat, and worked examples. core.py / method_lib.py are the reused frozen-SAE engine. method_out.json (exp_gen_sol_out; validates; full/mini/preview all <100MB) carries metadata.coverage_table (per-hierarchy + POOLED, strict & relaxed, with Wilson + bootstrap CIs), coverage_headline, screen_vs_oracle_agreement (incl. structured_corroboration 27/31), control_reproduction (positive_controls, homograph_informational, spelling_absorption, negative_summary, professions), shipped_screen_spec, gating_check (cosine 0.9189, layer_idx 13 by min-FVU), screen_thresholds, n_candidates_screened/n_eligible, and 10 honest_negatives. datasets: absorption_coverage_screen (336 one-row-per-candidate, predict_absorption) + coverage_summary (22 (hierarchy,gate) rows, predict_coverage). Model google/gemma-2-2b (gated); SAE google/gemma-scope-2b-pt-res sae_id layer_12/width_16k/average_l0_82.

SO-WHAT (for the paper, answering reviewer R3 'why build on it'): practitioners can verify WHERE feature absorption can or cannot occur on ANY frozen SAE label-free; safety/demographic attributes are predominantly CO_FIRING/NO_HOLE, so absorption need not be feared there. The contribution is a quantified, CI-bounded coverage map of an SAE-reliability failure mode plus a reusable screening tool, with homograph/named-entity confinement (and the demographic null) as the honest headline. NOTE on infra: ran on a local RTX 5090 (Blackwell sm_120) with torch 2.11.0+cu128; the prior attempt's crash was an external RunPod pod-stock failure, not a code error.

## Dependencies

- `art_2xQn686KUmV5` — homograph-data
- `art_KNPsfjByyxiS` — entity-data
- `art_dpYpjSn2Xvg3` — spelling-data
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
