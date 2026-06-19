# Evaluation iter-6 dir-5 — M3/M4/M8 (+M5/M7) Integrity-Lock Consolidation

**Pure CPU-only re-analysis ($0, no GPU, no encoding, no LLM).** Reads four existing
JSONs, recomputes the iter-5 reviewer-flagged headline numbers, and emits cross-checked,
drop-in paper wording. Source experiment JSONs are ground truth: every headline value is
COMPUTED then COMPARED to the stored/expected value, and any mismatch is reported with an
explanatory note (the "integrity lock").

## Run
```bash
uv venv .venv --python=3.12 && source .venv/bin/activate && uv pip install numpy scipy loguru
python eval.py
```
Runs in seconds. Output: `eval_out.json` (+ `full_/mini_/preview_` variants), schema
`exp_eval_sol_out`.

## Reviewer-mandate blocks (mapped by CONTENT, not by the iter-5 eval's internal labels)
- **M3 — cross-dictionary selectivity artifact (NEW load-bearing).** The stored 65k
  "absorption mean selectivity 466997x" and "Georgia 3.7e6x" are divide-by-epsilon
  artifacts (kg_collateral=0 → ratio=on_target/1e-8). Excluding floor-limited (kg_coll==0)
  and NO_ON_TARGET_EFFECT cases, the **corrected 65k absorption mean = 721.7x (median
  676.3x, n=4)** [primary], or 483.1x (median 184.6x, n=6) [keep tiny nulls]. 65k Georgia
  (floor-limited ≥ ~371x at 1e-4, ≥ ~1290x ref to 16k 2.9e-5 collateral) is **comparably
  surgical** to 16k Georgia (1722x), **not ~2000x apart**. Plus the honest layer-9 note.
- **M4 — router out-of-sample Wilson-CI (NEW).** Prospective absorption-predicted hit-rate
  is exactly chance (**3/6=0.50, Wilson [0.188,0.812] INCLUDES 0.5**); combined 11/18=0.61
  [0.386,0.797] INCLUDES 0.5. recall-hole=1.0 over-predicts absorption on new letters
  **F/M/W** (which measure co-firing). The vs-h 14/19 [0.512,0.882] (excludes 0.5) is
  flagged SECONDARY/non-primary. Decision: **DEMOTE to exploratory diagnostic** (iter-6
  run-tree scan found no expansion experiment with a CI excluding 0.5).
- **M8 — honest counting (carry D4, re-verify selectivity from D2).** 22 distinct holes
  (=30−6−2); absorption mean **1452.47** / median **1262.21** (the draft's "1452 median"
  is the MEAN); surgical-5 median 1722.46; within-taxonomic Spearman ρ=**0.90** (not 1.0);
  random SINGLE-latent control 28/28>p95, 23/28>p99; member-labeling gap 0.6344
  [0.545,0.724]; numeric flagged below-gate (digit cosine 0.876<0.90).
- **M5 — US consistency.** US = CO-FIRING (aggregate recall-hole 0.20–0.23 < τ_h 0.78), yet
  narrow absorber 846 = 214x surgical → router FALSE-NEGATIVE. Jaccard 0.04 (specific 846)
  vs 0.20 (aggregate detector).
- **M7 — grouping → label-free DISCOVERY procedure.** Wins trace to individual absorbers
  (Georgia 16009, large 8463, US 846), not multi-member grouping; C-track ties weak
  baselines (toxicity 0.762 vs 0.765); set-cover-specific on only I, D, Georgia.

## Integrity lock
44 cross-checks, **43 pass**. The one intentional mismatch is `m3_n_floor_limited`:
computed **2** (both Georgia/46143 and Jordan/60904 have kg_collateral==0.0, per the plan's
own definition) vs the plan's metrics-anchor of 1 (which counts only the floor-limited case
retaining an on-target effect). Reported honestly with a note — the JSON is truth, the
anchor is guidance. This mirrors the iter-5 eval, which likewise honestly carried
computed≠planned values (22≠23 holes, 2≠1 non-hole, ρ=0.90≠1.0).

## Sources
- D1 `art_4L1MZxvWYlGd` iter-5 exp2 cross-dict 65k — `replication_tables['65k']`
- D2 `art_0CZwPjG2YMCf` iter-4 exp2 surgical 16k — `metadata.per_case`
- D3 `art_4q5Om8wdqZuz` iter-5 exp3 router — `prospective_hitrate_primary`
- D4 `art_-k4Yg-l4NaNO` iter-5 consolidation eval — counting/control/transparency template

## Output datasets (schema-valid; every example has predict_* string + input + output)
`M3_selectivity_cases` (16=9×65k+7×16k), `M4_router_prospective_strata` (4),
`M4_new_letter_directionality` (7), `M8_distinct_hole_survivors` (30, from D4),
`M8_selectivity_reverify` (7).
