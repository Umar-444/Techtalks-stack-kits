# GitHub Copilot Instructions for LlamaIndex + PostgreSQL pgvector + FastAPI
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## 01 Framework Architecture And Standards
﻿---
id: 01-framework-architecture-and-standards
title: FastAPI Architecture, LlamaIndex Settings & Async Lifespan
globs: "*"
alwaysApply: true
---
# Rule 1: FastAPI Architecture, LlamaIndex Settings & Async Lifespan

## Context & Principles
- Pair FastAPI 0.115+ with LlamaIndex 0.11+ using global `Settings` configuration rather than legacy `ServiceContext`.
- Manage persistent database connection pools and embedding models via FastAPI's `@asynccontextmanager` lifespan handler.
- Expose typed asynchronous REST endpoints backed by Pydantic v2 schemas and structured exception handlers.

## Standards
1. **Global LlamaIndex Configuration**:
   ```python
   from llama_index.core import Settings
   from llama_index.embeddings.fastembed import FastEmbedEmbedding

   Settings.embed_model = FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5")
   Settings.chunk_size = 512
   Settings.chunk_overlap = 64
   ```
2. **Lifespan Management**:
   ```python
   @asynccontextmanager
   async def lifespan(app: FastAPI):
       await vector_service.initialize()
       yield
       await vector_service.close()
   ```
3. **Pydantic Validation**: All request and response payloads must subclass `pydantic.BaseModel` with explicit constraints (`Field(min_length=1, max_length=10000)`).
4. **Health Probe**: Provide a non-blocking `/healthz` endpoint verifying application health and PostgreSQL pgvector connectivity.


## 02 Pgvector Schema And Hnsw Indexing
﻿---
id: 02-pgvector-schema-and-hnsw-indexing
title: PostgreSQL 16+ pgvector Schema & HNSW Indexing
globs: "*"
alwaysApply: true
---
# Rule 2: PostgreSQL 16+ pgvector Schema & HNSW Indexing

## Context & Principles
- Store dense high-dimensional vectors in PostgreSQL using the `pgvector` extension and native `vector` data types.
- Build Hierarchical Navigable Small World (HNSW) indexes (`vector_cosine_ops`) rather than legacy IVFFlat indexes to achieve high recall without requiring index rebuilds.
- Configure connection pooling via SQLAlchemy / asyncpg / psycopg3 to reuse connections across concurrent API requests.

