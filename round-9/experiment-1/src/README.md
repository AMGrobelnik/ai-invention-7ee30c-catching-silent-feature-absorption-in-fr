# M1⁗ — Label-Scarce **Where-to-Gate** Demonstration

The single make-or-break iter-9 experiment for the auditability-first two-track **Counterfactual
Co-Response Grouping (CCRG)** units. It answers the one question the iter-8 result left open.

## The question

iter-8 (`DENSE-SUB-ABL-GATED-FAIR`) showed that **at FULL sub-context labels** a *genuinely-fair*
conditional-dense gate — erase the labeled direction `u_sub` **only where a precise logistic detector
`d_sub` fires**, β ≤ 1 — **matches** the label-free single SAE absorber handle (**KG-ABL**) on every case
(`KG_BEATS = 0/8`, `adv_KGvsFAIR ≈ 0`). iter-8's honest conclusion was therefore
`DISCOVERY_IS_THE_VALUE_FAIR_GATE_CLOSES_GAP`: the SAE adds no edit-quality *magic* beyond the labeled
direction — its value, if any, must be the **label-free WHERE-to-gate discovery**.

**This experiment tests that claim head-on.** Vary `n` = the number of sub-context-labeled examples used to
fit **both** `u_sub(n)` (the erase direction) **and** `d_sub(n)` (the gate), `n ∈ {0, 1, 5, 20, full}`. At
each `n`, compare the **labeled** dense fair gate against the **n-independent, label-free** SAE absorber
handle on two arms:

```
SAE handle (KG-ABL)        : "gate where the discovered absorber latent fires" — uses ZERO sub-context
                             labels at refit time -> a FLAT line in n.
Dense fair gate (n)        : u_sub(n) erased where d_sub(n) > 0, beta<=1 — its ENTIRE supervision is the n
                             sub-context labels.
```

If the SAE handle **holds** while the dense gate **collapses** as `n` shrinks → the concrete SAE-specific
positive the paper needs (`DEMONSTRATED_WHERE_TO_GATE_VALUE`). If the dense gate matches even at `n = 1`
(`FAIR_GATE_MATCHES_AT_N1`) → no SAE-specific value; retarget to a localization/confinement boundary paper.
**Both forks are publishable**; the experiment is decisive either way.

> **Label-free caveat (stated honestly).** The SAE handle uses **0 sub-context labels at refit time** (the
> absorber id is fixed/discovered once), so its curve is flat in `n`. The absorber was *discovered* with
> labels in prior iterations → the handle is **amortized / transferable** label-free at deployment, **not**
> zero-label end-to-end. This is recorded in `metadata.sae_handle_label_caveat`.

## Two arms

| arm | metric | cost | cases |
|---|---|---|---|
| **LOCALIZATION** (decides the fork; never dropped) | gate **balanced-accuracy** on a FROZEN disjoint eval fold | **$0**, deterministic, `K_LOC=30` label resamples | all 5 |
| **EDIT** | preservation/forget quality at **matched meaningful forget** | 2 LLM judges, `K_EDIT=4` resamples | large, Amazon |

**Localization** = does the gate fire on the *right* tokens?  `balacc = ½(TPR + TNR)` where TPR = P(gate fires
| held-out target-sub-positive), TNR = P(gate silent | held-out sibling-positive). The SAE handle's gate is
"absorber latent fires"; the dense gate's is `d_sub(n) > 0`. The dense gate is refit `K_LOC` times on fresh
`n`-row subsamples → a label-sampling CI; the SAE point gets an eval-row bootstrap CI. **`n = 0`** is the
chance anchor 0.5 (a conditional gate is undefined with zero labels).

**Edit.** Fix the matched forget target to the SAE handle's own achievable **behavioral** forget
(`matched_target = 0.8·max KG subprobe-drop`, the frozen iter-8 sub-probe positive-rate drop on held-out X
contexts). Match KG and each dense-gate-at-`n` to that target via their own β/λ sweeps (β ≤ 1; if a low-`n`
gate cannot reach it, `reaches=False`, β=1 — an informative under-erosion, never driven past β=1). Then judge
free continuations (FORGET / RETAIN / UNRELATED) with two LLMs.

