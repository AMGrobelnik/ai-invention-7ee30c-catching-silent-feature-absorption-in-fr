# gen_art_experiment_1 — test_idea

> Phase: `invention_loop` · round 2 · `gen_art`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_experiment_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-17 15:42:23 UTC

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
The entire worker container crashed after 58s.
Error: Pod launch failed — no instance booted (tried 2, 13 still out of stock): Failed to create pod: RunPod API error (HTTP 500 POST /pods): {"error":"create pod: There are no instances currently available","status":500}


This was NOT a normal code error — the entire container died. Study the error
and last messages above carefully. Identify what caused the crash and be
EXTREMELY careful to avoid repeating it. Do NOT use the same approach.
</CRITICAL_WARNING__PREVIOUS_ATTEMPT_CRASHED>

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/results/out.json`
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
  Execute the First-Letter Primary Falsification Endpoint (E1/E2), Count-Matched C1, Admission + Steering on Frozen Gemma
  Scope SAE
summary: >-
  EXPERIMENT (GPU). The single highest-value iter-2 artifact: run the two-track CCRG pipeline on a frozen Gemma Scope L12/16k
  SAE over the pre-built first-letter spelling testbed (art_dpYpjSn2Xvg3) and decide the PRIMARY FALSIFICATION ENDPOINT. (Tier-0/E1)
  K-track anchored greedy set-cover, given ONLY content-flip pairs, recovers the form-free-diagnostic parent + >=2 per-token
  absorbers (e.g. lion/London) above a random-membership null, with anchor-fidelity validation and a threshold sensitivity
  sweep. (E2/C3) the resulting co-response unit beats count-matched oracle pool (g), count-and-pool-matched probe (h), and
  count-matched observational clusters (b)/(c) on recovered-absorber count and sliced recall over the absorbed sub-contexts
  (paired-bootstrap CI excluding 0), plus KG specialization-edge agreement with the diagnostic. (C1) pooled-max unit vs (a)/(b)/(c)/(h)
  on starts-with-L classification. (Admission) Step-5 rule with unit-proposal-level BH/Holm multiplicity and empirical false-admit
  rate under both nulls. (Steering, run last) mean-member-decoder direction moves starts-with-L output mass at MATCHED on-target
  effect with LOWER full-vocab-KL + PPL collateral than a non-SAE diff-of-means direction and a hub/best-single-latent control.
  Letter L primary then O/T/I/D. Core LLM spend = $0 (everything is code-based; the dataset is pre-built and the diagnostic
  is the form-free probe-projection). Emit method_out.json with all metrics, paired-bootstrap CIs, recovered unit definitions
  (members, logit-lens tokens, conditioning contexts), and the specialization-edge KG.
runpod_compute_profile: gpu
implementation_pseudocode: |-
  # ============================================================================
  # experiment_iter2_dir1 : Two-Track CCRG on first-letter spelling (PRIMARY ENDPOINT)
  # GPU (RTX A4500 20GB ok). bf16. ~6h wall-clock budget. Core LLM spend = $0.
  # Read pinned facts from the 3 deps before coding:
  #   DATA  : /ai-inventor/.../iter_1/gen_art/gen_art_dataset_1/{full_data_out.json,data.py}
  #   METHOD: /ai-inventor/.../iter_1/gen_art/gen_art_research_1/research_out.json
  #   DIAG  : /ai-inventor/.../iter_1/gen_art/gen_art_research_2/research_out.json
  # Use skills: aii-use-hardware (detect GPU), aii-parallel-computing (batching),
  #   aii-long-running-tasks (mini->full scaling), aii-json (validate output),
  #   aii-file-size-limit (split method_out.json if >limit), aii-python (structure/logging).
  # ============================================================================

  # ---------- CONFIG (all defaults pinned; do NOT guess) ----------
  RELEASE='gemma-scope-2b-pt-res-canonical'; SAE_ID='layer_12/width_16k/canonical'  # d_model=2304, n_latents=16384
  HOOK_LAYER=12  # blocks.12.hook_resid_post == HF hidden_states[13] == output of decoder layer 12
  MODEL_ID='unsloth/gemma-2-2b'  # non-gated mirror, vocab 256000 (google/gemma-2-2b is GATED)
  LETTERS=['L','O','T','I','D']; PRIMARY='L'
  BETA=6; GAMMA_GRID=[0.3,0.5,0.7,1.0,1.5]; PREC_FLOOR=0.7; JACCARD_MAX=0.1; COVGAIN_FLOOR=0.05
  B_GAP=10000; B_NULL=1000; N_MIN=150; STEER_C=[0,0.5,1,2,4,8]
  SPELLING_CARRIERS=['t_verbose','t_colon','t_icl']  # primary substrate (matches Chanin VERBOSE template)
  ALL_CARRIERS=SPELLING_CARRIERS+['t_mention_word','t_mention_term','t_mention_example','t_mention_spelled']

  # ---------- STEP 0: load model + SAE + GATING SANITY CHECK ----------
  from sae_lens import SAE
  ret = SAE.from_pretrained(release=RELEASE, sae_id=SAE_ID, device='cuda')
  sae = ret[0] if isinstance(ret, tuple) else ret           # DEFENSIVE: v6 returns SAE, <=v5 returns 3-tuple
  assert sae.W_dec.shape == (16384, 2304)                    # [n_latents, d_model]
  from transformers import AutoModelForCausalLM, AutoTokenizer
  tok = AutoTokenizer.from_pretrained(MODEL_ID)
  model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=bf16, device_map='cuda').eval()
  # get_resid(prompts): tokenize, forward(output_hidden_states=True), take hidden_states[HOOK_LAYER+1]
  #   (== residual stream AFTER block 12, pre-final-norm, exactly what Gemma Scope was trained on).
  #   Equivalent: forward hook on model.model.layers[12] capturing output[0].
  # firing(acts) := sae.encode(acts) > 0   (JumpReLU threshold applied inside encode)
  # *** GATING CHECK (MUST PASS before anything else) ***
  #   h = get_resid(sample of ~64 corpus windows)[token positions];  z = sae.encode(h);  h_hat = sae.decode(z)
  #   assert mean cosine(h, h_hat) > 0.9 AND explained_variance > 0.5   # else WRONG layer/position/scaling -> debug
  #   (Gemma Scope SAEs reconstruct their own input well; a low value means activations are wrong.)
  # NOTE: the literature worked indices (S:6510/1085, L:7112/7657) are LAYER-3 width-16k; at LAYER 12
  #   parent/absorbers MUST be discovered fresh by the diagnostic, never hard-coded.

  # ---------- DATA LOADING ----------
  load full_data_out.json -> rows grouped into 5 letter datasets. Each row: input, output, metadata_*.
  # content_flip pair: rows sharing metadata_pair_id with metadata_role in {on,off}; on-word starts with
  #   target letter, off-word surface-matched (len/single-token/log-freq) NOT starting with it.
  # surface_flip pair: metadata_role in {var_a,var_b}; both words start with target letter (component B).
  # corpus rows: metadata_pair_type=='corpus_context'; real Pile windows centered on a slot-eligible
  #   target-letter token at metadata_token_position (component C). 2500/letter.
  WORD-TOKEN LOCALIZATION: tokenize input with return_offsets_mapping; map metadata_word_char_span ->
  #   token index of the slotted word (words are single-token by construction). Read SAE activation THERE.
  #   (sae-spelling reads the word token; for t_verbose this is pos -6. Use offset mapping, not a magic index.)

  # ============================================================================
  # STEP 1: content-response matrix + cover sets   (per letter; substrate = SPELLING_CARRIERS)
  # ============================================================================
  for each on-word w and its carrier instances:
      encode x_on, x_off at word token -> a_on[16384], a_off[16384]; r = a_on - a_off
  # Aggregate to WORD granularity: r_l(w) = mean over w carrier pairs of r_l. Build R[16384 x n_words].
  # CONTENT-RESPONSIVE PREFILTER: shuffled-pair null = permute on/off labels within letter, recompute mean
  #   response B_NULL times; keep latent l iff mean_w r_l(w) > 95th pct of its shuffle null. -> responsive set Lr.
  # tau_resp(l) = max(eps, 95th pct of l shuffle null). Word w is COVERED by l iff r_l(w)>tau_resp AND
  #   sae.encode fires on x_on(w). COVER SET C_l = { w : covered }.
  # PER-LATENT PRECISION precision_l = (#on-words it covers) / (#words where it fires on EITHER on or off).
  #   Require precision_l>=PREC_FLOOR for l to be cover-set-eligible (a starts-with-L latent should fire on
  #   L-words, not off-words). FIRING SETS for Jaccard: binary firing over all on-words (and over corpus for robustness).

  # ============================================================================
  # STEP 2: C-TRACK (splitting; shared-support; correlation IS appropriate)
  # ============================================================================
  rho = Spearman correlation of content-response profiles among Lr (over words)
  A = max(rho, 0) ** BETA                       # DiffCoEx/WGCNA signed soft-threshold, beta=6
  import leidenalg, igraph
  for gamma in GAMMA_GRID:
      part = leidenalg.find_partition(graph_from(A), leidenalg.RBConfigurationVertexPartition,
                                      weights=edge_weights, resolution_parameter=gamma)
      # bootstrap-ARI stability: resample words, recluster, adjusted_rand_score vs shuffle null
  choose gamma maximizing mean bootstrap-ARI above shuffle null; C-communities = part at chosen gamma.

  # ============================================================================
  # STEP 3: K-TRACK (absorption; DISJOINT-support; anchored greedy MAX-COVERAGE)  <-- E1 CORE
  # ============================================================================
  ANCHOR = argmax over l in Lr of |C_l|   using ONLY pairs (NOT the diagnostic). Tie-break: broadest, lowest-entropy support.
  Holes H = AllWords MINUS C_ANCHOR     # absorbed sub-contexts (e.g. lion, London)
  unit_members = [ANCHOR]
  while H nonempty and improving:
      cand = argmax over l not in unit of |C_l intersect H|
      gain = |C_cand intersect H| / |AllWords|
      if firing_Jaccard(cand, ANCHOR) < JACCARD_MAX and precision_cand >= PREC_FLOOR and gain >= COVGAIN_FLOOR and bootstrap_CI(gain, B_GAP) excludes 0:
          unit_members.append(cand); H = H MINUS C_cand
      else: break
  K_UNIT = unit_members   # {general starts-with-L latent} + {per-word absorbers}

  # ============================================================================
  # STEP 4: RECONCILE + STEP 5 ADMISSION (with multiplicity)
  # ============================================================================
  # Reconcile: anchor each C-community highest-recall member, K-augment with mutually-exclusive absorbers
  #   covering its holes; seed K from standalone high-recall latents; de-dup latent->highest-coverage-gain unit.
  # For EACH candidate unit, ADMISSION:
  #   sigC: within-unit mean content-response correlation > 95th pct shuffled-pair null
  #   sigK: pooled-max AUC - best-single-member AUC > AUC-matched random-k null  AND  k in {2,3} abs gain>=0.05
  #         with bootstrap CI excl 0  AND  Jaccard<JACCARD_MAX  AND  per-member precision>=PREC_FLOOR
  #   AND-GATE surface invariance: pooled-max response on surface_flip pairs (component B) NOT above
  #         shuffled-surface null. Report null SIZE per letter (L:170 surface pairs etc.).
  #   admit iff (sigC OR sigK) AND surface_invariant.
  # MULTIPLICITY: collect M candidate-unit admission p-values per letter; apply Benjamini-Hochberg (and Holm)
  #   via statsmodels.stats.multitest.multipletests. Report M and EMPIRICAL family-wise false-admit rate from
  #   the matched random-k null on the real run. (Separate from across-claims Holm used for headline comparisons.)

  # ============================================================================
  # FORM-FREE ABSORPTION DIAGNOSTIC (ORACLE for E1/E2; SCORES edges, never forms units -> non-circular)
  # ============================================================================
  # Train parent-concept probe d_p on DISJOINT data: corpus windows (component C). Positives = L-windows
  #   (residual at metadata_token_position), Negatives = O/T/I/D windows. LogisticRegression -> d_p (2304-vec).
  #   Require probe test-acc > 0.8 (else parent direction unreliable -> debug position).
  # parent latent = argmax_l cosine(sae.W_enc[:,l]  (ENCODER dir), d_p)   # Chanin: parent uses ENCODER cosine
  # For each first-letter FALSE-NEGATIVE word (probe right but parent latent silent), find absorber via the
  #   form-free A.13 / SAEBench absorption_fraction test:  a_hat_l = enc_act_l * W_dec[l];
  #   latent l absorbs iff  tau_c < (a_hat_l . d_p)/(a . d_p)   (a = full residual). DECODER cosine for alignment.
  #   tau_c default 0.5 (sweep robustness). -> DIAG_PARENT, DIAG_ABSORBERS (with the word each covers).

  # ============================================================================
  # E1 (Tier-0 pilot, NEVER dropped) : does K-track PROPOSE the right unit?
  # ============================================================================
  membership precision/recall/F1 of K_UNIT vs (DIAG_PARENT + DIAG_ABSORBERS).
  RANDOM-MEMBERSHIP NULL: sample |K_UNIT| random latents from Lr, B_NULL times, F1 distribution.
  E1_PASS := (F1 > 95th pct of null) AND (anchor recovered) AND (>=2 absorbers recovered).
  ANCHOR-FIDELITY: is ANCHOR == DIAG_PARENT? Confirm no high-frequency/polysemantic latent usurped anchor
     (anchor corpus firing rate must be selective to L-words, not near-uniform; report firing rate + logit-lens).
  THRESHOLD SWEEP (show recovery is not knife-edge): Jaccard in {0.05,0.1,0.15,0.2} x precision in {0.6,0.7,0.8}
     x coverage-gain in {0.03,0.05,0.07}; report recovery F1 over the grid (heatmap-ready table).

  # ============================================================================
  # BASELINES (count-matched to k = |K_UNIT|)
  # ============================================================================
  (a) best raw single latent : argmax held-out AUC of single-latent starts-with-L detection.
  (b) co-activation clusters : sklearn HDBSCAN on co-firing of Lr over corpus; pick concept-aligned cluster;
        cut to k members (top-k by individual AUC; augment with nearest co-firing if <k).
  (c) decoder-geometry clusters: agglomerative cosine clustering of W_dec[Lr]; concept-aligned cluster cut to k.
  (g) oracle pool SCR/TPP : score each latent by attribution to d_p  =  |d_p . W_dec[l]| * mean_activation_l
        (probe-weight x mean-activation proxy; SAEBench stable_paper_version is the reference). Top-N, N in {10,20}.
        Absorbers (low mean activation) get low attribution -> dropped. THIS IS THE GAP.
  (h) count-and-pool-matched : max-pool over EXACTLY k raw residual directions W_dec[i] of the top-k SCR/TPP
        latents (pool SIZE fixed = k; only the SELECTION criterion differs from the unit).

  # ============================================================================
  # E2 / C3 (NEVER dropped) : does the co-response UNIT win on absorber recovery + sliced recall?
  # ============================================================================
  Recovered-absorber COUNT: |K_UNIT cap DIAG_ABSORBERS| vs |(g) cap DIAG_ABSORBERS| vs |(h)latents cap DIAG_ABSORBERS|.
  SLICED RECALL on the differing sub-contexts (the absorbed words where parent/(g)/(h)/(b)/(c) have holes):
     detect starts-with-L via pooled-max activation thresholded; recall on absorbed-word slice; unit vs each baseline.
  PAIRED BOOTSTRAP (B_GAP) over examples in the slice: CI on (unit - baseline) gap must EXCLUDE 0;
     exact McNemar (statsmodels) for the unit-vs-(g)/(h) win; Holm-Bonferroni across the headline comparisons.
  KG SPECIALIZATION EDGES: for each absorber member, directed edge ANCHOR->absorber labeled 'absorbed_child(word)'.
     AGREEMENT with diagnostic = precision/recall of unit edges vs DIAG (parent,absorber) pairs.
  E2_PASS := unit beats count-matched (g)/(h)/(b)/(c) on recovered-absorber count AND sliced recall, CI excl 0.
  HARD CHECKPOINT: if E1_PASS and E2_PASS on L -> proceed to O/T/I/D + steering; else write up the executed NEGATIVE
     (with threshold sweep + diagnostic proving it is structural, not a knob artifact).

  # ============================================================================
  # C1 classification (NEVER dropped)
  # ============================================================================
  Form unit + fit pooled-max threshold on TRAIN folds (metadata_fold 0-3); evaluate on TEST fold 4 (no target_word
     leakage). Pooled-max unit activation classifies starts-with-L. Compare unit vs (a),(b),(c),(h).
  Metrics: F1 + AUC + worst-word recall; per-letter paired-bootstrap CIs (B_GAP). LOAD-BEARING half = unit beats
     count-matched (b)/(c)/(h) (beating single best latent (a) is a near-foregone capacity win, completeness only).
  Run L first; then O/T/I/D.

  # ============================================================================
  # STEERING (run LAST so the endpoint always lands; required, null-floored)
  # ============================================================================
  d_unit = normalize(mean over members of W_dec[member])         # mean-member-decoder direction
  d_dom  = W_dec[best_single_member]                              # hub / best-single-latent-alone control
  d_dm   = non-SAE diff-of-means direction (mean resid of L-windows - mean resid of non-L-windows; INDEPENDENT data)
  Rnorm = mean residual L2 norm at layer 12 (for alpha scaling)
  for c in STEER_C: add (c*Rnorm)*dir at blocks.12.hook_resid_post via forward hook during generation on HELD-OUT prompts.
  ON-TARGET = increase in summed next-token prob over L-initial vocab tokens (word-initial 'L'/'l' + 'L'/'l').
  COLLATERAL = full-vocab next-token KL(steered||unsteered) on UNRELATED prompts + PPL on held-out text.
  MATCH on-target across methods (interpolate alpha to equal on-target Delta), then COMPARE collateral.
  Report: d_unit vs d_dm vs d_dom at MATCHED on-target -> lower KL + PPL is the win. Doc-bootstrap CIs + shuffle
     null (random direction). STEERING_PASS := d_unit lower collateral than BOTH d_dm and d_dom at matched on-target.

  # ============================================================================
  # OUTPUT method_out.json (validate with aii-json; split if > size limit via aii-file-size-limit)
  # ============================================================================
  { verdicts:{E1_PASS,E2_PASS,STEERING_PASS, primary_endpoint:'WORKS' or 'DOES_NOT_WORK'},
    per_letter:{L,O,T,I,D}: { anchor_fidelity, E1{precision,recall,F1,null_pctile,threshold_sweep_grid},
        E2{recovered_absorber_counts{unit,g,h,b,c}, sliced_recall{unit,a,b,c,g,h}, paired_bootstrap_CIs, mcnemar_p,
           kg_edge_agreement{prec,recall}}, C1{F1,AUC,worst_word_recall, CIs, holm_p},
        admission{M, signatures_cleared, empirical_false_admit_rate_allnull, false_admit_randomknull},
        cluster_stability_ARI },
    steering:{ on_target_curve, collateral_KL, PPL, matched_comparison, CIs, shuffle_null },
    unit_definitions:[ {letter, members:[idx], member_logit_lens_tokens:[top-k from W_dec[l] times embed.T],
        member_conditioning_contexts:[top-activating corpus windows], anchor_idx, absorber_idxs} ],
    kg_edges:[ {src:anchor, dst:absorber, type:'absorbed_child', sub_context:word, diag_agrees:bool} ],
    config:{release,sae_id,hook,thresholds,seeds}, runtime_stats }
  # Keep big arrays (R matrix, per-latent activations) OUT of method_out.json; save as .npy for provenance.

  # ---------- PRIORITIZATION (partial completion must still yield the primary endpoint) ----------
  # (1) STEP0-1 encode + two-track on L  ->  (2) E1 pilot on L  ->  (3) E2 + C1 on L  ->  (4) steering on L
  #  ->  (5) repeat E1/E2/C1 for O/T/I/D  ->  (6) admission multiplicity across letters.
  # SCALING: mini (L, ~10 on-words) confirm signal; then full L; then O/T/I/D. Process letters sequentially;
  #   discard residual caches after pooling; bf16; chunk corpus encoding.
fallback_plan: >-
  MODEL/SAE LOADING: primary = raw HF transformers on unsloth/gemma-2-2b (non-gated) + hidden_states[13] (== blocks.12.hook_resid_post).
  The SAE reconstruction GATING CHECK (cosine>0.9, EV>0.5) is the ground-truth correctness test: if it fails, the activations
  are wrong -> try (a) forward-hook on model.model.layers[12] output[0], (b) confirm you took hidden_states[13] not [12],
  (c) check for an activation-scaling normalization the SAE expects, (d) try google/gemma-2-2b with HF_TOKEN via transformer_lens
  HookedTransformer/HookedSAETransformer (which name the hook directly). Do NOT proceed past a failing reconstruction check.
  WORD POSITION: word-token (offset-mapping) is primary; if the anchor is weak or no parent emerges, try last-token (the colon
  answer position) and mean-pool, and report which position the diagnostic/probe works at. NO PARENT AT L12 (unexpected, since
  L12 is in the valid 0-17 range and is the densest layer): switch SAE to layer_12/width_65k/canonical (more features) and
  report; if still absent, that is itself a finding. SCR/TPP (g)/(h): if SAEBench integration is too heavy, the pinned attribution
  proxy (|d_p . W_dec[l]| * mean_activation_l) is acceptable (g/h are explicitly reference oracles, not ground truth). PROBE
  d_p: if corpus-trained probe acc<0.8, train on held-out content-flip on-words (still disjoint from the clustering pairs
  used to form units) or pool more corpus windows. E1 FAILURE (K-track cannot recover parent+>=2 absorbers above null): this
  IS the declared primary NEGATIVE (method does not work) -- report it honestly with the full threshold sweep + the diagnostic
  parent/absorbers to prove it is structural, not a knob artifact; the paper writes up the executed negative. E2 TIE (unit
  ties g/h on sliced recall): report as the secondary characterization 'robustness is pooling -> contribution reduces to absorber-recovery
  count + KG'. STEERING no advantage: report the on-target/collateral curves anyway (a clean null is publishable; steering
  is a generality demo, not load-bearing for E1/E2). GPU OOM: reduce batch to 8-16, fp16, encode corpus in chunks discarding
  residuals after pooling, store latent activations sparsely (JumpReLU is mostly zero), process one letter at a time. TIME
  SHORTFALL: strict order above -- L all the way through steering before touching O/T/I/D, so a partial run still delivers
  the L primary endpoint + steering. Robustness baselines (j)/(k), toxicity, and the auditability repair loop are OUT OF SCOPE
  for this artifact (other artifacts) -- do not start them. Core pipeline uses NO OpenRouter/LLM calls ($0); only an OPTIONAL
  stretch LLM-judge member-labeling would, and it must respect the $10 hard cap (skip if time/budget tight).
testing_plan: >-
  Follow aii-long-running-tasks gradual scaling; gate each stage on a confirmation signal before scaling. STAGE 0 (smoke,
  ~2 min): detect GPU (aii-use-hardware); load SAE (assert W_dec [16384,2304]) with the defensive tuple-or-object loader;
  load unsloth/gemma-2-2b; encode ~64 corpus windows and RUN THE RECONSTRUCTION GATING CHECK (mean cosine>0.9 AND explained_variance>0.5).
  If this fails, STOP and fix activation extraction (layer index/position/scaling) before anything else -- every downstream
  number depends on it. STAGE 1 (mini pilot on L, ~10 on-words, t_verbose only, ~5 min): compute content-response R; find
  ANCHOR (highest-|C_l| latent); CONFIRM (i) anchor logit-lens (W_dec[anchor] times embed.T top tokens) promotes L-initial/'L'/'l'
  tokens, (ii) anchor firing is SELECTIVE on L-words (not near-uniform over corpus), (iii) corpus-trained d_p probe test-acc>0.8,
  (iv) the form-free diagnostic returns a parent and >=1 absorber, (v) K-track runs end-to-end and proposes a multi-member
  unit, (vi) membership F1 vs the diagnostic exceeds the random-membership null. These six are the GO signal that the pipeline
  is wired correctly. STAGE 2 (full L, all carriers, ~20-40 min): run STEP1-5 + E1 (with anchor-fidelity + threshold sweep)
  + diagnostic + baselines (a/b/c/g/h) + E2 (counts, sliced recall, paired-bootstrap CIs, McNemar, KG agreement) + C1 (folded)
  + admission (M, BH/Holm, empirical false-admit) + steering. CHECKPOINT: record E1_PASS / E2_PASS / STEERING_PASS for L.
  STAGE 3 (O/T/I/D): repeat STEP1-5 + E1/E2/C1 per letter; aggregate admission multiplicity across letters. STAGE 4: assemble
  method_out.json, validate against any provided schema with aii-json, and check size with aii-file-size-limit (keep big arrays
  in .npy, not the JSON). Throughout, log per-stage timings and assert intermediate shapes (R[16384 x n_words], firing booleans,
  cover-set sizes) to catch wiring bugs early. Sanity cross-checks: anchor should have the LARGEST cover set; absorbers should
  have firing-Jaccard<0.1 with the anchor and fire on words the anchor misses; surface-flip pooled response should be near
  zero (much smaller than content-flip response).
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

### [2] HUMAN-USER prompt · 2026-06-17 15:42:23 UTC

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

### [3] SKILL-INPUT — aii-json · 2026-06-17 16:55:59 UTC

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

### [4] SYSTEM-USER prompt · 2026-06-17 17:28:36 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/results/out.json`
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
  Execute the First-Letter Primary Falsification Endpoint (E1/E2), Count-Matched C1, Admission + Steering on Frozen Gemma
  Scope SAE
