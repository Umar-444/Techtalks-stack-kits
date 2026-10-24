"""Deeper proofs for the controls declared in security/checks.json.

test_owasp_top10.py covers the happy path of each control. This suite attacks
them: forged and downgraded tokens, every private-address form, over-limit
pagination and payloads, and the container file. Everything is in-process
against the in-memory stores; no network is touched (SSRF targets are IP
literals, so no DNS lookup of an external host happens).
"""

import os
import re
import time

import jwt
import pytest
from fastapi.testclient import TestClient

import main
from main import SECRET_KEY, app

client = TestClient(app)
STARTER = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PUBLIC = "http://93.184.216.34/"
OVER_LIMIT = 200_000  # fixed on purpose: must exceed any sane cap, independent of the app constant


def bearer(sub="user-alice", role="user", key=SECRET_KEY, alg="HS256", **extra):
    token = jwt.encode({"sub": sub, "role": role, **extra}, key, algorithm=alg)
    return {"Authorization": f"Bearer {token}"}


# --- API1-01: BOLA ----------------------------------------------------------

def test_owner_can_read_own_document_and_stranger_cannot():
    assert client.get("/api/v1/documents/doc-2", headers=bearer("user-bob")).status_code == 200
    assert client.get("/api/v1/documents/doc-2", headers=bearer("user-mallory")).status_code == 403


def test_listing_never_includes_other_owners_documents():
    docs = client.get("/api/v1/documents", headers=bearer("user-bob")).json()
    assert docs and all(d["owner_id"] == "user-bob" for d in docs)


def test_admin_role_is_the_only_bypass():
    assert client.get("/api/v1/documents/doc-1", headers=bearer("user-bob", role="admin")).status_code == 200


# --- API2-01: JWT verification ---------------------------------------------

def test_token_signed_with_wrong_key_is_rejected():
    headers = bearer(key="attacker-key-0123456789abcdef0123")  # pragma: allowlist secret
    assert client.get("/api/v1/documents/doc-1", headers=headers).status_code == 401


def test_alg_none_token_is_rejected():
    forged = jwt.encode({"sub": "user-alice", "role": "admin"}, key=None, algorithm="none")
    r = client.get("/api/v1/documents/doc-1", headers={"Authorization": f"Bearer {forged}"})
    assert r.status_code == 401


def test_token_with_unexpected_algorithm_is_rejected():
    r = client.get("/api/v1/documents/doc-1", headers=bearer(alg="HS512", key=SECRET_KEY))
    assert r.status_code == 401


def test_expired_token_is_rejected():
    r = client.get("/api/v1/documents/doc-1", headers=bearer(exp=int(time.time()) - 60))
    assert r.status_code == 401


