#!/usr/bin/env python3
"""Verify (a) the canonical bias_in_bios profession int->string mapping empirically via
keyword alignment, and (b) CEBaB per-split original-row availability + flip feasibility."""
import os, re
from pathlib import Path
from collections import Counter, defaultdict

WS = Path(__file__).resolve().parent
os.environ.setdefault("HF_HOME", str(WS / "temp" / "hf_cache"))
from datasets import load_dataset  # noqa: E402

# Canonical De-Arteaga et al. (2019) biosbias 28 occupations, alphabetical, INCLUDING 'dj'.
PROF = ["accountant","architect","attorney","chiropractor","comedian","composer","dentist",
        "dietitian","dj","filmmaker","interior_designer","journalist","model","nurse","painter",
        "paralegal","pastor","personal_trainer","photographer","physician","poet","professor",
        "psychologist","rapper","software_engineer","surgeon","teacher","yoga_teacher"]
assert len(PROF) == 28

# Strong keyword signatures for a subset of professions to cross-check the mapping empirically.
KW = {
    "nurse": [r"\bnurs"], "attorney": [r"\battorney|\blaw\b|law school|law degree"],
    "surgeon": [r"\bsurg"], "dentist": [r"\bdent"], "yoga_teacher": [r"\byoga\b"],
    "software_engineer": [r"\bsoftware\b|\bprogramm|developer\b"], "physician": [r"\bphysician|\bmedicine\b|\bM\.?D\.?\b"],
    "photographer": [r"\bphotograph"], "psychologist": [r"\bpsycholog"], "dietitian": [r"\bdietit|\bnutrit"],
    "chiropractor": [r"\bchiropract"], "pastor": [r"\bpastor|\bchurch\b|\bministr"], "rapper": [r"\brapper|\bhip.?hop|\brap\b"],
    "comedian": [r"\bcomedian|\bcomedy\b|\bstand.?up"], "poet": [r"\bpoet|\bpoem|\bpoetry"],
    "architect": [r"\barchitect"], "accountant": [r"\baccountant|\baccounting\b|\bCPA\b"],
}

bib = load_dataset("LabHC/bias_in_bios")
tr = bib["train"]
# Sample up to 4000 rows per profession to compute keyword hit-rate
by_prof = defaultdict(list)
texts = tr["hard_text"]; profs = tr["profession"]
for i in range(0, len(profs), 7):  # stride-sample for speed
    by_prof[profs[i]].append(texts[i])

print("Empirical mapping check (profession_int -> proposed_name : top keyword hit-rate):")
ok = 0; total = 0
for pid in range(28):
    name = PROF[pid]
    if name not in KW:
        continue
    total += 1
    sample = by_prof[pid][:1500]
    pats = [re.compile(p, re.I) for p in KW[name]]
    hits = sum(1 for t in sample if any(p.search(t) for p in pats))
    rate = hits / max(1, len(sample))
    flag = "OK" if rate > 0.12 else "??"
    if rate > 0.12:
        ok += 1
    print(f"  {pid:2d} -> {name:18s} hitrate={rate:.2f} (n={len(sample)}) {flag}")
print(f"PASS {ok}/{total} professions confirmed by keyword signature.")

print("\n" + "=" * 60)
print("CEBaB per-split original availability + food/service flip feasibility")
print("=" * 60)
ceb = load_dataset("CEBaB/CEBaB")
for split in ["train_inclusive", "validation", "test"]:
    df = ceb[split].to_pandas()
    n_orig = int((df["is_original"] == True).sum())
    orig_ids = set(df.loc[df["is_original"] == True, "original_id"])
    # how many edit rows have their original present in the same split
    edits = df[df["is_original"] == False]
    present = edits["original_id"].isin(orig_ids).mean()
    # count potential food/service flips
    cnt = {"food": 0, "service": 0}
    omap = {r.original_id: r for r in df[df["is_original"] == True].itertuples()}
    for e in edits.itertuples():
        A = e.edit_type
        if A not in ("food", "service"):
            continue
        o = omap.get(e.original_id)
        if o is None:
            continue
        ev = getattr(e, f"{A}_aspect_majority"); ov = getattr(o, f"{A}_aspect_majority")
        if ev in ("Positive", "Negative") and ov in ("Positive", "Negative") and ev != ov:
            cnt[A] += 1
    print(f"{split}: n_orig={n_orig}, edits={len(edits)}, orig-present-rate={present:.3f}, "
          f"clean_flips food={cnt['food']} service={cnt['service']}")
