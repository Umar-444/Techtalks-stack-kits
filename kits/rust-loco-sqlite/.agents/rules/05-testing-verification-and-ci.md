# 05 Testing Verification And Ci

# Testing, Verification, and CI Standards

1. **In-Memory SQLite Testing**: Execute unit and integration tests against in-memory SQLite instances (`sqlite::memory:`) configured with isolated schemas for fast, deterministic, and parallel test execution.
2. **Loco Request Test Harness**: Author integration tests using `loco_rs::testing::prelude::*` utilities (`request().get("/healthz").await`). Verify HTTP status codes and JSON response contracts.
3. **Liveness and Readiness Probes**: Expose `/healthz` returning HTTP 200 and machine-readable service status for container orchestrators.
4. **Supply Chain Security**: Enforce `cargo audit` in CI to detect vulnerabilities in dependencies and verify license compliance with `cargo deny`.
5. **Transpiler Zero-Drift**: Validate that all 6 agent dialects match source rules using `python tools/transpiler.py --check` in continuous integration.

