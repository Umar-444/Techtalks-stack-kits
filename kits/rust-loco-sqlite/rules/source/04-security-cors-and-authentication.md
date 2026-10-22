# Security Invariants, CORS, and Authentication

1. **Strict CORS Whitelist**: Configure CORS middleware inside Loco's configuration files and `src/app.rs`. Whitelist allowed origins strictly from the `ALLOWED_ORIGINS` environment variable; never allow wildcard origins (`*`) on routes handling credentials.
2. **Loco JWT Authentication**: Protect private endpoints using Loco's built-in JWT authenticator middleware. Verify token expiration, issuer, and signature validity on every protected route.
3. **DTO Input Validation**: Derive `validator::Validate` on all incoming request models. Validate string length boundaries, email syntax, and numeric constraints before passing data to database models.
4. **Non-Root Container Hardening**: Compile statically linked binaries and package into minimal Alpine Linux runtime containers executing as unprivileged user `USER 10001:10001`.
5. **Denial-of-Service Request Limits**: Configure request body limits (`DefaultBodyLimit::max(262_144)`) to reject oversized payloads (256 KB) before memory allocation.
