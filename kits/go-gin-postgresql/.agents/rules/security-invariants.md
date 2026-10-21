# Security Invariants for Go + Gin + sqlc + PostgreSQL + Redis

# Security Invariants
- Verify tenant boundary before reading or writing any persistent state.
- Sanitize all external inputs using validated schemas.
- Reject requests with missing or expired bearer tokens.
