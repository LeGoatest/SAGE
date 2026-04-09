# Jules Bootstrap Process: Initial Environment Operations

This document details the exact process Jules is designed to operate once the VM environment is created and the repository is first accessed.

## 1. Initial Discovery: The "First Search"

Before any task execution begins, Jules must establish the **Governance Context**. This is done by searching for and accessing the following files in the **Target Repository** (the codebase you provide):

### 1.1 `governance.yaml` (Critical Entrypoint)
- **Purpose:** To resolve the authoritative governance source.
- **Search Logic:** Jules searches for this file at the repository root.
- **Access:** Jules reads the `repo` URL and the `ref` (commit SHA).
- **Enforcement:** If missing or if `ref` is not a commit SHA, Jules is required to **hard fail**.

### 1.2 `AGENTS.md` (Operational Onboarding)
- **Purpose:** To understand repository-specific onboarding and interaction rules.
- **Search Logic:** Root directory.
- **Access:** Provides instructions on the specific task classification and mode transitions expected in this repo.

### 1.3 `.docs/` and `canon/` (Dual-Layer Governance)
- **Purpose:** To load the Narrative Constitution and Machine Canon.
- **Logic:** Under the **External Canon Model**, these are often resolved from the pinned external SAGE repository rather than the local target repository.

---

## 2. The Step-by-Step Bootstrap Sequence

Once governance is resolved, Jules follows a deterministic sequence:

### Step 1: Evidence Detection (`PROJECT_EVIDENCE_REPORT.md`)
Jules scans the codebase for languages, tooling, frameworks, and CI configs.
- **Rule:** Evidence only. Jules is forbidden from inferring or assuming anything that isn't explicitly in the files.

### Step 2: Project Profiling (`project_profile.yaml`)
Jules generates a non-canonical DRAFT profile of the project.
- **Contents:** `primary_language`, `framework`, `database`, etc.
- **Rule:** Unknown values must be marked as `null` or `TODO`.

### Step 3: Canon Evaluation (`CANON_VIOLATIONS_REPORT.md`)
Using the resolved canon, Jules evaluates the target repository against universal invariants.
- **Output:** If violations exist, Jules documents the Invariant ID and evidence of the violation.

### Step 4: Decisions Required (`DECISIONS_NEEDED.md`)
Jules identifies missing declarations such as undefined security models or trust boundaries.
- **Rule:** Jules identifies the questions but **must not** propose solutions or defaults.

---

## 3. Mandatory Constraints & Anti-Hallucination

During the bootstrap process, Jules operates under strict prohibitions:

- **Anti-Hallucination:** Jules MUST NOT invent trust boundaries, threat models, or security properties without explicit evidence in the files.
- **No Speculative Architecture:** Jules cannot "improve" the design during bootstrap; it only reports what is there.
- **HITL Stop Point:** After generating the evidence report and project profile, Jules MUST emit the `[AWAIT_HUMAN_VALIDATION]` marker and stop. Jules cannot proceed to implementation until the human approves the bootstrap results.

---

## 4. Operational Files Produced

| File | Type | Purpose |
| :--- | :--- | :--- |
| `PROJECT_EVIDENCE_REPORT.md` | Audit | Verifiable facts about the environment. |
| `project_profile.yaml` | Metadata | High-level summary of the codebase. |
| `CANON_VIOLATIONS_REPORT.md` | Risk | Invariant breaches detected during scan. |
| `DECISIONS_NEEDED.md` | HITL | Questions required to finalize governance state. |

---
*This document defines the deterministic bootstrap procedure for SAGE-governed environments.*
