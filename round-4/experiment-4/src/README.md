# Iter-4 — First-Letter Selection Isolation (M5) + Endpoint Honesty (M4) + Compact-vs-15-Wide Transparency (M7)

Re-runs the frozen-SAE first-letter two-track **Counterfactual Co-Response Grouping (CCRG)** pipeline
(Gemma-Scope L12/16k JumpReLU SAE, gating cosine > 0.9, exact word-token localization) verbatim from
iter-3 and surgically adds three **honest-scoping** deltas. The iter-3 `method.py` was copied and only
the anchor step, `run_c1`, the verdict builder, and the output assembly changed; all load-bearing code
(SAE loader, hook, firing, diagnostic, baselines, E1/E2/admission, RE-k, bootstrap) is byte-identical.

## The three deltas

- **M5 — Selection isolation (the new decisive core).** Three NON-RANDOM, label-free, count-matched
  selectors are built over the SAME cover-eligible set `E = Lr` the K-track uses, each picking EXACTLY
  `k = |K_UNIT|` latents by ONE label-free criterion and max-pooled IDENTICALLY to the unit:
  `S_rec` (top-k by content-flip **recall** = cover size), `S_prec` (top-k by firing **precision**),
  `S_mag` (top-k by mean response **magnitude**). The only factor varying vs the unit is the
  membership/SELECTION rule, so `unit − S_*` isolates the two-track **set-cover** selection from sensible
  label-free selection. Reported per-letter held-out AUC + paired-bootstrap **AUC-difference CIs**
  (B = 10,000, whole content-flip pair-cluster resampling). The set-cover-specific claim is ESTABLISHED
  only where the unit beats **(h) AND all three S_\*** with CI excluding 0; else scoped to
  *cover-based eligibility + sensible selection*. The iter-3 **RE-k** floor is retained, demoted.

- **M4 — Endpoint honesty.** (a) An unsupervised **firing-floor anchor validation**: a valid parent
  anchor must fire on ≥ 5 % of held-out corpus windows; this rejects the iter-3 **I = 1227** anchor
  (fires 0 % on corpus = a spurious content-flip-only anchor) and substitutes the highest-recall
  corpus-firing eligible latent. (b) The per-letter **JOINT** (E1 AND selection-vs-the-M5-bar) and a
  **renamed** verdict keyed off it (not the easy RE-k floor). (c) An explicit **letter-I annotation**.
  The over-aggregating iter-3 `ABSORPTION_REPAIR_SELECTION_CONFIRMED` verdict is recorded under
  `legacy_iter3_verdict` and contrasted.

- **M7 — Compact named unit vs 15-wide max-pool.** Reports the COMPACT unit (anchor + diagnostic-
  corroborated, named absorbers, capped at 5) alongside the full 15-wide `K_UNIT`, with their
  AUC-difference CI, an `anchor_only` floor, and an **AUC-vs-cumulative-k** curve — disentangling
  human-auditable compactness from raw classification AUC.

## RESULTS (full L,O,T,I,D run, B = 10,000; `method_out.json`)

`primary_endpoint = REFRAMED_TO_ELIGIBILITY_AND_SENSIBLE_SELECTION` (n_joint = 2, n_eligibility-only = 2).

| letter | anchor (Δ) | unit AUC | beats h / REk / S_rec / S_prec / S_mag | set-cover | E1 |
|---|---|---|---|---|---|
| L | 205 (—) | 0.905 | ✓ ✓ ✗ ✓ ✗ | no | ✓ |
| O | 12334 (—) | 0.917 | ✗ ✓ ✗ ✓ ✗ | no | ✓ |
| T | 6355 (—) | 0.858 | ✓ ✓ ✗ ✓ ✓ | no | ✓ |
| **I** | **1227→1634** | 0.983 | ✓ ✓ ✓ ✓ ✓ | **yes** | **✓** |
| D | 6210 (—) | 0.956 | ✓ ✓ ✓ ✓ ✓ | yes | ✓ |

- **M4 firing-floor recovered I.** I's recall-argmax anchor 1227 fires 0 % on corpus; the validated
  anchor 1634 (fires 20.6 %) IS the form-free-diagnostic parent, so **E1 now PASSES for I** (5/5 overall,
  up from iter-3's 4/5). The firing-floor fix repaired the iter-3 spurious-anchor bug.
- **M5.** The set-cover-specific selection is established only on **I and D** (unit beats all three
  non-random selectors). On L/O/T the strong `S_rec` (top-k by recall, which picks the anchor + the
  highest-coverage latents) matches the unit, so the win there is *eligibility + sensible selection*, not
  set-cover-specific. Pooled across letters the unit beats `S_rec` by 0.109 (CI [0.077, 0.143]), `S_prec`
  by 0.273, `S_mag` by 0.120, and (h) by 0.188 — but per-letter `S_rec` is significant on only 2/5.
- **M7.** The compact named unit is **significantly below** the 15-wide pool on every letter (ΔAUC −0.056
  to −0.200, CIs exclude 0): the diagnostic-uncorroborated absorbers carry real classification signal, so
  human-auditable compactness costs AUC — reported honestly, not hidden.
- **Legacy contrast.** The iter-3 rule (E1 ∧ unit > h ∧ RE-k on ≥ 3/5) would have declared
  `ABSORPTION_REPAIR_SELECTION_CONFIRMED` (RE-k is an easy floor: median draw AUC ≈ 0.63–0.69,
  frac_rek ≥ unit ≤ 0.008). The honest per-letter joint vs the non-random selectors reframes this.

## Hardware / reproduction (verified)

This run is on an **RTX 2000 Ada (sm_89)**; iter-3 ran on an RTX 5090 (sm_120). The UNMODIFIED iter-3
`method.py` was re-run on this host and produced numbers **identical** to this iter-4 run for L (unit AUC
0.905, K_UNIT ending in latent 1566, RE-k mean 0.651), confirming the additive M4/M5/M7 code does not
perturb the pipeline. Differences from the *stored* iter-3 anchors (L unit 0.876, member 1362) are bf16
**hardware** numerics breaking a discrete greedy set-cover tie at L's 15th member — not a code change.
See `metadata.repro_appendix`.

## How to run
```bash
uv sync
uv run method.py --smoke                # stage 0: load + reconstruction gating (cosine 0.924, EV 0.857)
uv run method.py --letters L --mini     # stage 1: mini plumbing test on L
uv run method.py --letters L            # stage 2: full L
uv run method.py                        # stage 3: full L,O,T,I,D (default), ~14 min on one GPU
```
Key flags: `--b_gap` (AUC-diff bootstrap B, default 10000), `--rek_draws` (default 1000), `--steering`
(opt-in; off by default), `--no-superset-surface` (use iter-1 inline surface pairs).

## Output
`method_out.json` (schema `exp_gen_sol_out`): `{metadata, datasets}`. All analysis under `metadata.*`
(`per_letter[L].{anchor_validation, E1, E2, C1.per_method+auc_diff, selection_isolation, compact_vs_wide,
admission, unit_definition}`, `verdicts`, `pooled_across_letters`, `repro_appendix`, `config`,
`gating_check`). `datasets` = one group per letter of held-out test-fold rows with
`predict_{unit,a,b,c,h,REk,S_rec,S_prec,S_mag,unit_compact,unit_15wide,anchor_only}` alongside
`input`/`output`. `full_/mini_/preview_method_out.json` are the size variants (all < 1 MB).
