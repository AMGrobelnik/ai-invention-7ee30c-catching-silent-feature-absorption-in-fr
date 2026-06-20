# gen_art_research_1 — test_idea

> Phase: `invention_loop` · round 8 · `gen_art`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_research_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 10:51:12 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_research_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_research_1/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_research_1/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_research_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/user_uploads`. Check this folder for anything relevant to your task.
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

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>
</context>

<artifact_plan>
id: gen_plan_research_1_idx4
type: research
title: >-
  CCRG iter-8 Positioning: Chanin/Max-Precision Delta, Concentration-as-Sharp-Gate, Localization+Editing Retarget, Locked
  Cites
summary: >-
  Pure web-research positioning pass (no code, $0 LLM spend, cpu_light) that finalizes the iteration-8 CCRG paper framing
  for GEN_PAPER_TEXT. Four deliverables: (D1) the precise LABEL-FREE delta of CCRG's anchored recall-hole-guided precision
  selection vs (i) Chanin's SUPERVISED absorption diagnostic and (ii) a simple max-precision selector, with the M5''' novelty-trim
  wording (set-cover/(1-1/e) demoted to MOTIVATION); (D2) a survey grounding the M3''' mechanism reframe -- the edit win is
  driven by latent CONCENTRATION/PRECISION acting as a sharper conditional gate than a footprint-matched dense projection,
  absorption being only ONE label-free source of concentration -- positioned against the feature-selection-for-steering literature
  so 'concentration not absorption' is grounded, not asserted; (D3) the M2''' retarget decision + BOTH retargeted abstract/intro
  spines (>=4 concentrated wins landed vs base-stays-thin), leading with 'training-free auditable LOCALIZATION + EDITING of
  homograph-polysemy absorption', safety-homograph null as headline limitation, with verified venue-area fit (ICLR primary
  per goal, ICML acceptable); (D4) the locked citation table carried verbatim from iter-6/iter-7 + new concentration/precision-steering
  cites with verified IDs/venues/authors + BibTeX + unresolved flags + a presentation-strip checklist. Builds on iter-7 art_IlzAiXYWeUYH
  (gated-steering prior art + localization-first reposition) and iter-6 art_3zaa2xXEp8Az (safety/u_sub positioning); does
  NOT redo those settled surveys.
runpod_compute_profile: cpu_light
question: >-
  For the iteration-8 CCRG paper (GEN_PAPER_TEXT), how should the positioning be finalized so that (1) the method's novelty
  is honestly trimmed to 'anchored recall-hole-guided PRECISION SELECTION of a single absorber' with a precise stated delta
  vs Chanin's supervised absorption diagnostic AND vs a simple max-precision selector (set-cover/(1-1/e) demoted to motivation
  only); (2) the mechanism reframe 'the edit win tracks latent CONCENTRATION/PRECISION, not absorption structure' is POSITIONED
  against prior work relating per-feature precision/sparsity/selectivity to steering surgicality/conditional-gate sharpness;
  (3) the paper is retargeted to lead with training-free auditable LOCALIZATION + EDITING of homograph-polysemy absorption
  (ICLR primary, ICML acceptable), with both a wins-landed and a base-thin abstract/intro spine and the safety-homograph-confinement
  null as the headline limitation; and (4) the full citation set is locked (carry iter-6/iter-7 verbatim, add verified concentration/precision-steering
  cites, flag unresolved, invent nothing)?
research_plan: |-
  PURE WEB RESEARCH via the aii-web-tools skill (search -> fetch -> fetch_grep). NO code, NO datasets, NO experiments. $0 LLM/OpenRouter spend. Compute: cpu_light. Wall-clock budget ~3h. Output TWO files in the artifact workspace: research_out.json {title, summary, answer, sources[], follow_up_questions[]} and research_report.md (sections D1-D5). This pass FINALIZES positioning for GEN_PAPER_TEXT; it is a sibling/successor of iter-7 art_IlzAiXYWeUYH and iter-6 art_3zaa2xXEp8Az -- READ THOSE FIRST and CARRY THEIR SETTLED ENTRIES VERBATIM (do NOT re-survey gated-steering prior art or safety/u_sub positioning, which are settled). Both dependency research_out.json files are available; their locked-cite tables and abstract spines are the starting point.

  ========== STEP 0 -- GROUND IN THE DEPENDENCIES (no new searches; ~15 min) ==========
  Read the two dependency outputs already in this run:
    - iter-7 art_IlzAiXYWeUYH: /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_7/gen_art/gen_art_research_1/research_out.json (+ research_report.md). Extract: (a) the LOCKED gated-steering cites (CAST 2409.05907 ICLR2025-Spotlight; GUARD-IT 2605.12765 preprint; GSS 2602.08901 preprint = exact h'=h-G(|u^T h|>eps)v operator; SADI 2410.12299 ICLR2025-Poster; PID-Steering 2510.04309 preprint; DAC 2406.17563 preprint), all SUPERVISED-gate => gating is PRIOR ART, SAE value = label-free DISCOVERY of WHERE to gate; (b) the localization-first abstract spine + intro opener; (c) the full carried-forward locked-cite table listed in section (E); (d) Peng 'Discover-not-Act' 2506.23845 framing.
    - iter-6 art_3zaa2xXEp8Az: same dir under iter_6. Extract the safety-absorption cite-and-distinguish block + the u_sub label-efficiency positioning + the locked-cite refresh (14 entries). These are SETTLED -- carry, do not redo.
  Also anchor the load-bearing NUMBERS from the hypothesis (do NOT invent or alter; keep consistent across the report): large KG-vs-STRONGEST-ungated-dense (DENSE-SUB-ABL) = +1.00 CI[0.79,1.21] (the LEAD edit number); large KG-vs-footprint-GATED-dense = +1.58 CI[1.36,1.79] (the INFLATED/caveated robustness number -- gate driven to beta~2.97 over-erasure, gated collateral 0.290 vs its own ungated 0.021, ~14x more); Amazon = +0.75 CI[0.41,1.08] (named-entity homograph win, absorber 6846 max_kg 1.14); Bush = KG_MATCHES_GATED (parity), Cook structured; insult 13367 = +0.47 CO-FIRING win found by max-AUC NOT set-cover (the concentration-not-absorption evidence); Georgia 16009 / Jordan 540 = NO_MEANINGFUL_FORGET (distributed sense, max_kg 0.064/0.114, NOOP-identical 89%); safety 2/44 (white, straight; both homographs); named-entity 3/5 (Amazon/Bush/Cook); professions 0/28; homograph entities 3/64 (months only); selectivity corrected 722x/676x (16k/65k comparably surgical); cross-dictionary 65k full / layer-9 partial; the NEW fair control = DENSE-SUB-ABL-GATED-FAIR (u_sub gated by the precise d_sub detector AUC~1.0, bounded beta<=1).

  ========== STEP 1 -- DELIVERABLE D1: CHANIN-DELTA + MAX-PRECISION DELTA (M5''' novelty trim) ==========
  GOAL: write the precise paragraph stating what the LABEL-FREE anchor + recall-hole + precision-gate buys over (i) running Chanin's diagnostic directly and (ii) a simple max-precision selector; and supply the trim wording (set-cover/(1-1/e) = MOTIVATION only; method identity = 'anchored recall-hole-guided PRECISION SELECTION of a single absorber').
  SEARCH/FETCH:
    1a. fetch_grep the Chanin 2409.14507 FULL TEXT (try https://arxiv.org/html/2409.14507v3 first; fallback OpenReview PDF https://openreview.net/pdf/5fa0d903675ab0ae5df67d598ecfe21ce2dff8f7.pdf). Grep for: 'absorption fraction', 'absorption_fraction', 'probe', 'logistic regression', 'projection', 'ablation', 'first letter', 'main latent', 'encoder cosine', 'mean absorption'. EXTRACT precisely: (a) HOW the parent/main latent is identified -- confirm it uses a SUPERVISED logistic-regression probe (max encoder-cosine with the LR probe direction); (b) HOW the absorbing latent is identified -- ablation effect on a TASK-SPECIFIC logit (the first-letter logit) after projecting out the probe direction; (c) the absorption-fraction metric definition. CONFIRM the diagnostic REQUIRES (i) a supervised probe and (ii) a task label/logit, and that the empirical demonstration is almost entirely first-letter spelling (running example 'short'/'starts-with-S').
    1b. State the DELTA vs Chanin (label-free): CCRG's anchor is chosen by content-response RECALL on counterfactual pairs (available to every baseline, NO probe); the recall-hole is the parent's uncovered counterfactual pairs (NO logit); the precision-gate is firing-precision on the target sub-context (NO label beyond the counterfactual partition). Chanin DETECTS absorption on an individually-named latent GIVEN a supervised probe+logit; it does NOT propose parent+absorber as a usable, editable handle WITHOUT supervision, and is form-bound to spelling in its demonstrations. CCRG uses the FORM-FREE probe+ablation diagnostic ONLY to SCORE already-formed KG edges (non-circular), never to FORM units. So the buy is: training-free, label-free, form-free SURFACING of the precise sub-context latent that marginal-attribution selection silently drops.
    1c. MAX-PRECISION delta: the open question the iter-8 EXPERIMENT answers is whether the anchored recall-hole-guided set-cover beats a simple 'pick the single most precise latent firing on the target sub-context' (max-precision / S-prec) selector. Because every reported edit win is effectively k=1, the LIKELY answer is a TIE. Supply TWO conditional wordings: (TIE) trim to 'anchored recall-hole-guided PRECISION SELECTION of a single absorber'; present set-cover/(1-1/e) as MOTIVATION for the disjoint-support coverage view only, NOT a load-bearing guarantee; the discovery step's value over max-precision is the RECALL-HOLE ANCHORING that tells you WHICH sub-context to select a precise latent FOR (max-precision alone needs the sub-context handed to it). (SET-COVER ADDS SOMETHING) if any case shows k>1 or the recall-hole objective measurably helps, keep the set-cover framing but still demote (1-1/e) to motivation. Make clear GEN_PAPER_TEXT picks the wording matching the experiment's M3''' result.
    1d. Briefly search 'precision-weighted SAE latent selection' / 'recall-based vs precision-based SAE feature selection' / 'max-precision latent baseline steering' to confirm no existing named method already IS 'anchored recall-hole precision selection' (defensive novelty check); record near-misses (FGAA relevance/density filtering; CorrSteer correlation selection; Arad output-score filtering -- see D2) and state the delta (those select for steering EFFECT or correlation, not for the recall-hole an absorbed parent leaves).
  WRITE: research_report.md section D1 = the Chanin-and-max-precision delta paragraph (drop-in for the Related Work / Method-identity subsection), plus the two conditional trim sentences.

  ========== STEP 2 -- DELIVERABLE D2: CONCENTRATION-AS-SHARP-GATE (M3''' mechanism reframe grounding) ==========
  GOAL: ground the claim 'the edit advantage is a property of a PRECISE/CONCENTRATED latent acting as a SHARPER conditional gate than a footprint-matched dense projection; absorption is ONE label-free-discoverable source of concentration, not the cause of the win' against prior work relating per-feature precision/sparsity/selectivity to steering surgicality. This makes 'concentration not absorption' POSITIONED, not merely asserted.
  VERIFIED ANCHOR CITES (confirm IDs/venues/authors via fetch_grep of arXiv Comments; flag if unresolved):
    2a. Arad, Mueller, Belinkov -- 'SAEs Are Good for Steering -- If You Select the Right Features' (arXiv 2505.20063; verify EMNLP 2025). KEY: introduces input vs OUTPUT scores; filtering OUT low-output-score features gives 2-3x steering improvement => the right FEATURE SELECTION (a precise, output-effective feature), not the steering mechanism, drives steering quality. This is the HEADLINE cite for 'which precise latent you pick is what matters' -- directly supports CCRG's 'label-free discovery of WHERE to gate' and the concentration reframe.
    2b. CorrSteer -- 'Generation-Time LLM Steering via Correlated Sparse Autoencoder Features' (arXiv 2508.12535; Cho, Wu, Koshiyama; Comments say ICML 2026 -- FLAG/verify, cite preprint if unresolved). Correlation-based selection extracts 'more relevant features, thereby reducing spurious correlations' => precise/specific selection reduces collateral.
    2c. FGAA -- 'Steering LLMs with Feature Guided Activation Additions' (arXiv 2501.09929; verify authors/venue). Relevance + density/'concreteness' filtering: high-DENSITY (frequently-firing) features dominate despite limited task specificity and must be filtered out => low-density + high-precision = concentration = a clean handle. Directly supports the concentration axis (sparse firing + high per-sub-context precision).
    2d. Sparse Activation Steering -- 'Steering Large Language Model Activations in Sparse Spaces' (arXiv 2503.00177; verify). Scaling SAE width increases steering-vector sparsity/monosemanticity => 'better disentangle features by reducing overlap', improving intervention precision => sparser/more-concentrated => sharper gate.
    2e. Anthropic 'Scaling Monosemanticity' (Templeton et al. 2024, transformer-circuits.pub; cite as the canonical monosemanticity source). The precise-boundary claim: monosemantic features 'stop responding the moment text diverges from the target concept' -> a precise feature's firing IS a sharp conditional gate. Use to ground the conditional-gate-sharpness intuition.
    2f. Tie to the LOCKED iter-7 gating cites (CAST/GSS/GUARD-IT/SADI): the gating MECHANISM is prior art and supervised; a concentrated latent's calibrated JumpReLU firing is itself a sharp, threshold-free conditional gate, whereas a footprint-matched DENSE projection must be driven to beta~3 over-erasure to match the same forget (=> ~14x more collateral on 'large'). So the edit advantage = sharper conditioning from a concentrated detector, NOT absorption per se.
  SEARCH (to find any stronger/more-direct cite and avoid missing an obvious one): 'feature selectivity predicts steering side effects', 'sparse precise feature cleaner edit handle lower collateral', 'per-feature specificity steering fluency tradeoff', 'conditional steering reduces collateral selective feature'. Record 1-2 best additional hits with verified IDs.
  WRITE: research_report.md section D2 = the concentration-as-sharp-gate positioning paragraph(s): (i) state the property the method should select for = per-sub-context PRECISION x sparse firing = CONCENTRATION; (ii) cite 2a-2e that selection of a precise/specific/low-density feature is the established driver of clean steering; (iii) state that absorption is one label-free-discoverable source of concentration (absorber marginal-attribution drops) but a concentrated CO-FIRING latent (insult, found by max-AUC not set-cover) also wins, so the win predictor is concentration; (iv) explicitly DROP/heavily-qualify 'the win traces to the absorption structure the method discovers'.

  ========== STEP 3 -- DELIVERABLE D3: RETARGET/VENUE + BOTH ABSTRACT/INTRO SPINES (M2''' retarget) ==========
  GOAL: decide and justify leading the paper with 'training-free auditable LOCALIZATION + EDITING of homograph-polysemy absorption', confirm venue-area fit, and supply BOTH spines.
    3a. VENUE FIT: confirm via iclr.cc/Conferences/2026/CallForPapers and icml.cc/Conferences/2026/CallForPapers that the framing fits. NOTE the GOAL says 'Target ICLR primary, ICML fallback' while THIS artifact-direction says 'ICML primary acceptable, ICLR fallback' -- TREAT THE GOAL AS AUTHORITATIVE (ICLR primary) but explicitly state fit for BOTH and resolve the tension in-report. ICLR 2026 lists 'Interpretability, fairness, privacy, and ethical AI' as an area (fits). NOTE ICML 2026 main-track submission closed ~Jan 28 2026 (so the live cycle for a mid-2026 paper is ICLR 2026 / the next ICML); the deliverable is AREA fit, not a deadline. Map the contribution to the reviewer-evaluable areas named in the goal (clustering methods, feature selection, classification, knowledge graphs, knowledge extraction, applied knowledge discovery, text data analytics, LLMs/deep learning) -- the localization + editable feature-KG + label-free discovery framing fits these far better than a classification-win framing (the paper makes NO out-classifies-dense claim). State this mapping explicitly so the title/abstract commit to localization+editing, not classification/steering wins.
    3b. RETARGET DECISION: lead with auditable LOCALIZATION (+ EDITING on concentrated features) of homograph-polysemy absorption; safety-homograph-confinement null (2/44, both homographs) as the HEADLINE LIMITATION-and-finding; the concentrated-feature edit (large +1.00, Amazon +0.75) as a SCOPED capability bounded by the fair gated control; classification SUPPORTING/within-SAE; router DEMOTED to exploratory. Build directly on the iter-7 localization-first spine (carry it, then update for: de-inflation to +1.00-lead; the new fair bounded-beta d_sub control; concentration-not-absorption mechanism; set-cover-as-motivation; both forget instruments; unified gate operator).
    3c. SUPPLY BOTH SPINES (drop-in abstract ~150-220 words + intro opener ~1 para each):
       - OUTCOME A (>=4 independent concentrated wins LANDED: large, Amazon + Bush/Cook/wider-vocab under the fair bounded-beta d_sub-gated control): the sparse-gated EDIT is a broader load-bearing capability. Abstract foregrounds: training-free label-free localization of homograph-polysemy absorption + an editable feature-KG; the edit win LED by KG-vs-STRONGEST-dense (+1.00 on large; never lead with +1.58) on >=4 concentrated features, shown to track CONCENTRATION (max-precision ablation) and to beat the genuinely-fair bounded-beta d_sub-gated dense control; safety null as capping scope.
       - OUTCOME B (base STAYS THIN, n~=2; or the fair gated control MATCHES KG): lead FULLY with the auditability/localization SPINE + the safety-homograph-confinement NULL as the finding; the edit is a scoped capability on concentrated features; if fair-gated matches => contribution = label-free DISCOVERY of where to gate (gating is prior art); concentration-not-absorption reframe central; set-cover = motivation only.
       Each spine must: state localization-NOT-classification up front; name the durable contribution triad (label-free discovery + editable feature-KG; recall-hole screening diagnostic = exploratory; absorption-regime/concentration selection wins where the signature holds); headline the homograph-confined safety null; and avoid the inflated +1.58-vs-footprint-gated number as the lead.
  WRITE: research_report.md section D3 = venue-fit justification + retarget decision + BOTH abstract+intro spines, clearly labeled OUTCOME-A and OUTCOME-B with a one-line selector telling GEN_PAPER_TEXT which to use based on the M1'''/M2''' experiment results.

  ========== STEP 4 -- DELIVERABLE D4: CITATION FINALIZATION + D5: PRESENTATION-STRIP CHECKLIST ==========
    4a. CARRY FORWARD the FULL locked-cite table from iter-7 section (E) + iter-6, VERBATIM (Chanin 2409.14507 NeurIPS2025; Feature-Hedging 2505.11756; AxBench 2501.17148 ICML2025; SAEBench 2503.09532 ICML2025; CanonicalUnits 2502.04878 ICLR2025; Matryoshka 2503.17547 ICML2025; Farrell 2410.19278 NeurIPS2024-Safe-GenAI-WS; SPLINCE 2506.10703 NeurIPS2025; Karvonen-Marks 2506.10922 NeurIPS2025-MechInterp-WS; Ahsan-Wallace 2511.00177 ICLR2026; BiasEdit 2503.08588 TrustNLP@NAACL2025; Collapsed-LMs 2410.04472 ICLR2025; Entity-Level-Unlearning COLING2025; Deng 2506.18141 ACL2026; SAEmnesia 2509.21379 ICML2026; Peng 2506.23845; CRISP 2508.13650 ACL2026; SAUCE 2503.14530 WITHDRAWN/ICCV2025-CVF; SSPU 2505.24428 EMNLP2025; LEACE 2306.03819 NeurIPS2023; CAST 2409.05907 ICLR2025-Spotlight; GUARD-IT 2605.12765 preprint; GSS 2602.08901 preprint; SADI 2410.12299 ICLR2025-Poster; PID-Steering 2510.04309 preprint; DAC 2406.17563 preprint; the iter-6 debiasing set; JTT/GEORGE/EIIL/LfF; DiffCoEx/WGCNA; Nemhauser-Wolsey-Fisher/Feige set-cover; CDLC 2505.07073; Veitch 2106.00545; Kaushik CAD ICLR2020; CEBaB 2205.14140; ParaDetox). Do NOT re-verify settled locks; just list them with their locked venues and flag the ones the dependencies already flagged unresolved (GUARD-IT/GSS/DAC venues; DeBiasLens CVPR2026; Deng dual-listing; Karvonen-Marks workshop).
    4b. ADD the NEW concentration/precision-steering cites, each with fetch_grep-VERIFIED arXiv ID + Comments-field venue + FULL author list: Arad-Mueller-Belinkov 2505.20063 (verify EMNLP2025); CorrSteer 2508.12535 Cho-Wu-Koshiyama (Comments=ICML2026, FLAG); FGAA 2501.09929; Sparse-Activation-Steering 2503.00177; Anthropic Scaling-Monosemanticity (Templeton et al. 2024, transformer-circuits.pub -- cite by URL, no arXiv). For any venue not grep-confirmable from the Comments field, cite as PREPRINT and add to the unresolved-flags list. INVENT NOTHING.
    4c. EMIT BibTeX for every NEW cite added this iteration (the concentration set); carry the iter-6/iter-7 BibTeX by reference (note GEN_PAPER_TEXT already has it).
    4d. PRESENTATION-STRIP CHECKLIST (research_report.md section D5), 10-12 items: (1) lead title/abstract with 'training-free auditable LOCALIZATION (+ EDITING) of homograph-polysemy absorption'; (2) lead the edit table with KG-vs-STRONGEST-ungated-dense (+1.00 on large) -- caveat the +1.58-vs-footprint-gated number with the beta~2.97 over-erasure note (gated collateral 0.290 vs its own ungated 0.021); (3) report BOTH forget instruments (completion-drop AND sub-probe-drop) side by side and match operators on a BEHAVIORAL measure, not next-token KL; (4) UNIFY the gate operator into ONE definition across large/Amazon/Bush (or document the per-case clamp in-table: 3%-global-footprint vs 95%-X-rate); (5) present set-cover/(1-1/e) as MOTIVATION only; method identity = 'anchored recall-hole-guided precision selection of a single absorber'; (6) state the mechanism as CONCENTRATION/PRECISION not absorption (insult co-fires yet wins; Georgia/Jordan absorb yet lose); (7) safety-homograph null (2/44) = headline limitation; (8) state localization-NOT-classification (no SAE unit out-classifies a dense probe on any task); (9) router = exploratory (out-of-sample Wilson includes 0.5); (10) corrected selectivity (722x/676x; 16k/65k comparably surgical), cross-dictionary 65k full/layer-9 partial; (11) demote multi-member grouping + C-track to secondary (single absorber wins, multi-member adds collateral); (12) STRIP all iteration/rebuttal/infra scaffolding (M1''/M1'''/art_ tags/'iter-7 reviewer'/GPU-hours).

  ========== STEP 5 -- ASSEMBLE OUTPUTS ==========
  Write research_out.json with: title; summary; answer (a tight synthesis of D1-D5 with the key verdicts: method-identity = anchored recall-hole precision selection / set-cover=motivation; mechanism = concentration not absorption, positioned via 2505.20063/CorrSteer/FGAA/SAS/monosemanticity; retarget = localization+editing lead with both spines; cites locked); sources[] (every fetched URL with a one-line evidence note: Chanin body, the 4-5 concentration cites with verified venue/authors, ICLR/ICML CfP pages, plus the carried iter-6/iter-7 anchors by reference); follow_up_questions[] (e.g.: did M3''' show set-cover beats or ties max-precision? did M2''' land >=4 wins -> use OUTCOME-A or OUTCOME-B spine? did M1''' fair bounded-beta d_sub-gated control get beaten or matched? are the CorrSteer/Arad venues confirmable before camera-ready?). Write research_report.md with sections D1-D5 as specified, including all drop-in paragraphs, both spines, the locked+new cite table, BibTeX for new cites, unresolved-flags list, and the presentation-strip checklist.

  ========== CONTINGENCIES / FAILURE MODES ==========
  - If the Chanin HTML body is inaccessible, use the OpenReview PDF (fetch_grep) or the NeurIPS 2025 poster page; the supervised-probe + first-letter-logit + absorption-fraction facts are already corroborated by search snippets -- confirm and cite, do not block.
  - If a new concentration cite's venue is not grep-confirmable from the Comments field, cite as preprint + add to unresolved flags (NEVER invent a venue). CorrSteer's 'ICML 2026' is from Comments -> keep but flag (large 45-page preprint, may be a workshop/under-review listing).
  - If the concentration-steering literature turns out thinner than expected, fall back to the strongest anchors (Arad 2505.20063 + the locked CAST/GSS + Anthropic monosemanticity precise-boundary claim) -- these alone ground the reframe; do not pad with weak cites.
  - If venue CfP pages are unreachable, rely on the known areas (ICLR 'Interpretability, fairness, privacy, ethical AI'; reviewer-evaluable areas in the goal) and proceed; venue choice is ICLR-primary per the goal regardless.
  - Keep ALL load-bearing numbers consistent with the hypothesis; if a number is needed that is not in the hypothesis, mark it [VERIFY-AT-WRITE] rather than inventing.
  - Strictly $0 LLM spend (web research only); no OpenRouter calls.
explanation: >-
  This research artifact finalizes the iteration-8 CCRG paper positioning so GEN_PAPER_TEXT can write a defensible draft regardless
  of how the parallel iter-8 experiments (M1''' fair gated control, M2''' expanded base, M3''' max-precision ablation) land.
  The iter-7 reviewer raised three publication-gating majors that are framing/positioning problems this artifact must resolve:
  (R6/M5''') the set-cover/(1-1/e) framing oversells a step that is effectively k=1, so the novelty must be trimmed to 'anchored
  recall-hole-guided precision selection' with a precise stated delta vs Chanin's SUPERVISED diagnostic and vs a simple max-precision
  selector; (R3/M3''') the claim 'the win traces to absorption structure' is unsupported because a concentrated CO-FIRING
  latent also wins, so the mechanism must be reframed to latent CONCENTRATION/PRECISION and POSITIONED against the established
  feature-selection-for-steering literature (where selecting a precise/specific/low-density feature is the known driver of
  clean steering); (R2/M2''') the positive edit base is n~=2, so the paper must retarget to lead with auditable localization+editing
  of homograph-polysemy absorption with the safety-homograph null as the headline limitation, and needs both a wins-landed
  and a base-thin abstract/intro spine ready. The artifact also locks the citation set (carrying the iter-6/iter-7 venue-verified
  table verbatim and adding verified concentration/precision-steering cites) and supplies a presentation-strip checklist.
  Without this positioning pass the paper would lead with the inflated +1.58 number, an oversold set-cover guarantee, and
  an unsupported absorption-causation claim -- exactly the three things the reviewer flagged as blocking. Pure web research
  is the right tool: every deliverable is literature synthesis, delta articulation, venue-area mapping, and citation verification
  -- no computation, and it must run in parallel with the experiments so its both-outcome wording is ready for GEN_PAPER_TEXT.
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

### [2] HUMAN-USER prompt · 2026-06-18 10:51:12 UTC

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

### [3] SKILL-INPUT — aii-web-tools · 2026-06-18 10:51:22 UTC

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

### [4] SYSTEM-USER prompt · 2026-06-18 19:51:21 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_research_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_research_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_research_1/file.py`, `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_research_1/results/out.json`
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
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_6/gen_art/gen_art_research_1
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
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_7/gen_art/gen_art_research_1
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
id: gen_plan_research_1_idx4
type: research
title: >-
  CCRG iter-8 Positioning: Chanin/Max-Precision Delta, Concentration-as-Sharp-Gate, Localization+Editing Retarget, Locked
  Cites
