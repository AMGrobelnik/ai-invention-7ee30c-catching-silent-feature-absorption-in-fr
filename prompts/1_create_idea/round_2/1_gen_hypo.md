# gen_hypo — create_idea

> Phase: `hypo_loop` · round 2 · Substep: `gen_hypo`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave the agent(s) in this substep — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_hypo_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-17 11:56:55 UTC

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
  Counterfactual Co-Response Grouping: Reliable SAE Concept Units from Interventional Co-Sensitivity, Not Co-Activation
hypothesis: >-
  Sparse-autoencoder (SAE) latents that encode the same underlying concept are frequently observationally uncorrelated or
  mutually exclusive in their firing — precisely because of feature absorption and feature splitting — yet they share a correlated
  RESPONSE to content counterfactuals. Therefore the right signal for grouping latents into reliable units is not how often
  they fire together (co-activation) nor how similar their decoder directions are (geometry), but how their activations CHANGE
  TOGETHER when the input is minimally edited to add or remove a concept while surface form is held fixed (interventional
  co-sensitivity). Concretely: (1) clustering latents by the correlation of their per-context counterfactual content-response
  vectors, restricted to latents that are jointly invariant to surface-form counterfactuals, yields human-auditable concept
  units; (2) these units recover concept recall that absorption/splitting destroy at the single-latent level, because absorbed
  and split variants — observationally exclusive — have aligned counterfactual responses; (3) the units classify safety-relevant
  attributes more robustly than raw latents and at least as well as difference-of-means probes, with the gap widening under
  surface/distribution shift; (4) steering with a unit's shared content-response direction produces fewer side effects at
  matched on-target effect than steering with the best single latent or a difference-of-means direction, because idiosyncratic
  surface-specific components of individual latents cancel; and (5) the same units expose interpretable, validated differences
  between a base model and a fine-tuned variant. The falsifiable core claim is that interventional co-response is a strictly
  better grouping signal than baseline co-activation or decoder geometry whenever, and because, the SAE's failure modes corrupt
  observational signals while leaving interventional ones intact.
motivation: >-
  Single SAE latents are unreliable units of analysis: feature absorption (a general concept's latent silently fails to fire
  when a more specific latent 'takes over' its tokens) and feature splitting (one concept fragments across many latents) mean
  that no single latent reliably tracks a concept, and recent benchmarks (SAEBench, AxBench) show simple baselines often beat
  raw-latent SAE methods on classification and steering. Every existing post-hoc grouping method — co-activation 'feature
  families', decoder-geometry clustering, graph-regularized SAEs — relies on OBSERVATIONAL signals (which latents fire together,
  or which point in similar directions). But absorption is exactly the regime where observational signals break: the absorbed
  general latent and the absorbing specific latents are mutually exclusive in firing, so co-activation clustering provably
  cannot group them, and their decoders need not be cosine-similar. This is a structural blind spot, not a tuning problem.
  Systems biology faced the identical obstacle: genes that are co-regulated are often NOT co-expressed at baseline and only
  reveal their shared regulation under perturbation — which is why differential co-expression methods (DiffCoEx, WGCNA) cluster
  genes by their CORRELATED RESPONSE TO A PERTURBATION rather than by baseline co-expression. Transferring that principle,
  an input content-edit is the 'perturbation' and SAE latents are the 'genes': a concept's absorbed and split latents, invisible
  to co-activation, become visible through their aligned counterfactual response. If correct, this gives a training-free,
  single-GPU, human-auditable way to turn off-the-shelf public SAEs (Gemma Scope) into reliable units for the safety-critical
  tasks people actually want — robust attribute classification, low-collateral steering, and model-diffing — and a feature-level
  knowledge graph of concepts and their conditioning environments. It also explains a puzzle: why mutual-exclusivity-only
  grouping underperforms (exclusivity tells you latents do not co-fire, but not that they belong together; correlated counterfactual
  co-response is the missing positive signal).
assumptions:
- >-
  Approximate content/surface counterfactuals are obtainable at acceptable cost and quality: an LLM (via OpenRouter, well
  under the $10 budget) can generate matched minimal pairs that flip a target concept while holding surface form roughly fixed
  (content-flip), and that paraphrase surface while holding content fixed (surface-flip). Counterfactual-invariance theory
  tolerates approximate counterfactuals because the differential signal is averaged over many pairs; an activation-space content
  edit (a concept direction) is used as a corroborating cheaper counterfactual.
- >-
  The absorption/splitting hypothesis holds operationally: when a concept is counterfactually added or removed, its absorbed
  and split latents change in a correlated way across contexts, even when those same latents are mutually exclusive or uncorrelated
  in baseline firing. (If absorbed latents did NOT co-respond to the concept intervention, the method has no signal and should
  fail honestly.)
