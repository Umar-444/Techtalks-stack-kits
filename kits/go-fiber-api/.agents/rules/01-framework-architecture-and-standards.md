# 01 Framework Architecture And Standards

# Framework Architecture and Standards: Go and Fiber (fasthttp)

1. **Throughput-First Architecture**: Fiber is engineered on top of `fasthttp`, bypassing `net/http` allocation overhead for maximum request per second (RPS) throughput and lowest p99 latency.
2. **Route Grouping**: Encapsulate API resources under `/api/v1` route groups with explicit middleware composition (structured logger, recovery, and request ID).
3. **Graceful Shutdown**: Intercept `SIGINT` and `SIGTERM` signals using standard `signal.Notify`, triggering `app.ShutdownWithTimeout(ctx)` to finish active connections within 10 seconds.
4. **Environment Binding**: Ingest runtime configuration (`PORT`, `DATABASE_URL`, `ALLOWED_ORIGINS`) through strongly typed structs parsed from environment variables.
5. **Architectural Caveats**: Acknowledge that `fasthttp` is not 100% compatible with standard `net/http` middleware. Third-party packages requiring `http.Handler` must use Fiber adaptors or native Fiber implementations.

