import os
import pytest

os.environ["TEST_MODE"] = "true"
os.environ["APP_ENV"] = "test"
os.environ["RESTRICT_OUTBOUND_EGRESS"] = "true"

from app.schemas import (
    IngestRequest,
    QueryRequest,
    DataClassification,
    EvaluationRequest
)
from app.services.rag_service import rag_service

@pytest.mark.asyncio
async def test_healthz():
    assert rag_service.settings.restrict_outbound_egress is True
    assert rag_service.settings.test_mode is True

@pytest.mark.asyncio
async def test_document_ingest():
    req = IngestRequest(
        document_id="doc-security-policy-01",
        title="Saudi PDPL Cloud Isolation Policy",
        tenant_id="tenant-alpha",
        classification=DataClassification.CONFIDENTIAL,
        text="Proprietary patient healthcare records within the Kingdom must be processed on airgapped compute clusters without public internet egress.",
        chunk_size=256,
        chunk_overlap=32
    )
    res = await rag_service.ingest_document(req)
    assert res.document_id == "doc-security-policy-01"
    assert res.chunks_created >= 1
    assert res.status == "ingested"
    assert res.airgap_safe is True

@pytest.mark.asyncio
async def test_query_retrieval_success():
    req = QueryRequest(
        query="What are the compute requirements for patient healthcare records?",
        tenant_id="tenant-alpha",
        user_classification=DataClassification.CONFIDENTIAL,
        top_k=2
    )
    res = await rag_service.query_knowledge_base(req)
    assert res.airgap_safe is True
    assert res.privacy_verified is True
    assert len(res.sources) >= 1
    assert res.sources[0].document_id == "doc-security-policy-01"
    assert "patient healthcare records" in res.sources[0].text_snippet.lower()
    assert "patient healthcare records" in res.answer.lower() or "doc-security-policy-01" in res.answer

@pytest.mark.asyncio
async def test_cross_tenant_isolation():
    req = QueryRequest(
        query="What are the compute requirements for patient healthcare records?",
        tenant_id="tenant-beta",
        user_classification=DataClassification.RESTRICTED,
        top_k=2
    )
    res = await rag_service.query_knowledge_base(req)
    assert len(res.sources) == 0
    assert "No relevant documentation was found" in res.answer

@pytest.mark.asyncio
async def test_classification_clearance_filtering():
    req = QueryRequest(
        query="What are the compute requirements for patient healthcare records?",
        tenant_id="tenant-alpha",
        user_classification=DataClassification.PUBLIC,
        top_k=2
    )
    res = await rag_service.query_knowledge_base(req)
    assert len(res.sources) == 0

@pytest.mark.asyncio
async def test_offline_evaluation():
    eval_req = EvaluationRequest(
        query="What are the compute requirements for patient healthcare records?",
        ground_truth_context="Proprietary patient healthcare records within the Kingdom must be processed on airgapped compute clusters without public internet egress.",
        generated_answer="Patient healthcare records must be processed on airgapped compute clusters without public internet egress."
    )
    res = rag_service.evaluate_offline(eval_req)
    assert res.groundedness_score > 0.5
    assert res.context_relevance_score > 0.5
    assert res.is_hallucination_detected is False
    assert res.airgap_compliant is True
