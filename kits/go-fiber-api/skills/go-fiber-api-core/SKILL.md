---
name: go-fiber-api-core
description: Core operational workflows, fasthttp zero-allocation patterns, Fiber router configuration, and Token-Light evaluation.
---
# Go + Fiber + PostgreSQL Core Skill

## 1. Architecture Overview
This kit provides a high-throughput, low-latency API architecture powered by Go 1.23+ and Fiber v2/v3 on top of the fasthttp zero-allocation engine. It delivers maximum requests per second for I/O heavy workloads paired with PostgreSQL 16 connection pooling.

```
[HTTP Request]
      |
      v
[Fiber Router (fasthttp)] --> [Middleware: Logger, Recover, Helmet, Limiter, CORS]
      |
      v
[Handler Layer] (Safe buffer copy & BodyParser)
      |
      v
[Repository Layer] (pgx/v5 Parameterized Queries)
      |
      v
[PostgreSQL 16 Engine]
```

## 2. Invariant Rules
- **Zero Wildcard CORS**: Whitelisted origins read strictly from `ALLOWED_ORIGINS`.
- **Buffer Safety**: Strings copied via `strings.Clone` when passed across goroutines.
- **Rootless Container**: Dockerfile executes as `USER 10001:10001`.

## 3. Verification Commands
```bash
# Run unit tests with race detection
go test -v -race ./...

# Run benchmark runner
python evals/runner.py --kit go-fiber-api
```

## 4. Done Means
- 100% test assertions pass with zero data races.
- Buffer reuse invariants respected across all handlers.
