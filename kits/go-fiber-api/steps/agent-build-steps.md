# Agent Build Steps: Go + Fiber + PostgreSQL

Follow these 6 steps to scaffold, execute, and verify the Go + Fiber production API:

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

## Step 2: PostgreSQL Container Orchestration
Start PostgreSQL backing database service:
```bash
docker compose up -d postgres
```

## Step 3: Fiber Router & Middleware Assembly
Configure the Fiber application with recovery, logger, and strict CORS whitelist:
```bash
go test -v -run TestHealthEndpoint ./...
```

## Step 4: Fasthttp Buffer Safety Verification
Verify buffer safety and race detection on ingestion routes:
```bash
go test -v -race -run TestBenchAndRecordsEndpoints ./...
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
