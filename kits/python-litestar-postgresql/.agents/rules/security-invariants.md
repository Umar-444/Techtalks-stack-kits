# Security Invariants for Python + Litestar + SQLAlchemy 2 + PostgreSQL + Redis

# Security Invariants
- Verify tenant boundary before reading or writing any persistent state.
- Sanitize all external inputs using validated schemas.
- Reject requests with missing or expired bearer tokens.
