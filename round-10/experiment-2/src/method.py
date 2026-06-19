#!/usr/bin/env python
"""
M1''''' part 2 — LABEL-FREE ABSORBER CATALOG over a public Gemma-Scope-2b SAE suite.
=====================================================================================================
Parametrizes the SHIPPED iter-9 label-free firing-signature screen (screen.py + core.py + the iter-9
driver builders in m9.py) over a list of frozen Gemma-Scope-2b SAE configs:

        {width 16k, 65k}  x  {layer 9, 12}

and runs it over the full multi-hierarchy candidate vocabulary (first-letter spelling L/O/T/I/D;
taxonomic countries; homograph city/month/given-name/brand; safety nationality/religion/ethnicity/
named-entity).  It emits ONE catalog row per (candidate x config) carrying the full LABEL-FREE
signature (parent latent, absorber latent, recall-hole, firing-Jaccard, firing-precision, hole-coverage
gain + bootstrap CI, predict_absorption enum, form-free oracle corroboration, layer, width), reproduces
the known iter-9 positives on the 16k/L12 config as a correctness check, reports per-config Wilson
coverage CIs, and JOINS rows across configs for a CROSS-CONFIG STABILITY column (which absorbers persist
across width/layer vs are dictionary-specific).

WHAT IS REUSED VERBATIM
  - screen.py                : the entire label-free signature engine (compute_signature/classify/oracle).
  - core.py                  : JumpReLU SAE + gemma-2-2b ModelBundle + ParentProbe + stats. Two small,
                               additive generalizations vs iter-9: (a) load_sae_multidict + resolve_sae_path
                               (multi-dictionary loader, ported from run__C1 iter_5); (b) determine_layer_idx
                               takes a `hidden_search` tuple so an arbitrary layer-L SAE can be hooked.
  - m9.py                    : the iter-9 driver (build_spelling/taxonomic/homograph/safety, candidates,
                               screen_candidate, family_anchor, aggregate_coverage, oracle_agreement,
                               georgia_selfcheck). Imported as a module; its per-config CACHE dir and the
                               vendored homograph path are reassigned per run.

LABEL-FREE FOR EVERY CONFIG
  m9.family_anchor data-derives entity anchors already (highest content-flip x_on recall clearing a
  corpus firing floor, no oracle).  For spelling/taxonomic the iter-9 KG4 anchors are 16k/L12-specific
  and do NOT transfer, so this driver DATA-DERIVES the spelling/taxonomic parent latent for the other
  three configs (same recipe), keeping the published catalog genuinely label-free-derivable.  On 16k/L12
  it ALSO records the data-derived anchor next to the KG4 anchor + their agreement (anchor_provenance).

COST: $0 LLM (all model-internal).  Optional Neuronpedia auto-interp enrichment is free + non-blocking.

Usage:
  python method.py --smoke    # STEP1: 16k_L12, spelling L only, from iter-9 cache, oracle off
  python method.py --mini     # STEP3: {16k_L12,65k_L12} x {spelling L, taxonomic, hg city, safety nat}
  python method.py            # FULL : 4 configs x 10 hierarchies
  python method.py --configs 16k_L12,65k_L12   # explicit config subset (fallback drop order)
  python method.py --neuronpedia               # add the optional free auto-interp labels
"""
import os, sys, json, time, gc, argparse, csv, shutil
from pathlib import Path
from collections import defaultdict, Counter

import numpy as np

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")

import core
from core import logger, el, ModelBundle, save_json, SEED, set_limits
import screen as SCR
import m9

# --------------------------------------------------------------------------- paths
WORK = Path("/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_10/gen_art/gen_art_experiment_2")
RESULTS = WORK / "results"; CACHE = WORK / "cache"; LOGS = WORK / "logs"
for d in (RESULTS, CACHE, LOGS):
    d.mkdir(parents=True, exist_ok=True)

ITER9_DIR = Path("/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_9/gen_art/gen_art_experiment_2")
ITER9_CACHE = ITER9_DIR / "cache"
ITER9_OUT = ITER9_DIR / "method_out.json"

# point m9's homograph dataset at the copy vendored in THIS workspace (formal dep also at run__C1 iter_5)
m9.HG_FULL = WORK / "homograph_data/full_data_out.json"
KG4 = core.ROOT / "iter_4/gen_art/gen_art_experiment_1/method_out.json"

rng = np.random.default_rng(SEED)

# --------------------------------------------------------------------------- SAE config suite
# l0_target: closest available average_l0 is chosen. hidden_search: candidate hidden_states indices to
# FVU-probe for the SAE's read layer (blocks.L reads hidden_states[L+1]).
CONFIGS = [
    {"name": "16k_L12", "layer": 12, "width": "16k", "l0_target": 82,  "expect_dsae": 16384,
     "hidden_search": (11, 12, 13, 14), "use_kg": True,  "reuse_iter9_cache": True},   # reproduction anchor
    {"name": "65k_L12", "layer": 12, "width": "65k", "l0_target": 72,  "expect_dsae": 65536,
     "hidden_search": (11, 12, 13, 14), "use_kg": False, "reuse_iter9_cache": False},  # wider width
    {"name": "16k_L9",  "layer": 9,  "width": "16k", "l0_target": 100, "expect_dsae": 16384,
     "hidden_search": (8, 9, 10, 11),  "use_kg": False, "reuse_iter9_cache": False},   # earlier layer
    {"name": "65k_L9",  "layer": 9,  "width": "65k", "l0_target": 100, "expect_dsae": 65536,
     "hidden_search": (8, 9, 10, 11),  "use_kg": False, "reuse_iter9_cache": False},
]
CONFIG_BY_NAME = {c["name"]: c for c in CONFIGS}
FVU_ABORT = 0.35

