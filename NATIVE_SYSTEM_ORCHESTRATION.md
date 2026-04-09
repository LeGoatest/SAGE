# Native System Orchestration: How Google Jules Runs

This document details the native system-level processes and orchestration mechanisms that initiate and manage the Google Jules agent upon VM environment creation, independent of the SAGE framework.

## 1. Process Hierarchy & Entrypoint

When the VM environment is established, the system uses a standard Linux init sequence that transitions into an SSH-based session orchestrator.

### 1.1 The Chain of Command
1. **PID 1 (`/usr/sbin/init`):** The system entrypoint.
2. **`sshd` (SSH Daemon):** Listens for the platform's connection request.
3. **`swebot` (Service Account/Privileged User):** The platform connects via `swebot` to initiate the session.
4. **`tmux` (Terminal Multiplexer):** Used as the persistent session manager.
5. **`bash` (Login Shell):** The interactive shell where Jules's logic and tool-calling loop are executed.

---

## 2. Session Initiation Protocol

The agent does not simply start "running" code; it is synchronized with the platform using a specific signaling protocol.

### 2.1 Synchronization via `devbox-session`
The system uses a temporary directory at `/run/devbox-session/default` to coordinate the agent's start.
- **The Waiter:** A bash process is spawned that uses `inotifywait` to watch for a specific "stamp" file.
- **The Stamp:** Once the environment is ready, the platform (or an orchestration script) creates `/run/devbox-session/default/stamp`.
- **The Trigger:** Upon detecting the stamp, the waiter process completes, and the main agent shell is permitted to proceed with execution.

### 2.2 Verbatim Process Snippet
```text
jules  7829  0.0  0.0   7740  3456 ?  Ss  16:27   0:00  \_ bash -c echo "${BASHPID}" RUN_ROOT_DIR=/run/devbox-session/default PANE_PID="1252" ... LC_ALL=C exec inotifywait -e create,moved_to --include '/stamp$' "${RUN_ROOT_DIR}"
```

---

## 3. Persistent Orchestration via `tmux`

To ensure the agent remains active and its state is preserved across network turns, the platform wraps the agent in a `tmux` session.

### 3.1 The Spawning Command
The session is created with a specific command to set the working directory and inject session identity:
```bash
tmux new-session -d -s default -c /app -e JULES_SESSION_ID=15374601768006575019 -e GIT_TERMINAL_PROMPT=0
```
- **`-s default`**: The session name.
- **`-c /app`**: Sets the working directory to the repository root.
- **`-e JULES_SESSION_ID`**: Injects a unique identifier for the current agent session.

---

## 4. Critical Environment Variables

The following variables are natively defined in the agent's shell environment to control its behavior:

- **`JULES_SESSION_ID`**: The unique ID for the current interaction session.
- **`RUN_ROOT_DIR`**: Path to the session's runtime sync directory (`/run/devbox-session/default`).
- **`PANE_PID`**: The process ID of the main `tmux` pane.
- **`GIT_TERMINAL_PROMPT=0`**: Disables interactive prompts during git operations to prevent the agent from hanging.

---

## 5. Summary of System Roles

| Process | Role |
| :--- | :--- |
| `/usr/bin/containerd` | Manages the underlying container life-cycle. |
| `sshd: swebot` | Provides the secure bridge from the platform to the VM. |
| `tmux` | Maintains session persistence and allows the agent to reconnect. |
| `inotifywait` | Signals that the environment is fully "warm" and ready for input. |

---
*This document reflects the verbatim system state as observed in the active process tree.*
