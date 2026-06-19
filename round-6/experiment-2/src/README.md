# M2′ — Is SAE Feature **Absorption** a *Safety-Attribute* Phenomenon? A $0 Screen + a Conditional Downstream-Win Test vs a Sub-Context-Targeted Dense Direction `u_sub`

This experiment asks whether the **feature-absorption signature** that makes a single KG-named SAE
absorber a *surgical* unlearning handle (established for the homograph entity **Georgia → 16009** and
first-letter spelling) **extends to safety-relevant identity attributes** (religion, race/ethnicity,
sexual-orientation/gender-identity, nationality). It has two parts:

1. **A $0 absorption SCREEN** (the always-emitted deliverable). For each identity *hierarchy* we build
   candidate slices **inline** from `google/civil_comments` (gazetteer-matched windows, CC0) + a
   deterministic content-flip template set, find the firing-floor-validated **parent** latent, and test
   every group for the **Georgia signature**: a large parent **recall-hole** (>0.5) covered by a
   **firing-disjoint** (firing-Jaccard <0.1), **precise** (≥0.7), hole-covering absorber, on ≥150
   eligible diagnostic positives.
2. **A CONDITIONAL downstream-win test** (M1′). For any group that *is* absorption-structured — and,
   **always**, for the Georgia/Jordan **positive control** — we compare, at **matched forget-quality**,
   ablating the **one KG-named absorber** (**KG-ABL**) against erasing the **sub-context-targeted dense
   direction** `u_sub = diff-of-means(target-group, SIBLING-group)` (**DENSE-ABL-sub**, the decisive
   honest comparator), on a **joint retain-utility × fluency** LLM-judge outcome (paired-bootstrap
   ΔJoint CI, B≥10 000, two independent judges) plus a $0 model-internal selectivity / curve-dominance
   track. (The whole-parent direction `u_parent` is kept as a clearly-labelled *secondary* reference.)

> **Why `u_sub` is the right baseline.** iter-5 M1 already beat the *whole-parent* dense erasure. The
> sharper, fairer question is whether one absorber still wins against a dense direction that is itself
> *targeted at the sub-context* (target vs siblings). That is the contribution of `u_sub`.

## Headline result (full run: `civil_scale=full`, 1.76 M civil_comments rows; judge spend **$0.30**)

**The scoping finding is the headline: safety-attribute SAE absorption is HOMOGRAPH-CONFINED.** Of
**44** eligible safety identity groups (≥150 diagnostic positives) across 4 hierarchies, **only 2** are
absorption-structured — **`white`** (race; hole 0.63, absorber-Jaccard 0.019) and **`straight`**
(orientation; hole 0.72, Jaccard 0.009) — and **both are lexical homographs**. Every *descriptive*
identity term — religion (11 eligible: Muslim/Christian/Jewish/Catholic/…), nationality (20 eligible:
Mexican/Chinese/Canadian/…), plus gay/lesbian/Asian/Arab — shows **no parent recall-hole**: the general
identity parent reliably fires on them (`n_eligible_with_no_hole = 42`, `n_co_firing = 0`). Absorption
tracks **lexical polysemy** (exactly like Georgia/Jordan), **not safety semantics**. (`metadata.scoping_summary`.)

A **non-circular form-free absorption-fraction oracle** (SAEBench/Chanin-A.13: decoder-contribution
projected onto a parent LR-probe direction trained on disjoint data — *never used to flag*) corroborates
every flagged edge: Georgia 0.11, white 0.46, straight 0.26 (all ≈ their firing-based hole-coverage).

Downstream (`overall_verdict = SAFETY_ABSORPTION_FOUND_NO_WIN`), at MATCHED forget-quality vs the
sub-context-targeted `u_sub`, two independent judges (`claude-haiku-4.5` + `gemini-2.5-flash`),
paired-bootstrap B=10 000:

| case | absorber | recall-hole | oracle | matched forget-KL | ΔJoint CI (KG−u_sub) | 2nd judge | curve-dom | verdict |
|---|---|---|---|---|---|---|---|---|
| **taxonomic / Georgia** (positive control) | 16009 | 0.77 | 0.11 | 0.052 | **[0.53, 0.96]** excl 0 | excl 0 | 1.00 | **DOWNSTREAM_WIN_CONFIRMED** |
| **orientation / straight** (safety) | 3898 | 0.72 | 0.26 | 0.0012 | [0.04, 0.38] excl 0 | **incl 0** | 1.00 | **SAFETY_WIN_CONFIRMED (primary only)** |
| **race / white** (safety) | 1170 | 0.63 | 0.46 | 0.0004 | [−0.10, 0.20] incl 0 | — | 0.00 | **NO_ON_TARGET_EFFECT** |

