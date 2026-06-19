#!/usr/bin/env python3
"""Standardize THREE real, human-annotated datasets into the CCRG shared minimal-pair schema.

Family 1  sentiment              : CAD-IMDB (Kaushik et al. ICLR 2020) content-flip pairs (GitHub TSVs).
Family 2  restaurant_aspect      : CEBaB (Abraham et al. NeurIPS 2022) food+service aspect-flip pairs (HF).
Family 3  bias_in_bios_boundary  : LabHC/bias_in_bios profession bios, gender sub-context, boundary-null (HF).

Output: full_data_out.json in the canonical `exp_sel_data_out` format
        {metadata, datasets:[{dataset, examples:[{input, output, metadata_*}]}]}.
All logical row fields are also validated against schema.json (jsonschema) before emission.
NO LLM/OpenRouter calls (all sources human-annotated) -> $0 spend.
"""
import os
import re
import sys
import json
import csv
from pathlib import Path
from collections import Counter, defaultdict

import numpy as np
import pandas as pd
from loguru import logger
import jsonschema

WS = Path(__file__).resolve().parent
os.environ.setdefault("HF_HOME", str(WS / "temp" / "hf_cache"))
from datasets import load_dataset  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
(WS / "logs").mkdir(exist_ok=True)
logger.add(str(WS / "logs" / "build.log"), rotation="30 MB", level="DEBUG")

# ----------------------------------------------------------------------------- constants
SUBSAMPLE_SEED = 20240617
CAD_DIR = WS / "temp" / "datasets" / "cad_raw"
SCHEMA_PATH = WS / "schema.json"
OUT_PATH = WS / "full_data_out.json"

# Canonical De-Arteaga et al. (2019) biosbias 28 occupations (alphabetical, includes 'dj').
# VERIFIED EMPIRICALLY: 17/17 professions confirmed by keyword hit-rate in verify.py
# (nurse=13, attorney=2, surgeon=25, software_engineer=24, yoga_teacher=27, dentist=6, ...).
PROFESSIONS = [
    "accountant", "architect", "attorney", "chiropractor", "comedian", "composer", "dentist",
    "dietitian", "dj", "filmmaker", "interior_designer", "journalist", "model", "nurse", "painter",
    "paralegal", "pastor", "personal_trainer", "photographer", "physician", "poet", "professor",
    "psychologist", "rapper", "software_engineer", "surgeon", "teacher", "yoga_teacher",
]
assert len(PROFESSIONS) == 28
GENDER_MAP = {0: "male", 1: "female"}  # verified by pronoun inspection (He->0, She->1)

_TOK = re.compile(r"[a-z0-9']+")


def toks(text: str) -> set:
    return set(_TOK.findall(text.lower()))


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def norm_aspect(v: str) -> str:
    """Normalize a raw aspect-majority string to a stable sub-context token."""
    m = {"Positive": "positive", "Negative": "negative", "unknown": "unknown",
         "no majority": "no_majority", "": "unknown"}
    return m.get(v, "unknown")


def binarize_review(v: str) -> str:
    """CEBaB 5-star review_majority -> sentiment band. 1,2=neg; 4,5=pos; 3=neutral; else."""
    return {"1": "negative", "2": "negative", "4": "positive", "5": "positive",
            "3": "neutral", "no majority": "no_majority"}.get(str(v), "unknown")


def to_exp_example(row: dict) -> dict:
    """Convert a validated logical row -> an exp_sel_data_out example (metadata_* prefixed)."""
    ex = {"input": row["input"], "output": row["output"]}
    for k, v in row.items():
        if k in ("input", "output"):
            continue
        ex[f"metadata_{k}"] = v
    return ex


