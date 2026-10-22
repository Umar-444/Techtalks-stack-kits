# GitHub Copilot Instructions for Model Context Protocol (MCP) Server Kit (stdio + SSE)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## MCP Architecture and Protocol Standards
# MCP Architecture and Protocol Standards

## 1. Protocol Conformance
- Always use the official `@modelcontextprotocol/sdk` to implement server logic.
- Declare explicit capabilities during initialization: `tools`, `resources`, `prompts`.
- Adhere strictly to the JSON-RPC 2.0 specification for requests, responses, and error payloads.

## 2. Directory Layout
- **Transports**: `src/transports/` (`stdio.ts`, `sse.ts`).
- **Tools**: `src/tools/` (individual tool definitions with Zod schemas).
- **Resources**: `src/resources/` (dynamic URI-based data providers).
- **Prompts**: `src/prompts/` (reusable prompt templates).

## 3. Never-List
- Never use `eval()` or `new Function()` in tool implementations.
- Never write debug logs directly to `process.stdout` when running in `stdio` mode; write to `process.stderr` instead.
- Never execute tools without validating input arguments via Zod.

## Stdio and SSE Transport Architecture
# Stdio and SSE Transport Architecture

## 1. Stdio Transport Best Practices
- `StdioServerTransport` uses `process.stdin` and `process.stdout` for communication.
- All application logging must use `console.error()` to keep stdout exclusively reserved for JSON-RPC messages.

## 2. SSE HTTP Transport Best Practices
- `SSEServerTransport` handles HTTP GET `/sse` for client connection and POST `/messages` for commands.
- Protect SSE endpoints with authentication middleware in non-local environments.

## Tool Schema and Zod Validation Standards
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

## Security Sandboxing and Access Boundaries
# Security Sandboxing and Access Boundaries

## 1. Path Traversal Defense
- Always resolve paths against an allowed base directory using `path.resolve()`.
- Validate that `resolvedPath.startsWith(allowedRoot)`.
- Disallow access to hidden dotfiles or system directories (`/etc`, `/proc`).

## 2. Denial-of-Service Defense
- Cap tool output buffer size to 4MB.
- Impose timeout limits (default 10s) on long-running tool operations.

## Testing Verification and CI Standards
# Testing Verification and CI Standards

## 1. Unit Testing Tools
- Test tool execution directly by invoking registered handler functions.
- Test that invalid payloads fail Zod validation with code `-32602`.
- Test that path traversal attempts throw `SecurityError`.

## 2. CI Pipeline
- Every PR must pass `npm test`, `npm run build`, `gitleaks`, and `semgrep`.

