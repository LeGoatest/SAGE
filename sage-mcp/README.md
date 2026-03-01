# SAGE MCP (Cognitive Orchestration Service)

Self-contained MCP-style server for the Sovereign Agent Governance Engine (SAGE).

## Features
- Persistent cognitive memory via SQLite + `sqlite-vec`.
- Semantic recall and context injection.
- Worker-queued SAGE engine execution.
- Real-time event streaming via SSE.
- Anti-token-bloat distillation and duplicate suppression.

## Architecture
- **Adapter**: Interfaces with the SAGE Python/Bash engine.
- **Queue**: Asynchronous job processing with worker pool.
- **Memory**: Vector-enabled long-term storage.
- **Transport**: HTTP API with Bearer token auth.

## Configuration
| Env Var | Default | Description |
| --- | --- | --- |
| SAGE_MCP_ADDR | :8080 | Listen address |
| SAGE_MCP_TOKEN | (required) | Bearer auth token |
| SAGE_MCP_WORKERS | 2 | Number of concurrent workers |
| SAGE_MCP_DATA_DIR | /data | SQLite data directory |

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
