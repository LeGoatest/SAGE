# Requirements

Status: DRAFT
Task Group: audit
Modes: ENTER_DEEP_GOVERNANCE_MODE → ENTER_SPEC_MODE → ENTER_EXEC_MODE
Canon: canon/ (prevails)

---

## 0) Brownfield Determination (Mandatory)

Is this task modifying or extending an existing system?

- YES → GAP_REPORT.md is REQUIRED.
- NO → GAP_REPORT.md is OPTIONAL.

---

## 1) Purpose

Align the machine-readable spec-governance layer with the narrative templates and intended v5.0 structure.

---

## 2) Evidence (No Inference)

- `CONSISTENCY_REPORT.md` generated during Deep Mode audit.
- Missing files list in `MISSING_FILES.md`.
- Template contents in `.jtasks/_template/`.

---

## 3) Structured Constraint Extraction (Required)

```yaml
reasoning_context:
  situation:
    - SAGE v5.0 narrative docs and templates are present, but core spec-governance rules are missing or redundant.
  constraints:
    - MUST NOT delete narrative docs (.docs/).
    - MUST update canon version lock.
    - MUST NOT invent new governance concepts.
  true_goal:
    - Synchronize the machine-readable canon with the narrative specification standards.
  failure_states:
    - FAIL-001: Missing rules result in governance-check bypass.
    - FAIL-002: Redundant invariants cause semantic logic conflicts.
```

---

## 4) Functional Requirements (EARS)

- REQ-001: The system SHALL include rules mandating requirements.md, design.md, and tasks.md.
- REQ-002: The system SHALL include rules enforcing "Failure Modeling" and "Traceability Matrix" in requirements.md.
- REQ-003: The system SHALL include rules enforcing "Satisfies: REQ-" and "Files Modified:" in tasks.md.
- REQ-004: The system SHALL consolidate redundant integration invariants.
- REQ-005: The system SHALL update the canon hash in `version_lock.yaml`.

---

## 5) Non-Functional Requirements

- NFR-001: 100% rule-template parity.

---

## 6) Traceability Matrix

| Requirement | Evidence | Design Ref | Task Ref | Test/Validation | Canon Link | Failure State |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| REQ-001 | CONSISTENCY_REPORT | design.md §1 | TASK-001 | local validate | N/A | FAIL-001 |
| REQ-002 | CONSISTENCY_REPORT | design.md §1 | TASK-002 | local validate | N/A | FAIL-001 |
| REQ-003 | CONSISTENCY_REPORT | design.md §1 | TASK-003 | local validate | N/A | FAIL-001 |
| REQ-004 | CONSISTENCY_REPORT | design.md §2 | TASK-004 | local validate | N/A | FAIL-002 |

---

## 7) Acceptance Criteria

- AC-001: All missing spec-rules present in `canon/rules/spec/`.
- AC-002: Redundant "integration" YAML files removed.
- AC-003: `sage-check` and `validator.py` pass.

---

## 8) HITL Gate

[AWAIT_HUMAN_VALIDATION]
