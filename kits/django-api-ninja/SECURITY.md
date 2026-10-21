# Security Policy & Invariants: Django + Django Ninja + PostgreSQL + Celery

## 1. Mandatory Invariants
1. **Secret Scanning:** Zero hardcoded API keys, secrets, or JWT tokens. All secrets loaded through environment variables.
2. **Injection Defense:** Compile-time parameterized SQL / ORM bindings. No string concatenation in query builders.
3. **Authorization:** Explicit tenant validation on every object retrieval (BOLA prevention).
4. **Header Hardening:** HSTS, X-Content-Type-Options: nosniff, Frame-Ancestors: none.

## 2. Reporting Security Vulnerabilities
Report any vulnerability to [security@itsumarfarooq.com](mailto:security@itsumarfarooq.com).
