# Requirements

Status: DRAFT
Task Group: TODO
Modes: ENTER_DEEP_GOVERNANCE_MODE → ENTER_SPEC_MODE → ENTER_EXEC_MODE
Canon: canon/ (prevails)

---

## 0) Brownfield Determination (Mandatory)

Is this task modifying or extending an existing system?

- YES → GAP_REPORT.md is REQUIRED.
- NO → GAP_REPORT.md is OPTIONAL.

If YES and GAP_REPORT.md is missing:
- STOP
- Emit: [AWAIT_HUMAN_VALIDATION]

---

## 1) Purpose

Define a testable, traceable specification for the requested change.

Implementation is forbidden until:
- requirements.md approved
- design.md approved
- tasks.md approved
- GAP_REPORT.md approved (if required)

---

## 2) Evidence (No Inference)

List explicit evidence.

- TODO: <path or link> — <what it proves>
- TODO: <path or link> — <what it proves>

Rules:
- Evidence must be explicit; no assumptions.
- If evidence is missing, mark TODO and add to DECISIONS_NEEDED.md (if applicable).
- Do not fabricate architecture, boundaries, or security properties.

---

## 3) Structured Constraint Extraction (Required)

Paste finalized Deep Mode reasoning_context here.

```yaml
reasoning_context:
  situation:
    - TODO
  constraints:
    - TODO
  true_goal:
    - TODO
  failure_states:
    - TODO
```

Rules:
- situation: evidence-only, no inference
- constraints: include canon + .docs + governance.yaml (if external canon) + task group + mode limits
- true_goal: outcome-only, remove identity/role/stylistic framing
- failure_states: explicit, testable, include canon IDs where applicable

---

## 4) Functional Requirements (EARS)

REQ-001: TODO

REQ-002: TODO

---

## 5) Non-Functional Requirements

NFR-001: TODO

NFR-002: MUST NOT violate canon invariants.

NFR-003: Same inputs MUST produce equivalent outputs.

NFR-004: TODO

---

## 6) Failure Modeling

FAIL-001: TODO

FAIL-002: TODO

---

## 7) Traceability Matrix

| Requirement | Evidence | Design Ref | Task Ref | Test/Validation | Canon Link | Failure State |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| REQ-001 | TODO | design.md §TODO | tasks.md TASK-001 | TEST-001 | TODO | FAIL-001 |
| REQ-002 | TODO | design.md §TODO | tasks.md TASK-002 | TEST-002 | TODO | FAIL-002 |

Rules:
- No orphan requirements.
- No tasks without requirement linkage.
- Canon links required for any governance/security constraint.

---

## 8) Acceptance Criteria

AC-001: TODO

AC-002: TODO

AC-003: CI/governance checks pass with zero BLOCKER failures.

AC-004: No protected zones were modified.

---

## 9) HITL Gate

If canon conflict, ambiguity, or governance mutation:

[AWAIT_HUMAN_VALIDATION]
