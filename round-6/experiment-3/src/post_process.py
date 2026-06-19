#!/usr/bin/env python
"""Post-process method_out.json: add the DERIVED 'downstream-confirmed absorption' view to the M7
absorption-breadth block (+ two honest notes). This is a pure DERIVED enrichment computed from the
already-measured entity_table (no re-measurement, no RNG, deterministic) — identical to what the
updated method.py aggregate_and_verdict() now emits natively on a re-run. Kept as a separate step
(the iter-5 repatch pattern) to avoid a ~60-min GPU re-run for a derived field.

Run:  .venv/bin/python post_process.py [method_out.json]
"""
import json, math, sys
from pathlib import Path

OLD_SANITY = ("SANITY: the absorption-PREDICTED count (recall_hole>tau_h_alone~0.78) is a STRICTER gate "
              "than the absorption-STRUCTURED breadth flag (recall_hole>0.5), so #predicted-absorption "
              "<= #structured by construction; both are reported.")
NEW_SANITY = ("SANITY: the absorption-PREDICTED rule (recall_hole>tau_h_alone~0.78) is a stricter recall-hole "
              "gate than the recall_hole>0.5 used in the structural flag, so #(recall_hole>0.78) <= "
              "#(recall_hole>0.5); the absorption-STRUCTURED count additionally requires firing-Jaccard<0.1, "
              "so it is not strictly nested with the predicted-absorption set. All counts are reported.")
STRUCT_NOTE = ("absorption_structured (recall-hole>0.5 AND firing-Jaccard<0.1) is a STRUCTURAL flag; "
               "ground_truth_regime=='absorption' (label-free unit beats best raw latent (a)) is the "
               "DOWNSTREAM benefit. They can disagree: structurally-absorption-shaped months can still be "
               "co_firing downstream, and the strongest downstream-absorption case can have high firing-"
               "Jaccard. Both lenses are reported.")


def _sanitize(o):
    import numpy as _np  # not needed but mirrors core; plain floats here
    if isinstance(o, dict):
        return {k: _sanitize(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_sanitize(v) for v in o]
    if isinstance(o, float):
        return o if math.isfinite(o) else None
    return o


def main():
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "method_out.json")
    d = json.loads(path.read_text())
    m = d["metadata"]
    et = m["entity_table"]
    b = m["absorption_breadth"]

    downstream_abs = sorted([e for e in et if e.get("ground_truth_regime") == "absorption"],
                            key=lambda e: -(e.get("delta_vs_a") or 0.0))
    downstream_confirmed = [dict(
        hierarchy=e["hierarchy"], entity=e["entity"],
        recall_hole=round(e["recall_hole"], 3), jaccard=round(e["jaccard"], 3),
        delta_vs_a=round(e["delta_vs_a"], 4), delta_vs_a_ci=e["delta_vs_a_ci"],
        auc_unit=round(e["auc_unit"], 3), auc_a=round(e["auc_a"], 3),
        absorption_structured=e["absorption_structured"], eligible=e["eligible"],
        predicted_regime=e["predicted_regime"]) for e in downstream_abs]

    b["n_downstream_confirmed_absorption"] = len(downstream_confirmed)
    b["downstream_confirmed_absorption_entities"] = downstream_confirmed
    b["structural_vs_downstream_note"] = STRUCT_NOTE

    # honest_notes: replace the old SANITY line with the new wording, then insert the structural!=downstream note
    notes = m.get("honest_notes", [])
    notes = [NEW_SANITY if n == OLD_SANITY else n for n in notes]
    struct_line = None
    if downstream_confirmed:
        top = downstream_confirmed[0]
        struct_line = (
            f"STRUCTURAL != DOWNSTREAM: {len(downstream_confirmed)} eligible-or-stable entities are "
            f"DOWNSTREAM-confirmed absorption (label-free unit beats best raw latent (a)); the strongest is "
            f"{top['hierarchy']}/{top['entity']} (delta_vs_a={top['delta_vs_a']:+.3f}, recall_hole="
            f"{top['recall_hole']:.3f}, jaccard={top['jaccard']:.3f}). Note the structurally-absorption-shaped "
            f"months (recall-hole>0.5 AND jaccard<0.1) can be co_firing DOWNSTREAM and the strongest downstream "
            f"win can have high firing-Jaccard — structural shape does not guarantee a grouping benefit.")
    if struct_line and struct_line not in notes:
        # insert right after the (new) SANITY note if present, else append
        if NEW_SANITY in notes:
            notes.insert(notes.index(NEW_SANITY) + 1, struct_line)
        else:
            notes.append(struct_line)
    m["honest_notes"] = notes

    path.write_text(json.dumps(_sanitize(d), indent=2, allow_nan=False))
    print(f"post-processed {path}: +{len(downstream_confirmed)} downstream_confirmed_absorption entities")
    for e in downstream_confirmed:
        print(f"  {e['hierarchy']}/{e['entity']}: delta_vs_a={e['delta_vs_a']:+.4f} hole={e['recall_hole']} "
              f"jac={e['jaccard']} structured={e['absorption_structured']} eligible={e['eligible']}")


if __name__ == "__main__":
    main()
