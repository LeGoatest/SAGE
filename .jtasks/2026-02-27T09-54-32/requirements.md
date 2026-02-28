# Requirements

Status: DRAFT
Task Group: RUNTIME_SERVICE / COGNITIVE_ORCHESTRATION
Modes: ENTER_DEEP_GOVERNANCE_MODE → ENTER_SPEC_MODE → ENTER_EXEC_MODE
Canon: canon/ (prevails)

---

## 0) Brownfield Determination (Mandatory)

Is this task modifying or extending an existing system?

- YES → GAP_REPORT.md is REQUIRED.
- NO → GAP_REPORT.md is OPTIONAL. (New component `sage-mcp/`)

---

## 1) Purpose

Build a deployable MCP-style cognitive orchestration server (`sage-mcp`) around the existing SAGE engine to reduce token debt through persistent memory and semantic recall.

---

## 2) Evidence (No Inference)

- User requirement for a self-contained `sage-mcp/` folder.
- Service contract for `/healthz`, `/mcp/request`, and `/mcp/stream`.
- Mandatory use of Go, HTTP+SSE, Worker queue, SQLite, and `sqlite-vec`.
- Specified schema for `requests`, `request_events`, `memory_entries`, `memory_vectors`, `memory_vector_links`, and `tool_executions`.
- Specified cognitive injection and anti-token-bloat algorithms.

---

## 3) Structured Constraint Extraction (Required)

```yaml
reasoning_context:
  situation:
    - Jules currently lacks persistent cross-session cognitive memory, leading to token debt.
    - SAGE engine exists but needs an MCP-style orchestration wrapper.
  constraints:
    - MUST NOT move existing SAGE files.
    - MUST live entirely in `sage-mcp/`.
    - MUST use Go for the server.
    - MUST use CGO_ENABLED=1 for `sqlite-vec`.
    - MUST use Bearer auth for MCP endpoints.
  true_goal:
    - Create a self-contained cognitive orchestration service that manages memory and enqueues SAGE engine jobs.
  failure_states:
    - FAIL-001: SSE stream blocking HTTP request threads.
    - FAIL-002: Token bloat due to failure in memory compaction or duplicate suppression.
    - FAIL-003: SQLite-vec extension failing to load.
```

---

## 4) Functional Requirements (EARS)

- REQ-001: While enqueued, the system SHALL process jobs using a worker pool.
- REQ-002: When a request is received, the system SHALL return a queued response immediately and enqueues the job.
- REQ-003: If authorized, the system SHALL provide an SSE stream of status and output events.
- REQ-004: When processing a non-bootstrap request, the system SHALL inject relevant memory snippets based on the vector-search algorithm.
- REQ-005: Upon job completion, the system SHALL perform memory compaction and distillation.
- REQ-006: When method is "bootstrap_context", the system SHALL return a canonical snapshot of constraints and plans.

---

## 5) Non-Functional Requirements

- NFR-001: Persistent cognitive memory using SQLite + `sqlite-vec`.
- NFR-002: Maximum context injection budget of 1200 tokens.
- NFR-003: Bearer token authentication for all `/mcp/` endpoints.
- NFR-004: Dockerized deployment with Caddy reverse proxy.

---

## 6) Failure Modeling

- FAIL-001: Worker queue exhaustion.
- FAIL-002: Database corruption or extension load failure.
- FAIL-003: Memory injection surpassing token limits.

---

## 7) Traceability Matrix

| Requirement | Evidence | Design Ref | Task Ref | Test/Validation | Canon Link | Failure State |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| REQ-001 | User Goal | design.md §Worker | TASK-003 | SSE state 'running' | N/A | FAIL-001 |
| REQ-002 | Contract | design.md §Transport | TASK-002 | POST response code 200 | N/A | N/A |
| REQ-003 | Contract | design.md §Transport | TASK-002 | EventSource stream | N/A | N/A |
| REQ-004 | Algorithm | design.md §Memory | TASK-004 | Trace log injection | N/A | FAIL-003 |
| REQ-005 | Bloat Ctrl | design.md §Memory | TASK-004 | `memory_entries` count | N/A | N/A |
| REQ-006 | Bootstrap | design.md §Bootstrap | TASK-002 | JSON response structure | N/A | N/A |

---

## 8) Acceptance Criteria

- AC-001: `GET /healthz` returns 200 OK.
- AC-002: `POST /mcp/request` enqueues and returns immediately.
- AC-003: `GET /mcp/stream` provides real-time status and output updates.
- AC-004: Cognitive memory persists in `sage.db` and utilizes `vec0` virtual table.
- AC-005: Context injection respects the composite scoring and token budget.
- AC-006: Docker Compose successfully brings up `sage-mcp` and `caddy`.
