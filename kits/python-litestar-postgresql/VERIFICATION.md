# Verification Guide: Python + Litestar + SQLAlchemy 2 + PostgreSQL + Redis

Follow this 6-phase verification guide to confirm that the Litestar service is functioning cleanly with strict typing, clean DI, and complete security compliance.

---

## Phase 1: Environment & Dependency Verification
Verify Python runtime and required async libraries:
```bash
python --version
pip list | grep -E "litestar|uvicorn|sqlalchemy|asyncpg|msgspec"
```
**Expected Output:** Python 3.12+ with Litestar 2.12+, SQLAlchemy 2.0+, and msgspec installed.

---

## Phase 2: Manifest & Transpiler Zero-Drift Check
Run manifest validation and check for dialect drift:
```bash
python tools/validate_manifest.py kits/python-litestar-postgresql/kit.yaml
python tools/transpiler.py --kit kits/python-litestar-postgresql --check
```
**Expected Output:**
```
SUCCESS: Kit manifest and physical layer files passed all validation checks!
=== Transpiling 5 rules for: Python + Litestar + SQLAlchemy 2 + PostgreSQL + Redis ===
[PASSED] All agent dialect outputs match rules/source/* perfectly!
```

---

## Phase 3: Automated Pytest Suite Execution
Execute the automated test suite with AsyncTestClient:
```bash
python -m pytest kits/python-litestar-postgresql/starter/tests/test_app.py -v
```
**Expected Output:**
```
test_health PASSED
test_create_and_list_items PASSED
test_tenant_isolation_get PASSED
3 passed in < 1s
```

---

## Phase 4: Semgrep SAST & Security Invariant Audit
Scan all Python files and Docker configurations for security vulnerabilities:
```bash
semgrep scan --config "p/owasp-top-ten" --config "p/security-code-scan" --error
```
**Expected Output:**
```
Scan completed successfully.
Findings: 0 (0 blocking)
```

---

## Phase 5: Health & Readiness Probe
Start the server and check the `/health` endpoint:
```bash
curl -s http://localhost:8000/health | jq .
```
**Expected Output:**
```json
{
  "status": "ok",
  "framework": "litestar",
  "typing": "strict"
}
```

---

## Phase 6: DTO Ingestion & Tenant Isolation Test
Create an item and verify that cross-tenant access returns 404:
```bash
# Create
curl -X POST http://localhost:8000/api/v1/items \
  -H "Content-Type: application/json" \
  -d '{"title": "Database Node", "tenant_id": "tenant-001", "description": "High availability cluster"}'

# Query Matching Tenant (200 OK)
curl -s "http://localhost:8000/api/v1/items/1?tenant_id=tenant-001" | jq .

# Query Cross Tenant (404 Not Found)
curl -s -o /dev/null -w "%{http_code}\n" "http://localhost:8000/api/v1/items/1?tenant_id=tenant-999"
```
**Expected Output:** `200` for matching tenant, `404` for cross-tenant request.
