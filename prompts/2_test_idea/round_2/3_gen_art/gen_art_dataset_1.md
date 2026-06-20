# gen_art_dataset_1 — test_idea

> Phase: `invention_loop` · round 2 · `gen_art`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_dataset_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-17 15:41:06 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_dataset_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/results/out.json`
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
id: gen_plan_dataset_1_idx5
type: dataset
title: >-
  Enlarge & Independently Re-Judge the Surface-Invariance Pair Sets (First-Letter + Toxicity) for the Step-5 Admission AND-Gate
summary: >-
  Build a drop-in SUPERSET of the two iter-1 surface-flip pair sets that the next iteration's Step-5 admission AND-gate consumes.
  (1) Enlarge the FIRST-LETTER surface_flip set from 590 -> >=1,500 concept-constant pairs (two distinct single-token, slot-eligible
  words sharing the same first letter in the 3 carrier templates; deterministic check is AUTHORITATIVE). (2) Enlarge the TOXICITY
  surface_pair set from 546 -> >=1,500 toxic->toxic paraphrases (toxicity held constant, wording changed) generated via OpenRouter
  under the existing token-Jaccard<=0.6 + char-change>=0.25 double-gate. (3) Break the same-model generate-and-judge circularity
  by judging/re-judging a stratified sample with anthropic/claude-haiku-4.5 (a family different from both gpt-4o-mini, which
  generated AND judged toxicity, and gemini-3.1-flash-lite, which judged first-letter), report cross-judge agreement (Cohen's
  kappa) + the genuinely-meaning-preserving pass rate, and the confirmation rate of the 546 originals. Emit in the identical
  exp_sel_data_out flattened-metadata schema (pair_id/role linkage, doc-level folds), preserving the iter-1 originals VERBATIM,
  then report per-concept surface-response null distribution sizes. Schema-validate with aii-json; emit full/mini/preview.
  Hard $10 OpenRouter cap (est. ~$3-4); no GPU.
runpod_compute_profile: cpu_heavy
ideal_dataset_criteria: |-
  TWO enlarged surface-flip pair sets, each a superset of the frozen iter-1 originals, emitted in the SAME exp_sel_data_out flattened-metadata schema so the next iteration's admission filter consumes them identically.

  WHAT A SURFACE-FLIP PAIR IS (the load-bearing semantics): a CONCEPT-CONSTANT, SURFACE-CHANGED minimal pair used to estimate the shuffled-surface null in Step-5 (a unit is admitted only if its pooled surface-response is NOT above this null). The concept is held fixed; only the surface realization changes.
    - FIRST-LETTER concept 'starts-with-<X>': a pair = two DISTINCT single-token, slot-eligible words that BOTH start with the target letter X, placed in the SAME carrier template. Concept ('starts-with-X') is constant; surface (the word + its token id) changes. Meaning is NOT preserved between the two words (they are different words) -- what is preserved is the CONCEPT, so 'genuinely meaning-preserving' for this concept means 'genuinely concept-constant + grammatical/natural'. The deterministic structural check (both words begin with X, differ, single-token, slot-eligible, char-span correct) is AUTHORITATIVE; any LLM judge is a secondary naturalness audit and never drops a structurally-valid pair.
    - TOXICITY concept 'toxic': a pair = a toxic source comment and a TOXIC paraphrase of it (toxicity held constant, wording reworded). Both must remain toxic and meaning-equivalent; surface must genuinely differ.

  SIZE: >=1,500 surface pairs PER CONCEPT after enlargement (from 590 first-letter and 546 toxicity). The set must INCLUDE all iter-1 originals verbatim (same pair_ids, same field values) plus newly-generated pairs with fresh non-colliding pair_ids.

  INDEPENDENCE / NON-CIRCULARITY: every new toxicity pair must be accepted by a judge from a DIFFERENT model family than its generator; a stratified sample of BOTH concepts (originals + new) must be re-judged by a family different from both the generator AND the original iter-1 judge of that set (toxicity: gpt-4o-mini generated AND judged -> re-judge with anthropic/claude-haiku-4.5; first-letter: judged by google/gemini-3.1-flash-lite -> re-judge with a non-Gemini family, anthropic/claude-haiku-4.5). Report cross-judge agreement (raw + Cohen's kappa) and the genuinely-meaning-preserving pass rate per concept, plus the fraction of the 546 toxicity originals the independent judge confirms.

  GATES (reuse iter-1 values exactly): toxicity double-gate = token Jaccard <= 0.6 AND normalized char-change >= 0.25 (so surface genuinely differs), THEN judge for toxicity-constant + meaning-preserved + fluent. First-letter = deterministic structural validity.

  SCHEMA: identical to iter-1 (flattened metadata_* keys; pairs link by metadata_pair_id + metadata_role in {var_a,var_b} for first-letter or one-row-per-pair input/metadata_text_paired for toxicity; doc-level folds: first-letter folds by target_word 1-5, toxicity train/val/test by source with no cross-fold leakage). Real, pinned source corpora only (s-nlp/paradetox, google/civil_comments for toxicity; Gemma tokenizer vocab for first-letter words). No GPU, no SAE, no model activations. Hard $10 OpenRouter cap.

  REPORTED OUTPUTS: per-concept surface-response null distribution SIZE (total pairs + per-stratum: per-letter for first-letter, per-origin and optionally per-sub-attribute for toxicity), cross-judge agreement/kappa, independent-judge pass rate, originals-confirmation rate, generation cost.
dataset_search_plan: |-
  This is an ENLARGEMENT + INDEPENDENT-RE-JUDGE build, not a search. Source corpora and protocols are already pinned; the executor reuses them. Inputs are read directly from the iter-1 workspace (the temp/build/ helper scripts may be absent, but the surface rows are guaranteed present in the iter-1 full_data_out.json files).

  === PINNED INPUT PATHS (read these directly) ===
  - First-letter testbed: /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json  (dataset groups per letter; surface_flip rows have metadata_pair_type='surface_flip', metadata_role in {var_a,var_b}). Also read its preview_data_out.json metadata.llm_judge block (confirms judge model = google/gemini-3.1-flash-lite, secondary) and metadata.generation_config (carriers t_verbose/t_colon/t_mention_word, get_alpha_tokens recipe, tokenizer unsloth/gemma-2-2b vocab 256000, fold_rule 'minimal pairs by target_word').
  - Toxicity family: /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_3/full_data_out.json  (groups 'paradetox' and 'civil_comments'; surface_pair rows have metadata_record_type='surface_pair'). Also read data_summary.json -> surface_generation block (gen_model=judge_model=openai/gpt-4o-mini [the circularity], jaccard_max=0.6, char_change_min=0.25, 800 sources -> 546 accepted, judge_pass_rate 0.7063).
  - Dossier (dependency art_I2MrezW41iQo): /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_research_2/research_out.json  -> WP4 (minimal-pair generation prompt + independent LLM-judge rubric {content_flipped/surface_preserved/fluent/confidence/justification}; verified June-2026 OpenRouter prices: generator gemini-3.1-flash-lite $0.25/$1.50 or deepseek-v4-flash $0.09/$0.18; judge claude-haiku-4.5 $1.00/$5.00) and WP5 (get_alpha_tokens: convert_tokens_to_string -> strip ONE leading space -> require all chars in a-zA-Z; word-initial '_'/space-piece + single-token; carrier templates).

  === STEP 0 — INGEST & PARSE ORIGINALS (verbatim, no mutation) ===
  1. Load the two iter-1 full_data_out.json files. Extract ALL surface rows verbatim: first-letter -> 590 surface_flip pairs = 1,180 rows (L=170,O=105,T=95,I=110,D=110 pairs); toxicity -> 546 surface_pair rows. Record the exact per-concept original counts and per-stratum breakdown for the final null-size report.
  2. Capture the EXACT field set of each row type (so new rows are byte-compatible). First-letter surface_flip row keys: input, output, metadata_dataset, metadata_letter, metadata_pair_id, metadata_pair_type, metadata_role, metadata_sub_context, metadata_target_word, metadata_counterpart_word, metadata_template_id, metadata_label_starts_with_target, metadata_is_single_token, metadata_is_slot_eligible, metadata_first_letter, metadata_fold, metadata_word_char_span, metadata_judge_pass. Toxicity surface_pair row keys: input, output, metadata_id, metadata_fold, metadata_record_type, metadata_source, metadata_origin_source, metadata_toxicity_label, metadata_text_on(null), metadata_text_off(null), metadata_text_paired, metadata_pair_id, metadata_source_sentence_id, metadata_is_content_pair(false), metadata_is_surface_pair(true), metadata_subcontext_labels(6 nulls), metadata_subcontext_floats(7 nulls), metadata_subcontext_threshold(null), metadata_judge_pass, metadata_gen_model, metadata_surface_metrics{jaccard,char_change,reason}.
  3. To keep the output a clean drop-in, this artifact emits the SURFACE-PAIR superset only (it does NOT re-emit or mutate the frozen content_flip/content_pair/classification/corpus rows, which remain canonical at their iter-1 paths). State this explicitly in the README and reference the iter-1 paths the experiment merges by pair_id/record_type.

  === STEP 1 — ENLARGE FIRST-LETTER SURFACE PAIRS (590 -> >=1,500; deterministic, ~$0) ===
  1. Reuse the iter-1 word pools. For each target letter in {L,O,T,I,D}, gather single-token, slot-eligible words beginning with that letter using the get_alpha_tokens recipe (WP5) over the unsloth/gemma-2-2b tokenizer (vocab 256000): for each vocab token, tokenizer.convert_tokens_to_string([tok]) -> strip one leading space -> require word-initial (the '_'/space-piece marker, i.e. the token forms a word start) AND all chars a-zA-Z; keep words whose first alpha char (case-insensitive) == target letter. Verify each candidate word is single-token (re-encodes to one id) and slot-eligible. This yields tens-to-hundreds of words per letter -> more than enough (n words -> n*(n-1)/2 unordered same-letter pairs).
  2. Form NEW surface_flip pairs = ordered (var_a, var_b) of two DISTINCT same-letter words, placed in EACH of the 3 carriers (t_verbose '{word} has the first letter:', t_colon '{word}:', t_mention_word 'Here is an example word: {word}.'). Reproduce the carrier strings exactly from the iter-1 rows. Exclude case-only variants (e.g. 'list'/'List') as the iter-1 judge rejects them as the same word. Avoid regenerating any (word_a,word_b,carrier) combination already present in the 590 originals (dedupe on the normalized triple).
  3. Target distribution: bring each letter to >=300 surface pairs (5 letters x 300 = 1,500), balanced across the 3 carriers, so the per-letter null is well-powered; cap per (letter,carrier) to keep balance. Assign metadata_fold by target_word using the SAME 5-fold rule as iter-1 (a word's fold is deterministic from its hash/assignment; keep both members of a pair in one fold; never split a pair across folds). Set metadata_pair_type='surface_flip', metadata_role var_a/var_b, metadata_sub_context='wordA|wordB', metadata_label_starts_with_target=1 for both, metadata_first_letter=lowercase target, metadata_is_single_token/slot_eligible=true, metadata_word_char_span = char offsets of the slotted word in input, output = uppercase target letter. Assign fresh pair_ids that do not collide with iter-1 (e.g. '<L>_s2_NNNN').
  4. Run the DETERMINISTIC structural validator on every new pair (AUTHORITATIVE): both words begin with target letter, differ, single-token, slot-eligible, input[word_char_span]==target_word. Drop any violation (should be zero by construction); report violations==0 like iter-1.

  === STEP 2 — ENLARGE TOXICITY SURFACE PAIRS (546 -> >=1,500; OpenRouter, gated) ===
  1. Assemble fresh toxic SOURCE sentences NOT already used (dedupe against iter-1 metadata_source_sentence_id and against the originals' input/text_paired). Draw from: (a) s-nlp/paradetox en_toxic_comment column (download via aii-hf-datasets); (b) google/civil_comments rows with toxicity>=0.5 (stream-filter + subsample to stay <300MB and CC0). Stratify civil_comments sources across sub-attributes (obscene/threat/insult/identity_attack/sexual_explicit each >=0.5) so the enlarged set spans the same sub-contexts; tag the source's sub-attribute floats.
  2. Generate ONE toxic->toxic paraphrase per source via OpenRouter using the WP4 surface-flip prompt (instruction: reword the surface form, keep the toxicity level and target the same, do not detoxify, do not add new insults). Generator = openai/gpt-4o-mini (homogeneous with the 546 originals; ~$0.15/$0.60). If gpt-4o-mini refuses too often (iter-1 refusal_rate was only 0.015) or quality drops, fall back to google/gemini-3.1-flash-lite or deepseek-v4-flash. Generate enough sources to clear the target after gating: at iter-1's ~68% acceptance, ~1,400 new generations yield ~950 accepted -> with the 546 originals exceeds 1,500; budget up to ~1,800-2,000 sources for safety.
  3. Apply the iter-1 DOUBLE-GATE on (source, paraphrase): token Jaccard <= 0.6 (surface differs enough) AND normalized char-change >= 0.25; record metadata_surface_metrics{jaccard,char_change,reason}. Drop pairs failing the gate.
  4. Judge each gate-passing NEW pair with anthropic/claude-haiku-4.5 (INDEPENDENT family from the gpt-4o-mini generator -> no circularity). Rubric (adapt WP4): return {toxicity_constant (still toxic, same severity/target), meaning_preserved (semantically equivalent), surface_changed, fluent, confidence, justification}; ACCEPT iff toxicity_constant AND meaning_preserved AND surface_changed AND fluent. Discard fails. This makes every NEW pair born with an independent judge. Set metadata_source='generated_paraphrase', metadata_origin_source in {paradetox,civil_comments}, metadata_toxicity_label=1, metadata_gen_model=generator id, output='toxic', input=source, metadata_text_paired=paraphrase, fresh metadata_pair_id 'sp2_<hash>' and metadata_id 'tox_sp_NNNNNN' continuing the counter, metadata_fold inherited from the source's classification fold (no cross-fold leakage). OPTIONAL ENHANCEMENT (schema-compatible): for civil_comments-origin new pairs, populate metadata_subcontext_floats with the source's real sub-attribute floats (paradetox has none -> keep null) so the experiment can build per-sub-context surface nulls; keep metadata_subcontext_labels null unless thresholded.

  === STEP 3 — INDEPENDENT RE-JUDGE + CROSS-JUDGE AGREEMENT (resolves the circularity critique) ===
  1. Build a STRATIFIED re-judge sample per concept mixing iter-1 ORIGINALS and NEW pairs: toxicity stratified by origin (paradetox/civil_comments) x surface_metrics bins (low/high jaccard, low/high char_change); first-letter stratified by letter x carrier. Target ~300-400 sampled pairs per concept (~700 total).
  2. PRIMARY independent judge = anthropic/claude-haiku-4.5 for BOTH concepts (family != gpt-4o-mini [toxicity gen+judge] and != gemini-3.1-flash-lite [first-letter judge]). For toxicity it applies the Step-2 rubric; for first-letter it judges concept-constancy (both words start with target letter) + grammaticality/naturalness (deterministic remains authoritative -> a judge 'fail' on structurally-valid first-letter pairs is logged as a judge false-negative, NOT a drop, exactly like iter-1).
  3. To obtain a genuine 2-judge agreement that is independent of the generator, run a SECOND-family judge on the SAME sample: google/gemini-3.1-flash-lite for the toxicity sample (independent of both gpt-4o-mini and Anthropic) and deepseek-v4-flash (or gemini) for the first-letter sample (non-Gemini-original concern is satisfied by claude as primary). Report: (a) per-concept genuinely-meaning-preserving pass rate (fraction the independent judge passes); (b) cross-judge agreement = raw agreement + Cohen's kappa between the two independent judges on the sample; (c) the key circularity number = fraction of the 546 toxicity ORIGINALS (all gpt-4o-mini-accepted) that claude-haiku-4.5 CONFIRMS; (d) for first-letter, agreement of claude vs the stored gemini secondary labels on originals that carry them.
  4. Annotate every re-judged row with metadata_independent_judge_model, metadata_independent_judge_pass, metadata_independent_judge_reason. Add metadata_enlargement_batch in {'iter1_original','iter2_new'} to EVERY surface row. To keep exp_sel_data_out key-uniformity within each concept group, add these three independent-judge keys (null where a row was not in the re-judge sample) to ALL surface rows of that concept.

  === STEP 4 — ASSEMBLE THE SUPERSET (exp_sel_data_out schema) ===
  1. Output structure mirrors iter-1: a top-level object with metadata + a 'datasets' list of {dataset, examples[]} groups. FIRST-LETTER groups: one per letter (first_letter_spelling_L ... _D) holding that letter's surface_flip rows (originals verbatim + new). TOXICITY groups: 'paradetox' and 'civil_comments' holding surface_pair rows (originals verbatim + new), folded by metadata_origin_source as in iter-1.
  2. Originals MUST be byte-identical to iter-1 (same pair_ids, fields, values) except for the two additive uniformity keys (metadata_enlargement_batch='iter1_original'; the independent-judge keys, populated only if that original was in the re-judge sample, else null). New rows use the field templates captured in Step 0.
  3. Verify it is a true SUPERSET: every iter-1 surface pair_id is present; total surface pairs per concept >= max(1,500, original). Re-run the deterministic first-letter validator and the toxicity double-gate over the whole assembled set; assert zero structural violations and that every accepted toxicity pair has metadata_surface_metrics within gate bounds.

  === STEP 5 — REPORT SURFACE-RESPONSE NULL DISTRIBUTION SIZES ===
  In a data_summary.json (mirroring iter-1) report, per concept: total surface pairs available for the shuffled-surface null, broken down by stratum (first-letter: per letter x carrier; toxicity: per origin and, where populated, per sub-attribute), plus originals-vs-new counts, generation/judge stats (n_sources, n_gate_pass, n_accepted, acceptance rate, refusals, cost_usd, openrouter_calls), cross-judge agreement/kappa, independent-judge pass rate, originals-confirmation rate, and the exact gate constants used (jaccard_max=0.6, char_change_min=0.25). This is the 'per-concept surface-response null distribution size' deliverable the objective asks for.

  === STEP 6 — VALIDATE & VARIANTS ===
  1. Validate the assembled data_out.json against the exp_sel_data_out schema using the aii-json skill (each row must have non-empty input + output + metadata_fold; consistent metadata_* keys within a group).
  2. Emit full_data_out.json (canonical), mini_data_out.json, preview_data_out.json via aii-json. Run the aii-file-size-limit check (the surface-only superset is small -- ~3,000 first-letter rows + ~1,500 toxicity rows -- well under 300MB; split only if needed).
  3. Write a README documenting: the circularity fixed, model families used per step, the superset guarantee, the merge contract with the frozen iter-1 content/classification rows, and the null-size table.

  === COST CONTROL (hard $10 cap) ===
  Track cumulative OpenRouter spend after every call; STOP at $10. Estimate: toxicity gen ~2,000 x ~$0.0002 = ~$0.4 (gpt-4o-mini); toxicity accept-judge ~1,600 gate-passers x ~$0.0011 = ~$1.8 (claude-haiku); re-judge+second-judge samples ~1,400 calls x ~$0.0006-0.0011 = ~$1.0. Total ~$3-4, ample headroom. If approaching the cap: reduce the toxicity target toward 1,500 exactly, batch multiple pairs per judge call, switch generator to deepseek-v4-flash ($0.09/$0.18), or shrink the re-judge sample (keep >=200/concept for a stable kappa).

  === FAILURE / FALLBACK SCENARIOS ===
  - Toxicity acceptance < expected: generate more sources (cap ~2,500) or relax nothing on the gate (keep jaccard/char fixed for comparability); if still short, report the achieved count honestly and the null-size as-is (>=1,000 still strengthens the control). NEVER lower the double-gate to hit a number.
  - Independent judge refuses toxic content: frame the judge call as a CLASSIFICATION/validation task (not generation); if claude-haiku refuses, fall back to gemini-3.1-flash-lite or deepseek-v4-flash as the independent family (still != gpt-4o-mini). Record refusals.
  - First-letter word pool too small for a letter to reach 300 (unlikely): lift the per-(letter,carrier) cap or add a 4th carrier only if it matches an iter-1 template; if a letter genuinely caps out, redistribute the target to other letters and report the achieved per-letter sizes.
  - Low cross-judge agreement (kappa low): this is a REPORTABLE finding (the iter-1 same-model gate was lenient), not a failure -- keep all pairs in the superset with the independent-judge label recorded so the experiment can filter to the 'both-judges-pass' high-confidence subset; report both the full and high-confidence null sizes.
  - civil_comments download >300MB: stream + filter to toxicity>=0.5 and subsample before materializing; never load the full 414.95MB file.

  NOTE on the direction's claim: the direction states the first-letter set 'used gemini-3.1-flash-lite' as judge -- CONFIRMED (metadata.llm_judge.model='google/gemini-3.1-flash-lite', secondary role). The first-letter surface pairs are mechanically/deterministically constructed (not LLM-paraphrased), so enlargement there is deterministic and the independent re-judge is a naturalness/concept-constancy audit, not an acceptance gate.
target_num_datasets: 2
</artifact_plan>

<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
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
out_dependency_files:
  file_list:
  - research_out.json

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>

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
TODO 2. Read skill files for your data sources (see <available_data_sources>) and domain handbook if applicable (see <available_domain_handbooks>). Based on plan and context, decide which source(s) to use. Include everything specified in the artifact plan, but you may also collect additional relevant data beyond what's listed. Run 16 diverse searches across chosen source(s) — BROAD, GENERAL terms, not very specific. Parallelize where supported.
TODO 3. Identify the 8 most promising datasets. IMPORTANT: Only consider datasets under 300MB. Preview/inspect sample rows for each candidate. Parallelize previews.
TODO 4. Research each candidate BEFORE choosing which to download. For each, search the web (aii-web-tools skill): dataset name, papers citing it, original source/task, popularity. Red flags: no search results, no papers, anonymized features (F1, F2...), <100 downloads, no documentation. Green flags: papers using it, clear documentation, meaningful features, established benchmark. Also consider: will features/structure allow meaningful evaluation of the planned method?
TODO 5. Decide which to KEEP vs DISCARD. Look for: clear structure, relevant fields, quality examples matching requirements, confirmed provenance. Determine which 4 datasets have the most suitable data. Download and save to `temp/datasets/`. Parallelize downloads.
</todos>
```

