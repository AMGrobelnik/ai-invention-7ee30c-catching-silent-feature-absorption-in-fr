# gen_art_experiment_3 — test_idea

> Phase: `invention_loop` · round 3 · `gen_art`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_experiment_3` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-17 18:27:30 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_3`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_3/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_3/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_3/results/out.json`
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
id: gen_plan_experiment_3_idx3
type: experiment
title: >-
  Measure Auditability (M5): KG-Guided Repair Loop + LLM-Judge Member-Labeling for Two-Track CCRG Units (First-Letter + Taxonomic)
summary: >-
  Execute the two previously-dropped, now load-bearing auditability results for the two-track CCRG units on a frozen Gemma-Scope
  L12/16k SAE. (a) KG-GUIDED REPAIR LOOP: for each under-served sub-context (recall hole where the parent/anchor latent goes
  silent), ADD the KG-named covering absorber (max-pool) and MEASURE recall recovery on HELD-OUT corpus windows with a paired
  bootstrap CI (B>=10,000), versus a random-content-responsive-latent-addition control (averaged over many draws); success
  = KG-guided-minus-random gain CI excludes 0; plus confirm the label-free group-inference probe (k) cannot localize the fix
  to a single addable latent. (b) MEMBER-LABELING: for each unit member, assemble its logit-lens top tokens + raw top-activating
  corpus windows, send to an OpenRouter LLM judge (anthropic/claude-haiku-4.5) for forced-choice sub-context naming, score
  agreement vs a shuffled-label null with bootstrap CI. Reuse the iter-2 SAE loader/hook/firing/unit-definition/recall code
  verbatim and read iter-2 canonical units/KG; re-derive as a cross-check. At least one MEASURED KG-utility result must replace
  the iter-2 'we emit a 70-edge graph' assertion. Report honest negatives (a tie with the random-addition control = 'auditability
  buys no measurable fix there').
runpod_compute_profile: gpu
implementation_pseudocode: "# ============================================================================\n# EXPERIMENT iter3_dir3\
  \ - MEASURE AUDITABILITY (M5)\n# Compute: gpu (A4500 20GB). Wall-clock target <4h. LLM cap $10, target <$3.\n# Output: method_out.json\
  \ (+ full/mini/preview), all <100MB.\n# ============================================================================\n#\n\
  # ---- ABSOLUTE PATHS (read-only inputs; do NOT mutate) -----------------------\n# FIRST-LETTER dataset (art_dpYpjSn2Xvg3):\n\
  #   D1 = /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json\n\
  # TAXONOMIC/NUMERIC dataset (art_t2uUbjSwpd3t):\n#   D2 = /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_2/full_data_out.json\n\
  # Method dossier (art_RidEJtBC7gPT): .../iter_1/gen_art/gen_art_research_1/research_out.json\n# Diagnostic+data dossier\
  \ (art_I2MrezW41iQo): .../iter_1/gen_art/gen_art_research_2/research_out.json\n# iter-2 EXECUTED first-letter run (canonical\
  \ units/KG + reusable code):\n#   E1 = .../iter_2/gen_art/gen_art_experiment_1/   (method.py, method_out.json)\n# iter-2\
  \ EXECUTED taxonomic/numeric run:\n#   E3 = .../iter_2/gen_art/gen_art_experiment_3/   (method.py, method_out.json)\n#\n\
  # ---- REUSE (copy these functions VERBATIM from E1/method.py; they are tested) \n#   JumpReLUSAE, load_sae(params_file),\
  \ ModelBundle, sae_encode_np(sae,h,torch,keep_latents=...)\n#       (JumpReLU firing = encode>0; hook 'blocks.12.hook_resid_post'\
  \ / layer 12 resid_post)\n#   _find_token_idx(offsets, span), load_data(path), build_letter_struct(rows, carriers)\n#  \
  \ paired_bootstrap_diff(a,b,B=10000,rng), mcnemar_p, jaccard, auc\n#   unit_definition(...) -> per-member logit_lens_tokens(top-10\
  \ of E@W_dec) + top corpus contexts\n#   SAE config (from E1/method_out.json.metadata.config):\n#       release='google/gemma-scope-2b-pt-res',\
  \ sae_id='layer_12/width_16k/average_l0_82/params.npz',\n#       model='unsloth/gemma-2-2b', hook_layer=12, seed=1234. Gating\
  \ expected cosine~0.92 (assert >0.9).\n#\n# ============================================================================\n\
  # STAGE 0 - SETUP & CANONICAL UNITS\n# ============================================================================\n# 0.1\
  \  uv venv; deps: torch, numpy, scipy, scikit-learn, transformers, huggingface_hub,\n#      safetensors, requests, datasets\
  \ (pin same versions as E1/pyproject.toml). Log to logs/run.log.\n# 0.2  Load SAE + ModelBundle (gemma-2-2b on cuda, bf16/fp16).\
  \ Run gating_check; assert cosine>0.9.\n# 0.3  CANONICAL UNITS (read iter-2 outputs = deterministic, seed 1234):\n#    \
  \  FL = json.load(E1/method_out.json)['per_letter']   # keys L,O,T,I,D\n#        For each letter: anchor (FL[L]['anchor']),\
  \ K-track members (FL[L] members[].latent + role),\n#        kg edges = [(anchor, absorber) for absorbers], k_trace gains,\
  \ anchor recall fields.\n#        Known: L anchor=205 -> absorbers incl 3069('list'), 4736('linking/limiting'), 607, 8463...\n\
  #               O anchor=12334; T anchor=6355; D anchor=6210; I anchor=1227 (SPURIOUS: 0% corpus fire).\n#      TX = json.load(E3/method_out.json)\
  \  # taxonomic block\n#        anchor=3792 (anchor_recall_corpus 0.953, holes_corpus 253);\n#        k_track_unit=[3792,4697,9339,8442];\
  \ kg_edges: 3792->4697 'Georgia', ->9339 'Jordan', ->8442;\n#        non_triviality_passing_absorbers (diagnostic-corroborated,\
  \ higher subctx_precision):\n#               16009 'Georgia'(0.955), 540 'Jordan', 8347 'Jordan', 846 'United States', 3980\
  \ 'Georgia'...\n#      RECORD both the K-track-emitted KG edge AND the diagnostic-corroborated absorber per sub-context\n\
  #      (they can differ: K-track Georgia=4697 subctx_prec 0.35 vs diagnostic Georgia=16009 subctx_prec 0.955).\n# 0.4  CROSS-CHECK\
  \ (re-derivation, robustness, NOT load-bearing): re-run the two-track K-track proposal\n#      (reuse E1/method.py run_letter\
  \ K-track block; spec in art_RidEJtBC7gPT) on re-encoded data and assert\n#      the re-derived anchor+absorber member sets\
  \ match the canonical sets above (report any drift; proceed\n#      with the canonical iter-2 sets as the units of record).\
  \ If re-derivation diverges, log + use canonical.\n#\n# ============================================================================\n\
  # STAGE 1 - RE-ENCODE DATA (the only heavy GPU step)\n# ============================================================================\n\
  # For FIRST-LETTER (per letter) and TAXONOMIC:\n#   rows = load_data(D1 or D2); split into:\n#     content_flip pairs (metadata_pair_type=='content_flip',\
  \ roles on/off, linked by metadata_pair_id),\n#     corpus_context rows (real windows; carry metadata_sub_context = covered\
  \ word / country, and 'input' text,\n#         token_position/target span for word-token localization, fold for held-out\
  \ splits).\n#   Encode residuals at layer 12 for: (i) content-flip on/off instances, (ii) ALL corpus windows.\n#     Use\
  \ _find_token_idx on the target span to take the SAE activation at the word-token position\n#     (same as iter-2). Memory-safe\
  \ batch=32-64 forward passes; free activations after encoding.\n#   For efficiency, sae_encode_np(..., keep_latents=UNION\
  \ of all member latents + a pool of candidate\n#     content-responsive latents) so the activation matrix is small (|latents|\
  \ x n_windows), not 16k-wide.\n#   CONTENT-RESPONSIVE SET per concept: reuse iter-2 definition (r_l = a_l(on)-a_l(off) above\
  \ shuffle null,\n#     fires on x_on); for L this is ~373 latents, taxonomic ~684. Persist the responsive-latent index list.\n\
  #   Cache encoded matrices to disk (npz) keyed by concept so repair-loop + member-labeling reuse them.\n#\n# ============================================================================\n\
  # STAGE 2 - M5a: KG-GUIDED REPAIR LOOP  (load-bearing)\n# ============================================================================\n\
  # DETECTION/RECALL primitive (matches iter-2 _e2_finish): a latent set S 'detects' a window w iff\n#   pooled_max_{l in\
  \ S} encode_l(w) > 0  (i.e. some member fires). recall_on(X, S) = mean over corpus\n#   windows with metadata_sub_context==X\
  \ of detect(w,S).\n#\n# 2.1  IDENTIFY UNDER-SERVED SUB-CONTEXTS (recall holes) - data-driven, on TRAIN/diagnostic-A split:\n\
  #      For each concept, for each candidate sub-context X (word for first-letter; country for taxonomic)\n#      that has\
  \ >= N_MIN corpus windows (use >=30; relax to >=15 if too few), compute\n#         r_anchor(X) = recall_on(X, {anchor})\
  \   on the SELECTION split.\n#      An under-served sub-context = X with low r_anchor(X) (e.g. <=0.5) AND for which the\
  \ emitted KG names\n#      a covering absorber (an edge anchor->absorber with specializes==X, or for first-letter the absorber\n\
  #      whose dominant top-corpus sub_context == X, e.g. 3069 for 'list'). Select the TOP under-served X's\n#      per concept\
  \ (cap ~6 per concept to bound LLM/compute). Record r_anchor(X), n_windows, KG-absorber id.\n#      Taxonomic primary targets:\
  \ Georgia, Jordan, United States (KG edges 4697/9339/8442 +\n#      diagnostic 16009/540/846). First-letter L target: 'list'(3069)\
  \ and other absorber-covered words.\n#      NOTE letter I: anchor 1227 fires ~0% on corpus -> anchor recall ~0 EVERYWHERE\
  \ (degenerate). Handle\n#      via the parent-validation step (require anchor corpus-fire>floor); if anchor invalid, either\
  \ (a) use\n#      the highest-corpus-recall content-responsive latent as a surrogate parent, or (b) flag I as a case\n#\
  \      where no valid parent exists and report the repair loop as N/A for I (honest negative). Run L,O,T,D + tax.\n#\n#\
  \ 2.2  KG-GUIDED EDIT vs RANDOM-ADDITION CONTROL - measure on HELD-OUT EVALUATION split (corpus fold\n#      disjoint from\
  \ the selection split; first-letter has 5 doc folds, taxonomic has train/diagnostic 50/50):\n#      W = held-out corpus\
  \ windows with sub_context==X (the under-served sub-context).\n#      base_detect   = detect(w, {anchor})              \
  \         for w in W   (binary vector)\n#      kg_detect     = detect(w, {anchor, kg_absorber(X)})       for w in W\n# \
  \     gain_kg       = mean(kg_detect) - mean(base_detect)       # recall recovery from the KG-named latent\n#      RANDOM\
  \ CONTROL: draw R=500-1000 latents r_i at random from the content-responsive set\n#        EXCLUDING current unit members;\
  \ for each: rand_detect_i = detect(w,{anchor,r_i});\n#        gain_rand_i = mean(rand_detect_i)-mean(base_detect). Build\
  \ the gain_rand distribution.\n#      REPORT per (concept,X):\n#        - recall_anchor(X), recall_anchor+kg(X), gain_kg\n\
  #        - random-addition gain distribution: mean, sd, 5/50/95 percentiles\n#        - KG percentile = fraction of gain_rand\
  \ < gain_kg (success if >=0.95)\n#        - PAIRED BOOTSTRAP CI (B>=10,000, resample windows in W): diff per window =\n\
  #            kg_detect - mean_i(rand_detect_i)  -> CI of (gain_kg - mean random gain); success = CI excludes 0 & >0.\n#\
  \        - Also report the DIAGNOSTIC-corroborated absorber variant (e.g. 16009 for Georgia) as a second row\n#        \
  \  (high-subctx-precision specialist), since K-track edge and diagnostic edge can differ.\n#      AGGREGATE: per-concept\
  \ mean gain_kg vs mean random gain (descriptive); count of (concept,X) where\n#      CI excludes 0 = number of MEASURED\
  \ successful KG-localized repairs. >=1 success => M5 KG-utility met.\n#      HONEST NEGATIVE: if gain_kg ties/loses to the\
  \ random distribution on a concept, report it verbatim as\n#      'auditability buys no measurable fix on <concept/X>'.\n\
  #\n# 2.3  (k) LOCALIZATION-FAILURE CHECK (confirm KG localizes a fix that (k) cannot):\n#      Build the label-free group-inference\
  \ probe (k) per art_RidEJtBC7gPT spec on DENSE residuals:\n#        - JTT variant: train ERM logistic probe on concept (parent\
  \ label, e.g. starts-with-L / is-country) on\n#          residual deltas; identify high-loss (error-set) TRAIN examples;\
  \ upweight (lambda~20) and retrain.\n#        - GEORGE variant (optional, time-permitting): cluster ERM penultimate reps\
  \ (KMeans, k=#sub-contexts),\n#          treat clusters as groups, retrain with group-DRO. Use one variant as primary, the\
  \ other if budget.\n#      (k) OUTPUT IS EXAMPLE-LEVEL (a reweighted dense hyperplane), not a latent to add. To MEASURE\
  \ that it\n#      cannot localize the fix to a single SAE feature: project the (k) probe direction w_k onto the SAE\n# \
  \     decoder dictionary (cos(w_k, W_dec[l]) for all l); report that NO single latent dominates / the KG-named\n#      absorber\
  \ is NOT the argmax (or its projection is small), i.e. (k) provides no per-sub-context FEATURE to\n#      add - whereas\
  \ the KG names exactly latent 3069/4697/16009. Also report: (k)'s worst-sub-context recall on\n#      X (does retraining\
  \ even help X?) vs the KG repair. Conclusion line: KG localizes an addable, auditable\n#      unit; (k) reweights examples\
  \ and exposes no such unit.\n#\n# ============================================================================\n# STAGE\
  \ 3 - M5b: LLM-JUDGE MEMBER-LABELING  (load-bearing)\n# ============================================================================\n\
  # 3.1  BUILD EVIDENCE per unit member (anchor + absorbers), per concept, NON-LEAKY:\n#      logit_lens = top-10 tokens of\
  \ E @ W_dec[m] (reuse unit_definition logic).\n#      top_windows = top-5 corpus windows by encode_m (RAW 'input' TEXT,\
  \ target word marked with **..**),\n#        WITH the metadata_sub_context LABEL WITHHELD from the prompt (only the text\
  \ is shown -> no leakage).\n#      ground_truth_subctx(m): anchor -> 'GENERAL parent (any word starting with <L> / any country)';\n\
  #        absorber -> its KG specializes value (4697->Georgia) OR, for first-letter, the modal sub_context of\n#        its\
  \ top corpus windows (3069->'list'). Persist the ground-truth assignment table.\n#      candidate_list(concept) = ['GENERAL\
  \ parent'] + sorted unique sub-contexts covered by the unit's members.\n# 3.2  JUDGE (OpenRouter via aii-openrouter-llms;\
  \ model anthropic/claude-haiku-4.5, temp 0; fallback\n#      google/gemini-3.1-flash-lite). FORCED-CHOICE prompt: 'A feature\
  \ in a language model activates most on\n#      these tokens <logit_lens> and most strongly in these text snippets <top_windows>.\
  \ Which ONE of the\n#      following best describes the specific concept/sub-context it detects? <candidate_list>. Answer\
  \ with\n#      exactly one option.' Parse the option; map to index. Track cumulative cost after EVERY call; hard stop\n\
  #      at $10, target <$3 (only ~100-150 members total -> well under $1; verify with a cost meter).\n# 3.3  SCORE: agreement\
  \ = mean over members of [judge_choice == ground_truth]. NULL: shuffle the ground-truth\n#      labels across members within\
  \ concept (and pooled), S=2000 shuffles, agreement_null distribution;\n#      report null mean (~1/|candidates| analytic\
  \ + empirical), and gap = agreement - null_mean with a\n#      bootstrap CI (resample members, B>=10,000). Report per-concept\
  \ and pooled. Also report a confusion\n#      table (which sub-contexts the judge confuses) and per-role accuracy (anchors\
  \ vs absorbers).\n#      SUCCESS: agreement gap CI excludes 0 (judge recovers member sub-contexts above chance => units\
  \ are\n#      human/LLM-auditable). HONEST NEGATIVE if it ties the null on a concept.\n#\n# ============================================================================\n\
  # STAGE 4 - OUTPUT\n# ============================================================================\n# method_out.json =\
  \ {\n#   metadata: {method_name, sae config, gating_check, seed, B_gap, n_shuffles, llm_model, cumulative_llm_cost_usd},\n\
  #   canonical_units: {first_letter:{L:{anchor,members,kg_edges},O:...,D:...,I:{spurious_anchor:true}},\n#              \
  \       taxonomic:{anchor:3792, k_track_unit, kg_edges, diagnostic_absorbers}},\n#   reproduction_crosscheck: {per-concept\
  \ member-set match vs iter-2 (bool + any drift)},\n#   repair_loop: { per-concept: per-(sub_context): {n_windows_eval, recall_anchor,\
  \ recall_anchor_plus_kg,\n#        gain_kg, kg_absorber_id, kg_percentile_vs_random, random_gain_{mean,sd,p5,p50,p95},\n\
  #        paired_bootstrap_CI_kg_minus_random:{diff,lo,hi,excl_0}, diagnostic_absorber_variant:{...}},\n#        n_measured_successful_repairs,\
  \ honest_negatives:[...] },\n#   k_localization_check: { variant, projection_argmax_latent, kg_absorber_projection_rank,\n\
  #        single_latent_dominates:false, k_worstgroup_recall_on_X, conclusion },\n#   member_labeling: { per-concept:{agreement,\
  \ null_mean, gap, bootstrap_CI, n_members, confusion},\n#        pooled:{agreement, null_mean, gap, CI}, per_role_accuracy\
  \ },\n#   verdict: { kg_utility_measured:bool (>=1 repair CI excludes 0), member_labeling_above_null:bool,\n#        replaces_iter2_assertion:true,\
  \ notes } }\n# Validate full/mini/preview via aii-json; assert each <100MB (data is small JSON; corpus text snippets\n#\
  \   are few -> trivial). Save logs + cost ledger.\n"
fallback_plan: |-
  GPU/SAE issues: (1) If gemma-scope npz download or HF gating fails, mirror via unsloth/gemma-2-2b (ungated, vocab 256000) for the model and pull the SAE params.npz from the google/gemma-scope-2b-pt-res repo (layer_12/width_16k/average_l0_82); the exact loader is already proven in E1/method.py - copy it verbatim rather than re-implementing. (2) If full-window encoding is too slow/OOM, encode only the word-token position per window with keep_latents restricted to the member set + a ~1000-latent content-responsive candidate pool (never the full 16k); batch=16; this is the dominant cost and is small.

  Repair-loop design fallbacks: (3) If a concept has too few held-out corpus windows for a sub-context (n<15), pool windows across the selection+eval splits but keep absorber-selection-vs-evaluation separation by using leave-one-fold-out (select KG absorber on 4 folds, evaluate on the 5th, rotate). (4) If the binary 'fires>0' recall is saturated (anchor already detects X), that X is NOT a hole - drop it and pick lower-recall sub-contexts; if NO concept has a genuine anchor hole (anchor recall ~1 everywhere), report that as the honest finding that the unit has no recall holes to repair (auditability claim then rests on member-labeling alone) - this is a publishable negative, not a failure. (5) If the KG-named K-track absorber (e.g. Georgia=4697, subctx_prec 0.35) does NOT beat the random control but the diagnostic-corroborated absorber (16009, subctx_prec 0.955) DOES, report both transparently: the conclusion becomes 'the diagnostic-corroborated KG edge localizes the repair; the bare max-coverage edge is noisier' (informative about which KG-edge type to trust). (6) Letter I (spurious anchor 1227): if no valid parent exists, mark I N/A and exclude from aggregate; do not fabricate a repair.

  (k) baseline fallback: (7) If a full JTT/GEORGE retrain is too costly, implement the minimal JTT (ERM probe -> high-loss upweight -> retrain) only; the load-bearing claim is the STRUCTURAL one (example-reweighting yields no per-feature unit to add), which the decoder-projection argmax demonstrates even with a single (k) variant. If (k) entirely fails to build, the repair-loop vs random-addition result still stands; report (k) as 'not run' rather than block.

  LLM-judge fallbacks: (8) If anthropic/claude-haiku-4.5 errors/rate-limits, fall back to google/gemini-3.1-flash-lite then deepseek/deepseek-v3.2; temp 0; retries with backoff. (9) If forced-choice parsing is unreliable, constrain output to a single integer index and re-ask once on parse failure. (10) Cost is tiny (~100-150 members) - if any cost spike appears, STOP at $3 and report partial member-labeling.

  Overall triage: the SINGLE must-deliver is >=1 MEASURED KG-utility number replacing the iter-2 '70-edge graph' assertion. Priority order if time-pressed: (i) taxonomic repair loop on Georgia/Jordan/US (strongest, diagnostic-corroborated) -> (ii) member-labeling (cheap, fast) -> (iii) first-letter repair loop -> (iv) (k) localization check. Always emit method_out.json with whatever landed + explicit per-result status flags.
testing_plan: |-
  Confirmation-signal-driven, gradual scaling (aii-long-running-tasks):

  T0 - SMOKE (no GPU, seconds): json.load both iter-2 method_out.json files and assert the canonical structures parse: FL has keys L/O/T/I/D each with 'anchor' and member 'role' entries (L anchor==205, members include 3069 & 4736; I anchor==1227); TX has anchor==3792, k_track_unit==[3792,4697,9339,8442], kg_edges with specializes in {Georgia,Jordan}, non_triviality_passing_absorbers includes 16009->Georgia. Load D1/D2, assert corpus_context rows carry metadata_sub_context + 'input' text + target span. Fail fast if any path/shape is wrong.

  T1 - SAE/GATING SANITY (GPU, ~3-5 min): load SAE+model via the copied E1 loader; run gating_check on a handful of windows; ASSERT reconstruction cosine>0.9 (expect ~0.924) and JumpReLU firing=encode>0 reproduces a known latent. Encode 20 first-letter-L corpus windows for anchor 205 and absorber 3069; ASSERT 3069 fires (>0) on >=1 'list'/'listing' window and anchor 205 fires on general-L windows - reproduces the iter-2 unit before scaling.

  T2 - REPAIR-LOOP MICRO (1 concept, 1 sub-context): run Stage-2 on taxonomic Georgia only with R=50 random draws and B=1000. CONFIRMATION SIGNALS: (a) recall_anchor(Georgia) is materially <1 (a real hole); (b) recall_anchor+kg(Georgia) > recall_anchor (the KG absorber recovers windows); (c) gain_kg lands high in the random-gain distribution. If gain_kg is NOT above most random draws even for Georgia (the hypothesis's strongest case, expected unit recall 0.713 vs h 0.520), STOP and debug detection/threshold/fold logic before scaling - this is the canary. Cross-check the recall numbers are in the plausible regime of iter-2's taxonomic recall (~0.7).

  T3 - MEMBER-LABELING MICRO (3 members, 1 LLM call each): build evidence for anchor 205, absorber 3069('list'), absorber 4736('linking'); run the forced-choice judge; ASSERT the judge maps 3069->'list'-like and 4736->'linking'-like and 205->GENERAL more often than chance on this tiny set; verify cost ledger increments and stays <$0.05. Confirms prompt + parsing + cost tracking before the full sweep.

  T4 - FULL SCALE: run all concepts (L,O,T,D + taxonomic; I handled per spurious-anchor rule) with R=500-1000, B>=10,000, S=2000 shuffles. Monitor logs/run.log via PID-based tail. After completion, validate: every repair_loop entry has a paired-bootstrap CI; member_labeling has gap+CI; cumulative_llm_cost_usd recorded and <$3; method_out.json + variants <100MB via aii-json. Sanity: number of MEASURED successful repairs >=1 (else the run is reportable but flags kg_utility_measured=false honestly). Spot-check 2-3 repair rows by hand: gain_kg, random p95, and CI signs must be internally consistent (CI>0 iff gain_kg>random mean).

  GUARDRAILS: keep_latents must restrict encoding width (never materialize 16k x n); free GPU tensors between concepts; assert no NaN in recall/gain; assert eval windows are disjoint from selection windows (fold check) so the repair test is not circular; never overwrite the read-only iter-1/iter-2 artifacts.
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

### [2] HUMAN-USER prompt · 2026-06-17 18:27:30 UTC

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

### [3] SKILL-INPUT — aii-long-running-tasks · 2026-06-17 18:27:44 UTC

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

### [4] SKILL-INPUT — aii-use-hardware · 2026-06-17 18:27:44 UTC

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

### [5] SKILL-INPUT — aii-python · 2026-06-17 18:27:58 UTC

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

### [6] SKILL-INPUT — aii-json · 2026-06-17 18:27:58 UTC

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

### [7] SKILL-INPUT — aii-openrouter-llms · 2026-06-17 18:41:14 UTC

The agent loaded the **aii-openrouter-llms** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-openrouter-llms
description: Searches and calls LLMs from OpenRouter's extensive catalog (Claude, GPT, Gemini, Llama, Mistral, DeepSeek, etc.) with reasoning and temperature control. Use when user needs to access various LLMs, compare language models, call different model providers, find the best model for a task, or look up model pricing and costs per million tokens.
---

## Contents

- Workflow (2-phase model discovery and calling)
- Scripts (Search, Get Params, Call)

**IMPORTANT - Parallel execution:** GNU `parallel` subshells do NOT inherit `source activate`. Use `export` for variables and **single-quoted** command templates so parallel's subshells can resolve them:
```
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

