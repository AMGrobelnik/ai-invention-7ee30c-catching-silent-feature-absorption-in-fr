# review_hypo — create_idea

> Phase: `hypo_loop` · round 4 · `review_hypo`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `review_hypo` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-17 12:35:06 UTC

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
  Counterfactual Co-Response Clustering of SAE Latents: Grouping Sparse-Autoencoder Features into Reliable Concept Units by
  Their Joint Response to Content Perturbations, Tested Against Surface-Invariant Matched Probes and a Supervised Oracle Unit
hypothesis: |-
  FALSIFIABLE CORE CLAIM (the paper rises or falls on this): clustering sparse-autoencoder (SAE) latents by their CORRELATED RESPONSE TO CONTENT COUNTERFACTUALS (interventional co-sensitivity) yields concept units that are more reliable classifiers than (i) the best raw single latent, (ii) observational co-activation / decoder-geometry clusters, and CRITICALLY (iii) a SURFACE-INVARIANT counterfactually-matched probe and (iv) a SUPERVISED ORACLE UNIT, with the advantage appearing and GROWING under a NATURAL distribution shift, because absorption and splitting corrupt the observational signals while leaving the interventional co-response intact.

  THE THREE NESTED CLAIMS, EACH WITH ITS OWN BASELINE, PRE-REGISTERED SO ATTRIBUTION IS CLEAN. (A) 'Counterfactual supervision helps' (NOT our contribution): naive diff-of-means/linear probe on raw labels -> a counterfactually-MATCHED probe trained on the same content-flip residual deltas. Expected true; not claimed. (B) 'Counterfactual-INVARIANCE supervision helps' (the new PRIMARY bar): matched probe -> SURFACE-INVARIANT MATCHED PROBE. We build this two ways and report both: (b1) the PAIR-MATCHED construction -- estimate the surface direction from the surface-flip pairs and ERASE it from the representation via LEACE / mean-projection concept erasure (Belrose et al. 2024) before fitting the content-flip diff-of-means/linear probe; and (b2) a Veitch et al. 2021 MMD counterfactual-invariance regularizer that penalizes dependence of the probe output on a surface/style variable, using the CONDITIONAL (anti-causal) regularizer because for toxicity/sentiment the label generates the text. (b1) is the load-bearing kill-shot because it consumes exactly the surface-flip information the unit uses, closing the information gap flagged last round. (C) 'GROUPING helps' (THE contribution): the SAE co-response unit must beat the surface-invariant matched probe under shift AND match-or-beat a SUPERVISED ORACLE UNIT (the top-N latents a supervised probe-attribution criterion selects, then pooled -- the SCR/TPP selection of Karvonen et al. 2411.18895 / Marks et al. SHIFT) AND exhibit the MECHANISTIC BACKBONE no probe can replicate: co-response units have LOW Jaccard with co-activation/geometry clusters and WIN SPECIFICALLY on the members where they differ -- in particular RECOVERING absorbed latents whose low MARGINAL probe-attribution makes top-N selection silently drop them. If (C) fails but (B) holds we report honestly that 'counterfactual-invariance supervision helps, SAE grouping adds no classification value' (a useful field-level negative), and the grouping contribution then rests solely on the mechanistic backbone, which we report REGARDLESS of probe competitiveness.

  SINGLE CONCRETE ADMISSION RULE (resolves the prior 'unfalsifiable unifying criterion'). For each candidate unit, against a SHUFFLED-PAIR NULL (permute which member of each minimal pair is content-on; B=1000): admit iff it clears at least ONE of two signatures AND passes unit-level surface invariance. Signature C (SPLITTING): mean within-unit content-response correlation > 95th pct of null -- this targets FEATURE SPLITTING, where one concept fragments across multiple co-responding sub-latents. Signature K (ABSORPTION): pooled max-over-members content-response AUC minus best-single-member AUC > 95th pct of the 'best-of-random-k' null gain, AND members mutually exclusive in firing (mean pairwise co-activation Jaccard < 0.1), AND each member's content-response precision on its own firing support >= 0.7 (a PRECISION FLOOR blocking spurious surface latents). Unit-level surface invariance: pooled surface-response not significantly above the shuffled-surface-pair null. We REPORT, per concept, which signature(s) it cleared so the regime is read off, not retrofitted, and we report the FALSE-ADMIT RATE = admission rate under shuffled pairs (target <= 0.05). Feature hedging (Chanin et al. 2505.11756) -- where a narrow SAE MERGES correlated features into a SINGLE polysemantic latent -- is cited as the mechanistic CAUSE of inter-latent correlation but is NOT itself a grouping target (a single merged latent cannot be grouped); our grouping operates on splitting and absorption, which keep multiple latents.

  HEADLINE SCOPE STATED UP FRONT (resolves n=1): exactly 6 concepts form ONE robustness-gap effect distribution -- 5 civil_comments toxicity sub-attributes (overall toxicity, obscene, insult, threat, identity_attack) + SENTIMENT using Kaushik et al. 2020 human-written counterfactual IMDB pairs. We report the per-concept shift gap vs the surface-invariant matched probe AND an aggregate effect with CIs across the 6 concepts. bias_in_bios is a pre-registered 7th BOUNDARY-NULL (scoped, not failure); first-letter spelling is the controlled ABSORPTION MECHANISM testbed (not safety, not in the distribution). A clean null at any stage is a publishable mechanism-level finding about how SAEs (mis)represent concepts.
