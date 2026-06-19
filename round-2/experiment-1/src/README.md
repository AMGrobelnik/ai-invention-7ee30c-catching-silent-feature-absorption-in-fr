# Two-Track CCRG — First-Letter Spelling Primary Endpoint (E1/E2/C1 + Admission + Steering)

**Artifact:** `experiment_iter2_dir1` (GPU). Runs the two-track **Counterfactual Co-Response Grouping
(CCRG)** method on a *frozen* Gemma-Scope layer-12 / width-16k JumpReLU SAE over the pre-built
first-letter spelling absorption testbed, and decides the **primary falsification endpoint**.

The idea: single SAE latents are unreliable (feature **absorption / splitting** — the "starts-with-L"
concept fragments into a general parent latent plus many per-word absorber latents). CCRG groups latents
into **cluster-level units** (an *anchor* + disjoint-support *absorbers*) using only content-flip
co-response, with **no concept labels**, and asks whether such units are more reliable than raw latents
and than non-SAE / oracle baselines on concrete downstream tasks.

Core LLM spend = **$0** (everything is code; the diagnostic is the form-free probe-projection).

---

## How to run

```bash
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python torch==2.6.0 --index-url https://download.pytorch.org/whl/cu124
uv pip install --python .venv/bin/python transformers==4.46.3 accelerate scikit-learn scipy \
    statsmodels leidenalg igraph pandas "huggingface_hub<1.0" sentencepiece safetensors

# smoke (loads model+SAE, runs the reconstruction GATING CHECK only):
HF_TOKEN=$HF_TOKEN .venv/bin/python method.py --smoke --out smoke_out.json
# full run (all 5 letters + steering, ~8 min on an RTX 4090):
HF_TOKEN=$HF_TOKEN .venv/bin/python method.py --letters L,O,T,I,D --b_gap 10000 --b_null 1000 --out method_out.json
```

Data is read from the sibling dataset artifact (`gen_art_dataset_1/full_data_out.json`, first-letter
spelling testbed). Model = `unsloth/gemma-2-2b` (non-gated mirror). SAE = Gemma-Scope
`layer_12/width_16k/average_l0_82` (the "canonical" L0≈100 variant), loaded directly from `params.npz`
(no `sae_lens`/`transformer_lens`, to avoid version conflicts with `transformers` 5.x).

**Gating check (must pass before any analysis):** SAE reconstruction cosine **0.924**, explained-variance
**0.857**, L0 **95.9**, and corpus token-id localization exact (0/64 mismatches) — confirms the layer-12
residual hook and word-token positions match what the SAE was trained on.

---

## Method (pipeline per letter)

1. **Content-response matrix.** For each on-word *w* (starts-with-L) and a surface-matched off-word, read
   SAE activations at the word token under spelling carriers (`t_verbose`,`t_colon`,`t_icl`); `r_l(w) =
   a_l(on) − a_l(off)`.
2. **Eligibility (`Lr`).** A latent is eligible iff it is *selective* (firing-precision ≥ 0.7: fires on
   on-words not off-words) **and** covers ≥1 sub-context with net-positive response. (A mean-over-words
   prefilter rejects sparse absorbers — they fire on only 1–5 words — so we use this cover-based rule.)
3. **C-track (splitting).** Spearman co-response affinity → signed soft-threshold (β=6) → Leiden
   `RBConfigurationVertexPartition` (run in a **subprocess with a 45 s timeout** because Leiden's C
   extension intermittently hangs on pathological tied-rank graphs; falls back to agglomerative on
   correlation distance).
4. **K-track (absorption) — E1 core.** Anchor = highest-cover-set latent (chosen from pairs only, never
   the diagnostic). Then **anchored greedy max-coverage**: repeatedly add the precise (≥0.7),
   anchor-disjoint (firing-Jaccard < 0.1) latent covering the most uncovered hole sub-contexts.
5. **Form-free diagnostic (oracle, non-circular).** Train a parent-concept probe `d_p` on *disjoint*
   corpus windows; parent latent = max encoder-cosine with `d_p`; absorber for a false-negative word =
   firing latent with `(â_l·d_p)/(a·d_p) > 0.5` (the paper's Appendix-A.13 / SAEBench
   `absorption_fraction`). **Used only to score the K-track unit, never to form it.**
6. **Baselines** (count-matched to *k* = |unit|): (a) best raw latent, (b) co-firing HDBSCAN/agglomerative
   cluster, (c) decoder-cosine cluster, (h) count-matched oracle SCR/TPP attribution pool
   `|d_p·W_dec|·mean_act`; plus oracle pools g10/g20 (larger references).
7. **Admission (Step 5).** (sigC OR sigK) AND surface-invariance, with BH/Holm multiplicity and an
   empirical false-admit rate under the matched random-k null.
8. **Steering (run last).** mean-member-decoder direction vs hub (best single member) vs non-SAE
   diff-of-means, compared at **matched on-target** effect on full-vocab KL + PPL collateral.

---

## Results (verdict: `primary_endpoint = WORKS`)

