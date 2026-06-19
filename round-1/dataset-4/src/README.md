# CCRG supporting concept families + boundary-null dataset

Three real, human-annotated datasets standardized into the CCRG **shared minimal-pair schema**
(one row per text; content-flip pairs reconstructable via `pair_id`/`partner_id`). Emitted in the
canonical `exp_sel_data_out` format: `{metadata, datasets:[{dataset, examples:[{input, output, metadata_*}]}]}`.
**No LLM calls — all sources are human-annotated → $0 OpenRouter spend.**

## Families (separable via `metadata_family`)

| family | source | role | rows | pairs | concept(s) | independent sub-context |
|---|---|---|---|---|---|---|
| `sentiment` | CAD-IMDB (Kaushik et al. ICLR 2020) | supporting | 4,880 | 2,440 | `sentiment` | — |
| `restaurant_aspect` | CEBaB (Abraham et al. NeurIPS 2022) | supporting | 5,682 | 2,841 (food 1,740 / service 1,101) | `food_sentiment`, `service_sentiment` | food/service/ambiance/noise/review_sentiment |
| `bias_in_bios_boundary` | LabHC/bias_in_bios (De-Arteaga et al. 2019) | **boundary-null** | 20,177 | — (unpaired) | `profession` (28) | gender |

Total: **30,739 rows**, **5,281 minimal pairs**. `is_surface_pair = false` for every row (surface flips are
out of scope here — reserved for sibling ParaDetox/LLM artifacts).

## Deliverables
- `full_data_out.json` — all 30,739 rows (33 MB), validated against `exp_sel_data_out` and `schema.json`.
- `mini_data_out.json` — 3 examples/dataset (9 rows), full strings (aii-json format convention).
- `preview_data_out.json` — 3 examples/dataset (9 rows), strings truncated to 200 chars.
- `schema.json` — logical row schema (the `exp_sel_data_out` `metadata_*` fields map 1:1 to it).
- `data_summary.json` — the metadata block alone (per-family counts, balances, provenance, licenses).
- `manifest.json` — machine-readable deliverable + provenance index.
- `data.py` (entry point) / `build_dataset.py` / `qc.py` / `explore.py` / `verify.py` — reproducible pipeline (`uv run data.py`).

## Schema (per row, logical view)
`id, input, output, family, dataset_source, concept, concept_label, sub_context(dict),
pair_id, pair_role(content_off|content_on|null), partner_id, flip_type(content|null),
is_content_pair, is_surface_pair(=false), fold(train|dev|test), meta(dict)`. In the emitted file every
field except `input`/`output` is carried under a `metadata_` prefix.

## Key methodological decisions & corrections (verified empirically, not assumed)
1. **CAD-IMDB pairing.** The plan assumed `orig/[i] ↔ new/[i]` row-index alignment. This was **tested and
   REJECTED** (flip_rate ≈ 0.50, aligned token-Jaccard ≈ random ≈ 0.11). The authoritative pairing is the
   repo's `sentiment/combined/paired/*_paired.tsv`, where rows sharing a `batch_id` form one human minimal
   edit (exactly one Positive + one Negative). True-pair Jaccard = **0.816** vs random **0.108** confirms
   minimal edits. Pairing method recorded as `batch_id_grouped`.
2. **CEBaB field semantics.** The plan had `edit_goal`/`edit_type` swapped. Actual data: `edit_type` ∈
   {food,service,ambiance,noise} is the **edited aspect** (we pair on it); `edit_goal` ∈
   {Positive,Negative,unknown} is the target sentiment. `review_majority` is a **1–5 star rating** (binarized
   1,2→negative / 4,5→positive / 3→neutral / "no majority"). Only food+service pairs whose edited-aspect
   majority is Positive↔Negative and differs are kept; food/service nested as ONE family with all four aspect
   majorities retained as independent sub-context.
3. **bias_in_bios profession mapping.** The HF dataset ships no `ClassLabel` names. The canonical
   De-Arteaga 28-occupation alphabetical ordering (incl. `dj` at index 8) was **empirically verified 17/17**
   by keyword hit-rate (nurse=13, attorney=2, surgeon=25, software_engineer=24, yoga_teacher=27, …).
   Gender 0=male/1=female verified by pronoun inspection. Stratified subsample by (profession×gender),
   56 strata, fixed seed `20240617`; full 396k bios reproducible from the HF repo.
4. **Boundary-null rationale.** In bias_in_bios the profession "habitat" ≈ the class label, so co-response
   grouping is *predicted* to give no advantage — a **pre-registered expected null**, not method failure.

## Licenses / provenance
- CAD-IMDB: Apache-2.0 — github.com/acmi-lab/counterfactually-augmented-data — arXiv:1909.12434
- CEBaB: CC-BY-4.0 — huggingface.co/datasets/CEBaB/CEBaB — arXiv:2205.14140
- bias_in_bios: MIT — huggingface.co/datasets/LabHC/bias_in_bios — arXiv:1901.09451

`temp/` (HF cache + raw TSVs) and `.venv/` are build scratch and excluded from the published repo.
