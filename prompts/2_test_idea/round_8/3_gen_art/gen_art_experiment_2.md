# gen_art_experiment_2 — test_idea

> Phase: `invention_loop` · round 8 · `gen_art`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_experiment_2` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 10:51:16 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_experiment_2`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_experiment_2/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_experiment_2/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_experiment_2/results/out.json`
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
id: gen_plan_experiment_2_idx2
type: experiment
title: >-
  Base-Widener + Concentration-vs-Absorption Population Test (iter-8 M2''' + M3''')
summary: >-
  Screen a WIDER vocabulary of candidate tokens (first-letter spelling word-absorbers L/O/T/I/D + homograph entities/given-names/brands/months)
  for lexical CONCENTRATION (per-sub-context firing precision x sparse footprint), independent of absorption structure, then
  run the IDENTICAL unified fair-gated edit (the new DENSE-SUB-ABL-GATED-FAIR = u_sub gated by the precise d_sub detector
  with bounded beta<=1) on the most-concentrated candidates. Report (1) how many candidates clear the fair-control bar at
  MEANINGFUL forget => additional independent concentrated wins beyond large/Amazon (verdict BASE_REACHES_4_PLUS vs BASE_STAYS_THIN_RETARGET);
  (2) whether a candidate's continuous CONCENTRATION score predicts its edit-win/meaningful-forget outcome better than its
  binary ABSORPTION-regime label (the decisive M3''' population evidence); (3) per candidate, whether the precision-selected
  absorber EQUALS the unconstrained max-precision latent (set-cover inertness, M5'''). Reuses iter-7 core.py/method.py VERBATIM
  for the SAE pipeline, edit operators, judges, u_sub/d_sub, and meaningful-forget proof; adds ONE new operator, a $0 concentration
  screen, a budget-bounded edit loop, and the population correlation. Compute: GPU (gemma-2-2b + Gemma-Scope L12/16k). LLM
  judge target <$3, hard cap $10.
runpod_compute_profile: gpu
implementation_pseudocode: |
  ############################################################################
  # WORKSPACE: 3_invention_loop/iter_8/gen_art/gen_art_experiment_2  (executor's CWD)
  # READ-ONLY INPUTS (existing run-tree artifacts, accessed by absolute path):
  #   CORE7 = 3_invention_loop/iter_7/gen_art/gen_art_experiment_1/core.py     (SAE+edit machinery)
  #   METH7 = 3_invention_loop/iter_7/gen_art/gen_art_experiment_1/method.py   (u_sub/d_sub/judge/forget proof)
  #   KG4   = 3_invention_loop/iter_4/gen_art/gen_art_experiment_1/method_out.json (named absorbers)
  #   D1    = 3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json (first-letter spelling; art_dpYpjSn2Xvg3)
  #   D2    = 3_invention_loop/iter_1/gen_art/gen_art_dataset_2/full_data_out.json (taxonomic+numeric; for distributed-absorption population anchors Georgia/Jordan)
  #   HG_DIR= 3_invention_loop/iter_5/gen_art/gen_art_dataset_1                  (homograph entities; art_2xQn686KUmV5)
  #   DOSS  = 3_invention_loop/iter_1/gen_art/gen_art_research_1/research_out.json (SAE pins + baseline specs; art_RidEJtBC7gPT)
  # SAE pins (from core.py / dossier, DO NOT change): release google/gemma-scope-2b-pt-res,
  #   layer_12/width_16k/average_l0_82/params.npz, d_model 2304, hook blocks.12.hook_resid_post,
  #   model google/gemma-2-2b (mirror unsloth/gemma-2-2b), SEED 1234, B_BOOT 10000.
  ############################################################################

  # ============================ STEP A. ENV + REUSE (verbatim copy, not cross-dir import) ===========
  # Cross-dir import is unsafe because CORE7/METH7 hardcode WORK=iter_7 and create RESULTS/CACHE/LOGS there.
  #  - `uv init`; install: torch (CUDA cu124: `uv pip install torch --index-strategy unsafe-best-match`,
  #    add `--link-mode=copy` because the venv lives on mfs), transformers, numpy, scipy, scikit-learn,
  #    loguru, requests, huggingface_hub. Mirror iter-7 pyproject.toml.
  #  - Copy CORE7 -> ./core.py and METH7 -> ./method_lib.py VERBATIM. In BOTH, repoint the module-level
  #    WORK constant to THIS workspace so RESULTS/CACHE/LOGS/cache land here (never write into iter_7).
  #    Keep _find_sae_params() (auto-locates the cached SAE npz) and the unsloth fallback loader untouched.
  #  - Set HF_HUB_OFFLINE=1 if the SAE+model are already cached; else allow one download. HF_TOKEN optional
  #    (unsloth mirror is ungated). cache/ holds encodings + is EXCLUDED from upload (.gitignore-style).
  #  - aii-openrouter-llms for the judge; reuse METH7 judge infra (PRIMARY=anthropic/claude-haiku-4.5,
  #    SECOND auto-resolved from gpt-4o-mini / gemini-2.5-flash). Global SPENT cap TARGET=3.0, HARD_CAP=10.0.

  # ============================ STEP B. ADD THE NEW FAIR-GATED OPERATOR (the only genuinely-new edit code) =====
  # In ./core.py add kind=='erase_dir_gated_fair' to make_edit_hook(), _make_clamped_hook(),
  # and thread it through read_resid_under_edit()/forward_pos_logprobs()/behavioral_curve()/generate_under_edit().
  # Extend the hook signature with: gw (d_sub weight tensor [d_model]), gb (d_sub bias float), beta (<=1), gate_thresh.
  # Operator (UNIFIED, identical to iter-8 Artifact-1 spec -> MINOR-4 unification):
  #     dot  = h @ u                                   # u == unit u_sub (the labeled sub-direction; full projection)
  #     gate = (h @ gw + gb) > gate_thresh             # PRECISE d_sub detector (AUC~1.0) decides WHERE to erase
  #     hf   = hf - min(beta,1.0) * dot.unsqueeze(-1) * u.view(1,1,-1) * gate.unsqueeze(-1).to(hf.dtype)
  #     counter['edited'] += int(gate.sum()); counter['total'] += int(gate.numel())
  # RATIONALE vs iter-7 erase_dir_gated: iter-7 gated on |h.u_sub|>tau (a CRUDE magnitude gate calibrated to a
  # 3% GLOBAL footprint) which forced beta~2.97 over-erasure. THIS gate uses the precise supervised d_sub and
  # CAPS beta at 1.0 (beta=1 == full removal of the labeled component at exactly the detected X tokens), so it is
  # the genuinely-FAIR conditional-dense control. gate_thresh default 0.0 (prob 0.5); also record an alt calibration
  # where gate_thresh is set so the gate's X-recall equals the KG absorber's X firing-recall (report both, primary=0.0).

  # ============================ STEP C. BUILD THE CANDIDATE POOL ($0) ================================
  # C1. SPELLING word-absorbers (hierarchy='first_letter_spelling', parent=<letter>):
  #   curated = {L: large,list,line,law,like,level,low,leave,land,life ; O: our,one,only,other,out,over ;
  #              T: that,their,there,time,take,this ; I: in,into,it,is,if ; D: day,down,do,did,does}
  #   UNION the NON-EMPTY words in KG4.metadata.canonical_units.first_letter.{L,O,T,I,D}.sub_by_absorber
  #   (e.g. L: 3069->list, 2416->line, 3353->level, 3858->low, 7544->leave). Keep only words present in D1's
  #   per-letter corpus with >=12 word-initial windows (load via core.load_first_letter(['L','O','T','I','D'])).
  #   The absorber latent is RE-DERIVED in STEP D (do NOT trust sub_by_absorber gaps; large->8463 came from iter-7
  #   re-derivation, not iter-4). Carry 'large'=8463 as a hardcoded positive-control anchor.
  # C2. HOMOGRAPH entities (hierarchies city/month/given_name/brand):
  #   The shipped HG_DIR/full_data_out.json + manifest.json are ABSENT on disk -> REBUILD first (exactly as the
  #   iter-6 router experiment did): copy HG_DIR to ./homograph_data/, run `python pipeline.py --scale full --no-llm`
  #   there ($0, writes full_data_out.json + manifest.json). Read manifest.absorption_readiness per (hierarchy,entity);
  #   keep entities with status 'eligible' (>=150 diagnostic positives) OR diagnostic_positives>=120.
  #   curated must-include (reviewer-named): Apple,Shell,Target,Orange (brand); Grace,Hope,Mark,Will (given_name);
  #   March,June,May (month); Amazon,Bush,Cook (positive-control anchors from iter-7). sub_context=entity in TARGET
  #   sense; siblings=other eligible entities SAME hierarchy in target sense; hard-negatives=homograph_competitor rows.
  # C3. DISTRIBUTED-ABSORPTION population anchors (load from D2 via core.load_taxonomic): Georgia(16009),
  #   Jordan(540) -- known NO_MEANINGFUL_FORGET losers. Include 2-3 so the population scatter has the
  #   low-concentration/absorption-structured quadrant (else the M3''' contrast is unidentified).
  # Each candidate := {token, hierarchy, parent, dataset_handle}.  Expect ~45-70 candidates total.

  # ============================ STEP D. PER-CANDIDATE CONCENTRATION SCREEN ($0, GPU encode, cached) ===
  # load_sae(); ModelBundle(); determine_layer_idx() once (expect idx 13, FVU~0.19, cosine>0.9 gating PASS).
  # Build a NEUTRAL token pool (core.NEUTRAL_TEXT) once for footprint calibration.
  # for cand in pool:
  #   rows_X    = corpus windows where token appears in TARGET sense  (held-out fold for eval; disjoint fit fold for u_sub/d_sub)
  #   rows_SIB  = corpus windows of SIBLING tokens (same hierarchy, target sense)
  #   pairs     = content_pairs (x_on/x_off) for the token if present (spelling+homograph ship these)
  #   lat_csr, resid = mb.encode_rows(rows_X+rows_SIB+pairs)         # cache under cache/enc_<cand>_*.npz
  #   cr, prec_vec, _ = core.content_responsive(A_on, A_off)         # per-latent content-responsiveness + precision
  #   anchor      = highest-recall content-responsive latent on PARENT contexts (hierarchy-level; reuse KG4 anchor when available)
  #   recall_hole = 1 - mean(anchor fires on rows_X)
  #   # K-track precision selection (anchored, recall-hole-guided) -> the 'absorber' the method discovers:
  #   absorber    = argmax over cr latents s.t. firing_Jaccard(l,anchor)<0.1 AND precision_on_X(l)>=0.7 of coverage(l on rows_X)
  #                 (if none qualifies -> absorber=None, candidate flagged structure_absent, still screened for concentration)
  #   # UNCONSTRAINED max-precision selector (M3''' / M5''' baseline -- NO anchor/Jaccard constraint):
  #   max_prec_latent = argmax over cr latents with firing_on_X>=min_fire of precision_on_X(l)
  #   precision   = precision_on_X(absorber or max_prec_latent)
  #   footprint   = mean over NEUTRAL pool tokens of (chosen latent fires)   # forward over NEUTRAL_TEXT, count z[l]>0
  #   concentration_score = precision * (1 - footprint)                      # high precision AND sparse => concentrated
  #   firing_jaccard      = Jaccard(absorber/parent positive-token sets)
  #   absorption_structured = (recall_hole >= 0.6) and (firing_jaccard < 0.1)  # REPORTED, never gates the screen
  #   set_cover_eq_max_precision = (absorber is not None and absorber == max_prec_latent)
  #   record screen_row{token,hierarchy,precision,footprint,concentration_score,recall_hole,firing_jaccard,
  #                     absorber,max_prec_latent,set_cover_eq_max_precision,absorption_structured}
  # rank pool by concentration_score DESC.

  # ============================ STEP E. EDIT SET SELECTION (gradual scaling, breadth-first) ==========
  # edit_set = top-K by concentration_score (K ~= 10-14, concentrated co-firing candidates ARE eligible -- the
  #   reframe predicts they can win) UNION the population anchors {large(8463), Amazon, Bush, Cook} (positive controls,
  #   re-run to confirm the pipeline reproduces iter-7's KG win) UNION {Georgia, Jordan} (distributed-absorption losers).
  # Edit MOST-CONCENTRATED FIRST so breadth of independent wins is maximized before budget/time exhausts.
  # Use aii-long-running-tasks gradual pattern: smoke(2 cands) -> mini(5) -> full. Track SPENT after every judge batch.

  # ============================ STEP F. PER-CANDIDATE EDIT + MATCHED-FORGET COMPARISON ==============
  # for cand in edit_set (ordered):
  #   u_sub, u_meta = method_lib.build_u_sub(resid, X_pos_fit_mask, SIB_pos_fit_mask, probe.d_mu, fb...)
  #   d_sub         = method_lib.fit_sub_probe(resid, X_pos_fit_mask, SIB_pos_fit_mask)   # frozen {w,b,auc}; need auc>~0.9
  #   if u_meta.underpowered (n_pos<MIN_SUB=20) or d_sub is None: mark descriptive_only, emit screen row, CONTINUE
  #   # ---- OPERATORS (sweep each; all share ONE u_sub + ONE d_sub) ----
  #   OPS = {
  #     'KG-ABL'                  : (abl_latent,           l=absorber,          sweep LAM_GRID [0,.5,1,2,3,4]),
  #     'DENSE-SUB-ABL'           : (erase_dir,            u=u_sub,             sweep BETA_GRID [0,.5,1,1.5,2,3,4,6,8])  # LEAD comparator (strongest ungated dense),
  #     'DENSE-SUB-ABL-GATED-FAIR': (erase_dir_gated_fair, u=u_sub,gw=d_sub.w,gb=d_sub.b,gate_thresh=0, sweep beta [0,.25,.5,.75,1.0])  # BOUNDED beta<=1 (establishing control),
  #     'MAX-PREC-ABL'            : (abl_latent,           l=max_prec_latent,   sweep LAM_GRID)  # M3''' set-cover-vs-max-precision ablation
  #   }
  #   # ---- BEHAVIORAL forget curve per op (M4''': match on BEHAVIOR, NOT next-token KL) ----
  #   base_rate = subprobe_positive_rate(d_sub, resid_of(X_held_rows))   # ~1.0
  #   for op,scale: resid_e = read_resid_under_edit(X_held_rows, kind=op,...,scale); sub_drop(op,scale)=base_rate-subprobe_positive_rate(d_sub,resid_e)
  #   completion_drop via method_lib.completion_drop with TEMPLATED probes (M4''' ~20-50/case):
  #       spelling: ['{w} starts with the letter','The first letter of the word {w} is','{w} is spelled starting with',
  #                  'The word {w} begins with the letter', ... ~10 templates] gold=first letter (uppercase)
  #       homograph: target-sense completions where templatable (brand: '{e} announced a new'->product;
  #                  month: 'The month after {prev} is'->{e}; given_name: weak->rely on sub_drop); else completion=None.
  #   # ---- MATCHED MEANINGFUL-FORGET POINT (behavioral) ----
  #   FORGET_FLOOR=0.10 (meaningful); matched_target = max(FORGET_FLOOR, 0.8*min_op(max achievable sub_drop))
  #   for op: s_op = smallest scale whose interpolated sub_drop reaches matched_target; if op cannot reach it within its
  #           sweep (esp FAIR-GATED at beta=1.0) -> op_saturated=True, s_op=max-forget scale, note 'cannot match'.
  #   meaningful_forget = (KG sub_drop at s_KG >= 0.10) AND (completion drop CI>0 OR KG sub_drop>=0.10)  # success-criteria OR
  #   # ---- JUDGED JOINT at the matched point (2 judges) ----
  #   prompts: FORGET (~24, prefixes from X-held rows), RETAIN (~20, sibling rows), UNRELATED (~20, NEUTRAL_TEXT)
  #   for op: conts = generate_under_edit(prompts, kind=op,...,scale=s_op, clamp_norm=True)
  #           judge each (claude-haiku + 2nd) -> {fluency0-2, content_pres0-2}; joint=HM(fluency,content_pres)
  #           op_joint = aggregate(forget_quality on FORGET, preservation on RETAIN+UNRELATED)   # iter-7 convention
  #   Delta_joint(KG vs DENSE-SUB-ABL)     = paired_bootstrap_diff(joint_KG, joint_ungated)  per judge, B=10000
  #   Delta_joint(KG vs DENSE-SUB-ABL-GATED-FAIR) = paired_bootstrap_diff(...)               per judge, B=10000
  #   KG_beats_ungated  = both judges' CI excl 0 favoring KG
  #   KG_beats_fair     = both judges' CI excl 0 favoring KG (if fair op_saturated below match: KG auto-wins on forget,
  #                       still report the joint delta at the common achievable forget + the saturation note)
  #   concentrated_win  = meaningful_forget AND KG_beats_fair
  #   emit per-(token,role,prompt) prediction rows: predict_kg_abl/predict_dense_sub_abl/predict_dense_sub_gated_fair/
  #       predict_max_precision/predict_noop = the continuation STRINGS (all rows MUST carry these as strings -> validator),
  #       + per-op joint, sub_drop, footprint, s_op utilities.
  #   STOP issuing NEW judge calls once SPENT>=TARGET; remaining edit_set candidates fall back to $0 screen-only rows
  #   (concentration + structure + set_cover flag computed, edit/Delta marked budget_skipped).

  # ============================ STEP G. VERDICT (base count, M2''') ================================
  # known_wins = {'large','Amazon'} (iter-7); re-confirmed here as positive controls (assert KG_beats_fair reproduces;
  #   if a control FAILS to reproduce, that is a flagged honest negative about the new fair operator, not a silent pass).
  # new_wins = {token : concentrated_win True and token not in known_wins}
  # total_independent_concentrated_wins = | dedupe_by_token(known_wins UNION new_wins) |
  # verdict = 'BASE_REACHES_4_PLUS' if total>=4 else 'BASE_STAYS_THIN_RETARGET'
  #   (the latter triggers the paper retarget to 'localization+editing of homograph-polysemy absorption').

  # ============================ STEP H. POPULATION PREDICTOR ANALYSIS (decisive M3''' evidence) =====
  # over EDITED candidates that produced a Delta_joint (include the Georgia/Jordan distributed anchors + any co-firing):
  #   features: C=concentration_score (continuous), S=absorption_structured (binary 0/1)
  #   outcomes: Ymag=Delta_joint(KG vs fair) (continuous win-magnitude), Ywin=concentrated_win (binary 0/1)
  #   spearman(C,Ymag)+bootstrap CI ; point_biserial(C,Ywin)+CI
  #   point_biserial(S,Ymag)+CI     ; phi/point_biserial(S,Ywin)+CI
  #   predictor_verdict = 'CONCENTRATION_PREDICTS' if |corr(C,.)| CI is higher and excludes 0 while |corr(S,.)| does not,
  #                       'ABSORPTION_PREDICTS' if reverse, else 'TIE/UNDERPOWERED' (report n and CIs honestly).
  #   set_cover_inertness_rate = mean(set_cover_eq_max_precision over candidates with an absorber)  # M5'''
  #   (Report the expected story per the reframe: a concentrated CO-FIRING latent CAN win; Georgia/Jordan absorb but
  #    have LOW concentration and lose. Do NOT assert it -- let the correlation+CI decide; underpowered is reportable.)

  # ============================ STEP I. OUTPUT (exp_gen_sol_out schema) =============================
  # method_out.json:
  #   metadata: {method_name, description, sae{release,sae_params,width,d_model,hook}, model, seed, B_boot,
  #     gating_check{cosine,L0,fvu_by_idx,layer_idx}, forget_grids, judge{models,target_usd,hard_cap,spent_usd,calls},
  #     fair_gate_spec{operator='erase_dir_gated_fair', beta_cap=1.0, gate_thresh_primary=0.0, gate_alt='X-recall-matched'},
  #     concentration_screen_table:[per-candidate dict],
  #     base_count{known_wins, new_wins, total_independent_concentrated_wins, verdict},
  #     population_predictor{spearman_conc_mag_ci, pb_conc_win_ci, pb_absorp_mag_ci, pb_absorp_win_ci, predictor_verdict, n},
  #     set_cover_inertness_rate,
  #     honest_negatives:[ verbatim list -- see fallback ] }
  #   datasets:
  #     {dataset:'concentration_screen', examples:[ one per candidate; input=human-readable desc, output=tag
  #        ('concentrated_win'/'meaningful_no_win'/'no_meaningful_forget'/'structure_absent'/'budget_skipped'),
  #        metadata_*: token,hierarchy,precision,footprint,concentration_score,recall_hole,firing_jaccard,absorber,
  #        max_prec_latent,set_cover_eq_max_precision,absorption_structured,meaningful_forget,
  #        delta_joint_vs_ungated_{primary,second}_{diff,ci_lo,ci_hi,excl0}, delta_joint_vs_fair_{...},
  #        kg_beats_ungated,kg_beats_fair,fair_saturated, AND predict_* STRING fields (set to op tag/'NA') ]},
  #     {dataset:'edit_predictions', examples:[ per (token,role,prompt): input=prompt, output=role,
  #        predict_kg_abl, predict_dense_sub_abl, predict_dense_sub_gated_fair, predict_max_precision, predict_noop
  #        (continuation STRINGS), metadata_*: token,role,sub_probe_drop_kg, joint_kg, joint_ungated, joint_fair, s_op_* ]}
  #   EVERY example in EVERY dataset MUST carry the five predict_* keys as STRINGS (iter-5 GOTCHA: missing/
  #   non-string predict_* => validator FAIL). Use make_variants.py (copied from iter-7) to emit
  #   full/mini/preview_method_out.json each <100MB; validate all three with aii-json against exp_gen_sol_out.
  #   Exclude cache/ and .venv/ from the uploaded artifact.

  # ============================ COST / TIME BUDGET ==================================================
  # $0 screen over the full pool first. Editing ~12-16 candidates x 2 judges x ~64 continuations ~= $1.5-2.5 (iter-7
  # was $0.80 for 5 cases). Hard-stop judge calls at SPENT>=3.0. GPU wall-clock budget ~5h of the 6h: encoding is the
  # bulk (cached); generation+forward sweeps dominate per edited candidate (~10-15 min each). PID-based process mgmt only.
fallback_plan: |-
  DATA / REBUILD failures: (1) If `pipeline.py --scale full --no-llm` for the homograph dataset errors (geonamescache/protobuf/libgomp quirks seen in prior iters), fall back to `--scale smoke` for structure then hand-load the entities directly from HG_DIR/data.py's entity gazetteers + D1-style corpus windows; if it still fails, DROP the homograph hierarchies and run the base-widener on SPELLING words alone (L/O/T/I/D give 20-40 candidates -- enough for the population test and >=4-win target on concentrated spelling absorbers). (2) If a candidate has too few corpus positives for a trustworthy u_sub/d_sub (n_pos<MIN_SUB=20, AUC<0.9), mark it descriptive_only and keep it in the $0 screen (still contributes concentration + structure + set_cover flag) but exclude from the edit/Delta analysis -- report the excluded count.
  OPERATOR failures: (3) If the bounded-beta (<=1) fair-gated dense CANNOT reach the matched meaningful-forget for many candidates, that is a SUBSTANTIVE result, not a bug: KG wins on forget by construction -- report it as 'fair gated dense saturates below meaningful forget at beta<=1' and compare joint collateral at the common achievable forget. Also run the alt gate_thresh (X-recall-matched) to show the conclusion is calibration-robust. (4) If generation NaNs in bf16, use the clamp_norm=True path (_make_clamped_hook, already supports the new operator).
  BUDGET / TIME truncation (pre-registered drop order, breadth-first): keep the $0 full-pool concentration screen + set_cover_inertness ALWAYS (they alone answer M3''' structurally and M5'''); then the positive-control re-runs (large, Amazon); then top-concentration new candidates until SPENT>=3.0 or time runs low; DROP (first-dropped-first) the MAX-PREC-ABL judged edit (keep its $0 set_cover_eq flag), then the second judge on lowest-concentration candidates (keep primary), then the distributed-absorption Georgia/Jordan re-edit (cite iter-7 numbers as population anchors instead). NEVER drop: the concentration screen, >=the two positive-control wins, the population correlation over whatever edited points exist.
  VERDICT robustness: (5) If <4 independent concentrated wins land, emit BASE_STAYS_THIN_RETARGET honestly (this is an expected, publishable outcome that triggers the paper's localization-first retarget) -- do NOT inflate by re-counting the confirmatory Amazon or the excluded co-firing insult as load-bearing. (6) If the population correlation is underpowered (too few edited points / wide CIs), report 'TIE/UNDERPOWERED' with n and CIs rather than asserting CONCENTRATION_PREDICTS.
  HONEST NEGATIVES to record verbatim in metadata.honest_negatives: fair-gated-dense matches KG (=> value is label-free where-to-gate discovery, gating is prior art CAST/GSS/GUARD-IT/SADI); set-cover absorber == max-precision latent for most candidates (=> method is precise-latent discovery, set-cover inert); base stays thin (n~2-3) => retarget; concentration does NOT out-predict absorption (=> reframe unsupported, report as-is); distributed-absorption candidates show no meaningful forget (carries iter-7 Georgia/Jordan); homograph rebuild required (data not shipped); positive control fails to reproduce under the new fair operator.
testing_plan: |-
  1) SMOKE (logic, ~2-5 min, $0): run with a 2-candidate pool {large (spelling, known win), Georgia (taxonomic, known no-forget loser)} and tiny caps (cap=20 rows, 3 FORGET/2 RETAIN prompts, judges DISABLED by unsetting OPENROUTER_API_KEY). CONFIRM: SAE loads (d_sae=16384, d_model=2304), determine_layer_idx selects 13 with cosine>0.9 (gating PASS), encode_rows runs, the new erase_dir_gated_fair hook executes without shape/NaN errors and its token-footprint counter is >0 on X tokens and ~0 on neutral tokens, content_responsive returns cr latents, the concentration screen emits rows with precision/footprint/concentration_score in [0,1], and large's re-derived absorber == 8463 (sanity vs iter-7). Output a valid (judge-less) method_out.json skeleton.
  2) OPERATOR UNIT CHECK ($0): on 'large', verify (a) KG-ABL sub-probe positive-rate drops monotonically with lambda; (b) DENSE-SUB-ABL-GATED-FAIR at beta=1.0 produces a LARGE sub_drop ON X tokens but tiny token_footprint on UNRELATED/neutral text (precise gate), and at beta=1.0 the on-X erasure is full-projection (sub_drop>=ungated at matched gate) -- confirming it is a strong, fair, non-over-erasing control; (c) MAX-PREC-ABL on 'large' selects a latent and set_cover_eq_max_precision resolves to a definite bool. Print the matched-forget scales s_op and confirm they are finite.
  3) MINI (~15-25 min, <$0.5): 5 candidates {large, Amazon (rebuild homograph first), one new concentrated spelling word, one new homograph entity, Jordan}. ENABLE both judges on a reduced prompt set (~10/role). CONFIRMATION SIGNALS before scaling: large reproduces KG_beats_fair (positive control passes); Jordan shows NO meaningful forget (sub_drop<0.10); Delta_joint CIs compute under both judges; SPENT tracked and well under TARGET; the population-predictor function runs on >=4 points without error. If the large positive control does NOT reproduce a KG win under the new fair operator, STOP and debug the operator/gate calibration before spending more budget.
  4) FULL: only after mini confirms the positive control + judge pipeline + cost tracking. Screen the full pool ($0), then edit most-concentrated-first until SPENT approaches 3.0 or ~5h elapsed. After completion: validate full/mini/preview method_out.json with aii-json against exp_gen_sol_out (every example has the 5 predict_* STRING keys), confirm each variant <100MB, confirm cache/ excluded. Sanity-check the verdict arithmetic (total_independent_concentrated_wins dedup by token) and that honest_negatives reflects the actual outcome (no inflation of confirmatory/co-firing cases into the load-bearing count).
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

--- Dependency 3 ---
id: art_2xQn686KUmV5
type: dataset
title: >-
  Homograph/Polysemy Entity Absorption Testbed (cities, months, given-names, brands)
summary: |-
  A pure CPU/text artifact: a FOUR-hierarchy homograph/polysemy entity absorption testbed, built as a strict structural drop-in extension of the iter-1 non-spelling absorption testbed (art_t2uUbjSwpd3t). It is explicitly a NEXT-ITERATION BUILDING BLOCK (not consumed by this iteration's parallel experiments): it supplies breadth of suppressed-parent candidates so the persistent single-slice taxonomic critique (Georgia-only) can be answered with many homograph cases.

  Four `dataset`s, one per is-a hierarchy, whose surface tokens carry a strong competing NON-target sense (the competition that produces feature absorption / a suppressed-parent recall hole):
    1. city_homograph_absorption  (parent = is-a-city): Phoenix, Mobile, Reading, Bath, Nice, Buffalo, Paris, Mercury, Jackson, Columbus, Cleveland, Florence, ... (23 entities).
    2. month_name_absorption (parent = is-a-month): all 12 calendar months; homograph-strong May/March/August/April/June.
    3. given_name_absorption (parent = is-a-given-name): Grace, Hope, Mark, Will, Rose, Frank, Faith, Joy, Dawn, Jack, ... (34 entities).
    4. brand_homograph_absorption (parent = is-a-brand): Apple, Amazon, Shell, Target, Orange, Gap, Tide, Visa, Subway, Java, ... (24 entities).

  Each hierarchy ships the SAME three coordinated components as dataset_2: (A) content-flip minimal pairs (parent present vs absent, surface-matched), (B) surface-flip pairs (concept fixed, surface varied; both positive, for the unit-level surface-invariance check), and (C) a frozen monology/pile-uncopyrighted diagnostic corpus (pinned rev 3be90335b66f24456a5d6659d9c8d208c0357119) of real windows labelled by frozen, model-independent sub-context. The NEW homograph_competitor negative family (the same surface token in its non-target sense, e.g. lowercase 'apple'/'will'/'march', 'Joaquin Phoenix', 'Christopher Columbus') is the matched hard control that makes a suppressed parent visible.

  On-disk format is the AII exp_sel_data_out schema: {metadata, datasets:[{dataset, examples:[{input, output, metadata_*}]}]} with FLAT metadata_* keys (no nested objects). New/extended fields vs iter-1: metadata_hierarchy (city|month|given_name|brand), metadata_entity (canonical surface), metadata_target_sense (city|month|given_name|brand|competitor|null), metadata_competitor_sense (gloss of competing sense), metadata_homograph_strength (wordfreq Zipf of the lowercase competitor), and metadata_neg_family expanded to include homograph_competitor / other_place / other_time / other_person_ref / other_company_ref / easy. Fold semantics are unchanged (pairs 70/30 train/test by pair_id stratified by sub_context; corpus 50/50 train/diagnostic stratified), gemma-2-2b offset-mapping token anchoring is reused (metadata_target_token_indices), and the downstream K-track + form-free absorption diagnostic pipeline runs unchanged except for the new enum values.

  Labels are assigned PURELY from surface form / regex / gazetteer (geonamescache for cities) / disambiguating local context — never from a model — so the degenerate-construction guard holds and absorption presence/absence stays a future-iteration EMPIRICAL finding: the corpus equally supports the 'absorption is spelling-specific' null and a positive homograph-absorption finding. Corpus target-sense labels use high-precision case-aware cues; an LLM-judged stratified sample MEASURES per-hierarchy target-sense precision (reported in manifest.json, target >=0.9; it does not relabel the corpus). manifest.json carries per-(hierarchy,entity) absorption_readiness with diagnostic_positives counts and status (eligible if >=150 diagnostic-fold positives, else descriptive_only), eligible_entities_per_hierarchy, per-component counts, source/pile-set counts, llm_pair_pass_rate, llm_corpus_sense_precision, llm_cost_breakdown, city geonames provenance, and cross-hierarchy collision notes (Dawn, Chase, Jordan, Mercury, Paris). Deliverables: data.py, build_dataset.py, pipeline.py, schema.json, manifest.json, and full/mini/preview_data_out.json (validated against exp_sel_data_out, each <100MB). Reproducible via fixed seed 20240617 and pinned pile revision; total LLM spend well under $1.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_dataset_1
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

### [2] HUMAN-USER prompt · 2026-06-18 10:51:16 UTC

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

### [3] SKILL-INPUT — aii-long-running-tasks · 2026-06-18 10:51:46 UTC

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

### [4] SKILL-INPUT — aii-use-hardware · 2026-06-18 10:51:46 UTC

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

### [5] SYSTEM-USER prompt · 2026-06-18 19:59:22 UTC

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

<CRITICAL_WARNING__PREVIOUS_ATTEMPT_CRASHED>
YOUR PREVIOUS EXECUTION ATTEMPT CATASTROPHICALLY FAILED.
The entire worker container crashed after 765s.
Error: Pod launch failed — no instance booted (tried 4, 11 still out of stock): Container did not start within 240s on 8zu2qu2axkdeih (container_running=false, uptime=0, host_id=8zu2qu2axkdeih-64411ae3)

This was NOT a normal code error — the entire container died. Study the error
and last messages above carefully. Identify what caused the crash and be
EXTREMELY careful to avoid repeating it. Do NOT use the same approach.
</CRITICAL_WARNING__PREVIOUS_ATTEMPT_CRASHED>

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_2`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_2/`:
GOOD: `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_2/file.py`, `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_2/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_experiment_2_idx2
type: experiment
title: >-
  Base-Widener + Concentration-vs-Absorption Population Test (iter-8 M2''' + M3''')
