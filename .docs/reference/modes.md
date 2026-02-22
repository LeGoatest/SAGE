# Modes and Governance States

SAGT uses the term “mode” to mean a **governance state**.
States constrain what outputs are allowed at a given time.

A mode is not a skill.
A mode is not a task group.
A mode is not a tool.

Modes exist to prevent accidental authority mixing.

---

## What a Mode Is

A mode is:
- a named governance state
- with allowed outputs
- with explicit transitions
- with deterministic stopping conditions

Modes are machine-detectable because they are invoked by explicit tokens.

---

## What a Mode Is Not

A mode is not:
- an excuse to “think harder”
- a permission to rewrite canon
- a way to bypass task groups
- a way to produce implementation while “planning”

If a mode is used to expand authority, governance has failed.

---

## Core Modes

### Deep Governance Mode
Validation-only. Multi-pass convergence analysis.
Outputs: risk list + citations + verdict.

### Spec Mode
Planning-only. Produces requirements/design/tasks.
Outputs: spec artifacts only.

### Execution Mode
Execution-only. Produces file changes under tasks.md.
Outputs: code/docs edits only.

### HITL Pause
Stop state awaiting human validation.
Outputs: marker + minimal unblock info only.

---

## Determinism and Modes

Determinism requires that:
- state transitions are explicit
- outputs are constrained by state
- mode behavior does not vary by model “personality”

If two models interpret a mode differently, the mode definition is incomplete and must be strengthened.

---

Modes provide temporal governance.
They make “what is allowed right now” explicit.
