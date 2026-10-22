# RAG FastAPI + Qdrant + FastEmbed — Agent Operating Rules (AGENTS.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Table of Contents
- [01 Framework Architecture And Standards](#01-framework-architecture-and-standards)
- [02 Qdrant Vector Storage And Indexing](#02-qdrant-vector-storage-and-indexing)
- [03 Embeddings And Chunking Pipeline](#03-embeddings-and-chunking-pipeline)
- [04 Rag Retrieval Reranking And Context](#04-rag-retrieval-reranking-and-context)
- [05 Security Guardrails And Testing](#05-security-guardrails-and-testing)

---

<a id="01-framework-architecture-and-standards"></a>
## 01 Framework Architecture And Standards

﻿# Rule 1: FastAPI Architecture, Async Lifespan & Dependency Injection

## Context & Principles
- Build asynchronous, non-blocking APIs utilizing modern Python 3.12+ type annotations and Pydantic v2 schemas.
- Manage long-lived stateful clients (such as QdrantClient and embedding models) through FastAPI's `@asynccontextmanager` lifespan handler rather than deprecated startup/shutdown events.
- Utilize FastAPI dependency injection (`Depends`) to provide request-scoped access to vector search services, embedding pipelines, and authorization contexts.

## Standards
1. **Lifespan Management**:
   ```python
   @asynccontextmanager
   async def lifespan(app: FastAPI):
       # Initialize Qdrant collection and warm up embedding pipeline
       await qdrant_service.initialize()
       yield
       # Clean connection pools on shutdown
       await qdrant_service.close()
   ```
2. **Schema Invariants**: All request and response payloads must subclass `pydantic.BaseModel` with strict type annotations, field descriptions, and input constraints (`Field(min_length=1, max_length=10000)`).
3. **Structured Error Handling**: Raise `fastapi.HTTPException` with RFC 7807 compliant JSON details rather than unhandled raw runtime exceptions.
4. **Health Probe**: Expose a non-blocking `/healthz` probe validating application state and active connectivity to the Qdrant cluster.


---

<a id="02-qdrant-vector-storage-and-indexing"></a>
## 02 Qdrant Vector Storage And Indexing

﻿# Rule 2: Qdrant Vector Storage, Collections & HNSW Indexing

## Context & Principles
- Qdrant manages dense high-dimensional vectors with customizable distance metrics and Hierarchical Navigable Small World (HNSW) graph indexing.
- Use Cosine distance (`models.Distance.COSINE`) for normalized embeddings (such as BGE or text-embedding-3-small).
- Optimize HNSW index parameters (`m=16`, `ef_construct=100`) to balance memory consumption, build times, and retrieval precision.

## Standards
1. **Idempotent Collection Provisioning**:
   ```python
   if not client.collection_exists(collection_name):
       client.create_collection(
           collection_name=collection_name,
           vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
           hnsw_config=models.HnswConfigDiff(m=16, ef_construct=100)
       )
   ```
2. **Payload Indexing**: Always define payload schema indexes for fields used in filter queries (e.g. `tenant_id`, `category`, `document_id`) to ensure sub-millisecond filtering before graph traversal.
3. **Point IDs**: Use valid UUIDv4 strings or integer IDs. Generate deterministic UUIDv5 hashes from `(document_id, chunk_index)` to support idempotent document re-ingestion.
4. **Batch Upserts**: Group vector additions into batches of 100-256 points to minimize network I/O round trips and optimize disk flushing.


---

<a id="03-embeddings-and-chunking-pipeline"></a>
## 03 Embeddings And Chunking Pipeline

﻿# Rule 3: Text Chunking, Token Budgets & FastEmbed Generation

## Context & Principles
- RAG accuracy is fundamentally bounded by the quality and granularity of document chunking.
- Implement recursive character or markdown splitting with a target chunk size of 512 tokens and an overlap of 64 tokens (12.5%) to preserve cross-boundary semantics.
- Prefer local ONNX-based dense embeddings (e.g. `BAAI/bge-small-en-v1.5` via FastEmbed) for zero-latency, zero-cost, and fully offline vectorization.

## Standards
1. **Sliding Window Chunking**:
   ```python
   def chunk_text(text: str, chunk_size: int = 512, overlap: int = 64) -> list[str]:
       chunks = []
       start = 0
       while start < len(text):
           end = min(start + chunk_size, len(text))
           chunks.append(text[start:end])
           if end == len(text):
               break
           start += chunk_size - overlap
       return chunks
   ```
2. **Deterministic Dimensions**: Strictly enforce matching vector dimensionality between the embedding model output and the Qdrant collection configuration (`size=384` for BGE-small).
3. **Payload Metadata Enrichment**: Attach essential provenance metadata to every chunk payload: `{"document_id": doc_id, "chunk_index": idx, "text": chunk, "char_start": start, "char_end": end, "created_at": iso_timestamp}`.
4. **Zero Empty Chunks**: Filter out whitespace-only or empty strings prior to embedding generation to avoid degenerate null vectors.


---

<a id="04-rag-retrieval-reranking-and-context"></a>
## 04 Rag Retrieval Reranking And Context

﻿# Rule 4: Vector Retrieval, Payload Filtering & Context Assembly

## Context & Principles
- Retrieve relevant context with low latency using Qdrant vector search coupled with strict payload filtering for multi-tenant isolation.
- Enforce score thresholding (e.g. `score_threshold=0.65`) to eliminate hallucinated context from low-relevance matches.
- Format retrieved chunks into clear, structured context blocks with verifiable source citations.

## Standards
1. **Multi-Tenant Filter Invariants**:
   ```python
   query_filter = models.Filter(
       must=[
           models.FieldCondition(key="tenant_id", match=models.MatchValue(value=tenant_id)),
       ]
   )
   ```
   *Never execute unfiltered vector searches across multi-tenant collections.*
2. **Context Assembly with Citations**:
   Assemble context snippets into numbered citation blocks:
   ```markdown
   [Context 1] (doc_id: handbook.md, score: 0.89):
   "Refund policies allow full refunds within 30 days of purchase..."
   ```
3. **Budgeted Context Windows**: Limit total retrieved tokens to a maximum of 3,000 tokens to leave sufficient headroom for LLM response generation and avoid context truncation.
4. **Fallback on Empty Results**: When no documents exceed the score threshold, gracefully inform the caller rather than sending irrelevant noise to the generation model.


---

<a id="05-security-guardrails-and-testing"></a>
## 05 Security Guardrails And Testing

﻿# Rule 5: Security Guardrails, Prompt Injection Defense & In-Memory Testing

## Context & Principles
- RAG applications are susceptible to indirect prompt injection through ingested untrusted documents.
- Isolate system instructions from retrieved context using strict delimiters (`<context>...</context>`).
- Enforce automated unit and integration tests using Qdrant's embedded in-memory mode (`QdrantClient(":memory:")`), eliminating the need for an external database during local test execution.

## Standards
1. **Delimited Context Formatting**:
   ```python
   prompt = f"""You are a helpful assistant. Answer the user query using ONLY the provided context. If the answer cannot be found in the context, say 'I cannot find that in the documentation.'
   
   <context>
   {assembled_context}
   </context>
   
   User Question: {user_query}"""
   ```
2. **Untrusted Payload Sanitization**: Strip dangerous control characters and markdown injection tokens from user documents prior to embedding generation.
3. **In-Memory Testing Harness**:
   ```python
   @pytest.fixture
   def in_memory_client():
       return QdrantClient(":memory:")
   ```
4. **Secret Scanning**: Never hardcode API keys or vector database passwords. Validate that environment variables are non-empty during startup using Pydantic `BaseSettings`.


---

