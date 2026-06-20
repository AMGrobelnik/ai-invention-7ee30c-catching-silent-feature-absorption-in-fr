# gen_plan_research_1 — test_idea

> Phase: `invention_loop` · round 8 · `gen_plan`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_plan_research_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 10:39:56 UTC

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
You are expanding an artifact direction of type: RESEARCH

RESEARCH
Web research to answer key questions — like a researcher making decisions.
Runtime: LLM Agent, no code execution.
Tools: the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text).
Capabilities: Find, synthesize, and compare information across sources; survey SOTA and best practices.
Deps: REQUIRED none | OPTIONAL other RESEARCH to build on prior findings
</artifact_type_info>

<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>
</available_resources>

<time_budget>

The research executor has 3h total (including writing code, debugging, testing, and fixing errors).

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
</hypothesis>

<artifact_direction>
Make this direction concrete and actionable. Keep the same type and respect dependencies.

id: research_iter8_dir4
type: research
objective: >-
  NOVELTY TRIM + CONCENTRATION FRAMING + RETARGET/VENUE + LOCKED CITES (M5''' + M3''' framing + M2''' retarget) -- finalize
  positioning for GEN_PAPER_TEXT. (1) Sharpen the explicit DELTA vs Chanin's absorption diagnostic AND vs a max-precision
  selector: state precisely what the label-free anchor + recall-hole + precision-gate buys over (i) running Chanin's diagnostic
  directly (which needs a supervised probe/logit) and (ii) the simple 'pick the most precise latent firing on the target sub-context'
  selector; if the iteration shows set-cover ties max-precision (likely, since every reported win is effectively k=1), ground
  the trim to 'anchored recall-hole-guided PRECISION SELECTION of a single absorber' and present set-cover/(1-1/e) as MOTIVATION
  only, not a load-bearing guarantee. (2) Ground the M3''' MECHANISM reframe -- the edit advantage is a property of a PRECISE/CONCENTRATED
  latent acting as a SHARPER conditional gate than a footprint-matched dense projection; absorption is ONE label-free-discoverable
  source of concentration, not the cause of the win -- by surveying prior work relating per-feature precision/sparsity/selectivity
  to steering surgicality or conditional-gate sharpness, so 'concentration not absorption' is POSITIONED, not merely asserted.
  (3) Ground and decide the M2''' RETARGET: cite-and-justify leading the paper with 'training-free auditable LOCALIZATION
  + EDITING of homograph-polysemy absorption' (ICML primary acceptable, ICLR fallback), with the safety-homograph-confinement
  NULL as the headline limitation and the concentrated-feature edit as a scoped capability; supply the retargeted abstract/intro
  spine for BOTH outcomes (>=4 concentrated wins landed vs base-stays-thin). (4) Lock the citation set (carry iter-7 locked
  venues verbatim, add any new concentration/precision-steering cites with verified IDs/venues/authors, flag unresolved --
  do NOT invent) + a presentation-strip checklist.
approach: >-
  Pure web research via aii-web-tools (search -> fetch -> fetch_grep), building on the iter-7 positioning art_IlzAiXYWeUYH
  (gated-steering prior art CAST/GSS/GUARD-IT/SADI all SUPERVISED; localization-first reposition; method-identity reframe;
  locked venues) and iter-6 art_3zaa2xXEp8Az (safety/u_sub label-efficiency positioning) so settled entries are NOT redone.
  (1) CHANIN-DELTA + MAX-PRECISION block: re-read Chanin 2409.14507 (the form-free diagnostic = probe-projection / absorption_fraction)
  and articulate the precise LABEL-FREE delta; search for 'precision/selectivity-ranked SAE latent selection', 'single most-precise
  latent steering', max-precision / precision-weighted selector baselines, to position the set-cover-vs-max-precision question
  and supply the trim wording grounded in whatever the experiments return. (2) CONCENTRATION-as-sharp-gate block: survey conditional/gated-steering
  surgicality vs feature precision/sparsity (extend the already-locked CAST/GSS/GUARD-IT/SADI prior art) and any work on 'sparse
  precise features as cleaner edit handles' / per-feature selectivity-vs-collateral, to ground the concentration mechanism
  reframe. (3) RETARGET/VENUE block: confirm ICML-primary / ICLR-fallback fit for an auditable-localization+editing-of-absorption
  framing aligned to the reviewer-evaluable areas (clustering, feature selection, knowledge graphs, knowledge extraction,
  classification, applied knowledge discovery), and draft the retargeted abstract + intro spine for BOTH the wins-landed and
  base-thin outcomes. (4) CITATION FINALIZATION: carry forward every locked venue (Chanin NeurIPS-2025; AxBench/SAEBench ICML-2025;
  CanonicalUnits ICLR-2025; Farrell NeurIPS-2024 WS; CAST ICLR-2025 Spotlight / GSS / GUARD-IT / SADI; Peng 'Discover-not-Act'
  2506.23845; SPLINCE/Karvonen-Marks NeurIPS-2025), add concentration/precision-steering cites with verified IDs/venues/full
  author lists, flag unresolved (do not invent). Emit research_out.json {answer, sources, follow_up_questions} + research_report.md
  with: the Chanin-and-max-precision delta paragraph, the concentration-as-sharp-gate positioning, BOTH retargeted abstract/intro
  spines, the locked citation table + BibTeX for new cites, and a presentation-strip checklist (lead with localization/editing
  of homograph-polysemy absorption; lead the edit table with KG-vs-strongest-dense and caveat the footprint-gated number;
  report both forget instruments; unify the gate operator; present set-cover as motivation; safety null as headline limitation;
  strip iteration/rebuttal/infra scaffolding).
depends_on:
- id: art_IlzAiXYWeUYH
  label: prior-positioning
  relation_type:
  relation_rationale:
- id: art_3zaa2xXEp8Az
  label: prior-positioning
  relation_type:
  relation_rationale:
</artifact_direction>

<dependencies>
Completed artifacts this artifact can use during execution.

--- Dependency 1 ---
id: art_3zaa2xXEp8Az
type: research
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
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
out_dependency_files:
  file_list:
  - research_out.json

--- Dependency 2 ---
id: art_IlzAiXYWeUYH
type: research
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
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_7/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
out_dependency_files:
  file_list:
  - research_out.json
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

RESEARCH executor scope:
  Output: research_out.json with {answer, sources, follow_up_questions} + research_report.md
  DOES: Web research — search, read, synthesize information from papers/docs/APIs into a structured report
  DOES NOT: Run code, download files, execute scripts, compute anything — no shell/Python access
  Use for literature surveys, API documentation, technical specifications — pure information gathering
</artifact_executor_scope>

<artifact_planning_rules>
RESEARCH: Plan early — findings guide dataset selection, experiment design, and methodology.
</artifact_planning_rules>

<compute_profiles>
Choose the compute profile this artifact needs for execution.
Available profiles for research artifacts:
  - cpu_light: 4 vCPUs, 16GB RAM — proofs, research, lightweight tasks (fallback: memory-optimized CPUs first (cpu3m → cpu5m), then GPU hosts last-ditch)

Set runpod_compute_profile to one of these exact tier names.
</compute_profiles>
GOOD PLANS: specific, actionable, consider failure scenarios, build on the suggested approach.
BAD PLANS: vague hand-waving, ignoring the suggested approach, missing critical executor details.
</instructions><user_data>
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
  "description": "Plan for a RESEARCH artifact.",
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
    "question": {
      "default": "",
      "description": "The specific research question to investigate",
      "title": "Question",
      "type": "string"
    },
    "research_plan": {
      "description": "Step-by-step plan for web research to gather this research",
      "title": "Research Plan",
      "type": "string"
    },
    "explanation": {
      "description": "Why this research matters and what question it answers",
      "title": "Explanation",
      "type": "string"
    }
  },
  "required": [
    "title",
    "research_plan",
    "explanation"
  ],
  "title": "ResearchPlan",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-06-18 10:39:56 UTC

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
