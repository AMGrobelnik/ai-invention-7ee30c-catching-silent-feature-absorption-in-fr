# review_hypo — create_idea

> Phase: `hypo_loop` · round 6 · Substep: `review_hypo`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave the agent(s) in this substep — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `review_hypo` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-17 13:06:34 UTC

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
  Interventional Co-Response Grouping of SAE Latents into Auditable Concept Units: Recovering Absorbers That Marginal-Attribution
  Selection Drops, and Isolating Grouping From Pooling on Worst-Sub-Context Recall
hypothesis: |-
  ONE-SENTENCE HEADLINE (stated plainly, once): an unsupervised unit built by clustering SAE latents on their interventional co-response recovers the absorber latents that a count-matched marginal-attribution pool drops, and -- because each absorber is a sub-context specialist -- keeps worst-sub-context recall stable under sub-population reweighting in the regime where not only a single dense hyperplane but ALSO the count-matched marginal-attribution pool collapses, approaching an oracle group-DRO probe that uses sub-context labels while the unit uses none.

  MINIMUM VIABLE RESULT (what the paper must show to stand): (i) the two-arm pilot confirms above-null co-response structure in at least one regime; (ii) the unsupervised co-response unit beats the best raw single latent AND observational co-activation / decoder-geometry clustering on classification (claim C1); (iii) on the first-letter absorption testbed, the unit recovers absorber latents that the supervised oracle's top-N marginal-attribution selection drops, and wins specifically on the sub-contexts where they differ (claim C3). All sub-population-shift robustness results are supporting evidence layered on this backbone; aggregate-F1 parity with a strong dense probe is an explicitly acceptable, pre-registered outcome.

  HEADLINE RESULT GRID (claims x baselines x metric x predicted sign x what it isolates):
  | Test | Compared against | Metric | Predicted sign | What it isolates |
  |---|---|---|---|---|
  | C1 | (a) best raw latent; (b) co-activation/geometry clusters | classification F1/AUC, IID + shift | unit > both | grouping beats single-latent + observational grouping |
  | C2 | (g) oracle SAE-latent pool (top-N SCR/TPP); (h) count+pool-matched raw-direction pool | classification F1/AUC | unit >= both | gain is not just supervised selection or pooling nonlinearity |
  | C3 first-letter (ABSORPTION headline) | (g)/(h) marginal-attribution pools; supervised absorption diagnostic 2409.14507 | recall on differing sub-contexts; recovered-absorber count; KG-edge agreement | unit > (g)/(h); edges agree | co-response recovers absorbers marginal attribution drops |
  | Robustness POOLING contrast, toxicity | (f) single surface-invariant hyperplane | worst-sub-context recall vs reweighting magnitude | unit > (f), growing | EXPECTED: pooled specialists beat one hyperplane -- NOT grouping evidence |
  | Robustness GROUPING headline, toxicity | (g)/(h) count-matched marginal-attribution pools | worst-sub-context recall vs reweighting magnitude | unit > (g)/(h), growing | THE grouping signal: absorber coverage, not pooling, buys robustness |
  | Robustness bounds, toxicity | (j) oracle group-DRO probe WITH sub-context labels; (k) label-free group-inference probe (JTT/GEORGE-style) | worst-sub-context recall | unit approaches (j) w/o labels; unit >= (k) AND auditable | training-free auditable route vs loss-reweighting route |
  | Dense-probe aggregate F1 | (f) surface-invariant probe | aggregate F1 | tie acceptable (agnostic) | concedes the AxBench bar honestly |

  THE TWO REGIME STORIES, KEPT SEPARATE (resolves the rigor critique -- they are COMPLEMENTARY evidence for 'grouping helps', not the same metric on both testbeds).
  STORY 1 -- FIRST-LETTER = ABSORPTION (signature K, complementary coverage). The 'starts-with-L' concept fragments into a general latent (silent on specific tokens) plus per-token absorbers ('lion'-absorber, 'London'-absorber). No member tracks the concept everywhere; the pooled max does. Headline test here = absorber recovery vs the supervised oracle (the unit admits absorbers the top-N marginal-attribution selection drops) PLUS knowledge-graph specialization-edge agreement with the supervised absorption diagnostic (Chanin 2409.14507). The sub-population-reweighting prediction does NOT live on this testbed.
  STORY 2 -- TOXICITY = SPLITTING (signature C, multi-sub-context). Toxicity manifests across sub-contexts (slurs vs threats vs demeaning insults), each carried by positively co-responding latents. Headline test here = worst-sub-context recall under sub-population reweighting. (First-letter absorbers are also per-word specialists, so the reweighting framing extends there in principle, but the PRE-REGISTERED reweighting test is on toxicity, where independent sub-context labels exist.)

  THE GROUPING-VS-POOLING ISOLATION (resolves the major methodology critique). The group-of-specialists mechanism predicts that ANY pool of multiple specialists beats a single hyperplane under reweighting. So unit > (f) is EXPECTED and is NOT evidence for grouping -- it shows only 'pooled specialists beat one hyperplane', a capacity/pooling effect. The grouping-isolating comparison is unit vs the COUNT-MATCHED marginal-attribution pools (g) and (h): all three pool the same number of directions, but (g)/(h) select members by MARGINAL attribution (which drops the absorber covering the under-served sub-context) while the unit selects by co-response grouping (which admits it). Pre-registered ORDERING on worst-sub-context recall: (f) single hyperplane < (g)/(h) marginal-attribution pools < unit co-response pool, with the unit-minus-(g)/(h) gap GROWING in reweighting magnitude. That unit-minus-(g)/(h) gap is mechanistically the SAME quantity as C3 absorber-recovery: the unit wins because it carries the absorber that (g)/(h) drop. HONEST NEGATIVE: if the unit ties (g)/(h) on the slice, robustness is 'just pooling' and grouping's contribution reduces to absorber-recovery (C3) + auditability -- reported plainly.

  DEGENERATE-CONSTRUCTION GUARD (resolves the 'trivially-true-by-construction' critique). Sub-contexts are defined from INDEPENDENT labels fixed before any unit-vs-probe comparison: civil_comments toxicity sub-attribute floats (toxicity/obscene/insult/threat/identity_attack) and CEBaB aspect levels -- never from the unit's members. 'Under-served' sub-contexts are determined on the dense probe (f) ALONE, blind to the unit. The reweighting-magnitude axis (the test mixing-weight sweep) is pre-registered. We report a NON-TRIVIALITY CHECK: the dense probe genuinely collapses (recall drop above a pre-set threshold) on these independently-defined sub-contexts; if it does not collapse, the reweighting test is void and reported as such.

  THE THREE NESTED CLAIMS (each with its own baseline, pre-registered for clean attribution). (A) 'Counterfactual supervision helps' (NOT ours): naive diff-of-means/probe on raw labels -> counterfactually-matched probe on content-flip residual deltas. Expected true; not claimed. (B) 'Counterfactual-INVARIANCE supervision helps' (conceded, non-SAE): matched probe -> surface-invariant matched probe via LEACE / mean-projection erasure (Belrose 2024) of the surface direction estimated from surface-flip pairs (Veitch 2021 conditional-MMD is a drop-first alternative construction). (C) 'GROUPING helps' (THE contribution): C1 -- the unit beats the best raw latent and observational clusters on classification; C2 -- the unit matches-or-beats the supervised oracle pool (g) and the count-and-pool-matched probe (h); C3 -- the mechanistic backbone: low Jaccard with observational clusters AND wins on the differing members, recovering absorbers (g)/(h) drop. C1 + C3 are the headline and hold regardless of whether the dense probe is beatable on aggregate F1.

  SINGLE ADMISSION RULE (one falsifiable procedure). Against a shuffled-pair null (permute which member of each minimal pair is content-on; B=1000), admit a candidate unit iff it clears at least one signature AND passes unit-level surface invariance. Signature C (splitting): mean within-unit content-response correlation > 95th pct of the null. Signature K (absorption): pooled max-over-members content-response AUC minus best-single-member AUC > 95th pct of a MATCHED best-of-random-k null -- the random k drawn from CONTENT-RESPONSIVE latents matched on marginal content-response AUC to the candidate members (isolates COMPLEMENTARY COVERAGE rather than mere content-responsiveness) -- AND members mutually exclusive in firing (mean pairwise co-activation Jaccard < 0.1), AND each member's content-response precision on its own firing support >= 0.7. Unit-level surface invariance: pooled surface-response not above the shuffled-surface-pair null. We report, per concept, which signature cleared and the false-admit rate under BOTH the all-latent and the matched random-k null (target <= 0.05). Feature hedging (Chanin 2505.11756) is cited as a cause of inter-latent correlation but is NOT a grouping target (one merged latent cannot be grouped).

  ENGAGING THE LABEL-FREE GROUP-ROBUSTNESS LITERATURE (resolves the major novelty critique). Promoting the reweighting result makes the established competitors the label-free worst-group-robustness methods -- JTT (2107.09044), GEORGE (2011.12945), EIIL (2010.07249), LfF (2007.02561), and recent GIC / Evidential-Alignment / Diverse-Prototypical-Ensembles (2505.23027). These achieve worst-group robustness by inferring groups over EXAMPLES and RETRAINING with reweighted / group-DRO loss (or training a diverse prototype ensemble). Our contribution is a DIFFERENT ROUTE: we group FEATURES (discrete SAE latents) by interventional co-response, never retrain, and the recovered absorbers ARE the inferred sub-context specialists -- human-auditable, reusable for steering and model-diffing, and tied to a feature-level knowledge graph. We add (j) an oracle group-DRO dense probe trained WITH true sub-context labels (the robustness UPPER BOUND) and (k) a label-free group-inference dense probe (JTT/GEORGE-style: train probe, upweight high-loss examples or cluster representations to infer groups then group-DRO; no sub-context labels, like our unit). Pre-registered prediction: the unsupervised co-response unit APPROACHES (j)'s worst-sub-context recall WITHOUT using sub-context labels, and is competitive-or-better than (k) while being uniquely auditable; if (k) strictly beats the unit on recall, that is an honest negative (loss-reweighting wins for pure robustness, but the unit still delivers the auditable feature-level repair).

  HEADLINE SCOPE with honest effective-n (resolves the scope critique). The headline spans ~3 GENUINELY INDEPENDENT concept families: (1) TOXICITY (civil_comments / ParaDetox), with the 5 sub-attributes reported as WITHIN-family detail; (2) SENTIMENT (Kaushik 2020 human counterfactual IMDB); (3) RESTAURANT ASPECT-SENTIMENT (CEBaB), with food and service NESTED as ONE family -- they share the restaurant-review domain and are empirically positively correlated, and a single adverse SAE draw on that shared encoding would move both together, so we report the measured cross-aspect correlation explicitly rather than counting them as two independent draws. We report a CLUSTERED / hierarchical bootstrap CI (cluster by family; toxicity and CEBaB each contribute one family-level estimate). A 4th out-of-domain axis (formality via GYAFC parallel human rewrites, or spam) is a committed-if-time stretch to genuinely reach four. first-letter spelling = the controlled ABSORPTION mechanism testbed (outside the family count); bias_in_bios = a pre-registered BOUNDARY-NULL. A clean null at any stage is a publishable mechanism-level finding.
