# gen_strat_1 — test_idea

> Phase: `invention_loop` · round 5 · `gen_strat`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_strat_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 01:42:20 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A strategy planner (Step 3.1: GEN_STRAT in the invention loop)

Each iteration of the invention loop runs: GEN_STRAT → GEN_PLAN → GEN_ART → GEN_PAPER_TEXT → REVIEW_PAPER → UPD_HYPO
Artifact types: RESEARCH (web search), EXPERIMENT (code), DATASET (data collection), EVALUATION (metrics), PROOF (Lean 4)
State persists across iterations: strategies, plans, artifacts, paper_texts (read from the run tree)

You received the hypothesis, iteration status (current + remaining), previous iteration's strategies, available artifact types, existing artifacts, and reviewer feedback.
Your strategy governs THIS iteration only. You define what artifacts to create NOW.

Focused strategy → efficient progress. Scattered strategy → wasted iteration.
</your_role>
</ai_inventor_context>

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

<research_methodology>
Think like a researcher planning a study for a top venue.

- All strategies run in parallel and their artifacts combine into one pool. Together they must build toward a publishable paper — each strategy contributes a distinct, necessary piece. No strategy should be a standalone island.
- Ask yourself: what would a reviewer need to see? Proper baselines, controlled comparisons, ablations that isolate what matters. Plan artifacts that preempt reviewer objections.
- Depth over breadth. One well-designed experiment with proper controls beats five shallow ones.
- Match your evaluation to your claims. Measure what the hypothesis actually asserts.
- When results are weak or partial, vary the approach before writing it off. One failed method doesn't falsify the hypothesis.
- If iterations remain, think about what the NEXT iteration will need. Leave useful building blocks — datasets, baselines, preliminary results — that future strategies can build on, refine, or compare against.
</research_methodology>

<principles>
1. FOCUS ON NOVELTY - every strategy must lead to a genuinely novel contribution
2. MAXIMIZE PARALLELIZATION - all artifacts in your strategy run in parallel
3. BUILD ON EXISTING WORK - use completed artifacts from previous iterations, learn from failures
4. ITERATE ON THE METHOD - a negative result is about the approach, not the hypothesis. Try different methods, parameters, data, or formulations within the hypothesis bounds.
5. DIAGNOSE BEFORE DECIDING - before each iteration, review what worked, what didn't, and why. Use that to choose what to try next. Gaps are action items, not conclusions.
6. SET DEPENDENCIES WISELY - depends_on is a list of {id, label} objects referencing existing artifacts; each label is a short free-text type (a word or two, e.g. "dataset", "validates", "extends") that tags how the dep is used
7. PLAN FOR DEPENDENCIES - if an artifact depends on another (e.g. experiments need datasets), ensure prerequisites exist first or plan them this iteration for the next
</principles>

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
Your strategy should advance this hypothesis.

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

<iteration_status>
Current iteration: 5 of 10
Remaining (including this one): 6
</iteration_status>

<previous_strategies>
Strategies from the PREVIOUS iteration. You can CONTINUE these directions,
ADAPT based on what worked and what didn't in the artifacts produced, or PIVOT if results suggest a better path.

--- Strategy 1 ---
kind: strategy
id: gen_strat_1_idx1
title: >-
  Iteration 4: Pivot the Headline to AUDITABLE ABSORPTION-REGIME REPAIR — Expand the Measured KG-Repair Loop, Add a KG-Localized
  Surgical-Edit Downstream Task a Dense Probe Cannot Deliver, Fix the Taxonomic Unit/Specialist Conflation with a Precision-Weighted
  K-Track, Isolate Set-Cover from Sensible Label-Free Selection (S-rec/S-prec/S-mag), and Honor the Per-Letter Joint Endpoint
objective: >-
  Convert the reviewer's two dominant MAJORs into executed evidence that makes the paper stand on its UNIQUE, defensible capability
  rather than an over-claimed classification win. (A) Make MEASURED AUDITABILITY the load-bearing headline (M1): EXPAND the
  KG-guided recall-repair loop to many more concepts/sub-contexts with multiplicity-controlled bootstrap CIs, AND add one
  concrete DOWNSTREAM task where the localized, editable single-latent fix matters and a dense probe structurally cannot deliver
  it — a KG-localized SURGICAL SUB-CONCEPT EDIT (ablate/steer exactly one named absorber, e.g. Georgia=16009 or first-letter
  'list'=3069) with on-target/collateral/KL side-effect measurement, contrasted against a dense-probe edit (one hyperplane
  cannot localize one sub-context) and a random-latent control. (B) FIX THE TAXONOMIC CONFLATION (M2, the single highest-impact
  fix): rebuild the taxonomic CLASSIFICATION unit from the PRECISION-PASSING, diagnostic-corroborated absorbers (Georgia 16009
  prec 0.955, US 846, Jordan 540/8347) by adding a PRECISION-WEIGHTED / precision-GATED coverage objective to the K-track
  so greedy stops preferring the high-coverage/low-precision absorber (4697 prec 0.35); report THAT unit's Georgia AUC + RE-k-anchored
  + the new label-free controls, replace the single '0.318' with PER-EDGE KG-agreement (Georgia, Jordan, US separately), and
  characterize WHEN non-spelling absorption occurs (homograph/polysemous tokens with parent recall holes — exactly Georgia+Jordan,
  not broad taxonomic generalization). (C) ISOLATE SET-COVER from sensible selection (M5) by adding NON-RANDOM, label-free,
  count-matched controls (top-k by content-flip recall, by firing precision, by mean response magnitude) on both first-letter
  and taxonomic. (D) HONOR THE ENDPOINT (M4): report the per-letter JOINT (E1 AND selection)=2/5 (T,D) and rename the verdict
  so it does not imply mechanism+selection co-occur on 3 letters; annotate I as selection-without-mechanism. (E) REFRAME THE
  ROUTER (M6) as a screening heuristic with measured error, lead with the combined low-Jaccard-AND-high-recall-hole rule,
  and report derivation vs truly-prospective separately, adding cheap new held-out concepts. (F) Provide UNIT TRANSPARENCY
  (M7): held-out per-member precision with explicit fold disclosure, compact named-member-only unit AUC alongside the 15-wide
  pool, and the fraction of members receiving a confident LLM label. (G) Finalize citations/positioning (M8) and the homograph/surgical-edit
  novelty framing. The novel contribution being established: a training-free, auditable, EDITABLE feature knowledge graph
  whose edges carry MEASURED localized repair-and-edit utility a dense probe lacks, plus an a-priori router for when to use
  it.
rationale: >-
  The reviewer's scope MAJOR is decisive: after every fix the unit out-classifies NO non-SAE dense probe on any task and toxicity
  (the safety-relevant family) is a clean co-firing negative, so the affirmative classification story is narrow and within-SAE.
  But the reviewer also names exactly where a UNIQUE capability is demonstrated — the measured KG-guided recall repair and
  member-labeling — and instructs us to expand it and make it the headline. That instruction maps one-to-one onto hypothesis
  mandate M1 and is the highest-leverage use of this iteration. The auditability spine is also the most defensible result
  already in hand (art_lvYKkaolutJG: 8 repairs beat random-addition with CIs excluding 0; member-labeling 0.716 vs null 0.090),
  so EXPANDING it (more sub-contexts + a downstream edit task) is low-risk, high-payoff. The taxonomic-conflation MAJOR is
  concrete and falsifiable: the artifact itself shows the classification unit [3792,4697,9339,8442] uses the prec-0.35 Georgia
  absorber while the diagnostic-corroborated specialist is 16009 (prec 0.955); rebuilding from the precision-passing set with
  a precision-weighted K-track will likely STRENGTHEN the Georgia result and is the cheapest way to remove a headline overstatement
  a careful reviewer will catch. The endpoint MAJOR is a pure rigor/reporting fix (per-letter joint = 2/5) plus a verdict
  rename, computed from data largely in hand. The minors (M5 non-random controls, M6 router reframe, M7 transparency) each
  require re-deriving units and re-encoding (~8 min/$0 per pipeline) but are mechanical given the fully-specified algorithm
  in the method dossier (art_RidEJtBC7gPT) and the cached/re-runnable iter-2/iter-3 pipelines, which each artifact reads from
  its run-tree workspace path for code reuse and unit cross-check. All six artifacts are self-contained against the frozen
  iteration-1/2 datasets and the iteration-1 dossiers, run in parallel, and become the executed evidence the next iteration's
  auditability-headlined paper stands on.
