#!/usr/bin/env python3
"""STEP 0 — Ingest & parse the iter-1 surface originals VERBATIM (no mutation).

Reads the two iter-1 full_data_out.json files and emits compact intermediates:
  temp/intermediate/fl_originals.json     : 590 first-letter surface_flip pairs (1180 rows) verbatim + per-stratum counts
  temp/intermediate/fl_wordpools.json     : per-letter ranked word pool (word,count,token_id) from occurrence_tables
  temp/intermediate/tox_originals.json     : 546 toxicity surface_pair rows verbatim + per-origin counts
  temp/intermediate/tox_index.json          : norm_key->fold map, existing ssids, existing surface norm_keys, all norm_keys
"""
from __future__ import annotations

import json
import resource
import sys
from collections import Counter, defaultdict
from pathlib import Path

from loguru import logger

import cc

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")

WORK = Path(__file__).resolve().parent
INTER = WORK / "temp" / "intermediate"
INTER.mkdir(parents=True, exist_ok=True)


def set_mem(gb: float = 20.0):
    b = int(gb * 1024 ** 3)
    try:
        resource.setrlimit(resource.RLIMIT_AS, (b, b))
    except (ValueError, OSError) as e:
        logger.warning(f"rlimit not set: {e!r}")


def extract_first_letter():
    logger.info(f"loading FL full: {cc.FL_FULL}")
    obj = json.loads(cc.FL_FULL.read_text())
    meta = obj["metadata"]
    occ = meta["occurrence_tables"]  # letter(lower) -> [{word,count,token_id}]
    wordpools = {}
    for lt, rows in occ.items():
        wordpools[lt] = [{"word": r["word"], "count": int(r["count"]),
                          "token_id": r.get("token_id")} for r in rows]
        logger.info(f"  occ[{lt}] = {len(rows)} word-types")

    surface_rows = []
    per_letter_pid = defaultdict(set)
    per_letter_carrier = defaultdict(Counter)
    orig_pairsets = defaultdict(set)        # letter -> set of frozenset({wa.lower, wb.lower})
    pid_words = defaultdict(dict)           # (letter,pid) -> {role: word}
    for grp in obj["datasets"]:
        for r in grp["examples"]:
            if r.get("metadata_pair_type") != "surface_flip":
                continue
            surface_rows.append(r)
            lt = r["metadata_letter"].lower()
            pid = r["metadata_pair_id"]
            per_letter_pid[lt].add(pid)
            per_letter_carrier[lt][r["metadata_template_id"]] += 1
            pid_words[(lt, pid)][r["metadata_role"]] = r["metadata_target_word"]

    for (lt, pid), rolemap in pid_words.items():
        ws = [w.lower() for w in rolemap.values()]
        if len(ws) == 2:
            orig_pairsets[lt].add(frozenset(ws))

    counts = {lt: {"pairs": len(p), "rows": per_letter_carrier[lt].total() if hasattr(per_letter_carrier[lt], "total") else sum(per_letter_carrier[lt].values()),
                   "by_carrier_rows": dict(per_letter_carrier[lt])}
              for lt, p in per_letter_pid.items()}
    logger.info(f"FL surface originals: {len(surface_rows)} rows; pairs/letter="
                f"{ {lt: len(p) for lt, p in per_letter_pid.items()} }")

    (INTER / "fl_originals.json").write_text(json.dumps({
        "surface_rows": surface_rows,
        "per_letter_counts": counts,
        "letters": [c.lower() for c in meta["target_letters"]],
    }, ensure_ascii=False))
    (INTER / "fl_wordpools.json").write_text(json.dumps({
        "wordpools": wordpools,
        "orig_pairsets": {lt: [sorted(list(s)) for s in sets] for lt, sets in orig_pairsets.items()},
    }, ensure_ascii=False))
    return len(surface_rows)


def extract_toxicity():
    logger.info(f"loading TOX full: {cc.TOX_FULL}")
    obj = json.loads(cc.TOX_FULL.read_text())
    surface_rows = []
    normkey_fold = {}
    conflicts = 0
    existing_ssids = set()
    existing_surface_normkeys = set()
    all_normkeys = set()
    per_origin = Counter()

    def note(text, fold):
        nonlocal conflicts
        if not text:
            return
        k = cc.norm_key(text)
        all_normkeys.add(k)
        if k in normkey_fold and normkey_fold[k] != fold:
            conflicts += 1
        else:
            normkey_fold[k] = fold

    for grp in obj["datasets"]:
        for r in grp["examples"]:
            fold = r["metadata_fold"]
            for key in ("input", "metadata_text_on", "metadata_text_off", "metadata_text_paired"):
                note(r.get(key), fold)
            if r["metadata_source_sentence_id"]:
                existing_ssids.add(r["metadata_source_sentence_id"])
            if r.get("metadata_record_type") == "surface_pair":
                surface_rows.append(r)
                per_origin[r["metadata_origin_source"]] += 1
                existing_surface_normkeys.add(cc.norm_key(r["input"]))

    logger.info(f"TOX surface originals: {len(surface_rows)} rows; per_origin={dict(per_origin)}; "
                f"normkey_fold={len(normkey_fold)} conflicts={conflicts} ssids={len(existing_ssids)}")

    (INTER / "tox_originals.json").write_text(json.dumps({
        "surface_rows": surface_rows,
        "per_origin": dict(per_origin),
    }, ensure_ascii=False))
    (INTER / "tox_index.json").write_text(json.dumps({
        "normkey_fold": normkey_fold,
        "existing_ssids": sorted(existing_ssids),
        "existing_surface_normkeys": sorted(existing_surface_normkeys),
        "all_normkeys": sorted(all_normkeys),
        "fold_conflicts": conflicts,
    }, ensure_ascii=False))
    return len(surface_rows)


def main():
    set_mem(20.0)
    nfl = extract_first_letter()
    ntox = extract_toxicity()
    logger.info(f"DONE extract: FL surface rows={nfl} | TOX surface rows={ntox}")
    print(f"EXTRACT_OK fl_rows={nfl} tox_rows={ntox}")


if __name__ == "__main__":
    main()
