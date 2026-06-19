"""Independent re-verification of the emitted data_out.json + a quick baseline
to confirm the dataset carries the signal the downstream experiment needs.

Checks (read fresh from data_out.json, not from in-memory state):
  1. No pair_id and no source_sentence_id spans two folds.
  2. No GROUPING text (content/surface pair member) appears as an EVAL-fold
     (val/test) classification row -> no grouping->eval leakage.
  3. Baseline A: TF-IDF + logistic regression toxicity classifier
     (train -> test) -> confirms the classification set is learnable.
  4. Baseline B: content-pair separability -> mean |a_on - a_off| signal proxy
     via TF-IDF cosine, confirming toxic vs neutral members differ.
"""
from __future__ import annotations

import collections
import json
import os

from common import SUB_ATTRS, norm_key

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_OUT = os.path.join(ROOT, "data_out.json")


def load_rows():
    with open(DATA_OUT) as f:
        obj = json.load(f)
    rows = []
    for ds in obj["datasets"]:
        rows.extend(ds["examples"])
    return obj, rows


def check_invariants(rows):
    pf = collections.defaultdict(set)
    sf = collections.defaultdict(set)
    for r in rows:
        if r["metadata_pair_id"]:
            pf[r["metadata_pair_id"]].add(r["metadata_fold"])
        if r["metadata_source_sentence_id"]:
            sf[r["metadata_source_sentence_id"]].add(r["metadata_fold"])
    span_pair = sum(len(v) > 1 for v in pf.values())
    span_ssid = sum(len(v) > 1 for v in sf.values())

    # DEFINITIVE leakage test: no normalized text may appear in >1 fold.
    # Expand EVERY member text of every row (pair members included) and map
    # norm_key -> set of folds it occurs in. Any key in >1 fold is leakage.
    key_folds = collections.defaultdict(set)
    for r in rows:
        members = [r["input"]]
        if r["metadata_text_off"]:
            members.append(r["metadata_text_off"])
        if r["metadata_text_paired"]:
            members.append(r["metadata_text_paired"])
        for m in members:
            key_folds[norm_key(m)].add(r["metadata_fold"])
    cross_fold_keys = [k for k, fs in key_folds.items() if len(fs) > 1]
    print(f"[INV] pair_id spanning folds = {span_pair}")
    print(f"[INV] ssid spanning folds    = {span_ssid}")
    print(f"[INV] distinct normalized texts = {len(key_folds)} | texts appearing in >1 fold = {len(cross_fold_keys)}")
    if cross_fold_keys:
        ex = cross_fold_keys[0]
        print(f"      example leaking key={ex!r} folds={key_folds[ex]}")
    assert span_pair == 0 and span_ssid == 0 and len(cross_fold_keys) == 0, "INVARIANT VIOLATION"
    print("[INV] ALL PASSED (no text appears in two folds => no grouping/eval leakage)")


def baseline_classification(rows):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import f1_score, roc_auc_score

    cls = [r for r in rows if r["metadata_record_type"] == "classification"]
    tr = [r for r in cls if r["metadata_fold"] == "train"]
    te = [r for r in cls if r["metadata_fold"] == "test"]
    Xtr = [r["input"] for r in tr]; ytr = [r["metadata_toxicity_label"] for r in tr]
    Xte = [r["input"] for r in te]; yte = [r["metadata_toxicity_label"] for r in te]
    vec = TfidfVectorizer(max_features=20000, ngram_range=(1, 2), min_df=2)
    Xtr_v = vec.fit_transform(Xtr); Xte_v = vec.transform(Xte)
    clf = LogisticRegression(max_iter=1000, C=4.0)
    clf.fit(Xtr_v, ytr)
    proba = clf.predict_proba(Xte_v)[:, 1]
    pred = (proba >= 0.5).astype(int)
    print(f"[BASE-A toxicity] train={len(tr)} test={len(te)} | "
          f"AUC={roc_auc_score(yte, proba):.3f} F1={f1_score(yte, pred):.3f}")

    # per-sub-context one-vs-rest among toxic test rows (signal check)
    for a in SUB_ATTRS:
        ytr_a = [r["metadata_subcontext_labels"].get(a) or 0 for r in tr]
        yte_a = [r["metadata_subcontext_labels"].get(a) or 0 for r in te]
        if sum(ytr_a) < 30 or sum(yte_a) < 10:
            print(f"[BASE-A sub:{a:16s}] skipped (too few positives: train={sum(ytr_a)} test={sum(yte_a)})")
            continue
        clf_a = LogisticRegression(max_iter=1000, C=4.0, class_weight="balanced")
        clf_a.fit(Xtr_v, ytr_a)
        pa = clf_a.predict_proba(Xte_v)[:, 1]
        print(f"[BASE-A sub:{a:16s}] pos(tr/te)={sum(ytr_a)}/{sum(yte_a)} | AUC={roc_auc_score(yte_a, pa):.3f}")


def baseline_pairs(rows):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np

    cps = [r for r in rows if r["metadata_record_type"] == "content_pair"][:4000]
    sps = [r for r in rows if r["metadata_record_type"] == "surface_pair"]
    corpus = []
    for r in cps:
        corpus.append(r["input"]); corpus.append(r["metadata_text_off"])
    for r in sps:
        corpus.append(r["input"]); corpus.append(r["metadata_text_paired"])
    vec = TfidfVectorizer(max_features=20000).fit(corpus)

    def pair_sim(items, a_key, b_key):
        sims = []
        for r in items:
            va = vec.transform([r[a_key]]); vb = vec.transform([r[b_key]])
            sims.append(float(cosine_similarity(va, vb)[0, 0]))
        return np.array(sims)

    cp_sim = pair_sim(cps, "input", "metadata_text_off")
    sp_sim = pair_sim(sps, "input", "metadata_text_paired")
    print(f"[BASE-B content_pair] n={len(cps)} | mean TF-IDF cos(toxic,neutral)={cp_sim.mean():.3f} "
          f"(lower => content genuinely flips)")
    print(f"[BASE-B surface_pair] n={len(sps)} | mean TF-IDF cos(x,x')={sp_sim.mean():.3f} "
          f"(moderate => reworded, not copied; surface-gate enforced cos-proxy)")


if __name__ == "__main__":
    obj, rows = load_rows()
    print(f"Loaded {len(rows)} rows from data_out.json; datasets={[d['dataset'] for d in obj['datasets']]}")
    check_invariants(rows)
    baseline_classification(rows)
    baseline_pairs(rows)
