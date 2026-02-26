#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"

bash "$ROOT/tools/sage-check.sh" "$ROOT"
python "$ROOT/tools/sage_validate.py" "$ROOT"

echo "SAGE-CONFORMANCE: PASS"
