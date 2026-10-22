import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.vector_store import QdrantVectorService
from app.graph import run_agentic_rag, rewrite_query_node, grade_documents_node
from app.evals import RagasEvaluator

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["graph"] == "ready"

def test_cors_configuration():
    # Preflight check with allowed origin
    response = client.options(
        "/api/v1/rag/query",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST"
        }
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"

def test_qdrant_vector_service_and_tenant_isolation():
    vs = QdrantVectorService()
    vs.index_documents([
        {"id": "doc-tenant1", "content": "LangGraph manages state cycles for agentic RAG.", "tenant_id": "tenant-alpha"},
        {"id": "doc-tenant2", "content": "Confidential financial quarterly projections.", "tenant_id": "tenant-beta"}
    ])

    # Search for tenant-alpha
    res_alpha = vs.search(query="LangGraph state", tenant_id="tenant-alpha")
    assert len(res_alpha) == 1
    assert res_alpha[0]["id"] == "doc-tenant1"

    # Search for tenant-beta
    res_beta = vs.search(query="financial projections", tenant_id="tenant-beta")
    assert len(res_beta) == 1
    assert res_beta[0]["id"] == "doc-tenant2"

    # Search crossing tenant boundary
    res_isolated = vs.search(query="financial projections", tenant_id="tenant-alpha")
    assert len(res_isolated) == 0

def test_query_rewrite_node():
    state = {
        "question": "what is langgraph?",
        "tenant_id": "tenant-alpha",
        "documents": [],
        "generation": "",
        "iterations": 0,
        "max_iterations": 3,
        "groundedness_score": 0.0,
        "status": "init"
    }
    rewritten = rewrite_query_node(state)
    assert rewritten["iterations"] == 1
    assert "Semantic retrieval for: what is langgraph" in rewritten["question"]
    assert rewritten["status"] == "query_rewritten"

def test_ragas_evaluation_groundedness():
    evaluator = RagasEvaluator()
    docs = [{"content": "Qdrant is an open-source vector database written in Rust."}]
    
    # Grounded answer
    grounded_ans = "Qdrant is an open-source vector database written in Rust."
    score = evaluator.evaluate_groundedness("vector database", docs, grounded_ans)
    assert score >= 0.85

    # Hallucinated answer
    hallucinated_ans = "Solar eclipses occur only during the vernal equinox."
    score_low = evaluator.evaluate_groundedness("vector database", docs, hallucinated_ans)
    assert score_low < 0.30

def test_agentic_rag_full_cycle():
    # Index document first
    client.post(
        "/api/v1/documents/index",
        json={
            "documents": [
                {
                    "id": "kb-01",
                    "content": "LangGraph cycles allow adaptive re-querying and Ragas verification.",
                    "tenant_id": "org-prod"
                }
            ]
        }
    )

    # Execute query
    response = client.post(
        "/api/v1/rag/query",
        json={
            "question": "How do LangGraph cycles help?",
            "tenant_id": "org-prod",
            "max_iterations": 3
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["retrieved_documents"]) >= 1
    assert data["groundedness_score"] >= 0.0

def test_eval_endpoint_api():
    response = client.post(
        "/api/v1/rag/eval",
        json={
            "question": "What is Qdrant?",
            "context": ["Qdrant provides vector payload indexing and filtering."],
            "answer": "Qdrant provides vector payload indexing and filtering."
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["groundedness"] >= 0.85
    assert data["is_hallucination"] is False