### [2] HUMAN-USER prompt · 2026-06-17 15:41:06 UTC

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

### [3] SKILL-INPUT — aii-python · 2026-06-17 15:41:20 UTC

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

### [4] SKILL-INPUT — aii-long-running-tasks · 2026-06-17 15:41:20 UTC

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

### [5] SKILL-INPUT — aii-json · 2026-06-17 15:41:20 UTC

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

### [6] SKILL-INPUT — aii-file-size-limit · 2026-06-17 15:41:20 UTC

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

### [7] SKILL-INPUT — aii-use-hardware · 2026-06-17 15:41:20 UTC

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

### [8] SKILL-INPUT — aii-parallel-computing · 2026-06-17 15:41:20 UTC

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

### [9] SKILL-INPUT — aii-hf-datasets · 2026-06-17 15:41:32 UTC

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

### [10] SKILL-INPUT — aii-openrouter-llms · 2026-06-17 15:41:32 UTC

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

### [11] SYSTEM-USER prompt · 2026-06-17 16:04:55 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_dataset_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/results/out.json`
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
id: gen_plan_dataset_1_idx5
type: dataset
title: >-
  Enlarge & Independently Re-Judge the Surface-Invariance Pair Sets (First-Letter + Toxicity) for the Step-5 Admission AND-Gate
