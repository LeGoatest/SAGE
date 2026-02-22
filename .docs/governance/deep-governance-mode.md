# Deep Governance Mode

Deep Governance Mode is a **governance validation state**.
It increases inspection depth prior to planning or execution.

Deep Mode does not expand authority.
It reduces risk by forcing explicit validation loops.

---

## When to Use

Deep Mode must be entered when:
- the user explicitly requests it
- protected zones may be affected
- a canon conflict is suspected
- mutation is likely
- policy thresholds trigger escalation
- cross-model handover occurs mid-task

Deep Mode should be used for any “governance change” request.

---

## Activation Token

Deep Mode is invoked by emitting or receiving the marker:

ENTER_DEEP_GOVERNANCE_MODE

---

## Deterministic Loop Algorithm

Deep Mode runs up to **3 passes**.

Each pass MUST:
- Re-evaluate canonical precedence
- Detect canon conflicts or ambiguity
- Check protected zone interaction
- Check security boundary implications (no invention)
- Re-validate task group classification
- Evaluate determinism stability risk
- Detect shadow architecture pressure
- Determine if mutation is required

After each pass:
- Compare the risk list to the previous pass
- If no new risks appear for **two consecutive passes**, convergence is achieved

If new risks still appear in pass 3:
- Emit `[AWAIT_HUMAN_VALIDATION]`
- Stop

---

## Output Contract

Deep Mode output must contain ONLY:

- Risks (bullet list)
- Canon references (file + section)
- Determinism impact: None / Low / Moderate / High
- Mutation required: Yes / No
- Execution safe: Yes / No

If Execution safe = No:
- Emit `[AWAIT_HUMAN_VALIDATION]` on its own line
- Provide a short bullet list for what decision is required
- Stop

---

## Hard Prohibitions

Deep Mode MUST NOT:
- generate implementation steps
- modify any files
- draft security boundaries without repository evidence
- “best guess” trust models
- continue after emitting the HITL marker

Deep Mode is analysis-only.

---

## Relationship to Spec Mode

Deep Mode runs **before** Spec Mode for non-trivial or governance-sensitive work.

Deep Mode answers:
- “Is it safe to plan?”
- “Is mutation required?”
- “Is canon ambiguous?”

Spec Mode answers:
- “What should be built, in what order, under what constraints?”

---

## Telemetry Hooks (Policy)

Deep Mode should emit telemetry events (documented in policy):
- deep_mode_entered
- deep_mode_pass_completed (pass_count)
- deep_mode_converged
- deep_mode_escalated_hitl
- deep_mode_mutation_required

Policy observes; it does not override canon.

---

Deep Mode is a governance guardrail.
It makes drift visible before it becomes architecture.
