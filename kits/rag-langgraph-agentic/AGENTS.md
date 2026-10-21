# LangGraph + LangChain + Qdrant + Ragas Evals — Agent Operating Rules (AGENTS.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Table of Contents
- [Architectural Standards for LangGraph + LangChain + Qdrant + Ragas Evals](#architecture-guidelines)
- [Security Invariants for LangGraph + LangChain + Qdrant + Ragas Evals](#security-invariants)
- [Agent Coding Conventions for LangGraph + LangChain + Qdrant + Ragas Evals](#agent-coding-conventions)

---

<a id="architecture-guidelines"></a>
## Architectural Standards for LangGraph + LangChain + Qdrant + Ragas Evals

# Architecture Standards: LangGraph + LangChain + Qdrant + Ragas Evals
- Strictly adhere to modular component separation.
- Keep dependency surface minimal and auditable.
- Prefer explicit configuration over magic implicit defaults.

---

<a id="security-invariants"></a>
## Security Invariants for LangGraph + LangChain + Qdrant + Ragas Evals

# Security Invariants
- Verify tenant boundary before reading or writing any persistent state.
- Sanitize all external inputs using validated schemas.
- Reject requests with missing or expired bearer tokens.

---

<a id="agent-coding-conventions"></a>
## Agent Coding Conventions for LangGraph + LangChain + Qdrant + Ragas Evals

# Agent Coding Conventions
- Maintain clean, minimal code changes with zero extraneous comments.
- Run typecheck and compile verification after every file modification.
- Never introduce undocumented third-party libraries without explicit instructions.

---

