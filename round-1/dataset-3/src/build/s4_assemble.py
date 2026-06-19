"""STEP 4-6 — Cross-source de-dup, leakage-safe doc-level folds, schema
standardization, manifest, and full/mini/preview emission + validation.

Folds are assigned by a union-find over normalized-text keys: the two members
of every content/surface pair are linked, identical texts across components
collapse to one fold-group, and each group's fold is anchored to the native
civil_comments split when a classification row is present (else a stable
80/10/10 hash). This makes the invariants -- no pair_id and no
source_sentence_id spanning two folds, and no grouping text leaking into an
eval-fold classification row -- hold by construction.

Output (workspace root):
  data_out.json           (object form, exp_sel_data_out schema)
  data_summary.json       (manifest)
  mini_data_out.json / preview_data_out.json
"""
from __future__ import annotations

import collections
import json
import os
import random

from common import (FALLBACK_THRESHOLD, FLOAT_AXES, FOLDS, N_MIN,
                    PRIMARY_THRESHOLD, SUB_ATTRS, fold_from_ssid, get_logger,
                    make_row, norm_key, source_sentence_id)

LOG = get_logger("s4_assemble")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INTER = os.path.join(ROOT, "temp", "intermediate")
CONTENT_JSON = os.path.join(INTER, "content_pairs.json")
CLS_JSON = os.path.join(INTER, "classification.json")
SURFACE_JSON = os.path.join(INTER, "surface_pairs.json")
S3_STATS = os.path.join(INTER, "s3_stats.json")

DATA_OUT = os.path.join(ROOT, "data_out.json")
SUMMARY_OUT = os.path.join(ROOT, "data_summary.json")
MINI_OUT = os.path.join(ROOT, "mini_data_out.json")
PREVIEW_OUT = os.path.join(ROOT, "preview_data_out.json")


# --------------------------------------------------------------------------- #
# Union-Find for fold groups
# --------------------------------------------------------------------------- #

class UF:
    def __init__(self):
        self.p = {}

    def find(self, x):
        self.p.setdefault(x, x)
        root = x
        while self.p[root] != root:
            root = self.p[root]
        while self.p[x] != root:
            self.p[x], x = root, self.p[x]
        return root

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb


# --------------------------------------------------------------------------- #
# Load intermediates
# --------------------------------------------------------------------------- #

def load_json(path, default):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    LOG.warning("Missing %s -> using default", path)
    return default