- >-
  Off-the-shelf Gemma Scope SAEs on Gemma-2-2b expose latent counterfactual responses that are measurable above noise on a
  single GPU for a few thousand minimal pairs, and at least some safety-relevant attributes have enough labeled or templatable
  data to build minimal pairs and held-out, surface-shifted test sets.
- >-
  Surface-form confounding is a material driver of single-latent unreliability — i.e., individual latents partly entangle
  a concept with the surface forms it co-occurs with — so removing that confound by counterfactual matching yields units that
  generalize where single latents and single-surface probes do not. (If surface confounding is immaterial, units will collapse
  to raw latents and the method yields no gain.)
investigation_approach: >-
  DATA & CONCEPTS: Use safety-relevant attributes with label structure and natural minimal-pair edits — e.g. toxicity (Jigsaw/civil_comments),
  occupational-gender bias (bias_in_bios), and a clean controlled absorption testbed (first-letter / spelling, the canonical
  absorption case). For each attribute, build (a) content-flip minimal pairs (attribute on vs off, surface held as fixed as
  possible: detoxify/retoxify paraphrase, profession/pronoun swap, template fills) and (b) surface-flip pairs (paraphrase
  / synonym / formatting change, content fixed). COUNTERFACTUAL SIGNAL: Encode every text and its counterfactual with a frozen
  Gemma Scope residual-stream SAE (e.g. layer 12, width 16k canonical; widths as a robustness axis). For each latent, the
  content-response on a pair = delta(latent activation) under the content-flip; the surface-response = delta under the surface-flip.
  Aggregate into per-latent response profiles across contexts. GROUPING: (i) score each latent's surface-invariance (small,
  low-variance surface-response) and content-sensitivity (large, consistent content-response); (ii) among surface-invariant,
  content-sensitive latents, build the content-co-response matrix = correlation of content-response profiles across latents
  and cluster it (DiffCoEx-style differential clustering / correlation-graph community detection) into concept units; (iii)
  emit human-auditable definitions (top member latents, their decoder logit-lens tokens, and the conditioning contexts where
  each member carries the concept) and directed specialization edges (a member responsive only in a sub-context = an absorbed/split
  child) — a feature-level knowledge graph. BASELINES: raw best single latent (any width); observational co-activation clustering
  / feature families; decoder-geometry clustering; difference-of-means probe; linear probe on raw residual activations (the
  last two are the required non-SAE baselines). EVAL 1 - CLASSIFICATION: use unit-pooled activation (e.g. max/sum over members)
  as a classifier on IID and SURFACE-SHIFTED test splits; report F1/AUC and, crucially, recall on absorbed/held-out-surface
  cases; headline = robustness gap under shift vs baselines, plus a controlled check that content-co-response clusters have
  LOW overlap with co-activation/geometry clusters and win specifically where they differ. EVAL 2 - STEERING: steer with the
  unit's shared content-response direction vs best single latent vs difference-of-means; measure on-target effect (target-concept
  probability) and side effects (KL divergence on unrelated prompts, fluency), reporting side-effects at MATCHED on-target
  effect. EVAL 3 - MODEL-DIFFING: apply the same base SAE to base Gemma-2-2b and an instruction-tuned/LoRA-finetuned variant,
  recompute units on both, and report which units shift (membership change, response-magnitude change) as an interpretable
  diff, sanity-checked against known fine-tuning effects (e.g. refusal/safety shifts). HONEST FAILURE-MODE REPORTING: dependence
  on counterfactual quality; concepts with no surface-invariant co-responding group; regimes where co-response collapses to
  co-activation (no gain); cases where difference-of-means still wins IID; compute cost; sensitivity to SAE layer/width.
success_criteria: >-
  CONFIRMED if: (1) content-co-response units beat the best raw single latent on safety-attribute classification, and the
  advantage over difference-of-means probes and single-surface linear probes is positive and grows under surface/distribution
  shift (pre-registered shift split); (2) units recover concept recall on absorbed/held-out cases that observational co-activation
  clustering measurably misses, with a controlled experiment showing co-response clusters differ from co-activation/decoder
  clusters (low Jaccard) AND outperform them specifically on the differing members; (3) steering with the unit direction achieves
  lower KL side effects than best-single-latent and difference-of-means at matched on-target effect, with bootstrap confidence
  intervals; (4) model-diffing surfaces a small set of unit changes that align with independently known differences between
  the base and fine-tuned models. DISCONFIRMED / HONEST NEGATIVE if: content-co-response grouping gives no advantage over
  observational co-activation grouping (i.e. co-response approximately equals co-activation), or fails to beat raw latents
  and difference-of-means even under shift, or counterfactual responses are too noisy to cluster stably, or surface-form confounding
  turns out to be immaterial (units approximately equal raw latents). A clean null result — that absorbed latents do NOT co-respond
  to concept interventions, so interventional co-sensitivity carries no extra signal — would itself be a publishable, mechanism-level
  finding about how SAEs (mis)represent concepts.