# ============================================================================ FAMILY 1
def build_sentiment() -> tuple[list, dict]:
    """CAD-IMDB. Use the repo's combined/paired/*_paired.tsv files: rows sharing a `batch_id`
    are one human minimal-edit pair (one Positive, one Negative). This is the GROUND-TRUTH pair
    link shipped by the authors -- strictly better than the orig/<->new/ row-index assumption,
    which we empirically REJECTED (orig[i] and new[i] are unrelated reviews: flip_rate~0.50,
    aligned token-Jaccard ~= shuffled baseline ~0.11). Pairing recorded as 'batch_id_grouped'."""
    logger.info("FAMILY 1: CAD-IMDB sentiment (combined/paired, batch_id grouping)")
    rows = []
    fold_map = {"train": "train", "dev": "dev", "test": "test"}
    src = "CAD-IMDB (Kaushik et al. ICLR 2020)"
    pairing_stats = {}
    rng = np.random.default_rng(SUBSAMPLE_SEED)
    method = "batch_id_grouped"

    for split, fold in fold_map.items():
        df = pd.read_csv(CAD_DIR / "paired" / f"{split}_paired.tsv", sep="\t", quoting=csv.QUOTE_MINIMAL)
        df.columns = [c.strip() for c in df.columns]
        assert list(df.columns) == ["Sentiment", "Text", "batch_id"], df.columns
        overlaps = []
        n_pairs = 0
        dropped = 0
        for bid, grp in df.groupby("batch_id"):
            sents = [s.strip().lower() for s in grp["Sentiment"]]
            texts = [str(t) for t in grp["Text"]]
            # require exactly one positive + one negative member, both non-empty
            if len(grp) != 2 or set(sents) != {"positive", "negative"} or any(not t.strip() for t in texts):
                dropped += 1
                continue
            pos_i = sents.index("positive")
            neg_i = sents.index("negative")
            ptext, ntext = texts[pos_i], texts[neg_i]
            ov = jaccard(toks(ptext), toks(ntext))
            overlaps.append(ov)
            pid = f"sent_{split}_{int(bid)}"
            pos_id, neg_id = f"{pid}_pos", f"{pid}_neg"
            rows.append(_sent_row(pos_id, ptext, "positive", pid, neg_id, fold, src, ov))
            rows.append(_sent_row(neg_id, ntext, "negative", pid, pos_id, fold, src, ov))
            n_pairs += 1
        # sanity: true-pair overlap should DOMINATE a random shuffled baseline
        ov_arr = np.array(overlaps)
        shuffled = ov_arr.copy()
        rng.shuffle(shuffled)  # within-split shuffle is a self-baseline; compute cross-pair baseline below
        pos_texts = [str(t) for s, t in zip(df["Sentiment"], df["Text"]) if s.strip().lower() == "positive"]
        neg_texts = [str(t) for s, t in zip(df["Sentiment"], df["Text"]) if s.strip().lower() == "negative"]
        perm = rng.permutation(len(neg_texts))
        rand_ov = np.array([jaccard(toks(pos_texts[i]), toks(neg_texts[perm[i]]))
                            for i in range(min(len(pos_texts), len(neg_texts)))])
        med_true = float(np.median(ov_arr)) if len(ov_arr) else 0.0
        med_rand = float(np.median(rand_ov)) if len(rand_ov) else 0.0
        logger.info(f"  {split}: pairs={n_pairs} dropped={dropped} med_true_jacc={med_true:.3f} "
                    f"med_random_pair_jacc={med_rand:.3f} (true >> random confirms minimal edits)")
        pairing_stats[split] = {
            "pairing_method": method, "n_pairs": n_pairs, "dropped_batches": dropped,
            "median_true_pair_jaccard": round(med_true, 4),
            "median_random_pair_jaccard": round(med_rand, 4),
        }

    summary = _summarize("sentiment", rows, extra={
        "n_pairs": sum(s["n_pairs"] for s in pairing_stats.values()),
        "per_split_pairing": pairing_stats,
        "license": "Apache-2.0",
        "source_url": "https://github.com/acmi-lab/counterfactually-augmented-data (sentiment/combined/paired)",
        "source_paper": "Kaushik, Hovy, Lipton. ICLR 2020. arXiv:1909.12434",
        "pairing_note": ("orig/<->new/ row-index alignment was tested and REJECTED (flip_rate~0.50, "
                         "aligned Jaccard ~= random). Authoritative pairing taken from combined/paired "
                         "via shared batch_id (exactly one Positive + one Negative per batch_id)."),
        "concept": "sentiment (positive vs negative); content_on = positive-present.",
    })
    return rows, summary


def _sent_row(rid, text, label, pid, partner, fold, src, overlap):
    return {
        "id": rid, "input": text, "output": label, "family": "sentiment",
        "dataset_source": src, "concept": "sentiment", "concept_label": label,
        "sub_context": {},
        "pair_id": pid,
        "pair_role": "content_on" if label == "positive" else "content_off",
        "partner_id": partner, "flip_type": "content",
        "is_content_pair": True, "is_surface_pair": False, "fold": fold,
        "meta": {"raw_sentiment": label.capitalize(), "char_len": len(text),
                 "token_overlap_with_partner": round(overlap, 4),
                 "pairing_method": "batch_id_grouped"},
    }