---

## Workflow: Model Discovery and Calling

### Phase 1: Search for Models
Find models with pricing, context length, and descriptions
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_search_llms.py "claude" --limit 5
```

### Phase 2 (optional): Get Model Parameters
Check what parameters a specific model supports
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_get_llm_params.py "anthropic/claude-haiku-4.5"
```

### Phase 3: Call Model
Call a model using the API name from search results
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py --model "anthropic/claude-haiku-4.5" --input "What is 2+2?"
```

---

## Scripts

### Search OpenRouter models (aii_or_search_llms.py)

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_search_llms.py "claude" --limit 5
```

**Parallel execution (multiple queries):**

IMPORTANT: When running multiple searches, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_or_search_llms.py" && \
parallel -j 50 -k --group --will-cite '$PY $S {} --limit 5' ::: 'claude' 'gpt' 'gemini'
```

**Example output:**
```
Found 5 models for query: claude

[1] Anthropic: Claude Opus 4.5
    API: anthropic/claude-opus-4.5
    Context: 200,000 tokens
    Price: $5.00/M in, $25.00/M out
    Claude Opus 4.5 is Anthropic's frontier reasoning model...

[2] Anthropic: Claude Haiku 4.5
    API: anthropic/claude-haiku-4.5
    Context: 200,000 tokens
    Price: $1.00/M in, $5.00/M out
    ...
