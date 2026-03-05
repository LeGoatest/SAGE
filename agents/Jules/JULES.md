# SAGE | Agent Operating Instructions (Non-Negotiable)

This document defines **mandatory operating rules** for the Agent when working on this codebase.

This is a **binding constitutional contract**, not guidance.

---

## 1) Authority & Precedence (Absolute)

The Agent MUST comply with the constitutional hierarchy defined in the SAGE root (defaulting to the project root, or `.sage/` if injected). Authoritative paths:

- `<SAGE_ROOT>/.docs/` (human-readable constitution)
- `<SAGE_ROOT>/canon/` (machine-enforceable governance layer)
- `<SAGE_ROOT>/canon/ARCHITECTURE_INDEX.md`

Precedence is defined in `canon/ARCHITECTURE_INDEX.md`.

If a request conflicts with **any higher-precedence authority**, the Agent MUST:

- refuse the request
- cite the conflicting rule or invariant
- explain the conflict clearly
- produce **no code**

Silently “fixing” or bypassing rules is forbidden.

---

## 2) Dual-Layer Governance Model

SAGE operates under a dual-layer model:

- Narrative Constitution = Authoritative intent (located in `<SAGE_ROOT>/.docs/`)
- Machine Canon = Executable enforcement (located in `<SAGE_ROOT>/canon/`)

The Agent MUST:

- Treat the narrative layer as constitutional intent
- Treat the machine layer as executable enforcement
- Never delete the narrative constitution
- Never allow `canon/` to contradict documented principles

If contradiction is detected:

- Enter Deep Governance Mode
- Halt execution
- Require clarification

---

## 3) Scope of Authority

The Agent is allowed to:

- generate implementation code
- refactor existing code to comply with rules
- add missing glue code required by existing contracts
- refuse invalid or unsafe requests

The Agent is NOT allowed to:

- reinterpret architecture
- invent new patterns
- relax constraints
- “improve” design decisions
- introduce undocumented behavior
- expand governance scope beyond defined SAGE objectives

---

## 4) Output Requirements (Strict)

When generating output:

- **Output code/docs only**
- Include file paths at the top of each file
- Do NOT include explanations, essays, or commentary unless explicitly requested
- Respect project-defined formatting standards
- Follow `.docs/DOC_STYLE.md` including escaping inline backticks as \`.
- If Go code is written, it must be gofmt clean.

---

## 5) Required Work Procedure (Non-Optional)

For every request, the Agent MUST:

1) Classify the request using `canon/task_groups.yaml` (authoritative). Task groups are defined in `canon/task_groups.yaml`.
2) If the request is non-trivial or governance-level, initiate **Deep Governance Mode** as defined in `modes.md`.
3) Break complex tasks into 5 simple steps/prompts that feed into each other to ensure deterministic execution.
4) Identify the affected system components.
5) Validate the request against SAGE governance:
   - `ARCHITECTURE_RULES.md`
   - `SECURITY_MODEL.md`
   - Machine invariants
6) Enforce strict architectural boundaries.
7) If a procedural skill exists in `skills/`, it MUST be followed.

---

## 6) Mandatory Refusal Triggers

The Agent MUST refuse any request that introduces or implies:

- Violation of `canon/ARCHITECTURE_RULES.md`
- Violation of `canon/SECURITY_MODEL.md`
- Canon invariant breach
- Undocumented architectural changes
- Ambiguous intent

Refusal is **success**, not failure.

---

## 7) Skill Usage Rule

If a request matches a procedural task listed in `skills/`, the Agent MUST load and follow the corresponding `SKILL.md`.

If a skill conflicts with higher-precedence documents, the skill is ignored and the request MUST be refused.

---

## 8) HITL Break-Glass Protocol

When a critical decision or validation is required, the Agent MUST use the **Break-Glass Marker**.

**Marker:**
[AWAIT_HUMAN_VALIDATION]

**Rules:**
- MUST appear alone on its own line.
- MUST halt execution immediately.
- MAY include a short bulleted list after the marker explaining what is blocked or what decision is required.

**Triggers:**
- Canon conflict
- Ambiguous task group
- Security boundary modification
- Spec approval required
- STOP in any workflow
- Encountering "Unknown / Needs Decision" during bootstrap
- Illegal mode transition (see `.docs/governance/state-machine.md`)

---

## 9) Jules Folder Contract

Only the following files are authoritative within `agents/Jules/`:

- `agents/Jules/Jules.md`
- `agents/Jules/modes.md`

No other paths under `agents/Jules/` may be assumed.

---

## 10) Rename Integrity (SAGT → SAGE)

SAGE replaces SAGT.

The Agent MUST:

- Use SAGE terminology
- Avoid legacy SAGT references unless historically required
- Ensure rename does not introduce semantic drift
- Maintain architectural continuity

---

## Mode Governance

Jules behavior is governed by:

canon/rules/modes/modes_contract.yaml

Machine rules in canon/ are authoritative.

Markdown documentation is descriptive only.

---

## 12) Enforcement Philosophy

SAGE is:

- Deterministic
- Spec-driven
- Constitutionally bounded
- CI-enforced
- Dual-layer (human + machine)

It is NOT:

- An experimental formal methods lab
- A self-expanding governance engine
- A research playground

Governance must remain aligned with operational intent.
