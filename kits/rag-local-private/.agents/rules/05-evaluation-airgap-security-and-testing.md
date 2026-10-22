# Offline Evaluation, Airgap Security & Testing

# 05 - Offline Evaluation, Airgap Security & Testing

## 1. Zero-Egress Network Policy & Airgap Assertion
- **Outbound Request Blocker:** When `RESTRICT_OUTBOUND_EGRESS=true`, intercept any HTTP client initialization or outbound DNS requests attempting to contact public hostnames. Only loopback (`127.0.0.1`, `localhost`) and Docker bridge network aliases (`ollama`, `chroma`) are permitted.
- **Airgap Health Probe:** The `GET /healthz` endpoint must return the airgap compliance status:
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

## 2. Container Hardening & Unprivileged User
- **Non-Root Execution:** The production Dockerfile must run as an explicit unprivileged UID/GID (`USER 10001:10001`). Never execute container processes as `root`.
- **Read-Only Root Filesystem:** Mount writable volumes exclusively to designated persistence paths (`/app/data/chromadb`).
- **Multi-Stage Build:** Use multi-stage builds (`python:3.12-slim`) to discard build tools, compilers, and development headers from the final runtime image.

## 3. Offline RAG Evaluation Guardrail
- Evaluate query responses using offline metrics without calling external cloud LLMs:
  - **Context Relevance:** Fraction of retrieved context chunks containing query key concepts.
  - **Groundedness / Faithfulness:** Proportion of response claims directly corroborated by text within the retrieved context chunks.
  - **Leak Check:** Verification that responses strictly respect the requesting user's classification level and do not leak higher-classification text.
- Return structured evaluation reports via `POST /api/v1/evaluate`.

## 4. Automated Testing Standards
- All tests in `tests/test_rag.py` must run with `TEST_MODE=true` using `pytest`:
  - `test_healthz`: Verify health probe and airgap compliance flags.
  - `test_document_ingest`: Verify text extraction, chunking, and ChromaDB insertion.
  - `test_query_retrieval`: Verify similarity query, metadata filtering by tenant and classification.
  - `test_prompt_injection_defense`: Verify that adversarial instructions in documents are safely bounded.
  - `test_offline_evaluation`: Verify structured groundedness scoring.
- Pytest execution must complete in under 2 seconds with zero external network connectivity.
