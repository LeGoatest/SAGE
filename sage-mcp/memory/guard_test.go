package memory

import (
	"encoding/json"
	"testing"
)

func TestCleanseJSON(t *testing.T) {
	t.Run("Redaction", func(t *testing.T) {
		payload := []byte(`{"id": 123, "token": "secret-123", "nested": {"password": "pwd"}, "safe": "value"}`)
		cleansed := CleanseJSON(payload)

		var data map[string]interface{}
		json.Unmarshal(cleansed, &data)

		if data["token"] != "REDACTED" {
			t.Errorf("token not redacted: %v", data["token"])
		}
		if data["nested"].(map[string]interface{})["password"] != "REDACTED" {
			t.Errorf("nested password not redacted")
		}
		if data["safe"] != "value" {
			t.Errorf("safe value altered: %v", data["safe"])
		}
	})

	t.Run("Truncation", func(t *testing.T) {
		// Create payload > 64KB
		largeData := make(map[string]string)
		for i := 0; i < 2000; i++ {
			largeData[string(rune(i))] = "some long string value that repeats"
		}
		payload, _ := json.Marshal(largeData)

		cleansed := CleanseJSON(payload)

		var wrapper map[string]interface{}
		json.Unmarshal(cleansed, &wrapper)

		if wrapper["truncated"] != true {
			t.Errorf("large payload not truncated")
		}
		if _, ok := wrapper["sha256"]; !ok {
			t.Errorf("missing sha256 in truncated payload")
		}
	})
}
