package repo

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

type SearchResult struct {
	Hits []Hit `json:"hits"`
}

type Hit struct {
	Path    string `json:"path"`
	Line    int    `json:"line"`
	Snippet string `json:"snippet"`
}

// Search implements the repo.search method logic using pure Go walk + scanning.
func Search(repoRoot, dir, query string, globs []string, maxHits int) (*SearchResult, error) {
	fullDir, err := ResolveSafePath(repoRoot, dir)
	if err != nil {
		return nil, err
	}

	var hits []Hit

	err = filepath.WalkDir(fullDir, func(path string, d os.DirEntry, err error) error {
		if err != nil {
			return err
		}

		if len(hits) >= maxHits {
			return filepath.SkipDir
		}

		if d.IsDir() {
			// Skip hidden dirs
			if strings.HasPrefix(d.Name(), ".") && d.Name() != "." {
				return filepath.SkipDir
			}
			return nil
		}

		// Match globs
		match := false
		if len(globs) == 0 {
			match = true
		} else {
			for _, glob := range globs {
				if m, _ := filepath.Match(glob, d.Name()); m {
					match = true
					break
				}
			}
		}

		if !match {
			return nil
		}

		// Search within file
		f, err := os.Open(path)
		if err != nil {
			return nil
		}
		defer f.Close()

		rel, _ := filepath.Rel(repoRoot, path)
		scanner := bufio.NewScanner(f)
		lineNum := 1
		for scanner.Scan() {
			line := scanner.Text()
			if strings.Contains(line, query) {
				hits = append(hits, Hit{
					Path:    rel,
					Line:    lineNum,
					Snippet: strings.TrimSpace(line),
				})
				if len(hits) >= maxHits {
					return nil
				}
			}
			lineNum++
		}

		return nil
	})

	if err != nil {
		return nil, fmt.Errorf("failed to search: %w", err)
	}

	return &SearchResult{Hits: hits}, nil
}
