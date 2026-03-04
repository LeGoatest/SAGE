# Design - SAGE MCP Service

Status: DRAFT
Linked Requirements: requirements.md
Canon: canon/ (prevails)

---

## 1) Overview

`sage-mcp` is a Go-based service providing a cognitive orchestration layer for Jules. It manages long-term memory via a vector-enabled SQLite database and enqueues tasks for the SAGE engine.

---

## 2) Architecture Impact

### 2.1 Affected Components
- `sage-mcp/`: New self-contained service.
- `.jtasks/`: Will be used for task records as per SAGE standards.

### 2.2 Unaffected Components
- `..docs/`, `canon/`, `.governance/`: Must remain untouched but will be referenced/called.

---

## 3) Design Decisions

- **DEC-001: Language Choice**: Go (Golang) as requested for high-concurrency transport and worker management.
- **DEC-002: Memory Store**: SQLite with `sqlite-vec`. CGO is required to load the vector extension.
- **DEC-003: Concurrency**: Use a buffered channel for the job queue and a fixed-size worker pool to prevent resource exhaustion.
- **DEC-004: SSE Implementation**: Use a broadcast pattern where the worker writes events to the database and enqueues notifications to active SSE subscribers for a specific request ID.
- **DEC-005: Context Injection**: Implement the composite scoring algorithm (distance, importance, recency) in the `memory/` package.

---

## 4) Data / State Changes

### 4.1 SQLite Schema
Defined exactly as per user requirements in `sage-mcp/memory/schema.sql`.

---

## 5) Interface Changes

### 5.1 MCP Protocol
- `POST /mcp/request`: Accepts method/params, returns job ID.
- `GET /mcp/stream`: Returns SSE stream. Filtering by request ID is implied via query params or event tagging.

---

## 6) Risk Analysis

- **RISK-001: Token Bloat**: Mitigation: Strict caps on bucket counts and total token count (1200).
- **RISK-002: Database Locking**: Mitigation: SQLite WAL mode and careful connection pooling in Go.
- **RISK-003: Extension Loading**: Mitigation: Docker build will pre-install `sqlite-vec` shared library.

---

## 7) Failure Alignment

- FAIL-001 (Queue Exhaustion) -> Handled by returning 503 if the buffered channel is full.
- FAIL-002 (DB Failure) -> Handled by standard Go error wrapping and service health checks.

---

## 8) Acceptance Alignment

- AC-001 -> Verified via `/healthz`.
- AC-002 -> Verified via job ID return and `requests` table entry.
- AC-004 -> Verified by running vector distance queries in the database.

---

## 9) HITL Gate

[AWAIT_HUMAN_VALIDATION]
