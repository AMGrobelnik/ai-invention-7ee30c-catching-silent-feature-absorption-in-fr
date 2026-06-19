# Data sources & provenance — Safety-Relevant Identity Absorption Testbed

This testbed is **constructed** (templated minimal pairs + a labelled real-text diagnostic corpus),
so its "datasets" are (a) the FOUR identity hierarchies we build, and (b) the real-text corpus sources
we stream. Every source below was verified for downloads, documentation, license, and a citable paper
(no fabricated provenance). Sub-context labels are **always surface-derived**, never taken from a
source's own labels (the degenerate-construction guard).

## Primary corpus (shipped) — `monology/pile-uncopyrighted`
- **HF downloads:** 68,643 · **documented:** yes (dataset card + The Pile paper) · **license:** other
  (copyright-stripped subset of The Pile).
- **Pinned revision:** `3be90335b66f24456a5d6659d9c8d208c0357119` (frozen, fully reproducible; the SAME
  revision used by the iter-1 taxonomic testbed `gen_art_dataset_2` and the iter-5 homograph testbed).
- **Paper:** Gao et al., *The Pile: An 800GB Dataset of Diverse Text for Language Modeling*,
  arXiv:2101.00027.
- **Why suitable:** large, diverse, real English text with `pile_set_name` provenance per document
  (Pile-CC, Wikipedia (en), PubMed, FreeLaw, …); identity tokens (American/Black/White/Muslim/
  Christian/Jewish/Chinese/…) are abundant, so a high-precision surface-form classifier yields ample
  diagnostic positives per sub-context. Streamed via HTTP + zstandard over the pinned LFS shards
  (NOT `load_dataset`, which pulls >300 MB and busts the working limit).

## Optional safety-relevant supplement (tested, opt-in via `--with-civil`) — `google/civil_comments`
- **HF downloads:** 9,537 · **documented:** yes · **license:** CC0 1.0.
- **Columns:** `text` + 7 float toxicity sub-attributes (toxicity, severe_toxicity, obscene, threat,
  insult, identity_attack, sexual_explicit). NOTE: civil_comments has **no per-identity columns**
  (those live only in the Jigsaw competition CSV, see below).
- **Paper:** Borkan et al., *Nuanced Metrics for Measuring Unintended Bias with Real Data for Text
  Classification*, WWW 2019 (the Jigsaw "Unintended Bias in Toxicity Classification" data).
- **Role:** identity-rich real comments to bias the corpus toward demographic text. sub_context is
  STILL surface-derived; the toxicity column is recorded only as a corroborating
  `metadata_identity_label_source` (e.g. `civil_comments:toxicity>=0.5`). Verified to stream cleanly
  (8,000 rows → 249 labelled identity rows in ~5 s). Pile is the guaranteed-reproducible default, so
  the build never blocks on this supplement.

## Intentionally omitted — `google/jigsaw_unintended_bias`
- The plan names this as the per-identity-column source (christian/jewish/muslim/black/white/…).
  It is a **manual-download** dataset (the Kaggle competition CSVs); HF dataset search returns it as
  non-loadable here. Per the plan's fallback scenario (1) we omit it and rely on Pile (+ optional
  civil_comments), which is sufficient and reproducible. Recorded in `manifest.json`.

## Demonym → country provenance (nationality hierarchy)
- The demonym→country gazetteer is **baked into `build_dataset.py`** (no runtime package dependency,
  per plan). Cross-checked against `pycountry` (v249 ISO countries): all 31 demonyms resolve to a real
  ISO country (28 resolve by exact `pycountry.countries.lookup`; the 3 "misses" — Turkish→Türkiye,
  Russian→Russian Federation, Korean→Korea, Rep. — are ISO canonical-name aliases, all real countries).

## Token anchoring & method de-risking
- Target tokens anchored in the real `google/gemma-2-2b` vocab (vocab 256000) via offset-mapping
  (`add_special_tokens=False`); falls back to the non-gated `unsloth/gemma-2-2b` mirror. Multi-token
  spans (e.g. "African American") flagged `metadata_multi_token=true`.
- Absorption diagnostic context (consumer, next iteration): Chanin et al., *A is for Absorption:
  Studying Feature Splitting and Absorption in Sparse Autoencoders*, arXiv:2409.14507 — absorption is
  empirically documented ONLY on first-letter spelling, so this safety-relevant identity testbed is
  simultaneously a generality test and a novel empirical test.

## LLM augment + judge (OpenRouter, hard $10 cap)
- Generator `openai/gpt-4o-mini` ($0.15/$0.60 per M); judge `anthropic/claude-haiku-4.5` ($1.00/$5.00
  per M) — a DIFFERENT family than the generator, rubric extended with `sense_correct`. Both confirmed
  available on OpenRouter. The templated backbone is free, so LLM spend is small (see `manifest.json`
  `llm_cost_usd`).
