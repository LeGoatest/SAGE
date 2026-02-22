---
name: tailwindcss-cli
description: Defines the correct TailwindCSS CLI setup when input.css lives in the project root and compiled CSS outputs to assets/css/style.css.
metadata:
  category: operations
  authority: procedural
---

# SKILL: TailwindCSS CLI (Root Input + assets/css Output)

## Skill ID
SKILL-TWCLI-ROOT-ASSETS-001

## Classification
Build Tooling
Frontend Infrastructure

## Task Group
operations

## Source
TailwindCSS Official CLI Installation
https://tailwindcss.com/docs/installation/tailwind-cli

---

# 1) Purpose

This skill defines the correct TailwindCSS CLI setup when:

- `input.css` lives in the project root
- Compiled CSS outputs to `assets/css/style.css`
- No bundler is used
- No framework assumptions
- Clean deterministic build pipeline required

---

# 2) Required Project Structure

/input.css /assets/css/style.css /index.html /package.json

---

# 3) Installation

## Step 1 — Install Official CLI

npm install tailwindcss @tailwindcss/cli

---

## Step 2 — Root input.css

Create in project root:

/input.css

Contents:

@import "tailwindcss";

If using Iconify plugin:

@plugin "@iconify/tailwind4";

---

## Step 3 — CLI Commands

Build once:

npx @tailwindcss/cli -i ./input.css -o ./assets/css/style.css

Watch mode:

npx @tailwindcss/cli -i ./input.css -o ./assets/css/style.css --watch

Minified production build:

npx @tailwindcss/cli -i ./input.css -o ./assets/css/style.css --minify

---

# 4) package.json Scripts (Recommended)

"scripts": { "dev": "npx @tailwindcss/cli -i ./input.css -o ./assets/css/style.css --watch", "build": "npx @tailwindcss/cli -i ./input.css -o ./assets/css/style.css --minify" }

---

# 5) HTML Binding

In your HTML:

<link rel="stylesheet" href="./assets/css/style.css">

Never link to input.css.

---

# 6) Content Scanning

Tailwind v4 auto-detects content.

Only create a config file if:
- Custom theme needed
- Advanced scanning rules required

Minimal config (optional):

export default {
  content: [
    "./**/*.html",
    "./**/*.js"
  ]
}

---

# 7) Determinism Rules

This configuration guarantees:
- Single source input (/input.css)
- Single compiled output (/assets/css/style.css)
- No runtime CSS generation
- Reproducible builds
- No CDN reliance

---

# 8) Verification Checklist

[ ] npm install succeeds
[ ] npm run build creates /assets/css/style.css
[ ] npm run dev watches changes
[ ] HTML renders Tailwind utilities
[ ] No reference to input.css in HTML
[ ] No CDN Tailwind script tag

---

# 9) Common Mistakes

❌ Outputting to root accidentally
❌ Forgetting assets/css/ folder
❌ Linking wrong path in HTML
❌ Using outdated @tailwind base syntax
❌ Mixing CDN + CLI

---

# 10) Output Template (When Invoked)

Jules must output:

1. File tree
2. input.css contents
3. package.json scripts
4. CLI command used
5. HTML link tag update

No extra commentary.

---

## Authority Boundary
This skill is **procedural only**. It provides instructions for setting up the TailwindCSS build pipeline and does not modify canonical architecture.

---

END SKILL