summary: >-
  Build a drop-in SUPERSET of the two iter-1 surface-flip pair sets that the next iteration's Step-5 admission AND-gate consumes.
  (1) Enlarge the FIRST-LETTER surface_flip set from 590 -> >=1,500 concept-constant pairs (two distinct single-token, slot-eligible
  words sharing the same first letter in the 3 carrier templates; deterministic check is AUTHORITATIVE). (2) Enlarge the TOXICITY
  surface_pair set from 546 -> >=1,500 toxic->toxic paraphrases (toxicity held constant, wording changed) generated via OpenRouter
  under the existing token-Jaccard<=0.6 + char-change>=0.25 double-gate. (3) Break the same-model generate-and-judge circularity
  by judging/re-judging a stratified sample with anthropic/claude-haiku-4.5 (a family different from both gpt-4o-mini, which
  generated AND judged toxicity, and gemini-3.1-flash-lite, which judged first-letter), report cross-judge agreement (Cohen's
  kappa) + the genuinely-meaning-preserving pass rate, and the confirmation rate of the 546 originals. Emit in the identical
  exp_sel_data_out flattened-metadata schema (pair_id/role linkage, doc-level folds), preserving the iter-1 originals VERBATIM,
  then report per-concept surface-response null distribution sizes. Schema-validate with aii-json; emit full/mini/preview.
  Hard $10 OpenRouter cap (est. ~$3-4); no GPU.
