# gen_plan_experiment_4 — test_idea

> Phase: `invention_loop` · round 4 · `gen_plan`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_plan_experiment_4` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-17 21:50:31 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A plan generator (Step 3.2: GEN_PLAN in the invention loop)

You received the hypothesis, an artifact direction to elaborate, and dependency artifacts relevant to the plan.
Your job: elaborate this direction into a detailed, actionable plan for the executor agent.

Specific, actionable plan → valuable artifact. Vague plan → wasted execution.
</your_role>
</ai_inventor_context>

<artifact_type_info>
You are expanding an artifact direction of type: EXPERIMENT

EXPERIMENT
Run code to test hypotheses, implement methods, and collect empirical results.
Runtime: Python 3.12, UV (any pip package), isolated workspace, gradual scaling (mini → full data).
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Implement and run any code-based experiment, compare method vs baselines.
Deps: REQUIRED at least one DATASET | OPTIONAL RESEARCH for methodology guidance
</artifact_type_info>

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

<time_budget>

The experiment executor has 6h total (including writing code, debugging, testing, and fixing errors).

</time_budget>

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

<plan_guidelines>
You are expanding an artifact direction from the strategy into a detailed plan.
The artifact direction specifies what to do at a high level (type, objective, approach, dependencies).
Your job is to make it concrete and actionable as a detailed plan.
Use web research to look up technical details, verify feasibility, and find reference materials
that will make your plan more concrete and actionable for the executor.

GOOD PLANS:
- Make each component SPECIFIC and actionable (not vague platitudes)
- Consider both success AND failure scenarios
- Build on the approach in the artifact direction
- Add concrete details the executor needs

BAD PLANS:
- Vague hand-waving ("do research on X")
- Ignoring the approach in the artifact direction
- Missing critical details the executor needs
</plan_guidelines>

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

NOTE: a previous attempt at the task below was interrupted before it finished, and you are a FRESH session that does not remember it.

Any partial work the previous attempt wrote is on disk under /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_plan/gen_plan_experiment_4 — inspect that directory and REUSE whatever usable work is already there; do NOT start over from scratch if you can build on it. Then carry the task through to completion.

----- ORIGINAL TASK BELOW -----

<hypothesis>
kind: hypothesis
title: >-
  Auditable, Training-Free Repair of the SAE Absorption Regime: Two-Track Co-Response Grouping with a Measured Knowledge-Graph
  Repair Loop, Within-SAE Selection Gains, and a Firing-Jaccard-Plus-Recall-Hole Router for When Latent Grouping Beats Marginal-Attribution
  Selection
hypothesis: |-
  ITERATION-3 STATUS -- THE DECISIVE SELECTION CONTROL RAN AND THE AUDITABILITY RESULTS LANDED; THE LEAD NON-SPELLING CLAIM DID NOT SURVIVE SCRUTINY. Iteration 3 added five executed analyses on the FROZEN Gemma-Scope L12/16k JumpReLU SAE: a first-letter re-run with the random-eligible-k (RE-k) control + true AUC-difference CIs [art_8AwUJK9qOwX_]; a non-spelling re-analysis with RE-k / RE-k-anchored selection isolation [art_P8-3ipCuQwVY]; the two previously-dropped MEASURED auditability results [art_lvYKkaolutJG]; the a-priori firing-structure router validated prospectively [art_07ju05r0onqB]; a confound-bounded model-diffing result [art_jI2KIJotjzIU]; and a citation audit [art_i-tkvFCKneA-]. What honestly landed:
    - FIRST-LETTER SELECTION vs RE-k: the label-free unit beats the random-eligible-k pool on ALL 5 letters (frac_rek_ge_unit <= 0.009; pooled AUC +0.237 CI[0.191,0.280]) and the count-matched supervised attribution pool (h) on 3/5 (T +0.218, I +0.227, D +0.156; NOT L +0.081 CI incl 0, NOT O +0.096 CI incl 0). The iter-2 mislabeled accuracy-as-AUC margins are replaced with threshold-free AUC + bootstrap AUC-difference CIs (the R1 honesty fix). BUT (review MAJOR-rigor) the PER-LETTER JOINT of (E1 absorption mechanism) AND (selection beats both (h) and RE-k) is only {T,D} = 2/5, BELOW the stated 3/5 majority: E1 holds on {L,O,T,D}, the selection win holds on {T,I,D}, and the one extra selection letter (I) is EXACTLY where E1 FAILS (the recall-argmax anchor 1227 fires 0% on corpus). So 'I' is a pooling-classifies-well result, NOT a confirmed absorption repair; the emitted ABSORPTION_REPAIR_SELECTION_CONFIRMED verdict over-aggregates two separately-satisfied conditions.
    - MEASURED AUDITABILITY -- the strongest, most defensible, and now LOAD-BEARING result [art_lvYKkaolutJG]: the KG-guided recall-repair loop recovers a parent's recall holes with 8 repairs whose KG-minus-random-addition gain CI excludes 0 (taxonomic Georgia 0.20->1.00 gain 0.80 CI[0.70,0.82]; Jordan 0.29->1.00; United States 0.77->0.99; first-letter O/'our' and D/'day' 0.00->1.00), while a label-free dense group-inference probe (k) classifies the holes but exposes NO addable per-sub-context latent (its decoder-projection argmax is the parent, never the absorber). LLM member-labeling agrees with WITHHELD sub-context labels at 0.716 vs shuffle null 0.090 (gap CI[0.522,0.731]; absorbers 0.758, anchors 0.20). Honest negatives: first-letter L and T candidate words TIE the random-addition control. This is a capability a dense probe STRUCTURALLY LACKS -- the dimension on which the method genuinely and uniquely wins.
    - A-PRIORI ROUTER [art_07ju05r0onqB]: firing-Jaccard separates the regime EXTREMES (spelling firing-disjoint J<0.05 -> grouping helps; toxicity co-fires J~0.69 -> attribution wins; tau*=0.05, balanced-acc 0.917 on the 12 DERIVATION concepts). HONEST CORRECTIONS the review demands: firing-Jaccard ALONE is insufficient (numeric high-J yet absorption-like; aggregated-taxonomic low-J yet co-firing because the parent already has ~0.95 recall and no holes); the recall-hole signal alone reaches balanced-acc 1.0 and the COMBINED rule (low firing-Jaccard AND high parent recall-hole) is the real recommendation. Only 3 concepts were TRULY prospective (sentiment HIT; CEBaB food/service MISS) = 1/3 hits, LOO 0.733. The router is a SCREENING HEURISTIC WITH MEASURED ERROR, not a validated oracle; 'validated prospectively across spelling/taxonomic/toxicity/sentiment/aspect' is WRONG (the first three are the derivation set).
    - NON-SPELLING -- the review's highest-impact finding: the lead 'diagnostic-corroborated taxonomic hierarchy' is an OVERSTATEMENT built on a UNIT/SPECIALIST CONFLATION. The K-track CLASSIFICATION unit is [3792(anchor), 4697(Georgia), 9339(Jordan), 8442(US)]; per-edge form-free KG-agreement is Georgia(4697)=0.0, Jordan(9339)=0.955, US(8442)=0.0, so the headline '0.318' is the 3-edge MEAN driven ENTIRELY by Jordan -- the headline Georgia edge is NOT corroborated. Worse, those classification absorbers FAIL the method's own per-member precision floor (subctx_precision 0.350/0.633/0.347 < 0.70) and are NOT the diagnostic-corroborated, precision-passing specialists in non_triviality_passing_absorbers (Georgia=16009 prec 0.955 gain 0.482; Jordan=540 prec 0.975, 8347 prec 1.0). The classifier and the 'corroborated specialists' are DIFFERENT latent sets, and the greedy max-coverage objective PREFERRED the high-coverage/low-precision Georgia absorber (4697 gain 0.545 prec 0.35) over the high-precision corroborated one (16009 prec 0.955) -- a real limitation of pure coverage. absorption-type slices are EXACTLY Georgia + Jordan (the ambiguous homographs with parent recall holes); every other country has parent_recall_hole ~= 0. So non-spelling 'generalization' is a HOMOGRAPH/POLYSEMY phenomenon, not broad taxonomic absorption; the single corroborated edge (Jordan) is on a DESCRIPTIVE slice (n=124<150, ineligible). Numeric remains eligibility+pooling (RE-k-anchored CI incl 0) and diagnostic-unconfirmed (KG top-1 0.0; dense probe AUC 1.000).
    - MODEL-DIFFING [art_jI2KIJotjzIU]: a confound-bounded NULL (shared pt-SAE; toxicity base-vs-IT departure 0.062 matched IDENTICALLY by the spelling control -> control-subtracted genuine shift +0.000 CI[-0.009,0.007]; unit does NOT beat the best single latent). A valid infrastructure-bounded deliverable, NOT a positive contribution.

    WHAT THE REVIEW EXPOSED -- FOUR GAPS THAT DRIVE ITERATION 4:
      (R1, SCOPE -- the fundamental one) After all fixes the affirmative CLASSIFICATION contribution reduces to a within-SAE-ecosystem selection win on 3/5 (per-letter joint 2/5) first-letter letters; the unit out-classifies NO non-SAE dense probe on ANY task (Georgia 0.989 vs dense 1.000; numeric 0.687 vs 1.000; toxicity loses to a residual probe), and toxicity -- the only safety-relevant family -- is a clean co-firing negative. The genuinely UNIQUE capability is the MEASURED, EDITABLE auditability (KG repair + member-labeling) on a dimension the dense probe lacks. => PIVOT the headline to AUDITABLE ABSORPTION-REGIME REPAIR + the router for when to use it; EXPAND auditability.
      (R2, INTEGRITY) The taxonomic unit/specialist conflation must be fixed: make the classifier and the corroborated specialists the SAME unit by rebuilding from precision-passing, diagnostic-corroborated absorbers; report per-edge agreement; state corroboration currently holds only for the descriptive Jordan edge; discuss the max-coverage-vs-precision limitation.
      (R3, RIGOR) Report the first-letter per-letter JOINT (E1 AND selection)=2/5 and annotate I as selection-without-mechanism; ISOLATE the set-cover-specific claim against NON-RANDOM label-free selection controls (RE-k is too easy -- its AUC ~0.63-0.69 is at/below the best single latent on every letter, so 'unit beats RE-k' largely restates 'good selection beats random/best-single').
      (R4, FRAMING) The router is a screening heuristic with measured error (combined rule, 1/3 prospective); reported units must honor (or transparently report held-out collapse of) their precision floors; the 15-wide max-pool vs the compact named unit must be disentangled; rebuttal/iteration scaffolding must be stripped from the paper.

    THE ITERATION-4 MANDATE (load-bearing first; nothing else is load-bearing until these exist):
      (M1 = NEW HEADLINE -- EXPAND MEASURED AUDITABILITY) Make the KG-guided recall-repair loop + member-labeling the CENTRAL contribution. Add concepts/sub-contexts beyond the current 8 repairs; add at least one concrete DOWNSTREAM task where the localized, editable single-latent fix matters and a dense probe cannot deliver it (e.g. targeted recall recovery on a held-out safety-relevant sub-context, or a KG-localized steering/erasure edit with side-effect/KL measurement). Keep the random-addition control and the (k)-cannot-localize comparison; report gains with bootstrap CIs. This is the result the paper now stands on.
      (M2 = FIX THE TAXONOMIC CONFLATION) Rebuild the taxonomic CLASSIFICATION unit from the precision-passing, diagnostic-corroborated absorbers (Georgia 16009 prec 0.955; Jordan 540/8347; US the precision-passing analog); report THAT unit's Georgia AUC and RE-k-anchored selection (likely STRONGER, since 16009 prec 0.955 vs 4697 prec 0.35). Replace the single '0.318' with PER-EDGE KG-agreement and state explicitly that diagnostic corroboration currently holds only for the descriptive Jordan edge unless the rebuilt high-precision unit corroborates Georgia. If the greedy still prefers low-precision absorbers, either add a PRECISION-GATE / precision-weighted coverage objective to the K-track or report the limitation of the max-coverage objective.
      (M3 = HOMOGRAPH SCOPE) Characterize precisely WHEN non-spelling absorption occurs: homograph/polysemous tokens whose general parent latent is suppressed (Georgia = US-state/country/given-name; Jordan = country/given-name). Report that absorption-type slices are exactly the homographs with parent recall holes; REFRAME from 'broad taxonomic generalization' to 'absorption recurs on polysemous tokens, predicted by the router's recall-hole signal'. Keep numeric as suggestive/diagnostic-unconfirmed.
      (M4 = ENDPOINT HONESTY) Report the per-letter JOINT (E1 AND selection) = 2/5 (T,D) alongside the marginal counts; rename/reconcile the emitted verdict so it does not imply mechanism+selection co-occur on 3 letters; annotate I as 'selection win without confirmed absorption mechanism'.
      (M5 = ISOLATE SET-COVER FROM SENSIBLE SELECTION -- the new selection falsifier) Add NON-RANDOM, label-free, count-matched-to-k selection controls: (S-rec) top-k by content-flip recall, (S-prec) top-k by firing precision, (S-mag) top-k by mean response magnitude. The two-track set-cover claim is established ONLY if the unit SIGNIFICANTLY beats these (AUC-difference CI excluding 0); otherwise scope the claim to 'cover-based eligibility + sensible label-free selection', NOT the set-cover algorithm specifically. RE-k is RETAINED but DEMOTED to a floor.
      (M6 = ROUTER AS SCREENING HEURISTIC) Lead with the COMBINED rule (low firing-Jaccard AND high parent recall-hole); report derivation (12 concepts) vs TRULY-prospective (3 concepts, 1/3 hits, LOO 0.733) SEPARATELY; describe it as a screening heuristic with a measured error rate; if cheap, add more truly-held-out concepts to strengthen the prospective test. Do NOT list derivation concepts as if prospective.
      (M7 = UNIT TRANSPARENCY) Report HELD-OUT per-member subctx_precision and state the FOLD each gate (precision, Jaccard, gain-CI) is evaluated on; report the COMPACT named-member-only unit AUC alongside the 15-wide max-pool, and the FRACTION of the 15 members that receive a confident (non-shuffle) member-label; restrict the 'auditable' claim to the characterized subset or show the named structure carries the signal.
      (M8 = PRESENTATION + CITATIONS) Strip all rebuttal/iteration/infrastructure scaffolding ('previous draft', 'iter-3 re-runs', 'torch 2.8+cu128', verdict-reconciliation notes); move reproducibility notes to an appendix. Keep the citation-audit fixes [art_i-tkvFCKneA-]: Chanin 'A is for Absorption' -> NeurIPS 2025; AxBench/SAEBench -> ICML 2025; CanonicalUnits -> ICLR 2025; Winnicki 2604.23829 observational-KG contrast; audit all 2025/2026 venues.
      (M9 = RESOLVE/RETAIN) Model-diffing stays a confound-bounded NULL limitation (do not promote). Steering stays a generality demo (unit most surgical on L and D only).

    RE-DESIGNATED HEADLINE (auditability-first; the SAME two-track method, honestly scoped). On a FROZEN public SAE, grouping latents by interventional co-response to content counterfactuals via the TWO-TRACK algorithm yields training-free, human/LLM-auditable multi-member units and a feature-level KNOWLEDGE GRAPH whose edges carry MEASURED, localized repair utility: a KG-named absorber added to a suppressed parent recovers its recall hole, beating a random-addition control (CI excludes 0) -- a fix a dense probe provably cannot localize. In the ABSORPTION REGIME (mutually-exclusive parent/child firing WITH parent recall holes) the unit also recovers absorbers a count-matched marginal-attribution selection drops at matched pool size (within-SAE selection win on first-letter T,D; on a taxonomic HOMOGRAPH slice corroborated by an independent diagnostic ONCE the unit is built from precision-passing specialists). And a single cheap forward-pass measurement -- low firing-Jaccard AND high parent recall-hole -- is an a-priori SCREENING HEURISTIC that predicts which regime a concept is in before any grouping. The method does NOT generally out-classify a strong non-SAE dense probe; its value is AUDITABLE, EDITABLE, REGIME-TARGETED REPAIR plus the a-priori router.

    PRIMARY ENDPOINT (re-designated, auditability-spined, per-letter, code-honored).
      (a) AUDITABILITY (NEW LOAD-BEARING): at least one KG-guided repair recovers a parent recall hole with a bootstrap-CI gain over the random-addition control, AND member-labeling exceeds the shuffle null -- BOTH achieved [art_lvYKkaolutJG]; iter-4 must EXPAND to more concepts + one downstream task where the localized fix matters.
      (b) ABSORPTION-REGIME SELECTION (first-letter, SUPPORTING): the PER-LETTER JOINT of E1 (K-proposal recovers diagnostic parent + >=2 absorbers above the random-membership null) AND the SELECTION test (unit AUC beats BOTH (h) AND the NON-RANDOM label-free selectors of M5, AUC-difference CI excluding 0) on a majority of letters; currently 2/5 (T,D) against RE-k, to be RE-TESTED against the M5 controls. If the unit fails to beat the M5 non-random selectors, the selection claim is reframed to 'cover-based eligibility + sensible selection' (publishable).
      (c) ROUTER: the combined firing-Jaccard-AND-recall-hole heuristic reproduces with derivation/prospective reported separately.
    E2 absorbed-slice recall is SECONDARY (significant on T only). The headline NO LONGER depends on classification beating attribution on >=3 letters -- auditability is the spine.

    THE TWO-TRACK CLUSTERING ALGORITHM (specification unchanged except the K-track precision fix). STEP 1 cover-based eligibility (content-responsive above a shuffle null; firing-precision>=0.7; covers>=1 sub-context -- mean-over-pairs discards sparse absorbers). STEP 2 C-TRACK (splitting): positive-Spearman soft-threshold affinity (beta=6, WGCNA) -> Leiden RBConfiguration; resolution by bootstrap-ARI stability; run in a subprocess with a 45s timeout + agglomerative fallback (Leiden hangs on tied-rank graphs). STEP 3 K-TRACK (absorption, anchored greedy max-coverage): ANCHOR = argmax cover-set chosen WITHOUT the diagnostic, with the UNSUPERVISED PARENT-VALIDATION step (anchor must fire on the held-out corpus above a floor -- fixes the letter-I 0%-corpus spurious anchor 1227); HOLES = parent's uncovered pairs; greedily add mutually-exclusive (firing-Jaccard<0.1), precise (>=0.7) absorbers covering holes with marginal-gain>=0.05 CI excluding 0. NEW FIX (M2/M7): the greedy objective must NOT prefer high-coverage/low-precision absorbers over high-precision diagnostic-corroborated ones -- gate or precision-WEIGHT the coverage objective, and apply the precision floor on a HELD-OUT fold so the reported unit's members satisfy the stated floors (Georgia must select 16009 prec 0.955, not 4697 prec 0.35). STEP 4 reconcile C-communities and K-covers, de-duplicate by highest coverage gain. STEP 5 ADMISSION: signature C OR matched-null signature K (+ small-k absolute gain>=0.05 CI excluding 0, mutual-exclusivity, precision floor) AND unit-level surface invariance; multiplicity controlled at unit-proposal level (Bonferroni-within-unit then BH across M candidates; report empirical false-admit ~0.05-0.11).

    SAE-LATENT FIRING-STRUCTURE ROUTER (screening heuristic with MEASURED ERROR). One forward pass over data already held: encode examples, identify the content-responsive parent (with the firing-floor validation), find per-sub-context detectors, report (i) detector-vs-parent positive-only firing-Jaccard and (ii) parent per-sub-context recall holes. RULE: predict absorption-regime (grouping helps) iff firing-Jaccard is LOW (<~0.05-0.10) AND the parent has a recall HOLE (>~0.5-0.78). Firing-Jaccard alone reaches balanced-acc 0.917 on the 12 derivation concepts but mislabels numeric and aggregated-taxonomic; recall-hole alone reaches 1.0; the CONJUNCTION is the recommendation. Truly-prospective: 3 concepts, 1/3 hits (sentiment HIT co-firing; CEBaB food/service MISS predicted co-firing but showed small absorption deltas +0.034/+0.071), LOO 0.733. Report derivation vs prospective separately. Co-firing (toxicity threat 0.40, identity_attack 0.29, insult 0.66 >> 0.10) => splitting/co-activation regime => supervised attribution wins and CCRG does not help.

    BASELINE GLOSSARY (matched baselines primary): (a) best raw single latent; (b)/(c) observational co-activation/decoder clusters COUNT-MATCHED to k; (d) counterfactual diff-of-means; (e) raw-residual probe; (f) LEACE surface-invariant probe; (g) SCR/TPP oracle pool; (h) count-and-pool-matched SCR/TPP probe; (i) unmatched diff-of-means; (j) oracle group-DRO; (k) label-free group-inference (JTT/GEORGE). (RE-k) random-eligible-k pool = FLOOR (demoted; an easy bar). NEW REQUIRED (M5): (S-rec) top-k by content-flip recall, (S-prec) top-k by firing precision, (S-mag) top-k by mean response magnitude -- label-free, count-matched, NON-RANDOM selection controls. SET-COVER SELECTION is isolated ONLY by beating (S-rec)/(S-prec)/(S-mag), NOT merely (RE-k).

    NON-SPELLING TESTBED (re-scoped to HOMOGRAPH ABSORPTION). Absorption recurs on HOMOGRAPH/POLYSEMOUS tokens whose general parent latent is suppressed -- taxonomic absorption-type slices are EXACTLY Georgia + Jordan (homographs with parent recall holes); all other countries have ~0 hole and no selection advantage (so this is a homonym phenomenon, not broad taxonomic absorption). REBUILD the unit from precision-passing diagnostic-corroborated absorbers (16009 Georgia, 540/8347 Jordan) and report per-edge KG-agreement; corroboration currently holds only for the DESCRIPTIVE Jordan edge (n=124<150, ineligible). Numeric = eligibility+pooling, diagnostic-unconfirmed (RE-k-anchored CI incl 0; KG top-1 0.0; dense probe AUC 1.000). Honest scope: a non-SAE dense probe matches/beats the unit on ALL non-spelling classification.

    SCOPE AND VALUE PROPOSITION (reframed per the scope MAJOR). The previous 'absorption generalizes + classification win' framing is unsupported. The defensible contribution is: (1) MEASURED AUDITABILITY -- a feature-level KG whose edges carry localized, EDITABLE repair utility (recall-hole recovery beating random addition; (k) cannot localize) plus human/LLM-auditable members -- the UNIQUE capability a dense probe lacks; (2) an A-PRIORI SCREENING HEURISTIC (firing-Jaccard AND recall-hole) for when grouping helps vs when attribution wins; (3) a WITHIN-SAE absorption-regime selection win where it genuinely occurs (first-letter T,D; taxonomic homograph slices with a precision-passing, diagnostic-corroborated unit, pending the M5 non-random controls). The method does NOT claim to out-classify a strong dense probe; toxicity is a clean co-firing negative. HEADLINE = auditable absorption-regime repair + the router; classification is SUPPORTING and honestly within-SAE.

    HONEST NEGATIVES (each publishable): unit out-classifies NO non-SAE dense probe on any task; per-letter joint mechanism+selection only 2/5 (T,D); letter-I selection is pooling WITHOUT a confirmed mechanism (E1 fails, 0%-corpus anchor); taxonomic corroboration is a single DESCRIPTIVE homograph edge (Jordan), and the classification unit must be REBUILT to match the corroborated specialists; greedy max-coverage prefers low-precision absorbers (objective limitation); numeric is eligibility+pooling and diagnostic-unconfirmed; toxicity K-necessity REFUTED (real firing co-fires, departs from labels); router prospective 1/3, firing-Jaccard alone insufficient; model-diffing a confound-bounded null; steering surgical only on L,D; RE-k is an easy bar -- the set-cover-specific claim is PENDING the M5 non-random controls; bias_in_bios boundary-null. A clean failure of the AUDITABILITY spine (KG repair ties random addition everywhere) is the declared method-does-not-work outcome and is itself publishable.

    MOTIVATION (substance unchanged). Single SAE latents are unreliable units: feature absorption (a child latent suppresses a general parent's firing; Chanin 2409.14507, NeurIPS 2025), splitting, hedging (2505.11756), and 'SAEs Do Not Find Canonical Units' (ICLR 2025) converge on no single latent reliably tracking a concept; AxBench (ICML 2025) and DeepMind's negative report show plain diff-of-means beats raw-latent SAE methods. Absorption is the regime where OBSERVATIONAL signals break by construction (parent and absorbing child mutually exclusive in firing) and where MARGINAL-ATTRIBUTION selection (SCR/TPP) silently drops the absorber. Correlation-community detection (DiffCoEx/WGCNA transfer) handles shared-support splitting; anchored greedy set-cover (Nemhauser-Wolsey-Fisher / Feige (1-1/e) transfer) handles disjoint-support absorption -- coverage-complementarity is a set-level property no pairwise affinity can express. The crucial executed lesson: this matters ONLY in the absorption regime (mutually-exclusive firing AND parent recall holes), a cheap firing-Jaccard+recall-hole measurement tells you a priori whether you are in it, and the durable value is an AUDITABLE, EDITABLE feature-KG repair rather than a universal classification win. Training-free post-hoc repair of FROZEN public SAEs is exactly what practitioners holding Gemma Scope have; architectural remedies (Matryoshka/H-SAE/SASA) retrain and are orthogonal.

    SUCCESS CRITERIA. METHOD CONFIRMED iff: (LOAD-BEARING) at least one MEASURED KG-guided repair beats the random-addition control (CI excludes 0) AND member-labeling beats the shuffle null -- achieved, to be EXPANDED to more concepts + one downstream task where the localized fix matters; AND the a-priori screening heuristic (firing-Jaccard AND recall-hole) reproduces with derivation/prospective reported separately. SUPPORTING (strengthen, do not gate): first-letter per-letter JOINT (E1 AND selection) on a majority of letters AGAINST the M5 NON-RANDOM selectors (currently 2/5 vs RE-k); taxonomic HOMOGRAPH absorber recovery with a precision-passing, diagnostic-corroborated unit; toxicity K-refutation as the router's negative pole; admission false-admit <=0.05 with multiplicity control; the steering demo where the unit is most surgical (L,D). HONEST NEGATIVES are reportable: failure to beat the M5 non-random selectors reframes the contribution to 'cover-based eligibility + sensible selection'; a KG repair tying random addition removes the auditability value; numeric stays unconfirmed; a clean failure of the SELECTION test is the declared method-does-not-work-as-claimed outcome and is itself publishable.
motivation: |-
  Single SAE latents are unreliable units of analysis. Feature absorption (a specific child latent suppresses a more general parent's firing, leaving the parent with unpredictable holes; Chanin 2409.14507 [NeurIPS 2025], 2505.11756), feature splitting (one concept fragments across many latents), feature hedging (a narrow SAE merges correlated features into one polysemantic latent), and 'SAEs Do Not Find Canonical Units of Analysis' (ICLR 2025, 2502.04878) converge on one conclusion: no single latent reliably tracks a concept. AxBench (ICML 2025 spotlight, 2501.17148) and DeepMind's negative-results report make the stakes concrete -- plain difference-of-means beats raw-latent SAE methods -- so any SAE-grouping method must clear strong simple baselines.

  WHY THE LOAD-BEARING CLAIM IS C1+C3, AND WHY THE ALGORITHM HAD TO BE SPECIFIED. The single most defensible deliverable is absorber recovery (C3): the co-response unit admits the absorber latents the supervised oracle's top-N marginal-attribution selection (g) and the count-matched pool (h) drop, with KG edges agreeing with the absorption diagnostic. But absorbers are MUTUALLY EXCLUSIVE in firing with their parent and respond on DISJOINT supports, so they have LOW pairwise content-response correlation -- meaning a correlation/affinity-merging clustering can never even PROPOSE the right group, and an admission rule that only FILTERS candidates cannot rescue a unit the proposal step never generated. This is why the contribution is now a TWO-TRACK algorithm: a correlation-community track for splitting (where support is shared) and a separate ANCHORED GREEDY SET-COVER track for absorption (anchor on the highest-recall parent candidate, greedily add mutually-exclusive latents that cover its holes). Maximum-coverage greedy selection is the natural, classic instrument for 'cover a set with complementary specialists' -- and it is exactly the instrument the absorption regime demands, because coverage-complementarity is a set-level property, not a pairwise affinity. The anchor is chosen WITHOUT the absorption diagnostic (by content-response recall, available to every baseline), so 'the unsupervised unit beats the supervised oracle' is not undercut and the KG-edge validation against the diagnostic is non-circular (the diagnostic scores edges, never forms them).

  The contribution lives squarely in clustering / feature-selection / classification for a learned knowledge representation (SAE features): cluster-level units plus a feature-level knowledge graph, evaluated on downstream classification (headline) with steering and model-diffing as generality demonstrations. Every existing POST-HOC grouping method relies on OBSERVATIONAL signals -- which latents fire together (co-activation feature families) or which decoders point alike (geometry). But absorption is exactly the regime where observational signals break BY CONSTRUCTION: the parent and absorbing child are mutually exclusive in firing, so co-activation clustering provably cannot group them and their decoders need not be cosine-similar. The standard SUPERVISED remedy -- select top-N latents by causal effect on a concept probe (SCR/TPP, Karvonen 2411.18895, built on Marks SHIFT) -- SILENTLY DROPS absorbed latents, because a latent firing only in a narrow sub-context has low MARGINAL attribution even though it carries the concept there.

  ABSORPTION BEYOND SPELLING IS UNDER-TESTED -- AND THAT IS AN OPPORTUNITY. The literature documents absorption empirically almost entirely on first-letter spelling; the sparsity-plus-hierarchy MECHANISM, however, predicts absorption in any token-level hierarchy (numeric formats, taxonomic entities). Promoting one non-spelling hierarchy into the load-bearing core therefore does double duty: it moves C3 from 'one synthetic spelling task' to 'absorption as a phenomenon', and it is itself a novel empirical test of whether absorption generalizes -- with the form-free probe-plus-ablation diagnostic (domain-agnostic) as oracle and an explicit honest-null fallback (absorption is spelling-specific -> scope C3, route generality through C1) if the non-spelling parent has no specialist-filled holes.

  RECENT ARCHITECTURAL REMEDIES ARE ORTHOGONAL (and confirm the gap). Subspace-Aware SAEs (SASA, 2606.06333), Matryoshka SAEs, Concept-Bottleneck SAEs (CVPR 2026), AbsTopK and Group SAEs all RETRAIN the SAE to reduce splitting/absorption at training time. We do the opposite: a TRAINING-FREE, POST-HOC repair of FROZEN public SAEs (Gemma Scope), exactly as the goal requires. No retraining method produces a human-auditable multi-member unit over an existing public SAE, which is what practitioners actually have.

  TWO cross-field transfers motivate the method. (1) Systems biology faced the identical grouping obstacle: co-regulated genes are often NOT co-expressed at baseline and reveal shared regulation only under perturbation, which is why differential co-expression methods (DiffCoEx, WGCNA) cluster genes by CORRELATED RESPONSE TO A PERTURBATION rather than baseline co-expression -- the root of our C-track (genes->latents, perturbation->content counterfactual). (2) Combinatorial optimization supplies the absorption-regime instrument: the disjoint-support 'cover the concept with complementary specialists' problem is a MAXIMUM-COVERAGE / SET-COVER problem, whose greedy (1-1/e) solution is the natural proposer for K-units -- a Level-3 methodological import never applied to SAE-latent grouping. Distributionally-robust learning (group-DRO; Mind-the-GAP 2403.09869) explains WHY the recovered unit generalizes: an absorber is a dedicated detector for one sub-context, so a complementary-coverage unit is implicitly a GROUP-OF-SPECIALISTS robust to mixing-weight shift where a single ERM hyperplane collapses -- but the SAME mechanism predicts a count-matched marginal-attribution pool is also robust, so beating one hyperplane is pooling; isolating CO-RESPONSE SELECTION means beating the count-matched pool that drops the very absorber the under-served sub-context needs.

  The insight an interpretability expert would not reach for: SAE absorption/splitting are structurally the same obstacle that (a) defeats baseline co-expression in biology and (b) makes ERM probes brittle under subpopulation shift -- so observational co-activation/geometry AND marginal-attribution selection are the wrong instruments; interventional co-response is the matched instrument, correlation is the right grouping operator only for the shared-support splitting case, and maximum-coverage set-cover is the right operator for the disjoint-support absorption case. If correct, this turns off-the-shelf public SAEs into reliable, auditable concept units with a measurable recall recovery on absorbed sub-contexts -- across spelling AND at least one semantic hierarchy. If incorrect, the honest negatives are actionable: the K-proposal step fails at the pilot (set-cover cannot surface the right group); observational co-response equals interventional co-response (no gain from intervention); the unit ties (g)/(h) (robustness is pooling; contribution reduces to absorber-recovery + measured auditability); absorption is spelling-specific (scope C3); or SAE units should be abandoned for dense surface-invariant probes.
assumptions:
- >-
  THE TWO-TRACK CLUSTERING ALGORITHM CAN PROPOSE THE RIGHT UNITS AT PROPOSAL TIME, NOT JUST FILTER THEM. Splitting families
  (shared support, positive co-response correlation) are proposable by C-track correlation-community detection; absorption
  units (disjoint support, mutually exclusive firing) are proposable ONLY by the K-track anchored greedy max-coverage, because
  their members have low pairwise correlation. The K-anchor is selected by content-response RECALL using only the counterfactual
  pairs every baseline shares -- NOT by the Chanin absorption diagnostic -- so 'unsupervised unit beats supervised oracle'
  holds and KG-edge validation against that diagnostic is non-circular. We pre-register a Tier-0 PILOT proving the K-proposal
  recovers the worked 'starts-with-L' parent+absorbers (membership precision/recall vs the diagnostic, above a random-membership
  null) BEFORE C3 relies on it; if the proposal step fails there, the K-track is reported as failing at proposal time.
- >-
  MINIMAL PAIRS ARE OBTAINABLE AT HIGH QUALITY, LOW COST, AND NON-CIRCULARLY, FOR BOTH ABSORPTION HIERARCHIES AND THE SPLITTING
  FAMILIES. Content-flips use HUMAN-WRITTEN parallel corpora where available (ParaDetox toxic<->neutral; Kaushik 2020 CAD-IMDB
  sentiment; CEBaB human aspect edits) and templated/LLM-generated pairs (OpenRouter, well under $10, LLM-judge-scored for
  content-flipped + surface-preserved with reported pass rates) for first-letter substitutions and the non-spelling hierarchy
  (numeric-quantity formats or taxonomic entities). Any activation-space content edit, if used, is derived from an INDEPENDENT
  held-out diff-of-means on DISJOINT data, never from the SAE latents being grouped, so there is no circularity.
- >-
  THE C3 SPINE IS DEMONSTRATED ON ABSORPTION AS A PHENOMENON (TWO HIERARCHIES), NOT ONE SYNTHETIC TASK, WITH A HONEST-NULL
  FALLBACK. First-letter spelling is the documented, guaranteed-signal regime; one NON-SPELLING hierarchy (numeric-quantity
  formats primary, taxonomic 'is-a-country' alternative) is promoted into the NEVER-DROPPED Tier-1a core, scored by the FORM-FREE
  probe-plus-ablation absorption diagnostic. A NON-TRIVIALITY pre-check tests whether the non-spelling parent latent actually
  has specialist-filled holes; if it does not, we report that absorption is spelling-specific, scope the C3 title claim to
  spelling-type hierarchical absorption, and route cross-concept generality through C1 (toxicity/sentiment/aspect) -- the
  load-bearing core is unaffected either way.
- >-
  THE WIN, IF IT OCCURS, IS ATTRIBUTABLE TO CO-RESPONSE SELECTION AT MATCHED POOL SIZE -- NOT TO SUPERVISION, CAPACITY, OR
  MERE POOLING. C1 count-matches observational clusters (b)/(c) to the unit's exact member count (so beating them is not a
  capacity artifact; beating the single best latent (a) is a near-foregone capacity win reported only for completeness). (f)
  is information-matched via LEACE; (g) controls label selection; (h) max-pools EXACTLY #members SCR/TPP-selected raw directions,
  holding pool SIZE fixed so the ONLY varying factor is the membership/SELECTION criterion (co-response coverage vs marginal
  attribution). The pre-registered ORDERING (f) < (g)/(h) < unit on worst-sub-context recall isolates selection; beating (f)
  is conceded as pooling; beating (g)/(h) is the signal and equals C3 absorber-recovery.
- >-
  AUDITABILITY IS MEASURED, AND THE RUN FITS A SINGLE GPU WITHIN BUDGET. Off-the-shelf Gemma Scope SAEs on Gemma-2-2b expose
  latent counterfactual responses above noise on a single GPU for a few thousand minimal pairs per concept; chosen attributes
  have enough labeled/templatable data; paired base (pt) and instruction-tuned (it) Gemma Scope SAEs are available for model-diffing.
  The auditability claim is operationalized as a MEASURED repair loop (KG-guided absorber addition -> recall recovery on a
  targeted sub-context vs a random-addition control, with bootstrap CI) plus an LLM-judge member-labeling agreement metric
  against a shuffled-label null. Absorption is more severe at WIDER SAEs and splitting at larger width, so width/layer is
  a robustness axis (16k canonical primary; 65k drop-first). The load-bearing core fits the hard per-tier GPU-hour budgets
  below.
investigation_approach: |-
  DEPTH-FIRST EXECUTION ORDER WITH HARD PER-TIER BUDGETS AND A PRE-REGISTERED DROP ORDER. Single GPU; executor wall-clock ~6 h. The run is triaged so a clean LOAD-BEARING CORE is always produced.

  TIER 0 -- DE-RISKING PILOT INCLUDING THE PROPOSAL-STEP CHECK (<= 1.0 GPU-h, NEVER dropped). (ARM A, absorption, first-letter) build content-flip pairs; run the K-track STEP-3 set-cover given ONLY the pairs and verify the proposed anchor+absorbers MATCH the Chanin 2409.14507 diagnostic's parent+absorbers (membership precision/recall above a random-membership null) -- this proves the algorithm can PROPOSE K-units before C3 relies on it; also measure complementary coverage (pooled max tracks the flip where members have holes) vs the shuffled-pair null. (ARM B, splitting, toxicity) on ParaDetox/civil_comments measure how many latents carry toxicity, whether content-response profiles are positively correlated above null, and whether the C-track community + pooled unit beats the single best latent and the matched diff-of-means on a held-out IID slice. (ARM C, NON-SPELLING absorption non-triviality) on the chosen numeric/taxonomic hierarchy, test whether a high-recall parent latent exists AND has specialist-filled holes; a clean absence is reported as 'absorption is spelling-specific'. Proceed with a regime as headline only if its pilot clears the null.

  TIER 1a -- LOAD-BEARING CORE (<= 2.75 GPU-h, NEVER dropped). (1) C1: the co-response unit beats the best raw latent (a) AND COUNT-MATCHED observational co-activation/geometry clusters (b)/(c) on classification, on first-letter (absorption) AND the best-powered toxicity family; the matched (b)/(c) comparison is foregrounded as load-bearing. (2) C3 (the spine): on first-letter AND the non-spelling hierarchy, recovered-absorber count vs the oracle pool (g) and count-matched pool (h); sliced recall on the differing sub-contexts; KG specialization-edge agreement with the (form-free) absorption diagnostic. (3) the SELECTION-CRITERION ordering (f) < (g)/(h) < unit on worst-sub-context recall on the best-powered toxicity family, with the PAIRED-bootstrap per-pair gap and its slope-vs-reweighting as the primary inferential object. (4) the degenerate-construction guard and non-triviality check on (f). HARD CHECKPOINT: if the core has not cleared, STOP expanding and write up the core + honest negatives.

  ALWAYS-RUN MINIMAL GENERALITY + AUDITABILITY DEMOS (<= 0.75 GPU-h, NEVER dropped). (i) ONE null-floored STEERING result (toxicity unit direction vs best single latent vs matched diff-of-means: on-target effect + KL on unrelated prompts, above a shuffle null). (ii) ONE null-floored MODEL-DIFFING result (does the unit detect a base-vs-it concept-usage shift more reliably than the best single latent, above a shuffle null, using paired pt/it Gemma Scope SAEs?). (iii) THE MEASURED AUDITABILITY REPAIR LOOP: pick an under-served sub-context (recall hole on (f)); read the KG to find the absorber member covering it; ADD it; MEASURE recall recovery on that sub-context (bootstrap CI) AGAINST a random-content-responsive-latent-addition control, and confirm (k) exposes no per-sub-context member to add; PLUS an LLM-judge member-labeling agreement metric (predict each member's sub-context from its logit-lens tokens + conditioning contexts) vs a shuffled-label null. All three are stated as GENERALITY/AUDITABILITY DEMONSTRATIONS, not load-bearing.

  TIER 1b -- SUPPORTING (<= 1.5 GPU-h, demotable). Sentiment (CAD-IMDB) family; shift-decomposition conditions (i) surface-only + (ii) reweighting; the label-free group-inference probe (k) and oracle group-DRO probe (j); cluster-stability bootstraps (adjusted Rand / Jaccard vs null); per-family CIs.

  TIER 2 -- STRETCH (only if Tier 1a+1b land with budget left). CEBaB restaurant aspect-sentiment family; ONE DECISIVELY-executed steering case (matched on-target effect, KL on unrelated prompts + fluency, bootstrap CIs, engaging 2505.20063/AxBench); shift condition (iii) natural domain shift; a fuller model-diffing check; the SECOND non-spelling absorption hierarchy (taxonomic if numeric was primary, or vice versa).

  PRE-REGISTERED DROP ORDER (first dropped first): 4th out-of-domain axis -> CEBaB family -> shift condition (iii) -> oracle/label-free probes (j)/(k) -> sentiment family -> decisive Tier-2 steering (keep the minimal one) -> fuller model-diffing (keep the minimal one) -> second non-spelling hierarchy. NEVER dropped: Tier-0 pilot (incl. proposal-step check + non-triviality), Tier-1a core (incl. the FIRST non-spelling absorption hierarchy), the three minimal generality+auditability demos.

  COUNTERFACTUAL SIGNAL. Encode every text and its counterfactual with a frozen Gemma Scope residual-stream SAE (layer ~12, width 16k canonical). Per latent: content-response = delta(activation) under content-flip; surface-response = delta under surface-flip; aggregate into per-latent response profiles and cover sets across contexts.

  CLUSTERING METHOD (the in-scope contribution, specified above as STEPS 1-5 + pilot). C-TRACK: positive content-response correlation affinity (DiffCoEx-style) -> Leiden communities for splitting. K-TRACK: anchored greedy maximum-coverage over content-response cover sets for absorption (anchor = highest-recall content-responsive latent chosen WITHOUT the absorption diagnostic; greedily add mutually-exclusive, precise latents covering the anchor's holes until marginal coverage gain < 0.05 with CI excluding 0). RECONCILE C-communities and K-covers (anchor each community, augment with absorbers; seed K from standalone high-recall latents) into one de-duplicated output. Finalize each candidate unit with the SINGLE ADMISSION RULE (signature C OR matched-null signature K + small-k effect-size floor + mutual-exclusivity + precision floor, AND unit-level surface invariance); report the cleared signature per concept and the false-admit rate under both nulls. Emit human-auditable unit definitions (member latents, logit-lens tokens, conditioning contexts) and directed specialization edges (a member responsive only in a sub-context = absorbed/split child) = a feature-level knowledge graph.

  WORKED EXAMPLES. Toxicity unit (splitting, C-track): members = {profanity/slur latent, demeaning-insult latent, aggressive-imperative latent}; under ParaDetox detox all three drop together (signature C); pooled max tracks toxicity; pooled surface-response to paraphrase ~ 0. First-letter unit (absorption, K-track): anchor = general 'starts-with-L' latent (silent on 'lion'/'London'); greedy adds 'lion'-absorber then 'London'-absorber (each fires only in its sub-context, Jaccard ~ 0 with the anchor); pooled max covers 'starts-with-L' everywhere (signature K); pooled surface-response ~ 0. Numeric unit (non-spelling absorption, K-track): anchor = general 'numeric token' latent (holes on years/percentages); greedy adds a 4-digit-year absorber and a percentage absorber.

  BASELINES (matched baselines are primary). (a)-(k) as in the glossary; (b)/(c) COUNT-MATCHED to the unit for C1; (h) count-and-pool-matched for the selection-criterion isolation; (j)/(k) for the robustness bounds.

  EVAL -- LOAD-BEARING BACKBONE (reported regardless of dense-probe competitiveness): (1) co-response units have low Jaccard with co-activation/geometry clusters above the stability/shuffled-pair null; (2) units win specifically on the differing members -- sliced RECALL on the sub-contexts where the best latent / count-matched observational clusters / the oracle pool (g) / the count-matched pool (h) have holes, including absorbers (g)/(h) drop, on BOTH absorption hierarchies; (3) KG specialization edges agree with the form-free absorption diagnostic. EVAL -- CLASSIFICATION + SUPPORTING ROBUSTNESS: unit-pooled activation (max/sum over members) as classifier on IID and under the decomposed shifts; report F1/AUC AND worst-sub-context recall; the SELECTION-CRITERION prediction is the ORDERING (f) < (g)/(h) < unit with the unit-minus-(g)/(h) PAIRED gap GROWING in reweighting magnitude (slope CI primary). Robustness BOUNDS: unit approaches (j) without labels and is competitive-or-better than (k) while auditable. EVAL -- MEASURED AUDITABILITY: KG-guided absorber-addition recall recovery vs random-addition control (bootstrap CI); LLM-judge member-labeling agreement vs shuffled-label null. DEGENERATE-CONSTRUCTION GUARD applied throughout. STATISTICS: per-family paired-bootstrap CIs PRIMARY; cross-family aggregate DESCRIPTIVE; a-priori n_min=150 with stratified collection; cluster-stability bootstrap (adjusted Rand / Jaccard) vs shuffled-pair null.

  STEERING (Tier 2, ONE decisive case; minimal version always runs) and MODEL-DIFFING (minimal always runs; fuller Tier 2) as before -- generality demonstrations, not load-bearing, each null-floored.

  HONEST FAILURE-MODE REPORTING. The K-proposal set-cover failing to recover the worked unit at the pilot (proposal-step failure); the non-spelling parent having no specialist-filled holes (absorption spelling-specific -> scope C3); dependence on counterfactual quality (pass rates); concepts with no surface-invariant co-responding/complementary group; regimes where co-response collapses to co-activation (no gain over observational); the unit tying the count-matched pools (g)/(h) on sliced recall (robustness is pooling -> contribution reduces to absorber-recovery + measured auditability); the label-free group-inference probe (k) beating the unit on recall (loss-reweighting wins for pure robustness); the dense surface-invariant probe matching the unit on sliced recall (invariance supervision suffices; grouping adds only auditability); the oracle pool (g) tying the unit (selection not co-response structure); the reweighting test void because (f) does not collapse; the KG-guided repair not beating random-addition (auditability buys no fix); co-response too noisy to cluster (ARI ~ null); compute/SAE-width sensitivity; bias_in_bios boundary-null.
success_criteria: |-
  CONFIRMED if, pre-registered in this nesting (LOAD-BEARING CORE first):
  LOAD-BEARING (the paper stands on these alone, even if every robustness comparison ties and aggregate F1 ties the dense probe): (1) the Tier-0 pilot confirms above-null co-response structure AND the K-track PROPOSAL step recovers the known first-letter parent+absorbers (membership precision/recall above a random-membership null), with the toxicity arm also showing a pooled IID edge over the best single latent and the matched diff-of-means; (2) C1 -- the unit beats the best raw single latent AND COUNT-MATCHED observational co-activation/geometry clusters on classification on first-letter AND the best-powered toxicity family (matched-(b)/(c) per-family bootstrap CI excludes 0); the single-best-latent comparison is reported only for completeness; (3) C3 (the spine) -- on first-letter AND at least one NON-SPELLING absorption hierarchy the unit recovers absorber latents the oracle pool (g) and count-matched pool (h) drop, wins on the differing sub-contexts (paired-bootstrap gap CI excludes 0, sized to n_min=150), and its KG specialization edges agree with the (form-free) absorption diagnostic (2409.14507).
  SUPPORTING (strengthen the paper; honest nulls here do not sink it): (4) C2 + SELECTION-CRITERION ISOLATION -- the unit matches-or-beats (g) and (h) on classification AND shows the ORDERING (f) < (g)/(h) < unit on worst-sub-context recall, with a POSITIVE unit-minus-(g)/(h) PAIRED gap whose slope-vs-reweighting-magnitude CI excludes 0 (the unit-minus-(f) gap alone is conceded as pooling); (5) ROBUSTNESS BOUNDS -- the unit APPROACHES the oracle group-DRO probe (j) WITHOUT labels and is competitive-or-better than the label-free group-inference probe (k) while uniquely auditable; aggregate F1 vs (f) may tie; (6) MEASURED AUDITABILITY -- the KG-guided absorber-addition repair recovers recall on the targeted under-served sub-context with a bootstrap-CI gain over a random-content-responsive-latent-addition control, (k) cannot localize the fix, and LLM-judge member-labeling agreement exceeds a shuffled-label null; (7) ADMISSION + CONSTRUCTION INTEGRITY -- false-admit rate <= 0.05 under BOTH nulls; cluster assignments stable across bootstrap resamples (adjusted Rand/Jaccard above null); sub-contexts defined from independent labels frozen first, under-served determined on (f) alone, non-triviality check confirms (f) genuinely collapses; per-family CIs PRIMARY, cross-family DESCRIPTIVE.
  GENERALITY (always produced via the truncation fallback, never load-bearing): one null-floored steering result and one null-floored model-diffing result; the decisive Tier-2 steering case is confirmatory if it lands.
  HONEST NEGATIVES, each publishable: the K-track proposal step fails to recover the worked unit at the pilot (set-cover cannot surface disjoint-support absorbers); the non-spelling parent has no specialist-filled holes so absorption is spelling-specific (C3 scoped to spelling-type absorption, generality routed through C1); co-response grouping ties observational grouping (no gain from intervention); the unit ties (g)/(h) on sliced recall (robustness is pooling -> contribution reduces to absorber-recovery + measured auditability); (k) beats the unit on recall (loss-reweighting wins for pure robustness, unit still delivers the measured auditable repair); the dense surface-invariant probe matches the unit on sliced recall (grouping then contributes only auditability + the knowledge graph); the oracle pool (g) ties the unit (selection not co-response structure); the gap does NOT concentrate on the reweighting component or (f) does not collapse (supporting mechanism falsified/void, core unaffected); the KG-guided repair does not beat random-addition (auditability buys no measurable fix); co-response too noisy to cluster (ARI ~ null). bias_in_bios is a pre-registered boundary-null, not method failure.
related_works:
- >-
  Maximum-coverage / set-cover and the greedy (1-1/e) algorithm (Nemhauser, Wolsey, Fisher 1978; Feige 1998): the classic
  combinatorial-optimization instrument for selecting a small set of complementary subsets that jointly cover a universe.
  We transfer it as the K-TRACK PROPOSER: anchor on a parent latent, then greedily add mutually-exclusive latents whose content-response
  cover sets fill the anchor's holes. To our knowledge maximum-coverage has never been used to GROUP SAE latents -- and it
  is exactly the operator the disjoint-support absorption regime needs, where pairwise-affinity clustering provably cannot
  propose the right group.
- >-
  Differential co-expression / perturbation co-response module discovery (DiffCoEx, BMC Bioinformatics 2010; WGCNA): cluster
  genes by their CORRELATED RESPONSE TO A PERTURBATION rather than baseline co-expression, because co-regulated genes are
  often not co-expressed at baseline. This is the root of our C-TRACK (correlation-community detection on content-response
  profiles for the splitting regime); to our knowledge never applied to SAE/LLM features. Our novel claim is that the same
  baseline-vs-perturbation distinction explains and repairs SAE splitting, AND that the disjoint-support absorption case needs
  a SEPARATE set-cover operator, not correlation.
- >-
  A is for Absorption (Chanin et al., 2409.14507, NeurIPS 2025): a SUPERVISED DIAGNOSTIC -- identify the parent latent by
  max encoder-cosine with an LR probe, find the absorbing latent by ablation on the relevant logit. It DETECTS absorption
  on individual latents and demonstrates it empirically almost only on first-letter spelling (running non-spelling example:
  'short'/'starts-with-S'); it does not GROUP parent+absorbers into a usable unit, nor test absorption in semantic hierarchies.
  We use the FORM-FREE version (probe + ablation, domain-agnostic) ONLY to SCORE our already-formed unit's KG edges (never
  to form units, so non-circular), as a partial oracle for the pilot, and we add a novel empirical test of whether absorption
  generalizes to a non-spelling (numeric/taxonomic) hierarchy.
- >-
  Feature Hedging: Correlated Features Break Narrow SAEs (Chanin, Dulka, Garriga-Alonso, 2505.11756): ABSORPTION learns gerrymandered
  latents (worse at WIDER SAEs, parent->child hierarchy, mutually-exclusive firing) vs HEDGING merges correlated features
  into a SINGLE polysemantic latent (worse at NARROWER SAEs). We scope grouping to splitting+absorption (a hedged single latent
  is not groupable) and treat correlation/hierarchy as the mechanistic cause our interventional probe exposes -- correlation
  for shared-support splitting, set-cover for disjoint-support absorption.
- >-
  AxBench (Wu et al., ICML 2025 spotlight, 2501.17148) and Negative Results for SAEs on Downstream Tasks (DeepMind 2025):
  difference-in-means is the strongest concept-detection method and raw-latent SAEs are not competitive; this sets the dense-probe
  bar. We deliberately do NOT stake the load-bearing claim on beating it: C3 absorber-recovery is measured against SAE-SELECTION
  baselines (a)/(g)/(h), and aggregate-F1 parity with the surface-invariant dense probe (f) is pre-registered as acceptable.
- >-
  Sparse Autoencoders Do Not Find Canonical Units of Analysis (Bussmann et al., ICLR 2025, 2502.04878): uses SAE stitching
  and meta-SAEs to argue SAEs do not learn canonical units; its remedy is geometric/training-based. We propose a BEHAVIORAL
  unit defined by counterfactual co-response (correlation OR set-cover) and unit-level surface invariance, evaluated on downstream
  classification + steering + model-diffing, with no retraining.
- >-
  Subspace-Aware SAEs (SASA, 2606.06333, 2026), Matryoshka SAEs and Concept-Bottleneck SAEs (CVPR 2026), AbsTopK SAE, Group
  SAEs (negative results): all MODIFY SAE TRAINING -- decoder subspaces, nested dictionaries, concept bottlenecks, hard-thresholding,
  grouping losses -- to reduce absorption/splitting at training time. Our grouping is POST-HOC over a FROZEN public SAE's
  discrete latents, defined by interventional co-response, requiring no retraining and yielding an auditable feature-level
  knowledge graph.
- >-
  SHIFT / SCR / TPP SAE evaluation (Marks et al. 2024; Karvonen et al. 2411.18895): SELECT individual SAE latents by ranking
  causal effect on a concept probe (top-N), then ablate the set; they do NOT cluster latents by interventional co-response.
  This is exactly our supervised ORACLE-POOL baseline (g) and, count-matched, the pool (h); a latent firing only in a narrow
  sub-context (an absorber) has low marginal attribution and is silently dropped -- the specific gap our co-response set-cover
  fills, and the quantity the unit-minus-(g)/(h) sliced-recall gap measures.
- >-
  Co-activation feature families and graph-regularized SAEs (Disentangling Dense Embeddings 2408.00657; GSAE; Sparse Feature
  Coactivation 2506.18141): group SAE features by OBSERVATIONAL co-activation/geometry. By construction these cannot group
  a concept's absorbed/split latents (mutually exclusive in firing); for C1 we COUNT-MATCH them to the unit's member count
  so a unit win cannot be a capacity artifact. We use the opposite, INTERVENTIONAL signal and demonstrate the structural blind
  spot via low-Jaccard + sliced-recall wins.
- >-
  JTT (2107.09044), GEORGE / No Subclass Left Behind (2011.12945), EIIL (2010.07249), LfF (2007.02561): the label-free worst-group-robustness
  family -- infer GROUPS OVER EXAMPLES and RETRAIN with reweighted / group-DRO loss. Our route is orthogonal: we group FEATURES
  (discrete SAE latents) by interventional co-response, never retrain, and the recovered absorbers ARE the inferred sub-context
  specialists -- auditable. We add an oracle group-DRO probe (j, true sub-context labels = upper bound) and a label-free group-inference
  probe (k) as direct robustness baselines for the SUPPORTING result.
- >-
  Diverse Prototypical Ensembles (2505.23027): trains an ensemble of N diverse prototypes per class on FROZEN DENSE features
  with a diversity loss + bagging to capture subpopulation-specific patterns without group labels. The closest 'ensemble-of-specialists
  for subpopulation shift', but it TRAINS learnable prototype vectors on dense representations; we group pre-existing DISCRETE
  SAE latents by interventional co-response with no training, yielding auditable concept atoms (not opaque prototypes) and
  a feature-level knowledge graph.
- >-
  Group-DRO and subpopulation-shift robustness (Sagawa et al.; Mind the GAP: Group-Aware Priors, 2403.09869): a single ERM
  model collapses on under-served minority subgroups under mixing-weight shift; group-aware methods recover worst-group performance.
  We do NOT propose a new DRO method or theorem; we BORROW this as the a-priori mechanism explaining why a group-of-specialists
  unit out-generalizes a single hyperplane -- and use the SAME mechanism to predict a count-matched marginal-attribution pool
  is also robust, which is why selection is isolated against THAT pool, not the hyperplane.
- >-
  Discovering Concept Directions from Diffusion-based Counterfactuals via Latent Clustering (CDLC, 2505.07073; Pattern Recognition
  Letters 2025): clusters latent DIFFERENCE vectors from factual + diffusion-generated counterfactual IMAGE pairs into global
  class-specific concept DIRECTIONS (vision). Closest 'cluster counterfactual differences' template, but on a different substrate
  (one continuous direction per class in a diffusion latent space). We cluster DISCRETE SAE dictionary latents on a frozen
  LLM by their co-response PROFILES into auditable MULTI-MEMBER units, with a SET-COVER track for the absorption regime CDLC
  has no analogue for.
- >-
  LEACE (Belrose et al., 2306.03819) and Counterfactual Invariance to Spurious Correlations (Veitch et al., NeurIPS 2021,
  2106.00545): perfect linear concept erasure / MMD-based counterfactual-invariance regularizer. We erase the surface-flip
  direction to build the surface-invariant probe (f) -- a strong, principled non-SAE single hyperplane; beating it is conceded
  as a pooling effect, with selection isolated against the count-matched pools (g)/(h).
- >-
  Counterfactually-Augmented Data (Kaushik, Hovy, Lipton, ICLR 2020), CEBaB (Abraham et al., NeurIPS 2022, 2205.14140), ParaDetox
  (s-nlp, ACL 2022): human-written counterfactual minimal pairs for sentiment, aspect concepts, and toxicity. We use these
  for non-circular content-flips and independent sub-context labels for the degenerate-construction guard, not as the grouping
  method.
- >-
  Domain-Filtered Knowledge Graphs from SAE Features (2604.23829): builds an internal knowledge graph from SAE features via
  contrastive corpus filtering, co-occurrence, decoder geometry -- purely OBSERVATIONAL. Our feature-level knowledge graph
  is built from INTERVENTIONAL co-response/set-cover grouping, so its edges encode conditioning environments and specialization
  (absorbed/split children) invisible to observational co-occurrence -- and we MEASURE its utility via the auditability repair
  loop.
inspiration: >-
  A triple cross-field transfer, now with the named algorithm specified track-by-track. The SPLITTING-regime grouping (C-track)
  is a Level-3 methodological import from systems biology's differential co-expression / perturbation co-response module discovery
  (DiffCoEx, WGCNA): cluster units by CORRELATED RESPONSE TO A PERTURBATION, not baseline co-expression, because co-regulated
  genes are frequently not co-expressed until perturbed (genes->SAE latents, perturbation->content counterfactual). The crucial
  reviewer-prompted addition: correlation cannot group the ABSORPTION regime, because absorbers are mutually exclusive in
  firing and respond on disjoint supports -- so the K-track imports a SECOND, distinct instrument from combinatorial optimization,
  the MAXIMUM-COVERAGE / SET-COVER greedy (Nemhauser-Wolsey-Fisher; Feige): anchor on the highest-recall parent latent, then
  greedily add complementary specialists that cover its holes. The SUPPORTING robustness mechanism is a Level-1/2 import from
  distributionally-robust learning (group-DRO; Mind-the-GAP 2403.09869) and the label-free worst-group-robustness subfield
  (JTT, GEORGE, EIIL, LfF, Diverse Prototypical Ensembles): a single ERM hyperplane collapses on under-served minority subgroups
  under mixing-weight shift, whereas a union of specialists is robust -- and an absorber is precisely a specialist for one
  latent sub-context; because the SAME mechanism predicts a count-matched marginal-attribution pool is also robust, isolating
  CO-RESPONSE SELECTION means beating that pool, the SAME quantity as C3 absorber-recovery. These fuse with (i) causal ML's
  counterfactual invariance (Veitch 2021) and concept-erasure (LEACE, Belrose 2024) for the conceded surface-invariant baseline;
  (ii) NLP minimal-pair counterfactuals (ParaDetox, Kaushik 2020 CAD, CEBaB aspects) for non-circular perturbations and independent
  sub-context labels. The unifying insight an interpretability expert would not reach for: SAE splitting and absorption are
  TWO structurally different obstacles -- shared-support correlation (matched by DiffCoEx-style co-response correlation) vs
  disjoint-support coverage (matched by set-cover) -- the same dichotomy that distinguishes co-expression modules from complementary-pathway
  gene sets in biology, and the recovered absorbers ARE the latent subpopulations a robust classifier needs.
terms:
- term: Two-track clustering algorithm (the named contribution)
  definition: >-
    The grouping procedure: a C-TRACK that clusters content-responsive latents by positive content-response correlation (Leiden
    communities) for the SPLITTING regime where members share firing support, and a SEPARATE K-TRACK anchored greedy maximum-coverage
    for the ABSORPTION regime where members are mutually exclusive in firing and respond on disjoint supports (so correlation
    cannot propose them). C-communities and K-covers are reconciled into one de-duplicated output and filtered by the single
    admission rule.
- term: Cover set of a latent
  definition: >-
    C_l = the set of content-flip pairs whose flip latent l reliably and precisely tracks: r_l(p) above a response threshold,
    the latent fires on the content-on member, and the latent's content-response precision on its own firing support is >=
    0.7. The K-track operates on these cover sets; coverage-complementarity is defined as set intersection with an anchor's
    hole set, never as a vague pairwise affinity.
- term: Anchor-based greedy maximum-coverage (K-track)
  definition: >-
    The absorption-regime proposer. ANCHOR = the content-responsive latent with the highest cover-set size (highest recall
    of the concept's content flips), chosen using ONLY the counterfactual pairs (NOT the Chanin absorption diagnostic). HOLES
    = pairs the anchor does not cover (the absorbed sub-contexts). GREEDY: repeatedly add the latent covering the most uncovered
    holes subject to mutual-exclusivity (firing Jaccard<0.1), precision>=0.7, and a marginal coverage-gain floor (>=0.05 with
    bootstrap CI excluding 0). Recovers {general latent, per-sub-context absorbers} by construction, which correlation-merging
    clustering cannot.
- term: Proposal-step pilot validation
  definition: >-
    A Tier-0, never-dropped check that the K-track set-cover, given only content-flip pairs, RECOVERS the parent+absorbers
    the supervised Chanin 2409.14507 diagnostic identifies (membership precision/recall above a random-membership null) --
    proving the algorithm can PROPOSE absorption units before C3 relies on them. A failure here is reported as a proposal-step
    failure (an honest negative).
- term: Non-spelling absorption testbed (C3 generality)
  definition: >-
    A second absorption hierarchy promoted into the never-dropped Tier-1a core -- a NUMERIC-QUANTITY hierarchy (general numeric-token
    latent with year/percentage/date absorbers) as primary, or a TAXONOMIC 'is-a-country' hierarchy as the pre-registered
    alternative -- scored by the FORM-FREE (domain-agnostic) probe-plus-ablation absorption diagnostic. It moves C3 from one
    synthetic spelling task to absorption as a phenomenon AND is a novel empirical test of whether absorption generalizes
    beyond spelling, with a honest-null fallback (if no specialist-filled holes exist, absorption is reported spelling-specific
    and C3 is scoped accordingly).
- term: Feature absorption
  definition: >-
    A sparsity-induced failure (Chanin 2409.14507, 2505.11756) requiring a parent->child hierarchy: the more specific child
    latent suppresses the firing of the more general parent latent, which then has unpredictable holes. Parent and child are
    MUTUALLY EXCLUSIVE in firing (gerrymandered latents); absorption is worse at WIDER SAEs and documented empirically almost
    only on first-letter spelling.
- term: Feature splitting vs feature hedging
  definition: >-
    Splitting = one concept fragments across MANY latents (worse at larger width); sub-latents co-respond POSITIVELY to a
    content flip and share support -- the C-track (correlation) target. Hedging (Chanin 2505.11756) = a narrow SAE MERGES
    correlated features into a SINGLE polysemantic latent (worse at narrower width); a hedged single latent is NOT groupable
    but explains why inter-latent correlation exists.
- term: Interventional co-response (grouping criterion)
  definition: >-
    Latents belong to the same concept unit if they jointly track the content perturbation across contexts, even if their
    baseline activations never co-occur. Realized in two signatures via two operators: positive correlation of content-response
    profiles (signature C, splitting, C-track) and complementary coverage of an anchor's holes (signature K, absorption, K-track
    set-cover).
- term: Count-matched C1 comparison
  definition: >-
    For C1 the observational co-activation/geometry clusters (b)/(c) are CUT to the unit's exact member count k (top-k members
    by the same pooling rule), so a unit win is at matched pool size and cannot be a capacity/pooling artifact -- it shows
    co-response SELECTS the right members. Beating the single best raw latent (a) is a near-foregone capacity win reported
    only for completeness.
- term: Measured auditability repair loop
  definition: >-
    An always-run demo that operationalizes auditability as a result: pick an under-served sub-context (recall hole on the
    dense probe), read the knowledge graph to identify the absorber covering it, ADD it, and MEASURE recall recovery on that
    sub-context (bootstrap CI) against a random-content-responsive-latent-addition control, confirming a retrained label-free
    probe (k) exposes no per-sub-context member to add. Paired with an LLM-judge member-labeling agreement metric (predict
    each member's sub-context from logit-lens tokens + contexts) vs a shuffled-label null.
- term: Surface-invariant matched probe (baseline f, single hyperplane)
  definition: >-
    A counterfactually-matched diff-of-means/linear probe on content-flip residual deltas, made surface-invariant by ERASING
    the surface-flip direction via LEACE / mean-projection (Belrose 2024). A SINGLE hyperplane; the unit beating it is conceded
    to be a POOLING effect, not selection evidence.
- term: Supervised oracle pool (g) and count-and-pool-matched probe (h)
  definition: >-
    (g) pools the top-N SAE latents selected by SCR/TPP probe-attribution causal effect; because it ranks by MARGINAL attribution
    it silently drops absorbed latents firing only in narrow sub-contexts. (h) max-pools EXACTLY #members raw residual directions
    selected by the SAME SCR/TPP attribution, holding pool SIZE fixed so the only varying factor vs the unit is the membership/SELECTION
    criterion (co-response coverage vs marginal attribution). The unit-vs-(g)/(h) sliced-recall comparison is the selection-isolating
    headline test and equals C3 absorber-recovery.
- term: Oracle group-DRO probe (j) and label-free group-inference probe (k)
  definition: >-
    (j) a dense probe trained with a group-DRO objective using the TRUE independent sub-context labels = worst-group-robustness
    UPPER BOUND; the unit is predicted to APPROACH it without using labels. (k) a dense probe made group-robust WITHOUT sub-context
    labels via JTT-style high-loss upweighting or GEORGE-style representation clustering + group-DRO; like the unit it uses
    no sub-context labels, but it reweights EXAMPLES and retrains, whereas the unit groups FEATURES, is training-free, and
    is auditable.
- term: Selection-criterion isolation
  definition: >-
    The pre-registered ORDERING (f) single hyperplane < (g)/(h) count-matched marginal-attribution pools < unit co-response
    pool on worst-sub-context recall. The unit-vs-(g)/(h) comparison holds POOL SIZE FIXED and varies ONLY the membership/SELECTION
    rule (co-response set-cover vs marginal SCR/TPP ranking); both pool, so it isolates SELECTION. The structural claim reduces
    to: co-response COVERAGE admits the absorber marginal-attribution ranking drops -- the SAME quantity as C3 absorber-recovery.
    Beating (f) is conceded as pooling.
- term: Single unit admission rule
  definition: >-
    A proposed unit is admitted iff it clears signature C (within-unit content-response correlation > 95th-pct shuffled-pair
    null) OR signature K (matched best-of-random-k coverage null + the small-k absolute effect-size floor >=0.05 with bootstrap
    CI excluding 0, with mutual-exclusivity Jaccard<0.1 and per-member precision>=0.7), AND its pooled surface-response is
    not above the shuffled-surface null. The cleared signature is reported per concept and the false-admit rate under both
    nulls (target <=0.05). The rule FILTERS units the two-track algorithm PROPOSES.
- term: Load-bearing core
  definition: >-
    The minimal pre-registered result set the paper stands on regardless of robustness outcomes: pilot (incl. K-proposal recovery
    + non-triviality) + count-matched C1 + C3 absorber-recovery vs (g)/(h) + KG-edge agreement on first-letter AND one non-spelling
    absorption hierarchy. Measured against SAE-selection baselines, not the dense-probe aggregate-F1 bar, so it does not depend
    on out-classifying a strong dense probe.
summary: >-
  SAE latents encoding one concept are often mutually exclusive in firing (feature absorption and splitting), so observational
  co-activation, decoder geometry, and marginal-attribution selection all structurally miss the right members. We group frozen-SAE
  latents by how they jointly track a content counterfactual via a two-track algorithm -- correlation-community detection
  for shared-support splitting, and an anchored greedy SET-COVER for disjoint-support absorption (which correlation cannot
  even propose) -- producing training-free, auditable multi-member units. The load-bearing result is that the unit beats raw
  latents and COUNT-MATCHED observational clusters and recovers the absorbers a count-matched marginal-attribution selection
  drops on BOTH first-letter spelling AND one non-spelling hierarchy (KG edges agreeing with the absorption diagnostic); a
  measured auditability repair loop and worst-sub-context robustness approaching an oracle group-DRO probe without labels
  are supporting results.
_relation_rationale: >-
  Same two-track frame; pivots headline to measured auditability and re-scopes non-spelling absorption to homographs.
_confidence_delta: decreased
_key_changes:
- >-
  PIVOTED the LOAD-BEARING HEADLINE to MEASURED AUDITABILITY (KG-guided recall-repair loop + LLM member-labeling), since the
  unit beats NO non-SAE dense probe on classification but uniquely offers editable, localized repair a probe structurally
  lacks (reviewer scope MAJOR); mandated expanding it (more concepts/sub-contexts + one downstream task where the localized
  fix matters).
- >-
  EXPOSED and mandated fixing the taxonomic UNIT/SPECIALIST CONFLATION: the classification unit [3792,4697,9339,8442] uses
  the low-precision (0.35), NON-corroborated Georgia absorber 4697, while the diagnostic-corroborated precision-passing Georgia
  absorber is 16009 (prec 0.955); rebuild the unit from non_triviality_passing_absorbers and report PER-EDGE KG-agreement
  (Georgia 0.0, Jordan 0.955, US 0.0). Corroboration currently holds only for the descriptive Jordan edge (n=124<150).
- >-
  REFRAMED non-spelling 'generalization' as a HOMOGRAPH/POLYSEMY phenomenon (absorption-type slices = exactly Georgia + Jordan,
  the ambiguous homographs with parent recall holes), not broad taxonomic absorption (reviewer scope MAJOR).
- >-
  TIGHTENED the first-letter primary endpoint to the PER-LETTER JOINT (E1 AND selection) = 2/5 (T,D); annotated letter I as
  a selection win WITHOUT a confirmed absorption mechanism (E1 fails, 0%-corpus anchor); renamed/reconciled the over-aggregating
  verdict (reviewer rigor MAJOR).
- >-
  ADDED NON-RANDOM label-free selection controls (S-rec top-k by content-flip recall, S-prec top-k by firing precision, S-mag
  top-k by mean response magnitude, count-matched to k); the set-cover-SPECIFIC claim now requires beating THESE, not just
  the easy RE-k random pool (which sits at/below the best single latent) (reviewer methodology MINOR).
- >-
  REFRAMED the router as a SCREENING HEURISTIC WITH MEASURED ERROR: rule derived on 12 spelling/taxonomic/toxicity concepts,
  prospectively tested on only 3 (1/3 hits, LOO 0.733); lead with the COMBINED rule (low firing-Jaccard AND high parent recall-hole);
  stop listing derivation concepts as prospective (reviewer evidence MINOR).
- >-
  Mandated the K-track no longer prefer high-coverage/low-precision absorbers over high-precision diagnostic-corroborated
  ones: add a precision-gate/precision-weighted coverage objective and apply the precision floor on a HELD-OUT fold; report
  held-out per-member subctx_precision and the fold each gate is evaluated on (reviewer rigor MINOR).
- >-
  Mandated reporting the COMPACT named-member-only unit AUC alongside the 15-wide max-pool and the fraction of the 15 members
  that receive a confident member-label, restricting the 'auditable' claim to the characterized subset (reviewer rigor MINOR).
- >-
  Mandated stripping rebuttal/iteration/infrastructure scaffolding from the paper and moving reproducibility notes to an appendix;
  retained the citation-audit fixes (Chanin -> NeurIPS 2025; AxBench/SAEBench -> ICML 2025; Winnicki observational-KG contrast)
  (reviewer presentation MINOR).
- >-
  Retitled to an auditability-first, absorption-regime-repair + firing-Jaccard-plus-recall-hole-router framing; model-diffing
  kept as a confound-bounded null limitation (not promoted).
- >-
  Confidence DECREASED: the lead non-spelling headline was overstated (classifier != corroborated specialists), classification
  gains are narrow/within-SAE (per-letter joint 2/5, beats no dense probe), and the set-cover-specific selection claim is
  NOT yet isolated from sensible label-free selection.
relation_type: evolution
</hypothesis>

<artifact_direction>
Make this direction concrete and actionable. Keep the same type and respect dependencies.

id: experiment_iter4_dir4
type: experiment
objective: >-
  FIRST-LETTER SELECTION ISOLATION (M5) + ENDPOINT HONESTY (M4) + UNIT TRANSPARENCY (M7-compact). Isolate the two-track set-cover
  from sensible label-free selection by adding NON-RANDOM, count-matched controls (top-k by content-flip recall / firing precision
  / response magnitude), so 'unit beats RE-k' no longer merely restates 'good selection beats random/best-single'; report
  the per-letter JOINT (E1 AND selection) explicitly and rename the over-aggregating verdict; and disentangle the 15-wide
  max-pool from the compact named unit by reporting the compact (named-members-only) unit's AUC alongside the 15-wide pool.
approach: >-
  Re-run the first-letter two-track pipeline from art_RidEJtBC7gPT; for code reuse read the iter-3 first-letter re-run from
  its run-tree workspace path (3_invention_loop/iter_3/gen_art/gen_art_experiment_1/method.py and method_out.json) — SAE/loader/hook/firing
  identical; gate on reconstruction cosine>0.9. (1) M5 NON-RANDOM CONTROLS: from the cover-eligible set E, build three label-free,
  count-matched-to-k=|unit| selectors — (S-rec) top-k by content-flip recall, (S-prec) top-k by firing precision, (S-mag)
  top-k by mean response magnitude — max-pool each identically to the unit, and on every letter report held-out AUC plus the
  paired-bootstrap AUC-DIFFERENCE CI (B>=10,000, pair-cluster resampling) for unit-minus-each; RETAIN RE-k as the demoted
  floor. The set-cover-specific selection claim is ESTABLISHED only where the unit beats S-rec/S-prec/S-mag with CI excluding
  0; where it does not, scope the claim to 'cover-based eligibility + sensible selection'. Report a per-letter table of which
  controls the unit beats. (2) M4 ENDPOINT: compute and report the PER-LETTER JOINT of E1 (K-track recovers diagnostic parent
  + >=2 absorbers above the random-membership null) AND the selection test (unit AUC significantly above BOTH (h) AND the
  M5 non-random selectors), giving the honest intersection (currently {T,D}=2/5 vs RE-k; recompute vs the M5 bar). RENAME
  the emitted verdict so it does NOT imply mechanism+selection co-occur on 3 letters, and explicitly ANNOTATE letter I as
  'selection win WITHOUT confirmed absorption mechanism' (E1 fails: recall-argmax anchor 1227 fires 0% on corpus). Keep the
  unsupervised parent-validation (firing-floor) step that rejects the spurious I anchor. (3) M7 COMPACT-vs-15-WIDE: report
  the AUC of the COMPACT unit (anchor + named precision-passing absorbers only, ~4-5 members) ALONGSIDE the 15-wide max-pool
  on every letter, with their AUC-difference CI, to show whether the named structure carries the classification signal or
  the strong AUC reflects the wide pool; tie this to the member-labeling fraction reported in the auditability-expansion experiment.
  (4) Use the 1,700-pair re-judged surface superset (art_YwjLYapklnVk) for the admission surface-invariance gate; report the
  false-admit rate under the matched random-k null. Move the torch 2.8+cu128 / AUC-drift reproducibility note to a repro appendix
  block, not the headline. Memory-safe batching; gradual scaling (mini letter-L -> full). Emit method_out.json (exp_gen_sol_out
  schema) with per-letter AUC for unit/compact-unit/15-wide/a/b/c/h/RE-k/S-rec/S-prec/S-mag, all AUC-difference CIs, the per-letter
  joint (E1 AND selection) table, the renamed reconciled verdict, admission stats, and per-example held-out predictions. Validate
  full/mini/preview <100MB.
depends_on:
- id: art_dpYpjSn2Xvg3
  label: dataset
  relation_type:
  relation_rationale:
- id: art_YwjLYapklnVk
  label: surface-control
  relation_type:
  relation_rationale:
- id: art_RidEJtBC7gPT
  label: method
  relation_type:
  relation_rationale:
- id: art_I2MrezW41iQo
  label: diagnostic
  relation_type:
  relation_rationale:
</artifact_direction>

<dependencies>
Completed artifacts this artifact can use during execution.

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
out_expected_files:
- research_out.json
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
out_expected_files:
- research_out.json
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
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json
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
id: art_YwjLYapklnVk
type: dataset
title: 'Surface-Invariance Pair Superset: First-Letter 1,700 + Toxicity 1,631 Pairs'
summary: |-
  Drop-in SUPERSET of the two iter-1 surface-flip pair sets that the next iteration's Step-5 admission AND-gate consumes to estimate the shuffled-surface null (a candidate SAE unit is admitted only if its pooled surface-response is NOT above this null). Emits ONLY the surface-pair superset; the frozen iter-1 content_flip/content_pair/classification/corpus rows stay canonical at their iter-1 paths and are merged by metadata_pair_id/metadata_record_type. Pure CPU/data (no GPU, no SAE, no activations).

  full_data_out.json (exp_sel_data_out schema, PASSED) has 7 dataset groups / 5,031 surface rows: five first_letter_spelling_{L,O,T,I,D} groups (1,700 pairs = 3,400 rows; var_a/var_b linked by metadata_pair_id; int fold 0-4 by target_word) and paradetox + civil_comments groups (1,631 one-row toxicity pairs; input=source toxic, metadata_text_paired=toxic paraphrase; train/val/test fold by source, 0 cross-fold leakage). Both concepts exceed the >=1,500 target.

  FIRST-LETTER (concept 'starts-with-X'): 590 -> 1,700 pairs (340/letter, balanced across the 5 iter-1 carriers), built deterministically ($0) from the iter-1 Pile occurrence_tables (unsloth/gemma-2-2b get_alpha_tokens slot-eligible single-token words); authoritative structural validator = 0 violations. TOXICITY (concept 'toxic'): 546 -> 1,631 pairs (+1,085 new: civil 803, paradetox 282) generated by openai/gpt-4o-mini and gated by token Jaccard<0.6 AND norm char-change>0.25 (strict, verbatim from iter-1), then accepted by an INDEPENDENT family judge anthropic/claude-haiku-4.5 (toxicity_constant AND meaning_preserved AND surface_changed AND fluent). civil-origin new pairs carry real sub-attribute floats; per-sub pairs: insult 370, obscene 226, sexual_explicit 216, identity_attack 211, threat 205, severe_toxicity 12.

  Circularity fixed (iter-1 used the SAME gpt-4o-mini to generate AND judge toxicity, and gemini-3.1-flash-lite for first-letter): every new toxicity pair is born with a claude-haiku-4.5 label; a stratified sample of both concepts is re-judged by families different from both generator and original judge. Reportable findings: claude confirms 465/546 = 85.2% of gpt-4o-mini-accepted toxicity originals; toxicity cross-judge claude-vs-gemini raw 0.940 / Cohen kappa 0.263 (n=399, high base rate); first-letter independent audit claude pass-rate 0.68 (0.32 judge false-negative on tokenizer-artifact words; deterministic check is AUTHORITATIVE so these are NEVER dropped), claude-vs-deepseek raw 0.780 / kappa 0.433 (n=268), claude-vs-stored-gemini raw 0.692 / kappa 0.141 (n=130).

  Every row carries additive keys metadata_enlargement_batch in {iter1_original,iter2_new} and metadata_independent_judge_{model,pass,reason} (all toxicity rows populated; first-letter populated for the re-judge sample, else null). iter-1 originals are byte-identical except those additive keys (verified: 0 problems, true superset, no id collisions). data_summary.json reports the per-concept null-distribution sizes (per letter x carrier; per origin x fold; per sub-attribute), both-judges-pass high-confidence subset sizes (toxicity 370, first-letter 172 in-sample), generation/re-judge stats, agreement/kappa, originals-confirmation rate, and gate constants (jaccard_max=0.6, char_change_min=0.25). Total OpenRouter spend $1.72 (hard cap $10). Models: openai/gpt-4o-mini, anthropic/claude-haiku-4.5, google/gemini-3.1-flash-lite, deepseek/deepseek-v4-flash. Reproduce with `uv run data.py` (caches make re-runs $0).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json
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
</dependencies>

<instructions>
YOUR ROLE: Write a detailed PLAN for the artifact. A separate executor agent runs the actual artifact later.

You are a PLANNER, not an executor. Your output is a plan that tells the executor what to do and how.
Do NOT execute the artifact itself — a separate agent handles that. Your job is to plan it so well that the executor can follow your plan step by step.

You CAN and SHOULD: search the web, read papers, and explore library docs to make your plan concrete.
You CANNOT run shell commands or scripts — code execution is disabled. Research via web tools only.

Do NOT do the executor's job: don't download datasets, don't implement code, don't run experiments, don't write proofs, don't compute evaluations.

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

EXPERIMENT executor scope:
  Output: method_out.json with results (metrics, predictions, analysis) — the core computational work
  DOES: Implement and run methods/algorithms, compute metrics, compare approaches, produce quantitative results
  DOES NOT: Collect new datasets (depends on DATASET artifacts for input data), write formal proofs
  This is the right artifact for any code that processes data and produces results
</artifact_executor_scope>

<artifact_planning_rules>
EXPERIMENT: Must depend on at least one DATASET. Define clear metrics and baselines before running. Consider trying multiple method variations rather than a single approach.
</artifact_planning_rules>

<compute_profiles>
Choose the compute profile this artifact needs for execution.
Available profiles for experiment artifacts:
  - gpu: 1x NVIDIA RTX A4500, 20GB VRAM, 7 vCPUs, 29GB RAM — ML training, CUDA, large models (fallback: GPUs cheap→expensive: 2000 Ada → A4000 → 4000 Ada → L4 → 4090 → 5090)
  - cpu_heavy: 4 vCPUs, 32GB RAM — large datasets, memory-intensive processing (fallback: CPUs cheap→expensive, then GPU hosts cheap→expensive (all ≥32GB RAM))

Set runpod_compute_profile to one of these exact tier names.
</compute_profiles>
GOOD PLANS: specific, actionable, consider failure scenarios, build on the suggested approach.
BAD PLANS: vague hand-waving, ignoring the suggested approach, missing critical executor details.
</instructions><user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "description": "Plan for an EXPERIMENT artifact.",
  "properties": {
    "title": {
      "description": "Short title for the plan",
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Brief summary",
      "title": "Summary",
      "type": "string"
    },
    "runpod_compute_profile": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": "cpu_light",
      "description": "Compute tier for execution \u2014 pick from the available profiles list (e.g., 'gpu', 'cpu_heavy', 'cpu_light'). Only used in RunPod mode.",
      "title": "Runpod Compute Profile"
    },
    "implementation_pseudocode": {
      "description": "High-level pseudocode for the experiment implementation",
      "title": "Implementation Pseudocode",
      "type": "string"
    },
    "fallback_plan": {
      "description": "What to do if the primary approach fails - alternative methods, simplified versions",
      "title": "Fallback Plan",
      "type": "string"
    },
    "testing_plan": {
      "description": "How to validate the experiment works: start with small/fast tests, look for confirmation signals before running full-scale experiments",
      "title": "Testing Plan",
      "type": "string"
    }
  },
  "required": [
    "title",
    "implementation_pseudocode",
    "fallback_plan",
    "testing_plan"
  ],
  "title": "ExperimentPlan",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-06-17 21:50:31 UTC

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
