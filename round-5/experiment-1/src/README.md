# M1 — KG-Localized Single-Absorber **Unlearning** Beats Dense Parent Erasure on a Joint Collateral+Fluency Outcome

The **load-bearing downstream win** for the auditability-first two-track **Counterfactual Co-Response
Grouping (CCRG)** units. iter-4 showed a single **KG-named absorber latent** gives a *surgical* edit (a
capability the dense probe lacks). This experiment converts that capability into **a better RESULT than
the dense baseline** on an outcome that matters: **selective sub-concept UNLEARNING**.

> **WIN ⇔** at **MATCHED forget-quality**, ablating one KG-named absorber (**KG-ABL**) yields strictly
> **lower sibling+parent collateral AND better preserved fluency** than the standard dense
> diff-of-means / LEACE parent erasure (**DENSE-ABL**, baseline *f*), with a **paired-bootstrap CI on the
> JOINT (retain-quality × fluency) outcome difference that excludes 0**.

## Headline result (`method_out.json`, full run)

**4 cases, 2 `DOWNSTREAM_WIN_CONFIRMED` → the M1 gate is PASSED.** Judge spend **$0.4367** (876 calls,
0 fail / 0 refusal; hard cap $10, target $2).

| case | absorber | regime | verdict | retain-KL KG | retain-KL DENSE | joint Δ (KG−DENSE) [95% CI] | KG util | DENSE util | KG footprint | firing-Jaccard | dom. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| taxonomic / **Georgia** | 16009 | absorption | **DOWNSTREAM_WIN_CONFIRMED** | 0.00003 | 0.1022 | **+0.423 [0.274, 0.571]** | 1.75 | 1.33 | 0.014 | 0.013 | 1.00 |
| first-letter / **large** | 8463 | absorption | **DOWNSTREAM_WIN_CONFIRMED** | 0.00002 | 1.1245 | **+1.646 [1.479, 1.799]** | 1.82 | 0.17 | 0.030 | 0.002 | 1.00 |
| taxonomic / United States | 846 | absorption | *PARTIAL_WIN* | 0.00011 | 0.0314 | +0.357 [0.196, 0.524] | 1.70 | 1.35 | 0.017 | 0.040 | 1.00 |
| toxicity / **insult** (co-firing) | 13367 | co-firing | *EXPECTED_LOSS_ROUTER_CONSISTENT* | 0.0123 | 0.0233 | +0.208 [**−0.035**, 0.451] | 1.17 | 0.97 | **0.166** | **0.882** | 1.00 |

- **Georgia / large**: KG-ABL wins the JOINT outcome **and** both sub-dimensions independently
  (collateral CI and fluency CI each exclude 0 favoring KG). For `large`, the dense *starts-with-L*
  erasure at matched forget collapses to utility **0.17** (it wrecks fluency/content on every token),
  while KG stays at **1.82**.
- **United States** (weaker, multi-token absorber): joint CI excludes 0 (KG wins) and collateral favors
  KG, but the fluency CI includes 0 → honest **PARTIAL_WIN**.
- **toxicity / insult** is the **declared honest negative pole**: insult sub-attributes **co-fire** with
  the toxic parent (firing-Jaccard **0.882**, no parent recall-hole), so the single latent fires on
  **16.6%** of tokens — *not* a clean handle. The joint CI **includes 0**: KG does **not** beat dense,
  exactly as the firing-Jaccard router predicts. (The model-internal joint leans KG — `UNEXPECTED_WIN` —
  but the primary AxBench judge outcome does not; reported verbatim.)

**Regime split (the contribution):** absorption (Jaccard 0.002–0.04, footprint 0.014–0.03) → clean
surgical unlearning that beats the baseline; co-firing (Jaccard 0.88, footprint 0.17) → no joint win.
**Curve-level dominance = 1.00 for every case**: KG has strictly lower collateral (and lower unrelated
perturbation) at *every* achievable forget level, so the win is robust to the single matched-point.

## What is compared (at MATCHED forget-quality)

| Operator | Edit | Role |
|---|---|---|
| **KG-ABL** (ours) | `h ← h − λ·z_l·W_dec[l]` — ablate the KG-named absorber, **gated by its own sparse firing** | surgical |
| **DENSE-ABL** (baseline *f*) | `h ← h − β·(h·u)u` — erase the diff-of-means **parent** hyperplane (one direction for the WHOLE parent; for a binary parent ≈ LEACE) | structural over-shoot |
| **RAND** | ablate a firing-rate-matched random content latent | sanity (≈ no effect) |
| **NOOP** | unedited model | reference for "content unchanged" |

