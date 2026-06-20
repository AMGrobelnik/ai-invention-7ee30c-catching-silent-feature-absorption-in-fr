# gen_art_experiment_1 — test_idea

> Phase: `invention_loop` · round 4 · `gen_art`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_experiment_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-17 21:59:17 UTC

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

<research_methodology>
Design experiments like a researcher, not a programmer running a script.

- Every method needs a meaningful baseline — the current standard approach, not a strawman.
- Control your variables. When comparing methods, hold everything else constant.
- Results need variance, not just point estimates. A single run proves nothing.
- Implement the proposed method and baseline side-by-side in the same pipeline to eliminate implementation-level confounds.
</research_methodology>

<task>
Implement the research methodology as a production-ready experimental system.
Adapt your implementation approach based on the hypothesis and domain requirements.
</task>

<critical_requirements>
- Fully implement the methodology described in hypothesis
- Use appropriate frameworks based on research domain
- Load and process data from the specified data_filepath
- Complete working systems
- Handle all edge cases, errors, and exceptions properly
- Always implement baseline comparison method
</critical_requirements>

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
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_1/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_1/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_1/results/out.json`
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
id: gen_plan_experiment_1_idx1
type: experiment
title: >-
  Expand the Measured KG-Guided Recall-Repair Loop + Member-Labeling to ALL Eligible Absorbed Sub-Contexts (Auditability Spine,
  M1a + M7-fraction)
summary: >-
  Make the measured auditability result the paper's load-bearing spine by EXPANDING the iter-3 KG-repair loop (currently 8
  significant repairs over taxonomic Georgia/Jordan/US + first-letter O/'our', D/'day') and member-labeling (67 members) to
  the FULL set of eligible absorbed sub-contexts across spelling (L/O/T/I/D words), homograph-taxonomic (all >=150-positive
  countries, testing Georgia/Jordan/US + flagged homographs Turkey/Chile/etc. for holes) and numeric (year/percent/currency/date/decimal/integer/comma_number/ordinal).
  Reuse the iter-3 pipeline at iter_3/gen_art/gen_art_experiment_3/method.py almost verbatim (SAE loader, JumpReLU encode>0,
  hook blocks.12.hook_resid_post, gating cosine>0.9, repair_loop, k_localization_check, LLM judge), adding: (1) BROAD KG re-derivation
  so every eligible hole sub-context gets a named covering absorber via the K-track greedy (not just the 3 canonical taxonomic
  edges); (2) a one-sided bootstrap p-value per repair + Benjamini-Hochberg FDR<=0.05 across the now-many repairs (multiplicity
  MUST live in-experiment); (3) the (k)-cannot-localize JTT/GEORGE check run for first-letter and numeric too, not just taxonomic;
  (4) member-labeling over EVERY member of every admitted unit INCLUDING all 15 members of each first-letter max-pool, with
  an ensemble-based confidence test reporting the FRACTION of the 15-wide pool that receives a confident, above-null-margin
  label. Honest negatives (KG repair tying random-addition, e.g. first-letter L/T words; numeric ties) reported verbatim.
  GPU; LLM target <$1, hard $10 cap.
runpod_compute_profile: gpu
implementation_pseudocode: |-
  =====================================================================
  GOAL: broaden art_lvYkaolutJG (iter-3 experiment_3) from 8 repairs / 67 members
  to the FULL eligible set, with BH multiplicity + 15-wide confident-label fraction.
  The iter-3 code already WORKS end-to-end; this is an EXPANSION, not a rewrite.
  =====================================================================

  # ---------- 0. SETUP / HARDWARE (aii-use-hardware, aii-long-running-tasks) ----------
  # pyproject.toml: torch, transformers, scipy, scikit-learn, numpy, loguru, requests,
  #   statsmodels (BH) OR hand-roll BH; huggingface_hub.
  # Detect GPU + compute capability. KNOWN RISK (iter-3 note): host GPU may be sm_120
  #   (Blackwell / RTX 5090) which the default torch wheel does not support ->
  #   try `uv pip install torch --index-url https://download.pytorch.org/whl/cu128`;
  #   if CUDA still unusable, FALL BACK TO CPU encoding (works, just slow) and
  #   reduce per-concept corpus caps (mini scaling) to stay in wall-clock budget.
  # bf16 on GPU; float32 on CPU. Memory-safe batching BATCH=16, MAXLEN=192.
  # Set RLIMIT_AS guard (reuse set_limits()). seed=1234 everywhere.

  # ---------- 1. PATHS / INPUTS (read-only) ----------
  ROOT = /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop
  D1 = iter_1/gen_art/gen_art_dataset_1/full_data_out.json   # first-letter L/O/T/I/D (art_dpYpjSn2Xvg3)
  D2 = iter_1/gen_art/gen_art_dataset_2/full_data_out.json   # numeric + taxonomic (art_t2uUbjSwpd3t)
  E1 = iter_2/gen_art/gen_art_experiment_1/method_out.json   # first-letter canonical units + 15-wide pool
  E3 = iter_2/gen_art/gen_art_experiment_3/method_out.json   # taxonomic canonical units/KG
  ITER3 = iter_3/gen_art/gen_art_experiment_3/{method.py, method_out.json}  # REUSE code + cross-check
  # Optionally reuse cached encodings if iter_3/.../cache/ holds residuals+CSR latents.

  # ---------- 2. SAE + MODEL + GATING (reuse iter-3 verbatim) ----------
  load JumpReLUSAE from gemma-scope-2b-pt-res params.npz (layer_12/width_16k/average_l0_82);
    encode(x) = (pre>threshold)*relu(pre); decode(z)=z@W_dec+b_dec; d_model=2304, d_sae=16384.
  load model google/gemma-2-2b (fallback unsloth/gemma-2-2b mirror, vocab 256000).
  determine_layer_idx(gate_rows): pick hidden_states idx (12/13/14) with lowest FVU -> expect 13.
  ASSERT reconstruction cosine > 0.9 (iter-3 got 0.9190 @ idx 13, L0~88); abort if not.
  encode_rows(rows): per row, select target token positions by char span / token idx,
    max-pool SAE latents over target tokens -> CSR [N,d_sae]; mean residual -> fp16 [N,d_model];
    report align (decoded-token==target). REUSE select_positions / _attach_span_fl / _attach_span_tax.

  # ---------- 3. PER-CONCEPT: RE-DERIVE UNIT + BROAD KG (the key new derivation) ----------
  CONCEPTS = ['taxonomic','numeric','L','O','T','I','D']
  for concept in CONCEPTS:
      rows = load concept rows (D2 taxonomic_absorption / D2 numeric_absorption / D1 first_letter_X)
      lat_csr, resid, _, align = encode_rows(rows, sae)
      # 3a. content-responsive set + per-latent firing precision (reuse content_responsive()):
      #     from TRAIN content_pair (x_on,x_off): cr = latents with mean(on-off)>shuffle-null95 & >0
      cr, prec, mean_R = content_responsive(A_on, A_off)
      cover[l] = #content-flip x_on the latent fires on (recall proxy)
      # 3b. ANCHOR = highest-cover precise (prec>=0.7) content-responsive latent,
      #     WITH the unsupervised parent-firing-floor validation (reject anchors that fire ~0%
      #     on the held corpus -> this is what flags letter-I anchor 1227 as spurious).
      anchor = argmax_{l in cr, prec[l]>=0.7, corpus_fire_rate(l)>floor} cover[l]
      if no anchor clears the corpus firing floor: mark concept spurious_anchor -> repair N/A (report).
      # 3c. BROAD K-TRACK KG: for EVERY eligible sub-context X (>= N_MIN_EVAL positives in the
      #     corpus-diagnostic/eval split), NAME the covering absorber. This generalizes the
      #     iter-3 3-edge taxonomic KG to all countries / all numeric types / all first-letter words.
      eligible_X = sub_contexts with >= 150 (tax/numeric) OR >= N_MIN_RELAX (first-letter) eval positives
      for X in eligible_X:
          r_anchor_sel(X) = anchor firing recall on X's SELECTION-split positives
          is_hole(X) = r_anchor_sel(X) <= HOLE_RECALL_MAX(0.60) OR < overall_anchor_recall - 0.10
          # K-track covering absorber for X (selected ONLY on selection split = non-circular vs eval):
          kg_absorber[X] = argmax_{l in cr, l!=anchor, jaccard(l,anchor)<0.10, prec_on_X(l)>=0.70}
                            (firing recall of l on X's SELECTION positives)
          record KG edge anchor --specializes--> kg_absorber[X]  (sub_context=X)
      # Cross-check the re-derived anchor / KG against E1/E3/iter-3 canonical_units (reproduction block).
      # For TAXONOMIC also keep the diagnostic-corroborated absorbers from E3
      #   non_triviality_passing_absorbers: Georgia=16009(prec .955), Jordan=540/8347, US=846.

  # ---------- 4. REPAIR-LOOP EXPANSION (reuse repair_loop(), extend variants + p-value) ----------
  # Split policy to MAXIMIZE eligible sub-contexts while staying doc-disjoint:
  #   tax/numeric: selection = corpus fold 'train', eval = corpus fold 'diagnostic' (>=150 each).
  #   first-letter: selection = corpus source_doc folds {0,1,2}, eval = folds {3,4}  (40% to eval,
  #     ~2x iter-3's single-fold eval -> recovers more words past N_MIN_RELAX=15). Doc-disjoint = no leak.
  for concept, for each hole/eligible X with kg_absorber[X]:
      base = anchor fires on X's EVAL positives;  base_recall = mean(base)
      # random-addition control: add each OTHER content-responsive latent (population, excl unit members),
      #   per-window mean detection rand_detect_perwin; gives random_gain distribution (p5/p50/p95).
      for variant in {'kg_ktrack': kg_absorber[X], 'kg_diagnostic': diag_absorber[X] (tax only, 3 named)}:
          kg_detect = base | (variant latent fires on X eval positives)
          gain_kg = mean(kg_detect) - base_recall
          pct = fraction of random-control latents whose gain < gain_kg
          diff_perwin = kg_detect - rand_detect_perwin
          CI = paired_bootstrap_diff(diff_perwin, B=10000)     # 95% percentile CI
          p_value = (1 + #{bootstrap_mean <= 0}) / (B+1)         # NEW one-sided p (H0: gain<=0)
          measured_success = CI.excl_0 and CI.diff>0
          if is_hole and not measured_success: append honest_negative verbatim
  # Collect ALL (concept,X,variant) -> {gain_kg, CI, percentile, p_value, n_eval, is_hole}.

  # ---------- 5. MULTIPLICITY: BENJAMINI-HOCHBERG (must live IN this experiment) ----------
  pvals = [v.p_value for every measured repair variant across ALL concepts]
  q = benjamini_hochberg(pvals)        # statsmodels.stats.multitest.multipletests(method='fdr_bh')
  attach q to each repair; n_survive_FDR05 = #{q <= 0.05}
  report: n_repairs_tested, n_holes, n_measured_success(uncorrected CI), n_survive_FDR05,
          and per-concept breakdown (spelling vs homograph-tax vs numeric).

  # ---------- 6. (k)-CANNOT-LOCALIZE  (reuse k_localization_check, run for ALL concepts) ----------
  for concept in {taxonomic, numeric, L, O, T, D}:    # skip spurious-anchor concepts
      JTT label-free group inference on dense resid: ERM probe -> upweight error/low-margin set -> retrain.
      project reweighted hyperplane w_k onto SAE decoder dictionary (cos = W_dec @ w_k / |W_dec|).
      report: projection_argmax_latent (expect = PARENT/anchor, NOT an absorber),
              single_latent_dominates (expect False),
              kg_absorber_projection_ranks per X (expect deep ranks, e.g. Georgia 4697 rank ~1728),
              conclusion: (k) classifies holes but exposes NO addable per-sub-context latent.

  # ---------- 7. MEMBER-LABELING EXPANSION + CONFIDENT-FRACTION (M7) ----------
  # Members to label = EVERY admitted-unit member, INCLUDING all 15 members of each first-letter
  #   max-pool (anchor + the 14 cover-eligible latents in E1 per_letter / sub_by_absorber), and
  #   the taxonomic/numeric anchor + named absorbers (k-track AND diagnostic).
  for each member m (role in {anchor,absorber}, ground-truth sub-context = m's modal firing sub-context):
      evidence = { logit_lens_top10 = topk(E @ W_dec[m]) decoded tokens,
                   top5 activating corpus windows with TARGET span marked **..** and SUB-CONTEXT WITHHELD }
      candidates = ['GENERAL parent'] + named sub-contexts for that concept's pool
      # ENSEMBLE confidence (NEW): J=3 judge calls per member; diversify by shuffling candidate
      #   option ORDER across calls (+ optionally 1 fallback model) so position bias differs.
      #   judge = OpenRouter anthropic/claude-haiku-4.5 temp 0 forced-choice integer index;
      #   fallbacks gemini-3.1-flash-lite, deepseek-v3.2; track cumulative cost; HARD STOP $10, target <$1.
      majority_label = mode over the J calls (remapped through each call's shuffled order)
      agree_rate = (#calls agreeing with majority)/J
      confident(m) = (majority_label is a SPECIFIC sub-context, not GENERAL/parse-fail)
                     AND agree_rate >= 2/3 AND agree_rate > per-member chance(1/n_candidates)  # above-null-margin
      correct(m) = (majority_label == ground_truth sub-context)
  # SCORING (reuse score_labeling + add fraction):
    agreement = mean(correct over valid members); shuffle-null over N_SHUFFLE=2000 perms of gt;
    gap = agreement - null_mean; bootstrap CI on gap (excl_0?); per_role_accuracy {anchor,absorber}.
    NEW: confident_label_fraction[concept] = #confident / #members;
         first_letter_15wide_confident_fraction[letter] = (#confident of the 15 pool members)/15;
         also report confident-AND-correct fraction. -> directly answers the '15-wide vs named' critique.

  # ---------- 8. VERDICT + OUTPUT (exp_gen_sol_out schema; reuse save_json) ----------
  metadata = { sae, model, gating_check, seed, B_boot, n_shuffles, llm_model,
     reproduction_crosscheck (anchor/KG vs iter-2/iter-3 canonical),
     repair_loop: per concept per X { recall_anchor_selection, recall_anchor_eval,
         random_gain{p5,p50,p95}, variants{kg_ktrack,kg_diagnostic}:{absorber_latent,
         recall_anchor_plus_kg, gain_kg, kg_percentile_vs_random, paired_bootstrap_CI,
         p_value, bh_q, measured_success}, is_hole, n_eval },
     multiplicity: { n_tested, n_holes, n_measured_success, n_survive_FDR05, per_concept_breakdown },
     k_localization_check: per concept,
     member_labeling: { per_member, scoring{agreement, null_mean, gap, gap_CI, per_role_accuracy},
         confident_label_fraction, first_letter_15wide_confident_fraction, llm_cost_usd, llm_calls },
     honest_negatives: [verbatim strings],
     verdict: { kg_utility_measured, n_survive_FDR05, member_labeling_above_null,
         fifteen_wide_confident_fraction_reported: true } }
  datasets = [ {dataset:'kg_repair_loop', examples:[one row per (concept,X,variant): input describes
                  the repair, output in {repair_significant, survives_FDR, tie_with_random}, metadata_*
                  = gain_kg, CI, percentile, p_value, bh_q, n_eval, is_hole}],
               {dataset:'member_labeling', examples:[one row per member: gt label, judge majority label,
                  confident flag, correct flag, role, concept]} ]
  save method_out.json; then aii-json -> validate exp_gen_sol_out + generate mini/preview; assert all <100MB.

  # ---------- KEY CONSTANTS (from iter-3, keep) ----------
  N_MIN_EVAL=30 (relax 15), HOLE_RECALL_MAX=0.60, B_BOOT=10000, N_SHUFFLE=2000,
  jaccard<0.10, precision>=0.70, FDR alpha=0.05, LLM target<$1 hard-stop $10.
fallback_plan: >-
  GPU / CUDA arch (highest-risk, seen in iter-3): if the host is sm_120 (RTX 5090/Blackwell) and the default torch wheel errors
  on CUDA init, (a) install the cu128 wheel `uv pip install torch --index-url https://download.pytorch.org/whl/cu128`; (b)
  if still broken, run encoding on CPU (correct, just slow) and CAP corpus rows per concept (e.g. --max_corpus 600 for first-letter;
  keep all >=150 tax/numeric eval positives since those are the load-bearing repairs) so the full run finishes in budget.
  Reconstruction-gating failure (cosine<=0.9): re-run determine_layer_idx over idx 12/13/14 and pick the lowest-FVU index
  (iter-3 -> 13); if none clears 0.9 the SAE/layer mapping is wrong — abort and report, do NOT analyze a mis-mapped SAE. Few-eligible-first-letter
  holes (per-word corpus windows are scarce — iter-3 skipped most L/T words at n_eval<15): this is expected and HONEST — the
  expansion volume is carried by taxonomic (>=150-positive countries) + numeric (8 sub-contexts each >=150); report first-letter
  coverage as-is (folds {0,1,2}/{3,4} split already ~2x iter-3's eval), and if still too sparse, additionally report a POOLED
  first-letter repair (absorber recall recovery on the union of that letter's hole-words) as a supplementary, clearly-labeled
  aggregate. Numeric shows no clean holes (parent already high-recall; memory: numeric diagnostic-unconfirmed): report numeric
  repairs as ties/honest-negatives — a clean negative that STRENGTHENS the homograph-scope story (absorption concentrates
  on polysemous tokens), not a failure. BH leaves zero survivors (worst case): still report the uncorrected CI-excluding-0
  repairs (the 8 known taxonomic+O/D repairs have huge gains 0.2-1.0 with tight CIs, so several WILL survive FDR<=0.05); if
  truly none survive, that is the declared 'auditability buys no robust fix' negative and is itself publishable. LLM judge
  unreachable / over budget: degrade ensemble J 3->1, then run --no_llm and report member-labeling as 'not scored (LLM unavailable)'
  while still emitting the repair-loop + (k)-localization spine (the load-bearing numeric result needs no LLM). LLM parse
  failures: re-ask once constrained ('respond with ONLY the integer'), then fall back to next model; count parse-fails, exclude
  from agreement, include in the confident-fraction denominator (a parse-fail member is NOT confident). Output >100MB: drop
  per-window text from datasets rows (keep in a capped sample), keep all numeric stats; use aii-file-size-limit to split if
  needed.
testing_plan: >-
  Stage 0 — SMOKE (minutes, $0): `uv run method.py --smoke` loads SAE + model, runs determine_layer_idx + gating; CONFIRM
  reconstruction cosine>0.9 (expect ~0.919 @ idx 13, L0~88) and align~1.0. If gating fails, STOP and fix layer mapping before
  anything else. Stage 1 — MINI PILOT one absorption concept, no LLM (~10 min, $0): `uv run method.py --concepts taxonomic
  --max_corpus 300 --no_llm`. CONFIRMATION SIGNALS that the pipeline reproduces iter-3 before expanding: re-derived taxonomic
  anchor == 3792 (anchor_match true); Georgia repair gain_kg ~0.8 with paired-bootstrap CI excluding 0 and percentile_vs_random
  ~0.99; Jordan ~0.71; US ~0.22; (k) projection_argmax_latent == 3792 (parent) with single_latent_dominates False and Georgia(4697)
  rank in the hundreds-to-thousands. If these three known repairs do NOT reproduce, the encoding/KG derivation has drifted
  — debug before scaling. Stage 2 — ADD numeric + BROAD KG + BH (~15 min, $0): `--concepts taxonomic,numeric --no_llm`; verify
  the broad-KG derivation names a covering absorber for every eligible sub-context, the one-sided p_value + BH q columns populate,
  and n_survive_FDR05 >= the known taxonomic repairs (>=4). Sanity-check numeric mostly ties random (honest negatives), confirming
  homograph-scope. Stage 3 — FIRST-LETTER (~15 min, $0): `--concepts L,O,T,I,D --no_llm`; verify letter-I is flagged spurious_anchor
  (anchor 1227 fires 0% corpus -> repair N/A) and that O/'our', D/'day' reproduce as significant repairs; record how many
  first-letter words clear the {0,1,2}/{3,4} eval split. Stage 4 — LLM MEMBER-LABELING on a small subset first ($<0.05): label
  one letter's 15-wide pool + taxonomic members with the J=3 ensemble; verify cost-per-call tracked, parse rate high, confident_label_fraction
  computed, and absorber per-role accuracy >> shuffle null (iter-3 absorbers 0.758 vs null 0.090). CHECK cumulative spend
  after this subset and extrapolate; abort to --no_llm if projected >$1. Stage 5 — FULL RUN (all concepts + full corpus +
  LLM ensemble): monitor logs (PID-based, never by name), watch cumulative LLM cost line each iteration vs the $1 target /
  $10 hard cap, and confirm final method_out.json validates against exp_gen_sol_out with mini/preview all <100MB. Final acceptance:
  (a) >=1 KG repair survives BH FDR<=0.05 across spelling+homograph-tax+numeric; (b) (k) exposes no addable per-sub-context
  latent on every concept; (c) member-labeling gap CI excludes 0 AND the 15-wide first-letter confident-label fraction is
  reported per letter; (d) all honest negatives (ties with random) emitted verbatim.
</artifact_plan>

<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
id: art_RidEJtBC7gPT
type: research
title: 'Two-Track CCRG Implementation Dossier: SAE Pipeline, 11 Baselines, Protocols'
summary: >-
  A decision-complete, code-ready implementation blueprint for the two-track Counterfactual Co-Response Grouping (CCRG) method
  on frozen Gemma Scope SAEs. Pins the SAE encoding pipeline (defensive from_pretrained loader, JumpReLU firing=encode>0,
  hook blocks.12.hook_resid_post), the C-track (signed soft-threshold + leidenalg RBConfigurationVertexPartition) and K-track
  (anchored greedy max-coverage) algorithm with all thresholds, all eleven baselines (a)-(k) as runnable specs (LEACE for
  f, SAEBench SCR/TPP for g/h, JTT/GEORGE/group-DRO for j/k), the AxBench steering protocol (harmonic-mean LLM-judge 0/1/2),
  a corrected model-diffing recipe (shared frozen pt-SAE on gemma-2-2b vs gemma-2-2b-it because no gemma-scope-2b-it SAE exists),
  the statistics plan (paired bootstrap, exact McNemar, MDE n_min=150, Holm-Bonferroni), and a fully-verified 30+ citation
  table including all four high-risk future-dated arXiv IDs (all resolve).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_research_1
out_dependency_files:
  file_list:
  - research_out.json

--- Dependency 2 ---
id: art_I2MrezW41iQo
type: research
title: Absorption Diagnostic + Pinned Datasets Dossier for Two-Track SAE Grouping
summary: >-
  Executor-ready dossier de-risking the C3 absorption spine and pinning every data/infra build for the two-track co-response
  SAE-grouping experiment. WP1 extracts the Chanin 2409.14507 absorption diagnostic verified against the lasr-spelling/sae-spelling
  code: parent latent = max ENCODER-cosine with an LR probe (+ k-sparse splits at f1-jump 0.03); absorber = largest-negative
  integrated-gradients ablation (IG steps=6) on the first-letter logit-diff m=g[y]-mean(g[incorrect]); decision thresholds
  probe_cos_sim_threshold=0.025 computed on the DECODER (sae.W_dec), ablation_delta_threshold=1.0, EPS=1e-8, 200-FN cap, topk=10;
  absorption_rate=num_absorptions/lr_probe_true_positives; valid only layers 0-17. It also supplies the strictly non-circular
  FORM-FREE version the paper itself gives in Appendix A.13 (and SAEBench implements as absorption_fraction): latent l absorbs
  iff tau_c < (a_hat_l . d_p)/(a . d_p) with a_hat_l = enc_act*W_dec[l] and d_p the parent-concept LR-probe direction trained
  on data DISJOINT from clustering -- works at all layers, no output logit needed, never used to form units. WP2 confirms
  absorption is empirically documented ONLY on first-letter spelling (LessWrong toy-models post; SAEBench eval id 'absorption_first_letter';
  Matryoshka/H-SAE only mitigate via the spelling metric), making Testbed-2 both a generality test and a novel empirical test;
  numeric-quantity hierarchy is recommended primary (taxonomic country alternative) with concrete non-triviality gates (parent
  recall >=0.60; >=1 absorber with firing-Jaccard<0.10, sub-context precision>=0.70, hole-coverage gain>=0.05 with bootstrap
  CI excluding 0) and an honest-null fallback that scopes C3 to spelling and routes generality through C1. WP3 pins HF datasets:
  s-nlp/paradetox (en_toxic_comment/en_neutral_comment, 19,744 rows, openrail++); google/civil_comments (text + 7 float32
  sub-attrs, 1.8M/97k/97k, CC0, 414.95MB -> subsample); tasksource/counterfactually-augmented-imdb (Text/Sentiment, no pair-ids
  -> acmi-lab GitHub for pairing, license unknown); CEBaB/CEBaB (full aspect-majority schema, license NOT on card = TODO);
  LabHC/bias_in_bios (hard_text/profession-int64-0-27/gender, 257k/39.6k/99.1k, 266MB, MIT, full alphabetical profession map).
  WP4 gives generation prompts + an independent LLM-judge rubric and verified June-2026 OpenRouter prices (generator google/gemini-3.1-flash-lite
  $0.25/$1.50 or deepseek/deepseek-v4-flash $0.09/$0.18; judge anthropic/claude-haiku-4.5 $1.00/$5.00), totalling ~$5.9-7.6
  for ~5,000 pairs with a hard $10 stop. WP5 captures sae-spelling get_alpha_tokens (convert_tokens_to_string then strip one
  leading space then all-alpha) and prompt template '{word} has the first letter:'; pins pile-uncopyrighted rev 3be9033 (2023-08-31,
  non-streaming); and SAE.from_pretrained(release='gemma-scope-2b-pt-res-canonical', sae_id='layer_12/width_16k/canonical',
  d_model=2304) + the 65k variant. CRITICAL model-diffing finding: NO gemma-scope-2b-it SAE exists anywhere (Google IT residual
  SAEs only for 9B) -> use the SHARED pt SAE on both gemma-2-2b and gemma-2-2b-it activations; both Google models are gated,
  use unsloth/gemma-2-2b(-it) mirrors. Full detail in research_report.md; every pinned fact and citation is in research_out.json.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_research_2
out_dependency_files:
  file_list:
  - research_out.json

--- Dependency 3 ---
id: art_dpYpjSn2Xvg3
type: dataset
title: >-
  First-Letter-Spelling Absorption Testbed (L/O/T/I/D): minimal pairs + frozen Pile corpus
summary: |-
  First-Letter-Spelling Absorption Testbed — the load-bearing dataset for the Two-Track Co-Response Grouping hypothesis (building reliable cluster-level units from individual SAE latents). Pure CPU/data artifact: NO SAE, no model weights, no GPU. 17,180 examples in 5 per-letter dataset groups (first_letter_spelling_{L,O,T,I,D}; L primary, O/T/I/D secondary; degenerate S/X excluded), schema exp_sel_data_out (full/mini/preview all PASSED).

  Three linked components per letter: (A) content_flip minimal pairs — (x_on,x_off) in an IDENTICAL carrier where x_on slots a word STARTING WITH the target letter and x_off a surface-matched word that does NOT (matched on char length, single-token-ness, Pile log-frequency); 1,750 pairs / 3,500 rows. Feeds the Tier-0 K-track anchored set-cover PROPOSAL pilot and the C3 absorber-recovery spine; reconstruct via metadata_pair_id and compute r_l=a_l(x_on)-a_l(x_off). (B) surface_flip pairs — (x_a,x_b) in an identical carrier, BOTH words start with the target letter but differ; 590 pairs / 1,180 rows; for the unit-level surface-invariance admission check (pooled response to surface flips ~0). (C) corpus_context — 12,500 real ~48-token windows (2,500/letter) from monology/pile-uncopyrighted @ rev 3be9033, each centred on a slot-eligible word-initial target-letter token with token_position annotated; plus a per-letter occurrence table (<=2,000 word-types) in dataset-level metadata — the substrate for iteration-2's form-free/Chanin (2409.14507) absorption diagnostic to locate false-negative absorbers (e.g. lion, London).

  Words are anchored in the real gemma-2-2b vocabulary (unsloth/gemma-2-2b ungated mirror, vocab==256000) via the exact sae-spelling get_alpha_tokens slot-eligibility recipe (word-initial '_' marker AND alpha). 7 carriers per content pair: sae-spelling spelling prompts (t_verbose '{word} has the first letter:', t_colon, t_icl with contamination-free ICL examples) + 4 word-class-agnostic mention carriers.

  Row schema is FLAT (exp_sel_data_out): input, output (first letter, uppercase), and metadata_* keys (dataset, letter, pair_id, pair_type, role, sub_context=the word covered, target_word, counterpart_word, template_id, label_starts_with_target, is_single_token, is_slot_eligible, first_letter, fold, word_char_span; corpus rows add source_doc_id, pile_revision, token_position, target_token_id, window_char_span, target_char_in_window). Pairs LINK via shared metadata_pair_id + metadata_role ({on,off}/{var_a,var_b}). Folds: minimal pairs by target_word, corpus by source_doc_id (5 folds, no leakage).

  Validation: the deterministic check is AUTHORITATIVE and reports 0 violations / 17,180 rows (flip property + input-span correctness are guaranteed by construction). The LLM judge (google/gemini-3.1-flash-lite, $0.12 total, < $3 cap) is a SECONDARY grammaticality/independent audit with pass rates 0.89-0.99 per (letter,pair_type); judge false-negatives are retained because the deterministic check governs drops. Corpus token_position verified EXACT (tok(input,add_special_tokens=False)[token_position]==target_token_id) on sampled rows. Frozen & reproducible: pinned tokenizer + Pile revision 3be90335..., seed 1234, deps pinned in pyproject.toml; data.py rebuilds end-to-end. full_data_out.json=21MB (<100MB, no split). NOTE: iteration-2 reads SAE activations on these inputs; this artifact itself does not run the SAE.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json

--- Dependency 4 ---
id: art_t2uUbjSwpd3t
type: dataset
title: 'Non-Spelling SAE Absorption Testbed: Numeric & Taxonomic Hierarchies'
summary: |-
  TEXT-ONLY dataset (no SAE/model/activation computation here) for testing whether SAE feature absorption — documented almost exclusively on first-letter spelling — generalizes to two NON-spelling parent concepts. It is the never-dropped C3-spine testbed for the Counterfactual Co-Response Grouping hypothesis. Output is the AII exp_sel_data_out schema (one example per data row; per-row metadata flattened to metadata_* keys, since nested objects are disallowed), grouped into exactly two datasets:
  • numeric_absorption (8,380 examples): parent = 'token is numeric (a digit / part of a number)'; absorber sub-contexts = year, percent, currency, date, decimal, integer, comma_number, ordinal (year/percent/currency/date are the primary candidates).
  • taxonomic_absorption (15,748 examples): parent = 'token is part of a country name'; absorber sub-contexts = individual countries.

  Each hierarchy ships three coordinated components: (A) content-flip minimal pairs — x_on contains the concept, x_off a surface-matched non-concept word at the same slot (taxonomic uses country-vs-city and country-vs-other-proper-noun negative families); (B) surface-flip pairs — same concept token in two different carrier sentences, for the unit-level surface-invariance admission check; (C) a frozen pile-uncopyrighted (rev 3be90335b66f24456a5d6659d9c8d208c0357119) diagnostic corpus of real natural-text windows labelled by frozen sub-context, plus matched negatives (no-digit, city-mention, no-country), so iter-2 can train a parent linear probe and run the per-sub-context false-negative (parent-hole) search.

  Every row marks the exact target span (target_text + char_start/char_end) and carries precomputed google/gemma-2-2b token indices (100% coverage; the tokenizer splits numbers into individual digit tokens). Sub-context labels are assigned purely from surface form / regex / gazetteer (pycountry + geonamescache) — independent of any SAE latent or model behaviour — so the degenerate-construction guard holds and the same labelled corpus equally supports the honest 'absorption is spelling-specific' null (uniform high parent-probe recall across sub-contexts). Frozen folds (seed 20240617): pairs split train/test 70/30 by pair_id (stratified by sub_context); corpus splits train/diagnostic 50/50 (stratified). absorption_readiness in manifest.json: ALL 8 numeric sub-contexts and 20 countries reach ≥150 diagnostic-fold positives (eligible for the inferential test); rarer sub-contexts/countries are kept and flagged descriptive_only. Content-flip (≥240) and surface-flip (≥120) per-hierarchy floors are exceeded. A deterministic templated backbone is supplemented by openai/gpt-4o-mini generation, with every content/surface pair (LLM-generated + 20% templated spot-check) LLM-judged on content_flipped/surface_preserved/grammatical — 100% pass at $0.0104 total spend (hard cap $4, ceiling $10). Ambiguous homographs (Georgia, Turkey, Chile, Jordan) and multi-word countries are flagged via metadata_notes / metadata_multi_token.

  Deliverables: data.py (canonical builder), pipeline.py + build_dataset.py (logic modules), full/mini/preview_data_out.json, schema.json (JSON Schema + logical nested view), manifest.json (per-sub-context counts, fold counts, pass rates, spend, pile revision, readiness), and pyproject.toml with pinned dependency versions. Reproduce with `python3 data.py --scale full`. iter-2 consumes this to run the Tier-0 non-triviality pre-check (does a high-recall parent latent exist AND have specialist-filled holes?), the form-free absorption diagnostic as oracle, and the K-track anchored greedy set-cover proposal step — with numeric as the primary novelty test and taxonomic as the pre-registered alternative.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_2
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json

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

- **Multi-LLM Agents** — framework choices, implementation patterns, agent orchestration
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
TODO 2. Read preview files from dependencies to understand data structure. Use ALL datasets provided — do not skip or select a subset. Read domain handbook if applicable (see <available_domain_handbooks>). Test basic functionality with 'uv run'.
TODO 3. Fully implement our method AND baseline (comparison) as described in artifact plan in './method.py'. Use exp_gen_sol_out.json schema in aii-json skill for output format validation. Include everything specified in the artifact plan, but you may also implement additional relevant methods or analysis beyond what's listed. Be very attentive to meticulously and exhaustively fix any errors in your code.
</todos>
```

### [2] HUMAN-USER prompt · 2026-06-17 21:59:17 UTC

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

### [3] SKILL-INPUT — aii-python · 2026-06-17 21:59:25 UTC

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

### [4] SKILL-INPUT — aii-long-running-tasks · 2026-06-17 21:59:25 UTC

The agent loaded the **aii-long-running-tasks** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-long-running-tasks
description: Gradual scaling pattern for long-running autonomous tasks. Use when running experiments, evaluations, or any code that processes data at increasing scale with runtime checks.
---

## Core Principles

1. **Time budget first**: Read your time/runtime constraints before running anything. Set every Bash timeout to fit within the budget.
2. **Start small, scale up**: Run on minimal input first, fix errors, then increase scale.
3. **Extrapolate before scaling**: Use recorded runtimes to predict whether the next step fits in the budget. Don't guess — calculate.
4. **Background execution**: For anything that takes >1 min, run in background (`run_in_background=true`) and do useful work while waiting.
5. **Stop early if needed**: Quality results on less data beats a timeout or crash. It's always acceptable to stop at a smaller scale.

---

## Gradual Scaling Sequence

Run code at increasing data sizes, checking runtime at each step.

Substitute your actual file names:
- `{mini_file}` — mini JSON (3 examples) from dependency workspace
- `{full_file}` — full dataset from dependency workspace
- `{script}` — your processing script (e.g., `./method.py`, `./eval.py`)
- `{schema}` — JSON schema to validate output against

**STEP 1 — MINI DATA:** Run `{script}` on `{mini_file}`. Do NOT truncate logs. Fix all errors. Validate output against `{schema}`. Verify you are NOT using mock scripts, mock data, or mock APIs.

**STEP 2 — 10 EXAMPLES:** Modify `{script}` to load only the first 10 examples from `{full_file}`. Run and fix errors. Validate schema. Record the runtime.

**STEP 3 — 50 EXAMPLES:** Load first 50 examples from `{full_file}`. Run and fix errors. Record runtime. **EXTRAPOLATE**: Using runtimes from steps 2-3, estimate time per example. Calculate how many examples fit in your remaining time budget. If 50 already used most of the budget, stop here.

**STEP 4 — 100 EXAMPLES (if budget allows):** Load first 100 examples. Run and fix errors. Record runtime. Re-extrapolate with the new data point.

**STEP 5 — 200 EXAMPLES (if budget allows):** Load first 200 examples from `{full_file}`. Run and fix errors. Record runtime.

**STEP 6 — MAXIMIZE:** Using all recorded runtimes, extrapolate time-per-example (it may not be perfectly linear — account for overhead). Calculate the maximum number of examples that fits within your remaining time budget with a 10% safety margin. Load that many (or all if they fit). Run and validate.

## Final Testing Phase

After completing the scaling sequence, redo the entire sequence **one more time** up to your final example count:

mini → 10 → 50 → 100 → 200 → max

At each scale: look for issues, fix problems, validate output, ensure it completes within time limits.

---

## Background Execution

For any step that takes >1 min, run as a **background task**:

1. Launch with Bash `run_in_background=true`
2. While it runs, use the time productively:
   - Sanity-check previous outputs
   - Verify file integrity (correct field names, non-empty values)
   - Review code for edge cases at larger scale
   - Prepare the next step
3. Check back on the background task to get results
4. If it failed, fix errors and re-run

---

## Resource Limits

Set hard RAM and CPU time limits so code fails fast instead of crashing the system. Read limits from `<hardware>` and leave headroom for the OS (e.g., if 16GB total, cap at 14GB).

Python example using stdlib `resource` module:
```python
import resource
resource.setrlimit(resource.RLIMIT_AS, (14 * 1024**3, 14 * 1024**3))  # 14GB RAM
resource.setrlimit(resource.RLIMIT_CPU, (3600, 3600))  # 1 hour CPU time
```
Exceeding RAM raises `MemoryError`. Exceeding CPU time sends `SIGKILL`.

## Monitoring

At each step, record runtime AND check resource usage (`free -h` for RAM, `top -bn1 | head -5` for CPU). If memory usage is climbing toward the limit or CPU is pegged, stop and investigate before scaling further.
````

### [5] SKILL-INPUT — aii-use-hardware · 2026-06-17 21:59:25 UTC

The agent loaded the **aii-use-hardware** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-use-hardware
description: Detect hardware and use it responsibly. Covers CPU/RAM/GPU detection, memory-safe data processing, and resource-aware computation.
---

**Step 1** — Run `bash scripts/get_hardware.sh` (relative to this skill's directory).

Read the `=== CGROUP ===` section carefully. If `Type: cgroup v1` or `cgroup v2`:
- You are in a **container with hard resource limits**. Exceeding them = OOM kill, no recovery.
- **Never** use `psutil.virtual_memory().total`, `free -h`, `/proc/meminfo`, `os.cpu_count()`, or `nproc` for resource limits — these report **host** values, not your container's allocation.
- **Always** read limits from the cgroup paths shown in the output, or use the Python helpers below.
- For **runtime memory monitoring**, read current usage from cgroup too:
  - v2: `/sys/fs/cgroup/memory.current`
  - v1: `/sys/fs/cgroup/memory/memory.usage_in_bytes`

**Step 2** — Use Step 1 results to pick package variants **before** installing.

Defaults often target the most powerful environment — PyPI's `torch` ships with CUDA libs even on CPU-only hosts. Wrong variant = wasted disk, slow setup, possible import-time failures.

If `=== GPU ===` shows `No GPU`, install torch's CPU build (skips ~4.5GB of CUDA libs):
```bash
uv pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
```
Same idea for any library whose wheel selection depends on detected hardware (GPU/CPU-only builds, architecture-specific wheels).

After install, sanity-check imports right away (`python -c "import torch"`). Disk-pressure or interrupted installs leave half-built wheels (e.g. `libtorch_global_deps.so` missing) — catch these before the experiment runs.

**Step 3** — Set Python constants from the Step 1 results:
```python
import os, math, torch, psutil
from pathlib import Path

def _detect_cpus() -> int:
    """Detect actual CPU allocation (containers/pods/bare metal)."""
    try:  # cgroups v2 quota
        parts = Path("/sys/fs/cgroup/cpu.max").read_text().split()
        if parts[0] != "max":
            return math.ceil(int(parts[0]) / int(parts[1]))
    except (FileNotFoundError, ValueError): pass
    try:  # cgroups v1 quota
        q = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_quota_us").read_text())
        p = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_period_us").read_text())
        if q > 0:
            return math.ceil(q / p)
    except (FileNotFoundError, ValueError): pass
    try:  # CPU affinity (cpuset — used by RunPod, Docker --cpuset-cpus)
        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError): pass
    return os.cpu_count() or 1

def _container_ram_gb() -> float | None:
    """Read RAM limit from cgroup (containers/pods)."""
    for p in ["/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"]:
        try:
            v = Path(p).read_text().strip()
            if v != "max" and int(v) < 1_000_000_000_000:
                return int(v) / 1e9
        except (FileNotFoundError, ValueError): pass
    return None

NUM_CPUS = _detect_cpus()
HAS_GPU = torch.cuda.is_available()
VRAM_GB = torch.cuda.get_device_properties(0).total_mem / 1e9 if HAS_GPU else 0
DEVICE = torch.device("cuda" if HAS_GPU else "cpu")
TOTAL_RAM_GB = _container_ram_gb() or psutil.virtual_memory().total / 1e9
AVAILABLE_RAM_GB = min(psutil.virtual_memory().available / 1e9, TOTAL_RAM_GB)
```

## Step 4 — Set Memory Limits

OOM kills the entire container. **Every script MUST set RAM and VRAM limits at startup.**

Decide the budget based on what the script actually needs. Estimate data size × 2-5x for in-memory overhead, then add ~50% breathing room for temporaries. You may use up to 90% of available RAM/VRAM, but **scale gradually** — start small (e.g. 30-50%), verify it works, then increase toward the limit. Never exceed 90% to keep a buffer for the OS, system processes, and the agent runtime itself. Going over crashes the container/machine with no recovery.

```python
import resource, psutil

_avail = psutil.virtual_memory().available
RAM_BUDGET = ???  # YOU decide: estimate what this script needs (in bytes)
assert RAM_BUDGET < _avail, f"Budget {RAM_BUDGET/1e9:.1f}GB > available {_avail/1e9:.1f}GB"
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))  # 3x: virtual > RSS; raises MemoryError on exceed

if HAS_GPU:
    _free, _total = torch.cuda.mem_get_info(0)
    VRAM_BUDGET = ???  # YOU decide: estimate GPU memory needs
    torch.cuda.set_per_process_memory_fraction(min(VRAM_BUDGET / _total, 0.95))  # raises OutOfMemoryError on exceed
```

## Memory-Safe Data Processing

- **One at a time**: load one large object → process → `del obj; gc.collect()` → next
- **Load only what you need**: select specific tables/columns/rows, not entire databases
- **Test small first**: run on a sample before scaling to full data to estimate memory/time
- **Free intermediates in loops**: don't accumulate large results — aggregate incrementally
- **Size before loading**: check file/dataset size before loading; if it's >30% of `RAM_BUDGET`, chunk it

## Common Mistakes (from real crashes)

- **Skipping this skill entirely** — loading data with no RAM detection, no limits, no budget. Container OOM-killed, all agents lost.
- **Using `psutil.virtual_memory().total` instead of `_container_ram_gb()`** — reports host RAM (e.g. 66 GB) when container limit is 28 GB. You MUST use the cgroup-aware functions above.
- **Loading all tables from a multi-table database at once** — one agent loaded 14 RelBench tables simultaneously, spiked past container limit.
- **Setting no memory limits** — without `resource.setrlimit` (RAM) and `set_per_process_memory_fraction` (VRAM), a runaway script OOM-kills the container instead of raising a catchable error.
- **Using `os.cpu_count()` directly** — returns host CPUs (e.g. 192) instead of container limit (e.g. 4) on RunPod/Docker. Always use `_detect_cpus()` above which checks cgroup quota → CPU affinity → `os.cpu_count()` in order.

## Hardware Use

- Keep these results in mind for ALL subsequent tasks — don't assume more than detected
- GPU if available and parallelizable, multiprocessing if multiple CPUs
- Push available resources to their full potential — don't leave hardware idle
````

### [6] SKILL-INPUT — aii-json · 2026-06-17 21:59:31 UTC

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

### [7] SKILL-INPUT — aii-parallel-computing · 2026-06-17 21:59:31 UTC

The agent loaded the **aii-parallel-computing** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-parallel-computing
description: "CRITICAL PERFORMANCE SKILL. Maximize hardware utilization for compute-intensive tasks. Covers GPU acceleration, CPU parallelism, and async I/O. The difference between hours of failure and minutes of success. Use whenever writing ANY script that processes data, makes API calls, or does computation."
---

**ALWAYS parallelize. Sequential processing is unacceptable for any non-trivial workload.** A sequential script doing 1000 API calls takes hours and fails halfway. An async version finishes in minutes with proper error handling. ALWAYS ask: "Can this run in parallel?" — the answer is almost always yes.

Read aii-use-hardware skill first → get `NUM_CPUS`, `HAS_GPU`, `VRAM_GB`, `device`. Set `NUM_WORKERS` proportional to available CPU capacity — check `psutil.cpu_percent(interval=1)` and scale accordingly (e.g. 30% used → use ~70% of cores).

## Decision Tree (follow strictly)

- **I/O-bound** (API calls, downloads, web, file reads) → `asyncio` + `aiohttp` with `Semaphore(NUM_WORKERS * 4)`. NEVER do sequential HTTP requests in a loop.
- **CPU-bound, vectorizable** → GPU available: PyTorch on device / No GPU: NumPy vectorized ops. NEVER loop over array elements in Python.
- **CPU-bound, independent items** → `ProcessPoolExecutor(max_workers=NUM_WORKERS)`. NEVER process items one-by-one when they're independent.
- **Sequential** → only acceptable when items have data dependencies (each depends on the previous result).

## GPU Rules

- Use up to 90% of available VRAM — scale gradually (start small, increase after each successful run, keep 10% buffer)
- Move to device → compute → move back: `torch.tensor(data, device=device)` → `.cpu().numpy()`
- OOM fallback: catch `torch.cuda.OutOfMemoryError` → `empty_cache()` → halve batch size → retry on GPU. Keep reducing until it fits. Stay on GPU.
- Batch large data: chunk it, `del batch` between iterations to free VRAM

## Parallelism Rules

- **CPU-bound**: `ProcessPoolExecutor` + `as_completed`, pre-allocate result list indexed by submission order
- **I/O-bound**: `asyncio` + `aiohttp`, `Semaphore(NUM_WORKERS * 4)`, single shared `ClientSession`, `asyncio.gather(*tasks, return_exceptions=True)`
- Always add `tenacity` retries for transient failures, always set timeouts on HTTP requests
- **CRITICAL — `ProcessPoolExecutor` start method**: Default `fork` deadlocks with loguru (and any threading library). ALWAYS pass `mp_context=multiprocessing.get_context("spawn")` when constructing `ProcessPoolExecutor` in any script that uses loguru, threading, or async I/O. Example:
  ```python
  import multiprocessing as mp
  from concurrent.futures import ProcessPoolExecutor
  with ProcessPoolExecutor(max_workers=N, mp_context=mp.get_context("spawn")) as pool:
      ...
  ```
````

### [8] SKILL-INPUT — aii-file-size-limit · 2026-06-17 21:59:31 UTC

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

### [9] SYSTEM-USER prompt · 2026-06-17 23:00:06 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_1/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_1/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_1/results/out.json`
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
id: gen_plan_experiment_1_idx1
type: experiment
title: >-
  Expand the Measured KG-Guided Recall-Repair Loop + Member-Labeling to ALL Eligible Absorbed Sub-Contexts (Auditability Spine,
  M1a + M7-fraction)
summary: >-
  Make the measured auditability result the paper's load-bearing spine by EXPANDING the iter-3 KG-repair loop (currently 8
  significant repairs over taxonomic Georgia/Jordan/US + first-letter O/'our', D/'day') and member-labeling (67 members) to
  the FULL set of eligible absorbed sub-contexts across spelling (L/O/T/I/D words), homograph-taxonomic (all >=150-positive
  countries, testing Georgia/Jordan/US + flagged homographs Turkey/Chile/etc. for holes) and numeric (year/percent/currency/date/decimal/integer/comma_number/ordinal).
  Reuse the iter-3 pipeline at iter_3/gen_art/gen_art_experiment_3/method.py almost verbatim (SAE loader, JumpReLU encode>0,
  hook blocks.12.hook_resid_post, gating cosine>0.9, repair_loop, k_localization_check, LLM judge), adding: (1) BROAD KG re-derivation
  so every eligible hole sub-context gets a named covering absorber via the K-track greedy (not just the 3 canonical taxonomic
  edges); (2) a one-sided bootstrap p-value per repair + Benjamini-Hochberg FDR<=0.05 across the now-many repairs (multiplicity
  MUST live in-experiment); (3) the (k)-cannot-localize JTT/GEORGE check run for first-letter and numeric too, not just taxonomic;
  (4) member-labeling over EVERY member of every admitted unit INCLUDING all 15 members of each first-letter max-pool, with
  an ensemble-based confidence test reporting the FRACTION of the 15-wide pool that receives a confident, above-null-margin
  label. Honest negatives (KG repair tying random-addition, e.g. first-letter L/T words; numeric ties) reported verbatim.
  GPU; LLM target <$1, hard $10 cap.
runpod_compute_profile: gpu
implementation_pseudocode: |-
  =====================================================================
  GOAL: broaden art_lvYkaolutJG (iter-3 experiment_3) from 8 repairs / 67 members
  to the FULL eligible set, with BH multiplicity + 15-wide confident-label fraction.
  The iter-3 code already WORKS end-to-end; this is an EXPANSION, not a rewrite.
  =====================================================================

  # ---------- 0. SETUP / HARDWARE (aii-use-hardware, aii-long-running-tasks) ----------
  # pyproject.toml: torch, transformers, scipy, scikit-learn, numpy, loguru, requests,
  #   statsmodels (BH) OR hand-roll BH; huggingface_hub.
  # Detect GPU + compute capability. KNOWN RISK (iter-3 note): host GPU may be sm_120
  #   (Blackwell / RTX 5090) which the default torch wheel does not support ->
  #   try `uv pip install torch --index-url https://download.pytorch.org/whl/cu128`;
  #   if CUDA still unusable, FALL BACK TO CPU encoding (works, just slow) and
  #   reduce per-concept corpus caps (mini scaling) to stay in wall-clock budget.
  # bf16 on GPU; float32 on CPU. Memory-safe batching BATCH=16, MAXLEN=192.
  # Set RLIMIT_AS guard (reuse set_limits()). seed=1234 everywhere.

  # ---------- 1. PATHS / INPUTS (read-only) ----------
  ROOT = /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop
  D1 = iter_1/gen_art/gen_art_dataset_1/full_data_out.json   # first-letter L/O/T/I/D (art_dpYpjSn2Xvg3)
  D2 = iter_1/gen_art/gen_art_dataset_2/full_data_out.json   # numeric + taxonomic (art_t2uUbjSwpd3t)
  E1 = iter_2/gen_art/gen_art_experiment_1/method_out.json   # first-letter canonical units + 15-wide pool
  E3 = iter_2/gen_art/gen_art_experiment_3/method_out.json   # taxonomic canonical units/KG
  ITER3 = iter_3/gen_art/gen_art_experiment_3/{method.py, method_out.json}  # REUSE code + cross-check
  # Optionally reuse cached encodings if iter_3/.../cache/ holds residuals+CSR latents.

  # ---------- 2. SAE + MODEL + GATING (reuse iter-3 verbatim) ----------
  load JumpReLUSAE from gemma-scope-2b-pt-res params.npz (layer_12/width_16k/average_l0_82);
    encode(x) = (pre>threshold)*relu(pre); decode(z)=z@W_dec+b_dec; d_model=2304, d_sae=16384.
  load model google/gemma-2-2b (fallback unsloth/gemma-2-2b mirror, vocab 256000).
  determine_layer_idx(gate_rows): pick hidden_states idx (12/13/14) with lowest FVU -> expect 13.
  ASSERT reconstruction cosine > 0.9 (iter-3 got 0.9190 @ idx 13, L0~88); abort if not.
  encode_rows(rows): per row, select target token positions by char span / token idx,
    max-pool SAE latents over target tokens -> CSR [N,d_sae]; mean residual -> fp16 [N,d_model];
    report align (decoded-token==target). REUSE select_positions / _attach_span_fl / _attach_span_tax.

  # ---------- 3. PER-CONCEPT: RE-DERIVE UNIT + BROAD KG (the key new derivation) ----------
  CONCEPTS = ['taxonomic','numeric','L','O','T','I','D']
  for concept in CONCEPTS:
      rows = load concept rows (D2 taxonomic_absorption / D2 numeric_absorption / D1 first_letter_X)
      lat_csr, resid, _, align = encode_rows(rows, sae)
      # 3a. content-responsive set + per-latent firing precision (reuse content_responsive()):
      #     from TRAIN content_pair (x_on,x_off): cr = latents with mean(on-off)>shuffle-null95 & >0
      cr, prec, mean_R = content_responsive(A_on, A_off)
      cover[l] = #content-flip x_on the latent fires on (recall proxy)
      # 3b. ANCHOR = highest-cover precise (prec>=0.7) content-responsive latent,
      #     WITH the unsupervised parent-firing-floor validation (reject anchors that fire ~0%
      #     on the held corpus -> this is what flags letter-I anchor 1227 as spurious).
      anchor = argmax_{l in cr, prec[l]>=0.7, corpus_fire_rate(l)>floor} cover[l]
      if no anchor clears the corpus firing floor: mark concept spurious_anchor -> repair N/A (report).
      # 3c. BROAD K-TRACK KG: for EVERY eligible sub-context X (>= N_MIN_EVAL positives in the
      #     corpus-diagnostic/eval split), NAME the covering absorber. This generalizes the
      #     iter-3 3-edge taxonomic KG to all countries / all numeric types / all first-letter words.
      eligible_X = sub_contexts with >= 150 (tax/numeric) OR >= N_MIN_RELAX (first-letter) eval positives
      for X in eligible_X:
          r_anchor_sel(X) = anchor firing recall on X's SELECTION-split positives
          is_hole(X) = r_anchor_sel(X) <= HOLE_RECALL_MAX(0.60) OR < overall_anchor_recall - 0.10
          # K-track covering absorber for X (selected ONLY on selection split = non-circular vs eval):
          kg_absorber[X] = argmax_{l in cr, l!=anchor, jaccard(l,anchor)<0.10, prec_on_X(l)>=0.70}
                            (firing recall of l on X's SELECTION positives)
          record KG edge anchor --specializes--> kg_absorber[X]  (sub_context=X)
      # Cross-check the re-derived anchor / KG against E1/E3/iter-3 canonical_units (reproduction block).
      # For TAXONOMIC also keep the diagnostic-corroborated absorbers from E3
      #   non_triviality_passing_absorbers: Georgia=16009(prec .955), Jordan=540/8347, US=846.

  # ---------- 4. REPAIR-LOOP EXPANSION (reuse repair_loop(), extend variants + p-value) ----------
  # Split policy to MAXIMIZE eligible sub-contexts while staying doc-disjoint:
  #   tax/numeric: selection = corpus fold 'train', eval = corpus fold 'diagnostic' (>=150 each).
  #   first-letter: selection = corpus source_doc folds {0,1,2}, eval = folds {3,4}  (40% to eval,
  #     ~2x iter-3's single-fold eval -> recovers more words past N_MIN_RELAX=15). Doc-disjoint = no leak.
  for concept, for each hole/eligible X with kg_absorber[X]:
      base = anchor fires on X's EVAL positives;  base_recall = mean(base)
      # random-addition control: add each OTHER content-responsive latent (population, excl unit members),
      #   per-window mean detection rand_detect_perwin; gives random_gain distribution (p5/p50/p95).
      for variant in {'kg_ktrack': kg_absorber[X], 'kg_diagnostic': diag_absorber[X] (tax only, 3 named)}:
          kg_detect = base | (variant latent fires on X eval positives)
          gain_kg = mean(kg_detect) - base_recall
          pct = fraction of random-control latents whose gain < gain_kg
          diff_perwin = kg_detect - rand_detect_perwin
          CI = paired_bootstrap_diff(diff_perwin, B=10000)     # 95% percentile CI
          p_value = (1 + #{bootstrap_mean <= 0}) / (B+1)         # NEW one-sided p (H0: gain<=0)
          measured_success = CI.excl_0 and CI.diff>0
          if is_hole and not measured_success: append honest_negative verbatim
  # Collect ALL (concept,X,variant) -> {gain_kg, CI, percentile, p_value, n_eval, is_hole}.

  # ---------- 5. MULTIPLICITY: BENJAMINI-HOCHBERG (must live IN this experiment) ----------
  pvals = [v.p_value for every measured repair variant across ALL concepts]
  q = benjamini_hochberg(pvals)        # statsmodels.stats.multitest.multipletests(method='fdr_bh')
  attach q to each repair; n_survive_FDR05 = #{q <= 0.05}
  report: n_repairs_tested, n_holes, n_measured_success(uncorrected CI), n_survive_FDR05,
          and per-concept breakdown (spelling vs homograph-tax vs numeric).

  # ---------- 6. (k)-CANNOT-LOCALIZE  (reuse k_localization_check, run for ALL concepts) ----------
  for concept in {taxonomic, numeric, L, O, T, D}:    # skip spurious-anchor concepts
      JTT label-free group inference on dense resid: ERM probe -> upweight error/low-margin set -> retrain.
      project reweighted hyperplane w_k onto SAE decoder dictionary (cos = W_dec @ w_k / |W_dec|).
      report: projection_argmax_latent (expect = PARENT/anchor, NOT an absorber),
              single_latent_dominates (expect False),
              kg_absorber_projection_ranks per X (expect deep ranks, e.g. Georgia 4697 rank ~1728),
              conclusion: (k) classifies holes but exposes NO addable per-sub-context latent.

  # ---------- 7. MEMBER-LABELING EXPANSION + CONFIDENT-FRACTION (M7) ----------
  # Members to label = EVERY admitted-unit member, INCLUDING all 15 members of each first-letter
  #   max-pool (anchor + the 14 cover-eligible latents in E1 per_letter / sub_by_absorber), and
  #   the taxonomic/numeric anchor + named absorbers (k-track AND diagnostic).
  for each member m (role in {anchor,absorber}, ground-truth sub-context = m's modal firing sub-context):
      evidence = { logit_lens_top10 = topk(E @ W_dec[m]) decoded tokens,
                   top5 activating corpus windows with TARGET span marked **..** and SUB-CONTEXT WITHHELD }
      candidates = ['GENERAL parent'] + named sub-contexts for that concept's pool
      # ENSEMBLE confidence (NEW): J=3 judge calls per member; diversify by shuffling candidate
      #   option ORDER across calls (+ optionally 1 fallback model) so position bias differs.
      #   judge = OpenRouter anthropic/claude-haiku-4.5 temp 0 forced-choice integer index;
      #   fallbacks gemini-3.1-flash-lite, deepseek-v3.2; track cumulative cost; HARD STOP $10, target <$1.
      majority_label = mode over the J calls (remapped through each call's shuffled order)
      agree_rate = (#calls agreeing with majority)/J
      confident(m) = (majority_label is a SPECIFIC sub-context, not GENERAL/parse-fail)
                     AND agree_rate >= 2/3 AND agree_rate > per-member chance(1/n_candidates)  # above-null-margin
      correct(m) = (majority_label == ground_truth sub-context)
  # SCORING (reuse score_labeling + add fraction):
    agreement = mean(correct over valid members); shuffle-null over N_SHUFFLE=2000 perms of gt;
    gap = agreement - null_mean; bootstrap CI on gap (excl_0?); per_role_accuracy {anchor,absorber}.
    NEW: confident_label_fraction[concept] = #confident / #members;
         first_letter_15wide_confident_fraction[letter] = (#confident of the 15 pool members)/15;
         also report confident-AND-correct fraction. -> directly answers the '15-wide vs named' critique.

  # ---------- 8. VERDICT + OUTPUT (exp_gen_sol_out schema; reuse save_json) ----------
  metadata = { sae, model, gating_check, seed, B_boot, n_shuffles, llm_model,
     reproduction_crosscheck (anchor/KG vs iter-2/iter-3 canonical),
     repair_loop: per concept per X { recall_anchor_selection, recall_anchor_eval,
         random_gain{p5,p50,p95}, variants{kg_ktrack,kg_diagnostic}:{absorber_latent,
         recall_anchor_plus_kg, gain_kg, kg_percentile_vs_random, paired_bootstrap_CI,
         p_value, bh_q, measured_success}, is_hole, n_eval },
     multiplicity: { n_tested, n_holes, n_measured_success, n_survive_FDR05, per_concept_breakdown },
     k_localization_check: per concept,
     member_labeling: { per_member, scoring{agreement, null_mean, gap, gap_CI, per_role_accuracy},
         confident_label_fraction, first_letter_15wide_confident_fraction, llm_cost_usd, llm_calls },
     honest_negatives: [verbatim strings],
     verdict: { kg_utility_measured, n_survive_FDR05, member_labeling_above_null,
         fifteen_wide_confident_fraction_reported: true } }
  datasets = [ {dataset:'kg_repair_loop', examples:[one row per (concept,X,variant): input describes
                  the repair, output in {repair_significant, survives_FDR, tie_with_random}, metadata_*
                  = gain_kg, CI, percentile, p_value, bh_q, n_eval, is_hole}],
               {dataset:'member_labeling', examples:[one row per member: gt label, judge majority label,
                  confident flag, correct flag, role, concept]} ]
  save method_out.json; then aii-json -> validate exp_gen_sol_out + generate mini/preview; assert all <100MB.

  # ---------- KEY CONSTANTS (from iter-3, keep) ----------
  N_MIN_EVAL=30 (relax 15), HOLE_RECALL_MAX=0.60, B_BOOT=10000, N_SHUFFLE=2000,
  jaccard<0.10, precision>=0.70, FDR alpha=0.05, LLM target<$1 hard-stop $10.
fallback_plan: >-
  GPU / CUDA arch (highest-risk, seen in iter-3): if the host is sm_120 (RTX 5090/Blackwell) and the default torch wheel errors
  on CUDA init, (a) install the cu128 wheel `uv pip install torch --index-url https://download.pytorch.org/whl/cu128`; (b)
  if still broken, run encoding on CPU (correct, just slow) and CAP corpus rows per concept (e.g. --max_corpus 600 for first-letter;
  keep all >=150 tax/numeric eval positives since those are the load-bearing repairs) so the full run finishes in budget.
  Reconstruction-gating failure (cosine<=0.9): re-run determine_layer_idx over idx 12/13/14 and pick the lowest-FVU index
  (iter-3 -> 13); if none clears 0.9 the SAE/layer mapping is wrong — abort and report, do NOT analyze a mis-mapped SAE. Few-eligible-first-letter
  holes (per-word corpus windows are scarce — iter-3 skipped most L/T words at n_eval<15): this is expected and HONEST — the
  expansion volume is carried by taxonomic (>=150-positive countries) + numeric (8 sub-contexts each >=150); report first-letter
  coverage as-is (folds {0,1,2}/{3,4} split already ~2x iter-3's eval), and if still too sparse, additionally report a POOLED
  first-letter repair (absorber recall recovery on the union of that letter's hole-words) as a supplementary, clearly-labeled
  aggregate. Numeric shows no clean holes (parent already high-recall; memory: numeric diagnostic-unconfirmed): report numeric
  repairs as ties/honest-negatives — a clean negative that STRENGTHENS the homograph-scope story (absorption concentrates
  on polysemous tokens), not a failure. BH leaves zero survivors (worst case): still report the uncorrected CI-excluding-0
  repairs (the 8 known taxonomic+O/D repairs have huge gains 0.2-1.0 with tight CIs, so several WILL survive FDR<=0.05); if
  truly none survive, that is the declared 'auditability buys no robust fix' negative and is itself publishable. LLM judge
  unreachable / over budget: degrade ensemble J 3->1, then run --no_llm and report member-labeling as 'not scored (LLM unavailable)'
  while still emitting the repair-loop + (k)-localization spine (the load-bearing numeric result needs no LLM). LLM parse
  failures: re-ask once constrained ('respond with ONLY the integer'), then fall back to next model; count parse-fails, exclude
  from agreement, include in the confident-fraction denominator (a parse-fail member is NOT confident). Output >100MB: drop
  per-window text from datasets rows (keep in a capped sample), keep all numeric stats; use aii-file-size-limit to split if
  needed.
testing_plan: >-
  Stage 0 — SMOKE (minutes, $0): `uv run method.py --smoke` loads SAE + model, runs determine_layer_idx + gating; CONFIRM
  reconstruction cosine>0.9 (expect ~0.919 @ idx 13, L0~88) and align~1.0. If gating fails, STOP and fix layer mapping before
  anything else. Stage 1 — MINI PILOT one absorption concept, no LLM (~10 min, $0): `uv run method.py --concepts taxonomic
  --max_corpus 300 --no_llm`. CONFIRMATION SIGNALS that the pipeline reproduces iter-3 before expanding: re-derived taxonomic
  anchor == 3792 (anchor_match true); Georgia repair gain_kg ~0.8 with paired-bootstrap CI excluding 0 and percentile_vs_random
  ~0.99; Jordan ~0.71; US ~0.22; (k) projection_argmax_latent == 3792 (parent) with single_latent_dominates False and Georgia(4697)
  rank in the hundreds-to-thousands. If these three known repairs do NOT reproduce, the encoding/KG derivation has drifted
  — debug before scaling. Stage 2 — ADD numeric + BROAD KG + BH (~15 min, $0): `--concepts taxonomic,numeric --no_llm`; verify
  the broad-KG derivation names a covering absorber for every eligible sub-context, the one-sided p_value + BH q columns populate,
  and n_survive_FDR05 >= the known taxonomic repairs (>=4). Sanity-check numeric mostly ties random (honest negatives), confirming
  homograph-scope. Stage 3 — FIRST-LETTER (~15 min, $0): `--concepts L,O,T,I,D --no_llm`; verify letter-I is flagged spurious_anchor
  (anchor 1227 fires 0% corpus -> repair N/A) and that O/'our', D/'day' reproduce as significant repairs; record how many
  first-letter words clear the {0,1,2}/{3,4} eval split. Stage 4 — LLM MEMBER-LABELING on a small subset first ($<0.05): label
  one letter's 15-wide pool + taxonomic members with the J=3 ensemble; verify cost-per-call tracked, parse rate high, confident_label_fraction
  computed, and absorber per-role accuracy >> shuffle null (iter-3 absorbers 0.758 vs null 0.090). CHECK cumulative spend
  after this subset and extrapolate; abort to --no_llm if projected >$1. Stage 5 — FULL RUN (all concepts + full corpus +
  LLM ensemble): monitor logs (PID-based, never by name), watch cumulative LLM cost line each iteration vs the $1 target /
  $10 hard cap, and confirm final method_out.json validates against exp_gen_sol_out with mini/preview all <100MB. Final acceptance:
  (a) >=1 KG repair survives BH FDR<=0.05 across spelling+homograph-tax+numeric; (b) (k) exposes no addable per-sub-context
  latent on every concept; (c) member-labeling gap CI excludes 0 AND the 15-wide first-letter confident-label fraction is
  reported per letter; (d) all honest negatives (ties with random) emitted verbatim.
</artifact_plan>

<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
id: art_RidEJtBC7gPT
type: research
title: 'Two-Track CCRG Implementation Dossier: SAE Pipeline, 11 Baselines, Protocols'
summary: >-
  A decision-complete, code-ready implementation blueprint for the two-track Counterfactual Co-Response Grouping (CCRG) method
  on frozen Gemma Scope SAEs. Pins the SAE encoding pipeline (defensive from_pretrained loader, JumpReLU firing=encode>0,
  hook blocks.12.hook_resid_post), the C-track (signed soft-threshold + leidenalg RBConfigurationVertexPartition) and K-track
  (anchored greedy max-coverage) algorithm with all thresholds, all eleven baselines (a)-(k) as runnable specs (LEACE for
  f, SAEBench SCR/TPP for g/h, JTT/GEORGE/group-DRO for j/k), the AxBench steering protocol (harmonic-mean LLM-judge 0/1/2),
  a corrected model-diffing recipe (shared frozen pt-SAE on gemma-2-2b vs gemma-2-2b-it because no gemma-scope-2b-it SAE exists),
  the statistics plan (paired bootstrap, exact McNemar, MDE n_min=150, Holm-Bonferroni), and a fully-verified 30+ citation
  table including all four high-risk future-dated arXiv IDs (all resolve).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_research_1
out_dependency_files:
  file_list:
  - research_out.json

--- Dependency 2 ---
id: art_I2MrezW41iQo
type: research
title: Absorption Diagnostic + Pinned Datasets Dossier for Two-Track SAE Grouping
summary: >-
  Executor-ready dossier de-risking the C3 absorption spine and pinning every data/infra build for the two-track co-response
  SAE-grouping experiment. WP1 extracts the Chanin 2409.14507 absorption diagnostic verified against the lasr-spelling/sae-spelling
  code: parent latent = max ENCODER-cosine with an LR probe (+ k-sparse splits at f1-jump 0.03); absorber = largest-negative
  integrated-gradients ablation (IG steps=6) on the first-letter logit-diff m=g[y]-mean(g[incorrect]); decision thresholds
  probe_cos_sim_threshold=0.025 computed on the DECODER (sae.W_dec), ablation_delta_threshold=1.0, EPS=1e-8, 200-FN cap, topk=10;
  absorption_rate=num_absorptions/lr_probe_true_positives; valid only layers 0-17. It also supplies the strictly non-circular
  FORM-FREE version the paper itself gives in Appendix A.13 (and SAEBench implements as absorption_fraction): latent l absorbs
  iff tau_c < (a_hat_l . d_p)/(a . d_p) with a_hat_l = enc_act*W_dec[l] and d_p the parent-concept LR-probe direction trained
  on data DISJOINT from clustering -- works at all layers, no output logit needed, never used to form units. WP2 confirms
  absorption is empirically documented ONLY on first-letter spelling (LessWrong toy-models post; SAEBench eval id 'absorption_first_letter';
  Matryoshka/H-SAE only mitigate via the spelling metric), making Testbed-2 both a generality test and a novel empirical test;
  numeric-quantity hierarchy is recommended primary (taxonomic country alternative) with concrete non-triviality gates (parent
  recall >=0.60; >=1 absorber with firing-Jaccard<0.10, sub-context precision>=0.70, hole-coverage gain>=0.05 with bootstrap
  CI excluding 0) and an honest-null fallback that scopes C3 to spelling and routes generality through C1. WP3 pins HF datasets:
  s-nlp/paradetox (en_toxic_comment/en_neutral_comment, 19,744 rows, openrail++); google/civil_comments (text + 7 float32
  sub-attrs, 1.8M/97k/97k, CC0, 414.95MB -> subsample); tasksource/counterfactually-augmented-imdb (Text/Sentiment, no pair-ids
  -> acmi-lab GitHub for pairing, license unknown); CEBaB/CEBaB (full aspect-majority schema, license NOT on card = TODO);
  LabHC/bias_in_bios (hard_text/profession-int64-0-27/gender, 257k/39.6k/99.1k, 266MB, MIT, full alphabetical profession map).
  WP4 gives generation prompts + an independent LLM-judge rubric and verified June-2026 OpenRouter prices (generator google/gemini-3.1-flash-lite
  $0.25/$1.50 or deepseek/deepseek-v4-flash $0.09/$0.18; judge anthropic/claude-haiku-4.5 $1.00/$5.00), totalling ~$5.9-7.6
  for ~5,000 pairs with a hard $10 stop. WP5 captures sae-spelling get_alpha_tokens (convert_tokens_to_string then strip one
  leading space then all-alpha) and prompt template '{word} has the first letter:'; pins pile-uncopyrighted rev 3be9033 (2023-08-31,
  non-streaming); and SAE.from_pretrained(release='gemma-scope-2b-pt-res-canonical', sae_id='layer_12/width_16k/canonical',
  d_model=2304) + the 65k variant. CRITICAL model-diffing finding: NO gemma-scope-2b-it SAE exists anywhere (Google IT residual
  SAEs only for 9B) -> use the SHARED pt SAE on both gemma-2-2b and gemma-2-2b-it activations; both Google models are gated,
  use unsloth/gemma-2-2b(-it) mirrors. Full detail in research_report.md; every pinned fact and citation is in research_out.json.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_research_2
out_dependency_files:
  file_list:
  - research_out.json

--- Dependency 3 ---
id: art_dpYpjSn2Xvg3
type: dataset
title: >-
  First-Letter-Spelling Absorption Testbed (L/O/T/I/D): minimal pairs + frozen Pile corpus
summary: |-
  First-Letter-Spelling Absorption Testbed — the load-bearing dataset for the Two-Track Co-Response Grouping hypothesis (building reliable cluster-level units from individual SAE latents). Pure CPU/data artifact: NO SAE, no model weights, no GPU. 17,180 examples in 5 per-letter dataset groups (first_letter_spelling_{L,O,T,I,D}; L primary, O/T/I/D secondary; degenerate S/X excluded), schema exp_sel_data_out (full/mini/preview all PASSED).

  Three linked components per letter: (A) content_flip minimal pairs — (x_on,x_off) in an IDENTICAL carrier where x_on slots a word STARTING WITH the target letter and x_off a surface-matched word that does NOT (matched on char length, single-token-ness, Pile log-frequency); 1,750 pairs / 3,500 rows. Feeds the Tier-0 K-track anchored set-cover PROPOSAL pilot and the C3 absorber-recovery spine; reconstruct via metadata_pair_id and compute r_l=a_l(x_on)-a_l(x_off). (B) surface_flip pairs — (x_a,x_b) in an identical carrier, BOTH words start with the target letter but differ; 590 pairs / 1,180 rows; for the unit-level surface-invariance admission check (pooled response to surface flips ~0). (C) corpus_context — 12,500 real ~48-token windows (2,500/letter) from monology/pile-uncopyrighted @ rev 3be9033, each centred on a slot-eligible word-initial target-letter token with token_position annotated; plus a per-letter occurrence table (<=2,000 word-types) in dataset-level metadata — the substrate for iteration-2's form-free/Chanin (2409.14507) absorption diagnostic to locate false-negative absorbers (e.g. lion, London).

  Words are anchored in the real gemma-2-2b vocabulary (unsloth/gemma-2-2b ungated mirror, vocab==256000) via the exact sae-spelling get_alpha_tokens slot-eligibility recipe (word-initial '_' marker AND alpha). 7 carriers per content pair: sae-spelling spelling prompts (t_verbose '{word} has the first letter:', t_colon, t_icl with contamination-free ICL examples) + 4 word-class-agnostic mention carriers.

  Row schema is FLAT (exp_sel_data_out): input, output (first letter, uppercase), and metadata_* keys (dataset, letter, pair_id, pair_type, role, sub_context=the word covered, target_word, counterpart_word, template_id, label_starts_with_target, is_single_token, is_slot_eligible, first_letter, fold, word_char_span; corpus rows add source_doc_id, pile_revision, token_position, target_token_id, window_char_span, target_char_in_window). Pairs LINK via shared metadata_pair_id + metadata_role ({on,off}/{var_a,var_b}). Folds: minimal pairs by target_word, corpus by source_doc_id (5 folds, no leakage).

  Validation: the deterministic check is AUTHORITATIVE and reports 0 violations / 17,180 rows (flip property + input-span correctness are guaranteed by construction). The LLM judge (google/gemini-3.1-flash-lite, $0.12 total, < $3 cap) is a SECONDARY grammaticality/independent audit with pass rates 0.89-0.99 per (letter,pair_type); judge false-negatives are retained because the deterministic check governs drops. Corpus token_position verified EXACT (tok(input,add_special_tokens=False)[token_position]==target_token_id) on sampled rows. Frozen & reproducible: pinned tokenizer + Pile revision 3be90335..., seed 1234, deps pinned in pyproject.toml; data.py rebuilds end-to-end. full_data_out.json=21MB (<100MB, no split). NOTE: iteration-2 reads SAE activations on these inputs; this artifact itself does not run the SAE.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json

--- Dependency 4 ---
id: art_t2uUbjSwpd3t
type: dataset
title: 'Non-Spelling SAE Absorption Testbed: Numeric & Taxonomic Hierarchies'
summary: |-
  TEXT-ONLY dataset (no SAE/model/activation computation here) for testing whether SAE feature absorption — documented almost exclusively on first-letter spelling — generalizes to two NON-spelling parent concepts. It is the never-dropped C3-spine testbed for the Counterfactual Co-Response Grouping hypothesis. Output is the AII exp_sel_data_out schema (one example per data row; per-row metadata flattened to metadata_* keys, since nested objects are disallowed), grouped into exactly two datasets:
  • numeric_absorption (8,380 examples): parent = 'token is numeric (a digit / part of a number)'; absorber sub-contexts = year, percent, currency, date, decimal, integer, comma_number, ordinal (year/percent/currency/date are the primary candidates).
  • taxonomic_absorption (15,748 examples): parent = 'token is part of a country name'; absorber sub-contexts = individual countries.

  Each hierarchy ships three coordinated components: (A) content-flip minimal pairs — x_on contains the concept, x_off a surface-matched non-concept word at the same slot (taxonomic uses country-vs-city and country-vs-other-proper-noun negative families); (B) surface-flip pairs — same concept token in two different carrier sentences, for the unit-level surface-invariance admission check; (C) a frozen pile-uncopyrighted (rev 3be90335b66f24456a5d6659d9c8d208c0357119) diagnostic corpus of real natural-text windows labelled by frozen sub-context, plus matched negatives (no-digit, city-mention, no-country), so iter-2 can train a parent linear probe and run the per-sub-context false-negative (parent-hole) search.

  Every row marks the exact target span (target_text + char_start/char_end) and carries precomputed google/gemma-2-2b token indices (100% coverage; the tokenizer splits numbers into individual digit tokens). Sub-context labels are assigned purely from surface form / regex / gazetteer (pycountry + geonamescache) — independent of any SAE latent or model behaviour — so the degenerate-construction guard holds and the same labelled corpus equally supports the honest 'absorption is spelling-specific' null (uniform high parent-probe recall across sub-contexts). Frozen folds (seed 20240617): pairs split train/test 70/30 by pair_id (stratified by sub_context); corpus splits train/diagnostic 50/50 (stratified). absorption_readiness in manifest.json: ALL 8 numeric sub-contexts and 20 countries reach ≥150 diagnostic-fold positives (eligible for the inferential test); rarer sub-contexts/countries are kept and flagged descriptive_only. Content-flip (≥240) and surface-flip (≥120) per-hierarchy floors are exceeded. A deterministic templated backbone is supplemented by openai/gpt-4o-mini generation, with every content/surface pair (LLM-generated + 20% templated spot-check) LLM-judged on content_flipped/surface_preserved/grammatical — 100% pass at $0.0104 total spend (hard cap $4, ceiling $10). Ambiguous homographs (Georgia, Turkey, Chile, Jordan) and multi-word countries are flagged via metadata_notes / metadata_multi_token.

  Deliverables: data.py (canonical builder), pipeline.py + build_dataset.py (logic modules), full/mini/preview_data_out.json, schema.json (JSON Schema + logical nested view), manifest.json (per-sub-context counts, fold counts, pass rates, spend, pile revision, readiness), and pyproject.toml with pinned dependency versions. Reproduce with `python3 data.py --scale full`. iter-2 consumes this to run the Tier-0 non-triviality pre-check (does a high-recall parent latent exist AND have specialist-filled holes?), the form-free absorption diagnostic as oracle, and the K-track anchored greedy set-cover proposal step — with numeric as the primary novelty test and taxonomic as the pre-registered alternative.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_2
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json

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

- **Multi-LLM Agents** — framework choices, implementation patterns, agent orchestration
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
TODO 1. Use aii-json skill's format script with `--input method_out.json` to generate full, mini, and preview versions. If not in your workspace (see <workspace> above), copy them there. Run 'ls -lh' to verify these three files exist (DO NOT read them).
TODO 2. Apply aii-file-size-limit skill's file size check procedure (100MB limit) to method_out.json and full_method_out.json.
TODO 3. Ensure a `pyproject.toml` exists in your workspace with ALL dependencies pinned to the exact versions installed in your .venv (run `.venv/bin/pip freeze` to get them). This is required for reproducibility. The [project] section must include name, version, requires-python, and a dependencies list with pinned versions (e.g. `numpy==2.0.2`, not `numpy>=2.0`).
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ExperimentExpectedFiles": {
      "description": "All expected output files from experiment artifact.",
      "properties": {
        "script": {
          "description": "Path to method.py script. Example: 'method.py'",
          "title": "Script",
          "type": "string"
        },
        "full_output": {
          "description": "Full method output JSON file. Example: 'full_method_out.json'",
          "title": "Full Output",
          "type": "string"
        },
        "mini_output": {
          "description": "Mini method output JSON file. Example: 'mini_method_out.json'",
          "title": "Mini Output",
          "type": "string"
        },
        "preview_output": {
          "description": "Preview method output JSON file. Example: 'preview_method_out.json'",
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
      "title": "ExperimentExpectedFiles",
      "type": "object"
    }
  },
  "description": "Experiment artifact \u2014 structured output + file metadata.\n\nImplements research methodology with baseline comparison.\nProduces method.py and method_out.json files.",
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
      "$ref": "#/$defs/ExperimentExpectedFiles",
      "description": "All output files you created. Must include method.py script plus full/mini/preview method output JSON files."
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
  "title": "ExperimentArtifact",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````
