# M1″ — Footprint-Matched **Gated-Dense Control** + Honest Forget-Operating-Point Test

The decisive iter-7 control for the auditability-first two-track **Counterfactual Co-Response Grouping
(CCRG)** units. iter-5/iter-6 reported that ablating ONE **KG-named absorber latent** (**KG-ABL**) beats a
dense baseline at matched forget-quality — iter-6 against a **sub-context-labeled** diff-of-means `u_sub`
(`DENSE-SUB-ABL`). A reviewer can still object that the comparison is **unfair on token footprint**:
KG-ABL edits only the ~1–3 % of tokens where its sparse feature fires, while the *ungated* dense `u_sub`
edits **every** token. iter-7 closes that gap with the **fair, footprint-matched** control.

```
DENSE-SUB-ABL-GATED :  h ← h − β·(h·u_sub)·u_sub   applied ONLY where |h·u_sub| > τ
```

`τ` is **calibrated** so the gate's *global* firing fraction over a broad neutral pool equals the KG
absorber's own token footprint `f_kg`. Because `u_sub` points toward the target sub-context, the gate still
fires **densely on FORGET (X) tokens** and **sparsely elsewhere** — exactly "gate any edit by sparse
firing", now matched to the SAE feature's footprint. The decisive pair is **KG-ABL vs DENSE-SUB-ABL-GATED**.

## Operators (all compared in one pipeline, at the SAME swept matched forget)

| Operator | Edit | Role |
|---|---|---|
| **NOOP** | none | baseline continuation |
| **KG-ABL** (ours) | `h ← h − λ·z_l·W_dec[l]` — ablate the KG-named absorber, gated by its own sparse firing | the method |
| **DENSE-SUB-ABL-GATED** (decisive control) | `u_sub` erased **only at gated tokens**, footprint-matched to `f_kg` | fair labeled+sparse baseline |
| **DENSE-SUB-ABL** (secondary) | `h ← h − β·(h·u_sub)·u_sub` — **ungated** labeled erasure (iter-6 decisive) | strong, labeled, every-token |
| **DENSE-WHOLE-ABL** (secondary) | `h ← h − β·(h·u)·u` — whole-parent erasure | the iter-5 comparator |
| **RAND** | firing-rate-matched random latent | sanity (≈ no effect) |
| **KG-ABL-UNIT** (M7) | ablate ALL K-track unit members jointly | grouping-vs-single control |

**Forget-matching.** Sweep `λ∈{0..4}` / `β∈{0..8}`; `forget(op,s)` = mean next-token KL on held-out FORGET
windows at the target token. Decisive `matched_target = 0.8·min(maxKG, maxGATED)` (the KG–GATED pair). All
operators are scaled to reach the **same** `matched_target`, so the comparison holds forget constant and
reads off **collateral / joint utility**.

## The honest operating-point disclosure (the core of iter-7)

The matched point is **pinned at KG's tiny single-latent next-token-KL ceiling**. We report ALL of it:

- `max_forget_{kg,sub,gated,whole}` and the ratios — KG's ceiling is **17–320× smaller** than the dense
  directions' (e.g. Georgia `max_kg≈0.067` vs `max_sub≈6.6`, `max_gated≈1.5`, `max_whole≈13`).
- **NOOP-identical fraction** per operator/role — at the matched point KG-ABL is **near-NOOP on most
  prompts**, which is *why* its judged retain-utility ≈ NOOP.
- Full **collateral-vs-forget curves** for all four operators, so the KG-pinned point is shown in the
  context of the dense directions' far larger achievable range, plus a **gate footprint sweep**
  (`{0.5,1,2,4}·f_kg`) trade-off.

Because a near-NOOP edit trivially "preserves" everything, we **prove meaningful forgetting separately**
(all $0, deterministic), at each operator's **own** forget ceiling:

1. **Completion-accuracy drop** — log-prob of the gold continuation token on hand-built target-sense probes
   (`"The capital of Georgia is" → Tbilisi`, `"large starts with the letter" → L`, …): `drop = logp_NOOP −
   logp_op`, with a bootstrap CI over probes.
2. **Frozen sub-probe positive-rate drop** — a 1-D-free logistic probe `d_sub` (X-positive vs sibling on a
   disjoint fold, AUC≈1.0) is scored on the **real post-edit residual** (captured under the edit hook); the
   drop = how much the edit makes a held-out X context stop reading as X.
3. **Judged edit-vs-NOOP forget delta** + the NOOP-identical fraction.

`meaningful_forget[op] = (completion_drop CI>0) OR (sub-probe drop ≥ 0.1)`.

