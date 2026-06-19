#!/usr/bin/env python3
"""Generate schema-valid mini/preview variants of full_data_out.json.

The dataset is a top-level OBJECT ({"metadata":..., "datasets":[...]}), so the generic array-based
format script does not apply. mini keeps the structure with 3 representative examples per dataset and
trimmed dataset-level tables; preview truncates all strings to 200 chars. Both stay schema-valid
against exp_sel_data_out.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

WORKDIR = Path(__file__).resolve().parent
TRUNC = 200


def truncate_strings(obj):
    if isinstance(obj, str):
        return obj[:TRUNC]
    if isinstance(obj, list):
        return [truncate_strings(x) for x in obj]
    if isinstance(obj, dict):
        return {k: truncate_strings(v) for k, v in obj.items()}
    return obj


def representative(examples):
    """Pick up to 3 examples spanning pair types (content_flip, surface_flip, corpus_context)."""
    picks, seen = [], set()
    for r in examples:
        pt = r.get("metadata_pair_type")
        if pt not in seen:
            picks.append(r)
            seen.add(pt)
        if len(picks) >= 3:
            break
    if len(picks) < 3:
        picks = examples[:3]
    return picks


def trim_metadata(meta):
    m = copy.deepcopy(meta)
    # shrink the big dataset-level tables so mini/preview stay tiny
    if "occurrence_tables" in m:
        m["occurrence_tables"] = {k: v[:5] for k, v in m["occurrence_tables"].items()}
    if "on_words_by_letter" in m:
        m["on_words_by_letter"] = {k: v[:8] for k, v in m["on_words_by_letter"].items()}
    return m


def main():
    src = WORKDIR / (sys.argv[1] if len(sys.argv) > 1 else "full_data_out.json")
    data = json.loads(src.read_text())

    mini = {"metadata": trim_metadata(data.get("metadata", {})),
            "datasets": [{"dataset": d["dataset"], "examples": representative(d["examples"])}
                         for d in data["datasets"]]}
    (WORKDIR / "mini_data_out.json").write_text(json.dumps(mini, ensure_ascii=False, indent=2))

    preview = truncate_strings(copy.deepcopy(mini))
    (WORKDIR / "preview_data_out.json").write_text(json.dumps(preview, ensure_ascii=False, indent=2))

    n = sum(len(d["examples"]) for d in data["datasets"])
    print(f"mini_data_out.json + preview_data_out.json written "
          f"(full has {n} examples across {len(data['datasets'])} dataset(s))")


if __name__ == "__main__":
    main()
