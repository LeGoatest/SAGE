# Tasks

Status: DRAFT
Linked Requirements: requirements.md
Linked Design: design.md

---

## 2) Task List

### TASK-001: Initialization
- Description: Initialize `sage-mcp` directory and Go module.
- Files Modified:
  - sage-mcp/go.mod
  - sage-mcp/go.sum

### TASK-002: Transport and API
- Description: Implement HTTP server, health check, and SSE transport.
- Files Modified:
  - sage-mcp/main.go
  - sage-mcp/transport/http.go
  - sage-mcp/transport/sse.go
  - sage-mcp/auth/middleware.go
  - sage-mcp/config/config.go

### TASK-003: Worker Queue
- Description: Implement the job queue and worker pool.
- Files Modified:
  - sage-mcp/queue/job.go
  - sage-mcp/queue/worker.go
  - sage-mcp/adapter/engine.go

### TASK-004: Cognitive Memory
- Description: Implement SQLite + sqlite-vec storage and cognitive injection logic.
- Files Modified:
  - sage-mcp/memory/schema.sql
  - sage-mcp/memory/store.go
  - sage-mcp/memory/sqlite_store.go
  - sage-mcp/memory/vector.go
  - sage-mcp/memory/injection.go
  - sage-mcp/memory/compaction.go

### TASK-005: Deployment
- Description: Create Docker and Caddy configurations.
- Files Modified:
  - sage-mcp/Dockerfile
  - sage-mcp/docker-compose.yml
  - sage-mcp/Caddyfile
  - sage-mcp/README.md

---

## 3) Validation Tasks

### TEST-001: Health Check
- Method: `curl http://localhost:8080/healthz`

### TEST-002: Auth Check
- Method: Verify 401 Unauthorized without Bearer token.

---

[AWAIT_HUMAN_VALIDATION]
