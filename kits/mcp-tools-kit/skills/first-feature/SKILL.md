---
name: first-feature
description: Build the canonical sandboxed file inspector and database query tools with Zod schema verification and Vitest tests.
---

# Skill: First Feature (Sandboxed Tool Authoring)

## 1. Implement Tool
Implement `read_secure_file` in `src/tools/index.ts` with:
- Zod schema requiring `filepath: z.string()`.
- Path traversal protection verifying path boundary.

## 2. Register Tool
Register tool inside `McpServer` instance.

## 3. Test Feature
Create Vitest unit test in `tests/mcp-tools.test.ts` verifying tool execution and error handling.

## 4. Done Means
- Tool listed in `server.listTools()`.
- Adversarial path traversal payloads blocked.
- Vitest tests pass with code 0.