| Letter | C1 AUC unit / (a,b,h) | E1 F1 (pass) | E2 sliced unit vs h (sig) | Steering unit-best | Admission false-admit |
|--------|----------------------|--------------|----------------------------|--------------------|-----------------------|
| **L**  | **0.905** / .848,.864,.794 | 0.308 ✔ | .808 vs .767 (cm-win) | ✔ (KL 16.4 vs 27.9/30.4) | 0.087 |
| **O**  | **0.917** / .633,.808,.821 | 0.300 ✔ | .808 vs .717 (cm-win) | ✘ | 0.040 |
| **T**  | **0.859** / .667,.774,.648 | 0.263 ✔ | **.925 vs .763 ✔ (CI excl 0)** | ✘ | 0.067 |
| **I**  | **0.961** / .548,.662,.833 | 0.208 ✘(anchor) | **.775 vs .496 ✔ (CI excl 0)** | ✘ | 0.040 |
| **D**  | **0.956** / .711,.665,.726 | 0.381 ✔ (7 absorbers) | .810 vs .676 (cm-win) | ✔ (KL 28.6 vs 33.3/30.4) | 0.033 |

**Headline finding — C1 classification:** the label-free co-response **unit is the best
starts-with-letter classifier on all 5 letters**, beating the raw best latent (a), co-firing clusters
(b/c), and the **count-matched oracle-attribution pool (h)** — including cases where every individual
baseline is far worse (I: 0.961 vs ≤0.833). This is the load-bearing positive: cluster-level units are a
more reliable unit of analysis than single latents.

**E1 (label-free absorption recovery):** the K-track recovers the diagnostic parent + ≥2 absorbers above
the random-membership null on **4/5 letters**. The units are **human-auditable**, e.g. for **L**:
anchor 205 (logit-lens `Lohan/Ls/LS/LF/LK`) + absorbers 3069=`list`, 2416=`line`, 8463=`large`,
4736=`l…ing`; for **D**: anchor 6210 (`PhysRevD/DPR/DSS`) + 1970=`different`, 7293=`director`,
10769=`day`. A directed specialization knowledge-graph (anchor → absorbed_child(word)) is emitted in
`metadata.kg_edges` (70 edges).

**E2 (absorbed-slice recall):** the unit beats all **count-matched** baselines (h, b, c) directionally on
every letter and **significantly** (paired-bootstrap CI excludes 0) on T and I. The larger oracle pool
g20 is competitive — see the honest caveat below.

**Steering:** the mean-member-decoder unit has the lowest side-effect (KL) at matched on-target effect on
the primary letter **L** and on **D**; on O/T/I a non-SAE diff-of-means or the hub is more surgical
(steering is a generality demo, not load-bearing — reported honestly).

---

## Honest failure modes / caveats (reported, not hidden)

- **The recovered-absorber COUNT metric is `d_p`-circular for the oracle baselines.** The diagnostic
  *defines* absorbers via the probe direction `d_p`, and baselines g/h *rank* by `|d_p·W_dec|·mean_act`
  — both keyed on the same oracle direction, so g/h trivially overlap the diagnostic (g20 "recovers"
  10–16 vs the unit's 4–7). We therefore base the E2 verdict on the **non-circular** downstream metrics
  (C1 classification, count-matched sliced recall), and report the count as descriptive with this caveat
  (`metadata.per_letter.*.E2.recovered_count_caveat`).
- **E1 anchor-fidelity fails on I.** The highest-cover-set latent (1227) fires 0% on the corpus and has
  code-token logit-lens — it is a spurious anchor, not the semantic parent. The greedy anchor heuristic
  is not always the concept parent; yet the pooled unit is still the best classifier (C1 0.961).
- **C-track is secondary and Leiden hangs intermittently** on certain bootstrap-resampled tied-rank
  graphs; the subprocess+timeout falls back to agglomerative clustering for L/O (recorded as
  `gamma="agglo_fallback"`). The headline (K-track / E1 / C1) does not depend on the C-track.
- **Within the eligible set `Lr`, random k-latent pools also classify well** (`frac_randk_gain_gt_0.05`
  ≈ 0.92–1.0): the admission's discriminative power comes from surface-invariance + the 95th-pct sigK
  test (empirical false-admit 0.03–0.09), not from pooling per se.

---

## Output (`method_out.json`, `exp_gen_sol_out`-schema-valid)

- `metadata` — all metrics: `verdicts`, `config`, `gating_check`, per-letter `E1/E2/C1/admission/c_track`
  (with paired-bootstrap CIs, exact McNemar, Holm/BH multiplicity, threshold-sensitivity sweep),
  `steering` (on-target/KL/PPL curves + matched comparison + random-direction null), `unit_definitions`
  (members, logit-lens tokens, top corpus contexts), `kg_edges` (specialization graph), `runtime_stats`.
- `datasets` — per-letter held-out (test-fold) content instances with `input`, `output` (1 = starts with
  target letter), and per-method predictions `predict_unit / predict_a / predict_b / predict_c /
  predict_h` for the downstream solution-evaluation step.

## Files
- `method.py` — full pipeline (model+SAE load, gating, two-track CCRG, diagnostic, baselines, E1/E2/C1,
  admission, steering, output).
- `method_out.json` — results (0.39 MB, schema PASSED).
- `logs/final.log` — full run log (per-letter timings + metrics).