**Forget-matching (the crux):** sweep λ∈{0,…,4} / β∈{0,…,4}; `forget(op,s)` = mean next-token KL on
held-out FORGET windows at the target token; set `matched_target = 0.8·min(maxKG, maxDENSE)` and pick
`s_kg`, `s_de` reaching it. KG reaches forget with a **tiny footprint**; dense must suppress the whole
parent (siblings included) — the structural over-shoot the task is built around.

**Joint outcome:** for each held-out RETAIN+UNRELATED prompt, generate a 40-token greedy continuation
under each edit hook and score it with an **AxBench-style OpenRouter LLM judge**
(`anthropic/claude-haiku-4.5`, temp 0): `utility = harmonic_mean(fluency, content_pres) ∈ [0,2]`.
`joint_diff_CI = paired_bootstrap_diff(util_KG, util_DENSE, B=10000)`. Model-internal corroboration
(high-n retain next-token KL + continuation perplexity) is reported alongside, and is the explicit
fallback if the judge is budget-limited/unavailable.

## Cases / data (held-out eval fold disjoint from the probe-fit fold)

- **FORGET** = corpus windows with `sub_context == X` (suppress).
- **RETAIN** = sibling sub-contexts + parent-positive pool (preserve).
- **UNRELATED** = `NEUTRAL_TEXT` + non-parent windows (preserve).
- Cases: C1 taxonomic/Georgia→16009, C2 first-letter/large→8463, +taxonomic/US→846, C3 toxicity/insult
  (re-found by max-AUC among toxic rows = **13367**, matching iter-4).

## Reuse

`core.py` is iter-4 `gen_art_experiment_2/method.py` **verbatim** (only the `WORK` path repointed):
`JumpReLUSAE`, `load_sae`, `ModelBundle` (`determine_layer_idx`/`encode_rows`/`edit_layer`),
`ParentProbe` (logistic probe **and** the diff-of-means dense direction `u_t`), `make_edit_hook`,
`side_effects`, `forward_pos_logprobs`/`kl_rows`/`behavioral_curve`, `paired_bootstrap_diff`,
`bootstrap_mean_ci`, `_scale_for_on_target`, `pick_random_latents`, `content_responsive`,
`load_taxonomic`/`load_first_letter`/`load_toxicity`, `NEUTRAL_TEXT`, `read_canonical_units`,
`save_json`. `method.py` adds the genuinely-new pieces: **forget-matching**, **generation under the
edit hook**, the **LLM judge**, the **joint composite + KG−DENSE CIs**, and **curve-level dominance**.

- SAE: `google/gemma-scope-2b-pt-res`, `layer_12/width_16k/average_l0_82` (JumpReLU, d_model 2304).
- Model: `google/gemma-2-2b` (bf16, eager attn); edit + read at `blocks.12.hook_resid_post`
  (hidden_states idx 13; gating cosine **0.919**, L0 ≈ 88).
- Canonical units / KG from iter-3 `gen_art_experiment_3` (`taxonomic.anchor=3792`, Georgia→16009,
  `first_letter.L` `8463`→`large`).
- GPU (NVIDIA L4, 23 GB). **$0 model-internal**; LLM judge **$0.44** (< $2 target, hard $10 cap).

## Run

```bash
uv run method.py --smoke                                            # gating + Georgia locality + 1 gen + 1 judge
uv run method.py --cases taxonomic_georgia --cap 30 --gen_per_set 6 # mini (< $0.10)
uv run method.py --cases taxonomic_georgia,first_letter_large,taxonomic_us,toxicity_insult \
                 --cap 0 --gen_per_set 24                           # full (the reported run)
```

## Outputs

- `method_out.json` — `metadata` (gating, judge spend, canonical units, per-case curves, matched scales,
  collateral / fluency / joint CIs, judged-forget confirmation, curve-dominance, win verdicts, honest
  negatives) + `datasets`: `unlearn_per_prompt` (one row per (case, prompt): prefix → role, with
  `predict_kg_abl`/`predict_dense_abl`/`predict_rand`/`predict_noop` continuations and per-op judge
  fluency/content_pres/utility) and `kg_vs_dense_per_case` (one row per case, `output`=expected, all
  CIs). `full_/mini_/preview_method_out.json` are size-reduced variants. `logs/` run logs;
  `results/` smoke + mini diagnostic runs.

## Honest negatives (verbatim in `metadata.honest_negatives`)

- **United States**: `PARTIAL_WIN` — joint CI excludes 0 favoring KG, but not both sub-dimensions are
  individually significant (a lower-magnitude, multi-token absorber gives a weaker fluency edge).
- **toxicity / insult**: `EXPECTED_LOSS_ROUTER_CONSISTENT` — co-firing regime; the single-latent
  ablation is not a clean handle (footprint 0.166, Jaccard 0.882), dense is the right tool — predicted
  in advance by the firing-Jaccard router. The model-internal joint leaned KG (`UNEXPECTED_WIN`) while
  the LLM-judge joint did not; both are reported.
