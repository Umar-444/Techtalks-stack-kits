import pytest
from fastapi.testclient import TestClient
from qdrant_client import QdrantClient
from app.main import app
from app.services.qdrant_service import qdrant_service

@pytest.fixture(autouse=True)
def setup_in_memory_qdrant():
    # Force in-memory Qdrant instance for test isolation
    qdrant_service._client = QdrantClient(":memory:")
    qdrant_service.initialize()
    yield

client = TestClient(app)

def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["ok", "degraded"]
    assert data["app"] == "rag-fastapi-qdrant"

def test_document_ingest():
    payload = {
        "document_id": "test-doc-001",
        "title": "Refund and Billing Policy",
        "text": "Enterprise customers may request full invoice refunds within 30 days of service activation.",
        "metadata": {
            "department": "finance",
            "tenant_id": "tenant-test-a"
        }
    }
    response = client.post("/api/v1/documents/ingest", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["document_id"] == "test-doc-001"
    assert data["status"] == "indexed"
    assert data["chunks_created"] >= 1

def test_semantic_search():
    # First ingest document
    client.post("/api/v1/documents/ingest", json={
        "document_id": "test-doc-search",
        "title": "Hardware Allowance",
        "text": "Employees receive up to $1,000 annually for remote work hardware purchases.",
        "metadata": {"tenant_id": "tenant-test-a"}
    })

    # Search with matching query
    search_payload = {
        "query": "How much hardware budget do employees receive?",
        "top_k": 3,
        "score_threshold": 0.10,
        "filter": {"tenant_id": "tenant-test-a"}
    }
    response = client.post("/api/v1/query", json=search_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["results_count"] >= 1
    assert len(data["sources"]) >= 1
    assert data["sources"][0]["document_id"] == "test-doc-search"
    assert "assembled_context" in data

def test_tenant_filtered_search():
    # Ingest for tenant-a
    client.post("/api/v1/documents/ingest", json={
        "document_id": "doc-tenant-a",
        "text": "Confidential roadmap for Project Alpha.",
        "metadata": {"tenant_id": "tenant-a"}
    })

    # Ingest for tenant-b
    client.post("/api/v1/documents/ingest", json={
        "document_id": "doc-tenant-b",
        "text": "Confidential roadmap for Project Beta.",
        "metadata": {"tenant_id": "tenant-b"}
    })

    # Search strictly for tenant-b
    response = client.post("/api/v1/query", json={
        "query": "Project roadmap",
        "top_k": 5,
        "score_threshold": 0.0,
        "filter": {"tenant_id": "tenant-b"}
    })
    assert response.status_code == 200
    data = response.json()
    for source in data["sources"]:
        assert source["metadata"]["tenant_id"] == "tenant-b"
        assert source["document_id"] != "doc-tenant-a"
