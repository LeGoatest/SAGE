---
name: constitutional-check
description: Scans canonical documents for logical contradictions between modal operators (MUST, MUST NOT, SHALL, SHALL NOT).
metadata:
  category: audit
  authority: procedural
---

# Skill: constitutional-check

## Authority boundary
- This skill is **diagnostic only**.
- It identifies contradictions; it MUST NOT resolve them automatically.
- Resolving contradictions requires the Canon Mutation Process.

## When to use
- Before generating `tasks.md` in any non-trivial spec.
- During governance audits.
- After any update to canonical documents in `docs/`.

## Procedure

### Step 1: Extraction
1. Scan all files listed in `docs/ARCHITECTURE_INDEX.md`.
2. Extract all sentences containing the following modal operators:
   - MUST / MUST NOT
   - SHALL / SHALL NOT
   - REQUIRED / FORBIDDEN

### Step 2: Pairs Testing
1. Group extracted rules by subject or entity (e.g., "The Agent", "The Database", "Spec Files").
2. Perform pairwise comparison for logical contradictions.
   - Example contradiction: "Agent MUST refuse" vs "Agent MUST NOT refuse" for the same condition.

### Step 3: Reporting
1. If no contradictions are found, proceed with work.
2. If a contradiction is detected:
   - Emit `[AWAIT_HUMAN_VALIDATION]`.
   - List the conflicting rules and their source files/sections.
   - STOP execution.
   - Advise the user to initiate a Canon Mutation Process to resolve the conflict.

## Output
- Contradiction report (if applicable).