- **The single-absorber surgical win is decisive for the entity homograph (Georgia) but does NOT robustly
  transfer to safety identity attributes.** Georgia: at matched forget, **KG-ABL** retain-collateral KL ≈
  **3e-5** vs `u_sub` ≈ **0.078** (diff CI excl 0), curve-dominance **1.0**, ΔJoint [0.53,0.96] under
  **both** judges — beating even the *sub-context-targeted* dense direction (sharper than the whole-parent
  baseline iter-5 M1 already beat).
- **Honest nuance (in `metadata.honest_negatives`).** `straight`'s win is **small-magnitude** (matched
  forget only 0.0012 vs Georgia's 0.052) and **judge-fragile**: the primary judge ΔJoint CI excludes 0 but
  the second judge (gemini) is borderline (CI includes 0) — so the rigorous two-judge gate is NOT met.
  `white` is absorption-structured in the **screen** (and oracle-confirmed 0.46) yet its absorber has **no
  on-target leverage** downstream — **absorption STRUCTURE does not guarantee unlearning LEVERAGE**. Hence
  the conservative `SAFETY_ABSORPTION_FOUND_NO_WIN`: structure exists at homograph safety tokens, but the
  decisive downstream win seen for Georgia does not robustly carry over.

(Exact numbers in `method_out.json → metadata`: `overall_verdict`, `scoping_summary`,
`positive_control_reproduced`, `screen_summary_counts`, `screens`, `per_candidate_downstream`,
`honest_negatives`, `llm_cost_usd`.)

## What is compared (at MATCHED forget-quality)

| Operator | Edit | Role |
|---|---|---|
| **KG-ABL** (ours) | `h ← h − λ·z_l·W_dec[l]` — ablate the KG-named absorber, gated by its own sparse firing | surgical |
| **DENSE-ABL-sub** (decisive baseline) | `h ← h − β·(h·u_sub)u_sub`, `u_sub = mean(target) − mean(SIBLINGS)` | sub-context-targeted dense |
| **DENSE-ABL-parent** (secondary) | `h ← h − β·(h·u_parent)u_parent`, whole-parent diff-of-means | structural reference (model-internal only) |
| **RAND** | ablate a firing-rate-matched random content latent | sanity |
| **NOOP** | unedited model | reference |

Forget-matching: sweep λ/β, `matched_target = 0.8·min(maxKG, max_sub)` on held-out target-group FORGET
windows (next-token KL); pick scales reaching it. Joint outcome: 40-token greedy continuations under each
hook on RETAIN (siblings) + UNRELATED prompts, scored 0/1/2 on fluency × content-preservation
(harmonic mean ∈ [0,2]); `ΔJoint = joint(KG-ABL) − joint(DENSE-ABL-sub)`, paired by prompt.

## Screen design (Section 1–2, $0)

- **Hierarchies & gazetteers** (`safety.py`): `religion` (Muslim/Christian/Jewish/…), `race_ethnicity`
  (Black/White/Asian/Latino/…), `orientation_gender` (gay/lesbian/transgender/straight/…), `nationality`
  (Mexican/Chinese/Iranian/…). Homograph-strong surfaces (Black/White/Asian/gay/straight/queer/Indian/…)
  carry the strongest absorption prior and are flagged.
- **Three coordinated components per hierarchy**: (A) content-flip pairs (identity word vs surface-matched
  neutral filler in the same template slot) → identifies the content-responsive parent; (B) natural
  corpus positives from civil_comments (token-anchored at the matched surface, labelled by the
  earliest-occurring group surface); (C) clean negatives (windows with **no** identity surface of **any**
  hierarchy). Folds 50/50 fit/diagnostic, seed 20240617.
- **Parent** = highest positive-firing-recall content-responsive latent that clears an unsupervised
  content-flip firing floor (≥0.20) **and** a held-out corpus firing floor (≥0.05) — fixes the
  spurious 0%-corpus anchor; chosen **without** the Chanin diagnostic.
- **Absorber search** (K-track-lite, vectorised): among content-responsive latents firing on the group,
  pick the **firing-disjoint** (Jaccard<0.1), **precise** (≥0.7) latent with the largest **hole-coverage
  gain** (bootstrap CI excl 0). A best-AUC detector is reported separately for transparency.
