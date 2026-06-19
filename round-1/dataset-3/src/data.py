# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Consolidated, self-contained assembler for the Two-Track CCRG TOXICITY
dataset family. Reproducible, stdlib-only, deterministic.

  uv run data.py

Reads the three component inputs (all text-only, no activations):
  * ParaDetox CONTENT-FLIP source  -> temp/datasets/full_s-nlp_paradetox_default_train.json
        (HuggingFace s-nlp/paradetox, downloaded via the aii-hf-datasets skill)
  * civil_comments sub-context set -> temp/intermediate/classification.json
        (stream-filtered + stratified by build/s2_classification.py)
  * generated SURFACE-FLIP pairs   -> temp/intermediate/surface_pairs.json
        (OpenRouter gpt-4o-mini, double-gated, by build/s3_surface_flips.py;
         cached so re-runs cost $0 and stay deterministic)

THE BEST 2 DATASETS (target_num_datasets=2) are the two real, well-documented,
permissively-licensed HuggingFace SOURCE corpora:
  1. paradetox       (Logacheva et al., ACL 2022; openrail++)
  2. civil_comments  (Jigsaw Unintended Bias, Borkan et al. 2019; CC0 1.0)
The LLM-GENERATED surface-flip pairs are folded into the group of the SOURCE
corpus their seed sentence came from (metadata_origin_source), so the family
still carries all three record_types (content_pair / surface_pair /
classification) while presenting exactly two dataset groups.

Outputs (workspace root):
  data_out.json      -> exp_sel_data_out schema, input to the aii-json format script
  full_data_out.json -> identical full copy (the canonical full deliverable)
  data_summary.json  -> manifest (power, co-occurrence, generation stats, leakage report)
