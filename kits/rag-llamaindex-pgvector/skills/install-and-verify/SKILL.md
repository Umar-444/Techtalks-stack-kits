---
name: install-and-verify
description: Install, configure, orchestrate, and verify LlamaIndex + PostgreSQL pgvector RAG service.
---

# Install & Verify Skill: LlamaIndex + PostgreSQL pgvector + FastAPI

## Prerequisites
- Python 3.12+
- PostgreSQL 16+ with the `pgvector` extension enabled (`CREATE EXTENSION vector;`)
- Docker Engine 24.0+ and Docker Compose v2+

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
Spin up the local PostgreSQL 16 pgvector database and FastAPI LlamaIndex service:
```bash
cd starter/
cp .env.example .env
docker compose up --build -d
```

## Verification Probes
Run the following verification checks:

1. **FastAPI Health & Database Check**:
   ```bash
   curl -s http://localhost:8000/healthz
   ```
   *Expected Response*: `{"status":"ok","app":"rag-llamaindex-pgvector","database_connected":true,"version":"1.0.0"}`

2. **Verify pgvector Extension in PostgreSQL**:
   ```bash
   docker compose exec db psql -U postgres -d rag_db -c "SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';"
   ```
   *Expected Response*: Displays `vector` with version `0.7.0` or higher.

3. **In-Memory Automated Unit Tests**:
   ```bash
   pytest starter/tests/
   ```

## Failure Recovery Matrix

| Symptom | Root Cause | Remediation Command |
|---|---|---|
| `type "vector" does not exist` | The `vector` extension is not initialized in PostgreSQL | Run `CREATE EXTENSION IF NOT EXISTS vector;` inside your PostgreSQL database. |
| `connection to server at "localhost" (::1), port 5432 failed` | PostgreSQL service is stopped or port is blocked | Check `docker compose logs db` and confirm `POSTGRES_PORT=5432` is reachable. |
| `dimension mismatch (384 vs 1536)` | Embedding model output dimension does not match column type | Alter table column to matching dimension or update embedding model to BGE-small (384). |
| `psycopg.OperationalError: password authentication failed` | Incorrect password in `.env` | Ensure `.env` credentials match `docker-compose.yml` (`POSTGRES_PASSWORD=postgres`). |
| `LlamaIndex ServiceContext deprecation warning` | Legacy LlamaIndex code used | Migrate to `from llama_index.core import Settings` and configure settings directly. |

## Done Means
The `/healthz` endpoint returns HTTP 200 with `"database_connected": true`, the `vector` extension is active in PostgreSQL, and all unit tests pass with zero errors.