summary: >-
  Screen a WIDER vocabulary of candidate tokens (first-letter spelling word-absorbers L/O/T/I/D + homograph entities/given-names/brands/months)
  for lexical CONCENTRATION (per-sub-context firing precision x sparse footprint), independent of absorption structure, then
  run the IDENTICAL unified fair-gated edit (the new DENSE-SUB-ABL-GATED-FAIR = u_sub gated by the precise d_sub detector
  with bounded beta<=1) on the most-concentrated candidates. Report (1) how many candidates clear the fair-control bar at
  MEANINGFUL forget => additional independent concentrated wins beyond large/Amazon (verdict BASE_REACHES_4_PLUS vs BASE_STAYS_THIN_RETARGET);
  (2) whether a candidate's continuous CONCENTRATION score predicts its edit-win/meaningful-forget outcome better than its
  binary ABSORPTION-regime label (the decisive M3''' population evidence); (3) per candidate, whether the precision-selected
  absorber EQUALS the unconstrained max-precision latent (set-cover inertness, M5'''). Reuses iter-7 core.py/method.py VERBATIM
  for the SAE pipeline, edit operators, judges, u_sub/d_sub, and meaningful-forget proof; adds ONE new operator, a $0 concentration
  screen, a budget-bounded edit loop, and the population correlation. Compute: GPU (gemma-2-2b + Gemma-Scope L12/16k). LLM
  judge target <$3, hard cap $10.
