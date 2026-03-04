package queue

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"sync"
	"time"

	"sage-mcp/adapter"
	"sage-mcp/audit"
	"sage-mcp/memory"
	"sage-mcp/repo"
)

type WorkerPool struct {
	jobs    chan Job
	engine  adapter.Engine
	store   memory.MemoryStore
	wg      sync.WaitGroup
	workers int
	audit   *audit.Logger

	// Simple event hub for SSE
	events chan RequestEvent
}

type RequestEvent struct {
	RequestID string
	Type      string // status|output|repo_patch_*
	Payload   json.RawMessage
}

func NewWorkerPool(workers int, engine adapter.Engine, store memory.MemoryStore) *WorkerPool {
	return &WorkerPool{
		jobs:    make(chan Job, 100),
		engine:  engine,
		store:   store,
		workers: workers,
		events:  make(chan RequestEvent, 200),
	}
}

func (p *WorkerPool) WithAuditLogger(l *audit.Logger) {
	p.audit = l
}

func (p *WorkerPool) Start(ctx context.Context) {
	for i := 0; i < p.workers; i++ {
		p.wg.Add(1)
		go p.worker(ctx)
	}
}

func (p *WorkerPool) Enqueue(job Job) {
	p.jobs <- job
}

func (p *WorkerPool) Events() <-chan RequestEvent {
	return p.events
}

func (p *WorkerPool) worker(ctx context.Context) {
	defer p.wg.Done()
	for {
		select {
		case <-ctx.Done():
			return
		case job, ok := <-p.jobs:
			if !ok {
				return
			}
			p.process(ctx, job)
		}
	}
}

func (p *WorkerPool) process(ctx context.Context, job Job) {
	p.updateStatus(ctx, job.ID, "running")

	// Special case: REPO_PATCH
	if job.Method == "repo.patch" {
		p.processRepoPatch(ctx, job)
		return
	}

	var outputAccumulator string
	emit := func(chunk string) {
		outputAccumulator += chunk
		payload, _ := json.Marshal(map[string]interface{}{
			"id":    job.ID,
			"chunk": chunk,
			"ts":    time.Now().Format(time.RFC3339),
		})
		p.emitEvent(ctx, job.ID, "output", payload)
	}

	result, err := p.engine.Execute(ctx, job.Method, job.Params, job.InjectedContext, emit)
	if err != nil {
		p.updateStatus(ctx, job.ID, "error")
		errJSON, _ := json.Marshal(map[string]string{"message": err.Error()})
		p.store.SaveResult(ctx, job.ID, nil, errJSON)
		return
	}

	p.store.SaveResult(ctx, job.ID, result, nil)
	p.updateStatus(ctx, job.ID, "done")

	// Compaction
	memory.CompactMemory(ctx, p.store, job.ID, outputAccumulator)
}

func (p *WorkerPool) processRepoPatch(ctx context.Context, job Job) {
	var params struct {
		Path            string `json:"path"`
		UnifiedDiff     string `json:"unified_diff"`
		CreateIfMissing bool   `json:"create_if_missing"`
		TaskGroup       string `json:"task_group"`
	}
	if err := json.Unmarshal(job.Params, &params); err != nil {
		p.failJob(ctx, job.ID, fmt.Errorf("invalid params: %w", err))
		return
	}

	// 1. Started event
	startPayload, _ := json.Marshal(map[string]interface{}{
		"id":   job.ID,
		"path": params.Path,
		"ts":   time.Now().Format(time.RFC3339),
	})
	p.emitEvent(ctx, job.ID, "repo_patch_started", startPayload)
	if p.audit != nil {
		p.audit.LogEvent(job.ID, "repo_patch_started", fmt.Sprintf("patch started for %s", params.Path))
	}

	// 2. Guard Check
	if err := repo.CheckWritePermission(params.Path, params.TaskGroup); err != nil {
		p.failJob(ctx, job.ID, err)
		p.emitEvent(ctx, job.ID, "repo_patch_failed", startPayload)
		if p.audit != nil {
			p.audit.LogEvent(job.ID, "repo_patch_failed", fmt.Sprintf("permission denied for %s: %v", params.Path, err))
		}
		return
	}

	// 3. Apply Patch
	repoRoot := "."
	res, err := repo.ApplyPatch(repoRoot, params.Path, params.UnifiedDiff, params.CreateIfMissing)
	if err != nil {
		p.failJob(ctx, job.ID, err)
		p.emitEvent(ctx, job.ID, "repo_patch_failed", startPayload)
		if p.audit != nil {
			p.audit.LogEvent(job.ID, "repo_patch_failed", fmt.Sprintf("patch application failed for %s: %v", params.Path, err))
		}
		return
	}

	// 4. Success
	resultJSON, _ := json.Marshal(res)
	p.store.SaveResult(ctx, job.ID, resultJSON, nil)
	p.updateStatus(ctx, job.ID, "done")
	p.emitEvent(ctx, job.ID, "repo_patch_applied", resultJSON)
	if p.audit != nil {
		p.audit.LogEvent(job.ID, "repo_patch_applied", fmt.Sprintf("patch applied to %s", params.Path))
	}
}

func (p *WorkerPool) failJob(ctx context.Context, id string, err error) {
	log.Printf("Job %s failed: %v", id, err)
	p.updateStatus(ctx, id, "error")
	errJSON, _ := json.Marshal(map[string]string{"message": err.Error()})
	p.store.SaveResult(ctx, id, nil, errJSON)
}

func (p *WorkerPool) updateStatus(ctx context.Context, id, status string) {
	p.store.UpdateStatus(ctx, id, status)
	payload, _ := json.Marshal(map[string]interface{}{
		"id":    id,
		"state": status,
		"ts":    time.Now().Format(time.RFC3339),
	})
	p.emitEvent(ctx, id, "status", payload)
}

func (p *WorkerPool) emitEvent(ctx context.Context, id, eventType string, payload []byte) {
	p.store.AppendEvent(ctx, id, eventType, payload)
	select {
	case p.events <- RequestEvent{RequestID: id, Type: eventType, Payload: payload}:
	default:
		// Drop if channel full to prevent blocking workers
	}
}

func (p *WorkerPool) Stop() {
	close(p.jobs)
	p.wg.Wait()
}
