package config

import (
	"os"
	"strconv"
)

type Config struct {
	Addr              string
	Token             string
	Workers           int
	DataDir           string
	CorsOrigins       string
	MaxContextTokens  int
	LambdaHours       float64
}

func Load() *Config {
	return &Config{
		Addr:             getEnv("SAGE_MCP_ADDR", ":8080"),
		Token:            os.Getenv("SAGE_MCP_TOKEN"),
		Workers:          getEnvInt("SAGE_MCP_WORKERS", 2),
		DataDir:          getEnv("SAGE_MCP_DATA_DIR", "/data"),
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