artifact_directions:
- id: experiment_iter4_dir1
  type: experiment
  objective: >-
    NEW HEADLINE PART 1 (M1a + M7-fraction): EXPAND the measured KG-guided recall-repair loop and member-labeling from the
    current 8 repairs / 67 members to the full set of eligible absorbed sub-contexts, with multiplicity control across the
    now-many repairs, so the auditability result is broad enough to be the paper's load-bearing spine. Establish that the
    emitted feature knowledge graph carries MEASURED, localized repair utility (recall-hole recovery beating a random-addition
    control with a bootstrap CI excluding 0) across spelling AND homograph-taxonomic AND numeric, that a label-free group-inference
    probe (k) structurally cannot localize the fix, and that unit members are human/LLM-auditable — and report the FRACTION
    of each unit's members (including the full 15-wide first-letter pool) that receive a confident, non-shuffle LLM label.
  approach: >-
    Re-encode first-letter (art_dpYpjSn2Xvg3) and non-spelling (art_t2uUbjSwpd3t) through the frozen Gemma-Scope SAE (loader/hook/firing
    from art_RidEJtBC7gPT: gemma-scope-2b-pt-res-canonical layer_12/width_16k from params.npz; firing=encode>0; hook blocks.12.hook_resid_post;
    gate on reconstruction cosine>0.9 before analysis) and RE-DERIVE the admitted units + anchor->absorbed-child knowledge
    graphs via the two-track algorithm; for code reuse and cross-check read the iter-3 auditability pipeline + units from
    its run-tree workspace path (3_invention_loop/iter_3/gen_art/gen_art_experiment_3/method.py and method_out.json). (1)
    REPAIR-LOOP EXPANSION: for EVERY eligible sub-context with a parent recall hole — all first-letter slices (L/O/T/I/D),
    ALL taxonomic homograph countries with holes (Georgia, Jordan, United States, and TEST Turkey/Chile/other flagged homographs
    for holes), and numeric sub-contexts (year/percent/integer/...) — identify the hole on a SELECTION split, read the KG
    for the covering absorber, ADD it to the parent (max-pool), and MEASURE recall recovery on a DISJOINT held-out EVAL split
    vs a control that adds the full population of other content-responsive latents, paired bootstrap B>=10,000; report the
    KG-minus-random gain, its CI, and the percentile vs random. Because expansion creates many simultaneous tests, apply Benjamini-Hochberg
    across all repairs and report the count surviving FDR<=0.05 (this multiplicity control must live IN this experiment since
    same-iteration evaluations cannot depend on it). For taxonomic, run the repair with BOTH the K-track absorber AND the
    higher-precision diagnostic-corroborated absorber (16009 Georgia, 540/8347 Jordan, 846 US) and report both. (2) (k)-CANNOT-LOCALIZE:
    build the label-free JTT/GEORGE-style group-inference probe (per art_RidEJtBC7gPT), confirm its decoder-projection argmax
    is the PARENT not the absorber (so it classifies holes but exposes no addable per-sub-context latent), report the absorbers'
    projection ranks. (3) MEMBER-LABELING EXPANSION + FRACTION (M7): for every member of every admitted unit (anchor + absorbers,
    INCLUDING all 15 members of the first-letter max-pool), assemble logit-lens top tokens + top activating corpus windows
    with the sub-context label WITHHELD, send to an OpenRouter judge (anthropic/claude-haiku-4.5, temp 0, forced choice; track
    cumulative cost, hard $10 cap, target <$1), score agreement vs a shuffled-label null over many shuffles with a bootstrap-CI
    gap, and report per-role accuracy (anchor vs absorber) AND the FRACTION of the 15-wide first-letter members that receive
    a confident (above-null-margin) label — directly answering the '15-wide vs named' critique. Report honest negatives verbatim
    (sub-contexts where KG repair ties the random-addition control, e.g. first-letter L/T candidate words). Use aii-use-hardware
    / aii-long-running-tasks (detect GPU, bf16, memory-safe batching, mini->full scaling). Emit method_out.json (exp_gen_sol_out
    schema) with per-sub-context repair stats (recall_anchor, recall_anchor_plus_kg, gain_kg, CI, percentile, BH-adjusted
    q, k-track vs diagnostic variants, honest_negatives), the (k) localization check, member-labeling agreement + gap CI +
    per-role accuracy + 15-member confident-label fraction, cumulative LLM spend, and a datasets block of repair-loop and
    member-labeling rows. Validate full/mini/preview <100MB.
  depends_on:
  - id: art_dpYpjSn2Xvg3
    label: dataset
    relation_type:
    relation_rationale:
  - id: art_t2uUbjSwpd3t
    label: dataset
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
- id: experiment_iter4_dir2
  type: experiment
  objective: >-
    NEW HEADLINE PART 2 (M1b): deliver the concrete DOWNSTREAM task where the localized, editable single-latent fix MATTERS
    and a dense probe structurally cannot deliver it — a KG-LOCALIZED SURGICAL SUB-CONCEPT EDIT with side-effect measurement.
    Demonstrate that, using the feature knowledge graph, one can ablate or steer EXACTLY ONE sub-context (e.g. erase 'Georgia'-as-country,
    or suppress one absorbed first-letter word-context) by editing its single named absorber latent, achieving HIGH on-target
    effect with LOW collateral on sibling sub-contexts and low KL on unrelated prompts — whereas a dense difference-of-means/probe
    direction (one hyperplane for the whole parent concept) cannot separate the sub-context from the parent and therefore
    incurs high collateral, and a label-free group-probe (k) exposes no per-sub-context handle at all. This is the unique-capability
    result that justifies the auditability-first headline and directly answers the goal's 'activation steering with side-effect
    measurement' downstream requirement.
  approach: >-
    Re-encode taxonomic (art_t2uUbjSwpd3t) and first-letter (art_dpYpjSn2Xvg3) through the frozen SAE (loader/hook/firing
    from art_RidEJtBC7gPT) and re-derive the admitted units + KG; for code reuse read the iter-2 steering machinery and unit
    definitions from their run-tree workspace paths (3_invention_loop/iter_2/gen_art/gen_art_experiment_1 for first-letter
    steering/units; iter_2/gen_art/gen_art_experiment_3 for taxonomic units) and the iter-3 auditability KG from iter_3/gen_art/gen_art_experiment_3.
    PRIMARY case (absorption regime, taxonomic): pick a sub-context with a parent recall hole whose KG names a precision-passing
    absorber (Georgia -> 16009). SURGICAL ABLATION: at the layer-12 residual, subtract the absorber latent's reconstructed
    contribution (decoder direction x its activation), then measure (on-target) the drop in detecting/producing Georgia-as-country
    on held-out Georgia contexts; (collateral) preservation of detection on SIBLING countries (France/Japan/...) and on the
    parent concept broadly; (general) full-vocabulary KL on a held-out set of unrelated prompts and a fluency/PPL check. BASELINES
    at matched on-target effect: (i) DENSE-PROBE edit — erase the surface-invariant 'is-a-country' probe direction (f, LEACE)
    or the diff-of-means direction; because it is a single hyperplane for the whole parent it cannot localize to Georgia,
    so report its collateral (expected: all-country detection collapses, or no Georgia-specific effect achievable); (ii) RANDOM-LATENT
    ablation control (averaged over draws; expected on-target ~0); (iii) the (k) probe which provides NO per-sub-context latent
    to edit. Define SURGICAL SELECTIVITY = on-target effect / collateral effect and report it with bootstrap CIs; the KG single-latent
    edit should dominate the dense-probe edit on selectivity. Also run a STEERING-TOWARD variant (add the absorber decoder
    direction; measure on-target token emission vs collateral KL). MIRROR on first-letter (suppress one absorbed word-context,
    e.g. 'list'=3069, vs the dense first-letter probe). NEGATIVE-POLE tie to the router: attempt the same surgical edit on
    a TOXICITY sub-attribute (co-firing regime, no clean absorber) and show localization is NOT clean there (high collateral
    because detectors co-fire with the parent) — confirming the edit capability is regime-scoped exactly as the router predicts.
    Memory-safe one-pass-at-a-time GPU batching; gradual scaling (taxonomic Georgia first, then first-letter, then the toxicity
    negative pole). $0 LLM spend (all measurement is model-internal; optional small LLM-judge for output on-target/fluency
    under the $10 cap if needed, target <$1). Emit method_out.json (exp_gen_sol_out schema) with per-case on-target/collateral/KL/PPL
    curves at matched effect, surgical-selectivity with CIs for KG-edit vs dense-edit vs random vs (k), the toxicity negative-pole
    result, and per-prompt arrays for downstream eval. Validate full/mini/preview <100MB.
  depends_on:
  - id: art_t2uUbjSwpd3t
    label: dataset
    relation_type:
    relation_rationale:
  - id: art_dpYpjSn2Xvg3
    label: dataset
    relation_type:
    relation_rationale:
  - id: art_8QO7pl6Pd8UQ
    label: neg-pole-dataset
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
- id: experiment_iter4_dir3
  type: experiment
  objective: >-
    FIX THE TAXONOMIC UNIT/SPECIALIST CONFLATION (M2 — the single highest-impact reviewer fix) + HOMOGRAPH SCOPE (M3) + NON-SPELLING
    SET-COVER ISOLATION (M5) + UNIT TRANSPARENCY (M7-taxonomic). Make the classification unit and the diagnostic-corroborated
    specialists the SAME latent set by rebuilding the taxonomic K-track unit from the PRECISION-PASSING absorbers (Georgia
    16009 prec 0.955, US 846, Jordan 540/8347) using a precision-weighted/precision-gated coverage objective, then report
    THAT unit's Georgia AUC, RE-k-anchored selection, and the new non-random label-free controls; replace the single mean
    '0.318' KG-agreement with PER-EDGE agreement (Georgia, Jordan, US separately); and characterize precisely WHEN non-spelling
    absorption occurs (homograph/polysemous tokens with parent recall holes), reframing from 'broad taxonomic generalization'
    to 'absorption recurs on polysemous tokens predicted by the router's recall-hole signal'.
  approach: >-
    Re-derive the non-spelling K-track from art_RidEJtBC7gPT; for code reuse and cached-encoding reuse read the iter-3 non-spelling
    re-analysis from its run-tree workspace path (3_invention_loop/iter_3/gen_art/gen_art_experiment_2/method.py) and the
    iter-2 non-spelling run (iter_2/gen_art/gen_art_experiment_3). (1) PRECISION-WEIGHTED K-TRACK (M2): modify the anchored
    greedy coverage objective so it no longer prefers high-coverage/low-precision absorbers over high-precision diagnostic-corroborated
    ones — implement BOTH (a) a HARD precision-GATE that only admits absorbers whose HELD-OUT subctx_precision >= 0.7, and
    (b) a precision-WEIGHTED objective (maximize precision x marginal-coverage-gain). Apply the precision/jaccard/gain gates
    on a TRAIN fold and EVALUATE/report on a disjoint held-out fold (M7 fold disclosure). Verify the rebuilt Georgia unit
    now selects 16009 (prec 0.955) not 4697 (prec 0.35); if the greedy STILL diverges from the diagnostic-corroborated set
    under some objective, report that explicitly as a limitation of the max-coverage objective. (2) REBUILT-UNIT RESULTS:
    report the rebuilt taxonomic unit's Georgia-slice AUC (positives=150 Georgia tokens vs taxonomic negatives), unit-(h)
    and unit-(g) AUC-difference CIs (paired bootstrap B>=10,000), unit-vs-RE-k-anchored (anchor fixed, only absorbers randomized)
    — expected STRONGER than the iter-3 0.099 since 16009 prec 0.955 >> 4697 prec 0.35. (3) PER-EDGE KG-AGREEMENT (M2): report
    form-free diagnostic KG-agreement top-1 PER EDGE (Georgia, Jordan, US) NOT the 3-edge mean; state explicitly that diagnostic
    corroboration currently holds for the descriptive Jordan edge (n=124<150, eligible=False) and report whether the REBUILT
    high-precision Georgia unit (16009) now corroborates Georgia. (4) M5 NON-RANDOM CONTROLS: add label-free, count-matched-to-k
    selection controls — (S-rec) top-k by content-flip recall, (S-prec) top-k by firing precision, (S-mag) top-k by mean response
    magnitude — and report unit-minus-each AUC-difference CIs on the Georgia slice; the set-cover-specific claim is established
    ONLY if the unit beats these (CI excluding 0), else scope taxonomic selection to 'cover-based eligibility + sensible selection'.
    (5) HOMOGRAPH SCOPE (M3): for ALL countries (homographs Georgia/Jordan/Turkey/Chile/... AND non-homographs), measure parent
    per-sub-context recall hole and detector firing-Jaccard; show absorption-type slices (hole>0.5 AND Jaccard<0.10) are EXACTLY
    the homographs whose general country-latent is suppressed, and every non-homograph country has ~0 hole and no selection
    advantage — establishing absorption recurs on polysemous tokens, not broadly. (6) M7 transparency: report each rebuilt
    member's HELD-OUT subctx_precision and the fold each gate was evaluated on. Reuse cached CSR latents + fp16 residuals
    if available (CPU-fallback acceptable, per iter-3 sm_120 note, kept to a repro appendix); else GPU re-encode (memory-safe
    batching). Emit method_out.json (exp_gen_sol_out schema) with rebuilt-unit members + held-out precision, per-edge KG-agreement,
    all AUC-difference CIs (unit vs g/h/RE-k-anchored/S-rec/S-prec/S-mag/dense), the homograph-vs-non-homograph hole table,
    the precision-objective ablation (gated vs weighted vs original greedy), and per-row diagnostic predictions. Validate
    full/mini/preview <100MB.
  depends_on:
  - id: art_t2uUbjSwpd3t
    label: dataset
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
- id: experiment_iter4_dir4
  type: experiment
  objective: >-
    FIRST-LETTER SELECTION ISOLATION (M5) + ENDPOINT HONESTY (M4) + UNIT TRANSPARENCY (M7-compact). Isolate the two-track
    set-cover from sensible label-free selection by adding NON-RANDOM, count-matched controls (top-k by content-flip recall
    / firing precision / response magnitude), so 'unit beats RE-k' no longer merely restates 'good selection beats random/best-single';
    report the per-letter JOINT (E1 AND selection) explicitly and rename the over-aggregating verdict; and disentangle the
    15-wide max-pool from the compact named unit by reporting the compact (named-members-only) unit's AUC alongside the 15-wide
    pool.
  approach: >-
    Re-run the first-letter two-track pipeline from art_RidEJtBC7gPT; for code reuse read the iter-3 first-letter re-run from
    its run-tree workspace path (3_invention_loop/iter_3/gen_art/gen_art_experiment_1/method.py and method_out.json) — SAE/loader/hook/firing
    identical; gate on reconstruction cosine>0.9. (1) M5 NON-RANDOM CONTROLS: from the cover-eligible set E, build three label-free,
    count-matched-to-k=|unit| selectors — (S-rec) top-k by content-flip recall, (S-prec) top-k by firing precision, (S-mag)
    top-k by mean response magnitude — max-pool each identically to the unit, and on every letter report held-out AUC plus
    the paired-bootstrap AUC-DIFFERENCE CI (B>=10,000, pair-cluster resampling) for unit-minus-each; RETAIN RE-k as the demoted
    floor. The set-cover-specific selection claim is ESTABLISHED only where the unit beats S-rec/S-prec/S-mag with CI excluding
    0; where it does not, scope the claim to 'cover-based eligibility + sensible selection'. Report a per-letter table of
    which controls the unit beats. (2) M4 ENDPOINT: compute and report the PER-LETTER JOINT of E1 (K-track recovers diagnostic
    parent + >=2 absorbers above the random-membership null) AND the selection test (unit AUC significantly above BOTH (h)
    AND the M5 non-random selectors), giving the honest intersection (currently {T,D}=2/5 vs RE-k; recompute vs the M5 bar).
    RENAME the emitted verdict so it does NOT imply mechanism+selection co-occur on 3 letters, and explicitly ANNOTATE letter
    I as 'selection win WITHOUT confirmed absorption mechanism' (E1 fails: recall-argmax anchor 1227 fires 0% on corpus).
    Keep the unsupervised parent-validation (firing-floor) step that rejects the spurious I anchor. (3) M7 COMPACT-vs-15-WIDE:
    report the AUC of the COMPACT unit (anchor + named precision-passing absorbers only, ~4-5 members) ALONGSIDE the 15-wide
    max-pool on every letter, with their AUC-difference CI, to show whether the named structure carries the classification
    signal or the strong AUC reflects the wide pool; tie this to the member-labeling fraction reported in the auditability-expansion
    experiment. (4) Use the 1,700-pair re-judged surface superset (art_YwjLYapklnVk) for the admission surface-invariance
    gate; report the false-admit rate under the matched random-k null. Move the torch 2.8+cu128 / AUC-drift reproducibility
    note to a repro appendix block, not the headline. Memory-safe batching; gradual scaling (mini letter-L -> full). Emit
    method_out.json (exp_gen_sol_out schema) with per-letter AUC for unit/compact-unit/15-wide/a/b/c/h/RE-k/S-rec/S-prec/S-mag,
    all AUC-difference CIs, the per-letter joint (E1 AND selection) table, the renamed reconciled verdict, admission stats,
    and per-example held-out predictions. Validate full/mini/preview <100MB.
  depends_on:
  - id: art_dpYpjSn2Xvg3
    label: dataset
    relation_type:
    relation_rationale:
  - id: art_YwjLYapklnVk
    label: surface-control
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
- id: experiment_iter4_dir5
  type: experiment
  objective: >-
    ROUTER AS A SCREENING HEURISTIC WITH MEASURED ERROR (M6). Re-present the a-priori firing-structure router so it leads
    with the COMBINED rule (low firing-Jaccard AND high parent recall-hole), reports the DERIVATION set (12 concepts) separately
    from the TRULY-PROSPECTIVE set, strengthens the prospective test by adding cheap new truly-held-out concepts, and is described
    as a screening heuristic with a measured error rate rather than a validated oracle — fixing the overstated 'validated
    prospectively across spelling/taxonomic/toxicity/sentiment/aspect' claim (the first three are the derivation set).
  approach: >-
    Re-run the uniform router pipeline from art_RidEJtBC7gPT; for code reuse read the iter-3 router from its run-tree workspace
    path (3_invention_loop/iter_3/gen_art/gen_art_experiment_4/method.py). (1) LEAD WITH THE COMBINED RULE: compute, per concept,
    the positive-only firing-Jaccard(detector,parent) AND the parent per-sub-context recall hole, and report the COMBINED
    router (predict absorption-regime iff firing-Jaccard < tau_J AND recall-hole > tau_h) as the PRIMARY recommendation; report
    the single-signal routers (firing-Jaccard alone balanced-acc ~0.917; recall-hole alone ~1.0) as ablations, explicitly
    noting that recall-hole alone is the stronger single separator so the headline must be the conjunction, not firing-Jaccard
    alone. (2) DERIVATION vs PROSPECTIVE SEPARATION: clearly label the 12 DERIVATION concepts (spelling L/O/T/I/D; numeric;
    taxonomic; toxicity threat/identity_attack/insult/obscene/sexual_explicit) and report rule-fitting (tau sweep, balanced
    accuracy, LOO=0.733) ONLY on them; report the TRULY-PROSPECTIVE concepts separately with their hit rate. (3) ADD CHEAP
    NEW PROSPECTIVE CONCEPTS: beyond the existing 3 held-out (sentiment, CEBaB food, CEBaB service), carve additional truly-held-out
    concepts at $0 from datasets already in hand — additional bias_in_bios profession concepts (art_21JWypIydPMX; e.g. nurse/attorney/surgeon
    as is-a-profession concepts) and additional civil_comments sub-attributes not used in derivation (art_8QO7pl6Pd8UQ) —
    PREDICT each concept's regime from the frozen combined rule BEFORE measuring the matched-pool unit-vs-(h)/(a) outcome,
    then report the expanded prospective hit rate and its CI. (4) FRAMING: describe the router as a 'screening heuristic with
    substantial measured error' (report the prospective error rate and LOO), NOT an oracle; keep the honest counterexamples
    (numeric high-Jaccard yet absorption-like; aggregated-taxonomic low-Jaccard yet co-firing because the parent already has
    ~0.95 recall). Reproduce the established firing-Jaccard values (spelling <0.05; toxicity ~0.40/0.29/0.66) as a sanity
    check. Memory-safe batching; gradual scaling (established concepts first to lock the derivation table, then the new prospective
    concepts). Emit method_out.json (exp_gen_sol_out schema) with the combined-rule definition + thresholds, the derivation
    table (separate), the expanded prospective table with predicted-vs-measured regime + outcome AUCs + CIs + hit flags, LOO
    accuracy, single-signal ablations, and honest_notes. Validate full/mini/preview <100MB.
  depends_on:
  - id: art_dpYpjSn2Xvg3
    label: dataset
    relation_type:
    relation_rationale:
  - id: art_t2uUbjSwpd3t
    label: dataset
    relation_type:
    relation_rationale:
  - id: art_8QO7pl6Pd8UQ
    label: dataset
    relation_type:
    relation_rationale:
  - id: art_21JWypIydPMX
    label: dataset
    relation_type:
    relation_rationale:
  - id: art_RidEJtBC7gPT
    label: method
    relation_type:
    relation_rationale:
