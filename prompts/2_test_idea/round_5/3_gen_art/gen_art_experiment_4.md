# gen_art_experiment_4 — test_idea

> Phase: `invention_loop` · round 5 · `gen_art`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_experiment_4` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 02:12:06 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_4`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_4/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_4/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_4/results/out.json`
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
id: gen_plan_experiment_4_idx4
type: experiment
title: >-
  M7 — Second Polysemy/Absorption Case Beyond Georgia: Profession Is-A Hierarchy + Homograph Scan + Jordan-Beside-Georgia
summary: >-
  Search for >=1 additional suppressed-parent absorption case to corroborate the non-spelling set-cover-selection result that
  is currently effectively n=1 (Georgia), 1-2 with descriptive Jordan. Three parts on the FROZEN Gemma-2-2b / Gemma-Scope
  layer_12/width_16k JumpReLU SAE: (1) NEW corpus-only test of a SECOND is-a hierarchy = bias_in_bios professions (general
  'occupation' parent suppressed on specific professions), GPU-encoded fresh; (2) HOMOGRAPH SCAN re-running the country cross-tab
  + entity-token scan on the CACHED taxonomic encodings (CPU); (3) JORDAN-BESIDE-GEORGIA side-by-side selection table with
  n + eligibility. Reuse the iter-4 precision-gated K-track + selectors + AUC-diff machinery verbatim where possible. The
  EXPECTED, fully-publishable outcome is an honest negative ('absorption is narrow / specific to homograph-polysemy, not a
  general is-a-hierarchy phenomenon'); a positive second case strengthens the paper. Emit method_out.json (exp_gen_sol_out
  schema) with full hole tables, set-cover results with CIs, the side-by-side table, a 'second-case-found' vs 'absorption-remains-narrow'
  verdict, and per-row diagnostic predictions; validate full/mini/preview < 100MB.
runpod_compute_profile: gpu
implementation_pseudocode: |-
  # ===================================================================================
  # GOAL (M7): corroborate the non-spelling absorption/set-cover result beyond Georgia.
  # THREE PARTS. Part 1 (professions) is the NEW science and needs GPU encoding (no cache).
  # Parts 2-3 reuse the iter-4 taxonomic CACHE on CPU. Honest negative is the EXPECTED, publishable outcome.
  # ===================================================================================
  #
  # ---- ABSOLUTE PATHS (verified to exist by the planner) ----
  # ITER4_DIR  = /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_3
  # METHOD_SRC = ITER4_DIR/method.py            # 2108-line engine to COPY+adapt (do not re-derive)
  # TAX_LAT    = ITER4_DIR/cache/lat_taxonomic_w16384_n15748.npz   # cached taxonomic latents (CSR)
  # TAX_RES    = ITER4_DIR/cache/resid_taxonomic_w16384_n15748.npy # cached taxonomic residuals (fp16)
  # TAX_DATA   = .../iter_1/gen_art/gen_art_dataset_2/full_data_out.json   # taxonomic+numeric testbed
  # BIOS_DATA  = .../iter_1/gen_art/gen_art_dataset_4/full_data_out.json   # sentiment+aspect+bias_in_bios
  # DOSSIER_M  = .../iter_1/gen_art/gen_art_research_1/research_out.json    # SAE pipeline/baseline spec
  # DOSSIER_D  = .../iter_1/gen_art/gen_art_research_2/research_out.json    # form-free absorption diagnostic
  #
  # STEP 0 — SCAFFOLD & REUSE ENGINE
  #   * Copy METHOD_SRC into THIS workspace as engine.py; import its functions rather than rewriting:
  #       load_sae, JumpReLUSAE, _find_sae_params, load_model, Encoder (adapted), encode_or_cache,
  #       run_greedy, iter3_extensions, formfree_edge_agreement, admission_check, bootstrap_ci,
  #       paired_diff_ci, fast_auc, _auc_rows, _youden_table, firing_jaccard_pos, holm, match_threshold,
  #       emit_method_out, _json_default, write_figure_csvs.
  #   * Copy the two taxonomic cache files into ./cache/ with IDENTICAL names so engine.encode_or_cache
  #     loads them (it asserts shape (15748,16384)); set CACHE_DIR=./cache. Keep CPU-fallback block intact.
  #   * Pin pyproject deps to the iter-4 versions (torch, numpy, scipy, scikit-learn, statsmodels, loguru,
  #     transformers, huggingface_hub, networkx). Install a torch wheel matching the LANDED GPU arch
  #     (cu124+; the gpu profile may fall back to A4000/L4/4090 = sm_86/89 which standard torch supports;
  #     only the 5090=sm_120 needs a newer wheel — probe CUDA once like engine.py and CPU-fall-back if a
  #     real device op raises).
  #   * Constants reused verbatim: G1_RECALL=0.60, JACCARD_MAX=0.10, SUBCTX_PREC=0.70, GAIN_MIN=0.05,
  #     PRECISION_FLOOR=0.70, N_MIN_ELIGIBLE=150, GREEDY_MAX_MEMBERS=12, SEED=20240617, D_MODEL=2304.
  #
  # ===================================================================================
  # PART 1 — SECOND IS-A HIERARCHY: bias_in_bios PROFESSIONS  (NEW, GPU encode)
  # bias_in_bios rows have NO content pairs and NO target spans -> CORPUS-ONLY adaptation.
  # Framing: parent concept = 'occupation/profession' (general); CHILDREN/sub-contexts = the 28
  # professions; absorption = a general occupation latent that fires on most bios but has profession-
  # specific recall HOLES where a mutually-exclusive specialist fires instead.
  # ===================================================================================
  #
  # 1A. LOAD & SUBSAMPLE
  #   bios = [r for r in BIOS_DATA.datasets where dataset name family=='bias_in_bios_boundary']
  #       each row: input=bio text, output=profession (e.g. 'journalist'), metadata_sub_context={'gender':..},
  #                 metadata_concept_label=profession, metadata_meta.raw_profession_int (0..27).
  #   prof = output label; gender = sub_context.gender.
  #   Keep ALL 28 professions; flag profession descriptive_only if its TOTAL bios < 2*N_MIN_ELIGIBLE
  #     (need >=150 in the diagnostic fold AFTER a 50/50 split). dataset is gender-balanced ~20,177/28~=720
  #     avg, but skewed -> some rare professions (e.g. rapper/dj/personal_trainer) may fall below.
  #   To bound GPU cost, optionally cap bios per profession at ~600 (stratified by gender, seed 20240617):
  #     total ~ min(20177, 28*600) ~= 12-16k. Record the cap in metadata.
  #
  # 1B. NEGATIVE POOL (for parent precision-gating + dense-probe baseline)
  #   neg_texts = stratified subsample ~5,000 from BIOS_DATA sentiment (movie reviews) + restaurant_aspect
  #     (CEBaB reviews) families — full texts, NON-occupation, SAME corpus file, encoded with IDENTICAL
  #     whole-text pooling so pool SIZE is held fixed (no length confound vs the single-slot taxonomic neg).
  #   CAVEAT to log + guard: a 'parent' could key on genre (bio vs review) not 'occupation'. MITIGATION:
  #     the PRIMARY per-profession AUC is ONE-VS-REST WITHIN bios (positives=prof-p bios, negatives=other-
  #     profession bios) which is genre-matched; non-bio negatives are used ONLY for parent precision-gating
  #     and the dense-probe sanity baseline. Report both negative regimes.
  #
  # 1C. ENCODE (GPU; the ONE expensive step — no cache exists)
  #   * Adapt engine.Encoder: bios have no target span, so add a pooling mode 'whole_text' ->
  #       positions = all tokens with non-zero offset width and attention_mask==1 (exclude BOS/pad).
  #       resid[gid] = mean over those token residuals (fp16); pooled_lat = MAX over those tokens' SAE
  #       latents (firing detector) -> CSR row. (Same max-pool firing rule as the rest of the method.)
  #   * MAXLEN=256 (bio char_len up to ~500 => ~120 tok; covers it). BATCH=16. Validate FVU<0.6, meanL0
  #     plausible (engine asserts). Token-alignment metric is N/A here (no target_text) -> skip that assert.
  #   * Determine layer via engine.determine_layer_idx on a 32-bio sample (expect hidden_states[13]).
  #   * SAVE cache: ./cache/lat_bias_w16384_n{N}.npz, resid_bias_w16384_n{N}.npy (so re-runs are GPU-free).
  #   * Encode neg_texts the SAME way -> lat_neg, resid_neg.
  #
  # 1D. FOLD SPLIT (mirror the method's selection/eval discipline)
  #   Split bios 50/50 train(SELECTION) / diagnostic(HELD-OUT), STRATIFIED by profession (seed 20240617).
  #   Gates, anchor recall, firing-Jaccard, subctx precision, greedy are FIT on SELECTION; AUC / hole table
  #   / router REPORTED on the disjoint HELD-OUT fold.
  #
  # 1E. PARENT (anchor) IDENTIFICATION — corpus-only (no content pairs)
  #   * 'content-responsive'/discriminative latent := firing_rate(bios_sel) - firing_rate(neg) above a
  #     LABEL-SHUFFLE null (shuffle bio/neg labels B=1000, 95th pct), AND content-style precision
  #     prec_l = firing on bios / (firing on bios + firing on neg) >= PRECISION_FLOOR(0.70).
  #   * anchor = among precision-passing discriminative latents, the one with the HIGHEST overall bio-recall
  #     (fraction of ALL selection bios where it max-fires). Firing-floor validation: anchor must fire on
  #     >5% of HELD-OUT bios (drops spurious 0%-corpus anchors, the iter-4 letter-I fix).
  #   * Also fit the dense parent probe d_p: LogisticRegression(class_weight='balanced') on mean-pooled
  #     residuals, bios(+1) vs neg(0), TRAIN fold -> non-SAE baseline direction (engine Phase 4 recipe).
  #
  # 1F. PER-PROFESSION HOLE TABLE (the headline deliverable; reported for ALL 28)
  #   For each profession p (held-out fold):
  #     recall_p   = mean(anchor fires on prof-p bios);  hole_p = 1 - recall_p
  #     specialists_p = latents with one-vs-rest subctx FIRING precision_p >= 0.70 (prof-p vs other-prof bios)
  #                     AND fire on >= GAIN_MIN of prof-p bios.
  #     best_jaccard_p = min over specialists_p of positive-only firing_jaccard(specialist, anchor)
  #     absorption_type_p = (hole_p > 0.5) AND (exists specialist with best_jaccard_p < JACCARD_MAX)
  #     n_p, eligible_p = (n_p >= N_MIN_ELIGIBLE)
  #   Emit hole_table[p] = {n, eligible, parent_recall, parent_hole, best_specialist, best_jaccard,
  #                         n_specialists, absorption_type, gender_split:{male_hole,female_hole}}.
  #   IMPORTANT: a uniform parent_recall~1.0 across professions (NO holes) is the EXPECTED boundary-null and
  #   must be emitted explicitly as 'absorption does not generalize to the profession is-a hierarchy'.
  #
  # 1G. SET-COVER + SELECTION ISOLATION (only for professions with absorption_type==True)
  #   For each qualifying profession q:
  #     * Build per-fold firing matrices over the discriminative/eligible latent pool ELIG (precision>=0.70).
  #     * anchor = parent; HOLES = prof-q bios the anchor misses; run engine.run_greedy variant='gated'
  #       (per-sub-context firing-precision gate + mutual-exclusivity J<0.10 + gain>=0.05 CI>0) AND 'weighted'.
  #     * Build det_scores via engine.iter3_extensions-style logic adapted to ONE-VS-REST (positives=prof-q
  #       held-out bios, negatives=other-profession held-out bios):
  #         unit (max-pool members), anchor, g (top-20 |mean_pos-mean_neg| marginal-attr), h (count-matched),
  #         dense_probe (one-vs-rest LR on residual), RE-k, RE-k-anchored, S_rec (top-k by bio-recall),
  #         S_prec (top-k by subctx precision), S_mag (top-k by mean firing magnitude).
  #     * AUC-diff CIs: stratified paired bootstrap B>=10,000 (resample positives & negatives separately),
  #       reuse engine._auc_rows. set_cover_established_q := unit beats S_rec_anch AND S_prec_anch AND
  #       S_mag_anch AND RE-k-anchored AND g AND h with 95% CI excluding 0 on the prof-q slice.
  #     * setcover_corroborated_q := the greedy-chosen specialist is the precision-diagnostic member (held-out
  #       subctx precision >= 0.70) AND form-free KG agreement via engine.formfree_edge_agreement (note the
  #       known precision-blindness of the magnitude oracle; report precision diagnostic as primary).
  #   If NO profession qualifies: skip set-cover, set professions verdict = 'no_absorption_signature'.
  #
  # ===================================================================================
  # PART 2 — HOMOGRAPH SCAN  (CPU; reuse taxonomic cache)
  # ===================================================================================
  # 2A. Re-run the taxonomic pipeline from the CACHE to regenerate the homograph x absorption-type
  #     cross-tab over all 52 countries (engine.analyze_hierarchy + engine.iter3_extensions, name='taxonomic',
  #     use_cache=True). Confirms absorption_type==True for EXACTLY {Georgia, Jordan} (the iter-4 result),
  #     non-homograph countries (incl. United States) NOT absorption_type. Emit homograph_crosstab cell lists.
  # 2B. Entity-token scan beyond countries: the taxonomic testbed uses country-vs-CITY and country-vs-other-
  #     proper-noun negative families, so CITY / proper-noun surface tokens are present in x_off + corpus-neg
  #     rows. Group corpus rows by surface token (metadata_target_text on negatives / city gazetteer), and for
  #     any entity surface with >= N_MIN_ELIGIBLE occurrences test the SAME signature (a general parent latent
  #     for that entity-type with recall-hole>0.5 AND a specialist with firing-Jaccard<0.1). Report each
  #     qualifying entity with its set-cover result, OR honestly that the scan surfaced NONE beyond Georgia/Jordan.
  #     (Expected: none — the testbed has per-country labels but not per-city labels, so this is a best-effort
  #      scan; log the coverage limitation explicitly so 'no new case' is not over-read as exhaustive.)
  #
  # ===================================================================================
  # PART 3 — JORDAN BESIDE GEORGIA  (CPU; reuse taxonomic cache + iter-4 numbers)
  # ===================================================================================
  # Build ONE side_by_side table from the Part-2 taxonomic re-run:
  #   row Georgia: n_pos(150), eligible=True, absorption_type=True, parent_hole(~0.80), firing_jaccard(~0.059),
  #                unit_AUC(~0.995), AUC-diff CIs vs S_rec/S_prec/S_mag/RE-k-anch/g/h/dense, set_cover_established=True
  #   row Jordan:  n_pos(124), eligible=False (DESCRIPTIVE <150), absorption_type=True, parent_hole(~0.71),
  #                firing_jaccard, unit_AUC + AUC-diff CIs, set_cover_established (report value), status='descriptive'
  #   row United States: firing_jaccard(~0.20), absorption_type=False (co-firing/splitting, NOT absorption), n_pos
  #   Annotate: affirmative non-spelling set-cover evidence is currently ONE eligible slice (Georgia),
  #   1-2 counting descriptive Jordan; US is co-firing not absorption.
  #
  # ===================================================================================
  # STEP 4 — VERDICT + EMIT
  # ===================================================================================
  #   second_case_found := (any qualifying profession with set_cover_established) OR (any new homograph entity
  #                         with set_cover_established).
  #   verdict = 'second_case_found' if second_case_found else 'absorption_remains_narrow'
  #     ('absorption is narrow / specific to suppressed-parent homograph polysemy; the profession is-a
  #       hierarchy shows uniform-high parent recall = NO absorption' — the publishable honest negative).
  #   Emit method_out.json (engine.emit_method_out signature) with:
  #     metadata.per_family = {
  #        professions: {hole_table(all 28), parent_latent, anchor_recall, eligible_professions,
  #                      qualifying_professions, setcover (per qualifying: members, edges, auc_point,
  #                      auc_diff_ci, set_cover_established, setcover_corroborated, kg_agreement),
  #                      negative_regime_notes, gender_secondary, professions_verdict},
  #        taxonomic: {homograph_crosstab, homograph_scan, side_by_side(Georgia/Jordan/US)} },
  #     metadata.verdict, metadata.sae(release/sae_id/width/hook/layer/d_model), metadata.stats,
  #     metadata.thresholds, metadata.encoding(per-family fvu/meanL0/cached), metadata.runtime_s,
  #     metadata.honest_negatives (verbatim list incl. profession boundary-null, scan coverage limit, n=1-2).
  #   datasets = [{dataset:'professions', examples: per-bio held-out predictions predict_{unit,anchor,g,h,
  #                dense_probe,rek,S_rec,S_prec,S_mag} + metadata_sub_context(profession)+gender},
  #               {dataset:'taxonomic_sidebyside', examples: per-row predictions for Georgia/Jordan/US slices}].
  #   Run aii-json: validate method_out.json against exp_gen_sol_out; generate mini_/preview_method_out.json;
  #     ensure each < 100MB (cap examples to ~6-8k held-out rows like engine.make_predictions max_rows; if the
  #     full file exceeds 100MB, follow aii-file-size-limit to split).
  #
  # DELIVERABLES: engine.py (copied+adapted method), profession_absorption.py (Part 1 driver), method_out.json +
  #   full/mini/preview_method_out.json, results/*.csv (hole_table, side_by_side, homograph_crosstab,
  #   per-prof auc_diff), cache/lat_bias_*.npz, RESULTS_SUMMARY.md.
fallback_plan: |-
  COMPUTE / ENCODING FALLBACKS (Part 1 is the only GPU-dependent part):
    (a) GPU non-functional (sm_120/5090 'no kernel image'): engine.py already probes CUDA and CPU-falls-back, but ENCODING needs a working device. First retry relies on the gpu-profile fallback ladder (A4000/L4/4090 = sm_86/89 work with standard torch). If still broken, install a cu128 nightly torch matching sm_120; if that fails, subsample bios to ~6k (>=200/profession for the top ~20 professions) and mean-pool-encode on CPU (slow but bounded; ~1-2h). Document the subsample in metadata.
    (b) Encoding OOM / slow: drop BATCH to 8, MAXLEN to 192 (bios rarely exceed), free hidden_states each batch (engine already does), checkpoint the CSR every ~2k rows so a crash resumes from cache.

  SCIENCE FALLBACKS (each is itself a publishable result, consistent with the boundary-null framing):
    (c) NO general 'occupation' parent latent exists (no precision-passing high-recall latent across professions): report 'the profession is-a hierarchy has no suppressed general parent' -> absorption test VOID for professions (a finding: the phenomenon needs a token-level general parent, which professions lack). Still emit the discriminative-latent table + the dense-probe AUC so the section is non-empty.
    (d) Uniform high parent recall, no profession hole > 0.5 (the EXPECTED boundary-null): this is the primary honest-negative SUCCESS path -> verdict='absorption_remains_narrow', emit the full 28-row hole table as the evidence. Do NOT treat this as failure.
    (e) A profession shows a hole but NO mutually-exclusive specialist (firing-Jaccard>=0.1 everywhere = co-firing/splitting, like United States): report it as 'splitting not absorption', not a second case.
    (f) A profession qualifies the signature but the unit does NOT beat S-rec/S-prec/S-mag (CIs include 0): report set_cover_established=False -> 'eligibility+pooling, not set-cover-specific selection' (the numeric-integer outcome analog).
    (g) Genre confound suspected (parent keys on bio-vs-review not occupation): rely on the one-vs-rest WITHIN-bios AUC (genre-matched) as primary and DOWNWEIGHT the non-bio-negative result; report both and flag the confound.
    (h) Homograph entity scan surfaces nothing (likely, given per-city labels are absent): report 'no new homograph case beyond Georgia/Jordan; scan limited by available per-entity labels' — honest and expected.
    (i) If Part 1 cannot run at all (no compute), still deliver Parts 2-3 (CPU cache reuse) = the homograph cross-tab + Jordan-beside-Georgia table, and mark professions 'not_run_compute'. This is a degraded but non-empty deliverable; avoid this path if any GPU is obtainable.

  OVERALL: the artifact SUCCEEDS whether it finds a second case OR honestly concludes absorption is narrow; the failure mode to avoid is an un-interpretable/empty result. Always emit the full hole table + side-by-side table with CIs.
testing_plan: |-
  Gradual scaling with confirmation signals at each rung (aii-long-running-tasks pattern):
    1. ENGINE WIRING (CPU, seconds, no model): run the copied engine in --scale smoke against the COPIED taxonomic cache. It must reproduce the iter-4 invariants: anchor latent==3792, gated unit contains Georgia specialist 16009 and NOT low-precision 4697, Georgia held-out subctx precision >= 0.70. This confirms the cache copy + reused functions are intact BEFORE touching professions.
    2. SAE/POOLING SANITY (GPU, ~1 min): encode 32 bios (2 professions) with the new whole-text pooling. Assert FVU < 0.6 (SAE/layer pipeline correct), meanL0 in (1, width*0.5), and that >0 tokens were selected per bio (no all-dropped rows). Print 3 example bios + their top firing latents (logit-lens sanity that an 'occupation'-ish latent appears).
    3. PARENT/HOLE SMOKE (GPU, ~3-5 min): encode ~2,000 bios (4 professions incl. a likely-distinct one e.g. nurse/surgeon/attorney/poet) + 1,000 negatives. Run parent identification + the per-profession hole table on this mini set. Confirm: an anchor is found with recall>0.6 + firing-floor>5%; the hole table is populated for all 4; the S-rec/S-prec/S-mag selectors + RE-k baselines + AUC-diff CIs execute without shape errors. Eyeball whether any hole>0.5 appears.
    4. PART 2/3 SMOKE (CPU, ~5 min): full taxonomic re-run from cache; assert the homograph cross-tab yields exactly {Georgia, Jordan} absorption_type==True and the side-by-side table has Georgia(eligible)/Jordan(descriptive n=124)/US(co-firing) rows with AUC-diff CIs present.
    5. FULL RUN: encode the full (or capped ~12-16k) bios + 5k negatives; run all three parts; B_auc>=10,000, B_draws=1000. Watch logs for: encode FVU/meanL0 per family, anchor recall + firing-floor, count of professions with absorption_type, any set_cover_established, and the final verdict line.
    6. OUTPUT VALIDATION: aii-json validate method_out.json vs exp_gen_sol_out; generate + validate mini/preview; confirm each file < 100MB (split per aii-file-size-limit if needed). Spot-check that per-row predict_* fields are present and the hole_table has all 28 professions.
  CONFIRMATION SIGNALS before trusting the full run: smoke invariants pass (rung 1), FVU<0.6 on bios (rung 2), hole table populated + CIs computed (rung 3), Georgia/Jordan cross-tab reproduced (rung 4). If rung-1 invariants fail, the cache copy or function reuse is broken — fix before proceeding. If FVU>=0.6 on bios, the layer/pooling is wrong — re-check determine_layer_idx and the whole-text position selection.
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

--- Dependency 4 ---
id: art_21JWypIydPMX
type: dataset
title: CCRG supporting sentiment/aspect families + bias_in_bios boundary-null dataset
summary: >-
  Three REAL, human-annotated datasets standardized into the CCRG shared minimal-pair schema and emitted in the canonical
  exp_sel_data_out format ({metadata, datasets:[{dataset, examples:[{input, output, metadata_*}]}]}), ONE example per text
  row, grouped by dataset, $0 LLM spend. Families (separable via metadata_family): (1) sentiment = CAD-IMDB (Kaushik et al.
  ICLR 2020), 4,880 rows / 2,440 human counterfactual content-flip pairs (positive<->negative), supporting; (2) restaurant_aspect
  = CEBaB (Abraham et al. NeurIPS 2022), 5,682 rows / 2,841 pairs (food 1,740 + service 1,101) flipping ONE aspect's sentiment
  with all four aspect majorities (food/service/ambiance/noise) + binarized review_sentiment retained as INDEPENDENT sub_context
  labels, supporting; (3) bias_in_bios_boundary = LabHC/bias_in_bios (De-Arteaga et al. 2019), 20,177 profession bios (28
  classes, gender as independent sub-context), the PRE-REGISTERED boundary-null where habitat~=label. Total 30,739 rows, 5,281
  reconstructable minimal pairs. Per row: input(text), output(canonical label), and metadata_* fields: id, family, dataset_source,
  concept(sentiment|food_sentiment|service_sentiment|profession), concept_label, sub_context(dict), pair_id, partner_id, pair_role(content_on|content_off|null),
  flip_type(content|null), is_content_pair, is_surface_pair(false for all), fold(train|dev|test), meta(raw fields incl char_len,
  token_overlap_with_partner, raw labels, subsample seed). Every (x_off,x_on) content pair is reconstructable via pair_id/partner_id
  (content_on=positive/concept-present member). is_surface_pair=false everywhere — surface flips are out of scope here (reserved
  for sibling ParaDetox/LLM artifacts); no surface pairs fabricated. NO derived statistics (MI/probes) computed — raw standardized
  data only. Every row validated against schema.json (jsonschema Draft7) AND full/mini/preview validated against exp_sel_data_out
  (aii-json). THREE plan errors were caught and corrected by empirical verification: (a) CAD-IMDB orig/<->new/ row alignment
  is FALSE (flip_rate~0.50, aligned Jaccard~=random~0.11) — authoritative pairing taken from the repo's combined/paired/*_paired.tsv
  via shared batch_id (true-pair Jaccard 0.816 vs random 0.108); (b) CEBaB edit_type is the edited ASPECT {food,service,ambiance,noise}
  and edit_goal is the target sentiment (the plan swapped them), and review_majority is a 1-5 star rating (binarized 1,2->neg
  / 4,5->pos / 3->neutral); (c) bias_in_bios ships no ClassLabel names, so the canonical 28-occupation alphabetical mapping
  (incl 'dj' at index 8) was verified empirically 17/17 by keyword hit-rate (nurse=13, attorney=2, surgeon=25, software_engineer=24,
  yoga_teacher=27), gender 0=male/1=female confirmed by pronouns; stratified (profession x gender, 56 strata) capped subsample
  with fixed seed 20240617, gender-balanced (male 10,054 / female 10,123). Licenses: CAD Apache-2.0, CEBaB CC-BY-4.0, bias_in_bios
  MIT. Reproduce all deliverables with `uv run data.py`. Downstream guidance: compute per-family bootstrap CIs as primary
  (families cleanly separated); treat any bias_in_bios null as the expected boundary outcome, not method failure; build content
  (x_off,x_on) deltas from pair_id.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_4
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

### [2] HUMAN-USER prompt · 2026-06-18 02:12:06 UTC

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

### [3] SKILL-INPUT — aii-use-hardware · 2026-06-18 02:12:18 UTC

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

### [4] SKILL-INPUT — aii-long-running-tasks · 2026-06-18 02:12:18 UTC

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

### [5] SKILL-INPUT — aii-json · 2026-06-18 02:14:14 UTC

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

### [6] SYSTEM-USER prompt · 2026-06-18 03:10:32 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_4`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_4/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_4/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_4/results/out.json`
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
id: gen_plan_experiment_4_idx4
type: experiment
title: >-
  M7 — Second Polysemy/Absorption Case Beyond Georgia: Profession Is-A Hierarchy + Homograph Scan + Jordan-Beside-Georgia
summary: >-
  Search for >=1 additional suppressed-parent absorption case to corroborate the non-spelling set-cover-selection result that
  is currently effectively n=1 (Georgia), 1-2 with descriptive Jordan. Three parts on the FROZEN Gemma-2-2b / Gemma-Scope
  layer_12/width_16k JumpReLU SAE: (1) NEW corpus-only test of a SECOND is-a hierarchy = bias_in_bios professions (general
  'occupation' parent suppressed on specific professions), GPU-encoded fresh; (2) HOMOGRAPH SCAN re-running the country cross-tab
  + entity-token scan on the CACHED taxonomic encodings (CPU); (3) JORDAN-BESIDE-GEORGIA side-by-side selection table with
  n + eligibility. Reuse the iter-4 precision-gated K-track + selectors + AUC-diff machinery verbatim where possible. The
  EXPECTED, fully-publishable outcome is an honest negative ('absorption is narrow / specific to homograph-polysemy, not a
  general is-a-hierarchy phenomenon'); a positive second case strengthens the paper. Emit method_out.json (exp_gen_sol_out
  schema) with full hole tables, set-cover results with CIs, the side-by-side table, a 'second-case-found' vs 'absorption-remains-narrow'
  verdict, and per-row diagnostic predictions; validate full/mini/preview < 100MB.
runpod_compute_profile: gpu
implementation_pseudocode: |-
  # ===================================================================================
  # GOAL (M7): corroborate the non-spelling absorption/set-cover result beyond Georgia.
  # THREE PARTS. Part 1 (professions) is the NEW science and needs GPU encoding (no cache).
  # Parts 2-3 reuse the iter-4 taxonomic CACHE on CPU. Honest negative is the EXPECTED, publishable outcome.
  # ===================================================================================
  #
  # ---- ABSOLUTE PATHS (verified to exist by the planner) ----
  # ITER4_DIR  = /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_3
  # METHOD_SRC = ITER4_DIR/method.py            # 2108-line engine to COPY+adapt (do not re-derive)
  # TAX_LAT    = ITER4_DIR/cache/lat_taxonomic_w16384_n15748.npz   # cached taxonomic latents (CSR)
  # TAX_RES    = ITER4_DIR/cache/resid_taxonomic_w16384_n15748.npy # cached taxonomic residuals (fp16)
  # TAX_DATA   = .../iter_1/gen_art/gen_art_dataset_2/full_data_out.json   # taxonomic+numeric testbed
  # BIOS_DATA  = .../iter_1/gen_art/gen_art_dataset_4/full_data_out.json   # sentiment+aspect+bias_in_bios
  # DOSSIER_M  = .../iter_1/gen_art/gen_art_research_1/research_out.json    # SAE pipeline/baseline spec
  # DOSSIER_D  = .../iter_1/gen_art/gen_art_research_2/research_out.json    # form-free absorption diagnostic
  #
  # STEP 0 — SCAFFOLD & REUSE ENGINE
  #   * Copy METHOD_SRC into THIS workspace as engine.py; import its functions rather than rewriting:
  #       load_sae, JumpReLUSAE, _find_sae_params, load_model, Encoder (adapted), encode_or_cache,
  #       run_greedy, iter3_extensions, formfree_edge_agreement, admission_check, bootstrap_ci,
  #       paired_diff_ci, fast_auc, _auc_rows, _youden_table, firing_jaccard_pos, holm, match_threshold,
  #       emit_method_out, _json_default, write_figure_csvs.
  #   * Copy the two taxonomic cache files into ./cache/ with IDENTICAL names so engine.encode_or_cache
  #     loads them (it asserts shape (15748,16384)); set CACHE_DIR=./cache. Keep CPU-fallback block intact.
  #   * Pin pyproject deps to the iter-4 versions (torch, numpy, scipy, scikit-learn, statsmodels, loguru,
  #     transformers, huggingface_hub, networkx). Install a torch wheel matching the LANDED GPU arch
  #     (cu124+; the gpu profile may fall back to A4000/L4/4090 = sm_86/89 which standard torch supports;
  #     only the 5090=sm_120 needs a newer wheel — probe CUDA once like engine.py and CPU-fall-back if a
  #     real device op raises).
  #   * Constants reused verbatim: G1_RECALL=0.60, JACCARD_MAX=0.10, SUBCTX_PREC=0.70, GAIN_MIN=0.05,
  #     PRECISION_FLOOR=0.70, N_MIN_ELIGIBLE=150, GREEDY_MAX_MEMBERS=12, SEED=20240617, D_MODEL=2304.
  #
  # ===================================================================================
  # PART 1 — SECOND IS-A HIERARCHY: bias_in_bios PROFESSIONS  (NEW, GPU encode)
  # bias_in_bios rows have NO content pairs and NO target spans -> CORPUS-ONLY adaptation.
  # Framing: parent concept = 'occupation/profession' (general); CHILDREN/sub-contexts = the 28
  # professions; absorption = a general occupation latent that fires on most bios but has profession-
  # specific recall HOLES where a mutually-exclusive specialist fires instead.
  # ===================================================================================
  #
  # 1A. LOAD & SUBSAMPLE
  #   bios = [r for r in BIOS_DATA.datasets where dataset name family=='bias_in_bios_boundary']
  #       each row: input=bio text, output=profession (e.g. 'journalist'), metadata_sub_context={'gender':..},
  #                 metadata_concept_label=profession, metadata_meta.raw_profession_int (0..27).
  #   prof = output label; gender = sub_context.gender.
  #   Keep ALL 28 professions; flag profession descriptive_only if its TOTAL bios < 2*N_MIN_ELIGIBLE
  #     (need >=150 in the diagnostic fold AFTER a 50/50 split). dataset is gender-balanced ~20,177/28~=720
  #     avg, but skewed -> some rare professions (e.g. rapper/dj/personal_trainer) may fall below.
  #   To bound GPU cost, optionally cap bios per profession at ~600 (stratified by gender, seed 20240617):
  #     total ~ min(20177, 28*600) ~= 12-16k. Record the cap in metadata.
  #
  # 1B. NEGATIVE POOL (for parent precision-gating + dense-probe baseline)
  #   neg_texts = stratified subsample ~5,000 from BIOS_DATA sentiment (movie reviews) + restaurant_aspect
  #     (CEBaB reviews) families — full texts, NON-occupation, SAME corpus file, encoded with IDENTICAL
  #     whole-text pooling so pool SIZE is held fixed (no length confound vs the single-slot taxonomic neg).
  #   CAVEAT to log + guard: a 'parent' could key on genre (bio vs review) not 'occupation'. MITIGATION:
  #     the PRIMARY per-profession AUC is ONE-VS-REST WITHIN bios (positives=prof-p bios, negatives=other-
  #     profession bios) which is genre-matched; non-bio negatives are used ONLY for parent precision-gating
  #     and the dense-probe sanity baseline. Report both negative regimes.
  #
  # 1C. ENCODE (GPU; the ONE expensive step — no cache exists)
  #   * Adapt engine.Encoder: bios have no target span, so add a pooling mode 'whole_text' ->
  #       positions = all tokens with non-zero offset width and attention_mask==1 (exclude BOS/pad).
  #       resid[gid] = mean over those token residuals (fp16); pooled_lat = MAX over those tokens' SAE
  #       latents (firing detector) -> CSR row. (Same max-pool firing rule as the rest of the method.)
  #   * MAXLEN=256 (bio char_len up to ~500 => ~120 tok; covers it). BATCH=16. Validate FVU<0.6, meanL0
  #     plausible (engine asserts). Token-alignment metric is N/A here (no target_text) -> skip that assert.
  #   * Determine layer via engine.determine_layer_idx on a 32-bio sample (expect hidden_states[13]).
  #   * SAVE cache: ./cache/lat_bias_w16384_n{N}.npz, resid_bias_w16384_n{N}.npy (so re-runs are GPU-free).
  #   * Encode neg_texts the SAME way -> lat_neg, resid_neg.
  #
  # 1D. FOLD SPLIT (mirror the method's selection/eval discipline)
  #   Split bios 50/50 train(SELECTION) / diagnostic(HELD-OUT), STRATIFIED by profession (seed 20240617).
  #   Gates, anchor recall, firing-Jaccard, subctx precision, greedy are FIT on SELECTION; AUC / hole table
  #   / router REPORTED on the disjoint HELD-OUT fold.
  #
  # 1E. PARENT (anchor) IDENTIFICATION — corpus-only (no content pairs)
  #   * 'content-responsive'/discriminative latent := firing_rate(bios_sel) - firing_rate(neg) above a
  #     LABEL-SHUFFLE null (shuffle bio/neg labels B=1000, 95th pct), AND content-style precision
  #     prec_l = firing on bios / (firing on bios + firing on neg) >= PRECISION_FLOOR(0.70).
  #   * anchor = among precision-passing discriminative latents, the one with the HIGHEST overall bio-recall
  #     (fraction of ALL selection bios where it max-fires). Firing-floor validation: anchor must fire on
  #     >5% of HELD-OUT bios (drops spurious 0%-corpus anchors, the iter-4 letter-I fix).
  #   * Also fit the dense parent probe d_p: LogisticRegression(class_weight='balanced') on mean-pooled
  #     residuals, bios(+1) vs neg(0), TRAIN fold -> non-SAE baseline direction (engine Phase 4 recipe).
  #
  # 1F. PER-PROFESSION HOLE TABLE (the headline deliverable; reported for ALL 28)
  #   For each profession p (held-out fold):
  #     recall_p   = mean(anchor fires on prof-p bios);  hole_p = 1 - recall_p
  #     specialists_p = latents with one-vs-rest subctx FIRING precision_p >= 0.70 (prof-p vs other-prof bios)
  #                     AND fire on >= GAIN_MIN of prof-p bios.
  #     best_jaccard_p = min over specialists_p of positive-only firing_jaccard(specialist, anchor)
  #     absorption_type_p = (hole_p > 0.5) AND (exists specialist with best_jaccard_p < JACCARD_MAX)
  #     n_p, eligible_p = (n_p >= N_MIN_ELIGIBLE)
  #   Emit hole_table[p] = {n, eligible, parent_recall, parent_hole, best_specialist, best_jaccard,
  #                         n_specialists, absorption_type, gender_split:{male_hole,female_hole}}.
  #   IMPORTANT: a uniform parent_recall~1.0 across professions (NO holes) is the EXPECTED boundary-null and
  #   must be emitted explicitly as 'absorption does not generalize to the profession is-a hierarchy'.
  #
  # 1G. SET-COVER + SELECTION ISOLATION (only for professions with absorption_type==True)
  #   For each qualifying profession q:
  #     * Build per-fold firing matrices over the discriminative/eligible latent pool ELIG (precision>=0.70).
  #     * anchor = parent; HOLES = prof-q bios the anchor misses; run engine.run_greedy variant='gated'
  #       (per-sub-context firing-precision gate + mutual-exclusivity J<0.10 + gain>=0.05 CI>0) AND 'weighted'.
  #     * Build det_scores via engine.iter3_extensions-style logic adapted to ONE-VS-REST (positives=prof-q
  #       held-out bios, negatives=other-profession held-out bios):
  #         unit (max-pool members), anchor, g (top-20 |mean_pos-mean_neg| marginal-attr), h (count-matched),
  #         dense_probe (one-vs-rest LR on residual), RE-k, RE-k-anchored, S_rec (top-k by bio-recall),
  #         S_prec (top-k by subctx precision), S_mag (top-k by mean firing magnitude).
  #     * AUC-diff CIs: stratified paired bootstrap B>=10,000 (resample positives & negatives separately),
  #       reuse engine._auc_rows. set_cover_established_q := unit beats S_rec_anch AND S_prec_anch AND
  #       S_mag_anch AND RE-k-anchored AND g AND h with 95% CI excluding 0 on the prof-q slice.
  #     * setcover_corroborated_q := the greedy-chosen specialist is the precision-diagnostic member (held-out
  #       subctx precision >= 0.70) AND form-free KG agreement via engine.formfree_edge_agreement (note the
  #       known precision-blindness of the magnitude oracle; report precision diagnostic as primary).
  #   If NO profession qualifies: skip set-cover, set professions verdict = 'no_absorption_signature'.
  #
  # ===================================================================================
  # PART 2 — HOMOGRAPH SCAN  (CPU; reuse taxonomic cache)
  # ===================================================================================
  # 2A. Re-run the taxonomic pipeline from the CACHE to regenerate the homograph x absorption-type
  #     cross-tab over all 52 countries (engine.analyze_hierarchy + engine.iter3_extensions, name='taxonomic',
  #     use_cache=True). Confirms absorption_type==True for EXACTLY {Georgia, Jordan} (the iter-4 result),
  #     non-homograph countries (incl. United States) NOT absorption_type. Emit homograph_crosstab cell lists.
  # 2B. Entity-token scan beyond countries: the taxonomic testbed uses country-vs-CITY and country-vs-other-
  #     proper-noun negative families, so CITY / proper-noun surface tokens are present in x_off + corpus-neg
  #     rows. Group corpus rows by surface token (metadata_target_text on negatives / city gazetteer), and for
  #     any entity surface with >= N_MIN_ELIGIBLE occurrences test the SAME signature (a general parent latent
  #     for that entity-type with recall-hole>0.5 AND a specialist with firing-Jaccard<0.1). Report each
  #     qualifying entity with its set-cover result, OR honestly that the scan surfaced NONE beyond Georgia/Jordan.
  #     (Expected: none — the testbed has per-country labels but not per-city labels, so this is a best-effort
  #      scan; log the coverage limitation explicitly so 'no new case' is not over-read as exhaustive.)
  #
  # ===================================================================================
  # PART 3 — JORDAN BESIDE GEORGIA  (CPU; reuse taxonomic cache + iter-4 numbers)
  # ===================================================================================
  # Build ONE side_by_side table from the Part-2 taxonomic re-run:
  #   row Georgia: n_pos(150), eligible=True, absorption_type=True, parent_hole(~0.80), firing_jaccard(~0.059),
  #                unit_AUC(~0.995), AUC-diff CIs vs S_rec/S_prec/S_mag/RE-k-anch/g/h/dense, set_cover_established=True
  #   row Jordan:  n_pos(124), eligible=False (DESCRIPTIVE <150), absorption_type=True, parent_hole(~0.71),
  #                firing_jaccard, unit_AUC + AUC-diff CIs, set_cover_established (report value), status='descriptive'
  #   row United States: firing_jaccard(~0.20), absorption_type=False (co-firing/splitting, NOT absorption), n_pos
  #   Annotate: affirmative non-spelling set-cover evidence is currently ONE eligible slice (Georgia),
  #   1-2 counting descriptive Jordan; US is co-firing not absorption.
  #
  # ===================================================================================
  # STEP 4 — VERDICT + EMIT
  # ===================================================================================
  #   second_case_found := (any qualifying profession with set_cover_established) OR (any new homograph entity
  #                         with set_cover_established).
  #   verdict = 'second_case_found' if second_case_found else 'absorption_remains_narrow'
  #     ('absorption is narrow / specific to suppressed-parent homograph polysemy; the profession is-a
  #       hierarchy shows uniform-high parent recall = NO absorption' — the publishable honest negative).
  #   Emit method_out.json (engine.emit_method_out signature) with:
  #     metadata.per_family = {
  #        professions: {hole_table(all 28), parent_latent, anchor_recall, eligible_professions,
  #                      qualifying_professions, setcover (per qualifying: members, edges, auc_point,
  #                      auc_diff_ci, set_cover_established, setcover_corroborated, kg_agreement),
  #                      negative_regime_notes, gender_secondary, professions_verdict},
  #        taxonomic: {homograph_crosstab, homograph_scan, side_by_side(Georgia/Jordan/US)} },
  #     metadata.verdict, metadata.sae(release/sae_id/width/hook/layer/d_model), metadata.stats,
  #     metadata.thresholds, metadata.encoding(per-family fvu/meanL0/cached), metadata.runtime_s,
  #     metadata.honest_negatives (verbatim list incl. profession boundary-null, scan coverage limit, n=1-2).
  #   datasets = [{dataset:'professions', examples: per-bio held-out predictions predict_{unit,anchor,g,h,
  #                dense_probe,rek,S_rec,S_prec,S_mag} + metadata_sub_context(profession)+gender},
  #               {dataset:'taxonomic_sidebyside', examples: per-row predictions for Georgia/Jordan/US slices}].
  #   Run aii-json: validate method_out.json against exp_gen_sol_out; generate mini_/preview_method_out.json;
  #     ensure each < 100MB (cap examples to ~6-8k held-out rows like engine.make_predictions max_rows; if the
  #     full file exceeds 100MB, follow aii-file-size-limit to split).
  #
  # DELIVERABLES: engine.py (copied+adapted method), profession_absorption.py (Part 1 driver), method_out.json +
  #   full/mini/preview_method_out.json, results/*.csv (hole_table, side_by_side, homograph_crosstab,
  #   per-prof auc_diff), cache/lat_bias_*.npz, RESULTS_SUMMARY.md.
fallback_plan: |-
  COMPUTE / ENCODING FALLBACKS (Part 1 is the only GPU-dependent part):
    (a) GPU non-functional (sm_120/5090 'no kernel image'): engine.py already probes CUDA and CPU-falls-back, but ENCODING needs a working device. First retry relies on the gpu-profile fallback ladder (A4000/L4/4090 = sm_86/89 work with standard torch). If still broken, install a cu128 nightly torch matching sm_120; if that fails, subsample bios to ~6k (>=200/profession for the top ~20 professions) and mean-pool-encode on CPU (slow but bounded; ~1-2h). Document the subsample in metadata.
    (b) Encoding OOM / slow: drop BATCH to 8, MAXLEN to 192 (bios rarely exceed), free hidden_states each batch (engine already does), checkpoint the CSR every ~2k rows so a crash resumes from cache.

  SCIENCE FALLBACKS (each is itself a publishable result, consistent with the boundary-null framing):
    (c) NO general 'occupation' parent latent exists (no precision-passing high-recall latent across professions): report 'the profession is-a hierarchy has no suppressed general parent' -> absorption test VOID for professions (a finding: the phenomenon needs a token-level general parent, which professions lack). Still emit the discriminative-latent table + the dense-probe AUC so the section is non-empty.
    (d) Uniform high parent recall, no profession hole > 0.5 (the EXPECTED boundary-null): this is the primary honest-negative SUCCESS path -> verdict='absorption_remains_narrow', emit the full 28-row hole table as the evidence. Do NOT treat this as failure.
    (e) A profession shows a hole but NO mutually-exclusive specialist (firing-Jaccard>=0.1 everywhere = co-firing/splitting, like United States): report it as 'splitting not absorption', not a second case.
    (f) A profession qualifies the signature but the unit does NOT beat S-rec/S-prec/S-mag (CIs include 0): report set_cover_established=False -> 'eligibility+pooling, not set-cover-specific selection' (the numeric-integer outcome analog).
    (g) Genre confound suspected (parent keys on bio-vs-review not occupation): rely on the one-vs-rest WITHIN-bios AUC (genre-matched) as primary and DOWNWEIGHT the non-bio-negative result; report both and flag the confound.
    (h) Homograph entity scan surfaces nothing (likely, given per-city labels are absent): report 'no new homograph case beyond Georgia/Jordan; scan limited by available per-entity labels' — honest and expected.
    (i) If Part 1 cannot run at all (no compute), still deliver Parts 2-3 (CPU cache reuse) = the homograph cross-tab + Jordan-beside-Georgia table, and mark professions 'not_run_compute'. This is a degraded but non-empty deliverable; avoid this path if any GPU is obtainable.

  OVERALL: the artifact SUCCEEDS whether it finds a second case OR honestly concludes absorption is narrow; the failure mode to avoid is an un-interpretable/empty result. Always emit the full hole table + side-by-side table with CIs.
testing_plan: |-
  Gradual scaling with confirmation signals at each rung (aii-long-running-tasks pattern):
    1. ENGINE WIRING (CPU, seconds, no model): run the copied engine in --scale smoke against the COPIED taxonomic cache. It must reproduce the iter-4 invariants: anchor latent==3792, gated unit contains Georgia specialist 16009 and NOT low-precision 4697, Georgia held-out subctx precision >= 0.70. This confirms the cache copy + reused functions are intact BEFORE touching professions.
    2. SAE/POOLING SANITY (GPU, ~1 min): encode 32 bios (2 professions) with the new whole-text pooling. Assert FVU < 0.6 (SAE/layer pipeline correct), meanL0 in (1, width*0.5), and that >0 tokens were selected per bio (no all-dropped rows). Print 3 example bios + their top firing latents (logit-lens sanity that an 'occupation'-ish latent appears).
    3. PARENT/HOLE SMOKE (GPU, ~3-5 min): encode ~2,000 bios (4 professions incl. a likely-distinct one e.g. nurse/surgeon/attorney/poet) + 1,000 negatives. Run parent identification + the per-profession hole table on this mini set. Confirm: an anchor is found with recall>0.6 + firing-floor>5%; the hole table is populated for all 4; the S-rec/S-prec/S-mag selectors + RE-k baselines + AUC-diff CIs execute without shape errors. Eyeball whether any hole>0.5 appears.
    4. PART 2/3 SMOKE (CPU, ~5 min): full taxonomic re-run from cache; assert the homograph cross-tab yields exactly {Georgia, Jordan} absorption_type==True and the side-by-side table has Georgia(eligible)/Jordan(descriptive n=124)/US(co-firing) rows with AUC-diff CIs present.
    5. FULL RUN: encode the full (or capped ~12-16k) bios + 5k negatives; run all three parts; B_auc>=10,000, B_draws=1000. Watch logs for: encode FVU/meanL0 per family, anchor recall + firing-floor, count of professions with absorption_type, any set_cover_established, and the final verdict line.
    6. OUTPUT VALIDATION: aii-json validate method_out.json vs exp_gen_sol_out; generate + validate mini/preview; confirm each file < 100MB (split per aii-file-size-limit if needed). Spot-check that per-row predict_* fields are present and the hole_table has all 28 professions.
  CONFIRMATION SIGNALS before trusting the full run: smoke invariants pass (rung 1), FVU<0.6 on bios (rung 2), hole table populated + CIs computed (rung 3), Georgia/Jordan cross-tab reproduced (rung 4). If rung-1 invariants fail, the cache copy or function reuse is broken — fix before proceeding. If FVU>=0.6 on bios, the layer/pooling is wrong — re-check determine_layer_idx and the whole-text position selection.
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

--- Dependency 4 ---
id: art_21JWypIydPMX
type: dataset
title: CCRG supporting sentiment/aspect families + bias_in_bios boundary-null dataset
summary: >-
  Three REAL, human-annotated datasets standardized into the CCRG shared minimal-pair schema and emitted in the canonical
  exp_sel_data_out format ({metadata, datasets:[{dataset, examples:[{input, output, metadata_*}]}]}), ONE example per text
  row, grouped by dataset, $0 LLM spend. Families (separable via metadata_family): (1) sentiment = CAD-IMDB (Kaushik et al.
  ICLR 2020), 4,880 rows / 2,440 human counterfactual content-flip pairs (positive<->negative), supporting; (2) restaurant_aspect
  = CEBaB (Abraham et al. NeurIPS 2022), 5,682 rows / 2,841 pairs (food 1,740 + service 1,101) flipping ONE aspect's sentiment
  with all four aspect majorities (food/service/ambiance/noise) + binarized review_sentiment retained as INDEPENDENT sub_context
  labels, supporting; (3) bias_in_bios_boundary = LabHC/bias_in_bios (De-Arteaga et al. 2019), 20,177 profession bios (28
  classes, gender as independent sub-context), the PRE-REGISTERED boundary-null where habitat~=label. Total 30,739 rows, 5,281
  reconstructable minimal pairs. Per row: input(text), output(canonical label), and metadata_* fields: id, family, dataset_source,
  concept(sentiment|food_sentiment|service_sentiment|profession), concept_label, sub_context(dict), pair_id, partner_id, pair_role(content_on|content_off|null),
  flip_type(content|null), is_content_pair, is_surface_pair(false for all), fold(train|dev|test), meta(raw fields incl char_len,
  token_overlap_with_partner, raw labels, subsample seed). Every (x_off,x_on) content pair is reconstructable via pair_id/partner_id
  (content_on=positive/concept-present member). is_surface_pair=false everywhere — surface flips are out of scope here (reserved
  for sibling ParaDetox/LLM artifacts); no surface pairs fabricated. NO derived statistics (MI/probes) computed — raw standardized
  data only. Every row validated against schema.json (jsonschema Draft7) AND full/mini/preview validated against exp_sel_data_out
  (aii-json). THREE plan errors were caught and corrected by empirical verification: (a) CAD-IMDB orig/<->new/ row alignment
  is FALSE (flip_rate~0.50, aligned Jaccard~=random~0.11) — authoritative pairing taken from the repo's combined/paired/*_paired.tsv
  via shared batch_id (true-pair Jaccard 0.816 vs random 0.108); (b) CEBaB edit_type is the edited ASPECT {food,service,ambiance,noise}
  and edit_goal is the target sentiment (the plan swapped them), and review_majority is a 1-5 star rating (binarized 1,2->neg
  / 4,5->pos / 3->neutral); (c) bias_in_bios ships no ClassLabel names, so the canonical 28-occupation alphabetical mapping
  (incl 'dj' at index 8) was verified empirically 17/17 by keyword hit-rate (nurse=13, attorney=2, surgeon=25, software_engineer=24,
  yoga_teacher=27), gender 0=male/1=female confirmed by pronouns; stratified (profession x gender, 56 strata) capped subsample
  with fixed seed 20240617, gender-balanced (male 10,054 / female 10,123). Licenses: CAD Apache-2.0, CEBaB CC-BY-4.0, bias_in_bios
  MIT. Reproduce all deliverables with `uv run data.py`. Downstream guidance: compute per-family bootstrap CIs as primary
  (families cleanly separated); treat any bias_in_bios null as the expected boundary outcome, not method failure; build content
  (x_off,x_on) deltas from pair_id.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_4
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

### [7] SYSTEM-USER prompt · 2026-06-18 03:12:57 UTC

```
<CRITICAL_ERROR>
Some files in your workspace exceed the 100MB size limit for GitHub deployment.

