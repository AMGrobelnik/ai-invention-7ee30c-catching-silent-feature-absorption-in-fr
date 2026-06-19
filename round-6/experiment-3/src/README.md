# M4 — Recall-Hole Router: Homograph Prospective Expansion (validate-or-demote) + M7 Breadth

Reuses the iter-5 a-priori SAE firing-structure router **verbatim** (`core.py`) and applies the
**frozen** recall-hole-alone rule (`predict ABSORPTION iff parent recall-hole > tau_h_alone`, fit
ONLY on the 12 frozen derivation concepts) to a **much larger truly-prospective set**: ~93
homograph entities across 4 is-a hierarchies (cities / months / given-names / brands) from the
homograph testbed, plus the 7 internal new-spelling letters. Per-entity **predict-then-measure**:
the regime is predicted and logged *before* the per-entity outcome (label-free CCRG unit vs best
raw latent **(a)** / attribution pool **(h)** / non-SAE residual probe **(d)**) is measured;
`hit = (predicted == sign(auc_unit - auc_a))`.

## Headline results (`method_out.json`)

- **Integrity:** the frozen rule **reproduces iter-5 exactly** — `tau_h_alone = 0.7795`
  (drift 0.0000), derivation balanced_acc = 1.000, LOO = 0.833. Gating recon-cos = 0.927.
- **M4 verdict = `ROUTER_DEMOTED`** (honest negative). The router validates on the *base-rate*
  co-firing direction (co-firing-predicted 29/30, Wilson95 [0.833, 0.994]) but the **discriminative
  absorption-predicted stratum** is underpowered and its CI includes 0.5: homograph absorption
  stratum 2/4 [0.15, 0.85]; homograph+spelling absorption stratum 5/10 [0.237, 0.763]. So as an
  *a-priori predictor of where grouping helps* it is an **exploratory diagnostic, not validated**.
- **M7 breadth — absorption is NARROW.** Of 64 homograph entities with a stable recall-hole
  estimate (n>=30), only **3 are absorption-structured** (recall-hole > 0.5 AND firing-Jaccard < 0.1),
  **all in the month hierarchy** (cities 0/22, given-names 0/20, brands 0/10). This directly answers
  the "absorption is n=1-2" critique with a systematic count. **New named suppressed-parent
  homographs:** March (hole 0.997), June (0.947), February (0.573).
- **Structural != downstream.** The strongest *downstream-confirmed* absorption case (label-free unit
  actually beats the best raw latent) is **month/May: delta_vs_a = +0.160** (is-a-month parent misses
  98% of "May" mentions, absorbed by the modal verb; grouping recovers a beating unit) — even though
  May is NOT "structured" (jaccard 0.434). The structurally-shaped months (March/June/February) are
  co-firing downstream. Structural shape does not guarantee a grouping benefit.

34 of the ~93 entities are eligible (>=150 diagnostic-fold positives) — a 5.6x expansion of the
iter-5 prospective set. SAE = `google/gemma-scope-2b-pt-res` L12/16k JumpReLU; model =
`unsloth/gemma-2-2b`; SEED=1234; $0 LLM.

## Files

| file | what |
|---|---|
| `core.py` | iter-5 router copied VERBATIM (SAE/Encoder/identify_parent/ktrack_lite_unit/_outcome_core/derive_*/predict_*/wilson_ci/...) |
| `method.py` | M4 extension: homograph loader, per-entity predict-then-measure router, Wilson-CI verdict, M7 breadth, exp_gen_sol_out emit. Adds two surgical numerical-stability patches over core (NaN/inf-safe residual probe + `auc`) and `B_BOOT=2000` |
| `post_process.py` | pure DERIVED enrichment (downstream-confirmed-absorption view); no re-measurement |
| `method_out.json` + `full_/mini_/preview_method_out.json` | the artifact (exp_gen_sol_out; 111 cards = 12 derivation + 7 spelling + 92 homograph entities) |
| `method_out_smoke.json` / `method_out_mini.json` | gradual-scaling test outputs |
| `homograph_build/` | the homograph testbed builder (data.py/build_dataset.py/pipeline.py) + the rebuilt `full_data_out.json` (38 MB, 34,357 rows, $0) |

## Reproduce

```bash
# 1. rebuild the homograph corpus (CPU/network, ~40 min, $0) — needed because the source dep ships
#    only the builder, not full_data_out.json:
cd homograph_build && .venv/bin/python pipeline.py --scale full --no-llm
# 2. run the router (single GPU, ~50 min):
.venv/bin/python method.py --scale full --homograph_data homograph_build/full_data_out.json
.venv/bin/python post_process.py method_out.json
```
`method.py --smoke` (gating + city hierarchy) and `--scale mini` give fast end-to-end checks.
