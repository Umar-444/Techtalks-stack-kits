from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class DocumentPayload(BaseModel):
    id: str = Field(..., description="Unique document ID")
    content: str = Field(..., min_length=1, description="Text chunk payload")
    tenant_id: str = Field(default="default-tenant", description="Multi-tenant namespace")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary JSON metadata")

class IngestRequest(BaseModel):
    documents: List[DocumentPayload] = Field(..., min_length=1)

class IngestResponse(BaseModel):
    status: str
    indexed_count: int

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=1000, description="User search query")
    tenant_id: str = Field(default="default-tenant", description="Target tenant isolation ID")
    max_iterations: int = Field(default=3, ge=1, le=5, description="Cyclic recursion limit")

class QueryResponse(BaseModel):
    question: str
    answer: str
    retrieved_documents: List[Dict[str, Any]]
    iterations_used: int
    groundedness_score: float
    status: str

class EvalScoreRequest(BaseModel):
    question: str
    context: List[str]
    answer: str

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