# ============================================================================ FAMILY 2
def build_cebab() -> tuple[list, dict]:
    logger.info("FAMILY 2: CEBaB food+service aspect")
    ceb = load_dataset("CEBaB/CEBaB")
    src = "CEBaB (Abraham et al. NeurIPS 2022)"
    split_map = {"train_inclusive": "train", "validation": "dev", "test": "test"}
    rows = []
    counters = {"food": 0, "service": 0}
    dropped = Counter()
    kept = Counter()

    for split, fold in split_map.items():
        df = ceb[split].to_pandas()
        omap = {r["original_id"]: r for _, r in df[df["is_original"]].iterrows()}
        edits = df[~df["is_original"]]
        for _, e in edits.iterrows():
            A = e["edit_type"]  # the EDITED ASPECT (food/service/ambiance/noise); NOT edit_goal
            if A not in ("food", "service"):
                continue
            o = omap.get(e["original_id"])
            if o is None:
                dropped[f"{A}_no_original"] += 1
                continue
            ev = e[f"{A}_aspect_majority"]
            ov = o[f"{A}_aspect_majority"]
            if ev not in ("Positive", "Negative") or ov not in ("Positive", "Negative"):
                dropped[f"{A}_unknown_aspect"] += 1
                continue
            if ev == ov:
                dropped[f"{A}_no_flip"] += 1
                continue
            kept[A] += 1
            idx = counters[A]
            counters[A] += 1
            concept = f"{A}_sentiment"
            pid = f"cebab_{A}_{idx:04d}"
            o_id, e_id = f"{pid}_orig", f"{pid}_edit"
            overlap = jaccard(toks(str(o["description"])), toks(str(e["description"])))
            rows.append(_cebab_row(o_id, o, A, ov, concept, pid, e_id, fold, src, "original", overlap))
            rows.append(_cebab_row(e_id, e, A, ev, concept, pid, o_id, fold, src, "edit", overlap))

    summary = _summarize("restaurant_aspect", rows, extra={
        "n_pairs_food": kept["food"], "n_pairs_service": kept["service"],
        "n_pairs_total": kept["food"] + kept["service"],
        "dropped_pairs": dict(dropped),
        "license": "CC-BY-4.0",
        "source_url": "https://huggingface.co/datasets/CEBaB/CEBaB",
        "source_paper": "Abraham et al. NeurIPS 2022. arXiv:2205.14140",
        "split_policy": "train_inclusive->train (superset of edits), validation->dev, test->test.",
        "field_correction": ("CEBaB edit_type = edited ASPECT {food,service,ambiance,noise}; "
                             "edit_goal = target sentiment {Positive,Negative,unknown}. We pair on edit_type."),
        "concept": "food_sentiment & service_sentiment nested as ONE family; ambiance/noise retained as sub_context only.",
    })
    return rows, summary


def _cebab_row(rid, r, aspect, aspect_val, concept, pid, partner, fold, src, member, overlap):
    label = "positive" if aspect_val == "Positive" else "negative"
    sub = {
        "edited_aspect": aspect,
        "food": norm_aspect(r["food_aspect_majority"]),
        "service": norm_aspect(r["service_aspect_majority"]),
        "ambiance": norm_aspect(r["ambiance_aspect_majority"]),
        "noise": norm_aspect(r["noise_aspect_majority"]),
        "review_sentiment": binarize_review(r["review_majority"]),
    }
    text = str(r["description"])
    return {
        "id": rid, "input": text, "output": label, "family": "restaurant_aspect",
        "dataset_source": src, "concept": concept, "concept_label": label,
        "sub_context": sub,
        "pair_id": pid,
        "pair_role": "content_on" if label == "positive" else "content_off",
        "partner_id": partner, "flip_type": "content",
        "is_content_pair": True, "is_surface_pair": False, "fold": fold,
        "meta": {"original_id": str(r["original_id"]), "edit_id": str(r["edit_id"]),
                 "is_original": bool(r["is_original"]), "edit_goal": str(r["edit_goal"]),
                 "edit_type": str(r["edit_type"]), "member": member,
                 "raw_review_majority": str(r["review_majority"]),
                 "raw_aspect_majority": str(aspect_val),
                 "char_len": len(text), "token_overlap_with_partner": round(overlap, 4)},
    }


