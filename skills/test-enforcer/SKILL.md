---
name: test-enforcer
description: Procedure for drafting, implementing, and verifying tests to ensure code correctness and prevent regressions.
metadata:
  category: quality
  authority: procedural
  requires:
    - ARCHITECTURE_RULES.md
---

# Skill: test-enforcer

## Authority Boundary
This skill is **procedural only**.
Tests must verify architecture, not redefine it.
The agent must never "fake" or skip tests to meet a deadline.

## Procedure

### Step 1: Identify Testable Surfaces
Based on the task or changed files, identify:
- **Unit Tests**: Logic within a single function or domain entity.
- **Integration Tests**: Interaction between two layers (e.g., App -> Infra).
- **Property-based Tests**: Invariants that must hold true for all inputs.
- **Contract Tests**: Verification of API or SSE payloads.

### Step 2: Define Test Cases (Drafting)
Before writing code, list the scenarios:
- **Happy Path**: Expected valid behavior.
- **Edge Cases**: Empty inputs, maximum values, boundary conditions.
- **Error Paths**: Unauthenticated access, database failures, invalid states.

### Step 3: Implementation
1. Use the project's standard testing framework (detected in `PROJECT_PROFILE.md`).
2. Implement the drafted test cases.
3. Ensure tests are isolated and don't rely on global state.

### Step 4: Verification & Iteration
1. Run the tests.
2. If tests fail:
   - Determine if the **Code** is wrong (Bug).
   - Determine if the **Test** is wrong (Logic error).
   - Determine if the **Requirement** is ambiguous (STOP and ask).
3. Repeat until all relevant tests pass.

### Step 5: Coverage Check
Verify that the most critical paths (defined in `ARCHITECTURE_RULES.md` or `SECURITY_MODEL.md`) are covered. Do not settle for "Line Coverage" if "Path Coverage" of sensitive logic is missing.

## Guidelines
- Follow the "Test-Driven Development" (TDD) cycle whenever possible.
- Mock external dependencies (APIs, Databases) to keep tests fast and deterministic.
- In property-based testing, focus on "Monotonicity" and "Idempotency" of state changes.
