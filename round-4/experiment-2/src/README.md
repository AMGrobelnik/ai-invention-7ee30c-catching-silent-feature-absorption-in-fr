# M1b — KG-Localized Surgical Sub-Concept Edit with Side-Effect Measurement

The downstream payoff of the auditability-first two-track **Counterfactual Co-Response Grouping (CCRG)**
units: using the emitted **feature knowledge-graph** (KG), we edit *exactly one sub-context* by ablating
its single **named absorber latent**, and show this achieves a **high on-target behavioral effect** with
**near-zero collateral** on sibling sub-contexts and a **tiny token footprint** — a capability a dense
parent-concept direction (the standard non-SAE handle) **structurally cannot** provide.

This is the *unique-capability* downstream task for the hypothesis that cluster/KG-level units are more
reliable than raw SAE latents: a single auditable latent yields a surgical, localized edit.

## What is compared (all at MATCHED on-target effect)

| Operator | What it does | Expected |
|---|---|---|
| **KG-ABL** (ours) | ablate the KG-named absorber `h ← h − λ·z_l·W_dec[l]` (gated by the latent's own sparse firing) | high on-target, ~0 collateral, tiny footprint |
| **DENSE-ABL** (baseline f) | erase the diff-of-means **parent** hyperplane `h ← h − β·(h·u)u` (one direction for the WHOLE parent) | cannot separate the sub-context → high collateral, footprint ≈ 1 |
| **RAND** | ablate a random firing-rate-matched content latent (≥3–12 draws) | on-target ≈ 0 |
| **(k)** | label-free JTT probe → dense hyperplane | exposes **no** per-sub-context latent to edit (structural) |
| **KG-ADD** | steer toward `h ← h + α·unit(W_dec[l])` (applied to every token) | global steer, not surgical (footprint ≈ 1) — shows surgicality comes from ablation's *sparse gating* |

Baselines required by the goal are covered: **(ii) non-SAE** = the dense diff-of-means / logistic parent
probe (DENSE-ABL is its erasure); **raw-latent SAE** contrast = RAND (a raw latent with no KG role) and
the (k) probe (no localizable latent).

## Primary measure — behavioral, model-grounded

`on_target` / `collateral` = **next-token KL divergence at the edited token's position** (the textbook
"steering/ablation with side-effect measurement"). KG-ABL only fires on its own sub-context's tokens →
it changes the model's processing of *those* tokens and is silent elsewhere; DENSE erasure changes *every*
parent-positive token. A frozen dense **parent probe** (logistic + diff-of-means, fit on a DISJOINT
diagnostic fold) is reported as a secondary instrument — its **margin** drop is huge & broad under
DENSE-ABL but, due to redundant encoding, is insensitive to single-latent edits, which is *why* the
behavioral KL is the primary on-target signal.

`SURGICAL SELECTIVITY = on_target / collateral` at matched on-target, with **paired bootstrap CIs**
(B=10,000) on the on-target effect, on the collateral, and on the **dense−kg collateral difference**
(claim holds iff that CI excludes 0 favoring KG). A graded verdict separates a *clean* surgical edit
(KG collateral not significantly > 0, off-target footprint < 2%, ratio ≥ 20) from a *partial / co-firing*
edit.

## Families & the firing-Jaccard router

- **Taxonomic (primary):** parent = "token is part of a country name". Targets = homograph countries
  whose KG names a high-precision absorber: **Georgia → 16009** (sub-ctx precision 0.955), **Jordan → 540
  / 8347** (0.975 / 1.0), **United States → 846 / 4760**. Siblings = the other high-count countries.
- **First-letter spelling:** parent = "word starts with L"; the highest held-out word-precision absorber
  is selected (e.g. `large → 8463`, `list → 3069`); siblings = other L-words.
- **Toxicity (negative pole):** parent = toxic-vs-neutral; target = **insult** and its strongest
  sub-attribute latent. Because toxicity sub-attributes **co-fire** with the parent (high firing-Jaccard,
  no clean parent recall-hole), the single-latent ablation is **not clean** (selectivity collapses,
  collateral significantly > 0, footprint rises ~50×) — exactly as the firing-Jaccard router predicts.
  This maps the positive pole (absorption: low Jaccard, clean hole → surgical) against the negative pole.

