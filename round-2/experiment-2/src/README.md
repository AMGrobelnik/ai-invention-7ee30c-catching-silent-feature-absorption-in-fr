# Toxicity SAE-Latent Firing Structure (MAJOR-2) + C1 Count-Matched Classification + Selection Ordering

Two-Track **Counterfactual Co-Response Grouping (CCRG)** on a frozen Gemma-Scope SAE, run over the
ParaDetox + civil_comments toxicity family. This experiment tests whether **cluster-/group-level SAE
units** are more reliable than individual SAE latents for safety-attribute classification, and measures
the real **firing structure** of the SAE (not a label-co-occurrence proxy).

## What it does

Encodes every text through `gemma-2-2b` (unsloth mirror, eager attention for correct gemma-2 softcap)
and the Gemma-Scope SAE `gemma-scope-2b-pt-res-canonical / layer_12/width_16k/canonical`
(`firing = encode > 0`, JumpReLU; residual captured by a forward hook on `model.model.layers[12]`,
validated by SAE reconstruction cosine ≈ 0.91 and L0 ≈ 80/token).

**STAGE 3 — MAJOR-2 firing structure (priority 1, decisive).**
- Content-response `r_l(p) = act_mean_on - act_mean_off` on ParaDetox pairs (shuffle-sign null);
  the **general toxicity latent** `g` = highest-recall content-responsive latent (chosen from PAIRS,
  non-circular).
- Per-sub-attribute **detector** latents on civil_comments (best single-latent AUC vs clean negatives).
- **Firing-Jaccard** matrix over {g} ∪ detectors (all rows + toxic-only), bootstrap CIs.
- **Recall holes** of `g` per sub-context + how well each detector covers `g`'s holes.
- **K-necessity verdict** (CONFIRMED / REFUTED / MIXED): does any disjoint sub-attribute
  (threat, identity_attack) get carried by a latent *mutually exclusive in firing* with `g`?
  Compared directly to the label co-occurrence structure. Both branches are publishable.

**STAGE 4 — two-track unit.** C-track = signed soft-thresholded Spearman of co-response profiles +
Leiden (`RBConfigurationVertexPartition`); gamma chosen by bootstrap-ARI stability **subject to a
non-trivial, human-auditable g-community size** (ARI-stability alone collapses to one giant cluster).
K-track = anchored greedy max-coverage of `g`'s recall holes (firing-Jaccard<0.1, precision≥0.7,
marginal-gain CI excluding 0).

**STAGE 5 — C1 count-matched classification.** Primary classifier = logistic regression on each
method's **selected features** (held constant; only the SELECTION differs), evaluated on toxicity +
5 sub-attributes. Methods at matched size *k*: the co-response **unit**, best raw latent `(a)`,
co-activation neighbours `(b)`, decoder-geometry neighbours `(c)`, SCR/TPP attribution pool `(g)` /
raw-direction `(h)`, plus non-SAE diff-of-means `(d)` and full-residual LR `(e)`. Per-target paired
bootstrap (B=10000 toxicity / 2000 subs), exact McNemar, Holm-Bonferroni. Max-pool-z reported as a
secondary descriptive metric.

**STAGE 6 — selection ordering + reweight slope.** LEACE surface-invariant probe `(f)`; worst-sub-context
recall ordering `(f) ≤ (g)/(h) ≤ unit`; and the inferential **slope of the unit−(g)/(h) gap vs measured
sub-population reweighting** (upweighting threat/identity_attack).

**STAGE 7 — admission + multiplicity + surface null.** Per-candidate-unit signature-C (co-response) /
signature-K (pooled-gain) tests with a Bonferroni-within-unit p, BH across units, a surface-response
AND-gate, and the empirical family-wise false-admit rate on an AUC-matched random-k null.

## Run

```bash
uv venv .venv --python=3.12 && source .venv/bin/activate && uv pip install -e .
python method.py                 # full run -> method_out.json
python method.py --mini          # smoke (mini data, plumbing only)
python method.py --max-cls 4000 --max-pairs 4000   # fast signal check
python enrich_neuronpedia.py     # attach Neuronpedia auto-interp labels to key latents (no LLM cost)
```

GPU: single 24 GB card. Activations are disk-cached under `cache/` (not published). First run downloads
the model + SAE to `hf_cache/` (not published).

## Output

`method_out.json` (`exp_gen_sol_out` schema): `metadata` holds the full analysis
(`config`, `validation`, `firing_structure`, `unit`, `stability`, `c1`, `selection`, `admission`,
`provenance`); `datasets[0]` holds per-example test-fold toxicity predictions for every method
(`predict_unit`, `predict_a`, …). `full/mini/preview_method_out.json` are size variants.

## Honest finding (full run: 18,308 cls + 18,853 pairs)

Toxicity is a **splitting / C-track regime, not an absorption regime**. The general latent
`g=12714` ("profanity and vulgar expressions": fuck/damn/shit) fires on **94.3%** of toxic
content-flips. Distinct, on-target detector latents exist for the label-disjoint sub-attributes —
threat `11630` ("conflict and violence"), identity_attack `11573` ("race, identity, social justice"),
insult `13367` ("hypocrite/moron/coward") — and they cover `g`'s recall holes (cover-frac 0.74 / 0.93),
**but they co-fire with `g`** (firing-Jaccard 0.40 / 0.29 ≫ 0.1). So the SAE firing structure
**departs from the label co-occurrence structure**: there is no mutual-exclusivity/absorption →
K-necessity **REFUTED** on toxicity (both branches were pre-registered as publishable; the K-track
absorber win lives in the sibling first-letter experiment).

**C1 (logistic regression on selected features, AUC, test fold).** The k=3 co-response unit ties
co-activation `(b)` / decoder-geometry `(c)` / best-single `(a)` on toxicity (0.76 vs 0.77/0.80/0.79)
but is beaten by attribution selection `(g/h)`=0.84–0.89 and a full-residual probe `(e)`=0.86
(unit−h CI [−0.093,−0.055], Holm p≈5e-71), and **collapses on the disjoint sub-attributes**
(threat 0.63 vs h 0.93; identity_attack 0.63 vs h 0.94) — the benchmark pattern that simple baselines
often outperform raw-latent SAE methods.

**Selection ordering.** The pre-registered `(f) < (g)/(h) < unit` worst-sub-context-recall ordering
**does not hold** (f=0.09 < unit=0.24 < g=0.39 < h=0.45); the unit−(g/h) gap **slope vs disjoint
sub-population reweighting = −0.47 (95% CI [−0.54,−0.41], excludes 0)** — the unit's relative
advantage *shrinks* under shift toward the under-served subs. A clean honest negative.

Key latent definitions are human-auditable via Neuronpedia (`enrich_neuronpedia.py` →
`firing_structure.neuronpedia_labels`, `unit.member_labels`).
