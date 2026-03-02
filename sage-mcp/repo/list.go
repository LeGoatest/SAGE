package repo

import (
	"fmt"
	"os"
	"path/filepath"
	"time"
)

type ListResult struct {
	Entries []Entry `json:"entries"`
}

type Entry struct {
	Path    string    `json:"path"`
	Type    string    `json:"type"`
	Size    int64     `json:"size"`
	ModTime time.Time `json:"mod_time"`
}

// List implements the repo.list method logic.
func List(repoRoot, dir string, recursive bool, maxItems int) (*ListResult, error) {
	fullDir, err := ResolveSafePath(repoRoot, dir)
	if err != nil {
		return nil, err
	}

	var entries []Entry
	count := 0

	err = filepath.WalkDir(fullDir, func(path string, d os.DirEntry, err error) error {
		if err != nil {
			return err
		}

		if count >= maxItems {
			return filepath.SkipDir
		}

		// Skip the root dir itself
		if path == fullDir {
			return nil
		}

		rel, err := filepath.Rel(repoRoot, path)
		if err != nil {
			return err
		}

		info, err := d.Info()
		if err != nil {
			return err
		}

		entryType := "file"
		if d.IsDir() {
			entryType = "dir"
		}

		entries = append(entries, Entry{
			Path:    rel,
			Type:    entryType,
			Size:    info.Size(),
			ModTime: info.ModTime(),
		})

		count++

		if !recursive && d.IsDir() {
			return filepath.SkipDir
		}

		return nil
	})

	if err != nil {
		return nil, fmt.Errorf("failed to list directory: %w", err)
	}

	return &ListResult{Entries: entries}, nil
}
