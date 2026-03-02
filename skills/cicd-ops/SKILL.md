---
name: cicd-ops
description: CI/CD workflows and operational automation aligned with SAGE governance and enforcement.
task_groups:
  - CICD
  - GOVERNANCE
---

# CICD OPS

## Purpose
Create or modify CI/CD workflows that enforce SAGE governance and produce deterministic build outputs.

## Canon Alignment
- All workflow changes must respect `canon/` (machine) and `.docs/canon/` (human).

## Workflow
1. Identify existing workflows under `.github/workflows/`.
2. Ensure governance validators in `.governance/` run on PR/push.
3. Ensure any build workflows produce deterministic artifacts.
4. Refuse workflows that:
   - request secrets
   - exfiltrate data
   - disable governance checks

## Output
- Full workflow file(s) with explicit paths and complete content.
