# RAG FastAPI + Qdrant + FastEmbed Stack Kit

[![Stack Status: Ready to Ship](https://img.shields.io/badge/status-Ready%20to%20Ship-emerald?style=flat-square)](kit.yaml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue?style=flat-square)](https://www.python.org/)
[![FastAPI 0.115](https://img.shields.io/badge/fastapi-0.115-009688?style=flat-square)](https://fastapi.tiangolo.com/)
[![Qdrant 1.12](https://img.shields.io/badge/qdrant-1.12-DC2626?style=flat-square)](https://qdrant.tech/)
[![FastEmbed 0.4](https://img.shields.io/badge/fastembed-0.4-orange?style=flat-square)](https://github.com/qdrant/fastembed)

Production-grade Retrieval Augmented Generation (RAG) and vector similarity search service pairing FastAPI with the Qdrant Rust vector database, local FastEmbed dense vector generation, and strict multi-tenant payload isolation.

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
                   |        FastAPI RAG Service        |
                   |  - Lifespan & Connection Pools    |
                   |  - Input Validation (Pydantic v2) |
                   |  - Sliding-Window Text Chunker    |
                   |  - FastEmbed Local ONNX Engine    |
                   +-----------------+-----------------+
                                     |
                       Single-Stage Filtered Search
                                     v
                   +-----------------+-----------------+
                   |    Qdrant Vector Database v1.12   |
                   |  - Cosine Distance Metric         |
                   |  - HNSW Graph (m=16, ef=100)      |
                   |  - Payload Keyword Index (tenant) |
                   |  - Persistent Disk Storage        |
                   +-----------------------------------+
```

---

## Key Features

1. **Sub-30ms p95 Vector Retrieval**: High-throughput HNSW index traversal backed by Qdrant's Rust vector engine.
2. **Zero-Cost Local Embeddings**: Pre-integrated with FastEmbed (`BAAI/bge-small-en-v1.5`, 384 dimensions) running locally via ONNX Runtime without remote API latency or token expenses.
3. **Multi-Tenant Isolation**: Enforced single-stage payload filtering (`models.Filter`) ensuring cross-tenant queries cannot leak vectors across organizational boundaries.
4. **Sliding-Window Chunking**: Splits large documents into 500-character windows with 50-character overlaps, preserving semantic context and offsets.
5. **Prompt Injection Hardening**: Delimited context assembly separating untrusted knowledge chunks from system instructions.
6. **Zero-Dependency In-Memory Testing**: Embedded Qdrant mode (`QdrantClient(":memory:")`) executing entire test suites in milliseconds without Docker.

---

## Quickstart with Docker Compose

Spin up the local multi-container environment:

```bash
# 1. Clone the repository
git clone https://github.com/Umar-444/Techtalks-stack-kits.git
cd Techtalks-stack-kits/kits/rag-fastapi-qdrant/starter

# 2. Start services (FastAPI web + Qdrant vector database)
docker compose up --build -d
```

Access services:
- **API Documentation (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check Probe**: [http://localhost:8000/healthz](http://localhost:8000/healthz)
- **Qdrant Dashboard & Web UI**: [http://localhost:6333/dashboard](http://localhost:6333/dashboard)

---

## 7-Part Native Installation Guide

### 1. Prerequisites
- Python 3.12+
- Docker Engine & Docker Compose (or local Qdrant standalone binary)

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
Default configuration connects to `localhost:6333` with collection `documents` and 384-dimensional vectors.

### 4. Start Local Qdrant Engine
If running without Docker, start Qdrant via binary or docker container:
```bash
docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant:v1.12.0
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
    "document_id": "policy-01",
    "title": "Remote Work Policy",
    "text": "Employees receive up to $1,000 annually for home office equipment reimbursement.",
    "metadata": {"tenant_id": "org-alpha"}
  }'
```

### 7. Query with Semantic Search
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How much can I spend on office equipment?",
    "top_k": 3,
    "score_threshold": 0.50,
    "filter": {"tenant_id": "org-alpha"}
  }'
```

---

## Running Automated Tests

Run the test suite with in-memory Qdrant:

```bash
pytest tests/
```
All tests execute against `QdrantClient(":memory:")` with zero external dependencies.
