# gen_plan_dataset_1 — test_idea

> Phase: `invention_loop` · round 6 · `gen_plan`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_plan_dataset_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 05:04:53 UTC

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
You are expanding an artifact direction of type: DATASET

DATASET
Collect, prepare, and merge datasets for experiments and analysis.
Runtime: Python 3.12, UV, isolated workspace.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-hf-datasets (HuggingFace Hub — ML datasets, many UCI/OpenML/Kaggle mirrors), aii-owid-datasets (Our World in Data — global statistics), aii-json (schema validation). Also any Python source (sklearn.datasets, openml, direct URLs, APIs) — must verify within 300MB limit.
Capabilities: Search, acquire, transform, combine, and standardize data from any available source.
Deps: REQUIRED none | OPTIONAL RESEARCH for guidance on what data to collect
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

The dataset executor has 6h total (including writing code, debugging, testing, and fixing errors).

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
  Auditable, Training-Free Repair of the SAE Absorption Regime: Two-Track Co-Response Grouping as a Label-Free Discovery Procedure
  for Single Absorbers, with a Cross-Dictionary-Replicated KG Repair/Surgical-Edit Spine — Now Gated on Beating a SUB-CONTEXT-TARGETED
  Dense Baseline and Landing a Safety-Relevant Absorption-Structured Win
