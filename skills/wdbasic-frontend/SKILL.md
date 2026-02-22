---
name: wdbasic-frontend
description: Procedural playbook for building or modifying frontend components following the WDbasic philosophy (SEO-first, HTMX-first, Minimal JS).
metadata:
  category: frontend
  authority: procedural
  requires:
    - WDBASIC.md
    - ARCHITECTURE_RULES.md
---

# Skill: wdbasic-frontend

## Authority Boundary

This skill is **procedural only**.
It MUST NOT override the principles defined in `WDBASIC.md`.
It MUST NOT introduce client-side state or complex JavaScript patterns unless explicitly permitted by architecture.

## Procedure

### Step 1: Component Classification
Determine if the requested element is a:
- **Layout Shell**: The main HTML structure (head, body, global assets).
- **Surface**: A major page section (Hero, Features, FAQ).
- **Fragment**: A small, dynamic piece swapped by HTMX (Typing indicator, Chat message).

### Step 2: Implementation Sequence
1. **HTML Structure**: Define the semantic HTML first. Ensure it is readable without CSS or JS.
2. **Tailwind Styling**: Apply utility classes directly to the elements. Do NOT create custom CSS classes unless strictly necessary for external integrations.
3. **HTMX Integration**: Add `hx-*` attributes for interactivity. Identify the trigger, the target, and the swap strategy.
4. **Minimal JS**: If (and only if) HTMX cannot handle the requirement (e.g., local UI toggles), add minimal, stateless JavaScript.

### Step 3: Verification
- **SEO Check**: Does the component render meaningful content on the server?
- **Performance Check**: Are images lazy-loaded? Is the DOM structure lean?
- **Interactivity Check**: Does the HTMX swap work as expected? Does it handle error states?

## Guidelines
- Use `hx-swap="outerHTML"` for replacing entire components.
- Use `hx-swap="beforeend"` for appending to lists (e.g., chat, activity feeds).
- Always include loading indicators (`hx-indicator`) for network-dependent actions.
- Keep components small and focused on a single responsibility.