summary: >-
  EXPERIMENT (GPU). The single highest-value iter-2 artifact: run the two-track CCRG pipeline on a frozen Gemma Scope L12/16k
  SAE over the pre-built first-letter spelling testbed (art_dpYpjSn2Xvg3) and decide the PRIMARY FALSIFICATION ENDPOINT. (Tier-0/E1)
  K-track anchored greedy set-cover, given ONLY content-flip pairs, recovers the form-free-diagnostic parent + >=2 per-token
  absorbers (e.g. lion/London) above a random-membership null, with anchor-fidelity validation and a threshold sensitivity
  sweep. (E2/C3) the resulting co-response unit beats count-matched oracle pool (g), count-and-pool-matched probe (h), and
  count-matched observational clusters (b)/(c) on recovered-absorber count and sliced recall over the absorbed sub-contexts
  (paired-bootstrap CI excluding 0), plus KG specialization-edge agreement with the diagnostic. (C1) pooled-max unit vs (a)/(b)/(c)/(h)
  on starts-with-L classification. (Admission) Step-5 rule with unit-proposal-level BH/Holm multiplicity and empirical false-admit
  rate under both nulls. (Steering, run last) mean-member-decoder direction moves starts-with-L output mass at MATCHED on-target
  effect with LOWER full-vocab-KL + PPL collateral than a non-SAE diff-of-means direction and a hub/best-single-latent control.
  Letter L primary then O/T/I/D. Core LLM spend = $0 (everything is code-based; the dataset is pre-built and the diagnostic
  is the form-free probe-projection). Emit method_out.json with all metrics, paired-bootstrap CIs, recovered unit definitions
  (members, logit-lens tokens, conditioning contexts), and the specialization-edge KG.
