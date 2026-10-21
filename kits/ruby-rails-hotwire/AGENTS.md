# Ruby on Rails 8 + Hotwire (Turbo + Stimulus) + SQLite/PostgreSQL — Agent Operating Rules (AGENTS.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Table of Contents
- [Architectural Standards for Ruby on Rails 8 + Hotwire (Turbo + Stimulus) + SQLite/PostgreSQL](#architecture-guidelines)
- [Security Invariants for Ruby on Rails 8 + Hotwire (Turbo + Stimulus) + SQLite/PostgreSQL](#security-invariants)
- [Agent Coding Conventions for Ruby on Rails 8 + Hotwire (Turbo + Stimulus) + SQLite/PostgreSQL](#agent-coding-conventions)

---

<a id="architecture-guidelines"></a>
## Architectural Standards for Ruby on Rails 8 + Hotwire (Turbo + Stimulus) + SQLite/PostgreSQL

# Architecture Standards: Ruby on Rails 8 + Hotwire (Turbo + Stimulus) + SQLite/PostgreSQL
- Strictly adhere to modular component separation.
- Keep dependency surface minimal and auditable.
- Prefer explicit configuration over magic implicit defaults.

---

<a id="security-invariants"></a>
## Security Invariants for Ruby on Rails 8 + Hotwire (Turbo + Stimulus) + SQLite/PostgreSQL

# Security Invariants
- Verify tenant boundary before reading or writing any persistent state.
- Sanitize all external inputs using validated schemas.
- Reject requests with missing or expired bearer tokens.

---

<a id="agent-coding-conventions"></a>
## Agent Coding Conventions for Ruby on Rails 8 + Hotwire (Turbo + Stimulus) + SQLite/PostgreSQL

# Agent Coding Conventions
- Maintain clean, minimal code changes with zero extraneous comments.
- Run typecheck and compile verification after every file modification.
- Never introduce undocumented third-party libraries without explicit instructions.

---