related_works:
- >-
  A is for Absorption (Chanin et al., 2409.14507): diagnoses feature absorption/splitting on a supervised first-letter task
  using a logistic-regression probe direction plus decoder-cosine and ablation to identify the single absorbing latent. It
  is a supervised, pairwise DIAGNOSTIC, not an unsupervised grouping method, and its signal is observational (firing gap +
  decoder geometry). This proposal instead GROUPS latents into reliable units, unsupervised, using interventional counterfactual
  co-response, and repairs absorption into a usable classifier/steering unit rather than merely detecting it.
- >-
  Co-activation 'feature families' and graph-regularized SAEs (Disentangling Dense Embeddings 2408.00657; GSAE 2512.06655;
  'Sparse Feature Coactivation Reveals Causal Semantic Modules' 2506.18141): group SAE features by OBSERVATIONAL co-activation
  (e.g. Pearson rho > 0.9 of activations) and/or decoder geometry, sometimes baking the graph into retraining (GSAE). By construction
  these cannot group a concept's absorbed/split latents, which are mutually exclusive in firing. This proposal uses the opposite,
  interventional signal — correlated change under a content counterfactual — which is exactly the regime where co-activation
  is blind, and it is training-free on frozen public SAEs.
- >-
  Meta-SAEs and Matryoshka SAEs (Showing SAE Latents Are Not Atomic; 2503.17547): expose hierarchy by decomposing decoder
  directions with a learned meta-SAE (decoder geometry) or by RETRAINING nested dictionaries. They rely on geometry/training
  and target atomicity/hierarchy, not reliability under surface shift. This proposal needs no retraining and no decoder-geometry
  assumption; its unit is defined behaviorally by counterfactual co-response and surface invariance, and is evaluated on concrete
  safety classification/steering/diffing.
- >-
  SAE-Targeted Steering (SAE-TS, 2411.02193), Sparse Feature Circuits (Marks et al. 2403.19647), and functional neuron grouping
  (NeurFlow 2502.16105): build feature-to-OUTPUT causal maps/graphs (the feature is the CAUSE; effect measured on logits or
  downstream features) to optimize a single steering vector or find a task circuit. This proposal reverses the causal direction
  — it perturbs the INPUT (content edit) and measures each feature's RESPONSE (the feature is the EFFECT), then clusters features
  by correlated response into reusable, auditable reliability units; SAE-TS/SFC/NeurFlow neither cluster by counterfactual
  input-response nor target surface-invariant reliability units.
