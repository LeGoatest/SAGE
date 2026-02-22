# State Validator

This document defines how a future Canon Compiler validates governance state integrity.

This file is explanatory unless explicitly referenced by canon.

---

## Validation Goals

The compiler must ensure:

1. No cycles without explicit terminal states.
2. No forbidden transitions allowed.
3. All states referenced in canon exist in state-schema-v2.yaml.
4. All states have deterministic exit conditions.
5. All transitions are explicit and unambiguous.

---

## Determinism Requirements

- Every state must define allowed outputs.
- Every state must define forbidden outputs.
- Deep state must enforce max_passes <= 3.
- No state may have implicit transitions.

---

## Conflict Detection

Compiler must fail if:

- Canon rules contradict schema transitions.
- Enforcement matrix allows forbidden transition.
- State definitions differ between canon prose and YAML schema.

On failure:
- Emit BLOCK
- Require mutation workflow

---

## Future Integration

This validator may eventually:

- Parse rule-schema-v2.yaml
- Validate state-schema-v2.yaml
- Cross-check enforcement matrix
- Produce conflict reports