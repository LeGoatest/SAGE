# Design - SAGE Persistence and Audit Logging

## Component Overview

### Audit Logger (`audit/logger.go`)
- Thread-safe, append-only logger for JSONL emission.
- Encapsulates file operations with `sync.Mutex`.
- Defines `AuditEntry` struct to ensure consistency across log entries.

### Storage Guard (`memory/guard.go`)
- Provides `CleanseJSON(payload []byte)` utility.
- Implements two-pass processing:
  1. Redaction of sensitive keys using a case-insensitive regex or JSON map walk.
  2. Truncation of large strings (> 8KB) and overall payload check (> 64KB).

### Config & Startup (`config/config.go` & `main.go`)
- Standardizes path resolution for `.sage/state` and `.sage/events`.
- Injects `AuditLogger` into the `Server` and `WorkerPool`.

## Monitoring Strategy
`tools/ci/check_state_size.sh` will be a standalone bash script that performs simple `du -m` checks against pre-defined thresholds.

## Integration Plan
1. Update `config.go` to handle `SAGE_DATA_DIR`.
2. Implement `memory.CleanseJSON` and integrate into `SQLiteStore`.
3. Implement `audit.Logger` and integrate into `Server.HandleRequest` and `WorkerPool.process`.
4. Create CI script.
