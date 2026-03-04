---
name: constitutional-check
description: Validate requests and planned outputs against SAGE constitutional precedence and canon.
task_groups:
  - GOVERNANCE
---

# CONSTITUTIONAL CHECK

## Purpose
Before doing work, validate the request against:
- `.docs/canon/` (human-readable constitution)
- `canon/` (machine-readable canon)

## Workflow
1. Identify which canon documents apply.
2. Check for conflicts with precedence.
3. If conflict exists, refuse and cite the conflicting rule.
4. If allowed, proceed with a deterministic output plan.

## Output
- Allowed / Conditional / Refused decision + the exact reasons.
