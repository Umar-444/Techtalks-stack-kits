---
name: "install-and-verify"
description: "Install, compile, configure, and verify the Go + Chi + templ + HTMX + sqlc + PostgreSQL service."
---

# Skill: Install and Verify Go + Chi + templ + HTMX + sqlc

Use this skill to set up the development environment, generate code from templates and SQL queries, run PostgreSQL, and verify the service.

## Step 1: Toolchain Prerequisites
Verify that Go 1.23+ is installed:
```bash
go version
```

Install `templ` and `sqlc` code generators:
```bash
go install github.com/a-h/templ/cmd/templ@latest
go install github.com/sqlc-dev/sqlc/cmd/sqlc@latest
```

## Step 2: Code Generation
Run `templ` and `sqlc` in the starter directory:
```bash
cd starter
templ generate
sqlc generate
```

## Step 3: Start Local PostgreSQL (Docker Compose)
Launch PostgreSQL 16 using Docker Compose:
```bash
docker compose up -d postgres
docker compose ps
```

Apply database migrations:
```bash
psql -h localhost -U postgres -d app_db -f schema.sql
```

## Step 4: Run Tests & Start Service
Execute the Go test suite:
```bash
go test -v ./...
```

Run the application locally:
```bash
go run main.go
```

## Step 5: Verification Curls
Check application health:
```bash
curl -s http://localhost:8080/health | jq .
```
Expected response:
```json
{
  "status": "ok",
  "framework": "chi",
  "token_light": true
}
```
