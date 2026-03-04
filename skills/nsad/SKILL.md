---
name: nsad
description: Non-speculative analysis and diagnostics: grounded findings, concrete diffs, no invented paths.
task_groups:
  - GOVERNANCE
  - DEBUGGING
---

# NSAD

## Purpose
Produce grounded diagnostics and corrections without inventing structure.

## Hard Rules
- Do not reference nonexistent directories like `src/` or `docs/`.
- Use `.docs/` for human docs, `canon/` for machine rules, `.governance/` for validators.

## Workflow
1. Locate the file(s) involved.
2. Quote exact lines/sections.
3. Propose minimal changes that match repo reality.
4. Output deterministic patch files.

## Output
- Minimal patch list with full file contents.
