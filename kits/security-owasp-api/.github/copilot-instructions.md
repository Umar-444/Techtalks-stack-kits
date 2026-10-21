# GitHub Copilot Instructions for OWASP API Security Top 10 Reference + Pytest Attack Suite
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Architectural Standards for OWASP API Security Top 10 Reference + Pytest Attack Suite
# Architecture Standards: OWASP API Security Top 10 Reference + Pytest Attack Suite
- Strictly adhere to modular component separation.
- Keep dependency surface minimal and auditable.
- Prefer explicit configuration over magic implicit defaults.

## Security Invariants for OWASP API Security Top 10 Reference + Pytest Attack Suite
# Security Invariants
- Verify tenant boundary before reading or writing any persistent state.
- Sanitize all external inputs using validated schemas.
- Reject requests with missing or expired bearer tokens.

## Agent Coding Conventions for OWASP API Security Top 10 Reference + Pytest Attack Suite
# Agent Coding Conventions
- Maintain clean, minimal code changes with zero extraneous comments.
- Run typecheck and compile verification after every file modification.
- Never introduce undocumented third-party libraries without explicit instructions.

