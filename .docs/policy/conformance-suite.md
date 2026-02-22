# Governance Conformance Suite

This document defines what the conformance suite checks.

Non-canonical unless elevated by mutation.

---

## What It Verifies

- Canon files exist
- HITL marker exists where required
- Governance state machine docs exist
- State schema YAML is valid
- Structured rules YAML is valid
- Forbidden transitions are explicitly declared
- Deep Mode max_passes and convergence rules are present

---

## What It Does Not Verify

- Semantic correctness of every rule
- Security model completeness
- Project-specific architecture

This suite is structural.

---

## Conformance Output

- PASS: governance structure is consistent
- FAIL: missing files, invalid schemas, or missing invariants

Failing conformance should block execution in CI when enabled.
