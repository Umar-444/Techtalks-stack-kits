import pytest
from fastapi.testclient import TestClient
from main import app, SECRET_KEY
import jwt

client = TestClient(app)

def make_token(sub: str, role: str = "user") -> str:
    return jwt.encode({"sub": sub, "role": role}, SECRET_KEY, algorithm="HS256")

def test_healthz_endpoint():
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
    assert resp.json()["app"] == "security-owasp-api"

def test_api1_bola_prevention():
    bob_token = make_token("user-bob")
    resp = client.get("/api/v1/documents/doc-1", headers={"Authorization": f"Bearer {bob_token}"})
    assert resp.status_code == 403
    assert "BOLA protection" in resp.json()["detail"]

def test_api1_bola_authorized_owner():
    alice_token = make_token("user-alice")
    resp = client.get("/api/v1/documents/doc-1", headers={"Authorization": f"Bearer {alice_token}"})
    assert resp.status_code == 200
    assert resp.json()["id"] == "doc-1"

def test_api2_broken_auth_missing_token():
    resp = client.get("/api/v1/documents/doc-1")
    assert resp.status_code == 401

def test_api2_broken_auth_invalid_token():
    resp = client.get("/api/v1/documents/doc-1", headers={"Authorization": "Bearer bad-token"})
    assert resp.status_code == 401

def test_api3_bopla_no_sensitive_fields_leaked():
    alice_token = make_token("user-alice")
    resp = client.get("/api/v1/users/user-bob", headers={"Authorization": f"Bearer {alice_token}"})
    assert resp.status_code == 200
    data = resp.json()
    assert "internal_secret" not in data
    assert "email" in data

def test_api4_rate_limiting():
    alice_token = make_token("user-rate-tester")
    for _ in range(5):
        resp = client.get("/api/v1/rate-limited-action", headers={"Authorization": f"Bearer {alice_token}"})
        assert resp.status_code == 200
    # 6th request must trigger 429
    resp = client.get("/api/v1/rate-limited-action", headers={"Authorization": f"Bearer {alice_token}"})
    assert resp.status_code == 429
    assert "Rate limit exceeded" in resp.json()["detail"]

def test_api5_bfla_prevention():
    bob_token = make_token("user-bob", role="user")
    resp = client.delete("/api/v1/admin/users/user-bob", headers={"Authorization": f"Bearer {bob_token}"})
    assert resp.status_code == 403
    assert "BFLA protection" in resp.json()["detail"]

def test_api5_bfla_authorized_admin():
    alice_token = make_token("user-alice", role="admin")
    resp = client.delete("/api/v1/admin/users/user-bob", headers={"Authorization": f"Bearer {alice_token}"})
    assert resp.status_code == 200

def test_api7_ssrf_metadata_blocked():
    alice_token = make_token("user-alice")
    resp = client.post(
        "/api/v1/webhooks/verify",
        headers={"Authorization": f"Bearer {alice_token}"},
        json={"callback_url": "http://169.254.169.254/latest/meta-data/"}
    )
    assert resp.status_code == 403
    assert "SSRF protection" in resp.json()["detail"]

def test_api7_ssrf_loopback_blocked():
    alice_token = make_token("user-alice")
    resp = client.post(
        "/api/v1/webhooks/verify",
        headers={"Authorization": f"Bearer {alice_token}"},
        json={"callback_url": "http://127.0.0.1:8000/internal"}
    )
    assert resp.status_code == 403
    assert "SSRF protection" in resp.json()["detail"]
