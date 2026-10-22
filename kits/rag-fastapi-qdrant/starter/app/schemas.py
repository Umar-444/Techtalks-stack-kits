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
    chunks_created: int
    collection: str

class SearchQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="Natural language search query")
    top_k: int = Field(default=3, ge=1, le=20, description="Number of results to retrieve")
    score_threshold: float = Field(default=0.50, ge=0.0, le=1.0, description="Minimum cosine similarity score")
    filter: Optional[dict[str, Any]] = Field(default=None, description="Exact match payload filters e.g. tenant_id")

class SearchResultSource(BaseModel):
    document_id: str
    chunk_index: int
    score: float
    text: str
    metadata: dict[str, Any]

class SearchQueryResponse(BaseModel):
    query: str
    results_count: int
    sources: list[SearchResultSource]
    assembled_context: str

class HealthResponse(BaseModel):
    status: str
    app: str
    qdrant_connected: bool
    version: str = "1.0.0"
