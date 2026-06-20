# gen_art_evaluation_1 — test_idea

> Phase: `invention_loop` · round 8 · `gen_art`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_evaluation_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 10:51:12 UTC

```
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact executor (Step 3.3: GEN_ART in the invention loop)

Executing a plan to produce a concrete artifact.
GEN_PAPER_TEXT will use your artifact in the next paper draft.

Rigorous artifact with clear results → strong paper. Sloppy artifact → misdirected research.
</your_role>
</ai_inventor_context>

<task>
Evaluate experimental results using domain-appropriate methods, metrics, and analysis techniques.
When in doubt, prefer more metrics over fewer — but only ones that make sense for the domain.
</task>

<common_mistakes_to_avoid>
- Holding multiple large objects in memory at once — process one at a time: load → compute → del + gc.collect() → next
- Loading more data than needed — select only required tables/columns/rows
- Accumulating results in loops without freeing intermediates — aggregate incrementally
- Spawning too many parallel processes — stay within the hardware limits
- Running computation without timeouts or without first testing on a small sample
</common_mistakes_to_avoid>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_evaluation_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_evaluation_1/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_evaluation_1/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_evaluation_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_evaluation_1_idx3
type: evaluation
title: >-
  Iter-8 Integrity-Lock Eval: De-Inflate the Edit Headline, Lay Both Forget Instruments Side-by-Side, Show Concentration>Absorption
  Predicts the Win, and Lock the Georgia +0.561 Retraction
summary: >-
  Pure-CPU, $0, read-only re-analysis over the EXISTING iter-6/7 edit data (art_Cgk9ETiZfvtl, art_ZxVw0e4seBq3, art_3WXWsaSoGMnK).
  Following the project integrity-lock pattern (COMPUTE-from-source then COMPARE-to-stored, never overwrite), it produces
  GEN_PAPER_TEXT drop-in numbers that are robust to any truncation of the new iter-8 experiments: (1) the DE-INFLATED lead
  KG-vs-strongest-ungated-dense (+1.00 on 'large') reconciled against the inflated +1.58-vs-footprint-gated with its beta~2.97
  over-erasure stats; (2) BOTH meaningful-forget instruments (gold-completion-drop AND frozen sub-probe-drop) per case/operator
  side-by-side, with an instrument-disagreement metric proving next-token-KL matching != behavioral matching; (3) a per-case
  CONCENTRATION proxy correlated with the win/meaningful-forget outcome vs the absorption-regime label (concentration predicts,
  absorption does not); (4) the consolidated Georgia +0.561 RETRACTION (iter-6 win sat at a near-NOOP operating point); plus
  an operator-divergence flag (3%-global-footprint vs 95%-X-rate gate) the new experiments must unify. Emits eval_out.json
  (exp_eval_sol_out) with metrics_agg, per-case datasets, cross_checks, and cross-checked drop-in paper_wording.
runpod_compute_profile: cpu_heavy
metrics_descriptions: |-
  PURE-ANALYSIS INTEGRITY LOCK. No GPU, no model load, no LLM calls ($0). Read-only over three stored experiment outputs. EVERY headline value is RECOMPUTED from source columns, then COMPARED to the stored expectation; mismatches are reported in metadata.cross_checks with an explanatory note and NEVER overwritten (this mirrors art_w7p8du2N1f0Y / art_-k4Yg-l4NaNO). Use a fixed seed (1234) for every bootstrap so results are deterministic and re-checkable.

  === INPUTS (exact paths; load full_method_out.json, fall back to method_out.json if absent) ===
  - D1 = art_Cgk9ETiZfvtl @ /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_7/gen_art/gen_art_experiment_1/full_method_out.json. Use metadata.per_case[*] (5 cases: target_subcontext in {Georgia, large, Jordan, United States, insult}), metadata.summary, datasets.gated_dense_per_prompt (288 rows; columns predict_kg_abl/predict_dense_sub_gated/predict_dense_sub_abl/predict_dense_whole_abl/predict_noop + per-operator judged utilities + NOOP-identical + model-internal signals), datasets.kg_vs_gated_per_case (5 rows). Also read this dir's method.py to extract the EXACT joint-utility formula, paired_bootstrap_diff, completion_drop, fit_sub_probe and calibrate_gate_tau definitions so recomputation is faithful.
  - D2 = art_ZxVw0e4seBq3 @ .../iter_7/gen_art/gen_art_experiment_2/full_method_out.json. Use metadata.downstream[*] (3 cases: Amazon, Bush, Georgia-control), datasets.downstream_edit_per_prompt (90 rows), datasets.downstream_edit_per_case, metadata.screen_table (per-entity absorber_precision/hole/jaccard for Amazon/Bush/Cook).
  - D3 = art_3WXWsaSoGMnK @ .../iter_6/gen_art/gen_art_experiment_1/full_method_out.json. Use the Georgia kg_vs_dense_per_case entry (joint_diff_CI_KG_vs_SUB, matched_target_forget_kl, fork_verdict) and datasets.unlearn_per_prompt for Georgia if a recompute is needed.

  === GROUP A - DE-INFLATION (M1''' + M3''' lead number) ===
  A1. Mean joint utility per operator per D1 case: recompute from gated_dense_per_prompt judged-utility columns using the exact joint formula read from method.py (joint = judged retain-utility combined with fluency). Cross-check computed kg/gated/sub_joint_utility_mean against stored metadata.per_case[*].{kg_joint_utility_mean, gated_joint_utility_mean, sub_joint_utility_mean}. Expected for large: KG=1.8704, GATED=0.2870, SUB=0.8704.
  A2. Paired-bootstrap (B=10000, seed 1234, over preservation prompts) joint diffs per case: (i) DE-INFLATED LEAD = KG-ABL minus DENSE-SUB-ABL (ungated, strongest dense); (ii) INFLATED = KG-ABL minus DENSE-SUB-ABL-GATED. Cross-check (i) against stored joint_diff_CI_KG_vs_SUB_secondary and (ii) against joint_diff_CI_KG_vs_GATED. Expected for large: lead = +1.000 CI[0.787,1.213] (n=36); inflated = +1.583 CI[1.361,1.787]. Verify the reconciliation 1.8704-0.8704=+1.00 and 1.8704-0.2870=+1.58 hold to <1e-3.
  A3. Over-erasure stats for large (and report for all cases): gated retain-collateral KL = retain_collateral_kl_gated_mean (0.290) vs ungated SUB retain_collateral_kl_sub_mean (0.021) -> over_erasure_ratio = 0.290/0.021 ~= 13.8x; the beta the gate was driven to = scale_gated_beta (2.967) vs scale_sub_beta (0.649); gated_vs_ungated_collateral_CI (diff -0.269, excl_0 true => gated has MORE collateral than its OWN ungated form). Also report collateral_diff_CI_KG_vs_GATED (+0.290) and collateral_diff_CI_KG_vs_SUB_secondary (+0.021).
  A4. Emit per-case de-inflation rows {case, kg/gated/sub joint means, lead_diff+CI, inflated_diff+CI, gated_collateral, sub_collateral, over_erasure_ratio, scale_gated_beta, scale_sub_beta, gated_vs_ungated_collateral_excl_0}. metrics_agg gets de_inflated_lead_large=+1.00 (with CI), inflated_gap_large=+1.58 (with CI), over_erasure_ratio_large~=13.8.

  === GROUP B - BOTH FORGET INSTRUMENTS SIDE-BY-SIDE (M4''') ===
  B1. For every D1 case x operator at the matched point, tabulate the TWO behavioral instruments: (a) gold-completion-drop = metadata.per_case[*].completion_drop_matched[op].drop_vs_noop with drop_ci/excl_0; (b) frozen sub-probe positive-rate drop = subprobe_drop[op].drop (and NOOP pos_rate, auc). Build one row per (case, operator) with both numbers + their CI/excl_0.
  B2. Instrument-disagreement metric, per case, on the decisive KG-vs-GATED contrast: completion_contrast = completion_drop[KG]-completion_drop[GATED]; subprobe_contrast = subprobe_drop[KG]-subprobe_drop[GATED]. Report sign_divergence = (sign(completion_contrast) != sign(subprobe_contrast)) and the signed magnitudes. For large this fires: completion favors GATED (KG 0.072 vs GATED 1.080 => completion_contrast=-1.008) while sub-probe favors KG (KG 0.417 vs GATED 0.0 => subprobe_contrast=+0.417) -> sign_divergence=TRUE. Also compute, per case, a rank-disagreement (Spearman or Kendall-tau between the two instruments' operator orderings over {KG,GATED,SUB}).
  B3. Quantify 'next-token-KL matching != behavioral matching': all operators are scaled to the SAME matched_target next-token KL, yet at that point completion_drop and subprobe_drop differ sharply across operators (e.g. large: KL-matched but completion_drop spans 0.072..1.080 and subprobe_drop spans 0.0..0.917). Report, per case, the across-operator spread (max-min) of each behavioral instrument at the KL-matched point as the divergence evidence, and recommend (for paper_wording) matching operators on a BEHAVIORAL measure (sub-probe drop or completion accuracy) rather than next-token KL. Flag that the load-bearing large completion CI is over only n=4 probes (RIGOR caveat) -- read drop_ci.n.
  B4. metrics_agg gets instrument_disagreement_cases (list of cases with sign_divergence=TRUE; expect {large}), and the large KG-vs-GATED contrast pair (-1.008 completion, +0.417 sub-probe).

  === GROUP C - CONCENTRATION-vs-ABSORPTION PREDICTOR (M3''' decisive descriptive) ===
  C1. Assemble a pooled case table across D1 (large, Georgia, Jordan, United States, insult) and D2 (Amazon, Bush). For each case read: absorber_precision (per-sub-context precision), gate_footprint_used / gate_target_footprint (firing footprint f_kg), firing_jaccard_with_parent, max_forget_kg (single-latent next-token-KL ceiling = edit leverage), regime label ('absorption' vs 'co-firing'), and outcomes: win_binary = (fork_verdict==KG_BEATS_GATED_DENSE...), meaningful_forget_binary = kg_can_forget (D1) / non-trivial-forget (D2), adv_continuous = joint KG-vs-GATED diff. For D2 use downstream[*] fields (gate_calibration, max_forget_kg, fork_verdict, joint_diff_CI_KG_vs_GATED) and screen_table absorber_precision.
  C2. CONCENTRATION PROXY (primary): concentration = absorber_precision * (1 / f_kg) read from stored fields (per the direction: per-sub-context precision x inverse footprint). ALSO compute two robustness variants and report all three: (v2) absorber_precision * max_forget_kg (precision x single-latent leverage), (v3) absorber_precision * (1 - firing_jaccard_with_parent) * sub_probe_max_drop. Rank/z-score each case under each proxy. The qualitative pattern to confirm: concentrated cases (large prec 1.0, Amazon prec 0.99/max_kg 1.14, insult high-precision co-firing) WIN; distributed cases (Georgia/Jordan country sense, US co-firing) LOSE -- crossing BOTH regime labels.
  C3. PREDICTIVE COMPARISON: compute point-biserial (proxy continuous vs binary outcome) and Spearman (proxy vs adv_continuous) for (a) each concentration proxy and (b) the absorption-regime binary label, each with a bootstrap CI (B=10000, seed 1234, resampling cases). predictive_delta = corr(concentration_proxy, outcome) - corr(absorption_label, outcome). EXPECT concentration to track win/meaningful_forget better than the absorption label (absorption label is near-uninformative because wins/losses cross it). Because n is small (~7 cases) this is EXPLICITLY descriptive: report the delta + CI but label it 'descriptive, small-n' in the row and in paper_wording. Cross-check the absorption-mean-vs-cofiring-mean comparison the paper currently leans on: adv_absorption_mean (1.583) vs adv_cofiring_mean (0.372) from metadata.summary, and note it is a 1-case-vs-2-case-mean (thin/circular) basis -- the per-case concentration correlation supersedes it.
  C4. metrics_agg gets concentration_vs_absorption_predictive_delta (primary proxy, with CI), the per-proxy correlations, and a boolean concentration_outpredicts_absorption.

  === GROUP D - GEORGIA +0.561 RETRACTION (M1''' carry / M6) ===
  D1. From D3 recompute (or read+cross-check) the iter-6 Georgia KG-vs-SUB joint = +0.5606 CI[0.318,0.811] n=44 at matched_target_forget_kl=0.0517. If recomputing from unlearn_per_prompt, use the method.py joint formula; else cross-check the stored CI.
  D2. From D1 (iter-7) read the near-NOOP evidence at/near that operating point for Georgia: max_forget_kg=0.0647 (17-30x smaller than dense ceilings), noop_identical_fraction.FORGET['KG-ABL']=0.889, subprobe_drop['KG-ABL'].drop=0.075, completion_drop_matched['KG-ABL'].drop_ci.excl_0=false, fork_verdict=NO_MEANINGFUL_FORGET, and the iter-7 KG-vs-GATED Georgia adv=+0.174 / KG-vs-SUB=+0.197 (vacuous, KG barely edits).
  D3. RETRACTION ROW + STATEMENT: the iter-6 +0.561 'win' sat at a near-NOOP operating point (KG won by barely editing, and also barely forgot); it is retracted/recontextualized as clean low-collateral PARTIAL suppression, not meaningful unlearning. metrics_agg gets retraction_iter6_georgia_adv=+0.561, retraction_iter6_matched_kl=0.0517, retraction_iter7_max_forget_kg=0.0647, retraction_noop_identical=0.889, retraction_subprobe_drop=0.075, retraction_status='RETRACTED_NEAR_NOOP'.

  === GROUP E - OPERATOR-DEFINITION DIVERGENCE FLAG (MINOR 4 / M1''' unify) ===
  E1. Cross-check the two 'footprint-matched gated dense' operators are NOT identical: D1 = global-neutral-pool footprint gate (calibrate_gate_tau; gate_tau~=101, gate_footprint_used~=0.025-0.028, gate_target_footprint~=0.014-0.03, ~3% global firing). D2 = gate_calibration.method=='footprint_match_clamped' on X-POSITIVE firing rate clamped ~0.95 (gate_fire_rate_X~=0.9467, gate_fire_rate_sibling~=0.045). Set metrics_agg.operator_divergence_flag=TRUE with both calibration descriptors and a note that the iter-7 headline aggregates a 3%-global-footprint comparison (large) with a 95%-X-rate comparison (Amazon); the new iter-8 experiments must unify into ONE gate operator (or document any per-case clamp in-table).

  === OUTPUT (eval_out.json, schema exp_eval_sol_out; validate full/mini/preview <100MB via aii-json + aii-file-size-limit) ===
  - metrics_agg: {de_inflated_lead_large, inflated_gap_large, over_erasure_ratio_large, instrument_disagreement_cases, large_kg_vs_gated_completion_contrast, large_kg_vs_gated_subprobe_contrast, concentration_vs_absorption_predictive_delta, concentration_outpredicts_absorption, retraction_* fields, operator_divergence_flag, absorption_mean_vs_cofiring_mean_basis_note}.
  - datasets: de_inflation_per_case (>=5 D1 rows + D2 rows), both_instrument_per_case_op (one row per case x {KG,GATED,SUB} with completion_drop+CI and subprobe_drop), concentration_predictor_per_case (~7 rows with proxies+outcomes+labels), retraction_per_case (Georgia row), operator_divergence (2 rows). Each dataset row must carry predict_* / value STRING fields if the project schema requires non-null string predictions (mirror the iter-5/6 validator gotcha: every example needs a predict_* string).
  - metadata.cross_checks: array of {name, computed, stored, abs_diff, rel_diff, match (bool at tol: 1e-3 for point stats; CI-overlap for bootstrap), note}. Include at minimum the A1 utility means, A2 lead/inflated diffs+CIs, D1/D2 collateral CIs, the iter-6 Georgia +0.561, and the summary adv_absorption/adv_cofiring means.
  - metadata.paper_wording: drop-in strings (cross-checked) for: (W1) de-inflated lead '+1.00 vs the strongest ungated dense on large (CI[0.79,1.21]), with +1.58 vs a footprint-matched gate reported only as a robustness check handicapped by beta~3 over-erasure (gated collateral 0.29 = 13.8x its own ungated 0.021)'; (W2) instrument disagreement 'at the next-token-KL-matched point the two forget instruments disagree in sign for large (completion favors the gated dense by 1.01, frozen sub-probe favors KG by 0.42), so KL-matching does not equalize behavioral forgetting; operators should be matched on a behavioral measure'; (W3) concentration finding 'the edit-win predictor is latent concentration/precision, not absorption: wins span an absorption case (large) and a co-firing case (insult), losses are distributed senses (Georgia/Jordan); a precision-x-inverse-footprint proxy tracks the outcome where the absorption-regime label does not (descriptive, n~7)'; (W4) retraction 'the iter-6 Georgia +0.561 win sat at a near-NOOP operating point (max single-latent forget KL 0.065, NOOP-identical on 89% of forget prompts, frozen sub-probe drop 0.075); it is retracted as low-collateral partial suppression, not meaningful unlearning'; (W5) operator unification note.

  === FAILURE / EDGE HANDLING ===
  - If a per-prompt judged-utility column is missing or the joint formula cannot be reproduced exactly, fall back to cross-checking the stored *_joint_utility_mean and *_diff_CI directly and mark the cross_check note 'stored-only (recompute unavailable)'; do not fabricate.
  - If a recomputed bootstrap CI does not overlap the stored CI, record match=false with a note (seeding/resample-unit difference) -- report, never overwrite.
  - Some D1 cases (insult, US) are regime='co-firing'; keep them in Group C (they are load-bearing for the concentration claim) but exclude US/insult from any absorption-only aggregate, matching metadata.summary.us_excluded_gate.
  - D2 Amazon/Bush use the 95%-X-rate gate, so their joint diffs are NOT directly comparable to D1's 3%-global-footprint diffs; carry them as supporting concentration points flagged with the operator note (Group E), not pooled into the D1 lead CI.
  - Keep all three output variants <100MB; per-prompt source datasets are tiny (288/90/~hundreds rows) so full retention is fine.
metrics_justification: >-
  These metrics are exactly the four reviewer-gating integrity issues (R1 de-inflation, R3 concentration-not-absorption, R4
  operator divergence, R5 instrument rigor) reduced to arithmetic over data that ALREADY exists, so GEN_PAPER_TEXT gets defensible
  drop-in numbers no matter how the new iter-8 edit experiments turn out. (1) The DE-INFLATED lead matters because the abstract
  currently leads with the largest, least-defensible gap: the +1.58 is KG beating a gated dense that was driven to beta~2.97
  over-erasure (its own collateral 0.29 is 13.8x its ungated 0.021), i.e. a handicapped control. Recomputing KG-minus-strongest-ungated-dense
  (+1.00, CI[0.79,1.21]) from the stored per-prompt utilities, and proving the +1.58/+1.00 reconciliation against the stored
  utility means, gives the paper an honest headline and pre-empts the #1 blocker. (2) Laying BOTH forget instruments side-by-side
  and quantifying their sign-disagreement at the KL-matched point is the only way to honestly support 'meaningful forget':
  the completion-drop and sub-probe-drop instruments rank KG vs the gated dense in OPPOSITE directions for the load-bearing
  large case, which both proves the forget is real on the behavioral sub-probe AND shows that matching on next-token KL does
  not equalize behavior -- a rigor fix the paper must state, not hide. (3) The concentration-vs-absorption predictor is the
  decisive evidence reframe: the wins cross both regime labels (absorption 'large' wins, co-firing 'insult' wins; absorption
  'Georgia/Jordan' lose), so a per-case precision-x-inverse-footprint proxy correlating with the outcome better than the absorption-regime
  label directly substantiates 'the win traces to concentration, not the absorption structure the method discovers' and retires
  the thin 1-vs-2-case absorption_exceeds_cofiring aggregate. It is correctly scoped as small-n descriptive. (4) Consolidating
  the Georgia +0.561 retraction closes the loop on a now-known-misleading prior headline by showing, in one row, that the
  win sat at a near-NOOP operating point (tiny max forget KL, 89% NOOP-identical, sub-probe barely moved) -- protecting the
  paper's integrity. The operator-divergence flag surfaces the 3%-global-footprint vs 95%-X-rate inconsistency the new experiments
  must unify. Because the whole artifact is a read-only, $0, deterministic recompute-and-cross-check, it is immediately runnable
  and fully robust to truncation of the expensive new GPU experiments, which is precisely its strategic value as the always-produced
  clean deliverable.
</artifact_plan>

<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
id: art_3WXWsaSoGMnK
type: experiment
title: 'M1'': KG single-absorber unlearning vs a sub-context-targeted dense baseline'
summary: >-
  M1' replaces the near-tautological WHOLE-PARENT dense comparator of iter-5 with a STRONGER, sub-context-targeted dense baseline
  u_sub = diff-of-means(target-sub-context-positive, sibling-positive in the same parent context), fit on a DISJOINT fold
  from the per-sub-context labels the testbeds carry. The decisive downstream test is selective sub-concept UNLEARNING: at
  MATCHED forget-quality (next-token KL on held-out FORGET windows, matched_target = 0.8*min(maxKG,maxSUB)), it compares KG-ABL
  (ablate one KG-named absorber, h -= lambda*z_l*W_dec[l], gated by the latent's own sparse firing) against the DECISIVE DENSE-SUB-ABL
  (erase u_sub) and a clearly-labeled SECONDARY DENSE-WHOLE-ABL (erase the whole-parent diff-of-means), plus RAND and (M7)
  KG-ABL-UNIT. The joint (retain-utility x fluency) outcome is scored by an AxBench-style OpenRouter judge (anthropic/claude-haiku-4.5)
  with paired-bootstrap KG-vs-SUB CIs (B=10000), curve-dominance, and model-internal corroboration (continuation PPL + retain
  next-token KL). Per-case FORK verdict: KG_BEATS_USUB (joint CI excl 0 favoring KG AND a 2nd-family judge CI also excl 0),
  KG_MATCHES_USUB_LABEL_FREE (CI includes 0 - KG matches u_sub WITHOUT needing the labels), or KG_LOSES_TO_USUB. RESULTS (full
  run, both judges, $0.53/1459 calls): GATE PASSED. The two ABSORPTION cases are both KG_BEATS_USUB - taxonomic Georgia(16009)
  and first_letter large(8463) - each with u_sub localizing better than whole-parent and the M7 win tracing to the SINGLE
  discovered absorber (the multi-member K-track unit only adds collateral); human-proxy spot-checks pass. Folded-in modules:
  (M1') u_sub localization validation is CURVE-BASED over the achievable dense forget range (the KG-pinned matched point is
  tiny because KG single-latent next-token KL has a small ceiling, so a single-point check is mis-specified) - this DELETES
  the false 'a single dense hyperplane cannot localize' framing and reframes KG's edge as sparse-firing GATING (token footprint
  -> 0 for absorption), NOT the dense direction failing to localize; (M5) United States(846) is a ROUTER FALSE-NEGATIVE reclassified
  to co-firing - its absorber footprint is low/surgical-looking but the small parent recall-hole (0.197) flags co-firing,
  so it is moved out of the absorption gate; (M6) a second different-family judge (openai/gpt-4o-mini) with Cohen kappa +
  Pearson/Spearman utility correlation keeps a KG win only if its CI also excludes 0, plus a deterministic $0 human-proxy
  check that KG-ABL preserves sibling tokens while DENSE-WHOLE corrupts them; (M7) unit-vs-single ablation. Toxicity_insult
  is the co-firing case where KG is NOT surgical (footprint 0.166, firing-Jaccard 0.882, no recall-hole - the regime mechanism
  holds); it registers KG_BEATS_USUB on the LLM-judge joint but the $0 model-internal joint does NOT corroborate it (CI includes
  0) and u_sub itself fails to localize in co-firing, so it is reported as a weak judge-only edge, not a surgical win, and
  is not counted toward the gate. A per-case mi_corroborates_fork flag is reported (Georgia/US True; large/toxicity False
  - the noisier model-internal proxy is inconclusive there even though both LLM judges agree). Reuses the iter-4/iter-5 Gemma-Scope
  L12/16k JumpReLU engine via core.py (only the multi-latent abl_latent generalization for M7 + WORK repoint). Single GPU
  (NVIDIA L4); $0 model-internal, <$2 LLM judges (hard cap $10). All outputs validate against exp_gen_sol_out: unlearn_per_prompt
  (per (case,role,prompt) with predict_kg_abl / predict_dense_sub_abl / predict_dense_whole_abl / predict_rand / predict_noop
  continuations + both judges' utilities) and kg_vs_dense_per_case (fork verdicts + all decisive CIs).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_experiment_1
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Dependency 2 ---
id: art_Cgk9ETiZfvtl
type: experiment
title: M1'' Gated-Dense Control + Honest Forget Test of KG Single-Absorber Suppression
summary: |-
  iter-7 M1'' decisively stress-tests the auditability-first two-track CCRG claim that ablating ONE KG-named absorber latent (KG-ABL) is a better unlearning handle than a dense baseline. It adds the FAIR control iter-6 lacked and an honest operating-point protocol.

  NEW OPERATOR (core.py): DENSE-SUB-ABL-GATED (kind='erase_dir_gated') erases the sub-context diff-of-means u_sub ONLY where |h.u_sub|>tau; tau is calibrated (calibrate_gate_tau) so the gate's global firing fraction over a neutral pool equals the KG absorber's token footprint f_kg. This removes the iter-6 confound (KG edits ~1-3% of tokens; ungated u_sub edits every token). tau threaded through make_edit_hook/forward_pos_logprobs/behavioral_curve/side_effects/generate_under_edit/last_tok_logprobs. FIVE operators at the SAME swept matched forget: NOOP, KG-ABL, DENSE-SUB-ABL-GATED (decisive), DENSE-SUB-ABL (ungated, iter-6, secondary), DENSE-WHOLE-ABL (secondary), +RAND +KG-ABL-UNIT (M7).

  HONEST OPERATING POINT: per case we report max_forget_{kg,sub,gated,whole} (KG's next-token-KL ceiling is 17-30x smaller than the dense directions'), NOOP-identical fraction (KG is NOOP-identical on ~0.89 of FORGET prompts for the country cases), full collateral-vs-forget curves, a gate footprint sweep {0.5,1,2,4}*f_kg, matched_target=0.8*min(max_kg,max_gated), and op_high=0.95*max_kg.

  MEANINGFUL-FORGET PROOF ($0, deterministic, the key addition): (a) completion-accuracy drop = drop in gold-token log-prob on hand probes (capital-of-Georgia->Tbilisi, large->L, etc) with bootstrap CI; (b) frozen 1-D-free sub-probe d_sub (AUC~1.0) scored on the REAL post-edit residual via read_resid_under_edit; meaningful_forget[op] = (completion CI>0) OR (sub-probe positive-rate drop>=0.1). Decisive pair KG-ABL vs DENSE-SUB-ABL-GATED via paired_bootstrap_diff (B=10000) on the joint (retain-utility x fluency) outcome under TWO OpenRouter judges (claude-haiku-4.5 + gpt-4o-mini).

  PER-CASE 3-WAY FORK: KG_BEATS_GATED_DENSE_AT_MEANINGFUL_FORGET / GATED_DENSE_CLOSES_GAP_DISCOVERY_IS_THE_VALUE / NO_MEANINGFUL_FORGET_SCOPE_TO_PARTIAL_SUPPRESSION. Aggregate requires absorption advantage to EXCEED co-firing advantage; a US-excluded gate counts only powered absorption cases.

  RESULTS (5 cases, 2109 judge calls, $0.80 << $3 target; overall=SPARSE_SAE_HANDLE_ESTABLISHED, absorption_exceeds_cofiring=True, adv 1.58>0.37): (1) first_letter_large (spelling absorber 8463) = KG_BEATS_GATED_DENSE: KG meaningfully forgets (sub-probe drop 0.42, completion 0.11) AND beats the footprint-matched gated dense by +1.58 joint under BOTH judges with strictly lower collateral (CI excl 0) and 1.0 curve dominance -- a discovered single SAE feature beats a labeled+footprint-matched dense control. (2) taxonomic_georgia (16009) and taxonomic_jordan (540) = NO_MEANINGFUL_FORGET: the single-latent ablation CANNOT remove the DISTRIBUTED country sense even at full strength (max_kg 0.065/0.114, sub-probe drop 0.07/0.0); this directly EXPOSES that iter-6's KG_BEATS_USUB headline sat at a near-NOOP operating point (KG won by barely editing). (3) taxonomic_us (846) = NO_MEANINGFUL (co-firing). (4) toxicity_insult (13367) = KG_BEATS_GATED (+0.47) but co-firing, so excluded from the absorption gate. The month case was dropped because the iter-5 homograph month dataset's *_data_out.json artifacts were never materialized on disk; absorption set = {Georgia, large, Jordan}.

  OUTPUT (exp_gen_sol_out, validated full/mini/preview, 0.8MB): metadata.per_case (all operating points, gate tau sweep + footprint used, NOOP-identical, completion/sub-probe drops, meaningful_forget, collateral & joint CIs KG-vs-GATED decisive + KG-vs-SUB/WHOLE secondary + gated-vs-ungated, full-range collateral curves, M5/M6/M7, fork_verdict); metadata.summary (3-way fork counts, adv_absorption/adv_cofiring, absorption_exceeds_cofiring, us_excluded_gate, overall_verdict); 11 honest_negatives; datasets gated_dense_per_prompt (288 rows, predict_kg_abl/predict_dense_sub_gated/predict_dense_sub_abl/predict_dense_whole_abl/predict_noop + per-op judged utilities + NOOP-identical + model-internal signals) and kg_vs_gated_per_case (5 rows). For the paper: the honest, feature-dependent conclusion is that the single-SAE-absorber handle genuinely beats a fair dense control ONLY for concentrated features (spelling); for distributed taxonomic/co-firing senses it is clean low-collateral PARTIAL suppression, not meaningful unlearning.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_7/gen_art/gen_art_experiment_1
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Dependency 3 ---
id: art_ZxVw0e4seBq3
type: experiment
title: Named-Entity Homograph SAE Absorption Screen + Gated-Dense Unlearning Downstream
summary: |-
  M2'' CONFIRMATORY (supporting, not load-bearing) experiment on Gemma-2-2b + Gemma-Scope L12/16k JumpReLU SAE (gating cosine 0.92, layer hidden_states[13]). It consumes the previously-unused named_entity_safety hierarchy (art_KNPsfjByyxiS) and reuses the iter-5/6 engine verbatim (core.py, method_iter6.py) with two genuinely-new pieces: a $0 absorption SCREEN (screen.py) and a NEW gated-dense edit operator 'erase_dir_gated' + a footprint-matched gate-calibration primitive (calibrate_gate) added to core.py.

  THESIS TESTED: feature absorption = LEXICAL HOMOGRAPHY (a suppressed 'named-entity/org' parent latent under a polysemous surface token), NOT safety/demographic semantics. A single coherent content-responsive parent latent (2768; xon-recall 0.99, probe AUC 1.0, not diffuse) was identified non-circularly (recall-only + >5% firing-floor). Per eligible entity the screen computes, with the absorber chosen on the diagnostic fit fold and every metric scored on the disjoint train fold: recall-hole, K-track-lite absorber, firing-Jaccard(parent,absorber), held-out precision, hole-coverage-gain with bootstrap CI, and a form-free decoder-probe-cosine oracle (Chanin/SAEBench, tau 0.025). 'absorption_structured' is gated on the firing-signature (the canonical iter-2..6 definition the Georgia positive control satisfies); the form-free decoder-projection oracle is reported separately and confirms 3/3 named-entity hits (it is spelling/concept-tuned and does not transfer to the taxonomic Georgia absorber, which would be wrongly rejected if it gated the verdict).

  PRIMARY RESULT ($0 screen): 3/5 eligible named-entity homographs are absorption-structured AND oracle-confirmed: Amazon (hole 0.61, jac 0.048, prec 0.99, gain 0.61 CI>0, dec-cos 0.12), Bush (0.79/0.021/1.00/0.79, 0.04), Cook (0.72/0.045/1.00/0.70, 0.03). Apple (hole 0.25) and King (0.42) are NOT structured (the parent detector fires on them). Four descriptive-only homographs (West, Bell, Hunt, Banks) show the relaxed signature (n<150). The Georgia self-check PASSED (the identical screen flags the canonical taxonomic absorber 16009 structured). This reinforces the settled iter-6 demographic null: absorption tracks lexical polysemy.

  CONDITIONAL DOWNSTREAM (supporting; both judges claude-haiku-4.5 + gpt-4o-mini, $0.35 total, 949 calls): at matched forget (0.8*min(maxKG,maxSUB)) with an edit-vs-NOOP forget delta, four operators KG-ABL / DENSE-SUB-ABL / DENSE-SUB-ABL-GATED (footprint-matched gate, balanced-acc 0.95-0.97) / DENSE-WHOLE-ABL. Amazon = KG_BEATS_GATED_DENSE (non-trivial forget: median KL 0.58, 58% prompts changed; KG-vs-GATED joint CI [0.41,1.08] and 2nd-judge CI [0.35,0.68] both exclude 0; curve-dominance 1.0) -> a genuine NAMED_ENTITY_HOMOGRAPH_WIN. Bush = KG_MATCHES_GATED_DENSE (non-trivial forget, label-free parity). Georgia control = NEAR_NOOP_NO_WIN (KG cannot forget non-trivially at the matched point; the iter-5/6 Georgia 'win' was lower-collateral, not strong forgetting). Notably the named-entity absorber 6846 is a STRONGER edit handle (max_kg 1.14) than the country absorber (0.064).

  VERDICTS: overall_verdict = SAFETY_ABSORPTION_HOMOGRAPH_CONFINED (demographic null unchanged); secondary_tag = NAMED_ENTITY_HOMOGRAPH_WIN_FOUND. 8 honest negatives recorded (confirmatory framing, oracle scope/decoder-tuning, Bush parity, Georgia NEAR_NOOP context, named-entity-vs-country edit-handle strength).

  DELIVERABLES: method.py (driver), screen.py (screen), core.py (engine + erase_dir_gated + calibrate_gate), method_iter6.py (reused engine). method_out.json (+ full/mini/preview, all PASS exp_gen_sol_out, <=208KB) holds metadata.{screen_table, breadth_count, georgia_sanity, parent_identification, downstream (per-case matched_target, max_forget_kg/sub/gated/whole, full_range_collateral_curve, edit_vs_noop_forget, gate_calibration, joint CIs KG-vs-{GATED,SUB,WHOLE} under both judges, curve_dominance), overall_verdict, secondary_tag, honest_negatives, llm_cost_usd}. Three datasets: named_entity_absorption_screen (19), downstream_edit_per_case (3), downstream_edit_per_prompt (90).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_7/gen_art/gen_art_experiment_2
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>

<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>

<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Web search (Serper), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-image-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
- aii-handbook-multi-llm-agents: Multi-LLM agent orchestration patterns
</skills>
</available_resources>

<available_domain_handbooks>
If your domain has a handbook, read the relevant skill file BEFORE working on that domain.

- **Multi-LLM Agents** — evaluation metrics, agent orchestration patterns, benchmark design
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-python, aii-long-running-tasks, aii-json, aii-file-size-limit, aii-use-hardware, aii-parallel-computing.
TODO 2. Read preview files from dependencies to understand prediction format. Evaluate ALL experiments provided — do not skip or select a subset. Avoid re-training or re-executing the method unless absolutely necessary; prefer loading predictions from each dependency's method_out.json / predict_* fields. Read domain handbook if applicable (see <available_domain_handbooks>). Decide evaluation metrics based on artifact plan. Test basic functionality with 'uv run'.
TODO 3. Fully implement evaluation as described in artifact plan in './eval.py'. Use exp_eval_sol_out.json schema in aii-json skill for output format validation. Include everything specified in the artifact plan, but you may also implement additional relevant metrics or analysis beyond what's listed. Be very attentive to meticulously and exhaustively fix any errors in your code.
</todos>
```

