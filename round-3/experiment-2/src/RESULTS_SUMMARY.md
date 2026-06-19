# Iter-3 Non-Spelling Selection-Isolation — Results Summary

Re-analysis of the executed iter-2 non-spelling absorption experiment (gen_art_experiment_3),
**reusing the frozen Gemma-Scope `layer_12/width_16k` SAE encodings** (cached CSR latents + fp16
residuals) and the same two-track K-track unit/anchor/(g)/(h)/dense-probe. It adds the three things
the iter-3 mandate requires on the NON-SPELLING slices:

- **M1 — RE-k selection isolation.** A random-eligible-k pool baseline (`RE-k`) and an anchor-fixed
  variant (`RE-k-anchored`) that isolates the two-track **set-cover SELECTION** from cover-based
  *eligibility + pooling*. `selection_established(s) = (unit AUC > RE-k-anchored 95th pct) AND
  (paired AUC-difference CI vs RE-k-anchored mean excludes 0)`.
- **M2 — AUC + AUC-difference CIs.** Classification AUC with **stratified paired-bootstrap
  AUC-DIFFERENCE CIs (B = 10,000)** for unit vs (g)/(h)/(RE-k)/(RE-k-anchored)/dense-probe, replacing
  the mislabelled matched-recall-accuracy deltas. Plus a comparison-matched (Youden) accuracy table so
  no baseline is forced to predict-all (the artefact that made (h) look degenerate in iter-2).
- **M7/M4 — router inputs.** Per-hierarchy firing-Jaccard(parent, top per-sub-context detector) on
  positives + parent per-sub-context recall holes + a per-slice form-free KG top1 — emitted as router
  inputs for the M4 prediction-vs-outcome table.

Run: `python method.py --hierarchies taxonomic,numeric --b-auc 10000 --b-draws 1000`
(CPU; cache reuse makes the core CPU-cheap. The RTX 5090 is Blackwell/sm_120 and the pinned
torch 2.6.0+cu124 has no kernels for it, so the script auto-falls-back to CPU; the GPU path is only
needed for a cache miss, which never occurs because the iter-2 encodings are reused verbatim.)

## Verdict: `taxonomic_selection_established`

| | taxonomic (LEAD, M7) | numeric (suggestive) |
|---|---|---|
| anchor (parent) latent | 3792 | 14823 |
| two-track unit | [3792, 4697, 9339, 8442] | [14823, 11011, 14413, 2285] |
| defining absorbed slice | **Georgia** | **integer** |
| `selection_established` (defining) | **True** | **False** |
| router regime (defining) | **mutually_exclusive(absorption)**, J=0.059 | co_firing(splitting), J=0.256 |
| #absorption-type slices | 2 (Georgia, Jordan) | 1 |
| KG mean top1 (form-free) | 0.318 | 0.000 |
| generalization status | diagnostic_corroborated | suggestive_diagnostic_unconfirmed |

(The two-track `anchor` and `unit` reproduce iter-2 exactly; `rng` is re-seeded per hierarchy so
results are deterministic and **independent of processing order**.)

## Headline — taxonomic Georgia (the absorbed homograph), AUC + AUC-difference CIs (B=10,000)

Per-sub-context detection: positives = Georgia diagnostic tokens (n=150); negatives = ALL taxonomic
diagnostic negatives (n=2100).

- AUC: **unit = 0.989**, anchor = 0.583, **g = 0.418, h = 0.383 (below chance — the absorption
  signature: top-marginal-attribution pools fire on negatives but are silent on the absorbed slice)**,
  RE-k = 0.906, RE-k-anchored = 0.890, **dense-probe = 1.000**.
- unit − h = **+0.606 [+0.570, +0.642]** — excludes 0. The Georgia advantage is a genuine **AUC-rank**
  effect, not merely an operating-point artefact of the iter-2 matched-recall table (the R1 fix).
