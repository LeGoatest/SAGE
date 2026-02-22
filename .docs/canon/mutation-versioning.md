# Mutation Versioning Rules

This document defines deterministic versioning requirements for canonical changes.

Canon changes MUST be traceable.
Version changes MUST be deterministic.
Mutation MUST be explicit.

This document is canonical only if referenced by `ARCHITECTURE_INDEX.md`.
If not referenced, treat as enforcement guidance and keep it aligned with `ARCHITECTURE_RULES.md`.

---

## Version Fields

SAGT canon version is tracked as:

- Major.Minor

Where:
- Major increments on structural governance redesign
- Minor increments on additive canonical rules or enforcement expansions

---

## Mandatory Version Bump Conditions

A version bump is REQUIRED when any of the following occurs:

- Any change to `src/canon/ARCHITECTURE_RULES.md`
- Any change to `src/canon/SECURITY_MODEL.md`
- Any change to `src/canon/ENFORCEMENT_MATRIX.md`
- Any change that alters protected zone definitions or semantics
- Any change that introduces/changes rule-schema structured rules
- Any change that changes governance state machine semantics

If a change is purely editorial and does not change meaning, it MAY avoid bumping, but must be explicitly stated as editorial in `DECISIONS.md`.

---

## Where Version Is Recorded

Version must be recorded in:

- `src/canon/DECISIONS.md` (Decision entry must state the canon version impacted)

Optionally:
- a dedicated `src/canon/VERSION` file may be added later, but `DECISIONS.md` is authoritative for now.

---

## Deterministic Bump Procedure

When a mutation occurs:

1. Append a decision entry in `src/canon/DECISIONS.md`
2. The entry MUST include:
   - Date
   - New canon version
   - Summary
   - Rationale
   - Impact
3. Version must increase deterministically:
   - If structural redesign → Major++
   - Else → Minor++

---

## Prohibited Version Behavior

- Skipping version bumps on canonical changes
- Multiple conflicting versions in the same period
- Retroactively editing decision entries to change version history

If version history is ambiguous, execution must halt with HITL.

[AWAIT_HUMAN_VALIDATION]
