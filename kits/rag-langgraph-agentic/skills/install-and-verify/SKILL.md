---
name: install-and-verify
description: Comprehensive preflight verification, virtual environment setup, and test runner execution for LangGraph + Qdrant Agentic RAG.
---
# Install and Verify Skill: Agentic LangGraph RAG

## 1. Virtual Environment Setup
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Environment Configuration
```bash
cp .env.example .env
```
Ensure `QDRANT_URL=http://localhost:6333` is reachable or using in-memory client.

## 3. Run Automated Test Suite
```bash
pytest -v tests/
```

## 4. Launch Service
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```
Check health: `curl http://localhost:8080/health`.
