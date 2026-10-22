---
name: install-and-verify
description: Install, orchestrate, and verify the Agentic LangGraph + CrewAI + FastAPI multi-agent stack.
---

# Install & Verify Skill: Agentic LangGraph + CrewAI + FastAPI

## Prerequisites
- Python 3.12+ (or Docker Engine 24+ with Compose v2)
- Redis 7+ (local daemon or containerized service)
- OpenAI / Anthropic API Key or compatible local Ollama server

## OS-Specific Commands

### Linux / macOS
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Windows (PowerShell)
```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Docker Compose Quickstart
```bash
docker compose up --build -d
```

## Post-Install Verification
Run the verification curl against the local FastAPI orchestrator:
```bash
curl -X GET http://localhost:8000/healthz
```
Expected output:
```json
{"status":"ok","app":"agentic-langgraph-crewai","version":"1.0.0"}
```

Verify workflow execution:
```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"task": "Analyze security implications of SSRF in agent tool call loops"}'
```

## Failure Recovery Matrix
| Symptom | Probable Cause | Resolution |
| :--- | :--- | :--- |
| `ConnectionRefusedError: [Errno 111] Redis` | Redis daemon is not running on port 6379 | Start Redis via `docker compose up -d redis` or install local `redis-server` |
| `GraphRecursionError: Recursion limit reached` | LangGraph circular conditional routing loop | Verify node routing logic in `app/graph.py` and ensure `recursion_limit` parameter is explicitly capped at 15 |
| `ModuleNotFoundError: crewai` | Incomplete pip environment isolation | Run `pip install -r requirements.txt` inside active virtual environment |

## Done Means
The FastAPI server boots without warnings, connects to Redis state checkpointer, and completes an end-to-end two-node agent workflow responding with HTTP 200 OK.
