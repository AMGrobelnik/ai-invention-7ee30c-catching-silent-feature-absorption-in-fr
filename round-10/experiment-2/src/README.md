# Label-Free SAE Absorber Catalog (Gemma-Scope-2b suite)

A reusable, **label-free** catalog of feature-absorption structure across a public Gemma-Scope-2b SAE suite — **{16k, 65k} widths × {layer 9, layer 12}** — on gemma-2-2b. One row per *(candidate token × SAE config)* with the full model-internal absorption signature and a verdict in `{ABSORPTION_STRUCTURED, CO_FIRING, NO_HOLE, DESCRIPTIVE_ONLY}`. Built by re-running the shipped iter-9 screen (`screen.py`) over four frozen SAE dictionaries.

## Files

| file | role |
|---|---|
| `catalog.csv` | flat: one row per (candidate × config), all signature columns. |
| `catalog.json` | nested: config → hierarchy → rows. |
| `screen.py` | the shipped label-free screen (signature engine + form-free oracle + CLI). |
| `method.py` | the multi-config catalog driver (this experiment). |
| `core.py` / `m9.py` | SAE+model infra and the iter-9 builders, reused. |
| `method_out.json` | full machine-readable results (coverage, stability, controls). |

## Headline findings

- **Exact reproduction**: the 16k/L12 config reproduces the iter-9 screen bit-for-bit (336/336 rows match on predict + absorber id).
- **Layer effect is strong**: absorption is much more prevalent at the *earlier* layer 9 than at layer 12 — strict-structured counts rise 6→15 (16k) and 3→29 (65k) going L12→L9.
- **Width effect**: wider SAEs surface *more* absorption breadth — pooled relaxed-structured 31→62 (L12) and 52→58 (L9) going 16k→65k; 9/10 hierarchies have `65k ≥ 16k` at L12.
- **Stability**: of 131 tokens structured somewhere, only **8 are PERSISTENT** (≥3 configs; e.g. `Amazon`, `Jordan` in all four) while **69 are CONFIG_SPECIFIC** — absorption is mostly dictionary-dependent, so a latent's reliability must be checked *per SAE*.
- **Human-auditable labels**: every absorption-structured row carries the Neuronpedia auto-interp description of its parent + absorber latent (e.g. the `light` absorber → "references to light and illumination contexts").

## The label-free derivation (per candidate token X, per SAE config)

1. **Content-responsive eligibility** — candidate absorber latents are those that respond to the concept on content-flip minimal pairs (sign-flip null, no labels).
2. **Parent latent (anchor)** — the highest content-flip `x_on` recall latent that clears a corpus firing floor (the shared-concept detector). KG4 ids on 16k/L12 for reproduction; **data-derived everywhere else** (label-free).
3. **Recall-hole** — `1 − P(parent fires | X-positive rows)` on held-out rows (> 0.50 ⇒ the parent is suppressed on X).
4. **Absorber** — a content-responsive latent that is firing-disjoint from the parent (firing-Jaccard < 0.10), precise for X (≥ 0.70), and covers the parent's holes; the **hole-coverage gain** (recall recovered by OR-ing the absorber into the parent) must be ≥ 0.05 with a 5000-sample bootstrap CI excluding 0.
5. **Verdict** — `ABSORPTION_STRUCTURED` (strict, all hold + ≥150 positives) / `relaxed` (firing conditions hold, <150 positives) / `CO_FIRING` / `NO_HOLE` / `DESCRIPTIVE_ONLY`.

The form-free decoder-projection **oracle** (Chanin App. A.13 / SAEBench `absorption_fraction`) is **corroboration only** — it needs a dense parent-probe direction fit on a disjoint fold, is never used to flag, and under-fires for the taxonomic 'country' direction (documented).

## Configs run

| config | layer | width | avg L0 | SAE id | FVU | candidates | structured (strict / relaxed) | pooled-strict |
|---|---|---|---|---|---|---|---|---|
| 16k_L12 | 12 | 16k | 82 | layer_12/width_16k/average_l0_82 | 0.1926 | 336 | 6 / 31 | 6/110 |
| 65k_L12 | 12 | 65k | 72 | layer_12/width_65k/average_l0_72 | 0.17 | 336 | 3 / 62 | 3/110 |
| 16k_L9 | 9 | 16k | 73 | layer_9/width_16k/average_l0_73 | 0.2346 | 336 | 15 / 52 | 15/110 |
| 65k_L9 | 9 | 65k | 118 | layer_9/width_65k/average_l0_118 | 0.1661 | 336 | 29 / 58 | 29/110 |

## Cross-config stability

- tokens catalogued: **336**; structured in ≥1 config: **131**.
- stability classes: `{"NONE": 205, "CONFIG_SPECIFIC": 69, "LAYER_SPECIFIC": 3, "MIXED": 40, "WIDTH_SPECIFIC": 11, "PERSISTENT": 8}` (PERSISTENT = structured in ≥3 configs; WIDTH_SPECIFIC = both L12 widths only; LAYER_SPECIFIC = both 16k layers only; CONFIG_SPECIFIC = exactly one config).

- **wider width → ≥ absorption** (pooled relaxed): 16k/L12 = 31 vs 65k/L12 = 62 (wider ≥: True).

## 16k/L12 reproduction

Exact re-run of iter-9 from cached encodings: 336/336 rows match on (predict, absorber) (predict match 1.0, absorber match 1.0). iter-9 pooled-strict 6/110.

## Caveats / failure modes (reported honestly)

- Absorber LATENT IDs are dictionary-specific and CANNOT be matched across width/layer; cross-config stability is therefore measured at the (hierarchy, token) STRUCTURED-FLAG level, not by id equality.
- The form-free decoder-projection oracle is concept-tuned: it corroborates lexical/named-entity homograph absorbers but UNDER-fires for the taxonomic 'country' direction (Georgia's decoder is near-orthogonal to the generic country direction) -> it is corroboration-ONLY, never gates the flag.
- On 16k/L12 the catalog uses the KG4 anchors for spelling/taxonomic (reproduction) AND records the fully data-derived anchor + agreement; all other configs use data-derived anchors everywhere so the published catalog is genuinely label-free-derivable.
- Spelling word-types have <150 corpus positives so their coverage is the RELAXED breadth number, not the STRICT inferential one.
- A clean structured firing-signature need not be a meaningful single-latent EDIT handle (carried iter-8 finding); the catalog flags absorption STRUCTURE, not editability.
- Neuronpedia auto-interp labels are an OPTIONAL free enrichment; the catalog is complete without them.

## Reproduce
```
python method.py --smoke   # 16k/L12 spelling-L from cache
python method.py --mini    # 2 configs x 4 hierarchies
python method.py           # full: 4 configs x 10 hierarchies
```
$0 LLM. Single GPU (gemma-2-2b bf16 + one SAE).