- id: research_iter4_dir6
  type: research
  objective: >-
    Finalize positioning for the auditability-first headline and close the presentation/citation MINOR (M8) plus support the
    homograph scope (M3). Produce (1) a literature-grounded framing for 'absorption recurs on homograph/polysemous tokens
    whose general latent is suppressed' — confirm whether this homograph/polysemy characterization is novel relative to existing
    SAE-absorption work (which is spelling-only); (2) a novelty check + positioning for the KG-LOCALIZED SURGICAL SUB-CONCEPT
    EDIT (single-latent ablation/steering of one sub-context with side-effect/KL measurement vs a dense-probe edit that cannot
    localize) against SAE-steering/erasure/feature-editing literature, so the new headline's downstream task is correctly
    distinguished; and (3) a finalized, venue/version-accurate citation table for every 2025/2026-dated reference, completing
    the audit so the next paper draft can strip all rebuttal/iteration scaffolding and cite cleanly.
  approach: >-
    Use the aii-web-tools skill (search -> fetch -> fetch_grep), building on the iter-3 citation audit (art_i-tkvFCKneA-)
    so no work is duplicated. (1) HOMOGRAPH FRAMING: search for prior characterizations of WHEN feature absorption occurs
    (token frequency, polysemy, hierarchy depth) and for any SAE work on homograph/polysemous-token representation; confirm
    the spelling-only empirical scope of absorption (Chanin 2409.14507 NeurIPS 2025; SAEBench absorption_first_letter) and
    whether 'absorption recurs on polysemous/homograph tokens with suppressed general latents' is a novel empirical observation;
    draft a 2-3 sentence positioning paragraph. (2) SURGICAL-EDIT NOVELTY: survey SAE activation steering and concept erasure
    with side-effect/KL measurement (AxBench ICML 2025 2501.17148; feature steering/clamping; LEACE 2306.03819 erasure; any
    single-latent surgical-edit work) and confirm the distinction of CCRG's KG-LOCALIZED edit — using a knowledge-graph-named
    single absorber to surgically edit ONE sub-context while preserving the parent, a localization a single dense hyperplane
    structurally cannot achieve; draft cite-and-distinguish one-liners. (3) CITATION FINALIZATION: verify/lock the venue+version
    for every 2025/2026 citation (Chanin 'A is for Absorption' -> NeurIPS 2025; AxBench/SAEBench -> ICML 2025; CanonicalUnits
    2502.04878 -> ICLR 2025; MindTheGAP -> AISTATS 2024; SASA 2606.06333; Winnicki 2604.23829 observational-KG contrast; Muchane
    2506.01197; DPE/SCR-TPP as preprints), flag any that do not resolve, and emit a corrected BibTeX-ready table. (4) Provide
    an explicit note for the GEN_PAPER_TEXT step: strip all rebuttal/iteration/infrastructure scaffolding ('previous draft',
    'iter-3 re-runs', 'torch 2.8+cu128', verdict-reconciliation), move reproducibility to an appendix, and lead the paper
    with measured auditability. Emit research_out.json {answer, sources, follow_up_questions} + research_report.md with the
    homograph-framing paragraph, the surgical-edit cite-and-distinguish block, the finalized citation/venue table, and the
    presentation-strip checklist.
  depends_on:
  - id: art_i-tkvFCKneA-
    label: citations
    relation_type:
    relation_rationale:
expected_outcome: >-
  After this iteration the paper can stand on its UNIQUE, measured capability rather than a narrow within-SAE classification
  win, resolving all four reviewer MAJORs with executed evidence. From the auditability-expansion experiment: an EXPANDED
  set of KG-guided recall repairs (spelling + homograph-taxonomic + numeric sub-contexts) each beating a random-addition control
  with bootstrap CIs, multiplicity-controlled via BH (count surviving FDR<=0.05), a confirmed (k)-cannot-localize result,
  and member-labeling agreement vs null INCLUDING the fraction of the 15-wide first-letter members that receive a confident
  label — making auditability broad enough to be the headline. From the surgical-edit experiment: a concrete downstream demonstration
  that a KG-named single-latent edit surgically removes/steers ONE sub-context (Georgia; first-letter word-context) with high
  on-target effect and low collateral/KL, dominating a dense-probe edit (which cannot localize) on surgical selectivity, with
  a toxicity negative-pole confirming the capability is regime-scoped exactly as the router predicts — a unique capability
  a dense probe lacks, answering the scope MAJOR. From the taxonomic-fix experiment: the conflation removed by rebuilding
  the classification unit from the precision-passing diagnostic-corroborated absorbers (16009 Georgia etc.) via a precision-weighted/gated
  K-track, that unit's (likely stronger) Georgia AUC + RE-k-anchored + non-random-control selection, PER-EDGE KG-agreement
  (Georgia/Jordan/US separately) with corroboration honestly scoped to the descriptive Jordan edge unless the rebuilt unit
  corroborates Georgia, held-out per-member precision with fold disclosure, and a homograph-vs-non-homograph hole table establishing
  absorption-on-polysemous-tokens. From the first-letter experiment: the set-cover claim isolated against S-rec/S-prec/S-mag
  (or honestly scoped to 'eligibility + sensible selection'), the per-letter JOINT (E1 AND selection)=2/5 reported with a
  renamed honest verdict and I annotated as selection-without-mechanism, and the compact-vs-15-wide AUC disentangled. From
  the router experiment: the combined low-Jaccard-AND-high-recall-hole rule led as primary, derivation (12) vs truly-prospective
  (3+new) reported separately with measured error, framed as a screening heuristic not an oracle. From the research artifact:
  a novel homograph-absorption framing, a correctly-distinguished surgical-edit positioning, a finalized citation/venue table,
  and a presentation-strip checklist for the clean standalone draft. These become the executed evidence and building blocks
  for the next iteration's auditability-headlined paper and cross-family aggregation.
summary: >-
  The reviewer's two dominant MAJORs are: pivot the headline to measured auditability and EXPAND it, and fix the taxonomic
  unit/specialist conflation. This iteration executes six parallel, self-contained artifacts that do exactly that: (1) expand
  the KG-guided recall-repair loop + member-labeling with multiplicity control (new headline part 1); (2) add a KG-localized
  surgical sub-concept EDIT with on-target/collateral/KL side-effect measurement vs a dense-probe edit that cannot localize
  (new headline part 2 — the unique-capability downstream task); (3) fix the taxonomic conflation by rebuilding the unit from
  precision-passing diagnostic-corroborated absorbers via a precision-weighted K-track, with per-edge KG-agreement, held-out
  precision, and a homograph-scope characterization; (4) isolate set-cover from sensible label-free selection (S-rec/S-prec/S-mag),
  report the per-letter joint endpoint (2/5) with a renamed honest verdict, and disentangle the compact named unit from the
  15-wide pool; (5) reframe the router as a combined-rule screening heuristic with derivation-vs-prospective separation and
  new held-out concepts; (6) finalize the homograph/surgical-edit framing and citation/venue audit. Each experiment re-derives
  its units from the method dossier (re-encoding ~8 min, $0) and reads iter-2/iter-3 outputs from their run-tree workspace
  paths for code reuse and cross-check, turning a narrow over-claimed classification result into a defensible, auditable,
  EDITABLE absorption-regime-repair contribution with an a-priori router.
</previous_strategies>

<dependency_rules>
- depends_on is a list of objects {id, label} — each entry references an existing artifact and tags how it is being used
- "id" can ONLY reference IDs from <existing_artifacts> — never IDs you are proposing (all new artifacts run in parallel)
- "label" is a SHORT free-text type label (a word or two, NOT a sentence) describing what role the dep plays — e.g. "dataset", "validates", "extends", "supersedes". Required on every dep.
- Setting depends_on provides the dependency's out_dependency_files to your artifact at execution time
- If no suitable existing artifacts exist, use empty depends_on
- New artifact IDs are assigned by the system after submission — do not invent IDs for your proposed artifacts
</dependency_rules>

<available_artifact_types>
Artifact types you can plan. Use this to choose the right types for your strategy objectives.

<artifact_types>
RESEARCH
Web research to answer key questions — like a researcher making decisions.
Runtime: LLM Agent, no code execution.
Tools: the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text).
Capabilities: Find, synthesize, and compare information across sources; survey SOTA and best practices.
Deps: REQUIRED none | OPTIONAL other RESEARCH to build on prior findings

EXPERIMENT
Run code to test hypotheses, implement methods, and collect empirical results.
Runtime: Python 3.12, UV (any pip package), isolated workspace, gradual scaling (mini → full data).
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Implement and run any code-based experiment, compare method vs baselines.
Deps: REQUIRED at least one DATASET | OPTIONAL RESEARCH for methodology guidance

DATASET
Collect, prepare, and merge datasets for experiments and analysis.
Runtime: Python 3.12, UV, isolated workspace.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-hf-datasets (HuggingFace Hub — ML datasets, many UCI/OpenML/Kaggle mirrors), aii-owid-datasets (Our World in Data — global statistics), aii-json (schema validation). Also any Python source (sklearn.datasets, openml, direct URLs, APIs) — must verify within 300MB limit.
Capabilities: Search, acquire, transform, combine, and standardize data from any available source.
Deps: REQUIRED none | OPTIONAL RESEARCH for guidance on what data to collect

EVALUATION
Evaluate experiment results with metrics, statistical analysis, and validity checks.
Runtime: Python 3.12, UV (any evaluation library), isolated workspace, gradual scaling matching experiment.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Compute any quantitative metrics and statistical tests, analyze validity and robustness.
Deps: REQUIRED at least one EXPERIMENT | OPTIONAL DATASET if reference data needed

PROOF
Formally prove mathematical statements in Lean 4 with automated iteration.
Runtime: LLM agent with Lean 4 compiler feedback loop.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-lean (proof verification, Mathlib search, tactics: ring, linarith, nlinarith, omega, simp, etc.)
Capabilities: Formally verify properties and inequalities, iterative proof development, lemma decomposition.
Deps: REQUIRED none | OPTIONAL RESEARCH for mathematical background
</artifact_types>
</available_artifact_types>

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

RESEARCH executor scope:
  Output: research_out.json with {answer, sources, follow_up_questions} + research_report.md
  DOES: Web research — search, read, synthesize information from papers/docs/APIs into a structured report
  DOES NOT: Run code, download files, execute scripts, compute anything — no shell/Python access
  Use for literature surveys, API documentation, technical specifications — pure information gathering

EXPERIMENT executor scope:
  Output: method_out.json with results (metrics, predictions, analysis) — the core computational work
  DOES: Implement and run methods/algorithms, compute metrics, compare approaches, produce quantitative results
  DOES NOT: Collect new datasets (depends on DATASET artifacts for input data), write formal proofs
  This is the right artifact for any code that processes data and produces results

DATASET executor scope:
  Output: data_out.json with rows of {input, output, metadata_fold, ...} — raw data only, no derived computations
  DOES: Download/generate datasets, analyze candidates to pick the best ones, standardize to JSON schema (features, labels, folds, metadata), validate schema, split into full/mini/preview
  DOES NOT: Run experiments, train models, compute derived statistics (PID/MI/correlations/synergy matrices) as final output
  If you need to COMPUTE something from data (synergy matrices, MI scores, timing benchmarks), use an EXPERIMENT artifact instead

EVALUATION executor scope:
  Output: eval_out.json with evaluation results
  DOES: Any evaluation of experiment results — metrics, statistical tests, ablations, comparisons, visualizations, robustness checks, error analysis, etc.
  DOES NOT: Implement new methods (use EXPERIMENT), collect data (use DATASET)
  This is for analyzing experiment outputs from any angle

PROOF executor scope:
  Output: Lean 4 proof files (.lean) with verified theorems
  DOES: Write and verify Lean 4 formal proofs with Mathlib, iterative compilation
  DOES NOT: Run Python experiments, collect data, do empirical analysis
  Use only when formal mathematical guarantees are needed
</artifact_executor_scope>

<artifact_planning_rules>
RESEARCH: Plan early — findings guide dataset selection, experiment design, and methodology.
EXPERIMENT: Must depend on at least one DATASET. Define clear metrics and baselines before running. Consider trying multiple method variations rather than a single approach.
DATASET:
- Plan for REAL third-party datasets (HuggingFace, Kaggle, direct-download URLs) — downloadable within time and size constraints
- Describe dataset criteria (domain, size, format) — executors find exact sources, but you can suggest candidates or search directions
- ALWAYS prefer real datasets over synthetic. Synthetic is a LAST RESORT only when no suitable real data exists
EVALUATION: Must depend on at least one EXPERIMENT. Focus on statistical rigor and validity checks.
PROOF: Use only when the hypothesis requires formal mathematical guarantees. Lean 4 + Mathlib.
</artifact_planning_rules>

<existing_artifacts>
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
out_dependency_files:
  file_list:
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
out_dependency_files:
  file_list:
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

--- Item 7 ---
id: art_0ueMMR8Tt02P
type: experiment
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
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Item 8 ---
id: art_-o2RPMOZp37A
type: experiment
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
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Item 9 ---
id: art_QGSdsKY6U1vK
type: experiment
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
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Item 10 ---
id: art_YwjLYapklnVk
type: dataset
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