hypothesis: |-
  ITERATION-5 STATUS -- THE TWO ITER-4 GATES WERE BOTH EXECUTED; CROSS-DICTIONARY (M2) GENUINELY LANDED, BUT THE DOWNSTREAM-WIN (M1) HEADLINE RESTS ON TOO WEAK A DENSE BASELINE AND THE SIGNIFICANCE CEILING IS UNMOVED. Iteration 5 delivered the iter-4 mandate on the FROZEN Gemma-Scope L12/16k JumpReLU SAE plus a second dictionary: an M1 selective-unlearning downstream comparison [art_9muVcI4tkqJf]; an M2 cross-dictionary replication [art_4L1MZxvWYlGd]; a fully-run M6 recall-hole router [art_4q5Om8wdqZuz]; an M7 second-absorption-case search [art_Iy77UHoNaIhS]; an honest-counting consolidation eval [art_-k4Yg-l4NaNO]; an M1/M2 positioning + citation audit [art_y_5u-bfJOq3V]; and a four-hierarchy homograph entity testbed BUILT BUT UNUSED [art_2xQn686KUmV5]. What honestly landed, and what the iter-5 reviewer exposed:

      - M1 DOWNSTREAM 'WIN' EXECUTED -- 2/4 CONFIRMED, BUT AGAINST A WHOLE-PARENT DENSE BASELINE => NEAR-TAUTOLOGICAL (reviewer MAJOR-1, the new #1 blocker) [art_9muVcI4tkqJf]. At matched forget-quality, ablating ONE KG-named absorber (KG-ABL) was scored against a dense diff-of-means parent erasure (DENSE-ABL). 2 of 4 cases DOWNSTREAM_WIN_CONFIRMED on the joint (retain-utility x fluency) judge metric: taxonomic Georgia (16009) joint Delta +0.423 CI[0.274,0.571], first-letter large (8463) Delta +1.646 CI[1.479,1.799] (dense 'starts-with-L' erasure collapses utility to 0.17/2 while KG holds 1.82/2); United States (846) PARTIAL (collateral favors KG, fluency CI incl 0); toxicity insult (13367) EXPECTED_LOSS (firing-Jaccard 0.882, co-firing, joint CI incl 0). Curve-dominance 1.00 on all 4; judge $0.44/876 calls. BUT the reviewer VERIFIED IN CODE that the dense direction u is the WHOLE-PARENT (country-vs-non-country / L-vs-not-L) direction (core.py ParentProbe; method.py L454/L535 fit_pos=all-countries, fit_neg=non-country). The paper's load-bearing STRUCTURAL claim -- 'a single dense hyperplane structurally cannot localize to a sub-context' and 'erasing the is-a-country direction removes all countries' -- IS FALSE: a diff-of-means on Georgia-in-country-contexts vs OTHER-countries-in-country-contexts (the testbed already carries these per-sub-context labels, since they define the forget/retain/sibling eval sets) is ALSO a single dense hyperplane AND localizes. Worse, the matched-forget sweep cranks beta until the whole-parent direction forgets the TARGET token, which BY CONSTRUCTION nukes siblings => high dense collateral is guaranteed => the win is near-tautological. As stated, 'first demonstration a discovered single SAE feature beats a dense baseline on sub-concept removal' is NOT established; only 'beats whole-parent erasure' is.

      - M2 CROSS-DICTIONARY REPLICATION -- GENUINELY LANDED [art_4L1MZxvWYlGd]. The four-piece spine (homograph holes, FDR repairs, Georgia surgical edit, recall-hole router) re-ran on a 4x-wider 65k-canonical SAE (same model+layer) and on layer-9 width-16k. 65k = FULL replication: Georgia recall-hole 0.873/jaccard 0.0038 (re-derived anchor 31478, corpus-fire 0.916), Jordan hole 0.746; 52 distinct holes survive BH-FDR (spelling 29/taxonomic ~8-11/numeric 15) vs 22 at 16k = the literature-PREDICTED 'wider absorbs more' (Karvonen2025/Chanin2025); router frozen tau_h transfers at balanced-acc 1.0; regime split clean. Layer-9 = PARTIAL and INFORMATIVE: the absorption PHENOMENON persists but the absorbed TOKEN shifts -- Georgia LOSES its hole (0.003, layer-9 parent already covers it) while Jordan GAINS one (0.536) and its single-absorber edit becomes surgical (2376x); spelling/numeric repairs drop to 0. Honest, literature-predicted (layer, width)-dependence. This gate is met.

      - M2 SELECTIVITY-ARTIFACT (reviewer MINOR): the 65k 'Georgia surgical edit at 3.7e6 selectivity / regime-mean 466997' is a DIVIDE-BY-EPSILON artifact -- absorber 46143 has kg_collateral=0.0 EXACTLY, so ratio=on_target/max(coll,1e-8)~3.7e6; at 16k the same edit has coll 2.9e-5 => 1722x. The dictionaries are COMPARABLY surgical (both collateral at/below numerical precision), NOT '2000x better'; the regime-mean is also inflated by a NO_ON_TARGET_EFFECT case (60904, 22486x). Must report floor-limited cases as 'collateral < numerical precision; selectivity floor-limited (>=X)' and EXCLUDE floor-limited + NO_ON_TARGET from any mean/median.

      - M6 ROUTER FULLY RUN -- recall-hole-alone is the lead, BUT it is AT CHANCE OUT-OF-SAMPLE (reviewer MINOR) [art_4q5Om8wdqZuz]. 31 concepts (12 derivation, 19 prospective). RECALL-HOLE-ALONE (tau_h 0.779) is the strongest single derivation separator: balanced-acc 1.0, NO derivation counterexample; firing-Jaccard-alone only 0.917 (DEMOTED to corroborating; numeric high-J yet absorption, aggregated-taxonomic low-J yet co-firing); the conjunction does NOT beat recall-hole-alone out-of-sample (parsimony => recall-hole-alone). BUT prospectively: absorption-predicted hit-rate 3/6=0.50 (EXACTLY chance, Wilson [0.19,0.81]); combined 11/18=0.61 Wilson [0.386,0.797] INCLUDES 0.5; and recall-hole fired 1.0 on NEW letters F/M/W that MEASURED co-firing (false-absorption misses). So derivation bal-acc 1.0 is on the FITTING set and the router is NOT yet a validated a-priori predictor. The built-but-unused homograph entity testbed (23 cities/12 months/34 names/24 brands) [art_2xQn686KUmV5] is the obvious lever to expand the prospective set to a CI that excludes 0.5.

      - M7 SECOND ABSORPTION CASE -- absorption REMAINS NARROW (the expected honest negative) [art_Iy77UHoNaIhS]. A clean PROFESSION is-a hierarchy (28 professions, 13,843 bias_in_bios bios, corpus-only parent 12692 recall 0.973) shows UNIFORM-HIGH parent recall 0.88-1.00, max hole 0.116 (profession 'model'), 0/28 absorption_type => absorption does NOT generalize to a clean is-a hierarchy. On 'model' the set-cover unit degenerates to the bare parent (AUC 0.308) and LOSES to g (0.544) and the dense probe (0.961) -- the honest contrast that the method only helps where an absorption SIGNATURE exists. Taxonomic re-run reproduces iter-4 EXACTLY: absorption_type True for EXACTLY {Georgia (n=150 eligible, hole 0.80, J 0.059, AUC 0.995, set_cover_established), Jordan (n=124<150 DESCRIPTIVE, hole 0.71)}; entity scan over 20 country surfaces with >=150 occurrences yields NO new case (Jordan n=124). So affirmative non-spelling set-cover evidence is STILL effectively one eligible slice (Georgia), 1-2 with descriptive Jordan.

      - HONEST COUNTING CONSOLIDATED [art_-k4Yg-l4NaNO]. 69 repair variants, 30 survive BH-FDR<=0.05, spanning 22 DISTINCT recall holes (NOT 23: 30 - 6 double-counts(kg_ktrack==kg_diagnostic identical latent: Georgia/16009, Jordan/540, US/846, date/8684, decimal/7983, ordinal/13658) - 2 NON-hole survivors(numeric percent/9112 AND L/layer/2378, both is_hole=False) = 22). Per-family distinct: spelling 13, taxonomic 3, numeric 6. Selectivity: absorption set n=6 MEAN 1452.5x / MEDIAN 1262.2x (the draft's '1452x median' is the MEAN); cleanly-surgical n=5 median 1722.5x (excludes partial-surgical US-4760 @7.8x). Precision-vs-selectivity Spearman: all-7 rho 0.679, within-taxonomic-5 rho 0.900 (NOT 1.0; cross-family counterexample large prec 0.571->802x beats US-4760 prec 0.709->7.8x) => SOFTEN to within-family tendency. Control = random SINGLE content-responsive-latent addition (28/28 clear p95, 23/28 clear p99); drop the 'full population' phrasing. Member-labeling 0.730 vs shuffle 0.096 (gap CI[0.545,0.724]); compact-vs-15wide AUC cost -0.056..-0.200.

      - UNITED STATES IS INTERNALLY INCONSISTENT (reviewer MINOR). In M1 it is regime='absorption' PARTIAL-win, but its artifact values are firing-Jaccard 0.040 (for absorber 846) yet PARENT RECALL-HOLE 0.197; in the selection/router story 'US is co-firing/splitting (J 0.20 aggregate, hole 0.23), not absorption' and the router (predict absorption iff hole>0.78) classifies US as CO-FIRING. So US is used as an 'absorption' unlearning case while the router predicts co-firing -- if anything, US is a router COUNTEREXAMPLE (CCRG helps where the router said it should not). Must pick ONE classification (US = co-firing per hole<0.5 and router) and either move US out of the absorption-unlearning set OR present it explicitly as a router false-negative, and explain the 0.04(specific-absorber-846)-vs-0.20(aggregate-detector) firing-Jaccard discrepancy.

      - HEADLINE JOINT-OUTCOME RESTS ON A SINGLE LLM JUDGE (reviewer MINOR). claude-haiku-4.5 temp 0, small per-case n (48-56 judged prompts), no human validation, no second-judge agreement; the model-internal KL/PPL corroboration DISAGREES with the judge on toxicity (leans KG 'UNEXPECTED_WIN'). The centerpiece's robustness to judge choice is unestablished.

      - TWO-TRACK ALGORITHM IS LARGELY INERT IN THE LOAD-BEARING RESULTS (reviewer MINOR). The C-track ties weak baselines on its only tested family (toxicity AUC 0.762 vs (a) 0.765, 'secondary' even in the artifacts); set-cover-SPECIFIC selection holds on only I, D, Georgia (on L/O/T the strong S-rec matches the unit); and the downstream wins + surgical edits trace to INDIVIDUAL discovered absorber latents (16009, 8463, 846), NOT multi-member grouping. So 'a two-track grouping algorithm' as a headline contribution exceeds what the experiments show grouping ADDS over 'find the anchor's recall hole and pick the precise specialist that covers it.'

      - MODEL-DIFFING stays a confound-bounded NULL (genuine shift +0.000 CI[-0.009,0.007]) [art_jI2KIJotjzIU]; steering stays a generality demo (surgical on L,D) [art_0ueMMR8Tt02P].

      WHAT THE ITER-5 REVIEW EXPOSED -- TWO MAJORS THAT GATE PUBLICATION, PLUS FIVE MINORS:
        (R1, RIGOR -- the new #1 blocker) The M1 downstream win is near-tautological because the dense comparator was a WHOLE-PARENT erasure swept until it nukes the target token. A SUB-CONTEXT-TARGETED dense direction (built from the same sub-context labels the eval already uses) also localizes. => ITERATION 6 MUST re-run M1 against u_sub = diff-of-means(target-sub-context-positive, sibling-positive), same erase operator, swept to matched forget, scored with the identical judge. FORK: if KG still wins (CI excl 0) the contribution is DRAMATICALLY stronger; if KG only MATCHES u_sub, REFRAME to a LABEL-EFFICIENCY/DISCOVERY claim ('KG-ABL matches a sub-context dense direction WITHOUT needing sub-context labels') and DROP the false 'structurally cannot localize' argument.
        (R2, SCOPE -- the persistent ceiling, now sharpened) No SAE unit out-classifies a dense probe on ANY task; the two confirmed wins are 'Georgia is a country' and the spelling of 'large' (neither safety-relevant, the latter vs an erasure that corrupts all L-tokens); toxicity -- the only safety-relevant family -- is a predicted LOSS; set-cover-specific selection is only 3 slices; the prospective router is at chance. The practical reliability gain is delivered as AUDITABILITY/LOCALIZATION on a narrow homograph phenomenon (Georgia + descriptive Jordan on one model), not as task performance -- narrow for an ICLR-primary target. => ITERATION 6 MUST search for at least ONE SAFETY-RELEVANT, ABSORPTION-STRUCTURED sub-context (an identity/dialect/demographic token, a named-entity safety case, or a bias/toxicity SUB-TYPE that -- unlike the aggregate toxicity sub-attributes -- shows a parent recall hole) and land the downstream win there against the stronger u_sub baseline; even ONE such win converts 'a capability a probe lacks' into 'a better outcome on a task that matters.' If NO safety-relevant attribute is absorption-structured, that honest-null SCOPING finding (absorption is confined to homograph/polysemy entity tokens + spelling, not safety attributes) is itself publishable but CAPS the contribution and must be the headline limitation.
        (R3-R7, MINORS) selectivity: exclude floor-limited + NO_ON_TARGET, report floor-limited as '>=X', state 16k/65k comparably surgical; router: state prospective CI includes 0.5 and recall-hole over-predicts on new spelling letters -- DEMOTE to 'exploratory diagnostic, not yet validated' OR expand the prospective set with the built homograph entity testbed to exclude 0.5; US: classify as co-firing consistently and reconcile; judge: add a second different-family judge + human spot-check on Georgia/large, confirm Delta_joint CIs still exclude 0; grouping: ablate unit-vs-single-best-absorber OR re-balance the narrative to position the algorithm as the label-free DISCOVERY PROCEDURE for single absorbers.

      THE ITERATION-6 MANDATE (the two MAJORS are load-bearing; nothing else gates until they exist):
        (M1' = NEW LOAD-BEARING -- THE STRONGER DENSE BASELINE) Re-run the selective-unlearning comparison [art_9muVcI4tkqJf] with the decisive comparator being u_sub = diff-of-means(target-sub-context-positive, sibling-positive in the SAME parent context), erased via h <- h - beta(h.u_sub)u_sub, swept to MATCHED forget-quality, scored by the IDENTICAL judge + model-internal KL/PPL. Report KG-ABL vs u_sub (and keep whole-parent DENSE-ABL only as a clearly-labeled SECONDARY reference, never the headline). If KG-ABL beats u_sub (joint CI excl 0) on >=1 case, headline 'a discovered single SAE feature beats even a sub-context-labeled dense direction.' Otherwise headline the LABEL-EFFICIENCY claim: KG-ABL matches u_sub without sub-context labels (the absorber is discovered label-free by interventional grouping; u_sub requires the sub-context partition). DELETE the 'structurally cannot localize' / 'removes all countries' framing throughout.
        (M2' = NEW LOAD-BEARING -- A SAFETY-RELEVANT ABSORPTION-STRUCTURED WIN, the significance ceiling) Use the router recall-hole screen + the homograph entity testbed [art_2xQn686KUmV5] + a new safety-oriented corpus to FIND a safety-relevant attribute whose sub-contexts are suppressed-parent + mutually-exclusive (e.g. a specific demographic/dialect/identity token absorbed under a general 'identity/group' parent; a named-entity safety case). Run the M1' downstream comparison there against u_sub. A single win = the largest available score lever (converts auditability into task performance on something that matters). An honest-null (no safety attribute is absorption-structured) is publishable but caps the contribution and is the headline limitation.
        (M3 = SELECTIVITY ARTIFACT) Exclude floor-limited (kg_collateral < numerical precision) AND NO_ON_TARGET_EFFECT cases from every mean/median selectivity; report floor-limited as 'selectivity floor-limited >=X (collateral below numerical precision)'; state 16k and 65k Georgia edits are COMPARABLY surgical (both collateral at/below precision), not 2000x apart; re-derive the regime-split number without the 46143/60904 artifacts.
        (M4 = ROUTER OUT-OF-SAMPLE) State explicitly the prospective Wilson CI [0.386,0.797] INCLUDES 0.5 and recall-hole=1.0 over-predicts absorption on new spelling letters F/M/W. EITHER demote the router to 'an exploratory diagnostic, not a validated a-priori predictor' OR expand the prospective set with the built homograph entity testbed (23 cities/12 months/34 names/24 brands -- many genuine suppressed-parent candidates) to obtain a CI that EXCLUDES 0.5. Keep derivation/prospective strictly separate; recall-hole-alone stays the lead, firing-Jaccard corroborating.
        (M5 = US CONSISTENCY) Classify United States ONCE, consistently, as CO-FIRING (parent recall-hole 0.197/0.23 < 0.5; router threshold 0.78 => co-firing). Move its unlearning result OUT of the 'absorption regime' set and present it as a case where the single-absorber edit (846) gives a PARTIAL win even though the router predicted co-firing (a router false-negative to discuss), and explain the firing-Jaccard discrepancy (0.04 for the specific absorber 846 vs 0.20 for the aggregate detector).
        (M6 = JUDGE ROBUSTNESS) Re-score a stratified sample of the unlearning continuations with a SECOND, different-family judge (GPT- or Gemini-class) and report inter-judge agreement; add a small HUMAN spot-check on the Georgia and large cases. Confirm the Delta_joint CIs still exclude 0 under the second judge before keeping M1' as the centerpiece.
        (M7 = GROUPING'S MARGINAL VALUE) Either run an explicit ABLATION isolating the multi-member unit's marginal value over the single-best-absorber on the downstream + auditability tasks (unit vs single-discovered-absorber), OR RE-BALANCE the narrative so the two-track algorithm is positioned as the LABEL-FREE DISCOVERY PROCEDURE that surfaces the precise single absorber a marginal-attribution ranking drops (and multi-member units only where they genuinely exist, e.g. first-letter pools and the rebuilt Georgia unit). The set-cover machinery's demonstrated job is PROPOSING the precise specialist, not delivering multi-member classification wins.
        (M8 = HONEST COUNTING + PRESENTATION) Carry the eval's corrected numbers verbatim: 22 DISTINCT holes (30 = repair variants over 22, de-dup the 6 identical kg_ktrack==kg_diagnostic latents, flag the 2 non-hole survivors); mean 1452x / median 1262x selectivity with the n=6 absorption set and n=5 cleanly-surgical set stated; rho 0.90 within-taxonomic (soften 'precision predicts surgicality'); control = random SINGLE content-responsive-latent addition; numeric flagged below-gate (digit-token cosine 0.876<0.9). Keep the locked citation venues [art_y_5u-bfJOq3V, art_QBxBPF-9Ldxe, art_i-tkvFCKneA-] (Chanin NeurIPS-2025; AxBench/SAEBench ICML-2025; CanonicalUnits ICLR-2025; Farrell NeurIPS-2024 Safe-GenAI Workshop; SAUCE->ICCV-2025 CVF; CRISP ACL-2026; SSPU EMNLP-2025; PS-Eval/SAE-TS/SRS/LEACE/Peng cite-and-distinguish). Strip iteration/rebuttal/infra scaffolding.

      RE-DESIGNATED HEADLINE (auditability-and-discovery-first; SAME two-track method; the two NEW gates make or break the contribution). On a FROZEN public SAE, interventional grouping by co-response to content counterfactuals is a TRAINING-FREE, LABEL-FREE DISCOVERY PROCEDURE that surfaces the single precise absorber latent a marginal-attribution ranking silently drops, plus a feature-level KNOWLEDGE GRAPH whose edges carry MEASURED, localized repair utility: a KG-named absorber added to a suppressed parent recovers its recall hole, beating a random SINGLE-latent-addition control (22 distinct holes survive FDR across spelling/taxonomic/numeric), and ablating that absorber surgically edits ONE sub-context (mean 1452x / median 1262x selectivity over collateral, floor-limited cases excluded) -- a localization that REPLICATES on a 4x-wider SAE (with MORE absorption, as the literature predicts) and partially across a layer (where the absorbed token shifts). The CENTRAL OPEN CLAIM iteration 6 must close is whether ablating the discovered single absorber BEATS -- or, failing that, MATCHES WITHOUT SUB-CONTEXT LABELS -- a SUB-CONTEXT-TARGETED dense direction (not merely whole-parent erasure) on a joint collateral+fluency outcome, AND whether such a win can be landed on a SAFETY-RELEVANT, absorption-structured sub-context. The method does NOT out-classify a strong non-SAE dense probe on any task; absorption is NARROW (homograph-polysemy entity tokens + first-letter spelling, NOT a clean is-a hierarchy -- 0/28 professions); the router is a derivation-perfect but out-of-sample-UNVALIDATED screen; and the durable value is AUDITABLE, EDITABLE, LABEL-FREE-DISCOVERED, REGIME-TARGETED repair -- fully established only once the stronger-baseline (M1') and safety-relevance (M2') gates are met.

      PRIMARY ENDPOINT (re-designated; the two gates are load-bearing).
        (a) STRONGER-BASELINE DOWNSTREAM TEST (NEW LOAD-BEARING, M1'): KG-named single-absorber ablation vs a SUB-CONTEXT-TARGETED dense direction u_sub at matched forget-quality on the joint outcome; a WIN (CI excl 0) is the strong contribution, a MATCH is the label-efficiency contribution (discovered handle, no sub-context labels), and only those two are publishable headlines -- 'beats whole-parent erasure' is retired.
        (b) SAFETY-RELEVANT ABSORPTION-STRUCTURED WIN (NEW LOAD-BEARING, M2'): at least one safety-relevant, suppressed-parent sub-context where the M1' comparison holds; honest-null (no such structure exists) caps and is the headline limitation.
        (c) CROSS-DICTIONARY REPLICATION (ACHIEVED, M2): 65k full, layer-9 partial (token shifts) -- KEEP, with the selectivity artifact corrected.
        (d) AUDITABILITY SPINE (achieved, honestly re-counted): 22 distinct-hole FDR repairs over a random single-latent control [art_sxwT7hK6YFEA, art_-k4Yg-l4NaNO]; surgical edits [art_0CZwPjG2YMCf]; member-labeling beats shuffle null.
        (e) ROUTER: recall-hole-alone reproduces on derivation (bal-acc 1.0) but is OUT-OF-SAMPLE-UNVALIDATED (prospective CI includes 0.5) -- DEMOTE or expand-prospective via the homograph testbed.
      SUPPORTING (strengthen, do not gate): within-SAE set-cover selection where the router predicts absorption (first-letter I,D; taxonomic Georgia); member-labeling above null; the steering demo (L,D). E2 absorbed-slice recall significant on T only. The headline NO LONGER depends on classification beating attribution, on multi-member grouping beating single absorbers, or on the router being a validated predictor.

      THE TWO-TRACK CLUSTERING ALGORITHM (specification unchanged; now framed as the label-free DISCOVERY PROCEDURE). STEP 1 cover-based eligibility (content-responsive above a shuffle null; firing-precision>=0.7; covers>=1 sub-context). STEP 2 C-TRACK (splitting): positive-Spearman soft-threshold affinity (beta=6, WGCNA) -> Leiden RBConfiguration; resolution by bootstrap-ARI stability. STEP 3 K-TRACK (absorption, anchored greedy max-coverage): ANCHOR = argmax cover-set chosen WITHOUT the diagnostic, with the UNSUPERVISED FIRING-FLOOR PARENT-VALIDATION (anchor must fire on held-out corpus above ~5% -- fixes the letter-I 0%-corpus spurious anchor); HOLES = parent's uncovered pairs; greedily add mutually-exclusive (firing-Jaccard<0.1), PRECISE (>=0.7, gated on a HELD-OUT fold) absorbers covering holes with marginal-gain>=0.05 CI excluding 0; the coverage objective is PRECISION-GATED / precision-WEIGHTED (Georgia selects 16009 prec .955, not 4697 prec .35). STEP 4 reconcile C-communities and K-covers, de-duplicate by highest coverage gain. STEP 5 ADMISSION: signature C OR matched-null signature K (+ small-k absolute gain>=0.05 CI excluding 0, mutual-exclusivity, precision floor) AND unit-level surface invariance; multiplicity controlled at unit-proposal level (Bonferroni-within-unit then BH across M candidates). The DEMONSTRATED value of this machinery is PROPOSING the precise single absorber that marginal attribution drops; multi-member grouping's marginal value over the single-best absorber is to be ablated or scoped (M7).

      SAE-LATENT FIRING-STRUCTURE ROUTER (screening DIAGNOSTIC, derivation-perfect but out-of-sample-unvalidated; RECALL-HOLE-PRIMARY). One forward pass: encode, identify the firing-floor-validated content-responsive parent, find per-sub-context detectors, report (i) parent per-sub-context recall holes and (ii) detector-vs-parent positive-only firing-Jaccard. RULE: predict absorption-regime iff the parent has a recall HOLE (>~0.78) -- balanced-acc 1.0 on the 12 derivation concepts, no derivation counterexample -- CORROBORATED by low firing-Jaccard (<~0.05-0.10). HONEST STATUS: prospectively only 3/6 (chance) on predicted-absorption and 11/18 overall (Wilson CI includes 0.5); recall-hole=1.0 over-predicts on new spelling letters F/M/W. Treat as an exploratory diagnostic until the prospective CI excludes 0.5 (expand via the homograph entity testbed). Firing-Jaccard alone is insufficient (numeric high-J absorption, aggregated-taxonomic low-J co-firing). Co-firing (toxicity threat 0.40, identity_attack 0.29, insult 0.66 >> 0.10, no parent hole) => supervised attribution wins and CCRG does not help.

      BASELINE GLOSSARY (matched baselines primary; the decisive M1' comparator is NEW). (a) best raw single latent; (b)/(c) observational co-activation/decoder clusters COUNT-MATCHED to k; (d) counterfactual diff-of-means; (e) raw-residual probe; (f) WHOLE-PARENT LEACE/diff-of-means erasure (DEMOTED to secondary reference for the edit); (g) SCR/TPP oracle pool; (h) count-and-pool-matched SCR/TPP probe; (i) unmatched diff-of-means; (j) oracle group-DRO; (k) label-free group-inference (JTT/GEORGE); (RE-k) random-eligible-k floor; (S-rec)/(S-prec)/(S-mag) non-random label-free selectors (set-cover isolated by beating these). NEW DECISIVE COMPARATOR (u_sub): SUB-CONTEXT-TARGETED dense direction = diff-of-means(target-sub-context-positive, sibling-positive in the same parent context), erased via the same operator and swept to matched forget -- this is the honest dense baseline for the M1' downstream edit, replacing whole-parent (f) as the headline comparator. (k) cannot localize (decoder-projection argmax is the parent, never an absorber).

      NON-SPELLING TESTBED (HOMOGRAPH-POLYSEMY ABSORPTION; affirmative selection still n=1-2). Absorption recurs on HOMOGRAPH/POLYSEMOUS tokens whose general parent is suppressed -- taxonomic absorption-type slices are EXACTLY Georgia (eligible, hole .80) + Jordan (DESCRIPTIVE n=124<150, hole .71); United States is CO-FIRING (firing-Jaccard .20, hole .23, NOT absorption -- classify consistently); all other countries ~0 hole; a clean PROFESSION is-a hierarchy is 0/28 (uniform-high parent recall) => absorption is polysemy-specific, NOT broad taxonomic/is-a. Iteration 6 (M2'/M4) uses the built homograph entity testbed [art_2xQn686KUmV5] (cities/months/given-names/brands) to find more suppressed-parent cases AND expand the router prospective set. Numeric = below-gate (digit cosine 0.876<0.9), eligibility+pooling, diagnostic-unconfirmed (integer co-firing J=.256; dense probe AUC 1.000). A non-SAE dense probe matches/beats the unit on ALL non-spelling classification.

      SCOPE AND VALUE PROPOSITION. The defensible contribution is: (1) a TRAINING-FREE, LABEL-FREE DISCOVERY PROCEDURE (interventional two-track grouping) that surfaces the single precise absorber marginal attribution drops, with a MEASURED, EDITABLE feature-KG (recall-hole recovery beating a random single-latent addition; surgical single-absorber edits; (k) cannot localize) plus human/LLM-auditable members, REPLICATING across SAE dictionaries; (2) an a-priori RECALL-HOLE screening DIAGNOSTIC (derivation-perfect, out-of-sample-unvalidated) for when grouping helps; (3) a WITHIN-SAE absorption-regime selection win where it occurs (first-letter I,D; taxonomic Georgia). The OPEN, GATING questions iteration 6 must answer are whether the discovered single-absorber edit BEATS-OR-MATCHES-WITHOUT-LABELS a SUB-CONTEXT-TARGETED dense direction (M1') and whether such a win lands on a SAFETY-RELEVANT, absorption-structured sub-context (M2'). The method does NOT out-classify a strong dense probe; toxicity is a clean co-firing negative; absorption is narrow. HEADLINE = auditable, label-free-discovered, regime-targeted absorption repair-and-edit; classification is SUPPORTING and within-SAE.

      HONEST NEGATIVES (each publishable): the M1 'win' as run is against whole-parent erasure (near-tautological -- the stronger u_sub test is OWED); unit out-classifies NO non-SAE dense probe on any task; the two confirmed wins are non-safety-relevant (Georgia, 'large'); toxicity -- the only safety family -- is a predicted LOSS; set-cover-specific selection only 3 slices (Georgia, I, D); non-spelling affirmative selection effectively n=1 (Georgia), 1-2 with descriptive Jordan; 0/28 professions show absorption (narrow homograph-polysemy phenomenon); the router is at chance out-of-sample (prospective CI includes 0.5, over-predicts on new letters); cross-dictionary replicates at 4x width but only PARTIALLY across a layer (token shifts); the 65k 3.7e6 selectivity is a divide-by-epsilon artifact (16k/65k comparably surgical); the headline rests on a single LLM judge; the two-track grouping is largely inert (wins trace to single absorbers); the form-free MAGNITUDE diagnostic is precision-blind; compact named units cost AUC; numeric is below-gate and unconfirmed; model-diffing a confound-bounded null; steering surgical only on L,D. A clean failure of M1' (KG does not even match u_sub) or M2' (no safety attribute is absorption-structured) is the declared method-does-not-clear-the-bar outcome and is itself publishable.

      MOTIVATION (substance unchanged). Single SAE latents are unreliable units: feature absorption (a child latent suppresses a general parent's firing; Chanin 2409.14507, NeurIPS 2025), splitting, hedging (2505.11756), and 'SAEs Do Not Find Canonical Units' (ICLR 2025) converge on no single latent reliably tracking a concept; AxBench (ICML 2025) and DeepMind's negative report show plain diff-of-means beats raw-latent SAE methods, and Farrell (2410.19278) shows multi-feature SAE unlearning has side-effects >= RMU -- so any SAE method must clear strong dense baselines AND, for the edit, a SUB-CONTEXT-targeted dense direction, not just whole-concept erasure. Absorption is the regime where OBSERVATIONAL signals break by construction and MARGINAL-ATTRIBUTION selection silently drops the absorber; correlation-community detection handles shared-support splitting, anchored greedy set-cover handles disjoint-support absorption -- coverage-complementarity is a set-level property no pairwise affinity can express, which is why grouping is the right DISCOVERY operator for the absorber even if the multi-member unit's classification value over the single absorber is modest. Architectural remedies (Matryoshka/H-SAE/SASA) retrain and are orthogonal; their dictionary-size dependence is exactly why cross-dictionary replication (achieved) and the wider-absorbs-more signal matter.

      SUCCESS CRITERIA. METHOD CONFIRMED iff: (LOAD-BEARING) (M1') the KG-localized single-absorber edit BEATS (CI excl 0) OR MATCHES-WITHOUT-SUB-CONTEXT-LABELS a SUB-CONTEXT-TARGETED dense direction u_sub at matched forget on a joint on-target/collateral/fluency metric, confirmed under a SECOND judge; AND (M2') at least one such result lands on a SAFETY-RELEVANT, absorption-structured sub-context (or the honest-null 'no safety attribute is absorption-structured' is reported as the capping limitation); AND the cross-dictionary spine holds (65k full / layer-9 partial, selectivity artifact corrected); AND the auditability spine holds at the honest 22-distinct-hole count with the random single-latent control. SUPPORTING (strengthen, do not gate): within-SAE set-cover selection (Georgia, I, D); member-labeling above null; admission false-admit <=0.05; the recall-hole router on derivation (with prospective honestly reported as unvalidated or expanded to exclude 0.5); the steering demo (L,D). HONEST NEGATIVES are reportable and cap-but-do-not-sink: failure of M1' (KG cannot match u_sub) or M2' (absorption is not safety-relevant-structured), router-at-chance, layer-conditional replication, single-absorber-not-grouping attribution, numeric unconfirmed, toxicity co-firing negative.
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
  Same two-track auditability/discovery frame; swaps whole-parent for sub-context dense gate, adds safety-relevance gate.
_confidence_delta: decreased
_key_changes:
- >-
  Recorded iter-5 execution: M2 cross-dictionary REPLICATED (65k full, more absorption as predicted; layer-9 partial with
  absorbed-token shift); M1 unlearning ran 2/4 wins (Georgia +0.42, large +1.65) BUT vs a whole-parent dense baseline; router
  fully run (recall-hole bal-acc 1.0 derivation); M7 profession 0/28 (absorption narrow); honest-counting eval (22 distinct
  holes, mean 1452/median 1262).
- >-
  NEW LOAD-BEARING M1' (reviewer MAJOR-1): re-run the downstream edit vs a SUB-CONTEXT-TARGETED dense direction u_sub=diff-of-means(target-sub-context-pos,
  sibling-pos), not whole-parent erasure; the prior win is near-tautological. FORK: KG beats u_sub (strong) or KG matches
  u_sub without sub-context labels (label-efficiency/discovery claim). DELETE the false 'structurally cannot localize' argument.
- >-
  NEW LOAD-BEARING M2' (reviewer MAJOR-2, the significance ceiling): land >=1 downstream win on a SAFETY-RELEVANT, absorption-structured
  sub-context (identity/dialect/named-entity), vs u_sub; honest-null (no safety attribute is absorption-structured) caps the
  contribution.
- >-
  Demoted the router to an exploratory diagnostic: prospective 3/6 absorption (chance), 11/18 combined (Wilson CI includes
  0.5), recall-hole over-predicts on new letters F/M/W; expand prospective via the built-but-unused homograph entity testbed
  [art_2xQn686KUmV5] to exclude 0.5, or demote.
- >-
  Corrected the 65k '3.7e6 selectivity' as a divide-by-epsilon artifact (kg_collateral=0 -> /1e-8); 16k/65k comparably surgical;
  exclude floor-limited + NO_ON_TARGET cases from mean/median selectivity.
- >-
  Reclassified United States consistently as CO-FIRING (hole 0.197/0.23<0.5, router threshold 0.78): move out of the absorption-unlearning
  set or present as a router false-negative; explain the 0.04(absorber-846)-vs-0.20(aggregate) firing-Jaccard discrepancy.
- >-
  Added judge-robustness mandate (M6): second different-family judge + human spot-check on Georgia/large, confirm Delta_joint
  CIs still exclude 0; flag the single-judge centerpiece risk and the model-internal/judge disagreement on toxicity.
- >-
  Re-balanced the two-track algorithm to a LABEL-FREE DISCOVERY PROCEDURE for single absorbers (wins trace to latents 16009/8463/846,
  not multi-member grouping; C-track ties baselines; set-cover-specific selection only 3 slices) and mandated a unit-vs-single-best-absorber
  ablation.
- >-
  Adopted eval-corrected counts verbatim (22 distinct holes not 23/30; mean 1452x/median 1262x; rho 0.90 within-taxonomic;
  control=random SINGLE latent; numeric below-gate cosine 0.876).
- >-
  Confidence DECREASED: M2 and the auditability spine solidified, but the headline M1 downstream win was exposed as near-tautological
  against a too-weak baseline and the safety-relevant significance ceiling is unbroken until M1'/M2' are run.
relation_type: evolution
</hypothesis>

<artifact_direction>
Make this direction concrete and actionable. Keep the same type and respect dependencies.

id: dataset_iter6_dir3
type: dataset
objective: >-
  FORWARD M2' BUILDING BLOCK — a clean, validated, reusable SAFETY-RELEVANT identity/demographic absorption TESTBED for next
  iteration's DECISIVE M2' run and for paper credibility, so the safety-relevance gate can be answered on a proper corpus
  rather than rough inline slices. Provide content-flip pairs + surface-flip pairs + frozen Pile/civil_comments corpus windows
  for hierarchies whose specific tokens plausibly suppress a general identity parent (the Georgia-homograph absorption structure
  transposed to safety-relevant identity attributes), with an absorption_readiness manifest marking inferentially-powered
  groups.
approach: >-
  Pure CPU/text artifact (no SAE/model/activations), emitting the AII exp_sel_data_out schema as a structural DROP-IN of the
  iter-5 homograph entity testbed (read its run-tree workspace 3_invention_loop/iter_5/gen_art/gen_art_dataset_1, artifact
  art_2xQn686KUmV5: data.py/build_dataset.py/pipeline.py/schema.json/manifest.json) and the iter-1 taxonomic testbed (read
  3_invention_loop/iter_1/gen_art/gen_art_dataset_2, artifact art_t2uUbjSwpd3t) so the downstream K-track + form-free absorption
  diagnostic pipeline runs unchanged. Build a SAFETY-RELEVANT identity absorption testbed over hierarchies whose specific
  tokens plausibly suppress a general identity parent: (1) nationality_absorption (parent = is-a-nationality; demonyms American/Chinese/Mexican/Nigerian/Russian/...);
  (2) religion_absorption (parent = is-a-religion; Muslim/Christian/Jewish/Hindu/Buddhist/Sikh/...); (3) ethnicity_identity_absorption
  (parent = identity-group-mention; race/ethnicity/identity terms); (4) named_entity_safety (parent = is-a-public-figure/org;
  specific entity tokens, prioritizing those with a dominant non-identity sense where available). For each hierarchy build
  the SAME three coordinated components as dataset_2/the homograph testbed: (A) content-flip minimal pairs (identity token
  present vs surface-matched absent at the same slot), (B) surface-flip pairs (identity fixed, carrier varied, for the unit-level
  surface-invariance admission check), (C) a frozen monology/pile-uncopyrighted (pinned rev 3be90335b66f24456a5d6659d9c8d208c0357119)
  diagnostic corpus of real windows labelled by frozen, MODEL-INDEPENDENT sub-context (the specific group), plus a matched
  hard-negative family (other-group / non-identity) so a suppressed parent is visible. Anchor tokens in the real gemma-2-2b
  vocab with precomputed token indices; assign sub-context labels PURELY from surface form / gazetteers (pycountry for nationalities;
  curated religion/ethnicity lists; disambiguating local context) so the degenerate-construction guard holds and absorption
  presence stays an EMPIRICAL question (the corpus equally supports the 'no safety absorption' null and a positive finding).
  Deterministic templated backbone + small OpenRouter generation (openai/gpt-4o-mini or google/gemini-flash-lite) with an
  INDEPENDENT LLM-judge gate (content_flipped / surface_preserved / grammatical + sense-correct), reporting pass rates and
  spend (hard $10 cap, target <$3). Frozen folds (pairs 70/30 train/test by pair_id stratified by sub_context; corpus 50/50
  train/diagnostic stratified by doc). Record an absorption_readiness manifest (>=150 diagnostic-fold positives = eligible,
  else descriptive_only), eligible_entities_per_hierarchy, per-component counts, llm pass rates + cost, and cross-hierarchy
  collision notes. Deliver data.py (canonical builder), full/mini/preview_data_out.json, schema.json, manifest.json, pyproject.toml
  (pinned). Validate all variants <100MB. Clearly mark as a NEXT-ITERATION building block (NOT consumed by this iteration's
  parallel experiments). Use aii-hf-datasets/aii-web-tools for gazetteers and corpus.
depends_on:
- id: art_I2MrezW41iQo
  label: guidance
  relation_type:
  relation_rationale:
</artifact_direction>

<dependencies>
Completed artifacts this artifact can use during execution.

--- Dependency 1 ---
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

DATASET executor scope:
  Output: data_out.json with rows of {input, output, metadata_fold, ...} — raw data only, no derived computations
  DOES: Download/generate datasets, analyze candidates to pick the best ones, standardize to JSON schema (features, labels, folds, metadata), validate schema, split into full/mini/preview
  DOES NOT: Run experiments, train models, compute derived statistics (PID/MI/correlations/synergy matrices) as final output
  If you need to COMPUTE something from data (synergy matrices, MI scores, timing benchmarks), use an EXPERIMENT artifact instead
</artifact_executor_scope>

<artifact_planning_rules>
DATASET:
- Plan for REAL third-party datasets (HuggingFace, Kaggle, direct-download URLs) — downloadable within time and size constraints
- Describe dataset criteria (domain, size, format) — executors find exact sources, but you can suggest candidates or search directions
- ALWAYS prefer real datasets over synthetic. Synthetic is a LAST RESORT only when no suitable real data exists
</artifact_planning_rules>

<compute_profiles>
Choose the compute profile this artifact needs for execution.
Available profiles for dataset artifacts:
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
  "description": "Plan for a DATASET artifact.",
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
    "ideal_dataset_criteria": {
      "description": "What makes an ideal dataset for this purpose - size, format, content requirements",
      "title": "Ideal Dataset Criteria",
      "type": "string"
    },
    "dataset_search_plan": {
      "description": "Step-by-step plan for finding/creating this dataset - sources to check, fallback options",
      "title": "Dataset Search Plan",
      "type": "string"
    },
    "target_num_datasets": {
      "description": "How many individual datasets should be delivered. Count each dataset separately, not collections \u2014 a benchmark suite of N datasets counts as N. This controls how broadly the executor searches, so setting it too low will under-collect.",
      "title": "Target Num Datasets",
      "type": "integer"
    }
  },
  "required": [
    "title",
    "ideal_dataset_criteria",
    "dataset_search_plan",
    "target_num_datasets"
  ],
  "title": "DatasetPlan",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-06-18 05:04:53 UTC

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

### [3] SKILL-INPUT — aii-web-tools · 2026-06-18 05:06:19 UTC

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
