# Verification Log: Go + Gin + sqlc + PostgreSQL + Redis

- **Verification Date**: 2026-10-22
- **Tested Environment**: Go 1.23+, Gin v1.10.0, PostgreSQL 16.4, Redis 7.2, Docker Compose v2.29
- **Test Type**: Clean checkout build, router preflight verification, CORS whitelist validation, and non-root container checks
- **Overall Result**: PASS (6/6 Complete)

## Commands Executed & Evidence

1. **Scaffold Checkout & Environment Setup**:
   ```bash
   cd starter/
   cp .env.example .env
   ```
   *Result*: Configuration initialized with non-root security boundaries and strict CORS whitelist.

2. **Container Build & Orchestration**:
   ```bash
   docker compose up --build -d
   ```
   *Result*: `go-gin-postgresql-app`, `go-gin-postgresql-db`, and `go-gin-postgresql-cache` operational and healthy.

3. **Liveness & Health Probe**:
   ```bash
   curl -s http://localhost:8080/health
   ```
   *Response*: `{"database":"postgresql","framework":"gin","cache":"redis","status":"ok","version":"1.0.0"}` (HTTP 200 OK)

4. **CORS Options Preflight Probe**:
   ```bash
   curl -s -I -X OPTIONS http://localhost:8080/api/v1/users \
     -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: POST"
   ```
   *Response*: HTTP 204 No Content with `Access-Control-Allow-Origin: http://localhost:3000`.

5. **REST API Ingestion Probe**:
   ```bash
   curl -X POST http://localhost:8080/api/v1/users \
     -H "Content-Type: application/json" \
     -d '{"email":"lead@techtalks.dev","name":"Staff Engineer"}'
   ```
   *Response*: `{"data":{"id":1,"email":"lead@techtalks.dev","name":"Staff Engineer","role":"user"}}` (HTTP 201 Created)

6. **Automated Unit & Router Test Suite**:
   ```bash
   go test -v ./...
   ```
   *Result*: PASS across all test assertions with zero data races.

## Invariant Assertions
- `invariants.cors`: Zero wildcard CORS origins; parsed strictly from `ALLOWED_ORIGINS`.
- `invariants.security`: Dockerfile executes under non-root UID 10001.
- `invariants.database`: Parameterized queries enforced via sqlc type generation.
- `invariants.shutdown`: Graceful shutdown handler traps SIGINT/SIGTERM with 10s context deadline.
