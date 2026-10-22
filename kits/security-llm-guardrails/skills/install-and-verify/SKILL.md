---
name: install-and-verify
description: Complete preflight verification, virtual environment setup, and automated adversarial test suite execution for LLM Guardrails & AI Gateway.
---
# Install and Verify Skill: LLM Guardrails & AI Gateway

## 1. Virtual Environment Setup
Initialize Python 3.12+ isolated environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Configuration & Environment Variables
Copy the default environment configuration:
```bash
cp .env.example .env
```
Ensure `REDIS_URL` is accessible or that the gateway falls back gracefully to in-memory rate limiting.

## 3. Run Automated Security & Adversarial Test Suite
Verify that prompt injection filters, PII anonymizers, and budget checks pass:
```bash
pytest -v tests/
```

## 4. Boot Local Development Gateway
Run the FastAPI gateway with live reload:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```
Verify the health probe:
```bash
curl http://localhost:8080/health
```
