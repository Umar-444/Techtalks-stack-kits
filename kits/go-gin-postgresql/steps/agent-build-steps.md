# Agent Build Steps: Go + Gin + PostgreSQL + Redis

Follow these 6 steps to scaffold, execute, and verify the Go + Gin production API:

## Step 1: Environment Initialization & Preflight
Initialize Go module dependencies and environment configuration:
```bash
cp starter/.env.example starter/.env
cd starter
go mod download
```
Verification:
```bash
go version
```

## Step 2: PostgreSQL & Redis Container Orchestration
Start database and cache backing services:
```bash
docker compose up -d postgres redis
```

## Step 3: SQLC Query Generation
Compile SQL schemas and queries into type-safe Go structs:
```bash
sqlc generate
```

## Step 4: Gin Router & Middleware Assembly
Configure the Gin engine with recovery, logger, and strict CORS whitelist:
```bash
go test -v -run TestHealthEndpoint ./...
```

## Step 5: Application Service Launch
Start the HTTP API service with graceful shutdown handling:
```bash
go run main.go
```
Verification:
```bash
curl -f http://localhost:8080/health
```

## Step 6: Automated Security & Regression Suite
Run full test suite and verify compliance across all 12 security checks:
```bash
go test -v -race ./...
```
