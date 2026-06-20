# gen_art_dataset_1 — test_idea

> Phase: `invention_loop` · round 1 · `gen_art`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_dataset_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-17 13:48:39 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/results/out.json`
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
id: gen_plan_dataset_1_idx3
type: dataset
title: >-
  First-Letter-Spelling Absorption Testbed: Content/Surface-Flip Minimal Pairs + Frozen Pile Letter-Occurrence Corpus (L primary;
  O/T/I/D secondary)
summary: >-
  The single most load-bearing dataset for the Two-Track Co-Response Grouping hypothesis. Build, per target letter (L end-to-end
  first, then O/T/I/D), three linked components into one schema-standardized data_out.json: (A) CONTENT-FLIP minimal pairs
  ('starts-with-<letter>' present vs absent, surface-matched in a shared carrier) for the Tier-0 K-proposal pilot and the
  C3 absorber-recovery spine; (B) SURFACE-FLIP pairs (two different words SAME first letter) for the unit-level surface-invariance
  check; (C) a FROZEN natural-text corpus from monology/pile-uncopyrighted (pinned rev 3be9033) of slot-eligible alphabetic
  tokens starting with each letter, with per-token occurrence counts and real in-context windows, so iteration-2's form-free/Chanin
  (2409.14507) diagnostic can locate the false-negative ('lion'/'London') absorbers. Words are anchored in the real gemma-2-2b
  vocabulary via the exact sae-spelling get_alpha_tokens filter; pairs are mechanically constructed + LLM-judge-validated
  (OpenRouter, <$3, pass rates reported). Pure CPU/data task (no SAE, no GPU). Schema-validate; emit full/mini/preview under
  300MB.
runpod_compute_profile: cpu_heavy
ideal_dataset_criteria: |-
  PURPOSE & ROLE. This is the LOAD-BEARING absorption testbed: it feeds (1) the Tier-0 K-track PROPOSAL-step pilot (does anchored greedy set-cover, given ONLY the content-flip pairs, recover the known {general 'starts-with-L' parent + 'lion'/'London' absorbers} that the Chanin 2409.14507 diagnostic identifies?), and (2) the C3 absorber-recovery spine (the co-response unit recovers absorbers the marginal-attribution pools (g)/(h) drop, with KG edges agreeing with the form-free absorption diagnostic). It is PURE TEXT + tokenizer + LLM-judge construction; it does NOT run the SAE or read activations (that happens in iteration-2 experiments). Deliver letter L FULLY end-to-end before broadening to O/T/I/D.

  THREE COMPONENTS PER TARGET LETTER, all merged into one data_out.json:
  (A) CONTENT-FLIP PAIRS. Each pair = (x_off, x_on) embedded in an IDENTICAL carrier template, differing only in the slotted word: x_on = a word STARTING WITH the target letter (concept present); x_off = a matched word NOT starting with the letter (concept absent). 'Surface-matched' = the two slotted words are matched as closely as feasible on character length, token count (both ideally SINGLE gemma-2-2b tokens), and rough corpus frequency, so the only systematic difference is the first-letter identity. Multiple distinct carrier templates per word so cover-sets/precision can be computed across contexts. Target ~300-500 content-flip pairs for L; ~150-300 for each secondary letter (scale to the 300MB cap; mini/preview handle size).
  (B) SURFACE-FLIP PAIRS. Each pair = (x_a, x_b) in the same carrier, where BOTH slotted words start with the target letter but are DIFFERENT words/surface realizations (e.g., 'lion' vs 'lamp'; or same word in two carrier phrasings). The concept 'starts-with-L' is held CONSTANT while surface varies — used for the unit-level surface-invariance admission check (a good unit's pooled response to surface flips ~ 0). Target ~150-250 for L, ~80-150 per secondary letter.
  (C) FROZEN NATURAL-TEXT CORPUS (the diagnostic substrate). From monology/pile-uncopyrighted at PINNED revision 3be9033, provide for each target letter: (c1) a per-token OCCURRENCE-COUNT TABLE over a fixed pile sample, restricted to SLOT-ELIGIBLE word-initial alphabetic tokens whose first letter is the target; (c2) REAL in-context windows (e.g., ~32-64 token windows) sampled from the same pile docs, each containing >=1 target-letter slot-eligible token with that token's position annotated, capped per word-type to bound size. This lets iteration-2 train the parent 'starts-with-L' probe on real activations and search for false negatives (absorbed words). Cap ~30-80 contexts per word-type and a few thousand contexts per letter total.

  WORD ANCHORING — EXACT get_alpha_tokens RECIPE (verbatim from lasr-spelling/sae-spelling vocab.py; replicate it, ~10 lines). ALL_ALPHA_LETTERS = the 26 lowercase + 26 uppercase a-z. For each token in tokenizer.vocab: word = tokenizer.convert_tokens_to_string([token]); if allow_leading_space and word/token starts with ' ': strip exactly ONE leading space; keep iff len>0 AND every remaining char is in ALL_ALPHA_LETTERS. SLOT-ELIGIBILITY = the token is WORD-INITIAL (it originally carried the leading-space/'▁' marker, i.e. it represents the start of a word) AND passes the alpha filter — only word-initial tokens carry clean 'starts-with-<letter>' semantics, matching the SAE's first-letter regime (Gemma Scope L12 width_16k canonical context). The first letter = word.strip()[0].lower(). Group eligible words by first letter. Prefer SINGLE-TOKEN words for clean activation reads; record is_single_token and is_slot_eligible per word.

  TOKENIZER. Use the gemma-2-2b tokenizer. google/gemma-2-2b is GATED; use the ungated mirror unsloth/gemma-2-2b (identical vocab) OR google/gemma-2-2b with an HF_TOKEN env var. Verify vocab size == 256000 as a sanity gate. No model weights are needed — tokenizer only.

  ABSORBER CANDIDATES (metadata). For each letter, attach a candidate-absorber sublist: high-frequency single-token word-types most likely to host dedicated absorbers (e.g., L: 'lion','London','little','life','love','line' — derive empirically as the top-frequency slot-eligible words from the corpus table, union with any sae-spelling/Chanin-published examples). This is METADATA ONLY (a hint for iteration-2), never used to construct or filter the units.

  SPELLING-PROMPT CARRIERS (anchor to the documented regime). Include at least one carrier family mirroring sae-spelling prompting.py: the verbose first-letter template VERBOSE_FIRST_LETTER_TEMPLATE = '{word} has the first letter:' and/or default '{word}:', optionally with a few shuffled in-context-learning (ICL) examples (create_icl_prompt-style, newline-separated, no word contamination across examples) and answer ' <LETTER>' (space-prefixed, uppercase). ALSO include 2-4 NEUTRAL carrier sentences (e.g., 'I saw a {word} yesterday.', 'The {word} was on the table.', 'They wrote about {word} in the report.') so cover-sets span multiple natural contexts, not just the spelling prompt.

  SCHEMA (shared across the run's 4 datasets). data_out.json = {"metadata": {...dataset-level...}, "data": [ rows ]}. Each ROW: {"input": <text the SAE will encode>, "output": <concept-label string>, "metadata": {dataset:'first_letter_spelling', letter:'L', pair_id:'L_c_0001', pair_type:'content_flip'|'surface_flip'|'corpus_context', role:'on'|'off'|'var_a'|'var_b'|'occurrence', sub_context:<the specific word/token covered — THE key field>, target_word, counterpart_word, template_id, label_starts_with_target:1|0, is_single_token, is_slot_eligible, first_letter, fold; corpus rows ALSO: source_doc_id, pile_revision:'3be9033', token_position, window_char_span}}. output = the first letter (e.g. 'L') for on-rows / the off-word's actual first letter for off-rows / the token's first letter for corpus rows (supports both multi-class first-letter and binary starts-with-target framings; binary label also in metadata.label_starts_with_target). Pairs are LINKED by shared pair_id + role so iteration-2 can reconstruct (x_on,x_off) and compute r_l(p)=a_l(x_on)-a_l(x_off). DATASET-LEVEL metadata: per-letter per-token occurrence table (the big table lives HERE, not per-row), absorber-candidate sublists, LLM-judge pass-rates per (letter,pair_type), achieved counts per letter, generation config (models used, pinned pile revision, tokenizer id, get_alpha_tokens params), and total LLM $ spent.

  FOLDS. Doc-level folds for the corpus (assign each pile source doc to a fold by hashing source_doc_id → fold_0..fold_4) so probe train/test never leaks across the same document. For minimal pairs, fold by TARGET WORD (a given word-type appears in exactly one fold) to prevent word-identity leakage in any downstream probe.

  VALIDATION & SIZE. LLM-judge each pair (or a representative >=150/letter sample if total is large) for 'content correctly flipped (on starts-with-letter, off does not) AND surface preserved/grammatical'; report pass rate per letter & pair_type in metadata; DROP failed pairs. Keep total LLM spend <$3 (cheap flash/mini/haiku-tier model via OpenRouter; track cumulative cost, hard-stop at $3). Schema-validate with aii-json; emit full + mini + preview; run the aii-file-size-limit check and keep full data_out.json <=300MB (cap corpus contexts/word and pair counts on secondary letters to stay under).

  WHY THIS IS IDEAL. It is non-circular (words from public vocab + pile, never from the SAE latents being grouped), guaranteed-signal (first-letter absorption is the documented regime), provides BOTH the synthetic minimal pairs (for the pilot/co-response) AND the natural corpus (for the diagnostic), and is frozen/reproducible (pinned pile revision, pinned tokenizer, recorded config).
dataset_search_plan: |-
  STEP 0 — ENV & PINS (no GPU; cpu_heavy). Read skills: aii-hf-datasets, aii-openrouter-llms, aii-json, aii-file-size-limit, aii-python, aii-use-hardware. Confirm internet + HF access. Pin: pile dataset = monology/pile-uncopyrighted, revision='3be9033' (full SHA begins 3be90335; 'Upload to LFS', Aug 31 2023); tokenizer = unsloth/gemma-2-2b (ungated mirror; fallback google/gemma-2-2b with HF_TOKEN). Reference code = lasr-spelling/sae-spelling (vocab.py get_alpha_tokens / get_tokens; prompting.py SpellingPrompt, VERBOSE_FIRST_LETTER_TEMPLATE='{word} has the first letter:', first_letter_formatter, create_icl_prompt). If the sae_spelling pip package is unavailable, REPLICATE get_alpha_tokens inline (provided verbatim in the criteria).

  STEP 1 — BUILD THE VOCABULARY WORD LISTS. Load the gemma-2-2b tokenizer; assert vocab_size==256000. Apply get_alpha_tokens (allow_leading_space=True, replace_special_chars=True). Determine slot-eligibility: a token is slot-eligible iff it is WORD-INITIAL (raw token starts with the leading-space/'▁' marker) AND alpha. Compute first_letter = word.strip()[0].lower(). Group eligible words by first letter; flag is_single_token. Produce, per letter, the master word-type list (on-words). Build a pooled OFF-word list (slot-eligible words NOT starting with the target letter) for content-flip counterparts. NON-DEGENERACY GATE: a letter is usable only if it has enough distinct single-token slot-eligible word-types to support its target pair count (this is why L/O/T/I/D are chosen and S/X — k=1 singletons — are avoided); if a secondary letter has too few word-types, DROP it and record the reason. Prioritize L first.

  STEP 2 — FROZEN PILE CORPUS (component C). Stream monology/pile-uncopyrighted at the pinned revision (datasets.load_dataset(..., split='train', streaming=True, revision='3be9033')). FALLBACK if streaming is broken (known HF discussion #5): hf_hub_download the single shard train/00.jsonl.zst at the pinned revision, decompress with zstandard, read line-by-line. Take a FIXED, deterministic sample (e.g., first ~100k-300k documents) — record the exact count for reproducibility. For each doc: tokenize, walk tokens, and for every slot-eligible word-initial token whose first letter is a target letter: (a) increment its global occurrence count (per-letter per-token table), (b) with reservoir/capped sampling, store a ~32-64 token context window (decoded to text) + token_position + source_doc_id, capping at ~30-80 windows per word-type and a few-thousand per letter. Emit corpus_context rows; put the aggregate occurrence table in DATASET-LEVEL metadata. Derive each letter's empirical absorber-candidate sublist = the top-frequency single-token word-types (union with known examples like lion/London for L). Assign doc-level folds by hashing source_doc_id.

  STEP 3 — CONTENT-FLIP PAIRS (component A). Define 4-8 carrier templates per letter: include >=1 sae-spelling-style first-letter prompt ('{word} has the first letter:' / '{word}:', optionally with shuffled ICL examples and ' <LETTER>' answer) and 3-5 neutral sentence carriers. For each chosen on-word (prioritize single-token, frequency-spanning, including absorber candidates), pick a surface-matched off-word (closest match on char length, token count, frequency bucket; both single-token preferred). Instantiate the SAME carrier with on-word and off-word → an (x_on,x_off) pair sharing pair_id, role on/off, identical template_id, sub_context=on-word, counterpart_word=off-word. Record label_starts_with_target (1 for on, 0 for off) and the char/token span of the slotted word. Target ~300-500 pairs for L, ~150-300 per secondary; span many distinct on-words × multiple carriers.

  STEP 4 — SURFACE-FLIP PAIRS (component B). For pairs of DISTINCT on-words (both start with target letter) in the same carrier, OR the same on-word across two carrier phrasings, emit (x_a,x_b) sharing pair_id, roles var_a/var_b, pair_type='surface_flip', sub_context = the word(s) covered. The concept is held constant; only surface changes. Target ~150-250 for L, ~80-150 per secondary.

  STEP 5 — LLM-JUDGE VALIDATION (OpenRouter, <$3). Use a cheap flash/mini/haiku-tier model via aii-openrouter-llms. For each pair, ask the judge: for content_flip — does x_on contain a word starting with '<L>' in the slot, x_off a word NOT starting with '<L>', and is the carrier grammatical/surface-preserved across both? for surface_flip — do both contain DIFFERENT same-first-letter realizations while staying grammatical? Return pass/fail + reason. If total pairs are large, judge a representative sample of >=150 per letter and report the sampled pass rate; otherwise judge all. DROP failed pairs; record pass-rate per (letter,pair_type) and cumulative $ in metadata. Track cost after every batch; HARD-STOP at $3 (fall back to mechanical-only construction if budget is hit — mechanical first-letter pairs are largely self-validating).

  STEP 6 — ASSEMBLE, VALIDATE, SPLIT. Merge all rows into data_out.json with the shared schema (dataset-level metadata block + data array). Fold minimal pairs by target word; corpus by source doc. Validate against the shared run schema with aii-json (input/output strings present; required metadata keys present; pair_ids link consistently; no orphan roles). Run aii-file-size-limit; if full >300MB, reduce secondary-letter pair counts and per-word corpus-context caps first (NEVER reduce L). Emit full + mini + preview. Self-check report: counts per letter, per-pair-type, corpus contexts, occurrence-table size, judge pass-rates, total $ spent, and an explicit confirmation that L is complete end-to-end.

  FAILURE SCENARIOS & FALLBACKS. (i) Tokenizer gated → unsloth/gemma-2-2b mirror; verify vocab_size. (ii) Pile streaming broken → download single pinned shard + zstandard decode. (iii) Too few single-token word-types for a letter → supplement on-words with LLM-proposed common words RE-VERIFIED to be single gemma-2-2b tokens; if still too few, drop that secondary letter and document. (iv) LLM budget exhausted → mechanical pairs only, report which letters lack LLM-validated pass rates. (v) Size pressure → mini/preview + cap secondary letters; L stays full. (vi) A target letter is degenerate (k=1, like S/X) → exclude and record. PRIORITY ORDER if time-constrained: L (all 3 components, full) > corpus tables for O/T/I/D > content-flip pairs O/T/I/D > surface-flip pairs O/T/I/D.
target_num_datasets: 5
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
TODO 2. Read skill files for your data sources (see <available_data_sources>) and domain handbook if applicable (see <available_domain_handbooks>). Based on plan and context, decide which source(s) to use. Include everything specified in the artifact plan, but you may also collect additional relevant data beyond what's listed. Run 40 diverse searches across chosen source(s) — BROAD, GENERAL terms, not very specific. Parallelize where supported.
TODO 3. Identify the 20 most promising datasets. IMPORTANT: Only consider datasets under 300MB. Preview/inspect sample rows for each candidate. Parallelize previews.
TODO 4. Research each candidate BEFORE choosing which to download. For each, search the web (aii-web-tools skill): dataset name, papers citing it, original source/task, popularity. Red flags: no search results, no papers, anonymized features (F1, F2...), <100 downloads, no documentation. Green flags: papers using it, clear documentation, meaningful features, established benchmark. Also consider: will features/structure allow meaningful evaluation of the planned method?
TODO 5. Decide which to KEEP vs DISCARD. Look for: clear structure, relevant fields, quality examples matching requirements, confirmed provenance. Determine which 10 datasets have the most suitable data. Download and save to `temp/datasets/`. Parallelize downloads.
</todos>
```

