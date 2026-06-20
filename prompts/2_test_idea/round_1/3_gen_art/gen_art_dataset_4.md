# gen_art_dataset_4 — test_idea

> Phase: `invention_loop` · round 1 · `gen_art`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_dataset_4` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-17 14:03:34 UTC

```
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
Find, evaluate, and prepare high-quality datasets for the research experiment.
Adapt your search strategy based on the hypothesis and domain requirements.
</task>

<common_mistakes_to_avoid>
Critical pitfalls from past runs. MUST check for and avoid each one.

**1. Picking Obscure or Unusable Datasets**
Do NOT select datasets just because they match a keyword. Red flags: very few downloads (<100), no documentation (dataset card, paper, or GitHub page). Prefer well-used datasets (not necessarily popular or widely known) with clear documentation.
CHECK: >100 downloads? Has documentation? If any "no" → find a better dataset.

**2. Fabricating Dataset Provenance**
Do NOT invent justifications for why a dataset is relevant. If a dataset name contains a number (e.g., "797"), do NOT assume it refers to a specific benchmark suite, OpenML ID, or paper without verification. In past runs, an agent assumed "797" referred to "OpenML benchmark suite 797" with zero evidence, then fabricated a rationale. This was completely false.
CHECK: Can you cite a specific, verifiable source (paper, benchmark page, dataset card) confirming this dataset is what you claim? If not, do not make provenance claims.

**3. Not Verifying Dataset Usefulness**
Always sanity-check that a dataset is actually suitable for the task before committing. Download a sample, inspect the features, and run a quick baseline appropriate for the domain. If the dataset lacks signal or structure for the hypothesis being tested, the entire experiment is wasted.

**4. Settling for the Only Search Result**
If your search returns only 1-2 results, your search terms are too narrow. Broaden your queries, try different keyword combinations, or search for well-known benchmark datasets in the domain. A single obscure result from a narrow query should never be your final choice.
CHECK: Fewer than 5 candidate datasets? Run additional searches with broader or different terms before making a selection.
</common_mistakes_to_avoid>

<critical_requirements>
- Keep final response under 300 characters
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

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_4`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_4/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_4/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_4/results/out.json`
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
id: gen_plan_dataset_4_idx6
type: dataset
title: >-
  Supporting concept families + boundary-null dataset (CAD-IMDB sentiment, CEBaB food+service aspect, bias_in_bios) standardized
  to the CCRG shared minimal-pair schema
summary: >-
  Acquire and standardize THREE real, human-annotated HuggingFace/GitHub datasets into the CCRG two-track-grouping pipeline's
  shared JSON schema: (1) Kaushik 2020 CAD-IMDB human counterfactually-edited positive<->negative review pairs as a SUPPORTING
  sentiment family; (2) CEBaB human FOOD+SERVICE aspect edits as a SUPPORTING restaurant aspect-sentiment family (food+service
  nested as ONE family, with all four aspect-level majorities retained as INDEPENDENT sub-context labels); (3) LabHC/bias_in_bios
  profession-labeled biographies (gender as the independent sub-attribute) as the pre-registered BOUNDARY-NULL where habitat~=label.
  Each is reformatted to one-row-per-text with content-flip minimal pairs reconstructable via pair_id, concept labels, independent
  sub-context labels, content/surface pair flags, and train/dev/test folds. Schema-validate; emit full/mini/preview per family;
  keep families cleanly separated in metadata so downstream per-family bootstrap CIs (primary) compute cleanly and cross-family
  aggregates stay descriptive. No LLM calls needed (all human-annotated) -> $0 OpenRouter spend.
runpod_compute_profile: cpu_heavy
ideal_dataset_criteria: |-
  THREE REAL, downloadable, human-annotated datasets (no synthesis), each <=300MB, standardized to ONE shared JSON schema so iteration-2+ can run Tier-1b supporting families and the boundary-null through the identical CCRG pipeline.

  FAMILY 1 - SENTIMENT (supporting): Human counterfactually-EDITED minimal pairs flipping sentiment positive<->negative, with the ORIGINAL<->REVISED mapping PRESERVED so each pair is a clean content-flip (x_off, x_on) where only sentiment-bearing content changed and surface/topic is held as constant as the human editor allowed. Ideal = Kaushik/Hovy/Lipton ICLR-2020 CAD-IMDB (Amazon Mechanical Turk minimal revisions). Native train/dev/test folds. Tiny (few MB).

  FAMILY 2 - RESTAURANT ASPECT-SENTIMENT (supporting, food+service nested as ONE family): Human aspect edits that flip a SINGLE aspect's sentiment (food, service) while holding other aspects fixed, with per-aspect majority labels retained as INDEPENDENT sub-context labels (food/service/ambiance/noise). Ideal = CEBaB (Abraham et al. NeurIPS 2022). These independent aspect labels are exactly what the hypothesis's degenerate-construction guard needs (sub-contexts defined BEFORE any unit is formed). ~18.6k texts.

  FAMILY 3 - BOUNDARY-NULL (bias_in_bios): Profession-labeled biographies where the 'habitat' approximately equals the class label, so co-response grouping is PREDICTED to give no advantage (a publishable expected null, NOT method failure). Needs profession label (concept) + an independent sub-attribute (gender) usable as a sub-context. Ideal = LabHC/bias_in_bios (266MB full; subsample to keep output JSON manageable).

  SHARED-SCHEMA REQUIREMENTS for all three: one row per TEXT with {id, input(text), output(canonical concept label), family, dataset_source, concept, concept_label, sub_context(dict of independent labels), pair_id(links minimal-pair members; null if unpaired), pair_role(content_off|content_on|null), partner_id, flip_type(content|null), is_content_pair(bool), is_surface_pair(bool=false for all three), fold(train|dev|test), meta(source-specific raw fields)}. Families MUST be separable by the 'family' field. Surface-flip pairs are NOT natively available in any of these three and must NOT be fabricated here (out of scope; the schema reserves the surface fields for sibling LLM-generated/ParaDetox artifacts). Every text and its counterfactual share a pair_id so downstream can encode (x_off, x_on) deltas. License/provenance recorded per family.
