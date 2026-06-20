# review_hypo — create_idea

> Phase: `hypo_loop` · round 2 · Substep: `review_hypo`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave the agent(s) in this substep — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `review_hypo` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-17 12:03:52 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A hypothesis reviewer (Step 2.2: REVIEW_HYPO)

Pipeline: GEN_HYPO → REVIEW_HYPO (you) → INVENTION_LOOP → GEN_PAPER_REPO

You review a hypothesis BEFORE any experiments run. Catch problems early.

Rigorous pre-flight check → saves compute. Rubber-stamping → wasted pipeline run.
</your_role>
</ai_inventor_context>

ROLE: You are a very experienced and critical conference reviewer.
Your expertise spans the domain of the hypothesis under review.
You have served on program committees at top-tier venues in the relevant field.

TASK: Perform a deep and honest review (at the level of a top-tier venue submission) of
this research hypothesis BEFORE any experiments have been run.

GOAL: Your review feeds directly back to the hypothesis author. The objective is to
maximize the overall review score in subsequent rounds. Every piece of feedback you
give should be written with this goal in mind — prioritize the critiques and suggestions
that would produce the largest score improvement if addressed. Don't waste the author's
iteration budget on low-impact polish when there are score-blocking issues to fix.

STRENGTHS AND WEAKNESSES: Provide a thorough assessment touching on each of these:
(a) Originality: Are the ideas new? Novel combination of known techniques? Clear
    differentiation from prior work? Is related work adequately cited?
(b) Quality: Is the proposal technically sound? Are claims well supported? Is the
    methodology appropriate? Are the authors honest about limitations?
(c) Clarity: Is the hypothesis clearly written and well organized? Does it provide
    enough information for an expert to understand and evaluate it?
(d) Significance: Are the expected results important? Would others build on this?
    Does it address a meaningful problem better than prior work?

SUPPLEMENTARY SCORES: Rate each on a 1-4 scale.
Soundness (1-4) — soundness of the technical claims and proposed methodology:
  4: excellent  3: good  2: fair  1: poor
Presentation (1-4) — quality of writing, clarity, and contextualization relative to prior work:
  4: excellent  3: good  2: fair  1: poor
Contribution (1-4) — quality of the overall contribution, importance of questions asked,
originality of ideas, value to the broader research community:
  4: excellent  3: good  2: fair  1: poor

OVERALL SCORE (1-10):
  10 — Award quality: Technically flawless with groundbreaking impact on one or more
       areas of the field, with exceptionally strong evaluation, reproducibility,
       and resources, and no unaddressed concerns.
   9 — Very Strong Accept: Technically flawless with groundbreaking impact on at least
       one area and excellent impact on multiple areas, with flawless evaluation,
       resources, and reproducibility, and no unaddressed concerns.
   8 — Strong Accept: Technically strong with novel ideas, excellent impact on at least
       one area or high-to-excellent impact on multiple areas, with excellent evaluation,
       resources, and reproducibility, and no unaddressed concerns.
   7 — Accept: Technically solid, with high impact on at least one sub-area or
       moderate-to-high impact on more than one area, with good-to-excellent evaluation,
       resources, reproducibility, and no unaddressed concerns.
   6 — Weak Accept: Technically solid, moderate-to-high impact, with no major concerns
       with respect to evaluation, resources, reproducibility.
   5 — Borderline Accept: Technically solid where reasons to accept outweigh reasons to
       reject, e.g., limited evaluation. Use sparingly.
   4 — Borderline Reject: Technically solid where reasons to reject, e.g., limited
       evaluation, outweigh reasons to accept. Use sparingly.
   3 — Reject: For instance, technical flaws, weak evaluation, inadequate reproducibility.
   2 — Strong Reject: For instance, major technical flaws, poor evaluation, limited
       impact, poor reproducibility.
   1 — Very Strong Reject: For instance, trivial results or unaddressed concerns.

CONFIDENCE (1-5):
  5: Absolutely certain. Very familiar with related work, checked details carefully.
  4: Confident but not absolutely certain. Unlikely you misunderstood something.
  3: Fairly confident. Possible you missed some related work or details.
  2: Willing to defend your assessment, but quite likely missed central aspects.
  1: Educated guess. Not in your area or difficult to evaluate.

For each dimension, provide a list of specific improvements:
- WHAT needs to change
- HOW to change it (concrete enough for the author to act on immediately)
- EXPECTED SCORE IMPACT: how much would fixing this raise the overall score?

REVIEW PRINCIPLES:
- Be specific and actionable — vague critique is useless
- Ground your review in evidence — search for existing work, accepted papers, known results
- Rank critiques by score impact — address the biggest score blockers first
- Distinguish major issues (would waste compute if not fixed) from minor issues (polish)
- Acknowledge genuine strengths — don't be negative for its own sake
- Compare against the bar set by accepted papers at top-tier venues
- Flag fatal flaws that would make experiments pointless if not addressed first

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

<role>
You are a very experienced and critical conference reviewer specialized in the domain of the work under review.
You have reviewed for top-tier venues in the relevant field. Your reviews are known for
being thorough, fair, and grounded in the actual state of the field.
</role>

<hypothesis>
kind: hypothesis
title: >-
  Counterfactual Co-Response Grouping: Reliable SAE Concept Units from Interventional Co-Sensitivity, Tested Against Counterfactually-Matched
  Probes
