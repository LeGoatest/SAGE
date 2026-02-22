# WDbasic Governance & Framework Contract

This document defines the **WDbasic** philosophy. It is a **contract**, not guidance.

---

## 1) Framework Role

WDbasic is the authoritative framework for:
- Marketing surfaces (landing pages, conversion funnels)
- Product surfaces (layouts, sidebars, dashboards)
- Reusable UI components (Hero, FAQ, CTA, Features)

It prioritizes **declarative-first HTML** and **server-rendered fragments** over client-side logic.

---

## 2) Non-Negotiable Rules

- **SEO-First**: Every public page MUST be fully indexable by search engines without requiring JavaScript execution.
- **HTMX-First**: All interactivity MUST be implemented via HTMX unless the UX requirement is strictly local and stateless.
- **Minimal JS**: JavaScript is ONLY allowed for stateless UI toggles (modals, dropdowns) or specific integrations where HTMX is insufficient.
- **Component Modularity**: All UI elements MUST be built as reusable server-side fragments or components.

---

## 3) Conversion-First Architecture

Layouts MUST follow the WDbasic conversion sequence where appropriate:
1. **Hero**: Clear value proposition + immediate CTA.
2. **Proof**: Social proof or testimonials.
3. **Features/Benefits**: Pain-Agitate-Solution flow.
4. **FAQ**: Handling common objections.
5. **Final CTA**: Recurring opportunity for conversion.

---

## 4) Fragment Strategy

WDbasic leverages the **Universal View Theory**.
- The shell is the container.
- WDbasic components are the units of content.
- HTMX swaps components based on user intent or server events.

---

## 5) Styling Standards

- **Tailwind CSS** (or a chosen utility-first framework) is the primary styling utility.
- No custom CSS files allowed unless strictly required for third-party integrations.
- All styling MUST be embedded in the components via utility classes.

---

## 6) Relationship to Other Laws

This document is subordinate to `ARCHITECTURE_RULES.md`.
If a conflict exists, **ARCHITECTURE_RULES.md wins**.
