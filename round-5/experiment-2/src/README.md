# M2 — Cross-Dictionary Replication of the Auditability Spine on a Second Gemma-Scope SAE

**Artifact:** `gen_plan_experiment_2_idx2` (GPU). Re-runs the iter-4 *auditability spine* on a **second SAE
dictionary of the same frozen model** (`google/gemma-2-2b`), to test whether the iter-4 width-16k / layer-12
findings are a property of the model+method or an artifact of one particular SAE dictionary.

* **PRIMARY dictionary** — width-**65k** canonical at **layer 12** (`google/gemma-scope-2b-pt-res`,
  `layer_12/width_65k/average_l0_72`; canonical = avg-L0 closest to 100, resolved to 72 from
  `{21,38,72,141,297}`, verified at load time).
* **SECONDARY (reduced) dictionary** — an earlier residual layer (**layer 9**, width-16k), the most
  diagnostic taxonomic subset only, as a second axis (layer) of the same generalization claim.

The single most important difference vs iter-4: **latent indices are dictionary-specific**, so the anchor
AND the per-sub-context absorbers are **RE-DERIVED on each dictionary** — the 16k ids (Georgia→16009,
Jordan→540/8347) do NOT carry over. Anchor re-derivation = highest content-flip-coverage content-responsive
latent with sub-context precision ≥ 0.70, validated by an unsupervised corpus firing-floor ≥ 0.01 (the
iter-4 letter-I-1227 spurious-anchor fix). Absorbers re-derived per sub-context by the K-track greedy
(low firing-Jaccard, high precision) and, independently, by a form-free probe-projection (Chanin A.13 /
SAEBench `absorption_fraction`) diagnostic.

## The four replicated spine pieces (all model-internal, $0 LLM for the core)

| piece | what it measures | 16k (iter-4) reference |
|---|---|---|
| **(A) homograph recall-holes** | per-country parent recall-hole `1−recall` + positive-only firing-Jaccard(anchor,detector); does Georgia/Jordan still show `recall_hole>0.5 & jaccard<0.1`? | Georgia hole 0.77 jac 0.012; Jordan hole 0.68 jac 0.014 |
| **(B) KG-repair FDR** | broad K-track names a covering absorber per eligible sub-context; recall recovery vs a random-**single-latent** control, paired-bootstrap one-sided p, Benjamini-Hochberg FDR≤0.05 over ALL concepts; honest deltas vs the 16k survivor counts | survivors: spelling **14**, homograph-taxonomic **6**, numeric **10** (30 / 69 tested) |
| **(C) surgical edit** | KG-ABL single re-derived absorber vs DENSE diff-of-means parent erasure (baseline f) vs RAND; next-token-KL on_target/collateral at matched effect, paired-bootstrap CIs; selectivity ratio | Georgia ratio 1722×, KG-col 2.9e-5 vs DENSE 0.0496 |
| **(D) router transfer** | recompute recall-hole-max + firing-Jaccard-median per concept; apply **frozen 16k thresholds** (`τ_h=0.7774` recall-hole lead, `τ_j=0.05` corroborating) WITHOUT refit AND re-derive 65k-optimal; balanced-accuracy + does it transfer | recall-hole-alone bal-acc 1.0; firing-Jaccard 0.917 |

A per-dictionary **REPLICATES / PARTIAL / DICTIONARY-DEPENDENT** verdict per piece, plus an overall
`{full|partial|dictionary_dependent}` verdict. A clean non-replication is itself the publishable
*wider-SAE-absorbs-more* dictionary-dependence finding the literature predicts.

## Reuse

The spine is copied + parametrized over the SAE (release/width/layer) from:
* iter-4 `experiment_1` — broad K-track KG repair loop, random-addition control + one-sided bootstrap p,
  BH FDR (hand-rolled + statsmodels crosscheck), `k_localization_check` (JTT), ensemble member-labeling.
* iter-4 `experiment_2` — edit operators (KG-ABL / DENSE-ABL / RAND / KG-ADD), `run_case`,
  `forward_pos_logprobs` / `behavioral_curve`, next-token-KL on_target/collateral, paired bootstrap CIs.
* iter-3 `experiment_4` — `firing_jaccard`, per-sub-context recall-hole, `derive_1d` router.

## How to run

```bash
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python torch==2.6.0 --index-url https://download.pytorch.org/whl/cu124
uv pip install --python .venv/bin/python <pins in pyproject.toml>
HF_TOKEN=$HF_TOKEN .venv/bin/python method.py --smoke --dicts 65k                       # load + gating only
HF_TOKEN=$HF_TOKEN .venv/bin/python method.py --dicts 65k --families taxonomic --cap 40 # mini pilot
HF_HUB_OFFLINE=1 HF_TOKEN=$HF_TOKEN .venv/bin/python method.py --dicts 65k              # full 65k spine ($0 LLM)
HF_HUB_OFFLINE=1 HF_TOKEN=$HF_TOKEN .venv/bin/python method.py --dicts 65k,l9_16k       # + reduced secondary layer
HF_HUB_OFFLINE=1 HF_TOKEN=$HF_TOKEN .venv/bin/python method.py --dicts 65k --member_labeling  # + optional M7 (LLM)
```