- >-
  Counterfactual Invariance to Spurious Correlations (Veitch, D'Amour, Yadlowsky, Eisenstein, NeurIPS 2021, 2106.00545) and
  contrastive SAE steering (FGAA 2501.09929; Denoising Concept Vectors with SAEs 2505.15038): formalize counterfactual invariance
  for robust PREDICTORS, or compute a contrastive difference in SAE space to build a single steering vector. This proposal
  imports counterfactual invariance and minimal pairs as a GROUPING signal for SAE latents — clustering many latents into
  concept units by correlated counterfactual response — rather than training one predictor or one steering vector.
- >-
  Differential co-expression / perturbation co-response module discovery in systems biology (DiffCoEx, WGCNA): cluster genes
  by their CORRELATED RESPONSE TO A PERTURBATION rather than by baseline co-expression, precisely because co-regulated genes
  are often not co-expressed at baseline. This is the methodological root being transferred; to our knowledge it has never
  been applied to SAE/LLM features. The novel scientific claim is that the same baseline-vs-perturbation distinction explains
  and repairs SAE absorption/splitting, where the 'perturbation' is a content counterfactual on the input text.
- >-
  Mutual-exclusivity / Ising-coupling grouping of SAE latents (e.g. Bhalla et al. global Ising coupling, and slot-conditional
  exclusivity studies): group latents using negative co-occurrence (they do not fire together). Exclusivity establishes that
  two latents do not co-fire but not that they encode the same concept, and such methods have struggled to deliver downstream
  gains. This proposal supplies the missing positive signal — correlated counterfactual co-response plus surface invariance
  — that unites mutually-exclusive absorbed variants, and is explicitly designed to test whether this positive interventional
  signal succeeds where exclusivity alone does not.
inspiration: >-
  A Level-3 (methodological) cross-field transfer from systems biology's differential co-expression / perturbation co-response
  module discovery (DiffCoEx, WGCNA): cluster units by their CORRELATED RESPONSE TO A PERTURBATION, not by baseline co-expression,
  because co-regulated genes frequently are not co-expressed until perturbed. Mapping genes->SAE latents and a chemical/genetic
  perturbation->a content counterfactual on the input gives the core mechanism. This is fused with causal ML's counterfactual
  invariance to spurious correlations (Veitch et al. 2021) and minimal-pair counterfactuals from NLP, which supply the surface-vs-content
  axis and the robustness-under-shift guarantee. The unifying insight that an interpretability expert would not reach for:
  the SAE failure modes (absorption, splitting) are structurally the same obstacle that defeats baseline co-expression in
  biology — the right group members are invisible at baseline and only become visible under perturbation — so the field's
  reliance on observational co-activation/geometry is the wrong instrument, and interventional co-response is the matched
  one.
terms:
- term: Sparse autoencoder (SAE) latent
  definition: >-
    A single unit of a sparse dictionary trained to reconstruct a language model's internal activations; each latent has an
    encoder direction (when it fires) and a decoder direction (what it writes back), and is intended to correspond to one
    interpretable concept.
- term: Feature absorption
  definition: >-
    A sparsity-induced failure where a general concept's latent stops firing on inputs handled by a more specific latent (e.g.
    a 'starts-with-L' latent goes silent on 'lion' because a 'lion' latent absorbs it), so the general latent has unpredictable
    holes and is an unreliable classifier.
- term: Feature splitting
  definition: >-
    A single concept fragmenting across many latents (more so at larger dictionary width), so no individual latent covers
    the whole concept and the concept's latents are often mutually exclusive across contexts.
- term: Counterfactual minimal pair
  definition: >-
    Two inputs differing in exactly one targeted way: a content-flip pair changes whether a concept is present while holding
    surface form roughly fixed; a surface-flip pair paraphrases/rewrites surface while holding content fixed.
- term: Counterfactual content-response (of a latent)
  definition: >-
    The change in a latent's activation between a content-flip pair (concept added minus removed), measured per context; the
    vector of these changes across many contexts is the latent's content-response profile.
- term: Interventional co-sensitivity / co-response
  definition: >-
    The criterion that two latents belong to the same concept unit if their counterfactual content-response profiles are correlated
    across contexts — i.e. they change together when the concept is added/removed — even if their baseline activations never
    co-occur.
- term: Surface-form confounding / surface invariance
  definition: >-
    The tendency of a latent to entangle a concept with the surface forms it co-occurs with; a surface-invariant latent or
    unit shows little response to surface-flip counterfactuals, making it robust to paraphrase and distribution shift.
- term: Differential co-expression (analogy)
  definition: >-
    A systems-biology family of methods (DiffCoEx, WGCNA) that clusters genes by how their expression co-varies under a perturbation
    rather than at baseline, revealing co-regulated modules invisible to baseline co-expression — the methodological template
    transferred here to SAE latents.
- term: Difference-of-means probe
  definition: >-
    A non-SAE baseline classifier/steering direction computed as the difference between mean activations of positive and negative
    examples; strong but prone to absorbing surface correlations present in the training distribution.
- term: Model-diffing
  definition: >-
    Comparing two related models (e.g. a base model and a fine-tuned variant) through their internal features to localize
    what changed; here, by recomputing counterfactual co-response units on each model and reporting unit-level shifts.
- term: Reliable unit of analysis
  definition: >-
    A human-auditable group of SAE latents that tracks a concept dependably across surface variation — recovering recall that
    absorption/splitting destroy at the single-latent level — and is reusable for classification, steering, and model-diffing.
summary: >-
  SAE latents that encode the same concept are often mutually exclusive in firing (because of feature absorption and splitting),
  so observational co-activation and decoder geometry cannot group them; instead, grouping latents by their CORRELATED RESPONSE
  TO CONTENT COUNTERFACTUALS while requiring invariance to surface counterfactuals — a transfer of systems biology's differential
  co-expression principle — yields training-free, auditable concept units that classify safety attributes robustly under surface
  shift, steer with fewer side effects, and reveal interpretable model-diffs, beating raw latents and matching or auditing
  better than difference-of-means probes.
</previous_hypothesis>

<previous_review_feedback>
A reviewer evaluated your previous hypothesis and provided the feedback below.

