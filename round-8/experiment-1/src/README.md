# M1‴ — De-Inflated, **Genuinely-Fair-Gated**, Concentration-Attributed, Unified-Operator Unlearning-Edit Test

The iter-8 decisive control for the auditability-first two-track **Counterfactual Co-Response Grouping
(CCRG)** units. iter-5/6/7 reported that ablating ONE **KG-named absorber latent** (**KG-ABL**) beats a
dense baseline at matched forget-quality. iter-7 added a **footprint-magnitude-gated** dense control
(`DENSE-SUB-ABL-GATED`) and reported a **+1.58** KG win on the spelling absorber `large`. A reviewer can
still object that the iter-7 control is **not a fair WHERE-to-edit gate**: at the matched forget it
**over-erases** (β≈3, ~14× its own ungated collateral), which **inflates** KG's apparent edge. iter-8
replaces the decisive control with a **genuinely-fair** one and **de-inflates** the headline.

```
DENSE-SUB-ABL-GATED-FAIR :  h ← h − β·(h·u_sub)·u_sub   applied ONLY where (h·w_dsub + b_dsub) > 0,
                            β ∈ {0, 0.25, 0.5, 0.75, 1.0}   (BOUNDED ≤ 1 — NO over-erasure)
```

`d_sub = logistic(target-sub-positive vs sibling-positive)` is fit on the **DIAGNOSTIC** fold (never on SAE
latents → non-circular), threshold 0 (prob 0.5). It is **ONE unified gate definition for every case**
(resolves the iter-7 "the gate is a magnitude threshold / β≈3 over-erasure" critique). Its **balanced
accuracy on the disjoint eval fold** is reported per case.

## Operators (all compared in one pipeline, at the SAME swept matched forget)

| Operator | Edit | Role |
|---|---|---|
| **NOOP** | none | baseline |
| **KG-ABL** (ours) | `h ← h − λ·z_l·W_dec[l]` — ablate the KG-named absorber, gated by its own sparse firing | the method |
| **DENSE-SUB-ABL** (LEAD comparator) | `h ← h − β·(h·u_sub)·u_sub` — **ungated** labeled erasure (every token) | strongest dense; headline pair |
| **DENSE-SUB-ABL-GATED-FAIR** (ESTABLISHING control) | `u_sub` erased **only where a precise d_sub fires**, β ≤ 1 | the genuinely-fair gate |
| **DENSE-SUB-ABL-GATED** (CAVEATED robustness) | `u_sub` erased at magnitude-gated tokens, footprint-matched | the iter-7 (over-erasing) control |
| **MAX-PRECISION** (M3‴ ablation) | ablate the single **most sub-context-precise** latent (no set-cover) | does discovery add anything? |
| **DENSE-WHOLE-ABL** (secondary) | `h ← h − β·(h·u)·u` — whole-parent erasure | iter-5 comparator |
| **RAND** | firing-rate-matched random latent | sanity (≈ no effect) |
| **KG-ABL-UNIT** (M7) | ablate ALL K-track unit members jointly | grouping-vs-single control |

