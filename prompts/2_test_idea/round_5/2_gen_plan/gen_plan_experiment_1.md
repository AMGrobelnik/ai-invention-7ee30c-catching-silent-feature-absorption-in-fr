# gen_plan_experiment_1 — test_idea

> Phase: `invention_loop` · round 5 · `gen_plan`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_plan_experiment_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 01:55:36 UTC

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
You are expanding an artifact direction of type: EXPERIMENT

EXPERIMENT
Run code to test hypotheses, implement methods, and collect empirical results.
Runtime: Python 3.12, UV (any pip package), isolated workspace, gradual scaling (mini → full data).
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Implement and run any code-based experiment, compare method vs baselines.
Deps: REQUIRED at least one DATASET | OPTIONAL RESEARCH for methodology guidance
</artifact_type_info>

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

<time_budget>

The experiment executor has 6h total (including writing code, debugging, testing, and fixing errors).

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
  Auditable, Training-Free Repair of the SAE Absorption Regime: Two-Track Co-Response Grouping with a Measured KG Repair-and-Surgical-Edit
  Loop and a Recall-Hole Router — Now Gated on Beating a Dense Baseline on a Downstream Outcome and Replicating Across SAE
  Dictionaries
hypothesis: |-
  ITERATION-4 STATUS -- THE AUDITABILITY SPINE EXECUTED AND EXPANDED, THE INTEGRITY FIXES LANDED, BUT THE SIGNIFICANCE CEILING IS UNMOVED AND A CROSS-DICTIONARY GAP OPENED. Iteration 4 delivered the iter-3 mandate on the FROZEN Gemma-Scope L12/16k JumpReLU SAE: an expanded KG-repair + member-labeling spine [art_sxwT7hK6YFEA]; a KG-localized surgical sub-concept edit with side-effect measurement [art_0CZwPjG2YMCf]; a precision-gated taxonomic rebuild that fixed the unit/specialist conflation [art___vgSpUe6wAF]; a first-letter selection-isolation re-run with non-random selectors + a firing-floor anchor fix [art_JMA2gBvnakAm]; an a-priori router experiment [art_GTc_f26dMzFs]; and a citation/positioning audit [art_QBxBPF-9Ldxe]. What honestly landed, and what the iter-4 reviewer exposed:

    - MEASURED AUDITABILITY -- the load-bearing spine, now stronger but OVER-COUNTED in the draft [art_sxwT7hK6YFEA]. The KG-guided recall-repair loop yields 30 repair VARIANTS surviving Benjamini-Hochberg FDR<=0.05 over 69 tested, across THREE families (homograph-taxonomic 6, numeric 10 -- a NEW beyond-spelling generalization: date +0.68, ordinal +0.53, decimal +0.45, year +0.35, comma_number +0.24, currency +0.14 -- spelling 14). BUT (reviewer rigor MINOR) '30' over-counts DISTINCT holes: six sub-contexts (Georgia/Jordan/US/date/decimal/ordinal) are counted twice because their kg_ktrack and kg_diagnostic variants name the IDENTICAL latent, and at least one survivor (numeric 'percent') has is_hole=False (no hole to repair, gain +0.04). The honest distinct-hole count is ~23. Member-labeling: ensemble LLM judge agreement 0.730 vs shuffle null 0.096 (gap CI[0.545,0.724]; absorbers 0.756, anchors 0.43); 15-wide confident-label fraction L.87/O.80/T.93/I.87/D.67. Honest negatives emitted verbatim (numeric integer ties, first-letter O/on,out,over,own and T/this,think,time tie, letter-I anchor 1227 fires 0%). CONTROL WORDING (reviewer clarity MINOR): the implemented control is a RANDOM SINGLE content-responsive-latent addition (KG gain exceeds the 95th/99th pct of single-latent gains) -- NOT 'the full population of other content-responsive latents max-pooled' (which a union would drive recall->1.0 and the absorber would NOT beat). The actually-run single-latent control is the correct one; the prose must say so.

    - SURGICAL EDIT (M1b) -- the unique-capability downstream demo, BUT not yet a WIN over a baseline that MATTERS [art_0CZwPjG2YMCf]. Ablating a single KG-named absorber surgically edits exactly one sub-context: 5/7 cases SURGICAL_EDIT_CONFIRMED (Georgia->16009 1722x, Jordan->540 2722x & ->8347 3247x, US->846 214x, first-letter large->8463 802x); US->4760 is PARTIAL_SURGICAL (7.8x); toxicity insult->13367 is PARTIAL_CO_FIRING_AS_PREDICTED (2.4x, firing-Jaccard 0.878, footprint 0.117). LABELING FIX (reviewer evidence MINOR): the six absorption cases are {7.8, 213.5, 802, 1722.5, 2722.3, 3246.9} -> MEAN 1452.5, MEDIAN 1262.2; the draft's '1452x median' is the MEAN, and the n=6 average INCLUDES the partial-surgical US-4760 the text excludes from 'surgical'. State which cases are averaged; report the precise median (1262x) for the cleanly surgical set. SOFTEN 'absorber precision predicts surgicality': it is contradicted by 'large' (precision 0.571 -> 802x) vs US-4760 (precision 0.709 -> 7.8x); report the full precision-vs-selectivity relationship so the counterexample is visible, or scope to within-family.

    - TAXONOMIC CONFLATION FIXED, but the affirmative set-cover selection is effectively n=1 [art___vgSpUe6wAF]. The precision gate / precision-weighted coverage recovers the diagnostic-corroborated specialist Georgia 16009 (precision .968 sel / .955 held-out) and DROPS the low-precision 4697 (.35); rebuilt unit [3792,16009,540,846] reaches Georgia AUC 0.995 and beats EVERY label-free selector with CIs excluding 0 (S-rec +0.307, S-prec +0.416, S-mag +0.294, RE-k-anchored +0.082; g/h below chance = the absorption signature) => set_cover_established=True. HONEST: a non-SAE dense probe still edges it (1.000 vs 0.995, -0.005). REVIEWER evidence MINOR: only Georgia and Jordan satisfy the absorption signature (parent recall-hole>0.5 AND firing-Jaccard<0.1); Jordan is DESCRIPTIVE (n=124<150) and United States is co-firing/splitting (firing-Jaccard 0.20), so the non-spelling set-cover-selection HEADLINE rests on ONE eligible country (Georgia), 1-2 with descriptive Jordan -- thin for a headline. The form-free MAGNITUDE diagnostic is precision-blind (its top Georgia pick is the low-precision 1966; per-edge top-1 agreement with 16009 is 0), so corroboration rests on the PRECISION diagnostic + router recall-hole signal, reported separately (not a 3-edge mean).

    - FIRST-LETTER SELECTION ISOLATED HONESTLY [art_JMA2gBvnakAm]. Unit AUC L.905 O.917 T.858 I.983 D.956 beats (h) on all 5 and the firing-floor anchor validation RECOVERED letter I (its recall-argmax anchor 1227 fires 0%; the validated anchor 1634 fires 20.6% and IS the diagnostic parent), so E1 now holds 5/5. The SET-COVER-SPECIFIC win (unit beats h AND all three non-random selectors S-rec/S-prec/S-mag, CIs excluding 0) holds only on I and D = 2/5; on L/O/T the strong S-rec (top-k by recall) matches the unit (cover-based eligibility + sensible selection, not set-cover-specific). The per-letter JOINT of mechanism AND set-cover-selection is 2/5 (I,D). The compact named unit (k=5) is SIGNIFICANTLY BELOW the 15-wide pool on every letter (deltaAUC -0.056 to -0.200) -- human-auditable compactness costs AUC -- reported, not hidden.

    - ROUTER -- the iteration-4 run DID NOT COMPLETE [art_GTc_f26dMzFs]: its emitted JSON is a scale=smoke PLACEHOLDER with a single 'm6_router_concepts' group (a co-tenant job held the shared GPU >2.5h). So the router evidence still rests on the iter-3 full run [art_07ju05r0onqB], where firing-Jaccard separates the extremes (spelling <0.05 -> grouping helps; toxicity ~0.69 -> attribution wins) but firing-Jaccard ALONE is insufficient (numeric high-J yet absorption-like; aggregated-taxonomic low-J yet co-firing) AND the RECALL-HOLE signal ALONE reaches balanced-acc 1.0 with NO derivation counterexample, while the COMBINED rule sits at 0.917 -- LOWER. REVIEWER rigor MINOR: the draft recommends the conjunction on the grounds that 'each single signal has a counterexample,' but recall-hole-alone has NONE on the derivation set, so the justification does not favor the conjunction over recall-hole-alone. And the only truly-prospective test (1/3 hits) had ALL THREE predictions in the SAME regime (co-firing), so it cannot demonstrate out-of-sample DISCRIMINATIVE value.

    - MODEL-DIFFING stays a confound-bounded NULL (control-subtracted genuine shift +0.000 CI[-0.009,0.007]; unit does not beat best single latent) [art_jI2KIJotjzIU]. Steering stays a generality demo (unit most surgical only on L,D).

    WHAT THE ITER-4 REVIEW EXPOSED -- TWO MAJORS THAT NOW GATE PUBLICATION, PLUS FIVE MINORS:
      (R1, SCOPE -- the persistent ceiling, now the #1 blocker) The auditability reframe is the right honest move, but the unique capability (a named, addable/ablatable sub-context absorber) is never shown to CHANGE A DOWNSTREAM OUTCOME THAT MATTERS. Against the goal's three concrete tasks: classification LOSES to a non-SAE dense probe on EVERY task (Georgia 0.995 vs 1.000; numeric integer 0.635 vs 1.000; toxicity loses to a residual probe); steering is surgical on only 2/5 toy spelling letters; model-diffing is a confound-bounded null; toxicity -- the only safety-relevant family -- is a clean negative; and set-cover-specific SELECTION is established on just 3 slices total (Georgia, first-letter I, D). The localization is asserted-as-valuable, not DEMONSTRATED to beat the probe on a result. => ITERATION 5 MUST PRODUCE AT LEAST ONE DOWNSTREAM WIN where the KG-localized single-absorber edit BEATS the dense/diff-of-means baseline on an outcome that matters.
      (R2, RIGOR -- new generalization risk) ALL results come from ONE SAE (gemma-2-2b, layer 12, width-16k canonical). Absorption is KNOWN to depend on dictionary size and hierarchy (the very motivation for the Matryoshka/hierarchical SAEs we cite), so a method whose value proposition is 'repair absorption in frozen public SAEs' must show its units, repairs, surgical edits, and router are NOT artifacts of one (layer, width) dictionary. => ITERATION 5 MUST REPLICATE the headline spine on >=1 second dictionary (65k-width canonical and/or another layer).
      (R3-R7, MINORS) distinct-hole count ~23 not 30; selectivity mean 1452 / median 1262 with cases stated; control = random SINGLE-latent addition; router recommend recall-hole-alone (firing-Jaccard corroborating) + expand prospective to BOTH regimes; taxonomic affirmative selection is n=1-2 (find more cases, report Jordan's n/eligibility next to Georgia).

    THE ITERATION-5 MANDATE (the two MAJORS are load-bearing; nothing else is load-bearing until they exist):
      (M1 = NEW LOAD-BEARING -- A DOWNSTREAM WIN OVER THE BASELINE) Turn the surgical edit [art_0CZwPjG2YMCf] from 'a capability a probe lacks' into 'a BETTER RESULT than the probe on an outcome that matters.' Build at least one task where the KG-localized single-absorber edit OUTPERFORMS the dense diff-of-means / parent-direction baseline: e.g. surgically REMOVE or STEER one sub-context of a safety-relevant or polysemy-sensitive attribute (toxicity sub-attribute, a homograph sense, or a spelling sub-context) while PRESERVING the parent concept AND fluency, scored jointly by (i) on-target effect, (ii) sibling/parent collateral, and (iii) an AxBench-style fluency / LLM-judge score on unrelated prompts. The WIN condition is explicit: at matched on-target effect, the KG edit achieves LOWER sibling+parent collateral AND BETTER preserved fluency than dense erasure, with a bootstrap CI on the difference excluding 0. If the dense baseline matches or beats the KG edit on the joint metric everywhere, that is the declared 'localization buys auditability but not a better outcome' negative -- itself publishable, but it caps the contribution and must be stated as the headline limitation. Note the regime caveat: dense erasure of a redundantly-encoded country/letter membership has HUGE broad margin (the very reason behavioral KL was the iter-4 primary signal), so the task must be chosen where SINGLE-SUB-CONTEXT removal with parent preservation is the GOAL the dense direction structurally over-shoots.
      (M2 = NEW LOAD-BEARING -- CROSS-DICTIONARY ROBUSTNESS) Re-run the headline auditability spine -- KG-repair FDR, the Georgia/Jordan surgical edits, and the firing-Jaccard/recall-hole router -- on at least the 65k-width canonical SAE and/or one other layer of the SAME model, and report: (i) whether the SAME homograph recall holes (Georgia/Jordan) appear; (ii) whether the repairs and surgical selectivities REPLICATE (with honest deltas); (iii) whether the router thresholds TRANSFER. A partial replication with honest deltas substantially de-risks the generalization claim; a clean failure to replicate is a publishable, honest finding about DICTIONARY-DEPENDENCE of absorption (which the literature predicts: wider SAEs absorb MORE). Gate the numeric digit-token reconstruction concern explicitly (numeric reconstructs <0.9 in isolation).
      (M3 = HONEST COUNTING) Report ~23 DISTINCT holes as the primary headline number; present 30 as 'repair VARIANTS (k-track and diagnostic edges) over ~23 distinct holes'; DE-DUPLICATE where kg_ktrack and kg_diagnostic name the same latent; EXCLUDE or separately flag non-hole sub-contexts (numeric 'percent', is_hole=False) so the count matches the 'suppressed-parent recall hole' framing.
      (M4 = SELECTIVITY LABELING) Replace 'median' with 'mean' (1452x) OR report the true median (1262x), consistently across abstract/intro/audit/discussion; state explicitly which cases are averaged and whether the partial-surgical US-4760 (7.8x) is included; report the precision-vs-selectivity relationship across all 7 cases (so 'large' precision 0.571 -> 802x vs US-4760 precision 0.709 -> 7.8x is visible) and SOFTEN 'precision predicts surgicality' to a within-family observation.
      (M5 = CONTROL WORDING) State the repair control as 'a RANDOM SINGLE content-responsive-latent addition (the KG absorber's recall gain exceeds the 95th/99th percentile of single-latent additions)'; keep the implemented single-latent control; drop the 'full population' phrasing.
      (M6 = ROUTER -- FULLY RUN + REFRAME) FULLY EXECUTE the router (the iter-4 run is a smoke placeholder; the GPU was blocked). LEAD with the RECALL-HOLE-ALONE rule (balanced-acc 1.0 on derivation, no derivation counterexample) and frame firing-Jaccard as a CORROBORATING signal; only claim the conjunction if it is SHOWN to generalize better out-of-sample despite lower derivation accuracy. EXPAND the prospective set to contain BOTH regimes (the iter-4/iter-3 prospective set was all co-firing -> no discriminative test) so the router can be wrong in both directions, and report the measured error with a Wilson CI. Keep derivation (12 concepts) and prospective strictly separate.
      (M7 = TAXONOMIC SECOND CASE) Search for >=1 additional suppressed-parent polysemy case to corroborate Georgia (other entity homographs, or a SECOND is-a hierarchy where a general parent is suppressed on specific children); report the Jordan selection result WITH its n=124 and descriptive/ineligible status right next to Georgia, so the reader sees the affirmative non-spelling set-cover evidence is currently one-to-two slices, not a broad win.
      (M8 = UNIT TRANSPARENCY) Keep reporting HELD-OUT per-member subctx_precision and the FOLD each gate is on; the compact named unit AUC alongside the 15-wide pool; and the confident-label fraction of the 15. Restrict the 'auditable' claim to the characterized subset or show the named structure carries the signal.
      (M9 = PRESENTATION + CITATIONS) Strip rebuttal/iteration/infrastructure scaffolding; keep the locked citation venues [art_QBxBPF-9Ldxe, art_i-tkvFCKneA-] (Chanin->NeurIPS 2025; AxBench/SAEBench->ICML 2025; CanonicalUnits->ICLR 2025; PS-Eval cite-and-distinguish; Winnicki observational-KG contrast). Model-diffing stays a confound-bounded null limitation; steering stays a generality demo (surgical on L,D only).

    RE-DESIGNATED HEADLINE (auditability-first; SAME two-track method; the two NEW gates make or break the contribution). On a FROZEN public SAE, grouping latents by interventional co-response to content counterfactuals via the TWO-TRACK algorithm yields training-free, human/LLM-auditable multi-member units and a feature-level KNOWLEDGE GRAPH whose edges carry MEASURED, localized repair utility: a KG-named absorber added to a suppressed parent recovers its recall hole, beating a random SINGLE-latent-addition control (CI excludes 0; ~23 distinct holes survive FDR across spelling/taxonomic/numeric), and ablating that absorber surgically edits ONE sub-context (mean 1452x / median 1262x selectivity over collateral) -- localizations a dense probe structurally lacks. The CENTRAL OPEN CLAIM iteration 5 must close is that this localized, editable fix produces a BETTER DOWNSTREAM OUTCOME than the dense/diff-of-means baseline on a task that matters (lower sibling+parent collateral and preserved fluency at matched on-target effect), AND that the spine REPLICATES on a second SAE dictionary. In the ABSORPTION REGIME the unit also recovers absorbers a count-matched marginal-attribution selection drops (within-SAE set-cover-specific selection on first-letter I,D and the taxonomic Georgia homograph slice). A cheap one-forward-pass RECALL-HOLE measurement (corroborated by low firing-Jaccard) is an a-priori SCREENING HEURISTIC for which regime a concept is in. The method does NOT out-classify a strong non-SAE dense probe on any task; its value is AUDITABLE, EDITABLE, REGIME-TARGETED REPAIR plus the router -- and that value is only fully established once the downstream-win (M1) and cross-dictionary (M2) gates are met.

    PRIMARY ENDPOINT (re-designated; the two gates are load-bearing).
      (a) DOWNSTREAM WIN (NEW LOAD-BEARING, M1): at least one task where the KG-localized single-absorber edit BEATS the dense/diff-of-means baseline on a joint outcome metric (on-target effect, sibling+parent collateral, fluency/LLM-judge), difference CI excluding 0. A clean failure (dense matches/beats everywhere) is the declared 'auditability without a better outcome' limitation and is itself publishable but caps the contribution.
      (b) CROSS-DICTIONARY REPLICATION (NEW LOAD-BEARING, M2): the headline spine (KG-repair FDR, Georgia/Jordan surgical edits, router) is re-run on >=1 second dictionary (65k-width and/or another layer); replication-with-deltas confirms generality, a non-replication is reported as honest dictionary-dependence.
      (c) AUDITABILITY SPINE (achieved iter-4, to be re-counted honestly): ~23 distinct-hole KG-guided repairs survive FDR<=0.05 over the random single-latent control [art_sxwT7hK6YFEA]; surgical edits [art_0CZwPjG2YMCf]; member-labeling beats the shuffle null.
      (d) ROUTER: the RECALL-HOLE-ALONE screen (firing-Jaccard corroborating) reproduces, FULLY RUN, with derivation/prospective reported separately and a both-regime prospective test.
    SUPPORTING: within-SAE set-cover selection where the router predicts absorption -- first-letter per-letter joint (E1 AND set-cover-specific selection) currently 2/5 (I,D) against non-random selectors; taxonomic Georgia (+ any second polysemy case found under M7). E2 absorbed-slice recall is SECONDARY (significant on T only). The headline NO LONGER depends on classification beating attribution on >=3 letters.

    THE TWO-TRACK CLUSTERING ALGORITHM (specification unchanged; precision-gate retained). STEP 1 cover-based eligibility (content-responsive above a shuffle null; firing-precision>=0.7; covers>=1 sub-context). STEP 2 C-TRACK (splitting): positive-Spearman soft-threshold affinity (beta=6, WGCNA) -> Leiden RBConfiguration; resolution by bootstrap-ARI stability; subprocess with 45s timeout + agglomerative fallback. STEP 3 K-TRACK (absorption, anchored greedy max-coverage): ANCHOR = argmax cover-set chosen WITHOUT the diagnostic, with the UNSUPERVISED FIRING-FLOOR PARENT-VALIDATION (anchor must fire on held-out corpus above ~5% -- fixes the letter-I 0%-corpus spurious anchor); HOLES = parent's uncovered pairs; greedily add mutually-exclusive (firing-Jaccard<0.1), PRECISE (>=0.7, gated on a HELD-OUT fold) absorbers covering holes with marginal-gain>=0.05 CI excluding 0; the coverage objective is PRECISION-GATED / precision-WEIGHTED so it does not prefer high-coverage/low-precision absorbers over diagnostic-corroborated ones (Georgia must select 16009 prec .955, not 4697 prec .35). STEP 4 reconcile C-communities and K-covers, de-duplicate by highest coverage gain. STEP 5 ADMISSION: signature C OR matched-null signature K (+ small-k absolute gain>=0.05 CI excluding 0, mutual-exclusivity, precision floor) AND unit-level surface invariance; multiplicity controlled at unit-proposal level (Bonferroni-within-unit then BH across M candidates).

    SAE-LATENT FIRING-STRUCTURE ROUTER (screening heuristic; RECALL-HOLE-PRIMARY). One forward pass over data already held: encode examples, identify the content-responsive parent (with the firing-floor validation), find per-sub-context detectors, report (i) parent per-sub-context recall holes and (ii) detector-vs-parent positive-only firing-Jaccard. RULE: predict absorption-regime (grouping helps) iff the parent has a recall HOLE (>~0.5-0.78) -- the strongest single derivation separator, balanced-acc 1.0, no derivation counterexample -- CORROBORATED by low firing-Jaccard (<~0.05-0.10). The conjunction is reported only if it is SHOWN to generalize better out-of-sample; otherwise recall-hole-alone is the recommendation. Firing-Jaccard alone is insufficient (mislabels numeric high-J and aggregated-taxonomic low-J). The iter-4 router run is a smoke placeholder; iteration 5 fully runs it and expands the prospective set to BOTH regimes. Co-firing (toxicity threat 0.40, identity_attack 0.29, insult 0.66 >> 0.10, no parent hole) => splitting/co-activation regime => supervised attribution wins and CCRG does not help.

    BASELINE GLOSSARY (matched baselines primary): (a) best raw single latent; (b)/(c) observational co-activation/decoder clusters COUNT-MATCHED to k; (d) counterfactual diff-of-means; (e) raw-residual probe; (f) LEACE surface-invariant probe; (g) SCR/TPP oracle pool; (h) count-and-pool-matched SCR/TPP probe; (i) unmatched diff-of-means; (j) oracle group-DRO; (k) label-free group-inference (JTT/GEORGE); (RE-k) random-eligible-k pool = FLOOR (easy bar); (S-rec) top-k by content-flip recall, (S-prec) top-k by firing precision, (S-mag) top-k by mean response magnitude = the NON-RANDOM label-free selectors. SET-COVER SELECTION is isolated ONLY by beating (S-rec)/(S-prec)/(S-mag), not merely (RE-k). For the M1 downstream win, the decisive comparator is the DENSE diff-of-means / parent-erasure direction (baseline f) on the joint collateral+fluency metric.

    NON-SPELLING TESTBED (HOMOGRAPH ABSORPTION; affirmative selection currently n=1-2). Absorption recurs on HOMOGRAPH/POLYSEMOUS tokens whose general parent latent is suppressed -- taxonomic absorption-type slices are EXACTLY Georgia (eligible, hole .80) + Jordan (DESCRIPTIVE n=124<150, hole .71); United States is co-firing/splitting (firing-Jaccard .20, not absorption); all other countries have ~0 hole. So this is a polysemy phenomenon, NOT broad taxonomic absorption, and the affirmative set-cover-selection result is currently ONE eligible country. Iteration 5 (M7) searches for additional suppressed-parent polysemy cases. Numeric = eligibility+pooling, diagnostic-unconfirmed (integer co-firing J=.256, no precision-passing specialist; dense probe AUC 1.000). A non-SAE dense probe matches/beats the unit on ALL non-spelling classification.

    SCOPE AND VALUE PROPOSITION. The defensible contribution is: (1) MEASURED AUDITABILITY -- a feature-level KG whose edges carry localized, EDITABLE repair utility (recall-hole recovery beating a random single-latent addition; surgical single-absorber edits; (k) cannot localize) plus human/LLM-auditable members; (2) an A-PRIORI RECALL-HOLE SCREENING HEURISTIC for when grouping helps vs when attribution wins; (3) a WITHIN-SAE absorption-regime selection win where it occurs (first-letter I,D; taxonomic Georgia). The OPEN, GATING questions iteration 5 must answer are whether (1) yields a BETTER DOWNSTREAM OUTCOME than a dense baseline (M1) and whether the spine REPLICATES across SAE dictionaries (M2). The method does NOT claim to out-classify a strong dense probe; toxicity is a clean co-firing negative. HEADLINE = auditable absorption-regime repair-and-edit + the router; classification is SUPPORTING and within-SAE.

    HONEST NEGATIVES (each publishable): unit out-classifies NO non-SAE dense probe on any task; the localized fix is not YET shown to beat the dense baseline on an outcome that matters (the central ceiling); all results are from ONE SAE dictionary (generalization untested); per-letter joint mechanism+selection only 2/5 (I,D); non-spelling affirmative set-cover selection is effectively n=1 (Georgia), 1-2 with descriptive Jordan; the form-free MAGNITUDE diagnostic is precision-blind (per-edge top-1 agreement 0 with the precise member); compact named units cost AUC vs the wide pool; numeric is eligibility+pooling and diagnostic-unconfirmed; toxicity K-necessity REFUTED; router combined-rule does NOT beat recall-hole-alone on derivation and the prospective set was single-regime (1/3); the iter-4 router run did not complete; model-diffing a confound-bounded null; steering surgical only on L,D; RE-k is an easy floor. A clean failure of the M1 downstream-win gate (dense baseline matches/beats the KG edit everywhere) or the M2 replication gate (spine does not transfer dictionaries) is the declared method-does-not-clear-the-bar outcome and is itself publishable as an honest finding.

    MOTIVATION (substance unchanged). Single SAE latents are unreliable units: feature absorption (a child latent suppresses a general parent's firing; Chanin 2409.14507, NeurIPS 2025), splitting, hedging (2505.11756), and 'SAEs Do Not Find Canonical Units' (ICLR 2025) converge on no single latent reliably tracking a concept; AxBench (ICML 2025) and DeepMind's negative report show plain diff-of-means beats raw-latent SAE methods. Absorption is the regime where OBSERVATIONAL signals break by construction (parent/child mutually exclusive in firing) and where MARGINAL-ATTRIBUTION selection (SCR/TPP) silently drops the absorber. Correlation-community detection (DiffCoEx/WGCNA) handles shared-support splitting; anchored greedy set-cover (Nemhauser-Wolsey-Fisher / Feige (1-1/e)) handles disjoint-support absorption -- coverage-complementarity is a set-level property no pairwise affinity can express. The executed lesson: this matters ONLY in the absorption regime (mutually-exclusive firing AND parent recall holes), a cheap recall-hole measurement tells you a priori whether you are in it, and the durable value is an AUDITABLE, EDITABLE feature-KG repair -- whose practical worth is established by showing it produces a BETTER downstream result than a dense baseline and REPLICATES across dictionaries. Architectural remedies (Matryoshka/H-SAE/SASA) retrain and are orthogonal; their dictionary-size dependence is exactly why cross-dictionary replication (M2) matters.

    SUCCESS CRITERIA. METHOD CONFIRMED iff: (LOAD-BEARING) (M1) at least one downstream task where the KG-localized single-absorber edit BEATS the dense/diff-of-means baseline on a joint on-target/collateral/fluency metric (difference CI excludes 0); AND (M2) the auditability spine REPLICATES on >=1 second SAE dictionary (or non-replication is reported as honest dictionary-dependence); AND the iter-4 auditability spine holds at the honest ~23-distinct-hole count with the random single-latent control; AND the RECALL-HOLE router reproduces (fully run) with derivation/prospective separated and a both-regime prospective test. SUPPORTING (strengthen, do not gate): within-SAE set-cover-specific selection where the router predicts absorption (first-letter 2/5 I,D; taxonomic Georgia + any second case from M7); member-labeling above null; admission false-admit <=0.05; the steering demo (L,D). HONEST NEGATIVES are reportable: failure of M1 (localization buys auditability but not a better outcome) or M2 (dictionary-dependence) caps the contribution but is publishable; numeric stays unconfirmed; toxicity stays a co-firing negative.
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
  Same two-track auditability frame; adds downstream-win + cross-dictionary gates, fixes counts/router framing.
_confidence_delta: unchanged
_key_changes:
- >-
  Recorded iter-4 execution: auditability spine EXPANDED (30 FDR repair VARIANTS over ~23 distinct holes across spelling/taxonomic/numeric;
  M1b surgical edits 5/7 confirmed, mean 1452x/median 1262x; member-labeling 0.730 vs 0.096), taxonomic conflation FIXED (precision-gated
  rebuild -> Georgia 16009, set_cover_established), first-letter selection isolated (set-cover-specific 2/5: I,D; E1 5/5 via
  firing-floor anchor fix), citation audit.
- >-
  NEW LOAD-BEARING M1 (reviewer scope MAJOR, the persistent ceiling): produce a downstream outcome where the KG-localized
  single-absorber edit BEATS the dense/diff-of-means baseline (lower sibling+parent collateral AND preserved fluency at matched
  on-target effect, AxBench-style judge, difference CI excluding 0) — convert 'a capability a probe lacks' into 'a better
  result than the probe'.
- >-
  NEW LOAD-BEARING M2 (reviewer rigor MAJOR): replicate the headline spine (KG-repair FDR, Georgia/Jordan surgical edits,
  router) on >=1 second SAE dictionary (65k-width and/or another layer); honest deltas, or a publishable dictionary-dependence
  finding.
- >-
  Corrected counting: ~23 DISTINCT holes is the primary number; 30 = repair variants (de-dup kg_ktrack==kg_diagnostic identical
  latents; exclude non-hole numeric 'percent', is_hole=False).
- >-
  Corrected selectivity labeling: mean 1452x / median 1262x with cases stated (US-4760 partial-surgical 7.8x flagged); SOFTEN
  'precision predicts surgicality' (the 'large' 0.571->802x vs US-4760 0.709->7.8x counterexample).
- >-
  Corrected repair-control wording: random SINGLE content-responsive-latent addition (95th/99th pct of single-latent gains),
  NOT 'full population max-pool'.
- >-
  Router REFRAMED to RECALL-HOLE-ALONE primary (bal-acc 1.0, no derivation counterexample; firing-Jaccard corroborating);
  FULLY RE-RUN the router (iter-4 art_GTc_f26dMzFs confirmed scale=smoke placeholder, GPU-blocked) and EXPAND the prospective
  set to BOTH regimes (iter-4 prospective was all co-firing => no discriminative test).
- >-
  Taxonomic affirmative set-cover selection is effectively n=1 (Georgia), 1-2 with descriptive Jordan (n=124<150); mandated
  searching for >=1 more suppressed-parent polysemy case and reporting Jordan's n/eligibility beside Georgia.
- >-
  Confidence UNCHANGED: auditability spine solidified and integrity fixes landed, but the significance ceiling (beat a baseline
  on an outcome that matters) is unmoved and a new cross-dictionary generalization gap opened — net flat.
relation_type: evolution
</hypothesis>

<artifact_direction>
Make this direction concrete and actionable. Keep the same type and respect dependencies.

id: experiment_iter5_dir1
type: experiment
objective: >-
  M1 — THE LOAD-BEARING DOWNSTREAM WIN. Produce at least one task where the KG-localized single-absorber edit BEATS the dense
  diff-of-means / parent-erasure baseline on an outcome that matters: selective sub-concept UNLEARNING / TARGETED EDITING
  in which the model must suppress ONE sub-context (a homograph sense, a first-letter sub-context, or a toxicity sub-attribute)
  while PRESERVING the parent concept, sibling sub-contexts, AND fluency. WIN condition (explicit, pre-registered): at MATCHED
  on-target (forget) effect, the KG edit attains strictly LOWER sibling+parent collateral AND BETTER preserved fluency than
  dense erasure, with a paired-bootstrap CI on the JOINT-outcome difference excluding 0. A clean failure (dense matches/beats
  everywhere) is the declared 'localization buys auditability but not a better outcome' negative — itself publishable but
  capping the contribution — and must be stated as the headline limitation. Convert 'a capability a probe lacks' into 'a better
  RESULT than the probe.'
approach: >-
  Build on the iter-4 surgical-edit machinery by reading its workspace (3_invention_loop/iter_4/gen_art/gen_art_experiment_2,
  artifact art_0CZwPjG2YMCf: edit operators, behavioral next-token KL, canonical units/KG, JumpReLUSAE/ModelBundle, gating
  cosine>0.9 @ blocks.12.hook_resid_post) and re-derive units/KG from the method dossier (art_RidEJtBC7gPT). Define a SELECTIVE-UNLEARNING
  / TARGETED-EDIT downstream task with a joint outcome metric, NOT a classification metric (classification is conceded to
  dense). PRIMARY case (absorption regime, where dense structurally over-shoots): Georgia-as-country sense. FORGET set = held-out
  Georgia-country contexts; RETAIN set = sibling countries (France/Japan/Brazil/...) AND general parent (is-a-country) AND
  unrelated prompts. Operators (forward hooks at the edit layer): KG-ABL = ablate the single KG-named precision-passing absorber
  (16009) h -= lambda*z_l*W_dec[l] (gated by its own sparse firing); DENSE-ABL = erase the diff-of-means / LEACE parent 'is-a-country'
  direction h -= beta*(h.u)u (baseline f); plus RAND (firing-rate-matched random content latent) and a no-op control. MATCH
  on-target: sweep lambda and beta so both operators reach the SAME forget-quality target (e.g. equalized next-token KL /
  generation-suppression on the forget set), then compare at matched effect. MEASURE three outcome dimensions: (i) on-target/forget
  effect, (ii) sibling+parent COLLATERAL (behavioral next-token KL on retain contexts + retain-set detection/generation preservation),
  (iii) FLUENCY/UTILITY via an AxBench-style protocol — generate continuations under each edit on retain + unrelated prompts
  and score with an OpenRouter LLM judge (anthropic/claude-haiku-4.5, temp 0, graded 0-2 harmonic-mean rubric for fluency+coherence+whether
  the target sense was removed+whether unrelated content is preserved; track cumulative cost, hard $10 cap, target <$2) plus
  a model-internal perplexity/PPL check. JOINT outcome = a retain-quality x fluency composite at matched forget-quality; report
  KG-minus-dense on collateral, on fluency, and on the joint composite with paired-bootstrap CIs (B>=10,000, resampling contexts/prompts
  as clusters). SECONDARY case (still absorption): a first-letter sub-context edit (e.g. 'large'->8463) mirroring the same
  protocol. SAFETY-RELEVANT + ROUTER-TIED HONEST CASE (co-firing regime): a toxicity sub-attribute (e.g. identity_attack->13367
  or insult) where firing-Jaccard is high and the parent has no hole; show single-absorber ablation is NOT cleanly surgical
  there (high footprint/collateral), so dense or attribution is the right tool — i.e. the router PREDICTS in advance where
  KG wins vs loses, turning a per-case loss into evidence for the router. Report a clean per-case table: regime (router prediction),
  matched forget-quality, KG vs dense collateral, KG vs dense fluency, joint difference + CI, win/tie/loss verdict. Use aii-use-hardware/aii-long-running-tasks
  (detect GPU, bf16, memory-safe one-pass batching, gradual scaling: Georgia first, then first-letter, then toxicity). Emit
  method_out.json (exp_gen_sol_out schema): per-case matched-effect curves, joint-outcome differences with CIs, the win verdicts,
  the AxBench LLM-judge scores + spend, a datasets block of per-context/per-prompt rows with predict_* per operator for downstream
  evaluation, and honest negatives verbatim. Validate full/mini/preview <100MB.
depends_on:
- id: art_t2uUbjSwpd3t
  label: taxonomic-data
  relation_type:
  relation_rationale:
- id: art_dpYpjSn2Xvg3
  label: spelling-data
  relation_type:
  relation_rationale:
- id: art_8QO7pl6Pd8UQ
  label: toxicity-data
  relation_type:
  relation_rationale:
- id: art_RidEJtBC7gPT
  label: method
  relation_type:
  relation_rationale:
- id: art_I2MrezW41iQo
  label: diagnostic
  relation_type:
  relation_rationale:
</artifact_direction>

<dependencies>
Completed artifacts this artifact can use during execution.

--- Dependency 1 ---
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
out_dependency_files:
  file_list:
  - research_out.json

--- Dependency 2 ---
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
out_dependency_files:
  file_list:
  - research_out.json

--- Dependency 3 ---
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
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json

--- Dependency 4 ---
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
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json

--- Dependency 5 ---
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
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
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

EXPERIMENT executor scope:
  Output: method_out.json with results (metrics, predictions, analysis) — the core computational work
  DOES: Implement and run methods/algorithms, compute metrics, compare approaches, produce quantitative results
  DOES NOT: Collect new datasets (depends on DATASET artifacts for input data), write formal proofs
  This is the right artifact for any code that processes data and produces results
</artifact_executor_scope>

<artifact_planning_rules>
EXPERIMENT: Must depend on at least one DATASET. Define clear metrics and baselines before running. Consider trying multiple method variations rather than a single approach.
</artifact_planning_rules>

<compute_profiles>
Choose the compute profile this artifact needs for execution.
Available profiles for experiment artifacts:
  - gpu: 1x NVIDIA RTX A4500, 20GB VRAM, 7 vCPUs, 29GB RAM — ML training, CUDA, large models (fallback: GPUs cheap→expensive: 2000 Ada → A4000 → 4000 Ada → L4 → 4090 → 5090)
  - cpu_heavy: 4 vCPUs, 32GB RAM — large datasets, memory-intensive processing (fallback: CPUs cheap→expensive, then GPU hosts cheap→expensive (all ≥32GB RAM))

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
  "description": "Plan for an EXPERIMENT artifact.",
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
    "implementation_pseudocode": {
      "description": "High-level pseudocode for the experiment implementation",
      "title": "Implementation Pseudocode",
      "type": "string"
    },
    "fallback_plan": {
      "description": "What to do if the primary approach fails - alternative methods, simplified versions",
      "title": "Fallback Plan",
      "type": "string"
    },
    "testing_plan": {
      "description": "How to validate the experiment works: start with small/fast tests, look for confirmation signals before running full-scale experiments",
      "title": "Testing Plan",
      "type": "string"
    }
  },
  "required": [
    "title",
    "implementation_pseudocode",
    "fallback_plan",
    "testing_plan"
  ],
  "title": "ExperimentPlan",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-06-18 01:55:36 UTC

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