### [2] HUMAN-USER prompt · 2026-06-18 10:51:12 UTC

```
### Goal

Develop a new clustering-based method for organising sparse autoencoder (SAE) activations from large language models into more reliable units of analysis than individual latents.

### Reviewer Scope

Limit the technical core to areas the reviewer can deeply evaluate. Other fields are welcome for inspiration but should not host the substantive contribution.

Reviewer-evaluable areas: clustering methods, semantic technologies, information retrieval, machine learning, LLMs, deep learning, sensor data analysis, classification, active learning, feature selection, practical applications of ML methods, applied knowledge discovery, knowledge extraction, knowledge graphs, and text data analytics.

Single SAE latents suffer from feature absorption, feature splitting, and non-atomicity, making them unreliable as classifiers and as steering targets — recent benchmarks show simple baselines often outperform raw-latent SAE methods. Treat SAE features as a learned knowledge representation: produce cluster- or group-level units derived from co-activation statistics, decoder-direction geometry, hierarchical decomposition, or learned grouping objectives, and optionally extract structured relations between cluster-level concepts (a feature-level knowledge graph).

Evaluation must compare against (i) raw SAE latents and (ii) at least one non-SAE baseline (difference-of-means probes, linear classifiers on raw activations) on concrete downstream tasks: feature-based classification of safety-relevant attributes, activation steering with side-effect measurement, and model-diffing between fine-tuned variants.

Constraints: must run on open-source pretrained SAEs (Gemma Scope, Neuronpedia) on a single GPU, produce human-auditable cluster definitions, and report failure modes honestly.

### Publication

Target ICLR primary, ICML fallback.

### Things to Avoid

Theoretical results in computational learning theory (generalisation bounds, sample complexity, convergence proofs). The contribution must be a method or empirical finding, not a theorem.
```

