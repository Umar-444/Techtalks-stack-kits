import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.weaviate_service import WeaviateVectorService
from app.pipeline import HaystackRAGPipeline, FaithfulnessEvaluator

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["pipeline"] == "ready"

def test_cors_whitelist():
    response = client.options(
        "/api/v1/rag/query",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST"
        }
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"

def test_weaviate_hybrid_search_and_tenant_isolation():
    ws = WeaviateVectorService()
    ws.index_documents([
        {"id": "doc-a1", "content": "Haystack 2.5 uses explicit DAG pipelines.", "tenant_id": "tenant-corp"},
        {"id": "doc-b1", "content": "Top secret executive compensation schedules.", "tenant_id": "tenant-finance"}
    ])

    # Search within tenant-corp
    res_corp = ws.hybrid_search(query="Haystack DAG pipelines", tenant_id="tenant-corp", alpha=0.65)
    assert len(res_corp) == 1
    assert res_corp[0]["id"] == "doc-a1"

    # Search within tenant-finance
    res_fin = ws.hybrid_search(query="compensation schedules", tenant_id="tenant-finance", alpha=0.65)
    assert len(res_fin) == 1
    assert res_fin[0]["id"] == "doc-b1"

    # Cross-tenant boundary test: Searching for finance terms in corp tenant must yield 0 results
    res_isolated = ws.hybrid_search(query="compensation schedules", tenant_id="tenant-corp", alpha=0.65)
    assert len(res_isolated) == 0

def test_faithfulness_evaluator():
    evaluator = FaithfulnessEvaluator()
    docs = [{"content": "Weaviate is an open-source vector database supporting hybrid search."}]

    grounded_ans = "Weaviate is an open-source vector database supporting hybrid search."
    score = evaluator.evaluate(answer=grounded_ans, documents=docs)
    assert score >= 0.85

    ungrounded_ans = "Quantum computing relies strictly on topological qubits."
    low_score = evaluator.evaluate(answer=ungrounded_ans, documents=docs)
    assert low_score < 0.30

def test_haystack_pipeline_query():
    # Ingest document
    client.post(
        "/api/v1/documents/index",
        json={
            "documents": [
                {
                    "id": "hw-01",
                    "content": "Deepset Haystack allows inspectable pipeline execution with Weaviate.",
                    "tenant_id": "team-ml"
                }
            ]
        }
    )

    response = client.post(
        "/api/v1/rag/query",
        json={
            "question": "What does Deepset Haystack allow?",
            "tenant_id": "team-ml",
            "alpha": 0.65
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["retrieved_chunks"]) >= 1
    assert data["faithfulness_score"] >= 0.85

def test_eval_endpoint_api():
    response = client.post(
        "/api/v1/rag/eval",
        json={
            "question": "What is hybrid search?",
            "context": ["Hybrid search combines sparse BM25 and dense vectors."],
            "answer": "Hybrid search combines sparse BM25 and dense vectors."
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["faithfulness"] >= 0.85
    assert data["is_grounded"] is True