runpod_compute_profile: gpu
implementation_pseudocode: |-
  # ============================================================================
  # experiment_iter2_dir1 : Two-Track CCRG on first-letter spelling (PRIMARY ENDPOINT)
  # GPU (RTX A4500 20GB ok). bf16. ~6h wall-clock budget. Core LLM spend = $0.
  # Read pinned facts from the 3 deps before coding:
  #   DATA  : /ai-inventor/.../iter_1/gen_art/gen_art_dataset_1/{full_data_out.json,data.py}
  #   METHOD: /ai-inventor/.../iter_1/gen_art/gen_art_research_1/research_out.json
  #   DIAG  : /ai-inventor/.../iter_1/gen_art/gen_art_research_2/research_out.json
  # Use skills: aii-use-hardware (detect GPU), aii-parallel-computing (batching),
  #   aii-long-running-tasks (mini->full scaling), aii-json (validate output),
  #   aii-file-size-limit (split method_out.json if >limit), aii-python (structure/logging).
  # ============================================================================

  # ---------- CONFIG (all defaults pinned; do NOT guess) ----------
  RELEASE='gemma-scope-2b-pt-res-canonical'; SAE_ID='layer_12/width_16k/canonical'  # d_model=2304, n_latents=16384
  HOOK_LAYER=12  # blocks.12.hook_resid_post == HF hidden_states[13] == output of decoder layer 12
  MODEL_ID='unsloth/gemma-2-2b'  # non-gated mirror, vocab 256000 (google/gemma-2-2b is GATED)
  LETTERS=['L','O','T','I','D']; PRIMARY='L'
  BETA=6; GAMMA_GRID=[0.3,0.5,0.7,1.0,1.5]; PREC_FLOOR=0.7; JACCARD_MAX=0.1; COVGAIN_FLOOR=0.05
  B_GAP=10000; B_NULL=1000; N_MIN=150; STEER_C=[0,0.5,1,2,4,8]
  SPELLING_CARRIERS=['t_verbose','t_colon','t_icl']  # primary substrate (matches Chanin VERBOSE template)
  ALL_CARRIERS=SPELLING_CARRIERS+['t_mention_word','t_mention_term','t_mention_example','t_mention_spelled']

  # ---------- STEP 0: load model + SAE + GATING SANITY CHECK ----------
  from sae_lens import SAE
  ret = SAE.from_pretrained(release=RELEASE, sae_id=SAE_ID, device='cuda')
  sae = ret[0] if isinstance(ret, tuple) else ret           # DEFENSIVE: v6 returns SAE, <=v5 returns 3-tuple
  assert sae.W_dec.shape == (16384, 2304)                    # [n_latents, d_model]
  from transformers import AutoModelForCausalLM, AutoTokenizer
  tok = AutoTokenizer.from_pretrained(MODEL_ID)
  model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=bf16, device_map='cuda').eval()
  # get_resid(prompts): tokenize, forward(output_hidden_states=True), take hidden_states[HOOK_LAYER+1]
  #   (== residual stream AFTER block 12, pre-final-norm, exactly what Gemma Scope was trained on).
  #   Equivalent: forward hook on model.model.layers[12] capturing output[0].
  # firing(acts) := sae.encode(acts) > 0   (JumpReLU threshold applied inside encode)
  # *** GATING CHECK (MUST PASS before anything else) ***
  #   h = get_resid(sample of ~64 corpus windows)[token positions];  z = sae.encode(h);  h_hat = sae.decode(z)
  #   assert mean cosine(h, h_hat) > 0.9 AND explained_variance > 0.5   # else WRONG layer/position/scaling -> debug
  #   (Gemma Scope SAEs reconstruct their own input well; a low value means activations are wrong.)
  # NOTE: the literature worked indices (S:6510/1085, L:7112/7657) are LAYER-3 width-16k; at LAYER 12
  #   parent/absorbers MUST be discovered fresh by the diagnostic, never hard-coded.

  # ---------- DATA LOADING ----------
  load full_data_out.json -> rows grouped into 5 letter datasets. Each row: input, output, metadata_*.
  # content_flip pair: rows sharing metadata_pair_id with metadata_role in {on,off}; on-word starts with
  #   target letter, off-word surface-matched (len/single-token/log-freq) NOT starting with it.
  # surface_flip pair: metadata_role in {var_a,var_b}; both words start with target letter (component B).
  # corpus rows: metadata_pair_type=='corpus_context'; real Pile windows centered on a slot-eligible
  #   target-letter token at metadata_token_position (component C). 2500/letter.
  WORD-TOKEN LOCALIZATION: tokenize input with return_offsets_mapping; map metadata_word_char_span ->
  #   token index of the slotted word (words are single-token by construction). Read SAE activation THERE.
  #   (sae-spelling reads the word token; for t_verbose this is pos -6. Use offset mapping, not a magic index.)

  # ============================================================================
  # STEP 1: content-response matrix + cover sets   (per letter; substrate = SPELLING_CARRIERS)
  # ============================================================================
  for each on-word w and its carrier instances:
      encode x_on, x_off at word token -> a_on[16384], a_off[16384]; r = a_on - a_off
  # Aggregate to WORD granularity: r_l(w) = mean over w carrier pairs of r_l. Build R[16384 x n_words].
  # CONTENT-RESPONSIVE PREFILTER: shuffled-pair null = permute on/off labels within letter, recompute mean
  #   response B_NULL times; keep latent l iff mean_w r_l(w) > 95th pct of its shuffle null. -> responsive set Lr.
  # tau_resp(l) = max(eps, 95th pct of l shuffle null). Word w is COVERED by l iff r_l(w)>tau_resp AND
  #   sae.encode fires on x_on(w). COVER SET C_l = { w : covered }.
  # PER-LATENT PRECISION precision_l = (#on-words it covers) / (#words where it fires on EITHER on or off).
  #   Require precision_l>=PREC_FLOOR for l to be cover-set-eligible (a starts-with-L latent should fire on
  #   L-words, not off-words). FIRING SETS for Jaccard: binary firing over all on-words (and over corpus for robustness).

  # ============================================================================
  # STEP 2: C-TRACK (splitting; shared-support; correlation IS appropriate)
  # ============================================================================
  rho = Spearman correlation of content-response profiles among Lr (over words)
  A = max(rho, 0) ** BETA                       # DiffCoEx/WGCNA signed soft-threshold, beta=6
  import leidenalg, igraph
  for gamma in GAMMA_GRID:
      part = leidenalg.find_partition(graph_from(A), leidenalg.RBConfigurationVertexPartition,
                                      weights=edge_weights, resolution_parameter=gamma)
      # bootstrap-ARI stability: resample words, recluster, adjusted_rand_score vs shuffle null
  choose gamma maximizing mean bootstrap-ARI above shuffle null; C-communities = part at chosen gamma.

  # ============================================================================
  # STEP 3: K-TRACK (absorption; DISJOINT-support; anchored greedy MAX-COVERAGE)  <-- E1 CORE
  # ============================================================================
  ANCHOR = argmax over l in Lr of |C_l|   using ONLY pairs (NOT the diagnostic). Tie-break: broadest, lowest-entropy support.
  Holes H = AllWords MINUS C_ANCHOR     # absorbed sub-contexts (e.g. lion, London)
  unit_members = [ANCHOR]
  while H nonempty and improving:
      cand = argmax over l not in unit of |C_l intersect H|
      gain = |C_cand intersect H| / |AllWords|
      if firing_Jaccard(cand, ANCHOR) < JACCARD_MAX and precision_cand >= PREC_FLOOR and gain >= COVGAIN_FLOOR and bootstrap_CI(gain, B_GAP) excludes 0:
          unit_members.append(cand); H = H MINUS C_cand
      else: break
  K_UNIT = unit_members   # {general starts-with-L latent} + {per-word absorbers}

  # ============================================================================
  # STEP 4: RECONCILE + STEP 5 ADMISSION (with multiplicity)
  # ============================================================================
  # Reconcile: anchor each C-community highest-recall member, K-augment with mutually-exclusive absorbers
  #   covering its holes; seed K from standalone high-recall latents; de-dup latent->highest-coverage-gain unit.
  # For EACH candidate unit, ADMISSION:
  #   sigC: within-unit mean content-response correlation > 95th pct shuffled-pair null
  #   sigK: pooled-max AUC - best-single-member AUC > AUC-matched random-k null  AND  k in {2,3} abs gain>=0.05
  #         with bootstrap CI excl 0  AND  Jaccard<JACCARD_MAX  AND  per-member precision>=PREC_FLOOR
  #   AND-GATE surface invariance: pooled-max response on surface_flip pairs (component B) NOT above
  #         shuffled-surface null. Report null SIZE per letter (L:170 surface pairs etc.).
  #   admit iff (sigC OR sigK) AND surface_invariant.
  # MULTIPLICITY: collect M candidate-unit admission p-values per letter; apply Benjamini-Hochberg (and Holm)
  #   via statsmodels.stats.multitest.multipletests. Report M and EMPIRICAL family-wise false-admit rate from
  #   the matched random-k null on the real run. (Separate from across-claims Holm used for headline comparisons.)

  # ============================================================================
  # FORM-FREE ABSORPTION DIAGNOSTIC (ORACLE for E1/E2; SCORES edges, never forms units -> non-circular)
  # ============================================================================
  # Train parent-concept probe d_p on DISJOINT data: corpus windows (component C). Positives = L-windows
  #   (residual at metadata_token_position), Negatives = O/T/I/D windows. LogisticRegression -> d_p (2304-vec).
  #   Require probe test-acc > 0.8 (else parent direction unreliable -> debug position).
  # parent latent = argmax_l cosine(sae.W_enc[:,l]  (ENCODER dir), d_p)   # Chanin: parent uses ENCODER cosine
  # For each first-letter FALSE-NEGATIVE word (probe right but parent latent silent), find absorber via the
  #   form-free A.13 / SAEBench absorption_fraction test:  a_hat_l = enc_act_l * W_dec[l];
  #   latent l absorbs iff  tau_c < (a_hat_l . d_p)/(a . d_p)   (a = full residual). DECODER cosine for alignment.
  #   tau_c default 0.5 (sweep robustness). -> DIAG_PARENT, DIAG_ABSORBERS (with the word each covers).

  # ============================================================================
  # E1 (Tier-0 pilot, NEVER dropped) : does K-track PROPOSE the right unit?
  # ============================================================================
  membership precision/recall/F1 of K_UNIT vs (DIAG_PARENT + DIAG_ABSORBERS).
  RANDOM-MEMBERSHIP NULL: sample |K_UNIT| random latents from Lr, B_NULL times, F1 distribution.
  E1_PASS := (F1 > 95th pct of null) AND (anchor recovered) AND (>=2 absorbers recovered).
  ANCHOR-FIDELITY: is ANCHOR == DIAG_PARENT? Confirm no high-frequency/polysemantic latent usurped anchor
     (anchor corpus firing rate must be selective to L-words, not near-uniform; report firing rate + logit-lens).
  THRESHOLD SWEEP (show recovery is not knife-edge): Jaccard in {0.05,0.1,0.15,0.2} x precision in {0.6,0.7,0.8}
     x coverage-gain in {0.03,0.05,0.07}; report recovery F1 over the grid (heatmap-ready table).

  # ============================================================================
  # BASELINES (count-matched to k = |K_UNIT|)
  # ============================================================================
  (a) best raw single latent : argmax held-out AUC of single-latent starts-with-L detection.
  (b) co-activation clusters : sklearn HDBSCAN on co-firing of Lr over corpus; pick concept-aligned cluster;
        cut to k members (top-k by individual AUC; augment with nearest co-firing if <k).
  (c) decoder-geometry clusters: agglomerative cosine clustering of W_dec[Lr]; concept-aligned cluster cut to k.
  (g) oracle pool SCR/TPP : score each latent by attribution to d_p  =  |d_p . W_dec[l]| * mean_activation_l
        (probe-weight x mean-activation proxy; SAEBench stable_paper_version is the reference). Top-N, N in {10,20}.
        Absorbers (low mean activation) get low attribution -> dropped. THIS IS THE GAP.
  (h) count-and-pool-matched : max-pool over EXACTLY k raw residual directions W_dec[i] of the top-k SCR/TPP
        latents (pool SIZE fixed = k; only the SELECTION criterion differs from the unit).

  # ============================================================================
  # E2 / C3 (NEVER dropped) : does the co-response UNIT win on absorber recovery + sliced recall?
  # ============================================================================
  Recovered-absorber COUNT: |K_UNIT cap DIAG_ABSORBERS| vs |(g) cap DIAG_ABSORBERS| vs |(h)latents cap DIAG_ABSORBERS|.
  SLICED RECALL on the differing sub-contexts (the absorbed words where parent/(g)/(h)/(b)/(c) have holes):
     detect starts-with-L via pooled-max activation thresholded; recall on absorbed-word slice; unit vs each baseline.
  PAIRED BOOTSTRAP (B_GAP) over examples in the slice: CI on (unit - baseline) gap must EXCLUDE 0;
     exact McNemar (statsmodels) for the unit-vs-(g)/(h) win; Holm-Bonferroni across the headline comparisons.
  KG SPECIALIZATION EDGES: for each absorber member, directed edge ANCHOR->absorber labeled 'absorbed_child(word)'.
     AGREEMENT with diagnostic = precision/recall of unit edges vs DIAG (parent,absorber) pairs.
  E2_PASS := unit beats count-matched (g)/(h)/(b)/(c) on recovered-absorber count AND sliced recall, CI excl 0.
  HARD CHECKPOINT: if E1_PASS and E2_PASS on L -> proceed to O/T/I/D + steering; else write up the executed NEGATIVE
     (with threshold sweep + diagnostic proving it is structural, not a knob artifact).

  # ============================================================================
  # C1 classification (NEVER dropped)
  # ============================================================================
  Form unit + fit pooled-max threshold on TRAIN folds (metadata_fold 0-3); evaluate on TEST fold 4 (no target_word
     leakage). Pooled-max unit activation classifies starts-with-L. Compare unit vs (a),(b),(c),(h).
  Metrics: F1 + AUC + worst-word recall; per-letter paired-bootstrap CIs (B_GAP). LOAD-BEARING half = unit beats
     count-matched (b)/(c)/(h) (beating single best latent (a) is a near-foregone capacity win, completeness only).
  Run L first; then O/T/I/D.

  # ============================================================================
  # STEERING (run LAST so the endpoint always lands; required, null-floored)
  # ============================================================================
  d_unit = normalize(mean over members of W_dec[member])         # mean-member-decoder direction
  d_dom  = W_dec[best_single_member]                              # hub / best-single-latent-alone control
  d_dm   = non-SAE diff-of-means direction (mean resid of L-windows - mean resid of non-L-windows; INDEPENDENT data)
  Rnorm = mean residual L2 norm at layer 12 (for alpha scaling)
  for c in STEER_C: add (c*Rnorm)*dir at blocks.12.hook_resid_post via forward hook during generation on HELD-OUT prompts.
  ON-TARGET = increase in summed next-token prob over L-initial vocab tokens (word-initial 'L'/'l' + 'L'/'l').
  COLLATERAL = full-vocab next-token KL(steered||unsteered) on UNRELATED prompts + PPL on held-out text.
  MATCH on-target across methods (interpolate alpha to equal on-target Delta), then COMPARE collateral.
  Report: d_unit vs d_dm vs d_dom at MATCHED on-target -> lower KL + PPL is the win. Doc-bootstrap CIs + shuffle
     null (random direction). STEERING_PASS := d_unit lower collateral than BOTH d_dm and d_dom at matched on-target.

  # ============================================================================
  # OUTPUT method_out.json (validate with aii-json; split if > size limit via aii-file-size-limit)
  # ============================================================================
  { verdicts:{E1_PASS,E2_PASS,STEERING_PASS, primary_endpoint:'WORKS' or 'DOES_NOT_WORK'},
    per_letter:{L,O,T,I,D}: { anchor_fidelity, E1{precision,recall,F1,null_pctile,threshold_sweep_grid},
        E2{recovered_absorber_counts{unit,g,h,b,c}, sliced_recall{unit,a,b,c,g,h}, paired_bootstrap_CIs, mcnemar_p,
           kg_edge_agreement{prec,recall}}, C1{F1,AUC,worst_word_recall, CIs, holm_p},
        admission{M, signatures_cleared, empirical_false_admit_rate_allnull, false_admit_randomknull},
        cluster_stability_ARI },
    steering:{ on_target_curve, collateral_KL, PPL, matched_comparison, CIs, shuffle_null },
    unit_definitions:[ {letter, members:[idx], member_logit_lens_tokens:[top-k from W_dec[l] times embed.T],
        member_conditioning_contexts:[top-activating corpus windows], anchor_idx, absorber_idxs} ],
    kg_edges:[ {src:anchor, dst:absorber, type:'absorbed_child', sub_context:word, diag_agrees:bool} ],
    config:{release,sae_id,hook,thresholds,seeds}, runtime_stats }
  # Keep big arrays (R matrix, per-latent activations) OUT of method_out.json; save as .npy for provenance.

  # ---------- PRIORITIZATION (partial completion must still yield the primary endpoint) ----------
  # (1) STEP0-1 encode + two-track on L  ->  (2) E1 pilot on L  ->  (3) E2 + C1 on L  ->  (4) steering on L
  #  ->  (5) repeat E1/E2/C1 for O/T/I/D  ->  (6) admission multiplicity across letters.
  # SCALING: mini (L, ~10 on-words) confirm signal; then full L; then O/T/I/D. Process letters sequentially;
  #   discard residual caches after pooling; bf16; chunk corpus encoding.
