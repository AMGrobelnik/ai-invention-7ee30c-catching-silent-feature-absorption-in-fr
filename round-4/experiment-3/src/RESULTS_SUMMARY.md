# Iter-4 — Taxonomic Unit/Specialist Conflation FIX (M2 + M3 + M5 + M7)

Re-analysis (no new data) of the frozen Gemma-Scope `layer_12/width_16k` taxonomic absorption
testbed, **reusing the iter-2/3 cached SAE encodings** (CSR latents + fp16 residuals; CPU, no GPU
re-encode). It fixes the iter-3 conflation in which the K-track classification unit's Georgia member
was the **high-coverage / low-precision** latent 4697 (sub-context firing precision 0.35) while the
diagnostic-corroborated **high-precision** specialist 16009 (0.96) lived only in the non-triviality
list. Run:

```
python method.py --hierarchies taxonomic,numeric --b-auc 10000 --b-draws 1000   # CPU, ~5 min
```

## Verdict: `taxonomic_setcover_isolated` (taxonomic) | `numeric_suggestive_diagnostic_unconfirmed`

| | taxonomic (LEAD) | numeric (contrast) |
|---|---|---|
| anchor (parent) latent | 3792 | 14823 |
| rebuilt unit (headline = **gated**) | **[3792, 16009, 540, 846]** | [14823, 8684, 7983, 13658, 2842] |
| defining absorbed slice | **Georgia** | integer |
| Georgia/integer member subctx precision (sel / held-out) | **16009: 0.97 / 0.96** | none (no integer specialist) |
| `set_cover_established` (beats all S-rec/S-prec/S-mag on defining) | **True** | False |
| `setcover_corroborated` (precision diagnostic) | **True** | False |
| router regime (defining) | mutually_exclusive(absorption), J=0.059 | co_firing(splitting), J=0.256 |

## M2 — Precision-gated/weighted K-track rebuild (the core fix)

Three greedy objective variants, all run on the **SELECTION (train) fold** (M7 fold split):

| variant | unit | Georgia member (subctx prec sel) | Georgia AUC | unit−RE-k-anch |
|---|---|---|---|---|
| `original` (raw coverage; iter-3 behaviour) | [3792, **4697**, 945, 15519] | **4697 (0.335)** | 0.9945 | +0.115 |
| `gated` (+ per-sub-context precision gate) | [3792, **16009**, 540, 846] | **16009 (0.968)** | 0.9945 | +0.157 |
| `weighted` (precision×coverage objective) | [3792, **16009**, 540, 846] | **16009 (0.968)** | 0.9945 | +0.086 |

The per-sub-context FIRING-precision gate (and the precision-weighted objective) recover the
diagnostic-corroborated Georgia specialist **16009** and drop **4697**; both fold the same Jordan
(540) and United States (846) precision-passing specialists. **Honest:** classification AUC is
~identical across variants (all three Georgia absorbers have recall 1.0 and ~0 FP on the negative
pool) — the precision rebuild buys **auditability** (a Georgia-PURE member, prec 0.97 vs 0.34), NOT
raw AUC.

## M5 — Non-random, label-free, count-matched selection isolation (Georgia)

Unit AUC = **0.995**. It beats all three anchored label-free selectors with paired-bootstrap
AUC-difference CIs (B=10,000) excluding 0:

| comparator | members | AUC | unit − comparator (95% CI) |
|---|---|---|---|
| S-rec (content-flip recall) | [3792, 12691, 6211, 10582] | 0.687 | **+0.307 [+0.267, +0.348]** |
| **S-prec** (subctx precision) | [3792, 1769, 5449, 5938] | 0.579 | **+0.416 [+0.382, +0.448]** |
| S-mag (response magnitude) | [3792, 12691, 6211, 6125] | 0.701 | **+0.294 [+0.254, +0.334]** |
| (g) top-20 marginal attr | — | 0.418 | +0.577 [+0.534, +0.619] |
| (h) count-matched marginal attr | — | 0.383 | +0.612 [+0.576, +0.648] |
| RE-k-anchored (random eligible) | — | 0.913 | +0.082 [+0.070, +0.094] |
| dense probe (non-SAE) | — | 1.000 | −0.005 [−0.008, −0.003] |

