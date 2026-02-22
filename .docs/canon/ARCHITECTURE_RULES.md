# ARCHITECTURE_RULES

This document defines the highest-precedence invariants for SAGT.

These rules are binding.
Agents must refuse when these rules are violated or when compliance is ambiguous.

This document governs governance. It does not govern downstream application architecture.

---

## 0) Supreme Authority

```yaml sagrule
id: ARCH-SUPREME-AUTHORITY
statement: "This file overrides all other docs and comments."
operator: MUST
context: all
severity: CRITICAL
enforcement: REFUSAL
source: "src/canon/ARCHITECTURE_RULES.md §0"
```

- This file overrides all other docs and comments.
- If ambiguity exists, prefer: [Isolation > Reliability > Resilience] (Placeholder).

---

## 1) System Boundaries

```yaml sagrule
id: ARCH-SYSTEM-BOUNDARIES
statement: "Agents MUST strictly adhere to system boundaries: src/** for governance, Jules/ for agent OS, .jtasks/ for planning."
operator: MUST
context: all
severity: CRITICAL
enforcement: REFUSAL
source: "src/canon/ARCHITECTURE_RULES.md §1"
```

- `src/**` only when explicitly updating governance/canon.
- `Jules/` for agent governance and skills.
- `.jtasks/` for planning and execution workspaces.

---

## Rule A1 — Canon Precedence Is Mandatory

```yaml sagrule
id: A1
statement: "Canonical precedence order must be followed as declared in ARCHITECTURE_INDEX.md."
operator: MUST
context: all
severity: CRITICAL
enforcement: REFUSAL
source: "src/canon/ARCHITECTURE_RULES.md §Rule A1"
```

Canonical precedence order must be followed as declared in `ARCHITECTURE_INDEX.md`.

Agents must not reinterpret precedence or “merge” conflicting rules.

If precedence does not resolve a conflict, the agent must halt and emit:

[AWAIT_HUMAN_VALIDATION]

---

## Rule A2 — One Task Group per Execution

```yaml sagrule
id: A2
statement: "Every request must be classified into exactly one task group."
operator: MUST
context: all
severity: CRITICAL
enforcement: REFUSAL
source: "src/canon/ARCHITECTURE_RULES.md §Rule A2"
```

Every request must be classified into exactly one task group.

Mixed task groups are forbidden.

If classification is ambiguous, execution must halt and require human validation.

---

## Rule A3 — Skills Are Procedural Only

```yaml sagrule
id: A3
statement: "Skills may execute only deterministic procedures and MUST NOT introduce architecture or modify canon."
operator: MUST
context: all
severity: CRITICAL
enforcement: REFUSAL
source: "src/canon/ARCHITECTURE_RULES.md §Rule A3"
```

Skills may execute only deterministic procedures.

Skills must not:
- Introduce architecture
- Modify canon
- Modify invariants
- Fill missing security boundaries
- Interpret ambiguous canon

If a skill requires design judgment, it must stop.

---

## Rule A4 — Spec-First for Non-Trivial Work

```yaml sagrule
id: A4
statement: "Non-trivial work requires spec artifacts (requirements, design, tasks) and explicit human approval."
operator: MUST
context: all
severity: CRITICAL
enforcement: REFUSAL
source: "src/canon/ARCHITECTURE_RULES.md §Rule A4"
```

Non-trivial work requires spec artifacts:
- requirements.md
- design.md
- tasks.md

Execution begins only after explicit human instruction.

If a request is non-trivial and no spec exists, the agent must halt and require spec generation.

---

## Rule A5 — Refusal Is Enforced

```yaml sagrule
id: A5
statement: "Refusal is required when canon conflicts exist, task groups are ambiguous, or security model lacks evidence."
operator: MUST
context: all
severity: CRITICAL
enforcement: REFUSAL
source: "src/canon/ARCHITECTURE_RULES.md §Rule A5"
```

Refusal is required when:
- Canon conflicts exist
- Task group classification is ambiguous
- Protected zones would be modified without mutation
- Security model is undefined or lacks evidence
- Determinism cannot be guaranteed
- Compiler validation fails (if enabled)