--- Item 11 ---
id: art_8AwUJK9qOwX_
type: experiment
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
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Item 12 ---
id: art_P8-3ipCuQwVY
type: experiment
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
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Item 13 ---
id: art_lvYKkaolutJG
type: experiment
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
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Item 14 ---
id: art_07ju05r0onqB
type: experiment
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
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Item 15 ---
id: art_jI2KIJotjzIU
type: experiment
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
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Item 16 ---
id: art_i-tkvFCKneA-
type: research
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
out_dependency_files:
  file_list:
  - research_out.json

--- Item 17 ---
id: art_sxwT7hK6YFEA
type: experiment
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
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Item 18 ---
id: art_0CZwPjG2YMCf
type: experiment
title: KG-Localized Surgical Sub-Concept SAE Edit with Side-Effect Measurement (M1b)
summary: |-
  M1b is the unique-capability downstream task for the auditability-first two-track CCRG units: using the emitted feature knowledge-graph (KG), edit EXACTLY ONE sub-context by ablating its single NAMED absorber latent, and show high on-target effect with near-zero collateral on sibling sub-contexts and a tiny token footprint -- a capability the standard non-SAE handle (a dense parent direction) structurally cannot provide. This directly supplies the goal's 'activation steering with side-effect measurement' and 'feature-based classification of safety-relevant attributes' evaluation on a frozen Gemma-Scope L12/16k JumpReLU SAE + gemma-2-2b (edit/read at blocks.12.hook_resid_post; gating cosine 0.919, L0 88, matching iter-3), $0 LLM, single GPU.

  OPERATORS (forward hooks on the edit layer): KG-ABL = single named-absorber ablation h-=lambda*z_l*W_dec[l] (gated by the latent's own sparse firing); DENSE-ABL = diff-of-means parent erasure h-=beta*(h.u)u (baseline f, the non-SAE difference-of-means / logistic probe direction); RAND = random firing-rate-matched content latent; KG-ADD = steering-toward; (k) = label-free JTT probe (structural: no per-sub-context latent to edit). PRIMARY measure is behavioral: per-context next-token KL divergence at the edited token's position (steering-with-side-effects). A frozen dense parent probe (logistic + diff-of-means, fit on a DISJOINT diagnostic fold) is the secondary instrument; because country/letter membership is redundantly encoded, its margin is huge & broad under DENSE-ABL but insensitive to single-latent edits -- which is WHY behavioral KL is the primary on-target signal. Selectivity = on_target/collateral at matched effect, with B=10,000 paired bootstrap CIs on on-target, collateral, and the dense-minus-kg collateral difference; a graded verdict separates a CLEAN surgical edit (selectivity>=20, off-target footprint<5%, dense>kg collateral CI excludes 0) from a partial/co-firing edit.

  RESULTS (method_out.json, 7 cases, 5 SURGICAL_EDIT_CONFIRMED): taxonomic Georgia->16009 selectivity ratio 1722x (on-target KL 0.0216, KG collateral 3e-5, dense collateral 0.0496, KG footprint 0.0015 vs dense 1.0, dense-kg collateral CI [0.036,0.066]); Jordan->540 (2722x) & 8347 (3247x); United States->846 (214x); first-letter large->8463 (802x). The low-precision US absorber 4760 is only PARTIAL_SURGICAL (7.8x) -- absorber precision predicts surgicality (honest negative). TOXICITY negative pole (insult->13367) is PARTIAL_CO_FIRING_AS_PREDICTED: firing-Jaccard 0.878, parent recall-hole 0.0, selectivity 2.4x, footprint 0.117 -- single-latent ablation is NOT cleanly surgical because the sub-attribute co-fires with the parent, exactly as the firing-Jaccard/recall-hole router predicts. The regime router map cleanly splits absorption (n=6: mean selectivity 1452x, jaccard 0.014, footprint 0.0036) from co-firing (selectivity 2.4x, jaccard 0.878, footprint 0.117) -- a ~600x split. RAND raw-latent on-target ~0 (cannot reach matched); the (k) probe's decoder-projection argmax is the parent latent, never a KG absorber (no per-sub-context handle).

  OUTPUT DATASETS (exp_gen_sol_out, 409 examples, every example has predict_* per method): (1) edit_locality_per_context (402 rows) -- one labeled held-out context each: output=ON_TARGET (an X-context the edit SHOULD change) vs OFF_TARGET_SIBLING (a sibling it should NOT), with predict_kg_abl / predict_dense_abl / predict_rand = AFFECTED/UNAFFECTED from each operator's behavioral KL at full edit (lambda=1/beta=1); KG-ABL marks 0 of N siblings AFFECTED while DENSE-ABL marks nearly all (the collateral signature), RAND ~0 everywhere; (2) kg_surgical_edit_per_case (7 rows) -- output=SURGICAL_EXPECTED/NON_SURGICAL_EXPECTED by regime, predict_kg_abl=verdict, predict_dense_abl=HIGH/LOW_COLLATERAL, predict_*_selectivity. Rich aggregates live in metadata (per_case curves/matched/selectivity_CIs, summary.regime_router_map, k_localization_check, honest_negatives).

  DELIVERABLES: method.py (self-contained; reuses iter-2/iter-3 JumpReLUSAE/ModelBundle/encode_rows/k_localization_check/bootstrap + canonical units/KG read from iter-3 method_out.json; genuinely-new code = edit operators + behavioral side-effect measurement + per-context prediction rows); method_out.json + full/mini/preview_method_out.json (all schema-valid against exp_gen_sol_out, <500KB each); README.md; pyproject.toml (exact pinned versions, torch 2.6.0+cu124). Downstream paper can cite the surgical-edit ratios, the dense-baseline per-context collateral, the (k) no-handle result, and the firing-Jaccard router map as the auditability headline's concrete downstream payoff.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Item 19 ---
id: art___vgSpUe6wAF
type: experiment
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
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_3
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Item 20 ---
id: art_JMA2gBvnakAm
type: experiment
title: >-
  Two-Track CCRG Selection Isolation: Non-Random Selectors, Firing-Floor, Compact Unit
summary: |-
  Iter-4 re-runs the frozen-SAE first-letter two-track Counterfactual Co-Response Grouping (CCRG) pipeline (Gemma-Scope L12/16k JumpReLU SAE on unsloth/gemma-2-2b, hook blocks.12, gating cosine 0.924 / EV 0.857) verbatim from iter-3 and adds three honest-scoping deltas; $0 LLM spend, B=10,000, ~14 min on one GPU. Method = K-track anchored greedy set-cover unit (anchor + per-token absorbers). Baselines held constant: raw single latent (a), co-fire/decoder clusters (b,c), oracle attribution top-k (h), and the demoted random-eligible-k floor (RE-k). M5 (decisive new core): three NON-RANDOM, label-free, count-matched-to-k selectors over the SAME cover-eligible set Lr -- S_rec (top-k by content-flip recall), S_prec (top-k by firing precision), S_mag (top-k by mean magnitude) -- max-pooled identically to the unit, so unit-minus-each isolates the set-cover SELECTION rule from sensible label-free selection; reported as paired-bootstrap AUC-difference CIs (pair-cluster resampling). M4: an unsupervised firing-floor anchor validation (a valid parent anchor must fire >=5% on held-out corpus) plus a per-letter JOINT (E1 AND selection) and a renamed verdict. M7: the compact named unit (anchor + diagnostic-corroborated absorbers, cap 5) vs the full 15-wide max-pool, with an AUC-difference CI, an anchor_only floor, and an AUC-vs-cumulative-k curve.

  RESULTS (L,O,T,I,D). primary_endpoint = REFRAMED_TO_ELIGIBILITY_AND_SENSIBLE_SELECTION (n_E1_pass=5, n_joint=2, n_selection_vs_M5=2, n_eligibility_only=2). M4 firing-floor RECOVERED letter I: its recall-argmax anchor 1227 fires 0% on corpus; the validated anchor 1634 (fires 20.6%) IS the form-free-diagnostic parent, so E1 now PASSES for I (5/5 overall, up from iter-3's 4/5); L/O/T/D anchors unchanged (already fire >0.26). M5 selection isolation: the set-cover-specific selection is established only on I and D (unit beats h AND all three non-random selectors, CIs exclude 0); on L/O/T the strong S_rec (top-k by recall, which picks the anchor + highest-coverage latents) matches the unit, so the win there is cover-based eligibility + sensible selection, not set-cover-specific. Per-letter unit AUC (vs h): L .905(.795) O .917(.819) T .858(.647) I .983(.735) D .956(.727). Pooled across letters the unit beats h by 0.188 (CI .148-.223), S_rec by 0.109 (.077-.143), S_prec by 0.273, S_mag by 0.120 (all pooled CIs exclude 0), but per-letter S_rec is significant on only 2/5. M7: the compact named unit (k=5) is SIGNIFICANTLY BELOW the 15-wide pool on every letter ( delta AUC -0.056 to -0.200, CIs exclude 0) -- the diagnostic-uncorroborated absorbers carry real classification signal, so human-auditable compactness costs AUC; reported, not hidden. E2 (absorbed-slice recall) passes only on T. The iter-3 over-aggregating rule (E1 AND unit>h AND RE-k on >=3/5) would have declared ABSORPTION_REPAIR_SELECTION_CONFIRMED (RE-k is an easy floor: median draw AUC 0.63-0.69, frac_rek>=unit <=0.008); this is recorded under legacy_iter3_verdict and contrasted.

  FAITHFULNESS/HARDWARE: this run is on RTX 2000 Ada (sm_89); iter-3 ran on RTX 5090 (sm_120). The UNMODIFIED iter-3 method.py was re-run on this host and produced numbers IDENTICAL to this iter-4 run for L (unit AUC 0.905, K_UNIT ending in latent 1566, RE-k mean 0.651), confirming the additive M4/M5/M7 code does not perturb the pipeline (M5/M7 use separate child rngs; the firing-floor corpus encode consumes no shared rng). Differences from the stored iter-3 anchors (L unit 0.876, member 1362) are bf16 hardware numerics breaking a discrete greedy set-cover tie at L's 15th member -- documented in metadata.repro_appendix.

  OUTPUT (schema exp_gen_sol_out, {metadata, datasets}, all variants <0.7MB). metadata.per_letter[X] carries anchor_validation, E1, E2, C1 (per_method AUC for unit/a/b/c/h/REk/S_rec/S_prec/S_mag/unit_compact/unit_15wide/anchor_only + auc_diff CIs), selection_isolation, compact_vs_wide (auc_by_k curve, compact_minus_15wide CI), admission, kg_edges, unit_definition. metadata.verdicts carries primary_endpoint, per_letter_joint, set_cover_isolation_table, compact_vs_wide_table, letter_I_annotation, legacy_iter3_verdict, and pooled_across_letters (unit_vs_h/REk/S_rec/S_prec/S_mag stratified-bootstrap + inverse-variance meta). datasets = one group per letter of held-out test-fold rows with predict_{unit,a,b,c,h,REk,S_rec,S_prec,S_mag,unit_compact,unit_15wide,anchor_only}. For the paper: the headline is the honest reframe (cluster-level units beat raw latents and attribution and a random-eligible floor, but the set-cover-SPECIFIC win over strong non-random selectors holds only on 2/5 letters), plus the M4 firing-floor anchor fix and the M7 auditability-vs-AUC tradeoff.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_4
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Item 21 ---
id: art_GTc_f26dMzFs
type: experiment
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
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_5
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Item 22 ---
id: art_QBxBPF-9Ldxe
type: research
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
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
out_dependency_files:
  file_list:
  - research_out.json
</existing_artifacts>

<current_paper>
The current paper draft — represents the research story so far.

Use this to understand what's working, what's not, and what gaps remain.
Gaps and weak results signal what to try differently — not what to conclude.

# Introduction

Sparse autoencoders (SAEs) decompose the activations of large language models (LLMs) into a dictionary of sparsely-activating latents intended to be interpretable, monosemantic units of analysis \citep{Cunningham2023, Bricken2023, Templeton2024}. The appeal is operational: a latent that reliably tracks a human concept can be read off as a classifier, flipped as a steering knob, or compared across model variants. Public SAE suites such as Gemma Scope \citep{Lieberum2024} expose millions of such latents over open models, making this a practical interface for safety-relevant interpretability.

This appeal is undercut by a now well-documented fact: \emph{single SAE latents are not reliable units} \citep{Leask2025}. Two failure modes recur. \emph{Feature splitting} fragments one concept across many latents, so no single latent captures it. \emph{Feature absorption} is more insidious: a more specific child latent suppresses the firing of a more general parent, leaving the parent with unpredictable holes on exactly the sub-contexts the child covers; parent and child become \emph{mutually exclusive in firing} \citep{Chanin2024}. (A related failure, \emph{feature hedging}, merges correlated features into one polysemantic latent in narrow SAEs \citep{Chanin2025}; a hedged latent is not groupable and is out of scope.) On concrete downstream tasks the cost is stark: difference-of-means probes are the strongest concept detectors and raw-latent SAE methods are uncompetitive \citep{Wu2025, Kantamneni2025}, while standardized suites quantify absorption, sparse probing, and targeted erasure \citep{Karvonen2025}. Any method proposing SAE latents as a knowledge representation must clear strong simple baselines and address splitting and absorption head-on.

The task is hard because the obstacles defeat the obvious instruments \emph{by construction}. The intuitive fix for an unreliable single latent is to group several latents into a cluster-level unit. But every existing post-hoc grouping signal is \emph{observational}: which latents fire together (co-activation feature families \citep{ONeill2024, Deng2025}) or which decoder directions point alike. Absorption is precisely the regime where observational signals must fail---the parent and the absorbing child are mutually exclusive in firing, so co-activation can never group them, and their decoders need not be cosine-similar \citep{Chanin2024}. The standard \emph{supervised} remedy, selecting the top-$N$ latents by causal effect on a concept probe (SCR/TPP attribution \citep{Karvonen2024, Marks2024}), is no better: a latent that fires only in a narrow sub-context has low \emph{marginal} attribution and is silently dropped, even though it carries the concept there. The latents one most needs are exactly the ones these instruments discard.

Why has this not been solved post-hoc? Recent architectural remedies---Matryoshka SAEs \citep{Bussmann2025}, hierarchical SAEs \citep{Muchane2025}, and subspace-aware SAEs \citep{Dalili2026}---all \emph{retrain} the SAE to reduce splitting and absorption at training time, and do not help a practitioner holding a frozen public SAE. We take the opposite stance: a \emph{training-free, post-hoc repair of frozen public SAEs}. The methodological gap we fill is the \emph{grouping operator}. Grouping by \emph{interventional co-response}---how latents jointly track a content counterfactual, rather than how they co-fire at baseline---is the matched instrument, with a direct precedent in systems biology, where differential co-expression methods (DiffCoEx \citep{Tesson2010}, WGCNA \citep{Zhang2005}) cluster genes by correlated response to a perturbation precisely because co-regulated genes are often not co-expressed at baseline. Crucially, correlation is the right operator only for the \emph{shared-support} splitting case. Absorbers respond on \emph{disjoint} supports and have low pairwise correlation, so no affinity-merging clustering can even \emph{propose} the right group. The disjoint-support case is a \emph{maximum-coverage} problem, whose classic greedy solution \citep{Nemhauser1978, Feige1998} is the natural---and, we argue, the only correct---proposer for absorption units.

We introduce \textbf{Two-Track Co-Response Grouping (CCRG)} and execute it on a frozen Gemma Scope SAE. We deliberately do not stake the contribution on out-classifying a strong dense probe, because on aggregate detection no raw-latent SAE method does \citep{Wu2025}; our own results confirm this on every task we measure. Instead, the contribution is what a cluster-level unit and its \emph{feature knowledge graph} can do that a single dense hyperplane structurally cannot: \emph{measured, localized, auditable repair}. Four findings result. (1) The emitted knowledge graph carries \emph{measured} editorial utility: across three concept families, 30 KG-named absorber additions recover a suppressed parent's recall hole and survive a Benjamini--Hochberg false-discovery control over all 69 tested repairs, beating a random-addition control; and ablating a single KG-named absorber surgically edits exactly one sub-context with a $1452\times$ median selectivity over collateral, a localization a dense parent direction cannot provide [ARTIFACT:art_sxwT7hK6YFEA] [ARTIFACT:art_0CZwPjG2YMCf]. (2) A one-forward-pass measurement---low firing-Jaccard \emph{and} a parent recall hole---is an a-priori \emph{router} that predicts which regime a concept is in before any grouping, with a measured (not perfect) error rate [ARTIFACT:art_07ju05r0onqB]. (3) Non-spelling absorption is real but \emph{narrow}: it recurs on homograph tokens whose general parent is suppressed (Georgia, Jordan), and once the unit is rebuilt from precision-passing specialists, its set-cover \emph{selection} beats every label-free selector at matched pool size [ARTIFACT:art___vgSpUe6wAF]. (4) On first-letter spelling, the same selection is isolated against three non-random label-free selectors; the set-cover-specific win holds on two of five letters, which we report exactly [ARTIFACT:art_JMA2gBvnakAm].

[FIGURE:fig1]

\paragraph{Summary of contributions.}
\begin{itemize}
\item \textbf{A two-track grouping algorithm} (\S\ref{sec:method}): a training-free procedure that proposes split families by content-response correlation (C-track) and absorption units by a \emph{precision-gated} anchored greedy set-cover (K-track), reconciled and filtered by a single null-anchored, multiplicity-controlled admission rule. To our knowledge maximum-coverage set-cover has not previously been used to group SAE latents.
\item \textbf{Measured auditability as the headline} (\S\ref{sec:audit}): a KG-guided recall-repair loop (30 repairs surviving FDR control across spelling, taxonomic, and numeric families), a KG-localized single-absorber \emph{surgical edit} with side-effect measurement, and LLM member-labeling---each beating a null control on a dimension a dense probe lacks.
\item \textbf{An a-priori firing-structure router} (\S\ref{sec:router}) that predicts when grouping helps, reported as a screening heuristic with its measured error, separating a 12-concept derivation set from a 3-concept prospective test.
\item \textbf{Honestly-scoped within-SAE selection} (\S\ref{sec:selection}): a precision-rebuilt taxonomic homograph unit whose set-cover selection beats all label-free selectors, and a first-letter analysis reporting the per-letter joint of mechanism and selection ($2/5$) against non-random controls.
\item \textbf{Four frozen testbeds, a single-GPU pipeline, and a dedicated account of failure modes} (\S\ref{sec:setup}, \S\ref{sec:negatives}): a co-firing toxicity regime where CCRG does not help, an unconfirmed numeric hierarchy, no dense-probe out-classification on any task, and a confound-bounded null model-diffing result.
\end{itemize}

# Related Work
\label{sec:related}

\paragraph{SAEs and the unreliability of single latents.} Sparse dictionary learning on LLM activations yields interpretable features \citep{Cunningham2023, Bricken2023, Templeton2024, Lieberum2024}, but a growing body of work shows individual latents are not canonical units \citep{Leask2025}. \citet{Chanin2024} introduce and quantify \emph{feature absorption}---a specific child latent suppresses a general parent's firing---demonstrated on first-letter spelling, and \citet{Chanin2025} characterize \emph{hedging}. Benchmarks make the practical cost concrete: AxBench finds difference-of-means strongest and raw-latent SAE methods uncompetitive \citep{Wu2025}; a sparse-probing case study reaches the same conclusion \citep{Kantamneni2025}; and SAEBench standardizes absorption, sparse-probing, and erasure evaluations \citep{Karvonen2025}. We adopt this as our honest bar: our load-bearing claim is not out-classifying a dense probe but delivering an auditable, editable repair a probe cannot.

\paragraph{Post-hoc grouping of SAE features.} Prior grouping is observational: co-activation ``feature families'' \citep{ONeill2024} and sparse feature coactivation modules \citep{Deng2025} group latents by what fires together or which decoders align. Closest to our output, \citet{Winnicki2026} build a feature-level knowledge graph from SAE features, but its edges come from three purely observational sources---corpus co-occurrence weighted by Jaccard overlap of binary presence matrices, a transcoder cross-layer mechanism graph, and contrastive domain filtering---with no interventional signal. Such edges cannot, by construction, express CCRG's central relation: CCRG joins a country anchor latent to a Georgia specialist that is \emph{mutually exclusive in firing} with it (firing-Jaccard $<0.05$). A Jaccard co-occurrence edge between them is $\approx 0$ by definition, decoder geometry need not relate them, and a cross-layer transcoder graph encodes inter-layer pathways rather than within-layer firing-complementarity. CCRG's edge is interventional---the two latents track the same content counterfactual on disjoint supports. We count-match observational clusters to our unit's size so any classification comparison reflects \emph{selection}, not capacity.

\paragraph{Supervised latent selection and word-sense evaluation.} SHIFT and the SCR/TPP family rank individual latents by causal effect on a concept probe and ablate the top-$N$ \citep{Marks2024, Karvonen2024}; a latent firing only in a narrow sub-context has low marginal attribution and is silently dropped---the exact gap our co-response set-cover fills. We use SCR/TPP-style ranking as our oracle-pool baselines (g)/(h). Separately, PS-Eval \citep{Minegishi2025} asks whether SAE features \emph{separate the senses} of polysemous words; it never studies the absorption failure mode, a suppressed parent, or a recall hole, and is a clean cite-and-distinguish rather than a precedent for our homograph-absorption finding.

\paragraph{Architectural remedies and concept editing.} Matryoshka \citep{Bussmann2025}, hierarchical \citep{Muchane2025}, and subspace-aware \citep{Dalili2026} SAEs modify \emph{training} to reduce splitting/absorption; we repair a \emph{frozen} public SAE post-hoc. For our edit demonstration, SAE-TS \citep{Chalnev2024} and SRS \citep{He2025} select a whole \emph{concept} feature with a tuned coefficient; LEACE \citep{Belrose2023} is dense whole-concept erasure that cannot localize to a sub-context; and SAE concept-unlearning work targets text-to-image diffusion \citep{Cywinski2025}. None edits a single \emph{absorber} latent named by an interventional feature-graph edge to recover or change one sub-context while preserving the parent. AxBench \citep{Wu2025} is both our side-effect/fluency evaluation template and our honest concession that diff-of-means beats SAEs on aggregate steering.

\paragraph{Cross-field instruments and robustness.} The C-track imports differential co-expression module discovery \citep{Tesson2010, Zhang2005} and Leiden community detection \citep{Traag2018}; the K-track imports the maximum-coverage greedy with its $(1-1/e)$ guarantee \citep{Nemhauser1978, Feige1998}. The robustness framing engages label-free worst-group-robustness work---group-DRO \citep{Sagawa2019}, JTT \citep{Liu2021}, GEORGE \citep{Sohoni2020}, EIIL \citep{Creager2020}, LfF \citep{Nam2020}, group-aware priors \citep{Rudner2024}, and diverse prototypical ensembles \citep{To2025}---which infer groups over \emph{examples} and \emph{retrain}; CCRG groups \emph{features}, never retrains, and the recovered absorbers \emph{are} the inferred sub-context specialists. Surface invariance draws on LEACE \citep{Belrose2023} and counterfactual invariance \citep{Veitch2021}; minimal-pair supervision draws on counterfactually-augmented data \citep{Kaushik2019}, CEBaB \citep{Abraham2022}, and ParaDetox \citep{Logacheva2022}. The closest ``cluster counterfactual differences'' template is CDLC in vision \citep{Varshney2025}, which clusters diffusion-counterfactual difference vectors into one continuous direction per class; we cluster \emph{discrete} LLM SAE latents into multi-member units and add a set-cover track for which CDLC has no analogue.

# The Two-Track Co-Response Grouping Method
\label{sec:method}

\paragraph{Preliminaries.} Let the frozen SAE have latents $l \in \{1,\dots,L\}$ with encoder activation $a_l(x)$; a latent \emph{fires} on $x$ iff $a_l(x) > 0$ (Gemma Scope uses a JumpReLU, so the threshold is inside the encoder \citep{Lieberum2024}). For a concept $c$ we are given \emph{content-flip minimal pairs} $(x_{\text{off}}, x_{\text{on}})$ in which the concept is absent/present at matched surface form, plus \emph{surface-flip pairs} in which the concept is held constant and surface varies. Content labels are the supervision every matched baseline consumes; the method uses no absorption-specific oracle. We encode at one residual-stream site (\texttt{gemma-2-2b}, layer 12, width 16k canonical; $d_{\text{model}}=2304$, $16{,}384$ latents).

\paragraph{Step 1: interventional content-response and cover sets.} For each latent $l$ and pair $p$, the \emph{content-response} is $r_l(p) = a_l(x_{\text{on}}) - a_l(x_{\text{off}})$. A latent's \emph{cover set} $C_l$ is the set of pairs whose content flip it tracks reliably ($r_l(p)>\tau_{\text{resp}}$ and $a_l(x_{\text{on}})>0$) and precisely (firing-precision $\geq 0.7$ on its own support). Because absorbers fire on only a handful of words, a mean-over-pairs prefilter would discard them; eligibility is therefore \emph{cover-based} (selective \emph{and} covering $\geq 1$ sub-context), retaining the genuinely sparse absorbers. We denote the cover-eligible set $E$.

[FIGURE:fig2]

\paragraph{Step 2: C-track --- correlation communities for splitting.} Where a concept \emph{splits}, sub-latents share firing support and co-respond positively, so pairwise affinity is appropriate. We build a sign-aware soft-thresholded affinity from the positive part of the Spearman correlation between response profiles, $A^{C}_{l,l'} = \max(\rho(r_l, r_{l'}), 0)^{\beta}$ with $\beta=6$ (WGCNA's scale-free criterion \citep{Zhang2005}), and run Leiden community detection (RBConfiguration partition \citep{Traag2018}), with resolution fixed by bootstrap-ARI stability against a shuffle null.

\paragraph{Step 3: K-track --- precision-gated anchored set-cover for absorption.} Absorbers respond on \emph{disjoint} supports and are mutually exclusive in firing with their parent, so their pairwise correlation is low and no affinity-merging clustering can propose them (Figure~\ref{fig:tracks}). We use an anchored greedy maximum-coverage procedure. \textbf{(1) Anchor:} $l^\* = \arg\max_l |C_l|$, the highest-recall ``parent'' candidate, chosen using \emph{only} the pairs and \emph{not} the absorption diagnostic. An \emph{unsupervised parent-validation} step then requires the anchor to fire on the held-out corpus above a floor (we use $5\%$); this rejects a spurious high-cover-set latent that fires $0\%$ on the corpus rather than crowning it anchor. \textbf{(2) Holes:} $H = P \setminus C_{\text{anchor}}$, the pairs the parent goes silent on. \textbf{(3) Greedy cover:} while $H$ is non-empty and improving, add $\arg\max_l |C_l \cap H|$ subject to mutual exclusivity (firing-Jaccard $<0.1$ with members), per-member precision $\geq 0.7$, and a marginal-coverage-gain floor $\geq 0.05$ whose bootstrap CI excludes $0$. A pure maximum-coverage objective will, however, prefer a high-coverage low-precision latent over a high-precision specialist that covers the same hole; we therefore add a \emph{per-sub-context precision gate} (equivalently, a precision-weighted coverage objective $\text{precision}\times\text{coverage}$), evaluated on a held-out fold, so the selected absorber is the precise specialist rather than the broad latent. The greedy max-coverage choice is the classic instrument for ``cover a universe with complementary specialists'' \citep{Nemhauser1978, Feige1998}; coverage-complementarity is a set-level property a pairwise operator cannot express.

\paragraph{Step 4: reconciliation.} For each C-community we designate its highest-recall member as a candidate anchor and run Step 3 to pull in mutually-exclusive absorbers covering its holes; we also seed Step 3 from standalone high-recall latents in no dense community. A final unit is a pure C-community (splitting), a pure K-cover (absorption), or a hybrid; we de-duplicate by highest coverage gain.

\paragraph{Step 5: admission filter with multiplicity control.} A proposed unit is admitted iff it clears \textbf{signature C} (within-unit content-response correlation above the 95th-percentile shuffle null) \textbf{or signature K} (pooled-max minus best-single content-response AUC above the 95th percentile of a best-of-random-$k$ null \emph{matched on marginal AUC}, plus the $k\in\{2,3\}$ absolute gain floor of $0.05$ with bootstrap CI excluding $0$, plus mutual exclusivity and the precision floor), \textbf{and} unit-level surface invariance (pooled surface-response not above the shuffled-surface null). Because many candidate units are tested per concept, we control multiplicity at the \emph{unit-proposal} level: a Bonferroni-within-unit $p$ over the disjunctive signature, then Benjamini--Hochberg across the $M$ candidate units, reporting $M$ and the empirical family-wise false-admit rate under the matched random-$k$ null.

\paragraph{Non-circular diagnostic and auditable graph.} Specialization edges are \emph{scored}, never formed, by the absorption diagnostic of \citet{Chanin2024}. Because the strict form needs an output logit, we use the domain-agnostic \emph{form-free} variant (the probe-projection implemented in SAEBench as \texttt{absorption\_fraction}): $l$ absorbs iff $\tau_c < (\hat{a}_l \cdot d_p)/(a \cdot d_p)$, with $d_p$ a parent-concept probe trained on data \emph{disjoint} from clustering. The anchor is chosen by recall available to every baseline, so a label-free unit beating a supervised oracle is not undercut. Each admitted unit is emitted with logit-lens tokens and top conditioning contexts, plus directed anchor$\to$child specialization edges---a feature-level knowledge graph.

\paragraph{The a-priori router.} Before any grouping, one forward pass yields two label-free signals per concept: (i) the positive-only firing-Jaccard between each per-sub-context detector and the parent, and (ii) the parent's per-sub-context recall holes. The screening rule predicts the \emph{absorption regime} (where grouping helps) iff firing-Jaccard is low \emph{and} the parent has a recall hole, and the \emph{co-firing regime} (where supervised attribution wins and CCRG should not be used) otherwise.

# Testbeds, Baselines, and Protocol
\label{sec:setup}

\paragraph{Constructed testbeds.} We built four frozen, schema-standardized families (Table~\ref{tab:testbeds}) totalling $109{,}754$ examples. All are pure text/data artifacts---no SAE or model weights baked in---so absorption presence is an empirical question for the SAE run, not a construction artifact. Words for the spelling and non-spelling hierarchies are anchored in the real \texttt{gemma-2-2b} vocabulary and a pinned Pile revision, so they never derive from the latents being grouped. The first-letter testbed contributes $17{,}180$ examples over five letters (L/O/T/I/D) [ARTIFACT:art_dpYpjSn2Xvg3]; the non-spelling testbed contributes $24{,}128$ examples over a numeric-quantity hierarchy and a taxonomic is-a-country hierarchy [ARTIFACT:art_t2uUbjSwpd3t]; the toxicity family contributes $37{,}707$ examples from ParaDetox \citep{Logacheva2022} and civil\_comments \citep{Borkan2019} [ARTIFACT:art_8QO7pl6Pd8UQ]; and a supporting family contributes $30{,}739$ examples of CAD-IMDB sentiment \citep{Kaushik2019}, CEBaB aspect-sentiment \citep{Abraham2022}, and a bias\_in\_bios boundary-null \citep{DeArteaga2019} [ARTIFACT:art_21JWypIydPMX].

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

\paragraph{Baselines.} We compare CCRG units against fifteen baselines (Table~\ref{tab:baselines}), spanning raw latents, observational clusters (count-matched), dense probes (including a LEACE surface-invariant hyperplane), supervised oracle pools, label-free/oracle group-robustness probes, a random-eligible-$k$ pool (the easy floor), and---decisively---three \emph{non-random, label-free, count-matched} selectors (S-rec, S-prec, S-mag). The design isolates \emph{selection at matched pool size}: a unit win over (h) holds capacity fixed and varies how members are chosen; a unit win over (RE-$k$) holds eligibility and pooling fixed; and a unit win over the three S-selectors is what isolates the \emph{set-cover-specific} rule from any sensible label-free ranking.

\begin{table}[t]
\centering
\small
\caption{Baseline glossary. (b)/(c) are count-matched to the unit's member count $k$; (h) is count-and-pool-matched; (RE-$k$) is the random-eligible floor; (S-rec)/(S-prec)/(S-mag) are non-random label-free selectors count-matched to $k$.}
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
(RE-$k$) & Random-eligible-$k$ pool: $k$ latents drawn at random from $E$, max-pooled \\
(S-rec) & \textbf{Top-$k$ by content-flip recall} \\
(S-prec) & \textbf{Top-$k$ by firing precision} \\
(S-mag) & \textbf{Top-$k$ by mean response magnitude} \\
\bottomrule
\end{tabular}
\end{table}

\paragraph{Statistics.} The primary statistical object is the per-concept paired bootstrap of the AUC difference ($B=10{,}000$, resampling whole content-flip pairs as clusters on the held-out test fold), with exact McNemar confirmatory tests and Holm--Bonferroni across headline claims; any accuracy comparison uses a comparison-matched Youden threshold so no baseline collapses to predict-all-positive. Encoding, gating, hardware, and software pins are deferred to Appendix~\ref{sec:repro}.

# Measured Auditability: The Editable Feature Knowledge Graph
\label{sec:audit}

Because no SAE unit out-classifies a strong dense probe (a fact we confirm throughout), the method's distinctive value is the auditable, editable structure a probe lacks. We make this the load-bearing result and measure it three ways.

\paragraph{KG-guided recall repair, with multiplicity control.} For every eligible under-served sub-context---a recall hole where the parent goes silent---the knowledge graph names a covering absorber on a \emph{selection} split (argmax recall over content-responsive latents with firing-Jaccard $<0.1$ and held-out sub-context precision $\geq 0.7$ versus the anchor). We add it to the anchor (max-pool) and measure recall recovery on a disjoint held-out evaluation split against a control that adds the full population of other content-responsive latents, with a paired bootstrap ($B=10{,}000$) and a one-sided $p$-value. Across all three families, $69$ repair variants over $54$ holes enter one Benjamini--Hochberg family; \textbf{30 survive FDR $\leq 0.05$} (statsmodels-confirmed) [ARTIFACT:art_sxwT7hK6YFEA]. By family: homograph-taxonomic $6$ (Georgia $0.20\!\to\!1.00$, gain $+0.80$; Jordan $0.29\!\to\!1.00$, $+0.65$; United States $0.77\!\to\!0.99$, $+0.21$ [ARTIFACT:art_lvYKkaolutJG]), \emph{numeric} $10$ (date $+0.68$, ordinal $+0.53$, decimal $+0.45$, year $+0.35$, comma\_number $+0.24$, currency $+0.14$---absorption-repair generalizing beyond spelling), and spelling $14$ (e.g.\ T-words \texttt{that/their/there/then/those/three/through} $+1.0$; O \texttt{our} $+1.0$, \texttt{one} $+0.96$; L \texttt{like} $+1.0$, \texttt{law} $+0.78$). Nine honest negatives are emitted verbatim: numeric \emph{integer} ties the control ($+0.007$); first-letter O (\texttt{on/out/over/own}) and T (\texttt{this/think/time}) tie; and the letter-I anchor fires $0\%$ on the corpus and is auto-flagged spurious (repair N/A).

[FIGURE:fig3]

\paragraph{A dense probe cannot localize the fix.} The label-free group-inference probe (k) (JTT: ERM $\to$ upweight the hardest set $\to$ retrain) yields a dense hyperplane whose decoder-projection argmax is the \emph{parent} on every concept and never a KG absorber. So (k) classifies the holes (recall $1.0$) but exposes \emph{no} addable per-sub-context latent, whereas the KG names exactly one. The editable, single-latent repair is a capability the dense probe structurally lacks.

\paragraph{A KG-localized surgical sub-concept edit.} The sharpest demonstration of localization is an \emph{edit}: ablating the single KG-named absorber, $h \leftarrow h - \lambda\, z_l\, W_{\text{dec}}[l]$ (gated by the latent's own sparse firing), versus erasing the dense diff-of-means parent direction $h \leftarrow h - \beta (h\cdot u) u$. We measure the per-context next-token KL divergence at the edited token (on-target) and on sibling sub-contexts (collateral), and report \emph{surgical selectivity} $=$ on-target/collateral at matched effect with paired-bootstrap CIs [ARTIFACT:art_0CZwPjG2YMCf]. For every high-precision absorber the single-latent ablation is surgical: Georgia$\to$latent $16009$ achieves selectivity $1722\times$ (on-target KL $0.0216$, KG collateral $3\!\times\!10^{-5}$, dense collateral $0.0496$, KG token footprint $0.15\%$ vs.\ dense $100\%$; dense$-$KG collateral CI $[0.036,0.066]$), Jordan$\to$540 ($2722\times$) and $\to$8347 ($3247\times$), United States$\to$846 ($214\times$), and first-letter \texttt{large}$\to$8463 ($802\times$). The low-precision US absorber $4760$ is only partially surgical ($7.8\times$): absorber precision predicts surgicality. The regime map is clean: absorption cases ($n=6$) average selectivity $1452\times$ at firing-Jaccard $0.014$ and footprint $0.4\%$, whereas the co-firing toxicity pole (\texttt{insult}$\to$13367, firing-Jaccard $0.878$, no parent hole) collapses to $2.4\times$ with footprint $11.7\%$---a $\sim\!600\times$ split that the firing-Jaccard/recall-hole router predicts from one forward pass.

[FIGURE:fig4]

\paragraph{Members are human/LLM-auditable.} Describing each of $89$ unit members by its logit-lens top-10 tokens and top-5 activating corpus windows with the sub-context label withheld, an ensemble LLM judge (three forced-choice calls with shuffled option order) names the sub-context with agreement $0.730$ versus a shuffle null of $0.096$ (analytic chance $0.070$); the gap is $0.634$, bootstrap CI $[0.545,0.724]$, with zero parse failures and total LLM spend $\$0.194$. Per role, absorbers are named at $0.756$ while anchors are named at only $0.429$---the judge over-specifies the parent's mixed-context windows, an honest caveat. For the wide first-letter pools, the fraction of all $15$ members receiving a confident label is L $0.87$, O $0.80$, T $0.93$, I $0.87$, D $0.67$, so the auditability extends to the full pool, not only the named core.

# When Does Grouping Help? An A-Priori Router
\label{sec:router}

The contribution is regime-scoped, so its practical value depends on telling, \emph{before} grouping, which regime a concept is in. The router is one forward pass over data already held [ARTIFACT:art_07ju05r0onqB].

\paragraph{The signals and the recommended rule.} The firing-Jaccard separates the regime extremes: spelling is firing-disjoint (Jaccard L $0.017$, O $0.039$, T $0.003$, I $0.008$, D $0.017$, all $<0.05$) and grouping helps, whereas toxicity co-fires (Jaccard $\approx 0.69$) and a single specialist wins. A threshold $\tau^\ast=0.05$ on the firing-Jaccard reaches balanced accuracy $0.917$ on the $12$ \emph{derivation} concepts. But firing-Jaccard alone is insufficient: the \emph{numeric} concept has a high Jaccard ($0.285$) yet an absorption-like outcome, and the \emph{aggregated taxonomic} concept has a low Jaccard ($0.056$) yet a co-firing outcome, because its parent already has $\approx 0.95$ recall and therefore no holes to fill. The parent recall-hole signal alone separates the derivation concepts perfectly (balanced accuracy $1.0$), and the \emph{combined} rule---low firing-Jaccard \emph{and} a high parent recall-hole---is the recommended screen, because each single signal has a counterexample the conjunction survives.

[FIGURE:fig5]

\paragraph{Derivation versus prospective, reported separately.} The thresholds, single-signal ablations, and leave-one-concept-out are all \emph{fit} on the $12$ derivation concepts (spelling, numeric, taxonomic, five toxicity sub-attributes); leave-one-out accuracy there is $0.733$. The rule is then frozen and applied to $3$ truly held-out concepts before their outcome is revealed: sentiment is a correct co-firing prediction, but CEBaB food/service were predicted co-firing yet showed small, significant absorption deltas ($+0.034$/$+0.071$), so the router scores $1/3$ prospectively. We therefore present it as a \emph{screening heuristic with a measured error rate}, not a validated oracle: a practitioner runs the cheap test and learns whether to reach for set-cover grouping or for supervised attribution, accepting a non-trivial miss rate.

# Within-SAE Selection: Homograph Absorption and First-Letter Spelling
\label{sec:selection}

Where the router predicts absorption, the unit recovers absorbers that a count-matched marginal-attribution selection drops. We report this as a \emph{within-SAE selection} result: it isolates the set-cover rule at matched pool size, and we say plainly where a dense probe still wins.

\paragraph{Non-spelling absorption is a homograph phenomenon.} Across all $52$ countries, the absorption signature---a parent recall hole $>0.5$ \emph{and} a specialist firing-Jaccard $<0.1$---holds for \emph{exactly two}: Georgia (hole $0.80$) and Jordan (hole $0.71$), both documented homographs whose general is-a-country parent is suppressed (Georgia $=$ US-state / country / given-name; Jordan $=$ country / given-name) [ARTIFACT:art___vgSpUe6wAF]. Other homographs (Chile, Turkey) have their parent \emph{cover} them (hole $\approx 0$) and are not absorption; the remaining $48$ countries have no hole. So non-spelling absorption is not broad taxonomic generalization but a \emph{polysemy} phenomenon, flagged a priori by the router's recall-hole signal---consistent with the sparsity-and-hierarchy mechanism that produces absorption.

\paragraph{The classifier and the corroborated specialists are now the same unit.} A pure maximum-coverage objective selects, for the Georgia hole, the high-coverage \emph{low-precision} latent $4697$ (sub-context firing precision $0.335$), which is \emph{not} the diagnostic-corroborated specialist. The precision gate (and the precision-weighted objective) instead recover latent $16009$ (precision $0.968$ on selection, $0.955$ held-out) and drop $4697$; all three rebuilt absorbers (Georgia $16009$, Jordan $540$, United States $846$) pass the held-out per-sub-context precision floor (fraction $1.0$). On the defining Georgia slice ($150$ positives vs.\ $2{,}100$ negatives) the rebuilt unit reaches AUC $0.995$ and beats every label-free selector with AUC-difference CIs excluding $0$ (Table~\ref{tab:taxonomic}): S-rec $+0.307$, S-prec $+0.416$, S-mag $+0.294$, RE-$k$-anchored $+0.082$, and the supervised pools (g) $+0.577$ and (h) $+0.612$ (both below chance---the absorption signature, where top-marginal pools fire on negatives but are silent on the absorbed slice). The discriminating case is S-prec: the globally most-precise latents are not Georgia-specific, so a precision \emph{ranking} misses $16009$ and collapses to AUC $0.579$, exactly where set-cover \emph{coverage} wins. \emph{Honest scope:} the classification AUC is near-identical across the coverage and precision objectives (all three Georgia absorbers reach recall $1.0$ with $\approx 0$ false positives), so the precision rebuild buys \emph{auditability}---a Georgia-pure member---not raw AUC; and a non-SAE dense probe still edges the unit ($1.000$ vs.\ $0.995$, $-0.005$, CI $[-0.008,-0.003]$).

\begin{table}[t]
\centering
\small
\caption{Rebuilt taxonomic unit $[3792,16009,540,846]$ on the Georgia slice: AUC and AUC-difference CIs (paired bootstrap, $B=10{,}000$). The set-cover selection beats all label-free selectors; (g)/(h) below chance is the absorption signature; the dense probe still edges the unit. $^\ast$ = CI excludes $0$.}
\label{tab:taxonomic}
\begin{tabular}{lcc}
\toprule
Comparator & AUC & unit $-$ comparator [95\% CI] \\
\midrule
\textbf{Rebuilt unit} & \textbf{0.995} & --- \\
S-rec (content-flip recall) & 0.687 & $+0.307\ [0.267,0.348]^\ast$ \\
S-prec (firing precision) & 0.579 & $+0.416\ [0.382,0.448]^\ast$ \\
S-mag (response magnitude) & 0.701 & $+0.294\ [0.254,0.334]^\ast$ \\
RE-$k$-anchored & 0.913 & $+0.082\ [0.070,0.094]^\ast$ \\
(g) top-20 attribution & 0.418 & $+0.577\ [0.534,0.619]^\ast$ \\
(h) count-matched attribution & 0.383 & $+0.612\ [0.576,0.648]^\ast$ \\
Dense probe (non-SAE) & 1.000 & $-0.005\ [-0.008,-0.003]$ \\
\bottomrule
\end{tabular}
\end{table}

\paragraph{The diagnostic corroborates by precision, not by magnitude.} The form-free \texttt{absorption\_fraction} is a \emph{magnitude} oracle; on the Georgia hole its own top pick is the high-coverage low-precision latent $1966$ (precision $0.34$), not $16009$, so per-edge top-1 agreement with $16009$ is $0$. We report this honestly rather than as a $3$-edge mean: corroboration of the rebuilt unit rests on the \emph{precision} diagnostic (held-out precision $\geq 0.7$, mutual exclusivity, hole-coverage gain CI $>0$) and the router recall-hole signal---all of which $16009$, $540$, and $846$ pass---while the magnitude oracle is precision-blind and prefers the broad latent.

\paragraph{First-letter spelling: set-cover isolated against non-random selectors.} On first-letter spelling the unit attains the highest held-out AUC on every letter (L $0.905$, O $0.917$, T $0.858$, I $0.983$, D $0.956$) and beats the count-matched attribution pool (h) (L $0.795$, O $0.819$, T $0.647$, I $0.735$, D $0.727$) [ARTIFACT:art_JMA2gBvnakAm]. The unsupervised firing-floor anchor validation fixes a spurious-anchor failure on letter I---its recall-argmax anchor fires $0\%$ on the corpus; the validated anchor (fires $20.6\%$) is the diagnostic parent---so the absorption mechanism (E1) now holds on \emph{all five} letters. The decisive test is whether the \emph{set-cover} selection beats sensible label-free selection: the unit must beat (h) \emph{and} all three of S-rec/S-prec/S-mag with CIs excluding $0$. This holds on I and D ($2/5$); on L/O/T the strong S-rec (top-$k$ by recall, which already picks the anchor plus the highest-coverage latents) matches the unit, so the win there is cover-based eligibility plus sensible selection, not set-cover-specific (Table~\ref{tab:firstletter}). Pooled across letters the unit beats (h) by $0.188$ (CI $[0.148,0.223]$), S-rec by $0.109$ (CI $[0.077,0.143]$), S-prec by $0.273$, and S-mag by $0.120$, but the per-letter S-rec margin is significant on only $2/5$. We therefore scope the headline accordingly: the per-letter joint of mechanism \emph{and} set-cover-specific selection is $2/5$ (I, D), and we report it as such rather than aggregating two separately-satisfied conditions.

\begin{table}[t]
\centering
\small
\caption{First-letter selection isolation. ``Beats'' columns mark an AUC-difference CI excluding $0$ (unit minus comparator). Set-cover-specific selection (beats (h) AND all three S-selectors) holds on I and D; E1 (absorption mechanism) holds on all five after the firing-floor anchor fix.}
\label{tab:firstletter}
\begin{tabular}{lccccccc}
\toprule
Letter & unit AUC & (h) & beats h & beats S-rec & beats S-prec & beats S-mag & set-cover / E1 \\
\midrule
L & 0.905 & 0.795 & \checkmark & --- & \checkmark & --- & no / \checkmark \\
O & 0.917 & 0.819 & --- & --- & \checkmark & --- & no / \checkmark \\
T & 0.858 & 0.647 & \checkmark & --- & \checkmark & \checkmark & no / \checkmark \\
I & 0.983 & 0.735 & \checkmark & \checkmark & \checkmark & \checkmark & \textbf{yes} / \checkmark \\
D & 0.956 & 0.727 & \checkmark & \checkmark & \checkmark & \checkmark & \textbf{yes} / \checkmark \\
\bottomrule
\end{tabular}
\end{table}

\paragraph{The wide pool versus the named core.} The classification AUC above is from the full $\sim\!15$-member max-pool, of which only $\sim\!4$--$5$ are the named anchor and absorbers. A \emph{compact} unit restricted to the named members is significantly \emph{below} the wide pool on every letter (AUC difference $-0.056$ to $-0.200$, CIs excluding $0$): the diagnostic-uncorroborated eligible latents carry real classification signal, so human-auditable compactness costs AUC. We report this trade-off rather than conflate the two objects, and note (\S\ref{sec:audit}) that the wide pool remains auditable, with $67$--$93\%$ of its members receiving a confident label.

# Honest Negatives and Limitations
\label{sec:negatives}

We collect the method's failures in one place, each with its statistic.

\paragraph{No dense-probe out-classification.} On every task the best non-SAE dense probe matches or beats the unit: Georgia $0.995$ vs.\ dense $1.000$; numeric \texttt{integer} $0.635$ vs.\ $1.000$; toxicity loses to a residual probe ($0.859$). The contribution is auditable, editable, within-SAE repair---not aggregate classification.

\paragraph{Toxicity is a co-firing negative.} On ParaDetox/civil\_comments the general toxicity latent ($12714$, ``profanity/vulgar'') fires on $94.3\%$ of toxic content-flips (precision $0.996$), and on-target detectors exist for the label-disjoint sub-attributes (threat $11630$, identity\_attack $11573$, insult $13367$) [ARTIFACT:art_-o2RPMOZp37A]. But they \emph{co-fire} with the general latent (toxic-only firing-Jaccard $0.403$, $0.292$, $0.655$---all far above $0.10$), so the set-cover K-track correctly adds zero absorbers; the C-track unit ties weak baselines (AUC $0.762$ vs.\ (a) $0.765$), loses to attribution ((h) $0.837$; CI $[-0.093,-0.055]$) and a residual probe ($0.859$), and collapses on the disjoint sub-attributes (threat $0.626$ vs.\ (h) $0.929$). This is the co-firing pole the router predicts: where firing co-fires, supervised attribution is the right tool and CCRG should not be used.

\paragraph{Numeric is unconfirmed; set-cover is $2/5$ on spelling.} On the numeric hierarchy the \texttt{integer} slice is co-firing (firing-Jaccard $0.256$), the set-cover selection is not established (no precision-passing integer specialist), and a dense probe dominates (AUC $1.000$ vs.\ unit $0.635$). On first-letter spelling the set-cover-specific win is $2/5$ (\S\ref{sec:selection}); letter-I is a selection win that depends on the anchor-validation fix, and the absorbed-slice recall test is significant only on the best-powered letter (T). The RE-$k$ floor is an easy bar (median draw AUC $0.63$--$0.69$); we retain it only as a floor and rest the selection claim on the non-random S-selectors.

\paragraph{Steering and model-diffing are generality demos.} Steering with the unit's mean-member-decoder direction is the most surgical (lowest full-vocabulary KL at matched on-target effect) on letters L (KL $16.4$ vs.\ hub $27.9$, diff-of-means $30.4$) and D, but a diff-of-means or hub direction is more surgical on O/T/I [ARTIFACT:art_0ueMMR8Tt02P]. For model-diffing, no instruction-tuned Gemma Scope SAE exists for the 2B model, so we apply the shared pretrained SAE to \texttt{gemma-2-2b} and \texttt{gemma-2-2b-it} and bound the confound [ARTIFACT:art_jI2KIJotjzIU]. A base-vs-IT shift is detectable for the toxicity unit (departure $0.062$, $p<10^{-3}$) but is \emph{not concept-specific}: the spelling control shows the same $0.062$ departure, so the control-subtracted genuine shift is $+0.000$ (CI $[-0.009,0.007]$), and the unit does not detect the shift more reliably than the best single latent. We present this as a confound-bounded null, not future work.

\paragraph{Scope.} A hedged single polysemantic latent is not groupable \citep{Chanin2025}, and bias\_in\_bios is a pre-registered boundary-null, not a method failure.

# Discussion
\label{sec:discussion}

\paragraph{What is established.} Executed on a frozen Gemma Scope SAE, CCRG turns unreliable single latents into auditable multi-member units and a feature knowledge graph whose edges carry \emph{measured} utility. The headline is editorial, not classificatory: a KG-named absorber added to a suppressed parent recovers its recall hole ($30$ repairs surviving FDR control across spelling, taxonomic, and numeric families), a fix a dense probe provably cannot localize; and ablating a single KG-named absorber edits one sub-context with $\sim\!1452\times$ median selectivity over collateral. Where grouping helps---the absorption regime of mutually-exclusive firing with parent recall holes---a one-forward-pass router predicts it beforehand with a measured error rate, and the unit's set-cover selection beats every label-free selector at matched pool size (taxonomic Georgia; first-letter I and D).

\paragraph{A regime-scoped, auditability-first contribution.} The most useful lesson is that latent grouping is not a universal repair. It helps in a specific, a-priori-identifiable regime and not in the co-firing/splitting regime, where supervised attribution wins. This reframes the method from ``better SAE classifiers'' to ``an auditable repair for absorption, with a screening test for when to use it''---more defensible because it does not depend on beating a dense probe, and more useful because the unique deliverable (a named, addable, ablatable sub-context specialist) is exactly what a dense hyperplane cannot expose.

\paragraph{Honest failure modes.} (1) No SAE unit out-classifies a dense probe on any task. (2) On first-letter the per-letter joint of mechanism and set-cover-specific selection is $2/5$. (3) Non-spelling absorption is narrow---two homograph countries---rather than broad taxonomic generalization. (4) The numeric hierarchy is co-firing and diagnostic-unconfirmed. (5) Toxicity is a clean co-firing negative. (6) The router's prospective accuracy is $1/3$ on three held-out concepts. (7) The form-free magnitude diagnostic is precision-blind, so corroboration rests on the precision diagnostic. (8) Model-diffing is a confound-bounded null. Each is reported with its statistic rather than spun as future work.

# Conclusion
\label{sec:conclusion}

We presented Two-Track Co-Response Grouping, a training-free method that organizes the latents of a frozen public SAE into reliable, auditable concept units by their interventional response to content counterfactuals---correlation communities for shared-support splitting and a precision-gated anchored set-cover for disjoint-support absorption that no pairwise-affinity clustering can propose. The durable contribution is a feature knowledge graph with \emph{measured} repair utility: $30$ KG-guided recall repairs survive false-discovery control across three concept families, a single KG-named absorber yields a surgical sub-concept edit at $\sim\!1452\times$ selectivity, and members are LLM-auditable at $0.730$ agreement versus a $0.096$ null---capabilities a dense probe lacks. A one-forward-pass firing-Jaccard-plus-recall-hole router predicts when grouping helps, and where it does, the set-cover selection beats every label-free selector at matched pool size on a precision-rebuilt taxonomic homograph unit and on two first-letter tasks. We release four frozen testbeds, a single-GPU pipeline, and a complete account of where the method works and where it does not---a co-firing toxicity regime, an unconfirmed numeric hierarchy, a $2/5$ set-cover result on spelling, no dense-probe out-classification, and a null model-diffing result.

\paragraph{Future work.} Harden the router into a per-concept routing rule that picks set-cover grouping versus attribution automatically; extend the surgical-edit demonstration to a safety-relevant downstream task with fluency scoring; and revisit model-diffing if a paired instruction-tuned SAE becomes available.

# Appendix: Reproducibility
\label{sec:repro}

\paragraph{Encoding and gating.} The SAE is loaded directly from Gemma Scope \texttt{params.npz} (canonical \texttt{layer\_12/width\_16k}, JumpReLU, $d_{\text{model}}=2304$); the residual is captured by a forward hook on \texttt{model.layers[12]} output (equivalently \texttt{blocks.12.hook\_resid\_post}). Each run gates on reconstruction fidelity before analysis: first-letter reconstruction cosine $0.924$, explained variance $0.857$, mean L0 $96.1$; toxicity cosine $0.916$; non-spelling encode-time FVU $0.18$/$0.20$ with token-alignment $0.975$/$1.000$; the auditability and router runs gate at cosine $0.919$ and $0.927$. (Numeric digit-token reconstruction is $0.8911<0.9$ in isolation; because the SAE/layer mapping is global, the analysis is gated on taxonomic country tokens.) Word-token positions are recovered via the tokenizer offset map; corpus windows are drawn from a pinned Pile revision; surface-flip nulls use an independently re-judged $1{,}700$-pair superset [ARTIFACT:art_YwjLYapklnVk].

\paragraph{Models and software.} Model \texttt{google/gemma-2-2b} (and \texttt{-2b-it} for model-diffing) via ungated mirrors, bf16; SAE \texttt{google/gemma-scope-2b-pt-res}, \texttt{average\_l0\_82}. AUC is rank-based and robust to bf16 hardware numerics; deterministic baselines reproduce across GPU classes to within $\pm 0.001$ AUC, with a single discrete greedy set-cover tie at one letter's $15$th member documented as a hardware-numerics artifact. The form-free absorption diagnostic uses a parent probe trained on data disjoint from clustering. LLM member-labeling uses \texttt{claude-haiku-4.5} at temperature $0$; total auditability LLM spend is $\$0.194$. Citation venues follow a verified audit (e.g.\ \citet{Chanin2024} NeurIPS 2025; \citet{Wu2025}, \citet{Karvonen2025} ICML 2025; \citet{Leask2025} ICLR 2025) [ARTIFACT:art_QBxBPF-9Ldxe].

\bibliographystyle{plainnat}
\bibliography{references}

</current_paper>

<reviewer_feedback>
Paper reviewer feedback from the previous iteration. Your strategy MUST address these critiques.
Prioritize major issues — these are the most impactful improvements to make.

- [MAJOR] (scope) Demonstrated significance remains the central ceiling. The reframe to an auditability-first contribution is the right and honest move, but the unique capability (a named, addable/ablatable sub-context absorber) is never shown to change a downstream outcome that matters. Against the goal's three concrete tasks: classification loses to a non-SAE dense probe on EVERY task (Georgia 0.995 vs 1.000, numeric integer 0.635 vs 1.000, toxicity loses to a residual probe); steering is surgical on only 2/5 toy spelling letters; model-diffing is a confound-bounded null; and toxicity, the only safety-relevant family, is a clean negative. The set-cover-SPECIFIC selection win (over non-random selectors) is established on just 3 slices total (Georgia, first-letter I, D). So the method's reliability gain is delivered as localization/auditability, not as task performance, and the importance of that localization is asserted rather than demonstrated.
  Action: Add at least one downstream demonstration where the KG-localized single-absorber edit beats the dense/diff-of-means baseline on an outcome that matters (e.g., remove or steer a specific sub-context of a safety-relevant attribute while preserving the parent and fluency, measured by on-target effect, sibling collateral, and an AxBench-style fluency/LLM-judge score). One concrete win where the editable localized fix changes a real outcome would convert the auditability story from 'a capability a probe lacks' into 'a capability that produces a better result than the probe,' which is what the goal requires and what would lift the score.
- [MAJOR] (rigor) All results come from a single SAE (gemma-2-2b, layer 12, width-16k canonical). Feature absorption is known to depend on dictionary size and hierarchy (the very motivation for Matryoshka/hierarchical SAEs the paper cites), so a method whose entire value proposition is 'repair absorption in frozen public SAEs' needs to show its units, repairs, surgical edits, and router are not specific to one (layer, width) dictionary. As written, a skeptical reviewer cannot rule out that the regime map and the recovered absorbers are artifacts of this particular dictionary. The 65k-width canonical SAE and other layers are available on the same model.
  Action: Re-run the headline auditability spine (KG-repair FDR, the Georgia/Jordan surgical edits, the firing-Jaccard/recall-hole router) on at least the 65k-width SAE and/or one other layer, and report whether (i) the same homograph holes appear, (ii) the repairs and surgical selectivities replicate, and (iii) the router thresholds transfer. Even a partial replication with honest deltas would substantially de-risk the generalization claim; a failure to replicate is itself a publishable, honest finding about dictionary-dependence.
- [MINOR] (evidence) The headline selectivity figure is mislabeled. The artifact's six absorption cases have selectivity ratios {7.8, 213.5, 802.0, 1722.5, 2722.3, 3246.9}: mean = 1452.5, median = 1262.2. The paper reports '~1452x median selectivity' in the abstract, intro, and discussion (and '1452x average' in the audit section). 1452 is the mean, not the median. Moreover the n=6 average includes the United-States 4760 case the paper itself classifies as PARTIAL_SURGICAL (7.8x), so the 'absorption-regime' average is partly built on a case the text excludes from 'surgical.' Relatedly, the claim 'absorber precision predicts surgicality' is undercut by the first-letter 'large' case (precision 0.571 -> 802x surgical) versus US-4760 (precision 0.709 -> 7.8x partial): lower precision, higher surgicality.
  Action: Replace 'median' with 'mean' (or report the true median 1262x) consistently. State explicitly which cases are averaged and whether the partial-surgical 4760 is included. Soften 'absorber precision predicts surgicality' to a within-family observation, or report the precision-vs-selectivity relationship across all 7 cases so the 'large' counterexample is visible.
- [MINOR] (rigor) The '30 KG-named absorber additions recover a suppressed parent's recall hole' is over-counted. Of the 30 FDR survivors, six sub-contexts (Georgia, Jordan, US, date, decimal, ordinal) are counted TWICE because their kg_ktrack and kg_diagnostic variants name the IDENTICAL latent (e.g., Georgia 16009 in both), and at least one survivor, numeric 'percent', has is_hole=False in the artifact (no recall hole to repair, gain +0.04). So the headline phrase 'recover a suppressed parent's recall hole' applies to roughly 23 distinct holes, not 30; '30' is a count of repair VARIANTS, several of which are the same latent or not a hole.
  Action: Report the distinct-hole count (~23) as the primary headline number and present 30 as 'repair variants (k-track and diagnostic edges) over N distinct holes.' De-duplicate where kg_ktrack and kg_diagnostic are the same latent, and exclude or separately flag non-hole sub-contexts (percent) so the count cleanly matches the 'suppressed-parent recall hole' framing.
- [MINOR] (clarity) The repair-loop control is described in the audit section as 'a control that adds the full population of other content-responsive latents,' but the implemented control (method.py repair_loop) compares the KG absorber's per-window detection against rand_detect_perwin = the per-window MEAN detection of a single randomly-drawn content-responsive latent (the percentile is vs the distribution of single-latent gains). Adding the full population via max-pool would be a far stronger control that the absorber would likely NOT beat on recall (a union of many latents drives recall toward 1.0). The current wording overstates the control's strength; the actually-run control (random single-latent addition) is the appropriate one and should be described as such.
  Action: Reword to 'beating a random single content-responsive-latent addition control (the KG absorber's recall gain exceeds the 95th/99th percentile of single-latent additions).' Keep the (correct) implemented control and align the prose to it.
- [MINOR] (rigor) The router recommendation is internally tense. The paper recommends the combined rule (low firing-Jaccard AND high recall-hole) on the grounds that 'each single signal has a counterexample the conjunction survives,' but in the cited artifact the combined rule scores balanced accuracy 0.917 on the 12 derivation concepts, which is LOWER than recall-hole-alone (1.0). Recall-hole-alone has no counterexample on the derivation set, so the stated justification does not favor the conjunction over it. Separately, the prospective test (1/3) had all three predictions in the SAME regime (co_firing), so it cannot demonstrate discriminative value out-of-sample.
  Action: Either recommend recall-hole-alone (the empirically best derivation separator) and frame firing-Jaccard as a corroborating signal, or explicitly argue and, if possible, show that the conjunction generalizes better despite lower derivation accuracy. Acknowledge that the prospective set contained only one regime and expand it (above) so the router can be wrong in both directions.
- [MINOR] (evidence) The taxonomic 'selection beats every label-free selector' headline rests on a single slice. Per the homograph cross-tab, only Georgia and Jordan satisfy the absorption signature (parent recall-hole >0.5 AND specialist firing-Jaccard <0.1); Jordan is on a descriptive slice (n=124 < 150 in the eligibility analyses) and United States is co-firing/splitting (firing-Jaccard 0.20), not absorption-type. So the affirmative set-cover selection result for the non-spelling spine is effectively n=1 country (Georgia). The paper scopes this honestly, but a single-slice affirmative result is thin for a headline contribution.
  Action: Search for additional suppressed-parent polysemy cases to corroborate (other entity homographs, or a second is-a hierarchy where a general parent is suppressed on specific children), and report the Jordan selection result with its n and eligibility status next to Georgia so the reader sees the affirmative taxonomic evidence is currently one-to-two slices.
</reviewer_feedback>

<task>
Generate 1 research strategy for THIS iteration.

**ARTIFACT LIMIT: Each strategy may contain AT MOST 7 artifact directions.** Focus on the highest-impact artifacts. Quality over quantity.

Each strategy should:
1. Define a clear OBJECTIVE - what novel contribution we're building toward
2. Plan artifacts to execute NOW - specify type, objective, approach, and depends_on for each
3. Account for parallel execution - all strategies and all planned artifacts run simultaneously, their artifacts are combined into one shared pool


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
    "ArtifactDep": {
      "description": "A single dependency on an existing artifact, with a short type label.\n\n``id`` and ``label`` are LLM-generated at strategy time. ``label`` is free-text but\nshort \u2014 a word or two naming the type of dependency, not a sentence.\n\n``relation_type`` and ``relation_rationale`` are populated later, in upd_hypo,\nusing the MultiCite citation-function typology (Lauscher et al., NAACL 2022).\nThey are absent at strategy time and may stay absent for legacy runs.",
      "properties": {
        "id": {
          "description": "ID of an existing artifact this artifact depends on",
          "title": "Id",
          "type": "string"
        },
        "label": {
          "description": "Short free-text label naming the type of this dependency (a word or two, not a sentence)",
          "title": "Label",
          "type": "string"
        }
      },
      "required": [
        "id",
        "label"
      ],
      "title": "ArtifactDep",
      "type": "object"
    },
    "ArtifactDirection": {
      "description": "High-level direction for an artifact to execute this iteration.\n\nID is code-assigned (LLMPrompt only \u2014 visible in prompts, not LLM-generated).",
      "properties": {
        "type": {
          "description": "Type of artifact to create",
          "enum": [
            "experiment",
            "research",
            "proof",
            "evaluation",
            "dataset"
          ],
          "title": "Type",
          "type": "string"
        },
        "objective": {
          "description": "What we want to achieve with this artifact",
          "title": "Objective",
          "type": "string"
        },
        "approach": {
          "description": "High-level direction/method",
          "title": "Approach",
          "type": "string"
        },
        "depends_on": {
          "description": "Existing artifacts this depends on, each with a short type label",
          "items": {
            "$ref": "#/$defs/ArtifactDep"
          },
          "title": "Depends On",
          "type": "array"
        }
      },
      "required": [
        "type",
        "objective",
        "approach"
      ],
      "title": "ArtifactDirection",
      "type": "object"
    },
    "Strategy": {
      "description": "A research strategy.\n\nContent fields have LLMPrompt + LLMStructOut markers.\n``id`` is code-assigned (LLMPrompt only \u2014 visible in prompts, not LLM-generated).\n\nID format: gen_strat_idx{N}",
      "properties": {
        "title": {
          "description": "Short name for this strategy",
          "title": "Title",
          "type": "string"
        },
        "objective": {
          "description": "The novel contribution we're building toward",
          "title": "Objective",
          "type": "string"
        },
        "rationale": {
          "description": "Why this strategy is promising",
          "title": "Rationale",
          "type": "string"
        },
        "artifact_directions": {
          "description": "Artifacts to execute THIS iteration",
          "items": {
            "$ref": "#/$defs/ArtifactDirection"
          },
          "title": "Artifact Directions",
          "type": "array"
        },
        "expected_outcome": {
          "description": "What we'll have after this iteration's artifacts complete",
          "title": "Expected Outcome",
          "type": "string"
        },
        "summary": {
          "default": "",
          "description": "Brief summary of the strategy and its expected contribution",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "title",
        "objective",
        "rationale",
        "artifact_directions",
        "expected_outcome"
      ],
      "title": "Strategy",
      "type": "object"
    }
  },
  "description": "Top-level wrapper for LLM strategy generation output.",
  "properties": {
    "strategies": {
      "description": "List of generated strategies",
      "items": {
        "$ref": "#/$defs/Strategy"
      },
      "title": "Strategies",
      "type": "array"
    }
  },
  "required": [
    "strategies"
  ],
  "title": "Strategies",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-06-18 01:42:20 UTC

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

### [3] SYSTEM-USER prompt · 2026-06-18 01:51:42 UTC

```
<verification_results>
Your previous response had issues that need fixing:

DEPENDENCY ERRORS (depends_on can ONLY reference IDs from <existing_artifacts>):
  - Strategy 1: Artifact 'experiment_iter5_dir1' (experiment): dependency 'art_0CZwPjG2YMCf' has type 'experiment' which is not allowed (allowed: {'dataset', 'research'})
  - Strategy 1: Artifact 'experiment_iter5_dir2' (experiment): dependency 'art_sxwT7hK6YFEA' has type 'experiment' which is not allowed (allowed: {'dataset', 'research'})
  - Strategy 1: Artifact 'experiment_iter5_dir2' (experiment): dependency 'art_0CZwPjG2YMCf' has type 'experiment' which is not allowed (allowed: {'dataset', 'research'})
  - Strategy 1: Artifact 'experiment_iter5_dir2' (experiment): dependency 'art_07ju05r0onqB' has type 'experiment' which is not allowed (allowed: {'dataset', 'research'})
  - Strategy 1: Artifact 'experiment_iter5_dir3' (experiment): dependency 'art_GTc_f26dMzFs' has type 'experiment' which is not allowed (allowed: {'dataset', 'research'})
  - Strategy 1: Artifact 'experiment_iter5_dir3' (experiment): dependency 'art_07ju05r0onqB' has type 'experiment' which is not allowed (allowed: {'dataset', 'research'})
  - Strategy 1: Artifact 'experiment_iter5_dir4' (experiment): dependency 'art___vgSpUe6wAF' has type 'experiment' which is not allowed (allowed: {'dataset', 'research'})
  - Strategy 1: Artifact 'dataset_iter5_dir7' (dataset): dependency 'art_t2uUbjSwpd3t' has type 'dataset' which is not allowed (allowed: {'research'})

</verification_results>

<task>
Fix ALL issues above and regenerate your strategies:

1. Fix dependency errors:
   - depends_on is a list of {id, label} objects — every entry MUST have a non-empty short label
   - id can ONLY reference IDs from <existing_artifacts>
   - You CANNOT reference artifacts you are proposing in this strategy as dependencies (they all run in parallel)
   - Follow the dependency type rules (e.g., experiments require datasets)
   - If no suitable existing artifacts exist, use depends_on: []

Output the corrected JSON with the fixed strategies.
</task>
```
