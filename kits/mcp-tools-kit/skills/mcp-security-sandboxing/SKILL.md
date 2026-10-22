---
name: mcp-security-sandboxing
description: Enforce path traversal protection, command execution boundaries, and read-only access locks.
---

# Skill: MCP Security Sandboxing

## Workflow
1. Define base root path.
2. Verify: `target.startsWith(baseRoot)`.
3. Throw error code `-32602` on violation.

## Done Means
- Sandbox escape attempts blocked.
