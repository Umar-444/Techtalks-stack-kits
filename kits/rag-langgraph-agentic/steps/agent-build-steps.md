# Agent Build Steps: LangGraph + Qdrant + Ragas Agentic RAG

Follow these 6 steps to scaffold, execute, and verify the LangGraph agentic RAG stack:

## Step 1: Environment Initialization & Preflight
Initialize virtual environment and install pinned dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r starter/requirements.txt
cp starter/.env.example starter/.env
```
Verification:
```bash
python -c "import langgraph, qdrant_client, fastapi; print('Dependencies verified')"
```

## Step 2: Multi-Tenant Qdrant Vector Store Setup
Configure the vector payload service with tenant isolation:
```bash
python -c "from app.vector_store import QdrantVectorService; vs = QdrantVectorService(); assert vs.is_healthy()"
```

## Step 3: LangGraph State Machine Construction
Build the cyclical state graph with retrieve, grade, rewrite, generate, and eval nodes:
```bash
python -c "from app.graph import run_agentic_rag; res = run_agentic_rag('test query'); assert 'answer' in res or 'generation' in res"
```

## Step 4: Ragas Groundedness & Hallucination Guardrail
Implement automated response verification before returning to callers:
```bash
python -c "from app.evals import ragas_evaluator; s = ragas_evaluator.evaluate_groundedness('q', [{'content':'a b c'}], 'a b c'); assert s >= 0.85"
```

## Step 5: FastAPI ASGI Service Launch
Launch the application server with non-root security boundaries and strict CORS:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```
Verification:
```bash
curl -f http://localhost:8080/health
```

## Step 6: Automated Security & Regression Suite
Run full test suite and verify compliance across all 12 security checks:
```bash
pytest starter/tests/test_agentic_rag.py -v
```