# Known iter-9 16k/L12 positives (the screen's DATA-DERIVED absorber over the dataset corpus; these are
# the correctness-check targets).  Georgia's data-derived absorber over the corpus is 4697 (the KG4 Georgia
# absorber); 16009 is the SEPARATE pinned absorber the screen.py CLI/self-check uses on curated windows.
KNOWN_16K = {
    ("taxonomic_country", "Georgia"): 4697,
    ("safety_named_entity_safety", "Amazon"): 6846,
    ("safety_named_entity_safety", "Bush"): 9751,
    ("safety_named_entity_safety", "Cook"): 15631,
}
GEORGIA_CLI_ABSORBER = 16009
POS_TOKENS = ["Georgia", "Amazon", "Bush", "Cook"]


# =========================================================================== label-free anchor derivation
def _anchor_from_rows(fam, cr_arr, on_rows, corpus_rows):
    """Data-derived parent latent = highest content-flip x_on recall among content-responsive latents that
    clear the corpus firing floor (the shared-concept detector; identical recipe to m9.family_anchor's
    entity branch, applied here ALSO to spelling-per-letter and taxonomic). NON-circular: no oracle."""
    if len(cr_arr) == 0 or len(on_rows) == 0:
        return -1
    A_on = np.asarray((fam.lat_csr[on_rows][:, cr_arr] > 0).todense()).astype(np.float64)
    recall_on = A_on.mean(0)
    if len(corpus_rows):
        fire_corpus = np.asarray((fam.lat_csr[corpus_rows][:, cr_arr] > 0).mean(0)).ravel()
    else:
        fire_corpus = np.zeros(len(cr_arr))
    elig = np.where(fire_corpus >= SCR.PARENT_FIRE_FLOOR)[0]
    pool = elig if len(elig) else np.arange(len(cr_arr))
    best = pool[int(np.argmax(recall_on[pool]))]
    return int(cr_arr[best])


def data_derived_anchors(fam):
    """{parent_key: data_derived_latent} for every parent in the family (letters / 'country' / entity hier)."""
    cr = m9.family_cr(fam)
    cr_arr = np.array([int(c) for c in cr], dtype=int)
    kind, p1, sub, fold = m9.fam_arrays(fam)
    out = {}
    if fam.kind == "spelling":
        for lt in fam.kg_anchors:
            on = np.where((kind == "cf") & (p1 == lt) & np.isin(sub, ["on", "x_on"]))[0]
            corp = np.where((kind == "corpus") & (p1 == lt))[0]
            out[lt] = _anchor_from_rows(fam, cr_arr, on, corp)
    elif fam.kind == "country":
        on = np.where((kind == "cf") & (p1 == "country") & np.isin(sub, ["on", "x_on"]))[0]
        corp = np.where((kind == "corpus_pos") | (kind == "corpus_neg"))[0]
        out["country"] = _anchor_from_rows(fam, cr_arr, on, corp)
    else:
        on = np.where((kind == "cf") & np.isin(sub, ["on", "x_on"]))[0]
        corp = np.where((kind == "corpus_pos") | (kind == "corpus_neg"))[0]
        out[fam.hier] = _anchor_from_rows(fam, cr_arr, on, corp)
    return out


# =========================================================================== per-config cache linking
def _link_iter9_cache(cfg_cache_dir):
    """Symlink the iter-9 encodings into this config's cache dir so the 16k/L12 screen reuses the EXACT
    iter-9 residual+latent encodings -> exact reproduction of the iter-9 numbers."""
    cfg_cache_dir.mkdir(parents=True, exist_ok=True)
    n = 0
    for f in sorted(ITER9_CACHE.glob("enc_*.npz")):
        dst = cfg_cache_dir / f.name
        if dst.exists() or dst.is_symlink():
            continue
        try:
            dst.symlink_to(f)
        except OSError:
            shutil.copy(f, dst)
        n += 1
    logger.info(f"{el()} linked {n} iter-9 cache files into {cfg_cache_dir}")


# =========================================================================== positive-control reproduction
def reproduce_positive_controls(cfg, rows):
    by_tok = defaultdict(list)
    for r in rows:
        by_tok[r["token"]].append(r)
    out = []
    for tok in POS_TOKENS:
        for r in by_tok.get(tok, []):
            key = (r["hierarchy"], tok)
            expected = KNOWN_16K.get(key) if cfg["name"] == "16k_L12" else None
            found = r["absorber_latent"]
            out.append({
                "config": cfg["name"], "token": tok, "hierarchy": r["hierarchy"],
                "predict": r["predict_absorption"],
                "structured_strict": r["absorption_structured_strict"],
                "structured_relaxed": r["absorption_structured_relaxed"],
                "data_derived_absorber": found, "parent_latent": r["parent_latent"],
                "expected_absorber_16kL12": expected,
                "matches_expected": (None if expected is None else bool(found == expected)),
                "recall_hole": r["recall_hole"], "firing_jaccard": r["firing_jaccard"],
                "precision": r["precision"], "hole_coverage_gain": r["hole_coverage_gain"],
                "oracle_corroborates": r.get("oracle_corroborates"),
                "note": ("dictionary/layer-specific reproduction is reported honestly; absorber ids are "
                         "dict-specific and need NOT match across configs" if expected is None else
                         "16k/L12 reproduction target")})
    return out


