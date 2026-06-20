# gen_art_experiment_5 — test_idea

> Phase: `invention_loop` · round 4 · `gen_art`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_experiment_5` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-17 21:59:14 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_5`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_5/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_5/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_5/results/out.json`
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
id: gen_plan_experiment_5_idx5
type: experiment
title: >-
  M6: A-Priori SAE Firing-Structure Router as a Screening Heuristic with Measured Error (combined firing-Jaccard AND recall-hole
  rule; derivation vs expanded truly-prospective)
summary: >-
  GPU experiment that re-presents the iter-3 a-priori firing-structure router (gen_art_experiment_4/method.py) so it LEADS
  with the COMBINED rule (predict absorption-regime iff firing-Jaccard < tau_J AND parent recall-hole > tau_h), reports the
  12 DERIVATION concepts (rule-fitting, tau sweeps, balanced-acc, LOO) STRICTLY SEPARATELY from the TRULY-PROSPECTIVE concepts,
  EXPANDS the prospective set at $0 by carving new truly-held-out concepts from datasets already in hand (bias_in_bios profession
  concepts + civil_comments severe_toxicity, on top of the existing sentiment/CEBaB-food/CEBaB-service), and frames the router
  as a screening heuristic with a measured error rate (prospective hit-rate + Wilson CI, LOO=0.733) rather than a validated
  oracle. Heavily reuses the frozen iter-3 SAE pipeline and (where the build is unchanged) its on-disk encoding cache to stay
  well within budget.
runpod_compute_profile: gpu
implementation_pseudocode: |-
  LANGUAGE: Python 3.12, uv. SAE/model exactly as iter-3 (FROZEN, $0 LLM): SAE=google/gemma-scope-2b-pt-res layer_12/width_16k/average_l0_82 (JumpReLU, firing:=encode>0), MODEL=unsloth/gemma-2-2b, residual via forward hook on model.model.layers[12] (==blocks.12.hook_resid_post), SEED=1234, DEVICE=cuda. This is M6 of the iter-4 mandate; it is NOT load-bearing (auditability is) but must reproduce honestly.

  =================== STEP 0  SETUP / REUSE ===================
  - Read the iter-3 router VERBATIM first: /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_4/method.py (1256 lines). START THIS ARTIFACT FROM A COPY of it into this workspace as method.py, then EXTEND. Reuse UNCHANGED (do not reimplement): JumpReLUSAE, load_sae, Encoder(_hook, gating_check, encode_token, encode_sentence, _target_positions), identify_parent, per_subcontext, firing_jaccard, ktrack_lite_unit, attribution_pool_h, best_latent_a, nonsae_probe_score, run_outcome/_outcome_core, lr_score, cols_auc, _rankdata, boot_ci, paired_bootstrap_auc_delta, maxpool_z, _split, _fold01, _fold01t, build_spelling, build_nonspell, build_toxicity, run_toxicity_concepts, build_support_sentiment, build_support_aspect, cached_build, set_mem_limits. Keep all CONFIG pins/thresholds (PREC_FLOOR 0.70, JACCARD_MAX 0.10, COVGAIN_FLOOR 0.05, PARENT_FIRE_FLOOR 0.20, K_MAX 8, MIN_SUB_TOKEN 12, MIN_SUB_SENT 150, MIN_OUTCOME 120, N_SHUFFLE 1000, B_BOOT 10000, B_JAC 2000).
  - pyproject.toml: copy iter-3's (torch+cuda, transformers, huggingface_hub, scikit-learn, numpy, scipy, loguru). If the iter-3 .venv is reusable, point at it; else `uv sync`. Do NOT print torch/cuda build strings into the paper output (M8: strip infra scaffolding) — keep them in logs only.
  - DATA paths (READ-ONLY full_data_out.json) exactly as iter-3 DATA dict: spelling=gen_art_dataset_1, nonspell=gen_art_dataset_2, toxicity=gen_art_dataset_3, support=gen_art_dataset_4 (all under iter_1/gen_art).
  - COMPUTE-SAVER (important for 6h budget): copy iter_3/.../gen_art_experiment_4/cache/build_*_full_v5.pkl into this workspace's cache/ and KEEP CACHE_VER='v5' for every UNCHANGED builder (spelling L/O/T/I/D, numeric, taxonomic, toxicity, sentiment, aspect_food, aspect_service) so their expensive forward passes are cache-HITs. Only the NEW builders compute fresh encodings. If a cache load fails or shape-mismatches, fall through to recompute (cached_build already does this).
  - gating_check on ~8 real sentences; assert recon_cos_mean>0.90 (iter-3 got 0.927). Log L0 mean/median. --smoke also asserts BOS-offset correctness via encode_token check_ids on a few spelling corpus rows (token-id mismatch count ~0).

  =================== STEP 1  CONCEPT REGISTRY ===================
  DERIVATION (12, thresholds fit ONLY here): spelling_{L,O,T,I,D}, numeric, taxonomic, toxicity_{threat,identity_attack,insult,obscene,sexual_explicit}.
  PROSPECTIVE_EXISTING (3): sentiment, aspect_food, aspect_service.
  PROSPECTIVE_NEW (~7-9, all TRULY held out): profession_{X} for the top ~8 bias_in_bios professions by subsample count (build below) + toxicity_severe_toxicity (the one civil_comments sub-attribute NOT used in derivation; descriptive_only/underpowered -> flag, still predict+measure).
  RULE: tau_J, tau_h are derived on DERIVATION ONLY, then FROZEN before any prospective concept's predicted_regime is computed. In code, compute+log every prospective concept's predicted_regime (from frozen taus) BEFORE calling its run_outcome (the measurement), to make the prospective ordering auditable.

  =================== STEP 2  NEW BUILDER: bias_in_bios professions ===================
  def build_support_profession(which, enc, scale):
    - g = the bias_in_bios dataset group in DATA['support'] (match dataset name containing 'bias_in_bios'). FIRST inspect: print sorted(g[0].keys()) and a sample to confirm exact flattened keys for profession label and gender sub-context (summary says metadata_concept=='profession', metadata_concept_label==the profession, metadata_sub_context is a dict {gender:...}; in the flat schema gender may appear as metadata_sub_context_gender or inside metadata_sub_context). Adapt key access to what is actually present; fall back to parsing output (canonical label) for the profession and meta raw fields for gender (0=male,1=female per summary).
    - profession universe + counts: tally label frequencies; pick PROFS = top ~8 with >=200 bios AND both genders present (e.g. professor, physician, attorney, journalist, photographer, nurse, psychologist, surgeon, dentist, software_engineer, teacher). Log the chosen list + counts.
    - pos = bios with label==which (cap full=600, mini=120, smoke=20); neg = random sample of bios with label!=which, size-matched to pos (cap full=600). on=pos bios; off=neg bios randomly index-paired to pos (equal length) -> PSEUDO-PAIRS for identify_parent (unpaired diff-of-means contrast; sign-flip null still valid as a within-row randomization).
    - encode_sentence(on, want_resid=True), encode_sentence(off, want_resid=True), pos_lat=on_lat, neg_lat=off_lat.
    - pos_sub = gender label per pos bio (2 sub-contexts: 'male'/'female') -> recall-hole tests whether the profession parent fires on one gender but not the other (boundary-null expectation: ~0 hole -> co_firing).
    - fold via metadata_fold (train->0 else 1).
    - return dict(name='profession_%s'%which, granularity='sentence', kind='prospective', on_lat, off_lat, pos_lat, pos_sub, pos_fold(zeros), neg_lat, neg_fold(zeros), star_pos_lat=on_lat, star_pos_fold=fold, star_pos_resid=on_res, star_neg_lat=off_lat, star_neg_fold=fold, star_neg_resid=off_res, min_sub=MIN_SUB_SENT, s_star=which). Shape MATCHES build_support_aspect so run_concept/run_outcome work unchanged.
  Note: bias_in_bios is the pre-registered BOUNDARY-NULL; predicting co_firing here and confirming it is a VALID prospective hit (not a method failure). Do not over-engineer; if a profession has no content-responsive parent above null, mark parent_unresolved and still report (predicted co_firing by default since recall-hole machinery yields ~0 hole).

  severe_toxicity: extend build_toxicity's sub_lab dict / run_toxicity_concepts loop to ALSO emit 'severe_toxicity' from metadata_subcontext_labels (re-use the already-cached civil_comments encodings; no new forward pass). Flag descriptive_only if positives<MIN_SUB_SENT; if the outcome slice is underpowered, pool concept-wide and mark low-power. Mark kind='prospective'.

  =================== STEP 3  PER-CONCEPT PIPELINE (reuse run_concept) ===================
  For every concept (12 derivation + existing 3 + new): via run_concept (token/sentence builders) or run_toxicity_concepts (the 5 derivation tox + severe_toxicity):
    - identify_parent -> parent, responsive set, precision, pos_fire_rate (parent-validation floor fixes letter-I spurious 0%-corpus anchor).
    - per_subcontext -> per-sub detector (best-AUC non-parent latent), parent recall_hole=1-parent_recall, positive-only firing-Jaccard(detector,parent) + bootstrap CI. Aggregate jaccard_median/min/max and recall_hole_max.
    - run_outcome -> _outcome_core: build LABEL-FREE ktrack_lite unit on parent's TRAIN-positive holes; baselines (a) best raw latent, (h) count-matched standardized-diff-of-means attribution pool, (d) non-SAE residual diff-of-means probe; LR head held constant; held-out TEST AUCs auc_unit/auc_a/auc_h/auc_d; paired-bootstrap delta_vs_a (+CI) AND delta_vs_h (+CI).
    - GROUND-TRUTH REGIME: PRIMARY (iter-3-consistent, makes derivation reproduce) = 'absorption' if (auc_unit-auc_a)>0 else 'co_firing'. ALSO store delta_vs_h, delta_vs_h_ci and a SECONDARY regime label = 'absorption' if (auc_unit-auc_h)>0 else 'co_firing'. Report BOTH so the reader sees the contrast dependence (objective says measure unit-vs-(h)/(a)). honest_notes must state: general-classification (h) frequently beats the unit even in known absorption regimes (the absorption SELECTION advantage lives on the absorbed-slice recall, not general classification), which is WHY the primary 'grouping-helps' signal is vs-(a) here.

  =================== STEP 4  ROUTER DERIVATION (DERIVATION CONCEPTS ONLY) ===================
  J=[jaccard_median], H=[recall_hole_max], Y=[primary ground_truth_regime] over the 12 derivation concepts (absorption=positive class).
  (1) JACCARD-ALONE router: sweep tau_J in linspace(0.02,0.35,34); predict absorption iff J<tau_J; balanced-acc; report best tau_J* and balanced-acc (expect ~0.917). Note it MISLABELS numeric (high J yet absorption-like) and aggregated-taxonomic (low J yet co-firing).
  (2) RECALL-HOLE-ALONE router: sweep tau_h in linspace(0.0,0.95,40); predict absorption iff H>tau_h; balanced-acc; report best tau_h* (expect ~1.0). EXPLICITLY note this is the STRONGEST SINGLE separator -> headline must be the conjunction (not jaccard alone), per objective.
  (3) COMBINED router (LEAD): 2-D grid over (tau_J,tau_h); predict absorption iff J<tau_J AND H>tau_h; pick (tau_J*,tau_h*) maximizing balanced-acc (tie-break: larger margin = min co_firing score minus max absorption score region). Report balanced-acc + thresholds. If the grid degenerates to tau_h=0 (recall-hole non-binding, as in iter-3), REPORT that transparently and additionally report a 'recall-hole-primary' variant; do not hide it.
  LOO: leave-one-derivation-concept-out; refit each rule's tau on the N-1; predict held-out; report loo_accuracy per rule (combined PRIMARY; expect ~0.733). Emit loo_per_concept rows (concept, tau_fold, pred, ground_truth, hit).
  COUNTEREXAMPLES (compute + log explicitly): numeric -> jaccard high but absorption-like; taxonomic -> jaccard low but parent already ~0.95 recall / ~0 hole so combined correctly routes co_firing. These justify the conjunction.

  =================== STEP 5  EXPANDED PROSPECTIVE TEST (frozen combined rule) ===================
  Freeze (tau_J*,tau_h*) from STEP 4. For EACH prospective concept (existing 3 + new), in this order in code: (a) compute+log predicted_regime = 'absorption' if J<tau_J* AND H>tau_h* else 'co_firing'; (b) THEN run_outcome -> ground_truth_regime (primary vs-a; also vs-h); (c) hit = predicted==ground_truth.
  Report THREE prospective hit-rates with Wilson 95% CIs: existing-3 only, new-only, and combined-all. Primary = combined-all under vs-a ground-truth; ALSO report combined-all under vs-h ground-truth as a robustness row. Tabulate per concept: name, kind, jaccard_median, recall_hole_max, predicted_regime, ground_truth_regime(vs-a), ground_truth_regime_vs_h, auc_unit/a/h/d, delta_vs_a+CI, delta_vs_h+CI, hit, power_flag(descriptive_only for severe_toxicity / low-n).
  FRAMING (objective M6): describe router as 'screening heuristic with substantial measured error'; report prospective error rate (1-hitrate) and LOO; NEVER label the 12 derivation concepts as prospective; NEVER claim 'validated prospectively across spelling/taxonomic/toxicity/sentiment/aspect' (first three ARE derivation).

  =================== STEP 6  REPRODUCTION / SANITY ===================
  - Assert spelling jaccard_median all < 0.05 (sanity; iter-3: L .017,O .039(>.05! report actual, do not hard-fail),T .003,I .008,D .017 -> use threshold <0.05 as 'most letters', report the per-letter values and flag O). Use a soft check: report spelling_all_below_0_1 (true) and list values.
  - Recompute toxicity threat/identity_attack/insult firing-Jaccard; report values + the iter-3 'reference' (.40/.29/.66) and a within_tol flag (do NOT hard-fail; iter-3's recomputed values differed from reference and that is itself reported honestly).

  =================== STEP 7  OUTPUT (exp_gen_sol_out schema) ===================
  Write method_out.json with metadata{ method_name, description, sae_release/sae_id/hook/model/seed/scale, gating, firing_convention, combined_rule:{tau_j,tau_h,balanced_acc,definition_string}, single_signal_ablations:{jaccard_alone:{tau,balanced_acc}, recall_hole_alone:{tau,balanced_acc}}, loo:{combined_acc, per_concept[]}, derivation_table:[per derivation concept: concept, jaccard_median/min/max, recall_hole_max, parent_latent, n_subcontexts, ground_truth_regime, predicted_regime(at frozen tau, for display), outcome aucs+deltas+CIs], prospective_table:[expanded; per concept predicted_regime, ground_truth_regime(vs-a)+(vs-h), aucs, delta_vs_a+CI, delta_vs_h+CI, hit, power_flag], prospective_hitrate:{existing3, new_only, combined_all, combined_all_vs_h} each {hits,n,rate,wilson_ci}, per_concept_firing_jaccard:[detector/recall_hole detail], reproduction_check:{spelling values+flag, toxicity values+reference+within_tol}, honest_notes:[...] }. datasets:[{dataset:'m6_router_concepts', examples:[ONE row per concept = a router decision card: input='Concept X (granularity, derivation|prospective): parent L, firing-Jaccard median=..., recall-hole max=.... Route to absorption-repair (CCRG) or marginal attribution?', output=ground_truth_regime, predict_router=predicted_regime, metadata_* mirroring all fields above]}].
  honest_notes MUST include: derivation!=prospective separation; recall-hole-alone is strongest single signal; combined rule is the recommendation; jaccard-alone mislabels numeric+aggregated-taxonomic; prospective hit-rate is the MEASURED error; bias_in_bios is a boundary-null (co_firing predicted+confirmed is a valid hit); regime label depends on vs-(a) vs vs-(h) contrast and general-classification (h) is not the absorbed-slice; severe_toxicity underpowered.
  - aii-json: validate full_method_out.json against exp_gen_sol_out; generate mini_method_out.json + preview_method_out.json; assert all three <100MB (this output is tiny KB-scale).

  =================== STEP 8  GRADUAL SCALING / MEM SAFETY ===================
  set_mem_limits(); --smoke (load+gating+BOS assert+1 concept/family, schema-validate tiny) -> --scale mini (~6 concepts incl 1 new profession + severe_toxicity; verify reproduction signals + combined-rule fit + prospective predict/measure) -> --scale full (all). Encodings via cached_build (reuse v5 cache for unchanged builders; new builders compute fresh). torch.cuda.empty_cache() between concept families; del large arrays; batch encode_token/encode_sentence at iter-3 sizes (64/48). All randomness seeded 1234.
fallback_plan: >-
  GPU OOM / slow: lower encode batch (64->32, 48->24); cut full caps for professions (600->300) and N_SHUFFLE/B_BOOT only
  if time-bound (keep B_BOOT>=2000 for CIs); process one concept family at a time freeing GPU between. If model/SAE download
  or gating fails: it is the SAME pipeline iter-3 ran successfully, so retry hf_hub_download with HF_TOKEN; as last resort
  copy iter-3 cached encodings and run analysis-only (firing-Jaccard/recall-hole/router are pure-numpy on cached latents)
  — the router can be fully recomputed WITHOUT the GPU from cached build_*.pkl. If bias_in_bios professions yield no content-responsive
  parent above null (pseudo-pairs too weak): (i) increase neg sample size and re-pair; (ii) fall back to fewer professions
  (>=4); (iii) if still unresolved, report them as parent_unresolved=co_firing-by-default and keep them as boundary-null prospective
  points with a caveat — still strengthens the prospective n. If severe_toxicity has <30 positives even at threshold 0.3:
  keep it descriptive_only, pool concept-wide for the outcome, and exclude from the headline hit-rate but report it in a descriptive
  row. If the COMBINED 2-D grid degenerates to tau_h=0 (recall-hole adds nothing on derivation, as iter-3 found): do not force
  it — report the degeneracy honestly, LEAD with the combined rule as recommended but state recall-hole-alone (balanced-acc
  ~1.0) is the strongest single separator, and present the conjunction as the conservative screen. If expanding prospective
  concepts still leaves n small (<10): report Wilson CI honestly (wide) and frame as 'measured error on a still-small prospective
  set'; the contribution is the SEPARATION + measured error, not a tight estimate. If the cache from iter-3 is incompatible
  (CACHE_VER/shape): bump to v6 and recompute all (fits in 6h: derivation forward passes are ~the bulk; mini-first validates
  timing). If any new prospective concept's outcome AUCs are degenerate (single-class test fold): widen fold to random 70/30
  (the _split helper already does this when folds unusable). NEVER hard-fail on reproduction-tolerance mismatches (spelling_O
  jaccard ~0.039, toxicity values differing from the .40/.29/.66 reference) — report actuals + flags; the honest discrepancy
  is itself a result.
testing_plan: |-
  1) SMOKE (`uv run method.py --smoke`, target <8 min): assert model+SAE load; gating recon_cos_mean>0.90 and L0 median in ~50-90; encode_token BOS-offset check (token-id mismatches ~0 on spelling corpus); run ONE concept per family (spelling_L, toxicity_threat, sentiment, and ONE profession) end-to-end producing parent + jaccard + recall_hole + outcome; assert a tiny method_out validates against exp_gen_sol_out. CONFIRM the new build_support_profession reads bias_in_bios keys correctly (log the resolved profession/gender key names + chosen PROFS list + counts).
  2) MINI (`--scale mini`, target <30 min, leans on v5 cache): run ~6 concepts (spelling_L/O/T or all 5, numeric, toxicity_insult, sentiment, 1 profession, severe_toxicity). CONFIRMATION SIGNALS before going full: (a) spelling jaccard_median < 0.05 (O may be ~0.039, list values); (b) toxicity jaccard_median > 0.3 for threat/insult (co-firing pole); (c) derivation jaccard-alone balanced-acc ~0.90 and recall-hole-alone ~1.0; (d) combined-rule (tau_J*,tau_h*) selected with balanced-acc reported; (e) LOO computed and ~0.7; (f) prospective table populated with predicted_regime computed BEFORE outcome (check log ordering), ground_truth (vs-a AND vs-h), hit flags, Wilson CIs; (g) profession concepts predict co_firing (boundary-null) and most confirm. If spelling jaccard is NOT <0.05 or toxicity NOT >0.3, STOP and debug parent identification / encoding (likely a key-mapping or cache-version bug) before full.
  3) FULL (`--scale full`): all 12 derivation + 3 existing + ~7-9 new prospective. Verify: derivation table has exactly 12 rows and is labeled derivation (never prospective); prospective table has existing-3 + new separated AND combined hit-rates with CIs; reproduction_check present with actuals+flags (no hard-fail); honest_notes contains the required disclosures (derivation/prospective separation, recall-hole strongest single, combined=recommendation, jaccard-alone counterexamples numeric+taxonomic, measured prospective error, boundary-null framing, vs-a/vs-h contrast dependence). Final: aii-json validates full/mini/preview; all <100MB; no rebuttal/iteration/infra scaffolding strings in the JSON metadata (M8). Spot-check 2-3 datasets[].examples rows render as coherent router decision cards. Confirm $0 LLM spend (no OpenRouter calls).
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
id: art_8QO7pl6Pd8UQ
type: dataset
title: 'Two-Track CCRG Toxicity Family: ParaDetox flips + civil_comments sub-contexts'
summary: >-
  A single schema-standardized TOXICITY dataset family for the Two-Track CCRG experiments (organizing SAE latents into reliable
  group-level units). 37,707 examples in the exp_sel_data_out schema, grouped into the two real source corpora and validated.
  THE BEST 2 DATASETS are the dataset groups: (1) paradetox = s-nlp/paradetox (Logacheva et al., ACL 2022; openrail++), 19,096
  rows; (2) civil_comments = google/civil_comments (Jigsaw Unintended Bias, Borkan et al. 2019; CC0 1.0), 18,611 rows. Three
  role-distinct components are carried via metadata_record_type: (a) content_pair (18,853) = human toxic<->neutral parallel
  sentences, the NON-CIRCULAR content perturbation P (metadata_text_on / metadata_text_off) for per-latent content-response;
  (b) surface_pair (546) = OpenRouter gpt-4o-mini toxic->toxic paraphrases (input / metadata_text_paired), double-gated (token
  Jaccard<0.6 AND norm edit-dist>0.25 AND LLM-judge toxicity_preserved+meaning_preserved; judge pass 70.6%, refusal 1.5%,
  cost $0.060), the surface-invariance control, folded into their seed corpus's group via metadata_origin_source; (c) classification
  (18,308) = civil_comments comments with a binary metadata_toxicity_label plus FROZEN multi-label sub-context labels (severe_toxicity,
  obscene, threat, insult, identity_attack, sexual_explicit) thresholded at 0.5 from the raw annotator-fraction floats (preserved
  in metadata_subcontext_floats for re-thresholding). Power: obscene/threat/insult/identity_attack/sexual_explicit are inferential@0.5
  with >=150 positives in every eval fold; severe_toxicity is flagged descriptive_only (too rare even at 0.3) -- not silently
  dropped. data_summary.json reports per-sub-context per-fold counts at 0.5 and 0.3, the sub-attribute pairwise Jaccard co-occurrence
  matrix (insult<->obscene ~0.245 shared-support => C-track; threat/identity_attack <0.05 disjoint => K-track), generation
  stats, and 316 reconciled cross-source collisions. Leakage-safe doc-level folds (metadata_fold in train/val/test) via union-find
  over normalized text: civil_comments keeps native splits; verified 0 pair_id and 0 source_sentence_id spanning folds and
  0 normalized texts in >1 fold. Sanity baselines (TF-IDF+logistic regression, train->test): toxicity AUC 0.851/F1 0.773;
  sub-contexts AUC 0.81-0.94; content_pair mean cos 0.685 (genuine flip), surface_pair 0.355 (reworded not copied). Files:
  data.py (stdlib-only uv assembler), full/mini/preview_data_out.json (validated), data_summary.json, README.md, pyproject.toml
  (47 pinned deps), and build/ (staged pipeline: ParaDetox content-flips, civil_comments stream-filter, OpenRouter surface
  generation, assembler, verify_baseline). Downstream consumers flatten datasets[*].examples and filter metadata_record_type.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_3
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

--- Dependency 5 ---
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

### [2] HUMAN-USER prompt · 2026-06-17 21:59:14 UTC

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

### [3] SKILL-INPUT — aii-python · 2026-06-17 21:59:36 UTC

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

### [4] SKILL-INPUT — aii-long-running-tasks · 2026-06-17 21:59:36 UTC

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

### [5] SKILL-INPUT — aii-use-hardware · 2026-06-17 21:59:36 UTC

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

### [6] SKILL-INPUT — aii-json · 2026-06-17 22:09:02 UTC

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

### [7] SKILL-INPUT — aii-file-size-limit · 2026-06-17 22:09:02 UTC

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

### [8] SYSTEM-USER prompt · 2026-06-18 00:48:33 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_5`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_5/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_5/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_5/results/out.json`
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
id: gen_plan_experiment_5_idx5
type: experiment
title: >-
  M6: A-Priori SAE Firing-Structure Router as a Screening Heuristic with Measured Error (combined firing-Jaccard AND recall-hole
  rule; derivation vs expanded truly-prospective)
summary: >-
  GPU experiment that re-presents the iter-3 a-priori firing-structure router (gen_art_experiment_4/method.py) so it LEADS
  with the COMBINED rule (predict absorption-regime iff firing-Jaccard < tau_J AND parent recall-hole > tau_h), reports the
  12 DERIVATION concepts (rule-fitting, tau sweeps, balanced-acc, LOO) STRICTLY SEPARATELY from the TRULY-PROSPECTIVE concepts,
  EXPANDS the prospective set at $0 by carving new truly-held-out concepts from datasets already in hand (bias_in_bios profession
  concepts + civil_comments severe_toxicity, on top of the existing sentiment/CEBaB-food/CEBaB-service), and frames the router
  as a screening heuristic with a measured error rate (prospective hit-rate + Wilson CI, LOO=0.733) rather than a validated
  oracle. Heavily reuses the frozen iter-3 SAE pipeline and (where the build is unchanged) its on-disk encoding cache to stay
  well within budget.
runpod_compute_profile: gpu
implementation_pseudocode: |-
  LANGUAGE: Python 3.12, uv. SAE/model exactly as iter-3 (FROZEN, $0 LLM): SAE=google/gemma-scope-2b-pt-res layer_12/width_16k/average_l0_82 (JumpReLU, firing:=encode>0), MODEL=unsloth/gemma-2-2b, residual via forward hook on model.model.layers[12] (==blocks.12.hook_resid_post), SEED=1234, DEVICE=cuda. This is M6 of the iter-4 mandate; it is NOT load-bearing (auditability is) but must reproduce honestly.

  =================== STEP 0  SETUP / REUSE ===================
  - Read the iter-3 router VERBATIM first: /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_4/method.py (1256 lines). START THIS ARTIFACT FROM A COPY of it into this workspace as method.py, then EXTEND. Reuse UNCHANGED (do not reimplement): JumpReLUSAE, load_sae, Encoder(_hook, gating_check, encode_token, encode_sentence, _target_positions), identify_parent, per_subcontext, firing_jaccard, ktrack_lite_unit, attribution_pool_h, best_latent_a, nonsae_probe_score, run_outcome/_outcome_core, lr_score, cols_auc, _rankdata, boot_ci, paired_bootstrap_auc_delta, maxpool_z, _split, _fold01, _fold01t, build_spelling, build_nonspell, build_toxicity, run_toxicity_concepts, build_support_sentiment, build_support_aspect, cached_build, set_mem_limits. Keep all CONFIG pins/thresholds (PREC_FLOOR 0.70, JACCARD_MAX 0.10, COVGAIN_FLOOR 0.05, PARENT_FIRE_FLOOR 0.20, K_MAX 8, MIN_SUB_TOKEN 12, MIN_SUB_SENT 150, MIN_OUTCOME 120, N_SHUFFLE 1000, B_BOOT 10000, B_JAC 2000).
  - pyproject.toml: copy iter-3's (torch+cuda, transformers, huggingface_hub, scikit-learn, numpy, scipy, loguru). If the iter-3 .venv is reusable, point at it; else `uv sync`. Do NOT print torch/cuda build strings into the paper output (M8: strip infra scaffolding) — keep them in logs only.
  - DATA paths (READ-ONLY full_data_out.json) exactly as iter-3 DATA dict: spelling=gen_art_dataset_1, nonspell=gen_art_dataset_2, toxicity=gen_art_dataset_3, support=gen_art_dataset_4 (all under iter_1/gen_art).
  - COMPUTE-SAVER (important for 6h budget): copy iter_3/.../gen_art_experiment_4/cache/build_*_full_v5.pkl into this workspace's cache/ and KEEP CACHE_VER='v5' for every UNCHANGED builder (spelling L/O/T/I/D, numeric, taxonomic, toxicity, sentiment, aspect_food, aspect_service) so their expensive forward passes are cache-HITs. Only the NEW builders compute fresh encodings. If a cache load fails or shape-mismatches, fall through to recompute (cached_build already does this).
  - gating_check on ~8 real sentences; assert recon_cos_mean>0.90 (iter-3 got 0.927). Log L0 mean/median. --smoke also asserts BOS-offset correctness via encode_token check_ids on a few spelling corpus rows (token-id mismatch count ~0).

  =================== STEP 1  CONCEPT REGISTRY ===================
  DERIVATION (12, thresholds fit ONLY here): spelling_{L,O,T,I,D}, numeric, taxonomic, toxicity_{threat,identity_attack,insult,obscene,sexual_explicit}.
  PROSPECTIVE_EXISTING (3): sentiment, aspect_food, aspect_service.
  PROSPECTIVE_NEW (~7-9, all TRULY held out): profession_{X} for the top ~8 bias_in_bios professions by subsample count (build below) + toxicity_severe_toxicity (the one civil_comments sub-attribute NOT used in derivation; descriptive_only/underpowered -> flag, still predict+measure).
  RULE: tau_J, tau_h are derived on DERIVATION ONLY, then FROZEN before any prospective concept's predicted_regime is computed. In code, compute+log every prospective concept's predicted_regime (from frozen taus) BEFORE calling its run_outcome (the measurement), to make the prospective ordering auditable.

  =================== STEP 2  NEW BUILDER: bias_in_bios professions ===================
  def build_support_profession(which, enc, scale):
    - g = the bias_in_bios dataset group in DATA['support'] (match dataset name containing 'bias_in_bios'). FIRST inspect: print sorted(g[0].keys()) and a sample to confirm exact flattened keys for profession label and gender sub-context (summary says metadata_concept=='profession', metadata_concept_label==the profession, metadata_sub_context is a dict {gender:...}; in the flat schema gender may appear as metadata_sub_context_gender or inside metadata_sub_context). Adapt key access to what is actually present; fall back to parsing output (canonical label) for the profession and meta raw fields for gender (0=male,1=female per summary).
    - profession universe + counts: tally label frequencies; pick PROFS = top ~8 with >=200 bios AND both genders present (e.g. professor, physician, attorney, journalist, photographer, nurse, psychologist, surgeon, dentist, software_engineer, teacher). Log the chosen list + counts.
    - pos = bios with label==which (cap full=600, mini=120, smoke=20); neg = random sample of bios with label!=which, size-matched to pos (cap full=600). on=pos bios; off=neg bios randomly index-paired to pos (equal length) -> PSEUDO-PAIRS for identify_parent (unpaired diff-of-means contrast; sign-flip null still valid as a within-row randomization).
    - encode_sentence(on, want_resid=True), encode_sentence(off, want_resid=True), pos_lat=on_lat, neg_lat=off_lat.
    - pos_sub = gender label per pos bio (2 sub-contexts: 'male'/'female') -> recall-hole tests whether the profession parent fires on one gender but not the other (boundary-null expectation: ~0 hole -> co_firing).
    - fold via metadata_fold (train->0 else 1).
    - return dict(name='profession_%s'%which, granularity='sentence', kind='prospective', on_lat, off_lat, pos_lat, pos_sub, pos_fold(zeros), neg_lat, neg_fold(zeros), star_pos_lat=on_lat, star_pos_fold=fold, star_pos_resid=on_res, star_neg_lat=off_lat, star_neg_fold=fold, star_neg_resid=off_res, min_sub=MIN_SUB_SENT, s_star=which). Shape MATCHES build_support_aspect so run_concept/run_outcome work unchanged.
  Note: bias_in_bios is the pre-registered BOUNDARY-NULL; predicting co_firing here and confirming it is a VALID prospective hit (not a method failure). Do not over-engineer; if a profession has no content-responsive parent above null, mark parent_unresolved and still report (predicted co_firing by default since recall-hole machinery yields ~0 hole).

  severe_toxicity: extend build_toxicity's sub_lab dict / run_toxicity_concepts loop to ALSO emit 'severe_toxicity' from metadata_subcontext_labels (re-use the already-cached civil_comments encodings; no new forward pass). Flag descriptive_only if positives<MIN_SUB_SENT; if the outcome slice is underpowered, pool concept-wide and mark low-power. Mark kind='prospective'.

  =================== STEP 3  PER-CONCEPT PIPELINE (reuse run_concept) ===================
  For every concept (12 derivation + existing 3 + new): via run_concept (token/sentence builders) or run_toxicity_concepts (the 5 derivation tox + severe_toxicity):
    - identify_parent -> parent, responsive set, precision, pos_fire_rate (parent-validation floor fixes letter-I spurious 0%-corpus anchor).
    - per_subcontext -> per-sub detector (best-AUC non-parent latent), parent recall_hole=1-parent_recall, positive-only firing-Jaccard(detector,parent) + bootstrap CI. Aggregate jaccard_median/min/max and recall_hole_max.
    - run_outcome -> _outcome_core: build LABEL-FREE ktrack_lite unit on parent's TRAIN-positive holes; baselines (a) best raw latent, (h) count-matched standardized-diff-of-means attribution pool, (d) non-SAE residual diff-of-means probe; LR head held constant; held-out TEST AUCs auc_unit/auc_a/auc_h/auc_d; paired-bootstrap delta_vs_a (+CI) AND delta_vs_h (+CI).
    - GROUND-TRUTH REGIME: PRIMARY (iter-3-consistent, makes derivation reproduce) = 'absorption' if (auc_unit-auc_a)>0 else 'co_firing'. ALSO store delta_vs_h, delta_vs_h_ci and a SECONDARY regime label = 'absorption' if (auc_unit-auc_h)>0 else 'co_firing'. Report BOTH so the reader sees the contrast dependence (objective says measure unit-vs-(h)/(a)). honest_notes must state: general-classification (h) frequently beats the unit even in known absorption regimes (the absorption SELECTION advantage lives on the absorbed-slice recall, not general classification), which is WHY the primary 'grouping-helps' signal is vs-(a) here.

  =================== STEP 4  ROUTER DERIVATION (DERIVATION CONCEPTS ONLY) ===================
  J=[jaccard_median], H=[recall_hole_max], Y=[primary ground_truth_regime] over the 12 derivation concepts (absorption=positive class).
  (1) JACCARD-ALONE router: sweep tau_J in linspace(0.02,0.35,34); predict absorption iff J<tau_J; balanced-acc; report best tau_J* and balanced-acc (expect ~0.917). Note it MISLABELS numeric (high J yet absorption-like) and aggregated-taxonomic (low J yet co-firing).
  (2) RECALL-HOLE-ALONE router: sweep tau_h in linspace(0.0,0.95,40); predict absorption iff H>tau_h; balanced-acc; report best tau_h* (expect ~1.0). EXPLICITLY note this is the STRONGEST SINGLE separator -> headline must be the conjunction (not jaccard alone), per objective.
  (3) COMBINED router (LEAD): 2-D grid over (tau_J,tau_h); predict absorption iff J<tau_J AND H>tau_h; pick (tau_J*,tau_h*) maximizing balanced-acc (tie-break: larger margin = min co_firing score minus max absorption score region). Report balanced-acc + thresholds. If the grid degenerates to tau_h=0 (recall-hole non-binding, as in iter-3), REPORT that transparently and additionally report a 'recall-hole-primary' variant; do not hide it.
  LOO: leave-one-derivation-concept-out; refit each rule's tau on the N-1; predict held-out; report loo_accuracy per rule (combined PRIMARY; expect ~0.733). Emit loo_per_concept rows (concept, tau_fold, pred, ground_truth, hit).
  COUNTEREXAMPLES (compute + log explicitly): numeric -> jaccard high but absorption-like; taxonomic -> jaccard low but parent already ~0.95 recall / ~0 hole so combined correctly routes co_firing. These justify the conjunction.

  =================== STEP 5  EXPANDED PROSPECTIVE TEST (frozen combined rule) ===================
  Freeze (tau_J*,tau_h*) from STEP 4. For EACH prospective concept (existing 3 + new), in this order in code: (a) compute+log predicted_regime = 'absorption' if J<tau_J* AND H>tau_h* else 'co_firing'; (b) THEN run_outcome -> ground_truth_regime (primary vs-a; also vs-h); (c) hit = predicted==ground_truth.
  Report THREE prospective hit-rates with Wilson 95% CIs: existing-3 only, new-only, and combined-all. Primary = combined-all under vs-a ground-truth; ALSO report combined-all under vs-h ground-truth as a robustness row. Tabulate per concept: name, kind, jaccard_median, recall_hole_max, predicted_regime, ground_truth_regime(vs-a), ground_truth_regime_vs_h, auc_unit/a/h/d, delta_vs_a+CI, delta_vs_h+CI, hit, power_flag(descriptive_only for severe_toxicity / low-n).
  FRAMING (objective M6): describe router as 'screening heuristic with substantial measured error'; report prospective error rate (1-hitrate) and LOO; NEVER label the 12 derivation concepts as prospective; NEVER claim 'validated prospectively across spelling/taxonomic/toxicity/sentiment/aspect' (first three ARE derivation).

  =================== STEP 6  REPRODUCTION / SANITY ===================
  - Assert spelling jaccard_median all < 0.05 (sanity; iter-3: L .017,O .039(>.05! report actual, do not hard-fail),T .003,I .008,D .017 -> use threshold <0.05 as 'most letters', report the per-letter values and flag O). Use a soft check: report spelling_all_below_0_1 (true) and list values.
  - Recompute toxicity threat/identity_attack/insult firing-Jaccard; report values + the iter-3 'reference' (.40/.29/.66) and a within_tol flag (do NOT hard-fail; iter-3's recomputed values differed from reference and that is itself reported honestly).

  =================== STEP 7  OUTPUT (exp_gen_sol_out schema) ===================
  Write method_out.json with metadata{ method_name, description, sae_release/sae_id/hook/model/seed/scale, gating, firing_convention, combined_rule:{tau_j,tau_h,balanced_acc,definition_string}, single_signal_ablations:{jaccard_alone:{tau,balanced_acc}, recall_hole_alone:{tau,balanced_acc}}, loo:{combined_acc, per_concept[]}, derivation_table:[per derivation concept: concept, jaccard_median/min/max, recall_hole_max, parent_latent, n_subcontexts, ground_truth_regime, predicted_regime(at frozen tau, for display), outcome aucs+deltas+CIs], prospective_table:[expanded; per concept predicted_regime, ground_truth_regime(vs-a)+(vs-h), aucs, delta_vs_a+CI, delta_vs_h+CI, hit, power_flag], prospective_hitrate:{existing3, new_only, combined_all, combined_all_vs_h} each {hits,n,rate,wilson_ci}, per_concept_firing_jaccard:[detector/recall_hole detail], reproduction_check:{spelling values+flag, toxicity values+reference+within_tol}, honest_notes:[...] }. datasets:[{dataset:'m6_router_concepts', examples:[ONE row per concept = a router decision card: input='Concept X (granularity, derivation|prospective): parent L, firing-Jaccard median=..., recall-hole max=.... Route to absorption-repair (CCRG) or marginal attribution?', output=ground_truth_regime, predict_router=predicted_regime, metadata_* mirroring all fields above]}].
  honest_notes MUST include: derivation!=prospective separation; recall-hole-alone is strongest single signal; combined rule is the recommendation; jaccard-alone mislabels numeric+aggregated-taxonomic; prospective hit-rate is the MEASURED error; bias_in_bios is a boundary-null (co_firing predicted+confirmed is a valid hit); regime label depends on vs-(a) vs vs-(h) contrast and general-classification (h) is not the absorbed-slice; severe_toxicity underpowered.
  - aii-json: validate full_method_out.json against exp_gen_sol_out; generate mini_method_out.json + preview_method_out.json; assert all three <100MB (this output is tiny KB-scale).

  =================== STEP 8  GRADUAL SCALING / MEM SAFETY ===================
  set_mem_limits(); --smoke (load+gating+BOS assert+1 concept/family, schema-validate tiny) -> --scale mini (~6 concepts incl 1 new profession + severe_toxicity; verify reproduction signals + combined-rule fit + prospective predict/measure) -> --scale full (all). Encodings via cached_build (reuse v5 cache for unchanged builders; new builders compute fresh). torch.cuda.empty_cache() between concept families; del large arrays; batch encode_token/encode_sentence at iter-3 sizes (64/48). All randomness seeded 1234.
fallback_plan: >-
  GPU OOM / slow: lower encode batch (64->32, 48->24); cut full caps for professions (600->300) and N_SHUFFLE/B_BOOT only
  if time-bound (keep B_BOOT>=2000 for CIs); process one concept family at a time freeing GPU between. If model/SAE download
  or gating fails: it is the SAME pipeline iter-3 ran successfully, so retry hf_hub_download with HF_TOKEN; as last resort
  copy iter-3 cached encodings and run analysis-only (firing-Jaccard/recall-hole/router are pure-numpy on cached latents)
  — the router can be fully recomputed WITHOUT the GPU from cached build_*.pkl. If bias_in_bios professions yield no content-responsive
  parent above null (pseudo-pairs too weak): (i) increase neg sample size and re-pair; (ii) fall back to fewer professions
  (>=4); (iii) if still unresolved, report them as parent_unresolved=co_firing-by-default and keep them as boundary-null prospective
  points with a caveat — still strengthens the prospective n. If severe_toxicity has <30 positives even at threshold 0.3:
  keep it descriptive_only, pool concept-wide for the outcome, and exclude from the headline hit-rate but report it in a descriptive
  row. If the COMBINED 2-D grid degenerates to tau_h=0 (recall-hole adds nothing on derivation, as iter-3 found): do not force
  it — report the degeneracy honestly, LEAD with the combined rule as recommended but state recall-hole-alone (balanced-acc
  ~1.0) is the strongest single separator, and present the conjunction as the conservative screen. If expanding prospective
  concepts still leaves n small (<10): report Wilson CI honestly (wide) and frame as 'measured error on a still-small prospective
  set'; the contribution is the SEPARATION + measured error, not a tight estimate. If the cache from iter-3 is incompatible
  (CACHE_VER/shape): bump to v6 and recompute all (fits in 6h: derivation forward passes are ~the bulk; mini-first validates
  timing). If any new prospective concept's outcome AUCs are degenerate (single-class test fold): widen fold to random 70/30
  (the _split helper already does this when folds unusable). NEVER hard-fail on reproduction-tolerance mismatches (spelling_O
  jaccard ~0.039, toxicity values differing from the .40/.29/.66 reference) — report actuals + flags; the honest discrepancy
  is itself a result.
testing_plan: |-
  1) SMOKE (`uv run method.py --smoke`, target <8 min): assert model+SAE load; gating recon_cos_mean>0.90 and L0 median in ~50-90; encode_token BOS-offset check (token-id mismatches ~0 on spelling corpus); run ONE concept per family (spelling_L, toxicity_threat, sentiment, and ONE profession) end-to-end producing parent + jaccard + recall_hole + outcome; assert a tiny method_out validates against exp_gen_sol_out. CONFIRM the new build_support_profession reads bias_in_bios keys correctly (log the resolved profession/gender key names + chosen PROFS list + counts).
  2) MINI (`--scale mini`, target <30 min, leans on v5 cache): run ~6 concepts (spelling_L/O/T or all 5, numeric, toxicity_insult, sentiment, 1 profession, severe_toxicity). CONFIRMATION SIGNALS before going full: (a) spelling jaccard_median < 0.05 (O may be ~0.039, list values); (b) toxicity jaccard_median > 0.3 for threat/insult (co-firing pole); (c) derivation jaccard-alone balanced-acc ~0.90 and recall-hole-alone ~1.0; (d) combined-rule (tau_J*,tau_h*) selected with balanced-acc reported; (e) LOO computed and ~0.7; (f) prospective table populated with predicted_regime computed BEFORE outcome (check log ordering), ground_truth (vs-a AND vs-h), hit flags, Wilson CIs; (g) profession concepts predict co_firing (boundary-null) and most confirm. If spelling jaccard is NOT <0.05 or toxicity NOT >0.3, STOP and debug parent identification / encoding (likely a key-mapping or cache-version bug) before full.
  3) FULL (`--scale full`): all 12 derivation + 3 existing + ~7-9 new prospective. Verify: derivation table has exactly 12 rows and is labeled derivation (never prospective); prospective table has existing-3 + new separated AND combined hit-rates with CIs; reproduction_check present with actuals+flags (no hard-fail); honest_notes contains the required disclosures (derivation/prospective separation, recall-hole strongest single, combined=recommendation, jaccard-alone counterexamples numeric+taxonomic, measured prospective error, boundary-null framing, vs-a/vs-h contrast dependence). Final: aii-json validates full/mini/preview; all <100MB; no rebuttal/iteration/infra scaffolding strings in the JSON metadata (M8). Spot-check 2-3 datasets[].examples rows render as coherent router decision cards. Confirm $0 LLM spend (no OpenRouter calls).
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
id: art_8QO7pl6Pd8UQ
type: dataset
title: 'Two-Track CCRG Toxicity Family: ParaDetox flips + civil_comments sub-contexts'
summary: >-
  A single schema-standardized TOXICITY dataset family for the Two-Track CCRG experiments (organizing SAE latents into reliable
  group-level units). 37,707 examples in the exp_sel_data_out schema, grouped into the two real source corpora and validated.
  THE BEST 2 DATASETS are the dataset groups: (1) paradetox = s-nlp/paradetox (Logacheva et al., ACL 2022; openrail++), 19,096
  rows; (2) civil_comments = google/civil_comments (Jigsaw Unintended Bias, Borkan et al. 2019; CC0 1.0), 18,611 rows. Three
  role-distinct components are carried via metadata_record_type: (a) content_pair (18,853) = human toxic<->neutral parallel
  sentences, the NON-CIRCULAR content perturbation P (metadata_text_on / metadata_text_off) for per-latent content-response;
  (b) surface_pair (546) = OpenRouter gpt-4o-mini toxic->toxic paraphrases (input / metadata_text_paired), double-gated (token
  Jaccard<0.6 AND norm edit-dist>0.25 AND LLM-judge toxicity_preserved+meaning_preserved; judge pass 70.6%, refusal 1.5%,
  cost $0.060), the surface-invariance control, folded into their seed corpus's group via metadata_origin_source; (c) classification
  (18,308) = civil_comments comments with a binary metadata_toxicity_label plus FROZEN multi-label sub-context labels (severe_toxicity,
  obscene, threat, insult, identity_attack, sexual_explicit) thresholded at 0.5 from the raw annotator-fraction floats (preserved
  in metadata_subcontext_floats for re-thresholding). Power: obscene/threat/insult/identity_attack/sexual_explicit are inferential@0.5
  with >=150 positives in every eval fold; severe_toxicity is flagged descriptive_only (too rare even at 0.3) -- not silently
  dropped. data_summary.json reports per-sub-context per-fold counts at 0.5 and 0.3, the sub-attribute pairwise Jaccard co-occurrence
  matrix (insult<->obscene ~0.245 shared-support => C-track; threat/identity_attack <0.05 disjoint => K-track), generation
  stats, and 316 reconciled cross-source collisions. Leakage-safe doc-level folds (metadata_fold in train/val/test) via union-find
  over normalized text: civil_comments keeps native splits; verified 0 pair_id and 0 source_sentence_id spanning folds and
  0 normalized texts in >1 fold. Sanity baselines (TF-IDF+logistic regression, train->test): toxicity AUC 0.851/F1 0.773;
  sub-contexts AUC 0.81-0.94; content_pair mean cos 0.685 (genuine flip), surface_pair 0.355 (reworded not copied). Files:
  data.py (stdlib-only uv assembler), full/mini/preview_data_out.json (validated), data_summary.json, README.md, pyproject.toml
  (47 pinned deps), and build/ (staged pipeline: ParaDetox content-flips, civil_comments stream-filter, OpenRouter surface
  generation, assembler, verify_baseline). Downstream consumers flatten datasets[*].examples and filter metadata_record_type.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_3
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

--- Dependency 5 ---
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

### [9] SYSTEM-USER prompt · 2026-06-18 00:57:55 UTC

```
<validation-feedback>
Attempt 1 failed validation.

You have not created the output file `.terminal_claude_agent_struct_out.json` yet. Use the Write tool to create it.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```

### [10] SYSTEM-USER prompt · 2026-06-18 01:03:22 UTC

```
<CRITICAL_ERROR>
Some files in your workspace exceed the 100MB size limit for GitHub deployment.

OVERSIZED FILES:
  - cache/build_toxicity_family_full_v5.pkl (903.7 MB)
  - cache/build_taxonomic_full_v5.pkl (434.1 MB)
  - cache/build_numeric_full_v5.pkl (186.1 MB)
  - cache/build_sentiment_full_v5.pkl (174.0 MB)
  - cache/build_toxicity_family_mini_v5.pkl (125.9 MB)
  - cache/build_aspect_food_full_v5.pkl (124.1 MB)

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
