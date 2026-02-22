---
name: cicd-ops
description: Procedure for managing and installing CI/CD pipelines, linting configurations, and build scripts.
metadata:
  category: operations
  authority: procedural
---

# Skill: cicd-ops

## Authority Boundary
This skill is **procedural only**.
It installs or modifies automation; it does NOT change the underlying project architecture or security model.

## Procedure

### Step 1: Stack Detection
Identify the project stack by checking `docs/PROJECT_PROFILE.md` or scanning the repository (e.g., `go.mod`, `package.json`).

### Step 2: Asset Selection
Based on the detected stack, select the appropriate templates from the `assets/` directory.

### Step 3: Installation
Install the selected files into their canonical locations:
- **GitHub Actions**: `.github/workflows/`
- **Linting**: Root directory (e.g., `.golangci.yml`)
- **Build**: Root directory (e.g., `Makefile`)
- **PR Template**: `.github/pull_request_template.md`

### Step 4: Verification
1. Run local build/lint commands (e.g., `make ci`) to ensure the newly installed configurations are valid.
2. Verify that the files do not conflict with existing project-specific settings.

## Guidelines
- Always prioritize existing project configurations unless explicitly asked to overwrite them.
- Ensure all CI workflows are restricted to `contents: read` permissions unless more are strictly required.
- Use `set -euo pipefail` in shell scripts for robustness.
