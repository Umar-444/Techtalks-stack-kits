import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.schemas import (
    IngestRequest,
    IngestResponse,
    QueryRequest,
    QueryResponse,
    EvaluationRequest,
    EvaluationResponse,
    HealthResponse
)
from app.services.rag_service import rag_service, settings, check_egress, EgressBlocked

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lifecycle startup
    yield
    # Lifecycle shutdown cleanups

app = FastAPI(
    title="Local Private Airgapped RAG",
    description="100% offline, zero cloud egress private enterprise RAG with Ollama & ChromaDB",
    version="1.0.0",
    lifespan=lifespan
)

# Enforce explicit origins list from environment configuration (blocks wildcard CORS)
def parse_origins(raw: str) -> list:
    """Explicit origin whitelist; a wildcard entry is never honoured."""
    return [o.strip() for o in raw.split(",") if o.strip() and o.strip() != "*"]


allowed_origins_list = parse_origins(settings.allowed_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins_list or ["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal processing failure in private RAG pipeline.",
            "code": "RAG_PROCESSING_ERROR",
            "airgap_safe": True
        }
    )

@app.get("/healthz", response_model=HealthResponse)
async def health_check():
    try:
        check_egress(settings.ollama_base_url, True)
        endpoint_local = True
    except EgressBlocked:
        endpoint_local = False
    # Airgap-safe only when egress is restricted AND the LLM endpoint is local.
    airgap_safe = settings.restrict_outbound_egress and endpoint_local
    return HealthResponse(
        status="healthy" if airgap_safe else "degraded",
        airgap_safe=airgap_safe,
        cloud_egress_blocked=settings.restrict_outbound_egress,
        vector_store="chromadb",
        llm_engine="ollama",
        model=settings.ollama_model
    )

@app.post("/api/v1/documents/ingest", response_model=IngestResponse, status_code=status.HTTP_201_CREATED)
async def ingest_document(req: IngestRequest):
    # Failures fall through to the global handler: no exception text reaches the caller.
    return await rag_service.ingest_document(req)

@app.post("/api/v1/query", response_model=QueryResponse)
async def query_knowledge_base(req: QueryRequest):
    return await rag_service.query_knowledge_base(req)

@app.post("/api/v1/evaluate", response_model=EvaluationResponse)
async def evaluate_rag_response(req: EvaluationRequest):
    return rag_service.evaluate_offline(req)