## Per-case 3-way fork (decided on KG vs GATED, at meaningful forget)

- **`KG_BEATS_GATED_DENSE_AT_MEANINGFUL_FORGET`** — both KG and the footprint-matched gated dense reach
  real forgetting AND the KG-vs-GATED joint CI excludes 0 favoring KG under **both** judges. A *discovered*
  single SAE feature beats a *labeled + footprint-matched* dense control.
- **`GATED_DENSE_CLOSES_GAP_DISCOVERY_IS_THE_VALUE`** — the footprint-matched gated dense **matches** KG on
  the joint (CI includes 0). The SAE adds no edit-quality magic beyond the labeled direction; the value of
  the two-track method is the **label-free WHERE-to-gate discovery**.
- **`NO_MEANINGFUL_FORGET_SCOPE_TO_PARTIAL_SUPPRESSION`** — the single-latent ablation **cannot induce real
  forgetting even at full strength** (completion-drop CI incl 0 AND sub-probe drop < 0.1). The KG handle is
  clean, low-collateral **partial suppression**, not unlearning.

**Aggregate gates.** `adv_KG_vs_GATED` (signed joint diff) is averaged over the powered absorption cases vs
the co-firing cases; `absorption_exceeds_cofiring` requires the absorption advantage to **exceed** the
co-firing one (else the "win" is edit footprint, not structure). A **US-excluded** re-aggregation drops the
co-firing cases from the headline. The overall verdict is one of
`SPARSE_SAE_HANDLE_ESTABLISHED` / `DISCOVERY_IS_THE_VALUE_GATING_NOT_SAE_SPECIFIC` /
`SELECTIVE_LOW_COLLATERAL_PARTIAL_SUPPRESSION`.

## Cases

| case | X | absorber `l` | regime | role |
|---|---|---|---|---|
| `taxonomic_georgia` | Georgia | 16009 | absorption | PRIMARY (+M7) |
| `first_letter_large` | large | 8463 | absorption | secondary (+M7) |
| `taxonomic_jordan` | Jordan | 540 | absorption | **descriptive** (`u_sub` underpowered → excluded from the gate) |
| `taxonomic_us` | United States | 846 | co-firing | M5 router false-negative control |
| `toxicity_insult` | insult | auto | co-firing | declared negative pole |

> **Month case dropped.** The iter-5 homograph month dataset's `*_data_out.json` artifacts were **not
> materialized on disk** (only `schema.json` + builders remain), so the planned 4th absorption case could
> not be built. The absorption set is `{Georgia, large, Jordan-descriptive}` — consistent with the breadth
> count being structural-only; month was supporting, never load-bearing.

## Reuse / config

`core.py` is the iter-4/5/6 engine; iter-7 adds the `erase_dir_gated` operator (with `τ` threaded through
`make_edit_hook`/`forward_pos_logprobs`/`behavioral_curve`/`side_effects`). `method.py` adds
`calibrate_gate_tau`, the gated arm + footprint sweep, the meaningful-forget proof
(`completion_drop` / `fit_sub_probe` + `read_resid_under_edit`), and the 3-way fork.

- SAE: `google/gemma-scope-2b-pt-res`, `layer_12/width_16k/average_l0_82` (JumpReLU, d_model 2304).
- Model: `google/gemma-2-2b` (bf16, eager); edit + read at `blocks.12.hook_resid_post` (gating cosine
  **0.919**, L0≈88). Single GPU (NVIDIA L4, 23 GB). `$0` model-internal; LLM judges **target <$3, hard cap
  $10**. Two judges: `anthropic/claude-haiku-4.5` (primary) + `openai/gpt-4o-mini` (second).

## Run

```bash
uv run method.py --smoke                                                # gating + gated op + completion + sub-probe + 2 judges
uv run method.py --cases taxonomic_georgia --cap 30 --gen_per_set 6     # mini (< $0.10)
uv run method.py                                                        # full (5 cases, both judges)
```

## Outputs

