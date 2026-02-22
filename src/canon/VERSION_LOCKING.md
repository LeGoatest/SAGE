# VERSION LOCKING

Version locking ensures stability of governance and prevents "architectural drift" by anchoring execution to a specific state of the canon.

## 1. Canon Versioning
- The Project Canon is versioned (e.g., v1.0, v1.1).
- The version is recorded in `docs/ARCHITECTURE_INDEX.md`.

## 2. Lock Mechanism
- **Spec Anchoring**: Every spec in `.jtasks/` must record the Canon Version it was drafted against.
- **Drift Protection**: If the Canon Version changes during a spec's execution, the agent must STOP and re-verify the spec against the new version.

## 3. Dependency Locking
- **Skill Versions**: Procedural skills in `skills/` are locked to compatible canon versions.
- **External Dependencies**: Tooling and build versions are recorded in `docs/PROJECT_PROFILE.md` and locked via standard package management (e.g., `go.sum`, `package-lock.json`).

## 4. Release Process
Finalizing a major architectural milestone results in a "Canon Release," where all TODOs in the draft pack are cleared and the version is incremented.
