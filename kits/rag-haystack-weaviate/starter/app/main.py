import os
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import (
    QueryRequest, QueryResponse,
    IngestRequest, IngestResponse,
    EvalRequest, EvalResponse,
    HealthResponse
)
from app.weaviate_service import weaviate_service
from app.pipeline import rag_pipeline, faithfulness_evaluator

app = FastAPI(
    title="Haystack Pipelines + Weaviate RAG API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None
)

# CORS Policy - Strict whitelist from environment, zero wildcard
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
        weaviate="connected",
        pipeline="ready",
        version="1.0.0"
    )

@app.post("/api/v1/documents/index", response_model=IngestResponse, status_code=status.HTTP_201_CREATED, tags=["RAG"])
async def index_documents(req: IngestRequest):
    docs = [d.model_dump() for d in req.documents]
    indexed = weaviate_service.index_documents(docs)
    return IngestResponse(
        status="success",
        count=indexed
    )

@app.post("/api/v1/rag/query", response_model=QueryResponse, tags=["RAG"])
async def query_pipeline(req: QueryRequest):
    try:
        result = rag_pipeline.run(
            question=req.question,
            tenant_id=req.tenant_id,
            alpha=req.alpha
        )
        return QueryResponse(
            question=req.question,
            answer=result["answer"],
            retrieved_chunks=result["documents"],
            faithfulness_score=result["faithfulness"],
            pipeline_latency_ms=result["latency_ms"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Haystack pipeline error: {str(e)}"
        )

@app.post("/api/v1/rag/eval", response_model=EvalResponse, tags=["Evaluations"])
async def evaluate_output(req: EvalRequest):
    docs = [{"content": c} for c in req.context]
    score = faithfulness_evaluator.evaluate(answer=req.answer, documents=docs)
    return EvalResponse(
        faithfulness=score,
        is_grounded=(score >= 0.85)
    )