IMPORTANT: Do NOT generate a completely new hypothesis. Take the previous hypothesis above and
REVISE it to address the feedback. Keep what works, fix what was criticized.

You MUST address ALL the critiques. Do NOT repeat the same mistakes.

kind: reviewer_feedback
id: review_hypo_25d152809c51
overall_assessment: >-
  This is a strong, genuinely novel, and unusually well-positioned hypothesis. The central idea — group SAE latents by their
  CORRELATED RESPONSE TO CONTENT COUNTERFACTUALS (interventional co-sensitivity), restricted to surface-invariant latents,
  rather than by co-activation or decoder geometry — is a clean Level-3 cross-field transfer from systems biology's differential
  co-expression (DiffCoEx/WGCNA) that, to my knowledge, has not been applied to SAE/LLM features. The motivation is well-grounded
  in the current state of the field: AxBench (ICML 2025 spotlight, 2501.17148) shows simple baselines (difference-of-means,
  prompting) beat raw-latent SAE methods, and the absorption/splitting literature (Chanin et al. 2409.14507; 'Sparse Autoencoders
  Do Not Find Canonical Units of Analysis', ICLR 2025) establishes that single latents are unreliable units — so the problem
  is real and timely. I verified the closest recent competitor (Domain-Filtered Knowledge Graphs from SAE Features, 2604.23829)
  is purely observational (co-occurrence + contrastive-corpus filtering + decoder geometry), so the interventional-co-response
  grouping signal is genuinely unoccupied. The falsifiable core claim is crisp and the honest-null framing (a clean 'absorbed
  latents do NOT co-respond' negative is itself publishable) de-risks the project. However, the proposal is over-scoped (five
  distinct evaluation axes, each nearly a paper), the central mechanism is more plausible for feature SPLITTING than for feature
  ABSORPTION (which the proposal conflates and leans on heavily via the first-letter testbed), and — most importantly — the
  headline 'beats difference-of-means under shift' result is confounded unless the diff-of-means and linear-probe baselines
  are given the SAME counterfactual/minimal-pair training signal, since counterfactual matching strips surface confounds for
  ANY method, not just SAE units. Fixing the baseline confound, de-risking the absorption mechanism with a cheap pilot, and
  narrowing to one decisive headline would move this from Weak Accept toward a confident accept. The idea is on track and
  worth the compute.
strengths:
- >-
  Genuine, well-differentiated novelty: grouping SAE latents by correlated counterfactual content-response (interventional
  signal) — restricted to surface-invariant latents — is a new positive grouping signal. The related-work section correctly
  distinguishes it from co-activation feature families (2408.00657, GSAE, 2506.18141), decoder-geometry/meta-SAE/Matryoshka
  (2503.17547), feature->output causal maps (SAE-TS 2411.02193, SFC 2403.19647, NeurFlow), and mutual-exclusivity/Ising grouping.
  I confirmed the closest 2026 SAE-knowledge-graph work (2604.23829) uses observational signals, not interventional minimal-pair
  co-response.
- >-
  The cross-field transfer is principled and the analogy is exact: co-regulated genes are often not co-expressed at baseline
  and only reveal shared regulation under perturbation — structurally the same obstacle as absorption/splitting making a concept's
  latents observationally exclusive. This gives a real mechanistic 'why', not just a metaphor.
- >-
  Excellent honesty about failure modes and a pre-committed disconfirmation path. A clean null (absorbed latents do not co-respond
  → interventional signal carries no extra information) is framed as a publishable mechanism-level finding, which means the
  experiment is informative either way — rare and valuable for a pre-flight hypothesis.
- >-
  Strong fit to the stated constraints: training-free on frozen public Gemma Scope SAEs, single-GPU, human-auditable unit
  definitions (member latents + logit-lens tokens + conditioning contexts + directed specialization edges), explicit non-SAE
  baselines, and a feature-level knowledge graph as the structured-relations deliverable.
- >-
  Motivation is empirically anchored to the right benchmarks (AxBench, SAEBench, absorption work), so reviewers in interpretability
  will recognize the problem as live and the bar (beating diff-of-means) as the correct one.
dimension_scores:
- dimension: soundness
  score: 3
  justification: >-
    The design is falsifiable, uses the right baselines on paper, and the cross-field mechanism is principled. But two soundness
    gaps keep it from a 4: (a) the headline robustness-gap result is confounded unless baselines receive the same counterfactual
    training signal, and (b) the core mechanism (correlated counterfactual co-response among observationally-exclusive latents)
    is asserted, not demonstrated, and is notably more plausible for feature splitting than for feature absorption — the regime
    the proposal foregrounds.
  improvements:
  - >-
    WHAT: Add a counterfactually-matched difference-of-means probe and a counterfactually-matched linear probe (trained on
    the SAME minimal pairs the units are built from) as PRIMARY baselines. HOW: For every minimal pair, also compute the residual-stream
    diff and fit diff-of-means / a probe on those same paired deltas. WHY: counterfactual matching strips surface confound
    for any estimator; if the matched diff-of-means closes the shift gap, the contribution is 'use counterfactual data', not
    'group SAE latents'. This is the single most likely reviewer kill-shot and must be pre-empted. (+1 to +2 overall.)
  - >-
    WHAT: De-risk the central mechanism with a cheap pilot BEFORE the full eval suite. HOW: On the first-letter task, compute
    content-response profiles for the known general 'starts-with-L' latent and its absorbing token-latents and report whether
    their across-context response profiles actually correlate (vs. being disjoint/anti-correlated because the absorbed latent
    is silent exactly where the absorber fires). WHY: if co-response does not survive absorption, EVAL-1 recall claim collapses;
    a 1-GPU-hour pilot prevents wasting compute on five downstream evals. (+0.5 to +1.)
  - >-
    WHAT: Add cluster-stability statistics. HOW: bootstrap over minimal pairs, report cluster agreement (e.g., adjusted Rand
    / Jaccard) across resamples, and a shuffled-pair null for the co-response correlation matrix; report sensitivity to the
    number of pairs per concept. WHY: correlation-graph community detection on a few thousand pairs can be unstable, and the
    headline 'low Jaccard vs co-activation clusters' is only meaningful against a stability/null floor.
- dimension: presentation
  score: 3
  justification: >-
    Very clearly written and exceptionally well contextualized against prior work — the related-work differentiations are
    precise and each cited line has a crisp 'they do X, we do Y'. Held back from 4 by (a) conflating feature absorption and
    feature splitting as if the co-response mechanism behaves identically for both, and (b) extremely dense run-on sentences
    in the hypothesis and success-criteria fields that make the (already complex) five-part claim hard to parse.
  improvements:
  - >-
    WHAT: Separate absorption from splitting explicitly and predict different co-response behavior for each. HOW: state that
    splitting (e.g., toxicity sub-features co-rising under detoxify/retoxify) is the strong case for co-response, while absorption
    (first-letter token-latents) is the stress test, and say so. WHY: reviewers familiar with Chanin et al. will notice these
    are mechanistically distinct; treating them as one weakens credibility.
  - >-
    WHAT: Add a one-paragraph operational definition of the content/surface axis PER task. HOW: e.g., for first-letter, make
    explicit what counts as a 'surface flip' vs 'content flip' when spelling effectively IS the content; for toxicity, define
    how detoxify-paraphrase is prevented from leaking content. WHY: the surface/content distinction is the load-bearing construct
    and is currently underspecified for the spelling testbed.
  - >-
    WHAT: Promote the falsifiable claim and the single headline metric to the top of the hypothesis. HOW: lead with 'co-response
    is a strictly better grouping signal than co-activation/geometry iff SAE failure modes corrupt observational but not interventional
    signals; primary test = robustness gap under pre-registered surface shift'. WHY: improves at-a-glance evaluability.
- dimension: contribution
  score: 3
  justification: >-
    A novel, training-free, post-hoc method that targets a real and acknowledged structural blind spot (co-activation/geometry
    cannot group observationally-exclusive absorbed/split latents) with a principled interventional alternative, plus an auditable
    feature-level knowledge graph. High potential value to interpretability and safety practitioners. Not a 4 because the
    contribution's magnitude is contingent on clearing a very hard baseline (diff-of-means) on a narrow win condition (shift
    gap), and the five-axis scope risks producing five thin results instead of one decisive one.
  improvements:
  - >-
    WHAT: Designate ONE decisive headline (recommend: robustness gap on safety-attribute classification under a pre-registered
    surface/distribution shift, with the low-Jaccard controlled experiment as its mechanistic backbone) and demote steering
    + model-diffing to clearly-labeled secondary/stretch results. HOW: pre-register the primary split and metric; cap steering/diffing
    to a single illustrative case each. WHY: top venues reward one well-supported claim over five hedged ones; concentrating
    compute raises the probability of a confident accept. (+0.5 to +1.)
  - >-
    WHAT: Make the auditable knowledge-graph deliverable a first-class contribution with a concrete evaluation. HOW: specify
    how directed specialization edges (absorbed/split child) are validated (e.g., against the supervised absorption diagnostic
    of 2409.14507 as a partial oracle on first-letter). WHY: turns the KG from a by-product into a defensible artifact aligned
    with the 'knowledge graph / knowledge extraction' reviewer scope.