### [2] HUMAN-USER prompt · 2026-06-17 13:48:39 UTC

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

### [3] SKILL-INPUT — aii-python · 2026-06-17 13:49:09 UTC

The agent loaded the **aii-python** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-python
description: Python coding standards for experiment and evaluation scripts. Covers environment setup, logging, error handling, and code structure.
---

## Environment Setup

- Python 3.12+
- **NEVER use `pip` or `.venv/bin/pip`** — they are not installed. Use `uv` for ALL package operations:
  ```bash
  uv venv .venv --python=3.12
  source .venv/bin/activate  # or: .venv/bin/python script.py
  uv pip install pandas loguru  # NOT: pip install
  ```
- Create `.toml` file with dependencies, create uv `.venv` and activate it
- NO inline dependencies (no `# /// script` headers)

## Logging

Use `loguru` for all logging. Add a file sink alongside stdout.

```python
from loguru import logger
import sys

logger.remove()  # Remove default handler
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")
```

Rules:
- Log every major step (data loading, processing start/end, results)
- If applicable, log every LLM API call input and output
- Truncate long outputs in logs (add truncation logic for potentially large strings)
- Use `logger.error()` in except blocks (traceback auto-captured)

## Error Handling

- Wrap major operations in try/except blocks
- Use `@logger.catch(reraise=True)` decorator on main functions — without `reraise=True`, the script exits 0 even on uncaught exceptions, hiding failures from downstream consumers
- Use explicit exception types, not bare `except:`
- Never silently swallow exceptions — always log them