# =========================================================================== iter-9 exact reproduction check
def reproduce_iter9(rows_16k):
    """Compare the 16k/L12 catalog rows to the iter-9 method_out.json screen rows (must be identical:
    same cache, same KG anchors, same verbatim builders/screen)."""
    if not ITER9_OUT.exists():
        return {"status": "iter9_out_absent"}
    b = json.loads(ITER9_OUT.read_text())
    ds = {d["dataset"]: d for d in b["datasets"]}
    ref = {}
    for e in ds["absorption_coverage_screen"]["examples"]:
        ref[(e["metadata_hierarchy"], e["metadata_token"])] = e
    n = matched = pred_match = absb_match = 0
    mismatches = []
    for r in rows_16k:
        k = (r["hierarchy"], r["token"])
        if k not in ref:
            continue
        n += 1
        e = ref[k]
        pm = (r["predict_absorption"] == e["output"])
        am = (r["absorber_latent"] == e["metadata_absorber_latent"])
        pred_match += int(pm); absb_match += int(am)
        if pm and am:
            matched += 1
        elif len(mismatches) < 25:
            mismatches.append({"key": list(k), "got_predict": r["predict_absorption"],
                               "ref_predict": e["output"], "got_absorber": r["absorber_latent"],
                               "ref_absorber": e["metadata_absorber_latent"]})
    return {"status": "compared", "n_compared": n, "n_full_match": matched,
            "predict_match_rate": round(pred_match / max(n, 1), 4),
            "absorber_match_rate": round(absb_match / max(n, 1), 4),
            "full_match_rate": round(matched / max(n, 1), 4),
            "iter9_pooled_strict": b["metadata"]["coverage_headline"]["pooled_strict_n"],
            "iter9_pooled_relaxed": b["metadata"]["coverage_headline"]["pooled_relaxed_n"],
            "mismatches_sample": mismatches}


# =========================================================================== cross-config stability
def cross_config_stability(all_rows):
    groups = defaultdict(list)
    for r in all_rows:
        groups[(r["hierarchy"], r["token"])].append(r)
    stab = []
    for (hier, tok), grp in sorted(groups.items()):
        flags = {r["config"]: r["predict_absorption"] for r in grp}
        struct = {r["config"]: bool(r["absorption_structured_relaxed"]) for r in grp}
        strict = {r["config"]: bool(r["absorption_structured_strict"]) for r in grp}
        absb = {r["config"]: r["absorber_latent"] for r in grp}
        ocos = {r["config"]: r.get("oracle_decoder_cos") for r in grp}
        n_struct = int(sum(struct.values()))
        cross_width_L12 = bool(struct.get("16k_L12") and struct.get("65k_L12"))
        cross_layer_16k = bool(struct.get("16k_L12") and struct.get("16k_L9"))
        if n_struct >= 3:
            klass = "PERSISTENT"
        elif cross_width_L12 and not cross_layer_16k:
            klass = "WIDTH_SPECIFIC"
        elif cross_layer_16k and not cross_width_L12:
            klass = "LAYER_SPECIFIC"
        elif n_struct == 1:
            klass = "CONFIG_SPECIFIC"
        elif n_struct >= 2:
            klass = "MIXED"
        else:
            klass = "NONE"
        stab.append({"hierarchy": hier, "token": tok, "n_configs_present": len(grp),
                     "n_configs_structured": n_struct, "predict_by_config": flags,
                     "structured_by_config": struct, "strict_by_config": strict,
                     "absorber_by_config": absb, "oracle_cos_by_config": ocos,
                     "cross_width_L12": cross_width_L12, "cross_layer_16k": cross_layer_16k,
                     "stability_class": klass})
    return stab


def stability_counts(stab):
    c = Counter(s["stability_class"] for s in stab)
    any_struct = [s for s in stab if s["n_configs_structured"] >= 1]
    return {"n_tokens": len(stab), "n_tokens_structured_somewhere": len(any_struct),
            "class_counts": dict(c)}


def wider_width_table(per_config):
    """Per-hierarchy n_structured(65k_L12) vs n_structured(16k_L12): the 'wider width -> >= absorption' test."""
    out = {}
    a = per_config.get("16k_L12"); b = per_config.get("65k_L12")
    if not a or not b:
        return {"status": "needs_both_L12_configs"}
    def hcount(pc, gate):
        d = {}
        for t in pc["coverage_table"]:
            if t["hierarchy"] != "POOLED":
                d.setdefault(t["hierarchy"], {})[t["gate"]] = t["n_structured"]
        return {h: v.get(gate, 0) for h, v in d.items()}
    for gate in ("relaxed", "strict"):
        a_c = hcount(a, gate); b_c = hcount(b, gate)
        hiers = sorted(set(a_c) | set(b_c))
        out[gate] = {h: {"16k_L12": a_c.get(h, 0), "65k_L12": b_c.get(h, 0),
                         "wider_ge": bool(b_c.get(h, 0) >= a_c.get(h, 0))} for h in hiers}
        out[gate + "_pooled"] = {"16k_L12": a["n_structured_" + gate], "65k_L12": b["n_structured_" + gate],
                                 "wider_ge": bool(b["n_structured_" + gate] >= a["n_structured_" + gate])}
    return out


# =========================================================================== optional Neuronpedia enrichment
def enrich_neuronpedia(rows, timeout=6.0, max_calls=200):
    """Best-effort, $0, NON-blocking auto-interp labels for structured rows' parent+absorber latents.
    On ANY failure: set neuronpedia_label=None and return available=False (never blocks the run)."""
    import requests
    sess = requests.Session()
    cache = {}
    calls = [0]; available = [True]

    def fetch(layer, width, idx):
        if not available[0] or idx is None or idx < 0 or calls[0] >= max_calls:
            return None
        key = (layer, width, idx)
        if key in cache:
            return cache[key]
        url = f"https://www.neuronpedia.org/api/feature/gemma-2-2b/{layer}-gemmascope-res-{width}/{int(idx)}"
        try:
            calls[0] += 1
            r = sess.get(url, timeout=timeout)
            if r.status_code != 200:
                cache[key] = None; return None
            j = r.json()
            exps = j.get("explanations") or []
            lab = exps[0].get("description") if exps else None
            cache[key] = lab
            return lab
        except Exception:
            available[0] = False
            return None

    n_lab = 0
    for r in rows:
        if not r.get("absorption_structured_relaxed"):
            r["neuronpedia_parent_label"] = None; r["neuronpedia_absorber_label"] = None
            continue
        pl = fetch(r["layer"], r["width"], r.get("parent_latent"))
        al = fetch(r["layer"], r["width"], r.get("absorber_latent"))
        r["neuronpedia_parent_label"] = pl
        r["neuronpedia_absorber_label"] = al
        n_lab += int(pl is not None or al is not None)
    return {"available": bool(available[0] and calls[0] > 0), "n_calls": calls[0], "n_rows_labeled": n_lab}


