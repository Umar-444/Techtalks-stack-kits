# Agent Build Steps: Haystack Pipelines + Weaviate RAG

Follow these 6 steps to scaffold, execute, and verify the Haystack + Weaviate RAG stack:

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
python -c "import haystack, weaviate, fastapi; print('Dependencies verified')"
```

## Step 2: Weaviate Hybrid Collection Setup
Configure Weaviate collection with hybrid search properties and multi-tenancy:
```bash
python -c "from app.weaviate_service import weaviate_service; assert weaviate_service.is_healthy()"
```

## Step 3: Explicit Haystack DAG Assembly
Construct the pipeline DAG connecting retriever, prompt builder, and generator:
```bash
python -c "from app.pipeline import rag_pipeline; res = rag_pipeline.run('test query'); assert 'answer' in res"
```

## Step 4: Faithfulness & Groundedness Evaluator
Verify automated evaluation component:
```bash
python -c "from app.pipeline import faithfulness_evaluator; s = faithfulness_evaluator.evaluate('a b c', [{'content':'a b c'}]); assert s >= 0.85"
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
pytest starter/tests/test_haystack_rag.py -v
```
