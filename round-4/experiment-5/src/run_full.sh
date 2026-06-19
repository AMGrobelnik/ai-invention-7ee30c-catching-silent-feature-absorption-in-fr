#!/bin/bash
# Robust launcher for the full run on a CONTENDED shared single GPU.
# Each attempt is a FRESH process (in-process CUDA retry corrupts context), gated on a free GPU window,
# and MONITORED TO COMPLETION. On any death before method_out.json is written, it relaunches a fresh
# process (encodings recompute; on-disk cache is disabled to stay under the 100MB file limit). When the
# real run completes it AUTO-REGENERATES full/mini/preview from the upgraded method_out.json so the
# published deliverable is consistent (overwriting the small placeholder fallback).
cd /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_5
LOG=logs/full.out
DONE="wrote method_out.json"
NEED_FREE_MIB=8000
SKILL_DIR="/ai-inventor/.claude/skills/aii-json"
PY="$SKILL_DIR/../.ability_client_venv/bin/python"

finalize () {
  echo "FINALIZE: regenerating full/mini/preview from upgraded method_out.json $(date +%H:%M:%S)"
  "$PY" "$SKILL_DIR/scripts/aii_json_format_mini_preview.py" --input "$(pwd)/method_out.json" 2>&1 | tail -4
  echo "FINALIZE_DONE $(date +%H:%M:%S)"
}

echo "launcher start $(date +%H:%M:%S)"
for attempt in $(seq 1 60); do
  ok=0
  for w in $(seq 1 25); do
    free=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits 2>/dev/null | head -1 | tr -d ' ')
    if [ "${free:-0}" -ge "$NEED_FREE_MIB" ]; then ok=1; break; fi
    sleep 8
  done
  if [ "$ok" -ne 1 ]; then echo "attempt $attempt: no GPU window (free=${free:-?})"; continue; fi
  echo "attempt $attempt: launch fresh (free=${free}MiB) $(date +%H:%M:%S)"
  timeout 5400 .venv/bin/python method.py --scale full --out method_out.json > "$LOG" 2>&1 &
  PID=$!
  echo "attempt $attempt: pid=$PID"
  while kill -0 "$PID" 2>/dev/null; do
    if grep -q "$DONE" "$LOG" 2>/dev/null; then
      echo "RUN_COMPLETE attempt $attempt pid=$PID $(date +%H:%M:%S)"; finalize; exit 0
    fi
    sleep 10
  done
  if grep -q "$DONE" "$LOG" 2>/dev/null; then
    echo "RUN_COMPLETE (exited) attempt $attempt $(date +%H:%M:%S)"; finalize; exit 0
  fi
  tailmsg=$(grep -E "OutOfMemory|CUDA|Traceback" "$LOG" 2>/dev/null | tail -1)
  echo "attempt $attempt: died before completion [$tailmsg] $(date +%H:%M:%S)"
  sleep 8
done
echo "LAUNCHER_FAILED $(date +%H:%M:%S)"; exit 1
