# gen_plan_experiment_2 — test_idea

> Phase: `invention_loop` · round 10 · `gen_plan`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_plan_experiment_2` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-19 00:39:57 UTC

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

<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>
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
  Training-Free, Label-Free LOCALIZATION of Homograph-Polysemy SAE Absorption (Spine + Coverage Screen SOLID; Clustering INERT;
  All Three Goal Downstream Tasks NULL): The Iter-9 Label-Scarce "Where-to-Gate Win" Is CIRCULAR -- the Label-Free Handle
  Secretly Reused Absorber IDs PRE-DISCOVERED WITH FULL LABELS, So the Net Saving Is UNPROVEN. Iter-10 Must Prove GENUINE
  CROSS-DEPLOYMENT ZERO-LABEL TRANSFER / Report Break-Even-K* (or DROP the Where-to-Gate Thesis), and Demonstrate AVERTED
  COST + Ship an Absorber CATALOG to Turn the Screen From a Reassurance Instrument Into a Capability
hypothesis: |-
  ITERATION-9 STATUS -- THE THREE ITER-9 LOAD-BEARING PIECES EXECUTED. THE LOCALIZATION SPINE (re-controlled) AND THE CONFINEMENT-COVERAGE SCREEN LANDED SOLIDLY; BUT THE SINGLE NEW SAE-SPECIFIC POSITIVE -- THE LABEL-SCARCE "WHERE-TO-GATE VALUE" -- WAS EXPOSED BY REVIEW AS CIRCULAR, SO THE NET LABEL-SAVING REMAINS UNPROVEN. The honest contribution is therefore essentially unchanged in substance from iter-8: (i) auditable, label-free, regime-targeted LOCALIZATION of homograph-polysemy absorption (now STRENGTHENED against non-eval-aligned controls and TEMPERED to localization-not-utility); (ii) a quantified CONFINEMENT-COVERAGE result + a shipped label-free practitioner SCREEN; and (iii) a label-free WHERE-TO-GATE discovery whose NET BENEFIT over the labeled route is STILL UNDEMONSTRATED. Iteration 9 delivered: the label-scarce where-to-gate experiment [art_-zywGLxOcKOw]; the coverage screen + shipped tool [art_NIxb2uUvT-ze]; the strengthened-control repair spine + downstream-capability test [art_mHCB4FyqyMXL]; a $0 integrity-lock eval [art_A8o1h4sWckjw]; and a localization-commit / both-fork positioning audit [art_lkJ2wWVGDovC].

              WHAT LANDED.

              - M1'''' LABEL-SCARCE WHERE-TO-GATE EXECUTED [art_-zywGLxOcKOw], $0.34, 2 judges. Internal verdict DEMONSTRATED_WHERE_TO_GATE_VALUE: varying label budget n in {0,1,5,20,full} for the supervised fair gate (u_sub(n) + d_sub(n)), the LABEL-FREE SAE firing gate held localization balanced-accuracy 0.97-1.0 (flat in n, all 5 cases) while the dense gate COLLAPSED at n=1 (0.67-0.73, CI-separated below) and only MATCHED at n=20/full; edit-arm preservation advantage adv_pres = +0.81 (large) / +0.91 (Amazon) at n=1 converging to 0.000 at full labels. Georgia/Jordan/US were WEAK edit handles yet STRONG localizers (the iter-8 firing-signature != edit-handle finding turned positive on the localization axis). HOWEVER -- THE REVIEWER VERIFIED IN label_scarce.py THAT THIS RESULT IS CIRCULAR: the SAE handle's absorber IDs are HARD-CODED CONSTANTS (Georgia 16009, Amazon 6846, Bush 1418, Cook 15631, large 8463) that were DISCOVERED IN PRIOR ITERATIONS USING FULL PER-SUB-CONTEXT LABELS + ORACLE VALIDATION, while only the dense gate was restricted to n labels. So the comparison is "a handle that secretly used full-label discovery" vs "a from-scratch detector restricted to n labels"; the ONLY apples-to-apples point is n=full (where they MATCH, reproducing iter-8); the "saves 10-40 labels" headline is NOT netted against the SAE route's own discovery-time label cost; each absorber is sub-context-specific (Georgia's absorber is not Jordan's), so the amortization is real ONLY across repeated deployments of the SAME sub-context -- which the experiment NEVER exercises (fixed id, same data). The localization CURVES are real (a fixed-id firing gate is n-independent; a from-scratch dense gate needs ~5-20 labels to match; n=5 is already within ~0.03 balacc and the dramatic n=1 collapse is partly a diff-means-midpoint gate-CONSTRUCTION artifact); it is the SAVING INTERPRETATION that is circular. NET: the where-to-gate POSITIVE is downgraded from "demonstrated" to "curves established, net-saving UNPROVEN."

              - M3'''' COVERAGE SCREEN + SHIPPED TOOL EXECUTED [art_NIxb2uUvT-ze], $0. overall=COVERAGE_QUANTIFIED: 336 candidates over 10 hierarchies, 110 eligible; pooled STRICT coverage 6/110 = 5.5% (Wilson [0.025,0.114]); relaxed 31/336 = 9.2%. Absorption is HOMOGRAPH/NAMED-ENTITY-confined: strict-structured = Georgia (16009), Amazon/Bush/Cook (6846/9751/15631), borderline British/Greek; demographic religion 0/10, ethnicity 0/10, calendar months 0/12 ALL NO_HOLE; cities/given-names/most-brands 0; professions 0/28 (carried). First-letter spelling reproduces broadly (20/154 relaxed). Form-free oracle corroborates 27/31 structured (lexical 26/29 = 90%; Georgia the documented exception, decoder-cos ~0.01). Shipped screen.py + README. REVIEWER VERDICT: this is a REASSURANCE instrument ("the failure mode you feared is largely absent here"), NOT a capability; its build-on value is limited as written.

              - M5'''' STRENGTHENED REPAIR SPINE EXECUTED [art_mHCB4FyqyMXL], $0. KG-named absorber beats its named controls at FDR<=0.05 on 16/24 spelling+taxonomic holes (homograph-taxonomic 3/3; spelling 13/21); precision_specific=False (the win is WHICH latent covers the sub-context = coverage, not precision-magic); controls proven non-trivial (match-or-beat the KG on 6/7 numeric holes; S-mag recovers 45% of the Georgia hole yet is beaten +0.35). DOWNSTREAM-CAPABILITY NULL_TEMPER: the dense logistic probe OUT-RECALLS the repaired unit on 4/5 concepts (numeric -0.287, O -0.578, T -0.211, taxonomic -0.026; L ties), so the demonstrated value is auditable per-sub-context LOCALIZATION (a handle the single dense hyperplane lacks), NOT downstream recall utility. REVIEWER MINOR: the "four strictly stronger controls" count is INFLATED -- 2 of the 4 (dense-probe argmax under JTT and under diff-of-means) BOTH resolve to the PARENT, which by construction cannot recover its OWN hole, so they are VACUOUS-BY-CONSTRUCTION; the only informative controls are S-mag and S-rec. SECOND REVIEWER MINOR: the localization-arm metric (balanced-accuracy = TPR/TNR) is close to the firing-precision selection criterion, so the SAE handle's near-perfect balacc partly RESTATES why the latent was chosen; the non-tautological content is generalization to the disjoint eval fold.

              - INTEGRITY-LOCK EVAL [art_A8o1h4sWckjw], 47/49 cross-checks. Locks selectivity-AS-LOCALIZATION (the 16k selectivity denominator is the disowned DENSE-WHOLE-ABL strawman, footprint=1.0 on all 6; against the genuinely-fair conditional control the surgical advantage DISAPPEARS: fair collateral 2.79e-6 < KG 5.07e-5, FAIR-minus-KG CI excl 0; adv_KG_vs_FAIR ~ -0.05 CI incl 0; adv_KG_vs_SUB +0.97). Documented findings (recompute authoritative): distinct holes = 24 (NOT the carried 22; 6 of 30 survivors carry a 2nd variant); the 65k corrected MEAN is floor-recipe-dependent (721.7x vs robust 828.5x) but the MEDIAN 676.3x reproduces exactly -- paper must use ~676/722x, NEVER the 466997x divide-by-eps artifact. Carries 30 FDR survivors, member-labeling gap 0.634 [0.545,0.724], cross-dict 65k FULL/layer-9 PARTIAL (55/154 65k survivors), numeric digit-cos 0.876 below-gate, safety 2/44 homograph, named-entity 3/5, professions 0/28, router DEMOTED, model-diffing +0.000.

              - POSITIONING [art_lkJ2wWVGDovC]: localization reposition committed; both label-efficiency forks pre-written; confinement-screen 'so what' grounded in the SAE-reliability/auditing literature (Chanin reliability cites, Minegishi polysemy, Ahsan-Wallace co-firing corroboration); citation table locked.

              WHAT THE ITER-9 REVIEW EXPOSED -- TWO MAJORS THAT STILL GATE PUBLICATION, PLUS FOUR MINORS. Blunt summary: the iter-9 attempt to recover a DEMONSTRATED SAE-specific positive (the label-scarce where-to-gate) FAILED VERIFICATION (circular: full-label-discovered handle vs n-label dense), and SIGNIFICANCE remains the DOMINANT ceiling -- a confinement screen whose primary output is "the failure mode is largely absent here" is reassurance, not a capability others build on.
                (R1, EVIDENCE -- #1 evidence blocker) THE WHERE-TO-GATE 'WIN' DOES NOT DEMONSTRATE A NET LABEL SAVING. The SAE handle reused absorber IDs discovered with FULL labels + oracle; the saving is not netted against discovery cost; absorbers are sub-context-specific so amortization is only over repeated deployments of the SAME sub-context, never exercised. => ITER-10 MUST EITHER (1) DEMONSTRATE GENUINE TRANSFER (discover the id ONCE, apply the FIXED id with ZERO new labels to a DIFFERENT deployment of the SAME sub-context and beat an n-label dense gate fit fresh there) OR (2) EXPLICITLY NET OUT the discovery-time label cost and reframe as 'amortizable over K>=K* redeployments, break-even at K*', REPORTING K*. Also report the n=5 dense point (within ~0.03 balacc) as the honest practical comparison and note the n=1 collapse is partly a gate-construction artifact.
                (R2, SCOPE/SIGNIFICANCE -- #1 overall blocker) THE REPOSITION + SCREEN DO NOT BY THEMSELVES CREATE A CAPABILITY OTHERS WOULD BUILD ON. All three goal-named downstream tasks are nulls; clustering is inert; the phenomenon is confined to 6/110 eligible tokens and explicitly NOT the safety attributes the goal targets. => ITER-10 MUST RAISE SIGNIFICANCE BY DEMONSTRATING AVERTED COST: construct a concrete auditing scenario where absorption SILENTLY breaks a downstream artifact (a parent-latent/marginal-attribution classifier or a steer on an absorbed sub-context), show STANDARD PRACTICE does not flag it, the SHIPPED SCREEN catches it, and adding the named absorber REPAIRS the failure with a MEASURED benefit; PAIR with a PUBLISHED label-free-derivable absorber CATALOG over a public SAE suite so screen+catalog form a reusable resource.
                (R3, RIGOR -- minor) The 'four strictly stronger controls' count is inflated; 2 are vacuous-by-construction (parent cannot recover its own hole). => Reframe as 'beats the two label-free selectors S-mag and S-rec at FDR<=0.05 on 16/24 holes; the parent-argmax controls confirm they cannot recover the parent's own hole (vacuous by construction)'; keep the non-triviality (6/7 numeric) and precision_specific=False front and center.
                (R4, RIGOR -- minor) The localization metric (balanced-accuracy) is close to the firing-precision selection criterion (mild circularity). => State the coincidence explicitly, lean on held-out generalization, and ADD a SELECTION-INDEPENDENT localization metric (next-token behavioral KL targeting the sub-context vs siblings -- a metric the latent was NOT chosen to optimize).
                (R5, PRESENTATION -- minor) The BODY still reads as a rebuttal log ('the prior version conceded...', 'a reviewer rightly noted...', 'Honest ceiling' framed against prior versions). => Present corrected results AS results in the body; move EVERY 'prior version / a reviewer noted' reference into the appendix changelog; open the where-to-gate section directly with the experiment and its result.
                (R6, EVIDENCE -- minor) The Amazon edit caveat (adv_joint stays +0.52 at full labels, attributed to instrument disagreement, while the fork is decided on adv_pres) reads as metric-shopping unless substantiated. => Diagnose the disagreement directly: show at the matched behavioral-forget point that LLM-judged forget for KG and dense are equal on held-out probes (or quantify the residual judge-measured forget gap and argue it is below a materiality threshold); if it cannot be cleanly isolated, REPORT BOTH metrics and SOFTEN 'demonstrated' for the Amazon edit arm.

              THE ITERATION-10 MANDATE (the AVERTED-COST capability and the GENUINE-TRANSFER/break-even fix are the two make-or-break new pieces; the minors are cleanup; if BOTH new pieces fail, the paper stands as a localization + confinement-screen + absorber-catalog BOUNDARY/TOOL paper, itself publishable).
                (M1''''' = NEW LOAD-BEARING #1 -- AVERTED-COST CAPABILITY, R2, the new dominant-blocker fix). Build a concrete, end-to-end AUDITING SCENARIO: pick an absorbed sub-context (e.g. Georgia / a named-entity homograph Amazon-Bush-Cook / a first-letter absorbed word). Stand up a downstream artifact a practitioner WOULD actually use -- a parent-latent (or SCR/TPP marginal-attribution top-N SAE) classifier or steering handle for the concept -- and SHOW (a) because of absorption the parent has a recall hole on the absorbed sub-context, the artifact SILENTLY FAILS there (measured: classifier accuracy / steering-success drop on the absorbed slice); (b) STANDARD PRACTICE (raw parent latent / marginal-attribution selection / a contested SAEBench-style proxy) does NOT flag the silent failure; (c) the SHIPPED LABEL-FREE SCREEN DOES flag the recall hole and NAMES the absorber; (d) adding the named absorber REPAIRS the downstream failure with a bootstrap-CI measured benefit vs the practitioner's unrepaired baseline. PAIR with a PUBLISHED label-free absorber CATALOG mined over a public SAE suite (Gemma Scope widths/layers; optionally Neuronpedia): a reusable (concept, sub-context, parent latent, absorber latent, oracle-corroboration) table = the feature-level knowledge graph as a concrete deliverable, squarely in the goal's knowledge-graph/knowledge-extraction/applied-knowledge-discovery scope. This converts 'absorption is confined' from a boundary statement into an actionable reliability tool with measurable averted cost and a clear 'why build on it'.
                (M2''''' = NEW LOAD-BEARING #2 -- GENUINE NET-SAVING or DROP, R1). EITHER (1) TRANSFER: discover the absorber id ONCE (build phase, any labels), then APPLY THE FIXED id with ZERO new labels to a DIFFERENT deployment of the SAME sub-context -- a held-out distribution / corpus split / carrier-template shift / (if a paired SAE exists) a model variant -- and show the firing gate STILL beats an n-label dense gate fit fresh on the new deployment (realizing the amortization iter-9 never exercised). OR (2) NET-OUT + BREAK-EVEN: account for the discovery-time label cost and reframe as 'amortizable over K>=K* redeployments of the same sub-context, break-even at K*', REPORTING K*. In BOTH cases report the n=5 dense point as the honest practical comparison and flag the n=1 collapse as partly a gate-construction artifact. ADD a SELECTION-INDEPENDENT localization metric (behavioral next-token KL targeting) and lean on held-out generalization. FORK: genuine zero-label cross-deployment transfer beating n-label dense (or a small reported K*) => REAL demonstrated where-to-gate value; neither => DROP the where-to-gate thesis and stand fully on M1''''' + localization.
                (M3''''' = RE-CONTROL THE SPINE, R3+R4). Reframe to 'beats S-mag and S-rec (the two informative label-free selectors) at FDR<=0.05 on 16/24 holes'; report parent-argmax controls only as vacuous-by-construction confirmations; keep non-triviality (6/7 numeric, precision_specific=False) and the downstream-capability NULL_TEMPER; add the selection-independent behavioral-KL localization metric.
                (M4''''' = SUBSTANTIATE THE AMAZON CAVEAT, R6). Diagnose the adv_joint-vs-adv_pres instrument disagreement directly; else report both metrics and soften 'demonstrated' for the Amazon edit arm.
                (M5''''' = PRESENTATION, R5). Corrected results AS results in the body; rebuttal scaffolding to the appendix changelog; open each section with its result.
                (M6''''' = CARRIED INTEGRITY). Carry the settled spine [24 distinct holes (source-authoritative, supersedes 22) / 30 FDR survivors; 16k selectivity mean 1452x median 1262x; 65k median ~676x (NEVER 466997x, NEVER the floor-recipe-dependent mean); cross-dict 65k FULL / layer-9 PARTIAL] [art_sxwT7hK6YFEA, art_A8o1h4sWckjw, art_4L1MZxvWYlGd]; the settled safety null (2/44 homograph; named-entity 3/5) [art_yAQgbq5Wgymx, art_ZxVw0e4seBq3, art_NIxb2uUvT-ze]; router DEMOTED [art_F_-HUhl0NR_i]; clustering INERT (0/8) and all three goal-named downstream tasks NULL; numeric below editing gate; member-labeling 0.730 vs 0.096. Strip iteration/rebuttal scaffolding.

              RE-DESIGNATED HEADLINE (localization + the averted-cost screen/catalog FIRST; the where-to-gate edit advantage is REAL only vs an UNCONDITIONAL dense projection, NOT vs a fair conditional control, and its label-free NET SAVING is contingent on iter-10 transfer). On a FROZEN public SAE, anchored recall-hole-guided PRECISION SELECTION is a TRAINING-FREE, LABEL-FREE DISCOVERY PROCEDURE that surfaces the single PRECISE sub-context latent a marginal-attribution ranking silently drops -- in the absorption regime this IS the absorber -- plus a feature-level KNOWLEDGE GRAPH whose edges carry MEASURED, localized recall recovery (a KG-named absorber added to a suppressed parent recovers its recall hole over the two INFORMATIVE label-free selectors S-mag/S-rec; 16/24 holes survive FDR; the win is COVERAGE not precision-magic; replicates on a 4x-wider SAE with MORE absorption). The value is auditable per-sub-context LOCALIZATION, NOT classification or downstream recall (a dense probe out-recalls the repaired unit on 4/5 concepts; no SAE unit out-classifies a dense probe on any task). The CLUSTERING hypothesis was tested and did NOT pay off: multi-member grouping is INERT vs a max-precision selector (0/8 edit cases), adds collateral, and ties weak baselines. Gating is ESTABLISHED PRIOR ART (CAST/GSS/GUARD-IT/SADI, all SUPERVISED), so the only SAE-specific value left is whether the LABEL-FREE DISCOVERY of WHERE to gate SAVES the labeling cost over repeated redeployments -- the iter-9 'demonstration' was CIRCULAR (full-label-discovered handle vs n-label dense), so iter-10 must prove GENUINE cross-deployment transfer / a small break-even K* or DROP the thesis. SAFETY-relevant absorption is HOMOGRAPH-CONFINED (2/44, both homographs; 6/110 eligible polysemous tokens overall; religion/ethnicity/months never structured) -- the SETTLED ceiling and deliberate boundary. The DURABLE, BUILD-ON VALUE iteration 10 must establish: an AVERTED-COST reliability TOOL (the screen catches a silent absorption-induced downstream failure standard practice misses, and the named absorber repairs it) + a published label-free absorber CATALOG over a public SAE suite.

              PRIMARY ENDPOINT (re-designated; the averted-cost capability and the genuine-transfer/break-even are the NEW load-bearing positives).
                (a) AVERTED-COST CAPABILITY + ABSORBER CATALOG (NEW LOAD-BEARING #1, M1'''''): a worked auditing scenario where absorption silently breaks a downstream artifact, standard practice misses it, the shipped screen catches it, and the named absorber repairs it with a measured benefit; + a published label-free absorber catalog over a public SAE suite. THE answer to 'why build on it'.
                (b) GENUINE WHERE-TO-GATE NET-SAVING (NEW LOAD-BEARING #2, M2'''''): cross-deployment zero-label transfer of a FIXED absorber id beating an n-label dense gate, OR a netted break-even K* with a small K*, + a selection-independent localization metric. FORK: real saving vs DROP the thesis.
                (c) AUDITABILITY/LOCALIZATION SPINE (ACHIEVED, re-controlled): KG-named absorber beats S-mag/S-rec on 16/24 holes at FDR (parent-argmax controls = vacuous-by-construction confirmations); coverage not precision-magic; downstream-capability NULL -> tempered to localization-not-utility; selectivity presented strictly as localization (denominator is the disowned whole-parent strawman; fair gate is cleaner); member-labeling 0.730 vs 0.096; cross-dictionary 65k full / layer-9 partial [art_mHCB4FyqyMXL, art_sxwT7hK6YFEA, art_A8o1h4sWckjw, art_4L1MZxvWYlGd].
                (d) CONFINEMENT COVERAGE + SCREEN (ACHIEVED): 6/110 = 5.5% strict (Wilson [0.025,0.114]); homograph/named-entity-confined; demographic never; shipped screen.py; oracle corroborates 27/31 [art_NIxb2uUvT-ze]. To be ELEVATED from reassurance to capability via (a).
                (e) SAFETY SCOPE (SETTLED NULL): homograph-confined (2/44; named-entity 3/5) [art_yAQgbq5Wgymx, art_ZxVw0e4seBq3].
                (f) ROUTER: recall-hole-alone reproduces on derivation (bal-acc 1.0) but is OUT-OF-SAMPLE-UNVALIDATED (prospective Wilson includes 0.5) -- DEMOTED to exploratory diagnostic [art_F_-HUhl0NR_i].
              SUPPORTING (strengthen, do not gate): within-SAE precision selection where the signature holds (Georgia, I, D); the steering demo (L,D); the homograph/coverage breadth count. The headline NO LONGER depends on classification beating dense, on multi-member grouping, on the router being validated, on a safety win, on the edit beating a fair conditional dense control, OR on the iter-9 label-scarce 'saving' as stated.

              THE DISCOVERY ALGORITHM (framed as LABEL-FREE SINGLE-SPECIALIST LOCALIZATION; clustering DEMOTED to a tested-and-negative secondary). STEP 1 cover-based eligibility (content-responsive above a shuffle null; firing-precision>=0.7; covers>=1 sub-context). STEP 2 ANCHOR = argmax cover-set chosen WITHOUT the diagnostic, with the UNSUPERVISED FIRING-FLOOR PARENT-VALIDATION (anchor must fire on held-out corpus above ~5%). STEP 3 HOLE = parent's uncovered pairs (names the under-served sub-context, label-free). STEP 4 PRECISION-SELECT the single absorber covering the hole (held-out per-sub-context precision>=0.7, firing-Jaccard<0.1, marginal-gain>=0.05 CI excl 0; Georgia selects 16009 prec .955 not 4697 prec .335). NOTE the localization-arm metric (balanced-accuracy) is CLOSE to this selection criterion -- report the coincidence and add a selection-INDEPENDENT behavioral-KL metric. Set-cover/(1-1/e) is MOTIVATION only (effectively k=1 for every win; INERT vs max-precision for the edit). C-TRACK correlation-community splitting + multi-member units: TESTED AND NEGATIVE -> reported as the clustering-hypothesis null, NOT a contribution.

              BASELINE GLOSSARY. LOCALIZATION/REPAIR controls (decisive): S-mag (argmax mean content-response magnitude) and S-rec (argmax content-flip recall) = the TWO INFORMATIVE label-free selectors the KG must beat; dense-probe decoder-projection argmax (JTT-reweighted + diff-of-means) = VACUOUS-BY-CONSTRUCTION (resolve to the parent, which cannot recover its own hole) -- reported as confirmations only. EDIT comparators: KG-ABL (discovered absorber, sparse-firing-gated, ZERO sub-context labels at deploy); DENSE-SUB-ABL (strongest UNGATED dense, the LEAD reference, NOT the fair control); DENSE-SUB-ABL-GATED-FAIR (precise logistic d_sub gate, bounded beta<=1 -- the load-bearing fair control that CLOSED the gap and is studied vs label budget); DENSE-SUB-ABL-GATED footprint-gated (iter-7, DEMOTED, beta~3 over-erasure, robustness caveat only); MAX-PRECISION single latent (ablation: discovery is INERT for the edit win); DENSE-WHOLE-ABL (whole-parent over-shoot reference = the disowned selectivity-denominator strawman). For M1''''' averted-cost: the practitioner's parent-latent / SCR-TPP marginal-attribution selection / contested SAEBench-style proxy are the 'standard practice' the screen must beat at catching the silent failure. Classification baselines (a)-(k) carried as supporting/within-SAE.

              NON-SPELLING / HOMOGRAPH TESTBED. Absorption recurs on HOMOGRAPH/POLYSEMOUS tokens whose general parent is suppressed -- taxonomic Georgia/Jordan; United States CO-FIRING; 0/28 professions; of 64 homograph entities only 3 months (and months NO_HOLE in the iter-9 screen); of 5 named-entity homographs 3 structured (Amazon/Bush/Cook); of 44 safety groups only 2 homographs (white, straight). A structured absorber is an EDITABLE handle only if its targeted sense is LEXICALLY CONCENTRATED (spelling 'large', entity 'Amazon' forget; DISTRIBUTED country senses Georgia/Jordan and even structured Bush/Cook do NOT). A non-SAE dense probe matches/beats the unit on ALL classification.

              SCOPE AND VALUE PROPOSITION. The defensible contribution is: (1) a TRAINING-FREE, LABEL-FREE single-specialist LOCALIZATION procedure surfacing the precise absorber marginal attribution drops, with a MEASURED auditable feature-KG (recall recovery over S-mag/S-rec, coverage not precision-magic; localization-not-utility), REPLICATING across SAE dictionaries; (2) a LEXICAL-POLYSEMY CONFINEMENT finding + a label-free SCREEN; (3, NEW, the build-on capability) an AVERTED-COST reliability tool + a published absorber catalog turning the screen into a measurable benefit; (4, contingent) a label-free WHERE-TO-GATE discovery whose net saving iteration 10 must demonstrate via genuine cross-deployment transfer / break-even K* or DROP. The method does NOT out-classify a strong dense probe, does NOT beat a fair conditional dense control on the edit, the clustering machinery is INERT, and the iter-9 label-scarce 'saving' was circular.

              HONEST NEGATIVES (each publishable): the genuinely-fair bounded-beta d_sub-gated dense control CLOSES the edit gap on every case (0/8 KG-beats-both) and is cleaner on collateral (NO SAE-specific edit advantage); the iter-9 label-scarce where-to-gate 'demonstration' is CIRCULAR (full-label-discovered fixed absorber id vs from-scratch n-label dense; net saving unproven; n=5 dense already within 0.03 balacc; n=1 collapse partly a gate-construction artifact; amortization-across-same-sub-context-reuse never exercised); the localization-arm balanced-accuracy partly RESTATES the selection criterion; 2 of the 4 repair controls are VACUOUS-BY-CONSTRUCTION; the downstream-capability test is a NULL (dense probe out-recalls the repaired unit on 4/5); the concentrated positive base does NOT broaden (0 independent wins); the set-cover discovery is INERT vs max-precision (0/8); the clustering/multi-member hypothesis did NOT pay off; the edit-win predictor is CONCENTRATION not absorption (insult co-fires yet forgets; Georgia/Jordan absorb yet lose); iter-6's Georgia +0.561 RETRACTED as near-NOOP; the +1.58-vs-gated headline was inflated; the meaningful-forget proof was thin (n=4 probes, instruments disagree); the Amazon adv_joint does not converge at full labels (instrument-disagreement; risk of metric-shopping if unsubstantiated); gating is established prior art; no SAE unit out-classifies a dense probe; all three goal-named downstream tasks (classification, steering, model-diffing) are NULLS; safety absorption is homograph-confined (2/44; 6/110); 0/28 professions; the router is at chance out-of-sample; cross-dictionary replicates at 4x width but only PARTIALLY across a layer; the 65k 466997x selectivity was a divide-by-epsilon artifact and the corrected mean is floor-recipe-dependent (use median ~676x); numeric is below-gate. A clean iter-10 result where neither genuine transfer nor a small break-even K* holds = 'there is no realized SAE-specific where-to-gate saving' and the paper becomes a localization + confinement-screen + absorber-catalog boundary/tool paper -- itself publishable IF the averted-cost capability lands.

              MOTIVATION (substance unchanged). Single SAE latents are unreliable units: absorption (Chanin 2409.14507), splitting, hedging (2505.11756), 'SAEs Do Not Find Canonical Units' (ICLR 2025) converge on no single latent reliably tracking a concept; AxBench (ICML 2025) and DeepMind's negative report show diff-of-means beats raw-latent SAE methods, and Farrell (2410.19278) shows multi-feature SAE unlearning has side-effects >= RMU -- so any SAE method must clear strong dense baselines AND, for the edit, BOTH the strongest ungated dense AND a fair CONDITIONAL gated dense direction (which it does NOT). Absorption is the regime where OBSERVATIONAL signals break by construction and MARGINAL-ATTRIBUTION selection silently drops the absorber; anchored recall-hole-guided precision selection recovers it LABEL-FREE -- the durable localization deliverable. The contested reliability of the field's own SAE proxies (Chanin 'Are SAE Benchmarks Reliable?') is exactly why a TASK-GROUNDED, label-free, oracle-validated screen + catalog is a transferable reliability instrument. The method positions against 'use SAEs to DISCOVER, not to ACT' (Peng 2506.23845): CCRG discovers the sub-context handle and the silent-failure it causes; ACTING through it is no better than a fair labeled dense gate; whether DISCOVERING it label-free SAVES cost over redeployments, and whether the discovery AVERTS a downstream failure standard practice misses, are the load-bearing open questions iteration 10 must answer.

              SUCCESS CRITERIA. CONTRIBUTION CONFIRMED iff: (LOAD-BEARING) (M1''''') the averted-cost scenario shows absorption silently breaks a downstream artifact, the screen catches it where standard practice does not, and the named absorber repairs it with a CI-measured benefit, + a published label-free absorber catalog over a public SAE suite; AND (M2''''') EITHER genuine zero-label cross-deployment transfer of a FIXED absorber id beats an n-label dense gate OR a netted break-even K* is reported with a small K*, under a selection-independent localization metric; AND the re-controlled localization spine holds (KG beats S-mag/S-rec on 16/24 at FDR, coverage-not-precision, downstream-null-tempered, cross-dict 65k full / layer-9 partial); AND the coverage/screen + safety null + clustering-inert null are reported as deliberate findings. SUPPORTING (strengthen, do not gate): within-SAE precision selection (Georgia, I, D); member-labeling above null; the steering demo (L,D); the coverage breadth count. HONEST NEGATIVES are reportable and cap-but-do-not-sink: neither transfer nor a small K* holds (=> where-to-gate dropped; paper is localization + screen + catalog), the edit not beating a fair conditional control, near-NOOP forget for distributed senses, safety absorption absent, router-at-chance, layer-conditional replication, clustering inert, no classification win over dense.
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
  Reviewer exposed the iter-9 where-to-gate 'win' as circular (full-label-discovered handle); same frame, refined mandate.
_confidence_delta: decreased
_key_changes:
- >-
  Recorded the iter-9 label-scarce execution [art_-zywGLxOcKOw] AND the reviewer's MAJOR exposure that it is CIRCULAR: the
  label-free SAE handle reused absorber IDs hard-coded from prior full-label+oracle discovery vs an n-label-restricted dense
  gate, so the 'saves 10-40 labels' net saving is UNPROVEN; downgraded the where-to-gate positive from 'demonstrated' to 'curves
  real, net-saving unproven'.
- >-
  Reframed the iter-10 #2 evidence mandate (M2''''') to a GENUINE-TRANSFER-or-BREAK-EVEN test: discover the absorber id once,
  apply the FIXED id with zero new labels to a different deployment of the SAME sub-context beating an n-label dense gate,
  OR net out discovery cost and report break-even K*; plus report the n=5 dense point and note the n=1 collapse is partly
  a gate-construction artifact.
- >-
  Elevated SIGNIFICANCE (reviewer MAJOR R2) to the new dominant blocker: added NEW LOAD-BEARING M1''''' = AVERTED-COST CAPABILITY
  (a scenario where absorption silently breaks a downstream artifact, the screen catches it where standard practice does not,
  the named absorber repairs it with measured benefit) + a published label-free absorber CATALOG over a public SAE suite --
  turning the screen from reassurance into a build-on capability.
- >-
  Recorded the strengthened repair spine [art_mHCB4FyqyMXL] and reviewer minor: reframe to 'beats the TWO informative label-free
  selectors S-mag/S-rec on 16/24 holes at FDR'; the two parent-argmax controls are VACUOUS-BY-CONSTRUCTION (parent cannot
  recover its own hole); precision_specific=False (coverage not precision); downstream-capability NULL -> tempered to localization-not-utility.
- >-
  Added the localization-arm circularity minor (R4): balanced-accuracy is close to the firing-precision selection criterion;
  mandate a SELECTION-INDEPENDENT localization metric (behavioral next-token KL targeting) and leaning on held-out generalization.
- >-
  Recorded the integrity-lock eval [art_A8o1h4sWckjw]: selectivity presented strictly as localization (denominator is the
  disowned whole-parent strawman; fair gate is cleaner); distinct holes = 24 (supersedes carried 22); 65k corrected MEDIAN
  ~676x reproduces while the MEAN is floor-recipe-dependent (use median, never 466997x).
- >-
  Recorded the coverage screen [art_NIxb2uUvT-ze]: 6/110 = 5.5% strict, homograph/named-entity-confined, demographic/months
  never structured, shipped screen.py; flagged by the reviewer as a reassurance instrument to be elevated via M1'''''.
- >-
  Added the Amazon caveat substantiation mandate (R6): directly diagnose the adv_joint-vs-adv_pres instrument disagreement
  at matched behavioral forget, else report both metrics and soften 'demonstrated' for the Amazon edit arm.
- >-
  Added the presentation mandate (R5): move all 'prior version / a reviewer noted' references from the body to the appendix
  changelog; open each section with its result.
- >-
  Confidence DECREASED: the single new SAE-specific positive iter-9 was tasked to deliver (label-scarce where-to-gate) failed
  verification as circular, and the significance MAJOR remains the dominant unresolved blocker, partially offset by verified
  spine/screen rigor gains.
relation_type: evolution
</hypothesis>

<artifact_direction>
Make this direction concrete and actionable. Keep the same type and respect dependencies.

id: experiment_iter10_dir2
type: experiment
objective: >-
  M1''''' NEW LOAD-BEARING #1, part 2 (significance, R2): mine and PUBLISH a label-free-derivable ABSORBER CATALOG over a
  PUBLIC SAE SUITE, turning the screen from a one-off into a reusable resource (the feature-level knowledge graph as a concrete
  deliverable, in the goal's knowledge-graph/knowledge-extraction scope). Run the shipped label-free firing-signature screen
  across multiple frozen Gemma Scope configurations of gemma-2-2b — {width 16k, width 65k} x {layer 9, layer 12} (add further
  cheaply-runnable layers/widths if budget allows) — over the full candidate vocabulary (first-letter spelling word-types;
  taxonomic countries; homograph entities city/month/given-name/brand; safety-identity nationality/religion/ethnicity/named-entity).
  For EVERY candidate emit a catalog row: (concept hierarchy, sub-context token, parent latent id, absorber latent id, firing-precision,
  recall-hole, firing-Jaccard, hole-coverage-gain CI, predict_absorption enum, form-free oracle corroboration, layer, width,
  optional Neuronpedia auto-interp label). Reproduce the known positives per config (Georgia 16009 @16k-L12 and 46143 @65k;
  Amazon/Bush/Cook 6846/9751/15631; first-letter absorbers) as a correctness check. Report per-config coverage with Wilson
  CIs and a CROSS-CONFIG STABILITY column (which absorbers reappear across width/layer vs which are dictionary-specific —
  directly consistent with 'absorption worsens at wider width' and the iter-9 layer-conditional finding). VERDICT = CATALOG_PUBLISHED:
  a reusable (concept, sub-context, parent, absorber, oracle, config) table + per-config coverage map = the build-on resource
  that pairs with the averted-cost screen and answers 'why build on it'.
approach: >-
  Reuse the iter-9 shipped screen (screen.py from art_NIxb2uUvT-ze) and the cross-dictionary engine (art_4L1MZxvWYlGd at iter_5/gen_art/gen_art_experiment_2,
  which already loads 16k/65k/layer-9 params.npz, encodes the candidate corpora, and re-derives anchors+absorbers per dictionary
  with the K-track greedy + form-free oracle) by reading their run-tree workspaces DIRECTLY via the filesystem (experiments
  cannot be formal deps of an experiment). Consult the implementation dossier (art_RidEJtBC7gPT) and diagnostic dossier (art_I2MrezW41iQo)
  for SAE pins / the form-free oracle. Parametrize a single pipeline over the SAE config list; for each config load Gemma
  Scope from params.npz, encode the candidate corpora (cache under cache/, exclude from upload), run the firing-signature
  screen + form-free oracle, assemble catalog rows, and reproduce the per-config positive controls. Cross-config stability
  = join catalog rows across configs by (hierarchy, sub-context) and count how many absorbers persist vs are config-specific.
  Optionally enrich parent/absorber with Neuronpedia auto-interp labels via the public API (free/cheap; if unavailable, skip
  and flag); $0 LLM otherwise. Gradual scaling (16k-L12 first, then add 65k and layer-9). Output method_out.json (exp_gen_sol_out
  schema): metadata carries the catalog_summary (n_configs, n_candidates, n_structured per config, cross_config_stability
  counts, per-config Wilson coverage CIs), positive_control_reproduction per config, and the shipped catalog spec; datasets
  = absorber_catalog rows (one per candidate x config: predict_absorption + all signature fields + parent/absorber ids + oracle
  + layer/width) + catalog_coverage rows (per config x hierarchy coverage). Ship catalog.csv + catalog.json + README.md as
  the published resource (documented label-free derivation, enum semantics, per-config provenance). Validate full/mini/preview
  <100MB.
depends_on:
- id: art_t2uUbjSwpd3t
  label: taxonomic-data
  relation_type:
  relation_rationale:
- id: art_KNPsfjByyxiS
  label: entity-data
  relation_type:
  relation_rationale:
- id: art_2xQn686KUmV5
  label: homograph-data
  relation_type:
  relation_rationale:
- id: art_dpYpjSn2Xvg3
  label: spelling-data
  relation_type:
  relation_rationale:
- id: art_RidEJtBC7gPT
  label: method-dossier
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

--- Dependency 6 ---
id: art_KNPsfjByyxiS
type: dataset
title: >-
  Safety Identity SAE Absorption Testbed: nationality/religion/ethnicity/named-entity
summary: >-
  Four-hierarchy SAFETY-RELEVANT identity feature-absorption testbed, a strict structural drop-in of the iter-1 taxonomic
  testbed (gen_art_dataset_2) and the iter-5 homograph testbed, so the downstream K-track set-cover + form-free Chanin absorption
  diagnostic + recall-hole router pipeline runs UNCHANGED. exp_sel_data_out format: top-level {metadata, datasets:[{dataset,
  examples}]}; output is the PARENT binary label (positive=parent identity concept present at the target token, negative=absent);
  all per-row metadata flattened to metadata_<key>. FOUR datasets (36,448 examples): nationality_absorption (14,028), religion_absorption
  (6,055), ethnicity_identity_absorption (7,777), named_entity_safety (8,588). Each hierarchy has the same THREE coordinated
  components as dataset_2: (A) content-flip minimal pairs (x_on/x_off), (B) surface-flip pairs (surface_a/surface_b) for the
  surface-invariance admission, (C) a FROZEN diagnostic corpus of REAL Pile-uncopyrighted windows (pinned rev 3be90335...)
  labelled PURELY by surface form/gazetteer + per-token high-precision INCLUDE/EXCLUDE disambiguators, with a matched hard-negative
  family (other_group, non_identity, homograph_distractor=same token in its competing non-identity sense, easy). Labels are
  MODEL-INDEPENDENT and NON-CIRCULAR, so the corpus equally supports the honest 'no safety attribute is absorption-structured'
  null and a positive finding (degenerate-construction guard preserved). 56 sub-contexts reach >=150 diagnostic-fold positives
  = 'eligible' in the absorption_readiness manifest (far exceeding the >=4 target), including homograph-sense identity tokens
  Black/White/Asian/Native/Polish/Turkish/Indian/Apple/Amazon/Bush/Cook/King most likely to be absorption-structured. Target
  tokens anchored in the real google/gemma-2-2b vocab with precomputed metadata_target_token_indices via offset_mapping (add_special_tokens=False;
  token_indices_present=True; multi_token flagged). Sources: 35,430 pile_uncopyrighted + 922 templated + 96 llm_generated.
  LLM augment (openai/gpt-4o-mini) + independent judge (anthropic/claude-haiku-4.5, sense_correct rubric): pair pass 0.55;
  corpus sense precision nationality 0.935 / religion 1.0 / ethnicity 0.909 / named_entity 0.672; total spend $0.13 (under
  $3 target, $10 cap). Frozen folds (seed 20240617): pairs 70/30 by pair_id stratified by sub_context, corpus 50/50 by doc
  — the diagnostic fold is where iter-6 runs the form-free parent-hole search. Cross-hierarchy collisions documented (Jewish=ethnicity
  canonical, Indian/Arab notes). Validates PASSED against exp_sel_data_out; full=61MB, mini/preview ~20KB, all <100MB. Stamped
  NEXT-ITERATION (M2') building block — NOT consumed by this iteration's parallel experiments. Deliverables: data.py, build_dataset.py,
  pipeline.py, schema.json, manifest.json (counts/folds/sources/pass-rates/cost/absorption_readiness), pyproject.toml, full/mini/preview_data_out.json.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_dataset_1
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
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/user_uploads`. Check this folder for anything relevant to your task.
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

### [2] HUMAN-USER prompt · 2026-06-19 00:39:57 UTC

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