### [3] SKILL-INPUT — aii-json · 2026-06-18 10:51:34 UTC

The agent loaded the **aii-json** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-json
description: JSON validation and formatting toolkit. Validate JSON files against schemas for experiment pipelines, and generate full/mini/preview versions of JSON datasets. Use for validating pipeline outputs, checking schema compliance, or creating size-optimized JSON variants.
---

## Contents

- Validating JSON (schema validation against experiment schemas)
- Formatting JSON (generate full/mini/preview versions)

**IMPORTANT - Parallel execution:** GNU `parallel` subshells do NOT inherit `source activate`. Use `export` for variables and **single-quoted** command templates so parallel's subshells can resolve them:
```
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

---

## Validating JSON

Validate JSON files against predefined schemas for experiment-based hypothesis selection, data collection, solution generation, and evaluation.

### Quick Start

1. Read the schema spec you need to adhere to (e.g., `schemas/exp_eval_sol_out.json`)
2. Create your output file following that schema structure
3. Validate:

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /path/to/eval_out.json
```

### Script: aii_json_validate_schema.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /tmp/eval_out.json
```

**Parallel execution (multiple validations):**

IMPORTANT: When validating multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_validate_schema.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --format {1} --file {2}' ::: 'exp_sel_data_out' 'exp_gen_sol_out' 'exp_eval_sol_out' :::+ '/tmp/full_data_out.json' '/tmp/method_out.json' '/tmp/eval_out.json'
```