runpod_compute_profile: gpu
implementation_pseudocode: |
  ############################################################################
  # WORKSPACE: 3_invention_loop/iter_8/gen_art/gen_art_experiment_2  (executor's CWD)
  # READ-ONLY INPUTS (existing run-tree artifacts, accessed by absolute path):
  #   CORE7 = 3_invention_loop/iter_7/gen_art/gen_art_experiment_1/core.py     (SAE+edit machinery)
  #   METH7 = 3_invention_loop/iter_7/gen_art/gen_art_experiment_1/method.py   (u_sub/d_sub/judge/forget proof)
  #   KG4   = 3_invention_loop/iter_4/gen_art/gen_art_experiment_1/method_out.json (named absorbers)
  #   D1    = 3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json (first-letter spelling; art_dpYpjSn2Xvg3)
  #   D2    = 3_invention_loop/iter_1/gen_art/gen_art_dataset_2/full_data_out.json (taxonomic+numeric; for distributed-absorption population anchors Georgia/Jordan)
  #   HG_DIR= 3_invention_loop/iter_5/gen_art/gen_art_dataset_1                  (homograph entities; art_2xQn686KUmV5)
  #   DOSS  = 3_invention_loop/iter_1/gen_art/gen_art_research_1/research_out.json (SAE pins + baseline specs; art_RidEJtBC7gPT)
  # SAE pins (from core.py / dossier, DO NOT change): release google/gemma-scope-2b-pt-res,
  #   layer_12/width_16k/average_l0_82/params.npz, d_model 2304, hook blocks.12.hook_resid_post,
  #   model google/gemma-2-2b (mirror unsloth/gemma-2-2b), SEED 1234, B_BOOT 10000.
  ############################################################################

  # ============================ STEP A. ENV + REUSE (verbatim copy, not cross-dir import) ===========
  # Cross-dir import is unsafe because CORE7/METH7 hardcode WORK=iter_7 and create RESULTS/CACHE/LOGS there.
  #  - `uv init`; install: torch (CUDA cu124: `uv pip install torch --index-strategy unsafe-best-match`,
  #    add `--link-mode=copy` because the venv lives on mfs), transformers, numpy, scipy, scikit-learn,
  #    loguru, requests, huggingface_hub. Mirror iter-7 pyproject.toml.
  #  - Copy CORE7 -> ./core.py and METH7 -> ./method_lib.py VERBATIM. In BOTH, repoint the module-level
  #    WORK constant to THIS workspace so RESULTS/CACHE/LOGS/cache land here (never write into iter_7).
  #    Keep _find_sae_params() (auto-locates the cached SAE npz) and the unsloth fallback loader untouched.
  #  - Set HF_HUB_OFFLINE=1 if the SAE+model are already cached; else allow one download. HF_TOKEN optional
  #    (unsloth mirror is ungated). cache/ holds encodings + is EXCLUDED from upload (.gitignore-style).
  #  - aii-openrouter-llms for the judge; reuse METH7 judge infra (PRIMARY=anthropic/claude-haiku-4.5,
  #    SECOND auto-resolved from gpt-4o-mini / gemini-2.5-flash). Global SPENT cap TARGET=3.0, HARD_CAP=10.0.

  # ============================ STEP B. ADD THE NEW FAIR-GATED OPERATOR (the only genuinely-new edit code) =====
  # In ./core.py add kind=='erase_dir_gated_fair' to make_edit_hook(), _make_clamped_hook(),
  # and thread it through read_resid_under_edit()/forward_pos_logprobs()/behavioral_curve()/generate_under_edit().
  # Extend the hook signature with: gw (d_sub weight tensor [d_model]), gb (d_sub bias float), beta (<=1), gate_thresh.
  # Operator (UNIFIED, identical to iter-8 Artifact-1 spec -> MINOR-4 unification):
  #     dot  = h @ u                                   # u == unit u_sub (the labeled sub-direction; full projection)
  #     gate = (h @ gw + gb) > gate_thresh             # PRECISE d_sub detector (AUC~1.0) decides WHERE to erase
  #     hf   = hf - min(beta,1.0) * dot.unsqueeze(-1) * u.view(1,1,-1) * gate.unsqueeze(-1).to(hf.dtype)
  #     counter['edited'] += int(gate.sum()); counter['total'] += int(gate.numel())
  # RATIONALE vs iter-7 erase_dir_gated: iter-7 gated on |h.u_sub|>tau (a CRUDE magnitude gate calibrated to a
  # 3% GLOBAL footprint) which forced beta~2.97 over-erasure. THIS gate uses the precise supervised d_sub and
  # CAPS beta at 1.0 (beta=1 == full removal of the labeled component at exactly the detected X tokens), so it is
  # the genuinely-FAIR conditional-dense control. gate_thresh default 0.0 (prob 0.5); also record an alt calibration
  # where gate_thresh is set so the gate's X-recall equals the KG absorber's X firing-recall (report both, primary=0.0).

  # ============================ STEP C. BUILD THE CANDIDATE POOL ($0) ================================
  # C1. SPELLING word-absorbers (hierarchy='first_letter_spelling', parent=<letter>):
  #   curated = {L: large,list,line,law,like,level,low,leave,land,life ; O: our,one,only,other,out,over ;
  #              T: that,their,there,time,take,this ; I: in,into,it,is,if ; D: day,down,do,did,does}
  #   UNION the NON-EMPTY words in KG4.metadata.canonical_units.first_letter.{L,O,T,I,D}.sub_by_absorber
  #   (e.g. L: 3069->list, 2416->line, 3353->level, 3858->low, 7544->leave). Keep only words present in D1's
  #   per-letter corpus with >=12 word-initial windows (load via core.load_first_letter(['L','O','T','I','D'])).
  #   The absorber latent is RE-DERIVED in STEP D (do NOT trust sub_by_absorber gaps; large->8463 came from iter-7
  #   re-derivation, not iter-4). Carry 'large'=8463 as a hardcoded positive-control anchor.
  # C2. HOMOGRAPH entities (hierarchies city/month/given_name/brand):
  #   The shipped HG_DIR/full_data_out.json + manifest.json are ABSENT on disk -> REBUILD first (exactly as the
  #   iter-6 router experiment did): copy HG_DIR to ./homograph_data/, run `python pipeline.py --scale full --no-llm`
  #   there ($0, writes full_data_out.json + manifest.json). Read manifest.absorption_readiness per (hierarchy,entity);
  #   keep entities with status 'eligible' (>=150 diagnostic positives) OR diagnostic_positives>=120.
  #   curated must-include (reviewer-named): Apple,Shell,Target,Orange (brand); Grace,Hope,Mark,Will (given_name);
  #   March,June,May (month); Amazon,Bush,Cook (positive-control anchors from iter-7). sub_context=entity in TARGET
  #   sense; siblings=other eligible entities SAME hierarchy in target sense; hard-negatives=homograph_competitor rows.
  # C3. DISTRIBUTED-ABSORPTION population anchors (load from D2 via core.load_taxonomic): Georgia(16009),
  #   Jordan(540) -- known NO_MEANINGFUL_FORGET losers. Include 2-3 so the population scatter has the
  #   low-concentration/absorption-structured quadrant (else the M3''' contrast is unidentified).
  # Each candidate := {token, hierarchy, parent, dataset_handle}.  Expect ~45-70 candidates total.

  # ============================ STEP D. PER-CANDIDATE CONCENTRATION SCREEN ($0, GPU encode, cached) ===
  # load_sae(); ModelBundle(); determine_layer_idx() once (expect idx 13, FVU~0.19, cosine>0.9 gating PASS).
  # Build a NEUTRAL token pool (core.NEUTRAL_TEXT) once for footprint calibration.
  # for cand in pool:
  #   rows_X    = corpus windows where token appears in TARGET sense  (held-out fold for eval; disjoint fit fold for u_sub/d_sub)
  #   rows_SIB  = corpus windows of SIBLING tokens (same hierarchy, target sense)
  #   pairs     = content_pairs (x_on/x_off) for the token if present (spelling+homograph ship these)
  #   lat_csr, resid = mb.encode_rows(rows_X+rows_SIB+pairs)         # cache under cache/enc_<cand>_*.npz
  #   cr, prec_vec, _ = core.content_responsive(A_on, A_off)         # per-latent content-responsiveness + precision
  #   anchor      = highest-recall content-responsive latent on PARENT contexts (hierarchy-level; reuse KG4 anchor when available)
  #   recall_hole = 1 - mean(anchor fires on rows_X)
  #   # K-track precision selection (anchored, recall-hole-guided) -> the 'absorber' the method discovers:
  #   absorber    = argmax over cr latents s.t. firing_Jaccard(l,anchor)<0.1 AND precision_on_X(l)>=0.7 of coverage(l on rows_X)
  #                 (if none qualifies -> absorber=None, candidate flagged structure_absent, still screened for concentration)
  #   # UNCONSTRAINED max-precision selector (M3''' / M5''' baseline -- NO anchor/Jaccard constraint):
  #   max_prec_latent = argmax over cr latents with firing_on_X>=min_fire of precision_on_X(l)
  #   precision   = precision_on_X(absorber or max_prec_latent)
  #   footprint   = mean over NEUTRAL pool tokens of (chosen latent fires)   # forward over NEUTRAL_TEXT, count z[l]>0
  #   concentration_score = precision * (1 - footprint)                      # high precision AND sparse => concentrated
  #   firing_jaccard      = Jaccard(absorber/parent positive-token sets)
  #   absorption_structured = (recall_hole >= 0.6) and (firing_jaccard < 0.1)  # REPORTED, never gates the screen
  #   set_cover_eq_max_precision = (absorber is not None and absorber == max_prec_latent)
  #   record screen_row{token,hierarchy,precision,footprint,concentration_score,recall_hole,firing_jaccard,
  #                     absorber,max_prec_latent,set_cover_eq_max_precision,absorption_structured}
  # rank pool by concentration_score DESC.

  # ============================ STEP E. EDIT SET SELECTION (gradual scaling, breadth-first) ==========
  # edit_set = top-K by concentration_score (K ~= 10-14, concentrated co-firing candidates ARE eligible -- the
  #   reframe predicts they can win) UNION the population anchors {large(8463), Amazon, Bush, Cook} (positive controls,
  #   re-run to confirm the pipeline reproduces iter-7's KG win) UNION {Georgia, Jordan} (distributed-absorption losers).
  # Edit MOST-CONCENTRATED FIRST so breadth of independent wins is maximized before budget/time exhausts.
  # Use aii-long-running-tasks gradual pattern: smoke(2 cands) -> mini(5) -> full. Track SPENT after every judge batch.

  # ============================ STEP F. PER-CANDIDATE EDIT + MATCHED-FORGET COMPARISON ==============
  # for cand in edit_set (ordered):
  #   u_sub, u_meta = method_lib.build_u_sub(resid, X_pos_fit_mask, SIB_pos_fit_mask, probe.d_mu, fb...)
  #   d_sub         = method_lib.fit_sub_probe(resid, X_pos_fit_mask, SIB_pos_fit_mask)   # frozen {w,b,auc}; need auc>~0.9
  #   if u_meta.underpowered (n_pos<MIN_SUB=20) or d_sub is None: mark descriptive_only, emit screen row, CONTINUE
  #   # ---- OPERATORS (sweep each; all share ONE u_sub + ONE d_sub) ----
  #   OPS = {
  #     'KG-ABL'                  : (abl_latent,           l=absorber,          sweep LAM_GRID [0,.5,1,2,3,4]),
  #     'DENSE-SUB-ABL'           : (erase_dir,            u=u_sub,             sweep BETA_GRID [0,.5,1,1.5,2,3,4,6,8])  # LEAD comparator (strongest ungated dense),
  #     'DENSE-SUB-ABL-GATED-FAIR': (erase_dir_gated_fair, u=u_sub,gw=d_sub.w,gb=d_sub.b,gate_thresh=0, sweep beta [0,.25,.5,.75,1.0])  # BOUNDED beta<=1 (establishing control),
  #     'MAX-PREC-ABL'            : (abl_latent,           l=max_prec_latent,   sweep LAM_GRID)  # M3''' set-cover-vs-max-precision ablation
  #   }
  #   # ---- BEHAVIORAL forget curve per op (M4''': match on BEHAVIOR, NOT next-token KL) ----
  #   base_rate = subprobe_positive_rate(d_sub, resid_of(X_held_rows))   # ~1.0
  #   for op,scale: resid_e = read_resid_under_edit(X_held_rows, kind=op,...,scale); sub_drop(op,scale)=base_rate-subprobe_positive_rate(d_sub,resid_e)
  #   completion_drop via method_lib.completion_drop with TEMPLATED probes (M4''' ~20-50/case):
  #       spelling: ['{w} starts with the letter','The first letter of the word {w} is','{w} is spelled starting with',
  #                  'The word {w} begins with the letter', ... ~10 templates] gold=first letter (uppercase)
  #       homograph: target-sense completions where templatable (brand: '{e} announced a new'->product;
  #                  month: 'The month after {prev} is'->{e}; given_name: weak->rely on sub_drop); else completion=None.
  #   # ---- MATCHED MEANINGFUL-FORGET POINT (behavioral) ----
  #   FORGET_FLOOR=0.10 (meaningful); matched_target = max(FORGET_FLOOR, 0.8*min_op(max achievable sub_drop))
  #   for op: s_op = smallest scale whose interpolated sub_drop reaches matched_target; if op cannot reach it within its
  #           sweep (esp FAIR-GATED at beta=1.0) -> op_saturated=True, s_op=max-forget scale, note 'cannot match'.
  #   meaningful_forget = (KG sub_drop at s_KG >= 0.10) AND (completion drop CI>0 OR KG sub_drop>=0.10)  # success-criteria OR
  #   # ---- JUDGED JOINT at the matched point (2 judges) ----
  #   prompts: FORGET (~24, prefixes from X-held rows), RETAIN (~20, sibling rows), UNRELATED (~20, NEUTRAL_TEXT)
  #   for op: conts = generate_under_edit(prompts, kind=op,...,scale=s_op, clamp_norm=True)
  #           judge each (claude-haiku + 2nd) -> {fluency0-2, content_pres0-2}; joint=HM(fluency,content_pres)
  #           op_joint = aggregate(forget_quality on FORGET, preservation on RETAIN+UNRELATED)   # iter-7 convention
  #   Delta_joint(KG vs DENSE-SUB-ABL)     = paired_bootstrap_diff(joint_KG, joint_ungated)  per judge, B=10000
  #   Delta_joint(KG vs DENSE-SUB-ABL-GATED-FAIR) = paired_bootstrap_diff(...)               per judge, B=10000
  #   KG_beats_ungated  = both judges' CI excl 0 favoring KG
  #   KG_beats_fair     = both judges' CI excl 0 favoring KG (if fair op_saturated below match: KG auto-wins on forget,
  #                       still report the joint delta at the common achievable forget + the saturation note)
  #   concentrated_win  = meaningful_forget AND KG_beats_fair
  #   emit per-(token,role,prompt) prediction rows: predict_kg_abl/predict_dense_sub_abl/predict_dense_sub_gated_fair/
  #       predict_max_precision/predict_noop = the continuation STRINGS (all rows MUST carry these as strings -> validator),
  #       + per-op joint, sub_drop, footprint, s_op utilities.
  #   STOP issuing NEW judge calls once SPENT>=TARGET; remaining edit_set candidates fall back to $0 screen-only rows
  #   (concentration + structure + set_cover flag computed, edit/Delta marked budget_skipped).

  # ============================ STEP G. VERDICT (base count, M2''') ================================
  # known_wins = {'large','Amazon'} (iter-7); re-confirmed here as positive controls (assert KG_beats_fair reproduces;
  #   if a control FAILS to reproduce, that is a flagged honest negative about the new fair operator, not a silent pass).
  # new_wins = {token : concentrated_win True and token not in known_wins}
  # total_independent_concentrated_wins = | dedupe_by_token(known_wins UNION new_wins) |
  # verdict = 'BASE_REACHES_4_PLUS' if total>=4 else 'BASE_STAYS_THIN_RETARGET'
  #   (the latter triggers the paper retarget to 'localization+editing of homograph-polysemy absorption').

  # ============================ STEP H. POPULATION PREDICTOR ANALYSIS (decisive M3''' evidence) =====
  # over EDITED candidates that produced a Delta_joint (include the Georgia/Jordan distributed anchors + any co-firing):
  #   features: C=concentration_score (continuous), S=absorption_structured (binary 0/1)
  #   outcomes: Ymag=Delta_joint(KG vs fair) (continuous win-magnitude), Ywin=concentrated_win (binary 0/1)
  #   spearman(C,Ymag)+bootstrap CI ; point_biserial(C,Ywin)+CI
  #   point_biserial(S,Ymag)+CI     ; phi/point_biserial(S,Ywin)+CI
  #   predictor_verdict = 'CONCENTRATION_PREDICTS' if |corr(C,.)| CI is higher and excludes 0 while |corr(S,.)| does not,
  #                       'ABSORPTION_PREDICTS' if reverse, else 'TIE/UNDERPOWERED' (report n and CIs honestly).
  #   set_cover_inertness_rate = mean(set_cover_eq_max_precision over candidates with an absorber)  # M5'''
  #   (Report the expected story per the reframe: a concentrated CO-FIRING latent CAN win; Georgia/Jordan absorb but
  #    have LOW concentration and lose. Do NOT assert it -- let the correlation+CI decide; underpowered is reportable.)

  # ============================ STEP I. OUTPUT (exp_gen_sol_out schema) =============================
  # method_out.json:
  #   metadata: {method_name, description, sae{release,sae_params,width,d_model,hook}, model, seed, B_boot,
  #     gating_check{cosine,L0,fvu_by_idx,layer_idx}, forget_grids, judge{models,target_usd,hard_cap,spent_usd,calls},
  #     fair_gate_spec{operator='erase_dir_gated_fair', beta_cap=1.0, gate_thresh_primary=0.0, gate_alt='X-recall-matched'},
  #     concentration_screen_table:[per-candidate dict],
  #     base_count{known_wins, new_wins, total_independent_concentrated_wins, verdict},
  #     population_predictor{spearman_conc_mag_ci, pb_conc_win_ci, pb_absorp_mag_ci, pb_absorp_win_ci, predictor_verdict, n},
  #     set_cover_inertness_rate,
  #     honest_negatives:[ verbatim list -- see fallback ] }
  #   datasets:
  #     {dataset:'concentration_screen', examples:[ one per candidate; input=human-readable desc, output=tag
  #        ('concentrated_win'/'meaningful_no_win'/'no_meaningful_forget'/'structure_absent'/'budget_skipped'),
  #        metadata_*: token,hierarchy,precision,footprint,concentration_score,recall_hole,firing_jaccard,absorber,
  #        max_prec_latent,set_cover_eq_max_precision,absorption_structured,meaningful_forget,
  #        delta_joint_vs_ungated_{primary,second}_{diff,ci_lo,ci_hi,excl0}, delta_joint_vs_fair_{...},
  #        kg_beats_ungated,kg_beats_fair,fair_saturated, AND predict_* STRING fields (set to op tag/'NA') ]},
  #     {dataset:'edit_predictions', examples:[ per (token,role,prompt): input=prompt, output=role,
  #        predict_kg_abl, predict_dense_sub_abl, predict_dense_sub_gated_fair, predict_max_precision, predict_noop
  #        (continuation STRINGS), metadata_*: token,role,sub_probe_drop_kg, joint_kg, joint_ungated, joint_fair, s_op_* ]}
  #   EVERY example in EVERY dataset MUST carry the five predict_* keys as STRINGS (iter-5 GOTCHA: missing/
  #   non-string predict_* => validator FAIL). Use make_variants.py (copied from iter-7) to emit
  #   full/mini/preview_method_out.json each <100MB; validate all three with aii-json against exp_gen_sol_out.
  #   Exclude cache/ and .venv/ from the uploaded artifact.

  # ============================ COST / TIME BUDGET ==================================================
  # $0 screen over the full pool first. Editing ~12-16 candidates x 2 judges x ~64 continuations ~= $1.5-2.5 (iter-7
  # was $0.80 for 5 cases). Hard-stop judge calls at SPENT>=3.0. GPU wall-clock budget ~5h of the 6h: encoding is the
  # bulk (cached); generation+forward sweeps dominate per edited candidate (~10-15 min each). PID-based process mgmt only.
