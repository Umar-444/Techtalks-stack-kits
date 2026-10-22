---
name: mcp-tool-authoring
description: Author production-ready MCP tools with typed Zod arguments, error handling, and progress notifications.
---

# Skill: MCP Tool Authoring

## Workflow
1. Define tool with `server.tool(name, description, schema, handler)`.
2. Parse inputs safely.
3. Return `{ content: [{ type: 'text', text: result }] }`.

## Done Means
- Tool correctly registered and callable.
