---
name: audit-governance
description: A "self-check" procedure to identify architectural drift, security violations, or non-compliance with canonical documentation.
metadata:
  category: audit
  authority: procedural
  requires:
    - src/canon/ARCHITECTURE_RULES.md
    - src/canon/SECURITY_MODEL.md
    - src/canon/ENFORCEMENT_MATRIX.md
---

# Skill: audit-governance

## Authority Boundary
This skill is **procedural only**.
It detects violations; it does NOT change rules.
If a violation is found, the agent must report it and STOP before modifying code.

## Procedure

### Step 1: Scope Selection
Identify the scope of the audit:
- **Full Audit**: Scan the entire repository.
- **Delta Audit**: Scan only the files changed in the current branch or task.
- **Thematic Audit**: Scan specifically for one rule (e.g., "Security Model compliance").

### Step 2: Rule Mapping
1. Read the `src/canon/ARCHITECTURE_RULES.md` and `src/canon/SECURITY_MODEL.md`.
2. Extract the active invariants (e.g., "No direct DB access from Port layer").
3. Create a temporary checklist of these rules for the target files.

### Step 3: Scan & Evidence Collection
For each file in scope:
- Check for direct violations of the rule checklist.
- **Shadow Rule Detection**: Identify any non-trivial pattern introduced in code that lacks an authorizing canon citation.
  - If unauthorized: Emit `[AWAIT_HUMAN_VALIDATION]` and offer to simplify or create a Mutation Spec.
- **Dead Canon TTL Check**: Review `.jtasks` history for Canon Citations.
  - Any rule not cited within 180 days MUST be flagged for "Deprecation Review".
  - MUST NOT be auto-deleted.
- Identify "Ghost Architecture" (patterns that exist in code but aren't in `src/`).

### Step 4: Output Audit Report
Produce an `AUDIT_REPORT.md` (usually in the current `.jtasks` folder or root).

**Format:**
- **Violation**: [Rule cited]
- **Evidence**: [File path + line number or code snippet]
- **Severity**: [Critical / Warning / Advisory]
- **Recommendation**: [How to fix or if a DECISION is needed]

### Step 5: Stop Point
If any **Critical** violations are found, the Agent MUST STOP and present the report to the user. Do not attempt to fix violations unless specifically instructed via a new task.

## Guidelines
- Trust the `src/canon/ENFORCEMENT_MATRIX.md` to determine how strictly a rule should be applied.
- Look for "Import violations" as the most common source of architectural drift.
- Check for unhandled errors or missing security middleware in `Port` layers.
