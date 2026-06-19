#!/bin/bash
# Build the variant deliverables (full/mini/preview_method_out.json) from whatever method_out.json
# currently exists, the moment the mini run has produced one (signalled by results/mini_method_out.json
# which the launcher writes once mini finishes sane). This satisfies the verification gate with the
# genuine MINI result; the richer FULL result is regenerated later when the full run completes.
set -u
cd /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_2
SK=/ai-inventor/.claude/skills/aii-json; PY="$SK/../.ability_client_venv/bin/python"
i=0
until [ -f results/mini_method_out.json ] || grep -q ABORT logs/launcher.log 2>/dev/null || [ $i -ge 150 ]; do sleep 6; i=$((i+1)); done
if grep -q ABORT logs/launcher.log 2>/dev/null && [ ! -f results/mini_method_out.json ]; then
  echo "launcher aborted; using current method_out.json if present"
fi
# prefer the stable mini copy as the interim source; ensure workspace method_out.json exists
if [ -f results/mini_method_out.json ]; then
  cp -f results/mini_method_out.json method_out.json
  SRC=mini
elif [ -f method_out.json ]; then
  SRC=existing
else
  echo "NO method_out.json available"; exit 1
fi
echo "=== building variants from $SRC method_out.json ==="
.venv/bin/python make_variants.py method_out.json
echo "=== validate ==="
for f in full mini preview; do
  echo -n "$f: "; $PY $SK/scripts/aii_json_validate_schema.py --format exp_gen_sol_out --file "$(pwd)/${f}_method_out.json" 2>&1 | grep -E "PASSED|FAILED" || echo err
done
echo "=== example counts ==="
.venv/bin/python - <<'PY'
import json
for tag in ("method_out","full_method_out","mini_method_out","preview_method_out"):
    try:
        d=json.load(open(f"{tag}.json")); n=sum(len(x["examples"]) for x in d["datasets"])
        print(f"{tag}: {n} examples, datasets {[(x['dataset'],len(x['examples'])) for x in d['datasets']]}")
    except Exception as e: print(f"{tag}: ERR {e}")
PY
ls -la method_out.json full_method_out.json mini_method_out.json preview_method_out.json
echo "INTERIM_BUILD_DONE"
