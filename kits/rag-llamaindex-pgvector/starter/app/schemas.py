from typing import Any, Optional
from pydantic import BaseModel, Field

class DocumentIngestRequest(BaseModel):
    document_id: str = Field(..., min_length=1, max_length=128, description="Unique identifier for the document")
    title: Optional[str] = Field(None, max_length=256, description="Human readable title")
    text: str = Field(..., min_length=1, max_length=100000, description="Full text content of document")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Metadata tags e.g. tenant_id, category")

class DocumentIngestResponse(BaseModel):
    document_id: str
    status: str = "indexed"
    nodes_created: int
    table_name: str

class SearchQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="Natural language search query")
    similarity_top_k: int = Field(default=3, ge=1, le=20, description="Number of results to retrieve")
    score_threshold: float = Field(default=0.60, ge=0.0, le=1.0, description="Minimum cosine similarity score")
    filter: Optional[dict[str, Any]] = Field(default=None, description="Exact match payload filters e.g. tenant_id")

class SearchResultSource(BaseModel):
    node_id: str
    document_id: str
    score: float
    text: str
    metadata: dict[str, Any]

class SearchQueryResponse(BaseModel):
    query: str
    results_count: int
    sources: list[SearchResultSource]
    response: str

class EvaluationRequest(BaseModel):
    query: str = Field(..., max_length=1000)
    response: str = Field(..., max_length=20000)
    contexts: list[str] = Field(..., max_length=50)

class EvaluationResponse(BaseModel):
    faithfulness_passing: bool
    relevancy_passing: bool
    score: float
    feedback: str

class HealthResponse(BaseModel):
    status: str
    app: str
    database_connected: bool
    version: str = "1.0.0"
