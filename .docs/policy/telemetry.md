# Telemetry (Policy)

This document defines recommended telemetry events for governance observability.

This file is non-canonical unless explicitly promoted into canon via mutation.
Canon prevails.

---

## Event Principles

Telemetry must be:
- externally recordable
- consistent across models
- deterministic in naming
- low ambiguity

Telemetry should not require model interpretation.
Prefer counters and boolean markers.

---

## Recommended Events

### Governance State Events
- governance_state_entered
  - state: Normal | Deep | Spec | Exec | HITL
  - reason: explicit | policy | escalation | workflow

- governance_state_exited
  - state
  - outcome: completed | escalated | refused | blocked

### Deep Mode Events
- deep_mode_entered
- deep_mode_pass_completed
  - pass: 1..3
  - new_risks_count: integer
- deep_mode_converged
  - pass: 2..3
- deep_mode_escalated_hitl
  - pass
  - reason: ambiguity | instability | conflict
- deep_mode_mutation_required
  - reason: protected_zone | authority_change | precedence_gap

### Spec Mode Events
- spec_mode_started
- spec_artifacts_written
  - requirements: true/false
  - design: true/false
  - tasks: true/false
- spec_mode_completed
- spec_mode_requires_approval

### Execution Events
- exec_started
- exec_task_completed
  - task_id
- exec_blocked
  - reason
- exec_completed

---

## Minimum Policy Use

At minimum, policy should monitor:
- deep_mode_entered frequency
- deep_mode_pass distribution
- HITL escalation rate
- refusal rate
- mutation-required rate

Telemetry exists to detect drift early.
