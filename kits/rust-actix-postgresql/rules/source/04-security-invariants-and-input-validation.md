# Security Invariants, CORS, and Input Validation

1. **Strict CORS Whitelist**: Configure `actix_cors::Cors` explicitly from the `ALLOWED_ORIGINS` environment variable. Never configure permissive wildcard origins (`allow_any_origin()`) on authenticated routes.
2. **Payload Size Guardrails**: Configure `web::JsonConfig::default().limit(262_144)` (256 KB) to prevent memory exhaustion and Denial-of-Service attacks from oversized request bodies.
3. **DTO Input Validation**: Implement the `validator::Validate` derive macro on all request DTOs. Validate string lengths, email formats, and numerical bounds before passing data to entities.
4. **Pagination Bounds Clamping**: All list and search endpoints must enforce pagination clamps (`limit` clamped between 1 and 100, `offset` >= 0) to avoid unbounded table scans.
5. **Non-Root Container Hardening**: Build statically linked release binaries and package into minimal Alpine Linux runtime containers executing as unprivileged user `USER 10001:10001`.
