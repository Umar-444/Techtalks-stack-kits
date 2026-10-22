# OWASP API Security Top 10 Reference API Stack Kit

A production-grade Python/FastAPI reference implementation and automated test harness enforcing defense-in-depth across the **OWASP API Security Top 10 (2023)** standard.

## Features & Threat Defenses
- **API1:2023 BOLA**: Object ownership verification on all resource lookups.
- **API2:2023 Broken Authentication**: Cryptographically verified PyJWT tokens with explicit algorithm pinning.
- **API3:2023 BOPLA**: Pydantic response models eliminating sensitive property leakage.
- **API4:2023 Unrestricted Resource Consumption**: Sliding-window rate limiting & pagination caps.
- **API5:2023 BFLA**: Declarative role-based access control (RBAC) on administrative endpoints.
- **API7:2023 SSRF**: Strict outbound URL parsing blocking loopback, RFC1918, and AWS metadata (169.254.169.254).

## Quickstart

### 1. Run Automated Security Test Suite
```bash
python3 starter/run_security_tests.py
```

### 2. Start the API Server
```bash
uvicorn starter.main:app --reload --port 8000
```
Interactive documentation available at `http://localhost:8000/docs` (Swagger UI) and `http://localhost:8000/redoc`.

### 3. Run with Docker Compose
```bash
docker compose -f starter/docker-compose.yml up -d
curl http://localhost:8000/healthz
```

## Design Rationale
See [`DESIGN-NOTES.md`](DESIGN-NOTES.md) for architectural details on why this kit emphasizes interactive OpenAPI documentation and automated Pytest harnesses.