```python
@logger.catch(reraise=True)
def main():
    try:
        data = load_data(path)
    except FileNotFoundError:
        logger.error("Data file not found")
        raise
    except json.JSONDecodeError:
        logger.error("Invalid JSON in data file")
        raise
```

## Code Structure

- Use `pathlib.Path` for file operations: `Path("data/input.json").read_text()` not `open(...).read()`
- Use type hints for function signatures
- Use keyword arguments for functions with more than 4 parameters
- No hardcoded paths — derive from script location or accept as arguments

## Script Pattern

Standard pattern for experiment/evaluation scripts:

```python
#!/usr/bin/env python3
"""Brief description of what this script does."""

from loguru import logger
from pathlib import Path
import json
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

@logger.catch(reraise=True)
def main():
    # Load data
    data_path = Path("full_data_out.json")
    logger.info(f"Loading data from {data_path}")
    data = json.loads(data_path.read_text())
    logger.info(f"Loaded {len(data['examples'])} examples")

    # Process
    results = []
    for i, example in enumerate(data["examples"]):
        try:
            result = process(example)
            results.append(result)
        except Exception:
            logger.error(f"Failed on example {i}")
            continue

    # Save output
    output = {"examples": results}
    Path("method_out.json").write_text(json.dumps(output, indent=2))
    logger.info(f"Saved {len(results)} results")

if __name__ == "__main__":
    main()
```
````

### [4] SKILL-INPUT — aii-hf-datasets · 2026-06-17 13:49:09 UTC

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

### [5] SKILL-INPUT — aii-use-hardware · 2026-06-17 13:49:09 UTC

The agent loaded the **aii-use-hardware** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-use-hardware
description: Detect hardware and use it responsibly. Covers CPU/RAM/GPU detection, memory-safe data processing, and resource-aware computation.
---

