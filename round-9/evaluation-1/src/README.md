# Iter-9 M4''''+M6'''' Selectivity-Localization & Spine-Consolidation Integrity-Lock

Pure-CPU, **$0**, read-only integrity-lock over EXISTING iter-4/5/8 experiment JSONs.
No model, no GPU, no LLM calls. Recomputes every headline number from its source JSON,
compares to the stored/carried expectation, and **never overwrites a mismatch** — a
mismatch is reported as a documented *finding* (this is the same discipline that earlier
caught the +1.58→+1.00 de-inflation and the 3.7e6 divide-by-eps in this project).

## Run

```bash
uv venv .venv --python=3.12 && source .venv/bin/activate
uv pip install numpy==2.2.1 scipy==1.15.1 statsmodels==0.14.4 loguru==0.7.3
python eval.py                 # writes eval_out.json
python make_variants.py eval_out.json   # writes full/mini/preview_eval_out.json
```

`eval.py` loads its four dependencies from the self-contained `deps/` copies (falling back
to the canonical runs-tree paths, then a filename glob), so the run reproduces from this
directory alone.

## Inputs (deps/)

| key            | artifact          | what it provides                                        |
|----------------|-------------------|---------------------------------------------------------|
| surgical_16k   | art_0CZwPjG2YMCf  | iter-4 exp2 KG-localized surgical edit (16k selectivity) |
| fair_gate      | art_Qdoz9eH0AGjh  | iter-8 exp1 de-inflated fair-gated unlearning (collateral)|
| repair_spine   | art_sxwT7hK6YFEA  | iter-4 exp1 KG-repair + member-labeling spine            |
| cross_dict     | art_4L1MZxvWYlGd  | iter-5 exp2 cross-dictionary replication (65k / layer-9) |

## What it computes

**Part A — M4'''' selectivity-as-localization (recompute + reframe)**
- A1: 16k absorption selectivity mean **1452.5x** / median **1262.2x** / n=5-clean median **1722.5x** (all recompute-match).
- A2: proves the selectivity *denominator* is the disowned **DENSE-WHOLE-ABL** strawman
  (DENSE-ABL `token_footprint_offtarget==1.0` on all 6 cases = unconditional whole-parent erasure).
- A3: fair-vs-KG collateral contrast on `large` — fair **2.79e-6** < KG **5.07e-5**
  (FAIR−KG collateral CI excludes 0), `adv_KG_vs_FAIR ≈ -0.05` (CI incl 0): the surgical advantage **disappears**.
- A4: 65k corrected selectivity — raw stored **466997x** is a divide-by-epsilon artifact (Georgia KG-collateral=0);
  the raw **median 676.3x reproduces the carried corrected median exactly** (median is robust to the outlier).

**Part B — M6'''' carried-spine consolidation (recompute-or-carry, all cross-checked)**
- B1: BH FDR re-run → **30 survivors** (row-by-row match with stored + statsmodels); member-labeling gap **0.634** CI [0.545, 0.724].
- B2: cross-dict **65k full / layer-9 partial**; 65k **55/154** FDR survivors; numeric digit-cosine **0.876 < 0.9** (numeric below-gate).
- B3: carried constants — safety 2/44 homograph-confined, named-entity 3/5, professions 0/28, router DEMOTED, model-diffing +0.000.
- B4: the **6-operator** definition table (defined once). B5: one canonical name. B6: presentation-strip checklist.

## Two documented findings (recompute authoritative, never overwritten)

1. **`A4.65k_corrected_selectivity_mean`** — carried mean 721.7x vs robust-recompute 828.5x.
   The *median* (676.3x) reproduces exactly; the mean is floor-recipe-dependent. **Use the median; never the raw 466997x.**
2. **`B1.distinct_holes`** — source shows **24** distinct (concept, subcontext) holes among the 30 survivors
   (6 carry a 2nd variant), not the carried **22**. **Use 24** (the headline "30 FDR survivors across 3 families" is unaffected).

## Output

`eval_out.json` (exp_eval_sol_out): `metadata` (cross_checks[49], cross_check_summary, paper_wording[8]),
`metrics_agg` (80 scalars), `datasets` (selectivity_localization_rows, operator_definition_rows,
settled_spine_rows, cross_check_rows). Cross-check tally: **47/49 passed** (38 recompute-match + 9 carried-consistent),
2 documented findings, **0 unexpected failures**. All four JSON variants validate and are <100 MB.
