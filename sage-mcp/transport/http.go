package transport

import (
	"encoding/json"
	"net/http"
	"time"

	"sage-mcp/audit"
	"sage-mcp/memory"
	"sage-mcp/queue"
	"sage-mcp/repo"

	"github.com/google/uuid"
)

type Server struct {
	store   memory.MemoryStore
	pool    *queue.WorkerPool
	sse     *SSEServer
	maxToks int
	audit   *audit.Logger
}

func NewServer(store memory.MemoryStore, pool *queue.WorkerPool, sse *SSEServer, maxToks int) *Server {
	return &Server{
		store:   store,
		pool:    pool,
		sse:     sse,
		maxToks: maxToks,
	}
}

func (s *Server) WithAuditLogger(l *audit.Logger) {
	s.audit = l
}

func (s *Server) HandleHealth(w http.ResponseWriter, r *http.Request) {
	json.NewEncoder(w).Encode(map[string]interface{}{
		"ok":      true,
		"service": "sage-mcp",
		"ts":      time.Now().Format(time.RFC3339),
	})
}

func (s *Server) HandleRequest(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		return
	}

	var req struct {
		ID     string          `json:"id"`
		Method string          `json:"method"`
		Params json.RawMessage `json:"params"`
	}

	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Bad Request", http.StatusBadRequest)
		return
	}

	if req.ID == "" {
		req.ID = uuid.New().String()
	}

	// Audit Logging
	if s.audit != nil {
		s.audit.LogRequest(req.ID, req.Method, "incoming request")
	}

	// Persist
	if err := s.store.SaveRequest(r.Context(), req.ID, req.Method, req.Params); err != nil {
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	// Route methods
	switch req.Method {
	case "bootstrap_context":
		s.handleBootstrap(w, r, req.ID, req.Params)
	case "repo.list":
		s.handleRepoList(w, r, req.ID, req.Params)
	case "repo.read":
		s.handleRepoRead(w, r, req.ID, req.Params)
	case "repo.search":
		s.handleRepoSearch(w, r, req.ID, req.Params)
	case "repo.patch":
		s.handleRepoPatch(w, r, req.ID, req.Params)
	default:
		s.handleSageJob(w, r, req.ID, req.Method, req.Params)
	}
}

func (s *Server) handleBootstrap(w http.ResponseWriter, r *http.Request, id string, params json.RawMessage) {
	var bParams struct {
		Topic string `json:"topic"`
	}
	json.Unmarshal(params, &bParams)
	embedding, _ := memory.EmbedText(r.Context(), bParams.Topic)
	snap, _ := s.store.GetBootstrapSnapshot(r.Context(), bParams.Topic, embedding)

	s.store.UpdateStatus(r.Context(), id, "done")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"id":     id,
		"ok":     true,
		"result": snap,
		"error":  nil,
	})
}

func (s *Server) handleRepoList(w http.ResponseWriter, r *http.Request, id string, params json.RawMessage) {
	var p struct {
		Dir       string `json:"dir"`
		Recursive bool   `json:"recursive"`
		MaxItems  int    `json:"max_items"`
	}
	if p.MaxItems == 0 {
		p.MaxItems = 5000
	}
	json.Unmarshal(params, &p)

	res, err := repo.List(".", p.Dir, p.Recursive, p.MaxItems)
	if err != nil {
		s.jsonError(w, id, err, http.StatusBadRequest)
		return
	}

	s.store.UpdateStatus(r.Context(), id, "done")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"id":     id,
		"ok":     true,
		"result": res,
		"error":  nil,
	})
}

func (s *Server) handleRepoRead(w http.ResponseWriter, r *http.Request, id string, params json.RawMessage) {
	var p struct {
		Path     string `json:"path"`
		MaxBytes int    `json:"max_bytes"`
	}
	if p.MaxBytes == 0 {
		p.MaxBytes = 1048576
	}
	json.Unmarshal(params, &p)

	res, err := repo.Read(".", p.Path, p.MaxBytes)
	if err != nil {
		s.jsonError(w, id, err, http.StatusBadRequest)
		return
	}

	s.store.UpdateStatus(r.Context(), id, "done")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"id":     id,
		"ok":     true,
		"result": res,
		"error":  nil,
	})
}

func (s *Server) handleRepoSearch(w http.ResponseWriter, r *http.Request, id string, params json.RawMessage) {
	var p struct {
		Query   string   `json:"query"`
		Dir     string   `json:"dir"`
		Globs   []string `json:"globs"`
		MaxHits int      `json:"max_hits"`
	}
	if p.MaxHits == 0 {
		p.MaxHits = 200
	}
	json.Unmarshal(params, &p)

	res, err := repo.Search(".", p.Dir, p.Query, p.Globs, p.MaxHits)
	if err != nil {
		s.jsonError(w, id, err, http.StatusBadRequest)
		return
	}

	s.store.UpdateStatus(r.Context(), id, "done")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"id":     id,
		"ok":     true,
		"result": res,
		"error":  nil,
	})
}

func (s *Server) handleRepoPatch(w http.ResponseWriter, r *http.Request, id string, params json.RawMessage) {
	// Queue-based
	s.handleSageJob(w, r, id, "repo.patch", params)
}

func (s *Server) handleSageJob(w http.ResponseWriter, r *http.Request, id, method string, params json.RawMessage) {
	embedding, _ := memory.EmbedText(r.Context(), method+" "+string(params))
	injected, _ := memory.PrepareInjectedContext(r.Context(), s.store, embedding, memory.InjectionOptions{
		LambdaHours:      0.03,
		MaxContextTokens: s.maxToks,
	})

	s.pool.Enqueue(queue.Job{
		ID:              id,
		Method:          method,
		Params:          params,
		InjectedContext: injected,
	})

	json.NewEncoder(w).Encode(map[string]interface{}{
		"id":     id,
		"ok":     true,
		"result": map[string]bool{"queued": true},
		"error":  nil,
	})
}

func (s *Server) jsonError(w http.ResponseWriter, id string, err error, code int) {
	s.store.UpdateStatus(context.Background(), id, "error")
	w.WriteHeader(code)
	json.NewEncoder(w).Encode(map[string]interface{}{
		"id":     id,
		"ok":     false,
		"result": nil,
		"error":  err.Error(),
	})
}