def build():
    content = load_json(CONTENT_JSON, [])
    classification = load_json(CLS_JSON, [])
    surface = load_json(SURFACE_JSON, [])
    s3_stats = load_json(S3_STATS, {})
    LOG.info("Loaded content=%d classification=%d surface=%d",
             len(content), len(classification), len(surface))

    # ---- build union-find over normalized text keys ----
    uf = UF()
    for cp in content:
        uf.union("k:" + norm_key(cp["text_on"]), "k:" + norm_key(cp["text_off"]))
    for sp in surface:
        uf.union("k:" + norm_key(sp["text"]), "k:" + norm_key(sp["text_paired"]))
    for r in classification:
        uf.find("k:" + r["norm_key"])  # ensure node exists

    # native fold anchors from classification rows
    comp_native = collections.defaultdict(set)   # root -> set of native folds
    cls_fold_by_key = {}
    for r in classification:
        k = "k:" + r["norm_key"]
        comp_native[uf.find(k)].add(r["fold"])
        cls_fold_by_key[r["norm_key"]] = r["fold"]

    # decide ONE fold per component (so every member text of a component shares
    # a fold -> no text can land in two folds). Grouping-only components hash a
    # CANONICAL component key (the UF root), NOT a per-row ssid: multiple toxic
    # sources can share a neutral paraphrase, which links them into one
    # component that must therefore get a single fold.
    conflict_roots = set()
    comp_fold = {}
    for root in set(uf.find(x) for x in list(uf.p.keys())):
        natives = comp_native.get(root, set())
        if len(natives) == 0:
            comp_fold[root] = fold_from_ssid("comp_" + root)  # single fold, whole component
        elif len(natives) == 1:
            comp_fold[root] = next(iter(natives))             # anchored to native split
        else:
            conflict_roots.add(root)
            comp_fold[root] = "__CONFLICT__"
    LOG.info("Fold components=%d | conflict components=%d", len(comp_fold), len(conflict_roots))

    def key_fold(text, ssid=None):
        return comp_fold.get(uf.find("k:" + norm_key(text)), "__CONFLICT__")

    # cross-source collision report: keys present in >1 component-source
    # (a classification key also reachable from a grouping pair)
    cls_keys = set("k:" + r["norm_key"] for r in classification)
    grouping_keys = set()
    for cp in content:
        grouping_keys.add("k:" + norm_key(cp["text_on"]))
        grouping_keys.add("k:" + norm_key(cp["text_off"]))
    for sp in surface:
        grouping_keys.add("k:" + norm_key(sp["text"]))
    cross_collisions = len(cls_keys & grouping_keys)

    rows = []
    dropped_conflict = 0
    cp_i = sp_i = cls_i = 0

    # ---- classification rows (eval anchor) ----
    for r in classification:
        floats = {a: float(r["floats"].get(a, 0.0)) for a in FLOAT_AXES}
        sub_labels = {a: (1 if floats[a] >= PRIMARY_THRESHOLD else 0) for a in SUB_ATTRS}
        ssid = source_sentence_id(r["text"])
        fold = r["fold"]  # classification keeps native fold even in conflict comps
        rid = f"tox_cls_{cls_i:06d}"; cls_i += 1
        rows.append(make_row(
            rid=rid, input_text=r["text"],
            output_label=("toxic" if r["toxicity_label"] == 1 else "non_toxic"),
            fold=fold, record_type="classification", source="civil_comments",
            toxicity_label=r["toxicity_label"], ssid=ssid,
            subcontext_labels=sub_labels, subcontext_floats=floats,
            subcontext_threshold=PRIMARY_THRESHOLD))

    # ---- content pairs (grouping) ----
    for cp in content:
        fold = key_fold(cp["text_on"], cp["source_sentence_id"])
        if fold == "__CONFLICT__":
            dropped_conflict += 1
            continue
        rid = f"tox_cp_{cp_i:06d}"; cp_i += 1
        rows.append(make_row(
            rid=rid, input_text=cp["text_on"], output_label="toxic",
            fold=fold, record_type="content_pair", source="paradetox",
            toxicity_label=1, text_on=cp["text_on"], text_off=cp["text_off"],
            pair_id=cp["pair_id"], ssid=cp["source_sentence_id"],
            is_content_pair=True))

    # ---- surface pairs (grouping) ----
    for sp in surface:
        fold = key_fold(sp["text"], sp["source_sentence_id"])
        if fold == "__CONFLICT__":
            dropped_conflict += 1
            continue
        sub_labels = sp.get("subcontext_labels")
        floats = sp.get("subcontext_floats")
        if floats is not None:
            floats = {a: float(floats.get(a, 0.0)) for a in FLOAT_AXES}
        thr = PRIMARY_THRESHOLD if sub_labels is not None else None
        rid = f"tox_sp_{sp_i:06d}"; sp_i += 1
        rows.append(make_row(
            rid=rid, input_text=sp["text"], output_label="toxic",
            fold=fold, record_type="surface_pair", source="generated_paraphrase",
            toxicity_label=1, text_paired=sp["text_paired"], pair_id=sp["pair_id"],
            ssid=sp["source_sentence_id"], is_surface_pair=True,
            subcontext_labels=sub_labels, subcontext_floats=floats,
            subcontext_threshold=thr, judge_pass=bool(sp.get("judge_pass")),
            gen_model=sp.get("gen_model")))

    LOG.info("Standardized rows=%d (cp=%d sp=%d cls=%d) | dropped_conflict=%d cross_collisions=%d",
             len(rows), cp_i, sp_i, cls_i, dropped_conflict, cross_collisions)

    summary = build_summary(rows, classification, s3_stats, cross_collisions, dropped_conflict)
    verify_invariants(rows)
    emit(rows, summary)
    return rows, summary


# --------------------------------------------------------------------------- #
# Summary / manifest
# --------------------------------------------------------------------------- #

