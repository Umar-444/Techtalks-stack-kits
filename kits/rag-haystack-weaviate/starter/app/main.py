import os
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import (
    QueryRequest, QueryResponse,
    IngestRequest, IngestResponse,
    EvalRequest, EvalResponse,
    HealthResponse
)
from app.weaviate_service import weaviate_service
from app.pipeline import rag_pipeline, faithfulness_evaluator, FAITHFULNESS_THRESHOLD

app = FastAPI(
    title="Haystack Pipelines + Weaviate RAG API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None
)

# CORS Policy - Strict whitelist from environment, zero wildcard
raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8080")
allowed_origins = [o.strip() for o in raw_origins.split(",") if o.strip() and o.strip() != "*"]


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    # Never echo exception text, hostnames or stack frames to the caller.
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "Accept"]
)

@app.get("/health", response_model=HealthResponse, tags=["Observability"])
async def health_check():
    weaviate_ok = weaviate_service.is_healthy()
    pipeline_ok = bool(getattr(rag_pipeline, "is_ready", False))
    return HealthResponse(
        status="healthy" if (weaviate_ok and pipeline_ok) else "degraded",
        weaviate="connected" if weaviate_ok else "unreachable",
        pipeline="ready" if pipeline_ok else "not_ready",
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

@app.post("/api/v1/rag/eval", response_model=EvalResponse, tags=["Evaluations"])
async def evaluate_output(req: EvalRequest):
    docs = [{"content": c} for c in req.context]
    score = faithfulness_evaluator.evaluate(answer=req.answer, documents=docs)
    return EvalResponse(
        faithfulness=score,
        is_grounded=(score >= FAITHFULNESS_THRESHOLD)
    )