fallback_plan: >-
  MODEL/SAE LOADING: primary = raw HF transformers on unsloth/gemma-2-2b (non-gated) + hidden_states[13] (== blocks.12.hook_resid_post).
  The SAE reconstruction GATING CHECK (cosine>0.9, EV>0.5) is the ground-truth correctness test: if it fails, the activations
  are wrong -> try (a) forward-hook on model.model.layers[12] output[0], (b) confirm you took hidden_states[13] not [12],
  (c) check for an activation-scaling normalization the SAE expects, (d) try google/gemma-2-2b with HF_TOKEN via transformer_lens
  HookedTransformer/HookedSAETransformer (which name the hook directly). Do NOT proceed past a failing reconstruction check.
  WORD POSITION: word-token (offset-mapping) is primary; if the anchor is weak or no parent emerges, try last-token (the colon
  answer position) and mean-pool, and report which position the diagnostic/probe works at. NO PARENT AT L12 (unexpected, since
  L12 is in the valid 0-17 range and is the densest layer): switch SAE to layer_12/width_65k/canonical (more features) and
  report; if still absent, that is itself a finding. SCR/TPP (g)/(h): if SAEBench integration is too heavy, the pinned attribution
  proxy (|d_p . W_dec[l]| * mean_activation_l) is acceptable (g/h are explicitly reference oracles, not ground truth). PROBE
  d_p: if corpus-trained probe acc<0.8, train on held-out content-flip on-words (still disjoint from the clustering pairs
  used to form units) or pool more corpus windows. E1 FAILURE (K-track cannot recover parent+>=2 absorbers above null): this
  IS the declared primary NEGATIVE (method does not work) -- report it honestly with the full threshold sweep + the diagnostic
  parent/absorbers to prove it is structural, not a knob artifact; the paper writes up the executed negative. E2 TIE (unit
  ties g/h on sliced recall): report as the secondary characterization 'robustness is pooling -> contribution reduces to absorber-recovery
  count + KG'. STEERING no advantage: report the on-target/collateral curves anyway (a clean null is publishable; steering
  is a generality demo, not load-bearing for E1/E2). GPU OOM: reduce batch to 8-16, fp16, encode corpus in chunks discarding
  residuals after pooling, store latent activations sparsely (JumpReLU is mostly zero), process one letter at a time. TIME
  SHORTFALL: strict order above -- L all the way through steering before touching O/T/I/D, so a partial run still delivers
  the L primary endpoint + steering. Robustness baselines (j)/(k), toxicity, and the auditability repair loop are OUT OF SCOPE
  for this artifact (other artifacts) -- do not start them. Core pipeline uses NO OpenRouter/LLM calls ($0); only an OPTIONAL
  stretch LLM-judge member-labeling would, and it must respect the $10 hard cap (skip if time/budget tight).
