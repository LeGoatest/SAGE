package memory

import (
	"context"
	"crypto/sha256"
	"encoding/binary"
	"math"
)

// EmbedText generates a deterministic pseudo-embedding vector for a given text.
// In a production environment, this should be replaced with a call to a
// dedicated embedding model (e.g., OpenAI text-embedding-3-small).
func EmbedText(ctx context.Context, text string) ([]float32, error) {
	// For SAGE v5.0, we use a deterministic hash-based pseudo-embedding
	// to enable functional vector search testing without external dependencies.

	const dimensions = 1536
	vector := make([]float32, dimensions)

	// Use SHA256 of the text to seed the vector
	hash := sha256.Sum256([]byte(text))
	seed := binary.BigEndian.Uint64(hash[:8])

	// Very simple deterministic distribution
	for i := 0; i < dimensions; i++ {
		// Use a simple LCG-style generator seeded by hash
		seed = seed*6364136223846793005 + 1442695040888963407
		// Normalize to approx [-1, 1]
		vector[i] = float32(float64(int64(seed)) / float64(math.MaxInt64))
	}

	// Normalize the vector (L2 normalization)
	var sumSq float32
	for _, v := range vector {
		sumSq += v * v
	}
	norm := float32(math.Sqrt(float64(sumSq)))
	if norm > 0 {
		for i := range vector {
			vector[i] /= norm
		}
	}

	return vector, nil
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
