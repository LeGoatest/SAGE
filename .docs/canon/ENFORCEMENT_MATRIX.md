# ENFORCEMENT_MATRIX

This document defines the severity and failure modes for rule violations.

```yaml sagrule
id: ENF-MATRIX-ADHERENCE
statement: "Agents MUST adhere to the enforcement levels defined in the ENFORCEMENT_MATRIX.md."
operator: MUST
context: audit
severity: ADVISORY
enforcement: REFUSAL
source: "docs/canon/ENFORCEMENT_MATRIX.md"
```

---

## 1. Severity Scale

| Level | Impact | Agent Action |
| :--- | :--- | :--- |
| CRITICAL | Structural Integrity / Security | Absolute Refusal + HITL |
| HIGH | Determinism Risk / Shadow Patterns | Refusal + CITATION |
| MODERATE | Efficiency Loss / Metadata Gap | Warning + TODO |
| LOW | Procedural Nit / Formatting | Warning |

---

## 2. Global Enforcement Rules

| Trigger | Severity | Action |
| :--- | :--- | :--- |
| Canon Conflict | CRITICAL | STOP + HITL |
| Security Ambiguity | CRITICAL | STOP + HITL |
| Mixed Task Group | HIGH | Refuse |
| Missing Spec | HIGH | Halt -> Enter Spec Mode |
| Shadow Pattern | HIGH | Halt -> Propose Mutation |
| Determinism Fail | HIGH | STOP + HITL |
| Ambiguous Mode | CRITICAL | STOP + HITL |

---

## 3. Failure Mode: Refusal (Absolute)

When a CRITICAL or HIGH violation occurs:
- No files are modified.
- No tasks are generated.
- The agent must cite the specific Rule ID.
- The agent must explain the conflict clearly.
