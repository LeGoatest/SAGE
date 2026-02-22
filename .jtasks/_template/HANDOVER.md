# Semantic Handover (Multi-Model Resilience)

This document ensures continuity of execution across context resets or model changes.
**Mandatory for every incomplete execution.**

---

## 1. Context Snapshot
- **Task Group:** [e.g., development]
- **Spec State:** [e.g., In-progress / Design Approved]
- **Target Repository:** [repo name/path]
- **Governance Binding File:** `governance.yaml`
- **SAGT Repo:** https://github.com/LeGoatest/Sovereign-agent-template
- **Pinned Canon Ref (commit SHA):** [sha]
- **Resolved Canon Root (Jules cache):** [jules_cache/sagt/checkouts/<ref>/]
- **Current Model Identity:** [e.g., Jules]

## 2. Execution State
- **Active Task ID:** [e.g., T4]
- **Completed Tasks:**
  - [ID] - [Summary]
- **Pending Tasks:**
  - [ID] - [Summary]

## 3. Risks & Refusals
- **Last Refusal Trigger:** [None / Reason]
- **Architectural Risks Detected:**
  - [Risk] - [Canonical Reference]

## 4. Canonical References Used
List the canon references used during execution in this format:

- `SAGT@<ref>:<path>#<anchor>` — [Why it mattered]

## 5. Continuity Instruction
*Provide the exact next step for the successor model/context.*
> [Next step]
