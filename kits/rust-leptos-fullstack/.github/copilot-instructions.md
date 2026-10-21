# GitHub Copilot Instructions for Rust + Leptos Full-Stack + Axum + WebAssembly
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Architectural Standards for Rust + Leptos Full-Stack + Axum + WebAssembly
# Architecture Standards: Rust + Leptos Full-Stack + Axum + WebAssembly
- Strictly adhere to modular component separation.
- Keep dependency surface minimal and auditable.
- Prefer explicit configuration over magic implicit defaults.

## Security Invariants for Rust + Leptos Full-Stack + Axum + WebAssembly
# Security Invariants
- Verify tenant boundary before reading or writing any persistent state.
- Sanitize all external inputs using validated schemas.
- Reject requests with missing or expired bearer tokens.

## Agent Coding Conventions for Rust + Leptos Full-Stack + Axum + WebAssembly
# Agent Coding Conventions
- Maintain clean, minimal code changes with zero extraneous comments.
- Run typecheck and compile verification after every file modification.
- Never introduce undocumented third-party libraries without explicit instructions.