# =========================================================================== per-config runner
def run_config(cfg, mb, torch, letters, hg_only, saf_only, build_tax, compute_oracle, kg):
    name = cfg["name"]
    logger.info(f"\n{el()} ========== CONFIG {name} (layer {cfg['layer']} width {cfg['width']}) ==========")
    sae = core.load_sae_multidict(torch, cfg, name)

    cdir = CACHE / name
    cdir.mkdir(parents=True, exist_ok=True)
    if cfg["reuse_iter9_cache"]:
        _link_iter9_cache(cdir)
    m9.CACHE = cdir   # _encode_family reads/writes here (config-namespaced)

    # FVU sanity / hook install on taxonomic corpus rows
    sample = [core._attach_span_tax(dict(r)) for r in core.load_taxonomic()
              if r["metadata_row_type"] == "corpus"][:64]
    best_hi, fvu = mb.determine_layer_idx(sample, sae, hidden_search=cfg["hidden_search"])
    fvu_best = float(fvu[best_hi])
    logger.info(f"{el()} [{name}] FVU best hidden_idx={best_hi} FVU={fvu_best:.4f} (all: "
                + ", ".join(f"{k}:{v:.3f}" for k, v in sorted(fvu.items())) + ")")
    if fvu_best > FVU_ABORT and not cfg["reuse_iter9_cache"]:
        logger.error(f"{el()} [{name}] FVU {fvu_best:.3f} > {FVU_ABORT} -> SKIP config (bad reconstruction)")
        del sae; gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        return None

    # build families (reuse iter-9 builders verbatim)
    spell_anchors = {lt: int(kg["first_letter"][lt]["anchor"]) for lt in letters}
    tax_anchor = int(kg["taxonomic"]["anchor"])
    families = []
    families.append(m9.build_spelling(mb, sae, spell_anchors, letters=tuple(letters)))
    if build_tax:
        families.append(m9.build_taxonomic(mb, sae, tax_anchor))
    families.extend(m9.build_homograph(mb, sae, only=hg_only))
    families.extend(m9.build_safety(mb, sae, only=saf_only))
    families = [f for f in families if f is not None]
    for fam in families:
        fam._sae = sae; fam.torch = torch

    W_dec_np = sae.W_dec.detach().cpu().numpy().astype(np.float32)

    # PHASE 1 — for NON-KG configs, override the screen anchor with the data-derived parent BEFORE
    # screening (the catalog must be label-free off 16k/L12). For the KG config we screen first and derive
    # the data-derived anchor afterwards (from the cached cr) so the content_responsive rng-consumption
    # order matches iter-9 exactly -> bit-exact reproduction of the iter-9 numbers.
    if not cfg["use_kg"]:
        for fam in families:
            dd = data_derived_anchors(fam)
            if fam.kind in ("spelling", "country"):
                fam.kg_anchors = dict(dd)        # consumed by m9.family_anchor as the parent latent

    # PHASE 2 — screen every candidate (KG config triggers family_cr lazily, in iter-9 order)
    raw = []  # (fam, info, row)
    fam_by_hier = {}
    for fam in families:
        fam_by_hier[fam.cov_hier] = fam
        cand = m9.candidates(fam, kg=kg)
        logger.info(f"{el()} [{name}/{fam.name}] {len(cand)} candidates")
        for tok, info in cand.items():
            r = m9.screen_candidate(fam, tok, info, W_dec_np, compute_oracle=compute_oracle)
            raw.append((fam, info, r))

    # PHASE 3 — data-derived anchors for every family (cr is now cached -> no extra rng for the KG config)
    dd_map = {}
    for fam in families:
        dd = data_derived_anchors(fam)
        for k, v in dd.items():
            dd_map[(fam.cov_hier, k)] = v

    # PHASE 4 — stamp provenance / config fields
    cfg_rows = []
    for fam, info, r in raw:
        parent = info["parent"]
        is_kg_kind = fam.cov_hier in ("first_letter_spelling", "taxonomic_country")
        dd = dd_map.get((fam.cov_hier, parent))
        if cfg["use_kg"] and is_kg_kind:
            prov = "kg4"; kg4a = r["anchor"]; dda = dd
            agree = bool(dd == r["anchor"]) if dd is not None else None
        else:
            prov = "data_derived"; kg4a = None; dda = r["anchor"]; agree = None
        r.update({"config": name, "layer": cfg["layer"], "width": cfg["width"],
                  "sae_id": sae.sae_id, "avg_l0": int(sae.avg_l0), "fvu": round(fvu_best, 4),
                  "hidden_idx": int(best_hi), "anchor_provenance": prov,
                  "data_derived_anchor": dda, "kg4_anchor": kg4a, "anchor_agreement": agree})
        cfg_rows.append(r)

    # dedup per (hierarchy, token)
    seen = set(); rows = []
    for r in cfg_rows:
        k = (r["hierarchy"], r["token"])
        if k in seen:
            continue
        seen.add(k); rows.append(r)

    # coverage + oracle + controls
    cov_table = m9.aggregate_coverage(rows)
    oracle_agree = m9.oracle_agreement(rows) if compute_oracle else {"status": "oracle_off"}
    pooled = {t["gate"]: t for t in cov_table if t["hierarchy"] == "POOLED"}
    per_hier_counts = {}
    for t in cov_table:
        if t["hierarchy"] != "POOLED":
            per_hier_counts.setdefault(t["hierarchy"], {})[t["gate"]] = f"{t['n_structured']}/{t['N']}"

    pos = reproduce_positive_controls(cfg, rows)
    georgia_self = {}
    if cfg["name"] == "16k_L12" and "taxonomic_country" in fam_by_hier:
        try:
            georgia_self = m9.georgia_selfcheck(fam_by_hier["taxonomic_country"], W_dec_np)
        except Exception as e:  # noqa: BLE001
            georgia_self = {"error": repr(e)[:160]}

    per_config = {
        "config": name, "layer": cfg["layer"], "width": cfg["width"], "sae_id": sae.sae_id,
        "avg_l0": int(sae.avg_l0), "fvu": round(fvu_best, 4), "hidden_idx": int(best_hi),
        "n_candidates": len(rows), "n_eligible": sum(1 for r in rows if r["eligible"]),
        "n_structured_strict": sum(int(r["absorption_structured_strict"]) for r in rows),
        "n_structured_relaxed": sum(int(r["absorption_structured_relaxed"]) for r in rows),
        "pooled_strict": {"n": pooled.get("strict", {}).get("n_structured"),
                          "N": pooled.get("strict", {}).get("N"),
                          "fraction": pooled.get("strict", {}).get("fraction"),
                          "wilson": [pooled.get("strict", {}).get("wilson_lo"),
                                     pooled.get("strict", {}).get("wilson_hi")]},
        "pooled_relaxed": {"n": pooled.get("relaxed", {}).get("n_structured"),
                           "N": pooled.get("relaxed", {}).get("N"),
                           "fraction": pooled.get("relaxed", {}).get("fraction"),
                           "wilson": [pooled.get("relaxed", {}).get("wilson_lo"),
                                      pooled.get("relaxed", {}).get("wilson_hi")]},
        "per_hierarchy_counts": per_hier_counts, "coverage_table": cov_table,
        "oracle_agreement": oracle_agree, "georgia_selfcheck": georgia_self,
        "positive_control_reproduction": pos,
    }

    # free everything before the next config
    for fam in families:
        for attr in ("lat_csr", "resid", "_cand_fire", "_cr", "_recall_on", "_probe", "_parfire", "enc_rows"):
            if hasattr(fam, attr):
                try:
                    delattr(fam, attr)
                except Exception:
                    pass
    del families, fam_by_hier, W_dec_np, sae
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    logger.info(f"{el()} [{name}] DONE: {len(rows)} candidates | strict={per_config['n_structured_strict']} "
                f"relaxed={per_config['n_structured_relaxed']} | pooled_strict={per_config['pooled_strict']['n']}"
                f"/{per_config['pooled_strict']['N']}")
    return {"rows": rows, "per_config": per_config, "pos": pos, "georgia_self": georgia_self}


