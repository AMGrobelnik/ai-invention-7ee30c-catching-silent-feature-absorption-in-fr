#!/usr/bin/env python
"""Produce full/mini/preview variants of method_out.json ({metadata, datasets:[{dataset, examples}]}).
The aii-json format script assumes a top-level array; our output is an object, so we do it here.
  full    = identical copy
  mini    = first 3 examples per dataset (metadata kept verbatim)
  preview = mini + every string recursively truncated to 200 chars
"""
import json, sys, copy
from pathlib import Path

SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else \
    Path("/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_7/gen_art/gen_art_experiment_2/method_out.json")


def truncate(o, n=200):
    if isinstance(o, str):
        return o[:n]
    if isinstance(o, list):
        return [truncate(x, n) for x in o]
    if isinstance(o, dict):
        return {k: truncate(v, n) for k, v in o.items()}
    return o


def main():
    blob = json.loads(SRC.read_text())
    base = SRC.parent
    # full = identical
    (base / f"full_{SRC.name}").write_text(json.dumps(blob, indent=1))
    # mini = first 3 examples per dataset
    mini = {"metadata": blob.get("metadata", {}), "datasets": []}
    for d in blob["datasets"]:
        mini["datasets"].append({"dataset": d["dataset"], "examples": d["examples"][:3]})
    (base / f"mini_{SRC.name}").write_text(json.dumps(mini, indent=1))
    # preview = mini + truncated strings
    prev = {"metadata": truncate(blob.get("metadata", {})),
            "datasets": [{"dataset": d["dataset"], "examples": truncate(d["examples"][:3])}
                         for d in blob["datasets"]]}
    (base / f"preview_{SRC.name}").write_text(json.dumps(prev, indent=1))
    for pre in ("full_", "mini_", "preview_"):
        p = base / f"{pre}{SRC.name}"
        print(f"{p.name}: {p.stat().st_size/1024:.1f} KB")


if __name__ == "__main__":
    main()