- **`absorption_structured`** ⇔ recall-hole>0.5 ∧ Jaccard<0.1 ∧ ≥150 eligible ∧ precision≥0.7 ∧
  hole-coverage-gain≥0.05 (CI excl 0). High-confidence flag adds recall-hole>0.78. All criteria are
  firing-based (no output-logit / Chanin spelling diagnostic) → non-circular w.r.t. prior absorption work.
- **Form-free oracle** (`absorption_fraction_oracle`, §2.5): each flagged absorber is *independently*
  validated by the SAEBench/Chanin-A.13 `absorption_fraction` — the decoder contribution `z_l·W_dec[l]`
  projected onto a parent LR-probe direction `d_p` trained on **disjoint** fit-fold residuals, evaluated on
  the parent's hole rows. Reported, never used to flag (strictly non-circular).

## Files

- `method.py` — driver: gating, the screen, the conditional `u_sub` downstream, the Georgia/Jordan
  positive control, output assembly. Reuses `core.py` (iter-5 M1) **verbatim** (SAE loader, `ModelBundle`,
  edit hooks, `behavioral_curve`, `paired_bootstrap_diff`, `_scale_for_on_target`, …).
- `safety.py` — inline safety-slice builders + the screen primitives (`identify_parent`,
  `screen_subcontexts`, vectorised K-track-lite absorber search).
- `core.py` — iter-5 `gen_art_experiment_1/core.py` (only `WORK` repointed to this workspace).
- `prefetch.py` — pre-fetch SAE params + `unsloth/gemma-2-2b` mirror + `google/civil_comments`.
- `method_out.json` (+ `mini_`/`preview_`) — `exp_gen_sol_out` schema: datasets `safety_screen`
  (one row per (hierarchy, group), `predict_absorption ∈ {ABSORPTION_STRUCTURED, CO_FIRING, NO_HOLE,
  DESCRIPTIVE_ONLY, NO_PARENT}`) and `downstream_subcontext` (per (candidate, prompt) continuations with
  `predict_kg_abl` / `predict_dense_abl_sub`, plus per-candidate summary rows).
- `results/` — smoke / screen / downstream mini diagnostic runs. `logs/` — run logs.

## SAE / model

- SAE: `google/gemma-scope-2b-pt-res`, `layer_12/width_16k/average_l0_82` (JumpReLU, firing = encode>0,
  d_model 2304); hook `blocks.12.hook_resid_post`. Gating reconstruction cosine **0.919**, L0 ≈ 88.
- Model: `unsloth/gemma-2-2b` mirror (gated `google/gemma-2-2b` falls back to the mirror), bf16, eager attn.
- Single GPU (NVIDIA L4, 23 GB). $0 screen; LLM judge spend well under the $3 target / $9.5 hard cap.

## Run

```bash
uv run method.py --smoke                                   # SAE+model+gating+locality+1 judge
uv run method.py --posctl_only --screen_only               # taxonomic screen only ($0; reproduces Georgia)
uv run method.py --posctl_only --cap 30 --gen_per_set 6    # Georgia downstream mini
uv run method.py --civil_scale full --cap 0                # FULL screen + conditional downstream (reported)
```

## Honest negatives (verbatim in `metadata.honest_negatives`)

- **Homograph-confinement is the capping limitation**: 42/44 eligible safety groups show **no recall-hole**
  — absorption is narrow (homographs + spelling), not a property of safety attributes per se. Descriptive
  identity terms are well-captured by the general identity parent.
- **`race / white`** — absorption-structured in the screen but **`NO_ON_TARGET_EFFECT`** downstream (its
  absorber barely moves the forget target); excluded from selectivity means. Structure ≠ leverage.
- **`orientation / straight`** — **`SAFETY_WIN_CONFIRMED` under the primary judge only** and
  **small-magnitude** (matched forget 0.0012); the second judge (gemini) ΔJoint CI includes 0, so the
  rigorous two-judge gate fails → contributes to `SAFETY_ABSORPTION_FOUND_NO_WIN`. Reported, not hidden.
- **Jordan** — recall-hole reproduces (0.66) but its best absorber covers too few holes (gain < floor) →
  not flagged; an honest weaker case.
- `NO_ON_TARGET_EFFECT` rows are excluded from any mean; selectivity is reported as `floor-limited ≥X`
  when KG collateral is below numerical precision; judge/KL disagreements are reported, not hidden.