critiques:
- id: ''
  category: methodology
  severity: major
  description: >-
    BASELINE CONFOUND (likely reviewer kill-shot). The headline claim is that units beat difference-of-means and linear probes
    'with the gap widening under surface/distribution shift' because counterfactual matching strips the surface confound.
    But counterfactual matching strips surface confounds for ANY estimator, not just SAE-latent units. As written, the comparison
    risks pitting counterfactually-matched SAE units against distributionally-naive diff-of-means/probes trained on raw labeled
    data — so any shift-robustness gain could be attributed to the counterfactual training data, not to grouping SAE latents.
    AxBench (2501.17148, ICML 2025 spotlight) already shows plain diff-of-means is the strongest concept-detection baseline
    and beats SAE methods, so this baseline must be made maximally fair or the contribution evaporates.
  suggested_action: >-
    Add as PRIMARY baselines: (a) a difference-of-means probe computed on the SAME minimal-pair deltas the units are built
    from, and (b) a linear probe trained on counterfactually-matched (paired) residual activations. Pre-register the claim
    as 'SAE co-response units beat the counterfactually-matched diff-of-means/probe under shift'. If the matched diff-of-means
    closes the gap, report that honestly — it reframes the finding as 'counterfactual supervision helps' rather than 'SAE
    grouping helps', which is still publishable but a different paper.
