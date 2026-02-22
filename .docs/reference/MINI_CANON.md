# MINI CANON (Non-Canonical Convenience File)

> **DISCLAIMER:** MINI_CANON.md is not canonical; canon in /src prevails.
> This file is for token efficiency and quick reference only.

## 1. Absolute Precedence (Highest to Lowest)
1. src/canon/ARCHITECTURE_RULES.md
2. src/canon/SYSTEM_AXIOMS.md
3. src/reference/SAGT_OVERVIEW.md
4. src/canon/SECURITY_MODEL.md
... (Refer to src/canon/ARCHITECTURE_INDEX.md for full list)

## 2. Refusal Triggers
- Violation of any higher-precedence rule.
- Undocumented architectural changes.
- Ambiguous intent or task group.
- Missing spec approval.

## 3. Task Groups
- **architecture**: Changing system structure (Skills allowed: NO).
- **development**: Features, bugs, refactor (Skills allowed: YES).
- **operations**: Build, deploy, context pruning (Skills allowed: YES).
- **docs**: Writing, planning (Skills allowed: YES).
- **audit**: Compliance checking (Skills allowed: YES).

## 4. Spec-First Workflow
1. GAP_REPORT.md
2. requirements.md
3. design.md
4. tasks.md
5. Human Approval (HITL)

## 5. Global Constraints
- Escape inline backticks as `\\`.
- Go code must be `gofmt` clean.
- Break complex prompts into 5 simple steps.
- Use `[AWAIT_HUMAN_VALIDATION]` for halt points.
- Use ISO 8601 (YYYY-MM-DDTHH-MM-SS) for workspaces.
- Use `ENTER_DEEP_GOVERNANCE_MODE` for high-risk validation.
