# Verification Guide: Go + Chi + templ + HTMX + sqlc + PostgreSQL

Follow this 6-phase verification guide to confirm that the Go + Chi + templ + HTMX stack is functioning cleanly with compile-time type safety, zero ORM overhead, and complete security compliance.

---

## Phase 1: Toolchain & Dependency Verification
Verify Go runtime and required CLI code generators:
```bash
go version
templ --version || echo "Install: go install github.com/a-h/templ/cmd/templ@latest"
sqlc version || echo "Install: go install github.com/sqlc-dev/sqlc/cmd/sqlc@latest"
```
**Expected Output:** Go 1.23+ with `templ` and `sqlc` available.

---

## Phase 2: Manifest & Transpiler Zero-Drift Check
Run manifest validation and check for dialect drift:
```bash
python tools/validate_manifest.py kits/go-chi-templ-htmx/kit.yaml
python tools/transpiler.py --kit kits/go-chi-templ-htmx --check
```
**Expected Output:**
```
SUCCESS: Kit manifest and physical layer files passed all validation checks!
=== Transpiling 5 rules for: Go + Chi + templ + HTMX + sqlc + PostgreSQL ===
[PASSED] All agent dialect outputs match rules/source/* perfectly!
```

---

## Phase 3: Automated Go Unit Test Suite
Run the Go test suite:
```bash
cd starter
go test -v ./...
```
**Expected Output:**
```
=== RUN   TestHealthEndpoint
--- PASS: TestHealthEndpoint (0.00s)
=== RUN   TestRootEndpoint
--- PASS: TestRootEndpoint (0.00s)
PASS
ok      starter 0.02s
```

---

## Phase 4: Semgrep SAST & Security Invariant Audit
Scan all Go files and Docker configurations for security vulnerabilities:
```bash
semgrep scan --config "p/owasp-top-ten" --config "p/security-code-scan" --error
```
**Expected Output:**
```
Scan completed successfully.
Findings: 0 (0 blocking)
```

---

## Phase 5: Health & Token-Light Invariant Probe
Start the service and check the `/health` endpoint:
```bash
curl -s http://localhost:8080/health | jq .
```
**Expected Output:**
```json
{
  "status": "ok",
  "framework": "chi",
  "token_light": true
}
```

---

## Phase 6: HTMX Partial Fragment Verification
Simulate an asynchronous HTMX request by sending the `HX-Request: true` header:
```bash
curl -s -H "HX-Request: true" http://localhost:8080/
```
**Expected Output:** Returns HTML markup or targeted fragment without full document boilerplate.
