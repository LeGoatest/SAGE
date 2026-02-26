# HANDOVER

Status: DRAFT
Linked Task Folder: .jtasks/<timestamp>/
Purpose: Deterministic execution rehydration

---

## 1) Execution State

- Deep Mode completed: YES/NO
- Spec approved: YES/NO
- GAP_REPORT approved (if required): YES/NO
- Tasks completed:
  - TASK-001
  - TASK-002
- Tasks remaining:
  - TASK-003

---

## 2) Canon State

- Active canon ref / version_lock hash:
  - TODO
- Any canon mutations pending:
  - YES/NO
- Protected zones touched:
  - YES/NO

---

## 3) Validation State

- CI passing: YES/NO
- BLOCKER failures active: YES/NO
- If YES, list FAIL-IDs:
  - FAIL-###:

---

## 4) Files Modified So Far

List actual modified files to prevent drift:

- path/to/file.ext
- path/to/file.ext

---

## 5) Session Resume Instructions

When entering a new session:

1. Re-enter ENTER_DEEP_GOVERNANCE_MODE.
2. Re-validate reasoning_context.
3. Confirm canon version_lock.
4. Confirm task group.
5. Confirm no new drift.
6. Resume only remaining tasks.

No new implementation allowed until validation complete.

---

## 6) Risk Snapshot

- RISK-001:
- RISK-002:

---

## 7) Resume Mode

Next required mode:

- ENTER_DEEP_GOVERNANCE_MODE
- ENTER_SPEC_MODE
- ENTER_EXEC_MODE

---

If blocked:

[AWAIT_HUMAN_VALIDATION]
