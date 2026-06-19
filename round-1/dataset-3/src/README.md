# Two-Track CCRG Toxicity Dataset Family

One schema-standardized **toxicity** dataset family with three role-distinct
components that downstream iter-2 CCRG experiments consume directly. Built for
the goal *"organise SAE activations into more reliable units of analysis than
individual latents"* — this family hosts the C1 count-matched classification
task, the C-track (splitting / shared-support) story, and the
selection-criterion / worst-sub-context reweighting test.

## Deliverables (workspace root)

| File | Contents |
|------|----------|
| `data.py` | **Single self-contained `uv run` assembler** → emits the JSON below |
| `full_data_out.json` | **Full dataset** (37,707 rows), `exp_sel_data_out` schema, validated |
| `data_out.json` | Compact copy (format-script input; identical content) |
| `mini_data_out.json` | 3 examples/dataset (representative head: covers all record_types) |
| `preview_data_out.json` | mini with strings truncated to 200 chars |
| `data_summary.json` | Manifest: per-sub-context power, co-occurrence matrix, generation stats |
| `build/` | Staged pipeline (s1 content-flips, s2 civil stream-filter, s3 OpenRouter surface gen, s4 assemble, verify_baseline) |
| `temp/intermediate/` | Cached component outputs + the LLM generation/judge audit caches (JSONL) |

## Best 2 datasets

`target_num_datasets = 2`. The two real, well-documented, permissively-licensed
HuggingFace **source corpora** are the dataset groups: **`paradetox`**
(Logacheva et al., ACL 2022; openrail++) and **`civil_comments`** (Jigsaw
Unintended Bias, Borkan et al. 2019; CC0 1.0). The LLM-**generated** surface-flip
pairs are not a third corpus — they are seeded from those two and folded into
the group of their seed sentence's source (`metadata_origin_source`). So the
family presents exactly two dataset groups while still carrying all three
`metadata_record_type`s (`content_pair` / `surface_pair` / `classification`).

## Three components (shared schema, one row per pair)

1. **Content-flip pairs** (`record_type=content_pair`, source `paradetox`, 18,853 rows).
   Human-written parallel toxic↔neutral sentences from **ParaDetox**
   (Logacheva et al., ACL 2022; `s-nlp/paradetox`, openrail++). This is the
   *non-circular* content perturbation P: `metadata_text_on` = toxic (concept
   PRESENT), `metadata_text_off` = neutral (concept ABSENT). Used to compute
   per-latent content-response `r_l = a_l(x_on) − a_l(x_off)`. Human-authored,
   so co-response grouping is not circular.

2. **Surface-flip pairs** (`record_type=surface_pair`, source `generated_paraphrase`, 546 rows).
   Toxic→toxic paraphrases (content held fixed, wording changed) generated via
   **OpenRouter `openai/gpt-4o-mini`** under a defensive-research framing, then
   double-gated: a programmatic surface-change gate (token Jaccard < 0.6 AND
   normalized edit distance > 0.25) and an LLM-judge gate
   (`toxicity_preserved AND meaning_preserved`). `input` = original toxic `x`,
   `metadata_text_paired` = reworded toxic `x'`. The surface-invariance control:
   a valid unit's pooled surface-response must not exceed the shuffled-surface
   null. Judge pass rate **70.6%**, refusal rate **1.5%**, cost **$0.060**.

3. **Independent sub-context classification set** (`record_type=classification`, source `civil_comments`, 18,308 rows).
   Real toxic / non-toxic comments from **civil_comments** (Jigsaw Unintended
   Bias, Borkan et al. 2019; `google/civil_comments`, CC0 1.0) carrying a binary
   `metadata_toxicity_label` plus **FROZEN multi-label** sub-context labels
   (`severe_toxicity, obscene, threat, insult, identity_attack, sexual_explicit`)
   thresholded from the raw annotator-fraction floats at 0.5 (primary). Raw
   floats are preserved (`metadata_subcontext_floats`) so labels can be
   re-derived at the 0.3 fallback and so sub-attribute co-occurrence can be
   measured. Labels are frozen *before* any SAE comparison and are never derived
   from SAE members (degenerate-construction guard).

## Schema (per example)

