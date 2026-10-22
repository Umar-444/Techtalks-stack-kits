# Agent Build Steps: RAG FastAPI + Qdrant + FastEmbed

Execute the following sequential steps to build, orchestrate, verify, and test the FastAPI + Qdrant vector retrieval service. Every step includes an explicit verification command and expected output.

---

## Step 1: Python Virtual Environment & Dependencies
Create the isolated Python virtual environment and install all pinned dependencies including FastAPI, Qdrant Client, and FastEmbed.

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r starter/requirements.txt
```

**Verification Command**:
```bash
python -c "import fastapi, qdrant_client, pydantic; print('FastAPI:', fastapi.__version__, '| Qdrant Client:', qdrant_client.__version__)"
```
**Expected Output**:
```
FastAPI: 0.115.x | Qdrant Client: 1.12.x
```

---

## Step 2: Environment Configuration Setup
Copy `.env.example` to `.env` in the starter directory and configure vector dimensions.

```bash
cp starter/.env.example starter/.env
```

**Verification Command**:
```bash
python -c "import os; from pathlib import Path; assert Path('starter/.env').exists(), 'Missing .env file'"
```
**Expected Output**:
```
(No error; exit code 0)
```

---

## Step 3: FastEmbed & Embedding Pipeline Verification
Verify that the embedding service initializes the local ONNX embedding model and produces normalized 384-dimensional dense vectors.

```bash
cd starter/
python -c "from app.services.embedding_service import embedding_service; v = embedding_service.embed_query('Test query'); assert len(v) == 384; print('Vector dim:', len(v))"
```

**Verification Command**:
```bash
python -c "from app.services.embedding_service import embedding_service; chunks = embedding_service.chunk_text('Sample text for chunk verification'); assert len(chunks) >= 1; print('Chunks count:', len(chunks))"
```
**Expected Output**:
```
Chunks count: 1
```

---

## Step 4: Multi-Container Docker Orchestration
Spin up the coordinated multi-container architecture (FastAPI service + Qdrant vector database container).

```bash
docker compose up --build -d
```

**Verification Command**:
```bash
docker compose ps
```
**Expected Output**:
```
NAME                         IMAGE                  STATUS                   PORTS
starter-qdrant-1             qdrant/qdrant:v1.12.0  Up (healthy)             0.0.0.0:6333->6333/tcp
starter-web-1                starter-web            Up                       0.0.0.0:8000->8000/tcp
```

---

## Step 5: Ingest Canonical Knowledge Document
Ingest a sample knowledge base document into the Qdrant `documents` collection with tenant isolation metadata.

```bash
curl -X POST http://localhost:8000/api/v1/documents/ingest \
  -H "Content-Type: application/json" \
  -d '{"document_id":"kb-init-01","title":"System SLA","text":"Platform availability is guaranteed at 99.95% uptime monthly.","metadata":{"tenant_id":"demo"}}'
```

**Verification Command**:
```bash
curl -s http://localhost:8000/api/v1/documents/ingest -H "Content-Type: application/json" -d '{"document_id":"probe-doc","text":"Health probe document","metadata":{"tenant_id":"probe"}}' | grep "indexed"
```
**Expected Output**:
```
"status":"indexed"
```

---

## Step 6: End-to-End Vector Query & Automated Test Suite Execution
Execute the automated test suite verifying collection provisioning, semantic search, and tenant filtering.

```bash
pytest starter/tests/
curl -s http://localhost:8000/healthz
```

**Verification Command**:
```bash
curl -I http://localhost:8000/healthz
```
**Expected Output**:
```
HTTP/1.1 200 OK
Content-Type: application/json
```