**Forget-matching.** Sweep `λ∈{0..4}` / `β∈{0..8}` (`β_fair∈{0..1}`); `forget(op,s)` = mean next-token KL on
held-out FORGET windows at the target token. The **LEAD** point is `0.8·min(max_kg, max_sub)` (KG vs the
strongest **ungated** dense); the **canonical / ESTABLISHING** point is `0.8·min(max_kg, max_sub, max_fair)`
so the **bounded-β fair gate can also reach it** (if it cannot at β=1, KG is matched **down** to the fair
op's own max — a fair, not handicapped, comparison; never driven past β=1). The legacy footprint-gated arm
is matched at `0.8·min(max_kg, max_gated)`.

## The M4‴ hardened meaningful-forget proof (BOTH instruments + a behavioral match)

Because a near-NOOP edit trivially "preserves" everything, meaningful forgetting is proven separately ($0,
deterministic), at each operator's **own** ceiling, with **both instruments side-by-side**:

1. **Completion-accuracy drop** — log-prob of the gold continuation token over **20–50 templated
   target-sense probes** per case (`"large starts with the letter" → L`, `"Amazon was founded by Jeff" →
   Bezos`, `"Tim Cook is the CEO of" → Apple`, …), bootstrap CI over probes.
2. **Frozen sub-probe positive-rate drop** — a 1-D-free logistic `d_sub` (AUC≈1.0) scored on the **real
   post-edit residual**; the drop = how much a held-out X context stops reading as X.
3. **BEHAVIORAL forget-match** (the fix) — match all ops on the **sub-probe drop** (not next-token-KL), then
   re-compare collateral and completion-accuracy there. Catches "next-token-KL matching ≠ behavioral
   forgetting" (the iter-7 instrument disagreement).

`meaningful_forget[op] = (completion_drop CI>0) OR (sub-probe drop ≥ 0.1)`.

## Per-case 3-way fork (decided on KG vs BOTH dense controls, at meaningful forget)

- **`KG_BEATS_STRONGEST_AND_FAIR_GATED`** — KG beats the strongest **ungated** dense (DENSE-SUB-ABL) **AND**
  the **genuinely-fair** gated dense (DENSE-SUB-ABL-GATED-FAIR) on the joint CI under **both** judges. A
  discovered single SAE feature beats a labeled + fairly-gated dense control.
- **`FAIR_GATED_CLOSES_GAP_DISCOVERY_IS_THE_VALUE`** — the fair gated control **matches/beats** KG (joint CI
  includes 0). The SAE adds no edit-quality magic beyond the labeled direction; the value of the two-track
  method is the **label-free WHERE-to-gate discovery** (the sparse concentrated absorber recovers the gating
  footprint **without** the sub-context labels `u_sub` needs).
- **`NO_MEANINGFUL_FORGET_SCOPE_TO_PARTIAL_SUPPRESSION`** — the single-latent ablation cannot induce real
  forgetting even at full strength → clean, low-collateral **partial suppression**, not unlearning.

## M3‴ concentration-vs-absorption attribution + max-precision ablation

Each case is classified by **regime** (absorption / co-firing) × **concentration** (concentrated /
distributed). The win predictor is the **lexical CONCENTRATION / sub-context PRECISION** of the target
sense, **not** the absorption diagnostic: a concentrated *co-firing* latent (insult) can win while
*distributed* absorbers (Georgia/Jordan country senses) do **not** meaningfully forget. The **MAX-PRECISION**
operator ablates the single most-precise latent; where it **is** the set-cover-discovered absorber, the
set-cover/(1−1/e) machinery is **inert** for the edit win (method identity = label-free
precise-concentrated-latent discovery).

## Cases (gradual scaling order: 4 CONCENTRATED load-bearing first, then references)

| case | X | absorber `l` | parent | regime | concentration |
|---|---|---|---|---|---|
| `first_letter_large` | large | 8463 | 205 | absorption | concentrated (+M7) |
| `named_entity_amazon` | Amazon | 6846 | 2768 | absorption | concentrated (+M7) |
| `named_entity_bush` | Bush | 1418 | 2768 | absorption | concentrated |
| `named_entity_cook` | Cook | 15631 | 2768 | absorption | concentrated |
| `taxonomic_georgia` | Georgia | 16009 | 3792 | absorption | distributed (reference) |
| `taxonomic_jordan` | Jordan | 540 | 3792 | absorption | distributed (reference, u_sub descriptive) |
| `taxonomic_us` | United States | 846 | 3792 | co-firing | distributed (M5 router false-neg) |
| `toxicity_insult` | insult | auto (~13367) | auto | co-firing | concentrated (declared negative pole) |

The four concentrated absorbers were **discovered** in iter-7 exp2 (`screen.py`): named-entity parent
`2768`; Amazon `6846` (recall-hole .61, jaccard .048, precision .99), Bush `1418` (.79 / .021 / 1.00), Cook
`15631` (.72 / .045 / 1.00). Each is **re-validated at runtime** (K-track-lite: precision ≥ 0.7,
firing-Jaccard < 0.1, fires on ≥ 5 diagnostic X rows); the re-derived id replaces the hardcode on a mismatch.

## Reuse / config

`core.py` is the iter-4/5/6/7 engine; iter-8 adds the `erase_dir_dsub_gated` operator (with `w_dsub`,
`b_dsub` threaded through `make_edit_hook`/`forward_pos_logprobs`/`behavioral_curve`/`side_effects`).
`method.py` adds `fit_dsub_gate`, `max_precision_latent`, `setup_named_entity`, the FAIR + MAX-PRECISION
arms, the expanded completion probes, the behavioral forget-match, and the new 3-way fork.

- SAE: `google/gemma-scope-2b-pt-res`, `layer_12/width_16k/average_l0_82` (JumpReLU, d_model 2304).
- Model: `google/gemma-2-2b` (bf16, eager); edit + read at `blocks.12.hook_resid_post` (gating cosine
  **0.919**). Single GPU (NVIDIA L4, 23 GB). `$0` model-internal; LLM judges **target <$3, hard cap $10**.
  Two judges: `anthropic/claude-haiku-4.5` (primary) + `openai/gpt-4o-mini` (second).

## Run

```bash
uv run method.py --smoke                                                  # gating + fair op + d_sub balacc + NE locality + 2 judges
uv run method.py --cases first_letter_large --cap 30 --gen_per_set 4      # mini (< $0.10)
uv run method.py --gen_per_set 10                                         # full (8 cases, both judges)
uv run make_variants.py method_out.json                                  # full/mini/preview variants
```

## Outputs

- `method_out.json` — `metadata` (gating; judge spend; per-case operating points incl. `matched_target_LEAD`
  / `_FAIR` / `_FOOT`, all `max_forget_*` incl. `max_forget_fair`; `fair_gate_dsub` + `fair_gate_balacc_eval`;
  full collateral-vs-forget curves for all 6 ops; KG-vs-{SUB **LEAD**, FAIR **ESTABLISHING**, GATEDFOOT
  **caveated**, WHOLE, MAXPREC} joint + collateral CIs both judges + curve-dominance; `maxprec_verdict` +
  `maxprec_same_as_setcover`; 20–50-probe completion drop AND sub-probe drop side-by-side + `behavioral_match`;
  `fork_verdict`; M7; `summary` with the de-inflated headline, the `concentration_attribution` table,
  `maxprec_ablation`, `n_concentrated_wins`, `overall_verdict`; `honest_negatives`) + `datasets`:
  **`edit_per_prompt`** (one row per (case,role,prompt) with `predict_kg_abl` / `predict_dense_sub_abl` /
  `predict_dense_sub_gated_fair` / `predict_dense_sub_footprint_gated` / `predict_max_precision` /
  `predict_dense_whole_abl` / `predict_noop` continuations + per-op judged utilities + model-internal signals)
  and **`kg_vs_controls_per_case`** (one row per case with the fork verdict + all decisive CIs).
  `full_/mini_/preview_method_out.json` are the validated size-reduced variants.
- `logs/` run logs; `results/` smoke + mini diagnostic runs; `cache/` excluded from upload.

## Headline result (full run: 8 cases, 2 judges, 2709 calls, **$1.07** / target $3)

**Overall verdict: `DISCOVERY_IS_THE_VALUE_FAIR_GATE_CLOSES_GAP`.** On **every** case where KG meaningfully
forgets, the genuinely-fair `d_sub`-gated dense control **matches or beats** the single SAE absorber on the
joint — the iter-7 "KG beats the gated dense" headline was **inflated by the over-erasing footprint gate**.

`adv` = signed paired-bootstrap joint diff (>0 favors KG). **SUB** = vs the strongest **ungated** dense
(LEAD); **FOOT** = vs the iter-7 **footprint-gated** dense (the inflated number); **FAIR** = vs the
**genuinely-fair** `d_sub`-gated dense, β≤1 (ESTABLISHING). `max_kg` = KG's single-latent forget ceiling.

| case | absorber | conc. | `max_kg` | KG-forgets? | adv SUB (lead) | adv **FOOT** (iter-7) | adv **FAIR** (fair) | fork |
|---|---|---|---|---|---|---|---|---|
| `first_letter_large` | 8463 | conc | 0.45 | **yes** | **+0.98** | +1.38 | **−0.05** | FAIR_CLOSES |
| `named_entity_amazon` | 6846 | conc | 1.14 | **yes** | **+0.81** | +0.77 | **−0.05** | FAIR_CLOSES |
| `taxonomic_georgia` | 16009 | dist | 0.065 | **yes** | +0.38 | +0.52 | **−0.05** | FAIR_CLOSES |
| `toxicity_insult` | 13367 | conc | 0.047 | **yes** | +0.37 | +0.23 | +0.42 | FAIR_CLOSES |
| `named_entity_bush` | 1418 | conc | **0.040** | no | −0.10 | +0.08 | −0.39 | NO_MEANINGFUL |
| `named_entity_cook` | 15631 | conc | **0.032** | no | +0.17 | +0.17 | −0.02 | NO_MEANINGFUL |
| `taxonomic_jordan` | 540 | dist | 0.114 | no | +0.20 | +0.20 | −0.02 | NO_MEANINGFUL |
| `taxonomic_us` | 846 | dist | 0.035 | no | +0.30 | +0.37 | +0.25 | NO_MEANINGFUL |

**What it means.**
1. **De-inflation (the core result).** Across the 4 cases where KG meaningfully forgets, the iter-7-style
   **footprint-gated** advantage (FOOT **+0.23…+1.38**) **collapses** under the **genuinely-fair** gate
   (FAIR **−0.05…+0.42**). The footprint gate over-erases (β≈3): e.g. on `large` its retain collateral is
   **0.290** vs KG's **0.00005** and the fair gate's **6.8e-7**; on `amazon` **0.125** vs KG **9e-5** vs fair
   **6.6e-5**. The labeled dense direction, gated **precisely** with β≤1, is as clean as (or cleaner than)
   the single SAE absorber. **The SAE adds no edit-quality magic beyond the labeled direction** — its value
   is the **label-free WHERE-to-gate discovery** (the sparse concentrated absorber recovers the gating
   footprint without the sub-context labels `u_sub` needs). KG still beats the **ungated** dense (SUB
   +0.37…+0.98), but that is a **token-footprint** artifact (ungated edits every token).
2. **Firing-signature ≠ edit-handle (an honest, novel negative).** Two of the four discovered concentrated
   absorbers — `Bush` (1418) and `Cook` (15631) — have **clean absorption firing-signatures** (recall-hole
   .79/.72, firing-Jaccard .02/.05, precision ≈1.0 in iter-7) yet are **weak EDIT handles** (`max_kg` **0.04
   / 0.03**, 30× below the matched dense forget) and **cannot induce meaningful forgetting** even at full
   ablation. The absorption diagnostic does **not** predict edit strength.
3. **M3‴ set-cover vs max-precision.** Where the set-cover absorber **is** the max-precision latent (`large`,
   `Cook`, `US`) the set-cover/(1−1/e) machinery is **inert** for the edit. Where it differs (`Amazon`),
   set-cover finds a far **stronger forget handle** (`max_kg` **1.14** vs the max-precision latent's **0.035**,
   a 33× gap) — discovery's recall-hole objective beats pure precision for editing.
4. **Concentration, not absorption.** A concentrated **co-firing** latent (`insult`) meaningfully forgets and
   forks FAIR_CLOSES; distributed senses (`Jordan`, `US`) do not. The win predictor is lexical concentration /
   precision, not the absorption regime.

Two LLM judges (`claude-haiku-4.5` + `gpt-4o-mini`); the $0 model-internal joint + the $0 collateral/curve
analysis corroborate the verdict regardless of judges. See `metadata.summary`,
`metadata.summary.concentration_attribution`, `metadata.per_case`, and `metadata.honest_negatives`.
