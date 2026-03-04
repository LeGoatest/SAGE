#!/usr/bin/env bash
set -euo pipefail

# SAGE Size Guard
# Monitors the size of state and event logs to prevent Git bloat.

STATE_DIR=".sage/state"
EVENTS_DIR=".sage/events"

DB_LIMIT_MB=100
JSONL_LIMIT_MB=10

EXIT_CODE=0

echo "--- SAGE Size Guard ---"

check_size() {
    local file=$1
    local limit_mb=$2

    if [[ ! -f "$file" ]]; then
        echo "INFO: $file not present."
        return
    fi

    size_kb=$(du -k "$file" | cut -f1)
    size_mb=$((size_kb / 1024))

    if [[ $size_mb -gt $limit_mb ]]; then
        echo "❌ FAIL: $file is ${size_mb}MB (Limit: ${limit_mb}MB)"
        EXIT_CODE=1
    else
        echo "✅ PASS: $file is ${size_mb}MB (Limit: ${limit_mb}MB)"
    fi
}

check_size "$STATE_DIR/sage.db" "$DB_LIMIT_MB"
check_size "$EVENTS_DIR/session.jsonl" "$JSONL_LIMIT_MB"

if [[ $EXIT_CODE -ne 0 ]]; then
    echo "ERROR: State size limits exceeded. Vacuum the database or rotate session logs."
fi

exit $EXIT_CODE