```

**Parameters:**

`query` (optional, positional)
- Search query to filter models (e.g., 'claude', 'gpt', 'reasoning')

`--limit, -n` (optional)
- Maximum number of results (default: 10)

`--series, -s` (optional)
- Filter by model family
- Valid: GPT, Claude, Gemini, Grok, Cohere, Nova, Qwen, Yi, DeepSeek, Mistral, Llama2, Llama3, Llama4, RWKV, Qwen3, Router, Media, Other, PaLM

`--timeout` (optional)
- Request timeout in seconds (default: 60)

**Tips:**
- Use the `API` field from results for the `--model` parameter in calls
- Search is fast (queries OpenRouter's model list)

---

### Get model parameters (aii_or_get_llm_params.py)

Get detailed information and supported parameters for a specific model.

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_get_llm_params.py "anthropic/claude-haiku-4.5"
```

**Parallel execution (multiple models):**

IMPORTANT: When checking multiple models, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_or_get_llm_params.py" && \
parallel -j 50 -k --group --will-cite '$PY $S {}' ::: 'anthropic/claude-haiku-4.5' 'openai/gpt-4o-mini' 'google/gemini-2.0-flash-001'
```

**Example output:**
```
Model: Anthropic: Claude Haiku 4.5
API: anthropic/claude-haiku-4.5

