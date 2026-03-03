package config

import (
	"os"
	"path/filepath"
	"strconv"
)

type Config struct {
	Addr             string
	Token            string
	Workers          int
	DataDir          string
	EventsDir        string
	CorsOrigins      string
	MaxContextTokens int
	LambdaHours      float64
}

func Load() *Config {
	// Standardize DataDir:
	// 1. SAGE_DATA_DIR (preferred)
	// 2. SAGE_MCP_DATA_DIR (legacy)
	// 3. Default: .sage/state (repo context)
	dataDir := getEnv("SAGE_DATA_DIR", getEnv("SAGE_MCP_DATA_DIR", ".sage/state"))

	// EventsDir defaults to .sage/events in the same root
	eventsDir := getEnv("SAGE_EVENTS_DIR", filepath.Join(filepath.Dir(dataDir), "events"))

	return &Config{
		Addr:             getEnv("SAGE_MCP_ADDR", ":8080"),
		Token:            os.Getenv("SAGE_MCP_TOKEN"),
		Workers:          getEnvInt("SAGE_MCP_WORKERS", 2),
		DataDir:          dataDir,
		EventsDir:        eventsDir,
		CorsOrigins:      getEnv("SAGE_MCP_CORS_ORIGINS", "*"),
		MaxContextTokens: getEnvInt("SAGE_MCP_MAX_CONTEXT_TOKENS", 1200),
		LambdaHours:      getEnvFloat("SAGE_MCP_LAMBDA_HOURS", 0.03),
	}
}

func getEnv(key, fallback string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	return fallback
}

func getEnvInt(key string, fallback int) int {
	if value, ok := os.LookupEnv(key); ok {
		if i, err := strconv.Atoi(value); err == nil {
			return i
		}
	}
	return fallback
}

func getEnvFloat(key string, fallback float64) float64 {
	if value, ok := os.LookupEnv(key); ok {
		if f, err := strconv.ParseFloat(value, 64); err == nil {
			return f
		}
	}
	return fallback
}
