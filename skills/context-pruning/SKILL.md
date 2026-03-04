---
name: context-pruning
description: Reduce context bloat while preserving canonical authority and task-critical facts.
task_groups:
  - GOVERNANCE
  - DOCUMENTATION
---

# CONTEXT PRUNING

## Purpose
Produce a minimal context pack that preserves canon precedence.

## Sources of Truth
- `.docs/canon/` (human)
- `canon/` (machine)

## Workflow
1. Extract only what is required to complete the task.
2. Preserve precedence statements and refusal logic.
3. Remove repetition and non-binding narrative.
4. Output a compact context summary.

## Output
- A compact “context pack” suitable for agent sessions.