"""
from __future__ import annotations

import collections
import hashlib
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR = os.path.join(HERE, "temp", "datasets")
INTER_DIR = os.path.join(HERE, "temp", "intermediate")
PARADETOX_JSON = os.path.join(DATASETS_DIR, "full_s-nlp_paradetox_default_train.json")
CLS_JSON = os.path.join(INTER_DIR, "classification.json")
SURFACE_JSON = os.path.join(INTER_DIR, "surface_pairs.json")
S3_STATS = os.path.join(INTER_DIR, "s3_stats.json")

DATA_OUT = os.path.join(HERE, "data_out.json")
FULL_OUT = os.path.join(HERE, "full_data_out.json")
SUMMARY_OUT = os.path.join(HERE, "data_summary.json")

SUB_ATTRS = ["severe_toxicity", "obscene", "threat", "insult",
             "identity_attack", "sexual_explicit"]
FLOAT_AXES = ["toxicity"] + SUB_ATTRS
PRIMARY_THRESHOLD, FALLBACK_THRESHOLD, N_MIN = 0.5, 0.3, 150
FOLDS = ("train", "val", "test")

_WS = re.compile(r"\s+")
_PUNCT = re.compile(r"[^\w\s]", flags=re.UNICODE)
_HTML_ENT = re.compile(r"&(amp|lt|gt|quot|#39|nbsp|apos);")
_HTML_ENT_MAP = {"&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"',
                 "&#39;": "'", "&nbsp;": " ", "&apos;": "'"}


def log(msg):
    print("[data.py] " + msg, flush=True)


# --------------------------------------------------------------------------- #
# Text helpers (mirror build/common.py so this script is standalone)
# --------------------------------------------------------------------------- #

def clean_text(text):
    if text is None:
        return ""
    t = _HTML_ENT.sub(lambda m: _HTML_ENT_MAP.get(m.group(0), m.group(0)), str(text))
    t = t.replace(" ", " ").replace("\r", " ").replace("\n", " ")
    return _WS.sub(" ", t).strip()


def norm_key(text):
    t = _PUNCT.sub(" ", clean_text(text).lower())
    return _WS.sub(" ", t).strip()


def sha16(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]


def ssid_of(toxic_text):
    return "ssid_" + sha16(norm_key(toxic_text))


def fold_from_key(key, ratios=(0.8, 0.1, 0.1)):
    bucket = int(hashlib.sha1(key.encode("utf-8")).hexdigest(), 16) % 1000
    tcut = int(ratios[0] * 1000)
    vcut = tcut + int(ratios[1] * 1000)
    return "train" if bucket < tcut else ("val" if bucket < vcut else "test")


# --------------------------------------------------------------------------- #
# Union-Find for leakage-safe fold groups
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
# Shared row schema (exp_sel_data_out: input/output/metadata_* only)
# --------------------------------------------------------------------------- #

def make_row(rid, input_text, output_label, fold, record_type, source,
             origin_source, toxicity_label, *, text_on=None, text_off=None,
             text_paired=None, pair_id=None, ssid=None, is_content_pair=False,
             is_surface_pair=False, subcontext_labels=None, subcontext_floats=None,
             subcontext_threshold=None, judge_pass=None, gen_model=None,
             surface_metrics=None):
    if subcontext_labels is None:
        subcontext_labels = {a: None for a in SUB_ATTRS}
    if subcontext_floats is None:
        subcontext_floats = {a: None for a in FLOAT_AXES}
    return {
        "input": input_text,
        "output": output_label,
        "metadata_id": rid,
        "metadata_fold": fold,
        "metadata_record_type": record_type,
        "metadata_source": source,
        "metadata_origin_source": origin_source,
        "metadata_toxicity_label": int(toxicity_label),
        "metadata_text_on": text_on,
        "metadata_text_off": text_off,
        "metadata_text_paired": text_paired,
        "metadata_pair_id": pair_id,
        "metadata_source_sentence_id": ssid,
        "metadata_is_content_pair": bool(is_content_pair),
        "metadata_is_surface_pair": bool(is_surface_pair),
        "metadata_subcontext_labels": subcontext_labels,
        "metadata_subcontext_floats": subcontext_floats,
        "metadata_subcontext_threshold": subcontext_threshold,
        "metadata_judge_pass": judge_pass,
        "metadata_gen_model": gen_model,
        "metadata_surface_metrics": surface_metrics,
    }


# --------------------------------------------------------------------------- #
# Component loaders
# --------------------------------------------------------------------------- #

def load_paradetox_content_pairs():
    if not os.path.exists(PARADETOX_JSON):
        raise SystemExit(f"Missing {PARADETOX_JSON}; download via aii-hf-datasets (s-nlp/paradetox).")
    with open(PARADETOX_JSON) as f:
        data = json.load(f)
    rows = data["rows"] if isinstance(data, dict) and "rows" in data else data
    seen, out = set(), []
    n_same = n_dup = n_empty = 0
    for r in rows:
        toxic = clean_text(r.get("en_toxic_comment", ""))
        neutral = clean_text(r.get("en_neutral_comment", ""))
        if not toxic or not neutral:
            n_empty += 1
            continue
        if norm_key(toxic) == norm_key(neutral):
            n_same += 1
            continue
        dk = (toxic.lower(), neutral.lower())
        if dk in seen:
            n_dup += 1
            continue
        seen.add(dk)
        out.append({"text_on": toxic, "text_off": neutral,
                    "pair_id": "cp_" + sha16(toxic.lower() + "||" + neutral.lower()),
                    "ssid": ssid_of(toxic)})
    log(f"ParaDetox content pairs: kept={len(out)} (empty={n_empty} same={n_same} dup={n_dup}); "
        f"unique toxic sources={len({o['ssid'] for o in out})}")
    return out


def load_cached(path, what):
    if not os.path.exists(path):
        raise SystemExit(f"Missing {path}. Regenerate with build/ ({what}).")
    with open(path) as f:
        return json.load(f)


# --------------------------------------------------------------------------- #
# Assemble
# --------------------------------------------------------------------------- #

def assemble():
    content = load_paradetox_content_pairs()
    classification = load_cached(CLS_JSON, "build/s2_classification.py — civil_comments stream-filter")
    surface = load_cached(SURFACE_JSON, "build/s3_surface_flips.py — OpenRouter surface generation")
    s3_stats = json.load(open(S3_STATS)) if os.path.exists(S3_STATS) else {}
    log(f"Inputs: content={len(content)} classification={len(classification)} surface={len(surface)}")

    # ---- union-find over normalized text keys ----
    uf = UF()
    for cp in content:
        uf.union("k:" + norm_key(cp["text_on"]), "k:" + norm_key(cp["text_off"]))
    for sp in surface:
        uf.union("k:" + norm_key(sp["text"]), "k:" + norm_key(sp["text_paired"]))
    for r in classification:
        uf.find("k:" + r["norm_key"])

    comp_native = collections.defaultdict(set)
    for r in classification:
        comp_native[uf.find("k:" + r["norm_key"])].add(r["fold"])

    conflict = set()
    comp_fold = {}
    for root in set(uf.find(x) for x in list(uf.p.keys())):
        nats = comp_native.get(root, set())
        if len(nats) == 0:
            comp_fold[root] = fold_from_key("comp_" + root)   # one fold for whole component
        elif len(nats) == 1:
            comp_fold[root] = next(iter(nats))
        else:
            conflict.add(root)
            comp_fold[root] = "__CONFLICT__"
    log(f"Fold components={len(comp_fold)} conflict={len(conflict)}")

    def key_fold(text):
        return comp_fold.get(uf.find("k:" + norm_key(text)), "__CONFLICT__")

    cls_keys = set("k:" + r["norm_key"] for r in classification)
    grouping_keys = set()
    for cp in content:
        grouping_keys.add("k:" + norm_key(cp["text_on"]))
        grouping_keys.add("k:" + norm_key(cp["text_off"]))
    for sp in surface:
        grouping_keys.add("k:" + norm_key(sp["text"]))
    cross_collisions = len(cls_keys & grouping_keys)

    rows = []
    dropped = 0
    ci = si = li = 0

    # classification rows (eval anchor; keep native fold)
    for r in classification:
        floats = {a: float(r["floats"].get(a, 0.0)) for a in FLOAT_AXES}
        sub_labels = {a: (1 if floats[a] >= PRIMARY_THRESHOLD else 0) for a in SUB_ATTRS}
        rid = f"tox_cls_{li:06d}"; li += 1
        rows.append(make_row(rid, r["text"],
                             "toxic" if r["toxicity_label"] == 1 else "non_toxic",
                             r["fold"], "classification", "civil_comments", "civil_comments",
                             r["toxicity_label"], ssid=ssid_of(r["text"]),
                             subcontext_labels=sub_labels, subcontext_floats=floats,
                             subcontext_threshold=PRIMARY_THRESHOLD))

    # content pairs (grouping)
    for cp in content:
        f = key_fold(cp["text_on"])
        if f == "__CONFLICT__":
            dropped += 1
            continue
        rid = f"tox_cp_{ci:06d}"; ci += 1
        rows.append(make_row(rid, cp["text_on"], "toxic", f, "content_pair",
                             "paradetox", "paradetox", 1, text_on=cp["text_on"],
                             text_off=cp["text_off"], pair_id=cp["pair_id"],
                             ssid=cp["ssid"], is_content_pair=True))

    # surface pairs (grouping; folded into origin-source group)
    for sp in surface:
        f = key_fold(sp["text"])
        if f == "__CONFLICT__":
            dropped += 1
            continue
        floats = sp.get("subcontext_floats")
        if floats is not None:
            floats = {a: float(floats.get(a, 0.0)) for a in FLOAT_AXES}
        sub_labels = sp.get("subcontext_labels")
        origin = sp.get("origin_source", "paradetox")
        rid = f"tox_sp_{si:06d}"; si += 1
        rows.append(make_row(rid, sp["text"], "toxic", f, "surface_pair",
                             "generated_paraphrase", origin, 1,
                             text_paired=sp["text_paired"], pair_id=sp["pair_id"],
                             ssid=sp.get("source_sentence_id") or ssid_of(sp["text"]),
                             is_surface_pair=True, subcontext_labels=sub_labels,
                             subcontext_floats=floats,
                             subcontext_threshold=(PRIMARY_THRESHOLD if sub_labels else None),
                             judge_pass=bool(sp.get("judge_pass")),
                             gen_model=sp.get("gen_model"),
                             surface_metrics=sp.get("surface_metrics")))

    log(f"Rows={len(rows)} (cls={li} cp={ci} sp={si}) dropped_conflict={dropped} cross_collisions={cross_collisions}")
    verify(rows)
    summary = build_summary(rows, s3_stats, cross_collisions, dropped)
    emit(rows, summary)
    return rows, summary


# --------------------------------------------------------------------------- #
# Invariants
# --------------------------------------------------------------------------- #

def verify(rows):
    assert all(r["metadata_fold"] in FOLDS for r in rows), "bad fold"
    pf, sf, kf = collections.defaultdict(set), collections.defaultdict(set), collections.defaultdict(set)
    for r in rows:
        if r["metadata_pair_id"]:
            pf[r["metadata_pair_id"]].add(r["metadata_fold"])
        if r["metadata_source_sentence_id"]:
            sf[r["metadata_source_sentence_id"]].add(r["metadata_fold"])
        for m in (r["input"], r["metadata_text_off"], r["metadata_text_paired"]):
            if m:
                kf[norm_key(m)].add(r["metadata_fold"])
    assert not [p for p, s in pf.items() if len(s) > 1], "pair_id spans folds"
    assert not [s for s, v in sf.items() if len(v) > 1], "ssid spans folds"
    leaks = [k for k, v in kf.items() if len(v) > 1]
    assert not leaks, f"{len(leaks)} texts span folds (leakage)"
    for r in rows:
        assert r["metadata_toxicity_label"] in (0, 1)
        for v in r["metadata_subcontext_labels"].values():
            assert v in (0, 1, None)
        if r["metadata_subcontext_floats"]:
            for v in r["metadata_subcontext_floats"].values():
                assert v is None or 0.0 <= v <= 1.0
    log("Invariants PASSED (folds, pair_id, ssid, no text in >1 fold, binary labels, floats in [0,1])")


# --------------------------------------------------------------------------- #
# Summary
# --------------------------------------------------------------------------- #

def build_summary(rows, s3_stats, cross_collisions, dropped):
    cls = [r for r in rows if r["metadata_record_type"] == "classification"]
    counts = {thr: {a: {f: 0 for f in FOLDS} for a in SUB_ATTRS}
              for thr in (PRIMARY_THRESHOLD, FALLBACK_THRESHOLD)}
    for r in cls:
        fl, fold = r["metadata_subcontext_floats"], r["metadata_fold"]
        for a in SUB_ATTRS:
            for thr in (PRIMARY_THRESHOLD, FALLBACK_THRESHOLD):
                if (fl.get(a) or 0.0) >= thr:
                    counts[thr][a][fold] += 1
    sub_report = {}
    for a in SUB_ATTRS:
        rep = {}
        for thr in (PRIMARY_THRESHOLD, FALLBACK_THRESHOLD):
            pf = counts[thr][a]
            tot = sum(pf.values())
            rep[f"threshold_{thr}"] = {"per_fold": pf, "total": tot,
                                       "meets_n_min_overall": tot >= N_MIN,
                                       "meets_n_min_each_eval_fold": all(pf[f] >= N_MIN for f in ("val", "test"))}
        if rep[f"threshold_{PRIMARY_THRESHOLD}"]["total"] >= N_MIN:
            rep["status"] = "inferential@0.5"
        elif rep[f"threshold_{FALLBACK_THRESHOLD}"]["total"] >= N_MIN:
            rep["status"] = "inferential@0.3_fallback"
        else:
            rep["status"] = "descriptive_only"
        sub_report[a] = rep

    toxic_cls = [r for r in cls if r["metadata_toxicity_label"] == 1]
    cooc = {a: {b: 0 for b in SUB_ATTRS} for a in SUB_ATTRS}
    marg = {a: 0 for a in SUB_ATTRS}
    for r in toxic_cls:
        present = [a for a in SUB_ATTRS if r["metadata_subcontext_labels"].get(a) == 1]
        for a in present:
            marg[a] += 1
            for b in present:
                cooc[a][b] += 1
    overlap = {a: {b: (round(cooc[a][b] / (marg[a] + marg[b] - cooc[a][b]), 3)
                        if (marg[a] + marg[b] - cooc[a][b]) else 0.0) for b in SUB_ATTRS}
               for a in SUB_ATTRS}

    grp = collections.Counter(group_of(r) for r in rows)
    return {
        "title": "Two-Track CCRG Toxicity Dataset Family",
        "best_2_datasets": ["paradetox", "civil_comments"],
        "components": {
            "content_pair": "ParaDetox human toxic<->neutral CONTENT-FLIP pairs (non-circular perturbation P)",
            "surface_pair": "OpenRouter-generated toxic->toxic SURFACE-FLIP pairs (surface-invariance control)",
            "classification": "civil_comments rows + binary toxicity label + FROZEN multi-label sub-context labels",
        },
        "dataset_groups": {
            "paradetox": "ParaDetox content_pair rows + paradetox-origin surface_pair rows (Logacheva et al. ACL 2022; openrail++)",
            "civil_comments": "civil_comments classification rows + civil-origin surface_pair rows (Borkan et al. 2019; CC0 1.0)",
        },
        "canonical_representation": "ONE row per pair (content_pair: text_on/text_off; surface_pair: input/text_paired); classification: one row per comment. Surface pairs grouped by metadata_origin_source.",
        "totals": {
            "rows": len(rows),
            "by_record_type": dict(collections.Counter(r["metadata_record_type"] for r in rows)),
            "by_dataset_group": dict(grp),
            "by_fold": dict(collections.Counter(r["metadata_fold"] for r in rows)),
            "by_toxicity_label": {str(k): v for k, v in collections.Counter(r["metadata_toxicity_label"] for r in rows).items()},
        },
        "subcontext_report": sub_report,
        "subcontext_marginal_toxic_cls@0.5": marg,
        "subcontext_cooccurrence_counts@0.5": cooc,
        "subcontext_jaccard_overlap@0.5": overlap,
        "surface_generation": s3_stats,
        "cross_source_collisions_reconciled": cross_collisions,
        "grouping_rows_dropped_fold_conflict": dropped,
        "thresholds": {"primary": PRIMARY_THRESHOLD, "fallback": FALLBACK_THRESHOLD,
                       "clean_negative_ceiling": 0.2, "n_min": N_MIN},
    }


# --------------------------------------------------------------------------- #
# Emit (2 dataset groups, representative ordering for the 3-row mini slice)
# --------------------------------------------------------------------------- #

def group_of(r):
    return "paradetox" if r["metadata_origin_source"] == "paradetox" else "civil_comments"


def _representative_order(examples):
    """Put a diverse head first so the format script's 3-example mini slice
    covers multiple record_types / labels."""
    seen_keys, head, tail = set(), [], []
    def key(r):
        return (r["metadata_record_type"], r["metadata_toxicity_label"])
    for r in examples:
        k = key(r)
        if k not in seen_keys:
            seen_keys.add(k); head.append(r)
        else:
            tail.append(r)
    return head + tail


def emit(rows, summary):
    groups = collections.OrderedDict([("paradetox", []), ("civil_comments", [])])
    for r in rows:
        groups[group_of(r)].append(r)
    datasets = [{"dataset": name, "examples": _representative_order(exs)}
                for name, exs in groups.items() if exs]
    obj = {"metadata": summary, "datasets": datasets}
    with open(FULL_OUT, "w") as f:
        json.dump(obj, f)
    with open(SUMMARY_OUT, "w") as f:
        json.dump(summary, f, indent=2)
    log(f"Wrote {os.path.basename(FULL_OUT)}, {os.path.basename(SUMMARY_OUT)}")
    log("dataset groups: " + ", ".join(f"{d['dataset']}={len(d['examples'])}" for d in datasets))


if __name__ == "__main__":
    assemble()
