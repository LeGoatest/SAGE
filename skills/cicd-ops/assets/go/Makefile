.PHONY: fmt tidy test lint ci

fmt:
	gofmt -w .

tidy:
	go mod tidy

test:
	go test ./...

lint:
	golangci-lint run --timeout=5m

ci: fmt tidy test lint