**Step 1** — Run `bash scripts/get_hardware.sh` (relative to this skill's directory).

Read the `=== CGROUP ===` section carefully. If `Type: cgroup v1` or `cgroup v2`:
- You are in a **container with hard resource limits**. Exceeding them = OOM kill, no recovery.
- **Never** use `psutil.virtual_memory().total`, `free -h`, `/proc/meminfo`, `os.cpu_count()`, or `nproc` for resource limits — these report **host** values, not your container's allocation.
- **Always** read limits from the cgroup paths shown in the output, or use the Python helpers below.
- For **runtime memory monitoring**, read current usage from cgroup too:
  - v2: `/sys/fs/cgroup/memory.current`
  - v1: `/sys/fs/cgroup/memory/memory.usage_in_bytes`

**Step 2** — Use Step 1 results to pick package variants **before** installing.

Defaults often target the most powerful environment — PyPI's `torch` ships with CUDA libs even on CPU-only hosts. Wrong variant = wasted disk, slow setup, possible import-time failures.

If `=== GPU ===` shows `No GPU`, install torch's CPU build (skips ~4.5GB of CUDA libs):
```bash
uv pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
```
Same idea for any library whose wheel selection depends on detected hardware (GPU/CPU-only builds, architecture-specific wheels).

After install, sanity-check imports right away (`python -c "import torch"`). Disk-pressure or interrupted installs leave half-built wheels (e.g. `libtorch_global_deps.so` missing) — catch these before the experiment runs.

**Step 3** — Set Python constants from the Step 1 results:
```python
import os, math, torch, psutil
from pathlib import Path

def _detect_cpus() -> int:
    """Detect actual CPU allocation (containers/pods/bare metal)."""
    try:  # cgroups v2 quota
        parts = Path("/sys/fs/cgroup/cpu.max").read_text().split()
        if parts[0] != "max":
            return math.ceil(int(parts[0]) / int(parts[1]))
    except (FileNotFoundError, ValueError): pass
    try:  # cgroups v1 quota
        q = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_quota_us").read_text())
        p = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_period_us").read_text())
        if q > 0:
            return math.ceil(q / p)
    except (FileNotFoundError, ValueError): pass
    try:  # CPU affinity (cpuset — used by RunPod, Docker --cpuset-cpus)
        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError): pass
    return os.cpu_count() or 1

def _container_ram_gb() -> float | None:
    """Read RAM limit from cgroup (containers/pods)."""
    for p in ["/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"]:
        try:
            v = Path(p).read_text().strip()
            if v != "max" and int(v) < 1_000_000_000_000:
                return int(v) / 1e9
        except (FileNotFoundError, ValueError): pass
    return None

NUM_CPUS = _detect_cpus()
HAS_GPU = torch.cuda.is_available()
VRAM_GB = torch.cuda.get_device_properties(0).total_mem / 1e9 if HAS_GPU else 0
DEVICE = torch.device("cuda" if HAS_GPU else "cpu")
TOTAL_RAM_GB = _container_ram_gb() or psutil.virtual_memory().total / 1e9
AVAILABLE_RAM_GB = min(psutil.virtual_memory().available / 1e9, TOTAL_RAM_GB)
```

## Step 4 — Set Memory Limits

OOM kills the entire container. **Every script MUST set RAM and VRAM limits at startup.**

Decide the budget based on what the script actually needs. Estimate data size × 2-5x for in-memory overhead, then add ~50% breathing room for temporaries. You may use up to 90% of available RAM/VRAM, but **scale gradually** — start small (e.g. 30-50%), verify it works, then increase toward the limit. Never exceed 90% to keep a buffer for the OS, system processes, and the agent runtime itself. Going over crashes the container/machine with no recovery.

```python
import resource, psutil

_avail = psutil.virtual_memory().available
RAM_BUDGET = ???  # YOU decide: estimate what this script needs (in bytes)
assert RAM_BUDGET < _avail, f"Budget {RAM_BUDGET/1e9:.1f}GB > available {_avail/1e9:.1f}GB"
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))  # 3x: virtual > RSS; raises MemoryError on exceed

if HAS_GPU:
    _free, _total = torch.cuda.mem_get_info(0)
    VRAM_BUDGET = ???  # YOU decide: estimate GPU memory needs
    torch.cuda.set_per_process_memory_fraction(min(VRAM_BUDGET / _total, 0.95))  # raises OutOfMemoryError on exceed
```

## Memory-Safe Data Processing

- **One at a time**: load one large object → process → `del obj; gc.collect()` → next
- **Load only what you need**: select specific tables/columns/rows, not entire databases
- **Test small first**: run on a sample before scaling to full data to estimate memory/time
- **Free intermediates in loops**: don't accumulate large results — aggregate incrementally
- **Size before loading**: check file/dataset size before loading; if it's >30% of `RAM_BUDGET`, chunk it

## Common Mistakes (from real crashes)

- **Skipping this skill entirely** — loading data with no RAM detection, no limits, no budget. Container OOM-killed, all agents lost.
- **Using `psutil.virtual_memory().total` instead of `_container_ram_gb()`** — reports host RAM (e.g. 66 GB) when container limit is 28 GB. You MUST use the cgroup-aware functions above.
- **Loading all tables from a multi-table database at once** — one agent loaded 14 RelBench tables simultaneously, spiked past container limit.
- **Setting no memory limits** — without `resource.setrlimit` (RAM) and `set_per_process_memory_fraction` (VRAM), a runaway script OOM-kills the container instead of raising a catchable error.
- **Using `os.cpu_count()` directly** — returns host CPUs (e.g. 192) instead of container limit (e.g. 4) on RunPod/Docker. Always use `_detect_cpus()` above which checks cgroup quota → CPU affinity → `os.cpu_count()` in order.

## Hardware Use

- Keep these results in mind for ALL subsequent tasks — don't assume more than detected
- GPU if available and parallelizable, multiprocessing if multiple CPUs
- Push available resources to their full potential — don't leave hardware idle
````

### [6] SKILL-INPUT — aii-long-running-tasks · 2026-06-17 13:49:09 UTC

The agent loaded the **aii-long-running-tasks** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-long-running-tasks
description: Gradual scaling pattern for long-running autonomous tasks. Use when running experiments, evaluations, or any code that processes data at increasing scale with runtime checks.
---

## Core Principles

1. **Time budget first**: Read your time/runtime constraints before running anything. Set every Bash timeout to fit within the budget.
2. **Start small, scale up**: Run on minimal input first, fix errors, then increase scale.
3. **Extrapolate before scaling**: Use recorded runtimes to predict whether the next step fits in the budget. Don't guess — calculate.
4. **Background execution**: For anything that takes >1 min, run in background (`run_in_background=true`) and do useful work while waiting.
5. **Stop early if needed**: Quality results on less data beats a timeout or crash. It's always acceptable to stop at a smaller scale.

---

## Gradual Scaling Sequence

Run code at increasing data sizes, checking runtime at each step.

Substitute your actual file names:
- `{mini_file}` — mini JSON (3 examples) from dependency workspace
- `{full_file}` — full dataset from dependency workspace
- `{script}` — your processing script (e.g., `./method.py`, `./eval.py`)
- `{schema}` — JSON schema to validate output against

**STEP 1 — MINI DATA:** Run `{script}` on `{mini_file}`. Do NOT truncate logs. Fix all errors. Validate output against `{schema}`. Verify you are NOT using mock scripts, mock data, or mock APIs.

**STEP 2 — 10 EXAMPLES:** Modify `{script}` to load only the first 10 examples from `{full_file}`. Run and fix errors. Validate schema. Record the runtime.

**STEP 3 — 50 EXAMPLES:** Load first 50 examples from `{full_file}`. Run and fix errors. Record runtime. **EXTRAPOLATE**: Using runtimes from steps 2-3, estimate time per example. Calculate how many examples fit in your remaining time budget. If 50 already used most of the budget, stop here.

**STEP 4 — 100 EXAMPLES (if budget allows):** Load first 100 examples. Run and fix errors. Record runtime. Re-extrapolate with the new data point.

**STEP 5 — 200 EXAMPLES (if budget allows):** Load first 200 examples from `{full_file}`. Run and fix errors. Record runtime.

**STEP 6 — MAXIMIZE:** Using all recorded runtimes, extrapolate time-per-example (it may not be perfectly linear — account for overhead). Calculate the maximum number of examples that fits within your remaining time budget with a 10% safety margin. Load that many (or all if they fit). Run and validate.

## Final Testing Phase

After completing the scaling sequence, redo the entire sequence **one more time** up to your final example count:

mini → 10 → 50 → 100 → 200 → max

At each scale: look for issues, fix problems, validate output, ensure it completes within time limits.

---

## Background Execution

For any step that takes >1 min, run as a **background task**:

1. Launch with Bash `run_in_background=true`
2. While it runs, use the time productively:
   - Sanity-check previous outputs
   - Verify file integrity (correct field names, non-empty values)
   - Review code for edge cases at larger scale
   - Prepare the next step
3. Check back on the background task to get results
4. If it failed, fix errors and re-run

---

## Resource Limits

Set hard RAM and CPU time limits so code fails fast instead of crashing the system. Read limits from `<hardware>` and leave headroom for the OS (e.g., if 16GB total, cap at 14GB).

Python example using stdlib `resource` module:
```python
import resource
resource.setrlimit(resource.RLIMIT_AS, (14 * 1024**3, 14 * 1024**3))  # 14GB RAM
resource.setrlimit(resource.RLIMIT_CPU, (3600, 3600))  # 1 hour CPU time
```
Exceeding RAM raises `MemoryError`. Exceeding CPU time sends `SIGKILL`.

## Monitoring

At each step, record runtime AND check resource usage (`free -h` for RAM, `top -bn1 | head -5` for CPU). If memory usage is climbing toward the limit or CPU is pegged, stop and investigate before scaling further.
````

### [7] SKILL-INPUT — aii-json · 2026-06-17 13:49:15 UTC

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

### [8] SKILL-INPUT — aii-file-size-limit · 2026-06-17 13:49:15 UTC

The agent loaded the **aii-file-size-limit** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

```
---
name: aii-file-size-limit
description: File size check procedure for splitting oversized output files. Use after generating JSON output files to check and split files exceeding the provided size limit.
---

## File Size Check

After generating output files, run `ls -lh` to check sizes. If ANY file exceeds the provided file size limit:

1. Create directory with same base name (e.g., `data_out/` for `full_data_out.json`)
2. Split into parts under the limit named: `full_data_out_1.json`, `full_data_out_2.json`, etc.
3. Place parts in directory (e.g., `data_out/full_data_out_1.json`, `data_out/full_data_out_2.json`)
4. Delete the original oversized file
5. Update the script to read from split files: `for f in sorted(glob.glob('data_out/full_data_out_*.json')): data.extend(json.load(open(f)))`
6. For each split part, generate its own mini/preview versions with the json skill's format script
```

### [9] SKILL-INPUT — aii-openrouter-llms · 2026-06-17 13:49:15 UTC

The agent loaded the **aii-openrouter-llms** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-openrouter-llms
description: Searches and calls LLMs from OpenRouter's extensive catalog (Claude, GPT, Gemini, Llama, Mistral, DeepSeek, etc.) with reasoning and temperature control. Use when user needs to access various LLMs, compare language models, call different model providers, find the best model for a task, or look up model pricing and costs per million tokens.
---

## Contents

- Workflow (2-phase model discovery and calling)
- Scripts (Search, Get Params, Call)

**IMPORTANT - Parallel execution:** GNU `parallel` subshells do NOT inherit `source activate`. Use `export` for variables and **single-quoted** command templates so parallel's subshells can resolve them:
```
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

---

## Workflow: Model Discovery and Calling

### Phase 1: Search for Models
Find models with pricing, context length, and descriptions
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_search_llms.py "claude" --limit 5
```

### Phase 2 (optional): Get Model Parameters
Check what parameters a specific model supports
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_get_llm_params.py "anthropic/claude-haiku-4.5"
```

### Phase 3: Call Model
Call a model using the API name from search results
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py --model "anthropic/claude-haiku-4.5" --input "What is 2+2?"
```

---

## Scripts

### Search OpenRouter models (aii_or_search_llms.py)

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_search_llms.py "claude" --limit 5
```

**Parallel execution (multiple queries):**

IMPORTANT: When running multiple searches, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_or_search_llms.py" && \
parallel -j 50 -k --group --will-cite '$PY $S {} --limit 5' ::: 'claude' 'gpt' 'gemini'
```

**Example output:**
```
Found 5 models for query: claude

[1] Anthropic: Claude Opus 4.5
    API: anthropic/claude-opus-4.5
    Context: 200,000 tokens
    Price: $5.00/M in, $25.00/M out
    Claude Opus 4.5 is Anthropic's frontier reasoning model...

[2] Anthropic: Claude Haiku 4.5
    API: anthropic/claude-haiku-4.5
    Context: 200,000 tokens
    Price: $1.00/M in, $5.00/M out
    ...
```

**Parameters:**

`query` (optional, positional)
- Search query to filter models (e.g., 'claude', 'gpt', 'reasoning')

`--limit, -n` (optional)
- Maximum number of results (default: 10)

`--series, -s` (optional)
- Filter by model family
- Valid: GPT, Claude, Gemini, Grok, Cohere, Nova, Qwen, Yi, DeepSeek, Mistral, Llama2, Llama3, Llama4, RWKV, Qwen3, Router, Media, Other, PaLM

`--timeout` (optional)
- Request timeout in seconds (default: 60)

**Tips:**
- Use the `API` field from results for the `--model` parameter in calls
- Search is fast (queries OpenRouter's model list)

---

### Get model parameters (aii_or_get_llm_params.py)

Get detailed information and supported parameters for a specific model.

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_get_llm_params.py "anthropic/claude-haiku-4.5"
```

**Parallel execution (multiple models):**

IMPORTANT: When checking multiple models, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_or_get_llm_params.py" && \
parallel -j 50 -k --group --will-cite '$PY $S {}' ::: 'anthropic/claude-haiku-4.5' 'openai/gpt-4o-mini' 'google/gemini-2.0-flash-001'
```

**Example output:**
```
Model: Anthropic: Claude Haiku 4.5
API: anthropic/claude-haiku-4.5

=== Capabilities ===
Context Length: 200,000 tokens
Max Output: 64,000 tokens
Modality: text+image->text
Input: image, text
Output: text
Moderated: Yes

=== Pricing ===
Input: $1.0000/M tokens
Output: $5.0000/M tokens

=== Supported Parameters ===
  - include_reasoning
  - max_tokens
  - reasoning
  - stop
  - temperature
  - tool_choice
  - tools
  - top_k
  - top_p
```

**Parameters:**

`model` (required, positional)
- Model API name (e.g., 'anthropic/claude-haiku-4.5', 'openai/o1')

`--timeout` (optional)
- Request timeout in seconds (default: 30)

**Tips:**
- Use after search to see which parameters a model supports
- Check supported_parameters before using --reasoning or other options

---

### Call OpenRouter model (aii_or_call_llms.py)

Make an API call to an OpenRouter LLM model.

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py --model "anthropic/claude-haiku-4.5" --input "What is 2+2?"
```

**Parallel execution (multiple calls):**

IMPORTANT: When calling multiple models, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_or_call_llms.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --model {} --input "What is 2+2?"' ::: 'anthropic/claude-haiku-4.5' 'openai/gpt-4o-mini' 'google/gemini-2.0-flash-001'
```

**Example output:**
```
Model: anthropic/claude-haiku-4.5

Response:
Four.

Tokens: 12 in, 5 out
```

**Parameters:**

`--model, -m` (required)
- API model name from search results (format: `provider/model-name`)
- Examples: `anthropic/claude-sonnet-4`, `openai/gpt-5`, `google/gemini-2.5-pro`

`--input, -i` (required, unless using --input-json)
- Simple string prompt

`--input-json` (optional)
- Full conversation JSON for multi-turn (mutually exclusive with --input)

`--max-tokens` (optional)
- Maximum output tokens (default: 9000)

`--reasoning` (optional)
- Reasoning effort for reasoning models: `minimal`, `low`, `medium`, `high`

`--temperature, -t` (optional)
- Randomness (0.0-2.0): 0.0=deterministic, 0.7=balanced, 1.5+=creative

`--top-p` (optional)
- Nucleus sampling (0.0-1.0)

`--instructions` (optional)
- System instructions/prompt

`--web-search` (optional)
- Enable web search with max results (e.g., 10)

`--params, -p` (optional)
- Extra model-specific parameters as JSON string
- Use `aii_or_get_llm_params.py` to see which params a model supports
- Example: `--params '{"top_k": 50, "seed": 42, "frequency_penalty": 0.5}'`

`--timeout` (optional)
- Request timeout in seconds (default: 120)

**Examples:**

Simple call:
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py \
  --model "anthropic/claude-sonnet-4" \
  --input "Write a haiku about coding" \
  --temperature 0.8
```

With system instructions:
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py \
  --model "anthropic/claude-haiku-4.5" \
  --input "Explain recursion" \
  --instructions "You are a helpful programming tutor. Keep explanations concise."
```

With reasoning (for o1-style models):
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py \
  --model "openai/o1" \
  --input "Solve this complex math problem" \
  --reasoning high
```

With web search:
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py \
  --model "anthropic/claude-sonnet-4" \
  --input "What are the latest AI news?" \
  --web-search 10 \
  --max-tokens 15000
```

With extra model-specific params:
```bash
# Step 1: Check what params the model supports
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_get_llm_params.py "meta-llama/llama-3.3-70b-instruct"
# Shows: frequency_penalty, top_k, seed, min_p, etc.

# Step 2: Call with those params
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py \
  --model "meta-llama/llama-3.3-70b-instruct" \
  --input "Write a short poem" \
  --params '{"top_k": 50, "seed": 42, "frequency_penalty": 0.5}'
```

---

## Tips

- Use `aii_or_search_llms.py` first to find models, then copy `API` field for `--model`
- Use `aii_or_get_llm_params.py` to check what params a model supports before using `--params`
- For web search, increase `--max-tokens` to handle larger responses (15000+)

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [10] SKILL-INPUT — aii-parallel-computing · 2026-06-17 13:49:15 UTC

The agent loaded the **aii-parallel-computing** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-parallel-computing
description: "CRITICAL PERFORMANCE SKILL. Maximize hardware utilization for compute-intensive tasks. Covers GPU acceleration, CPU parallelism, and async I/O. The difference between hours of failure and minutes of success. Use whenever writing ANY script that processes data, makes API calls, or does computation."
---

**ALWAYS parallelize. Sequential processing is unacceptable for any non-trivial workload.** A sequential script doing 1000 API calls takes hours and fails halfway. An async version finishes in minutes with proper error handling. ALWAYS ask: "Can this run in parallel?" — the answer is almost always yes.

Read aii-use-hardware skill first → get `NUM_CPUS`, `HAS_GPU`, `VRAM_GB`, `device`. Set `NUM_WORKERS` proportional to available CPU capacity — check `psutil.cpu_percent(interval=1)` and scale accordingly (e.g. 30% used → use ~70% of cores).

## Decision Tree (follow strictly)

- **I/O-bound** (API calls, downloads, web, file reads) → `asyncio` + `aiohttp` with `Semaphore(NUM_WORKERS * 4)`. NEVER do sequential HTTP requests in a loop.
- **CPU-bound, vectorizable** → GPU available: PyTorch on device / No GPU: NumPy vectorized ops. NEVER loop over array elements in Python.
- **CPU-bound, independent items** → `ProcessPoolExecutor(max_workers=NUM_WORKERS)`. NEVER process items one-by-one when they're independent.
- **Sequential** → only acceptable when items have data dependencies (each depends on the previous result).

## GPU Rules

- Use up to 90% of available VRAM — scale gradually (start small, increase after each successful run, keep 10% buffer)
- Move to device → compute → move back: `torch.tensor(data, device=device)` → `.cpu().numpy()`
- OOM fallback: catch `torch.cuda.OutOfMemoryError` → `empty_cache()` → halve batch size → retry on GPU. Keep reducing until it fits. Stay on GPU.
- Batch large data: chunk it, `del batch` between iterations to free VRAM

## Parallelism Rules

- **CPU-bound**: `ProcessPoolExecutor` + `as_completed`, pre-allocate result list indexed by submission order
- **I/O-bound**: `asyncio` + `aiohttp`, `Semaphore(NUM_WORKERS * 4)`, single shared `ClientSession`, `asyncio.gather(*tasks, return_exceptions=True)`
- Always add `tenacity` retries for transient failures, always set timeouts on HTTP requests
- **CRITICAL — `ProcessPoolExecutor` start method**: Default `fork` deadlocks with loguru (and any threading library). ALWAYS pass `mp_context=multiprocessing.get_context("spawn")` when constructing `ProcessPoolExecutor` in any script that uses loguru, threading, or async I/O. Example:
  ```python
  import multiprocessing as mp
  from concurrent.futures import ProcessPoolExecutor
  with ProcessPoolExecutor(max_workers=N, mp_context=mp.get_context("spawn")) as pool:
      ...
  ```
````

### [11] SYSTEM-USER prompt · 2026-06-17 14:27:52 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/results/out.json`
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
id: gen_plan_dataset_1_idx3
type: dataset
title: >-
  First-Letter-Spelling Absorption Testbed: Content/Surface-Flip Minimal Pairs + Frozen Pile Letter-Occurrence Corpus (L primary;
  O/T/I/D secondary)
summary: >-
  The single most load-bearing dataset for the Two-Track Co-Response Grouping hypothesis. Build, per target letter (L end-to-end
  first, then O/T/I/D), three linked components into one schema-standardized data_out.json: (A) CONTENT-FLIP minimal pairs
  ('starts-with-<letter>' present vs absent, surface-matched in a shared carrier) for the Tier-0 K-proposal pilot and the
  C3 absorber-recovery spine; (B) SURFACE-FLIP pairs (two different words SAME first letter) for the unit-level surface-invariance
  check; (C) a FROZEN natural-text corpus from monology/pile-uncopyrighted (pinned rev 3be9033) of slot-eligible alphabetic
  tokens starting with each letter, with per-token occurrence counts and real in-context windows, so iteration-2's form-free/Chanin
  (2409.14507) diagnostic can locate the false-negative ('lion'/'London') absorbers. Words are anchored in the real gemma-2-2b
  vocabulary via the exact sae-spelling get_alpha_tokens filter; pairs are mechanically constructed + LLM-judge-validated
  (OpenRouter, <$3, pass rates reported). Pure CPU/data task (no SAE, no GPU). Schema-validate; emit full/mini/preview under
  300MB.
runpod_compute_profile: cpu_heavy
ideal_dataset_criteria: |-
  PURPOSE & ROLE. This is the LOAD-BEARING absorption testbed: it feeds (1) the Tier-0 K-track PROPOSAL-step pilot (does anchored greedy set-cover, given ONLY the content-flip pairs, recover the known {general 'starts-with-L' parent + 'lion'/'London' absorbers} that the Chanin 2409.14507 diagnostic identifies?), and (2) the C3 absorber-recovery spine (the co-response unit recovers absorbers the marginal-attribution pools (g)/(h) drop, with KG edges agreeing with the form-free absorption diagnostic). It is PURE TEXT + tokenizer + LLM-judge construction; it does NOT run the SAE or read activations (that happens in iteration-2 experiments). Deliver letter L FULLY end-to-end before broadening to O/T/I/D.

  THREE COMPONENTS PER TARGET LETTER, all merged into one data_out.json:
  (A) CONTENT-FLIP PAIRS. Each pair = (x_off, x_on) embedded in an IDENTICAL carrier template, differing only in the slotted word: x_on = a word STARTING WITH the target letter (concept present); x_off = a matched word NOT starting with the letter (concept absent). 'Surface-matched' = the two slotted words are matched as closely as feasible on character length, token count (both ideally SINGLE gemma-2-2b tokens), and rough corpus frequency, so the only systematic difference is the first-letter identity. Multiple distinct carrier templates per word so cover-sets/precision can be computed across contexts. Target ~300-500 content-flip pairs for L; ~150-300 for each secondary letter (scale to the 300MB cap; mini/preview handle size).
  (B) SURFACE-FLIP PAIRS. Each pair = (x_a, x_b) in the same carrier, where BOTH slotted words start with the target letter but are DIFFERENT words/surface realizations (e.g., 'lion' vs 'lamp'; or same word in two carrier phrasings). The concept 'starts-with-L' is held CONSTANT while surface varies — used for the unit-level surface-invariance admission check (a good unit's pooled response to surface flips ~ 0). Target ~150-250 for L, ~80-150 per secondary letter.
  (C) FROZEN NATURAL-TEXT CORPUS (the diagnostic substrate). From monology/pile-uncopyrighted at PINNED revision 3be9033, provide for each target letter: (c1) a per-token OCCURRENCE-COUNT TABLE over a fixed pile sample, restricted to SLOT-ELIGIBLE word-initial alphabetic tokens whose first letter is the target; (c2) REAL in-context windows (e.g., ~32-64 token windows) sampled from the same pile docs, each containing >=1 target-letter slot-eligible token with that token's position annotated, capped per word-type to bound size. This lets iteration-2 train the parent 'starts-with-L' probe on real activations and search for false negatives (absorbed words). Cap ~30-80 contexts per word-type and a few thousand contexts per letter total.

  WORD ANCHORING — EXACT get_alpha_tokens RECIPE (verbatim from lasr-spelling/sae-spelling vocab.py; replicate it, ~10 lines). ALL_ALPHA_LETTERS = the 26 lowercase + 26 uppercase a-z. For each token in tokenizer.vocab: word = tokenizer.convert_tokens_to_string([token]); if allow_leading_space and word/token starts with ' ': strip exactly ONE leading space; keep iff len>0 AND every remaining char is in ALL_ALPHA_LETTERS. SLOT-ELIGIBILITY = the token is WORD-INITIAL (it originally carried the leading-space/'▁' marker, i.e. it represents the start of a word) AND passes the alpha filter — only word-initial tokens carry clean 'starts-with-<letter>' semantics, matching the SAE's first-letter regime (Gemma Scope L12 width_16k canonical context). The first letter = word.strip()[0].lower(). Group eligible words by first letter. Prefer SINGLE-TOKEN words for clean activation reads; record is_single_token and is_slot_eligible per word.

  TOKENIZER. Use the gemma-2-2b tokenizer. google/gemma-2-2b is GATED; use the ungated mirror unsloth/gemma-2-2b (identical vocab) OR google/gemma-2-2b with an HF_TOKEN env var. Verify vocab size == 256000 as a sanity gate. No model weights are needed — tokenizer only.

  ABSORBER CANDIDATES (metadata). For each letter, attach a candidate-absorber sublist: high-frequency single-token word-types most likely to host dedicated absorbers (e.g., L: 'lion','London','little','life','love','line' — derive empirically as the top-frequency slot-eligible words from the corpus table, union with any sae-spelling/Chanin-published examples). This is METADATA ONLY (a hint for iteration-2), never used to construct or filter the units.

  SPELLING-PROMPT CARRIERS (anchor to the documented regime). Include at least one carrier family mirroring sae-spelling prompting.py: the verbose first-letter template VERBOSE_FIRST_LETTER_TEMPLATE = '{word} has the first letter:' and/or default '{word}:', optionally with a few shuffled in-context-learning (ICL) examples (create_icl_prompt-style, newline-separated, no word contamination across examples) and answer ' <LETTER>' (space-prefixed, uppercase). ALSO include 2-4 NEUTRAL carrier sentences (e.g., 'I saw a {word} yesterday.', 'The {word} was on the table.', 'They wrote about {word} in the report.') so cover-sets span multiple natural contexts, not just the spelling prompt.

  SCHEMA (shared across the run's 4 datasets). data_out.json = {"metadata": {...dataset-level...}, "data": [ rows ]}. Each ROW: {"input": <text the SAE will encode>, "output": <concept-label string>, "metadata": {dataset:'first_letter_spelling', letter:'L', pair_id:'L_c_0001', pair_type:'content_flip'|'surface_flip'|'corpus_context', role:'on'|'off'|'var_a'|'var_b'|'occurrence', sub_context:<the specific word/token covered — THE key field>, target_word, counterpart_word, template_id, label_starts_with_target:1|0, is_single_token, is_slot_eligible, first_letter, fold; corpus rows ALSO: source_doc_id, pile_revision:'3be9033', token_position, window_char_span}}. output = the first letter (e.g. 'L') for on-rows / the off-word's actual first letter for off-rows / the token's first letter for corpus rows (supports both multi-class first-letter and binary starts-with-target framings; binary label also in metadata.label_starts_with_target). Pairs are LINKED by shared pair_id + role so iteration-2 can reconstruct (x_on,x_off) and compute r_l(p)=a_l(x_on)-a_l(x_off). DATASET-LEVEL metadata: per-letter per-token occurrence table (the big table lives HERE, not per-row), absorber-candidate sublists, LLM-judge pass-rates per (letter,pair_type), achieved counts per letter, generation config (models used, pinned pile revision, tokenizer id, get_alpha_tokens params), and total LLM $ spent.

  FOLDS. Doc-level folds for the corpus (assign each pile source doc to a fold by hashing source_doc_id → fold_0..fold_4) so probe train/test never leaks across the same document. For minimal pairs, fold by TARGET WORD (a given word-type appears in exactly one fold) to prevent word-identity leakage in any downstream probe.

  VALIDATION & SIZE. LLM-judge each pair (or a representative >=150/letter sample if total is large) for 'content correctly flipped (on starts-with-letter, off does not) AND surface preserved/grammatical'; report pass rate per letter & pair_type in metadata; DROP failed pairs. Keep total LLM spend <$3 (cheap flash/mini/haiku-tier model via OpenRouter; track cumulative cost, hard-stop at $3). Schema-validate with aii-json; emit full + mini + preview; run the aii-file-size-limit check and keep full data_out.json <=300MB (cap corpus contexts/word and pair counts on secondary letters to stay under).

  WHY THIS IS IDEAL. It is non-circular (words from public vocab + pile, never from the SAE latents being grouped), guaranteed-signal (first-letter absorption is the documented regime), provides BOTH the synthetic minimal pairs (for the pilot/co-response) AND the natural corpus (for the diagnostic), and is frozen/reproducible (pinned pile revision, pinned tokenizer, recorded config).
dataset_search_plan: |-
  STEP 0 — ENV & PINS (no GPU; cpu_heavy). Read skills: aii-hf-datasets, aii-openrouter-llms, aii-json, aii-file-size-limit, aii-python, aii-use-hardware. Confirm internet + HF access. Pin: pile dataset = monology/pile-uncopyrighted, revision='3be9033' (full SHA begins 3be90335; 'Upload to LFS', Aug 31 2023); tokenizer = unsloth/gemma-2-2b (ungated mirror; fallback google/gemma-2-2b with HF_TOKEN). Reference code = lasr-spelling/sae-spelling (vocab.py get_alpha_tokens / get_tokens; prompting.py SpellingPrompt, VERBOSE_FIRST_LETTER_TEMPLATE='{word} has the first letter:', first_letter_formatter, create_icl_prompt). If the sae_spelling pip package is unavailable, REPLICATE get_alpha_tokens inline (provided verbatim in the criteria).

  STEP 1 — BUILD THE VOCABULARY WORD LISTS. Load the gemma-2-2b tokenizer; assert vocab_size==256000. Apply get_alpha_tokens (allow_leading_space=True, replace_special_chars=True). Determine slot-eligibility: a token is slot-eligible iff it is WORD-INITIAL (raw token starts with the leading-space/'▁' marker) AND alpha. Compute first_letter = word.strip()[0].lower(). Group eligible words by first letter; flag is_single_token. Produce, per letter, the master word-type list (on-words). Build a pooled OFF-word list (slot-eligible words NOT starting with the target letter) for content-flip counterparts. NON-DEGENERACY GATE: a letter is usable only if it has enough distinct single-token slot-eligible word-types to support its target pair count (this is why L/O/T/I/D are chosen and S/X — k=1 singletons — are avoided); if a secondary letter has too few word-types, DROP it and record the reason. Prioritize L first.

  STEP 2 — FROZEN PILE CORPUS (component C). Stream monology/pile-uncopyrighted at the pinned revision (datasets.load_dataset(..., split='train', streaming=True, revision='3be9033')). FALLBACK if streaming is broken (known HF discussion #5): hf_hub_download the single shard train/00.jsonl.zst at the pinned revision, decompress with zstandard, read line-by-line. Take a FIXED, deterministic sample (e.g., first ~100k-300k documents) — record the exact count for reproducibility. For each doc: tokenize, walk tokens, and for every slot-eligible word-initial token whose first letter is a target letter: (a) increment its global occurrence count (per-letter per-token table), (b) with reservoir/capped sampling, store a ~32-64 token context window (decoded to text) + token_position + source_doc_id, capping at ~30-80 windows per word-type and a few-thousand per letter. Emit corpus_context rows; put the aggregate occurrence table in DATASET-LEVEL metadata. Derive each letter's empirical absorber-candidate sublist = the top-frequency single-token word-types (union with known examples like lion/London for L). Assign doc-level folds by hashing source_doc_id.

  STEP 3 — CONTENT-FLIP PAIRS (component A). Define 4-8 carrier templates per letter: include >=1 sae-spelling-style first-letter prompt ('{word} has the first letter:' / '{word}:', optionally with shuffled ICL examples and ' <LETTER>' answer) and 3-5 neutral sentence carriers. For each chosen on-word (prioritize single-token, frequency-spanning, including absorber candidates), pick a surface-matched off-word (closest match on char length, token count, frequency bucket; both single-token preferred). Instantiate the SAME carrier with on-word and off-word → an (x_on,x_off) pair sharing pair_id, role on/off, identical template_id, sub_context=on-word, counterpart_word=off-word. Record label_starts_with_target (1 for on, 0 for off) and the char/token span of the slotted word. Target ~300-500 pairs for L, ~150-300 per secondary; span many distinct on-words × multiple carriers.

  STEP 4 — SURFACE-FLIP PAIRS (component B). For pairs of DISTINCT on-words (both start with target letter) in the same carrier, OR the same on-word across two carrier phrasings, emit (x_a,x_b) sharing pair_id, roles var_a/var_b, pair_type='surface_flip', sub_context = the word(s) covered. The concept is held constant; only surface changes. Target ~150-250 for L, ~80-150 per secondary.

  STEP 5 — LLM-JUDGE VALIDATION (OpenRouter, <$3). Use a cheap flash/mini/haiku-tier model via aii-openrouter-llms. For each pair, ask the judge: for content_flip — does x_on contain a word starting with '<L>' in the slot, x_off a word NOT starting with '<L>', and is the carrier grammatical/surface-preserved across both? for surface_flip — do both contain DIFFERENT same-first-letter realizations while staying grammatical? Return pass/fail + reason. If total pairs are large, judge a representative sample of >=150 per letter and report the sampled pass rate; otherwise judge all. DROP failed pairs; record pass-rate per (letter,pair_type) and cumulative $ in metadata. Track cost after every batch; HARD-STOP at $3 (fall back to mechanical-only construction if budget is hit — mechanical first-letter pairs are largely self-validating).

  STEP 6 — ASSEMBLE, VALIDATE, SPLIT. Merge all rows into data_out.json with the shared schema (dataset-level metadata block + data array). Fold minimal pairs by target word; corpus by source doc. Validate against the shared run schema with aii-json (input/output strings present; required metadata keys present; pair_ids link consistently; no orphan roles). Run aii-file-size-limit; if full >300MB, reduce secondary-letter pair counts and per-word corpus-context caps first (NEVER reduce L). Emit full + mini + preview. Self-check report: counts per letter, per-pair-type, corpus contexts, occurrence-table size, judge pass-rates, total $ spent, and an explicit confirmation that L is complete end-to-end.

  FAILURE SCENARIOS & FALLBACKS. (i) Tokenizer gated → unsloth/gemma-2-2b mirror; verify vocab_size. (ii) Pile streaming broken → download single pinned shard + zstandard decode. (iii) Too few single-token word-types for a letter → supplement on-words with LLM-proposed common words RE-VERIFIED to be single gemma-2-2b tokens; if still too few, drop that secondary letter and document. (iv) LLM budget exhausted → mechanical pairs only, report which letters lack LLM-validated pass rates. (v) Size pressure → mini/preview + cap secondary letters; L stays full. (vi) A target letter is degenerate (k=1, like S/X) → exclude and record. PRIORITY ORDER if time-constrained: L (all 3 components, full) > corpus tables for O/T/I/D > content-flip pairs O/T/I/D > surface-flip pairs O/T/I/D.
target_num_datasets: 5
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
TODO 1. For the top 10 datasets, create data.py (uv inline script) that: loads from temp/datasets/, standardizes to exp_sel_data_out.json schema (aii-json skill), extracts all examples per dataset, handles domain requirements, saves to full_data_out.json.

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
TODO 3. Read preview to inspect examples. Choose THE BEST 5 DATASETS based on domain requirements and artifact objective. Be very attentive to meticulously and exhaustively fix any errors in your code.
</todos>
````

### [12] SYSTEM-USER prompt · 2026-06-17 14:38:12 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/results/out.json`
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
id: gen_plan_dataset_1_idx3
type: dataset
title: >-
  First-Letter-Spelling Absorption Testbed: Content/Surface-Flip Minimal Pairs + Frozen Pile Letter-Occurrence Corpus (L primary;
  O/T/I/D secondary)
summary: >-
  The single most load-bearing dataset for the Two-Track Co-Response Grouping hypothesis. Build, per target letter (L end-to-end
  first, then O/T/I/D), three linked components into one schema-standardized data_out.json: (A) CONTENT-FLIP minimal pairs
  ('starts-with-<letter>' present vs absent, surface-matched in a shared carrier) for the Tier-0 K-proposal pilot and the
  C3 absorber-recovery spine; (B) SURFACE-FLIP pairs (two different words SAME first letter) for the unit-level surface-invariance
  check; (C) a FROZEN natural-text corpus from monology/pile-uncopyrighted (pinned rev 3be9033) of slot-eligible alphabetic
  tokens starting with each letter, with per-token occurrence counts and real in-context windows, so iteration-2's form-free/Chanin
  (2409.14507) diagnostic can locate the false-negative ('lion'/'London') absorbers. Words are anchored in the real gemma-2-2b
  vocabulary via the exact sae-spelling get_alpha_tokens filter; pairs are mechanically constructed + LLM-judge-validated
  (OpenRouter, <$3, pass rates reported). Pure CPU/data task (no SAE, no GPU). Schema-validate; emit full/mini/preview under
  300MB.
runpod_compute_profile: cpu_heavy
ideal_dataset_criteria: |-
  PURPOSE & ROLE. This is the LOAD-BEARING absorption testbed: it feeds (1) the Tier-0 K-track PROPOSAL-step pilot (does anchored greedy set-cover, given ONLY the content-flip pairs, recover the known {general 'starts-with-L' parent + 'lion'/'London' absorbers} that the Chanin 2409.14507 diagnostic identifies?), and (2) the C3 absorber-recovery spine (the co-response unit recovers absorbers the marginal-attribution pools (g)/(h) drop, with KG edges agreeing with the form-free absorption diagnostic). It is PURE TEXT + tokenizer + LLM-judge construction; it does NOT run the SAE or read activations (that happens in iteration-2 experiments). Deliver letter L FULLY end-to-end before broadening to O/T/I/D.

  THREE COMPONENTS PER TARGET LETTER, all merged into one data_out.json:
  (A) CONTENT-FLIP PAIRS. Each pair = (x_off, x_on) embedded in an IDENTICAL carrier template, differing only in the slotted word: x_on = a word STARTING WITH the target letter (concept present); x_off = a matched word NOT starting with the letter (concept absent). 'Surface-matched' = the two slotted words are matched as closely as feasible on character length, token count (both ideally SINGLE gemma-2-2b tokens), and rough corpus frequency, so the only systematic difference is the first-letter identity. Multiple distinct carrier templates per word so cover-sets/precision can be computed across contexts. Target ~300-500 content-flip pairs for L; ~150-300 for each secondary letter (scale to the 300MB cap; mini/preview handle size).
  (B) SURFACE-FLIP PAIRS. Each pair = (x_a, x_b) in the same carrier, where BOTH slotted words start with the target letter but are DIFFERENT words/surface realizations (e.g., 'lion' vs 'lamp'; or same word in two carrier phrasings). The concept 'starts-with-L' is held CONSTANT while surface varies — used for the unit-level surface-invariance admission check (a good unit's pooled response to surface flips ~ 0). Target ~150-250 for L, ~80-150 per secondary letter.
  (C) FROZEN NATURAL-TEXT CORPUS (the diagnostic substrate). From monology/pile-uncopyrighted at PINNED revision 3be9033, provide for each target letter: (c1) a per-token OCCURRENCE-COUNT TABLE over a fixed pile sample, restricted to SLOT-ELIGIBLE word-initial alphabetic tokens whose first letter is the target; (c2) REAL in-context windows (e.g., ~32-64 token windows) sampled from the same pile docs, each containing >=1 target-letter slot-eligible token with that token's position annotated, capped per word-type to bound size. This lets iteration-2 train the parent 'starts-with-L' probe on real activations and search for false negatives (absorbed words). Cap ~30-80 contexts per word-type and a few thousand contexts per letter total.

  WORD ANCHORING — EXACT get_alpha_tokens RECIPE (verbatim from lasr-spelling/sae-spelling vocab.py; replicate it, ~10 lines). ALL_ALPHA_LETTERS = the 26 lowercase + 26 uppercase a-z. For each token in tokenizer.vocab: word = tokenizer.convert_tokens_to_string([token]); if allow_leading_space and word/token starts with ' ': strip exactly ONE leading space; keep iff len>0 AND every remaining char is in ALL_ALPHA_LETTERS. SLOT-ELIGIBILITY = the token is WORD-INITIAL (it originally carried the leading-space/'▁' marker, i.e. it represents the start of a word) AND passes the alpha filter — only word-initial tokens carry clean 'starts-with-<letter>' semantics, matching the SAE's first-letter regime (Gemma Scope L12 width_16k canonical context). The first letter = word.strip()[0].lower(). Group eligible words by first letter. Prefer SINGLE-TOKEN words for clean activation reads; record is_single_token and is_slot_eligible per word.

  TOKENIZER. Use the gemma-2-2b tokenizer. google/gemma-2-2b is GATED; use the ungated mirror unsloth/gemma-2-2b (identical vocab) OR google/gemma-2-2b with an HF_TOKEN env var. Verify vocab size == 256000 as a sanity gate. No model weights are needed — tokenizer only.

  ABSORBER CANDIDATES (metadata). For each letter, attach a candidate-absorber sublist: high-frequency single-token word-types most likely to host dedicated absorbers (e.g., L: 'lion','London','little','life','love','line' — derive empirically as the top-frequency slot-eligible words from the corpus table, union with any sae-spelling/Chanin-published examples). This is METADATA ONLY (a hint for iteration-2), never used to construct or filter the units.

  SPELLING-PROMPT CARRIERS (anchor to the documented regime). Include at least one carrier family mirroring sae-spelling prompting.py: the verbose first-letter template VERBOSE_FIRST_LETTER_TEMPLATE = '{word} has the first letter:' and/or default '{word}:', optionally with a few shuffled in-context-learning (ICL) examples (create_icl_prompt-style, newline-separated, no word contamination across examples) and answer ' <LETTER>' (space-prefixed, uppercase). ALSO include 2-4 NEUTRAL carrier sentences (e.g., 'I saw a {word} yesterday.', 'The {word} was on the table.', 'They wrote about {word} in the report.') so cover-sets span multiple natural contexts, not just the spelling prompt.

  SCHEMA (shared across the run's 4 datasets). data_out.json = {"metadata": {...dataset-level...}, "data": [ rows ]}. Each ROW: {"input": <text the SAE will encode>, "output": <concept-label string>, "metadata": {dataset:'first_letter_spelling', letter:'L', pair_id:'L_c_0001', pair_type:'content_flip'|'surface_flip'|'corpus_context', role:'on'|'off'|'var_a'|'var_b'|'occurrence', sub_context:<the specific word/token covered — THE key field>, target_word, counterpart_word, template_id, label_starts_with_target:1|0, is_single_token, is_slot_eligible, first_letter, fold; corpus rows ALSO: source_doc_id, pile_revision:'3be9033', token_position, window_char_span}}. output = the first letter (e.g. 'L') for on-rows / the off-word's actual first letter for off-rows / the token's first letter for corpus rows (supports both multi-class first-letter and binary starts-with-target framings; binary label also in metadata.label_starts_with_target). Pairs are LINKED by shared pair_id + role so iteration-2 can reconstruct (x_on,x_off) and compute r_l(p)=a_l(x_on)-a_l(x_off). DATASET-LEVEL metadata: per-letter per-token occurrence table (the big table lives HERE, not per-row), absorber-candidate sublists, LLM-judge pass-rates per (letter,pair_type), achieved counts per letter, generation config (models used, pinned pile revision, tokenizer id, get_alpha_tokens params), and total LLM $ spent.

  FOLDS. Doc-level folds for the corpus (assign each pile source doc to a fold by hashing source_doc_id → fold_0..fold_4) so probe train/test never leaks across the same document. For minimal pairs, fold by TARGET WORD (a given word-type appears in exactly one fold) to prevent word-identity leakage in any downstream probe.

  VALIDATION & SIZE. LLM-judge each pair (or a representative >=150/letter sample if total is large) for 'content correctly flipped (on starts-with-letter, off does not) AND surface preserved/grammatical'; report pass rate per letter & pair_type in metadata; DROP failed pairs. Keep total LLM spend <$3 (cheap flash/mini/haiku-tier model via OpenRouter; track cumulative cost, hard-stop at $3). Schema-validate with aii-json; emit full + mini + preview; run the aii-file-size-limit check and keep full data_out.json <=300MB (cap corpus contexts/word and pair counts on secondary letters to stay under).

  WHY THIS IS IDEAL. It is non-circular (words from public vocab + pile, never from the SAE latents being grouped), guaranteed-signal (first-letter absorption is the documented regime), provides BOTH the synthetic minimal pairs (for the pilot/co-response) AND the natural corpus (for the diagnostic), and is frozen/reproducible (pinned pile revision, pinned tokenizer, recorded config).
dataset_search_plan: |-
  STEP 0 — ENV & PINS (no GPU; cpu_heavy). Read skills: aii-hf-datasets, aii-openrouter-llms, aii-json, aii-file-size-limit, aii-python, aii-use-hardware. Confirm internet + HF access. Pin: pile dataset = monology/pile-uncopyrighted, revision='3be9033' (full SHA begins 3be90335; 'Upload to LFS', Aug 31 2023); tokenizer = unsloth/gemma-2-2b (ungated mirror; fallback google/gemma-2-2b with HF_TOKEN). Reference code = lasr-spelling/sae-spelling (vocab.py get_alpha_tokens / get_tokens; prompting.py SpellingPrompt, VERBOSE_FIRST_LETTER_TEMPLATE='{word} has the first letter:', first_letter_formatter, create_icl_prompt). If the sae_spelling pip package is unavailable, REPLICATE get_alpha_tokens inline (provided verbatim in the criteria).

  STEP 1 — BUILD THE VOCABULARY WORD LISTS. Load the gemma-2-2b tokenizer; assert vocab_size==256000. Apply get_alpha_tokens (allow_leading_space=True, replace_special_chars=True). Determine slot-eligibility: a token is slot-eligible iff it is WORD-INITIAL (raw token starts with the leading-space/'▁' marker) AND alpha. Compute first_letter = word.strip()[0].lower(). Group eligible words by first letter; flag is_single_token. Produce, per letter, the master word-type list (on-words). Build a pooled OFF-word list (slot-eligible words NOT starting with the target letter) for content-flip counterparts. NON-DEGENERACY GATE: a letter is usable only if it has enough distinct single-token slot-eligible word-types to support its target pair count (this is why L/O/T/I/D are chosen and S/X — k=1 singletons — are avoided); if a secondary letter has too few word-types, DROP it and record the reason. Prioritize L first.

  STEP 2 — FROZEN PILE CORPUS (component C). Stream monology/pile-uncopyrighted at the pinned revision (datasets.load_dataset(..., split='train', streaming=True, revision='3be9033')). FALLBACK if streaming is broken (known HF discussion #5): hf_hub_download the single shard train/00.jsonl.zst at the pinned revision, decompress with zstandard, read line-by-line. Take a FIXED, deterministic sample (e.g., first ~100k-300k documents) — record the exact count for reproducibility. For each doc: tokenize, walk tokens, and for every slot-eligible word-initial token whose first letter is a target letter: (a) increment its global occurrence count (per-letter per-token table), (b) with reservoir/capped sampling, store a ~32-64 token context window (decoded to text) + token_position + source_doc_id, capping at ~30-80 windows per word-type and a few-thousand per letter. Emit corpus_context rows; put the aggregate occurrence table in DATASET-LEVEL metadata. Derive each letter's empirical absorber-candidate sublist = the top-frequency single-token word-types (union with known examples like lion/London for L). Assign doc-level folds by hashing source_doc_id.

  STEP 3 — CONTENT-FLIP PAIRS (component A). Define 4-8 carrier templates per letter: include >=1 sae-spelling-style first-letter prompt ('{word} has the first letter:' / '{word}:', optionally with shuffled ICL examples and ' <LETTER>' answer) and 3-5 neutral sentence carriers. For each chosen on-word (prioritize single-token, frequency-spanning, including absorber candidates), pick a surface-matched off-word (closest match on char length, token count, frequency bucket; both single-token preferred). Instantiate the SAME carrier with on-word and off-word → an (x_on,x_off) pair sharing pair_id, role on/off, identical template_id, sub_context=on-word, counterpart_word=off-word. Record label_starts_with_target (1 for on, 0 for off) and the char/token span of the slotted word. Target ~300-500 pairs for L, ~150-300 per secondary; span many distinct on-words × multiple carriers.

  STEP 4 — SURFACE-FLIP PAIRS (component B). For pairs of DISTINCT on-words (both start with target letter) in the same carrier, OR the same on-word across two carrier phrasings, emit (x_a,x_b) sharing pair_id, roles var_a/var_b, pair_type='surface_flip', sub_context = the word(s) covered. The concept is held constant; only surface changes. Target ~150-250 for L, ~80-150 per secondary.

  STEP 5 — LLM-JUDGE VALIDATION (OpenRouter, <$3). Use a cheap flash/mini/haiku-tier model via aii-openrouter-llms. For each pair, ask the judge: for content_flip — does x_on contain a word starting with '<L>' in the slot, x_off a word NOT starting with '<L>', and is the carrier grammatical/surface-preserved across both? for surface_flip — do both contain DIFFERENT same-first-letter realizations while staying grammatical? Return pass/fail + reason. If total pairs are large, judge a representative sample of >=150 per letter and report the sampled pass rate; otherwise judge all. DROP failed pairs; record pass-rate per (letter,pair_type) and cumulative $ in metadata. Track cost after every batch; HARD-STOP at $3 (fall back to mechanical-only construction if budget is hit — mechanical first-letter pairs are largely self-validating).

  STEP 6 — ASSEMBLE, VALIDATE, SPLIT. Merge all rows into data_out.json with the shared schema (dataset-level metadata block + data array). Fold minimal pairs by target word; corpus by source doc. Validate against the shared run schema with aii-json (input/output strings present; required metadata keys present; pair_ids link consistently; no orphan roles). Run aii-file-size-limit; if full >300MB, reduce secondary-letter pair counts and per-word corpus-context caps first (NEVER reduce L). Emit full + mini + preview. Self-check report: counts per letter, per-pair-type, corpus contexts, occurrence-table size, judge pass-rates, total $ spent, and an explicit confirmation that L is complete end-to-end.

  FAILURE SCENARIOS & FALLBACKS. (i) Tokenizer gated → unsloth/gemma-2-2b mirror; verify vocab_size. (ii) Pile streaming broken → download single pinned shard + zstandard decode. (iii) Too few single-token word-types for a letter → supplement on-words with LLM-proposed common words RE-VERIFIED to be single gemma-2-2b tokens; if still too few, drop that secondary letter and document. (iv) LLM budget exhausted → mechanical pairs only, report which letters lack LLM-validated pass rates. (v) Size pressure → mini/preview + cap secondary letters; L stays full. (vi) A target letter is degenerate (k=1, like S/X) → exclude and record. PRIORITY ORDER if time-constrained: L (all 3 components, full) > corpus tables for O/T/I/D > content-flip pairs O/T/I/D > surface-flip pairs O/T/I/D.
target_num_datasets: 5
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
TODO 1. Update data.py to only include the chosen 5 datasets and generate full_data_out.json. Re-run to generate full_data_out.json. Validate output format with aii-json skill and fix any errors. Generate full, mini, and preview versions with aii-json skill's format script using `--input full_data_out.json` (creates full_full_data_out.json, mini_full_data_out.json, preview_full_data_out.json — rename to full_data_out.json, mini_data_out.json, preview_data_out.json).
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
