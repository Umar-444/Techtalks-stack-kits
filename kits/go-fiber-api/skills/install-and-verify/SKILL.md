---
name: install-and-verify
description: Comprehensive preflight setup, container orchestration, and test execution for Go + Fiber + PostgreSQL.
---
# Install and Verify Skill: Go + Fiber + PostgreSQL

## 1. Prerequisites Setup
Ensure Go 1.23+ and Docker Compose are installed:
```bash
go version
docker compose version
```

## 2. Configuration Setup
```bash
cd starter
cp .env.example .env
```

## 3. Database Container Orchestration
```bash
docker compose up -d postgres
```

## 4. Run Automated Test Suite
```bash
go test -v -race ./...
```

## 5. Launch Service
```bash
go run main.go
```
Health probe:
```bash
curl http://localhost:8080/health
```

## 6. Done Means
- Go dependencies resolved cleanly via `go.mod`.
- PostgreSQL 16 container healthy.
- HTTP `/health` returns `{"status":"ok","framework":"fiber"}` with HTTP 200.
