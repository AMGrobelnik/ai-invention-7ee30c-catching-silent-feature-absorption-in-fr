# Iter-3 Decisive Re-Run — Two-Track CCRG (First-Letter Spelling)

Random-Eligible-k baseline (M1) + AUC-difference CIs / pooled meta / Youden accuracy (M2) +
verdict reconciliation from the stated falsifier (M3), on the executed iter-2 pipeline.

This artifact **re-runs the iter-2 two-track Counterfactual Co-Response Grouping (CCRG) first-letter
pipeline verbatim** (frozen Gemma-Scope L12/16k JumpReLU SAE, gating cosine > 0.9, exact word-token
localization) and surgically **adds three fixes** that decide whether the contribution is *two-track
SELECTION* or merely *cover-based eligibility + max-pooling*. Nothing in the load-bearing method was
re-derived; the iter-2 `method.py` was copied and new code paths were appended.

## What the three fixes are

- **M1 — Random-Eligible-k (RE-k) baseline (decisive).** For each letter we draw `k = |unit|` latents
  uniformly at random from the **cover-eligible set** `E = Lr` (`precision ≥ 0.7 ∧ covers ≥ 1
  sub-context ∧ net-positive response`), max-pool them with the *identical* pooling rule used by the
  unit / (h) / (b) / (c), and repeat for `B_draws` draws. Because RE-k differs from the two-track unit
  **only** in the membership/SELECTION criterion (everything else — eligibility filter, pool size,
  max-pool — is held constant), `unit − RE-k` isolates *selection* from *eligibility+pooling*. The
  single most decisive number is **`frac_rek_ge_unit`** = fraction of random eligible pools whose
  test-fold AUC matches or beats the two-track unit (a one-sided permutation p-value). RE-k is added to
  both **C1** (classification) and **E2** (absorbed-slice recall).

- **M2 — AUC points + AUC-difference CIs (replaces the accuracy-as-margin artifact).** `per_method.AUC`
  is the threshold-free held-out **test-fold AUC point** (reproduces iter-2). We add **bootstrap
  AUC-DIFFERENCE CIs** (`B ≥ 10,000`, whole content-flip **pair** cluster resampling on the test fold)
  for `unit` vs `(a)/(b)/(c)/(h)/(RE-k)` on every letter, plus a **pooled-across-letters stratified
  meta-analysis** (test-pair-weighted stratified cluster bootstrap, primary; fixed-effect
  inverse-variance, secondary). All accuracy is reported at a comparison-matched **Youden (TPR−FPR)**
  threshold so no baseline collapses to predict-all-positive; the iter-2 **F1-threshold** accuracy is
  retained and flagged (`accuracy_f1thresh`, `f1thresh_collapse`) to document the artifact.

- **M3 — Verdict from the stated falsifier.** `primary_endpoint` is computed from
  *E1 AND unit-AUC-significantly-above-BOTH-(h)-and-(RE-k) on ≥ 3/5 letters*. E1 (4/5; fails on I) and
  E2 (2/5; only T, I — **not** primary L) are reported transparently and **E2 is never silently dropped
  from a conjunction** (iter-2 computed the headline "WORKS" as `E1 ∧ C1` and dropped E2). Outcomes:
  - `ABSORPTION_REPAIR_SELECTION_CONFIRMED` — E1 ∧ `n_selection ≥ 3` (unit beats BOTH h AND RE-k).
  - `REFRAMED_TO_ELIGIBILITY_POOLING` — `n_selection + n_eligibility ≥ 3` but `n_selection < 3`
    (unit beats attribution (h) via eligibility+pooling, but not the random-eligible-k control).
  - `SELECTION_NOT_ESTABLISHED` — otherwise.
  Both of the first two are publishable; the reframe is an honest-negative success, not a failure.

## Scope

First-letter pipeline **only** (5 letters L, O, T, I, D). The non-spelling RE-k is a separate
dataset/artifact and is out of scope here. Steering is **off by default** (`--steering` to opt in); it
was already executed in iter-2 and is not a deliverable of this re-run.

## Data
- First-letter testbed: `iter_1/.../gen_art_dataset_1/full_data_out.json` (`art_dpYpjSn2Xvg3`).
- Surface superset (admission null): `iter_2/.../gen_art_dataset_1/full_data_out.json`
  (`art_YwjLYapklnVk`, 1,700 first-letter surface pairs, independently judged).

## How to run
```bash
uv sync
uv run method.py --smoke                       # stage 0: load + reconstruction gating check
uv run method.py --letters L --mini            # stage 1: mini plumbing test on L
uv run method.py --letters L                    # stage 2: full L (reproduction anchor)
uv run method.py --letters L,O,T,I,D            # stage 3: full 5-letter decisive run (default)
```
Key flags: `--b_gap` (AUC-diff/accuracy bootstrap B, default 10000), `--rek_draws` (RE-k draws, default
1000), `--no-superset-surface` (use iter-1 inline surface pairs), `--steering` (opt-in).

## Hardware note (reproduction)
iter-2 ran on torch 2.6.0+cu126, which lacks Blackwell (sm_120) kernels and **cannot execute on this
RTX 5090**. This re-run uses **torch 2.8.0+cu128** (Blackwell-compatible); all non-torch dependencies
are pinned identically to iter-2 to preserve model-forward numerics. AUC is rank-based and robust to
the residual bf16 differences across the torch/GPU change. Reproduction is verified against the
iter-2 anchors (gating cosine ≈ 0.92; unit test AUC L 0.905, O 0.917, T 0.859, I 0.961, D 0.956;
E1 4/5 with I failing; E2 2/5 with only T, I).

## Output
`method_out.json` (schema `exp_gen_sol_out`): top-level `{metadata, datasets}`. All analysis under
`metadata.*` (`per_letter`, `verdicts`, `pooled_across_letters`, `endpoint_reconciliation_note`,
`config`, `gating_check`). `datasets` = one group per letter of held-out **test-fold** example rows
with `predict_unit/a/b/c/h/REk` (Youden-thresholded) alongside `input`/`output`. The large per-letter
bootstrap `_diffs` arrays are kept out of the JSON (held in memory only for the pooled meta).

## RESULTS

_Filled in after the full 5-letter run — see `metadata.verdicts` in `method_out.json`._