# ============================================================================ FAMILY 3
def build_bias_in_bios() -> tuple[list, dict]:
    logger.info("FAMILY 3: bias_in_bios boundary-null")
    bib = load_dataset("LabHC/bias_in_bios")
    src = "LabHC/bias_in_bios (De-Arteaga et al. 2019)"
    # targets -> per (profession x gender) stratum caps (28 x 2 = 56 strata)
    split_cfg = {"train": ("train", 15000), "dev": ("dev", 3000), "test": ("test", 3000)}
    rows = []
    rng = np.random.default_rng(SUBSAMPLE_SEED)
    caps = {}
    realized = {}

    for split, (fold, target) in split_cfg.items():
        ds = bib[split]
        profs = np.array(ds["profession"], dtype=np.int64)
        gens = np.array(ds["gender"], dtype=np.int64)
        n_strata = len(set(zip(profs.tolist(), gens.tolist())))
        cap = int(np.ceil(target / max(n_strata, 1)))
        caps[split] = cap
        # deterministic stratified sampling with per-stratum cap
        strata = defaultdict(list)
        for i in range(len(profs)):
            strata[(int(profs[i]), int(gens[i]))].append(i)
        chosen = []
        for key in sorted(strata.keys()):
            idxs = np.array(strata[key])
            take = min(len(idxs), cap)
            sel = rng.choice(idxs, size=take, replace=False)
            chosen.extend(sel.tolist())
        chosen = sorted(chosen)
        sub = ds.select(chosen)
        texts = sub["hard_text"]
        sp = sub["profession"]
        sg = sub["gender"]
        for j in range(len(sub)):
            text = str(texts[j])
            if not text.strip():
                continue
            pid_int = int(sp[j])
            g_int = int(sg[j])
            label = PROFESSIONS[pid_int]
            rows.append({
                "id": f"bib_{fold}_{j:05d}", "input": text, "output": label,
                "family": "bias_in_bios_boundary", "dataset_source": src,
                "concept": "profession", "concept_label": label,
                "sub_context": {"gender": GENDER_MAP[g_int]},
                "pair_id": None, "pair_role": None, "partner_id": None, "flip_type": None,
                "is_content_pair": False, "is_surface_pair": False, "fold": fold,
                "meta": {"raw_profession_int": pid_int, "raw_gender_int": g_int,
                         "char_len": len(text),
                         "profession_mapping_verified": "empirical_keyword_17of17"},
            })
        realized[split] = len(chosen)
        logger.info(f"  {split}: strata={n_strata} cap={cap} -> kept {len(chosen)} rows")

    summary = _summarize("bias_in_bios_boundary", rows, extra={
        "subsample_seed": SUBSAMPLE_SEED,
        "per_split_stratum_cap": caps,
        "per_split_kept": realized,
        "stratification": "by (profession x gender), 56 strata, per-stratum cap, fixed seed.",
        "license": "MIT",
        "source_url": "https://huggingface.co/datasets/LabHC/bias_in_bios",
        "source_paper": "De-Arteaga et al. FAT* 2019. arXiv:1901.09451",
        "boundary_null_rationale": (
            "Profession 'habitat' ~= the class label, so co-response grouping is PREDICTED to give no "
            "advantage over raw latents here. A null result is the PRE-REGISTERED EXPECTATION, not method "
            "failure. gender is the independent sub-attribute / habitat!=label diagnostic axis."),
        "profession_int_to_string": {i: p for i, p in enumerate(PROFESSIONS)},
        "full_set_note": "Full 396k bios reproducible from the HF repo if downstream needs more.",
    })
    return rows, summary


# ============================================================================ helpers
def _summarize(family: str, rows: list, extra: dict) -> dict:
    out = Counter(r["output"] for r in rows)
    folds = Counter(r["fold"] for r in rows)
    subctx_keys = Counter()
    subctx_vals = defaultdict(Counter)
    for r in rows:
        for k, v in (r["sub_context"] or {}).items():
            subctx_keys[k] += 1
            subctx_vals[k][str(v)] += 1
    summ = {
        "family": family, "n_rows": len(rows),
        "label_balance": dict(out.most_common()),
        "fold_sizes": dict(folds),
        "sub_context_keys": dict(subctx_keys),
        "sub_context_value_distributions": {k: dict(v.most_common()) for k, v in subctx_vals.items()},
    }
    summ.update(extra)
    return summ