Encodings are disk-cached per `(dictionary, sae_id, split)` under `cache/` (excluded from the repo).

## Gating (65k, verified)

cosine **0.9280** (> 0.9; +0.009 vs 16k 0.9189), L0 70.8, `hidden_states[13]` (FVU 0.170 vs 0.278/0.334
for 12/14), spelling cosine 0.9353, **numeric digit-token cosine 0.8762 (descriptive, < 0.9 — NOT a
gate-fail**, matches the iter-4 16k numeric ~0.8911 observation). The gate is the global taxonomic-token
SAE→layer reconstruction; numeric/spelling are recorded descriptively.

## Output (`method_out.json`, `exp_gen_sol_out`-schema-valid)

`metadata` — per-dictionary `gating`, re-derived anchors (with firing-floor validation), a
`replication_tables[dict]` block with one entry per spine piece (`homograph_holes`, `repair_fdr` with
per-family survivors + deltas-vs-16k + distinct-hole count, `surgical` per-case selectivity/CI/footprint,
`router` frozen-vs-refit balanced-accuracy), `regime_split`, `per_piece_verdicts`, `overall_verdict`;
`router_transfer`; `multiplicity` (BH); and a top-level `verdict.cross_dictionary_replicates`.
`datasets` — `cross_dictionary_replication` (one row per dictionary×piece×sub-context, output = verdict /
numeric prediction), `kg_repair_loop`, `edit_locality_per_context`, and optional `member_labeling`.

`full_/mini_/preview_method_out.json` are size-reduced variants. `logs/` run logs.

## Results (full run, seed 1234, `method_out.json`)

**Cross-dictionary verdict: `full`** (primary 65k). Re-derived anchors differ from the 16k ids exactly as
expected: taxonomic 65k anchor = **31478** (16k was 3792), layer-9/16k anchor = **3443**; all
firing-floor-validated.

### PRIMARY — width-65k, layer-12 → overall `full` (all four pieces REPLICATE)

* **(A) homograph holes — REPLICATES.** Georgia recall-hole **0.873**, firing-Jaccard **0.0038**; Jordan
  recall-hole **0.746**, firing-Jaccard **0.097** — both clear `hole>0.5 & jaccard<0.1`. (United States is
  an even larger hole: the 65k parent never fires on "United States", recall-hole 1.0.)
* **(B) KG-repair FDR — REPLICATES (and stronger).** 55 of 154 tested repairs survive BH FDR≤0.05
  (statsmodels-confirmed), per family **spelling 29 / homograph-taxonomic 11 / numeric 15** — *more* than
  the 16k counts (14 / 6 / 10), i.e. **Δ = +15 / +5 / +5**, the predicted *wider-SAE-absorbs-more* signal.
  52 distinct holes.
* **(C) surgical edit — REPLICATES.** Georgia single-absorber (46143) ablation is **SURGICAL_EDIT_CONFIRMED**,
  selectivity ratio **3.7M×** (KG collateral 0.0 vs DENSE 0.037, off-target footprint 1e-4); United States
  (29902) confirmed at 1518×; first-letter `layer` (8234) 1000× and `did` (41077) 353× confirmed. Honest
  nulls: the re-derived **Jordan** absorber fires (jaccard 8e-4) but its ablation has *no measurable
  on-target effect* (NO_ON_TARGET_EFFECT), and first-letter `on`/`take` likewise — a re-derived absorber is
  not guaranteed to be behaviorally load-bearing on the new dictionary.
* **(D) router transfer — REPLICATES.** The **frozen 16k** recall-hole threshold (τ_h=0.7774) gives
  balanced-accuracy **1.0** on the 65k concept set (firing-Jaccard corroborating 0.929); the thresholds
  transfer without refit.
* **Regime split (confirms the router on the new dictionary):** absorption (n=8) mean selectivity
  **466 997×**, firing-Jaccard 0.0071; co-firing toxicity-insult (n=1, the negative pole) selectivity
  **1.99×**, firing-Jaccard 0.837 — a ~235 000× clean split, exactly as the firing-Jaccard / recall-hole
  router predicts.

### SECONDARY (reduced) — width-16k, layer-9 → overall `partial`

A second axis (layer) of the same claim. **Absorption is layer-specific**: the layer-9 country parent
(3443) is *cleaner* (corpus firing-rate 0.987) so **Georgia loses its hole** (recall-hole 0.003 →
`homograph_holes` PARTIAL), but **Jordan keeps its hole** (0.536) and its single-absorber (14745) ablation
is **SURGICAL_EDIT_CONFIRMED** (2376×); United States also confirmed (427×). `repair_fdr` REPLICATES
(taxonomic family, 2 survivors); the multi-concept `router` transfer is `NOT_RUN_REDUCED` (the reduced
taxonomic-only run lacks the co-firing concepts needed to test it). Gating cosine 0.9301, `hidden_states[10]`.

**Headline:** the iter-4 auditability spine **fully replicates on a 4× wider SAE of the same layer**
(holes reappear, repairs survive — and *more* of them, surgical Georgia edit is even sharper, router
thresholds transfer), and **partially replicates across a different layer** where the absorption hole
structure is genuinely layer-dependent — a precise, publishable characterization of when SAE-feature
absorption (and the KG-repair / surgical-edit story built on it) is dictionary-dependent.
