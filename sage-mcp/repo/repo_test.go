package repo

import (
	"os"
	"path/filepath"
	"testing"
)

func TestResolveSafePath(t *testing.T) {
	tmpDir := t.TempDir()
	repoRoot := tmpDir

	tests := []struct {
		name      string
		input     string
		expectErr bool
	}{
		{"Valid relative", "README.md", false},
		{"Valid subdirectory", "docs/canon/rules.yaml", false},
		{"Path traversal", "../../etc/passwd", true},
		{"Absolute path", "/etc/passwd", true},
		{"Valid dot", ".", false},
		{"Valid dot-slash", "./README.md", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			_, err := ResolveSafePath(repoRoot, tt.input)
			if (err != nil) != tt.expectErr {
				t.Errorf("ResolveSafePath(%s) error = %v, expectErr %v", tt.input, err, tt.expectErr)
			}
		})
	}
}

func TestCheckWritePermission(t *testing.T) {
	tests := []struct {
		path      string
		taskGroup string
		expectErr bool
	}{
		{"main.go", "FEATURE", false},
		{"canon/rules.yaml", "FEATURE", true},
		{"tools/validator.py", "FEATURE", true},
		{"tools/validator.py", "GOVERNANCE", false},
		{".github/workflows/ci.yml", "FEATURE", true},
		{".github/workflows/ci.yml", "INFRASTRUCTURE", false},
		{".docs/canon/rules.md", "GOVERNANCE", true}, // Absolute denial
	}

	for _, tt := range tests {
		t.Run(tt.path, func(t *testing.T) {
			err := CheckWritePermission(tt.path, tt.taskGroup)
			if (err != nil) != tt.expectErr {
				t.Errorf("CheckWritePermission(%s, %s) error = %v, expectErr %v", tt.path, tt.taskGroup, err, tt.expectErr)
			}
		})
	}
}

func TestRepoList(t *testing.T) {
	tmpDir := t.TempDir()
	os.WriteFile(filepath.Join(tmpDir, "file1.txt"), []byte("test"), 0644)
	os.Mkdir(filepath.Join(tmpDir, "subdir"), 0755)
	os.WriteFile(filepath.Join(tmpDir, "subdir/file2.txt"), []byte("test2"), 0644)

	res, err := List(tmpDir, ".", true, 100)
	if err != nil {
		t.Fatalf("List failed: %v", err)
	}

	if len(res.Entries) < 3 {
		t.Errorf("expected at least 3 entries, got %d", len(res.Entries))
	}
}

func TestRepoRead(t *testing.T) {
	tmpDir := t.TempDir()
	path := "test.txt"
	content := "hello world"
	os.WriteFile(filepath.Join(tmpDir, path), []byte(content), 0644)

	res, err := Read(tmpDir, path, 1024)
	if err != nil {
		t.Fatalf("Read failed: %v", err)
	}

	if res.Content != content {
		t.Errorf("expected content %q, got %q", content, res.Content)
	}
}

func TestRepoSearch(t *testing.T) {
	tmpDir := t.TempDir()
	path := "test.txt"
	os.WriteFile(filepath.Join(tmpDir, path), []byte("needle in a haystack"), 0644)

	res, err := Search(tmpDir, ".", "needle", nil, 10)
	if err != nil {
		t.Fatalf("Search failed: %v", err)
	}

	if len(res.Hits) != 1 {
		t.Errorf("expected 1 hit, got %d", len(res.Hits))
	}
}