motivation: |-
  Single SAE latents are unreliable units of analysis. Feature absorption (a specific latent suppresses the firing of a more general latent, which then has unpredictable holes; Chanin et al. 2409.14507, 2505.11756), feature splitting (one concept fragments across many latents, worse at larger width), feature hedging (a narrow SAE merges correlated features into one polysemantic latent; Chanin et al. 2505.11756), and 'Sparse Autoencoders Do Not Find Canonical Units of Analysis' (ICLR 2025, 2502.04878) all say the same thing: no single latent reliably tracks a concept. AxBench (ICML 2025 spotlight, 2501.17148) makes the stakes concrete -- plain difference-of-means beats raw-latent SAE methods on concept detection and steering -- so the bar any SAE-grouping method must clear is 'beat diff-of-means', and beating it on raw labeled data is not enough because diff-of-means can itself be made shift-robust with counterfactual data and concept erasure.

  The contribution lives squarely in clustering / feature-selection / classification for a learned knowledge representation (SAE features): we produce cluster-level units and a feature-level knowledge graph, evaluated on downstream classification. Every existing post-hoc grouping method relies on OBSERVATIONAL signals -- which latents fire together (co-activation 'feature families') or which decoders point alike (geometry). But absorption is exactly the regime where observational signals break BY CONSTRUCTION: per Chanin et al., the parent and the absorbing child are HIERARCHICAL and the child fires only where the parent's latent goes silent, so the two are MUTUALLY EXCLUSIVE in firing -- co-activation clustering provably cannot group them and their decoders need not be cosine-similar. This is a structural blind spot, not a tuning problem. And the standard supervised remedy -- select the top-N latents by their causal effect on a concept probe (the SCR/TPP latent selection of Karvonen et al. 2411.18895, built on Marks et al. SHIFT) -- SILENTLY DROPS absorbed latents, because a latent that fires only in a narrow sub-context has low MARGINAL probe-attribution even though it carries the concept there. Feature Hedging supplies the mechanistic 'why': absorption, splitting and hedging are all CAUSED by feature correlation/hierarchy -- precisely the structure an INTERVENTIONAL probe (perturb the concept, watch what moves together) is built to expose.

  Systems biology faced the identical obstacle and solved it: co-regulated genes are often NOT co-expressed at baseline and reveal shared regulation only under perturbation, which is why differential co-expression methods (DiffCoEx, WGCNA) cluster genes by their CORRELATED RESPONSE TO A PERTURBATION rather than baseline co-expression. Mapping genes->SAE latents and a chemical/genetic perturbation->an input content counterfactual gives the core mechanism. The insight an interpretability expert would not reach for is that SAE absorption/splitting are STRUCTURALLY the same obstacle that defeats baseline co-expression in biology, so the field's reliance on observational co-activation/geometry (and on marginal-attribution selection) is the wrong instrument and interventional co-response is the matched one. If correct, this gives a training-free, single-GPU, human-auditable way to turn off-the-shelf public SAEs (Gemma Scope) into reliable concept units for the safety-critical classification people actually want -- plus an auditable feature-level knowledge graph of concepts and their conditioning environments. If incorrect, the honest negative still tells the field to use surface-invariant probes rather than SAE units for robust classification, which is itself actionable.
assumptions:
- >-
  MINIMAL PAIRS ARE OBTAINABLE AT HIGH QUALITY, LOW COST, AND NON-CIRCULARLY. Primary content-flips use HUMAN-WRITTEN parallel
  corpora needing no LLM generation: ParaDetox (s-nlp, ACL 2022) toxic<->neutral for toxicity, and Kaushik et al. 2020 (ICLR)
  crowd-revised IMDB minimal pairs for sentiment. For rare toxicity sub-attributes (threat, identity_attack) and first-letter
  substitutions, LLM-generated pairs (OpenRouter, well under $10) are each LLM-judge-scored for content-flipped + surface-preserved,
  with reported pass rates and sensitivity to the pair-quality threshold. Any activation-space content edit, if used, is derived
  from an INDEPENDENT held-out diff-of-means on DISJOINT data, never from the SAE latents being grouped, so there is no circularity.
- >-
  THE MECHANISM IS PILOT-GATED IN BOTH HEADLINE REGIMES BEFORE THE FULL RUN. (1) Absorption arm (first-letter): the general
  latent (found by MAX ENCODER-COSINE with the LR first-letter probe, per Chanin et al. 2409.14507) and its absorbers (found
  by ablation effect on the correct-letter-minus-mean-incorrect-letter logit in contexts where the general latent fails to
  fire) show COMPLEMENTARY COVERAGE -- mutually-exclusive support whose POOLED response tracks the flip above the shuffled-pair
  null. (2) Splitting arm (toxicity): MULTIPLE latents carry toxicity with POSITIVELY-CORRELATED content-response above null
  AND a pooled unit beats both the single best toxicity latent and the matched diff-of-means on a held-out IID slice. Each
  arm has a symmetric decision rule; the headline proceeds only in a regime its pilot confirms, and a pilot null is reported
  as a mechanism finding.
