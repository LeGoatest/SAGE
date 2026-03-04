# AGENTS.md — SAGE Agent Onboarding (Non-Canonical)

This file is an onboarding guide for AI agents operating in this repository.

**Non-canonical notice:**
This document is not authoritative unless `canon/` explicitly references it.
If any conflict exists, `canon/` prevails.

---

## What SAGE Is

SAGE (Sovereign Agent Governance Engine) provides a constitutional governance model for AI-assisted development.

- `.docs/` is the human-readable constitution (must not be deleted).
- `canon/` is the machine-enforceable governance layer.

---

## Repo-as-Trigger Setup (External Canon Model)

When operating on a Target Repository, governance is resolved **only** via `governance.yaml` in the Target Repository root:

```yaml
sage:
  repo: <SAGE_REPO_URL>
  ref: <commit-sha>
  mode: strict
```

Rules:
- `ref` MUST be a commit SHA (no branches).
- Missing/invalid `governance.yaml` → hard fail.
- Prompts MUST NOT override canon resolution.

---

## Canon Entrypoint

After resolving the pinned SAGE ref, the agent MUST load and follow the canonical entrypoint:

`canon/bootstrap.md`

This entrypoint defines the required bootstrap and validation flow.

---

## Required Workflow

Unless explicitly instructed otherwise by canon:

1. **ENTER_DEEP_GOVERNANCE_MODE**
   Validate authority, scope, and invariants.

2. **Classify the request into exactly one task group**
   Task groups are defined in `canon/task_groups.yaml` (authoritative).

3. **ENTER_SPEC_MODE** (required for non-trivial work)
   Produce spec artifacts (requirements/design/tasks).

4. **ENTER_EXEC_MODE**
   Implement exactly what `tasks.md` specifies.

If blocked or ambiguous, emit:
[AWAIT_HUMAN_VALIDATION]
and stop.

---

## Skills

Operational skills live in:
`skills/`

Skills are optional helpers, not governance.
If a skill conflicts with canon, the agent must refuse.

---

## Absolute Prohibitions

The agent MUST NOT:
- Delete `.docs/`
- Create/modify canonical documents in a Target Repository under External Canon Model
- Invent trust boundaries, threat models, or security properties without evidence
- Mutate `canon/` unless explicitly authorized and HITL approved
- Execute implementation without task group classification (and Spec Mode for non-trivial work)

---

## Jules-Specific Notes

Jules behavior conventions may be defined in:
- `agents/Jules/Jules.md`
- `agents/Jules/modes.md`

These are guidance documents unless canon references them.
