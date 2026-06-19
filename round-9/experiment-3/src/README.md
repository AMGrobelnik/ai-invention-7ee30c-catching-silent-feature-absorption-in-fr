# M5'''' — Strengthen the KG-Repair Spine (iter-9 experiment_3, reviewer R5)

**Goal.** Close reviewer **R5** on the now-headline SAE-cluster **localization/repair spine**. The iter-4
result (69 repairs / 30 BH-FDR survivors across spelling L/O/T/I/D + homograph-taxonomic + numeric)
compared the **KG-named absorber** — selected by held-out per-sub-context **precision/recall** for covering
a parent "hole" X — against only a **weak single-random-latent control**, while *evaluating recovery of
recall on X*. R5: that is a near-definitional comparison that certifies naming self-consistency more than
repair utility. This experiment replaces that control with **strictly stronger, NON-eval-aligned controls**
and adds a **downstream-capability** test.

This is a **pure reuse / $0-LLM** experiment. `core.py` is the iter-4 `method.py` **verbatim** (output
dirs repointed); the SAE encodings are reused **verbatim** from the iter-4 disk cache, so we never re-run
gemma-2-2b. The JumpReLU SAE forward (encode/decode, decoder geometry) is reimplemented in **pure numpy**
from `params.npz`; the **gating check is computed from the cached layer-13 residuals** and reproduces the
iter-4 value exactly (cosine **0.9189**, L0 87.9).

## What was added

1. **Stronger, non-eval-aligned controls** (none ranked by per-sub-context precision):
   - **dense_jtt / dense_dom** — the decoder-projection argmax of a dense probe (JTT example-reweighted
     hyperplane and a plain diff-of-means hyperplane). The k-localization check confirms this argmax **is
     the parent/anchor** (`argmax_is_anchor=True`) → expected ~0 incremental recall.
   - **S_mag_global** — argmax mean content-response **magnitude** (label-free, parent-like).
   - **S_rec_global** — argmax content-flip **firing recall** (label-free, parent-like).
   - **S_mag_poolX / S_rec_poolX** — *same-pool-matched*: hold candidate eligibility **fixed** (the exact
     pool the KG argmax-recall selects from: jaccard<0.10, sub-context precision≥0.70) and vary **only the
     ranking criterion**. Singleton pools (`|pool|=1`, the absorber is unique) are flagged and **excluded
     from FDR** as structural, not inferential.
   KG-minus-control **paired bootstrap** (B=10,000) + one-sided p + an **augmented Benjamini-Hochberg FDR**
   over the hole×stronger-control family (cross-checked against `statsmodels`).

2. **Downstream-capability test** on the disjoint held-out fold: worst-sub-context recall of
   **(parent + KG absorber)** [2 SAE latents] vs **(parent + dense logistic probe)** [1 SAE latent + 1
   hyperplane, matched 2 components], paired bootstrap, plus the structural per-sub-context-handle from the
   k-localization logic and a dense-probe **selectivity** (false-positive-rate) report.

## Result (verdict fork)

```
overall = REPAIR_IS_NON_TAUTOLOGICAL_LOCALIZATION + DOWNSTREAM_CAPABILITY_NULL_TEMPER
```

- **Reproduction: 100%** — all 63 re-materialized KG absorbers match the iter-4 published spine exactly
  (taxonomic 31/31, numeric 8/8, L 3/3, O 10/10, T 11/11), so the strengthening runs on the *settled* holes.
- **Repair is non-tautological**: on **16/24** spelling+taxonomic holes the KG absorber **beats all four
  named non-eval-aligned controls at FDR≤0.05**. Per family: **homograph-taxonomic 3/3 clean (Georgia,
  Jordan, US; 0 controls competitive)**, spelling 13/21, **numeric honestly mixed 1/7** (on integer / year /
  currency / comma_number a stronger control *matches-or-beats* the KG absorber — the controls are genuinely
  non-trivial, not strawmen). The 8 spelling+tax non-wins are all **weak-gain holes** (gain_kg≈0) that tie
  *everything*, not control artifacts. Even strong label-free controls are real: `S_mag_global` recovers 45%
  of the Georgia hole, yet KG still beats it +0.35 (FDR).
- **precision_specific = False**: within the same eligibility pool, ranking by per-X precision is **not**
  strictly better than ranking by magnitude/recall — the win is *which latent localizes the sub-context*
  (coverage), not precision-magic. Emitted as honest temper (78 honest negatives, verbatim).
- **Downstream NULL_TEMPER**: the repaired unit does **not** out-recall a strong dense logistic probe
  (numeric −0.287, O −0.578, T −0.211, taxonomic −0.026, all CI-excl-0; L ties), so the demonstrated value
  is **auditable per-sub-context LOCALIZATION** (a handle the single dense hyperplane lacks —
  `argmax_is_anchor`, `single_latent_dominates=False`), **not** downstream recall utility. `metadata.verdict.
  temper_language` carries the exact tempering wording.

## Files

- `method.py` — this experiment (materialize iter-4 context from cache → stronger controls → strengthened
  repair → augmented BH → downstream → verdict fork → output).
- `core.py` — iter-4 `method.py` **verbatim** (output dirs repointed); source of the reused primitives
  (`content_responsive`, `derive_broad_kg`, `repair_loop`, `paired_bootstrap_diff`, `benjamini_hochberg`,
  `k_localization_check`, loaders, canonical units).
- `method_out.json` (+ `full_/mini_/preview_`) — `exp_gen_sol_out` schema, all validated. Datasets:
  `kg_repair_strengthened` (per hole×control row) and `downstream_capability` (per sub-context row).
- `cache/` — **symlinks** to the iter-4 cached encodings (not re-uploaded).

## Reproduce

```bash
uv venv .venv --python=3.12 && source .venv/bin/activate
uv pip install -r <deps in pyproject.toml>
python method.py --smoke      # gating-from-cache + taxonomic reproduction cross-check
python method.py              # full run (all concepts), ~155s, $0
```