`set_cover_established = True`: the **set-cover CHOICE** of absorbers (which includes 16009 to cover
the Georgia hole) genuinely beats sensible label-free RANKING. The discriminating case is **S-prec**:
the globally most-precise latents (1769/5449/5938, precision ~1.0) are NOT Georgia-specific, so with
k−1 slots S-prec misses 16009 and collapses to AUC 0.579 — exactly where set-cover wins. The dense
probe still slightly edges the unit (honest negative).

## M2 (Phase 4) — Per-EDGE form-free KG (reported separately, NOT a 3-edge mean) + a magnitude/precision tension

The form-free `absorption_fraction` is a **MAGNITUDE** oracle (enc · W_dec·d_p). On Georgia holes its
own top pick is **1966** (subctx precision **0.34**, the high-coverage representative), not the
precise member 16009 (0.96); the two co-fire (firing-Jaccard 0.34). So per-edge top-1 agreement with
16009 is 0 — the magnitude oracle is **precision-blind** and prefers the broad latent. Corroboration
of the rebuilt unit therefore rests on the **PRECISION diagnostic** (non-triviality: precision ≥0.70
on both folds, mutual-exclusivity J<0.10, hole-coverage gain CI>0) + the router recall-hole signal,
all of which 16009/540/846 pass. (Jordan/US edges show the same magnitude-top pattern: 9339/0.63,
6125/0.50.)

## M3 — Homograph × absorption-type scope (cross-tab over ALL 52 countries)

`absorption_type` (parent recall-hole > 0.5 AND specialist firing-Jaccard < 0.10) is True for
**exactly {Georgia, Jordan}** — and both are documented homographs whose **general parent latent is
suppressed** (recall-hole 0.80 / 0.71). The hardcoded homograph set equals the dataset's
`metadata_notes=='ambiguous_homograph'` flag (no discrepancy).

| | absorption_type | NOT absorption_type |
|---|---|---|
| **homograph** | Georgia, Jordan (parent suppressed) | Chile, Turkey (parent COVERS them, hole ≈ 0) |
| **non-homograph** | — (none) | 48 countries (hole ≈ 0; incl. United States = co-firing/splitting) |

Framing: absorption recurs on polysemous/homograph tokens **whose general parent latent is
suppressed**, identified a-priori by the router recall-hole signal — it is NOT broad taxonomic
absorption. Numeric (no homographs) is the contrast: `integer` is co-firing (J=0.256) and
diagnostic-UNCONFIRMED (dense probe AUC 1.0 dominates; integer unit AUC 0.635).

## M7 — Held-out fold split + unit transparency

Gates/greedy fit on the corpus **TRAIN** fold (Georgia 150 pos); AUC/precision/router REPORTED on the
disjoint **diagnostic** fold (Georgia 150 pos). All 3 rebuilt absorbers pass held-out subctx precision
≥ 0.70 (fraction = **1.0**); member-labeling (greedy specializes vs form-free held-out modal
sub-context) agrees for all 3 (Georgia/Jordan/United States).

## Files

- `method.py` — single pipeline (copied & edited from the iter-3 method; +`run_greedy` 3-variant
  K-track, fold split, M5 selectors, M3 homograph cross-tab, ablation, transparency).
- `full/mini/preview_method_out.json` (schema `exp_gen_sol_out`, all PASS; full 10.9 MB) —
  `metadata.per_hierarchy.{taxonomic,numeric}` carries `rebuilt_units` (original/gated/weighted),
  `precision_objective_ablation`, `auc_point` + `auc_diff_ci` (incl. S-rec/S-prec/S-mag + RE-k-anchored
  + g/h/dense), `kg_agreement` (per-edge), `formfree_magnitude_tension`, `homograph_crosstab`,
  `router_all`, `selection_isolation`, `rebuilt_unit_transparency`; `datasets[].examples` carry
  per-row `predict_{unit,anchor,g,h,dense_probe,rek,S_rec,S_prec,S_mag,original,weighted}`.
- `results/` — `auc_diff_{h}.csv` (+S-* cols), `router_{h}.csv`, `router_all_{h}.csv` (+homograph),
  `ablation_{h}.csv`, `per_edge_kg_{h}.csv`, `sliced_recall_{h}.csv`, `arrays_{h}_w16384.npz`,
  `partial_{h}_iter3.json`.
- `cache/` — reused iter-2/3 SAE encodings (re-encodable; excluded from repo upload).