- `method_out.json` — `metadata` (gating; judge spend; per-case operating points incl. `matched_target`,
  `matched_target_iter6`, `op_high`, `max_forget_*`, gate `τ` sweep + footprint used; NOOP-identical
  fractions; `collateral_diff_CI_KG_vs_GATED` [DECISIVE] + KG-vs-SUB/WHOLE secondary + gated-vs-ungated;
  full-range collateral curves + footprint trade-off; `joint_diff_CI_KG_vs_GATED` under both judges +
  model-internal joint; completion/sub-probe meaningful-forget; `fork_verdict`; M5/M6/M7; `summary` with
  `adv_absorption`/`adv_cofiring`/`absorption_exceeds_cofiring`/`us_excluded_gate`/`overall_verdict`;
  `honest_negatives`) + `datasets`: **`gated_dense_per_prompt`** (one row per (case,role,prompt) with
  `predict_kg_abl`/`predict_dense_sub_gated`/`predict_dense_sub_abl`/`predict_dense_whole_abl`/`predict_noop`
  continuations + per-op judged utilities + NOOP-identical + model-internal signals) and
  **`kg_vs_gated_per_case`** (one row per case with the fork verdict + all decisive CIs + operating points +
  completion/sub-probe drops). `full_/mini_/preview_method_out.json` are the size-reduced variants.
- `logs/` run logs; `results/` smoke + mini diagnostic runs; `cache/` excluded from upload.

## Headline result (full run: 5 cases, 2 judges, 2109 calls, **$0.80** / target $3)

**Overall verdict: `SPARSE_SAE_HANDLE_ESTABLISHED` — but feature-dependent, and the iter-6 framing is
sharpened.** The footprint-matched control turns the result into a clean, honest, regime-split finding.

| case | absorber | fork | KG can forget? | adv KG−GATED (joint, both judges) | max_forget KG vs GATED |
|---|---|---|---|---|---|
| `first_letter_large` (spelling) | 8463 | **KG_BEATS_GATED_DENSE** | **yes** (sub-probe drop 0.42, compl. 0.11) | **+1.58** (CI excl 0) | 0.45 vs 0.97 |
| `taxonomic_georgia` (country) | 16009 | NO_MEANINGFUL_FORGET | **no** (sub-probe 0.07, compl. 0.06) | +0.17 (vacuous — KG near-NOOP) | 0.065 vs 1.92 |
| `taxonomic_jordan` (country) | 540 | NO_MEANINGFUL_FORGET | **no** (sub-probe 0.0) | +0.15 (vacuous) | 0.11 vs 3.18 |
| `taxonomic_us` (co-firing) | 846 | NO_MEANINGFUL_FORGET | no | +0.27 | 0.035 vs 2.40 |
| `toxicity_insult` (co-firing) | 13367 | KG_BEATS_GATED_DENSE | yes (sub-probe 0.42) | +0.47 (co-firing → NOT in abs gate) | 0.055 vs 1.21 |

**What it means.**
1. **The single SAE absorber genuinely beats the fair, footprint-matched gated-dense control — but only
   where the feature is CONCENTRATED.** For the spelling absorber `large`, KG-ABL meaningfully forgets
   (frozen sub-probe positive-rate drops 0.42; gold-completion log-prob drops 0.11) AND wins the joint by
   **+1.58** under *both* judges, with strictly lower collateral (Δ +0.29, CI excl 0) and 1.0 curve
   dominance. `toxicity/insult` (a co-firing case whose latent happens to concentrate) also forks KG_BEATS
   (+0.47) — reported, but **excluded from the absorption gate** because it is co-firing.
2. **For DISTRIBUTED senses the single-latent handle is clean but PARTIAL — it cannot induce meaningful
   forgetting even at full ablation.** Georgia (16009) and Jordan (540) fork
   `NO_MEANINGFUL_FORGET_SCOPE_TO_PARTIAL_SUPPRESSION`: at full strength the absorber's next-token-KL ceiling
   is tiny (`max_kg` 0.065 / 0.114, **17–30× smaller** than the dense directions), the frozen sub-probe is
   barely moved (drop 0.07 / 0.0), and the gold completion barely shifts (0.06). This **directly exposes**
   that the iter-6 `KG_BEATS_USUB` headline sat at a **near-NOOP operating point** (KG is NOOP-identical on
   **89 %** of FORGET prompts for Georgia/Jordan) — KG "won" because it barely edited, but it also barely
   forgot. The footprint-matched control + meaningful-forget proof make this honest.
3. **The advantage on the meaningful-forget absorption case (+1.58) EXCEEDS the co-firing advantage
   (+0.37)** → `absorption_exceeds_cofiring = True`; the win is structure, not edit footprint. The
   **US-excluded** headline gate (powered absorption only) = 3 cases, **1 KG_BEATS** (`large`), 2
   NO_MEANINGFUL, gate passed.

Two LLM judges (`claude-haiku-4.5` + `gpt-4o-mini`); deterministic `$0` meaningful-forget proof
(completion-accuracy + frozen sub-probe) carries the verdict regardless of judges. See
`metadata.summary`, `metadata.per_case`, and the 11 `metadata.honest_negatives` in `method_out.json`.
