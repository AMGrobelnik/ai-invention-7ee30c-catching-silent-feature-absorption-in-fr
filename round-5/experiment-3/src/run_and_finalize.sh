#!/bin/bash
# Self-finalizing full-run launcher for the M6 router (iter-5).
# Runs method.py --scale full to completion, then (ONLY on success) regenerates full/mini/preview,
# validates against exp_gen_sol_out, runs self_check.py, and checks file sizes. Emits unambiguous
# status markers so the orchestrating agent can finalize in ONE step on process exit.
# Launched via the harness-native run_in_background (tracked -> auto re-invoke on exit). NO detached
# monitor (that is what made iter-4 look idle and crash). PID-based only; never kill/grep by name.
set -u
cd /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_3
# NOTE: do NOT force HF offline mode — the model (unsloth/gemma-2-2b) + SAE are NOT pre-cached in this
# fresh container and must be downloaded over the network (HF reachable, HF_TOKEN set), exactly as the
# prior successful smoke run did. Forcing offline made model load fail.
export TOKENIZERS_PARALLELISM=false
PY=.venv/bin/python
OUT="$(pwd)/method_out.json"
RUNLOG=logs/full.out
FINLOG=logs/finalize.out
SKILL_DIR=/ai-inventor/.claude/skills/aii-json
APY="$SKILL_DIR/../.ability_client_venv/bin/python"
: > "$RUNLOG"; : > "$FINLOG"

echo "LAUNCH $(date +%H:%M:%S) gpu_free=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits 2>/dev/null | head -1)MiB"

# --- STEP A: full run (fresh process; idempotent; on-disk cache disabled by design) ---
timeout 9000 "$PY" method.py --scale full --out "$OUT" > "$RUNLOG" 2>&1
RC=$?
echo "RUN_EXIT rc=$RC $(date +%H:%M:%S)"
if [ "$RC" -ne 0 ] || ! grep -q "wrote .*method_out.json" "$RUNLOG"; then
  echo "RUN_FAILED rc=$RC (see $RUNLOG)"
  echo "---- last 25 lines of run log ----"; tail -25 "$RUNLOG"
  echo "ALL_DONE status=RUN_FAILED"
  exit 1
fi
echo "RUN_OK $(date +%H:%M:%S)"

# --- STEP B: confirm scale==full + concept count before finalizing ---
"$PY" - "$OUT" <<'PYEOF'
import json,sys
d=json.load(open(sys.argv[1])); m=d["metadata"]; ex=d["datasets"][0]["examples"]
nd=sum(1 for e in ex if e["metadata_role"]=="derivation")
print(f"CHECK scale={m.get('scale')} n_concepts={len(ex)} n_derivation={nd} recommended={m.get('recommended')}")
assert m.get("scale")=="full", "scale != full"
assert len(ex)>=26, "fewer than 26 concepts"
assert nd==12, "derivation != 12"
print("CHECK_OK")
PYEOF
[ $? -ne 0 ] && { echo "ALL_DONE status=CHECK_FAILED"; exit 1; }

# --- STEP C: regenerate full/mini/preview from the upgraded method_out.json ---
echo "FINALIZE_FORMAT $(date +%H:%M:%S)" | tee -a "$FINLOG"
"$APY" "$SKILL_DIR/scripts/aii_json_format_mini_preview.py" --input "$OUT" >> "$FINLOG" 2>&1
FMT_RC=$?
tail -6 "$FINLOG"
[ "$FMT_RC" -ne 0 ] && { echo "ALL_DONE status=FORMAT_FAILED rc=$FMT_RC"; exit 1; }

# --- STEP D: validate full/mini/preview against exp_gen_sol_out ---
VS="$SKILL_DIR/scripts/aii_json_validate_schema.py"
VAL_OK=1
for f in full_method_out.json mini_method_out.json preview_method_out.json; do
  echo "VALIDATE $f" | tee -a "$FINLOG"
  if "$APY" "$VS" --format exp_gen_sol_out --file "$(pwd)/$f" >> "$FINLOG" 2>&1; then
    echo "  $f PASSED"
  else
    echo "  $f FAILED"; VAL_OK=0; tail -8 "$FINLOG"
  fi
done
[ "$VAL_OK" -ne 1 ] && { echo "ALL_DONE status=VALIDATE_FAILED"; exit 1; }

# --- STEP E: self-check integrity assertions ---
echo "SELF_CHECK $(date +%H:%M:%S)"
"$PY" self_check.py "$OUT" 2>&1 | tee -a "$FINLOG"
SC_RC=${PIPESTATUS[0]}

# --- STEP F: file-size check (limit 100MB) ---
echo "FILE_SIZES:"; ls -lh full_method_out.json mini_method_out.json preview_method_out.json method_out.json
BIG=$(find . -maxdepth 1 -name "*method_out.json" -size +100M | head -1)
[ -n "$BIG" ] && echo "OVERSIZE $BIG" || echo "SIZE_OK all <100MB"

if [ "$SC_RC" -eq 0 ]; then
  echo "ALL_DONE status=SUCCESS $(date +%H:%M:%S)"
else
  echo "ALL_DONE status=SELFCHECK_NONZERO rc=$SC_RC $(date +%H:%M:%S)"
fi
