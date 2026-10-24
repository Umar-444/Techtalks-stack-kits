"""Structured logging, request correlation, and an audit trail.

Covers OWASP A09:2025 (Security Logging & Alerting Failures):

  - every log line is JSON with a request id, so events can be correlated
  - sensitive keys are redacted before a record is ever formatted, not after
  - mutations are written to an append-only audit table

Redaction happens in the formatter rather than at call sites because a call
site that forgets is exactly how secrets reach logs (CWE-532).
"""

from __future__ import annotations

import json
import logging
import re
import sys
import time
import uuid

from flask import g, has_request_context, request

from app.db import get_db

#: Keys whose values must never be written to a log record.
SENSITIVE_KEYS = frozenset({
    "password", "passwd", "secret", "token", "csrf_token", "authorization",
    "api_key", "apikey", "access_token", "refresh_token", "session",
    "cookie", "private_key", "secret_key",
})

REDACTED = "[REDACTED]"

#: Matches secret-looking values even when they appear inside free text.
_INLINE_SECRET = re.compile(
    r"\b(sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})\b"
)


def redact(value):
    """Recursively strip sensitive values from a structure bound for a log."""
    if isinstance(value, dict):
        return {
            key: (REDACTED if key.lower() in SENSITIVE_KEYS else redact(item))
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [redact(item) for item in value]
    if isinstance(value, str):
        return _INLINE_SECRET.sub(REDACTED, value)
    return value


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "message": redact(record.getMessage()),
        }
        if has_request_context():
            payload["request_id"] = getattr(g, "request_id", None)
            payload["method"] = request.method
            payload["path"] = request.path
        extra = getattr(record, "context", None)
        if extra:
            payload["context"] = redact(extra)
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, separators=(",", ":"))


def record_audit(action: str, entity: str, entity_id=None, detail=None) -> None:
    """Append one row to the audit trail. Never raises into the request path."""
    try:
        db = get_db()
        db.execute(
            "INSERT INTO audit_log (request_id, action, entity, entity_id, detail)"
            " VALUES (?, ?, ?, ?, ?)",
            (
                getattr(g, "request_id", None),
                action,
                entity,
                str(entity_id) if entity_id is not None else None,
                json.dumps(redact(detail)) if detail is not None else None,
            ),
        )
        db.commit()
    except Exception:  # pragma: no cover - auditing must not break a request
        logging.getLogger("app.audit").exception("failed to write audit row")


def init_app(app) -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    app.logger.handlers = [handler]
    app.logger.setLevel(logging.INFO if not app.debug else logging.DEBUG)
    app.logger.propagate = False

    @app.before_request
    def _assign_request_id():
        # Honour an upstream id so traces survive a proxy hop.
        g.request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex[:16]
        g.request_started = time.perf_counter()

    @app.after_request
    def _log_request(response):
        duration_ms = round((time.perf_counter() - getattr(g, "request_started", time.perf_counter())) * 1000, 2)
        app.logger.info(
            "request complete",
            extra={"context": {"status": response.status_code, "duration_ms": duration_ms}},
        )
        response.headers["X-Request-ID"] = getattr(g, "request_id", "")
        return response
