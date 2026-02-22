---
name: bootstrap-project
description: Bootstraps governance in an existing repo by scanning the codebase, identifying missing canonical docs, and producing a DRAFT canon pack (including a proposed ARCHITECTURE_RULES.md) plus a DECISIONS_NEEDED.md. Use when Jules is first introduced to an existing project.
metadata:
  authority: procedural
---

# Skill: bootstrap-project

## Authority boundary

This skill is **procedural only**.
It MUST NOT introduce architecture as fact.
It MUST NOT create new invariants unless they already exist in the repository or are explicitly provided by the user.
If required decisions are missing, the skill must STOP and ask for them.

## When to use

Use when:
- Jules is first introduced to a repository.
- Governance/canon files are missing or incomplete.
- The user requests “bootstrap”, “initialize”, or “set up rules/governance”.

Do not use when:
- The task is clearly a single-file edit.
- Architecture decisions are already complete and canonical.

## Procedure

### Step 1: Detect Project Language, Tooling, & Gaps
1) **Inventory Scan:**
   - Enumerate top-level folders and key packages.
   - Detect primary language and build systems (e.g., `go.mod`, `package.json`, `Makefile`).
   - Identify existing documentation (README, `src/`).
2) **Gap Analysis:**
   - Compare current state against the [Sovereign Agent Template structure](../../../README.md).
   - Identify missing canonical docs (Rules, Security, Index).
   - Identify missing agent governance files (JULES.md, TASK_GROUPS.md, SKILLS_INDEX.md).

**Output:** `GAP_REPORT.md` (detailing evidence found and missing components).

### Step 2: Generate Proposed Project Profile
Draft a `src/canon/PROJECT_PROFILE.md` based strictly on repo evidence.
Label it clearly as **[DRAFT - NEEDS HUMAN VALIDATION]**.

### Step 3: Output Proposed Canon (DRAFT)
Generate drafts for missing canon docs in `src/canon/`:
- `src/canon/ARCHITECTURE_RULES.md`
- `src/canon/SECURITY_MODEL.md`
- `src/canon/ARCHITECTURE_INDEX.md`

**Anti-Hallucination Rule (Mandatory):**
- When drafting canonical documents (especially `SECURITY_MODEL.md`):
  - MUST NOT invent trust boundaries, threat models, roles, or security properties.
  - MUST derive content only from explicit repository evidence.
  - If no security model evidence exists:
    - `SECURITY_MODEL.md` MUST contain ONLY:
      - "TODO: Security model not yet defined"
      - TODO list of questions/decisions
      - NO assumptions, NO proposed boundaries, NO defaults
  - If evidence incomplete:
    - Draft MUST be partial
    - Unknowns MUST be marked TODO
- Violation requires refusal.

### Step 4: Propose Additional Skills
Based on detected tooling (e.g., HTMX, Tailwind, Gin), suggest specific skill folders that should be created in `skills/`.
Do NOT create the full skill logic yet—only the folder and a draft `SKILL.md` with "Procedure: TBD".

### Step 5: Finalize Unresolved Decisions
Produce a `DECISIONS_NEEDED.md` file listing all unanswered questions required to finalize the canon.

**Format:**
- **Question:** [What needs to be decided?]
- **Why it matters:** [Impact on the system]
- **Target Location:** [Where it will be recorded (e.g., ARCHITECTURE_RULES)]

### Step 6: Stop Point (Crucial)
After producing the draft pack and `DECISIONS_NEEDED.md`:
1. STOP.
2. Present the `DECISIONS_NEEDED.md` to the user.
3. Wait for the user to validate the `PROJECT_PROFILE.md` and answer the pending decisions.
4. **Do NOT** proceed to implementation or "Final Canon" status without explicit instruction.

**Emit:**
[AWAIT_HUMAN_VALIDATION]