hypothesis: |-
  FALSIFIABLE CORE CLAIM (the one thing this paper rises or falls on): grouping sparse-autoencoder (SAE) latents by their CORRELATED RESPONSE TO CONTENT COUNTERFACTUALS (interventional co-sensitivity) is a strictly better unit-formation signal than observational co-activation or decoder geometry, but only when, and because, the SAE's failure modes corrupt the observational signals while leaving the interventional one intact.

  PRIMARY pre-registered headline (single decisive test): counterfactual co-response units beat (i) the best raw single latent, (ii) co-activation / decoder-geometry clusters, and CRITICALLY (iii) a difference-of-means probe AND a linear probe that are trained on the SAME counterfactual minimal-pair deltas the units are built from, on safety-attribute classification, with the advantage appearing and GROWING under a pre-registered surface / distribution shift split. The matched probes are the load-bearing baselines: counterfactual matching strips surface confounds for ANY estimator, so if the matched diff-of-means closes the shift gap, we report honestly that the finding is 'counterfactual supervision helps' rather than 'SAE grouping helps' (a different, still-publishable result).

  The grouping signal has TWO mechanism-specific signatures that we predict and test separately rather than conflating: (A) FEATURE SPLITTING / HEDGING is the SOUND regime and the headline (toxicity): when content is minimally toxified or detoxified, a concept's sub-latents rise and fall TOGETHER across contexts (positively correlated content-response on overlapping support), so a DiffCoEx-style correlation-of-response clustering recovers the unit; Feature Hedging (Chanin et al. 2505.11756) shows correlated features are exactly what SAEs entangle, so this regime is mechanistically expected. (B) FEATURE ABSORPTION is the CONTROLLED STRESS-TEST (first-letter spelling): the general latent is silent precisely where a specific absorber fires, so under a content flip in those contexts the general latent's delta is approximately zero while the absorber's is large; their per-context response profiles therefore have DISJOINT support and are near-uncorrelated. Here the correct unit-formation signal is NOT correlation but COMPLEMENTARY COVERAGE: the group's POOLED (max-over-members) content-response tracks the concept flip across all contexts even though no single member does and members never co-fire. Both signatures are unified as 'members that jointly track the content perturbation at the UNIT level'; positive correlation is the splitting-only special case and complementary coverage is the absorption case. Whether absorbed latents actually exhibit above-null complementary co-response is de-risked by a cheap pilot BEFORE the full suite, and the headline lives in whichever regime the pilot confirms.

  Surface invariance is enforced at the UNIT (pooled) level, not on individual member latents, resolving the tension that absorbed members are themselves token-/surface-specific: surface-specific absorbed children are admitted into a unit whose AGGREGATE is paraphrase-invariant. Concretely we claim: (1) units recover concept recall that absorption/splitting destroy at the single-latent level; (2) content-co-response clusters have LOW Jaccard overlap with co-activation/geometry clusters AND win specifically on the members where they differ (the mechanistic backbone of the headline); (3) units beat the counterfactually-matched probes under shift. Steering side-effects and model-diffing are explicitly SECONDARY confirmatory checks (one illustrative case each), not load-bearing. A clean null — absorbed/split latents neither co-respond nor complementarily cover under the concept intervention — is itself a publishable mechanism-level finding about how SAEs (mis)represent concepts.
