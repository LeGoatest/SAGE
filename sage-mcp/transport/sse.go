package transport

import (
	"context"
	"fmt"
	"net/http"
	"sync"

	"sage-mcp/queue"
)

type SSEServer struct {
	mu          sync.Mutex
	subscribers map[chan queue.RequestEvent]bool
}

func NewSSEServer() *SSEServer {
	return &SSEServer{
		subscribers: make(map[chan queue.RequestEvent]bool),
	}
}

func (s *SSEServer) HandleStream(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/event-stream")
	w.Header().Set("Cache-Control", "no-cache")
	w.Header().Set("Connection", "keep-alive")
	w.Header().Set("Access-Control-Allow-Origin", "*")

	flusher, ok := w.(http.Flusher)
	if !ok {
		http.Error(w, "Streaming unsupported", http.StatusInternalServerError)
		return
	}

	ch := make(chan queue.RequestEvent, 10)
	s.mu.Lock()
	s.subscribers[ch] = true
	s.mu.Unlock()

	defer func() {
		s.mu.Lock()
		delete(s.subscribers, ch)
		s.mu.Unlock()
		close(ch)
	}()

	for {
		select {
		case <-r.Context().Done():
			return
		case ev := <-ch:
			fmt.Fprintf(w, "event: %s\n", ev.Type)
			fmt.Fprintf(w, "data: %s\n\n", string(ev.Payload))
			flusher.Flush()
		}
	}
}

func (s *SSEServer) Broadcast(ctx context.Context, events <-chan queue.RequestEvent) {
	for {
		select {
		case <-ctx.Done():
			return
		case ev := <-events:
			s.mu.Lock()
			for ch := range s.subscribers {
				select {
				case ch <- ev:
				default:
					// Slow subscriber, drop
				}
			}
			s.mu.Unlock()
		}
	}
}
