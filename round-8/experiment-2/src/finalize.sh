#!/bin/bash
# Finalize: build full/mini/preview variants, check sizes, validate against exp_gen_sol_out, print summary.
# PID-based (process-isolation safe): pass the full-run PID as $1 (optional); we wait on it, never pgrep by name.
set -u
cd /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_2
SK=/ai-inventor/.claude/skills/aii-json
VAL="$SK/../.ability_client_venv/bin/python $SK/scripts/aii_json_validate_schema.py"
WS=$(pwd)
PID="${1:-}"

if [ -n "$PID" ]; then
  echo "[finalize] waiting on PID $PID ..."
  i=0; while kill -0 "$PID" 2>/dev/null && [ $i -lt 1200 ]; do sleep 10; i=$((i+1)); done
  kill -0 "$PID" 2>/dev/null && echo "[finalize] WARNING still running after wait" || echo "[finalize] run finished"
fi

echo "[finalize] verdict line:"; grep -E "verdict=" logs/full.log | tail -1
echo "[finalize] method_out.json:"; ls -la method_out.json 2>/dev/null | awk '{print $5,$6,$7,$8}'

echo "[finalize] === make variants ==="
.venv/bin/python make_variants.py method_out.json

echo "[finalize] === sizes (100MB limit) ==="
for f in method_out.json full_method_out.json mini_method_out.json preview_method_out.json; do
  sz=$(stat -c%s "$f" 2>/dev/null || echo 0)
  printf "%-30s %10d bytes  %s\n" "$f" "$sz" "$([ "$sz" -lt 104857600 ] && echo OK || echo OVER_100MB)"
done

echo "[finalize] === validate variants (exp_gen_sol_out) ==="
for f in full mini preview; do
  echo -n "$f: "; $VAL --format exp_gen_sol_out --file "$WS/${f}_method_out.json" 2>&1 | grep -E "PASSED|FAILED" || echo "validator-error"
done

echo "[finalize] === summary ==="
.venv/bin/python - <<'PY'
import json
d=json.load(open("method_out.json")); m=d["metadata"]
bc=m["base_count"]; pop=m["population_predictor"]
print("verdict:", bc["verdict"], "| total_wins:", bc["total_independent_concentrated_wins"])
print("known_wins:", bc["known_wins"], "| new_wins:", bc["new_wins"])
print("pc_repro:", bc.get("positive_control_reproduces"))
print("predictor_verdict:", pop.get("predictor_verdict"), "| n:", pop.get("n"))
print("spearman_conc_mag:", pop.get("spearman_conc_mag"))
print("pb_absorp_mag:", pop.get("pb_absorp_mag"))
print("set_cover_inertness_rate:", m.get("set_cover_inertness_rate"), "| n_with_absorber:", m.get("set_cover_n_with_absorber"))
print("judge spent:", m["judge"]["spent_usd"], "calls:", m["judge"]["calls"])
print("n screen rows:", len(m["concentration_screen_table"]))
print("datasets:", [(x["dataset"], len(x["examples"])) for x in d["datasets"]])
print("edited tokens:")
for e in m["edit_results"]:
    print("  ", e.get("token"), "| status", e.get("status"), "| mf", e.get("meaningful_forget"),
          "| kg_beats_fair", e.get("kg_beats_fair"), "| dJoint_fair_p", e.get("delta_joint_vs_fair_primary"))
print("HONEST NEGATIVES:")
for h in m["honest_negatives"]: print("  -", h[:160])
PY
echo "[finalize] DONE"
