# upd_hypo — test_idea

> Phase: `invention_loop` · round 8 · Substep: `upd_hypo`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave the agent(s) in this substep — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `upd_hypo` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 21:56:35 UTC

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
  Training-Free Auditable Localization and Editing of Homograph-Polysemy SAE Absorption: The Gated-Dense Control PASSED at
  Meaningful Forget on Concentrated Features (large/Amazon), But the Win Predictor Is Latent CONCENTRATION Not Absorption
  Structure -- De-Inflate to +1.00-vs-Strongest-Dense, Add a Bounded-beta d_sub-Gated Control, and Expand the n~=2 Positive
  Base
hypothesis: |-
  ITERATION-7 STATUS -- THE TWO ITER-6 GATES (gated-dense control + honest forget operating point) WERE BOTH EXECUTED. M1'' RETURNED A REAL BUT NARROWER, DIFFERENTLY-CAUSED, AND OVER-STATED POSITIVE: at a forget level where the edit MEANINGFULLY forgets, a discovered single-absorber sparse-gated ablation beats a footprint-matched gated dense edit -- but ONLY on LEXICALLY CONCENTRATED features, the headline magnitude is INFLATED by a mis-tuned gate, and the iter-8 reviewer showed the real win predictor is latent CONCENTRATION/PRECISION, not the absorption structure the method discovers. Iteration 7 delivered: the gated-dense control + honest-forget edit test [art_Cgk9ETiZfvtl]; a confirmatory named-entity homograph screen + gated-dense downstream [art_ZxVw0e4seBq3]; and a gated-steering prior-art + localization-first positioning audit [art_IlzAiXYWeUYH]. What honestly landed, and what the iter-7 reviewer exposed:

          - M1'' GATED-DENSE-CONTROLLED, HONEST-FORGET EDIT EXECUTED [art_Cgk9ETiZfvtl]. A NEW operator DENSE-SUB-ABL-GATED (erase u_sub only where |h.u_sub|>tau, tau calibrated so the gate's global firing fraction over a neutral pool equals the KG absorber's token footprint f_kg) was added, plus a $0 MEANINGFUL-FORGET PROOF: (a) gold-completion log-prob drop on hand probes; (b) a frozen 1-D sub-context probe d_sub (AUC~1.0) scored on the REAL post-edit residual via read_resid_under_edit; meaningful_forget = (completion CI>0) OR (sub-probe drop>=0.1). FIVE operators at the SAME swept matched forget (NOOP, KG-ABL, DENSE-SUB-ABL-GATED decisive, DENSE-SUB-ABL ungated secondary, DENSE-WHOLE-ABL secondary). Per-case 3-way fork. RESULTS (5 cases, $0.80, 2 judges): (1) first_letter_large (spelling absorber 8463) = KG_BEATS_GATED_DENSE AT MEANINGFUL FORGET -- KG meaningfully forgets (sub-probe 0.92->0.50, drop 0.42; completion drop 0.11) and beats the footprint-matched gated dense by Delta_joint +1.58 CI[1.36,1.79] under BOTH judges, collateral KG 5e-5 vs gated 0.290, curve-dominance 1.0. (2) taxonomic_georgia (16009) and taxonomic_jordan (540) = NO_MEANINGFUL_FORGET -- the single-latent ablation CANNOT remove the DISTRIBUTED country sense even at full strength (max_forget_KG 0.065/0.114, sub-probe drop 0.07/0.0, NOOP-identical on 89% of FORGET prompts); KG keeps a CI-excl-0 joint edge (+0.17/+0.15) but it is MECHANICALLY VACUOUS (the absorber barely edits). THIS DIRECTLY EXPOSES that iter-6's KG_BEATS_USUB Georgia headline (+0.561) sat at a near-NOOP operating point. (3) taxonomic_us (846) = NO_MEANINGFUL (co-firing). (4) toxicity_insult (13367) = KG_BEATS_GATED +0.47 but co-firing, excluded from the absorption gate. overall_verdict = SPARSE_SAE_HANDLE_ESTABLISHED, absorption_exceeds_cofiring 1.58>0.37. The month case was dropped (iter-5 homograph month *_data_out.json never materialized on disk).

          - M2'' CONFIRMATORY NAMED-ENTITY HOMOGRAPH SCREEN + GATED DOWNSTREAM [art_ZxVw0e4seBq3]. Of 5 eligible named-entity homographs, 3 are absorption-structured AND form-free-oracle-confirmed -- Amazon (hole 0.61, J 0.048, prec 0.99), Bush (0.79/0.021/1.00), Cook (0.72/0.045/1.00); Apple (0.25) and King (0.42) are NOT structured. Georgia self-check PASSES. Downstream: Amazon = KG_BEATS_GATED_DENSE (median matched KL 0.58, 58% prompts changed, +0.75 CI[0.41,1.08] both judges) = a genuine NAMED_ENTITY_HOMOGRAPH_WIN; Bush = KG_MATCHES_GATED_DENSE (label-free parity); Georgia control = NEAR_NOOP_NO_WIN (corroborates M1''). Notably the named-entity absorber 6846 is a STRONGER handle (max_kg 1.14) than the country absorber (0.064). overall_verdict = SAFETY_ABSORPTION_HOMOGRAPH_CONFINED (demographic null unchanged); secondary_tag = NAMED_ENTITY_HOMOGRAPH_WIN_FOUND.

          - GATED STEERING IS PRIOR ART [art_IlzAiXYWeUYH]. The exact gated-dense operator the paper uses as a control is published: CAST (2409.05907 ICLR-2025 Spotlight), GUARD-IT (2605.12765), GSS (2602.08901, the EXACT h'=h-1(|u^T h|>eps)*v operator), SADI (2410.12299 ICLR-2025). In ALL of them the gate is SUPERVISED. So DENSE-SUB-ABL-GATED is a CONTROL, not a contribution; the SAE-specific value is the TRAINING-FREE, LABEL-FREE DISCOVERY of WHERE to gate, with the absorber's calibrated JumpReLU firing a built-in calibration-free gate (Peng 'Discover-not-Act' 2506.23845). Locked gated-steering cites added; localization-first reposition + one-canonical-Georgia-number clarity fixes supplied.

          WHAT THE ITER-7 REVIEW EXPOSED -- THREE MAJORS THAT GATE PUBLICATION, PLUS THREE MINORS:
            (R1, METHODOLOGY -- new #1 blocker) THE 'DECISIVE' FOOTPRINT-MATCHED GATED DENSE CONTROL IS MIS-TUNED AND STRICTLY WEAKER THAN THE UNGATED DENSE IT WAS MEANT TO STRENGTHEN, INFLATING THE HEADLINE. Verified for 'large': KG util 1.870; GATED util 0.287; UNGATED DENSE-SUB util 0.870; retain-collateral KL KG 5e-5 / GATED 0.290 / ungated SUB 0.021. To reach the matched forget (KL 0.36) WITHIN the 3% footprint, the gated dense is driven to beta=2.97 (over-erasure) which crashes fluency and yields ~14x MORE collateral than the ungated dense at beta=0.65. So footprint-matching HANDICAPS the dense; KG's win vs the STRONGEST dense baseline (ungated DENSE-SUB-ABL) is +1.00 CI[0.79,1.21], NOT the advertised +1.58 vs the handicapped gate. The abstract/title lead with the largest, least-defensible gap. => ITERATION 8 MUST lead with KG-vs-strongest-dense (+1.00 on large), report +1.58-vs-gated only as a robustness check WITH the explicit beta~3 over-erasure caveat (gated collateral 0.29 >> its own ungated 0.021), and ADD A GENUINELY-FAIR GATED CONTROL: gate by the PRECISE d_sub detector (AUC~1.0) with BOUNDED beta<=1. If KG still wins THERE, the sparse-SAE-handle claim is established; if not, the value reduces to label-free DISCOVERY of where to gate.
            (R2, SCOPE -- new #2 blocker) THE POSITIVE EDIT CONTRIBUTION IS n~=1-2 LOAD-BEARING. In the main experiment only first_letter_large is KG_BEATS_GATED; Amazon (+0.75) is from a 'confirmatory, not load-bearing' experiment; insult (+0.47) wins but is excluded as co-firing; Georgia/Jordan/US are nulls. Meanwhile ALL THREE downstream tasks the GOAL explicitly names -- (i) feature-based classification of safety-relevant attributes, (ii) steering with side-effect measurement, (iii) model-diffing -- are delivered as NULLS (no unit out-classifies a dense probe on any task; steering surgical only on 2/5 letters; model-diffing a confound-bounded +0.000 null; safety homograph-confined, no robust win). => ITERATION 8 MUST strengthen the positive base: run gated-controlled edits on the already-discovered structured named-entity absorbers Bush AND Cook, plus additional concentrated homographs from a WIDER entity/spelling vocabulary, TARGETING >=4 INDEPENDENT CONCENTRATED WINS under the fair bounded-beta d_sub-gated control. If the base stays thin or demographic safety attributes genuinely lack absorption structure (as the 2/44 screen indicates), RETARGET the paper headline FULLY to 'training-free auditable LOCALIZATION + EDITING of homograph-polysemy absorption' (ICML primary acceptable), leading with the auditability spine + the homograph-confinement null, with the edit a scoped capability on concentrated features.
            (R3, EVIDENCE -- new #3 blocker) 'THE WIN TRACES TO THE ABSORPTION STRUCTURE THE METHOD DISCOVERS' IS NOT SUPPORTED. The meaningful-forget WINS span BOTH regimes -- large (absorption +1.58) AND insult (CO-FIRING, firing-Jaccard 0.882, no recall hole, +0.47, FOUND BY max-AUC NOT set-cover) -- while the absorption LOSSES (Georgia, Jordan) are DISTRIBUTED senses. So the real predictor of a win is lexical CONCENTRATION (high per-sub-context precision + sparse firing), NOT absorption; a concentrated co-firing latent also beats the gated control, and the set-cover machinery is NOT necessary to find it. The aggregate gate 'absorption_exceeds_cofiring (1.58>0.37)' compares the single INFLATED absorption number against a 2-case co-firing MEAN -- a thin, somewhat circular basis for an absorption-specific claim. => ITERATION 8 MUST REFRAME THE MECHANISM HONESTLY: the edit advantage is a property of a PRECISE/CONCENTRATED latent acting as a sharper conditional gate than a footprint-matched dense projection; absorption is ONE label-free-discoverable SOURCE of such concentration (the absorber marginal attribution drops), but NOT the only one. DROP/heavily-qualify 'traces to absorption structure', state the property the method should select for (per-sub-context PRECISION x sparse firing = concentration), and run the DECISIVE ABLATION: does the anchored set-cover discovery add ANYTHING over a simple 'pick the single most precise latent firing on the target sub-context' max-precision selector? If not, the method identity is label-free precise-concentrated-latent discovery, and the set-cover/(1-1/e) framing is motivation only.
            (R4, CLARITY -- minor) The two 'footprint-matched gated dense' controls are NOT the same operator across experiments: in [art_Cgk9ETiZfvtl] the gate is calibrated so the GLOBAL firing fraction over a neutral pool equals f_kg (~3%, tau~101); in [art_ZxVw0e4seBq3] (Amazon/Bush) it is 'footprint_match_clamped' on the X-POSITIVE firing rate clamped to 0.95 (gate_fire_rate_X ~0.947). The headline aggregates a 3%-global-footprint comparison (large) with a 95%-X-rate comparison (Amazon). => ITERATION 8 MUST UNIFY the gate-calibration definition into ONE well-defined operator across all cases (or state any per-case clamp explicitly in the edit table + appendix with justification).
            (R5, RIGOR -- minor) The meaningful-forget proof for the load-bearing 'large' case is THIN: the completion-drop CI is over only n=4 hand probes (drop 0.072, CI[0.017,0.117]) and the sub-probe drops only to 0.50 (partial, not strong, forget); the OR-verdict relies on two instruments that DISAGREE sharply at the matched point (completion favors GATED 1.08>>0.07; sub-probe favors KG 0.42>>0.0), undercutting 'matched on forgetting'. => ITERATION 8 MUST expand the completion-probe set to ~20-50 templated probes per case, report the matched-forget comparison on BOTH instruments side by side, discuss why next-token-KL matching does not equalize behavioral forgetting, and MATCH operators on a BEHAVIORAL measure (sub-probe drop or completion accuracy) rather than next-token KL.
            (R6, NOVELTY -- minor) The 'single-absorber discovery via anchored max-coverage set-cover' framing OVERSELLS: the procedure is effectively k=1 for every reported win, so the (1-1/e) max-coverage guarantee dresses up a step that reduces to 'pick the most precise latent covering the anchor's recall hole'; the C-track ties weak baselines and the multi-member unit only ADDS collateral, so the distinctive machinery is largely INERT in load-bearing results, and the discovery step is incremental over Chanin's diagnostic used label-free. => ITERATION 8 MUST either demonstrate a case where multi-member grouping (k>1) or the set-cover objective beyond k=1 measurably helps a downstream outcome, OR trim the framing to 'anchored recall-hole-guided PRECISION SELECTION of a single absorber' and present set-cover/(1-1/e) as MOTIVATION only; and explicitly sharpen the delta vs Chanin's diagnostic (what the label-free anchor + recall-hole + precision-gate buys = no supervised probe/logit, form-free, surfaces the absorber marginal attribution drops).

          THE ITERATION-8 MANDATE (the two NEW load-bearing pieces -- the genuinely-fair bounded-beta d_sub-gated control + an expanded/concentrated positive base -- make or break the edit headline; the mechanism reframe + de-inflation are required; nothing else gates):
            (M1''' = NEW LOAD-BEARING #1 -- DE-INFLATE + GENUINELY-FAIR GATED CONTROL + UNIFIED OPERATOR) Re-report the edit comparison LEADING WITH KG-ABL vs the STRONGEST dense baseline (ungated DENSE-SUB-ABL: large +1.00 CI[0.79,1.21]); report +1.58-vs-footprint-gated ONLY as a robustness check with the explicit over-erasure caveat. ADD DENSE-SUB-ABL-GATED-FAIR = u_sub gated by the PRECISE d_sub detector (AUC~1.0) with BOUNDED beta<=1 (NOT a global-footprint threshold that forces beta~3 over-erasure). UNIFY the gate-calibration into ONE operator across large/Amazon/Bush (or document the per-case clamp in-table). Keep both judges + deterministic human-proxy + full operating-point disclosure (both max_forget ceilings, NOOP-identical fractions, full collateral-vs-forget curves). FORK: (a) KG-ABL beats BOTH the strongest ungated dense AND the fair bounded-beta d_sub-gated control (joint CI excl 0, both judges) at meaningful forget => SPARSE-SAE-HANDLE established; (b) the fair gated dense matches/closes the gap => contribution is label-free DISCOVERY of where to gate (gating is prior art); (c) near-NOOP everywhere for the feature => scope to selective low-collateral PARTIAL suppression.
            (M2''' = EXPAND THE POSITIVE BASE OR RETARGET -- NEW LOAD-BEARING #2) Run the fair gated-controlled edit on the already-discovered structured named-entity absorbers Bush and Cook and on additional CONCENTRATED homograph/spelling tokens from a wider vocabulary, TARGETING >=4 INDEPENDENT CONCENTRATED WINS (large + Amazon are the existing 2). If >=4 land, the editing-of-homograph-polysemy-absorption contribution stands on a broader base. If it stays thin, LEAD the paper with the auditability/localization SPINE + the safety-homograph-confinement NULL as the finding, edit as a scoped capability, and RETARGET framing/venue to localization+editing of homograph-polysemy absorption.
            (M3''' = MECHANISM REFRAME -- CONCENTRATION/PRECISION, NOT ABSORPTION) State plainly: the edit advantage is a property of a PRECISE/CONCENTRATED latent acting as a sharper conditional gate than a footprint-matched dense projection; absorption is one label-free-discoverable source of concentration; the set-cover machinery is NOT necessary for the edit win (insult was found via max-AUC). Run the DECISIVE ABLATION: KG-ABL vs an edit through the SINGLE MOST PRECISE latent firing on the target sub-context (max-precision selector, no set-cover) -- does the discovery add anything over max-precision? Report what property to select for and the answer.
            (M4''' = RIGOR -- meaningful-forget proof) Expand to ~20-50 templated completion probes per case; report BOTH instruments (completion-drop AND sub-probe-drop) side by side; match operators on a BEHAVIORAL forget measure, not next-token KL; discuss the instrument disagreement.
            (M5''' = METHOD-IDENTITY / NOVELTY TRIM) Reframe to 'anchored recall-hole-guided PRECISION SELECTION of a single absorber'; present set-cover/(1-1/e) as MOTIVATION only; sharpen the explicit delta vs Chanin's supervised diagnostic; demote multi-member grouping + C-track to secondary/exploratory (already shown the single absorber WINS and multi-member ADDS collateral).
            (M6 = CARRIED INTEGRITY + REPOSITION) Lead with 'training-free auditable localization (+ editing) of homograph-polysemy absorption'; reliability gain = LOCALIZATION/AUDITABILITY not classification (no SAE unit out-classifies a dense probe on any task). Safety null is the SETTLED capping limitation (2/44, both homographs) [art_yAQgbq5Wgymx]; named-entity 3/5 confirmatory [art_ZxVw0e4seBq3]. Carry: selectivity divide-by-epsilon corrected (722x/676x n=4; 16k/65k comparably surgical) [art_w7p8du2N1f0Y]; router demoted (prospective Wilson includes 0.5; 3/64 entities, months only) [art_F_-HUhl0NR_i]; 22 distinct holes / mean 1452x median 1262x / rho 0.90 within-taxonomic; random SINGLE-latent control; numeric below-gate; cross-dictionary 65k full / layer-9 partial [art_4L1MZxvWYlGd]; gated-steering prior-art + locked venues [art_IlzAiXYWeUYH]. Strip iteration/rebuttal/infra scaffolding.

          RE-DESIGNATED HEADLINE (auditable-localization-first; the edit win is REAL but NARROW, DE-INFLATED, and CONCENTRATION-driven). On a FROZEN public SAE, interventional grouping by co-response to content counterfactuals is a TRAINING-FREE, LABEL-FREE DISCOVERY PROCEDURE that surfaces the single PRECISE sub-context latent a marginal-attribution ranking silently drops -- in the absorption regime this IS the absorber -- plus a feature-level KNOWLEDGE GRAPH whose edges carry MEASURED, localized repair utility (a KG-named absorber added to a suppressed parent recovers its recall hole, beating a random SINGLE-latent control; 22 distinct holes survive FDR across spelling/taxonomic/numeric; replicates on a 4x-wider SAE with MORE absorption). The EDIT capability: ablating that precise, sparsely-firing latent through its OWN firing gives strictly lower within-hierarchy collateral than a dense baseline AT A FORGET LEVEL WHERE IT MEANINGFULLY FORGETS -- but ONLY where the targeted feature is LEXICALLY CONCENTRATED (first-letter spelling 'large'; named-entity homograph 'Amazon'), and the DEFENSIBLE magnitude is the +1.00 win vs the STRONGEST (ungated) dense, not the +1.58 vs a footprint-matched gate handicapped into beta~3 over-erasure. The win predictor is the latent's PRECISION/CONCENTRATION, NOT absorption per se: a concentrated CO-FIRING latent (insult) also wins, and the absorption LOSSES (Georgia/Jordan) are DISTRIBUTED senses the single latent cannot meaningfully forget. Because gating an edit by a sparse detector is ESTABLISHED PRIOR ART (CAST/GSS/GUARD-IT/SADI, all SUPERVISED), the SAE-specific value is the LABEL-FREE DISCOVERY of WHERE to gate; the OPEN, GATING question iteration 8 must close is whether KG-ABL beats a GENUINELY-FAIR bounded-beta d_sub-gated dense control AND whether the set-cover discovery beats a simple max-precision selector. SAFETY-RELEVANT absorption does NOT exist beyond homographs (2/44 safety groups, both homographs, no robust safety win -- the SETTLED ceiling and headline limitation); absorption is NARROW (homograph-polysemy entity tokens + first-letter spelling; 3/5 named-entity homographs structured; 0/28 professions; 3/64 homograph entities); the router is derivation-perfect but out-of-sample-UNVALIDATED; the durable value is AUDITABLE, EDITABLE, LABEL-FREE-DISCOVERED, REGIME-TARGETED LOCALIZATION of homograph-polysemy absorption.

          PRIMARY ENDPOINT (re-designated; the two NEW pieces are load-bearing).
            (a) DE-INFLATED, GENUINELY-FAIR-GATED, CONCENTRATION-ATTRIBUTED EDIT TEST (NEW LOAD-BEARING, M1'''+M3'''): KG-named single-absorber gated ablation vs (i) the STRONGEST ungated dense (lead number) and (ii) a bounded-beta d_sub-PRECISE-gated dense control, at matched MEANINGFUL forget, on a UNIFIED gate operator, with both judges + the full operating-point curve + a behavioral-match forget proof. A WIN over the fair bounded-beta gated control at meaningful forget = the strong contribution; a MATCH = label-free where-to-gate discovery; and the win must be shown to track CONCENTRATION/PRECISION (with the max-precision-selector ablation) rather than asserted to track absorption structure.
            (b) EXPANDED POSITIVE BASE (NEW LOAD-BEARING, M2'''): >=4 independent CONCENTRATED gated-controlled edit wins (large, Amazon + Bush/Cook/wider-vocab) OR an explicit retarget to localization+editing-of-homograph-polysemy-absorption with the spine + safety-null leading.
            (c) AUDITABILITY/LOCALIZATION SPINE (ACHIEVED, honestly re-counted): 22 distinct-hole FDR repairs over a random single-latent control [art_sxwT7hK6YFEA, art_w7p8du2N1f0Y]; sparse-gated surgical edits with corrected selectivity [art_0CZwPjG2YMCf]; member-labeling beats shuffle null; cross-dictionary 65k full / layer-9 partial [art_4L1MZxvWYlGd].
            (d) SAFETY SCOPE (SETTLED NULL, M6): safety absorption is homograph-confined (2/44, both homographs; no robust safety win); named-entity 3/5 confirmatory [art_yAQgbq5Wgymx, art_ZxVw0e4seBq3].
            (e) ROUTER: recall-hole-alone reproduces on derivation (bal-acc 1.0) but is OUT-OF-SAMPLE-UNVALIDATED (homograph prospective Wilson includes 0.5) -- DEMOTED to exploratory diagnostic [art_F_-HUhl0NR_i].
          SUPPORTING (strengthen, do not gate): within-SAE set-cover/precision selection where the signature holds (first-letter I,D; taxonomic Georgia); member-labeling above null; the steering demo (L,D); the homograph breadth count (months: March/June/February). The headline NO LONGER depends on classification beating dense, on multi-member grouping beating single absorbers, on the router being validated, on a safety win existing, OR on the inflated +1.58-vs-footprint-gated number.

          THE DISCOVERY ALGORITHM (specification unchanged; now FRAMED as anchored recall-hole-guided PRECISION SELECTION of a single absorber; set-cover/(1-1/e) is MOTIVATION only). STEP 1 cover-based eligibility (content-responsive above a shuffle null; firing-precision>=0.7; covers>=1 sub-context). STEP 2 C-TRACK (splitting, SECONDARY/EXPLORATORY): positive-Spearman soft-threshold affinity (beta=6, WGCNA) -> Leiden RBConfiguration; resolution by bootstrap-ARI stability; ties weak baselines so reported secondary only. STEP 3 K-TRACK (absorption, the DISCOVERY step, effectively k=1 for the wins): ANCHOR = argmax cover-set chosen WITHOUT the diagnostic, with the UNSUPERVISED FIRING-FLOOR PARENT-VALIDATION (anchor must fire on held-out corpus above ~5%); HOLES = parent's uncovered pairs; greedily add mutually-exclusive (firing-Jaccard<0.1), PRECISE (>=0.7, held-out-gated) latents covering holes with marginal-gain>=0.05 CI excluding 0; PRECISION-GATED / precision-WEIGHTED objective (Georgia selects 16009 prec .955, not 4697 prec .35). The DEMONSTRATED value of this machinery is PROPOSING the single PRECISE sub-context latent marginal attribution drops -- iteration 8 must test (M3''') whether this beats a simple MAX-PRECISION selector, since the edit win is concentration-driven and a concentrated co-firing latent (insult) was found WITHOUT set-cover. Multi-member units ADD collateral on the downstream edit, so they are reported SECONDARY.

          SAE-LATENT FIRING-STRUCTURE ROUTER (screening DIAGNOSTIC, derivation-perfect but out-of-sample-UNVALIDATED; RECALL-HOLE-PRIMARY). One forward pass: encode, identify the firing-floor-validated content-responsive parent, find per-sub-context detectors, report (i) parent per-sub-context recall holes and (ii) detector-vs-parent positive-only firing-Jaccard. RULE: predict absorption-regime iff the parent has a recall HOLE (>~0.78); balanced-acc 1.0 on 12 derivation concepts; on the 34-entity homograph-prospective expansion the discriminative absorption stratum's Wilson CI INCLUDES 0.5 -> EXPLORATORY DIAGNOSTIC. NOTE the router predicts the ABSORPTION REGIME, NOT the EDIT-WIN: the edit win tracks lexical CONCENTRATION (insult co-fires yet wins; Georgia/Jordan absorb yet lose), an orthogonal axis the router does not capture. Co-firing (toxicity, US aggregate, the 42 no-hole safety groups) => supervised attribution wins for CLASSIFICATION and CCRG grouping does not help, but a concentrated co-firing latent can still be a sharp EDIT gate.

          BASELINE GLOSSARY (matched baselines primary; the decisive M1''' comparators are the STRONGEST ungated dense AND a fair bounded-beta d_sub-gated dense). (a) best raw single latent; (b)/(c) observational co-activation/decoder clusters COUNT-MATCHED to k; (d) counterfactual diff-of-means; (e) raw-residual probe; (f) WHOLE-PARENT LEACE/diff-of-means erasure (SECONDARY 'naive over-shoot' reference); (g) SCR/TPP oracle pool; (h) count-and-pool-matched SCR/TPP probe; (i) unmatched diff-of-means; (j) oracle group-DRO; (k) label-free group-inference; (RE-k) random-eligible-k floor; (S-rec)/(S-prec)/(S-mag) non-random label-free selectors -- S-prec / a SINGLE-MAX-PRECISION selector is now LOAD-BEARING for the M3''' ablation (does set-cover beat max-precision?). DECISIVE EDIT COMPARATORS: u_sub (DENSE-SUB-ABL, ungated continuous) = the STRONGEST dense, the LEAD comparator (KG beats it by +1.00 on large); u_sub-footprint-GATED (DENSE-SUB-ABL-GATED, iter-7) = the MIS-TUNED control (beta~3 over-erasure), reported as robustness with caveat; and the NEW u_sub-d_sub-PRECISE-bounded-beta-GATED (DENSE-SUB-ABL-GATED-FAIR) = the genuinely-fair conditional-dense control, the load-bearing iter-8 piece.

          NON-SPELLING / HOMOGRAPH TESTBED (HOMOGRAPH-POLYSEMY ABSORPTION; CONCENTRATED-vs-DISTRIBUTED is the edit-relevant axis). Absorption recurs on HOMOGRAPH/POLYSEMOUS tokens whose general parent is suppressed -- taxonomic Georgia (hole .80) + Jordan (descriptive, hole .71); United States CO-FIRING; 0/28 professions; of 64 homograph entities only 3 months structured; of 5 named-entity homographs 3 structured (Amazon/Bush/Cook); of 44 safety groups only 2 homographs (white, straight). NEW axis from the edit test: a structured absorber is an EDITABLE handle only if its targeted sense is LEXICALLY CONCENTRATED (spelling 'large', entity 'Amazon' meaningfully forget; DISTRIBUTED country senses Georgia/Jordan do NOT). Numeric = below-gate (digit cosine 0.876<0.9). A non-SAE dense probe matches/beats the unit on ALL classification.

          SCOPE AND VALUE PROPOSITION. The defensible contribution is: (1) a TRAINING-FREE, LABEL-FREE DISCOVERY PROCEDURE that surfaces the single PRECISE sub-context latent marginal attribution drops (the absorber where absorption exists), with a MEASURED, EDITABLE feature-KG (recall-hole recovery beating a random single-latent control; sparse-gated surgical edits) plus human/LLM-auditable members, REPLICATING across SAE dictionaries; (2) an a-priori RECALL-HOLE screening DIAGNOSTIC (derivation-perfect, out-of-sample-unvalidated) for when grouping helps CLASSIFICATION; (3) a SPARSE-GATED EDIT capability whose advantage over a dense baseline at MEANINGFUL forget is REAL but driven by latent CONCENTRATION/PRECISION (large +1.00 vs strongest dense; Amazon +0.75) -- NARROW (n~=2, expand to >=4 in iter-8) and bounded by the genuinely-fair bounded-beta d_sub-gated control. The method does NOT out-classify a strong dense probe; toxicity is a clean co-firing CLASSIFICATION negative (yet a concentrated co-firing EDIT win); SAFETY absorption does NOT exist beyond homographs (settled). HEADLINE = auditable, label-free-discovered, regime-targeted LOCALIZATION (+ EDITING on concentrated features) of homograph-polysemy absorption; classification is SUPPORTING and within-SAE; the sparse-gated edit is a CAPABILITY whose strength is bounded by the fair gated-dense control and attributable to concentration.

          HONEST NEGATIVES (each publishable): the iter-7 +1.58-vs-gated headline is INFLATED -- the footprint-matched gate is mis-tuned (beta~3 over-erasure, 14x more collateral than its own ungated form), the defensible win is +1.00 vs the strongest ungated dense, and a genuinely-fair bounded-beta d_sub-gated control is not yet run; the positive edit base is n~=2 (large, Amazon); the win predictor is CONCENTRATION not absorption (insult, a co-firing latent found by max-AUC, also wins; Georgia/Jordan absorb but lose), so the set-cover machinery may be inert vs a max-precision selector; iter-6's Georgia 'win' (+0.561) sat at a near-NOOP operating point (now retired); the two gated controls are DIFFERENT operators across experiments (3%-global-footprint vs 95%-X-rate clamp); the meaningful-forget proof is thin (n=4 probes, partial sub-probe drop, instruments disagree at the matched point); gating is established prior art (CAST/GSS/GUARD-IT/SADI), so the SAE-specific value is where-to-gate discovery; unit out-classifies NO non-SAE dense probe on any task; safety absorption is homograph-confined (2/44, no robust win); 0/28 professions; 3/64 homograph entities; the router is at chance out-of-sample; cross-dictionary replicates at 4x width but only PARTIALLY across a layer; the 65k 3.7e6 selectivity was a divide-by-epsilon artifact (16k/65k comparably surgical); the headline rests on a single primary LLM judge (second judge corroborates); multi-member grouping ADDS collateral; the C-track ties weak baselines; numeric is below-gate; model-diffing a confound-bounded null; steering surgical only on L,D. A clean iter-8 result where the FAIR bounded-beta gated dense matches KG = 'the value is label-free discovery of where to gate, not an SAE-specific edit advantage' and is itself publishable; near-NOOP-everywhere for a feature = scope to 'selective low-collateral partial suppression'.

          MOTIVATION (substance unchanged). Single SAE latents are unreliable units: feature absorption (Chanin 2409.14507, NeurIPS 2025), splitting, hedging (2505.11756), and 'SAEs Do Not Find Canonical Units' (ICLR 2025) converge on no single latent reliably tracking a concept; AxBench (ICML 2025) and DeepMind's negative report show plain diff-of-means beats raw-latent SAE methods, and Farrell (2410.19278) shows multi-feature SAE unlearning has side-effects >= RMU -- so any SAE method must clear strong dense baselines AND, for the edit, BOTH the strongest ungated dense AND a fair bounded-beta gated dense direction. Absorption is the regime where OBSERVATIONAL signals break by construction and MARGINAL-ATTRIBUTION selection silently drops the absorber; anchored recall-hole-guided precision selection recovers it. But the iter-7 edit test shows the EDIT advantage is about a PRECISE/CONCENTRATED latent acting as a sharp conditional gate -- absorption is one label-free source of such concentration, not the cause of the edit win -- which is why iteration 8 must isolate concentration/precision from absorption and discovery from max-precision. The method positions against the 'use SAEs to DISCOVER, not to ACT' thesis (Peng 2506.23845): CCRG discovers the sub-context handle; whether ACTING through it beats a FAIR gated dense direction is the load-bearing open question, and gating itself is established prior art.

          SUCCESS CRITERIA. METHOD CONFIRMED iff: (LOAD-BEARING) (M1'''+M3''') the KG-localized sparse-gated single-absorber edit BEATS (joint CI excl 0 under two judges) the STRONGEST ungated dense AND a GENUINELY-FAIR bounded-beta d_sub-gated dense control at a forget level where a behavioral-match delta confirms MEANINGFUL forgetting, with the win shown to track CONCENTRATION/PRECISION (max-precision-selector ablation) and the gate a UNIFIED operator; AND (M2''') the positive base reaches >=4 independent concentrated wins OR the paper is retargeted to localization+editing with the spine + safety-null leading; AND the auditability/localization spine holds (22 distinct holes, random single-latent control, corrected selectivity, cross-dictionary 65k full / layer-9 partial); AND the safety null is reported as the capping scope. SUPPORTING (strengthen, do not gate): within-SAE precision/set-cover selection (Georgia, I, D); member-labeling above null; the recall-hole router on derivation; the steering demo (L,D); the homograph breadth count. HONEST NEGATIVES are reportable and cap-but-do-not-sink: a fair gated dense matching KG (=> contribution is label-free where-to-gate discovery), the set-cover failing to beat a max-precision selector (=> method is precise-latent discovery), near-NOOP forget for a feature (=> partial suppression), safety absorption absent (settled), router-at-chance, layer-conditional replication, single-absorber-not-grouping attribution, numeric unconfirmed, toxicity co-firing CLASSIFICATION negative, no classification win over dense on any task.
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
  Same homograph-absorption frame; edit win de-inflated, reattributed to concentration not absorption; fair gated control.
_confidence_delta: decreased
_key_changes:
- >-
  Recorded iter-7 execution of M1'' (gated-dense control + honest forget): KG-ABL beats the footprint-matched gated dense
  at MEANINGFUL forget ONLY on concentrated features -- first_letter large +1.58 and named-entity Amazon +0.75 (both judges);
  Georgia/Jordan NO_MEANINGFUL_FORGET (distributed sense, max_kg 17-30x smaller, NOOP-identical on 89%), directly exposing
  iter-6's Georgia +0.561 as a near-NOOP win (now retired) [art_Cgk9ETiZfvtl, art_ZxVw0e4seBq3].
- >-
  DE-INFLATION (reviewer R1): the +1.58-vs-gated headline is inflated -- the footprint-matched gate is mis-tuned (driven to
  beta~2.97 over-erasure, ~14x more collateral than its own ungated form). The defensible lead number is KG vs the STRONGEST
  ungated dense = +1.00 CI[0.79,1.21] on large; +1.58 demoted to a caveated robustness check.
- >-
  NEW LOAD-BEARING control (R1): add DENSE-SUB-ABL-GATED-FAIR = u_sub gated by the precise d_sub detector (AUC~1.0) with BOUNDED
  beta<=1 -- the genuinely-fair conditional-dense control; KG must beat it to establish the sparse-SAE-handle claim.
- >-
  MECHANISM REFRAME (R3): the edit-win predictor is latent CONCENTRATION/PRECISION, NOT absorption -- a concentrated co-firing
  latent (insult, found by max-AUC not set-cover) also wins, and absorption losses (Georgia/Jordan) are distributed. Dropped
  'the win traces to absorption structure'; added the decisive ablation 'does set-cover discovery beat a simple max-precision
  selector?'.
- >-
  SCOPE (R2): the positive edit base is n~=2 (large, Amazon). NEW LOAD-BEARING mandate to reach >=4 independent concentrated
  wins (Bush, Cook, wider vocab) OR retarget the paper fully to 'training-free auditable localization + editing of homograph-polysemy
  absorption' (ICML acceptable), leading with the spine + the settled safety null.
- >-
  CLARITY (R4): noted the two gated controls are DIFFERENT operators (large = 3%-global-footprint tau~101; Amazon/Bush = 95%-X-rate
  clamp); iter-8 must unify into one well-defined gate operator.
- >-
  RIGOR (R5): the meaningful-forget proof is thin (n=4 probes, partial sub-probe drop 0.92->0.50, instruments disagree at
  the matched point); iter-8 must expand to ~20-50 probes, report both instruments side by side, and MATCH operators on a
  behavioral measure not next-token KL.
- >-
  NOVELTY (R6): trimmed the set-cover/(1-1/e) framing to MOTIVATION; method identity reframed to 'anchored recall-hole-guided
  PRECISION SELECTION of a single absorber'; multi-member grouping + C-track demoted to secondary (they add collateral / tie
  weak baselines); sharpen delta vs Chanin's supervised diagnostic.
- >-
  Recorded gated-steering PRIOR ART (CAST/GSS/GUARD-IT/SADI, all supervised) [art_IlzAiXYWeUYH]: gating is a control not a
  contribution; SAE-specific value = label-free DISCOVERY of where to gate.
- >-
  Confidence DECREASED: the iter-7 gate returned a real positive but it is narrower (n~=2), smaller (+1.00 not +1.58), and
  differently-caused (concentration not absorption) than reported, while all three goal-named downstream tasks (safety classification,
  steering, model-diffing) remain nulls -- narrowing the durable contribution to auditable localization + concentrated-feature
  editing of homograph-polysemy absorption.
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
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_1/gen_art/gen_art_research_1
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
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_1/gen_art/gen_art_research_2
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
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
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
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_1/gen_art/gen_art_dataset_2
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
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_1/gen_art/gen_art_dataset_3
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
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_1/gen_art/gen_art_dataset_4
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
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_2/gen_art/gen_art_experiment_1
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
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_2/gen_art/gen_art_experiment_2
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
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_2/gen_art/gen_art_experiment_3
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
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_2/gen_art/gen_art_dataset_1
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
  relation_type: uses
  relation_rationale: >-
    Encodes the first-letter spelling testbed pairs/corpus through the frozen SAE for the RE-k re-run.
- id: art_RidEJtBC7gPT
  label: method
  relation_type: uses
  relation_rationale: >-
    Reuses the dossier's two-track pipeline and baselines; adds RE-k, AUC-diff CIs, verdict reconciliation.
- id: art_I2MrezW41iQo
  label: diagnostic
  relation_type: uses
  relation_rationale: Uses the form-free absorption diagnostic as the non-circular E1 oracle.
- id: art_YwjLYapklnVk
  label: surface-control
  relation_type: uses
  relation_rationale: Admission surface-invariance null computed on the 1,700-pair surface superset.
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
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_3/gen_art/gen_art_experiment_1
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
  relation_type: uses
  relation_rationale: >-
    Re-analyzes the numeric+taxonomic testbed encodings for RE-k/RE-k-anchored selection isolation.
- id: art_RidEJtBC7gPT
  label: method
  relation_type: uses
  relation_rationale: >-
    Uses the dossier's K-track and marginal-attribution (g)/(h) baselines on non-spelling slices.
- id: art_I2MrezW41iQo
  label: diagnostic
  relation_type: uses
  relation_rationale: >-
    Uses the form-free diagnostic to score KG edges; numeric edges fail corroboration (top-1 0.0).
title: >-
  Non-Spelling SAE Absorption: RE-k Selection-Isolation, AUC-Diff CIs, Router Inputs
summary: |-
  Iteration-3 re-analysis of the executed iter-2 non-spelling SAE-absorption experiment. It reuses the frozen Gemma-Scope layer_12/width_16k SAE encodings (cached CSR latents + fp16 residuals) and the same two-track K-track unit/anchor/(g)/(h)/dense-probe, then adds the three iter-3-mandate analyses on the NON-SPELLING slices (taxonomic countries; numeric quantity types). Runs CPU-only via cache reuse (the RTX 5090 sm_120 is unsupported by torch 2.6.0+cu124, so the script auto-falls-back to CPU; the GPU re-encode path exists only for a cache miss, which never occurs). VERDICT = taxonomic_selection_established.

  M1 (selection isolation): adds a RANDOM-ELIGIBLE-k pool baseline (RE-k) and an anchor-fixed variant (RE-k-anchored) that separate the two-track set-cover SELECTION from cover-based eligibility+pooling. Rule selection_established(s) = (unit AUC > RE-k-anchored 95th pct) AND (paired AUC-difference CI vs RE-k-anchored mean excludes 0). TAXONOMIC Georgia: True (unit-RE-k-anchored = +0.099 [+0.085,+0.113], unit at 100th pct of draws). NUMERIC integer: False (unit-RE-k-anchored = +0.029 [-0.006,+0.062] includes 0) -> non-spelling numeric is eligibility+pooling, not set-cover selection.

  M2 (AUC + AUC-difference CIs): point AUC plus stratified paired-bootstrap AUC-DIFFERENCE CIs (B=10,000) for unit vs (g)/(h)/RE-k/RE-k-anchored/dense-probe on the defining absorbed slices (Georgia, integer), all 20 eligible countries / 8 numeric sub-contexts, and descriptive subs (Jordan, United States, decimal, year), replacing iter-2's mislabelled matched-recall-accuracy deltas. Georgia headline (pos=150 Georgia tokens vs 2100 taxonomic negatives): unit AUC=0.989, g=0.418, h=0.383 (below chance = absorption signature), RE-k=0.906, RE-k-anchored=0.890, dense-probe=1.000; unit-h=+0.606 [+0.570,+0.642] confirms a genuine AUC-rank effect (the R1 honesty fix), unit-dense=-0.011 [-0.015,-0.008] (the non-SAE probe slightly edges the unit but the unit is the best SAE detector). A comparison-matched Youden accuracy table is added so NO baseline is forced to predict-all (the artefact that made (h) look degenerate in iter-2).

  M7/M4 (router inputs): per-hierarchy firing-Jaccard(parent, top per-sub-context detector) on positives + parent per-sub-context recall holes + per-slice form-free KG top1, emitted as inputs for the M4 prediction-vs-outcome router table. absorption_type (parent hole>0.5 AND Jaccard<0.10) is True for exactly two countries -- Georgia (J=0.059, KG top1=1.0) and Jordan (n=124<150 descriptive, KG top1=0.95), the ambiguous homographs where the parent country-latent has a genuine recall hole; all other countries have parent_recall_hole~=0. Numeric integer router J=0.256 (co-firing, not mutually exclusive), KG mean top1=0.0. M7 framing: taxonomic = diagnostic_corroborated LEAD; numeric = suggestive_diagnostic_unconfirmed (dense-probe AUC=1.000 dominates, KG top1=0.0) and is NOT promoted.

  Deliverables: method.py (single pipeline = iter-2 core + iter-3 phases D-H), method_out.json / full|mini|preview_method_out.json (exp_gen_sol_out schema, PASSED, 8.5MB < 100MB; metadata.per_hierarchy carries auc_point, auc_diff_ci, rek_distribution, selection_established, youden tables, router+regime, generalization_status, honest_notes; datasets[].examples carry per-row diagnostic predictions predict_{unit,anchor,g,h,dense_probe,rek}), results/ (partial_{taxonomic,numeric}_iter3.json, results.json, auc_diff/router/sliced_recall CSVs, arrays npz), pyproject.toml (21 pinned deps), RESULTS_SUMMARY.md. Downstream GEN_PAPER_TEXT consumes this for the M1/M2/M7 non-spelling tables: taxonomic Georgia is the established selection win (and the only AUC-rank win that survives the anchor-fixed random control), numeric is honestly demoted to suggestive, and the router rows feed the M4 absorption-vs-splitting regime map.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_3/gen_art/gen_art_experiment_2
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
  relation_type: uses
  relation_rationale: >-
    Uses first-letter corpus windows for the KG-guided recall-repair held-out evaluation.
- id: art_t2uUbjSwpd3t
  label: dataset
  relation_type: uses
  relation_rationale: Uses taxonomic corpus windows (Georgia/Jordan/US) for the repair loop.
- id: art_RidEJtBC7gPT
  label: method
  relation_type: uses
  relation_rationale: >-
    Reads/re-derives the dossier's two-track units and KG for the auditability measurement.
- id: art_I2MrezW41iQo
  label: diagnostic
  relation_type: uses
  relation_rationale: >-
    Uses diagnostic-corroborated absorbers as KG repair candidates and the (k) localization check.
title: >-
  Measured Auditability of Two-Track CCRG SAE Units: KG Repair Loop + LLM Member-Labeling
summary: |-
  Executes the two previously-dropped, now load-bearing M5 AUDITABILITY results for the two-track Counterfactual Co-Response Grouping (CCRG) units on a frozen Gemma-Scope L12/16k JumpReLU SAE (gating cosine 0.919, token localization exact, hidden_states[13]). Canonical units/KG are READ from the deterministic iter-2 outputs (first-letter exp_1, taxonomic exp_3) and re-derived as a cross-check (responsive set 682 vs iter-2 684; anchor 3792 matches). It converts the iter-2 'we emit a 70-edge graph' ASSERTION into MEASURED numbers.

  M5a KG-GUIDED REPAIR LOOP (load-bearing): for each under-served sub-context (recall hole where the anchor/parent latent goes silent) the KG names a covering absorber; we ADD it to the anchor (max-pool) and measure recall recovery on HELD-OUT corpus windows (selection split disjoint from eval split: taxonomic train->diagnostic; first-letter folds 0-3 -> fold 4) vs a control that adds the full population of other content-responsive latents, with a paired-bootstrap CI (B=10,000). Result: 8 measured successful repairs whose KG-minus-random gain CI excludes 0 -- taxonomic Georgia (anchor recall 0.20 -> 1.00, gain 0.80, 99.4th pct vs random, CI [0.70,0.82]), Jordan (0.29 -> 1.00/0.935), United States (0.77 -> 0.99/0.97), plus first-letter O/'our' and D/'day' (0.00 -> 1.00). BOTH the K-track edge (4697/9339/8442) and the higher-precision diagnostic-corroborated absorber (16009/540/846) are significant. Honest negatives: first-letter L ('list','line',...) and T ('type','things',...) candidate words tie the random-addition control (too few held-out windows / no extra localization) -- reported verbatim.

  M5a(k) LOCALIZATION-FAILURE CHECK: the label-free group-inference probe (k) (JTT: ERM -> upweight hardest/error set -> retrain) yields a dense hyperplane whose decoder-projection argmax is the PARENT 3792 (top |cos|=0.44, does not dominate; KG absorbers rank 2269/58/5964, never argmax). (k) classifies the holes (recall 1.0 on Georgia/Jordan/US) but exposes NO addable per-sub-context latent -- whereas the KG names exactly one. Country is linearly separable so the JTT error set is empty and we upweight the lowest-margin 20%; the structural conclusion is unchanged.

  M5b LLM-JUDGE MEMBER-LABELING (load-bearing): 67 unit members (anchor + absorbers across taxonomic + L/O/T/D) each described by logit-lens top-10 tokens + top-5 raw activating corpus windows with the sub-context label WITHHELD (non-leaky); anthropic/claude-haiku-4.5 (temp 0, forced-choice) names the sub-context. Agreement 0.716 vs shuffle null 0.090 (analytic chance 0.087); gap 0.627, bootstrap CI [0.522,0.731] excludes 0. Per-role: absorbers 0.76 accuracy, anchors 0.20 (judge over-specifies the parent's mixed-country/word windows -- honest caveat). 84 calls, 0 errors, total LLM spend $0.047 (<<$3 target).

  VERDICT: kg_utility_measured=True, member_labeling_above_null=True, replaces_iter2_assertion=True. Output method_out.json (exp_gen_sol_out-schema-valid, full/mini/preview all <100MB) stores per-sub-context repair stats (recall_anchor, recall_anchor_plus_kg, gain_kg, kg_percentile_vs_random, random_gain percentiles, paired_bootstrap_CI, k-track + diagnostic variants, honest_negatives), the (k) decoder-projection check, full member evidence + judge choices + scoring (gap CI, per-role accuracy, confusion), and a datasets block (kg_repair_loop rows; member_labeling rows with predict_judge) for downstream solution evaluation. This provides the paper's auditability section: the emitted feature knowledge-graph carries MEASURED localization utility and the cluster-level units are human/LLM-auditable, while example-reweighting baselines provide no addable per-feature unit.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_3/gen_art/gen_art_experiment_3
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
  relation_type: uses
  relation_rationale: Encodes spelling concepts as firing-disjoint derivation points for the router.
- id: art_t2uUbjSwpd3t
  label: dataset
  relation_type: uses
  relation_rationale: Encodes numeric/taxonomic concepts as router derivation points.
- id: art_8QO7pl6Pd8UQ
  label: dataset
  relation_type: uses
  relation_rationale: Encodes toxicity concepts as the co-firing pole of the router.
- id: art_21JWypIydPMX
  label: dataset
  relation_type: uses
  relation_rationale: >-
    Provides the truly-prospective sentiment/aspect concepts (CAD-IMDB, CEBaB food/service).
- id: art_RidEJtBC7gPT
  label: method
  relation_type: uses
  relation_rationale: >-
    Uses the dossier's unit construction and (a)/(h)/(d) baselines for the outcome measurement.
- id: art_I2MrezW41iQo
  label: diagnostic
  relation_type: uses
  relation_rationale: >-
    Uses the firing-Jaccard threshold / form-free diagnostic to define regime labels.
title: >-
  Firing-Structure Router (M4): firing-Jaccard predicts when grouping beats attribution
summary: |-
  This experiment promotes the SAE-latent firing-Jaccard to a headline, a-priori router (M4) and validates it PROSPECTIVELY on a frozen Gemma-Scope SAE (google/gemma-scope-2b-pt-res, layer_12/width_16k/average_l0_82; model unsloth/gemma-2-2b; hook blocks.12.hook_resid_post; firing := encode>0; gating reconstruction-cosine 0.927, L0 median 70). method.py runs ONE uniform pipeline over 15 concepts: 12 ESTABLISHED (spelling L/O/T/I/D; numeric; taxonomic; toxicity threat/identity_attack/insult/obscene/sexual_explicit) used to DERIVE the rule, and 3 PROSPECTIVE (CAD-IMDB sentiment; CEBaB food/service aspect) predicted BEFORE their outcome is revealed. Per concept it (1) identifies a content-responsive parent latent on content-flip pairs (an unsupervised positive-firing-floor validation fixes the letter-I spurious-anchor bug), (2) finds per-sub-context detector latents + parent recall holes, (3) computes positive-only firing-Jaccard(detector,parent) over the concept's positives, and (4) measures a downstream OUTCOME: a LABEL-FREE CCRG K-track-lite unit (parent anchor + firing-disjoint, hole-covering absorbers) versus three required baselines at MATCHED pool size k -- (a) the best single raw SAE latent, (h) a supervised SAE standardized diff-of-means attribution pool (AxBench/SCR-TPP proxy), and (d) a non-SAE diff-of-means probe on the raw layer-12 residual -- scored by a held-constant logistic head on a held-out test fold with paired-bootstrap CIs (B=10000).

  KEY RESULTS: firing-Jaccard cleanly separates the regime EXTREMES -- spelling is firing-disjoint (Jaccard L=0.017, O=0.039, T=0.003, I=0.008, D=0.017, all <0.1; reproduces iter-2) and cluster-level grouping helps; toxicity co-fires (~0.69) so a single specialist latent wins. The primary router (predict absorption iff Jaccard<tau*) yields tau*=0.05, balanced accuracy 0.917 on the 12 established concepts; leave-one-concept-out accuracy 0.733; prospective out-of-sample accuracy 0.333 (sentiment HIT, predicted+measured co_firing; aspect_food/service MISS -- predicted co_firing but showed small absorption deltas +0.034/+0.071).

  HONEST FINDINGS (load-bearing for the paper): (i) firing-Jaccard ALONE is insufficient -- the TAXONOMIC counterexample has LOW Jaccard (0.056) yet a co_firing OUTCOME because the parent already has ~0.95 recall (no holes to fill); accordingly a recall-hole-only router (hole>0.777) reaches balanced accuracy 1.0 on established concepts, and a 2-signal router (low-Jaccard AND high-recall-hole) is also reported, supporting the refined rule 'grouping helps only when disjoint specialists AND parent recall holes co-occur'. (ii) The supervised baselines (h)/(d) frequently MATCH or beat the label-free unit on raw AUC (consistent with 'simple baselines are strong on raw-latent SAE tasks'); the unit's contribution is being LABEL-FREE while still beating the best single latent (a) in the absorption regime. (iii) numeric is reported honestly as suggestive/diagnostic-unconfirmed (absorption is documented empirically only on spelling).

  DELIVERABLES: method.py (self-contained, single-GPU, $0 LLM spend) and method_out.json with full/mini/preview variants (exp_gen_sol_out schema, all schema-PASSED, each <0.4MB). The output carries metadata with the prediction_vs_outcome_table (parent, jaccard min/median/max, recall_hole_max, predicted vs ground-truth regime, per-baseline AUCs auc_unit/auc_a/auc_h/auc_d, deltas with paired-bootstrap CIs, hit), per_concept_firing_jaccard (per-sub-context detector + bootstrap CIs), the router block (tau-sweep, regime separation, LOO per-concept, prospective table, plus strict-CI / recall-hole-only / combined router variants), a reproduction_check (spelling all <0.1 = True; toxicity references), and honest_notes. Expensive SAE forward passes are cached under cache/ (excluded from the published repo). Downstream GEN_PAPER_TEXT can use this as the M4 'when does cluster-level grouping help vs marginal attribution' router result and its honestly-reported boundary (firing-disjointness must co-occur with parent recall holes).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_3/gen_art/gen_art_experiment_4
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
  relation_type: uses
  relation_rationale: Uses civil_comments toxic texts for base-vs-IT model-diffing.
- id: art_dpYpjSn2Xvg3
  label: control-dataset
  relation_type: uses
  relation_rationale: Uses spelling-L corpus as the control concept for confound subtraction.
- id: art_RidEJtBC7gPT
  label: method
  relation_type: uses
  relation_rationale: Applies the dossier's co-response unit and shared pt-SAE diffing recipe.
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
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_3/gen_art/gen_art_experiment_5
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
  relation_type: differences
  relation_rationale: >-
    Audit corrects the dossier's Chanin venue (NeurIPS-2024->2025) and adds the Winnicki observational-KG contrast.
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
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_3/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

--- Item 17 ---
id: art_sxwT7hK6YFEA
type: experiment
in_dependencies:
- id: art_dpYpjSn2Xvg3
  label: dataset
  relation_type: uses
  relation_rationale: Uses first-letter corpus windows for the broad KG-repair held-out evaluation.
- id: art_t2uUbjSwpd3t
  label: dataset
  relation_type: uses
  relation_rationale: Uses taxonomic+numeric corpus windows for the cross-family repair loop.
- id: art_RidEJtBC7gPT
  label: method
  relation_type: uses
  relation_rationale: >-
    Reuses the dossier's two-track units/KG and repair-loop machinery for the auditability spine.
- id: art_I2MrezW41iQo
  label: diagnostic
  relation_type: uses
  relation_rationale: >-
    Uses diagnostic-corroborated absorbers as repair candidates and the (k) localization check.
title: >-
  Expanded KG-Repair + Member-Labeling Auditability Spine for SAE-Latent Cluster Units
summary: >-
  Expands the iter-3 measured-auditability result into the paper's load-bearing spine on a frozen Gemma-Scope L12/16k JumpReLU
  SAE over gemma-2-2b (gating cosine 0.9189 @ hidden_states[13], align 1.000; always gated on taxonomic country tokens because
  numeric digit tokens reconstruct at 0.8911<0.9 yet the SAE/layer mapping is global). FOUR measured pieces. (M1a) BROAD K-track
  KG: for EVERY eligible sub-context X a covering absorber is named purely on the selection split (argmax recall over content-responsive
  latents with firing-Jaccard<0.10 and sub-context precision>=0.70 vs the anchor), then ADDED to the parent/anchor and tested
  on held-out eval windows against a random-addition control of every other content-responsive latent, with paired-bootstrap
  CI (B=10000) AND a one-sided bootstrap p. (Multiplicity) Benjamini-Hochberg FDR<=0.05 across ALL 69 repair variants of all
  three families (hand-rolled BH cross-checked against statsmodels): 30 survive — homograph-taxonomic 6 (Georgia +0.80, Jordan
  +0.65, United States +0.21; k-track AND diagnostic; reproduces iter-3 exactly), numeric 10 (date +0.68, ordinal +0.53, decimal
  +0.45, year +0.35, comma_number +0.24, currency +0.14 — a NEW result showing absorption-repair generalises beyond spelling),
  spelling 14 (T that/their/there/then/those/three/through +1.0; O our +1.0, one +0.96; L like +1.0, law +0.78). 9 honest
  negatives emitted verbatim: numeric integer ties random (+0.007), first-letter O/on,out,over,own and T/this,think,time tie
  random; letter I anchor (1227) fires 0% on corpus -> auto-flagged spurious, repair N/A. (M1a-k) JTT label-free group-inference
  probe run per concept: its decoder-dictionary projection argmax is NEVER a KG absorber (kg_absorber_is_argmax=False everywhere)
  and on taxonomic/L/O/T/D is the PARENT anchor at rank 1 — (k) classifies holes but exposes no addable per-sub-context latent,
  whereas the KG names exactly one. (M7) Ensemble member-labeling (J=3 forced-choice claude-haiku-4.5 calls with shuffled
  candidate order to kill position bias) over 89 unit members INCLUDING all 15 of every first-letter max-pool: agreement 0.730
  vs shuffle null 0.096, gap 0.634, bootstrap CI [0.545,0.724] excludes 0, 0 parse-fails; per-role absorbers 0.756 / anchors
  0.43 (honest over-specification caveat). 15-wide confident-label fraction per letter L 0.87 / O 0.80 / T 0.93 / I 0.87 /
  D 0.67 (confident-and-correct ~0.60-0.73). LLM spend $0.194 (target <$1). Deliverables: method.py (full pipeline, reuses
  iter-3 SAE loader/encoder/repair_loop/k_localization_check, adds broad-KG derivation, one-sided p + BH, generalized (k),
  ensemble labeling + confident-fraction, disk-cached encodings), method_out.json (exp_gen_sol_out schema PASSED) with datasets
  kg_repair_loop (69 rows) and member_labeling (89 rows, predict_judge), README.md, fully-pinned pyproject.toml. Verdict:
  kg_utility_measured=True, n_survive_FDR05=30, member_labeling_above_null=True, fifteen_wide_confident_fraction_reported=True.
  Downstream paper-writing should headline the cross-family BH-surviving repairs + the (k)-cannot-localize contrast + the
  15-wide auditability fraction, and report numeric-integer/sparse-first-letter ties as honest negatives.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_4/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 18 ---
id: art_0CZwPjG2YMCf
type: experiment
in_dependencies:
- id: art_t2uUbjSwpd3t
  label: dataset
  relation_type: uses
  relation_rationale: >-
    Uses taxonomic country contexts (Georgia/Jordan/US) for the surgical sub-context edit.
- id: art_dpYpjSn2Xvg3
  label: dataset
  relation_type: uses
  relation_rationale: Uses first-letter contexts (large) for the surgical-edit demonstration.
- id: art_8QO7pl6Pd8UQ
  label: neg-pole-dataset
  relation_type: uses
  relation_rationale: Uses toxicity insult as the co-firing negative pole for the edit regime map.
- id: art_RidEJtBC7gPT
  label: method
  relation_type: extends
  relation_rationale: >-
    Adds new edit operators + behavioral side-effect measurement on top of the dossier's units/KG.
- id: art_I2MrezW41iQo
  label: diagnostic
  relation_type: uses
  relation_rationale: Uses diagnostic-named absorbers as edit targets and the (k) no-handle check.
title: KG-Localized Surgical Sub-Concept SAE Edit with Side-Effect Measurement (M1b)
summary: |-
  M1b is the unique-capability downstream task for the auditability-first two-track CCRG units: using the emitted feature knowledge-graph (KG), edit EXACTLY ONE sub-context by ablating its single NAMED absorber latent, and show high on-target effect with near-zero collateral on sibling sub-contexts and a tiny token footprint -- a capability the standard non-SAE handle (a dense parent direction) structurally cannot provide. This directly supplies the goal's 'activation steering with side-effect measurement' and 'feature-based classification of safety-relevant attributes' evaluation on a frozen Gemma-Scope L12/16k JumpReLU SAE + gemma-2-2b (edit/read at blocks.12.hook_resid_post; gating cosine 0.919, L0 88, matching iter-3), $0 LLM, single GPU.

  OPERATORS (forward hooks on the edit layer): KG-ABL = single named-absorber ablation h-=lambda*z_l*W_dec[l] (gated by the latent's own sparse firing); DENSE-ABL = diff-of-means parent erasure h-=beta*(h.u)u (baseline f, the non-SAE difference-of-means / logistic probe direction); RAND = random firing-rate-matched content latent; KG-ADD = steering-toward; (k) = label-free JTT probe (structural: no per-sub-context latent to edit). PRIMARY measure is behavioral: per-context next-token KL divergence at the edited token's position (steering-with-side-effects). A frozen dense parent probe (logistic + diff-of-means, fit on a DISJOINT diagnostic fold) is the secondary instrument; because country/letter membership is redundantly encoded, its margin is huge & broad under DENSE-ABL but insensitive to single-latent edits -- which is WHY behavioral KL is the primary on-target signal. Selectivity = on_target/collateral at matched effect, with B=10,000 paired bootstrap CIs on on-target, collateral, and the dense-minus-kg collateral difference; a graded verdict separates a CLEAN surgical edit (selectivity>=20, off-target footprint<5%, dense>kg collateral CI excludes 0) from a partial/co-firing edit.

  RESULTS (method_out.json, 7 cases, 5 SURGICAL_EDIT_CONFIRMED): taxonomic Georgia->16009 selectivity ratio 1722x (on-target KL 0.0216, KG collateral 3e-5, dense collateral 0.0496, KG footprint 0.0015 vs dense 1.0, dense-kg collateral CI [0.036,0.066]); Jordan->540 (2722x) & 8347 (3247x); United States->846 (214x); first-letter large->8463 (802x). The low-precision US absorber 4760 is only PARTIAL_SURGICAL (7.8x) -- absorber precision predicts surgicality (honest negative). TOXICITY negative pole (insult->13367) is PARTIAL_CO_FIRING_AS_PREDICTED: firing-Jaccard 0.878, parent recall-hole 0.0, selectivity 2.4x, footprint 0.117 -- single-latent ablation is NOT cleanly surgical because the sub-attribute co-fires with the parent, exactly as the firing-Jaccard/recall-hole router predicts. The regime router map cleanly splits absorption (n=6: mean selectivity 1452x, jaccard 0.014, footprint 0.0036) from co-firing (selectivity 2.4x, jaccard 0.878, footprint 0.117) -- a ~600x split. RAND raw-latent on-target ~0 (cannot reach matched); the (k) probe's decoder-projection argmax is the parent latent, never a KG absorber (no per-sub-context handle).

  OUTPUT DATASETS (exp_gen_sol_out, 409 examples, every example has predict_* per method): (1) edit_locality_per_context (402 rows) -- one labeled held-out context each: output=ON_TARGET (an X-context the edit SHOULD change) vs OFF_TARGET_SIBLING (a sibling it should NOT), with predict_kg_abl / predict_dense_abl / predict_rand = AFFECTED/UNAFFECTED from each operator's behavioral KL at full edit (lambda=1/beta=1); KG-ABL marks 0 of N siblings AFFECTED while DENSE-ABL marks nearly all (the collateral signature), RAND ~0 everywhere; (2) kg_surgical_edit_per_case (7 rows) -- output=SURGICAL_EXPECTED/NON_SURGICAL_EXPECTED by regime, predict_kg_abl=verdict, predict_dense_abl=HIGH/LOW_COLLATERAL, predict_*_selectivity. Rich aggregates live in metadata (per_case curves/matched/selectivity_CIs, summary.regime_router_map, k_localization_check, honest_negatives).

  DELIVERABLES: method.py (self-contained; reuses iter-2/iter-3 JumpReLUSAE/ModelBundle/encode_rows/k_localization_check/bootstrap + canonical units/KG read from iter-3 method_out.json; genuinely-new code = edit operators + behavioral side-effect measurement + per-context prediction rows); method_out.json + full/mini/preview_method_out.json (all schema-valid against exp_gen_sol_out, <500KB each); README.md; pyproject.toml (exact pinned versions, torch 2.6.0+cu124). Downstream paper can cite the surgical-edit ratios, the dense-baseline per-context collateral, the (k) no-handle result, and the firing-Jaccard router map as the auditability headline's concrete downstream payoff.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_4/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 19 ---
id: art___vgSpUe6wAF
type: experiment
in_dependencies:
- id: art_t2uUbjSwpd3t
  label: dataset
  relation_type: uses
  relation_rationale: Reuses cached taxonomic encodings for the precision-gated K-track rebuild.
- id: art_RidEJtBC7gPT
  label: method
  relation_type: extends
  relation_rationale: >-
    Extends the K-track with precision-gated/weighted coverage objectives and S-selectors.
- id: art_I2MrezW41iQo
  label: diagnostic
  relation_type: uses
  relation_rationale: >-
    Uses the form-free diagnostic to corroborate edges; reports its magnitude version is precision-blind.
title: 'Taxonomic SAE Unit/Specialist Conflation Fix: Precision-Gated K-Track Rebuild'
summary: |-
  Re-analysis (no new data) of the frozen Gemma-Scope L12/16k taxonomic absorption testbed, reusing the iter-2/3 cached CSR latents + fp16 residuals (CPU; no GPU re-encode). Fixes the iter-3 conflation where the two-track K-track classification unit's Georgia member was the high-coverage/low-precision latent 4697 (sub-context firing precision 0.35), not the diagnostic-corroborated specialist 16009 (0.96).

  CORE FIX (M2): the anchored greedy max-coverage is run in three objective variants on a SELECTION (train) fold and reported on a disjoint HELD-OUT (diagnostic) fold (M7): `original` (raw coverage; reproduces 4697), `gated` (+ hard per-sub-context FIRING-precision gate >=0.70 -> recovers 16009, drops 4697), and `weighted` (precision*coverage -> also 16009). Headline = gated unit [3792(anchor), 16009(Georgia .97/.96 sel/held-out), 540(Jordan), 846(United States)]. All 3 absorbers pass held-out subctx precision >=0.70 (fraction 1.0); member-labeling agrees.

  VERDICT taxonomic_setcover_isolated. On the held-out Georgia slice (150 pos vs 2100 neg, paired bootstrap B=10000) the unit AUC=0.995 beats every comparator with CIs excluding 0: vs (g) +0.577, (h) +0.612 (g/h below chance = the absorption signature), RE-k-anchored +0.082, and the three NEW non-random label-free count-matched selectors S-rec (+0.307), S-mag (+0.294), and the discriminating S-prec (+0.416; the globally most-precise latents are not Georgia-specific so S-prec misses 16009 -> AUC 0.579) => set_cover_established=True. A non-SAE dense probe still slightly edges the unit (-0.005, honest negative): the contribution is auditable WITHIN-SAE precision-gated selection + the homograph router, not out-classifying a dense probe.

  M3 homograph scope: a homograph x absorption-type cross-tab over all 52 countries shows absorption_type (parent recall-hole>0.5 AND specialist firing-Jaccard<0.10) is True for EXACTLY {Georgia, Jordan} - both documented homographs whose general parent latent is suppressed (hole 0.80/0.71). Chile/Turkey are homographs but their parent COVERS them (hole ~0) -> not absorption; United States is non-homograph co-firing/splitting (fj 0.20); 48 non-homographs have hole~0. The hardcoded homograph set equals the dataset's metadata_notes=='ambiguous_homograph' flag (no discrepancy).

  HONEST NUANCE (per-edge form-free KG, M2 Phase 4): the form-free absorption_fraction is a MAGNITUDE oracle and on Georgia holes picks the high-coverage LOW-precision latent 1966 (precision 0.34), not the precise member 16009 (they co-fire, Jaccard 0.34) -> per-edge top-1 agreement with 16009 is 0. Corroboration therefore rests on the PRECISION diagnostic (non-triviality) + the router recall-hole signal, all of which 16009/540/846 pass; the magnitude oracle is precision-blind (reported separately, not a 3-edge mean). The precision rebuild buys AUDITABILITY (a Georgia-pure member), not raw AUC (all 3 Georgia absorbers reach recall 1.0 / ~0 FP so AUC is ~identical across variants).

  Numeric is the contrast: verdict numeric_suggestive_diagnostic_unconfirmed, set_cover_established=False (integer is co-firing/splitting J=0.256, no precision-passing integer specialist; dense probe AUC 1.0 dominates the unit's 0.635).

  DELIVERABLES: method.py (single pipeline; copied & edited from iter-3 method, +run_greedy 3-variant K-track, fold split, M5 selectors, M3 cross-tab, ablation, transparency). full/mini/preview_method_out.json (schema exp_gen_sol_out, all PASS; full 10.9MB <100MB) with metadata.per_hierarchy.{taxonomic,numeric} carrying rebuilt_units, precision_objective_ablation, auc_point + auc_diff_ci (S-rec/S-prec/S-mag + RE-k-anchored + g/h/dense), kg_agreement (per-edge + formfree_magnitude_top), formfree_magnitude_tension, homograph_crosstab, router_all, selection_isolation, rebuilt_unit_transparency; datasets[].examples carry predict_{unit,anchor,g,h,dense_probe,rek,S_rec,S_prec,S_mag,original,weighted}. results/*.csv (auc_diff +S-* cols, router_all +homograph col, ablation, per_edge_kg). All JSON-vs-CSV internal-consistency cross-checks PASS. cache/ (124MB reused encodings) is upload-ignored.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_4/gen_art/gen_art_experiment_3
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 20 ---
id: art_JMA2gBvnakAm
type: experiment
in_dependencies:
- id: art_dpYpjSn2Xvg3
  label: dataset
  relation_type: uses
  relation_rationale: >-
    Encodes the first-letter spelling testbed pairs/corpus for the selection-isolation re-run.
- id: art_YwjLYapklnVk
  label: surface-control
  relation_type: uses
  relation_rationale: >-
    Computes the admission surface-invariance null on the 1,700-pair surface superset.
- id: art_RidEJtBC7gPT
  label: method
  relation_type: extends
  relation_rationale: >-
    Extends the pipeline with firing-floor anchor validation and non-random S-selector controls.
- id: art_I2MrezW41iQo
  label: diagnostic
  relation_type: uses
  relation_rationale: Uses the form-free diagnostic as the non-circular E1 absorption oracle.
title: >-
  Two-Track CCRG Selection Isolation: Non-Random Selectors, Firing-Floor, Compact Unit
summary: |-
  Iter-4 re-runs the frozen-SAE first-letter two-track Counterfactual Co-Response Grouping (CCRG) pipeline (Gemma-Scope L12/16k JumpReLU SAE on unsloth/gemma-2-2b, hook blocks.12, gating cosine 0.924 / EV 0.857) verbatim from iter-3 and adds three honest-scoping deltas; $0 LLM spend, B=10,000, ~14 min on one GPU. Method = K-track anchored greedy set-cover unit (anchor + per-token absorbers). Baselines held constant: raw single latent (a), co-fire/decoder clusters (b,c), oracle attribution top-k (h), and the demoted random-eligible-k floor (RE-k). M5 (decisive new core): three NON-RANDOM, label-free, count-matched-to-k selectors over the SAME cover-eligible set Lr -- S_rec (top-k by content-flip recall), S_prec (top-k by firing precision), S_mag (top-k by mean magnitude) -- max-pooled identically to the unit, so unit-minus-each isolates the set-cover SELECTION rule from sensible label-free selection; reported as paired-bootstrap AUC-difference CIs (pair-cluster resampling). M4: an unsupervised firing-floor anchor validation (a valid parent anchor must fire >=5% on held-out corpus) plus a per-letter JOINT (E1 AND selection) and a renamed verdict. M7: the compact named unit (anchor + diagnostic-corroborated absorbers, cap 5) vs the full 15-wide max-pool, with an AUC-difference CI, an anchor_only floor, and an AUC-vs-cumulative-k curve.

  RESULTS (L,O,T,I,D). primary_endpoint = REFRAMED_TO_ELIGIBILITY_AND_SENSIBLE_SELECTION (n_E1_pass=5, n_joint=2, n_selection_vs_M5=2, n_eligibility_only=2). M4 firing-floor RECOVERED letter I: its recall-argmax anchor 1227 fires 0% on corpus; the validated anchor 1634 (fires 20.6%) IS the form-free-diagnostic parent, so E1 now PASSES for I (5/5 overall, up from iter-3's 4/5); L/O/T/D anchors unchanged (already fire >0.26). M5 selection isolation: the set-cover-specific selection is established only on I and D (unit beats h AND all three non-random selectors, CIs exclude 0); on L/O/T the strong S_rec (top-k by recall, which picks the anchor + highest-coverage latents) matches the unit, so the win there is cover-based eligibility + sensible selection, not set-cover-specific. Per-letter unit AUC (vs h): L .905(.795) O .917(.819) T .858(.647) I .983(.735) D .956(.727). Pooled across letters the unit beats h by 0.188 (CI .148-.223), S_rec by 0.109 (.077-.143), S_prec by 0.273, S_mag by 0.120 (all pooled CIs exclude 0), but per-letter S_rec is significant on only 2/5. M7: the compact named unit (k=5) is SIGNIFICANTLY BELOW the 15-wide pool on every letter ( delta AUC -0.056 to -0.200, CIs exclude 0) -- the diagnostic-uncorroborated absorbers carry real classification signal, so human-auditable compactness costs AUC; reported, not hidden. E2 (absorbed-slice recall) passes only on T. The iter-3 over-aggregating rule (E1 AND unit>h AND RE-k on >=3/5) would have declared ABSORPTION_REPAIR_SELECTION_CONFIRMED (RE-k is an easy floor: median draw AUC 0.63-0.69, frac_rek>=unit <=0.008); this is recorded under legacy_iter3_verdict and contrasted.

  FAITHFULNESS/HARDWARE: this run is on RTX 2000 Ada (sm_89); iter-3 ran on RTX 5090 (sm_120). The UNMODIFIED iter-3 method.py was re-run on this host and produced numbers IDENTICAL to this iter-4 run for L (unit AUC 0.905, K_UNIT ending in latent 1566, RE-k mean 0.651), confirming the additive M4/M5/M7 code does not perturb the pipeline (M5/M7 use separate child rngs; the firing-floor corpus encode consumes no shared rng). Differences from the stored iter-3 anchors (L unit 0.876, member 1362) are bf16 hardware numerics breaking a discrete greedy set-cover tie at L's 15th member -- documented in metadata.repro_appendix.

  OUTPUT (schema exp_gen_sol_out, {metadata, datasets}, all variants <0.7MB). metadata.per_letter[X] carries anchor_validation, E1, E2, C1 (per_method AUC for unit/a/b/c/h/REk/S_rec/S_prec/S_mag/unit_compact/unit_15wide/anchor_only + auc_diff CIs), selection_isolation, compact_vs_wide (auc_by_k curve, compact_minus_15wide CI), admission, kg_edges, unit_definition. metadata.verdicts carries primary_endpoint, per_letter_joint, set_cover_isolation_table, compact_vs_wide_table, letter_I_annotation, legacy_iter3_verdict, and pooled_across_letters (unit_vs_h/REk/S_rec/S_prec/S_mag stratified-bootstrap + inverse-variance meta). datasets = one group per letter of held-out test-fold rows with predict_{unit,a,b,c,h,REk,S_rec,S_prec,S_mag,unit_compact,unit_15wide,anchor_only}. For the paper: the headline is the honest reframe (cluster-level units beat raw latents and attribution and a random-eligible floor, but the set-cover-SPECIFIC win over strong non-random selectors holds only on 2/5 letters), plus the M4 firing-floor anchor fix and the M7 auditability-vs-AUC tradeoff.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_4/gen_art/gen_art_experiment_4
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 21 ---
id: art_GTc_f26dMzFs
type: experiment
in_dependencies:
- id: art_dpYpjSn2Xvg3
  label: dataset
  relation_type: uses
  relation_rationale: Encodes spelling concepts as firing-disjoint absorption-pole derivation points.
- id: art_t2uUbjSwpd3t
  label: dataset
  relation_type: uses
  relation_rationale: Encodes numeric/taxonomic concepts as router derivation points.
- id: art_8QO7pl6Pd8UQ
  label: dataset
  relation_type: uses
  relation_rationale: Encodes toxicity concepts as the co-firing pole of the router.
- id: art_21JWypIydPMX
  label: dataset
  relation_type: uses
  relation_rationale: >-
    Provides the truly-prospective sentiment/aspect/bias concepts for the held-out router test.
- id: art_RidEJtBC7gPT
  label: method
  relation_type: uses
  relation_rationale: >-
    Uses the dossier's unit construction and (a)/(h)/(d) baselines for the router outcome.
title: >-
  A-priori SAE firing-structure router as a screening heuristic with measured error
summary: >-
  method.py implements an a-priori SAE firing-structure ROUTER on the frozen Gemma-Scope L12/16k JumpReLU SAE over unsloth/gemma-2-2b
  (layer-12 residual hook; firing := encode>0; SEED=1234; $0 LLM). From ONE forward pass it reads two label-free signals per
  concept — the firing-Jaccard between per-sub-context detector latents and the broad parent latent, and the parent's recall-hole
  — and combines them into a screening rule: predict ABSORPTION-regime iff (firing-Jaccard < tau_J) AND (recall-hole > tau_h),
  else CO-FIRING. Absorption => the label-free CCRG K-track unit (parent anchor + firing-disjoint hole-covering absorbers)
  beats the best single RAW SAE latent (a); co-firing => a single specialist already wins. The experiment's contribution is
  methodological honesty: (1) DERIVATION vs TRULY-PROSPECTIVE separation — 12 derivation concepts (spelling L/O/T/I/D, numeric,
  taxonomic, 5 toxicity sub-attributes) fit the thresholds, single-signal ablations, and leave-one-out; they are NEVER counted
  as prospective. (2) An EXPANDED, truly-held-out prospective set predicted with the FROZEN rule before measurement: sentiment,
  CEBaB aspect_food/service, ~8 bias_in_bios profession concepts (pre-registered boundary-null), and civil_comments severe_toxicity
  (descriptive_only). Prospective hit-rate + Wilson CI = the MEASURED error, framed as a screening heuristic, not a validated
  oracle. Each concept reports the held-out-test outcome of the label-free unit vs three supervised baselines at matched pool
  size: (a) best raw SAE latent, (h) standardized diff-of-means SAE attribution pool, (d) non-SAE residual diff-of-means probe;
  paired-bootstrap delta CIs (B_BOOT=4000); PRIMARY regime = sign(auc_unit-auc_a), SECONDARY vs (h). KEY VERIFIED RESULT (reproduced
  exactly in the run logs at full scale): spelling firing-Jaccard 0.017/0.039/0.003/0.009/0.017 (all absorption), numeric
  0.285 with recall-hole 0.800 (absorption), toxicity ~0.69 (co_firing); the COMBINED rule achieves balanced-accuracy 1.0
  on derivation at tau_J~0.30, tau_h~0.78 — strictly dominating jaccard-alone (0.917) and tying recall-hole-alone (1.0, the
  strongest single separator) — with derivation leave-one-out ~0.83 (misses only the boundary concepts numeric+taxonomic).
  Counterexamples justify the conjunction: numeric has HIGH jaccard yet is absorption; taxonomic has LOW jaccard yet co_firing
  (parent already ~full recall). Outputs (exp_gen_sol_out): method_out.json + full/mini/preview, one router-decision card
  per concept with metadata mirroring derivation_table, prospective_table (vs-a AND vs-h), single_signal_ablations, loo, prospective_hitrate
  (existing-3 / new-only / combined-all + Wilson CIs), reproduction_check, and honest_notes. IMPORTANT STATUS: the currently-emitted
  JSON is a small placeholder from the --smoke run because a co-tenant job held the shared single GPU continuously for >2.5h,
  blocking the full-scale pass; method.py is complete, correct, and validated (gating recon-cos 0.927, BOS token-id mismatches
  0), and its self-healing launcher (run_full.sh) is wired to overwrite the output with the full 24-concept result the instant
  the GPU frees. Reproduce: uv run method.py --scale full.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_4/gen_art/gen_art_experiment_5
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 22 ---
id: art_QBxBPF-9Ldxe
type: research
in_dependencies:
- id: art_i-tkvFCKneA-
  label: citations
  relation_type: extends
  relation_rationale: >-
    Extends the iter-3 citation audit with homograph-novelty + surgical-edit positioning and locked venues.
title: >-
  CCRG iter-4: Homograph-Absorption Novelty, KG-Surgical-Edit Distinctness, Locked Citations
summary: >-
  Finalizes positioning + citations for the auditability-first CCRG (Counterfactual Co-Response Grouping) paper, building
  on the iter-3 audit (art_i-tkvFCKneA-) without re-doing settled entries. FOUR deliverables (pure web research, $0): (A)
  Homograph/polysemy absorption framing = NOVEL: documented feature absorption is empirically first-letter-spelling-only (Chanin
  2409.14507 'short'/'starts-with-S'; SAEBench 2503.09532 absorption metric is built on Chanin's first-letter task) and mechanistically
  tied to sparsity+hierarchy+dictionary-size (Chanin; Matryoshka 2503.17547), NOT to homograph/polysemous tokens with a suppressed
  parent on a semantic hierarchy. The key near-miss PS-Eval (Minegishi et al., 2501.06254, ICLR 2025) evaluates SAE word-SENSE
  separation and a full-text grep finds it NEVER mentions absorption/recall-hole/router/spelling/suppressed-parent (only hit
  = JumpReLU 'suppresses small activations'). Provides short+long positioning paragraphs + a one-line PS-Eval cite-and-distinguish;
  framing guardrail = 'absorption recurs on polysemous tokens, predicted by the recall-hole signal' NOT 'broad taxonomic generalization'.
  (B) KG-localized single-absorber surgical sub-concept edit = DISTINCT: no SAE/LLM steering/erasure method edits a single
  absorber latent NAMED by an interventional feature-KG edge to change/recover ONE sub-context while preserving the parent,
  measured as recall-recovery vs random-addition control + side-effect KL. SAE-TS (2411.02193) and SRS (2503.16851) select
  a CONCEPT feature (effect-approximator / contrastive-KL) with a coefficient; SALVE (2512.15938) is VISION (ResNet-18/ViT-B/16);
  LEACE (2306.03819, NeurIPS 2023) is dense whole-concept erasure that cannot localize to a sub-context; SAeUron/SAEmnesia/SNCE
  are text-to-image DIFFUSION erasure (modality distinguisher). AxBench (2501.17148, ICML 2025) is the side-effect/fluency
  LLM-judge eval bar AND the honest concession (diff-of-means beats SAEs on aggregate steering) -> CCRG scopes the edit as
  an auditability DEMONSTRATION. Cite-and-distinguish table + M1 positioning paragraph + honest-scope note provided. (C) Locked
  2025/2026 citation table: PS-Eval=ICLR2025; SALVE=ICLR2026 Trustworthy-AI Workshop(vision); SAE-TS=arXiv2024; SRS=arXiv2025;
  LEACE=NeurIPS2023; SAeUron=ICML2025(diffusion); SAEmnesia/SNCE=2025 preprints(diffusion). TWO upgrades vs iter-3: DPE 2505.23027
  -> ICML 2025 (poster 43937/OpenReview qUTiOeM57J); SCR/TPP 2411.18895 -> NeurIPS 2024 ATTRIB Workshop. BibTeX block + corrections
  diff + unresolved flags (SAEmnesia/SNCE author lists to verify at bib-time; do not invent). (D) Presentation-strip checklist
  for GEN_PAPER_TEXT (strip iteration/rebuttal/infra scaffolding; move SAE-IDs/seeds/env to appendix; lead with measured auditability;
  dedicated honest-negatives subsection; use locked table). Outputs research_out.json {title, summary, answer, 23 sources,
  4 follow_ups} + research_report.md (sections A-D with drop-in paragraphs, full table, BibTeX, checklist). Both novelty claims
  HOLD; adversarial disprove-searches found no precedent.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_4/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

--- Item 23 ---
id: art_9muVcI4tkqJf
type: experiment
in_dependencies:
- id: art_t2uUbjSwpd3t
  label: taxonomic-data
  relation_type: uses
  relation_rationale: >-
    Unlearning edit uses taxonomic Georgia/US country contexts as forget/retain targets.
- id: art_dpYpjSn2Xvg3
  label: spelling-data
  relation_type: uses
  relation_rationale: Uses first-letter 'large' spelling contexts as an absorption unlearning case.
- id: art_8QO7pl6Pd8UQ
  label: toxicity-data
  relation_type: uses
  relation_rationale: Uses toxicity insult as the predicted co-firing negative-pole unlearning case.
- id: art_RidEJtBC7gPT
  label: method
  relation_type: uses
  relation_rationale: >-
    Reuses the dossier's units/edit operators verbatim (core.py) for the unlearning task.
- id: art_I2MrezW41iQo
  label: diagnostic
  relation_type: uses
  relation_rationale: >-
    Uses diagnostic-named absorbers (16009/8463/846) as the single-latent edit targets.
title: KG-Localized Absorber Unlearning Beats Dense Parent Erasure on a Joint Outcome
summary: |-
  M1 LOAD-BEARING DOWNSTREAM WIN for the two-track CCRG units: it converts iter-4's 'surgical selectivity' capability into a BETTER RESULT than the dense baseline on selective sub-concept UNLEARNING. Task: at MATCHED forget-quality, ablate ONE KG-named absorber latent (KG-ABL: h-=lambda*z_l*W_dec[l], gated by the latent's own sparse firing) vs erase the dense diff-of-means parent direction (DENSE-ABL, baseline f; for a binary parent ~ LEACE 1-D erasure). WIN <=> KG-ABL has strictly LOWER sibling+parent collateral AND BETTER fluency than DENSE-ABL, with a KG-minus-dense paired-bootstrap CI (B=10000) on the JOINT (retain-quality x fluency) outcome excluding 0.

  RESULT (method_out.json, full run): 4 cases, 2 DOWNSTREAM_WIN_CONFIRMED => the M1 gate is PASSED. (i) taxonomic/Georgia (absorber 16009): joint Delta=+0.423 [0.274,0.571], retain next-token KL KG=3e-5 vs DENSE=0.102, KG utility 1.75 vs 1.33, footprint 0.014 vs 1.0; collateral AND fluency CIs each exclude 0. (ii) first-letter/large (8463): joint Delta=+1.646 [1.479,1.799]; the dense 'starts-with-L' erasure at matched forget collapses to utility 0.17 while KG stays 1.82 (it wrecks fluency on every token; KG does not). (iii) taxonomic/United States (846): PARTIAL_WIN -- joint CI excludes 0 and collateral favors KG, but fluency CI includes 0 (weaker, multi-token absorber). (iv) toxicity/insult (13367) is the declared honest co-firing negative pole: insult sub-attributes co-fire with the toxic parent (firing-Jaccard 0.882, no parent recall-hole), the single latent fires on 16.6% of tokens, and the joint CI INCLUDES 0 [-0.035,0.451] -> EXPECTED_LOSS_ROUTER_CONSISTENT, exactly as the firing-Jaccard router predicts in advance. Curve-level dominance = 1.00 for every case (KG strictly lower collateral at every achievable forget level), so the win is robust to the single matched point. The REGIME SPLIT (absorption Jaccard 0.002-0.04 -> clean win; co-firing Jaccard 0.88 -> no win) is the contribution.

  METHOD/BASELINES: forget-matching via a lambda/beta sweep (next-token KL on held-out FORGET windows); generation under each edit hook (greedy, 40 tokens); an AxBench-style OpenRouter LLM judge (anthropic/claude-haiku-4.5, temp 0, utility=harmonic_mean(fluency,content_pres) in [0,2]); plus a model-internal joint (high-n retain next-token KL + continuation perplexity) as corroboration and explicit fallback. Required baselines covered: (ii) non-SAE = dense diff-of-means/LEACE parent probe (DENSE-ABL); raw-latent SAE contrast = RAND (firing-rate-matched random latent, ~no effect). SAE google/gemma-scope-2b-pt-res layer_12/width_16k (JumpReLU, d_model 2304); model google/gemma-2-2b bf16; edit+read at blocks.12.hook_resid_post (gating cosine 0.919). Canonical units/KG from iter-3 (taxonomic.anchor=3792, Georgia->16009, L 8463->large); insult latent re-found by max-AUC among toxic rows (13367, matching iter-4). $0 model-internal + $0.4367 LLM judge (876 calls, 0 fail/refusal; target $2, hard cap $10).

  REUSE: core.py = iter-4 gen_art_experiment_2/method.py verbatim (only WORK path repointed): JumpReLUSAE, load_sae, ModelBundle, ParentProbe (logistic probe AND diff-of-means dense direction u_t), make_edit_hook, side_effects, forward_pos_logprobs/kl_rows/behavioral_curve, paired_bootstrap_diff, bootstrap_mean_ci, _scale_for_on_target, pick_random_latents, content_responsive, load_*, NEUTRAL_TEXT, read_canonical_units, save_json. method.py adds the new pieces.

  OUTPUTS: datasets[0]='unlearn_per_prompt' (292 rows: one per (case, held-out prompt); input=prefix, output=role FORGET/RETAIN/UNRELATED, predict_kg_abl/predict_dense_abl/predict_rand/predict_noop = generated continuations + per-op metadata_fluency/content_pres/utility and model-internal last-token KL + continuation PPL). datasets[1]='kg_vs_dense_per_case' (4 rows: output=WIN_EXPECTED/LOSS_EXPECTED, predict_kg_abl=win_verdict, all collateral/joint CIs + firing-Jaccard + curve-dominance in metadata_*). metadata holds gating, judge spend, per_case curves/matched-scales/CIs/judged-forget-confirmation, summary, and honest_negatives verbatim. Concrete worked example in the data: on a sibling context naming 'United States', KG-ABL preserves it (content_pres 2) while DENSE-ABL corrupts 'United States'->'surrounding areas' (content_pres 1). All outputs validate against exp_gen_sol_out and are < 0.5 MB.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_5/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 24 ---
id: art_4L1MZxvWYlGd
type: experiment
in_dependencies:
- id: art_I2MrezW41iQo
  label: sae-ids
  relation_type: uses
  relation_rationale: >-
    Uses the dossier's pinned Gemma-Scope SAE IDs (65k/layer-9) and diagnostic for re-derivation.
- id: art_t2uUbjSwpd3t
  label: taxonomic-data
  relation_type: uses
  relation_rationale: Re-encodes taxonomic homograph testbed on the second dictionary.
- id: art_dpYpjSn2Xvg3
  label: spelling-data
  relation_type: uses
  relation_rationale: Re-encodes first-letter spelling testbed on the second dictionary.
- id: art_8QO7pl6Pd8UQ
  label: toxicity-data
  relation_type: uses
  relation_rationale: Re-encodes toxicity as the co-firing pole for the cross-dictionary regime split.
- id: art_RidEJtBC7gPT
  label: method
  relation_type: extends
  relation_rationale: >-
    Extends the iter-4 spine pipeline to a second SAE dictionary parametrized over config.
title: >-
  Cross-Dictionary Replication of the SAE Auditability Spine on a 65k Gemma-Scope SAE
summary: |-
  M2 re-runs iter-4's four-piece auditability spine on a SECOND Gemma-Scope SAE dictionary of the SAME frozen gemma-2-2b, to separate model+method findings from one-dictionary artifacts. PRIMARY = width-65k canonical at layer-12 (average_l0_72, d_sae=65536, resolved as closest-to-100 from {21,38,72,141,297}); SECONDARY (reduced) = layer-9 width-16k (average_l0_73). The decisive design point: latent indices are dictionary-specific, so anchors AND per-sub-context absorbers are RE-DERIVED on each dictionary (16k Georgia->16009/Jordan->540 do not carry over). Anchor re-derivation = highest content-flip-coverage content-responsive latent with sub-context precision>=0.70, validated by an unsupervised corpus firing-floor>=0.01; absorbers via the K-track greedy (firing-Jaccard<0.10, precision>=0.70) and, independently, a form-free probe-projection diagnostic. method.py is one file parametrized over the SAE config; it reuses iter-4 exp1 (broad KG-repair + random-single-latent control + one-sided bootstrap p + Benjamini-Hochberg FDR, statsmodels-crosschecked), iter-4 exp2 (KG-ABL/DENSE-ABL/RAND edit operators + next-token-KL on_target/collateral run_case), iter-3 exp4 (firing_jaccard, recall-hole, derive_1d router). Core is $0 LLM.

  HEADLINE: cross_dictionary_replicates = full. 65k (layer-12) gives overall=full with ALL four pieces REPLICATES: (A) homograph holes reappear (Georgia recall-hole 0.873/jaccard 0.0038; Jordan 0.746/0.097; re-derived anchor 31478, corpus-fire 0.916); (B) 55/154 KG-repairs survive BH FDR<=0.05 (spelling 29 / homograph-taxonomic 11 / numeric 15, deltas +15/+5/+5 vs 16k's 14/6/10 = the predicted wider-SAE-absorbs-more signal; 52 distinct holes); (C) Georgia single-absorber (46143) ablation is SURGICAL_EDIT_CONFIRMED at selectivity ratio 3.7M (KG-collateral 0 vs DENSE 0.037), plus US/`layer`/`did`; (D) the FROZEN 16k recall-hole threshold (tau_h=0.7774) transfers at balanced-accuracy 1.0. Clean regime split: absorption mean selectivity 466997x vs co-firing toxicity-insult 1.99x (jaccard 0.837), confirming the router on the new dictionary. SECONDARY layer-9 gives overall=partial and shows absorption is LAYER-specific: a cleaner layer-9 parent (corpus-fire 0.987) means Georgia loses its hole (0.003) while Jordan keeps its hole (0.536) and a confirmed surgical edit (2376x); the multi-concept router transfer is NOT_RUN in the reduced taxonomic-only run. Honest nulls reported verbatim (re-derived Jordan/`on`/`take` absorbers fire but ablation has no on-target effect). Gating: 65k cosine 0.9280 (>0.9, +0.009 vs 16k), hidden_states[13]; numeric digit-token cosine 0.876 recorded descriptively (not gate-failed); all anchors firing-floor-validated, none spurious.

  OUTPUT (exp_gen_sol_out, schema-valid): metadata.replication_tables[dict] (per-piece recall_hole/jaccard, per-family FDR survivors+deltas+distinct count, surgical CIs/footprint, frozen-vs-refit router balanced-accuracy, regime_split, per_piece_verdicts, overall_verdict), metadata.router_transfer, metadata.verdict.cross_dictionary_replicates, plus datasets cross_dictionary_replication (one row per dictionary x piece x sub_context), kg_repair_loop, edit_locality_per_context. Downstream (paper) gets a precise, honest characterization of when the absorption/KG-repair/surgical-edit story is dictionary- and layer-dependent. cache/ (encoding npz, ~400MB) is excluded from upload. NOTE: repatch_verdicts.py re-assembles the verdict tables from the saved run via the same method.py functions (no model re-run); a fresh `uv run method.py --dicts 65k,l9_16k` reproduces method_out.json identically.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_5/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 25 ---
id: art_4q5Om8wdqZuz
type: experiment
in_dependencies:
- id: art_dpYpjSn2Xvg3
  label: spelling-data
  relation_type: uses
  relation_rationale: >-
    Encodes spelling concepts as firing-disjoint absorption derivation points for the router.
- id: art_t2uUbjSwpd3t
  label: nonspelling-data
  relation_type: uses
  relation_rationale: Encodes numeric/taxonomic concepts as router derivation points.
- id: art_8QO7pl6Pd8UQ
  label: toxicity-data
  relation_type: uses
  relation_rationale: Encodes toxicity as the co-firing pole of the router.
- id: art_21JWypIydPMX
  label: prospective-data
  relation_type: uses
  relation_rationale: >-
    Provides truly-prospective sentiment/aspect/bias concepts for the held-out router test.
- id: art_RidEJtBC7gPT
  label: method
  relation_type: uses
  relation_rationale: >-
    Uses the dossier's unit construction and (a)/(h)/(d) baselines for the router outcome.
title: >-
  A-priori SAE firing-structure router: recall-hole screens cluster-vs-latent reliability
summary: >-
  method.py FULLY RUNS (scale=full, 31 concepts) an a-priori SAE firing-structure ROUTER on the frozen Gemma-Scope L12/16k
  JumpReLU SAE over unsloth/gemma-2-2b (layer-12 residual hook; firing := encode>0; SEED=1234; $0 LLM; single GPU; gating
  recon_cos_mean=0.9269 (>0.80), encode_token token-id mismatches 0). From ONE forward pass it reads label-free firing-structure
  signals per concept and predicts the regime: ABSORPTION (the label-free CCRG K-track unit = parent anchor + firing-disjoint
  hole-covering absorbers BEATS the best single raw SAE latent) vs CO-FIRING (a single specialist already wins). M6b REFRAME
  (recommended): RECALL-HOLE-ALONE = predict absorption iff the parent latent's per-sub-context recall-hole > tau_h_alone=0.779;
  on the 12 derivation concepts this is the strongest single separator (balanced-acc=1.0, NO counterexample). Firing-Jaccard-alone
  reaches only balanced-acc=0.917 (demoted to a CORROBORATING signal); the combined conjunction (firing-Jaccard<0.31 AND recall-hole>0.78)
  also reaches 1.0 on derivation but its out-of-sample prospective hit-rate does NOT exceed recall-hole-alone (conjunction_beats_primary_out_of_sample=False),
  so recall-hole-alone stays the recommendation by parsimony. Two honest counterexamples justify recall-hole over firing-Jaccard-alone:
  numeric (firing-Jaccard 0.285 HIGH yet ground-truth absorption) and aggregated taxonomic (firing-Jaccard 0.058 LOW yet co_firing
  because the parent already has near-full recall / ~0 hole). EVALUATION compares the label-free unit against (a) best single
  raw SAE latent, (h) supervised standardized diff-of-means SAE-attribution pool, and (d) a non-SAE residual diff-of-means
  probe, all at MATCHED pool size with a held-constant LR head (only SELECTION differs); paired-bootstrap delta CIs (B_BOOT=4000);
  ground-truth regime = sign(auc_unit-auc_a). INTEGRITY: 12 DERIVATION concepts (spelling L/O/T/I/D, numeric, taxonomic, 5
  toxicity sub-attributes) fit thresholds/ablations/leave-one-out (LOO acc 0.833; misses ONLY the boundary numeric+taxonomic)
  and are NEVER counted as prospective. M6c: the truly-held-out PROSPECTIVE set is predicted with the FROZEN rule BEFORE its
  outcome is measured ('logged BEFORE outcome measurement') and spans BOTH regimes: 7 internally-built NEW first-letter spelling
  concepts (B,C,F,M,P,R,W; 250 content pairs + 300 real Pile-window corpus positives each, from_templates=False; derived from
  the gemma vocab get_alpha_tokens recipe) supply ABSORPTION-regime concepts alongside CO-FIRING concepts (sentiment, CEBaB
  aspect food/service, 8 bias_in_bios professions, civil_comments severe_toxicity). M6d DECISIVE deliverable - prospective
  hit-rate STRATIFIED by predicted regime, each with a Wilson 95% CI (the MEASURED error of a screening heuristic, not a validated
  oracle): absorption_predicted 3/6=0.50 [0.19,0.81], cofiring_predicted 8/12=0.67 [0.39,0.86], combined_all 11/18=0.61 [0.39,0.80].
  The router is genuinely WRONG IN BOTH DIRECTIONS: new letters F/M/W are predicted absorption (recall-hole=1.0) but measure
  co_firing (unit ties (a)) = false-absorption misses, while C/P/R are correct absorption wins (delta_vs_a +0.05 to +0.07,
  sig). Honest reproduction: derivation spelling firing-Jaccard stays low (L .017 .. D .016) but several new letters are higher
  (B .10, F .089, M .087, R .09) so spelling<0.05 is False (reported, not hidden); recomputed toxicity firing-Jaccard (threat
  .69, identity_attack .11, insult .69) differs from the prior reference and is reported as an honest discrepancy. Outputs
  (exp_gen_sol_out, all PASSED, <100MB): method_out.json + full/mini/preview, 31 router-decision cards (metadata_role, metadata_predicted_regime
  [PRIMARY recall-hole-alone] + _combined/_jaccard ablations, ground-truth regimes, recall_hole_max, jaccard_median, outcome
  auc_unit/a/h/d + delta CIs, is_prospective_hit, power_flag, per_subcontext) mirroring top-level derivation_table, prospective_table,
  single_signal_ablations (recall_hole_alone PRIMARY), ablation_combined, loo, counterexamples, prospective_hitrate_primary
  + ablation hitrates, reproduction_check, honest_notes, new_letter_report. self_check.py: ALL CHECKS PASSED. Reproduce: uv
  run method.py --scale full.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_5/gen_art/gen_art_experiment_3
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 26 ---
id: art_Iy77UHoNaIhS
type: experiment
in_dependencies:
- id: art_21JWypIydPMX
  label: profession-data
  relation_type: uses
  relation_rationale: Uses bias_in_bios profession bios to test absorption on a clean is-a hierarchy.
- id: art_t2uUbjSwpd3t
  label: taxonomic-data
  relation_type: uses
  relation_rationale: >-
    Re-uses cached taxonomic encodings to reproduce the Georgia/Jordan homograph cross-tab.
- id: art_RidEJtBC7gPT
  label: method
  relation_type: uses
  relation_rationale: Reuses the two-track set-cover engine and baselines for the second-case search.
- id: art_I2MrezW41iQo
  label: diagnostic
  relation_type: uses
  relation_rationale: >-
    Uses the form-free absorption diagnostic to score professions; finds 0/28 absorption.
title: >-
  M7: Second SAE Absorption Case Beyond Georgia — Profession Is-A Hierarchy + Homograph Scan
summary: |-
  Executes M7 on the FROZEN Gemma-2-2b / Gemma-Scope layer_12/width_16k JumpReLU SAE to test whether the iter-4 non-spelling absorption/set-cover result (effectively n=1, Georgia; 1-2 with descriptive Jordan) corroborates on a SECOND suppressed-parent case. VERDICT = `absorption_remains_narrow` (the expected, publishable honest negative).

  PART 1 (NEW science, fresh GPU whole-text encode): the bias_in_bios PROFESSION is-a hierarchy. 13,843 bios (cap 500/profession, gender-stratified) + 5,000 non-bio negatives (movie+restaurant reviews, same corpus file) encoded by mean-residual / max-latent over all non-special tokens (per-token FVU=0.173, meanL0=76.9 — pipeline correct). 50/50 selection/diagnostic split, stratified by profession. Corpus-only parent = latent 12692 (discriminative bio-vs-review, content-style precision 0.906, held-out recall 0.973, firing-floor pass). The 28-profession HOLE TABLE (held-out) is the headline: every profession has parent recall 0.88-1.00 (max hole 0.116 on 'model'), 0/28 `absorption_type` => `uniform_high_parent_recall_no_absorption`: a general occupation parent fires on ~all professions with NO suppressed hole for a specialist to fill => absorption does NOT generalize to a clean is-a hierarchy. Baseline comparison on the largest-hole profession 'model' (one-vs-rest, DESCRIPTIVE): the set-cover unit degenerates to the bare parent (AUC 0.308) and is BEATEN by g=top-20 marginal-attr (0.544) and the non-SAE dense difference-probe (0.961); set_cover_established=False — the honest contrast showing the two-track method only helps when an absorption signature exists.

  PART 2 (CPU, iter-4 taxonomic cache): re-running reproduces iter-4 EXACTLY. `absorption_type` (parent recall-hole>0.5 AND specialist firing-Jaccard<0.10) is True for exactly {Georgia, Jordan}, both suppressed-parent homographs; {Chile,Turkey} are homographs the parent covers; 48 non-homograph countries (incl. United States = co-firing/splitting) are not. Entity-token scan over 20 country-mention surfaces with >=150 occurrences: only Georgia qualifies (Jordan n=124<150) => no new case; coverage-limited (testbed labels per-country not per-city).

  PART 3 (CPU): Jordan-beside-Georgia side-by-side. Georgia (n=150, eligible, hole 0.80, J=0.059, unit AUC 0.995, set_cover_established=True) beats every label-free/attribution baseline with paired-bootstrap AUC-diff CIs (B=10,000) excluding 0: S-rec +0.307[0.267,0.348], S-prec +0.416[0.382,0.448], S-mag +0.294[0.254,0.334], RE-k-anch +0.082, g +0.577, h +0.612; non-SAE dense probe still slightly edges it (-0.005[-0.008,-0.003], honest). Jordan (n=124, descriptive, hole 0.71, J=0.021, AUC 0.957). United States (n=150, J=0.204, hole 0.23, NOT absorption).

  BASELINES held side-by-side in one pipeline: two-track set-cover UNIT vs raw-SAE {anchor, g top-20 marginal-attr, h count-matched, S_rec/S_prec/S_mag label-free selectors, RE-k-anchored} vs non-SAE {dense difference-of-means probe}. Result reproduced deterministically across two runs (cache-reuse re-run identical).

  DELIVERABLES: method.py (orchestrator + baselines), profession_absorption.py (Part 1: whole-text encoder, corpus-only parent ID, 28-profession hole table, per-profession set-cover/selection-isolation), engine.py (iter-4 method reused verbatim for the taxonomic cache path). method_out.json (+ full/mini/preview) validate against exp_gen_sol_out (all PASS, 2.85 MB <100 MB); metadata.per_family.{professions,taxonomic} carries the full 28-row hole table, parent, set-cover with CIs, homograph cross-tab, entity scan, side_by_side, honest_negatives; datasets[].examples carry per-row predict_{unit,anchor,g,h,dense_probe,rek,S_rec,S_prec,S_mag} (2,750 profession one-vs-rest rows + 424 Georgia/Jordan/US rows). results/*.csv (hole_table_professions, setcover_auc_diff_model, side_by_side_jordan_georgia, homograph_crosstab). FOR DOWNSTREAM PAPER: this corroborates that SAE feature absorption is specific to suppressed-parent homograph polysemy, NOT a general is-a/taxonomic phenomenon; affirmative non-spelling set-cover evidence remains ONE eligible slice (Georgia), 1-2 counting descriptive Jordan — report as a scoped, honest finding. SAE: gemma-scope-2b-pt-res-canonical layer_12/width_16k/canonical (avg L0 82), seed 20240617, GPU NVIDIA L4 (sm_89); re-runs GPU-free (encodings cached).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_5/gen_art/gen_art_experiment_4
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 27 ---
id: art_-k4Yg-l4NaNO
type: evaluation
in_dependencies:
- id: art_sxwT7hK6YFEA
  label: fdr-repairs
  relation_type: differences
  relation_rationale: >-
    Recomputes 22 distinct holes (not 30) and 2 non-hole survivors, correcting the FDR-count framing.
- id: art_0CZwPjG2YMCf
  label: selectivity
  relation_type: differences
  relation_rationale: Shows '1452x median' is the MEAN and precision-vs-selectivity rho=0.90 not 1.0.
- id: art_JMA2gBvnakAm
  label: firstletter-transparency
  relation_type: uses
  relation_rationale: >-
    Recomputes first-letter compact-vs-15wide AUC deltas and confident-label fractions (reproduce).
- id: art___vgSpUe6wAF
  label: taxonomic-transparency
  relation_type: uses
  relation_rationale: >-
    Recomputes taxonomic held-out per-member precision and member-labeling (reproduce).
title: >-
  M3/M4/M5/M8 honest-counting, selectivity, control & transparency consolidation eval
summary: |-
  Pure-analysis ($0, CPU-only, no LLM/GPU) read-only evaluation that recomputes the four iter-4 reviewer-flagged headline numbers directly from the stored experiment JSONs (D1 art_sxwT7hK6YFEA, D2 art_0CZwPjG2YMCf, D3 art___vgSpUe6wAF, D4 art_JMA2gBvnakAm) and serializes them as drop-in, cross-checked statements. eval.py loads each full_method_out.json, traverses defensively, and emits eval_out.json (schema exp_eval_sol_out PASSED; 91KB) with metrics_agg (25 scalars), 5 datasets (M3 survivor_table 30, M4 cases 7, M5 percentile_evidence 28, M8 first-letter 5 + taxonomic 4), and rich M3/M4/M5/M8 + cross_checks blocks under metadata.

  KEY CORRECTED NUMBERS (every value COMPUTED then compared to stored expectations; mismatches reported, never overwritten). M3 honest counting: 69 repair variants tested, 30 survive BH-FDR<=0.05, spanning 22 DISTINCT recall holes (NOT 23) = 30 - 6 double-count-redundant - 2 non-hole survivors; reconciliation balances. The 6 identical-latent double-counts are exactly Georgia/16009, Jordan/540, United States/846, date/8684, decimal/7983, ordinal/13658 (kg_ktrack==kg_diagnostic). HONEST DEVIATION from plan: there are 2 non-hole survivors, not 1 — numeric/percent (lat 9112) AND L/layer (lat 2378, anchor already recalls 'layer' at 1.0 on the selection fold), so per-family distinct holes are spelling 13 (not 14), taxonomic 3, numeric 6. M4 selectivity: absorption set n=6 mean=1452.5x / median=1262.2x; cleanly-surgical set n=5 (excludes partial-surgical US-4760 at 7.8x) median=1722.5x — the draft's '1452x median' is the MEAN of the n=6 set. Spearman precision-vs-selectivity: all-7 rho=0.679, absorption-6 rho=0.714, within-taxonomic-5 rho=0.900 (p=0.037) — NOT 1.0, because US-846 (prec 0.973) has lower selectivity (213.5) than Georgia (prec 0.955 -> 1722.5); the softened verdict and paper_wording use the actual 0.90. Cross-family counterexample confirmed: spelling large (prec 0.571 -> 802x) beats taxonomic US-4760 (prec 0.709 -> 7.8x). M5 control wording: implemented control is a random SINGLE content-responsive-latent addition (method.py lines 617-621: ctrl_detect=base[:,None]|ctrl_fire is per-latent; pct=(ctrl_gain<gain_kg).mean()); no union/max-pool exists. All 28 surviving hole-variants clear the single-latent p95 (frac 1.0); 23/28 clear p99 (frac 0.821); Georgia pct=0.9939. The misleading docstring phrase 'every OTHER content-responsive latent (the full random-addition population)' at lines 19-20 is flagged for removal. M8 transparency: first-letter compact-vs-15-wide AUC deltas -0.056..-0.200 (all CIs exclude 0 = auditability cost); 15-wide confident-fraction L .867/O .8/T .933/I .867/D .667; taxonomic held-out per-member precision with gate-fold=selection/report-fold=heldout (16009 .968/.955, 540 .992/.975, 846 .993/.973, all pass >=0.70 heldout); member-labeling agreement 0.730 vs shuffle null 0.096, gap 0.634 CI [0.545,0.724]; characterized-subset fractions per letter scope the auditability claim.

  cross_checks: 35/38 pass; the 3 'fails' are the honest expected-vs-actual discrepancies (n_distinct_holes 22 vs ~23, non_hole_survivors 2 vs 1, taxonomic rho 0.90 vs 1.0), each carrying an explanatory note — this is the integrity-lock working as designed, surfacing that the iter-4 draft framing needs these exact edits. Outputs: eval.py, eval_out.json + full/mini/preview_eval_out.json (all schema-valid), pinned pyproject.toml (numpy==2.1.3, scipy==1.14.1, loguru==0.7.2). Paper-writing can drop the M3/M4/M5/M8 paper_wording strings in verbatim to preempt the reviewer minors.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_5/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

--- Item 28 ---
id: art_y_5u-bfJOq3V
type: research
in_dependencies:
- id: art_QBxBPF-9Ldxe
  label: prior-audit
  relation_type: extends
  relation_rationale: >-
    Extends the iter-4 audit with M1 unlearning + M2 width-dependence positioning and new locked cites.
- id: art_i-tkvFCKneA-
  label: prior-audit
  relation_type: extends
  relation_rationale: Builds on the iter-3 citation audit without redoing settled entries.
title: >-
  CCRG iter-5: M1 Unlearning Positioning, M2 Absorption Width-Dependence, Locked Cites
summary: >-
  Positions the two new iteration-5 results of the Counterfactual Co-Response Grouping (CCRG) paper against the right literatures
  and finalizes the venue-locked citation set for GEN_PAPER_TEXT. Pure web research, $0, no code; builds on iter-3 (art_i-tkvFCKneA-)
  and iter-4 (art_QBxBPF-9Ldxe) without re-doing settled entries. THREE deliverables. (A) M1 = a KG-named single-ABSORBER
  edit claimed to beat a dense diff-of-means / LEACE whole-concept-erasure baseline on a joint within-hierarchy-collateral
  + fluency metric at matched on-target (forget) effect. VERDICT: DISTINCT but must be framed NARROWLY. The broad claim 'an
  SAE-feature intervention can beat a dense baseline on unlearning/steering' is CONTESTED, not unprecedented: Farrell/Lau/Conmy
  (2410.19278, NeurIPS-2024 Safe-GenAI Workshop) report multi-feature SAE unlearning has side-effects >= RMU and that SAE
  quality must improve to match fine-tuning, and AxBench/Kantamneni concede dense beats SAEs on aggregate -- BUT CRISP (2508.13650,
  ACL 2026), SAUCE (ICCV 2025, VLM), SSPU (2505.24428, EMNLP 2025) and SRMU (2512.16297) all claim utility-preserving SAE-unlearning
  wins on WHOLE concepts. The defensible novelty is the CONJUNCTION none combine: (1) regime = single SUB-CONTEXT removal
  WITH PARENT preservation on the SAME hierarchy (where a dense whole-concept direction structurally over-shoots); (2) unit
  = ONE KG-NAMED absorber latent DISCOVERED (not pre-known) -- directly answering the 'Use SAEs to Discover, not Act' framing
  threat (2506.23845, Peng et al.); (3) metric = within-hierarchy sibling+parent collateral mapped onto the established forget-quality/retain-utility/fluency
  Pareto triad (WMDP=ICML2024, TOFU=COLM2024, MUSE=ICLR2025, RWKU=NeurIPS2024-D&B, SHRED 'new Pareto frontier' 2605.07482,
  survey 2601.13264). Three adversarial disprove searches returned only whole-concept removal (SAUCE/SAeUron/CRISP/Harry-Potter-ablation)
  and non-archival single-feature steering near-misses (GDM anger feature; ETH SAE-vs-MeanActDiff) -- no archival precedent
  for the conjunction. Honest concession + scope guardrail + 'if it fails reframe to auditability' contingency provided. (B)
  M2 = cross-dictionary (65k-width and/or second-layer) replication is the literature-PREDICTED robustness axis with a SIGNED
  prediction: SAEBench (2503.09532) states verbatim 'Feature Absorption ... scores degrade at larger widths' and 'Absorption
  scores worsen with increased dictionary size for all architectures except Matryoshka' and 'Unlearning effectiveness is best
  at earlier layers and varies significantly by layer' (width series 4k/16k/65k at layers [5,12,19]); Feature Hedging (2505.11756)
  gives the two-sided law (absorption worse WIDER, hedging worse NARROWER, 'width is not a neutral hyperparameter'); Matryoshka
  (2503.17547) gives the dictionary-size law + a non-spelling 'Lily/female-names' absorption hole. So 16k->65k should show
  MORE absorption (the CCRG phenomenon stronger), making replication the expected outcome and non-replication itself a publishable
  dictionary-dependence finding. Feasibility confirmed: Gemma-Scope has 65k residual SAEs at ALL gemma-2-2b layers (Neuronpedia)
  + width series at layers 5/12/19; numeric-digit reconstruction <0.9 caveat has NO literature basis -> gate the numeric arm
  on measured cosine. (C) Citation finalization: carries forward every iter-3/iter-4 lock; adds 13 verified M1/M2 cites with
  IDs/venues/authors; KEY CORRECTION: SAUCE arXiv 2503.14530 is WITHDRAWN but an ICCV 2025 CVF camera-ready exists -> cite
  CVF; CRISP UPGRADED to ACL 2026; SSPU=EMNLP 2025; Farrell=NeurIPS 2024 Safe-GenAI Workshop; possible Deng NeurIPS-2025 upgrade
  flagged (verify track); BibTeX block + corrections diff + extended presentation-strip checklist provided. Outputs research_out.json
  + research_report.md (sections A-D).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_5/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

--- Item 29 ---
id: art_2xQn686KUmV5
type: dataset
in_dependencies:
- id: art_I2MrezW41iQo
  label: guidance
  relation_type: uses
  relation_rationale: >-
    Builds the homograph entity testbed per the dossier's absorption-diagnostic + data-sourcing guidance.
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
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_5/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

--- Item 30 ---
id: art_3WXWsaSoGMnK
type: experiment
in_dependencies:
- id: art_t2uUbjSwpd3t
  label: taxonomic-data
  relation_type: uses
  relation_rationale: >-
    Uses taxonomic Georgia/US country contexts as forget/retain targets for the unlearning edit.
- id: art_dpYpjSn2Xvg3
  label: spelling-data
  relation_type: uses
  relation_rationale: Uses first-letter 'large' spelling contexts as the absorption unlearning case.
- id: art_8QO7pl6Pd8UQ
  label: toxicity-data
  relation_type: uses
  relation_rationale: Uses toxicity insult as the predicted co-firing negative-pole unlearning case.
- id: art_RidEJtBC7gPT
  label: method
  relation_type: uses
  relation_rationale: >-
    Reuses the dossier's units/edit operators (core.py) for the KG-ABL vs u_sub test.
title: 'M1'': KG single-absorber unlearning vs a sub-context-targeted dense baseline'
summary: >-
  M1' replaces the near-tautological WHOLE-PARENT dense comparator of iter-5 with a STRONGER, sub-context-targeted dense baseline
  u_sub = diff-of-means(target-sub-context-positive, sibling-positive in the same parent context), fit on a DISJOINT fold
  from the per-sub-context labels the testbeds carry. The decisive downstream test is selective sub-concept UNLEARNING: at
  MATCHED forget-quality (next-token KL on held-out FORGET windows, matched_target = 0.8*min(maxKG,maxSUB)), it compares KG-ABL
  (ablate one KG-named absorber, h -= lambda*z_l*W_dec[l], gated by the latent's own sparse firing) against the DECISIVE DENSE-SUB-ABL
  (erase u_sub) and a clearly-labeled SECONDARY DENSE-WHOLE-ABL (erase the whole-parent diff-of-means), plus RAND and (M7)
  KG-ABL-UNIT. The joint (retain-utility x fluency) outcome is scored by an AxBench-style OpenRouter judge (anthropic/claude-haiku-4.5)
  with paired-bootstrap KG-vs-SUB CIs (B=10000), curve-dominance, and model-internal corroboration (continuation PPL + retain
  next-token KL). Per-case FORK verdict: KG_BEATS_USUB (joint CI excl 0 favoring KG AND a 2nd-family judge CI also excl 0),
  KG_MATCHES_USUB_LABEL_FREE (CI includes 0 - KG matches u_sub WITHOUT needing the labels), or KG_LOSES_TO_USUB. RESULTS (full
  run, both judges, $0.53/1459 calls): GATE PASSED. The two ABSORPTION cases are both KG_BEATS_USUB - taxonomic Georgia(16009)
  and first_letter large(8463) - each with u_sub localizing better than whole-parent and the M7 win tracing to the SINGLE
  discovered absorber (the multi-member K-track unit only adds collateral); human-proxy spot-checks pass. Folded-in modules:
  (M1') u_sub localization validation is CURVE-BASED over the achievable dense forget range (the KG-pinned matched point is
  tiny because KG single-latent next-token KL has a small ceiling, so a single-point check is mis-specified) - this DELETES
  the false 'a single dense hyperplane cannot localize' framing and reframes KG's edge as sparse-firing GATING (token footprint
  -> 0 for absorption), NOT the dense direction failing to localize; (M5) United States(846) is a ROUTER FALSE-NEGATIVE reclassified
  to co-firing - its absorber footprint is low/surgical-looking but the small parent recall-hole (0.197) flags co-firing,
  so it is moved out of the absorption gate; (M6) a second different-family judge (openai/gpt-4o-mini) with Cohen kappa +
  Pearson/Spearman utility correlation keeps a KG win only if its CI also excludes 0, plus a deterministic $0 human-proxy
  check that KG-ABL preserves sibling tokens while DENSE-WHOLE corrupts them; (M7) unit-vs-single ablation. Toxicity_insult
  is the co-firing case where KG is NOT surgical (footprint 0.166, firing-Jaccard 0.882, no recall-hole - the regime mechanism
  holds); it registers KG_BEATS_USUB on the LLM-judge joint but the $0 model-internal joint does NOT corroborate it (CI includes
  0) and u_sub itself fails to localize in co-firing, so it is reported as a weak judge-only edge, not a surgical win, and
  is not counted toward the gate. A per-case mi_corroborates_fork flag is reported (Georgia/US True; large/toxicity False
  - the noisier model-internal proxy is inconclusive there even though both LLM judges agree). Reuses the iter-4/iter-5 Gemma-Scope
  L12/16k JumpReLU engine via core.py (only the multi-latent abl_latent generalization for M7 + WORK repoint). Single GPU
  (NVIDIA L4); $0 model-internal, <$2 LLM judges (hard cap $10). All outputs validate against exp_gen_sol_out: unlearn_per_prompt
  (per (case,role,prompt) with predict_kg_abl / predict_dense_sub_abl / predict_dense_whole_abl / predict_rand / predict_noop
  continuations + both judges' utilities) and kg_vs_dense_per_case (fork verdicts + all decisive CIs).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_6/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 31 ---
id: art_yAQgbq5Wgymx
type: experiment
in_dependencies:
- id: art_8QO7pl6Pd8UQ
  label: identity-data
  relation_type: uses
  relation_rationale: >-
    Builds identity slices inline from the full civil_comments corpus for the safety screen.
- id: art_2xQn686KUmV5
  label: entity-testbed
  relation_type: uses
  relation_rationale: Uses the homograph entity testbed as candidate suppressed-parent safety cases.
- id: art_t2uUbjSwpd3t
  label: taxonomic-template
  relation_type: uses
  relation_rationale: Reuses the taxonomic testbed template + Georgia/Jordan positive control.
- id: art_RidEJtBC7gPT
  label: method
  relation_type: uses
  relation_rationale: >-
    Reuses iter-5 core.py edit/curve/bootstrap engine verbatim for the downstream test.
- id: art_I2MrezW41iQo
  label: diagnostic
  relation_type: uses
  relation_rationale: Uses the form-free absorption-fraction oracle to corroborate flagged edges.
title: >-
  Safety-Attribute SAE Absorption Screen + Sub-Context Dense-Direction Unlearning Test
summary: |-
  M2' answers whether the feature-absorption signature that makes one KG-named SAE latent a SURGICAL unlearning handle (established for the entity homograph Georgia->16009 and first-letter spelling) extends to SAFETY-RELEVANT identity attributes. Two parts, both reusing iter-5 core.py VERBATIM (JumpReLU Gemma-Scope L12/16k SAE d_model=2304, edit hooks, behavioral_curve, paired_bootstrap_diff, _scale_for_on_target) on a single L4 GPU.

  (1) $0 ABSORPTION SCREEN (always emitted). For 4 identity hierarchies (religion / race_ethnicity / orientation_gender / nationality) we build candidate slices INLINE from the FULL google/civil_comments (1.76M rows, CC0) gazetteer-matched windows + deterministic content-flip templates; group labels are surface-form only (never the model, never Jigsaw identity columns). Per hierarchy we find a firing-floor-validated content-responsive PARENT latent and screen every group for the Georgia signature via a vectorised K-track-lite absorber search (firing-disjoint Jaccard<0.1 + hole-covering + precision>=0.7), flagging absorption_structured = recall-hole>0.5 AND Jaccard<0.1 AND >=150 eligible AND precision>=0.7 AND hole-coverage-gain>=0.05 (CI excl 0). Each flagged edge is corroborated by a NON-CIRCULAR form-free absorption-fraction oracle (SAEBench/Chanin-A.13: decoder contribution projected onto a parent LR-probe direction trained on disjoint data; never used to flag).

  HEADLINE FINDING: safety-attribute SAE absorption is HOMOGRAPH-CONFINED. Of 44 eligible safety groups, only 2 are absorption-structured -- white (race; hole .63, Jaccard .019, oracle .46) and straight (orientation; hole .72, Jaccard .009, oracle .26) -- and BOTH are lexical homographs. The other 42 (Muslim/Hindu/Catholic, gay/lesbian/Asian, Mexican/Chinese/Canadian, ...) show NO parent recall-hole: the general identity parent reliably fires on them. Absorption tracks LEXICAL POLYSEMY (like Georgia/Jordan), NOT safety semantics. Positive control reproduces: Georgia recall-hole .76 (flagged), Jordan .66.

  (2) CONDITIONAL DOWNSTREAM (M1', $0.30 of $10 cap). At MATCHED forget-quality, ablating one KG absorber (KG-ABL) vs erasing the SUB-CONTEXT-targeted dense direction u_sub=diff-of-means(target-group, SIBLING-group) -- a sharper comparator than the whole-parent direction iter-5 M1 already beat -- scored on a joint retain-utility x fluency outcome with TWO judges (claude-haiku-4.5 + gemini-2.5-flash), paired-bootstrap Delta_joint CI B=10000, plus a $0 model-internal selectivity/curve-dominance track. overall_verdict = SAFETY_ABSORPTION_FOUND_NO_WIN: the single-absorber surgical win is DECISIVE for the entity homograph Georgia (DOWNSTREAM_WIN_CONFIRMED: retain-collateral KL 3e-5 vs u_sub .078, curve-dominance 1.0, Delta_joint [.53,.96] under BOTH judges) but does NOT robustly transfer to safety -- straight wins under the PRIMARY judge only (small-magnitude matched-forget .0012; second judge borderline, CI incl 0), and white has NO_ON_TARGET_EFFECT (its oracle-confirmed absorber gives no unlearning leverage). Structure != leverage.

  DELIVERABLES: method.py (driver), safety.py (gazetteers, identify_parent, screen_subcontexts, absorption_fraction_oracle), core.py (iter-5 verbatim), prefetch.py, finalize.py, README.md, pyproject.toml (48 pinned deps). method_out.json validates against exp_gen_sol_out: dataset safety_screen (one row per (hierarchy,group), predict_absorption in {ABSORPTION_STRUCTURED, CO_FIRING, NO_HOLE, DESCRIPTIVE_ONLY}, metadata_is_homograph + metadata_absorption_fraction_oracle) and downstream_subcontext (per (candidate,prompt) KG/u_sub/NOOP continuations + per-candidate summary rows). metadata carries overall_verdict, scoping_summary (homograph-confinement), positive_control_reproduced, screens, per_candidate_downstream, honest_negatives, llm_cost_usd. All honest negatives reported verbatim (homograph confinement, straight judge-fragility, white no-leverage, Jordan weak case). Gating reconstruction cosine 0.919.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_6/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 32 ---
id: art_KNPsfjByyxiS
type: dataset
in_dependencies:
- id: art_I2MrezW41iQo
  label: guidance
  relation_type: uses
  relation_rationale: >-
    Builds the safety-identity testbed per the dossier's absorption-diagnostic + data-sourcing guidance.
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
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_6/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

--- Item 33 ---
id: art_F_-HUhl0NR_i
type: experiment
in_dependencies:
- id: art_2xQn686KUmV5
  label: prospective-data
  relation_type: uses
  relation_rationale: >-
    Runs the router prospective expansion + breadth count over the homograph entity testbed.
- id: art_t2uUbjSwpd3t
  label: taxonomic-data
  relation_type: uses
  relation_rationale: Reuses taxonomic Georgia/Jordan as derivation-set absorption anchors.
- id: art_RidEJtBC7gPT
  label: method
  relation_type: uses
  relation_rationale: Reuses the iter-5 a-priori firing-structure router as core.py verbatim.
title: 'M4 Recall-Hole Router: Homograph Prospective Expansion + M7 Absorption Breadth'
summary: |-
  Executes M4 + M7 on the homograph/polysemy entity testbed (art_2xQn686KUmV5), reusing the iter-5 a-priori SAE firing-structure router VERBATIM as core.py and adding a thin method.py (homograph hierarchy loader + per-entity predict-then-measure router + Wilson-CI verdict + breadth count). SAE = google/gemma-scope-2b-pt-res L12/16k JumpReLU on unsloth/gemma-2-2b; SEED=1234; single GPU (NVIDIA L4); $0 LLM. The homograph dataset shipped builder-only (no full_data_out.json), so it was deterministically rebuilt in homograph_build/ (pipeline.py --scale full --no-llm, 34,357 rows, $0).

  INTEGRITY: the FROZEN recall-hole-alone rule, fit ONLY on the 12 derivation concepts (spelling L/O/T/I/D, numeric, taxonomic, 5 toxicity sub-attrs), reproduces iter-5 EXACTLY: tau_h_alone=0.7795 (drift 0.0000), derivation balanced_acc=1.000, LOO=0.833, gating recon-cos=0.927. Every entity regime is PREDICTED and LOGGED before its outcome is measured (predict-then-measure audit trail). Ground-truth regime PRIMARY = sign(auc_unit - auc_a); baselines (a) best raw latent, (h) supervised attribution pool, (d) non-SAE residual probe are reported per entity.

  M4 VERDICT = ROUTER_DEMOTED (honest negative). 34 eligible entities (>=150 diagnostic positives: city 18 / month 12 / given-name 3 / brand 1) — a 5.6x expansion of the iter-5 6-concept set. The router validates on the base-rate co-firing direction (co-firing-predicted 29/30, Wilson95 [0.833,0.994] excludes 0.5) but the DISCRIMINATIVE absorption-predicted stratum does NOT: homograph 2/4 [0.15,0.85]; homograph+7-spelling-letters 5/10 [0.237,0.763] — both include 0.5. So as an a-priori predictor of WHERE label-free grouping helps it is an exploratory diagnostic, not validated. This is the acceptable/publishable negative the plan anticipated and matches the iter-6 consolidation memo's M4 DEMOTE.

  M7 BREADTH (answers the 'absorption is n=1-2' critique with a systematic count): of 64 homograph entities with a stable estimate (n_all>=30), only 3 are absorption-structured (recall-hole>0.5 AND firing-Jaccard<0.1) — ALL months (cities 0/22, given-names 0/20, brands 0/10). NEW named suppressed-parent homographs (beyond Georgia/Jordan, which live in the taxonomic derivation set): March (recall-hole 0.997), June (0.947), February (0.573). The month parent fires on only 0.623 of month mentions vs 0.94/0.92/0.95 for city/given-name/brand, so only months leave holes. STRUCTURAL != DOWNSTREAM: the strongest downstream-confirmed absorption (label-free unit actually beats best raw latent) is month/May, delta_vs_a=+0.160 (the is-a-month parent misses 98% of 'May' mentions, absorbed by the modal verb), even though May is NOT 'structured' (jaccard 0.434); the structurally-shaped months are co-firing downstream. Documented counterexamples re-confirmed: numeric (high Jaccard yet absorption), taxonomic (low Jaccard yet co-firing), spelling F/M/W (recall-hole~1.0 over-predicts absorption).

  DELIVERABLES: method_out.json (+ full/mini/preview, all validate against exp_gen_sol_out, each <0.4MB) with 111 cards (12 derivation + 7 spelling-prospective + 92 homograph entities), each card = {input: router-decision string, output: ground_truth_regime, predict_router: predicted_regime, metadata_*: recall_hole, jaccard, predicted/ground-truth regimes, auc_unit/a/h/d, deltas+CIs, eligibility, absorption_structured, is_prospective_hit}. Rich metadata: frozen_rule, reproduction_check, router_verdict(+rationale), all prospective hitrate strata (primary/combined-with-spelling/ablations/vs-h) with Wilson CIs, absorption_breadth (per-hierarchy + new-suppressed + downstream-confirmed), hierarchy_parents, entity_table, honest_notes. NOTE: two surgical numerical-stability patches over core (NaN/inf-safe residual probe and auc — Gemma massive-activation residual dims overflow float16) and B_BOOT=2000 (plan allows >=2000; CI-width only, point estimates/tau unaffected); core.py stays verbatim. For GEN_PAPER_TEXT: this gives an honest validate-or-demote result + a breadth count that directly rebuts the single-slice critique and names new homograph cases (May the downstream winner).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_6/gen_art/gen_art_experiment_3
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 34 ---
id: art_w7p8du2N1f0Y
type: evaluation
in_dependencies:
- id: art_4L1MZxvWYlGd
  label: crossdict-selectivity
  relation_type: differences
  relation_rationale: >-
    Shows the stored 65k 466997x/3.7e6 selectivity is a divide-by-epsilon artifact; corrects to ~722x.
- id: art_0CZwPjG2YMCf
  label: surgical-selectivity
  relation_type: uses
  relation_rationale: >-
    Recomputes/re-verifies the 16k surgical selectivity (mean 1452x, median 1262x) from its JSON.
- id: art_4q5Om8wdqZuz
  label: router-ci
  relation_type: uses
  relation_rationale: >-
    Recomputes router prospective Wilson CIs (include 0.5) from its output, supporting the demote.
title: >-
  Integrity-Lock Eval: 65k Selectivity Fix, Router Wilson-CI, Honest-Counting Drop-in
summary: |-
  Pure CPU-only ($0, no GPU/encoding/LLM) integrity-lock re-analysis (eval.py) over four frozen JSONs (D1 iter5-exp2 65k cross-dict, D2 iter4-exp2 surgical 16k, D3 iter5-exp3 router, D4 iter5-eval template). Every headline value is COMPUTED then COMPARED to source; mismatches are reported with notes (44 cross-checks, 43 pass; the one mismatch is the intentional honest correction m3_n_floor_limited=2 vs the plan's anchor of 1). Labels mapped by CONTENT, not by D4's differing internal label numbers.

  M3 (NEW, load-bearing): the stored 65k 'absorption mean selectivity 466996.718x' and 'Georgia 3.7e6x' are divide-by-epsilon artifacts (kg_collateral==0 -> ratio=on_target/1e-8; recomputed mean reproduces 466996.718 exactly, confirming the artifact). Excluding floor-limited (kg_coll==0: Georgia/46143, Jordan/60904) and NO_ON_TARGET_EFFECT (60904, on/54546, take/26458) cases, the CORRECTED 65k absorption mean = 721.72x / median 676.33x (n=4 PRIMARY); the lenient rule that excludes only the two artifacts gives 483.06x / 184.61x (n=6 SECONDARY). 65k Georgia (on_target 0.03711 = dense_collateral; floor-limited >= ~371x at 1e-4, or >= ~1290x referenced to the 16k 2.876e-5 collateral) is COMPARABLY surgical to 16k Georgia (1722.46x), NOT ~2000x better. Honest layer-9 note: Georgia loses its hole (0.003) while Jordan keeps it (0.536) with a 2376x surgical edit.

  M4 (NEW): prospective Wilson CIs INCLUDE 0.5 -> absorption-predicted 3/6=0.50 [0.188,0.812], cofiring 8/12=0.667 [0.391,0.862], combined 11/18=0.611 [0.386,0.797]; the vs-h 14/19=0.737 [0.512,0.882] (excludes 0.5) is flagged SECONDARY/non-primary (unit-beats-h ground truth). recall-hole=1.0 over-predicts absorption on new letters F/M/W (which measure co-firing); C/P/R are correct wins -> router is WRONG IN BOTH DIRECTIONS. Run-tree scan found no iter-6 expansion experiment with a CI excluding 0.5 -> DEMOTE to exploratory diagnostic (derivation balanced-acc 1.0, tau_h_alone 0.77949 kept separate).

  M8 (carry D4, RE-VERIFY selectivity from D2): 22 distinct holes = 30 FDR survivors - 6 double-counts - 2 non-hole; per-family distinct 13/3/6, survive-FDR 14/6/10; absorption-6 mean 1452.47x / median 1262.21x (the draft's '1452 median' is the MEAN); surgical-5 median 1722.46x; within-taxonomic Spearman rho=0.90 (NOT 1.0, p 0.037), cross-family counterexample (large prec 0.571 -> 802x beats US-4760 prec 0.709 -> 7.8x); random SINGLE-latent control 28/28 > p95, 23/28 > p99; member-labeling gap 0.6344 [0.545,0.724]; numeric flagged below-gate (digit cosine 0.876 < 0.90). M5: US = CO-FIRING (aggregate recall-hole 0.20-0.23 < tau_h 0.78) yet absorber 846 = 214x surgical -> router FALSE-NEGATIVE (jaccard 0.04 specific vs 0.20 aggregate). M7: two-track = TRAINING-FREE LABEL-FREE DISCOVERY of the single absorber (16009/8463/846), not multi-member grouping; C-track ties weak baselines (toxicity 0.762 vs 0.765); set-cover-specific only on I/D/Georgia.

  Output eval_out.json (exp_eval_sol_out schema, all variants validate, <100MB): metadata blocks M3_selectivity_artifact / M4_router_ci / M8_honest_counting / M5_us_consistency / M7_grouping_reframe / cross_checks, a flat numeric metrics_agg (62 scalars incl. all corrected means, includes_half flags, n_cross_checks/pass), and 5 datasets (M3_selectivity_cases 16, M4_router_prospective_strata 4, M4_new_letter_directionality 7, M8_distinct_hole_survivors 30 reused from D4, M8_selectivity_reverify 7), each example carrying predict_* strings. Provides GEN_PAPER_TEXT with trustworthy, cross-checked drop-in paper_wording for the cross-dictionary and auditability spines.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_6/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

--- Item 35 ---
id: art_3zaa2xXEp8Az
type: research
in_dependencies:
- id: art_y_5u-bfJOq3V
  label: prior-positioning
  relation_type: extends
  relation_rationale: >-
    Extends iter-5 positioning with safety-identity absorption + u_sub label-efficiency framing.
- id: art_QBxBPF-9Ldxe
  label: prior-audit
  relation_type: extends
  relation_rationale: Builds on the iter-4 audit's locked venues without redoing settled entries.
title: 'CCRG iter-6: Safety-Identity Absorption & u_sub Label-Efficiency Positioning'
summary: >-
  Positions the two new load-bearing iter-6 gates of the Counterfactual Co-Response Grouping (CCRG) paper and refreshes the
  venue-locked citation set for GEN_PAPER_TEXT. Pure web research, $0 LLM spend, no code; builds on iter-4 (art_QBxBPF-9Ldxe)
  and iter-5 (art_y_5u-bfJOq3V) without re-doing settled entries. THREE deliverables. (A) M2' SAFETY-RELEVANT IDENTITY ABSORPTION:
  a cite-and-distinguish block over FIVE sub-literatures never previously surveyed -- SAE debiasing (debiaSAE 2410.13146 VLM/COLM-under-review;
  Ahsan&Wallace 2511.00177 ICLR2026 healthcare; SteerRM 2603.12795 reward-model; DeBiasLens 2602.24014 VLM/CVPR2026-flag),
  model-editing for stereotype (BiasEdit 2503.08588 TrustNLP@NAACL2025; Collapsed-LMs 2410.04472 ICLR2025), fairness/concept-erasure
  editing (Karvonen&Marks 2506.10922 NeurIPS2025 Mech-Interp-WS affine edit; SPLINCE 2506.10703 NeurIPS2025; H-SAL 2606.12088),
  identity/entity/PII unlearning (Entity-Level-Unlearning COLING2025; Not-Every-Token 2506.00876; DFSU 2601.15595), and example-reweighting
  debiasing (JTT/GEORGE/EIIL/LfF, carried). VERDICT: CCRG's three-part conjunction -- a DISCOVERED single absorber latent
  for ONE identity sub-context + a PARENT-preserving sub-context edit + scoring vs a SUB-CONTEXT-targeted dense direction
  u_sub -- is distinct from all five (each edits a WHOLE attribute/entity/example-set and preserves UNRELATED material; closest
  near-miss Ahsan&Wallace steers a single race-latent that CO-FIRES with 'incarceration' = entanglement not absorption, and
  concedes SAE steering is 'of marginal utility for realistic tasks'). Both-branches honest-null framing supplied (safety-WIN
  vs absorption-not-exhibited NULL bounded to the auditable edit primitive, connected to the existing 0/28-professions + toxicity-co-firing
  negatives). (B) M1' u_sub LABEL-EFFICIENCY: RETIRES the now-FALSE 'a single dense hyperplane structurally cannot localize
  to a sub-context / erasing the is-a-country direction removes all countries' argument -- u_sub IS a dense hyperplane and
  DOES localize, the testbed already carries its labels, and SPLINCE (preserves covariance with target label), Karvonen&Marks
  (affine edit, bias <2.5%, perf maintained) and H-SAL (label-free matches label-based) externally prove a labeled dense direction
  localizes/preserves utility. Supplies an exact DELETE/REPLACE list + BOTH M1' fork paragraphs (FORK-WIN: discovered single
  feature beats sub-context-labeled dense; FORK-MATCH: matches u_sub WITHOUT sub-context labels = label-efficiency/discovery,
  grounded in Peng 'Discover-not-Act' 2506.23845 verbatim thesis + label-free SAE 2506.01247) + an honest cost note (counterfactual-pair
  cost of grouping vs sub-context-label cost of u_sub). (C) CITATION REFRESH: 14 new grep-verified entries + carry-forward
  flags RESOLVED (Deng 2506.18141 UPGRADE->ACL2026; SAEmnesia 2509.21379 UPGRADE->ICML2026; SNCE 2509.21008 authors confirmed;
  Muchane 2506.01197 keep-preprint), BibTeX, corrections diff, unresolved-flags list, and an updated presentation-strip checklist.
  Outputs research_out.json + research_report.md (sections A-D).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_6/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

--- Item 36 ---
id: art_Cgk9ETiZfvtl
type: experiment
in_dependencies:
- id: art_t2uUbjSwpd3t
  label: taxonomic-data
  relation_type: uses
  relation_rationale: >-
    Uses taxonomic Georgia/US country contexts as forget/retain targets for the gated-dense edit test.
- id: art_dpYpjSn2Xvg3
  label: spelling-data
  relation_type: uses
  relation_rationale: >-
    Uses first-letter 'large' spelling contexts as the concentrated absorption edit case (the headline win).
- id: art_8QO7pl6Pd8UQ
  label: toxicity-data
  relation_type: uses
  relation_rationale: >-
    Uses toxicity insult as the concentrated co-firing comparison case (which also wins).
- id: art_2xQn686KUmV5
  label: homograph-data
  relation_type: background
  relation_rationale: >-
    Homograph entity testbed was the candidate edit-case pool; month case dropped (its data_out.json unmaterialized).
- id: art_RidEJtBC7gPT
  label: method
  relation_type: extends
  relation_rationale: >-
    Reuses dossier units/operators (core.py) and ADDS the new gated DENSE-SUB-ABL-GATED operator + tau calibration.
title: M1'' Gated-Dense Control + Honest Forget Test of KG Single-Absorber Suppression
summary: |-
  iter-7 M1'' decisively stress-tests the auditability-first two-track CCRG claim that ablating ONE KG-named absorber latent (KG-ABL) is a better unlearning handle than a dense baseline. It adds the FAIR control iter-6 lacked and an honest operating-point protocol.

  NEW OPERATOR (core.py): DENSE-SUB-ABL-GATED (kind='erase_dir_gated') erases the sub-context diff-of-means u_sub ONLY where |h.u_sub|>tau; tau is calibrated (calibrate_gate_tau) so the gate's global firing fraction over a neutral pool equals the KG absorber's token footprint f_kg. This removes the iter-6 confound (KG edits ~1-3% of tokens; ungated u_sub edits every token). tau threaded through make_edit_hook/forward_pos_logprobs/behavioral_curve/side_effects/generate_under_edit/last_tok_logprobs. FIVE operators at the SAME swept matched forget: NOOP, KG-ABL, DENSE-SUB-ABL-GATED (decisive), DENSE-SUB-ABL (ungated, iter-6, secondary), DENSE-WHOLE-ABL (secondary), +RAND +KG-ABL-UNIT (M7).

  HONEST OPERATING POINT: per case we report max_forget_{kg,sub,gated,whole} (KG's next-token-KL ceiling is 17-30x smaller than the dense directions'), NOOP-identical fraction (KG is NOOP-identical on ~0.89 of FORGET prompts for the country cases), full collateral-vs-forget curves, a gate footprint sweep {0.5,1,2,4}*f_kg, matched_target=0.8*min(max_kg,max_gated), and op_high=0.95*max_kg.

  MEANINGFUL-FORGET PROOF ($0, deterministic, the key addition): (a) completion-accuracy drop = drop in gold-token log-prob on hand probes (capital-of-Georgia->Tbilisi, large->L, etc) with bootstrap CI; (b) frozen 1-D-free sub-probe d_sub (AUC~1.0) scored on the REAL post-edit residual via read_resid_under_edit; meaningful_forget[op] = (completion CI>0) OR (sub-probe positive-rate drop>=0.1). Decisive pair KG-ABL vs DENSE-SUB-ABL-GATED via paired_bootstrap_diff (B=10000) on the joint (retain-utility x fluency) outcome under TWO OpenRouter judges (claude-haiku-4.5 + gpt-4o-mini).

  PER-CASE 3-WAY FORK: KG_BEATS_GATED_DENSE_AT_MEANINGFUL_FORGET / GATED_DENSE_CLOSES_GAP_DISCOVERY_IS_THE_VALUE / NO_MEANINGFUL_FORGET_SCOPE_TO_PARTIAL_SUPPRESSION. Aggregate requires absorption advantage to EXCEED co-firing advantage; a US-excluded gate counts only powered absorption cases.

  RESULTS (5 cases, 2109 judge calls, $0.80 << $3 target; overall=SPARSE_SAE_HANDLE_ESTABLISHED, absorption_exceeds_cofiring=True, adv 1.58>0.37): (1) first_letter_large (spelling absorber 8463) = KG_BEATS_GATED_DENSE: KG meaningfully forgets (sub-probe drop 0.42, completion 0.11) AND beats the footprint-matched gated dense by +1.58 joint under BOTH judges with strictly lower collateral (CI excl 0) and 1.0 curve dominance -- a discovered single SAE feature beats a labeled+footprint-matched dense control. (2) taxonomic_georgia (16009) and taxonomic_jordan (540) = NO_MEANINGFUL_FORGET: the single-latent ablation CANNOT remove the DISTRIBUTED country sense even at full strength (max_kg 0.065/0.114, sub-probe drop 0.07/0.0); this directly EXPOSES that iter-6's KG_BEATS_USUB headline sat at a near-NOOP operating point (KG won by barely editing). (3) taxonomic_us (846) = NO_MEANINGFUL (co-firing). (4) toxicity_insult (13367) = KG_BEATS_GATED (+0.47) but co-firing, so excluded from the absorption gate. The month case was dropped because the iter-5 homograph month dataset's *_data_out.json artifacts were never materialized on disk; absorption set = {Georgia, large, Jordan}.

  OUTPUT (exp_gen_sol_out, validated full/mini/preview, 0.8MB): metadata.per_case (all operating points, gate tau sweep + footprint used, NOOP-identical, completion/sub-probe drops, meaningful_forget, collateral & joint CIs KG-vs-GATED decisive + KG-vs-SUB/WHOLE secondary + gated-vs-ungated, full-range collateral curves, M5/M6/M7, fork_verdict); metadata.summary (3-way fork counts, adv_absorption/adv_cofiring, absorption_exceeds_cofiring, us_excluded_gate, overall_verdict); 11 honest_negatives; datasets gated_dense_per_prompt (288 rows, predict_kg_abl/predict_dense_sub_gated/predict_dense_sub_abl/predict_dense_whole_abl/predict_noop + per-op judged utilities + NOOP-identical + model-internal signals) and kg_vs_gated_per_case (5 rows). For the paper: the honest, feature-dependent conclusion is that the single-SAE-absorber handle genuinely beats a fair dense control ONLY for concentrated features (spelling); for distributed taxonomic/co-firing senses it is clean low-collateral PARTIAL suppression, not meaningful unlearning.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_7/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 37 ---
id: art_IlzAiXYWeUYH
type: research
in_dependencies:
- id: art_3zaa2xXEp8Az
  label: prior-positioning
  relation_type: extends
  relation_rationale: >-
    Extends iter-6 positioning with the gated-dense prior-art survey + localization-first reposition.
- id: art_y_5u-bfJOq3V
  label: prior-positioning
  relation_type: extends
  relation_rationale: Builds on iter-5 positioning/locked citations without redoing settled entries.
title: 'CCRG iter-7 Positioning: Gated-Dense Prior Art, Localization-First Reposition'
summary: >-
  Positions the iteration-7 CCRG paper and refreshes the venue-locked citation set for GEN_PAPER_TEXT. Pure web research,
  $0, no code; builds on iter-5 (art_y_5u-bfJOq3V) and iter-6 (art_3zaa2xXEp8Az) without re-doing settled entries. FIVE deliverables.
  (A) GATED/CONDITIONAL ACTIVATION-EDITING SURVEY (the new load-bearing piece): VERDICT = gating a dense edit by a sparse/threshold
  detector is ESTABLISHED PRIOR ART, and the exact gated-dense operator the paper uses as a control is already published,
  so DENSE-SUB-ABL-GATED is a CONTROL, not a contribution. Four verified cites: CAST (2409.05907, ICLR 2025 Spotlight; condition-vector
  switch over the prompt's hidden state, gate fit on LABELED example sets), GUARD-IT (2605.12765, preprint; Sentence-Transformer
  Similarity Gate K(x)={j:sim(c_j,phi(x))>=T} over LABELED-forget clusters + norm-preserving rotation h'=(h-a*vhat)*||h||/||h-a*vhat||),
  GSS (2602.08901, preprint; the EXACT operator h'=h-G(|u^T h|>eps)*v Eq.3 / multi-component Eq.14, probe u + steer v OPTIMIZED
  on 1,000 memorization-labeled sequences with eps tuned to the 95th percentile), SADI (2410.12299, ICLR 2025 Poster; dynamic
  per-input steering via a contrastive-pair binary mask). The PLAN MIS-ATTRIBUTED the |u^T h|>eps formula to GUARD-IT; it
  is actually GSS (corrected). In ALL prior methods the gate is SUPERVISED; the SAE-specific contribution is therefore the
  TRAINING-FREE, LABEL-FREE DISCOVERY of WHERE to gate (the precise sub-context absorber marginal-attribution drops) plus
  the absorber's calibrated JumpReLU firing as a built-in calibration-free gate, grounded in Peng 'Discover-not-Act' (2506.23845).
  BOTH M1'' fork paragraphs supplied (WIN: discovered sparse handle beats even gated dense, advantage larger on absorption
  than co-firing cases => traces to structure not footprint; MATCH: gating not SAE-specific => value=label-free discovery;
  plus fallback FORK-c near-NOOP => scope to selective partial suppression). (B) LOCALIZATION-FIRST REPOSITION: drop-in abstract
  spine + intro opener leading with training-free auditable LOCALIZATION of homograph-polysemy absorption, stating localization-NOT-classification
  up front (toxicity unit AUC 0.762 ties/loses raw latents, trails dense 0.84-0.89; sub-attrs 0.63 vs 0.93), presenting the
  44-group safety screen (2/44 = white/straight, both homographs) as the HEADLINE LIMITATION-and-finding (absorption=lexical
  polysemy not demographic semantics; Ahsan-Wallace co-firing corroborates), naming the durable contribution triad (label-free
  discovery+editable feature-KG; a-priori recall-hole diagnostic=exploratory; absorption-regime selection wins). (C) METHOD-IDENTITY
  REFRAME: foreground single-absorber discovery (anchored set-cover effectively k=1; unit-vs-single-best-absorber ablation
  art_3WXWsaSoGMnK shows single absorber WINS; M7 multi-member adds collateral), demote multi-member grouping + C-track to
  secondary, 5 retitle options. (D) CLARITY FIXES: ONE canonical Georgia number (+0.561 CI[0.318,0.811], 2nd judge +0.465
  CI[0.289,0.658]) + exact footnote for the +0.743 safety-section re-run; concept-space-KL (u_sub 0.078 < whole-parent 0.102)
  vs judged-collateral (util_SUB 1.17 < util_whole 1.33, inverts) drop-in. (E) CITATIONS: inherited locked table carried forward
  verbatim + 6 new gated-steering cites with verified IDs/venues/full author lists + new-cite BibTeX + unresolved-flags list
  + 10-item presentation-strip checklist. Outputs research_out.json + research_report.md (sections A-E).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_7/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

--- Item 38 ---
id: art_ZxVw0e4seBq3
type: experiment
in_dependencies:
- id: art_KNPsfjByyxiS
  label: safety-data
  relation_type: uses
  relation_rationale: >-
    Consumes the previously-unused named_entity_safety hierarchy for the homograph screen + downstream.
- id: art_I2MrezW41iQo
  label: diagnostic
  relation_type: uses
  relation_rationale: >-
    Uses the form-free absorption-fraction oracle to corroborate the flagged named-entity edges (3/3).
- id: art_RidEJtBC7gPT
  label: method
  relation_type: extends
  relation_rationale: >-
    Reuses iter-5/6 engine and ADDS the erase_dir_gated operator + footprint-matched calibrate_gate primitive.
title: Named-Entity Homograph SAE Absorption Screen + Gated-Dense Unlearning Downstream
summary: |-
  M2'' CONFIRMATORY (supporting, not load-bearing) experiment on Gemma-2-2b + Gemma-Scope L12/16k JumpReLU SAE (gating cosine 0.92, layer hidden_states[13]). It consumes the previously-unused named_entity_safety hierarchy (art_KNPsfjByyxiS) and reuses the iter-5/6 engine verbatim (core.py, method_iter6.py) with two genuinely-new pieces: a $0 absorption SCREEN (screen.py) and a NEW gated-dense edit operator 'erase_dir_gated' + a footprint-matched gate-calibration primitive (calibrate_gate) added to core.py.

  THESIS TESTED: feature absorption = LEXICAL HOMOGRAPHY (a suppressed 'named-entity/org' parent latent under a polysemous surface token), NOT safety/demographic semantics. A single coherent content-responsive parent latent (2768; xon-recall 0.99, probe AUC 1.0, not diffuse) was identified non-circularly (recall-only + >5% firing-floor). Per eligible entity the screen computes, with the absorber chosen on the diagnostic fit fold and every metric scored on the disjoint train fold: recall-hole, K-track-lite absorber, firing-Jaccard(parent,absorber), held-out precision, hole-coverage-gain with bootstrap CI, and a form-free decoder-probe-cosine oracle (Chanin/SAEBench, tau 0.025). 'absorption_structured' is gated on the firing-signature (the canonical iter-2..6 definition the Georgia positive control satisfies); the form-free decoder-projection oracle is reported separately and confirms 3/3 named-entity hits (it is spelling/concept-tuned and does not transfer to the taxonomic Georgia absorber, which would be wrongly rejected if it gated the verdict).

  PRIMARY RESULT ($0 screen): 3/5 eligible named-entity homographs are absorption-structured AND oracle-confirmed: Amazon (hole 0.61, jac 0.048, prec 0.99, gain 0.61 CI>0, dec-cos 0.12), Bush (0.79/0.021/1.00/0.79, 0.04), Cook (0.72/0.045/1.00/0.70, 0.03). Apple (hole 0.25) and King (0.42) are NOT structured (the parent detector fires on them). Four descriptive-only homographs (West, Bell, Hunt, Banks) show the relaxed signature (n<150). The Georgia self-check PASSED (the identical screen flags the canonical taxonomic absorber 16009 structured). This reinforces the settled iter-6 demographic null: absorption tracks lexical polysemy.

  CONDITIONAL DOWNSTREAM (supporting; both judges claude-haiku-4.5 + gpt-4o-mini, $0.35 total, 949 calls): at matched forget (0.8*min(maxKG,maxSUB)) with an edit-vs-NOOP forget delta, four operators KG-ABL / DENSE-SUB-ABL / DENSE-SUB-ABL-GATED (footprint-matched gate, balanced-acc 0.95-0.97) / DENSE-WHOLE-ABL. Amazon = KG_BEATS_GATED_DENSE (non-trivial forget: median KL 0.58, 58% prompts changed; KG-vs-GATED joint CI [0.41,1.08] and 2nd-judge CI [0.35,0.68] both exclude 0; curve-dominance 1.0) -> a genuine NAMED_ENTITY_HOMOGRAPH_WIN. Bush = KG_MATCHES_GATED_DENSE (non-trivial forget, label-free parity). Georgia control = NEAR_NOOP_NO_WIN (KG cannot forget non-trivially at the matched point; the iter-5/6 Georgia 'win' was lower-collateral, not strong forgetting). Notably the named-entity absorber 6846 is a STRONGER edit handle (max_kg 1.14) than the country absorber (0.064).

  VERDICTS: overall_verdict = SAFETY_ABSORPTION_HOMOGRAPH_CONFINED (demographic null unchanged); secondary_tag = NAMED_ENTITY_HOMOGRAPH_WIN_FOUND. 8 honest negatives recorded (confirmatory framing, oracle scope/decoder-tuning, Bush parity, Georgia NEAR_NOOP context, named-entity-vs-country edit-handle strength).

  DELIVERABLES: method.py (driver), screen.py (screen), core.py (engine + erase_dir_gated + calibrate_gate), method_iter6.py (reused engine). method_out.json (+ full/mini/preview, all PASS exp_gen_sol_out, <=208KB) holds metadata.{screen_table, breadth_count, georgia_sanity, parent_identification, downstream (per-case matched_target, max_forget_kg/sub/gated/whole, full_range_collateral_curve, edit_vs_noop_forget, gate_calibration, joint CIs KG-vs-{GATED,SUB,WHOLE} under both judges, curve_dominance), overall_verdict, secondary_tag, honest_negatives, llm_cost_usd}. Three datasets: named_entity_absorption_screen (19), downstream_edit_per_case (3), downstream_edit_per_prompt (90).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_7/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 39 ---
id: art_Qdoz9eH0AGjh
type: experiment
in_dependencies:
- id: art_dpYpjSn2Xvg3
  label: spelling-data
- id: art_t2uUbjSwpd3t
  label: taxonomic-data
- id: art_8QO7pl6Pd8UQ
  label: toxicity-data
- id: art_KNPsfjByyxiS
  label: entity-data
- id: art_RidEJtBC7gPT
  label: method-dossier
- id: art_I2MrezW41iQo
  label: diagnostic
title: De-Inflated Fair-Gated SAE Unlearning-Edit Test on Concentrated Absorbers
summary: |-
  Executed the M1''' unlearning-edit experiment end-to-end on a single 16GB GPU (google/gemma-2-2b + Gemma Scope layer_12/width_16k JumpReLU SAE, gating cosine 0.9189). At a MATCHED forget level it compares ablating ONE knowledge-graph-named absorber latent (KG-ABL, label-free/discovered) against a side-by-side battery of dense and selector baselines implemented in the same pipeline: (i) the strongest UNGATED difference-of-means erasure DENSE-SUB-ABL (LEAD comparator), (ii) the NEW genuinely-fair control DENSE-SUB-ABL-GATED-FAIR (erase u_sub only where a precise logistic d_sub detector fires, beta<=1, ONE unified gate for every case, balacc reported on a disjoint fold), (iii) the iter-7 footprint-gated DENSE-SUB-ABL-GATED (DEMOTED to a caveated robustness arm that over-erases ~14x), (iv) DENSE-WHOLE-ABL, (v) the M3''' MAX-PRECISION single-latent selector, and (vi) RAND. 8 cases ran in case order: 4 CONCENTRATED absorbers (first-letter large 8463, named-entity Amazon 6846 / Bush 1418 / Cook 15631 with parent 2768) then 4 references (Georgia 16009, Jordan 540, US 846, toxicity insult 13367). Two OpenRouter judges (anthropic/claude-haiku-4.5 primary + openai/gpt-4o-mini second) scored fluency/content-preservation/utility; total spend $1.073 (0 failures, 0 refusals; <$3 target, <$10 cap).

  HEADLINE VERDICT: DISCOVERY_IS_THE_VALUE_FAIR_GATE_CLOSES_GAP. Per case 3-way fork tally: KG_BEATS_STRONGEST_AND_FAIR_GATED=0, FAIR_GATED_CLOSES_GAP=5 (large/Amazon/Bush/Georgia/insult), NO_MEANINGFUL_FORGET=3 (Cook/Jordan/US), n_concentrated_wins=0. KG-ABL beats the strongest UNGATED dense on the joint (adv_KGvsSUB +0.97 large, +0.87 Amazon, +0.48 Georgia, both judges, CI excl 0) and is far cleaner on retain collateral (KG 5e-5 vs ungated 0.021 vs footprint-gate 0.295), with curve-dominance 1.0 — but the GENUINELY-FAIR d_sub-gated dense control CLOSES the gap everywhere (adv_KGvsFAIR ~0.0, CI includes 0), and the fair gate is even cleaner than KG (collateral ~3e-6). So the SAE's contribution is NOT edit quality over a fair dense baseline; it is label-free WHERE-to-gate discovery. The M3''' ablation shows set-cover machinery is INERT for the edit win (3 cases the max-precision latent equals the set-cover absorber, 0 cases discovery adds value). CONCENTRATION/precision, not the absorption diagnostic, predicts forgetting: distributed country senses (Jordan/US, and Cook) do NOT meaningfully forget (kg_can_forget=False) despite clean firing signatures, while a concentrated co-firing latent (insult) does. Hardened meaningful-forget proof uses BOTH instruments (20-50-probe completion-accuracy drop + frozen sub-probe positive-rate drop) at KL-matched AND behavioral-matched points; named-entity absorbers were re-validated at runtime (Amazon 6846 passes prec 0.94/jaccard 0.04; Bush 1418 and Cook 15631 disclosed as borderline-precision but used as the published discovery artifact under test, not silently overridden).

  DELIVERABLES: method.py (M1''' runner) + core.py (reused Gemma-Scope engine with the added erase_dir_dsub_gated operator) + make_variants.py + pinned pyproject.toml. method_out.json validates against exp_gen_sol_out (full/mini/preview all PASSED, <100MB). Two downstream-consumable datasets: 'edit_per_prompt' (288 rows; per (case,role,prompt) generations predict_kg_abl / predict_dense_sub_abl / predict_dense_sub_gated_fair / predict_dense_sub_footprint_gated / predict_max_precision / predict_dense_whole_abl / predict_noop / predict_rand, with per-op judge + model-internal forget-KL/PPL/sub-probe metadata; output=role) and 'kg_vs_controls_per_case' (8 rows; output=WIN_EXPECTED/LOSS_EXPECTED, predict_kg_abl=fork_verdict, adv_KG_vs_SUB/FAIR/GATEDFOOT, all CIs both judges, max_forget per op, gated_fair_reaches, kg_can_forget, concentration tag). 30 verbatim honest_negatives capture the de-inflation (iter-7 footprint headline over-erased), the fair-gate-closes finding, concentration-not-absorption, instrument disagreement, gating-is-prior-art, and that distributed senses don't forget. For GEN_PAPER_TEXT: lead with the honest 'discovery is the value' result and the auditability/localization + concentration-attribution spine; do NOT claim a KG edit-quality win over a fair dense control.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 40 ---
id: art_bPU1evbgN0og
type: experiment
in_dependencies:
- id: art_2xQn686KUmV5
  label: homograph-data
- id: art_dpYpjSn2Xvg3
  label: spelling-data
- id: art_RidEJtBC7gPT
  label: method-dossier
title: Base-Widener + Concentration-vs-Absorption SAE Edit Population Test (iter-8)
summary: >-
  iter-8 M2'''/M3'''/M5''' base-widener experiment on the two-track CCRG auditability spine (Gemma-2-2b + Gemma-Scope L12/width-16k
  JumpReLU SAE). Reuses the iter-7 engine VERBATIM (core.py / method_lib.py, WORK repointed to this workspace; ROOT left pointing
  at the upstream datasets) and adds ONE new edit operator plus a $0 concentration screen, a budget-bounded edit loop, and
  a population correlation. VALIDATED so far (smoke, $0): SAE loads (d_sae=16384, d_model=2304), determine_layer_idx selects
  13, gating PASS (cosine 0.9190, L0 88.0); the new operator runs without shape/NaN errors. NEW OPERATOR (core.make_edit_hook
  + _make_clamped_hook, threaded through forward_pos_logprobs/behavioral_curve/read_resid_under_edit/generate_under_edit):
  DENSE-SUB-ABL-GATED-FAIR = h - min(beta,1)*(h.u_sub)*u_sub applied ONLY where the PRECISE supervised sub-probe d_sub(h)>gate_thresh
  -- the genuinely fair conditional-dense control (labeled u_sub direction + precise where-to-edit + bounded beta<=1), replacing
  iter-7's crude |h.u_sub|>tau magnitude gate that forced beta~3 over-erasure. CANDIDATE POOL (~100 screened): first-letter
  spelling word-absorbers L/O/T/I/D (curated + KG4) + homograph entities rebuilt from the iter-5 testbed (city/month/given_name/brand,
  eligible >=150 diagnostic positives or curated/reviewer-named) + distributed-sense country anchors Georgia/Jordan. CONCENTRATION
  SCREEN ($0): per candidate compute precision, coverage, neutral footprint, the anchored K-track absorber, the unconstrained
  max-precision latent, recall-hole, firing-Jaccard, absorption_structured (reported, never gates) and set_cover_eq_max_precision;
  the PRIMARY concentration_score is the d_sub-margin CAPTURE fraction (fraction of the average target context's frozen sub-probe
  margin removed by ablating the single absorber); the literal precision*(1-footprint) saturates (~0.98) so is reported only
  as concentration_firing. The smoke screen confirmed the intended separation: spelling word-absorbers concentrate high (law
  0.745, level 0.739, list 0.714) while distributed country senses sit low (Georgia 0.113, Jordan 0.046). EDIT LOOP (budget-bounded,
  most-concentrated-first after the load-bearing anchors large/Georgia/Jordan): build u_sub/d_sub, sweep KG-ABL / DENSE-SUB-ABL
  (ungated lead comparator) / DENSE-SUB-ABL-GATED-FAIR / MAX-PREC-ABL, find the matched meaningful-forget point on the BEHAVIORAL
  sub-probe-drop curve (M4'''), prove meaningful forget ($0: sub-probe drop + templated completion-accuracy drop), then judge
  the joint fluency x content at the matched point with TWO OpenRouter judges (anthropic/claude-haiku-4.5 primary + openai/gpt-4o-mini
  second) and paired bootstrap (B=10000). VERDICT (M2''' base count): BASE_REACHES_4_PLUS vs BASE_STAYS_THIN_RETARGET by counting
  independent concentrated wins (meaningful_forget AND KG beats the fair control on both judges). M3''' POPULATION TEST: spearman(concentration,
  Delta_joint) and point-biserial(absorption-regime label, .) with bootstrap CIs decide CONCENTRATION_PREDICTS vs ABSORPTION_PREDICTS
  vs TIE/UNDERPOWERED. M5''' set-cover inertness rate = fraction of candidates whose anchored absorber equals the unconstrained
  max-precision latent. Outputs method_out.json (full/mini/preview variants, exp_gen_sol_out schema) with datasets concentration_screen
  (one row/candidate) and edit_predictions (one row/(candidate,role,prompt) carrying the five predict_* continuation strings);
  metadata holds gating_check, fair_gate_spec, concentration_screen_table, base_count (verdict + positive_control_reproduces),
  population_predictor (spearman + point-biserial CIs + predictor_verdict), set_cover_inertness_rate, judge spend, and the
  verbatim honest_negatives. Final aggregate CIs, the verdict, the predictor_verdict and the per-candidate tables are in method_out.json.metadata.
  Total LLM spend target <$3, hard cap $10.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 41 ---
id: art_Mlx5GfSusrjm
type: evaluation
in_dependencies:
- id: art_Cgk9ETiZfvtl
  label: edit-data
- id: art_ZxVw0e4seBq3
  label: entity-edit-data
- id: art_3WXWsaSoGMnK
  label: retraction-data
title: >-
  Iter-8 Integrity-Lock Eval: De-Inflated Lead, Dual Forget Instruments, Retraction
summary: >-
  Pure-CPU, $0, read-only re-analysis over the existing iter-6/7 edit data (D1=iter7_exp1 gated-dense, D2=iter7_exp2 named-entity,
  D3=iter6_exp1 u_sub), copied into deps/. Recompute-from-source then compare-to-stored (never overwrite); 44/44 cross-checks
  PASS. GROUP A de-inflates the headline: the honest lead is KG-ABL vs the strongest UNGATED dense = +1.00 (CI[0.79,1.21],
  n=36) on 'large'; the +1.58-vs-footprint-gated gap is robustness-only, handicapped by beta~2.97 over-erasure (gated retain-collateral
  0.290 = 13.8x its own ungated 0.021); reconciliation 1.8704-0.8704=+1.00 and 1.8704-0.2870=+1.58 verified <1e-3, and the
  per-prompt joint=HM(fluency,content_pres) recompute matches stored utility means exactly for all 5 cases. GROUP B lays both
  meaningful-forget instruments side-by-side: at the next-token-KL-matched point gold-completion-drop and frozen sub-probe-drop
  disagree in SIGN for 'large' (completion -1.01 favors gated, sub-probe +0.42 favors KG) => KL-matching != behavioral matching;
  a materiality filter shows 'large' is the ONLY material flip (the other 2 raw flips are on near-zero magnitudes), and the
  load-bearing 'large' completion CI is over only n=4 probes. GROUP C (descriptive, n~7): the edit-win predictor is latent
  CONCENTRATION not the absorption label - precision x single-latent leverage (v2) tracks the win (point-biserial r=+0.63)
  where the absorption label does not (r=-0.09); the inverse-FOOTPRINT proxy (v1=prec/f_kg) ANTI-correlates (r=-0.80) because
  distributed senses also fire sparsely, so footprint sparsity != concentration; predictive_delta=+0.72 CI[0.08,1.20]; supersedes
  the thin 1-case-vs-2-case adv_absorption(1.583)/adv_cofiring(0.372) aggregate. GROUP D locks the Georgia +0.561 retraction
  (recomputed +0.5606 from D3): it sat at a near-NOOP operating point (max single-latent forget KL 0.065, NOOP-identical 0.889,
  sub-probe drop 0.075, completion CI excl_0=false) => RETRACTED_NEAR_NOOP partial suppression. GROUP E flags operator divergence
  (D1 ~3% global-footprint gate vs D2 ~95% X-positive-rate clamp), which iter-8 must unify. Output eval_out.json (+full/mini/preview,
  all validate exp_eval_sol_out, <100MB): metrics_agg with 53 numeric drop-in metrics; datasets de_inflation_per_case(7),
  both_instrument_per_case_op(15), concentration_predictor_per_case(7), retraction_per_case(1), operator_divergence(2); metadata.cross_checks(44,
  all pass), group_c_correlations, and cross-checked paper_wording W1-W5 for GEN_PAPER_TEXT.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

--- Item 42 ---
id: art_JCYCmzJDvUm5
type: research
in_dependencies:
- id: art_IlzAiXYWeUYH
  label: prior-positioning
- id: art_3zaa2xXEp8Az
  label: prior-positioning
title: 'CCRG iter-8 Positioning: Chanin Delta, Concentration-Gate, Localization Retarget'
summary: >-
  Finalizes iteration-8 CCRG paper positioning for GEN_PAPER_TEXT, $0 web-only. (D1) States the label-free DELTA of 'anchored
  recall-hole-guided precision selection of a single absorber' vs Chanin et al.'s SUPERVISED, spelling-bound absorption diagnostic
  (2409.14507: LR probe on ground-truth first-letter labels -> max encoder-cosine parent; ablation on the first-letter logit
  + probe-projection for the absorber; absorption_rate=num_absorptions/lr_probe_true_positives) and vs a simple max-precision
  selector (empirically a TIE since wins are k=1); trims set-cover/(1-1/e) to MOTIVATION only. (D2) Grounds 'the edit win
  tracks CONCENTRATION/PRECISION, not absorption' against the feature-selection-for-steering literature: Arad/Mueller/Belinkov
  (EMNLP2025 output-score selection 2-3x), CorrSteer (correlation), FGAA (density filtering), Sparse Activation Steering (width->monosemanticity),
  Duan 2606.08365 (pre-intervention feature statistics predict collateral spread), SAE-TS (target specific feature, min side-effects),
  Anthropic Scaling Monosemanticity (specificity = sharp conditional gate); internal predictor concentration r=+0.63 vs absorption-label
  r=-0.09 vs footprint-sparsity r=-0.80. (D3) Retargets to lead with 'training-free auditable LOCALIZATION + EDITING of homograph-polysemy
  absorption' (ICLR primary per goal, ICML acceptable; ICLR2026 CfP fits), safety-homograph null (2/44) as headline limitation,
  with BOTH a wins-landed (OUTCOME-A) and base-thin (OUTCOME-B, expected) abstract+intro spine plus a selector keyed to the
  parallel M1'''/M3''' results (BEATS=0/FAIR_CLOSES=4/n_concentrated_wins=0 -> OUTCOME-B). (D4) Locks the citation set: carries
  iter-6/iter-7 venue-verified table verbatim + 7 web-verified new cites with IDs/venues/authors + BibTeX + unresolved-flags
  (CorrSteer venue conflict). (D5) 14-item presentation-strip checklist (lead +1.00 not +1.58; both forget instruments; unify
  gate operator; concentration not absorption; localization-not-classification; retract Georgia +0.561; firing-signature !=
  edit-handle). Outputs research_out.json + research_report.md (D1-D5).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
</all_artifacts>

<new_artifacts_this_iteration>
These 4 artifacts were created THIS iteration.

id: art_Qdoz9eH0AGjh
type: experiment
in_dependencies:
- id: art_dpYpjSn2Xvg3
  label: spelling-data
- id: art_t2uUbjSwpd3t
  label: taxonomic-data
- id: art_8QO7pl6Pd8UQ
  label: toxicity-data
- id: art_KNPsfjByyxiS
  label: entity-data
- id: art_RidEJtBC7gPT
  label: method-dossier
- id: art_I2MrezW41iQo
  label: diagnostic
title: De-Inflated Fair-Gated SAE Unlearning-Edit Test on Concentrated Absorbers
summary: |-
  Executed the M1''' unlearning-edit experiment end-to-end on a single 16GB GPU (google/gemma-2-2b + Gemma Scope layer_12/width_16k JumpReLU SAE, gating cosine 0.9189). At a MATCHED forget level it compares ablating ONE knowledge-graph-named absorber latent (KG-ABL, label-free/discovered) against a side-by-side battery of dense and selector baselines implemented in the same pipeline: (i) the strongest UNGATED difference-of-means erasure DENSE-SUB-ABL (LEAD comparator), (ii) the NEW genuinely-fair control DENSE-SUB-ABL-GATED-FAIR (erase u_sub only where a precise logistic d_sub detector fires, beta<=1, ONE unified gate for every case, balacc reported on a disjoint fold), (iii) the iter-7 footprint-gated DENSE-SUB-ABL-GATED (DEMOTED to a caveated robustness arm that over-erases ~14x), (iv) DENSE-WHOLE-ABL, (v) the M3''' MAX-PRECISION single-latent selector, and (vi) RAND. 8 cases ran in case order: 4 CONCENTRATED absorbers (first-letter large 8463, named-entity Amazon 6846 / Bush 1418 / Cook 15631 with parent 2768) then 4 references (Georgia 16009, Jordan 540, US 846, toxicity insult 13367). Two OpenRouter judges (anthropic/claude-haiku-4.5 primary + openai/gpt-4o-mini second) scored fluency/content-preservation/utility; total spend $1.073 (0 failures, 0 refusals; <$3 target, <$10 cap).

  HEADLINE VERDICT: DISCOVERY_IS_THE_VALUE_FAIR_GATE_CLOSES_GAP. Per case 3-way fork tally: KG_BEATS_STRONGEST_AND_FAIR_GATED=0, FAIR_GATED_CLOSES_GAP=5 (large/Amazon/Bush/Georgia/insult), NO_MEANINGFUL_FORGET=3 (Cook/Jordan/US), n_concentrated_wins=0. KG-ABL beats the strongest UNGATED dense on the joint (adv_KGvsSUB +0.97 large, +0.87 Amazon, +0.48 Georgia, both judges, CI excl 0) and is far cleaner on retain collateral (KG 5e-5 vs ungated 0.021 vs footprint-gate 0.295), with curve-dominance 1.0 — but the GENUINELY-FAIR d_sub-gated dense control CLOSES the gap everywhere (adv_KGvsFAIR ~0.0, CI includes 0), and the fair gate is even cleaner than KG (collateral ~3e-6). So the SAE's contribution is NOT edit quality over a fair dense baseline; it is label-free WHERE-to-gate discovery. The M3''' ablation shows set-cover machinery is INERT for the edit win (3 cases the max-precision latent equals the set-cover absorber, 0 cases discovery adds value). CONCENTRATION/precision, not the absorption diagnostic, predicts forgetting: distributed country senses (Jordan/US, and Cook) do NOT meaningfully forget (kg_can_forget=False) despite clean firing signatures, while a concentrated co-firing latent (insult) does. Hardened meaningful-forget proof uses BOTH instruments (20-50-probe completion-accuracy drop + frozen sub-probe positive-rate drop) at KL-matched AND behavioral-matched points; named-entity absorbers were re-validated at runtime (Amazon 6846 passes prec 0.94/jaccard 0.04; Bush 1418 and Cook 15631 disclosed as borderline-precision but used as the published discovery artifact under test, not silently overridden).

  DELIVERABLES: method.py (M1''' runner) + core.py (reused Gemma-Scope engine with the added erase_dir_dsub_gated operator) + make_variants.py + pinned pyproject.toml. method_out.json validates against exp_gen_sol_out (full/mini/preview all PASSED, <100MB). Two downstream-consumable datasets: 'edit_per_prompt' (288 rows; per (case,role,prompt) generations predict_kg_abl / predict_dense_sub_abl / predict_dense_sub_gated_fair / predict_dense_sub_footprint_gated / predict_max_precision / predict_dense_whole_abl / predict_noop / predict_rand, with per-op judge + model-internal forget-KL/PPL/sub-probe metadata; output=role) and 'kg_vs_controls_per_case' (8 rows; output=WIN_EXPECTED/LOSS_EXPECTED, predict_kg_abl=fork_verdict, adv_KG_vs_SUB/FAIR/GATEDFOOT, all CIs both judges, max_forget per op, gated_fair_reaches, kg_can_forget, concentration tag). 30 verbatim honest_negatives capture the de-inflation (iter-7 footprint headline over-erased), the fair-gate-closes finding, concentration-not-absorption, instrument disagreement, gating-is-prior-art, and that distributed senses don't forget. For GEN_PAPER_TEXT: lead with the honest 'discovery is the value' result and the auditability/localization + concentration-attribution spine; do NOT claim a KG edit-quality win over a fair dense control.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

id: art_bPU1evbgN0og
type: experiment
in_dependencies:
- id: art_2xQn686KUmV5
  label: homograph-data
- id: art_dpYpjSn2Xvg3
  label: spelling-data
- id: art_RidEJtBC7gPT
  label: method-dossier
title: Base-Widener + Concentration-vs-Absorption SAE Edit Population Test (iter-8)
summary: >-
  iter-8 M2'''/M3'''/M5''' base-widener experiment on the two-track CCRG auditability spine (Gemma-2-2b + Gemma-Scope L12/width-16k
  JumpReLU SAE). Reuses the iter-7 engine VERBATIM (core.py / method_lib.py, WORK repointed to this workspace; ROOT left pointing
  at the upstream datasets) and adds ONE new edit operator plus a $0 concentration screen, a budget-bounded edit loop, and
  a population correlation. VALIDATED so far (smoke, $0): SAE loads (d_sae=16384, d_model=2304), determine_layer_idx selects
  13, gating PASS (cosine 0.9190, L0 88.0); the new operator runs without shape/NaN errors. NEW OPERATOR (core.make_edit_hook
  + _make_clamped_hook, threaded through forward_pos_logprobs/behavioral_curve/read_resid_under_edit/generate_under_edit):
  DENSE-SUB-ABL-GATED-FAIR = h - min(beta,1)*(h.u_sub)*u_sub applied ONLY where the PRECISE supervised sub-probe d_sub(h)>gate_thresh
  -- the genuinely fair conditional-dense control (labeled u_sub direction + precise where-to-edit + bounded beta<=1), replacing
  iter-7's crude |h.u_sub|>tau magnitude gate that forced beta~3 over-erasure. CANDIDATE POOL (~100 screened): first-letter
  spelling word-absorbers L/O/T/I/D (curated + KG4) + homograph entities rebuilt from the iter-5 testbed (city/month/given_name/brand,
  eligible >=150 diagnostic positives or curated/reviewer-named) + distributed-sense country anchors Georgia/Jordan. CONCENTRATION
  SCREEN ($0): per candidate compute precision, coverage, neutral footprint, the anchored K-track absorber, the unconstrained
  max-precision latent, recall-hole, firing-Jaccard, absorption_structured (reported, never gates) and set_cover_eq_max_precision;
  the PRIMARY concentration_score is the d_sub-margin CAPTURE fraction (fraction of the average target context's frozen sub-probe
  margin removed by ablating the single absorber); the literal precision*(1-footprint) saturates (~0.98) so is reported only
  as concentration_firing. The smoke screen confirmed the intended separation: spelling word-absorbers concentrate high (law
  0.745, level 0.739, list 0.714) while distributed country senses sit low (Georgia 0.113, Jordan 0.046). EDIT LOOP (budget-bounded,
  most-concentrated-first after the load-bearing anchors large/Georgia/Jordan): build u_sub/d_sub, sweep KG-ABL / DENSE-SUB-ABL
  (ungated lead comparator) / DENSE-SUB-ABL-GATED-FAIR / MAX-PREC-ABL, find the matched meaningful-forget point on the BEHAVIORAL
  sub-probe-drop curve (M4'''), prove meaningful forget ($0: sub-probe drop + templated completion-accuracy drop), then judge
  the joint fluency x content at the matched point with TWO OpenRouter judges (anthropic/claude-haiku-4.5 primary + openai/gpt-4o-mini
  second) and paired bootstrap (B=10000). VERDICT (M2''' base count): BASE_REACHES_4_PLUS vs BASE_STAYS_THIN_RETARGET by counting
  independent concentrated wins (meaningful_forget AND KG beats the fair control on both judges). M3''' POPULATION TEST: spearman(concentration,
  Delta_joint) and point-biserial(absorption-regime label, .) with bootstrap CIs decide CONCENTRATION_PREDICTS vs ABSORPTION_PREDICTS
  vs TIE/UNDERPOWERED. M5''' set-cover inertness rate = fraction of candidates whose anchored absorber equals the unconstrained
  max-precision latent. Outputs method_out.json (full/mini/preview variants, exp_gen_sol_out schema) with datasets concentration_screen
  (one row/candidate) and edit_predictions (one row/(candidate,role,prompt) carrying the five predict_* continuation strings);
  metadata holds gating_check, fair_gate_spec, concentration_screen_table, base_count (verdict + positive_control_reproduces),
  population_predictor (spearman + point-biserial CIs + predictor_verdict), set_cover_inertness_rate, judge spend, and the
  verbatim honest_negatives. Final aggregate CIs, the verdict, the predictor_verdict and the per-candidate tables are in method_out.json.metadata.
  Total LLM spend target <$3, hard cap $10.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

id: art_Mlx5GfSusrjm
type: evaluation
in_dependencies:
- id: art_Cgk9ETiZfvtl
  label: edit-data
- id: art_ZxVw0e4seBq3
  label: entity-edit-data
- id: art_3WXWsaSoGMnK
  label: retraction-data
title: >-
  Iter-8 Integrity-Lock Eval: De-Inflated Lead, Dual Forget Instruments, Retraction
summary: >-
  Pure-CPU, $0, read-only re-analysis over the existing iter-6/7 edit data (D1=iter7_exp1 gated-dense, D2=iter7_exp2 named-entity,
  D3=iter6_exp1 u_sub), copied into deps/. Recompute-from-source then compare-to-stored (never overwrite); 44/44 cross-checks
  PASS. GROUP A de-inflates the headline: the honest lead is KG-ABL vs the strongest UNGATED dense = +1.00 (CI[0.79,1.21],
  n=36) on 'large'; the +1.58-vs-footprint-gated gap is robustness-only, handicapped by beta~2.97 over-erasure (gated retain-collateral
  0.290 = 13.8x its own ungated 0.021); reconciliation 1.8704-0.8704=+1.00 and 1.8704-0.2870=+1.58 verified <1e-3, and the
  per-prompt joint=HM(fluency,content_pres) recompute matches stored utility means exactly for all 5 cases. GROUP B lays both
  meaningful-forget instruments side-by-side: at the next-token-KL-matched point gold-completion-drop and frozen sub-probe-drop
  disagree in SIGN for 'large' (completion -1.01 favors gated, sub-probe +0.42 favors KG) => KL-matching != behavioral matching;
  a materiality filter shows 'large' is the ONLY material flip (the other 2 raw flips are on near-zero magnitudes), and the
  load-bearing 'large' completion CI is over only n=4 probes. GROUP C (descriptive, n~7): the edit-win predictor is latent
  CONCENTRATION not the absorption label - precision x single-latent leverage (v2) tracks the win (point-biserial r=+0.63)
  where the absorption label does not (r=-0.09); the inverse-FOOTPRINT proxy (v1=prec/f_kg) ANTI-correlates (r=-0.80) because
  distributed senses also fire sparsely, so footprint sparsity != concentration; predictive_delta=+0.72 CI[0.08,1.20]; supersedes
  the thin 1-case-vs-2-case adv_absorption(1.583)/adv_cofiring(0.372) aggregate. GROUP D locks the Georgia +0.561 retraction
  (recomputed +0.5606 from D3): it sat at a near-NOOP operating point (max single-latent forget KL 0.065, NOOP-identical 0.889,
  sub-probe drop 0.075, completion CI excl_0=false) => RETRACTED_NEAR_NOOP partial suppression. GROUP E flags operator divergence
  (D1 ~3% global-footprint gate vs D2 ~95% X-positive-rate clamp), which iter-8 must unify. Output eval_out.json (+full/mini/preview,
  all validate exp_eval_sol_out, <100MB): metrics_agg with 53 numeric drop-in metrics; datasets de_inflation_per_case(7),
  both_instrument_per_case_op(15), concentration_predictor_per_case(7), retraction_per_case(1), operator_divergence(2); metadata.cross_checks(44,
  all pass), group_c_correlations, and cross-checked paper_wording W1-W5 for GEN_PAPER_TEXT.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

id: art_JCYCmzJDvUm5
type: research
in_dependencies:
- id: art_IlzAiXYWeUYH
  label: prior-positioning
- id: art_3zaa2xXEp8Az
  label: prior-positioning
title: 'CCRG iter-8 Positioning: Chanin Delta, Concentration-Gate, Localization Retarget'
summary: >-
  Finalizes iteration-8 CCRG paper positioning for GEN_PAPER_TEXT, $0 web-only. (D1) States the label-free DELTA of 'anchored
  recall-hole-guided precision selection of a single absorber' vs Chanin et al.'s SUPERVISED, spelling-bound absorption diagnostic
  (2409.14507: LR probe on ground-truth first-letter labels -> max encoder-cosine parent; ablation on the first-letter logit
  + probe-projection for the absorber; absorption_rate=num_absorptions/lr_probe_true_positives) and vs a simple max-precision
  selector (empirically a TIE since wins are k=1); trims set-cover/(1-1/e) to MOTIVATION only. (D2) Grounds 'the edit win
  tracks CONCENTRATION/PRECISION, not absorption' against the feature-selection-for-steering literature: Arad/Mueller/Belinkov
  (EMNLP2025 output-score selection 2-3x), CorrSteer (correlation), FGAA (density filtering), Sparse Activation Steering (width->monosemanticity),
  Duan 2606.08365 (pre-intervention feature statistics predict collateral spread), SAE-TS (target specific feature, min side-effects),
  Anthropic Scaling Monosemanticity (specificity = sharp conditional gate); internal predictor concentration r=+0.63 vs absorption-label
  r=-0.09 vs footprint-sparsity r=-0.80. (D3) Retargets to lead with 'training-free auditable LOCALIZATION + EDITING of homograph-polysemy
  absorption' (ICLR primary per goal, ICML acceptable; ICLR2026 CfP fits), safety-homograph null (2/44) as headline limitation,
  with BOTH a wins-landed (OUTCOME-A) and base-thin (OUTCOME-B, expected) abstract+intro spine plus a selector keyed to the
  parallel M1'''/M3''' results (BEATS=0/FAIR_CLOSES=4/n_concentrated_wins=0 -> OUTCOME-B). (D4) Locks the citation set: carries
  iter-6/iter-7 venue-verified table verbatim + 7 web-verified new cites with IDs/venues/authors + BibTeX + unresolved-flags
  (CorrSteer venue conflict). (D5) 14-item presentation-strip checklist (lead +1.00 not +1.58; both forget instruments; unify
  gate operator; concentration not absorption; localization-not-classification; retract Georgia +0.561; firing-signature !=
  edit-handle). Outputs research_out.json + research_report.md (D1-D5).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
</new_artifacts_this_iteration>

<current_paper>
The paper draft from this iteration — represents the current state of the research story.


# Introduction
\label{sec:intro}

Sparse autoencoders (SAEs) decompose the activations of large language models (LLMs) into a dictionary of sparsely-activating latents intended to be interpretable, monosemantic units of analysis \citep{Cunningham2023, Bricken2023, Templeton2024}. The promise is operational: a latent that reliably tracks a human concept could be read off as a classifier, flipped as a steering knob, or compared across model variants. Public SAE suites such as Gemma Scope \citep{Lieberum2024} expose millions of such latents over open models, making this a practical interface for safety-relevant interpretability and the substrate our work operates on.

The promise is undercut by a now well-documented fact: \emph{single SAE latents are not reliable units} \citep{Leask2025}. Two failure modes recur. \emph{Feature splitting} fragments one concept across many latents. \emph{Feature absorption} is more insidious: a more specific child latent suppresses the firing of a more general parent, leaving the parent with unpredictable holes on exactly the sub-contexts the child covers; parent and child become \emph{mutually exclusive in firing} \citep{Chanin2024}. (\emph{Feature hedging} merges correlated features into one polysemantic latent in narrow SAEs \citep{Chanin2025}; a hedged latent is not groupable and is out of scope.) On concrete downstream tasks the cost is stark: difference-of-means probes are the strongest concept detectors and raw-latent SAE methods are uncompetitive \citep{Wu2025, Kantamneni2025}, while standardized suites quantify absorption, sparse probing, and targeted erasure \citep{Karvonen2025}. We adopt this as an honest constraint up front: \textbf{the reliability gain we deliver is localization and auditability, not classification.} On every task we measure, no SAE unit out-classifies a strong dense probe (toxicity unit AUC $0.762$ vs.\ dense $0.84$--$0.89$; Georgia $0.995$ vs.\ $1.000$). A reader should not read ``reliable units'' as a classification claim our evidence contradicts.

The task is hard because absorption defeats the obvious instruments \emph{by construction}. The intuitive fix for an unreliable single latent is to group several latents into a cluster-level unit, but every existing post-hoc grouping signal is \emph{observational}: which latents fire together (co-activation feature families \citep{ONeill2024, Deng2025}) or which decoder directions point alike. Absorption is precisely the regime where observational signals must fail---parent and absorbing child are mutually exclusive in firing, so co-activation can never group them, and their decoders need not be cosine-similar \citep{Chanin2024}. The standard \emph{supervised} remedy, selecting the top-$N$ latents by causal effect on a concept probe (SCR/TPP attribution \citep{Karvonen2024, Marks2024}), is no better: a latent that fires only in a narrow sub-context has low \emph{marginal} attribution and is silently dropped, even though it carries the concept there. The latents one most needs to find are exactly the ones these instruments discard.

Why has this not been solved post-hoc? Recent architectural remedies---Matryoshka SAEs \citep{Bussmann2025}, hierarchical SAEs \citep{Muchane2025}, and subspace-aware SAEs \citep{Dalili2026}---all \emph{retrain} the SAE to reduce splitting and absorption at training time, and do not help a practitioner holding a frozen public SAE. We take the opposite stance: a \emph{training-free, post-hoc} procedure over frozen public SAEs. Given only content-flip pairs, the matched instrument is to anchor on the highest-recall parent latent, read its recall \emph{hole} to name an under-served sub-context, and \emph{precision-select} the single latent that covers it---the absorber that marginal attribution drops. (We motivate the search by maximum coverage \citep{Nemhauser1978, Feige1998} and import a correlation-community track for the splitting regime from differential co-expression in systems biology \citep{Tesson2010, Zhang2005}; both are secondary, as \S\ref{sec:method} explains, because for every result the procedure is effectively single-absorber.)

[FIGURE:fig1]

We introduce \textbf{Co-Response Grouping (CCRG)} and execute it on a frozen Gemma Scope SAE. The discovered absorber becomes a node in a feature-level knowledge graph (KG) whose edges carry \emph{measured} repair utility, plus a sparsely-firing handle for editing one sub-context. Our durable, strongly-evidenced contribution is the \textbf{auditable, label-free-discovered, regime-targeted localization of homograph-polysemy absorption} (\S\ref{sec:spine}): KG-named absorbers recover suppressed-parent recall holes over a random single-latent control, the localized edits are surgical, members are LLM-auditable, and the entire spine replicates on a wider dictionary.

\paragraph{An honest self-correction on editing.} A prior version of this work claimed that ablating one discovered absorber, gated by its own sparse firing, \emph{beats} a footprint-matched gated dense edit by $\Delta_{\text{joint}}{=}{+}1.58$ at meaningful forget. A reviewer made two decisive objections, and a controlled re-run \emph{confirms both} [ARTIFACT:art_Mlx5GfSusrjm]. First, the footprint-matched gate was \emph{mis-tuned}: to reach matched forget within a $3\%$ token footprint it was driven to over-erasure ($\beta{\approx}2.97$), producing $13.8\times$ \emph{more} collateral than its own ungated form. The defensible number is the win against the \emph{strongest} dense baseline---the ungated difference-of-means erasure---which is $+1.00$ (CI $[0.79,1.21]$), not $+1.58$. Second, and decisively, we added a \emph{genuinely fair} dense control: the same labeled direction erased only where a precise sub-context detector fires, with bounded $\beta{\leq}1$. \textbf{This fair control closes the gap on every case} (KG-vs-fair joint CI includes $0$; the fair gate is even cleaner on collateral) [ARTIFACT:art_Qdoz9eH0AGjh]. So a discovered absorber is \emph{not} a better edit operator than a fair dense baseline. Because gating an edit by a sparse/threshold detector is \emph{established prior art} (CAST \citep{Lee2024}, GSS \citep{Zhang2026}, GUARD-IT \citep{Turani2026}, SADI \citep{Wang2024}, all with \emph{supervised} gates), the SAE-specific value that remains is the \textbf{training-free, label-free discovery of \emph{where} to gate}---embracing the ``discover, don't act'' thesis \citep{Peng2025}.

\paragraph{The edit advantage tracks concentration, not absorption.} The meaningful-forget edit cases span \emph{both} firing regimes---the absorption case \texttt{large} and a co-firing toxicity latent \texttt{insult} (firing-Jaccard $0.882$, no recall hole) both forget cleanly---while the absorption \emph{losses} (Georgia, Jordan) are \emph{distributed} senses a single latent cannot meaningfully forget. The win predictor is therefore lexical \emph{concentration} (high per-sub-context precision concentrated on a sparse handle), of which absorption is \emph{one} label-free-discoverable source, neither necessary nor sufficient. A decisive ablation confirms it: replacing the anchored set-cover with a simple ``pick the single most precise latent on the target sub-context'' selector \emph{ties} the discovery on every edit ($0/8$ cases where the machinery adds value) [ARTIFACT:art_Qdoz9eH0AGjh]. What discovery buys over max-precision is the recall-hole \emph{anchoring} that names \emph{which} sub-context to gate, label-free.

\paragraph{Safety-relevant absorption is homograph-confined.} The goal asks for reliability on safety-relevant attributes; we searched directly. Of $44$ eligible identity groups built from the full \texttt{civil\_comments} corpus, \emph{exactly two}---\texttt{white} and \texttt{straight}, both lexical homographs---exhibit the absorption signature; the other $42$ show no parent recall hole [ARTIFACT:art_yAQgbq5Wgymx]. Absorption tracks lexical polysemy, not safety semantics. This is the settled scope and the headline limitation: the confirmed structure and edits are on non-safety lexical-homograph/spelling tokens.

\paragraph{Summary of contributions.}
\begin{itemize}
\item \textbf{An auditable localization spine} (\S\ref{sec:spine}): a label-free feature-KG whose edges carry measured repair utility ($22$ distinct recall holes, $30$ FDR survivors, over a random single-latent control), a median $1262\times$-selective surgical edit with a corrected selectivity account, LLM-auditable members ($0.730$ vs.\ $0.096$ null), and full replication on a $4\times$-wider SAE that absorbs \emph{more}.
\item \textbf{A label-free single-absorber discovery method} (\S\ref{sec:method}): anchored, recall-hole-guided precision selection of the absorber that marginal attribution drops, sharpened against the \emph{supervised}, spelling-bound absorption diagnostic of \citet{Chanin2024}; set-cover/$(1{-}1/e)$ and the correlation track are motivation/secondary.
\item \textbf{A de-inflated, fair-control edit result} (\S\ref{sec:edit}): the SAE-specific edit value is label-free \emph{where-to-gate discovery}, not edit quality---a genuinely fair gated dense control matches a discovered absorber; the residual advantage over the \emph{strongest} ungated dense ($+0.97$ on \texttt{large}, $+0.87$ on \texttt{Amazon}) tracks lexical concentration, not absorption, and the set-cover machinery is inert versus a max-precision selector.
\item \textbf{A settled safety scoping null} (\S\ref{sec:safety}): absorption is homograph-confined ($2/44$ safety groups, $0/28$ professions, $3/64$ homograph entities), with a confirmatory named-entity pass ($3/5$ structured).
\item \textbf{Honestly-reported nulls on the goal's downstream tasks} (\S\ref{sec:neg}): no SAE unit out-classifies a dense probe; steering is surgical on $2/5$ letters; model-diffing is a confound-bounded $+0.000$ null; the a-priori router is out-of-sample-unvalidated.
\end{itemize}

# Related Work
\label{sec:related}

\paragraph{SAEs and the unreliability of single latents.} Sparse dictionary learning on LLM activations yields interpretable features \citep{Cunningham2023, Bricken2023, Templeton2024, Lieberum2024}, but individual latents are not canonical units \citep{Leask2025}. \citet{Chanin2024} introduce and quantify \emph{feature absorption}---a specific child latent suppresses a general parent's firing---demonstrated on first-letter spelling, and \citet{Chanin2025} give the two-sided width law (absorption worsens as the SAE widens, hedging as it narrows). Benchmarks make the cost concrete: difference-of-means is strongest and raw-latent SAE methods are uncompetitive \citep{Wu2025, Kantamneni2025}, and SAEBench reports that ``absorption scores worsen with increased dictionary size'' \citep{Karvonen2025}---the \emph{signed prediction} for our cross-dictionary test (\S\ref{sec:spine}).

\paragraph{Post-hoc grouping and supervised selection.} Prior grouping is observational: co-activation ``feature families'' \citep{ONeill2024}, sparse coactivation modules \citep{Deng2025}, and the closest feature-level KG \citep{Winnicki2026}, which builds edges from corpus co-occurrence, transcoder pathways, and decoder geometry. By construction such edges cannot express CCRG's central relation: a parent anchor joined to a specialist that is \emph{mutually exclusive in firing} (firing-Jaccard $<0.05$). SHIFT and the SCR/TPP family rank individual latents by marginal causal effect and ablate the top-$N$ \citep{Marks2024, Karvonen2024}; a latent firing only in a narrow sub-context is silently dropped---the gap our recall-hole-guided selection fills. PS-Eval \citep{Minegishi2025} asks whether SAE features separate word senses but never studies a suppressed parent or a recall hole.

\paragraph{Distinction from the absorption diagnostic.} \citet{Chanin2024} provide a \emph{supervised, spelling-bound diagnostic}: a logistic probe trained on ground-truth first-letter labels locates the parent (max encoder-cosine), an ablation on the first-letter logit plus a probe-projection test locates the absorber. CCRG's delta is to make the discovery \emph{label-free, training-free, and form-free}: the parent is anchored by content-response recall on counterfactual pairs (no probe), its recall hole names the sub-context (no logit), the absorber is chosen by firing-precision, and the form-free probe$+$ablation diagnostic only \emph{scores} already-formed KG edges (never forms them, so the comparison is non-circular). We run it on homograph/numeric hierarchies the diagnostic was never applied to.

\paragraph{Gated/conditional activation editing: the decisive control is prior art.} Our edit is benchmarked against \emph{gated} dense directions, and gating an edit by a sparse/threshold detector is \emph{established prior art}. CAST \citep{Lee2024} applies a steering vector only when a learned condition vector matches the input. GSS \citep{Zhang2026} publishes essentially the exact operator our footprint control uses, $h'=h-\mathbb{1}(|u^\top h|>\epsilon)\,v$, with $u,v$ optimized on labeled sequences and $\epsilon$ at the $95$th percentile. GUARD-IT \citep{Turani2026} routes queries through a similarity gate over labeled forget clusters, and SADI \citep{Wang2024} builds a per-input mask from contrastive pairs. In \emph{all} prior methods the gate is \emph{supervised}; the SAE-specific value that remains is the \emph{label-free discovery} of where to gate \citep{Peng2025}.

\paragraph{Feature selection for clean steering (the concentration axis).} A recent literature establishes that \emph{which} precise feature you select---not the operator---drives clean, low-collateral edits, and that pre-intervention feature statistics predict collateral: output-score filtering yields $2$--$3\times$ better steering \citep{Arad2025}, correlation-based selection reduces spurious features \citep{Cho2025}, density filtering keeps specialized features \citep{Soo2025}, wider SAEs give sharper handles \citep{Bayat2025}, and side-effect spread is forecastable from feature statistics \citep{Duan2026}; SAE-TS targets a specific feature to minimize side effects \citep{Chalnev2024}, and ``specificity'' in monosemanticity is exactly a sharp conditional gate \citep{Templeton2024}. Our concentration-not-absorption finding sits squarely in this line: a concentrated latent's calibrated firing is a sharp gate, whereas a footprint-matched dense projection must over-erase.

\paragraph{Unlearning, concept removal, and the dense comparator.} The canonical SAE-unlearning study finds multi-feature interventions unlearn topics ``with similar or larger unwanted side-effects'' than fine-tuning \citep{Farrell2024}; CRISP contests this for \emph{whole} concepts \citep{Ashuach2025}. We make \emph{no} general claim that SAE interventions beat dense baselines. A labeled dense direction can be removed while preserving task-relevant information \citep{Holstege2025}, overall utility \citep{KarvonenMarks2025}, and even without protected attributes \citep{Shao2026}; whole-concept erasure is LEACE-style \citep{Belrose2023}, and SAE-TS/SRS select a whole \emph{concept} feature, not a sub-context absorber \citep{Chalnev2024, He2025}. We map outcomes onto the forget-quality/retain-utility/fluency triad \citep{Li2024, Shi2024}.

\paragraph{Safety/identity debiasing.} SAE debiasing edits \emph{whole} bias-correlated features, often in vision-language models \citep{Sasse2024}; the closest near-miss steers a single race-correlated latent in clinical LLMs but that latent \emph{co-fires} (entangled, not an absorber) and the authors concede SAE steering is ``of marginal utility for realistic tasks'' \citep{Ahsan2025}. Model-editing for stereotypes \citep{Xu2025} and neural-collapse fairness fine-tuning \citep{Xu2024} edit a whole association. Our safety finding is a \emph{measured scoping null}: identity attributes are predominantly co-firing, and absorption-structured identity tokens are homograph-confined (\S\ref{sec:safety}).

\paragraph{Cross-field instruments and robustness framing.} The (secondary) correlation track imports differential co-expression \citep{Tesson2010, Zhang2005} and Leiden community detection \citep{Traag2018}; the search motivation imports maximum coverage \citep{Nemhauser1978, Feige1998}. The robustness framing engages label-free worst-group robustness---group-DRO \citep{Sagawa2019}, JTT \citep{Liu2021}, GEORGE \citep{Sohoni2020}, EIIL \citep{Creager2020}, LfF \citep{Nam2020}, group-aware priors \citep{Rudner2024}, diverse prototypical ensembles \citep{To2025}---which infer groups over \emph{examples} and \emph{retrain}; CCRG groups \emph{features}, never retrains, and the recovered absorbers \emph{are} the inferred sub-context specialists. Surface invariance draws on LEACE \citep{Belrose2023} and counterfactual invariance \citep{Veitch2021}; label-free SAE steering on \citep{Chatzoudis2025}; minimal-pair supervision on counterfactually-augmented data \citep{Kaushik2019}, CEBaB \citep{Abraham2022}, and ParaDetox \citep{Logacheva2022}. The closest ``cluster counterfactual differences'' template is CDLC in vision \citep{Varshney2025}, which clusters one continuous direction per class; we select \emph{discrete} SAE latents.

# Label-Free Single-Absorber Discovery
\label{sec:method}

We frame CCRG primarily as a \emph{discovery procedure}: its demonstrated job is to surface the single precise absorber latent that marginal attribution drops, from which the KG, the repair, and the sparse-firing handle follow. Multi-member units and the correlation track are secondary (\S\ref{sec:method}, last paragraph), because the downstream wins trace to individual discovered absorbers and multi-member units only add collateral.

\paragraph{Preliminaries.} Let the frozen SAE have latents $l \in \{1,\dots,L\}$ with encoder activation $a_l(x)$; a latent \emph{fires} on $x$ iff $a_l(x)>0$ (Gemma Scope uses a JumpReLU \citep{Lieberum2024}). For a concept $c$ we are given \emph{content-flip minimal pairs} $(x_{\text{off}}, x_{\text{on}})$ in which the concept is absent/present at matched surface form, plus \emph{surface-flip pairs}. Content labels are the supervision every matched baseline consumes; the method uses no absorption-specific oracle. The primary run encodes at one residual-stream site (\texttt{gemma-2-2b}, layer 12, width 16k canonical; $d_{\text{model}}=2304$); \S\ref{sec:spine} re-runs at width $65$k and layer $9$.

\paragraph{Step 1: interventional content-response and cover sets.} For each latent $l$ and pair $p$, the \emph{content-response} is $r_l(p)=a_l(x_{\text{on}})-a_l(x_{\text{off}})$. A latent's \emph{cover set} $C_l$ is the set of pairs whose content flip it tracks reliably ($r_l(p)>\tau_{\text{resp}}$, $a_l(x_{\text{on}})>0$) and precisely (firing-precision $\geq 0.7$ on its own support). Because absorbers fire on only a handful of words, a mean-over-pairs prefilter would discard them; eligibility is therefore \emph{cover-based}.

\paragraph{Step 2: anchored recall-hole-guided precision selection (the discovery step).} \textbf{(1) Anchor:} $l^{*}=\arg\max_l |C_l|$, the highest-recall ``parent'' candidate, chosen using \emph{only} the pairs and \emph{not} the absorption diagnostic; an \emph{unsupervised firing-floor} step requires the anchor to fire on the held-out corpus above $5\%$, rejecting spurious high-cover latents (which fixes a letter-I anchor that fired $0\%$ on corpus). \textbf{(2) Hole:} $H = P \setminus C_{\text{anchor}}$, the pairs the parent goes silent on---the recall hole that \emph{names the under-served sub-context, label-free}. \textbf{(3) Precision-select:} over latents covering $H$, choose by held-out per-sub-context firing-precision the precise specialist (Georgia selects latent $16009$ at precision $0.955$, not $4697$ at $0.335$), subject to mutual exclusivity (firing-Jaccard $<0.1$) and a bootstrap-CI-positive coverage gain. \textbf{Motivation, not guarantee.} Because absorbers respond on disjoint supports, covering a parent's holes with complementary specialists is naturally a maximum-coverage problem \citep{Nemhauser1978, Feige1998}; we use that lens to \emph{motivate} the search. But for every downstream/edit result the procedure is effectively $k{=}1$ (it proposes \emph{the single precise absorber}), so we present set-cover/$(1{-}1/e)$ as motivation, not a load-bearing guarantee, and report (\S\ref{sec:edit}) that the discovery is inert versus a max-precision selector for the \emph{edit}---its value over max-precision is the recall-hole \emph{anchoring} that names which sub-context to gate.

\paragraph{Non-circular diagnostic and auditable graph.} Specialization edges are \emph{scored}, never formed, by the absorption diagnostic of \citet{Chanin2024}---we use the domain-agnostic \emph{form-free} variant (the probe-projection implemented in SAEBench as \texttt{absorption\_fraction}), with the parent probe trained on data \emph{disjoint} from grouping. Because the anchor is chosen by recall available to every baseline, a label-free unit beating a supervised oracle is not undercut. Each admitted unit is emitted with logit-lens tokens, top conditioning contexts, and directed anchor$\to$child specialization edges---a feature-level knowledge graph.

\paragraph{Editable graph operators.} Two operators act through a named anchor$\to$absorber edge. \emph{Repair} adds the absorber to the suppressed parent ($\max$-pool) to recover the parent's recall hole (\S\ref{sec:spine}). \emph{Sparse-gated edit} ablates the single absorber, $h \leftarrow h - \lambda\,z_l\,W_{\text{dec}}[l]$, gated by the latent's own sparse firing (\S\ref{sec:edit}).

\paragraph{Secondary: the correlation track and multi-member units.} Where a concept \emph{splits}, sub-latents share firing support and co-respond positively, so we build a sign-aware soft-thresholded affinity from positive Spearman correlation \citep{Zhang2005} and run Leiden community detection \citep{Traag2018}. We report this track as \emph{secondary/exploratory}: it ties weak baselines (toxicity unit AUC $0.762$ vs.\ best raw latent $0.765$), and ablating the full multi-member unit instead of the single absorber strictly \emph{lowers} retained utility on the edit (\texttt{large}: single $1.87$ vs.\ unit $1.38$) [ARTIFACT:art_3WXWsaSoGMnK]. The demonstrated value of the machinery is \emph{proposing} the single precise sub-context latent.

# Testbeds, Baselines, and Protocol
\label{sec:setup}

\paragraph{Constructed testbeds.} We built seven frozen, schema-standardized families. All are pure text/data artifacts, so absorption presence is an empirical question for the SAE run, not a construction artifact. The first-letter testbed contributes $17{,}180$ examples over five letters [ARTIFACT:art_dpYpjSn2Xvg3]; the non-spelling testbed contributes $24{,}128$ numeric and is-a-country examples [ARTIFACT:art_t2uUbjSwpd3t]; the toxicity family contributes $37{,}707$ examples \citep{Logacheva2022, Borkan2019} [ARTIFACT:art_8QO7pl6Pd8UQ]; a supporting family contributes $30{,}739$ examples of CAD-IMDB sentiment, CEBaB aspect-sentiment, and a bias\_in\_bios boundary-null \citep{Kaushik2019, Abraham2022, DeArteaga2019} [ARTIFACT:art_21JWypIydPMX]; a homograph-entity testbed supplies prospective router candidates [ARTIFACT:art_2xQn686KUmV5]; a safety-identity testbed ($36{,}448$ examples) hosts the safety screen [ARTIFACT:art_KNPsfjByyxiS]; and a named-entity-homograph slice hosts the confirmatory pass.

\paragraph{Baselines.} For classification we compare against raw latents, observational clusters (count-matched), dense probes, supervised oracle pools, label-free/oracle group-robustness probes, a random-eligible pool, and three label-free selectors (S-rec, S-prec, S-mag) that isolate the selection rule. For the edit (\S\ref{sec:edit}) the comparators, in one unified pipeline, are: KG-ABL (discovered absorber, sparse-firing-gated); \textbf{DENSE-SUB-ABL}, the \emph{strongest} (ungated) sub-context diff-of-means erasure $u_{\text{sub}}$, our \emph{lead} comparator; \textbf{DENSE-SUB-ABL-GATED-FAIR}, the genuinely fair control (erase $u_{\text{sub}}$ only where a precise logistic detector $d_{\text{sub}}(h)>0$ fires, bounded $\beta{\leq}1$; one operator across all cases); DENSE-SUB-ABL-GATED, the demoted iter-prior footprint-matched gate (calibrated to the absorber's $\sim$$3\%$ global firing fraction, hence forced to over-erase); DENSE-WHOLE-ABL; \textbf{MAX-PRECISION}, the single most precise latent on the sub-context (no recall-hole anchoring), the decisive ablation of whether discovery adds anything; and RAND.

\paragraph{Statistics.} The primary object is the per-concept paired bootstrap of the AUC or outcome difference ($B=10{,}000$, resampling content-flip pairs or held-out prompts as clusters), with Holm--Bonferroni across headline claims and a second different-family LLM judge required to also exclude $0$ for any edit win. Encoding and software pins are in the Appendix.

# The Auditability and Localization Spine
\label{sec:spine}

The durable contribution is that the KG's edges are \emph{measured} and the spine is \emph{not} an artifact of one dictionary. We lead with it because it is the strongest evidence and does not depend on any edit-quality claim.

[FIGURE:fig5]

\paragraph{KG-guided recall repair, honestly counted.} For every eligible under-served sub-context the KG names a covering absorber on a selection split and adds it to the anchor; recall recovery on a disjoint held-out split must exceed the $95$th/$99$th percentile of a \emph{random single content-responsive-latent addition} control (paired bootstrap, $B=10{,}000$). Across spelling, taxonomic, and numeric families, $69$ repair variants over $54$ candidate holes enter one Benjamini--Hochberg family; \textbf{$30$ survive FDR $\leq 0.05$}, spanning \textbf{$22$ distinct suppressed-parent recall holes} (spelling $13$, homograph-taxonomic $3$, numeric $6$) [ARTIFACT:art_sxwT7hK6YFEA]. The control is cleared by $28/28$ surviving holes at the $95$th percentile and $23/28$ at the $99$th [ARTIFACT:art_w7p8du2N1f0Y]; numeric is flagged \emph{below-gate} (digit-token reconstruction cosine $0.876<0.9$). A dense label-free probe classifies the holes but its decoder-projection argmax is always the \emph{parent}, never an absorber---it exposes no addable per-sub-context latent, whereas the KG names exactly one.

\paragraph{A KG-localized surgical edit, with the selectivity artifact corrected.} Measuring on-target next-token KL at the edited token and collateral on siblings, surgical selectivity ($=$ on-target/collateral at matched effect) over the $n{=}6$ absorption cases at $16$k has \textbf{mean $1452\times$ and median $1262\times$}; the cleanly-surgical $n{=}5$ subset has median $1722\times$ [ARTIFACT:art_0CZwPjG2YMCf]. We do \emph{not} claim ``precision predicts surgicality'': it holds within the taxonomic family (Spearman $\rho=0.90$, $p=0.037$) but breaks across families. We also correct a prior divide-by-$\epsilon$ artifact: the $65$k Georgia edit's reported ``$3.7\times10^{6}$ selectivity'' arose because its KG collateral is exactly $0$; the corrected $65$k absorption selectivity is mean $722\times$, median $676\times$ ($n{=}4$), so the $16$k and $65$k Georgia edits are \emph{comparably} surgical, not $2000\times$ apart [ARTIFACT:art_w7p8du2N1f0Y].

\paragraph{Members are human/LLM-auditable.} Describing each of $89$ unit members by its logit-lens top-10 tokens and top-5 activating windows with the sub-context label withheld, an ensemble LLM judge names the sub-context with agreement $0.730$ versus a shuffle null of $0.096$ (gap $0.634$, CI $[0.545,0.724]$). Absorbers are named at $0.756$, anchors at only $0.43$ (the judge over-specifies the parent's mixed windows, an honest caveat) [ARTIFACT:art_sxwT7hK6YFEA].

\paragraph{The wider SAE fully replicates---and absorbs more.} On the $4\times$-wider $65$k canonical SAE (same model+layer, gating cosine $0.928$) all four spine pieces replicate [ARTIFACT:art_4L1MZxvWYlGd]: the homograph holes recur (Georgia recall hole $0.873$, firing-Jaccard $0.004$, AUC $0.995$), the FDR repair loop yields \emph{more} survivors ($52$ distinct holes vs.\ $22$ at $16$k, spelling $29$/taxonomic $8$/numeric $15$---directly consistent with ``wider absorbs more'' \citep{Karvonen2025, Chanin2025}), the Georgia surgical edit reproduces, and the frozen recall-hole router transfers at balanced accuracy $1.0$. The second \emph{layer} (layer 9) replicates only partially: Georgia loses its hole ($0.003$; the layer-9 parent already covers it) while Jordan gains one ($0.536$) with a confirmed surgical edit ($2376\times$). Which homograph is absorbed is a property of the (layer, width) dictionary; the mechanism and its repairs replicate.

\paragraph{Within-SAE selection where the signature holds.} On the Georgia slice the precision-gated rebuild recovers the specialist $16009$ (held-out precision $0.955$), drops the high-coverage low-precision $4697$ ($0.335$), and the rebuilt unit reaches AUC $0.995$, beating every label-free selector with CIs excluding $0$ (S-rec $+0.307$, S-prec $+0.416$, S-mag $+0.294$) and the below-chance supervised pools \citep{Marks2024, Karvonen2024} [ARTIFACT:art___vgSpUe6wAF]. A non-SAE dense probe still edges the unit ($1.000$ vs.\ $0.995$): the contribution is auditable within-SAE selection, not out-classifying a dense probe.

# The Edit: Label-Free Discovery of Where to Gate, Not Edit Quality
\label{sec:edit}

The reviewer of our prior version raised two decisive objections to the edit headline; a controlled re-run with one unified gate operator and a behavioral forget proof confirms both and reframes the contribution.

[FIGURE:fig2]

\paragraph{The task, the unified controls, and the forget proof.} The goal is to make the model forget \emph{one} sub-context---``Georgia is a country,'' the spelling of \texttt{large}, ``Amazon is a company''---while preserving the parent and fluency. We sweep edit strength to match \emph{meaningful} forget across operators, proven $\$0$ and deterministically by (i) a \emph{gold-completion log-probability drop} on $20$--$50$ templated probes per case (expanded from the prior $n{=}4$) and (ii) a \emph{frozen sub-context probe} $d_{\text{sub}}$ (AUC $\approx 1.0$, fit on a disjoint fold) scored on the \emph{real post-edit residual}, with operators matched on the \emph{behavioral} sub-probe-drop curve rather than next-token KL [ARTIFACT:art_Qdoz9eH0AGjh]. We disclose both maximum-forget ceilings, NOOP-identical fractions, and the full collateral-vs-forget curve (Figure~\ref{fig:fig3}). At the matched point we generate a $40$-token greedy continuation under each edit hook on held-out RETAIN/UNRELATED prompts and score it with two judges (\texttt{claude-haiku-4.5} primary, \texttt{gpt-4o-mini} second; $\Delta_{\text{joint}}=$ paired-bootstrap difference of $\text{harmonic\_mean}(\text{fluency},\text{content\_pres})\in[0,2]$). Total judge spend was $\$1.07$ over $2709$ calls, zero failures.

[FIGURE:fig3]

\paragraph{Result 1: de-inflation.} Against the \emph{strongest} dense baseline (ungated $u_{\text{sub}}$ erasure), a discovered absorber gated by its own firing wins where the feature is concentrated: on \texttt{large} (absorber $8463$) $\Delta_{\text{joint}}={+}0.97$ (CI $[0.70,1.25]$; second judge $+0.55$, $[0.35,0.78]$), and on the named-entity homograph \texttt{Amazon} (absorber $6846$) $\Delta_{\text{joint}}={+}0.87$ ($[0.55,1.17]$; second judge $+0.58$, $[0.37,0.79]$), each with strictly lower collateral and curve-dominance $1.0$ (Table~\ref{tab:edit}). An integrity-lock re-analysis confirms the $+1.00$ ($[0.79,1.21]$) lead number and shows that the previously-headlined ``$+1.58$'' was a comparison against a \emph{handicapped} footprint-matched gate driven to $\beta{\approx}2.97$ over-erasure, producing retain-collateral $0.290$---$13.8\times$ its own ungated form's $0.021$ [ARTIFACT:art_Mlx5GfSusrjm]. We report $+1.58$-vs-footprint-gated only as a caveated robustness point, never as the headline.

\paragraph{Result 2: a genuinely fair gated dense control closes the gap.} The decisive control erases the \emph{same} labeled direction $u_{\text{sub}}$ only where the precise detector $d_{\text{sub}}$ fires, with bounded $\beta{\leq}1$ (gate balanced accuracy $0.96$--$1.00$). \textbf{It matches the discovered absorber on every case}: on \texttt{large}, $\Delta_{\text{joint}}^{\text{KG-vs-fair}}={-}0.05$ (CI $[-0.15,0.00]$, includes $0$); on \texttt{Amazon}, exactly $0.00$; on Georgia, $0.00$ ($[-0.21,0.21]$). The fair gate is even \emph{cleaner} on retain collateral ($2.8\times10^{-6}$ vs.\ KG's $5.1\times10^{-5}$ on \texttt{large}). No case is ``KG beats both the strongest ungated dense \emph{and} the fair gate'' ($0/8$); the overall verdict is \textbf{DISCOVERY\_IS\_THE\_VALUE: the fair gate closes the gap} [ARTIFACT:art_Qdoz9eH0AGjh]. Because gating is prior art \citep{Lee2024, Zhang2026, Turani2026, Wang2024}, the SAE-specific value is not the edit operator but the \emph{label-free discovery of where to gate}: the absorber's own sparse firing is a calibration-free gate, found with no sub-context labels, whereas the fair dense gate must be \emph{trained} on $d_{\text{sub}}$.

\paragraph{Result 3: the win tracks concentration, and set-cover is inert.} The meaningful-forget edit cases span both regimes: the absorption case \texttt{large} \emph{and} the co-firing case \texttt{insult} (firing-Jaccard $0.882$, no recall hole, sub-probe drop $0.45$) both forget, while the absorption losses Georgia/Jordan are \emph{distributed} senses (max single-latent forget KL $0.06$/$0.11$, sub-probe drop $0.05$/$0.0$). An integrity re-analysis quantifies the predictor: lexical \emph{concentration} (precision $\times$ single-latent leverage) tracks the win at point-biserial $r{=}{+}0.63$, the absorption label does \emph{not} ($r{=}{-}0.09$), and inverse footprint anti-correlates ($r{=}{-}0.80$, because distributed senses also fire sparsely)---predictive $\Delta={+}0.72$ (CI $[0.08,1.20]$) [ARTIFACT:art_Mlx5GfSusrjm]. We therefore \emph{drop} the prior claim that the win traces to absorption structure. The decisive ablation seals it: replacing the anchored set-cover with the single most precise latent on the sub-context (MAX-PRECISION) \emph{ties} KG-ABL on every case ($0/8$ where discovery adds value; $3/8$ it is the \emph{same} latent), so the set-cover machinery is inert for the edit [ARTIFACT:art_Qdoz9eH0AGjh].

[FIGURE:fig4]

\paragraph{Result 4: an honest retraction and a thin base.} We \emph{retire} the prior-iteration claim that a discovered absorber beats dense on Georgia ($+0.561$ against the \emph{ungated} $u_{\text{sub}}$): that win sat at a near-NOOP operating point (max single-latent forget KL $0.065$, NOOP-identical on $0.889$ of prompts, sub-probe drop $0.075$, completion CI including $0$)---it ``won'' by barely editing [ARTIFACT:art_Mlx5GfSusrjm]. A wider screen of concentrated homograph/spelling absorbers under the fair control finds \textbf{zero} independent concentrated wins (Bush/Cook do not meaningfully forget despite clean firing signatures), so the positive edit base does not broaden under the fair control [ARTIFACT:art_bPU1evbgN0og]. We therefore retarget the paper to lead with the auditability spine (\S\ref{sec:spine}) and present the edit as a \emph{scoped} capability whose SAE-specific value is where-to-gate discovery. Finally, the two instruments \emph{disagree} at the next-token-KL-matched point on \texttt{large} (sub-probe favors KG by $0.42$, completion favors gated by $1.01$), demonstrating that KL-matching does not equalize behavioral forgetting---which is why we match on the behavioral sub-probe-drop curve and report both instruments [ARTIFACT:art_Mlx5GfSusrjm].

\begin{table}[t]
\centering
\small
\caption{Unified fair-control edit study (one gate operator across all cases). KG-ABL = discovered absorber, sparse-firing-gated. Lead comparator = DENSE-SUB-ABL (strongest ungated dense). Fair control = DENSE-SUB-ABL-GATED-FAIR (precise $d_{\text{sub}}$ gate, $\beta\leq1$). $\Delta_{\text{joint}}$ = paired-bootstrap difference of judged $\text{HM}(\text{fluency},\text{content\_pres})\in[0,2]$, $B{=}10{,}000$, primary judge. $^\ast$ = both-judge CIs exclude $0$. No case beats \emph{both} the strongest ungated dense and the fair gate; the fair gate closes the gap everywhere.}
\label{tab:edit}
\begin{tabular}{lllccc}
\toprule
Case (absorber) & regime & forget? & $\Delta_{\text{joint}}$ vs.\ ungated [CI] & $\Delta_{\text{joint}}$ vs.\ fair [CI] & verdict \\
\midrule
\texttt{large} (8463) & absorption/conc. & yes & $+0.97\ [0.70,1.25]^{\ast}$ & $-0.05\ [-0.15,0.00]$ & fair closes gap \\
\texttt{Amazon} (6846) & absorption/conc. & yes & $+0.87\ [0.55,1.17]^{\ast}$ & $\phantom{-}0.00\ [0.00,0.00]$ & fair closes gap \\
\texttt{Bush} (1418) & absorption/conc. & weak & $-0.06\ [-0.29,0.13]$ & $-0.26\ [-0.45,-0.11]$ & fair $\succ$ KG \\
Georgia (16009) & absorption/distrib. & near-NOOP & $+0.48\ [0.14,0.80]^{\ast}$ & $\phantom{-}0.00\ [-0.21,0.21]$ & near-NOOP (retracted) \\
\texttt{insult} (13367) & co-firing/conc. & yes & --- & $+0.12\ [-0.20,0.43]$ & concentration, not absorption \\
\texttt{Cook} (15631) & absorption/conc. & no & --- & --- & no meaningful forget \\
Jordan (540) & absorption/distrib. & no & --- & --- & no meaningful forget \\
United States (846) & co-firing/distrib. & no & --- & --- & router false-neg.\ / no forget \\
\bottomrule
\end{tabular}
\end{table}

# Safety-Relevant Absorption Is Homograph-Confined
\label{sec:safety}

The goal asks for reliability on safety-relevant attributes; we tested directly and report the result as the contribution's ceiling.

\paragraph{A \$0 absorption screen over four identity hierarchies.} From the full \texttt{civil\_comments} corpus ($1{,}756{,}346$ rows, CC0) we build gazetteer-matched windows and content-flip templates for religion, race/ethnicity, orientation/gender, and nationality, with group labels assigned by surface form only. Per hierarchy we identify a firing-floor-validated parent latent and screen every group for the absorption signature (recall hole $>0.5$, firing-disjoint absorber Jaccard $<0.1$, precision $\geq 0.7$, $\geq 150$ eligible, hole-coverage gain CI excluding $0$), corroborated by the non-circular form-free oracle [ARTIFACT:art_yAQgbq5Wgymx].

\paragraph{Of $44$ safety groups, exactly two are structured---and both are homographs.} The positive control reproduces (Georgia recall hole $0.77$, Jordan $0.68$). Among the $44$ eligible safety groups, only \texttt{white} (race; hole $0.63$, Jaccard $0.019$, oracle $0.46$) and \texttt{straight} (orientation; hole $0.72$, Jaccard $0.009$, oracle $0.26$) exhibit the signature, and both are lexical homographs (Table~\ref{tab:safety}); the other $42$---Muslim, Hindu, gay, lesbian, Asian, Mexican, Chinese, Canadian, $\dots$---show \emph{no} parent recall hole. Structure does not imply leverage: on the conditional downstream test, the two structured \emph{safety} groups do not transfer (\texttt{straight} wins under the primary judge only at tiny magnitude; \texttt{white}'s oracle-confirmed absorber has no on-target effect). The verdict is \textbf{safety absorption found, no win}.

\paragraph{Confirmatory named-entity pass.} An identical screen over named-entity homographs finds three of five structured and oracle-confirmed---\texttt{Amazon} (hole $0.61$, Jaccard $0.048$, precision $0.99$), \texttt{Bush} ($0.79$/$0.021$/$1.00$), \texttt{Cook} ($0.72$/$0.045$/$1.00$)---while \texttt{Apple} (hole $0.25$) and \texttt{King} ($0.42$) are not [ARTIFACT:art_ZxVw0e4seBq3]. This reinforces the settled demographic null: absorption is a property of lexically polysemous surface tokens, not demographic semantics. Critically, a clean firing signature is \emph{not} a usable edit handle: Bush and Cook have clean signatures yet $\max$-forget ceilings of $0.04$/$0.03$ and do not meaningfully forget (\S\ref{sec:edit}).

\begin{table}[t]
\centering
\small
\caption{Identity absorption screen. ``struct.''\ = groups with the absorption signature (recall hole $>0.5$ and firing-disjoint specialist). Only homograph tokens are structured; no demographic safety group yields a robust downstream win.}
\label{tab:safety}
\begin{tabular}{lrrl}
\toprule
Hierarchy & eligible & struct. & structured groups \\
\midrule
taxonomic (control) & 20 & 1 & Georgia (homograph) \\
religion & 11 & 0 & --- \\
race/ethnicity & 8 & 1 & \texttt{white} (homograph) \\
orientation/gender & 5 & 1 & \texttt{straight} (homograph) \\
nationality & 20 & 0 & --- \\
\midrule
\textbf{safety total} & \textbf{44} & \textbf{2} & all structured are homographs \\
\midrule
named-entity (confirmatory) & 5 & 3 & \texttt{Amazon}, \texttt{Bush}, \texttt{Cook} \\
\bottomrule
\end{tabular}
\end{table}

# Router, Breadth, and Goal-Named Downstream Tasks
\label{sec:router}

\paragraph{An exploratory recall-hole router.} The recall-hole-alone rule (predict absorption iff the parent's per-sub-context recall hole $>\tau_h=0.779$) separates the $12$ derivation concepts perfectly (balanced accuracy $1.0$, leave-one-out $0.833$) [ARTIFACT:art_F_-HUhl0NR_i]. To test it out-of-sample we enlarged the prospective set with the homograph-entity testbed ($5.6\times$). It validates on the base-rate co-firing direction (co-firing-predicted $29/30$, Wilson $[0.833,0.994]$) but the \emph{discriminative} absorption stratum does not: homograph $2/4$ (Wilson $[0.15,0.85]$), homograph$+$spelling $5/10$ ($[0.237,0.763]$)---both CIs include $0.5$. We therefore \emph{demote} the router to an exploratory diagnostic. Note also that the router predicts the absorption \emph{regime}, not the edit win, which tracks concentration (an orthogonal axis): \texttt{insult} co-fires yet forgets; Georgia/Jordan absorb yet do not.

\paragraph{A breadth count that bounds the phenomenon.} Of $64$ homograph entities with a stable estimate, only \textbf{three} are absorption-structured---all months (March $0.997$, June $0.947$, February $0.573$); zero of $22$ cities, $20$ given-names, and $10$ brands [ARTIFACT:art_F_-HUhl0NR_i]. A clean profession is-a hierarchy ($28$ professions) shows uniform-high parent recall and \textbf{$0/28$} absorption [ARTIFACT:art_Iy77UHoNaIhS]. Absorption recurs but is confined to homograph/polysemy tokens.

\paragraph{The goal's named downstream tasks, reported honestly.} The goal names three downstream evaluations; we deliver all three as nulls and report them as such. (1) \emph{Classification of safety-relevant attributes}: no SAE unit out-classifies a dense probe on any task (Georgia $0.995$ vs.\ $1.000$; toxicity unit AUC $0.762$ vs.\ raw $0.765$, dense $0.84$--$0.89$, sub-attributes $0.63$ vs.\ $0.93$) [ARTIFACT:art_-o2RPMOZp37A]. (2) \emph{Steering with side-effect measurement}: the unit's mean-member direction is most surgical only on letters L and D ($2/5$) [ARTIFACT:art_0ueMMR8Tt02P]. (3) \emph{Model-diffing}: no instruction-tuned Gemma Scope SAE exists for the 2B model, so the shared-SAE base-vs-IT shift is detectable but \emph{not} concept-specific (control-subtracted genuine shift $+0.000$, CI $[-0.009,0.007]$), a confound-bounded null [ARTIFACT:art_jI2KIJotjzIU]. The contribution is auditable localization, not these tasks.

# Honest Negatives and Limitations
\label{sec:neg}

We collect the method's failures in one place, each with its statistic. (1) \textbf{No edit-quality win over a fair dense control}: the genuinely fair $d_{\text{sub}}$-gated dense control matches the discovered absorber on every case, and gating itself is prior art; the SAE-specific value is label-free where-to-gate discovery. (2) \textbf{The edit win tracks concentration, not absorption}: a concentrated co-firing latent wins, distributed absorbers lose, and the set-cover machinery is inert versus max-precision. (3) \textbf{The positive edit base is thin}: only \texttt{large} and \texttt{Amazon} meaningfully forget \emph{and} beat the strongest ungated dense, and the base does not broaden under the fair control; we retracted our prior near-NOOP Georgia win. (4) \textbf{No dense-probe out-classification} on any task. (5) \textbf{Safety absorption is homograph-confined} ($2/44$, $0/28$ professions, $3/64$ entities); no robust safety win. (6) \textbf{The router is exploratory} (prospective Wilson includes $0.5$). (7) \textbf{Grouping is discovery, not a multi-member win}: wins trace to single absorbers; the C-track ties weak baselines. (8) \textbf{Replication is layer-conditional}; numeric is below-gate ($0.876$); model-diffing is a confound-bounded null. Each is reported with its statistic, not spun as future work.

# Discussion
\label{sec:discussion}

\paragraph{What is established.} Executed on a frozen Gemma Scope SAE, CCRG is a training-free, label-free \emph{discovery procedure} that surfaces the single precise absorber a marginal-attribution ranking drops and emits a feature knowledge graph whose edges carry \emph{measured}, replicable repair utility---the durable, strongly-evidenced result. The reliability gain is localization and auditability, not classification. On editing we deliver an honest, fair-control correction of our own prior claim: a discovered absorber beats the \emph{strongest} dense baseline on concentrated features ($+0.97$/$+0.87$), but a genuinely fair gated dense control matches it, so the SAE-specific value is the label-free discovery of \emph{where} to gate, and the advantage tracks lexical concentration rather than the absorption structure the method discovers.

\paragraph{A regime-scoped contribution with an honest ceiling.} The most useful lesson is that latent grouping is not a universal repair; the regime where it adds value---label-free localization of homograph-polysemy absorption with a suppressed parent---is \emph{narrow} and does \emph{not} coincide with the safety-relevant attributes the goal targets ($2/44$ groups, both homographs). The work positions precisely against the ``discover, don't act'' critique \citep{Peng2025}: CCRG discovers the sub-context handle through interventional grouping; acting through it is no better than a fair dense baseline, but \emph{finding} it is label-free, auditable, and the absorber's firing is itself the gate.

\paragraph{Why the fair-gate result is publishable, not a failure.} A clean negative---the fair dense gate matches the discovered absorber---is informative: it isolates the genuine SAE-specific deliverable (label-free discovery and auditability) from the part that is prior art (conditional editing), and it corrects an over-claim that would otherwise propagate. Combined with the replicated auditability spine and the settled safety null, the contribution is a precise, honest characterization of when frozen-SAE grouping helps.

# Conclusion
\label{sec:conclusion}

We presented Co-Response Grouping, a training-free, label-free procedure that organizes the latents of a frozen public SAE by their interventional response to content counterfactuals---anchoring on the highest-recall parent, reading its recall hole to name an under-served sub-context, and precision-selecting the single absorber latent that marginal attribution silently drops. The durable result is an \emph{auditable feature knowledge graph} with \emph{measured} localization utility: $22$ distinct suppressed-parent recall holes recovered over a random single-latent control ($30$ FDR survivors), a median $1262\times$-selective surgical edit (corrected from a divide-by-$\epsilon$ artifact), LLM-auditable members, and full replication on a $4\times$-wider SAE that absorbs more. On editing we report an honest correction: against the strongest dense baseline a discovered absorber wins on concentrated features ($+0.97$ on \texttt{large}, $+0.87$ on \texttt{Amazon}), but a genuinely fair gated dense control closes the gap everywhere, so the SAE-specific value is the label-free discovery of \emph{where} to gate---and the win tracks lexical concentration, not absorption, with set-cover discovery inert versus a max-precision selector. Safety-relevant absorption is homograph-confined ($2/44$ groups, $0/28$ professions); the durable value is auditable, label-free-discovered, regime-targeted localization of homograph-polysemy absorption.

\paragraph{Future work.} Characterize a priori what makes an absorbed feature \emph{concentrated} enough to edit; test whether label-free where-to-gate discovery lowers the labeling cost of conditional editing at scale; search wider entity vocabularies for additional concentrated suppressed-parent homographs; and revisit model-diffing if a paired instruction-tuned SAE becomes available.

# Appendix: Reproducibility
\label{sec:repro}

\paragraph{Encoding and gating.} SAEs are loaded directly from Gemma Scope \texttt{params.npz} (primary: canonical \texttt{layer\_12/width\_16k}, \texttt{average\_l0\_82}, JumpReLU, $d_{\text{model}}=2304$; cross-dictionary: \texttt{layer\_12/width\_65k} and \texttt{layer\_9/width\_16k}); the residual is captured by a forward hook on \texttt{model.layers[L]} output (\texttt{hidden\_states} index $L{+}1$). The edit and safety runs gate at cosine $0.919$ (L0 $\approx 88$); the $65$k and layer-9 runs at cosine $0.928$/$0.930$. Numeric digit-token reconstruction is $0.876<0.9$ and flagged below-gate.

\paragraph{The unified fair-gate operator and forget proof.} DENSE-SUB-ABL-GATED-FAIR erases $u_{\text{sub}}$ by $h\leftarrow h-\min(\beta,1)(h\!\cdot\!u_{\text{sub}})u_{\text{sub}}$ only where the precise supervised detector $d_{\text{sub}}(h)=w_{\text{sub}}^\top h + b_{\text{sub}}>0$ fires (gate balanced accuracy $0.96$--$1.00$ on a disjoint fold), one operator across all cases; the demoted footprint-matched gate calibrates a magnitude threshold $\tau$ so the gate's global firing fraction equals the absorber footprint $f_{\text{kg}}$ ($\sim$$3\%$), forcing $\beta{\approx}3$ over-erasure. Meaningful forgetting is proven by a gold-completion log-probability drop on $20$--$50$ templated probes and a frozen $1$-D sub-probe $d_{\text{sub}}$ (AUC $\approx 1.0$) read on the real post-edit residual via \texttt{read\_resid\_under\_edit}; operators are matched on the behavioral sub-probe-drop curve [ARTIFACT:art_Qdoz9eH0AGjh].

\paragraph{Models, edits, and software.} Model \texttt{google/gemma-2-2b} (and \texttt{-2b-it} for model-diffing) via ungated mirrors, bf16, eager attention; SAE \texttt{google/gemma-scope-2b-pt-res}. The edit experiment reuses the iter-7 surgical-edit engine verbatim (\texttt{JumpReLUSAE}, \texttt{ModelBundle}, \texttt{make\_edit\_hook}, \texttt{side\_effects}, \texttt{paired\_bootstrap\_diff}) and adds the unified \texttt{erase\_dir\_dsub\_gated} operator, the MAX-PRECISION selector, and two LLM judges. KG/units are taken from prior unit/KG artifacts (taxonomic anchor $3792$, Georgia$\to$$16009$, first-letter L $8463$$\to$\texttt{large}, named-entity parent $2768$). LLM judging used \texttt{claude-haiku-4.5} (primary) and \texttt{gpt-4o-mini} (second); edit spend was $\$1.07$ ($2709$ calls, $0$ failures); all other compute is $\$0$ on a single NVIDIA L4 ($16$--$23$\,GB). Citation venues follow a verified audit (e.g.\ \citet{Chanin2024} NeurIPS 2025; \citet{Wu2025}, \citet{Karvonen2025}, \citet{Li2024} ICML 2025; \citet{Leask2025}, \citet{Lee2024}, \citet{Marks2024} ICLR 2025; \citet{Arad2025} EMNLP 2025; \citet{Farrell2024} NeurIPS 2024 Safe-GenAI Workshop).

\bibliographystyle{plainnat}
\bibliography{references}

</current_paper>

<reviewer_feedback>
Feedback from the paper reviewer this iteration.

- [MAJOR] (contribution) Goal-contribution mismatch. The stated goal is a clustering-based method that organizes SAE latents into more reliable group-level UNITS that beat single latents on three named downstream tasks (safety-attribute classification, steering with side-effect measurement, model-diffing). The paper instead establishes that (a) the clustering/multi-member machinery is inert and 'only adds collateral' (the method is effectively k=1 single-absorber selection); (b) all three goal-named downstream tasks are delivered as nulls (no SAE unit out-classifies a dense probe; steering is more surgical on only 2/5 letters; model-diffing is a confound-bounded +0.000 null); and (c) the MAX-PRECISION ablation shows the set-cover discovery adds value in 0/8 edit cases. After all the honest corrections, the surviving positive is a narrow, label-free re-implementation of Chanin's absorption diagnostic plus an auditable KG. This is admirable as integrity but leaves the net contribution below the bar for an ICLR/ICML primary.
  Action: Pick one and commit: (1) deliver a demonstrated positive the community can build on (see the label-efficiency experiment), or (2) explicitly reposition away from 'clustering' to 'label-free single-specialist localization', stating in the intro that the clustering hypothesis was tested and did not pay off, and make the rigorous homograph-confinement boundary result the deliberate headline contribution with a clear 'why this matters' for the SAE-reliability/safety community.
- [MAJOR] (evidence) The central surviving positive claim is asserted, not demonstrated. The paper concedes the SAE edit is matched by a genuinely fair d_sub-gated dense control and that gating is prior art, then retreats to 'the SAE-specific value is the training-free, label-free discovery of WHERE to gate'. But nowhere is it shown that this label-free discovery produces any benefit over the labeled alternative. The fair gate needs d_sub trained on sub-context labels; the paper never quantifies the labeling cost saved, never identifies a regime where the label-free route wins, and the Future Work section itself admits 'test whether label-free where-to-gate discovery lowers the labeling cost of conditional editing at scale' is undone. So the paper's load-bearing positive thesis currently has no supporting experiment.
  Action: Run the label-scarce demonstration: vary the number of sub-context labels available to fit d_sub (e.g., 0, 1, 5, 20, full) and plot editing/localization quality for the fair dense gate vs the label-free SAE discovery. If the SAE discovery holds quality where d_sub collapses for lack of labels, that is the concrete, demonstrated 'discovery is the value' result the paper needs. If it does not, report that honestly and adjust the thesis.
- [MAJOR] (scope) Significance is sharply limited by homograph-confinement, and the paper does not make the case for why others would build on it. The phenomenon CCRG localizes is confined to lexically polysemous surface tokens: 2/44 safety identity groups (both homographs), 3/64 homograph entities, 0/28 professions. The headline auditability spine is therefore about a structure that appears in a small, lexically-defined slice of features and does not coincide with the safety-relevant attributes the goal targets. As written, the reader is left unsure what capability or scientific advance this enables for the broader community.
  Action: Either broaden the empirical base (systematically mine a large entity/word vocabulary for additional suppressed-parent homographs and validate a sample, turning breadth into a real coverage result), or frame the confinement as the deliberate scientific contribution with explicit downstream consequences: e.g., 'the SAE absorption-reliability concern is a lexical-polysemy phenomenon, so practitioners auditing safety attributes need not fear absorption there; here is the label-free screen to verify it on any frozen SAE'. Make the 'so what' explicit in the discussion.
- [MINOR] (clarity) Internal inconsistency between the auditability spine (Section 5) and the edit section (Section 6). Section 5 advertises 'a median 1262x-selective surgical edit' as a durable contribution, but its selectivity is computed against whole-parent dense erasure (DENSE-WHOLE-ABL), a baseline Section 6 explicitly disowns, while Section 6 shows that a fair gated dense control is equally or MORE surgical (retain collateral 2.8e-6 vs KG 5.1e-5). A reader who takes Section 5 at face value will believe the SAE edit is uniquely surgical, which Section 6 contradicts.
  Action: Reconcile the two sections: present the 1262x number strictly as evidence that the KG-NAMED latent's edit is localized (a localization claim), not as an SAE-specific surgical advantage, and add a one-line cross-reference noting that against the fair gated dense control the surgical advantage disappears. Avoid letting the whole-parent strawman do rhetorical work the fair-gate result removes.
- [MINOR] (rigor) The broad recall-repair headline (22 distinct holes, 30 FDR survivors, over a random single-latent control) rests on a near-definitional comparison. The absorber is selected by held-out per-sub-context precision for covering the hole H, then evaluated on recovering recall on H; even on disjoint splits, 'the latent I chose because it fires on sub-context X recovers recall on X better than a random latent' is close to tautological, and the control (a single random content-responsive latent) is weak. The FDR family therefore certifies that the naming is self-consistent more than that the repair is useful.
  Action: Add a stronger control (e.g., the best latent selected by an alternative label-free signal not aligned with the eval metric, or the dense-probe argmax which the paper already notes is always the parent) and, more importantly, show the repaired unit buys a downstream capability the parent-alone-plus-dense-probe cannot. If it does not (as the classification null suggests), state that the repair demonstrates correct localization rather than utility, and temper the 'measured repair utility' language accordingly.
- [MINOR] (presentation) The paper reads as an iteration/rebuttal log rather than a finished submission. The abstract, intro, and Section 6 all foreground 'A prior version of this work claimed...' and 'An honest self-correction', and the body carries a dense alphabet of operators and internal experiment labels (M1''', M3''', S-rec/S-prec/S-mag, KG-ABL, DENSE-SUB-ABL-GATED-FAIR, MAX-PRECISION). Combined with the repeatedly-redefined central object, this makes the durable thesis hard to extract on a first read.
  Action: Present the corrected results as the results; move the self-correction history to a brief limitations/changelog note. Fix one stable name for the central object, define the gate operators once in a compact table, and relegate the selector zoo and M-numbered labels to the appendix. Lead each section with its single takeaway sentence.
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

### [2] HUMAN-USER prompt · 2026-06-18 21:56:35 UTC

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
