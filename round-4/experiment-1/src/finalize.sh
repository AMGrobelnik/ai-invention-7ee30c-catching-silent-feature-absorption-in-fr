#!/usr/bin/env bash
# Finalize: validate method_out.json against exp_gen_sol_out, generate mini/preview, check sizes.
set -e
W="/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_1"
SKILL_DIR="/ai-inventor/.claude/skills/aii-json"
PY="$SKILL_DIR/../.ability_client_venv/bin/python"

echo "=== validate exp_gen_sol_out ==="
$PY "$SKILL_DIR/scripts/aii_json_validate_schema.py" --format exp_gen_sol_out --file "$W/method_out.json" 2>&1 | grep -E "PASSED|FAILED|Error|Path" | head -20

echo "=== generate mini/preview ==="
$PY "$SKILL_DIR/scripts/aii_json_format_mini_preview.py" --input "$W/method_out.json" 2>&1 | tail -5

echo "=== sizes ==="
ls -lh "$W"/full_method_out.json "$W"/method_out.json "$W"/mini_method_out.json "$W"/preview_method_out.json 2>/dev/null

echo "=== size guard (<100MB each) ==="
for f in "$W"/method_out.json "$W"/full_method_out.json "$W"/mini_method_out.json "$W"/preview_method_out.json; do
  [ -f "$f" ] || continue
  sz=$(stat -c %s "$f")
  mb=$(( sz / 1048576 ))
  if [ "$sz" -gt 104857600 ]; then echo "OVERSIZE: $f = ${mb}MB"; else echo "OK: $(basename $f) = ${mb}MB"; fi
done
