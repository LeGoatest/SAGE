# Jules Modes Contract (Reference)

Canonical machine rules are defined in:

canon/rules/modes/modes_contract.yaml

If conflict exists, canon rules prevail.

---

# Jules Modes Contract

This document defines how Jules must behave when a mode is requested.

This file is non-canonical unless explicitly referenced by `canon/`.
If conflict exists, `canon/` prevails.

---

## Invocation Tokens

The following tokens activate modes:

- ENTER_DEEP_GOVERNANCE_MODE
- ENTER_SPEC_MODE
- ENTER_EXEC_MODE

If multiple tokens appear, precedence order is:

Deep → Spec → Exec

Higher mode suppresses lower modes.

---

## Deep Governance Mode

Purpose:
Constitutional and architectural validation before design or execution.

Allowed Outputs:

- risks
- rule citations (with file path)
- conflict explanations
- structural impact analysis
- verdict

Forbidden:

- implementation steps
- file edits
- speculative architecture
- relaxing constraints
- introducing new patterns

Loop Behavior:

- Maximum 3 passes
- Converge if two consecutive passes identify no new risks
- If pass 3 introduces new risks → emit HITL

Exit Condition:

- Explicit human instruction
- Clear "No constitutional risk detected" verdict

---

## Spec Mode

Purpose:
Define deterministic implementation plan.

Allowed Outputs:

- requirements.md
- design.md
- tasks.md
- HANDOVER.md (if incomplete)

Forbidden:

- file edits
- execution steps
- canon mutation
- architectural reinterpretation

Spec Mode MUST:

- Reference acceptance criteria
- Identify affected components
- Respect protected zones
- Align with canon invariants

---

## Execution Mode

Purpose:
Perform deterministic implementation defined in `tasks.md`.

Allowed Outputs:

- File edits required to satisfy tasks.md
- Minimal supporting glue code

Forbidden:

- Modifying canon unless:
  - Explicitly declared in tasks.md
  - Human approval recorded
  - Deep Governance Mode completed first

- Altering architecture without spec approval
- Expanding scope beyond tasks.md

Execution must remain bounded.

---

## Canon Mutation Rule

Canon may only change through formal mutation process.

Canon may only be modified if:

1. ENTER_DEEP_GOVERNANCE_MODE executed
2. Risks analyzed
3. Spec Mode defines mutation explicitly
4. Human approval recorded
5. Mutation scope is narrow and declared

Otherwise, canon is immutable.

---

## HITL Pause

When blocked, Jules MUST emit:

[AWAIT_HUMAN_VALIDATION]

Rules:

- Must appear alone on its own line
- Execution halts immediately
- May include a short bullet list explaining the block
- No additional output after marker

Triggers include:

- Canon conflict
- Ambiguous mode invocation
- Security boundary change
- Spec approval missing
- Mutation request without authorization
- Governance drift detected

---

## Determinism Guarantee

Modes exist to:

- Prevent cross-mode leakage
- Prevent speculative execution
- Prevent silent governance mutation
- Ensure reproducible behavior across sessions

Mode discipline is mandatory.