**Example output (success):**
```
Validating: aii_json_validate_schema.py
Format: exp_eval_sol_out

✓ Validation PASSED
```

**Example output (failure):**
```
Validating: aii_json_validate_schema.py
Format: exp_sel_data_out

✗ Validation FAILED

Errors:
  Path: datasets → 0 → examples → 0
  Error: 'output' is a required property
  Validator: required
```

**Parameters:**

`--format` (required)
- Format type to validate against
- Determines which schema to use

`--file` (required)
- Path to JSON file to validate
- Must be valid JSON
- **Always pass an absolute path.** Relative paths resolve from the
  ability server's CWD (typically ``/ai-inventor/aii_server``), not from
  your agent workspace, so ``data_out/x.json`` will silently look in the
  wrong directory and fail with "Could not load JSON file". The validate
  endpoint also accepts a ``workspace_dir`` arg if you need to keep a
  relative path — pass your workspace path there.

**Tips:**
- Fix errors in your JSON and rerun validation until it passes

### Schema Files

Schemas are stored in `.claude/skills/aii-json/schemas/`:

**Hypothesis Selection & Evaluation:**
- `sel_hypo_out.json` - Hypothesis Selection output (all hypotheses with selected flags)
- `feasibility_eval_all.json` - All hypotheses with feasibility scores
- `feasibility_eval_top.json` - Top 5 most feasible hypotheses
- `novelty_research_one.json` - Single hypothesis novelty research arguments with citations
- `novelty_eval_all.json` - All hypotheses with novelty scores
- `novelty_eval_top.json` - Single best selected hypothesis

**Experiment Pipeline:**
- `exp_sel_data_out.json` - Experiment Data Selection format
- `exp_gen_sol_out.json` - Experiment Solution Generation format
- `exp_eval_sol_out.json` - Experiment Solution Evaluation format

---

## Formatting JSON

Generate three size-optimized versions of a JSON file for efficient development and preview:
- **full**: Identical to original (all data)
- **mini**: First 3 items only (for quick testing)
- **preview**: Mini + all strings truncated to 200 chars (for quick inspection)

### Quick Start

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

### Script: aii_json_format_mini_preview.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

**Parallel execution (multiple files):**

IMPORTANT: When formatting multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_format_mini_preview.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --input {}' ::: 'full_data_out.json' 'method_out.json' 'eval_out.json'
```

**Example output:**
```
Generated 3 versions:
  Full (50 items): /path/to/full_method_out.json
  Mini (3 items): /path/to/mini_method_out.json
  Preview (3 items, truncated): /path/to/preview_method_out.json
