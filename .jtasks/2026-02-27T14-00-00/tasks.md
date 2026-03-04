# Tasks - SAGE Persistence and Audit Logging

## Phase 1: Storage Infrastructure
- [ ] TASK-01: Update `config/config.go` to support `SAGE_DATA_DIR` and resolve local paths.
  - Files Modified: `sage-mcp/config/config.go`
- [ ] TASK-02: Update `main.go` to initialize directories for state and events.
  - Files Modified: `sage-mcp/main.go`
- [ ] TASK-05: Implement JSON truncation and redaction guards in `memory/sqlite_store.go`.
  - Files Modified: `sage-mcp/memory/sqlite_store.go`, `sage-mcp/memory/guard.go`

## Phase 2: Audit Trail
- [ ] TASK-03: Implement the `audit.Logger` service.
  - Files Modified: `sage-mcp/audit/logger.go`
- [ ] TASK-04: Wire `audit.Logger` into HTTP transport and Worker Pool.
  - Files Modified: `sage-mcp/transport/http.go`, `sage-mcp/queue/worker.go`

## Phase 3: Monitoring & Docs
- [ ] TASK-06: Create `tools/ci/check_state_size.sh`.
  - Files Modified: `tools/ci/check_state_size.sh`
- [ ] TASK-07: Update `sage-mcp/README.md` with persistence and audit details.
  - Files Modified: `sage-mcp/README.md`
