# Verification Log: Go + Fiber + PostgreSQL

- **Verification Date**: 2026-10-22
- **Tested Environment**: Go 1.23+, Fiber v2.52.5 (fasthttp), PostgreSQL 16.4, Docker Compose v2.29
- **Test Type**: Clean checkout build, in-memory app.Test execution, buffer safety validation, CORS whitelist verification, and non-root container checks
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
   *Result*: `go-fiber-api-app` and `go-fiber-api-db` operational and healthy on ports 8080 and 5432.

3. **Liveness & Health Probe**:
   ```bash
   curl -s http://localhost:8080/health
   ```
   *Response*: `{"engine":"fasthttp","framework":"fiber","status":"ok","version":"1.0.0"}` (HTTP 200 OK)

4. **CORS Options Preflight Probe**:
   ```bash
   curl -s -I -X OPTIONS http://localhost:8080/api/v1/bench \
     -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: GET"
   ```
   *Response*: HTTP 204 No Content with `Access-Control-Allow-Origin: http://localhost:3000`.

5. **Throughput Benchmark & Ingestion Probe**:
   ```bash
   curl -X POST http://localhost:8080/api/v1/records \
     -H "Content-Type: application/json" \
     -d '{"key":"telemetry-sensor","value":"24.5C"}'
   ```
   *Response*: `{"data":{"id":1,"key":"telemetry-sensor","value":"24.5C"}}` (HTTP 201 Created)

6. **Automated Unit & Test Suite**:
   ```bash
   go test -v -race ./...
   ```
   *Result*: PASS across all test assertions with zero data races.

## Invariant Assertions
- `invariants.cors`: Zero wildcard CORS origins; parsed strictly from `ALLOWED_ORIGINS`.
- `invariants.security`: Dockerfile executes under non-root UID 10001.
- `invariants.buffer_safety`: String copying via `strings.Clone` prevents fasthttp buffer reuse race conditions.
- `invariants.shutdown`: Graceful shutdown traps SIGINT/SIGTERM with 10s deadline.
