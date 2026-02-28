# Sovereign Agent | Architectural Index (Precedence & Governance)

This document defines the **canonical order of precedence** for all documentation in this project.
It is the secondary authority for resolving conflicts, as defined in `Jules/JULES.md`.

---

## 1. Functional Governance Zones

The system is organized into six functional zones within the `.docs/` directory:

- `.docs/canon/`: Supreme Laws, Rules, and Invariants.
- `.docs/governance/`: State Machine and Mode protocols.
- `.docs/policy/`: Telemetry, thresholds, and conformance.
- `.docs/reference/`: Supporting guides and handbooks.
- `.docs/jules/`: Agent mode instructions.
- `.docs/compiler/`: Validation schemas and specifications.

---

## 2. Absolute Precedence List

In the event of a conflict between documents, the document appearing **higher in this list** always wins. Agents MUST refuse any request that violates a higher-precedence rule.

### I. Supreme Canon (Zone: canon)
1. [.docs/canon/ARCHITECTURE_RULES.md](./ARCHITECTURE_RULES.md)
2. [.docs/canon/SYSTEM_AXIOMS.md](./SYSTEM_AXIOMS.md)
3. [.docs/canon/SECURITY_MODEL.md](./SECURITY_MODEL.md)
4. [.docs/canon/INVARIANT_MODEL.md](./INVARIANT_MODEL.md)
5. [.docs/canon/CONTRACT_MODEL.md](./CONTRACT_MODEL.md)
6. [.docs/canon/ARCHITECTURE_INDEX.md](./ARCHITECTURE_INDEX.md)
7. [.docs/canon/MUTATION_PROCESS.md](./MUTATION_PROCESS.md)
8. [.docs/canon/VERSION_LOCKING.md](./VERSION_LOCKING.md)
9. [.docs/canon/DECISIONS.md](./DECISIONS.md)
10. [.docs/canon/TERMINOLOGY.md](./TERMINOLOGY.md)
11. [.docs/canon/DOC_STYLE.md](./DOC_STYLE.md)
12. [.docs/canon/ENFORCEMENT_MATRIX.md](./ENFORCEMENT_MATRIX.md)
13. [.docs/canon/WDBASIC.md](./WDBASIC.md)

### II. State & Mode Governance (Zone: governance)
14. [.docs/governance/state-machine.md](../governance/state-machine.md)
15. [.docs/governance/deep-governance-mode.md](../governance/deep-governance-mode.md)

### III. Agent Operating Instructions (Zone: Jules/)
16. [Jules/JULES.md](../../Jules/JULES.md)
17. [Jules/TASK_GROUPS.md](../../Jules/TASK_GROUPS.md)
18. [Jules/SKILLS_INDEX.md](../../Jules/SKILLS_INDEX.md)

### IV. Procedural Skills & Work Orders
19. [SKILL.md files](../../skills/)
20. [Spec files (in .jtasks)](../../.jtasks/)

---

## 3. Non-Canonical Convenience Files

The following files are provided for token efficiency or quick reference. They carry NO canonical authority and are subordinate to all documents listed above.

- [.docs/reference/MINI_CANON.md](../reference/MINI_CANON.md)
- [.docs/reference/SAGE_OVERVIEW.md](../reference/SAGE_OVERVIEW.md)

---

## 4. YAML Rule Schema (sagrule)

Canonical rules may be expressed in structured `yaml sagrule` blocks within these documents. These rules are machine-validated and take precedence as the most precise expression of the project's law. The `tools/run-conformance.sh` tool MUST be used to verify the consistency of these rules.

---

## 5. Summary

If a rule in a lower-precedence document contradicts a higher one, the lower rule is **void**.
The Agent MUST refuse any request that violates this hierarchy.
The agent must STOP if design judgment is required but not specified in canon.