```

**Parameters:**

`--input` (required)
- Path to input JSON file
- Must have a top-level array
- Example: `method_out.json`, `full_data_out.json`

`--output-dir` (optional)
- Output directory for generated files
- Default: same directory as input file
- Files are prefixed with `full_`, `mini_`, `preview_`

**Output Files:**

All three files use the same base name with different prefixes:
- `full_{basename}.json` - Complete dataset (identical to original)
- `mini_{basename}.json` - First 3 array items only
- `preview_{basename}.json` - First 3 items with strings truncated to 200 chars

**Tips:**
- Input JSON must have a top-level array structure
- String truncation is recursive (applies to nested objects and arrays)
- Use preview files for quick inspection without reading large datasets
- Use mini files for developing/testing code before running on full dataset

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [4] SKILL-INPUT — aii-python · 2026-06-18 10:51:34 UTC

The agent loaded the **aii-python** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-python
description: Python coding standards for experiment and evaluation scripts. Covers environment setup, logging, error handling, and code structure.
---

## Environment Setup

- Python 3.12+
- **NEVER use `pip` or `.venv/bin/pip`** — they are not installed. Use `uv` for ALL package operations:
  ```bash
  uv venv .venv --python=3.12
  source .venv/bin/activate  # or: .venv/bin/python script.py
  uv pip install pandas loguru  # NOT: pip install
  ```
- Create `.toml` file with dependencies, create uv `.venv` and activate it
- NO inline dependencies (no `# /// script` headers)

## Logging

Use `loguru` for all logging. Add a file sink alongside stdout.

```python
from loguru import logger
import sys

logger.remove()  # Remove default handler
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")
```

Rules:
- Log every major step (data loading, processing start/end, results)
- If applicable, log every LLM API call input and output
- Truncate long outputs in logs (add truncation logic for potentially large strings)
- Use `logger.error()` in except blocks (traceback auto-captured)

## Error Handling

- Wrap major operations in try/except blocks
- Use `@logger.catch(reraise=True)` decorator on main functions — without `reraise=True`, the script exits 0 even on uncaught exceptions, hiding failures from downstream consumers
- Use explicit exception types, not bare `except:`
- Never silently swallow exceptions — always log them

```python
@logger.catch(reraise=True)
def main():
    try:
        data = load_data(path)
    except FileNotFoundError:
        logger.error("Data file not found")
        raise
    except json.JSONDecodeError:
        logger.error("Invalid JSON in data file")
        raise
```

## Code Structure

- Use `pathlib.Path` for file operations: `Path("data/input.json").read_text()` not `open(...).read()`
- Use type hints for function signatures
- Use keyword arguments for functions with more than 4 parameters
- No hardcoded paths — derive from script location or accept as arguments

## Script Pattern

Standard pattern for experiment/evaluation scripts:

```python
#!/usr/bin/env python3
"""Brief description of what this script does."""

from loguru import logger
from pathlib import Path
import json
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

@logger.catch(reraise=True)
def main():
    # Load data
    data_path = Path("full_data_out.json")
    logger.info(f"Loading data from {data_path}")
    data = json.loads(data_path.read_text())
    logger.info(f"Loaded {len(data['examples'])} examples")

    # Process
    results = []
    for i, example in enumerate(data["examples"]):
        try:
            result = process(example)
            results.append(result)
        except Exception:
            logger.error(f"Failed on example {i}")
            continue

    # Save output
    output = {"examples": results}
    Path("method_out.json").write_text(json.dumps(output, indent=2))
    logger.info(f"Saved {len(results)} results")

if __name__ == "__main__":
    main()
```
````

### [5] SKILL-INPUT — aii-file-size-limit · 2026-06-18 10:51:34 UTC

The agent loaded the **aii-file-size-limit** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

```
---
name: aii-file-size-limit
description: File size check procedure for splitting oversized output files. Use after generating JSON output files to check and split files exceeding the provided size limit.
---

## File Size Check

After generating output files, run `ls -lh` to check sizes. If ANY file exceeds the provided file size limit:

1. Create directory with same base name (e.g., `data_out/` for `full_data_out.json`)
2. Split into parts under the limit named: `full_data_out_1.json`, `full_data_out_2.json`, etc.
3. Place parts in directory (e.g., `data_out/full_data_out_1.json`, `data_out/full_data_out_2.json`)
4. Delete the original oversized file
5. Update the script to read from split files: `for f in sorted(glob.glob('data_out/full_data_out_*.json')): data.extend(json.load(open(f)))`
6. For each split part, generate its own mini/preview versions with the json skill's format script
```

### [6] SYSTEM-USER prompt · 2026-06-18 11:11:10 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_evaluation_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_evaluation_1/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_evaluation_1/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_evaluation_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_evaluation_1_idx3
type: evaluation
title: >-
  Iter-8 Integrity-Lock Eval: De-Inflate the Edit Headline, Lay Both Forget Instruments Side-by-Side, Show Concentration>Absorption
  Predicts the Win, and Lock the Georgia +0.561 Retraction
summary: >-
  Pure-CPU, $0, read-only re-analysis over the EXISTING iter-6/7 edit data (art_Cgk9ETiZfvtl, art_ZxVw0e4seBq3, art_3WXWsaSoGMnK).
  Following the project integrity-lock pattern (COMPUTE-from-source then COMPARE-to-stored, never overwrite), it produces
  GEN_PAPER_TEXT drop-in numbers that are robust to any truncation of the new iter-8 experiments: (1) the DE-INFLATED lead
  KG-vs-strongest-ungated-dense (+1.00 on 'large') reconciled against the inflated +1.58-vs-footprint-gated with its beta~2.97
  over-erasure stats; (2) BOTH meaningful-forget instruments (gold-completion-drop AND frozen sub-probe-drop) per case/operator
  side-by-side, with an instrument-disagreement metric proving next-token-KL matching != behavioral matching; (3) a per-case
  CONCENTRATION proxy correlated with the win/meaningful-forget outcome vs the absorption-regime label (concentration predicts,
  absorption does not); (4) the consolidated Georgia +0.561 RETRACTION (iter-6 win sat at a near-NOOP operating point); plus
  an operator-divergence flag (3%-global-footprint vs 95%-X-rate gate) the new experiments must unify. Emits eval_out.json
  (exp_eval_sol_out) with metrics_agg, per-case datasets, cross_checks, and cross-checked drop-in paper_wording.
