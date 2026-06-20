# gen_art_experiment_2 — test_idea

> Phase: `invention_loop` · round 5 · `gen_art`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_experiment_2` (terminal_claude_agent)

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
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_2`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_2/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_2/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_2/results/out.json`
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
  M2 — Cross-Dictionary Replication of the Auditability Spine on the 65k-Width (and a Second-Layer) Gemma-Scope SAE
summary: >-
  Re-run the headline auditability spine (homograph recall-holes, KG-repair FDR survivors, Georgia/Jordan surgical edits,
  recall-hole/firing-Jaccard router) on the 65k-width canonical Gemma-Scope SAE (layer_12, primary) and, if budget allows,
  one earlier residual layer at width-16k (secondary), on the SAME frozen gemma-2-2b model and the SAME frozen testbeds used
  at iter-4. The single most important difference vs iter-4: latent indices are dictionary-specific, so anchors AND absorbers
  MUST be re-derived on each new dictionary (the 16k IDs Georgia->16009 / Jordan->540,8347 do NOT carry over). Output is a
  per-dictionary replication table with honest deltas vs the 16k counts and a REPLICATES / PARTIAL / DICTIONARY-DEPENDENT
  verdict per piece. A partial replication de-risks generalization; a clean non-replication is itself the publishable dictionary-dependence
  finding the literature predicts (wider SAEs absorb MORE). Core run is $0 LLM (all measurement is model-internal); member-labeling
  is an optional, budget-gated extra.
runpod_compute_profile: gpu
implementation_pseudocode: |-
  GOAL (load-bearing M2): replicate iter-4's auditability spine on >=1 SECOND SAE dictionary of the SAME model (gemma-2-2b). PRIMARY dictionary = width-65k canonical at layer 12; SECONDARY (budget-permitting) = an earlier residual layer (~6-9) at width-16k. Report honest deltas + a REPLICATES/PARTIAL/DICTIONARY-DEPENDENT verdict per spine piece.

  =================== REUSE (copy + adapt; do NOT rewrite from scratch) ===================
  The full spine is ALREADY IMPLEMENTED at iter-4/iter-3 — copy these files into the workspace and parametrize the SAE (release/width/layer):
    R1 = run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_1/method.py
         -> JumpReLUSAE class, _find_sae_params(), load_sae(), gating check, determine_layer_idx(), select_positions(),
            BROAD K-track KG-repair loop (kg_absorber[X]=argmax recall over content-responsive latents, jaccard<0.10, subctx_prec>=0.70),
            random-latent control + one-sided bootstrap p, Benjamini-Hochberg FDR<=0.05 (hand-rolled + statsmodels crosscheck),
            k_localization_check (JTT), ensemble member-labeling.
    R2 = run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_2/method.py
         -> edit operators KG-ABL (h <- h - lambda*z_l*W_dec[l], gated by latent's own firing), DENSE-ABL (h <- h - beta*(h.u)u, diff-of-means parent erasure = baseline f), RAND, KG-ADD, (k);
            forward_pos_logprobs(), behavioral_curve(), run_case(), next-token-KL on_target/collateral, SURGICAL SELECTIVITY=on_target/collateral, paired bootstrap CI (B=10000) on dense-minus-kg collateral, regime router map.
    R3 = run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_4/method.py
         -> firing_jaccard(), per-sub-context parent recall-hole (recall_hole=1-parent_recall), derive_1d() threshold sweep, balanced_accuracy(), 2-signal router (jaccard<tau_j AND recall_hole>tau_h), recall_hole_router (tau_h-only).
  Pin deps from the iter-4 pyproject.toml (torch==2.6.0 cu124, transformers, numpy, scipy, statsmodels, scikit-learn, networkx, loguru). Use unsloth/gemma-2-2b mirror fallback if google/gemma-2-2b is gated.

  =================== DATASETS (frozen; same testbeds as iter-4) ===================
    taxonomic + numeric: iter_1/gen_art/gen_art_dataset_2/full_data_out.json (datasets: taxonomic_absorption, numeric_absorption; content_flip pairs, surface_flip pairs, corpus windows; sub_context labels; gemma token indices precomputed).
    spelling L/O/T/I/D:   iter_1/gen_art/gen_art_dataset_1/full_data_out.json (first_letter_spelling_{L,O,T,I,D}; content_flip, surface_flip, corpus_context).
    toxicity (co-firing pole): iter_1/gen_art/gen_art_dataset_3/full_data_out.json (paradetox content_pair, civil_comments classification with frozen sub-context labels insult/obscene/threat/identity_attack/...).
  Flatten datasets[*].examples; filter by metadata_record_type / pair_type / role; reconstruct pairs by shared metadata_pair_id + role(on/off).

  =================== SAE CONFIG (the only thing that changes vs iter-4) ===================
  D_MODEL=2304; gemma-2-2b is 26 layers; hook at blocks.L.hook_resid_post == model.model.layers[L].forward_hook output == hidden_states[L+1].
  DICT-65K (PRIMARY): raw release 'google/gemma-scope-2b-pt-res', path 'layer_12/width_65k/average_l0_72/params.npz'. CANONICAL = avg L0 closest to 100; for layer_12/width_65k the available L0s are {21,38,72,141,297} -> 72 is canonical (VERIFIED on HF tree). Reuse _find_sae_params() but glob 'layer_12/width_65k/average_l0_*/params.npz' and pick min|L0-100|; assert resolved==72 and LOG it. (Equivalent SAELens path: release='gemma-scope-2b-pt-res-canonical', sae_id='layer_12/width_65k/canonical' — both resolve to the same npz; prefer the direct-npz JumpReLUSAE loader for zero new deps.) Expected d_sae=65536, W_enc[2304,65536], W_dec[65536,2304], plus b_enc,b_dec,threshold; firing=encode>0 = (pre>threshold)*relu(pre).
  DICT-L9-16K (SECONDARY): 'layer_9/width_16k/average_l0_*/params.npz' (glob closest-to-100), HOOK_LAYER=9, hidden_states idx=10; set determine_layer_idx to search (8,9,10,11). Earlier layer chosen to contrast L12 and stay inside the strict-diagnostic-valid 0-17 range (form-free diagnostic works at all layers). If layer_9 unavailable pick layer_6.
  GATING: cosine(h, decode(encode(h)))>0.9 measured on TAXONOMIC + SPELLING tokens (the gate is a GLOBAL property of the mapping). EXPECT ~0.90-0.92 at 65k. Record numeric digit-token cosine DESCRIPTIVELY (iter-4 found 16k numeric ~0.8911<0.9); do NOT gate-fail on numeric. If the GLOBAL taxonomic cosine<0.9 at 65k, that is itself a reportable reconstruction-quality delta — log it, demote 65k numeric/spelling to descriptive, continue.
  MEMORY (4x wider dict): W matrices ~1.2GB f32 fine on 20GB. The RISK is materializing dense latent matrices [N_tokens, 65536]. Use aii-use-hardware; chunk encoding (BATCH<=16, MAXLEN<=192); NEVER hold all-token x all-65536 in f32 — either (a) compute per-latent firing/recall statistics streaming over chunks, or (b) keep only the candidate-latent columns needed (anchor + top-K covering latents) as f16. Disk-cache per-(dict,layer,split) encodings under cache/ keyed by SAE id + dataset hash; EXCLUDE cache/ from upload.

  =================== EXECUTION ORDER (gradual scaling; depth-first on the highest-value slice) ===================
  STAGE 0 — SETUP & SMOKE (~10 min): load gemma-2-2b + DICT-65K; run determine_layer_idx on 32 taxonomic rows to confirm hidden_states[13]; assert gating cosine>0.9; assert d_sae==65536. Emit a tiny smoke method_out.json (gating only) and STOP if --smoke.

  STAGE 1 — 65k TAXONOMIC Georgia/Jordan (the minimal load-bearing replication; do FIRST):
    1a. Encode taxonomic content_flip pairs (x_on/x_off) + corpus windows at L12/65k. Per latent l, content-response r_l = a_l(x_on)-a_l(x_off); firing = encode>0 at the target token position (use precomputed token indices / select_positions on offset map).
    1b. RE-DERIVE the parent anchor on 65k: anchor = highest content-flip-recall content-responsive latent, with the UNSUPERVISED FIRING-FLOOR validation (anchor must fire on >= SPURIOUS_FIRE_FLOOR=0.01 of held-out corpus positives; else pick next — this is the iter-4 letter-I fix). Log the new 65k anchor latent id (will differ from 16k 3792).
    1c. (A) ROUTER SIGNALS per country: per-sub-context parent recall-hole = 1 - parent_recall on that country's positives; detector = best per-country latent; positive-only firing-Jaccard(parent,detector) (reuse R3 firing_jaccard). QUESTION: do Georgia & Jordan still satisfy recall_hole>0.5 AND jaccard<0.1? Report hole + jaccard for ALL eligible countries (>=150 diagnostic positives) and flag Jordan's n (iter-4 n=124 descriptive) next to Georgia.
    1d. (B) KG-REPAIR for Georgia & Jordan (and every eligible country): kg_absorber[X]=argmax_{l: content-responsive, l!=anchor, jaccard(l,anchor)<KG_JACCARD_MAX=0.10, subctx_prec(l,X)>=KG_PREC_MIN=0.70} recall_l(X-selection-split). ADD absorber to anchor (max-pool) and MEASURE held-out recall recovery (gain_kg) vs the RANDOM-SINGLE-LATENT control distribution (each other content-responsive latent added singly -> gain distribution); report kg_percentile_vs_random (KG gain exceeds 95th/99th pct), paired-bootstrap CI (B=10000) and one-sided p (H0: kg_gain-random_gain<=0). [M5 wording: control = random SINGLE content-responsive-latent addition, NOT a full-population max-pool.] Use HOLE_RECALL_MAX=0.60 to flag holes; N_MIN_SEL=10/N_MIN_RELAX=15/N_MIN_EVAL=30 floors.
    1e. (C) SURGICAL EDIT for the re-derived Georgia & Jordan absorbers (reuse R2 run_case): KG-ABL the absorber, DENSE-ABL the diff-of-means parent (fit on a DISJOINT diagnostic fold), RAND control, KG-ADD; next-token KL on_target (edited token) vs collateral (sibling-country tokens) over kl_prompts; SURGICAL SELECTIVITY=on_target/collateral at MATCHED on-target; paired-bootstrap CI on (dense_collateral - kg_collateral) must exclude 0 favoring KG; graded verdict (clean surgical: kg collateral not sig>0, footprint<2%, ratio>=20).

  STAGE 2 — 65k SPELLING (L/O/T/I/D) + TOXICITY co-firing pole:
    Spelling: per letter re-derive anchor (firing-floor validated) + per-word absorbers; router signals (recall_hole, jaccard); KG-repair FDR rows; ONE surgical edit on the best-precision letter absorber (iter-4 used 'large'->8463; re-derive the 65k id). Expect letters where 16k held (T/O/L words +1.0) to remain strong.
    Toxicity (NEGATIVE pole, regime contrast): parent=toxic-vs-neutral; sub-attributes insult/obscene/threat/identity_attack. Confirm the co-firing signature PERSISTS at 65k: recall_hole ~0 and firing-Jaccard high (iter-4: insult jaccard 0.878, hole 0.00). Run the insult single-latent ablation -> expect NOT clean (selectivity collapses). This anchors the absorption-vs-co-firing split on the new dictionary.
    Numeric (optional, demotable): repair-FDR rows only; remember digit-token cosine<0.9 (descriptive). iter-4 numeric survivors: date+0.68/ordinal+0.53/decimal+0.45/year+0.35/comma+0.24/currency+0.14, integer tied.

  STAGE 3 — BH FDR ACROSS ALL 65k VARIANTS (one BH family over all concepts, exactly like iter-4): assign bh_q + survives_FDR; hand-rolled BH crosschecked vs statsmodels. Report per-family survivor counts and DELTAS vs 16k counts (16k: homograph-taxonomic 6, numeric 10, spelling 14, over ~23 distinct holes). De-duplicate variants where kg_ktrack and kg_diagnostic name the SAME 65k latent (M3 honest counting); report DISTINCT-hole count as the headline number.

  STAGE 4 — ROUTER THRESHOLD TRANSFER on 65k: recompute recall_hole_max + firing_jaccard_median for the SAME derivation concept set used at iter-3/iter-4. (i) Apply the FROZEN 16k-derived thresholds (tau_h, tau_j) WITHOUT refitting and report balanced-accuracy on 65k. (ii) Re-derive 65k-optimal tau_h (recall-hole-ALONE, lead signal per M6) and tau_j (firing-Jaccard corroborating) via derive_1d; report 65k balanced-acc and whether the 65k thresholds are close to 16k (transfer = frozen 16k thresholds still give high bal-acc on 65k). Lead with recall-hole-alone (iter-4: bal-acc 1.0, no derivation counterexample); firing-Jaccard corroborating.

  STAGE 5 — SECONDARY DICTIONARY (DICT-L9-16K), only if Stages 1-4 land with budget left: repeat the MOST DIAGNOSTIC subset only — Georgia/Jordan router signals (1c) + KG-repair (1d) + surgical edit (1e). This is a second axis (layer) of the same generalization claim.

  STAGE 6 — ASSEMBLE method_out.json (exp_gen_sol_out schema):
    metadata: per-dictionary gating_check (cosine, L0, resolved average_l0, layer_idx, numeric_digit_cosine descriptive); re-derived anchors+absorber latent ids per concept (with the firing-floor validation result); a REPLICATION TABLE per dictionary with one entry per spine piece:
      {dictionary, layer, width,
       homograph_holes: {Georgia:{recall_hole, firing_jaccard, eligible, n}, Jordan:{...}, ...},
       repair_fdr: {per_family_survivors, deltas_vs_16k, distinct_hole_count, example gains+p+bh_q},
       surgical: {per_case selectivity_ratio, kg_collateral, dense_collateral, dense_minus_kg_CI, footprint, verdict, delta_vs_16k},
       router: {tau_h, tau_j, balanced_acc_recall_hole_alone, balanced_acc_combined, frozen_16k_threshold_balanced_acc, transfers:bool},
       regime_split: {absorption_mean_selectivity, cofiring_mean_selectivity}}
    PER-PIECE VERDICT logic: REPLICATES if (Georgia&Jordan holes reappear: recall_hole>0.5 & jaccard<0.1) AND (>=1 repair per replicated family survives FDR) AND (surgical selectivity ratio>=20 with dense-kg collateral CI>0) AND (router frozen-16k thresholds still bal-acc>=0.8). PARTIAL if some pieces hold and others don't (state which). DICTIONARY-DEPENDENT if holes vanish / repairs die / selectivity collapses (report as the honest, publishable wider-SAE-absorbs-more finding). Also an OVERALL verdict {cross_dictionary_replicates: full|partial|dictionary_dependent}.
    datasets: a 'cross_dictionary_replication' dataset with ONE exp_gen_sol_out example per (dictionary x piece x sub_context): input=concept/sub-context descriptor; output=verdict label or numeric prediction; metadata_* = dictionary, layer, width, recall_hole, firing_jaccard, gain_kg, one_sided_p, bh_q, survives_FDR, selectivity_ratio, dense_minus_kg_collateral, delta_vs_16k. These per-row predictions feed downstream evaluation.
    Validate with aii-json; run aii-file-size-limit; ensure full/mini/preview_method_out.json each <100MB (drop per-token arrays into cache/, keep summaries in JSON). EXCLUDE cache/ from upload.

  COST: core spine = $0 LLM (KL, recall, selectivity, router all model-internal). OPTIONAL member-labeling (M7) on 65k members uses anthropic/claude-haiku-4.5 J=3 (~$0.2, hard stop $10) — run ONLY if Stages 1-5 finish early; otherwise skip (not in the M2 headline spine).
fallback_plan: |-
  TRIAGE / DROP ORDER (first dropped first), so a clean load-bearing replication always ships: optional member-labeling -> second layer (Stage 5) -> 65k numeric -> 65k toxicity -> 65k spelling letters beyond one -> down to the NEVER-DROP minimum = 65k taxonomic Georgia/Jordan router-signals + KG-repair + surgical edit (Stage 1) with a verdict. Always emit a verdict for whatever completed.

  OOM on the 4x-wider dict: lower BATCH to 8 and MAXLEN to 128; store latents as float16; do NOT materialize [N,65536] dense — switch to streaming per-latent firing/recall accumulation over chunks, or restrict to the candidate-latent columns (anchor + top-K coverers). If still tight, subsample corpus windows to ~1000/concept and content-flip pairs to the dataset's inferential floor (>=150 positives/sub-context). The W matrices themselves (~1.2GB) are never the problem.

  params.npz / model download: 'google/gemma-scope-2b-pt-res' is the open Gemma-Scope repo (use HF_TOKEN if prompted); for the gated gemma-2-2b fall back to unsloth/gemma-2-2b mirror (vocab 256000), exactly as iter-4. Use HF_HUB_OFFLINE=1 after first cache to skip the ~140s metadata check.

  65k gating cosine<=0.9 on taxonomic tokens: first re-check the hidden_states index via determine_layer_idx over (11,12,13,14) — wrong-layer mapping is the usual cause. If the global mapping genuinely reconstructs <0.9, that is a REPORTABLE reconstruction-quality delta: demote affected families to descriptive and continue (do not abort the whole run).

  Re-derived 65k anchor is spurious (fires ~0% on corpus, the letter-I-1227 failure mode): apply SPURIOUS_FIRE_FLOOR=0.01 firing-floor validation and take the next-highest-recall validated latent; if no validated anchor exists for a concept, mark that concept 'anchor-invalid at 65k' (an honest dictionary-dependence datum), skip its repair/surgical, keep it in the report.

  No precision>=0.70 absorber found for Georgia/Jordan at 65k (wider SAE may split the country across many lower-precision specialists, or absorb it differently): this is the KEY dictionary-dependence outcome the literature predicts (wider->more absorption/more fragmentation). Report it explicitly: record the best available absorber with its precision/jaccard, mark repair/surgical as NON-REPLICATED, and write the verdict as DICTIONARY-DEPENDENT for that piece. Do NOT force a low-precision absorber to manufacture a positive.

  Surgical selectivity collapses at 65k even though a clean absorber exists: report the ratio + CI honestly; if dense-minus-kg collateral CI includes 0, that piece is PARTIAL/non-replicated. A genuine failure of the surgical replication is publishable.

  Router thresholds don't transfer (frozen 16k tau give low bal-acc on 65k): report both frozen-16k and re-fit-65k thresholds and the gap; conclude 'router thresholds are dictionary-specific' — still an honest M2 finding. Lead with recall-hole-alone either way.

  Time exhausted mid-stage: write whatever method_out.json exists with completed pieces + explicit 'not_run' flags for the rest, so the artifact is always valid and downstream can read partial replication.
testing_plan: |-
  1) IMPORT/LOAD smoke (`python method.py --smoke`, ~5-10 min): load gemma-2-2b (or unsloth mirror) + DICT-65K via the JumpReLUSAE npz loader; ASSERT resolved average_l0==72, d_sae==65536, d_model==2304; run determine_layer_idx on 32 taxonomic rows and CONFIRM best hidden_states idx==13; ASSERT gating cosine>0.9 on a small taxonomic+spelling batch. Print numeric digit-token cosine descriptively. If any assert fails, fix loader/layer mapping BEFORE proceeding. Emit a tiny gating-only method_out.json and exit.

  2) MINI pilot (`--families taxonomic --cap 40 --kl_prompts 16`, ~20-30 min): on 65k taxonomic only, RE-DERIVE the parent anchor (confirm it fires >1% on corpus, i.e. not spurious) and the Georgia absorber (confirm jaccard(absorber,anchor)<0.10 and subctx_precision>=0.70 on a held-out fold). Run ONE Georgia surgical edit and confirm KG collateral << DENSE collateral and selectivity ratio is large (directionally matching 16k's Georgia ~1722x/hole~0.8). CONFIRMATION SIGNALS to gate the full run: (a) gating passes; (b) re-derived Georgia anchor non-spurious; (c) Georgia recall_hole>0.5 & jaccard<0.1; (d) Georgia repair gain_kg>0 exceeding the random-single-latent 95th pct; (e) Georgia surgical dense-minus-kg collateral CI>0. If (c)-(e) FAIL on mini, that is the dictionary-dependence signal — still scale up to characterize it fully (don't abort), but flag it early.

  3) NUMERICAL cross-checks: hand-rolled BH q-values matched against statsmodels.stats.multitest.multipletests(method='fdr_bh') (as iter-4 did); paired bootstrap CIs reproducible under fixed SEED=1234; firing_jaccard and recall_hole recomputed on a 16k slice to confirm the copied R3 functions reproduce iter-3/iter-4 numbers before trusting them on 65k.

  4) GUARDRAILS during scaling (use aii-long-running-tasks staged pattern): run as `uv run method.py & PID=$!`; monitor logs/run.log by PID only; checkpoint after each stage (Stage1->Stage2->...) so a crash keeps completed pieces. Watch GPU memory after first 65k encode chunk; if >16GB, trigger the float16/streaming fallback before full-scale encode.

  5) FINAL validation: aii-json validate method_out.json against exp_gen_sol_out; aii-file-size-limit on full/mini/preview (<100MB each, split or push per-token arrays to cache/ if over); confirm cache/ is excluded from upload; sanity-read the replication table + per-piece verdicts for internal consistency (e.g. a piece marked REPLICATES must have its CI/threshold conditions actually satisfied in the row data).
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

--- Dependency 5 ---
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

### [3] SKILL-INPUT — aii-long-running-tasks · 2026-06-18 02:12:38 UTC

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

### [4] SKILL-INPUT — aii-use-hardware · 2026-06-18 02:12:38 UTC

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

### [5] SYSTEM-USER prompt · 2026-06-18 03:33:33 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_2`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_2/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_2/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_2/results/out.json`
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
  M2 — Cross-Dictionary Replication of the Auditability Spine on the 65k-Width (and a Second-Layer) Gemma-Scope SAE
summary: >-
  Re-run the headline auditability spine (homograph recall-holes, KG-repair FDR survivors, Georgia/Jordan surgical edits,
  recall-hole/firing-Jaccard router) on the 65k-width canonical Gemma-Scope SAE (layer_12, primary) and, if budget allows,
  one earlier residual layer at width-16k (secondary), on the SAME frozen gemma-2-2b model and the SAME frozen testbeds used
  at iter-4. The single most important difference vs iter-4: latent indices are dictionary-specific, so anchors AND absorbers
  MUST be re-derived on each new dictionary (the 16k IDs Georgia->16009 / Jordan->540,8347 do NOT carry over). Output is a
  per-dictionary replication table with honest deltas vs the 16k counts and a REPLICATES / PARTIAL / DICTIONARY-DEPENDENT
  verdict per piece. A partial replication de-risks generalization; a clean non-replication is itself the publishable dictionary-dependence
  finding the literature predicts (wider SAEs absorb MORE). Core run is $0 LLM (all measurement is model-internal); member-labeling
  is an optional, budget-gated extra.
runpod_compute_profile: gpu
implementation_pseudocode: |-
  GOAL (load-bearing M2): replicate iter-4's auditability spine on >=1 SECOND SAE dictionary of the SAME model (gemma-2-2b). PRIMARY dictionary = width-65k canonical at layer 12; SECONDARY (budget-permitting) = an earlier residual layer (~6-9) at width-16k. Report honest deltas + a REPLICATES/PARTIAL/DICTIONARY-DEPENDENT verdict per spine piece.

  =================== REUSE (copy + adapt; do NOT rewrite from scratch) ===================
  The full spine is ALREADY IMPLEMENTED at iter-4/iter-3 — copy these files into the workspace and parametrize the SAE (release/width/layer):
    R1 = run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_1/method.py
         -> JumpReLUSAE class, _find_sae_params(), load_sae(), gating check, determine_layer_idx(), select_positions(),
            BROAD K-track KG-repair loop (kg_absorber[X]=argmax recall over content-responsive latents, jaccard<0.10, subctx_prec>=0.70),
            random-latent control + one-sided bootstrap p, Benjamini-Hochberg FDR<=0.05 (hand-rolled + statsmodels crosscheck),
            k_localization_check (JTT), ensemble member-labeling.
    R2 = run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_2/method.py
         -> edit operators KG-ABL (h <- h - lambda*z_l*W_dec[l], gated by latent's own firing), DENSE-ABL (h <- h - beta*(h.u)u, diff-of-means parent erasure = baseline f), RAND, KG-ADD, (k);
            forward_pos_logprobs(), behavioral_curve(), run_case(), next-token-KL on_target/collateral, SURGICAL SELECTIVITY=on_target/collateral, paired bootstrap CI (B=10000) on dense-minus-kg collateral, regime router map.
    R3 = run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_4/method.py
         -> firing_jaccard(), per-sub-context parent recall-hole (recall_hole=1-parent_recall), derive_1d() threshold sweep, balanced_accuracy(), 2-signal router (jaccard<tau_j AND recall_hole>tau_h), recall_hole_router (tau_h-only).
  Pin deps from the iter-4 pyproject.toml (torch==2.6.0 cu124, transformers, numpy, scipy, statsmodels, scikit-learn, networkx, loguru). Use unsloth/gemma-2-2b mirror fallback if google/gemma-2-2b is gated.

  =================== DATASETS (frozen; same testbeds as iter-4) ===================
    taxonomic + numeric: iter_1/gen_art/gen_art_dataset_2/full_data_out.json (datasets: taxonomic_absorption, numeric_absorption; content_flip pairs, surface_flip pairs, corpus windows; sub_context labels; gemma token indices precomputed).
    spelling L/O/T/I/D:   iter_1/gen_art/gen_art_dataset_1/full_data_out.json (first_letter_spelling_{L,O,T,I,D}; content_flip, surface_flip, corpus_context).
    toxicity (co-firing pole): iter_1/gen_art/gen_art_dataset_3/full_data_out.json (paradetox content_pair, civil_comments classification with frozen sub-context labels insult/obscene/threat/identity_attack/...).
  Flatten datasets[*].examples; filter by metadata_record_type / pair_type / role; reconstruct pairs by shared metadata_pair_id + role(on/off).

  =================== SAE CONFIG (the only thing that changes vs iter-4) ===================
  D_MODEL=2304; gemma-2-2b is 26 layers; hook at blocks.L.hook_resid_post == model.model.layers[L].forward_hook output == hidden_states[L+1].
  DICT-65K (PRIMARY): raw release 'google/gemma-scope-2b-pt-res', path 'layer_12/width_65k/average_l0_72/params.npz'. CANONICAL = avg L0 closest to 100; for layer_12/width_65k the available L0s are {21,38,72,141,297} -> 72 is canonical (VERIFIED on HF tree). Reuse _find_sae_params() but glob 'layer_12/width_65k/average_l0_*/params.npz' and pick min|L0-100|; assert resolved==72 and LOG it. (Equivalent SAELens path: release='gemma-scope-2b-pt-res-canonical', sae_id='layer_12/width_65k/canonical' — both resolve to the same npz; prefer the direct-npz JumpReLUSAE loader for zero new deps.) Expected d_sae=65536, W_enc[2304,65536], W_dec[65536,2304], plus b_enc,b_dec,threshold; firing=encode>0 = (pre>threshold)*relu(pre).
  DICT-L9-16K (SECONDARY): 'layer_9/width_16k/average_l0_*/params.npz' (glob closest-to-100), HOOK_LAYER=9, hidden_states idx=10; set determine_layer_idx to search (8,9,10,11). Earlier layer chosen to contrast L12 and stay inside the strict-diagnostic-valid 0-17 range (form-free diagnostic works at all layers). If layer_9 unavailable pick layer_6.
  GATING: cosine(h, decode(encode(h)))>0.9 measured on TAXONOMIC + SPELLING tokens (the gate is a GLOBAL property of the mapping). EXPECT ~0.90-0.92 at 65k. Record numeric digit-token cosine DESCRIPTIVELY (iter-4 found 16k numeric ~0.8911<0.9); do NOT gate-fail on numeric. If the GLOBAL taxonomic cosine<0.9 at 65k, that is itself a reportable reconstruction-quality delta — log it, demote 65k numeric/spelling to descriptive, continue.
  MEMORY (4x wider dict): W matrices ~1.2GB f32 fine on 20GB. The RISK is materializing dense latent matrices [N_tokens, 65536]. Use aii-use-hardware; chunk encoding (BATCH<=16, MAXLEN<=192); NEVER hold all-token x all-65536 in f32 — either (a) compute per-latent firing/recall statistics streaming over chunks, or (b) keep only the candidate-latent columns needed (anchor + top-K covering latents) as f16. Disk-cache per-(dict,layer,split) encodings under cache/ keyed by SAE id + dataset hash; EXCLUDE cache/ from upload.

  =================== EXECUTION ORDER (gradual scaling; depth-first on the highest-value slice) ===================
  STAGE 0 — SETUP & SMOKE (~10 min): load gemma-2-2b + DICT-65K; run determine_layer_idx on 32 taxonomic rows to confirm hidden_states[13]; assert gating cosine>0.9; assert d_sae==65536. Emit a tiny smoke method_out.json (gating only) and STOP if --smoke.

  STAGE 1 — 65k TAXONOMIC Georgia/Jordan (the minimal load-bearing replication; do FIRST):
    1a. Encode taxonomic content_flip pairs (x_on/x_off) + corpus windows at L12/65k. Per latent l, content-response r_l = a_l(x_on)-a_l(x_off); firing = encode>0 at the target token position (use precomputed token indices / select_positions on offset map).
    1b. RE-DERIVE the parent anchor on 65k: anchor = highest content-flip-recall content-responsive latent, with the UNSUPERVISED FIRING-FLOOR validation (anchor must fire on >= SPURIOUS_FIRE_FLOOR=0.01 of held-out corpus positives; else pick next — this is the iter-4 letter-I fix). Log the new 65k anchor latent id (will differ from 16k 3792).
    1c. (A) ROUTER SIGNALS per country: per-sub-context parent recall-hole = 1 - parent_recall on that country's positives; detector = best per-country latent; positive-only firing-Jaccard(parent,detector) (reuse R3 firing_jaccard). QUESTION: do Georgia & Jordan still satisfy recall_hole>0.5 AND jaccard<0.1? Report hole + jaccard for ALL eligible countries (>=150 diagnostic positives) and flag Jordan's n (iter-4 n=124 descriptive) next to Georgia.
    1d. (B) KG-REPAIR for Georgia & Jordan (and every eligible country): kg_absorber[X]=argmax_{l: content-responsive, l!=anchor, jaccard(l,anchor)<KG_JACCARD_MAX=0.10, subctx_prec(l,X)>=KG_PREC_MIN=0.70} recall_l(X-selection-split). ADD absorber to anchor (max-pool) and MEASURE held-out recall recovery (gain_kg) vs the RANDOM-SINGLE-LATENT control distribution (each other content-responsive latent added singly -> gain distribution); report kg_percentile_vs_random (KG gain exceeds 95th/99th pct), paired-bootstrap CI (B=10000) and one-sided p (H0: kg_gain-random_gain<=0). [M5 wording: control = random SINGLE content-responsive-latent addition, NOT a full-population max-pool.] Use HOLE_RECALL_MAX=0.60 to flag holes; N_MIN_SEL=10/N_MIN_RELAX=15/N_MIN_EVAL=30 floors.
    1e. (C) SURGICAL EDIT for the re-derived Georgia & Jordan absorbers (reuse R2 run_case): KG-ABL the absorber, DENSE-ABL the diff-of-means parent (fit on a DISJOINT diagnostic fold), RAND control, KG-ADD; next-token KL on_target (edited token) vs collateral (sibling-country tokens) over kl_prompts; SURGICAL SELECTIVITY=on_target/collateral at MATCHED on-target; paired-bootstrap CI on (dense_collateral - kg_collateral) must exclude 0 favoring KG; graded verdict (clean surgical: kg collateral not sig>0, footprint<2%, ratio>=20).

  STAGE 2 — 65k SPELLING (L/O/T/I/D) + TOXICITY co-firing pole:
    Spelling: per letter re-derive anchor (firing-floor validated) + per-word absorbers; router signals (recall_hole, jaccard); KG-repair FDR rows; ONE surgical edit on the best-precision letter absorber (iter-4 used 'large'->8463; re-derive the 65k id). Expect letters where 16k held (T/O/L words +1.0) to remain strong.
    Toxicity (NEGATIVE pole, regime contrast): parent=toxic-vs-neutral; sub-attributes insult/obscene/threat/identity_attack. Confirm the co-firing signature PERSISTS at 65k: recall_hole ~0 and firing-Jaccard high (iter-4: insult jaccard 0.878, hole 0.00). Run the insult single-latent ablation -> expect NOT clean (selectivity collapses). This anchors the absorption-vs-co-firing split on the new dictionary.
    Numeric (optional, demotable): repair-FDR rows only; remember digit-token cosine<0.9 (descriptive). iter-4 numeric survivors: date+0.68/ordinal+0.53/decimal+0.45/year+0.35/comma+0.24/currency+0.14, integer tied.

  STAGE 3 — BH FDR ACROSS ALL 65k VARIANTS (one BH family over all concepts, exactly like iter-4): assign bh_q + survives_FDR; hand-rolled BH crosschecked vs statsmodels. Report per-family survivor counts and DELTAS vs 16k counts (16k: homograph-taxonomic 6, numeric 10, spelling 14, over ~23 distinct holes). De-duplicate variants where kg_ktrack and kg_diagnostic name the SAME 65k latent (M3 honest counting); report DISTINCT-hole count as the headline number.

  STAGE 4 — ROUTER THRESHOLD TRANSFER on 65k: recompute recall_hole_max + firing_jaccard_median for the SAME derivation concept set used at iter-3/iter-4. (i) Apply the FROZEN 16k-derived thresholds (tau_h, tau_j) WITHOUT refitting and report balanced-accuracy on 65k. (ii) Re-derive 65k-optimal tau_h (recall-hole-ALONE, lead signal per M6) and tau_j (firing-Jaccard corroborating) via derive_1d; report 65k balanced-acc and whether the 65k thresholds are close to 16k (transfer = frozen 16k thresholds still give high bal-acc on 65k). Lead with recall-hole-alone (iter-4: bal-acc 1.0, no derivation counterexample); firing-Jaccard corroborating.

  STAGE 5 — SECONDARY DICTIONARY (DICT-L9-16K), only if Stages 1-4 land with budget left: repeat the MOST DIAGNOSTIC subset only — Georgia/Jordan router signals (1c) + KG-repair (1d) + surgical edit (1e). This is a second axis (layer) of the same generalization claim.

  STAGE 6 — ASSEMBLE method_out.json (exp_gen_sol_out schema):
    metadata: per-dictionary gating_check (cosine, L0, resolved average_l0, layer_idx, numeric_digit_cosine descriptive); re-derived anchors+absorber latent ids per concept (with the firing-floor validation result); a REPLICATION TABLE per dictionary with one entry per spine piece:
      {dictionary, layer, width,
       homograph_holes: {Georgia:{recall_hole, firing_jaccard, eligible, n}, Jordan:{...}, ...},
       repair_fdr: {per_family_survivors, deltas_vs_16k, distinct_hole_count, example gains+p+bh_q},
       surgical: {per_case selectivity_ratio, kg_collateral, dense_collateral, dense_minus_kg_CI, footprint, verdict, delta_vs_16k},
       router: {tau_h, tau_j, balanced_acc_recall_hole_alone, balanced_acc_combined, frozen_16k_threshold_balanced_acc, transfers:bool},
       regime_split: {absorption_mean_selectivity, cofiring_mean_selectivity}}
    PER-PIECE VERDICT logic: REPLICATES if (Georgia&Jordan holes reappear: recall_hole>0.5 & jaccard<0.1) AND (>=1 repair per replicated family survives FDR) AND (surgical selectivity ratio>=20 with dense-kg collateral CI>0) AND (router frozen-16k thresholds still bal-acc>=0.8). PARTIAL if some pieces hold and others don't (state which). DICTIONARY-DEPENDENT if holes vanish / repairs die / selectivity collapses (report as the honest, publishable wider-SAE-absorbs-more finding). Also an OVERALL verdict {cross_dictionary_replicates: full|partial|dictionary_dependent}.
    datasets: a 'cross_dictionary_replication' dataset with ONE exp_gen_sol_out example per (dictionary x piece x sub_context): input=concept/sub-context descriptor; output=verdict label or numeric prediction; metadata_* = dictionary, layer, width, recall_hole, firing_jaccard, gain_kg, one_sided_p, bh_q, survives_FDR, selectivity_ratio, dense_minus_kg_collateral, delta_vs_16k. These per-row predictions feed downstream evaluation.
    Validate with aii-json; run aii-file-size-limit; ensure full/mini/preview_method_out.json each <100MB (drop per-token arrays into cache/, keep summaries in JSON). EXCLUDE cache/ from upload.

  COST: core spine = $0 LLM (KL, recall, selectivity, router all model-internal). OPTIONAL member-labeling (M7) on 65k members uses anthropic/claude-haiku-4.5 J=3 (~$0.2, hard stop $10) — run ONLY if Stages 1-5 finish early; otherwise skip (not in the M2 headline spine).
fallback_plan: |-
  TRIAGE / DROP ORDER (first dropped first), so a clean load-bearing replication always ships: optional member-labeling -> second layer (Stage 5) -> 65k numeric -> 65k toxicity -> 65k spelling letters beyond one -> down to the NEVER-DROP minimum = 65k taxonomic Georgia/Jordan router-signals + KG-repair + surgical edit (Stage 1) with a verdict. Always emit a verdict for whatever completed.

  OOM on the 4x-wider dict: lower BATCH to 8 and MAXLEN to 128; store latents as float16; do NOT materialize [N,65536] dense — switch to streaming per-latent firing/recall accumulation over chunks, or restrict to the candidate-latent columns (anchor + top-K coverers). If still tight, subsample corpus windows to ~1000/concept and content-flip pairs to the dataset's inferential floor (>=150 positives/sub-context). The W matrices themselves (~1.2GB) are never the problem.

  params.npz / model download: 'google/gemma-scope-2b-pt-res' is the open Gemma-Scope repo (use HF_TOKEN if prompted); for the gated gemma-2-2b fall back to unsloth/gemma-2-2b mirror (vocab 256000), exactly as iter-4. Use HF_HUB_OFFLINE=1 after first cache to skip the ~140s metadata check.

  65k gating cosine<=0.9 on taxonomic tokens: first re-check the hidden_states index via determine_layer_idx over (11,12,13,14) — wrong-layer mapping is the usual cause. If the global mapping genuinely reconstructs <0.9, that is a REPORTABLE reconstruction-quality delta: demote affected families to descriptive and continue (do not abort the whole run).

  Re-derived 65k anchor is spurious (fires ~0% on corpus, the letter-I-1227 failure mode): apply SPURIOUS_FIRE_FLOOR=0.01 firing-floor validation and take the next-highest-recall validated latent; if no validated anchor exists for a concept, mark that concept 'anchor-invalid at 65k' (an honest dictionary-dependence datum), skip its repair/surgical, keep it in the report.

  No precision>=0.70 absorber found for Georgia/Jordan at 65k (wider SAE may split the country across many lower-precision specialists, or absorb it differently): this is the KEY dictionary-dependence outcome the literature predicts (wider->more absorption/more fragmentation). Report it explicitly: record the best available absorber with its precision/jaccard, mark repair/surgical as NON-REPLICATED, and write the verdict as DICTIONARY-DEPENDENT for that piece. Do NOT force a low-precision absorber to manufacture a positive.

  Surgical selectivity collapses at 65k even though a clean absorber exists: report the ratio + CI honestly; if dense-minus-kg collateral CI includes 0, that piece is PARTIAL/non-replicated. A genuine failure of the surgical replication is publishable.

  Router thresholds don't transfer (frozen 16k tau give low bal-acc on 65k): report both frozen-16k and re-fit-65k thresholds and the gap; conclude 'router thresholds are dictionary-specific' — still an honest M2 finding. Lead with recall-hole-alone either way.

  Time exhausted mid-stage: write whatever method_out.json exists with completed pieces + explicit 'not_run' flags for the rest, so the artifact is always valid and downstream can read partial replication.
testing_plan: |-
  1) IMPORT/LOAD smoke (`python method.py --smoke`, ~5-10 min): load gemma-2-2b (or unsloth mirror) + DICT-65K via the JumpReLUSAE npz loader; ASSERT resolved average_l0==72, d_sae==65536, d_model==2304; run determine_layer_idx on 32 taxonomic rows and CONFIRM best hidden_states idx==13; ASSERT gating cosine>0.9 on a small taxonomic+spelling batch. Print numeric digit-token cosine descriptively. If any assert fails, fix loader/layer mapping BEFORE proceeding. Emit a tiny gating-only method_out.json and exit.

  2) MINI pilot (`--families taxonomic --cap 40 --kl_prompts 16`, ~20-30 min): on 65k taxonomic only, RE-DERIVE the parent anchor (confirm it fires >1% on corpus, i.e. not spurious) and the Georgia absorber (confirm jaccard(absorber,anchor)<0.10 and subctx_precision>=0.70 on a held-out fold). Run ONE Georgia surgical edit and confirm KG collateral << DENSE collateral and selectivity ratio is large (directionally matching 16k's Georgia ~1722x/hole~0.8). CONFIRMATION SIGNALS to gate the full run: (a) gating passes; (b) re-derived Georgia anchor non-spurious; (c) Georgia recall_hole>0.5 & jaccard<0.1; (d) Georgia repair gain_kg>0 exceeding the random-single-latent 95th pct; (e) Georgia surgical dense-minus-kg collateral CI>0. If (c)-(e) FAIL on mini, that is the dictionary-dependence signal — still scale up to characterize it fully (don't abort), but flag it early.

  3) NUMERICAL cross-checks: hand-rolled BH q-values matched against statsmodels.stats.multitest.multipletests(method='fdr_bh') (as iter-4 did); paired bootstrap CIs reproducible under fixed SEED=1234; firing_jaccard and recall_hole recomputed on a 16k slice to confirm the copied R3 functions reproduce iter-3/iter-4 numbers before trusting them on 65k.

  4) GUARDRAILS during scaling (use aii-long-running-tasks staged pattern): run as `uv run method.py & PID=$!`; monitor logs/run.log by PID only; checkpoint after each stage (Stage1->Stage2->...) so a crash keeps completed pieces. Watch GPU memory after first 65k encode chunk; if >16GB, trigger the float16/streaming fallback before full-scale encode.

  5) FINAL validation: aii-json validate method_out.json against exp_gen_sol_out; aii-file-size-limit on full/mini/preview (<100MB each, split or push per-token arrays to cache/ if over); confirm cache/ is excluded from upload; sanity-read the replication table + per-piece verdicts for internal consistency (e.g. a piece marked REPLICATES must have its CI/threshold conditions actually satisfied in the row data).
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

--- Dependency 5 ---
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

### [6] SYSTEM-USER prompt · 2026-06-18 03:35:54 UTC

```
<CRITICAL_ERROR>
Some files in your workspace exceed the 100MB size limit for GitHub deployment.

OVERSIZED FILES:
  - cache/enc_65k_layer_12_width_65k_average_l0_72_tox_cap400_4800_ws1_bbcfc809ad48.npz (106.2 MB)

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
