# gen_art_research_1 — test_idea

> Phase: `invention_loop` · round 1 · `gen_art`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_research_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-17 13:48:12 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_research_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_research_1/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_research_1/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_research_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

<artifact_plan>
id: gen_plan_research_1_idx1
type: research
title: >-
  Implementation Dossier for Two-Track CCRG: SAE Pipeline, 11-Baseline Suite, Steering/Model-Diffing/Statistics Protocols
summary: >-
  A web-research plan that produces one consolidated, code-ready implementation dossier (research_report.md + research_out.json)
  covering: (1) the verified frozen-SAE encoding pipeline on Gemma-2-2b via sae_lens/Neuronpedia; (2) the two-track CCRG algorithm
  pinned to concrete libraries and parameters (STEP 1-5 + Tier-0 proposal pilot); (3) every baseline (a)-(k) specified as
  runnable code with library + API; (4) steering (AxBench), model-diffing, and statistics (paired bootstrap/McNemar/MDE/Holm-Bonferroni)
  protocols; (5) a verified citation table. Goal: iteration-2 experiments can be coded with zero methodology ambiguity.
runpod_compute_profile: cpu_light
question: >-
  What are the exact, verified library APIs, model/SAE artifact identifiers, algorithmic parameters, baseline implementations,
  evaluation protocols, and statistical procedures needed to implement the two-track Counterfactual Co-Response Grouping (CCRG)
  method end-to-end on frozen Gemma Scope SAEs, such that an executor can write working iteration-2 code without any remaining
  methodology ambiguity?
