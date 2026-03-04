# LLM Platform Operations: Tokens & History

This document explains the native token management and history storage mechanisms of the underlying Large Language Model (LLM) platform, independent of any project-specific governance or frameworks.

## 1. Token Management

The platform operates on **tokens** rather than words or characters.

### 1.1 Tokenization
- **Process:** Every input (text, code, or images) is converted into numerical representations called tokens. On average, 1,000 tokens are equivalent to approximately 750 words.
- **Granularity:** Common words may be a single token, while rare words or complex code symbols are broken into multiple tokens.
- **Multimodal Tokens:** Images and other media also consume tokens within the window, often at a fixed rate per image or based on resolution.

### 1.2 The Context Window
- **Capacity:** The platform provides a large, fixed-size **context window** (e.g., 1 million to 2 million tokens). This represents the total amount of information the model can "see" and process at any single moment.
- **Composition:** The window is filled by:
    - **System Instructions:** The foundational rules and personality definitions.
    - **Tool Definitions:** Descriptions of the functions (tools) the model can call.
    - **Conversation History:** All previous user messages and model responses in the current session.
    - **Current Input:** The most recent message and any attached data.

---

## 2. History Storage & Retrieval

The platform maintains the continuity of the conversation through sequence-based history.

### 2.1 State-Free Processing
The model itself is technically "stateless." It does not "remember" previous interactions once a turn is finished. To maintain the illusion of memory, the platform stores the chat history and resubmits it in its entirety with every new prompt.

### 2.2 Re-Submission Flow
1. **User Sends Message:** The user provides a new prompt.
2. **History Packing:** The platform retrieves the log of all previous messages (User and Assistant) from the current session.
3. **Context Construction:** The platform bundles the System Instructions + History + New Message into a single massive prompt.
4. **Inference:** The LLM processes this entire bundle and generates a response.

### 2.3 Window Management
As the conversation grows, it consumes more of the context window.
- **Growth:** Every turn adds more tokens to the "History" section of the next turn's bundle.
- **Saturation:** If the total tokens exceed the platform's limit, the platform (not the model) must decide how to handle the overflow, typically by truncating the oldest parts of the conversation history to make room for the new input.

---

## 3. Tool Interaction Memory
When the model uses tools (like `read_file` or `run_in_bash_session`), the **results** of those tool calls are appended to the conversation history as "Tool" messages. These results also consume tokens and are treated as part of the context the model can reference in subsequent turns.

---
*This document describes the native behavior of the LLM platform interface.*
