---
name: tailwindcss-cli
description: Tailwind CLI workflows aligned with SAGE determinism and minimal JS assumptions.
task_groups:
  - FRONTEND
  - BUILD
---

# TAILWINDCSS CLI

## Purpose
Provide deterministic Tailwind CLI setup and build instructions.

## Repo Reality Rules
- Do not reference nonexistent paths like `src/` or `docs/`.
- Use `.docs/` and `canon/` as the governance sources of truth.

## Output
- Deterministic commands + file outputs.
