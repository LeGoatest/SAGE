---
name: bootstrap-project
description: Bootstrap a new project into SAGE governance with required canon + workflow scaffolding.
task_groups:
  - GOVERNANCE
  - PROJECT_BOOTSTRAP
---

# BOOTSTRAP PROJECT

## Purpose
Create a SAGE-governed repository skeleton, aligned with canon and standard enforcement.

## Canon Sources
- `.docs/canon/` for human-readable guidance
- `canon/` for machine-enforceable definitions

## Workflow
1. Create baseline folders:
   - `.docs/`
   - `.docs/canon/`
   - `.docs/reference/`
   - `canon/`
   - `canon/rules/`
   - `.governance/`
   - `skills/`
   - `.jtasks/`
2. Add minimum required canon artifacts:
   - `.docs/canon/ARCHITECTURE_RULES.md`
   - `.docs/canon/SECURITY_MODEL.md`
   - `.docs/canon/ENFORCEMENT_MATRIX.md`
   - `canon/` equivalents (machine-readable)
3. Wire CI enforcement for validators in `.governance/`.
4. Add a starter `skills/SKILLS_INDEX.md`.
5. Confirm precedence: `canon/` is the machine source of truth; `.docs/canon/` is human-readable.

## Output
- Deterministic file tree + full contents for created files.