def build_summary(rows, classification, s3_stats, cross_collisions, dropped_conflict):
    by_type = collections.Counter(r["metadata_record_type"] for r in rows)
    by_fold = collections.Counter(r["metadata_fold"] for r in rows)
    by_label = collections.Counter(r["metadata_toxicity_label"] for r in rows)

    # per-sub-context per-fold positive counts at 0.5 AND 0.3 (classification only)
    sub_counts = {thr: {a: {f: 0 for f in FOLDS} for a in SUB_ATTRS}
                  for thr in (PRIMARY_THRESHOLD, FALLBACK_THRESHOLD)}
    cls_rows = [r for r in rows if r["metadata_record_type"] == "classification"]
    for r in cls_rows:
        fl = r["metadata_subcontext_floats"]
        f = r["metadata_fold"]
        for a in SUB_ATTRS:
            v = fl.get(a) or 0.0
            for thr in (PRIMARY_THRESHOLD, FALLBACK_THRESHOLD):
                if v >= thr:
                    sub_counts[thr][a][f] += 1

    subcontext_report = {}
    for a in SUB_ATTRS:
        rep = {}
        for thr in (PRIMARY_THRESHOLD, FALLBACK_THRESHOLD):
            per_fold = sub_counts[thr][a]
            total = sum(per_fold.values())
            rep[f"threshold_{thr}"] = {
                "per_fold": per_fold, "total": total,
                "meets_n_min_overall": total >= N_MIN,
                "meets_n_min_each_eval_fold": all(per_fold[f] >= N_MIN for f in ("val", "test")),
            }
        # decision: usable inferentially at primary, else fallback, else descriptive-only
        if rep[f"threshold_{PRIMARY_THRESHOLD}"]["total"] >= N_MIN:
            rep["status"] = "inferential@0.5"
        elif rep[f"threshold_{FALLBACK_THRESHOLD}"]["total"] >= N_MIN:
            rep["status"] = "inferential@0.3_fallback"
        else:
            rep["status"] = "descriptive_only"
        subcontext_report[a] = rep

    # pairwise co-occurrence matrix among toxic classification rows (at 0.5)
    toxic_cls = [r for r in cls_rows if r["metadata_toxicity_label"] == 1]
    cooc = {a: {b: 0 for b in SUB_ATTRS} for a in SUB_ATTRS}
    sub_marginal = {a: 0 for a in SUB_ATTRS}
    for r in toxic_cls:
        present = [a for a in SUB_ATTRS if (r["metadata_subcontext_labels"].get(a) == 1)]
        for a in present:
            sub_marginal[a] += 1
            for b in present:
                cooc[a][b] += 1
    # jaccard-style overlap to inform C-track(shared-support) vs K-track(disjoint)
    overlap = {a: {b: 0.0 for b in SUB_ATTRS} for a in SUB_ATTRS}
    for a in SUB_ATTRS:
        for b in SUB_ATTRS:
            union = sub_marginal[a] + sub_marginal[b] - cooc[a][b]
            overlap[a][b] = round(cooc[a][b] / union, 3) if union else 0.0

    summary = {
        "title": "Two-Track CCRG Toxicity Dataset Family",
        "components": {
            "content_pair": "ParaDetox human toxic<->neutral CONTENT-FLIP pairs (non-circular perturbation P)",
            "surface_pair": "OpenRouter-generated toxic->toxic SURFACE-FLIP pairs (surface-invariance control)",
            "classification": "civil_comments rows w/ binary toxicity label + FROZEN multi-label sub-context labels",
        },
        "sources": {
            "paradetox": "s-nlp/paradetox (Logacheva et al., ACL 2022; license openrail++)",
            "civil_comments": "google/civil_comments (Jigsaw Unintended Bias, Borkan et al. 2019; CC0 1.0)",
            "generated_paraphrase": s3_stats.get("gen_model", "openrouter (see s3_stats)"),
        },
        "canonical_representation": "ONE row per pair: content_pair carries text_on/text_off; surface_pair carries input/text_paired; classification is one row per comment.",
        "totals": {
            "rows": len(rows),
            "by_record_type": dict(by_type),
            "by_fold": dict(by_fold),
            "by_toxicity_label": {str(k): v for k, v in by_label.items()},
        },
        "subcontext_report": subcontext_report,
        "subcontext_marginal_toxic_cls@0.5": sub_marginal,
        "subcontext_cooccurrence_counts@0.5": cooc,
        "subcontext_jaccard_overlap@0.5": overlap,
        "surface_generation": s3_stats,
        "cross_source_collisions_reconciled": cross_collisions,
        "grouping_rows_dropped_fold_conflict": dropped_conflict,
        "thresholds": {"primary": PRIMARY_THRESHOLD, "fallback": FALLBACK_THRESHOLD,
                       "clean_negative_ceiling": 0.2, "n_min": N_MIN},
        "n_unique_source_sentence_ids": len(set(r["metadata_source_sentence_id"]
                                                for r in rows if r["metadata_source_sentence_id"])),
    }
    return summary


# --------------------------------------------------------------------------- #
# Invariant checks
# --------------------------------------------------------------------------- #

