# Testing, Verification & CI Invariants

# Testing Standards, HTML Fragment Assertions & CI Pipeline

## 1. Pytest Test Client & In-Memory Isolation
- Always configure an isolated temporary database in tests so unit runs never mutate real files:
  ```python
  import tempfile
  import os
  import pytest
  from app import create_app
  from app.db import init_db

  @pytest.fixture
  def app():
      db_fd, db_path = tempfile.mkstemp()
      app = create_app({
          "TESTING": True,
          "DATABASE": db_path,
          "WTF_CSRF_ENABLED": False,  # Simplified client testing, or enabled with test CSRF
      })
      with app.app_context():
          init_db()
      yield app
      os.close(db_fd)
      os.unlink(db_path)

  @pytest.fixture
  def client(app):
      return app.test_client()
  ```

## 2. Testing HTMX Fragment Swaps vs Full Page Navigation
- Assert that requests without `HX-Request` return full HTML shells (`<html`, `<head`, `<body>`).
- Assert that requests with `headers={"HX-Request": "true"}` return ONLY targeted HTML fragments:
  ```python
  def test_list_items_htmx_partial(client):
      res = client.get("/items", headers={"HX-Request": "true"})
      assert res.status_code == 200
      assert b"<tr" in res.data or b"<div class=\"item-row\"" in res.data
      assert b"<!DOCTYPE html>" not in res.data
  ```

## 3. Automated Security Audits in CI
- Code must pass:
  1. `gitleaks detect --no-git` with 0 secret leaks.
  2. `semgrep scan --config p/owasp-top-ten --config p/security-code-scan` with 0 blocking findings.
  3. `python tools/validate_manifest.py` ensuring complete physical manifest parity.
  4. `python tools/transpiler.py --check` guaranteeing 0 dialect drift.
