#!/usr/bin/env python
"""Post-process method_out.json WITHOUT re-running the GPU pipeline: apply enrich_summary (homograph-
confinement scoping + per-candidate magnitude/leverage caveats) and re-build the safety_screen dataset
from metadata.screens (adds metadata_is_homograph). Everything is read back from the existing metadata —
no fabrication. Re-saves method_out.json so it matches a fresh `uv run method.py`.

Future `uv run method.py` runs already call enrich_summary + the homograph flag inline; this script only
exists so the ALREADY-COMPUTED run gets the same enrichment without paying for another GPU+judge pass."""
import json
from pathlib import Path
from method import enrich_summary, assemble_outputs, save_sanitized

OUT = Path(__file__).parent / "method_out.json"


def main():
    out = json.loads(OUT.read_text())
    md = out["metadata"]
    screens = md.get("screens", [])
    existing_down = next((d for d in out["datasets"] if d["dataset"] == "downstream_subcontext"), None)
    enrich_summary(out)
    assemble_outputs(out, screens, [])                 # rebuild safety_screen (+ placeholder downstream)
    if existing_down is not None:                      # restore the REAL downstream dataset verbatim
        out["datasets"] = [d for d in out["datasets"] if d["dataset"] != "downstream_subcontext"]
        out["datasets"].append(existing_down)
    save_sanitized(out, str(OUT))
    print("scoping_summary:\n", json.dumps(md["scoping_summary"], indent=1)[:1400])
    print("\nhonest_negatives:")
    for n in md["honest_negatives"]:
        print("  -", n[:220])
    print("\ndatasets:", [(d["dataset"], len(d["examples"])) for d in out["datasets"]])


if __name__ == "__main__":
    main()
