# gen_art_research_1 — test_idea

> Phase: `invention_loop` · round 9 · `gen_art`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_research_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 22:27:39 UTC

````
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

<task>
Conduct thorough, unbiased research on the given topic.
Adapt your investigation approach based on the research question and domain.
</task>

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<critical_requirements>
1. SOURCE DIVERSITY - Consult MANY sources (10+), not just the first few results
2. AVOID SELECTION BIAS - Actively seek contradicting viewpoints, not just confirming ones
3. TRIANGULATE - Cross-reference claims across multiple independent sources
4. ACKNOWLEDGE UNCERTAINTY - Be honest about confidence levels and limitations
5. SYNTHESIZE - Produce a coherent answer that accounts for conflicting evidence
</critical_requirements>

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

Read and STRICTLY follow these skills: aii-web-tools.

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_9/gen_art/gen_art_research_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_9/gen_art/gen_art_research_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_9/gen_art/gen_art_research_1/file.py`, `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_9/gen_art/gen_art_research_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

<context>
<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
id: art_3zaa2xXEp8Az
type: research
title: 'CCRG iter-6: Safety-Identity Absorption & u_sub Label-Efficiency Positioning'
summary: >-
  Positions the two new load-bearing iter-6 gates of the Counterfactual Co-Response Grouping (CCRG) paper and refreshes the
  venue-locked citation set for GEN_PAPER_TEXT. Pure web research, $0 LLM spend, no code; builds on iter-4 (art_QBxBPF-9Ldxe)
  and iter-5 (art_y_5u-bfJOq3V) without re-doing settled entries. THREE deliverables. (A) M2' SAFETY-RELEVANT IDENTITY ABSORPTION:
  a cite-and-distinguish block over FIVE sub-literatures never previously surveyed -- SAE debiasing (debiaSAE 2410.13146 VLM/COLM-under-review;
  Ahsan&Wallace 2511.00177 ICLR2026 healthcare; SteerRM 2603.12795 reward-model; DeBiasLens 2602.24014 VLM/CVPR2026-flag),
  model-editing for stereotype (BiasEdit 2503.08588 TrustNLP@NAACL2025; Collapsed-LMs 2410.04472 ICLR2025), fairness/concept-erasure
  editing (Karvonen&Marks 2506.10922 NeurIPS2025 Mech-Interp-WS affine edit; SPLINCE 2506.10703 NeurIPS2025; H-SAL 2606.12088),
  identity/entity/PII unlearning (Entity-Level-Unlearning COLING2025; Not-Every-Token 2506.00876; DFSU 2601.15595), and example-reweighting
  debiasing (JTT/GEORGE/EIIL/LfF, carried). VERDICT: CCRG's three-part conjunction -- a DISCOVERED single absorber latent
  for ONE identity sub-context + a PARENT-preserving sub-context edit + scoring vs a SUB-CONTEXT-targeted dense direction
  u_sub -- is distinct from all five (each edits a WHOLE attribute/entity/example-set and preserves UNRELATED material; closest
  near-miss Ahsan&Wallace steers a single race-latent that CO-FIRES with 'incarceration' = entanglement not absorption, and
  concedes SAE steering is 'of marginal utility for realistic tasks'). Both-branches honest-null framing supplied (safety-WIN
  vs absorption-not-exhibited NULL bounded to the auditable edit primitive, connected to the existing 0/28-professions + toxicity-co-firing
  negatives). (B) M1' u_sub LABEL-EFFICIENCY: RETIRES the now-FALSE 'a single dense hyperplane structurally cannot localize
  to a sub-context / erasing the is-a-country direction removes all countries' argument -- u_sub IS a dense hyperplane and
  DOES localize, the testbed already carries its labels, and SPLINCE (preserves covariance with target label), Karvonen&Marks
  (affine edit, bias <2.5%, perf maintained) and H-SAL (label-free matches label-based) externally prove a labeled dense direction
  localizes/preserves utility. Supplies an exact DELETE/REPLACE list + BOTH M1' fork paragraphs (FORK-WIN: discovered single
  feature beats sub-context-labeled dense; FORK-MATCH: matches u_sub WITHOUT sub-context labels = label-efficiency/discovery,
  grounded in Peng 'Discover-not-Act' 2506.23845 verbatim thesis + label-free SAE 2506.01247) + an honest cost note (counterfactual-pair
  cost of grouping vs sub-context-label cost of u_sub). (C) CITATION REFRESH: 14 new grep-verified entries + carry-forward
  flags RESOLVED (Deng 2506.18141 UPGRADE->ACL2026; SAEmnesia 2509.21379 UPGRADE->ICML2026; SNCE 2509.21008 authors confirmed;
  Muchane 2506.01197 keep-preprint), BibTeX, corrections diff, unresolved-flags list, and an updated presentation-strip checklist.
  Outputs research_out.json + research_report.md (sections A-D).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_research_1
out_dependency_files:
  file_list:
  - research_out.json