=== Capabilities ===
Context Length: 200,000 tokens
Max Output: 64,000 tokens
Modality: text+image->text
Input: image, text
Output: text
Moderated: Yes

=== Pricing ===
Input: $1.0000/M tokens
Output: $5.0000/M tokens

=== Supported Parameters ===
  - include_reasoning
  - max_tokens
  - reasoning
  - stop
  - temperature
  - tool_choice
  - tools
  - top_k
  - top_p
```

**Parameters:**

`model` (required, positional)
- Model API name (e.g., 'anthropic/claude-haiku-4.5', 'openai/o1')

`--timeout` (optional)
- Request timeout in seconds (default: 30)

**Tips:**
- Use after search to see which parameters a model supports
- Check supported_parameters before using --reasoning or other options

---

### Call OpenRouter model (aii_or_call_llms.py)

Make an API call to an OpenRouter LLM model.

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py --model "anthropic/claude-haiku-4.5" --input "What is 2+2?"
```

**Parallel execution (multiple calls):**

IMPORTANT: When calling multiple models, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_or_call_llms.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --model {} --input "What is 2+2?"' ::: 'anthropic/claude-haiku-4.5' 'openai/gpt-4o-mini' 'google/gemini-2.0-flash-001'
```

**Example output:**
```
Model: anthropic/claude-haiku-4.5