# =========================================================================== catalog file writers
CSV_COLS = ["config", "layer", "width", "sae_id", "avg_l0", "fvu", "hierarchy", "parent", "token",
            "predict_absorption", "absorption_structured_strict", "absorption_structured_relaxed",
            "eligible", "n_eligible", "parent_latent", "absorber_latent", "anchor_provenance",
            "kg4_anchor", "data_derived_anchor", "anchor_agreement", "recall_hole", "firing_jaccard",
            "precision", "hole_coverage_gain", "gain_ci_lo", "gain_ci_hi", "random_latent_gain",
            "oracle_decoder_cos", "oracle_absorption_fraction", "oracle_corroborates",
            "max_prec_latent", "concentration_score", "neuronpedia_parent_label",
            "neuronpedia_absorber_label"]


def write_catalog_csv(rows, path):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c) for c in CSV_COLS})


def write_catalog_json(rows, path):
    nested = {}
    for r in rows:
        nested.setdefault(r["config"], {}).setdefault(r["hierarchy"], []).append(
            {k: r.get(k) for k in CSV_COLS if k not in ("config", "hierarchy")})
    Path(path).write_text(json.dumps(nested, indent=1, default=core._json_default))


# =========================================================================== exp_gen_sol_out examples
def _catalog_example(r):
    desc = (f"Absorber catalog entry [{r['config']}: layer {r['layer']} width {r['width']}] for "
            f"'{r['token']}' ({r['hierarchy']}, parent={r['parent']}): is the parent concept suppressed "
            f"on this token with a precise, mutually-exclusive absorber latent on this SAE?")
    md = {f"metadata_{k}": r.get(k) for k in CSV_COLS}
    md.update({"metadata_token": r["token"], "metadata_hierarchy": r["hierarchy"],
               "metadata_n_x": r.get("n_x_fit", 0) + r.get("n_x_eval", 0)})
    return {"input": desc, "output": r["predict_absorption"], "predict_absorption": r["predict_absorption"],
            **md}


def _coverage_example(name, t):
    return {"input": f"{name} :: {t['hierarchy']} coverage ({t['gate']} gate)",
            "output": str(t["fraction"]), "predict_coverage": f"{t['n_structured']}/{t['N']}",
            "metadata_config": name, "metadata_hierarchy": t["hierarchy"], "metadata_gate": t["gate"],
            "metadata_N": t["N"], "metadata_n_structured": t["n_structured"],
            "metadata_fraction": t["fraction"], "metadata_wilson_lo": t["wilson_lo"],
            "metadata_wilson_hi": t["wilson_hi"], "metadata_boot_lo": t["boot_lo"],
            "metadata_boot_hi": t["boot_hi"]}


def _stability_example(s):
    return {"input": f"Cross-config stability for '{s['token']}' ({s['hierarchy']}): does the absorber "
                     f"signature persist across SAE width/layer?",
            "output": s["stability_class"],
            "predict_stability_class": s["stability_class"],
            "metadata_hierarchy": s["hierarchy"], "metadata_token": s["token"],
            "metadata_n_configs_present": s["n_configs_present"],
            "metadata_n_configs_structured": s["n_configs_structured"],
            "metadata_cross_width_L12": s["cross_width_L12"],
            "metadata_cross_layer_16k": s["cross_layer_16k"],
            "metadata_structured_by_config": json.dumps(s["structured_by_config"]),
            "metadata_absorber_by_config": json.dumps(s["absorber_by_config"]),
            "metadata_predict_by_config": json.dumps(s["predict_by_config"])}


