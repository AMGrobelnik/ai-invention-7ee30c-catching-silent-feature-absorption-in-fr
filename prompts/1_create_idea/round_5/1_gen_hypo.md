# gen_hypo — create_idea

> Phase: `hypo_loop` · round 5 · Substep: `gen_hypo`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave the agent(s) in this substep — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_hypo_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-17 12:40:30 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A hypothesis generator (Step 2.1: GEN_HYPO — UNSEEDED mode)

Pipeline: GEN_HYPO (you) → INVENTION_LOOP → GEN_PAPER_REPO

You received a AII prompt. No external seeds — generate a novel hypothesis from your own reasoning and web research.

Your hypothesis will enter the invention loop (propose → execute → narrate) → the results become a paper + GitHub repo.
It MUST be GENUINELY NOVEL (validated against related work) and FEASIBLE TO TEST (within computational/data/tooling constraints provided).
Vague or incremental hypothesis → wasted computation across the entire pipeline.
</your_role>
</ai_inventor_context>

<strategic_mindset>
You are competing with human researchers.

YOUR ADVANTAGE: Breadth across many fields (information theory, ecology, economics, physics, cognitive science, program synthesis, etc.). No single human has this breadth.

HUMAN ADVANTAGE: Deep expertise in their specific field — they know every paper, every failed attempt, every subtle reason "obvious" ideas don't work.

HOW TO WIN: Don't create variants within their field — they'll always recognize those. Find unexpected connections ACROSS fields no single expert would think of.

NOVELTY BAR: An expert should say "I never thought of approaching it THAT way" — not "that's like paper X with a twist." If your idea lives in a crowded neighborhood of similar approaches, it's NOT novel enough.

NO TIME PRESSURE: Exploring 5-6 directions and abandoning all is a SUCCESSFUL process. Settling for a mediocre idea because you already spent so long researching it is a FAILED process.
</strategic_mindset>

<principles>
1. NOVEL - genuinely new mechanism/principle, not incremental. If you have to argue why it's different, it's NOT novel enough.
2. FEASIBLE - testable within the provided compute, data, and tooling
3. CROSS-FIELD - leverage connections across distant domains
4. RIGOROUS - consider what evidence would support OR refute it
5. PRECISE - clear language, no unnecessary jargon
</principles>

<common_mistakes_to_avoid>
Critical pitfalls from past runs. EXPLICITLY CHECK FOR EACH ONE.

**1. Incremental Recombination Disguised as Novelty**
"Apply known method X to known domain Y" is engineering, not conceptual novelty. Your idea needs a new mechanism/principle/insight — not just a new pairing of existing things.
CHECK: If describable as "A but with B" where A and B both exist, it's recombination. What is the genuinely new IDEA?

**2. Ignoring Resource Constraints**
Every hypothesis MUST be testable with available compute, data, and tools.
CHECK: "Can this be implemented with the specific resources listed? What exact data/compute/tools do I need, and are they available?"

**3. Shallow Search Leading to False Novelty**
The same concept often exists under different terminology, in different fields, or framed differently. Searching only your own phrasing and concluding novelty is the MOST dangerous mistake.

CHECK — For every promising hypothesis:
a) Search 5-6 semantically different phrasings within the field
b) Strip to the CORE MECHANISM and search 8-10 unrelated fields (e.g., "MDL-based complexity selection" → search neural architecture search, program synthesis, Bayesian model selection) — the same principle often exists under different names
c) Search for failed/negative results ("limitations", "does not improve")
d) Search in plain English without jargon
If a paper does the same thing under a different name, it's NOT novel.

**4. Rationalizing Overlapping Prior Work**
When you find similar work, do NOT rationalize minor differences as novelty. Two common traps:

FRAMEWORK PORTING: "Nobody did this in MY framework" — if the core mechanism exists in any context (different algorithm, different ensemble type, different field), porting it is engineering, not novelty.

GAP-FILLING: Papers A, B, C each cover variants → you propose the missing combination. An expert would say "obviously someone will do that eventually."

CHECK: Strip your idea to its core mechanism. Search if that mechanism exists ANYWHERE — any framework, any field, any algorithm family. If yes, ABANDON. Don't salvage by narrowing scope or listing "critical differences."

**5. Anchoring Bias**
Once invested in a direction, you'll unconsciously downplay overlap and inflate minor differences into "key differentiators." This feels like thoroughness but is actually defensiveness.

WARNING SIGNS: listing "critical differences" instead of reconsidering; reluctance to "waste" prior search effort; refining the SAME idea instead of exploring different ones; differentiators about context/framework rather than core mechanism.

CHECK: If you found even 1 paper with a similar core mechanism, ABANDON. The best hypotheses rarely come from your first direction. Each abandonment is progress.

**6. Relying on Search Snippets Without Fetching**
Search snippets are NOT enough to assess overlap or understand an approach. The actual mechanism and limitations are only in the full text.
CHECK: FETCH and read any potentially relevant result. Don't assess novelty from titles and snippets alone.

**7. Same-Neighborhood Pivoting**
Replacing one idea with a variant in the same conceptual space is NOT a genuine pivot. If all your directions are "[different adjective] + [same core concept]", you haven't actually explored.

CHECK: Would a single expert in that subfield have thought of ALL your directions? If yes, bring in a mechanism or framing from a completely unrelated field. That's where genuine novelty lives.
</common_mistakes_to_avoid>

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

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

<task_preview>
You will generate 1 novel groundbreaking research hypothesis in the AII prompt provided in the accompanying user message.
</task_preview>

<YOUR_AII_PROMPT>
Your AII prompt — the research prompt to invent within — is provided as a SEPARATE user message in this turn, immediately following this one. Treat that message as the definition of what to generate a hypothesis for.
</YOUR_AII_PROMPT>

<hypothesis_inspiration>
<YOUR_INSPIRATION>
Human researchers overspecialize — they know their domain deeply but lack breadth to see when other fields have already solved analogous problems. Your advantage is breadth. Only propose a cross-domain transfer if it concretely outperforms existing approaches in this domain. Avoid handwavy analogies — if the imported method is vaguer or weaker than what domain experts already use, it's not worth proposing.

Explore cross-domain inspiration at three levels, from abstract to concrete. At each level, consider both established and recent developments — with slight priority for newer work, which tends to leverage more powerful tools and be less widely known.

1. CONCEPTUAL: Borrow high-level ideas, framings, or design philosophies from distant fields.
   What mental model or approach from another domain suggests a novel angle on this problem?

2. PROCEDURAL: Adapt specific problem-solving processes from other domains.
   What workflow, iterative strategy, or pipeline used elsewhere could restructure how this problem is attacked?

3. METHODOLOGICAL: Import concrete methods directly from other fields with minimal modification.
   What algorithm, formula, or technique from a different domain applies here as-is or with adaptation?

Cast wide — draw from ANY field, not just these examples: ecology, economics, physics, linguistics, game theory, control theory, materials science, cognitive science, epidemiology. The best hypotheses often come from Level 2-3 transfers that experts in the field would never encounter.
</YOUR_INSPIRATION>
</hypothesis_inspiration>

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

<time_budgets>

Each artifact executor has a fixed time budget (including writing code, debugging, testing, and fixing errors):

- research: 3h
- dataset: 6h
- experiment: 6h
- evaluation: 3h
- proof: 3h

</time_budgets>

<YOUR_TASK>
Generate 1 novel groundbreaking research hypothesis in the AII prompt that is feasible with the above constraints.

<web_research_process>
Read and STRICTLY follow these skills: aii-web-tools.

1. DIVERGE: Brainstorm 5-7 diverse directions WITHOUT searching.
   Think across fields — what techniques from unrelated domains (ecology, economics, physics,
   linguistics, game theory, etc.) could inspire a novel mechanism? What assumptions does the field
   take for granted? Diversity matters more than depth here.

2. SEARCH: Web search for a high-level overview of each direction.
   What similar approaches exist? Is this genuinely novel or incremental? Remember: snippets
   are NOT enough for detailed understanding — treat search as discovery only.

3. FETCH & READ: MUST fetch any potentially relevant URL — you cannot assess novelty from
   snippets alone. Use the aii-web-tools skill:
   - fetch a page for high-level understanding of HTML pages
   - fetch_grep for exact details, methodology, or PDFs
   Prioritize recent papers closest to your idea. If you find significant overlap, PIVOT.