runpod_compute_profile: cpu_heavy
metrics_descriptions: |-
  PURE-ANALYSIS INTEGRITY LOCK. No GPU, no model load, no LLM calls ($0). Read-only over three stored experiment outputs. EVERY headline value is RECOMPUTED from source columns, then COMPARED to the stored expectation; mismatches are reported in metadata.cross_checks with an explanatory note and NEVER overwritten (this mirrors art_w7p8du2N1f0Y / art_-k4Yg-l4NaNO). Use a fixed seed (1234) for every bootstrap so results are deterministic and re-checkable.

  === INPUTS (exact paths; load full_method_out.json, fall back to method_out.json if absent) ===
  - D1 = art_Cgk9ETiZfvtl @ /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_7/gen_art/gen_art_experiment_1/full_method_out.json. Use metadata.per_case[*] (5 cases: target_subcontext in {Georgia, large, Jordan, United States, insult}), metadata.summary, datasets.gated_dense_per_prompt (288 rows; columns predict_kg_abl/predict_dense_sub_gated/predict_dense_sub_abl/predict_dense_whole_abl/predict_noop + per-operator judged utilities + NOOP-identical + model-internal signals), datasets.kg_vs_gated_per_case (5 rows). Also read this dir's method.py to extract the EXACT joint-utility formula, paired_bootstrap_diff, completion_drop, fit_sub_probe and calibrate_gate_tau definitions so recomputation is faithful.
  - D2 = art_ZxVw0e4seBq3 @ .../iter_7/gen_art/gen_art_experiment_2/full_method_out.json. Use metadata.downstream[*] (3 cases: Amazon, Bush, Georgia-control), datasets.downstream_edit_per_prompt (90 rows), datasets.downstream_edit_per_case, metadata.screen_table (per-entity absorber_precision/hole/jaccard for Amazon/Bush/Cook).
  - D3 = art_3WXWsaSoGMnK @ .../iter_6/gen_art/gen_art_experiment_1/full_method_out.json. Use the Georgia kg_vs_dense_per_case entry (joint_diff_CI_KG_vs_SUB, matched_target_forget_kl, fork_verdict) and datasets.unlearn_per_prompt for Georgia if a recompute is needed.

  === GROUP A - DE-INFLATION (M1''' + M3''' lead number) ===
  A1. Mean joint utility per operator per D1 case: recompute from gated_dense_per_prompt judged-utility columns using the exact joint formula read from method.py (joint = judged retain-utility combined with fluency). Cross-check computed kg/gated/sub_joint_utility_mean against stored metadata.per_case[*].{kg_joint_utility_mean, gated_joint_utility_mean, sub_joint_utility_mean}. Expected for large: KG=1.8704, GATED=0.2870, SUB=0.8704.
  A2. Paired-bootstrap (B=10000, seed 1234, over preservation prompts) joint diffs per case: (i) DE-INFLATED LEAD = KG-ABL minus DENSE-SUB-ABL (ungated, strongest dense); (ii) INFLATED = KG-ABL minus DENSE-SUB-ABL-GATED. Cross-check (i) against stored joint_diff_CI_KG_vs_SUB_secondary and (ii) against joint_diff_CI_KG_vs_GATED. Expected for large: lead = +1.000 CI[0.787,1.213] (n=36); inflated = +1.583 CI[1.361,1.787]. Verify the reconciliation 1.8704-0.8704=+1.00 and 1.8704-0.2870=+1.58 hold to <1e-3.
  A3. Over-erasure stats for large (and report for all cases): gated retain-collateral KL = retain_collateral_kl_gated_mean (0.290) vs ungated SUB retain_collateral_kl_sub_mean (0.021) -> over_erasure_ratio = 0.290/0.021 ~= 13.8x; the beta the gate was driven to = scale_gated_beta (2.967) vs scale_sub_beta (0.649); gated_vs_ungated_collateral_CI (diff -0.269, excl_0 true => gated has MORE collateral than its OWN ungated form). Also report collateral_diff_CI_KG_vs_GATED (+0.290) and collateral_diff_CI_KG_vs_SUB_secondary (+0.021).
  A4. Emit per-case de-inflation rows {case, kg/gated/sub joint means, lead_diff+CI, inflated_diff+CI, gated_collateral, sub_collateral, over_erasure_ratio, scale_gated_beta, scale_sub_beta, gated_vs_ungated_collateral_excl_0}. metrics_agg gets de_inflated_lead_large=+1.00 (with CI), inflated_gap_large=+1.58 (with CI), over_erasure_ratio_large~=13.8.

  === GROUP B - BOTH FORGET INSTRUMENTS SIDE-BY-SIDE (M4''') ===
  B1. For every D1 case x operator at the matched point, tabulate the TWO behavioral instruments: (a) gold-completion-drop = metadata.per_case[*].completion_drop_matched[op].drop_vs_noop with drop_ci/excl_0; (b) frozen sub-probe positive-rate drop = subprobe_drop[op].drop (and NOOP pos_rate, auc). Build one row per (case, operator) with both numbers + their CI/excl_0.
  B2. Instrument-disagreement metric, per case, on the decisive KG-vs-GATED contrast: completion_contrast = completion_drop[KG]-completion_drop[GATED]; subprobe_contrast = subprobe_drop[KG]-subprobe_drop[GATED]. Report sign_divergence = (sign(completion_contrast) != sign(subprobe_contrast)) and the signed magnitudes. For large this fires: completion favors GATED (KG 0.072 vs GATED 1.080 => completion_contrast=-1.008) while sub-probe favors KG (KG 0.417 vs GATED 0.0 => subprobe_contrast=+0.417) -> sign_divergence=TRUE. Also compute, per case, a rank-disagreement (Spearman or Kendall-tau between the two instruments' operator orderings over {KG,GATED,SUB}).
  B3. Quantify 'next-token-KL matching != behavioral matching': all operators are scaled to the SAME matched_target next-token KL, yet at that point completion_drop and subprobe_drop differ sharply across operators (e.g. large: KL-matched but completion_drop spans 0.072..1.080 and subprobe_drop spans 0.0..0.917). Report, per case, the across-operator spread (max-min) of each behavioral instrument at the KL-matched point as the divergence evidence, and recommend (for paper_wording) matching operators on a BEHAVIORAL measure (sub-probe drop or completion accuracy) rather than next-token KL. Flag that the load-bearing large completion CI is over only n=4 probes (RIGOR caveat) -- read drop_ci.n.
  B4. metrics_agg gets instrument_disagreement_cases (list of cases with sign_divergence=TRUE; expect {large}), and the large KG-vs-GATED contrast pair (-1.008 completion, +0.417 sub-probe).

  === GROUP C - CONCENTRATION-vs-ABSORPTION PREDICTOR (M3''' decisive descriptive) ===
  C1. Assemble a pooled case table across D1 (large, Georgia, Jordan, United States, insult) and D2 (Amazon, Bush). For each case read: absorber_precision (per-sub-context precision), gate_footprint_used / gate_target_footprint (firing footprint f_kg), firing_jaccard_with_parent, max_forget_kg (single-latent next-token-KL ceiling = edit leverage), regime label ('absorption' vs 'co-firing'), and outcomes: win_binary = (fork_verdict==KG_BEATS_GATED_DENSE...), meaningful_forget_binary = kg_can_forget (D1) / non-trivial-forget (D2), adv_continuous = joint KG-vs-GATED diff. For D2 use downstream[*] fields (gate_calibration, max_forget_kg, fork_verdict, joint_diff_CI_KG_vs_GATED) and screen_table absorber_precision.
  C2. CONCENTRATION PROXY (primary): concentration = absorber_precision * (1 / f_kg) read from stored fields (per the direction: per-sub-context precision x inverse footprint). ALSO compute two robustness variants and report all three: (v2) absorber_precision * max_forget_kg (precision x single-latent leverage), (v3) absorber_precision * (1 - firing_jaccard_with_parent) * sub_probe_max_drop. Rank/z-score each case under each proxy. The qualitative pattern to confirm: concentrated cases (large prec 1.0, Amazon prec 0.99/max_kg 1.14, insult high-precision co-firing) WIN; distributed cases (Georgia/Jordan country sense, US co-firing) LOSE -- crossing BOTH regime labels.
  C3. PREDICTIVE COMPARISON: compute point-biserial (proxy continuous vs binary outcome) and Spearman (proxy vs adv_continuous) for (a) each concentration proxy and (b) the absorption-regime binary label, each with a bootstrap CI (B=10000, seed 1234, resampling cases). predictive_delta = corr(concentration_proxy, outcome) - corr(absorption_label, outcome). EXPECT concentration to track win/meaningful_forget better than the absorption label (absorption label is near-uninformative because wins/losses cross it). Because n is small (~7 cases) this is EXPLICITLY descriptive: report the delta + CI but label it 'descriptive, small-n' in the row and in paper_wording. Cross-check the absorption-mean-vs-cofiring-mean comparison the paper currently leans on: adv_absorption_mean (1.583) vs adv_cofiring_mean (0.372) from metadata.summary, and note it is a 1-case-vs-2-case-mean (thin/circular) basis -- the per-case concentration correlation supersedes it.
  C4. metrics_agg gets concentration_vs_absorption_predictive_delta (primary proxy, with CI), the per-proxy correlations, and a boolean concentration_outpredicts_absorption.

  === GROUP D - GEORGIA +0.561 RETRACTION (M1''' carry / M6) ===
  D1. From D3 recompute (or read+cross-check) the iter-6 Georgia KG-vs-SUB joint = +0.5606 CI[0.318,0.811] n=44 at matched_target_forget_kl=0.0517. If recomputing from unlearn_per_prompt, use the method.py joint formula; else cross-check the stored CI.
  D2. From D1 (iter-7) read the near-NOOP evidence at/near that operating point for Georgia: max_forget_kg=0.0647 (17-30x smaller than dense ceilings), noop_identical_fraction.FORGET['KG-ABL']=0.889, subprobe_drop['KG-ABL'].drop=0.075, completion_drop_matched['KG-ABL'].drop_ci.excl_0=false, fork_verdict=NO_MEANINGFUL_FORGET, and the iter-7 KG-vs-GATED Georgia adv=+0.174 / KG-vs-SUB=+0.197 (vacuous, KG barely edits).
  D3. RETRACTION ROW + STATEMENT: the iter-6 +0.561 'win' sat at a near-NOOP operating point (KG won by barely editing, and also barely forgot); it is retracted/recontextualized as clean low-collateral PARTIAL suppression, not meaningful unlearning. metrics_agg gets retraction_iter6_georgia_adv=+0.561, retraction_iter6_matched_kl=0.0517, retraction_iter7_max_forget_kg=0.0647, retraction_noop_identical=0.889, retraction_subprobe_drop=0.075, retraction_status='RETRACTED_NEAR_NOOP'.

  === GROUP E - OPERATOR-DEFINITION DIVERGENCE FLAG (MINOR 4 / M1''' unify) ===
  E1. Cross-check the two 'footprint-matched gated dense' operators are NOT identical: D1 = global-neutral-pool footprint gate (calibrate_gate_tau; gate_tau~=101, gate_footprint_used~=0.025-0.028, gate_target_footprint~=0.014-0.03, ~3% global firing). D2 = gate_calibration.method=='footprint_match_clamped' on X-POSITIVE firing rate clamped ~0.95 (gate_fire_rate_X~=0.9467, gate_fire_rate_sibling~=0.045). Set metrics_agg.operator_divergence_flag=TRUE with both calibration descriptors and a note that the iter-7 headline aggregates a 3%-global-footprint comparison (large) with a 95%-X-rate comparison (Amazon); the new iter-8 experiments must unify into ONE gate operator (or document any per-case clamp in-table).

  === OUTPUT (eval_out.json, schema exp_eval_sol_out; validate full/mini/preview <100MB via aii-json + aii-file-size-limit) ===
  - metrics_agg: {de_inflated_lead_large, inflated_gap_large, over_erasure_ratio_large, instrument_disagreement_cases, large_kg_vs_gated_completion_contrast, large_kg_vs_gated_subprobe_contrast, concentration_vs_absorption_predictive_delta, concentration_outpredicts_absorption, retraction_* fields, operator_divergence_flag, absorption_mean_vs_cofiring_mean_basis_note}.
  - datasets: de_inflation_per_case (>=5 D1 rows + D2 rows), both_instrument_per_case_op (one row per case x {KG,GATED,SUB} with completion_drop+CI and subprobe_drop), concentration_predictor_per_case (~7 rows with proxies+outcomes+labels), retraction_per_case (Georgia row), operator_divergence (2 rows). Each dataset row must carry predict_* / value STRING fields if the project schema requires non-null string predictions (mirror the iter-5/6 validator gotcha: every example needs a predict_* string).
  - metadata.cross_checks: array of {name, computed, stored, abs_diff, rel_diff, match (bool at tol: 1e-3 for point stats; CI-overlap for bootstrap), note}. Include at minimum the A1 utility means, A2 lead/inflated diffs+CIs, D1/D2 collateral CIs, the iter-6 Georgia +0.561, and the summary adv_absorption/adv_cofiring means.
  - metadata.paper_wording: drop-in strings (cross-checked) for: (W1) de-inflated lead '+1.00 vs the strongest ungated dense on large (CI[0.79,1.21]), with +1.58 vs a footprint-matched gate reported only as a robustness check handicapped by beta~3 over-erasure (gated collateral 0.29 = 13.8x its own ungated 0.021)'; (W2) instrument disagreement 'at the next-token-KL-matched point the two forget instruments disagree in sign for large (completion favors the gated dense by 1.01, frozen sub-probe favors KG by 0.42), so KL-matching does not equalize behavioral forgetting; operators should be matched on a behavioral measure'; (W3) concentration finding 'the edit-win predictor is latent concentration/precision, not absorption: wins span an absorption case (large) and a co-firing case (insult), losses are distributed senses (Georgia/Jordan); a precision-x-inverse-footprint proxy tracks the outcome where the absorption-regime label does not (descriptive, n~7)'; (W4) retraction 'the iter-6 Georgia +0.561 win sat at a near-NOOP operating point (max single-latent forget KL 0.065, NOOP-identical on 89% of forget prompts, frozen sub-probe drop 0.075); it is retracted as low-collateral partial suppression, not meaningful unlearning'; (W5) operator unification note.

  === FAILURE / EDGE HANDLING ===
  - If a per-prompt judged-utility column is missing or the joint formula cannot be reproduced exactly, fall back to cross-checking the stored *_joint_utility_mean and *_diff_CI directly and mark the cross_check note 'stored-only (recompute unavailable)'; do not fabricate.
  - If a recomputed bootstrap CI does not overlap the stored CI, record match=false with a note (seeding/resample-unit difference) -- report, never overwrite.
  - Some D1 cases (insult, US) are regime='co-firing'; keep them in Group C (they are load-bearing for the concentration claim) but exclude US/insult from any absorption-only aggregate, matching metadata.summary.us_excluded_gate.
  - D2 Amazon/Bush use the 95%-X-rate gate, so their joint diffs are NOT directly comparable to D1's 3%-global-footprint diffs; carry them as supporting concentration points flagged with the operator note (Group E), not pooled into the D1 lead CI.
  - Keep all three output variants <100MB; per-prompt source datasets are tiny (288/90/~hundreds rows) so full retention is fine.
