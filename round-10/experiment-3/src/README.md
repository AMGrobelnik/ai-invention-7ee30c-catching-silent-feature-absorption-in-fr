# M2′′′′′ — Genuine Cross-Deployment Zero-Label Transfer + Break-Even K* + Selection-Independent KL Localization + Amazon Caveat (iter-10)

The iter-10 **evidence fix (R1) + R4 + R6** for the auditability-first two-track **Counterfactual Co-Response
Grouping (CCRG)** SAE units. It removes the circularity in iter-9's "where-to-gate win", adds a
selection-independent localization axis, and diagnoses the one honest caveat iter-9 left open.

## What iter-9 left circular (R1)

iter-9 (`label_scarce.py`, `DEMONSTRATED_WHERE_TO_GATE_VALUE`) showed that the **label-free** single SAE
absorber handle (**KG-ABL**, "gate where the absorber fires", 0 labels at refit) holds at balanced-accuracy
≈ 0.97–1.0 while a **labeled** dense fair gate `d_sub(n)` collapses at low `n` and only catches up at
`n ≈ 5–20`. But (a) the absorber id was **hard-coded** (discovered in prior iters with **full** labels + an
oracle), and (b) **both** gates were scored on the **same** eval fold (deployment A == deployment B), so the
claimed label saving was **never realized on a different deployment**.

## The iter-10 fix — genuine A→B transfer

Fix the absorber id **once** on deployment **A** (the diagnostic fold, where it was discovered); then on a
**disjoint** deployment **B** score the **n-independent fixed-id SAE firing gate** against a **fresh** dense
gate fit on **B's own labels**, with B's fit/eval halves disjoint from each other and from A. Two
B-deployments + the iter-9 contrast:

| deployment | dense gate fit on | both gates scored on | role |
|---|---|---|---|
| `same_deployment_A` | diagnostic fold | full eval fold | **iter-9 reproduction / contrast** (circular) |
| `corpus_fold_B` | B_fit = half of eval fold (doc-hash split) | B_eval = the **other** half | **DECISIVE genuine transfer** |
| `carrier_shift_C` | TEMPLATED content x_on pairs | NATURAL eval-fold corpus | template→natural carrier shift |

`A_fit`, `B_fit`, `B_eval` are asserted pairwise disjoint (`transfer_disjoint`); the doc-hash split is a stable
`md5(source_doc_id or window-text) % 2` (reproducible across processes).

Four pieces, single GPU (Gemma-2-2b + Gemma Scope 16k L12, bf16, RTX 5090 / sm_120, torch cu128):

- **(A)** transfer curves: fixed-id SAE flat balacc vs dense balacc at `n ∈ {1,5,20,full}` (K_LOC=30 label
  resamples) on B and C, plus the A contrast. `$0`, deterministic.
- **(B)** break-even `K* = D / n*` — `D` = one-time discovery labels paid on A (`D_full` = full diagnostic
  fold; `D_min` = smallest A-subsample on which a label-frugal precision×coverage argmax **re-discovers the
  same absorber id**); `n*` = dense labels needed to match the fixed-id handle on B.
- **(C)** selection-**independent** next-token **behavioral-KL targeting**: `targeting = mean KL_X − mean KL_S`
  under the absorber's firing-gated ablation on held-out eval rows, vs a **random-latent shuffle null** (90th-
  percentile permutation bar over 8 draws). A *different* axis from the firing-precision the absorber was
  selected on. `$0` GPU forward.
- **(D)** Amazon `adv_joint`-vs-`adv_pres` **instrument-disagreement** diagnosis at matched behavioral forget
  (LLM-judged): is iter-9's residual `adv_joint` offset material?

**FORK.** `REAL_WHERE_TO_GATE_SAVING` if any powered case is `TRANSFER_CONFIRMED` (dense CI-separated below
the fixed-id handle at low `n` on B) or `TRANSFER_VIA_BREAKEVEN` (small `K*`); else `DROP_WHERE_TO_GATE`
(publishable boundary/tool paper on the M1′′′′ averted-cost capability + localization + the confinement
screen). **Both forks are publishable.**

## Headline result (FULL run, 5 cases × 2 axes + A contrast, KL all 5, edit Amazon+large, 2 judges, **$0.054**)

**Overall: `REAL_WHERE_TO_GATE_SAVING`** — and **honestly de-inflated from iter-9's blanket 5/5**: on the
genuine deployment B the transfer holds for **3/4 powered cases** but **not** for Jordan.

### (A)+(B) Transfer — fixed-id SAE handle (0 deploy labels) vs dense gate on the deployment's own `n` labels

