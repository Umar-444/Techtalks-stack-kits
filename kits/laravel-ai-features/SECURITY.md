# Security Policy: Laravel 12/13 + AI Features

## 1. Security Invariants
- **Rootless Docker**: Container execution is restricted to non-root UID `10001:10001`.
- **Prompt Injection Defense**: All user-supplied prompts pass through injection heuristic checks (regex jailbreak signatures, system prompt override attempts, base64 smuggling detectors) before invocation.
- **Strict Parameterized Vector Queries**: pgvector cosine distance operations (`<=>`) are executed via parameterized queries, never raw string interpolations.
- **Egress & Token Budgeting**: Per-user rate limiting and maximum completion token caps prevent denial-of-wallet attacks.
- **Zero Secret Leaks**: LLM API keys must reside in environment variables; mock adapters are provided for local development and CI testing.

## 2. Vulnerability Reporting
Please report security issues to `security@techtalks.dev`.