metrics_justification: >-
  These metrics are exactly the four reviewer-gating integrity issues (R1 de-inflation, R3 concentration-not-absorption, R4
  operator divergence, R5 instrument rigor) reduced to arithmetic over data that ALREADY exists, so GEN_PAPER_TEXT gets defensible
  drop-in numbers no matter how the new iter-8 edit experiments turn out. (1) The DE-INFLATED lead matters because the abstract
  currently leads with the largest, least-defensible gap: the +1.58 is KG beating a gated dense that was driven to beta~2.97
  over-erasure (its own collateral 0.29 is 13.8x its ungated 0.021), i.e. a handicapped control. Recomputing KG-minus-strongest-ungated-dense
  (+1.00, CI[0.79,1.21]) from the stored per-prompt utilities, and proving the +1.58/+1.00 reconciliation against the stored
  utility means, gives the paper an honest headline and pre-empts the #1 blocker. (2) Laying BOTH forget instruments side-by-side
  and quantifying their sign-disagreement at the KL-matched point is the only way to honestly support 'meaningful forget':
  the completion-drop and sub-probe-drop instruments rank KG vs the gated dense in OPPOSITE directions for the load-bearing
  large case, which both proves the forget is real on the behavioral sub-probe AND shows that matching on next-token KL does
  not equalize behavior -- a rigor fix the paper must state, not hide. (3) The concentration-vs-absorption predictor is the
  decisive evidence reframe: the wins cross both regime labels (absorption 'large' wins, co-firing 'insult' wins; absorption
  'Georgia/Jordan' lose), so a per-case precision-x-inverse-footprint proxy correlating with the outcome better than the absorption-regime
  label directly substantiates 'the win traces to concentration, not the absorption structure the method discovers' and retires
  the thin 1-vs-2-case absorption_exceeds_cofiring aggregate. It is correctly scoped as small-n descriptive. (4) Consolidating
  the Georgia +0.561 retraction closes the loop on a now-known-misleading prior headline by showing, in one row, that the
  win sat at a near-NOOP operating point (tiny max forget KL, 89% NOOP-identical, sub-probe barely moved) -- protecting the
  paper's integrity. The operator-divergence flag surfaces the 3%-global-footprint vs 95%-X-rate inconsistency the new experiments
  must unify. Because the whole artifact is a read-only, $0, deterministic recompute-and-cross-check, it is immediately runnable
  and fully robust to truncation of the expensive new GPU experiments, which is precisely its strategic value as the always-produced
  clean deliverable.
</artifact_plan>

