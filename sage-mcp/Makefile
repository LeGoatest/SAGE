# Build commands for SAGE MCP

.PHONY: build clean docker-build

BINARY_NAME=sage-mcp

build:
	@echo "Building SAGE MCP..."
	cd .. && CGO_ENABLED=1 go build -o sage-mcp/$(BINARY_NAME) ./sage-mcp

clean:
	@echo "Cleaning up..."
	rm -f $(BINARY_NAME)

docker-build:
	@echo "Building Docker image..."
	docker build -t sage-mcp:latest .
