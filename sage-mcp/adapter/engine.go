package adapter

import (
	"bufio"
	"context"
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
)

type Engine interface {
	Execute(ctx context.Context, method string, params json.RawMessage, injectedContext string, emit func(string)) (json.RawMessage, error)
}

type SAGEAdapter struct{}

func (a *SAGEAdapter) Execute(ctx context.Context, method string, params json.RawMessage, injectedContext string, emit func(string)) (json.RawMessage, error) {
	// SAGE v5.0 is implemented as a Python governance engine.
	// This adapter executes the engine and captures output chunks.

	emit(fmt.Sprintf("SAGE: Starting execution for method: %s\n", method))

	// Set SAGE_INJECTED_CONTEXT so the Python engine can pick it up
	// In a real deployment, we might write this to a temporary file instead.
	os.Setenv("SAGE_INJECTED_CONTEXT", injectedContext)

	// Determine command based on method
	var cmd *exec.Cmd
	switch method {
	case "validate":
		cmd = exec.CommandContext(ctx, "python3", ".governance/validator.py")
	case "compile":
		cmd = exec.CommandContext(ctx, "bash", "canon-compile.sh")
	default:
		// Default to running the full validator
		cmd = exec.CommandContext(ctx, "python3", ".governance/validator.py")
	}

	stdout, err := cmd.StdoutPipe()
	if err != nil {
		return nil, fmt.Errorf("failed to get stdout pipe: %w", err)
	}
	stderr, err := cmd.StderrPipe()
	if err != nil {
		return nil, fmt.Errorf("failed to get stderr pipe: %w", err)
	}

	if err := cmd.Start(); err != nil {
		return nil, fmt.Errorf("failed to start SAGE engine: %w", err)
	}

	// Stream output back to the user
	go func() {
		scanner := bufio.NewScanner(stdout)
		for scanner.Scan() {
			emit(scanner.Text() + "\n")
		}
	}()
	go func() {
		scanner := bufio.NewScanner(stderr)
		for scanner.Scan() {
			emit("ERR: " + scanner.Text() + "\n")
		}
	}()

	if err := cmd.Wait(); err != nil {
		return nil, fmt.Errorf("SAGE engine execution failed: %w", err)
	}

	result := map[string]interface{}{
		"method": method,
		"status": "success",
		"data":   "SAGE execution completed successfully",
	}

	resJSON, _ := json.Marshal(result)
	return resJSON, nil
}