Response:
Four.

Tokens: 12 in, 5 out
```

**Parameters:**

`--model, -m` (required)
- API model name from search results (format: `provider/model-name`)
- Examples: `anthropic/claude-sonnet-4`, `openai/gpt-5`, `google/gemini-2.5-pro`

`--input, -i` (required, unless using --input-json)
- Simple string prompt

`--input-json` (optional)
- Full conversation JSON for multi-turn (mutually exclusive with --input)

`--max-tokens` (optional)
- Maximum output tokens (default: 9000)

`--reasoning` (optional)
- Reasoning effort for reasoning models: `minimal`, `low`, `medium`, `high`

`--temperature, -t` (optional)
- Randomness (0.0-2.0): 0.0=deterministic, 0.7=balanced, 1.5+=creative

`--top-p` (optional)
- Nucleus sampling (0.0-1.0)

`--instructions` (optional)
- System instructions/prompt

`--web-search` (optional)
- Enable web search with max results (e.g., 10)

`--params, -p` (optional)
- Extra model-specific parameters as JSON string
- Use `aii_or_get_llm_params.py` to see which params a model supports
- Example: `--params '{"top_k": 50, "seed": 42, "frequency_penalty": 0.5}'`

`--timeout` (optional)
- Request timeout in seconds (default: 120)

**Examples:**

Simple call:
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py \
  --model "anthropic/claude-sonnet-4" \
  --input "Write a haiku about coding" \
  --temperature 0.8
```

With system instructions:
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py \
  --model "anthropic/claude-haiku-4.5" \
  --input "Explain recursion" \
  --instructions "You are a helpful programming tutor. Keep explanations concise."
```

With reasoning (for o1-style models):
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py \
  --model "openai/o1" \
  --input "Solve this complex math problem" \
  --reasoning high
```

With web search:
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py \
  --model "anthropic/claude-sonnet-4" \
  --input "What are the latest AI news?" \
  --web-search 10 \
  --max-tokens 15000
```

With extra model-specific params:
```bash
# Step 1: Check what params the model supports
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_get_llm_params.py "meta-llama/llama-3.3-70b-instruct"
# Shows: frequency_penalty, top_k, seed, min_p, etc.

# Step 2: Call with those params
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py \
  --model "meta-llama/llama-3.3-70b-instruct" \
  --input "Write a short poem" \
  --params '{"top_k": 50, "seed": 42, "frequency_penalty": 0.5}'