def _control_example(p):
    return {"input": f"Positive-control reproduction [{p['config']}] for '{p['token']}' ({p['hierarchy']})",
            "output": p["predict"],
            "predict_reproduced": ("MATCH" if p["matches_expected"] else
                                   ("MISMATCH" if p["matches_expected"] is False else "NO_EXPECTED")),
            "metadata_config": p["config"], "metadata_token": p["token"],
            "metadata_hierarchy": p["hierarchy"], "metadata_structured_strict": p["structured_strict"],
            "metadata_structured_relaxed": p["structured_relaxed"],
            "metadata_data_derived_absorber": p["data_derived_absorber"],
            "metadata_expected_absorber_16kL12": p["expected_absorber_16kL12"],
            "metadata_matches_expected": p["matches_expected"],
            "metadata_recall_hole": p["recall_hole"], "metadata_precision": p["precision"]}


HONEST_NOTES = [
    "Absorber LATENT IDs are dictionary-specific and CANNOT be matched across width/layer; cross-config "
    "stability is therefore measured at the (hierarchy, token) STRUCTURED-FLAG level, not by id equality.",
    "The form-free decoder-projection oracle is concept-tuned: it corroborates lexical/named-entity "
    "homograph absorbers but UNDER-fires for the taxonomic 'country' direction (Georgia's decoder is "
    "near-orthogonal to the generic country direction) -> it is corroboration-ONLY, never gates the flag.",
    "On 16k/L12 the catalog uses the KG4 anchors for spelling/taxonomic (reproduction) AND records the "
    "fully data-derived anchor + agreement; all other configs use data-derived anchors everywhere so the "
    "published catalog is genuinely label-free-derivable.",
    "Spelling word-types have <150 corpus positives so their coverage is the RELAXED breadth number, not "
    "the STRICT inferential one.",
    "A clean structured firing-signature need not be a meaningful single-latent EDIT handle (carried "
    "iter-8 finding); the catalog flags absorption STRUCTURE, not editability.",
    "Neuronpedia auto-interp labels are an OPTIONAL free enrichment; the catalog is complete without them.",
]


def assemble_output(args, results, all_rows, stab, stab_cnt, wider, repro9, np_meta, mb, n_configs_run,
                    config_names, kg_present):
    per_config = {r["per_config"]["config"]: r["per_config"] for r in results}
    catalog_summary = {
        "verdict": "CATALOG_PUBLISHED",
        "n_configs": n_configs_run, "configs": config_names,
        "n_candidates_total": len(all_rows),
        "per_config": {name: {"n_candidates": pc["n_candidates"], "n_eligible": pc["n_eligible"],
                              "n_structured_strict": pc["n_structured_strict"],
                              "n_structured_relaxed": pc["n_structured_relaxed"],
                              "pooled_strict": pc["pooled_strict"], "pooled_relaxed": pc["pooled_relaxed"],
                              "fvu": pc["fvu"], "avg_l0": pc["avg_l0"], "sae_id": pc["sae_id"]}
                       for name, pc in per_config.items()},
        "cross_config_stability_counts": stab_cnt,
        "wider_width_more_absorption": wider,
        "iter9_reproduction_16kL12": repro9,
        "neuronpedia_enrichment": np_meta,
    }
    metadata = {
        "method_name": "M1''''' part 2: Label-Free Absorber Catalog over a Gemma-Scope SAE suite",
        "overall_verdict": "CATALOG_PUBLISHED",
        "run_scale": ("smoke" if args.smoke else ("mini" if args.mini else "full")),
        "sae_suite": [{"name": c["name"], "layer": c["layer"], "width": c["width"],
                       "l0_target": c["l0_target"]} for c in CONFIGS if c["name"] in config_names],
        "release_repo": core.RELEASE_REPO, "model": mb.model_id, "seed": SEED,
        "B_boot_gain": SCR.B_BOOT_GAIN, "B_boot_coverage": 10000,
        "screen_thresholds": {"RECALL_HOLE_MIN": SCR.RECALL_HOLE_MIN, "JAC_MAX": SCR.JAC_MAX,
                              "PREC_MIN": SCR.PREC_MIN, "GAIN_MIN": SCR.GAIN_MIN,
                              "N_ELIGIBLE_MIN": SCR.N_ELIGIBLE_MIN, "DECODER_COS_MIN": SCR.DECODER_COS_MIN,
                              "MIN_FIRE_DIAG": SCR.MIN_FIRE_DIAG, "PARENT_FIRE_FLOOR": SCR.PARENT_FIRE_FLOOR},
        "per_config": per_config,
        "catalog_summary": catalog_summary,
        "shipped_files": {"catalog_csv": "catalog.csv", "catalog_json": "catalog.json",
                          "screen_module": "screen.py", "readme": "README.md"},
        "label_free_guarantee": ("the predict_absorption flag uses ONLY model-internal firing statistics "
                                 "(recall, firing-Jaccard, firing-precision, hole-coverage gain + bootstrap "
                                 "CI) from a frozen SAE on raw text; the decoder-projection oracle is "
                                 "corroboration-only and never gates."),
        "baselines": {"raw_single_latent": "parent latent alone (recall_hole = 1 - parent recall on X)",
                      "augmented_unit_gain": "hole_coverage_gain = recall recovered when the absorber is "
                                             "OR-ed into the parent (the cluster-level unit beats the raw "
                                             "latent iff gain CI excludes 0)",
                      "random_latent_control": "random_latent_gain (firing-rate-matched random latent; "
                                               "near 0 -> the absorber is not a coincidence)",
                      "non_sae_probe_oracle": "form-free decoder-projection vs a dense diff-of-means probe "
                                              "direction d_p (independent corroboration)"},
        "honest_notes": HONEST_NOTES, "cost_usd": 0.0, "budget_cap_usd": 10,
    }
    cov_examples = []
    for name, pc in per_config.items():
        for t in pc["coverage_table"]:
            cov_examples.append(_coverage_example(name, t))
    control_examples = []
    for r in results:
        for p in r["pos"]:
            control_examples.append(_control_example(p))
    datasets = [
        {"dataset": "absorber_catalog", "examples": [_catalog_example(r) for r in all_rows]},
        {"dataset": "catalog_coverage", "examples": cov_examples},
        {"dataset": "cross_config_stability", "examples": [_stability_example(s) for s in stab]},
        {"dataset": "positive_control_reproduction", "examples": control_examples},
    ]
    return {"metadata": metadata, "datasets": datasets}


