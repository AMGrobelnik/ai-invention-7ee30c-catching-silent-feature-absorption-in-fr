# M1a + M7 Auditability Spine (expanded) — iter-4 experiment_1

**Artifact:** `gen_plan_experiment_1_idx1` (GPU). Expands the iter-3 measured-auditability result
(`iter_3/gen_art/gen_art_experiment_3`) from **8 KG repairs / 67 labelled members** to the **FULL**
set of eligible absorbed sub-contexts, across **three** concept families, on a *frozen* Gemma-Scope
**L12 / width-16k** JumpReLU SAE (`google/gemma-scope-2b-pt-res`, `average_l0_82`) over
`google/gemma-2-2b`:

* **spelling** — first-letter `L / O / T / I / D` word absorption (dataset `art_dpYpjSn2Xvg3`)
* **homograph-taxonomic** — country absorption incl. flagged homographs Georgia / Jordan / Turkey /
  Chile / … (dataset `art_t2uUbjSwpd3t`)
* **numeric** — year / percent / currency / date / decimal / integer / comma_number / ordinal

The iter-3 pipeline (SAE loader, JumpReLU `encode>0`, hook `blocks.12.hook_resid_post`, gating
`cosine>0.9`, repair loop, `k_localization_check`, LLM judge) is reused; the expansion adds the four
pieces below.

## How to run
```bash
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python torch==2.6.0 --index-url https://download.pytorch.org/whl/cu124
uv pip install --python .venv/bin/python <pins in pyproject.toml>
HF_TOKEN=$HF_TOKEN .venv/bin/python method.py --smoke                       # load + gating only
HF_TOKEN=$HF_TOKEN .venv/bin/python method.py --concepts taxonomic --no_llm  # mini pilot (reproduce iter-3)
HF_TOKEN=$HF_TOKEN .venv/bin/python method.py                                # full run (all concepts + LLM)
```
After the model is cached, add `HF_HUB_OFFLINE=1` to skip the ~140 s gated-repo metadata check.
Encodings are disk-cached under `cache/` (reused across staged runs; excluded from the repo).

## What it measures

### M1a — BROAD K-track KG-guided repair loop (load-bearing)
For **EVERY** eligible sub-context X (≥ `N_MIN_SEL=10` selection + `N_MIN_RELAX=15` eval positives)
the K-track greedy NAMES a covering absorber, derived **purely on the selection split**
(non-circular vs eval):

> `kg_absorber[X] = argmax_{l ∈ content-responsive, l≠anchor, jaccard(l,anchor)<0.10, subctx_prec(l,X)≥0.70} recall_l(X-selection)`

We ADD the named absorber to the parent/anchor (max-pool) and MEASURE recall recovery on **held-out**
eval windows vs a control that adds **every other content-responsive latent** (the full
random-addition population). Per repair: `gain_kg`, `kg_percentile_vs_random`, paired-bootstrap CI
(B=10,000) **and a one-sided bootstrap p-value** (H0: KG-minus-random gain ≤ 0). Taxonomic also
reports the iter-3 diagnostic-corroborated absorbers as a `kg_diagnostic` variant.

### MULTIPLICITY — Benjamini-Hochberg FDR ≤ 0.05 (in-experiment)
All repair variants across **all** concepts enter one BH family; each gets a `bh_q` and
`survives_FDR` flag, with a per-family breakdown (spelling / homograph-taxonomic / numeric).
Hand-rolled BH is cross-checked against `statsmodels`.

### M1a(k) — localization-failure check, run per concept (taxonomic, numeric, first-letter)
Label-free group inference (**JTT**: ERM probe → upweight error/low-margin set → retrain) yields a
*dense* reweighted hyperplane. We project it onto the SAE decoder dictionary and report the argmax
latent (expect the **parent/anchor**, not an absorber), whether a single latent dominates (expect
False), and the per-sub-context KG-absorber projection ranks (expect deep). Conclusion: (k)
*classifies* the holes but exposes **no addable per-sub-context feature**, whereas the KG names
exactly one latent.

