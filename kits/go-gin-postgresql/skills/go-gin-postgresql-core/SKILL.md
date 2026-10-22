---
name: go-gin-postgresql-core
description: Core operational workflows, layered Go architecture, Gin router configuration, and Token-Light evaluation.
---
# Go + Gin + PostgreSQL + Redis Core Skill

## 1. Architecture Overview
This kit provides a battle-tested production Go API architecture. It combines the Gin HTTP framework (the #1 Go web engine by adoption) with sqlc compile-time checked SQL queries, `pgx/v5` connection pooling, and Redis 7 cache.

```
[HTTP Request]
      |
      v
[Gin Engine Router] --> [Middleware: Logger, Recovery, CORS, Timeout]
      |
      v
[Handler Layer] (DTO Validation via go-playground/validator)
      |
      v
[Service Layer] (Business Logic & Cache-Aside Coordination)
     /             v           v
[Redis 7]   [SQLC Repository (pgxpool)]
(Cache)     (PostgreSQL 16 Storage)
```

## 2. Invariant Rules
- **Zero Wildcard CORS**: Origins parsed strictly from `ALLOWED_ORIGINS`.
- **Rootless Container**: Dockerfile compiles binary and executes as `USER 10001:10001`.
- **Graceful Shutdown**: SIGINT / SIGTERM triggers `srv.Shutdown(ctx)` with 10s deadline.

## 3. Verification Commands
```bash
# Unit & HTTP tests
go test -v ./...

# Benchmark execution
python evals/runner.py --kit go-gin-postgresql
```

## 4. Done Means
- 100% test assertions pass with zero data races.
- Database queries use type-safe sqlc generated code.
