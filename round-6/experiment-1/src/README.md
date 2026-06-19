# M1′ — KG-Localized Single-Absorber **Unlearning** vs a SUB-CONTEXT-Targeted Dense Baseline

The decisive downstream test for the auditability-first two-track **Counterfactual Co-Response Grouping
(CCRG)** units. iter-5 showed that ablating one **KG-named absorber latent** (**KG-ABL**) beats a
**whole-parent** dense erasure at matched forget-quality. A reviewer can object that erasing the
whole-parent diff-of-means ("erase *is-a-country* → remove every country") is a near-tautological
strawman. **M1′ replaces the decisive comparator** with a **sub-context-targeted dense direction**

```
u_sub = diff-of-means( target-sub-context-positive , sibling-positive in the SAME parent context )
```

built from the per-sub-context labels the testbeds already carry and **fit on a disjoint fold**. `u_sub`
is *itself a single hyperplane that localizes* — so it directly refutes the "a single dense direction
structurally cannot localize" framing. The decisive comparison is now **KG-ABL vs DENSE-SUB-ABL** at
matched forget-quality on the identical joint (retain-utility × fluency) LLM-judge outcome.

> **Per-case FORK verdict** (decided on KG vs SUB):
> - **`KG_BEATS_USUB`** — joint Δ CI excludes 0 favoring KG **AND** a 2nd-family judge CI also excludes 0
>   (a *discovered* single SAE feature beats a *sub-context-labeled* dense direction).
> - **`KG_MATCHES_USUB_LABEL_FREE`** — joint Δ CI includes 0 (KG matches `u_sub` **without** needing the
>   sub-context partition/labels that `u_sub` requires). Still a win for the method's practicality.
> - **`KG_LOSES_TO_USUB`** — joint Δ CI excludes 0 favoring SUB (a declared, clean negative).

## What is compared (at MATCHED forget-quality)

| Operator | Edit | Role |
|---|---|---|
| **KG-ABL** (ours) | `h ← h − λ·z_l·W_dec[l]` — ablate the KG-named absorber, **gated by its own sparse firing** | the method |
| **DENSE-SUB-ABL** (decisive baseline) | `h ← h − β·(h·u_sub)·u_sub` — erase the **sub-context** diff-of-means | strong, *labeled*, localizing |
| **DENSE-WHOLE-ABL** (secondary ref.) | `h ← h − β·(h·u)·u` — erase the **whole-parent** diff-of-means | the old comparator, now secondary |
| **RAND** | ablate a firing-rate-matched random latent | sanity (≈ no effect) |
| **KG-ABL-UNIT** (M7) | ablate ALL members of the K-track unit jointly | grouping-vs-single control |

**Forget-matching:** sweep `λ∈{0..4}` / `β∈{0..8}`; `forget(op,s)` = mean next-token KL on held-out FORGET
windows at the target token; `matched_target = 0.8·min(maxKG, maxSUB)` (the **decisive KG–SUB pair**);
pick `s_kg, s_sub, s_whl` reaching it. **Joint outcome:** for each held-out RETAIN+UNRELATED prompt,
generate a 40-token greedy continuation under each edit hook and score it with an AxBench-style OpenRouter
LLM judge (`anthropic/claude-haiku-4.5`, temp 0): `utility = harmonic_mean(fluency, content_pres) ∈ [0,2]`.
`joint_diff_CI_KG_vs_SUB = paired_bootstrap_diff(util_KG, util_SUB, B=10000)` is the **headline**.

## Folded-in modules

- **M1′ — `u_sub` localization validation.** At matched forget we report `collateral_SUB` vs
  `collateral_WHOLE`. Because the matched forget is pinned at KG's small single-latent KL ceiling (where
  *both* dense erasures barely act), the **robust** localization statement is **curve-based**: over the
  achievable dense forget range, the fraction of levels where `u_sub` has lower sibling collateral than
  the whole-parent. This **deletes** the false "structurally cannot localize" framing and shows the real
  mechanism — KG's surgical edge is **sparse-firing gating** (token footprint → 0), not the dense
  direction failing to localize.
- **M5 — United States reclassified as co-firing.** The specific absorber `846` has a tiny
  firing-Jaccard with the parent, but the *aggregate* parent-detector Jaccard and a low parent recall-hole
  put US in the **co-firing / router-false-negative** bucket. Both Jaccards are reported; US is moved out
  of the absorption win-set and **not** counted toward the M1′ gate.
- **M6 — second-family judge + human-proxy.** A stratified PRES subsample is re-judged by a different
  judge (`openai/gpt-4o-mini`, fallback `gemini-2.5-flash`/`gemini-2.0-flash-001`); we report Cohen κ and
  Pearson/Spearman utility correlation, and a `KG_BEATS_USUB` win is kept **only if the second-judge CI
  also excludes 0**. A deterministic `$0` human-proxy spot-check (curated sibling prompts) verifies KG-ABL
  preserves sibling tokens while DENSE-WHOLE corrupts them.
- **M7 — unit vs single absorber.** Ablating the full K-track unit (multi-member) is compared to the
  single discovered absorber at matched forget; the win **traces to the single absorber** (the extra unit
  members only add collateral), re-framing the two-track algorithm as the **label-free discovery
  procedure** that surfaces the precise single absorber.