- id: ''
  category: rigor
  severity: major
  description: >-
    CORE MECHANISM IS ASSERTED, NOT DEMONSTRATED, AND IS WEAKEST FOR ABSORPTION. The pivotal premise is that a concept's absorbed/split
    latents, while observationally exclusive, have CORRELATED counterfactual content-response across contexts. For feature
    splitting this is plausible (toxify a sentence → many toxicity sub-latents rise together). For feature absorption it is
    questionable: an absorbed general latent is SILENT in exactly the contexts the absorbing token-latent handles, so under
    a content flip in those contexts its delta-activation is ~0 while the absorber's is large — their across-context response
    profiles can be disjoint or anti-correlated rather than correlated, which would make co-response no better than co-activation
    precisely in the canonical absorption case the proposal foregrounds. The assumptions section honestly flags the null,
    but a reviewer wants the mechanism de-risked before five downstream evals are run.
  suggested_action: >-
    Run a ~1-GPU-hour pilot on the first-letter task using the known absorbing latents (identifiable via the supervised diagnostic
    of Chanin et al. 2409.14507): measure whether the general latent and its absorbers actually have correlated content-response
    profiles across contexts, and report the correlation distribution vs a shuffled null. Separate predictions for splitting
    vs absorption explicitly. Only proceed to the full suite if the pilot shows above-null co-response in the absorption regime;
    otherwise pivot the headline to splitting-dominated concepts (toxicity) where the mechanism is sound.