def test_token_without_subject_is_rejected():
    token = jwt.encode({"role": "admin"}, SECRET_KEY, algorithm="HS256")
    r = client.get("/api/v1/documents/doc-1", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401


def test_non_bearer_scheme_is_rejected():
    r = client.get("/api/v1/documents/doc-1", headers={"Authorization": "Basic abc"})
    assert r.status_code == 401


# --- API3-01: property filtering -------------------------------------------

def test_internal_fields_never_leave_the_api():
    body = client.get("/api/v1/users/user-bob", headers=bearer()).json()
    assert set(body) == {"id", "username", "email", "role"}


# --- API4-01 / 02 / 03: resource consumption --------------------------------

def test_rate_limit_is_per_user():
    for _ in range(5):
        assert client.get("/api/v1/rate-limited-action", headers=bearer("user-r1")).status_code == 200
    assert client.get("/api/v1/rate-limited-action", headers=bearer("user-r1")).status_code == 429
    assert client.get("/api/v1/rate-limited-action", headers=bearer("user-r2")).status_code == 200


def test_rate_limit_window_expires(monkeypatch):
    for _ in range(5):
        client.get("/api/v1/rate-limited-action", headers=bearer("user-r3"))
    assert client.get("/api/v1/rate-limited-action", headers=bearer("user-r3")).status_code == 429
    real = time.time()
    monkeypatch.setattr(main.time, "time", lambda: real + 61)
    assert client.get("/api/v1/rate-limited-action", headers=bearer("user-r3")).status_code == 200


@pytest.mark.parametrize("query", ["limit=51", "limit=0", "limit=-1", "skip=-1", "limit=abc"])
def test_pagination_bounds_are_enforced(query):
    assert client.get(f"/api/v1/documents?{query}", headers=bearer()).status_code == 422


def test_pagination_max_is_accepted():
    assert client.get("/api/v1/documents?limit=50", headers=bearer()).status_code == 200


def test_oversized_json_body_is_rejected():
    big = {"callback_url": PUBLIC + "a" * OVER_LIMIT}
    r = client.post("/api/v1/webhooks/verify", headers=bearer(), json=big)
    assert r.status_code == 413


def test_oversized_chunked_body_without_content_length_is_rejected():
    def chunks():
        yield b'{"callback_url": "' + PUBLIC.encode() + b"a" * OVER_LIMIT + b'"}'

    headers = {**bearer(), "Content-Type": "application/json"}
    r = client.post("/api/v1/webhooks/verify", headers=headers, content=chunks())
    assert r.status_code == 413


def test_body_cap_is_reasonable():
    assert main.MAX_BODY_BYTES <= 128 * 1024


def test_normal_sized_body_still_accepted():
    r = client.post("/api/v1/webhooks/verify", headers=bearer(), json={"callback_url": PUBLIC})
    assert r.status_code == 200


# --- API5-01: BFLA ----------------------------------------------------------

def test_admin_route_requires_authentication_and_role():
    assert client.delete("/api/v1/admin/users/user-bob").status_code == 401
    assert client.delete("/api/v1/admin/users/user-bob", headers=bearer(role="user")).status_code == 403


# --- API7-01 / 02: SSRF ------------------------------------------------------

@pytest.mark.parametrize("url", [
    "http://169.254.169.254/latest/meta-data/",
    "http://127.0.0.1/",
    "http://127.1.2.3/",
    "http://10.0.0.5/",
    "http://172.16.0.9/",
    "http://192.168.1.1/",
    "http://0.0.0.0/",
    "http://localhost/",
])
def test_private_and_metadata_targets_are_blocked(url):
    r = client.post("/api/v1/webhooks/verify", headers=bearer(), json={"callback_url": url})
    assert r.status_code == 403, url


@pytest.mark.parametrize("url", ["file:///etc/passwd", "gopher://127.0.0.1/", "ftp://example.com/", "http:///nohost"])
def test_non_http_schemes_and_hostless_urls_are_rejected(url):
    r = client.post("/api/v1/webhooks/verify", headers=bearer(), json={"callback_url": url})
    assert r.status_code == 400, url


def test_public_ip_literal_is_allowed():
    r = client.post("/api/v1/webhooks/verify", headers=bearer(), json={"callback_url": PUBLIC})
    assert r.status_code == 200 and r.json()["target_ip"] == "93.184.216.34"


# --- API8-01: strict request schemas ---------------------------------------

def test_webhook_request_rejects_unknown_fields():
    r = client.post("/api/v1/webhooks/verify", headers=bearer(), json={"callback_url": PUBLIC, "extra": "x"})
    assert r.status_code == 422


# --- OPS-01 / OPS-02 --------------------------------------------------------

def test_healthz_needs_no_credentials():
    assert client.get("/healthz").status_code == 200


def test_dockerfile_is_rootless_and_has_healthcheck():
    with open(os.path.join(STARTER, "Dockerfile"), encoding="utf-8") as handle:
        text = handle.read()
    users = re.findall(r"^USER\s+(\S+)", text, re.M)
    assert users and users[-1].split(":")[0] == "10001"
    assert "/healthz" in text
