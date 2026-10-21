# Elixir + Phoenix 1.7+ + LiveView + Ecto + PostgreSQL — Claude Code Guidelines (CLAUDE.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Quick Reference & Non-Negotiable Standards
### Architectural Standards for Elixir + Phoenix 1.7+ + LiveView + Ecto + PostgreSQL
# Architecture Standards: Elixir + Phoenix 1.7+ + LiveView + Ecto + PostgreSQL
- Strictly adhere to modular component separation.
- Keep dependency surface minimal and auditable.
- Prefer explicit configuration over magic implicit defaults.

### Security Invariants for Elixir + Phoenix 1.7+ + LiveView + Ecto + PostgreSQL
# Security Invariants
- Verify tenant boundary before reading or writing any persistent state.
- Sanitize all external inputs using validated schemas.
- Reject requests with missing or expired bearer tokens.

### Agent Coding Conventions for Elixir + Phoenix 1.7+ + LiveView + Ecto + PostgreSQL
# Agent Coding Conventions
- Maintain clean, minimal code changes with zero extraneous comments.
- Run typecheck and compile verification after every file modification.
- Never introduce undocumented third-party libraries without explicit instructions.