- id: ''
  category: scope
  severity: major
  description: >-
    OVER-SCOPED: five evaluation axes, each nearly a standalone paper. EVAL-1 (classification under shift + low-Jaccard controlled
    experiment), EVAL-2 (steering with matched-effect side-effect measurement + bootstrap CIs), EVAL-3 (model-diffing), plus
    the knowledge graph and the absorption-recovery study — across three datasets (toxicity, bias_in_bios, first-letter) and
    a width/layer robustness axis — on a single GPU under a <$10 budget. Steering side-effect protocols (cf. AxBench, 2505.20063)
    and model-diffing each demand substantial, careful infrastructure. Attempting all five risks five underpowered results
    and no decisive claim. A sibling line of work on slot-conditional exclusivity shows how much effort each single axis consumes.
  suggested_action: >-
    Pick ONE headline (recommend classification robustness-gap under pre-registered shift, anchored by the low-Jaccard 'wins
    where it differs' controlled experiment). Demote steering and model-diffing to explicitly-labeled secondary/stretch with
    a single illustrative case each, and state up front that they are confirmatory not load-bearing. Pre-register the primary
    split, metric, and decision rule.
- id: ''
  category: methodology
  severity: major
  description: >-
    TENSION BETWEEN THE SURFACE-INVARIANCE FILTER AND THE ABSORPTION-RECOVERY GOAL. The method pre-filters to latents that
    are surface-invariant before clustering. But absorbed latents are frequently token-aligned / surface-specific by construction
    (the 'lion' latent fires on the surface token 'lion'). A strict surface-invariance screen may therefore discard exactly
    the absorbed member latents the method aims to recover, collapsing units back toward surface-invariant generalists. Conversely,
    on the first-letter task the 'surface form' is largely the spelling itself, so the surface/content separation may be ill-defined.
  suggested_action: >-
    Reconcile explicitly: either (a) apply surface-invariance at the UNIT level (the pooled unit should be surface-invariant)
    rather than filtering individual member latents, allowing surface-specific absorbed children into a unit whose aggregate
    is invariant; or (b) define surface flips as content-preserving token substitutions (synonyms, morphological/format changes)
    and show absorbed token-latents survive. Report an ablation with the surface-invariance filter on vs off to quantify what
    it costs in recall.
- id: ''
  category: evidence
  severity: major
  description: >-
    COUNTERFACTUAL-GENERATION QUALITY AND CIRCULARITY. LLM-generated minimal pairs (detoxify/retoxify, profession/pronoun
    swap, template fills) will themselves perturb many surface tokens and may leak or partially fail to flip the target concept;
    the resulting content-response delta then conflates content change with residual surface change — the very confound the
    method claims to remove. Separately, the proposed 'cheaper corroborating' activation-space counterfactual (a concept direction)
    is circular if that direction is derived from the same SAE latents being grouped.
  suggested_action: >-
    Add a counterfactual-quality validation: LLM-judge (or small human audit) that each pair flips content and preserves surface,
    and report pass rates and sensitivity of results to pair quality. Ensure the activation-space counterfactual is derived
    from an INDEPENDENT source (e.g., a held-out diff-of-means direction on disjoint data), and report results with text-only
    counterfactuals as the primary so the headline does not depend on a potentially circular activation edit.
- id: ''
  category: novelty
  severity: minor
  description: >-
    A few high-relevance citations are missing or under-engaged, which a knowledgeable reviewer would flag. The 'reliable
    unit of analysis' framing should engage 'Sparse Autoencoders Do Not Find Canonical Units of Analysis' (ICLR 2025), which
    is directly about SAE units and stitching. AxBench (2501.17148) is the empirical backbone of the motivation and should
    be cited explicitly (not just alluded to). For the steering eval, 'SAEs Are Good for Steering — If You Select the Right
    Features' (2505.20063) is a direct counterpoint to AxBench. Feature Hedging (Chanin, 2505.11756) explains why correlated
    features get absorbed and supports the mechanism.
  suggested_action: >-
    Add and engage these four references in related work / eval design. For the canonical-units paper, contrast your behavioral
    (counterfactual co-response) unit definition with their stitching/geometry view. Cite AxBench as the source of the diff-of-means-beats-SAE
    finding that sets your bar.
- id: ''
  category: scope
  severity: minor
  description: >-
    MODEL-DIFFING (EVAL-3) IS THE WEAKEST LINK AND UNDER-SPECIFIED. 'Sanity-checked against known fine-tuning effects (e.g.
    refusal/safety shifts)' lacks a concrete ground truth or validation protocol; without one, 'which units shift' is unfalsifiable
    and reads as a qualitative demo. Also, recomputing units on two models requires the counterfactual co-response pipeline
    to be stable enough that unit changes reflect the model, not estimation noise.
  suggested_action: >-
    Either demote to a clearly-labeled qualitative illustration, or give it a concrete oracle: diff against a model with a
    KNOWN injected/finetuned behavior (e.g., a published safety/refusal fine-tune or a deliberately fine-tuned variant) and
    show the surfaced unit changes recover it, with a stability/null floor distinguishing real shifts from re-estimation noise.
- id: ''
  category: clarity
  severity: minor
  description: >-
    FIRST-LETTER IS THE MECHANISM TESTBED, NOT A SAFETY TASK, but the success criteria headline is 'safety-attribute classification'.
    The proposal mixes the clean controlled absorption case (spelling) with the safety payoff (toxicity, bias_in_bios) without
    flagging that the spelling mechanism may not transfer to the messier safety regime — and bias_in_bios in particular is
    known to be SAE-unfavorable / strongly diff-of-means-favorable, so a null there should be anticipated and scoped, not
    treated as a failure of the method.
  suggested_action: >-
    State explicitly that first-letter is the clean mechanism testbed (where absorption is verifiable) and toxicity/bias_in_bios
    are the safety payoff, and pre-register the expectation that bias_in_bios may be a hard/null case. Frame a scoped result
    (works on toxicity/spelling, null on bias_in_bios) as a boundary finding rather than a failure.
score: 6
confidence: 4
relation_type:
relation_rationale: ''
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

### [2] HUMAN-USER prompt · 2026-06-17 11:56:55 UTC

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

### [3] SKILL-INPUT — aii-web-tools · 2026-06-17 11:57:25 UTC

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
