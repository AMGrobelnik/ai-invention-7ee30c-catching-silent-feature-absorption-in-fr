#!/bin/bash
# Wait for the FULL run (PID $1) to finish, then regenerate variants + validate + size-check from the
# full method_out.json. If the full run produced an invalid/short output, RESTORE the genuine mini result
# (results/mini_method_out.json) so a valid deliverable always exists. Prints FINAL_SUMMARY for the struct out.
set -u
cd /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_2
SK=/ai-inventor/.claude/skills/aii-json; PY="$SK/../.ability_client_venv/bin/python"
FPID="${1:?need full PID}"

echo "[finalize] waiting on full PID $FPID ..."
i=0; while kill -0 "$FPID" 2>/dev/null && [ $i -lt 1400 ]; do sleep 12; i=$((i+1)); done
if kill -0 "$FPID" 2>/dev/null; then echo "[finalize] WARNING: full still running after $((i*12))s; proceeding to check current output"; fi
echo "[finalize] full run ended (or timed out). verdict line:"; grep -E "verdict=" logs/full.log | tail -1

# decide source: full method_out.json if valid & >=50 examples, else restore mini
USE=$(.venv/bin/python - <<'PY'
import json,os
def nex(d): return sum(len(x["examples"]) for x in d.get("datasets",[]))
ok=False
try:
    d=json.load(open("method_out.json")); m=d["metadata"]
    assert "base_count" in m and "population_predictor" in m
    n=nex(d); ne=len(m.get("edit_results",{}))
    ok = (n>=50 and ne>=3)
    print("FULL" if ok else "RESTORE", f"examples={n} n_edit={ne}")
except Exception as e:
    print("RESTORE", "err:",repr(e)[:120])
PY
)
echo "[finalize] source decision: $USE"
if echo "$USE" | head -1 | grep -q "^RESTORE"; then
  echo "[finalize] restoring genuine mini result"
  cp -f results/mini_method_out.json method_out.json
fi

echo "[finalize] === make variants ==="
.venv/bin/python make_variants.py method_out.json
echo "[finalize] === sizes (100MB limit) ==="
for f in method_out.json full_method_out.json mini_method_out.json preview_method_out.json; do
  sz=$(stat -c%s "$f" 2>/dev/null || echo 0)
  printf "  %-28s %10d bytes  %s\n" "$f" "$sz" "$([ "$sz" -lt 104857600 ] && echo OK || echo OVER_100MB)"
done
echo "[finalize] === validate variants ==="
for f in full mini preview; do
  echo -n "  $f: "; $PY $SK/scripts/aii_json_validate_schema.py --format exp_gen_sol_out --file "$(pwd)/${f}_method_out.json" 2>&1 | grep -E "PASSED|FAILED" || echo err
done

echo "[finalize] === FINAL_SUMMARY ==="
.venv/bin/python - <<'PY'
import json
d=json.load(open("method_out.json")); m=d["metadata"]
bc=m["base_count"]; pop=m["population_predictor"]
print("verdict:",bc["verdict"],"| total_wins:",bc["total_independent_concentrated_wins"])
print("known_wins:",bc["known_wins"],"| new_wins:",bc["new_wins"])
print("pc_repro:",bc.get("positive_control_reproduces"))
print("predictor_verdict:",pop.get("predictor_verdict"),"| n:",pop.get("n"))
print("spearman_conc_mag:",pop.get("spearman_conc_mag"))
print("pb_conc_win:",pop.get("pb_conc_win"))
print("pb_absorp_mag:",pop.get("pb_absorp_mag"))
print("pb_absorp_win:",pop.get("pb_absorp_win"))
print("set_cover_inertness_rate:",m.get("set_cover_inertness_rate"),"| n_with_absorber:",m.get("set_cover_n_with_absorber"))
print("judge spent$:",m["judge"]["spent_usd"],"| calls:",m["judge"]["calls"])
print("gating:",m.get("gating_check"))
print("n screen rows:",len(m["concentration_screen_table"]),"| n edited:",len(m.get("edit_results",{})))
print("datasets:",[(x["dataset"],len(x["examples"])) for x in d["datasets"]])
print("EDITED:")
er=m.get("edit_results",{})
for uid,e in (er.items() if isinstance(er,dict) else []):
    print("  ",e.get("token"),"| st:",e.get("status"),"| mf:",e.get("meaningful_forget"),"| kbf:",e.get("kg_beats_fair"),"| conc:",round(e.get("concentration_score",0),3) if isinstance(e.get("concentration_score"),(int,float)) else e.get("concentration_score"))
print("HONEST_NEGATIVES:")
for h in m.get("honest_negatives",[]): print("  -",h[:160])
PY
echo "[finalize] FINALIZE_DONE"
