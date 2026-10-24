"""Security controls declared in security/checks.json, verified.

The functional suite in test_app.py disables CSRF so it can exercise routes
directly. That makes it unable to prove the protection exists, so these tests
run with CSRF switched on and assert the guarantees the kit advertises.
"""

import os
import tempfile

import pytest

from app import create_app
from app.db import get_db, init_db


@pytest.fixture
def secure_app():
    """App with CSRF enabled — the production configuration."""
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        "TESTING": True,
        "DATABASE": db_path,
        "WTF_CSRF_ENABLED": True,
        "SECRET_KEY": "security-suite-key-at-least-32-characters-long",
    })
    with app.app_context():
        init_db()
    yield app
    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture
def secure_client(secure_app):
    return secure_app.test_client()


# --- SEC: CSRF protection (A06:2025, CWE-352) ------------------------------

def test_post_without_csrf_token_is_rejected(secure_client):
    res = secure_client.post("/items", data={"title": "No token"})
    assert res.status_code == 400, (
        f"CSRF protection did not reject a tokenless POST (got {res.status_code})"
    )


def test_htmx_post_without_csrf_token_is_rejected(secure_client):
    """HTMX bypasses normal form submission, so it must be covered too."""
    res = secure_client.post(
        "/items", data={"title": "No token"}, headers={"HX-Request": "true"}
    )
    assert res.status_code == 400


def test_delete_without_csrf_token_is_rejected(secure_client):
    res = secure_client.delete("/items/1", headers={"HX-Request": "true"})
    assert res.status_code == 400


def test_csrf_token_is_exposed_to_htmx(secure_client):
    """The page must publish a token for hx-headers to attach."""
    body = secure_client.get("/").data
    assert b"csrf" in body.lower(), "no CSRF token rendered for HTMX to read"


# --- SEC: response hardening (A02:2025, CWE-693) ---------------------------

@pytest.mark.parametrize("header,expected", [
    ("X-Content-Type-Options", "nosniff"),
    ("X-Frame-Options", "DENY"),
    ("Referrer-Policy", "strict-origin-when-cross-origin"),
])
def test_security_headers_present(client, header, expected):
    assert client.get("/").headers.get(header) == expected


def test_permissions_policy_disables_hardware(client):
    policy = client.get("/").headers.get("Permissions-Policy", "")
    for feature in ("geolocation", "microphone", "camera"):
        assert f"{feature}=()" in policy


# --- SEC: injection resistance (A05:2025, CWE-89 / CWE-79) -----------------

def test_search_is_parameterized_against_injection(client):
    """A quote-breaking payload must be treated as a literal, not as SQL."""
    res = client.get("/items?q=' OR 1=1 --", headers={"HX-Request": "true"})
    assert res.status_code == 200
    # Seeded rows must not leak: the payload matches nothing literally.
    assert b"Initialize SQLite WAL Mode" not in res.data


def test_injection_payload_does_not_drop_table(client, app):
    client.get("/items?q='; DROP TABLE items; --", headers={"HX-Request": "true"})
    with app.app_context():
        rows = get_db().execute("SELECT COUNT(*) AS n FROM items").fetchone()
        assert rows["n"] >= 3, "seeded table was damaged by an injection payload"


def test_stored_script_is_escaped_on_render(client):
    payload = "<script>alert('xss')</script>"
    client.post(
        "/items", data={"title": payload, "category": "general"},
        headers={"HX-Request": "true"},
    )
    body = client.get("/").data
    assert b"<script>alert(" not in body, "stored XSS rendered unescaped"
    assert b"&lt;script&gt;" in body, "payload was not HTML-escaped"


# --- SEC: SQLite durability settings (A06:2025, CWE-662) -------------------

def test_wal_mode_and_foreign_keys_enforced(app):
    with app.app_context():
        db = get_db()
        assert db.execute("PRAGMA journal_mode").fetchone()[0] == "wal"
        assert db.execute("PRAGMA foreign_keys").fetchone()[0] == 1
        assert db.execute("PRAGMA busy_timeout").fetchone()[0] >= 5000


def test_expected_indexes_exist(app):
    with app.app_context():
        names = {
            row[0] for row in get_db().execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'"
            )
        }
        assert {"idx_items_category", "idx_items_created_at"} <= names


