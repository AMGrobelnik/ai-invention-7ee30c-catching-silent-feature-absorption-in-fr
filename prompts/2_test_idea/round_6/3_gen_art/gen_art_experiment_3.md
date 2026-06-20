# gen_art_experiment_3 — test_idea

> Phase: `invention_loop` · round 6 · `gen_art`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_experiment_3` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 05:16:00 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_experiment_3`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_experiment_3/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_experiment_3/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_experiment_3/results/out.json`
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
id: gen_plan_experiment_3_idx4
type: experiment
title: >-
  M4 — Expand the Recall-Hole Router Prospective Set on the Homograph Entity Testbed (validate-or-demote) + Count Absorption
  Breadth (M7)
summary: >-
  Reuse the iter-5 a-priori SAE firing-structure router VERBATIM and apply the FROZEN recall-hole-alone rule (absorption iff
  parent recall-hole > tau_h_alone=0.7795, derived ONLY on the 12 frozen derivation concepts) to a much larger truly-prospective
  set built from the homograph/polysemy entity testbed (art_2xQn686KUmV5: ~93 entities across 4 is-a hierarchies — cities/months/given-names/brands).
  For each eligible entity (>=150 diagnostic-fold positives) PREDICT the regime with the frozen rule, log it BEFORE measuring
  the per-entity outcome (label-free CCRG unit vs (a) best raw latent / (h) attribution pool / (d) non-SAE probe at matched
  pool size), then score hit = (predicted == sign(auc_unit-auc_a)). Report prospective hit-rate STRATIFIED by predicted regime
  with Wilson 95% CIs and a clear ROUTER_VALIDATED (CI excludes 0.5) / ROUTER_DEMOTED (CI includes 0.5) verdict. Simultaneously
  answer the 'absorption is narrow, n=1-2' weakness with a SYSTEMATIC breadth count (M7): how many of the ~93 entities are
  absorption-structured (recall-hole>0.5 AND firing-Jaccard<0.1), naming any NEW suppressed-parent homograph beyond Georgia/Jordan.
  Frozen Gemma-Scope L12/16k JumpReLU SAE over unsloth/gemma-2-2b, $0 LLM (router itself), single GPU, SEED=1234. Emit method_out.json
  in exp_gen_sol_out schema.
runpod_compute_profile: gpu
implementation_pseudocode: |
  # =====================================================================================
  # GOAL (two coupled deliverables, both from ONE forward-pass router run):
  #   M4: a Wilson CI on the PROSPECTIVE absorption hit-rate that EXCLUDES 0.5 (ROUTER_VALIDATED)
  #       or, failing that, an honest ROUTER_DEMOTED verdict, computed on a MUCH larger prospective
  #       set than the iter-5 6-concept absorption set (which gave Wilson [0.19,0.81]).
  #   M7: a systematic absorption-BREADTH count over ~93 homograph entities + identities of any
  #       NEW suppressed-parent homograph beyond Georgia/Jordan.
  # STRATEGY: do NOT reinvent the router. Copy iter-5 method.py VERBATIM as core.py and reuse every
  # function; add only (i) a homograph-hierarchy loader, (ii) a per-entity concept runner, (iii) the
  # prospective aggregation + breadth count + verdict in main(). Keep derivation FROZEN & separate.
  # =====================================================================================

  # ------------------------------------------------------------------ 0. SETUP / REUSE
  # Source of truth to copy VERBATIM (read it first):
  #   ITER5_EXP = run-tree .../3_invention_loop/iter_5/gen_art/gen_art_experiment_3/method.py  (2107 lines)
  # Copy it to ./core.py UNCHANGED. It already contains, all reusable as-is:
  #   - JumpReLUSAE, load_sae (google/gemma-scope-2b-pt-res, layer_12/width_16k/average_l0_82/params.npz)
  #   - Encoder (model unsloth/gemma-2-2b, hook layer 12 == blocks.12.hook_resid_post, firing=encode>0,
  #     SHARED-GPU acquire/forward retry loops, encode_token / encode_sentence, gating_check)
  #   - identify_parent (content-responsive latents + firing-floor parent validation PARENT_FIRE_FLOOR=0.20),
  #     per_subcontext (per-sub recall_hole + firing-Jaccard(detector,parent) + bootstrap CI),
  #     ktrack_lite_unit (label-free CCRG K-track-lite: parent anchor + firing-disjoint hole-covering
  #       absorbers; PREC_FLOOR=0.70, JACCARD_MAX=0.10, COVGAIN_FLOOR=0.05, K_MAX=8),
  #     attribution_pool_h (baseline h), best_latent_a (a), nonsae_probe_score (d),
  #     _outcome_core (label-free unit vs a/h/d at matched pool size, held-out LR head, paired-bootstrap delta CI),
  #     wilson_ci, boot_ci, paired_bootstrap_auc_delta, cols_auc, derive_single, derive_combined,
  #     predict_recall_hole_alone, predict_combined, predict_jaccard_alone, loo_*, balanced_accuracy,
  #     build_spelling / build_nonspell / build_toxicity / build_support_* / build_spelling_prospective,
  #     run_concept, run_toxicity_concepts, run_severe_toxicity, assemble_and_save, _sanitize, _json_default.
  # CONSTANTS to keep identical: SEED=1234, MIN_SUB_SENT=150, MIN_OUTCOME=120, PREC_FLOOR=0.70,
  #   JACCARD_MAX=0.10, PARENT_FIRE_FLOOR=0.20, B_BOOT(>=2000), B_JAC=2000, N_SHUFFLE=1000.
  # Write a thin method.py that imports from core.py and adds the homograph extension + new main().
  # Use aii-use-hardware to detect GPU/RAM; aii-parallel-computing for batched encoding; aii-python style.

  # ------------------------------------------------------------------ 1. LOCATE / (RE)BUILD HOMOGRAPH DATA
  # Dependency art_2xQn686KUmV5 = 4-hierarchy homograph testbed. Its data files live at
  #   HG_DIR = .../iter_5/gen_art/gen_art_dataset_1/   (full_data_out.json + manifest.json)
  # IMPORTANT: those *_data_out.json + manifest.json may NOT be present on disk in the source dir
  # (only data.py / pipeline.py / schema.json were confirmed). Therefore:
  full = find_file([HG_DIR/'full_data_out.json', staged_dependency_dir/'full_data_out.json'])
  if full is None:
      # deterministic rebuild (seed 20240617, pinned pile rev 3be90335...). $0-<$1 (gpt-4o-mini via
      # OpenRouter, well under the $10 cap). For a guaranteed $0 build use --no-llm (templated backbone
      # + real pile corpus) — the corpus windows (component C) are what the recall-hole needs, and the
      # content-flip pairs (component A) the parent ID needs; templates suffice for both.
      run('cd HG_DIR && python3 data.py --scale full [--no-llm]')   # writes full_data_out.json + manifest.json
      full = HG_DIR/'full_data_out.json'
  manifest = json.load(HG_DIR/'manifest.json')   # absorption_readiness per (hierarchy,entity), eligible_entities_per_hierarchy
  # The 4 datasets inside full_data_out.json (one per hierarchy):
  HIERARCHIES = {'city':'city_homograph_absorption', 'month':'month_name_absorption',
                 'given_name':'given_name_absorption', 'brand':'brand_homograph_absorption'}
  # Row schema (structural drop-in of dataset_2 / build_nonspell), FLAT metadata_* keys:
  #   content pairs: metadata_row_type=='content_pair', metadata_pair_id, metadata_pair_role in {x_on,x_off},
  #                  input, metadata_target_char_start/end, metadata_target_token_indices, metadata_fold
  #   corpus rows:   metadata_row_type=='corpus', metadata_concept_present(bool), metadata_sub_context,
  #                  metadata_entity, metadata_hierarchy, metadata_target_sense (city|month|...|competitor|null),
  #                  metadata_neg_family (homograph_competitor|other_place|other_time|...|easy),
  #                  metadata_target_char_start/end, metadata_target_token_indices, metadata_fold (train|diagnostic)
  # Also keep DATA paths for derivation deps (already wired in core.py): spelling=dataset_1(iter1),
  #   nonspell=dataset_2(iter1, taxonomic-data art_t2uUbjSwpd3t), toxicity=dataset_3, support=dataset_4.

  # ------------------------------------------------------------------ 2. DERIVATION: RE-FREEZE THE RULE
  # Re-run the 12 DERIVATION concepts EXACTLY as iter-5 (NEVER counted as prospective):
  #   spelling_{L,O,T,I,D}, numeric, taxonomic, toxicity_{threat,identity_attack,insult,obscene,sexual_explicit}
  derivation = [run_concept(build_*( ... ), rng) for each derivation concept]   # core.py verbatim
  frozen_combined = derive_combined(derivation)
  th_alone, bacc_h, _ = derive_single(derivation, 'recall_hole_max', lt=False, grid=TAU_H_GRID)  # PRIMARY
  tj_alone, bacc_j, _ = derive_single(derivation, 'jaccard_median', lt=True,  grid=TAU_J_GRID)   # corroborating
  FROZEN = dict(tau_h_alone=th_alone, tau_j=frozen_combined['tau_j'], tau_h=frozen_combined['tau_h'], tau_j_alone=tj_alone)
  # EXPECT reproduction (report actuals; do NOT hard-fail on tiny drift): tau_h_alone~=0.7795, derivation
  # balanced_acc 1.0, LOO~=0.833 (iter-5 values). Log them. If materially different, flag in honest_notes.
  # Also re-run the 7 internal prospective spelling letters {B,C,F,M,P,R,W} via build_spelling_prospective
  # (cheap, $0): they supply guaranteed ABSORPTION-regime prospective members AND the verbatim honest
  # counterexample that recall-hole=1.0 OVER-predicts absorption on new letters F/M/W (false-absorption misses).

  # ------------------------------------------------------------------ 3. HOMOGRAPH LOADER (adapt build_nonspell)
  def build_homograph(hier_key, enc, scale):
      g = dataset(full, HIERARCHIES[hier_key])['examples']
      # (A) content-flip pairs -> identify the ONE broad hierarchy parent (is-a-city / is-a-month / ...)
      pairs = group by metadata_pair_id where metadata_row_type=='content_pair'; keep {x_on,x_off}
      on_lat,on_res = enc.encode_token(x_on inputs, (char_start,char_end), token_idx_lists, want_resid=True)
      off_lat,off_res = enc.encode_token(x_off inputs, ...)
      # (C) corpus: positives = concept_present True AND target_sense==hier parent sense (NOT 'competitor');
      #     negatives = concept_present False (homograph_competitor + other_* + easy families).
      corpus_pos = [r for r in g if r.row_type=='corpus' and r.concept_present]
      corpus_neg = [r for r in g if r.row_type=='corpus' and not r.concept_present]
      # ENCODE THE CORPUS ONCE PER HIERARCHY (do NOT re-encode per entity) — cap per entity to bound size
      #   cap_pos_per_entity = {smoke:20, mini:60, full:300}; cap_neg = {smoke:60, mini:600, full:4000}
      pos_lat = enc.encode_token(kept corpus_pos inputs, spans, token_idx_lists, check_ids=token_ids)
      neg_lat = enc.encode_token(corpus_neg[:cap_neg] inputs, spans, token_idx_lists)
      pos_entity = np.array([r.metadata_entity for r in kept])
      pos_sense  = np.array([r.metadata_target_sense for r in kept])
      pos_fold   = np.array([r.metadata_fold for r in kept])   # 'train' | 'diagnostic'
      return dict(hier=hier_key, on_lat, off_lat, on_res, off_res, pos_lat, pos_entity, pos_sense,
                  pos_fold, neg_lat, neg_res)

  # ------------------------------------------------------------------ 4. PER-ENTITY ROUTER (predict-then-measure)
  # For each hierarchy: identify the broad parent ONCE on (content pairs + ALL corpus positives).
  for hier_key in HIERARCHIES:
      H = build_homograph(hier_key, enc, scale)
      parent, resp, precision, pos_fire_rate, null95, pinfo = identify_parent(H.on_lat, H.off_lat, H.pos_lat, rng)
      # parent must clear PARENT_FIRE_FLOOR; if unresolved -> log parent_unresolved, entities default co_firing.
      entities = sorted(set(H.pos_entity))
      for E in entities:
          mE = (H.pos_entity == E)
          nE_diag = count(mE & (H.pos_fold=='diagnostic'))   # eligibility uses DIAGNOSTIC-fold positives
          nE_all  = count(mE)
          # ---- firing structure for E (reuse per_subcontext math) ----
          parent_recall_E = mean( (H.pos_lat[mE][:,parent] > 0) )
          recall_hole_E   = 1 - parent_recall_E
          detector_E      = argmax_AUC over eligible non-parent latents: E-pos vs H.neg_lat
          jaccard_E       = firing_jaccard(parent fires, detector_E fires) over ALL hierarchy positives  # matches per_subcontext
          eligible = (nE_diag >= MIN_SUB_SENT)       # >=150 diagnostic-fold positives -> inferential
          # ---- PREDICT with FROZEN rule, LOG BEFORE measuring outcome (audit trail) ----
          predicted_regime          = predict_recall_hole_alone({recall_hole_max:recall_hole_E}, th_alone)  # PRIMARY
          predicted_regime_combined = predict_combined({jaccard_median:jaccard_E, recall_hole_max:recall_hole_E}, FROZEN.tau_j, FROZEN.tau_h)
          predicted_regime_jaccard  = predict_jaccard_alone({jaccard_median:jaccard_E}, tj_alone)
          log(f'{hier}/{E}: PREDICT(recall_hole={recall_hole_E:.3f}>{th_alone:.3f})={predicted_regime}  [logged BEFORE outcome]')
          # ---- MEASURE outcome: E-positives vs hierarchy negatives, held-out (fold: diagnostic=test, train=train) ----
          Cs = dict(parent=parent, resp=resp, precision=precision,
                    star_pos_lat=H.pos_lat[mE], star_pos_fold=(fold=='diagnostic'?1:0)[mE], star_pos_resid=H.pos_res[mE],
                    star_neg_lat=H.neg_lat, star_neg_fold=neg_fold01, star_neg_resid=H.neg_res, pos_lat=H.pos_lat[mE])
          out = _outcome_core(parent, resp, precision, full_pos_lat=H.pos_lat[mE],
                              pos_lat=H.pos_lat[mE], pos_fold=..., neg_lat=H.neg_lat, neg_fold=...,
                              res_pos=H.pos_res[mE], res_neg=H.neg_res, s_name=f'{hier}_{E}', rng)
          # out has auc_unit, auc_a, auc_h, auc_d, delta(vs a)+ci, delta_vs_h+ci, k, unit_members
          ground_truth_regime = 'absorption' if out.delta>0 else 'co_firing'   # PRIMARY = sign(auc_unit-auc_a)
          ground_truth_regime_vs_h = 'absorption' if out.delta_vs_h>0 else 'co_firing'
          hit_vs_a          = (predicted_regime == ground_truth_regime)
          hit_vs_a_combined = (predicted_regime_combined == ground_truth_regime)
          is_prospective_hit = hit_vs_a
          # absorption-STRUCTURED flag for M7 breadth (separate from the 0.7795 prediction threshold):
          absorption_structured = (recall_hole_E > 0.5) and (jaccard_E < 0.1)
          record entity row {hierarchy, entity, n_diag, n_all, eligible, parent_latent, parent_unresolved,
                             recall_hole_E, jaccard_E, predicted_regime(+combined/+jaccard),
                             auc_unit, auc_a, auc_h, auc_d, delta_vs_a(+ci), delta_vs_h(+ci), k, unit_members,
                             ground_truth_regime(+vs_h), hit_vs_a(+combined), is_prospective_hit,
                             absorption_structured, power_flag=('inferential' if eligible else 'descriptive_only')}

  # ------------------------------------------------------------------ 5. M4 AGGREGATION + VERDICT (Wilson CIs)
  entity_inf = [e for e in entity_rows if e.eligible]            # inferential prospective entities
  # Stratify by PRIMARY predicted regime (recall-hole-alone), exactly like iter-5 strat():
  abs_pred = [e for e in entity_inf if e.predicted_regime=='absorption']
  cof_pred = [e for e in entity_inf if e.predicted_regime=='co_firing']
  wilson_abs = wilson_ci(sum(e.hit_vs_a for e in abs_pred), len(abs_pred))
  wilson_cof = wilson_ci(sum(e.hit_vs_a for e in cof_pred), len(cof_pred))
  wilson_all = wilson_ci(sum(e.hit_vs_a for e in entity_inf), len(entity_inf))
  # ALSO report a COMBINED-WITH-ITER5-SPELLING stratum (homograph entities + the 7 internal spelling
  # letters) so the absorption-predicted arm has maximal n -> the best chance to exclude 0.5:
  abs_pred_plus = abs_pred + [spelling letters with predicted_regime=='absorption']
  wilson_abs_plus = wilson_ci(hits, n)
  # VERDICT (per objective): the router is validated iff a prospective Wilson CI EXCLUDES 0.5.
  # Use the absorption-predicted stratum (the discriminative test) as primary; report all three.
  def excludes_half(ci): return ci.wilson_ci[0] > 0.5 or ci.wilson_ci[1] < 0.5
  router_verdict = ('ROUTER_VALIDATED' if (excludes_half(wilson_abs) or excludes_half(wilson_abs_plus))
                    else 'ROUTER_DEMOTED')   # DEMOTED => 'exploratory diagnostic, not a validated a-priori predictor'

  # ------------------------------------------------------------------ 6. M7 ABSORPTION BREADTH COUNT
  # Over ALL entities with a stable recall-hole estimate (n_all >= MIN_SUB_TOKEN-style floor, e.g. >=30,
  # NOT just the >=150 eligible — breadth is a phenomenon count, report both the >=30 and >=150 tallies):
  breadth = {
    'n_entities_total': len(entity_rows),
    'n_entities_with_stable_estimate': count(n_all>=30),
    'n_absorption_structured': count(absorption_structured & n_all>=30),   # recall_hole>0.5 AND jaccard<0.1
    'absorption_structured_entities': [ (hier,E,recall_hole,jaccard) sorted by recall_hole desc ],
    'per_hierarchy': { hier: {n_entities, n_absorption_structured, examples} },
    'new_suppressed_parent_homographs': [ entities that are absorption_structured (beyond Georgia/Jordan,
        which live in the taxonomic derivation set, not here) — these are the NEW cases the paper can name ],
  }
  # This DIRECTLY quantifies 'how narrow is absorption' across 93 homograph entities and surfaces new cases.

  # ------------------------------------------------------------------ 7. HONEST NOTES (keep verbatim)
  honest = [
    'recall-hole=1.0 OVER-predicts absorption on new spelling letters F/M/W (false-absorption misses) — re-confirmed here.',
    'numeric: HIGH firing-Jaccard yet ABSORPTION (jaccard-alone mislabels; recall-hole gate fixes it).',
    'aggregated-taxonomic: LOW firing-Jaccard yet CO-FIRING (parent already fires; no holes).',
    'derivation (12 concepts) is FROZEN and NEVER counted prospective; tau fit ONLY on derivation.',
    'every entity prediction LOGGED before its outcome was measured (predict-then-measure integrity).',
    'ground-truth regime PRIMARY = sign(auc_unit-auc_a); the label-free unit is built on the parent holes,
     so a hit means grouping helps exactly where the recall-hole rule said it would.',
    'parent_unresolved hierarchies default to co_firing (boundary handling, not a method failure).',
    router_verdict-specific sentence (validated: CI excludes 0.5; demoted: CI still includes 0.5 ->
     exploratory diagnostic only),
    + any prospective MISS rows + reproduction drift notes.
  ]

  # ------------------------------------------------------------------ 8. EMIT method_out.json (exp_gen_sol_out)
  # metadata: method_name, sae_release/sae_id/hook/model/seed/scale/accelerator, gating, FROZEN rule
  #   (tau_h_alone, balanced_acc, loo), derivation reproduction block (tau actuals vs iter-5 0.7795/1.0/0.833),
  #   derivation_concepts list, prospective_entities list, prospective_spelling list,
  #   prospective_hitrate_primary={absorption_predicted:wilson_abs, cofiring_predicted:wilson_cof, combined_all:wilson_all},
  #   prospective_hitrate_combined_with_spelling={absorption_predicted:wilson_abs_plus, ...},
  #   prospective_hitrate_ablation_combined / _jaccard (same strat under ablation rules),
  #   router_verdict ('ROUTER_VALIDATED'|'ROUTER_DEMOTED') + a one-line rationale,
  #   absorption_breadth (the M7 block), counterexamples, honest_notes,
  #   entity_table (every entity row), spelling_prospective_table, n_* counts.
  # datasets: [{ 'dataset':'m4_router_prospective_concepts', 'examples':[ one CARD per derivation concept,
  #   per spelling-prospective letter, AND per homograph entity ]}], each card mirroring iter-5's exp_gen_sol_out
  #   card (input=human-readable router decision string; output=ground_truth_regime; predict_router=predicted_regime;
  #   metadata_* = all numeric fields incl metadata_is_prospective_hit, metadata_hierarchy, metadata_entity,
  #   metadata_recall_hole, metadata_jaccard, metadata_absorption_structured, metadata_power_flag).
  write _sanitize(out) with json.dumps(..., allow_nan=False)   # NaN/Inf -> None (strict JSON)
  # Then: aii-json -> emit full/mini/preview_method_out.json and VALIDATE against format 'exp_gen_sol_out'.
  # Confirm each variant < 100MB (entity cards are small; ~150 cards => well under). cache/ excluded from upload.
fallback_plan: "DATA MISSING / REBUILD: If full_data_out.json (+ manifest.json) for the homograph testbed is not on disk,\
  \ rebuild deterministically with `cd <HG_DIR> && python3 data.py --scale full` (seed 20240617, pinned pile rev; LLM spend\
  \ <$1 via OpenRouter gpt-4o-mini, within the $10 cap). If no OpenRouter key / to guarantee $0, use `python3 data.py --scale\
  \ full --no-llm` (templated content-flip backbone + real pile corpus — both components the router needs are produced without\
  \ LLM). If data.py errors, fall back to the iter-1 taxonomic-data dep (art_t2uUbjSwpd3t, dataset_2, known-present full_data_out.json)\
  \ and run the SAME per-entity router over its 20 eligible countries (this still expands the prospective set well beyond\
  \ 6 and exercises the identical code path; report it as the homograph-unavailable fallback). \nVERDICT IS NEGATIVE (CI still\
  \ includes 0.5): This is an ACCEPTABLE, publishable outcome — emit router_verdict='ROUTER_DEMOTED' and the honest 'exploratory\
  \ diagnostic, not a validated a-priori predictor' framing. Do NOT p-hack: keep derivation/prospective strictly separated\
  \ and the predict-then-measure log intact. \nTOO FEW ELIGIBLE ENTITIES (manifest eligible_entities_per_hierarchy small):\
  \ widen the inferential floor to the largest entities available and report n; ALSO report the n_all>=30 'descriptive' stratum\
  \ so breadth (M7) is still answered even if M4's CI stays wide; combine homograph absorption-predicted entities WITH the\
  \ 7 internal spelling letters to maximize the absorption-predicted arm's n. \nPARENT UNRESOLVED for a hierarchy (no responsive\
  \ latent clears the 20% firing floor): log parent_unresolved, default its entities to co_firing, exclude from absorption-structured\
  \ count, note it — do not crash. \nGPU OOM / shared-GPU contention: the copied Encoder already retries acquire/forward;\
  \ additionally cut cap_pos_per_entity (300->150) and cap_neg (4000->2000), or run `--scale mini` for the homograph arm while\
  \ keeping full derivation. Encode each hierarchy's corpus ONCE and slice per entity (never re-encode per entity) to stay\
  \ within wall-clock. \nDERIVATION DOES NOT REPRODUCE tau_h~0.7795 / balanced_acc 1.0: report the ACTUAL frozen values, freeze\
  \ on them anyway (the rule is whatever derivation yields), and flag the drift in honest_notes — do not hard-fail. \nTORCH/CUDA\
  \ INSTALL: if torch wheel resolution fails, install with the cu124 index workaround (`uv pip install ... --index-strategy\
  \ unsafe-best-match`) per prior-iter GOTCHA; reuse the iter-5 pyproject.toml/.venv pins. SAE + model are public non-gated\
  \ mirrors (google/gemma-scope-2b-pt-res, unsloth/gemma-2-2b); set HF_HUB_DISABLE_PROGRESS_BARS=1; only set HF_HUB_OFFLINE=1\
  \ AFTER a successful first download."
testing_plan: "STAGE 1 — SMOKE (`python method.py --smoke`, minutes, no full data): load model+SAE; assert gating recon_cos_mean>0.80\
  \ (iter-5 got 0.927) and the BOS/offset token-id self-check passes on a few real corpus windows; build ONE homograph hierarchy\
  \ (e.g. city) and run 2-3 entities end-to-end; assert: parent identified (or cleanly parent_unresolved), recall_hole_E and\
  \ jaccard_E computed, predicted_regime LOGGED before the outcome line, _outcome_core returns finite auc_unit/auc_a/delta,\
  \ a Wilson CI object is produced, and a tiny exp_gen_sol_out validates via aii-json. CONFIRM the data path resolves (or\
  \ the rebuild ran). \nSTAGE 2 — MINI (`--scale mini`): run full derivation (12 concepts) + a 1-2-entity-per-hierarchy subset\
  \ + the 7 spelling letters. CONFIRMATION SIGNALS that the pipeline is correct: (a) derivation reproduces recall-hole-alone\
  \ tau_h ~0.78 with balanced_acc 1.0 and LOO ~0.83 (matches iter-5 — strongest single-run integrity check); (b) spelling\
  \ letters F/M/W reproduce recall_hole=1.0 (the documented over-prediction counterexample); (c) at least some homograph entities\
  \ show recall_hole>0.5 with low jaccard (absorption-structured) — Phoenix/Mobile/Reading/Apple/Amazon are prime candidates;\
  \ if NONE do, that is a real (publishable) breadth-narrow signal, not a bug, but double-check the corpus positive filter\
  \ (target_sense==parent sense, not 'competitor'). (d) predict-then-measure ordering visible in the log for every prospective\
  \ entity. \nSTAGE 3 — FULL (`--scale full`): all 4 hierarchies, all eligible entities. Validate: prospective_hitrate_primary\
  \ strata + Wilson CIs present; router_verdict set by the excludes-0.5 rule; absorption_breadth count + named new cases present;\
  \ derivation_concepts and prospective_entities disjoint; honest_notes carry the three verbatim counterexamples; method_out.json\
  \ + full/mini/preview validate against exp_gen_sol_out and each < 100MB; cache/ excluded from upload. Sanity cross-check:\
  \ number of absorption-PREDICTED entities (recall_hole>0.7795) <= number absorption-STRUCTURED (recall_hole>0.5) — the 0.7795\
  \ gate is stricter than the 0.5 breadth flag. Track cumulative OpenRouter spend (router itself is $0; only a data rebuild\
  \ can incur cost) and stop well under $10."
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

### [2] HUMAN-USER prompt · 2026-06-18 05:16:00 UTC

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

### [3] SKILL-INPUT — aii-python · 2026-06-18 05:16:36 UTC

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

### [4] SKILL-INPUT — aii-long-running-tasks · 2026-06-18 05:16:36 UTC

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

### [5] SKILL-INPUT — aii-use-hardware · 2026-06-18 05:16:36 UTC

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

### [6] SKILL-INPUT — aii-json · 2026-06-18 05:16:42 UTC

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

### [7] SKILL-INPUT — aii-file-size-limit · 2026-06-18 05:16:42 UTC

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

### [8] SKILL-INPUT — aii-parallel-computing · 2026-06-18 05:16:42 UTC

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

### [9] SYSTEM-USER prompt · 2026-06-18 06:22:08 UTC

```
continue
```

### [10] SYSTEM-USER prompt · 2026-06-18 06:59:21 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_experiment_3`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_experiment_3/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_experiment_3/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_experiment_3/results/out.json`
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
id: gen_plan_experiment_3_idx4
type: experiment
title: >-
  M4 — Expand the Recall-Hole Router Prospective Set on the Homograph Entity Testbed (validate-or-demote) + Count Absorption
  Breadth (M7)
summary: >-
  Reuse the iter-5 a-priori SAE firing-structure router VERBATIM and apply the FROZEN recall-hole-alone rule (absorption iff
  parent recall-hole > tau_h_alone=0.7795, derived ONLY on the 12 frozen derivation concepts) to a much larger truly-prospective
  set built from the homograph/polysemy entity testbed (art_2xQn686KUmV5: ~93 entities across 4 is-a hierarchies — cities/months/given-names/brands).
  For each eligible entity (>=150 diagnostic-fold positives) PREDICT the regime with the frozen rule, log it BEFORE measuring
  the per-entity outcome (label-free CCRG unit vs (a) best raw latent / (h) attribution pool / (d) non-SAE probe at matched
  pool size), then score hit = (predicted == sign(auc_unit-auc_a)). Report prospective hit-rate STRATIFIED by predicted regime
  with Wilson 95% CIs and a clear ROUTER_VALIDATED (CI excludes 0.5) / ROUTER_DEMOTED (CI includes 0.5) verdict. Simultaneously
  answer the 'absorption is narrow, n=1-2' weakness with a SYSTEMATIC breadth count (M7): how many of the ~93 entities are
  absorption-structured (recall-hole>0.5 AND firing-Jaccard<0.1), naming any NEW suppressed-parent homograph beyond Georgia/Jordan.
  Frozen Gemma-Scope L12/16k JumpReLU SAE over unsloth/gemma-2-2b, $0 LLM (router itself), single GPU, SEED=1234. Emit method_out.json
  in exp_gen_sol_out schema.
runpod_compute_profile: gpu
implementation_pseudocode: |
  # =====================================================================================
  # GOAL (two coupled deliverables, both from ONE forward-pass router run):
  #   M4: a Wilson CI on the PROSPECTIVE absorption hit-rate that EXCLUDES 0.5 (ROUTER_VALIDATED)
  #       or, failing that, an honest ROUTER_DEMOTED verdict, computed on a MUCH larger prospective
  #       set than the iter-5 6-concept absorption set (which gave Wilson [0.19,0.81]).
  #   M7: a systematic absorption-BREADTH count over ~93 homograph entities + identities of any
  #       NEW suppressed-parent homograph beyond Georgia/Jordan.
  # STRATEGY: do NOT reinvent the router. Copy iter-5 method.py VERBATIM as core.py and reuse every
  # function; add only (i) a homograph-hierarchy loader, (ii) a per-entity concept runner, (iii) the
  # prospective aggregation + breadth count + verdict in main(). Keep derivation FROZEN & separate.
  # =====================================================================================

  # ------------------------------------------------------------------ 0. SETUP / REUSE
  # Source of truth to copy VERBATIM (read it first):
  #   ITER5_EXP = run-tree .../3_invention_loop/iter_5/gen_art/gen_art_experiment_3/method.py  (2107 lines)
  # Copy it to ./core.py UNCHANGED. It already contains, all reusable as-is:
  #   - JumpReLUSAE, load_sae (google/gemma-scope-2b-pt-res, layer_12/width_16k/average_l0_82/params.npz)
  #   - Encoder (model unsloth/gemma-2-2b, hook layer 12 == blocks.12.hook_resid_post, firing=encode>0,
  #     SHARED-GPU acquire/forward retry loops, encode_token / encode_sentence, gating_check)
  #   - identify_parent (content-responsive latents + firing-floor parent validation PARENT_FIRE_FLOOR=0.20),
  #     per_subcontext (per-sub recall_hole + firing-Jaccard(detector,parent) + bootstrap CI),
  #     ktrack_lite_unit (label-free CCRG K-track-lite: parent anchor + firing-disjoint hole-covering
  #       absorbers; PREC_FLOOR=0.70, JACCARD_MAX=0.10, COVGAIN_FLOOR=0.05, K_MAX=8),
  #     attribution_pool_h (baseline h), best_latent_a (a), nonsae_probe_score (d),
  #     _outcome_core (label-free unit vs a/h/d at matched pool size, held-out LR head, paired-bootstrap delta CI),
  #     wilson_ci, boot_ci, paired_bootstrap_auc_delta, cols_auc, derive_single, derive_combined,
  #     predict_recall_hole_alone, predict_combined, predict_jaccard_alone, loo_*, balanced_accuracy,
  #     build_spelling / build_nonspell / build_toxicity / build_support_* / build_spelling_prospective,
  #     run_concept, run_toxicity_concepts, run_severe_toxicity, assemble_and_save, _sanitize, _json_default.
  # CONSTANTS to keep identical: SEED=1234, MIN_SUB_SENT=150, MIN_OUTCOME=120, PREC_FLOOR=0.70,
  #   JACCARD_MAX=0.10, PARENT_FIRE_FLOOR=0.20, B_BOOT(>=2000), B_JAC=2000, N_SHUFFLE=1000.
  # Write a thin method.py that imports from core.py and adds the homograph extension + new main().
  # Use aii-use-hardware to detect GPU/RAM; aii-parallel-computing for batched encoding; aii-python style.

  # ------------------------------------------------------------------ 1. LOCATE / (RE)BUILD HOMOGRAPH DATA
  # Dependency art_2xQn686KUmV5 = 4-hierarchy homograph testbed. Its data files live at
  #   HG_DIR = .../iter_5/gen_art/gen_art_dataset_1/   (full_data_out.json + manifest.json)
  # IMPORTANT: those *_data_out.json + manifest.json may NOT be present on disk in the source dir
  # (only data.py / pipeline.py / schema.json were confirmed). Therefore:
  full = find_file([HG_DIR/'full_data_out.json', staged_dependency_dir/'full_data_out.json'])
  if full is None:
      # deterministic rebuild (seed 20240617, pinned pile rev 3be90335...). $0-<$1 (gpt-4o-mini via
      # OpenRouter, well under the $10 cap). For a guaranteed $0 build use --no-llm (templated backbone
      # + real pile corpus) — the corpus windows (component C) are what the recall-hole needs, and the
      # content-flip pairs (component A) the parent ID needs; templates suffice for both.
      run('cd HG_DIR && python3 data.py --scale full [--no-llm]')   # writes full_data_out.json + manifest.json
      full = HG_DIR/'full_data_out.json'
  manifest = json.load(HG_DIR/'manifest.json')   # absorption_readiness per (hierarchy,entity), eligible_entities_per_hierarchy
  # The 4 datasets inside full_data_out.json (one per hierarchy):
  HIERARCHIES = {'city':'city_homograph_absorption', 'month':'month_name_absorption',
                 'given_name':'given_name_absorption', 'brand':'brand_homograph_absorption'}
  # Row schema (structural drop-in of dataset_2 / build_nonspell), FLAT metadata_* keys:
  #   content pairs: metadata_row_type=='content_pair', metadata_pair_id, metadata_pair_role in {x_on,x_off},
  #                  input, metadata_target_char_start/end, metadata_target_token_indices, metadata_fold
  #   corpus rows:   metadata_row_type=='corpus', metadata_concept_present(bool), metadata_sub_context,
  #                  metadata_entity, metadata_hierarchy, metadata_target_sense (city|month|...|competitor|null),
  #                  metadata_neg_family (homograph_competitor|other_place|other_time|...|easy),
  #                  metadata_target_char_start/end, metadata_target_token_indices, metadata_fold (train|diagnostic)
  # Also keep DATA paths for derivation deps (already wired in core.py): spelling=dataset_1(iter1),
  #   nonspell=dataset_2(iter1, taxonomic-data art_t2uUbjSwpd3t), toxicity=dataset_3, support=dataset_4.

  # ------------------------------------------------------------------ 2. DERIVATION: RE-FREEZE THE RULE
  # Re-run the 12 DERIVATION concepts EXACTLY as iter-5 (NEVER counted as prospective):
  #   spelling_{L,O,T,I,D}, numeric, taxonomic, toxicity_{threat,identity_attack,insult,obscene,sexual_explicit}
  derivation = [run_concept(build_*( ... ), rng) for each derivation concept]   # core.py verbatim
  frozen_combined = derive_combined(derivation)
  th_alone, bacc_h, _ = derive_single(derivation, 'recall_hole_max', lt=False, grid=TAU_H_GRID)  # PRIMARY
  tj_alone, bacc_j, _ = derive_single(derivation, 'jaccard_median', lt=True,  grid=TAU_J_GRID)   # corroborating
  FROZEN = dict(tau_h_alone=th_alone, tau_j=frozen_combined['tau_j'], tau_h=frozen_combined['tau_h'], tau_j_alone=tj_alone)
  # EXPECT reproduction (report actuals; do NOT hard-fail on tiny drift): tau_h_alone~=0.7795, derivation
  # balanced_acc 1.0, LOO~=0.833 (iter-5 values). Log them. If materially different, flag in honest_notes.
  # Also re-run the 7 internal prospective spelling letters {B,C,F,M,P,R,W} via build_spelling_prospective
  # (cheap, $0): they supply guaranteed ABSORPTION-regime prospective members AND the verbatim honest
  # counterexample that recall-hole=1.0 OVER-predicts absorption on new letters F/M/W (false-absorption misses).

  # ------------------------------------------------------------------ 3. HOMOGRAPH LOADER (adapt build_nonspell)
  def build_homograph(hier_key, enc, scale):
      g = dataset(full, HIERARCHIES[hier_key])['examples']
      # (A) content-flip pairs -> identify the ONE broad hierarchy parent (is-a-city / is-a-month / ...)
      pairs = group by metadata_pair_id where metadata_row_type=='content_pair'; keep {x_on,x_off}
      on_lat,on_res = enc.encode_token(x_on inputs, (char_start,char_end), token_idx_lists, want_resid=True)
      off_lat,off_res = enc.encode_token(x_off inputs, ...)
      # (C) corpus: positives = concept_present True AND target_sense==hier parent sense (NOT 'competitor');
      #     negatives = concept_present False (homograph_competitor + other_* + easy families).
      corpus_pos = [r for r in g if r.row_type=='corpus' and r.concept_present]
      corpus_neg = [r for r in g if r.row_type=='corpus' and not r.concept_present]
      # ENCODE THE CORPUS ONCE PER HIERARCHY (do NOT re-encode per entity) — cap per entity to bound size
      #   cap_pos_per_entity = {smoke:20, mini:60, full:300}; cap_neg = {smoke:60, mini:600, full:4000}
      pos_lat = enc.encode_token(kept corpus_pos inputs, spans, token_idx_lists, check_ids=token_ids)
      neg_lat = enc.encode_token(corpus_neg[:cap_neg] inputs, spans, token_idx_lists)
      pos_entity = np.array([r.metadata_entity for r in kept])
      pos_sense  = np.array([r.metadata_target_sense for r in kept])
      pos_fold   = np.array([r.metadata_fold for r in kept])   # 'train' | 'diagnostic'
      return dict(hier=hier_key, on_lat, off_lat, on_res, off_res, pos_lat, pos_entity, pos_sense,
                  pos_fold, neg_lat, neg_res)

  # ------------------------------------------------------------------ 4. PER-ENTITY ROUTER (predict-then-measure)
  # For each hierarchy: identify the broad parent ONCE on (content pairs + ALL corpus positives).
  for hier_key in HIERARCHIES:
      H = build_homograph(hier_key, enc, scale)
      parent, resp, precision, pos_fire_rate, null95, pinfo = identify_parent(H.on_lat, H.off_lat, H.pos_lat, rng)
      # parent must clear PARENT_FIRE_FLOOR; if unresolved -> log parent_unresolved, entities default co_firing.
      entities = sorted(set(H.pos_entity))
      for E in entities:
          mE = (H.pos_entity == E)
          nE_diag = count(mE & (H.pos_fold=='diagnostic'))   # eligibility uses DIAGNOSTIC-fold positives
          nE_all  = count(mE)
          # ---- firing structure for E (reuse per_subcontext math) ----
          parent_recall_E = mean( (H.pos_lat[mE][:,parent] > 0) )
          recall_hole_E   = 1 - parent_recall_E
          detector_E      = argmax_AUC over eligible non-parent latents: E-pos vs H.neg_lat
          jaccard_E       = firing_jaccard(parent fires, detector_E fires) over ALL hierarchy positives  # matches per_subcontext
          eligible = (nE_diag >= MIN_SUB_SENT)       # >=150 diagnostic-fold positives -> inferential
          # ---- PREDICT with FROZEN rule, LOG BEFORE measuring outcome (audit trail) ----
          predicted_regime          = predict_recall_hole_alone({recall_hole_max:recall_hole_E}, th_alone)  # PRIMARY
          predicted_regime_combined = predict_combined({jaccard_median:jaccard_E, recall_hole_max:recall_hole_E}, FROZEN.tau_j, FROZEN.tau_h)
          predicted_regime_jaccard  = predict_jaccard_alone({jaccard_median:jaccard_E}, tj_alone)
          log(f'{hier}/{E}: PREDICT(recall_hole={recall_hole_E:.3f}>{th_alone:.3f})={predicted_regime}  [logged BEFORE outcome]')
          # ---- MEASURE outcome: E-positives vs hierarchy negatives, held-out (fold: diagnostic=test, train=train) ----
          Cs = dict(parent=parent, resp=resp, precision=precision,
                    star_pos_lat=H.pos_lat[mE], star_pos_fold=(fold=='diagnostic'?1:0)[mE], star_pos_resid=H.pos_res[mE],
                    star_neg_lat=H.neg_lat, star_neg_fold=neg_fold01, star_neg_resid=H.neg_res, pos_lat=H.pos_lat[mE])
          out = _outcome_core(parent, resp, precision, full_pos_lat=H.pos_lat[mE],
                              pos_lat=H.pos_lat[mE], pos_fold=..., neg_lat=H.neg_lat, neg_fold=...,
                              res_pos=H.pos_res[mE], res_neg=H.neg_res, s_name=f'{hier}_{E}', rng)
          # out has auc_unit, auc_a, auc_h, auc_d, delta(vs a)+ci, delta_vs_h+ci, k, unit_members
          ground_truth_regime = 'absorption' if out.delta>0 else 'co_firing'   # PRIMARY = sign(auc_unit-auc_a)
          ground_truth_regime_vs_h = 'absorption' if out.delta_vs_h>0 else 'co_firing'
          hit_vs_a          = (predicted_regime == ground_truth_regime)
          hit_vs_a_combined = (predicted_regime_combined == ground_truth_regime)
          is_prospective_hit = hit_vs_a
          # absorption-STRUCTURED flag for M7 breadth (separate from the 0.7795 prediction threshold):
          absorption_structured = (recall_hole_E > 0.5) and (jaccard_E < 0.1)
          record entity row {hierarchy, entity, n_diag, n_all, eligible, parent_latent, parent_unresolved,
                             recall_hole_E, jaccard_E, predicted_regime(+combined/+jaccard),
                             auc_unit, auc_a, auc_h, auc_d, delta_vs_a(+ci), delta_vs_h(+ci), k, unit_members,
                             ground_truth_regime(+vs_h), hit_vs_a(+combined), is_prospective_hit,
                             absorption_structured, power_flag=('inferential' if eligible else 'descriptive_only')}

  # ------------------------------------------------------------------ 5. M4 AGGREGATION + VERDICT (Wilson CIs)
  entity_inf = [e for e in entity_rows if e.eligible]            # inferential prospective entities
  # Stratify by PRIMARY predicted regime (recall-hole-alone), exactly like iter-5 strat():
  abs_pred = [e for e in entity_inf if e.predicted_regime=='absorption']
  cof_pred = [e for e in entity_inf if e.predicted_regime=='co_firing']
  wilson_abs = wilson_ci(sum(e.hit_vs_a for e in abs_pred), len(abs_pred))
  wilson_cof = wilson_ci(sum(e.hit_vs_a for e in cof_pred), len(cof_pred))
  wilson_all = wilson_ci(sum(e.hit_vs_a for e in entity_inf), len(entity_inf))
  # ALSO report a COMBINED-WITH-ITER5-SPELLING stratum (homograph entities + the 7 internal spelling
  # letters) so the absorption-predicted arm has maximal n -> the best chance to exclude 0.5:
  abs_pred_plus = abs_pred + [spelling letters with predicted_regime=='absorption']
  wilson_abs_plus = wilson_ci(hits, n)
  # VERDICT (per objective): the router is validated iff a prospective Wilson CI EXCLUDES 0.5.
  # Use the absorption-predicted stratum (the discriminative test) as primary; report all three.
  def excludes_half(ci): return ci.wilson_ci[0] > 0.5 or ci.wilson_ci[1] < 0.5
  router_verdict = ('ROUTER_VALIDATED' if (excludes_half(wilson_abs) or excludes_half(wilson_abs_plus))
                    else 'ROUTER_DEMOTED')   # DEMOTED => 'exploratory diagnostic, not a validated a-priori predictor'

  # ------------------------------------------------------------------ 6. M7 ABSORPTION BREADTH COUNT
  # Over ALL entities with a stable recall-hole estimate (n_all >= MIN_SUB_TOKEN-style floor, e.g. >=30,
  # NOT just the >=150 eligible — breadth is a phenomenon count, report both the >=30 and >=150 tallies):
  breadth = {
    'n_entities_total': len(entity_rows),
    'n_entities_with_stable_estimate': count(n_all>=30),
    'n_absorption_structured': count(absorption_structured & n_all>=30),   # recall_hole>0.5 AND jaccard<0.1
    'absorption_structured_entities': [ (hier,E,recall_hole,jaccard) sorted by recall_hole desc ],
    'per_hierarchy': { hier: {n_entities, n_absorption_structured, examples} },
    'new_suppressed_parent_homographs': [ entities that are absorption_structured (beyond Georgia/Jordan,
        which live in the taxonomic derivation set, not here) — these are the NEW cases the paper can name ],
  }
  # This DIRECTLY quantifies 'how narrow is absorption' across 93 homograph entities and surfaces new cases.

  # ------------------------------------------------------------------ 7. HONEST NOTES (keep verbatim)
  honest = [
    'recall-hole=1.0 OVER-predicts absorption on new spelling letters F/M/W (false-absorption misses) — re-confirmed here.',
    'numeric: HIGH firing-Jaccard yet ABSORPTION (jaccard-alone mislabels; recall-hole gate fixes it).',
    'aggregated-taxonomic: LOW firing-Jaccard yet CO-FIRING (parent already fires; no holes).',
    'derivation (12 concepts) is FROZEN and NEVER counted prospective; tau fit ONLY on derivation.',
    'every entity prediction LOGGED before its outcome was measured (predict-then-measure integrity).',
    'ground-truth regime PRIMARY = sign(auc_unit-auc_a); the label-free unit is built on the parent holes,
     so a hit means grouping helps exactly where the recall-hole rule said it would.',
    'parent_unresolved hierarchies default to co_firing (boundary handling, not a method failure).',
    router_verdict-specific sentence (validated: CI excludes 0.5; demoted: CI still includes 0.5 ->
     exploratory diagnostic only),
    + any prospective MISS rows + reproduction drift notes.
  ]

  # ------------------------------------------------------------------ 8. EMIT method_out.json (exp_gen_sol_out)
  # metadata: method_name, sae_release/sae_id/hook/model/seed/scale/accelerator, gating, FROZEN rule
  #   (tau_h_alone, balanced_acc, loo), derivation reproduction block (tau actuals vs iter-5 0.7795/1.0/0.833),
  #   derivation_concepts list, prospective_entities list, prospective_spelling list,
  #   prospective_hitrate_primary={absorption_predicted:wilson_abs, cofiring_predicted:wilson_cof, combined_all:wilson_all},
  #   prospective_hitrate_combined_with_spelling={absorption_predicted:wilson_abs_plus, ...},
  #   prospective_hitrate_ablation_combined / _jaccard (same strat under ablation rules),
  #   router_verdict ('ROUTER_VALIDATED'|'ROUTER_DEMOTED') + a one-line rationale,
  #   absorption_breadth (the M7 block), counterexamples, honest_notes,
  #   entity_table (every entity row), spelling_prospective_table, n_* counts.
  # datasets: [{ 'dataset':'m4_router_prospective_concepts', 'examples':[ one CARD per derivation concept,
  #   per spelling-prospective letter, AND per homograph entity ]}], each card mirroring iter-5's exp_gen_sol_out
  #   card (input=human-readable router decision string; output=ground_truth_regime; predict_router=predicted_regime;
  #   metadata_* = all numeric fields incl metadata_is_prospective_hit, metadata_hierarchy, metadata_entity,
  #   metadata_recall_hole, metadata_jaccard, metadata_absorption_structured, metadata_power_flag).
  write _sanitize(out) with json.dumps(..., allow_nan=False)   # NaN/Inf -> None (strict JSON)
  # Then: aii-json -> emit full/mini/preview_method_out.json and VALIDATE against format 'exp_gen_sol_out'.
  # Confirm each variant < 100MB (entity cards are small; ~150 cards => well under). cache/ excluded from upload.
fallback_plan: "DATA MISSING / REBUILD: If full_data_out.json (+ manifest.json) for the homograph testbed is not on disk,\
  \ rebuild deterministically with `cd <HG_DIR> && python3 data.py --scale full` (seed 20240617, pinned pile rev; LLM spend\
  \ <$1 via OpenRouter gpt-4o-mini, within the $10 cap). If no OpenRouter key / to guarantee $0, use `python3 data.py --scale\
  \ full --no-llm` (templated content-flip backbone + real pile corpus — both components the router needs are produced without\
  \ LLM). If data.py errors, fall back to the iter-1 taxonomic-data dep (art_t2uUbjSwpd3t, dataset_2, known-present full_data_out.json)\
  \ and run the SAME per-entity router over its 20 eligible countries (this still expands the prospective set well beyond\
  \ 6 and exercises the identical code path; report it as the homograph-unavailable fallback). \nVERDICT IS NEGATIVE (CI still\
  \ includes 0.5): This is an ACCEPTABLE, publishable outcome — emit router_verdict='ROUTER_DEMOTED' and the honest 'exploratory\
  \ diagnostic, not a validated a-priori predictor' framing. Do NOT p-hack: keep derivation/prospective strictly separated\
  \ and the predict-then-measure log intact. \nTOO FEW ELIGIBLE ENTITIES (manifest eligible_entities_per_hierarchy small):\
  \ widen the inferential floor to the largest entities available and report n; ALSO report the n_all>=30 'descriptive' stratum\
  \ so breadth (M7) is still answered even if M4's CI stays wide; combine homograph absorption-predicted entities WITH the\
  \ 7 internal spelling letters to maximize the absorption-predicted arm's n. \nPARENT UNRESOLVED for a hierarchy (no responsive\
  \ latent clears the 20% firing floor): log parent_unresolved, default its entities to co_firing, exclude from absorption-structured\
  \ count, note it — do not crash. \nGPU OOM / shared-GPU contention: the copied Encoder already retries acquire/forward;\
  \ additionally cut cap_pos_per_entity (300->150) and cap_neg (4000->2000), or run `--scale mini` for the homograph arm while\
  \ keeping full derivation. Encode each hierarchy's corpus ONCE and slice per entity (never re-encode per entity) to stay\
  \ within wall-clock. \nDERIVATION DOES NOT REPRODUCE tau_h~0.7795 / balanced_acc 1.0: report the ACTUAL frozen values, freeze\
  \ on them anyway (the rule is whatever derivation yields), and flag the drift in honest_notes — do not hard-fail. \nTORCH/CUDA\
  \ INSTALL: if torch wheel resolution fails, install with the cu124 index workaround (`uv pip install ... --index-strategy\
  \ unsafe-best-match`) per prior-iter GOTCHA; reuse the iter-5 pyproject.toml/.venv pins. SAE + model are public non-gated\
  \ mirrors (google/gemma-scope-2b-pt-res, unsloth/gemma-2-2b); set HF_HUB_DISABLE_PROGRESS_BARS=1; only set HF_HUB_OFFLINE=1\
  \ AFTER a successful first download."
testing_plan: "STAGE 1 — SMOKE (`python method.py --smoke`, minutes, no full data): load model+SAE; assert gating recon_cos_mean>0.80\
  \ (iter-5 got 0.927) and the BOS/offset token-id self-check passes on a few real corpus windows; build ONE homograph hierarchy\
  \ (e.g. city) and run 2-3 entities end-to-end; assert: parent identified (or cleanly parent_unresolved), recall_hole_E and\
  \ jaccard_E computed, predicted_regime LOGGED before the outcome line, _outcome_core returns finite auc_unit/auc_a/delta,\
  \ a Wilson CI object is produced, and a tiny exp_gen_sol_out validates via aii-json. CONFIRM the data path resolves (or\
  \ the rebuild ran). \nSTAGE 2 — MINI (`--scale mini`): run full derivation (12 concepts) + a 1-2-entity-per-hierarchy subset\
  \ + the 7 spelling letters. CONFIRMATION SIGNALS that the pipeline is correct: (a) derivation reproduces recall-hole-alone\
  \ tau_h ~0.78 with balanced_acc 1.0 and LOO ~0.83 (matches iter-5 — strongest single-run integrity check); (b) spelling\
  \ letters F/M/W reproduce recall_hole=1.0 (the documented over-prediction counterexample); (c) at least some homograph entities\
  \ show recall_hole>0.5 with low jaccard (absorption-structured) — Phoenix/Mobile/Reading/Apple/Amazon are prime candidates;\
  \ if NONE do, that is a real (publishable) breadth-narrow signal, not a bug, but double-check the corpus positive filter\
  \ (target_sense==parent sense, not 'competitor'). (d) predict-then-measure ordering visible in the log for every prospective\
  \ entity. \nSTAGE 3 — FULL (`--scale full`): all 4 hierarchies, all eligible entities. Validate: prospective_hitrate_primary\
  \ strata + Wilson CIs present; router_verdict set by the excludes-0.5 rule; absorption_breadth count + named new cases present;\
  \ derivation_concepts and prospective_entities disjoint; honest_notes carry the three verbatim counterexamples; method_out.json\
  \ + full/mini/preview validate against exp_gen_sol_out and each < 100MB; cache/ excluded from upload. Sanity cross-check:\
  \ number of absorption-PREDICTED entities (recall_hole>0.7795) <= number absorption-STRUCTURED (recall_hole>0.5) — the 0.7795\
  \ gate is stricter than the 0.5 breadth flag. Track cumulative OpenRouter spend (router itself is $0; only a data rebuild\
  \ can incur cost) and stop well under $10."
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