Conforms to `exp_sel_data_out` (`{datasets:[{dataset, examples:[{input, output,
metadata_*}]}]}`, `additionalProperties:false`), so every domain field is carried
under a `metadata_` prefix:

`metadata_id`, `metadata_fold` (train/val/test), `metadata_record_type`,
`metadata_source`, `metadata_toxicity_label` (0/1), `metadata_text_on`,
`metadata_text_off`, `metadata_text_paired`, `metadata_pair_id`,
`metadata_source_sentence_id`, `metadata_is_content_pair`,
`metadata_is_surface_pair`, `metadata_subcontext_labels` (6 ints|null),
`metadata_subcontext_floats` (7 floats|null), `metadata_subcontext_threshold`,
`metadata_judge_pass`, `metadata_gen_model`. `output` ∈ {`toxic`, `non_toxic`}.

The top-level `datasets` array has **two entries** (`paradetox`,
`civil_comments`); filter `metadata_record_type` to recover the three
components, and flatten `datasets[*].examples` to iterate the family uniformly.
The full manifest is in `data_summary.json` and mirrored in the top-level
`metadata` object of `full_data_out.json`.

## Folds & leakage safety

`metadata_fold` ∈ {train, val, test}. civil_comments rows inherit their native
split. Folds are assigned by a **union-find over normalized-text keys**: the two
members of every pair are linked, identical texts across components collapse to
one fold-group, and each group is anchored to the native split when a
classification row is present (else a stable 80/10/10 hash of the component).
Verified invariants (`build/verify_baseline.py`): **0** `pair_id` spanning folds,
**0** `source_sentence_id` spanning folds, **0** normalized texts appearing in
more than one fold (no grouping→eval leakage). 316 cross-source ParaDetox↔civil
collisions were reconciled by co-folding; 0 grouping rows dropped.

## Power (n_min = 150 per sub-context for the paired-bootstrap MDE)

At threshold 0.5, **inferential** (≥150 positives in each eval fold):
`obscene, threat, insult, identity_attack, sexual_explicit`.
`severe_toxicity` is **descriptive-only** (13 @0.5, 95 @0.3 — too rare even after
the pre-registered relaxation; flagged, not silently dropped). The Jaccard
co-occurrence matrix in `data_summary.json` informs the C-track-vs-K-track
question: `insult↔obscene` ≈ 0.245 and `obscene↔sexual_explicit` ≈ 0.185 share
support (C-track), while `threat` / `identity_attack` are near-disjoint from the
others (<0.05; K-track).

## Sanity baselines (`build/verify_baseline.py`, TF-IDF + logistic regression)

- Toxicity (train→test): **AUC 0.851, F1 0.773**.
- Sub-contexts one-vs-rest AUC: obscene 0.900, threat 0.936, insult 0.808,
  identity_attack 0.925, sexual_explicit 0.929.
- Content pairs mean TF-IDF cos(toxic, neutral) = 0.685 (content genuinely flips).
- Surface pairs mean TF-IDF cos(x, x') = 0.355 (substantially reworded, not copied).

## Reproduce

Final assembly (stdlib-only, deterministic, $0 — consumes the cached component
outputs in `temp/`):

```bash
uv run data.py                                  # -> data_out.json + full_data_out.json + data_summary.json
SK=/ai-inventor/.claude/skills/aii-json; PY=$SK/../.ability_client_venv/bin/python
$PY $SK/scripts/aii_json_format_mini_preview.py --format exp_sel_data_out --input data_out.json
$PY $SK/scripts/aii_json_validate_schema.py     --format exp_sel_data_out --file full_data_out.json
.venv/bin/python build/verify_baseline.py       # invariants + signal baselines
```

Regenerate the cached component inputs from scratch (network + OpenRouter):

```bash
.venv/bin/python build/s1_content_flips.py      # ParaDetox content-flips
.venv/bin/python build/s2_classification.py     # civil_comments stream-filter (~4 min)
.venv/bin/python build/s3_surface_flips.py \
    --gen-model openai/gpt-4o-mini --judge-model openai/gpt-4o-mini \
    --n-paradetox 450 --n-civil 350             # OpenRouter; cached, resumable
```

LLM calls go through OpenRouter only; total spend **$0.060** (hard component
ceiling $5, global $10). `temp/datasets/` (raw HF downloads incl. backup
sources) and `.venv/` are excluded from the published repo.
