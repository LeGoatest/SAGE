#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"

# Detection of SAGE root for injection awareness
SAGE_ROOT="${SAGE_ROOT:-$ROOT}"
if [ -d "$ROOT/.sage" ]; then
  SAGE_ROOT="$ROOT/.sage"
fi

die() { echo "SAGE-CHECK: $*" >&2; exit 1; }

echo "SAGE-CHECK: verifying required governance files..."

req_sage_file() {
  local p="$1"
  [[ -f "$SAGE_ROOT/$p" ]] || die "Missing required file: $p (in $SAGE_ROOT)"
}

req_sage_file ".docs/canon/ARCHITECTURE_RULES.md"
req_sage_file ".docs/canon/ENFORCEMENT_MATRIX.md"
req_sage_file ".docs/canon/TERMINOLOGY.md"
req_sage_file ".docs/canon/DECISIONS.md"

req_sage_file ".docs/canon/INVARIANT_MODEL.md"
req_sage_file ".docs/canon/SECURITY_MODEL.md"

req_sage_file ".docs/canon/rule-schema-v2.governance.yaml"

# Verify HITL marker appears in key canon files
grep -q "\[AWAIT_HUMAN_VALIDATION\]" "$SAGE_ROOT/.docs/canon/ARCHITECTURE_RULES.md" || die "HITL marker missing in ARCHITECTURE_RULES.md"

# Verify forbidden transition is declared somewhere
grep -qi "Deep.*MUST NOT transition.*Execution" "$SAGE_ROOT/.docs/canon/ARCHITECTURE_RULES.md" || die "Missing Deep→Exec invariant in ARCHITECTURE_RULES.md"

echo "SAGE-CHECK: OK"