dataset_search_plan: |-
  Use the aii-hf-datasets skill for HF pulls and plain HTTPS/requests for GitHub raw TSVs. Use aii-json to author the shared JSON Schema and to emit full/mini/preview + validate. NO LLM/OpenRouter calls are required (all three are human-annotated) -> $0 spend. Work family-by-family; write all three into ONE data_out.json with a 'family' discriminator (plus per-family full/mini/preview if the file-size limit requires splitting).

  === STEP 0: DEFINE THE SHARED JSON SCHEMA (write schema.json first) ===
  Author a JSON Schema for a row object with these fields (one row per TEXT):
  - id: string, globally unique, family-prefixed (e.g. 'sent_0001', 'cebab_food_0001', 'bib_0001').
  - input: string, the raw text (movie review / restaurant review / biography). REQUIRED non-empty.
  - output: string, the canonical concept label that a classifier predicts for this text ('positive'/'negative' for sentiment & aspect; profession-string for bios).
  - family: enum ['sentiment','restaurant_aspect','bias_in_bios_boundary'].
  - dataset_source: string provenance ('CAD-IMDB (Kaushik et al. ICLR 2020)','CEBaB (Abraham et al. NeurIPS 2022)','LabHC/bias_in_bios').
  - concept: string concept name ('sentiment' | 'food_sentiment' | 'service_sentiment' | 'profession').
  - concept_label: string (== output; kept explicit for downstream).
  - sub_context: object/dict of INDEPENDENT sub-context labels fixed BEFORE any grouping (see per-family). {} allowed.
  - pair_id: string|null linking the two members of a content-flip minimal pair (null for unpaired bios rows).
  - pair_role: enum ['content_off','content_on',null] (concept-absent vs concept-present member).
  - partner_id: string|null (the id of the other pair member; null if unpaired).
  - flip_type: enum ['content',null] (this row participates in a content flip; surface reserved/unused here).
  - is_content_pair: bool.
  - is_surface_pair: bool (FALSE for all rows in this artifact).
  - fold: enum ['train','dev','test'] (this is metadata_fold).
  - meta: object for source-specific raw fields (original raw labels, edit_goal/edit_type, char_len, token_overlap_with_partner, gender, raw profession id, etc.).
  Validate every emitted row against this schema with aii-json before finishing.

  === STEP 1: FAMILY 1 - CAD-IMDB SENTIMENT (content-flip pairs) ===
  SOURCE (primary): GitHub acmi-lab/counterfactually-augmented-data (Apache-2.0). Raw-file URLs:
    https://raw.githubusercontent.com/acmi-lab/counterfactually-augmented-data/master/sentiment/orig/{train,dev,test}.tsv
    https://raw.githubusercontent.com/acmi-lab/counterfactually-augmented-data/master/sentiment/new/{train,dev,test}.tsv
  TSV columns: 'Sentiment' in {Positive,Negative} and 'Text'. Expected rows ~1707 train / 245 dev / 488 test in EACH of orig and new (one human revision per original). Total ~4880 texts, a few MB. If raw URLs 404, fall back to: (a) git-clone the repo, or (b) search HF Hub for a mirror (e.g. query 'counterfactually augmented IMDB', candidate names like 'sentiment counterfactual'); verify any mirror has the orig<->revised mapping before use.
  PROCESSING per split s in {train(->fold train), dev(->fold dev), test(->fold test)}:
    1. Read orig/s.tsv and new/s.tsv.
    2. PAIRING (preserve original<->edited mapping = the core requirement). Primary assumption: the i-th row of new/s.tsv is the counterfactual revision of the i-th row of orig/s.tsv (row-index alignment within a split is the repo convention). MANDATORY VERIFICATION before trusting it: (i) row counts match between orig and new; (ii) per aligned pair the Sentiment is FLIPPED (orig.Sentiment != new.Sentiment); (iii) per aligned pair the texts are MINIMAL edits of each other -- compute normalized token Jaccard / character-level overlap and confirm the median aligned-pair overlap is FAR above a random-pair baseline (shuffle new within split and recompute). If (i)-(iii) all hold, accept row alignment. IF verification FAILS, fall back to bipartite matching: within each split, for each original review greedily match the opposite-label revised review with maximal token overlap (Levenshtein/Jaccard), enforce one-to-one, and drop any unmatched. Record the chosen pairing method in meta.
    3. For each accepted pair (o, r) create pair_id = 'sent_'+s+'_'+i. Emit TWO rows:
       - original o: input=o.Text, output=lower(o.Sentiment) ('positive'/'negative'), concept='sentiment', concept_label=output, pair_role = 'content_on' if o is Positive else 'content_off', partner_id = r.id, sub_context={}, flip_type='content', is_content_pair=true, is_surface_pair=false, fold=mapped, meta={raw_sentiment, role_source:'original', char_len, token_overlap_with_partner}.
       - revised r: symmetric, pair_role = the opposite of o, partner_id=o.id. (Define pair_role by the row's OWN sentiment value: Positive->content_on, Negative->content_off. This makes 'content_on' = positive-sentiment-present, consistent across the family.)
  NOTE: 'positive sentiment' is the designated concept; content_off = the negative member. Keep BOTH members so downstream can form (x_off,x_on) deltas either direction.

  === STEP 2: FAMILY 2 - CEBaB FOOD+SERVICE ASPECT (content-flip pairs + independent aspect sub-contexts) ===
  SOURCE (primary): HF dataset 'CEBaB/CEBaB' (parquet; ~18.6k rows). Load via aii-hf-datasets (datasets.load_dataset('CEBaB/CEBaB')) or pull parquet directly. Splits: train_exclusive, train_inclusive, train_observational, validation, test. Use train_inclusive as the TRAIN pool (it contains originals + all edits), validation->dev, test->test. (Document: train_inclusive is the superset; ignore the partially-overlapping train_exclusive/train_observational to avoid double counting, OR dedupe by id across all train_* and assign fold='train' -- prefer the simpler train_inclusive-only path and note it.)
  VERIFIED FIELDS: id, original_id, edit_id, is_original(bool), edit_goal in {food,ambiance,service,noise} (= which aspect the edit targeted), edit_type (5 values; INSPECT actual values and record), description(text), review_majority (sentiment string, ~5 values incl Positive/Negative/unknown/no-majority -- INSPECT), and the four aspect-majority fields food_aspect_majority/service_aspect_majority/ambiance_aspect_majority/noise_aspect_majority each in {Positive,Negative,unknown}(+possibly 'no majority'). original_id groups every edit with its base; is_original=true marks the base.
  PROCESSING:
    1. Index all rows by id; build original_id -> {original row, list of edit rows}.
    2. Build content-flip pairs ONLY for the FOOD and SERVICE aspects (food+service = the nested family; do NOT use ambiance/noise as the flipped concept, but DO retain their labels as sub-context). For each edited row e with edit_goal in {food,service} and its original o (same original_id, is_original=true):
       - Let A = edit_goal (the edited aspect). Read the binarized aspect sentiment of A on BOTH members: aspect_val(o) and aspect_val(e) from {o,e}.A_aspect_majority. KEEP the pair only if both are in {Positive,Negative} AND they DIFFER (a clean flip); DROP pairs where either side is 'unknown'/'no majority' on aspect A or where they do not differ (degenerate, no flip). Record dropped counts.
       - concept = A+'_sentiment' (e.g. 'food_sentiment'); pair_id = 'cebab_'+A+'_'+edit_id.
       - Emit TWO rows (o and e): input=description, output = 'positive' if that row's A_aspect_majority=='Positive' else 'negative', concept_label=output, pair_role = 'content_on' if positive else 'content_off', partner_id = the other member's id, flip_type='content', is_content_pair=true, is_surface_pair=false, fold from source split.
       - sub_context (INDEPENDENT labels, frozen before any unit) for BOTH rows = {edited_aspect:A, food:food_aspect_majority, service:service_aspect_majority, ambiance:ambiance_aspect_majority, noise:noise_aspect_majority, review_sentiment: binarized review_majority}. meta = {original_id, edit_id, is_original, edit_goal, edit_type, raw review_majority, restaurant metadata if present, char_len}.
    NOTE on duplication: one original may anchor several edits; emit the original once PER pair it participates in (distinct pair_id each). This duplication is small (food+service pairs are a few thousand) and keeps minimal-pair reconstruction trivial. If output size becomes a concern, instead dedupe originals and reconstruct pairs via (original_id, edit_id) -- but prefer the explicit-pair form and document the choice.
    3. Sanity: report #food pairs, #service pairs, label balance, and confirm food and service are separable via the 'concept' and sub_context.edited_aspect fields.
  FALLBACK if HF load fails: download the public JSON release from cebabing.github.io/CEBaB (linked from the project page) and map the identical fields.

  === STEP 3: FAMILY 3 - bias_in_bios BOUNDARY-NULL (unpaired labeled classification) ===
  SOURCE (primary): HF 'LabHC/bias_in_bios' (parquet, MIT, 266MB full). Fields: hard_text(string bio), profession(int 0-27), gender(int; 0=male,1=female). Splits train(257k)/dev(39.6k)/test(99.1k). 28 professions (accountant..yoga_teacher).
  PROCESSING:
    1. SUBSAMPLE to keep data_out.json manageable (full 396k bios would make the JSON > the file-size limit). Target ~21k rows total: ~15k train / ~3k dev / ~3k test. Use a FIXED seed (record it) and STRATIFY by (profession x gender) so the 28 professions and both genders stay proportionally represented; cap each stratum at min(available, target_per_stratum). Document the exact subsample procedure + seed for reproducibility, and note the full set is reproducible from the HF repo if downstream needs more.
    2. Build a profession int->string map (0:accountant,1:architect,2:attorney,3:chiropractor,4:comedian,5:composer,6:dentist,7:dietitian,8:filmmaker,9:interior_designer,10:journalist,11:model,12:nurse,13:painter,14:paralegal,15:pastor,16:personal_trainer,17:photographer,18:physician,19:poet,20:professor,21:psychologist,22:rapper,23:software_engineer,24:surgeon,25:teacher,26:yoga_teacher,27:...) -- VERIFY the exact ordering against the HF dataset's own label feature names rather than trusting this list (the dataset ships the canonical mapping in its features; use that).
    3. Emit one row per bio: input=hard_text, output=profession_string, concept='profession', concept_label=profession_string, family='bias_in_bios_boundary'. UNPAIRED: pair_id=null, pair_role=null, partner_id=null, flip_type=null, is_content_pair=false, is_surface_pair=false. sub_context={gender: 'female' if gender==1 else 'male'} (gender is the independent sub-attribute / 'habitat~=label' diagnostic axis). fold from source split. meta={raw_profession_int, raw_gender_int, char_len}.
    4. Note in family-level metadata WHY this is a boundary-null (profession habitat ~= label; expected no co-response-grouping advantage) so downstream treats a null as the pre-registered expectation, not a failure.

  === STEP 4: STANDARDIZE, VALIDATE, EMIT VARIANTS ===
    1. Concatenate all three families into data_out.json (a list of rows, OR {schema_version, families:{...}, rows:[...]}); ensure the 'family' field cleanly partitions them and ids are globally unique.
    2. Emit a family_summary block in metadata: per family report row count, #pairs (sentiment/food/service), label balance, fold sizes, sub-context value distributions, license, source URL/commit, pairing method used (CAD), subsample seed (bios).
    3. Validate EVERY row against schema.json using aii-json; fix any violations.
    4. Use aii-json to emit full / mini / preview per the skill's convention: mini ~ a few hundred rows balanced across the three families and across folds/labels (e.g. ~150-200/family preserving pairs intact -- never split a pair across the mini boundary); preview ~ 5-10 representative rows per family (include at least one full content-flip pair from sentiment and from CEBaB, and one bios row).
    5. Run aii-file-size-limit: if data_out.json exceeds the limit, first reduce the bias_in_bios subsample (it dominates size), then if still large split into per-family files (data_out_sentiment.json / data_out_cebab.json / data_out_bias_in_bios.json) each with its own full/mini/preview, and record the split in metadata.

  === STEP 5: FAILURE HANDLING / REPORT ===
  Report honestly in metadata: CAD pairing method chosen + verification stats (median aligned-pair overlap vs random baseline); CEBaB dropped-pair counts (unknown/no-flip) and final food/service pair counts; bias_in_bios subsample seed + per-stratum caps. If any single source is wholly unavailable (rare), proceed with the other two and clearly mark the missing family as NOT DELIVERED with the reason (do NOT substitute synthetic data or an unrelated dataset). Do NOT fabricate surface-flip pairs for any family (out of scope). Do NOT compute any derived statistics (MI/correlations/probes) -- raw standardized data only.
target_num_datasets: 3
</artifact_plan>



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

<available_data_sources>
Use the sources appropriate to your task. Read the relevant skill file BEFORE using each source.

- **HuggingFace Hub** (HF) — ML datasets (NLP, vision, tabular, benchmarks)
- **Our World in Data** (OWID) — Global statistics (energy, health, economics, environment, demographics)
- **Alternate methods** — Python/shell (sklearn.datasets, openml, direct URL, APIs, etc.)

If the plan specifies a source or one fits better, use it.
You may combine sources. Use web search (aii-web-tools skill) to research candidates (background, papers, provenance) — NOT to find/download datasets.
</available_data_sources>

<available_domain_handbooks>
If your domain has a handbook, read the relevant skill file BEFORE working on that domain.

- **Multi-LLM Agents** — dataset selection, evaluation metrics, agent orchestration patterns
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-python, aii-long-running-tasks, aii-json, aii-file-size-limit, aii-use-hardware, aii-parallel-computing.
TODO 2. Read skill files for your data sources (see <available_data_sources>) and domain handbook if applicable (see <available_domain_handbooks>). Based on plan and context, decide which source(s) to use. Include everything specified in the artifact plan, but you may also collect additional relevant data beyond what's listed. Run 24 diverse searches across chosen source(s) — BROAD, GENERAL terms, not very specific. Parallelize where supported.
TODO 3. Identify the 12 most promising datasets. IMPORTANT: Only consider datasets under 300MB. Preview/inspect sample rows for each candidate. Parallelize previews.
TODO 4. Research each candidate BEFORE choosing which to download. For each, search the web (aii-web-tools skill): dataset name, papers citing it, original source/task, popularity. Red flags: no search results, no papers, anonymized features (F1, F2...), <100 downloads, no documentation. Green flags: papers using it, clear documentation, meaningful features, established benchmark. Also consider: will features/structure allow meaningful evaluation of the planned method?
TODO 5. Decide which to KEEP vs DISCARD. Look for: clear structure, relevant fields, quality examples matching requirements, confirmed provenance. Determine which 6 datasets have the most suitable data. Download and save to `temp/datasets/`. Parallelize downloads.
</todos>
```

### [2] HUMAN-USER prompt · 2026-06-17 14:03:34 UTC

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

### [3] SKILL-INPUT — aii-hf-datasets · 2026-06-17 14:06:08 UTC

The agent loaded the **aii-hf-datasets** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-hf-datasets
description: Searches, previews, and downloads datasets from HuggingFace Hub. Use when user needs machine learning datasets, training data, HuggingFace datasets, dataset discovery, or .parquet/.json exports.
---

## Contents

- Workflow (3-phase dataset discovery)
- Scripts (Search, Preview, Download)

**IMPORTANT - Parallel execution:** GNU `parallel` subshells do NOT inherit `source activate`. Use `export` for variables and **single-quoted** command templates so parallel's subshells can resolve them:
```
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-hf-datasets"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

---

## Workflow: 3-Phase Dataset Discovery

### Phase 1: Search for Datasets
Find datasets with metadata (configs, splits, features, sizes)
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-hf-datasets" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_hf_search_datasets.py --query "sentiment analysis" --limit 5
```

### Phase 2: Preview Dataset (if promising)
Inspect metadata AND sample rows in one call
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-hf-datasets" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_hf_preview_datasets.py openai/gsm8k
```

### Phase 3: Download Dataset (if suitable)
Download after reviewing the preview
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-hf-datasets" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_hf_download_datasets.py openai/gsm8k --config main --split train
```

---

## Scripts

### Search HuggingFace Datasets (aii_hf_search_datasets.py)

Search and discover datasets on HuggingFace Hub.

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-hf-datasets" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_hf_search_datasets.py --query "text classification" --limit 5
```

**Parallel execution (multiple queries):**

IMPORTANT: Use full python path with GNU parallel (venv activate does NOT work in parallel subshells):
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-hf-datasets" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_hf_search_datasets.py" && \
parallel -j 10 -k --group --will-cite '$PY $S --query {} --limit 3' ::: 'sentiment' 'classification' 'translation'
```

**Example output:**
```
Found 5 dataset(s) for query='text classification'

============================================================
Dataset 1: stanfordnlp/imdb
Downloads: 2,500,000 | Likes: 1,234
Description: Large Movie Review Dataset for binary sentiment classification...
Tags: text-classification, en, sentiment-analysis
```

**Result fields per dataset:**

Each entry in ``results`` carries:

- ``id`` / ``downloads`` / ``likes`` / ``tags`` / ``description`` — standard
  HF metadata
- ``has_loader_script`` (bool) — repo ships a top-level ``<repo>.py`` loader.
  ``datasets>=3`` won't run these directly; the dataset is reachable only
  via the Datasets Server's pre-converted parquet shards. Treat as a yellow
  flag.
- ``loadable`` (bool) — **prefer datasets where this is ``True``.** Means
  the dataset is reachable via *some* path: either native parquet (no
  script) or HF auto-converted the script's output to parquet. When
  ``False``, the script needs deps HF can't install (e.g. ``conllu``,
  custom audio decoders) and ``aii_hf_datasets__download_datasets`` will
  fail — pick a different candidate.

**Parameters:**

`--query` (optional)
- Search query string
- Example: `--query "sentiment analysis"`

`--limit` (optional)
- Maximum number of results (default: 5)

`--tags` (optional)
- Filter by tags (comma-separated)
- Format: `category:value`
- Examples: `language:en`, `task_categories:text-classification`

`--sort` (optional)
- Sort by field: `downloads`, `likes` (default: downloads)

**Tips:**
- Search displays full dataset metadata
- Use tags to filter: `--tags "language:en,task_categories:translation"`

---

### Preview HuggingFace Dataset (aii_hf_preview_datasets.py)

Inspect a specific dataset - shows metadata AND sample rows.

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-hf-datasets" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_hf_preview_datasets.py openai/gsm8k --num-rows 5
```

**Parallel execution (multiple datasets):**

IMPORTANT: Use full python path with GNU parallel:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-hf-datasets" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_hf_preview_datasets.py" && \
parallel -j 10 -k --group --will-cite '$PY $S {} --num-rows 3' ::: 'openai/gsm8k' 'imdb' 'squad'
```

**Example output:**
```
============================================================
Dataset: openai/gsm8k
============================================================
Downloads: 425,109 | Likes: 1,102

Description: GSM8K (Grade School Math 8K) is a dataset of 8.5K high quality
linguistically diverse grade school math word problems...

Configs: main, socratic

--- Sample Rows (train) ---
Columns: question, answer

Row 1:
  question: Natalia sold clips to 48 of her friends in April...
  answer: Natalia sold 48/2 = <<48/2=24>>24 clips in May...
```

**Parameters:**

`dataset_id` (required, positional)
- HuggingFace dataset ID
- Examples: `openai/gsm8k`, `glue`, `imdb`

`--config` (optional)
- Dataset configuration/subset name
- Auto-detects first config if not specified

`--split` (optional)
- Split to preview (default: `train`)

`--num-rows` (optional)
- Number of sample rows (default: 5, max: 20)

**Tips:**
- Use after search to verify data structure
- Streaming mode - doesn't download full dataset

---

### Download HuggingFace Dataset (aii_hf_download_datasets.py)

Download datasets and save to files.

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-hf-datasets" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_hf_download_datasets.py openai/gsm8k --config main --split train
```

**Parallel execution (multiple datasets):**

IMPORTANT: Use full python path with GNU parallel. Use `eval {}` pattern when datasets need different flags (e.g. `--config`):
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-hf-datasets" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_hf_download_datasets.py" && \
parallel -j 10 -k --group --will-cite 'eval {}' ::: '$PY $S openai/gsm8k --config main --split train' '$PY $S imdb --split train' '$PY $S squad --split train'
```

**Example output:**
```
Downloaded: openai/gsm8k

  train:
    Rows: 7,473
    Preview: temp/datasets/preview_openai_gsm8k_main_train.json
    Mini: temp/datasets/mini_openai_gsm8k_main_train.json
    Full: temp/datasets/full_openai_gsm8k_main_train.json
```

**Parameters:**

`dataset_id` (required, positional)
- HuggingFace dataset ID
- Examples: `openai/gsm8k`, `imdb`

`--config` (optional)
- Dataset configuration/subset name
- Use preview to see available configs

`--split` (optional)
- Specific split to load (e.g., `train`, `test`)
- If not specified, loads all splits

`--output-dir` (optional)
- Output directory (default: `temp/datasets/`)

**Output files (auto-saved):**
1. **Preview**: `preview_{dataset}_{split}.json` - 3 truncated rows - **READ THIS** for quick inspection
2. **Mini**: `mini_{dataset}_{split}.json` - 3 full rows - for development/testing
3. **Full**: `full_{dataset}_{split}.json` - All rows - **DO NOT READ directly** - use as input path for code

**Tips:**
- Only read preview file directly with Read tool
- Mini and full are input paths for processing code

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [4] SKILL-INPUT — aii-json · 2026-06-17 14:06:08 UTC

The agent loaded the **aii-json** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-json
description: JSON validation and formatting toolkit. Validate JSON files against schemas for experiment pipelines, and generate full/mini/preview versions of JSON datasets. Use for validating pipeline outputs, checking schema compliance, or creating size-optimized JSON variants.
---

## Contents

- Validating JSON (schema validation against experiment schemas)
- Formatting JSON (generate full/mini/preview versions)

**IMPORTANT - Parallel execution:** GNU `parallel` subshells do NOT inherit `source activate`. Use `export` for variables and **single-quoted** command templates so parallel's subshells can resolve them:
```
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

---

## Validating JSON

Validate JSON files against predefined schemas for experiment-based hypothesis selection, data collection, solution generation, and evaluation.

### Quick Start

1. Read the schema spec you need to adhere to (e.g., `schemas/exp_eval_sol_out.json`)
2. Create your output file following that schema structure
3. Validate:

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /path/to/eval_out.json
```

### Script: aii_json_validate_schema.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /tmp/eval_out.json
```

**Parallel execution (multiple validations):**

IMPORTANT: When validating multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_validate_schema.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --format {1} --file {2}' ::: 'exp_sel_data_out' 'exp_gen_sol_out' 'exp_eval_sol_out' :::+ '/tmp/full_data_out.json' '/tmp/method_out.json' '/tmp/eval_out.json'
```

**Example output (success):**
```
Validating: aii_json_validate_schema.py
Format: exp_eval_sol_out

✓ Validation PASSED
```

**Example output (failure):**
```
Validating: aii_json_validate_schema.py
Format: exp_sel_data_out

✗ Validation FAILED

Errors:
  Path: datasets → 0 → examples → 0
  Error: 'output' is a required property
  Validator: required
```

**Parameters:**

`--format` (required)
- Format type to validate against
- Determines which schema to use

`--file` (required)
- Path to JSON file to validate
- Must be valid JSON
- **Always pass an absolute path.** Relative paths resolve from the
  ability server's CWD (typically ``/ai-inventor/aii_server``), not from
  your agent workspace, so ``data_out/x.json`` will silently look in the
  wrong directory and fail with "Could not load JSON file". The validate
  endpoint also accepts a ``workspace_dir`` arg if you need to keep a
  relative path — pass your workspace path there.

**Tips:**
- Fix errors in your JSON and rerun validation until it passes

### Schema Files

Schemas are stored in `.claude/skills/aii-json/schemas/`:

**Hypothesis Selection & Evaluation:**
- `sel_hypo_out.json` - Hypothesis Selection output (all hypotheses with selected flags)
- `feasibility_eval_all.json` - All hypotheses with feasibility scores
- `feasibility_eval_top.json` - Top 5 most feasible hypotheses
- `novelty_research_one.json` - Single hypothesis novelty research arguments with citations
- `novelty_eval_all.json` - All hypotheses with novelty scores
- `novelty_eval_top.json` - Single best selected hypothesis

**Experiment Pipeline:**
- `exp_sel_data_out.json` - Experiment Data Selection format
- `exp_gen_sol_out.json` - Experiment Solution Generation format
- `exp_eval_sol_out.json` - Experiment Solution Evaluation format

---

## Formatting JSON

Generate three size-optimized versions of a JSON file for efficient development and preview:
- **full**: Identical to original (all data)
- **mini**: First 3 items only (for quick testing)
- **preview**: Mini + all strings truncated to 200 chars (for quick inspection)

### Quick Start

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

### Script: aii_json_format_mini_preview.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

**Parallel execution (multiple files):**

IMPORTANT: When formatting multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_format_mini_preview.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --input {}' ::: 'full_data_out.json' 'method_out.json' 'eval_out.json'
```

**Example output:**
```
Generated 3 versions:
  Full (50 items): /path/to/full_method_out.json
  Mini (3 items): /path/to/mini_method_out.json
  Preview (3 items, truncated): /path/to/preview_method_out.json
```

**Parameters:**

`--input` (required)
- Path to input JSON file
- Must have a top-level array
- Example: `method_out.json`, `full_data_out.json`

`--output-dir` (optional)
- Output directory for generated files
- Default: same directory as input file
- Files are prefixed with `full_`, `mini_`, `preview_`

**Output Files:**

All three files use the same base name with different prefixes:
- `full_{basename}.json` - Complete dataset (identical to original)
- `mini_{basename}.json` - First 3 array items only
- `preview_{basename}.json` - First 3 items with strings truncated to 200 chars

**Tips:**
- Input JSON must have a top-level array structure
- String truncation is recursive (applies to nested objects and arrays)
- Use preview files for quick inspection without reading large datasets
- Use mini files for developing/testing code before running on full dataset

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [5] SKILL-INPUT — aii-web-tools · 2026-06-17 14:13:08 UTC

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

### [6] SYSTEM-USER prompt · 2026-06-17 14:26:08 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_4`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_4/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_4/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_4/results/out.json`
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
id: gen_plan_dataset_4_idx6
type: dataset
title: >-
  Supporting concept families + boundary-null dataset (CAD-IMDB sentiment, CEBaB food+service aspect, bias_in_bios) standardized
  to the CCRG shared minimal-pair schema
summary: >-
  Acquire and standardize THREE real, human-annotated HuggingFace/GitHub datasets into the CCRG two-track-grouping pipeline's
  shared JSON schema: (1) Kaushik 2020 CAD-IMDB human counterfactually-edited positive<->negative review pairs as a SUPPORTING
  sentiment family; (2) CEBaB human FOOD+SERVICE aspect edits as a SUPPORTING restaurant aspect-sentiment family (food+service
  nested as ONE family, with all four aspect-level majorities retained as INDEPENDENT sub-context labels); (3) LabHC/bias_in_bios
  profession-labeled biographies (gender as the independent sub-attribute) as the pre-registered BOUNDARY-NULL where habitat~=label.
  Each is reformatted to one-row-per-text with content-flip minimal pairs reconstructable via pair_id, concept labels, independent
  sub-context labels, content/surface pair flags, and train/dev/test folds. Schema-validate; emit full/mini/preview per family;
  keep families cleanly separated in metadata so downstream per-family bootstrap CIs (primary) compute cleanly and cross-family
  aggregates stay descriptive. No LLM calls needed (all human-annotated) -> $0 OpenRouter spend.
runpod_compute_profile: cpu_heavy
ideal_dataset_criteria: |-
  THREE REAL, downloadable, human-annotated datasets (no synthesis), each <=300MB, standardized to ONE shared JSON schema so iteration-2+ can run Tier-1b supporting families and the boundary-null through the identical CCRG pipeline.

  FAMILY 1 - SENTIMENT (supporting): Human counterfactually-EDITED minimal pairs flipping sentiment positive<->negative, with the ORIGINAL<->REVISED mapping PRESERVED so each pair is a clean content-flip (x_off, x_on) where only sentiment-bearing content changed and surface/topic is held as constant as the human editor allowed. Ideal = Kaushik/Hovy/Lipton ICLR-2020 CAD-IMDB (Amazon Mechanical Turk minimal revisions). Native train/dev/test folds. Tiny (few MB).

  FAMILY 2 - RESTAURANT ASPECT-SENTIMENT (supporting, food+service nested as ONE family): Human aspect edits that flip a SINGLE aspect's sentiment (food, service) while holding other aspects fixed, with per-aspect majority labels retained as INDEPENDENT sub-context labels (food/service/ambiance/noise). Ideal = CEBaB (Abraham et al. NeurIPS 2022). These independent aspect labels are exactly what the hypothesis's degenerate-construction guard needs (sub-contexts defined BEFORE any unit is formed). ~18.6k texts.

  FAMILY 3 - BOUNDARY-NULL (bias_in_bios): Profession-labeled biographies where the 'habitat' approximately equals the class label, so co-response grouping is PREDICTED to give no advantage (a publishable expected null, NOT method failure). Needs profession label (concept) + an independent sub-attribute (gender) usable as a sub-context. Ideal = LabHC/bias_in_bios (266MB full; subsample to keep output JSON manageable).

  SHARED-SCHEMA REQUIREMENTS for all three: one row per TEXT with {id, input(text), output(canonical concept label), family, dataset_source, concept, concept_label, sub_context(dict of independent labels), pair_id(links minimal-pair members; null if unpaired), pair_role(content_off|content_on|null), partner_id, flip_type(content|null), is_content_pair(bool), is_surface_pair(bool=false for all three), fold(train|dev|test), meta(source-specific raw fields)}. Families MUST be separable by the 'family' field. Surface-flip pairs are NOT natively available in any of these three and must NOT be fabricated here (out of scope; the schema reserves the surface fields for sibling LLM-generated/ParaDetox artifacts). Every text and its counterfactual share a pair_id so downstream can encode (x_off, x_on) deltas. License/provenance recorded per family.
dataset_search_plan: |-
  Use the aii-hf-datasets skill for HF pulls and plain HTTPS/requests for GitHub raw TSVs. Use aii-json to author the shared JSON Schema and to emit full/mini/preview + validate. NO LLM/OpenRouter calls are required (all three are human-annotated) -> $0 spend. Work family-by-family; write all three into ONE data_out.json with a 'family' discriminator (plus per-family full/mini/preview if the file-size limit requires splitting).

  === STEP 0: DEFINE THE SHARED JSON SCHEMA (write schema.json first) ===
  Author a JSON Schema for a row object with these fields (one row per TEXT):
  - id: string, globally unique, family-prefixed (e.g. 'sent_0001', 'cebab_food_0001', 'bib_0001').
  - input: string, the raw text (movie review / restaurant review / biography). REQUIRED non-empty.
  - output: string, the canonical concept label that a classifier predicts for this text ('positive'/'negative' for sentiment & aspect; profession-string for bios).
  - family: enum ['sentiment','restaurant_aspect','bias_in_bios_boundary'].
  - dataset_source: string provenance ('CAD-IMDB (Kaushik et al. ICLR 2020)','CEBaB (Abraham et al. NeurIPS 2022)','LabHC/bias_in_bios').
  - concept: string concept name ('sentiment' | 'food_sentiment' | 'service_sentiment' | 'profession').
  - concept_label: string (== output; kept explicit for downstream).
  - sub_context: object/dict of INDEPENDENT sub-context labels fixed BEFORE any grouping (see per-family). {} allowed.
  - pair_id: string|null linking the two members of a content-flip minimal pair (null for unpaired bios rows).
  - pair_role: enum ['content_off','content_on',null] (concept-absent vs concept-present member).
  - partner_id: string|null (the id of the other pair member; null if unpaired).
  - flip_type: enum ['content',null] (this row participates in a content flip; surface reserved/unused here).
  - is_content_pair: bool.
  - is_surface_pair: bool (FALSE for all rows in this artifact).
  - fold: enum ['train','dev','test'] (this is metadata_fold).
  - meta: object for source-specific raw fields (original raw labels, edit_goal/edit_type, char_len, token_overlap_with_partner, gender, raw profession id, etc.).
  Validate every emitted row against this schema with aii-json before finishing.

  === STEP 1: FAMILY 1 - CAD-IMDB SENTIMENT (content-flip pairs) ===
  SOURCE (primary): GitHub acmi-lab/counterfactually-augmented-data (Apache-2.0). Raw-file URLs:
    https://raw.githubusercontent.com/acmi-lab/counterfactually-augmented-data/master/sentiment/orig/{train,dev,test}.tsv
    https://raw.githubusercontent.com/acmi-lab/counterfactually-augmented-data/master/sentiment/new/{train,dev,test}.tsv
  TSV columns: 'Sentiment' in {Positive,Negative} and 'Text'. Expected rows ~1707 train / 245 dev / 488 test in EACH of orig and new (one human revision per original). Total ~4880 texts, a few MB. If raw URLs 404, fall back to: (a) git-clone the repo, or (b) search HF Hub for a mirror (e.g. query 'counterfactually augmented IMDB', candidate names like 'sentiment counterfactual'); verify any mirror has the orig<->revised mapping before use.
  PROCESSING per split s in {train(->fold train), dev(->fold dev), test(->fold test)}:
    1. Read orig/s.tsv and new/s.tsv.
    2. PAIRING (preserve original<->edited mapping = the core requirement). Primary assumption: the i-th row of new/s.tsv is the counterfactual revision of the i-th row of orig/s.tsv (row-index alignment within a split is the repo convention). MANDATORY VERIFICATION before trusting it: (i) row counts match between orig and new; (ii) per aligned pair the Sentiment is FLIPPED (orig.Sentiment != new.Sentiment); (iii) per aligned pair the texts are MINIMAL edits of each other -- compute normalized token Jaccard / character-level overlap and confirm the median aligned-pair overlap is FAR above a random-pair baseline (shuffle new within split and recompute). If (i)-(iii) all hold, accept row alignment. IF verification FAILS, fall back to bipartite matching: within each split, for each original review greedily match the opposite-label revised review with maximal token overlap (Levenshtein/Jaccard), enforce one-to-one, and drop any unmatched. Record the chosen pairing method in meta.
    3. For each accepted pair (o, r) create pair_id = 'sent_'+s+'_'+i. Emit TWO rows:
       - original o: input=o.Text, output=lower(o.Sentiment) ('positive'/'negative'), concept='sentiment', concept_label=output, pair_role = 'content_on' if o is Positive else 'content_off', partner_id = r.id, sub_context={}, flip_type='content', is_content_pair=true, is_surface_pair=false, fold=mapped, meta={raw_sentiment, role_source:'original', char_len, token_overlap_with_partner}.
       - revised r: symmetric, pair_role = the opposite of o, partner_id=o.id. (Define pair_role by the row's OWN sentiment value: Positive->content_on, Negative->content_off. This makes 'content_on' = positive-sentiment-present, consistent across the family.)
  NOTE: 'positive sentiment' is the designated concept; content_off = the negative member. Keep BOTH members so downstream can form (x_off,x_on) deltas either direction.

  === STEP 2: FAMILY 2 - CEBaB FOOD+SERVICE ASPECT (content-flip pairs + independent aspect sub-contexts) ===
  SOURCE (primary): HF dataset 'CEBaB/CEBaB' (parquet; ~18.6k rows). Load via aii-hf-datasets (datasets.load_dataset('CEBaB/CEBaB')) or pull parquet directly. Splits: train_exclusive, train_inclusive, train_observational, validation, test. Use train_inclusive as the TRAIN pool (it contains originals + all edits), validation->dev, test->test. (Document: train_inclusive is the superset; ignore the partially-overlapping train_exclusive/train_observational to avoid double counting, OR dedupe by id across all train_* and assign fold='train' -- prefer the simpler train_inclusive-only path and note it.)
  VERIFIED FIELDS: id, original_id, edit_id, is_original(bool), edit_goal in {food,ambiance,service,noise} (= which aspect the edit targeted), edit_type (5 values; INSPECT actual values and record), description(text), review_majority (sentiment string, ~5 values incl Positive/Negative/unknown/no-majority -- INSPECT), and the four aspect-majority fields food_aspect_majority/service_aspect_majority/ambiance_aspect_majority/noise_aspect_majority each in {Positive,Negative,unknown}(+possibly 'no majority'). original_id groups every edit with its base; is_original=true marks the base.
  PROCESSING:
    1. Index all rows by id; build original_id -> {original row, list of edit rows}.
    2. Build content-flip pairs ONLY for the FOOD and SERVICE aspects (food+service = the nested family; do NOT use ambiance/noise as the flipped concept, but DO retain their labels as sub-context). For each edited row e with edit_goal in {food,service} and its original o (same original_id, is_original=true):
       - Let A = edit_goal (the edited aspect). Read the binarized aspect sentiment of A on BOTH members: aspect_val(o) and aspect_val(e) from {o,e}.A_aspect_majority. KEEP the pair only if both are in {Positive,Negative} AND they DIFFER (a clean flip); DROP pairs where either side is 'unknown'/'no majority' on aspect A or where they do not differ (degenerate, no flip). Record dropped counts.
       - concept = A+'_sentiment' (e.g. 'food_sentiment'); pair_id = 'cebab_'+A+'_'+edit_id.
       - Emit TWO rows (o and e): input=description, output = 'positive' if that row's A_aspect_majority=='Positive' else 'negative', concept_label=output, pair_role = 'content_on' if positive else 'content_off', partner_id = the other member's id, flip_type='content', is_content_pair=true, is_surface_pair=false, fold from source split.
       - sub_context (INDEPENDENT labels, frozen before any unit) for BOTH rows = {edited_aspect:A, food:food_aspect_majority, service:service_aspect_majority, ambiance:ambiance_aspect_majority, noise:noise_aspect_majority, review_sentiment: binarized review_majority}. meta = {original_id, edit_id, is_original, edit_goal, edit_type, raw review_majority, restaurant metadata if present, char_len}.
    NOTE on duplication: one original may anchor several edits; emit the original once PER pair it participates in (distinct pair_id each). This duplication is small (food+service pairs are a few thousand) and keeps minimal-pair reconstruction trivial. If output size becomes a concern, instead dedupe originals and reconstruct pairs via (original_id, edit_id) -- but prefer the explicit-pair form and document the choice.
    3. Sanity: report #food pairs, #service pairs, label balance, and confirm food and service are separable via the 'concept' and sub_context.edited_aspect fields.
  FALLBACK if HF load fails: download the public JSON release from cebabing.github.io/CEBaB (linked from the project page) and map the identical fields.

  === STEP 3: FAMILY 3 - bias_in_bios BOUNDARY-NULL (unpaired labeled classification) ===
  SOURCE (primary): HF 'LabHC/bias_in_bios' (parquet, MIT, 266MB full). Fields: hard_text(string bio), profession(int 0-27), gender(int; 0=male,1=female). Splits train(257k)/dev(39.6k)/test(99.1k). 28 professions (accountant..yoga_teacher).
  PROCESSING:
    1. SUBSAMPLE to keep data_out.json manageable (full 396k bios would make the JSON > the file-size limit). Target ~21k rows total: ~15k train / ~3k dev / ~3k test. Use a FIXED seed (record it) and STRATIFY by (profession x gender) so the 28 professions and both genders stay proportionally represented; cap each stratum at min(available, target_per_stratum). Document the exact subsample procedure + seed for reproducibility, and note the full set is reproducible from the HF repo if downstream needs more.
    2. Build a profession int->string map (0:accountant,1:architect,2:attorney,3:chiropractor,4:comedian,5:composer,6:dentist,7:dietitian,8:filmmaker,9:interior_designer,10:journalist,11:model,12:nurse,13:painter,14:paralegal,15:pastor,16:personal_trainer,17:photographer,18:physician,19:poet,20:professor,21:psychologist,22:rapper,23:software_engineer,24:surgeon,25:teacher,26:yoga_teacher,27:...) -- VERIFY the exact ordering against the HF dataset's own label feature names rather than trusting this list (the dataset ships the canonical mapping in its features; use that).
    3. Emit one row per bio: input=hard_text, output=profession_string, concept='profession', concept_label=profession_string, family='bias_in_bios_boundary'. UNPAIRED: pair_id=null, pair_role=null, partner_id=null, flip_type=null, is_content_pair=false, is_surface_pair=false. sub_context={gender: 'female' if gender==1 else 'male'} (gender is the independent sub-attribute / 'habitat~=label' diagnostic axis). fold from source split. meta={raw_profession_int, raw_gender_int, char_len}.
    4. Note in family-level metadata WHY this is a boundary-null (profession habitat ~= label; expected no co-response-grouping advantage) so downstream treats a null as the pre-registered expectation, not a failure.

  === STEP 4: STANDARDIZE, VALIDATE, EMIT VARIANTS ===
    1. Concatenate all three families into data_out.json (a list of rows, OR {schema_version, families:{...}, rows:[...]}); ensure the 'family' field cleanly partitions them and ids are globally unique.
    2. Emit a family_summary block in metadata: per family report row count, #pairs (sentiment/food/service), label balance, fold sizes, sub-context value distributions, license, source URL/commit, pairing method used (CAD), subsample seed (bios).
    3. Validate EVERY row against schema.json using aii-json; fix any violations.
    4. Use aii-json to emit full / mini / preview per the skill's convention: mini ~ a few hundred rows balanced across the three families and across folds/labels (e.g. ~150-200/family preserving pairs intact -- never split a pair across the mini boundary); preview ~ 5-10 representative rows per family (include at least one full content-flip pair from sentiment and from CEBaB, and one bios row).
    5. Run aii-file-size-limit: if data_out.json exceeds the limit, first reduce the bias_in_bios subsample (it dominates size), then if still large split into per-family files (data_out_sentiment.json / data_out_cebab.json / data_out_bias_in_bios.json) each with its own full/mini/preview, and record the split in metadata.

  === STEP 5: FAILURE HANDLING / REPORT ===
  Report honestly in metadata: CAD pairing method chosen + verification stats (median aligned-pair overlap vs random baseline); CEBaB dropped-pair counts (unknown/no-flip) and final food/service pair counts; bias_in_bios subsample seed + per-stratum caps. If any single source is wholly unavailable (rare), proceed with the other two and clearly mark the missing family as NOT DELIVERED with the reason (do NOT substitute synthetic data or an unrelated dataset). Do NOT fabricate surface-flip pairs for any family (out of scope). Do NOT compute any derived statistics (MI/correlations/probes) -- raw standardized data only.
target_num_datasets: 3
</artifact_plan>



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

<available_data_sources>
Use the sources appropriate to your task. Read the relevant skill file BEFORE using each source.

- **HuggingFace Hub** (HF) — ML datasets (NLP, vision, tabular, benchmarks)
- **Our World in Data** (OWID) — Global statistics (energy, health, economics, environment, demographics)
- **Alternate methods** — Python/shell (sklearn.datasets, openml, direct URL, APIs, etc.)

If the plan specifies a source or one fits better, use it.
You may combine sources. Use web search (aii-web-tools skill) to research candidates (background, papers, provenance) — NOT to find/download datasets.
</available_data_sources>

<available_domain_handbooks>
If your domain has a handbook, read the relevant skill file BEFORE working on that domain.

- **Multi-LLM Agents** — dataset selection, evaluation metrics, agent orchestration patterns
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. For the top 6 datasets, create data.py (uv inline script) that: loads from temp/datasets/, standardizes to exp_sel_data_out.json schema (aii-json skill), extracts all examples per dataset, handles domain requirements, saves to full_data_out.json.

Each data ROW must be a separate example — do NOT create one example per dataset or per fold. Each data point (row, sample, instance) = one example. 500 rows → 500 examples. The output is GROUPED BY DATASET:
```json
{
  "datasets": [
    {
      "dataset": "iris",
      "examples": [
        {"input": "...", "output": "...", "metadata_fold": 2, "metadata_feature_names": [...]},
        ...
      ]
    },
    {
      "dataset": "adult_census",
      "examples": [...]
    }
  ]
}
```
Per-example required fields:
- `input`: input features/text (tabular: JSON string of feature values)
- `output`: target/label (as string)
Per-example optional metadata via `metadata_<name>` fields (flat, not nested object):
- `metadata_fold`: fold assignment (int), `metadata_feature_names`: feature name list, `metadata_task_type`: "classification"/"regression", `metadata_n_classes`: number of classes, `metadata_row_index`: original row index, etc.
Do NOT use `split`, `dataset`, or `context` as per-example fields. Dataset name goes at the group level, metadata goes in `metadata_*` fields.
TODO 2. Run 'uv run data.py' and fix errors. Validate full_data_out.json against exp_sel_data_out.json schema (aii-json skill) — fix errors. Generate preview, mini, full versions with aii-json skill's format script.
TODO 3. Read preview to inspect examples. Choose THE BEST 3 DATASETS based on domain requirements and artifact objective. Be very attentive to meticulously and exhaustively fix any errors in your code.
</todos>
````

### [7] SYSTEM-USER prompt · 2026-06-17 14:28:10 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_4`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_4/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_4/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_4/results/out.json`
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
id: gen_plan_dataset_4_idx6
type: dataset
title: >-
  Supporting concept families + boundary-null dataset (CAD-IMDB sentiment, CEBaB food+service aspect, bias_in_bios) standardized
  to the CCRG shared minimal-pair schema
summary: >-
  Acquire and standardize THREE real, human-annotated HuggingFace/GitHub datasets into the CCRG two-track-grouping pipeline's
  shared JSON schema: (1) Kaushik 2020 CAD-IMDB human counterfactually-edited positive<->negative review pairs as a SUPPORTING
  sentiment family; (2) CEBaB human FOOD+SERVICE aspect edits as a SUPPORTING restaurant aspect-sentiment family (food+service
  nested as ONE family, with all four aspect-level majorities retained as INDEPENDENT sub-context labels); (3) LabHC/bias_in_bios
  profession-labeled biographies (gender as the independent sub-attribute) as the pre-registered BOUNDARY-NULL where habitat~=label.
  Each is reformatted to one-row-per-text with content-flip minimal pairs reconstructable via pair_id, concept labels, independent
  sub-context labels, content/surface pair flags, and train/dev/test folds. Schema-validate; emit full/mini/preview per family;
  keep families cleanly separated in metadata so downstream per-family bootstrap CIs (primary) compute cleanly and cross-family
  aggregates stay descriptive. No LLM calls needed (all human-annotated) -> $0 OpenRouter spend.
runpod_compute_profile: cpu_heavy
ideal_dataset_criteria: |-
  THREE REAL, downloadable, human-annotated datasets (no synthesis), each <=300MB, standardized to ONE shared JSON schema so iteration-2+ can run Tier-1b supporting families and the boundary-null through the identical CCRG pipeline.

  FAMILY 1 - SENTIMENT (supporting): Human counterfactually-EDITED minimal pairs flipping sentiment positive<->negative, with the ORIGINAL<->REVISED mapping PRESERVED so each pair is a clean content-flip (x_off, x_on) where only sentiment-bearing content changed and surface/topic is held as constant as the human editor allowed. Ideal = Kaushik/Hovy/Lipton ICLR-2020 CAD-IMDB (Amazon Mechanical Turk minimal revisions). Native train/dev/test folds. Tiny (few MB).

  FAMILY 2 - RESTAURANT ASPECT-SENTIMENT (supporting, food+service nested as ONE family): Human aspect edits that flip a SINGLE aspect's sentiment (food, service) while holding other aspects fixed, with per-aspect majority labels retained as INDEPENDENT sub-context labels (food/service/ambiance/noise). Ideal = CEBaB (Abraham et al. NeurIPS 2022). These independent aspect labels are exactly what the hypothesis's degenerate-construction guard needs (sub-contexts defined BEFORE any unit is formed). ~18.6k texts.

  FAMILY 3 - BOUNDARY-NULL (bias_in_bios): Profession-labeled biographies where the 'habitat' approximately equals the class label, so co-response grouping is PREDICTED to give no advantage (a publishable expected null, NOT method failure). Needs profession label (concept) + an independent sub-attribute (gender) usable as a sub-context. Ideal = LabHC/bias_in_bios (266MB full; subsample to keep output JSON manageable).

  SHARED-SCHEMA REQUIREMENTS for all three: one row per TEXT with {id, input(text), output(canonical concept label), family, dataset_source, concept, concept_label, sub_context(dict of independent labels), pair_id(links minimal-pair members; null if unpaired), pair_role(content_off|content_on|null), partner_id, flip_type(content|null), is_content_pair(bool), is_surface_pair(bool=false for all three), fold(train|dev|test), meta(source-specific raw fields)}. Families MUST be separable by the 'family' field. Surface-flip pairs are NOT natively available in any of these three and must NOT be fabricated here (out of scope; the schema reserves the surface fields for sibling LLM-generated/ParaDetox artifacts). Every text and its counterfactual share a pair_id so downstream can encode (x_off, x_on) deltas. License/provenance recorded per family.
dataset_search_plan: |-
  Use the aii-hf-datasets skill for HF pulls and plain HTTPS/requests for GitHub raw TSVs. Use aii-json to author the shared JSON Schema and to emit full/mini/preview + validate. NO LLM/OpenRouter calls are required (all three are human-annotated) -> $0 spend. Work family-by-family; write all three into ONE data_out.json with a 'family' discriminator (plus per-family full/mini/preview if the file-size limit requires splitting).

  === STEP 0: DEFINE THE SHARED JSON SCHEMA (write schema.json first) ===
  Author a JSON Schema for a row object with these fields (one row per TEXT):
  - id: string, globally unique, family-prefixed (e.g. 'sent_0001', 'cebab_food_0001', 'bib_0001').
  - input: string, the raw text (movie review / restaurant review / biography). REQUIRED non-empty.
  - output: string, the canonical concept label that a classifier predicts for this text ('positive'/'negative' for sentiment & aspect; profession-string for bios).
  - family: enum ['sentiment','restaurant_aspect','bias_in_bios_boundary'].
  - dataset_source: string provenance ('CAD-IMDB (Kaushik et al. ICLR 2020)','CEBaB (Abraham et al. NeurIPS 2022)','LabHC/bias_in_bios').
  - concept: string concept name ('sentiment' | 'food_sentiment' | 'service_sentiment' | 'profession').
  - concept_label: string (== output; kept explicit for downstream).
  - sub_context: object/dict of INDEPENDENT sub-context labels fixed BEFORE any grouping (see per-family). {} allowed.
  - pair_id: string|null linking the two members of a content-flip minimal pair (null for unpaired bios rows).
  - pair_role: enum ['content_off','content_on',null] (concept-absent vs concept-present member).
  - partner_id: string|null (the id of the other pair member; null if unpaired).
  - flip_type: enum ['content',null] (this row participates in a content flip; surface reserved/unused here).
  - is_content_pair: bool.
  - is_surface_pair: bool (FALSE for all rows in this artifact).
  - fold: enum ['train','dev','test'] (this is metadata_fold).
  - meta: object for source-specific raw fields (original raw labels, edit_goal/edit_type, char_len, token_overlap_with_partner, gender, raw profession id, etc.).
  Validate every emitted row against this schema with aii-json before finishing.

  === STEP 1: FAMILY 1 - CAD-IMDB SENTIMENT (content-flip pairs) ===
  SOURCE (primary): GitHub acmi-lab/counterfactually-augmented-data (Apache-2.0). Raw-file URLs:
    https://raw.githubusercontent.com/acmi-lab/counterfactually-augmented-data/master/sentiment/orig/{train,dev,test}.tsv
    https://raw.githubusercontent.com/acmi-lab/counterfactually-augmented-data/master/sentiment/new/{train,dev,test}.tsv
  TSV columns: 'Sentiment' in {Positive,Negative} and 'Text'. Expected rows ~1707 train / 245 dev / 488 test in EACH of orig and new (one human revision per original). Total ~4880 texts, a few MB. If raw URLs 404, fall back to: (a) git-clone the repo, or (b) search HF Hub for a mirror (e.g. query 'counterfactually augmented IMDB', candidate names like 'sentiment counterfactual'); verify any mirror has the orig<->revised mapping before use.
  PROCESSING per split s in {train(->fold train), dev(->fold dev), test(->fold test)}:
    1. Read orig/s.tsv and new/s.tsv.
    2. PAIRING (preserve original<->edited mapping = the core requirement). Primary assumption: the i-th row of new/s.tsv is the counterfactual revision of the i-th row of orig/s.tsv (row-index alignment within a split is the repo convention). MANDATORY VERIFICATION before trusting it: (i) row counts match between orig and new; (ii) per aligned pair the Sentiment is FLIPPED (orig.Sentiment != new.Sentiment); (iii) per aligned pair the texts are MINIMAL edits of each other -- compute normalized token Jaccard / character-level overlap and confirm the median aligned-pair overlap is FAR above a random-pair baseline (shuffle new within split and recompute). If (i)-(iii) all hold, accept row alignment. IF verification FAILS, fall back to bipartite matching: within each split, for each original review greedily match the opposite-label revised review with maximal token overlap (Levenshtein/Jaccard), enforce one-to-one, and drop any unmatched. Record the chosen pairing method in meta.
    3. For each accepted pair (o, r) create pair_id = 'sent_'+s+'_'+i. Emit TWO rows:
       - original o: input=o.Text, output=lower(o.Sentiment) ('positive'/'negative'), concept='sentiment', concept_label=output, pair_role = 'content_on' if o is Positive else 'content_off', partner_id = r.id, sub_context={}, flip_type='content', is_content_pair=true, is_surface_pair=false, fold=mapped, meta={raw_sentiment, role_source:'original', char_len, token_overlap_with_partner}.
       - revised r: symmetric, pair_role = the opposite of o, partner_id=o.id. (Define pair_role by the row's OWN sentiment value: Positive->content_on, Negative->content_off. This makes 'content_on' = positive-sentiment-present, consistent across the family.)
  NOTE: 'positive sentiment' is the designated concept; content_off = the negative member. Keep BOTH members so downstream can form (x_off,x_on) deltas either direction.

  === STEP 2: FAMILY 2 - CEBaB FOOD+SERVICE ASPECT (content-flip pairs + independent aspect sub-contexts) ===
  SOURCE (primary): HF dataset 'CEBaB/CEBaB' (parquet; ~18.6k rows). Load via aii-hf-datasets (datasets.load_dataset('CEBaB/CEBaB')) or pull parquet directly. Splits: train_exclusive, train_inclusive, train_observational, validation, test. Use train_inclusive as the TRAIN pool (it contains originals + all edits), validation->dev, test->test. (Document: train_inclusive is the superset; ignore the partially-overlapping train_exclusive/train_observational to avoid double counting, OR dedupe by id across all train_* and assign fold='train' -- prefer the simpler train_inclusive-only path and note it.)
  VERIFIED FIELDS: id, original_id, edit_id, is_original(bool), edit_goal in {food,ambiance,service,noise} (= which aspect the edit targeted), edit_type (5 values; INSPECT actual values and record), description(text), review_majority (sentiment string, ~5 values incl Positive/Negative/unknown/no-majority -- INSPECT), and the four aspect-majority fields food_aspect_majority/service_aspect_majority/ambiance_aspect_majority/noise_aspect_majority each in {Positive,Negative,unknown}(+possibly 'no majority'). original_id groups every edit with its base; is_original=true marks the base.
  PROCESSING:
    1. Index all rows by id; build original_id -> {original row, list of edit rows}.
    2. Build content-flip pairs ONLY for the FOOD and SERVICE aspects (food+service = the nested family; do NOT use ambiance/noise as the flipped concept, but DO retain their labels as sub-context). For each edited row e with edit_goal in {food,service} and its original o (same original_id, is_original=true):
       - Let A = edit_goal (the edited aspect). Read the binarized aspect sentiment of A on BOTH members: aspect_val(o) and aspect_val(e) from {o,e}.A_aspect_majority. KEEP the pair only if both are in {Positive,Negative} AND they DIFFER (a clean flip); DROP pairs where either side is 'unknown'/'no majority' on aspect A or where they do not differ (degenerate, no flip). Record dropped counts.
       - concept = A+'_sentiment' (e.g. 'food_sentiment'); pair_id = 'cebab_'+A+'_'+edit_id.
       - Emit TWO rows (o and e): input=description, output = 'positive' if that row's A_aspect_majority=='Positive' else 'negative', concept_label=output, pair_role = 'content_on' if positive else 'content_off', partner_id = the other member's id, flip_type='content', is_content_pair=true, is_surface_pair=false, fold from source split.
       - sub_context (INDEPENDENT labels, frozen before any unit) for BOTH rows = {edited_aspect:A, food:food_aspect_majority, service:service_aspect_majority, ambiance:ambiance_aspect_majority, noise:noise_aspect_majority, review_sentiment: binarized review_majority}. meta = {original_id, edit_id, is_original, edit_goal, edit_type, raw review_majority, restaurant metadata if present, char_len}.
    NOTE on duplication: one original may anchor several edits; emit the original once PER pair it participates in (distinct pair_id each). This duplication is small (food+service pairs are a few thousand) and keeps minimal-pair reconstruction trivial. If output size becomes a concern, instead dedupe originals and reconstruct pairs via (original_id, edit_id) -- but prefer the explicit-pair form and document the choice.
    3. Sanity: report #food pairs, #service pairs, label balance, and confirm food and service are separable via the 'concept' and sub_context.edited_aspect fields.
  FALLBACK if HF load fails: download the public JSON release from cebabing.github.io/CEBaB (linked from the project page) and map the identical fields.

  === STEP 3: FAMILY 3 - bias_in_bios BOUNDARY-NULL (unpaired labeled classification) ===
  SOURCE (primary): HF 'LabHC/bias_in_bios' (parquet, MIT, 266MB full). Fields: hard_text(string bio), profession(int 0-27), gender(int; 0=male,1=female). Splits train(257k)/dev(39.6k)/test(99.1k). 28 professions (accountant..yoga_teacher).
  PROCESSING:
    1. SUBSAMPLE to keep data_out.json manageable (full 396k bios would make the JSON > the file-size limit). Target ~21k rows total: ~15k train / ~3k dev / ~3k test. Use a FIXED seed (record it) and STRATIFY by (profession x gender) so the 28 professions and both genders stay proportionally represented; cap each stratum at min(available, target_per_stratum). Document the exact subsample procedure + seed for reproducibility, and note the full set is reproducible from the HF repo if downstream needs more.
    2. Build a profession int->string map (0:accountant,1:architect,2:attorney,3:chiropractor,4:comedian,5:composer,6:dentist,7:dietitian,8:filmmaker,9:interior_designer,10:journalist,11:model,12:nurse,13:painter,14:paralegal,15:pastor,16:personal_trainer,17:photographer,18:physician,19:poet,20:professor,21:psychologist,22:rapper,23:software_engineer,24:surgeon,25:teacher,26:yoga_teacher,27:...) -- VERIFY the exact ordering against the HF dataset's own label feature names rather than trusting this list (the dataset ships the canonical mapping in its features; use that).
    3. Emit one row per bio: input=hard_text, output=profession_string, concept='profession', concept_label=profession_string, family='bias_in_bios_boundary'. UNPAIRED: pair_id=null, pair_role=null, partner_id=null, flip_type=null, is_content_pair=false, is_surface_pair=false. sub_context={gender: 'female' if gender==1 else 'male'} (gender is the independent sub-attribute / 'habitat~=label' diagnostic axis). fold from source split. meta={raw_profession_int, raw_gender_int, char_len}.
    4. Note in family-level metadata WHY this is a boundary-null (profession habitat ~= label; expected no co-response-grouping advantage) so downstream treats a null as the pre-registered expectation, not a failure.

  === STEP 4: STANDARDIZE, VALIDATE, EMIT VARIANTS ===
    1. Concatenate all three families into data_out.json (a list of rows, OR {schema_version, families:{...}, rows:[...]}); ensure the 'family' field cleanly partitions them and ids are globally unique.
    2. Emit a family_summary block in metadata: per family report row count, #pairs (sentiment/food/service), label balance, fold sizes, sub-context value distributions, license, source URL/commit, pairing method used (CAD), subsample seed (bios).
    3. Validate EVERY row against schema.json using aii-json; fix any violations.
    4. Use aii-json to emit full / mini / preview per the skill's convention: mini ~ a few hundred rows balanced across the three families and across folds/labels (e.g. ~150-200/family preserving pairs intact -- never split a pair across the mini boundary); preview ~ 5-10 representative rows per family (include at least one full content-flip pair from sentiment and from CEBaB, and one bios row).
    5. Run aii-file-size-limit: if data_out.json exceeds the limit, first reduce the bias_in_bios subsample (it dominates size), then if still large split into per-family files (data_out_sentiment.json / data_out_cebab.json / data_out_bias_in_bios.json) each with its own full/mini/preview, and record the split in metadata.

  === STEP 5: FAILURE HANDLING / REPORT ===
  Report honestly in metadata: CAD pairing method chosen + verification stats (median aligned-pair overlap vs random baseline); CEBaB dropped-pair counts (unknown/no-flip) and final food/service pair counts; bias_in_bios subsample seed + per-stratum caps. If any single source is wholly unavailable (rare), proceed with the other two and clearly mark the missing family as NOT DELIVERED with the reason (do NOT substitute synthetic data or an unrelated dataset). Do NOT fabricate surface-flip pairs for any family (out of scope). Do NOT compute any derived statistics (MI/correlations/probes) -- raw standardized data only.
target_num_datasets: 3
</artifact_plan>



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

<available_data_sources>
Use the sources appropriate to your task. Read the relevant skill file BEFORE using each source.

- **HuggingFace Hub** (HF) — ML datasets (NLP, vision, tabular, benchmarks)
- **Our World in Data** (OWID) — Global statistics (energy, health, economics, environment, demographics)
- **Alternate methods** — Python/shell (sklearn.datasets, openml, direct URL, APIs, etc.)

If the plan specifies a source or one fits better, use it.
You may combine sources. Use web search (aii-web-tools skill) to research candidates (background, papers, provenance) — NOT to find/download datasets.
</available_data_sources>

<available_domain_handbooks>
If your domain has a handbook, read the relevant skill file BEFORE working on that domain.

- **Multi-LLM Agents** — dataset selection, evaluation metrics, agent orchestration patterns
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Update data.py to only include the chosen 3 datasets and generate full_data_out.json. Re-run to generate full_data_out.json. Validate output format with aii-json skill and fix any errors. Generate full, mini, and preview versions with aii-json skill's format script using `--input full_data_out.json` (creates full_full_data_out.json, mini_full_data_out.json, preview_full_data_out.json — rename to full_data_out.json, mini_data_out.json, preview_data_out.json).
TODO 2. Verify full_data_out.json, preview_data_out.json, and mini_data_out.json exist in your workspace (see <workspace>) and contain correct data.
TODO 3. Apply aii-file-size-limit skill's file size check procedure (100MB limit) to full_data_out.json.
TODO 4. Ensure a `pyproject.toml` exists in your workspace with ALL dependencies pinned to the exact versions installed in your .venv (run `.venv/bin/pip freeze` to get them). This is required for reproducibility. The [project] section must include name, version, requires-python, and a dependencies list with pinned versions (e.g. `numpy==2.0.2`, not `numpy>=2.0`).
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "DatasetExpectedFiles": {
      "description": "All expected output files from dataset artifact.",
      "properties": {
        "script": {
          "description": "Path to data.py script. Example: 'data.py'",
          "title": "Script",
          "type": "string"
        },
        "datasets": {
          "description": "Dataset file groups \u2014 one per dataset, each with full/mini/preview variants",
          "items": {
            "$ref": "#/$defs/DatasetFileSet"
          },
          "title": "Datasets",
          "type": "array"
        }
      },
      "required": [
        "script",
        "datasets"
      ],
      "title": "DatasetExpectedFiles",
      "type": "object"
    },
    "DatasetFileSet": {
      "description": "One dataset's three required output variants.",
      "properties": {
        "full": {
          "description": "Full dataset JSON file(s). Single file or split files. Example: ['full_data_out.json'] or ['full_data_out/full_data_out_1.json', 'full_data_out/full_data_out_2.json']",
          "items": {
            "type": "string"
          },
          "title": "Full",
          "type": "array"
        },
        "mini": {
          "description": "Mini dataset JSON file path (3 examples). Example: 'mini_data_out.json'",
          "title": "Mini",
          "type": "string"
        },
        "preview": {
          "description": "Preview dataset JSON file path (10 examples). Example: 'preview_data_out.json'",
          "title": "Preview",
          "type": "string"
        }
      },
      "required": [
        "full",
        "mini",
        "preview"
      ],
      "title": "DatasetFileSet",
      "type": "object"
    }
  },
  "description": "Dataset artifact \u2014 structured output + file metadata.\n\nFinds, evaluates, and prepares datasets for research experiments.\nProduces data.py and full_data_out.json files.",
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
      "$ref": "#/$defs/DatasetExpectedFiles",
      "description": "All output files you created. Must include data.py script plus dataset file groups (full/mini/preview variants)."
    },
    "upload_ignore_regexes": {
      "description": "Regex patterns for workspace paths that must NOT be published to the GitHub repo, matched against each file's path relative to this artifact's workspace root (POSIX form, e.g. 'cache/abc.json'). Applied ON TOP OF the deploy step's built-in exclusions. Use this for executor-specific caches, large transient intermediates, or content-addressed blob stores (e.g. a cache/ dir of thousands of hash-named files) that would bloat the repo. Examples: ['(^|/)cache/', '(^|/)\\\\.weight_cache/', '(^|/)checkpoints/']. Leave empty if every workspace file should be published.",
      "items": {
        "type": "string"
      },
      "title": "Upload Ignore Regexes",
      "type": "array"
    }
  },
  "required": [
    "out_expected_files"
  ],
  "title": "DatasetArtifact",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````
