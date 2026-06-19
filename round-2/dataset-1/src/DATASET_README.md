# Enlarged & Independently Re-Judged Surface-Invariance Pair Sets (First-Letter + Toxicity)

A drop-in **SUPERSET** of the two iter-1 *surface-flip* pair sets that the next iteration's
**Step-5 admission AND-gate** consumes to estimate the *shuffled-surface null* (a candidate SAE
unit is admitted only if its pooled response to surface flips is **not** above this null). A
surface-flip pair holds the **concept constant** and changes only the **surface realization**.

This artifact emits the **surface-pair superset ONLY**. The frozen iter-1
content_flip / content_pair / classification / corpus rows are **not** re-emitted or mutated; they
stay canonical at their iter-1 paths (see *Merge contract*). Pure CPU/data task — **no GPU, no SAE,
no model activations**.

## Headline numbers
| concept | iter-1 originals | iter-2 superset | per-stratum |
|---|---|---|---|
| **first-letter** `starts-with-X` | 590 pairs | **1,700 pairs** (3,400 rows) | 340 pairs each for L/O/T/I/D |
| **toxicity** `toxic` | 546 pairs | **1,631 pairs** | paradetox 525, civil_comments 1,106 |

Both concepts clear the ≥1,500-pair target. Total OpenRouter spend **$1.72** (hard cap $10).

## The circularity this build fixes
iter-1 **generated AND judged** the 546 toxicity surface pairs with the *same* model
(`openai/gpt-4o-mini`), and judged the first-letter pairs with `google/gemini-3.1-flash-lite`.
This iteration breaks that with judges from **different model families**:

| step | model | role |
|---|---|---|
| toxicity generation | `openai/gpt-4o-mini` | reword toxic→toxic (homogeneous w/ the 546 originals) |
| toxicity **accept** judge (every new pair) | `anthropic/claude-haiku-4.5` | independent family ≠ generator |
| toxicity 2nd-family judge (cross-judge sample) | `google/gemini-3.1-flash-lite` | ≠ gpt-4o-mini and ≠ Anthropic |
| first-letter independent judge | `anthropic/claude-haiku-4.5` | non-Gemini family ≠ iter-1 judge |
| first-letter 2nd-family judge | `deepseek/deepseek-v4-flash` | fresh family for a 2-judge kappa |

**Every new toxicity pair is born with an independent-family judge label.** Each row also carries
`metadata_independent_judge_{model,pass,reason}` (claude) and `metadata_enlargement_batch`.

### Independent re-judge results (the reportable circularity finding)
- **Originals-confirmation:** `claude-haiku-4.5` confirms **465/546 = 85.2%** of the
  gpt-4o-mini-accepted toxicity originals → ~15% of iter-1's same-model-accepted pairs do **not**
  survive a stricter independent judge (the same-model gate was somewhat lenient).
- **Toxicity cross-judge (claude vs gemini), n=399:** raw agreement **0.940**, Cohen's κ **0.263**
  (high base rates → low κ; claude pass 0.952, gemini pass 0.962). Reported with marginals.
- **First-letter independent audit (n=400 sampled):** claude pass-rate **0.68** ⇒ a **0.32 judge
  false-negative rate** on structurally-valid pairs (claude flags tokenizer-artifact words such as
  `doesn`/`isn` as un-natural). The **deterministic structural check is AUTHORITATIVE — these are
  logged as judge false-negatives, never dropped.**
- **First-letter cross-judge (claude vs deepseek), n=268:** raw **0.780**, κ **0.433**.
- **First-letter claude vs stored gemini labels (n=130):** raw **0.692**, κ **0.141**
  (claude pass 0.66 vs gemini 0.94 — claude is much stricter on naturalness).

## What a surface pair is
- **First-letter** `starts-with-X`: two **distinct single-token, slot-eligible** words that BOTH
  start with X, slotted into an identical carrier. Concept (`starts-with-X`) constant; surface
  (word + token id) varies. The two words differ, so meaning is not preserved — **the concept is**.
  Authoritative check: both begin with X, differ (case-insensitive), single-token, slot-eligible,
  `input[word_char_span]==target_word`. **0 violations / 1,700 pairs.**
- **Toxicity** `toxic`: a toxic source comment + a **toxic paraphrase** (toxicity held constant,
  wording reworded). Double-gate **token Jaccard < 0.6 AND normalized char-change > 0.25** (strict,
  verbatim from iter-1), then the independent judge requires
  `toxicity_constant ∧ meaning_preserved ∧ surface_changed ∧ fluent`.

