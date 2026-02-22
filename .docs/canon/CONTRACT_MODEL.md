# CONTRACT MODEL

This document defines how different system planes and components interact. All communication MUST follow these formal contract rules to ensure sovereignty and replaceability.

## 1. Explicit Interfaces
Cross-boundary communication occurs only through explicit, documented interfaces (APIs, Events, or Shared Data Schemas). Implicit dependencies (e.g., direct database access across planes) are forbidden.

## 2. Plane Isolation
The system is divided into logical planes (e.g., Domain, Infrastructure, Port).
- A plane owns its internal state.
- No plane can directly mutate the state of another plane.
- Interactions are requested via the contract; the owning plane decides how to fulfill it.

## 3. Contract Enforcement
- **Verification**: Contracts must be verifiable via automated tests or schema validation.
- **Stability**: Breaking changes to a contract require a formal Decision Record and a Spec-led migration.

## 4. Discovery
Components should discover each other via registry or configuration, never through hardcoded global state.
