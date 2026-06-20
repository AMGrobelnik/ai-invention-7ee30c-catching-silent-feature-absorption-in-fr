# gen_art_experiment_2 — test_idea

> Phase: `invention_loop` · round 3 · `gen_art`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_experiment_2` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-17 18:29:26 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_2`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_2/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_2/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_2/results/out.json`
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
  Non-Spelling Selection-Isolation: RE-k Control + AUC-Difference CIs + Router Inputs (Taxonomic lead, Numeric down-weighted)
summary: >-
  Iteration-3 re-analysis of the executed non-spelling absorption experiment (iter-2 gen_art_experiment_3). It does NOT re-run
  the discovery pipeline from scratch: it RE-USES the frozen Gemma-Scope layer_12/width_16k SAE encodings (cached lat CSR
  + residuals) and the same two-track K-track unit/anchor/(g)/(h)/dense-probe that iter-2 produced, then adds the three things
  the iter-3 mandate (M1/M2/M7) requires on the NON-SPELLING slices: (1) a RANDOM-ELIGIBLE-k pool baseline (RE-k) plus an
  anchor-fixed variant (RE-k-anchored) that isolates the two-track SET-COVER selection from cover-based eligibility+pooling;
  (2) classification AUC point values WITH bootstrap AUC-DIFFERENCE CIs (B>=10,000) for unit vs (g)/(h)/(RE-k)/(RE-k-anchored)/dense-probe
  on the defining absorbed slices (Georgia for taxonomic, integer for numeric) and all eligible slices, replacing the mislabelled
  matched-recall-accuracy deltas, with comparison-matched (Youden) thresholds for any accuracy table; (3) per-hierarchy firing-Jaccard(parent,
  top per-sub-context detector) on positives + parent per-sub-context recall holes, emitted as router inputs for M4. Re-frames
  generalization per M7: taxonomic (Georgia, diagnostic-corroborated, Jordan KG top1=0.95) is the LEAD; numeric (integer)
  is explicitly SUGGESTIVE/diagnostic-UNCONFIRMED (KG top1=0.0, dense probe 0.643 dominates). Compute: GPU (cache reuse makes
  the core CPU-cheap, but GPU guarantees the re-encode fallback).
runpod_compute_profile: gpu
implementation_pseudocode: |
  # ============================================================================
  # experiment_iter3_dir2 -- Non-spelling selection-isolation (M1) + AUC-diff CIs (M2) + router inputs (M7/M4)
  # Build a SINGLE method.py. The cheapest correct path is to COPY the iter-2 file and ADD phases D-G below.
  # Deps: dataset art_t2uUbjSwpd3t (full_data_out.json), method art_RidEJtBC7gPT, diagnostic art_I2MrezW41iQo.
  # ============================================================================

  # ---- PINNED PATHS / CONSTANTS (verified) ----
  DATA = '/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_2/full_data_out.json'
  ITER2 = '/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_3'
  #   reuse code: ITER2/method.py  (JumpReLUSAE, load_hierarchies, _select_positions, Encoder, determine_layer_idx,
  #               bootstrap_ci, paired_diff_ci, mcnemar_exact, holm, auc, match_threshold, analyze_hierarchy core,
  #               admission_check, formfree_edge_agreement, emit/predictions/csv)
  #   reuse encodings (PRIMARY fast path -- no GPU needed if they load & align):
  #       ITER2/cache/lat_numeric_w16384_n8380.npz , resid_numeric_w16384_n8380.npy
  #       ITER2/cache/lat_taxonomic_w16384_n15748.npz , resid_taxonomic_w16384_n15748.npy
  SAE_RELEASE='gemma-scope-2b-pt-res-canonical'; SAE_ID='layer_12/width_16k/canonical'; WIDTH=16384; D_MODEL=2304
  MODEL='unsloth/gemma-2-2b' (fallback google/gemma-2-2b); HOOK layer 12 == hidden_states[13]; BATCH=16; MAXLEN=288; SEED=20240617
  thresholds: PRECISION_FLOOR=0.70, JACCARD_MAX=0.10, GAIN_MIN=0.05, N_MIN_ELIGIBLE=150, GREEDY_MAX_MEMBERS=8, G1_RECALL=0.60
  HIERARCHIES order = ['taxonomic','numeric']   # taxonomic FIRST (M7 lead); numeric second
  ELIGIBLE (get_eligible) taxonomic = 20 countries [Canada,France,Iran,United States,Brazil,Georgia,New Zealand,Spain,
     Mexico,China,Japan,India,Italy,Ireland,Australia,Poland,Germany,United Kingdom,Israel,Russia];
     numeric = [year,percent,currency,date,decimal,integer,comma_number,ordinal]
  ABSORBED_DEFINING = {'taxonomic':'Georgia', 'numeric':'integer'}   # the M2 headline slices

  # ---- PHASE A: load data exactly as iter-2 (deterministic row order so cache row_ids align) ----
  data = load_hierarchies(DATA, HIERARCHIES, max_corpus=None, max_pairs=None)   # numeric 8380 rows, taxonomic 15748 rows

  # ---- PHASE B: encodings -- REUSE cache (primary) else RE-ENCODE on GPU (fallback) ----
  load SAE via JumpReLUSAE(params.npz)  # _find_sae_params('16k'); also set _GLOBAL['W_dec']=sae.W_dec.float().cpu().numpy()
  for name in HIERARCHIES:
      tag = f'{name}_w{WIDTH}_n{len(data[name])}'              # taxonomic_w16384_n15748 / numeric_w16384_n8380
      if ITER2/cache/lat_{tag}.npz and resid exist:
          lat = scipy.sparse.load_npz(...); resid = np.load(...)
          ASSERT lat.shape == (len(data[name]), WIDTH) and resid.shape[0]==len(data[name])   # row alignment guard
          # SANITY (must reproduce iter-2): recompute anchor (Phase-2 logic) -> expect 3792 (tax) / 14823 (num)
      else:  # FALLBACK: re-encode on GPU
          load_model(); layer_idx=determine_layer_idx(...) (expect 13, FVU<0.6); enc=Encoder(...);
          lat,resid,info = enc.encode_rows(data[name]); assert info.fvu<0.6 and 1<info.mean_l0<WIDTH*0.5 and info.align>=0.90
          save to local cache/.

  # ---- PHASE C: re-derive the iter-2 per-hierarchy objects (call analyze_hierarchy, OR refactor it to RETURN extras) ----
  # Need from the iter-2 pipeline, per hierarchy:
  #   anchor (int), k_track_unit (list), g_pool (top-20 |mean_pos-mean_neg| attribution), h_pool (top-len(unit)),
  #   cr_idx (content-responsive latents), precision_l[] (content-flip precision), neg_fire_rate[] (corpus-train neg firing),
  #   d_p (LogisticRegression on corpus-TRAIN residuals = dense probe), diag_rows, diagpos_rows, label[], sub[],
  #   scores{unit,anchor,g,h,dense_probe} = pool_score over diag_rows, kg_edges, formfree kg_agreement.
  # EXPECTED (sanity vs iter-2 partial_*.json):
  #   taxonomic anchor=3792 unit=[3792,4697,9339,8442] gpool head=[3792,12772,1322,6810,...] Georgia matched recall unit~0.713 h~0.520
  #   numeric anchor=14823 unit=[14823,11011,14413,2285] integer matched recall unit~0.283 g~0.107 h~0.110 dense~0.643

  # ---- PHASE D (NEW, M1): cover-eligible set + RE-k baselines (the SELECTION-ISOLATION decider) ----
  # cover-eligible candidate set = the pool the two-track selects members FROM:
  ELIG = [l for l in cr_idx if precision_l[l] >= PRECISION_FLOOR and neg_fire_rate[l] < 0.5]   # report len(ELIG)
  if len(ELIG) < len(unit): ELIG = [l for l in cr_idx if precision_l[l] >= PRECISION_FLOOR]   # relax guard, then cr_idx
  k = len(unit)                                  # = 4 for both hierarchies
  B_DRAWS = 1000
  # scores over diag_rows for a pool = max over members of SAE latent activation (same pool_score rule as unit/g/h)
  for draw in range(B_DRAWS):
      pool      = rng.choice(ELIG, size=k, replace=False)               # RE-k : k random eligible
      pool_anch = [anchor] + list(rng.choice([e for e in ELIG if e!=anchor], size=k-1, replace=False))  # RE-k-anchored
      rek_scores[draw]      = pool_score(pool)         # [n_diag]
      rek_anch_scores[draw] = pool_score(pool_anch)
  # representative single-detector baselines for the AUC-difference CI:
  rek_mean_score      = mean over draws of rek_scores       # [n_diag]  (average random-eligible pool)
  rek_anch_mean_score = mean over draws of rek_anch_scores  # [n_diag]
  # ALSO keep one representative draw (median-AUC-on-defining-slice draw) for per-row predictions emit.

  # ---- PHASE E (NEW, M2/R1): per-sub-context AUC + bootstrap AUC-DIFFERENCE CIs ----
  def point_auc(scores, y): return roc_auc_score(y, scores)               # sklearn; 0.5 if one class
  def auc_diff_ci(sa, sb, y, B=10000):                                    # STRATIFIED paired bootstrap on AUC difference
      pos=np.where(y==1)[0]; neg=np.where(y==0)[0]
      d=[]
      for _ in range(B):
          ip=rng.integers(0,len(pos),len(pos)); ineg=rng.integers(0,len(neg),len(neg))
          idx=np.concatenate([pos[ip],neg[ineg]])                         # resample pos & neg separately (prevalence stable)
          d.append(point_auc(sa[idx],y[idx]) - point_auc(sb[idx],y[idx]))
      return float(np.mean(d)), float(np.percentile(d,2.5)), float(np.percentile(d,97.5))
  # Build per-slice detection task: positives = that sub-context's diagnostic positives; negatives = ALL diagnostic negatives
  # of the hierarchy (label==0 corpus diag rows). DETECTORS = {unit,anchor,g,h,dense_probe, rek_mean, rek_anch_mean}.
  for s in ELIGIBLE[name] + [ABSORBED_DEFINING[name]] (dedup) + descriptive subs of interest (Jordan,United States,decimal,year):
      pos = diag positives of s; neg = diag negatives; y=[1]*|pos|+[0]*|neg|; n_pos=|pos|
      auc_point[s] = {det: point_auc(concat(scores[det][pos],scores[det][neg]), y) for det in DETECTORS}
      eligible_flag = (s in ELIGIBLE[name]) and n_pos >= N_MIN_ELIGIBLE
      for comp in ['g','h','rek_mean','rek_anch_mean','dense_probe']:
          auc_diff[s][comp] = auc_diff_ci(unit_slice_scores, comp_slice_scores, y, B=10000)  # diff, ci_lo, ci_hi
      # RE-k DRAW DISTRIBUTION (selection-isolation, primary M1 object):
      rek_draw_aucs      = [point_auc(concat(rek_scores[d][pos],rek_scores[d][neg]), y) for d in range(B_DRAWS)]
      rek_anch_draw_aucs = [...same with rek_anch_scores...]
      rek_dist[s] = {mean, median, p5, p95, p97_5, unit_auc, unit_percentile_in_draws, unit_above_95th(bool)} for both variants
  # DECISION RULE per slice (record, do not gate the whole run):
  #   SELECTION_ESTABLISHED[s] = (unit_auc > rek_anch p95) AND (auc_diff[s]['rek_anch_mean'].ci_lo > 0)
  #   (RE-k-anchored is the honest control: it holds the high-recall anchor fixed and asks whether the SET-COVER choice of
  #    absorbers beats random eligible absorbers. RE-k-full is also reported as the literal M1 control.)

  # ---- PHASE F (NEW, R1 anti-collapse): comparison-matched (Youden) accuracy table ----
  # For any ACCURACY comparison choose each detector's threshold by Youden-J on a TRAIN split of {pos,neg} (or on the
  # fitted F1 BUT verify no detector predicts-all-positive). Report per-detector operating point + accuracy so NO baseline
  # collapses to predict-all (the iter-2 matched-recall table forced every detector to the SAME recall, which is what made
  # (h) look degenerate). Keep the iter-2 matched-recall numbers too, clearly LABELLED 'matched-recall accuracy (legacy)'.

  # ---- PHASE G (NEW, M7/M4 router inputs): firing-Jaccard(parent,detector) + parent recall holes ----
  for name in HIERARCHIES:
    parent = anchor; anchor_fire = (lat[diagpos_rows][:,parent]>0)              # [n_pos] bool
    for s in ELIGIBLE[name] + absorbed/descriptive subs:
       pos_s = diagpos rows of s
       # top per-sub-context detector = eligible latent (!=parent) with highest firing recall on pos_s
       top_det = argmax over l in ELIG\{parent} of mean(lat[pos_s][:,l]>0)
       fj = firing_jaccard(parent,top_det) over diag POSITIVES (toxic/positive-only Jaccard, matching the router definition):
            inter=|fire_parent & fire_det| ; union=|fire_parent | fire_det| (over all diag positives) ; fj=inter/union
       parent_recall_on_s = mean(anchor_fire over pos_s)        # == sliced recall_raw['anchor']
       router[name][s] = {parent_latent, top_detector_latent, firing_jaccard, detector_recall_on_s,
                          parent_recall_on_s, parent_recall_hole = 1-parent_recall_on_s}
    router[name]['regime'] = 'mutually_exclusive(absorption)' if median(fj over absorbed subs) < JACCARD_MAX
                              else 'co_firing(splitting)'      # expect taxonomic & numeric BOTH absorption
  # (This produces the non-spelling rows of the M4 prediction-vs-outcome router table downstream.)

  # ---- PHASE H: KG-agreement (reuse formfree_edge_agreement) + M7 framing flags ----
  # Recompute/keep kg_agreement per hierarchy (taxonomic mean top1 ~0.318, Jordan edge ~0.95 above null; numeric ~0.0).
  # Set framing: per_hierarchy[name]['generalization_status'] =
  #    'diagnostic_corroborated' if name=='taxonomic' (Georgia win vs h + Jordan KG corroboration)
  #    'suggestive_diagnostic_unconfirmed' if name=='numeric' (integer beats g/h on matched recall BUT KG top1=0.0 AND dense 0.643 dominates).
  # Record honest notes: Georgia KG edge top1=0.0 (greedy picked low-precision 4697 over high-precision 16009);
  #    Jordan n=124 < 150 -> DESCRIPTIVE/underpowered though KG-corroborated; United States: unit collapses at matched tau
  #    (0.353) and g/h already cover it -> NOT a selection win; gains are sub-context-specific (20-oracle wins year/date/decimal).

  # ---- PHASE I: emit (exp_gen_sol_out schema, same shape as iter-2) ----
  out = {'metadata': {method_name, verdict, sae{...}, model, encoding, stats{bootstrap_B_auc:10000, B_draws:1000, seed},
                      thresholds, per_hierarchy: {taxonomic:{...all of C..H, auc_point, auc_diff_ci, rek_dist,
                      selection_established, router, generalization_status, honest_notes}, numeric:{...}}},
         'datasets': [ {dataset:'taxonomic_absorption', examples:[per-row diag predictions]}, {dataset:'numeric_absorption', ...} ]}
  # per-row predictions: extend iter-2 make_predictions to ADD predict_rek (representative draw thresholded at its Youden tau)
  #   so each diag row carries predict_{unit,anchor,g,h,rek,dense_probe} + sub_context + target_text.
  write method_out.json (json.dumps default=_json_default); also results/results.json (metadata only) + sliced CSVs.
  # verdict = 'taxonomic_selection_established' if SELECTION_ESTABLISHED['Georgia'] else
  #           'eligibility_pooling_only' (honest reframe per M1) ; numeric always reported suggestive.

  # ---- PHASE J: file-size compliance ----
  use aii-json skill: validate method_out.json against the exp_gen_sol_out schema; generate mini_/preview_ variants;
  assert full/mini/preview each < 100MB (iter-2 full was 7.7MB with ~11k diag rows -> safe; cap per-row predict rows at 20000).
fallback_plan: |-
  CACHE REUSE FAILS (file missing, shape != (n,16384), or anchor sanity != 3792/14823): fall back to GPU re-encode using the iter-2 Encoder/determine_layer_idx verbatim (expect hidden_states[13], FVU<0.6, align>=0.90, 1<L0<8192). This is why the profile is GPU even though the new math is CPU-cheap. GPU OOM during re-encode: lower BATCH 16->8->4, set PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True, process taxonomic then numeric sequentially with gc.collect()+torch.cuda.empty_cache() between (iter-2 already does this).

  SCIENTIFIC OUTCOMES ARE ALL PUBLISHABLE (do NOT treat any as failure):
  - Unit does NOT beat RE-k / RE-k-anchored on the absorbed slices (CI includes 0 or unit below draw p95): this is the declared honest reframe (M1) -> set verdict='eligibility_pooling_only', state plainly that cover-based ELIGIBILITY + pooling, not set-cover SELECTION, drives the non-spelling result. Still emit all numbers.
  - Georgia AUC-difference vs (h) CI includes 0 even though matched-recall excluded 0: report that the Georgia advantage is a threshold/operating-point effect, not an AUC-rank effect -- exactly the R1 honesty fix; say so.
  - Numeric integer AUC-diff vs RE-k excludes 0 but dense_probe AUC dominates and KG top1=0.0: keep numeric as 'suggestive_diagnostic_unconfirmed' (M7); do not promote it.
  - |ELIG| too small for k distinct draws: relax to precision-only filter, then to cr_idx; if still < k, report RE-k as not-computable for that hierarchy and rely on RE-k-anchored only; log the reason.
  - formfree_edge_agreement / dense probe degenerate (one-class slice, AUC undefined): mark that slice descriptive_only and skip its CI (do not fabricate 0.5).

  If time runs short: TAXONOMIC is the lead (M7) and is fully cached -- complete taxonomic (RE-k + RE-k-anchored + AUC-diff CIs on Georgia + all 20 eligible + Jordan/US descriptive + router) FIRST and emit; numeric (integer + 8 subs + router) is the demotable second hierarchy. Never drop: Georgia AUC-diff CIs vs (h)/(RE-k)/(RE-k-anchored)/dense, the RE-k draw distribution on Georgia, and the per-hierarchy router inputs.
testing_plan: |-
  Gradual scaling with confirmation signals BEFORE the full run (reuse iter-2 --scale flags + a new fast path):
  1. CACHE-LOAD SMOKE (no GPU): load lat/resid for taxonomic; assert shape (15748,16384)/(15748,2304); rebuild content-responsive+anchor on the train pairs; CONFIRM anchor==3792. Repeat numeric -> CONFIRM anchor==14823. If either mismatches, switch to re-encode fallback before proceeding.
  2. REPRODUCE iter-2 (regression check): run the legacy matched-recall path on Georgia only; CONFIRM unit recall_matched ~0.713, h ~0.520, unit_minus_h diff ~0.193 (CI ~[0.073,0.307]); on integer CONFIRM unit ~0.283, g/h ~0.11, dense ~0.643. These reproduce the iter-2 partials and prove the encodings + pipeline are wired correctly.
  3. AUC SANITY on Georgia: point_auc(unit) should be high (>0.95 given recall_raw unit=1.0 vs negatives FP~0.014); point_auc(h) lower; auc_diff_ci(unit,h) returns finite (diff, lo, hi) with B=2000 in the test (B=10000 for the real run). Confirm no NaN and lo<=diff<=hi.
  4. RE-k MICRO (B_DRAWS=50): confirm rng.choice draws k=4 distinct eligible latents, pool_score runs, rek draw-AUC list has 50 finite entries; confirm RE-k-anchored always contains the anchor. Then scale B_DRAWS=1000.
  5. ROUTER spot-check: for Georgia, top_detector should be a high-recall Georgia latent and firing_jaccard(parent,top_det) should be < 0.10 (mutually exclusive -> absorption regime); parent_recall_hole on Georgia ~ 0.80 (anchor recall_raw 0.20). Confirm regime classifies as absorption.
  6. FULL taxonomic -> checkpoint results/partial_taxonomic_iter3.json -> then FULL numeric. After each, log verdict + Georgia/integer AUC-diff CIs.
  7. OUTPUT validation: run aii-json to schema-validate method_out.json, generate mini/preview, assert each <100MB; open results.json and eyeball per_hierarchy.taxonomic.selection_established and router.regime. Stop and report if Georgia RE-k-anchored CI is the deciding (selection vs eligibility) result either way.
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

### [2] HUMAN-USER prompt · 2026-06-17 18:29:26 UTC

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

### [3] SKILL-INPUT — aii-python · 2026-06-17 18:29:38 UTC

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

### [4] SKILL-INPUT — aii-long-running-tasks · 2026-06-17 18:29:38 UTC

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

### [5] SKILL-INPUT — aii-json · 2026-06-17 18:29:38 UTC

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

### [6] SKILL-INPUT — aii-file-size-limit · 2026-06-17 18:29:38 UTC

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

### [7] SKILL-INPUT — aii-use-hardware · 2026-06-17 18:29:38 UTC

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

### [8] SKILL-INPUT — aii-parallel-computing · 2026-06-17 18:29:38 UTC

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

### [9] SYSTEM-USER prompt · 2026-06-17 19:03:09 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_2`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_2/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_2/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_2/results/out.json`
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
  Non-Spelling Selection-Isolation: RE-k Control + AUC-Difference CIs + Router Inputs (Taxonomic lead, Numeric down-weighted)
summary: >-
  Iteration-3 re-analysis of the executed non-spelling absorption experiment (iter-2 gen_art_experiment_3). It does NOT re-run
  the discovery pipeline from scratch: it RE-USES the frozen Gemma-Scope layer_12/width_16k SAE encodings (cached lat CSR
  + residuals) and the same two-track K-track unit/anchor/(g)/(h)/dense-probe that iter-2 produced, then adds the three things
  the iter-3 mandate (M1/M2/M7) requires on the NON-SPELLING slices: (1) a RANDOM-ELIGIBLE-k pool baseline (RE-k) plus an
  anchor-fixed variant (RE-k-anchored) that isolates the two-track SET-COVER selection from cover-based eligibility+pooling;
  (2) classification AUC point values WITH bootstrap AUC-DIFFERENCE CIs (B>=10,000) for unit vs (g)/(h)/(RE-k)/(RE-k-anchored)/dense-probe
  on the defining absorbed slices (Georgia for taxonomic, integer for numeric) and all eligible slices, replacing the mislabelled
  matched-recall-accuracy deltas, with comparison-matched (Youden) thresholds for any accuracy table; (3) per-hierarchy firing-Jaccard(parent,
  top per-sub-context detector) on positives + parent per-sub-context recall holes, emitted as router inputs for M4. Re-frames
  generalization per M7: taxonomic (Georgia, diagnostic-corroborated, Jordan KG top1=0.95) is the LEAD; numeric (integer)
  is explicitly SUGGESTIVE/diagnostic-UNCONFIRMED (KG top1=0.0, dense probe 0.643 dominates). Compute: GPU (cache reuse makes
  the core CPU-cheap, but GPU guarantees the re-encode fallback).
runpod_compute_profile: gpu
implementation_pseudocode: |
  # ============================================================================
  # experiment_iter3_dir2 -- Non-spelling selection-isolation (M1) + AUC-diff CIs (M2) + router inputs (M7/M4)
  # Build a SINGLE method.py. The cheapest correct path is to COPY the iter-2 file and ADD phases D-G below.
  # Deps: dataset art_t2uUbjSwpd3t (full_data_out.json), method art_RidEJtBC7gPT, diagnostic art_I2MrezW41iQo.
  # ============================================================================

  # ---- PINNED PATHS / CONSTANTS (verified) ----
  DATA = '/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_2/full_data_out.json'
  ITER2 = '/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_3'
  #   reuse code: ITER2/method.py  (JumpReLUSAE, load_hierarchies, _select_positions, Encoder, determine_layer_idx,
  #               bootstrap_ci, paired_diff_ci, mcnemar_exact, holm, auc, match_threshold, analyze_hierarchy core,
  #               admission_check, formfree_edge_agreement, emit/predictions/csv)
  #   reuse encodings (PRIMARY fast path -- no GPU needed if they load & align):
  #       ITER2/cache/lat_numeric_w16384_n8380.npz , resid_numeric_w16384_n8380.npy
  #       ITER2/cache/lat_taxonomic_w16384_n15748.npz , resid_taxonomic_w16384_n15748.npy
  SAE_RELEASE='gemma-scope-2b-pt-res-canonical'; SAE_ID='layer_12/width_16k/canonical'; WIDTH=16384; D_MODEL=2304
  MODEL='unsloth/gemma-2-2b' (fallback google/gemma-2-2b); HOOK layer 12 == hidden_states[13]; BATCH=16; MAXLEN=288; SEED=20240617
  thresholds: PRECISION_FLOOR=0.70, JACCARD_MAX=0.10, GAIN_MIN=0.05, N_MIN_ELIGIBLE=150, GREEDY_MAX_MEMBERS=8, G1_RECALL=0.60
  HIERARCHIES order = ['taxonomic','numeric']   # taxonomic FIRST (M7 lead); numeric second
  ELIGIBLE (get_eligible) taxonomic = 20 countries [Canada,France,Iran,United States,Brazil,Georgia,New Zealand,Spain,
     Mexico,China,Japan,India,Italy,Ireland,Australia,Poland,Germany,United Kingdom,Israel,Russia];
     numeric = [year,percent,currency,date,decimal,integer,comma_number,ordinal]
  ABSORBED_DEFINING = {'taxonomic':'Georgia', 'numeric':'integer'}   # the M2 headline slices

  # ---- PHASE A: load data exactly as iter-2 (deterministic row order so cache row_ids align) ----
  data = load_hierarchies(DATA, HIERARCHIES, max_corpus=None, max_pairs=None)   # numeric 8380 rows, taxonomic 15748 rows

  # ---- PHASE B: encodings -- REUSE cache (primary) else RE-ENCODE on GPU (fallback) ----
  load SAE via JumpReLUSAE(params.npz)  # _find_sae_params('16k'); also set _GLOBAL['W_dec']=sae.W_dec.float().cpu().numpy()
  for name in HIERARCHIES:
      tag = f'{name}_w{WIDTH}_n{len(data[name])}'              # taxonomic_w16384_n15748 / numeric_w16384_n8380
      if ITER2/cache/lat_{tag}.npz and resid exist:
          lat = scipy.sparse.load_npz(...); resid = np.load(...)
          ASSERT lat.shape == (len(data[name]), WIDTH) and resid.shape[0]==len(data[name])   # row alignment guard
          # SANITY (must reproduce iter-2): recompute anchor (Phase-2 logic) -> expect 3792 (tax) / 14823 (num)
      else:  # FALLBACK: re-encode on GPU
          load_model(); layer_idx=determine_layer_idx(...) (expect 13, FVU<0.6); enc=Encoder(...);
          lat,resid,info = enc.encode_rows(data[name]); assert info.fvu<0.6 and 1<info.mean_l0<WIDTH*0.5 and info.align>=0.90
          save to local cache/.

  # ---- PHASE C: re-derive the iter-2 per-hierarchy objects (call analyze_hierarchy, OR refactor it to RETURN extras) ----
  # Need from the iter-2 pipeline, per hierarchy:
  #   anchor (int), k_track_unit (list), g_pool (top-20 |mean_pos-mean_neg| attribution), h_pool (top-len(unit)),
  #   cr_idx (content-responsive latents), precision_l[] (content-flip precision), neg_fire_rate[] (corpus-train neg firing),
  #   d_p (LogisticRegression on corpus-TRAIN residuals = dense probe), diag_rows, diagpos_rows, label[], sub[],
  #   scores{unit,anchor,g,h,dense_probe} = pool_score over diag_rows, kg_edges, formfree kg_agreement.
  # EXPECTED (sanity vs iter-2 partial_*.json):
  #   taxonomic anchor=3792 unit=[3792,4697,9339,8442] gpool head=[3792,12772,1322,6810,...] Georgia matched recall unit~0.713 h~0.520
  #   numeric anchor=14823 unit=[14823,11011,14413,2285] integer matched recall unit~0.283 g~0.107 h~0.110 dense~0.643

  # ---- PHASE D (NEW, M1): cover-eligible set + RE-k baselines (the SELECTION-ISOLATION decider) ----
  # cover-eligible candidate set = the pool the two-track selects members FROM:
  ELIG = [l for l in cr_idx if precision_l[l] >= PRECISION_FLOOR and neg_fire_rate[l] < 0.5]   # report len(ELIG)
  if len(ELIG) < len(unit): ELIG = [l for l in cr_idx if precision_l[l] >= PRECISION_FLOOR]   # relax guard, then cr_idx
  k = len(unit)                                  # = 4 for both hierarchies
  B_DRAWS = 1000
  # scores over diag_rows for a pool = max over members of SAE latent activation (same pool_score rule as unit/g/h)
  for draw in range(B_DRAWS):
      pool      = rng.choice(ELIG, size=k, replace=False)               # RE-k : k random eligible
      pool_anch = [anchor] + list(rng.choice([e for e in ELIG if e!=anchor], size=k-1, replace=False))  # RE-k-anchored
      rek_scores[draw]      = pool_score(pool)         # [n_diag]
      rek_anch_scores[draw] = pool_score(pool_anch)
  # representative single-detector baselines for the AUC-difference CI:
  rek_mean_score      = mean over draws of rek_scores       # [n_diag]  (average random-eligible pool)
  rek_anch_mean_score = mean over draws of rek_anch_scores  # [n_diag]
  # ALSO keep one representative draw (median-AUC-on-defining-slice draw) for per-row predictions emit.

  # ---- PHASE E (NEW, M2/R1): per-sub-context AUC + bootstrap AUC-DIFFERENCE CIs ----
  def point_auc(scores, y): return roc_auc_score(y, scores)               # sklearn; 0.5 if one class
  def auc_diff_ci(sa, sb, y, B=10000):                                    # STRATIFIED paired bootstrap on AUC difference
      pos=np.where(y==1)[0]; neg=np.where(y==0)[0]
      d=[]
      for _ in range(B):
          ip=rng.integers(0,len(pos),len(pos)); ineg=rng.integers(0,len(neg),len(neg))
          idx=np.concatenate([pos[ip],neg[ineg]])                         # resample pos & neg separately (prevalence stable)
          d.append(point_auc(sa[idx],y[idx]) - point_auc(sb[idx],y[idx]))
      return float(np.mean(d)), float(np.percentile(d,2.5)), float(np.percentile(d,97.5))
  # Build per-slice detection task: positives = that sub-context's diagnostic positives; negatives = ALL diagnostic negatives
  # of the hierarchy (label==0 corpus diag rows). DETECTORS = {unit,anchor,g,h,dense_probe, rek_mean, rek_anch_mean}.
  for s in ELIGIBLE[name] + [ABSORBED_DEFINING[name]] (dedup) + descriptive subs of interest (Jordan,United States,decimal,year):
      pos = diag positives of s; neg = diag negatives; y=[1]*|pos|+[0]*|neg|; n_pos=|pos|
      auc_point[s] = {det: point_auc(concat(scores[det][pos],scores[det][neg]), y) for det in DETECTORS}
      eligible_flag = (s in ELIGIBLE[name]) and n_pos >= N_MIN_ELIGIBLE
      for comp in ['g','h','rek_mean','rek_anch_mean','dense_probe']:
          auc_diff[s][comp] = auc_diff_ci(unit_slice_scores, comp_slice_scores, y, B=10000)  # diff, ci_lo, ci_hi
      # RE-k DRAW DISTRIBUTION (selection-isolation, primary M1 object):
      rek_draw_aucs      = [point_auc(concat(rek_scores[d][pos],rek_scores[d][neg]), y) for d in range(B_DRAWS)]
      rek_anch_draw_aucs = [...same with rek_anch_scores...]
      rek_dist[s] = {mean, median, p5, p95, p97_5, unit_auc, unit_percentile_in_draws, unit_above_95th(bool)} for both variants
  # DECISION RULE per slice (record, do not gate the whole run):
  #   SELECTION_ESTABLISHED[s] = (unit_auc > rek_anch p95) AND (auc_diff[s]['rek_anch_mean'].ci_lo > 0)
  #   (RE-k-anchored is the honest control: it holds the high-recall anchor fixed and asks whether the SET-COVER choice of
  #    absorbers beats random eligible absorbers. RE-k-full is also reported as the literal M1 control.)

  # ---- PHASE F (NEW, R1 anti-collapse): comparison-matched (Youden) accuracy table ----
  # For any ACCURACY comparison choose each detector's threshold by Youden-J on a TRAIN split of {pos,neg} (or on the
  # fitted F1 BUT verify no detector predicts-all-positive). Report per-detector operating point + accuracy so NO baseline
  # collapses to predict-all (the iter-2 matched-recall table forced every detector to the SAME recall, which is what made
  # (h) look degenerate). Keep the iter-2 matched-recall numbers too, clearly LABELLED 'matched-recall accuracy (legacy)'.

  # ---- PHASE G (NEW, M7/M4 router inputs): firing-Jaccard(parent,detector) + parent recall holes ----
  for name in HIERARCHIES:
    parent = anchor; anchor_fire = (lat[diagpos_rows][:,parent]>0)              # [n_pos] bool
    for s in ELIGIBLE[name] + absorbed/descriptive subs:
       pos_s = diagpos rows of s
       # top per-sub-context detector = eligible latent (!=parent) with highest firing recall on pos_s
       top_det = argmax over l in ELIG\{parent} of mean(lat[pos_s][:,l]>0)
       fj = firing_jaccard(parent,top_det) over diag POSITIVES (toxic/positive-only Jaccard, matching the router definition):
            inter=|fire_parent & fire_det| ; union=|fire_parent | fire_det| (over all diag positives) ; fj=inter/union
       parent_recall_on_s = mean(anchor_fire over pos_s)        # == sliced recall_raw['anchor']
       router[name][s] = {parent_latent, top_detector_latent, firing_jaccard, detector_recall_on_s,
                          parent_recall_on_s, parent_recall_hole = 1-parent_recall_on_s}
    router[name]['regime'] = 'mutually_exclusive(absorption)' if median(fj over absorbed subs) < JACCARD_MAX
                              else 'co_firing(splitting)'      # expect taxonomic & numeric BOTH absorption
  # (This produces the non-spelling rows of the M4 prediction-vs-outcome router table downstream.)

  # ---- PHASE H: KG-agreement (reuse formfree_edge_agreement) + M7 framing flags ----
  # Recompute/keep kg_agreement per hierarchy (taxonomic mean top1 ~0.318, Jordan edge ~0.95 above null; numeric ~0.0).
  # Set framing: per_hierarchy[name]['generalization_status'] =
  #    'diagnostic_corroborated' if name=='taxonomic' (Georgia win vs h + Jordan KG corroboration)
  #    'suggestive_diagnostic_unconfirmed' if name=='numeric' (integer beats g/h on matched recall BUT KG top1=0.0 AND dense 0.643 dominates).
  # Record honest notes: Georgia KG edge top1=0.0 (greedy picked low-precision 4697 over high-precision 16009);
  #    Jordan n=124 < 150 -> DESCRIPTIVE/underpowered though KG-corroborated; United States: unit collapses at matched tau
  #    (0.353) and g/h already cover it -> NOT a selection win; gains are sub-context-specific (20-oracle wins year/date/decimal).

  # ---- PHASE I: emit (exp_gen_sol_out schema, same shape as iter-2) ----
  out = {'metadata': {method_name, verdict, sae{...}, model, encoding, stats{bootstrap_B_auc:10000, B_draws:1000, seed},
                      thresholds, per_hierarchy: {taxonomic:{...all of C..H, auc_point, auc_diff_ci, rek_dist,
                      selection_established, router, generalization_status, honest_notes}, numeric:{...}}},
         'datasets': [ {dataset:'taxonomic_absorption', examples:[per-row diag predictions]}, {dataset:'numeric_absorption', ...} ]}
  # per-row predictions: extend iter-2 make_predictions to ADD predict_rek (representative draw thresholded at its Youden tau)
  #   so each diag row carries predict_{unit,anchor,g,h,rek,dense_probe} + sub_context + target_text.
  write method_out.json (json.dumps default=_json_default); also results/results.json (metadata only) + sliced CSVs.
  # verdict = 'taxonomic_selection_established' if SELECTION_ESTABLISHED['Georgia'] else
  #           'eligibility_pooling_only' (honest reframe per M1) ; numeric always reported suggestive.

  # ---- PHASE J: file-size compliance ----
  use aii-json skill: validate method_out.json against the exp_gen_sol_out schema; generate mini_/preview_ variants;
  assert full/mini/preview each < 100MB (iter-2 full was 7.7MB with ~11k diag rows -> safe; cap per-row predict rows at 20000).
fallback_plan: |-
  CACHE REUSE FAILS (file missing, shape != (n,16384), or anchor sanity != 3792/14823): fall back to GPU re-encode using the iter-2 Encoder/determine_layer_idx verbatim (expect hidden_states[13], FVU<0.6, align>=0.90, 1<L0<8192). This is why the profile is GPU even though the new math is CPU-cheap. GPU OOM during re-encode: lower BATCH 16->8->4, set PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True, process taxonomic then numeric sequentially with gc.collect()+torch.cuda.empty_cache() between (iter-2 already does this).

  SCIENTIFIC OUTCOMES ARE ALL PUBLISHABLE (do NOT treat any as failure):
  - Unit does NOT beat RE-k / RE-k-anchored on the absorbed slices (CI includes 0 or unit below draw p95): this is the declared honest reframe (M1) -> set verdict='eligibility_pooling_only', state plainly that cover-based ELIGIBILITY + pooling, not set-cover SELECTION, drives the non-spelling result. Still emit all numbers.
  - Georgia AUC-difference vs (h) CI includes 0 even though matched-recall excluded 0: report that the Georgia advantage is a threshold/operating-point effect, not an AUC-rank effect -- exactly the R1 honesty fix; say so.
  - Numeric integer AUC-diff vs RE-k excludes 0 but dense_probe AUC dominates and KG top1=0.0: keep numeric as 'suggestive_diagnostic_unconfirmed' (M7); do not promote it.
  - |ELIG| too small for k distinct draws: relax to precision-only filter, then to cr_idx; if still < k, report RE-k as not-computable for that hierarchy and rely on RE-k-anchored only; log the reason.
  - formfree_edge_agreement / dense probe degenerate (one-class slice, AUC undefined): mark that slice descriptive_only and skip its CI (do not fabricate 0.5).

  If time runs short: TAXONOMIC is the lead (M7) and is fully cached -- complete taxonomic (RE-k + RE-k-anchored + AUC-diff CIs on Georgia + all 20 eligible + Jordan/US descriptive + router) FIRST and emit; numeric (integer + 8 subs + router) is the demotable second hierarchy. Never drop: Georgia AUC-diff CIs vs (h)/(RE-k)/(RE-k-anchored)/dense, the RE-k draw distribution on Georgia, and the per-hierarchy router inputs.
testing_plan: |-
  Gradual scaling with confirmation signals BEFORE the full run (reuse iter-2 --scale flags + a new fast path):
  1. CACHE-LOAD SMOKE (no GPU): load lat/resid for taxonomic; assert shape (15748,16384)/(15748,2304); rebuild content-responsive+anchor on the train pairs; CONFIRM anchor==3792. Repeat numeric -> CONFIRM anchor==14823. If either mismatches, switch to re-encode fallback before proceeding.
  2. REPRODUCE iter-2 (regression check): run the legacy matched-recall path on Georgia only; CONFIRM unit recall_matched ~0.713, h ~0.520, unit_minus_h diff ~0.193 (CI ~[0.073,0.307]); on integer CONFIRM unit ~0.283, g/h ~0.11, dense ~0.643. These reproduce the iter-2 partials and prove the encodings + pipeline are wired correctly.
  3. AUC SANITY on Georgia: point_auc(unit) should be high (>0.95 given recall_raw unit=1.0 vs negatives FP~0.014); point_auc(h) lower; auc_diff_ci(unit,h) returns finite (diff, lo, hi) with B=2000 in the test (B=10000 for the real run). Confirm no NaN and lo<=diff<=hi.
  4. RE-k MICRO (B_DRAWS=50): confirm rng.choice draws k=4 distinct eligible latents, pool_score runs, rek draw-AUC list has 50 finite entries; confirm RE-k-anchored always contains the anchor. Then scale B_DRAWS=1000.
  5. ROUTER spot-check: for Georgia, top_detector should be a high-recall Georgia latent and firing_jaccard(parent,top_det) should be < 0.10 (mutually exclusive -> absorption regime); parent_recall_hole on Georgia ~ 0.80 (anchor recall_raw 0.20). Confirm regime classifies as absorption.
  6. FULL taxonomic -> checkpoint results/partial_taxonomic_iter3.json -> then FULL numeric. After each, log verdict + Georgia/integer AUC-diff CIs.
  7. OUTPUT validation: run aii-json to schema-validate method_out.json, generate mini/preview, assert each <100MB; open results.json and eyeball per_hierarchy.taxonomic.selection_established and router.regime. Stop and report if Georgia RE-k-anchored CI is the deciding (selection vs eligibility) result either way.
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

### [10] SYSTEM-USER prompt · 2026-06-17 19:04:59 UTC

```
continue
```

### [11] SYSTEM-USER prompt · 2026-06-17 19:05:07 UTC

```
continue
```

### [12] SYSTEM-USER prompt · 2026-06-17 19:05:15 UTC

```
continue
```

### [13] SYSTEM-USER prompt · 2026-06-17 19:05:23 UTC

```
continue
```

### [14] SYSTEM-USER prompt · 2026-06-17 19:05:31 UTC

```
continue
```

### [15] SYSTEM-USER prompt · 2026-06-17 19:05:35 UTC

```
<validation-feedback>
Attempt 1 failed validation.

