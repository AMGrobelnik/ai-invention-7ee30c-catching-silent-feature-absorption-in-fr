# gen_plan_research_1 — test_idea

> Phase: `invention_loop` · round 9 · `gen_plan`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_plan_research_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 22:14:59 UTC

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
  Training-Free, Label-Free LOCALIZATION (Not Clustering, Not an Edit-Quality Advantage) of Homograph-Polysemy SAE Absorption:
  The Genuinely-Fair d_sub-Gated Dense Control CLOSED the Edit Gap and the Concentrated-Win Base Stayed Thin (0/8) -- Commit
  the Reposition to Single-Specialist Localization + a Label-Free Homograph-Confinement SCREEN, and DEMONSTRATE the Where-to-Gate
  Value with a Label-Scarce Experiment or Drop the Thesis
hypothesis: |-
  ITERATION-8 STATUS -- THE TWO ITER-7 LOAD-BEARING GATES (a genuinely-fair bounded-beta d_sub-gated dense control + an expanded concentrated positive base) WERE BOTH EXECUTED AND BOTH RETURNED NEGATIVE, LANDING EXACTLY ON THE PRE-REGISTERED FORK (b): the sparse-SAE edit is NOT an SAE-specific advantage over a fair conditional-dense baseline, and the concentrated positive base does NOT broaden. The honest contribution has therefore narrowed to (i) auditable, label-free, regime-targeted LOCALIZATION of homograph-polysemy absorption + (ii) the homograph-confinement BOUNDARY as a deliberate scientific finding with a practitioner-facing screen + (iii) a label-free WHERE-TO-GATE discovery whose VALUE OVER THE LABELED ALTERNATIVE IS STILL UNDEMONSTRATED. Iteration 8 delivered: the de-inflated fair-gated edit test [art_Qdoz9eH0AGjh]; a base-widener + concentration-vs-absorption population test [art_bPU1evbgN0og]; a $0 integrity-lock eval [art_Mlx5GfSusrjm]; and a localization-retarget positioning audit [art_JCYCmzJDvUm5]. What landed:

            - M1''' FAIR-GATED EDIT EXECUTED [art_Qdoz9eH0AGjh], 8 cases, $1.07, 2 judges. overall = DISCOVERY_IS_THE_VALUE_FAIR_GATE_CLOSES_GAP. Fork tally: KG_BEATS_STRONGEST_AND_FAIR_GATED = 0; FAIR_GATED_CLOSES_GAP = 5 (large/Amazon/Bush/Georgia/insult); NO_MEANINGFUL_FORGET = 3 (Cook/Jordan/US); n_concentrated_wins = 0. The NEW genuinely-fair control DENSE-SUB-ABL-GATED-FAIR (erase u_sub ONLY where a precise logistic d_sub detector fires, bounded beta<=1, ONE unified operator across all cases, gate balanced-acc 0.96-1.00) MATCHES the discovered absorber on EVERY case (adv_KGvsFAIR ~ 0.0, CI incl 0) and is even CLEANER on retain collateral (fair ~3e-6 vs KG ~5e-5). KG-ABL still beats the STRONGEST UNGATED dense (+0.97 large, +0.87 Amazon, +0.48 Georgia, both judges CI excl 0, curve-dominance 1.0) -- but that is a win over an UNCONDITIONAL projection, not over the fair CONDITIONAL control, so it does NOT establish an SAE-specific edit advantage. The M3''' MAX-PRECISION ablation is decisive: the anchored set-cover DISCOVERY is INERT for the edit (0/8 cases it adds value over simply picking the single most precise latent on the target sub-context; 3/8 it returns the SAME latent). CONCENTRATION/precision -- not the absorption diagnostic -- predicts forgetting: a concentrated co-firing latent (insult, firing-Jaccard 0.882, no recall hole) forgets, while distributed country senses (Jordan/US, and Cook) do NOT meaningfully forget despite clean firing signatures (kg_can_forget=False).

            - M2'''/M3'''/M5''' BASE-WIDENER EXECUTED [art_bPU1evbgN0og]: verdict BASE_STAYS_THIN. Targeting >=4 INDEPENDENT concentrated wins under the FAIR control found ZERO -- large + Amazon do not survive as fair-control WINS (the fair gate matches), and Bush/Cook do not meaningfully forget. A $0 concentration screen over ~100 candidates confirmed the intended separation (spelling word-absorbers concentrate high: law 0.745, level 0.739, list 0.714; distributed country senses low: Georgia 0.113, Jordan 0.046) and a high set_cover_inertness_rate (anchored absorber == unconstrained max-precision latent for most candidates). So the positive edit base does NOT broaden under a fair control; the OUTCOME-B (base-thin) retarget is the correct one.

            - INTEGRITY-LOCK EVAL [art_Mlx5GfSusrjm], 44/44 cross-checks. De-inflates the headline: the defensible lead is KG vs the STRONGEST ungated dense = +1.00 CI[0.79,1.21] on large; the iter-7 +1.58 was a comparison against a footprint-matched gate handicapped to beta~2.97 over-erasure (gated collateral 0.290 = 13.8x its own ungated 0.021). Both forget instruments DISAGREE IN SIGN at the next-token-KL-matched point on large (completion -1.01 favors gated, sub-probe +0.42 favors KG) => KL-matching != behavioral matching, and the load-bearing 'large' completion CI is over only n=4 probes (thin). CONCENTRATION (precision x single-latent leverage, v2) tracks the win at point-biserial r=+0.63 where the absorption LABEL does NOT (r=-0.09) and inverse-footprint ANTI-correlates (r=-0.80, because distributed senses also fire sparsely). The iter-6 Georgia +0.561 'win' is RETRACTED as near-NOOP (max single-latent forget KL 0.065, NOOP-identical 0.889, sub-probe drop 0.075, completion CI incl 0). Operator-divergence flagged (D1 ~3%-global-footprint gate vs D2 ~95%-X-positive-rate clamp -- the two gates are NOT the same operator).

            - POSITIONING [art_JCYCmzJDvUm5]: OUTCOME-B selected; localization+editing retarget; Chanin label-free delta sharpened; concentration-gate grounded in the feature-selection-for-steering literature; safety-homograph null (2/44) framed as the headline limitation.

            WHAT THE ITER-8 REVIEW EXPOSED -- THREE MAJORS THAT GATE PUBLICATION, PLUS THREE MINORS. The blunt finding: AS WRITTEN THE PAPER HAS NO DEMONSTRATED LOAD-BEARING POSITIVE -- the clustering hypothesis (the core prompt) was tested and did not pay off, and the only surviving positive thesis ('discovery is the value') has no supporting experiment.
              (R1, CONTRIBUTION -- #1 blocker) GOAL-CONTRIBUTION MISMATCH. The goal asks for a CLUSTERING method producing group-level UNITS that beat single latents on three named downstream tasks. The paper instead shows (a) the clustering/multi-member machinery is INERT -- effectively k=1 single-absorber selection, multi-member only ADDS collateral; (b) ALL THREE goal-named downstream tasks are NULLS (no SAE unit out-classifies a dense probe; steering surgical on 2/5 letters; model-diffing +0.000 confound-bounded null); (c) the MAX-PRECISION ablation shows set-cover adds value in 0/8 edit cases. The surviving positive is a narrow label-free re-implementation of Chanin's absorption diagnostic + an auditable KG = below the ICLR/ICML primary bar. => ITER-9 MUST PICK ONE AND COMMIT: (1) deliver a DEMONSTRATED positive (the label-scarce experiment, R2), OR (2) explicitly REPOSITION away from 'clustering' to 'label-free single-specialist LOCALIZATION', state in the intro that the clustering hypothesis was tested and did NOT pay off, and make the HOMOGRAPH-CONFINEMENT boundary the DELIBERATE HEADLINE with a clear 'why this matters'. RECOMMENDED: attempt (1) AND commit to (2) as the standing frame, so the paper is coherent whichever way the experiment lands.
              (R2, EVIDENCE -- #2 blocker) THE LOAD-BEARING POSITIVE THESIS HAS NO SUPPORTING EXPERIMENT. The paper concedes the edit is matched by the fair d_sub-gated dense control and that gating is prior art, then retreats to 'the SAE-specific value is label-free discovery of WHERE to gate' -- but NOWHERE demonstrates that this label-free discovery yields any BENEFIT over the labeled alternative. The fair gate needs d_sub TRAINED on sub-context labels; the paper never quantifies the labeling cost saved nor identifies a regime where the label-free route wins. => ITER-9 MUST RUN THE LABEL-SCARCE DEMONSTRATION (NEW LOAD-BEARING #1): vary the number of sub-context labels available to fit d_sub (n in {0,1,5,20,full}); at each n compare the FAIR d_sub-gated dense gate vs the LABEL-FREE SAE absorber discovery (KG-ABL gated by the absorber's own JumpReLU firing -- a calibration-free, ZERO-sub-context-label gate) on BOTH edit quality (joint fluency x content at matched meaningful forget) AND localization quality (recall-hole recovery / gate balanced-accuracy). If the SAE discovery HOLDS quality where d_sub COLLAPSES at low label counts (CI separation), that is the concrete demonstrated 'discovery is the value' result. If the fair gate matches even at n=1, the where-to-gate thesis is NOT supported and the paper retargets FULLY to localization + the homograph-confinement screen.
              (R3, SCOPE -- #3 blocker) SIGNIFICANCE LIMITED BY HOMOGRAPH-CONFINEMENT, with no 'why others build on it'. Confined to lexically-polysemous tokens (2/44 safety groups, 3/64 homograph entities, 0/28 professions). => ITER-9 MUST EITHER BROADEN THE EMPIRICAL BASE (systematically MINE a large entity/word vocabulary for additional suppressed-parent homographs via the $0 label-free recall-hole + firing-disjoint screen, VALIDATE a sample with the form-free oracle, and report a COVERAGE number = how many of N candidate polysemous tokens are absorption-structured), OR FRAME THE CONFINEMENT AS THE DELIBERATE SCIENTIFIC CONTRIBUTION with explicit downstream consequences ('SAE absorption-reliability is a LEXICAL-POLYSEMY phenomenon, so practitioners auditing safety attributes need not fear absorption there; here is the LABEL-FREE SCREEN to verify it on any frozen SAE'). RECOMMENDED: do BOTH -- the mining gives a coverage result, the screen gives the practitioner takeaway and the 'so what' for the discussion.
              (R4, CLARITY -- minor) Section 5 advertises a median 1262x-selective surgical edit computed vs WHOLE-PARENT dense (DENSE-WHOLE-ABL), a baseline Section 6 disowns, while the FAIR gated dense control is equally/MORE surgical (collateral 2.8e-6 vs KG 5.1e-5). => ITER-9 MUST present 1262x strictly as a LOCALIZATION claim (the KG-named latent's edit IS localized), NOT an SAE-specific surgical advantage, with a one-line cross-reference that against the fair gated control the surgical advantage disappears; drop the whole-parent strawman from the surgical-advantage rhetoric.
              (R5, RIGOR -- minor) The recall-repair headline (22 distinct holes, 30 FDR survivors, vs a random single-latent control) rests on a NEAR-DEFINITIONAL comparison (the absorber is SELECTED by held-out per-sub-context precision for covering hole H, then EVALUATED on recovering recall on H; the single-random-latent control is weak) -- it certifies naming SELF-CONSISTENCY more than repair UTILITY. => ITER-9 MUST add a STRONGER control (best latent by an alternative label-free signal NOT aligned with the eval metric, or the dense-probe argmax which is always the parent) AND show the repaired unit buys a downstream capability parent-alone-plus-dense-probe cannot -- OR state the repair demonstrates correct LOCALIZATION rather than utility and TEMPER 'measured repair utility'.
              (R6, PRESENTATION -- minor) The paper reads as an iteration/rebuttal log ('A prior version of this work claimed...', a dense alphabet M1'''/S-rec/S-prec/S-mag/KG-ABL/DENSE-SUB-ABL-GATED-FAIR/MAX-PRECISION). => ITER-9 MUST present the corrected results AS the results, move the self-correction to a brief changelog/limitations note, FIX ONE STABLE NAME for the central object, define gate operators ONCE in a compact table, relegate the selector zoo + M-labels to the appendix, and lead each section with its single takeaway sentence.

            THE ITERATION-9 MANDATE (the label-scarce demonstration is the single make-or-break new piece; the reposition + confinement-as-contribution are required; the minors are cleanup):
              (M1'''' = NEW LOAD-BEARING -- THE LABEL-SCARCE WHERE-TO-GATE DEMONSTRATION, the only path to a demonstrated SAE-specific positive). Vary the sub-context labels available to fit d_sub (n in {0,1,5,20,full}). At each n, compare the FAIR d_sub-gated dense gate (labeled, supervised) vs the LABEL-FREE SAE absorber discovery (anchored recall-hole-guided precision selection; KG-ABL via the absorber's own sparse firing; ZERO sub-context labels) on BOTH (i) edit quality (joint fluency x content at matched meaningful forget, two judges, paired bootstrap) AND (ii) localization quality (recall-hole recovery and/or gate balanced-accuracy). Report quality-vs-#labels curves with CIs. FORK: (a) the SAE discovery HOLDS quality where the fair gate COLLAPSES for lack of labels (CI separation at low n) => DEMONSTRATED 'discovery is the value' = the concrete positive the paper needs; (b) the fair gate matches even at n=1 => the where-to-gate thesis is NOT supported; retarget FULLY to localization + the homograph-confinement screen as the deliberate contribution (honest negative, publishable as a boundary paper).
              (M2'''' = COMMIT THE REPOSITION, R1). Drop the 'clustering' framing as the headline. The central object is LABEL-FREE SINGLE-SPECIALIST LOCALIZATION = anchored recall-hole-guided PRECISION SELECTION of one absorber latent that marginal attribution drops. State up front that the multi-member CLUSTERING hypothesis (the core prompt) was TESTED and did NOT pay off -- the machinery is inert vs a max-precision selector (0/8 edit cases), multi-member units add collateral, and all three goal-named downstream tasks (safety classification / steering / model-diffing) are nulls -- and report that null as a finding. Make the HOMOGRAPH-CONFINEMENT BOUNDARY the deliberate headline scientific finding.
              (M3'''' = CONFINEMENT AS A COVERAGE RESULT + A PRACTITIONER SCREEN, R3). Systematically mine a LARGE entity/word vocabulary (wider city/given-name/brand/named-entity + first-letter spelling) for suppressed-parent homographs using the $0 label-free recall-hole + firing-disjoint + precision screen; validate a stratified sample with the non-circular form-free oracle; report COVERAGE (fraction of N candidate polysemous tokens that are absorption-structured) with CIs, and ship the screen as the practitioner deliverable ('verify absorption-confinement on any frozen SAE, label-free, no diagnostic probe').
              (M4'''' = RECONCILE SELECTIVITY, R4). Present 1262x as LOCALIZATION evidence only; cross-reference that the fair gated dense control is equally/more surgical; drop the whole-parent strawman.
              (M5'''' = STRENGTHEN OR TEMPER THE REPAIR, R5). Add a non-eval-aligned label-free control + a downstream-capability test for the repaired unit; if neither pays, state 'repair demonstrates correct localization, not utility' and temper 'measured repair utility'.
              (M6'''' = PRESENTATION + CARRIED INTEGRITY, R6). One stable name; gate operators in a compact table; selector zoo + M-labels to appendix; self-correction history -> brief changelog. CARRY the settled spine (22 distinct holes / 30 FDR survivors; corrected selectivity 16k mean 1452x median 1262x / 65k mean 722x median 676x; cross-dictionary 65k FULL / layer-9 PARTIAL) [art_sxwT7hK6YFEA, art_w7p8du2N1f0Y, art_4L1MZxvWYlGd]; the settled safety null (2/44, both homographs; named-entity 3/5 confirmatory) [art_yAQgbq5Wgymx, art_ZxVw0e4seBq3]; router DEMOTED (homograph prospective Wilson includes 0.5) [art_F_-HUhl0NR_i]; member-labeling above shuffle null (0.730 vs 0.096); 0/28 professions [art_Iy77UHoNaIhS]; numeric below-gate; model-diffing confound-bounded +0.000 null. Strip iteration/rebuttal scaffolding.

            RE-DESIGNATED HEADLINE (localization + screening first; the edit advantage is REAL only vs an unconditional dense projection, NOT vs a fair conditional control). On a FROZEN public SAE, interventional anchored recall-hole-guided PRECISION SELECTION is a TRAINING-FREE, LABEL-FREE DISCOVERY PROCEDURE that surfaces the single PRECISE sub-context latent a marginal-attribution ranking silently drops -- in the absorption regime this IS the absorber -- plus a feature-level KNOWLEDGE GRAPH whose edges carry MEASURED, localized repair (a KG-named absorber added to a suppressed parent recovers its recall hole over a random single-latent control; 22 distinct holes survive FDR across spelling/taxonomic/numeric; replicates on a 4x-wider SAE with MORE absorption). The CLUSTERING hypothesis was tested and did NOT pay off: multi-member grouping is INERT vs a max-precision selector (0/8 edit cases), adds collateral, and ties weak baselines for classification. The EDIT capability is REAL only relative to an UNCONDITIONAL dense projection (KG beats the strongest ungated dense by +1.00 on large, +0.87 on Amazon); a GENUINELY-FAIR bounded-beta d_sub-gated CONDITIONAL dense control CLOSES THE GAP on every case (0/8 KG-beats-both) and is even cleaner on collateral, so the edit is NOT an SAE-specific advantage. Gating is ESTABLISHED PRIOR ART (CAST/GSS/GUARD-IT/SADI, all SUPERVISED), so the SAE-specific value -- IF any survives -- is the LABEL-FREE DISCOVERY of WHERE to gate, whose benefit over the LABELED route iteration 9 must DEMONSTRATE in the label-scarce regime or DROP. The win predictor is lexical CONCENTRATION/PRECISION (insult, a co-firing latent, also forgets; Georgia/Jordan, absorbers, do NOT), of which absorption is ONE label-free-discoverable source. SAFETY-relevant absorption does NOT exist beyond homographs (2/44, both homographs -- the SETTLED ceiling and the deliberate headline boundary); absorption is a LEXICAL-POLYSEMY phenomenon (homograph entity tokens + first-letter spelling; 3/5 named-entity homographs; 0/28 professions; 3/64 homograph entities). The DURABLE VALUE is AUDITABLE, LABEL-FREE-DISCOVERED, REGIME-TARGETED LOCALIZATION + a LABEL-FREE SCREEN that tells a practitioner where absorption can and cannot occur on a frozen SAE.

            PRIMARY ENDPOINT (re-designated; the label-scarce demonstration is the only NEW load-bearing positive).
              (a) LABEL-SCARCE WHERE-TO-GATE DEMONSTRATION (NEW LOAD-BEARING, M1''''): quality-vs-#labels curves for the FAIR d_sub-gated dense gate vs the LABEL-FREE SAE absorber discovery, on edit AND localization quality, with CIs. A CI separation where the SAE handle holds and the fair gate collapses at low n = the demonstrated SAE-specific positive; a match at n=1 = the thesis is dropped and the paper is a localization + screening boundary paper.
              (b) CONFINEMENT COVERAGE + PRACTITIONER SCREEN (NEW LOAD-BEARING, M3''''): a coverage number over a wide mined vocabulary + the shipped label-free screen with the explicit 'so what'.
              (c) AUDITABILITY/LOCALIZATION SPINE (ACHIEVED, to be re-controlled per R5): 22 distinct-hole FDR repairs [art_sxwT7hK6YFEA, art_w7p8du2N1f0Y]; KG-named edits LOCALIZED (selectivity presented as localization, not surgical advantage); member-labeling above null; cross-dictionary 65k full / layer-9 partial [art_4L1MZxvWYlGd].
              (d) SAFETY SCOPE (SETTLED NULL, deliberate headline boundary): homograph-confined (2/44; named-entity 3/5) [art_yAQgbq5Wgymx, art_ZxVw0e4seBq3].
              (e) ROUTER: recall-hole-alone reproduces on derivation (bal-acc 1.0) but is OUT-OF-SAMPLE-UNVALIDATED (homograph prospective Wilson includes 0.5) -- DEMOTED to exploratory diagnostic [art_F_-HUhl0NR_i].
            SUPPORTING (strengthen, do not gate): within-SAE precision/set-cover selection where the signature holds (Georgia, first-letter I,D); the steering demo (L,D); the homograph breadth count (months March/June/February). The headline NO LONGER depends on classification beating dense, on multi-member grouping beating single absorbers, on the router being validated, on a safety win existing, on the +1.58-vs-footprint-gated number, OR on the edit beating a fair conditional dense control.

            THE DISCOVERY ALGORITHM (framed as LABEL-FREE SINGLE-SPECIALIST LOCALIZATION; clustering DEMOTED to a tested-and-negative secondary). STEP 1 cover-based eligibility (content-responsive above a shuffle null; firing-precision>=0.7; covers>=1 sub-context). STEP 2 ANCHOR = argmax cover-set chosen WITHOUT the diagnostic, with the UNSUPERVISED FIRING-FLOOR PARENT-VALIDATION (anchor must fire on held-out corpus above ~5%). STEP 3 HOLE = parent's uncovered pairs (names the under-served sub-context, label-free). STEP 4 PRECISION-SELECT the single absorber covering the hole (held-out per-sub-context precision>=0.7, firing-Jaccard<0.1, marginal-gain>=0.05 CI excl 0; Georgia selects 16009 prec .955 not 4697 prec .35). Set-cover/(1-1/e) is MOTIVATION only (effectively k=1 for every win; INERT vs max-precision for the edit -- the value over max-precision is the recall-hole ANCHORING that names WHICH sub-context to gate). C-TRACK correlation-community splitting + multi-member units: TESTED AND NEGATIVE (ties weak baselines, adds edit collateral) -> reported as the clustering-hypothesis null, NOT a contribution.

            BASELINE GLOSSARY (decisive M1'''' comparators are the FAIR d_sub-gated dense gate at varying label budgets vs the LABEL-FREE SAE absorber handle). DECISIVE EDIT COMPARATORS: KG-ABL (discovered absorber, sparse-firing-gated, ZERO sub-context labels); DENSE-SUB-ABL (strongest UNGATED dense, the LEAD reference, NOT the fair control); DENSE-SUB-ABL-GATED-FAIR (precise d_sub gate, bounded beta<=1 -- the load-bearing fair control, which CLOSED the gap and is now studied vs label budget); DENSE-SUB-ABL-GATED footprint-gated (iter-7, DEMOTED, beta~3 over-erasure, robustness caveat only); MAX-PRECISION single latent (ablation: does discovery beat picking the most precise latent -- answer NO for the edit); DENSE-WHOLE-ABL (whole-parent over-shoot reference). Classification baselines (a)-(k) carried as supporting/within-SAE.

            NON-SPELLING / HOMOGRAPH TESTBED (CONCENTRATED-vs-DISTRIBUTED is the edit-relevant axis; ABSORPTION-STRUCTURED-vs-CO-FIRING is the screen axis). Absorption recurs on HOMOGRAPH/POLYSEMOUS tokens whose general parent is suppressed -- taxonomic Georgia/Jordan; United States CO-FIRING; 0/28 professions; of 64 homograph entities only 3 months; of 5 named-entity homographs 3 structured (Amazon/Bush/Cook); of 44 safety groups only 2 homographs (white, straight). A structured absorber is an EDITABLE handle only if its targeted sense is LEXICALLY CONCENTRATED (spelling 'large', entity 'Amazon' forget; DISTRIBUTED country senses Georgia/Jordan and even structured Bush/Cook do NOT). A non-SAE dense probe matches/beats the unit on ALL classification.

            SCOPE AND VALUE PROPOSITION. The defensible contribution is: (1) a TRAINING-FREE, LABEL-FREE single-specialist LOCALIZATION procedure that surfaces the precise absorber marginal attribution drops, with a MEASURED, auditable feature-KG (recall-hole recovery over a random single-latent control -- to be re-controlled per R5 as localization vs utility), REPLICATING across SAE dictionaries; (2) a LEXICAL-POLYSEMY CONFINEMENT finding + a label-free SCREEN practitioners can run on any frozen SAE to verify where absorption can/cannot occur (the deliberate headline boundary; safety attributes are predominantly co-firing); (3) a label-free WHERE-TO-GATE discovery whose value over the labeled route iteration 9 must DEMONSTRATE in the label-scarce regime or DROP. The method does NOT out-classify a strong dense probe, does NOT beat a fair conditional dense control on the edit, and the clustering machinery is INERT. HEADLINE = auditable, label-free-discovered, regime-targeted LOCALIZATION of homograph-polysemy absorption + the confinement screen; the edit is a SCOPED capability, not an advantage.

            HONEST NEGATIVES (each publishable): the genuinely-fair bounded-beta d_sub-gated dense control CLOSES the edit gap on every case (0/8 KG-beats-both) and is cleaner on collateral, so there is NO SAE-specific edit advantage; the concentrated positive base does NOT broaden under the fair control (0 independent wins); the set-cover discovery is INERT vs a max-precision selector for the edit (0/8); the clustering/multi-member hypothesis (the core prompt) did NOT pay off (inert, adds collateral, ties weak baselines); the edit-win predictor is CONCENTRATION not absorption (insult co-fires yet forgets; Georgia/Jordan absorb yet lose); iter-6's Georgia +0.561 win RETRACTED as near-NOOP; the +1.58-vs-gated headline was inflated (footprint gate driven to beta~3 over-erasure); the two iter-7 gated controls were DIFFERENT operators; the meaningful-forget proof was thin (n=4 probes, instruments disagree at the KL-matched point); gating is established prior art; the unit out-classifies NO non-SAE dense probe on any task; all three goal-named downstream tasks (safety classification, steering, model-diffing) are NULLS; safety absorption is homograph-confined (2/44); 0/28 professions; 3/64 homograph entities; the router is at chance out-of-sample; cross-dictionary replicates at 4x width but only PARTIALLY across a layer; the 65k 3.7e6 selectivity was a divide-by-epsilon artifact; numeric is below-gate. A clean iter-9 result where the FAIR gate matches the SAE handle EVEN AT n=1 labels = 'there is no SAE-specific where-to-gate value' and the paper becomes a localization + confinement-screen boundary paper -- itself publishable.

            MOTIVATION (substance unchanged). Single SAE latents are unreliable units: absorption (Chanin 2409.14507), splitting, hedging (2505.11756), 'SAEs Do Not Find Canonical Units' (ICLR 2025) converge on no single latent reliably tracking a concept; AxBench (ICML 2025) and DeepMind's negative report show diff-of-means beats raw-latent SAE methods, and Farrell (2410.19278) shows multi-feature SAE unlearning has side-effects >= RMU -- so any SAE method must clear strong dense baselines AND, for the edit, BOTH the strongest ungated dense AND a fair CONDITIONAL gated dense direction (which it does NOT). Absorption is the regime where OBSERVATIONAL signals break by construction and MARGINAL-ATTRIBUTION selection silently drops the absorber; anchored recall-hole-guided precision selection recovers it LABEL-FREE -- the durable localization deliverable. The EDIT advantage is about a PRECISE/CONCENTRATED latent acting as a sharp conditional gate -- but a fair LABELED conditional gate matches it, so the only SAE-specific value left is whether the label-free route SAVES the labeling cost (the iter-9 demonstration). The method positions against 'use SAEs to DISCOVER, not to ACT' (Peng 2506.23845): CCRG discovers the sub-context handle; ACTING through it is no better than a fair labeled dense gate; whether DISCOVERING it label-free beats the labeled route is the load-bearing open question.

            SUCCESS CRITERIA. CONTRIBUTION CONFIRMED iff: (LOAD-BEARING) (M1'''') the label-scarce demonstration shows the LABEL-FREE SAE handle HOLDS edit/localization quality where the FAIR d_sub-gated dense gate COLLAPSES at low label budgets (CI separation), establishing a concrete where-to-gate value; AND (M3'''') the confinement is turned into a coverage result + a shipped label-free practitioner screen; AND the auditability/localization spine holds (22 distinct holes over a STRENGTHENED control or honestly tempered to localization-not-utility; cross-dictionary 65k full / layer-9 partial); AND the safety null + clustering-did-not-pay-off null are reported as deliberate findings. SUPPORTING (strengthen, do not gate): within-SAE precision selection (Georgia, I, D); member-labeling above null; the recall-hole router on derivation; the steering demo (L,D); the homograph breadth count. HONEST NEGATIVES are reportable and cap-but-do-not-sink: the fair gate matching the SAE handle even at n=1 (=> contribution is localization + confinement screen, no SAE-specific where-to-gate value), the edit not beating a fair conditional control (=> scoped capability), near-NOOP forget for distributed senses, safety absorption absent (settled), router-at-chance, layer-conditional replication, clustering inert, no classification win over dense on any task.
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
  Fair gate closed the edit gap, base stayed thin (0/8); reposition to localization+screening, add label-efficiency test.
_confidence_delta: decreased
_key_changes:
- >-
  Recorded iter-8 execution: the genuinely-fair bounded-beta d_sub-gated dense control CLOSES the edit gap on every case (KG_BEATS_BOTH=0/8,
  FAIR_CLOSES=5, NO_FORGET=3) and is cleaner on collateral -- landing exactly on the pre-registered fork (b): the edit is
  NOT an SAE-specific advantage [art_Qdoz9eH0AGjh].
- >-
  Recorded the base-widener NEGATIVE: 0 independent concentrated wins under the fair control (BASE_STAYS_THIN); concentration
  screen confirmed the concentrated-vs-distributed separation but the positive edit base does not broaden [art_bPU1evbgN0og].
- >-
  Recorded the MAX-PRECISION ablation: anchored set-cover discovery is INERT for the edit (0/8 cases adds value over picking
  the single most precise latent; 3/8 same latent) -- the clustering/discovery machinery does not pay off for editing.
- >-
  Locked the de-inflation/concentration/retraction (44/44 cross-checks): defensible lead +1.00 vs strongest ungated (not +1.58
  vs handicapped beta~3 footprint gate); concentration r=+0.63 vs absorption-label r=-0.09; Georgia +0.561 retracted as near-NOOP;
  instruments disagree at the KL-matched point [art_Mlx5GfSusrjm].
- >-
  Addressed reviewer MAJOR #1 (goal-contribution mismatch): committed the REPOSITION away from 'clustering' to label-free
  single-specialist LOCALIZATION, stating the clustering hypothesis was tested and did NOT pay off, and making homograph-confinement
  the deliberate headline.
- >-
  Addressed reviewer MAJOR #2 (no supporting experiment for the surviving positive): added the NEW LOAD-BEARING label-scarce
  demonstration (vary d_sub labels n=0/1/5/20/full; fair dense gate vs label-free SAE handle on edit + localization quality)
  as the make-or-break for the 'discovery is the value' thesis.
- >-
  Addressed reviewer MAJOR #3 (significance/scope): mandated turning homograph-confinement into a COVERAGE result (mine a
  wide vocabulary, validate a sample) AND a shipped label-free practitioner SCREEN with an explicit 'so what'.
- >-
  Addressed reviewer minors: reconcile the 1262x selectivity to a localization claim not an SAE-specific surgical advantage
  (R4); strengthen the recall-repair control or temper to localization-not-utility (R5); strip the iteration/rebuttal log,
  fix one stable name, compact operator table, selector zoo to appendix (R6).
- >-
  Confidence DECREASED: both iter-7-mandated load-bearing pieces returned negative (fair gate matches; base stays thin), the
  clustering machinery is inert, all three goal-named downstream tasks are nulls, and the only surviving positive thesis (label-free
  where-to-gate) is currently undemonstrated -- net contribution is below the primary bar until the label-scarce experiment
  lands.
relation_type: evolution
</hypothesis>

<artifact_direction>
Make this direction concrete and actionable. Keep the same type and respect dependencies.

id: research_iter9_dir5
type: research
objective: >-
  M2'''' COMMIT THE REPOSITION + M3'''' CONFINEMENT 'SO WHAT' + LABEL-EFFICIENCY FRAMING + M6'''' PRESENTATION -- finalize
  positioning for GEN_PAPER_TEXT so the paper is coherent whichever way M1'''' lands. (1) COMMIT THE REPOSITION (R1/M2''''):
  drop 'clustering' as the headline; the central object is LABEL-FREE SINGLE-SPECIALIST LOCALIZATION = anchored recall-hole-guided
  precision selection of one absorber. Draft the intro spine that states UP FRONT that the multi-member CLUSTERING hypothesis
  (the core prompt) was TESTED and did NOT pay off (inert vs a max-precision selector 0/8; multi-member adds collateral; all
  three goal-named downstream tasks -- safety classification / steering / model-diffing -- are nulls) and reports that null
  as a FINDING, and makes the HOMOGRAPH-CONFINEMENT boundary the deliberate headline scientific contribution. Supply 4-5 retitle
  options committing to localization + screening. (2) GROUND THE LABEL-EFFICIENCY RESULT (M1''''): survey the label-efficient
  / few-shot concept-probing, active-learning-for-probing, and 'discover-not-act' literature so the label-scarce demonstration
  is POSITIONED whichever fork it lands -- supply BOTH framings (FORK-A: the label-free SAE discovery SAVES the sub-context-labeling
  cost the fair dense gate needs, a concrete where-to-gate value; FORK-B: the fair gate matches even at n=1 => no SAE-specific
  where-to-gate value, a clean localization + confinement-screen boundary paper). (3) CONFINEMENT 'SO WHAT' (R3/M3''''): articulate
  why practitioners build on a LEXICAL-POLYSEMY confinement finding + a shipped label-free SCREEN (the SAE absorption-reliability
  concern is a lexical-polysemy phenomenon; safety attributes are predominantly co-firing; here is the screen to verify it
  on any frozen SAE), positioned against the SAE-reliability / safety-auditing literature. (4) LOCK CITES + PRESENTATION-STRIP
  CHECKLIST (M6''''): carry the venue-verified table verbatim, add label-efficiency / active-learning / few-shot-probing cites
  with verified IDs/venues/authors (flag unresolved, do NOT invent), and supply the presentation-strip checklist (one stable
  name; self-correction to changelog; selector zoo + M-labels to appendix; lead each section with its takeaway).
approach: >-
  Pure web research via aii-web-tools (search -> fetch -> fetch_grep), building on the iter-8 positioning (art_JCYCmzJDvUm5,
  formal dep: Chanin delta, concentration-gate, localization retarget, OUTCOME-A/B spines), the iter-7 positioning (art_IlzAiXYWeUYH,
  formal dep: gated-steering prior art CAST/GSS/GUARD-IT/SADI all SUPERVISED; localization-first reposition; locked venues),
  and the iter-6 label-efficiency positioning (art_3zaa2xXEp8Az, formal dep: u_sub label-efficiency; Peng 'discover-not-act'
  2506.23845) so settled entries are NOT redone. (1) REPOSITION block: write the intro spine + abstract committing to label-free
  single-specialist localization with the clustering-tested-and-negative null stated up front and homograph-confinement as
  the deliberate headline; supply retitle options. (2) LABEL-EFFICIENCY block: search 'label-efficient concept probing', 'few-shot
  linear probe / diff-of-means sample complexity', 'active learning for concept detectors', 'label cost of conditional steering/gating',
  and label-free vs labeled steering comparisons, to ground BOTH forks of the M1'''' result; relate to the established gated-steering
  prior art (all supervised) so the SAE label-free route is the explicit delta IF FORK-A lands, and to the boundary framing
  IF FORK-B lands. (3) CONFINEMENT-SO-WHAT block: position the lexical-polysemy confinement + label-free screen against SAE-reliability/auditing
  (Chanin absorption, SAEBench, 'SAEs do not find canonical units') and safety-attribute auditing, articulating the practitioner
  takeaway. (4) CITATION FINALIZATION: carry every locked venue forward verbatim; add label-efficiency/active-learning/few-shot-probing
  cites with verified IDs/venues/full author lists; flag unresolved; supply BibTeX for new cites and the 10-14 item presentation-strip
  checklist. Emit research_out.json {answer, sources, follow_up_questions} + research_report.md with: the committed reposition
  intro/abstract spine, the BOTH-FORKS label-efficiency positioning, the confinement 'so what' paragraph + screen framing,
  the retitle options, the locked citation table + new-cite BibTeX, and the presentation-strip checklist.
depends_on:
- id: art_JCYCmzJDvUm5
  label: prior-positioning
  relation_type:
  relation_rationale:
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

--- Dependency 3 ---
id: art_JCYCmzJDvUm5
type: research
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

### [2] HUMAN-USER prompt · 2026-06-18 22:14:59 UTC

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
