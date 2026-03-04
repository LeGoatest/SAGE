---
name: doc-maintainer
description: Maintain documentation consistency across `.docs/` and keep it aligned with machine canon.
task_groups:
  - DOCUMENTATION
  - GOVERNANCE
---

# DOC MAINTAINER

## Purpose
Keep `.docs/` accurate, consistent, and aligned with the enforcement reality in `canon/` and `.governance/`.

## Workflow
1. Identify drift between `.docs/canon/` and `canon/`.
2. Update `.docs/` language to reflect reality.
3. Remove stale references (no `canon/`, no `docs/`).
4. Ensure paths match the actual repo structure.

## Output
- Updated `.md` files with full contents.
