#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"

die() { echo "SAGE-CHECK: $*" >&2; exit 1; }

req_file() {
  local p="$1"
  [[ -f "$ROOT/$p" ]] || die "Missing required file: $p"
}

echo "SAGE-CHECK: verifying required governance files..."

req_file "src/canon/ARCHITECTURE_RULES.md"
req_file "src/canon/ENFORCEMENT_MATRIX.md"
req_file "src/canon/TERMINOLOGY.md"
req_file "src/canon/DECISIONS.md"

req_file "src/governance/state-machine.md"
req_file "src/governance/deep-governance-mode.md"

req_file "src/canon/state-schema-v2.yaml"
req_file "src/canon/rule-schema-v2.governance.yaml"

req_file "src/reference/modes.md"

# Verify HITL marker appears in key canon files
grep -q "\[AWAIT_HUMAN_VALIDATION\]" "$ROOT/src/canon/ARCHITECTURE_RULES.md" || die "HITL marker missing in ARCHITECTURE_RULES.md"
grep -q "\[AWAIT_HUMAN_VALIDATION\]" "$ROOT/src/governance/deep-governance-mode.md" || die "HITL marker missing in deep-governance-mode.md"

# Verify forbidden transition is declared somewhere
grep -qi "Deep.*MUST NOT transition.*Execution" "$ROOT/src/canon/ARCHITECTURE_RULES.md" || die "Missing Deep→Exec invariant in ARCHITECTURE_RULES.md"

echo "SAGE-CHECK: OK"
