# Verification Guide: Flask + HTMX + SQLite

Follow this 6-phase verification guide to confirm that the Flask + HTMX + SQLite stack is functioning cleanly with zero-ceremony persistence, non-blocking WAL mode, and complete security compliance.

---

## Phase 1: Toolchain & Dependency Verification
Verify Python runtime and required tools:
```bash
python --version
pytest --version
sqlite3 --version
```
**Expected Output:** Python 3.12+, Pytest 8.3+, and SQLite 3.45+.

---

## Phase 2: Manifest & Transpiler Zero-Drift Check
Run manifest validation and check for dialect drift:
```bash
python tools/validate_manifest.py kits/flask-htmx-sqlite/kit.yaml
python tools/transpiler.py --kit kits/flask-htmx-sqlite --check
```
**Expected Output:**
```
SUCCESS: Kit manifest and physical layer files passed all validation checks!
=== Transpiling 5 rules for: Flask + HTMX + SQLite ===
[PASSED] All agent dialect outputs match rules/source/* perfectly!
```

---

## Phase 3: Application Factory & SQLite WAL Initialization
Verify database table creation and WAL mode activation:
```bash
cd kits/flask-htmx-sqlite/starter
flask --app "app:create_app()" init-db
sqlite3 instance/app.sqlite "PRAGMA journal_mode;"
```
**Expected Output:** `wal`

---

## Phase 4: Automated Pytest Suite
Run the unit test suite verifying health checks, dual-rendering, and CRUD operations:
```bash
pytest -v tests/
```
**Expected Output:**
```
============================== 5 passed in 0.45s ==============================
```

---

## Phase 5: Security Audits & Container Linting
Verify code security, zero secret leaks, and non-root Docker execution:
```bash
gitleaks detect --no-git
semgrep scan --config "p/owasp-top-ten" --config "p/security-code-scan"
grep -q "USER 10001:10001" Dockerfile && echo "Non-root user check: PASS"
```
**Expected Output:** 0 secret findings, 0 blocking Semgrep SAST findings, Non-root check PASS.

---

## Phase 6: Token-Light Efficiency Benchmark
Run the evaluator to verify the kit passes all Doc 20 Part F requirements:
```bash
python evals/runner.py --kit flask-htmx-sqlite
```
**Expected Output:** Tier A+ efficiency tier confirmed.
