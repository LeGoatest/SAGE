# Design

Status: DRAFT
Linked Requirements: requirements.md
Canon: canon/ (prevails)

---

## 1) Overview

Describe how the system will satisfy the approved requirements.

- No new architectural patterns unless explicitly approved.
- No canon mutation unless explicitly declared and approved.
- Must remain within selected Task Group boundaries.

---

## 2) Architecture Impact

### 2.1 Affected Components

- TODO: <component/file/module>
- TODO: <component/file/module>

### 2.2 Unaffected Components

- TODO: explicitly list critical components that must remain untouched.

---

## 3) Design Decisions

Each decision must reference one or more requirement IDs.

- DEC-001: <decision>
  - Satisfies: REQ-###
  - Rationale: <why this design>

- DEC-002: <decision>
  - Satisfies: REQ-###

---

## 4) Data / State Changes (if applicable)

- TODO

---

## 5) Interface Changes (if applicable)

- TODO

---

## 6) Governance & Canon Considerations

- Confirm no invariant violations.
- Confirm no protected zones modified.
- Confirm task group alignment.

If canon mutation is required:

- Specify invariant/rule ID
- Justify necessity
- Require HITL approval

---

## 7) Risk Analysis

- RISK-001: <description>
  - Mitigation: <strategy>

- RISK-002: <description>

---

## 8) Failure Alignment

Map failure states from requirements.md to mitigation strategy.

- FAIL-001 → <design safeguard>
- FAIL-002 → <design safeguard>

---

## 9) Acceptance Alignment

Explain how design enables each Acceptance Criterion.

- AC-001 → <design mechanism>
- AC-002 → <design mechanism>

---

## 10) HITL Gate

If architecture, governance, or security boundaries change:

[AWAIT_HUMAN_VALIDATION]
