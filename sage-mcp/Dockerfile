# Multi-stage build for SAGE MCP
FROM golang:1.24-alpine AS builder

# Install build dependencies for CGO and sqlite-vec
RUN apk add --no-cache gcc musl-dev sqlite-dev git

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .

# Build with CGO enabled for sqlite-vec
ENV CGO_ENABLED=1
RUN go build -o sage-mcp .

# Runtime image
FROM alpine:3.19

# Install Python 3, patch utility, and dependencies for governance validator
RUN apk add --no-cache python3 py3-pip sqlite-libs ca-certificates patch

# Install Python packages required by .governance/
RUN pip install --break-system-packages PyYAML jsonschema

WORKDIR /app
COPY --from=builder /app/sage-mcp .
COPY memory/schema.sql memory/

# Data volume
VOLUME /data

EXPOSE 8080

CMD ["./sage-mcp"]
