# upd_hypo — test_idea

> Phase: `invention_loop` · round 3 · `upd_hypo`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `upd_hypo` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-17 21:32:19 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A hypothesis reviser (Step 3.6: UPD_HYPO in the invention loop)

You received the current hypothesis, all artifacts, and the paper draft.
Revise the hypothesis based on what the evidence supports.

Honest revision → focused research. Inflated confidence → wasted iteration.
</your_role>
</ai_inventor_context>

You are revising a research hypothesis based on empirical evidence gathered
during an iterative invention loop. Your role is internal reflection — honest
assessment of what the evidence supports.

SCOPE: Your ONLY output is the revised hypothesis text. You do NOT run code,
produce artifacts, fix bugs, or otherwise act on the evidence yourself — the
next iteration of the invention loop will spawn fresh artifacts based on your
revised hypothesis. Reflect on the evidence and rewrite the hypothesis;
nothing else.

PRINCIPLES:
- Ground every revision in specific artifacts and results
- Treat negative and null results as valuable contributions. If the original
  approach failed, the null result IS often the contribution — frame it as
  such (e.g. "X does not improve Y under conditions Z"). Only pivot to a
  different positive claim when the evidence actually supports one; never
  fabricate a positive narrative to mask a failed approach.
- Increase specificity as evidence accumulates
- Don't inflate confidence without strong evidence
- Preserve the core AII prompt unless evidence clearly contradicts it
- Revise hypothesis text only — never attempt to address feedback by running
  code, proposing fixes, or producing artifacts; the next loop iteration
  handles all artifact generation

<current_hypothesis>
The hypothesis as it stands. Revise it based on the evidence below.

kind: hypothesis
title: >-
  Two-Track Interventional Co-Response Grouping of SAE Latents (Correlation for Splitting, Anchored Greedy Set-Cover for Absorption):
  A Training-Free, Auditable Repair for the Mutually-Exclusive-Firing Absorption Regime, with an A-Priori Firing-Structure
  Router That Predicts When SAE-Latent Grouping Beats Marginal-Attribution Selection
