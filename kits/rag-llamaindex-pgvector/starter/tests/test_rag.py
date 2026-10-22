import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.vector_service import vector_service

@pytest.fixture(autouse=True)
def setup_vector_store():
    vector_service._in_memory_nodes = []
    vector_service.initialize()
    yield

client = TestClient(app)

def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["ok", "degraded"]
    assert data["app"] == "rag-llamaindex-pgvector"

def test_document_ingest():
    payload = {
        "document_id": "test-doc-001",
        "title": "Wellness Stipend Policy",
        "text": "Full-time team members receive up to $1,200 annually for fitness and wellness expenses.",
        "metadata": {
            "department": "hr",
            "tenant_id": "tenant-test-x"
        }
    }
    response = client.post("/api/v1/documents/ingest", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["document_id"] == "test-doc-001"
    assert data["status"] == "indexed"
    assert data["nodes_created"] >= 1

def test_semantic_search():
    client.post("/api/v1/documents/ingest", json={
        "document_id": "doc-benefits",
        "title": "Benefits Guide",
        "text": "Employees receive 20 days of paid vacation annually plus national holidays.",
        "metadata": {"tenant_id": "tenant-test-x"}
    })

    search_payload = {
        "query": "How many days of paid vacation do employees receive?",
        "similarity_top_k": 3,
        "score_threshold": 0.10,
        "filter": {"tenant_id": "tenant-test-x"}
    }
    response = client.post("/api/v1/query", json=search_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["results_count"] >= 1
    assert len(data["sources"]) >= 1
    assert data["sources"][0]["document_id"] == "doc-benefits"
    assert "vacation" in data["response"]

def test_tenant_filtered_search():
    client.post("/api/v1/documents/ingest", json={
        "document_id": "doc-tenant-1",
        "text": "Project 1 confidential data.",
        "metadata": {"tenant_id": "tenant-1"}
    })

    client.post("/api/v1/documents/ingest", json={
        "document_id": "doc-tenant-2",
        "text": "Project 2 confidential data.",
        "metadata": {"tenant_id": "tenant-2"}
    })

    response = client.post("/api/v1/query", json={
        "query": "Project confidential data",
        "similarity_top_k": 5,
        "score_threshold": 0.0,
        "filter": {"tenant_id": "tenant-2"}
    })
    assert response.status_code == 200
    data = response.json()
    for source in data["sources"]:
        assert source["metadata"]["tenant_id"] == "tenant-2"
        assert source["document_id"] != "doc-tenant-1"

def test_rag_evaluation():
    eval_payload = {
        "query": "What is the wellness stipend amount?",
        "response": "The wellness stipend amount is $1,200 annually.",
        "contexts": ["Full-time team members receive up to $1,200 annually for fitness and wellness expenses."]
    }
    response = client.post("/api/v1/evaluate", json=eval_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["faithfulness_passing"] is True
    assert data["relevancy_passing"] is True
    assert data["score"] >= 0.8
