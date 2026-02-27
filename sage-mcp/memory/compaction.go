package memory

import (
	"context"
	"fmt"
	"time"

	"github.com/google/uuid"
)

func CompactMemory(ctx context.Context, store MemoryStore, requestID string, rawOutput string) error {
	// In a real implementation, this would call an LLM to summarize/distill.
	// For this scaffolding, we perform a deterministic distillation.

	distilled := fmt.Sprintf("Distilled output for request %s: %s", requestID, truncate(rawOutput, 100))

	entry := MemoryEntry{
		ID:         uuid.New().String(),
		RequestID:  requestID,
		MemoryType: "conclusion",
		Content:    distilled,
		Importance: 0.6,
		CreatedAt:  time.Now(),
	}

	// Duplicate Suppression
	embedding, _ := EmbedText(ctx, entry.Content)
	hits, _ := store.VectorSearch(ctx, embedding, 3)
	for _, hit := range hits {
		existingEmbedding, _ := EmbedText(ctx, hit.Entry.Content)
		if CosineSimilarity(embedding, existingEmbedding) >= 0.92 {
			// Merge/Skip
			fmt.Printf("Memory duplicate detected, skipping %s\n", entry.ID)
			return nil
		}
	}

	// Plan Supersession
	if entry.MemoryType == "plan" {
		// Mark older plans as superseded (simplified logic)
	}

	err := store.SaveMemoryEntry(ctx, entry)
	if err != nil {
		return err
	}

	return store.VectorUpsert(ctx, entry.ID, embedding)
}

func truncate(s string, n int) string {
	if len(s) <= n {
		return s
	}
	return s[:n] + "..."
}
