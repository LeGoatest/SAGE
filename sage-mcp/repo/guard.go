package repo

import (
	"fmt"
	"path/filepath"
	"strings"
)

// ProtectedZones defines the standard SAGE protection boundaries.
var ProtectedZones = []string{
	"canon/",
	".docs/",
	".governance/",
	".github/",
	"Jules/",
	"tools/",
}

// CheckWritePermission enforces SAGE protection gates for write operations.
func CheckWritePermission(relPath, taskGroup string) error {
	cleaned := filepath.Clean(relPath)

	// Check if path is within a protected zone
	isProtected := false
	for _, zone := range ProtectedZones {
		if strings.HasPrefix(cleaned, zone) || cleaned == strings.TrimSuffix(zone, "/") {
			isProtected = true
			break
		}
	}

	if !isProtected {
		return nil
	}

	// Governance bypass for tools/
	if strings.HasPrefix(cleaned, "tools/") {
		if taskGroup == "GOVERNANCE" {
			return nil
		}
		return fmt.Errorf("write to tools/ requires task_group=GOVERNANCE")
	}

	// Infrastructure bypass for .github/workflows/
	if strings.HasPrefix(cleaned, ".github/workflows/") {
		if taskGroup == "INFRASTRUCTURE" {
			return nil
		}
		return fmt.Errorf("write to .github/workflows/ requires task_group=INFRASTRUCTURE")
	}

	// Absolute denial for all other protected zones
	return fmt.Errorf("write to protected zone %s is forbidden", cleaned)
}
