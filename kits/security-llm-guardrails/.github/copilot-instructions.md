# GitHub Copilot Instructions for LLM Guardrails & AI Gateway (Pydantic AI + Llama Guard)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Architectural Standards for LLM Guardrails & AI Gateway (Pydantic AI + Llama Guard)
# Architecture Standards: LLM Guardrails & AI Gateway (Pydantic AI + Llama Guard)
- Strictly adhere to modular component separation.
- Keep dependency surface minimal and auditable.
- Prefer explicit configuration over magic implicit defaults.

## Security Invariants for LLM Guardrails & AI Gateway (Pydantic AI + Llama Guard)
# Security Invariants
- Verify tenant boundary before reading or writing any persistent state.
- Sanitize all external inputs using validated schemas.
- Reject requests with missing or expired bearer tokens.

## Agent Coding Conventions for LLM Guardrails & AI Gateway (Pydantic AI + Llama Guard)
# Agent Coding Conventions
- Maintain clean, minimal code changes with zero extraneous comments.
- Run typecheck and compile verification after every file modification.
- Never introduce undocumented third-party libraries without explicit instructions.