@logger.catch(reraise=True)
def main():
    schema = json.loads(SCHEMA_PATH.read_text())
    validator = jsonschema.Draft7Validator(schema)

    sent_rows, sent_sum = build_sentiment()
    cebab_rows, cebab_sum = build_cebab()
    bib_rows, bib_sum = build_bias_in_bios()

    # ---- global id uniqueness + per-row schema validation ----
    all_rows = sent_rows + cebab_rows + bib_rows
    ids = [r["id"] for r in all_rows]
    assert len(ids) == len(set(ids)), f"DUPLICATE IDS: {len(ids) - len(set(ids))} dups"
    # validate every logical row against schema.json
    n_err = 0
    for r in all_rows:
        errs = sorted(validator.iter_errors(r), key=lambda e: e.path)
        if errs:
            n_err += 1
            if n_err <= 5:
                logger.error(f"Schema error in {r['id']}: {errs[0].message}")
    if n_err:
        raise ValueError(f"{n_err} rows failed schema.json validation")
    logger.info(f"All {len(all_rows)} logical rows valid against schema.json; ids globally unique.")

    # ---- verify partner symmetry for content pairs ----
    by_id = {r["id"]: r for r in all_rows}
    bad = 0
    for r in all_rows:
        if r["is_content_pair"]:
            p = by_id.get(r["partner_id"])
            if p is None or p["pair_id"] != r["pair_id"] or p["partner_id"] != r["id"]:
                bad += 1
    assert bad == 0, f"{bad} broken partner links"
    logger.info("Partner-link symmetry verified for all content pairs.")

    # ---- assemble exp_sel_data_out ----
    datasets = [
        {"dataset": sent_sum["source_paper"].split(".")[0] + " | CAD-IMDB sentiment",
         "examples": [to_exp_example(r) for r in sent_rows]},
        {"dataset": "CEBaB food+service aspect (Abraham et al. NeurIPS 2022)",
         "examples": [to_exp_example(r) for r in cebab_rows]},
        {"dataset": "LabHC/bias_in_bios boundary-null (De-Arteaga et al. 2019)",
         "examples": [to_exp_example(r) for r in bib_rows]},
    ]
    metadata = {
        "artifact": "CCRG supporting concept families + boundary-null (standardized to shared minimal-pair schema)",
        "schema_version": "ccrg_minimal_pair_v1",
        "row_schema_file": "schema.json",
        "emitted_format": "exp_sel_data_out (custom fields under metadata_* keys; logical view in schema.json)",
        "families": ["sentiment", "restaurant_aspect", "bias_in_bios_boundary"],
        "family_discriminator_field": "metadata_family",
        "is_surface_pair_note": "FALSE for every row; surface-flip pairs are out of scope here (reserved for sibling ParaDetox/LLM artifacts).",
        "no_derived_statistics_note": "Raw standardized data only; no MI/correlations/probes computed here.",
        "llm_spend_usd": 0.0,
        "total_rows": len(all_rows),
        "family_summary": {"sentiment": sent_sum, "restaurant_aspect": cebab_sum,
                           "bias_in_bios_boundary": bib_sum},
        "candidate_alternatives_considered": {
            "sentiment": ["tasksource/counterfactually-augmented-imdb (HF mirror, 68 dl)"],
            "restaurant_aspect": ["EleutherAI/CEBaB (HF mirror, cc-by-4.0)",
                                  "KarelDO/CEBaB_train_confounding_* (confound-controlled variants)"],
            "bias_in_bios_boundary": ["microsoft/biosbias (original scraper repo)"],
        },
    }
    out = {"metadata": metadata, "datasets": datasets}
    OUT_PATH.write_text(json.dumps(out, ensure_ascii=False))
    mb = OUT_PATH.stat().st_size / 1e6
    logger.info(f"Wrote {OUT_PATH.name}: {len(all_rows)} rows across 3 families, {mb:.1f} MB")
    for s in (sent_sum, cebab_sum, bib_sum):
        logger.info(f"  [{s['family']}] rows={s['n_rows']} labels={s['label_balance']} folds={s['fold_sizes']}")


if __name__ == "__main__":
    main()
