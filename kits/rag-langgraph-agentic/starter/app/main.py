import os
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import (
    QueryRequest, QueryResponse,
    IngestRequest, IngestResponse,
    EvalScoreRequest, EvalScoreResponse,
    HealthResponse
)
from app.vector_store import vector_service
from app.graph import run_agentic_rag
from app.evals import ragas_evaluator

app = FastAPI(
    title="Agentic LangGraph + Qdrant + Ragas RAG API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None
)

# CORS Policy - Strict origin configuration, zero wildcard
raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8080")
allowed_origins = [o.strip() for o in raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "Accept"]
)

@app.get("/health", response_model=HealthResponse, tags=["Observability"])
async def health_check():
    return HealthResponse(
        status="healthy",
        qdrant="connected",
        graph="ready",
        version="1.0.0"
    )

@app.post("/api/v1/documents/index", response_model=IngestResponse, status_code=status.HTTP_201_CREATED, tags=["RAG"])
async def index_documents(req: IngestRequest):
    docs = [d.model_dump() for d in req.documents]
    indexed = vector_service.index_documents(docs)
    return IngestResponse(
        status="success",
        indexed_count=indexed
    )

@app.post("/api/v1/rag/query", response_model=QueryResponse, tags=["RAG"])
async def query_agentic_rag(req: QueryRequest):
    try:
        final_state = run_agentic_rag(
            question=req.question,
            tenant_id=req.tenant_id,
            max_iterations=req.max_iterations
        )
        return QueryResponse(
            question=req.question,
            answer=final_state.get("generation", ""),
            retrieved_documents=final_state.get("documents", []),
            iterations_used=final_state.get("iterations", 0),
            groundedness_score=final_state.get("groundedness_score", 0.0),
            status=final_state.get("status", "completed")
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agentic graph execution error: {str(e)}"
        )

@app.post("/api/v1/rag/eval", response_model=EvalScoreResponse, tags=["Evaluations"])
async def evaluate_output(req: EvalScoreRequest):
    docs = [{"content": c} for c in req.context]
    groundedness = ragas_evaluator.evaluate_groundedness(
        question=req.question,
        documents=docs,
        answer=req.answer
    )
    precision = ragas_evaluator.evaluate_context_precision(
        question=req.question,
        documents=docs
    )
    is_hallucination = groundedness < 0.85
    return EvalScoreResponse(
        groundedness=groundedness,
        context_precision=precision,
        is_hallucination=is_hallucination,
        status="evaluated"
    )
