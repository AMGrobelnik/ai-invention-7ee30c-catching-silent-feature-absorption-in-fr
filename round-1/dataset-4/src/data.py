#!/usr/bin/env python3
"""Canonical entry point for the CCRG supporting-families + boundary-null dataset.

Run:  uv run data.py   (uses pyproject.toml -> .venv)

THREE chosen real, human-annotated datasets (no synthesis, $0 LLM spend):
  1. CAD-IMDB sentiment            (Kaushik et al. ICLR 2020)   -> family 'sentiment'             [supporting]
  2. CEBaB food+service aspect     (Abraham et al. NeurIPS 2022)-> family 'restaurant_aspect'     [supporting]
  3. LabHC/bias_in_bios            (De-Arteaga et al. 2019)     -> family 'bias_in_bios_boundary' [boundary-null]

Pipeline (deterministic):
  1. build_dataset.main()  -> full_data_out.json  (exp_sel_data_out: {metadata, datasets:[{dataset, examples:[...]}]};
                              ONE example per TEXT row; every row validated vs schema.json).
  2. write_summary()       -> data_summary.json   (the metadata block alone, for cheap inspection).
  3. emit_variants()       -> mini_data_out.json + preview_data_out.json via the aii-json format script
                              (3 examples/dataset; preview truncated). Native fallback if the skill is absent.
  4. write_manifest()      -> manifest.json       (machine-readable deliverable + provenance index).
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

from loguru import logger

import build_dataset

WS = Path(__file__).resolve().parent
AII_JSON_DIR = Path("/ai-inventor/.claude/skills/aii-json")
AII_JSON_PY = AII_JSON_DIR / ".." / ".ability_client_venv" / "bin" / "python"
AII_JSON_FMT = AII_JSON_DIR / "scripts" / "aii_json_format_mini_preview.py"
TRUNC = 200

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")


def write_summary():
    full = json.loads((WS / "full_data_out.json").read_text())
    (WS / "data_summary.json").write_text(json.dumps(full["metadata"], ensure_ascii=False, indent=2))
    logger.info("Wrote data_summary.json")


def _truncate(obj):
    if isinstance(obj, str):
        return obj if len(obj) <= TRUNC else obj[:TRUNC] + f"...[+{len(obj) - TRUNC} chars]"
    if isinstance(obj, list):
        return [_truncate(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _truncate(v) for k, v in obj.items()}
    return obj


def _native_variants():
    """Fallback that mirrors the aii-json convention: 3 examples/dataset; preview = truncated mini."""
    full = json.loads((WS / "full_data_out.json").read_text())
    mini = {"metadata": full["metadata"],
            "datasets": [{"dataset": d["dataset"], "examples": d["examples"][:3]} for d in full["datasets"]]}
    preview = _truncate(mini)
    (WS / "mini_data_out.json").write_text(json.dumps(mini, ensure_ascii=False, indent=2))
    (WS / "preview_data_out.json").write_text(json.dumps(preview, ensure_ascii=False, indent=2))
    logger.info("emit_variants: native fallback (aii-json skill unavailable)")


def emit_variants():
    """Primary: aii-json format script on full_data_out.json, then rename to canonical names."""
    if AII_JSON_PY.exists() and AII_JSON_FMT.exists():
        try:
            subprocess.run([str(AII_JSON_PY), str(AII_JSON_FMT), "--input", str(WS / "full_data_out.json")],
                           check=True, capture_output=True, text=True)
            # script writes full_/mini_/preview_full_data_out.json alongside the input
            (WS / "mini_full_data_out.json").replace(WS / "mini_data_out.json")
            (WS / "preview_full_data_out.json").replace(WS / "preview_data_out.json")
            # full_full_data_out.json is byte-identical content to full_data_out.json -> drop the duplicate
            (WS / "full_full_data_out.json").unlink(missing_ok=True)
            logger.info("emit_variants: via aii-json format script (3 examples/dataset; preview truncated)")
            return
        except subprocess.CalledProcessError as e:
            logger.warning(f"aii-json format script failed ({e.stderr[:200] if e.stderr else e}); using native fallback")
    _native_variants()


def write_manifest():
    m = json.loads((WS / "data_summary.json").read_text())
    fs = m["family_summary"]
    man = {
        "artifact": m["artifact"],
        "schema_version": m["schema_version"],
        "emitted_format": m["emitted_format"],
        "total_rows": m["total_rows"],
        "llm_spend_usd": m["llm_spend_usd"],
        "deliverables": {
            "full": "full_data_out.json",
            "mini": "mini_data_out.json",
            "preview": "preview_data_out.json",
            "row_schema": "schema.json",
            "summary": "data_summary.json",
            "pipeline": ["data.py", "build_dataset.py", "qc.py", "explore.py", "verify.py"],
        },
        "validated_against": ["exp_sel_data_out (aii-json)",
                              "schema.json (jsonschema Draft7, every row)"],
        "families": {
            fam: {
                "role": ("boundary-null" if fam == "bias_in_bios_boundary" else "supporting"),
                "n_rows": s["n_rows"],
                "n_pairs": s.get("n_pairs") or s.get("n_pairs_total"),
                "label_balance": (s["label_balance"] if fam != "bias_in_bios_boundary"
                                  else f"{len(s['label_balance'])} professions, ~balanced (capped)"),
                "fold_sizes": s["fold_sizes"],
                "license": s["license"],
                "source_url": s["source_url"],
                "source_paper": s["source_paper"],
            } for fam, s in fs.items()
        },
        "discriminator_field": m["family_discriminator_field"],
        "is_surface_pair": "false for all rows (out of scope here)",
    }
    (WS / "manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=2))
    logger.info(f"Wrote manifest.json ({len(man['families'])} families, {man['total_rows']} rows)")


def main():
    logger.info("STEP 1/4: build_dataset (standardize 3 families -> full_data_out.json)")
    build_dataset.main()
    logger.info("STEP 2/4: write_summary")
    write_summary()
    logger.info("STEP 3/4: emit_variants (mini / preview)")
    emit_variants()
    logger.info("STEP 4/4: write_manifest")
    write_manifest()
    logger.info("DONE: full/mini/preview_data_out.json + schema.json + data_summary.json + manifest.json")


if __name__ == "__main__":
    main()