fallback_plan: |-
  DATA / REBUILD failures: (1) If `pipeline.py --scale full --no-llm` for the homograph dataset errors (geonamescache/protobuf/libgomp quirks seen in prior iters), fall back to `--scale smoke` for structure then hand-load the entities directly from HG_DIR/data.py's entity gazetteers + D1-style corpus windows; if it still fails, DROP the homograph hierarchies and run the base-widener on SPELLING words alone (L/O/T/I/D give 20-40 candidates -- enough for the population test and >=4-win target on concentrated spelling absorbers). (2) If a candidate has too few corpus positives for a trustworthy u_sub/d_sub (n_pos<MIN_SUB=20, AUC<0.9), mark it descriptive_only and keep it in the $0 screen (still contributes concentration + structure + set_cover flag) but exclude from the edit/Delta analysis -- report the excluded count.
  OPERATOR failures: (3) If the bounded-beta (<=1) fair-gated dense CANNOT reach the matched meaningful-forget for many candidates, that is a SUBSTANTIVE result, not a bug: KG wins on forget by construction -- report it as 'fair gated dense saturates below meaningful forget at beta<=1' and compare joint collateral at the common achievable forget. Also run the alt gate_thresh (X-recall-matched) to show the conclusion is calibration-robust. (4) If generation NaNs in bf16, use the clamp_norm=True path (_make_clamped_hook, already supports the new operator).
  BUDGET / TIME truncation (pre-registered drop order, breadth-first): keep the $0 full-pool concentration screen + set_cover_inertness ALWAYS (they alone answer M3''' structurally and M5'''); then the positive-control re-runs (large, Amazon); then top-concentration new candidates until SPENT>=3.0 or time runs low; DROP (first-dropped-first) the MAX-PREC-ABL judged edit (keep its $0 set_cover_eq flag), then the second judge on lowest-concentration candidates (keep primary), then the distributed-absorption Georgia/Jordan re-edit (cite iter-7 numbers as population anchors instead). NEVER drop: the concentration screen, >=the two positive-control wins, the population correlation over whatever edited points exist.
  VERDICT robustness: (5) If <4 independent concentrated wins land, emit BASE_STAYS_THIN_RETARGET honestly (this is an expected, publishable outcome that triggers the paper's localization-first retarget) -- do NOT inflate by re-counting the confirmatory Amazon or the excluded co-firing insult as load-bearing. (6) If the population correlation is underpowered (too few edited points / wide CIs), report 'TIE/UNDERPOWERED' with n and CIs rather than asserting CONCENTRATION_PREDICTS.
  HONEST NEGATIVES to record verbatim in metadata.honest_negatives: fair-gated-dense matches KG (=> value is label-free where-to-gate discovery, gating is prior art CAST/GSS/GUARD-IT/SADI); set-cover absorber == max-precision latent for most candidates (=> method is precise-latent discovery, set-cover inert); base stays thin (n~2-3) => retarget; concentration does NOT out-predict absorption (=> reframe unsupported, report as-is); distributed-absorption candidates show no meaningful forget (carries iter-7 Georgia/Jordan); homograph rebuild required (data not shipped); positive control fails to reproduce under the new fair operator.
testing_plan: |-
  1) SMOKE (logic, ~2-5 min, $0): run with a 2-candidate pool {large (spelling, known win), Georgia (taxonomic, known no-forget loser)} and tiny caps (cap=20 rows, 3 FORGET/2 RETAIN prompts, judges DISABLED by unsetting OPENROUTER_API_KEY). CONFIRM: SAE loads (d_sae=16384, d_model=2304), determine_layer_idx selects 13 with cosine>0.9 (gating PASS), encode_rows runs, the new erase_dir_gated_fair hook executes without shape/NaN errors and its token-footprint counter is >0 on X tokens and ~0 on neutral tokens, content_responsive returns cr latents, the concentration screen emits rows with precision/footprint/concentration_score in [0,1], and large's re-derived absorber == 8463 (sanity vs iter-7). Output a valid (judge-less) method_out.json skeleton.
  2) OPERATOR UNIT CHECK ($0): on 'large', verify (a) KG-ABL sub-probe positive-rate drops monotonically with lambda; (b) DENSE-SUB-ABL-GATED-FAIR at beta=1.0 produces a LARGE sub_drop ON X tokens but tiny token_footprint on UNRELATED/neutral text (precise gate), and at beta=1.0 the on-X erasure is full-projection (sub_drop>=ungated at matched gate) -- confirming it is a strong, fair, non-over-erasing control; (c) MAX-PREC-ABL on 'large' selects a latent and set_cover_eq_max_precision resolves to a definite bool. Print the matched-forget scales s_op and confirm they are finite.
  3) MINI (~15-25 min, <$0.5): 5 candidates {large, Amazon (rebuild homograph first), one new concentrated spelling word, one new homograph entity, Jordan}. ENABLE both judges on a reduced prompt set (~10/role). CONFIRMATION SIGNALS before scaling: large reproduces KG_beats_fair (positive control passes); Jordan shows NO meaningful forget (sub_drop<0.10); Delta_joint CIs compute under both judges; SPENT tracked and well under TARGET; the population-predictor function runs on >=4 points without error. If the large positive control does NOT reproduce a KG win under the new fair operator, STOP and debug the operator/gate calibration before spending more budget.
  4) FULL: only after mini confirms the positive control + judge pipeline + cost tracking. Screen the full pool ($0), then edit most-concentrated-first until SPENT approaches 3.0 or ~5h elapsed. After completion: validate full/mini/preview method_out.json with aii-json against exp_gen_sol_out (every example has the 5 predict_* STRING keys), confirm each variant <100MB, confirm cache/ excluded. Sanity-check the verdict arithmetic (total_independent_concentrated_wins dedup by token) and that honest_negatives reflects the actual outcome (no inflation of confirmatory/co-firing cases into the load-bearing count).
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
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_1/gen_art/gen_art_research_1
out_dependency_files:
  file_list:
  - research_out.json

