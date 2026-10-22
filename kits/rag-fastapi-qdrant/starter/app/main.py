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
    HealthResponse
)
from .services.embedding_service import embedding_service
from .services.qdrant_service import qdrant_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Qdrant collection on startup
    qdrant_service.initialize()
    yield

app = FastAPI(
    title="RAG FastAPI + Qdrant Vector Service",
    description="Production-grade vector search and RAG retrieval service powered by FastAPI and Qdrant.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz", response_model=HealthResponse, tags=["Health"])
def healthz():
    connected = qdrant_service.is_connected()
    return HealthResponse(
        status="ok" if connected else "degraded",
        app=os.getenv("APP_NAME", "rag-fastapi-qdrant"),
        qdrant_connected=connected,
        version="1.0.0"
    )

@app.post("/api/v1/documents/ingest", response_model=DocumentIngestResponse, status_code=status.HTTP_201_CREATED, tags=["Ingestion"])
def ingest_document(payload: DocumentIngestRequest):
    chunks = embedding_service.chunk_text(
        text=payload.text,
        chunk_size=int(os.getenv("MAX_CHUNK_SIZE", "500")),
        chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "50"))
    )
    if not chunks:
        raise HTTPException(status_code=400, detail="Document text could not be chunked into valid tokens.")

    chunk_texts = [c["text"] for c in chunks]
    vectors = embedding_service.embed_texts(chunk_texts)

    metadata = dict(payload.metadata)
    if payload.title:
        metadata["title"] = payload.title

    qdrant_service.upsert_chunks(
        document_id=payload.document_id,
        chunks=chunks,
        vectors=vectors,
        metadata=metadata
    )

    return DocumentIngestResponse(
        document_id=payload.document_id,
        status="indexed",
        chunks_created=len(chunks),
        collection=qdrant_service.collection_name
    )

@app.post("/api/v1/query", response_model=SearchQueryResponse, tags=["Retrieval"])
def search_query(payload: SearchQueryRequest):
    query_vector = embedding_service.embed_query(payload.query)

    hits = qdrant_service.search(
        query_vector=query_vector,
        top_k=payload.top_k,
        score_threshold=payload.score_threshold,
        filters=payload.filter
    )

    sources = [
        SearchResultSource(
            document_id=h["document_id"],
            chunk_index=h["chunk_index"],
            score=round(h["score"], 4),
            text=h["text"],
            metadata=h["metadata"]
        )
        for h in hits
    ]

    # Assemble structured context block with source citations
    context_lines = []
    for idx, s in enumerate(sources, 1):
        context_lines.append(f"[Source {idx}] (Score: {s.score}, Doc: {s.document_id}):\n{s.text}")

    assembled_context = "\n\n".join(context_lines) if context_lines else "No relevant context found."

    return SearchQueryResponse(
        query=payload.query,
        results_count=len(sources),
        sources=sources,
        assembled_context=assembled_context
    )
