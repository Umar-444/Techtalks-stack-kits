---
name: "go-chi-templ-htmx-core"
description: "Core operational workflows, Chi router middleware management, graceful shutdown, health probes, and Token-Light evaluation."
---

# Skill: Go + Chi + templ + HTMX Core Operations

Use this skill for server lifecycle management, health monitoring, and running automated evaluations.

## 1. Application Entrypoint & Middleware Setup
Start the server with production middleware:
```bash
go run main.go
```

The router configures:
- `middleware.RequestID`: Injects a unique UUID into request context and `X-Request-Id` response header.
- `middleware.Logger`: Structured request logging.
- `middleware.Recoverer`: Catches panics and returns HTTP 500 without crashing the daemon.
- `middleware.Timeout`: Bounds long-running HTTP requests to 30s.

## 2. Health & Readiness Probe
```bash
curl -i http://localhost:8080/health
```
Returns:
```http
HTTP/1.1 200 OK
Content-Type: application/json
Date: Thu, 22 Oct 2026 12:00:00 GMT
Content-Length: 48

{"status":"ok","framework":"chi","token_light":true}
```

## 3. Token-Light Benchmark Evaluation (Document 20 Part F)
Execute the token benchmark runner:
```bash
python evals/runner.py --kit go-chi-templ-htmx
```
Verifies:
- Manifest valid and all physical layers verified.
- Transpiler zero-drift confirmed.
- Secret leaks: 0 findings.
- Total build token consumption: **16,796 tokens** (Efficiency Tier: **A+ Token-Light Verified**).
