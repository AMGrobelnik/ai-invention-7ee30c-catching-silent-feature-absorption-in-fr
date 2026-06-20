# gen_art_research_1 — test_idea

> Phase: `invention_loop` · round 6 · `gen_art`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_research_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 05:31:43 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact executor (Step 3.3: GEN_ART in the invention loop)

Executing a plan to produce a concrete artifact.
GEN_PAPER_TEXT will use your artifact in the next paper draft.

Rigorous artifact with clear results → strong paper. Sloppy artifact → misdirected research.
</your_role>
</ai_inventor_context>

<task>
Conduct thorough, unbiased research on the given topic.
Adapt your investigation approach based on the research question and domain.
</task>

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

<critical_requirements>
1. SOURCE DIVERSITY - Consult MANY sources (10+), not just the first few results
2. AVOID SELECTION BIAS - Actively seek contradicting viewpoints, not just confirming ones
3. TRIANGULATE - Cross-reference claims across multiple independent sources
4. ACKNOWLEDGE UNCERTAINTY - Be honest about confidence levels and limitations
5. SYNTHESIZE - Produce a coherent answer that accounts for conflicting evidence
</critical_requirements>

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

Read and STRICTLY follow these skills: aii-web-tools.

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_research_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_research_1/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_research_1/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_research_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

<context>
<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
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
out_dependency_files:
  file_list:
  - research_out.json

--- Dependency 2 ---
id: art_y_5u-bfJOq3V
type: research
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
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_research_1
out_dependency_files:
  file_list:
  - research_out.json

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>
</context>

<artifact_plan>
id: gen_plan_research_1_idx6
type: research
title: >-
  CCRG iter-6 Positioning Plan: M2' Safety-Identity-Absorption Cite-and-Distinguish, M1' u_sub Label-Efficiency Reframe (retire
  'structurally cannot localize'), Locked-Citation Refresh
summary: >-
  Detailed RESEARCH plan for the iter-6 positioning + citation-finalization artifact (research_iter6_dir6). Pure web research,
  $0 LLM spend, cpu_light, no code. Three workstreams build on the iter-4 (art_QBxBPF-9Ldxe) and iter-5 (art_y_5u-bfJOq3V)
  positioning WITHOUT re-doing settled entries: (1) a M2' SAFETY cite-and-distinguish block establishing that CCRG's conjunction
  -- a DISCOVERED single absorber for ONE identity/demographic sub-context, edited while PRESERVING the parent identity concept,
  scored vs a SUB-CONTEXT-targeted dense direction u_sub -- is distinct from whole-group/whole-concept bias/identity erasure
  AND from example-reweighting debiasing, with a both-branches honest-null framing; (2) a M1' u_sub LABEL-EFFICIENCY positioning
  paragraph that explicitly RETIRES the false 'a single dense hyperplane structurally cannot localize to a sub-context / erasing
  the is-a-country direction removes all countries' argument and supplies replacement wording grounded in Peng 'Discover-not-Act'
  (2506.23845) + the weak-supervision/label-efficiency literature, covering BOTH M1' forks (KG beats u_sub vs KG matches-u_sub-without-labels);
  (3) a refreshed venue-locked citation table + BibTeX adding verified identity-unlearning/bias-editing cites and re-confirming
  carry-forwards. Emits research_out.json {answer, sources, follow_up_questions} + research_report.md with the safety block,
  the u_sub paragraph (both forks), the honest-null framing, the locked table, BibTeX, and an updated presentation-strip checklist
  for GEN_PAPER_TEXT.
runpod_compute_profile: cpu_light
question: >-
  How should the iter-6 CCRG paper position (a) the M2' safety-relevant identity-absorption framing against the identity/demographic-unlearning,
  bias/stereotype-mitigation, and fairness/association-editing literature so that a safety win OR an honest-null lands as
  a deliberate, literature-grounded contribution; and (b) the M1' u_sub LABEL-EFFICIENCY fork against the 'use SAEs to discover,
  not act' framing and weak-supervision/label-efficiency literature -- while explicitly retiring the false 'a dense hyperplane
  structurally cannot localize to a sub-context' argument and refreshing the venue-locked citation set for GEN_PAPER_TEXT?
