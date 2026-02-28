package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"sage-mcp/adapter"
	"sage-mcp/auth"
	"sage-mcp/config"
	"sage-mcp/memory"
	"sage-mcp/queue"
	"sage-mcp/transport"
)

func main() {
	cfg := config.Load()
	if cfg.Token == "" {
		log.Fatal("SAGE_MCP_TOKEN is required")
	}

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()

	// Persistence
	if err := os.MkdirAll(cfg.DataDir, 0755); err != nil {
		log.Fatalf("failed to create data dir: %v", err)
	}
	store, err := memory.NewSQLiteStore(cfg.DataDir + "/sage.db")
	if err != nil {
		log.Fatalf("failed to open store: %v", err)
	}
	if err := store.Init(ctx); err != nil {
		log.Fatalf("failed to init store: %v", err)
	}

	// Queue & Adapter
	engine := &adapter.SAGEAdapter{}
	pool := queue.NewWorkerPool(cfg.Workers, engine, store)
	pool.Start(ctx)

	// Transport
	sse := transport.NewSSEServer()
	go sse.Broadcast(ctx, pool.Events())

	srv := transport.NewServer(store, pool, sse, cfg.MaxContextTokens)

	mux := http.NewServeMux()
	mux.HandleFunc("/healthz", srv.HandleHealth)
	mux.HandleFunc("/mcp/request", srv.HandleRequest)
	mux.HandleFunc("/mcp/stream", sse.HandleStream)

	handler := auth.Middleware(cfg.Token, mux)

	httpSrv := &http.Server{
		Addr:    cfg.Addr,
		Handler: handler,
	}

	go func() {
		log.Printf("SAGE MCP serving on %s", cfg.Addr)
		if err := httpSrv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("listen: %s\n", err)
		}
	}()

	<-ctx.Done()
	log.Println("Shutting down gracefully...")

	shutdownCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := httpSrv.Shutdown(shutdownCtx); err != nil {
		log.Fatalf("Server forced to shutdown: %v", err)
	}

	pool.Stop()
	log.Println("SAGE MCP stopped.")
}