| case | A_eval SAE (iter-9 repro) | **B SAE (flat)** | **B dense n=1** | below@n=1 | B verdict | n\* | K\*(D_full) | D_min |
|---|---|---|---|---|---|---|---|---|
| `taxonomic_georgia` | 1.000 (n_be 20) | **1.000** | 0.718 | **yes** | **TRANSFER_CONFIRMED** | 20 | 150 | 3000 |
| `taxonomic_us` | 0.983 (n_be 5) | **0.986** | 0.664 | **yes** | **TRANSFER_CONFIRMED** | 5 | 600 | 3000 |
| `named_entity_amazon` | 1.000 (n_be 20) | **0.999** | 0.674 | **yes** | **TRANSFER_CONFIRMED** | 20 | 69.7 | 1394 |
| `taxonomic_jordan` | 0.968 (n_be 5) | 0.955 | 0.761 | no | **NO_TRANSFER** | 1 | 3124 | **20** |
| `first_letter_large` | 0.995 (n_be 20) | 0.991 | 0.630 | yes | **UNDERPOWERED** (B_eval_pos=7) | 20 | 80.3 | **10** |

- **The A_eval contrast reproduces iter-9 exactly** (Georgia 1.0/n_be20, Jordan 0.968/n_be5, US 0.983/n_be5,
  Amazon 1.0/n_be20, large 0.995/n_be20) — proving the **only** change is the non-circular B deployment.
- On B, Georgia/US/Amazon keep the win (dense n=1 CI-separated **below** the fixed-id handle); the handle's
  near-perfect balacc means an imperfect dense gate cannot match it at low label budgets — the realized saving
  at ≤5 labels per deployment.
- **Jordan flips to NO_TRANSFER**: its handle is 0.955 (not 1.0), so a noisy n=1 dense gate's CI overlaps it —
  the dense gate matches even at n=1 on B. Honest, case-varying.
- `large` is rare (33 corpus windows): the doc-hash split leaves B_eval_pos=7 (<10) → **UNDERPOWERED on B**;
  the carrier-shift axis **C confirms** it (SAE 0.995 vs dense, `TRANSFER_CONFIRMED`).
- **Carrier-shift C**: `TRANSFER_CONFIRMED` for Georgia/US/Amazon/large, `NO_TRANSFER` for Jordan — the same
  split, under a template→natural distribution shift.
- **Break-even / D_min**: label-frugal re-discovery (precision×coverage argmax) recovers the **same** absorber
  id cheaply for **Jordan (D_min=20)** and **large (D_min=10)** but **not** for Georgia/US/Amazon
  (`D_min=D_full`) — an honest **feature-splitting** signal (several X-specific latents exist; the oracle-found
  one is not the cheap argmax). `K*` is therefore large under the conservative `D_full`; the decisive win is the
  low-`n` CI separation, not the amortized accounting.

### (C) Selection-independent behavioral-KL targeting (90th-pct random-latent null, 8 draws)

| case | targeting (scale 2) | CI | null p90 | frac null ≥ | verdict |
|---|---|---|---|---|---|
| `named_entity_amazon` | **0.650** | [0.48, 0.84] | 0.0002 | 0.00 | **KL_LOCALIZED** |
| `taxonomic_jordan` | 0.032 | [0.018, 0.048] | 0.0001 | 0.00 | **KL_LOCALIZED** |
| `taxonomic_georgia` | 0.028 | [0.009, 0.060] | 0.0016 | 0.00 | **KL_LOCALIZED** |
| `taxonomic_us` | 0.009 | [0.005, 0.014] | 0.0000 | 0.00 | **KL_LOCALIZED** |
| `first_letter_large` | 0.047 | [0.026, 0.072] | 0.876 | 0.12 | **KL_NULL_DESCRIPTIVE** |

The absorber-ablation next-token effect is **localized to the absorbed sub-context** (KL_X ≫ KL_S) and
**exceeds the random-latent null** for the named-entity and all three taxonomic cases — a localization signal
on an axis the absorber was **not** selected on (firing precision ≈ balanced accuracy; this coincidence is
stated explicitly in `metadata.kl_selection_caveat`, and the claim leans on held-out generalization + this
KL). **Honest negative for `large`**: its targeting (0.047) is real (CI excludes 0) but a **random
content-responsive spelling latent** produces a *larger* effect (null p90 = 0.876; one draw = 2.92), so the
absorber is not a uniquely strong **behavioral** handle for first-letter spelling — consistent with the broader
"single latents are unreliable" thesis. (This is the *opposite* split from firing-balacc, which localizes `large`
perfectly — firing localizes everywhere; behavioral-KL localizes only where the random-latent baseline is weak.)

