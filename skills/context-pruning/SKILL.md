---
name: context-pruning
description: Produces a non-canonical MINI_CANON.md to reduce token bloat while preserving essential governance context.
metadata:
  category: operations
  authority: procedural
---

# Skill: context-pruning

## Authority boundary
- This skill MUST NOT modify canonical documents in `docs/` or `Jules/`.
- `docs/MINI_CANON.md` is informational only and has NO canonical authority.
- If a conflict exists between `MINI_CANON.md` and the `/docs` folder, the latter prevails.

## When to use
- When the conversation context becomes large.
- When token efficiency is required for complex execution.
- To provide a "quick reference" for the Agent's core operating rules.

## Procedure

### Step 1: Data Gathering
1. Read the Absolute Precedence List from `docs/ARCHITECTURE_INDEX.md`.
2. Extract all Refusal Triggers from `Jules/JULES.md`, `docs/ARCHITECTURE_RULES.md`, and `docs/SECURITY_MODEL.md`.
3. Extract Task Group rules from `Jules/TASK_GROUPS.md`.
4. Summarize the Spec-First workflow from `.jtasks/`.

### Step 2: Generate MINI_CANON.md
Produce `docs/MINI_CANON.md` following these strict constraints:
- **Max length**: 250 lines.
- **Format**: Bullet-heavy, high information density.
- **Mandatory Disclaimer**:
  > "MINI_CANON.md is not canonical; canon in /docs prevails."
- **Content MUST include**:
  - Precedence list (ordered).
  - Consolidated Refusal Triggers.
  - Task Group definitions.
  - Skill execution constraints.
  - Spec-first lifecycle summary.

### Step 3: Verification
- Ensure NO new rules were introduced.
- Ensure NO ambiguous canon was "interpreted" to fill gaps.
- Ensure NO security assumptions were added.

## Output
- `docs/MINI_CANON.md`
