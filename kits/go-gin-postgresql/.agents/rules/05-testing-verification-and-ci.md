# 05 Testing Verification And Ci

# Evaluation, Testing, and CI Invariants

1. **HTTP Test Isolation**: Author unit and integration tests using standard `net/http/httptest`. Execute test assertions directly against the `*gin.Engine` without binding local network ports.
2. **Repository Mocking**: Define repository interfaces (`UserRepository`, `CacheRepository`) to enable deterministic mock testing without live database dependencies in unit suites.
3. **Transpiler Zero Drift**: Single-source rules in `rules/source/` must compile to all 6 agent dialects (`CLAUDE.md`, Cursor, Codex, Copilot, Cline, Antigravity) with zero drift.
4. **Sub-Second Execution**: Unit test suites must execute in under 2 seconds.
5. **Linting and Semgrep Cleanliness**: Pass `golangci-lint` and Semgrep OWASP security rules with zero blocking findings.