## How it was built
- **First-letter (deterministic, $0):** word pool = the iter-1 `occurrence_tables` (the
  `unsloth/gemma-2-2b` tokenizer `get_alpha_tokens` slot-eligible, single-token, word-initial
  target-letter set, ranked by Pile frequency; len≥3, count≥20). New word-pairs are consecutive
  disjoint pairs over the ranked pool, skipping any word-set already used by the 590 originals, each
  emitted in the **same 5 carriers** as iter-1 (`t_verbose, t_colon, t_mention_word, t_mention_term,
  t_mention_example`). Fold by `target_word` (md5 % 5), both members in one fold.
- **Toxicity (OpenRouter, gated):** fresh toxic sources NOT already used as iter-1 surface sources
  (reusing content/classification toxic comments is the iter-1 protocol and inherits their native,
  leakage-safe fold). paradetox toxic from `content_pairs.json`; civil toxic from
  `classification.json`, **stratified across the 6 sub-attributes** with their real sub-attribute
  floats carried so the experiment can build per-sub-context surface nulls. Generation stats:
  1,500 generated, 25 refusals, 1,462 gate-pass, **1,085 accepted** (claude pass-rate 0.742; main
  rejection = softened toxicity, 362).

## Surface-response null-distribution sizes (the deliverable)
**First-letter** (one surface response per pair; 340 pairs/letter, balanced across 5 carriers):
L=340, O=340, T=340, I=340, D=340 → **1,700**.

**Toxicity** (one surface response per pair): paradetox 525, civil_comments 1,106 → **1,631**.
Per sub-attribute (civil-origin, label@0.5): insult 370, obscene 226, sexual_explicit 216,
identity_attack 211, threat 205, severe_toxicity 12. Cross-fold leakage: **0** (no toxicity surface
text spans >1 fold). `data_summary.json` has the full per-letter×carrier and per-origin×fold tables,
plus the `both-judges-pass` high-confidence subset sizes.

## Superset guarantee
Every iter-1 surface `pair_id` is present, and each iter-1 original row is **byte-identical** to
iter-1 except for ≤4 additive keys: `metadata_enlargement_batch` and the three
`metadata_independent_judge_*` keys (populated for re-judged rows, else null — toxicity originals are
all populated by the 546-confirmation pass). New rows use fresh non-colliding ids
(`<L>_s2_NNNN`, `sp2_<hash>`, `tox_sp_NNNNNN` continuing the counter). Verified by
`verify_superset.py`: **0 problems**.

## Schema & merge contract
`exp_sel_data_out` (validated PASSED for full/mini/preview): top-level `{metadata, datasets:[…]}`
with **7 groups** — `first_letter_spelling_{L,O,T,I,D}` + `paradetox` + `civil_comments`. Each row
has `input`, `output`, flattened `metadata_*`.
- **First-letter** pairs link by `metadata_pair_id` + `metadata_role ∈ {var_a,var_b}`; fold is an int
  0–4 by `target_word`.
- **Toxicity** is one row per pair (`input` = source toxic, `metadata_text_paired` = toxic
  paraphrase); fold ∈ {train,val,test} by source, no cross-fold leakage.

The experiment **merges this surface superset with the frozen iter-1 non-surface rows** by
`metadata_pair_id` / `metadata_record_type`:
- first-letter content_flip + corpus_context: `iter_1/gen_art/gen_art_dataset_1/full_data_out.json`
- toxicity content_pair + classification: `iter_1/gen_art/gen_art_dataset_3/full_data_out.json`

## Files
- `full_data_out.json` (5.3 MB), `mini_data_out.json` (3 examples/group), `preview_data_out.json`
  (truncated) — all schema-PASSED.
- `data_summary.json` — null-size tables, generation/re-judge stats, agreement/kappa, gate constants.
- `cc.py` (shared helpers, imports iter-1 `common.py` verbatim), `extract_originals.py` (Step 0),
  `build_first_letter.py` (Step 1), `gen_toxicity.py` (Step 2), `rejudge.py` (Step 3),
  `assemble.py` (Steps 4–5), `make_variants.py` (Step 6), `verify_superset.py`.
- `temp/intermediate/*.jsonl` — OpenRouter generate/judge/re-judge caches (re-runs cost $0).

## Reproduce
```
uv run extract_originals.py        # Step 0: ingest 590 + 546 originals verbatim
uv run build_first_letter.py       # Step 1: 590 -> 1,700 (deterministic, $0)
uv run gen_toxicity.py --target-accepted 1050   # Step 2: gpt-4o-mini gen + gate + claude judge
uv run rejudge.py                  # Step 3: confirmation + cross-judge agreement
uv run assemble.py                 # Steps 4-5: superset + data_summary.json
uv run make_variants.py            # Step 6: mini/preview
uv run verify_superset.py          # superset + byte-identical-originals audit
```
Pinned: `s-nlp/paradetox` (openrail++), `google/civil_comments` (CC0), `unsloth/gemma-2-2b`
tokenizer vocab 256000. Gate constants `jaccard_max=0.6`, `char_change_min=0.25`.
