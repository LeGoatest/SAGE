package memory

import (
	"context"
	"math"
)

// In a real implementation, this would call an LLM embedding service.
// For this scaffolding, we provide a placeholder.
func EmbedText(ctx context.Context, text string) ([]float32, error) {
	// Dummy embedding: just return a zero vector of size 1536
	return make([]float32, 1536), nil
}

func CosineSimilarity(a, b []float32) float32 {
	var dot, sumA, sumB float32
	for i := range a {
		dot += a[i] * b[i]
		sumA += a[i] * a[i]
		sumB += b[i] * b[i]
	}
	if sumA == 0 || sumB == 0 {
		return 0
	}
	return dot / (float32(math.Sqrt(float64(sumA))) * float32(math.Sqrt(float64(sumB))))
}
