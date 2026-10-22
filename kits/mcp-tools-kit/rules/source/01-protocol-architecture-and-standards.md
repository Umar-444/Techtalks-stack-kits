---
id: 01-protocol-architecture-and-standards
title: MCP Architecture and Protocol Standards
description: Core specifications for Model Context Protocol servers.
globs: ["src/**/*.ts"]
alwaysApply: true
---

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