Schema validation found 1 problem — fix ALL of them at once:
  - at `title`: 'Non-Spelling SAE Absorption: RE-k Selection-Isolation, AUC-Difference CIs and Router Inputs' is too long (at most 90 characters, got 91)
Every required field must be present and every field type must match the schema.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```

### [16] SYSTEM-USER prompt · 2026-06-17 19:05:45 UTC

```
continue
```

### [17] SYSTEM-USER prompt · 2026-06-17 19:05:51 UTC

```
continue
```

### [18] SYSTEM-USER prompt · 2026-06-17 19:05:59 UTC

```
continue
```

### [19] SYSTEM-USER prompt · 2026-06-17 19:06:07 UTC

```
continue
```

### [20] SYSTEM-USER prompt · 2026-06-17 19:06:13 UTC

```
continue
```

### [21] SYSTEM-USER prompt · 2026-06-17 19:06:17 UTC

```
<validation-feedback>
Attempt 2 failed validation.

Schema validation found 1 problem — fix ALL of them at once:
  - at `title`: 'Non-Spelling SAE Absorption: RE-k Selection-Isolation, AUC-Difference CIs and Router Inputs' is too long (at most 90 characters, got 91)
Every required field must be present and every field type must match the schema.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```

### [22] SYSTEM-USER prompt · 2026-06-17 19:06:25 UTC

```
continue
```

### [23] SYSTEM-USER prompt · 2026-06-17 19:06:31 UTC

```
continue
```

### [24] SYSTEM-USER prompt · 2026-06-17 19:06:39 UTC

```
continue
```

### [25] SYSTEM-USER prompt · 2026-06-17 19:06:47 UTC

```
continue
```

### [26] SYSTEM-USER prompt · 2026-06-17 19:06:55 UTC

```
continue
```

### [27] SYSTEM-USER prompt · 2026-06-17 19:06:59 UTC

```
<validation-feedback>
Attempt 3 failed validation.

