package repo

import (
	"fmt"
	"os"
	"os/exec"
)

type PatchResult struct {
	Applied bool   `json:"applied"`
	Path    string `json:"path"`
}

// ApplyPatch applies a unified diff to a file atomically.
// It uses the system 'patch' command if available, or returns an error.
func ApplyPatch(repoRoot, path, diff string, createIfMissing bool) (*PatchResult, error) {
	fullPath, err := ResolveSafePath(repoRoot, path)
	if err != nil {
		return nil, err
	}

	// 1. If not createIfMissing, ensure file exists
	if _, err := os.Stat(fullPath); os.IsNotExist(err) && !createIfMissing {
		return nil, fmt.Errorf("file does not exist and create_if_missing is false: %s", path)
	}

	// 2. Write diff to a temp file
	tmpDiff, err := os.CreateTemp("", "sage-patch-*.diff")
	if err != nil {
		return nil, fmt.Errorf("failed to create temp diff: %w", err)
	}
	defer os.Remove(tmpDiff.Name())
	if _, err := tmpDiff.WriteString(diff); err != nil {
		return nil, fmt.Errorf("failed to write temp diff: %w", err)
	}
	tmpDiff.Close()

	// 3. Apply patch using 'patch' command
	// patch -u <file> -i <diff>
	// We use -u for unified diff and -f to fail instead of asking questions
	cmd := exec.Command("patch", "-u", "-f", fullPath, "-i", tmpDiff.Name())
	if output, err := cmd.CombinedOutput(); err != nil {
		return &PatchResult{Applied: false, Path: path}, fmt.Errorf("patch failed: %s: %w", string(output), err)
	}

	return &PatchResult{Applied: true, Path: path}, nil
}
