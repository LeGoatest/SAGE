-- Core request lifecycle
CREATE TABLE IF NOT EXISTS requests (
  id TEXT PRIMARY KEY,
  method TEXT NOT NULL,
  params_json TEXT NOT NULL,
  status TEXT NOT NULL,                 -- received|queued|running|done|error
  result_json TEXT,                     -- final result json
  error_json TEXT,                      -- {"code":"...","message":"..."} or null
  token_usage INTEGER DEFAULT 0,
  created_at TEXT NOT NULL,             -- RFC3339
  updated_at TEXT NOT NULL              -- RFC3339
);
CREATE INDEX IF NOT EXISTS idx_requests_status ON requests(status);
CREATE INDEX IF NOT EXISTS idx_requests_created_at ON requests(created_at);

-- Event log (replay + audit + SSE reconstruction)
CREATE TABLE IF NOT EXISTS request_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  request_id TEXT NOT NULL,
  event_type TEXT NOT NULL,             -- status|output|reasoning|tool_call
  payload_json TEXT NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY (request_id) REFERENCES requests(id)
);
CREATE INDEX IF NOT EXISTS idx_request_events_request_id ON request_events(request_id);
CREATE INDEX IF NOT EXISTS idx_request_events_created_at ON request_events(created_at);

-- Symbolic memory (distilled cognition)
CREATE TABLE IF NOT EXISTS memory_entries (
  id TEXT PRIMARY KEY,
  request_id TEXT,
  memory_type TEXT NOT NULL,            -- constraint|plan|conclusion|observation|tool_result
  content TEXT NOT NULL,                -- distilled text
  metadata_json TEXT,                   -- optional structured metadata
  importance REAL DEFAULT 0.5,          -- 0..1
  superseded INTEGER DEFAULT 0,          -- 0/1
  created_at TEXT NOT NULL,             -- RFC3339
  FOREIGN KEY (request_id) REFERENCES requests(id)
);
CREATE INDEX IF NOT EXISTS idx_memory_entries_request_id ON memory_entries(request_id);
CREATE INDEX IF NOT EXISTS idx_memory_entries_type ON memory_entries(memory_type);
CREATE INDEX IF NOT EXISTS idx_memory_entries_created_at ON memory_entries(created_at);

-- sqlite-vec vector store for memory embeddings
-- NOTE: This requires sqlite-vec extension loaded (vec0)
CREATE VIRTUAL TABLE IF NOT EXISTS memory_vectors USING vec0(
  id TEXT PRIMARY KEY,
  embedding FLOAT[1536]
);

-- Link symbolic memory -> vector rows (allows different embedding ids if needed)
CREATE TABLE IF NOT EXISTS memory_vector_links (
  memory_id TEXT NOT NULL,
  vector_id TEXT NOT NULL,
  PRIMARY KEY (memory_id, vector_id),
  FOREIGN KEY (memory_id) REFERENCES memory_entries(id)
);
CREATE INDEX IF NOT EXISTS idx_memory_vector_links_memory_id ON memory_vector_links(memory_id);
CREATE INDEX IF NOT EXISTS idx_memory_vector_links_vector_id ON memory_vector_links(vector_id);

-- Tool execution trace (optional but powerful)
CREATE TABLE IF NOT EXISTS tool_executions (
  id TEXT PRIMARY KEY,
  request_id TEXT,
  tool_name TEXT NOT NULL,
  input_json TEXT,
  output_json TEXT,
  status TEXT,                          -- ok|error
  created_at TEXT NOT NULL,             -- RFC3339
  FOREIGN KEY (request_id) REFERENCES requests(id)
);
CREATE INDEX IF NOT EXISTS idx_tool_exec_request_id ON tool_executions(request_id);
CREATE INDEX IF NOT EXISTS idx_tool_exec_tool_name ON tool_executions(tool_name);
CREATE INDEX IF NOT EXISTS idx_tool_exec_created_at ON tool_executions(created_at);
