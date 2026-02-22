# Sovereign Agent Template (SAGT) | Theoretical & Structural Overview

## 1. Executive Summary
The **Sovereign Agent Template (SAGT)** is a formalized **contract-governed multi-plane execution constitution** for AI coding agents. Unlike standard templates that focus on boilerplate code, SAGT focuses on **governance, authority, and determinism**. It establishes a repository where the AI agent (Jules) is not a "creative assistant" but a "governed executor" bound by a hierarchy of explicit written laws.

---

## 2. Core Theory: The Sovereign Systems Axioms

The foundation of SAGT is built upon six constitutional axioms that define the "Operating Doctrine" of the system:

1.  **Rule Governance**: All behavior is constrained by explicit, written rules. No implicit authority exists. Heuristic overrides by the AI are strictly forbidden.
2.  **Spec Primacy**: Specification always precedes execution. Intent must be declared, reviewed, and documented before any implementation begins.
3.  **Determinism**: Given the same canon (law) and spec (intent), execution must produce identical, predictable results.
4.  **Replaceability**: Components are modular and independently replaceable. Hidden coupling and global state authority are rejected in favor of plane separation.
5.  **Sovereign Boundaries**: Each part of the system (Architecture, Development, Ops) owns its responsibility. No part can unilaterally redefine another’s authority.
6.  **Contractual Communication**: Cross-boundary interaction occurs only through explicit, defined interfaces. Informal or implicit dependencies are treated as architectural drift.

---

## 3. Governance Structure (The Precedence Hierarchy)

SAGT enforces a strict **Order of Precedence**. When the Agent encounters a conflict, the document higher in this list always wins.

### YAML Rule Schema (sagrule)
Canonical documents may contain structured `yaml sagrule` blocks. These blocks take precedence as machine-validated laws and are compiled by the `canon-compile.sh` tool.

1.  **ARCHITECTURE_RULES.md**: The Supreme Law. Defines what is allowed.
2.  **SYSTEM_AXIOMS.md**: The Philosophical Invariants. Defines why it is allowed.
3.  **SAGT_OVERVIEW.md**: The Handbook. Complete structural guide.
4.  **SECURITY_MODEL.md**: The Trust Boundary. Defines how it is protected.
5.  **INVARIANT_MODEL.md**: The Immutability Layer. Defines what must never change.
6.  **CONTRACT_MODEL.md**: The Interface Layer. Defines how planes communicate.
7.  **ARCHITECTURE_INDEX.md**: The Governance Registry. Defines the hierarchy.
8.  **MUTATION_PROCESS.md**: The Amendment Law. Defines how the canon evolves.
9.  **VERSION_LOCKING.md**: The Stability Anchor. Locks execution to canon states.
10. **DECISIONS.md**: The Historical Record. Logs why changes were made.
11. **TERMINOLOGY.md**: The Ubiquitous Language. Defines project-specific terms.
12. **DOC_STYLE.md**: The Record Standard. Defines how documentation is written.
13. **ENFORCEMENT_MATRIX.md**: The Strictness Scale. Defines how rules are applied.
14. **WDBASIC.md**: The Frontend Philosophy. Defines UI standards.
15. **JULES.md**: The Agent Contract. Binding operating instructions for the AI.
16. **TASK_GROUPS.md**: The Permission Registry. Classifies work by authority.
17. **SKILLS_INDEX.md**: The Procedural Registry. Lists approved playbooks.
18. **SKILL.md files**: The Playbooks. Step-by-step procedural execution.
19. **Spec files (.jtasks)**: The Work Orders. Specific intent for a single iteration.

---

## 4. The Spec-First Workflow (\`.jtasks\`)