- >-
  THE WIN, IF IT OCCURS, IS ATTRIBUTABLE TO GROUPING, NOT TO EXTRA SUPERVISION OR EXTRA CAPACITY. The kill-shot baseline (surface-invariant
  matched probe) is INFORMATION-MATCHED via LEACE/mean-projection erasure of the surface direction estimated from the SAME
  surface-flip pairs the unit uses (with a Veitch-2021 conditional-MMD regularizer as a reported alternative). A SUPERVISED
  ORACLE UNIT (top-N latents by probe-attribution, then pooled = the SCR/TPP selection) and a CAPACITY-MATCHED nonlinear probe
  (max-pool over supervised-selected raw residual directions) control for label selection and for max-pool nonlinearity. The
  grouping claim survives only if the unsupervised co-response unit matches/beats the oracle unit AND the mechanistic backbone
  (low-Jaccard vs observational clusters + wins on differing members, including recovered absorbers) holds.
- >-
  SURFACE-FORM CONFOUNDING IS MATERIAL AT THE UNIT LEVEL AND THE NATURAL SHIFT IS REAL. Individual latents entangle a concept
  with the surface forms it co-occurs with, so enforcing surface invariance on the POOLED unit yields units that generalize
  where single latents and distributionally-naive probes do not. The primary shift is NATURAL (train on one platform/domain,
  e.g. Jigsaw Wikipedia-talk comments; test on another, e.g. civil_comments; sentiment trained on CAD-IMDB and tested on an
  out-of-domain review source such as CEBaB restaurant reviews / Amazon), with the gap reported as a function of a MEASURED
  shift magnitude (train/test embedding distance or domain-classifier separability). LLM-paraphrase shift is a SECONDARY check
  with judge pass rates. If surface confounding is immaterial, units collapse toward the surface-invariant probe and the method
  yields no gain -- the pre-registered boundary finding, not a hidden failure.
- >-
  Off-the-shelf Gemma Scope SAEs on Gemma-2-2b expose latent counterfactual responses measurable above noise on a single GPU
  for a few thousand minimal pairs per concept, and the chosen attributes have enough labeled/templatable data (civil_comments
  sub-attribute floats, CAD-IMDB, ParaDetox) to build minimal pairs and held-out, natural-shift test splits. Absorption is
  more severe at WIDER SAEs and splitting at larger width, so SAE width/layer is a robustness axis (16k canonical primary,
  65k as a stress point).
