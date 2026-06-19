# Iter-10 Integrity-Lock EVAL — R3 control-reframe + R4 circularity + R6 Amazon + carried spine

Pure-CPU, **$0**, read-only integrity-lock over EXISTING iter-4/5/8/9 experiment JSONs. Every
headline scalar locked here is computable from data that *already exists*, so it is **robust to
truncation** of iter-10's three new experiments (averted-cost / catalog / transfer).

Discipline: for every value → **COMPUTE** from source, **COMPARE** to stored/carried expectation,
emit a cross-check `{name,kind,computed,stored,abs_diff,rel_diff,match,status,provenance,note}`,
and **never overwrite a mismatch** (a mismatch is a documented FINDING). Map cases/holes by
CONTENT (case_id / `(concept,X)` / absorber id), never by array index.

## Run

```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python \
  numpy==2.1.3 scipy==1.14.1 statsmodels==0.14.4 loguru==0.7.2
.venv/bin/python eval.py                 # writes eval_out.json (~187 KB)
.venv/bin/python make_variants.py eval_out.json   # full/mini/preview, all schema-valid, <100MB
```

## What it locks

- **BLOCK C (R3 control-reframe — new core).** Re-runs Benjamini-Hochberg over **just** the two
  INFORMATIVE label-free selectors (S-mag = argmax mean content-response magnitude; S-rec = argmax
  content-flip recall) across the 24 spelling+taxonomic holes → KG beats **both** at FDR≤0.05 on
  **16/24** (spelling 13/21, taxonomic 3/3). This reproduces the stored all-named count (16) because
  the two dense decoder-projection controls (`dense_jtt`, `dense_dom`) resolve to the **parent/anchor**
  on all 24 holes (gain==0 → cannot recover their own hole) and are tagged **vacuous-by-construction**.
  Numeric non-triviality: on **6/7** numeric holes a stronger control matches-or-beats KG (controls are
  genuine, not strawmen). `precision_specific=False` (win is coverage, not precision-magic). Georgia:
  label-free S-mag recovers 45% of the hole yet is beaten +0.35. Downstream NULL_TEMPER: the dense
  probe out-recalls the repaired unit on **4/5** concepts (numeric −0.287, O −0.578, T −0.211,
  taxonomic −0.026; L ties).
- **BLOCK C-R4 (circularity).** States that balanced-accuracy ≈ the firing-precision selection
  criterion (mild circularity) and leans the claim on held-out generalization + the
  selection-independent behavioral next-token-KL metric from the iter-10 transfer experiment.
- **BLOCK A (selectivity-as-localization).** 16k median 1262.21×/mean 1452.47×; denominator IS the
  disowned DENSE-WHOLE-ABL strawman (footprint==1.0 on all 6); fair gate (2.79e-6) cleaner than KG
  (5.07e-5), `adv_KG_vs_FAIR` CI incl 0; 65k corrected median ~676× (never the 466997× divide-by-eps).
- **BLOCK B (carried spine).** 30 FDR survivors, **24 distinct holes (supersedes carried 22)**,
  member-labeling gap 0.634 [0.545,0.724]; cross-dict 65k full / l9 partial (55/154); numeric digit
  cosine 0.876/0.8911 below-gate; coverage 6/110 (Wilson [0.025,0.114]); named-entity 3/5;
  professions 0/28; safety 2/44 (carried iter-6); router DEMOTED; model-diffing +0.000; clustering inert 0/8.
- **BLOCK D (R6 Amazon both-metrics fallback).** adv_pres (PRIMARY) = 0.000 at full / +0.911 at n=1;
  adv_joint (SECONDARY) = +0.523 at full = instrument-disagreement, not label-scarcity. If the transfer
  experiment isolates the disagreement the paper keeps "demonstrated"; otherwise it reports both and
  softens to "demonstrated on adv_pres; adv_joint caveated".

## Result

`80` cross-checks: `68` PASS (recompute matched) + `10` CARRIED + **2 documented FINDINGS**
(65k corrected-mean floor-recipe drift; 24-supersedes-22 distinct holes) + **0 unexpected failures**.
`pass_fraction = 0.975`, `resolved_fraction = 1.0`. The C2 informative-only recompute = **16**,
reproducing the headline (statsmodels cross-checks the hand-rolled BH). `seed=1234`, `B_boot=10000`,
`tol_point=1e-3`, `llm_cost_usd=0.0`, `gpu_used=false`.

## Output (`eval_out.json`, exp_eval_sol_out schema)

- `metadata` — cross_checks[], cross_check_summary, paper_wording{W_control_reframe, W_R4_circularity,
  W_amazon_both_metrics, W_operator_table (6 ops), W_canonical_name, W_presentation_strip (12-item),
  W_selectivity_as_localization, W_section56_*, W_65k_correction, W_numeric_below_gate}, canonical_name,
  deprecated_aliases, second_variant_holes, control_reframe_note, amazon_both_metrics_note, notes.
- `metrics_agg` — 114 flat scalars.
- `datasets` — control_reframe_rows (31), settled_spine_rows (24), selectivity_localization_rows (8),
  amazon_both_metrics_rows (3), operator_definition_rows (6), cross_check_rows (80). Every example
  carries `input`, `output`, and a `predict_*` string.

## Dependencies (read-only; two live in the run__C1-INh1YNGn tree)

surgical_16k (iter-4 exp2), cross_dict (iter-5 exp2), fair_gate (iter-8 exp1), label_scarce (iter-9
exp1), coverage_screen (iter-9 exp2), spine_controls (iter-9 exp3, art_mHCB4FyqyMXL — Block C + B1).
The distinct-holes + member-labeling carry-source (iter-4 exp1 art_sxwT7hK6YFEA) is read when present
and otherwise carried as constants.
