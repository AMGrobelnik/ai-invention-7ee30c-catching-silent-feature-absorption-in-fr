#!/bin/bash
# Wait for the mini run (PID passed as $1) to finish, sanity-check the judge pipeline,
# preserve the mini output, then launch the FULL run. PID-based (process-isolation safe).
set -u
cd /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_2
MINI_PID="${1:?need mini PID}"
export HF_HUB_OFFLINE=1

echo "[launcher] waiting on mini PID $MINI_PID ..."
i=0; while kill -0 "$MINI_PID" 2>/dev/null && [ $i -lt 360 ]; do sleep 10; i=$((i+1)); done
if kill -0 "$MINI_PID" 2>/dev/null; then echo "[launcher] ABORT: mini still running after wait"; exit 1; fi
echo "[launcher] mini finished."

if [ ! -f method_out.json ]; then echo "[launcher] ABORT: no mini method_out.json"; exit 1; fi

# sanity-check the mini result: pipeline must have produced edits + judge calls
SANE=$(.venv/bin/python - <<'PY'
import json
try:
    m=json.load(open("method_out.json"))["metadata"]
    calls=m["judge"]["calls"]; ne=len(m["edit_results"])
    large=next((e for e in m["edit_results"] if e.get("token")=="large"), None)
    large_mf = bool(large and large.get("meaningful_forget"))
    # pipeline is sane if judges ran AND >=3 edits produced AND large achieved meaningful forget (operator works)
    ok = (calls>0 and ne>=3 and large_mf)
    print("OK" if ok else "BAD")
    print(f"calls={calls} n_edit={ne} large_mf={large_mf}")
except Exception as e:
    print("BAD"); print("err:",repr(e)[:160])
PY
)
echo "[launcher] mini sanity: $SANE"
echo "$SANE" | head -1 | grep -q "^OK" || { echo "[launcher] ABORT: mini pipeline not sane (judges/operator) -- not launching full"; cp method_out.json results/mini_method_out_RAW.json 2>/dev/null; exit 1; }

cp method_out.json results/mini_method_out.json
echo "[launcher] preserved mini -> results/mini_method_out.json; launching FULL ..."
nohup .venv/bin/python method.py > logs/full.log 2>&1 &
FULL_PID=$!
echo "$FULL_PID" > logs/full.pid
echo "[launcher] FULL launched PID=$FULL_PID"
