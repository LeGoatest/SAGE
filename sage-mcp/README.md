# SAGE MCP (Cognitive Orchestration Service)

Self-contained MCP-style server for the Sovereign Agent Governance Engine (SAGE).

## Features
- Persistent cognitive memory via SQLite + `sqlite-vec`.
- **Repository File API**: Safe list, read, search, and patch.
- **Git-Friendly Audit Trail**: Append-only JSONL session logs.
- **Safe Storage**: Automatic redaction of secrets and truncation of large payloads.
- Semantic recall and context injection.
- Worker-queued SAGE engine execution.
- Real-time event streaming via SSE.
- Anti-token-bloat distillation and duplicate suppression.

## Architecture
- **Adapter**: Interfaces with the SAGE Python/Bash engine.
- **Repo**: SAGE-governed repository file interface.
- **Queue**: Asynchronous job processing with worker pool.
- **Memory**: Vector-enabled long-term storage.
- **Transport**: HTTP API with Bearer token auth.
- **Audit**: Thread-safe JSONL event logging.

## Configuration
| Env Var | Default | Description |
| --- | --- | --- |
| SAGE_MCP_ADDR | :8080 | Listen address |
| SAGE_MCP_TOKEN | (required) | Bearer auth token |
| SAGE_MCP_WORKERS | 2 | Number of concurrent workers |
| SAGE_DATA_DIR | .sage/state | Directory for SQLite database |
| SAGE_EVENTS_DIR| .sage/events | Directory for JSONL audit logs |

## Persistence

### SQLite (Runtime State)
SAGE uses SQLite with the `sqlite-vec` extension for runtime memory and vector search. By default, it resides in `.sage/state/sage.db`. This file contains the active session state and should generally be ignored by Git (added to `.gitignore`) unless a persistent snapshot is required.

### JSONL (Audit Trail)
SAGE emits an append-only audit trail to `.sage/events/session.jsonl`. This file is designed to be committed to Git to provide a verifiable history of agent actions.
- **Safe Redaction**: Fields like `token`, `password`, and `secret` are automatically replaced with `REDACTED`.
- **Size Guards**: Payloads exceeding 64KB are truncated to 8KB with a SHA256 hash for integrity.

## Monitoring
Use `tools/ci/check_state_size.sh` to monitor the size of state files.
- **SQLite Limit**: 100MB
- **JSONL Limit**: 10MB

## API Methods

### `repo.list`
Lists files and directories.
```json
{ "dir": ".", "recursive": false, "max_items": 5000 }
```

### `repo.read`
Reads file content with binary detection and truncation support.
```json
{ "path": "README.md", "max_bytes": 1048576 }
```

### `repo.search`
Pure-Go deterministic file content search.
```json
{ "query": "TODO", "dir": ".", "globs": ["*.go"], "max_hits": 200 }
```

### `repo.patch` (Queued)
Applies a unified diff atomically with SAGE protection gates.
```json
{
  "path": "main.go",
  "unified_diff": "...",
  "create_if_missing": false,
  "task_group": "FEATURE"
}
```

## Build

### Local Build
Ensure you have Go 1.24+ and a C compiler (gcc) installed for CGO.
```bash
cd sage-mcp
# Build binary
CGO_ENABLED=1 go build -o sage-mcp .
```

### Makefile
```bash
cd sage-mcp
make build
```

## Deployment
```bash
docker-compose up -d
```
