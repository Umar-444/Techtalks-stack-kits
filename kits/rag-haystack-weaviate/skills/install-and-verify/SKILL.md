---
name: install-and-verify
description: Comprehensive preflight setup, container orchestration, and test execution for Haystack 2.5+ and Weaviate.
---
# Install and Verify Skill: Haystack + Weaviate RAG

## 1. Virtual Environment Setup
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r starter/requirements.txt
```

## 2. Environment Configuration
```bash
cp starter/.env.example starter/.env
```
Ensure `WEAVIATE_URL=http://localhost:8085` and `WEAVIATE_GRPC_PORT=50051`.

## 3. Container Orchestration
```bash
cd starter
docker compose up -d weaviate
```

## 4. Run Automated Test Suite
```bash
pytest starter/tests/test_haystack_rag.py -v
```

## 5. Done Means
- Virtual environment is active and pinned packages installed without conflicts.
- Weaviate container responds with HTTP 200 on `/v1/.well-known/ready`.
- Test suite executes and passes 100% of assertions in under 3 seconds.
