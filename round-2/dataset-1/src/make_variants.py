#!/usr/bin/env python3
"""Emit mini_data_out.json (3 examples/group) and preview_data_out.json (mini + strings<=200 chars).

The exp_sel_data_out object is {metadata, datasets:[{dataset, examples[]}]}, not a top-level array,
so the generic aii-json format script (which truncates a top-level list) does not apply; this mirrors
the iter-1 make_variants convention exactly.
"""
from __future__ import annotations

import json
from pathlib import Path

WORK = Path(__file__).resolve().parent
FULL = WORK / "full_data_out.json"


def truncate(obj, n=200):
    if isinstance(obj, str):
        return obj if len(obj) <= n else obj[:n]
    if isinstance(obj, list):
        return [truncate(x, n) for x in obj]
    if isinstance(obj, dict):
        return {k: truncate(v, n) for k, v in obj.items()}
    return obj


def main():
    full = json.loads(FULL.read_text())
    mini = {"metadata": full["metadata"],
            "datasets": [{"dataset": d["dataset"], "examples": d["examples"][:3]} for d in full["datasets"]]}
    (WORK / "mini_data_out.json").write_text(json.dumps(mini, ensure_ascii=False))
    preview = {"metadata": truncate(full["metadata"]),
               "datasets": [{"dataset": d["dataset"], "examples": truncate(d["examples"][:10])}
                            for d in full["datasets"]]}
    (WORK / "preview_data_out.json").write_text(json.dumps(preview, ensure_ascii=False, indent=1))
    n_full = sum(len(d["examples"]) for d in full["datasets"])
    print(f"VARIANTS_OK full_examples={n_full} groups={len(full['datasets'])} "
          f"mini_examples={sum(len(d['examples']) for d in mini['datasets'])}")


if __name__ == "__main__":
    main()
