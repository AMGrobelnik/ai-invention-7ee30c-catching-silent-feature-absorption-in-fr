#!/usr/bin/env python3
"""Canonical end-to-end builder for the iter-2 surface-invariance SUPERSET.

Orchestrates the six stages in order. All LLM calls (Steps 2-3) are JSONL-cached, so a re-run
of a completed build costs $0 and is deterministic. Run with `uv run data.py` (deps in
pyproject.toml). Requires OPENROUTER_API_KEY for the toxicity generation/judge stages.

Stages (each is an importable module with a main()/run()):
  0  extract_originals.py  — ingest the 590 first-letter + 546 toxicity surface originals VERBATIM
  1  build_first_letter.py — enlarge first-letter 590 -> 1,700 pairs (deterministic, $0)
  2  gen_toxicity.py       — enlarge toxicity 546 -> 1,631 pairs (gpt-4o-mini gen + double-gate +
                              claude-haiku-4.5 INDEPENDENT accept judge)
  3  rejudge.py            — confirmation rate + cross-judge (claude vs gemini / claude vs deepseek)
  4-5 assemble.py          — assemble exp_sel_data_out superset + data_summary.json (null sizes)
  6  make_variants.py      — mini/preview variants

The two source families ("datasets") are:
  * first-letter words from the unsloth/gemma-2-2b tokenizer vocab + Pile occurrence frequencies
  * toxicity from s-nlp/paradetox (openrail++) and google/civil_comments (CC0)
"""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

WORK = Path(__file__).resolve().parent


def _run(module: str, argv=None):
    print(f"\n=== running {module} ===", flush=True)
    saved = sys.argv
    sys.argv = [module] + (argv or [])
    try:
        runpy.run_path(str(WORK / module), run_name="__main__")
    finally:
        sys.argv = saved


def main():
    _run("extract_originals.py")
    _run("build_first_letter.py")
    _run("gen_toxicity.py", ["--max-paradetox", "1100", "--max-civil", "1700",
                             "--target-accepted", "1050", "--batch", "100", "--ceiling", "6.0"])
    _run("rejudge.py", ["--tox-sample", "400", "--fl-sample", "400"])
    _run("assemble.py")
    _run("make_variants.py")
    print("\nDONE: full_data_out.json + mini/preview + data_summary.json")


if __name__ == "__main__":
    main()