summary: >-
  Pure web-research positioning pass (no code, $0 LLM spend, cpu_light) that finalizes the iteration-8 CCRG paper framing
  for GEN_PAPER_TEXT. Four deliverables: (D1) the precise LABEL-FREE delta of CCRG's anchored recall-hole-guided precision
  selection vs (i) Chanin's SUPERVISED absorption diagnostic and (ii) a simple max-precision selector, with the M5''' novelty-trim
  wording (set-cover/(1-1/e) demoted to MOTIVATION); (D2) a survey grounding the M3''' mechanism reframe -- the edit win is
  driven by latent CONCENTRATION/PRECISION acting as a sharper conditional gate than a footprint-matched dense projection,
  absorption being only ONE label-free source of concentration -- positioned against the feature-selection-for-steering literature
  so 'concentration not absorption' is grounded, not asserted; (D3) the M2''' retarget decision + BOTH retargeted abstract/intro
  spines (>=4 concentrated wins landed vs base-stays-thin), leading with 'training-free auditable LOCALIZATION + EDITING of
  homograph-polysemy absorption', safety-homograph null as headline limitation, with verified venue-area fit (ICLR primary
  per goal, ICML acceptable); (D4) the locked citation table carried verbatim from iter-6/iter-7 + new concentration/precision-steering
  cites with verified IDs/venues/authors + BibTeX + unresolved flags + a presentation-strip checklist. Builds on iter-7 art_IlzAiXYWeUYH
  (gated-steering prior art + localization-first reposition) and iter-6 art_3zaa2xXEp8Az (safety/u_sub positioning); does
  NOT redo those settled surveys.