### M7 — ensemble LLM-judge member-labeling + 15-wide confident fraction (load-bearing)
Every admitted-unit member — INCLUDING **all 15 members of each first-letter max-pool** `K_UNIT` —
gets **J=3** forced-choice judge calls (`anthropic/claude-haiku-4.5`, temp 0) with the candidate
option **order shuffled** across calls (kills position bias). We report agreement vs a shuffle null
(gap bootstrap CI), per-role accuracy, and the **fraction of members (and of each 15-wide pool)**
receiving a *confident* label (majority is a specific sub-context, agreement ≥ 2/3, above per-member
chance). LLM target < $1, hard stop $10; degrades J 3→1 then `--no_llm` if budget-constrained.

## Honest negatives
KG repairs that tie the random-addition control (e.g. numeric ties — the parent already covers most
numeric tokens, strengthening the *homograph-scope* story; sparse first-letter words) are emitted
verbatim in `repair_loop.<concept>.honest_negatives` and aggregated in `metadata.honest_negatives`.
A supplementary **pooled** first-letter repair (union of a letter's hole-words) is reported when
per-word eval slices are scarce.

## Output (`method_out.json`, `exp_gen_sol_out`-schema-valid)
`metadata` — `gating_check`, `canonical_units`, `reproduction_crosscheck`, `broad_kg`
(per-sub-context derivation), `repair_loop` (per-X: anchor/+KG recalls, random-gain dist, variants
with CI + one-sided p + `bh_q` + `survives_FDR`, honest negatives), `multiplicity`,
`k_localization_check` (per concept), `member_labeling` (per-member ensemble evidence + scoring with
gap CI, per-role accuracy, `confident_label_fraction`, `first_letter_15wide_confident_fraction`),
`honest_negatives`, `verdict`.
`datasets` — `kg_repair_loop` rows (one per concept×X×variant; output ∈
{`survives_FDR`,`repair_significant`,`tie_with_random`}) and `member_labeling` rows (gt label,
`predict_judge`, confident/correct/agree_rate).

## Final results (full run, seed 1234)
Gating (taxonomic country tokens, global SAE/layer check): cosine **0.9189**, L0 87.9, align 1.000,
`hidden_states[13]`. Re-derived anchors match iter-2 exactly (taxonomic 3792, numeric 14823); letter
anchors from E1.

**M1a broad KG repair — 69 variants tested, 54 holes, 30 survive Benjamini-Hochberg FDR≤0.05**
(statsmodels-confirmed), per family:
| family | survive FDR≤0.05 | example repairs (gain_kg, one-sided p) |
|---|---|---|
| homograph-taxonomic | **6** | Georgia +0.80, Jordan +0.65, United States +0.21 (k-track & diagnostic; p≈1e-4) |
| numeric | **10** | date +0.68, ordinal +0.53, decimal +0.45, year +0.35, comma_number +0.24, currency +0.14 |
| spelling | **14** | T: that/their/there/then/those/three/through +1.0; O: our +1.0, one +0.96; L: like +1.0, law +0.78 |

Honest negatives (9, verbatim in `honest_negatives`): numeric **integer** ties random (+0.007); first-letter
**O/on,out,over,own** and **T/this,think,time** tie random (sparse / no localizing absorber). Letter **I**
anchor (1227) fires 0 % on corpus → flagged **spurious**, repair N/A.

**M1a(k):** for every concept the JTT reweighted hyperplane's decoder-projection argmax is NOT a KG
absorber (`kg_absorber_is_argmax=False` everywhere); on taxonomic/L/O/T/D the argmax is the **parent
anchor** (rank 1). (k) classifies holes but exposes no addable per-sub-context feature.

**M7 ensemble member-labeling (J=3, shuffled order):** 89 members, **agreement 0.730 vs shuffle null
0.096, gap 0.634, bootstrap CI [0.545, 0.724] excludes 0**, 0 parse-fails. Per-role: absorbers **0.756**,
anchors 0.43 (anchors over-specified — honest caveat). 15-wide confident-label fraction per first-letter
pool: **L 0.87 / O 0.80 / T 0.93 / I 0.87 / D 0.67** (confident-and-correct ≈ 0.60–0.73). LLM spend
**$0.194** (target <$1, hard stop $10).

Verdict: `kg_utility_measured=True`, `n_survive_FDR05=30`, `member_labeling_above_null=True`,
`fifteen_wide_confident_fraction_reported=True`.

## Files
- `method.py` — full pipeline.
- `method_out.json` / `full_/mini_/preview_method_out.json` — results.
- `pyproject.toml` — pinned deps. `logs/` — run logs. `cache/` — encodings (repo-excluded).
