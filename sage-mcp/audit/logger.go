package audit

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sync"
	"time"
)

type AuditEntry struct {
	Timestamp string          `json:"ts"`
	RequestID string          `json:"id"`
	Type      string          `json:"type"` // request|event|result|error
	Method    string          `json:"method,omitempty"`
	Summary   string          `json:"summary"`
	Hashes    map[string]string `json:"hashes,omitempty"`
	Metadata  json.RawMessage `json:"metadata,omitempty"`
}

type Logger struct {
	mu       sync.Mutex
	filePath string
}

func NewLogger(eventsDir string) (*Logger, error) {
	path := filepath.Join(eventsDir, "session.jsonl")
	return &Logger{
		filePath: path,
	}, nil
}

func (l *Logger) Log(entry AuditEntry) error {
	if entry.Timestamp == "" {
		entry.Timestamp = time.Now().Format(time.RFC3339)
	}

	line, err := json.Marshal(entry)
	if err != nil {
		return fmt.Errorf("failed to marshal audit entry: %w", err)
	}

	l.mu.Lock()
	defer l.mu.Unlock()

	f, err := os.OpenFile(l.filePath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return fmt.Errorf("failed to open audit log: %w", err)
	}
	defer f.Close()

	if _, err := f.Write(append(line, '\n')); err != nil {
		return fmt.Errorf("failed to write audit entry: %w", err)
	}

	return nil
}

// LogRequest logs a summary of an incoming request.
func (l *Logger) LogRequest(id, method string, summary string) {
	l.Log(AuditEntry{
		RequestID: id,
		Type:      "request",
		Method:    method,
		Summary:   summary,
	})
}

// LogEvent logs a summary of an internal event.
func (l *Logger) LogEvent(requestID, eventType, summary string) {
	l.Log(AuditEntry{
		RequestID: requestID,
		Type:      "event",
		Method:    eventType,
		Summary:   summary,
	})
}
