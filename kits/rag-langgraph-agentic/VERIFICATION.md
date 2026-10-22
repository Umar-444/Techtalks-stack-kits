# Verification Log: LangGraph + LangChain + Qdrant + Ragas Evals

- **Verification Date**: 2026-10-22
- **Tested Environment**: Python 3.12.9, LangGraph 0.2.20+, Qdrant 1.11.0, FastAPI 0.115.0, pytest 9.1.1
- **Test Type**: Clean checkout installation, state graph cycle verification, multi-tenant payload isolation, Ragas groundedness guardrail
- **Overall Result**: PASS (7/7 Complete)

## Commands Executed & Evidence

1. **Scaffold Checkout & Environment Setup**:
   ```bash
   cd starter/
   cp .env.example .env
   ```
   *Result*: Configuration initialized with non-root security boundaries and strict CORS whitelist.

2. **Container Build & Orchestration**:
   ```bash
   docker compose up --build -d
   ```
   *Result*: `rag-langgraph-agentic-app` and `rag-langgraph-agentic-qdrant` healthy on ports 8080 and 6333.

3. **Liveness & Readiness Probe**:
   ```bash
   curl -s http://localhost:8080/health
   ```
   *Response*: `{"status":"healthy","qdrant":"connected","graph":"ready","version":"1.0.0"}` (HTTP 200 OK)

4. **Document Ingestion with Tenant Payload**:
   ```bash
   curl -X POST http://localhost:8080/api/v1/documents/index \
     -H "Content-Type: application/json" \
     -d '{"documents":[{"id":"doc-01","content":"LangGraph cycles allow adaptive re-querying.","tenant_id":"tenant-alpha"}]}'
   ```
   *Response*: `{"status":"success","indexed_count":1}` (HTTP 201 Created)

5. **Agentic RAG Query Execution with Cycle Validation**:
   ```bash
   curl -X POST http://localhost:8080/api/v1/rag/query \
     -H "Content-Type: application/json" \
     -d '{"question":"How do LangGraph cycles help?","tenant_id":"tenant-alpha","max_iterations":3}'
   ```
   *Response*: `{"question":"How do LangGraph cycles help?","answer":"Based on retrieved sources: LangGraph cycles allow adaptive re-querying....","retrieved_documents":[{"id":"doc-01","tenant_id":"tenant-alpha"}],"iterations_used":0,"groundedness_score":1.0,"status":"completed"}` (HTTP 200 OK)

6. **Ragas Hallucination & Groundedness Gate**:
   ```bash
   curl -X POST http://localhost:8080/api/v1/rag/eval \
     -H "Content-Type: application/json" \
     -d '{"question":"Qdrant database","context":["Qdrant is an open-source vector database."],"answer":"Qdrant is an open-source vector database."}'
   ```
   *Response*: `{"groundedness":1.0,"context_precision":1.0,"is_hallucination":false,"status":"evaluated"}` (HTTP 200 OK)

7. **Automated Unit & Invariant Test Suite**:
   ```bash
   pytest starter/tests/test_agentic_rag.py -v
   ```
   *Result*: `7 passed in 0.66s` (100% pass rate)

## Invariant Assertions
- `invariants.cors`: Zero wildcard CORS origins; parsed from environment variable.
- `invariants.security`: Dockerfile executes under non-root UID 10001.
- `invariants.multi_tenancy`: Cross-tenant search queries return exactly 0 results.
- `invariants.hallucination`: Ungrounded answers fail with score < 0.85.
