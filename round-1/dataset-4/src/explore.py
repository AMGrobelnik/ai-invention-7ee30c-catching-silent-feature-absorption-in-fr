#!/usr/bin/env python3
"""Inspect CEBaB and bias_in_bios structure before building the standardization pipeline."""
import os
from pathlib import Path
from collections import Counter

WS = Path(__file__).resolve().parent
os.environ.setdefault("HF_HOME", str(WS / "temp" / "hf_cache"))

from datasets import load_dataset, get_dataset_config_names  # noqa: E402

print("=" * 70)
print("CEBaB/CEBaB")
print("=" * 70)
ceb = load_dataset("CEBaB/CEBaB")
print("Splits + sizes:")
for k, v in ceb.items():
    print(f"  {k}: {len(v)} rows")
print("Features:")
for name, feat in ceb["train_inclusive"].features.items():
    print(f"  {name}: {feat}")

ti = ceb["train_inclusive"]
print("\n-- train_inclusive value distributions --")
print("is_original:", Counter(ti["is_original"]))
print("edit_goal:", Counter(ti["edit_goal"]))
print("edit_type:", Counter(ti["edit_type"]))
print("review_majority:", Counter(ti["review_majority"]))
print("food_aspect_majority:", Counter(ti["food_aspect_majority"]))
print("service_aspect_majority:", Counter(ti["service_aspect_majority"]))
print("ambiance_aspect_majority:", Counter(ti["ambiance_aspect_majority"]))
print("noise_aspect_majority:", Counter(ti["noise_aspect_majority"]))

# Show one original + its edits to understand pairing structure
import pandas as pd  # noqa: E402
df = ti.to_pandas()
print("\n-- example: original_id == one group --")
oid = df.loc[df["is_original"] == True, "original_id"].iloc[0]
grp = df[df["original_id"] == oid][
    ["id", "original_id", "edit_id", "is_original", "edit_goal", "edit_type",
     "food_aspect_majority", "service_aspect_majority", "review_majority"]
]
print(grp.to_string(index=False))
print("\nid dtype:", df["id"].dtype, "| original_id dtype:", df["original_id"].dtype,
      "| edit_id dtype:", df["edit_id"].dtype)
print("sample description len chars:", df["description"].str.len().describe().to_dict())

print("\n" + "=" * 70)
print("LabHC/bias_in_bios")
print("=" * 70)
bib = load_dataset("LabHC/bias_in_bios")
print("Splits + sizes:")
for k, v in bib.items():
    print(f"  {k}: {len(v)} rows")
print("Features:")
for name, feat in bib["train"].features.items():
    print(f"  {name}: {feat}")
# profession label names (canonical mapping ships in features?)
prof_feat = bib["train"].features["profession"]
print("\nprofession feature type:", type(prof_feat).__name__)
if hasattr(prof_feat, "names"):
    print("profession names:", prof_feat.names)
else:
    print("profession has NO ClassLabel names -> need external mapping")
gen_feat = bib["train"].features["gender"]
print("gender feature type:", type(gen_feat).__name__)
if hasattr(gen_feat, "names"):
    print("gender names:", gen_feat.names)
print("profession value range:", min(bib["train"]["profession"]), "-", max(bib["train"]["profession"]))
print("distinct professions:", len(set(bib["train"]["profession"])))
print("gender values:", Counter(bib["train"]["gender"]))
