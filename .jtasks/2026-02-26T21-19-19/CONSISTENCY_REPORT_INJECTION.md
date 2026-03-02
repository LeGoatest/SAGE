# CONSISTENCY REPORT - Injection Model Audit

Status: **FAIL**

## 1. Governance Docs Directory
- Result: **INCONSISTENT**
- Findings: The repository uses `..docs/` as the primary standard (80 instances), but 17 instances of legacy `.docs/` paths remain in `skills/`, `canon/`, and `CONTRIBUTING.md`.

## 2. Target Repo Independence
- Result: **FAIL**
- Findings: Multiple validators and scripts still assume `..docs/` and `canon/` exist in the current working directory.
  - `tools/sage_validate.py` hardcodes `ROOT / "..docs/..."`
  - `tools/sage-check.sh` hardcodes `ROOT/..docs/...`
  - `.governance/legacy_validator.py` hardcodes `Path("canon")`
  - `.governance/graph_generator.py` hardcodes `Path("canon")`

## 3. Bootstrap Behavior
- Result: **PASS**
- Findings: `scripts/sage-bootstrap.sh` correctly clones and pins SAGE to `.sage/` and initializes templates. It respects the non-mutation rule for SAGE contents.

## 4. Path Resolution
- Result: **PARTIAL**
- Findings: The core SAGE engine (`validator.py`, `boot_validator.py`) is injection-aware, but secondary auditing tools are not.