def verify_invariants(rows):
    # folds in allowed set
    bad_fold = [r["metadata_id"] for r in rows if r["metadata_fold"] not in FOLDS]
    assert not bad_fold, f"rows with bad fold: {bad_fold[:5]}"
    # pair_id never spans two folds
    pf = collections.defaultdict(set)
    for r in rows:
        if r["metadata_pair_id"]:
            pf[r["metadata_pair_id"]].add(r["metadata_fold"])
    span_pair = [p for p, fs in pf.items() if len(fs) > 1]
    assert not span_pair, f"pair_id spanning folds: {span_pair[:5]}"
    # source_sentence_id never spans two folds
    sf = collections.defaultdict(set)
    for r in rows:
        if r["metadata_source_sentence_id"]:
            sf[r["metadata_source_sentence_id"]].add(r["metadata_fold"])
    span_ssid = [s for s, fs in sf.items() if len(fs) > 1]
    assert not span_ssid, f"ssid spanning folds: {span_ssid[:5]} (n={len(span_ssid)})"
    # labels binary, floats in [0,1]
    for r in rows:
        assert r["metadata_toxicity_label"] in (0, 1)
        for a, v in r["metadata_subcontext_labels"].items():
            assert v in (0, 1, None), f"bad sublabel {a}={v}"
        if r["metadata_subcontext_floats"]:
            for a, v in r["metadata_subcontext_floats"].items():
                assert v is None or (0.0 <= v <= 1.0), f"float out of range {a}={v}"
    LOG.info("Invariant checks PASSED (folds, pair_id, ssid, labels, floats)")


# --------------------------------------------------------------------------- #
# Emit object-form data_out + variants
# --------------------------------------------------------------------------- #

def _group_examples(rows):
    groups = {
        "paradetox_content_flips": [r for r in rows if r["metadata_record_type"] == "content_pair"],
        "civil_comments_subcontext": [r for r in rows if r["metadata_record_type"] == "classification"],
        "generated_surface_flips": [r for r in rows if r["metadata_record_type"] == "surface_pair"],
    }
    return groups


def _to_obj(groups, metadata):
    datasets = []
    for name, exs in groups.items():
        if exs:  # schema requires minItems>=1
            datasets.append({"dataset": name, "examples": exs})
    return {"metadata": metadata, "datasets": datasets}


def emit(rows, summary):
    groups = _group_examples(rows)
    obj = _to_obj(groups, summary)
    with open(DATA_OUT, "w") as f:
        json.dump(obj, f)
    with open(SUMMARY_OUT, "w") as f:
        json.dump(summary, f, indent=2)
    LOG.info("Wrote %s and %s", DATA_OUT, SUMMARY_OUT)

    # mini: ~200 rows balanced across record_type x fold x label
    rng = random.Random(7)
    mini_rows = _balanced_sample(rows, target=200, rng=rng)
    mini_groups = _group_examples(mini_rows)
    # guarantee >=1 per group
    for name, exs in _group_examples(rows).items():
        if exs and not mini_groups.get(name):
            mini_groups[name] = exs[:1]
    mini_meta = {"note": "mini variant (~200 balanced rows)", "parent": "data_out.json",
                 "totals": {"rows": sum(len(v) for v in mini_groups.values())}}
    with open(MINI_OUT, "w") as f:
        json.dump(_to_obj(mini_groups, mini_meta), f, indent=2)

    # preview: a few rows covering each record_type + a couple sub-contexts
    preview_rows = _preview_sample(rows)
    prev_groups = _group_examples(preview_rows)
    prev_meta = {"note": "preview variant (one of each record_type + sub-contexts, strings full)",
                 "parent": "data_out.json"}
    with open(PREVIEW_OUT, "w") as f:
        json.dump(_to_obj(prev_groups, prev_meta), f, indent=2)
    LOG.info("Wrote %s (%d rows) and %s (%d rows)", MINI_OUT, len(mini_rows), PREVIEW_OUT, len(preview_rows))


def _balanced_sample(rows, target, rng):
    buckets = collections.defaultdict(list)
    for r in rows:
        key = (r["metadata_record_type"], r["metadata_fold"], r["metadata_toxicity_label"])
        buckets[key].append(r)
    keys = list(buckets.keys())
    per = max(1, target // max(1, len(keys)))
    out = []
    for k in keys:
        pool = buckets[k][:]
        rng.shuffle(pool)
        out.extend(pool[:per])
    rng.shuffle(out)
    return out[:target]


def _preview_sample(rows):
    out = []
    # one content_pair, one surface_pair
    for rt in ("content_pair", "surface_pair"):
        for r in rows:
            if r["metadata_record_type"] == rt:
                out.append(r); break
    # a couple of classification rows for distinct sub-contexts + a non-toxic
    want = ["insult", "identity_attack", "obscene"]
    for a in want:
        for r in rows:
            if (r["metadata_record_type"] == "classification"
                    and r["metadata_subcontext_labels"].get(a) == 1):
                out.append(r); break
    for r in rows:
        if r["metadata_record_type"] == "classification" and r["metadata_toxicity_label"] == 0:
            out.append(r); break
    # de-dup by id, cap ~8
    seen, uniq = set(), []
    for r in out:
        if r["metadata_id"] not in seen:
            seen.add(r["metadata_id"]); uniq.append(r)
    return uniq[:8]


if __name__ == "__main__":
    build()
