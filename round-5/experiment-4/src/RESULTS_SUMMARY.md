# M7 (iter-5) — Second Polysemy/Absorption Case Beyond Georgia

**Verdict: `absorption_remains_narrow`** — the publishable honest negative the plan anticipated.

Three parts on the **frozen** Gemma-2-2b / Gemma-Scope `layer_12/width_16k` JumpReLU SAE
(`blocks.12.hook_resid_post` = `hidden_states[13]`, d_model=2304), asking whether the iter-4
non-spelling absorption / set-cover result (effectively **n=1**, Georgia; 1–2 with descriptive
Jordan) corroborates on a **second** suppressed-parent case.

```
uv run method.py --scale full --parts 1,2,3 --b-auc 10000 --b-draws 1000   # ~16 min (Part 1 GPU encode ~6 min)
```

Method vs **baselines**, held side-by-side in one pipeline:
two-track set-cover **unit** vs **raw-SAE** {anchor, g=top-20 marginal-attr, h=count-matched,
S_rec/S_prec/S_mag label-free selectors, RE-k-anchored} vs **non-SAE** {dense difference-of-means probe}.

---

## PART 1 — Profession is-a hierarchy (bias_in_bios) — **NEW science, fresh GPU encode**

Is absorption a property of a *clean is-a hierarchy*? Parent = a general **occupation/biography**
latent; children = the 28 professions. bias_in_bios rows have no content pairs / target spans, so we
**whole-text** encode (mean residual / max latent over all non-special tokens); 13,843 bios (cap
500/profession, gender-stratified) + 5,000 non-bio negatives (movie + restaurant reviews) from the
same corpus file. **Encode validation: per-token FVU = 0.173, mean L0 = 76.9** (SAE/layer pipeline
correct). 50/50 selection/diagnostic split, stratified by profession.

**Corpus-only parent** = `latent 12692` (discriminative bio-vs-review, content-style precision 0.906,
held-out recall **0.973**, fires on >5% held-out — passes the firing-floor). The bios-vs-review dense
probe AUC is **1.000** (the genre is trivially separable — exactly the confound the within-bios
one-vs-rest design guards against).

### Per-profession hole table (all 28, held-out fold) — the headline deliverable

| | result |
|---|---|
| max parent recall **hole** | **0.116** (profession `model`) — every other ≤ 0.064 |
| professions with `absorption_type` (hole>0.5 **AND** mutually-exclusive specialist J<0.10) | **0 / 28** |
| parent recall range across professions | **0.88 – 1.00** (uniform-high) |

➡️ **`uniform_high_parent_recall_no_absorption`.** The general occupation parent fires on 88–100 % of
*every* profession's bios — there is **no suppressed-parent hole** for a specialist to fill. Absorption
does **not** generalise to the profession is-a hierarchy. (`model` is instructive: it *does* have 14
mutually-exclusive specialists (best J=0.002, precision 1.0), but the parent still covers 88 % of
models, so hole 0.116 ≪ 0.5 → correctly **not** absorption. It also shows a gender asymmetry: male-model
hole 0.19 vs female 0.04.)

### Baseline comparison on the largest-hole profession (`model`, one-vs-rest, DESCRIPTIVE)

With no absorption hole, the set-cover greedy adds **no** absorber → the "unit" degenerates to the bare
parent, and a general parent is a **poor** specific-class detector:

| detector | one-vs-rest AUC (`model`) |
|---|---|
| **unit (= parent 12692)** | **0.308** |
| g (top-20 marginal-attr) | 0.544 |
| dense difference probe (non-SAE) | 0.961 |

`set_cover_established = False` (unit beats none of g / h / dense / selectors). This is the honest
**contrast** to Georgia below: the two-track method only helps when a suppressed-parent absorption
signature actually exists.

---

## PART 2 — Homograph scan (CPU, iter-4 taxonomic cache)

Re-running the taxonomic pipeline from cache reproduces iter-4 **exactly**. `absorption_type` (parent
recall-hole > 0.5 **and** specialist firing-Jaccard < 0.10) is True for **exactly {Georgia, Jordan}**,
both documented homographs whose general "country" parent (`3792`) is suppressed:

| | absorption_type | NOT absorption_type |
|---|---|---|
| **homograph** | Georgia, Jordan | Chile, Turkey (parent covers them) |
| **non-homograph** | — (none) | 48 countries incl. United States (co-firing/splitting) |

