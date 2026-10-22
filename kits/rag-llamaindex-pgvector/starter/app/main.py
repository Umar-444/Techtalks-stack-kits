import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from .schemas import (
    DocumentIngestRequest,
    DocumentIngestResponse,
    SearchQueryRequest,
    SearchQueryResponse,
    SearchResultSource,
    EvaluationRequest,
    EvaluationResponse,
    HealthResponse
)
from .services.vector_service import vector_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    vector_service.initialize()
    yield

app = FastAPI(
    title="LlamaIndex + PostgreSQL pgvector Service",
    description="Production-grade RAG retrieval and evaluation service using LlamaIndex and PostgreSQL pgvector.",
    version="1.0.0",
    lifespan=lifespan
)

allowed_origins = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/healthz", response_model=HealthResponse, tags=["Health"])
def healthz():
    connected = vector_service.is_connected()
    return HealthResponse(
        status="ok" if connected else "degraded",
        app=os.getenv("APP_NAME", "rag-llamaindex-pgvector"),
        database_connected=connected,
        version="1.0.0"
    )

@app.post("/api/v1/documents/ingest", response_model=DocumentIngestResponse, status_code=status.HTTP_201_CREATED, tags=["Ingestion"])
def ingest_document(payload: DocumentIngestRequest):
    nodes_count = vector_service.ingest_document(
        document_id=payload.document_id,
        title=payload.title,
        text=payload.text,
        metadata=payload.metadata
    )
    if nodes_count == 0:
        raise HTTPException(status_code=400, detail="Document could not be chunked into valid nodes.")

    return DocumentIngestResponse(
        document_id=payload.document_id,
        status="indexed",
        nodes_created=nodes_count,
        table_name=vector_service.table_name
    )

@app.post("/api/v1/query", response_model=SearchQueryResponse, tags=["Retrieval"])
def search_query(payload: SearchQueryRequest):
    hits = vector_service.query_documents(
        query=payload.query,
        top_k=payload.similarity_top_k,
        score_threshold=payload.score_threshold,
        filters=payload.filter
    )

    sources = [
        SearchResultSource(
            node_id=h["node_id"],
            document_id=h["document_id"],
            score=h["score"],
            text=h["text"],
            metadata=h["metadata"]
        )
        for h in hits
    ]

    context_snippets = [f"[Source {idx}] (Doc: {s.document_id}, Score: {s.score}): {s.text}" for idx, s in enumerate(sources, 1)]
    response_text = "Based on retrieved documentation: " + " ".join([s.text for s in sources]) if sources else "No relevant context found in database."

    return SearchQueryResponse(
        query=payload.query,
        results_count=len(sources),
        sources=sources,
        response=response_text
    )

@app.post("/api/v1/evaluate", response_model=EvaluationResponse, tags=["Evaluation"])
def evaluate_rag(payload: EvaluationRequest):
    result = vector_service.evaluate(
        query=payload.query,
        response=payload.response,
        contexts=payload.contexts
    )
    return EvaluationResponse(
        faithfulness_passing=result["faithfulness_passing"],
        relevancy_passing=result["relevancy_passing"],
        score=result["score"],
        feedback=result["feedback"]
    )