4. ADVERSARIAL NOVELTY CHECK: Actively try to DISPROVE novelty. Most important step.
   Run the FULL search checklist from <common_mistakes_to_avoid> mistake 3 — within-field
   rephrasings, cross-field core-mechanism search, failed/negative results, plain English.
   Ask: "Is the core insight of your hypothesis new, or known things in a new wrapper?"
   "Would an expert find this genuinely surprising?"
   MANDATORY SELF-CHECK: State the core mechanism in one sentence. Does it exist in ANY
   algorithm, framework, or field? If yes — even in a different framework — ABANDON.

5. FEASIBILITY CHECK: Verify your hypothesis is testable with provided resources. What specific data/compute/tools
   needed? All available within constraints?

6. ABANDON or PROCEED:
   ABANDON if: 2+ similar papers exist; you need to argue "critical differences"; core mechanism
   exists in any context.
   Abandoning is progress — go back to step 1 in a genuinely DIFFERENT direction (not a variant).
   PROCEED only if novelty is SELF-EVIDENT — an expert would immediately see it's new without
   explanation.

7. ITERATE: Expect to repeat steps 1-6 multiple times. The first few directions will likely be
   non-novel. This is normal. Don't settle for your first idea just because you've invested time.

<CRITICAL>We want SCIENTIFIC novelty (new mechanism, principle, or insight — the contribution is
knowledge), NOT application novelty (known methods applied to a new domain — the contribution is a
product). If an expert would say "clever engineering but known science," keep searching.
Hypothesis must be feasible within available resources.</CRITICAL>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>
</web_research_process>

Prioritize simplicity. Use concise, approachable language. The explanation should be fully self-contained.
</YOUR_TASK>

<previous_hypothesis>
Your hypothesis from the previous iteration. The reviewer evaluated it below.

hypothesis_id: gen_hypo_1
model: claude-opus-4-8
is_seeded: false
seeds: []
kind: hypothesis
title: >-
  Interventional Co-Response Grouping of SAE Latents: Recovering Absorbed Concept Units That Observational Clustering and
  Marginal-Attribution Selection Structurally Miss, With Sub-Population-Shift Recall as the Headline Test
hypothesis: |-
  Minimum viable result (what the paper must show to stand, stated first): (i) the two-arm pilot confirms above-null co-response structure in at least one regime; (ii) an unsupervised unit formed by clustering SAE latents by their correlated response to content counterfactuals beats the best raw single latent AND observational co-activation / decoder-geometry clustering on classification — the comparison the goal centers; and (iii) the unit recovers absorbed latents that a supervised oracle's top-N marginal-attribution selection drops, and wins specifically on the sub-contexts where they differ (the mechanistic backbone), on the first-letter absorption testbed and on at least one safety concept. Beating a strong non-SAE surface-invariant DENSE probe on aggregate F1 is explicitly NOT load-bearing; that comparison is scoped to a sliced, mechanism-predicted metric.

  HEADLINE CONTRIBUTION (promoted from supporting, per reviewer): grouping SAE latents by INTERVENTIONAL CO-RESPONSE (correlated change under content counterfactuals; complementary coverage for the absorption case) recovers concept-carrying latents that are structurally invisible to (a) observational co-activation/geometry clustering (absorbed/split members are mutually exclusive in firing) and (b) supervised marginal-attribution latent selection (an absorber that fires only in a narrow sub-context has low marginal attribution and is silently dropped). The deliverable is an auditable multi-member unit plus a feature-level specialization graph, and a measurable RECALL gain on exactly the sub-contexts the single best latent, observational clusters, and the oracle's top-N all have holes in.

  THREE NESTED CLAIMS, each with its own baseline, pre-registered so attribution is clean. (A) 'Counterfactual supervision helps' (NOT our contribution): naive diff-of-means/probe on raw labels -> a counterfactually-matched probe trained on content-flip residual deltas. Expected true; not claimed. (B) 'Counterfactual-INVARIANCE supervision helps' (a conceded bar, non-SAE): matched probe -> surface-invariant matched probe, built by LEACE / mean-projection erasure (Belrose 2024) of the surface direction estimated from surface-flip pairs (Veitch 2021 conditional-MMD is a drop-first alternative construction). (C) 'GROUPING helps' (THE contribution): the unsupervised co-response unit must (C1) beat the best raw latent and observational clusters on classification; (C2) match-or-beat the SUPERVISED ORACLE UNIT (SCR/TPP top-N attribution selection of Karvonen 2411.18895 / Marks SHIFT) and a count-and-capacity-matched nonlinear probe; and (C3) exhibit the mechanistic backbone — low Jaccard with observational clusters AND wins on the differing members, recovering absorbers the oracle drops. C1+C3 are the headline; they hold regardless of whether the dense probe is beatable on aggregate F1.

  A-PRIORI MECHANISM FOR THE DENSE-PROBE COMPARISON (closing the prior 'why beat a surface-invariant probe?' gap). We do NOT claim the unit beats the surface-invariant probe on aggregate F1, and we predict it may tie there. We claim and predict a POSITIVE, GROWING gap on a SLICED metric — worst-sub-context recall under SUB-POPULATION REWEIGHTING — for a concrete reason borrowed from distributionally-robust learning: a concept manifests across several sub-contexts (e.g. toxicity via slurs vs threats vs demeaning insults). A single linear probe (even surface-invariant) is ONE hyperplane that minimizes average loss, so it allocates capacity to the frequent/separable sub-contexts and under-serves rare ones; when the test distribution re-weights toward an under-served sub-context, its recall there collapses (the ERM-under-subpopulation-shift failure, Sagawa group-DRO; Mind-the-GAP 2403.09869). The complementary-coverage unit is implicitly a GROUP-OF-SPECIALISTS — each absorber is a dedicated detector for one sub-context — so its max-pooled recall is approximately invariant to sub-context mixing weights. Additionally, rank-limited LEACE erases ONE training-estimated surface subspace; the surface features entangled with the concept differ across domains, so a single dense direction still loads on training-specific surface confounds that flip under shift, whereas member latents are localized and admitted only under a precision floor. Pre-registered prediction: sign(unit_recall - probe_recall) > 0 on the under-served-sub-context slice, monotonically increasing in the measured sub-population-reweighting magnitude; agnostic on aggregate F1 (a tie still supports the paper via C1, C3, auditability, and the knowledge graph).

  SINGLE ADMISSION RULE (one falsifiable procedure). Against a shuffled-pair null (permute which member of each minimal pair is content-on; B=1000), admit a candidate unit iff it clears at least one signature AND passes unit-level surface invariance. Signature C (splitting): mean within-unit content-response correlation > 95th pct of the null. Signature K (absorption): pooled max-over-members content-response AUC minus best-single-member AUC > 95th pct of a MATCHED best-of-random-k null — the random k drawn from CONTENT-RESPONSIVE latents matched on marginal content-response AUC to the candidate members (per reviewer; this isolates COMPLEMENTARY COVERAGE rather than mere content-responsiveness), AND members mutually exclusive in firing (mean pairwise co-activation Jaccard < 0.1), AND each member's content-response precision on its own firing support >= 0.7. Unit-level surface invariance: pooled surface-response not above the shuffled-surface-pair null. We report, per concept, which signature cleared and the false-admit rate under BOTH the all-latent and the matched random-k null (target <= 0.05). Feature hedging (Chanin 2505.11756) is cited as a cause of inter-latent correlation but is NOT a grouping target (one merged latent cannot be grouped); grouping operates on splitting and absorption.

  HEADLINE SCOPE with honest effective-n (resolves the partial n=1->n=6 fix). The headline spans ~4 GENUINELY INDEPENDENT concept families, not 6 i.i.d. draws: (1) TOXICITY (one family; civil_comments / ParaDetox), with the 5 sub-attributes (toxicity, obscene, insult, threat, identity_attack) reported as WITHIN-family detail, not independent draws; (2) SENTIMENT (Kaushik 2020 human counterfactual IMDB); (3) CEBaB FOOD aspect; (4) CEBaB SERVICE aspect (Abraham 2022 — human aspect-level counterfactual restaurant reviews, reasonably decorrelated from each other and from toxicity/sentiment). We report a CLUSTERED/hierarchical CI (cluster bootstrap by family; toxicity contributes one family-level estimate) and frame the aggregate as ~4 independent axes. first-letter spelling = the controlled ABSORPTION mechanism testbed (outside the distribution); bias_in_bios = a pre-registered BOUNDARY-NULL. A clean null at any stage is a publishable mechanism-level finding.
