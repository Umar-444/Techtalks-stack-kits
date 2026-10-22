# Verification Guide: Local Private RAG (Ollama + Chroma + FastAPI)

Follow this 6-phase verification guide to confirm that the Local Private RAG service is functioning cleanly with zero egress, deterministic retrieval, and complete regulatory compliance.

---

## Phase 1: Environment & Dependency Verification
Verify Python version, virtual environment, and dependency packages:
```bash
python --version
pip list | grep -E "fastapi|uvicorn|chromadb|pydantic|httpx"
```
**Expected Output:** Python 3.12+ with all production libraries installed.

---

## Phase 2: Manifest & Transpiler Zero-Drift Check
Run manifest validation and check for dialect drift:
```bash
python tools/validate_manifest.py
python tools/transpiler.py --kit kits/rag-local-private --check
```
**Expected Output:**
```
[PASSED] Manifest validation for rag-local-private passed!
=== Transpiling 5 rules for: Local Private RAG (Ollama + Chroma + FastAPI) ===
[PASSED] All agent dialect outputs match rules/source/* perfectly!
```

---

## Phase 3: Automated Pytest Suite Execution
Execute the automated test suite in test mode with in-memory isolation:
```bash
python -m pytest kits/rag-local-private/starter/tests/test_rag.py -v
```
**Expected Output:**
```
test_healthz PASSED
test_document_ingest PASSED
test_query_retrieval_success PASSED
test_cross_tenant_isolation PASSED
test_classification_clearance_filtering PASSED
test_offline_evaluation PASSED
6 passed in < 1s
```

---

## Phase 4: Semgrep SAST & Security Invariant Audit
Scan all source files for OWASP API vulnerabilities and security policies:
```bash
semgrep scan --config "p/owasp-top-ten" --config "p/php" --config "p/security-code-scan" --error
```
**Expected Output:**
```
Scan completed successfully.
Findings: 0 (0 blocking)
```

---

## Phase 5: Airgap & Health Check Endpoint
Query the live or local FastAPI instance:
```bash
curl -s http://localhost:8000/healthz | jq .
```
**Expected Output:**
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

---

## Phase 6: Document Ingestion & Tenant Query
Ingest a confidential record and verify retrieval:
```bash
# Ingest
curl -X POST http://localhost:8000/api/v1/documents/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "test-doc-01",
    "title": "Airgap Test Document",
    "tenant_id": "tenant-001",
    "classification": "CONFIDENTIAL",
    "text": "Enterprise airgap systems prevent outbound packets to public cloud APIs."
  }'

# Query
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What do enterprise airgap systems prevent?",
    "tenant_id": "tenant-001",
    "user_classification": "CONFIDENTIAL"
  }'
```
**Expected Output:** Grounded answer with source citations and `airgap_safe: true`.
