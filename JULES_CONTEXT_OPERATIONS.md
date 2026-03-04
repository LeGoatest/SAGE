# Jules Internal Operations: Context & Memory

This document explains the internal mechanisms Jules (this agent) uses to manage the Context Window and Persistent Memory within the Sovereign Agent Governance Engine (SAGE) v5.0 framework.

## 1. The Context Window

The **Context Window** is the transient space where Jules processes current interaction data, repository state, and governance rules. Because this space is finite, SAGE uses deterministic resolution and pruning to ensure critical information is never lost.

### 1.1 Context Resolution
At the start of every turn or session, a **Context Builder** (internal logic) assembles the window by resolving the governance graph defined in `canon/graph.yaml`. The resolution order is:
1. **Core Governance:** Axioms and Invariants from the Narrative Constitution (`.docs/`).
2. **Architectural Rules:** Structural boundaries defined in `canon/ARCHITECTURE_RULES.md`.
3. **Task Group Definitions:** Metadata from `canon/task_groups.yaml` to set mode permissions.
4. **Current Session State:** Data from the active `.jtasks/` directory and `HANDOVER.md`.

### 1.2 Context Pruning Priority
When the token limit of the context window is reached, a **Context Pruner** automatically removes information based on a strict priority hierarchy. This ensures the agent remains governed even in long sessions.

**Pruning Order (Last to be Removed):**
1. **Architecture Rules:** (Highest Priority - Never Pruned)
2. **Task Groups:** (Required for mode discipline)
3. **Canon Rules:** (Machine-enforceable logic)
4. **Skill Metadata:** (Optional helper instructions)
5. **Session Logs/History:** (Lowest Priority - Pruned First)

---

## 2. Context Memory

SAGE distinguishes between **Transient Session State** and **Persistent Memory Recording**.

### 2.1 Transient Session State
This is the "short-term memory" stored in the `.jtasks/` folder and `state.yaml`. It tracks the progress of the current task. If a session is interrupted, Jules uses the `HANDOVER.md` file as a "Deterministic Session Rehydration Artifact" to restore this state in the next turn.

### 2.2 Persistent Memory Recording
The **Memories** seen at the start of a prompt are "long-term" facts or repository-specific instructions.
- **Recording:** Jules uses the `initiate_memory_recording` tool to commit significant findings, patterns, or user preferences to this permanent layer.
- **Authority:** These memories provide historical context and intent ("the why") but do not override the active code state ("the what") or the Canonical Rules.

---

## 3. Operational Modes

Jules operates in specific modes to prevent "context leakage" or unauthorized changes:
- **Deep Governance Mode:** Used for architectural validation. No file edits are allowed.
- **Spec Mode:** Used for planning. Produces `.jtasks/` artifacts.
- **Execution Mode:** Used for implementation. Restricted to the scope of the approved `tasks.md`.

---
*This document is for informational purposes regarding Jules' internal operating environment.*