investigation_approach: |-
  STEP 0 - TWO-ARM DE-RISKING PILOT (run first, ~1-2 GPU-hours total, gates the full suite). ARM A (absorption, first-letter): using Chanin et al. 2409.14507, find the general first-letter latent by max encoder-cosine with the LR probe and its absorbers by ablation effect on the (correct-letter minus mean-incorrect-letter) logit where the general latent is silent; build first-letter content-flip pairs; measure (a) correlated content-response (expected low/disjoint) and (b) COMPLEMENTARY coverage (pooled max-over-members tracks the flip where members have holes) against a shuffled-pair null. ARM B (splitting, toxicity): on ParaDetox/civil_comments, measure how many latents carry toxicity, whether their content-response profiles are POSITIVELY correlated above the shuffled-pair null, and whether the pooled unit beats (i) the single best toxicity latent and (ii) the matched diff-of-means on a held-out IID slice. DECISION RULES (symmetric): proceed with a regime as headline only if its pilot clears the null AND (for B) shows a non-trivial IID edge over the best single latent; otherwise report that regime's null as a mechanism finding and keep the headline in the regime that passed.

  DATA & CONCEPTS (exact count up front). HEADLINE DISTRIBUTION (6 concepts): 5 civil_comments toxicity sub-attributes (toxicity, obscene, insult, threat, identity_attack; rare sub-attributes supplemented with judge-validated LLM pairs and flagged) + SENTIMENT (Kaushik et al. 2020 human counterfactual IMDB). BOUNDARY-NULL: bias_in_bios. MECHANISM TESTBED: first-letter spelling (absorption; NOT safety). Per concept, content/surface definition: toxicity content-flip = toxify/detoxify (ParaDetox), surface-flip = content-preserving paraphrase; sentiment content-flip = human counterfactual label flip (CAD), surface-flip = paraphrase; first-letter content-flip = change whether the word starts with the target letter, surface-flip = a DIFFERENT same-letter word / capitalization / context paraphrase.

  COUNTERFACTUAL SIGNAL. Encode every text and its counterfactual with a frozen Gemma Scope residual-stream SAE (layer ~12, width 16k canonical; layer/width as robustness axis). Per latent: content-response = delta(activation) under content-flip; surface-response = delta under surface-flip. Aggregate into per-latent response profiles across contexts.

  CLUSTERING METHOD (the in-scope contribution). Build a latent-by-context content-response matrix. Cluster latents with a differential-correlation affinity (DiffCoEx-style) for signature C and a coverage-complementarity term for signature K, via agglomerative clustering / graph community detection on the affinity. Finalize each candidate unit with the SINGLE ADMISSION RULE above: clear signature C (within-unit content-response correlation > 95th-pct null) OR signature K (pooled-minus-best-member AUC gain > 95th-pct best-of-random-k null, AND mutual-exclusivity Jaccard < 0.1, AND per-member precision floor >= 0.7), AND pass unit-level surface invariance (pooled surface-response not above the shuffled-surface null). Report which signature each concept cleared and the false-admit rate under shuffled pairs (<= 0.05). Emit human-auditable unit definitions (member latents, logit-lens tokens, conditioning contexts) and directed specialization edges (a member responsive only in a sub-context = absorbed/split child) = a feature-level knowledge graph.

  WORKED EXAMPLE (concrete schematic). Toxicity unit (splitting): members = {profanity/slur latent, demeaning-insult latent, aggressive-imperative latent}; under ParaDetox detox all three drop TOGETHER (positive co-response, signature C); pooled max tracks toxicity; pooled surface-response to paraphrase ~ 0. First-letter unit (absorption): members = {general 'starts-with-L' latent (fires on most L-words but SILENT on 'lion'/'London'), 'lion'-absorber, 'London'-absorber}; no member tracks 'starts-with-L' everywhere, but pooled max does (signature K); members never co-fire (Jaccard ~ 0); pooled surface-response (capitalization/paraphrase) ~ 0.

  BASELINES (matched baselines are PRIMARY). (a) best raw single latent (any width); (b) observational co-activation clustering / feature families; (c) decoder-geometry clustering; (d) counterfactually-MATCHED diff-of-means (same content-flip deltas); (e) counterfactually-MATCHED linear probe; (f) SURFACE-INVARIANT MATCHED PROBE = (d)/(e) with the surface-flip direction erased via LEACE/mean-projection (Belrose et al. 2024), with a Veitch et al. 2021 conditional-MMD invariance regularizer reported as an alternative -- the INFORMATION-MATCHED PRIMARY kill-shot; (g) SUPERVISED ORACLE UNIT = pool the top-N latents selected by probe-attribution causal-effect score (the SCR/TPP selection of Karvonen et al. 2411.18895 / Marks et al. SHIFT) -- controls 'grouping vs flat supervised selection' and is the baseline our absorber-recovery must beat; (h) CAPACITY-MATCHED nonlinear probe = max-pool over supervised-selected raw residual directions (controls 'grouping vs max-pool nonlinearity'; overlaps (g)); (i) standard unmatched diff-of-means / linear probe on raw labels.

  EVAL 1 - CLASSIFICATION ROBUSTNESS GAP (the single headline AXIS, over 6 concepts). Unit-pooled activation (max/sum over members) as classifier on IID and on the NATURAL shift split; report F1/AUC and recall on absorbed/held-out-surface cases; headline metric = robustness gap under shift vs ALL baselines including the surface-invariant matched probe and oracle unit, per concept AND aggregated with CIs across concepts, plotted against MEASURED shift magnitude. MECHANISTIC BACKBONE (load-bearing for 'grouping helps', reported even under a partial probe-null): co-response units have low Jaccard with co-activation/geometry clusters AND win specifically on the differing members, including absorbed latents the oracle unit's top-N attribution dropped. CLUSTER-STABILITY: bootstrap over minimal pairs reporting adjusted Rand / Jaccard across resamples, the shuffled-pair null for the affinity matrix, and sensitivity to pairs-per-concept.

  SECONDARY / STRETCH (clearly labeled, confirmatory not load-bearing, one illustrative case each). STEERING: steer with the unit's shared content-response direction vs best single latent vs surface-invariant matched diff-of-means; measure on-target effect and side-effects (KL on unrelated prompts, fluency) at MATCHED on-target effect with bootstrap CIs; engage 'SAEs Are Good for Steering -- If You Select the Right Features' (2505.20063) and AxBench protocol. MODEL-DIFFING: diff a base model vs a variant with a KNOWN injected/fine-tuned behavior and test whether surfaced unit changes recover it, with a stability/null floor.

  HONEST FAILURE-MODE REPORTING. Dependence on counterfactual quality (pass rates); concepts with no surface-invariant co-responding/complementary group; regimes where co-response collapses to co-activation (no gain); cases where the surface-invariant matched probe still wins under shift (reframes to 'invariance supervision helps'); cases where the oracle unit ties the co-response unit (reframes to 'selection, not grouping'); compute cost; sensitivity to SAE layer/width; bias_in_bios boundary-null.
