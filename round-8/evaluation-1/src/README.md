# Iter-8 Integrity-Lock Eval

Pure-CPU, **$0**, read-only re-analysis over the EXISTING iter-6/7 edit data. No GPU, no model
load, no LLM calls. Following the project **integrity-lock** pattern: every headline value is
**RECOMPUTED from source columns**, then **COMPARED to the stored expectation**; mismatches are
recorded in `metadata.cross_checks` and **never overwritten**. Deterministic (`seed=1234`,
`B_boot=10000`).

## Run

```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python numpy scipy loguru
.venv/bin/python eval.py
.venv/bin/python make_variants.py eval_out.json   # full/mini/preview
```

## Inputs (copied into `deps/` for reproducibility)

| tag | source | used for |
|-----|--------|----------|
| D1 | iter-7 exp1 (`M1''` gated-dense control) | per-prompt utilities, per-case operating points |
| D2 | iter-7 exp2 (named-entity homograph downstream) | Amazon/Bush supporting cases, gate calibration |
| D3 | iter-6 exp1 (`M1'` u_sub baseline) | Georgia +0.561 retraction source |

## What it computes (Groups A–E)

- **A — De-inflation.** Recomputes mean joint utility (`HM(fluency, content_pres)`) per operator
  from the 288 per-prompt rows and the paired-bootstrap joint diffs. The honest lead is
  **KG vs the strongest UNGATED dense = +1.00** (CI [0.79, 1.21], n=36) on `large`; the inflated
  **+1.58 vs a footprint-matched gate** is a robustness check handicapped by **β≈2.97 over-erasure**
  (gated retain-collateral 0.290 = **13.8× its own ungated 0.021**). Reconciliation
  `1.8704−0.8704=+1.00`, `1.8704−0.2870=+1.58` verified to <1e-3.
- **B — Both forget instruments side-by-side.** Gold-completion-drop AND frozen sub-probe-drop per
  (case, operator). At the KL-matched point the two instruments **disagree in sign** for `large`
  (completion favors the gated dense by −1.01, sub-probe favors KG by +0.42) ⇒ **KL-matching ≠
  behavioral matching**. Raw sign-flips fire in 3 cases, but only `large` is **material** (both
  instruments move; the other 2 flip on near-zero magnitudes). The `large` completion CI is over
  only **n=4** probes (rigor caveat).
- **C — Concentration vs absorption predictor (descriptive, n≈7).** Per-case proxies vs the
  absorption-regime label. **The win predictor is concentration (precision × single-latent
  leverage), NOT absorption:** v2 = `precision × max_forget_kg` tracks the win
  (point-biserial r=+0.63) where the absorption label does not (r=−0.09). The inverse-FOOTPRINT
  proxy v1 = `precision / f_kg` **anti-correlates** (r=−0.80) — distributed senses also fire
  sparsely, so footprint sparsity alone is not concentration. Wins cross both regime labels
  (absorption `large`, co-firing `insult`); losses are distributed senses (Georgia/Jordan/US) and a
  low-leverage homograph (Bush). Supersedes the thin 1-case-vs-2-case `absorption_exceeds_cofiring`
  aggregate.
- **D — Georgia +0.561 retraction.** The iter-6 KG-vs-dense win (+0.561, recomputed from D3 to
  +0.5606) sat at a **near-NOOP** operating point: single-latent forget-KL ceiling 0.065
  (17–30× below dense), NOOP-identical on 89% of forget prompts, frozen sub-probe drop 0.075,
  completion CI excludes-0 = false. Retracted as low-collateral **partial suppression**, not
  meaningful unlearning.
- **E — Operator-divergence flag.** D1 gate = ~3% **global** token-footprint match
  (`calibrate_gate_tau`); D2 gate = ~95% **X-positive** firing-rate clamp
  (`footprint_match_clamped`). The cross-experiment headline aggregates a 3%-global comparison
  (large) with a 95%-X-rate comparison (Amazon); iter-8 must unify into ONE gate operator.

## Outputs

- `eval_out.json` (+ `full_`/`mini_`/`preview_`, all validate against `exp_eval_sol_out`, <100 MB).
  - `metrics_agg` — 53 numeric drop-in metrics.
  - `datasets` — `de_inflation_per_case` (7), `both_instrument_per_case_op` (15),
    `concentration_predictor_per_case` (7), `retraction_per_case` (1), `operator_divergence` (2).
  - `metadata.cross_checks` — 44 recompute-vs-stored checks (**44/44 pass**), `paper_wording`
    (W1–W5 drop-in strings), `group_c_correlations`, materiality notes.

All recomputed point estimates match stored to <1e-3; bootstrap CIs match by overlap (the original
run's global RNG state differed, so CIs are re-seeded fresh and compared by interval overlap, never
overwritten).