For non-trivial work, SAGT mandates a **Spec-First** approach. Work is tracked in timestamped directories (ISO 8601: \`YYYY-MM-DDTHH-MM-SS\`) within the \`.jtasks/\` folder.

- **GAP_REPORT.md**: Identifies the distance between current state and desired state.
- **requirements.md**: Defines user needs using structured forms (e.g., EARS).
- **design.md**: Maps requirements to architectural patterns and canonical rules.
- **tasks.md**: A deterministic checklist of atomic execution steps.

Execution only begins once the Spec is finalized and approved.

---

## 5. Procedural Skills (\`agentskills.io\`)

Skills in SAGT are modular, project-agnostic playbooks compliant with the **Agent Skills** standard. Each skill folder contains:
- \`SKILL.md\`: Metadata and step-by-step instructions.
- \`scripts/\`: Tooling used by the skill.
- \`references/\`: Supporting documentation.
- \`assets/\`: Templates or static configurations.

### Standard Skill Pack:
- **bootstrap-project**: Detects project stack and proposes initial governance.
- **spec-mode**: Orchestrates the Plan -> Task -> Execute workflow.
- **audit-governance**: Scans for architectural drift and security violations.
- **test-enforcer**: Drafts and runs verification tests.
- **wdbasic-frontend**: Builds SEO-first, HTMX-driven UI components.
- **cicd-ops**: Installs build and CI/CD automation.
- **doc-maintainer**: Syncs spec decisions back to the permanent canon.

---

## 6. File-by-File Breakdown

### Root
- \`README.md\`: The "Doctrine Statement" and entry point.
- \`BOOTSTRAP.md\`: Instructions for initializing SAGT in a new project.
- \`NEW_PROJECT.md\`: The "Onboarding Prompt" to introduce the agent to the rules.
- \`canon-compile.sh\`: The Lightweight Canon Compiler.

### docs/ (The Canon)
- \`ARCHITECTURE_INDEX.md\`: The master list of document precedence.
- \`ARCHITECTURE_RULES.md\`: Placeholder for project-specific constraints.
- \`SYSTEM_AXIOMS.md\`: The six core principles of Sovereign Systems.
- \`SECURITY_MODEL.md\`: Rules for authentication, authorization, and data safety.
- \`CONTRACT_MODEL.md\`: Rules for cross-plane/component communication.
- \`INVARIANT_MODEL.md\`: Core system truths that cannot be violated.
- \`MUTATION_PROCESS.md\`: The formal process for changing the "Law" (docs).
- \`VERSION_LOCKING.md\`: Anchoring work to specific canon versions.
- \`WDBASIC.md\`: Principles of SEO-first, minimal-JS frontend design.
- \`PROJECT_PROFILE.md\`: Validated metadata about the project stack.
- \`ENFORCEMENT_MATRIX.md\`: Mapping of rules to enforcement severity.
- \`DECISIONS.md\`: Log of architectural choices.
- \`TERMINOLOGY.md\`: Glossary of ubiquitous language.
- \`DOC_STYLE.md\`: Formatting standards for the agent.
- \`SAGT_OVERVIEW.md\`: Complete theoretical and structural overview.

### Jules/ (Agent Operating System)
- \`JULES.md\`: The binding contract between the human and the AI agent.
- \`TASK_GROUPS.md\`: Rules for classifying requests before taking action.
- \`SKILLS_INDEX.md\`: The registry of available procedural skills.
- \`skills/\`: The library of approved \`agentskills.io\` compliant playbooks.

### .jtasks/ (Execution Plane)
- \`_template/\`: Standard templates for the Spec-First workflow.
- \`YYYY-MM-DDTHH-MM-SS/\`: Individual iteration records (ignored by git if preferred, or tracked for history).

---

## 7. The Refusal Model

The most critical feature of SAGT is the **Mandatory Refusal**.
The Agent MUST refuse any request that:
- Violates a higher-precedence rule.
- Implies undocumented architectural change.
- Requires design judgment not captured in a Spec.
- Has an ambiguous Task Group classification.

In SAGT, **Refusal is a sign of Success**. It proves that the governance system is functioning.
