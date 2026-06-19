# iter-8 — Base-Widener + Concentration-vs-Absorption Population Test (M2‴ / M3‴ / M5‴)

The iter-8 decisive control for the auditability-first two-track **Counterfactual Co-Response Grouping
(CCRG)** units. iter-7 found that ablating ONE KG-named SAE **absorber latent** (KG-ABL) beats a
footprint-matched gated-dense control at meaningful forget — but only for the spelling word `large`, while the
distributed country senses `Georgia`/`Jordan` could not forget at all. iter-8 asks three questions over a
**wide** candidate vocabulary, with a **stronger, fairer** dense control:

- **M2‴ (base width).** Screen a wide vocabulary (spelling word-absorbers L/O/T/I/D + homograph entities:
  brands / given-names / months / cities) and count how many clear the fair-control bar at **meaningful
  forget** → `BASE_REACHES_4_PLUS` vs `BASE_STAYS_THIN_RETARGET`.
- **M3‴ (predictor).** Does a candidate's **continuous lexical-CONCENTRATION** score predict its edit
  outcome **better than** its **binary absorption-regime** label? (the decisive population evidence).
- **M5‴ (set-cover inertness).** Per candidate, does the anchored precision-selected absorber **equal** the
  unconstrained max-precision latent? (if yes for most → the K-track set-cover step is inert).

## The UNIFIED fair operator (the only new edit code)

Added to `core.make_edit_hook` as `kind='erase_dir_gated_fair'`:

```
DENSE-SUB-ABL-GATED-FAIR :  h ← h − min(β,1)·(h·u_sub)·u_sub   applied ONLY where d_sub(h) > gate_thresh
```

- `u_sub` = the **labeled** sub-direction (diff-of-means target-sub vs sibling, disjoint fit fold).
- `d_sub` = a **precise supervised** sub-probe (logistic, AUC≈1.0) that decides **WHERE** to erase.
- `β ≤ 1` (bounded) — at most a full removal of the labeled component at the detected tokens.

vs iter-7's `erase_dir_gated`, which gated on a **crude** projection-magnitude `|h·u_sub|>τ` calibrated to a
3 % global footprint, forcing **β≈3 over-erasure**. The new operator removes that handicap → the genuinely
**fair** conditional-dense control (labeled direction + precise where-to-edit, no over-erasure). The decisive
per-candidate comparison is **KG-ABL vs DENSE-SUB-ABL-GATED-FAIR** (with the ungated DENSE-SUB-ABL as the
lead secondary comparator and MAX-PREC-ABL for the set-cover test).

## Concentration score (the M3‴ predictor)

The plan's literal firing formula `precision·(1−footprint)` **saturates** (~0.98 for every candidate that has
*any* precise sparse latent — see `metadata.honest_negatives`), so it is reported only as the secondary
`concentration_firing`. The **primary** `concentration_score` is the **$0 analytic forget-capture fraction**:

```
concentration = mean_X( z_absorber · (W_dec[absorber] · w_dsub) ) / mean_X( d_sub margin )
```

i.e. the fraction of the average target context's frozen-sub-probe margin removed by ablating the single
absorber once. High ⇒ the sub-context's detectable signal is **concentrated** in one latent (editable, like
spelling `large`); low ⇒ **distributed** across many latents (country `Georgia`/`Jordan`). This discriminates
the editable from the non-editable populations that the firing statistics cannot.

## Pipeline (`method.py`)

1. **Reuse** `core.py` / `method_lib.py` (verbatim copies of the iter-7 engine, `WORK` repointed here) for the
   SAE pipeline, edit operators, judges, `u_sub` / `d_sub`, and the $0 meaningful-forget proof.
2. **Candidate pool ($0):** spelling words (curated ∪ KG4 sub_by_absorber, ≥12 windows) + homograph entities
   (rebuilt from the iter-5 builder via `homograph_data/pipeline.py --scale full --no-llm`; eligible ≥150 diag
   positives or curated) + the distributed-absorption anchors `Georgia`/`Jordan`.
3. **Concentration screen ($0):** per candidate compute precision, coverage, neutral footprint, the anchored
   K-track absorber, the unconstrained max-precision latent, recall-hole, firing-Jaccard,
   `absorption_structured` (reported, never gates), `set_cover_eq_max_precision`, and the capture-concentration.
4. **Budget-bounded edit loop:** most-concentrated-first (after the load-bearing anchors `large`/`Georgia`/
   `Jordan`). For each: build `u_sub`/`d_sub`, sweep KG-ABL / DENSE-SUB-ABL / DENSE-SUB-ABL-GATED-FAIR /
   MAX-PREC-ABL, find the **matched meaningful-forget** point on the **behavioral** sub-probe-drop curve, prove
   meaningful forget ($0: sub-probe drop + templated completion-accuracy drop), then judge the **joint**
   (fluency × content) at the matched point with **two** OpenRouter judges and a paired bootstrap (B=10000).
5. **Verdict / population / set-cover:** base win count; `spearman(concentration, Δjoint)` &
   point-biserial(absorption, ·) with bootstrap CIs (decide CONCENTRATION_PREDICTS vs ABSORPTION_PREDICTS);
   set-cover inertness rate.

## Config

- SAE: `google/gemma-scope-2b-pt-res`, `layer_12/width_16k/average_l0_82` (JumpReLU, d_model 2304).
- Model: `google/gemma-2-2b` (bf16, eager); edit + read at `blocks.12.hook_resid_post` (gating cosine
  **0.919**, L0≈88, layer_idx 13). Single GPU (NVIDIA L4, 23 GB). `$0` model-internal; LLM judges
  `anthropic/claude-haiku-4.5` (primary) + `openai/gpt-4o-mini` (second), target < $3, hard cap $10.

## Run

```bash
uv run method.py --smoke                              # gating + screen + operator, judges off, $0
uv run method.py --mini --families spelling,taxonomic # 5 cands, both judges, reduced prompts
uv run method.py                                       # full screen (all families) + budget-bounded edits
```

## Outputs

- `method_out.json` (`full_/mini_/preview_` variants via `make_variants.py`, each < 100 MB, validated against
  `exp_gen_sol_out`):
  - `metadata` — gating, fair-gate spec, judge spend, `concentration_screen_table` (per-candidate),
    `base_count` (`known_wins`/`new_wins`/`total_independent_concentrated_wins`/`verdict`),
    `population_predictor` (spearman + point-biserial CIs + `predictor_verdict`), `set_cover_inertness_rate`,
    per-candidate `edit_results` (sub-drop curves, matched point, joint deltas + CIs, fork status),
    `honest_negatives`.
  - `datasets`: **`concentration_screen`** (one row / candidate; tag = outcome) and **`edit_predictions`**
    (one row / (candidate, role, prompt) carrying the five `predict_*` continuation strings).
- `homograph_data/` — the rebuilt homograph testbed (builders + `full_data_out.json` + `manifest.json`).
- `logs/` run logs; `cache/` encodings (EXCLUDED from upload).

<!-- HEADLINE_RESULTS -->
