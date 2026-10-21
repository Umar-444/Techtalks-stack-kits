# GitHub Copilot Instructions for TypeScript + Hono + Bun + Drizzle + SQLite
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Architectural Standards for TypeScript + Hono + Bun + Drizzle + SQLite
# Architecture Standards: TypeScript + Hono + Bun + Drizzle + SQLite
- Strictly adhere to modular component separation.
- Keep dependency surface minimal and auditable.
- Prefer explicit configuration over magic implicit defaults.

## Security Invariants for TypeScript + Hono + Bun + Drizzle + SQLite
# Security Invariants
- Verify tenant boundary before reading or writing any persistent state.
- Sanitize all external inputs using validated schemas.
- Reject requests with missing or expired bearer tokens.

## Agent Coding Conventions for TypeScript + Hono + Bun + Drizzle + SQLite
# Agent Coding Conventions
- Maintain clean, minimal code changes with zero extraneous comments.
- Run typecheck and compile verification after every file modification.
- Never introduce undocumented third-party libraries without explicit instructions.

