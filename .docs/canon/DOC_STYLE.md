# Project Name | Documentation Style Guide

## 1) Markdown Standards
- Use clear, descriptive headings.
- Prefer lists for procedures and requirements.

## 2) Backtick Handling (Critical for Agents)
- Escape inline backticks as `\\` in generated markdown if they are part of a literal string.
- Never output literal triple-backticks inside a fenced code block.
- If you must show markdown code blocks inside markdown, use tilde fences (~~~md) or quadrupled backticks if supported.

## 3) Tone & Clarity
- Be direct and deterministic.
- Avoid flowery language or ambiguity.