## Cases / data (held-out eval fold disjoint from the u_sub-fit fold)

- **FORGET** = corpus windows with `sub_context == X` (suppress). **RETAIN** = sibling sub-contexts +
  parent-positive pool (preserve). **UNRELATED** = `NEUTRAL_TEXT` + non-parent windows (preserve).
- `taxonomic_georgia` → 16009 (absorption, PRIMARY) · `first_letter_large` → 8463 (absorption) ·
  `taxonomic_us` → 846 (M5 co-firing) · `toxicity_insult` → auto (declared co-firing negative pole).

## Reuse / config

`core.py` is the iter-4/iter-5 engine (only the multi-latent `abl_latent` generalization for M7 +
`WORK` repoint). `method.py` adds: `build_u_sub`, the three-arm forget-matching + generation + joint CIs,
the fork logic, M5/M6/M7, the curve-based localization validation, and the new output schema.

- SAE: `google/gemma-scope-2b-pt-res`, `layer_12/width_16k/average_l0_82` (JumpReLU, d_model 2304).
- Model: `google/gemma-2-2b` (bf16, eager); edit + read at `blocks.12.hook_resid_post` (hidden idx 13;
  gating cosine **0.919**, L0 ≈ 88). GPU (NVIDIA L4, 23 GB). `$0` model-internal; LLM judges **< $2**
  (hard cap $10). Canonical units / KG from iter-3 `gen_art_experiment_3`.

## Run

```bash
uv run method.py --smoke                                                          # gating + u_sub distinctness + 1 judge
uv run method.py --cases taxonomic_georgia --cap 30 --gen_per_set 6               # mini (< $0.10)
uv run method.py --cases taxonomic_georgia,first_letter_large,taxonomic_us,toxicity_insult \
                 --cap 0 --gen_per_set 18                                          # full (the reported run)
```

## Outputs

- `method_out.json` — `metadata` (gating; judge spend per model; per-case 3-way matched-forget curves,
  `s_kg/s_sub/s_whl`, matched_target; **`joint_diff_CI_KG_vs_SUB`** + collateral/fluency CIs +
  curve-dominance; `joint_diff_CI_KG_vs_WHOLE` secondary; `u_sub_meta` {n_pos,n_sib,underpowered,
  sub_probe_auc,cos_with_whole_parent}; `dense_localization_curve`; second-judge κ + CI; `fork_verdict`;
  M7 `unit_vs_single`; M5 US reclassification; human-proxy; summary with the M1′ gate; honest negatives)
  + `datasets`: `unlearn_per_prompt` (one row per (case,role,gen-prompt) with `predict_kg_abl` /
  `predict_dense_sub_abl` / `predict_dense_whole_abl` / `predict_rand` / `predict_noop` continuations +
  both judges' per-op utilities) and `kg_vs_dense_per_case` (one row per case, `output`=expected,
  `predict_kg_abl`=fork verdict, all decisive CIs). `full_/mini_/preview_method_out.json` are size-reduced
  variants. `logs/` run logs; `results/` smoke + mini diagnostic runs.

## Honest negatives (verbatim in `metadata.honest_negatives`)

- "Beats whole-parent erasure" is **RETIRED** as the headline; the decisive comparator is the
  sub-context-labeled `u_sub`. The "a single dense hyperplane structurally cannot localize" framing is
  **DELETED** — `u_sub` is itself a localizing single direction; KG's edge is sparse-firing gating.
- The win traces to the **single** discovered absorber, not multi-member grouping (M7).
- Absorption is **narrow** (these structured sub-contexts); numeric sub-contexts sit below the
  SAE-reconstruction gate and are out of scope.
- `toxicity/insult` is a **co-firing** case: the KG edit is **not surgical** (footprint 0.166,
  firing-Jaccard 0.882, no recall-hole) — the regime mechanism holds. It nonetheless registers
  `KG_BEATS_USUB` on the LLM-judge joint, but the **$0 model-internal joint does NOT corroborate it**
  (CI includes 0) and `u_sub` itself fails to localize in co-firing, so this is a **weak judge-only edge,
  not a surgical win**; it is **not** counted toward the absorption gate.
- `taxonomic_us` is a **router false-negative** (M5): its absorber footprint is low/surgical-looking, but
  the small parent recall-hole (0.197) flags co-firing — so it is reclassified out of the absorption gate.
- `mi_corroborates_fork` is reported per case; for `first_letter_large` the noisier model-internal joint
  is inconclusive even though both LLM judges agree — reported, not hidden.
- If the second judge is unavailable, M6 judge-robustness is **unverified** and any `KG_BEATS_USUB` is
  flagged accordingly.

## Headline result (full run)

**Gate PASSED.** The two **absorption** cases are both **`KG_BEATS_USUB`** (joint Δ CI excludes 0 favoring
KG **and** the second-family judge CI also excludes 0): Georgia (16009) and `large` (8463), with `u_sub`
localizing better than whole-parent and the M7 win tracing to the single absorber. United States (846) is
an M5 router false-negative; `toxicity/insult` is the co-firing case described above. Two LLM judges
(`claude-haiku-4.5` + `gpt-4o-mini`), 1459 calls, **$0.53** total (target $2, hard cap $10). Deterministic
human-proxy spot-checks pass for Georgia and `large`.