success_criteria: >-
  CONFIRMED if (pre-registered, in this nesting): (1) the two-arm STEP-0 pilot confirms above-null structure in at least one
  headline regime -- positively correlated content-response (splitting/toxicity) and/or complementary coverage (absorption/first-letter)
  -- with the toxicity arm also showing a pooled IID edge over the best single latent and the matched diff-of-means; (2) across
  the 6 headline concepts, content-co-response units beat the best raw single latent AND the INFORMATION-MATCHED SURFACE-INVARIANT
  probe (LEACE/mean-projection construction) on classification, with the advantage positive and GROWING with MEASURED shift
  magnitude (per-concept and aggregate CIs across concepts); (3) the co-response unit matches-or-beats the SUPERVISED ORACLE
  UNIT (top-N probe-attribution selection) and the capacity-matched nonlinear probe, so the gain is grouping rather than mere
  supervised selection or pooling nonlinearity; (4) the MECHANISTIC BACKBONE holds -- co-response units have low Jaccard with
  co-activation/geometry clusters (above the stability/shuffled-pair null) AND win specifically on the differing members,
  including absorbed latents the oracle's top-N attribution dropped -- and is reported regardless of probe competitiveness;
  (5) cluster assignments are stable across bootstrap resamples (adjusted Rand/Jaccard well above null), false-admit rate
  under shuffled pairs <= 0.05, and knowledge-graph specialization edges agree with the supervised absorption diagnostic (2409.14507)
  on first-letter. SECONDARY (confirmatory only): unit-direction steering achieves lower KL side-effects than best-single-latent
  and the matched diff-of-means at matched on-target effect; model-diffing recovers a known injected behavior above its null
  floor. HONEST NEGATIVES, EACH PUBLISHABLE: content-co-response grouping gives no advantage over observational co-activation
  grouping (co-response ~ co-activation); OR units fail to beat raw latents AND the surface-invariant probe even under shift;
  OR the surface-invariant matched probe closes the shift gap (reframes to 'counterfactual-invariance supervision helps',
  grouping claim then rests only on the mechanistic backbone); OR the oracle unit ties the co-response unit (reframes to 'selection,
  not grouping'); OR co-response is too noisy to cluster (ARI ~ null); OR a pilot arm shows neither correlated nor complementary
  above-null co-response. bias_in_bios is a pre-registered boundary-null, not method failure.
related_works:
- >-
  AxBench: Steering LLMs? Even Simple Baselines Outperform Sparse Autoencoders (Wu et al., ICML 2025 spotlight, 2501.17148):
  on Gemma-2-2B/9B, for concept DETECTION difference-in-means performs best and SAEs are not competitive (likewise steering).
  This sets our bar. We differ by making diff-of-means MAXIMALLY fair (counterfactually matched AND surface-invariant via
  concept erasure) and pre-registering the win condition as a shift-robustness gap against THAT information-matched baseline
  plus a supervised oracle unit.
- >-
  Sparse Autoencoders Do Not Find Canonical Units of Analysis (Bussmann et al., ICLR 2025, 2502.04878): uses SAE stitching
  and meta-SAEs to argue SAEs do not learn canonical units; its remedy is geometric/training-based. We propose a BEHAVIORAL
  unit defined by counterfactual co-response and unit-level surface invariance, evaluated on downstream classification, with
  no retraining.
- >-
  Feature Hedging: Correlated Features Break Narrow SAEs (Chanin, Dulka, Garriga-Alonso, 2505.11756): full-text confirms its
  Table 1 contrast -- ABSORPTION learns gerrymandered latents (sparsity-loss-driven, worse at WIDER SAEs, BOTH features tracked
  across mutually-exclusive latents via a parent->child hierarchy fc=>fp) vs HEDGING merges correlated features into a SINGLE
  polysemantic latent (MSE-driven, worse at NARROWER SAEs, ONE feature in the SAE). We use this to (a) correctly scope our
  grouping to splitting+absorption (a hedged single latent is not groupable) and (b) treat correlation/hierarchy as the mechanistic
  cause our interventional probe exposes.
- >-
  A is for Absorption (Chanin et al., 2409.14507, NeurIPS): full-text confirms a SUPERVISED DIAGNOSTIC -- identify the first-letter
  latent by max encoder-cosine with an LR probe (or k=1 sparse probing), and use ablation on the correct-minus-incorrect-letter
  logit to find the absorbing latent that mediates the concept where the general latent fails to fire. It DETECTS absorption
  on individual latents; it does not GROUP parent+absorbers into a usable unit. We use it as a partial ORACLE for the pilot
  and to validate knowledge-graph edges; our contribution is the unsupervised grouping/repair.
- >-
  Counterfactual Invariance to Spurious Correlations (Veitch, D'Amour, Yadlowsky, Eisenstein, NeurIPS 2021, 2106.00545): full-text
  confirms the regularizer is MMD-based (penalize MMD between prediction distributions conditioned on the nuisance Z) and
  is NOT pair-based -- it enforces the counterfactual-invariance SIGNATURE without counterfactual examples -- and that the
  correct scheme DEPENDS on causal direction (marginal MMD in the causal direction; CONDITIONAL MMD in the anti-causal direction
  where Y causes X, as for toxicity/sentiment). We import this as ONE construction of the information-matched kill-shot baseline;
  the load-bearing construction is LEACE/mean-projection erasure of the surface direction estimated from surface-flip pairs.
  The grouping must beat this baseline to attribute the gain to SAE units rather than to invariance supervision.
- >-
  LEACE: Perfect linear concept erasure in closed form (Belrose et al., 2306.03819) and mean-projection erasure: closed-form
  / heuristic projection onto the orthogonal complement of a class-mean-difference direction. We use this to erase the surface-flip
  direction and build the PAIR-MATCHED surface-invariant probe -- a strong, principled baseline, not a novelty claim.
- >-
  SHIFT / SCR / TPP SAE evaluation (Marks et al. 2024; Karvonen et al. 2411.18895): full-text confirms these SELECT individual
  SAE latents by ranking their CAUSAL EFFECT on a concept probe (top-N by probe-attribution score, optionally LLM-filtered),
  then ABLATE the set; they do NOT cluster latents by interventional co-response. This is exactly our SUPERVISED ORACLE-UNIT
  baseline, and a latent that fires only in a narrow sub-context (an absorber) has low marginal attribution and is silently
  dropped -- the specific gap our coverage grouping fills. We must match/beat this select-then-pool baseline to show grouping
  by co-response STRUCTURE adds value.
- >-
  Counterfactually-Augmented Data (Kaushik, Hovy, Lipton, ICLR 2020) and CEBaB (Abraham et al., NeurIPS 2022, 2205.14140):
  human-written counterfactual minimal pairs for sentiment (IMDB; 1707/245/488 minimally-edited reviews) and aspect concepts
  (restaurant reviews), with out-of-domain sources. We use CAD as a SECOND human-counterfactual concept axis (breaking the
  prior n=1 toxicity headline) and CEBaB/cross-domain reviews as a natural shift target; these supply non-circular pairs and
  a measured shift, not the grouping method.
- >-
  Co-activation feature families and graph-regularized SAEs (Disentangling Dense Embeddings 2408.00657; GSAE 2512.06655; Sparse
  Feature Coactivation 2506.18141): group SAE features by OBSERVATIONAL co-activation/geometry. By construction these cannot
  group a concept's absorbed/split latents (mutually exclusive in firing). We use the opposite, INTERVENTIONAL signal (correlated
  change, or complementary coverage, under a content counterfactual), training-free on frozen public SAEs.
- >-
  Mutual-exclusivity / Ising-coupling and slot-conditional exclusivity grouping of SAE latents (Bhalla et al. global Ising
  coupling; slot-conditional exclusivity studies): group latents by negative co-occurrence. Exclusivity shows two latents
  do not co-fire but not that they belong together, and such methods have struggled downstream. We supply the missing POSITIVE
  interventional signal (correlated co-response for splitting; complementary coverage of the same content flip for absorption)
  and a precision floor, and test whether it succeeds where exclusivity alone does not.
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
  A Level-3 (methodological) cross-field transfer from systems biology's differential co-expression / perturbation co-response
  module discovery (DiffCoEx, WGCNA): cluster units by their CORRELATED RESPONSE TO A PERTURBATION, not by baseline co-expression,
  because co-regulated genes are frequently not co-expressed until perturbed. Mapping genes->SAE latents and a chemical/genetic
  perturbation->an input content counterfactual gives the core mechanism. It is fused with (i) causal ML's counterfactual
  invariance (Veitch et al. 2021, whose full-text MMD/causal-direction analysis we use to build the information-matched baseline)
  and concept-erasure (LEACE / mean-projection, Belrose et al. 2024), which supply the surface-vs-content axis AND the surface-invariant
  kill-shot; (ii) NLP minimal-pair counterfactuals (ParaDetox, Kaushik et al. 2020 CAD, CEBaB) for non-circular human-written
  perturbations; and (iii) a COMPLEMENTARY-COVERAGE (set-cover-style) extension for feature absorption, where members have
  disjoint support and plain correlation fails. The unifying insight an interpretability expert would not reach for: SAE failure
  modes (absorption, splitting) are structurally the same obstacle that defeats baseline co-expression in biology -- the right
  members are invisible at baseline and visible only under perturbation -- so observational co-activation/geometry AND marginal-attribution
  selection are the wrong instruments, and interventional co-response is the matched one. This revision hardens attribution
  after reading the sources in full: the baseline is now information-matched (LEACE-erased surface direction; Veitch conditional-MMD
  as alternative), the oracle unit is the actual SCR/TPP top-N attribution selection that demonstrably drops absorbers, the
  headline spans 6 concepts, both regimes are pilot-gated, and the admission rule is a single falsifiable procedure with explicit
  null floors.
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
    unpredictable holes. Both features stay tracked in the SAE across mutually-exclusive 'gerrymandered' latents; absorption
    is worse at WIDER SAEs.
- term: Feature splitting vs feature hedging
  definition: >-
    Splitting = one concept fragments across MANY latents (worse at larger width); these sub-latents co-respond POSITIVELY
    to a content flip and are the groupable signature-C regime. Hedging (Chanin et al. 2505.11756) = a narrow SAE MERGES correlated
    features into a SINGLE polysemantic latent (MSE-driven, worse at narrower width); a hedged single latent is NOT a grouping
    target but explains why inter-latent correlation exists.
- term: Counterfactual minimal pair
  definition: >-
    Two inputs differing in exactly one targeted way: a content-flip pair changes whether a concept is present while holding
    surface fixed; a surface-flip pair paraphrases/rewrites surface while holding content fixed. Human-written pairs (ParaDetox,
    Kaushik et al. 2020 CAD, CEBaB) are used where available; LLM-generated pairs are LLM-judge-validated for content-flip
    and surface-preservation.
- term: Counterfactual content-response (of a latent)
  definition: >-
    The change in a latent's activation between a content-flip pair (concept added minus removed), measured per context; the
    vector of these changes across many contexts is the latent's content-response profile.
- term: Interventional co-response (grouping criterion)
  definition: >-
    Latents belong to the same concept unit if they jointly track the content perturbation across contexts, even if their
    baseline activations never co-occur. Realized in two signatures applied via a single admission rule: positive correlation
    of content-response profiles (signature C, splitting) and complementary coverage (signature K, absorption).
- term: Complementary coverage (signature K)
  definition: >-
    The absorption-regime grouping signal: members respond to the SAME content flip on DISJOINT context supports, so no single
    member tracks the concept everywhere but the group's POOLED (max-over-members) content-response covers the flip across
    all contexts. Admitted only with a mutual-exclusivity constraint (low co-activation Jaccard) AND a per-member precision
    floor that blocks spurious surface latents.
- term: Single unit admission rule
  definition: >-
    A candidate unit is admitted iff it clears signature C (within-unit content-response correlation above the 95th-pct shuffled-pair
    null) OR signature K (pooled-minus-best-member AUC gain above the best-of-random-k null, with mutual-exclusivity and precision-floor
    constraints), AND its pooled surface-response is not above the shuffled-surface null. The cleared signature is reported
    per concept and the false-admit rate under shuffled pairs is reported (target <= 0.05), pinning the otherwise-flexible
    'jointly track at the unit level' criterion into one falsifiable procedure.
- term: Surface-invariant matched probe (primary kill-shot)
  definition: >-
    A counterfactually-matched diff-of-means/linear probe trained on the content-flip residual deltas and made surface-invariant
    by ERASING the surface-flip direction via LEACE / mean-projection (Belrose et al. 2024) estimated from the same surface-flip
    pairs (pair-matched), with a Veitch et al. 2021 conditional-MMD invariance regularizer as a reported alternative. It is
    INFORMATION-MATCHED to the unit (uses both content- and surface-flip information), so a unit win attributes to GROUPING
    rather than to extra counterfactual information.
- term: Supervised oracle unit
  definition: >-
    A baseline that pools the top-N latents selected by a supervised probe-attribution causal-effect criterion (the SCR/TPP
    latent selection of Karvonen et al. 2411.18895 / Marks et al. SHIFT). It is the standard supervised remedy; because it
    ranks by MARGINAL attribution it silently drops absorbed latents that fire only in narrow sub-contexts. The unsupervised
    co-response unit must match or beat it to show that grouping by co-response STRUCTURE adds value over flat supervised
    selection.
- term: Unit-level surface invariance
  definition: >-
    Surface invariance enforced on the POOLED unit (the aggregate shows little response to surface-flip counterfactuals) rather
    than on each member, so surface-/token-specific absorbed children can be admitted into a unit whose aggregate is paraphrase-robust.
- term: Measured shift magnitude
  definition: >-
    A scalar quantifying how different the natural train and test distributions are (e.g. train/test embedding distance or
    domain-classifier separability AUC), against which the unit-minus-baseline robustness gap is plotted, so 'the gap grows
    under shift' is anchored to a measured, not hand-tuned, axis.
- term: Differential co-expression (analogy)
  definition: >-
    A systems-biology family (DiffCoEx, WGCNA) that clusters genes by how their expression co-varies under a perturbation
    rather than at baseline, revealing co-regulated modules invisible to baseline co-expression -- the methodological template
    transferred here to SAE latents.
- term: Reliable unit of analysis
  definition: >-
    A human-auditable group of SAE latents that tracks a concept dependably across surface variation -- recovering recall
    that absorption/splitting destroy at the single-latent level -- and is reusable as a classifier (headline), and secondarily
    for steering and model-diffing.
summary: >-
  SAE latents encoding the same concept are often mutually exclusive in firing (feature absorption and splitting), so observational
  co-activation, decoder geometry, and marginal-attribution latent selection cannot group them; clustering latents instead
  by how they jointly track a content counterfactual -- positively correlated co-response for splitting, complementary coverage
  for absorption, admitted by one falsifiable null-anchored rule and made surface-invariant at the pooled-unit level -- yields
  training-free, auditable concept units whose headline test, over 6 safety/sentiment concepts, is beating an information-matched
  LEACE-surface-invariant diff-of-means/linear probe AND a supervised top-N oracle unit on classification with a widening
  advantage under a measured natural distribution shift.
</previous_hypothesis>

<previous_review>
Critiques from the previous review. Check which ones have been addressed
in the revised hypothesis. Do NOT re-raise critiques that have been adequately fixed.
Only re-raise if the fix is insufficient.

- [MAJOR] (methodology) HEADLINE-MECHANISM GAP for the new primary bar. The motivation convincingly explains why interventional co-response grouping should beat OBSERVATIONAL methods (co-activation/geometry are structurally blind to mutually-exclusive absorbed/split latents) and why it should beat the NAIVE probe (surface confound contaminates diff-of-means). But this round makes the SURFACE-INVARIANT matched probe (LEACE-erased, information-matched) the primary bar for the CLASSIFICATION claim (C), and the existing motivation does NOT explain why a grouped SAE unit should out-generalize THAT baseline under shift. Against a surface-invariant probe, the 'surface confound contaminates the estimator' story no longer applies — both the unit and the probe are surface-invariant. The success criterion 'advantage positive and GROWING with measured shift magnitude' is therefore asserted without an a-priori mechanism. Combined with AxBench's finding that diff-of-means is the strongest detection method, there is a real risk that claim-C's classification part is a foregone partial-null, collapsing the headline to the already-conceded 'invariance supervision helps' (B) plus the mechanistic backbone — i.e., the costly 6-concept x all-baselines x 2-shift classification sweep mostly confirms a negative.
  Action: Either (preferred) articulate the concrete mechanism by which grouping out-generalizes a surface-invariant probe on classification — e.g., rank-limited LEACE erasure of a single estimated surface direction cannot remove MULTI-DIMENSIONAL or context-dependent surface confounds, whereas a unit of complementary members spreads coverage across those sub-contexts and recovers recall under shift — and pre-register the predicted SIGN and rough magnitude; OR promote the MECHANISTIC BACKBONE (absorber recovery vs the oracle unit; low Jaccard + wins on differing members) to be the actual headline contribution and explicitly demote the classification robustness gap to supporting evidence. This protects the paper from a diffuse partial-null and focuses compute on the claim that is robust regardless of probe competitiveness.
- [MAJOR] (scope) The n=1 -> n=6 fix is only partial. Five of the six headline concepts (overall toxicity, obscene, insult, threat, identity_attack) are civil_comments toxicity SUB-ATTRIBUTES that co-occur very heavily and share most of their positive instances; treating them as six independent draws for an 'aggregate effect with CIs across the 6 concepts' overstates the effective sample size and the independence the CI assumes. The genuinely independent concept axes are closer to two (a toxicity family + sentiment), with first-letter explicitly outside the distribution and bias_in_bios a boundary-null. A single adverse draw at the toxicity-family level (toxicity happens not to split usefully in this SAE) still propagates across five of the six 'concepts', so the headline is less robust to that risk than the count suggests.
  Action: Report a clustered/hierarchical CI that accounts for within-toxicity-family correlation (or down-weight the five sub-attributes to one family-level effect plus per-subtype detail), and add at least one MORE genuinely independent concept family with available minimal pairs (e.g., a CEBaB aspect such as service/food, or spam/formality/politeness) to raise the effective independent-axis count toward 3. Frame the aggregate honestly as ~2-3 independent families rather than 6 i.i.d. concepts.
- [MAJOR] (scope) EXECUTION-COMPLEXITY / FEASIBILITY RISK. The design has grown into a very large matrix: 3 nested claims x 6 headline concepts (+2 testbeds) x ~9 baselines (a-i) x 2 admission signatures x 2 shift types (natural + paraphrase) x SAE width/layer robustness axis x bootstrap stability stats, plus a two-arm pilot, plus secondary steering and model-diffing — all on a single GPU under a <$10 LLM budget. The risk is not any single component but that the whole is executed shallowly (every cell run once, underpowered) rather than the core executed decisively, which would read as a thin, hedged result and depress the score regardless of the idea's merit.
  Action: Declare a strict, depth-first MINIMUM VIABLE headline that must be completed before anything else: the two-arm STEP-0 pilot, then claim B vs C on the toxicity family + sentiment (the two independent axes) with the surface-invariant probe and oracle unit, plus the mechanistic backbone and first-letter absorber recovery. Explicitly mark steering, model-diffing, the 65k-width stress point, the Veitch-MMD alternative construction, and the LLM-paraphrase secondary shift as DROP-FIRST stretch goals that are only attempted if the core lands. Pre-commit pairs-per-concept counts adequate for the bootstrap CIs.
- [MINOR] (rigor) The signature-K admission null ('pooled max-over-members content-response AUC minus best-single-member AUC > 95th pct of the best-of-random-k null gain') is well-intentioned but its strength depends entirely on the population the random k are drawn from. If drawn from ALL latents (the vast majority of which are silent or content-irrelevant), the random-k pooled gain is near zero, so almost any pooling of content-responsive latents clears the null trivially — the test would then certify 'these latents respond to content', not 'these latents provide COMPLEMENTARY coverage of the same flip'. The mutual-exclusivity (Jaccard < 0.1) and precision-floor constraints mitigate but do not fully substitute for a matched null.
  Action: Draw the best-of-random-k null from the set of CONTENT-RESPONSIVE latents (matched on marginal content-response AUC to the candidate members) rather than from all latents, so the admission test isolates the complementarity/coverage structure rather than mere content-responsiveness. Report the false-admit rate under this matched null.
- [MINOR] (methodology) Baseline (h), the capacity-matched nonlinear probe, is described only as 'max-pool over supervised-selected raw residual directions' and overlaps with the oracle unit (g), but the selection rule and the number of pooled directions are not pinned down. Since this baseline is the control that isolates 'grouping' from 'max-pool nonlinearity', leaving it underspecified weakens that isolation: if the number of pooled directions or the selection differs from the unit, an apparent unit advantage could be a capacity/count artifact rather than grouping.
  Action: Specify (h) precisely: max-pool over exactly the same NUMBER of raw residual-stream directions as the admitted unit has members, selected by the same supervised attribution criterion as the oracle unit, on the matched paired activations. State explicitly that this controls count and pooling nonlinearity so any residual unit advantage is attributable to the co-response grouping structure.
- [MINOR] (novelty) A closely-adjacent recent work is uncited: 'Discovering Concept Directions from Diffusion-based Counterfactuals via Latent Clustering' (CDLC, arXiv 2505.07073) clusters latent DIFFERENCES between factual and counterfactual pairs to recover class-specific concept directions — the same counterfactual-difference-clustering template proposed here, in the vision/diffusion domain. 'Causal Differentiating Concepts: Interpreting LM Behavior' (OpenReview Zf6Oj5x9sE) is similarly adjacent. A reviewer familiar with these will ask why they are not engaged, and absence reads as an incomplete related-work survey even though the substrate (SAE latents on a frozen LLM, plus surface-invariance and absorption-recovery) is genuinely different.
  Action: Add and differentiate CDLC (2505.07073) and the Causal Differentiating Concepts paper: note that they cluster counterfactual latent-DIFFERENCE vectors to find concept directions (one direction per concept) in vision, whereas this work clusters SAE LATENTS (discrete dictionary units) by their co-response profiles into auditable multi-member units, adds unit-level surface invariance, and specifically targets the absorption regime via complementary coverage — none of which CDLC addresses. This pre-empts the 'not the first to cluster counterfactual responses' objection.
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

### [2] HUMAN-USER prompt · 2026-06-17 12:35:06 UTC

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