motivation: |-
  Single SAE latents are unreliable units of analysis. Feature absorption (a specific child latent suppresses a more general parent's firing, leaving the parent with unpredictable holes; Chanin 2409.14507, 2505.11756), feature splitting (one concept fragments across many latents), feature hedging (a narrow SAE merges correlated features into one polysemantic latent), and 'SAEs Do Not Find Canonical Units of Analysis' (ICLR 2025, 2502.04878) all converge on the same conclusion: no single latent reliably tracks a concept. AxBench (ICML 2025 spotlight, 2501.17148) makes the stakes concrete -- plain difference-of-means beats raw-latent SAE methods on concept detection and steering -- so any SAE-grouping method must clear strong simple baselines.

  The contribution lives squarely in clustering / feature-selection / classification for a learned knowledge representation (SAE features): we produce cluster-level units and a feature-level knowledge graph, evaluated on downstream classification (headline) with steering and model-diffing as generality demonstrations. Every existing post-hoc grouping method relies on OBSERVATIONAL signals -- which latents fire together (co-activation feature families) or which decoders point alike (geometry). But absorption is exactly the regime where observational signals break by construction: per Chanin, the parent and the absorbing child are hierarchical and the child fires only where the parent goes silent, so the two are MUTUALLY EXCLUSIVE in firing -- co-activation clustering provably cannot group them and their decoders need not be cosine-similar. This is a structural blind spot, not a tuning problem. The standard supervised remedy -- select the top-N latents by causal effect on a concept probe (SCR/TPP, Karvonen 2411.18895, built on Marks SHIFT) -- SILENTLY DROPS absorbed latents, because a latent that fires only in a narrow sub-context has low MARGINAL attribution even though it carries the concept there.

  TWO cross-field transfers motivate the method and its robustness mechanism. (1) Systems biology faced the identical grouping obstacle: co-regulated genes are often NOT co-expressed at baseline and reveal shared regulation only under perturbation, which is why differential co-expression methods (DiffCoEx, WGCNA) cluster genes by their CORRELATED RESPONSE TO A PERTURBATION rather than baseline co-expression. Mapping genes->SAE latents and a chemical/genetic perturbation->an input content counterfactual gives the grouping mechanism. (2) Distributionally-robust learning explains WHY the recovered unit should generalize, and pins down what must be controlled: an absorber is a dedicated detector for one sub-context, so a complementary-coverage unit is implicitly a GROUP-OF-SPECIALISTS, and a max-pool of specialists is robust to sub-population MIXING-WEIGHT shift in exactly the regime where a single ERM hyperplane (the surface-invariant probe) collapses on under-served minority sub-contexts (group-DRO; Mind-the-GAP 2403.09869). Crucially -- and this is the change this round -- the SAME mechanism predicts that a count-matched POOL of marginal-attribution-selected directions is also more robust than one hyperplane, so beating one hyperplane is a pooling effect; what isolates GROUPING is beating the count-matched marginal-attribution pool, which drops the very absorber the under-served sub-context needs.

  This places the robustness result alongside the label-free worst-group-robustness literature (JTT 2107.09044; GEORGE 2011.12945; EIIL 2010.07249; LfF 2007.02561; Diverse Prototypical Ensembles 2505.23027), which infer groups over EXAMPLES and RETRAIN with reweighted / group-DRO loss. Our route is orthogonal and, we argue, complementary: we group FEATURES on a frozen public SAE, never retrain, and the recovered absorbers are themselves the inferred sub-context specialists -- auditable (you can read which absorber covers which sub-context, as a knowledge graph), reusable for steering and model-diffing, and benchmarkable against an oracle group-DRO probe that DOES use sub-context labels. The insight an interpretability expert would not reach for: SAE absorption/splitting are structurally the same obstacle that (a) defeats baseline co-expression in biology and (b) makes ERM probes brittle under subpopulation shift -- so observational co-activation/geometry AND marginal-attribution selection are the wrong instruments, interventional co-response is the matched instrument, and the recovered absorbers ARE the latent subpopulations a robust classifier needs.

  If correct, this gives a training-free, single-GPU, human-auditable way to turn off-the-shelf public SAEs (Gemma Scope) into reliable concept units -- with a measurable recall recovery on absorbed sub-contexts, an auditable specialization graph, and a robustness story that approaches an oracle group-DRO probe without labels. If incorrect, the honest negatives are themselves actionable: that observational co-response equals interventional co-response (no gain from intervention); that grouping ties the count-matched marginal-attribution pool (robustness is pooling, not grouping); that the label-free group-inference probe beats the unit on recall (loss-reweighting wins for pure robustness); or that SAE units should be abandoned in favor of dense surface-invariant probes for robust classification.
assumptions:
- >-
  MINIMAL PAIRS ARE OBTAINABLE AT HIGH QUALITY, LOW COST, AND NON-CIRCULARLY. Primary content-flips use HUMAN-WRITTEN parallel
  corpora needing no LLM generation: ParaDetox (s-nlp, ACL 2022) toxic<->neutral for toxicity, Kaushik 2020 (ICLR) crowd-revised
  IMDB minimal pairs for sentiment, and CEBaB (Abraham 2022) human aspect-edited restaurant reviews for the restaurant aspect-sentiment
  family. For rare toxicity sub-attributes (threat, identity_attack) and first-letter substitutions, LLM-generated pairs (OpenRouter,
  well under $10) are each LLM-judge-scored for content-flipped + surface-preserved, with reported pass rates and sensitivity
  to the pair-quality threshold. Any activation-space content edit, if used, is derived from an INDEPENDENT held-out diff-of-means
  on DISJOINT data, never from the SAE latents being grouped, so there is no circularity.
- >-
  THE MECHANISM IS PILOT-GATED IN BOTH HEADLINE REGIMES BEFORE THE FULL RUN. Absorption arm (first-letter): the general latent
  (max encoder-cosine with the LR first-letter probe, per Chanin 2409.14507) and its absorbers (ablation effect on the correct-minus-mean-incorrect-letter
  logit where the general latent is silent) show COMPLEMENTARY COVERAGE -- mutually-exclusive support whose pooled response
  tracks the flip above the shuffled-pair null. Splitting arm (toxicity): MULTIPLE latents carry toxicity with positively-correlated
  content-response above null AND a pooled unit beats both the single best toxicity latent and the matched diff-of-means on
  a held-out IID slice. Each arm has a symmetric decision rule; the headline proceeds with a regime only if its pilot confirms
  it, and a pilot null is reported as a mechanism finding.
- >-
  THE WIN, IF IT OCCURS, IS ATTRIBUTABLE TO GROUPING -- NOT TO EXTRA SUPERVISION, CAPACITY, OR MERE POOLING. The conceded
  dense baseline (f, surface-invariant matched probe) is information-matched via LEACE/mean-projection erasure of the surface
  direction. The supervised oracle pool (g, SCR/TPP top-N latents) controls for label selection. The count-and-pool-matched
  probe (h, max-pool over EXACTLY #members raw residual directions selected by the SAME SCR/TPP attribution as (g)) controls
  member-count AND pooling nonlinearity. The grouping-isolating prediction is the pre-registered ORDERING (f) < (g)/(h) <
  unit on worst-sub-context recall: the unit beats the count-matched marginal-attribution pools (g)/(h), not merely the single
  hyperplane (f), and the unit-minus-(g)/(h) gap is the same quantity as C3 absorber-recovery. Beating only (f) is conceded
  to be a pooling effect, not grouping evidence.
- >-
  THE ROBUSTNESS GAP IS DRIVEN BY SUB-POPULATION REWEIGHTING, IS NOT TRUE-BY-CONSTRUCTION, AND IS BENCHMARKED AGAINST THE
  LABEL-FREE GROUP-ROBUSTNESS LITERATURE. Sub-contexts are defined from INDEPENDENT labels (civil_comments sub-attribute floats;
  CEBaB aspect levels) frozen before any unit-vs-probe comparison; 'under-served' is determined on the dense probe (f) alone;
  the reweighting-magnitude axis is pre-registered; and a non-triviality check confirms (f) genuinely collapses on those independently-defined
  sub-contexts. We decompose the shift into (i) surface-only paraphrase (unit NOT predicted to win), (ii) sub-population reweighting
  (unit predicted to win on worst-sub-context recall, growing with magnitude), (iii) natural domain shift (attributed to i
  or ii). We benchmark against an oracle group-DRO dense probe (j, uses sub-context labels = upper bound) and a label-free
  group-inference dense probe (k, JTT/GEORGE-style, no labels); the unit is predicted to approach (j) without labels and be
  competitive-or-better than (k) while uniquely auditable. If the gap does not concentrate on (ii), or the unit ties (g)/(h)
  on the slice, the headline mechanism is falsified and reported.
- >-
  Off-the-shelf Gemma Scope SAEs on Gemma-2-2b expose latent counterfactual responses measurable above noise on a single GPU
  for a few thousand minimal pairs per concept, and the chosen attributes have enough labeled/templatable data (civil_comments
  sub-attribute floats, CAD-IMDB, CEBaB aspect labels, ParaDetox) to build minimal pairs and natural-shift test splits. Absorption
  is more severe at WIDER SAEs and splitting at larger width, so SAE width/layer is a robustness axis (16k canonical primary;
  65k is a drop-first stress point). For the model-diffing demonstration, paired base (gemma-scope-2b-pt) and instruction-tuned
  (gemma-scope-2b-it) SAEs are available off the shelf.
investigation_approach: |-
  DEPTH-FIRST EXECUTION ORDER (resolves the feasibility/breadth risk and the all-three-tasks scope critique). TIER 0 (must complete): two-arm STEP-0 pilot. TIER 1 (the headline, must complete): claims C1+C3 (beat raw latent + observational clusters; mechanistic backbone / absorber recovery vs the oracle pool (g) and count-matched pool (h)) plus claim B vs C2 on the toxicity family + sentiment with the surface-invariant probe and the oracle/count-matched pools; first-letter absorber recovery + KG-edge agreement; the shift DECOMPOSITION (surface-only + sub-population-reweighting + natural) on toxicity, including the pre-registered ORDERING (f)<(g)/(h)<unit and the oracle group-DRO (j) + label-free group-inference (k) robustness baselines; clustered-CI aggregate over the ~3 families. TIER 2 (attempt if Tier 1 lands; FIRST stretch, committed because the goal foregrounds steering): the CEBaB restaurant aspect-sentiment family AND ONE DECISIVELY-executed steering case (matched on-target effect, KL on unrelated prompts + fluency, bootstrap CIs, engaging 2505.20063/AxBench -- not illustrative). DROP-FIRST stretch (only if everything above lands): a minimal null-floored MODEL-DIFFING check (does the unit detect a base-vs-it concept-usage shift more reliably than the best single latent, above a shuffle null, using paired pt/it Gemma Scope SAEs?) so all three goal tasks are at least touched; plus the 4th out-of-domain axis (GYAFC formality / spam), 65k-width stress point, Veitch-MMD alternative, LLM-paraphrase secondary shift. Steering and model-diffing are GENERALITY demonstrations, not load-bearing. PRE-COMMITTED counts: >=800 content-flip pairs and >=800 surface-flip pairs per family for the bootstrap CIs.

  STEP 0 -- TWO-ARM DE-RISKING PILOT (run first, ~1-2 GPU-hours). ARM A (absorption, first-letter): find the general first-letter latent and its absorbers; build first-letter content-flip pairs; measure (a) correlated content-response (expected low/disjoint) and (b) COMPLEMENTARY coverage (pooled max tracks the flip where members have holes) vs the shuffled-pair null. ARM B (splitting, toxicity): on ParaDetox/civil_comments, measure how many latents carry toxicity, whether their content-response profiles are positively correlated above null, and whether the pooled unit beats the single best toxicity latent and the matched diff-of-means on a held-out IID slice. Symmetric decision rules; proceed with a regime as headline only if its pilot clears the null.

  COUNTERFACTUAL SIGNAL. Encode every text and its counterfactual with a frozen Gemma Scope residual-stream SAE (layer ~12, width 16k canonical). Per latent: content-response = delta(activation) under content-flip; surface-response = delta under surface-flip. Aggregate into per-latent response profiles across contexts.

  CLUSTERING METHOD (the in-scope contribution). Build a latent-by-context content-response matrix. Cluster latents with a differential-correlation affinity (DiffCoEx-style) for signature C and a coverage-complementarity term for signature K, via agglomerative clustering / graph community detection on the affinity. Finalize each candidate unit with the SINGLE ADMISSION RULE (signature C OR matched-null signature K + mutual-exclusivity + precision floor, AND unit-level surface invariance); report the cleared signature per concept and the false-admit rate under both nulls. Emit human-auditable unit definitions (member latents, logit-lens tokens, conditioning contexts) and directed specialization edges (a member responsive only in a sub-context = absorbed/split child) = a feature-level knowledge graph.

  WORKED EXAMPLES. Toxicity unit (splitting): members = {profanity/slur latent, demeaning-insult latent, aggressive-imperative latent}; under ParaDetox detox all three drop together (signature C); pooled max tracks toxicity; pooled surface-response to paraphrase ~ 0. First-letter unit (absorption): members = {general 'starts-with-L' latent (silent on 'lion'/'London'), 'lion'-absorber, 'London'-absorber}; no member tracks 'starts-with-L' everywhere, pooled max does (signature K); members never co-fire (Jaccard ~ 0); pooled surface-response ~ 0.

  BASELINES (matched baselines are primary). (a) best raw single latent; (b) observational co-activation clustering / feature families; (c) decoder-geometry clustering; (d) counterfactually-matched diff-of-means; (e) counterfactually-matched linear probe; (f) surface-invariant matched probe = (d)/(e) with the surface-flip direction LEACE/mean-projection erased (Belrose 2024) -- the conceded SINGLE-HYPERPLANE non-SAE baseline; (g) supervised oracle pool = top-N latents by SCR/TPP probe-attribution (Karvonen 2411.18895 / Marks SHIFT); (h) count-and-pool-matched probe = max-pool over EXACTLY #members raw residual directions selected by the SAME SCR/TPP attribution as (g); (i) unmatched diff-of-means / linear probe on raw labels; (j) ORACLE GROUP-DRO dense probe trained WITH true sub-context labels = robustness UPPER BOUND; (k) LABEL-FREE GROUP-INFERENCE dense probe (JTT/GEORGE-style: ERM probe -> upweight high-loss examples or cluster representations to infer groups -> group-DRO; no sub-context labels, like the unit).

  EVAL -- HEADLINE BACKBONE (reported regardless of dense-probe competitiveness): (1) co-response units have low Jaccard with co-activation/geometry clusters above the stability/shuffled-pair null; (2) units win specifically on the differing members -- sliced RECALL on the sub-contexts where the best latent / observational clusters / the oracle pool (g) / the count-matched pool (h) have holes, including absorbers (g)/(h) drop; (3) knowledge-graph specialization edges agree with the supervised absorption diagnostic (2409.14507) on first-letter. EVAL -- CLASSIFICATION + ROBUSTNESS: unit-pooled activation (max/sum over members) as classifier on IID and under the THREE decomposed shifts; report F1/AUC AND worst-sub-context recall. The GROUPING-ISOLATING prediction is the ORDERING (f) < (g)/(h) < unit on worst-sub-context recall with the unit-minus-(g)/(h) gap GROWING in reweighting magnitude; the (g)/(h)-minus-(f) gap is the (expected, non-grouping) pooling effect. Robustness BOUNDS: unit approaches (j) without sub-context labels and is competitive-or-better than (k) while auditable. Aggregate F1 vs (f) reported honestly (tie acceptable). DEGENERATE-CONSTRUCTION GUARD applied throughout: independent sub-context labels frozen first, under-served determined on (f) alone, reweighting axis pre-registered, non-triviality check on (f)'s collapse. CLUSTER-STABILITY: bootstrap over minimal pairs (adjusted Rand / Jaccard), shuffled-pair null for the affinity, sensitivity to pairs-per-concept. Aggregate across ~3 families with a CLUSTERED bootstrap CI; report measured CEBaB food-service cross-aspect correlation.

  STEERING (Tier 2, ONE decisive case). Steer with the toxicity unit's shared content-response direction vs best single latent vs the matched surface-invariant diff-of-means; measure on-target effect and side-effects (KL on unrelated prompts, fluency) at MATCHED on-target effect with bootstrap CIs; engage 'SAEs Are Good for Steering -- If You Select the Right Features' (2505.20063) and the AxBench protocol.

  MODEL-DIFFING (drop-first stretch, minimal null-floored). Using paired Gemma Scope pt/it SAEs, test whether the co-response unit detects a base-vs-instruction-tuned shift in concept usage more reliably than the best single latent, above a shuffle null. Touches the third goal task without being load-bearing.

  HONEST FAILURE-MODE REPORTING. Dependence on counterfactual quality (pass rates); concepts with no surface-invariant co-responding/complementary group; regimes where co-response collapses to co-activation (no gain over observational); the unit tying the count-matched pools (g)/(h) on sliced recall (robustness is pooling, not grouping -- grouping reduces to absorber-recovery + auditability); the label-free group-inference probe (k) beating the unit on recall (loss-reweighting wins for pure robustness); the dense surface-invariant probe matching the unit on sliced recall too (invariance supervision suffices, grouping adds only auditability); the oracle pool (g) tying the unit (selection not grouping); the reweighting test void because (f) does not collapse on independently-defined sub-contexts; co-response too noisy to cluster (ARI ~ null); a pilot arm showing neither correlated nor complementary above-null structure; compute/SAE-width sensitivity; bias_in_bios boundary-null.
success_criteria: >-
  CONFIRMED if, pre-registered in this nesting: (1) the two-arm STEP-0 pilot confirms above-null structure in at least one
  regime (positively-correlated content-response for splitting and/or complementary coverage for absorption), with the toxicity
  arm also showing a pooled IID edge over the best single latent and the matched diff-of-means; (2) HEADLINE BACKBONE: co-response
  units have low Jaccard with co-activation/geometry clusters (above the stability/shuffled-pair null) AND win on the differing
  members -- sliced recall on the sub-contexts where the best latent, observational clusters, the oracle pool (g), and the
  count-matched pool (h) have holes, including recovered absorbers -- on first-letter (absorption: absorber-recovery-vs-oracle
  + KG-edge agreement with 2409.14507) AND on at least one safety concept; (3) C1: the unit beats the best raw single latent
  and observational co-activation/geometry clustering on classification across the ~3 families (clustered-CI aggregate); (4)
  C2 + GROUPING ISOLATION: the unit matches-or-beats the oracle pool (g) and the count-and-pool-matched probe (h) on classification,
  AND -- the headline grouping test -- shows the pre-registered ORDERING (f) single hyperplane < (g)/(h) count-matched marginal-attribution
  pools < unit, with a POSITIVE unit-minus-(g)/(h) worst-sub-context recall gap that GROWS with the measured sub-population-reweighting
  magnitude (the unit-minus-(f) gap alone is conceded to be a pooling effect, not grouping evidence); (5) ROBUSTNESS BOUNDS:
  the unit APPROACHES the oracle group-DRO probe (j)'s worst-sub-context recall WITHOUT using sub-context labels, and is competitive-or-better
  than the label-free group-inference probe (k) while uniquely auditable; aggregate F1 vs the surface-invariant probe (f)
  may tie; (6) ADMISSION + CONSTRUCTION INTEGRITY: false-admit rate <= 0.05 under BOTH the all-latent and matched random-k
  nulls; cluster assignments stable across bootstrap resamples (adjusted Rand/Jaccard above null); KG specialization edges
  agree with the supervised absorption diagnostic (2409.14507) on first-letter; sub-contexts defined from independent labels
  frozen first, under-served determined on (f) alone, and the non-triviality check confirms (f) genuinely collapses on those
  sub-contexts. TIER 2 (confirmatory only): one steering case where the unit direction achieves lower KL side-effects than
  best-single-latent and the matched diff-of-means at matched on-target effect. HONEST NEGATIVES, each publishable: co-response
  grouping ties observational co-activation grouping (no gain from intervention); the unit ties the count-matched pools (g)/(h)
  on sliced recall (robustness is pooling, not grouping -- contribution reduces to absorber-recovery + auditability); the
  label-free group-inference probe (k) beats the unit on recall (loss-reweighting wins for pure robustness, unit still delivers
  auditable repair); the dense surface-invariant probe matches the unit on sliced recall under reweighting (grouping then
  contributes only auditability + the knowledge graph); the oracle pool (g) ties the unit (selection not grouping); the gap
  does NOT concentrate on the sub-population-reweighting component, or (f) does not collapse on independently-defined sub-contexts
  (headline mechanism falsified/void); co-response too noisy to cluster (ARI ~ null); a pilot arm shows neither correlated
  nor complementary above-null structure. bias_in_bios is a pre-registered boundary-null, not method failure.
related_works:
- >-
  AxBench: Steering LLMs? Even Simple Baselines Outperform Sparse Autoencoders (Wu et al., ICML 2025 spotlight, 2501.17148):
  on Gemma-2-2B/9B, difference-in-means is the strongest concept-detection method and SAEs are not competitive. This sets
  our bar. We differ by making diff-of-means maximally fair (counterfactually matched AND surface-invariant via concept erasure),
  then scoping the contribution to (a) beating raw latents + observational clusters, (b) recovering absorbers that marginal-attribution
  selection drops, and (c) a sliced sub-population-shift recall gap isolated from pooling -- NOT a blanket aggregate-F1 win.
- >-
  Sparse Autoencoders Do Not Find Canonical Units of Analysis (Bussmann et al., ICLR 2025, 2502.04878): uses SAE stitching
  and meta-SAEs to argue SAEs do not learn canonical units; its remedy is geometric/training-based. We propose a BEHAVIORAL
  unit defined by counterfactual co-response and unit-level surface invariance, evaluated on downstream classification + steering
  + model-diffing, with no retraining.
- >-
  Feature Hedging: Correlated Features Break Narrow SAEs (Chanin, Dulka, Garriga-Alonso, 2505.11756): ABSORPTION learns gerrymandered
  latents (worse at WIDER SAEs, both features tracked across mutually-exclusive latents via a parent->child hierarchy) vs
  HEDGING merges correlated features into a SINGLE polysemantic latent (worse at NARROWER SAEs). We use this to scope grouping
  to splitting+absorption (a hedged single latent is not groupable) and to treat correlation/hierarchy as the mechanistic
  cause our interventional probe exposes.
- >-
  A is for Absorption (Chanin et al., 2409.14507, NeurIPS): a SUPERVISED DIAGNOSTIC -- identify the first-letter latent by
  max encoder-cosine with an LR probe and use ablation on the correct-minus-incorrect-letter logit to find the absorbing latent.
  It DETECTS absorption on individual latents; it does not GROUP parent+absorbers into a usable unit. We use it as a partial
  ORACLE for the pilot and to validate knowledge-graph edges; our contribution is the unsupervised grouping/repair.
- >-
  Counterfactual Invariance to Spurious Correlations (Veitch, D'Amour, Yadlowsky, Eisenstein, NeurIPS 2021, 2106.00545): an
  MMD-based regularizer enforcing the counterfactual-invariance signature, with conditional MMD in the anti-causal direction
  (as for toxicity/sentiment). We import this as a DROP-FIRST alternative construction of the surface-invariant baseline (f);
  the primary construction is LEACE/mean-projection erasure.
- >-
  LEACE: Perfect linear concept erasure in closed form (Belrose et al., 2306.03819): we erase the surface-flip direction to
  build the surface-invariant probe (f) -- a strong, principled non-SAE baseline. LEACE erases a single/low-rank TRAINING-estimated
  subspace, which motivates why one hyperplane cannot remove multi-dimensional/context-dependent surface confounds that differ
  across domains; but per the reviewer we now treat beating one hyperplane as a pooling effect and isolate grouping against
  count-matched pools.
- >-
  SHIFT / SCR / TPP SAE evaluation (Marks et al. 2024; Karvonen et al. 2411.18895): these SELECT individual SAE latents by
  ranking causal effect on a concept probe (top-N), then ablate the set; they do NOT cluster latents by interventional co-response.
  This is exactly our supervised ORACLE-POOL baseline (g) and, count-matched, the pool (h); a latent firing only in a narrow
  sub-context (an absorber) has low marginal attribution and is silently dropped -- the specific gap our coverage grouping
  fills, and the quantity the unit-minus-(g)/(h) sliced-recall gap measures.
- >-
  Just Train Twice (JTT, Liu et al., ICML 2021, 2107.09044), GEORGE / No Subclass Left Behind (Sohoni et al., NeurIPS 2020,
  2011.12945), Environment Inference for Invariant Learning (EIIL, Creager et al., ICML 2021, 2010.07249), Learning from Failure
  (LfF, Nam et al., NeurIPS 2020, 2007.02561): the label-free worst-group-robustness family. They achieve robustness by INFERRING
  GROUPS OVER EXAMPLES (high-loss upweighting, feature-space clustering of data points, environment inference) and RETRAINING
  with reweighted / group-DRO loss. Our route is orthogonal: we group FEATURES (discrete SAE latents) by interventional co-response,
  never retrain, and the recovered absorbers ARE the inferred sub-context specialists -- human-auditable and reusable for
  steering/model-diffing. We add an oracle group-DRO probe (uses sub-context labels = upper bound) and a label-free group-inference
  probe (JTT/GEORGE-style) as direct robustness baselines, and predict the unit approaches the oracle without labels.
- >-
  Diverse Prototypical Ensembles (2505.23027): trains an ensemble of N diverse prototypes per class on FROZEN DENSE features
  (validation subset), with an inter-prototype-similarity diversity loss + bagging, to capture subpopulation-specific patterns
  without group labels. Conceptually the closest 'ensemble-of-specialists for subpopulation shift', but it TRAINS learnable
  prototype vectors on dense representations; we group pre-existing DISCRETE SAE latents by interventional co-response with
  no training, yielding auditable concept atoms (not opaque prototypes) and a feature-level knowledge graph.
- >-
  Group Distributionally Robust Optimization and subpopulation-shift robustness (Sagawa et al. group-DRO; Mind the GAP: Group-Aware
  Priors, 2403.09869): a single ERM model collapses on under-served minority subgroups under mixing-weight shift; group-aware
  methods recover worst-group performance. We do NOT propose a new DRO method or theorem; we BORROW this as the a-priori mechanism
  explaining why a group-of-specialists unit out-generalizes a single hyperplane -- and, per the reviewer, we use the SAME
  mechanism to predict a count-matched marginal-attribution pool is also robust, so grouping must be isolated against THAT
  pool, not the hyperplane.
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
  human-written counterfactual minimal pairs for sentiment (IMDB) and ASPECT concepts (food/service/ambiance/noise in restaurant
  reviews), with out-of-domain sources. We use CAD as one independent axis and CEBaB as ONE restaurant aspect-sentiment family
  (food+service nested, cross-aspect correlation reported), plus cross-domain reviews as a natural shift; these supply non-circular
  pairs and independent sub-context labels for the degenerate-construction guard, not the grouping method.
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
  A dual cross-field transfer, sharpened this round to isolate the mechanism. The GROUPING mechanism is a Level-3 (methodological)
  import from systems biology's differential co-expression / perturbation co-response module discovery (DiffCoEx, WGCNA):
  cluster units by their CORRELATED RESPONSE TO A PERTURBATION, not by baseline co-expression, because co-regulated genes
  are frequently not co-expressed until perturbed -- mapping genes->SAE latents and a chemical/genetic perturbation->an input
  content counterfactual. The ROBUSTNESS mechanism is a Level-1/2 import from distributionally-robust learning / subpopulation-shift
  research (group-DRO; Mind-the-GAP 2403.09869) and, newly this round, the label-free worst-group-robustness subfield (JTT,
  GEORGE, EIIL, LfF, Diverse Prototypical Ensembles): a single ERM hyperplane collapses on under-served minority subgroups
  under mixing-weight shift, whereas a union of specialists is robust -- and an absorber is precisely a specialist for one
  latent sub-context. The key refinement the reviewer prompted: because the SAME mechanism predicts that a count-matched POOL
  of marginal-attribution-selected directions is also robust, beating one hyperplane is a pooling effect; what isolates GROUPING
  is beating the count-matched marginal-attribution pool, which drops the absorber the under-served sub-context needs -- so
  the headline robustness test is the unit-vs-pool comparison, benchmarked against an oracle group-DRO probe (with sub-context
  labels) the unit must approach WITHOUT labels. These fuse with (i) causal ML's counterfactual invariance (Veitch 2021) and
  concept-erasure (LEACE, Belrose 2024) for the conceded surface-invariant baseline; (ii) NLP minimal-pair counterfactuals
  (ParaDetox, Kaushik 2020 CAD, CEBaB aspects) for non-circular perturbations and independent sub-context labels; and (iii)
  a complementary-coverage (set-cover-style) extension for absorption. The unifying insight an interpretability expert would
  not reach for: SAE absorption/splitting are structurally the same obstacle that (a) defeats baseline co-expression in biology
  and (b) makes ERM probes brittle under subpopulation shift -- and the label-free group-robustness literature already attacks
  (b) by reweighting EXAMPLES and retraining, whereas grouping FEATURES gives a training-free, auditable route to the same
  end where the recovered absorbers ARE the latent subpopulations.
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
    signature is reported per concept and the false-admit rate under both nulls (target <= 0.05).
- term: Surface-invariant matched probe (baseline f, single hyperplane)
  definition: >-
    A counterfactually-matched diff-of-means/linear probe on content-flip residual deltas, made surface-invariant by ERASING
    the surface-flip direction via LEACE / mean-projection (Belrose 2024). It is a SINGLE hyperplane after erasing one training-estimated
    surface subspace; per the reviewer, the unit beating it is conceded to be a POOLING effect (multiple specialists vs one
    hyperplane), not grouping evidence.
- term: Supervised oracle pool (baseline g)
  definition: >-
    Pools the top-N SAE latents selected by a supervised probe-attribution causal-effect criterion (SCR/TPP, Karvonen 2411.18895
    / Marks SHIFT). Because it ranks by MARGINAL attribution it silently drops absorbed latents firing only in narrow sub-contexts;
    the co-response unit must match/beat it to show grouping by co-response STRUCTURE adds value over flat supervised selection.
- term: Count-and-pool-matched probe (baseline h)
  definition: >-
    Max-pool over EXACTLY the number of raw residual-stream directions equal to the admitted unit's member count, selected
    by the SAME SCR/TPP attribution criterion as (g), on the matched paired activations. It controls member-count AND pooling
    nonlinearity, so any residual unit advantage over it is attributable to co-response grouping structure rather than to
    count or max-pool. The unit-vs-(h) sliced-recall comparison is the GROUPING-ISOLATING headline test.
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
    and auditable. The unit is predicted to be competitive-or-better while uniquely auditable.
- term: Grouping-vs-pooling isolation
  definition: >-
    The pre-registered ORDERING (f) single hyperplane < (g)/(h) count-matched marginal-attribution pools < unit co-response
    pool on worst-sub-context recall. Beating (f) shows only that pooled specialists beat one hyperplane (a capacity/pooling
    effect predicted by the same group-DRO mechanism); beating the count-matched pools (g)/(h) -- which the same mechanism
    predicts are also robust -- is what isolates co-response GROUPING, and equals the C3 absorber-recovery quantity.
- term: >-
    Worst-sub-context recall under sub-population reweighting (headline classification slice)
  definition: >-
    Recall on the sub-contexts a training-fit dense probe under-serves, evaluated as the test mixture is re-weighted toward
    those sub-contexts. Sub-contexts are defined from INDEPENDENT labels frozen before any comparison and 'under-served' is
    determined on the dense probe (f) alone; the complementary-coverage unit is predicted to keep this recall stable while
    a single hyperplane AND the count-matched marginal-attribution pool collapse.
- term: Degenerate-construction guard
  definition: >-
    The set of pre-registrations that prevent the reweighting headline from being true-by-construction: sub-contexts defined
    from independent labels fixed first (never from the unit's members), under-served determined on the dense probe alone,
    a pre-registered reweighting-magnitude axis, and a non-triviality check confirming the dense probe genuinely collapses
    on those independently-defined sub-contexts (else the test is void).
- term: Group-of-specialists (robustness framing)
  definition: >-
    The view that a complementary-coverage unit's members are dedicated detectors for disjoint sub-contexts, making the max-pooled
    unit implicitly group-aware and robust to sub-population MIXING-WEIGHT shift. Borrowed framing (group-DRO; Mind-the-GAP
    2403.09869), not a new theorem; the same framing predicts ANY count-matched pool is robust, which is why grouping is isolated
    against the pool, not the hyperplane.
- term: Shift decomposition
  definition: >-
    Splitting the evaluation shift into three controlled conditions -- (i) surface-only paraphrase (unit NOT predicted to
    win), (ii) sub-population reweighting (unit predicted to win on worst-sub-context recall vs the count-matched pool), and
    (iii) natural domain shift (attributed to i or ii) -- so the unit-minus-pool gap is attributed to a specific, mechanism-aligned
    component.
- term: Reliable unit of analysis
  definition: >-
    A human-auditable group of SAE latents that tracks a concept dependably across surface variation and sub-population reweighting
    -- recovering recall that absorption/splitting destroy at the single-latent level and that marginal-attribution selection
    drops -- reusable as a classifier (headline) and secondarily for steering and model-diffing.
summary: >-
  SAE latents encoding one concept are often mutually exclusive in firing (feature absorption and splitting), so observational
  co-activation, decoder geometry, and marginal-attribution selection all structurally miss the right members; clustering
  latents instead by how they jointly track a content counterfactual (correlated co-response for splitting, complementary
  coverage for absorption, admitted by one null-anchored rule) recovers auditable multi-member concept units. The headline
  tests isolate GROUPING from mere pooling: the unit must recover absorbers that a count-matched marginal-attribution pool
  drops on the first-letter testbed, and keep worst-sub-context recall stable under sub-population reweighting where that
  same count-matched pool -- not just a single hyperplane -- collapses, approaching an oracle group-DRO probe's robustness
  without using sub-context labels.
</previous_hypothesis>

<previous_review>
Critiques from the previous review. Check which ones have been addressed
in the revised hypothesis. Do NOT re-raise critiques that have been adequately fixed.
Only re-raise if the fix is insufficient.

- [MAJOR] (rigor) The statistical backbone for the aggregate headline is thin, and the now-central contrast has no power analysis. (1) The aggregate is a clustered/hierarchical bootstrap over ~3 family-level clusters (toxicity, sentiment, restaurant-aspect). A bootstrap over 3 clusters cannot yield an informative population-level CI — between-cluster variance is essentially unestimable with so few clusters — so the 'across ~3 families' aggregate is descriptive at best, not inferential. (2) The promoted metric, worst-sub-context recall on under-served/minority sub-contexts, is by construction computed on the SMALLEST slices, where recall is high-variance; and the key prediction (a positive unit-minus-(g)/(h) gap that GROWS with reweighting magnitude) has no stated MDE or sample-size justification. There is a real risk the central result lands as an inconclusive wide CI rather than a clean win or an honest null, which would waste the run.
  Action: (a) Make per-concept / per-family effect sizes with within-family bootstrap CIs the PRIMARY statistical object and frame the cross-family number as descriptive (or add the 4th out-of-domain axis to reach 4 clusters, still acknowledging the limit). (b) Provide an a-priori MDE for the unit-minus-(g)/(h) worst-sub-context-recall gap given expected minority-sub-context counts at each reweighting level, and size the >=800-pair budget against it (minimum examples per under-served sub-context to detect a gap of magnitude X). (c) Pre-register a paired bootstrap on the per-pair gap (unit - (g)/(h)) rather than comparing two marginal CIs.
- [MAJOR] (scope) Execution complexity grew with the revision and now threatens clean completion of even Tier 1. The design spans 11 baselines (a-k), including two newly-added non-trivial TRAINED probes — (j) an oracle group-DRO dense probe and (k) a JTT/GEORGE-style label-free group-inference probe, each with its own training/tuning loop — plus two regime testbeds, >=3 concept families, the first-letter absorption suite with the Chanin diagnostic, a 3-way shift decomposition, cluster-stability bootstraps, steering, and model-diffing. Tier 1 as written (C1+C3 + B/C2 + shift decomposition + the ordering + (j)/(k)) is a very large body of work; a half-finished Tier 1 yields a weak paper, and (j)/(k) materially raise that risk.
  Action: Carve out an explicit minimal LOAD-BEARING subset inside Tier 1 — e.g., C1 + C3 absorber-recovery + KG-edge agreement on first-letter + the unit-vs-(g)/(h) ordering on the single best-powered toxicity family — and mark everything else (second/third family, (k), shift-decomposition condition iii, steering, model-diffing) as demotable without invalidating the headline. State a hard wall-clock/GPU-hour budget per tier so the run can be triaged, and pre-register which results are dropped first under time pressure.
- [MINOR] (clarity) The title and one-sentence headline lead with the worst-sub-context-recall / group-DRO / grouping-isolation story, but the MVP explicitly demotes 'all sub-population-shift robustness results' to 'supporting evidence layered on' the C1+C3 backbone and pre-registers aggregate-F1 parity as acceptable. A top-down reader will expect the robustness result to be load-bearing and may judge the paper by it; if it ties or lands as an honest null (an explicitly anticipated outcome), the mismatch reads as a failed headline rather than the planned supporting-evidence result.
  Action: Re-lead the title and the one-sentence headline with C1+C3 (auditable units that recover the absorbers marginal-attribution selection drops, beating raw latents and observational clusters), and present worst-sub-context recall + the grouping-vs-pooling ordering as the sharp SECOND, supporting contribution. Keep the robustness clause but stop promising it in the title.
- [MINOR] (rigor) The 'grouping-vs-pooling isolation' label is slightly misleading: the unit-vs-(g)/(h) comparison holds pool SIZE fixed and varies only HOW members are chosen (co-response membership vs marginal-attribution ranking). Both arms pool, so what is isolated is the membership/SELECTION criterion, not 'grouping vs pooling' as a structural distinction. Separately, the signature-K matched best-of-random-k null may be conservative at small member counts k (max-over-k already buys a pooling boost from the matched content-responsive draws), risking an under-powered absorption-admission test exactly where members are few.
  Action: Reframe the contrast as 'co-response selection vs marginal-attribution selection at matched pool size' (the unit's clustering IS the selection rule), and state plainly that the structural claim reduces to: co-response membership admits the absorber that marginal-attribution ranking drops. Add a one-line justification of signature-K power at the expected small k (report the random-k null's spread and the minimum coverage-gain detectable at k=2-3).
- [MINOR] (scope) The stated goal requires three downstream tasks (classification, steering with side-effect measurement, model-diffing). The design keeps classification load-bearing, steering a single Tier-2 case, and model-diffing a drop-first stretch. The revision's commitment to a decisive steering case plus a minimal null-floored model-diffing check adequately answers the prior review, but a goal-aligned ICLR reviewer may still penalize under-delivery on two of the three required tasks if the run truncates at Tier 1.
  Action: Pre-commit a truncation fallback so that even if the run stops at Tier 1, a single null-floored steering result AND a single null-floored model-diffing result are produced (one concept each), and state explicitly in the paper that both are generality demonstrations, not load-bearing. If feasible, promote the model-diffing check into the same Tier-2 bracket as steering so both goal tasks are touched whenever Tier 1 lands.
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

### [2] HUMAN-USER prompt · 2026-06-17 13:06:34 UTC

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

### [3] SKILL-INPUT — aii-web-tools · 2026-06-17 13:09:06 UTC

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

### [4] SYSTEM-USER prompt · 2026-06-17 13:12:32 UTC

```
<validation-feedback>
Attempt 1 failed validation.

Schema validation found 1 problem — fix ALL of them at once:
  - at `relation_rationale`: 'Same interventional-co-response-grouping frame; re-led title to C1+C3, added a-priori MDE/paired bootstrap, tiering, and renamed selection isolation.' is too long (at most 120 characters, got 149)
Every required field must be present and every field type must match the schema.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```
