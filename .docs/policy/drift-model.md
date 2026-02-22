# Drift Model

This document defines structured drift detection logic tied to governance states.

Non-canonical unless elevated via mutation.

---

## Drift Types

### Validation Drift
Deep Mode requires 3 passes frequently.
Indicates canon ambiguity.

### Mutation Pressure Drift
Mutation_required events increase over time.
Indicates unstable governance boundaries.

### Shadow Pattern Drift
Shadow architecture detections trend upward.
Indicates missing canonical pattern authorization.

### Transition Drift
Invalid transition attempts occur.
Indicates confusion in state model.

---

## Detection Windows

Recommended rolling window:
- 50 executions
- or 14 days (whichever first)

---

## Escalation Logic

If two or more drift types exceed thresholds:
- Recommend governance review
- Suggest Deep Mode usage for subsequent tasks

Policy escalates.
Canon decides.