**Entity-token scan** (20 country-mention surfaces with ≥150 diagnostic occurrences): the only
`absorption_type` surface is **Georgia** (Jordan's n=124 < 150 → below the inferential floor).
**No new case beyond Georgia/Jordan.** Honest coverage limit: the testbed labels per-**country**, not
per-city, so non-country entity absorption is **untestable** here — "no new case" is expected, not
exhaustive.

## PART 3 — Jordan beside Georgia (CPU, cache)

| country | n_pos | eligible | absorption_type | parent hole | firing-Jaccard | unit AUC | set_cover_established | status |
|---|---|---|---|---|---|---|---|---|
| **Georgia** | 150 | ✅ | ✅ | 0.80 | 0.059 | **0.995** | **True** | eligible (inferential) |
| **Jordan** | 124 | ❌ | ✅ | 0.71 | 0.021 | 0.957 | — | descriptive (underpowered) |
| **United States** | 150 | ✅ | ❌ | 0.23 | **0.204** | 0.974 | — | co-firing (not absorption) |

Georgia unit beats every label-free / attribution baseline (paired-bootstrap AUC-diff, B=10,000,
95 % CI excluding 0): **S-rec +0.307 [0.267, 0.348]**, **S-prec +0.416 [0.382, 0.448]**, **S-mag
+0.294 [0.254, 0.334]**, RE-k-anch +0.082 [0.070, 0.094], g +0.577, h +0.612. The non-SAE dense probe
still slightly edges it (−0.005 [−0.008, −0.003]) — an honest negative (the contribution is auditable
within-SAE precision-gated selection, not out-classifying a dense probe).

---

## Bottom line (honest negatives)

1. **Absorption is narrow.** Affirmative non-spelling set-cover evidence remains **one eligible slice
   (Georgia)**, 1–2 counting descriptive Jordan. The clean profession is-a hierarchy adds **zero** new
   eligible cases (uniform-high parent recall, 0/28 absorption_type).
2. Absorption recurs specifically on **suppressed-parent homograph polysemy**, not on general is-a /
   taxonomic structure — a positive scoping result for the iter-4 framing.
3. Entity scan surfaces no new case (coverage-limited to country labels).
4. The two-track method **degenerates to the bare parent and loses to baselines** when no absorption
   hole exists (`model` AUC 0.308) — it only helps where the signature is present (Georgia AUC 0.995).

## Files

- `method.py` — orchestrator (Part 1 driver + Parts 2-3 taxonomic re-run + verdict + emit).
- `profession_absorption.py` — Part 1: whole-text encoder, corpus-only parent ID, 28-profession hole
  table, per-profession set-cover + selection-isolation (reuses `engine.run_greedy` / `fast_auc` /
  `_auc_rows` / bootstrap machinery).
- `engine.py` — iter-4 method copied verbatim (2107 lines), reused for the taxonomic cache path.
- `method_out.json` (+ `full/mini/preview_`) — `exp_gen_sol_out` schema, all PASS, 3.0 MB <100 MB.
  `metadata.per_family.{professions,taxonomic}` carries the full hole table, parent, set-cover with
  CIs, homograph cross-tab, entity scan, and the Jordan-beside-Georgia side-by-side;
  `datasets[].examples` carry per-row `predict_{unit,anchor,g,h,dense_probe,rek,S_rec,S_prec,S_mag}`.
- `results/` — `hole_table_professions.csv` (28 rows), `setcover_auc_diff_model.csv`,
  `side_by_side_jordan_georgia.csv`, `homograph_crosstab.csv`, `arrays_taxonomic_w16384.npz`.
- `cache/` — SAE encodings (frozen taxonomic from iter-4 + fresh whole-text bios/neg); re-encodable,
  **excluded from repo upload**.

## SAE / reproducibility
`gemma-scope-2b-pt-res-canonical` / `layer_12/width_16k/canonical` (avg L0 82) on `google/gemma-2-2b`;
seed 20240617; thresholds G1_recall 0.60, jaccard_max 0.10, subctx_precision 0.70, gain_min 0.05,
precision_floor 0.70, n_min_eligible 150, firing_floor_heldout 0.05; GPU = NVIDIA L4 (sm_89). Re-runs
are GPU-free (whole-text encodings cached).
