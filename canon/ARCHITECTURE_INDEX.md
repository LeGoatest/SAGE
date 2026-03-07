# SAGE | Architectural Index (Precedence & Governance)

This document defines the **canonical order of precedence** for all documentation in this project.
It is the secondary authority for resolving conflicts, as defined in `agents/Jules/JULES.md`.

---

## 1. Functional Governance Zones

The system is organized into functional zones:

- `.docs/`: Human-readable narrative constitution.
- `canon/`: Machine-enforceable governance layer.
- `agents/Jules/`: Agent operating instructions and modes.
- `skills/`: Procedural execution playbooks.
- `.jtasks/`: Deterministic planning and execution records.

---

## 2. Absolute Precedence List

In the event of a conflict between documents, the document appearing **higher in this list** always wins. Agents MUST refuse any request that violates a higher-precedence rule.

### I. Semantic Layer (Axioms & Invariants)
1. `canon/semantic/axioms.yaml`
2. `canon/semantic/invariants.yaml`
3. `canon/rules/bootstrap/bootstrap_invariant.yaml`
4. `canon/rules/task_groups/task_group_invariant.yaml`
5. `canon/rules/modes/deep_governance_context_invariant.yaml`

### II. Supreme Canon (Machine-Enforceable)
6. `canon/ARCHITECTURE_RULES.md`
7. `canon/SECURITY_MODEL.md`
8. `canon/rules/` (All YAML rules)

### III. Human Constitution (Narrative)
9. `.docs/canon/ARCHITECTURE_RULES.md`
10. `.docs/canon/SYSTEM_AXIOMS.md`
11. `.docs/canon/SECURITY_MODEL.md`
12. `.docs/canon/INVARIANT_MODEL.md`
13. `.docs/canon/CONTRACT_MODEL.md`
14. `canon/ARCHITECTURE_INDEX.md`
15. `.docs/canon/MUTATION_PROCESS.md`
16. `.docs/canon/VERSION_LOCKING.md`
17. `.docs/canon/DECISIONS.md`
18. `.docs/canon/TERMINOLOGY.md`
19. `.docs/canon/DOC_STYLE.md`
20. `.docs/canon/ENFORCEMENT_MATRIX.md`
21. `.docs/canon/WDBASIC.md`
22. `.docs/DEEP_GOVERNANCE_CONTEXT.md`

### IV. Agent Operating Instructions
23. `.docs/AGENT_OPERATING_INSTRUCTIONS.md`
24. `agents/Jules/JULES.md`
25. `agents/Jules/modes.md`
26. `canon/task_groups.yaml`

### V. Procedural Skills & Work Orders
27. `skills/` (SKILL.md files)
28. `.jtasks/` (Spec files)

---

## 3. Non-Canonical Convenience Files

The following files are provided for token efficiency or quick reference. They carry NO canonical authority and are subordinate to all documents listed above.

- `AGENTS.md`
- `.docs/reference/MINI_CANON.md`
- `.docs/reference/SAGE_OVERVIEW.md`
- `.docs/BOOTSTRAP_EXTERNAL_CANON_MODEL.md`
- `.docs/NEW_PROJECT_PROMPT.md`

---

## 4. Summary

If a rule in a lower-precedence document contradicts a higher one, the lower rule is **void**.
The Agent MUST refuse any request that violates this hierarchy.
The agent must STOP if design judgment is required but not specified in canon.