# =========================================================================== README
def write_readme(path, summary, config_names):
    pc = summary["per_config"]
    lines = []
    lines.append("# Label-Free SAE Absorber Catalog (Gemma-Scope-2b suite)\n")
    lines.append("A reusable, **label-free** catalog of feature-absorption structure across a public "
                 "Gemma-Scope-2b SAE suite — **{16k, 65k} widths × {layer 9, layer 12}** — on gemma-2-2b. "
                 "One row per *(candidate token × SAE config)* with the full model-internal absorption "
                 "signature and a verdict in `{ABSORPTION_STRUCTURED, CO_FIRING, NO_HOLE, "
                 "DESCRIPTIVE_ONLY}`. Built by re-running the shipped iter-9 screen (`screen.py`) over four "
                 "frozen SAE dictionaries.\n")
    lines.append("## Files\n")
    lines.append("| file | role |\n|---|---|")
    lines.append("| `catalog.csv` | flat: one row per (candidate × config), all signature columns. |")
    lines.append("| `catalog.json` | nested: config → hierarchy → rows. |")
    lines.append("| `screen.py` | the shipped label-free screen (signature engine + form-free oracle + CLI). |")
    lines.append("| `method.py` | the multi-config catalog driver (this experiment). |")
    lines.append("| `core.py` / `m9.py` | SAE+model infra and the iter-9 builders, reused. |")
    lines.append("| `method_out.json` | full machine-readable results (coverage, stability, controls). |\n")
    lines.append("## The label-free derivation (per candidate token X, per SAE config)\n")
    lines.append("1. **Content-responsive eligibility** — candidate absorber latents are those that "
                 "respond to the concept on content-flip minimal pairs (sign-flip null, no labels).\n"
                 "2. **Parent latent (anchor)** — the highest content-flip `x_on` recall latent that clears "
                 "a corpus firing floor (the shared-concept detector). KG4 ids on 16k/L12 for reproduction; "
                 "**data-derived everywhere else** (label-free).\n"
                 "3. **Recall-hole** — `1 − P(parent fires | X-positive rows)` on held-out rows (> 0.50 ⇒ "
                 "the parent is suppressed on X).\n"
                 "4. **Absorber** — a content-responsive latent that is firing-disjoint from the parent "
                 "(firing-Jaccard < 0.10), precise for X (≥ 0.70), and covers the parent's holes; the "
                 "**hole-coverage gain** (recall recovered by OR-ing the absorber into the parent) must be "
                 "≥ 0.05 with a 5000-sample bootstrap CI excluding 0.\n"
                 "5. **Verdict** — `ABSORPTION_STRUCTURED` (strict, all hold + ≥150 positives) / `relaxed` "
                 "(firing conditions hold, <150 positives) / `CO_FIRING` / `NO_HOLE` / `DESCRIPTIVE_ONLY`.\n")
    lines.append("The form-free decoder-projection **oracle** (Chanin App. A.13 / SAEBench "
                 "`absorption_fraction`) is **corroboration only** — it needs a dense parent-probe direction "
                 "fit on a disjoint fold, is never used to flag, and under-fires for the taxonomic "
                 "'country' direction (documented).\n")
    lines.append("## Configs run\n")
    lines.append("| config | layer | width | avg L0 | SAE id | FVU | candidates | structured (strict / relaxed) | pooled-strict |\n|---|---|---|---|---|---|---|---|---|")
    for name in config_names:
        if name not in pc:
            continue
        p = pc[name]
        ps = p["pooled_strict"]
        lines.append(f"| {name} | {CONFIG_BY_NAME[name]['layer']} | {CONFIG_BY_NAME[name]['width']} | "
                     f"{p['avg_l0']} | {p['sae_id']} | {p['fvu']} | {p['n_candidates']} | "
                     f"{p['n_structured_strict']} / {p['n_structured_relaxed']} | {ps['n']}/{ps['N']} |")
    lines.append("\n## Cross-config stability\n")
    sc = summary["cross_config_stability_counts"]
    lines.append(f"- tokens catalogued: **{sc['n_tokens']}**; structured in ≥1 config: "
                 f"**{sc['n_tokens_structured_somewhere']}**.")
    lines.append(f"- stability classes: `{json.dumps(sc['class_counts'])}` "
                 "(PERSISTENT = structured in ≥3 configs; WIDTH_SPECIFIC = both L12 widths only; "
                 "LAYER_SPECIFIC = both 16k layers only; CONFIG_SPECIFIC = exactly one config).\n")
    ww = summary.get("wider_width_more_absorption", {})
    if isinstance(ww, dict) and "relaxed_pooled" in ww:
        rp = ww["relaxed_pooled"]
        lines.append(f"- **wider width → ≥ absorption** (pooled relaxed): 16k/L12 = {rp['16k_L12']} vs "
                     f"65k/L12 = {rp['65k_L12']} (wider ≥: {rp['wider_ge']}).\n")
    r9 = summary.get("iter9_reproduction_16kL12", {})
    if r9.get("status") == "compared":
        lines.append(f"## 16k/L12 reproduction\n\nExact re-run of iter-9 from cached encodings: "
                     f"{r9['n_full_match']}/{r9['n_compared']} rows match on (predict, absorber) "
                     f"(predict match {r9['predict_match_rate']}, absorber match {r9['absorber_match_rate']}). "
                     f"iter-9 pooled-strict {r9['iter9_pooled_strict']}.\n")
    lines.append("## Caveats / failure modes (reported honestly)\n")
    for n in HONEST_NOTES:
        lines.append(f"- {n}")
    lines.append("\n## Reproduce\n```\npython method.py --smoke   # 16k/L12 spelling-L from cache\n"
                 "python method.py --mini    # 2 configs x 4 hierarchies\npython method.py           "
                 "# full: 4 configs x 10 hierarchies\n```\n$0 LLM. Single GPU (gemma-2-2b bf16 + one SAE).\n")
    Path(path).write_text("\n".join(lines))


