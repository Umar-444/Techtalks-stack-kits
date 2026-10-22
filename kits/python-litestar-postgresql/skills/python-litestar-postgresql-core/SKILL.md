---
name: "python-litestar-postgresql-core"
description: "Core operational workflows, Litestar application lifecycle management, Redis caching, and Token-Light evaluation."
---

# Skill: Python Litestar + PostgreSQL + Redis Core Operations

Use this skill for server lifecycle management, health monitoring, Redis caching, and automated benchmark evaluations.

## 1. Application Entrypoint & Startup
Start the Litestar ASGI application with Uvicorn:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 2. Health & Readiness Probe
```bash
curl -s http://localhost:8000/health | jq .
```
Expected output:
```json
{
  "status": "ok",
  "framework": "litestar",
  "typing": "strict"
}
```

## 3. Token-Light Benchmark Evaluation (Document 20 Part F)
Execute the token benchmark runner:
```bash
python evals/runner.py --kit python-litestar-postgresql
```
Verifies:
- Manifest valid and all physical layers verified.
- Transpiler zero-drift confirmed across 6 agent dialects.
- Secret leaks: 0 findings.
- Total build token consumption: ~22,100 tokens (Efficiency Tier: **A**).
