---
name: "install-and-verify"
description: "Install, configure, orchestrate, and verify the Local Private RAG (Ollama + Chroma + FastAPI) service with zero outbound network egress."
---

# Skill: Install and Verify Local Private RAG

Use this skill to deploy, configure, and verify the complete 100% offline Local Private RAG stack.

## Step 1: Environment Setup & Dependencies
Ensure Python 3.12+ and Docker / Ollama are installed:
```bash
python3 --version
ollama --version
```

Create an isolated virtual environment and install pinned dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r starter/requirements.txt
```

## Step 2: Local Model Pulling
Pull the required open-weights LLM and embedding models via Ollama:
```bash
# Pull generation model (compact 3B model for edge/workstations)
ollama pull llama3.2:3b

# Pull dedicated local embedding model
ollama pull nomic-embed-text
```

Verify that Ollama lists the models locally:
```bash
ollama list
```

## Step 3: Configure Environment
Copy `.env.example` to `.env` and verify airgap settings:
```bash
cp starter/.env.example starter/.env
```

Ensure `RESTRICT_OUTBOUND_EGRESS=true` is enabled to enforce the zero-egress security policy.

## Step 4: Container Orchestration (Optional)
Run the complete stack with Docker Compose:
```bash
cd starter
docker compose up -d --build
docker compose ps
```

## Step 5: Verification Curls
Check application health and airgap compliance status:
```bash
curl -s http://localhost:8000/healthz | jq .
```
Expected response:
```json
{
  "status": "healthy",
  "airgap_safe": true,
  "cloud_egress_blocked": true,
  "vector_store": "chromadb",
  "llm_engine": "ollama",
  "model": "llama3.2"
}
```

Run the automated test suite in test mode:
```bash
pytest starter/tests/test_rag.py -v
```
