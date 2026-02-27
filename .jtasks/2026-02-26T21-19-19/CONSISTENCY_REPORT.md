# CONSISTENCY REPORT

Status: FAILED
Audit Date: 2026-02-26

## 1. Inventory Status
- Spec Templates: ✅ 5/5 present.
- Governance Rules (Spec): ❌ 2/8 present. Missing 6 files.
- Governance Rules (Session): ✅ 2/2 present.
- CI Validators: ✅ 2/2 present.
- GitHub Workflows: ✅ 2/2 present.
- Narrative Constitution: ✅ `.docs/` present.

## 2. Integrity Issues
- Foundational spec rules (A4 alignment) are missing machine-readable definitions.
- Templates are correctly structured but have no machine-readable enforcement of that structure.
- Redundant integration files (`gap_report_ci_integration.yaml`, `handover_integration.yaml`) overlap with core invariants.

## 3. Structural Alignment
- `requirements.md`: Compliant.
- `tasks.md`: Compliant.
- `GAP_REPORT.md`: Compliant.
- `HANDOVER.md`: Compliant.

## 4. CI Alignment
- Triggers and script logic are aligned with SAGE v5 intents.