## Standards
1. **Extension & Index Provisioning**:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   
   CREATE TABLE IF NOT EXISTS data_rag_embeddings (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       text TEXT NOT NULL,
       metadata_ JSONB DEFAULT '{}',
       embedding vector(384)
   );

   CREATE INDEX IF NOT EXISTS idx_hnsw_embedding
   ON data_rag_embeddings USING hnsw (embedding vector_cosine_ops)
   WITH (m = 16, ef_construction = 100);
   ```
2. **Metadata GIN Indexing**: Create GIN indexes on the `metadata_` JSONB column (`CREATE INDEX idx_metadata ON data_rag_embeddings USING gin (metadata_);`) to accelerate hybrid metadata filters.
3. **Exact Dimensions**: Vector column dimensions must strictly match the embedding model output dimensionality (`384` for BGE-small).
4. **Maintenance**: Regularly schedule `VACUUM ANALYZE data_rag_embeddings;` to keep vector page layout and index statistics optimal.


## 03 Ingestion Chunking And Metadata
﻿---
id: 03-ingestion-chunking-and-metadata
title: Document Ingestion, Semantic Chunking & Metadata Enrichment
globs: "*"
alwaysApply: true
---
# Rule 3: Document Ingestion, Semantic Chunking & Metadata Enrichment

## Context & Principles
- Ingestion pipelines must transform unstructured documents into discrete, high-signal nodes with preserved provenance.
- Use LlamaIndex `SentenceSplitter` with a target chunk size of 512 tokens and 64-token overlap to prevent truncation of conceptual units.
- Enrich every document node with structured metadata keys enabling granular access control and tenant isolation.

## Standards
1. **Node Parsing**:
   ```python
   from llama_index.core.node_parser import SentenceSplitter
   from llama_index.core.schema import Document

   parser = SentenceSplitter(chunk_size=512, chunk_overlap=64)
   nodes = parser.get_nodes_from_documents([
       Document(
           text=raw_text,
           metadata={"document_id": doc_id, "tenant_id": tenant_id, "category": category}
       )
   ])
   ```
2. **Metadata Hygiene**: Strip internal file system paths or PII before persisting metadata to the database.
3. **Idempotent Ingestion**: Use deterministic node IDs (`doc_id + "_" + str(chunk_idx)`) to ensure re-ingesting a document updates existing records rather than producing duplicates.
4. **Empty Node Rejection**: Filter out whitespace-only strings or empty chunks prior to embedding calculation.


## 04 Retrieval Query Engine And Reranking
﻿---
id: 04-retrieval-query-engine-and-reranking
title: Vector Retrieval, Metadata Filtering & Response Synthesis
globs: "*"
alwaysApply: true
---
# Rule 4: Vector Retrieval, Metadata Filtering & Response Synthesis

## Context & Principles
- Retrieve semantically relevant context nodes using PostgreSQL vector distance calculations coupled with strict metadata filtering.
- Prevent cross-tenant information leakage by mandating tenant filter predicates on every query engine execution.
- Synthesize grounded, factual answers using structured context delimiters and explicit source citations.

## Standards
1. **Metadata Filtered Retriever**:
   ```python
   from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter

   filters = MetadataFilters(
       filters=[ExactMatchFilter(key="tenant_id", value=tenant_id)]
   )
   retriever = index.as_retriever(
       similarity_top_k=5,
       filters=filters
   )
   ```
2. **Citation Assembly**:
   Format retrieved nodes with score badges and document IDs before returning responses:
   ```markdown
   [Source 1] (Score: 0.82, Doc: policy.pdf):
   "Employees may expense up to $1,000 annually for ergonomic furniture..."
   ```
3. **Score Thresholding**: Filter out nodes with similarity scores below `0.60` to eliminate irrelevant context from being passed to LLM generation prompts.
4. **Context Budgeting**: Cap total retrieved context at 3,000 tokens to guarantee room for generation without truncation.


## 05 Evaluation Security And Testing
﻿---
id: 05-evaluation-security-and-testing
title: Faithfulness Evaluations, Security Guardrails & In-Memory Testing
globs: "*"
alwaysApply: true
---
# Rule 5: Faithfulness Evaluations, Security Guardrails & In-Memory Testing

## Context & Principles
- Continuous evaluation prevents retrieval drift, hallucination, and prompt injection attacks in RAG pipelines.
- Verify generated responses using LlamaIndex `FaithfulnessEvaluator` and `RelevancyEvaluator` against reference ground truth pairs.
- Implement automated unit tests using an in-memory mock vector store to ensure test suites execute with zero external database dependencies.

## Standards
1. **Faithfulness & Relevancy Evaluation**:
   ```python
   from llama_index.core.evaluation import FaithfulnessEvaluator, RelevancyEvaluator

   faithfulness = FaithfulnessEvaluator()
   relevancy = RelevancyEvaluator()

   f_eval = faithfulness.evaluate_response(response=response)
   r_eval = relevancy.evaluate_response(query=query_str, response=response)
   assert f_eval.passing and r_eval.passing
   ```
2. **Prompt Injection Mitigation**: Isolate retrieved context from system instructions using explicit XML/markdown boundaries (`<context>...</context>`).
3. **Zero Plaintext Secrets**: Never hardcode database passwords or LLM API keys. Validate required secrets during startup using Pydantic `BaseSettings`.
4. **Fast Unit Tests**: Test retrieval, ingestion, and evaluation pipelines using Pytest with in-memory fixtures.


