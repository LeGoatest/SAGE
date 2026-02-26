#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"

die() { echo "SAGE-CHECK: $*" >&2; exit 1; }

req_file() {
  local p="$1"
  [[ -f "$ROOT/$p" ]] || die "Missing required file: $p"
}

echo "SAGE-CHECK: verifying required governance files..."

req_file ".docs/canon/ARCHITECTURE_RULES.md"
req_file ".docs/canon/ENFORCEMENT_MATRIX.md"
req_file ".docs/canon/TERMINOLOGY.md"
req_file ".docs/canon/DECISIONS.md"

req_file ".docs/governance/state-machine.md"
req_file ".docs/governance/deep-governance-mode.md"

req_file ".docs/canon/state-schema-v2.yaml"
req_file ".docs/canon/rule-schema-v2.governance.yaml"

req_file ".docs/reference/modes.md"

# Verify HITL marker appears in key canon files
grep -q "\[AWAIT_HUMAN_VALIDATION\]" "$ROOT/.docs/canon/ARCHITECTURE_RULES.md" || die "HITL marker missing in ARCHITECTURE_RULES.md"
grep -q "\[AWAIT_HUMAN_VALIDATION\]" "$ROOT/.docs/governance/deep-governance-mode.md" || die "HITL marker missing in deep-governance-mode.md"

# Verify forbidden transition is declared somewhere
grep -qi "Deep.*MUST NOT transition.*Execution" "$ROOT/.docs/canon/ARCHITECTURE_RULES.md" || die "Missing Deep→Exec invariant in ARCHITECTURE_RULES.md"

echo "SAGE-CHECK: OK"
