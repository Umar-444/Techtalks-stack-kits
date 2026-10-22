---
name: install-and-verify
description: Install, configure, orchestrate, and verify the FastAPI + Qdrant vector database RAG service.
---

# Install & Verify Skill: FastAPI + Qdrant RAG Service

## Prerequisites
- Python 3.12+
- Docker Engine 24.0+ and Docker Compose v2+
- 4GB+ available system RAM (for vector embedding models and Qdrant in-memory graphs)

## OS-Specific Installation Commands

### Linux / macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r starter/requirements.txt
```

### Windows (PowerShell)
```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r starter/requirements.txt
```

## Docker Compose Orchestration
Spin up the local Qdrant vector database (port 6333) and the FastAPI RAG service (port 8000):
```bash
cd starter/
cp .env.example .env
docker compose up --build -d
```

## Verification Probes
Run the following verification checks:

1. **FastAPI Health & Qdrant Connectivity**:
   ```bash
   curl -s http://localhost:8000/healthz
   ```
   *Expected Response*: `{"status":"ok","app":"rag-fastapi-qdrant","qdrant_connected":true,"version":"1.0.0"}`

2. **Qdrant Native Cluster Health**:
   ```bash
   curl -s http://localhost:6333/healthz
   ```
   *Expected Response*: `healthz check passed`

3. **In-Memory Automated Unit Tests**:
   ```bash
   pytest starter/tests/
   ```

## Failure Recovery Matrix

| Symptom | Root Cause | Remediation Command |
|---|---|---|
| `Connection refused: localhost:6333` | Qdrant container is still initializing or stopped | Run `docker compose logs qdrant` and verify port 6333 is not bound by another process. |
| `Dimension mismatch: 384 vs 1536` | Embedding model output does not match vector config | Ensure `FastEmbed` uses `BAAI/bge-small-en-v1.5` (dim 384) or recreate collection with matching size. |
| `OutOfMemoryError during embedding` | System ran out of RAM while loading model weights | Allocate at least 2GB RAM to the Docker container or set `EMBEDDING_BATCH_SIZE=16`. |
| `PydanticValidationError on ingest` | Request body missing mandatory `text` or `document_id` | Validate payload matches schema: `{"document_id": "doc1", "text": "content", "metadata": {}}`. |
| `FastEmbed model download timeout` | Hugging Face model cache timeout | Pre-download model or set `HF_HUB_ENABLE_HF_TRANSFER=1`. |

## Done Means
The `/healthz` endpoint returns HTTP 200 with `"qdrant_connected": true`, the local embedding model vectorizes sample text into 384-dimensional dense vectors, and all test cases pass without errors.