testing_plan: >-
  Follow aii-long-running-tasks gradual scaling; gate each stage on a confirmation signal before scaling. STAGE 0 (smoke,
  ~2 min): detect GPU (aii-use-hardware); load SAE (assert W_dec [16384,2304]) with the defensive tuple-or-object loader;
  load unsloth/gemma-2-2b; encode ~64 corpus windows and RUN THE RECONSTRUCTION GATING CHECK (mean cosine>0.9 AND explained_variance>0.5).
  If this fails, STOP and fix activation extraction (layer index/position/scaling) before anything else -- every downstream
  number depends on it. STAGE 1 (mini pilot on L, ~10 on-words, t_verbose only, ~5 min): compute content-response R; find
  ANCHOR (highest-|C_l| latent); CONFIRM (i) anchor logit-lens (W_dec[anchor] times embed.T top tokens) promotes L-initial/'L'/'l'
  tokens, (ii) anchor firing is SELECTIVE on L-words (not near-uniform over corpus), (iii) corpus-trained d_p probe test-acc>0.8,
  (iv) the form-free diagnostic returns a parent and >=1 absorber, (v) K-track runs end-to-end and proposes a multi-member
  unit, (vi) membership F1 vs the diagnostic exceeds the random-membership null. These six are the GO signal that the pipeline
  is wired correctly. STAGE 2 (full L, all carriers, ~20-40 min): run STEP1-5 + E1 (with anchor-fidelity + threshold sweep)
  + diagnostic + baselines (a/b/c/g/h) + E2 (counts, sliced recall, paired-bootstrap CIs, McNemar, KG agreement) + C1 (folded)
  + admission (M, BH/Holm, empirical false-admit) + steering. CHECKPOINT: record E1_PASS / E2_PASS / STEERING_PASS for L.
  STAGE 3 (O/T/I/D): repeat STEP1-5 + E1/E2/C1 per letter; aggregate admission multiplicity across letters. STAGE 4: assemble
  method_out.json, validate against any provided schema with aii-json, and check size with aii-file-size-limit (keep big arrays
  in .npy, not the JSON). Throughout, log per-stage timings and assert intermediate shapes (R[16384 x n_words], firing booleans,
  cover-set sizes) to catch wiring bugs early. Sanity cross-checks: anchor should have the LARGEST cover set; absorbers should
  have firing-Jaccard<0.1 with the anchor and fire on words the anchor misses; surface-flip pooled response should be near
  zero (much smaller than content-flip response).
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