Schema validation found 1 problem — fix ALL of them at once:
  - at `title`: 'Non-Spelling SAE Absorption: RE-k Selection-Isolation, AUC-Difference CIs and Router Inputs' is too long (at most 90 characters, got 91)
Every required field must be present and every field type must match the schema.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```

### [28] SYSTEM-USER prompt · 2026-06-17 19:07:05 UTC

```
continue
```

### [29] SYSTEM-USER prompt · 2026-06-17 19:07:13 UTC

```
continue
```

### [30] SYSTEM-USER prompt · 2026-06-17 19:07:21 UTC

```
continue
```

### [31] SYSTEM-USER prompt · 2026-06-17 19:07:27 UTC

```
continue
```

### [32] SYSTEM-USER prompt · 2026-06-17 19:07:35 UTC

```
continue
```

### [33] SYSTEM-USER prompt · 2026-06-17 19:08:51 UTC

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
The entire worker container crashed after 2519s.
Error: output_format validation failed after 3 retries: Schema validation found 1 problem — fix ALL of them at once:
  - at `title`: 'Non-Spelling SAE Absorption: RE-k Selection-Isolation, AUC-Difference CIs and Router Inputs' is too long (at most 90 characters, got 91)
Every required field must be present and every field type must match the schema.

Last messages before the crash:
  - [agent_response] Please run /login · API Error: 401 Invalid authentication credentials
  - [agent_response] Please run /login · API Error: 401 Invalid authentication credentials
  - [agent_response] Please run /login · API Error: 401 Invalid authentication credentials
  - [agent_response] Please run /login · API Error: 401 Invalid authentication credentials
  - [agent_response] Please run /login · API Error: 401 Invalid authentication credentials
  - [agent_response] Please run /login · API Error: 401 Invalid authentication credentials
  - [agent_response] No response requested.
  - [agent_response] Please run /login · API Error: 401 Invalid authentication credentials
  - [agent_response] Please run /login · API Error: 401 Invalid authentication credentials
  - [agent_response] Please run /login · API Error: 401 Invalid authentication credentials
  - [agent_response] Please run /login · API Error: 401 Invalid authentication credentials
  - [agent_response] Please run /login · API Error: 401 Invalid authentication credentials
  - [agent_response] Please run /login · API Error: 401 Invalid authentication credentials
  - [agent_response] Please run /login · API Error: 401 Invalid authentication credentials
  - [agent_response] Please run /login · API Error: 401 Invalid authentication credentials

This was NOT a normal code error — the entire container died. Study the error
and last messages above carefully. Identify what caused the crash and be
EXTREMELY careful to avoid repeating it. Do NOT use the same approach.
</CRITICAL_WARNING__PREVIOUS_ATTEMPT_CRASHED>

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_2`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_2/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_2/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_2/results/out.json`
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
  Non-Spelling Selection-Isolation: RE-k Control + AUC-Difference CIs + Router Inputs (Taxonomic lead, Numeric down-weighted)
summary: >-
  Iteration-3 re-analysis of the executed non-spelling absorption experiment (iter-2 gen_art_experiment_3). It does NOT re-run
  the discovery pipeline from scratch: it RE-USES the frozen Gemma-Scope layer_12/width_16k SAE encodings (cached lat CSR
  + residuals) and the same two-track K-track unit/anchor/(g)/(h)/dense-probe that iter-2 produced, then adds the three things
  the iter-3 mandate (M1/M2/M7) requires on the NON-SPELLING slices: (1) a RANDOM-ELIGIBLE-k pool baseline (RE-k) plus an
  anchor-fixed variant (RE-k-anchored) that isolates the two-track SET-COVER selection from cover-based eligibility+pooling;
  (2) classification AUC point values WITH bootstrap AUC-DIFFERENCE CIs (B>=10,000) for unit vs (g)/(h)/(RE-k)/(RE-k-anchored)/dense-probe
  on the defining absorbed slices (Georgia for taxonomic, integer for numeric) and all eligible slices, replacing the mislabelled
  matched-recall-accuracy deltas, with comparison-matched (Youden) thresholds for any accuracy table; (3) per-hierarchy firing-Jaccard(parent,
  top per-sub-context detector) on positives + parent per-sub-context recall holes, emitted as router inputs for M4. Re-frames
  generalization per M7: taxonomic (Georgia, diagnostic-corroborated, Jordan KG top1=0.95) is the LEAD; numeric (integer)
  is explicitly SUGGESTIVE/diagnostic-UNCONFIRMED (KG top1=0.0, dense probe 0.643 dominates). Compute: GPU (cache reuse makes
  the core CPU-cheap, but GPU guarantees the re-encode fallback).
runpod_compute_profile: gpu
implementation_pseudocode: |
  # ============================================================================
  # experiment_iter3_dir2 -- Non-spelling selection-isolation (M1) + AUC-diff CIs (M2) + router inputs (M7/M4)
  # Build a SINGLE method.py. The cheapest correct path is to COPY the iter-2 file and ADD phases D-G below.
  # Deps: dataset art_t2uUbjSwpd3t (full_data_out.json), method art_RidEJtBC7gPT, diagnostic art_I2MrezW41iQo.
  # ============================================================================

  # ---- PINNED PATHS / CONSTANTS (verified) ----
  DATA = '/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_2/full_data_out.json'
  ITER2 = '/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_3'
  #   reuse code: ITER2/method.py  (JumpReLUSAE, load_hierarchies, _select_positions, Encoder, determine_layer_idx,
  #               bootstrap_ci, paired_diff_ci, mcnemar_exact, holm, auc, match_threshold, analyze_hierarchy core,
  #               admission_check, formfree_edge_agreement, emit/predictions/csv)
  #   reuse encodings (PRIMARY fast path -- no GPU needed if they load & align):
  #       ITER2/cache/lat_numeric_w16384_n8380.npz , resid_numeric_w16384_n8380.npy
  #       ITER2/cache/lat_taxonomic_w16384_n15748.npz , resid_taxonomic_w16384_n15748.npy
  SAE_RELEASE='gemma-scope-2b-pt-res-canonical'; SAE_ID='layer_12/width_16k/canonical'; WIDTH=16384; D_MODEL=2304
  MODEL='unsloth/gemma-2-2b' (fallback google/gemma-2-2b); HOOK layer 12 == hidden_states[13]; BATCH=16; MAXLEN=288; SEED=20240617
  thresholds: PRECISION_FLOOR=0.70, JACCARD_MAX=0.10, GAIN_MIN=0.05, N_MIN_ELIGIBLE=150, GREEDY_MAX_MEMBERS=8, G1_RECALL=0.60
  HIERARCHIES order = ['taxonomic','numeric']   # taxonomic FIRST (M7 lead); numeric second
  ELIGIBLE (get_eligible) taxonomic = 20 countries [Canada,France,Iran,United States,Brazil,Georgia,New Zealand,Spain,
     Mexico,China,Japan,India,Italy,Ireland,Australia,Poland,Germany,United Kingdom,Israel,Russia];
     numeric = [year,percent,currency,date,decimal,integer,comma_number,ordinal]
  ABSORBED_DEFINING = {'taxonomic':'Georgia', 'numeric':'integer'}   # the M2 headline slices

  # ---- PHASE A: load data exactly as iter-2 (deterministic row order so cache row_ids align) ----
  data = load_hierarchies(DATA, HIERARCHIES, max_corpus=None, max_pairs=None)   # numeric 8380 rows, taxonomic 15748 rows

  # ---- PHASE B: encodings -- REUSE cache (primary) else RE-ENCODE on GPU (fallback) ----
  load SAE via JumpReLUSAE(params.npz)  # _find_sae_params('16k'); also set _GLOBAL['W_dec']=sae.W_dec.float().cpu().numpy()
  for name in HIERARCHIES:
      tag = f'{name}_w{WIDTH}_n{len(data[name])}'              # taxonomic_w16384_n15748 / numeric_w16384_n8380
      if ITER2/cache/lat_{tag}.npz and resid exist:
          lat = scipy.sparse.load_npz(...); resid = np.load(...)
          ASSERT lat.shape == (len(data[name]), WIDTH) and resid.shape[0]==len(data[name])   # row alignment guard
          # SANITY (must reproduce iter-2): recompute anchor (Phase-2 logic) -> expect 3792 (tax) / 14823 (num)
      else:  # FALLBACK: re-encode on GPU
          load_model(); layer_idx=determine_layer_idx(...) (expect 13, FVU<0.6); enc=Encoder(...);
          lat,resid,info = enc.encode_rows(data[name]); assert info.fvu<0.6 and 1<info.mean_l0<WIDTH*0.5 and info.align>=0.90
          save to local cache/.

  # ---- PHASE C: re-derive the iter-2 per-hierarchy objects (call analyze_hierarchy, OR refactor it to RETURN extras) ----
  # Need from the iter-2 pipeline, per hierarchy:
  #   anchor (int), k_track_unit (list), g_pool (top-20 |mean_pos-mean_neg| attribution), h_pool (top-len(unit)),
  #   cr_idx (content-responsive latents), precision_l[] (content-flip precision), neg_fire_rate[] (corpus-train neg firing),
  #   d_p (LogisticRegression on corpus-TRAIN residuals = dense probe), diag_rows, diagpos_rows, label[], sub[],
  #   scores{unit,anchor,g,h,dense_probe} = pool_score over diag_rows, kg_edges, formfree kg_agreement.
  # EXPECTED (sanity vs iter-2 partial_*.json):
  #   taxonomic anchor=3792 unit=[3792,4697,9339,8442] gpool head=[3792,12772,1322,6810,...] Georgia matched recall unit~0.713 h~0.520
  #   numeric anchor=14823 unit=[14823,11011,14413,2285] integer matched recall unit~0.283 g~0.107 h~0.110 dense~0.643

  # ---- PHASE D (NEW, M1): cover-eligible set + RE-k baselines (the SELECTION-ISOLATION decider) ----
  # cover-eligible candidate set = the pool the two-track selects members FROM:
  ELIG = [l for l in cr_idx if precision_l[l] >= PRECISION_FLOOR and neg_fire_rate[l] < 0.5]   # report len(ELIG)
  if len(ELIG) < len(unit): ELIG = [l for l in cr_idx if precision_l[l] >= PRECISION_FLOOR]   # relax guard, then cr_idx
  k = len(unit)                                  # = 4 for both hierarchies
  B_DRAWS = 1000
  # scores over diag_rows for a pool = max over members of SAE latent activation (same pool_score rule as unit/g/h)
  for draw in range(B_DRAWS):
      pool      = rng.choice(ELIG, size=k, replace=False)               # RE-k : k random eligible
      pool_anch = [anchor] + list(rng.choice([e for e in ELIG if e!=anchor], size=k-1, replace=False))  # RE-k-anchored
      rek_scores[draw]      = pool_score(pool)         # [n_diag]
      rek_anch_scores[draw] = pool_score(pool_anch)
  # representative single-detector baselines for the AUC-difference CI:
  rek_mean_score      = mean over draws of rek_scores       # [n_diag]  (average random-eligible pool)
  rek_anch_mean_score = mean over draws of rek_anch_scores  # [n_diag]
  # ALSO keep one representative draw (median-AUC-on-defining-slice draw) for per-row predictions emit.

  # ---- PHASE E (NEW, M2/R1): per-sub-context AUC + bootstrap AUC-DIFFERENCE CIs ----
  def point_auc(scores, y): return roc_auc_score(y, scores)               # sklearn; 0.5 if one class
  def auc_diff_ci(sa, sb, y, B=10000):                                    # STRATIFIED paired bootstrap on AUC difference
      pos=np.where(y==1)[0]; neg=np.where(y==0)[0]
      d=[]
      for _ in range(B):
          ip=rng.integers(0,len(pos),len(pos)); ineg=rng.integers(0,len(neg),len(neg))
          idx=np.concatenate([pos[ip],neg[ineg]])                         # resample pos & neg separately (prevalence stable)
          d.append(point_auc(sa[idx],y[idx]) - point_auc(sb[idx],y[idx]))
      return float(np.mean(d)), float(np.percentile(d,2.5)), float(np.percentile(d,97.5))
  # Build per-slice detection task: positives = that sub-context's diagnostic positives; negatives = ALL diagnostic negatives
  # of the hierarchy (label==0 corpus diag rows). DETECTORS = {unit,anchor,g,h,dense_probe, rek_mean, rek_anch_mean}.
  for s in ELIGIBLE[name] + [ABSORBED_DEFINING[name]] (dedup) + descriptive subs of interest (Jordan,United States,decimal,year):
      pos = diag positives of s; neg = diag negatives; y=[1]*|pos|+[0]*|neg|; n_pos=|pos|
      auc_point[s] = {det: point_auc(concat(scores[det][pos],scores[det][neg]), y) for det in DETECTORS}
      eligible_flag = (s in ELIGIBLE[name]) and n_pos >= N_MIN_ELIGIBLE
      for comp in ['g','h','rek_mean','rek_anch_mean','dense_probe']:
          auc_diff[s][comp] = auc_diff_ci(unit_slice_scores, comp_slice_scores, y, B=10000)  # diff, ci_lo, ci_hi
      # RE-k DRAW DISTRIBUTION (selection-isolation, primary M1 object):
      rek_draw_aucs      = [point_auc(concat(rek_scores[d][pos],rek_scores[d][neg]), y) for d in range(B_DRAWS)]
      rek_anch_draw_aucs = [...same with rek_anch_scores...]
      rek_dist[s] = {mean, median, p5, p95, p97_5, unit_auc, unit_percentile_in_draws, unit_above_95th(bool)} for both variants
  # DECISION RULE per slice (record, do not gate the whole run):
  #   SELECTION_ESTABLISHED[s] = (unit_auc > rek_anch p95) AND (auc_diff[s]['rek_anch_mean'].ci_lo > 0)
  #   (RE-k-anchored is the honest control: it holds the high-recall anchor fixed and asks whether the SET-COVER choice of
  #    absorbers beats random eligible absorbers. RE-k-full is also reported as the literal M1 control.)

  # ---- PHASE F (NEW, R1 anti-collapse): comparison-matched (Youden) accuracy table ----
  # For any ACCURACY comparison choose each detector's threshold by Youden-J on a TRAIN split of {pos,neg} (or on the
  # fitted F1 BUT verify no detector predicts-all-positive). Report per-detector operating point + accuracy so NO baseline
  # collapses to predict-all (the iter-2 matched-recall table forced every detector to the SAME recall, which is what made
  # (h) look degenerate). Keep the iter-2 matched-recall numbers too, clearly LABELLED 'matched-recall accuracy (legacy)'.

  # ---- PHASE G (NEW, M7/M4 router inputs): firing-Jaccard(parent,detector) + parent recall holes ----
  for name in HIERARCHIES:
    parent = anchor; anchor_fire = (lat[diagpos_rows][:,parent]>0)              # [n_pos] bool
    for s in ELIGIBLE[name] + absorbed/descriptive subs:
       pos_s = diagpos rows of s
       # top per-sub-context detector = eligible latent (!=parent) with highest firing recall on pos_s
       top_det = argmax over l in ELIG\{parent} of mean(lat[pos_s][:,l]>0)
       fj = firing_jaccard(parent,top_det) over diag POSITIVES (toxic/positive-only Jaccard, matching the router definition):
            inter=|fire_parent & fire_det| ; union=|fire_parent | fire_det| (over all diag positives) ; fj=inter/union
       parent_recall_on_s = mean(anchor_fire over pos_s)        # == sliced recall_raw['anchor']
       router[name][s] = {parent_latent, top_detector_latent, firing_jaccard, detector_recall_on_s,
                          parent_recall_on_s, parent_recall_hole = 1-parent_recall_on_s}
    router[name]['regime'] = 'mutually_exclusive(absorption)' if median(fj over absorbed subs) < JACCARD_MAX
                              else 'co_firing(splitting)'      # expect taxonomic & numeric BOTH absorption
  # (This produces the non-spelling rows of the M4 prediction-vs-outcome router table downstream.)

  # ---- PHASE H: KG-agreement (reuse formfree_edge_agreement) + M7 framing flags ----
  # Recompute/keep kg_agreement per hierarchy (taxonomic mean top1 ~0.318, Jordan edge ~0.95 above null; numeric ~0.0).
  # Set framing: per_hierarchy[name]['generalization_status'] =
  #    'diagnostic_corroborated' if name=='taxonomic' (Georgia win vs h + Jordan KG corroboration)
  #    'suggestive_diagnostic_unconfirmed' if name=='numeric' (integer beats g/h on matched recall BUT KG top1=0.0 AND dense 0.643 dominates).
  # Record honest notes: Georgia KG edge top1=0.0 (greedy picked low-precision 4697 over high-precision 16009);
  #    Jordan n=124 < 150 -> DESCRIPTIVE/underpowered though KG-corroborated; United States: unit collapses at matched tau
  #    (0.353) and g/h already cover it -> NOT a selection win; gains are sub-context-specific (20-oracle wins year/date/decimal).

  # ---- PHASE I: emit (exp_gen_sol_out schema, same shape as iter-2) ----
  out = {'metadata': {method_name, verdict, sae{...}, model, encoding, stats{bootstrap_B_auc:10000, B_draws:1000, seed},
                      thresholds, per_hierarchy: {taxonomic:{...all of C..H, auc_point, auc_diff_ci, rek_dist,
                      selection_established, router, generalization_status, honest_notes}, numeric:{...}}},
         'datasets': [ {dataset:'taxonomic_absorption', examples:[per-row diag predictions]}, {dataset:'numeric_absorption', ...} ]}
  # per-row predictions: extend iter-2 make_predictions to ADD predict_rek (representative draw thresholded at its Youden tau)
  #   so each diag row carries predict_{unit,anchor,g,h,rek,dense_probe} + sub_context + target_text.
  write method_out.json (json.dumps default=_json_default); also results/results.json (metadata only) + sliced CSVs.
  # verdict = 'taxonomic_selection_established' if SELECTION_ESTABLISHED['Georgia'] else
  #           'eligibility_pooling_only' (honest reframe per M1) ; numeric always reported suggestive.

  # ---- PHASE J: file-size compliance ----
  use aii-json skill: validate method_out.json against the exp_gen_sol_out schema; generate mini_/preview_ variants;
  assert full/mini/preview each < 100MB (iter-2 full was 7.7MB with ~11k diag rows -> safe; cap per-row predict rows at 20000).
fallback_plan: |-
  CACHE REUSE FAILS (file missing, shape != (n,16384), or anchor sanity != 3792/14823): fall back to GPU re-encode using the iter-2 Encoder/determine_layer_idx verbatim (expect hidden_states[13], FVU<0.6, align>=0.90, 1<L0<8192). This is why the profile is GPU even though the new math is CPU-cheap. GPU OOM during re-encode: lower BATCH 16->8->4, set PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True, process taxonomic then numeric sequentially with gc.collect()+torch.cuda.empty_cache() between (iter-2 already does this).

  SCIENTIFIC OUTCOMES ARE ALL PUBLISHABLE (do NOT treat any as failure):
  - Unit does NOT beat RE-k / RE-k-anchored on the absorbed slices (CI includes 0 or unit below draw p95): this is the declared honest reframe (M1) -> set verdict='eligibility_pooling_only', state plainly that cover-based ELIGIBILITY + pooling, not set-cover SELECTION, drives the non-spelling result. Still emit all numbers.
  - Georgia AUC-difference vs (h) CI includes 0 even though matched-recall excluded 0: report that the Georgia advantage is a threshold/operating-point effect, not an AUC-rank effect -- exactly the R1 honesty fix; say so.
  - Numeric integer AUC-diff vs RE-k excludes 0 but dense_probe AUC dominates and KG top1=0.0: keep numeric as 'suggestive_diagnostic_unconfirmed' (M7); do not promote it.
  - |ELIG| too small for k distinct draws: relax to precision-only filter, then to cr_idx; if still < k, report RE-k as not-computable for that hierarchy and rely on RE-k-anchored only; log the reason.
  - formfree_edge_agreement / dense probe degenerate (one-class slice, AUC undefined): mark that slice descriptive_only and skip its CI (do not fabricate 0.5).

  If time runs short: TAXONOMIC is the lead (M7) and is fully cached -- complete taxonomic (RE-k + RE-k-anchored + AUC-diff CIs on Georgia + all 20 eligible + Jordan/US descriptive + router) FIRST and emit; numeric (integer + 8 subs + router) is the demotable second hierarchy. Never drop: Georgia AUC-diff CIs vs (h)/(RE-k)/(RE-k-anchored)/dense, the RE-k draw distribution on Georgia, and the per-hierarchy router inputs.
testing_plan: |-
  Gradual scaling with confirmation signals BEFORE the full run (reuse iter-2 --scale flags + a new fast path):
  1. CACHE-LOAD SMOKE (no GPU): load lat/resid for taxonomic; assert shape (15748,16384)/(15748,2304); rebuild content-responsive+anchor on the train pairs; CONFIRM anchor==3792. Repeat numeric -> CONFIRM anchor==14823. If either mismatches, switch to re-encode fallback before proceeding.
  2. REPRODUCE iter-2 (regression check): run the legacy matched-recall path on Georgia only; CONFIRM unit recall_matched ~0.713, h ~0.520, unit_minus_h diff ~0.193 (CI ~[0.073,0.307]); on integer CONFIRM unit ~0.283, g/h ~0.11, dense ~0.643. These reproduce the iter-2 partials and prove the encodings + pipeline are wired correctly.
  3. AUC SANITY on Georgia: point_auc(unit) should be high (>0.95 given recall_raw unit=1.0 vs negatives FP~0.014); point_auc(h) lower; auc_diff_ci(unit,h) returns finite (diff, lo, hi) with B=2000 in the test (B=10000 for the real run). Confirm no NaN and lo<=diff<=hi.
  4. RE-k MICRO (B_DRAWS=50): confirm rng.choice draws k=4 distinct eligible latents, pool_score runs, rek draw-AUC list has 50 finite entries; confirm RE-k-anchored always contains the anchor. Then scale B_DRAWS=1000.
  5. ROUTER spot-check: for Georgia, top_detector should be a high-recall Georgia latent and firing_jaccard(parent,top_det) should be < 0.10 (mutually exclusive -> absorption regime); parent_recall_hole on Georgia ~ 0.80 (anchor recall_raw 0.20). Confirm regime classifies as absorption.
  6. FULL taxonomic -> checkpoint results/partial_taxonomic_iter3.json -> then FULL numeric. After each, log verdict + Georgia/integer AUC-diff CIs.
  7. OUTPUT validation: run aii-json to schema-validate method_out.json, generate mini/preview, assert each <100MB; open results.json and eyeball per_hierarchy.taxonomic.selection_established and router.regime. Stop and report if Georgia RE-k-anchored CI is the deciding (selection vs eligibility) result either way.
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

### [34] HUMAN-USER prompt · 2026-06-17 19:08:51 UTC

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

### [35] SYSTEM-USER prompt · 2026-06-17 19:08:59 UTC

```
continue
```

### [36] SYSTEM-USER prompt · 2026-06-17 19:09:07 UTC

```
continue
```

### [37] SYSTEM-USER prompt · 2026-06-17 19:09:13 UTC

```
continue
```

### [38] SYSTEM-USER prompt · 2026-06-17 19:09:21 UTC

```
continue
```

### [39] SYSTEM-USER prompt · 2026-06-17 19:09:29 UTC

```
continue
```

### [40] SYSTEM-USER prompt · 2026-06-17 19:09:33 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_2`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_2/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_2/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_2/results/out.json`
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
  Non-Spelling Selection-Isolation: RE-k Control + AUC-Difference CIs + Router Inputs (Taxonomic lead, Numeric down-weighted)
summary: >-
  Iteration-3 re-analysis of the executed non-spelling absorption experiment (iter-2 gen_art_experiment_3). It does NOT re-run
  the discovery pipeline from scratch: it RE-USES the frozen Gemma-Scope layer_12/width_16k SAE encodings (cached lat CSR
  + residuals) and the same two-track K-track unit/anchor/(g)/(h)/dense-probe that iter-2 produced, then adds the three things
  the iter-3 mandate (M1/M2/M7) requires on the NON-SPELLING slices: (1) a RANDOM-ELIGIBLE-k pool baseline (RE-k) plus an
  anchor-fixed variant (RE-k-anchored) that isolates the two-track SET-COVER selection from cover-based eligibility+pooling;
  (2) classification AUC point values WITH bootstrap AUC-DIFFERENCE CIs (B>=10,000) for unit vs (g)/(h)/(RE-k)/(RE-k-anchored)/dense-probe
  on the defining absorbed slices (Georgia for taxonomic, integer for numeric) and all eligible slices, replacing the mislabelled
  matched-recall-accuracy deltas, with comparison-matched (Youden) thresholds for any accuracy table; (3) per-hierarchy firing-Jaccard(parent,
  top per-sub-context detector) on positives + parent per-sub-context recall holes, emitted as router inputs for M4. Re-frames
  generalization per M7: taxonomic (Georgia, diagnostic-corroborated, Jordan KG top1=0.95) is the LEAD; numeric (integer)
  is explicitly SUGGESTIVE/diagnostic-UNCONFIRMED (KG top1=0.0, dense probe 0.643 dominates). Compute: GPU (cache reuse makes
  the core CPU-cheap, but GPU guarantees the re-encode fallback).
runpod_compute_profile: gpu
implementation_pseudocode: |
  # ============================================================================
  # experiment_iter3_dir2 -- Non-spelling selection-isolation (M1) + AUC-diff CIs (M2) + router inputs (M7/M4)
  # Build a SINGLE method.py. The cheapest correct path is to COPY the iter-2 file and ADD phases D-G below.
  # Deps: dataset art_t2uUbjSwpd3t (full_data_out.json), method art_RidEJtBC7gPT, diagnostic art_I2MrezW41iQo.
  # ============================================================================

  # ---- PINNED PATHS / CONSTANTS (verified) ----
  DATA = '/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_2/full_data_out.json'
  ITER2 = '/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_3'
  #   reuse code: ITER2/method.py  (JumpReLUSAE, load_hierarchies, _select_positions, Encoder, determine_layer_idx,
  #               bootstrap_ci, paired_diff_ci, mcnemar_exact, holm, auc, match_threshold, analyze_hierarchy core,
  #               admission_check, formfree_edge_agreement, emit/predictions/csv)
  #   reuse encodings (PRIMARY fast path -- no GPU needed if they load & align):
  #       ITER2/cache/lat_numeric_w16384_n8380.npz , resid_numeric_w16384_n8380.npy
  #       ITER2/cache/lat_taxonomic_w16384_n15748.npz , resid_taxonomic_w16384_n15748.npy
  SAE_RELEASE='gemma-scope-2b-pt-res-canonical'; SAE_ID='layer_12/width_16k/canonical'; WIDTH=16384; D_MODEL=2304
  MODEL='unsloth/gemma-2-2b' (fallback google/gemma-2-2b); HOOK layer 12 == hidden_states[13]; BATCH=16; MAXLEN=288; SEED=20240617
  thresholds: PRECISION_FLOOR=0.70, JACCARD_MAX=0.10, GAIN_MIN=0.05, N_MIN_ELIGIBLE=150, GREEDY_MAX_MEMBERS=8, G1_RECALL=0.60
  HIERARCHIES order = ['taxonomic','numeric']   # taxonomic FIRST (M7 lead); numeric second
  ELIGIBLE (get_eligible) taxonomic = 20 countries [Canada,France,Iran,United States,Brazil,Georgia,New Zealand,Spain,
     Mexico,China,Japan,India,Italy,Ireland,Australia,Poland,Germany,United Kingdom,Israel,Russia];
     numeric = [year,percent,currency,date,decimal,integer,comma_number,ordinal]
  ABSORBED_DEFINING = {'taxonomic':'Georgia', 'numeric':'integer'}   # the M2 headline slices

  # ---- PHASE A: load data exactly as iter-2 (deterministic row order so cache row_ids align) ----
  data = load_hierarchies(DATA, HIERARCHIES, max_corpus=None, max_pairs=None)   # numeric 8380 rows, taxonomic 15748 rows

  # ---- PHASE B: encodings -- REUSE cache (primary) else RE-ENCODE on GPU (fallback) ----
  load SAE via JumpReLUSAE(params.npz)  # _find_sae_params('16k'); also set _GLOBAL['W_dec']=sae.W_dec.float().cpu().numpy()
  for name in HIERARCHIES:
      tag = f'{name}_w{WIDTH}_n{len(data[name])}'              # taxonomic_w16384_n15748 / numeric_w16384_n8380
      if ITER2/cache/lat_{tag}.npz and resid exist:
          lat = scipy.sparse.load_npz(...); resid = np.load(...)
          ASSERT lat.shape == (len(data[name]), WIDTH) and resid.shape[0]==len(data[name])   # row alignment guard
          # SANITY (must reproduce iter-2): recompute anchor (Phase-2 logic) -> expect 3792 (tax) / 14823 (num)
      else:  # FALLBACK: re-encode on GPU
          load_model(); layer_idx=determine_layer_idx(...) (expect 13, FVU<0.6); enc=Encoder(...);
          lat,resid,info = enc.encode_rows(data[name]); assert info.fvu<0.6 and 1<info.mean_l0<WIDTH*0.5 and info.align>=0.90
          save to local cache/.

  # ---- PHASE C: re-derive the iter-2 per-hierarchy objects (call analyze_hierarchy, OR refactor it to RETURN extras) ----
  # Need from the iter-2 pipeline, per hierarchy:
  #   anchor (int), k_track_unit (list), g_pool (top-20 |mean_pos-mean_neg| attribution), h_pool (top-len(unit)),
  #   cr_idx (content-responsive latents), precision_l[] (content-flip precision), neg_fire_rate[] (corpus-train neg firing),
  #   d_p (LogisticRegression on corpus-TRAIN residuals = dense probe), diag_rows, diagpos_rows, label[], sub[],
  #   scores{unit,anchor,g,h,dense_probe} = pool_score over diag_rows, kg_edges, formfree kg_agreement.
  # EXPECTED (sanity vs iter-2 partial_*.json):
  #   taxonomic anchor=3792 unit=[3792,4697,9339,8442] gpool head=[3792,12772,1322,6810,...] Georgia matched recall unit~0.713 h~0.520
  #   numeric anchor=14823 unit=[14823,11011,14413,2285] integer matched recall unit~0.283 g~0.107 h~0.110 dense~0.643

  # ---- PHASE D (NEW, M1): cover-eligible set + RE-k baselines (the SELECTION-ISOLATION decider) ----
  # cover-eligible candidate set = the pool the two-track selects members FROM:
  ELIG = [l for l in cr_idx if precision_l[l] >= PRECISION_FLOOR and neg_fire_rate[l] < 0.5]   # report len(ELIG)
  if len(ELIG) < len(unit): ELIG = [l for l in cr_idx if precision_l[l] >= PRECISION_FLOOR]   # relax guard, then cr_idx
  k = len(unit)                                  # = 4 for both hierarchies
  B_DRAWS = 1000
  # scores over diag_rows for a pool = max over members of SAE latent activation (same pool_score rule as unit/g/h)
  for draw in range(B_DRAWS):
      pool      = rng.choice(ELIG, size=k, replace=False)               # RE-k : k random eligible
      pool_anch = [anchor] + list(rng.choice([e for e in ELIG if e!=anchor], size=k-1, replace=False))  # RE-k-anchored
      rek_scores[draw]      = pool_score(pool)         # [n_diag]
      rek_anch_scores[draw] = pool_score(pool_anch)
  # representative single-detector baselines for the AUC-difference CI:
  rek_mean_score      = mean over draws of rek_scores       # [n_diag]  (average random-eligible pool)
  rek_anch_mean_score = mean over draws of rek_anch_scores  # [n_diag]
  # ALSO keep one representative draw (median-AUC-on-defining-slice draw) for per-row predictions emit.

  # ---- PHASE E (NEW, M2/R1): per-sub-context AUC + bootstrap AUC-DIFFERENCE CIs ----
  def point_auc(scores, y): return roc_auc_score(y, scores)               # sklearn; 0.5 if one class
  def auc_diff_ci(sa, sb, y, B=10000):                                    # STRATIFIED paired bootstrap on AUC difference
      pos=np.where(y==1)[0]; neg=np.where(y==0)[0]
      d=[]
      for _ in range(B):
          ip=rng.integers(0,len(pos),len(pos)); ineg=rng.integers(0,len(neg),len(neg))
          idx=np.concatenate([pos[ip],neg[ineg]])                         # resample pos & neg separately (prevalence stable)
          d.append(point_auc(sa[idx],y[idx]) - point_auc(sb[idx],y[idx]))
      return float(np.mean(d)), float(np.percentile(d,2.5)), float(np.percentile(d,97.5))
  # Build per-slice detection task: positives = that sub-context's diagnostic positives; negatives = ALL diagnostic negatives
  # of the hierarchy (label==0 corpus diag rows). DETECTORS = {unit,anchor,g,h,dense_probe, rek_mean, rek_anch_mean}.
  for s in ELIGIBLE[name] + [ABSORBED_DEFINING[name]] (dedup) + descriptive subs of interest (Jordan,United States,decimal,year):
      pos = diag positives of s; neg = diag negatives; y=[1]*|pos|+[0]*|neg|; n_pos=|pos|
      auc_point[s] = {det: point_auc(concat(scores[det][pos],scores[det][neg]), y) for det in DETECTORS}
      eligible_flag = (s in ELIGIBLE[name]) and n_pos >= N_MIN_ELIGIBLE
      for comp in ['g','h','rek_mean','rek_anch_mean','dense_probe']:
          auc_diff[s][comp] = auc_diff_ci(unit_slice_scores, comp_slice_scores, y, B=10000)  # diff, ci_lo, ci_hi
      # RE-k DRAW DISTRIBUTION (selection-isolation, primary M1 object):
      rek_draw_aucs      = [point_auc(concat(rek_scores[d][pos],rek_scores[d][neg]), y) for d in range(B_DRAWS)]
      rek_anch_draw_aucs = [...same with rek_anch_scores...]
      rek_dist[s] = {mean, median, p5, p95, p97_5, unit_auc, unit_percentile_in_draws, unit_above_95th(bool)} for both variants
  # DECISION RULE per slice (record, do not gate the whole run):
  #   SELECTION_ESTABLISHED[s] = (unit_auc > rek_anch p95) AND (auc_diff[s]['rek_anch_mean'].ci_lo > 0)
  #   (RE-k-anchored is the honest control: it holds the high-recall anchor fixed and asks whether the SET-COVER choice of
  #    absorbers beats random eligible absorbers. RE-k-full is also reported as the literal M1 control.)

  # ---- PHASE F (NEW, R1 anti-collapse): comparison-matched (Youden) accuracy table ----
  # For any ACCURACY comparison choose each detector's threshold by Youden-J on a TRAIN split of {pos,neg} (or on the
  # fitted F1 BUT verify no detector predicts-all-positive). Report per-detector operating point + accuracy so NO baseline
  # collapses to predict-all (the iter-2 matched-recall table forced every detector to the SAME recall, which is what made
  # (h) look degenerate). Keep the iter-2 matched-recall numbers too, clearly LABELLED 'matched-recall accuracy (legacy)'.

  # ---- PHASE G (NEW, M7/M4 router inputs): firing-Jaccard(parent,detector) + parent recall holes ----
  for name in HIERARCHIES:
    parent = anchor; anchor_fire = (lat[diagpos_rows][:,parent]>0)              # [n_pos] bool
    for s in ELIGIBLE[name] + absorbed/descriptive subs:
       pos_s = diagpos rows of s
       # top per-sub-context detector = eligible latent (!=parent) with highest firing recall on pos_s
       top_det = argmax over l in ELIG\{parent} of mean(lat[pos_s][:,l]>0)
       fj = firing_jaccard(parent,top_det) over diag POSITIVES (toxic/positive-only Jaccard, matching the router definition):
            inter=|fire_parent & fire_det| ; union=|fire_parent | fire_det| (over all diag positives) ; fj=inter/union
       parent_recall_on_s = mean(anchor_fire over pos_s)        # == sliced recall_raw['anchor']
       router[name][s] = {parent_latent, top_detector_latent, firing_jaccard, detector_recall_on_s,
                          parent_recall_on_s, parent_recall_hole = 1-parent_recall_on_s}
    router[name]['regime'] = 'mutually_exclusive(absorption)' if median(fj over absorbed subs) < JACCARD_MAX
                              else 'co_firing(splitting)'      # expect taxonomic & numeric BOTH absorption
  # (This produces the non-spelling rows of the M4 prediction-vs-outcome router table downstream.)

  # ---- PHASE H: KG-agreement (reuse formfree_edge_agreement) + M7 framing flags ----
  # Recompute/keep kg_agreement per hierarchy (taxonomic mean top1 ~0.318, Jordan edge ~0.95 above null; numeric ~0.0).
  # Set framing: per_hierarchy[name]['generalization_status'] =
  #    'diagnostic_corroborated' if name=='taxonomic' (Georgia win vs h + Jordan KG corroboration)
  #    'suggestive_diagnostic_unconfirmed' if name=='numeric' (integer beats g/h on matched recall BUT KG top1=0.0 AND dense 0.643 dominates).
  # Record honest notes: Georgia KG edge top1=0.0 (greedy picked low-precision 4697 over high-precision 16009);
  #    Jordan n=124 < 150 -> DESCRIPTIVE/underpowered though KG-corroborated; United States: unit collapses at matched tau
  #    (0.353) and g/h already cover it -> NOT a selection win; gains are sub-context-specific (20-oracle wins year/date/decimal).

  # ---- PHASE I: emit (exp_gen_sol_out schema, same shape as iter-2) ----
  out = {'metadata': {method_name, verdict, sae{...}, model, encoding, stats{bootstrap_B_auc:10000, B_draws:1000, seed},
                      thresholds, per_hierarchy: {taxonomic:{...all of C..H, auc_point, auc_diff_ci, rek_dist,
                      selection_established, router, generalization_status, honest_notes}, numeric:{...}}},
         'datasets': [ {dataset:'taxonomic_absorption', examples:[per-row diag predictions]}, {dataset:'numeric_absorption', ...} ]}
  # per-row predictions: extend iter-2 make_predictions to ADD predict_rek (representative draw thresholded at its Youden tau)
  #   so each diag row carries predict_{unit,anchor,g,h,rek,dense_probe} + sub_context + target_text.
  write method_out.json (json.dumps default=_json_default); also results/results.json (metadata only) + sliced CSVs.
  # verdict = 'taxonomic_selection_established' if SELECTION_ESTABLISHED['Georgia'] else
  #           'eligibility_pooling_only' (honest reframe per M1) ; numeric always reported suggestive.

  # ---- PHASE J: file-size compliance ----
  use aii-json skill: validate method_out.json against the exp_gen_sol_out schema; generate mini_/preview_ variants;
  assert full/mini/preview each < 100MB (iter-2 full was 7.7MB with ~11k diag rows -> safe; cap per-row predict rows at 20000).
fallback_plan: |-
  CACHE REUSE FAILS (file missing, shape != (n,16384), or anchor sanity != 3792/14823): fall back to GPU re-encode using the iter-2 Encoder/determine_layer_idx verbatim (expect hidden_states[13], FVU<0.6, align>=0.90, 1<L0<8192). This is why the profile is GPU even though the new math is CPU-cheap. GPU OOM during re-encode: lower BATCH 16->8->4, set PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True, process taxonomic then numeric sequentially with gc.collect()+torch.cuda.empty_cache() between (iter-2 already does this).

  SCIENTIFIC OUTCOMES ARE ALL PUBLISHABLE (do NOT treat any as failure):
  - Unit does NOT beat RE-k / RE-k-anchored on the absorbed slices (CI includes 0 or unit below draw p95): this is the declared honest reframe (M1) -> set verdict='eligibility_pooling_only', state plainly that cover-based ELIGIBILITY + pooling, not set-cover SELECTION, drives the non-spelling result. Still emit all numbers.
  - Georgia AUC-difference vs (h) CI includes 0 even though matched-recall excluded 0: report that the Georgia advantage is a threshold/operating-point effect, not an AUC-rank effect -- exactly the R1 honesty fix; say so.
  - Numeric integer AUC-diff vs RE-k excludes 0 but dense_probe AUC dominates and KG top1=0.0: keep numeric as 'suggestive_diagnostic_unconfirmed' (M7); do not promote it.
  - |ELIG| too small for k distinct draws: relax to precision-only filter, then to cr_idx; if still < k, report RE-k as not-computable for that hierarchy and rely on RE-k-anchored only; log the reason.
  - formfree_edge_agreement / dense probe degenerate (one-class slice, AUC undefined): mark that slice descriptive_only and skip its CI (do not fabricate 0.5).

  If time runs short: TAXONOMIC is the lead (M7) and is fully cached -- complete taxonomic (RE-k + RE-k-anchored + AUC-diff CIs on Georgia + all 20 eligible + Jordan/US descriptive + router) FIRST and emit; numeric (integer + 8 subs + router) is the demotable second hierarchy. Never drop: Georgia AUC-diff CIs vs (h)/(RE-k)/(RE-k-anchored)/dense, the RE-k draw distribution on Georgia, and the per-hierarchy router inputs.
testing_plan: |-
  Gradual scaling with confirmation signals BEFORE the full run (reuse iter-2 --scale flags + a new fast path):
  1. CACHE-LOAD SMOKE (no GPU): load lat/resid for taxonomic; assert shape (15748,16384)/(15748,2304); rebuild content-responsive+anchor on the train pairs; CONFIRM anchor==3792. Repeat numeric -> CONFIRM anchor==14823. If either mismatches, switch to re-encode fallback before proceeding.
  2. REPRODUCE iter-2 (regression check): run the legacy matched-recall path on Georgia only; CONFIRM unit recall_matched ~0.713, h ~0.520, unit_minus_h diff ~0.193 (CI ~[0.073,0.307]); on integer CONFIRM unit ~0.283, g/h ~0.11, dense ~0.643. These reproduce the iter-2 partials and prove the encodings + pipeline are wired correctly.
  3. AUC SANITY on Georgia: point_auc(unit) should be high (>0.95 given recall_raw unit=1.0 vs negatives FP~0.014); point_auc(h) lower; auc_diff_ci(unit,h) returns finite (diff, lo, hi) with B=2000 in the test (B=10000 for the real run). Confirm no NaN and lo<=diff<=hi.
  4. RE-k MICRO (B_DRAWS=50): confirm rng.choice draws k=4 distinct eligible latents, pool_score runs, rek draw-AUC list has 50 finite entries; confirm RE-k-anchored always contains the anchor. Then scale B_DRAWS=1000.
  5. ROUTER spot-check: for Georgia, top_detector should be a high-recall Georgia latent and firing_jaccard(parent,top_det) should be < 0.10 (mutually exclusive -> absorption regime); parent_recall_hole on Georgia ~ 0.80 (anchor recall_raw 0.20). Confirm regime classifies as absorption.
  6. FULL taxonomic -> checkpoint results/partial_taxonomic_iter3.json -> then FULL numeric. After each, log verdict + Georgia/integer AUC-diff CIs.
  7. OUTPUT validation: run aii-json to schema-validate method_out.json, generate mini/preview, assert each <100MB; open results.json and eyeball per_hierarchy.taxonomic.selection_established and router.regime. Stop and report if Georgia RE-k-anchored CI is the deciding (selection vs eligibility) result either way.
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

### [41] SYSTEM-USER prompt · 2026-06-17 19:09:35 UTC

```
<validation-feedback>
Attempt 1 failed validation.

You have not created the output file `.terminal_claude_agent_struct_out.json` yet. Use the Write tool to create it.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```

### [42] SYSTEM-USER prompt · 2026-06-17 19:09:43 UTC

```
continue
```

### [43] SYSTEM-USER prompt · 2026-06-17 19:12:11 UTC

```
continue
```
