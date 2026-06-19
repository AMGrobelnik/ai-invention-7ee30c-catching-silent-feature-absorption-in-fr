# Label-Free SAE Absorption-Coverage Screen (`screen.py`)

A reusable, **label-free** practitioner tool that decides — for any candidate token on any frozen
sparse-autoencoder (SAE) — *whether the parent concept is suppressed and re-encoded by a single,
mutually-exclusive "absorber" latent* (the feature-absorption signature of Chanin et al. 2024, first
documented on first-letter spelling and on the country "Georgia").  It turns the qualitative question
"can absorption happen here?" into a screenable, CI-quantified **coverage** number per concept hierarchy.

This is the shipped deliverable of experiment **M3''''**.  `method.py` runs it over a wide
multi-hierarchy candidate pool to produce the coverage table; `screen.py` is the standalone module +
CLI.

---

## Why this exists

Single SAE latents are unreliable units (feature absorption, splitting, non-atomicity).  Absorption is
the sharpest failure: the general parent latent (e.g. *is-a-country*, *starts-with-L*) goes **silent** on
a specific token, whose signal is *absorbed* into a token-specific latent.  Practitioners need to know
**where** this happens before trusting a latent as a classifier or steering target — *without* gold
labels or an oracle.  This screen answers that from raw text + a frozen SAE alone, and reports the
fraction of candidates in a hierarchy that are absorption-structured, with confidence intervals.

---

## The verdict (`predict_absorption`)

Each candidate token gets exactly one of:

| label | meaning |
|---|---|
| `ABSORPTION_STRUCTURED` | parent recall-hole is large **and** a firing-disjoint, precise absorber covers the hole (bootstrap-CI-positive gain) **and** the token has ≥150 positives (inferential). |
| `CO_FIRING` | a recall-hole exists but no clean mutually-exclusive absorber — the sub-attribute *co-fires* with the parent (not absorption-structured). |
| `NO_HOLE` | the parent fires on the token like on its siblings — no suppression. |
| `DESCRIPTIVE_ONLY` | fewer than 150 positives — reported for breadth, **not** for an inferential claim. |

### The signature (all model-internal, label-free)

For candidate token *X* with parent latent *p* (the shared-concept detector):

- **recall-hole** `= 1 − P(p fires | X-positive rows)` — is the parent suppressed on *X*?  (> 0.50)
- **absorber** = a content-responsive latent that, on the fit fold, is **firing-disjoint** from *p*
  (firing-Jaccard < 0.10), **precise** for *X* (≥ 0.70), and **covers** the parent's holes (max coverage).
- **precision** = fraction of absorber-firing held-out rows whose sub-context is *X* (≥ 0.70).
- **hole-coverage gain** = recall recovered on held-out *X* rows when the absorber is OR-ed into the
  parent, with a 5000-sample bootstrap CI that must **exclude 0** (≥ 0.05).
- **n_eligible** = number of fit/diagnostic-fold *X*-positive rows; ≥ 150 for the STRICT gate.

`ABSORPTION_STRUCTURED` (strict) = all five hold.  `relaxed` = the five firing conditions hold but
n_eligible < 150 (used for breadth coverage of small candidates such as spelling word-types).

---

## Label-free guarantee

The four-way flag uses **only model-internal firing statistics** computed from a frozen SAE on raw text:
recall, firing-Jaccard, firing-precision, and hole-coverage gain.  It uses **NO** diagnostic probe, **NO**
Chanin absorption diagnostic, and **NO** sub-context labels to *flag*.

The optional form-free **decoder-projection oracle** (`absorption_fraction_oracle`, SAEBench /
Chanin App. A.13) is **corroboration only**.  It needs a dense parent-probe direction `d_p` fit on a
**disjoint** fold (never a single latent; never used to flag).  It is concept-tuned: it confirms
lexical / named-entity homograph absorbers strongly, but **under-fires for taxonomic concepts** (Georgia's
decoder is near-orthogonal to the generic "country" direction), so it must **not** gate the structured
flag — agreement is therefore reported separately for lexical vs taxonomic hierarchies.

---

## Inputs / Outputs

`screen_token(sae, mb, token, x_windows, sibling_windows, compute_oracle=True)`

**Inputs**

- `sae` — a frozen SAE (`core.load_sae`), e.g. Gemma-Scope `layer_12/width_16k`.
- `mb` — a `core.ModelBundle` (gemma-2-2b) with the residual hook installed.
- `token` — the candidate surface token (e.g. `"Georgia"`, `"large"`, `"Amazon"`).
- `x_windows` — list of `{"input": "<text containing the token in its target parent sense>", "span"?: [s,e]}`.
- `sibling_windows` — list of `{"input": "<window of another member of the same parent concept>"}` —
  the precision denominator (e.g. for `"Georgia"`, windows mentioning other countries).

**Output** — a flat dict:

```
{ predict_absorption, absorption_structured_strict, absorption_structured_relaxed,
  recall_hole, firing_jaccard, precision, hole_coverage_gain, gain_ci_lo, gain_ci_hi,
  absorber_latent, parent_latent, oracle_decoder_cos, oracle_absorption_fraction, oracle_corroborates }
```

- `parent_latent` (optional) — pin the parent/concept latent id (e.g. from Neuronpedia or a probe). If
  omitted, the parent is identified **unsupervised** as the highest-recall latent over the *sibling*
  windows (independent of the candidate). The unsupervised heuristic is honest but conservative: when a
  concept's broadest co-detector also fires on the absorbed token it reports `NO_HOLE`. Pin the parent to
  reproduce the rigorous coverage-table result.

### CLI

```bash
# unsupervised parent (conservative):
python screen.py --token Georgia --windows windows.jsonl --siblings siblings.jsonl
# pinned parent latent (rigorous; reproduces the coverage table):
python screen.py --token Georgia --windows windows.jsonl --siblings siblings.jsonl --parent_latent 3792
# windows.jsonl / siblings.jsonl : one JSON object per line: {"input": "...text..."}  (optional "span":[s,e])
```

Worked example (shipped `example_windows_georgia.jsonl` + `example_siblings_countries.jsonl`, parent 3792):
`predict_absorption = ABSORPTION_STRUCTURED`, recall_hole 0.76, precision 1.0, absorber latent **16009**
(the canonical Georgia absorber), oracle_corroborates True.

---

## Worked examples (reproduced by `method.py`)

**Positives** (flag structured):

- `large` — first-letter-spelling L (the parent "starts-with-L" latent is suppressed; a `large`-specific
  latent re-encodes the spelling).  RELAXED-structured (n_eligible < 150 — spelling word-types are small).
- `Georgia` — taxonomic country (canonical absorber latent 16009).  STRICT-structured via the firing
  signature; the decoder oracle under-fires (documented).
- `Amazon`, `Apple`, `March`, `June` — homograph entities (brand / month) with a strong competing sense.

**Negatives** (NOT structured → `CO_FIRING` / `NO_HOLE`):

- Most cities (`Paris`, `Florence`, `Columbus`…), most brands, most given-names.
- Demographic safety groups (nationality / religion / ethnicity): predominantly `CO_FIRING` — absorption
  is **homograph-confined**, so absorption need not be feared for demographic attributes.
- Professions (0/28, carried from prior iterations).

---

## Files

| file | role |
|---|---|
| `screen.py` | the shipped screen: signature engine, form-free oracle, coverage CIs, CLI. |
| `method.py` | driver: builds 10 hierarchies, screens all candidates, aggregates the coverage table, reproduces controls, writes `method_out.json`. |
| `core.py` | frozen Gemma-Scope JumpReLU SAE loader + gemma-2-2b `ModelBundle` + `ParentProbe` + stats (reused). |
| `cache/enc_*.npz` | cached residual+latent encodings (spelling / taxonomic / homograph). Not published. |

## Reproduce

```bash
python download_assets.py                 # fetch SAE params + gemma-2-2b
python method.py --smoke                  # end-to-end logic check (spelling L), $0
python method.py --mini                   # spelling + 1 homograph + 1 safety, oracle on, $0
python method.py                          # full: all 10 hierarchies -> results/method_out.json
```

All screen + coverage computation is `$0` (model-internal). Requires a single GPU
(gemma-2-2b bf16 + 16k SAE fits in ~6 GB; tested on an RTX 5090 / CUDA 12.8).