research_plan: |-
  DELIVERABLE & SCOPE. Produce ONE consolidated implementation dossier: research_report.md (the human-readable spec, organized by the five workstreams A-E below) plus research_out.json with {answer (executive summary of every pinned decision), sources (every URL consulted, deduplicated, with a one-line note on what each established), follow_up_questions (open items the experiment executor must resolve at runtime, e.g. exact sae_lens return signature on the installed version)}. This is a PURE WEB-RESEARCH artifact: NO code execution, NO downloads, NO experiments. The output is a decision-complete blueprint. Keep the technical core inside reviewer-evaluable areas (clustering, feature selection, classification, knowledge graphs, IR, LLMs/deep learning); robustness/DRO content is supporting only. WHERE DECISIONS ARE NEEDED, give a primary recommendation AND a named fallback with the trigger condition. Mark every concrete claim with the source that established it. A sibling research artifact (research_iter1_dir2) owns the FORM-FREE absorption diagnostic details + minimal-pair DATA SOURCING; this dossier covers the absorption diagnostic only at the depth the Tier-0 pilot and KG-edge scoring need, and explicitly cross-references dir2 rather than duplicating data-sourcing.

  === WORKSTREAM A: FROZEN-SAE ENCODING PIPELINE (verify, do not assume) ===
  A1. SAE artifact identifiers. CONFIRMED starting points (verify each still resolves and record exact strings): primary load-bearing SAE = sae_lens release `gemma-scope-2b-pt-res-canonical`, sae_id `layer_12/width_16k/canonical` on base model `google/gemma-2-2b` (W_dec expected ~[16384, 2304]; d_model(gemma-2-2b)=2304). Fetch the SAELens docs (https://decoderesearch.github.io/SAELens/dev/ and /usage/) and the HF model card (https://huggingface.co/google/gemma-scope-2b-pt-res) to confirm. RECORD: (i) the exact `SAE.from_pretrained(...)` RETURN SIGNATURE on current sae_lens (older versions return `(sae, cfg_dict, sparsity)` tuple; newer return the SAE object or use `from_pretrained_with_cfg_and_sparsity`) — this is a known gotcha, give the version-conditional code; (ii) whether Gemma Scope uses JumpReLU activation and what 'firing' means (a_l>0 post-threshold) and how to obtain the threshold/encode acts via `sae.encode(acts)`; (iii) the hook point name for layer-12 residual stream (`blocks.12.hook_resid_post`).
  A2. Model-diffing pair. Find and PIN the instruction-tuned counterpart for the model-diffing demo: candidates to verify are `gemma-scope-2b-it-res` / a sae_lens `gemma-scope-2b-it-res-canonical` release on `google/gemma-2-2b-it`, vs the older `jbloom/Gemma-2b-IT-Residual-Stream-SAEs` (`gemma-2b-it-res-jb`). REQUIREMENT: the pt and it SAEs must share layer (12) and width (16k) so unit definitions transfer. Beware the distractor 'Gemma Scope 2' suite (it targets the Gemma-3 family, NOT gemma-2-2b) — explicitly note this trap. State the recommended pt/it pair and the exact load strings.
  A3. Width robustness axis. Confirm the 65k-width release/sae_id (`.../width_65k/canonical`) exists for the drop-first width-sensitivity axis; note absorption is reported worse at wider SAEs (motivates the axis).
  A4. Runtime / wiring. Document: (a) `HookedSAETransformer` from sae_lens vs running the SAE manually on cached residuals via TransformerLens `run_with_cache`; (b) recommended way to get per-token and mean-pooled latent activations for a batch of minimal pairs; (c) single-GPU feasibility for a few thousand pairs per concept (mean-pool over tokens, fp16, chunked encode) — give a back-of-envelope memory note (16k latents x few-thousand pairs is small; residual caching dominates). (d) Neuronpedia: find the API/endpoint for retrieving a latent's auto-interp label, top-activating examples, and logit-lens/top-promoted tokens (needed for human-auditable unit definitions and the LLM-judge member-labeling demo). Record base URL + example endpoint shape for `gemma-2-2b` layer-12 16k features.

  === WORKSTREAM B: TWO-TRACK CCRG ALGORITHM — CONCRETE, PARAMETERIZED SPEC ===
  Goal: turn STEPS 1-5 + the Tier-0 pilot into pseudocode-level instructions with named libraries and every threshold pinned (with a default value AND how to stability-select it).
  B1. STEP-1 content-response matrix. Specify building R[L x |P|] where r_l(p)=a_l(x_on)-a_l(x_off) on mean-pooled (or last-token) encode activations; firing support F_l(p)=1[a_l(x_on)>0]. Content-responsive prefilter: mean r_l above the 95th-pct of a SHUFFLED-PAIR null (define the shuffle: permute on/off assignment within concept). Cover set C_l = {p : r_l(p)>tau_resp AND a_l fires on x_on AND per-latent content-response precision on its firing support >=0.7}. Pin tau_resp as a quantile of the null (recommend) vs absolute; specify precision definition (fraction of pairs in firing support where r_l>0 / correct direction).
  B2. STEP-2 C-TRACK (splitting). Affinity A_C[l,l'] = positive part of Spearman correlation of content-response profiles (DiffCoEx sign-aware soft-threshold: recommend power/soft-threshold beta on the signed correlation, cite DiffCoEx BMC Bioinformatics 2010 and WGCNA for the soft-threshold rationale; record the exact DiffCoEx transform sign((1+rho)/2)*|((1+rho)/2)|^beta or the simpler positive-part threshold and recommend one). Build igraph weighted graph; run Leiden via `leidenalg.find_partition`. PIN: partition type = `RBConfigurationVertexPartition` with `weights=g.es['weight']` and a resolution parameter (note ModularityVertexPartition has no resolution knob and needs positive weights — positive-part affinity satisfies that). Community count fixed by modularity + bootstrap-ARI stability vs shuffled-pair null: specify the bootstrap-ARI stability-selection recipe (resample pairs B times, recompute partitions, pick resolution maximizing mean pairwise Adjusted Rand Index while exceeding the null). Cite the Leiden algorithm (Traag et al. 2019) and give the python-igraph + leidenalg install/usage from leidenalg.readthedocs.io.
  B3. STEP-3 K-TRACK (absorption) anchored greedy max-coverage. Specify in full: ANCHOR = argmax_l |C_l| over content-responsive latents (highest recall; tie-break by broadest, lowest-entropy firing support) — chosen using ONLY the pairs, NOT the Chanin diagnostic (state why: keeps 'unsupervised unit beats supervised oracle' non-circular). HOLES H = P \ C_anchor. GREEDY loop: while H non-empty and improving, add l* = argmax_l |C_l ∩ H| subject to (i) firing Jaccard < 0.1 with every current member, (ii) per-member precision >= 0.7, (iii) marginal coverage gain |C_l* ∩ H|/|P| >= 0.05 with a bootstrap CI excluding 0; then H <- H \ C_l*. Cite the maximum-coverage / set-cover greedy (1-1/e) guarantee (Nemhauser-Wolsey-Fisher 1978; Feige 1998) as the algorithmic justification. Note it is plain Python (no special library) — give the loop structure and the bootstrap-CI-on-marginal-gain recipe (resample pairs, recompute gain).
  B4. STEP-4 reconciliation. Per C-community designate its highest-recall member as a candidate anchor and run STEP-3 K-augmentation to pull in mutually-exclusive absorbers for that community's holes; ALSO seed STEP-3 from standalone high-recall latents in no dense community. A unit is a pure C-community, pure K-cover, or hybrid. De-duplicate; assign each latent to its highest-coverage-gain unit. Specify the de-dup/assignment rule concretely.
  B5. STEP-5 admission filter. Admit iff signature C (within-unit mean content-response correlation > 95th-pct shuffled-pair null) OR signature K (pooled-max content-response AUC minus best-single-member AUC > 95th pct of a best-of-random-k null MATCHED on marginal content-response AUC, PLUS at k in {2,3} the absolute >=0.05 gain floor with CI excluding 0, PLUS mutual-exclusivity Jaccard<0.1 and per-member precision>=0.7), AND unit-level surface invariance (pooled surface-response not above the shuffled-surface null). Specify: how to construct the MATCHED random-k null (sample k content-responsive latents matched on marginal AUC bins), and report false-admit rate under BOTH the all-latent and matched-random-k nulls (target <=0.05). Give the exact pooling rule (max vs sum over members) used everywhere downstream — recommend max-pool for detection, note sum as ablation.
  B6. TIER-0 PROPOSAL PILOT. Specify the never-dropped check: run STEP-3 on first-letter given ONLY content-flip pairs; compute membership precision/recall of the proposed anchor+absorbers vs the parent+absorbers the Chanin 2409.14507 diagnostic identifies (using the sae-spelling repo's diagnostic — see B7), against a random-membership null. Define pass/fail and the honest-negative report if it fails.
  B7. Absorption diagnostic (only as needed for pilot + KG-edge scoring). From github.com/lasr-spelling/sae-spelling and the paper (arxiv 2409.14507 / its OpenReview PDF), extract: how the parent latent is identified (max encoder-cosine with an LR probe) and how the absorbing latent is found (ablation effect on the relevant logit / probe). Then specify the FORM-FREE generalization for the non-spelling testbed (train an LR probe for the parent concept; for each false-negative example find the latent whose ablation most shifts the concept logit) at implementation level. NOTE explicitly that detailed minimal-pair sourcing and the deeper form-free diagnostic write-up live in research_iter1_dir2; here, only give what the pilot and KG-edge agreement metric require, and cross-reference.

  === WORKSTREAM C: ELEVEN BASELINES (a)-(k) — EACH AS A RUNNABLE SPEC ===
  For each, state: input representation, library + function, selection/training procedure, count-matching rule, and output used for the metric.
  (a) best raw single latent: pick the SAE latent with max held-out content-response AUC / classification F1; trivial.
  (b) observational co-activation / feature-family clusters: cluster latents by CO-FIRING (e.g., binarized co-activation correlation / Jaccard over a corpus) using HDBSCAN (sklearn `cluster.HDBSCAN` or `hdbscan`), then COUNT-MATCH to the unit's member count k (take the top-k members by the same pooling/AUC rule). Specify the co-activation feature matrix construction.
  (c) decoder-geometry clusters: cluster latents by W_dec cosine similarity (agglomerative or HDBSCAN on cosine), COUNT-MATCHED to k. Specify cosine-affinity construction.
  (d) counterfactually-matched diff-of-means: mean(residual delta on content-on) - mean(content-off) as a direction; score by projection. On residual-stream deltas (NOT SAE space).
  (e) counterfactually-matched linear probe: logistic regression (sklearn `LogisticRegression`) on residual deltas with the content label.
  (f) LEACE surface-invariant single hyperplane: take (d)/(e) but first ERASE the surface-flip direction with `concept_erasure.LeaceEraser` (pip install concept-erasure; fit on residuals with surface-flip as the concept Z, then apply eraser before fitting the content probe). This is the conceded single dense hyperplane. Cite LEACE 2306.03819 and link the EleutherAI/concept-erasure repo + the leace.py API (LeaceFitter.update / .eraser, LeaceEraser.fit(X,Z), eraser(X)).
  (g) supervised oracle pool (SCR/TPP top-N): rank SAE latents by SCR/TPP probe-attribution causal effect and pool the top-N. From github.com/adamkarvonen/SAEBench (use the `stable_paper_version` branch for pinned deps): extract exactly how SCR (Spurious Correlation Removal) and TPP (Targeted Probe Perturbation) rank/select latents (attribution patching / probe-attribution effect), and how many N. Give the function/module names and the selection metric.
  (h) count-and-pool-matched probe: max-pool over EXACTLY #members raw RESIDUAL directions chosen by the SAME SCR/TPP attribution as (g) — isolates SELECTION vs marginal-attribution at fixed pool size. Specify how to extract raw residual directions for the top-N attributed latents.
  (i) unmatched diff-of-means/probe on raw labels (no counterfactual matching): naive baseline for the nesting (A).
  (j) oracle group-DRO probe: dense probe trained with a group-DRO objective on TRUE independent sub-context labels = robustness UPPER BOUND. Cite Sagawa et al. group-DRO (1911.08731) and Mind-the-GAP (2403.09869); give the standard group-DRO loss (per-group loss, max over groups) and a minimal training recipe.
  (k) label-free group-inference probe: JTT-style high-loss upweighting (2107.09044 — train ERM, upweight misclassified, retrain) OR GEORGE-style representation clustering + group-DRO (2011.12945 — cluster features, treat clusters as noisy subclass labels, group-DRO). Also note EIIL (2010.07249), LfF (2007.02561), Diverse Prototypical Ensembles (2505.23027) as the competitor family. Recommend JTT as primary (k) for simplicity; give the two-stage recipe and the upweight factor convention.
  Also confirm the COUNT-MATCHING convention used across (b)/(c)/(h): cut to the unit's exact k members by the same pooling rule.

  === WORKSTREAM D: PROTOCOLS (steering, model-diffing, statistics) ===
  D1. Steering side-effect protocol (AxBench-style). From AxBench (2501.17148; arxiv abs/pdf + repo if findable) and the steering-side-effect literature, specify: (i) how to apply a steering vector (unit direction = mean/sum of member decoder vectors, alpha = c * R scaling, added at the residual hook via run_with_hooks); (ii) ON-TARGET effect measure at MATCHED strength; (iii) COLLATERAL = KL divergence on UNRELATED prompts (full-vocab next-token KL) — cite the KL-on-unrelated protocol; (iv) FLUENCY via an LLM-judge on {0,1,2} through OpenRouter (give the rubric and that fluency is LLM-judge not perplexity). State the null floor (shuffle null). Note this is a GENERALITY demo, not load-bearing; the minimal version always runs, decisive version is Tier-2.
  D2. Model-diffing protocol. Specify: using the paired pt/it SAEs (A2), test whether the unit detects a base-vs-it concept-usage shift more reliably than the best single latent, above a shuffle null. Describe the measure (e.g., difference in unit-pooled activation distribution between pt and it on the same probes; AUC of detecting which model produced an activation). Keep minimal version always-run.
  D3. Statistics. Pin: (i) PRIMARY object = per-concept / within-family PAIRED bootstrap CIs (B=10000) on per-example correctness differences; cross-family number is DESCRIPTIVE only (variance not estimable over ~3-4 families). (ii) For the central unit-minus-(g)/(h) worst-sub-context-recall gap: paired bootstrap on per-example correctness diffs + EXACT McNemar (scipy/statsmodels `mcnemar`) confirmatory; primary reported quantity = the gap's SIGN and its SLOPE vs measured reweighting magnitude (bootstrap CI on the slope). (iii) A-PRIORI MDE (proportion, conservative unpaired): n ≈ 7.84*[p1(1-p1)+p2(1-p2)]/Δ^2 → ~91 positives for Δ=0.20, ~167 for 0.15, ~384 for 0.10; PRE-REGISTER n_min=150 positive examples per tested under-served sub-context with stratified collection; rarer sub-contexts reported descriptively only. (iv) MULTIPLICITY: Holm-Bonferroni across the headline claim family (give the ordered-p-value procedure and which comparisons are in the family). (v) Cluster-stability: bootstrap Adjusted Rand Index / Jaccard vs shuffled-pair null (sklearn `adjusted_rand_score`). Name the exact scipy/statsmodels/sklearn functions for each test.
  D4. Auditability metrics. Specify the MEASURED repair loop (pick under-served sub-context = recall hole on (f); read KG to find covering absorber; ADD it; measure recall before/after with bootstrap CI vs a random-content-responsive-latent-addition control) and the LLM-judge MEMBER-LABELING agreement (give each member's logit-lens tokens + top contexts to an OpenRouter judge, ask which sub-context it covers, compare to KG edge vs a shuffled-label null). Give the OpenRouter call pattern and a cheap model recommendation, with a note that total LLM spend must stay well under the $10 cap (estimate per-call and total).

  === WORKSTREAM E: CITATION / ARXIV VERIFICATION TABLE ===
  Verify EVERY arXiv ID and venue cited in the hypothesis and resolve title+year+venue; produce a table {claimed_id, resolves?, actual_title, venue/year, one-line role}. CONFIRMED so far (re-state, don't re-verify unless quick): 2409.14507 (A is for Absorption, NeurIPS 2025), 2505.11756 (Feature Hedging), 2501.17148 (AxBench, ICML 2025), 2502.04878 (SAEs Do Not Find Canonical Units, ICLR 2025), 2411.18895 (SCR/TPP eval, Karvonen), 2306.03819 (LEACE), 2107.09044 (JTT), 2011.12945 (GEORGE), 2010.07249 (EIIL), 2007.02561 (LfF), 2505.23027 (Diverse Prototypical Ensembles), 2403.09869 (Mind-the-GAP group-aware priors), 2106.00545 (Veitch counterfactual invariance), 2205.14140 (CEBaB), 2505.07073 (CDLC). MUST-VERIFY (recent/future-dated, higher fabrication risk — flag any that DO NOT resolve and propose the closest real substitute): 2606.06333 (SASA Subspace-Aware SAEs), 2604.23829 (Domain-Filtered KGs from SAE Features), 2408.00657 (Disentangling Dense Embeddings), 2506.18141 (Sparse Feature Coactivation), Sagawa group-DRO (confirm 1911.08731), DiffCoEx (BMC Bioinformatics 2010) and WGCNA citations, Nemhauser-Wolsey-Fisher 1978 / Feige 1998 (max-coverage), Traag 2019 (Leiden), ParaDetox (ACL 2022), Kaushik CAD (ICLR 2020). For any non-resolving ID, do NOT silently keep it — record it in follow_up_questions and supply the best-matching real reference.

  === OUTPUT STRUCTURE (research_report.md) ===
  One section per workstream A-E. Each technical decision = a short subsection with: PINNED VALUE/LIBRARY, the source URL that established it, and a FALLBACK with its trigger. Include a final 'OPEN ITEMS FOR THE EXECUTOR' list (e.g., exact sae_lens return signature on installed version, confirmed it-SAE release string, Neuronpedia rate limits) mirrored into research_out.json.follow_up_questions. Prefer official docs/repos over blogs: SAELens docs, HF model cards, SAEBench repo (stable_paper_version), EleutherAI/concept-erasure, leidenalg.readthedocs.io, lasr-spelling/sae-spelling, AxBench repo/paper, and the primary arXiv PDFs (use fetch_grep for exact API signatures, function names, and parameter values rather than relying on lossy summaries).
explanation: >-
  This dossier is the methodological foundation for the entire CCRG invention. The iteration-1 strategy is a foundation iteration
  with no runnable experiments yet; the two RESEARCH artifacts must de-risk every implementation decision so that iteration-2
  GPU experiments can be coded directly. The hypothesis is unusually specification-heavy (a named two-track algorithm with
  five steps, eleven baselines, multiple null models, and a pre-registered statistical plan), and its credibility depends
  on each piece mapping to a real, verified library/API and a real citation. The single biggest execution risk is methodology
  ambiguity at code-time: the wrong sae_lens return signature, an unverified IT-SAE release for model-diffing, a misremembered
  SCR/TPP selection rule, or a fabricated future-dated arXiv ID would each silently corrupt the load-bearing core (Tier-0
  pilot + count-matched C1 + C3 absorber-recovery). By verifying SAE artifact strings, pinning the C-track (leidenalg) and
  K-track (greedy max-coverage) to concrete code, specifying all eleven baselines (LEACE for (f), SAEBench for (g)/(h), JTT/GEORGE
  for (k)), and locking the statistics (paired bootstrap, McNemar, MDE n_min=150, Holm-Bonferroni), this research removes
  that ambiguity. It also enforces the reviewer-scope constraint (clustering / feature selection / classification / knowledge
  graphs) and the $10 OpenRouter budget for the LLM-judge components, keeping the contribution evaluable and feasible on a
  single GPU.
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

### [2] HUMAN-USER prompt · 2026-06-17 13:48:12 UTC

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

### [3] SKILL-INPUT — aii-web-tools · 2026-06-17 13:48:24 UTC

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
