---
id: 03-tool-schema-and-zod-validation
title: Tool Schema and Zod Validation Standards
description: Defining type-safe tools, arguments, and error codes.
globs: ["src/tools/**/*.ts"]
alwaysApply: true
---

# Tool Schema and Zod Validation Standards

## 1. Tool Declaration Structure
- Every tool must specify:
  - `name`: Unique identifier in `snake_case` (e.g. `read_secure_file`).
  - `description`: Clear technical description aiding LLM tool selection.
  - `parameters`: Zod object schema defining typed arguments.
- Handle execution errors gracefully and return structured content:
  `{ content: [{ type: 'text', text: JSON.stringify(result) }] }`.

## 2. Parameter Sanitization
- Set bounds on numeric inputs (`.min()`, `.max()`).
- Sanitize string inputs using `.trim()` and regex patterns.
