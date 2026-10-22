# Testing, Verification, and CI Invariants

1. **Fiber Test Harness**: Execute unit and integration tests using `app.Test(req, timeoutMs)`. Tests must run against the in-memory Fiber app without opening local TCP ports.
2. **Deterministic Test Isolation**: Pytest / Go test cases must run independently with mock or in-memory fallback, ensuring the entire test suite passes in under 3 seconds.
3. **Transpiler Zero Drift**: Single-source rules in `rules/source/` must compile to all 6 agent dialects (`CLAUDE.md`, Cursor, Codex, Copilot, Cline, Antigravity) with zero drift.
4. **Data Race Auditing**: Run all Go tests with `-race` flag enabled (`go test -race ./...`) to catch buffer reuse data races.
5. **Semgrep SAST Compliance**: Pass all configured Semgrep security and OWASP rules with zero blocking findings.
