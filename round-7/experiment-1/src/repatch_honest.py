#!/usr/bin/env python
"""Post-process: re-derive the corrected honest_negatives (regime-split + model-internal corroboration)
on a CACHED method_out.json, without re-running the model/judges. Adds mi_corroborates_fork per case.

This exists because the full-run toxicity (co-firing) case came out KG_BEATS_USUB on the LLM-judge joint
(both judges' CIs exclude 0) even though it is a co-firing case where KG is NOT a clean surgical handle
(footprint ~0.17, firing-Jaccard ~0.88) and the $0 model-internal joint does NOT corroborate the judge
edge (CI includes 0). The corrected honest_negatives report this faithfully instead of the stale
'predicted to lose' text. Pure text/derived-field fix — the numeric results are untouched.
"""
import json, sys
from pathlib import Path

import method  # build_honest_negatives, _mi_corroborates, save_json


def main():
    p = Path(sys.argv[1] if len(sys.argv) > 1 else "method_out.json")
    blob = json.loads(p.read_text())
    m = blob["metadata"]
    summaries = m["per_case"]
    second_available = m.get("judge", {}).get("second_judge_model", "unavailable") != "unavailable"
    honest = method.build_honest_negatives(summaries, second_available)   # mutates summaries -> mi_corroborates_fork
    m["honest_negatives"] = honest
    # propagate mi_corroborates_fork into the summary's per_case_fork view
    mic = {r["case_id"]: r.get("mi_corroborates_fork") for r in summaries}
    for e in m.get("summary", {}).get("per_case_fork", []):
        e["mi_corroborates_fork"] = mic.get(e["case_id"])
    method.save_json(blob, str(p))
    print(f"repatched {p.name}: {len(honest)} honest_negatives; mi_corroborates_fork = {mic}")
    for h in honest:
        print("  -", h[:140])


if __name__ == "__main__":
    main()
