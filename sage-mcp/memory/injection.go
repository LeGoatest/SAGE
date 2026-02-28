package memory

import (
	"context"
	"math"
	"sort"
	"strings"
	"time"
)

type InjectionOptions struct {
	LambdaHours      float64
	MaxContextTokens int
}

func PrepareInjectedContext(ctx context.Context, store MemoryStore, queryEmbedding []float32, opts InjectionOptions) (string, error) {
	hits, err := store.VectorSearch(ctx, queryEmbedding, 20)
	if err != nil {
		return "", err
	}

	// Score hits
	now := time.Now()
	for i := range hits {
		ageHours := now.Sub(hits[i].Entry.CreatedAt).Hours()
		recencyDecay := math.Exp(-opts.LambdaHours * ageHours)

		hits[i].Score = (1/(1+hits[i].Distance))*0.5 + hits[i].Entry.Importance*0.3 + recencyDecay*0.2
	}

	// Sort by composite score
	sort.Slice(hits, func(i, j int) bool {
		return hits[i].Score > hits[j].Score
	})

	// Bucket and Cap
	caps := map[string]int{
		"plan":        3,
		"constraint":  5,
		"tool_result": 3,
		"conclusion":  5,
		"observation": 4,
	}
	counts := make(map[string]int)

	var sections = struct {
		Constraints []string
		Plans       []string
		Conclusions []string
		ToolResults []string
	}{}

	for _, hit := range hits {
		mType := hit.Entry.MemoryType
		if counts[mType] >= caps[mType] {
			continue
		}
		counts[mType]++

		switch mType {
		case "constraint":
			sections.Constraints = append(sections.Constraints, hit.Entry.Content)
		case "plan":
			sections.Plans = append(sections.Plans, hit.Entry.Content)
		case "conclusion":
			sections.Conclusions = append(sections.Conclusions, hit.Entry.Content)
		case "tool_result":
			sections.ToolResults = append(sections.ToolResults, hit.Entry.Content)
		}
	}

	// Build string
	var sb strings.Builder
	sb.WriteString("[RELEVANT MEMORY SNAPSHOT]\n")

	if len(sections.Constraints) > 0 {
		sb.WriteString("Active Constraints:\n- ")
		sb.WriteString(strings.Join(sections.Constraints, "\n- "))
		sb.WriteString("\n")
	}
	if len(sections.Plans) > 0 {
		sb.WriteString("Recent Plans:\n- ")
		sb.WriteString(strings.Join(sections.Plans, "\n- "))
		sb.WriteString("\n")
	}
	if len(sections.Conclusions) > 0 {
		sb.WriteString("Prior Conclusions:\n- ")
		sb.WriteString(strings.Join(sections.Conclusions, "\n- "))
		sb.WriteString("\n")
	}
	if len(sections.ToolResults) > 0 {
		sb.WriteString("Recent Tool Results:\n- ")
		sb.WriteString(strings.Join(sections.ToolResults, "\n- "))
		sb.WriteString("\n")
	}

	// Simple token approximation (4 chars per token)
	result := sb.String()
	if len(result)/4 > opts.MaxContextTokens {
		// Truncate if necessary (very basic implementation)
		limit := opts.MaxContextTokens * 4
		if limit < len(result) {
			result = result[:limit] + "... [truncated]"
		}
	}

	return result, nil
}
