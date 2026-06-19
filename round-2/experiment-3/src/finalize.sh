#!/usr/bin/env bash
# Post-run: validate method_out.json against exp_gen_sol_out, check size, make mini/preview.
set -uo pipefail
cd "$(dirname "$0")"
SKILL_DIR="/ai-inventor/.claude/skills/aii-json"
PY="$SKILL_DIR/../.ability_client_venv/bin/python"

echo "=== file sizes ==="
ls -lh method_out.json results/*.json results/*.csv results/*.npz 2>/dev/null

echo "=== schema validation (exp_gen_sol_out) ==="
"$PY" "$SKILL_DIR/scripts/aii_json_validate_schema.py" --format exp_gen_sol_out \
  --file "$(pwd)/method_out.json"

echo "=== generate mini/preview ==="
"$PY" "$SKILL_DIR/scripts/aii_json_format_mini_preview.py" --input "$(pwd)/method_out.json"

echo "=== method_out.json top-level verdict ==="
.venv/bin/python - <<'PY'
import json
d = json.load(open("method_out.json"))
m = d["metadata"]
print("verdict:", m.get("verdict"))
for h, r in m.get("per_hierarchy", {}).items():
    print(f"[{h}] gate={r['gate_decision']} recovered={r['recovered_absorber_count']} "
          f"c3_confirmed={r['c3_confirmed']} absorbed={r['absorbed_subcontexts']} "
          f"anchor_recall_corp={r['anchor_recall_corpus']:.3f}")
print("datasets:", [(x['dataset'], len(x['examples'])) for x in d['datasets']])
PY
