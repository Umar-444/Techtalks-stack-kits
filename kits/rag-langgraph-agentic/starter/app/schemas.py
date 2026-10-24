from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

TENANT_PATTERN = r"^[A-Za-z0-9_.-]{1,64}$"

class DocumentPayload(BaseModel):
    id: str = Field(..., min_length=1, max_length=128, description="Unique document ID")
    content: str = Field(..., min_length=1, max_length=20000, description="Text chunk payload")
    tenant_id: str = Field(..., pattern=TENANT_PATTERN, description="Multi-tenant namespace (required)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary JSON metadata")

class IngestRequest(BaseModel):
    documents: List[DocumentPayload] = Field(..., min_length=1, max_length=100)

class IngestResponse(BaseModel):
    status: str
    indexed_count: int

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=1000, description="User search query")
    tenant_id: str = Field(..., pattern=TENANT_PATTERN, description="Target tenant isolation ID (required)")
    max_iterations: int = Field(default=3, ge=1, le=5, description="Cyclic recursion limit")

class QueryResponse(BaseModel):
    question: str
    answer: str
    retrieved_documents: List[Dict[str, Any]]
    iterations_used: int
    groundedness_score: float
    status: str

class EvalScoreRequest(BaseModel):
    question: str = Field(..., max_length=1000)
    context: List[str] = Field(..., max_length=50)
    answer: str = Field(..., max_length=20000)

class EvalScoreResponse(BaseModel):
    groundedness: float
    context_precision: float
    is_hallucination: bool
    status: str

class HealthResponse(BaseModel):
    status: str
    qdrant: str
    graph: str
    version: str
