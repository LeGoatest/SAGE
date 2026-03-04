# Project Name | Agent Skills Registry

This document defines the **procedural skill system**.
Skills are approved playbooks for repeatable tasks.

---

## 1) Authority Model

All skills are subordinate to canonical documents.
If a skill conflicts with any document in `canon/` (machine) or `.docs/canon/` (human), the skill is ignored.

---

## 2) Standard Structure (Compliance: agentskills.io)

This repository follows the **Agent Skills** specification for modular procedural knowledge. Each skill folder MUST contain:

- `SKILL.md`: Mandatory instructions and metadata.
- `scripts/`: (Optional) Executable scripts or tools used by the skill.
- `references/`: (Optional) Supporting docs, tables, checklists.
- `assets/`: (Optional) Icons, images, example files.

---

## 3) Skill Registry

### ✅ Core Skills (Registered)

- `spec-mode`
- `audit-governance`
- `bootstrap-project`
- `constitutional-check`
- `context-pruning`
- `doc-maintainer`
- `test-enforcer`
- `cicd-ops`
- `nsad`
- `tailwindcss-cli`
- `wdbasic-frontend`

---

## 4) Skill Rules

1. **Skills cannot override canon.**
2. **Skills cannot introduce new governance.**
3. **Skills must be deterministic.**
4. **Skills must be scoped.**
5. **Skills must be safe-by-default.**

---

## 5) Anti-patterns (Forbidden)

- Using skills to bypass canonical enforcement
- Introducing “shadow governance” rules not present in canon
- Generating instructions that include secrets, credentials, or destructive ops
- Producing a non-canonical .docs/reference/MINI_CANON.md to reduce token bloat
