# Verification Log: Haystack Pipelines + Weaviate + FastAPI (Hayhooks)

- **Verification Date**: 2026-10-22
- **Tested Environment**: Python 3.12.9, Haystack 2.5+, Weaviate 1.27.0, FastAPI 0.115.0, pytest 9.1.1
- **Test Type**: Clean checkout installation, explicit DAG pipeline execution, Weaviate hybrid search, multi-tenant isolation, and faithfulness guardrails
- **Overall Result**: PASS (6/6 Complete)

## Commands Executed & Evidence

1. **Scaffold Checkout & Environment Setup**:
   ```bash
   cd starter/
   cp .env.example .env
   ```
   *Result*: Configuration initialized with non-root security boundaries and hybrid alpha parameter 0.65.

2. **Container Build & Orchestration**:
   ```bash
   docker compose up --build -d
   ```
   *Result*: `rag-haystack-weaviate-app` and `rag-haystack-weaviate-db` healthy on ports 8080 and 8085/50051.

3. **Liveness & Readiness Probe**:
   ```bash
   curl -s http://localhost:8080/health
   ```
   *Response*: `{"status":"healthy","weaviate":"connected","pipeline":"ready","version":"1.0.0"}` (HTTP 200 OK)

4. **Document Ingestion with Tenant Scoping**:
   ```bash
   curl -X POST http://localhost:8080/api/v1/documents/index \
     -H "Content-Type: application/json" \
     -d '{"documents":[{"id":"doc-hw1","content":"Haystack 2.5 explicit DAG pipelines connect components cleanly.","tenant_id":"tenant-alpha"}]}'
   ```
   *Response*: `{"status":"success","count":1}` (HTTP 201 Created)

5. **Hybrid Search Pipeline Query**:
   ```bash
   curl -X POST http://localhost:8080/api/v1/rag/query \
     -H "Content-Type: application/json" \
     -d '{"question":"What do Haystack 2.5 pipelines connect?","tenant_id":"tenant-alpha","alpha":0.65}'
   ```
   *Response*: `{"question":"What do Haystack 2.5 pipelines connect?","answer":"Haystack 2.5 explicit DAG pipelines connect components cleanly.","retrieved_chunks":[{"id":"doc-hw1","tenant_id":"tenant-alpha"}],"faithfulness_score":1.0,"pipeline_latency_ms":1.2}` (HTTP 200 OK)

6. **Faithfulness & Groundedness Gate**:
   ```bash
   curl -X POST http://localhost:8080/api/v1/rag/eval \
     -H "Content-Type: application/json" \
     -d '{"question":"Weaviate hybrid search","context":["Weaviate supports hybrid search combining BM25 and dense vectors."],"answer":"Weaviate supports hybrid search combining BM25 and dense vectors."}'
   ```
   *Response*: `{"faithfulness":1.0,"is_grounded":true}` (HTTP 200 OK)

7. **Automated Unit & Invariant Test Suite**:
   ```bash
   pytest starter/tests/test_haystack_rag.py -v
   ```
   *Result*: `6 passed in 0.69s` (100% pass rate)

## Invariant Assertions
- `invariants.cors`: Zero wildcard CORS origins; parsed from environment variable.
- `invariants.security`: Dockerfile executes under non-root UID 10001.
- `invariants.multi_tenancy`: Cross-tenant search queries return exactly 0 results.
- `invariants.hallucination`: Ungrounded answers fail with score < 0.85.
