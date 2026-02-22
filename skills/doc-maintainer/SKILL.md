---
name: doc-maintainer
description: Procedure for synchronizing finalized design decisions and terminology from specs into the permanent canonical documentation.
metadata:
  category: maintenance
  authority: procedural
  requires:
    - ARCHITECTURE_INDEX.md
    - DECISIONS.md
    - TERMINOLOGY.md
---

# Skill: doc-maintainer

## Authority Boundary
This skill is **procedural only**.
It records existing decisions; it does NOT make new ones.
Documentation must reflect the *actual* implemented state or *explicitly approved* design.

## Procedure

### Step 1: Spec Review
Identify a finalized and executed spec in `.jtasks/`.
1. Review the `design.md` and `tasks.md`.
2. Extract any new architectural patterns, database schemas, or business rules that were implemented.
3. Extract any new terms or definitions used in the spec.

### Step 2: Decision Sync
1. Open `docs/DECISIONS.md`.
2. Record the new decision(s).
   - **ID**: [Next available ID]
   - **Title**: [Summary of the decision]
   - **Status**: [Accepted / Superseded]
   - **Context**: [Why it was needed]
   - **Consequences**: [Impact on future work]

### Step 3: Terminology Sync
1. Open `docs/TERMINOLOGY.md`.
2. Add any new ubiquitous language terms to ensure alignment between code, docs, and human communication.

### Step 4: Rule Propagation (Optional)
If a decision significantly alters the "Law" of the project:
1. Propose an update to `ARCHITECTURE_RULES.md`.
2. STOP and ask the human to approve the new rule.

### Step 5: Verification
Ensure that the updated docs follow the formatting rules in `docs/DOC_STYLE.md` (e.g., escaping backticks, using tilde fences).

## Guidelines
- Keep `DECISIONS.md` chronological.
- Ensure that superseded decisions are marked as such with a link to the new decision.
- "Documentation as Code": treat doc updates with the same rigor as code changes.
