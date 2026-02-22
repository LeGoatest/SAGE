# Governance State Machine

SAGT treats “modes” as **governance states** in a deterministic state machine.
States are not vibes, and they do not expand authority.

This document defines:
- the set of governance states
- allowed transitions
- invalid transitions (must halt)
- the minimum output contracts per state

If any transition is ambiguous, execution must halt with:
[AWAIT_HUMAN_VALIDATION]

---

## States

### Normal
Default governed behavior. Requests are classified into exactly one task group.

### Deep Governance Mode
Pre-flight validation intensifier. Multi-pass risk discovery and convergence.
No planning artifacts. No implementation steps.

### Spec Mode
Planning-only. Generates requirements/design/tasks. No execution.

### Execution Mode
Task execution-only. Runs tasks.md items under canon constraints.

### HITL Pause
Explicit stop awaiting human validation. No further output beyond what is needed to unblock.

---

## Transition Rules

- Normal → Deep Governance Mode (explicit trigger or policy escalation)
- Normal → Spec Mode (explicit request for spec-first work)
- Normal → Execution Mode (only if a complete approved spec exists and execution is explicitly requested)

- Deep Governance Mode → Spec Mode (only if “Execution safe = Yes”)
- Deep Governance Mode → HITL Pause (if any ambiguity or instability is detected)
- Deep Governance Mode → Execution Mode (FORBIDDEN)

- Spec Mode → HITL Pause (approval required before execution)
- Spec Mode → Normal (after spec delivery, awaiting next instruction)
- Spec Mode → Execution Mode (FORBIDDEN unless explicitly re-entered via Execution Mode request)

- Execution Mode → Normal (task completion)
- Execution Mode → HITL Pause (blocked by conflict, protected zone, security ambiguity, or mutation requirement)

---

## Invalid Transitions

Any of the following must trigger a hard stop:
- Deep Governance Mode → Execution Mode
- Spec Mode → Execution Mode without explicit user authorization
- Execution Mode without an approved tasks.md
- Any state transition that requires mutation but mutation has not been initiated

Hard stop behavior:
- Emit `[AWAIT_HUMAN_VALIDATION]` on its own line
- Provide a short bullet list: what is blocked + what decision is required
- Stop output immediately afterward

---

## Output Contracts by State

### Deep Governance Mode Output Contract
Must output ONLY:
- Risk list (bullets)
- Canon citations (file + section)
- Determinism impact (None/Low/Moderate/High)
- Mutation required? (Yes/No)
- Execution safe? (Yes/No)

No implementation steps. No file edits.

### Spec Mode Output Contract
Must output ONLY:
- requirements.md
- design.md
- tasks.md
- HANDOVER.md (if incomplete)

No implementation changes.

### Execution Mode Output Contract
May output:
- File edits required by tasks.md
- Patch-style changes or full file replacements

Must halt on any HITL trigger.

---

## Mermaid Diagram

```mermaid
stateDiagram-v2
  [*] --> Normal

  Normal --> Deep : ENTER_DEEP_GOVERNANCE_MODE / policy escalation
  Normal --> Spec : ENTER_SPEC_MODE
  Normal --> Exec : ENTER_EXEC_MODE (only if approved spec exists)

  Deep --> Spec : safe=yes
  Deep --> HITL : ambiguity/instability
  Deep --> Exec : forbidden

  Spec --> HITL : approval needed
  Spec --> Normal : spec delivered

  Exec --> Normal : tasks complete
  Exec --> HITL : blocked/unsafe
