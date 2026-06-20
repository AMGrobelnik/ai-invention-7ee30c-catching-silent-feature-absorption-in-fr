# upd_hypo — test_idea

> Phase: `invention_loop` · round 2 · Substep: `upd_hypo`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave the agent(s) in this substep — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `upd_hypo` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-17 17:58:07 UTC

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
  Training-Free, Auditable Concept Units that Recover the Absorbers Marginal-Attribution Selection Drops on First-Letter Spelling
  (and, where present, a Non-Spelling Hierarchy), and Beat Raw Latents, Count-Matched Observational Clusters, and Count-Matched
  Oracle Pools
hypothesis: |-
  ITERATION-1 STATUS AND THE SINGLE MANDATE FOR ITERATION 2 (EXECUTE THE CORE). Iteration 1 was a foundation iteration: it produced and validated EVERYTHING the SAE-grouping run needs but ran NO SAE. Delivered: two verified dossiers (art_RidEJtBC7gPT pins the SAE pipeline -- defensive from_pretrained, JumpReLU firing=encode>0, hook blocks.12.hook_resid_post, gemma-scope-2b-pt-res-canonical layer_12/width_16k -- the C-track leidenalg + K-track greedy max-coverage, all 11 baselines (a)-(k), AxBench steering, the shared-pt-SAE model-diffing recipe, and a verified 30+ citation table; art_I2MrezW41iQo verifies the Chanin 2409.14507 absorption diagnostic against sae-spelling and the non-circular FORM-FREE probe-projection variant, and pins all datasets) and four FROZEN, schema-validated testbeds (first-letter L/O/T/I/D, 17,180 ex, 0 deterministic violations; non-spelling numeric+taxonomic, 24,128 ex; toxicity ParaDetox+civil_comments, 37,707 ex; supporting sentiment/aspect/bias_in_bios, 30,739 ex). The paper therefore reports ZERO unit-vs-baseline numbers -- every Table-3 row is a PREDICTION -- and the reviewer's decisive verdict is that this reads as an incomplete submission whose own thesis (units > latents > observational clusters > oracle pools) has no supporting evidence. THE REVISION'S CENTRAL MOVE: the load-bearing core is NO LONGER a pre-registration; it is the immediate, mandatory deliverable of iteration 2. A SINGLE fully-executed positive testbed -- first-letter spelling, the documented guaranteed-signal regime -- transforms the paper's standing. Iteration 2 STOPS building infrastructure and RUNS the pipeline; nothing else is load-bearing until real numbers exist.

  ONE-SENTENCE HEADLINE (load-bearing, C1+C3; conceptually UNCHANGED): clustering frozen SAE latents by their INTERVENTIONAL co-response to content counterfactuals -- via a concretely specified TWO-TRACK algorithm (positive content-response CORRELATION for the splitting regime; an ANCHORED GREEDY SET-COVER for the absorption regime, because mutually-exclusive disjoint-support absorbers have LOW pairwise correlation and cannot be proposed by any affinity-merging clustering) -- yields training-free, human-auditable, multi-member concept units that (C1) beat the best raw single latent AND COUNT-MATCHED observational co-activation/decoder-geometry clusters on safety-attribute classification, and (C3, the spine) recover the absorber latents a count-matched marginal-attribution selection silently drops, with knowledge-graph specialization edges that agree with the absorption diagnostic (Chanin 2409.14507, NeurIPS 2025 Oral) used ONLY to score edges, never to form units (non-circular).

  PRIMARY FALSIFICATION ENDPOINT (NEW -- resolves the 'protocol that cannot lose' critique). The method is judged to WORK if and only if, on FIRST-LETTER SPELLING (the regime where absorption is guaranteed to exist), BOTH hold: (E1) the K-track proposal step, given ONLY content-flip pairs (NOT the Chanin diagnostic), recovers the diagnostic-identified parent latent plus >=2 per-token absorbers (e.g. lion/London) with membership F1 above a random-membership null; AND (E2) the resulting co-response unit BEATS the count-matched oracle pool (g) and count-and-pool-matched probe (h) AND the count-matched observational clusters (b)/(c) on absorber-recovery count and sliced recall over the differing sub-contexts, with a paired-bootstrap CI excluding 0. If EITHER fails on first-letter -- the lowest-risk testbed -- the method DOES NOT WORK, and that is the reportable negative; the honest-null branches below are SECONDARY characterizations of HOW it works when it does, not co-equal successes. This is the one outcome the paper stakes itself on.

  THE LOAD-BEARING CORE, REFRAMED AS THE ITER-2 EXECUTION LIST (run, do not pre-register):
    (RUN-0, Tier-0 pilot, first-letter, GUARANTEED-SIGNAL) Encode the first-letter content-flip pairs through Gemma Scope L12/16k; run K-track STEP-3 set-cover; report (a) anchor-FIDELITY -- does the recall-argmax anchor coincide with the diagnostic-identified parent? (b) recovered membership precision/recall vs the diagnostic above the random-membership null; (c) a THRESHOLD SENSITIVITY SWEEP over mutual-exclusivity Jaccard, per-member precision, and coverage-gain floors, to show the recovery is not knife-edge on hand-set constants. This is E1.
    (RUN-1, C1 classification) unit vs best raw latent (a), vs COUNT-MATCHED observational clusters (b)/(c), and vs count-and-pool-matched (h), on first-letter AND the best-powered toxicity sub-attributes; per-family paired-bootstrap CIs.
    (RUN-2, C3 absorber-recovery) on first-letter: recovered-absorber count and sliced recall vs (g)/(h); KG specialization-edge agreement with the diagnostic. This is E2.
    (RUN-3, SAE-LATENT FIRING REGIME MEASUREMENT -- see next block) the cheap forward pass that grounds the regime-separation claim.
    (RUN-4, REQUIRED steering demo) the first-letter steering result (see steering block).
  HARD CHECKPOINT: if E1 and E2 clear on first-letter, the paper has a real positive anchor and proceeds to toxicity + the non-spelling testbed + supporting results; if not, write up the executed negative.

  SAE-LATENT FIRING REGIME MEASUREMENT (NEW -- resolves the MAJOR critique that the standalone finding was measured on LABELS, not latents). The iteration-1 'both regimes occur in safety data' finding rests on civil_comments sub-attribute LABEL co-occurrence (insult-obscene Jaccard 0.245 shared-support; threat 0.044 disjoint). The reviewer is correct that label co-occurrence is NOT latent co-firing -- a single general toxicity latent can fire across all sub-attributes regardless of label disjointness, so the label-Jaccard does NOT establish that any pairwise operator fails on real SAE latents. The regime claim is therefore DEMOTED from a headline standalone finding to a motivating proxy, and iteration 2 MUST replace it with the real measurement (a single forward pass over data already built): encode the toxicity examples through Gemma Scope L12/16k, identify the top per-sub-attribute detector latents and the candidate general/parent toxicity latent, and report (i) the actual SAE-LATENT firing-Jaccard among those detectors, and (ii) the parent latent's RECALL HOLES per sub-context. The K-track's necessity is established ONLY if disjoint sub-attributes (threat, identity_attack) are carried by latents that are mutually exclusive in firing with the general latent. If SAE-latent disjointness does NOT mirror label disjointness, that is itself an important finding and reshapes the K-track motivation (reported honestly, not buried). The same firing-Jaccard measurement is the first quantitative step of RUN-0/RUN-2 on first-letter.

  DOWNSTREAM TASKS THE GOAL MANDATES -- NO LONGER DEFERRED (resolves the MAJOR scope critique). (1) STEERING is now a REQUIRED iter-2 deliverable, not future work: on first-letter (the most de-risked concept), steer with the unit's MEAN-MEMBER-DECODER direction and show it moves 'starts-with-L' output mass at MATCHED on-target effect with LOWER collateral than (i) a non-SAE difference-of-means direction and (ii) a hub/best-single-latent-alone control, measured by full-vocab KL on unrelated prompts AND perplexity, with doc-bootstrap CIs and a shuffle null. (2) MODEL-DIFFING is bounded honestly: because NO instruction-tuned Gemma Scope 2B SAE exists (verified: Google IT residual SAEs only for 9B), diffing applies the SHARED frozen pt-SAE to gemma-2-2b vs gemma-2-2b-it activations -- a CONFOUNDED setup. Iteration 2 either presents one small concrete diffing result with the shared-SAE confound explicitly bounded (does the unit detect a base-vs-it concept-usage shift more reliably than the best single latent, above a shuffle null?), or moves model-diffing out of the contribution claims and into an explicit LIMITATION -- NOT into open-ended future work.

  THE TWO-TRACK CLUSTERING ALGORITHM -- THE NAMED CONTRIBUTION (specification retained; anchor validation strengthened). Input: a frozen SAE and, per concept, content-flip minimal pairs (x_off,x_on) plus surface-flip pairs; the concept labels are the SAME supervision every matched baseline (d)-(h) consumes (no absorption oracle). STEP 1 -- per-latent content-response r_l(p)=a_l(x_on)-a_l(x_off); keep CONTENT-RESPONSIVE latents (mean r_l above the 95th-pct shuffled-pair null); cover set C_l = pairs with r_l>tau_resp AND a_l fires on x_on AND content-response precision >=0.7. STEP 2 -- C-TRACK (splitting; shared support, symmetric affinity APPROPRIATE): A_C[l,l'] = positive Spearman correlation of content-response profiles (DiffCoEx-style soft-threshold, beta=6 per WGCNA scale-free criterion); Leiden communities; count fixed by modularity + bootstrap-ARI stability vs the shuffled-pair null. STEP 3 -- K-TRACK (absorption; ANCHORED GREEDY MAX-COVERAGE, NOT pairwise affinity): (i) ANCHOR = argmax_l |C_l| using ONLY P (NOT the diagnostic; tie-break broadest, lowest-entropy support) -- and, per the methodology critique, iteration 2 VALIDATES the 'anchor=parent' identification by reporting whether the recall-argmax anchor coincides with the diagnostic parent and by checking that a high-frequency/polysemantic latent has not usurped the anchor; (ii) HOLES H = P\C_anchor; (iii) GREEDY: while H non-empty and improving, add l*=argmax_l |C_l intersect H| subject to mutual exclusivity (firing Jaccard<0.1), precision>=0.7, marginal coverage gain>=0.05 with bootstrap CI excluding 0; H<-H\C_l*. STEP 4 -- RECONCILE: anchor each C-community's highest-recall member and K-augment with mutually-exclusive absorbers covering its holes; seed K from standalone high-recall latents; de-duplicate to highest-coverage-gain unit. STEP 5 -- ADMISSION FILTER: admit iff signature C (within-unit content-response correlation > 95th-pct shuffled-pair null) OR signature K (pooled-max minus best-single content-response AUC > 95th-pct of a best-of-random-k null MATCHED on marginal AUC, PLUS the k in {2,3} absolute >=0.05 gain with CI excluding 0, PLUS Jaccard<0.1 and per-member precision>=0.7), AND unit-level surface invariance (pooled surface-response not above the shuffled-surface null).

  MULTIPLICITY AT THE UNIT-PROPOSAL LEVEL (NEW -- resolves the rigor critique). The admission filter tests MANY candidate units per concept against 95th-pct nulls with a disjunctive (C OR K) rule plus a surface AND-gate; per-unit thresholds do NOT compose to a per-concept <=0.05 false-admit guarantee. Iteration 2 SPECIFIES and APPLIES a multiplicity correction at the unit-proposal level (Benjamini-Hochberg or Holm over the M candidate-unit admission tests within each concept), reports M, and reports the EMPIRICAL family-wise false-admit rate from the matched random-k null on the real run -- SEPARATE from the across-claims Holm-Bonferroni used for the headline comparisons.

  SURFACE-INVARIANCE CONTROL STRENGTHENED (NEW -- resolves the control-circularity critique). Surface-invariance is the load-bearing AND-gate of Step 5, yet iter-1 surface-flip sets are small (546 toxicity, 590 first-letter) and the toxicity surface pairs were both GENERATED and JUDGED by gpt-4o-mini (70.6% pass) -- a mild same-model circularity in a control that gates every admitted unit. Iteration 2: (a) ENLARGE the surface-pair sets for the concepts where surface-invariance is actually exercised; (b) RE-JUDGE a sample with an INDEPENDENT model from a different family (or a small human audit) to confirm the pass set is genuinely meaning-preserving; (c) REPORT the surface-response null distribution SIZE used per concept.

  BASELINE GLOSSARY (one line each): (a) best raw single latent; (b) observational co-activation clusters, COUNT-MATCHED to the unit's k for C1; (c) decoder-geometry clusters, COUNT-MATCHED; (d) counterfactually-matched diff-of-means; (e) counterfactually-matched probe; (f) surface-invariant matched probe = (d)/(e) with surface direction LEACE-erased (the conceded single dense hyperplane); (g) supervised oracle pool = top-N SAE latents by SCR/TPP attribution; (h) count-and-pool-matched probe = max-pool over EXACTLY k SCR/TPP-selected raw directions; (i) unmatched diff-of-means/probe; (j) oracle group-DRO probe (true sub-context labels) = robustness UPPER BOUND; (k) label-free group-inference probe (JTT/GEORGE-style). C1 LOAD-BEARING half = unit beats COUNT-MATCHED (b)/(c) (beating single latent (a) is a near-foregone capacity win, completeness only). SELECTION-CRITERION ISOLATION = unit vs (g)/(h) at FIXED pool size, varying only HOW members are chosen (co-response set-cover vs marginal attribution); beating (f) is conceded as pooling.

  THE NON-SPELLING TESTBED (C3 generality, SECONDARY to executing first-letter). Numeric-quantity hierarchy primary (general numeric-token latent with year/percent/currency/date absorbers), taxonomic 'is-a-country' alternative; scored by the FORM-FREE probe-plus-ablation diagnostic. Because absorption is documented almost ONLY on first-letter (verified across the original work, SAEBench's sole 'absorption_first_letter' eval, and the Matryoshka/H-SAE mitigations), Testbed-2 is ALSO a novel empirical test of whether absorption generalizes. NON-TRIVIALITY GATE (parent recall>=0.60; >=1 absorber with firing-Jaccard<0.10, precision>=0.70, hole-coverage gain>=0.05 CI-excluding-0). HONEST-NULL FALLBACK: if the non-spelling parent has no specialist-filled holes, report 'absorption is spelling-specific', scope the C3 title claim to spelling-type hierarchical absorption, and route cross-concept generality through C1. This is a SECONDARY characterization, executed only after first-letter E1/E2 land.

  SUPPORTING RESULTS (strengthen the paper; honest nulls here do not sink it). (S1) SELECTION-CRITERION ORDERING on toxicity worst-sub-context recall: pre-registered (f) < (g)/(h) < unit, with the unit-minus-(g)/(h) PAIRED gap (B=10000) GROWING in measured sub-population reweighting magnitude (slope CI primary). (S2) ROBUSTNESS BOUNDS: unit APPROACHES the oracle group-DRO probe (j) without labels and is competitive-or-better than the label-free probe (k) while uniquely auditable. (S3) MEASURED AUDITABILITY REPAIR LOOP: pick an under-served sub-context (recall hole on the dense probe (f) ALONE), read the KG to find the covering absorber, ADD it, MEASURE recall recovery (bootstrap CI) vs a RANDOM-content-responsive-latent-addition control, confirm (k) exposes no per-sub-context member to add; PLUS LLM-judge member-labeling agreement vs a shuffled-label null. DEGENERATE-CONSTRUCTION GUARD: sub-contexts from INDEPENDENT labels frozen first (civil_comments sub-attribute floats, CEBaB aspect levels), 'under-served' on (f) alone, non-triviality check that (f) genuinely collapses.

  NOVELTY DELTAS (resolves the novelty critique). Update Chanin 'A is for Absorption' to NeurIPS 2025 Oral (not just arXiv:2409.14507 2024) and audit all 2026-dated cites for venue/version. State EXPLICITLY (not in one hedged line): vs [13] Domain-Filtered Knowledge Graphs from SAE Features (2604.23829) -- their edges are OBSERVATIONAL (co-occurrence, decoder geometry, contrastive corpus filtering) over single latents; ours are INTERVENTIONAL specialization edges (absorbed/split child of an anchor) over MULTI-MEMBER co-response units, with measured repair utility. Vs [14] Subspace-Aware SAEs (2606.06333) and the Matryoshka/H-SAE/concept-bottleneck family -- they RETRAIN the dictionary to reduce absorption at training time; we are training-free POST-HOC over a frozen public SAE. Vs CDLC (2505.07073) -- they cluster continuous diffusion-counterfactual difference vectors into one direction per class in vision; we cluster DISCRETE LLM SAE latents into multi-member units with a SET-COVER track CDLC has no analogue for.

  HONEST NEGATIVES (now SUBORDINATE to the primary endpoint, reported as characterizations of failure modes, NOT as guaranteed wins): the K-proposal set-cover fails to recover the worked first-letter unit at the pilot (=primary-endpoint failure E1, method does not work); SAE-latent firing-Jaccard does NOT mirror label disjointness (reshape K-track motivation); the unit ties (g)/(h) on first-letter sliced recall (=primary-endpoint failure E2); observational co-response equals interventional co-response (no gain from intervention); the non-spelling parent has no specialist-filled holes (absorption spelling-specific -> scope C3); the unit ties (g)/(h) on toxicity (robustness is pooling -> contribution reduces to absorber-recovery + measured auditability); (k) beats the unit on recall (loss-reweighting wins for pure robustness); (f) matches the unit on sliced recall (invariance suffices, grouping adds only auditability); the KG-guided repair does not beat random-addition (auditability buys no measurable fix); steering shows no lower-collateral advantage (the steering application does not hold). bias_in_bios is a pre-registered boundary-null, not method failure.

  MOTIVATION (unchanged in substance). Single SAE latents are unreliable: feature absorption (a child latent suppresses a more general parent's firing; Chanin 2409.14507 NeurIPS 2025 Oral, 2505.11756), splitting, hedging, and 'SAEs Do Not Find Canonical Units' (ICLR 2025) converge on no single latent reliably tracking a concept; AxBench (ICML 2025) and DeepMind's negative report show plain diff-of-means beats raw-latent SAE methods, so any SAE-grouping method must clear strong simple baselines. Absorption is exactly the regime where OBSERVATIONAL signals break by construction (parent and absorbing child are mutually exclusive in firing) and where MARGINAL-ATTRIBUTION selection (SCR/TPP) silently drops the absorber (low marginal attribution because it fires only in a narrow sub-context). The two-track design follows: correlation-community detection for shared-support splitting (DiffCoEx/WGCNA transfer) and anchored greedy set-cover for disjoint-support absorption (Nemhauser-Wolsey-Fisher / Feige (1-1/e) transfer). The anchor is chosen WITHOUT the diagnostic, so 'unsupervised unit beats supervised oracle' holds and KG-edge validation is non-circular. Training-free post-hoc repair of FROZEN public SAEs is exactly what practitioners holding Gemma Scope have; architectural remedies retrain and are orthogonal.

  SUCCESS CRITERIA. METHOD WORKS iff the PRIMARY ENDPOINT clears on first-letter (E1 K-proposal recovers parent + >=2 absorbers above the random-membership null AND E2 unit beats count-matched (g)/(h)/(b)/(c) on absorber-recovery/sliced recall, paired-bootstrap CI excluding 0), AND the REQUIRED first-letter steering demo shows matched-on-target effect at lower collateral than diff-of-means and hub-alone. SUPPORTING (strengthen, do not gate): C1 on toxicity; S1 selection ordering; S2 robustness bounds; S3 measured auditability; the SAE-latent firing-Jaccard regime measurement; the non-spelling C3 generality (gated by non-triviality); admission false-admit <=0.05 under both nulls with the unit-proposal multiplicity correction; cluster-stability ARI/Jaccard above null. A clean primary-endpoint NEGATIVE on first-letter is the declared method-failure outcome and is itself a reportable finding; the other honest negatives are secondary characterizations.
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
  Same two-track frame; pivots iter2 to executing the core and grounds the regime claim in SAE-latent firing.
_confidence_delta: unchanged
_key_changes:
- >-
  Reframed the load-bearing core from 'pre-registered prediction' to the MANDATORY iteration-2 execution deliverable (the
  #1 reviewer demand: run the SAE pipeline). First-letter spelling designated the guaranteed-signal anchor to execute first.
- >-
  Added a single PRIMARY FALSIFICATION ENDPOINT on first-letter (E1: K-track recovers parent + >=2 absorbers above a random-membership
  null; E2: unit beats count-matched (g)/(h)/(b)/(c) on absorber-recovery/sliced recall, CI excluding 0) whose negative =
  method failure; demoted the honest-null branches to secondary characterizations (resolves the 'protocol that cannot lose'
  critique).
- >-
  Replaced the label-co-occurrence 'both regimes occur' standalone finding with a REQUIRED SAE-latent firing-Jaccard + parent-recall-hole
  measurement on Gemma Scope; the K-track necessity claim must be grounded in latent firing, not labels (resolves the major
  proxy critique).
- >-
  Elevated the first-letter STEERING demo (mean-member-decoder direction, matched on-target effect, full-vocab KL + PPL collateral
  vs diff-of-means and hub-alone) to a required deliverable; bounded MODEL-DIFFING as an explicitly-caveated shared-pt-SAE
  result or a limitation, removed from open-ended future work (resolves the major scope critique).
- >-
  Added anchor-FIDELITY validation (recall-argmax anchor vs diagnostic parent) and a threshold sensitivity sweep (Jaccard/precision/coverage-gain)
  to the Tier-0 pilot (resolves the anchor=parent methodology minor).
- >-
  Specified unit-proposal-level multiplicity correction (BH/Holm over candidate-unit admission tests per concept, report M
  and empirical false-admit rate from the real run), separate from across-claims Holm-Bonferroni (resolves the rigor minor).
- >-
  Strengthened the surface-invariance control: enlarge surface-pair sets, re-judge a sample with an independent model, report
  per-concept surface-response null sizes (resolves the same-model generate-and-judge circularity minor).
- >-
  Sharpened novelty deltas vs [13] domain-filtered KG (interventional specialization edges over multi-member units vs co-occurrence/geometry)
  and [14] subspace-aware SAEs (post-hoc vs retraining); updated Chanin absorption to NeurIPS 2025 Oral and flagged a 2026-citation
  venue audit.
- >-
  Scoped the non-spelling testbed as secondary to first-letter execution (run only after E1/E2 land), keeping its non-triviality
  gate and spelling-specific honest-null fallback.
- >-
  Confidence unchanged: the conceptual frame is intact and fully de-risked by validated data/dossiers, but no SAE evidence
  yet exists; the revision reorients the next iteration to produce it.
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
- id: art_RidEJtBC7gPT
  label: method
- id: art_I2MrezW41iQo
  label: diagnostic
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
- id: art_RidEJtBC7gPT
  label: method
- id: art_I2MrezW41iQo
  label: diagnostic
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
- id: art_RidEJtBC7gPT
  label: method
- id: art_I2MrezW41iQo
  label: diagnostic
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
</all_artifacts>

<new_artifacts_this_iteration>
These 4 artifacts were created THIS iteration.

id: art_0ueMMR8Tt02P
type: experiment
in_dependencies:
- id: art_dpYpjSn2Xvg3
  label: dataset
- id: art_RidEJtBC7gPT
  label: method
- id: art_I2MrezW41iQo
  label: diagnostic
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

id: art_-o2RPMOZp37A
type: experiment
in_dependencies:
- id: art_8QO7pl6Pd8UQ
  label: dataset
- id: art_RidEJtBC7gPT
  label: method
- id: art_I2MrezW41iQo
  label: diagnostic
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

id: art_QGSdsKY6U1vK
type: experiment
in_dependencies:
- id: art_t2uUbjSwpd3t
  label: dataset
- id: art_RidEJtBC7gPT
  label: method
- id: art_I2MrezW41iQo
  label: diagnostic
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

id: art_YwjLYapklnVk
type: dataset
in_dependencies:
- id: art_I2MrezW41iQo
  label: protocol
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
</new_artifacts_this_iteration>

<current_paper>
The paper draft from this iteration — represents the current state of the research story.

# Introduction

Sparse autoencoders (SAEs) decompose the activations of large language models (LLMs) into a dictionary of sparsely-activating latents intended to be interpretable, monosemantic units of analysis \citep{Cunningham2023, Bricken2023, Templeton2024}. The promise is operational: a latent that reliably tracks a human concept can be read off as a classifier, flipped as a steering knob, or compared across model variants for model-diffing. Public SAE suites such as Gemma Scope \citep{Lieberum2024} expose millions of such latents over open models, making this a practical interface for safety-relevant interpretability.

This promise is undercut by a now well-documented fact: \emph{single SAE latents are not reliable units} \citep{Leask2025}. Two failure modes recur. \emph{Feature splitting} fragments one concept across many latents, so no single latent captures it. \emph{Feature absorption} is more insidious: a more specific child latent suppresses the firing of a more general parent latent, leaving the parent with unpredictable holes on exactly the sub-contexts the child covers; parent and child are \emph{mutually exclusive in firing} \citep{Chanin2024}. (A related failure, \emph{feature hedging}, merges correlated features into one polysemantic latent in narrow SAEs \citep{Chanin2025}; a hedged latent is not groupable and is out of scope.) On concrete downstream tasks the practical cost is stark: difference-of-means probes are the strongest concept detectors and raw-latent SAE methods are uncompetitive \citep{Wu2025}, while standardized suites quantify absorption, sparse-probing, and targeted erasure \citep{Karvonen2025}. Any method that proposes SAE latents as a knowledge representation must therefore clear strong, simple baselines and address splitting and absorption head-on.

The task is hard because the obstacles defeat the obvious instruments \emph{by construction}. The intuitive fix for an unreliable single latent is to group several latents into a cluster-level unit. But every existing post-hoc grouping signal is \emph{observational}: which latents fire together (co-activation feature families \citep{ONeill2024, Deng2025}) or which decoder directions point alike (geometry). Absorption is precisely the regime where observational signals must fail---the parent and the absorbing child are mutually exclusive in firing, so co-activation can never group them, and their decoders need not be cosine-similar \citep{Chanin2024}. The standard \emph{supervised} remedy, selecting the top-$N$ latents by causal effect on a concept probe (SCR/TPP attribution \citep{Karvonen2024, Marks2024}), is no better: a latent that fires only in a narrow sub-context has low \emph{marginal} attribution and is silently dropped, even though it carries the concept there. The latents one most needs are exactly the ones these instruments discard.

Why has this not been solved post-hoc? Recent architectural remedies---Matryoshka SAEs \citep{Bussmann2025}, hierarchical SAEs \citep{Muchane2025}, and subspace-aware SAEs \citep{Dalili2026}---all \emph{retrain} the SAE to reduce splitting and absorption at training time. They do not help a practitioner holding a frozen public SAE, and none produces a human-auditable multi-member unit over an existing dictionary. We take the opposite stance: a \emph{training-free, post-hoc repair of frozen public SAEs}. The methodological gap we fill is the \emph{grouping operator}. We observe that grouping by \emph{interventional co-response}---how latents jointly track a content counterfactual, rather than how they co-fire at baseline---is the matched instrument, with a direct precedent in systems biology, where differential co-expression methods (DiffCoEx \citep{Tesson2010}, WGCNA \citep{Zhang2005}) cluster genes by correlated response to a perturbation precisely because co-regulated genes are often not co-expressed at baseline. Crucially, correlation is the right operator only for the \emph{shared-support} splitting case. Absorbers respond on \emph{disjoint} supports and have low pairwise correlation, so no affinity-merging clustering can even \emph{propose} the right group. The disjoint-support case is a \emph{maximum-coverage} problem, whose classic greedy solution \citep{Nemhauser1978, Feige1998} is the natural---and, we argue, the only correct---proposer for absorption units.

We introduce \textbf{Two-Track Co-Response Grouping (CCRG)} and, unlike the previous iteration of this work, we \emph{execute} it on a frozen Gemma Scope SAE rather than pre-registering it. Three findings result. (1) On the first-letter spelling testbed---the regime where absorption is guaranteed to exist---the label-free unit is the best classifier on all five letters and recovers the parent plus per-token absorbers; this is the load-bearing positive. (2) Absorption \emph{generalizes} beyond spelling: the K-track recovers numeric and country absorbers that marginal-attribution pools drop. (3) Most informatively, we replace a prior label-based regime claim with a \emph{direct measurement of SAE-latent firing}, which reveals that toxicity is a co-firing (splitting) regime, not an absorption regime, so the set-cover track is unnecessary there and attribution selection wins. This firing-structure measurement is a cheap diagnostic that predicts, before any grouping, whether CCRG can help on a given concept---turning what could have been an over-claim into a falsifiable scope statement.

[FIGURE:fig1]

\paragraph{Summary of contributions.}
\begin{itemize}
\item \textbf{A two-track grouping algorithm} (\S\ref{sec:method}). A concrete, training-free procedure that proposes split families by content-response correlation (C-track) and absorption units by an anchored greedy set-cover (K-track), reconciles them, and filters them with a single null-anchored, multiplicity-controlled admission rule. To our knowledge, maximum-coverage set-cover has not previously been used to group SAE latents, and it is exactly the operator the disjoint-support absorption regime requires.
\item \textbf{An executed primary result on first-letter spelling} (\S\ref{sec:firstletter}). The label-free unit is the best starts-with-letter classifier on all five letters (AUC 0.86--0.96), beating the best raw latent, count-matched observational clusters, and a count-matched oracle-attribution pool; it recovers the diagnostic parent plus $\geq 2$ absorbers on 4/5 letters and beats the count-matched pool on absorbed-slice recall (paired-bootstrap CI excluding 0) on the two best-powered letters.
\item \textbf{Absorption generalizes beyond spelling} (\S\ref{sec:nonspelling}). On a novel non-spelling testbed the unit recovers a numeric (\texttt{integer}) and a country (\texttt{Georgia}) absorber that marginal-attribution pools drop at matched pool size, with near-zero false positives.
\item \textbf{A firing-structure test for when grouping helps} (\S\ref{sec:toxicity}). Measuring real SAE-latent firing on toxicity shows the regime is co-firing, not absorption, so CCRG does not help and attribution wins---an honest negative that doubles as an a-priori applicability test, replacing the previous label-based proxy.
\item \textbf{Four frozen testbeds and a single-GPU pipeline} (\S\ref{sec:setup}). 109{,}754 examples across spelling, a numeric/taxonomic absorption hierarchy, toxicity, and sentiment/aspect, with eleven baselines and honestly reported failure modes.
\end{itemize}

# Related Work
\label{sec:related}

\paragraph{SAEs and the unreliability of single latents.} Sparse dictionary learning on LLM activations yields interpretable features \citep{Cunningham2023, Bricken2023, Templeton2024, Lieberum2024}, but a growing body of work shows individual latents are not canonical units \citep{Leask2025}. \citet{Chanin2024} introduce and quantify \emph{feature absorption}---a specific child latent suppresses a general parent's firing---demonstrated on first-letter spelling, and \citet{Chanin2025} characterize \emph{hedging}. Dense-latent analyses confirm that single-latent semantics are unstable \citep{Sun2025}, and benchmarks make the practical cost concrete: AxBench finds difference-of-means strongest and raw-latent SAE methods uncompetitive \citep{Wu2025}; SAEBench standardizes absorption, sparse-probing, and erasure evaluations \citep{Karvonen2025}; and recent audits caution these benchmarks are imperfect ground truth \citep{Chanin2026}. We do not stake our load-bearing claim on out-classifying a strong dense probe; our central comparison is against SAE-\emph{selection} baselines.

\paragraph{Post-hoc grouping of SAE features.} Prior grouping is observational: co-activation ``feature families'' \citep{ONeill2024}, sparse feature coactivation modules \citep{Deng2025}, and decoder-geometry clusters group latents by what fires together or which decoders align. Closest to our output, \citet{Winnicki2026} build a knowledge graph from SAE features via co-occurrence and decoder geometry. Our edges differ in kind: they are \emph{interventional specialization edges} (an absorbed/split child of an anchor) over \emph{multi-member} co-response units, encoding conditioning environments invisible to co-occurrence, and we measure their utility rather than only displaying them. By construction, observational signals cannot group an absorbed parent and child, which are mutually exclusive in firing; we therefore count-match observational clusters to our unit's size so any win reflects \emph{selection}, not capacity.

\paragraph{Supervised latent selection.} SHIFT and the SCR/TPP family rank individual latents by causal effect on a concept probe and ablate the top-$N$ \citep{Marks2024, Karvonen2024}. A latent firing only in a narrow sub-context has low marginal attribution and is silently dropped---the exact gap our co-response set-cover fills. We use SCR/TPP-style ranking as our oracle-pool baselines.

\paragraph{Architectural remedies vs. our setting.} Matryoshka \citep{Bussmann2025}, hierarchical \citep{Muchane2025}, and subspace-aware \citep{Dalili2026} SAEs modify \emph{training} to reduce splitting/absorption. They are orthogonal to our setting: we repair a \emph{frozen} public SAE post-hoc and emit an auditable graph rather than retraining a dictionary.

\paragraph{Cross-field instruments and robustness.} The C-track imports differential co-expression module discovery \citep{Tesson2010, Zhang2005} and Leiden community detection \citep{Traag2018}; the K-track imports the maximum-coverage / set-cover greedy with its $(1-1/e)$ guarantee \citep{Nemhauser1978, Feige1998}. The supporting robustness framing engages label-free worst-group-robustness work---group-DRO \citep{Sagawa2019}, JTT \citep{Liu2021}, GEORGE \citep{Sohoni2020}, EIIL \citep{Creager2020}, LfF \citep{Nam2020}, group-aware priors \citep{Rudner2024}, and diverse prototypical ensembles \citep{To2025}---which infer groups over \emph{examples} and \emph{retrain}; CCRG instead groups \emph{features}, never retrains, and the recovered absorbers \emph{are} the inferred sub-context specialists. Surface-invariance draws on LEACE concept erasure \citep{Belrose2023} and counterfactual invariance \citep{Veitch2021}; minimal-pair supervision draws on counterfactually-augmented data \citep{Kaushik2019}, CEBaB \citep{Abraham2022}, and ParaDetox \citep{Logacheva2022}. The closest ``cluster counterfactual differences'' template is CDLC in vision \citep{Varshney2025}, which clusters diffusion-counterfactual difference vectors into one continuous direction per class; we cluster \emph{discrete} LLM SAE latents into multi-member units and add a set-cover track for which CDLC has no analogue.

# The Two-Track Co-Response Grouping Method
\label{sec:method}

\paragraph{Preliminaries.} Let the frozen SAE have latents $l \in \{1,\dots,L\}$ with encoder activation $a_l(x)$; a latent \emph{fires} on $x$ iff $a_l(x) > 0$ (Gemma Scope uses a JumpReLU, so the threshold is inside the encoder \citep{Lieberum2024}). For a concept $c$ we are given \emph{content-flip minimal pairs} $(x_{\text{off}}, x_{\text{on}})$ in which the concept is absent/present at matched surface form, plus \emph{surface-flip pairs} in which the concept is held constant and surface varies. The content labels are the supervision every matched baseline consumes; the method uses no absorption-specific oracle. We encode at one residual-stream site (\texttt{gemma-2-2b}, layer 12, width 16k canonical; hook \texttt{blocks.12.hook\_resid\_post}; $d_{\text{model}}=2304$, 16{,}384 latents) \citep{Lieberum2024}.

\paragraph{Step 1: interventional content-response.} For each latent $l$ and pair $p$, the \emph{content-response} is $r_l(p) = a_l(x_{\text{on}}) - a_l(x_{\text{off}})$. We retain \emph{content-responsive} latents whose response exceeds a within-concept shuffle null. A latent's \emph{cover set} $C_l$ is the set of pairs whose content flip it tracks reliably ($r_l(p)>\tau_{\text{resp}}$ and $a_l(x_{\text{on}})>0$) and precisely (firing-precision $\geq 0.7$ on its own support). Because absorbers fire on only a handful of words, a mean-over-pairs prefilter would discard them; eligibility is therefore \emph{cover-based} (selective \emph{and} covering $\geq 1$ sub-context), which retains the genuinely sparse absorbers.

\paragraph{Step 2: C-track --- correlation communities for splitting.} Where a concept \emph{splits}, sub-latents share firing support and co-respond positively, so pairwise affinity is appropriate. We build a sign-aware soft-thresholded affinity from the positive part of the Spearman correlation between response profiles, $A^{C}_{l,l'} = \max(\rho(r_l, r_{l'}), 0)^{\beta}$ with $\beta=6$ (WGCNA's scale-free criterion \citep{Zhang2005}), and run Leiden community detection (RBConfiguration partition \citep{Traag2018}). Resolution is fixed by bootstrap-ARI stability against a shuffle null. (In practice Leiden's C extension intermittently hangs on tied-rank graphs; we run it in a subprocess with a 45\,s timeout and fall back to agglomerative clustering, recorded per run.)

\paragraph{Step 3: K-track --- anchored greedy set-cover for absorption.} Absorbers respond on \emph{disjoint} supports and are mutually exclusive in firing with their parent, so their pairwise correlation is low and no affinity-merging clustering can propose them (Figure~\ref{fig:tracks}). We use a different operator: an anchored greedy maximum-coverage procedure. \textbf{(1) Anchor:} $l^\* = \arg\max_l |C_l|$, the highest-recall ``general/parent'' candidate, chosen using \emph{only} the pairs and \emph{not} the absorption diagnostic, with ties broken toward the broadest support. \textbf{(2) Holes:} $H = P \setminus C_{\text{anchor}}$, the pairs the parent goes silent on. \textbf{(3) Greedy cover:} while $H$ is non-empty and improving, add $\arg\max_l |C_l \cap H|$ subject to mutual exclusivity (firing-Jaccard $<0.1$ with members), per-member precision $\geq 0.7$, and a marginal-coverage-gain floor $\geq 0.05$ whose bootstrap CI excludes 0. The greedy max-coverage choice is the classic instrument for ``cover a universe with complementary specialists,'' with the $(1-1/e)$ guarantee \citep{Nemhauser1978, Feige1998}; coverage-complementarity is a set-level property, which is exactly why a pairwise operator cannot express it.

[FIGURE:fig2]

\paragraph{Step 4: reconciliation.} For each C-community we designate its highest-recall member as a candidate anchor and run Step 3 to pull in mutually-exclusive absorbers covering its holes; we also seed Step 3 from standalone high-recall latents in no dense community. A final unit is a pure C-community (splitting), a pure K-cover (absorption), or a hybrid; we de-duplicate by highest coverage gain.

\paragraph{Step 5: admission filter with multiplicity control.} A proposed unit is admitted iff it clears \textbf{signature C} (within-unit content-response correlation above the 95th-percentile shuffle null) \textbf{or signature K} (pooled-max minus best-single content-response AUC above the 95th percentile of a best-of-random-$k$ null \emph{matched on marginal AUC}, plus the $k\in\{2,3\}$ absolute gain floor of $0.05$ with bootstrap CI excluding 0, plus mutual exclusivity and the precision floor), \textbf{and} unit-level surface invariance (pooled surface-response not above the shuffled-surface null). Because many candidate units are tested per concept, we control multiplicity at the \emph{unit-proposal} level: a Bonferroni-within-unit $p$ over the disjunctive (C-or-K) signature, then Benjamini--Hochberg across the $M$ candidate units in a concept, and we report $M$ and the \emph{empirical} family-wise false-admit rate under the matched random-$k$ null---separate from the Holm--Bonferroni used across headline claims.

\paragraph{Proposal-step pilot.} Before any absorber-recovery claim relies on the K-track, a never-dropped pilot runs Step 3 on content-flip pairs \emph{alone} and checks that the proposed anchor and absorbers match the parent and absorbers the supervised diagnostic of \citet{Chanin2024} identifies (membership F1 above a random-membership null), and that the recall-argmax anchor actually coincides with the diagnostic parent (\emph{anchor fidelity}). A failure here is reported as a proposal-step failure, not silently omitted.

\paragraph{Non-circular diagnostic and auditable graph.} Specialization edges are \emph{scored}, never formed, by the absorption diagnostic of \citet{Chanin2024}. Because the strict form needs an output logit, we use the domain-agnostic \emph{form-free} variant (the appendix probe-projection, implemented in SAEBench as \texttt{absorption\_fraction}): $l$ absorbs iff $\tau_c < (\hat{a}_l \cdot d_p)/(a \cdot d_p)$, with $d_p$ a parent-concept probe trained on data \emph{disjoint} from clustering. The anchor is chosen by recall available to every baseline, so ``the unsupervised unit beats the supervised oracle'' is not undercut. Each admitted unit is emitted with logit-lens tokens and top conditioning contexts, plus directed anchor$\to$child specialization edges---a feature-level knowledge graph.

# Testbeds, Baselines, and Protocol
\label{sec:setup}

\paragraph{Constructed testbeds.} We built four frozen, schema-standardized families (Table~\ref{tab:testbeds}) totalling 109{,}754 examples. All are pure text/data artifacts---no SAE or model weights baked in---so absorption presence is an empirical question for the SAE run, not a construction artifact. Words for the spelling and non-spelling hierarchies are anchored in the real \texttt{gemma-2-2b} vocabulary and a pinned Pile revision, so they never derive from the latents being grouped (non-circular). The first-letter testbed contributes 17{,}180 examples over five letters (L/O/T/I/D) with 0 deterministic flip/span violations [ARTIFACT:art_dpYpjSn2Xvg3]; the non-spelling testbed contributes 24{,}128 examples over a numeric-quantity hierarchy and a taxonomic ``is-a-country'' hierarchy [ARTIFACT:art_t2uUbjSwpd3t]; the toxicity family contributes 37{,}707 examples from ParaDetox \citep{Logacheva2022} and civil\_comments \citep{Borkan2019} [ARTIFACT:art_8QO7pl6Pd8UQ]; and a supporting family contributes 30{,}739 examples of CAD-IMDB sentiment \citep{Kaushik2019}, CEBaB aspect-sentiment \citep{Abraham2022}, and a bias\_in\_bios boundary-null \citep{DeArteaga2019} [ARTIFACT:art_21JWypIydPMX].

\begin{table}[t]
\centering
\small
\caption{Constructed testbeds. Counts are released examples; pairs are reconstructable minimal pairs. LB = load-bearing, NS = non-spelling spine, SP = supporting, BN = boundary-null.}
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

\paragraph{Baselines.} We compare CCRG units against eleven baselines (Table~\ref{tab:baselines}), spanning raw latents, observational clusters (count-matched for classification), dense probes (including a LEACE surface-invariant hyperplane), supervised oracle pools, and label-free/oracle group-robustness probes. The design isolates \emph{selection at matched pool size}: against the count-and-pool-matched attribution pool (h), the unit and (h) pool the same number of directions and vary only \emph{how} members are chosen.

\begin{table}[t]
\centering
\small
\caption{Baseline glossary. (b)/(c) are count-matched to the unit's member count $k$; (h) is count-and-pool-matched to isolate the selection criterion.}
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
(h) & Count-and-pool-matched: max-pool over exactly $k$ SCR/TPP-selected raw directions \\
(i) & Unmatched difference-of-means / probe on raw labels \\
(j) & Oracle group-DRO probe with true sub-context labels (robustness upper bound) \\
(k) & Label-free group-inference probe (JTT/GEORGE-style) \\
\bottomrule
\end{tabular}
\end{table}

\paragraph{Encoding and gating.} The SAE is loaded directly from Gemma Scope \texttt{params.npz} (canonical \texttt{layer\_12/width\_16k}); the residual is captured by a forward hook on \texttt{model.layers[12]}. Each run gates on reconstruction fidelity before analysis: on first-letter, reconstruction cosine $0.924$, explained variance $0.857$, mean L0 $95.9$, and exact word-token localization (0/64 mismatches) [ARTIFACT:art_0ueMMR8Tt02P]; on toxicity, reconstruction cosine $0.916$ [ARTIFACT:art_-o2RPMOZp37A]; on the non-spelling testbed, encode-time FVU $0.18$/$0.20$ and token-alignment $0.975$/$1.000$ [ARTIFACT:art_QGSdsKY6U1vK].

\paragraph{Statistics and the primary endpoint.} The primary statistical object is the per-concept paired bootstrap CI ($B=10{,}000$ on per-example correctness differences), with an exact McNemar confirmatory and Holm--Bonferroni across claims. We declare a single \emph{primary falsification endpoint} on first-letter (the guaranteed-signal regime): the method works iff (E1) the K-track proposal step, given only content-flip pairs, recovers the diagnostic parent plus $\geq 2$ absorbers above a random-membership null, \emph{and} (E2) the resulting label-free unit beats the count-matched pools on classification and absorbed-slice recall with a CI excluding 0. The honest-null branches reported below are \emph{secondary characterizations} of how the method behaves, not co-equal successes; a clean E1$\wedge$E2 failure on first-letter would mean the method does not work.

# Results: First-Letter Spelling (Primary Endpoint)
\label{sec:firstletter}

We ran the full pipeline on all five letters in $\sim$8 minutes on one RTX 4090, with \$0 in LLM spend (the diagnostic is the form-free probe-projection) [ARTIFACT:art_0ueMMR8Tt02P].

\paragraph{C1 classification: the label-free unit is the best classifier on all five letters.} Treating each method's pooled activation as a starts-with-letter classifier, the co-response unit attains the highest held-out AUC on every letter---L $0.905$, O $0.917$, T $0.859$, I $0.961$, D $0.956$---beating the best raw latent (a), the count-matched co-activation (b) and decoder-geometry (c) clusters, \emph{and} the count-and-pool-matched oracle-attribution pool (h) in every case (Figure~\ref{fig:c1}). The margin over (h) is large and significant on the harder letters (unit$-$(h) AUC: T $+0.205$, CI $[0.064,0.333]$; I $+0.405$, CI $[0.286,0.524]$; D $+0.456$, CI $[0.333,0.578]$) and positive but not significant on L ($+0.091$) and O ($+0.150$). On I, where every individual baseline is weak ($\leq 0.833$), the unit reaches $0.961$: pooling the right complementary members recovers signal no single selection criterion captures. This is the load-bearing positive---cluster-level units are a more reliable unit of analysis than single latents, observational clusters, or supervised attribution pools.

[FIGURE:fig3]

\paragraph{E1 absorber recovery: 4/5, with one honest anchor failure.} Given only content-flip pairs, the K-track recovers the diagnostic-identified parent plus $\geq 2$ absorbers above the 95th-percentile random-membership null on L, O, T, and D (membership F1 vs.\ null: L $0.308$ vs.\ $0.103$; O $0.300$ vs.\ $0.150$; T $0.263$ vs.\ $0.211$; D $0.381$ vs.\ $0.190$, with 7 absorbers). On these four letters the recall-argmax anchor \emph{is} the diagnostic parent (anchor corpus-firing rate $0.27$--$0.39$). The units are human-auditable: for L, anchor latent 205 (logit-lens \texttt{Lohan/Ls/LS/LF}) plus absorbers 3069=\texttt{list}, 2416=\texttt{line}, 8463=\texttt{large}, 4736=\texttt{l\ldots ing}; for D, anchor 6210 (\texttt{PhysRevD/DPR/DSS}) plus 1970=\texttt{different}, 7293=\texttt{director}, 10769=\texttt{day}. A 70-edge anchor$\to$absorbed-child knowledge graph is emitted. E1 \emph{fails} on I by anchor fidelity only: the highest-cover-set latent (1227) fires 0\% on the corpus and has code-token logit-lens---a spurious anchor, not the semantic parent. We report this as a mechanism finding: the recall-argmax heuristic is not always the concept parent, yet the pooled unit remains the best I classifier (AUC $0.961$).

\paragraph{E2 absorbed-slice recall: the unit beats count-matched pools.} On the absorbed slice---words on which the parent goes silent---the unit beats the count-matched pool (h) directionally on all five letters and significantly on the two best-powered slices: T $0.925$ vs.\ $0.763$ (CI of difference $[0.054,0.269]$) and I $0.775$ vs.\ $0.496$ (CI $[0.178,0.380]$). It also beats the count-matched observational clusters (b)/(c) significantly on every letter, and beats the larger 10-latent oracle pool g10 significantly throughout. We deliberately base the E2 verdict on these \emph{non-circular} downstream metrics rather than on a recovered-absorber \emph{count}: the count is circular for the oracle baselines, because the diagnostic and the attribution pools (g)/(h) both rank by the same probe direction $d_p$, so they trivially overlap the diagnostic. The 20-latent oracle pool (g) is competitive on the slice (e.g.\ L $0.883$), but it is not count-matched; at matched pool size the co-response unit wins.

\paragraph{Steering: lowest collateral on the primary letter.} As a generality demonstration, we steer with the unit's mean-member-decoder direction and compare, at \emph{matched} on-target effect, the full-vocabulary KL divergence on unrelated prompts against a best-single-member (hub) direction and a non-SAE difference-of-means direction (Figure~\ref{fig:steer}). On the primary letter L the unit is the most surgical---KL $16.4$ versus hub $27.9$ and diff-of-means $30.4$ at the same on-target shift---and likewise on D ($28.6$ vs.\ $33.3$/$30.5$). On O and T a non-SAE diff-of-means is more surgical, and on I the hub is; we report steering honestly as a demonstration, not a load-bearing claim, and note that the unit's advantage tracks the letters where E1 anchor fidelity holds.

[FIGURE:fig5]

\paragraph{Admission.} The K-unit is admitted via signature K on all five letters (surface-invariant, $p_{\text{surf}}=1.0$); the empirical false-admit rate under the matched random-$k$ null is $0.03$--$0.09$, at or near the $0.05$ target. We note a real limitation: within the eligible set, random $k$-latent pools also classify well (random-gain-$>$-0.05 fraction $\approx 0.92$--$1.0$), so the admission filter's discriminative power comes from the surface-invariance gate and the matched-null signature-K test, not from pooling per se.

# Results: Absorption Generalizes Beyond Spelling
\label{sec:nonspelling}

Absorption is documented empirically almost only on first-letter spelling: the original study is spelling-only \citep{Chanin2024}, SAEBench's sole absorption eval is \texttt{absorption\_first\_letter} \citep{Karvonen2025}, and the Matryoshka/hierarchical mitigations measure it via the spelling metric \citep{Bussmann2025, Muchane2025}. We therefore treat the non-spelling testbed as both a generality test and a novel empirical question, gated by an explicit non-triviality pre-check [ARTIFACT:art_QGSdsKY6U1vK].

\paragraph{The non-triviality gate passes on both hierarchies.} On the \emph{numeric} hierarchy the parent latent 14823 (content-response precision $1.000$, negative-firing $0.0006$) covers $0.829$ of content flips but only $0.427$ of the corpus, missing 1{,}060 positives---genuine holes. The K-track fills them with a year and two decimal absorbers. On the \emph{taxonomic} hierarchy the parent latent 3792 (recall $0.953$) admits Georgia, Jordan, and United-States specialists. Both gates pass: absorption is \emph{not} spelling-specific.

\paragraph{The K-track recovers absorbers the oracle pool drops, with near-zero false positives.} At matched overall recall, the compact 4-latent unit beats the marginal-attribution pools on the absorbed sub-context that defines each hierarchy (Table~\ref{tab:nonspelling}). On numeric \texttt{integer}, unit recall $0.283$ versus (g) $0.107$ and (h) $0.110$ (unit$-$(g) $+0.177$, CI $[0.120,0.237]$, Holm $p=8\!\times\!10^{-8}$; unit$-$(h) $+0.173$, CI $[0.117,0.233]$), with the unit at \emph{zero} false positives versus $0.12$/$0.13$ for the oracle pools. On taxonomic \texttt{Georgia}, unit recall $0.713$ versus (h) $0.520$ (unit$-$(h) $+0.193$, CI $[0.073,0.307]$, Holm $p=0.035$), again at near-zero false positives ($0.014$ vs.\ $0.85$/$0.65$). The honest nuance: gains are sub-context-specific, not blanket wins over the 20-latent oracle (on numeric year/date/decimal the larger pool wins); the form-free diagnostic corroborates the K-track edges for taxonomic (top-1 agreement $0.318$ vs.\ null $0.002$; the Jordan edge agrees $0.99$) but diverges for numeric, where coverage-based and projection-based absorber notions disagree; and a non-SAE dense probe reaches recall $1.0$ at zero false positives---the ``simple baselines can match raw-SAE'' point, reported plainly.

\begin{table}[t]
\centering
\small
\caption{Non-spelling absorber recovery at matched overall recall. The compact K-track unit beats the count-matched attribution pool (h) and the larger oracle pool (g) on the defining absorbed sub-context, with near-zero false positives. Recall on the absorbed slice; FP = false-positive rate.}
\label{tab:nonspelling}
\begin{tabular}{llccccc}
\toprule
Hierarchy & Absorbed sub-context & unit & (g) pool & (h) pool & dense probe & unit FP \\
\midrule
Numeric & \texttt{integer} & \textbf{0.283} & 0.107 & 0.110 & 0.643 & 0.000 \\
Taxonomic & \texttt{Georgia} & \textbf{0.713} & 0.800 & 0.520 & 0.807 & 0.014 \\
\bottomrule
\end{tabular}
\end{table}

# Results: A Firing-Structure Test for When Grouping Helps
\label{sec:toxicity}

The previous iteration argued that both splitting and absorption regimes occur in safety data using civil\_comments sub-attribute \emph{label} co-occurrence. A reviewer correctly noted that label co-occurrence is not latent co-firing: a single general toxicity latent can fire across all sub-attributes regardless of label disjointness, so the label statistic does not establish that any pairwise operator fails on real SAE latents. We replace the proxy with a \emph{direct measurement} of SAE-latent firing [ARTIFACT:art_-o2RPMOZp37A].

\paragraph{Toxicity is a co-firing regime, not an absorption regime.} The general toxicity latent (12714, Neuronpedia: ``profanity and vulgar expressions'') fires on $94.3\%$ of toxic content-flips (precision $0.996$). Distinct, on-target detector latents exist for the label-disjoint sub-attributes---threat (11630, ``conflict and violence'', AUC $0.828$), identity\_attack (11573, ``race, identity, social justice'', AUC $0.930$), insult (13367, ``hypocrite/moron/coward'', AUC $0.871$)---and they cover the general latent's recall holes (cover-fraction $0.74$/$0.93$). \emph{But they co-fire with the general latent}: the toxic-only firing-Jaccard is $0.403$ (threat, CI $[0.392,0.414]$), $0.292$ (identity\_attack, CI $[0.282,0.303]$), and $0.655$ (insult)---all far above the $0.10$ mutual-exclusivity threshold absorption requires (Figure~\ref{fig:firing}). The SAE firing structure thus \emph{departs sharply from the label co-occurrence structure} (label-Jaccard: threat $0.044$, identity\_attack near-zero): there is no mutual exclusivity, so the K-track's necessity is \textbf{refuted} on toxicity. The set-cover track correctly adds zero absorbers here.

[FIGURE:fig4]

\paragraph{Consequently, grouping does not help and attribution wins.} The $k{=}3$ co-response unit ties the count-matched observational and single-latent baselines on toxicity classification (AUC $0.762$ vs.\ (a) $0.765$, (b) $0.797$, (c) $0.792$) but is beaten by attribution selection ((g) $0.892$, (h) $0.837$) and a full-residual probe ((e) $0.859$); unit$-$(h) AUC CI $[-0.093,-0.055]$, Holm $p\approx 5\!\times\!10^{-71}$. It \emph{collapses} on the disjoint sub-attributes (threat $0.626$ vs.\ (h) $0.929$; identity\_attack $0.633$ vs.\ (h) $0.936$). The pre-registered selection ordering $(f)<(g)/(h)<\text{unit}$ on worst-sub-context recall does \emph{not} hold (f $0.086 <$ unit $0.237 <$ g $0.393 <$ h $0.451$), and the unit$-$(g)/(h) gap \emph{shrinks} under sub-population reweighting toward the under-served sub-attributes (slope $-0.474$, CI $[-0.536,-0.412]$). This is a clean, decisive honest negative.

\paragraph{Why this strengthens, not weakens, the contribution.} The firing-Jaccard is a single cheap forward pass over data one already has, and it predicts the outcome \emph{before} any grouping: where detectors are mutually exclusive with the parent (spelling, numeric, taxonomic), CCRG recovers absorbers and out-classifies attribution pools at matched size; where they co-fire (toxicity), the regime is splitting/co-activation and supervised attribution is the right tool. Rather than over-claiming a universal win, we deliver an a-priori applicability test. The C-track unit on toxicity is also less interpretable than the absorption units (its anchor is the profanity latent, but its co-members include off-target name and acronym latents), consistent with the C-track being the secondary track.

\paragraph{Admission and the strengthened surface control.} On toxicity, $M=31$ candidate units were tested; 11 were admitted, with an empirical family-wise false-admit rate of $0.08$ under the random-$k$ null and bootstrap cluster-stability ARI $0.79$ (CI $[0.70,0.92]$) against a shuffle-null ARI of $0$. The surface-invariance gate is load-bearing, so we enlarged the surface-flip pair sets (first-letter $590\to1{,}700$; toxicity $546\to1{,}631$) and re-judged with an independent model family: an Anthropic judge confirms $85.2\%$ ($465/546$) of the original gpt-4o-mini-accepted toxicity pairs, removing the iter-1 same-model generate-and-judge circularity, for \$1.72 total [ARTIFACT:art_YwjLYapklnVk]. We report the per-concept surface-response null sizes used per admission.

# Discussion
\label{sec:discussion}

\paragraph{What is established.} CCRG, executed on a frozen Gemma Scope SAE, produces auditable multi-member units that (i) out-classify raw latents, count-matched observational clusters, and a count-matched supervised attribution pool on all five first-letter spelling tasks; (ii) recover the parent plus per-token absorbers on 4/5 letters and beat the count-matched pool on absorbed-slice recall; and (iii) recover numeric and country absorbers that marginal-attribution drops at matched pool size, establishing that absorption is not a spelling artifact. These are SAE-\emph{selection} comparisons, so the load-bearing claim does not depend on out-classifying a strong dense probe---which, honestly, we do not always do (a dense probe matches the unit on the non-spelling slices).

\paragraph{The contribution is regime-scoped, and we can say which regime a priori.} The most important methodological lesson is that grouping helps exactly in the absorption regime (mutually-exclusive parent/child firing) and not in the co-firing/splitting regime, and that a single firing-Jaccard measurement separates the two before grouping. This reframes the method from ``a universal repair'' to ``a repair for absorption, with a test for applicability,'' which is both more defensible and more useful: a practitioner can run the cheap test and know whether to reach for set-cover grouping or for supervised attribution.

\paragraph{Honest failure modes.} (1) The recall-argmax anchor is not always the semantic parent (letter I: a code-token latent fires 0\% on the corpus yet maximizes cover-set size); a parent-validation step is needed for unsupervised deployment. (2) E2 is significant on the two best-powered absorbed slices and directional elsewhere; the recovered-absorber \emph{count} is circular for oracle baselines and is reported descriptively only. (3) Within the eligible set, random $k$-pools also classify well, so admission power comes from the surface-invariance gate, not pooling. (4) On toxicity the unit ties weak baselines and loses to attribution, and its advantage shrinks under sub-population shift. (5) The form-free diagnostic corroborates K-track edges for taxonomic but not numeric absorption. Each is reported with its statistic rather than spun as future work.

\paragraph{Limitations: model-diffing.} The goal mandates a model-diffing demonstration, but no instruction-tuned Gemma Scope SAE exists for the 2B model (Google's IT residual SAEs cover only 9B). Diffing would therefore require applying the shared frozen pretrained SAE to base and instruction-tuned activations---a confounded setup, not a paired-SAE diff. We do not present a model-diffing result and state this as an explicit infrastructure limitation rather than deferring it to open-ended future work. We also scope the method to splitting and absorption: a hedged single polysemantic latent is not groupable \citep{Chanin2025}.

# Conclusion
\label{sec:conclusion}

We presented Two-Track Co-Response Grouping, a training-free method that organizes the latents of a frozen public SAE into reliable, auditable concept units by their interventional response to content counterfactuals---correlation communities for shared-support splitting and an anchored greedy set-cover for disjoint-support absorption that no pairwise-affinity clustering can propose. Executed on Gemma Scope, the label-free unit is the best classifier on all five first-letter spelling tasks (AUC 0.86--0.96), beating raw latents, count-matched observational clusters, and a count-matched oracle-attribution pool; it recovers per-token absorbers and beats the count-matched pool on absorbed-slice recall; and absorption generalizes to numeric (\texttt{integer}) and country (\texttt{Georgia}) hierarchies with near-zero false positives. A direct measurement of SAE-latent firing shows that toxicity is a co-firing regime in which grouping does not help and supervised attribution wins---turning a potential over-claim into a cheap, a-priori applicability test. We release four frozen testbeds, the single-GPU pipeline, and a complete account of where the method works and where it does not.

\paragraph{Future work.} Add an unsupervised parent-validation step to fix the anchor-fidelity failure; extend the firing-Jaccard applicability test into a routing rule that picks set-cover grouping versus attribution per concept; and revisit model-diffing if a paired instruction-tuned SAE becomes available.

\bibliographystyle{plainnat}
\bibliography{references}
</current_paper>

<reviewer_feedback>
Feedback from the paper reviewer this iteration.

- [MAJOR] (evidence) The headline C1 classification margins are mislabeled and overstated. The paper writes 'unit-(h) AUC: T +0.205, CI [0.064,0.333]; I +0.405, CI [0.286,0.524]; D +0.456, CI [0.333,0.578].' I confirmed in full_method_out.json that these CIs are the paired-bootstrap differences in per-example CORRECTNESS (accuracy at each method's train-fit F1-optimal threshold), NOT AUC differences. The actual point-AUC margins over (h) are far smaller: T 0.859-0.648=+0.211, I 0.961-0.833=+0.128, D 0.956-0.726=+0.230. Worse, the large accuracy gaps on I and D are partly a threshold artifact: (h)'s F1-optimal train threshold collapses to 0.0 (predict-all-positive, giving ~0.5 accuracy) even though its AUC is a respectable 0.833/0.726. So a substantial fraction of the reported 'AUC' separation reflects a degenerate baseline operating point, not separability. No CIs are reported on the true AUC differences, and per-letter test sets are tiny (n=60-90 words).
  Action: Stop calling these AUC margins. Report (i) AUC point values with bootstrap AUC-DIFFERENCE CIs (B>=10,000) for unit vs (h)/(b)/(c) on all five letters, and (ii) if you keep an accuracy comparison, select thresholds by a metric matched to the comparison (Youden/accuracy-optimal on train) so no baseline collapses to predict-all. Expect L and O to become non-significant on AUC; state that plainly. This is the single most important honesty fix and it is cheap (data already in hand).
- [MAJOR] (rigor) The pre-registered primary falsification endpoint is not honored as stated. The paper declares: 'the method works iff (E1) ... AND (E2) the resulting label-free unit beats the count-matched pools on classification and absorbed-slice recall with a CI excluding 0,' and 'a clean E1-and-E2 failure ... would mean the method does not work.' But the artifact records verdicts.E2_PASS=false, and the code that emits primary_endpoint='WORKS' computes it as `endpoint = 'WORKS' if (e1 and c1w)` (method.py:1676) -- E2 is dropped from the conjunction and replaced by C1. On the nominal PRIMARY letter L, E2 vs (h) is +0.042 CI [-0.067,0.150] (includes 0) and C1 (accuracy) vs (h) is +0.091 CI [-0.045,0.227] (includes 0). E2 vs (h) excludes 0 on only T and I (2/5). So under the endpoint as written, the result is E1 pass + E2 fail = the conjunction fails, yet the paper reports an unqualified 'WORKS' and calls it 'the load-bearing positive.' This re-opens (partially) my iter-1 concern that the protocol is hard to falsify: the one declared kill-switch was tripped and the verdict was computed around it.
  Action: Be transparent: report E2_PASS=false and that the operative verdict is E1-and-C1, with E2 (CI excluding 0 vs count-matched (h)) holding on 2/5 letters and NOT on the primary letter L. Either (a) re-designate the endpoint to E1-and-C1 and argue why classification-AUC win is the right falsifier, or (b) keep E1-and-E2 and report the method as 'partially confirmed.' Also reconcile the code so the emitted verdict matches the paper's stated endpoint.
- [MAJOR] (methodology) The central 'selection at matched pool size' claim is not isolated from a simpler explanation. The unit is a 15-latent max-pool (k=15 on every letter), of which only ~4-7 are the named anchor+absorbers; the remaining ~8-11 members are uncharacterized eligible latents. The paper itself reports that ~97-99% of RANDOM eligible k-pools clear the admission gain floor (frac_randk_gain_gt_0.05 = 0.97/0.98/0.99) and concedes 'admission power comes from the surface-invariance gate ... not from pooling per se.' This strongly suggests the cover-based ELIGIBILITY prefilter plus 15-way pooling -- not the two-track set-cover SELECTION -- may be what beats the attribution pool (h), whose attribution-ranked members are redundant on the easy cases. Yet C1 never compares the unit against a random-eligible-k pool on classification AUC. Without that control, 'the two-track unit is the best classifier' could reduce to 'any 15 eligible latents pooled beat 15 attribution-selected latents.'
  Action: Add a random-eligible-k (=15) pool baseline to C1 and E2 on all five letters, with bootstrap CIs (average over many random draws). If the two-track unit significantly beats the random-eligible pool, the selection contribution is established; if not, reframe the contribution around the eligibility criterion (cover-based selectivity) rather than the set-cover grouping. Either outcome is publishable and far more convincing than the current under-determined claim.
- [MAJOR] (scope) Demonstrated significance is narrow and the practical 'use this over a simple baseline' case is largely unmet. (1) On the non-spelling testbed a non-SAE dense probe dominates the unit (integer: dense 0.643 vs unit 0.283; Georgia: dense 0.807 vs unit 0.713) and the larger 20-latent oracle pool also beats it (Georgia: g 0.800 vs unit 0.713), so the unit only wins against the SIZE-MATCHED attribution pool (h) on the defining sub-context -- a within-SAE-ecosystem result. (2) On toxicity -- the only safety-relevant family, central to the stated goal -- the method explicitly does NOT help (it ties weak baselines, loses to attribution and a residual probe, and collapses on disjoint sub-attributes). (3) Model-diffing, one of the three downstream tasks the goal mandates, is entirely absent (acknowledged as an infrastructure limitation). The goal requires beating a non-SAE baseline on concrete downstream tasks; the unit generally does not. The contribution thus rests on auditability + the diagnostic, neither of which is yet quantified as decision-relevant.
  Action: Sharpen the value proposition along the auditability/steering/diagnostic axes (see contribution improvements): quantify a task where the auditable unit beats a dense probe on a dimension the probe lacks (surgical steering across concepts, or a measured KG repair/utility), and either deliver a bounded model-diffing result or remove it from the contribution claims. Frame the headline as 'a repair for the absorption regime + an a-priori router,' supported by the routing experiment, rather than as a general improvement over baselines.
- [MINOR] (evidence) The 'absorption generalizes beyond spelling' claim is weaker for numeric than the prose suggests. On the numeric hierarchy the form-free oracle diagnostic does NOT corroborate the K-track edges (kg_agreement top-1 = 0.0 vs taxonomic 0.318), i.e. the coverage-based and projection-based notions of 'absorber' disagree, and the integer-slice recovery is low in absolute terms (0.283). So the genuine 'absorber' status (mutual-exclusivity specialist, not merely an additional detector) is only independently validated for taxonomic. The paper notes the divergence but still presents numeric (integer) as a co-equal generalization result and as a contribution bullet.
  Action: Down-weight numeric to a 'suggestive, diagnostic-unconfirmed' result and lead the generalization claim with taxonomic (where the independent diagnostic agrees and the Jordan edge agrees 0.99). State explicitly that on numeric the K-track recovers complementary detectors whose absorber status the projection diagnostic does not confirm.
- [MINOR] (rigor) Per-letter C1 evaluation is small (n=60-90 held-out words) and the auditability/knowledge-graph utility is asserted by emission, not measured. The paper emits a 70-edge anchor->absorbed-child graph but does not test whether the edges carry decision-relevant information beyond classification (earlier iterations contemplated a KG repair-loop / member-labeling-vs-shuffle test, which appears dropped). 'Human-auditable' and 'knowledge graph' are load-bearing for significance but currently unsubstantiated as useful.
  Action: Either (a) enlarge/pool the first-letter classification evaluation and report AUC-difference CIs so 'best on all five' is statistically backed, and (b) add one measured KG-utility result (e.g. LLM-judge agreement that named absorbers match their assigned sub-context vs a shuffle null, or a KG-guided edit that improves parent recall vs a random-edit control), or soften the auditability/KG language to 'we emit, but do not yet evaluate, a feature-level graph.'
- [MINOR] (novelty) The method's headline output -- 'a feature-level knowledge graph from SAE features' -- directly overlaps the closest contemporaneous work, Winnicki 2026 'Domain-Filtered Knowledge Graphs from Sparse Autoencoder Features' (arXiv:2604.23829, which I confirmed resolves), which is differentiated in only one sentence. The distinction (interventional specialization edges over multi-member co-response units vs co-occurrence/geometry edges) is real but should be made unmistakable since the outputs are nominally the same artifact. Also, Chanin et al. 'A is for Absorption' (2409.14507) is now a NeurIPS 2025 paper and should be cited to its venue.
  Action: Expand the Winnicki contrast to 2-3 sentences with a concrete example of an edge CCRG produces that co-occurrence/geometry cannot (a mutually-exclusive parent->absorber edge), and update the Chanin citation to NeurIPS 2025. Audit all 2026-dated citations for venue/version accuracy.
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

### [2] HUMAN-USER prompt · 2026-06-17 17:58:07 UTC

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
