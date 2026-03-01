package queue

import (
	"context"
	"encoding/json"
	"sync"
	"time"

	"sage-mcp/adapter"
	"sage-mcp/memory"
)

type WorkerPool struct {
	jobs    chan Job
	engine  adapter.Engine
	store   memory.MemoryStore
	wg      sync.WaitGroup
	workers int

	// Simple event hub for SSE
	events chan RequestEvent
}

type RequestEvent struct {
	RequestID string
	Type      string // status|output
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
