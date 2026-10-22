---
id: "05-testing-verification-and-ci"
title: "Testing, Container Hardening & Token Benchmark"
description: "Testing standards using AsyncTestClient, pytest-asyncio, in-memory SQLite isolation, and rootless Docker execution (UID 10001)."
globs: ["tests/**/*.py", "Dockerfile", "evals/**"]
alwaysApply: true
---

# 05 - Testing, Container Hardening & Token Benchmark

## 1. Async Testing with AsyncTestClient
- Test Litestar routes using `litestar.testing.AsyncTestClient`:
  ```python
  import pytest
  from litestar.testing import AsyncTestClient
  from app.main import app

  @pytest.mark.asyncio
  async def test_health_endpoint():
      async with AsyncTestClient(app=app) as client:
          res = await client.get("/health")
          assert res.status_code == 200
          data = res.json()
          assert data["status"] == "ok"
          assert data["framework"] == "litestar"
  ```
- Fast execution invariant: Tests must complete within 2 seconds using an in-memory SQLite test database.

## 2. Container Hardening & Rootless Execution
- Docker containers must execute as an unprivileged user (`USER 10001:10001`):
  ```dockerfile
  RUN groupadd -g 10001 appgroup && \
      useradd -u 10001 -g appgroup -s /bin/sh appuser
  USER 10001:10001
  ```
- Discard build tools and header libraries in the multi-stage builder.

## 3. Token Benchmark Metric (Document 20 Part F)
- Benchmark verification: Run `python evals/runner.py --kit python-litestar-postgresql`.
- Target token consumption: ~22,100 tokens (Efficiency Tier: **A**).
- Justification: Clean layered dependency injection and first-class DTO typing eliminate boilerplate and ensure fast, predictable code generation by AI agents.
