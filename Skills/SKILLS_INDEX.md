# Project Name | Agent Skills Registry

This document defines the **procedural skill system**.
Skills are approved playbooks for repeatable tasks.

---

## 1) Authority Model

All skills are subordinate to canonical documents.
If a skill conflicts with any document in `src/`, the skill is ignored.

---

## 2) Standard Structure (Compliance: agentskills.io)

This repository follows the **Agent Skills** specification for modular procedural knowledge. Each skill folder MUST contain:

- `SKILL.md`: Mandatory instructions and metadata.
- `scripts/`: (Optional) Executable scripts or tools used by the skill.
- `references/`: (Optional) Deep-dive documentation or lookup data.
- `assets/`: (Optional) Static files, templates, or schemas.

---

## 3) Available Skills

### spec-mode/SKILL.md
**Use when:**
- building a non-trivial feature
- work spans multiple files
- a plan → task list → execution workflow is needed

**Task group:** docs

**Reads first:**
- JULES.md
- TASK_GROUPS.md

### nsad/SKILL.md
**Use when:**
- evaluating or designing system boundaries
- optimizing data layout, cache alignment, or network packet sizing
- ensuring natural units pack natively into the next stage's grain

**Task group:** development

**Reads first:**
- ARCHITECTURE_RULES.md
- INVARIANT_MODEL.md

### wdbasic-frontend/SKILL.md
**Use when:**
- building or modifying frontend components
- implementing HTMX interactivity
- designing marketing or product surfaces

**Task group:** development

**Reads first:**
- WDBASIC.md
- ARCHITECTURE_RULES.md

### audit-governance/SKILL.md
**Use when:**
- performing a security or architectural review
- checking for drift between code and docs
- verifying task compliance before submission

**Task group:** audit

**Reads first:**
- ARCHITECTURE_RULES.md
- SECURITY_MODEL.md

### constitutional-check/SKILL.md
**Use when:**
- scanning for logical contradictions in canon before generating tasks
- performing a governance integrity pass

**Task group:** audit

**Reads first:**
- ARCHITECTURE_INDEX.md

### test-enforcer/SKILL.md
**Use when:**
- implementing new features
- fixing bugs
- verifying system invariants

**Task group:** development

**Reads first:**
- ARCHITECTURE_RULES.md
- PROJECT_PROFILE.md

### doc-maintainer/SKILL.md
**Use when:**
- a spec in `.jtasks/` is completed and finalized
- terminology needs to be synchronized
- a permanent decision record is required

**Task group:** docs

**Reads first:**
- DECISIONS.md
- TERMINOLOGY.md

### cicd-ops/SKILL.md
**Use when:**
- setting up or modifying CI/CD pipelines
- adding linting or formatting automation
- configuring build systems (Makefiles)

**Task group:** operations

**Reads first:**
- PROJECT_PROFILE.md

### tailwindcss-cli/SKILL.md
**Use when:**
- setting up or modifying TailwindCSS build pipeline
- configuring CSS output to assets/css/style.css
- installing TailwindCSS v4 CLI

**Task group:** operations

**Reads first:**
- PROJECT_PROFILE.md

### context-pruning/SKILL.md
**Use when:**
- producing a non-canonical src/MINI_CANON.md to reduce token bloat
- conversation context is large and needs optimization

**Task group:** operations

**Reads first:**
- ARCHITECTURE_INDEX.md
- JULES.md

### bootstrap-project/SKILL.md
**Use when:**
- Jules is first introduced to a repository
- governance/canon files are missing or incomplete
- the user requests “bootstrap”, “initialize”, or “set up rules/governance”

**Task group:** docs

**Reads first:**
- JULES.md
- TASK_GROUPS.md
