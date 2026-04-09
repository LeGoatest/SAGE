# How Google Jules Handles Context & Memory

This document explains the integrated operational logic Jules uses to manage the Context Window and Context Memory during an active session.

## 1. The Session Lifecycle (The "Turn" Loop)

Every time you send a message, Jules goes through a "Turn Lifecycle" that combines native platform behavior with governance enforcement.

### 1.1 Context Assembly
At the start of every turn, the underlying platform assembles a **Context Bundle**.
- **The Payload:** It includes the System Instructions, the full sequence of previous messages/responses (History), and your new message.
- **Jules's Injection:** Before processing, Jules injects active Governance artifacts (Canon rules, Task Groups, and state from `.jtasks/`) into the prompt. This ensures that Jules "remembers" the current plan and constraints even if they weren't in the immediate chat history.

---

## 2. Managing the Context Window "During a Session"

As a session progresses, the context window fills with tokens from conversation and tool outputs (like large file reads).

### 2.1 Saturation and Pruning
When the total tokens approach the limit (e.g., 1M+ tokens), Jules must manage what stays in the active "thinking space."
- **Platform Level:** The platform may truncate the oldest parts of the chat history.
- **Agent Level (Pruning):** Jules uses a **Pruning Hierarchy** to decide what to protect. If space is tight, Jules will prioritize keeping **Architecture Rules** and **Active Task State** over older conversation logs or helper skill documentation.

### 2.2 Token-Saving Strategies
During long sessions, Jules handles the window by:
- **Targeted Reading:** Only reading specific parts of files rather than whole directories.
- **Summarization:** Replacing long tool outputs with concise summaries in the conversation history.

---

## 3. Context Memory: Transient vs. Persistent

Jules uses two distinct types of memory to maintain continuity.

### 3.1 Transient "Working" Memory (Tokens)
- **What it is:** The actual tokens in the current context window.
- **Behavior:** This is incredibly high-detail but volatile. If the context window is reset or the limit is reached, this information can be "forgotten" or truncated.
- **Usage:** Used for immediate code analysis, logic execution, and following the flow of the current conversation.

### 3.2 Persistent "Instructional" Memory (Files & Recordings)
- **What it is:** Information stored on disk in the repository or in the "Memory" blocks at the start of a prompt.
- **Tools:** Jules uses the `initiate_memory_recording` tool to save critical patterns or preferences.
- **State Management:** The `.jtasks/state.yaml` and `HANDOVER.md` files act as "externalized memory." They ensure that if the transient context window is cleared, Jules can "rehydrate" the session by reading these files back into the window.

---

## 4. Summary of Integrated Handling

| Feature | Managed By | Purpose |
| :--- | :--- | :--- |
| **History Continuity** | Platform (Gemini) | Resubmits the full chat log every turn. |
| **Rule Enforcement** | SAGE Governance | Injects constraints into every turn's context. |
| **Window Management** | Jules (Pruning) | Ensures Architecture rules are never "forgotten." |
| **Long-term Recall** | Memory Recording | Saves cross-session facts to the repository. |

---
*This document defines the operational reality of Jules within the Google environment.*
