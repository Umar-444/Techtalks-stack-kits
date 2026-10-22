from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_healthcheck():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_run_agent_endpoint():
    response = client.post("/api/v1/run-agent", json={"query": "Automated security audit"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "Synthesized Intelligence Report" in data["report"]
