"""STEP 2 — Independent sub-context classification set from civil_comments.

Streams google/civil_comments (CC0, ~1.8M train + 97k val + 97k test), keeps
toxic positives (stratified to maximise the rare sub-contexts threat /
identity_attack) plus clean non-toxic negatives, and preserves the raw float
vector on every kept row so the binary sub-context labels can be re-derived at
either the primary (0.5) or fallback (0.3) threshold downstream.

Sub-context labels are FROZEN here, before any SAE comparison, and are
multi-label (a comment can be both insulting and obscene) — the degenerate-
construction guard for the C-track-vs-K-track (shared-support vs disjoint)
question.

Output: temp/intermediate/classification.json
"""
from __future__ import annotations

import json
import os

from common import (CLEAN_NEG_CEILING, FALLBACK_THRESHOLD, FLOAT_AXES,
                    PRIMARY_THRESHOLD, SUB_ATTRS, clean_text, get_logger,
                    norm_key, sha16)

LOG = get_logger("s2_cls")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "temp", "intermediate", "classification.json")

# Per-split quotas (fold inherits the native civil_comments split).
SPLIT_CFG = {
    "train":      {"fold": "train", "sub_quota": 1000, "generic_quota": 1500, "neg_quota": 9000},
    "validation": {"fold": "val",   "sub_quota": 250,  "generic_quota": 400,  "neg_quota": 2500},
    "test":       {"fold": "test",  "sub_quota": 250,  "generic_quota": 400,  "neg_quota": 2500},
}
# Hard safety cap on rows scanned per split (train is ~1.8M; we want a full
# pass to recover rare sub-contexts, so set comfortably above the real size).
MAX_SCAN = {"train": 2_000_000, "validation": 120_000, "test": 120_000}


def collect_split(split_name: str, cfg: dict, seen_norm: set):
    from datasets import load_dataset
    ds = load_dataset("google/civil_comments", split=split_name, streaming=True)
    sub_quota = cfg["sub_quota"]
    sub_counts = {a: 0 for a in SUB_ATTRS}     # counted at 0.5 among KEPT toxic
    generic_count = 0
    neg_count = 0
    kept = []
    scanned = 0
    for row in ds:
        scanned += 1
        if scanned > MAX_SCAN[split_name]:
            break
        if scanned % 200_000 == 0:
            LOG.info("[%s] scanned=%d kept=%d sub=%s gen=%d neg=%d",
                     split_name, scanned, len(kept),
                     {a: sub_counts[a] for a in SUB_ATTRS}, generic_count, neg_count)
        text = clean_text(row.get("text", ""))
        if len(text) < 3:
            continue
        tox = float(row.get("toxicity") or 0.0)
        floats = {a: float(row.get(a) or 0.0) for a in FLOAT_AXES}

        if tox >= PRIMARY_THRESHOLD:
            present = [a for a in SUB_ATTRS if floats[a] >= PRIMARY_THRESHOLD]
            helps = any(sub_counts[a] < sub_quota for a in present)
            if helps:
                role = "toxic_subattr"
            elif not present and generic_count < cfg["generic_quota"]:
                role = "toxic_generic"
            else:
                continue  # all relevant buckets full
        elif tox < CLEAN_NEG_CEILING:
            if neg_count >= cfg["neg_quota"]:
                continue
            role = "nontoxic"
        else:
            continue  # ambiguous 0.2-0.5 band excluded for clean labels

        nk = norm_key(text)
        if not nk or nk in seen_norm:
            continue
        seen_norm.add(nk)

        if role == "toxic_subattr":
            for a in [x for x in SUB_ATTRS if floats[x] >= PRIMARY_THRESHOLD]:
                sub_counts[a] += 1
        elif role == "toxic_generic":
            generic_count += 1
        else:
            neg_count += 1

        kept.append({
            "record_type": "classification",
            "source": "civil_comments",
            "text": text,
            "norm_key": nk,
            "toxicity_label": 1 if tox >= PRIMARY_THRESHOLD else 0,
            "floats": floats,
            "role": role,
            "fold": cfg["fold"],
            "id_seed": sha16(nk),
        })
    LOG.info("[%s] DONE scanned=%d kept=%d | sub@0.5=%s generic=%d neg=%d",
             split_name, scanned, len(kept), sub_counts, generic_count, neg_count)
    return kept


def build():
    seen_norm = set()
    all_kept = []
    for split_name, cfg in SPLIT_CFG.items():
        all_kept.extend(collect_split(split_name, cfg, seen_norm))

    # Balance: trim non-toxic per fold so toxic:non-toxic is ~1:1 within fold.
    import collections
    by_fold = collections.defaultdict(list)
    for r in all_kept:
        by_fold[r["fold"]].append(r)
    balanced = []
    for fold, rows in by_fold.items():
        tox = [r for r in rows if r["toxicity_label"] == 1]
        neg = [r for r in rows if r["toxicity_label"] == 0]
        keep_neg = neg[:max(len(tox), 1)]  # stream order is deterministic
        balanced.extend(tox + keep_neg)
        LOG.info("[%s] balanced: toxic=%d nontoxic_kept=%d (of %d)",
                 fold, len(tox), len(keep_neg), len(neg))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(balanced, f)
    LOG.info("Wrote %s (%d rows)", OUT, len(balanced))
    return balanced


if __name__ == "__main__":
    build()
