---
name: spec-mode
description: Enforce and generate Spec Mode artifacts in `.jtasks/<ISO-8601>/` with canonical structure.
task_groups:
  - SPECIFICATION
  - GOVERNANCE
---

# SPEC MODE

## Purpose
Create and maintain Spec Mode bundles under `.jtasks/<ISO-8601>/`.

## Canon Alignment
- Spec artifacts must match `canon/rules/spec/` (machine) and `.docs/canon/` (human).

## Workflow
1. Create `.jtasks/<ISO-8601>/`
2. Generate required artifacts:
   - requirements.md
   - tasks.md
   - GAP_REPORT.md
   - HANDOVER.md
3. Validate against canonical invariants.
4. Refuse ad-hoc feature work without a spec if required.

## Output
- Deterministic file tree + full file contents.
