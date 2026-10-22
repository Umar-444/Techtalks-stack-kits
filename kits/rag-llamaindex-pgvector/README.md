# LlamaIndex + PostgreSQL pgvector + FastAPI Stack Kit

[![Stack Status: Ready to Ship](https://img.shields.io/badge/status-Ready%20to%20Ship-emerald?style=flat-square)](kit.yaml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue?style=flat-square)](https://www.python.org/)
[![FastAPI 0.115](https://img.shields.io/badge/fastapi-0.115-009688?style=flat-square)](https://fastapi.tiangolo.com/)
[![LlamaIndex 0.11](https://img.shields.io/badge/llamaindex-0.11-purple?style=flat-square)](https://www.llamaindex.ai/)
[![PostgreSQL 16](https://img.shields.io/badge/postgresql-16-336791?style=flat-square)](https://www.postgresql.org/)
[![pgvector](https://img.shields.io/badge/pgvector-0.7.0-blue?style=flat-square)](https://github.com/pgvector/pgvector)

Production-grade Retrieval Augmented Generation (RAG) and evaluation service combining LlamaIndex 0.11+ ingestion pipelines, PostgreSQL 16+ pgvector HNSW indexing, FastAPI REST endpoints, and automated faithfulness & relevancy evaluations.

---

## Architecture Overview

```
                   +-----------------------------------+
                   |         Client Application        |
                   +-----------------+-----------------+
                                     |
                          JSON REST API Requests
                                     v
                   +-----------------+-----------------+
                   |     FastAPI Service Layer         |
                   |  - Lifespan & Connection Pools    |
                   |  - SentenceSplitter Parsing       |
                   |  - Faithfulness / Relevancy Evals |
                   +-----------------+-----------------+
                                     |
                           LlamaIndex PGVectorStore
                                     v
                   +-----------------+-----------------+
                   |       PostgreSQL 16 Database      |
                   |  - pgvector Extension (HNSW)      |
                   |  - Cosine Distance (<=>)          |
                   |  - GIN Index on JSONB Metadata    |
                   |  - Multi-Tenant SQL Filters       |
                   +-----------------------------------+
```

---

## Key Features

1. **Transactional Vector Store**: Embeddings reside directly in PostgreSQL, enabling native transactional consistency, foreign key relationships, and ACID compliance.
2. **HNSW Vector Indexing**: Configured with `vector_cosine_ops` (`m=16`, `ef_construction=100`) delivering sub-15ms nearest-neighbor retrieval without clustering rebuild delays.
3. **Automated RAG Evaluations**: Built-in support for `FaithfulnessEvaluator` and `RelevancyEvaluator` measuring groundedness and preventing hallucinations.
4. **Metadata GIN Indexing**: Enforces strict multi-tenant data isolation by indexing JSONB metadata keys for single-digit millisecond pre-filtering.
5. **Sentence-Aware Chunking**: LlamaIndex `SentenceSplitter` partitions unstructured text respecting grammatical sentence boundaries.
6. **Zero-Dependency Testing**: Includes an in-memory test runner fixture allowing test suites to execute offline in milliseconds without Docker.

---

## Quickstart with Docker Compose

Spin up the local multi-container environment:

```bash
# 1. Clone the repository
git clone https://github.com/Umar-444/Techtalks-stack-kits.git
cd Techtalks-stack-kits/kits/rag-llamaindex-pgvector/starter

# 2. Start services (FastAPI web + PostgreSQL 16 pgvector)
docker compose up --build -d
```

Access services:
- **API Documentation (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check Probe**: [http://localhost:8000/healthz](http://localhost:8000/healthz)

---

## 7-Part Native Installation Guide

### 1. Prerequisites
- Python 3.12+
- PostgreSQL 16+ with the `pgvector` extension installed

### 2. Environment Setup
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Environment Variables
```bash
cp .env.example .env
```
Default configuration connects to `localhost:5432` with database `rag_db` and table `data_rag_embeddings`.

### 4. Enable pgvector Extension in PostgreSQL
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### 5. Launch FastAPI Service
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 6. Ingest Sample Document
```bash
curl -X POST http://localhost:8000/api/v1/documents/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "sla-policy",
    "title": "Platform SLA",
    "text": "Enterprise plans provide 99.99% monthly availability with dedicated support response times within 15 minutes.",
    "metadata": {"tenant_id": "tenant-corp-a"}
  }'
```

### 7. Query with Semantic Search & Evaluation
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What uptime SLA is provided for enterprise plans?",
    "similarity_top_k": 3,
    "score_threshold": 0.50,
    "filter": {"tenant_id": "tenant-corp-a"}
  }'
```

---

## Running Automated Tests

Run the test suite with in-memory vector store:

```bash
pytest tests/
```
All tests execute in sub-second time with zero external network or database requirements.