runpod_compute_profile: cpu_light
question: >-
  For the iteration-8 CCRG paper (GEN_PAPER_TEXT), how should the positioning be finalized so that (1) the method's novelty
  is honestly trimmed to 'anchored recall-hole-guided PRECISION SELECTION of a single absorber' with a precise stated delta
  vs Chanin's supervised absorption diagnostic AND vs a simple max-precision selector (set-cover/(1-1/e) demoted to motivation
  only); (2) the mechanism reframe 'the edit win tracks latent CONCENTRATION/PRECISION, not absorption structure' is POSITIONED
  against prior work relating per-feature precision/sparsity/selectivity to steering surgicality/conditional-gate sharpness;
  (3) the paper is retargeted to lead with training-free auditable LOCALIZATION + EDITING of homograph-polysemy absorption
  (ICLR primary, ICML acceptable), with both a wins-landed and a base-thin abstract/intro spine and the safety-homograph-confinement
  null as the headline limitation; and (4) the full citation set is locked (carry iter-6/iter-7 verbatim, add verified concentration/precision-steering
  cites, flag unresolved, invent nothing)?
research_plan: |-
  PURE WEB RESEARCH via the aii-web-tools skill (search -> fetch -> fetch_grep). NO code, NO datasets, NO experiments. $0 LLM/OpenRouter spend. Compute: cpu_light. Wall-clock budget ~3h. Output TWO files in the artifact workspace: research_out.json {title, summary, answer, sources[], follow_up_questions[]} and research_report.md (sections D1-D5). This pass FINALIZES positioning for GEN_PAPER_TEXT; it is a sibling/successor of iter-7 art_IlzAiXYWeUYH and iter-6 art_3zaa2xXEp8Az -- READ THOSE FIRST and CARRY THEIR SETTLED ENTRIES VERBATIM (do NOT re-survey gated-steering prior art or safety/u_sub positioning, which are settled). Both dependency research_out.json files are available; their locked-cite tables and abstract spines are the starting point.

  ========== STEP 0 -- GROUND IN THE DEPENDENCIES (no new searches; ~15 min) ==========
  Read the two dependency outputs already in this run:
    - iter-7 art_IlzAiXYWeUYH: /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_7/gen_art/gen_art_research_1/research_out.json (+ research_report.md). Extract: (a) the LOCKED gated-steering cites (CAST 2409.05907 ICLR2025-Spotlight; GUARD-IT 2605.12765 preprint; GSS 2602.08901 preprint = exact h'=h-G(|u^T h|>eps)v operator; SADI 2410.12299 ICLR2025-Poster; PID-Steering 2510.04309 preprint; DAC 2406.17563 preprint), all SUPERVISED-gate => gating is PRIOR ART, SAE value = label-free DISCOVERY of WHERE to gate; (b) the localization-first abstract spine + intro opener; (c) the full carried-forward locked-cite table listed in section (E); (d) Peng 'Discover-not-Act' 2506.23845 framing.
    - iter-6 art_3zaa2xXEp8Az: same dir under iter_6. Extract the safety-absorption cite-and-distinguish block + the u_sub label-efficiency positioning + the locked-cite refresh (14 entries). These are SETTLED -- carry, do not redo.
  Also anchor the load-bearing NUMBERS from the hypothesis (do NOT invent or alter; keep consistent across the report): large KG-vs-STRONGEST-ungated-dense (DENSE-SUB-ABL) = +1.00 CI[0.79,1.21] (the LEAD edit number); large KG-vs-footprint-GATED-dense = +1.58 CI[1.36,1.79] (the INFLATED/caveated robustness number -- gate driven to beta~2.97 over-erasure, gated collateral 0.290 vs its own ungated 0.021, ~14x more); Amazon = +0.75 CI[0.41,1.08] (named-entity homograph win, absorber 6846 max_kg 1.14); Bush = KG_MATCHES_GATED (parity), Cook structured; insult 13367 = +0.47 CO-FIRING win found by max-AUC NOT set-cover (the concentration-not-absorption evidence); Georgia 16009 / Jordan 540 = NO_MEANINGFUL_FORGET (distributed sense, max_kg 0.064/0.114, NOOP-identical 89%); safety 2/44 (white, straight; both homographs); named-entity 3/5 (Amazon/Bush/Cook); professions 0/28; homograph entities 3/64 (months only); selectivity corrected 722x/676x (16k/65k comparably surgical); cross-dictionary 65k full / layer-9 partial; the NEW fair control = DENSE-SUB-ABL-GATED-FAIR (u_sub gated by the precise d_sub detector AUC~1.0, bounded beta<=1).

  ========== STEP 1 -- DELIVERABLE D1: CHANIN-DELTA + MAX-PRECISION DELTA (M5''' novelty trim) ==========
  GOAL: write the precise paragraph stating what the LABEL-FREE anchor + recall-hole + precision-gate buys over (i) running Chanin's diagnostic directly and (ii) a simple max-precision selector; and supply the trim wording (set-cover/(1-1/e) = MOTIVATION only; method identity = 'anchored recall-hole-guided PRECISION SELECTION of a single absorber').
  SEARCH/FETCH:
    1a. fetch_grep the Chanin 2409.14507 FULL TEXT (try https://arxiv.org/html/2409.14507v3 first; fallback OpenReview PDF https://openreview.net/pdf/5fa0d903675ab0ae5df67d598ecfe21ce2dff8f7.pdf). Grep for: 'absorption fraction', 'absorption_fraction', 'probe', 'logistic regression', 'projection', 'ablation', 'first letter', 'main latent', 'encoder cosine', 'mean absorption'. EXTRACT precisely: (a) HOW the parent/main latent is identified -- confirm it uses a SUPERVISED logistic-regression probe (max encoder-cosine with the LR probe direction); (b) HOW the absorbing latent is identified -- ablation effect on a TASK-SPECIFIC logit (the first-letter logit) after projecting out the probe direction; (c) the absorption-fraction metric definition. CONFIRM the diagnostic REQUIRES (i) a supervised probe and (ii) a task label/logit, and that the empirical demonstration is almost entirely first-letter spelling (running example 'short'/'starts-with-S').
    1b. State the DELTA vs Chanin (label-free): CCRG's anchor is chosen by content-response RECALL on counterfactual pairs (available to every baseline, NO probe); the recall-hole is the parent's uncovered counterfactual pairs (NO logit); the precision-gate is firing-precision on the target sub-context (NO label beyond the counterfactual partition). Chanin DETECTS absorption on an individually-named latent GIVEN a supervised probe+logit; it does NOT propose parent+absorber as a usable, editable handle WITHOUT supervision, and is form-bound to spelling in its demonstrations. CCRG uses the FORM-FREE probe+ablation diagnostic ONLY to SCORE already-formed KG edges (non-circular), never to FORM units. So the buy is: training-free, label-free, form-free SURFACING of the precise sub-context latent that marginal-attribution selection silently drops.
    1c. MAX-PRECISION delta: the open question the iter-8 EXPERIMENT answers is whether the anchored recall-hole-guided set-cover beats a simple 'pick the single most precise latent firing on the target sub-context' (max-precision / S-prec) selector. Because every reported edit win is effectively k=1, the LIKELY answer is a TIE. Supply TWO conditional wordings: (TIE) trim to 'anchored recall-hole-guided PRECISION SELECTION of a single absorber'; present set-cover/(1-1/e) as MOTIVATION for the disjoint-support coverage view only, NOT a load-bearing guarantee; the discovery step's value over max-precision is the RECALL-HOLE ANCHORING that tells you WHICH sub-context to select a precise latent FOR (max-precision alone needs the sub-context handed to it). (SET-COVER ADDS SOMETHING) if any case shows k>1 or the recall-hole objective measurably helps, keep the set-cover framing but still demote (1-1/e) to motivation. Make clear GEN_PAPER_TEXT picks the wording matching the experiment's M3''' result.
    1d. Briefly search 'precision-weighted SAE latent selection' / 'recall-based vs precision-based SAE feature selection' / 'max-precision latent baseline steering' to confirm no existing named method already IS 'anchored recall-hole precision selection' (defensive novelty check); record near-misses (FGAA relevance/density filtering; CorrSteer correlation selection; Arad output-score filtering -- see D2) and state the delta (those select for steering EFFECT or correlation, not for the recall-hole an absorbed parent leaves).
  WRITE: research_report.md section D1 = the Chanin-and-max-precision delta paragraph (drop-in for the Related Work / Method-identity subsection), plus the two conditional trim sentences.

  ========== STEP 2 -- DELIVERABLE D2: CONCENTRATION-AS-SHARP-GATE (M3''' mechanism reframe grounding) ==========
  GOAL: ground the claim 'the edit advantage is a property of a PRECISE/CONCENTRATED latent acting as a SHARPER conditional gate than a footprint-matched dense projection; absorption is ONE label-free-discoverable source of concentration, not the cause of the win' against prior work relating per-feature precision/sparsity/selectivity to steering surgicality. This makes 'concentration not absorption' POSITIONED, not merely asserted.
  VERIFIED ANCHOR CITES (confirm IDs/venues/authors via fetch_grep of arXiv Comments; flag if unresolved):
    2a. Arad, Mueller, Belinkov -- 'SAEs Are Good for Steering -- If You Select the Right Features' (arXiv 2505.20063; verify EMNLP 2025). KEY: introduces input vs OUTPUT scores; filtering OUT low-output-score features gives 2-3x steering improvement => the right FEATURE SELECTION (a precise, output-effective feature), not the steering mechanism, drives steering quality. This is the HEADLINE cite for 'which precise latent you pick is what matters' -- directly supports CCRG's 'label-free discovery of WHERE to gate' and the concentration reframe.
    2b. CorrSteer -- 'Generation-Time LLM Steering via Correlated Sparse Autoencoder Features' (arXiv 2508.12535; Cho, Wu, Koshiyama; Comments say ICML 2026 -- FLAG/verify, cite preprint if unresolved). Correlation-based selection extracts 'more relevant features, thereby reducing spurious correlations' => precise/specific selection reduces collateral.
    2c. FGAA -- 'Steering LLMs with Feature Guided Activation Additions' (arXiv 2501.09929; verify authors/venue). Relevance + density/'concreteness' filtering: high-DENSITY (frequently-firing) features dominate despite limited task specificity and must be filtered out => low-density + high-precision = concentration = a clean handle. Directly supports the concentration axis (sparse firing + high per-sub-context precision).
    2d. Sparse Activation Steering -- 'Steering Large Language Model Activations in Sparse Spaces' (arXiv 2503.00177; verify). Scaling SAE width increases steering-vector sparsity/monosemanticity => 'better disentangle features by reducing overlap', improving intervention precision => sparser/more-concentrated => sharper gate.
    2e. Anthropic 'Scaling Monosemanticity' (Templeton et al. 2024, transformer-circuits.pub; cite as the canonical monosemanticity source). The precise-boundary claim: monosemantic features 'stop responding the moment text diverges from the target concept' -> a precise feature's firing IS a sharp conditional gate. Use to ground the conditional-gate-sharpness intuition.
    2f. Tie to the LOCKED iter-7 gating cites (CAST/GSS/GUARD-IT/SADI): the gating MECHANISM is prior art and supervised; a concentrated latent's calibrated JumpReLU firing is itself a sharp, threshold-free conditional gate, whereas a footprint-matched DENSE projection must be driven to beta~3 over-erasure to match the same forget (=> ~14x more collateral on 'large'). So the edit advantage = sharper conditioning from a concentrated detector, NOT absorption per se.
  SEARCH (to find any stronger/more-direct cite and avoid missing an obvious one): 'feature selectivity predicts steering side effects', 'sparse precise feature cleaner edit handle lower collateral', 'per-feature specificity steering fluency tradeoff', 'conditional steering reduces collateral selective feature'. Record 1-2 best additional hits with verified IDs.
  WRITE: research_report.md section D2 = the concentration-as-sharp-gate positioning paragraph(s): (i) state the property the method should select for = per-sub-context PRECISION x sparse firing = CONCENTRATION; (ii) cite 2a-2e that selection of a precise/specific/low-density feature is the established driver of clean steering; (iii) state that absorption is one label-free-discoverable source of concentration (absorber marginal-attribution drops) but a concentrated CO-FIRING latent (insult, found by max-AUC not set-cover) also wins, so the win predictor is concentration; (iv) explicitly DROP/heavily-qualify 'the win traces to the absorption structure the method discovers'.

  ========== STEP 3 -- DELIVERABLE D3: RETARGET/VENUE + BOTH ABSTRACT/INTRO SPINES (M2''' retarget) ==========
  GOAL: decide and justify leading the paper with 'training-free auditable LOCALIZATION + EDITING of homograph-polysemy absorption', confirm venue-area fit, and supply BOTH spines.
    3a. VENUE FIT: confirm via iclr.cc/Conferences/2026/CallForPapers and icml.cc/Conferences/2026/CallForPapers that the framing fits. NOTE the GOAL says 'Target ICLR primary, ICML fallback' while THIS artifact-direction says 'ICML primary acceptable, ICLR fallback' -- TREAT THE GOAL AS AUTHORITATIVE (ICLR primary) but explicitly state fit for BOTH and resolve the tension in-report. ICLR 2026 lists 'Interpretability, fairness, privacy, and ethical AI' as an area (fits). NOTE ICML 2026 main-track submission closed ~Jan 28 2026 (so the live cycle for a mid-2026 paper is ICLR 2026 / the next ICML); the deliverable is AREA fit, not a deadline. Map the contribution to the reviewer-evaluable areas named in the goal (clustering methods, feature selection, classification, knowledge graphs, knowledge extraction, applied knowledge discovery, text data analytics, LLMs/deep learning) -- the localization + editable feature-KG + label-free discovery framing fits these far better than a classification-win framing (the paper makes NO out-classifies-dense claim). State this mapping explicitly so the title/abstract commit to localization+editing, not classification/steering wins.
    3b. RETARGET DECISION: lead with auditable LOCALIZATION (+ EDITING on concentrated features) of homograph-polysemy absorption; safety-homograph-confinement null (2/44, both homographs) as the HEADLINE LIMITATION-and-finding; the concentrated-feature edit (large +1.00, Amazon +0.75) as a SCOPED capability bounded by the fair gated control; classification SUPPORTING/within-SAE; router DEMOTED to exploratory. Build directly on the iter-7 localization-first spine (carry it, then update for: de-inflation to +1.00-lead; the new fair bounded-beta d_sub control; concentration-not-absorption mechanism; set-cover-as-motivation; both forget instruments; unified gate operator).
    3c. SUPPLY BOTH SPINES (drop-in abstract ~150-220 words + intro opener ~1 para each):
       - OUTCOME A (>=4 independent concentrated wins LANDED: large, Amazon + Bush/Cook/wider-vocab under the fair bounded-beta d_sub-gated control): the sparse-gated EDIT is a broader load-bearing capability. Abstract foregrounds: training-free label-free localization of homograph-polysemy absorption + an editable feature-KG; the edit win LED by KG-vs-STRONGEST-dense (+1.00 on large; never lead with +1.58) on >=4 concentrated features, shown to track CONCENTRATION (max-precision ablation) and to beat the genuinely-fair bounded-beta d_sub-gated dense control; safety null as capping scope.
       - OUTCOME B (base STAYS THIN, n~=2; or the fair gated control MATCHES KG): lead FULLY with the auditability/localization SPINE + the safety-homograph-confinement NULL as the finding; the edit is a scoped capability on concentrated features; if fair-gated matches => contribution = label-free DISCOVERY of where to gate (gating is prior art); concentration-not-absorption reframe central; set-cover = motivation only.
       Each spine must: state localization-NOT-classification up front; name the durable contribution triad (label-free discovery + editable feature-KG; recall-hole screening diagnostic = exploratory; absorption-regime/concentration selection wins where the signature holds); headline the homograph-confined safety null; and avoid the inflated +1.58-vs-footprint-gated number as the lead.
  WRITE: research_report.md section D3 = venue-fit justification + retarget decision + BOTH abstract+intro spines, clearly labeled OUTCOME-A and OUTCOME-B with a one-line selector telling GEN_PAPER_TEXT which to use based on the M1'''/M2''' experiment results.

  ========== STEP 4 -- DELIVERABLE D4: CITATION FINALIZATION + D5: PRESENTATION-STRIP CHECKLIST ==========
    4a. CARRY FORWARD the FULL locked-cite table from iter-7 section (E) + iter-6, VERBATIM (Chanin 2409.14507 NeurIPS2025; Feature-Hedging 2505.11756; AxBench 2501.17148 ICML2025; SAEBench 2503.09532 ICML2025; CanonicalUnits 2502.04878 ICLR2025; Matryoshka 2503.17547 ICML2025; Farrell 2410.19278 NeurIPS2024-Safe-GenAI-WS; SPLINCE 2506.10703 NeurIPS2025; Karvonen-Marks 2506.10922 NeurIPS2025-MechInterp-WS; Ahsan-Wallace 2511.00177 ICLR2026; BiasEdit 2503.08588 TrustNLP@NAACL2025; Collapsed-LMs 2410.04472 ICLR2025; Entity-Level-Unlearning COLING2025; Deng 2506.18141 ACL2026; SAEmnesia 2509.21379 ICML2026; Peng 2506.23845; CRISP 2508.13650 ACL2026; SAUCE 2503.14530 WITHDRAWN/ICCV2025-CVF; SSPU 2505.24428 EMNLP2025; LEACE 2306.03819 NeurIPS2023; CAST 2409.05907 ICLR2025-Spotlight; GUARD-IT 2605.12765 preprint; GSS 2602.08901 preprint; SADI 2410.12299 ICLR2025-Poster; PID-Steering 2510.04309 preprint; DAC 2406.17563 preprint; the iter-6 debiasing set; JTT/GEORGE/EIIL/LfF; DiffCoEx/WGCNA; Nemhauser-Wolsey-Fisher/Feige set-cover; CDLC 2505.07073; Veitch 2106.00545; Kaushik CAD ICLR2020; CEBaB 2205.14140; ParaDetox). Do NOT re-verify settled locks; just list them with their locked venues and flag the ones the dependencies already flagged unresolved (GUARD-IT/GSS/DAC venues; DeBiasLens CVPR2026; Deng dual-listing; Karvonen-Marks workshop).
    4b. ADD the NEW concentration/precision-steering cites, each with fetch_grep-VERIFIED arXiv ID + Comments-field venue + FULL author list: Arad-Mueller-Belinkov 2505.20063 (verify EMNLP2025); CorrSteer 2508.12535 Cho-Wu-Koshiyama (Comments=ICML2026, FLAG); FGAA 2501.09929; Sparse-Activation-Steering 2503.00177; Anthropic Scaling-Monosemanticity (Templeton et al. 2024, transformer-circuits.pub -- cite by URL, no arXiv). For any venue not grep-confirmable from the Comments field, cite as PREPRINT and add to the unresolved-flags list. INVENT NOTHING.
    4c. EMIT BibTeX for every NEW cite added this iteration (the concentration set); carry the iter-6/iter-7 BibTeX by reference (note GEN_PAPER_TEXT already has it).
    4d. PRESENTATION-STRIP CHECKLIST (research_report.md section D5), 10-12 items: (1) lead title/abstract with 'training-free auditable LOCALIZATION (+ EDITING) of homograph-polysemy absorption'; (2) lead the edit table with KG-vs-STRONGEST-ungated-dense (+1.00 on large) -- caveat the +1.58-vs-footprint-gated number with the beta~2.97 over-erasure note (gated collateral 0.290 vs its own ungated 0.021); (3) report BOTH forget instruments (completion-drop AND sub-probe-drop) side by side and match operators on a BEHAVIORAL measure, not next-token KL; (4) UNIFY the gate operator into ONE definition across large/Amazon/Bush (or document the per-case clamp in-table: 3%-global-footprint vs 95%-X-rate); (5) present set-cover/(1-1/e) as MOTIVATION only; method identity = 'anchored recall-hole-guided precision selection of a single absorber'; (6) state the mechanism as CONCENTRATION/PRECISION not absorption (insult co-fires yet wins; Georgia/Jordan absorb yet lose); (7) safety-homograph null (2/44) = headline limitation; (8) state localization-NOT-classification (no SAE unit out-classifies a dense probe on any task); (9) router = exploratory (out-of-sample Wilson includes 0.5); (10) corrected selectivity (722x/676x; 16k/65k comparably surgical), cross-dictionary 65k full/layer-9 partial; (11) demote multi-member grouping + C-track to secondary (single absorber wins, multi-member adds collateral); (12) STRIP all iteration/rebuttal/infra scaffolding (M1''/M1'''/art_ tags/'iter-7 reviewer'/GPU-hours).

  ========== STEP 5 -- ASSEMBLE OUTPUTS ==========
  Write research_out.json with: title; summary; answer (a tight synthesis of D1-D5 with the key verdicts: method-identity = anchored recall-hole precision selection / set-cover=motivation; mechanism = concentration not absorption, positioned via 2505.20063/CorrSteer/FGAA/SAS/monosemanticity; retarget = localization+editing lead with both spines; cites locked); sources[] (every fetched URL with a one-line evidence note: Chanin body, the 4-5 concentration cites with verified venue/authors, ICLR/ICML CfP pages, plus the carried iter-6/iter-7 anchors by reference); follow_up_questions[] (e.g.: did M3''' show set-cover beats or ties max-precision? did M2''' land >=4 wins -> use OUTCOME-A or OUTCOME-B spine? did M1''' fair bounded-beta d_sub-gated control get beaten or matched? are the CorrSteer/Arad venues confirmable before camera-ready?). Write research_report.md with sections D1-D5 as specified, including all drop-in paragraphs, both spines, the locked+new cite table, BibTeX for new cites, unresolved-flags list, and the presentation-strip checklist.

  ========== CONTINGENCIES / FAILURE MODES ==========
  - If the Chanin HTML body is inaccessible, use the OpenReview PDF (fetch_grep) or the NeurIPS 2025 poster page; the supervised-probe + first-letter-logit + absorption-fraction facts are already corroborated by search snippets -- confirm and cite, do not block.
  - If a new concentration cite's venue is not grep-confirmable from the Comments field, cite as preprint + add to unresolved flags (NEVER invent a venue). CorrSteer's 'ICML 2026' is from Comments -> keep but flag (large 45-page preprint, may be a workshop/under-review listing).
  - If the concentration-steering literature turns out thinner than expected, fall back to the strongest anchors (Arad 2505.20063 + the locked CAST/GSS + Anthropic monosemanticity precise-boundary claim) -- these alone ground the reframe; do not pad with weak cites.
  - If venue CfP pages are unreachable, rely on the known areas (ICLR 'Interpretability, fairness, privacy, ethical AI'; reviewer-evaluable areas in the goal) and proceed; venue choice is ICLR-primary per the goal regardless.
  - Keep ALL load-bearing numbers consistent with the hypothesis; if a number is needed that is not in the hypothesis, mark it [VERIFY-AT-WRITE] rather than inventing.
  - Strictly $0 LLM spend (web research only); no OpenRouter calls.
explanation: >-
  This research artifact finalizes the iteration-8 CCRG paper positioning so GEN_PAPER_TEXT can write a defensible draft regardless
  of how the parallel iter-8 experiments (M1''' fair gated control, M2''' expanded base, M3''' max-precision ablation) land.
  The iter-7 reviewer raised three publication-gating majors that are framing/positioning problems this artifact must resolve:
  (R6/M5''') the set-cover/(1-1/e) framing oversells a step that is effectively k=1, so the novelty must be trimmed to 'anchored
  recall-hole-guided precision selection' with a precise stated delta vs Chanin's SUPERVISED diagnostic and vs a simple max-precision
  selector; (R3/M3''') the claim 'the win traces to absorption structure' is unsupported because a concentrated CO-FIRING
  latent also wins, so the mechanism must be reframed to latent CONCENTRATION/PRECISION and POSITIONED against the established
  feature-selection-for-steering literature (where selecting a precise/specific/low-density feature is the known driver of
  clean steering); (R2/M2''') the positive edit base is n~=2, so the paper must retarget to lead with auditable localization+editing
  of homograph-polysemy absorption with the safety-homograph null as the headline limitation, and needs both a wins-landed
  and a base-thin abstract/intro spine ready. The artifact also locks the citation set (carrying the iter-6/iter-7 venue-verified
  table verbatim and adding verified concentration/precision-steering cites) and supplies a presentation-strip checklist.
  Without this positioning pass the paper would lead with the inflated +1.58 number, an oversold set-cover guarantee, and
  an unsupported absorption-causation claim -- exactly the three things the reviewer flagged as blocking. Pure web research
  is the right tool: every deliverable is literature synthesis, delta articulation, venue-area mapping, and citation verification
  -- no computation, and it must run in parallel with the experiments so its both-outcome wording is ready for GEN_PAPER_TEXT.
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

### [5] HUMAN-USER prompt · 2026-06-18 19:51:21 UTC

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
