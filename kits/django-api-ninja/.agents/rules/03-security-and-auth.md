---
name: 03-security-and-auth
description: Bearer Token Authentication & Input Validation
---
# Security & Authorization Invariants
- Require authentication on all sensitive endpoints via uth=django_auth or custom HttpBearer.
- Validate all incoming payloads against strict Pydantic schemas. Never parse untyped 
equest.body.
- Keep DEBUG=False in production; use environment variables for SECRET_KEY and database credentials.
- Run Gitleaks secret scans and Semgrep AST checkers on every pull request.
