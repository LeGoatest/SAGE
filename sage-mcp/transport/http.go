package transport

import (
	"encoding/json"
	"net/http"
	"time"

	"sage-mcp/memory"
	"sage-mcp/queue"

	"github.com/google/uuid"
)

type Server struct {
	store   memory.MemoryStore
	pool    *queue.WorkerPool
	sse     *SSEServer
	maxToks int
}

func NewServer(store memory.MemoryStore, pool *queue.WorkerPool, sse *SSEServer, maxToks int) *Server {
	return &Server{
		store:   store,
		pool:    pool,
		sse:     sse,
		maxToks: maxToks,
	}
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

	// Persist
	if err := s.store.SaveRequest(r.Context(), req.ID, req.Method, req.Params); err != nil {
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	// Special Bootstrap logic
	if req.Method == "bootstrap_context" {
		var bParams struct {
			Topic string `json:"topic"`
		}
		json.Unmarshal(req.Params, &bParams)
		embedding, _ := memory.EmbedText(r.Context(), bParams.Topic)
		snap, _ := s.store.GetBootstrapSnapshot(r.Context(), bParams.Topic, embedding)

		s.store.UpdateStatus(r.Context(), req.ID, "done")
		json.NewEncoder(w).Encode(map[string]interface{}{
			"id":     req.ID,
			"ok":     true,
			"result": snap,
			"error":  nil,
		})
		return
	}

	// Normal job
	embedding, _ := memory.EmbedText(r.Context(), req.Method+" "+string(req.Params))
	injected, _ := memory.PrepareInjectedContext(r.Context(), s.store, embedding, memory.InjectionOptions{
		LambdaHours:      0.03,
		MaxContextTokens: s.maxToks,
	})

	s.pool.Enqueue(queue.Job{
		ID:              req.ID,
		Method:          req.Method,
		Params:          req.Params,
		InjectedContext: injected,
	})

	json.NewEncoder(w).Encode(map[string]interface{}{
		"id":     req.ID,
		"ok":     true,
		"result": map[string]bool{"queued": true},
		"error":  nil,
	})
}