# =========================================================================== main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--mini", action="store_true")
    ap.add_argument("--no_oracle", action="store_true")
    ap.add_argument("--neuronpedia", action="store_true")
    ap.add_argument("--configs", type=str, default=None, help="comma-sep config names subset")
    args = ap.parse_args()

    set_limits()
    logger.info(f"{el()} ===== M1''''' part2 — Label-Free Absorber Catalog (suite sweep) =====")
    torch = __import__("torch")
    mb = ModelBundle(torch)

    kg = json.loads(KG4.read_text())["metadata"]["canonical_units"]

    # run scale
    if args.smoke:
        config_names = ["16k_L12"]; letters = ["L"]; hg_only = set(); saf_only = set(); build_tax = False
        compute_oracle = False
    elif args.mini:
        config_names = ["16k_L12", "65k_L12"]; letters = ["L"]; hg_only = {"city"}
        saf_only = {"nationality"}; build_tax = True; compute_oracle = not args.no_oracle
    else:
        config_names = ["16k_L12", "65k_L12", "16k_L9", "65k_L9"]
        letters = ["L", "O", "T", "I", "D"]; hg_only = None; saf_only = None; build_tax = True
        compute_oracle = not args.no_oracle
    if args.configs:
        want = [c.strip() for c in args.configs.split(",") if c.strip()]
        config_names = [c for c in want if c in CONFIG_BY_NAME]

    results = []
    for name in config_names:
        cfg = CONFIG_BY_NAME[name]
        try:
            res = run_config(cfg, mb, torch, letters, hg_only, saf_only, build_tax, compute_oracle, kg)
        except Exception as e:  # noqa: BLE001
            logger.exception(f"{el()} [{name}] FAILED: {repr(e)[:200]}")
            res = None
        if res is not None:
            results.append(res)
            # checkpoint per config
            (RESULTS / f"per_config_{name}.json").write_text(
                json.dumps(res["per_config"], indent=1, default=core._json_default))

    if not results:
        logger.error("no config produced rows; aborting")
        sys.exit(1)

    all_rows = [r for res in results for r in res["rows"]]
    logger.info(f"{el()} TOTAL catalog rows across {len(results)} configs: {len(all_rows)}")

    # optional Neuronpedia enrichment (best-effort, $0)
    np_meta = {"available": False, "attempted": bool(args.neuronpedia)}
    if args.neuronpedia:
        try:
            np_meta = enrich_neuronpedia(all_rows)
            np_meta["attempted"] = True
        except Exception as e:  # noqa: BLE001
            logger.warning(f"neuronpedia enrichment failed: {repr(e)[:160]}")
            np_meta = {"available": False, "attempted": True, "error": repr(e)[:160]}
    else:
        for r in all_rows:
            r.setdefault("neuronpedia_parent_label", None)
            r.setdefault("neuronpedia_absorber_label", None)

    stab = cross_config_stability(all_rows)
    stab_cnt = stability_counts(stab)
    per_config = {res["per_config"]["config"]: res["per_config"] for res in results}
    wider = wider_width_table(per_config)
    rows_16k = [r for r in all_rows if r["config"] == "16k_L12"]
    repro9 = reproduce_iter9(rows_16k) if rows_16k else {"status": "no_16kL12"}

    out = assemble_output(args, results, all_rows, stab, stab_cnt, wider, repro9, np_meta, mb,
                          len(results), [res["per_config"]["config"] for res in results], kg)

    # ship the resource files
    write_catalog_csv(all_rows, WORK / "catalog.csv")
    write_catalog_json(all_rows, WORK / "catalog.json")
    write_readme(WORK / "README.md", out["metadata"]["catalog_summary"],
                 [res["per_config"]["config"] for res in results])

    outp = RESULTS / ("smoke_method_out.json" if args.smoke else
                      ("mini_method_out.json" if args.mini else "method_out.json"))
    save_json(out, outp)
    if not args.smoke and not args.mini:
        save_json(out, WORK / "method_out.json")
    logger.info(f"{el()} WROTE {outp}")
    logger.info(f"{el()} catalog.csv / catalog.json / README.md shipped")
    logger.info(f"{el()} stability classes: {json.dumps(stab_cnt['class_counts'])}")
    logger.info(f"{el()} iter9 reproduction(16k_L12): {json.dumps(repro9 if repro9.get('status')!='compared' else {k: repro9[k] for k in ('n_full_match','n_compared','full_match_rate')})}")
    for res in results:
        pc = res["per_config"]
        logger.info(f"{el()}   {pc['config']}: strict={pc['n_structured_strict']} relaxed={pc['n_structured_relaxed']} "
                    f"pooled_strict={pc['pooled_strict']['n']}/{pc['pooled_strict']['N']} fvu={pc['fvu']}")
    return out


if __name__ == "__main__":
    main()
