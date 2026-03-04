package repo

import (
	"fmt"
	"io"
	"net/http"
	"os"
)

type ReadResult struct {
	Path      string `json:"path"`
	Content   string `json:"content,omitempty"`
	Binary    bool   `json:"binary,omitempty"`
	Truncated bool   `json:"truncated,omitempty"`
}

// Read implements the repo.read method logic.
func Read(repoRoot, path string, maxBytes int) (*ReadResult, error) {
	fullPath, err := ResolveSafePath(repoRoot, path)
	if err != nil {
		return nil, err
	}

	f, err := os.Open(fullPath)
	if err != nil {
		return nil, fmt.Errorf("failed to open file: %w", err)
	}
	defer f.Close()

	buf := make([]byte, maxBytes)
	n, err := f.Read(buf) // Use Read instead of ReadFull
	if err != nil && err != io.EOF {
		return nil, fmt.Errorf("failed to read file: %w", err)
	}

	content := buf[:n]

	// Check for binary
	contentType := http.DetectContentType(content)
	if !isText(contentType) && n > 0 {
		return &ReadResult{Path: path, Binary: true}, nil
	}

	// Check if truncated
	truncated := false
	if n == maxBytes {
		// Try to read one more byte
		oneMore := make([]byte, 1)
		nn, _ := f.Read(oneMore)
		if nn > 0 {
			truncated = true
		}
	}

	return &ReadResult{
		Path:      path,
		Content:   string(content),
		Truncated: truncated,
	}, nil
}

func isText(contentType string) bool {
	return contentType == "text/plain" ||
		contentType == "text/html" ||
		contentType == "text/xml" ||
		contentType == "application/json" ||
		contentType == "application/javascript" ||
		contentType == "application/x-javascript" ||
		contentType == "text/css" ||
		contentType == "text/csv" ||
		contentType == "application/xml" ||
		contentType == "text/plain; charset=utf-8"
}
