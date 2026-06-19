#!/usr/bin/env python
"""Generate full/mini/preview variants of method_out.json (object schema: {metadata, datasets}).

full    = identical to the input.
mini    = same metadata, but each dataset's `examples` truncated to the first 3.
preview = mini, with every string recursively truncated to 200 chars.

Self-contained (no ability server). Keeps the exp_gen_sol_out object shape so all three validate.
"""
import json, sys, copy
from pathlib import Path

PREVIEW_STR = 200
MINI_EXAMPLES = 3


def _truncate_strings(obj, n=PREVIEW_STR):
    if isinstance(obj, str):
        return obj if len(obj) <= n else obj[:n]
    if isinstance(obj, list):
        return [_truncate_strings(x, n) for x in obj]
    if isinstance(obj, dict):
        return {k: _truncate_strings(v, n) for k, v in obj.items()}
    return obj


def main():
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "method_out.json")
    blob = json.loads(src.read_text())
    base = src.parent
    stem = src.stem  # method_out

    # full = identical
    (base / f"full_{stem}.json").write_text(json.dumps(blob, indent=1))

    # mini = first MINI_EXAMPLES per dataset, metadata kept
    mini = copy.deepcopy(blob)
    for ds in mini.get("datasets", []):
        ds["examples"] = ds["examples"][:MINI_EXAMPLES]
    (base / f"mini_{stem}.json").write_text(json.dumps(mini, indent=1))

    # preview = mini + strings truncated
    preview = _truncate_strings(copy.deepcopy(mini), PREVIEW_STR)
    (base / f"preview_{stem}.json").write_text(json.dumps(preview, indent=1))

    for tag in ("full", "mini", "preview"):
        p = base / f"{tag}_{stem}.json"
        nex = sum(len(d["examples"]) for d in json.loads(p.read_text()).get("datasets", []))
        print(f"{tag}: {p.name}  {p.stat().st_size/1024:.1f} KB  examples={nex}")


if __name__ == "__main__":
    main()