```

---

## Tips

- Use `aii_or_search_llms.py` first to find models, then copy `API` field for `--model`
- Use `aii_or_get_llm_params.py` to check what params a model supports before using `--params`
- For web search, increase `--max-tokens` to handle larger responses (15000+)

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [8] SYSTEM-USER prompt · 2026-06-17 19:05:11 UTC

```
continue
```

### [9] SYSTEM-USER prompt · 2026-06-17 19:05:19 UTC

```
continue
```

### [10] SYSTEM-USER prompt · 2026-06-17 19:05:27 UTC

```
continue
```

### [11] SYSTEM-USER prompt · 2026-06-17 19:05:37 UTC

```
continue
```

### [12] SYSTEM-USER prompt · 2026-06-17 19:05:59 UTC

```
continue
```

### [13] SYSTEM-USER prompt · 2026-06-17 19:06:03 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_3`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_3/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_3/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_3/results/out.json`
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
id: gen_plan_experiment_3_idx3
type: experiment
title: >-
  Measure Auditability (M5): KG-Guided Repair Loop + LLM-Judge Member-Labeling for Two-Track CCRG Units (First-Letter + Taxonomic)
summary: >-
  Execute the two previously-dropped, now load-bearing auditability results for the two-track CCRG units on a frozen Gemma-Scope
  L12/16k SAE. (a) KG-GUIDED REPAIR LOOP: for each under-served sub-context (recall hole where the parent/anchor latent goes
  silent), ADD the KG-named covering absorber (max-pool) and MEASURE recall recovery on HELD-OUT corpus windows with a paired
  bootstrap CI (B>=10,000), versus a random-content-responsive-latent-addition control (averaged over many draws); success
  = KG-guided-minus-random gain CI excludes 0; plus confirm the label-free group-inference probe (k) cannot localize the fix
  to a single addable latent. (b) MEMBER-LABELING: for each unit member, assemble its logit-lens top tokens + raw top-activating
  corpus windows, send to an OpenRouter LLM judge (anthropic/claude-haiku-4.5) for forced-choice sub-context naming, score
  agreement vs a shuffled-label null with bootstrap CI. Reuse the iter-2 SAE loader/hook/firing/unit-definition/recall code
  verbatim and read iter-2 canonical units/KG; re-derive as a cross-check. At least one MEASURED KG-utility result must replace
  the iter-2 'we emit a 70-edge graph' assertion. Report honest negatives (a tie with the random-addition control = 'auditability
  buys no measurable fix there').
runpod_compute_profile: gpu
implementation_pseudocode: "# ============================================================================\n# EXPERIMENT iter3_dir3\
  \ - MEASURE AUDITABILITY (M5)\n# Compute: gpu (A4500 20GB). Wall-clock target <4h. LLM cap $10, target <$3.\n# Output: method_out.json\
  \ (+ full/mini/preview), all <100MB.\n# ============================================================================\n#\n\
  # ---- ABSOLUTE PATHS (read-only inputs; do NOT mutate) -----------------------\n# FIRST-LETTER dataset (art_dpYpjSn2Xvg3):\n\
  #   D1 = /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json\n\
  # TAXONOMIC/NUMERIC dataset (art_t2uUbjSwpd3t):\n#   D2 = /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_2/full_data_out.json\n\
  # Method dossier (art_RidEJtBC7gPT): .../iter_1/gen_art/gen_art_research_1/research_out.json\n# Diagnostic+data dossier\
  \ (art_I2MrezW41iQo): .../iter_1/gen_art/gen_art_research_2/research_out.json\n# iter-2 EXECUTED first-letter run (canonical\
  \ units/KG + reusable code):\n#   E1 = .../iter_2/gen_art/gen_art_experiment_1/   (method.py, method_out.json)\n# iter-2\
  \ EXECUTED taxonomic/numeric run:\n#   E3 = .../iter_2/gen_art/gen_art_experiment_3/   (method.py, method_out.json)\n#\n\
  # ---- REUSE (copy these functions VERBATIM from E1/method.py; they are tested) \n#   JumpReLUSAE, load_sae(params_file),\
  \ ModelBundle, sae_encode_np(sae,h,torch,keep_latents=...)\n#       (JumpReLU firing = encode>0; hook 'blocks.12.hook_resid_post'\
  \ / layer 12 resid_post)\n#   _find_token_idx(offsets, span), load_data(path), build_letter_struct(rows, carriers)\n#  \
  \ paired_bootstrap_diff(a,b,B=10000,rng), mcnemar_p, jaccard, auc\n#   unit_definition(...) -> per-member logit_lens_tokens(top-10\
  \ of E@W_dec) + top corpus contexts\n#   SAE config (from E1/method_out.json.metadata.config):\n#       release='google/gemma-scope-2b-pt-res',\
  \ sae_id='layer_12/width_16k/average_l0_82/params.npz',\n#       model='unsloth/gemma-2-2b', hook_layer=12, seed=1234. Gating\
  \ expected cosine~0.92 (assert >0.9).\n#\n# ============================================================================\n\
  # STAGE 0 - SETUP & CANONICAL UNITS\n# ============================================================================\n# 0.1\
  \  uv venv; deps: torch, numpy, scipy, scikit-learn, transformers, huggingface_hub,\n#      safetensors, requests, datasets\
  \ (pin same versions as E1/pyproject.toml). Log to logs/run.log.\n# 0.2  Load SAE + ModelBundle (gemma-2-2b on cuda, bf16/fp16).\
  \ Run gating_check; assert cosine>0.9.\n# 0.3  CANONICAL UNITS (read iter-2 outputs = deterministic, seed 1234):\n#    \
  \  FL = json.load(E1/method_out.json)['per_letter']   # keys L,O,T,I,D\n#        For each letter: anchor (FL[L]['anchor']),\
  \ K-track members (FL[L] members[].latent + role),\n#        kg edges = [(anchor, absorber) for absorbers], k_trace gains,\
  \ anchor recall fields.\n#        Known: L anchor=205 -> absorbers incl 3069('list'), 4736('linking/limiting'), 607, 8463...\n\
  #               O anchor=12334; T anchor=6355; D anchor=6210; I anchor=1227 (SPURIOUS: 0% corpus fire).\n#      TX = json.load(E3/method_out.json)\
  \  # taxonomic block\n#        anchor=3792 (anchor_recall_corpus 0.953, holes_corpus 253);\n#        k_track_unit=[3792,4697,9339,8442];\
  \ kg_edges: 3792->4697 'Georgia', ->9339 'Jordan', ->8442;\n#        non_triviality_passing_absorbers (diagnostic-corroborated,\
  \ higher subctx_precision):\n#               16009 'Georgia'(0.955), 540 'Jordan', 8347 'Jordan', 846 'United States', 3980\
  \ 'Georgia'...\n#      RECORD both the K-track-emitted KG edge AND the diagnostic-corroborated absorber per sub-context\n\
  #      (they can differ: K-track Georgia=4697 subctx_prec 0.35 vs diagnostic Georgia=16009 subctx_prec 0.955).\n# 0.4  CROSS-CHECK\
  \ (re-derivation, robustness, NOT load-bearing): re-run the two-track K-track proposal\n#      (reuse E1/method.py run_letter\
  \ K-track block; spec in art_RidEJtBC7gPT) on re-encoded data and assert\n#      the re-derived anchor+absorber member sets\
  \ match the canonical sets above (report any drift; proceed\n#      with the canonical iter-2 sets as the units of record).\
  \ If re-derivation diverges, log + use canonical.\n#\n# ============================================================================\n\
  # STAGE 1 - RE-ENCODE DATA (the only heavy GPU step)\n# ============================================================================\n\
  # For FIRST-LETTER (per letter) and TAXONOMIC:\n#   rows = load_data(D1 or D2); split into:\n#     content_flip pairs (metadata_pair_type=='content_flip',\
  \ roles on/off, linked by metadata_pair_id),\n#     corpus_context rows (real windows; carry metadata_sub_context = covered\
  \ word / country, and 'input' text,\n#         token_position/target span for word-token localization, fold for held-out\
  \ splits).\n#   Encode residuals at layer 12 for: (i) content-flip on/off instances, (ii) ALL corpus windows.\n#     Use\
  \ _find_token_idx on the target span to take the SAE activation at the word-token position\n#     (same as iter-2). Memory-safe\
  \ batch=32-64 forward passes; free activations after encoding.\n#   For efficiency, sae_encode_np(..., keep_latents=UNION\
  \ of all member latents + a pool of candidate\n#     content-responsive latents) so the activation matrix is small (|latents|\
  \ x n_windows), not 16k-wide.\n#   CONTENT-RESPONSIVE SET per concept: reuse iter-2 definition (r_l = a_l(on)-a_l(off) above\
  \ shuffle null,\n#     fires on x_on); for L this is ~373 latents, taxonomic ~684. Persist the responsive-latent index list.\n\
  #   Cache encoded matrices to disk (npz) keyed by concept so repair-loop + member-labeling reuse them.\n#\n# ============================================================================\n\
  # STAGE 2 - M5a: KG-GUIDED REPAIR LOOP  (load-bearing)\n# ============================================================================\n\
  # DETECTION/RECALL primitive (matches iter-2 _e2_finish): a latent set S 'detects' a window w iff\n#   pooled_max_{l in\
  \ S} encode_l(w) > 0  (i.e. some member fires). recall_on(X, S) = mean over corpus\n#   windows with metadata_sub_context==X\
  \ of detect(w,S).\n#\n# 2.1  IDENTIFY UNDER-SERVED SUB-CONTEXTS (recall holes) - data-driven, on TRAIN/diagnostic-A split:\n\
  #      For each concept, for each candidate sub-context X (word for first-letter; country for taxonomic)\n#      that has\
  \ >= N_MIN corpus windows (use >=30; relax to >=15 if too few), compute\n#         r_anchor(X) = recall_on(X, {anchor})\
  \   on the SELECTION split.\n#      An under-served sub-context = X with low r_anchor(X) (e.g. <=0.5) AND for which the\
  \ emitted KG names\n#      a covering absorber (an edge anchor->absorber with specializes==X, or for first-letter the absorber\n\
  #      whose dominant top-corpus sub_context == X, e.g. 3069 for 'list'). Select the TOP under-served X's\n#      per concept\
  \ (cap ~6 per concept to bound LLM/compute). Record r_anchor(X), n_windows, KG-absorber id.\n#      Taxonomic primary targets:\
  \ Georgia, Jordan, United States (KG edges 4697/9339/8442 +\n#      diagnostic 16009/540/846). First-letter L target: 'list'(3069)\
  \ and other absorber-covered words.\n#      NOTE letter I: anchor 1227 fires ~0% on corpus -> anchor recall ~0 EVERYWHERE\
  \ (degenerate). Handle\n#      via the parent-validation step (require anchor corpus-fire>floor); if anchor invalid, either\
  \ (a) use\n#      the highest-corpus-recall content-responsive latent as a surrogate parent, or (b) flag I as a case\n#\
  \      where no valid parent exists and report the repair loop as N/A for I (honest negative). Run L,O,T,D + tax.\n#\n#\
  \ 2.2  KG-GUIDED EDIT vs RANDOM-ADDITION CONTROL - measure on HELD-OUT EVALUATION split (corpus fold\n#      disjoint from\
  \ the selection split; first-letter has 5 doc folds, taxonomic has train/diagnostic 50/50):\n#      W = held-out corpus\
  \ windows with sub_context==X (the under-served sub-context).\n#      base_detect   = detect(w, {anchor})              \
  \         for w in W   (binary vector)\n#      kg_detect     = detect(w, {anchor, kg_absorber(X)})       for w in W\n# \
  \     gain_kg       = mean(kg_detect) - mean(base_detect)       # recall recovery from the KG-named latent\n#      RANDOM\
  \ CONTROL: draw R=500-1000 latents r_i at random from the content-responsive set\n#        EXCLUDING current unit members;\
  \ for each: rand_detect_i = detect(w,{anchor,r_i});\n#        gain_rand_i = mean(rand_detect_i)-mean(base_detect). Build\
  \ the gain_rand distribution.\n#      REPORT per (concept,X):\n#        - recall_anchor(X), recall_anchor+kg(X), gain_kg\n\
  #        - random-addition gain distribution: mean, sd, 5/50/95 percentiles\n#        - KG percentile = fraction of gain_rand\
  \ < gain_kg (success if >=0.95)\n#        - PAIRED BOOTSTRAP CI (B>=10,000, resample windows in W): diff per window =\n\
  #            kg_detect - mean_i(rand_detect_i)  -> CI of (gain_kg - mean random gain); success = CI excludes 0 & >0.\n#\
  \        - Also report the DIAGNOSTIC-corroborated absorber variant (e.g. 16009 for Georgia) as a second row\n#        \
  \  (high-subctx-precision specialist), since K-track edge and diagnostic edge can differ.\n#      AGGREGATE: per-concept\
  \ mean gain_kg vs mean random gain (descriptive); count of (concept,X) where\n#      CI excludes 0 = number of MEASURED\
  \ successful KG-localized repairs. >=1 success => M5 KG-utility met.\n#      HONEST NEGATIVE: if gain_kg ties/loses to the\
  \ random distribution on a concept, report it verbatim as\n#      'auditability buys no measurable fix on <concept/X>'.\n\
  #\n# 2.3  (k) LOCALIZATION-FAILURE CHECK (confirm KG localizes a fix that (k) cannot):\n#      Build the label-free group-inference\
  \ probe (k) per art_RidEJtBC7gPT spec on DENSE residuals:\n#        - JTT variant: train ERM logistic probe on concept (parent\
  \ label, e.g. starts-with-L / is-country) on\n#          residual deltas; identify high-loss (error-set) TRAIN examples;\
  \ upweight (lambda~20) and retrain.\n#        - GEORGE variant (optional, time-permitting): cluster ERM penultimate reps\
  \ (KMeans, k=#sub-contexts),\n#          treat clusters as groups, retrain with group-DRO. Use one variant as primary, the\
  \ other if budget.\n#      (k) OUTPUT IS EXAMPLE-LEVEL (a reweighted dense hyperplane), not a latent to add. To MEASURE\
  \ that it\n#      cannot localize the fix to a single SAE feature: project the (k) probe direction w_k onto the SAE\n# \
  \     decoder dictionary (cos(w_k, W_dec[l]) for all l); report that NO single latent dominates / the KG-named\n#      absorber\
  \ is NOT the argmax (or its projection is small), i.e. (k) provides no per-sub-context FEATURE to\n#      add - whereas\
  \ the KG names exactly latent 3069/4697/16009. Also report: (k)'s worst-sub-context recall on\n#      X (does retraining\
  \ even help X?) vs the KG repair. Conclusion line: KG localizes an addable, auditable\n#      unit; (k) reweights examples\
  \ and exposes no such unit.\n#\n# ============================================================================\n# STAGE\
  \ 3 - M5b: LLM-JUDGE MEMBER-LABELING  (load-bearing)\n# ============================================================================\n\
  # 3.1  BUILD EVIDENCE per unit member (anchor + absorbers), per concept, NON-LEAKY:\n#      logit_lens = top-10 tokens of\
  \ E @ W_dec[m] (reuse unit_definition logic).\n#      top_windows = top-5 corpus windows by encode_m (RAW 'input' TEXT,\
  \ target word marked with **..**),\n#        WITH the metadata_sub_context LABEL WITHHELD from the prompt (only the text\
  \ is shown -> no leakage).\n#      ground_truth_subctx(m): anchor -> 'GENERAL parent (any word starting with <L> / any country)';\n\
  #        absorber -> its KG specializes value (4697->Georgia) OR, for first-letter, the modal sub_context of\n#        its\
  \ top corpus windows (3069->'list'). Persist the ground-truth assignment table.\n#      candidate_list(concept) = ['GENERAL\
  \ parent'] + sorted unique sub-contexts covered by the unit's members.\n# 3.2  JUDGE (OpenRouter via aii-openrouter-llms;\
  \ model anthropic/claude-haiku-4.5, temp 0; fallback\n#      google/gemini-3.1-flash-lite). FORCED-CHOICE prompt: 'A feature\
  \ in a language model activates most on\n#      these tokens <logit_lens> and most strongly in these text snippets <top_windows>.\
  \ Which ONE of the\n#      following best describes the specific concept/sub-context it detects? <candidate_list>. Answer\
  \ with\n#      exactly one option.' Parse the option; map to index. Track cumulative cost after EVERY call; hard stop\n\
  #      at $10, target <$3 (only ~100-150 members total -> well under $1; verify with a cost meter).\n# 3.3  SCORE: agreement\
  \ = mean over members of [judge_choice == ground_truth]. NULL: shuffle the ground-truth\n#      labels across members within\
  \ concept (and pooled), S=2000 shuffles, agreement_null distribution;\n#      report null mean (~1/|candidates| analytic\
  \ + empirical), and gap = agreement - null_mean with a\n#      bootstrap CI (resample members, B>=10,000). Report per-concept\
  \ and pooled. Also report a confusion\n#      table (which sub-contexts the judge confuses) and per-role accuracy (anchors\
  \ vs absorbers).\n#      SUCCESS: agreement gap CI excludes 0 (judge recovers member sub-contexts above chance => units\
  \ are\n#      human/LLM-auditable). HONEST NEGATIVE if it ties the null on a concept.\n#\n# ============================================================================\n\
  # STAGE 4 - OUTPUT\n# ============================================================================\n# method_out.json =\
  \ {\n#   metadata: {method_name, sae config, gating_check, seed, B_gap, n_shuffles, llm_model, cumulative_llm_cost_usd},\n\
  #   canonical_units: {first_letter:{L:{anchor,members,kg_edges},O:...,D:...,I:{spurious_anchor:true}},\n#              \
  \       taxonomic:{anchor:3792, k_track_unit, kg_edges, diagnostic_absorbers}},\n#   reproduction_crosscheck: {per-concept\
  \ member-set match vs iter-2 (bool + any drift)},\n#   repair_loop: { per-concept: per-(sub_context): {n_windows_eval, recall_anchor,\
  \ recall_anchor_plus_kg,\n#        gain_kg, kg_absorber_id, kg_percentile_vs_random, random_gain_{mean,sd,p5,p50,p95},\n\
  #        paired_bootstrap_CI_kg_minus_random:{diff,lo,hi,excl_0}, diagnostic_absorber_variant:{...}},\n#        n_measured_successful_repairs,\
  \ honest_negatives:[...] },\n#   k_localization_check: { variant, projection_argmax_latent, kg_absorber_projection_rank,\n\
  #        single_latent_dominates:false, k_worstgroup_recall_on_X, conclusion },\n#   member_labeling: { per-concept:{agreement,\
  \ null_mean, gap, bootstrap_CI, n_members, confusion},\n#        pooled:{agreement, null_mean, gap, CI}, per_role_accuracy\
  \ },\n#   verdict: { kg_utility_measured:bool (>=1 repair CI excludes 0), member_labeling_above_null:bool,\n#        replaces_iter2_assertion:true,\
  \ notes } }\n# Validate full/mini/preview via aii-json; assert each <100MB (data is small JSON; corpus text snippets\n#\
  \   are few -> trivial). Save logs + cost ledger.\n"
fallback_plan: |-
  GPU/SAE issues: (1) If gemma-scope npz download or HF gating fails, mirror via unsloth/gemma-2-2b (ungated, vocab 256000) for the model and pull the SAE params.npz from the google/gemma-scope-2b-pt-res repo (layer_12/width_16k/average_l0_82); the exact loader is already proven in E1/method.py - copy it verbatim rather than re-implementing. (2) If full-window encoding is too slow/OOM, encode only the word-token position per window with keep_latents restricted to the member set + a ~1000-latent content-responsive candidate pool (never the full 16k); batch=16; this is the dominant cost and is small.

  Repair-loop design fallbacks: (3) If a concept has too few held-out corpus windows for a sub-context (n<15), pool windows across the selection+eval splits but keep absorber-selection-vs-evaluation separation by using leave-one-fold-out (select KG absorber on 4 folds, evaluate on the 5th, rotate). (4) If the binary 'fires>0' recall is saturated (anchor already detects X), that X is NOT a hole - drop it and pick lower-recall sub-contexts; if NO concept has a genuine anchor hole (anchor recall ~1 everywhere), report that as the honest finding that the unit has no recall holes to repair (auditability claim then rests on member-labeling alone) - this is a publishable negative, not a failure. (5) If the KG-named K-track absorber (e.g. Georgia=4697, subctx_prec 0.35) does NOT beat the random control but the diagnostic-corroborated absorber (16009, subctx_prec 0.955) DOES, report both transparently: the conclusion becomes 'the diagnostic-corroborated KG edge localizes the repair; the bare max-coverage edge is noisier' (informative about which KG-edge type to trust). (6) Letter I (spurious anchor 1227): if no valid parent exists, mark I N/A and exclude from aggregate; do not fabricate a repair.

  (k) baseline fallback: (7) If a full JTT/GEORGE retrain is too costly, implement the minimal JTT (ERM probe -> high-loss upweight -> retrain) only; the load-bearing claim is the STRUCTURAL one (example-reweighting yields no per-feature unit to add), which the decoder-projection argmax demonstrates even with a single (k) variant. If (k) entirely fails to build, the repair-loop vs random-addition result still stands; report (k) as 'not run' rather than block.

  LLM-judge fallbacks: (8) If anthropic/claude-haiku-4.5 errors/rate-limits, fall back to google/gemini-3.1-flash-lite then deepseek/deepseek-v3.2; temp 0; retries with backoff. (9) If forced-choice parsing is unreliable, constrain output to a single integer index and re-ask once on parse failure. (10) Cost is tiny (~100-150 members) - if any cost spike appears, STOP at $3 and report partial member-labeling.

  Overall triage: the SINGLE must-deliver is >=1 MEASURED KG-utility number replacing the iter-2 '70-edge graph' assertion. Priority order if time-pressed: (i) taxonomic repair loop on Georgia/Jordan/US (strongest, diagnostic-corroborated) -> (ii) member-labeling (cheap, fast) -> (iii) first-letter repair loop -> (iv) (k) localization check. Always emit method_out.json with whatever landed + explicit per-result status flags.
testing_plan: |-
  Confirmation-signal-driven, gradual scaling (aii-long-running-tasks):

  T0 - SMOKE (no GPU, seconds): json.load both iter-2 method_out.json files and assert the canonical structures parse: FL has keys L/O/T/I/D each with 'anchor' and member 'role' entries (L anchor==205, members include 3069 & 4736; I anchor==1227); TX has anchor==3792, k_track_unit==[3792,4697,9339,8442], kg_edges with specializes in {Georgia,Jordan}, non_triviality_passing_absorbers includes 16009->Georgia. Load D1/D2, assert corpus_context rows carry metadata_sub_context + 'input' text + target span. Fail fast if any path/shape is wrong.

  T1 - SAE/GATING SANITY (GPU, ~3-5 min): load SAE+model via the copied E1 loader; run gating_check on a handful of windows; ASSERT reconstruction cosine>0.9 (expect ~0.924) and JumpReLU firing=encode>0 reproduces a known latent. Encode 20 first-letter-L corpus windows for anchor 205 and absorber 3069; ASSERT 3069 fires (>0) on >=1 'list'/'listing' window and anchor 205 fires on general-L windows - reproduces the iter-2 unit before scaling.

  T2 - REPAIR-LOOP MICRO (1 concept, 1 sub-context): run Stage-2 on taxonomic Georgia only with R=50 random draws and B=1000. CONFIRMATION SIGNALS: (a) recall_anchor(Georgia) is materially <1 (a real hole); (b) recall_anchor+kg(Georgia) > recall_anchor (the KG absorber recovers windows); (c) gain_kg lands high in the random-gain distribution. If gain_kg is NOT above most random draws even for Georgia (the hypothesis's strongest case, expected unit recall 0.713 vs h 0.520), STOP and debug detection/threshold/fold logic before scaling - this is the canary. Cross-check the recall numbers are in the plausible regime of iter-2's taxonomic recall (~0.7).

  T3 - MEMBER-LABELING MICRO (3 members, 1 LLM call each): build evidence for anchor 205, absorber 3069('list'), absorber 4736('linking'); run the forced-choice judge; ASSERT the judge maps 3069->'list'-like and 4736->'linking'-like and 205->GENERAL more often than chance on this tiny set; verify cost ledger increments and stays <$0.05. Confirms prompt + parsing + cost tracking before the full sweep.

  T4 - FULL SCALE: run all concepts (L,O,T,D + taxonomic; I handled per spurious-anchor rule) with R=500-1000, B>=10,000, S=2000 shuffles. Monitor logs/run.log via PID-based tail. After completion, validate: every repair_loop entry has a paired-bootstrap CI; member_labeling has gap+CI; cumulative_llm_cost_usd recorded and <$3; method_out.json + variants <100MB via aii-json. Sanity: number of MEASURED successful repairs >=1 (else the run is reportable but flags kg_utility_measured=false honestly). Spot-check 2-3 repair rows by hand: gain_kg, random p95, and CI signs must be internally consistent (CI>0 iff gain_kg>random mean).

  GUARDRAILS: keep_latents must restrict encoding width (never materialize 16k x n); free GPU tensors between concepts; assert no NaN in recall/gain; assert eval windows are disjoint from selection windows (fold check) so the repair test is not circular; never overwrite the read-only iter-1/iter-2 artifacts.
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

### [14] SYSTEM-USER prompt · 2026-06-17 19:06:07 UTC

```
<validation-feedback>
Attempt 1 failed validation.

