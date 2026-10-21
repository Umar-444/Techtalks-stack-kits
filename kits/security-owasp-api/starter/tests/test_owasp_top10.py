import pytest
from fastapi.testclient import TestClient
from main import app, SECRET_KEY
import jwt

client = TestClient(app)

def make_token(sub: str, role: str = "user") -> str:
    return jwt.encode({"sub": sub, "role": role}, SECRET_KEY, algorithm="HS256")

def test_api1_bola_prevention():
    bob_token = make_token("user-bob")
    resp = client.get("/api/v1/documents/doc-1", headers={"Authorization": f"Bearer {bob_token}"})
    assert resp.status_code == 403
    assert "BOLA protection" in resp.json()["detail"]

def test_api2_broken_auth_missing_token():
    resp = client.get("/api/v1/documents/doc-1")
    assert resp.status_code == 401

def test_api5_bfla_prevention():
    alice_token = make_token("user-alice", role="user")
    resp = client.delete("/api/v1/admin/users/user-bob", headers={"Authorization": f"Bearer {alice_token}"})
    assert resp.status_code == 403
    assert "BFLA protection" in resp.json()["detail"]

def test_legitimate_access():
    alice_token = make_token("user-alice")
    resp = client.get("/api/v1/documents/doc-1", headers={"Authorization": f"Bearer {alice_token}"})
    assert resp.status_code == 200
    assert resp.json()["content"] == "Alice private record"
