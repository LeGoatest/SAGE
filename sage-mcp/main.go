package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"path/filepath"
	"syscall"
	"time"

	"sage-mcp/adapter"
	"sage-mcp/audit"
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

	// Persistence Initialization
	if err := os.MkdirAll(cfg.DataDir, 0755); err != nil {
		log.Fatalf("failed to create data dir: %v", err)
	}
	if err := os.MkdirAll(cfg.EventsDir, 0755); err != nil {
		log.Fatalf("failed to create events dir: %v", err)
	}

	// Audit Logger
	auditLogger, err := audit.NewLogger(cfg.EventsDir)
	if err != nil {
		log.Fatalf("failed to create audit logger: %v", err)
	}

	store, err := memory.NewSQLiteStore(filepath.Join(cfg.DataDir, "sage.db"))
	if err != nil {
		log.Fatalf("failed to open store: %v", err)
	}
	if err := store.Init(ctx); err != nil {
		log.Fatalf("failed to init store: %v", err)
	}

	// Queue & Adapter
	engine := &adapter.SAGEAdapter{}
	pool := queue.NewWorkerPool(cfg.Workers, engine, store)
	pool.WithAuditLogger(auditLogger)
	pool.Start(ctx)

	// Transport
	sse := transport.NewSSEServer()
	go sse.Broadcast(ctx, pool.Events())

	srv := transport.NewServer(store, pool, sse, cfg.MaxContextTokens)
	srv.WithAuditLogger(auditLogger)

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
		log.Printf("State stored in %s", cfg.DataDir)
		log.Printf("Events stored in %s", cfg.EventsDir)
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
