package memory

import (
	"context"
	"encoding/json"
	"time"
)

type MemoryEntry struct {
	ID           string          `json:"id"`
	RequestID    string          `json:"request_id,omitempty"`
	MemoryType   string          `json:"memory_type"` // constraint|plan|conclusion|observation|tool_result
	Content      string          `json:"content"`
	MetadataJSON json.RawMessage `json:"metadata_json,omitempty"`
	Importance   float64         `json:"importance"`
	Superseded   int             `json:"superseded"`
	CreatedAt    time.Time       `json:"created_at"`
}

type VectorHit struct {
	Entry    MemoryEntry `json:"entry"`
	Distance float64     `json:"distance"`
	Score    float64     `json:"score"`
}

type BootstrapSnapshot struct {
	Topic       string        `json:"topic"`
	Constraints []MemoryEntry `json:"constraints"`
	Plans       []MemoryEntry `json:"plans"`
	Conclusions []MemoryEntry `json:"conclusions"`
	ToolResults []MemoryEntry `json:"tool_results"`
}

type MemoryStore interface {
	Init(ctx context.Context) error
	SaveRequest(ctx context.Context, id, method string, paramsJSON []byte) error
	UpdateStatus(ctx context.Context, id, status string) error
	AppendEvent(ctx context.Context, requestID, eventType string, payloadJSON []byte) error
	SaveResult(ctx context.Context, id string, resultJSON, errorJSON []byte) error

	SaveMemoryEntry(ctx context.Context, entry MemoryEntry) error
	VectorUpsert(ctx context.Context, vectorID string, embedding []float32) error
	LinkMemoryVector(ctx context.Context, memoryID, vectorID string) error
	VectorSearch(ctx context.Context, queryEmbedding []float32, limit int) ([]VectorHit, error)

	GetBootstrapSnapshot(ctx context.Context, topic string, queryEmbedding []float32) (BootstrapSnapshot, error)
}
