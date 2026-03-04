---
name: audit-governance
description: Audit repo governance, detect drift, and report compliance status against canonical documents.
task_groups:
  - GOVERNANCE
---

# AUDIT GOVERNANCE

## Purpose
This skill audits governance artifacts and enforcement wiring, then produces a compliance report.

## Canonical Inputs
- `.docs/canon/` (human-readable canon)
- `canon/` (machine-readable canon)
- `.governance/` (validators)

## Required Canon References
- canon/ARCHITECTURE_RULES.md
- canon/SECURITY_MODEL.md
- canon/ENFORCEMENT_MATRIX.md

## Workflow

1. Read the `canon/ARCHITECTURE_RULES.md` and `canon/SECURITY_MODEL.md`.
2. Confirm `.governance/` scripts exist and are referenced by CI.
3. Inspect `canon/rules/` and confirm spec invariants are present.
4. Identify drift:
   - Canon described behavior vs actual repository wiring.
   - Missing governance files referenced by other docs.
   - Redundant files that imply competing sources of truth.
5. Produce a report:
   - ✅ passes
   - ❌ failures
   - ⚠️ warnings
   - concrete fixes

## Checks

- Identify "Ghost Architecture" (patterns that exist in code but aren't in `canon/` or `.docs/canon/`).
- Identify duplicate governance and conflicting precedence.
- Trust the `canon/ENFORCEMENT_MATRIX.md` to determine how strictly a rule should be applied.

## Output
- `CONSISTENCY_REPORT.md` style summary or equivalent compliance report.
