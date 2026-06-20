# gen_plan_experiment_1 — test_idea

> Phase: `invention_loop` · round 7 · `gen_plan`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_plan_experiment_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 08:02:13 UTC

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

<hypothesis>
kind: hypothesis
title: >-
  Training-Free Auditable Localization of Homograph-Polysemy SAE Absorption: Single-Absorber Discovery via Two-Track Co-Response
  Grouping with a Sparse-Gated Edit — Now Gated on a GATED-DENSE Control + Honest Forget-Operating-Point, After the Safety
  Screen Returned a Homograph-Confined NULL
hypothesis: |-
  ITERATION-6 STATUS -- THE TWO ITER-5 GATES WERE BOTH EXECUTED; M2' (SAFETY-RELEVANT WIN) RETURNED A FIRM NULL THAT CLOSES THE SAFETY CEILING, AND M1' (STRONGER DENSE BASELINE) 'PASSED' ITS PRE-REGISTERED GATE BUT THE ITER-6 REVIEWER EXPOSED THAT THE WIN SITS AT A NEAR-NOOP FORGET OPERATING POINT AND IS MISSING THE DECISIVE GATED-DENSE CONTROL. Iteration 6 delivered: the M1' sub-context-targeted dense comparison [art_3WXWsaSoGMnK]; the M2' safety-attribute absorption screen + conditional downstream [art_yAQgbq5Wgymx]; a four-hierarchy safety-identity testbed [art_KNPsfjByyxiS]; the M4 router homograph-prospective expansion + M7 breadth count [art_F_-HUhl0NR_i]; an integrity-lock consolidation eval [art_w7p8du2N1f0Y]; and an M1'/M2' positioning + citation audit [art_3zaa2xXEp8Az]. What honestly landed, and what the iter-6 reviewer exposed:

        - M1' STRONGER-BASELINE DOWNSTREAM 'WIN' EXECUTED -- KG-ABL beats u_sub on the two clean absorption cases under both judges, BUT the headline is undercut by a near-NOOP forget operating point AND a MISSING gated-dense control (reviewer MAJOR-1 RIGOR + MAJOR-2 METHODOLOGY, the new #1 and #2 blockers) [art_3WXWsaSoGMnK]. The decisive comparator was rebuilt as u_sub = diff-of-means(target-sub-context-positive, sibling-positive in the same parent context), fit on a disjoint fold from the per-sub-context labels the testbeds already carry, erased via the SAME operator h <- h - beta(h.u_sub)u_sub swept to MATCHED forget. The two absorption cases registered KG_BEATS_USUB on the joint (retain-utility x fluency) judge metric: taxonomic Georgia (16009) joint Delta +0.561 CI[0.318,0.811] (second judge +0.465 CI[0.289,0.658]) and first-letter large (8463) Delta +1.000 CI[0.796,1.213]; US (846) reclassified co-firing and moved OUT of the gate; toxicity insult a weak judge-only edge not counted. The 'a single dense hyperplane structurally cannot localize' framing was correctly DELETED (u_sub IS a dense hyperplane and DOES localize, sub-probe AUC ~1.0), and the KG edge was reframed as sparse-firing GATING (token footprint 0.014-0.03). BUT the reviewer VERIFIED IN CODE (method.py:836) that matched_target = 0.8*min(max_forget_KG, max_forget_SUB), and the single-latent ablation has a TINY forget ceiling in every case (max_forget_KG = 0.065 Georgia / 0.035 US / 0.45 large / 0.054 insult) while u_sub can forget far more (max_forget_SUB = 7.1 / 11.1 / 7.7 / 12.6, i.e. ~17-320x; reviewer 'up to 400x'). So the matched point is ALWAYS ~0.8*max_forget_KG and u_sub is throttled to ~1% of its range; on the held-out FORGET prompts the KG edit is a NO-OP on the majority (median next-token forget-KL = 0.0; 89% (Georgia) / 83% (large) / 94% (US) of KG continuations are IDENTICAL to the unedited model), the judged_forget_quality is ~equal for KG and u_sub (both ~1.0/2) PRECISELY because KG's generations equal NOOP, and the low KG collateral is partly MECHANICAL (the gated edit is near-identity off its sparse support). 'Curve-dominance over the full achievable forget range' is reported without disclosing that range is ~1% of u_sub's. WORSE: the decisive control is MISSING -- gating is NOT SAE-specific. One can gate ANY edit by a sparse firing indicator (erase u_sub only where the sub-context projection |h.u_sub| or a 1-D sub-context detector exceeds a threshold). Every comparison is gated-sparse-KG vs UNGATED-continuous-dense, conflating 'discovering a sparse SAE handle is valuable' with 'gating any edit by sparse firing reduces collateral.' And US 'wins' +0.439 despite being CO-FIRING (not absorption), suggesting the win is driven by edit FOOTPRINT, not by the absorption structure the method discovers. As stated, 'ablating one discovered absorber produces a better downstream outcome than a sub-context-targeted dense baseline on a parent-preserving sub-context-removal task' OVERSTATES the result: the model does not actually forget on most prompts, and the gating advantage is unproven against a gated dense direction.

        - M2' SAFETY-RELEVANT WIN -- A FIRM NULL: SAFETY ABSORPTION IS HOMOGRAPH-CONFINED [art_yAQgbq5Wgymx]. Screening four identity hierarchies (religion / race-ethnicity / orientation-gender / nationality) built INLINE from the full civil_comments corpus (1.76M rows, surface-form-only labels, never Jigsaw columns), of 44 ELIGIBLE safety identity groups EXACTLY TWO exhibit the absorption signature (recall-hole>0.5, firing-Jaccard<0.1, precision>=0.7, >=150 eligible, hole-coverage-gain CI excl 0, corroborated by the non-circular form-free oracle): white (race; hole .63, J .019, oracle .46) and straight (orientation; hole .72, J .009, oracle .26) -- and BOTH are lexical homographs. The other 42 (Muslim/Hindu/Catholic, gay/lesbian/Asian, Mexican/Chinese/Canadian, ...) show NO parent recall-hole. Absorption tracks LEXICAL POLYSEMY, exactly as for Georgia/Jordan, NOT safety semantics. STRUCTURE != LEVERAGE: on the conditional downstream test (KG-ABL vs u_sub=diff-of-means(target-group, sibling-groups), two judges), Georgia (non-safety positive control) is a clean win (Delta_joint [.53,.96] both judges, retain-collateral KL 3e-5 vs u_sub .078, curve-dom 1.0), but straight wins under the PRIMARY judge only (matched-forget magnitude .0012, second judge CI incl 0) and white's oracle-confirmed absorber has NO_ON_TARGET_EFFECT. overall_verdict = SAFETY_ABSORPTION_FOUND_NO_WIN. THIS GATE IS RESOLVED AS A NULL: the safety-relevance significance ceiling is CLOSED -- the absorption phenomenon CCRG repairs is confined to homograph/polysemy tokens, NOT the demographic attributes a safety practitioner most wants to control.

        - M4 ROUTER DEMOTED + M7 BREADTH COUNTED [art_F_-HUhl0NR_i]. The FROZEN recall-hole-alone rule (tau_h=0.7795, derivation balanced-acc 1.0, LOO 0.833) was tested on a 5.6x-enlarged prospective set of 34 eligible homograph entities (18 cities / 12 months / 3 names / 1 brand). It validates on the base-rate co-firing direction (co-firing-predicted 29/30, Wilson [0.833,0.994]) but the DISCRIMINATIVE absorption-predicted stratum does NOT: homograph 2/4 [0.15,0.85], homograph+7-spelling-letters 5/10 [0.237,0.763] -- both include 0.5; recall-hole=1.0 over-predicts on new letters F/M/W. VERDICT = ROUTER_DEMOTED (exploratory diagnostic, not validated a-priori predictor). M7 BREADTH (rebutting 'absorption is n=1-2' with a count): of 64 homograph entities with a stable estimate only THREE are absorption-structured -- all MONTHS (March 0.997, June 0.947, February 0.573; cities 0/22, names 0/20, brands 0/10), the month parent firing on only 0.62 of month mentions. STRUCTURAL != DOWNSTREAM: the strongest downstream-confirmed case is month/May (label-free unit AUC 0.95 vs raw 0.79, delta +0.160) even though May is NOT 'structured' (J 0.434).

        - M3/M8 SELECTIVITY ARTIFACT CORRECTED [art_w7p8du2N1f0Y]. The stored 65k 'Georgia 3.7e6 selectivity / regime-mean 466997x' is a DIVIDE-BY-EPSILON artifact (kg_collateral==0 -> ratio=on_target/1e-8); excluding floor-limited + NO_ON_TARGET cases the corrected 65k absorption selectivity is mean 721.72x / median 676.33x (n=4); 16k and 65k Georgia edits are COMPARABLY surgical (both collateral at/below numerical precision), NOT 2000x apart. 22 DISTINCT holes (30 FDR survivors - 6 double-counts - 2 non-hole); absorption-6 mean 1452.47x / median 1262.21x (the draft's '1452 median' is the MEAN); surgical-5 median 1722.46x; within-taxonomic Spearman rho 0.90 (NOT 1.0); random SINGLE content-responsive-latent control 28/28>p95, 23/28>p99; member-labeling gap 0.634; numeric below-gate (digit cosine 0.876<0.9). M5: US is CO-FIRING (aggregate recall-hole 0.20-0.23 < tau_h 0.78) yet absorber 846 = 214x surgical -> a router FALSE-NEGATIVE (J 0.04 specific vs 0.20 aggregate). M7: the two-track algorithm is a TRAINING-FREE LABEL-FREE DISCOVERY of the SINGLE absorber (16009/8463/846), not multi-member grouping; C-track ties weak baselines (toxicity 0.762 vs 0.765); set-cover-specific selection only on I/D/Georgia.

        - CROSS-DICTIONARY REPLICATION HOLDS (carried, M2 iter-5) [art_4L1MZxvWYlGd]: 65k FULL (more absorption, as predicted; 52 distinct holes vs 22 at 16k), layer-9 PARTIAL (absorbed token shifts: Georgia loses hole, Jordan gains it + surgical 2376x). MODEL-DIFFING stays a confound-bounded NULL (+0.000 CI[-0.009,0.007]); steering stays a generality demo (surgical on L,D only).

        WHAT THE ITER-6 REVIEW EXPOSED -- THREE MAJORS THAT GATE PUBLICATION, PLUS THREE MINORS:
          (R1, RIGOR -- new #1 blocker) The M1' downstream win sits at a forget operating point hard-pinned to the single latent's weak ceiling, where the KG edit produces little-to-no actual forgetting (median forget-KL 0; 83-94% of continuations equal NOOP); the low KG collateral is partly mechanical; curve-dominance is over ~1% of u_sub's range. => ITERATION 7 MUST report matched_target KL and BOTH max_forget values, disclose u_sub can forget ~17-320x more, show the FULL-range collateral curve, and add an edit-vs-NOOP judged-forget delta (or a sub-context probe-accuracy drop) PROVING the matched point induces MEANINGFUL forgetting. If it does not, the claim is SCOPED from 'unlearning that beats dense' to 'sparse, selective, LOW-COLLATERAL PARTIAL sub-context suppression at the small forget a sparse latent can reach.'
          (R2, METHODOLOGY -- new #2 blocker) The decisive control is missing: a GATED DENSE baseline. Gating is not SAE-specific. => ITERATION 7 MUST add DENSE-SUB-ABL-GATED (erase u_sub ONLY where the sub-context projection or a 1-D detector exceeds a threshold), swept to the SAME matched forget, scored identically. FORK: if KG still beats gated-dense (CI excl 0) at a meaningful forget level, the SPARSE-SAE-HANDLE contribution is established; if the gated dense direction CLOSES the gap, the contribution is the GATING IDEA (not SAE-specific) and the SAE-specific value reduces to label-free DISCOVERY of WHERE to gate. Also test absorption-vs-co-firing: the win must be LARGER on the absorption cases (Georgia/large) than on co-firing (US/toxicity), else it is footprint, not the absorption structure the method discovers.
          (R3, SCOPE -- the now-CLOSED ceiling) Demonstrated significance against the stated goal is the ceiling: no SAE unit out-classifies a dense probe on ANY task; the 44-group safety screen is a NULL; model-diffing is a confound-bounded null; steering is a demo; the two confirmed downstream wins are non-safety homograph/spelling tokens (Georgia, large). => ITERATION 7 MUST REPOSITION the framing around 'training-free, auditable LOCALIZATION of homograph-polysemy absorption in frozen SAEs', state up front that the reliability gain is LOCALIZATION/AUDITABILITY (NOT classification), and present the safety homograph-confinement as the HEADLINE LIMITATION. The safety null IS the finding; an optional confirmatory pass over the built named_entity_safety hierarchy [art_KNPsfjByyxiS] may broaden the count but the null stands. Do NOT lead with safety-reliability language the results do not support.
          (R4-R6, MINORS) novelty: the titular two-track grouping is largely inert (M7: multi-member unit strictly WORSE than the single absorber; C-track ties; set-cover-specific selection only 3 slices) -- REFRAME the method identity around SINGLE-ABSORBER DISCOVERY (anchored, recall-hole-guided, precision-gated set-cover with effectively k=1 for the wins), demoting multi-member grouping and the C-track to secondary/exploratory, and consider foregrounding 'discovery + sparse-gated edit' over 'grouping into reliable units'. clarity: Georgia is reported with two different effect sizes (+0.561 unlearning vs +0.743 safety) due to different judge pair + retain/sibling pool -- pick ONE canonical number and footnote the re-run; and clarify 'u_sub is a stronger comparator' means localization IN CONCEPT SPACE (model-internal KL 0.078<0.102), not a uniformly larger JUDGED collateral (Table util_SUB 1.17 < util_whole 1.33 at the matched point). evidence: state up front (intro+abstract) that on classification the units do NOT beat dense probes on any task (toxicity unit AUC 0.762 vs h 0.84-0.89, residual probe 0.86; sub-attributes collapse to 0.63 vs 0.93), so 'reliable units' is a LOCALIZATION claim, not a classification claim.

        THE ITERATION-7 MANDATE (the two NEW load-bearing pieces -- gated-dense control + honest forget -- make or break the headline; the reposition + reframe are required; nothing else gates):
          (M1'' = NEW LOAD-BEARING #1 -- GATED-DENSE CONTROL + HONEST FORGET-OPERATING-POINT) Re-run the selective-suppression comparison [art_3WXWsaSoGMnK] with FOUR operators at the SAME swept matched forget: KG-ABL (gated sparse SAE absorber), DENSE-SUB-ABL (ungated continuous u_sub), the NEW DENSE-SUB-ABL-GATED (u_sub erased only where the sub-context projection / 1-D sub-context detector exceeds a threshold), and DENSE-WHOLE-ABL (secondary reference). Report matched_target KL, both max_forget_KG and max_forget_SUB per case, the full-range collateral curve (not only the KG-pinned point), and an edit-vs-NOOP judged-forget delta or sub-context probe-accuracy drop confirming MEANINGFUL edit-induced forgetting. Keep the second different-family judge + the deterministic human-proxy. FORK: (a) KG-ABL beats DENSE-SUB-ABL-GATED (joint CI excl 0 under both judges) at a forget level where edit-vs-NOOP forgetting is non-trivial AND the absorption-case advantage exceeds the co-firing-case advantage => headline 'a DISCOVERED sparse SAE absorber gives lower collateral than even a GATED sub-context-labeled dense direction at matched selective suppression'; (b) the gated dense direction closes the gap => reframe to 'the value is the label-free DISCOVERY of where to gate; gating itself is not SAE-specific'; (c) KG cannot reach meaningful forget anywhere => scope to 'selective LOW-COLLATERAL PARTIAL suppression', dropping 'unlearning/beats-dense'.
          (M2'' = REPOSITION (safety null is the finding) -- THE SIGNIFICANCE CEILING, NOW SETTLED) Lead the paper with 'training-free, auditable localization of homograph-polysemy SAE absorption'; state in the intro/abstract that the reliability gain is LOCALIZATION/AUDITABILITY not classification (no SAE unit out-classifies a dense probe on any task). Present the 44-group safety screen [art_yAQgbq5Wgymx] homograph-confinement as the HEADLINE LIMITATION (absorption = lexical polysemy, not demographic semantics; the closest near-miss steers a CO-FIRING race latent, consistent with Ahsan-Wallace). The non-safety positive control (Georgia) is reported against u_sub under both judges. An optional confirmatory pass over the named_entity_safety hierarchy [art_KNPsfjByyxiS] may add homograph-entity cases but does not change the verdict.
          (M3 = METHOD-IDENTITY REFRAME) Foreground SINGLE-ABSORBER DISCOVERY (the anchored, recall-hole-guided, precision-gated set-cover with effectively k=1 for the downstream/edit wins); present multi-member grouping (real on first-letter pools and the rebuilt Georgia unit) and the C-track as SECONDARY/EXPLORATORY. The two-track machinery's demonstrated job is PROPOSING the precise single absorber that marginal attribution drops; explicitly ablate unit-vs-single-best-absorber (already shows the single absorber WINS [art_3WXWsaSoGMnK]).
          (M4 = CLARITY) Pick ONE canonical Georgia positive-control number; footnote that the safety section re-runs it under a different judge/sibling pool (the +0.743 value). State that u_sub 'localizes better than whole-parent' refers to model-internal KL (0.078<0.102), while the JUDGED collateral can invert at the matched point.
          (M5 = CARRIED INTEGRITY) Selectivity divide-by-epsilon corrected (722x/676x n=4; 16k/65k comparably surgical) [art_w7p8du2N1f0Y]; router demoted (prospective Wilson includes 0.5; 3/64 entities, months only) [art_F_-HUhl0NR_i]; US = co-firing router false-negative; 22 distinct holes / mean 1452x median 1262x / rho 0.90 within-taxonomic; random SINGLE-latent control; numeric below-gate; cross-dictionary 65k full / layer-9 partial [art_4L1MZxvWYlGd]; locked citation venues [art_3zaa2xXEp8Az] (Chanin NeurIPS-2025; AxBench/SAEBench ICML-2025; CanonicalUnits ICLR-2025; Farrell NeurIPS-2024 Safe-GenAI WS; SPLINCE/Karvonen-Marks NeurIPS-2025; Ahsan-Wallace ICLR-2026; BiasEdit TrustNLP@NAACL-2025; Collapsed-LMs ICLR-2025; Entity-Level COLING-2025; Deng->ACL-2026; SAEmnesia->ICML-2026; Peng 'Discover-not-Act'). Strip iteration/rebuttal/infra scaffolding.

        RE-DESIGNATED HEADLINE (auditable-localization-first; SAME two-track method now framed as single-absorber discovery; the gated-dense control + honest forget make or break the edit claim). On a FROZEN public SAE, interventional grouping by co-response to content counterfactuals is a TRAINING-FREE, LABEL-FREE DISCOVERY PROCEDURE that surfaces the single precise absorber latent a marginal-attribution ranking silently drops, plus a feature-level KNOWLEDGE GRAPH whose edges carry MEASURED, localized repair utility: a KG-named absorber added to a suppressed parent recovers its recall hole, beating a random SINGLE-latent-addition control (22 distinct holes survive FDR across spelling/taxonomic/numeric), and ablating that absorber gives a SPARSE-FIRING-GATED, LOW-COLLATERAL, SELECTIVE sub-context edit (mean 1452x / median 1262x selectivity over collateral at 16k, floor-limited cases excluded) -- a localization that REPLICATES on a 4x-wider SAE (with MORE absorption, as the literature predicts) and partially across a layer (where the absorbed token shifts). The CENTRAL OPEN CLAIM iteration 7 must close is whether the discovered sparse-gated edit beats a GATED sub-context-targeted dense direction (DENSE-SUB-ABL-GATED) -- not merely an ungated one throttled to ~1% of its range -- at a forget level where the edit induces MEANINGFUL forgetting; if a gated dense direction closes the gap, the SAE-specific value reduces to label-free DISCOVERY of where to gate. The method does NOT out-classify a strong dense probe on any task (reliability gain = LOCALIZATION/AUDITABILITY, not classification); SAFETY-RELEVANT absorption does NOT exist beyond homographs (2/44 safety groups, both lexical homographs, no robust safety win -- the SETTLED ceiling and headline limitation); absorption is NARROW (homograph-polysemy entity tokens + first-letter spelling, 0/28 professions, 3/64 homograph entities); the router is a derivation-perfect but out-of-sample-UNVALIDATED screen; and the durable value is AUDITABLE, EDITABLE, LABEL-FREE-DISCOVERED, REGIME-TARGETED LOCALIZATION of homograph-polysemy absorption.

        PRIMARY ENDPOINT (re-designated; the two NEW pieces are load-bearing).
          (a) GATED-DENSE-CONTROLLED, HONEST-FORGET EDIT TEST (NEW LOAD-BEARING, M1''): KG-named single-absorber gated ablation vs DENSE-SUB-ABL-GATED at matched forget on the joint outcome, with the forget operating point and full-range curve disclosed and an edit-vs-NOOP forget delta proving meaningful forgetting. A WIN over GATED dense at meaningful forget = the strong contribution; a MATCH = the label-free-discovery (where-to-gate) contribution; near-NOOP-everywhere = scope to 'selective low-collateral suppression'. 'Beats ungated u_sub' (iter-6) is necessary but no longer sufficient.
          (b) AUDITABILITY/LOCALIZATION SPINE (ACHIEVED, honestly re-counted): 22 distinct-hole FDR repairs over a random single-latent control [art_sxwT7hK6YFEA, art_w7p8du2N1f0Y]; sparse-gated surgical edits with corrected selectivity [art_0CZwPjG2YMCf]; member-labeling beats shuffle null; cross-dictionary 65k full / layer-9 partial [art_4L1MZxvWYlGd].
          (c) SAFETY SCOPE (SETTLED NULL, M2''): safety absorption is homograph-confined (2/44, both homographs; no robust safety win) -- the capping limitation, reported as the finding [art_yAQgbq5Wgymx].
          (d) ROUTER: recall-hole-alone reproduces on derivation (bal-acc 1.0) but is OUT-OF-SAMPLE-UNVALIDATED (homograph prospective Wilson includes 0.5) -- DEMOTED to exploratory diagnostic [art_F_-HUhl0NR_i].
        SUPPORTING (strengthen, do not gate): within-SAE set-cover selection where the signature holds (first-letter I,D; taxonomic Georgia); member-labeling above null; the steering demo (L,D); the homograph breadth count (months: March/June/February). The headline NO LONGER depends on classification beating dense, on multi-member grouping beating single absorbers, on the router being validated, or on a safety win existing.

        THE TWO-TRACK CLUSTERING ALGORITHM (specification unchanged; now FRAMED as single-absorber discovery). STEP 1 cover-based eligibility (content-responsive above a shuffle null; firing-precision>=0.7; covers>=1 sub-context). STEP 2 C-TRACK (splitting, SECONDARY): positive-Spearman soft-threshold affinity (beta=6, WGCNA) -> Leiden RBConfiguration; resolution by bootstrap-ARI stability. STEP 3 K-TRACK (absorption, the DISCOVERY step, effectively k=1 for the wins): ANCHOR = argmax cover-set chosen WITHOUT the diagnostic, with the UNSUPERVISED FIRING-FLOOR PARENT-VALIDATION (anchor must fire on held-out corpus above ~5%); HOLES = parent's uncovered pairs; greedily add mutually-exclusive (firing-Jaccard<0.1), PRECISE (>=0.7, held-out-gated) absorbers covering holes with marginal-gain>=0.05 CI excluding 0; PRECISION-GATED / precision-WEIGHTED objective (Georgia selects 16009 prec .955, not 4697 prec .35). STEP 4 reconcile C-communities and K-covers, de-duplicate by highest coverage gain. STEP 5 ADMISSION: signature C OR matched-null signature K (+ small-k absolute gain>=0.05 CI excluding 0, mutual-exclusivity, precision floor) AND unit-level surface invariance; BH across M candidates. The DEMONSTRATED value of this machinery is PROPOSING the precise single absorber that marginal attribution drops (multi-member grouping ADDS collateral on the downstream task, so multi-member units are reported SECONDARY, real only where the data support them, e.g. first-letter pools).

        SAE-LATENT FIRING-STRUCTURE ROUTER (screening DIAGNOSTIC, derivation-perfect but out-of-sample-UNVALIDATED; RECALL-HOLE-PRIMARY). One forward pass: encode, identify the firing-floor-validated content-responsive parent, find per-sub-context detectors, report (i) parent per-sub-context recall holes and (ii) detector-vs-parent positive-only firing-Jaccard. RULE: predict absorption-regime iff the parent has a recall HOLE (>~0.78) -- balanced-acc 1.0 on 12 derivation concepts -- CORROBORATED by low firing-Jaccard. HONEST STATUS: on the 34-entity homograph-prospective expansion the discriminative absorption stratum's Wilson CI INCLUDES 0.5 (homograph 2/4, homograph+spelling 5/10) and recall-hole=1.0 over-predicts on new letters F/M/W; treat as an EXPLORATORY DIAGNOSTIC. Firing-Jaccard alone is insufficient (numeric high-J absorption, aggregated-taxonomic low-J co-firing). Co-firing (toxicity, US aggregate, the 42 no-hole safety groups) => supervised attribution wins and CCRG does not help.

        BASELINE GLOSSARY (matched baselines primary; the decisive M1'' comparator is the GATED dense direction). (a) best raw single latent; (b)/(c) observational co-activation/decoder clusters COUNT-MATCHED to k; (d) counterfactual diff-of-means; (e) raw-residual probe; (f) WHOLE-PARENT LEACE/diff-of-means erasure (SECONDARY 'naive over-shoot' reference); (g) SCR/TPP oracle pool; (h) count-and-pool-matched SCR/TPP probe; (i) unmatched diff-of-means; (j) oracle group-DRO; (k) label-free group-inference (JTT/GEORGE -- cannot localize, decoder-projection argmax is the parent); (RE-k) random-eligible-k floor; (S-rec)/(S-prec)/(S-mag) non-random label-free selectors. DECISIVE COMPARATORS FOR THE EDIT: u_sub (DENSE-SUB-ABL) = SUB-CONTEXT-TARGETED dense direction = diff-of-means(target-sub-context-positive, sibling-positive in the same parent context), ungated continuous erasure -- the iter-6 comparator KG already beats but only at a throttled operating point; and the NEW u_sub-GATED (DENSE-SUB-ABL-GATED) = the SAME u_sub erased ONLY where the sub-context projection / 1-D detector exceeds a threshold, the load-bearing iter-7 control that isolates 'sparse SAE handle' from 'gating any edit'.

        NON-SPELLING / HOMOGRAPH TESTBED (HOMOGRAPH-POLYSEMY ABSORPTION; affirmative selection n=1-2 + months). Absorption recurs on HOMOGRAPH/POLYSEMOUS tokens whose general parent is suppressed -- taxonomic absorption-type slices are EXACTLY Georgia (eligible, hole .80) + Jordan (DESCRIPTIVE n=124, hole .71); United States is CO-FIRING (J .20, hole .23); a clean PROFESSION is-a hierarchy is 0/28; of 64 homograph entities only 3 months (March/June/February) are structured (0/22 cities, 0/20 names, 0/10 brands); of 44 safety identity groups only 2 homographs (white, straight). So absorption is POLYSEMY-SPECIFIC, NOT broad taxonomic/is-a and NOT safety-semantic. Numeric = below-gate (digit cosine 0.876<0.9), eligibility+pooling, diagnostic-unconfirmed. A non-SAE dense probe matches/beats the unit on ALL classification.

        SCOPE AND VALUE PROPOSITION. The defensible contribution is: (1) a TRAINING-FREE, LABEL-FREE DISCOVERY PROCEDURE (interventional two-track grouping, effectively single-absorber discovery) that surfaces the single precise absorber marginal attribution drops, with a MEASURED, EDITABLE feature-KG (recall-hole recovery beating a random single-latent addition; sparse-gated surgical edits; (k) cannot localize) plus human/LLM-auditable members, REPLICATING across SAE dictionaries; (2) an a-priori RECALL-HOLE screening DIAGNOSTIC (derivation-perfect, out-of-sample-unvalidated) for when grouping helps; (3) a WITHIN-SAE absorption-regime selection win where it occurs (first-letter I,D; taxonomic Georgia). The OPEN, GATING question iteration 7 must answer is whether the discovered sparse-gated edit BEATS-OR-MATCHES-WITHOUT-LABELS a GATED sub-context-targeted dense direction at a forget level inducing meaningful forgetting (M1''). The method does NOT out-classify a strong dense probe; toxicity is a clean co-firing negative; SAFETY absorption does NOT exist beyond homographs (settled); absorption is narrow. HEADLINE = auditable, label-free-discovered, regime-targeted LOCALIZATION of homograph-polysemy absorption; classification is SUPPORTING and within-SAE; the sparse-gated edit is a CAPABILITY whose strength is bounded by the M1'' gated-dense control.

        HONEST NEGATIVES (each publishable): the M1' 'win' as run is at a near-NOOP forget operating point pinned to the sparse latent's tiny ceiling (KG identical to unedited on 83-94% of FORGET prompts) and the decisive GATED-DENSE control is not yet run (the gating advantage is unproven against gated dense); unit out-classifies NO non-SAE dense probe on any task (toxicity unit 0.762 vs dense 0.86-0.89); the two confirmed downstream wins are non-safety (Georgia, large); SAFETY absorption is homograph-confined (2/44, both homographs, no robust safety win) -- the settled ceiling; set-cover-specific selection only 3 slices (Georgia, I, D); non-spelling affirmative selection effectively n=1 (Georgia), 1-2 with descriptive Jordan, +3 months structurally; 0/28 professions; the router is at chance out-of-sample (homograph prospective Wilson includes 0.5, over-predicts on new letters); cross-dictionary replicates at 4x width but only PARTIALLY across a layer; the 65k 3.7e6 selectivity was a divide-by-epsilon artifact (16k/65k comparably surgical); the headline rests on a single primary LLM judge (second judge corroborates Georgia/large); the two-track grouping is largely inert (wins trace to single absorbers; multi-member units ADD collateral); the form-free MAGNITUDE diagnostic is precision-blind; compact named units cost AUC; numeric is below-gate; model-diffing a confound-bounded null; steering surgical only on L,D. A clean result of M1'' where the GATED dense direction closes the gap = 'the value is label-free discovery of where to gate, not an SAE-specific edit advantage' and is itself publishable; near-NOOP-everywhere = scope to 'selective low-collateral suppression'.

        MOTIVATION (substance unchanged). Single SAE latents are unreliable units: feature absorption (Chanin 2409.14507, NeurIPS 2025), splitting, hedging (2505.11756), and 'SAEs Do Not Find Canonical Units' (ICLR 2025) converge on no single latent reliably tracking a concept; AxBench (ICML 2025) and DeepMind's negative report show plain diff-of-means beats raw-latent SAE methods, and Farrell (2410.19278) shows multi-feature SAE unlearning has side-effects >= RMU -- so any SAE method must clear strong dense baselines AND, for the edit, a GATED sub-context-targeted dense direction, not just an ungated one. Absorption is the regime where OBSERVATIONAL signals break by construction and MARGINAL-ATTRIBUTION selection silently drops the absorber; correlation-community detection handles shared-support splitting, anchored greedy set-cover handles disjoint-support absorption -- coverage-complementarity is a set-level property no pairwise affinity can express, which is why grouping is the right DISCOVERY operator for the absorber even though the multi-member unit's edit value over the single absorber is negative. Architectural remedies (Matryoshka/H-SAE/SASA) retrain and are orthogonal; their dictionary-size dependence is exactly why cross-dictionary replication (achieved) and the wider-absorbs-more signal matter. The method positions against the 'use SAEs to DISCOVER, not to ACT' thesis (Peng 2506.23845): CCRG discovers the sub-context handle by interventional grouping; whether ACTING through it beats a gated dense direction is the load-bearing open question.

        SUCCESS CRITERIA. METHOD CONFIRMED iff: (LOAD-BEARING) (M1'') the KG-localized sparse-gated single-absorber edit BEATS (joint CI excl 0 under two judges) OR MATCHES-WITHOUT-SUB-CONTEXT-LABELS the GATED sub-context-targeted dense direction (DENSE-SUB-ABL-GATED) at a forget level where an edit-vs-NOOP delta confirms MEANINGFUL forgetting, with the absorption-case advantage exceeding the co-firing-case advantage; AND the auditability/localization spine holds (22 distinct holes, random single-latent control, corrected selectivity, cross-dictionary 65k full / layer-9 partial); AND the safety null is reported as the capping scope (homograph-confined). SUPPORTING (strengthen, do not gate): within-SAE set-cover selection (Georgia, I, D); member-labeling above null; admission false-admit <=0.05; the recall-hole router on derivation (prospective honestly demoted); the steering demo (L,D); the homograph breadth count. HONEST NEGATIVES are reportable and cap-but-do-not-sink: a gated dense direction closing the gap (=> contribution is label-free where-to-gate discovery), near-NOOP forget everywhere (=> selective low-collateral suppression), safety absorption absent (settled), router-at-chance, layer-conditional replication, single-absorber-not-grouping attribution, numeric unconfirmed, toxicity co-firing negative, no classification win over dense on any task.
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
  Same auditable-absorption frame; reposition to homograph-localization, add gated-dense gate, resolve safety null.
_confidence_delta: decreased
_key_changes:
- >-
  Recorded iter-6 execution: M1' KG-ABL beats u_sub on Georgia (+0.561) and large (+1.000) under both judges, but the reviewer
  exposed the win sits at a near-NOOP forget operating point (matched_target=0.8*min(maxKG,maxSUB); KG identical to unedited
  on 83-94% of FORGET prompts) and is missing the decisive gated-dense control [art_3WXWsaSoGMnK].
- >-
  NEW LOAD-BEARING #1 (M1''): add DENSE-SUB-ABL-GATED (gate u_sub by a sparse sub-context indicator) at the same matched forget,
  report matched_target KL + both max_forget (u_sub forgets ~17-320x more), the full-range curve, and an edit-vs-NOOP forget
  delta proving meaningful forgetting. FORK: KG beats gated-dense at meaningful forget -> sparse-SAE-handle established; gated-dense
  closes gap -> contribution is the gating idea (not SAE-specific), SAE value reduces to label-free DISCOVERY of where to
  gate; near-NOOP everywhere -> scope to 'selective low-collateral suppression' not 'unlearning'.
- >-
  Require the absorption cases (Georgia/large) to beat gated-dense by MORE than the co-firing cases (US/toxicity), else the
  win is edit footprint, not the absorption structure the method discovers.
- >-
  M2' SAFETY GATE RESOLVED AS A FIRM NULL: absorption is homograph-confined (2/44 safety groups = white/straight, both lexical
  homographs; 42 no-hole; no robust safety win) [art_yAQgbq5Wgymx]. The safety-relevance ceiling is CLOSED; REPOSITION the
  paper to 'training-free auditable localization of homograph-polysemy absorption in frozen SAEs' and drop safety-reliability
  leading language.
- >-
  State up front (intro/abstract) that the reliability gain is LOCALIZATION/AUDITABILITY, NOT classification (no SAE unit
  out-classifies a dense probe on any task; toxicity unit AUC 0.762 vs dense 0.86-0.89).
- >-
  Reframed method identity to SINGLE-ABSORBER DISCOVERY (anchored, recall-hole-guided, precision-gated set-cover, effectively
  k=1 for the wins); demoted multi-member grouping and the C-track to secondary/exploratory (M7: multi-member unit strictly
  worse than the single absorber).
- >-
  Demoted the router to an exploratory diagnostic (homograph prospective Wilson CIs include 0.5) and added the breadth count
  (3/64 homograph entities structured, all months: March/June/February) [art_F_-HUhl0NR_i].
- >-
  Corrected the 65k '3.7e6 selectivity' divide-by-epsilon artifact (722x/676x n=4; 16k/65k comparably surgical) and carried
  honest counts (22 distinct holes, mean 1452x/median 1262x, rho 0.90) [art_w7p8du2N1f0Y].
- >-
  Clarity: pick one canonical Georgia number (footnote the safety-section +0.743 re-run); clarify 'u_sub is a stronger comparator'
  means localization in concept space (model-internal KL 0.078<0.102), not a uniformly larger judged collateral.
- >-
  Confidence DECREASED: both iter-6 load-bearing gates resolved unfavorably -- the safety gate is a NULL closing the ceiling,
  and the M1' headline win is exposed as near-NOOP + missing its decisive gated-dense control -- narrowing the contribution
  to auditable homograph-polysemy localization.
relation_type: evolution
</hypothesis>

<artifact_direction>
Make this direction concrete and actionable. Keep the same type and respect dependencies.

id: experiment_iter7_dir1
type: experiment
objective: >-
  M1'' — THE LOAD-BEARING GATED-DENSE CONTROL + HONEST FORGET-OPERATING-POINT TEST. Re-run the selective sub-concept suppression
  comparison with FOUR operators at the SAME swept matched forget and report it honestly. PRIMARY new deliverables: (i) the
  GATED dense control DENSE-SUB-ABL-GATED — erase u_sub ONLY at tokens where a sparse sub-context gate (the |h.u_sub| projection
  magnitude, or a 1-D logistic sub-context detector fit on the disjoint fold) exceeds a threshold — swept to the same matched
  forget and scored identically; (ii) the HONEST operating-point disclosure — matched_target KL, max_forget_KG, max_forget_SUB
  (and max_forget for the gated arm), the fraction of FORGET continuations identical to NOOP per operator, and the FULL-RANGE
  collateral-vs-forget curve for every operator (so the KG-pinned point is shown in the context of u_sub's full ~17-360x-larger
  range); (iii) an edit-vs-NOOP MEANINGFUL-FORGETTING proof — at the matched point AND at the highest forget KG can reach,
  a judged edit-vs-NOOP forget-quality delta PLUS a deterministic, judge-free sub-context probe-accuracy / absorbed-token
  completion-accuracy drop, establishing whether the operating point induces real edit-induced forgetting. DECISIVE comparison:
  KG-ABL vs DENSE-SUB-ABL-GATED on the joint (retain-utility x fluency) outcome with paired-bootstrap Delta_joint CIs (B>=10,000)
  under BOTH judges, REQUIRING the absorption-case advantage (Georgia 16009, large 8463, + descriptive Jordan 540 and one
  structured month homograph as additional absorption cases) to EXCEED the co-firing-case advantage (US 846, insult), plus
  an explicit 'win persists when US/co-firing excluded' check. Emit a per-case FORK verdict: (a) KG_BEATS_GATED_DENSE_AT_MEANINGFUL_FORGET,
  (b) GATED_DENSE_CLOSES_GAP_DISCOVERY_IS_THE_VALUE, or (c) NO_MEANINGFUL_FORGET_SCOPE_TO_PARTIAL_SUPPRESSION. 'Beats ungated
  u_sub' (iter-6) is reported as necessary-but-no-longer-sufficient context.
approach: >-
  Build directly on the iter-6 M1' experiment by reading its run-tree workspace 3_invention_loop/iter_6/gen_art/gen_art_experiment_1
  (artifact art_3WXWsaSoGMnK: method.py + core.py = the iter-4/iter-5 Gemma-Scope L12/16k JumpReLU engine — JumpReLUSAE/load_sae/ModelBundle,
  ParentProbe diff-of-means u_t + u_sub builder, make_edit_hook(kind='erase_dir'/'ablate_latent'), _scale_for_on_target forget-matching,
  behavioral_curve/kl_rows, paired_bootstrap_diff, the two-judge AxBench pipeline (anthropic/claude-haiku-4.5 primary + openai/gpt-4o-mini
  second), curve-dominance, the deterministic human-proxy, and the KG_BEATS_USUB fork). THE CORE NEW OPERATOR: add DENSE-SUB-ABL-GATED
  as a forward hook that computes p_t = h_t . u_sub at every token and applies h_t <- h_t - beta*(h_t . u_sub)*u_sub ONLY
  where a sparse sub-context gate fires — gate = |p_t| > tau_gate (projection magnitude) AND/OR a 1-D logistic sub-context
  detector d_sub (trained on the SAME disjoint fold as u_sub, never from SAE latents) firing above threshold. To make it a
  fair 'gate ANY edit by sparse firing' control, set tau_gate so the gated-dense token footprint MATCHES the KG absorber's
  firing footprint per case, AND additionally sweep tau_gate across a small footprint range to show the full footprint/collateral
  trade-off; then sweep beta at fixed gate to reach the same matched_target forget. HONEST-FORGET INSTRUMENTATION (the rigor
  MAJOR): for each case and operator record the achievable forget ceiling (max over the lambda/beta sweep of next-token KL
  on held-out FORGET windows), the matched_target value (keep 0.8*min(max_forget_KG,max_forget_SUB) but ALSO evaluate at max_forget_KG),
  the per-operator fraction of FORGET continuations byte-identical to the unedited (NOOP) generation, and the full collateral-vs-forget
  curve over the swept range. MEANINGFUL-FORGETTING PROOF: (a) judged edit-vs-NOOP forget delta = judge(forget-quality of
  operator) - judge(NOOP) on FORGET prompts; (b) DETERMINISTIC, $0 measure = drop in a frozen sub-context probe's accuracy
  (or in the absorbed-token greedy-completion accuracy, e.g. P('country' | 'Georgia is a ___') or the spelling completion
  for 'large') between NOOP and each operator at matched forget — proving the edit actually removes the sub-context, not just
  that KG generations equal NOOP. DECISIVE STATS: KG-ABL vs DENSE-SUB-ABL-GATED Delta_joint paired-bootstrap CI (B>=10,000)
  under BOTH judges + curve-dominance over the GATED-dense achievable range; report KG vs ungated DENSE-SUB-ABL as secondary
  context; tabulate absorption-case advantage vs co-firing-case advantage and the US-excluded re-aggregation. CASES (gradual
  scaling via aii-use-hardware/aii-long-running-tasks; reuse cached encodings, bf16): Georgia (PRIMARY) -> large -> Jordan(540)
  -> one structured month homograph (March/June from art_2xQn686KUmV5 month_name_absorption; discover its absorber via the
  K-track-lite recall-hole+precision-gate, firing-floor-validated, then run the edit) -> US(846) -> insult (co-firing controls).
  Emit a clear per-case FORK verdict and an overall verdict. LLM cost target <$3, hard cap $10, cumulative tracking. Output
  method_out.json (exp_gen_sol_out schema): per-case full-range collateral curves, all forget ceilings + matched_target KL,
  NOOP-identical fractions, edit-vs-NOOP judged delta + deterministic probe/completion drop, KG-vs-GATED-dense joint CIs (both
  judges) + curve-dominance, KG-vs-ungated-u_sub context, absorption-vs-co-firing advantage table, US-excluded check, per-case
  + overall fork verdicts, honest negatives verbatim; datasets block = per-(case,role,prompt) rows with predict_kg_abl/predict_dense_sub_abl/predict_dense_sub_gated/predict_dense_whole_abl/predict_noop
  continuations + per-op fluency/content_pres/utility + model-internal forget-KL/PPL. Validate full/mini/preview <100MB; cache
  encodings under cache/ (exclude from upload).
depends_on:
- id: art_t2uUbjSwpd3t
  label: taxonomic-data
  relation_type:
  relation_rationale:
- id: art_dpYpjSn2Xvg3
  label: spelling-data
  relation_type:
  relation_rationale:
- id: art_8QO7pl6Pd8UQ
  label: toxicity-data
  relation_type:
  relation_rationale:
- id: art_2xQn686KUmV5
  label: homograph-data
  relation_type:
  relation_rationale:
- id: art_RidEJtBC7gPT
  label: method
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

--- Dependency 5 ---
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

### [2] HUMAN-USER prompt · 2026-06-18 08:02:13 UTC

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