runpod_compute_profile: cpu_heavy
ideal_dataset_criteria: |-
  TWO enlarged surface-flip pair sets, each a superset of the frozen iter-1 originals, emitted in the SAME exp_sel_data_out flattened-metadata schema so the next iteration's admission filter consumes them identically.

  WHAT A SURFACE-FLIP PAIR IS (the load-bearing semantics): a CONCEPT-CONSTANT, SURFACE-CHANGED minimal pair used to estimate the shuffled-surface null in Step-5 (a unit is admitted only if its pooled surface-response is NOT above this null). The concept is held fixed; only the surface realization changes.
    - FIRST-LETTER concept 'starts-with-<X>': a pair = two DISTINCT single-token, slot-eligible words that BOTH start with the target letter X, placed in the SAME carrier template. Concept ('starts-with-X') is constant; surface (the word + its token id) changes. Meaning is NOT preserved between the two words (they are different words) -- what is preserved is the CONCEPT, so 'genuinely meaning-preserving' for this concept means 'genuinely concept-constant + grammatical/natural'. The deterministic structural check (both words begin with X, differ, single-token, slot-eligible, char-span correct) is AUTHORITATIVE; any LLM judge is a secondary naturalness audit and never drops a structurally-valid pair.
    - TOXICITY concept 'toxic': a pair = a toxic source comment and a TOXIC paraphrase of it (toxicity held constant, wording reworded). Both must remain toxic and meaning-equivalent; surface must genuinely differ.

  SIZE: >=1,500 surface pairs PER CONCEPT after enlargement (from 590 first-letter and 546 toxicity). The set must INCLUDE all iter-1 originals verbatim (same pair_ids, same field values) plus newly-generated pairs with fresh non-colliding pair_ids.

  INDEPENDENCE / NON-CIRCULARITY: every new toxicity pair must be accepted by a judge from a DIFFERENT model family than its generator; a stratified sample of BOTH concepts (originals + new) must be re-judged by a family different from both the generator AND the original iter-1 judge of that set (toxicity: gpt-4o-mini generated AND judged -> re-judge with anthropic/claude-haiku-4.5; first-letter: judged by google/gemini-3.1-flash-lite -> re-judge with a non-Gemini family, anthropic/claude-haiku-4.5). Report cross-judge agreement (raw + Cohen's kappa) and the genuinely-meaning-preserving pass rate per concept, plus the fraction of the 546 toxicity originals the independent judge confirms.

  GATES (reuse iter-1 values exactly): toxicity double-gate = token Jaccard <= 0.6 AND normalized char-change >= 0.25 (so surface genuinely differs), THEN judge for toxicity-constant + meaning-preserved + fluent. First-letter = deterministic structural validity.

  SCHEMA: identical to iter-1 (flattened metadata_* keys; pairs link by metadata_pair_id + metadata_role in {var_a,var_b} for first-letter or one-row-per-pair input/metadata_text_paired for toxicity; doc-level folds: first-letter folds by target_word 1-5, toxicity train/val/test by source with no cross-fold leakage). Real, pinned source corpora only (s-nlp/paradetox, google/civil_comments for toxicity; Gemma tokenizer vocab for first-letter words). No GPU, no SAE, no model activations. Hard $10 OpenRouter cap.

  REPORTED OUTPUTS: per-concept surface-response null distribution SIZE (total pairs + per-stratum: per-letter for first-letter, per-origin and optionally per-sub-attribute for toxicity), cross-judge agreement/kappa, independent-judge pass rate, originals-confirmation rate, generation cost.
dataset_search_plan: |-
  This is an ENLARGEMENT + INDEPENDENT-RE-JUDGE build, not a search. Source corpora and protocols are already pinned; the executor reuses them. Inputs are read directly from the iter-1 workspace (the temp/build/ helper scripts may be absent, but the surface rows are guaranteed present in the iter-1 full_data_out.json files).

  === PINNED INPUT PATHS (read these directly) ===
  - First-letter testbed: /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json  (dataset groups per letter; surface_flip rows have metadata_pair_type='surface_flip', metadata_role in {var_a,var_b}). Also read its preview_data_out.json metadata.llm_judge block (confirms judge model = google/gemini-3.1-flash-lite, secondary) and metadata.generation_config (carriers t_verbose/t_colon/t_mention_word, get_alpha_tokens recipe, tokenizer unsloth/gemma-2-2b vocab 256000, fold_rule 'minimal pairs by target_word').
  - Toxicity family: /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_3/full_data_out.json  (groups 'paradetox' and 'civil_comments'; surface_pair rows have metadata_record_type='surface_pair'). Also read data_summary.json -> surface_generation block (gen_model=judge_model=openai/gpt-4o-mini [the circularity], jaccard_max=0.6, char_change_min=0.25, 800 sources -> 546 accepted, judge_pass_rate 0.7063).
  - Dossier (dependency art_I2MrezW41iQo): /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_research_2/research_out.json  -> WP4 (minimal-pair generation prompt + independent LLM-judge rubric {content_flipped/surface_preserved/fluent/confidence/justification}; verified June-2026 OpenRouter prices: generator gemini-3.1-flash-lite $0.25/$1.50 or deepseek-v4-flash $0.09/$0.18; judge claude-haiku-4.5 $1.00/$5.00) and WP5 (get_alpha_tokens: convert_tokens_to_string -> strip ONE leading space -> require all chars in a-zA-Z; word-initial '_'/space-piece + single-token; carrier templates).

  === STEP 0 — INGEST & PARSE ORIGINALS (verbatim, no mutation) ===
  1. Load the two iter-1 full_data_out.json files. Extract ALL surface rows verbatim: first-letter -> 590 surface_flip pairs = 1,180 rows (L=170,O=105,T=95,I=110,D=110 pairs); toxicity -> 546 surface_pair rows. Record the exact per-concept original counts and per-stratum breakdown for the final null-size report.
  2. Capture the EXACT field set of each row type (so new rows are byte-compatible). First-letter surface_flip row keys: input, output, metadata_dataset, metadata_letter, metadata_pair_id, metadata_pair_type, metadata_role, metadata_sub_context, metadata_target_word, metadata_counterpart_word, metadata_template_id, metadata_label_starts_with_target, metadata_is_single_token, metadata_is_slot_eligible, metadata_first_letter, metadata_fold, metadata_word_char_span, metadata_judge_pass. Toxicity surface_pair row keys: input, output, metadata_id, metadata_fold, metadata_record_type, metadata_source, metadata_origin_source, metadata_toxicity_label, metadata_text_on(null), metadata_text_off(null), metadata_text_paired, metadata_pair_id, metadata_source_sentence_id, metadata_is_content_pair(false), metadata_is_surface_pair(true), metadata_subcontext_labels(6 nulls), metadata_subcontext_floats(7 nulls), metadata_subcontext_threshold(null), metadata_judge_pass, metadata_gen_model, metadata_surface_metrics{jaccard,char_change,reason}.
  3. To keep the output a clean drop-in, this artifact emits the SURFACE-PAIR superset only (it does NOT re-emit or mutate the frozen content_flip/content_pair/classification/corpus rows, which remain canonical at their iter-1 paths). State this explicitly in the README and reference the iter-1 paths the experiment merges by pair_id/record_type.

  === STEP 1 — ENLARGE FIRST-LETTER SURFACE PAIRS (590 -> >=1,500; deterministic, ~$0) ===
  1. Reuse the iter-1 word pools. For each target letter in {L,O,T,I,D}, gather single-token, slot-eligible words beginning with that letter using the get_alpha_tokens recipe (WP5) over the unsloth/gemma-2-2b tokenizer (vocab 256000): for each vocab token, tokenizer.convert_tokens_to_string([tok]) -> strip one leading space -> require word-initial (the '_'/space-piece marker, i.e. the token forms a word start) AND all chars a-zA-Z; keep words whose first alpha char (case-insensitive) == target letter. Verify each candidate word is single-token (re-encodes to one id) and slot-eligible. This yields tens-to-hundreds of words per letter -> more than enough (n words -> n*(n-1)/2 unordered same-letter pairs).
  2. Form NEW surface_flip pairs = ordered (var_a, var_b) of two DISTINCT same-letter words, placed in EACH of the 3 carriers (t_verbose '{word} has the first letter:', t_colon '{word}:', t_mention_word 'Here is an example word: {word}.'). Reproduce the carrier strings exactly from the iter-1 rows. Exclude case-only variants (e.g. 'list'/'List') as the iter-1 judge rejects them as the same word. Avoid regenerating any (word_a,word_b,carrier) combination already present in the 590 originals (dedupe on the normalized triple).
  3. Target distribution: bring each letter to >=300 surface pairs (5 letters x 300 = 1,500), balanced across the 3 carriers, so the per-letter null is well-powered; cap per (letter,carrier) to keep balance. Assign metadata_fold by target_word using the SAME 5-fold rule as iter-1 (a word's fold is deterministic from its hash/assignment; keep both members of a pair in one fold; never split a pair across folds). Set metadata_pair_type='surface_flip', metadata_role var_a/var_b, metadata_sub_context='wordA|wordB', metadata_label_starts_with_target=1 for both, metadata_first_letter=lowercase target, metadata_is_single_token/slot_eligible=true, metadata_word_char_span = char offsets of the slotted word in input, output = uppercase target letter. Assign fresh pair_ids that do not collide with iter-1 (e.g. '<L>_s2_NNNN').
  4. Run the DETERMINISTIC structural validator on every new pair (AUTHORITATIVE): both words begin with target letter, differ, single-token, slot-eligible, input[word_char_span]==target_word. Drop any violation (should be zero by construction); report violations==0 like iter-1.

  === STEP 2 — ENLARGE TOXICITY SURFACE PAIRS (546 -> >=1,500; OpenRouter, gated) ===
  1. Assemble fresh toxic SOURCE sentences NOT already used (dedupe against iter-1 metadata_source_sentence_id and against the originals' input/text_paired). Draw from: (a) s-nlp/paradetox en_toxic_comment column (download via aii-hf-datasets); (b) google/civil_comments rows with toxicity>=0.5 (stream-filter + subsample to stay <300MB and CC0). Stratify civil_comments sources across sub-attributes (obscene/threat/insult/identity_attack/sexual_explicit each >=0.5) so the enlarged set spans the same sub-contexts; tag the source's sub-attribute floats.
  2. Generate ONE toxic->toxic paraphrase per source via OpenRouter using the WP4 surface-flip prompt (instruction: reword the surface form, keep the toxicity level and target the same, do not detoxify, do not add new insults). Generator = openai/gpt-4o-mini (homogeneous with the 546 originals; ~$0.15/$0.60). If gpt-4o-mini refuses too often (iter-1 refusal_rate was only 0.015) or quality drops, fall back to google/gemini-3.1-flash-lite or deepseek-v4-flash. Generate enough sources to clear the target after gating: at iter-1's ~68% acceptance, ~1,400 new generations yield ~950 accepted -> with the 546 originals exceeds 1,500; budget up to ~1,800-2,000 sources for safety.
  3. Apply the iter-1 DOUBLE-GATE on (source, paraphrase): token Jaccard <= 0.6 (surface differs enough) AND normalized char-change >= 0.25; record metadata_surface_metrics{jaccard,char_change,reason}. Drop pairs failing the gate.
  4. Judge each gate-passing NEW pair with anthropic/claude-haiku-4.5 (INDEPENDENT family from the gpt-4o-mini generator -> no circularity). Rubric (adapt WP4): return {toxicity_constant (still toxic, same severity/target), meaning_preserved (semantically equivalent), surface_changed, fluent, confidence, justification}; ACCEPT iff toxicity_constant AND meaning_preserved AND surface_changed AND fluent. Discard fails. This makes every NEW pair born with an independent judge. Set metadata_source='generated_paraphrase', metadata_origin_source in {paradetox,civil_comments}, metadata_toxicity_label=1, metadata_gen_model=generator id, output='toxic', input=source, metadata_text_paired=paraphrase, fresh metadata_pair_id 'sp2_<hash>' and metadata_id 'tox_sp_NNNNNN' continuing the counter, metadata_fold inherited from the source's classification fold (no cross-fold leakage). OPTIONAL ENHANCEMENT (schema-compatible): for civil_comments-origin new pairs, populate metadata_subcontext_floats with the source's real sub-attribute floats (paradetox has none -> keep null) so the experiment can build per-sub-context surface nulls; keep metadata_subcontext_labels null unless thresholded.

  === STEP 3 — INDEPENDENT RE-JUDGE + CROSS-JUDGE AGREEMENT (resolves the circularity critique) ===
  1. Build a STRATIFIED re-judge sample per concept mixing iter-1 ORIGINALS and NEW pairs: toxicity stratified by origin (paradetox/civil_comments) x surface_metrics bins (low/high jaccard, low/high char_change); first-letter stratified by letter x carrier. Target ~300-400 sampled pairs per concept (~700 total).
  2. PRIMARY independent judge = anthropic/claude-haiku-4.5 for BOTH concepts (family != gpt-4o-mini [toxicity gen+judge] and != gemini-3.1-flash-lite [first-letter judge]). For toxicity it applies the Step-2 rubric; for first-letter it judges concept-constancy (both words start with target letter) + grammaticality/naturalness (deterministic remains authoritative -> a judge 'fail' on structurally-valid first-letter pairs is logged as a judge false-negative, NOT a drop, exactly like iter-1).
  3. To obtain a genuine 2-judge agreement that is independent of the generator, run a SECOND-family judge on the SAME sample: google/gemini-3.1-flash-lite for the toxicity sample (independent of both gpt-4o-mini and Anthropic) and deepseek-v4-flash (or gemini) for the first-letter sample (non-Gemini-original concern is satisfied by claude as primary). Report: (a) per-concept genuinely-meaning-preserving pass rate (fraction the independent judge passes); (b) cross-judge agreement = raw agreement + Cohen's kappa between the two independent judges on the sample; (c) the key circularity number = fraction of the 546 toxicity ORIGINALS (all gpt-4o-mini-accepted) that claude-haiku-4.5 CONFIRMS; (d) for first-letter, agreement of claude vs the stored gemini secondary labels on originals that carry them.
  4. Annotate every re-judged row with metadata_independent_judge_model, metadata_independent_judge_pass, metadata_independent_judge_reason. Add metadata_enlargement_batch in {'iter1_original','iter2_new'} to EVERY surface row. To keep exp_sel_data_out key-uniformity within each concept group, add these three independent-judge keys (null where a row was not in the re-judge sample) to ALL surface rows of that concept.

  === STEP 4 — ASSEMBLE THE SUPERSET (exp_sel_data_out schema) ===
  1. Output structure mirrors iter-1: a top-level object with metadata + a 'datasets' list of {dataset, examples[]} groups. FIRST-LETTER groups: one per letter (first_letter_spelling_L ... _D) holding that letter's surface_flip rows (originals verbatim + new). TOXICITY groups: 'paradetox' and 'civil_comments' holding surface_pair rows (originals verbatim + new), folded by metadata_origin_source as in iter-1.
  2. Originals MUST be byte-identical to iter-1 (same pair_ids, fields, values) except for the two additive uniformity keys (metadata_enlargement_batch='iter1_original'; the independent-judge keys, populated only if that original was in the re-judge sample, else null). New rows use the field templates captured in Step 0.
  3. Verify it is a true SUPERSET: every iter-1 surface pair_id is present; total surface pairs per concept >= max(1,500, original). Re-run the deterministic first-letter validator and the toxicity double-gate over the whole assembled set; assert zero structural violations and that every accepted toxicity pair has metadata_surface_metrics within gate bounds.

  === STEP 5 — REPORT SURFACE-RESPONSE NULL DISTRIBUTION SIZES ===
  In a data_summary.json (mirroring iter-1) report, per concept: total surface pairs available for the shuffled-surface null, broken down by stratum (first-letter: per letter x carrier; toxicity: per origin and, where populated, per sub-attribute), plus originals-vs-new counts, generation/judge stats (n_sources, n_gate_pass, n_accepted, acceptance rate, refusals, cost_usd, openrouter_calls), cross-judge agreement/kappa, independent-judge pass rate, originals-confirmation rate, and the exact gate constants used (jaccard_max=0.6, char_change_min=0.25). This is the 'per-concept surface-response null distribution size' deliverable the objective asks for.

  === STEP 6 — VALIDATE & VARIANTS ===
  1. Validate the assembled data_out.json against the exp_sel_data_out schema using the aii-json skill (each row must have non-empty input + output + metadata_fold; consistent metadata_* keys within a group).
  2. Emit full_data_out.json (canonical), mini_data_out.json, preview_data_out.json via aii-json. Run the aii-file-size-limit check (the surface-only superset is small -- ~3,000 first-letter rows + ~1,500 toxicity rows -- well under 300MB; split only if needed).
  3. Write a README documenting: the circularity fixed, model families used per step, the superset guarantee, the merge contract with the frozen iter-1 content/classification rows, and the null-size table.

  === COST CONTROL (hard $10 cap) ===
  Track cumulative OpenRouter spend after every call; STOP at $10. Estimate: toxicity gen ~2,000 x ~$0.0002 = ~$0.4 (gpt-4o-mini); toxicity accept-judge ~1,600 gate-passers x ~$0.0011 = ~$1.8 (claude-haiku); re-judge+second-judge samples ~1,400 calls x ~$0.0006-0.0011 = ~$1.0. Total ~$3-4, ample headroom. If approaching the cap: reduce the toxicity target toward 1,500 exactly, batch multiple pairs per judge call, switch generator to deepseek-v4-flash ($0.09/$0.18), or shrink the re-judge sample (keep >=200/concept for a stable kappa).

  === FAILURE / FALLBACK SCENARIOS ===
  - Toxicity acceptance < expected: generate more sources (cap ~2,500) or relax nothing on the gate (keep jaccard/char fixed for comparability); if still short, report the achieved count honestly and the null-size as-is (>=1,000 still strengthens the control). NEVER lower the double-gate to hit a number.
  - Independent judge refuses toxic content: frame the judge call as a CLASSIFICATION/validation task (not generation); if claude-haiku refuses, fall back to gemini-3.1-flash-lite or deepseek-v4-flash as the independent family (still != gpt-4o-mini). Record refusals.
  - First-letter word pool too small for a letter to reach 300 (unlikely): lift the per-(letter,carrier) cap or add a 4th carrier only if it matches an iter-1 template; if a letter genuinely caps out, redistribute the target to other letters and report the achieved per-letter sizes.
  - Low cross-judge agreement (kappa low): this is a REPORTABLE finding (the iter-1 same-model gate was lenient), not a failure -- keep all pairs in the superset with the independent-judge label recorded so the experiment can filter to the 'both-judges-pass' high-confidence subset; report both the full and high-confidence null sizes.
  - civil_comments download >300MB: stream + filter to toxicity>=0.5 and subsample before materializing; never load the full 414.95MB file.

  NOTE on the direction's claim: the direction states the first-letter set 'used gemini-3.1-flash-lite' as judge -- CONFIRMED (metadata.llm_judge.model='google/gemini-3.1-flash-lite', secondary role). The first-letter surface pairs are mechanically/deterministically constructed (not LLM-paraphrased), so enlargement there is deterministic and the independent re-judge is a naturalness/concept-constancy audit, not an acceptance gate.
target_num_datasets: 2
</artifact_plan>

<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
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
out_dependency_files:
  file_list:
  - research_out.json

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>

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
TODO 1. For the top 4 datasets, create data.py (uv inline script) that: loads from temp/datasets/, standardizes to exp_sel_data_out.json schema (aii-json skill), extracts all examples per dataset, handles domain requirements, saves to full_data_out.json.

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
TODO 3. Read preview to inspect examples. Choose THE BEST 2 DATASETS based on domain requirements and artifact objective. Be very attentive to meticulously and exhaustively fix any errors in your code.
</todos>
````

### [12] SYSTEM-USER prompt · 2026-06-17 16:14:05 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_dataset_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/results/out.json`
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
id: gen_plan_dataset_1_idx5
type: dataset
title: >-
  Enlarge & Independently Re-Judge the Surface-Invariance Pair Sets (First-Letter + Toxicity) for the Step-5 Admission AND-Gate
summary: >-
  Build a drop-in SUPERSET of the two iter-1 surface-flip pair sets that the next iteration's Step-5 admission AND-gate consumes.
  (1) Enlarge the FIRST-LETTER surface_flip set from 590 -> >=1,500 concept-constant pairs (two distinct single-token, slot-eligible
  words sharing the same first letter in the 3 carrier templates; deterministic check is AUTHORITATIVE). (2) Enlarge the TOXICITY
  surface_pair set from 546 -> >=1,500 toxic->toxic paraphrases (toxicity held constant, wording changed) generated via OpenRouter
  under the existing token-Jaccard<=0.6 + char-change>=0.25 double-gate. (3) Break the same-model generate-and-judge circularity
  by judging/re-judging a stratified sample with anthropic/claude-haiku-4.5 (a family different from both gpt-4o-mini, which
  generated AND judged toxicity, and gemini-3.1-flash-lite, which judged first-letter), report cross-judge agreement (Cohen's
  kappa) + the genuinely-meaning-preserving pass rate, and the confirmation rate of the 546 originals. Emit in the identical
  exp_sel_data_out flattened-metadata schema (pair_id/role linkage, doc-level folds), preserving the iter-1 originals VERBATIM,
  then report per-concept surface-response null distribution sizes. Schema-validate with aii-json; emit full/mini/preview.
  Hard $10 OpenRouter cap (est. ~$3-4); no GPU.
runpod_compute_profile: cpu_heavy
ideal_dataset_criteria: |-
  TWO enlarged surface-flip pair sets, each a superset of the frozen iter-1 originals, emitted in the SAME exp_sel_data_out flattened-metadata schema so the next iteration's admission filter consumes them identically.

  WHAT A SURFACE-FLIP PAIR IS (the load-bearing semantics): a CONCEPT-CONSTANT, SURFACE-CHANGED minimal pair used to estimate the shuffled-surface null in Step-5 (a unit is admitted only if its pooled surface-response is NOT above this null). The concept is held fixed; only the surface realization changes.
    - FIRST-LETTER concept 'starts-with-<X>': a pair = two DISTINCT single-token, slot-eligible words that BOTH start with the target letter X, placed in the SAME carrier template. Concept ('starts-with-X') is constant; surface (the word + its token id) changes. Meaning is NOT preserved between the two words (they are different words) -- what is preserved is the CONCEPT, so 'genuinely meaning-preserving' for this concept means 'genuinely concept-constant + grammatical/natural'. The deterministic structural check (both words begin with X, differ, single-token, slot-eligible, char-span correct) is AUTHORITATIVE; any LLM judge is a secondary naturalness audit and never drops a structurally-valid pair.
    - TOXICITY concept 'toxic': a pair = a toxic source comment and a TOXIC paraphrase of it (toxicity held constant, wording reworded). Both must remain toxic and meaning-equivalent; surface must genuinely differ.

  SIZE: >=1,500 surface pairs PER CONCEPT after enlargement (from 590 first-letter and 546 toxicity). The set must INCLUDE all iter-1 originals verbatim (same pair_ids, same field values) plus newly-generated pairs with fresh non-colliding pair_ids.

  INDEPENDENCE / NON-CIRCULARITY: every new toxicity pair must be accepted by a judge from a DIFFERENT model family than its generator; a stratified sample of BOTH concepts (originals + new) must be re-judged by a family different from both the generator AND the original iter-1 judge of that set (toxicity: gpt-4o-mini generated AND judged -> re-judge with anthropic/claude-haiku-4.5; first-letter: judged by google/gemini-3.1-flash-lite -> re-judge with a non-Gemini family, anthropic/claude-haiku-4.5). Report cross-judge agreement (raw + Cohen's kappa) and the genuinely-meaning-preserving pass rate per concept, plus the fraction of the 546 toxicity originals the independent judge confirms.

  GATES (reuse iter-1 values exactly): toxicity double-gate = token Jaccard <= 0.6 AND normalized char-change >= 0.25 (so surface genuinely differs), THEN judge for toxicity-constant + meaning-preserved + fluent. First-letter = deterministic structural validity.

  SCHEMA: identical to iter-1 (flattened metadata_* keys; pairs link by metadata_pair_id + metadata_role in {var_a,var_b} for first-letter or one-row-per-pair input/metadata_text_paired for toxicity; doc-level folds: first-letter folds by target_word 1-5, toxicity train/val/test by source with no cross-fold leakage). Real, pinned source corpora only (s-nlp/paradetox, google/civil_comments for toxicity; Gemma tokenizer vocab for first-letter words). No GPU, no SAE, no model activations. Hard $10 OpenRouter cap.

  REPORTED OUTPUTS: per-concept surface-response null distribution SIZE (total pairs + per-stratum: per-letter for first-letter, per-origin and optionally per-sub-attribute for toxicity), cross-judge agreement/kappa, independent-judge pass rate, originals-confirmation rate, generation cost.
dataset_search_plan: |-
  This is an ENLARGEMENT + INDEPENDENT-RE-JUDGE build, not a search. Source corpora and protocols are already pinned; the executor reuses them. Inputs are read directly from the iter-1 workspace (the temp/build/ helper scripts may be absent, but the surface rows are guaranteed present in the iter-1 full_data_out.json files).

  === PINNED INPUT PATHS (read these directly) ===
  - First-letter testbed: /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json  (dataset groups per letter; surface_flip rows have metadata_pair_type='surface_flip', metadata_role in {var_a,var_b}). Also read its preview_data_out.json metadata.llm_judge block (confirms judge model = google/gemini-3.1-flash-lite, secondary) and metadata.generation_config (carriers t_verbose/t_colon/t_mention_word, get_alpha_tokens recipe, tokenizer unsloth/gemma-2-2b vocab 256000, fold_rule 'minimal pairs by target_word').
  - Toxicity family: /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_3/full_data_out.json  (groups 'paradetox' and 'civil_comments'; surface_pair rows have metadata_record_type='surface_pair'). Also read data_summary.json -> surface_generation block (gen_model=judge_model=openai/gpt-4o-mini [the circularity], jaccard_max=0.6, char_change_min=0.25, 800 sources -> 546 accepted, judge_pass_rate 0.7063).
  - Dossier (dependency art_I2MrezW41iQo): /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_research_2/research_out.json  -> WP4 (minimal-pair generation prompt + independent LLM-judge rubric {content_flipped/surface_preserved/fluent/confidence/justification}; verified June-2026 OpenRouter prices: generator gemini-3.1-flash-lite $0.25/$1.50 or deepseek-v4-flash $0.09/$0.18; judge claude-haiku-4.5 $1.00/$5.00) and WP5 (get_alpha_tokens: convert_tokens_to_string -> strip ONE leading space -> require all chars in a-zA-Z; word-initial '_'/space-piece + single-token; carrier templates).

  === STEP 0 — INGEST & PARSE ORIGINALS (verbatim, no mutation) ===
  1. Load the two iter-1 full_data_out.json files. Extract ALL surface rows verbatim: first-letter -> 590 surface_flip pairs = 1,180 rows (L=170,O=105,T=95,I=110,D=110 pairs); toxicity -> 546 surface_pair rows. Record the exact per-concept original counts and per-stratum breakdown for the final null-size report.
  2. Capture the EXACT field set of each row type (so new rows are byte-compatible). First-letter surface_flip row keys: input, output, metadata_dataset, metadata_letter, metadata_pair_id, metadata_pair_type, metadata_role, metadata_sub_context, metadata_target_word, metadata_counterpart_word, metadata_template_id, metadata_label_starts_with_target, metadata_is_single_token, metadata_is_slot_eligible, metadata_first_letter, metadata_fold, metadata_word_char_span, metadata_judge_pass. Toxicity surface_pair row keys: input, output, metadata_id, metadata_fold, metadata_record_type, metadata_source, metadata_origin_source, metadata_toxicity_label, metadata_text_on(null), metadata_text_off(null), metadata_text_paired, metadata_pair_id, metadata_source_sentence_id, metadata_is_content_pair(false), metadata_is_surface_pair(true), metadata_subcontext_labels(6 nulls), metadata_subcontext_floats(7 nulls), metadata_subcontext_threshold(null), metadata_judge_pass, metadata_gen_model, metadata_surface_metrics{jaccard,char_change,reason}.
  3. To keep the output a clean drop-in, this artifact emits the SURFACE-PAIR superset only (it does NOT re-emit or mutate the frozen content_flip/content_pair/classification/corpus rows, which remain canonical at their iter-1 paths). State this explicitly in the README and reference the iter-1 paths the experiment merges by pair_id/record_type.

  === STEP 1 — ENLARGE FIRST-LETTER SURFACE PAIRS (590 -> >=1,500; deterministic, ~$0) ===
  1. Reuse the iter-1 word pools. For each target letter in {L,O,T,I,D}, gather single-token, slot-eligible words beginning with that letter using the get_alpha_tokens recipe (WP5) over the unsloth/gemma-2-2b tokenizer (vocab 256000): for each vocab token, tokenizer.convert_tokens_to_string([tok]) -> strip one leading space -> require word-initial (the '_'/space-piece marker, i.e. the token forms a word start) AND all chars a-zA-Z; keep words whose first alpha char (case-insensitive) == target letter. Verify each candidate word is single-token (re-encodes to one id) and slot-eligible. This yields tens-to-hundreds of words per letter -> more than enough (n words -> n*(n-1)/2 unordered same-letter pairs).
  2. Form NEW surface_flip pairs = ordered (var_a, var_b) of two DISTINCT same-letter words, placed in EACH of the 3 carriers (t_verbose '{word} has the first letter:', t_colon '{word}:', t_mention_word 'Here is an example word: {word}.'). Reproduce the carrier strings exactly from the iter-1 rows. Exclude case-only variants (e.g. 'list'/'List') as the iter-1 judge rejects them as the same word. Avoid regenerating any (word_a,word_b,carrier) combination already present in the 590 originals (dedupe on the normalized triple).
  3. Target distribution: bring each letter to >=300 surface pairs (5 letters x 300 = 1,500), balanced across the 3 carriers, so the per-letter null is well-powered; cap per (letter,carrier) to keep balance. Assign metadata_fold by target_word using the SAME 5-fold rule as iter-1 (a word's fold is deterministic from its hash/assignment; keep both members of a pair in one fold; never split a pair across folds). Set metadata_pair_type='surface_flip', metadata_role var_a/var_b, metadata_sub_context='wordA|wordB', metadata_label_starts_with_target=1 for both, metadata_first_letter=lowercase target, metadata_is_single_token/slot_eligible=true, metadata_word_char_span = char offsets of the slotted word in input, output = uppercase target letter. Assign fresh pair_ids that do not collide with iter-1 (e.g. '<L>_s2_NNNN').
  4. Run the DETERMINISTIC structural validator on every new pair (AUTHORITATIVE): both words begin with target letter, differ, single-token, slot-eligible, input[word_char_span]==target_word. Drop any violation (should be zero by construction); report violations==0 like iter-1.

  === STEP 2 — ENLARGE TOXICITY SURFACE PAIRS (546 -> >=1,500; OpenRouter, gated) ===
  1. Assemble fresh toxic SOURCE sentences NOT already used (dedupe against iter-1 metadata_source_sentence_id and against the originals' input/text_paired). Draw from: (a) s-nlp/paradetox en_toxic_comment column (download via aii-hf-datasets); (b) google/civil_comments rows with toxicity>=0.5 (stream-filter + subsample to stay <300MB and CC0). Stratify civil_comments sources across sub-attributes (obscene/threat/insult/identity_attack/sexual_explicit each >=0.5) so the enlarged set spans the same sub-contexts; tag the source's sub-attribute floats.
  2. Generate ONE toxic->toxic paraphrase per source via OpenRouter using the WP4 surface-flip prompt (instruction: reword the surface form, keep the toxicity level and target the same, do not detoxify, do not add new insults). Generator = openai/gpt-4o-mini (homogeneous with the 546 originals; ~$0.15/$0.60). If gpt-4o-mini refuses too often (iter-1 refusal_rate was only 0.015) or quality drops, fall back to google/gemini-3.1-flash-lite or deepseek-v4-flash. Generate enough sources to clear the target after gating: at iter-1's ~68% acceptance, ~1,400 new generations yield ~950 accepted -> with the 546 originals exceeds 1,500; budget up to ~1,800-2,000 sources for safety.
  3. Apply the iter-1 DOUBLE-GATE on (source, paraphrase): token Jaccard <= 0.6 (surface differs enough) AND normalized char-change >= 0.25; record metadata_surface_metrics{jaccard,char_change,reason}. Drop pairs failing the gate.
  4. Judge each gate-passing NEW pair with anthropic/claude-haiku-4.5 (INDEPENDENT family from the gpt-4o-mini generator -> no circularity). Rubric (adapt WP4): return {toxicity_constant (still toxic, same severity/target), meaning_preserved (semantically equivalent), surface_changed, fluent, confidence, justification}; ACCEPT iff toxicity_constant AND meaning_preserved AND surface_changed AND fluent. Discard fails. This makes every NEW pair born with an independent judge. Set metadata_source='generated_paraphrase', metadata_origin_source in {paradetox,civil_comments}, metadata_toxicity_label=1, metadata_gen_model=generator id, output='toxic', input=source, metadata_text_paired=paraphrase, fresh metadata_pair_id 'sp2_<hash>' and metadata_id 'tox_sp_NNNNNN' continuing the counter, metadata_fold inherited from the source's classification fold (no cross-fold leakage). OPTIONAL ENHANCEMENT (schema-compatible): for civil_comments-origin new pairs, populate metadata_subcontext_floats with the source's real sub-attribute floats (paradetox has none -> keep null) so the experiment can build per-sub-context surface nulls; keep metadata_subcontext_labels null unless thresholded.

  === STEP 3 — INDEPENDENT RE-JUDGE + CROSS-JUDGE AGREEMENT (resolves the circularity critique) ===
  1. Build a STRATIFIED re-judge sample per concept mixing iter-1 ORIGINALS and NEW pairs: toxicity stratified by origin (paradetox/civil_comments) x surface_metrics bins (low/high jaccard, low/high char_change); first-letter stratified by letter x carrier. Target ~300-400 sampled pairs per concept (~700 total).
  2. PRIMARY independent judge = anthropic/claude-haiku-4.5 for BOTH concepts (family != gpt-4o-mini [toxicity gen+judge] and != gemini-3.1-flash-lite [first-letter judge]). For toxicity it applies the Step-2 rubric; for first-letter it judges concept-constancy (both words start with target letter) + grammaticality/naturalness (deterministic remains authoritative -> a judge 'fail' on structurally-valid first-letter pairs is logged as a judge false-negative, NOT a drop, exactly like iter-1).
  3. To obtain a genuine 2-judge agreement that is independent of the generator, run a SECOND-family judge on the SAME sample: google/gemini-3.1-flash-lite for the toxicity sample (independent of both gpt-4o-mini and Anthropic) and deepseek-v4-flash (or gemini) for the first-letter sample (non-Gemini-original concern is satisfied by claude as primary). Report: (a) per-concept genuinely-meaning-preserving pass rate (fraction the independent judge passes); (b) cross-judge agreement = raw agreement + Cohen's kappa between the two independent judges on the sample; (c) the key circularity number = fraction of the 546 toxicity ORIGINALS (all gpt-4o-mini-accepted) that claude-haiku-4.5 CONFIRMS; (d) for first-letter, agreement of claude vs the stored gemini secondary labels on originals that carry them.
  4. Annotate every re-judged row with metadata_independent_judge_model, metadata_independent_judge_pass, metadata_independent_judge_reason. Add metadata_enlargement_batch in {'iter1_original','iter2_new'} to EVERY surface row. To keep exp_sel_data_out key-uniformity within each concept group, add these three independent-judge keys (null where a row was not in the re-judge sample) to ALL surface rows of that concept.

  === STEP 4 — ASSEMBLE THE SUPERSET (exp_sel_data_out schema) ===
  1. Output structure mirrors iter-1: a top-level object with metadata + a 'datasets' list of {dataset, examples[]} groups. FIRST-LETTER groups: one per letter (first_letter_spelling_L ... _D) holding that letter's surface_flip rows (originals verbatim + new). TOXICITY groups: 'paradetox' and 'civil_comments' holding surface_pair rows (originals verbatim + new), folded by metadata_origin_source as in iter-1.
  2. Originals MUST be byte-identical to iter-1 (same pair_ids, fields, values) except for the two additive uniformity keys (metadata_enlargement_batch='iter1_original'; the independent-judge keys, populated only if that original was in the re-judge sample, else null). New rows use the field templates captured in Step 0.
  3. Verify it is a true SUPERSET: every iter-1 surface pair_id is present; total surface pairs per concept >= max(1,500, original). Re-run the deterministic first-letter validator and the toxicity double-gate over the whole assembled set; assert zero structural violations and that every accepted toxicity pair has metadata_surface_metrics within gate bounds.

  === STEP 5 — REPORT SURFACE-RESPONSE NULL DISTRIBUTION SIZES ===
  In a data_summary.json (mirroring iter-1) report, per concept: total surface pairs available for the shuffled-surface null, broken down by stratum (first-letter: per letter x carrier; toxicity: per origin and, where populated, per sub-attribute), plus originals-vs-new counts, generation/judge stats (n_sources, n_gate_pass, n_accepted, acceptance rate, refusals, cost_usd, openrouter_calls), cross-judge agreement/kappa, independent-judge pass rate, originals-confirmation rate, and the exact gate constants used (jaccard_max=0.6, char_change_min=0.25). This is the 'per-concept surface-response null distribution size' deliverable the objective asks for.

  === STEP 6 — VALIDATE & VARIANTS ===
  1. Validate the assembled data_out.json against the exp_sel_data_out schema using the aii-json skill (each row must have non-empty input + output + metadata_fold; consistent metadata_* keys within a group).
  2. Emit full_data_out.json (canonical), mini_data_out.json, preview_data_out.json via aii-json. Run the aii-file-size-limit check (the surface-only superset is small -- ~3,000 first-letter rows + ~1,500 toxicity rows -- well under 300MB; split only if needed).
  3. Write a README documenting: the circularity fixed, model families used per step, the superset guarantee, the merge contract with the frozen iter-1 content/classification rows, and the null-size table.

  === COST CONTROL (hard $10 cap) ===
  Track cumulative OpenRouter spend after every call; STOP at $10. Estimate: toxicity gen ~2,000 x ~$0.0002 = ~$0.4 (gpt-4o-mini); toxicity accept-judge ~1,600 gate-passers x ~$0.0011 = ~$1.8 (claude-haiku); re-judge+second-judge samples ~1,400 calls x ~$0.0006-0.0011 = ~$1.0. Total ~$3-4, ample headroom. If approaching the cap: reduce the toxicity target toward 1,500 exactly, batch multiple pairs per judge call, switch generator to deepseek-v4-flash ($0.09/$0.18), or shrink the re-judge sample (keep >=200/concept for a stable kappa).

  === FAILURE / FALLBACK SCENARIOS ===
  - Toxicity acceptance < expected: generate more sources (cap ~2,500) or relax nothing on the gate (keep jaccard/char fixed for comparability); if still short, report the achieved count honestly and the null-size as-is (>=1,000 still strengthens the control). NEVER lower the double-gate to hit a number.
  - Independent judge refuses toxic content: frame the judge call as a CLASSIFICATION/validation task (not generation); if claude-haiku refuses, fall back to gemini-3.1-flash-lite or deepseek-v4-flash as the independent family (still != gpt-4o-mini). Record refusals.
  - First-letter word pool too small for a letter to reach 300 (unlikely): lift the per-(letter,carrier) cap or add a 4th carrier only if it matches an iter-1 template; if a letter genuinely caps out, redistribute the target to other letters and report the achieved per-letter sizes.
  - Low cross-judge agreement (kappa low): this is a REPORTABLE finding (the iter-1 same-model gate was lenient), not a failure -- keep all pairs in the superset with the independent-judge label recorded so the experiment can filter to the 'both-judges-pass' high-confidence subset; report both the full and high-confidence null sizes.
  - civil_comments download >300MB: stream + filter to toxicity>=0.5 and subsample before materializing; never load the full 414.95MB file.

  NOTE on the direction's claim: the direction states the first-letter set 'used gemini-3.1-flash-lite' as judge -- CONFIRMED (metadata.llm_judge.model='google/gemini-3.1-flash-lite', secondary role). The first-letter surface pairs are mechanically/deterministically constructed (not LLM-paraphrased), so enlargement there is deterministic and the independent re-judge is a naturalness/concept-constancy audit, not an acceptance gate.
target_num_datasets: 2
</artifact_plan>

<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
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
out_dependency_files:
  file_list:
  - research_out.json

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>

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
TODO 1. Update data.py to only include the chosen 2 datasets and generate full_data_out.json. Re-run to generate full_data_out.json. Validate output format with aii-json skill and fix any errors. Generate full, mini, and preview versions with aii-json skill's format script using `--input full_data_out.json` (creates full_full_data_out.json, mini_full_data_out.json, preview_full_data_out.json — rename to full_data_out.json, mini_data_out.json, preview_data_out.json).
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
