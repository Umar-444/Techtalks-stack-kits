from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class DataClassification(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"

class DocumentChunk(BaseModel):
    model_config = ConfigDict(extra="forbid")
    chunk_id: str
    text: str
    chunk_index: int
    metadata: Dict[str, Any] = Field(default_factory=dict)

class IngestRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    document_id: str = Field(..., min_length=1, max_length=128)
    title: str = Field(..., min_length=1, max_length=256)
    tenant_id: str = Field(..., min_length=1, max_length=64)
    classification: DataClassification = DataClassification.INTERNAL
    text: str = Field(..., min_length=1, max_length=10_000_000)
    chunk_size: int = Field(default=512, ge=64, le=4096)
    chunk_overlap: int = Field(default=64, ge=0, le=512)

class IngestResponse(BaseModel):
    document_id: str
    chunks_created: int
    collection: str
    status: str = "ingested"
    airgap_safe: bool = True

class SourceNode(BaseModel):
    document_id: str
    chunk_index: int
    classification: str
    similarity_score: float
    text_snippet: str

class QueryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    query: str = Field(..., min_length=1, max_length=1000)
    tenant_id: str = Field(..., min_length=1, max_length=64)
    user_classification: DataClassification = DataClassification.CONFIDENTIAL
    top_k: int = Field(default=3, ge=1, le=20)

class QueryResponse(BaseModel):
    query: str
    answer: str
    sources: List[SourceNode]
    airgap_safe: bool = True
    privacy_verified: bool = True

class EvaluationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    query: str = Field(..., min_length=1)
    ground_truth_context: str = Field(..., min_length=1)
    generated_answer: str = Field(..., min_length=1)

class EvaluationResponse(BaseModel):
    groundedness_score: float = Field(..., ge=0.0, le=1.0)
    context_relevance_score: float = Field(..., ge=0.0, le=1.0)
    airgap_compliant: bool = True
    is_hallucination_detected: bool = False

class HealthResponse(BaseModel):
    status: str = "healthy"
    airgap_safe: bool = True
    cloud_egress_blocked: bool = True
    vector_store: str = "chromadb"
    llm_engine: str = "ollama"
    model: str = "llama3.2"