motivation: |-
  Single SAE latents are unreliable units of analysis. Feature absorption (a general concept's latent silently fails to fire when a more specific latent takes over its tokens; Chanin et al. 2409.14507), feature splitting (one concept fragments across many latents), feature hedging (correlated features get merged into one latent in narrow SAEs; Chanin et al. 2505.11756), and the demonstration that SAEs do not find canonical, atomic units at all ('Sparse Autoencoders Do Not Find Canonical Units of Analysis', ICLR 2025, 2502.04878) all say the same thing: no single latent reliably tracks a concept. AxBench (ICML 2025 spotlight, 2501.17148) makes the stakes concrete — plain difference-of-means and prompting beat raw-latent SAE methods on both concept detection and steering — so the bar any SAE-grouping method must clear is 'beat diff-of-means', and beating it on raw labeled data is not enough because diff-of-means itself can be made shift-robust with counterfactual data.

  Every existing post-hoc grouping method relies on OBSERVATIONAL signals — which latents fire together (co-activation 'feature families') or which decoders point in similar directions (geometry). But absorption is exactly the regime where observational signals break by construction: the absorbed general latent and the absorbing specific latents are mutually exclusive in firing, so co-activation clustering provably cannot group them, and their decoders need not be cosine-similar. This is a structural blind spot, not a tuning problem. Feature Hedging supplies the mechanistic 'why': both absorption and hedging are CAUSED by feature correlation/hierarchy — precisely the structure an INTERVENTIONAL probe (perturb the concept, watch what moves together) is built to expose.

  Systems biology faced the identical obstacle and solved it: co-regulated genes are often NOT co-expressed at baseline and reveal their shared regulation only under perturbation, which is why differential co-expression methods (DiffCoEx, WGCNA) cluster genes by their CORRELATED RESPONSE TO A PERTURBATION rather than by baseline co-expression. Transferring that principle, an input content-edit is the 'perturbation' and SAE latents are the 'genes'. The pivotal scientific insight an interpretability expert would not reach for is that SAE absorption/splitting are structurally the same obstacle that defeats baseline co-expression in biology, so the field's reliance on observational co-activation/geometry is the wrong instrument and interventional co-response is the matched one. If correct, this gives a training-free, single-GPU, human-auditable way to turn off-the-shelf public SAEs (Gemma Scope) into reliable units for the safety-critical tasks people actually want — robust attribute classification first and foremost — plus an auditable feature-level knowledge graph of concepts and their conditioning environments.
assumptions:
- >-
  MINIMAL PAIRS ARE OBTAINABLE AT HIGH QUALITY AND LOW COST, NON-CIRCULARLY. For the toxicity headline we use ParaDetox (s-nlp,
  ACL 2022), a HUMAN-WRITTEN parallel toxic<->neutral corpus, so the primary content-flip pairs do not depend on LLM generation
  at all. Where LLM-generated pairs are used (additional toxicity, bias_in_bios pronoun/profession swaps, first-letter substitutions;
  OpenRouter, well under the $10 budget), every pair is passed through an LLM-judge that scores whether content flipped and
  surface was preserved, and we report pass rates plus sensitivity of all results to the pair-quality threshold. Text-only
  counterfactuals are the PRIMARY signal; the corroborating activation-space content edit, if used, is derived from an INDEPENDENT
  held-out diff-of-means direction on DISJOINT data, never from the SAE latents being grouped, so there is no circularity.
- >-
  THE MECHANISM HOLDS IN AT LEAST THE SPLITTING REGIME, AND IS TESTED SEPARATELY FROM ABSORPTION. For feature splitting/hedging
  (toxicity) we assume sub-latents of a concept show positively correlated content-response across contexts (sound per Feature
  Hedging). For feature absorption (first-letter) we make the WEAKER, pilot-gated assumption that the general latent and its
  absorbers exhibit COMPLEMENTARY coverage (mutually-exclusive support whose pooled response tracks the flip), NOT correlation.
  A cheap pilot using the supervised absorption diagnostic of Chanin et al. (2409.14507) tests this before the full suite;
  if absorption shows neither correlated nor complementary above-null co-response, the headline stays in the splitting regime
  and the absorption result is reported as an honest mechanism-level null.
- >-
  Off-the-shelf Gemma Scope SAEs on Gemma-2-2b expose latent counterfactual responses measurable above noise on a single GPU
  for a few thousand minimal pairs, and the chosen attributes have enough labeled/templatable data to build minimal pairs
  and held-out, surface-shifted test splits.
- >-
  SURFACE-FORM CONFOUNDING IS MATERIAL AT THE UNIT LEVEL. Individual latents partly entangle a concept with the surface forms
  it co-occurs with, so enforcing surface invariance on the POOLED unit yields units that generalize where single latents
  and distributionally-naive probes do not. If surface confounding turns out immaterial, units collapse toward the counterfactually-matched
  probes and the method yields no gain over them — which is itself the pre-registered boundary finding, not a hidden failure.
investigation_approach: |-
  STEP 0 - DE-RISKING PILOT (run first, ~1 GPU-hour, gates everything downstream). On the first-letter task, use the supervised absorption diagnostic of Chanin et al. (2409.14507) to identify the known general 'starts-with-L' latent and its absorbing token-latents. Build first-letter content-flip pairs (swap an L-word for a non-L-word in matched contexts) and measure: (a) do the general latent and absorbers show CORRELATED content-response (expected low/disjoint), and (b) do they show COMPLEMENTARY coverage (pooled max-over-members response tracks the flip where individual members have holes)? Report the correlation and coverage distributions against a shuffled-pair null. Decision rule: proceed with absorption as a headline regime only if complementary coverage is above null; otherwise keep the headline in the splitting/toxicity regime and report absorption as an honest null. This pre-empts spending compute on downstream evals if the central premise fails.

  DATA & CONCEPTS. (1) TOXICITY = primary safety headline (splitting/hedging regime): ParaDetox human-written toxic<->neutral pairs for content-flips, plus Jigsaw/civil_comments for IID and a pre-registered SURFACE/DISTRIBUTION SHIFT test split (e.g., train on one comment source/style, test on another; paraphrase-shifted held-out set). (2) FIRST-LETTER spelling = clean controlled MECHANISM testbed (absorption regime; explicitly NOT a safety task) where absorption is verifiable against the supervised oracle. (3) bias_in_bios = pre-registered EXPECTED-HARD / likely-null case (known SAE-unfavorable, strongly diff-of-means-favorable); a null here is framed as a scope boundary, not a failure. Per task we give a one-line operational content/surface definition: for toxicity, content-flip = toxify/detoxify (ParaDetox), surface-flip = content-preserving paraphrase; for first-letter, content-flip = change whether the word starts with the target letter, surface-flip = a DIFFERENT same-letter word / capitalization / context paraphrase (keeps 'starts-with-L' true, changes surface) so absorbed token-latents can still be members.

  COUNTERFACTUAL SIGNAL. Encode every text and its counterfactual with a frozen Gemma Scope residual-stream SAE (layer ~12, width 16k canonical; width/layer as a robustness axis). Per latent, content-response on a pair = delta(activation) under the content-flip; surface-response = delta under the surface-flip. Aggregate into per-latent response profiles across contexts.

  GROUPING (unsupervised given the perturbation). Cluster latents on a content-response affinity that rewards BOTH (i) positive co-response (splitting) and (ii) complementary coverage of the SAME content flip (absorption) — unified as 'members that jointly track the perturbation at the unit level'. Use DiffCoEx-style differential-correlation clustering for (i) and a greedy/agglomerative coverage-maximizing merge (increase pooled content-flip coverage while minimizing per-context member overlap) for (ii). Enforce surface invariance at the POOLED UNIT level (pooled unit shows low surface-response), NOT on individual members; report an ABLATION with the surface-invariance filter on vs off and member-level vs unit-level, to quantify what it costs in recall. Emit human-auditable unit definitions (member latents, their logit-lens tokens, conditioning contexts) and directed specialization edges (a member responsive only in a sub-context = absorbed/split child) = a feature-level knowledge graph.

  BASELINES (matched baselines are PRIMARY). (a) Best raw single latent (any width); (b) observational co-activation clustering / feature families; (c) decoder-geometry clustering; (d) COUNTERFACTUALLY-MATCHED difference-of-means probe = diff-of-means on the SAME paired residual-stream deltas; (e) COUNTERFACTUALLY-MATCHED linear probe trained on the same paired activations; (f) standard (unmatched) diff-of-means / linear probe on raw labeled data. (d) and (e) are the kill-shot baselines and are pre-registered as the bar to beat.

  EVAL 1 - CLASSIFICATION ROBUSTNESS GAP (the single headline). Unit-pooled activation (max/sum over members) as a classifier on IID and on the pre-registered SHIFT split; report F1/AUC and recall on absorbed/held-out-surface cases; headline metric = robustness gap under shift vs ALL baselines including matched probes. Mechanistic backbone = controlled experiment showing co-response clusters have low Jaccard with co-activation/geometry clusters AND win specifically on the differing members. Include CLUSTER-STABILITY statistics: bootstrap over minimal pairs reporting adjusted Rand / Jaccard agreement across resamples, a shuffled-pair null for the co-response affinity matrix, and sensitivity to the number of pairs per concept.

  SECONDARY / STRETCH (clearly labeled, confirmatory not load-bearing, one illustrative case each). STEERING: steer with the unit's shared content-response direction vs best single latent vs matched diff-of-means; measure on-target effect and side-effects (KL on unrelated prompts, fluency) at MATCHED on-target effect with bootstrap CIs; engage 'SAEs Are Good for Steering -- If You Select the Right Features' (2505.20063) feature-selection as a comparator and AxBench's protocol. MODEL-DIFFING: demoted to a concrete-oracle check — diff a base model against a variant with a KNOWN injected/fine-tuned behavior and test whether surfaced unit changes recover it, with a stability/null floor distinguishing real shifts from re-estimation noise (else reported as a qualitative illustration).

  HONEST FAILURE-MODE REPORTING. Dependence on counterfactual quality (with pass rates); concepts with no surface-invariant co-responding/complementary group; regimes where co-response collapses to co-activation (no gain); cases where matched diff-of-means still wins under shift (reframes the contribution); compute cost; sensitivity to SAE layer/width; bias_in_bios expected boundary-null.
success_criteria: >-
  CONFIRMED if (pre-registered): (1) on the toxicity headline, content-co-response units beat the best raw single latent AND
  the counterfactually-MATCHED diff-of-means and matched linear probe on classification, with the advantage positive and GROWING
  under the pre-registered surface/distribution shift split (bootstrap CIs); (2) units recover concept recall on absorbed/held-out
  cases that observational co-activation clustering measurably misses, with the controlled experiment showing co-response
  clusters differ from co-activation/decoder clusters (low Jaccard, above the stability/shuffled-pair null floor) AND outperform
  them specifically on the differing members; (3) the de-risking pilot confirms above-null co-response (correlated for splitting
  and/or complementary-coverage for absorption); (4) cluster assignments are stable across bootstrap resamples (adjusted Rand
  / Jaccard well above the shuffled-pair null) and the knowledge-graph specialization edges agree with the supervised absorption
  diagnostic (2409.14507) as a partial oracle on first-letter. SECONDARY (confirmatory only): steering with the unit direction
  achieves lower KL side-effects than best-single-latent and matched diff-of-means at matched on-target effect; model-diffing
  recovers a known injected behavior above its null floor. DISCONFIRMED / HONEST NEGATIVE if: content-co-response grouping
  gives no advantage over observational co-activation grouping (co-response ~ co-activation); OR it fails to beat raw latents
  AND the matched probes even under shift; OR the matched diff-of-means closes the shift gap (reframes the finding as 'counterfactual
  supervision helps', still publishable but a different paper); OR counterfactual responses are too noisy to cluster stably
  (ARI ~ null); OR the pilot shows absorbed latents neither co-respond nor complementarily cover the concept intervention.
  A clean null on the pilot is itself a publishable mechanism-level finding about how SAEs represent concepts. bias_in_bios
  is pre-registered as a likely boundary-null and a null there is scoped, not counted as method failure.
related_works:
- >-
  AxBench: Steering LLMs? Even Simple Baselines Outperform Sparse Autoencoders (Wu et al., ICML 2025 spotlight, 2501.17148):
  large-scale benchmark on Gemma-2-2B/9B showing that for concept DETECTION representation methods like difference-in-means
  perform best and SAEs are not competitive, and likewise for steering. This is the empirical backbone of our motivation and
  sets our bar: any SAE-grouping method must beat diff-of-means. We differ by making diff-of-means MAXIMALLY fair (counterfactually
  matched on the same minimal pairs) and pre-registering the win condition as a shift-robustness gap against that matched
  baseline, rather than against distributionally-naive probes.
- >-
  Sparse Autoencoders Do Not Find Canonical Units of Analysis (Bussmann et al., ICLR 2025, 2502.04878): uses SAE stitching
  (incompleteness) and meta-SAEs (non-atomicity) to argue SAEs do not learn canonical units. This is the strongest statement
  of the problem we address, but its remedy is geometric/training-based (stitching, meta-SAE decomposition). We propose a
  BEHAVIORAL unit defined by counterfactual co-response and unit-level surface invariance, evaluated on concrete downstream
  classification, not a geometry/stitching view.
- >-
  Feature Hedging / Correlated Features Break Narrow Sparse Autoencoders (Chanin, Dulka, Garriga-Alonso, 2505.11756): shows
  narrow SAEs merge correlated features into one latent (MSE-driven hedging), and contrasts hedging (polysemantic mixtures,
  one feature in the SAE) with absorption (gerrymandered latents, sparsity-driven, both features tracked). We use this as
  the mechanistic 'why' for our signal — both pathologies are CAUSED by feature correlation/hierarchy, exactly what an interventional
  perturb-and-watch probe exposes — and to justify treating splitting and absorption as DISTINCT co-response signatures rather
  than conflating them.
- >-
  A is for Absorption: Studying Feature Splitting and Absorption in Sparse Autoencoders (Chanin et al., 2409.14507, NeurIPS):
  supervised pairwise DIAGNOSTIC of absorption on first-letter using a logistic-probe direction + decoder-cosine + ablation
  to find the single absorbing latent. We use it as a partial ORACLE to identify known absorbers for our de-risking pilot
  and to validate knowledge-graph specialization edges, but our contribution is an UNSUPERVISED GROUPING method (interventional
  co-response) that repairs absorption into a usable unit rather than merely detecting it.
- >-
  SAEs Are Good for Steering -- If You Select the Right Features (Arad et al., 2505.20063, EMNLP 2025): shows SAE steering
  becomes competitive with supervised methods after filtering features by an output-score, a direct counterpoint to AxBench.
  We engage it as the steering-eval comparator; its selection is per-feature by output effect (feature->output), whereas our
  units are formed by INPUT-intervention co-response and steering is only a secondary confirmatory check, not our headline.
- >-
  Co-activation feature families and graph-regularized SAEs (Disentangling Dense Embeddings 2408.00657; GSAE 2512.06655; Sparse
  Feature Coactivation Reveals Causal Semantic Modules 2506.18141): group SAE features by OBSERVATIONAL co-activation and/or
  decoder geometry, sometimes baking the graph into retraining. By construction these cannot group a concept's absorbed/split
  latents, which are mutually exclusive in firing. We use the opposite, interventional signal (correlated change, or complementary
  coverage, under a content counterfactual), training-free on frozen public SAEs.
- >-
  Meta-SAEs and Matryoshka SAEs (Showing SAE Latents Are Not Atomic, 2503.17547): expose hierarchy by decomposing decoder
  directions with a learned meta-SAE or by RETRAINING nested dictionaries. They rely on geometry/training and target atomicity.
  We need no retraining and no decoder-geometry assumption; our unit is defined behaviorally by counterfactual co-response
  + unit-level surface invariance.
- >-
  Counterfactual Invariance to Spurious Correlations (Veitch, D'Amour, Yadlowsky, Eisenstein, NeurIPS 2021, 2106.00545) and
  contrastive SAE steering (FGAA 2501.09929; Denoising Concept Vectors with SAEs 2505.15038): formalize counterfactual invariance
  for robust PREDICTORS, or compute a single contrastive SAE-space steering vector. We import counterfactual invariance and
  minimal pairs as a GROUPING signal that clusters many latents into concept units, not as a single predictor or single steering
  vector, and we make the matched-counterfactual probe a baseline rather than the method.
- >-
  Differential co-expression / perturbation co-response module discovery in systems biology (DiffCoEx, BMC Bioinformatics
  2010; WGCNA): cluster genes by their CORRELATED RESPONSE TO A PERTURBATION rather than baseline co-expression, because co-regulated
  genes are often not co-expressed at baseline. This is the methodological root being transferred; to our knowledge it has
  never been applied to SAE/LLM features. Our novel scientific claim is that the same baseline-vs-perturbation distinction
  explains and repairs SAE absorption/splitting, with the input content counterfactual as the 'perturbation', extended with
  a complementary-coverage variant for the mutually-exclusive absorption case.
- >-
  Mutual-exclusivity / Ising-coupling and slot-conditional exclusivity grouping of SAE latents (e.g. Bhalla et al. global
  Ising coupling; slot-conditional exclusivity studies): group latents by negative co-occurrence (they do not fire together).
  Exclusivity establishes that two latents do not co-fire but not that they belong together, and such methods have struggled
  to deliver downstream gains. We supply the missing POSITIVE interventional signal (correlated co-response for splitting;
  complementary coverage of the same content flip for absorption) that unites mutually-exclusive variants, and explicitly
  test whether it succeeds where exclusivity alone does not.
- >-
  Domain-Filtered Knowledge Graphs from Sparse Autoencoder Features (2604.23829): builds an internal knowledge graph from
  SAE features using contrastive corpus filtering, co-occurrence, and decoder geometry — i.e. purely OBSERVATIONAL signals.
  Our feature-level knowledge graph is built from the INTERVENTIONAL co-response/complementary-coverage grouping instead,
  so its edges encode conditioning environments and specialization (absorbed/split children) invisible to observational co-occurrence.
inspiration: >-
  A Level-3 (methodological) cross-field transfer from systems biology's differential co-expression / perturbation co-response
  module discovery (DiffCoEx, WGCNA): cluster units by their CORRELATED RESPONSE TO A PERTURBATION, not by baseline co-expression,
  because co-regulated genes frequently are not co-expressed until perturbed. Mapping genes->SAE latents and a chemical/genetic
  perturbation->a content counterfactual on the input gives the core mechanism. This is fused with causal ML's counterfactual
  invariance to spurious correlations (Veitch et al. 2021) and minimal-pair counterfactuals from NLP, which supply the surface-vs-content
  axis and the robustness-under-shift framing. The revision adds a second cross-field idea — COMPLEMENTARY COVERAGE (a 'module
  eigengene tracks the perturbation even when individual members have gaps', generalized to mutually-exclusive members) —
  to handle feature absorption, where members have disjoint support and plain correlation fails. The unifying insight an interpretability
  expert would not reach for: SAE failure modes (absorption, splitting, hedging) are structurally the same obstacle that defeats
  baseline co-expression in biology — the right members are invisible at baseline and visible only under perturbation — so
  the field's reliance on observational co-activation/geometry is the wrong instrument, and interventional co-response is
  the matched one. Feature Hedging (2505.11756) supplies the mechanistic grounding that both pathologies arise from feature
  correlation/hierarchy.
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
    holes and is unreliable. Per Feature Hedging, absorption learns 'gerrymandered' latents and keeps both features in the
    SAE.
- term: Feature splitting / feature hedging
  definition: >-
    Splitting = one concept fragments across many latents (more so at larger width). Hedging (Chanin et al. 2505.11756) =
    a narrow SAE merges correlated features into one latent, driven by reconstruction loss. Both arise from feature correlation/hierarchy
    and make single latents unreliable; this is the 'sound' regime where members co-respond positively to a content flip.
- term: Counterfactual minimal pair
  definition: >-
    Two inputs differing in exactly one targeted way: a content-flip pair changes whether a concept is present while holding
    surface form roughly fixed; a surface-flip pair paraphrases/rewrites surface while holding content fixed. Human-written
    pairs (ParaDetox) are used where available; LLM-generated pairs are LLM-judge-validated for content-flip and surface-preservation.
- term: Counterfactual content-response (of a latent)
  definition: >-
    The change in a latent's activation between a content-flip pair (concept added minus removed), measured per context; the
    vector of these changes across many contexts is the latent's content-response profile.
- term: Interventional co-sensitivity / co-response
  definition: >-
    The criterion that latents belong to the same concept unit if they jointly track the content perturbation across contexts,
    even if their baseline activations never co-occur. Realized in two signatures: positive correlation of content-response
    profiles (splitting) and complementary coverage (absorption).
- term: Complementary coverage
  definition: >-
    The absorption-regime grouping signal: member latents respond to the SAME content flip on DISJOINT context supports (mutually
    exclusive), so no single member tracks the concept everywhere, but the group's POOLED (max-over-members) content-response
    covers the concept flip across all contexts. The interventional analogue of a module eigengene tracking the perturbation
    despite per-member gaps.
- term: Unit-level surface invariance
  definition: >-
    Surface invariance enforced on the POOLED unit (the aggregate shows little response to surface-flip counterfactuals) rather
    than on each member latent, so surface-/token-specific absorbed children can be admitted into a unit whose aggregate is
    paraphrase-robust. Resolves the tension between filtering for invariance and recovering token-aligned absorbed latents.
- term: Counterfactually-matched probe
  definition: >-
    A difference-of-means probe or linear probe trained on the SAME paired residual-stream deltas from the minimal pairs the
    units are built from (not on raw labeled data). It is the primary kill-shot baseline: counterfactual matching strips surface
    confounds for any estimator, so units must beat the matched probe under shift to attribute the gain to SAE grouping rather
    than to counterfactual supervision.
- term: Differential co-expression (analogy)
  definition: >-
    A systems-biology family of methods (DiffCoEx, WGCNA) that clusters genes by how their expression co-varies under a perturbation
    rather than at baseline, revealing co-regulated modules invisible to baseline co-expression — the methodological template
    transferred here to SAE latents.
- term: Reliable unit of analysis
  definition: >-
    A human-auditable group of SAE latents that tracks a concept dependably across surface variation — recovering recall that
    absorption/splitting destroy at the single-latent level — and is reusable as a classifier (headline), and secondarily
    for steering and model-diffing.
summary: >-
  SAE latents that encode the same concept are often mutually exclusive in firing (because of feature absorption, splitting,
  and hedging), so observational co-activation and decoder geometry cannot group them; grouping latents instead by how they
  jointly track a content counterfactual — positively correlated co-response for splitting, complementary coverage for absorption
  — while requiring surface invariance at the pooled-unit level yields training-free, auditable concept units whose headline
  test is beating counterfactually-MATCHED difference-of-means/linear probes on safety-attribute classification with a widening
  advantage under surface shift.
</hypothesis>

<review_context>
No experiments have been run yet — evaluate the hypothesis purely on its merits.
</review_context>

<previous_hypothesis>
The hypothesis from the PREVIOUS iteration (before the revision under review).
Use this to classify how the current hypothesis relates to it (see the H↔H
edge instructions in the task).

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

<previous_review>
Critiques from the previous review. Check which ones have been addressed
in the revised hypothesis. Do NOT re-raise critiques that have been adequately fixed.
Only re-raise if the fix is insufficient.

- [MAJOR] (methodology) BASELINE CONFOUND (likely reviewer kill-shot). The headline claim is that units beat difference-of-means and linear probes 'with the gap widening under surface/distribution shift' because counterfactual matching strips the surface confound. But counterfactual matching strips surface confounds for ANY estimator, not just SAE-latent units. As written, the comparison risks pitting counterfactually-matched SAE units against distributionally-naive diff-of-means/probes trained on raw labeled data — so any shift-robustness gain could be attributed to the counterfactual training data, not to grouping SAE latents. AxBench (2501.17148, ICML 2025 spotlight) already shows plain diff-of-means is the strongest concept-detection baseline and beats SAE methods, so this baseline must be made maximally fair or the contribution evaporates.
  Action: Add as PRIMARY baselines: (a) a difference-of-means probe computed on the SAME minimal-pair deltas the units are built from, and (b) a linear probe trained on counterfactually-matched (paired) residual activations. Pre-register the claim as 'SAE co-response units beat the counterfactually-matched diff-of-means/probe under shift'. If the matched diff-of-means closes the gap, report that honestly — it reframes the finding as 'counterfactual supervision helps' rather than 'SAE grouping helps', which is still publishable but a different paper.
- [MAJOR] (rigor) CORE MECHANISM IS ASSERTED, NOT DEMONSTRATED, AND IS WEAKEST FOR ABSORPTION. The pivotal premise is that a concept's absorbed/split latents, while observationally exclusive, have CORRELATED counterfactual content-response across contexts. For feature splitting this is plausible (toxify a sentence → many toxicity sub-latents rise together). For feature absorption it is questionable: an absorbed general latent is SILENT in exactly the contexts the absorbing token-latent handles, so under a content flip in those contexts its delta-activation is ~0 while the absorber's is large — their across-context response profiles can be disjoint or anti-correlated rather than correlated, which would make co-response no better than co-activation precisely in the canonical absorption case the proposal foregrounds. The assumptions section honestly flags the null, but a reviewer wants the mechanism de-risked before five downstream evals are run.
  Action: Run a ~1-GPU-hour pilot on the first-letter task using the known absorbing latents (identifiable via the supervised diagnostic of Chanin et al. 2409.14507): measure whether the general latent and its absorbers actually have correlated content-response profiles across contexts, and report the correlation distribution vs a shuffled null. Separate predictions for splitting vs absorption explicitly. Only proceed to the full suite if the pilot shows above-null co-response in the absorption regime; otherwise pivot the headline to splitting-dominated concepts (toxicity) where the mechanism is sound.
- [MAJOR] (scope) OVER-SCOPED: five evaluation axes, each nearly a standalone paper. EVAL-1 (classification under shift + low-Jaccard controlled experiment), EVAL-2 (steering with matched-effect side-effect measurement + bootstrap CIs), EVAL-3 (model-diffing), plus the knowledge graph and the absorption-recovery study — across three datasets (toxicity, bias_in_bios, first-letter) and a width/layer robustness axis — on a single GPU under a <$10 budget. Steering side-effect protocols (cf. AxBench, 2505.20063) and model-diffing each demand substantial, careful infrastructure. Attempting all five risks five underpowered results and no decisive claim. A sibling line of work on slot-conditional exclusivity shows how much effort each single axis consumes.
  Action: Pick ONE headline (recommend classification robustness-gap under pre-registered shift, anchored by the low-Jaccard 'wins where it differs' controlled experiment). Demote steering and model-diffing to explicitly-labeled secondary/stretch with a single illustrative case each, and state up front that they are confirmatory not load-bearing. Pre-register the primary split, metric, and decision rule.
- [MAJOR] (methodology) TENSION BETWEEN THE SURFACE-INVARIANCE FILTER AND THE ABSORPTION-RECOVERY GOAL. The method pre-filters to latents that are surface-invariant before clustering. But absorbed latents are frequently token-aligned / surface-specific by construction (the 'lion' latent fires on the surface token 'lion'). A strict surface-invariance screen may therefore discard exactly the absorbed member latents the method aims to recover, collapsing units back toward surface-invariant generalists. Conversely, on the first-letter task the 'surface form' is largely the spelling itself, so the surface/content separation may be ill-defined.
  Action: Reconcile explicitly: either (a) apply surface-invariance at the UNIT level (the pooled unit should be surface-invariant) rather than filtering individual member latents, allowing surface-specific absorbed children into a unit whose aggregate is invariant; or (b) define surface flips as content-preserving token substitutions (synonyms, morphological/format changes) and show absorbed token-latents survive. Report an ablation with the surface-invariance filter on vs off to quantify what it costs in recall.
- [MAJOR] (evidence) COUNTERFACTUAL-GENERATION QUALITY AND CIRCULARITY. LLM-generated minimal pairs (detoxify/retoxify, profession/pronoun swap, template fills) will themselves perturb many surface tokens and may leak or partially fail to flip the target concept; the resulting content-response delta then conflates content change with residual surface change — the very confound the method claims to remove. Separately, the proposed 'cheaper corroborating' activation-space counterfactual (a concept direction) is circular if that direction is derived from the same SAE latents being grouped.
  Action: Add a counterfactual-quality validation: LLM-judge (or small human audit) that each pair flips content and preserves surface, and report pass rates and sensitivity of results to pair quality. Ensure the activation-space counterfactual is derived from an INDEPENDENT source (e.g., a held-out diff-of-means direction on disjoint data), and report results with text-only counterfactuals as the primary so the headline does not depend on a potentially circular activation edit.
- [MINOR] (novelty) A few high-relevance citations are missing or under-engaged, which a knowledgeable reviewer would flag. The 'reliable unit of analysis' framing should engage 'Sparse Autoencoders Do Not Find Canonical Units of Analysis' (ICLR 2025), which is directly about SAE units and stitching. AxBench (2501.17148) is the empirical backbone of the motivation and should be cited explicitly (not just alluded to). For the steering eval, 'SAEs Are Good for Steering — If You Select the Right Features' (2505.20063) is a direct counterpoint to AxBench. Feature Hedging (Chanin, 2505.11756) explains why correlated features get absorbed and supports the mechanism.
  Action: Add and engage these four references in related work / eval design. For the canonical-units paper, contrast your behavioral (counterfactual co-response) unit definition with their stitching/geometry view. Cite AxBench as the source of the diff-of-means-beats-SAE finding that sets your bar.
- [MINOR] (scope) MODEL-DIFFING (EVAL-3) IS THE WEAKEST LINK AND UNDER-SPECIFIED. 'Sanity-checked against known fine-tuning effects (e.g. refusal/safety shifts)' lacks a concrete ground truth or validation protocol; without one, 'which units shift' is unfalsifiable and reads as a qualitative demo. Also, recomputing units on two models requires the counterfactual co-response pipeline to be stable enough that unit changes reflect the model, not estimation noise.
  Action: Either demote to a clearly-labeled qualitative illustration, or give it a concrete oracle: diff against a model with a KNOWN injected/finetuned behavior (e.g., a published safety/refusal fine-tune or a deliberately fine-tuned variant) and show the surfaced unit changes recover it, with a stability/null floor distinguishing real shifts from re-estimation noise.
- [MINOR] (clarity) FIRST-LETTER IS THE MECHANISM TESTBED, NOT A SAFETY TASK, but the success criteria headline is 'safety-attribute classification'. The proposal mixes the clean controlled absorption case (spelling) with the safety payoff (toxicity, bias_in_bios) without flagging that the spelling mechanism may not transfer to the messier safety regime — and bias_in_bios in particular is known to be SAE-unfavorable / strongly diff-of-means-favorable, so a null there should be anticipated and scoped, not treated as a failure of the method.
  Action: State explicitly that first-letter is the clean mechanism testbed (where absorption is verifiable) and toxicity/bias_in_bios are the safety payoff, and pre-register the expectation that bias_in_bios may be a hard/null case. Frame a scoped result (works on toxicity/spelling, null on bias_in_bios) as a boundary finding rather than a failure.
</previous_review>

<task>
Provide a thorough peer review of this research hypothesis.

STEP 1 — GROUND YOUR REVIEW IN EVIDENCE:
Before writing critiques, search for relevant context to make your review authoritative:
- Search for accepted papers at top venues in this area — what level of
  contribution gets accepted? How does this hypothesis compare?
- Search for the closest existing work — is this genuinely novel or incremental?
- Check if the proposed methodology has known failure modes in the literature

STEP 2 — WRITE YOUR REVIEW:
For each critique:
1. Categorize: methodology, evidence, novelty, clarity, scope, or rigor
2. Rate severity: major (would waste compute if not fixed) or minor (polish)
3. Describe the issue clearly
4. Suggest a concrete action to address it

Focus on the most impactful issues. Flag fatal flaws that would waste compute if not fixed first.

STABILITY IS OK: If the hypothesis is on track and just needs more iterations to prove itself,
keep your feedback similar to the previous round. Don't manufacture new critiques — only escalate
when the revision introduced new issues or failed to address prior ones.

STEP 3 — H↔H EDGE (only if a <previous_hypothesis> block is present):
Classify how the current hypothesis relates to the previous iteration's hypothesis
using Moulines's structuralist typology. Set ``relation_type`` to one of:
    - "evolution": refining specialised claims while keeping the same conceptual frame
    - "embedding": the previous hypothesis is now a special case of a broader frame
    - "replacement": rejecting the previous frame entirely (Kuhnian, incommensurable shift)
Set ``relation_rationale`` to a brief justification (≤120 chars).

If no <previous_hypothesis> is present (this is iteration 1), leave both fields
null/empty.

Provide your review via structured output.
</task><user_data>
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
    "Critique": {
      "description": "A single actionable critique from the reviewer.",
      "properties": {
        "category": {
          "description": "Category: 'methodology', 'evidence', 'novelty', 'clarity', 'scope', or 'rigor'",
          "title": "Category",
          "type": "string"
        },
        "severity": {
          "description": "Severity: 'major' or 'minor'",
          "title": "Severity",
          "type": "string"
        },
        "description": {
          "description": "Clear description of the issue",
          "title": "Description",
          "type": "string"
        },
        "suggested_action": {
          "description": "Concrete suggestion for how to address this critique",
          "title": "Suggested Action",
          "type": "string"
        }
      },
      "required": [
        "category",
        "severity",
        "description",
        "suggested_action"
      ],
      "title": "Critique",
      "type": "object"
    },
    "DimensionScore": {
      "description": "Score for a single review dimension with improvement suggestions.",
      "properties": {
        "dimension": {
          "description": "Dimension name: 'soundness', 'presentation', or 'contribution'",
          "title": "Dimension",
          "type": "string"
        },
        "score": {
          "description": "Score from 1 (poor) to 4 (excellent)",
          "title": "Score",
          "type": "integer"
        },
        "justification": {
          "description": "Brief justification for this score",
          "title": "Justification",
          "type": "string"
        },
        "improvements": {
          "description": "Specific improvements to raise the score (what + how + why)",
          "items": {
            "type": "string"
          },
          "title": "Improvements",
          "type": "array"
        }
      },
      "required": [
        "dimension",
        "score",
        "justification"
      ],
      "title": "DimensionScore",
      "type": "object"
    }
  },
  "description": "ReviewerFeedback + Moulines H\u2194H typology for hypo_loop iterations.\n\nAdds ``relation_type`` + ``relation_rationale`` so the trace projection\ncan build a typed edge from the previous iteration's hypothesis to\nthis iteration's. On iteration 1 (no previous), both fields are\nempty/None.",
  "properties": {
    "overall_assessment": {
      "description": "Overall assessment of the paper's quality and readiness",
      "title": "Overall Assessment",
      "type": "string"
    },
    "strengths": {
      "description": "Key strengths of the paper",
      "items": {
        "type": "string"
      },
      "title": "Strengths",
      "type": "array"
    },
    "dimension_scores": {
      "description": "Scores (1-4) for: soundness, presentation, contribution",
      "items": {
        "$ref": "#/$defs/DimensionScore"
      },
      "title": "Dimension Scores",
      "type": "array"
    },
    "critiques": {
      "description": "Actionable critiques \u2014 specific issues with concrete suggestions",
      "items": {
        "$ref": "#/$defs/Critique"
      },
      "title": "Critiques",
      "type": "array"
    },
    "score": {
      "description": "Overall quality score from 1 (very strong reject) to 10 (award quality)",
      "title": "Score",
      "type": "integer"
    },
    "confidence": {
      "default": 3,
      "description": "Confidence in assessment from 1 (educated guess) to 5 (absolutely certain)",
      "title": "Confidence",
      "type": "integer"
    },
    "relation_type": {
      "anyOf": [
        {
          "enum": [
            "evolution",
            "embedding",
            "replacement"
          ],
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Moulines's structuralist typology classifying how this iteration's hypothesis relates to the previous iteration's: 'evolution' \u2014 refining specialised claims while keeping the same conceptual frame; 'embedding' \u2014 the previous hypothesis is now a special case of a broader frame; 'replacement' \u2014 rejecting the previous frame entirely (Kuhnian shift). Leave null on the first iteration (no previous hypothesis).",
      "title": "Relation Type"
    },
    "relation_rationale": {
      "default": "",
      "description": "Brief rationale (one short line, \u2264120 chars) for the relation_type. Empty on the first iteration.",
      "maxLength": 120,
      "title": "Relation Rationale",
      "type": "string"
    }
  },
  "required": [
    "overall_assessment",
    "strengths",
    "critiques",
    "score"
  ],
  "title": "HypoReviewerFeedback",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-06-17 12:03:52 UTC

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

### [3] SYSTEM-USER prompt · 2026-06-17 12:07:44 UTC

```
<validation-feedback>
Attempt 1 failed validation.

Schema validation found 1 problem — fix ALL of them at once:
  - at `relation_rationale`: "Prior correlation-only grouping is now an explicit special case of a broader 'jointly-track-at-unit-level' frame adding complementary coverage." is too long (at most 120 characters, got 143)
Every required field must be present and every field type must match the schema.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```
