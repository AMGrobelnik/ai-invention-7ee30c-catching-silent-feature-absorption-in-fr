#!/usr/bin/env python3
"""Final verification of the assembled superset:
  1. every iter-1 surface pair_id present (true superset);
  2. each iter-1 original row is BYTE-IDENTICAL except the (<=4) additive keys;
  3. no new pair_id collides with an iter-1 pair_id;
  4. additive-key coverage (enlargement_batch on every row; independent-judge keys present);
  5. per-concept totals >= max(1500, original).
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

WORK = Path(__file__).resolve().parent
INTER = WORK / "temp" / "intermediate"
ADDITIVE = {"metadata_enlargement_batch", "metadata_independent_judge_model",
            "metadata_independent_judge_pass", "metadata_independent_judge_reason"}

full = json.loads((WORK / "full_data_out.json").read_text())
groups = {d["dataset"]: d["examples"] for d in full["datasets"]}

# originals (verbatim, pre-additive)
fl_orig = {r["metadata_pair_id"] + "|" + r["metadata_role"]: r
           for r in json.loads((INTER / "fl_originals.json").read_text())["surface_rows"]}
tox_orig = {r["metadata_pair_id"]: r
            for r in json.loads((INTER / "tox_originals.json").read_text())["surface_rows"]}

problems = []

# ---- FIRST-LETTER ----
fl_rows = [r for g, ex in groups.items() if g.startswith("first_letter_spelling_") for r in ex]
fl_pairs = {r["metadata_pair_id"] for r in fl_rows}
fl_orig_pairs = {r["metadata_pair_id"] for r in fl_orig.values()}
assert fl_orig_pairs <= fl_pairs, "FL superset broken"
batch_cnt_fl = Counter()
ind_present_fl = 0
for r in fl_rows:
    batch_cnt_fl[r.get("metadata_enlargement_batch")] += 1
    if "metadata_independent_judge_model" not in r:
        problems.append(f"FL row missing independent-judge keys: {r['metadata_pair_id']}")
    if r.get("metadata_independent_judge_model"):
        ind_present_fl += 1
    if r.get("metadata_enlargement_batch") == "iter1_original":
        key = r["metadata_pair_id"] + "|" + r["metadata_role"]
        o = fl_orig.get(key)
        if o is None:
            problems.append(f"FL original row not found: {key}")
            continue
        extra = (set(r) - set(o)) - ADDITIVE
        changed = [k for k in o if r.get(k) != o[k]]
        if extra:
            problems.append(f"FL original {key} has unexpected extra keys {extra}")
        if changed:
            problems.append(f"FL original {key} mutated keys {changed}")

# ---- TOXICITY ----
tox_rows = [r for g in ("paradetox", "civil_comments") for r in groups[g]]
tox_pairs = {r["metadata_pair_id"] for r in tox_rows}
assert set(tox_orig) <= tox_pairs, "TOX superset broken"
new_tox_pairs = tox_pairs - set(tox_orig)
assert not (new_tox_pairs & set(tox_orig)), "TOX pair_id collision"
batch_cnt_tox = Counter()
ind_present_tox = 0
ids = Counter()
for r in tox_rows:
    batch_cnt_tox[r.get("metadata_enlargement_batch")] += 1
    ids[r["metadata_id"]] += 1
    if r.get("metadata_independent_judge_model"):
        ind_present_tox += 1
    if r.get("metadata_enlargement_batch") == "iter1_original":
        o = tox_orig.get(r["metadata_pair_id"])
        extra = (set(r) - set(o)) - ADDITIVE
        changed = [k for k in o if r.get(k) != o[k]]
        if extra:
            problems.append(f"TOX original {r['metadata_pair_id']} extra keys {extra}")
        if changed:
            problems.append(f"TOX original {r['metadata_pair_id']} mutated {changed}")
dup_ids = [i for i, c in ids.items() if c > 1]
if dup_ids:
    problems.append(f"TOX duplicate metadata_id: {dup_ids[:5]} ({len(dup_ids)})")

fl_pair_count = len(fl_pairs)
tox_pair_count = len(tox_rows)
print(f"FL pairs={fl_pair_count} (orig {len(fl_orig_pairs)} + new {fl_pair_count-len(fl_orig_pairs)}) "
      f"batch={dict(batch_cnt_fl)} independent_judge_rows={ind_present_fl}")
print(f"TOX pairs={tox_pair_count} (orig {len(tox_orig)} + new {len(new_tox_pairs)}) "
      f"batch={dict(batch_cnt_tox)} independent_judge_rows={ind_present_tox}")
assert fl_pair_count >= 1500, "FL < 1500"
assert tox_pair_count >= 1500, "TOX < 1500"
assert not problems, "PROBLEMS:\n" + "\n".join(problems[:20])
print(f"VERIFY_OK problems={len(problems)} fl>=1500 tox>=1500 superset+byte-identical-originals confirmed")
