package repo

import (
	"fmt"
	"path/filepath"
	"strings"
)

// ResolveSafePath resolves a repository-relative path and ensures it does not
// escape the repository root. It rejects absolute paths and path traversal.
func ResolveSafePath(repoRoot, inputPath string) (string, error) {
	// 1. Clean the input path
	cleaned := filepath.Clean(inputPath)

	// 2. Reject absolute paths
	if filepath.IsAbs(cleaned) || strings.HasPrefix(cleaned, "/") {
		return "", fmt.Errorf("absolute paths are forbidden: %s", inputPath)
	}

	// 3. Reject path traversal
	if strings.HasPrefix(cleaned, "..") {
		return "", fmt.Errorf("path traversal is forbidden: %s", inputPath)
	}

	// 4. Resolve the full path
	fullPath := filepath.Join(repoRoot, cleaned)

	// 5. Final safety check: double-ensure it's under repoRoot
	absRepoRoot, err := filepath.Abs(repoRoot)
	if err != nil {
		return "", fmt.Errorf("failed to get absolute repo root: %w", err)
	}
	absFullPath, err := filepath.Abs(fullPath)
	if err != nil {
		return "", fmt.Errorf("failed to get absolute full path: %w", err)
	}

	if !strings.HasPrefix(absFullPath, absRepoRoot) {
		return "", fmt.Errorf("path escaped repository root: %s", inputPath)
	}

	return fullPath, nil
}
