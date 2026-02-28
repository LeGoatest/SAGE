#!/usr/bin/env bash
# SAGE | Injection Bootstrap Script
# This script injects SAGE governance into a project at runtime.
# It clones SAGE into .sage/ and verifies the pinned reference.

set -euo pipefail

SAGE_DIR=".sage"
SAGE_URL="${SAGE_URL:-https://github.com/LeGoatest/SAGE}"
SAGE_REF="${SAGE_REF:-}"

# Detect root if not in CWD
ROOT_DIR="$(pwd)"

echo "SAGE: Initiating injection bootstrap..."

if [ ! -d "$SAGE_DIR/.git" ]; then
  echo "SAGE: Cloning engine into $SAGE_DIR..."
  git clone --no-checkout "$SAGE_URL" "$SAGE_DIR"
fi

git -C "$SAGE_DIR" fetch --all --tags --quiet

# Resolve SAGE_REF from governance.yaml if not provided
if [ -z "${SAGE_REF}" ]; then
  if [ -f "governance.yaml" ]; then
    echo "SAGE: Resolving ref from governance.yaml..."
    SAGE_REF="$(awk '
      BEGIN {in_sage=0}
      /^[[:space:]]*sage:[[:space:]]*$/ {in_sage=1; next}
      in_sage && /^[[:space:]]*ref:[[:space:]]*/ {
        sub(/^[[:space:]]*ref:[[:space:]]*/, "", $0)
        gsub(/^[\"\047]|[\"\047][[:space:]]*$/, "", $0)
        print $0
        exit
      }
    ' governance.yaml)"
  fi
fi

if [ -z "${SAGE_REF}" ]; then
  echo "ERROR: Missing SAGE_REF and governance.yaml sage.ref"
  exit 1
fi

echo "SAGE: Checking out ref $SAGE_REF..."
git -C "$SAGE_DIR" rev-parse --verify "$SAGE_REF" >/dev/null 2>&1 \
  || { echo "ERROR: Invalid SAGE_REF: $SAGE_REF"; exit 1; }

git -C "$SAGE_DIR" checkout --detach "$SAGE_REF" --quiet
git -C "$SAGE_DIR" rev-parse HEAD > "$SAGE_DIR/.pinned_ref"

# Validate core components
test -d "$SAGE_DIR/canon"       || { echo "ERROR: Missing canon/ in SAGE"; exit 1; }
test -d "$SAGE_DIR/.docs"       || { echo "ERROR: Missing .docs/ in SAGE"; exit 1; }
test -d "$SAGE_DIR/.governance" || { echo "ERROR: Missing .governance/ in SAGE"; exit 1; }

# Initialize .jtasks if missing
if [ ! -d ".jtasks" ]; then
  echo "SAGE: Initializing .jtasks/ from template..."
  mkdir -p .jtasks/_template
  cp -r "$SAGE_DIR"/.jtasks/_template/* .jtasks/_template/
fi

echo "SAGE: Injection complete."
echo "Pinned SHA: $(cat "$SAGE_DIR/.pinned_ref")"
echo "Run 'bash $SAGE_DIR/tools/sage-check.sh' to verify."
