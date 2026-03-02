package memory

import (
	"context"
	"database/sql"
	_ "embed"
	"encoding/json"
	"fmt"
	"time"

	_ "github.com/mattn/go-sqlite3"
)

//go:embed schema.sql
var schemaSQL string

type SQLiteStore struct {
	db *sql.DB
}

func NewSQLiteStore(dbPath string) (*SQLiteStore, error) {
	db, err := sql.Open("sqlite3", dbPath+"?_journal=WAL")
	if err != nil {
		return nil, err
	}
	return &SQLiteStore{db: db}, nil
}

func (s *SQLiteStore) Init(ctx context.Context) error {
	// Load extension
	_, err := s.db.Exec("SELECT load_extension('vec0')")
	if err != nil {
		return fmt.Errorf("failed to load sqlite-vec: %w", err)
	}

	_, err = s.db.Exec(schemaSQL)
	return err
}

func (s *SQLiteStore) SaveRequest(ctx context.Context, id, method string, paramsJSON []byte) error {
	now := time.Now().Format(time.RFC3339)
	_, err := s.db.ExecContext(ctx,
		"INSERT INTO requests (id, method, params_json, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
		id, method, string(paramsJSON), "received", now, now)
	return err
}

func (s *SQLiteStore) UpdateStatus(ctx context.Context, id, status string) error {
	now := time.Now().Format(time.RFC3339)
	_, err := s.db.ExecContext(ctx,
		"UPDATE requests SET status = ?, updated_at = ? WHERE id = ?",
		status, now, id)
	return err
}

func (s *SQLiteStore) AppendEvent(ctx context.Context, requestID, eventType string, payloadJSON []byte) error {
	now := time.Now().Format(time.RFC3339)
	_, err := s.db.ExecContext(ctx,
		"INSERT INTO request_events (request_id, event_type, payload_json, created_at) VALUES (?, ?, ?, ?)",
		requestID, eventType, string(payloadJSON), now)
	return err
}

func (s *SQLiteStore) SaveResult(ctx context.Context, id string, resultJSON, errorJSON []byte) error {
	now := time.Now().Format(time.RFC3339)
	_, err := s.db.ExecContext(ctx,
		"UPDATE requests SET result_json = ?, error_json = ?, status = ?, updated_at = ? WHERE id = ?",
		string(resultJSON), string(errorJSON), "done", now, id)
	return err
}

func (s *SQLiteStore) SaveMemoryEntry(ctx context.Context, entry MemoryEntry) error {
	now := entry.CreatedAt.Format(time.RFC3339)
	_, err := s.db.ExecContext(ctx,
		"INSERT OR REPLACE INTO memory_entries (id, request_id, memory_type, content, metadata_json, importance, superseded, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
		entry.ID, entry.RequestID, entry.MemoryType, entry.Content, string(entry.MetadataJSON), entry.Importance, entry.Superseded, now)
	return err
}

func (s *SQLiteStore) VectorUpsert(ctx context.Context, vectorID string, embedding []float32) error {
	blob, err := json.Marshal(embedding)
	if err != nil {
		return err
	}
	_, err = s.db.ExecContext(ctx,
		"INSERT OR REPLACE INTO memory_vectors (id, embedding) VALUES (?, ?)",
		vectorID, blob)
	return err
}

func (s *SQLiteStore) LinkMemoryVector(ctx context.Context, memoryID, vectorID string) error {
	_, err := s.db.ExecContext(ctx,
		"INSERT OR REPLACE INTO memory_vector_links (memory_id, vector_id) VALUES (?, ?)",
		memoryID, vectorID)
	return err
}

func (s *SQLiteStore) VectorSearch(ctx context.Context, queryEmbedding []float32, limit int) ([]VectorHit, error) {
	blob, err := json.Marshal(queryEmbedding)
	if err != nil {
		return nil, err
	}

	query := `
		SELECT me.id, me.request_id, me.memory_type, me.content, me.metadata_json, me.importance, me.superseded, me.created_at, mv.distance
		FROM memory_vectors mv
		JOIN memory_vector_links l ON l.vector_id = mv.id
		JOIN memory_entries me ON me.id = l.memory_id
		WHERE mv.embedding MATCH ?
		  AND me.superseded = 0
		ORDER BY mv.distance ASC
		LIMIT ?;
	`

	rows, err := s.db.QueryContext(ctx, query, blob, limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var hits []VectorHit
	for rows.Next() {
		var h VectorHit
		var meta string
		var createdAt string
		err := rows.Scan(&h.Entry.ID, &h.Entry.RequestID, &h.Entry.MemoryType, &h.Entry.Content, &meta, &h.Entry.Importance, &h.Entry.Superseded, &createdAt, &h.Distance)
		if err != nil {
			return nil, err
		}
		h.Entry.MetadataJSON = json.RawMessage(meta)
		h.Entry.CreatedAt, _ = time.Parse(time.RFC3339, createdAt)
		hits = append(hits, h)
	}

	return hits, nil
}

func (s *SQLiteStore) GetBootstrapSnapshot(ctx context.Context, topic string, queryEmbedding []float32) (BootstrapSnapshot, error) {
	hits, err := s.VectorSearch(ctx, queryEmbedding, 50)
	if err != nil {
		return BootstrapSnapshot{}, err
	}

	snap := BootstrapSnapshot{Topic: topic}
	for _, hit := range hits {
		switch hit.Entry.MemoryType {
		case "constraint":
			snap.Constraints = append(snap.Constraints, hit.Entry)
		case "plan":
			snap.Plans = append(snap.Plans, hit.Entry)
		case "conclusion":
			snap.Conclusions = append(snap.Conclusions, hit.Entry)
		case "tool_result":
			snap.ToolResults = append(snap.ToolResults, hit.Entry)
		}
	}
	return snap, nil
}
