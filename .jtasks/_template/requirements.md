# Requirements

Status: DRAFT
Task Group: TODO
Modes: ENTER_DEEP_GOVERNANCE_MODE → ENTER_SPEC_MODE → ENTER_EXEC_MODE
Canon: canon/ (prevails)
Docs: .docs/ (must not be deleted)

---

## 1) Purpose

Define a testable, traceable specification for the requested change.

Implementation is forbidden until:
- requirements.md approved
- design.md approved
- tasks.md approved
- any required HITL validation completed

---

## 2) Request Summary

- TODO: one-paragraph summary of the request in plain language.

---

## 3) Evidence (No Inference)

List evidence sources used (files, paths, links, logs). Evidence must be explicit; no assumptions.

- TODO: <path or link> — <what it proves>
- TODO: <path or link> — <what it proves>

Rules:
- If evidence is missing, mark TODO and add to DECISIONS_NEEDED.md (if applicable).
- Do not fabricate architecture, boundaries, or security properties.

---

## 4) Structured Constraint Extraction (Required)

Before Spec or Exec, Deep Governance Mode MUST produce the following `reasoning_context` block.
Paste the finalized Deep Mode output here once produced.

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

## 5) Functional Requirements (EARS)

Each requirement MUST be:
- uniquely ID’d
- testable
- mapped in the Traceability Matrix (§8)

Template patterns:
- REQ-###: When <trigger>, the system SHALL <behavior>.
- REQ-###: While <state>, the system SHALL <behavior>.
- REQ-###: If <condition>, the system SHALL <behavior>.
- REQ-###: The system SHALL NOT <prohibited behavior>.

### Requirements

REQ-001: TODO

REQ-002: TODO

---

## 6) Non-Functional Requirements

NFR-001 (Performance): TODO

NFR-002 (Security/Governance): MUST NOT violate canon invariants.

NFR-003 (Determinism): Same inputs MUST produce equivalent outputs.

NFR-004 (Compatibility): TODO

---

## 7) Failure Modeling (Mandatory)

Define what “failure” means and how it is detected.

Each failure state MUST include:
- ID
- Description
- Detection method
- Severity (BLOCKER/HIGH/MED/LOW)
- Canon linkage (invariant/rule IDs) when applicable

### Failure States

FAIL-001: TODO
- Detection: TODO
- Severity: TODO
- Canon: TODO

FAIL-002: TODO
- Detection: TODO
- Severity: TODO
- Canon: TODO

### Negative Tests (if applicable)

NEG-001: TODO

---

## 8) Traceability Matrix (Mandatory)

Every requirement MUST trace to:
- Evidence
- Design section(s)
- Task(s)
- Test/Validation
- Canon linkage (when governance/security relevant)
- Failure state(s)

| Requirement | Evidence | Design Ref | Task Ref | Test/Validation | Canon Link | Failure State |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| REQ-001 | TODO | design.md §TODO | tasks.md TASK-001 | TEST-001 | TODO | FAIL-001 |
| REQ-002 | TODO | design.md §TODO | tasks.md TASK-002 | TEST-002 | TODO | FAIL-002 |

Rules:
- No orphan requirements.
- No tasks without requirement linkage.
- Canon links required for any governance/security constraint.

---

## 9) Acceptance Criteria

AC-001: TODO (observable pass condition)

AC-002: TODO (observable pass condition)

AC-003: CI/governance checks pass with zero BLOCKER failures.

AC-004: No protected zones were modified.

---

## 10) Out of Scope

OOS-001: TODO

OOS-002: TODO

---

## 11) HITL Gate

If any of the following are true, end this document with:

[AWAIT_HUMAN_VALIDATION]

Triggers:
- ambiguous task group classification
- canon conflict or required canon mutation
- security boundary modification
- unresolved DECISIONS_NEEDED.md items
- missing evidence for required claims