# --- SEC: no secrets committed (A04:2025, CWE-798) -------------------------

def test_env_example_holds_no_real_secret():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env.example")
    with open(path, encoding="utf-8") as handle:
        content = handle.read()
    assert not content.startswith("﻿"), ".env.example starts with a UTF-8 BOM"
    for line in content.splitlines():
        if line.startswith("SECRET_KEY="):
            value = line.split("=", 1)[1]
            assert "change" in value.lower() or "your" in value.lower(), (
                "SECRET_KEY in .env.example looks like a real secret"
            )


# --- SEC: logging, audit trail and redaction (A09:2025, CWE-532/778) -------

def test_mutations_are_written_to_the_audit_trail(client, app):
    client.post(
        "/items", data={"title": "Audited item", "category": "security"},
        headers={"HX-Request": "true"},
    )
    with app.app_context():
        rows = get_db().execute(
            "SELECT action, entity FROM audit_log WHERE entity = 'item'"
        ).fetchall()
    assert any(r["action"] == "create" for r in rows), "create was not audited"


def test_delete_is_audited(client, app):
    client.post("/items", data={"title": "Doomed"}, headers={"HX-Request": "true"})
    client.delete("/items/1", headers={"HX-Request": "true"})
    with app.app_context():
        actions = {
            r["action"] for r in get_db().execute("SELECT action FROM audit_log")
        }
    assert "delete" in actions


def test_every_response_carries_a_request_id(client):
    assert client.get("/").headers.get("X-Request-ID"), "no correlation id on response"


def test_upstream_request_id_is_honoured(client):
    res = client.get("/", headers={"X-Request-ID": "trace-abc-123"})
    assert res.headers.get("X-Request-ID") == "trace-abc-123"


def test_sensitive_keys_are_redacted_before_logging():
    from app.observability import redact
    cleaned = redact({
        "username": "umar",
        "password": "hunter2",
        "api_key": "sk-live-9999",
        "nested": {"csrf_token": "abc", "safe": "keep"},
    })
    assert cleaned["username"] == "umar"
    assert cleaned["password"] == "[REDACTED]"
    assert cleaned["api_key"] == "[REDACTED]"
    assert cleaned["nested"]["csrf_token"] == "[REDACTED]"
    assert cleaned["nested"]["safe"] == "keep"


def test_inline_secrets_in_free_text_are_redacted():
    from app.observability import redact
    assert "sk-" not in redact("call failed with key sk-live-abcdefghijklmnop")  # pragma: allowlist secret
    assert "AKIA" not in redact("creds AKIAIOSFODNN7EXAMPLE leaked")  # pragma: allowlist secret


def test_log_output_is_json_with_request_id(app, client):
    """Attach a StringIO sink using the app's own formatter.

    Reading stdout is unreliable here: the stream handler binds sys.stdout when
    the app is built, which is before pytest swaps it. Reusing the configured
    formatter tests the same guarantee without depending on capture internals.
    """
    import io
    import json as _json
    import logging

    sink = io.StringIO()
    handler = logging.StreamHandler(sink)
    handler.setFormatter(app.logger.handlers[0].formatter)
    app.logger.addHandler(handler)
    try:
        client.get("/health")
    finally:
        app.logger.removeHandler(handler)

    structured = [line for line in sink.getvalue().strip().splitlines() if line.startswith("{")]
    assert structured, "no JSON log lines emitted"
    record = _json.loads(structured[-1])
    assert record["request_id"], "log line has no request_id"
    assert record["path"] == "/health"
    assert record["level"] == "INFO"


def test_json_formatter_redacts_secrets_in_the_record(app):
    """The formatter must redact even when a call site passes a secret through."""
    import io
    import json as _json
    import logging

    sink = io.StringIO()
    handler = logging.StreamHandler(sink)
    handler.setFormatter(app.logger.handlers[0].formatter)
    app.logger.addHandler(handler)
    try:
        app.logger.info("auth attempt", extra={"context": {"password": "hunter2"}})
    finally:
        app.logger.removeHandler(handler)

    record = _json.loads(sink.getvalue().strip().splitlines()[-1])
    assert record["context"]["password"] == "[REDACTED]"
    assert "hunter2" not in sink.getvalue()