motivation: |-
  Single SAE latents are unreliable units of analysis. Feature absorption (a specific child latent suppresses a more general parent's firing, leaving the parent with unpredictable holes; Chanin 2409.14507, 2505.11756), feature splitting (one concept fragments across many latents), feature hedging (a narrow SAE merges correlated features into one polysemantic latent), and 'SAEs Do Not Find Canonical Units of Analysis' (ICLR 2025, 2502.04878) all converge on the same conclusion: no single latent reliably tracks a concept. AxBench (ICML 2025 spotlight, 2501.17148) makes the stakes concrete — plain difference-of-means beats raw-latent SAE methods on concept detection and steering — so any SAE-grouping method must clear strong simple baselines.

  The contribution lives squarely in clustering / feature-selection / classification for a learned knowledge representation (SAE features): we produce cluster-level units and a feature-level knowledge graph, evaluated on downstream classification and one steering case. Every existing post-hoc grouping method relies on OBSERVATIONAL signals — which latents fire together (co-activation feature families) or which decoders point alike (geometry). But absorption is exactly the regime where observational signals break by construction: per Chanin, the parent and the absorbing child are hierarchical and the child fires only where the parent goes silent, so the two are MUTUALLY EXCLUSIVE in firing — co-activation clustering provably cannot group them and their decoders need not be cosine-similar. This is a structural blind spot, not a tuning problem. The standard supervised remedy — select the top-N latents by causal effect on a concept probe (SCR/TPP, Karvonen 2411.18895, built on Marks SHIFT) — SILENTLY DROPS absorbed latents, because a latent that fires only in a narrow sub-context has low MARGINAL attribution even though it carries the concept there. Feature Hedging supplies the 'why': absorption, splitting and hedging are all caused by feature correlation/hierarchy — precisely the structure an INTERVENTIONAL probe (perturb the concept, watch what moves together) is built to expose.

  TWO cross-field transfers motivate the method and its robustness mechanism. (1) Systems biology faced the identical grouping obstacle: co-regulated genes are often NOT co-expressed at baseline and reveal shared regulation only under perturbation, which is why differential co-expression methods (DiffCoEx, WGCNA) cluster genes by their CORRELATED RESPONSE TO A PERTURBATION rather than baseline co-expression. Mapping genes->SAE latents and a chemical/genetic perturbation->an input content counterfactual gives the grouping mechanism. (2) Distributionally-robust learning explains WHY the recovered unit should generalize: an absorber is a dedicated detector for one sub-context, so a complementary-coverage unit is implicitly a GROUP-OF-SPECIALISTS, and a union/max-pool of specialists is robust to sub-population MIXING-WEIGHT shift in exactly the regime where a single ERM hyperplane (the surface-invariant probe) collapses on under-served minority sub-contexts (group-DRO; Mind-the-GAP 2403.09869). The insight an interpretability expert would not reach for is that SAE absorption/splitting are structurally the same obstacle that (a) defeats baseline co-expression in biology and (b) makes ERM probes brittle under subpopulation shift — so observational co-activation/geometry AND marginal-attribution selection are the wrong instruments, interventional co-response is the matched grouping instrument, and the recovered absorbers ARE the latent subpopulations a robust classifier needs.

  If correct, this gives a training-free, single-GPU, human-auditable way to turn off-the-shelf public SAEs (Gemma Scope) into reliable concept units — with a measurable recall recovery on absorbed sub-contexts, an auditable specialization graph, and a robustness story grounded in subpopulation shift. If incorrect, the honest negatives are themselves actionable: that observational co-response equals interventional co-response (no gain from intervention), that grouping ties flat supervised selection (selection not grouping), or that SAE units should be abandoned in favor of dense surface-invariant probes for robust classification.
assumptions:
- >-
  MINIMAL PAIRS ARE OBTAINABLE AT HIGH QUALITY, LOW COST, AND NON-CIRCULARLY. Primary content-flips use HUMAN-WRITTEN parallel
  corpora needing no LLM generation: ParaDetox (s-nlp, ACL 2022) toxic<->neutral for toxicity, Kaushik 2020 (ICLR) crowd-revised
  IMDB minimal pairs for sentiment, and CEBaB (Abraham 2022) human aspect-edited restaurant reviews for the food and service
  families. For rare toxicity sub-attributes (threat, identity_attack) and first-letter substitutions, LLM-generated pairs
  (OpenRouter, well under $10) are each LLM-judge-scored for content-flipped + surface-preserved, with reported pass rates
  and sensitivity to the pair-quality threshold. Any activation-space content edit, if used, is derived from an INDEPENDENT
  held-out diff-of-means on DISJOINT data, never from the SAE latents being grouped, so there is no circularity.
- >-
  THE MECHANISM IS PILOT-GATED IN BOTH HEADLINE REGIMES BEFORE THE FULL RUN. Absorption arm (first-letter): the general latent
  (max encoder-cosine with the LR first-letter probe, per Chanin 2409.14507) and its absorbers (ablation effect on the correct-minus-mean-incorrect-letter
  logit where the general latent is silent) show COMPLEMENTARY COVERAGE — mutually-exclusive support whose pooled response
  tracks the flip above the shuffled-pair null. Splitting arm (toxicity): MULTIPLE latents carry toxicity with positively-correlated
  content-response above null AND a pooled unit beats both the single best toxicity latent and the matched diff-of-means on
  a held-out IID slice. Each arm has a symmetric decision rule; the headline proceeds only in a regime its pilot confirms,
  and a pilot null is reported as a mechanism finding.
- >-
  THE WIN, IF IT OCCURS, IS ATTRIBUTABLE TO GROUPING, NOT TO EXTRA SUPERVISION OR CAPACITY. The conceded dense baseline (surface-invariant
  matched probe) is information-matched via LEACE/mean-projection erasure of the surface direction estimated from the SAME
  surface-flip pairs. The SUPERVISED ORACLE UNIT (SCR/TPP top-N) controls for label selection. The CAPACITY-MATCHED nonlinear
  probe is pinned precisely (per reviewer): max-pool over EXACTLY the number of raw residual-stream directions equal to the
  admitted unit's member count, selected by the SAME SCR/TPP attribution criterion as the oracle, on the matched paired activations
  — so it controls member-count AND pooling nonlinearity, and any residual unit advantage is attributable to co-response grouping
  structure rather than to count or max-pool.
- >-
  THE ROBUSTNESS GAP IS DRIVEN BY SUB-POPULATION REWEIGHTING, AND THIS IS TESTABLE BY DECOMPOSING THE SHIFT. We do not rely
  on the natural domain shift alone; we decompose it into three controlled conditions and predict where the unit wins: (i)
  a SURFACE-ONLY paraphrase shift (content held, surface changed) — the unit and the surface-invariant probe should both be
  robust here, so the unit is NOT predicted to win (this isolates and concedes surface invariance); (ii) a SUB-POPULATION-REWEIGHTING
  shift (resample the test set to up-weight sub-contexts the training probe under-serves, holding surface and label definition)
  — the unit IS predicted to win on worst-sub-context recall, growing with the reweighting magnitude; (iii) the NATURAL domain
  shift (Jigsaw Wikipedia-talk -> civil_comments; IMDB -> CEBaB/Amazon reviews), reported with the gap attributed to whichever
  component (i/ii) it tracks. If the unit's gap over the dense probe does not concentrate on condition (ii), the subpopulation
  mechanism is falsified and we report that.
- >-
  Off-the-shelf Gemma Scope SAEs on Gemma-2-2b expose latent counterfactual responses measurable above noise on a single GPU
  for a few thousand minimal pairs per concept, and the chosen attributes have enough labeled/templatable data (civil_comments
  sub-attribute floats, CAD-IMDB, CEBaB aspect labels, ParaDetox) to build minimal pairs and natural-shift test splits. Absorption
  is more severe at WIDER SAEs and splitting at larger width, so SAE width/layer is a robustness axis (16k canonical primary;
  65k is a drop-first stress point).
investigation_approach: |-
  DEPTH-FIRST EXECUTION ORDER (resolves the feasibility/breadth risk). TIER 0 (must complete): two-arm STEP-0 pilot. TIER 1 (the headline, must complete): claims C1+C3 (beat raw latent + observational clusters; mechanistic backbone / absorber recovery vs oracle) plus claim B vs C2 on the toxicity family + sentiment with the surface-invariant probe and oracle unit; first-letter absorber recovery; the shift DECOMPOSITION (surface-only + sub-population-reweighting + natural) on toxicity + sentiment; clustered-CI aggregate over the families completed. TIER 2 (attempt if Tier 1 lands; the FIRST stretch goal, committed because the goal foregrounds steering): the CEBaB food+service families AND ONE executed steering case. DROP-FIRST stretch (only if everything above lands): model-diffing, 65k-width stress point, the Veitch-MMD alternative construction, the LLM-paraphrase secondary shift, additional CEBaB aspects (noise/ambiance). PRE-COMMITTED counts: >=800 content-flip pairs and >=800 surface-flip pairs per family for the bootstrap CIs (ParaDetox/CAD/CEBaB supply this from human data; rare toxicity subtypes topped up with judge-validated LLM pairs, pass rates reported).

  STEP 0 — TWO-ARM DE-RISKING PILOT (run first, ~1-2 GPU-hours). ARM A (absorption, first-letter): find the general first-letter latent (max encoder-cosine with LR probe) and its absorbers (ablation on the correct-minus-mean-incorrect-letter logit where the general latent is silent); build first-letter content-flip pairs; measure (a) correlated content-response (expected low/disjoint) and (b) COMPLEMENTARY coverage (pooled max tracks the flip where members have holes) vs the shuffled-pair null. ARM B (splitting, toxicity): on ParaDetox/civil_comments, measure how many latents carry toxicity, whether their content-response profiles are positively correlated above null, and whether the pooled unit beats the single best toxicity latent and the matched diff-of-means on a held-out IID slice. Symmetric decision rules; proceed with a regime as headline only if its pilot clears the null (and, for B, shows a non-trivial IID edge); otherwise report that regime's null as a mechanism finding.

  COUNTERFACTUAL SIGNAL. Encode every text and its counterfactual with a frozen Gemma Scope residual-stream SAE (layer ~12, width 16k canonical). Per latent: content-response = delta(activation) under content-flip; surface-response = delta under surface-flip. Aggregate into per-latent response profiles across contexts.

  CLUSTERING METHOD (the in-scope contribution). Build a latent-by-context content-response matrix. Cluster latents with a differential-correlation affinity (DiffCoEx-style) for signature C and a coverage-complementarity term for signature K, via agglomerative clustering / graph community detection on the affinity. Finalize each candidate unit with the SINGLE ADMISSION RULE: clear signature C (within-unit content-response correlation > 95th-pct shuffled-pair null) OR signature K (pooled-minus-best-member AUC gain > 95th-pct of the MATCHED best-of-random-k null drawn from content-responsive latents, AND mutual-exclusivity Jaccard < 0.1, AND per-member precision floor >= 0.7), AND pass unit-level surface invariance. Report the cleared signature per concept and the false-admit rate under both the all-latent and matched random-k nulls (<= 0.05). Emit human-auditable unit definitions (member latents, logit-lens tokens, conditioning contexts) and directed specialization edges (a member responsive only in a sub-context = absorbed/split child) = a feature-level knowledge graph.

  WORKED EXAMPLE. Toxicity unit (splitting): members = {profanity/slur latent, demeaning-insult latent, aggressive-imperative latent}; under ParaDetox detox all three drop together (signature C); pooled max tracks toxicity; pooled surface-response to paraphrase ~ 0. First-letter unit (absorption): members = {general 'starts-with-L' latent (silent on 'lion'/'London'), 'lion'-absorber, 'London'-absorber}; no member tracks 'starts-with-L' everywhere, pooled max does (signature K); members never co-fire (Jaccard ~ 0); pooled surface-response ~ 0.

  BASELINES (matched baselines are primary). (a) best raw single latent; (b) observational co-activation clustering / feature families; (c) decoder-geometry clustering; (d) counterfactually-matched diff-of-means; (e) counterfactually-matched linear probe; (f) surface-invariant matched probe = (d)/(e) with the surface-flip direction LEACE/mean-projection erased (Belrose 2024) — the conceded non-SAE dense baseline; (g) supervised oracle unit = pool top-N latents by SCR/TPP probe-attribution (Karvonen 2411.18895 / Marks SHIFT); (h) capacity-matched nonlinear probe = max-pool over EXACTLY #members raw residual directions selected by the SAME SCR/TPP attribution as (g), on matched paired activations (controls count + pooling nonlinearity); (i) unmatched diff-of-means / linear probe on raw labels.

  EVAL — HEADLINE (mechanistic backbone, reported regardless of dense-probe competitiveness): (1) co-response units have low Jaccard with co-activation/geometry clusters above the stability/shuffled-pair null; (2) units win specifically on the differing members — sliced RECALL on the sub-contexts where the best latent / observational clusters / the oracle's top-N have holes, including absorbers the oracle drops; (3) agreement of knowledge-graph specialization edges with the supervised absorption diagnostic (2409.14507) on first-letter. EVAL — CLASSIFICATION (C1 primary, C2 + dense-probe supporting): unit-pooled activation (max/sum over members) as classifier on IID and under the THREE decomposed shifts; report F1/AUC AND worst-sub-context recall; vs the dense surface-invariant probe report the SLICED worst-sub-context recall gap under sub-population reweighting with its predicted positive sign and growth, and report aggregate F1 honestly (a tie is acceptable). Aggregate across the ~4 families with a CLUSTERED bootstrap CI (toxicity = one family-level estimate). CLUSTER-STABILITY: bootstrap over minimal pairs (adjusted Rand / Jaccard across resamples), the shuffled-pair null for the affinity matrix, sensitivity to pairs-per-concept.

  STEERING (Tier 2, ONE executed case). Steer with the toxicity unit's shared content-response direction vs best single latent vs the matched surface-invariant diff-of-means; measure on-target effect and side-effects (KL on unrelated prompts, fluency) at MATCHED on-target effect with bootstrap CIs; engage 'SAEs Are Good for Steering — If You Select the Right Features' (2505.20063) and the AxBench protocol.

  HONEST FAILURE-MODE REPORTING. Dependence on counterfactual quality (pass rates); concepts with no surface-invariant co-responding/complementary group; regimes where co-response collapses to co-activation (no gain over observational); cases where the dense surface-invariant probe matches the unit on sliced recall too (reframes to 'invariance supervision suffices, grouping adds only auditability'); cases where the oracle ties the unit (reframes to 'selection, not grouping'); co-response too noisy to cluster (ARI ~ null); a pilot arm showing neither correlated nor complementary above-null structure; the gap NOT concentrating on the sub-population-reweighting shift component (falsifies the headline mechanism); compute/SAE-width sensitivity; bias_in_bios boundary-null.
success_criteria: >-
  CONFIRMED if, pre-registered in this nesting: (1) the two-arm STEP-0 pilot confirms above-null structure in at least one
  regime (positively-correlated content-response for splitting and/or complementary coverage for absorption), with the toxicity
  arm also showing a pooled IID edge over the best single latent and the matched diff-of-means; (2) HEADLINE — the mechanistic
  backbone holds: co-response units have low Jaccard with co-activation/geometry clusters (above the stability/shuffled-pair
  null) AND win on the differing members — sliced recall on the sub-contexts where the best latent, observational clusters,
  and the oracle's top-N attribution have holes, including recovered absorbers — on first-letter AND at least one safety concept;
  (3) C1 — the unit beats the best raw single latent and observational co-activation/geometry clustering on classification
  across the families (clustered-CI aggregate); (4) C2 — the unit matches-or-beats the supervised oracle unit and the count-and-capacity-matched
  nonlinear probe, so the gain is grouping rather than supervised selection or max-pool nonlinearity; (5) DENSE-PROBE PREDICTION
  (supporting, scoped) — against the surface-invariant matched probe, the unit shows a POSITIVE worst-sub-context recall gap
  that GROWS with the measured sub-population-reweighting magnitude (condition ii of the shift decomposition), even if aggregate
  F1 ties; (6) admission integrity — false-admit rate <= 0.05 under BOTH the all-latent and matched random-k nulls, cluster
  assignments stable across bootstrap resamples (adjusted Rand/Jaccard above null), and knowledge-graph specialization edges
  agree with the supervised absorption diagnostic (2409.14507) on first-letter. TIER 2 (confirmatory only): one steering case
  where the unit direction achieves lower KL side-effects than best-single-latent and the matched diff-of-means at matched
  on-target effect. HONEST NEGATIVES, each publishable: co-response grouping ties observational co-activation grouping (no
  gain from intervention); the unit fails C1/C3 (units no better than raw latents/observational clusters even on sliced recall);
  the dense surface-invariant probe matches the unit on sliced recall under reweighting too (grouping then contributes only
  auditability + the knowledge graph); the oracle ties the unit (selection not grouping); the gap does NOT concentrate on
  the sub-population-reweighting component (headline mechanism falsified); co-response too noisy to cluster (ARI ~ null);
  a pilot arm shows neither correlated nor complementary above-null structure. bias_in_bios is a pre-registered boundary-null,
  not method failure.
related_works:
- >-
  AxBench: Steering LLMs? Even Simple Baselines Outperform Sparse Autoencoders (Wu et al., ICML 2025 spotlight, 2501.17148):
  on Gemma-2-2B/9B, difference-in-means is the strongest concept-detection method and SAEs are not competitive. This sets
  our bar. We differ by making diff-of-means maximally fair (counterfactually matched AND surface-invariant via concept erasure),
  then scoping the contribution to (a) beating raw latents + observational clusters, (b) recovering absorbers that marginal-attribution
  selection drops, and (c) a sliced sub-population-shift recall gap — NOT a blanket aggregate-F1 win over diff-of-means.
- >-
  Sparse Autoencoders Do Not Find Canonical Units of Analysis (Bussmann et al., ICLR 2025, 2502.04878): uses SAE stitching
  and meta-SAEs to argue SAEs do not learn canonical units; its remedy is geometric/training-based. We propose a BEHAVIORAL
  unit defined by counterfactual co-response and unit-level surface invariance, evaluated on downstream classification + one
  steering case, with no retraining.
- >-
  Feature Hedging: Correlated Features Break Narrow SAEs (Chanin, Dulka, Garriga-Alonso, 2505.11756): ABSORPTION learns gerrymandered
  latents (worse at WIDER SAEs, both features tracked across mutually-exclusive latents via a parent->child hierarchy) vs
  HEDGING merges correlated features into a SINGLE polysemantic latent (worse at NARROWER SAEs). We use this to (a) scope
  grouping to splitting+absorption (a hedged single latent is not groupable) and (b) treat correlation/hierarchy as the mechanistic
  cause our interventional probe exposes.
- >-
  A is for Absorption (Chanin et al., 2409.14507, NeurIPS): a SUPERVISED DIAGNOSTIC — identify the first-letter latent by
  max encoder-cosine with an LR probe and use ablation on the correct-minus-incorrect-letter logit to find the absorbing latent.
  It DETECTS absorption on individual latents; it does not GROUP parent+absorbers into a usable unit. We use it as a partial
  ORACLE for the pilot and to validate knowledge-graph edges; our contribution is the unsupervised grouping/repair.
- >-
  Counterfactual Invariance to Spurious Correlations (Veitch, D'Amour, Yadlowsky, Eisenstein, NeurIPS 2021, 2106.00545): an
  MMD-based regularizer enforcing the counterfactual-invariance signature without counterfactual examples, with conditional
  MMD in the anti-causal direction (Y causes X, as for toxicity/sentiment). We import this as a DROP-FIRST alternative construction
  of the surface-invariant baseline; the primary construction is LEACE/mean-projection erasure. The grouping must show its
  scoped advantage over this baseline (sliced recall + auditability), not merely beat it on F1.
- >-
  LEACE: Perfect linear concept erasure in closed form (Belrose et al., 2306.03819) and mean-projection erasure: we erase
  the surface-flip direction to build the surface-invariant probe — a strong, principled non-SAE baseline. Crucially, LEACE
  erases a single/low-rank TRAINING-estimated subspace, which motivates our a-priori mechanism: it cannot remove multi-dimensional/context-dependent
  surface confounds that differ across domains.
- >-
  SHIFT / SCR / TPP SAE evaluation (Marks et al. 2024; Karvonen et al. 2411.18895): these SELECT individual SAE latents by
  ranking causal effect on a concept probe (top-N), then ablate the set; they do NOT cluster latents by interventional co-response.
  This is exactly our supervised ORACLE-UNIT baseline, and a latent firing only in a narrow sub-context (an absorber) has
  low marginal attribution and is silently dropped — the specific gap our coverage grouping fills and the headline mechanistic
  backbone targets.
- >-
  Discovering Concept Directions from Diffusion-based Counterfactuals via Latent Clustering (CDLC, 2505.07073; Pattern Recognition
  Letters 2025): clusters latent DIFFERENCE vectors from factual + diffusion-generated counterfactual IMAGE pairs into global
  class-specific concept DIRECTIONS (validated on skin-lesion data). It is the closest 'cluster counterfactual differences'
  template, but on a DIFFERENT substrate: it yields one continuous direction per class in a diffusion latent space, in vision.
  We cluster DISCRETE SAE dictionary latents on a frozen LLM by their co-response PROFILES into auditable MULTI-MEMBER units,
  add unit-level surface invariance, and specifically target the ABSORPTION regime via complementary coverage — none of which
  CDLC addresses.
- >-
  Causal-differentiating / counterfactual concept-representation methods for LMs (e.g. CausaLM, Feder et al. 2020, MIT Press
  CL 2021; and OpenReview 'Causal Differentiating Concepts'): learn or adversarially fine-tune a counterfactual concept REPRESENTATION
  / direction to isolate a concept's causal effect. These produce a (learned) concept direction or a concept-invariant model,
  not a clustering of pre-existing discrete SAE latents; they do not address SAE absorption/splitting or build a multi-member
  auditable unit. We are training-free over frozen public SAEs and our object is the discrete-latent GROUP.
- >-
  Counterfactually-Augmented Data (Kaushik, Hovy, Lipton, ICLR 2020) and CEBaB (Abraham et al., NeurIPS 2022, 2205.14140):
  human-written counterfactual minimal pairs for sentiment (IMDB) and ASPECT concepts (food/service/ambiance/noise in restaurant
  reviews), with out-of-domain sources. We use CAD as one independent concept axis and CEBaB food/service as TWO MORE genuinely
  independent axes (raising effective-n toward 4), plus CEBaB/cross-domain reviews as a natural shift; these supply non-circular
  pairs, not the grouping method.
- >-
  Co-activation feature families and graph-regularized SAEs (Disentangling Dense Embeddings 2408.00657; GSAE 2512.06655; Sparse
  Feature Coactivation 2506.18141): group SAE features by OBSERVATIONAL co-activation/geometry. By construction these cannot
  group a concept's absorbed/split latents (mutually exclusive in firing). We use the opposite, INTERVENTIONAL signal (correlated
  change, or complementary coverage, under a content counterfactual), training-free on frozen public SAEs, and demonstrate
  the structural blind spot directly via low-Jaccard + sliced-recall wins.
- >-
  Mutual-exclusivity / Ising-coupling and slot-conditional exclusivity grouping of SAE latents (Bhalla et al. global Ising
  coupling; slot-conditional exclusivity studies): group latents by negative co-occurrence. Exclusivity shows two latents
  do not co-fire but not that they belong together. We supply the missing POSITIVE interventional signal (correlated co-response
  for splitting; complementary coverage of the same content flip for absorption) plus a precision floor.
- >-
  Group Distributionally Robust Optimization and subpopulation-shift robustness (Sagawa et al. group-DRO; 'Mind the GAP: Group-Aware
  Priors', 2403.09869): a single ERM model collapses on under-served minority subgroups under mixing-weight shift, and group-aware
  methods recover worst-group performance. We do NOT propose a new DRO method (no learning-theory theorem); we BORROW this
  as the a-priori mechanism explaining why a complementary-coverage unit (a group-of-specialists whose absorbers are the latent
  subpopulations) should out-generalize a single surface-invariant probe on worst-sub-context recall under sub-population
  reweighting. The connection of SAE absorption to latent subpopulations is, to our knowledge, novel.
- >-
  Differential co-expression / perturbation co-response module discovery in systems biology (DiffCoEx, BMC Bioinformatics
  2010; WGCNA): cluster genes by their CORRELATED RESPONSE TO A PERTURBATION rather than baseline co-expression, because co-regulated
  genes are often not co-expressed at baseline. This is the methodological root transferred; to our knowledge never applied
  to SAE/LLM features. Our novel claim is that the same baseline-vs-perturbation distinction explains and repairs SAE absorption/splitting,
  extended with a complementary-coverage variant for the mutually-exclusive absorption case.
- >-
  Domain-Filtered Knowledge Graphs from SAE Features (2604.23829): builds an internal knowledge graph from SAE features via
  contrastive corpus filtering, co-occurrence, decoder geometry — purely OBSERVATIONAL. Our feature-level knowledge graph
  is built from INTERVENTIONAL co-response/complementary-coverage grouping, so its edges encode conditioning environments
  and specialization (absorbed/split children) invisible to observational co-occurrence.
inspiration: >-
  A dual cross-field transfer. The GROUPING mechanism is a Level-3 (methodological) import from systems biology's differential
  co-expression / perturbation co-response module discovery (DiffCoEx, WGCNA): cluster units by their CORRELATED RESPONSE
  TO A PERTURBATION, not by baseline co-expression, because co-regulated genes are frequently not co-expressed until perturbed
  — mapping genes->SAE latents and a chemical/genetic perturbation->an input content counterfactual. The ROBUSTNESS mechanism
  (added this round to close the headline-mechanism gap) is a Level-1/2 import from distributionally-robust learning / subpopulation-shift
  research (group-DRO; Mind-the-GAP 2403.09869): a single ERM hyperplane collapses on under-served minority subgroups under
  mixing-weight shift, whereas a union of specialists is robust — and an absorber is precisely a specialist for one latent
  sub-context, so a complementary-coverage unit is implicitly group-aware and should win on worst-sub-context recall under
  sub-population reweighting. These fuse with (i) causal ML's counterfactual invariance (Veitch 2021) and concept-erasure
  (LEACE, Belrose 2024), which build the conceded surface-invariant baseline; (ii) NLP minimal-pair counterfactuals (ParaDetox,
  Kaushik 2020 CAD, CEBaB aspects) for non-circular human-written perturbations and independent concept axes; and (iii) a
  complementary-coverage (set-cover-style) extension for absorption where plain correlation fails. The unifying insight an
  interpretability expert would not reach for: SAE absorption/splitting are structurally the same obstacle that (a) defeats
  baseline co-expression in biology and (b) makes ERM probes brittle under subpopulation shift — so observational co-activation/geometry
  AND marginal-attribution selection are the wrong instruments, interventional co-response is the matched grouping instrument,
  and the recovered absorbers ARE the latent subpopulations a robust classifier needs.
terms:
- term: Sparse autoencoder (SAE) latent
  definition: >-
    A single unit of a sparse dictionary trained to reconstruct a language model's internal activations; each latent has an
    encoder direction (when it fires) and a decoder direction (what it writes back), intended to correspond to one interpretable
    concept.
- term: Feature absorption
  definition: >-
    A sparsity-induced failure (Chanin et al. 2409.14507, 2505.11756) requiring a parent->child hierarchy (child fires only
    if parent fires): the more specific child latent suppresses the firing of the more general parent latent, which then has
    unpredictable holes. Both features stay tracked across mutually-exclusive 'gerrymandered' latents; absorption is worse
    at WIDER SAEs.
- term: Feature splitting vs feature hedging
  definition: >-
    Splitting = one concept fragments across MANY latents (worse at larger width); these sub-latents co-respond POSITIVELY
    to a content flip and are the groupable signature-C regime. Hedging (Chanin 2505.11756) = a narrow SAE MERGES correlated
    features into a SINGLE polysemantic latent (worse at narrower width); a hedged single latent is NOT a grouping target
    but explains why inter-latent correlation exists.
- term: Counterfactual minimal pair
  definition: >-
    Two inputs differing in exactly one targeted way: a content-flip pair changes whether a concept is present while holding
    surface fixed; a surface-flip pair paraphrases/rewrites surface while holding content fixed. Human-written pairs (ParaDetox,
    Kaushik 2020 CAD, CEBaB aspects) are used where available; LLM-generated pairs are LLM-judge-validated for content-flip
    and surface-preservation.
- term: Interventional co-response (grouping criterion)
  definition: >-
    Latents belong to the same concept unit if they jointly track the content perturbation across contexts, even if their
    baseline activations never co-occur. Realized in two signatures via a single admission rule: positive correlation of content-response
    profiles (signature C, splitting) and complementary coverage (signature K, absorption).
- term: Complementary coverage (signature K)
  definition: >-
    The absorption-regime grouping signal: members respond to the SAME content flip on DISJOINT context supports, so no single
    member tracks the concept everywhere but the group's POOLED (max-over-members) content-response covers the flip across
    all contexts. Admitted only with a mutual-exclusivity constraint (Jaccard < 0.1), a per-member precision floor (>= 0.7),
    and a best-of-random-k null MATCHED on marginal content-response AUC (so the test isolates coverage, not mere content-responsiveness).
- term: Single unit admission rule
  definition: >-
    A candidate unit is admitted iff it clears signature C (within-unit content-response correlation above the 95th-pct shuffled-pair
    null) OR signature K (pooled-minus-best-member AUC gain above the MATCHED best-of-random-k null, with mutual-exclusivity
    and precision-floor constraints), AND its pooled surface-response is not above the shuffled-surface null. The cleared
    signature is reported per concept and the false-admit rate is reported under both nulls (target <= 0.05).
- term: Surface-invariant matched probe (conceded non-SAE baseline)
  definition: >-
    A counterfactually-matched diff-of-means/linear probe on content-flip residual deltas, made surface-invariant by ERASING
    the surface-flip direction via LEACE / mean-projection (Belrose 2024), with a Veitch 2021 conditional-MMD regularizer
    as a drop-first alternative. It is a single (or low-rank) hyperplane after erasing ONE training-estimated surface subspace;
    we predict the unit beats it only on a SLICED sub-population-shift recall metric, not necessarily on aggregate F1.
- term: Supervised oracle unit
  definition: >-
    A baseline that pools the top-N latents selected by a supervised probe-attribution causal-effect criterion (SCR/TPP, Karvonen
    2411.18895 / Marks SHIFT). Because it ranks by MARGINAL attribution it silently drops absorbed latents firing only in
    narrow sub-contexts; the co-response unit must match/beat it to show grouping by co-response STRUCTURE adds value over
    flat supervised selection.
- term: Capacity-matched nonlinear probe (baseline h)
  definition: >-
    Max-pool over EXACTLY the number of raw residual-stream directions equal to the admitted unit's member count, selected
    by the SAME SCR/TPP attribution criterion as the oracle, on the matched paired activations. It controls member-count AND
    pooling nonlinearity, so any residual unit advantage is attributable to co-response grouping structure rather than to
    count or max-pool.
- term: >-
    Worst-sub-context recall under sub-population reweighting (headline classification slice)
  definition: >-
    Recall measured on the sub-contexts a training-fit linear probe under-serves, evaluated as the test mixture is re-weighted
    toward those sub-contexts. The complementary-coverage unit (a group-of-specialists, each absorber a sub-context detector)
    is predicted to keep this recall stable while a single surface-invariant hyperplane collapses — the mechanism borrowed
    from group-DRO / subpopulation-shift research.
- term: Group-of-specialists (robustness framing)
  definition: >-
    The view that a complementary-coverage unit's members are dedicated detectors for disjoint sub-contexts, making the max-pooled
    unit implicitly group-aware and robust to sub-population MIXING-WEIGHT shift, in the regime where a single ERM hyperplane
    collapses on minority subgroups. Borrowed framing (group-DRO; Mind-the-GAP 2403.09869), not a new theorem.
- term: Shift decomposition
  definition: >-
    Splitting the evaluation shift into three controlled conditions — (i) surface-only paraphrase (unit NOT predicted to win),
    (ii) sub-population reweighting (unit predicted to win on worst-sub-context recall), and (iii) natural domain shift (attributed
    to i or ii) — so the unit-minus-probe gap is attributed to a specific, mechanism-aligned component rather than a bundled
    confound.
- term: Reliable unit of analysis
  definition: >-
    A human-auditable group of SAE latents that tracks a concept dependably across surface variation and sub-population reweighting
    — recovering recall that absorption/splitting destroy at the single-latent level and that marginal-attribution selection
    drops — reusable as a classifier (headline) and secondarily for steering.
summary: >-
  SAE latents encoding one concept are often mutually exclusive in firing (feature absorption and splitting), so observational
  co-activation, decoder geometry, and marginal-attribution selection all structurally miss the right members; clustering
  latents instead by how they jointly track a content counterfactual (correlated co-response for splitting, complementary
  coverage for absorption, admitted by one null-anchored rule and made surface-invariant at the pooled-unit level) recovers
  auditable multi-member concept units. The headline test is that these units recover absorbers the supervised oracle's top-N
  attribution drops and, because each absorber is a sub-context specialist, keep worst-sub-context recall stable under sub-population
  reweighting where a single surface-invariant probe collapses — over ~4 independent concept families, with aggregate-F1 parity
  to the dense probe treated as an acceptable, honestly-reported outcome.
</previous_hypothesis>

<previous_review_feedback>
A reviewer evaluated your previous hypothesis and provided the feedback below.

IMPORTANT: Do NOT generate a completely new hypothesis. Take the previous hypothesis above and
REVISE it to address the feedback. Keep what works, fix what was criticized.

You MUST address ALL the critiques. Do NOT repeat the same mistakes.

kind: reviewer_feedback
id: review_hypo_a065cb6c6154
overall_assessment: >-
  This is a strong, much-improved revision of the interventional co-response SAE-latent grouping hypothesis. All six critiques
  from the previous round are adequately addressed: (1) the headline-mechanism gap is fixed with a DUAL move — the mechanistic
  backbone (absorber recovery vs the SCR/TPP oracle, low-Jaccard, wins-on-differing-members) is promoted to the actual headline,
  and a concrete a-priori mechanism (group-of-specialists robustness under sub-population reweighting, borrowed from group-DRO
  / Mind-the-GAP) is articulated with a pre-registered sign+growth prediction while honestly conceding aggregate-F1 parity;
  (2) the n-count is reframed as ~4 genuinely independent families with a clustered/hierarchical bootstrap CI; (3) execution
  risk is contained with an explicit MVP + depth-first TIER 0/1/2 + drop-first stretch and pre-committed pair counts; (4)
  the signature-K null is now matched on marginal content-responsiveness; (5) baseline (h) is pinned precisely; (6) CDLC (2505.07073)
  and the CausaLM/Causal-Differentiating-Concepts family are cited and differentiated. The core idea remains novel and well-motivated:
  interventional co-response is the matched instrument for absorption/splitting precisely where observational co-activation/geometry
  and marginal-attribution selection are structurally blind, transferred from differential co-expression in systems biology.
  The design is rigorous (single null-anchored admission rule, matched baselines a-i, pre-registered honest negatives, pilot-gating),
  training-free, auditable, and feasible on a single GPU. The remaining concerns are NOT fatal and all have pre-registered
  honest-negative paths, so the score holds at Weak Accept rather than dropping. What keeps it from a clean Accept is that
  the NEWLY-PROMOTED subpopulation-shift headline is still under-controlled: as pre-registered, the sliced worst-sub-context-recall
  win is asserted against the single-hyperplane dense probe (f), but the same group-DRO mechanism predicts the capacity-matched
  POOLED baseline (h) is also robust under reweighting — so that comparison does not yet isolate GROUPING from mere pooling-of-multiple-specialists,
  the natural strong baseline (a group-aware/DRO dense probe, and the label-free worst-group-robustness literature) is absent,
  and the integrity of the reweighting construction needs locking down to avoid a trivially-true-by-construction result. Closing
  these two issues is the clear path from 6 to 7.
strengths:
- >-
  Genuinely novel and well-scoped core: clustering DISCRETE SAE dictionary latents by INTERVENTIONAL co-response (correlated
  change for splitting; complementary coverage for absorption) targets exactly the regime — mutually-exclusive absorbed/split
  latents — where observational co-activation/geometry clustering is provably blind and where marginal-attribution selection
  (SCR/TPP) silently drops absorbers. The structural-blind-spot argument is correct and the closest prior work (CDLC vision/diffusion
  latent-difference clustering; co-activation feature families 2506.18141; Bhalla Ising exclusivity) is cited and cleanly
  differentiated.
- >-
  The dual cross-field transfer is principled, not decorative: DiffCoEx/WGCNA supplies the grouping instrument (perturbation
  co-response > baseline co-expression), and group-DRO/subpopulation-shift supplies an a-priori robustness mechanism — closing
  the prior round's biggest gap — rather than leaving 'advantage grows under shift' as a bare assertion.
- >-
  Excellent pre-registration and attribution hygiene: three nested claims each with its own baseline; a single falsifiable
  admission rule with a matched random-k null and false-admit reporting under both nulls; a comprehensive matched-baseline
  set (a-i) including an information-matched surface-invariant LEACE probe, a supervised oracle unit, and a count-and-pooling-matched
  nonlinear probe; and an unusually complete catalogue of pre-registered, individually-publishable honest negatives (including
  a falsifier for the headline mechanism itself — the gap NOT concentrating on the reweighting component).
- >-
  Strong feasibility discipline: explicit minimum-viable-result stated first, depth-first TIER 0/1/2 ordering with drop-first
  stretch goals, human-written non-circular minimal pairs (ParaDetox / Kaushik CAD / CEBaB) as primary, pre-committed ≥800-pair
  counts for the bootstrap CIs, and a frozen-SAE training-free pipeline on a single GPU — a realistic plan that maps directly
  onto the venue's single-GPU / auditable / honest-failure constraints.
- >-
  Honest about the AxBench bar: the paper explicitly does NOT claim a blanket aggregate-F1 win over diff-of-means, scopes
  the dense-probe comparison to a mechanism-predicted sliced metric, and treats a tie as an acceptable, pre-registered outcome
  — a mature framing that de-risks the headline against the strongest simple baseline.
dimension_scores:
- dimension: soundness
  score: 3
  justification: >-
    Methodologically rigorous: single null-anchored admission rule, matched random-k and shuffled-pair nulls, comprehensive
    matched baselines, pilot-gating, cluster-stability stats, and pre-registered falsifiers including one for the headline
    mechanism. Held at 3 (not 4) because the newly-promoted subpopulation-shift headline is under-controlled: the same group-DRO
    mechanism that predicts the unit beats the single-hyperplane dense probe (f) also predicts the capacity-matched POOLED
    baseline (h) is robust under reweighting, so the pre-registered sliced-recall-vs-(f) win does not isolate grouping from
    pooling; the natural strong baseline (a group-aware/DRO dense probe) is missing; and the reweighting-construction integrity
    (independent sub-context definition) needs locking down to avoid a trivially-true result.
  improvements:
  - >-
    Pre-register the unit-vs-(h) prediction on the SLICED worst-sub-context-recall metric, not only unit-vs-(f); state explicitly
    that vs-(f) demonstrates 'multiple specialists beat one hyperplane' (a pooling/capacity effect predicted by the same mechanism)
    whereas only unit-vs-(h) plus absorber-recovery (C3) isolates co-response GROUPING.
  - >-
    Add a group-aware dense-probe baseline: an oracle group-DRO / worst-group probe trained WITH the sub-context labels (an
    upper bound), so the contribution can be framed and tested as 'the unsupervised unit approaches group-DRO robustness WITHOUT
    sub-context labels.'
  - >-
    Lock the reweighting construction: define sub-contexts from INDEPENDENT labels/annotation fixed before any unit-vs-probe
    comparison, determine 'under-served' on the dense probe alone, and report a non-triviality check (the probe genuinely
    collapses on independently-defined sub-contexts, not artificially-constructed ones).
- dimension: presentation
  score: 3
  justification: >-
    Clearly organized into MVP / nested claims / admission rule / tiers / baselines / honest negatives, and an expert can
    follow and evaluate it. But it is extremely dense — heavy ALL-CAPS, deeply nested parentheticals, and two distinct mechanisms
    (absorption/signature-K on first-letter vs splitting/signature-C + subpopulation-reweighting on toxicity) bundled under
    one 'headline' — which makes the single load-bearing result hard to extract on a first read.
  improvements:
  - >-
    Add one compact claims × baselines × metrics table (rows: C1/C2/C3/dense-probe-prediction; columns: which baseline, which
    metric, predicted sign) so a reviewer can read the headline result off a grid rather than reconstructing it from prose.
  - >-
    State the single headline sentence plainly once ('the unsupervised co-response unit recovers absorbers the oracle drops
    and keeps worst-sub-context recall stable under reweighting where a single dense probe collapses') and separate the two
    regime-specific stories (first-letter absorption vs toxicity splitting) so they are not conflated.
- dimension: contribution
  score: 3
  justification: >-
    Addresses a real, well-motivated problem (single SAE latents are unreliable units), proposes a genuinely novel and matched
    instrument, and delivers auditable multi-member units + a feature-level specialization graph that others could build on.
    Significance is high for interpretability/feature-selection. Capped at 3 because the headline's practical payoff hinges
    on the still-open question of whether GROUPING (not just pooling multiple specialists) is what buys the robustness, and
    the honest aggregate-F1-tie concession means the classifier-utility ceiling is modest unless the sliced-recall and absorber-recovery
    wins are decisive and grouping-attributable.
  improvements: []
critiques:
- id: ''
  category: methodology
  severity: major
  description: >-
    The newly-promoted subpopulation-shift headline does not yet ISOLATE grouping from pooling, and risks being trivially
    true by construction. (1) Attribution: the group-DRO 'group-of-specialists' mechanism that predicts the unit beats the
    single-hyperplane surface-invariant probe (f) on worst-sub-context recall ALSO predicts that the capacity-matched POOLED
    baseline (h) — itself a max-pool over multiple SCR/TPP-selected directions — is robust under reweighting. So the pre-registered
    prediction 'sign(unit_recall − probe_recall) > 0, growing with reweighting magnitude' is stated only against (f), the
    one-hyperplane baseline, and a win there is explained by 'multiple specialists vs one hyperplane' (a pooling/capacity
    effect) rather than by co-response grouping. The grouping-isolating comparison is unit-vs-(h) on the SAME sliced metric,
    which is not pre-registered as a headline prediction — success criterion (4)/C2 only asks the unit to 'match-or-beat'
    (h) on classification generally. (2) Construction integrity: max-pooled recall is approximately invariant to mixing weights
    almost BY CONSTRUCTION if each member perfectly covers one sub-context, so unless the sub-contexts are defined from labels/annotation
    that are independent of the unit's members and fixed before the comparison, and 'under-served' is determined on the dense
    probe alone, the headline metric can be rigged to favor the unit.
  suggested_action: >-
    Pre-register the unit-vs-(h) prediction on the worst-sub-context-recall slice and state which comparison demonstrates
    what: unit-vs-(f) = 'multiple pooled specialists beat one hyperplane' (predicted by the same mechanism, NOT grouping evidence);
    unit-vs-(h) + absorber-recovery (C3) = the grouping-isolating tests. Add a degenerate-construction guard: define sub-contexts
    from independent labels (toxicity subtypes / CEBaB aspect levels) frozen before any unit-vs-probe result, determine under-served
    sub-contexts on the dense probe only, pre-register the reweighting-magnitude axis, and report that the dense probe genuinely
    collapses on these independently-defined sub-contexts. If unit ties (h) on the slice, report honestly that the robustness
    is a pooling effect and the grouping contribution rests on absorber-recovery + auditability.
- id: ''
  category: novelty
  severity: major
  description: >-
    By promoting subpopulation-shift robustness (group-DRO / Mind-the-GAP 2403.09869) to the headline, the revision steps
    directly into the 'worst-group / subpopulation robustness WITHOUT group labels' subfield — JTT (Just Train Twice, 2107.09044),
    GEORGE, EIIL, LfF, and 2024-25 follow-ups — which is currently uncited and unbaselined. These methods are exactly the
    established competitors for the paper's most compelling framing ('the unit achieves subpopulation robustness without sub-context
    labels'). A reviewer from the robustness area will immediately ask how an unsupervised co-response unit compares to (a)
    a group-DRO probe WITH oracle sub-context labels (the upper bound) and (b) label-free group-inference baselines. With
    neither cited nor run, the robustness headline reads as untested against the obvious strong baseline, and the cross-field-transfer
    novelty is overstated relative to a subfield that already does 'group robustness from inferred groups.'
  suggested_action: >-
    Cite and differentiate the label-free worst-group-robustness literature (JTT, GEORGE, EIIL, LfF) and position the contribution
    as 'group-of-specialists from interventional co-response = a representation-level, training-free, auditable route to subpopulation
    robustness vs their loss-reweighting/group-inference route.' Add at least an oracle group-DRO dense probe (sub-context
    labels available) as the robustness upper-bound baseline; optionally one label-free group-inference probe. Pre-register
    the prediction that the unsupervised unit approaches the oracle group-DRO probe's worst-sub-context recall without using
    sub-context labels.
- id: ''
  category: scope
  severity: minor
  description: >-
    The effective-n fix is good but still slightly overstated. Two of the four 'genuinely independent' families — CEBaB food
    and CEBaB service — come from the SAME dataset and domain (restaurant reviews), and aspect-level sentiments in restaurant
    reviews are empirically positively correlated (a reviewer happy with food is often happy with service), so they are not
    fully decorrelated draws. The genuinely independent axes are closer to three (toxicity-family, sentiment, restaurant-aspect-cluster)
    than four, and a single adverse SAE draw on the shared restaurant-review encoding could move both CEBaB estimates together.
  suggested_action: >-
    Either treat the CEBaB food+service pair as one 'aspect-sentiment' family in the clustered CI (nesting them like the toxicity
    sub-attributes) and report their measured cross-aspect correlation, or add one more out-of-domain independent axis (e.g.,
    formality/politeness or spam) to genuinely reach four. Frame the aggregate as ~3 independent axes and report the within-CEBaB
    correlation explicitly.
- id: ''
  category: scope
  severity: minor
  description: >-
    The stated goal foregrounds three downstream tasks — classification, activation steering with side-effect measurement,
    AND model-diffing — but the design makes classification the headline, steering a single Tier-2 'confirmatory' case, and
    model-diffing a drop-first stretch. The depth-first MVP rationale is sound (and was endorsed last round), but as written
    the paper may under-deliver on two of the three tasks the goal explicitly requires, which a goal-aligned reviewer could
    penalize.
  suggested_action: >-
    Keep classification as the headline but commit that IF Tier 1 lands, the single steering case is executed decisively (matched
    on-target effect, KL on unrelated prompts + fluency, bootstrap CIs, engaging 2505.20063/AxBench) rather than illustratively,
    and add a minimal model-diffing null-floored check to the stretch tier so all three goal tasks are at least touched. State
    plainly that steering/model-diffing are demonstrations of generality, not load-bearing.
- id: ''
  category: rigor
  severity: minor
  description: >-
    The two headline regimes exercise different mechanisms under one 'mechanistic backbone' banner: first-letter is the clean
    ABSORPTION / signature-K / complementary-coverage case where absorber-recovery-vs-oracle is the test, whereas toxicity
    is mostly SPLITTING / signature-C where the subpopulation-reweighting recall story lives. The success criteria require
    the backbone on 'first-letter AND at least one safety concept,' but the subpopulation-reweighting prediction (the new
    a-priori mechanism) really only applies to the multi-sub-context splitting regime, not to first-letter. Bundling them
    risks a reader expecting the reweighting result on first-letter, where it does not apply.
  suggested_action: >-
    Explicitly map each headline test to its regime: absorber-recovery-vs-oracle + knowledge-graph-edge agreement = the first-letter
    (absorption) headline; worst-sub-context-recall-under-reweighting = the toxicity (splitting, multi-sub-context) headline.
    State that the two are complementary evidence for 'grouping helps,' not the same metric on both testbeds.
score: 6
confidence: 4
relation_type: evolution
relation_rationale: >-
  Same co-response-grouping frame; promotes backbone to headline + adds group-DRO robustness mechanism, CEBaB axes, tiers.
</previous_review_feedback><user_data>
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
  "$defs": {
    "TermDefinition": {
      "description": "A technical term and its definition.",
      "properties": {
        "term": {
          "description": "The technical term",
          "title": "Term",
          "type": "string"
        },
        "definition": {
          "description": "Clear definition of the term",
          "title": "Definition",
          "type": "string"
        }
      },
      "required": [
        "term",
        "definition"
      ],
      "title": "TermDefinition",
      "type": "object"
    }
  },
  "description": "A research hypothesis with validation approach.",
  "properties": {
    "title": {
      "description": "Concise, self-explanatory title",
      "title": "Title",
      "type": "string"
    },
    "hypothesis": {
      "description": "The core hypothesis statement",
      "title": "Hypothesis",
      "type": "string"
    },
    "motivation": {
      "description": "Why this hypothesis matters - significance and impact",
      "title": "Motivation",
      "type": "string"
    },
    "assumptions": {
      "description": "Key assumptions that must hold for this hypothesis (2-5 items)",
      "items": {
        "type": "string"
      },
      "title": "Assumptions",
      "type": "array"
    },
    "investigation_approach": {
      "description": "High-level approach to investigating this hypothesis",
      "title": "Investigation Approach",
      "type": "string"
    },
    "success_criteria": {
      "description": "What outcomes would confirm or disconfirm this hypothesis?",
      "title": "Success Criteria",
      "type": "string"
    },
    "related_works": {
      "description": "The most similar existing works found during research. Each entry describes one related work: what it does and how the proposed hypothesis fundamentally differs from it.",
      "items": {
        "type": "string"
      },
      "title": "Related Works",
      "type": "array"
    },
    "inspiration": {
      "description": "What inspired this hypothesis - which patterns, techniques, or cross-field insights were adapted (from the explicit inspiration seeds if your prompt included any, otherwise from your own cross-domain exploration)",
      "title": "Inspiration",
      "type": "string"
    },
    "terms": {
      "description": "Definitions of key technical terms used in the hypothesis",
      "items": {
        "$ref": "#/$defs/TermDefinition"
      },
      "title": "Terms",
      "type": "array"
    },
    "summary": {
      "description": "Brief summary of the hypothesis in 1-2 sentences",
      "title": "Summary",
      "type": "string"
    }
  },
  "required": [
    "title",
    "hypothesis",
    "motivation",
    "assumptions",
    "investigation_approach",
    "success_criteria",
    "related_works",
    "inspiration",
    "terms",
    "summary"
  ],
  "title": "Hypothesis",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-06-17 12:40:30 UTC

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

### [3] SKILL-INPUT — aii-web-tools · 2026-06-17 12:42:02 UTC

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
