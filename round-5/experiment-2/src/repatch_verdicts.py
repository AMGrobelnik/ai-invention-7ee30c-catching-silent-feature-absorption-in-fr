#!/usr/bin/env python
"""Re-assemble the replication tables + cross_dictionary_replication dataset from a SAVED method_out.json
using the ACTUAL (fixed) build_replication_table / replication_dataset_rows from method.py — no model needed.
Heavy results (surgical CIs, router signals, multiplicity) are preserved in the compact concept results, so
this only re-labels per-piece verdicts under the reduced-run-aware logic. kg_repair_loop and
edit_locality_per_context datasets are verdict-independent and kept verbatim."""
import json, sys
from types import SimpleNamespace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import method as M

OUT = Path(__file__).parent / "method_out.json"
d = json.loads(OUT.read_text())
meta = d["metadata"]

per_dict_overall = {}
all_repl_rows = []
for dict_name, cfg in M.DICTS.items():
    if dict_name not in meta.get("replication_tables", {}):
        continue
    dinfo = meta["dictionaries"][dict_name]
    sae_stub = SimpleNamespace(sae_id=dinfo["sae_id"], avg_l0=dinfo["avg_l0"], d_sae=dinfo.get("d_sae"))
    gating = dinfo["gating"]
    multiplicity = dinfo["multiplicity"]
    router_xfer = meta["router_transfer"][dict_name]
    compact = meta["per_dictionary_concept_results"][dict_name]
    concept_results = [r for r in compact if r.get("concept") != "toxicity"]
    tox_result = next((r for r in compact if r.get("concept") == "toxicity"), None)
    table = M.build_replication_table(dict_name, cfg, sae_stub, gating, concept_results, tox_result,
                                      multiplicity, router_xfer)
    meta["replication_tables"][dict_name] = table
    per_dict_overall[dict_name] = table["overall_verdict"]
    all_repl_rows.extend(M.replication_dataset_rows(table))
    print(f"[{dict_name}] pieces={table['per_piece_verdicts']} overall={table['overall_verdict']} "
          f"regime_split co_firing_sel={table['regime_split'].get('co_firing_mean_selectivity')}")

# recompute the top-level cross-dictionary verdict
primary = "65k" if "65k" in per_dict_overall else (list(per_dict_overall)[0] if per_dict_overall else None)
meta["verdict"]["cross_dictionary_replicates"] = per_dict_overall.get(primary, "not_run")
meta["verdict"]["per_dictionary"] = per_dict_overall
meta["verdict"]["primary_dictionary"] = primary

# replace ONLY the cross_dictionary_replication dataset (verdict-encoding); keep others verbatim
for ds in d["datasets"]:
    if ds["dataset"] == "cross_dictionary_replication":
        ds["examples"] = all_repl_rows or [{"input": "none", "output": "NONE", "predict_none": "NONE"}]

OUT.write_text(json.dumps(d, indent=1, default=M._json_default))
print("CROSS-DICTIONARY VERDICT =", meta["verdict"]["cross_dictionary_replicates"], "per_dict =", per_dict_overall)
print("re-saved", OUT)
