# Requirements - SAGE Persistence and Audit Logging

## REQ-001: Standardize DB Location
The system SHALL support `SAGE_DATA_DIR` and default to `.sage/state` for local development.
- Input: `SAGE_DATA_DIR` environment variable.
- Output: Initialized SQLite database in `.sage/state/sage.db`.
- Constraint: Ensure directories exist on startup.

## REQ-002: JSONL Session Audit Log
The system SHALL emit an append-only audit trail in `.sage/events/session.jsonl`.
- Input: Request and internal event stream.
- Output: Exactly one JSON object per line.
- Constraint: Atomicity per line and concurrent safety.

## REQ-003: SQLite Safe Logging (Truncation)
The system SHALL truncate JSON fields exceeding 64KB when storing in SQLite.
- Input: Large JSON payload.
- Output: Stored JSON containing prefix (8KB), SHA256 hash, and `"truncated": true`.

## REQ-004: SQLite Safe Logging (Redaction)
The system SHALL redact values for sensitive keys in stored JSON payloads.
- Input: JSON containing keys like `token`, `auth`, `password`, `secret`, `api_key`.
- Output: Values replaced with `"REDACTED"`.

## REQ-005: State Size Monitoring
The system SHALL provide a CI script to monitor state and event log sizes.
- Input: `.sage/state/` and `.sage/events/` files.
- Output: Pass/Fail based on limits (SQLite < 100MB, JSONL < 10MB).

## Failure Modeling
| Failure | Response |
| :--- | :--- |
| Failed to create directory | Log error and exit |
| Failed to write audit line | Log warning, do not block request |
| Malformed JSON for redaction | Store with warning, ensure no secret leakage |

## Traceability Matrix
| Requirement | Design Section | Task ID |
| :--- | :--- | :--- |
| REQ-001 | Config & Initialization | TASK-01, TASK-02 |
| REQ-002 | Audit Logging Service | TASK-03, TASK-04 |
| REQ-003 | SQLite Store Hardening | TASK-05 |
| REQ-004 | SQLite Store Hardening | TASK-05 |
| REQ-005 | CI Size Guard | TASK-06 |
