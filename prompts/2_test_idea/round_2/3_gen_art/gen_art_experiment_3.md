# gen_art_experiment_3 — test_idea

> Phase: `invention_loop` · round 2 · `gen_art`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_experiment_3` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-17 15:42:13 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_3`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_3/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_3/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_3/results/out.json`
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
  C3 Generality Experiment: Does SAE Feature Absorption Generalize Beyond First-Letter Spelling? (Numeric + Taxonomic Hierarchies,
  Gemma Scope L12/16k)
summary: >-
  Execute the never-dropped Tier-1a SECOND (non-spelling) absorption hierarchy for the C3 spine of the two-track CCRG hypothesis.
  Encode the frozen non-spelling testbed (numeric primary, taxonomic alternative) through Gemma-2-2b + Gemma Scope layer_12/width_16k
  SAE; run the NON-TRIVIALITY GATE (does a high-recall general parent latent exist AND have specialist-filled, mutually-exclusive,
  precise absorber holes?). If the gate passes, run the K-track anchored greedy set-cover proposal, report recovered-absorber
  count + per-sub-context sliced recall vs the (g) SCR/TPP oracle pool and (h) count-matched pool, and score KG specialization
  edges with the FORM-FREE (probe-projection / absorption_fraction) diagnostic (parent probe trained on DISJOINT corpus data
  -> non-circular). If the gate fails on BOTH hierarchies, deliver the clean honest-null finding 'absorption is spelling-specific'
  (uniform high per-sub-context parent recall), which scopes the C3 title claim to spelling and routes generality through
  C1. Self-contained on the non-spelling testbed; produces a publishable result either way. GPU profile (Gemma-2-2b inference);
  well within a single-GPU 6h budget.
runpod_compute_profile: gpu
implementation_pseudocode: |-
  ################################################################################
  # OVERVIEW. This is the SECONDARY C3 generality run (the PRIMARY first-letter
  # E1/E2 lives in a sibling artifact). Goal: a GO/NO-GO on whether absorption
  # generalizes to a NON-spelling token hierarchy, plus, if GO, the absorber-
  # recovery numbers vs marginal-attribution pools. Either outcome is publishable.
  # Order: numeric_absorption FULLY first (primary novelty test); taxonomic_absorption
  # only after numeric completes (alternative). Single GPU, ~6h wall-clock; the SAE
  # work is ~24k short forward passes => minutes, so budget is generous.
  #
  # DEPENDENCIES (read these EXACT pins, do not re-derive):
  #  - DATA  art_t2uUbjSwpd3t: full_data_out.json  (two datasets:
  #      'numeric_absorption' ~8,380 ex; 'taxonomic_absorption' ~15,748 ex).
  #      Row fields (FLAT metadata_* keys): input(str), output('positive'|'negative'
  #      = PARENT label), metadata_row_type in {content_pair, surface_pair, corpus},
  #      metadata_sub_context (numeric: year|percent|currency|date|decimal|integer|
  #      comma_number|ordinal ; taxonomic: a country name | null for negatives),
  #      metadata_pair_id, metadata_pair_role in {x_on,x_off,surface_a,surface_b,null},
  #      metadata_target_char_start/end, metadata_target_token_indices (gemma-2-2b,
  #      computed add_special_tokens=False -> SEE BOS GOTCHA), metadata_fold in
  #      {train,test,diagnostic}, metadata_neg_family, metadata_multi_token,
  #      metadata_notes ('ambiguous_homograph' for Turkey/Georgia/Chile/Jordan).
  #      ELIGIBLE sub-contexts (>=150 diagnostic positives, from manifest.json
  #      absorption_readiness): numeric ALL 8; taxonomic 20 countries
  #      (Canada,France,Iran,United States,Brazil,Georgia,New Zealand,Spain,Mexico,
  #       China,Japan,India,Italy,Ireland,Australia,Poland,Germany,United Kingdom,
  #       Israel,Russia). Others = descriptive_only (report, do NOT use for inference).
  #  - METHOD dossier art_RidEJtBC7gPT/research_out.json: SAE pipeline + K-track
  #      + baselines (g)/(h) + stats. DIAGNOSTIC dossier art_I2MrezW41iQo: form-free
  #      diagnostic + non-triviality gate.
  #
  # PINNED SAE/MODEL (verbatim from dossiers):
  #   SAE = sae_lens.SAE.from_pretrained(release='gemma-scope-2b-pt-res-canonical',
  #                                      sae_id='layer_12/width_16k/canonical')
  #         DEFENSIVE: ret=...; sae = ret[0] if isinstance(ret,tuple) else ret
  #         d_model=2304, W_dec shape [16384,2304], hook='blocks.12.hook_resid_post'
  #         JumpReLU => firing = (sae.encode(acts) > 0)  (threshold is inside encode)
  #   MODEL = google/gemma-2-2b (gated). Try HF_TOKEN; FALLBACK mirror unsloth/gemma-2-2b
  #         (vocab 256000). Width-robustness secondary SAE: 'layer_12/width_65k/canonical'
  #         (absorption WORSENS at wider SAEs -> good robustness axis; run only if time).
  ################################################################################

  #=============================================================================
  # PHASE 0  ENV + ENCODER  (build once, reuse for both hierarchies)
  #=============================================================================
  # uv venv; install: torch, transformer_lens (or transformers), sae_lens,
  #   scikit-learn, scipy, numpy, igraph+leidenalg (C-track, optional here),
  #   loguru, tqdm. (see aii-python, aii-parallel-computing, aii-use-hardware.)
  # Detect GPU; load model in bf16/fp16 on cuda.
  #
  # PREFERRED loader = transformer_lens HookedTransformer/HookedSAETransformer so the
  # hook name 'blocks.12.hook_resid_post' is unambiguous:
  #   model = HookedTransformer.from_pretrained('gemma-2-2b', dtype='bfloat16')
  #   (if gated load fails: AutoModelForCausalLM.from_pretrained('unsloth/gemma-2-2b')
  #    then HookedTransformer.from_pretrained('gemma-2-2b', hf_model=hf, tokenizer=tok).)
  # HF FALLBACK: model.forward(output_hidden_states=True); residual AFTER block 12
  #   == hidden_states[13]  (hidden_states[0]=embeddings, hidden_states[i+1]=block i out).
  #   VALIDATE the layer mapping (critical, see VALIDATION below).
  #
  # def encode_batch(texts, char_spans, stored_idx_list, roles):
  #   # tokenize WITH bos (prepend_bos=True default for gemma) + offsets
  #   enc = tokenizer(texts, return_offsets_mapping=True, add_special_tokens=True,
  #                   padding=True, truncation=True, max_length=128, return_tensors='pt')
  #   run model -> resid = cache['blocks.12.hook_resid_post']  # [B,T,2304]
  #   lat = sae.encode(resid)                                   # [B,T,16384] (sparse-ish)
  #   for each example pick TARGET positions:
  #     if target_text non-empty (x_on / corpus / surface): positions p whose offset
  #        span overlaps [char_start,char_end)  -> robust, BOS-safe.
  #     else (x_off, zero-width span): use stored metadata_target_token_indices
  #        SHIFTED +1 for the single prepended <bos> (BOS GOTCHA: stored indices were
  #        computed add_special_tokens=False; model run prepends exactly one bos).
  #     pooled_latent = MAX over target positions of lat  # [16384] (max-pool handles
  #        multi-token years/countries; report sum-pool as robustness alt only).
  #     also keep pooled RESIDUAL (max or mean over same positions) for dense probes.
  #   return latent_vec(fp16, store as scipy.sparse CSR; ~24k x 16384 dense fp16 ~0.8GB
  #        but JumpReLU is sparse -> CSR is far smaller), residual_vec(fp16), and the
  #        actual token strings selected (for the alignment assert).
  #
  # MEMORY-SAFE: batch 16-32 texts; pull only blocks.12 cache; encode; pool; DISCARD
  #   the [B,T,*] tensors immediately. Persist per-row pooled latent (CSR) + pooled
  #   residual (fp16 np.memmap or .npz) keyed by a stable row id, so re-runs are cheap.
  #
  # VALIDATION GATES (must pass before any analysis; abort + log if not):
  #   (V1 layer/SAE correctness) On ~200 corpus rows compute FVU = ||resid - sae.decode(
  #        sae.encode(resid))||^2 / ||resid - mean||^2 at the target token. Expect ~0.1-0.4.
  #        If FVU ~1.0 -> WRONG layer/hook (e.g. HF off-by-one) -> fix mapping.
  #   (V2 alignment) For >=200 x_on/corpus rows, decode the selected target tokens and
  #        assert string match to metadata_target_text >= 0.98 (strip leading space).
  #   (V3 sparsity) mean L0 of firing latents per token in plausible Gemma Scope range
  #        (~tens-to-low-hundreds); if ~0 or ~16384 the pipeline is broken.

  #=============================================================================
  # PHASE 1  PER-HIERARCHY FEATURE TENSORS  (run for 'numeric' first)
  #=============================================================================
  # Split rows by metadata_row_type and metadata_fold:
  #   PAIRS  = content_pair rows -> {pair_id: (x_on row, x_off row)} ; use fold 'train'
  #           for clustering/anchor, 'test' for held-out recall reporting.
  #   SURF   = surface_pair rows (surface_a,surface_b) -> unit-level surface-invariance.
  #   CORPUS = corpus rows; fold 'train' -> probe training; fold 'diagnostic' -> the
  #           parent-hole search + sliced recall (DISJOINT from probe-train => non-circular).
  #
  # Encode all needed rows once (Phase 0). Build:
  #   A_on[L,Npair], A_off[L,Npair]  pooled latent acts (max-pool target tokens)
  #   FIRE_on = A_on>0 ; FIRE_off = A_off>0
  #   R[L,Npair] = A_on - A_off                              # content-response matrix
  #   CORP_lat[L, Ncorp_diag], CORP_fire, with parent label y (pos/neg) and sub_context.

  #=============================================================================
  # PHASE 2  STEP-1 content-responsive latents + ANCHOR  (no diagnostic used)
  #=============================================================================
  # Shuffled-pair NULL: permute x_on<->x_off labels within concept; recompute mean|R|
  #   per latent over B=1000 shuffles -> per-latent 95th-pct null threshold tau95_l.
  # CONTENT-RESPONSIVE set = { l : mean_p R[l,p] > tau95_l }.
  # Cover set C_l = { pairs p : R[l,p] > tau_resp(=median positive response or small
  #   abs floor) AND FIRE_on[l,p] AND per-latent content-response PRECISION>=0.70 }
  #   where precision(l) = #{p: fires on x_on & not on x_off} / #{p: fires on x_on}.
  # ANCHOR = argmax_l |C_l| over content-responsive latents (tie-break: broadest /
  #   lowest-entropy firing support).  *** chosen from PAIRS ONLY, NOT the diagnostic.***
  # anchor_recall_contentflip = |C_anchor| / Npair.
  # anchor_recall_corpus = recall of anchor on CORPUS diagnostic-fold parent-positives
  #   (fires>0), at the firing rule above. Report BOTH.
  # Also record diagnostic-parent latent = argmax_l cos(W_enc[l], d_p) for ANCHOR-
  #   FIDELITY reporting (d_p from Phase 4 probe) — to check anchor==diagnostic parent
  #   and that no high-frequency polysemantic latent usurped the anchor (firing-rate sanity).

  #=============================================================================
  # PHASE 3  NON-TRIVIALITY GATE  (THE GO/NO-GO — diagnostic dossier art_I2MrezW41iQo)
  #=============================================================================
  # Compute, per candidate absorber latent l (content-responsive, l != anchor):
  #   HOLES H = parent-positive items the anchor MISSES (anchor silent / not in C_anchor).
  #            Use BOTH supports and report: (Ha) content-flip x_on pairs uncovered by
  #            anchor; (Hb) corpus diagnostic positives where anchor doesn't fire.
  #   firing_Jaccard(l,anchor) = |FIRE_l & FIRE_anchor| / |FIRE_l | FIRE_anchor|
  #                              (over corpus diagnostic parent-positives).
  #   sub_context_precision(l) = max over sub-contexts s of
  #            #{l fires & sub==s} / #{l fires on parent-positives}.   (which s it specializes)
  #   hole_coverage_gain(l) = fraction of H that l covers (l fires) — marginal over anchor.
  #   bootstrap (B=2000, resample H items) 95% CI on hole_coverage_gain.
  # GATE PASSES for the hierarchy IFF:
  #   (G1) anchor_recall >= 0.60  (use the higher-powered of content-flip / corpus; report both)
  #   (G2) EXISTS >=1 (target >=2) absorber l with: firing_Jaccard<0.10 AND
  #        sub_context_precision>=0.70 AND hole_coverage_gain>=0.05 with bootstrap CI low >0.
  # Log a THRESHOLD SENSITIVITY note: also report counts of passing absorbers at
  #   Jaccard in {0.05,0.10,0.20}, precision in {0.60,0.70,0.80}, gain in {0.03,0.05,0.10}
  #   so the verdict is shown not knife-edge.
  #
  # IF GATE PASSES on numeric -> Phase 4-7 for numeric (the positive C3 result), then
  #   STILL run numeric->done; taxonomic is optional corroboration if budget remains.
  # IF GATE FAILS on numeric -> run the SAME Phases 2-3 on taxonomic_absorption.
  # IF GATE FAILS on BOTH -> go to Phase 8 (honest null).

  #=============================================================================
  # PHASE 4  PARENT PROBE d_p  (for form-free diagnostic; trained on DISJOINT data)
  #=============================================================================
  # Train sklearn LogisticRegression on pooled RESIDUAL vectors (2304-d) at target
  #   token, parent positive vs negative, on CORPUS *train* fold only.
  # d_p = probe.coef_ (unit-normalized 2304-vector) = parent-concept direction.
  # Report parent_probe_recall per sub-context on the diagnostic fold (used for the
  #   honest-null uniformity check too).  *** disjoint from diagnostic fold => non-circular.***

  #=============================================================================
  # PHASE 5  K-TRACK PROPOSAL  (anchored greedy max-coverage — method dossier STEP-3)
  #=============================================================================
  # unit = {anchor}; H = HOLES of anchor (use content-flip support Ha as primary,
  #        corroborate on Hb).
  # while H not empty and improving:
  #     l* = argmax_l |C_l ∩ H|   over content-responsive l not in unit
  #     accept l* IFF firing_Jaccard(l*, every member)<0.10 AND precision(l*)>=0.70
  #                  AND marginal coverage gain = |C_l* ∩ H|/|H_0| >= 0.05 with
  #                  bootstrap CI (resample holes) excluding 0.
  #     if accepted: unit += l*; H = H \ C_l* ;  else break.
  # recovered_absorber_count = |unit| - 1.
  # Record each edge anchor->l* with the sub-context l* specializes (argmax precision s).
  # ADMISSION (signature K) sanity: pooled-max content-response AUC(unit) minus best-
  #   single-member AUC > 95th pct of an AUC-matched random-k null (B=1000), AND the
  #   k in {2,3} absolute gain>=0.05 CI-excl-0, AND unit-level SURFACE INVARIANCE:
  #   pooled surface-response on SURF pairs not above a shuffled-surface null. Report.

  #=============================================================================
  # PHASE 6  BASELINES (g)/(h) + SLICED-RECALL  (the C3 absorber-recovery numbers)
  #=============================================================================
  # Marginal-attribution selection (SCR/TPP-style) to the PARENT concept:
  #   attribution(l) = |mean A_on_latent_l[pos] - mean[neg]| on the CORPUS train fold
  #     (mean-difference / MMD). (Alt: LR-probe weight on latent acts * latent std.)
  #   rank latents by attribution.
  #   (g) ORACLE POOL = top-N latents, N=20 (default).  max-pool detector.
  #   (h) COUNT-MATCHED POOL = top-k latents, k = |unit| member count. max-pool detector.
  #   Note: narrow absorbers fire only in one sub-context -> LOW marginal attribution
  #         over all parent-positives -> DROPPED by (g)/(h). This is the gap the unit fills.
  # SLICED RECALL on CORPUS diagnostic fold, per ELIGIBLE sub-context s (>=150 positives):
  #   recall_X(s) = fraction of sub-context-s positives where detector X fires (>0 / max-pool).
  #   detectors X in { UNIT, anchor_alone, (g), (h) }.
  #   Choose firing thresholds per detector to MATCH overall parent recall (fair compare),
  #   OR report at the >0 JumpReLU firing rule; report both, primary = matched-recall.
  # PRIMARY C3 inferential object: per absorbed sub-context (where anchor has holes),
  #   paired bootstrap (B=10000 over diagnostic tokens) 95% CI on recall_UNIT(s) -
  #   recall_(g)(s) and - recall_(h)(s); also exact McNemar on per-token hit/miss
  #   (statsmodels mcnemar exact). Aggregate over absorbed sub-contexts (descriptive).
  #   Multiplicity: Holm-Bonferroni / BH over the per-sub-context tests; report corrected.
  # C3 CONFIRMED for the hierarchy iff UNIT recovers >=1 absorber (g)/(h) drop AND
  #   UNIT-minus-(g)/(h) sliced-recall CI excludes 0 on >=1 absorbed sub-context.

  #=============================================================================
  # PHASE 7  KG SPECIALIZATION-EDGE AGREEMENT  (FORM-FREE diagnostic — non-circular)
  #=============================================================================
  # Form-free absorption (paper App. A.13 == SAEBench absorption_fraction):
  #   absorption_fraction(l on token t) = (a_hat_l . d_p) / (a . d_p),
  #       a_hat_l = enc_act_l(t) * W_dec[l]   (a single latent's reconstruction contrib),
  #       a        = sae.decode(sae.encode(resid_t))  (full SAE reconstruction) — or resid_t.
  # For each proposed edge anchor->absorber(l*, sub-context s): on diagnostic-fold
  #   sub-context-s tokens that are ANCHOR HOLES (parent present, anchor silent):
  #     diag_absorber(t) = argmax over content-responsive latents of absorption_fraction.
  #   EDGE AGREEMENT = fraction of such hole-tokens where diag_absorber == l*
  #     (or l* in top-3). NULL = same with a random content-responsive latent as the
  #     'proposed' absorber (B=1000) -> report agreement_rate vs null mean+CI.
  #   (Threshold-free argmax avoids pinning tau_c; ALSO log raw absorption_fraction
  #    distribution. If SAEBench tau_c is found in code, additionally report the
  #    binary 'absorbs' rate at that tau_c.)
  # d_p is trained on DISJOINT corpus-train fold => diagnostic only SCORES edges, never
  #   forms units. by-construction risk (holes ~ parent false-negatives) is controlled
  #   by the random-latent null.

  #=============================================================================
  # PHASE 8  HONEST-NULL BRANCH  (only if GATE fails on numeric AND taxonomic)
  #=============================================================================
  # Confirm 'absorption is spelling-specific':
  #   - Report per-sub-context parent (anchor + probe) recall; show it is UNIFORMLY HIGH
  #     (no sub-context with a dramatic recall hole) => no specialist-filled holes.
  #   - Report that no candidate absorber clears (Jaccard<0.10 & precision>=0.70 &
  #     gain CI>0) on either hierarchy.
  #   - verdict='spelling_specific_null'; state C3 title scoped to spelling-type
  #     hierarchical absorption, generality routed through C1. THIS IS A PUBLISHABLE
  #     FINDING, not a method failure.

  #=============================================================================
  # PHASE 9  EMIT method_out.json  (+ schema-validate well-formedness via aii-json)
  #=============================================================================
  # {
  #   'verdict': 'non_spelling_absorption_confirmed' | 'spelling_specific_null'
  #              | 'partial_<hierarchy>',
  #   'sae': {release, sae_id, hook, d_model, width, fvu_check, mean_l0},
  #   'model': 'gemma-2-2b' (or unsloth mirror),
  #   'per_hierarchy': { 'numeric': {...}, 'taxonomic': {...} },
  #     # each: gate_decision, anchor_latent, anchor_recall_{contentflip,corpus},
  #     #       anchor_fidelity (anchor==diagnostic_parent? usurp check),
  #     #       parent_probe_recall_by_subcontext, non_triviality{passing absorbers w/
  #     #       jaccard/precision/gain+CI}, threshold_sensitivity, k_track_unit{members},
  #     #       recovered_absorber_count, baselines{g_pool,h_pool},
  #     #       sliced_recall{ s: {unit,anchor,g,h, unit_minus_g_ci, unit_minus_h_ci,
  #     #                          mcnemar_p, holm_p} }, kg_edges[...],
  #     #       kg_agreement_rate, kg_agreement_null, admission{signatureK, surface_inv}
  #   'eligible_subcontexts': {...}, 'descriptive_only': {...},
  #   'stats': {bootstrap_B, n_min:150, multiplicity:'holm/bh'},
  #   'honest_null': {... if applicable ...},
  #   'failure_modes_observed': [...], 'runtime_s': ..., 'gpu': ...
  # }
  # Also save intermediate arrays (anchor idx, unit members, attribution ranks,
  # per-subcontext recall tables) as .npz / .csv for the paper figures.
  #
  # GRADUAL SCALING (aii-long-running-tasks): (1) smoke = 10 rows, V1-V3 gates;
  # (2) mini = numeric, ONE sub-context (year) end-to-end -> anchor+gate+sliced recall;
  # (3) full numeric; (4) taxonomic. Checkpoint after each. 65k-width robustness last.
fallback_plan: |-
  GATED-MODEL ACCESS: if google/gemma-2-2b is gated and HF_TOKEN fails, load weights from the non-gated mirror unsloth/gemma-2-2b (vocab 256000, identical weights) and wrap in transformer_lens via hf_model=. If transformer_lens can't host gemma-2-2b cleanly, fall back to raw HF transformers with output_hidden_states=True and residual = hidden_states[13] (block-12 output) — but ONLY after the FVU validation (V1) confirms the layer index (FVU~0.1-0.4 correct vs ~1.0 wrong; try hidden_states[12] and [13] and keep the one the SAE reconstructs).

  TOKEN ALIGNMENT BREAKS (V2 fails): primary path re-derives target positions from char offsets (BOS-safe). If offset mapping is unreliable for some rows, fall back to stored metadata_target_token_indices + an empirically measured BOS offset (verify the tokenizer prepends exactly one <bos>; offset is +1). If a specific row still misaligns, drop it and log; keep coverage >=95% per sub-context (eligibility floor 150 has headroom). As a last resort use MEAN-pool over all non-special tokens (cruder but robust) and flag the run as pooled-not-token-localized.

  GATE FAILS ON NUMERIC: this is EXPECTED-possible (dossier WP2: absorption documented ONLY on spelling). Immediately run the identical Phases 2-3 on taxonomic_absorption (the pre-registered alternative). If taxonomic ALSO fails, that is the clean Phase-8 honest null — deliver it confidently with the uniform per-sub-context recall evidence; do NOT manufacture a positive.

  ANCHOR DEGENERACY: if argmax|C_l| picks a high-frequency polysemantic latent (fires on ~everything, low precision) instead of a true parent, the precision>=0.70 cover-set filter should exclude it; if not, restrict the anchor search to latents with corpus firing-rate < 0.5 on NEGATIVES (a parent fires on positives, not negatives) and re-pick. Report the anchor-fidelity check (anchor vs diagnostic max-encoder-cosine parent).

  NO ABSORBER CLEARS THE GAIN-CI BUT GATE-1 PASSES (parent exists, holes not specialist-filled): report 'parent present, no recoverable absorbers' — a graded null that still scopes C3; do not force a K-track unit. If the greedy proposer returns only the anchor, recovered_absorber_count=0 and the C3 claim for that hierarchy is reported negative.

  BASELINE (g)/(h) AMBIGUITY: if a full SAEBench SCR/TPP install is heavy/flaky, the mean-difference (MMD) attribution ranking specified in Phase 6 IS the faithful, self-contained SCR/TPP surrogate (latents ranked by causal/marginal relevance to the parent probe) — use it directly; note SCR/TPP are 'reference oracles not ground truth' (2605.18229). Keep N=20 for (g) and k=|unit| for (h).

  COMPUTE/MEMORY: if storing dense fp16 latents (24k x 16384) strains RAM, store JumpReLU activations as scipy CSR (they are sparse) or only keep latents that pass the content-responsive prefilter (typically << 16384). If GPU OOM on batch, drop batch size to 8 and max_length to 96. The 65k-width robustness SAE is the FIRST thing to drop if time runs short.

  STATISTICS UNDERPOWERED: every eligible sub-context already has >=150 diagnostic positives (n_min met). If paired bootstrap CIs are wide, report them honestly and lean on the aggregate (descriptive) + the binary gate decision rather than overclaiming per-sub-context significance.
testing_plan: "BUILD UP SMALL -> BIG, with hard confirmation signals at each step before scaling (aii-long-running-tasks,\
  \ aii-use-hardware):\n\n1) SMOKE (seconds, ~10 rows, no analysis): load SAE with the defensive tuple-unwrap; assert sae.W_dec.shape==[16384,2304].\
  \ Load model. Encode 10 mixed rows. CONFIRM: (V3) per-token firing L0 is in the tens-to-low-hundreds (not 0, not ~16384);\
  \ (V1) FVU at target tokens ~0.1-0.4 (proves correct layer/hook — if ~1.0 STOP and fix the layer index BEFORE anything else);\
  \ (V2) decoded target tokens string-match metadata_target_text for x_on/corpus rows (>=0.98). These three gates catch every\
  \ high-risk pipeline bug (wrong layer, BOS offset, dead/saturated SAE) up front.\n\n2) MINI END-TO-END (minutes, numeric\
  \ / sub-context='year' only): encode that slice + a sample of negatives; run Phase 2 (anchor), Phase 3 (gate on year holes),\
  \ Phase 5 (greedy), Phase 6 (sliced recall vs g/h on year). CONFIRM: an anchor latent exists with sensible recall; the pipeline\
  \ produces a numeric anchor whose top-activating contexts (logit-lens / decoded) look numeric (sanity, eyeball 3-5). This\
  \ proves the whole chain executes and the numbers are not degenerate, on a cheap slice.\n\n3) CONFIRMATION SIGNALS that\
  \ the experiment is 'working' (vs broken): (a) the anchor latent fires on a clear majority of parent-positives and rarely\
  \ on negatives (recall>=0.6, low false-positive) — if it fires on everything, anchor selection is broken; (b) the anchor's\
  \ per-sub-context recall is NOT uniform if absorption is present (some sub-contexts much lower = the holes) — uniform-high\
  \ recall is the NULL signal (legitimate, route to Phase 8); (c) marginal-attribution (g)/(h) pools are dominated by high-frequency\
  \ latents and the ranking is stable across two attribution variants (MMD vs probe-weight) — sanity that 'oracle' selection\
  \ behaves. \n\n4) FULL NUMERIC: run all phases; checkpoint method_out partial. Verify the gate decision is robust to the\
  \ threshold-sensitivity sweep (Phase 3) — the verdict shouldn't flip between Jaccard 0.05<->0.10. \n\n5) TAXONOMIC: only\
  \ after numeric is fully written out. Watch the multi-token / ambiguous-homograph flags (United States, Turkey/Georgia/Chile/Jordan)\
  \ — for multi-token countries confirm max-pool over the country's token span; for homographs, the country-positive corpus\
  \ rows were already disambiguated at build time, but spot-check 3-5.\n\n6) ROBUSTNESS (only if budget remains): re-run the\
  \ gate + sliced-recall on the 65k-width SAE; absorption should be EQUAL-OR-STRONGER at 65k (wider) — if it appears only\
  \ at 16k, note the width sensitivity. Cross-check sum-pool vs max-pool does not flip the verdict.\n\n7) FINAL: validate\
  \ method_out.json is well-formed JSON and contains the required keys (verdict, per_hierarchy gate_decision, sliced_recall\
  \ with CIs, kg_edges, honest_null-if-applicable) via the aii-json skill before finishing."
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

### [2] HUMAN-USER prompt · 2026-06-17 15:42:13 UTC

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

### [3] SKILL-INPUT — aii-use-hardware · 2026-06-17 15:42:31 UTC

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

### [4] SKILL-INPUT — aii-long-running-tasks · 2026-06-17 15:42:31 UTC

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

### [5] SKILL-INPUT — aii-json · 2026-06-17 15:46:31 UTC

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

### [6] SKILL-INPUT — aii-python · 2026-06-17 15:46:31 UTC

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

### [7] SKILL-INPUT — aii-file-size-limit · 2026-06-17 15:47:03 UTC

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

### [8] SYSTEM-USER prompt · 2026-06-17 16:50:55 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_3`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_3/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_3/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_3/results/out.json`
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
  C3 Generality Experiment: Does SAE Feature Absorption Generalize Beyond First-Letter Spelling? (Numeric + Taxonomic Hierarchies,
  Gemma Scope L12/16k)
summary: >-
  Execute the never-dropped Tier-1a SECOND (non-spelling) absorption hierarchy for the C3 spine of the two-track CCRG hypothesis.
  Encode the frozen non-spelling testbed (numeric primary, taxonomic alternative) through Gemma-2-2b + Gemma Scope layer_12/width_16k
  SAE; run the NON-TRIVIALITY GATE (does a high-recall general parent latent exist AND have specialist-filled, mutually-exclusive,
  precise absorber holes?). If the gate passes, run the K-track anchored greedy set-cover proposal, report recovered-absorber
  count + per-sub-context sliced recall vs the (g) SCR/TPP oracle pool and (h) count-matched pool, and score KG specialization
  edges with the FORM-FREE (probe-projection / absorption_fraction) diagnostic (parent probe trained on DISJOINT corpus data
  -> non-circular). If the gate fails on BOTH hierarchies, deliver the clean honest-null finding 'absorption is spelling-specific'
  (uniform high per-sub-context parent recall), which scopes the C3 title claim to spelling and routes generality through
  C1. Self-contained on the non-spelling testbed; produces a publishable result either way. GPU profile (Gemma-2-2b inference);
  well within a single-GPU 6h budget.
runpod_compute_profile: gpu
implementation_pseudocode: |-
  ################################################################################
  # OVERVIEW. This is the SECONDARY C3 generality run (the PRIMARY first-letter
  # E1/E2 lives in a sibling artifact). Goal: a GO/NO-GO on whether absorption
  # generalizes to a NON-spelling token hierarchy, plus, if GO, the absorber-
  # recovery numbers vs marginal-attribution pools. Either outcome is publishable.
  # Order: numeric_absorption FULLY first (primary novelty test); taxonomic_absorption
  # only after numeric completes (alternative). Single GPU, ~6h wall-clock; the SAE
  # work is ~24k short forward passes => minutes, so budget is generous.
  #
  # DEPENDENCIES (read these EXACT pins, do not re-derive):
  #  - DATA  art_t2uUbjSwpd3t: full_data_out.json  (two datasets:
  #      'numeric_absorption' ~8,380 ex; 'taxonomic_absorption' ~15,748 ex).
  #      Row fields (FLAT metadata_* keys): input(str), output('positive'|'negative'
  #      = PARENT label), metadata_row_type in {content_pair, surface_pair, corpus},
  #      metadata_sub_context (numeric: year|percent|currency|date|decimal|integer|
  #      comma_number|ordinal ; taxonomic: a country name | null for negatives),
  #      metadata_pair_id, metadata_pair_role in {x_on,x_off,surface_a,surface_b,null},
  #      metadata_target_char_start/end, metadata_target_token_indices (gemma-2-2b,
  #      computed add_special_tokens=False -> SEE BOS GOTCHA), metadata_fold in
  #      {train,test,diagnostic}, metadata_neg_family, metadata_multi_token,
  #      metadata_notes ('ambiguous_homograph' for Turkey/Georgia/Chile/Jordan).
  #      ELIGIBLE sub-contexts (>=150 diagnostic positives, from manifest.json
  #      absorption_readiness): numeric ALL 8; taxonomic 20 countries
  #      (Canada,France,Iran,United States,Brazil,Georgia,New Zealand,Spain,Mexico,
  #       China,Japan,India,Italy,Ireland,Australia,Poland,Germany,United Kingdom,
  #       Israel,Russia). Others = descriptive_only (report, do NOT use for inference).
  #  - METHOD dossier art_RidEJtBC7gPT/research_out.json: SAE pipeline + K-track
  #      + baselines (g)/(h) + stats. DIAGNOSTIC dossier art_I2MrezW41iQo: form-free
  #      diagnostic + non-triviality gate.
  #
  # PINNED SAE/MODEL (verbatim from dossiers):
  #   SAE = sae_lens.SAE.from_pretrained(release='gemma-scope-2b-pt-res-canonical',
  #                                      sae_id='layer_12/width_16k/canonical')
  #         DEFENSIVE: ret=...; sae = ret[0] if isinstance(ret,tuple) else ret
  #         d_model=2304, W_dec shape [16384,2304], hook='blocks.12.hook_resid_post'
  #         JumpReLU => firing = (sae.encode(acts) > 0)  (threshold is inside encode)
  #   MODEL = google/gemma-2-2b (gated). Try HF_TOKEN; FALLBACK mirror unsloth/gemma-2-2b
  #         (vocab 256000). Width-robustness secondary SAE: 'layer_12/width_65k/canonical'
  #         (absorption WORSENS at wider SAEs -> good robustness axis; run only if time).
  ################################################################################

  #=============================================================================
  # PHASE 0  ENV + ENCODER  (build once, reuse for both hierarchies)
  #=============================================================================
  # uv venv; install: torch, transformer_lens (or transformers), sae_lens,
  #   scikit-learn, scipy, numpy, igraph+leidenalg (C-track, optional here),
  #   loguru, tqdm. (see aii-python, aii-parallel-computing, aii-use-hardware.)
  # Detect GPU; load model in bf16/fp16 on cuda.
  #
  # PREFERRED loader = transformer_lens HookedTransformer/HookedSAETransformer so the
  # hook name 'blocks.12.hook_resid_post' is unambiguous:
  #   model = HookedTransformer.from_pretrained('gemma-2-2b', dtype='bfloat16')
  #   (if gated load fails: AutoModelForCausalLM.from_pretrained('unsloth/gemma-2-2b')
  #    then HookedTransformer.from_pretrained('gemma-2-2b', hf_model=hf, tokenizer=tok).)
  # HF FALLBACK: model.forward(output_hidden_states=True); residual AFTER block 12
  #   == hidden_states[13]  (hidden_states[0]=embeddings, hidden_states[i+1]=block i out).
  #   VALIDATE the layer mapping (critical, see VALIDATION below).
  #
  # def encode_batch(texts, char_spans, stored_idx_list, roles):
  #   # tokenize WITH bos (prepend_bos=True default for gemma) + offsets
  #   enc = tokenizer(texts, return_offsets_mapping=True, add_special_tokens=True,
  #                   padding=True, truncation=True, max_length=128, return_tensors='pt')
  #   run model -> resid = cache['blocks.12.hook_resid_post']  # [B,T,2304]
  #   lat = sae.encode(resid)                                   # [B,T,16384] (sparse-ish)
  #   for each example pick TARGET positions:
  #     if target_text non-empty (x_on / corpus / surface): positions p whose offset
  #        span overlaps [char_start,char_end)  -> robust, BOS-safe.
  #     else (x_off, zero-width span): use stored metadata_target_token_indices
  #        SHIFTED +1 for the single prepended <bos> (BOS GOTCHA: stored indices were
  #        computed add_special_tokens=False; model run prepends exactly one bos).
  #     pooled_latent = MAX over target positions of lat  # [16384] (max-pool handles
  #        multi-token years/countries; report sum-pool as robustness alt only).
  #     also keep pooled RESIDUAL (max or mean over same positions) for dense probes.
  #   return latent_vec(fp16, store as scipy.sparse CSR; ~24k x 16384 dense fp16 ~0.8GB
  #        but JumpReLU is sparse -> CSR is far smaller), residual_vec(fp16), and the
  #        actual token strings selected (for the alignment assert).
  #
  # MEMORY-SAFE: batch 16-32 texts; pull only blocks.12 cache; encode; pool; DISCARD
  #   the [B,T,*] tensors immediately. Persist per-row pooled latent (CSR) + pooled
  #   residual (fp16 np.memmap or .npz) keyed by a stable row id, so re-runs are cheap.
  #
  # VALIDATION GATES (must pass before any analysis; abort + log if not):
  #   (V1 layer/SAE correctness) On ~200 corpus rows compute FVU = ||resid - sae.decode(
  #        sae.encode(resid))||^2 / ||resid - mean||^2 at the target token. Expect ~0.1-0.4.
  #        If FVU ~1.0 -> WRONG layer/hook (e.g. HF off-by-one) -> fix mapping.
  #   (V2 alignment) For >=200 x_on/corpus rows, decode the selected target tokens and
  #        assert string match to metadata_target_text >= 0.98 (strip leading space).
  #   (V3 sparsity) mean L0 of firing latents per token in plausible Gemma Scope range
  #        (~tens-to-low-hundreds); if ~0 or ~16384 the pipeline is broken.

  #=============================================================================
  # PHASE 1  PER-HIERARCHY FEATURE TENSORS  (run for 'numeric' first)
  #=============================================================================
  # Split rows by metadata_row_type and metadata_fold:
  #   PAIRS  = content_pair rows -> {pair_id: (x_on row, x_off row)} ; use fold 'train'
  #           for clustering/anchor, 'test' for held-out recall reporting.
  #   SURF   = surface_pair rows (surface_a,surface_b) -> unit-level surface-invariance.
  #   CORPUS = corpus rows; fold 'train' -> probe training; fold 'diagnostic' -> the
  #           parent-hole search + sliced recall (DISJOINT from probe-train => non-circular).
  #
  # Encode all needed rows once (Phase 0). Build:
  #   A_on[L,Npair], A_off[L,Npair]  pooled latent acts (max-pool target tokens)
  #   FIRE_on = A_on>0 ; FIRE_off = A_off>0
  #   R[L,Npair] = A_on - A_off                              # content-response matrix
  #   CORP_lat[L, Ncorp_diag], CORP_fire, with parent label y (pos/neg) and sub_context.

  #=============================================================================
  # PHASE 2  STEP-1 content-responsive latents + ANCHOR  (no diagnostic used)
  #=============================================================================
  # Shuffled-pair NULL: permute x_on<->x_off labels within concept; recompute mean|R|
  #   per latent over B=1000 shuffles -> per-latent 95th-pct null threshold tau95_l.
  # CONTENT-RESPONSIVE set = { l : mean_p R[l,p] > tau95_l }.
  # Cover set C_l = { pairs p : R[l,p] > tau_resp(=median positive response or small
  #   abs floor) AND FIRE_on[l,p] AND per-latent content-response PRECISION>=0.70 }
  #   where precision(l) = #{p: fires on x_on & not on x_off} / #{p: fires on x_on}.
  # ANCHOR = argmax_l |C_l| over content-responsive latents (tie-break: broadest /
  #   lowest-entropy firing support).  *** chosen from PAIRS ONLY, NOT the diagnostic.***
  # anchor_recall_contentflip = |C_anchor| / Npair.
  # anchor_recall_corpus = recall of anchor on CORPUS diagnostic-fold parent-positives
  #   (fires>0), at the firing rule above. Report BOTH.
  # Also record diagnostic-parent latent = argmax_l cos(W_enc[l], d_p) for ANCHOR-
  #   FIDELITY reporting (d_p from Phase 4 probe) — to check anchor==diagnostic parent
  #   and that no high-frequency polysemantic latent usurped the anchor (firing-rate sanity).

  #=============================================================================
  # PHASE 3  NON-TRIVIALITY GATE  (THE GO/NO-GO — diagnostic dossier art_I2MrezW41iQo)
  #=============================================================================
  # Compute, per candidate absorber latent l (content-responsive, l != anchor):
  #   HOLES H = parent-positive items the anchor MISSES (anchor silent / not in C_anchor).
  #            Use BOTH supports and report: (Ha) content-flip x_on pairs uncovered by
  #            anchor; (Hb) corpus diagnostic positives where anchor doesn't fire.
  #   firing_Jaccard(l,anchor) = |FIRE_l & FIRE_anchor| / |FIRE_l | FIRE_anchor|
  #                              (over corpus diagnostic parent-positives).
  #   sub_context_precision(l) = max over sub-contexts s of
  #            #{l fires & sub==s} / #{l fires on parent-positives}.   (which s it specializes)
  #   hole_coverage_gain(l) = fraction of H that l covers (l fires) — marginal over anchor.
  #   bootstrap (B=2000, resample H items) 95% CI on hole_coverage_gain.
  # GATE PASSES for the hierarchy IFF:
  #   (G1) anchor_recall >= 0.60  (use the higher-powered of content-flip / corpus; report both)
  #   (G2) EXISTS >=1 (target >=2) absorber l with: firing_Jaccard<0.10 AND
  #        sub_context_precision>=0.70 AND hole_coverage_gain>=0.05 with bootstrap CI low >0.
  # Log a THRESHOLD SENSITIVITY note: also report counts of passing absorbers at
  #   Jaccard in {0.05,0.10,0.20}, precision in {0.60,0.70,0.80}, gain in {0.03,0.05,0.10}
  #   so the verdict is shown not knife-edge.
  #
  # IF GATE PASSES on numeric -> Phase 4-7 for numeric (the positive C3 result), then
  #   STILL run numeric->done; taxonomic is optional corroboration if budget remains.
  # IF GATE FAILS on numeric -> run the SAME Phases 2-3 on taxonomic_absorption.
  # IF GATE FAILS on BOTH -> go to Phase 8 (honest null).

  #=============================================================================
  # PHASE 4  PARENT PROBE d_p  (for form-free diagnostic; trained on DISJOINT data)
  #=============================================================================
  # Train sklearn LogisticRegression on pooled RESIDUAL vectors (2304-d) at target
  #   token, parent positive vs negative, on CORPUS *train* fold only.
  # d_p = probe.coef_ (unit-normalized 2304-vector) = parent-concept direction.
  # Report parent_probe_recall per sub-context on the diagnostic fold (used for the
  #   honest-null uniformity check too).  *** disjoint from diagnostic fold => non-circular.***

  #=============================================================================
  # PHASE 5  K-TRACK PROPOSAL  (anchored greedy max-coverage — method dossier STEP-3)
  #=============================================================================
  # unit = {anchor}; H = HOLES of anchor (use content-flip support Ha as primary,
  #        corroborate on Hb).
  # while H not empty and improving:
  #     l* = argmax_l |C_l ∩ H|   over content-responsive l not in unit
  #     accept l* IFF firing_Jaccard(l*, every member)<0.10 AND precision(l*)>=0.70
  #                  AND marginal coverage gain = |C_l* ∩ H|/|H_0| >= 0.05 with
  #                  bootstrap CI (resample holes) excluding 0.
  #     if accepted: unit += l*; H = H \ C_l* ;  else break.
  # recovered_absorber_count = |unit| - 1.
  # Record each edge anchor->l* with the sub-context l* specializes (argmax precision s).
  # ADMISSION (signature K) sanity: pooled-max content-response AUC(unit) minus best-
  #   single-member AUC > 95th pct of an AUC-matched random-k null (B=1000), AND the
  #   k in {2,3} absolute gain>=0.05 CI-excl-0, AND unit-level SURFACE INVARIANCE:
  #   pooled surface-response on SURF pairs not above a shuffled-surface null. Report.

  #=============================================================================
  # PHASE 6  BASELINES (g)/(h) + SLICED-RECALL  (the C3 absorber-recovery numbers)
  #=============================================================================
  # Marginal-attribution selection (SCR/TPP-style) to the PARENT concept:
  #   attribution(l) = |mean A_on_latent_l[pos] - mean[neg]| on the CORPUS train fold
  #     (mean-difference / MMD). (Alt: LR-probe weight on latent acts * latent std.)
  #   rank latents by attribution.
  #   (g) ORACLE POOL = top-N latents, N=20 (default).  max-pool detector.
  #   (h) COUNT-MATCHED POOL = top-k latents, k = |unit| member count. max-pool detector.
  #   Note: narrow absorbers fire only in one sub-context -> LOW marginal attribution
  #         over all parent-positives -> DROPPED by (g)/(h). This is the gap the unit fills.
  # SLICED RECALL on CORPUS diagnostic fold, per ELIGIBLE sub-context s (>=150 positives):
  #   recall_X(s) = fraction of sub-context-s positives where detector X fires (>0 / max-pool).
  #   detectors X in { UNIT, anchor_alone, (g), (h) }.
  #   Choose firing thresholds per detector to MATCH overall parent recall (fair compare),
  #   OR report at the >0 JumpReLU firing rule; report both, primary = matched-recall.
  # PRIMARY C3 inferential object: per absorbed sub-context (where anchor has holes),
  #   paired bootstrap (B=10000 over diagnostic tokens) 95% CI on recall_UNIT(s) -
  #   recall_(g)(s) and - recall_(h)(s); also exact McNemar on per-token hit/miss
  #   (statsmodels mcnemar exact). Aggregate over absorbed sub-contexts (descriptive).
  #   Multiplicity: Holm-Bonferroni / BH over the per-sub-context tests; report corrected.
  # C3 CONFIRMED for the hierarchy iff UNIT recovers >=1 absorber (g)/(h) drop AND
  #   UNIT-minus-(g)/(h) sliced-recall CI excludes 0 on >=1 absorbed sub-context.

  #=============================================================================
  # PHASE 7  KG SPECIALIZATION-EDGE AGREEMENT  (FORM-FREE diagnostic — non-circular)
  #=============================================================================
  # Form-free absorption (paper App. A.13 == SAEBench absorption_fraction):
  #   absorption_fraction(l on token t) = (a_hat_l . d_p) / (a . d_p),
  #       a_hat_l = enc_act_l(t) * W_dec[l]   (a single latent's reconstruction contrib),
  #       a        = sae.decode(sae.encode(resid_t))  (full SAE reconstruction) — or resid_t.
  # For each proposed edge anchor->absorber(l*, sub-context s): on diagnostic-fold
  #   sub-context-s tokens that are ANCHOR HOLES (parent present, anchor silent):
  #     diag_absorber(t) = argmax over content-responsive latents of absorption_fraction.
  #   EDGE AGREEMENT = fraction of such hole-tokens where diag_absorber == l*
  #     (or l* in top-3). NULL = same with a random content-responsive latent as the
  #     'proposed' absorber (B=1000) -> report agreement_rate vs null mean+CI.
  #   (Threshold-free argmax avoids pinning tau_c; ALSO log raw absorption_fraction
  #    distribution. If SAEBench tau_c is found in code, additionally report the
  #    binary 'absorbs' rate at that tau_c.)
  # d_p is trained on DISJOINT corpus-train fold => diagnostic only SCORES edges, never
  #   forms units. by-construction risk (holes ~ parent false-negatives) is controlled
  #   by the random-latent null.

  #=============================================================================
  # PHASE 8  HONEST-NULL BRANCH  (only if GATE fails on numeric AND taxonomic)
  #=============================================================================
  # Confirm 'absorption is spelling-specific':
  #   - Report per-sub-context parent (anchor + probe) recall; show it is UNIFORMLY HIGH
  #     (no sub-context with a dramatic recall hole) => no specialist-filled holes.
  #   - Report that no candidate absorber clears (Jaccard<0.10 & precision>=0.70 &
  #     gain CI>0) on either hierarchy.
  #   - verdict='spelling_specific_null'; state C3 title scoped to spelling-type
  #     hierarchical absorption, generality routed through C1. THIS IS A PUBLISHABLE
  #     FINDING, not a method failure.

  #=============================================================================
  # PHASE 9  EMIT method_out.json  (+ schema-validate well-formedness via aii-json)
  #=============================================================================
  # {
  #   'verdict': 'non_spelling_absorption_confirmed' | 'spelling_specific_null'
  #              | 'partial_<hierarchy>',
  #   'sae': {release, sae_id, hook, d_model, width, fvu_check, mean_l0},
  #   'model': 'gemma-2-2b' (or unsloth mirror),
  #   'per_hierarchy': { 'numeric': {...}, 'taxonomic': {...} },
  #     # each: gate_decision, anchor_latent, anchor_recall_{contentflip,corpus},
  #     #       anchor_fidelity (anchor==diagnostic_parent? usurp check),
  #     #       parent_probe_recall_by_subcontext, non_triviality{passing absorbers w/
  #     #       jaccard/precision/gain+CI}, threshold_sensitivity, k_track_unit{members},
  #     #       recovered_absorber_count, baselines{g_pool,h_pool},
  #     #       sliced_recall{ s: {unit,anchor,g,h, unit_minus_g_ci, unit_minus_h_ci,
  #     #                          mcnemar_p, holm_p} }, kg_edges[...],
  #     #       kg_agreement_rate, kg_agreement_null, admission{signatureK, surface_inv}
  #   'eligible_subcontexts': {...}, 'descriptive_only': {...},
  #   'stats': {bootstrap_B, n_min:150, multiplicity:'holm/bh'},
  #   'honest_null': {... if applicable ...},
  #   'failure_modes_observed': [...], 'runtime_s': ..., 'gpu': ...
  # }
  # Also save intermediate arrays (anchor idx, unit members, attribution ranks,
  # per-subcontext recall tables) as .npz / .csv for the paper figures.
  #
  # GRADUAL SCALING (aii-long-running-tasks): (1) smoke = 10 rows, V1-V3 gates;
  # (2) mini = numeric, ONE sub-context (year) end-to-end -> anchor+gate+sliced recall;
  # (3) full numeric; (4) taxonomic. Checkpoint after each. 65k-width robustness last.
fallback_plan: |-
  GATED-MODEL ACCESS: if google/gemma-2-2b is gated and HF_TOKEN fails, load weights from the non-gated mirror unsloth/gemma-2-2b (vocab 256000, identical weights) and wrap in transformer_lens via hf_model=. If transformer_lens can't host gemma-2-2b cleanly, fall back to raw HF transformers with output_hidden_states=True and residual = hidden_states[13] (block-12 output) — but ONLY after the FVU validation (V1) confirms the layer index (FVU~0.1-0.4 correct vs ~1.0 wrong; try hidden_states[12] and [13] and keep the one the SAE reconstructs).

  TOKEN ALIGNMENT BREAKS (V2 fails): primary path re-derives target positions from char offsets (BOS-safe). If offset mapping is unreliable for some rows, fall back to stored metadata_target_token_indices + an empirically measured BOS offset (verify the tokenizer prepends exactly one <bos>; offset is +1). If a specific row still misaligns, drop it and log; keep coverage >=95% per sub-context (eligibility floor 150 has headroom). As a last resort use MEAN-pool over all non-special tokens (cruder but robust) and flag the run as pooled-not-token-localized.

  GATE FAILS ON NUMERIC: this is EXPECTED-possible (dossier WP2: absorption documented ONLY on spelling). Immediately run the identical Phases 2-3 on taxonomic_absorption (the pre-registered alternative). If taxonomic ALSO fails, that is the clean Phase-8 honest null — deliver it confidently with the uniform per-sub-context recall evidence; do NOT manufacture a positive.

  ANCHOR DEGENERACY: if argmax|C_l| picks a high-frequency polysemantic latent (fires on ~everything, low precision) instead of a true parent, the precision>=0.70 cover-set filter should exclude it; if not, restrict the anchor search to latents with corpus firing-rate < 0.5 on NEGATIVES (a parent fires on positives, not negatives) and re-pick. Report the anchor-fidelity check (anchor vs diagnostic max-encoder-cosine parent).

  NO ABSORBER CLEARS THE GAIN-CI BUT GATE-1 PASSES (parent exists, holes not specialist-filled): report 'parent present, no recoverable absorbers' — a graded null that still scopes C3; do not force a K-track unit. If the greedy proposer returns only the anchor, recovered_absorber_count=0 and the C3 claim for that hierarchy is reported negative.

  BASELINE (g)/(h) AMBIGUITY: if a full SAEBench SCR/TPP install is heavy/flaky, the mean-difference (MMD) attribution ranking specified in Phase 6 IS the faithful, self-contained SCR/TPP surrogate (latents ranked by causal/marginal relevance to the parent probe) — use it directly; note SCR/TPP are 'reference oracles not ground truth' (2605.18229). Keep N=20 for (g) and k=|unit| for (h).

  COMPUTE/MEMORY: if storing dense fp16 latents (24k x 16384) strains RAM, store JumpReLU activations as scipy CSR (they are sparse) or only keep latents that pass the content-responsive prefilter (typically << 16384). If GPU OOM on batch, drop batch size to 8 and max_length to 96. The 65k-width robustness SAE is the FIRST thing to drop if time runs short.

  STATISTICS UNDERPOWERED: every eligible sub-context already has >=150 diagnostic positives (n_min met). If paired bootstrap CIs are wide, report them honestly and lean on the aggregate (descriptive) + the binary gate decision rather than overclaiming per-sub-context significance.
testing_plan: "BUILD UP SMALL -> BIG, with hard confirmation signals at each step before scaling (aii-long-running-tasks,\
  \ aii-use-hardware):\n\n1) SMOKE (seconds, ~10 rows, no analysis): load SAE with the defensive tuple-unwrap; assert sae.W_dec.shape==[16384,2304].\
  \ Load model. Encode 10 mixed rows. CONFIRM: (V3) per-token firing L0 is in the tens-to-low-hundreds (not 0, not ~16384);\
  \ (V1) FVU at target tokens ~0.1-0.4 (proves correct layer/hook — if ~1.0 STOP and fix the layer index BEFORE anything else);\
  \ (V2) decoded target tokens string-match metadata_target_text for x_on/corpus rows (>=0.98). These three gates catch every\
  \ high-risk pipeline bug (wrong layer, BOS offset, dead/saturated SAE) up front.\n\n2) MINI END-TO-END (minutes, numeric\
  \ / sub-context='year' only): encode that slice + a sample of negatives; run Phase 2 (anchor), Phase 3 (gate on year holes),\
  \ Phase 5 (greedy), Phase 6 (sliced recall vs g/h on year). CONFIRM: an anchor latent exists with sensible recall; the pipeline\
  \ produces a numeric anchor whose top-activating contexts (logit-lens / decoded) look numeric (sanity, eyeball 3-5). This\
  \ proves the whole chain executes and the numbers are not degenerate, on a cheap slice.\n\n3) CONFIRMATION SIGNALS that\
  \ the experiment is 'working' (vs broken): (a) the anchor latent fires on a clear majority of parent-positives and rarely\
  \ on negatives (recall>=0.6, low false-positive) — if it fires on everything, anchor selection is broken; (b) the anchor's\
  \ per-sub-context recall is NOT uniform if absorption is present (some sub-contexts much lower = the holes) — uniform-high\
  \ recall is the NULL signal (legitimate, route to Phase 8); (c) marginal-attribution (g)/(h) pools are dominated by high-frequency\
  \ latents and the ranking is stable across two attribution variants (MMD vs probe-weight) — sanity that 'oracle' selection\
  \ behaves. \n\n4) FULL NUMERIC: run all phases; checkpoint method_out partial. Verify the gate decision is robust to the\
  \ threshold-sensitivity sweep (Phase 3) — the verdict shouldn't flip between Jaccard 0.05<->0.10. \n\n5) TAXONOMIC: only\
  \ after numeric is fully written out. Watch the multi-token / ambiguous-homograph flags (United States, Turkey/Georgia/Chile/Jordan)\
  \ — for multi-token countries confirm max-pool over the country's token span; for homographs, the country-positive corpus\
  \ rows were already disambiguated at build time, but spot-check 3-5.\n\n6) ROBUSTNESS (only if budget remains): re-run the\
  \ gate + sliced-recall on the 65k-width SAE; absorption should be EQUAL-OR-STRONGER at 65k (wider) — if it appears only\
  \ at 16k, note the width sensitivity. Cross-check sum-pool vs max-pool does not flip the verdict.\n\n7) FINAL: validate\
  \ method_out.json is well-formed JSON and contains the required keys (verdict, per_hierarchy gate_decision, sliced_recall\
  \ with CIs, kg_edges, honest_null-if-applicable) via the aii-json skill before finishing."
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
