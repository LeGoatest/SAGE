# Bootstrapping a Target Repository  
## SAGE v4.1 — External Canon Model

---

# Terminology

To eliminate ambiguity:

- **SAGE Repository**
  The Sovereign Agent Governance Engine repository.
  This contains the Universal Canon.  
  It is the only authoritative governance source.

- **Target Repository**  
  The project being governed and evaluated by Jules.  
  This is the codebase under bootstrap or validation.

- **Jules Environment**  
  The execution environment running governance evaluation.  
  It contains:
  - Target Repository (working directory)
  - Jules Canon Cache (external, read-only)
  - No canonical documents inside the Target Repository

---

# Core Rule

The Target Repository:

- MUST NOT contain canonical documents.
- MUST NOT generate or modify canonical documents.
- MUST only declare governance reference via `governance.yaml`.

Canon lives exclusively in the SAGE Repository.

---

# Preconditions (Target Repository)

The Target Repository MUST contain:

```yaml
# governance.yaml
sage:
  repo: https://github.com/LeGoatest/Sovereign-agent-template
  ref: <commit-sha>
  mode: strict
```

Rules:

- `ref` MUST be a commit SHA.
- Branch names are forbidden.
- Missing `governance.yaml` → hard fail.
- Invalid `ref` → hard fail.

---

# Jules Canon Resolution (Before Bootstrap)

For every bootstrap session:

1. Read `governance.yaml` from Target Repository.
2. Resolve `<ref>` via Jules Canon Cache.
3. Materialize read-only checkout if missing.
4. Load canonical entrypoint:

```
<jules_cache>/sage/checkouts/<ref>/canon/bootstrap.md
```

Prompts MUST NOT specify canon paths.
Only `governance.yaml` controls canon resolution.

Failure to resolve canon → abort.

---

# Step 1 — Detect Target Repository Evidence

The Agent scans the Target Repository and produces:

```
PROJECT_EVIDENCE_REPORT.md
```

Contents:

- Detected languages
- Tooling
- Frameworks
- Build systems
- CI configuration
- Security-relevant artifacts
- Runtime indicators
- Structural layout

Rules:

- Evidence only.
- No inference.
- No assumptions.
- No architectural speculation.

---

# Step 2 — Generate Project Profile (Non-Canonical)

The Agent generates:

```
project_profile.yaml
```

Located at the root of the Target Repository.

Example:

```yaml
project:
  primary_language: Go
  framework: Gin
  rendering: HTMX
  database: SQLite
  ci: GitHub Actions
  security_model_defined: false
```

Rules:

- Must be labeled DRAFT.
- Must reflect only explicit evidence.
- Unknown values must be `null` or `TODO`.
- This file is not canon.
- This file does not alter canon.

---

# Step 3 — Canon Evaluation

Using the externally resolved canon:

The Agent evaluates the Target Repository against universal invariants.

If violations exist:

Generate:

```
CANON_VIOLATIONS_REPORT.md
```

Each entry must include:

- Invariant ID
- Evidence reference
- Description of violation
- Required decision or correction

No canon files are generated.
No canon files are modified.

---

# Step 4 — Propose Skills (Operational Layer)

Agent may propose operational skills in:

```
skills/<skill_name>/
```

Skills are:

- Tooling helpers
- Not governance
- Optional
- Non-authoritative

---

# Step 5 — Generate DECISIONS_NEEDED.md

This file must contain:

- Undefined security model declarations
- Missing trust boundary definitions
- Required project authority declarations
- Architectural ambiguities
- Required governance classifications

Rules:

- No solutions.
- No defaults.
- Only questions and required declarations.

---

# Anti-Hallucination Rule (Mandatory)

The Agent MUST NOT:

- Invent trust boundaries
- Invent threat models
- Invent roles
- Invent security properties
- Infer architecture without explicit evidence

If evidence missing:

- Mark as TODO.
- Add to DECISIONS_NEEDED.md.
- Do not fabricate.

If security model undefined:

- Do NOT generate `SECURITY_MODEL.md`.
- Add required declarations to DECISIONS_NEEDED.md.
- Set `security_model_defined: false`.

Violation requires refusal.

---

# Step 6 — STOP POINT (HITL)

After producing:

- PROJECT_EVIDENCE_REPORT.md
- project_profile.yaml (DRAFT)
- CANON_VIOLATIONS_REPORT.md (if applicable)
- DECISIONS_NEEDED.md

The Agent MUST:

1. STOP.
2. Present DECISIONS_NEEDED.md.
3. Wait for explicit human validation.
4. NOT proceed to implementation.
5. NOT mutate canon.
6. NOT finalize governance state.

---

# L0 Enforcement Invariants

- Target Repository MUST NOT contain canonical documents.
- Target Repository MUST NOT contain `.canon/`.
- Canon MUST be resolved from pinned external `ref`.
- Prompts MUST NOT override canon entrypoint.
- Canon mutations MUST occur only in the SAGE Repository.
- Canon is authoritative; Target Repository is declarative only.

---

# Emit

[AWAIT_HUMAN_VALIDATION]