### (D) Amazon instrument-disagreement diagnosis (R6)

| case | fq_kg | fq_fair | gap | both forget? | adv_pres(full) | adv_joint(full) | verdict |
|---|---|---|---|---|---|---|---|
| `named_entity_amazon` | 1.625 | 0.750 | **0.875** | no | 0.00 (incl 0) | **+0.68 (excl 0)** | **MATERIAL_REPORT_BOTH** |
| `first_letter_large` | 1.750 | 1.750 | 0.00 | yes | 0.00 | 0.00 | **ISOLATED_IMMATERIAL** |

At matched behavioral (subprobe) forget the LLM judge still scores KG as forgetting **more** than the fair gate
on Amazon (gap 0.875 > 0.30, `adv_joint` +0.68 excl 0 while `adv_pres` = 0) — a **material** instrument
disagreement → **report BOTH** metrics and **soften "demonstrated" to "preservation-advantage-only at matched
forget"** for the Amazon edit arm (the R6 fallback). For `large` the gap is 0 (both routes forget equally well)
→ the iter-9 offset is **isolated and immaterial**; "demonstrated" stands. A concrete continuation: KG-ABL
removes the entity (*"…Netflix has announced…"*) where the full fair gate does not (*"…Amazon has signed
director Woody Allen…"*).

## Engine reuse

`core.py` + `method.py` + `label_scarce.py` are the iter-4…9 Gemma-Scope L12/16k engine, **copied verbatim**
except the `WORK` path and an **additive** `_ls_stash_v2(...)` on each `setup_*` (carves the A/B/C deployment
partitions over the already-encoded arrays — **zero extra encode**). `transfer.py` is the only new driver
(generalized `build_dense_route` / `sae_gate_balacc_rows` over arbitrary fit/eval masks; `transfer_arm`,
`discovery_cost_min`, `kl_targeting`, `amazon_caveat`). Reuses the `forward_pos_logprobs` / `kl_rows` engine
for piece C and `run_edit_arm` (iter-9 verbatim) for piece D.

- SAE: `google/gemma-scope-2b-pt-res`, `layer_12/width_16k/average_l0_82` (JumpReLU, d_model 2304).
- Model: `google/gemma-2-2b` (bf16, eager), edit/read at `blocks.12.hook_resid_post` (gating cosine 0.919).
- Cases: `taxonomic_{georgia,jordan,us}` (absorbers 16009/540/846), `named_entity_amazon` (6846),
  `first_letter_large` (8463). Judges `anthropic/claude-haiku-4.5` (primary) + `openai/gpt-4o-mini`. Spend
  **$0.054** / target $2 / hard cap $10.

## Run

```bash
.venv/bin/python transfer.py --smoke                                              # stash-v2 + arms + KL checks
.venv/bin/python transfer.py --cases taxonomic_georgia,named_entity_amazon --no_judge   # mini ($0)
.venv/bin/python transfer.py                                                      # FULL (5 cases, 2 axes, edit)
.venv/bin/python make_variants.py method_out.json                                # full/mini/preview
```

## Outputs

- `method_out.json` (+ `full_/mini_/preview_`, all validate against `exp_gen_sol_out`).
  - `metadata`: `overall_transfer_fork_verdict`, per-axis tallies, `r1_fix`, `deployments`, full `per_case`
    (transferB/C curves with CIs + `dense_below_sae`, `n_breakeven`, `K_star`, `D_full`, `D_min`/trace, the
    `A_eval_contrast` reproducing iter-9, `kl_targeting`, `amazon_caveat`), `sae_handle_label_caveat`,
    `kl_selection_caveat`, gating check, cost, `honest_negatives`.
  - dataset **`transfer_curve`** (92 rows): one row per (case × axis × metric × n × route × deployment) with
    `predict_value` / `predict_ci_lo` / `predict_ci_hi` + `metadata_{axis,deployment,route,n,dense_below_sae,
    n_breakeven,K_star,D_full,D_min,kl_*,...}`; includes the SAE-flat, dense-per-n, A-contrast, and
    KL-targeting rows.
  - dataset **`edit_per_prompt`** (48 rows): Amazon + large re-judge — `predict_kg_abl` /
    `predict_dense_fair` / `predict_noop` continuations + both judges' fluency/content_pres per role.
- `logs/` run logs; `results/` mini + run-1 backup; `.venv/`, `cache/`, `__pycache__/` excluded from upload.
