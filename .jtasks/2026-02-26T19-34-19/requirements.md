# Requirements

Status: DRAFT
Task Group: GOVERNANCE_CHANGE
Modes: ENTER_DEEP_GOVERNANCE_MODE → ENTER_SPEC_MODE → ENTER_EXEC_MODE
Canon: canon/ (prevails)
Docs: ..docs/ (must not be deleted)

---

## 1) Purpose

Implement the GAP_REPORT governance layer into SAGE v5.0, including machine-readable rules, updated spec templates, and CI validation.

---

## 2) Request Summary

The user wants to formalize the use of `GAP_REPORT.md` for brownfield modifications. This involves:
- Updating `requirements.md` and `GAP_REPORT.md` templates.
- Adding machine-readable invariants and rules to `canon/`.
- Adding a Python validation script to enforce the presence and validity of `GAP_REPORT.md`.
- Adding a GitHub Action.

---

## 3) Evidence (No Inference)

- User prompt providing `GAP_REPORT.md` template content.
- User prompt providing `requirements.md` template content.
- User prompt providing `gap_report_invariant.yaml` and `gap_report_rules.yaml`.
- User prompt providing `validate_gap_report.py` code.
- User prompt providing `sage-spec-gap-report.yml` GitHub Action.
- Existing `.jtasks/_template/` contents.
- Existing `canon/rules/` directory structure.

---

## 4) Structured Constraint Extraction (Required)

```yaml
reasoning_context:
  situation:
    - SAGE v5.0 is established but lacks explicit "brownfield" vs "greenfield" gating.
    - Spec templates need synchronization with the latest governance intent.
  constraints:
    - MUST NOT modify protected zones without authorizing a canon mutation.
    - MUST update `canon/version_lock.yaml` to maintain system integrity.
    - GAP_REPORT must be required when `tasks.md` lists existing files as modified.
    - BLOCKER risk levels in GAP_REPORT must fail validation.
  true_goal:
    - Integrate the provided GAP_REPORT and requirement template updates and enforcement logic into the SAGE framework.
  failure_states:
    - FAIL-001: GAP_REPORT logic missing from CI or local check.
    - FAIL-002: Requirements template does not match the provided EARS + Traceability structure.
    - FAIL-003: Version lock hash mismatch after changes.
```

---

## 5) Functional Requirements (EARS)

- REQ-001: When a task modifies existing files, the system SHALL require a `GAP_REPORT.md`.
- REQ-002: If `GAP_REPORT.md` contains "Risk Level: BLOCKER", validation SHALL fail.
- REQ-003: The `requirements.md` template SHALL include the EARS-style requirements section and a Traceability Matrix.
- REQ-004: The system SHALL update the canon version lock to reflect the new rules.

---

## 6) Traceability Matrix

| Requirement | Evidence | Design Ref | Task Ref | Test/Validation | Canon Link | Failure State |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| REQ-001 | User Prompt | N/A | TASK-002, TASK-004 | `validate_gap_report.py` | GAP_REPORT_REQUIRED_RULE | FAIL-001 |
| REQ-002 | User Prompt | N/A | TASK-004 | `validate_gap_report.py` | GAP_REPORT_BLOCKERS_MUST_BE_RESOLVED | FAIL-001 |
| REQ-003 | User Prompt | N/A | TASK-003 | Manual check | N/A | FAIL-002 |
| REQ-004 | User Prompt | N/A | TASK-006 | `validator.py` | IDENTITY_VERSION_LOCK | FAIL-003 |

---

## 7) Acceptance Criteria

- AC-001: `canon/rules/spec/` contains the new rule files.
- AC-002: `.jtasks/_template/GAP_REPORT.md` and `requirements.md` match user-provided content.
- AC-003: `tools/ci/validate_gap_report.py` correctly identifies brownfield changes and blockers.
- AC-004: `canon/version_lock.yaml` is updated and matches the current `canon/` hash.
- AC-005: GitHub Action file is present in `.github/workflows/`.
