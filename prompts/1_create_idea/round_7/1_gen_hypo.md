# gen_hypo_1 — create_idea

> Phase: `hypo_loop` · round 7 · `gen_hypo`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_hypo_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-17 13:12:52 UTC

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
  Recovering Absorbed SAE Features by Interventional Co-Response Grouping: Training-Free, Auditable Concept Units That Beat
  Raw Latents and the Observational Clusters, and Recover the Absorbers Marginal-Attribution Selection Drops (Sub-Population
  Robustness as a Supporting Second Result)
hypothesis: |-
  ONE-SENTENCE HEADLINE (load-bearing, C1+C3): clustering SAE latents by their INTERVENTIONAL co-response to content counterfactuals -- not by which latents fire together (co-activation) or point alike (decoder geometry) -- yields training-free, human-auditable, multi-member concept units that (C1) beat the best raw single latent AND observational co-activation/decoder-geometry clusters on safety-attribute classification, and (C3, the single most defensible deliverable) recover the absorber latents that a count-matched marginal-attribution selection silently drops, with knowledge-graph specialization edges that agree with the supervised absorption diagnostic (Chanin 2409.14507). SUPPORTING SECOND RESULT (deliberately NOT promised in the title): the SAME absorber-recovery, viewed under sub-population reweighting, keeps worst-sub-context recall stable where a count-matched marginal-attribution pool -- not merely a single dense hyperplane -- collapses, approaching an oracle group-DRO probe that uses sub-context labels while the unit uses none.

  MINIMUM VIABLE RESULT = THE LOAD-BEARING CORE (what the paper must show to stand, and what STILL stands even if every robustness comparison ties and aggregate F1 ties the dense probe): (i) the two-arm pilot confirms above-null co-response structure in at least one regime; (ii) C1 -- the unsupervised co-response unit beats the best raw single latent AND observational co-activation/decoder-geometry clustering on classification; (iii) C3 -- on the first-letter absorption testbed the unit recovers absorber latents that the supervised oracle's top-N marginal-attribution selection (g) and the count-matched pool (h) drop, wins specifically on the sub-contexts where they differ, and its knowledge-graph specialization edges agree with Chanin 2409.14507. C3 IS THE SPINE: it is measured against SAE-selection baselines (a)/(g)/(h), NOT against the brutal dense-probe aggregate-F1 bar, so the central empirical bet does NOT ride on out-classifying a strong dense probe (this is the deliberate de-risking of the AxBench-bar concern). All sub-population-shift robustness results are SUPPORTING evidence layered on this backbone; aggregate-F1 parity with the strong dense surface-invariant probe (f) is an explicitly acceptable, pre-registered outcome.

  BASELINE GLOSSARY (one plain-English line each, so the reader need not hold eleven in working memory): (a) best raw single latent = single-latent status quo; (b) observational co-activation / feature-family clusters = grouped by what fires together; (c) decoder-geometry clusters = grouped by decoder cosine; (d) counterfactually-matched diff-of-means = non-SAE direction from content-flip deltas; (e) counterfactually-matched linear probe = non-SAE probe on the same deltas; (f) surface-invariant matched probe = (d)/(e) with the surface direction LEACE-erased -- the conceded SINGLE dense hyperplane; (g) supervised oracle pool = top-N SAE latents by SCR/TPP causal attribution; (h) count-and-pool-matched probe = max-pool over EXACTLY #members raw residual directions chosen by the SAME SCR/TPP attribution as (g); (i) unmatched diff-of-means/probe on raw labels = naive non-counterfactual baseline; (j) oracle group-DRO probe = dense probe trained WITH true sub-context labels = robustness UPPER BOUND; (k) label-free group-inference probe = JTT/GEORGE-style infer-groups-over-EXAMPLES then retrain group-DRO, no sub-context labels.

  HEADLINE RESULT GRID (claim x baseline x metric x predicted sign x what it isolates; LOAD-BEARING rows first, SUPPORTING rows clearly marked):
  | Claim (role) | Compared against | Metric | Predicted sign | What it isolates |
  |---|---|---|---|---|
  | C1 (CORE) | (a) best raw latent; (b)/(c) observational clusters | classification F1/AUC, IID + shift | unit > both | co-response grouping beats single latent + observational grouping |
  | C3 first-letter ABSORBER-RECOVERY (CORE, the spine) | (g) oracle pool; (h) count-matched pool; diagnostic 2409.14507 | recovered-absorber count; recall on differing sub-contexts; KG-edge agreement | unit > (g)/(h); edges agree | co-response selection ADMITS the absorber marginal attribution DROPS |
  | C2 (core-adjacent) | (g) oracle pool; (h) count+pool-matched probe | classification F1/AUC | unit >= both | gain is not just supervised selection or pooling nonlinearity |
  | SELECTION-CRITERION ordering, toxicity (SUPPORTING) | (f) hyperplane; (g)/(h) marginal-attribution pools | worst-sub-context recall vs reweighting magnitude | (f) < (g)/(h) < unit; unit-(g)/(h) grows | co-response vs marginal-attribution SELECTION at matched pool size |
  | Robustness bounds, toxicity (SUPPORTING) | (j) oracle group-DRO (labels); (k) label-free group-inference | worst-sub-context recall | unit approaches (j) w/o labels; unit >= (k) AND auditable | training-free auditable route vs loss-reweighting route |
  | Dense-probe aggregate F1 (CONCEDED) | (f) surface-invariant probe | aggregate F1 | tie acceptable | concedes the AxBench bar honestly |

  THE SELECTION-CRITERION ISOLATION (RENAMED from the prior 'grouping-vs-pooling' label, which the reviewer correctly flagged as misleading). The unit-vs-(g)/(h) comparison holds POOL SIZE FIXED -- all three pool the same number of directions -- and varies ONLY HOW members are chosen: co-response membership (the unit's clustering IS the selection rule) vs marginal SCR/TPP attribution ranking ((g)/(h)). Both arms pool, so what is isolated is the SELECTION/MEMBERSHIP CRITERION, not 'grouping vs pooling' as a structural distinction. The structural claim therefore reduces to one plain sentence: CO-RESPONSE MEMBERSHIP ADMITS THE ABSORBER THAT MARGINAL-ATTRIBUTION RANKING DROPS. Beating the single hyperplane (f) is conceded to be a pooling/capacity effect -- the same group-DRO mechanism predicts ANY count-matched pool beats one hyperplane -- and is NOT evidence for co-response selection. The signal is exactly unit-minus-(g)/(h), which is mechanistically the SAME quantity as C3 absorber-recovery. Pre-registered ORDERING on worst-sub-context recall: (f) single hyperplane < (g)/(h) marginal-attribution pools < unit co-response pool, with unit-minus-(g)/(h) GROWING in reweighting magnitude. HONEST NEGATIVE: if the unit ties (g)/(h), the contribution reduces cleanly to C3 absorber-recovery + auditability -- which the load-bearing core already delivers -- and we report it plainly.

  THE TWO REGIME STORIES, KEPT SEPARATE (they are COMPLEMENTARY evidence for 'co-response selection helps', not the same metric on both testbeds).
  STORY 1 -- FIRST-LETTER = ABSORPTION (signature K, complementary coverage). 'starts-with-L' fragments into a general latent (silent on specific tokens) plus per-token absorbers ('lion'-absorber, 'London'-absorber). No member tracks the concept everywhere; the pooled max does. Headline test here = absorber recovery vs the oracle pool (g)/(h) (the unit admits absorbers the top-N marginal-attribution selection drops) PLUS knowledge-graph specialization-edge agreement with the supervised absorption diagnostic (Chanin 2409.14507). The sub-population-reweighting prediction does NOT live on this testbed.
  STORY 2 -- TOXICITY = SPLITTING (signature C, multi-sub-context). Toxicity manifests across sub-contexts (slurs vs threats vs demeaning insults), each carried by positively co-responding latents. Headline test here = worst-sub-context recall under sub-population reweighting (a SUPPORTING result). First-letter absorbers are also per-word specialists so the reweighting framing extends there in principle, but the PRE-REGISTERED reweighting test is on toxicity, where independent sub-context labels exist.

  DEGENERATE-CONSTRUCTION GUARD (the reweighting test is not true-by-construction). Sub-contexts are defined from INDEPENDENT labels fixed before any unit-vs-probe comparison: civil_comments sub-attribute floats (toxicity/obscene/insult/threat/identity_attack) and CEBaB aspect levels -- never from the unit's members. 'Under-served' sub-contexts are determined on the dense probe (f) ALONE, blind to the unit. The reweighting-magnitude axis is pre-registered. NON-TRIVIALITY CHECK: the dense probe genuinely collapses (recall drop above a pre-set threshold) on these independently-defined sub-contexts; if it does not, the reweighting test is void and reported as such.

  THE THREE NESTED CLAIMS (each with its own baseline, pre-registered for clean attribution). (A) 'Counterfactual supervision helps' (NOT ours): naive diff-of-means/probe (i) -> counterfactually-matched probe (d)/(e). Expected true; not claimed. (B) 'Counterfactual-INVARIANCE supervision helps' (conceded, non-SAE): matched probe -> surface-invariant matched probe (f) via LEACE / mean-projection erasure (Belrose 2024). (C) 'CO-RESPONSE GROUPING helps' (THE contribution): C1 -- unit beats best raw latent and observational clusters on classification; C2 -- unit matches-or-beats the supervised oracle pool (g) and the count-and-pool-matched probe (h); C3 -- the spine: low Jaccard with observational clusters AND wins on the differing members, recovering absorbers (g)/(h) drop with KG-edge agreement. C1 + C3 are the headline and hold regardless of whether the dense probe is beatable on aggregate F1.

  SINGLE ADMISSION RULE (one falsifiable procedure). Against a shuffled-pair null (permute which member of each minimal pair is content-on; B=1000), admit a candidate unit iff it clears at least one signature AND passes unit-level surface invariance. Signature C (splitting): mean within-unit content-response correlation > 95th pct of the null. Signature K (absorption): pooled max-over-members content-response AUC minus best-single-member AUC > 95th pct of a MATCHED best-of-random-k null -- the random k drawn from CONTENT-RESPONSIVE latents matched on marginal content-response AUC to the candidate members (isolates COMPLEMENTARY COVERAGE rather than mere content-responsiveness) -- AND members mutually exclusive in firing (mean pairwise co-activation Jaccard < 0.1), AND each member's content-response precision on its own firing support >= 0.7. SIGNATURE-K POWER AT SMALL k (resolves the prior minor): the matched best-of-random-k null is CONSERVATIVE at small member counts (max-over-2-or-3 already buys a pooling boost from the matched content-responsive draws), so for k in {2,3} we additionally require the observed effect size (pooled-minus-best-member AUC gain) to exceed a pre-set absolute floor (>= 0.05) with a bootstrap CI excluding 0 -- not merely to clear the null percentile -- and we report the matched-null spread (std of the gain across random matched draws) and the minimum coverage-gain detectable at k=2-3. Unit-level surface invariance: pooled surface-response not above the shuffled-surface-pair null. We report, per concept, which signature cleared and the false-admit rate under BOTH the all-latent and the matched random-k null (target <= 0.05).

  A-PRIORI POWER / MDE (resolves the central rigor critique; the now-load-bearing inferential object is a PER-PAIR gap, not two marginal CIs). PRIMARY statistical object = per-concept / within-family effect sizes with WITHIN-FAMILY paired bootstrap CIs. The cross-family number is DESCRIPTIVE ONLY: a bootstrap over ~3-4 family clusters cannot estimate between-cluster variance, so we state this explicitly and do NOT report it as an inferential population-level CI. For the central unit-minus-(g)/(h) worst-sub-context-recall gap we PRE-REGISTER a PAIRED bootstrap (B=10000) on the per-example correctness difference (unit_correct - pool_correct) on the under-served sub-context, with an EXACT McNemar test as confirmatory; the primary reported quantity is the gap's SIGN and its GROWTH -- the slope of the gap against measured reweighting magnitude, with a bootstrap CI on the slope. A-PRIORI MDE: treating recall as a proportion, the conservative (unpaired) per-arm size to detect a gap Delta at alpha=0.05 / power=0.80 is n ~= 7.84 * [p1(1-p1)+p2(1-p2)] / Delta^2 -> ~91 positives for Delta=0.20 (0.50->0.70), ~167 for Delta=0.15, ~384 for Delta=0.10; the paired design is strictly MORE powerful because absorption makes the discordance asymmetric (the pool has a recall 'hole' the unit fills), so these are upper bounds. We therefore PRE-REGISTER n_min = 150 positive examples per under-served sub-context TESTED (powers Delta >= 0.15 unpaired, more when paired) and STRATIFY pair collection to hit n_min on each tested sub-context rather than sampling uniformly; any sub-context too rare to reach n_min (e.g., civil_comments threat / identity_attack at base rate) is reported DESCRIPTIVELY and EXCLUDED from the inferential reweighting test, with the exclusion stated. The >=800-pair-per-family budget is re-allocated accordingly: >= 150 positive + >= 150 negative per tested under-served sub-context, plus a matched IID slice.

  ENGAGING THE LABEL-FREE GROUP-ROBUSTNESS LITERATURE (the established competitors for the SUPPORTING result). Promoting the reweighting result makes the competitors the label-free worst-group-robustness methods -- JTT (2107.09044), GEORGE (2011.12945), EIIL (2010.07249), LfF (2007.02561), Diverse Prototypical Ensembles (2505.23027). They achieve worst-group robustness by inferring groups over EXAMPLES and RETRAINING with reweighted / group-DRO loss (or training a diverse prototype ensemble). Our route is DIFFERENT: we group FEATURES (discrete SAE latents) by interventional co-response, never retrain, and the recovered absorbers ARE the inferred sub-context specialists. Baselines (j) oracle group-DRO (true sub-context labels = upper bound) and (k) label-free group-inference (JTT/GEORGE-style, no labels, like our unit). Pre-registered prediction: the unit APPROACHES (j) WITHOUT labels and is competitive-or-better than (k) while uniquely auditable; if (k) strictly beats the unit on recall, that is an honest negative (loss-reweighting wins for pure robustness, but the unit still delivers the auditable feature-level repair).

  AUDITABILITY -- THE CONCRETE DIFFERENTIATOR OVER (k) (resolves the contribution critique by stating what auditability buys when robustness ties). When loss-reweighting (k) wins on raw recall, the unit still delivers something (k) structurally cannot: a READABLE REPAIR. Worked case: the 'starts-with-L' unit's members = {general 'starts-with-L' latent (silent on 'lion'/'London'), 'lion'-absorber, 'London'-absorber}; a practitioner reading the knowledge graph sees exactly WHICH sub-context each member covers, can ADD a missing absorber to fix a steering hole, and can cite the specialization edge -- none of which a retrained reweighted dense probe (k) exposes. Auditability + absorber-recovery is the standalone deliverable when every robustness comparison ties.

  HEADLINE SCOPE with honest effective-n (the aggregate is DESCRIPTIVE, per-family CIs are PRIMARY). The headline spans ~3 GENUINELY INDEPENDENT concept families: (1) TOXICITY (civil_comments / ParaDetox), 5 sub-attributes reported as WITHIN-family detail and the best-powered family (so the load-bearing reweighting test runs here first); (2) SENTIMENT (Kaushik 2020 human counterfactual IMDB); (3) RESTAURANT ASPECT-SENTIMENT (CEBaB), food and service NESTED as ONE family (shared domain, positively correlated; cross-aspect correlation reported). A 4th out-of-domain axis (formality via GYAFC, or spam) is a drop-first stretch to reach four clusters. We report per-family bootstrap CIs as the PRIMARY evidence and the cross-family number as DESCRIPTIVE. first-letter spelling = the controlled ABSORPTION mechanism testbed (outside the family count); bias_in_bios = a pre-registered BOUNDARY-NULL. A clean null at any stage is a publishable mechanism-level finding.
motivation: |-
  Single SAE latents are unreliable units of analysis. Feature absorption (a specific child latent suppresses a more general parent's firing, leaving the parent with unpredictable holes; Chanin 2409.14507 [NeurIPS 2025], 2505.11756), feature splitting (one concept fragments across many latents), feature hedging (a narrow SAE merges correlated features into one polysemantic latent), and 'SAEs Do Not Find Canonical Units of Analysis' (ICLR 2025, 2502.04878) all converge on the same conclusion: no single latent reliably tracks a concept. AxBench (ICML 2025 spotlight, 2501.17148) and DeepMind's negative-results report make the stakes concrete -- plain difference-of-means beats raw-latent SAE methods on concept detection and steering -- so any SAE-grouping method must clear strong simple baselines.

  WHY THE LOAD-BEARING CLAIM IS C1+C3, NOT THE ROBUSTNESS STORY. The single most defensible deliverable is absorber recovery (C3): on the first-letter testbed the co-response unit admits the absorber latents that the supervised oracle's top-N marginal-attribution selection (g) and the count-matched pool (h) drop, and its knowledge-graph specialization edges agree with the supervised absorption diagnostic (Chanin 2409.14507). C3 is measured against SAE-SELECTION baselines, not against the brutal dense-probe aggregate-F1 bar; this is the deliberate de-risking of the central empirical bet flagged by the reviewer -- the paper's spine does not depend on out-classifying a strong dense probe. Robustness under sub-population reweighting is a SUPPORTING second result that re-uses the SAME absorber-recovery quantity.

  The contribution lives squarely in clustering / feature-selection / classification for a learned knowledge representation (SAE features): we produce cluster-level units and a feature-level knowledge graph, evaluated on downstream classification (headline) with steering and model-diffing as generality demonstrations. Every existing POST-HOC grouping method relies on OBSERVATIONAL signals -- which latents fire together (co-activation feature families) or which decoders point alike (geometry). But absorption is exactly the regime where observational signals break by construction: per Chanin, the parent and the absorbing child are hierarchical and the child fires only where the parent goes silent, so the two are MUTUALLY EXCLUSIVE in firing -- co-activation clustering provably cannot group them and their decoders need not be cosine-similar. This is a structural blind spot, not a tuning problem. The standard SUPERVISED remedy -- select the top-N latents by causal effect on a concept probe (SCR/TPP, Karvonen 2411.18895, built on Marks SHIFT) -- SILENTLY DROPS absorbed latents, because a latent that fires only in a narrow sub-context has low MARGINAL attribution even though it carries the concept there.

  RECENT ARCHITECTURAL REMEDIES ARE ORTHOGONAL (and confirm the gap). Subspace-Aware SAEs (SASA, 2606.06333), Matryoshka SAEs, Concept-Bottleneck SAEs (CVPR 2026), and Group SAEs (negative results) all RETRAIN the SAE -- new decoder subspaces, nested dictionaries, bottlenecks, or grouping losses -- to reduce splitting/absorption at training time. We do the opposite: a TRAINING-FREE, POST-HOC repair of FROZEN public SAEs (Gemma Scope), exactly as the goal requires ('must run on open-source pretrained SAEs'). No retraining method produces a human-auditable multi-member unit over an existing public SAE, which is what practitioners actually have.

  TWO cross-field transfers motivate the method and its supporting robustness mechanism. (1) Systems biology faced the identical grouping obstacle: co-regulated genes are often NOT co-expressed at baseline and reveal shared regulation only under perturbation, which is why differential co-expression methods (DiffCoEx, WGCNA) cluster genes by their CORRELATED RESPONSE TO A PERTURBATION rather than baseline co-expression. Mapping genes->SAE latents and a chemical/genetic perturbation->an input content counterfactual gives the grouping mechanism. (2) Distributionally-robust learning explains WHY the recovered unit should generalize under sub-population shift: an absorber is a dedicated detector for one sub-context, so a complementary-coverage unit is implicitly a GROUP-OF-SPECIALISTS robust to mixing-weight shift where a single ERM hyperplane collapses (group-DRO; Mind-the-GAP 2403.09869). Crucially, the SAME mechanism predicts a count-matched POOL of marginal-attribution-selected directions is ALSO robust -- so beating one hyperplane is a pooling effect; what isolates CO-RESPONSE SELECTION is beating the count-matched marginal-attribution pool, which drops the very absorber the under-served sub-context needs.

  This places the supporting robustness result alongside the label-free worst-group-robustness literature (JTT, GEORGE, EIIL, LfF, Diverse Prototypical Ensembles), which infer groups over EXAMPLES and RETRAIN. Our route is orthogonal and complementary: we group FEATURES on a frozen public SAE, never retrain, and the recovered absorbers are themselves the inferred sub-context specialists -- auditable (you can read which absorber covers which sub-context, as a knowledge graph), reusable for steering and model-diffing, benchmarkable against an oracle group-DRO probe that DOES use sub-context labels. The insight an interpretability expert would not reach for: SAE absorption/splitting are structurally the same obstacle that (a) defeats baseline co-expression in biology and (b) makes ERM probes brittle under subpopulation shift -- so observational co-activation/geometry AND marginal-attribution selection are the wrong instruments, interventional co-response is the matched instrument, and the recovered absorbers ARE the latent subpopulations a robust classifier needs.

  If correct, this gives a training-free, single-GPU, human-auditable way to turn off-the-shelf public SAEs into reliable concept units -- with a measurable recall recovery on absorbed sub-contexts, an auditable specialization graph, and a supporting robustness story that approaches an oracle group-DRO probe without labels. If incorrect, the honest negatives are themselves actionable: that observational co-response equals interventional co-response (no gain from intervention); that co-response selection ties the count-matched marginal-attribution pool (robustness is pooling, contribution reduces to absorber-recovery + auditability); that the label-free group-inference probe beats the unit on recall (loss-reweighting wins for pure robustness); or that SAE units should be abandoned in favor of dense surface-invariant probes for robust classification.
assumptions:
- >-
  MINIMAL PAIRS ARE OBTAINABLE AT HIGH QUALITY, LOW COST, AND NON-CIRCULARLY. Primary content-flips use HUMAN-WRITTEN parallel
  corpora needing no LLM generation: ParaDetox (s-nlp, ACL 2022) toxic<->neutral for toxicity, Kaushik 2020 (ICLR) crowd-revised
  IMDB minimal pairs for sentiment, CEBaB (Abraham 2022) human aspect-edited restaurant reviews for the restaurant aspect-sentiment
  family. For rare toxicity sub-attributes (threat, identity_attack) and first-letter substitutions, LLM-generated pairs (OpenRouter,
  well under $10) are each LLM-judge-scored for content-flipped + surface-preserved, with reported pass rates and sensitivity
  to the pair-quality threshold. Any activation-space content edit, if used, is derived from an INDEPENDENT held-out diff-of-means
  on DISJOINT data, never from the SAE latents being grouped, so there is no circularity.
- >-
  THE CENTRAL CONTRAST IS A-PRIORI POWERED AND TESTED AS A PER-PAIR GAP, NOT TWO MARGINAL CIs. The now-load-bearing inferential
  object is the unit-minus-(g)/(h) worst-sub-context recall gap, tested by a PAIRED bootstrap (B=10000) on per-example correctness
  differences plus an exact McNemar test, with the gap's sign and its slope-vs-reweighting-magnitude as the primary reported
  quantities. We pre-register n_min = 150 positive examples per tested under-served sub-context (conservative-unpaired MDE
  for Delta >= 0.15 at alpha=0.05 / power=0.80; n ~= 7.84*[p1(1-p1)+p2(1-p2)]/Delta^2) and STRATIFY pair collection to reach
  n_min; sub-contexts too rare to reach it (e.g., threat/identity_attack at base rate) are reported descriptively and excluded
  from the inferential test. Per-family CIs are PRIMARY; the cross-family aggregate over ~3-4 clusters is DESCRIPTIVE only
  (between-cluster variance is not estimable with so few clusters) and is reported as such.
- >-
  THE WIN, IF IT OCCURS, IS ATTRIBUTABLE TO CO-RESPONSE SELECTION AT MATCHED POOL SIZE -- NOT TO SUPERVISION, CAPACITY, OR
  MERE POOLING. The conceded dense baseline (f, surface-invariant matched probe) is information-matched via LEACE/mean-projection
  erasure. The supervised oracle pool (g, SCR/TPP top-N latents) controls for label selection. The count-and-pool-matched
  probe (h, max-pool over EXACTLY #members raw directions selected by the SAME SCR/TPP attribution) controls member-count
  AND pooling nonlinearity, holding pool SIZE fixed so the ONLY varying factor is the membership/SELECTION criterion (co-response
  vs marginal attribution). The pre-registered ORDERING (f) < (g)/(h) < unit on worst-sub-context recall isolates selection:
  beating (f) is conceded as a pooling effect; beating (g)/(h) is the signal and equals C3 absorber-recovery. The structural
  claim reduces to: co-response membership admits the absorber marginal-attribution ranking drops.
- >-
  THE ROBUSTNESS GAP (SUPPORTING) IS DRIVEN BY SUB-POPULATION REWEIGHTING, IS NOT TRUE-BY-CONSTRUCTION, AND IS BENCHMARKED
  AGAINST THE LABEL-FREE GROUP-ROBUSTNESS LITERATURE. Sub-contexts are defined from INDEPENDENT labels (civil_comments sub-attribute
  floats; CEBaB aspect levels) frozen before any comparison; 'under-served' is determined on the dense probe (f) alone; the
  reweighting-magnitude axis is pre-registered; a non-triviality check confirms (f) genuinely collapses on those independently-defined
  sub-contexts. We decompose the shift into (i) surface-only paraphrase (unit NOT predicted to win), (ii) sub-population reweighting
  (unit predicted to win on worst-sub-context recall, growing with magnitude), (iii) natural domain shift (drop-first). We
  benchmark against an oracle group-DRO probe (j, uses sub-context labels = upper bound) and a label-free group-inference
  probe (k, JTT/GEORGE-style, no labels); the unit is predicted to approach (j) without labels and be competitive-or-better
  than (k) while uniquely auditable. If the gap does not concentrate on (ii), or the unit ties (g)/(h) on the slice, the supporting
  mechanism is falsified and reported -- the load-bearing C1+C3 core is unaffected.
- >-
  Off-the-shelf Gemma Scope SAEs on Gemma-2-2b expose latent counterfactual responses measurable above noise on a SINGLE GPU
  within the budget for a few thousand minimal pairs per concept, and the chosen attributes have enough labeled/templatable
  data (civil_comments sub-attribute floats, CAD-IMDB, CEBaB aspect labels, ParaDetox) to build minimal pairs and natural-shift
  test splits. Absorption is more severe at WIDER SAEs and splitting at larger width, so SAE width/layer is a robustness axis
  (16k canonical primary; 65k is a drop-first stress point). For the model-diffing demonstration, paired base (gemma-scope-2b-pt)
  and instruction-tuned (gemma-scope-2b-it) SAEs are available off the shelf. The whole load-bearing core fits a hard per-tier
  GPU-hour budget (below).
investigation_approach: |-
  DEPTH-FIRST EXECUTION ORDER WITH HARD PER-TIER BUDGETS AND A PRE-REGISTERED DROP ORDER (resolves the execution-complexity critique). Single GPU; executor wall-clock ~6 h. The run is triaged so a clean LOAD-BEARING CORE is always produced.

  TIER 0 -- TWO-ARM DE-RISKING PILOT (<= 1.0 GPU-h, NEVER dropped). ARM A (absorption, first-letter): find the general first-letter latent and its absorbers; build content-flip pairs; measure (a) correlated content-response (expected low/disjoint) and (b) COMPLEMENTARY coverage (pooled max tracks the flip where members have holes) vs the shuffled-pair null. ARM B (splitting, toxicity): on ParaDetox/civil_comments, measure how many latents carry toxicity, whether their content-response profiles are positively correlated above null, and whether the pooled unit beats the single best toxicity latent and the matched diff-of-means on a held-out IID slice. Symmetric decision rules; proceed with a regime as headline only if its pilot clears the null (a pilot null is itself a reported mechanism finding).

  TIER 1a -- LOAD-BEARING CORE (<= 2.5 GPU-h, NEVER dropped; this alone makes a publishable paper). (1) C1: the co-response unit beats the best raw latent (a) and observational co-activation/geometry clusters (b)/(c) on classification, on first-letter (absorption) AND the single best-powered toxicity family. (2) C3 (the spine): on first-letter, recovered-absorber count vs the oracle pool (g) and count-matched pool (h); sliced recall on the differing sub-contexts; KG specialization-edge agreement with Chanin 2409.14507. (3) The SELECTION-CRITERION ordering (f) < (g)/(h) < unit on worst-sub-context recall on the best-powered toxicity family, with the PAIRED-bootstrap per-pair gap and its slope-vs-reweighting as the primary inferential object. (4) The degenerate-construction guard and non-triviality check on (f). HARD CHECKPOINT at end of Tier 1a: if the core has not cleared, STOP expanding and write up the core + honest negatives.

  ALWAYS-RUN MINIMAL GENERALITY DEMOS (<= 0.5 GPU-h, NEVER dropped; resolves the all-three-tasks critique via a truncation fallback). Even if the run stops at Tier 1, produce ONE null-floored STEERING result (toxicity unit direction vs best single latent vs matched diff-of-means: on-target effect + KL on unrelated prompts, above a shuffle null) AND ONE null-floored MODEL-DIFFING result (does the unit detect a base-vs-it concept-usage shift more reliably than the best single latent, above a shuffle null, using paired pt/it Gemma Scope SAEs?). Both are stated in the paper as GENERALITY DEMONSTRATIONS, not load-bearing.

  TIER 1b -- SUPPORTING (<= 1.5 GPU-h, demotable). Sentiment (CAD-IMDB) family; shift-decomposition conditions (i) surface-only + (ii) reweighting; the label-free group-inference probe (k) and oracle group-DRO probe (j); cluster-stability bootstraps (adjusted Rand / Jaccard vs null); per-family CIs.

  TIER 2 -- STRETCH (only if Tier 1a+1b land with budget left). CEBaB restaurant aspect-sentiment family; ONE DECISIVELY-executed steering case (matched on-target effect, KL on unrelated prompts + fluency, bootstrap CIs, engaging 2505.20063/AxBench); shift condition (iii) natural domain shift; a fuller model-diffing check.

  PRE-REGISTERED DROP ORDER UNDER TIME PRESSURE (first dropped first): 4th out-of-domain axis -> CEBaB family -> shift condition (iii) natural -> oracle/label-free probes (j)/(k) -> sentiment family -> decisive Tier-2 steering (keep the minimal one) -> fuller model-diffing (keep the minimal one). NEVER dropped: Tier 0 pilot, Tier 1a core, the two minimal generality demos.

  COUNTERFACTUAL SIGNAL. Encode every text and its counterfactual with a frozen Gemma Scope residual-stream SAE (layer ~12, width 16k canonical). Per latent: content-response = delta(activation) under content-flip; surface-response = delta under surface-flip. Aggregate into per-latent response profiles across contexts.

  CLUSTERING METHOD (the in-scope contribution). Build a latent-by-context content-response matrix. Cluster latents with a differential-correlation affinity (DiffCoEx-style) for signature C and a coverage-complementarity term for signature K, via agglomerative clustering / graph community detection on the affinity. Finalize each candidate unit with the SINGLE ADMISSION RULE (signature C OR matched-null signature K + small-k effect-size floor + mutual-exclusivity + precision floor, AND unit-level surface invariance); report the cleared signature per concept and the false-admit rate under both nulls. Emit human-auditable unit definitions (member latents, logit-lens tokens, conditioning contexts) and directed specialization edges (a member responsive only in a sub-context = absorbed/split child) = a feature-level knowledge graph.

  WORKED EXAMPLES. Toxicity unit (splitting): members = {profanity/slur latent, demeaning-insult latent, aggressive-imperative latent}; under ParaDetox detox all three drop together (signature C); pooled max tracks toxicity; pooled surface-response to paraphrase ~ 0. First-letter unit (absorption): members = {general 'starts-with-L' latent (silent on 'lion'/'London'), 'lion'-absorber, 'London'-absorber}; no member tracks 'starts-with-L' everywhere, pooled max does (signature K); members never co-fire (Jaccard ~ 0); pooled surface-response ~ 0.

  BASELINES (matched baselines are primary). (a) best raw single latent; (b) observational co-activation clustering / feature families; (c) decoder-geometry clustering; (d) counterfactually-matched diff-of-means; (e) counterfactually-matched linear probe; (f) surface-invariant matched probe = (d)/(e) with the surface-flip direction LEACE/mean-projection erased (Belrose 2024) -- the conceded SINGLE-HYPERPLANE non-SAE baseline; (g) supervised oracle pool = top-N latents by SCR/TPP probe-attribution (Karvonen 2411.18895 / Marks SHIFT); (h) count-and-pool-matched probe = max-pool over EXACTLY #members raw residual directions selected by the SAME SCR/TPP attribution as (g); (i) unmatched diff-of-means / linear probe on raw labels; (j) ORACLE GROUP-DRO dense probe WITH true sub-context labels = upper bound; (k) LABEL-FREE GROUP-INFERENCE dense probe (JTT/GEORGE-style).

  EVAL -- LOAD-BEARING BACKBONE (reported regardless of dense-probe competitiveness): (1) co-response units have low Jaccard with co-activation/geometry clusters above the stability/shuffled-pair null; (2) units win specifically on the differing members -- sliced RECALL on the sub-contexts where the best latent / observational clusters / the oracle pool (g) / the count-matched pool (h) have holes, including absorbers (g)/(h) drop; (3) knowledge-graph specialization edges agree with the supervised absorption diagnostic (2409.14507) on first-letter. EVAL -- CLASSIFICATION + SUPPORTING ROBUSTNESS: unit-pooled activation (max/sum over members) as classifier on IID and under the decomposed shifts; report F1/AUC AND worst-sub-context recall. The SELECTION-CRITERION prediction is the ORDERING (f) < (g)/(h) < unit on worst-sub-context recall with the unit-minus-(g)/(h) PAIRED gap GROWING in reweighting magnitude (slope CI as primary object). Robustness BOUNDS: unit approaches (j) without labels and is competitive-or-better than (k) while auditable. Aggregate F1 vs (f) reported honestly (tie acceptable). DEGENERATE-CONSTRUCTION GUARD applied throughout. STATISTICS: per-family paired-bootstrap CIs PRIMARY; cross-family aggregate DESCRIPTIVE; a-priori n_min=150 with stratified collection; cluster-stability bootstrap (adjusted Rand / Jaccard) vs shuffled-pair null.

  STEERING (Tier 2, ONE decisive case; a minimal version always runs). Steer with the toxicity unit's shared content-response direction vs best single latent vs the matched surface-invariant diff-of-means; measure on-target effect and side-effects (KL on unrelated prompts, fluency) at MATCHED on-target effect with bootstrap CIs; engage 'SAEs Are Good for Steering -- If You Select the Right Features' (2505.20063) and the AxBench protocol.

  MODEL-DIFFING (minimal version always runs; fuller version Tier 2). Using paired Gemma Scope pt/it SAEs, test whether the co-response unit detects a base-vs-instruction-tuned shift in concept usage more reliably than the best single latent, above a shuffle null. Touches the third goal task without being load-bearing.

  HONEST FAILURE-MODE REPORTING. Dependence on counterfactual quality (pass rates); concepts with no surface-invariant co-responding/complementary group; regimes where co-response collapses to co-activation (no gain over observational); the unit tying the count-matched pools (g)/(h) on sliced recall (robustness is pooling -> contribution reduces to absorber-recovery + auditability); the label-free group-inference probe (k) beating the unit on recall (loss-reweighting wins for pure robustness); the dense surface-invariant probe matching the unit on sliced recall (invariance supervision suffices, grouping adds only auditability); the oracle pool (g) tying the unit (selection not co-response structure); the reweighting test void because (f) does not collapse on independently-defined sub-contexts; co-response too noisy to cluster (ARI ~ null); a pilot arm showing neither correlated nor complementary above-null structure; compute/SAE-width sensitivity; bias_in_bios boundary-null.
success_criteria: |-
  CONFIRMED if, pre-registered in this nesting (LOAD-BEARING CORE first):
  LOAD-BEARING (the paper stands on these alone, even if every robustness comparison ties and aggregate F1 ties the dense probe): (1) the two-arm STEP-0 pilot confirms above-null structure in at least one regime (positively-correlated content-response for splitting and/or complementary coverage for absorption), with the toxicity arm also showing a pooled IID edge over the best single latent and the matched diff-of-means; (2) C1 -- the unit beats the best raw single latent and observational co-activation/geometry clustering on classification on first-letter AND the best-powered toxicity family (per-family bootstrap CI excludes 0); (3) C3 (the spine) -- on first-letter the unit recovers absorber latents that the oracle pool (g) and count-matched pool (h) drop, wins on the differing sub-contexts (paired-bootstrap gap CI excludes 0, sized to n_min=150), and its KG specialization edges agree with the supervised absorption diagnostic (2409.14507).
  SUPPORTING (strengthen the paper; honest nulls here do not sink it): (4) C2 + SELECTION-CRITERION ISOLATION -- the unit matches-or-beats (g) and (h) on classification AND shows the pre-registered ORDERING (f) < (g)/(h) < unit on worst-sub-context recall, with a POSITIVE unit-minus-(g)/(h) PAIRED gap whose slope-vs-reweighting-magnitude CI excludes 0 (the unit-minus-(f) gap alone is conceded as a pooling effect); (5) ROBUSTNESS BOUNDS -- the unit APPROACHES the oracle group-DRO probe (j) WITHOUT sub-context labels and is competitive-or-better than the label-free group-inference probe (k) while uniquely auditable; aggregate F1 vs (f) may tie; (6) ADMISSION + CONSTRUCTION INTEGRITY -- false-admit rate <= 0.05 under BOTH nulls (with the small-k effect-size floor for signature K); cluster assignments stable across bootstrap resamples (adjusted Rand/Jaccard above null); sub-contexts defined from independent labels frozen first, under-served determined on (f) alone, non-triviality check confirms (f) genuinely collapses; per-family CIs reported as PRIMARY and the cross-family aggregate as DESCRIPTIVE only.
  GENERALITY (always produced via the truncation fallback, never load-bearing): one null-floored steering result and one null-floored model-diffing result; the decisive Tier-2 steering case (lower KL side-effects than best-single-latent and matched diff-of-means at matched on-target effect) is confirmatory if it lands.
  HONEST NEGATIVES, each publishable: co-response grouping ties observational grouping (no gain from intervention); the unit ties (g)/(h) on sliced recall (robustness is pooling -> contribution reduces to absorber-recovery + auditability); (k) beats the unit on recall (loss-reweighting wins for pure robustness, unit still delivers auditable repair); the dense surface-invariant probe matches the unit on sliced recall (grouping then contributes only auditability + the knowledge graph); the oracle pool (g) ties the unit (selection not co-response structure); the gap does NOT concentrate on the reweighting component, or (f) does not collapse on independently-defined sub-contexts (supporting mechanism falsified/void, core unaffected); co-response too noisy to cluster (ARI ~ null); a pilot arm shows neither correlated nor complementary above-null structure. bias_in_bios is a pre-registered boundary-null, not method failure.
related_works:
- >-
  AxBench: Steering LLMs? Even Simple Baselines Outperform Sparse Autoencoders (Wu et al., ICML 2025 spotlight, 2501.17148):
  on Gemma-2-2B/9B, difference-in-means is the strongest concept-detection method and SAEs are not competitive. This sets
  the dense-probe bar. We deliberately do NOT stake the load-bearing claim on beating it: C3 absorber-recovery is measured
  against SAE-SELECTION baselines (a)/(g)/(h), and aggregate-F1 parity with the surface-invariant dense probe (f) is pre-registered
  as acceptable.
- >-
  Negative Results for Sparse Autoencoders on Downstream Tasks (DeepMind, 2025): reports SAEs are not competitive with baselines
  on downstream tasks and de-prioritises SAE research. We treat this as the bar to clear specifically for the SUPPORTING classification/robustness
  story, while the load-bearing contribution (auditable absorber-recovery + KG edges vs SCR/TPP selection) is a different,
  more favorable comparison the report does not address.
- >-
  Sparse Autoencoders Do Not Find Canonical Units of Analysis (Bussmann et al., ICLR 2025, 2502.04878): uses SAE stitching
  and meta-SAEs to argue SAEs do not learn canonical units; its remedy is geometric/training-based. We propose a BEHAVIORAL
  unit defined by counterfactual co-response and unit-level surface invariance, evaluated on downstream classification + steering
  + model-diffing, with no retraining.
- >-
  Subspace-Aware Sparse Autoencoders (SASA, Dalili & Mahdavi, 2606.06333, 2026): RETRAINS the SAE with learned decoder SUBSPACES,
  block sparsity, and a nuclear-norm rank regularizer to provably reduce feature splitting and absorption on GPT-2/Mistral-7B.
  It is a TRAINING-TIME architectural remedy; we are POST-HOC and TRAINING-FREE over frozen public SAEs (Gemma Scope), produce
  human-auditable multi-member units, and never modify the SAE -- the regime practitioners with off-the-shelf SAEs actually
  face.
- >-
  Matryoshka SAEs and Concept-Bottleneck SAEs (CVPR 2026); Group SAEs (negative results, LessWrong 2025): all modify SAE TRAINING
  -- nested dictionaries, concept bottlenecks, or a same-group penalty in the loss -- to reduce absorption/splitting. Group
  SAEs report negative results for training-time grouping. Our grouping is POST-HOC over a FROZEN public SAE's discrete latents,
  defined by interventional co-response, requiring no retraining and yielding an auditable feature-level knowledge graph.
- >-
  Feature Hedging: Correlated Features Break Narrow SAEs (Chanin, Dulka, Garriga-Alonso, 2505.11756): ABSORPTION learns gerrymandered
  latents (worse at WIDER SAEs, parent->child hierarchy, mutually-exclusive firing) vs HEDGING merges correlated features
  into a SINGLE polysemantic latent (worse at NARROWER SAEs). We scope grouping to splitting+absorption (a hedged single latent
  is not groupable) and treat correlation/hierarchy as the mechanistic cause our interventional probe exposes.
- >-
  A is for Absorption (Chanin et al., 2409.14507, NeurIPS 2025): a SUPERVISED DIAGNOSTIC -- identify the first-letter latent
  by max encoder-cosine with an LR probe, use ablation on the correct-minus-incorrect-letter logit to find the absorbing latent.
  It DETECTS absorption on individual latents; it does not GROUP parent+absorbers into a usable unit. We use it as a partial
  ORACLE for the pilot and to validate knowledge-graph edges; our contribution is the unsupervised grouping/repair.
- >-
  Counterfactual Invariance to Spurious Correlations (Veitch, D'Amour, Yadlowsky, Eisenstein, NeurIPS 2021, 2106.00545): an
  MMD-based regularizer enforcing the counterfactual-invariance signature (conditional MMD in the anti-causal direction).
  We import this as a DROP-FIRST alternative construction of the surface-invariant baseline (f); the primary construction
  is LEACE/mean-projection erasure.
- >-
  LEACE: Perfect linear concept erasure in closed form (Belrose et al., 2306.03819): we erase the surface-flip direction to
  build the surface-invariant probe (f) -- a strong, principled non-SAE single hyperplane. Per the reviewer, beating one hyperplane
  is treated as a pooling effect; selection is isolated against the count-matched pools (g)/(h).
- >-
  SHIFT / SCR / TPP SAE evaluation (Marks et al. 2024; Karvonen et al. 2411.18895): SELECT individual SAE latents by ranking
  causal effect on a concept probe (top-N), then ablate the set; they do NOT cluster latents by interventional co-response.
  This is exactly our supervised ORACLE-POOL baseline (g) and, count-matched, the pool (h); a latent firing only in a narrow
  sub-context (an absorber) has low marginal attribution and is silently dropped -- the specific gap our co-response selection
  fills, and the quantity the unit-minus-(g)/(h) sliced-recall gap measures.
- >-
  Just Train Twice (JTT, 2107.09044), GEORGE / No Subclass Left Behind (2011.12945), EIIL (2010.07249), Learning from Failure
  (LfF, 2007.02561): the label-free worst-group-robustness family. They infer GROUPS OVER EXAMPLES (high-loss upweighting,
  feature-space clustering of data points, environment inference) and RETRAIN with reweighted / group-DRO loss. Our route
  is orthogonal: we group FEATURES (discrete SAE latents) by interventional co-response, never retrain, and the recovered
  absorbers ARE the inferred sub-context specialists -- auditable. We add an oracle group-DRO probe (j, uses sub-context labels
  = upper bound) and a label-free group-inference probe (k) as direct robustness baselines for the SUPPORTING result.
- >-
  Diverse Prototypical Ensembles (2505.23027): trains an ensemble of N diverse prototypes per class on FROZEN DENSE features
  with an inter-prototype-similarity diversity loss + bagging to capture subpopulation-specific patterns without group labels.
  Conceptually the closest 'ensemble-of-specialists for subpopulation shift', but it TRAINS learnable prototype vectors on
  dense representations; we group pre-existing DISCRETE SAE latents by interventional co-response with no training, yielding
  auditable concept atoms (not opaque prototypes) and a feature-level knowledge graph.
- >-
  Group Distributionally Robust Optimization and subpopulation-shift robustness (Sagawa et al. group-DRO; Mind the GAP: Group-Aware
  Priors, 2403.09869): a single ERM model collapses on under-served minority subgroups under mixing-weight shift; group-aware
  methods recover worst-group performance. We do NOT propose a new DRO method or theorem; we BORROW this as the a-priori mechanism
  explaining why a group-of-specialists unit out-generalizes a single hyperplane -- and use the SAME mechanism to predict
  a count-matched marginal-attribution pool is also robust, which is why selection is isolated against THAT pool, not the
  hyperplane.
- >-
  Discovering Concept Directions from Diffusion-based Counterfactuals via Latent Clustering (CDLC, 2505.07073; Pattern Recognition
  Letters 2025): clusters latent DIFFERENCE vectors from factual + diffusion-generated counterfactual IMAGE pairs into global
  class-specific concept DIRECTIONS (skin-lesion data). Closest 'cluster counterfactual differences' template, but on a different
  substrate: one continuous direction per class in a diffusion latent space, in vision. We cluster DISCRETE SAE dictionary
  latents on a frozen LLM by their co-response PROFILES into auditable MULTI-MEMBER units, add unit-level surface invariance,
  and target the ABSORPTION regime via complementary coverage.
- >-
  Causal-differentiating / counterfactual concept-representation methods for LMs (CausaLM, Feder et al. 2020; Causal Differentiating
  Concepts): learn or adversarially fine-tune a counterfactual concept REPRESENTATION / direction. These produce a learned
  concept direction or concept-invariant model, not a clustering of pre-existing discrete SAE latents; they do not address
  SAE absorption/splitting or build a multi-member auditable unit. We are training-free over frozen public SAEs and our object
  is the discrete-latent GROUP.
- >-
  Counterfactually-Augmented Data (Kaushik, Hovy, Lipton, ICLR 2020) and CEBaB (Abraham et al., NeurIPS 2022, 2205.14140):
  human-written counterfactual minimal pairs for sentiment (IMDB) and ASPECT concepts (food/service/ambiance/noise), with
  out-of-domain sources. We use CAD as one independent axis and CEBaB as ONE restaurant aspect-sentiment family (food+service
  nested, cross-aspect correlation reported); these supply non-circular pairs and independent sub-context labels for the degenerate-construction
  guard, not the grouping method.
- >-
  Co-activation feature families and graph-regularized SAEs (Disentangling Dense Embeddings 2408.00657; GSAE; Sparse Feature
  Coactivation 2506.18141): group SAE features by OBSERVATIONAL co-activation/geometry. By construction these cannot group
  a concept's absorbed/split latents (mutually exclusive in firing). We use the opposite, INTERVENTIONAL signal (correlated
  change, or complementary coverage, under a content counterfactual), training-free, and demonstrate the structural blind
  spot via low-Jaccard + sliced-recall wins.
- >-
  Mutual-exclusivity / Ising-coupling and slot-conditional exclusivity grouping of SAE latents (Bhalla et al. global Ising
  coupling; slot-conditional exclusivity studies): group latents by negative co-occurrence. Exclusivity shows two latents
  do not co-fire but not that they belong together. We supply the missing POSITIVE interventional signal (correlated co-response
  for splitting; complementary coverage of the same content flip for absorption) plus a precision floor.
- >-
  Domain-Filtered Knowledge Graphs from SAE Features (2604.23829): builds an internal knowledge graph from SAE features via
  contrastive corpus filtering, co-occurrence, decoder geometry -- purely OBSERVATIONAL. Our feature-level knowledge graph
  is built from INTERVENTIONAL co-response/complementary-coverage grouping, so its edges encode conditioning environments
  and specialization (absorbed/split children) invisible to observational co-occurrence.
- >-
  Differential co-expression / perturbation co-response module discovery in systems biology (DiffCoEx, BMC Bioinformatics
  2010; WGCNA): cluster genes by their CORRELATED RESPONSE TO A PERTURBATION rather than baseline co-expression, because co-regulated
  genes are often not co-expressed at baseline. This is the methodological root transferred; to our knowledge never applied
  to SAE/LLM features. Our novel claim is that the same baseline-vs-perturbation distinction explains and repairs SAE absorption/splitting,
  extended with a complementary-coverage variant for the mutually-exclusive absorption case.
inspiration: >-
  A dual cross-field transfer, with the load-bearing claim now re-led toward absorber-recovery. The GROUPING mechanism is
  a Level-3 (methodological) import from systems biology's differential co-expression / perturbation co-response module discovery
  (DiffCoEx, WGCNA): cluster units by their CORRELATED RESPONSE TO A PERTURBATION, not by baseline co-expression, because
  co-regulated genes are frequently not co-expressed until perturbed -- mapping genes->SAE latents and a chemical/genetic
  perturbation->an input content counterfactual. The SUPPORTING robustness mechanism is a Level-1/2 import from distributionally-robust
  learning / subpopulation-shift research (group-DRO; Mind-the-GAP 2403.09869) and the label-free worst-group-robustness subfield
  (JTT, GEORGE, EIIL, LfF, Diverse Prototypical Ensembles): a single ERM hyperplane collapses on under-served minority subgroups
  under mixing-weight shift, whereas a union of specialists is robust -- and an absorber is precisely a specialist for one
  latent sub-context. The reviewer-prompted refinement: because the SAME mechanism predicts a count-matched POOL of marginal-attribution-selected
  directions is also robust, beating one hyperplane is a pooling effect; what isolates CO-RESPONSE SELECTION is beating the
  count-matched marginal-attribution pool -- the membership/selection criterion at matched pool size -- which is the SAME
  quantity as C3 absorber-recovery. These fuse with (i) causal ML's counterfactual invariance (Veitch 2021) and concept-erasure
  (LEACE, Belrose 2024) for the conceded surface-invariant baseline; (ii) NLP minimal-pair counterfactuals (ParaDetox, Kaushik
  2020 CAD, CEBaB aspects) for non-circular perturbations and independent sub-context labels; and (iii) a complementary-coverage
  (set-cover-style) extension for absorption. The unifying insight an interpretability expert would not reach for: SAE absorption/splitting
  are structurally the same obstacle that (a) defeats baseline co-expression in biology and (b) makes ERM probes brittle under
  subpopulation shift -- and the recovered absorbers ARE the latent subpopulations.
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
    a best-of-random-k null MATCHED on marginal content-response AUC, and -- at small k in {2,3} -- an absolute effect-size
    floor (pooled-minus-best AUC gain >= 0.05 with a bootstrap CI excluding 0) because the matched null is conservative there.
- term: Single unit admission rule
  definition: >-
    A candidate unit is admitted iff it clears signature C (within-unit content-response correlation above the 95th-pct shuffled-pair
    null) OR signature K (matched best-of-random-k null plus the small-k effect-size floor, with mutual-exclusivity and precision-floor
    constraints), AND its pooled surface-response is not above the shuffled-surface null. The cleared signature is reported
    per concept and the false-admit rate under both nulls (target <= 0.05).
- term: Surface-invariant matched probe (baseline f, single hyperplane)
  definition: >-
    A counterfactually-matched diff-of-means/linear probe on content-flip residual deltas, made surface-invariant by ERASING
    the surface-flip direction via LEACE / mean-projection (Belrose 2024). It is a SINGLE hyperplane after erasing one training-estimated
    surface subspace; the unit beating it is conceded to be a POOLING effect, not selection evidence.
- term: Supervised oracle pool (baseline g)
  definition: >-
    Pools the top-N SAE latents selected by a supervised probe-attribution causal-effect criterion (SCR/TPP, Karvonen 2411.18895
    / Marks SHIFT). Because it ranks by MARGINAL attribution it silently drops absorbed latents firing only in narrow sub-contexts;
    the co-response unit must match/beat it to show co-response selection adds value over flat supervised selection.
- term: Count-and-pool-matched probe (baseline h)
  definition: >-
    Max-pool over EXACTLY the number of raw residual-stream directions equal to the admitted unit's member count, selected
    by the SAME SCR/TPP attribution as (g). It controls member-count AND pooling nonlinearity, holding pool SIZE fixed, so
    any residual unit advantage over it is attributable to the membership/SELECTION criterion. The unit-vs-(h) sliced-recall
    comparison is the selection-isolating headline test.
- term: Oracle group-DRO probe (baseline j)
  definition: >-
    A dense probe trained with a group-DRO objective using the TRUE independent sub-context labels (toxicity sub-attributes
    / CEBaB aspect levels). It is the worst-group-robustness UPPER BOUND because it uses labels the unsupervised unit never
    sees; the unit is predicted to APPROACH its worst-sub-context recall without using sub-context labels.
- term: Label-free group-inference probe (baseline k)
  definition: >-
    A dense probe made group-robust WITHOUT sub-context labels via the established label-free route -- JTT-style upweighting
    of high-loss examples or GEORGE-style clustering of representations to infer groups followed by group-DRO. Like the unit
    it uses no sub-context labels, but it reweights EXAMPLES and retrains; the unit instead groups FEATURES and is training-free
    and auditable.
- term: >-
    Selection-criterion isolation (co-response vs marginal-attribution at matched pool size)
  definition: >-
    The pre-registered ORDERING (f) single hyperplane < (g)/(h) count-matched marginal-attribution pools < unit co-response
    pool on worst-sub-context recall. The unit-vs-(g)/(h) comparison holds POOL SIZE FIXED and varies ONLY the membership/SELECTION
    rule (co-response clustering vs marginal SCR/TPP ranking); both arms pool, so it isolates SELECTION, not 'grouping vs
    pooling'. The structural claim reduces to: co-response membership admits the absorber marginal-attribution ranking drops
    -- the SAME quantity as C3 absorber-recovery. Beating (f) is conceded as a pooling effect.
- term: A-priori MDE / paired-gap bootstrap
  definition: >-
    The pre-registered power analysis for the now-central unit-minus-(g)/(h) worst-sub-context recall gap. Conservative unpaired
    per-arm size n ~= 7.84*[p1(1-p1)+p2(1-p2)]/Delta^2 (alpha=0.05, power=0.80): ~91 positives for Delta=0.20, ~167 for Delta=0.15,
    ~384 for Delta=0.10; the paired design is more powerful. We pre-register n_min=150 positives per tested under-served sub-context,
    stratify collection to reach it, and test the gap by a PAIRED bootstrap (B=10000) on per-example correctness differences
    plus an exact McNemar test, reporting the gap's sign and its slope-vs-reweighting-magnitude as the primary inferential
    object.
- term: >-
    Worst-sub-context recall under sub-population reweighting (supporting classification slice)
  definition: >-
    Recall on the sub-contexts a training-fit dense probe under-serves, evaluated as the test mixture is re-weighted toward
    those sub-contexts. Sub-contexts are defined from INDEPENDENT labels frozen before any comparison and 'under-served' is
    determined on the dense probe (f) alone; the complementary-coverage unit is predicted to keep this recall stable while
    a single hyperplane AND the count-matched marginal-attribution pool collapse.
- term: Degenerate-construction guard
  definition: >-
    The pre-registrations that prevent the reweighting headline from being true-by-construction: sub-contexts defined from
    independent labels fixed first (never from the unit's members), under-served determined on the dense probe alone, a pre-registered
    reweighting-magnitude axis, and a non-triviality check confirming the dense probe genuinely collapses on those independently-defined
    sub-contexts (else the test is void).
- term: Load-bearing core
  definition: >-
    The minimal pre-registered result set the paper stands on regardless of robustness outcomes: pilot (Tier 0) + C1 (beat
    raw latent + observational clusters) + C3 (absorber-recovery vs the oracle pool (g)/count-matched pool (h) + KG-edge agreement
    with Chanin 2409.14507) on first-letter and the best-powered toxicity family. Measured against SAE-selection baselines,
    not the dense-probe aggregate-F1 bar, so it does not depend on out-classifying a strong dense probe.
- term: Reliable unit of analysis
  definition: >-
    A human-auditable group of SAE latents that tracks a concept dependably across surface variation and sub-population reweighting
    -- recovering recall that absorption/splitting destroy at the single-latent level and that marginal-attribution selection
    drops -- reusable as a classifier (headline) and secondarily for steering and model-diffing.
summary: >-
  SAE latents encoding one concept are often mutually exclusive in firing (feature absorption and splitting), so observational
  co-activation, decoder geometry, and marginal-attribution selection all structurally miss the right members; clustering
  latents instead by how they jointly track a content counterfactual (correlated co-response for splitting, complementary
  coverage for absorption, admitted by one null-anchored rule) recovers training-free, auditable multi-member concept units.
  The load-bearing result is that the unit beats raw latents and observational clusters and recovers the absorbers a count-matched
  marginal-attribution selection drops (with knowledge-graph edges agreeing with the supervised absorption diagnostic); keeping
  worst-sub-context recall stable under sub-population reweighting -- approaching an oracle group-DRO probe without sub-context
  labels -- is a supporting second result.
</previous_hypothesis>

<previous_review_feedback>
A reviewer evaluated your previous hypothesis and provided the feedback below.

IMPORTANT: Do NOT generate a completely new hypothesis. Take the previous hypothesis above and
REVISE it to address the feedback. Keep what works, fix what was criticized.

You MUST address ALL the critiques. Do NOT repeat the same mistakes.

kind: reviewer_feedback
id: review_hypo_3520d8dd7e4a
overall_assessment: >-
  This is a mature, exceptionally well-engineered iteration-6 revision of the Counterfactual Co-Response Grouping (CCRG) hypothesis:
  cluster frozen SAE latents by their INTERVENTIONAL co-response to content counterfactuals (rather than observational co-activation
  or decoder geometry) to recover training-free, auditable, multi-member concept units. The revision substantively addresses
  ALL five critiques from the prior round. (1) The thin-statistics major is fixed with a genuine a-priori MDE (n approx 7.84*[p1(1-p1)+p2(1-p2)]/Delta^2),
  a pre-registered PAIRED bootstrap on the per-pair unit-minus-(g)/(h) gap plus exact McNemar, n_min=150 with stratified collection,
  and per-family CIs made PRIMARY with the cross-family number explicitly demoted to descriptive. (2) The execution-complexity
  major is fixed via an explicit TIER-1a load-bearing core, hard per-tier GPU-hour budgets, and a pre-registered drop order.
  (3) The title/headline is re-led with C1+C3 and robustness is openly labelled a supporting second result. (4) The 'grouping-vs-pooling'
  label is renamed to 'selection-criterion isolation' and a small-k effect-size floor (>=0.05, bootstrap CI excluding 0) is
  added for signature K. (5) Steering and model-diffing now have always-run minimal fallbacks. The cross-field transfer (differential
  co-expression / DiffCoEx -> SAE feature grouping) remains novel against the current literature, and the honesty/de-risking
  is best-in-class. What still holds it at Weak Accept rather than Accept: the NAMED contribution -- the clustering algorithm
  itself -- remains the least-specified part of an otherwise meticulous design, and it harbors a real proposal-time tension
  for the absorption (signature-K) regime; and the genuinely load-bearing spine (C3 absorber-recovery) is pre-registered on
  a single narrow, synthetic concept (first-letter spelling). Both are fixable and neither is fatal, but for a clustering-methods
  venue they are the highest-impact residuals. The hypothesis is on track and the score is stable at 6.
strengths:
- >-
  Genuinely novel, well-motivated cross-field transfer: differential co-expression / perturbation co-response module discovery
  (DiffCoEx, WGCNA) mapped to SAE-latent grouping (genes->latents, perturbation->content counterfactual). Verified against
  the current literature -- existing SAE-feature grouping is observational (co-activation feature families, decoder geometry,
  spectral clustering of binarized embeddings on Jaccard = exactly the conceded (b) baseline); no prior work groups FROZEN
  public SAE latents by interventional co-response into auditable multi-member units. The structural argument that observational
  signals CANNOT group absorbed/split latents (mutually exclusive in firing) is correct and well-grounded in Chanin 2409.14507.
- >-
  Best-in-class de-risking and intellectual honesty: a clearly delineated load-bearing core vs supporting results, a pre-registered
  honest-negative interpretation for every branch (tie with (g)/(h) -> reduces to absorber-recovery+auditability; (k) wins
  -> loss-reweighting wins for pure robustness; (f) does not collapse -> reweighting test void), the AxBench/DeepMind dense-probe
  bar conceded explicitly rather than fought, and bias_in_bios pre-registered as a boundary-null.
- >-
  The statistical design is now strong and directly answers the prior major: a real a-priori MDE, a paired-gap bootstrap (B=10000)
  plus exact McNemar as the central inferential object, slope-vs-reweighting-magnitude as the primary quantity, stratified
  collection to n_min, and the correct demotion of the n=3-4 cross-family bootstrap to descriptive-only.
- >-
  The selection-criterion isolation (co-response membership vs marginal SCR/TPP attribution at MATCHED pool size) is a sharp,
  mechanistically grounded contrast that reduces the structural claim to one falsifiable sentence ('co-response membership
  admits the absorber that marginal-attribution ranking drops') and correctly concedes that beating the single hyperplane
  (f) is a pooling effect, not selection evidence.
- >-
  Tiered execution with hard GPU-hour budgets, a pre-registered drop order, and always-run minimal steering + model-diffing
  fallbacks makes the run robustly triageable: a clean publishable core is produced even under heavy truncation.
dimension_scores:
- dimension: soundness
  score: 3
  justification: >-
    The evaluation design, baseline matching (especially (g)/(h) count-and-pool matching), admission rule with dual nulls,
    degenerate-construction guard, and the now-rigorous power/MDE analysis are all sound and carefully reasoned. The principal
    soundness gap is that the clustering algorithm -- the actual method -- is specified in two sentences, and the signature-K
    (absorption) candidate-proposal mechanism has an unresolved tension: mutually-exclusive, disjoint-support absorbers have
    LOW pairwise content-response correlation, so a correlation/affinity-based agglomerative clustering cannot naturally propose
    them as a group. The admission rule only FILTERS candidates; it cannot rescue a K-unit the clustering never proposes.
  improvements:
  - >-
    Specify the K-candidate generation procedure concretely (e.g., anchor on a candidate general/parent latent, then greedily
    add mutually-exclusive latents that cover its content-response holes -- a set-cover, not a symmetric pairwise affinity)
    and prove it can recover the worked 'starts-with-L' example at proposal time.
  - >-
    State explicitly that the K-anchor/seed is selected WITHOUT the supervised absorption diagnostic (else 'unsupervised grouping
    beats the supervised oracle' is undercut and the KG-edge validation against Chanin 2409.14507 becomes partly circular).
  - >-
    Define the coverage-complementarity 'affinity term' formally, since 'complementary' is ill-defined for arbitrary disjoint-support
    latent pairs without a shared concept reference.
- dimension: presentation
  score: 3
  justification: >-
    Well-organized and navigable despite enormous density: the baseline glossary (a-k in one plain line each), the explicit
    load-bearing/supporting/conceded labelling, the result grid with predicted signs and 'what it isolates', and the tiered
    execution plan are all genuine aids. The title now correctly leads with C1+C3. The cost is sheer length and the cognitive
    load of 11 baselines and two parallel regime stories; a first-time reader must work hard. Minor: the central novel object
    (the clustering algorithm) gets a fraction of the page budget that the evaluation scaffolding receives.
  improvements:
  - >-
    Give the clustering algorithm its own compact, prominent specification (pseudocode-level) so the named contribution is
    as legible as the evaluation design.
  - >-
    Consider a single figure schematic of the two signatures (C: positive co-response correlation; K: complementary coverage
    over disjoint supports) to offload the reader's working memory.
- dimension: contribution
  score: 3
  justification: >-
    A solid, original contribution: a training-free, post-hoc, auditable repair of frozen public SAEs that targets the precise
    regime (absorption/splitting) where observational grouping and marginal-attribution selection structurally fail, with
    a feature-level knowledge graph as a usable artifact. The contribution is held back from 'excellent' by two things: the
    truly load-bearing spine (C3 absorber-recovery) is demonstrated on ONE narrow synthetic concept (first-letter spelling
    -- the only regime where absorption is empirically documented at scale), and 'auditability', which becomes the standalone
    deliverable in the all-ties branch, is asserted rather than measured.
  improvements:
  - >-
    Broaden C3 to at least one non-spelling absorption testbed (a documented taxonomic/numeric hierarchy, e.g. hypernym 'is-a-country/city'
    with per-entity absorbers, or numerical-quantity -> dates/percentages) to move the spine from 'one synthetic task' to
    'absorption as a phenomenon'.
  - >-
    Operationalize one auditability claim as a measured experiment (the 'read the KG -> add the missing absorber -> fix the
    steering/recall hole' loop) so the fallback deliverable is a result, not an assertion.
critiques:
- id: ''
  category: methodology
  severity: major
  description: >-
    The clustering algorithm -- the explicitly named contribution per the goal ('a new clustering-based method for organising
    SAE activations') -- is the least-specified part of an otherwise meticulous design, and it has an unresolved PROPOSAL-TIME
    tension for the absorption regime. The method is described as 'a differential-correlation affinity (DiffCoEx-style) for
    signature C and a coverage-complementarity term for signature K, via agglomerative clustering / graph community detection
    on the affinity.' But signature K targets latents that are MUTUALLY EXCLUSIVE in firing (Jaccard<0.1) and respond to the
    same content flip on DISJOINT context supports. Such members have LOW pairwise content-response correlation (the general
    'starts-with-L' latent responds broadly; the 'lion'-absorber responds only on lion pairs; their content-response vectors
    barely overlap), so a correlation/affinity-based agglomerative clustering -- which merges positively-correlated items
    -- will NOT propose them as a candidate group. Complementary coverage is a set-level / set-cover property, not a symmetric
    pairwise affinity, and 'complementary' is ill-defined for arbitrary disjoint-support latent pairs without a shared concept
    anchor. The single admission rule is only a FILTER over candidate units; it cannot admit a K-unit the clustering never
    generated. If the proposal step cannot surface the right absorber group, the entire C3 spine fails at step 1. This concern
    has been latent across all prior iterations (reviews focused on statistics, scope, baselines, novelty -- never on whether
    the clustering can actually PROPOSE the K-units), and it is now the highest-impact fix because C3 is the load-bearing
    spine.
  suggested_action: >-
    Spell out the clustering pipeline as a concrete, reproducible procedure: (i) the per-latent context-by-content-response
    feature it operates on; (ii) the C-affinity (positive content-response correlation) used for splitting; (iii) a SEPARATE,
    anchor-based set-cover procedure for K -- seed on a candidate general/parent latent and greedily add mutually-exclusive
    latents that cover the seed's content-response holes -- since pairwise affinity cannot group disjoint-support absorbers;
    (iv) how C-clusters and K-units are reconciled into one output; (v) the cluster-count / stopping criterion. CRITICAL:
    confirm the K-seed is selected WITHOUT the supervised absorption diagnostic (e.g., the highest-recall content-responsive
    latent), because if the seed uses the Chanin 2409.14507 diagnostic, the 'unsupervised unit beats the supervised oracle
    (g)/(h)' claim is undercut and the KG-edge-agreement validation against that same diagnostic becomes partly circular.
    Demonstrate at the pilot that the proposal step recovers the worked 'starts-with-L' unit before relying on it for C3.
- id: ''
  category: scope
  severity: major
  description: >-
    The genuinely load-bearing spine (C3 absorber-recovery + KG-edge agreement) is pre-registered on a SINGLE narrow, synthetic
    concept: first-letter spelling. The toxicity testbed carries SPLITTING (signature C), not absorption, so it does NOT carry
    the C3 spine -- on toxicity the spine reduces to C1 (beating raw latents + observational clusters). Because Tier 1b and
    below are pre-registered as droppable, under time pressure the load-bearing result collapses to 'co-response grouping
    recovers spelling absorbers and beats raw latents on first-letter + one toxicity family.' Web verification confirms feature
    absorption is studied almost exclusively on spelling/first-letter in the literature, which makes a spelling-only spine
    read as a narrow, somewhat toy result to a top-tier reviewer assessing significance -- exactly the dimension where this
    paper is weakest. Crucially, Chanin et al. explicitly name non-spelling absorption cases (taxonomic hierarchies such as
    India->Asia / 'short'->'S'; numerical-quantity latents losing dates and percentages to specialized children), so a second
    absorption testbed is cheap and well-motivated, not speculative.
  suggested_action: >-
    Promote ONE non-spelling absorption concept into the Tier-1a load-bearing core: a documented taxonomic or numeric hierarchy
    (e.g., a hypernym concept like 'is-a-country' / 'is-a-city' with per-entity absorbers, or 'numerical quantity' with date/percentage
    absorbers). Even a single second absorption regime moves C3 from 'one synthetic spelling task' to 'absorption as a general
    phenomenon', materially raising significance, and provides a non-spelling check on the K-proposal procedure. If genuinely
    infeasible within the Tier-1a budget, explicitly scope the C3 claim to spelling-type hierarchical absorption in the title
    and headline, and route the cross-concept generality claim through C1 (which spans toxicity/sentiment/aspect) rather than
    through C3.
- id: ''
  category: rigor
  severity: minor
  description: >-
    C1 -- the unit beats the best raw single latent AND observational co-activation/geometry clusters (b)/(c) on classification
    -- is NOT count-matched, even though the robustness story is at great pains to count-and-pool-match the unit against (g)/(h).
    Beating the 'best raw single latent' (1 direction) with a multi-member pooled unit is near-guaranteed by capacity and
    carries little evidential weight. The meaningful comparison is against the observational clusters (b)/(c); but if the
    co-response unit pools more member latents than the observational cluster it is compared to, a C1 win is a capacity/pooling
    artifact -- precisely the confound the unit-vs-(h) design exists to remove -- rather than evidence that co-response selects
    the RIGHT members.
  suggested_action: >-
    For C1, count-match (b)/(c) to the co-response unit's member count (cut the observational clustering to the same k, or
    take its top-k members by the same pooling rule), and report the comparison at matched pool size. Foreground the matched
    (b)/(c) comparison as the load-bearing part of C1 and explicitly note that beating the single best latent is a near-foregone
    capacity win included only for completeness.
- id: ''
  category: rigor
  severity: minor
  description: >-
    Auditability is promoted to the standalone deliverable when every robustness comparison ties ('Auditability + absorber-recovery
    is the standalone deliverable when every robustness comparison ties'), yet it is asserted rather than operationalized
    or measured. There is no auditability metric, no human-prediction check, and no demonstration that the audit actually
    buys a downstream fix. In the explicitly anticipated all-ties branch, half of the surviving contribution is therefore
    an unmeasured claim, which a skeptical reviewer can dismiss. The hypothesis already states a concretely testable instance
    of auditability -- 'a practitioner reads the KG, sees which sub-context each member covers, and adds a missing absorber
    to fix a steering hole' -- which can be turned into a measured result.
  suggested_action: >-
    Operationalize at least one auditability claim as a measured experiment within the always-run generality demos: show the
    'read the KG -> identify the missing absorber for an under-served sub-context -> add it -> recover recall/steering on
    that sub-context' loop produces a quantifiable repair that the label-free reweighting probe (k) structurally cannot expose
    (because (k) yields an opaque retrained probe, not a per-sub-context member map). This converts the fallback deliverable
    from an assertion into a result and directly de-risks the all-ties branch the paper explicitly anticipates.
score: 6
confidence: 4
relation_type: evolution
relation_rationale: >-
  Same co-response-grouping frame; refined claims: re-led title to C1+C3, added MDE/paired bootstrap, tiering.
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

### [2] HUMAN-USER prompt · 2026-06-17 13:12:52 UTC

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

### [3] SKILL-INPUT — aii-web-tools · 2026-06-17 13:14:10 UTC

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