hypothesis: |-
  ITERATION-2 STATUS -- THE LOAD-BEARING CORE WAS EXECUTED (this resolves iter-1's decisive 'incomplete submission / every Table-3 row is a prediction' verdict). Iteration 2 ran the two-track Counterfactual Co-Response Grouping (CCRG) pipeline on a FROZEN Gemma Scope layer-12/width-16k JumpReLU SAE across three executed experiments [art_0ueMMR8Tt02P first-letter; art_-o2RPMOZp37A toxicity; art_QGSdsKY6U1vK non-spelling], plus an enlarged, independently re-judged surface-invariance pair set [art_YwjLYapklnVk]. Gating passed everywhere (reconstruction cosine ~0.92, exact token localization). REAL NUMBERS NOW EXIST. What landed, honestly:
    - FIRST-LETTER C1 (classification): the label-free co-response unit is the highest-AUC starts-with-letter classifier on all 5 letters (L 0.905, O 0.917, T 0.859, I 0.961, D 0.956), above the raw best latent (a), count-matched observational clusters (b)/(c), and the count-matched attribution pool (h). A real positive -- but see R1/R3 below for why the MARGIN and its ATTRIBUTION are not yet established.
    - E1 (label-free absorber recovery vs the form-free diagnostic, random-membership null): PASS on 4/5 (L,O,T,D recover the diagnostic parent + >=2 absorbers above the 95th-pct null); I FAILS anchor-fidelity (the recall-argmax latent 1227 fires 0% on the corpus -- a spurious anchor). Honest mechanism finding: the recall-argmax heuristic is not always the semantic parent.
    - NON-SPELLING (C3 generality): absorption is NOT spelling-specific, but the two hierarchies are NOT co-equal. TAXONOMIC is the strong result -- the K-track recovers a Georgia country-specialist the count-matched attribution pool (h) drops (unit recall 0.713 vs h 0.520, paired-bootstrap CI[0.073,0.307]) at near-zero FP (0.014 vs g/h 0.85/0.65), AND the INDEPENDENT form-free diagnostic CORROBORATES the edges (KG-agreement 0.318 vs null 0.002; Jordan edge agrees 0.99). NUMERIC is DOWN-WEIGHTED to suggestive/diagnostic-UNCONFIRMED: the integer-slice recovery is low in absolute terms (0.283 vs g/h ~0.11) and the form-free diagnostic does NOT corroborate the K-track edges (KG-agreement top-1 = 0.0), so numeric recovers complementary DETECTORS whose absorber status the projection diagnostic does not confirm.
    - TOXICITY -- the decisive honest finding and the conceptual pivot: the iter-1 label-co-occurrence 'both regimes occur' proxy was REPLACED with a direct SAE-latent firing measurement. The general toxicity latent (12714, 'profanity/vulgar') fires on 94.3% of toxic content-flips (precision 0.996); the sub-attribute detectors (threat 11630, identity_attack 11573, insult 13367) CO-FIRE with it (toxic-only firing-Jaccard 0.40/0.29/0.66, all >> the 0.10 mutual-exclusivity threshold), DEPARTING sharply from label disjointness (label-Jaccard threat 0.044). So K-necessity is REFUTED on toxicity, grouping does NOT help (unit AUC 0.762 vs attribution g 0.892 / h 0.837 and full-residual probe 0.859; the unit COLLAPSES on disjoint sub-attributes -- threat 0.626 vs h 0.929, identity_attack 0.633 vs h 0.936), and the pre-registered selection ordering FAILS (f 0.086 < unit 0.237 < g 0.393 < h 0.451; unit-minus-(g/h) gap SLOPE vs sub-population reweighting -0.474, CI[-0.536,-0.412] -- the unit's advantage SHRINKS under shift).

  WHAT THE REVIEW EXPOSED -- THREE INTEGRITY/RIGOR GAPS THAT NOW DRIVE ITERATION 3 (the difference between an honest contribution and an over-claim):
    (R1, THE HEADLINE MARGIN IS MISLABELED AND OVERSTATED) The reported 'unit-minus-(h) AUC' CIs (T +0.205, I +0.405, D +0.456) are NOT AUC differences -- they are paired-bootstrap differences in per-example ACCURACY at each method's train-fit F1-optimal threshold. The true point-AUC margins over (h) are much smaller (T +0.211, I +0.128, D +0.230) and have NO reported CIs; worse, the large accuracy gaps on I/D are partly a THRESHOLD ARTIFACT -- (h)'s F1-optimal threshold collapses to predict-all-positive (~0.5 accuracy) despite AUC 0.833/0.726, so part of the apparent separation reflects a degenerate baseline operating point. Per-letter test sets are tiny (n=60-90 words). ITER-3 MUST report AUC point values WITH bootstrap AUC-DIFFERENCE CIs (B>=10,000) for unit vs (h)/(b)/(c) on all 5 letters, and any accuracy comparison must select thresholds by a metric matched to the comparison (Youden/accuracy-optimal) so no baseline collapses to predict-all. Expect L and O to become NON-significant on AUC -- state that plainly. This is the single cheapest honesty fix (data already in hand).
    (R2, THE PRIMARY ENDPOINT WAS NOT HONORED) The pre-registered endpoint was E1 AND E2. The artifact records verdicts.E2_PASS=false (per-letter E2: L false, O false, T true, I true, D false = 2/5), yet the code emitted primary_endpoint='WORKS' as `endpoint = 'WORKS' if (e1 and c1w)` (method.py:1676), DROPPING E2 and substituting C1. On the nominal PRIMARY letter L, E2 vs (h) is +0.042 CI[-0.067,0.150] (includes 0) and accuracy-C1 vs (h) is +0.091 CI[-0.045,0.227] (includes 0). So the one declared kill-switch (E1 AND E2) was tripped and the verdict was computed around it -- re-opening iter-1's 'protocol that cannot lose' concern. ITER-3 MUST reconcile code and paper and adopt the RE-DESIGNATED endpoint below, reporting E1 (4/5) and E2 (2/5, NOT on L) transparently.
    (R3, SELECTION IS NOT YET ISOLATED FROM ELIGIBILITY+POOLING -- the most important methodological gap) The admitted unit is a k=15 max-pool of which only ~4-7 are the named anchor+absorbers; the remaining ~8-11 members are uncharacterized eligible latents, and ~97-99% of RANDOM eligible k-pools clear the admission gain floor (the artifact itself concedes 'admission power comes from the surface-invariance gate ... not from pooling per se'). C1/E2 NEVER compare the unit against a RANDOM-ELIGIBLE-k (=15) pool. Without that control, 'the two-track unit is the best classifier / beats (h)' may reduce to 'ANY 15 eligible latents pooled beat 15 attribution-selected latents' -- i.e., the win is the cover-based ELIGIBILITY prefilter plus 15-way pooling, NOT the two-track set-cover SELECTION. This control is now the load-bearing decider of whether the contribution exists as claimed.

  ONE-SENTENCE HEADLINE (REGIME-SCOPED; conceptually the SAME two-track method, now grounded in executed evidence): clustering frozen SAE latents by their INTERVENTIONAL co-response to content counterfactuals -- via the TWO-TRACK algorithm (content-response CORRELATION for shared-support splitting; ANCHORED GREEDY SET-COVER for disjoint-support absorption, which correlation cannot propose) -- yields training-free, human-auditable, multi-member concept units that REPAIR the SAE specifically in the ABSORPTION REGIME (mutually-exclusive parent/child firing: first-letter spelling and, validated by an independent diagnostic, a taxonomic 'is-a-country' hierarchy), recovering absorbers a count-matched marginal-attribution selection silently drops; AND a single cheap forward-pass measurement -- the SAE-latent firing-Jaccard between candidate detectors and the general latent -- is an A-PRIORI ROUTER that predicts, BEFORE any grouping, whether a concept sits in the absorption regime (CCRG helps) or the co-firing/splitting regime (supervised attribution wins, as demonstrated on toxicity).

  THE ITERATION-3 MANDATE (the next loop MUST execute these; nothing else is load-bearing until they exist):
    (M1 = R3, THE DECISIVE NEW EXPERIMENT) ADD A RANDOM-ELIGIBLE-k POOL BASELINE (=15, averaged over many random draws from the cover-eligible set, with bootstrap CIs) to C1 and E2 on all 5 first-letter letters AND the non-spelling slices. Primary inferential object: unit-minus-(random-eligible-k) AUC with bootstrap CI. If the two-track unit SIGNIFICANTLY beats the random-eligible pool, the SELECTION contribution is established; if NOT, the contribution is honestly reframed around the cover-based ELIGIBILITY criterion, not the set-cover grouping -- both outcomes are publishable.
    (M2 = R1) RE-REPORT C1 as AUC point values with bootstrap AUC-DIFFERENCE CIs vs (h)/(b)/(c)/(random-eligible-k); use comparison-matched thresholds for any accuracy table; expect L,O non-significant on AUC and say so.
    (M3 = R2) HONOR THE ENDPOINT: reconcile the emitted verdict with the stated falsifier; report E1 (4/5) and E2 (2/5, NOT on L) transparently; adopt the re-designated primary endpoint below.
    (M4, ELEVATE AND VALIDATE THE A-PRIORI ROUTER) Promote the firing-Jaccard measurement to a HEADLINE contribution and validate it PROSPECTIVELY across all executed concepts: mutually-exclusive firing (spelling letters, taxonomic countries) predicts CCRG helps; co-firing (toxicity) predicts attribution wins. Report a prediction-vs-outcome table, the per-concept firing-Jaccard and parent recall-hole measurements, and a concrete decision rule (a firing-Jaccard threshold) a practitioner can run on data they already have. This is what converts a regime-limited method into a generally useful tool.
    (M5, MEASURE AUDITABILITY -- now load-bearing for significance because the unit generally does NOT beat a non-SAE dense probe on classification) Execute the previously-specified-but-DROPPED auditability results: (a) the KG-guided REPAIR LOOP -- pick an under-served sub-context (recall hole), read the KG for the covering absorber, ADD it, MEASURE recall recovery (bootstrap CI) vs a random-content-responsive-latent-addition control; (b) LLM-judge MEMBER-LABELING agreement -- predict each member's sub-context from its logit-lens tokens/contexts vs a shuffled-label null. At least one MEASURED KG-utility result must replace the current 'we emit a 70-edge graph' assertion, or the auditability/KG language must be softened to 'emitted but not yet evaluated'.
    (M6, RESOLVE MODEL-DIFFING) Either DELIVER one bounded shared-pretrained-SAE diffing result (does the unit detect a base-vs-instruction-tuned concept-usage shift more reliably than the best single latent, above a shuffle null, with the shared-SAE confound explicitly bounded, given that no gemma-scope-2b-it SAE exists) OR formally REMOVE model-diffing from the contribution claims and keep it ONLY as a stated infrastructure limitation. Do not leave it as open-ended future work.
    (M7, GENERALIZATION FRAMING) Lead 'absorption generalizes beyond spelling' with TAXONOMIC (diagnostic-corroborated); present NUMERIC as suggestive/diagnostic-unconfirmed (complementary detectors, not confirmed absorbers).
    (M8, NOVELTY) Expand the contrast with Winnicki 2026 'Domain-Filtered Knowledge Graphs from SAE Features' (2604.23829, confirmed to resolve) to 2-3 sentences with a CONCRETE mutually-exclusive parent->absorber edge that observational co-occurrence/decoder-geometry provably cannot produce (e.g. anchor 205 -> absorber 3069='list' on first-letter L, where parent and child are mutually exclusive in firing); cite Chanin 'A is for Absorption' to NeurIPS 2025; audit all 2026-dated citations for venue/version.

  PRIMARY ENDPOINT (RE-DESIGNATED to be honestly falsifiable AND honored by code). The method WORKS in the absorption regime iff, on first-letter spelling: (E1) the K-track proposal step, given ONLY content-flip pairs, recovers the diagnostic-identified parent + >=2 absorbers above the random-membership null (achieved 4/5; I fails anchor-fidelity); AND (C1-AUC, the SELECTION falsifier) the label-free unit beats BOTH the count-matched attribution pool (h) AND the random-eligible-k pool on classification AUC, with a bootstrap AUC-DIFFERENCE CI excluding 0 on a MAJORITY of letters. The random-eligible-k comparison is what makes this a SELECTION claim rather than a pooling claim, and it can genuinely kill the claim -- this closes the 'protocol that cannot lose' critique. E2 (absorbed-slice recall vs (h)) is RETAINED as a secondary characterization, reported per-letter (significant on T,I; directional elsewhere; NOT on L) -- never dropped or hidden. If C1-AUC vs the random-eligible-k pool does NOT exclude 0 on a majority of letters, the contribution is reframed from 'two-track selection' to 'cover-based eligibility + pooling' and reported as the executed finding.

  THE TWO-TRACK CLUSTERING ALGORITHM -- THE NAMED CONTRIBUTION (specification UNCHANGED; it executed as written). STEP 1 -- per-latent content-response r_l(p)=a_l(x_on)-a_l(x_off); keep content-responsive latents above a shuffle null; cover set C_l = pairs the latent tracks reliably (r_l>tau_resp, fires on x_on) and precisely (firing-precision>=0.7). EMPIRICALLY CONFIRMED: eligibility MUST be cover-based, NOT mean-over-pairs, or the genuinely sparse 1-5-word absorbers are discarded. STEP 2 -- C-TRACK (splitting): positive-Spearman soft-threshold affinity (beta=6, WGCNA) -> Leiden RBConfiguration; resolution by bootstrap-ARI stability. EMPIRICALLY CONFIRMED: Leiden's C extension hangs on tied-rank graphs -> run in a subprocess with a 45s timeout + agglomerative fallback. STEP 3 -- K-TRACK (absorption, anchored greedy max-coverage): ANCHOR=argmax_l|C_l| chosen WITHOUT the diagnostic; HOLES=P\C_anchor; greedily add l*=argmax_l|C_l intersect H| subject to mutual-exclusivity (firing-Jaccard<0.1), precision>=0.7, marginal-coverage-gain>=0.05 with bootstrap CI excluding 0. NEW (fixes the observed letter-I failure): add an UNSUPERVISED PARENT-VALIDATION step -- require the anchor to fire on the held-out corpus above a floor before trusting it, so a spurious high-cover-set latent that fires 0% on corpus (latent 1227) is rejected rather than crowned anchor. STEP 4 -- RECONCILE C-communities and K-covers, de-duplicate by highest coverage gain. STEP 5 -- ADMISSION FILTER: signature C (within-unit content-response correlation > 95th-pct shuffle null) OR signature K (pooled-max minus best-single AUC > 95th-pct of a best-of-random-k null MATCHED on marginal AUC, plus the k in {2,3} absolute gain >=0.05 with CI excluding 0, mutual-exclusivity, precision floor), AND unit-level surface invariance. Multiplicity controlled at the unit-proposal level (Bonferroni-within-unit then BH across the M candidates; report M and the empirical family-wise false-admit rate -- observed 0.03-0.09, at/near the 0.05 target).

  SAE-LATENT FIRING-STRUCTURE ROUTER (PROMOTED FROM PROXY TO HEADLINE; the measurement that grounds when grouping helps). The router is a single forward pass over data already held: encode examples through the SAE, identify the candidate general/parent latent and the top per-sub-context detectors, and report (i) the toxic/positive-only firing-Jaccard between detectors and the parent, and (ii) the parent's per-sub-context recall holes. Mutually-exclusive firing (Jaccard < ~0.10: spelling letters; taxonomic countries) => absorption regime => CCRG recovers absorbers and beats attribution at matched pool size. Co-firing (Jaccard >> 0.10: toxicity threat 0.40, identity_attack 0.29, insult 0.66) => splitting/co-activation regime => supervised attribution wins and CCRG does not help. The router REPLACES the discredited label-co-occurrence proxy and turns a potential over-claim into a falsifiable a-priori applicability test.

  BASELINE GLOSSARY (one line each; matched baselines are primary): (a) best raw single latent; (b) observational co-activation clusters COUNT-MATCHED to k; (c) decoder-geometry clusters COUNT-MATCHED; (d) counterfactually-matched diff-of-means; (e) probe on raw residuals; (f) surface-invariant matched probe (LEACE-erased surface direction); (g) supervised oracle pool = top-N SCR/TPP latents; (h) count-and-pool-matched probe = max-pool over EXACTLY k SCR/TPP-selected directions; (i) unmatched diff-of-means/probe; (j) oracle group-DRO probe (true sub-context labels = robustness upper bound); (k) label-free group-inference probe (JTT/GEORGE). NEW REQUIRED BASELINE (M1): (RE-k) random-eligible-k pool = k latents drawn at random from the cover-eligible set, averaged over many draws -- the control that isolates SELECTION from eligibility+pooling. SELECTION ISOLATION now requires beating BOTH (h) AND (RE-k), not just (h).

  NON-SPELLING TESTBED (C3 generality, executed). TAXONOMIC primary/diagnostic-corroborated (anchor 3792 recall 0.953; recovers Georgia/Jordan/United-States specialists (h) drops at near-zero FP; form-free KG-agreement 0.318 vs null 0.002). NUMERIC suggestive/diagnostic-unconfirmed (anchor 14823 precision 1.000, misses 1060 corpus positives; K-track recovers year/decimal detectors; integer-slice unit 0.283 vs g/h ~0.11 but a non-SAE dense probe reaches 0.643; KG-agreement top-1 = 0.0 so absorber status is not independently confirmed). Honest scope: gains are sub-context-specific (not blanket wins over the 20-latent oracle), and a non-SAE dense probe matches/beats the unit on classification.

  SCOPE AND VALUE PROPOSITION (reframed per the reviewer's scope MAJOR; the previous 'general improvement over baselines' framing is unsupported). The unit generally does NOT beat a non-SAE dense probe on classification (toxicity: loses to attribution+residual probe; non-spelling: dense probe dominates), and its classification wins are mostly within-SAE-ecosystem (vs (h) at matched pool size, pending the (RE-k) control). The defensible contribution is therefore: (1) a TRAINING-FREE REPAIR FOR THE ABSORPTION REGIME (recover absorbers attribution drops at matched pool size, taxonomic-corroborated); (2) an A-PRIORI FIRING-STRUCTURE ROUTER that tells a practitioner which regime a concept is in before any grouping; (3) MEASURED AUDITABILITY (KG repair utility + member-labeling) -- a dimension a dense probe lacks; (4) where the unit IS the most surgical steering direction (lowest full-vocab-KL collateral at matched on-target effect on L and D; not on O/T/I -- reported honestly as a generality demo). The headline is 'a repair for the absorption regime plus an a-priori router', supported by the routing experiment and at least one measured auditability result -- NOT a universal classifier win.

  HONEST NEGATIVES (most now OBSERVED, not hypothetical -- each publishable): K-necessity REFUTED on toxicity (real firing co-fires, departs from labels -> reshapes the K-track to absorption-regime-only); anchor-fidelity FAILS on letter I (recall-argmax can be a spurious 0%-corpus latent -> motivates the parent-validation step); numeric absorber status diagnostic-UNCONFIRMED; the unit TIES/LOSES to attribution and a residual probe on toxicity and a dense probe on non-spelling classification; E2 vs (h) excludes 0 on only 2/5 letters and NOT on the primary letter L; admission discriminative power comes from the surface gate, not pooling (random eligible k-pools clear the gain floor ~0.97-0.99). STILL TO TEST and capable of refuting the claim: the (RE-k) random-eligible-pool control (could reduce 'selection' to 'eligibility+pooling'); the KG-guided repair not beating random-addition (auditability buys no measurable fix); model-diffing under the shared-SAE confound. bias_in_bios remains a pre-registered boundary-null, not method failure.

  MOTIVATION (substance unchanged). Single SAE latents are unreliable units: feature absorption (a child latent suppresses a general parent's firing; Chanin 2409.14507, NeurIPS 2025), splitting, hedging, and 'SAEs Do Not Find Canonical Units' (ICLR 2025) converge on no single latent reliably tracking a concept; AxBench (ICML 2025) and DeepMind's negative report show plain diff-of-means beats raw-latent SAE methods. Absorption is exactly the regime where OBSERVATIONAL signals break by construction (parent and absorbing child mutually exclusive in firing) and where MARGINAL-ATTRIBUTION selection (SCR/TPP) silently drops the absorber. Correlation-community detection (DiffCoEx/WGCNA transfer) handles shared-support splitting; anchored greedy set-cover (Nemhauser-Wolsey-Fisher / Feige (1-1/e) transfer) handles disjoint-support absorption -- coverage-complementarity is a set-level property no pairwise affinity can express. The crucial executed lesson: this matters ONLY in the absorption regime, and a cheap firing-Jaccard measurement tells you a priori whether you are in it. Training-free post-hoc repair of FROZEN public SAEs is exactly what practitioners holding Gemma Scope have; architectural remedies (Matryoshka/H-SAE/subspace-aware) retrain and are orthogonal.

  SUCCESS CRITERIA. METHOD CONFIRMED (absorption regime) iff the RE-DESIGNATED PRIMARY ENDPOINT clears: E1 (K-proposal recovers parent + >=2 absorbers above the random-membership null, 4/5 achieved) AND C1-AUC (the unit beats BOTH (h) AND the random-eligible-k pool on classification AUC with a bootstrap AUC-difference CI excluding 0 on a majority of letters). HEADLINE CONTRIBUTIONS (also required for the paper to stand): the validated a-priori firing-structure router (prediction-vs-outcome across spelling/taxonomic/toxicity) AND at least one MEASURED auditability result. SUPPORTING (strengthen, do not gate): E2 absorbed-slice recall vs (h) (2/5 significant); taxonomic absorber recovery with diagnostic corroboration; the toxicity K-refutation as the negative pole of the router; admission false-admit <=0.05 with multiplicity correction; cluster-stability ARI above null; the steering demo where the unit is most surgical. HONEST NEGATIVES are reportable findings: a (RE-k) result that does not exclude 0 reframes the contribution to eligibility+pooling; a KG repair that ties random-addition removes the auditability value; numeric remains diagnostic-unconfirmed. A clean failure of the SELECTION falsifier (unit ties (RE-k)) is the declared method-does-not-work-as-claimed outcome and is itself publishable as 'cover-based eligibility, not set-cover selection, is what helps'.
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
  Same two-track frame; revision scopes to the absorption regime and elevates the a-priori firing-structure router.
_confidence_delta: decreased
_key_changes:
- >-
  Reframed status from 'execute the core (all predictions)' to 'core EXECUTED' and rewrote every claim as observed evidence
  with real Gemma-Scope numbers (first-letter AUC .86-.96, E1 4/5, toxicity K-refuted, taxonomic absorber recovery).
- >-
  Added the RANDOM-ELIGIBLE-k pool control (M1) as the decisive iter-3 experiment isolating two-track SELECTION from cover-based
  eligibility + 15-way pooling (reviewer R3); selection isolation now requires beating BOTH (h) AND random-eligible-k.
- >-
  Re-designated the primary endpoint to E1 AND C1-AUC-vs-(h)-and-random-eligible-k (honestly falsifiable, code-honored); E2
  demoted to secondary and reported 2/5, NOT on primary letter L; mandated reconciling method.py:1676 which dropped E2 from
  the WORKS conjunction (reviewer R2).
- >-
  Mandated AUC point values + bootstrap AUC-DIFFERENCE CIs and comparison-matched thresholds, replacing the mislabeled accuracy-as-AUC
  margins and the predict-all-positive threshold artifact; flagged L,O likely non-significant on AUC (reviewer R1).
- >-
  Elevated the SAE-latent firing-Jaccard measurement from a motivating proxy to a HEADLINE a-priori router and mandated prospective
  prediction-vs-outcome validation across spelling/taxonomic/toxicity; toxicity K-necessity REFUTED is now established evidence.
- >-
  Down-weighted numeric absorption to suggestive/diagnostic-UNCONFIRMED (KG-agreement top-1 = 0.0); lead the generalization
  claim with diagnostic-corroborated TAXONOMIC.
- >-
  Made MEASURED auditability (KG repair loop + member-labeling vs shuffle null) load-bearing for significance, since the unit
  does not beat a non-SAE dense probe on classification (reviewer scope MAJOR).
- >-
  Reframed the value proposition to 'a repair for the absorption regime + an a-priori router + measured auditability', not
  a universal classifier win; mandated resolving model-diffing (one bounded shared-SAE result OR formal removal from contributions).
- >-
  Added an unsupervised parent-validation step to the K-track anchor (require corpus-firing above a floor) to fix the observed
  letter-I spurious-anchor failure.
- >-
  Expanded novelty deltas: Winnicki 2026 contrast to 2-3 sentences with a concrete mutually-exclusive parent->absorber edge;
  Chanin to NeurIPS 2025; 2026-citation venue audit.
- Retitled to a regime-scoped repair + a-priori firing-structure router framing.
- >-
  Confidence DECREASED: the pre-registered endpoint was not honored, the central selection-isolation is unestablished pending
  the random-eligible-k control, headline AUC margins are overstated, and practical value vs non-SAE baselines is unmet.
relation_type: evolution
</current_hypothesis>

<all_artifacts>
Complete set of research artifacts across all iterations.

--- Item 1 ---
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

--- Item 2 ---
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

--- Item 3 ---
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

--- Item 4 ---
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

--- Item 5 ---
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

--- Item 6 ---
id: art_21JWypIydPMX
type: dataset
title: CCRG supporting sentiment/aspect families + bias_in_bios boundary-null dataset
summary: >-
  Three REAL, human-annotated datasets standardized into the CCRG shared minimal-pair schema and emitted in the canonical
  exp_sel_data_out format ({metadata, datasets:[{dataset, examples:[{input, output, metadata_*}]}]}), ONE example per text
  row, grouped by dataset, $0 LLM spend. Families (separable via metadata_family): (1) sentiment = CAD-IMDB (Kaushik et al.
  ICLR 2020), 4,880 rows / 2,440 human counterfactual content-flip pairs (positive<->negative), supporting; (2) restaurant_aspect
  = CEBaB (Abraham et al. NeurIPS 2022), 5,682 rows / 2,841 pairs (food 1,740 + service 1,101) flipping ONE aspect's sentiment
  with all four aspect majorities (food/service/ambiance/noise) + binarized review_sentiment retained as INDEPENDENT sub_context
  labels, supporting; (3) bias_in_bios_boundary = LabHC/bias_in_bios (De-Arteaga et al. 2019), 20,177 profession bios (28
  classes, gender as independent sub-context), the PRE-REGISTERED boundary-null where habitat~=label. Total 30,739 rows, 5,281
  reconstructable minimal pairs. Per row: input(text), output(canonical label), and metadata_* fields: id, family, dataset_source,
  concept(sentiment|food_sentiment|service_sentiment|profession), concept_label, sub_context(dict), pair_id, partner_id, pair_role(content_on|content_off|null),
  flip_type(content|null), is_content_pair, is_surface_pair(false for all), fold(train|dev|test), meta(raw fields incl char_len,
  token_overlap_with_partner, raw labels, subsample seed). Every (x_off,x_on) content pair is reconstructable via pair_id/partner_id
  (content_on=positive/concept-present member). is_surface_pair=false everywhere — surface flips are out of scope here (reserved
  for sibling ParaDetox/LLM artifacts); no surface pairs fabricated. NO derived statistics (MI/probes) computed — raw standardized
  data only. Every row validated against schema.json (jsonschema Draft7) AND full/mini/preview validated against exp_sel_data_out
  (aii-json). THREE plan errors were caught and corrected by empirical verification: (a) CAD-IMDB orig/<->new/ row alignment
  is FALSE (flip_rate~0.50, aligned Jaccard~=random~0.11) — authoritative pairing taken from the repo's combined/paired/*_paired.tsv
  via shared batch_id (true-pair Jaccard 0.816 vs random 0.108); (b) CEBaB edit_type is the edited ASPECT {food,service,ambiance,noise}
  and edit_goal is the target sentiment (the plan swapped them), and review_majority is a 1-5 star rating (binarized 1,2->neg
  / 4,5->pos / 3->neutral); (c) bias_in_bios ships no ClassLabel names, so the canonical 28-occupation alphabetical mapping
  (incl 'dj' at index 8) was verified empirically 17/17 by keyword hit-rate (nurse=13, attorney=2, surgeon=25, software_engineer=24,
  yoga_teacher=27), gender 0=male/1=female confirmed by pronouns; stratified (profession x gender, 56 strata) capped subsample
  with fixed seed 20240617, gender-balanced (male 10,054 / female 10,123). Licenses: CAD Apache-2.0, CEBaB CC-BY-4.0, bias_in_bios
  MIT. Reproduce all deliverables with `uv run data.py`. Downstream guidance: compute per-family bootstrap CIs as primary
  (families cleanly separated); treat any bias_in_bios null as the expected boundary outcome, not method failure; build content
  (x_off,x_on) deltas from pair_id.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_4
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

--- Item 7 ---
id: art_0ueMMR8Tt02P
type: experiment
in_dependencies:
- id: art_dpYpjSn2Xvg3
  label: dataset
  relation_type: uses
  relation_rationale: >-
    First-letter exp encodes this spelling testbed's content/surface pairs and corpus through the frozen SAE.
- id: art_RidEJtBC7gPT
  label: method
  relation_type: uses
  relation_rationale: >-
    Implements the dossier's SAE pipeline, two-track algorithm, baselines, and admission rule.
- id: art_I2MrezW41iQo
  label: diagnostic
  relation_type: uses
  relation_rationale: Uses the form-free absorption diagnostic as the non-circular oracle for E1/E2.
title: >-
  Two-Track CCRG First-Letter Endpoint: E1/E2/C1, Admission & Steering on Gemma-Scope SAE
summary: |-
  EXECUTED the load-bearing two-track Counterfactual Co-Response Grouping (CCRG) experiment on a FROZEN Gemma-Scope layer-12/width-16k JumpReLU SAE over the first-letter spelling absorption testbed (letters L,O,T,I,D). Verdict = WORKS. Core LLM spend $0. Runs end-to-end in ~8 min on one RTX 4090.

  PIPELINE (method.py, fully implemented + baselines side-by-side): model = unsloth/gemma-2-2b (bf16); SAE loaded DIRECTLY from Gemma-Scope params.npz (canonical layer_12/width_16k/average_l0_82) to avoid sae_lens/transformer_lens version conflicts with transformers 5.x. Residual read via forward-hook on model.model.layers[12] output (== blocks.12.hook_resid_post). GATING CHECK PASSED: reconstruction cosine 0.924, explained-variance 0.857, L0 95.9, corpus token-id localization exact (0/64). Steps: (1) content-flip co-response matrix r_l(w)=a_l(on)-a_l(off) at the word token over spelling carriers; (2) eligibility Lr = firing-precision>=0.7 AND covers>=1 sub-context (a mean-over-words prefilter rejects the genuinely sparse 1-5-word absorbers, so a cover-based rule is used); (3) C-track: Spearman co-response affinity -> signed soft-threshold (beta=6) -> Leiden RBConfiguration, run in a SUBPROCESS with a 45s timeout + agglomerative fallback because Leiden's C extension intermittently hangs on tied-rank graphs; (4) K-track: anchor = highest-cover-set latent, then anchored greedy max-coverage adding precise (>=0.7), anchor-disjoint (firing-Jaccard<0.1) latents covering uncovered holes; (5) FORM-FREE diagnostic (non-circular oracle): corpus-trained probe d_p (acc ~0.99), parent = max encoder-cosine, absorber via (a_hat_l.d_p)/(a.d_p)>0.5; baselines count-matched to k: (a) best raw latent, (b) co-firing cluster, (c) decoder-cosine cluster, (h) oracle SCR/TPP attribution pool, plus oracle pools g10/g20.

  KEY RESULTS (per-example test-fold predictions are in the datasets array as predict_unit/a/b/c/h). HEADLINE C1 classification: the LABEL-FREE co-response UNIT is the best starts-with-letter classifier on ALL 5 letters (test AUC L 0.905, O 0.917, T 0.859, I 0.961, D 0.956), beating raw best latent (a), co-firing (b) / decoder (c) clusters, AND the count-matched oracle-attribution pool (h) every time. E1 (label-free absorption recovery vs the diagnostic, random-membership null): PASS on 4/5 (L,O,T,D recover parent + >=2 absorbers above the 95th-pct null; I fails ANCHOR-FIDELITY only - its max-coverage latent fires 0% on corpus, a spurious anchor, an honest mechanism finding). Units are human-auditable, e.g. L = anchor 205 (logit-lens Lohan/Ls/LS) + absorbers 3069=list, 2416=line, 8463=large; a directed specialization knowledge-graph (anchor->absorbed_child(word)) is emitted (70 edges). E2 (absorbed-slice recall): the unit beats all COUNT-MATCHED baselines (h,b,c) directionally on all 5 letters and SIGNIFICANTLY (paired-bootstrap CI excludes 0) on T (.925 vs .763) and I (.775 vs .496). Steering: the mean-member-decoder direction has the LOWEST full-vocab-KL collateral at matched on-target effect on the primary letter L (16.4 vs hub 27.9 / diffmean 30.4) and on D; on O/T/I a non-SAE diff-of-means or the hub is more surgical (steering is a generality demo, reported honestly). Admission (Step-5, BH/Holm): K_UNIT admitted via sigK; empirical false-admit under the matched random-k null 0.03-0.09.

  HONEST CAVEATS (recorded in the JSON): the recovered-absorber COUNT metric is d_p-CIRCULAR for the oracle baselines (the diagnostic and g/h both rank by the probe direction d_p), so the E2 verdict is based on the non-circular downstream metrics (C1 + count-matched sliced recall) with the count reported descriptively; within Lr even random k-latent pools classify well (so admission power comes from surface-invariance + the 95th-pct sigK test, not pooling per se); the C-track is secondary and used the agglomerative fallback for L/O (Leiden hang).

  OUTPUT method_out.json is exp_gen_sol_out-schema-valid: metadata holds all metrics (verdicts, config, gating_check, per-letter E1 with 36-cell threshold sweep / E2 with CIs+McNemar+Holm / C1 / admission / c_track, full steering on-target+KL+PPL curves with matched comparison and random-direction null, unit_definitions with logit-lens tokens and top corpus contexts, kg_edges, runtime_stats); datasets holds per-letter held-out content instances with predict_unit/a/b/c/h for the downstream solution-evaluation step. full/mini/preview variants generated and schema-validated; both JSONs < 1 MB (well under 100 MB). pyproject.toml pins all 55 deps. Provides the paper its PRIMARY positive finding (cluster-level units > single latents + non-SAE/oracle baselines on downstream classification) plus rigorous, honestly-scoped E1/E2/steering/admission evidence and failure modes.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 8 ---
id: art_-o2RPMOZp37A
type: experiment
in_dependencies:
- id: art_8QO7pl6Pd8UQ
  label: dataset
  relation_type: differences
  relation_rationale: >-
    Real SAE firing-Jaccard 0.29-0.40 departs from this dataset's label-co-occurrence K/C routing prediction.
- id: art_RidEJtBC7gPT
  label: method
  relation_type: uses
  relation_rationale: >-
    Implements the dossier's pipeline, C/K tracks, and (a)-(h) baselines on the toxicity family.
- id: art_I2MrezW41iQo
  label: diagnostic
  relation_type: uses
  relation_rationale: >-
    Applies the dossier's firing-Jaccard<0.10 absorption threshold and diagnostic to test K-necessity.
title: 'Gemma-Scope toxicity: SAE firing-structure, count-matched C1, selection ordering'
summary: |-
  GPU experiment for the Two-Track CCRG method: organising frozen Gemma-Scope SAE latents (gemma-scope-2b-pt-res-canonical, layer_12/width_16k; firing=encode>0; residual captured by a forward hook on gemma-2-2b layers[12], validated by SAE reconstruction cosine 0.92 and L0~80/token) into cluster-level units, evaluated on the ParaDetox + civil_comments toxicity family (18,853 content pairs, 546 surface pairs, 18,308 classification rows). method_out.json (exp_gen_sol_out schema): metadata holds the full analysis; datasets[0] holds 2,980 per-example test-fold toxicity predictions for every method (predict_unit/a/b/c/h/d/e). Full/mini/preview variants validate; all <3MB.

  KEY RESULTS (full run). MAJOR-2 firing structure (replaces iter-1's label-co-occurrence proxy with real SAE-latent firing): the general toxicity latent g=12714 (Neuronpedia: 'profanity and vulgar expressions') fires on 94.3% of toxic content-flips (precision 0.996). Distinct, on-target detector latents exist for the label-disjoint sub-attributes - threat=11630 ('conflict and violence'), identity_attack=11573 ('race, identity, social justice'), insult=13367 ('hypocrite/moron/coward') - and they cover g's recall holes (cover-frac 0.74/0.93), BUT they co-fire with g (firing-Jaccard 0.40/0.29, far above the 0.10 absorption threshold). So SAE firing structure DEPARTS from the label co-occurrence structure: no mutual-exclusivity => K-necessity verdict REFUTED on toxicity (both branches were pre-registered as publishable; the K-track absorber win lives in the sibling first-letter experiment). This is the experiment's decisive, honest finding.

  C1 count-matched classification (primary scorer = logistic regression on each method's selected features, so only the SELECTION differs; secondary max-pool-z reported): the k=3 two-track co-response unit ties co-activation (b), decoder-geometry (c) and best-single-latent (a) on toxicity AUC (0.76 vs 0.80/0.79/0.77) but is beaten by SCR/TPP attribution selection (g/h=0.84-0.89), a full-residual probe (e=0.86) and diff-of-means (d), with unit-minus-h AUC CI [-0.093,-0.055] (exact McNemar Holm p~5e-71); and it COLLAPSES on the disjoint sub-attributes (threat 0.63 vs h 0.93; identity_attack 0.63 vs h 0.94). This is the benchmarked pattern that simple baselines and attribution often outperform raw-latent SAE grouping. Per-target paired bootstrap (B=10000 toxicity/2000 subs) + exact McNemar + Holm.

  Selection ordering: the pre-registered (f)<(g)/(h)<unit worst-sub-context-recall ordering does NOT hold (f=0.09 < unit=0.24 < g=0.39 < h=0.45); the unit-minus-(g/h) gap SLOPE vs measured disjoint sub-population reweighting = -0.47 (95% CI [-0.54,-0.41], excludes 0) - the unit's relative advantage SHRINKS under subpopulation shift. A clean honest negative. (f) is a LEACE surface-invariant probe.

  Unit construction: C-track = signed soft-thresholded Spearman of co-response profiles + Leiden RBConfiguration; gamma chosen by bootstrap-ARI stability subject to a non-trivial human-auditable g-community size (ARI-stability alone collapses to one giant cluster - documented gamma sweep included). K-track added 0 absorbers (consistent with the REFUTE branch). Admission/multiplicity: M=31 candidate units, BH-corrected with a Bonferroni-within-unit (C-or-K) signature p and a surface-response AND-gate; 11 admitted; empirical family-wise false-admit rate on the random-k null = 0.08 (reported as a limitation). Surface null caveat (n=546, gpt-4o-mini gen+judge, same-model circularity) flagged.

  Baselines vs reviewer scope: raw SAE latents (a), co-activation (b), decoder-geometry (c), SCR/TPP attribution pool (g) and raw-direction (h); non-SAE diff-of-means probe (d) and logistic regression on raw residuals (e). Human-auditable cluster definitions via Neuronpedia auto-interp labels + top tokens for every key latent (firing_structure.neuronpedia_labels, unit.member_labels). Stats: tie-aware AUC, exact McNemar, Holm-Bonferroni, paired bootstrap CIs. Files: method.py, enrich_neuronpedia.py, probe.py, pyproject.toml (pinned), README.md, full/mini/preview_method_out.json. Caches (cache/, hf_cache/) are excluded from publication.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 9 ---
id: art_QGSdsKY6U1vK
type: experiment
in_dependencies:
- id: art_t2uUbjSwpd3t
  label: dataset
  relation_type: uses
  relation_rationale: >-
    Encodes the numeric+taxonomic testbed and runs the non-triviality gate + K-track set-cover.
- id: art_RidEJtBC7gPT
  label: method
  relation_type: uses
  relation_rationale: >-
    Implements the dossier's K-track set-cover and marginal-attribution oracle baselines.
- id: art_I2MrezW41iQo
  label: diagnostic
  relation_type: extends
  relation_rationale: >-
    Extends the dossier's spelling-only absorption diagnostic to numeric/taxonomic; absorption generalizes.
title: >-
  SAE Absorption Generalizes Beyond Spelling: Numeric & Taxonomic (Gemma Scope L12)
summary: |-
  C3 generality experiment for the two-track CCRG hypothesis. Question: does SAE feature absorption (documented almost only on first-letter spelling) generalize to NON-spelling token hierarchies? Encodes the frozen non-spelling testbed (numeric_absorption 8,380 rows; taxonomic_absorption 15,748 rows) through google/gemma-2-2b + Gemma Scope layer_12/width_16k SAE and runs the non-triviality gate + K-track anchored greedy set-cover, vs marginal-attribution baselines and a non-SAE probe.

  VERDICT = non_spelling_absorption_confirmed: the gate PASSES on BOTH hierarchies (absorption is NOT spelling-specific).

  PIPELINE/VALIDATION: SAE loaded directly from DeepMind params.npz (JumpReLU; no sae_lens dependency). Residual taken at HF hidden_states[13] == blocks.12.hook_resid_post, empirically selected by FVU sweep over indices {11,12,13}; encode-time FVU=0.18 (numeric)/0.20 (taxonomic), token-alignment 0.975/1.000, mean L0 68/101 — all three V1/V2/V3 gates pass.

  NUMERIC: anchor latent 14823 (content-response precision 1.000, negative-firing 0.001; recall 0.829 content-flip / 0.427 corpus) misses 1060/1850 corpus positives (holes). K-track recovers 3 absorbers (year, decimal x2). C3 confirmed via the 'integer' sub-context: unit recall 0.28 vs (g)/(h) 0.11, paired-bootstrap diff +0.18 CI[0.12,0.24], Holm p=8e-8. On year/date/decimal the broader 20-latent oracle pool beats the compact 4-latent unit (honest, mixed). Form-free absorption_fraction KG-agreement ~ null (coverage-based and projection-based absorber notions DIVERGE here). Unit has 0 false-positives vs (g)/(h) 0.12/0.13; the non-SAE dense probe reaches recall 1.000 at 0 FP (the 'simple baselines can match raw-SAE' point, honestly reported).

  TAXONOMIC: anchor latent 3792 (recall 0.953, neg-fire 0.033); K-track recovers Georgia/Jordan/United-States specialists. C3 confirmed via 'Georgia': unit beats the count-matched (h) pool, diff CI[0.073,0.307] — the K-track recovers a country-specialist that marginal attribution drops at matched pool size. Form-free KG-agreement = 0.318 vs null 0.0016 (the projection diagnostic CORROBORATES the K-track edges here, unlike numeric). (g)/(h) oracle pools have huge FP (0.85/0.65) while the unit is clean (0.014).

  BASELINES & STATS: raw single SAE latent (anchor-alone), (g) SCR/TPP-style top-20 marginal-attribution oracle pool, (h) count-matched top-k pool, and a non-SAE dense logistic/diff-of-means probe (trained on the DISJOINT corpus-train fold). Reported per eligible sub-context (>=150 diagnostic positives) at both the >0 JumpReLU rule and matched overall recall: paired bootstrap (B=10000), exact McNemar, Holm-Bonferroni multiplicity, threshold-sensitivity sweep over Jaccard/precision/gain, admission (signature-K AUC-gain vs AUC-matched random-k null + surface-invariance), and parent-probe recall-by-sub-context (honest-null uniformity check). The form-free diagnostic only SCORES edges (probe direction trained disjoint), never forms units (non-circular).

  HEADLINE for the paper: absorption generalizes beyond spelling to numeric and country hierarchies; the K-track recovers specialist absorbers (integer; Georgia) that marginal-attribution pools drop, and yields a compact, near-zero-FP, human-auditable cluster (anchor + named specialist edges). Honest nuance: gains are sub-context-specific (not a blanket win over the 20-latent oracle), and the coverage-based vs projection-based absorption definitions agree for taxonomic but diverge for numeric. method_out.json carries full per_hierarchy results in metadata + per-row detector predictions (predict_unit/anchor/g/h/dense_probe) on the diagnostic fold; results/ has partial per-hierarchy JSON, sliced-recall CSVs, and .npz figure arrays.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_3
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 10 ---
id: art_YwjLYapklnVk
type: dataset
in_dependencies:
- id: art_I2MrezW41iQo
  label: protocol
  relation_type: uses
  relation_rationale: >-
    Surface-pair superset built per the dossier's generation prompts, judge rubric, and gate constants.
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

--- Item 11 ---
id: art_8AwUJK9qOwX_
type: experiment
in_dependencies:
- id: art_dpYpjSn2Xvg3
  label: dataset
- id: art_RidEJtBC7gPT
  label: method
- id: art_I2MrezW41iQo
  label: diagnostic
- id: art_YwjLYapklnVk
  label: surface-control
title: >-
  Iter-3 CCRG Re-Run: Random-Eligible-k Baseline, AUC-Difference CIs, Verdict Reconciliation
summary: >-
  Decisive iter-3 re-run of the two-track CCRG first-letter-spelling pipeline (frozen Gemma-Scope L12/16k JumpReLU SAE on
  gemma-2-2b), reusing iter-2's method.py verbatim and surgically adding three fixes. M1 (decisive): a RANDOM-ELIGIBLE-k (RE-k)
  baseline drawing k=|unit| latents uniformly at random from the cover-eligible set Lr, max-pooled identically to the unit/(h)/(b)/(c),
  so unit-minus-RE-k isolates two-track SELECTION from cover-based eligibility+pooling; added to C1 and E2. The single most
  decisive number is frac_rek_ge_unit (one-sided permutation p: fraction of random eligible pools matching/beating the unit).
  M2: replaces the iter-2 accuracy-as-margin artifact with threshold-free AUC POINTS plus bootstrap AUC-DIFFERENCE CIs (B>=10,000,
  content-flip pair-cluster resampling on the held-out test fold) for unit vs (a)/(b)/(c)/(h)/(RE-k) per letter, a pooled-across-letters
  stratified-bootstrap + inverse-variance meta-analysis, and a Youden-threshold accuracy table (no predict-all-positive collapse;
  the F1-threshold artifact is retained and flagged). M3: computes primary_endpoint from the stated falsifier (E1 AND unit-AUC-significantly-above-BOTH-(h)-AND-(RE-k)
  on >=3/5 letters => ABSORPTION_REPAIR_SELECTION_CONFIRMED; else REFRAMED_TO_ELIGIBILITY_POOLING; else SELECTION_NOT_ESTABLISHED),
  reporting E1 and E2 transparently and never dropping E2 from the conjunction. Reproduction is verified: gating cosine 0.924,
  deterministic baselines reproduce iter-2 (h-AUC 0.795 vs 0.794), E1_PASS and E2_PASS patterns match; the greedy set-cover
  unit AUC drifts within ~0.03 because iter-2's torch 2.6+cu126 cannot run on this RTX 5090 (Blackwell sm_120), requiring
  torch 2.8+cu128 (all other deps pinned identically). On L the unit significantly beats RE-k (frac_rek_ge_unit~0.009, diff
  +0.24 CI excludes 0) but ties the oracle attribution baseline h (CI includes 0) — the pre-registered expectation. All analysis
  is under metadata.* (per_letter, verdicts, pooled_across_letters, endpoint_reconciliation_note, admission on the 1,700-pair
  surface superset, config, gating_check); datasets carry per-letter held-out test-fold rows with predict_unit/a/b/c/h/REk
  (Youden-thresholded). Output validates against exp_gen_sol_out.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 12 ---
id: art_P8-3ipCuQwVY
type: experiment
in_dependencies:
- id: art_t2uUbjSwpd3t
  label: dataset
- id: art_RidEJtBC7gPT
  label: method
- id: art_I2MrezW41iQo
  label: diagnostic
title: >-
  Non-Spelling SAE Absorption: RE-k Selection-Isolation, AUC-Diff CIs, Router Inputs
summary: |-
  Iteration-3 re-analysis of the executed iter-2 non-spelling SAE-absorption experiment. It reuses the frozen Gemma-Scope layer_12/width_16k SAE encodings (cached CSR latents + fp16 residuals) and the same two-track K-track unit/anchor/(g)/(h)/dense-probe, then adds the three iter-3-mandate analyses on the NON-SPELLING slices (taxonomic countries; numeric quantity types). Runs CPU-only via cache reuse (the RTX 5090 sm_120 is unsupported by torch 2.6.0+cu124, so the script auto-falls-back to CPU; the GPU re-encode path exists only for a cache miss, which never occurs). VERDICT = taxonomic_selection_established.

  M1 (selection isolation): adds a RANDOM-ELIGIBLE-k pool baseline (RE-k) and an anchor-fixed variant (RE-k-anchored) that separate the two-track set-cover SELECTION from cover-based eligibility+pooling. Rule selection_established(s) = (unit AUC > RE-k-anchored 95th pct) AND (paired AUC-difference CI vs RE-k-anchored mean excludes 0). TAXONOMIC Georgia: True (unit-RE-k-anchored = +0.099 [+0.085,+0.113], unit at 100th pct of draws). NUMERIC integer: False (unit-RE-k-anchored = +0.029 [-0.006,+0.062] includes 0) -> non-spelling numeric is eligibility+pooling, not set-cover selection.

  M2 (AUC + AUC-difference CIs): point AUC plus stratified paired-bootstrap AUC-DIFFERENCE CIs (B=10,000) for unit vs (g)/(h)/RE-k/RE-k-anchored/dense-probe on the defining absorbed slices (Georgia, integer), all 20 eligible countries / 8 numeric sub-contexts, and descriptive subs (Jordan, United States, decimal, year), replacing iter-2's mislabelled matched-recall-accuracy deltas. Georgia headline (pos=150 Georgia tokens vs 2100 taxonomic negatives): unit AUC=0.989, g=0.418, h=0.383 (below chance = absorption signature), RE-k=0.906, RE-k-anchored=0.890, dense-probe=1.000; unit-h=+0.606 [+0.570,+0.642] confirms a genuine AUC-rank effect (the R1 honesty fix), unit-dense=-0.011 [-0.015,-0.008] (the non-SAE probe slightly edges the unit but the unit is the best SAE detector). A comparison-matched Youden accuracy table is added so NO baseline is forced to predict-all (the artefact that made (h) look degenerate in iter-2).

  M7/M4 (router inputs): per-hierarchy firing-Jaccard(parent, top per-sub-context detector) on positives + parent per-sub-context recall holes + per-slice form-free KG top1, emitted as inputs for the M4 prediction-vs-outcome router table. absorption_type (parent hole>0.5 AND Jaccard<0.10) is True for exactly two countries -- Georgia (J=0.059, KG top1=1.0) and Jordan (n=124<150 descriptive, KG top1=0.95), the ambiguous homographs where the parent country-latent has a genuine recall hole; all other countries have parent_recall_hole~=0. Numeric integer router J=0.256 (co-firing, not mutually exclusive), KG mean top1=0.0. M7 framing: taxonomic = diagnostic_corroborated LEAD; numeric = suggestive_diagnostic_unconfirmed (dense-probe AUC=1.000 dominates, KG top1=0.0) and is NOT promoted.

  Deliverables: method.py (single pipeline = iter-2 core + iter-3 phases D-H), method_out.json / full|mini|preview_method_out.json (exp_gen_sol_out schema, PASSED, 8.5MB < 100MB; metadata.per_hierarchy carries auc_point, auc_diff_ci, rek_distribution, selection_established, youden tables, router+regime, generalization_status, honest_notes; datasets[].examples carry per-row diagnostic predictions predict_{unit,anchor,g,h,dense_probe,rek}), results/ (partial_{taxonomic,numeric}_iter3.json, results.json, auc_diff/router/sliced_recall CSVs, arrays npz), pyproject.toml (21 pinned deps), RESULTS_SUMMARY.md. Downstream GEN_PAPER_TEXT consumes this for the M1/M2/M7 non-spelling tables: taxonomic Georgia is the established selection win (and the only AUC-rank win that survives the anchor-fixed random control), numeric is honestly demoted to suggestive, and the router rows feed the M4 absorption-vs-splitting regime map.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 13 ---
id: art_lvYKkaolutJG
type: experiment
in_dependencies:
- id: art_dpYpjSn2Xvg3
  label: dataset
- id: art_t2uUbjSwpd3t
  label: dataset
- id: art_RidEJtBC7gPT
  label: method
- id: art_I2MrezW41iQo
  label: diagnostic
title: >-
  Measured Auditability of Two-Track CCRG SAE Units: KG Repair Loop + LLM Member-Labeling
summary: |-
  Executes the two previously-dropped, now load-bearing M5 AUDITABILITY results for the two-track Counterfactual Co-Response Grouping (CCRG) units on a frozen Gemma-Scope L12/16k JumpReLU SAE (gating cosine 0.919, token localization exact, hidden_states[13]). Canonical units/KG are READ from the deterministic iter-2 outputs (first-letter exp_1, taxonomic exp_3) and re-derived as a cross-check (responsive set 682 vs iter-2 684; anchor 3792 matches). It converts the iter-2 'we emit a 70-edge graph' ASSERTION into MEASURED numbers.

  M5a KG-GUIDED REPAIR LOOP (load-bearing): for each under-served sub-context (recall hole where the anchor/parent latent goes silent) the KG names a covering absorber; we ADD it to the anchor (max-pool) and measure recall recovery on HELD-OUT corpus windows (selection split disjoint from eval split: taxonomic train->diagnostic; first-letter folds 0-3 -> fold 4) vs a control that adds the full population of other content-responsive latents, with a paired-bootstrap CI (B=10,000). Result: 8 measured successful repairs whose KG-minus-random gain CI excludes 0 -- taxonomic Georgia (anchor recall 0.20 -> 1.00, gain 0.80, 99.4th pct vs random, CI [0.70,0.82]), Jordan (0.29 -> 1.00/0.935), United States (0.77 -> 0.99/0.97), plus first-letter O/'our' and D/'day' (0.00 -> 1.00). BOTH the K-track edge (4697/9339/8442) and the higher-precision diagnostic-corroborated absorber (16009/540/846) are significant. Honest negatives: first-letter L ('list','line',...) and T ('type','things',...) candidate words tie the random-addition control (too few held-out windows / no extra localization) -- reported verbatim.

  M5a(k) LOCALIZATION-FAILURE CHECK: the label-free group-inference probe (k) (JTT: ERM -> upweight hardest/error set -> retrain) yields a dense hyperplane whose decoder-projection argmax is the PARENT 3792 (top |cos|=0.44, does not dominate; KG absorbers rank 2269/58/5964, never argmax). (k) classifies the holes (recall 1.0 on Georgia/Jordan/US) but exposes NO addable per-sub-context latent -- whereas the KG names exactly one. Country is linearly separable so the JTT error set is empty and we upweight the lowest-margin 20%; the structural conclusion is unchanged.

  M5b LLM-JUDGE MEMBER-LABELING (load-bearing): 67 unit members (anchor + absorbers across taxonomic + L/O/T/D) each described by logit-lens top-10 tokens + top-5 raw activating corpus windows with the sub-context label WITHHELD (non-leaky); anthropic/claude-haiku-4.5 (temp 0, forced-choice) names the sub-context. Agreement 0.716 vs shuffle null 0.090 (analytic chance 0.087); gap 0.627, bootstrap CI [0.522,0.731] excludes 0. Per-role: absorbers 0.76 accuracy, anchors 0.20 (judge over-specifies the parent's mixed-country/word windows -- honest caveat). 84 calls, 0 errors, total LLM spend $0.047 (<<$3 target).

  VERDICT: kg_utility_measured=True, member_labeling_above_null=True, replaces_iter2_assertion=True. Output method_out.json (exp_gen_sol_out-schema-valid, full/mini/preview all <100MB) stores per-sub-context repair stats (recall_anchor, recall_anchor_plus_kg, gain_kg, kg_percentile_vs_random, random_gain percentiles, paired_bootstrap_CI, k-track + diagnostic variants, honest_negatives), the (k) decoder-projection check, full member evidence + judge choices + scoring (gap CI, per-role accuracy, confusion), and a datasets block (kg_repair_loop rows; member_labeling rows with predict_judge) for downstream solution evaluation. This provides the paper's auditability section: the emitted feature knowledge-graph carries MEASURED localization utility and the cluster-level units are human/LLM-auditable, while example-reweighting baselines provide no addable per-feature unit.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_3
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 14 ---
id: art_07ju05r0onqB
type: experiment
in_dependencies:
- id: art_dpYpjSn2Xvg3
  label: dataset
- id: art_t2uUbjSwpd3t
  label: dataset
- id: art_8QO7pl6Pd8UQ
  label: dataset
- id: art_21JWypIydPMX
  label: dataset
- id: art_RidEJtBC7gPT
  label: method
- id: art_I2MrezW41iQo
  label: diagnostic
title: >-
  Firing-Structure Router (M4): firing-Jaccard predicts when grouping beats attribution
summary: |-
  This experiment promotes the SAE-latent firing-Jaccard to a headline, a-priori router (M4) and validates it PROSPECTIVELY on a frozen Gemma-Scope SAE (google/gemma-scope-2b-pt-res, layer_12/width_16k/average_l0_82; model unsloth/gemma-2-2b; hook blocks.12.hook_resid_post; firing := encode>0; gating reconstruction-cosine 0.927, L0 median 70). method.py runs ONE uniform pipeline over 15 concepts: 12 ESTABLISHED (spelling L/O/T/I/D; numeric; taxonomic; toxicity threat/identity_attack/insult/obscene/sexual_explicit) used to DERIVE the rule, and 3 PROSPECTIVE (CAD-IMDB sentiment; CEBaB food/service aspect) predicted BEFORE their outcome is revealed. Per concept it (1) identifies a content-responsive parent latent on content-flip pairs (an unsupervised positive-firing-floor validation fixes the letter-I spurious-anchor bug), (2) finds per-sub-context detector latents + parent recall holes, (3) computes positive-only firing-Jaccard(detector,parent) over the concept's positives, and (4) measures a downstream OUTCOME: a LABEL-FREE CCRG K-track-lite unit (parent anchor + firing-disjoint, hole-covering absorbers) versus three required baselines at MATCHED pool size k -- (a) the best single raw SAE latent, (h) a supervised SAE standardized diff-of-means attribution pool (AxBench/SCR-TPP proxy), and (d) a non-SAE diff-of-means probe on the raw layer-12 residual -- scored by a held-constant logistic head on a held-out test fold with paired-bootstrap CIs (B=10000).

  KEY RESULTS: firing-Jaccard cleanly separates the regime EXTREMES -- spelling is firing-disjoint (Jaccard L=0.017, O=0.039, T=0.003, I=0.008, D=0.017, all <0.1; reproduces iter-2) and cluster-level grouping helps; toxicity co-fires (~0.69) so a single specialist latent wins. The primary router (predict absorption iff Jaccard<tau*) yields tau*=0.05, balanced accuracy 0.917 on the 12 established concepts; leave-one-concept-out accuracy 0.733; prospective out-of-sample accuracy 0.333 (sentiment HIT, predicted+measured co_firing; aspect_food/service MISS -- predicted co_firing but showed small absorption deltas +0.034/+0.071).

  HONEST FINDINGS (load-bearing for the paper): (i) firing-Jaccard ALONE is insufficient -- the TAXONOMIC counterexample has LOW Jaccard (0.056) yet a co_firing OUTCOME because the parent already has ~0.95 recall (no holes to fill); accordingly a recall-hole-only router (hole>0.777) reaches balanced accuracy 1.0 on established concepts, and a 2-signal router (low-Jaccard AND high-recall-hole) is also reported, supporting the refined rule 'grouping helps only when disjoint specialists AND parent recall holes co-occur'. (ii) The supervised baselines (h)/(d) frequently MATCH or beat the label-free unit on raw AUC (consistent with 'simple baselines are strong on raw-latent SAE tasks'); the unit's contribution is being LABEL-FREE while still beating the best single latent (a) in the absorption regime. (iii) numeric is reported honestly as suggestive/diagnostic-unconfirmed (absorption is documented empirically only on spelling).

  DELIVERABLES: method.py (self-contained, single-GPU, $0 LLM spend) and method_out.json with full/mini/preview variants (exp_gen_sol_out schema, all schema-PASSED, each <0.4MB). The output carries metadata with the prediction_vs_outcome_table (parent, jaccard min/median/max, recall_hole_max, predicted vs ground-truth regime, per-baseline AUCs auc_unit/auc_a/auc_h/auc_d, deltas with paired-bootstrap CIs, hit), per_concept_firing_jaccard (per-sub-context detector + bootstrap CIs), the router block (tau-sweep, regime separation, LOO per-concept, prospective table, plus strict-CI / recall-hole-only / combined router variants), a reproduction_check (spelling all <0.1 = True; toxicity references), and honest_notes. Expensive SAE forward passes are cached under cache/ (excluded from the published repo). Downstream GEN_PAPER_TEXT can use this as the M4 'when does cluster-level grouping help vs marginal attribution' router result and its honestly-reported boundary (firing-disjointness must co-occur with parent recall holes).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_4
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 15 ---
id: art_jI2KIJotjzIU
type: experiment
in_dependencies:
- id: art_8QO7pl6Pd8UQ
  label: dataset
- id: art_dpYpjSn2Xvg3
  label: control-dataset
- id: art_RidEJtBC7gPT
  label: method
title: >-
  M6 Model-Diffing: Shared pt-SAE Co-Response Unit vs Best Latent, gemma-2-2b vs -it
summary: >-
  Delivers the M6 (model-diffing) downstream task for the Two-Track CCRG hypothesis: a single frozen Gemma-Scope layer-12/width-16k
  JumpReLU pretrained SAE (loaded directly from params.npz; reconstruction cosine 0.925 base / 0.913 IT, matching iter-2 ~0.92)
  applied to layer-12 residual activations of gemma-2-2b (base) vs gemma-2-2b-it (instruction-tuned), both unsloth ungated
  mirrors. METHOD = the iter-2 co-response UNIT (toxicity members {1920,12714,14630}; spelling-L 15-member anchor+absorber
  unit, anchor 205; both READ from iter-2 method_out.json). BASELINE = best single latent (toxicity anchor 12714) plus a descriptive
  oracle best-member. For 1200 toxic (civil_comments) and 1200 spelling-L corpus texts, it computes BOS-excluded max-pooled
  unit and single-latent responses on base vs IT, then base-vs-IT separability AUC, paired Cohen's d_z, a 2000x paired sign-flip
  shuffle null, and 2000x doc-bootstrap CIs. CONFOUND BOUNDING is load-bearing: B1 reconstruction parity (IT cosine 0.913
  not catastrophic, so the shared-base-SAE recipe is viable here); B2 control-concept floor (genuine toxicity shift = toxicity
  AUC-departure MINUS spelling-control departure); B3 residual-norm / norm-matched re-analysis (IT residual-stream norm 1.11x
  base). RESULT (verdict = clean-null-limitation, an explicitly valid M6 deliverable): a base-vs-IT shift IS detectable above
  the shuffle null for the toxicity unit (AUC 0.438, departure 0.062, p<1e-3, direction IT>base), but it is NOT concept-specific.
  The spelling control shows the SAME direction and an identical 0.062 departure, so the confound-controlled genuine toxicity
  shift is +0.000 (95% CI [-0.009, 0.007], includes 0); the norm-matched genuine shift is a small +0.027 (CI [0.021, 0.033])
  but still IT>base, OPPOSITE the naive detox prediction, i.e. generic OOD/norm drift rather than a concept-specific reduction
  in toxicity-feature usage. A within-model sanity check confirms the unit IS a genuine toxicity detector (toxic-vs-neutral
  AUC 0.71 base / 0.73 IT). The co-response UNIT does NOT detect the shift more reliably than the best single latent (abs-AUC-deviation
  difference CI includes 0; unit_wins=false), reported honestly. The result is stable across the gradual-scaling smoke/100/1200
  runs (toxicity unit AUC 0.459 -> 0.443 -> 0.438; genuine departure -> 0), evidence of a genuine null not noise. Honest framing:
  no gemma-scope-2b-it SAE exists, so this is an INFRASTRUCTURE-BOUNDED diffing result; the B1/B2/B3 bounds make the shared-SAE
  OOD confound explicit rather than leaving it as future work (cf. crosscoders, Anthropic 2024; Latent-Scaling misattribution
  risk, arXiv 2504.02922). Outputs: method.py (memory-safe one-model-at-a-time GPU pipeline), method_out.json + full/mini/preview
  variants (all validate against exp_gen_sol_out schema, all <1.7MB), and a results/per_text_arrays.npz sidecar of paired
  per-text arrays. Pure SAE/model inference; $0 LLM spend.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_5
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 16 ---
id: art_i-tkvFCKneA-
type: research
in_dependencies:
- id: art_RidEJtBC7gPT
  label: citations
title: >-
  CCRG Citation Audit: Chanin NeurIPS-2025 Fix, Muchane Resolved, Winnicki Contrast
summary: >-
  Closes the iteration-3 M8 novelty/citation minors for the two-track CCRG paper (pure web research). THREE DELIVERABLES.
  (A) A drop-in Winnicki-2026 contrast: arXiv:2604.23829 (Winnicki, Gnanasekaran, Darve; Stanford ICME; arXiv preprint, no
  venue) builds feature-level KG edges PURELY OBSERVATIONALLY (corpus co-occurrence graph weighted by Jaccard over binary
  presence matrices + transcoder cross-layer mechanism graph of source->target sparse latent pathways); a full-text grep finds
  ZERO occurrences of 'interventional/counterfactual/intervention', so it provably cannot draw CCRG's interventional anchor-205
  -> absorber-3069('list') edge (firing-Jaccard<0.1, never co-fire) nor the taxonomic 3792 -> Georgia/Jordan edges (diagnostic
  KG-agreement 0.318 vs 0.002 null; Jordan 0.99). 2-3 sentence + long paragraph versions provided. (B) Corrected citation
  table. CRITICAL FIX: Chanin 'A is for Absorption' (2409.14507) = NeurIPS 2025 ORAL (Dec 4 2025; forum R73ybUciQF; 6 authors
  incl. Golechha), NOT the dossier's 'NeurIPS 2024' (which is the separate NeurIPS-2024 Workshop version, forum Wzav8fesTL,
  5 authors, '...in Spelling Tasks'). Muchane2025 RESOLVES to arXiv:2506.01197 (Muchane/Richardson/Park/Veitch) -- no removal
  needed. Benchmark audit 2605.18229 is SOLE-authored by David Chanin (key 'Chanin2026' VALID). SASA 2606.06333 confirmed
  (Dalili & Mahdavi). AxBench 2501.17148 = ICML 2025 (not ICLR); SAEBench 2503.09532 = ICML 2025; CanonicalUnits 2502.04878
  = ICLR 2025; MindTheGAP 2403.09869 = AISTATS 2024. DPE 2505.23027 and SCR/TPP 2411.18895 have NO venue in arXiv metadata
  -> cite as preprints. SparseCoactivation 2506.18141 title is now '...Causal Semantic Modules...' (was 'Composable'). Full
  table + corrections diff + BibTeX in research_report.md. (C) Three-axis novelty confirmation -- interventional co-response
  grouping, set-cover-for-SAE-grouping, a-priori firing-structure router -- ALL HOLD, with cite-and-distinguish one-liners
  for the four near-misses (Winnicki 2604.23829; Deng 2506.18141 observational coactivation; CDLC 2505.07073 vision/diffusion
  analog; Kantamneni 2502.16681 post-hoc, not a-priori). Outputs: research_out.json {answer, sources(19), follow_up_questions(5)}
  + research_report.md.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
</all_artifacts>

<new_artifacts_this_iteration>
These 6 artifacts were created THIS iteration.

id: art_8AwUJK9qOwX_
type: experiment
in_dependencies:
- id: art_dpYpjSn2Xvg3
  label: dataset
- id: art_RidEJtBC7gPT
  label: method
- id: art_I2MrezW41iQo
  label: diagnostic
- id: art_YwjLYapklnVk
  label: surface-control
title: >-
  Iter-3 CCRG Re-Run: Random-Eligible-k Baseline, AUC-Difference CIs, Verdict Reconciliation
summary: >-
  Decisive iter-3 re-run of the two-track CCRG first-letter-spelling pipeline (frozen Gemma-Scope L12/16k JumpReLU SAE on
  gemma-2-2b), reusing iter-2's method.py verbatim and surgically adding three fixes. M1 (decisive): a RANDOM-ELIGIBLE-k (RE-k)
  baseline drawing k=|unit| latents uniformly at random from the cover-eligible set Lr, max-pooled identically to the unit/(h)/(b)/(c),
  so unit-minus-RE-k isolates two-track SELECTION from cover-based eligibility+pooling; added to C1 and E2. The single most
  decisive number is frac_rek_ge_unit (one-sided permutation p: fraction of random eligible pools matching/beating the unit).
  M2: replaces the iter-2 accuracy-as-margin artifact with threshold-free AUC POINTS plus bootstrap AUC-DIFFERENCE CIs (B>=10,000,
  content-flip pair-cluster resampling on the held-out test fold) for unit vs (a)/(b)/(c)/(h)/(RE-k) per letter, a pooled-across-letters
  stratified-bootstrap + inverse-variance meta-analysis, and a Youden-threshold accuracy table (no predict-all-positive collapse;
  the F1-threshold artifact is retained and flagged). M3: computes primary_endpoint from the stated falsifier (E1 AND unit-AUC-significantly-above-BOTH-(h)-AND-(RE-k)
  on >=3/5 letters => ABSORPTION_REPAIR_SELECTION_CONFIRMED; else REFRAMED_TO_ELIGIBILITY_POOLING; else SELECTION_NOT_ESTABLISHED),
  reporting E1 and E2 transparently and never dropping E2 from the conjunction. Reproduction is verified: gating cosine 0.924,
  deterministic baselines reproduce iter-2 (h-AUC 0.795 vs 0.794), E1_PASS and E2_PASS patterns match; the greedy set-cover
  unit AUC drifts within ~0.03 because iter-2's torch 2.6+cu126 cannot run on this RTX 5090 (Blackwell sm_120), requiring
  torch 2.8+cu128 (all other deps pinned identically). On L the unit significantly beats RE-k (frac_rek_ge_unit~0.009, diff
  +0.24 CI excludes 0) but ties the oracle attribution baseline h (CI includes 0) — the pre-registered expectation. All analysis
  is under metadata.* (per_letter, verdicts, pooled_across_letters, endpoint_reconciliation_note, admission on the 1,700-pair
  surface superset, config, gating_check); datasets carry per-letter held-out test-fold rows with predict_unit/a/b/c/h/REk
  (Youden-thresholded). Output validates against exp_gen_sol_out.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

id: art_P8-3ipCuQwVY
type: experiment
in_dependencies:
- id: art_t2uUbjSwpd3t
  label: dataset
- id: art_RidEJtBC7gPT
  label: method
- id: art_I2MrezW41iQo
  label: diagnostic
title: >-
  Non-Spelling SAE Absorption: RE-k Selection-Isolation, AUC-Diff CIs, Router Inputs
summary: |-
  Iteration-3 re-analysis of the executed iter-2 non-spelling SAE-absorption experiment. It reuses the frozen Gemma-Scope layer_12/width_16k SAE encodings (cached CSR latents + fp16 residuals) and the same two-track K-track unit/anchor/(g)/(h)/dense-probe, then adds the three iter-3-mandate analyses on the NON-SPELLING slices (taxonomic countries; numeric quantity types). Runs CPU-only via cache reuse (the RTX 5090 sm_120 is unsupported by torch 2.6.0+cu124, so the script auto-falls-back to CPU; the GPU re-encode path exists only for a cache miss, which never occurs). VERDICT = taxonomic_selection_established.

  M1 (selection isolation): adds a RANDOM-ELIGIBLE-k pool baseline (RE-k) and an anchor-fixed variant (RE-k-anchored) that separate the two-track set-cover SELECTION from cover-based eligibility+pooling. Rule selection_established(s) = (unit AUC > RE-k-anchored 95th pct) AND (paired AUC-difference CI vs RE-k-anchored mean excludes 0). TAXONOMIC Georgia: True (unit-RE-k-anchored = +0.099 [+0.085,+0.113], unit at 100th pct of draws). NUMERIC integer: False (unit-RE-k-anchored = +0.029 [-0.006,+0.062] includes 0) -> non-spelling numeric is eligibility+pooling, not set-cover selection.

  M2 (AUC + AUC-difference CIs): point AUC plus stratified paired-bootstrap AUC-DIFFERENCE CIs (B=10,000) for unit vs (g)/(h)/RE-k/RE-k-anchored/dense-probe on the defining absorbed slices (Georgia, integer), all 20 eligible countries / 8 numeric sub-contexts, and descriptive subs (Jordan, United States, decimal, year), replacing iter-2's mislabelled matched-recall-accuracy deltas. Georgia headline (pos=150 Georgia tokens vs 2100 taxonomic negatives): unit AUC=0.989, g=0.418, h=0.383 (below chance = absorption signature), RE-k=0.906, RE-k-anchored=0.890, dense-probe=1.000; unit-h=+0.606 [+0.570,+0.642] confirms a genuine AUC-rank effect (the R1 honesty fix), unit-dense=-0.011 [-0.015,-0.008] (the non-SAE probe slightly edges the unit but the unit is the best SAE detector). A comparison-matched Youden accuracy table is added so NO baseline is forced to predict-all (the artefact that made (h) look degenerate in iter-2).

  M7/M4 (router inputs): per-hierarchy firing-Jaccard(parent, top per-sub-context detector) on positives + parent per-sub-context recall holes + per-slice form-free KG top1, emitted as inputs for the M4 prediction-vs-outcome router table. absorption_type (parent hole>0.5 AND Jaccard<0.10) is True for exactly two countries -- Georgia (J=0.059, KG top1=1.0) and Jordan (n=124<150 descriptive, KG top1=0.95), the ambiguous homographs where the parent country-latent has a genuine recall hole; all other countries have parent_recall_hole~=0. Numeric integer router J=0.256 (co-firing, not mutually exclusive), KG mean top1=0.0. M7 framing: taxonomic = diagnostic_corroborated LEAD; numeric = suggestive_diagnostic_unconfirmed (dense-probe AUC=1.000 dominates, KG top1=0.0) and is NOT promoted.

  Deliverables: method.py (single pipeline = iter-2 core + iter-3 phases D-H), method_out.json / full|mini|preview_method_out.json (exp_gen_sol_out schema, PASSED, 8.5MB < 100MB; metadata.per_hierarchy carries auc_point, auc_diff_ci, rek_distribution, selection_established, youden tables, router+regime, generalization_status, honest_notes; datasets[].examples carry per-row diagnostic predictions predict_{unit,anchor,g,h,dense_probe,rek}), results/ (partial_{taxonomic,numeric}_iter3.json, results.json, auc_diff/router/sliced_recall CSVs, arrays npz), pyproject.toml (21 pinned deps), RESULTS_SUMMARY.md. Downstream GEN_PAPER_TEXT consumes this for the M1/M2/M7 non-spelling tables: taxonomic Georgia is the established selection win (and the only AUC-rank win that survives the anchor-fixed random control), numeric is honestly demoted to suggestive, and the router rows feed the M4 absorption-vs-splitting regime map.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

id: art_lvYKkaolutJG
type: experiment
in_dependencies:
- id: art_dpYpjSn2Xvg3
  label: dataset
- id: art_t2uUbjSwpd3t
  label: dataset
- id: art_RidEJtBC7gPT
  label: method
- id: art_I2MrezW41iQo
  label: diagnostic
title: >-
  Measured Auditability of Two-Track CCRG SAE Units: KG Repair Loop + LLM Member-Labeling
summary: |-
  Executes the two previously-dropped, now load-bearing M5 AUDITABILITY results for the two-track Counterfactual Co-Response Grouping (CCRG) units on a frozen Gemma-Scope L12/16k JumpReLU SAE (gating cosine 0.919, token localization exact, hidden_states[13]). Canonical units/KG are READ from the deterministic iter-2 outputs (first-letter exp_1, taxonomic exp_3) and re-derived as a cross-check (responsive set 682 vs iter-2 684; anchor 3792 matches). It converts the iter-2 'we emit a 70-edge graph' ASSERTION into MEASURED numbers.

  M5a KG-GUIDED REPAIR LOOP (load-bearing): for each under-served sub-context (recall hole where the anchor/parent latent goes silent) the KG names a covering absorber; we ADD it to the anchor (max-pool) and measure recall recovery on HELD-OUT corpus windows (selection split disjoint from eval split: taxonomic train->diagnostic; first-letter folds 0-3 -> fold 4) vs a control that adds the full population of other content-responsive latents, with a paired-bootstrap CI (B=10,000). Result: 8 measured successful repairs whose KG-minus-random gain CI excludes 0 -- taxonomic Georgia (anchor recall 0.20 -> 1.00, gain 0.80, 99.4th pct vs random, CI [0.70,0.82]), Jordan (0.29 -> 1.00/0.935), United States (0.77 -> 0.99/0.97), plus first-letter O/'our' and D/'day' (0.00 -> 1.00). BOTH the K-track edge (4697/9339/8442) and the higher-precision diagnostic-corroborated absorber (16009/540/846) are significant. Honest negatives: first-letter L ('list','line',...) and T ('type','things',...) candidate words tie the random-addition control (too few held-out windows / no extra localization) -- reported verbatim.

  M5a(k) LOCALIZATION-FAILURE CHECK: the label-free group-inference probe (k) (JTT: ERM -> upweight hardest/error set -> retrain) yields a dense hyperplane whose decoder-projection argmax is the PARENT 3792 (top |cos|=0.44, does not dominate; KG absorbers rank 2269/58/5964, never argmax). (k) classifies the holes (recall 1.0 on Georgia/Jordan/US) but exposes NO addable per-sub-context latent -- whereas the KG names exactly one. Country is linearly separable so the JTT error set is empty and we upweight the lowest-margin 20%; the structural conclusion is unchanged.

  M5b LLM-JUDGE MEMBER-LABELING (load-bearing): 67 unit members (anchor + absorbers across taxonomic + L/O/T/D) each described by logit-lens top-10 tokens + top-5 raw activating corpus windows with the sub-context label WITHHELD (non-leaky); anthropic/claude-haiku-4.5 (temp 0, forced-choice) names the sub-context. Agreement 0.716 vs shuffle null 0.090 (analytic chance 0.087); gap 0.627, bootstrap CI [0.522,0.731] excludes 0. Per-role: absorbers 0.76 accuracy, anchors 0.20 (judge over-specifies the parent's mixed-country/word windows -- honest caveat). 84 calls, 0 errors, total LLM spend $0.047 (<<$3 target).

  VERDICT: kg_utility_measured=True, member_labeling_above_null=True, replaces_iter2_assertion=True. Output method_out.json (exp_gen_sol_out-schema-valid, full/mini/preview all <100MB) stores per-sub-context repair stats (recall_anchor, recall_anchor_plus_kg, gain_kg, kg_percentile_vs_random, random_gain percentiles, paired_bootstrap_CI, k-track + diagnostic variants, honest_negatives), the (k) decoder-projection check, full member evidence + judge choices + scoring (gap CI, per-role accuracy, confusion), and a datasets block (kg_repair_loop rows; member_labeling rows with predict_judge) for downstream solution evaluation. This provides the paper's auditability section: the emitted feature knowledge-graph carries MEASURED localization utility and the cluster-level units are human/LLM-auditable, while example-reweighting baselines provide no addable per-feature unit.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_3
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

id: art_07ju05r0onqB
type: experiment
in_dependencies:
- id: art_dpYpjSn2Xvg3
  label: dataset
- id: art_t2uUbjSwpd3t
  label: dataset
- id: art_8QO7pl6Pd8UQ
  label: dataset
- id: art_21JWypIydPMX
  label: dataset
- id: art_RidEJtBC7gPT
  label: method
- id: art_I2MrezW41iQo
  label: diagnostic
title: >-
  Firing-Structure Router (M4): firing-Jaccard predicts when grouping beats attribution
summary: |-
  This experiment promotes the SAE-latent firing-Jaccard to a headline, a-priori router (M4) and validates it PROSPECTIVELY on a frozen Gemma-Scope SAE (google/gemma-scope-2b-pt-res, layer_12/width_16k/average_l0_82; model unsloth/gemma-2-2b; hook blocks.12.hook_resid_post; firing := encode>0; gating reconstruction-cosine 0.927, L0 median 70). method.py runs ONE uniform pipeline over 15 concepts: 12 ESTABLISHED (spelling L/O/T/I/D; numeric; taxonomic; toxicity threat/identity_attack/insult/obscene/sexual_explicit) used to DERIVE the rule, and 3 PROSPECTIVE (CAD-IMDB sentiment; CEBaB food/service aspect) predicted BEFORE their outcome is revealed. Per concept it (1) identifies a content-responsive parent latent on content-flip pairs (an unsupervised positive-firing-floor validation fixes the letter-I spurious-anchor bug), (2) finds per-sub-context detector latents + parent recall holes, (3) computes positive-only firing-Jaccard(detector,parent) over the concept's positives, and (4) measures a downstream OUTCOME: a LABEL-FREE CCRG K-track-lite unit (parent anchor + firing-disjoint, hole-covering absorbers) versus three required baselines at MATCHED pool size k -- (a) the best single raw SAE latent, (h) a supervised SAE standardized diff-of-means attribution pool (AxBench/SCR-TPP proxy), and (d) a non-SAE diff-of-means probe on the raw layer-12 residual -- scored by a held-constant logistic head on a held-out test fold with paired-bootstrap CIs (B=10000).

  KEY RESULTS: firing-Jaccard cleanly separates the regime EXTREMES -- spelling is firing-disjoint (Jaccard L=0.017, O=0.039, T=0.003, I=0.008, D=0.017, all <0.1; reproduces iter-2) and cluster-level grouping helps; toxicity co-fires (~0.69) so a single specialist latent wins. The primary router (predict absorption iff Jaccard<tau*) yields tau*=0.05, balanced accuracy 0.917 on the 12 established concepts; leave-one-concept-out accuracy 0.733; prospective out-of-sample accuracy 0.333 (sentiment HIT, predicted+measured co_firing; aspect_food/service MISS -- predicted co_firing but showed small absorption deltas +0.034/+0.071).

  HONEST FINDINGS (load-bearing for the paper): (i) firing-Jaccard ALONE is insufficient -- the TAXONOMIC counterexample has LOW Jaccard (0.056) yet a co_firing OUTCOME because the parent already has ~0.95 recall (no holes to fill); accordingly a recall-hole-only router (hole>0.777) reaches balanced accuracy 1.0 on established concepts, and a 2-signal router (low-Jaccard AND high-recall-hole) is also reported, supporting the refined rule 'grouping helps only when disjoint specialists AND parent recall holes co-occur'. (ii) The supervised baselines (h)/(d) frequently MATCH or beat the label-free unit on raw AUC (consistent with 'simple baselines are strong on raw-latent SAE tasks'); the unit's contribution is being LABEL-FREE while still beating the best single latent (a) in the absorption regime. (iii) numeric is reported honestly as suggestive/diagnostic-unconfirmed (absorption is documented empirically only on spelling).

  DELIVERABLES: method.py (self-contained, single-GPU, $0 LLM spend) and method_out.json with full/mini/preview variants (exp_gen_sol_out schema, all schema-PASSED, each <0.4MB). The output carries metadata with the prediction_vs_outcome_table (parent, jaccard min/median/max, recall_hole_max, predicted vs ground-truth regime, per-baseline AUCs auc_unit/auc_a/auc_h/auc_d, deltas with paired-bootstrap CIs, hit), per_concept_firing_jaccard (per-sub-context detector + bootstrap CIs), the router block (tau-sweep, regime separation, LOO per-concept, prospective table, plus strict-CI / recall-hole-only / combined router variants), a reproduction_check (spelling all <0.1 = True; toxicity references), and honest_notes. Expensive SAE forward passes are cached under cache/ (excluded from the published repo). Downstream GEN_PAPER_TEXT can use this as the M4 'when does cluster-level grouping help vs marginal attribution' router result and its honestly-reported boundary (firing-disjointness must co-occur with parent recall holes).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_4
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

id: art_jI2KIJotjzIU
type: experiment
in_dependencies:
- id: art_8QO7pl6Pd8UQ
  label: dataset
- id: art_dpYpjSn2Xvg3
  label: control-dataset
- id: art_RidEJtBC7gPT
  label: method
title: >-
  M6 Model-Diffing: Shared pt-SAE Co-Response Unit vs Best Latent, gemma-2-2b vs -it
summary: >-
  Delivers the M6 (model-diffing) downstream task for the Two-Track CCRG hypothesis: a single frozen Gemma-Scope layer-12/width-16k
  JumpReLU pretrained SAE (loaded directly from params.npz; reconstruction cosine 0.925 base / 0.913 IT, matching iter-2 ~0.92)
  applied to layer-12 residual activations of gemma-2-2b (base) vs gemma-2-2b-it (instruction-tuned), both unsloth ungated
  mirrors. METHOD = the iter-2 co-response UNIT (toxicity members {1920,12714,14630}; spelling-L 15-member anchor+absorber
  unit, anchor 205; both READ from iter-2 method_out.json). BASELINE = best single latent (toxicity anchor 12714) plus a descriptive
  oracle best-member. For 1200 toxic (civil_comments) and 1200 spelling-L corpus texts, it computes BOS-excluded max-pooled
  unit and single-latent responses on base vs IT, then base-vs-IT separability AUC, paired Cohen's d_z, a 2000x paired sign-flip
  shuffle null, and 2000x doc-bootstrap CIs. CONFOUND BOUNDING is load-bearing: B1 reconstruction parity (IT cosine 0.913
  not catastrophic, so the shared-base-SAE recipe is viable here); B2 control-concept floor (genuine toxicity shift = toxicity
  AUC-departure MINUS spelling-control departure); B3 residual-norm / norm-matched re-analysis (IT residual-stream norm 1.11x
  base). RESULT (verdict = clean-null-limitation, an explicitly valid M6 deliverable): a base-vs-IT shift IS detectable above
  the shuffle null for the toxicity unit (AUC 0.438, departure 0.062, p<1e-3, direction IT>base), but it is NOT concept-specific.
  The spelling control shows the SAME direction and an identical 0.062 departure, so the confound-controlled genuine toxicity
  shift is +0.000 (95% CI [-0.009, 0.007], includes 0); the norm-matched genuine shift is a small +0.027 (CI [0.021, 0.033])
  but still IT>base, OPPOSITE the naive detox prediction, i.e. generic OOD/norm drift rather than a concept-specific reduction
  in toxicity-feature usage. A within-model sanity check confirms the unit IS a genuine toxicity detector (toxic-vs-neutral
  AUC 0.71 base / 0.73 IT). The co-response UNIT does NOT detect the shift more reliably than the best single latent (abs-AUC-deviation
  difference CI includes 0; unit_wins=false), reported honestly. The result is stable across the gradual-scaling smoke/100/1200
  runs (toxicity unit AUC 0.459 -> 0.443 -> 0.438; genuine departure -> 0), evidence of a genuine null not noise. Honest framing:
  no gemma-scope-2b-it SAE exists, so this is an INFRASTRUCTURE-BOUNDED diffing result; the B1/B2/B3 bounds make the shared-SAE
  OOD confound explicit rather than leaving it as future work (cf. crosscoders, Anthropic 2024; Latent-Scaling misattribution
  risk, arXiv 2504.02922). Outputs: method.py (memory-safe one-model-at-a-time GPU pipeline), method_out.json + full/mini/preview
  variants (all validate against exp_gen_sol_out schema, all <1.7MB), and a results/per_text_arrays.npz sidecar of paired
  per-text arrays. Pure SAE/model inference; $0 LLM spend.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_5
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

id: art_i-tkvFCKneA-
type: research
in_dependencies:
- id: art_RidEJtBC7gPT
  label: citations
title: >-
  CCRG Citation Audit: Chanin NeurIPS-2025 Fix, Muchane Resolved, Winnicki Contrast
summary: >-
  Closes the iteration-3 M8 novelty/citation minors for the two-track CCRG paper (pure web research). THREE DELIVERABLES.
  (A) A drop-in Winnicki-2026 contrast: arXiv:2604.23829 (Winnicki, Gnanasekaran, Darve; Stanford ICME; arXiv preprint, no
  venue) builds feature-level KG edges PURELY OBSERVATIONALLY (corpus co-occurrence graph weighted by Jaccard over binary
  presence matrices + transcoder cross-layer mechanism graph of source->target sparse latent pathways); a full-text grep finds
  ZERO occurrences of 'interventional/counterfactual/intervention', so it provably cannot draw CCRG's interventional anchor-205
  -> absorber-3069('list') edge (firing-Jaccard<0.1, never co-fire) nor the taxonomic 3792 -> Georgia/Jordan edges (diagnostic
  KG-agreement 0.318 vs 0.002 null; Jordan 0.99). 2-3 sentence + long paragraph versions provided. (B) Corrected citation
  table. CRITICAL FIX: Chanin 'A is for Absorption' (2409.14507) = NeurIPS 2025 ORAL (Dec 4 2025; forum R73ybUciQF; 6 authors
  incl. Golechha), NOT the dossier's 'NeurIPS 2024' (which is the separate NeurIPS-2024 Workshop version, forum Wzav8fesTL,
  5 authors, '...in Spelling Tasks'). Muchane2025 RESOLVES to arXiv:2506.01197 (Muchane/Richardson/Park/Veitch) -- no removal
  needed. Benchmark audit 2605.18229 is SOLE-authored by David Chanin (key 'Chanin2026' VALID). SASA 2606.06333 confirmed
  (Dalili & Mahdavi). AxBench 2501.17148 = ICML 2025 (not ICLR); SAEBench 2503.09532 = ICML 2025; CanonicalUnits 2502.04878
  = ICLR 2025; MindTheGAP 2403.09869 = AISTATS 2024. DPE 2505.23027 and SCR/TPP 2411.18895 have NO venue in arXiv metadata
  -> cite as preprints. SparseCoactivation 2506.18141 title is now '...Causal Semantic Modules...' (was 'Composable'). Full
  table + corrections diff + BibTeX in research_report.md. (C) Three-axis novelty confirmation -- interventional co-response
  grouping, set-cover-for-SAE-grouping, a-priori firing-structure router -- ALL HOLD, with cite-and-distinguish one-liners
  for the four near-misses (Winnicki 2604.23829; Deng 2506.18141 observational coactivation; CDLC 2505.07073 vision/diffusion
  analog; Kantamneni 2502.16681 post-hoc, not a-priori). Outputs: research_out.json {answer, sources(19), follow_up_questions(5)}
  + research_report.md.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
</new_artifacts_this_iteration>

<current_paper>
The paper draft from this iteration — represents the current state of the research story.


# Introduction

Sparse autoencoders (SAEs) decompose the activations of large language models (LLMs) into a dictionary of sparsely-activating latents intended to be interpretable, monosemantic units of analysis \citep{Cunningham2023, Bricken2023, Templeton2024}. The promise is operational: a latent that reliably tracks a human concept can be read off as a classifier, flipped as a steering knob, or compared across model variants. Public SAE suites such as Gemma Scope \citep{Lieberum2024} expose millions of such latents over open models, making this a practical interface for safety-relevant interpretability.

This promise is undercut by a now well-documented fact: \emph{single SAE latents are not reliable units} \citep{Leask2025}. Two failure modes recur. \emph{Feature splitting} fragments one concept across many latents, so no single latent captures it. \emph{Feature absorption} is more insidious: a more specific child latent suppresses the firing of a more general parent, leaving the parent with unpredictable holes on exactly the sub-contexts the child covers; parent and child are \emph{mutually exclusive in firing} \citep{Chanin2024}. (A related failure, \emph{feature hedging}, merges correlated features into one polysemantic latent in narrow SAEs \citep{Chanin2025}; a hedged latent is not groupable and is out of scope.) On concrete downstream tasks the cost is stark: difference-of-means probes are the strongest concept detectors and raw-latent SAE methods are uncompetitive \citep{Wu2025, Kantamneni2025}, while standardized suites quantify absorption, sparse-probing, and targeted erasure \citep{Karvonen2025}. Any method proposing SAE latents as a knowledge representation must clear strong simple baselines and address splitting and absorption head-on.

The task is hard because the obstacles defeat the obvious instruments \emph{by construction}. The intuitive fix for an unreliable single latent is to group several latents into a cluster-level unit. But every existing post-hoc grouping signal is \emph{observational}: which latents fire together (co-activation feature families \citep{ONeill2024, Deng2025}) or which decoder directions point alike. Absorption is precisely the regime where observational signals must fail---the parent and the absorbing child are mutually exclusive in firing, so co-activation can never group them, and their decoders need not be cosine-similar \citep{Chanin2024}. The standard \emph{supervised} remedy, selecting the top-$N$ latents by causal effect on a concept probe (SCR/TPP attribution \citep{Karvonen2024, Marks2024}), is no better: a latent that fires only in a narrow sub-context has low \emph{marginal} attribution and is silently dropped, even though it carries the concept there. The latents one most needs are exactly the ones these instruments discard.

Why has this not been solved post-hoc? Recent architectural remedies---Matryoshka SAEs \citep{Bussmann2025}, hierarchical SAEs \citep{Muchane2025}, and subspace-aware SAEs \citep{Dalili2026}---all \emph{retrain} the SAE to reduce splitting and absorption at training time. They do not help a practitioner holding a frozen public SAE. We take the opposite stance: a \emph{training-free, post-hoc repair of frozen public SAEs}. The methodological gap we fill is the \emph{grouping operator}. Grouping by \emph{interventional co-response}---how latents jointly track a content counterfactual, rather than how they co-fire at baseline---is the matched instrument, with a direct precedent in systems biology, where differential co-expression methods (DiffCoEx \citep{Tesson2010}, WGCNA \citep{Zhang2005}) cluster genes by correlated response to a perturbation precisely because co-regulated genes are often not co-expressed at baseline. Crucially, correlation is the right operator only for the \emph{shared-support} splitting case. Absorbers respond on \emph{disjoint} supports and have low pairwise correlation, so no affinity-merging clustering can even \emph{propose} the right group. The disjoint-support case is a \emph{maximum-coverage} problem, whose classic greedy solution \citep{Nemhauser1978, Feige1998} is the natural---and, we argue, the only correct---proposer for absorption units.

We introduce \textbf{Two-Track Co-Response Grouping (CCRG)} and execute it on a frozen Gemma Scope SAE. This iteration is organized around the single hardest question a skeptical reviewer can ask of a pooling method: \emph{is the win due to the two-track set-cover selection, or merely to pooling any pile of eligible latents?} We answer it with a new \emph{random-eligible-$k$} (RE-$k$) control---a max-pool of $k$ latents drawn at random from the same cover-eligible set, differing from the unit \emph{only} in the membership criterion. Four findings result. (1) On the first-letter spelling testbed, the label-free unit beats the random-eligible pool on \emph{all five} letters (one-sided permutation $p\le 0.009$) and the count-matched supervised attribution pool on three of five, with true AUC-difference confidence intervals---establishing that the two-track \emph{selection}, not eligibility-plus-pooling, is what helps. (2) Absorption generalizes to a taxonomic is-a-country hierarchy, where an independent form-free diagnostic corroborates the recovered specialists and the selection survives an anchor-fixed random control; a numeric hierarchy is honestly demoted to suggestive. (3) A single forward-pass measurement of SAE-latent firing---the firing-Jaccard between candidate detectors and the parent---is an a-priori router that predicts which regime a concept is in before any grouping, validated prospectively across spelling, taxonomic, toxicity, sentiment, and aspect concepts. (4) The emitted feature knowledge graph carries \emph{measured} utility: a KG-guided edit recovers a parent's recall hole, beating a random-addition control with a confidence interval excluding zero.

[FIGURE:fig1]

\paragraph{Summary of contributions.}
\begin{itemize}
\item \textbf{A two-track grouping algorithm} (\S\ref{sec:method}): a training-free procedure that proposes split families by content-response correlation (C-track) and absorption units by an anchored greedy set-cover (K-track), with an unsupervised parent-validation step, reconciled and filtered by a single null-anchored, multiplicity-controlled admission rule. To our knowledge maximum-coverage set-cover has not previously been used to group SAE latents.
\item \textbf{Selection isolated from pooling} (\S\ref{sec:firstletter}): against the new random-eligible-$k$ control the unit wins on all five letters, with true AUC-difference CIs replacing the previous iteration's mislabeled accuracy margins, and the primary endpoint reconciled to be honestly falsifiable and code-honored.
\item \textbf{Absorption generalizes beyond spelling}, led by a diagnostic-corroborated taxonomic hierarchy where selection survives an anchor-fixed random control; numeric is reported as suggestive and diagnostic-unconfirmed (\S\ref{sec:nonspelling}).
\item \textbf{An a-priori firing-structure router} that predicts when grouping helps, validated prospectively, with its honest boundary: firing-disjointness must co-occur with parent recall holes (\S\ref{sec:router}).
\item \textbf{Measured auditability}: a KG-guided recall-repair loop and an LLM member-labeling test, both beating null controls---a decision-relevant dimension a dense probe lacks (\S\ref{sec:audit}).
\item \textbf{Four frozen testbeds, a single-GPU pipeline, and honestly reported failure modes}, including a co-firing toxicity regime where CCRG does not help and a confound-bounded null model-diffing result (\S\ref{sec:setup}, \S\ref{sec:other}).
\end{itemize}

# Related Work
\label{sec:related}

\paragraph{SAEs and the unreliability of single latents.} Sparse dictionary learning on LLM activations yields interpretable features \citep{Cunningham2023, Bricken2023, Templeton2024, Lieberum2024}, but a growing body of work shows individual latents are not canonical units \citep{Leask2025}. \citet{Chanin2024} introduce and quantify \emph{feature absorption}---a specific child latent suppresses a general parent's firing---demonstrated on first-letter spelling, and \citet{Chanin2025} characterize \emph{hedging}. Benchmarks make the practical cost concrete: AxBench finds difference-of-means strongest and raw-latent SAE methods uncompetitive \citep{Wu2025}; a sparse-probing case study reaches the same conclusion \citep{Kantamneni2025}; SAEBench standardizes absorption, sparse-probing, and erasure evaluations \citep{Karvonen2025}; and recent audits caution these benchmarks are imperfect ground truth \citep{Chanin2026}. We do not stake our load-bearing claim on out-classifying a strong dense probe; our central comparison is against SAE-\emph{selection} baselines.

\paragraph{Post-hoc grouping of SAE features.} Prior grouping is observational: co-activation ``feature families'' \citep{ONeill2024} and sparse feature coactivation modules \citep{Deng2025} group latents by what fires together or which decoders align. Closest to our output, \citet{Winnicki2026} build a feature-level knowledge graph from SAE features. Because both methods emit a knowledge graph, the distinction is the \emph{edge semantics}, not the artifact. Their edges come from three purely observational sources---a corpus co-occurrence graph weighted by the Jaccard overlap of binary feature-presence matrices, a transcoder-based cross-layer mechanism graph linking source- and target-layer latents through sparse pathways, and contrastive domain filtering---with no interventional or counterfactual signal anywhere in the pipeline. Such edges cannot, by construction, express CCRG's central relation: on the first-letter-L task CCRG joins anchor latent 205 to absorber latent 3069 (auto-interp label ``list''), two latents that are \emph{mutually exclusive in firing} (firing-Jaccard $<0.1$). A Jaccard co-occurrence edge between them is $\approx 0$ by definition, decoder geometry need not relate them, and a cross-layer transcoder graph encodes inter-layer pathways rather than within-layer firing-complementarity. CCRG's edge is interventional---the two latents track the same content counterfactual on disjoint supports---and the same structure recurs taxonomically, where CCRG recovers is-a-country anchor (3792) $\to$ Georgia/Jordan specialist edges that an independent form-free diagnostic corroborates. We count-match observational clusters to our unit's size so any classification win reflects \emph{selection}, not capacity.

\paragraph{Supervised latent selection.} SHIFT and the SCR/TPP family rank individual latents by causal effect on a concept probe and ablate the top-$N$ \citep{Marks2024, Karvonen2024}. A latent firing only in a narrow sub-context has low marginal attribution and is silently dropped---the exact gap our co-response set-cover fills. We use SCR/TPP-style ranking as our oracle-pool baselines (g)/(h).

\paragraph{Architectural remedies vs.\ our setting.} Matryoshka \citep{Bussmann2025}, hierarchical \citep{Muchane2025}, and subspace-aware \citep{Dalili2026} SAEs modify \emph{training} to reduce splitting/absorption. They are orthogonal: we repair a \emph{frozen} public SAE post-hoc and emit an auditable graph rather than retraining.

\paragraph{Cross-field instruments and robustness.} The C-track imports differential co-expression module discovery \citep{Tesson2010, Zhang2005} and Leiden community detection \citep{Traag2018}; the K-track imports the maximum-coverage greedy with its $(1-1/e)$ guarantee \citep{Nemhauser1978, Feige1998}. The robustness framing engages label-free worst-group-robustness work---group-DRO \citep{Sagawa2019}, JTT \citep{Liu2021}, GEORGE \citep{Sohoni2020}, EIIL \citep{Creager2020}, LfF \citep{Nam2020}, group-aware priors \citep{Rudner2024}, and diverse prototypical ensembles \citep{To2025}---which infer groups over \emph{examples} and \emph{retrain}; CCRG groups \emph{features}, never retrains, and the recovered absorbers \emph{are} the inferred sub-context specialists. Surface-invariance draws on LEACE \citep{Belrose2023} and counterfactual invariance \citep{Veitch2021}; minimal-pair supervision draws on counterfactually-augmented data \citep{Kaushik2019}, CEBaB \citep{Abraham2022}, and ParaDetox \citep{Logacheva2022}. The closest ``cluster counterfactual differences'' template is CDLC in vision \citep{Varshney2025}, which clusters diffusion-counterfactual difference vectors into one continuous direction per class; we cluster \emph{discrete} LLM SAE latents into multi-member units and add a set-cover track for which CDLC has no analogue.

# The Two-Track Co-Response Grouping Method
\label{sec:method}

\paragraph{Preliminaries.} Let the frozen SAE have latents $l \in \{1,\dots,L\}$ with encoder activation $a_l(x)$; a latent \emph{fires} on $x$ iff $a_l(x) > 0$ (Gemma Scope uses a JumpReLU, so the threshold is inside the encoder \citep{Lieberum2024}). For a concept $c$ we are given \emph{content-flip minimal pairs} $(x_{\text{off}}, x_{\text{on}})$ in which the concept is absent/present at matched surface form, plus \emph{surface-flip pairs} in which the concept is held constant and surface varies. Content labels are the supervision every matched baseline consumes; the method uses no absorption-specific oracle. We encode at one residual-stream site (\texttt{gemma-2-2b}, layer 12, width 16k canonical; $d_{\text{model}}=2304$, 16{,}384 latents) \citep{Lieberum2024}.

\paragraph{Step 1: interventional content-response.} For each latent $l$ and pair $p$, the \emph{content-response} is $r_l(p) = a_l(x_{\text{on}}) - a_l(x_{\text{off}})$. A latent's \emph{cover set} $C_l$ is the set of pairs whose content flip it tracks reliably ($r_l(p)>\tau_{\text{resp}}$ and $a_l(x_{\text{on}})>0$) and precisely (firing-precision $\geq 0.7$ on its own support). Because absorbers fire on only a handful of words, a mean-over-pairs prefilter would discard them; eligibility is therefore \emph{cover-based} (selective \emph{and} covering $\geq 1$ sub-context), which retains the genuinely sparse absorbers. We denote the cover-eligible set $E$.

[FIGURE:fig2]

\paragraph{Step 2: C-track --- correlation communities for splitting.} Where a concept \emph{splits}, sub-latents share firing support and co-respond positively, so pairwise affinity is appropriate. We build a sign-aware soft-thresholded affinity from the positive part of the Spearman correlation between response profiles, $A^{C}_{l,l'} = \max(\rho(r_l, r_{l'}), 0)^{\beta}$ with $\beta=6$ (WGCNA's scale-free criterion \citep{Zhang2005}), and run Leiden community detection (RBConfiguration partition \citep{Traag2018}), with resolution fixed by bootstrap-ARI stability against a shuffle null. (Leiden's C extension intermittently hangs on tied-rank graphs; we run it in a 45\,s-timeout subprocess and fall back to agglomerative clustering, recorded per run.)

\paragraph{Step 3: K-track --- anchored greedy set-cover for absorption.} Absorbers respond on \emph{disjoint} supports and are mutually exclusive in firing with their parent, so their pairwise correlation is low and no affinity-merging clustering can propose them (Figure~\ref{fig:tracks}). We use an anchored greedy maximum-coverage procedure. \textbf{(1) Anchor:} $l^\* = \arg\max_l |C_l|$, the highest-recall ``parent'' candidate, chosen using \emph{only} the pairs and \emph{not} the absorption diagnostic, with ties broken toward broadest support. An \emph{unsupervised parent-validation} step then requires the anchor to fire on the held-out corpus above a floor; this rejects a spurious high-cover-set latent that fires $0\%$ on the corpus (the letter-I failure mode in \S\ref{sec:firstletter}) rather than crowning it anchor. \textbf{(2) Holes:} $H = P \setminus C_{\text{anchor}}$, the pairs the parent goes silent on. \textbf{(3) Greedy cover:} while $H$ is non-empty and improving, add $\arg\max_l |C_l \cap H|$ subject to mutual exclusivity (firing-Jaccard $<0.1$ with members), per-member precision $\geq 0.7$, and a marginal-coverage-gain floor $\geq 0.05$ whose bootstrap CI excludes 0. The greedy max-coverage choice is the classic instrument for ``cover a universe with complementary specialists'' \citep{Nemhauser1978, Feige1998}; coverage-complementarity is a set-level property that a pairwise operator cannot express.

\paragraph{Step 4: reconciliation.} For each C-community we designate its highest-recall member as a candidate anchor and run Step 3 to pull in mutually-exclusive absorbers covering its holes; we also seed Step 3 from standalone high-recall latents in no dense community. A final unit is a pure C-community (splitting), a pure K-cover (absorption), or a hybrid; we de-duplicate by highest coverage gain.

\paragraph{Step 5: admission filter with multiplicity control.} A proposed unit is admitted iff it clears \textbf{signature C} (within-unit content-response correlation above the 95th-percentile shuffle null) \textbf{or signature K} (pooled-max minus best-single content-response AUC above the 95th percentile of a best-of-random-$k$ null \emph{matched on marginal AUC}, plus the $k\in\{2,3\}$ absolute gain floor of $0.05$ with bootstrap CI excluding 0, plus mutual exclusivity and the precision floor), \textbf{and} unit-level surface invariance (pooled surface-response not above the shuffled-surface null). Because many candidate units are tested per concept, we control multiplicity at the \emph{unit-proposal} level: a Bonferroni-within-unit $p$ over the disjunctive signature, then Benjamini--Hochberg across the $M$ candidate units, and we report $M$ and the \emph{empirical} family-wise false-admit rate under the matched random-$k$ null.

\paragraph{The decisive selection control (RE-$k$).} A pooling method must rule out the simplest alternative explanation: that \emph{any} $k$ eligible latents, pooled, beat a size-matched competitor. We therefore add a \emph{random-eligible-$k$} baseline: draw $k=|\text{unit}|$ latents uniformly from $E$, max-pool with the identical rule, and repeat over $B_{\text{draws}}=1{,}000$ draws. Because RE-$k$ differs from the unit \emph{only} in the membership criterion---eligibility filter, pool size, and max-pool are held constant---the quantity $\text{unit}-\text{RE-}k$ isolates \emph{selection} from eligibility-plus-pooling. The decisive scalar is $\text{frac\_rek\_ge\_unit}$, the fraction of random eligible pools whose held-out AUC matches or beats the unit (a one-sided permutation $p$-value). We add RE-$k$ to classification (C1) and absorbed-slice recall (E2) on every concept, and an anchor-fixed variant (RE-$k$-anchored, parent held fixed and only the absorbers randomized) on the non-spelling slices.

\paragraph{Non-circular diagnostic and auditable graph.} Specialization edges are \emph{scored}, never formed, by the absorption diagnostic of \citet{Chanin2024}. Because the strict form needs an output logit, we use the domain-agnostic \emph{form-free} variant (the appendix probe-projection, implemented in SAEBench as \texttt{absorption\_fraction}): $l$ absorbs iff $\tau_c < (\hat{a}_l \cdot d_p)/(a \cdot d_p)$, with $d_p$ a parent-concept probe trained on data \emph{disjoint} from clustering. The anchor is chosen by recall available to every baseline, so ``the unsupervised unit beats the supervised oracle'' is not undercut. Each admitted unit is emitted with logit-lens tokens and top conditioning contexts, plus directed anchor$\to$child specialization edges---a feature-level knowledge graph.

# Testbeds, Baselines, and Protocol
\label{sec:setup}

\paragraph{Constructed testbeds.} We built four frozen, schema-standardized families (Table~\ref{tab:testbeds}) totalling 109{,}754 examples. All are pure text/data artifacts---no SAE or model weights baked in---so absorption presence is an empirical question for the SAE run, not a construction artifact. Words for the spelling and non-spelling hierarchies are anchored in the real \texttt{gemma-2-2b} vocabulary and a pinned Pile revision, so they never derive from the latents being grouped. The first-letter testbed contributes 17{,}180 examples over five letters (L/O/T/I/D) with 0 deterministic flip/span violations [ARTIFACT:art_dpYpjSn2Xvg3]; the non-spelling testbed contributes 24{,}128 examples over a numeric-quantity hierarchy and a taxonomic is-a-country hierarchy [ARTIFACT:art_t2uUbjSwpd3t]; the toxicity family contributes 37{,}707 examples from ParaDetox \citep{Logacheva2022} and civil\_comments \citep{Borkan2019} [ARTIFACT:art_8QO7pl6Pd8UQ]; and a supporting family contributes 30{,}739 examples of CAD-IMDB sentiment \citep{Kaushik2019}, CEBaB aspect-sentiment \citep{Abraham2022}, and a bias\_in\_bios boundary-null \citep{DeArteaga2019} [ARTIFACT:art_21JWypIydPMX].

\begin{table}[t]
\centering
\small
\caption{Constructed testbeds. Counts are released examples. LB = load-bearing, NS = non-spelling spine, SP = supporting, BN = boundary-null.}
\label{tab:testbeds}
\begin{tabular}{lllrl}
\toprule
Family & Source & Concepts & Examples & Role \\
\midrule
First-letter spelling & Pile + gemma vocab & 5 letters (L/O/T/I/D) & 17{,}180 & LB \\
Non-spelling absorption & Pile + templates + LLM & numeric (8 sub), taxonomic (countries) & 24{,}128 & NS \\
Toxicity & ParaDetox, civil\_comments & toxicity + 6 sub-attributes & 37{,}707 & LB \\
Sentiment / aspect / bias & CAD-IMDB, CEBaB, bias\_in\_bios & sentiment, food/service, 28 professions & 30{,}739 & SP / BN \\
\midrule
\textbf{Total} & & 12 dataset groups & \textbf{109{,}754} & \\
\bottomrule
\end{tabular}
\end{table}

\paragraph{Baselines.} We compare CCRG units against twelve baselines (Table~\ref{tab:baselines}), spanning raw latents, observational clusters (count-matched), dense probes (including a LEACE surface-invariant hyperplane), supervised oracle pools, label-free/oracle group-robustness probes, and---decisively---the random-eligible-$k$ pool. The design isolates \emph{selection at matched pool size}: a unit win over (h) holds capacity fixed and varies how members are chosen, and a unit win over (RE-$k$) holds eligibility and pooling fixed and varies only the selection criterion.

\begin{table}[t]
\centering
\small
\caption{Baseline glossary. (b)/(c) are count-matched to the unit's member count $k$; (h) is count-and-pool-matched; (RE-$k$) is the random-eligible-$k$ selection control added this iteration.}
\label{tab:baselines}
\begin{tabular}{cl}
\toprule
ID & Baseline \\
\midrule
(a) & Best raw single latent (held-out AUC/F1) \\
(b) & Observational co-activation / feature-family clusters, count-matched to $k$ \\
(c) & Decoder-geometry (cosine) clusters, count-matched to $k$ \\
(d) & Counterfactually-matched difference-of-means \\
(e) & Linear probe on raw residual activations \\
(f) & Surface-invariant matched probe (LEACE-erased surface direction) \\
(g) & Supervised oracle pool: top-$N$ latents by SCR/TPP attribution \\
(h) & Count-and-pool-matched: max-pool over exactly $k$ SCR/TPP-selected directions \\
(i) & Unmatched difference-of-means / probe on raw labels \\
(j) & Oracle group-DRO probe with true sub-context labels (robustness upper bound) \\
(k) & Label-free group-inference probe (JTT/GEORGE-style) \\
(RE-$k$) & \textbf{Random-eligible-$k$ pool: $k$ latents drawn at random from $E$, max-pooled} \\
\bottomrule
\end{tabular}
\end{table}

\paragraph{Encoding and gating.} The SAE is loaded directly from Gemma Scope \texttt{params.npz} (canonical \texttt{layer\_12/width\_16k}); the residual is captured by a forward hook on \texttt{model.layers[12]}. Each run gates on reconstruction fidelity before analysis: first-letter reconstruction cosine $0.924$, explained variance $0.857$, mean L0 $96.1$ [ARTIFACT:art_8AwUJK9qOwX_]; toxicity cosine $0.916$ [ARTIFACT:art_-o2RPMOZp37A]; non-spelling encode-time FVU $0.18$/$0.20$ with token-alignment $0.975$/$1.000$ [ARTIFACT:art_QGSdsKY6U1vK]; the auditability and router runs gate at cosine $0.919$ and $0.927$ respectively [ARTIFACT:art_lvYKkaolutJG, art_07ju05r0onqB]. (The iter-3 re-runs use \texttt{torch~2.8+cu128} for Blackwell-class GPUs; AUC is rank-based and robust to the residual bf16 differences, and the deterministic baselines reproduce the previous iteration to within $\pm 0.001$ AUC.)

\paragraph{Statistics and the primary endpoint.} The primary statistical object is the per-concept paired bootstrap of the AUC difference ($B=10{,}000$, resampling whole content-flip pairs as clusters on the held-out test fold), with exact McNemar confirmatory tests and Holm--Bonferroni across headline claims; any accuracy comparison uses a comparison-matched Youden threshold so no baseline collapses to predict-all-positive. We declare a single, code-honored \emph{primary endpoint} on first-letter (the guaranteed-signal regime): CCRG \emph{works in the absorption regime} iff (E1) the K-track proposal step, given only content-flip pairs, recovers the diagnostic parent plus $\geq 2$ absorbers above a random-membership null, \emph{and} (C1-AUC) the label-free unit's classification AUC significantly exceeds \emph{both} the count-matched attribution pool (h) \emph{and} the random-eligible-$k$ pool on a majority ($\geq 3/5$) of letters. The RE-$k$ comparison is what makes this a \emph{selection} claim rather than a pooling claim, and it can genuinely kill the claim. The absorbed-slice recall test (E2) is retained as a \emph{secondary characterization}, reported per-letter and never dropped from the conjunction.

# Results: First-Letter Spelling --- Selection Isolated
\label{sec:firstletter}

We ran the full pipeline on all five letters with \$0 in LLM spend (the diagnostic is the form-free probe-projection) [ARTIFACT:art_8AwUJK9qOwX_]. The decisive question this iteration answers is whether the contribution is two-track \emph{selection} or merely cover-based eligibility plus 15-way max-pooling, which a previous reviewer correctly flagged as unaddressed.

\paragraph{C1 (corrected): true AUC margins with difference CIs.} The previous draft reported per-example \emph{accuracy} differences mislabeled as AUC margins, inflated on letters I and D by an attribution baseline whose F1-optimal threshold collapsed to predict-all-positive. We replace this with threshold-free AUC points and bootstrap AUC-\emph{difference} CIs (Table~\ref{tab:c1}, Figure~\ref{fig:c1}). The co-response unit attains the highest held-out AUC on every letter (L $0.876$, O $0.917$, T $0.858$, I $0.956$, D $0.886$). Against the count-and-pool-matched attribution pool (h) the gain is significant on three of five letters (T $+0.218$, CI $[0.115,0.310]$; I $+0.227$, CI $[0.146,0.304]$; D $+0.156$, CI $[0.058,0.254]$) and \emph{not} significant on L ($+0.081$, CI $[-0.008,0.160]$) or O ($+0.096$, CI $[-0.019,0.208]$). We state this plainly: on true AUC, two of five letters do not separate from supervised attribution, exactly as a careful reading predicts. The pooled stratified-bootstrap gain over (h) is $+0.162$, CI $[0.118,0.202]$ (inverse-variance $p\approx 2\times 10^{-14}$).

\begin{table}[t]
\centering
\small
\caption{First-letter C1 classification AUC and AUC-difference CIs (paired bootstrap, $B=10{,}000$, pair-cluster resampling; $n=30$--$45$ held-out test pairs per letter). The unit beats the random-eligible-$k$ control (RE-$k$) on all five letters and the count-matched attribution pool (h) on three. $^\ast$ = CI excludes 0.}
\label{tab:c1}
\begin{tabular}{lcccccc}
\toprule
Letter & unit & (h) & RE-$k$ & unit$-$(h) [CI] & unit$-$RE-$k$ [CI] & frac$_{\text{RE-}k\ge\text{unit}}$ \\
\midrule
L & 0.876 & 0.795 & 0.637 & $+0.081\ [-0.008,0.160]$ & $+0.239\ [0.153,0.326]^\ast$ & 0.009 \\
O & 0.917 & 0.821 & 0.633 & $+0.096\ [-0.019,0.208]$ & $+0.283\ [0.183,0.383]^\ast$ & 0.000 \\
T & 0.858 & 0.640 & 0.692 & $+0.218\ [0.115,0.310]^\ast$ & $+0.166\ [0.037,0.283]^\ast$ & 0.006 \\
I & 0.956 & 0.729 & 0.667 & $+0.227\ [0.146,0.304]^\ast$ & $+0.289\ [0.214,0.360]^\ast$ & 0.000 \\
D & 0.886 & 0.730 & 0.668 & $+0.156\ [0.058,0.254]^\ast$ & $+0.218\ [0.118,0.319]^\ast$ & 0.000 \\
\midrule
\textbf{Pooled} & & & & $+0.162\ [0.118,0.202]^\ast$ & $+0.237\ [0.191,0.280]^\ast$ & \\
\bottomrule
\end{tabular}
\end{table}

\paragraph{The selection control settles the question.} Against the random-eligible-$k$ pool---which holds eligibility, pool size, and max-pooling fixed and varies \emph{only} the membership criterion---the unit wins on \emph{all five} letters with CIs excluding 0 (L $+0.239$, O $+0.283$, T $+0.166$, I $+0.289$, D $+0.218$; pooled $+0.237$, CI $[0.191,0.280]$). The one-sided permutation $p$ (fraction of $1{,}000$ random eligible pools matching or beating the unit) is $\le 0.009$ on every letter and exactly $0.000$ on four. The two-track set-cover selection, not eligibility-plus-pooling, is what beats both the random pool and---on the harder letters---supervised attribution. The unit also beats the count-matched observational clusters (b)/(c) significantly on O, T, I, D and the best raw latent (a) on O, T, I, D (not on L, where the best raw latent is already AUC $0.848$).

[FIGURE:fig3]

\paragraph{The primary endpoint, honored.} Under the endpoint stated in \S\ref{sec:setup}, E1 (proposal recovers parent $+\geq 2$ absorbers above the random-membership null) holds on 4/5 letters; the joint selection test (unit AUC significantly above \emph{both} (h) and RE-$k$) holds on T, I, and D ($3/5$). The verdict the pipeline emits is therefore \texttt{ABSORPTION\_REPAIR\_SELECTION\_CONFIRMED} [ARTIFACT:art_8AwUJK9qOwX_]. We reconcile this with the previous iteration honestly: the earlier code computed an unqualified ``WORKS'' as $\text{E1}\wedge\text{C1}$, silently dropping the absorbed-slice recall test (E2) from the conjunction and reporting no RE-$k$ control. The current verdict is computed from the stated falsifier, reports E1, E2, and the selection test independently, and would have returned \texttt{REFRAMED\_TO\_ELIGIBILITY\_POOLING} had the unit failed to beat RE-$k$---a publishable outcome that did not occur.

\paragraph{E1 absorber recovery and the letter-I lesson.} Given only content-flip pairs, the K-track recovers the diagnostic parent plus $\geq 2$ absorbers above the 95th-percentile random-membership null on L, O, T, and D. The units are human-auditable: for L, anchor latent 205 (logit-lens \texttt{Lohan/Ls/LS/LF}) plus absorbers 3069=\texttt{list}, 2416=\texttt{line}, 3353=\texttt{level}, 3858=\texttt{low}; for D, anchor 6210 (\texttt{PhysRevD/DPR/DSS}) plus 1970=\texttt{different}, 7293=\texttt{director}, 10769=\texttt{day}. A 70-edge anchor$\to$absorbed-child knowledge graph is emitted. E1 \emph{fails} on I by anchor fidelity only: the highest-cover-set latent (1227) fires $0\%$ on the corpus and has code-token logit-lens---a spurious anchor. We treat this as a mechanism finding and add the unsupervised parent-validation step (\S\ref{sec:method}) that rejects it; the pooled unit nonetheless remains the best I classifier (AUC $0.956$).

\paragraph{E2 absorbed-slice recall (secondary).} On the absorbed slice---words where the parent goes silent---the unit beats the count-matched pool (h) directionally on all five letters and significantly on the best-powered slice T ($0.925$ vs.\ $0.763$, CI of difference $[0.054,0.269]$); the other slices are directional but not significant (e.g.\ L $0.800$ vs.\ $0.750$, CI $[-0.058,0.158]$; I $0.767$ vs.\ $0.705$, CI $[-0.047,0.171]$), and per-slice $n$ is $93$--$129$. We base the headline on the non-circular AUC and selection tests rather than a recovered-absorber count, which is circular for the oracle baselines because the diagnostic and the attribution pools both rank by the same probe direction.

\paragraph{Admission.} The K-unit is admitted via signature K on all five letters (surface-invariant, $p_{\text{surf}}=1.0$, on the enlarged 1{,}700-pair independently re-judged surface superset [ARTIFACT:art_YwjLYapklnVk]); the empirical false-admit rate under the matched random-$k$ null is $0.05$--$0.11$, at or near the $0.05$ target. We note honestly that within the eligible set random $k$-pools also clear the admission \emph{gain floor}, so the admission filter's discriminative power comes from the surface-invariance gate and the matched-null signature-K test; the \emph{classification} separation from random pools, however, is large and significant (the RE-$k$ result above).

# Results: Absorption Generalizes Beyond Spelling
\label{sec:nonspelling}

Absorption is documented empirically almost only on first-letter spelling: the original study is spelling-only \citep{Chanin2024}, SAEBench's sole absorption eval is \texttt{absorption\_first\_letter} \citep{Karvonen2025}, and the Matryoshka/hierarchical mitigations measure it via the spelling metric \citep{Bussmann2025, Muchane2025}. We therefore treat the non-spelling testbed as both a generality test and a novel empirical question, and---following reviewer guidance---\emph{lead with the diagnostic-corroborated taxonomic hierarchy} and report numeric as suggestive [ARTIFACT:art_P8-3ipCuQwVY].

\paragraph{Taxonomic (lead): selection survives an anchor-fixed random control.} On the is-a-country hierarchy the parent latent 3792 (recall $0.953$) admits Georgia, Jordan, and United-States specialists. On the defining absorbed slice \texttt{Georgia} (positives = 150 Georgia tokens vs.\ 2{,}100 taxonomic negatives), the compact 4-latent unit reaches AUC $0.989$, while the marginal-attribution pools fall \emph{below chance} ((g) $0.418$, (h) $0.383$)---the absorption signature, where top-marginal pools fire on negatives but are silent on the absorbed slice. The AUC-difference is a genuine rank effect, not the operating-point artifact of the previous matched-recall table: unit$-$(h) $=+0.606$, CI $[0.570,0.642]$. Crucially, the set-cover selection survives the \emph{anchor-fixed} random control (RE-$k$-anchored, parent held fixed and only absorbers randomized): unit$-$RE-$k$-anchored $=+0.099$, CI $[0.085,0.113]$, with the unit at the 100th percentile of random draws. The independent form-free diagnostic corroborates the recovered edges (KG-agreement top-1 $0.318$ vs.\ a $0.002$ null; the Jordan edge agrees at $0.99$). Honestly, a non-SAE dense probe edges the unit on Georgia ($1.000$ vs.\ $0.989$, unit$-$dense $=-0.011$, CI $[-0.015,-0.008]$): the unit is the best \emph{SAE} detector and beats every SAE baseline and both random controls, but it does not out-classify a strong dense probe.

\paragraph{Numeric (suggestive, diagnostic-unconfirmed).} On the numeric hierarchy the parent latent 14823 (content-response precision $1.000$) covers $0.829$ of content flips but only $0.427$ of the corpus, missing $1{,}060$ positives, and the K-track fills them with year/decimal detectors. On the defining \texttt{integer} slice the unit (AUC $0.687$) beats (g) ($+0.128$, CI $[0.092,0.164]$), (h) ($+0.114$, CI $[0.074,0.153]$), and the plain RE-$k$ control ($+0.057$, CI $[0.024,0.090]$), but the \emph{anchor-fixed} control is not cleared: unit$-$RE-$k$-anchored $=+0.029$, CI $[-0.006,0.062]$ (includes 0). The numeric win is therefore \emph{eligibility-plus-pooling, not set-cover selection}. The form-free diagnostic also fails to corroborate the numeric edges (KG top-1 $=0.0$; firing-Jaccard $0.256$, i.e.\ co-firing not mutually exclusive), and a dense probe dominates (AUC $1.000$). We report numeric as a complementary-detector recovery whose \emph{absorber} status is not independently confirmed, and do not promote it (Table~\ref{tab:nonspelling}).

\begin{table}[t]
\centering
\small
\caption{Non-spelling absorber recovery, AUC on the defining absorbed slice with AUC-difference CIs. Taxonomic (Georgia) clears the anchor-fixed random control (selection established); numeric (integer) does not (eligibility+pooling). A dense probe matches/dominates both---the contribution is a within-SAE selection win plus diagnostic corroboration, not a non-SAE classification win.}
\label{tab:nonspelling}
\begin{tabular}{llcccccc}
\toprule
Hierarchy & Slice & unit & (h) & RE-$k$-anch.\ [CI] & dense & KG top-1 & selection? \\
\midrule
Taxonomic & \texttt{Georgia} & \textbf{0.989} & 0.383 & $+0.099\ [0.085,0.113]^\ast$ & 1.000 & 0.318 & \textbf{yes} \\
Numeric & \texttt{integer} & 0.687 & $\approx$0.57 & $+0.029\ [-0.006,0.062]$ & 1.000 & 0.000 & no \\
\bottomrule
\end{tabular}
\end{table}

# Results: An A-Priori Firing-Structure Router
\label{sec:router}

Because the contribution is regime-scoped, its practical value depends on being able to tell, \emph{before} grouping, which regime a concept is in. We promote the SAE-latent firing-Jaccard to a headline, a-priori router and validate it prospectively across 15 concepts [ARTIFACT:art_07ju05r0onqB]. The router is one forward pass over data already held: encode examples, identify the content-responsive parent latent (with the unsupervised firing-floor validation that fixes the letter-I bug), find per-sub-context detectors, and measure (i) the positive-only firing-Jaccard between detectors and the parent and (ii) the parent's per-sub-context recall holes.

\paragraph{The firing-Jaccard separates the regime extremes.} Spelling is firing-disjoint (Jaccard L $0.017$, O $0.039$, T $0.003$, I $0.008$, D $0.017$, all $<0.05$), and the label-free unit beats the best single latent there (e.g.\ I $+0.048$, CI $[0.012,0.095]$). Toxicity co-fires (Jaccard $\approx 0.69$), and a single specialist latent wins. A threshold $\tau^\ast=0.05$ on the firing-Jaccard reaches balanced accuracy $0.917$ on the 12 established concepts (mean absorption-regime Jaccard $0.062$ vs.\ mean co-firing $0.486$).

[FIGURE:fig4]

\paragraph{Honest boundary: Jaccard alone is insufficient.} Leave-one-concept-out accuracy is $0.733$, and the firing-Jaccard alone mislabels two informative cases: the \emph{numeric} concept has a high Jaccard ($0.285$) yet an absorption-like outcome, and the \emph{taxonomic} concept aggregated over all countries has a low Jaccard ($0.056$) yet a co-firing outcome, because its parent already has $\approx 0.95$ recall and therefore no holes to fill (the slice-level Georgia/Jordan homographs are the genuine absorbers). A recall-hole signal ($>0.777$) alone separates the established concepts perfectly (balanced accuracy $1.0$), and the combined rule---\emph{low firing-Jaccard AND high parent recall-hole}---is the honest decision procedure: grouping helps only when disjoint specialists \emph{and} parent recall holes co-occur. Prospectively, on three held-out concepts the router scores $0.333$ (sentiment correctly predicted co-firing; CEBaB food/service were predicted co-firing but showed small, significant absorption deltas of $+0.034$/$+0.071$, so the regime label missed). We report the prospective miss rather than tune it away: the router is a useful screening tool with a measured error rate, not an oracle.

\paragraph{Toxicity is the co-firing pole.} On ParaDetox/civil\_comments the general toxicity latent (12714, ``profanity/vulgar'') fires on $94.3\%$ of toxic content-flips (precision $0.996$), and on-target detectors exist for the label-disjoint sub-attributes (threat 11630, identity\_attack 11573, insult 13367) [ARTIFACT:art_-o2RPMOZp37A]. But they \emph{co-fire} with the general latent (toxic-only firing-Jaccard $0.403$, $0.292$, $0.655$---all far above $0.10$), departing sharply from label disjointness (label-Jaccard threat $0.044$). The set-cover K-track correctly adds zero absorbers; the C-track unit ties weak baselines (AUC $0.762$ vs.\ (a) $0.765$) and loses to attribution ((h) $0.837$; unit$-$(h) CI $[-0.093,-0.055]$, Holm $p\approx 5\times 10^{-71}$) and a residual probe ($0.859$), collapsing on the disjoint sub-attributes (threat $0.626$ vs.\ (h) $0.929$). This is the negative pole the router predicts from one forward pass: where firing co-fires, supervised attribution is the right tool, and CCRG should not be used.

# Results: Measured Auditability
\label{sec:audit}

Because the unit does not out-classify a strong dense probe, its distinctive value must be the auditable, editable structure a probe lacks. We replace the previous ``we emit a 70-edge graph'' assertion with two measured results [ARTIFACT:art_lvYKkaolutJG].

\paragraph{KG-guided recall repair.} For each under-served sub-context (a recall hole where the parent goes silent) the knowledge graph names a covering absorber; we add it to the anchor (max-pool) and measure recall recovery on held-out corpus windows (selection split disjoint from the evaluation split) against a control that adds the full population of other content-responsive latents, with a paired bootstrap ($B=10{,}000$). Eight repairs beat the random-addition control with a CI excluding 0 (Figure~\ref{fig:repair}): taxonomic Georgia (anchor recall $0.20 \to 1.00$, gain $0.80$, $99.4$th percentile vs.\ random, CI $[0.70,0.82]$), Jordan ($0.29\to 1.00$, gain $0.71$, CI $[0.61,0.77]$), United States ($0.77\to 0.99$, gain $0.22$, CI $[0.15,0.27]$), and first-letter O/``our'' and D/``day'' ($0.00\to 1.00$). Both the K-track edge and the higher-precision diagnostic-corroborated absorber are significant. Honest negatives: first-letter L and T candidate words \emph{tie} the random-addition control (too few held-out windows), reported verbatim.

[FIGURE:fig5]

\paragraph{A dense probe cannot localize the fix.} The label-free group-inference probe (k) (JTT: ERM $\to$ upweight the hardest set $\to$ retrain) yields a dense hyperplane whose decoder-projection argmax is the \emph{parent} (3792, top $|\cos|=0.44$, not dominant); the KG absorbers rank 1728/52/11015 by projection and are never the argmax. So (k) classifies the holes (recall $1.0$ on Georgia/Jordan/US) but exposes \emph{no} addable per-sub-context latent, whereas the KG names exactly one. The editable, single-latent repair is a capability the dense probe structurally lacks.

\paragraph{Members are human/LLM-auditable.} Describing each of 67 unit members by its logit-lens top-10 tokens and top-5 activating corpus windows with the sub-context label withheld, an independent LLM judge (claude-haiku-4.5, temperature 0, forced choice) names the sub-context with agreement $0.716$ versus a shuffle null of $0.090$ (analytic chance $0.087$); the gap is $0.627$, bootstrap CI $[0.522,0.731]$. Per role, absorbers are named at $0.758$ accuracy ($n=62$) while anchors are named at only $0.20$ ($n=5$)---the judge over-specifies the parent's mixed-context windows, an honest caveat. Total LLM spend was \$0.047.

# Results: Steering and Model-Diffing (Generality Demonstrations)
\label{sec:other}

\paragraph{Steering.} As a generality demonstration we steer with the unit's mean-member-decoder direction and compare, at matched on-target effect, the full-vocabulary KL divergence on unrelated prompts against a best-single-member (hub) direction and a non-SAE difference-of-means direction [ARTIFACT:art_0ueMMR8Tt02P]. On the primary letter L the unit is the most surgical (KL $16.4$ vs.\ hub $27.9$ and diff-of-means $30.4$ at matched shift) and likewise on D; on O, T, and I a non-SAE diff-of-means or the hub is more surgical. We report steering honestly as a demonstration, noting the unit's advantage tracks the letters where anchor fidelity holds.

\paragraph{Model-diffing (bounded).} The goal mandates a model-diffing task. No instruction-tuned Gemma Scope SAE exists for the 2B model, so we apply the shared frozen pretrained SAE to \texttt{gemma-2-2b} and \texttt{gemma-2-2b-it} activations and bound the resulting confound explicitly [ARTIFACT:art_jI2KIJotjzIU]. The shared SAE reconstructs IT activations almost as well as base (cosine $0.913$ vs.\ $0.925$), so the recipe is viable. A base-vs-IT shift is detectable above a model-label shuffle null for the toxicity unit (separability AUC $0.438$, departure $0.062$, $p<10^{-3}$), but it is \emph{not concept-specific}: the spelling control shows the same direction and an identical $0.062$ departure, so the control-subtracted genuine toxicity shift is $+0.000$ (CI $[-0.009,0.007]$), and a norm-matched estimate is a small $+0.027$ (CI $[0.021,0.033]$) but in the direction \emph{opposite} the naive detox prediction (IT uses the toxicity feature more, consistent with generic out-of-distribution norm drift; IT residual-stream norm is $1.11\times$ base). A within-model sanity check confirms the unit is a genuine toxicity detector (toxic-vs-neutral AUC $0.71$ base, $0.73$ IT). The co-response unit does \emph{not} detect the shift more reliably than the best single latent (abs-deviation difference CI $[-0.001,0.008]$, includes 0). We present this as an honest, infrastructure-bounded null---a valid deliverable with its confound made explicit---rather than as open-ended future work.

# Discussion
\label{sec:discussion}

\paragraph{What is established.} Executed on a frozen Gemma Scope SAE, CCRG produces auditable multi-member units whose classification advantage is attributable to the two-track \emph{selection}: the unit beats a random-eligible-$k$ pool of identical size and pooling on all five first-letter tasks (one-sided $p\le0.009$; pooled AUC $+0.237$, CI $[0.191,0.280]$) and a supervised attribution pool on three of five, with true AUC-difference CIs. Absorption generalizes to a taxonomic hierarchy where an independent diagnostic corroborates the recovered specialists and the selection survives an anchor-fixed control. These are SAE-\emph{selection} results; we do not claim to out-classify a strong dense probe, and say so where the probe wins.

\paragraph{A regime-scoped contribution with an a-priori test.} The most useful methodological lesson is that grouping helps in the absorption regime (mutually-exclusive parent/child firing with parent recall holes) and not in the co-firing/splitting regime, and that a one-forward-pass firing-Jaccard-plus-recall-hole measurement separates the two beforehand. This reframes the method from ``a universal repair'' to ``a repair for absorption, with a screening test of measured accuracy''---more defensible and more useful: a practitioner can run the cheap test and know whether to reach for set-cover grouping or for supervised attribution.

\paragraph{Honest failure modes.} (1) On true AUC the unit does not beat supervised attribution on L or O (only the random-eligible control is beaten there). (2) The recall-argmax anchor is not always the semantic parent (letter I); the parent-validation step is needed for unsupervised deployment. (3) E2 absorbed-slice recall is significant only on the best-powered slice T. (4) On numeric the set-cover selection is \emph{not} established (anchor-fixed control includes 0) and the diagnostic does not corroborate, so absorber status is unconfirmed. (5) On toxicity the regime is co-firing: CCRG ties weak baselines and loses to attribution. (6) The router's prospective accuracy is $0.333$ on three held-out concepts. (7) Model-diffing is a confound-bounded null, and no paired instruction-tuned SAE exists. (8) A non-SAE dense probe matches or beats the unit on classification across the non-spelling slices. Each is reported with its statistic rather than spun as future work.

\paragraph{Scope.} We scope the method to splitting and absorption; a hedged single polysemantic latent is not groupable \citep{Chanin2025}. bias\_in\_bios is a pre-registered boundary-null, not a method failure.

# Conclusion
\label{sec:conclusion}

We presented Two-Track Co-Response Grouping, a training-free method that organizes the latents of a frozen public SAE into reliable, auditable concept units by their interventional response to content counterfactuals---correlation communities for shared-support splitting and an anchored greedy set-cover for disjoint-support absorption that no pairwise-affinity clustering can propose. Against a random-eligible-$k$ control that isolates selection from pooling, the label-free unit beats the random pool on all five first-letter tasks and supervised attribution on three, with true AUC-difference confidence intervals; absorption generalizes to a taxonomic hierarchy where an independent diagnostic corroborates the recovered specialists and the selection survives an anchor-fixed control. A one-forward-pass firing-Jaccard-plus-recall-hole measurement is an a-priori router that predicts which regime a concept is in, and the emitted feature knowledge graph carries measured repair utility a dense probe lacks. We release four frozen testbeds, the single-GPU pipeline, and a complete account of where the method works and where it does not---a co-firing toxicity regime, an unconfirmed numeric hierarchy, two non-significant letters, and a null model-diffing result.

\paragraph{Future work.} Extend the firing-Jaccard-plus-recall-hole router into a per-concept routing rule that picks set-cover grouping versus attribution automatically; harden the parent-validation step; and revisit model-diffing if a paired instruction-tuned SAE becomes available.

\bibliographystyle{plainnat}
\bibliography{references}

</current_paper>

<reviewer_feedback>
Feedback from the paper reviewer this iteration.

- [MAJOR] (evidence) The lead non-spelling claim — a 'diagnostic-corroborated taxonomic hierarchy' — is internally inconsistent with its own artifact. In full_method_out.json (experiment_2), the K-track classification unit is [3792 (anchor), 4697 (Georgia), 9339 (Jordan), 8442 (US)], and these three absorbers have form-free-diagnostic KG-agreement_top1 of 0.0 (Georgia/4697), 0.955 (Jordan/9339), and 0.0 (US/8442) — so the reported 'KG-agreement top-1 0.318' is the 3-edge MEAN, driven entirely by Jordan. The paper places this 0.318 in the Georgia table row (Table tab:nonspelling) and states 'the diagnostic corroborates the recovered edges,' but the headline Georgia edge is specifically NOT corroborated. Worse, the selected absorbers fail the method's stated per-member precision floor (subctx_precision 0.350/0.633/0.347 in kg_edges, all <0.70) and are absent from the non_triviality_passing_absorbers set {16009, 540, 846, ...}, whose members ARE the high-precision (0.95-1.0), diagnostic-corroborated specialists (e.g., 16009 for Georgia). So the classification unit and the 'corroborated specialists' are two DIFFERENT latent sets, and the paper conflates them. The one corroborated edge (Jordan) is on a descriptive slice (n=124<150, eligible=False).
  Action: Make the classifier and the corroborated specialists the SAME unit: rebuild the taxonomic unit from the diagnostic-corroborated, precision-passing absorbers (16009 Georgia, 846 US, etc.) and report that unit's Georgia AUC and RE-k-anchored selection result (likely stronger, since 16009 has precision 0.955 vs 4697's 0.35). In the table, replace the single '0.318' with per-edge agreement (Georgia 0.0, Jordan 0.955, US 0.0) and state explicitly that diagnostic corroboration currently holds only for the descriptive Jordan edge. If the greedy genuinely prefers high-coverage/low-precision absorbers over high-precision diagnostic-corroborated ones, discuss this as a limitation of the max-coverage objective. This is the single highest-impact fix; it removes a headline overstatement that a careful reviewer will catch.
- [MAJOR] (scope) Demonstrated significance is narrow relative to the goal, which requires beating a non-SAE baseline on concrete downstream tasks. After all fixes: (1) the unit out-classifies NO non-SAE dense probe on any task (explicitly conceded: Georgia 0.989 vs dense 1.000; numeric integer 0.687 vs dense 1.000; toxicity loses to a residual probe); (2) toxicity — the only safety-relevant family and central to the goal — is a clean negative (unit ties weak baselines, loses to attribution, collapses on disjoint sub-attributes); (3) the taxonomic 'generalization' is carried by exactly two homograph countries (Georgia, Jordan are the only slices with parent recall holes), so it is a homonym phenomenon rather than broad taxonomic absorption; (4) numeric selection is not established; (5) model-diffing is a confound-bounded null; (6) steering wins on 2/5 letters. The affirmative contribution thus reduces to a within-SAE-ecosystem selection win on 3/5 first-letter tasks plus the auditability/KG-repair result.
  Action: Concentrate the contribution on the one place a unique capability is demonstrated and beats a control on a dimension the dense probe lacks: the measured KG-guided recall repair and member-labeling. Expand that experiment (more concepts/sub-contexts; ideally a downstream task where the editable localized fix matters) and make it the headline. Reframe the paper as 'auditable absorption-regime repair + an a-priori router for when to use it,' explicitly scoping away from a general classification-improvement claim. Characterize precisely WHEN non-spelling absorption occurs (homograph/polysemous tokens whose general latent is suppressed) instead of claiming broad taxonomic generalization.
- [MAJOR] (rigor) The primary-endpoint verdict aggregates two separately-satisfied conditions in a way that masks a weaker per-letter reality. E1 (absorption mechanism: parent + >=2 absorbers above null) holds on {L,O,T,D}, and the joint selection test (unit AUC significantly > BOTH (h) and RE-k) holds on {T,I,D}. Their per-letter INTERSECTION — i.e., letters where the absorption mechanism AND the selection win co-occur — is only {T,D} = 2/5, below the stated 3/5 majority. The third selection letter, I, is precisely the one where E1 FAILS (the recall-argmax anchor fires 0% on corpus), so 'ABSORPTION_REPAIR_SELECTION_CONFIRMED' is partly carried by a letter where the absorption repair does not actually occur (it is a pooling-classifies-well result). The paper is transparent about each component separately, but the single emitted verdict and the abstract/conclusion phrasing imply a stronger joint result than the data support.
  Action: Report the per-letter joint (E1 AND selection) = 2/5 (T, D) explicitly alongside the marginal counts, and either (a) tighten the verdict to require both conditions per letter (and re-state the headline accordingly), or (b) keep the marginal framing but rename the verdict so it does not imply mechanism+selection co-occur on 3 letters, and annotate I as 'selection win without confirmed absorption mechanism.' Reconcile the emitted verdict string with whichever you choose.
- [MINOR] (evidence) The a-priori router's prospective validation is overstated. The contribution bullet and abstract say it is 'validated prospectively across spelling, taxonomic, toxicity, sentiment, and aspect concepts,' but the first three categories are the 12 concepts used to DERIVE the rule; only 3 concepts (sentiment, food, service) were truly held out, and the router hit 1/3 (prospective accuracy 0.333, LOO accuracy 0.733). Moreover the headline single signal (firing-Jaccard, balanced acc 0.917) is weaker than the recall-hole signal alone (balanced acc 1.0) on the derivation set, so leading with 'firing-Jaccard router' slightly misranks the actual best separator.
  Action: State clearly that the rule was derived on spelling/taxonomic/toxicity and prospectively tested on 3 concepts with 1/3 hits and LOO 0.733; present the combined (low firing-Jaccard AND high recall-hole) rule as the actual recommendation with its measured error rate, and describe it as a 'screening heuristic with substantial measured error,' not a validated oracle. Avoid listing derivation concepts as if they were prospective.
- [MINOR] (methodology) The RE-k control, while the right addition, is a comparatively easy bar and does not isolate the two-track set-cover from any reasonable label-free selection. RE-k max-pools k random eligible latents, which predictably underperforms because random latents inject spurious activations into the max-pool; its AUC (~0.63-0.69) is at or below the best single latent (a) on every letter. So 'unit beats RE-k' largely restates 'good selection beats random/best-single,' which the (a) baseline already shows. The informative comparisons remain unit vs (a) (a tie on L) and unit vs supervised (h) (3/5). The claim 'the two-track set-cover SELECTION is what helps' is not isolated from simpler label-free selections (e.g., top-k by content-flip recall, by firing precision, or by response magnitude).
  Action: Add one or two label-free, non-random selection controls count-matched to k (top-k by content-flip recall; top-k by firing precision; top-k by mean response magnitude). If the two-track set-cover unit significantly beats these, the set-cover-specific contribution is established; if not, scope the claim to 'cover-based eligibility + sensible selection' rather than the set-cover algorithm specifically.
- [MINOR] (rigor) The reported units do not visibly honor the method's stated precision floors, and the fold on which gates are applied is ambiguous. The method specifies per-member precision >=0.7 and subctx_precision >=0.7, but the taxonomic K-track unit's members (kg_edges) have subctx_precision 0.350/0.633/0.347, and none appear in non_triviality_passing_absorbers. This suggests either the gates are applied on a train fold and the members generalize poorly (precision collapses to ~0.35 on eval) or the unit-forming path and the validation path use inconsistent criteria. Either way the 'precise specialist' characterization is undercut for the headline unit.
  Action: State explicitly which fold each gate (precision, jaccard, gain-CI) is evaluated on, and report each admitted member's HELD-OUT subctx_precision in the unit table. If train->eval precision collapses (0.7->0.35), report it as a generalization caveat; if the greedy and validation paths diverge, reconcile them so the reported unit's members satisfy the stated floors (this dovetails with critique 1's fix).
- [MINOR] (rigor) The first-letter 'human-auditable unit' is a 15-wide max-pool (config max_k=15) of which only ~4-5 members are the named anchor+absorbers; the remaining ~10 are uncharacterized eligible latents. This is in mild tension with the auditability framing and means the strong C1 AUC reflects a wide pool, not the compact named structure. (The RE-k control addresses 'is it just pooling,' but the auditability/interpretability of the 15-member object is not the same as the 4-5 named ones.)
  Action: Either report a compact (named-members-only) unit's C1 AUC alongside the 15-wide one to show the named structure carries the signal, or describe the unit consistently as a 15-latent pool and restrict the 'auditable' claim to the characterized subset. Tie this to the member-labeling result (which already labels members) by reporting what fraction of the 15 members receive a confident, non-shuffle label.
- [MINOR] (presentation) The manuscript is written as a rebuttal to a prior review rather than as a standalone paper, with pervasive references to 'the previous draft/iteration,' 'a previous reviewer correctly flagged,' 'the earlier code computed an unqualified WORKS,' 'iter-3 re-runs use torch 2.8+cu128 for Blackwell-class GPUs,' and verdict-reconciliation notes. This is inappropriate for a submission and dilutes the contribution.
  Action: Strip all iteration/rebuttal/process scaffolding and infrastructure asides; present the method, endpoint, and results once, cleanly. Move any reproducibility notes (torch/GPU versions, AUC drift) to an appendix. Audit all 2025/2026-dated citations for venue/version accuracy while doing this pass (e.g., ensure Chanin 'A is for Absorption' is cited to NeurIPS 2025).
</reviewer_feedback>



<task>
IMPORTANT: Your ONLY output is the revised hypothesis text. Do NOT run code, produce artifacts,
fix bugs, or attempt to address the evidence yourself — the next iteration of the invention loop
will generate fresh artifacts based on your revised hypothesis. Reflect and rewrite; nothing else.

Do NOT generate a completely new hypothesis. Take the current hypothesis and REVISE it
to incorporate new evidence. Keep the core idea — refine, narrow, or strengthen it.

1. Does the evidence support the hypothesis? Narrow or broaden scope as needed.
2. Which claims now have strong evidence? Which are still unsupported?
3. Should the hypothesis become more specific based on what we've learned?
4. If reviewer feedback is provided, address the critiques directly.

STABILITY IS OK: If progress is good and evidence supports the current direction, keep the
hypothesis similar or identical. Only make substantive changes when evidence clearly calls for
them — e.g., contradictory results, fundamental reviewer critiques, or findings that refine scope.

You must also classify two kinds of edges in the research trace:

(A) The H↔H edge — how does this revised hypothesis relate to the previous one?
    Set `relation_type` (Moulines's structuralist typology) to one of:
    - "evolution": refining specialised claims, same conceptual frame
    - "embedding": previous hypothesis is now a special case of a broader frame
    - "replacement": rejecting the previous frame entirely (Kuhnian shift)
    Set `relation_rationale` to a brief justification (≤120 chars).

(B) The A↔A edges — for each artifact created THIS iteration, classify each of its
    `in_dependencies` (predecessor → dependent) using MultiCite's citation-function
    typology (Lauscher et al., NAACL 2022) — emit one entry in `artifact_relations`
    per (predecessor, dependent) pair. Predecessors are ALWAYS artifacts from EARLIER
    iterations — artifacts within one iteration run in parallel and cannot depend on
    each other, so never emit a relation between two same-iteration artifacts (it
    will be dropped):
    - "background": predecessor is treated as background context
    - "motivation": predecessor motivated this artifact's research
    - "uses": this artifact uses the predecessor's data, method, or output
    - "extends": this artifact extends the predecessor
    - "similarities": this artifact's results agree with the predecessor's
    - "differences": this artifact's results disagree with the predecessor's
    Each `relation_rationale` must be ≤120 characters.

Output the COMPLETE revised hypothesis (with the H↔H relation fields) AND the full
list of A↔A `artifact_relations` for this iteration's new artifacts.
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
    "ArtifactRelation": {
      "description": "One typed A\u2194A edge between a dependent artifact and one of its in_dependencies.\n\nMultiCite citation-function typology (Lauscher et al., NAACL 2022),\nreduced to 6 plain-English types.",
      "properties": {
        "from_id": {
          "description": "ID of the predecessor artifact (the one being depended on)",
          "title": "From Id",
          "type": "string"
        },
        "to_id": {
          "description": "ID of the dependent artifact (the new artifact this iteration)",
          "title": "To Id",
          "type": "string"
        },
        "relation_type": {
          "description": "MultiCite citation-function type for the predecessor\u2192dependent edge: 'background' \u2014 predecessor is treated as background context; 'motivation' \u2014 predecessor motivated this artifact's research; 'uses' \u2014 this artifact uses the predecessor's data, method, or output; 'extends' \u2014 this artifact extends the predecessor; 'similarities' \u2014 this artifact's results agree with the predecessor's; 'differences' \u2014 this artifact's results disagree with the predecessor's.",
          "enum": [
            "background",
            "motivation",
            "uses",
            "extends",
            "similarities",
            "differences"
          ],
          "title": "Relation Type",
          "type": "string"
        },
        "relation_rationale": {
          "description": "Brief rationale for this relation type (one short line, max 120 characters).",
          "maxLength": 120,
          "title": "Relation Rationale",
          "type": "string"
        }
      },
      "required": [
        "from_id",
        "to_id",
        "relation_type",
        "relation_rationale"
      ],
      "title": "ArtifactRelation",
      "type": "object"
    }
  },
  "description": "Revised hypothesis after reviewing iteration results.\n\nOutput matches the hypothesis dict structure so it can replace the\noriginal hypothesis in subsequent iterations.",
  "properties": {
    "title": {
      "description": "Revised hypothesis title (may be unchanged if still accurate)",
      "title": "Title",
      "type": "string"
    },
    "hypothesis": {
      "description": "Revised hypothesis statement \u2014 what we now believe based on evidence",
      "title": "Hypothesis",
      "type": "string"
    },
    "relation_rationale": {
      "description": "Brief rationale for the H\u2194H revision type (one short line, max 120 characters).",
      "maxLength": 120,
      "title": "Relation Rationale",
      "type": "string"
    },
    "confidence_delta": {
      "description": "How confidence changed: 'increased', 'decreased', or 'unchanged'",
      "title": "Confidence Delta",
      "type": "string"
    },
    "key_changes": {
      "description": "Bullet list of specific changes made to the hypothesis",
      "items": {
        "type": "string"
      },
      "title": "Key Changes",
      "type": "array"
    },
    "relation_type": {
      "description": "Moulines's structuralist typology of this hypothesis revision: 'evolution' \u2014 refining specialised claims while keeping the same conceptual frame; 'embedding' \u2014 the previous hypothesis is now a special case of a broader frame; 'replacement' \u2014 rejecting the previous frame entirely (incommensurable, Kuhnian revolution).",
      "enum": [
        "evolution",
        "embedding",
        "replacement"
      ],
      "title": "Relation Type",
      "type": "string"
    },
    "artifact_relations": {
      "description": "Typed A\u2194A edges for this iteration's new artifacts. Emit one entry per (predecessor \u2192 dependent) edge for every in_dependency on each artifact produced this iteration.",
      "items": {
        "$ref": "#/$defs/ArtifactRelation"
      },
      "title": "Artifact Relations",
      "type": "array"
    }
  },
  "required": [
    "title",
    "hypothesis",
    "relation_rationale",
    "confidence_delta",
    "key_changes",
    "relation_type"
  ],
  "title": "RevisedHypothesis",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-06-17 21:32:19 UTC

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
