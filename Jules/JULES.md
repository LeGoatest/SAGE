# Project Name | Agent Operating Instructions (Non-Negotiable)

This document defines **mandatory operating rules** for the Agent when working on this codebase.

This is a **binding contract**, not guidance.

---

## 1) Authority & Precedence (Absolute)

You MUST comply with the documents in the order defined in `src/canon/ARCHITECTURE_INDEX.md`.

If a request conflicts with **any higher-precedence document**, you MUST:
- refuse the request
- cite the conflicting rule
- explain the conflict clearly
- produce **no code**

Silently “fixing” or bypassing rules is forbidden.

---

## 2) Scope of Authority

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

---

## 3) Output Requirements (Strict)

When generating output:
- **Output code/docs only**
- Include file paths at the top of each file
- Do NOT include explanations, essays, or commentary unless explicitly requested
- Respect project-defined formatting standards
- Follow `src/DOC_STYLE.md` including escaping inline backticks as \`.
- If Go code is written, it must be gofmt clean.

---

## 4) Required Work Procedure (Non-Optional)

For every request, the Agent MUST:
1) Classify the request using `Jules/TASK_GROUPS.md`.
2) If the request is non-trivial or governance-level, initiate **Deep Governance Mode** using `ENTER_DEEP_GOVERNANCE_MODE`.
3) Break complex tasks into 5 simple steps/prompts that feed into each other to ensure deterministic execution.
4) Identify the affected system components.
5) Validate the request against `src/canon/ARCHITECTURE_RULES.md` and `src/canon/SECURITY_MODEL.md`.
6) Enforce strict architectural boundaries.
7) If a procedural skill exists in `skills/`, it MUST be followed.

---

## 5) Mandatory Refusal Triggers

The Agent MUST refuse any request that introduces or implies:
- Violation of `src/canon/ARCHITECTURE_RULES.md`
- Violation of `src/canon/SECURITY_MODEL.md`
- Undocumented architectural changes
- Ambiguous intent

Refusal is **success**, not failure.

---

## 6) Skill Usage Rule

If a request matches a procedural task listed in `Jules/SKILLS_INDEX.md`, the Agent MUST load and follow the corresponding `SKILL.md`.
If a skill conflicts with higher-precedence documents, the skill is ignored and the request MUST be refused.

---

## 7) HITL Break-Glass Protocol

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
- Illegal mode transition (see `src/governance/state-machine.md`)
