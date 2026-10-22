# Haystack Pipelines + Weaviate + FastAPI (Hayhooks) — Agent Operating Rules (AGENTS.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Table of Contents
- [01 Framework Architecture And Standards](#01-framework-architecture-and-standards)
- [02 Hybrid Retrieval And Reciprocal Rank Fusion](#02-hybrid-retrieval-and-reciprocal-rank-fusion)
- [03 Weaviate Collections And Tenant Isolation](#03-weaviate-collections-and-tenant-isolation)
- [04 Evaluators And Pipeline Validation](#04-evaluators-and-pipeline-validation)
- [05 Testing Verification And Ci](#05-testing-verification-and-ci)

---

<a id="01-framework-architecture-and-standards"></a>
## 01 Framework Architecture And Standards

# Framework Architecture and Standards: Haystack 2.5+ and Weaviate

1. **Explicit DAG Component Wiring**: Haystack 2.x uses explicit, directional DAG connections via `pipeline.connect("component_a.output", "component_b.input")`. Never use implicit or hidden execution flow.
2. **Component Isolation**: Every pipeline component must implement the `@component` decorator with typed inputs and outputs. Do not mutate global state inside components.
3. **Async FastAPI Layer**: Expose pipeline executions through FastAPI endpoints with typed Pydantic models. All blocking pipeline calls must execute asynchronously or in a worker thread pool.
4. **Environment Invariant**: All external service hosts (`WEAVIATE_URL`, `OPENAI_API_BASE`) must be injected through environment variables. Zero hardcoded localhost URLs in production code.
5. **Python 3.12+ Typing**: Use standard type annotations (`list[str]`, `dict[str, Any]`, `str | None`). Do not use legacy typing imports (`typing.List`, `typing.Optional`).


---

<a id="02-hybrid-retrieval-and-reciprocal-rank-fusion"></a>
## 02 Hybrid Retrieval And Reciprocal Rank Fusion

# Hybrid Retrieval and Reciprocal Rank Fusion

1. **Hybrid Search Composition**: Combine dense vector similarity with BM25 sparse keyword matching using Weaviate's native hybrid search operator.
2. **Alpha Parameter Calibration**: Set `alpha` between `0.0` (pure BM25 sparse) and `1.0` (pure vector dense). The production baseline must default to `alpha=0.65` for balanced semantic domain recall.
3. **Score Normalization and Thresholding**: Apply reciprocal rank fusion (RRF) to merge candidate lists from sparse and dense channels. Reject document candidates whose fused score falls below `0.40`.
4. **Query Preprocessing**: Sanitize incoming query text to strip prompt injection tags and excessive wildcard syntax before submitting to Weaviate hybrid search.
5. **Result Limit Boundaries**: Hard-limit retrieved chunk count to `top_k=5` in the retriever component to prevent context window bloat and excessive LLM token consumption.


---

<a id="03-weaviate-collections-and-tenant-isolation"></a>
## 03 Weaviate Collections And Tenant Isolation

# Weaviate Collections and Multi-Tenant Isolation

1. **Weaviate v4 Python Client**: All schema definitions and queries must utilize the `weaviate-client` v4 collection API (`client.collections.get(...)` and `client.collections.create(...)`). Legacy v3 methods (`client.schema.create_class`) are prohibited.
2. **Multi-Tenancy Configuration**: Enable multi-tenancy at collection creation time via `Configure.multi_tenancy(enabled=True)` whenever managing multiple client or user organizations.
3. **Tenant Scoping on Every Query**: Never execute a search query without explicit tenant context. Obtain tenant-scoped collection references via `collection.with_tenant(tenant_id)`.
4. **Property Indexing**: Configure vectorizer properties explicitly. Mark text chunks with `skip=False` for vector indexing and administrative metadata (UUIDs, timestamps) with `skip=True`.
5. **Connection Pooling and Lifecycle**: Manage Weaviate client lifecycle using context managers (`with weaviate.connect_to_custom(...)`) or FastAPI lifespan handlers. Never leak open gRPC channels.


---

<a id="04-evaluators-and-pipeline-validation"></a>
## 04 Evaluators And Pipeline Validation

# Evaluators and Pipeline Validation

1. **Built-in Haystack Evaluators**: Integrate Haystack's native evaluation components (`FaithfulnessEvaluator`, `ContextRelevanceEvaluator`) to continuously validate pipeline outputs against source documents.
2. **Groundedness SLA Gate**: Every generated response in automated benchmark suites must achieve a faithfulness score `>= 0.85`. Responses scoring below this threshold must trigger alerting or query reformulation.
3. **Zero-Cost Heuristic Fallback**: Test suites and local CI jobs must utilize deterministic heuristic scoring fixtures that assess token overlap and claim inference without requiring external OpenAI API keys.
4. **Latency Budget Assertion**: A standard RAG query cycle (hybrid retrieval + context assembly + generation) must complete within a p95 latency budget of `< 1500ms`.
5. **Evaluation Metric Logging**: Log structured evaluation metrics (retrieval recall, context precision, generation latency) in JSON format for observability pipelines.


---

<a id="05-testing-verification-and-ci"></a>
## 05 Testing Verification And Ci

# Testing, Verification, and CI Invariants

1. **Non-Root Container Security**: Dockerfiles must compile with a dedicated unprivileged user (`USER 10001:10001`). Never execute services as root inside production containers.
2. **Strict CORS Policy**: CORS middleware must parse allowed origins strictly from the `ALLOWED_ORIGINS` environment variable. Never configure `allow_origins=["*"]`.
3. **Deterministic Test Isolation**: Pytest test cases must run independently with mock or in-memory vector storage fallback, ensuring the entire test suite passes in under 3 seconds.
4. **Dependency Pinning**: All dependencies in `requirements.txt` must be pinned with exact or minimum bounded versions (`package>=X.Y.Z`).
5. **No Secret Invariants**: Zero credentials, API keys, or private certificates may be committed to version control. Verified via automated Gitleaks scans.


---