- **PRIMARY edit metric = `adv_pres`** = paired-bootstrap diff of the preservation joint
  `HM(fluency, content_pres)` over held-out RETAIN+UNRELATED prompts, KG minus dense (>0 favors the SAE
  handle). It is the **iter-8-comparable, anchor-respecting** statistic and cleanly isolates the where-to-gate
  effect: **few labels → mislocalized gate / noisy `u_sub` erase → collateral damage to preservation**; full
  labels → `adv_pres → 0` (the iter-8 match, reproduced).
- **SECONDARY (stricter) = `adv_joint`** = `HM(forget_quality, preservation)`. It additionally credits KG's
  higher *judged* forget quality and can stay > 0 at full labels via **instrument disagreement** (at matched
  *behavioral* subprobe-drop the judge still scores KG as forgetting more) — flagged `adv_joint_full_offset`,
  reported as an honest caveat, **not** counted as the where-to-gate signal.

## Cases (built on the iter-8 engine VERBATIM)

`core.py` + `method.py` are the iter-4…8 Gemma-Scope L12/16k engine, copied here unchanged except `WORK` and
an **additive** `_ls_stash(...)` on each `setup_*` that exposes the already-computed fit/eval residual arrays
(zero extra compute). `label_scarce.py` is the only new driver.

| case | X | absorber `l` | parent | role | localization | edit |
|---|---|---|---|---|---|---|
| `first_letter_large` | large | 8463 | 205 | concentrated | ✓ | ✓ |
| `named_entity_amazon` | Amazon | 6846 | 2768 | concentrated | ✓ | ✓ |
| `taxonomic_georgia` | Georgia | 16009 | 3792 | distributed-edit | ✓ | — |
| `taxonomic_jordan` | Jordan | 540 | 3792 | distributed-edit | ✓ | — |
| `taxonomic_us` | United States | 846 | 3792 | co-firing | ✓ | — |

- SAE: `google/gemma-scope-2b-pt-res`, `layer_12/width_16k/average_l0_82` (JumpReLU, d_model 2304).
- Model: `google/gemma-2-2b` (bf16, eager), edit+read at `blocks.12.hook_resid_post` (gating cosine **0.919**).
- Single GPU (ran on a 16 GB RTX 2000 Ada). `$0` model-internal; two judges
  `anthropic/claude-haiku-4.5` (primary) + `openai/gpt-4o-mini` (second). Total spend **$0.34** / target $3.

## Run

```bash
uv run label_scarce.py --smoke                                                       # stash + refit + ops checks
uv run label_scarce.py --cases first_letter_large --edit_cases first_letter_large \
  --n_grid 1,5,full --K_LOC 8 --K_EDIT 2 --gen_per_set 4 --cap 80                     # mini (< $0.05)
uv run label_scarce.py                                                               # FULL (5 loc + 2 edit)
uv run make_variants.py method_out.json                                              # full/mini/preview
```

## Headline result (FULL run, 5 loc + 2 edit cases, 2 judges, 817 calls, **$0.34**)

**Overall verdict: `DEMONSTRATED_WHERE_TO_GATE_VALUE`.** In **both** arms, on **every** powered case, the
label-free SAE handle **holds** at high quality while the labeled dense fair gate **collapses at low label
budgets** and only catches up after `n ≈ 5–20` labels — exactly the SAE-specific positive iter-8 said was the
only remaining value.

### Localization arm — gate balanced-accuracy vs `n` (all 5 cases DEMONSTRATED)

| case | SAE (flat, **0 labels**) | dense n=0 | dense n=1 | dense n=5 | dense n=20 | dense full | n_breakeven |
|---|---|---|---|---|---|---|---|
| `first_letter_large` | **0.995** [.991,.998] | 0.50 | 0.67 [.50,.88] | 0.94 [.86,.98] | 0.99 [.97,1.0] | 0.96 | **20** |
| `named_entity_amazon` | **1.000** [1.0,1.0] | 0.50 | 0.67 [.49,.89] | 0.94 [.88,.98] | 1.00 [.98,1.0] | 1.00 | **20** |
| `taxonomic_georgia` | **1.000** [1.0,1.0] | 0.50 | 0.71 [.55,.87] | 0.97 [.93,.99] | 1.00 [.99,1.0] | 0.99 | **20** |
| `taxonomic_jordan` | **0.968** | 0.50 | 0.73 [.48,.88] | 0.93 [.88,.99] | 0.99 [.95,1.0] | 1.00 | **5** |
| `taxonomic_us` | **0.983** | 0.50 | 0.70 [.49,.90] | 0.94 [.87,.98] | 0.98 [.97,1.0] | 1.00 | **5** |

