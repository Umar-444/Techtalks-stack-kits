# LlamaIndex + PostgreSQL pgvector + FastAPI — Claude Code Guidelines (CLAUDE.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Quick Reference & Non-Negotiable Standards
### Architectural Standards for LlamaIndex + PostgreSQL pgvector + FastAPI
# Architecture Standards: LlamaIndex + PostgreSQL pgvector + FastAPI
- Strictly adhere to modular component separation.
- Keep dependency surface minimal and auditable.
- Prefer explicit configuration over magic implicit defaults.

### Security Invariants for LlamaIndex + PostgreSQL pgvector + FastAPI
# Security Invariants
- Verify tenant boundary before reading or writing any persistent state.
- Sanitize all external inputs using validated schemas.
- Reject requests with missing or expired bearer tokens.

### Agent Coding Conventions for LlamaIndex + PostgreSQL pgvector + FastAPI
# Agent Coding Conventions
- Maintain clean, minimal code changes with zero extraneous comments.
- Run typecheck and compile verification after every file modification.
- Never introduce undocumented third-party libraries without explicit instructions.

