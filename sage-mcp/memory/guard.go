package memory

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"strings"
)

const (
	MaxJSONSize    = 64 * 1024 // 64KB
	TruncationSize = 8 * 1024  // 8KB
)

var sensitiveKeys = []string{
	"token", "auth", "password", "secret", "api_key", "apikey",
}

// CleanseJSON processes a JSON payload for safe storage.
// It redacts sensitive keys and truncates large payloads.
func CleanseJSON(payload []byte) []byte {
	if len(payload) == 0 {
		return payload
	}

	// 1. Redact secrets
	cleansed := redactSecrets(payload)

	// 2. Truncate if still too large
	if len(cleansed) > MaxJSONSize {
		return truncateJSON(cleansed)
	}

	return cleansed
}

func redactSecrets(payload []byte) []byte {
	var data interface{}
	if err := json.Unmarshal(payload, &data); err != nil {
		return payload // Return as-is if not valid JSON
	}

	redactRecursive(data)

	result, err := json.Marshal(data)
	if err != nil {
		return payload
	}
	return result
}

func redactRecursive(data interface{}) {
	switch v := data.(type) {
	case map[string]interface{}:
		for key, val := range v {
			if isSensitive(key) {
				v[key] = "REDACTED"
			} else {
				redactRecursive(val)
			}
		}
	case []interface{}:
		for _, item := range v {
			redactRecursive(item)
		}
	}
}

func isSensitive(key string) bool {
	k := strings.ToLower(key)
	for _, s := range sensitiveKeys {
		if strings.Contains(k, s) {
			return true
		}
	}
	return false
}

func truncateJSON(payload []byte) []byte {
	hash := sha256.Sum256(payload)
	hashStr := hex.EncodeToString(hash[:])

	prefix := payload
	if len(payload) > TruncationSize {
		prefix = payload[:TruncationSize]
	}

	wrapper := map[string]interface{}{
		"truncated": true,
		"sha256":    hashStr,
		"size":      len(payload),
		"prefix":    string(prefix),
	}

	result, _ := json.Marshal(wrapper)
	return result
}