- unit − g = +0.571 [+0.529, +0.612] — excludes 0.
- unit − RE-k = +0.082 [+0.070, +0.095] — excludes 0.
- **unit − RE-k-anchored = +0.099 [+0.085, +0.113] — excludes 0**, and unit sits at the 100th
  percentile of RE-k-anchored draws ⇒ the **set-cover SELECTION genuinely beats random eligible
  absorbers with the parent held fixed**. This is the M1 decider for the LEAD result.
- unit − dense-probe = −0.011 [−0.015, −0.008]. **Honest:** the non-SAE dense probe slightly edges
  the cluster unit on Georgia AUC, but the unit is the best SAE-based detector and beats every SAE
  baseline and both RE-k controls.

Router (Georgia): parent=3792, top detector=1966, firing-Jaccard=0.059 (<0.10 ⇒ mutually exclusive
with the parent), parent_recall_hole=0.80, form-free KG top1=1.0.

## Where absorption actually occurs (router table, taxonomic)

`absorption_type` (parent hole > 0.5 AND specialist firing-Jaccard < 0.10) is True for **exactly two
countries — Georgia and Jordan** — the ambiguous homographs (US state / given name) where the parent
country-latent has a genuine recall hole. Every other country has parent_recall_hole ≈ 0 (the parent
already covers it), so there is no absorption and no selection advantage (`selection_established` is
True only for Georgia and Jordan). Jordan (n=124 < 150 → DESCRIPTIVE/underpowered) corroborates with
form-free KG top1 = **0.95**.

## Numeric (integer) — suggestive, diagnostic-UNCONFIRMED (M7)

- AUC: unit = 0.687, **dense-probe = 1.000** (dominates: unit − dense = −0.313 [−0.342, −0.285]).
- unit beats g (+0.128 [+0.092,+0.164]), h (+0.114 [+0.074,+0.153]), RE-k (+0.057 [+0.024,+0.090]).
- **unit − RE-k-anchored = +0.029 [−0.006, +0.062] — INCLUDES 0.** Although unit is at the 98.8th
  percentile of RE-k-anchored draws, the paired AUC-difference CI vs the control includes 0, so the
  conjunctive rule returns `selection_established = False`. The non-spelling numeric result is
  **eligibility + pooling, not set-cover SELECTION**.
- Router (integer): firing-Jaccard = 0.256 (co-firing, NOT mutually exclusive), KG mean top1 = 0.0.
- Conclusion: numeric is **not promoted** — kept as suggestive/diagnostic-unconfirmed.

## Anti-collapse Youden accuracy table (overall + defining slice)

Comparison-matched (Youden-J fit on a held-out half) operating points; NO detector predicts-all.
On Georgia: unit balanced-acc = 0.975 (tpr 0.987, fpr 0.036); g/h have high fpr (0.70/0.82) but are
not forced to predict-all; dense-probe = 1.000; anchor misses Georgia (tpr 0.093). This is the honest
replacement for the iter-2 matched-recall table that had forced (h) to look degenerate.

## Files

- `method.py` — single pipeline (iter-2 core + iter-3 phases D–H). `--scale full` default.
- `method_out.json` (8.2 MB, schema `exp_gen_sol_out`, PASSED) — `metadata.per_hierarchy` carries
  `auc_point`, `auc_diff_ci`, `rek_distribution`, `selection_established`, `youden_overall/defining`,
  `router` (+ regime), `generalization_status`, `honest_notes`; `datasets[].examples` carry per-row
  diagnostic predictions `predict_{unit,anchor,g,h,dense_probe,rek}`. `full/mini/preview` variants.
- `results/partial_{taxonomic,numeric}_iter3.json`, `results/results.json` (metadata only),
  `results/auc_diff_{h}.csv`, `results/router_{h}.csv`, `results/sliced_recall_{h}.csv`,
  `results/arrays_{h}_w16384.npz`.
- `cache/` — reused iter-2 SAE encodings (re-encodable intermediates; excluded from repo upload).
