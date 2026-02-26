#!/bin/bash

# sage-check.sh - SAGE Vibe Check CLI
# Informational only. Detects HITL markers, TODOs, and Refusals.

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}--- SAGE Vibe Check ---${NC}"

# Check for HITL markers
echo -e "\n${YELLOW}Checking for [AWAIT_HUMAN_VALIDATION]...${NC}"
HITL_COUNT=$(grep -r "\[AWAIT_HUMAN_VALIDATION\]" . --exclude-dir=".git" --exclude-dir="temp_v2" | wc -l)
if [ "$HITL_COUNT" -gt 0 ]; then
    echo -e "${RED}FOUND: $HITL_COUNT HITL markers detected.${NC}"
    grep -rn "\[AWAIT_HUMAN_VALIDATION\]" . --exclude-dir=".git" --exclude-dir="temp_v2"
else
    echo -e "${GREEN}CLEAN: No active HITL markers found.${NC}"
fi

# Check for TODOs
echo -e "\n${YELLOW}Checking for TODOs...${NC}"
TODO_COUNT=$(grep -ri "TODO" . --exclude-dir=".git" --exclude-dir="temp_v2" | wc -l)
if [ "$TODO_COUNT" -gt 0 ]; then
    echo -e "${YELLOW}FOUND: $TODO_COUNT TODOs detected.${NC}"
    grep -rin "TODO" . --exclude-dir=".git" --exclude-dir="temp_v2"
else
    echo -e "${GREEN}CLEAN: No TODOs found.${NC}"
fi

# Check for Refusals
echo -e "\n${YELLOW}Checking for Refusals (REFUSE)...${NC}"
REFUSE_COUNT=$(grep -ri "REFUSE" . --exclude-dir=".git" --exclude-dir="temp_v2" | wc -l)
if [ "$REFUSE_COUNT" -gt 0 ]; then
    echo -e "${YELLOW}FOUND: $REFUSE_COUNT Refusal markers detected.${NC}"
    grep -rin "REFUSE" . --exclude-dir=".git" --exclude-dir="temp_v2"
else
    echo -e "${GREEN}CLEAN: No Refusal markers found.${NC}"
fi

echo -e "\n${YELLOW}--- Check Complete ---${NC}"