--- Dependency 2 ---
id: art_IlzAiXYWeUYH
type: research
title: 'CCRG iter-7 Positioning: Gated-Dense Prior Art, Localization-First Reposition'
summary: >-
  Positions the iteration-7 CCRG paper and refreshes the venue-locked citation set for GEN_PAPER_TEXT. Pure web research,
  $0, no code; builds on iter-5 (art_y_5u-bfJOq3V) and iter-6 (art_3zaa2xXEp8Az) without re-doing settled entries. FIVE deliverables.
  (A) GATED/CONDITIONAL ACTIVATION-EDITING SURVEY (the new load-bearing piece): VERDICT = gating a dense edit by a sparse/threshold
  detector is ESTABLISHED PRIOR ART, and the exact gated-dense operator the paper uses as a control is already published,
  so DENSE-SUB-ABL-GATED is a CONTROL, not a contribution. Four verified cites: CAST (2409.05907, ICLR 2025 Spotlight; condition-vector
  switch over the prompt's hidden state, gate fit on LABELED example sets), GUARD-IT (2605.12765, preprint; Sentence-Transformer
  Similarity Gate K(x)={j:sim(c_j,phi(x))>=T} over LABELED-forget clusters + norm-preserving rotation h'=(h-a*vhat)*||h||/||h-a*vhat||),
  GSS (2602.08901, preprint; the EXACT operator h'=h-G(|u^T h|>eps)*v Eq.3 / multi-component Eq.14, probe u + steer v OPTIMIZED
  on 1,000 memorization-labeled sequences with eps tuned to the 95th percentile), SADI (2410.12299, ICLR 2025 Poster; dynamic
  per-input steering via a contrastive-pair binary mask). The PLAN MIS-ATTRIBUTED the |u^T h|>eps formula to GUARD-IT; it
  is actually GSS (corrected). In ALL prior methods the gate is SUPERVISED; the SAE-specific contribution is therefore the
  TRAINING-FREE, LABEL-FREE DISCOVERY of WHERE to gate (the precise sub-context absorber marginal-attribution drops) plus
  the absorber's calibrated JumpReLU firing as a built-in calibration-free gate, grounded in Peng 'Discover-not-Act' (2506.23845).
  BOTH M1'' fork paragraphs supplied (WIN: discovered sparse handle beats even gated dense, advantage larger on absorption
  than co-firing cases => traces to structure not footprint; MATCH: gating not SAE-specific => value=label-free discovery;
  plus fallback FORK-c near-NOOP => scope to selective partial suppression). (B) LOCALIZATION-FIRST REPOSITION: drop-in abstract
  spine + intro opener leading with training-free auditable LOCALIZATION of homograph-polysemy absorption, stating localization-NOT-classification
  up front (toxicity unit AUC 0.762 ties/loses raw latents, trails dense 0.84-0.89; sub-attrs 0.63 vs 0.93), presenting the
  44-group safety screen (2/44 = white/straight, both homographs) as the HEADLINE LIMITATION-and-finding (absorption=lexical
  polysemy not demographic semantics; Ahsan-Wallace co-firing corroborates), naming the durable contribution triad (label-free
  discovery+editable feature-KG; a-priori recall-hole diagnostic=exploratory; absorption-regime selection wins). (C) METHOD-IDENTITY
  REFRAME: foreground single-absorber discovery (anchored set-cover effectively k=1; unit-vs-single-best-absorber ablation
  art_3WXWsaSoGMnK shows single absorber WINS; M7 multi-member adds collateral), demote multi-member grouping + C-track to
  secondary, 5 retitle options. (D) CLARITY FIXES: ONE canonical Georgia number (+0.561 CI[0.318,0.811], 2nd judge +0.465
  CI[0.289,0.658]) + exact footnote for the +0.743 safety-section re-run; concept-space-KL (u_sub 0.078 < whole-parent 0.102)
  vs judged-collateral (util_SUB 1.17 < util_whole 1.33, inverts) drop-in. (E) CITATIONS: inherited locked table carried forward
  verbatim + 6 new gated-steering cites with verified IDs/venues/full author lists + new-cite BibTeX + unresolved-flags list
  + 10-item presentation-strip checklist. Outputs research_out.json + research_report.md (sections A-E).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_7/gen_art/gen_art_research_1
out_dependency_files:
  file_list:
  - research_out.json

--- Dependency 3 ---
id: art_JCYCmzJDvUm5
type: research
title: 'CCRG iter-8 Positioning: Chanin Delta, Concentration-Gate, Localization Retarget'
summary: >-
  Finalizes iteration-8 CCRG paper positioning for GEN_PAPER_TEXT, $0 web-only. (D1) States the label-free DELTA of 'anchored
  recall-hole-guided precision selection of a single absorber' vs Chanin et al.'s SUPERVISED, spelling-bound absorption diagnostic
  (2409.14507: LR probe on ground-truth first-letter labels -> max encoder-cosine parent; ablation on the first-letter logit
  + probe-projection for the absorber; absorption_rate=num_absorptions/lr_probe_true_positives) and vs a simple max-precision
  selector (empirically a TIE since wins are k=1); trims set-cover/(1-1/e) to MOTIVATION only. (D2) Grounds 'the edit win
  tracks CONCENTRATION/PRECISION, not absorption' against the feature-selection-for-steering literature: Arad/Mueller/Belinkov
  (EMNLP2025 output-score selection 2-3x), CorrSteer (correlation), FGAA (density filtering), Sparse Activation Steering (width->monosemanticity),
  Duan 2606.08365 (pre-intervention feature statistics predict collateral spread), SAE-TS (target specific feature, min side-effects),
  Anthropic Scaling Monosemanticity (specificity = sharp conditional gate); internal predictor concentration r=+0.63 vs absorption-label
  r=-0.09 vs footprint-sparsity r=-0.80. (D3) Retargets to lead with 'training-free auditable LOCALIZATION + EDITING of homograph-polysemy
  absorption' (ICLR primary per goal, ICML acceptable; ICLR2026 CfP fits), safety-homograph null (2/44) as headline limitation,
  with BOTH a wins-landed (OUTCOME-A) and base-thin (OUTCOME-B, expected) abstract+intro spine plus a selector keyed to the
  parallel M1'''/M3''' results (BEATS=0/FAIR_CLOSES=4/n_concentrated_wins=0 -> OUTCOME-B). (D4) Locks the citation set: carries
  iter-6/iter-7 venue-verified table verbatim + 7 web-verified new cites with IDs/venues/authors + BibTeX + unresolved-flags
  (CorrSteer venue conflict). (D5) 14-item presentation-strip checklist (lead +1.00 not +1.58; both forget instruments; unify
  gate operator; concentration not absorption; localization-not-classification; retract Georgia +0.561; firing-signature !=
  edit-handle). Outputs research_out.json + research_report.md (D1-D5).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_research_1
out_dependency_files:
  file_list:
  - research_out.json

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>
</context>

<artifact_plan>
id: gen_plan_research_1_idx5
type: research
title: >-
  CCRG iter-9 Positioning: Commit Localization Reposition + Label-Efficiency Both-Forks + Confinement 'So What' + Cite/Presentation
  Lock
summary: >-
  Pure web-research plan (cpu_light, $0 LLM spend) finalizing iteration-9 positioning of the CCRG paper for GEN_PAPER_TEXT.
  Four blocks: (1) commit the reposition away from 'clustering' to LABEL-FREE SINGLE-SPECIALIST LOCALIZATION with the clustering-tested-and-negative
  null stated up front and homograph-confinement as the deliberate headline (intro/abstract spine + 4-5 retitle options);
  (2) ground the M1'''' label-scarce where-to-gate demonstration with the label-efficient/few-shot-probing + active-learning-for-probing
  + steering-data-efficiency literature, producing BOTH fork framings (FORK-A label-free saves labeling cost; FORK-B fair
  gate matches at n=1 => boundary paper); (3) articulate the lexical-polysemy confinement 'so what' + label-free practitioner
  screen against the SAE-reliability/auditing literature; (4) carry the venue-locked citation table verbatim, add new cites
  with verified IDs/venues/authors (flag unresolved, do NOT invent) + BibTeX, and supply the presentation-strip checklist.
  Builds on iter-6/7/8 positioning deps so settled entries are not redone.
runpod_compute_profile: cpu_light
question: >-
  How should iteration 9 of the CCRG paper be POSITIONED for GEN_PAPER_TEXT so it is coherent whichever way the M1'''' label-scarce
  demonstration lands? Specifically: (a) how to COMMIT the reposition away from 'clustering' to LABEL-FREE SINGLE-SPECIALIST
  LOCALIZATION, stating up front that the multi-member clustering hypothesis was tested and did NOT pay off (inert 0/8 vs
  a max-precision selector; multi-member adds collateral; all three goal-named downstream tasks -- safety classification,
  steering, model-diffing -- are nulls) and reporting that null as a finding, with homograph-confinement as the deliberate
  headline scientific contribution; (b) how to GROUND the label-scarce where-to-gate demonstration in the label-efficient/few-shot-probing,
  active-learning-for-probing, and steering/gating-label-cost literature so BOTH forks are positioned (FORK-A: the label-free
  SAE absorber discovery saves the sub-context-labeling cost the fair supervised d_sub gate needs = a concrete SAE-specific
  value; FORK-B: the fair gate matches even at n=1 => no SAE-specific where-to-gate value => a clean localization + confinement-screen
  boundary paper); (c) how to articulate WHY practitioners build on a lexical-polysemy confinement finding + a shipped label-free
  SCREEN, positioned against the SAE-reliability/auditing literature; (d) which citations to carry verbatim and which new
  label-efficiency/active-learning/few-shot/SAE-reliability cites to add with verified IDs/venues/authors, plus the presentation-strip
  checklist.
research_plan: |-
  PROFILE & BUDGET. cpu_light. Pure web research via the aii-web-tools skill (web search -> web fetch -> fetch_grep); NO code, NO LLM API spend ($0). Deliverables are positioning prose + a citation table + a checklist for the downstream GEN_PAPER_TEXT writer; this artifact does NOT write the paper, run experiments, or know the M1'''' verdict (M1'''' executes in a PARALLEL experiment artifact this same iteration -- so EVERY result-dependent passage MUST be supplied in BOTH fork variants plus a selector, exactly as iter-8 [art_JCYCmzJDvUm5] supplied OUTCOME-A/OUTCOME-B spines).

  === STEP 0 -- READ PRIORS, DO NOT REDO SETTLED WORK (mandatory first action) ===
  Read, in full, the three dependency positioning artifacts BEFORE any new search, and extract what is already locked so it is carried verbatim and NOT re-derived:
    - art_JCYCmzJDvUm5 (iter-8): /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_research_1/research_out.json + research_report.md. Carry: the Chanin label-free DELTA (D1); the concentration/precision-gate grounding (D2: Arad/Mueller/Belinkov EMNLP2025, CorrSteer [venue conflict flagged], FGAA, Sparse Activation Steering, Duan 2606.08365, SAE-TS, Anthropic Scaling Monosemanticity; internal predictor concentration r=+0.63 vs absorption-label r=-0.09 vs footprint r=-0.80); the localization-retarget spine + OUTCOME-A/OUTCOME-B abstract+intro pair + the M1'''/M3''' selector (BEATS=0/FAIR_CLOSES/n_concentrated_wins=0 -> OUTCOME-B); the safety-homograph 2/44 headline-limitation framing; the locked citation table + 7 iter-8 new cites; the 14-item presentation-strip checklist.
    - art_IlzAiXYWeUYH (iter-7): /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_7/gen_art/gen_art_research_1/research_out.json + research_report.md. Carry: gated/conditional-editing PRIOR ART is established and SUPERVISED -- CAST (2409.05907, ICLR 2025 Spotlight), GUARD-IT (2605.12765), GSS (2602.08901, the |u^T h|>eps operator -- NOTE the iter-7 correction that this is GSS not GUARD-IT), SADI (2410.12299, ICLR 2025 Poster); Peng 'Discover-not-Act' (2506.23845); the localization-first reposition spine; the method-identity reframe (single-absorber discovery, set-cover effectively k=1, multi-member adds collateral); 5 retitle options; the canonical Georgia footnote.
    - art_3zaa2xXEp8Az (iter-6): /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_research_1/research_out.json + research_report.md. Carry: the u_sub LABEL-EFFICIENCY framing + Peng discover-not-act verbatim thesis + label-free SAE (2506.01247); the safety sub-literature survey (debiaSAE, Ahsan&Wallace 2511.00177, SteerRM, DeBiasLens, BiasEdit, Collapsed-LMs, Karvonen&Marks 2506.10922, SPLINCE 2506.10703, H-SAL, Entity-Level-Unlearning, etc.); the 14 venue-verified citation refresh entries + carry-forward resolutions (Deng 2506.18141->ACL2026, SAEmnesia 2509.21379->ICML2026, etc.).
  Also re-read the iter-9 hypothesis 'THE ITERATION-9 MANDATE' (M1''''-M6'''') and 'RE-DESIGNATED HEADLINE' / 'HONEST NEGATIVES' blocks in the prompt -- these are the source of truth for the claims this report must position. RULE: any entry already venue-verified in a prior dep is carried VERBATIM (ID/venue/authors), never re-searched; new web searches are ONLY for the genuinely new label-efficiency/active-learning/few-shot-probing/SAE-reliability material below.

  === STEP 1 -- BLOCK 1: COMMIT THE REPOSITION (M2''''/R1) ===
  Goal: a drop-in intro spine + abstract that the GEN_PAPER_TEXT writer can adopt, committing to LABEL-FREE SINGLE-SPECIALIST LOCALIZATION as the central object and reporting the clustering null as a finding.
    1a. Synthesis (web-light -- mostly framing, anchored in already-locked cites): write (i) an abstract spine and (ii) a 3-4 sentence intro opener that: names the central object as 'anchored recall-hole-guided PRECISION SELECTION of a single absorber latent that marginal attribution silently drops' (ONE stable name -- propose it, e.g. keep 'CCRG' as the system name but describe the object as 'recall-hole-anchored absorber localization'); states UP FRONT that the multi-member CLUSTERING hypothesis (the core prompt) was TESTED and did NOT pay off -- the set-cover/multi-member machinery is INERT vs a max-precision single-latent selector (0/8 edit cases, 3/8 returns the same latent), multi-member units only ADD collateral, and all THREE goal-named downstream tasks (safety-attribute classification, steering, model-diffing) are NULLS (no SAE unit out-classifies a dense probe; steering surgical on only 2/5 letters; model-diffing confound-bounded +0.000) -- and frames that null as a deliberate, reportable FINDING (cite 'SAEs Do Not Find Canonical Units' 2502.04878 ICLR2025, AxBench 2501.17148, DeepMind negative results, Peng 2506.23845 as the literature that PREDICTS this null); and makes the HOMOGRAPH-CONFINEMENT boundary (absorption is a lexical-polysemy phenomenon; 2/44 safety groups, 3/64 homograph entities, 0/28 professions) the deliberate HEADLINE scientific contribution. Anchor the editing-is-real-only-vs-unconditional-dense caveat to the locked gated-steering prior art (Block from iter-7). Target ICLR primary / ICML fallback (the iter-8 note that the ICLR2026 CfP fits).
    1b. Supply 4-5 RETITLE options that COMMIT to localization + screening and DROP 'clustering/grouping' from the title (distinct from the iter-7/iter-8 options -- build on but do not duplicate them). Seeds to refine: e.g. 'Where Absorption Hides: Training-Free, Label-Free Localization of Homograph-Polysemy Feature Absorption in Frozen SAEs (and a Screen to Find It)'; 'Localizing, Not Clustering: A Label-Free Procedure That Surfaces the Single Absorber Marginal Attribution Drops'; 'A Lexical-Polysemy Boundary for SAE Feature Absorption, and a Label-Free Screen for It'. Each option must encode: label-free + training-free + single-specialist localization + the confinement/screen. Mark which one is recommended and why.

  === STEP 2 -- BLOCK 2: GROUND THE LABEL-SCARCE WHERE-TO-GATE DEMONSTRATION, BOTH FORKS (M1'''') ===
  Goal: position the NEW load-bearing M1'''' experiment (quality-vs-#labels curves, n in {0,1,5,20,full}, fair supervised d_sub-gated dense gate vs the label-free SAE absorber handle, on edit AND localization quality) in the label-efficiency literature, so the paper has a literature-grounded 'discovery is the value' argument READY in BOTH fork variants.
    2a. SEARCH the new literature (run these as parallel web searches, then fetch + fetch_grep the most relevant arXiv abstract pages to verify ID/venue/authors):
       - 'label-efficient concept probing LLM few-shot linear probe'; 'sample complexity of linear probing representations'; 'how many labels to learn a concept direction language model'.
       - 'active learning for linear probes / concept detectors uncertainty sampling foundation models'.
       - 'steering vector data efficiency number of contrast pairs diff-of-means'; 'reliability of steering vectors number of examples'.
       - 'label-free vs labeled concept steering sparse autoencoder'; 'discover not act sparse autoencoders concepts'.
    2b. CANDIDATE ANCHOR PAPERS surfaced in planning (executor MUST verify each ID/venue/full-author-list via fetch_grep on the arXiv /abs/ page or the published proceedings; flag any that do not resolve, do NOT invent):
       - 'Evaluating representations by the complexity of learning low-loss predictors' (arXiv 2009.07368; epsilon-sample-complexity / Surplus Description Length / loss-data framework) -- grounds the quality-vs-#labels CURVE methodology and the 'sample complexity of a probe' vocabulary.
       - Prompt-Augmented Linear Probing (arXiv 2212.10873) -- few-shot linear probing scaling; secondary.
       - 'Convergence of Uncertainty Sampling for Active Learning' (arXiv 2110.15784) and 'Parameter-Efficient Active Learning for Foundational models' (arXiv 2406.09296, active learning + linear probing of frozen features) -- ground 'the labeled route's cost can be reduced by active learning, yet still needs labels; the label-free route needs none'.
       - 'A Unified Understanding and Evaluation of Steering Methods' (arXiv 2502.02716; ~80-100 contrast pairs needed, diff-of-means strongest) and the steering-reliability paper (search 'Analysing the Generalisation and Reliability of Steering Vectors', candidate arXiv 2407.12404 / OpenReview JZiKuvIK1t -- VERIFY) -- ground the CONCRETE labeling cost the fair supervised gate incurs (FORK-A's numerator).
       - Label-free SAE (arXiv 2506.01247) and Peng 'Use SAEs to Discover Unknown Concepts, Not to Act on Known Concepts' (arXiv 2506.23845) -- ALREADY locked from deps; carry, and make them the spine of the 'label-free discovery is the SAE-specific value' argument.
    2c. WRITE BOTH FORK FRAMINGS (each a drop-in paragraph + a one-line abstract variant), keyed to a selector the writer flips once M1'''' lands:
       - FORK-A (SAE handle HOLDS quality where the fair gate COLLAPSES at low n, CI separation): the label-free SAE absorber discovery SAVES the per-sub-context labeling cost the fair supervised d_sub gate requires (quantify against the steering-data-efficiency literature: a precise supervised gate needs ~tens-to-hundreds of sub-context labels per gate; the SAE route needs ZERO). This is the concrete, demonstrated SAE-specific WHERE-TO-GATE value, and the explicit DELTA over the established SUPERVISED gated-steering prior art (CAST/GSS/GUARD-IT/SADI). Position as the load-bearing positive.
       - FORK-B (fair gate matches even at n=1): there is NO SAE-specific where-to-gate value; the editing capability is a scoped capability over an unconditional dense projection only, and gating is prior art -- so the paper retargets FULLY to (i) auditable label-free single-specialist LOCALIZATION and (ii) the homograph-confinement screen as the deliberate contribution. This is an honest negative, publishable as a boundary paper; frame via 'discover-not-act' (acting through the handle is no better than a fair labeled dense gate). Make explicit that FORK-B does NOT sink the paper (the localization spine + the confinement screen stand alone).
       - Provide the SELECTOR rule (e.g. 'if M1'''' shows CI separation at n in {0,1,5} favoring the SAE handle on edit OR localization quality -> FORK-A; else FORK-B'), mirroring the iter-8 OUTCOME selector.

  === STEP 3 -- BLOCK 3: CONFINEMENT 'SO WHAT' + LABEL-FREE PRACTITIONER SCREEN (M3''''/R3) ===
  Goal: a discussion-ready 'why others build on this' paragraph + the screen framing, positioned against the SAE-reliability/auditing literature.
    3a. SEARCH + verify the SAE-reliability/auditing anchors (fetch_grep the /abs/ pages for ID/venue/authors):
       - SAEBench (arXiv 2503.09532; Karvonen et al.) -- the field's SAE evaluation suite, includes feature-absorption + sparse-probing metrics.
       - 'Are Sparse Autoencoder Benchmarks Reliable?' (arXiv 2605.18229) -- audits SAEBench (TPP/SCR fail multiple lenses; sae-probes k-sparse most reliable; proxy gains do not transfer) -- use to argue the field NEEDS label-free, task-grounded reliability screens like ours.
       - 'Rethinking Evaluation of Sparse Autoencoders through the Representation of Polysemous Words' (arXiv 2501.06254) -- directly grounds the LEXICAL-POLYSEMY framing: absorption-reliability is a polysemy phenomenon.
       - 'Sparse Autoencoder Features for Classifications and Transferability' (arXiv 2502.11367; ACL Anthology 2025.emnlp-main.1521) -- smaller-model SAE features predict larger-model behavior = an auditing/oversight use-case the screen serves.
       - Chanin 'A is for Absorption' (2409.14507, NeurIPS2025) and 'SAEs Do Not Find Canonical Units' (2502.04878, ICLR2025) -- ALREADY locked; carry as the absorption-reliability backdrop.
       - Templeton et al. 2024 'Scaling Monosemanticity' (Anthropic, safety-feature auditing) -- ALREADY referenced in iter-8 D2; carry for the safety-attribute-auditing framing.
    3b. WRITE the confinement 'so what' (1-2 paragraphs): (i) the empirical finding -- SAE feature-absorption reliability concern is a LEXICAL-POLYSEMY phenomenon (homograph entity tokens + first-letter spelling), NOT a demographic/semantic one; safety attributes are predominantly CO-FIRING (2/44, both homographs); 0/28 professions; 3/64 homograph entities; so practitioners AUDITING safety attributes on a frozen SAE need NOT fear absorption there. (ii) the practitioner DELIVERABLE -- a $0 label-free SCREEN (recall-hole + firing-disjoint + precision, validated against the non-circular form-free probe-plus-ablation oracle on a stratified sample) that verifies, on ANY frozen SAE, WHERE absorption can and cannot occur, with NO diagnostic probe and NO sub-context labels. (iii) the 'why build on it' -- ties to the SAE-reliability-audit gap (proxy metrics do not transfer; benchmarks unreliable) so the screen is a concrete, transferable, label-free reliability instrument; and to the coverage result (M3'''' mines a wide vocabulary and reports the fraction of N candidate polysemous tokens that are absorption-structured, with CIs). Make this the deliberate headline boundary, not an apology.

  === STEP 4 -- BLOCK 4: LOCK CITES + PRESENTATION-STRIP CHECKLIST (M6'''') ===
    4a. CITATION TABLE: reproduce the venue-verified table from iter-6/7/8 VERBATIM (carry every locked ID/venue/author exactly; do NOT re-search settled entries). Then ADD the new Block-2/Block-3 cites (label-efficiency, active-learning, few-shot probing, steering-data-efficiency/reliability, SAE-reliability/auditing, polysemy-evaluation) -- for EACH new cite, fetch_grep the arXiv /abs/ page (or ACL Anthology / OpenReview / proceedings page) to record exact arXiv ID, exact venue+year (preprint if none), and the FULL author list. Mark each as VERIFIED or UNRESOLVED-FLAGGED; NEVER invent an ID, venue, or author. Supply ready-to-paste BibTeX for all new entries. Note any venue conflicts (e.g. carry forward the iter-8 CorrSteer conflict; resolve or flag the steering-reliability OpenReview-vs-arXiv mapping).
    4b. PRESENTATION-STRIP CHECKLIST (10-14 items; build on iter-8's 14-item list, ADD the iter-9 R4/R5/R6 fixes): (i) ONE stable name for the central object; selector zoo + M-labels (M1''''/S-rec/S-prec/KG-ABL/DENSE-SUB-ABL-GATED-FAIR/MAX-PRECISION) RELEGATED to an appendix; gate operators defined ONCE in a compact table. (ii) Self-correction history -> a brief changelog/limitations note; STRIP all 'a prior version claimed...' iteration/rebuttal scaffolding. (iii) Lead EVERY section with its single takeaway sentence. (iv) R4: present 1262x selectivity strictly as a LOCALIZATION claim (the KG-named latent's edit IS localized), with a one-line cross-reference that against the FAIR gated dense control the surgical advantage DISAPPEARS (collateral 2.8e-6 vs KG 5.1e-5); DROP the whole-parent (DENSE-WHOLE-ABL) strawman from the surgical-advantage rhetoric. (v) R5: present the 22-distinct-hole/30-FDR-survivor recall-repair with a STRONGER non-eval-aligned control (or the dense-probe argmax = always the parent) + a downstream-capability test; if neither pays, TEMPER to 'repair demonstrates correct LOCALIZATION, not utility'. (vi) Carry the settled spine numbers verbatim (corrected selectivity 16k mean 1452x/median 1262x; 65k mean 722x/median 676x; cross-dictionary 65k FULL / layer-9 PARTIAL; safety 2/44; member-labeling 0.730 vs shuffle 0.096; router DEMOTED, homograph prospective Wilson includes 0.5; numeric below-gate; model-diffing confound-bounded +0.000). (vii) State the defensible lead as KG vs the STRONGEST UNGATED dense = +1.00 CI[0.79,1.21] on large (NOT the inflated +1.58-vs-footprint-gated number).

  === STEP 5 -- OUTPUTS ===
  Emit (a) research_out.json = {"answer": <comprehensive synthesis of all four blocks>, "sources": [<every URL used with title>], "follow_up_questions": [<e.g. which fork M1'''' landed; any UNRESOLVED cite IDs needing manual check; whether the M3'''' coverage number came back; whether the R5 downstream-capability control paid off>]}; and (b) research_report.md with explicit sections: (S1) committed reposition intro + abstract spine + retitle options; (S2) BOTH-FORKS label-efficiency positioning + the selector + the labeling-cost grounding; (S3) the confinement 'so what' paragraph + screen framing + coverage-result framing; (S4) the locked citation table (carried verbatim) + new-cite table with VERIFIED/UNRESOLVED flags + BibTeX; (S5) the 10-14 item presentation-strip checklist. If aii-file-size-limit applies to research_out.json, follow that skill to split.

  === FAILURE / EDGE HANDLING ===
   - If a candidate arXiv ID does not resolve or maps to a different paper, FLAG it UNRESOLVED in the cite table and pick the closest verifiable alternative via search -- never fabricate. The plan's candidate IDs are starting points, not ground truth.
   - The M1'''' verdict is UNKNOWN at research time: producing only one fork is a failure mode -- BOTH forks + the selector are mandatory.
   - Do NOT re-survey the safety sub-literature, the gated-steering prior art, or the concentration-gate literature already locked in deps -- carry them; new searches are ONLY for label-efficiency/active-learning/few-shot-probing/SAE-reliability/polysemy-evaluation material.
   - Keep $0 LLM spend (pure web research). No code execution.
explanation: >-
  WHY THIS MATTERS. Iteration 8 landed both load-bearing gates NEGATIVE (the genuinely-fair bounded-beta d_sub-gated dense
  control CLOSED the edit gap on every case, 0/8 KG-beats-both; the concentrated positive base did NOT broaden, 0 independent
  wins), and the iter-8 review exposed three publication-gating MAJORS: the goal asked for a CLUSTERING method beating single
  latents on three named downstream tasks, but the clustering machinery is inert and all three tasks are nulls (R1); the only
  surviving positive thesis ('label-free discovery of WHERE to gate is the value') has no supporting experiment (R2); and
  significance is limited by homograph-confinement with no 'why others build on it' (R3). Iteration 9 runs the make-or-break
  M1'''' label-scarce demonstration in a parallel experiment artifact, but the PAPER must be coherent whichever way M1''''
  lands -- which is exactly what this positioning artifact secures BEFORE GEN_PAPER_TEXT writes. This research artifact answers:
  how to commit the reposition to label-free single-specialist localization while honestly reporting the clustering-and-downstream-tasks
  null as a finding (R1/M2''''); how to ground the label-scarce result in the label-efficiency / few-shot-probing / active-learning
  / steering-data-efficiency literature so BOTH the FORK-A 'discovery saves the labeling cost' positive and the FORK-B 'fair
  gate matches at n=1 => boundary paper' negative are literature-grounded and ready (R2/M1''''); how to turn the lexical-polysemy
  confinement into a 'so what' + a shipped label-free practitioner screen positioned against the SAE-reliability/auditing
  gap (R3/M3''''); and how to lock the citation set verbatim from prior iterations while adding verified new cites and a presentation-strip
  checklist that fixes the R4 (selectivity-as-localization-not-surgical-advantage), R5 (stronger repair control or temper
  to localization), and R6 (strip the iteration/rebuttal log) minors. A vague positioning here forces GEN_PAPER_TEXT to improvise
  the single most contested framing in the paper; a concrete both-forks plan with verified anchors lets the writer adopt the
  correct spine the moment M1'''' resolves. Pure web research (cpu_light, $0) is the right executor: the task is literature
  synthesis + citation verification + framing, with no code, data, or computation required.
</artifact_plan>

<investigation_process>
1. DIVERGE: Brainstorm multiple angles/framings of the question before searching. Think across fields — what adjacent domains might have relevant insights?
2. SEARCH: Multiple queries per angle with different phrasings to discover the landscape
3. FETCH: Read promising URLs at high level. Snippets are NOT enough — fetch full pages
4. DETAIL: aii-web-tools fetch_grep for specifics from key pages/PDFs
5. CONTRAST: Actively try to disprove your emerging conclusions. Search with different phrasings, "[topic] criticism", "[topic] limitations". Check across fields — the same finding may exist under different names
6. SYNTHESIZE: Integrate into balanced conclusion
7. ITERATE: Expect to repeat steps 2-6 if findings are incomplete or one-sided. Don't settle on first results
8. SUMMARIZE: Output JSON must include 'title' and 'summary' fields
</investigation_process>

<output_requirements>
- Write research_out.json to your workspace with all findings
- Provide your finding as clear prose WITH NUMBERED CITATIONS
- EVERY factual claim must have a citation number in brackets: [1], [2], [1, 3], etc.
- Include BOTH supporting AND contradicting evidence
- Be explicit about confidence level and what would change it
- End with follow-up questions for further investigation
</output_requirements>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

Research everything specified in the artifact plan, but you may also investigate additional relevant aspects beyond what's listed. Investigate this question thoroughly.

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ResearchExpectedFiles": {
      "description": "All expected output files from research artifact.",
      "properties": {
        "output": {
          "description": "Path to research output JSON. Example: 'research_out.json'",
          "title": "Output",
          "type": "string"
        }
      },
      "required": [
        "output"
      ],
      "title": "ResearchExpectedFiles",
      "type": "object"
    },
    "Source": {
      "description": "A source used in the research.",
      "properties": {
        "index": {
          "description": "Citation number (1, 2, 3, ...)",
          "title": "Index",
          "type": "integer"
        },
        "url": {
          "description": "Full URL of the source",
          "title": "Url",
          "type": "string"
        },
        "title": {
          "description": "Title of the article/page",
          "title": "Title",
          "type": "string"
        },
        "summary": {
          "description": "Brief summary of what this source contributed",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "index",
        "url",
        "title",
        "summary"
      ],
      "title": "Source",
      "type": "object"
    }
  },
  "description": "Research artifact \u2014 structured output + file metadata.\n\nConducts thorough web research using the aii-web-tools skill.\nReturns structured JSON output with citations.",
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
      "$ref": "#/$defs/ResearchExpectedFiles",
      "description": "All output files you created. Must include research_out.json with your research findings."
    },
    "upload_ignore_regexes": {
      "description": "Regex patterns for workspace paths that must NOT be published to the GitHub repo, matched against each file's path relative to this artifact's workspace root (POSIX form, e.g. 'cache/abc.json'). Applied ON TOP OF the deploy step's built-in exclusions. Use this for executor-specific caches, large transient intermediates, or content-addressed blob stores (e.g. a cache/ dir of thousands of hash-named files) that would bloat the repo. Examples: ['(^|/)cache/', '(^|/)\\\\.weight_cache/', '(^|/)checkpoints/']. Leave empty if every workspace file should be published.",
      "items": {
        "type": "string"
      },
      "title": "Upload Ignore Regexes",
      "type": "array"
    },
    "answer": {
      "description": "Comprehensive answer with NUMBERED CITATIONS. Cite sources by number: 'Claim [1].' or 'According to [2, 3]...'",
      "title": "Answer",
      "type": "string"
    },
    "sources": {
      "description": "All sources used, with index matching citation numbers in answer",
      "items": {
        "$ref": "#/$defs/Source"
      },
      "title": "Sources",
      "type": "array"
    },
    "follow_up_questions": {
      "description": "2-3 follow-up questions that emerged from the investigation",
      "items": {
        "type": "string"
      },
      "title": "Follow Up Questions",
      "type": "array"
    }
  },
  "required": [
    "out_expected_files",
    "answer",
    "sources",
    "follow_up_questions"
  ],
  "title": "ResearchArtifact",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-06-18 22:27:39 UTC

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

### [3] SKILL-INPUT — aii-web-tools · 2026-06-18 22:27:51 UTC

The agent loaded the **aii-web-tools** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-web-tools
description: "Web research toolkit: web search (Serper/Google), web page fetch as markdown (HTML and PDF), and regex grep over full page/PDF text. Use whenever a task needs to search the web, read a page, mine a paper/PDF, verify citations, or extract exact quotes, numbers, or methodology from a URL."
---

## Web tools

You have three web capabilities: **search**, **fetch**, and **grep** (exact
regex extraction over a full page or PDF).

**Pick where they come from, in this order:**

1. **If you have built-in `WebSearch` / `WebFetch` tools, PREFER those over the
   scripts below.** They may be **deferred tools** (listed by name but with
   schemas not yet loaded) — if so, call `ToolSearch("select:WebSearch,WebFetch")`
   ONCE to load them, then use them normally. Do not skip them just because they
   need that one extra load step; they are the preferred path. Pair them with the
   `aii_web_tools__fetch_grep` script below when you need exact text / numbers /
   methodology that a summary would miss, or when reading a PDF.
2. **Only if you have NO built-in `WebSearch` / `WebFetch`** (e.g. the OpenHands
   backend), use the scripts in this skill (below). They are our own
   implementations — Serper.dev for search, html2text + PyMuPDF for fetch, and
   regex grep over the full document text. They work without any built-in web
   tools.

Workflow either way: **search** (discover) → **fetch** (read for the gist) →
**grep** (pull exact details / read PDFs).

---

## Running the scripts

Run every script with the skill's pre-provisioned interpreter (it already has
`requests`, `html2text`, `pymupdf`, `python-dotenv`). Set `PY` once:

```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-web-tools"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

### 1. Search the web (Serper.dev / Google)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_search.py" --query "neuro-symbolic FOL translation LLM" --max-results 10
```

Returns ranked title / URL / snippet lines. Use it first to scan the
landscape; snippets are for discovery only — fetch a page before judging it.

### 2. Fetch a page as markdown (HTML or PDF)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" fetch --url "https://arxiv.org/abs/2303.11366" --max-chars 10000
```

`--max-chars` caps output (default 10000); `--char-offset N` pages further in.
Handles PDFs transparently via PyMuPDF.

### 3. Grep a page or PDF (exact regex extraction)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" grep --url "https://arxiv.org/pdf/2303.11366" --pattern "verbal reinforcement" --max-matches 20 --context-chars 200
```

Returns only the matching sections with surrounding context — the right tool
for exact numbers, table values, methodology, or long PDFs where a summary
would lose the detail. `-i` for case-insensitive.

**Parallelize** independent searches/fetches in one turn; only sequence a
fetch after the search that produced its URL.

---

## Notes

- The scripts call our ability server. If a script prints
  `Ability service not available`, the server is down — say so rather than
  silently improvising a different search method.
- Do **not** hand-roll your own `requests`/scraping for search when these
  tools are available: Serper returns clean Google results and the fetch/grep
  scripts already handle HTML, PDFs, and encoding.
````
