# INVARIANT MODEL

Invariants are core truths and constraints that MUST be preserved through every change. They are the "immutability layer" of the project's identity.

## 1. System Invariants
These rules apply to the entire system:

```yaml sagrule
id: INV-RULE-OF-LAW
statement: "No code change can bypass ARCHITECTURE_RULES.md."
operator: MUST_NOT
context: all
severity: CRITICAL
enforcement: REFUSAL
source: "docs/INVARIANT_MODEL.md §1"
```

- **Rule of Law**: No code change can bypass `ARCHITECTURE_RULES.md`.

```yaml sagrule
id: INV-ZERO-HALLUCINATION
statement: "Every implementation detail must be traceable to a specification."
operator: MUST
context: development
severity: CRITICAL
enforcement: REFUSAL
source: "docs/INVARIANT_MODEL.md §1"
```

- **Zero Hallucination**: Every implementation detail must be traceable to a specification.

```yaml sagrule
id: INV-TRACEABILITY
statement: "Every system mutation must be recorded in .jtasks/."
operator: MUST
context: all
severity: CRITICAL
enforcement: REFUSAL
source: "docs/INVARIANT_MODEL.md §1"
```

- **Traceability**: Every system mutation must be recorded in `.jtasks/`.

## 2. Domain Invariants
(Placeholders to be filled by the specific project)
- [Example: All token transactions must be ACID compliant.]
- [Example: Public surfaces must be SEO-first and indexable.]

## 3. Enforcement
Invariants are enforced via:
1. **Audit-Governance Skill**: Automated checking of code against invariants.
2. **Test-Enforcer Skill**: Property-based testing of state transitions.

```yaml sagrule
id: INV-ENFORCEMENT-REFUSAL
statement: "The agent MUST refuse any request that breaks a system invariant."
operator: MUST
context: all
severity: CRITICAL
enforcement: REFUSAL
source: "docs/INVARIANT_MODEL.md §3"
```

3. **Agent Refusal**: The agent must refuse any request that breaks an invariant.
