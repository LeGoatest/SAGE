# SAGE | Agent Task Group Classification

This document defines **task groups** used by the Agent to classify user requests **before** selecting skills or executing work.

Task classification is mandatory and must occur before any mode activation or implementation.

Canon prevails over this document.

---

## 1) Classification Procedure (Non-Optional)

For every request, the Agent MUST:

1. Classify the request into **exactly one** task group.
2. If classification is ambiguous → emit:

   [AWAIT_HUMAN_VALIDATION]

3. Determine whether the selected task group allows skills.
4. If skills are allowed:
   - Consult `skills/`
   - Activate a matching `SKILL.md` if applicable.
5. If skills are not allowed:
   - Rely exclusively on `.docs/` and `canon/`
6. Activate the appropriate mode (Deep / Spec / Exec) if required.

The Agent MUST NOT:
- Skip classification
- Use multiple task groups simultaneously
- Silently reclassify mid-task
- Execute before classification

---

## 2) Defined Task Groups

### 2.1 architecture

Use when the request involves:

- Changing system structure
- Redefining invariants
- Altering authority or trust boundaries
- Modifying canon
- Introducing new architectural patterns
- Changing governance flow

Skills Allowed: NO
Mode: Deep Governance Mode required

Behavior:
- Rely exclusively on `.docs/` and `canon/`
- Validate against invariants
- Refuse if rules are violated
- Require explicit human approval before mutation

---

### 2.2 development

Use when the request involves:

- Implementing features within existing architecture
- Fixing bugs
- Refactoring for compliance
- Adding tests
- Writing glue code

Skills Allowed: YES
Mode: Spec → Exec

Behavior:
- Must not alter architecture
- Must not mutate canon
- Must remain within declared scope

---

### 2.3 operations

Use when the request involves:

- Build systems
- CI/CD configuration
- Deployment configuration
- Environment setup
- Dependency management
- Toolchain updates

Skills Allowed: YES
Mode: Spec → Exec (if non-trivial)

Behavior:
- Must not alter governance or invariants
- Must respect protected zones

---

### 2.4 docs

Use when the request involves:

- Writing or updating documentation
- Clarifying behavior
- Producing requirements/design/tasks
- Procedural planning
- Spec Mode outputs

Skills Allowed: YES
Mode: Spec Mode

Behavior:
- Must not change canon meaning
- Must preserve constitutional intent
- Documentation must not contradict canon

---

### 2.5 audit

Use when the request involves:

- Checking architectural compliance
- Scanning for security violations
- Detecting governance drift
- Verifying invariants
- Rename integrity checks
- Structural consistency review

Skills Allowed: YES
Mode: Deep Governance Mode

Behavior:
- No implementation output
- Produce structured findings
- Cite canonical references
- Provide verdict

---

## 3) Escalation Rules

If during execution the task scope expands into another group:

- STOP
- Emit:

[AWAIT_HUMAN_VALIDATION]

- Explain required reclassification

No implicit cross-group escalation is allowed.

---

## 4) Determinism Requirement

Task groups exist to:

- Prevent architectural drift
- Prevent skill misuse
- Prevent scope creep
- Ensure reproducible behavior across sessions

Classification discipline is mandatory.
