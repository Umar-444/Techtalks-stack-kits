# Security Invariants for TypeScript + Hono + Bun + Drizzle + SQLite

# Security Invariants
- Verify tenant boundary before reading or writing any persistent state.
- Sanitize all external inputs using validated schemas.
- Reject requests with missing or expired bearer tokens.
