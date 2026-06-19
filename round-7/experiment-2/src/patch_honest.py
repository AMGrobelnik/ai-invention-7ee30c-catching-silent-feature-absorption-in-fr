#!/usr/bin/env python
"""Post-process patch: append two honest-negative notes derived purely from the saved downstream data
(the Georgia positive-control NEAR_NOOP context + the Amazon-win interpretation). No model re-run."""
import json
from pathlib import Path

P = Path("/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_7/gen_art/gen_art_experiment_2/method_out.json")
b = json.loads(P.read_text())
m = b["metadata"]
dn = {r["case_id"]: r for r in m["downstream"]}
honest = m["honest_negatives"]

geo = dn.get("taxonomic_georgia"); amz = dn.get("named_entity_amazon")
notes = []
if geo is not None:
    notes.append(
        f"GEORGIA POSITIVE CONTROL = NEAR_NOOP_NO_WIN at the matched point: ablating the canonical country "
        f"absorber (16009) cannot induce non-trivial forgetting at 0.8*min(maxKG,maxSUB) "
        f"(max_forget_kg={geo['max_forget_kg']:.3f}, median matched forget-KL "
        f"{geo['edit_vs_noop_forget']['median_matched_forget_kl']:.4f}, frac-changed "
        f"{geo['edit_vs_noop_forget']['frac_forget_prompts_changed']:.2f}). This is the honest edit-vs-NOOP "
        f"R1 check: the iter-5/6 'KG beats dense' Georgia result was about LOWER COLLATERAL at matched forget, "
        f"NOT about KG forgetting strongly; pinned at KG's small single-latent KL ceiling, KG barely acts. "
        f"Reported, not hidden.")
if amz is not None and geo is not None:
    notes.append(
        f"NAMED-ENTITY ABSORBER IS A STRONGER EDIT HANDLE THAN THE COUNTRY ABSORBER: the Amazon homograph "
        f"absorber (6846) has a much larger single-latent forget ceiling (max_forget_kg={amz['max_forget_kg']:.3f}) "
        f"than the Georgia/country absorber ({geo['max_forget_kg']:.3f}), so KG-ABL on Amazon DOES forget "
        f"non-trivially (median {amz['edit_vs_noop_forget']['median_matched_forget_kl']:.3f}, frac-changed "
        f"{amz['edit_vs_noop_forget']['frac_forget_prompts_changed']:.2f}) and BEATS the footprint-matched gated "
        f"dense control under BOTH judges (KGvsGATED CI excl 0). This is a MODEST safety-adjacent (named-entity / "
        f"PII-style) bonus and does NOT alter the settled demographic-attribute null.")
# insert after the first two framing notes, before the per-case notes
honest[2:2] = notes
m["honest_negatives"] = honest
P.write_text(json.dumps(b, indent=1))
print(f"appended {len(notes)} honest notes; total {len(honest)}")
