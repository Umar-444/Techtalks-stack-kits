# Security Policy: Model Context Protocol (MCP) Server

## 1. Invariants
- **Rootless Docker**: Container execution is restricted to non-root UID `10001:10001`.
- **Path Traversal Defense**: All file tools enforce strict root boundaries (`path.resolve` check against allowed workspace root). Absolute parent escapes (`../`) are rejected immediately.
- **Command Injection Prevention**: No arbitrary shell execution; only pre-approved, parameterized utilities are permitted.
- **Zod Schema Validation**: Every tool call validates incoming JSON-RPC parameters before invocation.
- **Rate & Memory Limits**: Maximum payload size capped at 4MB to prevent memory exhaustion.

## 2. Vulnerability Reporting
Please report vulnerabilities to `security@techtalks.dev`.
