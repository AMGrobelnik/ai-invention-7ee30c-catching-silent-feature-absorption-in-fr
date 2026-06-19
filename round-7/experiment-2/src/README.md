# M2″ — Named-Entity Homograph Absorption Screen + Conditional Gated-Dense Downstream

**Confirmatory / supporting (NOT load-bearing).** Reuses the iter-5/iter-6 Gemma-Scope L12/16k engine
(`core.py`, `method_iter6.py`) verbatim except for one new edit operator and a gate-calibration primitive.

## Thesis under test
Feature **absorption = LEXICAL HOMOGRAPHY** — a *suppressed* parent latent (here "a named public figure or
organization") under a polysemous surface token — **NOT** safety / demographic semantics. Named-entity
homographs (Apple / Amazon / Bush / Cook / King) should show the **Georgia signature**; plain demographic
identity terms (iter-6) do not. The iter-6 demographic-attribute null (absorption is homograph-confined) is
**settled and unchanged** regardless of any named-entity outcome here.

## Two deliverables

### (A) `$0` SCREEN (primary) — `screen.py`
For each eligible named entity X, compute the Georgia absorption signature **non-circularly** (absorber chosen
on the diagnostic fit fold; every metric scored on the disjoint **train** eval fold):

| signal | meaning | structured gate |
|---|---|---|
| `recall_hole` | `1 − P(parent latent fires | X-positive)` | `> 0.5` |
| `firing_jaccard` | `J(parent, absorber)` over firing rows | `< 0.1` |
| `precision` | fraction of absorber-firing eval rows whose entity == X | `≥ 0.7` |
| `hole_coverage_gain` + bootstrap CI | recall recovered by OR-ing absorber into parent | `gain ≥ 0.05`, CI excl 0 |
| `oracle` (form-free) | **decoder–probe cosine** `cos(W_dec[absorber], d_p)` (Chanin/SAEBench, τ=0.025) + reported SAE-recon projection share | `cos ≥ 0.025` |
| `n_eligible` | diagnostic-fold positives | `≥ 150` |

A **known-positive self-check** runs the *identical* screen on Georgia (taxonomic, canonical absorber 16009)
and asserts it is flagged structured — proving the screen detects a real absorber, not noise.

### (B) Conditional gated-dense downstream (supporting) — `method.py`
For any absorption-structured named-entity case **and** Georgia (canonical non-safety positive control), at
**matched forget** (`0.8·min(maxKG,maxSUB)`):

| operator | edit |
|---|---|
| **KG-ABL** (ours) | ablate the KG-named absorber latent (gated by its own sparse firing) |
| **DENSE-SUB-ABL** | erase the sub-context diff-of-means `u_sub` (ungated; iter-6 comparator) |
| **DENSE-SUB-ABL-GATED** (NEW) | erase `u_sub` **only where** `h·u_sub > gate_thresh`, footprint-matched to the absorber |
| **DENSE-WHOLE-ABL** | erase the whole-parent diff-of-means (secondary reference) |

Decisive comparison **KG vs DENSE-SUB-ABL-GATED** on a paired-bootstrap joint (retain-utility × fluency)
LLM-judge CI (primary `anthropic/claude-haiku-4.5` + 2nd-family `openai/gpt-4o-mini`), with an
**edit-vs-NOOP forget delta** (median matched forget-KL + fraction-of-prompts-changed + judged forget
quality) so a "win" is only claimed where forgetting is non-trivial.

Per-case fork: `KG_BEATS_GATED_DENSE` / `KG_MATCHES_GATED_DENSE` / `GATED_DENSE_CLOSES_GAP` / `NEAR_NOOP_NO_WIN`.

## Verdicts
`overall_verdict = SAFETY_ABSORPTION_HOMOGRAPH_CONFINED` (demographic null unchanged) + secondary tag
`NAMED_ENTITY_HOMOGRAPH_WIN_FOUND` / `NAMED_ENTITY_STRUCTURE_NO_WIN` / `NO_NAMED_ENTITY_WIN`.

## Run
```bash
uv run method.py --smoke                                  # gating + token-locality (Apple-company ≫ apple-fruit), $0
uv run method.py --mini --no_downstream                   # 2-entity screen + Georgia self-check, $0
uv run method.py --gen_per_set 12                         # full screen + conditional downstream (<$2 judges, $10 cap)
```

## Files
- `core.py` — iter-5/6 engine (verbatim) **+** new `erase_dir_gated` operator and `calibrate_gate` primitive.
- `method_iter6.py` — iter-6 driver (reused helpers: `build_u_sub`, judge infra, generation, curve dominance,
  `setup_taxonomic` for the Georgia control) **+** gate-threading.
- `screen.py` — the `$0` named-entity absorption screen + Georgia self-check (NEW).
- `method.py` — orchestration: gating → screen → conditional gated-dense downstream → verdicts → output (NEW).
- `method_out.json` — results (`metadata.screen_table`, `breadth_count`, `georgia_sanity`, `downstream`,
  `overall_verdict`, `secondary_tag`, `honest_negatives`); `full_/mini_/preview_` size variants.

`$0` for the screen; downstream LLM judges target `<$2`, hard cap `$10`. GPU (single RTX 4090).
