---
name: mcp-transport-configuration
description: Configure StdioServerTransport for desktop clients and SSEServerTransport for distributed agent swarms.
---

# Skill: MCP Transport Configuration

## Workflow
1. Run stdio: `node dist/transports/stdio.js`.
2. Run SSE: `node dist/transports/sse.js`.
3. Handle process signal traps (`SIGTERM`, `SIGINT`).

## Done Means
- Both transports operate deterministically.
