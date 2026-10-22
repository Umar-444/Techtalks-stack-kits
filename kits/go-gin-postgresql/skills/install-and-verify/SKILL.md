---
name: install-and-verify
description: Comprehensive preflight setup, database container orchestration, and test execution for Go + Gin + PostgreSQL + Redis.
---
# Install and Verify Skill: Go + Gin + PostgreSQL + Redis

## 1. Prerequisites and Environment Setup
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

## 3. Database & Redis Orchestration
```bash
docker compose up -d postgres redis
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
- PostgreSQL 16 and Redis 7 healthy and accepting connections.
- HTTP `/health` returns `{"status":"ok","framework":"gin"}` with HTTP 200.