Refusal must be explicit and must stop execution.

---

## Rule A6 — Protected Zones Are Immutable Without Mutation

```yaml sagrule
id: A6
statement: "Protected zones (governance, canon) cannot be modified without formal Canon Mutation."
operator: MUST_NOT
context: all
severity: CRITICAL
enforcement: REFUSAL
source: "src/canon/ARCHITECTURE_RULES.md §Rule A6"
```

Protected zones define structural invariants and security boundaries.

Protected zones cannot be modified by:
- Skills
- Implementation tasks
- Routine documentation updates

Any modification requires Canon Mutation and human validation.

---

## Rule A7 — Mutation Is the Only Legal Canon Change

```yaml sagrule
id: A7
statement: "Canon may only change through formal mutation process involving human validation."
operator: MUST
context: all
severity: CRITICAL
enforcement: REFUSAL
source: "src/canon/ARCHITECTURE_RULES.md §Rule A7"
```

Canon may only change through formal mutation.

Mutation must include:
- Proposal
- Impact analysis
- Human validation
- Version traceability

Any attempt to “just update the docs” that modifies authority is a violation.

---

## Rule A8 — No Shadow Architecture

```yaml sagrule
id: A8
statement: "Agents MUST NOT introduce structural patterns not authorized by canon."
operator: MUST_NOT
context: all
severity: CRITICAL
enforcement: REFUSAL
source: "src/canon/ARCHITECTURE_RULES.md §Rule A8"
```

Agents must not introduce structural patterns not authorized by canon.

If a pattern is needed:
- remove it, or
- initiate a canon mutation to authorize it

Silent adoption is prohibited.

---

## Rule A9 — Determinism Is Required

```yaml sagrule
id: A9
statement: "Outputs MUST converge structurally given the same canon version, spec, and inputs."
operator: MUST
context: all
severity: CRITICAL
enforcement: REFUSAL
source: "src/canon/ARCHITECTURE_RULES.md §Rule A9"
```

Given the same canon version, spec, and inputs, outputs must converge structurally.

If determinism cannot be guaranteed due to ambiguity or missing authority, execution must halt.

---

## Rule A10 — HITL Break-Glass Marker Is Mandatory

```yaml sagrule
id: A10
statement: "When execution pauses for validation, the agent MUST emit [AWAIT_HUMAN_VALIDATION] on its own line."
operator: MUST
context: all
severity: CRITICAL
enforcement: REFUSAL
source: "src/canon/ARCHITECTURE_RULES.md §Rule A10"
```

When execution must pause for validation, the agent must emit:

[AWAIT_HUMAN_VALIDATION]

The marker must appear on its own line.
After emitting it, the agent must not continue execution.

---

## Rule A11 — Governance State Machine Is Mandatory

Refer to `src/canon/rule-schema-v2.governance.yaml` for structured definition.

SAGT governance operates as a deterministic state machine with explicit states and transitions.

States include:
- Normal
- Deep Governance Mode
- Spec Mode
- Execution Mode
- HITL Pause

If a request attempts to combine outputs from multiple states (e.g., planning + execution), governance must halt.

State transitions must be explicit and must follow the transition rules documented in governance.

---

## Rule A12 — Deep Governance Mode

Refer to `src/canon/rule-schema-v2.governance.yaml` for structured definition.

Deep Governance Mode is a governance validation state used before planning or execution.

Deep Mode must:
- run up to 3 validation passes
- converge only when two consecutive passes find no new risks
- evaluate precedence, protected zones, security implications, task group, determinism, shadow patterns, and mutation necessity
- output only risks, citations, and a safety verdict

---

## Rule A13 — Mode Transition Invariants

Refer to `src/canon/rule-schema-v2.governance.yaml` for structured definition.

The following invariants are binding:

- Deep Governance Mode MUST NOT transition directly to Execution Mode.
- Spec Mode MUST NOT perform execution.
- Execution Mode MUST NOT start without an approved tasks.md.
- Any ambiguity in transition legality requires HITL.
