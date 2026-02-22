---
name: spec-mode
description: Create a feature spec workspace in .jtasks and execute tasks step-by-step.
metadata:
  category: docs
  authority: procedural
  requires:
    - src/canon/ARCHITECTURE_RULES.md
    - JULES.md
    - TASK_GROUPS.md
    - SKILLS_INDEX.md
---

# Skill: Spec Mode (Plan → Tasks → Execute)

## Purpose
Provide a deterministic workflow to:
1) create a feature spec workspace under `.jtasks/`
2) generate a checkbox `tasks.md` plan
3) execute it step-by-step

## Workspace Layout
Create:
- `.jtasks/YYYY-MM-DDTHH-MM-SS/` (ISO 8601)
  - GAP_REPORT.md
  - requirements.md
  - design.md
  - tasks.md

Use templates from `.jtasks/_template/`.

## Procedure Checklist

### A) Classification Gate
1. Classify the request using `TASK_GROUPS.md`.
2. If classification is `architecture`, STOP.

### B) Generate Spec Files
1. Create the timestamped folder (ISO 8601).
2. Fill `GAP_REPORT.md` identifying the current state vs. desired state.
3. Fill `requirements.md` (EARS form).
4. Fill `design.md` referencing canonical docs in `src/canon/`.
5. Generate `tasks.md` with checkbox tasks.

### C) Task Authoring Rules
For each task in `tasks.md`:
- must declare exactly one task-group
- must declare a skill if one exists
- must list expected outputs

### D) Execution Mode
1. For each unchecked task in order:
   - validate task-group
   - implement changes
   - mark task [x] with a one-line result note

## Authority Boundary
This skill provides workflow structure only. It does NOT introduce architecture or redefine invariants.
