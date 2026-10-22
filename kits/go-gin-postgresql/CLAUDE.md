# Go + Gin + sqlc + PostgreSQL + Redis — Claude Code Guidelines (CLAUDE.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Quick Reference & Non-Negotiable Standards
### 01 Framework Architecture And Standards
# Framework Architecture and Standards: Go, Gin, and SQLC

1. **Idiomatic Layered Architecture**: Structure code strictly into `cmd/`, `internal/handler/`, `internal/service/`, and `internal/repository/`. Never leak raw database queries into HTTP handlers.
2. **Gin Router Organization**: Group routes under `/api/v1` with explicit middleware chains (`gin.Recovery()`, structured logger, CORS, and request timeout).
3. **Structured JSON Responses**: Standardize all JSON payloads using envelope types (`data`, `error`, `meta`). Never return unstructured raw string error messages.
4. **Graceful Shutdown**: Implement standard `os/signal` listening for `SIGINT` and `SIGTERM`, invoking `http.Server.Shutdown(ctx)` with a 10-second timeout to flush in-flight requests.
5. **Strict Environment Injection**: Bind all configuration (PostgreSQL DSN, Redis URL, server port, CORS origins) via environment variables using strongly-typed configuration structs.


### 02 Sqlc Queries And Pgx Pooling
# SQLC Queries and PostgreSQL Connection Pooling

1. **SQLC Type Safety**: Author all database interactions in standard SQL files (`queries/*.sql`). Generate type-safe Go structs and queries via `sqlc generate`. Never use runtime reflection ORMs for critical query paths.
2. **Strict Parameterized Queries**: Every dynamic query value must be parameterized (`$1`, `$2`). Dynamic string interpolation or `fmt.Sprintf` query assembly is strictly prohibited.
3. **PGX Connection Pooling**: Manage PostgreSQL connections using `jackc/pgx/v5/pgxpool`. Set `MaxConns` (default: 25), `MinConns` (default: 5), and `MaxConnLifetime` (default: 1 hour) tuned for containerized deployment.
4. **Context Propagation**: Always pass `context.Context` (derived from `gin.Context.Request.Context()`) down through service and repository layers to ensure database query cancellation on client disconnects.
5. **Database Transaction Boundaries**: Encapsulate multi-table operations within explicit `pgx.Tx` transactions using a callback runner that guarantees rollback on error.


### 03 Redis Caching And Rate Limiting
# Redis Caching and Rate Limiting

1. **Cache-Aside Pattern**: Implement cache-aside for high-read entities. Check Redis before querying PostgreSQL; on cache miss, populate Redis with an explicit TTL. Never set keys with indefinite expiration.
2. **Cache Key Namespacing**: Format Redis keys predictably: `entity:{tenant_id}:{id}` (e.g. `user:org-alpha:1001`). Never use un-namespaced generic keys.
3. **Sliding Window Rate Limiter**: Guard public and authenticated endpoints with Redis-backed rate limiting. Rate limit headers (`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`) must be set on every response.
4. **Connection Resiliency**: Redis client connection errors must gracefully degrade to database fallback rather than halting the entire HTTP request lifecycle.
5. **Serialization Safety**: Store cached payloads in compact JSON or Protobuf. Always handle unmarshaling errors defensively.


### 04 Api Security And Input Validation
# API Security and Input Validation

1. **Strict CORS Whitelist**: Parse allowed CORS origins strictly from the `ALLOWED_ORIGINS` environment variable. Never configure `AllowAllOrigins = true` or `*` wildcards.
2. **Request Validation**: Use `go-playground/validator/v10` tags (`binding:"required,min=3,email"`) on all request DTO structs. Reject malformed payloads with HTTP 422 Unprocessable Entity.
3. **Non-Root Container Execution**: Compile multi-stage Dockerfiles that copy stripped Go binaries into minimal Alpine or scratch runners executing as `USER 10001:10001`.
4. **Security Headers Middleware**: Apply standard defense-in-depth headers: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `X-XSS-Protection: 1; mode=block`.
5. **No Secret Invariants**: Zero passwords, tokens, or private keys in source code. Enforced via automated Gitleaks CI audits.


### 05 Testing Verification And Ci
# Evaluation, Testing, and CI Invariants

1. **HTTP Test Isolation**: Author unit and integration tests using standard `net/http/httptest`. Execute test assertions directly against the `*gin.Engine` without binding local network ports.
2. **Repository Mocking**: Define repository interfaces (`UserRepository`, `CacheRepository`) to enable deterministic mock testing without live database dependencies in unit suites.
3. **Transpiler Zero Drift**: Single-source rules in `rules/source/` must compile to all 6 agent dialects (`CLAUDE.md`, Cursor, Codex, Copilot, Cline, Antigravity) with zero drift.
4. **Sub-Second Execution**: Unit test suites must execute in under 2 seconds.
5. **Linting and Semgrep Cleanliness**: Pass `golangci-lint` and Semgrep OWASP security rules with zero blocking findings.


