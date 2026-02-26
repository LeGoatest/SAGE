# Tasks

Status: DRAFT
Linked Requirements: requirements.md
Linked Design: design.md

Execution is forbidden until this document is approved.

---

## 1) Task Rules

- Each task must map to at least one REQ-###.
- No task without requirement linkage.
- No task outside selected Task Group.
- No canon mutation unless explicitly declared and approved.

---

## 2) Task List

### TASK-001
- Description: TODO
- Satisfies: REQ-###
- Files Modified:
  - path/to/file.ext
- Test/Validation:
  - TEST-001

---

### TASK-002
- Description: TODO
- Satisfies: REQ-###
- Files Modified:
  - path/to/file.ext
- Test/Validation:
  - TEST-002

---

## 3) Validation Tasks

### TEST-001
- Verifies: REQ-###
- Method: TODO

### TEST-002
- Verifies: REQ-###
- Method: TODO

---

## 4) Governance Validation

- Confirm reasoning_context was produced in Deep Mode.
- Confirm no protected zones modified.
- Confirm task group alignment.
- Confirm no illegal mode transition.

---

## 5) Completion Criteria

Task execution is complete only when:

- All tasks implemented.
- All tests pass.
- No BLOCKER failure states active.
- Canon validation passes.

---

## 6) HITL Gate

If scope changes, classification shifts, or canon mutation becomes necessary:

[AWAIT_HUMAN_VALIDATION]