At `n = 1` the dense gate's CI is **separated below** the SAE flat point on all 5 cases (1 label per side
yields a noisy `u_sub` direction + a midpoint gate that over-fires on siblings, TNR ≈ 0.3). The gate needs
**`n_breakeven = 5–20` labels per side (10–40 total)** to reach the balanced-accuracy the SAE handle delivers
for free — a direct, $0, deterministic measure of the **labeling cost the SAE handle saves**. At `full`
labels the dense gate matches the SAE handle (**reproducing the iter-8 match**).

A notable extension: Georgia/Jordan/US are *weak edit handles* (iter-8: tiny `max_kg`), yet their absorbers
are **strong localizers** (balacc 0.97–1.0). The where-to-gate value therefore **decouples from edit
strength** — it is the iter-8 *"firing-signature ≠ edit-handle"* finding, now turned into a positive: the
firing signature is exactly the label-free localizer.

### Edit arm — `adv_pres` (PRIMARY) vs `adv_joint` (stricter secondary); >0 favors the SAE handle

| case | n=1 `adv_pres` | n=5 | n=20 | full (anchor) | verdict |
|---|---|---|---|---|---|
| `first_letter_large` | **+0.81** (excl 0) | +0.08 (incl 0) | +0.03 (incl 0) | **+0.00** (incl 0) | DEMONSTRATED, breakeven n=5 |
| `named_entity_amazon` | **+0.91** (excl 0) | **+1.23** (excl 0) | **+0.39** (excl 0) | **+0.00** (incl 0) | DEMONSTRATED, breakeven full |

At matched forget, the **clean, anchor-respecting `adv_pres`** is **0 at full labels for both cases** (the
iter-8 match, reproduced) and is **significantly positive at low `n`** because the under-/mis-localized gate
(noisy `u_sub`, broad `d_sub`) inflicts preservation collateral the precise label-free SAE handle avoids.
KG-ABL produces clean removals (e.g. *"Amazon has announced…"* → *"Netflix has announced…"*) where the `n=1`
gate corrupts fluency. Amazon needs the **full** label budget for the dense gate's *edit* to match — stronger
than its localization breakeven (n=20) — because the **erase direction** `u_sub(n)`, not just the gate, must
also be learned; the SAE absorber supplies both the *where* (its firing) and the *what* (its decoder
direction) for free.

### Honest caveat (populated automatically)

`named_entity_amazon`: the stricter `adv_joint` stays **+0.52 at full labels** (`adv_joint_full_offset=True`).
This is an **instrument-disagreement artifact** — at matched *behavioral* (sub-probe) forget the LLM judge
still scores KG as forgetting more than the dense gate — **not** a label-scarcity effect. The where-to-gate
fork is therefore decided on `adv_pres`, which converges to ~0 at full labels. (`metadata.honest_negatives`.)

## Outputs

- `method_out.json` (+ `full_/mini_/preview_` variants, all validate against `exp_gen_sol_out`).
  - `metadata`: `overall_fork_verdict`, `per_arm_verdict`, `verdict_drivers`, `localization_tally`,
    `edit_tally`; full `curves` per case (SAE flat ± CI, dense per-`n` ± CI, `n_breakeven`,
    `labeling_cost_saved_per_side/total`); `primary_edit_metric=adv_pres`; the `iter8_anchor`; gating check;
    `sae_handle_label_caveat`; `cost`; `honest_negatives`.
  - dataset **`label_scarce_curve`** (43 rows): one row per (case × metric × `n` × route) with
    `predict_value` / `predict_ci_lo` / `predict_ci_hi` and `metadata_{case,metric,route,n,n_resamples,
    balacc_tpr/tnr,dense_below_sae,overlaps_sae,adv_joint/pres_*,Q_*,…}`.
  - dataset **`edit_per_prompt`** (192 rows): per (case × `n` × role × prompt) the
    `predict_kg_abl` / `predict_dense_sub_gated_fair_n` / `predict_noop` continuations + both judges'
    fluency/content_pres + `fair_beta`, `reaches`, subprobe/completion drops.
- `logs/` run logs; `results/` mini run + the run-1 backup; `cache/`, `.venv/`, `__pycache__/` excluded from
  upload.
