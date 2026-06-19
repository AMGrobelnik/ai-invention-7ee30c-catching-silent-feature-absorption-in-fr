#!/usr/bin/env python
"""Optional, $0, best-effort Neuronpedia auto-interp enrichment as a POST-pass on the finished catalog
(so the 47-min pipeline does not need re-running). Adds human-auditable labels for the parent + absorber
latents of every absorption-structured catalog row; rewrites catalog.csv / catalog.json / method_out.json
+ variants. NON-blocking: on any network failure it leaves labels None and records available=False."""
import json, copy
from pathlib import Path

import core
import method as M

WORK = M.WORK
OUT = WORK / "method_out.json"


def main():
    b = json.loads(OUT.read_text())
    cat = next(d for d in b["datasets"] if d["dataset"] == "absorber_catalog")
    exs = cat["examples"]

    # reconstruct flat rows from the catalog examples (metadata_<col> -> col)
    rows = []
    for e in exs:
        rows.append({c: e.get(f"metadata_{c}") for c in M.CSV_COLS})

    np_meta = M.enrich_neuronpedia(rows, timeout=8.0, max_calls=1500)  # mutates rows[*]["neuronpedia_*_label"]
    np_meta["attempted"] = True
    print("neuronpedia:", np_meta)

    # write labels back onto the examples (1:1 order)
    for e, r in zip(exs, rows):
        e["metadata_neuronpedia_parent_label"] = r.get("neuronpedia_parent_label")
        e["metadata_neuronpedia_absorber_label"] = r.get("neuronpedia_absorber_label")

    b["metadata"]["catalog_summary"]["neuronpedia_enrichment"] = np_meta

    # rewrite shipped catalog files from the enriched rows
    M.write_catalog_csv(rows, WORK / "catalog.csv")
    M.write_catalog_json(rows, WORK / "catalog.json")

    # rewrite method_out.json (+ results copy) and variants
    core.save_json(b, OUT)
    core.save_json(b, M.RESULTS / "method_out.json")
    import subprocess, sys
    subprocess.run([sys.executable, str(WORK / "make_variants.py"), str(OUT)], check=True)
    print("rewrote method_out.json + catalog.csv/json + variants")


if __name__ == "__main__":
    main()
