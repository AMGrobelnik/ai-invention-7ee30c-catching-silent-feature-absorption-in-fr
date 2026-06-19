# M1′′′′′ — Averted-Cost Auditing Scenario

**Claim.** The iter-9 label-free absorption screen (`screen.py`) is not just a *reassurance* that
"absorption is confined" — it is an *actionable* reliability tool with a **measured averted cost**.
We ship two downstream artifacts a practitioner would actually build on top of frozen Gemma-Scope SAE
latents — a parent-concept **classifier** and a parent-concept **steering handle** — both selected by
SAEBench **SCR/TPP marginal-attribution** over the SAE latents (the standard raw-latent practice), and
show end-to-end:

| step | evidence |
|------|----------|
| **(a) silent failure** | absorption drops the absorber out of the compact top-N selection → the shipped artifact has a recall / steer **hole on the absorbed slice** (Georgia / Amazon / large) vs non-absorbed sibling slices |
| **(b) standard practice misses it** | the absorber is buried **deep in the SCR/TPP attribution ranking** (Georgia rank 42, Amazon rank 14 — far below a compact top-N) **and** the form-free decoder-projection oracle scores Georgia **clean** (decoder-cos −0.024, \|·\|<0.025) |
| **(c) the screen catches it** | the shipped label-free firing-signature screen flags `ABSORPTION_STRUCTURED` (recall_hole>0.5, firing-disjoint absorber) and **names the latent** — zero sub-context labels |
| **(d) named-absorber repair** | adding the screen-named absorber repairs the artifact with a **KG-minus-baseline CI excluding 0** and no meaningful sibling degradation |

## Baselines (reviewer-required)
- **raw SAE latents** — the SCR/TPP top-N classifier **and** the single parent latent (both carry the hole).
- **non-SAE** — a dense **diff-of-means parent probe** on the residual (`core.ParentProbe`). It generally has
  **no** slice hole → the hole is an *SAE-selection artifact*, and the named-absorber repair recovers the
  **compact, auditable** SAE unit to match the dense baseline while staying sparse/interpretable.
- **our unit** — `parent latent + screen-named absorber`, a human-auditable **2-member group**.

## Key finding — the cost is the *compactness* you give up
Absorption bites exactly the **compact, human-auditable** classifiers (the units the reviewer asks for):
at selection size k∈{1,2,5} the Georgia/Amazon country/org sense is silently missed (recall ≈0.1 vs ≈0.96
on siblings); the named absorber repairs it to ≈1.0. With a *larger, less-auditable* ensemble (k≥10) the
hole closes on its own — so the **averted cost = the extra raw latents (less auditability) you would need,
or the hole you would ship,** if you did not know the one named absorber. The full **N-curve** is reported
per arm (`by_N`, `n_curve`, `hole_closes_at_N`).

## Arms & FORK
Per arm: `AVERTED_COST_DEMONSTRATED` iff (hole real, CI excl 0) ∧ (absorber not in top-N) ∧ (screen flags +
names it) ∧ (repair CI excl 0) ∧ (no sibling collateral beyond a magnitude tolerance). Else the matching
honest null verbatim: `HN_NO_HOLE` / `HN_SCREEN_MISS` / `HN_REPAIR_NULL` / `HN_SIBLING_COLLATERAL`.
- `georgia_classifier` (taxonomic, **primary**; oracle-blind), `amazon_classifier` (named-entity; oracle works),
- `amazon_steer`, `large_steer` (steering handles with full **side-effect** measurement: KL / PPL / token-
  footprint on unrelated text vs a firing-rate-matched shuffle null).

## Files
- `method.py` — the new driver (SCR/TPP selector + per-slice recall/steer harness + averted_cost_table + FORK).
- `core.py`, `screen.py`, `m9.py` — reused **verbatim** from iter-4..9 (SAE engine + edit operators; the
  shipped label-free screen; family builders + `screen_candidate`). Only `WORK` was repointed.
- `probe.py` — one-off diagnostic that chose the canonical absorber + the N-grid (kept for provenance).
- `method_out.json` / `full_/mini_/preview_` — the `exp_gen_sol_out` deliverable (datasets
  `averted_cost_per_slice`, `averted_cost_per_case`).
- `cache/enc_*.npz` — cached SAE encodings reused from iter-9 (excluded from upload).

## Reproduce
```bash
# single L4/Ada-class GPU, ~12 GB; torch 2.6+cu124
HF_HUB_OFFLINE=1 .venv/bin/python method.py --smoke   # Georgia classifier, tiny
HF_HUB_OFFLINE=1 .venv/bin/python method.py --mini    # Georgia + Amazon classifiers, full eval fold
HF_HUB_OFFLINE=1 .venv/bin/python method.py           # full: + Amazon/large steer + side-effects ($0)
HF_HUB_OFFLINE=1 .venv/bin/python method.py --judge   # + optional Amazon-steer LLM-judge spot-check (<$1)
.venv/bin/python make_variants.py method_out.json     # full/mini/preview
```
SAE: `google/gemma-scope-2b-pt-res` `layer_12/width_16k/average_l0_82` on `google/gemma-2-2b`
(`blocks.12.hook_resid_post`). Core measurement is **$0** (model-internal); the judge is optional and
capped (`--judge`, hard $10 ceiling, auto-stop near $1).

## Honest negatives (carried)
See `metadata.honest_negatives` — the oracle is concept-tuned (blind to taxonomic Georgia); firing-signature
≠ edit-handle; the dense probe matches/beats raw latents (the repair is SAE-artifact-specific); absorption is
homograph/named-entity-confined (iter-9 STRICT 6/110); the multi-member *clustering* hypothesis did not pay
off — the shipped value is the label-free WHERE-screen + the named-absorber 2-member repair unit.
