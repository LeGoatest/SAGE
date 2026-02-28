# FIX PLAN

1. **Add Spec Artifact Rules**: Implement rules mandating the presence of `requirements.md`, `design.md`, and `tasks.md` in any non-trivial task folder.
2. **Add Structure Rules**: Implement rules enforcing specific mandatory sections (Failure Modeling, Traceability Matrix, etc.) in the spec files.
3. **Synchronize Integration**: Merge "integration" invariants into the primary spec invariants to ensure a single source of truth for the governance engine.
4. **Update Version Lock**: Recalculate the `canon/` hash to include the new rules.
