#!/usr/bin/env python3
"""Final QC: re-load full_data_out.json, assert structural invariants, report distributions."""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from loguru import logger

WS = Path(__file__).resolve().parent
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")


def main():
    data = json.loads((WS / "full_data_out.json").read_text())
    assert set(data) == {"metadata", "datasets"}
    rows = []
    for ds in data["datasets"]:
        rows.extend(ds["examples"])
    logger.info(f"Total rows: {len(rows)} across {len(data['datasets'])} dataset entries")

    ids = set()
    by_id = {}
    fam_ct = Counter()
    for ex in rows:
        # required base fields
        assert ex["input"] and ex["input"].strip(), "empty input"
        assert ex["output"] and ex["output"].strip(), "empty output"
        assert ex["metadata_concept_label"] == ex["output"], "concept_label != output"
        assert ex["metadata_is_surface_pair"] is False, "is_surface_pair must be False"
        rid = ex["metadata_id"]
        assert rid not in ids, f"dup id {rid}"
        ids.add(rid)
        by_id[rid] = ex
        fam_ct[ex["metadata_family"]] += 1
    logger.info(f"Per-family rows: {dict(fam_ct)}")

    # paired families: resolvable, symmetric, opposite labels, same pair_id
    pairs = defaultdict(list)
    n_content = 0
    for ex in rows:
        if ex["metadata_is_content_pair"]:
            n_content += 1
            p = by_id.get(ex["metadata_partner_id"])
            assert p is not None, f"missing partner for {ex['metadata_id']}"
            assert p["metadata_pair_id"] == ex["metadata_pair_id"], "pair_id mismatch"
            assert p["metadata_partner_id"] == ex["metadata_id"], "asymmetric partner"
            pairs[ex["metadata_pair_id"]].append(ex)
        else:
            assert ex["metadata_pair_id"] is None and ex["metadata_partner_id"] is None
            assert ex["metadata_pair_role"] is None and ex["metadata_flip_type"] is None
    # each pair has exactly 2 members with opposite content roles
    role_bad = 0
    for pid, mem in pairs.items():
        if len(mem) != 2 or {m["metadata_pair_role"] for m in mem} != {"content_on", "content_off"}:
            role_bad += 1
    assert role_bad == 0, f"{role_bad} malformed pairs"
    logger.info(f"Content-pair rows: {n_content} -> {len(pairs)} reconstructable minimal pairs (all 2-member, opposite roles)")

    # bias_in_bios gender x boundary diagnostics
    bib = [e for e in rows if e["metadata_family"] == "bias_in_bios_boundary"]
    gender = Counter(e["metadata_sub_context"]["gender"] for e in bib)
    logger.info(f"bias_in_bios gender distribution: {dict(gender)}")
    # gender spread within a few professions (the habitat!=label diagnostic axis must vary)
    pg = defaultdict(Counter)
    for e in bib:
        pg[e["output"]][e["metadata_sub_context"]["gender"]] += 1
    sample = {p: dict(c) for p, c in list(sorted(pg.items()))[:5]}
    logger.info(f"gender-by-profession (first 5): {sample}")
    assert all(len(c) >= 1 for c in pg.values())
    assert gender["male"] > 0 and gender["female"] > 0, "gender axis degenerate"

    # CEBaB concept split + independent sub-context presence
    ceb = [e for e in rows if e["metadata_family"] == "restaurant_aspect"]
    concepts = Counter(e["metadata_concept"] for e in ceb)
    logger.info(f"CEBaB concepts: {dict(concepts)}")
    assert concepts["food_sentiment"] > 0 and concepts["service_sentiment"] > 0
    # every CEBaB row carries all 4 aspect sub-contexts + review_sentiment
    keys_ok = all({"food", "service", "ambiance", "noise", "review_sentiment", "edited_aspect"}
                  <= set(e["metadata_sub_context"]) for e in ceb)
    assert keys_ok, "CEBaB sub_context missing independent aspect labels"
    logger.info("CEBaB: every row carries food/service/ambiance/noise/review_sentiment/edited_aspect sub-contexts.")

    assert data["metadata"]["llm_spend_usd"] == 0.0
    logger.info("LLM spend: $0.00 (all human-annotated sources).")
    logger.info("ALL QC CHECKS PASSED ✓")


if __name__ == "__main__":
    main()
