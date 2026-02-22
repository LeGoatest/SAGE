# MUTATION PROCESS (Canon Evolution)

The Project Canon (files in `docs/` and `Jules/`) defines the project's constitution. This document establishes how this constitution is amended.

## 1. Triggering an Amendment
Amendments are required when:
- Existing rules are discovered to be insufficient or contradictory.
- A new architectural pattern is introduced.
- Trust or security boundaries are redefined.

## 2. The Amendment Workflow
1. **Request**: The user or agent identifies the need for a rule change.
2. **Drafting (Spec-First)**: A dedicated Spec is created in `.jtasks/` specifically for the `architecture` task group.
3. **Verification**: The agent analyzes the impact of the change on existing `INVARIANTS` and `AXIOMS`.
4. **Human Approval**: The amendment MUST be explicitly approved by the human authority. The agent cannot self-amend the canon.
5. **Execution**: Upon approval, the agent updates the canonical documents and records the update in `docs/DECISIONS.md`.

## 3. Atomic Updates
A canon mutation should be atomic. All dependent documents (Index, Rules, Matrix) must be updated in the same task to maintain consistency.
