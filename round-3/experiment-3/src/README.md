# M5 Auditability for Two-Track CCRG Units (KG Repair Loop + LLM Member-Labeling)

**Artifact:** `experiment_iter3_dir3` (GPU). Executes the two previously-dropped, now load-bearing
**auditability** results for the two-track Counterfactual Co-Response Grouping (CCRG) units on a
*frozen* Gemma-Scope layer-12 / width-16k JumpReLU SAE. It turns the iter-2 *"we emit a 70-edge
feature knowledge-graph"* **assertion** into **measured numbers**.

Units of record are READ from the deterministic iter-2 outputs (first-letter
`gen_art_experiment_1`, taxonomic `gen_art_experiment_3`; seed 1234) and re-derived as a cross-check.

## How to run
```bash
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python torch==2.6.0 --index-url https://download.pytorch.org/whl/cu124
uv pip install --python .venv/bin/python -r <pins in pyproject.toml>
HF_TOKEN=$HF_TOKEN .venv/bin/python method.py --smoke                       # load + gating only
HF_TOKEN=$HF_TOKEN .venv/bin/python method.py --concepts taxonomic,L,O,T,D  # full (~6 min, RTX 4090)
```
Gating (must pass before analysis): reconstruction cosine **0.919**, token localization exact
(align 1.000), `hidden_states[13]` (HF decoder layer 12). Core LLM spend **$0.047** (84 calls, hard
stop $10, target $3).

## What it measures

### M5a — KG-guided repair loop (load-bearing)
For each under-served sub-context (a recall hole where the anchor/parent latent goes silent) the
emitted KG *names* a covering absorber. We ADD that latent to the anchor (max-pool) and measure
recall recovery on **held-out** corpus windows (selection split = train fold / corpus folds 0-3;
eval split = diagnostic fold / corpus fold 4 — **disjoint**), versus a control that adds **every
other content-responsive latent** (the full random-addition population). Success = KG-minus-random
gain, paired-bootstrap CI (B=10,000) excludes 0.

| concept / sub-context | anchor recall | +KG recall | gain | %ile vs random | CI excl 0 |
|---|---|---|---|---|---|
| taxonomic / Georgia (4697 k-track; 16009 diag) | 0.200 | **1.000** | 0.800 | 0.994 | ✔ |
| taxonomic / Jordan (9339; 540) | 0.290 | **1.000 / 0.935** | 0.71 / 0.65 | 0.999 / 0.996 | ✔ |
| taxonomic / United States (8442; 846) | 0.767 | **0.987 / 0.973** | 0.22 / 0.21 | 0.984 / 0.978 | ✔ |
| first-letter O / "our" (1032) | 0.000 | **1.000** | 1.000 | 0.997 | ✔ |
| first-letter D / "day" (10769) | 0.000 | **1.000** | 1.000 | 1.000 | ✔ |

**8 measured successful repairs** (taxonomic ×6, first-letter ×2). Honest negatives: first-letter
**L** ("list"/"line"/…) and **T** ("type"/"things"/…) candidate words tie the random-addition
control (too few held-out windows / the added latent is no more localizing than a random
content-responsive one) — reported verbatim in `repair_loop.<concept>.honest_negatives`.

### M5a(k) — localization-failure check
The label-free group-inference probe **(k)** (JTT: ERM probe → upweight the hardest/error set →
retrain) yields a *dense reweighted hyperplane*. Its decoder-dictionary projection argmax is the
**parent (3792)**, not the absorbers (top |cos|=0.44, does not dominate; KG absorbers rank
2269/58/5964, never the argmax). (k) *classifies* the holes (recall 1.0 on Georgia/Jordan/US) but
exposes **no addable per-sub-context feature** — whereas the KG names exactly one latent. (Country
is linearly separable so the JTT error set is empty → we upweight the lowest-margin 20%; the
structural conclusion is unchanged.)

### M5b — LLM-judge member-labeling (load-bearing)
For each of **67** unit members (anchor + absorbers across taxonomic + L/O/T/D) we assemble its
logit-lens top-10 tokens + top-5 raw activating corpus windows (sub-context label **withheld** =
non-leaky) and ask `anthropic/claude-haiku-4.5` (temp 0, forced-choice) to name the sub-context.
Agreement **0.716** vs shuffle null **0.090** (analytic chance 0.087); **gap 0.627, bootstrap CI
[0.522, 0.731] excludes 0**. Per-role: absorbers **0.76**, anchors **0.20** (the judge tends to
over-specify the parent's mixed windows to one country/word — honest caveat). 0 parse failures.

## Verdict
`kg_utility_measured = True` (≥1 repair CI excludes 0) · `member_labeling_above_null = True` ·
`replaces_iter2_assertion = True`. Cross-check: re-derived content-responsive set 682 ≈ iter-2 684;
re-derived anchor 3792 matches iter-2.

## Output (`method_out.json`, `exp_gen_sol_out`-schema-valid)
`metadata` — `gating_check`, `canonical_units`, `reproduction_crosscheck`, `repair_loop`
(per-sub-context: recall_anchor / recall_anchor_plus_kg / gain_kg / kg_percentile_vs_random /
random_gain {mean,sd,p5,p50,p95} / paired_bootstrap_CI / both k-track & diagnostic variants /
honest_negatives), `k_localization_check`, `member_labeling` (per-member evidence + judge choice +
scoring with gap CI, per-role accuracy, confusion), `verdict`.
`datasets` — `kg_repair_loop` rows and `member_labeling` rows (with `predict_judge`) for downstream
solution evaluation.

## Files
- `method.py` — full pipeline (SAE+model load, gating, unified encoder, repair loop, (k) check,
  member-labeling, output).
- `method_out.json` / `full_/mini_/preview_method_out.json` — results (schema PASSED, all <100MB).
- `pyproject.toml` — pinned deps. `logs/` — run logs.