<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
id: art_3WXWsaSoGMnK
type: experiment
title: 'M1'': KG single-absorber unlearning vs a sub-context-targeted dense baseline'
summary: >-
  M1' replaces the near-tautological WHOLE-PARENT dense comparator of iter-5 with a STRONGER, sub-context-targeted dense baseline
  u_sub = diff-of-means(target-sub-context-positive, sibling-positive in the same parent context), fit on a DISJOINT fold
  from the per-sub-context labels the testbeds carry. The decisive downstream test is selective sub-concept UNLEARNING: at
  MATCHED forget-quality (next-token KL on held-out FORGET windows, matched_target = 0.8*min(maxKG,maxSUB)), it compares KG-ABL
  (ablate one KG-named absorber, h -= lambda*z_l*W_dec[l], gated by the latent's own sparse firing) against the DECISIVE DENSE-SUB-ABL
  (erase u_sub) and a clearly-labeled SECONDARY DENSE-WHOLE-ABL (erase the whole-parent diff-of-means), plus RAND and (M7)
  KG-ABL-UNIT. The joint (retain-utility x fluency) outcome is scored by an AxBench-style OpenRouter judge (anthropic/claude-haiku-4.5)
  with paired-bootstrap KG-vs-SUB CIs (B=10000), curve-dominance, and model-internal corroboration (continuation PPL + retain
  next-token KL). Per-case FORK verdict: KG_BEATS_USUB (joint CI excl 0 favoring KG AND a 2nd-family judge CI also excl 0),
  KG_MATCHES_USUB_LABEL_FREE (CI includes 0 - KG matches u_sub WITHOUT needing the labels), or KG_LOSES_TO_USUB. RESULTS (full
  run, both judges, $0.53/1459 calls): GATE PASSED. The two ABSORPTION cases are both KG_BEATS_USUB - taxonomic Georgia(16009)
  and first_letter large(8463) - each with u_sub localizing better than whole-parent and the M7 win tracing to the SINGLE
  discovered absorber (the multi-member K-track unit only adds collateral); human-proxy spot-checks pass. Folded-in modules:
  (M1') u_sub localization validation is CURVE-BASED over the achievable dense forget range (the KG-pinned matched point is
  tiny because KG single-latent next-token KL has a small ceiling, so a single-point check is mis-specified) - this DELETES
  the false 'a single dense hyperplane cannot localize' framing and reframes KG's edge as sparse-firing GATING (token footprint
  -> 0 for absorption), NOT the dense direction failing to localize; (M5) United States(846) is a ROUTER FALSE-NEGATIVE reclassified
  to co-firing - its absorber footprint is low/surgical-looking but the small parent recall-hole (0.197) flags co-firing,
  so it is moved out of the absorption gate; (M6) a second different-family judge (openai/gpt-4o-mini) with Cohen kappa +
  Pearson/Spearman utility correlation keeps a KG win only if its CI also excludes 0, plus a deterministic $0 human-proxy
  check that KG-ABL preserves sibling tokens while DENSE-WHOLE corrupts them; (M7) unit-vs-single ablation. Toxicity_insult
  is the co-firing case where KG is NOT surgical (footprint 0.166, firing-Jaccard 0.882, no recall-hole - the regime mechanism
  holds); it registers KG_BEATS_USUB on the LLM-judge joint but the $0 model-internal joint does NOT corroborate it (CI includes
  0) and u_sub itself fails to localize in co-firing, so it is reported as a weak judge-only edge, not a surgical win, and
  is not counted toward the gate. A per-case mi_corroborates_fork flag is reported (Georgia/US True; large/toxicity False
  - the noisier model-internal proxy is inconclusive there even though both LLM judges agree). Reuses the iter-4/iter-5 Gemma-Scope
  L12/16k JumpReLU engine via core.py (only the multi-latent abl_latent generalization for M7 + WORK repoint). Single GPU
  (NVIDIA L4); $0 model-internal, <$2 LLM judges (hard cap $10). All outputs validate against exp_gen_sol_out: unlearn_per_prompt
  (per (case,role,prompt) with predict_kg_abl / predict_dense_sub_abl / predict_dense_whole_abl / predict_rand / predict_noop
  continuations + both judges' utilities) and kg_vs_dense_per_case (fork verdicts + all decisive CIs).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_experiment_1
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Dependency 2 ---
id: art_Cgk9ETiZfvtl
type: experiment
title: M1'' Gated-Dense Control + Honest Forget Test of KG Single-Absorber Suppression
summary: |-
  iter-7 M1'' decisively stress-tests the auditability-first two-track CCRG claim that ablating ONE KG-named absorber latent (KG-ABL) is a better unlearning handle than a dense baseline. It adds the FAIR control iter-6 lacked and an honest operating-point protocol.

  NEW OPERATOR (core.py): DENSE-SUB-ABL-GATED (kind='erase_dir_gated') erases the sub-context diff-of-means u_sub ONLY where |h.u_sub|>tau; tau is calibrated (calibrate_gate_tau) so the gate's global firing fraction over a neutral pool equals the KG absorber's token footprint f_kg. This removes the iter-6 confound (KG edits ~1-3% of tokens; ungated u_sub edits every token). tau threaded through make_edit_hook/forward_pos_logprobs/behavioral_curve/side_effects/generate_under_edit/last_tok_logprobs. FIVE operators at the SAME swept matched forget: NOOP, KG-ABL, DENSE-SUB-ABL-GATED (decisive), DENSE-SUB-ABL (ungated, iter-6, secondary), DENSE-WHOLE-ABL (secondary), +RAND +KG-ABL-UNIT (M7).

  HONEST OPERATING POINT: per case we report max_forget_{kg,sub,gated,whole} (KG's next-token-KL ceiling is 17-30x smaller than the dense directions'), NOOP-identical fraction (KG is NOOP-identical on ~0.89 of FORGET prompts for the country cases), full collateral-vs-forget curves, a gate footprint sweep {0.5,1,2,4}*f_kg, matched_target=0.8*min(max_kg,max_gated), and op_high=0.95*max_kg.

  MEANINGFUL-FORGET PROOF ($0, deterministic, the key addition): (a) completion-accuracy drop = drop in gold-token log-prob on hand probes (capital-of-Georgia->Tbilisi, large->L, etc) with bootstrap CI; (b) frozen 1-D-free sub-probe d_sub (AUC~1.0) scored on the REAL post-edit residual via read_resid_under_edit; meaningful_forget[op] = (completion CI>0) OR (sub-probe positive-rate drop>=0.1). Decisive pair KG-ABL vs DENSE-SUB-ABL-GATED via paired_bootstrap_diff (B=10000) on the joint (retain-utility x fluency) outcome under TWO OpenRouter judges (claude-haiku-4.5 + gpt-4o-mini).

  PER-CASE 3-WAY FORK: KG_BEATS_GATED_DENSE_AT_MEANINGFUL_FORGET / GATED_DENSE_CLOSES_GAP_DISCOVERY_IS_THE_VALUE / NO_MEANINGFUL_FORGET_SCOPE_TO_PARTIAL_SUPPRESSION. Aggregate requires absorption advantage to EXCEED co-firing advantage; a US-excluded gate counts only powered absorption cases.

  RESULTS (5 cases, 2109 judge calls, $0.80 << $3 target; overall=SPARSE_SAE_HANDLE_ESTABLISHED, absorption_exceeds_cofiring=True, adv 1.58>0.37): (1) first_letter_large (spelling absorber 8463) = KG_BEATS_GATED_DENSE: KG meaningfully forgets (sub-probe drop 0.42, completion 0.11) AND beats the footprint-matched gated dense by +1.58 joint under BOTH judges with strictly lower collateral (CI excl 0) and 1.0 curve dominance -- a discovered single SAE feature beats a labeled+footprint-matched dense control. (2) taxonomic_georgia (16009) and taxonomic_jordan (540) = NO_MEANINGFUL_FORGET: the single-latent ablation CANNOT remove the DISTRIBUTED country sense even at full strength (max_kg 0.065/0.114, sub-probe drop 0.07/0.0); this directly EXPOSES that iter-6's KG_BEATS_USUB headline sat at a near-NOOP operating point (KG won by barely editing). (3) taxonomic_us (846) = NO_MEANINGFUL (co-firing). (4) toxicity_insult (13367) = KG_BEATS_GATED (+0.47) but co-firing, so excluded from the absorption gate. The month case was dropped because the iter-5 homograph month dataset's *_data_out.json artifacts were never materialized on disk; absorption set = {Georgia, large, Jordan}.

  OUTPUT (exp_gen_sol_out, validated full/mini/preview, 0.8MB): metadata.per_case (all operating points, gate tau sweep + footprint used, NOOP-identical, completion/sub-probe drops, meaningful_forget, collateral & joint CIs KG-vs-GATED decisive + KG-vs-SUB/WHOLE secondary + gated-vs-ungated, full-range collateral curves, M5/M6/M7, fork_verdict); metadata.summary (3-way fork counts, adv_absorption/adv_cofiring, absorption_exceeds_cofiring, us_excluded_gate, overall_verdict); 11 honest_negatives; datasets gated_dense_per_prompt (288 rows, predict_kg_abl/predict_dense_sub_gated/predict_dense_sub_abl/predict_dense_whole_abl/predict_noop + per-op judged utilities + NOOP-identical + model-internal signals) and kg_vs_gated_per_case (5 rows). For the paper: the honest, feature-dependent conclusion is that the single-SAE-absorber handle genuinely beats a fair dense control ONLY for concentrated features (spelling); for distributed taxonomic/co-firing senses it is clean low-collateral PARTIAL suppression, not meaningful unlearning.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_7/gen_art/gen_art_experiment_1
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Dependency 3 ---
id: art_ZxVw0e4seBq3
type: experiment
title: Named-Entity Homograph SAE Absorption Screen + Gated-Dense Unlearning Downstream
summary: |-
  M2'' CONFIRMATORY (supporting, not load-bearing) experiment on Gemma-2-2b + Gemma-Scope L12/16k JumpReLU SAE (gating cosine 0.92, layer hidden_states[13]). It consumes the previously-unused named_entity_safety hierarchy (art_KNPsfjByyxiS) and reuses the iter-5/6 engine verbatim (core.py, method_iter6.py) with two genuinely-new pieces: a $0 absorption SCREEN (screen.py) and a NEW gated-dense edit operator 'erase_dir_gated' + a footprint-matched gate-calibration primitive (calibrate_gate) added to core.py.

  THESIS TESTED: feature absorption = LEXICAL HOMOGRAPHY (a suppressed 'named-entity/org' parent latent under a polysemous surface token), NOT safety/demographic semantics. A single coherent content-responsive parent latent (2768; xon-recall 0.99, probe AUC 1.0, not diffuse) was identified non-circularly (recall-only + >5% firing-floor). Per eligible entity the screen computes, with the absorber chosen on the diagnostic fit fold and every metric scored on the disjoint train fold: recall-hole, K-track-lite absorber, firing-Jaccard(parent,absorber), held-out precision, hole-coverage-gain with bootstrap CI, and a form-free decoder-probe-cosine oracle (Chanin/SAEBench, tau 0.025). 'absorption_structured' is gated on the firing-signature (the canonical iter-2..6 definition the Georgia positive control satisfies); the form-free decoder-projection oracle is reported separately and confirms 3/3 named-entity hits (it is spelling/concept-tuned and does not transfer to the taxonomic Georgia absorber, which would be wrongly rejected if it gated the verdict).

  PRIMARY RESULT ($0 screen): 3/5 eligible named-entity homographs are absorption-structured AND oracle-confirmed: Amazon (hole 0.61, jac 0.048, prec 0.99, gain 0.61 CI>0, dec-cos 0.12), Bush (0.79/0.021/1.00/0.79, 0.04), Cook (0.72/0.045/1.00/0.70, 0.03). Apple (hole 0.25) and King (0.42) are NOT structured (the parent detector fires on them). Four descriptive-only homographs (West, Bell, Hunt, Banks) show the relaxed signature (n<150). The Georgia self-check PASSED (the identical screen flags the canonical taxonomic absorber 16009 structured). This reinforces the settled iter-6 demographic null: absorption tracks lexical polysemy.

  CONDITIONAL DOWNSTREAM (supporting; both judges claude-haiku-4.5 + gpt-4o-mini, $0.35 total, 949 calls): at matched forget (0.8*min(maxKG,maxSUB)) with an edit-vs-NOOP forget delta, four operators KG-ABL / DENSE-SUB-ABL / DENSE-SUB-ABL-GATED (footprint-matched gate, balanced-acc 0.95-0.97) / DENSE-WHOLE-ABL. Amazon = KG_BEATS_GATED_DENSE (non-trivial forget: median KL 0.58, 58% prompts changed; KG-vs-GATED joint CI [0.41,1.08] and 2nd-judge CI [0.35,0.68] both exclude 0; curve-dominance 1.0) -> a genuine NAMED_ENTITY_HOMOGRAPH_WIN. Bush = KG_MATCHES_GATED_DENSE (non-trivial forget, label-free parity). Georgia control = NEAR_NOOP_NO_WIN (KG cannot forget non-trivially at the matched point; the iter-5/6 Georgia 'win' was lower-collateral, not strong forgetting). Notably the named-entity absorber 6846 is a STRONGER edit handle (max_kg 1.14) than the country absorber (0.064).

  VERDICTS: overall_verdict = SAFETY_ABSORPTION_HOMOGRAPH_CONFINED (demographic null unchanged); secondary_tag = NAMED_ENTITY_HOMOGRAPH_WIN_FOUND. 8 honest negatives recorded (confirmatory framing, oracle scope/decoder-tuning, Bush parity, Georgia NEAR_NOOP context, named-entity-vs-country edit-handle strength).

  DELIVERABLES: method.py (driver), screen.py (screen), core.py (engine + erase_dir_gated + calibrate_gate), method_iter6.py (reused engine). method_out.json (+ full/mini/preview, all PASS exp_gen_sol_out, <=208KB) holds metadata.{screen_table, breadth_count, georgia_sanity, parent_identification, downstream (per-case matched_target, max_forget_kg/sub/gated/whole, full_range_collateral_curve, edit_vs_noop_forget, gate_calibration, joint CIs KG-vs-{GATED,SUB,WHOLE} under both judges, curve_dominance), overall_verdict, secondary_tag, honest_negatives, llm_cost_usd}. Three datasets: named_entity_absorption_screen (19), downstream_edit_per_case (3), downstream_edit_per_prompt (90).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_7/gen_art/gen_art_experiment_2
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>

<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>

<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Web search (Serper), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-image-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
- aii-handbook-multi-llm-agents: Multi-LLM agent orchestration patterns
</skills>
</available_resources>

<available_domain_handbooks>
If your domain has a handbook, read the relevant skill file BEFORE working on that domain.

- **Multi-LLM Agents** — evaluation metrics, agent orchestration patterns, benchmark design
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Use aii-json skill's format script with `--input eval_out.json` to generate full, mini, and preview versions. If not in your workspace (see <workspace> above), copy them there. Run 'ls -lh' to verify these three files exist (DO NOT read them).
TODO 2. Apply aii-file-size-limit skill's file size check procedure (100MB limit) to eval_out.json and full_eval_out.json.
TODO 3. Ensure a `pyproject.toml` exists in your workspace with ALL dependencies pinned to the exact versions installed in your .venv (run `.venv/bin/pip freeze` to get them). This is required for reproducibility. The [project] section must include name, version, requires-python, and a dependencies list with pinned versions (e.g. `numpy==2.0.2`, not `numpy>=2.0`).
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "EvaluationExpectedFiles": {
      "description": "All expected output files from evaluation artifact.",
      "properties": {
        "script": {
          "description": "Path to eval.py script. Example: 'eval.py'",
          "title": "Script",
          "type": "string"
        },
        "full_output": {
          "description": "Full evaluation JSON file. Example: 'full_eval_out.json'",
          "title": "Full Output",
          "type": "string"
        },
        "mini_output": {
          "description": "Mini evaluation JSON file. Example: 'mini_eval_out.json'",
          "title": "Mini Output",
          "type": "string"
        },
        "preview_output": {
          "description": "Preview evaluation JSON file. Example: 'preview_eval_out.json'",
          "title": "Preview Output",
          "type": "string"
        }
      },
      "required": [
        "script",
        "full_output",
        "mini_output",
        "preview_output"
      ],
      "title": "EvaluationExpectedFiles",
      "type": "object"
    }
  },
  "description": "Evaluation artifact \u2014 structured output + file metadata.\n\nEvaluates both proposed and baseline methods with appropriate metrics.\nProduces eval.py and eval_out.json files.",
  "properties": {
    "title": {
      "default": "",
      "description": "Descriptive title (roughly 30-90 characters). Must describe content, NOT a status message.",
      "maxLength": 90,
      "minLength": 30,
      "title": "Title",
      "type": "string"
    },
    "layman_summary": {
      "default": "",
      "description": "One-sentence plain-language summary of what this artifact does, accessible to non-experts. Used only in the per-artifact README, not in downstream prompts.",
      "maxLength": 250,
      "minLength": 80,
      "title": "Layman Summary",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Summary for downstream artifacts: what this artifact provides",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/EvaluationExpectedFiles",
      "description": "All output files you created. Must include eval.py script plus full/mini/preview evaluation JSON files."
    },
    "upload_ignore_regexes": {
      "description": "Regex patterns for workspace paths that must NOT be published to the GitHub repo, matched against each file's path relative to this artifact's workspace root (POSIX form, e.g. 'cache/abc.json'). Applied ON TOP OF the deploy step's built-in exclusions. Use this for executor-specific caches, large transient intermediates, or content-addressed blob stores (e.g. a cache/ dir of thousands of hash-named files) that would bloat the repo. Examples: ['(^|/)cache/', '(^|/)\\\\.weight_cache/', '(^|/)checkpoints/']. Leave empty if every workspace file should be published.",
      "items": {
        "type": "string"
      },
      "title": "Upload Ignore Regexes",
      "type": "array"
    }
  },
  "required": [
    "out_expected_files"
  ],
  "title": "EvaluationArtifact",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [7] SYSTEM-USER prompt · 2026-06-18 11:12:32 UTC

```
<validation-feedback>
Attempt 1 failed validation.

Schema validation found 1 problem — fix ALL of them at once:
  - at `title`: 'Iter-8 Integrity-Lock Eval: De-Inflated Edit Lead, Dual Forget Instruments, Concentration>Absorption, Georgia Retraction' is too long (at most 90 characters, got 120)
Every required field must be present and every field type must match the schema.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```
