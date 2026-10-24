from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

TENANT_PATTERN = r"^[A-Za-z0-9_.-]{1,64}$"

class DocumentChunk(BaseModel):
    id: str = Field(..., min_length=1, max_length=128, description="Document identifier")
    content: str = Field(..., min_length=1, max_length=20000, description="Text chunk payload")
    tenant_id: str = Field(..., pattern=TENANT_PATTERN, description="Multi-tenant namespace (required)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom JSON metadata")

class IngestRequest(BaseModel):
    documents: List[DocumentChunk] = Field(..., min_length=1, max_length=100)

class IngestResponse(BaseModel):
    status: str
    count: int

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=1000)
    tenant_id: str = Field(..., pattern=TENANT_PATTERN, description="Multi-tenant namespace (required)")
    alpha: float = Field(default=0.65, ge=0.0, le=1.0, description="Hybrid search alpha weight (0=sparse, 1=dense)")

class QueryResponse(BaseModel):
    question: str
    answer: str
    retrieved_chunks: List[Dict[str, Any]]
    faithfulness_score: float
    pipeline_latency_ms: float

class EvalRequest(BaseModel):
    question: str = Field(..., max_length=1000)
    context: List[str] = Field(..., max_length=50)
    answer: str = Field(..., max_length=20000)

class EvalResponse(BaseModel):
    faithfulness: float
    is_grounded: bool

class HealthResponse(BaseModel):
    status: str
    weaviate: str
    pipeline: str
    version: str
