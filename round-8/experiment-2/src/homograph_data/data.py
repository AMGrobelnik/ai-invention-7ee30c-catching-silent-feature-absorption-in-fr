#!/usr/bin/env python3
"""Canonical entrypoint for the Non-Spelling Absorption Testbed dataset.

Builds a TEXT-ONLY dataset for the downstream SAE feature-absorption experiment and emits it in
the AII `exp_sel_data_out` schema, GROUPED BY DATASET (exactly two datasets):

  {"metadata": {...}, "datasets": [
      {"dataset": "numeric_absorption",   "examples": [ {input, output, metadata_*}, ... ]},
      {"dataset": "taxonomic_absorption", "examples": [ {input, output, metadata_*}, ... ]}
  ]}

Each example is ONE data row (one content/surface-pair sentence, or one pile context window) — NOT
one example per dataset or per fold. Per-row metadata is flattened into metadata_<name> keys (the
exp_sel schema forbids nested objects inside an example).

Construction logic lives in build_dataset.py (constants/builders) and pipeline.py (orchestration:
templated content/surface pairs + pile-uncopyrighted corpus streaming + LLM augment/judge +
gemma-2-2b token indices + frozen folds + sanity asserts). This script:
  1. runs that build  -> writes full_data_out.json + manifest.json (schema.json is static),
  2. runs the aii-json format script on full_data_out.json -> full_/mini_/preview_full_data_out.json,
     then renames them to full_data_out.json / mini_data_out.json / preview_data_out.json,
  3. validates full_data_out.json against the exp_sel_data_out schema.

Run:  python3 data.py [--scale full|smoke] [--no-llm] [--no-rebuild]
('uv run' is unavailable here because the ambient uv workspace pyproject references a non-member
 'aii-server'; use python3. Pinned dependencies are listed in pyproject.toml / installed system-wide.)
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from loguru import logger

HERE = Path(__file__).resolve().parent
AII_JSON = Path("/ai-inventor/.claude/skills/aii-json")
AII_JSON_PY = AII_JSON / ".." / ".ability_client_venv" / "bin" / "python"
FMT = AII_JSON / "scripts" / "aii_json_format_mini_preview.py"
VAL = AII_JSON / "scripts" / "aii_json_validate_schema.py"
SCHEMA_FORMAT = "exp_sel_data_out"
FULL = HERE / "full_data_out.json"


def build(scale: str, no_llm: bool):
    """Run the construction pipeline (writes full_data_out.json + manifest.json)."""
    import pipeline
    argv = ["pipeline.py", "--scale", scale] + (["--no-llm"] if no_llm else [])
    old = sys.argv
    sys.argv = argv
    try:
        pipeline.main()
    finally:
        sys.argv = old


def emit_variants():
    """full_data_out.json -> aii-json format -> rename to full_/mini_/preview_data_out.json."""
    cmd = [str(AII_JSON_PY), str(FMT), "--input", str(FULL), "--format", SCHEMA_FORMAT,
           "--output-dir", str(HERE)]
    logger.info("emitting variants: " + " ".join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True)
    logger.info((res.stdout or "").strip()[-600:])
    if res.returncode != 0:
        logger.warning(f"format script rc={res.returncode}: {res.stderr[-400:]}")
    # the script writes full_full_/mini_full_/preview_full_data_out.json -> canonical names
    renames = {
        HERE / "full_full_data_out.json": HERE / "full_data_out.json",
        HERE / "mini_full_data_out.json": HERE / "mini_data_out.json",
        HERE / "preview_full_data_out.json": HERE / "preview_data_out.json",
    }
    for src, dst in renames.items():
        if src.exists():
            src.replace(dst)
            logger.info(f"renamed {src.name} -> {dst.name}")
    # robust fallback if the skill failed: build mini/preview manually (datasets-grouped)
    if not (HERE / "mini_data_out.json").exists() or not (HERE / "preview_data_out.json").exists():
        logger.warning("format script outputs missing; generating mini/preview manually")
        data = json.loads(FULL.read_text())

        def trunc(o, n=200):
            if isinstance(o, str):
                return o[:n]
            if isinstance(o, list):
                return [trunc(x, n) for x in o]
            if isinstance(o, dict):
                return {k: trunc(v, n) for k, v in o.items()}
            return o
        mini = {"metadata": data.get("metadata", {}),
                "datasets": [{"dataset": d["dataset"], "examples": d["examples"][:3]} for d in data["datasets"]]}
        (HERE / "mini_data_out.json").write_text(json.dumps(mini, ensure_ascii=False, indent=2))
        (HERE / "preview_data_out.json").write_text(json.dumps(trunc(mini), ensure_ascii=False, indent=2))


def validate():
    cmd = [str(AII_JSON_PY), str(VAL), "--format", SCHEMA_FORMAT, "--file", str(FULL)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    out = (res.stdout + res.stderr).strip()
    passed = "PASSED" in out
    logger.info(f"schema validation of {FULL.name}: {'PASSED' if passed else 'FAILED'}")
    if not passed:
        logger.error(out[-600:])
    return passed


@logger.catch(reraise=True)
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scale", choices=["smoke", "full"], default="full")
    ap.add_argument("--no-llm", action="store_true")
    ap.add_argument("--no-rebuild", action="store_true",
                    help="skip the (expensive) pile-streaming build if full_data_out.json already exists")
    args = ap.parse_args()

    if args.no_rebuild and FULL.exists():
        logger.info(f"--no-rebuild: reusing existing {FULL.name}")
    else:
        build(args.scale, args.no_llm)
    if not FULL.exists():
        raise FileNotFoundError(f"{FULL} was not produced by the build step")

    emit_variants()
    ok = validate()

    data = json.loads(FULL.read_text())
    per = {d["dataset"]: len(d["examples"]) for d in data["datasets"]}
    n = sum(per.values())
    logger.info(f"DELIVERABLE full_data_out.json: {n} examples across {len(data['datasets'])} datasets: {per}")
    logger.info(f"schema_valid={ok}  files: full/mini/preview_data_out.json, schema.json, manifest.json")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