## Reuse

~90% reused from iter-2 (`gen_art_experiment_1`, SAE/JumpReLU loader, residual hook, steering/KL/PPL
matched protocol, NEUTRAL prompts) and iter-3 (`gen_art_experiment_3`, layer selection, `k_localization_check`,
canonical units + KG, paired/mean bootstrap). The genuinely new code is the **edit operators** and the
**behavioral side-effect measurement** (`forward_pos_logprobs`, `behavioral_curve`, `run_case`).

- SAE: `google/gemma-scope-2b-pt-res`, `layer_12/width_16k/average_l0_82` (JumpReLU, d_model 2304).
- Model: `google/gemma-2-2b` (bf16, eager attn). Edit + read at `blocks.12.hook_resid_post`
  (hidden_states idx 13; gating cosine ≈ 0.919, L0 ≈ 88 — matches iter-3).
- **$0 LLM spend** — all measurement is model-internal. GPU (NVIDIA L4, 23 GB).

## Run

```bash
uv run method.py --smoke                                   # gating + Georgia token-locality sanity
uv run method.py --families taxonomic --cap 40 --kl_prompts 16   # mini
uv run method.py                                           # full (all families)
```

## Outputs

- `method_out.json` — `metadata` (gating, canonical units/KG, k-localization, per-case curves, matched
  comparison, bootstrap CIs, regime router map, honest negatives) + `datasets[kg_surgical_edit]` one
  `exp_gen_sol_out` example per case. `mini_/preview_method_out.json` are size-reduced variants.
- `logs/` run logs. `results/` mini diagnostic runs.

## Headline result (full run, `method_out.json`)

7 cases, **5 SURGICAL_EDIT_CONFIRMED**. For every high-precision absorber the KG single-latent ablation is
surgical: on-target behavioral KL CI > 0, off-target collateral ≈ 0, footprint ≈ 0.1 %, while the matched
dense parent erasure has collateral ≈ its on-target and footprint = 1.0 (dense−kg collateral CI excludes 0).

| case | absorber | verdict | selectivity ratio | KG collat | dense collat | KG footprint | firing-Jaccard | parent hole |
|---|---|---|---|---|---|---|---|---|
| taxonomic / **Georgia** | 16009 | SURGICAL | **1722×** | 0.00003 | 0.0496 | 0.0015 | 0.012 | 0.77 |
| taxonomic / Jordan | 540 | SURGICAL | 2722× | 0.00000 | 0.0721 | 0.0010 | 0.014 | 0.68 |
| taxonomic / Jordan | 8347 | SURGICAL | 3247× | 0.00000 | 0.0288 | 0.0002 | 0.008 | 0.68 |
| taxonomic / United States | 846 | SURGICAL | 214× | 0.0001 | 0.0156 | 0.0013 | 0.040 | 0.19 |
| taxonomic / United States | 4760 | *PARTIAL* (low-prec) | 7.8× | 0.0007 | 0.0054 | 0.0152 | 0.009 | 0.19 |
| first-letter / **large** | 8463 | SURGICAL | 802× | 0.0001 | 0.0450 | 0.0022 | 0.002 | 1.00 |
| toxicity / **insult** (neg pole) | 13367 | *PARTIAL_CO_FIRING* | 2.4× | 0.0035 | 0.0083 | 0.1169 | **0.878** | **0.00** |

**Regime router map:** absorption (n=6) mean selectivity **1452×**, firing-Jaccard 0.014, footprint 0.0036;
co-firing (n=1) selectivity **2.4×**, firing-Jaccard 0.878, footprint 0.117 — a clean ~600× selectivity split
that confirms editability is regime-scoped exactly as the firing-Jaccard / parent-recall-hole router predicts.
RAND raw-latent on-target ≈ 0 (cannot reach matched), and the (k) label-free probe's decoder-projection
argmax is the parent latent, never a KG absorber → no per-sub-context handle. Honest negatives: the
low-precision US absorber 4760 is only partially surgical (precision predicts surgicality), and toxicity is
the declared non-surgical co-firing pole.