You have not created the output file `.terminal_claude_agent_struct_out.json` yet. Use the Write tool to create it.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```

### [15] SYSTEM-USER prompt · 2026-06-17 19:06:13 UTC

```
continue
```

### [16] SYSTEM-USER prompt · 2026-06-17 19:06:21 UTC

```
continue
```

### [17] SYSTEM-USER prompt · 2026-06-17 19:06:29 UTC

```
continue
```

### [18] SYSTEM-USER prompt · 2026-06-17 19:06:35 UTC

```
continue
```

### [19] SYSTEM-USER prompt · 2026-06-17 19:06:43 UTC

```
continue
```

### [20] SYSTEM-USER prompt · 2026-06-17 19:07:57 UTC

```
<validation-feedback>
Attempt 2 failed validation.

You have not created the output file `.terminal_claude_agent_struct_out.json` yet. Use the Write tool to create it.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```

### [21] SYSTEM-USER prompt · 2026-06-17 19:08:05 UTC

```
continue
```

### [22] SYSTEM-USER prompt · 2026-06-17 19:08:11 UTC

```
continue
```

### [23] SYSTEM-USER prompt · 2026-06-17 19:08:19 UTC

```
continue
```

### [24] SYSTEM-USER prompt · 2026-06-17 19:08:27 UTC

```
continue
```

### [25] SYSTEM-USER prompt · 2026-06-17 19:08:35 UTC

```
continue
```

### [26] SYSTEM-USER prompt · 2026-06-17 19:08:55 UTC

```
<validation-feedback>
Attempt 3 failed validation.

You have not created the output file `.terminal_claude_agent_struct_out.json` yet. Use the Write tool to create it.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```

### [27] SYSTEM-USER prompt · 2026-06-17 19:09:35 UTC

```
continue
```

### [28] SYSTEM-USER prompt · 2026-06-17 19:09:43 UTC

```
continue
```

### [29] SYSTEM-USER prompt · 2026-06-17 19:12:09 UTC

```
continue
```