research_plan: |-
  PURE WEB RESEARCH (aii-web-tools: search -> fetch -> fetch_grep). $0 LLM spend, no code, cpu_light. Output = research_out.json {title, summary, answer, sources[], follow_up_questions[]} + research_report.md. Do NOT run experiments, do NOT invent venues/authors. ALWAYS prefer fetch_grep over a fetched page when you need an exact venue string, author list, or verbatim quote (especially for arXiv abstract pages and ACL Anthology / OpenReview PDFs).

  =========================================================
  WS0 -- GROUND IN PRIORS; DO NOT REDO SETTLED WORK (~15 min)
  =========================================================
  Read BOTH dependency files first and inventory what is already locked so you only spend effort on the NEW iter-6 deliverables:
    - art_QBxBPF-9Ldxe (iter-4): /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_research_1/research_out.json AND its sibling research_report.md.
    - art_y_5u-bfJOq3V (iter-5): /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_research_1/research_out.json AND its sibling research_report.md.
  Extract and TABULATE the SETTLED entries (carry verbatim, do NOT re-verify unless a quick sanity check is free):
    - Chanin 'A is for Absorption' 2409.14507 = NeurIPS 2025 (Oral); SAEBench 2503.09532 + AxBench 2501.17148 + Matryoshka 2503.17547 + SAeUron 2501.18052 + DPE 2505.23027 = ICML 2025; CanonicalUnits 2502.04878 + PS-Eval 2501.06254 = ICLR 2025; LEACE 2306.03819 = NeurIPS 2023; SCR/TPP 2411.18895 = NeurIPS 2024 ATTRIB Workshop; Mind-the-GAP 2403.09869 = AISTATS 2024.
    - M1 unlearning literature already positioned in iter-5: Farrell 2410.19278 = NeurIPS 2024 Safe-GenAI Workshop; CRISP 2508.13650 = ACL 2026; SAUCE = ICCV 2025 CVF (arXiv 2503.14530 WITHDRAWN -> cite CVF only); SSPU 2505.24428 = EMNLP 2025 Main; SRMU 2512.16297 = preprint; Peng 'Discover-not-Act' 2506.23845 = preprint; WMDP 2403.03218 = ICML 2024; TOFU 2401.06121 = COLM 2024; MUSE 2407.06460 = ICLR 2025; RWKU 2406.10890 = NeurIPS 2024 D&B; SHRED 2605.07482 + unlearning-survey 2601.13264 = preprints; SAE-TS 2411.02193 + SRS 2503.16851 = preprints.
    - Carry-forward flags to RESOLVE this iteration: Deng 2506.18141 possible NeurIPS-2025 upgrade (verify track); Muchane 2506.01197 OpenReview C7M6F0OJ1l acceptance unconfirmed; SAEmnesia 2509.21379 / SNCE 2509.21008 author lists to verify at bib-time.
  EXPLICITLY NOTE what is NEW for iter-6 and is the ONLY substantive new work: (i) the M2' identity/demographic/bias-editing/fairness-editing/PII literature was NOT surveyed in iter-4/iter-5 (those covered whole-concept unlearning + the homograph-absorption novelty + the surgical-edit distinctness); (ii) the M1' decisive comparator changed from whole-parent erasure (f) to a SUB-CONTEXT-targeted dense direction u_sub, which RETIRES the iter-5 'LEACE single hyperplane structurally cannot localize to a sub-context' framing -- that argument is now FALSE and must be replaced; (iii) new identity-unlearning/bias-editing cites need verification.
  Write a 'what changed vs iter-5' preamble for the report capturing exactly (i)-(iii).

  =========================================================
  WS1 -- M2' SAFETY-RELEVANT IDENTITY-ABSORPTION POSITIONING (~50 min)
  =========================================================
  GOAL: produce a cite-and-distinguish block proving CCRG's M2' conjunction is a deliberate, distinct contribution. The conjunction to defend (state it as the explicit novelty boundary): a single SAFETY/IDENTITY sub-context (e.g. a specific demographic/dialect/identity token absorbed under a general 'identity/group/demographic' parent) is (1) DISCOVERED label-free as one absorber latent by interventional two-track grouping (not pre-specified), (2) EDITED to surgically remove/recover ONLY that sub-context while PRESERVING the parent identity concept and sibling sub-contexts, (3) SCORED vs a SUB-CONTEXT-targeted dense direction u_sub = diff-of-means(target-sub-context-positive, sibling-positive) at matched forget on a joint on-target/collateral/fluency metric. The block must distinguish this from BOTH whole-group/whole-concept erasure AND example-reweighting debiasing.

  Survey FIVE sub-literatures. For each, run 2-3 searches, fetch the 1-2 most representative/most-comparable papers, fetch_grep their abstract+method for (a) WHAT unit they edit/remove (whole demographic direction? whole entity? a stereotype association? reweighted examples?), (b) WHETHER they preserve a same-hierarchy parent vs only unrelated material, (c) WHETHER the target is discovered or pre-specified, (d) venue/authors/arXiv-id. Record each as a source with a one-line distinguisher.
    (1) SAE-BASED DEBIASING / DEMOGRAPHIC-FEATURE MITIGATION. Candidates already surfaced: debiaSAE 2410.13146 (VLM); 'Can SAEs Reveal and Mitigate Racial Biases of LLMs in Healthcare?' 2511.00177; SteerRM 2603.12795 (debiasing reward models via SAEs); 'Interpretable Debiasing of VLMs for Social Fairness' 2602.24014. Queries: 'sparse autoencoder debiasing demographic feature language model preserve utility'; 'SAE latent gender race feature steering bias mitigation LLM'. Distinguisher to establish: these steer/ablate a WHOLE demographic feature (gender/race direction) for fairness, NOT a single absorbed sub-context with parent preservation, and are NOT scored vs a sub-context-targeted dense direction; several are vision/VLM or reward-model modality distinguishers.
    (2) MODEL-EDITING FOR STEREOTYPE/BIAS. Candidates: BiasEdit 2503.08588 (= TrustNLP 2025 / ACL Anthology 2025.trustnlp-main.13; verify); 'Collapsed Language Models Promote Fairness' 2410.04472. Queries: 'BiasEdit debiasing stereotyped language model model editing'; 'model editing remove stereotype association preserve language modeling 2025'. Distinguisher: edits the stereotype ASSOCIATION / a bias subnetwork via gradient-localized weight edits, whole-stereotype not one absorbed identity sub-context; no discovered SAE absorber; no u_sub baseline.
    (3) FAIRNESS / CONCEPT-ERASURE EDITING (the dense-direction comparators). Candidates: 'Robustly Improving LLM Fairness in Realistic Settings via Interpretability' 2506.10922 (affine inference-time edit; OpenReview fHBb8BisyW); 'Debiasing Without Protected Attributes: Latent Concept Erasure from Textual Profiles' 2606.12088; 'Preserving Task-Relevant Information Under Linear Concept Removal' 2506.10703; INLP/RLACE/SAL family (mention, do not deep-dive). Queries: 'affine concept erasure bias direction ablation preserve task utility LLM 2025'; 'linear concept removal preserve task-relevant information fairness'. Distinguisher: these ablate a single dense BIAS direction (whole protected-attribute concept) -- exactly the whole-concept dense move; CCRG instead targets ONE sub-context and is compared to the strictly stronger u_sub (sub-context-targeted) dense direction. CRITICAL: these papers are ALSO the empirical evidence for WS2 that a dense direction built from the right labels DOES localize/preserve utility -- harvest one or two verbatim lines for the u_sub reframe.
    (4) IDENTITY / ENTITY / PII SELECTIVE UNLEARNING. Candidates: 'Unveiling Entity-Level Unlearning for LLMs' (COLING 2025, 2025.coling-main.358); 'Not Every Token Needs Forgetting: Selective Unlearning' 2506.00876; DFSU 'Data-Free Privacy-Preserving for LLMs via Model Inversion and Selective Unlearning' 2601.15595; NER-type-unlearning (preserve other entity types). Queries: 'entity-level unlearning preserve related entities LLM'; 'selective unlearning single demographic identity preserve sibling 2025'. Distinguisher: these remove a WHOLE entity/entity-type/PII record (and aim to preserve UNRELATED knowledge), not ONE absorbed sub-context on a shared identity hierarchy with parent + sibling preservation; not feature-discovered; not SAE.
    (5) LABEL-FREE WORST-GROUP / DEMOGRAPHIC-ROBUSTNESS by REWEIGHTING (already cited family -- distinguish, do not re-survey deeply). JTT 2107.09044 / GEORGE 2011.12945 / EIIL 2010.07249 / LfF 2007.02561 (carried). Distinguisher: these infer GROUPS OVER EXAMPLES and RETRAIN with reweighted/group-DRO loss; CCRG groups FEATURES, never retrains, and the recovered absorber IS the auditable sub-context specialist that can be EDITED -- orthogonal route.
  DELIVERABLE 1 (report section A): a cite-and-distinguish TABLE (columns: Method | arXiv-id+venue | Unit edited/removed | Preserves same-hierarchy parent? | Target discovered or pre-specified? | Scored vs sub-context dense direction? | Distinguisher one-liner) + a 1-2 paragraph drop-in 'Related work: safety-relevant identity absorption' block stating the explicit conjunction novelty boundary.
  DELIVERABLE 2 (report section A, honest-null subsection): draft the BOTH-BRANCHES framing. BRANCH-WIN: if M2' lands a safety-relevant absorption-structured win vs u_sub, supply drop-in wording positioning it as 'converting auditability into task performance on a safety-relevant sub-context, distinct from whole-group erasure and from reweighting debiasing.' BRANCH-NULL: if NO safety attribute is absorption-structured, supply drop-in wording for the capping limitation -- 'absorption is confined to homograph/polysemy entity tokens + first-letter spelling and is NOT exhibited by safety/identity attributes (which are co-firing, parent has no recall hole), so the safety contribution is bounded to the auditable repair/edit primitive rather than a new safety result' -- and connect to the 0/28-professions and toxicity-co-firing negatives already in the paper. Make clear GEN_PAPER_TEXT will keep whichever branch the experiments produced.
  GUARDRAIL: do NOT claim CCRG is the first SAE debiasing method (it is not); claim only the specific conjunction (discovered single absorber + parent-preserving sub-context edit + u_sub-scored). If an adversarial disprove search ('SAE single-feature edit one demographic sub-context preserve parent identity concept') surfaces a true precedent, REPORT it and narrow the claim honestly.

  =========================================================
  WS2 -- M1' u_sub LABEL-EFFICIENCY FRAMING + RETIRE THE FALSE ARGUMENT (~35 min)
  =========================================================
  GOAL: (a) explicitly RETIRE the false 'a single dense hyperplane structurally cannot localize to a sub-context' / 'erasing the is-a-country direction removes all countries' argument, and (b) supply replacement wording for BOTH M1' forks, grounded in the literature.
  STEP 2a -- WRITE THE RETIREMENT NOTE. State plainly WHY the old argument is false: u_sub = diff-of-means(target-sub-context-positive, sibling-positive within the same parent context) is ALSO a single dense hyperplane and DOES localize to the sub-context; the testbed already carries these per-sub-context labels (they define the forget/retain/sibling eval sets). Cite the WS1(3) fairness-editing papers (e.g. 2506.10922 affine edit, 2506.10703 linear concept removal preserving task-relevant info) as external evidence that a correctly-targeted dense direction localizes and preserves utility. Provide an exact 'DELETE this sentence / REPLACE with this sentence' list for GEN_PAPER_TEXT: remove every instance of 'structurally cannot localize', 'removes all countries', 'a dense direction over-shoots by construction', and any LEACE-as-decisive-comparator framing that depends on it. Note: LEACE / whole-parent (f) stay ONLY as a clearly-labeled SECONDARY reference, never the headline comparator.
  STEP 2b -- POSITION THE LABEL-EFFICIENCY / DISCOVERY FORK. The defensible claim if KG-ABL only MATCHES u_sub: the absorber is DISCOVERED label-free by interventional two-track grouping, whereas u_sub REQUIRES the sub-context partition (labeled target/sibling sets within the parent). Ground this in:
    - Peng et al. 'Use SAEs to Discover Unknown Concepts, Not to Act on Known Concepts' 2506.23845 (CONFIRMED authors: Kenny Peng, Rajiv Movva, Jon Kleinberg, Emma Pierson, Nikhil Garg; preprint, no venue). fetch_grep for the verbatim thesis ('SAEs may be less effective for acting on known concepts ... powerful for discovering unknown concepts'). Frame CCRG as the constructive instantiation: SAE grouping DISCOVERS the sub-context handle that a labeled dense direction would otherwise need supervision to find -- 'discover, then optionally act on what you discovered.'
    - Label-efficiency / weak-supervision / label-free framing: search 'sparse autoencoder label-free feature discovery without concept supervision'; candidates 'Beyond Interpretability: When/Why/How SAEs Enable Label-Free Visual Steering' 2506.01247; SAE-unsupervised-feature-discovery framing generally. Establish the general principle (SAE latents are obtained with NO concept supervision) so 'no sub-context labels needed' is a recognized value axis, not a bespoke claim.
  STEP 2c -- WRITE BOTH M1' FORK PARAGRAPHS (drop-in for GEN_PAPER_TEXT, since the iter-6 experiment result is not yet known at positioning time):
    - FORK-WIN (KG-ABL beats u_sub, joint CI excl 0 on >=1 case): 'a discovered single SAE feature beats even a sub-context-labeled dense direction at parent-preserving sub-context removal' -- the strong contribution; distinguish from all WS1 methods (none compare a discovered single absorber against a sub-context-targeted dense baseline).
    - FORK-MATCH (KG-ABL matches u_sub without sub-context labels): 'KG-ABL matches a sub-context-targeted dense direction WITHOUT requiring the sub-context partition' -- the label-efficiency/discovery contribution; cite Peng + label-free SAE framing; concede u_sub is competitive given labels (consistent with AxBench/DeepMind dense-beats-SAE concession, already carried).
    - Include the matched-forget + identical-judge + KL/PPL corroboration framing so the comparison reads as fair.
  GUARDRAIL: do NOT overclaim label-efficiency as cost-free -- note that interventional grouping itself uses content counterfactual pairs (an unlabeled-but-not-free signal); state the honest cost comparison (counterfactual pairs vs sub-context partition labels).

  =========================================================
  WS3 -- CITATION FINALIZATION (~30 min)
  =========================================================
  For every NEW WS1/WS2 paper the report cites, fetch the arXiv abstract page (and fetch_grep for venue/author strings) and record: arXiv-id, exact title, FULL author list (do NOT abbreviate or invent), venue+year (or 'preprint, no venue' if none found), and a one-line role. Specifically verify (best current guesses to confirm, not assume):
    - BiasEdit 2503.08588 -> check ACL Anthology 2025.trustnlp-main.13 (TrustNLP 2025 Workshop @ ACL/NAACL -- confirm which) for the camera-ready venue + authors.
    - 'Robustly Improving LLM Fairness ...' 2506.10922 -> check OpenReview fHBb8BisyW for any conference acceptance vs preprint.
    - 'Unveiling Entity-Level Unlearning' -> ACL Anthology 2025.coling-main.358 = COLING 2025 (confirm authors).
    - debiaSAE 2410.13146; SAEs-healthcare-racial-bias 2511.00177; SteerRM 2603.12795; 2602.24014; 2606.12088; 2506.10703; 2506.00876; DFSU 2601.15595; label-free-visual-steering 2506.01247 -> fetch each, record venue (likely several preprints/workshops), flag any with future-dated IDs (2601/2602/2603/2606) as 2026 preprints unless a venue is found.
    - RESOLVE the carry-forward flags: Deng 2506.18141 (NeurIPS-2025 track?), Muchane 2506.01197 (OpenReview C7M6F0OJ1l acceptance?), SAEmnesia 2509.21379 / SNCE 2509.21008 author lists.
  Re-confirm (cheap, only if a single search/fetch each is enough) the highest-stakes carry-forward venues that GEN_PAPER_TEXT will print prominently: Chanin=NeurIPS2025, AxBench/SAEBench=ICML2025, CanonicalUnits/PS-Eval=ICLR2025, Farrell=NeurIPS2024-Safe-GenAI-Workshop, SAUCE=ICCV2025-CVF (arXiv withdrawn), CRISP=ACL2026, SSPU=EMNLP2025, LEACE=NeurIPS2023, Peng=preprint. If any quick check contradicts the locked value, FLAG it; otherwise carry verbatim.
  DELIVERABLE 3 (report section C): the UPDATED locked-citation TABLE (all carry-forwards + all new entries, columns: key | arXiv-id | title | authors | venue+year | modality/role | status[LOCKED/FLAGGED]) + a ready-to-paste BibTeX block for the NEW entries + a corrections/additions diff vs the iter-5 table + an explicit 'UNRESOLVED -- verify at bib-time, do NOT invent' list (any author lists or venues not positively confirmed).
  HARD RULE: never fabricate an author list or venue. If unconfirmed, write 'authors unverified -- fetch at bib-time' and cite as preprint.

  =========================================================
  WS4 -- ASSEMBLE OUTPUTS + PRESENTATION-STRIP CHECKLIST (~15 min)
  =========================================================
  Write research_report.md with sections: (A) M2' safety cite-and-distinguish block + conjunction novelty boundary + both-branches honest-null framing; (B) M1' u_sub label-efficiency positioning -- the retirement note (DELETE/REPLACE list) + both fork paragraphs + Peng/label-free grounding; (C) updated locked-citation table + BibTeX + corrections diff + unresolved flags; (D) UPDATED presentation-strip checklist for GEN_PAPER_TEXT.
  Section D checklist must add to the iter-4/iter-5 checklist these iter-6-specific items: (i) LEAD with the M1' KG-vs-u_sub result + any M2' safety win (not whole-parent erasure); (ii) DELETE every 'structurally cannot localize' / 'removes all countries' / 'dense over-shoots by construction' sentence (give the exact strings); (iii) keep whole-parent (f)/LEACE ONLY as a labeled SECONDARY reference; (iv) include whichever M1' fork (WIN vs MATCH) and whichever M2' branch (safety-win vs honest-null) the experiments produced -- both drop-in paragraphs supplied; (v) keep a dedicated HONEST-NEGATIVES section listing: no dense-probe out-classification, toxicity co-firing predicted LOSS, 0/28 professions, router at chance out-of-sample, single-absorber-not-grouping, single-judge centerpiece risk, numeric below-gate; (vi) strip iteration/rebuttal/infra scaffolding (iterN, M1..M8, art_<id>, reviewer MAJOR/MINOR, torch/CUDA strings, selectivity-artifact bookkeeping) to the appendix or out entirely.
  Then write research_out.json: title; summary; answer (a thorough prose synthesis of A-C with the conjunction boundary, the retirement of the false argument, both forks, and the citation status); sources[] (every fetched URL with index/url/title/summary one-liner -- include the iter-4/iter-5 carry-forward anchors you re-touched plus all new WS1/WS2/WS3 papers); follow_up_questions[] (e.g.: should the paper run a small identity-sub-context absorption screen to convert the honest-null into a positive scoping result; is one Peng rebuttal paragraph enough or should the conjunction boundary go in the abstract; should the label-efficiency claim quantify the label cost of u_sub vs the counterfactual-pair cost of grouping).
  VALIDATION before finishing: (a) every citation in the report has a fetched source URL behind it; (b) no invented authors/venues -- unconfirmed ones are flagged; (c) both M1' forks AND both M2' branches have drop-in wording; (d) the 'structurally cannot localize' argument is explicitly retired with replacement text; (e) research_out.json is valid JSON with all four keys and parses. If a target paper 404s or is paywalled, record the failure, try the arXiv/ACL-Anthology/OpenReview mirror, and if still unreachable cite it as 'unverified -- bib-time' rather than dropping the distinguisher.

  FAILURE SCENARIOS TO HANDLE: (1) WS1 surfaces a true precedent for the exact conjunction -> narrow the novelty claim and report it, do not suppress. (2) The fairness-editing papers turn out to NOT cleanly preserve utility at sub-context granularity -> still usable as 'dense direction can localize given labels' evidence; note any caveats. (3) Several candidate IDs are 2026 future-dated preprints with no venue -> cite as preprints, flag, do not inflate. (4) Peng full text unreachable -> the abstract + the iter-5 carry-forward quote suffice; reuse the verified iter-5 framing.
