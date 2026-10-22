# Security Headers, CORS, and Rate Limiting

1. **Strict CORS Whitelist**: Parse allowed origins strictly from `ALLOWED_ORIGINS`. Never configure `AllowOrigins = "*"` or reflective wildcard origins in production environments.
2. **Security Headers Middleware**: Enforce HTTP defense-in-depth using Fiber's native helmet middleware (`X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `X-XSS-Protection: 1`).
3. **Rate Limiting Guardrails**: Apply Fiber's native rate limiter middleware to public API routes (e.g. max 100 requests per minute per IP) with Redis or memory store backends.
4. **Non-Root Container Security**: Dockerfiles must compile statically and execute under unprivileged user `USER 10001:10001` with read-only root filesystems where applicable.
5. **No Secret Invariants**: Zero credentials, tokens, or encryption keys in source code. Enforced via automated Gitleaks scans.