--- Dependency 2 ---
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
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
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

--- Dependency 3 ---
id: art_2xQn686KUmV5
type: dataset
title: >-
  Homograph/Polysemy Entity Absorption Testbed (cities, months, given-names, brands)
summary: |-
  A pure CPU/text artifact: a FOUR-hierarchy homograph/polysemy entity absorption testbed, built as a strict structural drop-in extension of the iter-1 non-spelling absorption testbed (art_t2uUbjSwpd3t). It is explicitly a NEXT-ITERATION BUILDING BLOCK (not consumed by this iteration's parallel experiments): it supplies breadth of suppressed-parent candidates so the persistent single-slice taxonomic critique (Georgia-only) can be answered with many homograph cases.

  Four `dataset`s, one per is-a hierarchy, whose surface tokens carry a strong competing NON-target sense (the competition that produces feature absorption / a suppressed-parent recall hole):
    1. city_homograph_absorption  (parent = is-a-city): Phoenix, Mobile, Reading, Bath, Nice, Buffalo, Paris, Mercury, Jackson, Columbus, Cleveland, Florence, ... (23 entities).
    2. month_name_absorption (parent = is-a-month): all 12 calendar months; homograph-strong May/March/August/April/June.
    3. given_name_absorption (parent = is-a-given-name): Grace, Hope, Mark, Will, Rose, Frank, Faith, Joy, Dawn, Jack, ... (34 entities).
    4. brand_homograph_absorption (parent = is-a-brand): Apple, Amazon, Shell, Target, Orange, Gap, Tide, Visa, Subway, Java, ... (24 entities).

  Each hierarchy ships the SAME three coordinated components as dataset_2: (A) content-flip minimal pairs (parent present vs absent, surface-matched), (B) surface-flip pairs (concept fixed, surface varied; both positive, for the unit-level surface-invariance check), and (C) a frozen monology/pile-uncopyrighted diagnostic corpus (pinned rev 3be90335b66f24456a5d6659d9c8d208c0357119) of real windows labelled by frozen, model-independent sub-context. The NEW homograph_competitor negative family (the same surface token in its non-target sense, e.g. lowercase 'apple'/'will'/'march', 'Joaquin Phoenix', 'Christopher Columbus') is the matched hard control that makes a suppressed parent visible.

  On-disk format is the AII exp_sel_data_out schema: {metadata, datasets:[{dataset, examples:[{input, output, metadata_*}]}]} with FLAT metadata_* keys (no nested objects). New/extended fields vs iter-1: metadata_hierarchy (city|month|given_name|brand), metadata_entity (canonical surface), metadata_target_sense (city|month|given_name|brand|competitor|null), metadata_competitor_sense (gloss of competing sense), metadata_homograph_strength (wordfreq Zipf of the lowercase competitor), and metadata_neg_family expanded to include homograph_competitor / other_place / other_time / other_person_ref / other_company_ref / easy. Fold semantics are unchanged (pairs 70/30 train/test by pair_id stratified by sub_context; corpus 50/50 train/diagnostic stratified), gemma-2-2b offset-mapping token anchoring is reused (metadata_target_token_indices), and the downstream K-track + form-free absorption diagnostic pipeline runs unchanged except for the new enum values.

  Labels are assigned PURELY from surface form / regex / gazetteer (geonamescache for cities) / disambiguating local context — never from a model — so the degenerate-construction guard holds and absorption presence/absence stays a future-iteration EMPIRICAL finding: the corpus equally supports the 'absorption is spelling-specific' null and a positive homograph-absorption finding. Corpus target-sense labels use high-precision case-aware cues; an LLM-judged stratified sample MEASURES per-hierarchy target-sense precision (reported in manifest.json, target >=0.9; it does not relabel the corpus). manifest.json carries per-(hierarchy,entity) absorption_readiness with diagnostic_positives counts and status (eligible if >=150 diagnostic-fold positives, else descriptive_only), eligible_entities_per_hierarchy, per-component counts, source/pile-set counts, llm_pair_pass_rate, llm_corpus_sense_precision, llm_cost_breakdown, city geonames provenance, and cross-hierarchy collision notes (Dawn, Chase, Jordan, Mercury, Paris). Deliverables: data.py, build_dataset.py, pipeline.py, schema.json, manifest.json, and full/mini/preview_data_out.json (validated against exp_sel_data_out, each <100MB). Reproducible via fixed seed 20240617 and pinned pile revision; total LLM spend well under $1.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_5/gen_art/gen_art_dataset_1
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

### [6] HUMAN-USER prompt · 2026-06-18 19:59:22 UTC

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

### [7] SKILL-INPUT — aii-json · 2026-06-18 20:18:27 UTC

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

### [8] SYSTEM-USER prompt · 2026-06-18 20:22:37 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_2`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_2/`:
GOOD: `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_2/file.py`, `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_2/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_experiment_2_idx2
type: experiment
title: >-
  Base-Widener + Concentration-vs-Absorption Population Test (iter-8 M2''' + M3''')
summary: >-
  Screen a WIDER vocabulary of candidate tokens (first-letter spelling word-absorbers L/O/T/I/D + homograph entities/given-names/brands/months)
  for lexical CONCENTRATION (per-sub-context firing precision x sparse footprint), independent of absorption structure, then
  run the IDENTICAL unified fair-gated edit (the new DENSE-SUB-ABL-GATED-FAIR = u_sub gated by the precise d_sub detector
  with bounded beta<=1) on the most-concentrated candidates. Report (1) how many candidates clear the fair-control bar at
  MEANINGFUL forget => additional independent concentrated wins beyond large/Amazon (verdict BASE_REACHES_4_PLUS vs BASE_STAYS_THIN_RETARGET);
  (2) whether a candidate's continuous CONCENTRATION score predicts its edit-win/meaningful-forget outcome better than its
  binary ABSORPTION-regime label (the decisive M3''' population evidence); (3) per candidate, whether the precision-selected
  absorber EQUALS the unconstrained max-precision latent (set-cover inertness, M5'''). Reuses iter-7 core.py/method.py VERBATIM
  for the SAE pipeline, edit operators, judges, u_sub/d_sub, and meaningful-forget proof; adds ONE new operator, a $0 concentration
  screen, a budget-bounded edit loop, and the population correlation. Compute: GPU (gemma-2-2b + Gemma-Scope L12/16k). LLM
  judge target <$3, hard cap $10.
runpod_compute_profile: gpu
implementation_pseudocode: |
  ############################################################################
  # WORKSPACE: 3_invention_loop/iter_8/gen_art/gen_art_experiment_2  (executor's CWD)
  # READ-ONLY INPUTS (existing run-tree artifacts, accessed by absolute path):
  #   CORE7 = 3_invention_loop/iter_7/gen_art/gen_art_experiment_1/core.py     (SAE+edit machinery)
  #   METH7 = 3_invention_loop/iter_7/gen_art/gen_art_experiment_1/method.py   (u_sub/d_sub/judge/forget proof)
  #   KG4   = 3_invention_loop/iter_4/gen_art/gen_art_experiment_1/method_out.json (named absorbers)
  #   D1    = 3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json (first-letter spelling; art_dpYpjSn2Xvg3)
  #   D2    = 3_invention_loop/iter_1/gen_art/gen_art_dataset_2/full_data_out.json (taxonomic+numeric; for distributed-absorption population anchors Georgia/Jordan)
  #   HG_DIR= 3_invention_loop/iter_5/gen_art/gen_art_dataset_1                  (homograph entities; art_2xQn686KUmV5)
  #   DOSS  = 3_invention_loop/iter_1/gen_art/gen_art_research_1/research_out.json (SAE pins + baseline specs; art_RidEJtBC7gPT)
  # SAE pins (from core.py / dossier, DO NOT change): release google/gemma-scope-2b-pt-res,
  #   layer_12/width_16k/average_l0_82/params.npz, d_model 2304, hook blocks.12.hook_resid_post,
  #   model google/gemma-2-2b (mirror unsloth/gemma-2-2b), SEED 1234, B_BOOT 10000.
  ############################################################################

  # ============================ STEP A. ENV + REUSE (verbatim copy, not cross-dir import) ===========
  # Cross-dir import is unsafe because CORE7/METH7 hardcode WORK=iter_7 and create RESULTS/CACHE/LOGS there.
  #  - `uv init`; install: torch (CUDA cu124: `uv pip install torch --index-strategy unsafe-best-match`,
  #    add `--link-mode=copy` because the venv lives on mfs), transformers, numpy, scipy, scikit-learn,
  #    loguru, requests, huggingface_hub. Mirror iter-7 pyproject.toml.
  #  - Copy CORE7 -> ./core.py and METH7 -> ./method_lib.py VERBATIM. In BOTH, repoint the module-level
  #    WORK constant to THIS workspace so RESULTS/CACHE/LOGS/cache land here (never write into iter_7).
  #    Keep _find_sae_params() (auto-locates the cached SAE npz) and the unsloth fallback loader untouched.
  #  - Set HF_HUB_OFFLINE=1 if the SAE+model are already cached; else allow one download. HF_TOKEN optional
  #    (unsloth mirror is ungated). cache/ holds encodings + is EXCLUDED from upload (.gitignore-style).
  #  - aii-openrouter-llms for the judge; reuse METH7 judge infra (PRIMARY=anthropic/claude-haiku-4.5,
  #    SECOND auto-resolved from gpt-4o-mini / gemini-2.5-flash). Global SPENT cap TARGET=3.0, HARD_CAP=10.0.

  # ============================ STEP B. ADD THE NEW FAIR-GATED OPERATOR (the only genuinely-new edit code) =====
  # In ./core.py add kind=='erase_dir_gated_fair' to make_edit_hook(), _make_clamped_hook(),
  # and thread it through read_resid_under_edit()/forward_pos_logprobs()/behavioral_curve()/generate_under_edit().
  # Extend the hook signature with: gw (d_sub weight tensor [d_model]), gb (d_sub bias float), beta (<=1), gate_thresh.
  # Operator (UNIFIED, identical to iter-8 Artifact-1 spec -> MINOR-4 unification):
  #     dot  = h @ u                                   # u == unit u_sub (the labeled sub-direction; full projection)
  #     gate = (h @ gw + gb) > gate_thresh             # PRECISE d_sub detector (AUC~1.0) decides WHERE to erase
  #     hf   = hf - min(beta,1.0) * dot.unsqueeze(-1) * u.view(1,1,-1) * gate.unsqueeze(-1).to(hf.dtype)
  #     counter['edited'] += int(gate.sum()); counter['total'] += int(gate.numel())
  # RATIONALE vs iter-7 erase_dir_gated: iter-7 gated on |h.u_sub|>tau (a CRUDE magnitude gate calibrated to a
  # 3% GLOBAL footprint) which forced beta~2.97 over-erasure. THIS gate uses the precise supervised d_sub and
  # CAPS beta at 1.0 (beta=1 == full removal of the labeled component at exactly the detected X tokens), so it is
  # the genuinely-FAIR conditional-dense control. gate_thresh default 0.0 (prob 0.5); also record an alt calibration
  # where gate_thresh is set so the gate's X-recall equals the KG absorber's X firing-recall (report both, primary=0.0).

  # ============================ STEP C. BUILD THE CANDIDATE POOL ($0) ================================
  # C1. SPELLING word-absorbers (hierarchy='first_letter_spelling', parent=<letter>):
  #   curated = {L: large,list,line,law,like,level,low,leave,land,life ; O: our,one,only,other,out,over ;
  #              T: that,their,there,time,take,this ; I: in,into,it,is,if ; D: day,down,do,did,does}
  #   UNION the NON-EMPTY words in KG4.metadata.canonical_units.first_letter.{L,O,T,I,D}.sub_by_absorber
  #   (e.g. L: 3069->list, 2416->line, 3353->level, 3858->low, 7544->leave). Keep only words present in D1's
  #   per-letter corpus with >=12 word-initial windows (load via core.load_first_letter(['L','O','T','I','D'])).
  #   The absorber latent is RE-DERIVED in STEP D (do NOT trust sub_by_absorber gaps; large->8463 came from iter-7
  #   re-derivation, not iter-4). Carry 'large'=8463 as a hardcoded positive-control anchor.
  # C2. HOMOGRAPH entities (hierarchies city/month/given_name/brand):
  #   The shipped HG_DIR/full_data_out.json + manifest.json are ABSENT on disk -> REBUILD first (exactly as the
  #   iter-6 router experiment did): copy HG_DIR to ./homograph_data/, run `python pipeline.py --scale full --no-llm`
  #   there ($0, writes full_data_out.json + manifest.json). Read manifest.absorption_readiness per (hierarchy,entity);
  #   keep entities with status 'eligible' (>=150 diagnostic positives) OR diagnostic_positives>=120.
  #   curated must-include (reviewer-named): Apple,Shell,Target,Orange (brand); Grace,Hope,Mark,Will (given_name);
  #   March,June,May (month); Amazon,Bush,Cook (positive-control anchors from iter-7). sub_context=entity in TARGET
  #   sense; siblings=other eligible entities SAME hierarchy in target sense; hard-negatives=homograph_competitor rows.
  # C3. DISTRIBUTED-ABSORPTION population anchors (load from D2 via core.load_taxonomic): Georgia(16009),
  #   Jordan(540) -- known NO_MEANINGFUL_FORGET losers. Include 2-3 so the population scatter has the
  #   low-concentration/absorption-structured quadrant (else the M3''' contrast is unidentified).
  # Each candidate := {token, hierarchy, parent, dataset_handle}.  Expect ~45-70 candidates total.

  # ============================ STEP D. PER-CANDIDATE CONCENTRATION SCREEN ($0, GPU encode, cached) ===
  # load_sae(); ModelBundle(); determine_layer_idx() once (expect idx 13, FVU~0.19, cosine>0.9 gating PASS).
  # Build a NEUTRAL token pool (core.NEUTRAL_TEXT) once for footprint calibration.
  # for cand in pool:
  #   rows_X    = corpus windows where token appears in TARGET sense  (held-out fold for eval; disjoint fit fold for u_sub/d_sub)
  #   rows_SIB  = corpus windows of SIBLING tokens (same hierarchy, target sense)
  #   pairs     = content_pairs (x_on/x_off) for the token if present (spelling+homograph ship these)
  #   lat_csr, resid = mb.encode_rows(rows_X+rows_SIB+pairs)         # cache under cache/enc_<cand>_*.npz
  #   cr, prec_vec, _ = core.content_responsive(A_on, A_off)         # per-latent content-responsiveness + precision
  #   anchor      = highest-recall content-responsive latent on PARENT contexts (hierarchy-level; reuse KG4 anchor when available)
  #   recall_hole = 1 - mean(anchor fires on rows_X)
  #   # K-track precision selection (anchored, recall-hole-guided) -> the 'absorber' the method discovers:
  #   absorber    = argmax over cr latents s.t. firing_Jaccard(l,anchor)<0.1 AND precision_on_X(l)>=0.7 of coverage(l on rows_X)
  #                 (if none qualifies -> absorber=None, candidate flagged structure_absent, still screened for concentration)
  #   # UNCONSTRAINED max-precision selector (M3''' / M5''' baseline -- NO anchor/Jaccard constraint):
  #   max_prec_latent = argmax over cr latents with firing_on_X>=min_fire of precision_on_X(l)
  #   precision   = precision_on_X(absorber or max_prec_latent)
  #   footprint   = mean over NEUTRAL pool tokens of (chosen latent fires)   # forward over NEUTRAL_TEXT, count z[l]>0
  #   concentration_score = precision * (1 - footprint)                      # high precision AND sparse => concentrated
  #   firing_jaccard      = Jaccard(absorber/parent positive-token sets)
  #   absorption_structured = (recall_hole >= 0.6) and (firing_jaccard < 0.1)  # REPORTED, never gates the screen
  #   set_cover_eq_max_precision = (absorber is not None and absorber == max_prec_latent)
  #   record screen_row{token,hierarchy,precision,footprint,concentration_score,recall_hole,firing_jaccard,
  #                     absorber,max_prec_latent,set_cover_eq_max_precision,absorption_structured}
  # rank pool by concentration_score DESC.

  # ============================ STEP E. EDIT SET SELECTION (gradual scaling, breadth-first) ==========
  # edit_set = top-K by concentration_score (K ~= 10-14, concentrated co-firing candidates ARE eligible -- the
  #   reframe predicts they can win) UNION the population anchors {large(8463), Amazon, Bush, Cook} (positive controls,
  #   re-run to confirm the pipeline reproduces iter-7's KG win) UNION {Georgia, Jordan} (distributed-absorption losers).
  # Edit MOST-CONCENTRATED FIRST so breadth of independent wins is maximized before budget/time exhausts.
  # Use aii-long-running-tasks gradual pattern: smoke(2 cands) -> mini(5) -> full. Track SPENT after every judge batch.

  # ============================ STEP F. PER-CANDIDATE EDIT + MATCHED-FORGET COMPARISON ==============
  # for cand in edit_set (ordered):
  #   u_sub, u_meta = method_lib.build_u_sub(resid, X_pos_fit_mask, SIB_pos_fit_mask, probe.d_mu, fb...)
  #   d_sub         = method_lib.fit_sub_probe(resid, X_pos_fit_mask, SIB_pos_fit_mask)   # frozen {w,b,auc}; need auc>~0.9
  #   if u_meta.underpowered (n_pos<MIN_SUB=20) or d_sub is None: mark descriptive_only, emit screen row, CONTINUE
  #   # ---- OPERATORS (sweep each; all share ONE u_sub + ONE d_sub) ----
  #   OPS = {
  #     'KG-ABL'                  : (abl_latent,           l=absorber,          sweep LAM_GRID [0,.5,1,2,3,4]),
  #     'DENSE-SUB-ABL'           : (erase_dir,            u=u_sub,             sweep BETA_GRID [0,.5,1,1.5,2,3,4,6,8])  # LEAD comparator (strongest ungated dense),
  #     'DENSE-SUB-ABL-GATED-FAIR': (erase_dir_gated_fair, u=u_sub,gw=d_sub.w,gb=d_sub.b,gate_thresh=0, sweep beta [0,.25,.5,.75,1.0])  # BOUNDED beta<=1 (establishing control),
  #     'MAX-PREC-ABL'            : (abl_latent,           l=max_prec_latent,   sweep LAM_GRID)  # M3''' set-cover-vs-max-precision ablation
  #   }
  #   # ---- BEHAVIORAL forget curve per op (M4''': match on BEHAVIOR, NOT next-token KL) ----
  #   base_rate = subprobe_positive_rate(d_sub, resid_of(X_held_rows))   # ~1.0
  #   for op,scale: resid_e = read_resid_under_edit(X_held_rows, kind=op,...,scale); sub_drop(op,scale)=base_rate-subprobe_positive_rate(d_sub,resid_e)
  #   completion_drop via method_lib.completion_drop with TEMPLATED probes (M4''' ~20-50/case):
  #       spelling: ['{w} starts with the letter','The first letter of the word {w} is','{w} is spelled starting with',
  #                  'The word {w} begins with the letter', ... ~10 templates] gold=first letter (uppercase)
  #       homograph: target-sense completions where templatable (brand: '{e} announced a new'->product;
  #                  month: 'The month after {prev} is'->{e}; given_name: weak->rely on sub_drop); else completion=None.
  #   # ---- MATCHED MEANINGFUL-FORGET POINT (behavioral) ----
  #   FORGET_FLOOR=0.10 (meaningful); matched_target = max(FORGET_FLOOR, 0.8*min_op(max achievable sub_drop))
  #   for op: s_op = smallest scale whose interpolated sub_drop reaches matched_target; if op cannot reach it within its
  #           sweep (esp FAIR-GATED at beta=1.0) -> op_saturated=True, s_op=max-forget scale, note 'cannot match'.
  #   meaningful_forget = (KG sub_drop at s_KG >= 0.10) AND (completion drop CI>0 OR KG sub_drop>=0.10)  # success-criteria OR
  #   # ---- JUDGED JOINT at the matched point (2 judges) ----
  #   prompts: FORGET (~24, prefixes from X-held rows), RETAIN (~20, sibling rows), UNRELATED (~20, NEUTRAL_TEXT)
  #   for op: conts = generate_under_edit(prompts, kind=op,...,scale=s_op, clamp_norm=True)
  #           judge each (claude-haiku + 2nd) -> {fluency0-2, content_pres0-2}; joint=HM(fluency,content_pres)
  #           op_joint = aggregate(forget_quality on FORGET, preservation on RETAIN+UNRELATED)   # iter-7 convention
  #   Delta_joint(KG vs DENSE-SUB-ABL)     = paired_bootstrap_diff(joint_KG, joint_ungated)  per judge, B=10000
  #   Delta_joint(KG vs DENSE-SUB-ABL-GATED-FAIR) = paired_bootstrap_diff(...)               per judge, B=10000
  #   KG_beats_ungated  = both judges' CI excl 0 favoring KG
  #   KG_beats_fair     = both judges' CI excl 0 favoring KG (if fair op_saturated below match: KG auto-wins on forget,
  #                       still report the joint delta at the common achievable forget + the saturation note)
  #   concentrated_win  = meaningful_forget AND KG_beats_fair
  #   emit per-(token,role,prompt) prediction rows: predict_kg_abl/predict_dense_sub_abl/predict_dense_sub_gated_fair/
  #       predict_max_precision/predict_noop = the continuation STRINGS (all rows MUST carry these as strings -> validator),
  #       + per-op joint, sub_drop, footprint, s_op utilities.
  #   STOP issuing NEW judge calls once SPENT>=TARGET; remaining edit_set candidates fall back to $0 screen-only rows
  #   (concentration + structure + set_cover flag computed, edit/Delta marked budget_skipped).

  # ============================ STEP G. VERDICT (base count, M2''') ================================
  # known_wins = {'large','Amazon'} (iter-7); re-confirmed here as positive controls (assert KG_beats_fair reproduces;
  #   if a control FAILS to reproduce, that is a flagged honest negative about the new fair operator, not a silent pass).
  # new_wins = {token : concentrated_win True and token not in known_wins}
  # total_independent_concentrated_wins = | dedupe_by_token(known_wins UNION new_wins) |
  # verdict = 'BASE_REACHES_4_PLUS' if total>=4 else 'BASE_STAYS_THIN_RETARGET'
  #   (the latter triggers the paper retarget to 'localization+editing of homograph-polysemy absorption').

  # ============================ STEP H. POPULATION PREDICTOR ANALYSIS (decisive M3''' evidence) =====
  # over EDITED candidates that produced a Delta_joint (include the Georgia/Jordan distributed anchors + any co-firing):
  #   features: C=concentration_score (continuous), S=absorption_structured (binary 0/1)
  #   outcomes: Ymag=Delta_joint(KG vs fair) (continuous win-magnitude), Ywin=concentrated_win (binary 0/1)
  #   spearman(C,Ymag)+bootstrap CI ; point_biserial(C,Ywin)+CI
  #   point_biserial(S,Ymag)+CI     ; phi/point_biserial(S,Ywin)+CI
  #   predictor_verdict = 'CONCENTRATION_PREDICTS' if |corr(C,.)| CI is higher and excludes 0 while |corr(S,.)| does not,
  #                       'ABSORPTION_PREDICTS' if reverse, else 'TIE/UNDERPOWERED' (report n and CIs honestly).
  #   set_cover_inertness_rate = mean(set_cover_eq_max_precision over candidates with an absorber)  # M5'''
  #   (Report the expected story per the reframe: a concentrated CO-FIRING latent CAN win; Georgia/Jordan absorb but
  #    have LOW concentration and lose. Do NOT assert it -- let the correlation+CI decide; underpowered is reportable.)

  # ============================ STEP I. OUTPUT (exp_gen_sol_out schema) =============================
  # method_out.json:
  #   metadata: {method_name, description, sae{release,sae_params,width,d_model,hook}, model, seed, B_boot,
  #     gating_check{cosine,L0,fvu_by_idx,layer_idx}, forget_grids, judge{models,target_usd,hard_cap,spent_usd,calls},
  #     fair_gate_spec{operator='erase_dir_gated_fair', beta_cap=1.0, gate_thresh_primary=0.0, gate_alt='X-recall-matched'},
  #     concentration_screen_table:[per-candidate dict],
  #     base_count{known_wins, new_wins, total_independent_concentrated_wins, verdict},
  #     population_predictor{spearman_conc_mag_ci, pb_conc_win_ci, pb_absorp_mag_ci, pb_absorp_win_ci, predictor_verdict, n},
  #     set_cover_inertness_rate,
  #     honest_negatives:[ verbatim list -- see fallback ] }
  #   datasets:
  #     {dataset:'concentration_screen', examples:[ one per candidate; input=human-readable desc, output=tag
  #        ('concentrated_win'/'meaningful_no_win'/'no_meaningful_forget'/'structure_absent'/'budget_skipped'),
  #        metadata_*: token,hierarchy,precision,footprint,concentration_score,recall_hole,firing_jaccard,absorber,
  #        max_prec_latent,set_cover_eq_max_precision,absorption_structured,meaningful_forget,
  #        delta_joint_vs_ungated_{primary,second}_{diff,ci_lo,ci_hi,excl0}, delta_joint_vs_fair_{...},
  #        kg_beats_ungated,kg_beats_fair,fair_saturated, AND predict_* STRING fields (set to op tag/'NA') ]},
  #     {dataset:'edit_predictions', examples:[ per (token,role,prompt): input=prompt, output=role,
  #        predict_kg_abl, predict_dense_sub_abl, predict_dense_sub_gated_fair, predict_max_precision, predict_noop
  #        (continuation STRINGS), metadata_*: token,role,sub_probe_drop_kg, joint_kg, joint_ungated, joint_fair, s_op_* ]}
  #   EVERY example in EVERY dataset MUST carry the five predict_* keys as STRINGS (iter-5 GOTCHA: missing/
  #   non-string predict_* => validator FAIL). Use make_variants.py (copied from iter-7) to emit
  #   full/mini/preview_method_out.json each <100MB; validate all three with aii-json against exp_gen_sol_out.
  #   Exclude cache/ and .venv/ from the uploaded artifact.

  # ============================ COST / TIME BUDGET ==================================================
  # $0 screen over the full pool first. Editing ~12-16 candidates x 2 judges x ~64 continuations ~= $1.5-2.5 (iter-7
  # was $0.80 for 5 cases). Hard-stop judge calls at SPENT>=3.0. GPU wall-clock budget ~5h of the 6h: encoding is the
  # bulk (cached); generation+forward sweeps dominate per edited candidate (~10-15 min each). PID-based process mgmt only.
fallback_plan: |-
  DATA / REBUILD failures: (1) If `pipeline.py --scale full --no-llm` for the homograph dataset errors (geonamescache/protobuf/libgomp quirks seen in prior iters), fall back to `--scale smoke` for structure then hand-load the entities directly from HG_DIR/data.py's entity gazetteers + D1-style corpus windows; if it still fails, DROP the homograph hierarchies and run the base-widener on SPELLING words alone (L/O/T/I/D give 20-40 candidates -- enough for the population test and >=4-win target on concentrated spelling absorbers). (2) If a candidate has too few corpus positives for a trustworthy u_sub/d_sub (n_pos<MIN_SUB=20, AUC<0.9), mark it descriptive_only and keep it in the $0 screen (still contributes concentration + structure + set_cover flag) but exclude from the edit/Delta analysis -- report the excluded count.
  OPERATOR failures: (3) If the bounded-beta (<=1) fair-gated dense CANNOT reach the matched meaningful-forget for many candidates, that is a SUBSTANTIVE result, not a bug: KG wins on forget by construction -- report it as 'fair gated dense saturates below meaningful forget at beta<=1' and compare joint collateral at the common achievable forget. Also run the alt gate_thresh (X-recall-matched) to show the conclusion is calibration-robust. (4) If generation NaNs in bf16, use the clamp_norm=True path (_make_clamped_hook, already supports the new operator).
  BUDGET / TIME truncation (pre-registered drop order, breadth-first): keep the $0 full-pool concentration screen + set_cover_inertness ALWAYS (they alone answer M3''' structurally and M5'''); then the positive-control re-runs (large, Amazon); then top-concentration new candidates until SPENT>=3.0 or time runs low; DROP (first-dropped-first) the MAX-PREC-ABL judged edit (keep its $0 set_cover_eq flag), then the second judge on lowest-concentration candidates (keep primary), then the distributed-absorption Georgia/Jordan re-edit (cite iter-7 numbers as population anchors instead). NEVER drop: the concentration screen, >=the two positive-control wins, the population correlation over whatever edited points exist.
  VERDICT robustness: (5) If <4 independent concentrated wins land, emit BASE_STAYS_THIN_RETARGET honestly (this is an expected, publishable outcome that triggers the paper's localization-first retarget) -- do NOT inflate by re-counting the confirmatory Amazon or the excluded co-firing insult as load-bearing. (6) If the population correlation is underpowered (too few edited points / wide CIs), report 'TIE/UNDERPOWERED' with n and CIs rather than asserting CONCENTRATION_PREDICTS.
  HONEST NEGATIVES to record verbatim in metadata.honest_negatives: fair-gated-dense matches KG (=> value is label-free where-to-gate discovery, gating is prior art CAST/GSS/GUARD-IT/SADI); set-cover absorber == max-precision latent for most candidates (=> method is precise-latent discovery, set-cover inert); base stays thin (n~2-3) => retarget; concentration does NOT out-predict absorption (=> reframe unsupported, report as-is); distributed-absorption candidates show no meaningful forget (carries iter-7 Georgia/Jordan); homograph rebuild required (data not shipped); positive control fails to reproduce under the new fair operator.
testing_plan: |-
  1) SMOKE (logic, ~2-5 min, $0): run with a 2-candidate pool {large (spelling, known win), Georgia (taxonomic, known no-forget loser)} and tiny caps (cap=20 rows, 3 FORGET/2 RETAIN prompts, judges DISABLED by unsetting OPENROUTER_API_KEY). CONFIRM: SAE loads (d_sae=16384, d_model=2304), determine_layer_idx selects 13 with cosine>0.9 (gating PASS), encode_rows runs, the new erase_dir_gated_fair hook executes without shape/NaN errors and its token-footprint counter is >0 on X tokens and ~0 on neutral tokens, content_responsive returns cr latents, the concentration screen emits rows with precision/footprint/concentration_score in [0,1], and large's re-derived absorber == 8463 (sanity vs iter-7). Output a valid (judge-less) method_out.json skeleton.
  2) OPERATOR UNIT CHECK ($0): on 'large', verify (a) KG-ABL sub-probe positive-rate drops monotonically with lambda; (b) DENSE-SUB-ABL-GATED-FAIR at beta=1.0 produces a LARGE sub_drop ON X tokens but tiny token_footprint on UNRELATED/neutral text (precise gate), and at beta=1.0 the on-X erasure is full-projection (sub_drop>=ungated at matched gate) -- confirming it is a strong, fair, non-over-erasing control; (c) MAX-PREC-ABL on 'large' selects a latent and set_cover_eq_max_precision resolves to a definite bool. Print the matched-forget scales s_op and confirm they are finite.
  3) MINI (~15-25 min, <$0.5): 5 candidates {large, Amazon (rebuild homograph first), one new concentrated spelling word, one new homograph entity, Jordan}. ENABLE both judges on a reduced prompt set (~10/role). CONFIRMATION SIGNALS before scaling: large reproduces KG_beats_fair (positive control passes); Jordan shows NO meaningful forget (sub_drop<0.10); Delta_joint CIs compute under both judges; SPENT tracked and well under TARGET; the population-predictor function runs on >=4 points without error. If the large positive control does NOT reproduce a KG win under the new fair operator, STOP and debug the operator/gate calibration before spending more budget.
  4) FULL: only after mini confirms the positive control + judge pipeline + cost tracking. Screen the full pool ($0), then edit most-concentrated-first until SPENT approaches 3.0 or ~5h elapsed. After completion: validate full/mini/preview method_out.json with aii-json against exp_gen_sol_out (every example has the 5 predict_* STRING keys), confirm each variant <100MB, confirm cache/ excluded. Sanity-check the verdict arithmetic (total_independent_concentrated_wins dedup by token) and that honest_negatives reflects the actual outcome (no inflation of confirmatory/co-firing cases into the load-bearing count).
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
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_1/gen_art/gen_art_research_1
out_dependency_files:
  file_list:
  - research_out.json

--- Dependency 2 ---
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
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
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

--- Dependency 3 ---
id: art_2xQn686KUmV5
type: dataset
title: >-
  Homograph/Polysemy Entity Absorption Testbed (cities, months, given-names, brands)
summary: |-
  A pure CPU/text artifact: a FOUR-hierarchy homograph/polysemy entity absorption testbed, built as a strict structural drop-in extension of the iter-1 non-spelling absorption testbed (art_t2uUbjSwpd3t). It is explicitly a NEXT-ITERATION BUILDING BLOCK (not consumed by this iteration's parallel experiments): it supplies breadth of suppressed-parent candidates so the persistent single-slice taxonomic critique (Georgia-only) can be answered with many homograph cases.

  Four `dataset`s, one per is-a hierarchy, whose surface tokens carry a strong competing NON-target sense (the competition that produces feature absorption / a suppressed-parent recall hole):
    1. city_homograph_absorption  (parent = is-a-city): Phoenix, Mobile, Reading, Bath, Nice, Buffalo, Paris, Mercury, Jackson, Columbus, Cleveland, Florence, ... (23 entities).
    2. month_name_absorption (parent = is-a-month): all 12 calendar months; homograph-strong May/March/August/April/June.
    3. given_name_absorption (parent = is-a-given-name): Grace, Hope, Mark, Will, Rose, Frank, Faith, Joy, Dawn, Jack, ... (34 entities).
    4. brand_homograph_absorption (parent = is-a-brand): Apple, Amazon, Shell, Target, Orange, Gap, Tide, Visa, Subway, Java, ... (24 entities).

  Each hierarchy ships the SAME three coordinated components as dataset_2: (A) content-flip minimal pairs (parent present vs absent, surface-matched), (B) surface-flip pairs (concept fixed, surface varied; both positive, for the unit-level surface-invariance check), and (C) a frozen monology/pile-uncopyrighted diagnostic corpus (pinned rev 3be90335b66f24456a5d6659d9c8d208c0357119) of real windows labelled by frozen, model-independent sub-context. The NEW homograph_competitor negative family (the same surface token in its non-target sense, e.g. lowercase 'apple'/'will'/'march', 'Joaquin Phoenix', 'Christopher Columbus') is the matched hard control that makes a suppressed parent visible.

  On-disk format is the AII exp_sel_data_out schema: {metadata, datasets:[{dataset, examples:[{input, output, metadata_*}]}]} with FLAT metadata_* keys (no nested objects). New/extended fields vs iter-1: metadata_hierarchy (city|month|given_name|brand), metadata_entity (canonical surface), metadata_target_sense (city|month|given_name|brand|competitor|null), metadata_competitor_sense (gloss of competing sense), metadata_homograph_strength (wordfreq Zipf of the lowercase competitor), and metadata_neg_family expanded to include homograph_competitor / other_place / other_time / other_person_ref / other_company_ref / easy. Fold semantics are unchanged (pairs 70/30 train/test by pair_id stratified by sub_context; corpus 50/50 train/diagnostic stratified), gemma-2-2b offset-mapping token anchoring is reused (metadata_target_token_indices), and the downstream K-track + form-free absorption diagnostic pipeline runs unchanged except for the new enum values.

  Labels are assigned PURELY from surface form / regex / gazetteer (geonamescache for cities) / disambiguating local context — never from a model — so the degenerate-construction guard holds and absorption presence/absence stays a future-iteration EMPIRICAL finding: the corpus equally supports the 'absorption is spelling-specific' null and a positive homograph-absorption finding. Corpus target-sense labels use high-precision case-aware cues; an LLM-judged stratified sample MEASURES per-hierarchy target-sense precision (reported in manifest.json, target >=0.9; it does not relabel the corpus). manifest.json carries per-(hierarchy,entity) absorption_readiness with diagnostic_positives counts and status (eligible if >=150 diagnostic-fold positives, else descriptive_only), eligible_entities_per_hierarchy, per-component counts, source/pile-set counts, llm_pair_pass_rate, llm_corpus_sense_precision, llm_cost_breakdown, city geonames provenance, and cross-hierarchy collision notes (Dawn, Chase, Jordan, Mercury, Paris). Deliverables: data.py, build_dataset.py, pipeline.py, schema.json, manifest.json, and full/mini/preview_data_out.json (validated against exp_sel_data_out, each <100MB). Reproducible via fixed seed 20240617 and pinned pile revision; total LLM spend well under $1.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_5/gen_art/gen_art_dataset_1
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

### [9] SYSTEM-USER prompt · 2026-06-18 20:23:53 UTC

```
<validation-feedback>
Attempt 1 failed validation.

You have not created the output file `.terminal_claude_agent_struct_out.json` yet. Use the Write tool to create it.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```

### [10] SYSTEM-USER prompt · 2026-06-18 20:28:00 UTC

```
<validation-feedback>
Attempt 2 failed validation.

You have not created the output file `.terminal_claude_agent_struct_out.json` yet. Use the Write tool to create it.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```

### [11] SYSTEM-USER prompt · 2026-06-18 20:33:32 UTC

```
<verification_failed>
Your experiment output failed verification (attempt 1/10).
</verification_failed>

<file_errors>
MISSING OR UNREADABLE FILES:
  - Missing file: full_method_out.json
  - Missing file: mini_method_out.json
  - Missing file: preview_method_out.json

Fix: Create the missing files directly in your workspace (see <workspace> above for the exact path).
     Required files: method.py, method_out.json, full_method_out.json, mini_method_out.json, preview_method_out.json
     Use 'ls' to check what files exist.
</file_errors>

<task>
FIX THESE ISSUES:
1. Create all missing files by running method.py

After making changes, verify:
- 'ls -la' shows all required files
- 'uv run method.py' completes successfully
- JSON files are valid (use aii-json skill validation)
- full_method_out.json has at least 50 examples
</task>
```

### [12] SYSTEM-USER prompt · 2026-06-18 20:37:33 UTC

```
<verification_failed>
Your experiment output failed verification (attempt 2/10).
</verification_failed>

<file_errors>
MISSING OR UNREADABLE FILES:
  - Missing file: full_method_out.json
  - Missing file: mini_method_out.json
  - Missing file: preview_method_out.json

Fix: Create the missing files directly in your workspace (see <workspace> above for the exact path).
     Required files: method.py, method_out.json, full_method_out.json, mini_method_out.json, preview_method_out.json
     Use 'ls' to check what files exist.
</file_errors>

<task>
FIX THESE ISSUES:
1. Create all missing files by running method.py

After making changes, verify:
- 'ls -la' shows all required files
- 'uv run method.py' completes successfully
- JSON files are valid (use aii-json skill validation)
- full_method_out.json has at least 50 examples
</task>
```