explanation: >-
  This artifact closes the literature-positioning gaps for the TWO new load-bearing iter-6 gates (M1' and M2') so GEN_PAPER_TEXT
  can land the contribution as a deliberate, literature-grounded result REGARDLESS of which experimental fork the parallel
  iter-6 experiments produce. The iter-5 reviewer raised two publication-gating MAJORS: (R1) the M1 downstream 'win' was near-tautological
  because it beat only a WHOLE-PARENT dense erasure, and the paper's load-bearing structural argument ('a single dense hyperplane
  structurally cannot localize to a sub-context / erasing the is-a-country direction removes all countries') is FALSE -- a
  sub-context-targeted dense direction u_sub also localizes; (R2) the significance ceiling is that none of the confirmed wins
  are safety-relevant. iter-6 re-runs M1 against u_sub (M1') and searches for a safety-relevant absorption-structured win
  (M2'). This research artifact supplies the positioning those experiments need: (1) a M2' cite-and-distinguish block establishing
  that CCRG's conjunction (discovered single absorber for ONE identity sub-context + parent-preserving edit + u_sub-scored)
  is distinct from the whole-group/whole-concept bias-erasure, model-editing-debiasing, fairness-association-editing, identity/PII-unlearning,
  and example-reweighting literatures -- with both a safety-WIN framing and an honest-NULL capping framing; (2) a M1' u_sub
  paragraph that RETIRES the false structural argument the reviewer flagged and replaces it with a defensible label-efficiency/discovery
  claim grounded in Peng 'Discover-not-Act' and the label-free-SAE literature, written for BOTH forks (KG beats u_sub vs KG
  matches-without-labels); (3) a refreshed venue-locked citation table so the paper's bibliography is accurate and reviewer-proof.
  Without this, GEN_PAPER_TEXT would either re-assert the false structural claim (a reviewer red flag) or present the safety/label-efficiency
  framing without the literature scaffolding that makes it land as a contribution rather than an afterthought. It is RESEARCH
  (not experiment) because it is pure synthesis/verification over published papers -- no code, no data, $0 LLM spend, cpu_light
  -- and it must be planned early because its findings shape how the M1'/M2' experimental results are framed in the final
  paper.
</artifact_plan>

<investigation_process>
1. DIVERGE: Brainstorm multiple angles/framings of the question before searching. Think across fields — what adjacent domains might have relevant insights?
2. SEARCH: Multiple queries per angle with different phrasings to discover the landscape
3. FETCH: Read promising URLs at high level. Snippets are NOT enough — fetch full pages
4. DETAIL: aii-web-tools fetch_grep for specifics from key pages/PDFs
5. CONTRAST: Actively try to disprove your emerging conclusions. Search with different phrasings, "[topic] criticism", "[topic] limitations". Check across fields — the same finding may exist under different names
6. SYNTHESIZE: Integrate into balanced conclusion
7. ITERATE: Expect to repeat steps 2-6 if findings are incomplete or one-sided. Don't settle on first results
8. SUMMARIZE: Output JSON must include 'title' and 'summary' fields
</investigation_process>

<output_requirements>
- Write research_out.json to your workspace with all findings
- Provide your finding as clear prose WITH NUMBERED CITATIONS
- EVERY factual claim must have a citation number in brackets: [1], [2], [1, 3], etc.
- Include BOTH supporting AND contradicting evidence
- Be explicit about confidence level and what would change it
- End with follow-up questions for further investigation
</output_requirements>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

Research everything specified in the artifact plan, but you may also investigate additional relevant aspects beyond what's listed. Investigate this question thoroughly.

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ResearchExpectedFiles": {
      "description": "All expected output files from research artifact.",
      "properties": {
        "output": {
          "description": "Path to research output JSON. Example: 'research_out.json'",
          "title": "Output",
          "type": "string"
        }
      },
      "required": [
        "output"
      ],
      "title": "ResearchExpectedFiles",
      "type": "object"
    },
    "Source": {
      "description": "A source used in the research.",
      "properties": {
        "index": {
          "description": "Citation number (1, 2, 3, ...)",
          "title": "Index",
          "type": "integer"
        },
        "url": {
          "description": "Full URL of the source",
          "title": "Url",
          "type": "string"
        },
        "title": {
          "description": "Title of the article/page",
          "title": "Title",
          "type": "string"
        },
        "summary": {
          "description": "Brief summary of what this source contributed",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "index",
        "url",
        "title",
        "summary"
      ],
      "title": "Source",
      "type": "object"
    }
  },
  "description": "Research artifact \u2014 structured output + file metadata.\n\nConducts thorough web research using the aii-web-tools skill.\nReturns structured JSON output with citations.",
  "properties": {
    "title": {
      "default": "",
      "description": "Descriptive title (roughly 30-90 characters). Must describe content, NOT a status message.",
      "maxLength": 90,
      "minLength": 30,
      "title": "Title",
      "type": "string"
    },
    "layman_summary": {
      "default": "",
      "description": "One-sentence plain-language summary of what this artifact does, accessible to non-experts. Used only in the per-artifact README, not in downstream prompts.",
      "maxLength": 250,
      "minLength": 80,
      "title": "Layman Summary",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Summary for downstream artifacts: what this artifact provides",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/ResearchExpectedFiles",
      "description": "All output files you created. Must include research_out.json with your research findings."
    },
    "upload_ignore_regexes": {
      "description": "Regex patterns for workspace paths that must NOT be published to the GitHub repo, matched against each file's path relative to this artifact's workspace root (POSIX form, e.g. 'cache/abc.json'). Applied ON TOP OF the deploy step's built-in exclusions. Use this for executor-specific caches, large transient intermediates, or content-addressed blob stores (e.g. a cache/ dir of thousands of hash-named files) that would bloat the repo. Examples: ['(^|/)cache/', '(^|/)\\\\.weight_cache/', '(^|/)checkpoints/']. Leave empty if every workspace file should be published.",
      "items": {
        "type": "string"
      },
      "title": "Upload Ignore Regexes",
      "type": "array"
    },
    "answer": {
      "description": "Comprehensive answer with NUMBERED CITATIONS. Cite sources by number: 'Claim [1].' or 'According to [2, 3]...'",
      "title": "Answer",
      "type": "string"
    },
    "sources": {
      "description": "All sources used, with index matching citation numbers in answer",
      "items": {
        "$ref": "#/$defs/Source"
      },
      "title": "Sources",
      "type": "array"
    },
    "follow_up_questions": {
      "description": "2-3 follow-up questions that emerged from the investigation",
      "items": {
        "type": "string"
      },
      "title": "Follow Up Questions",
      "type": "array"
    }
  },
  "required": [
    "out_expected_files",
    "answer",
    "sources",
    "follow_up_questions"
  ],
  "title": "ResearchArtifact",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-06-18 05:31:43 UTC

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

### [3] SKILL-INPUT — aii-web-tools · 2026-06-18 05:32:01 UTC

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