OVERSIZED FILES:
  - cache/lat_bias_w16384_n13843.npz (146.6 MB)

You MUST reduce these files to under 100MB each. Use ONE of these strategies:

=== STRATEGY 1: SPLIT FILES (PREFERRED) ===
Split large files into smaller parts and update code to read them sequentially.

For data files (JSON, JSONL, CSV, Parquet):
1. Split the file into parts under 100MB each:
   - data.jsonl -> data_part_001.jsonl, data_part_002.jsonl, ...
2. Update ALL code that reads this file to handle the split parts
3. Delete the original large file after splitting

=== STRATEGY 2: COMPRESSION (FALLBACK) ===
Only use if splitting is not feasible (e.g., binary files, model weights).

1. Compress the file with gzip
2. Update ALL code to decompress before use
3. Delete the original uncompressed file

=== REQUIRED: UPDATE AND TEST CODE ===
After applying your chosen strategy, you MUST:

1. Find ALL code files that reference the modified files (use grep/search)
2. Update each file to work with the new format (split parts or compressed)
3. Run the updated code to verify it still works correctly
4. Fix any errors that occur until the code runs successfully

Do NOT skip testing - the code must actually execute without errors.

Start by listing the oversized files with `ls -lh`, then apply the appropriate strategy.
</CRITICAL_ERROR>
```
