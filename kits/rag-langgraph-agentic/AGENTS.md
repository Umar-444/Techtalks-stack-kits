# LangGraph + LangChain + Qdrant + Ragas Evals — Agent Operating Rules (AGENTS.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Table of Contents
- [01 Framework Architecture And Standards](#01-framework-architecture-and-standards)
- [02 Adaptive Retrieval And Query Rewriting](#02-adaptive-retrieval-and-query-rewriting)
- [03 Qdrant Vector Filtering And Payloads](#03-qdrant-vector-filtering-and-payloads)
- [04 Ragas Groundedness And Hallucination Evals](#04-ragas-groundedness-and-hallucination-evals)
- [05 Testing Verification And Ci](#05-testing-verification-and-ci)

---

<a id="01-framework-architecture-and-standards"></a>
## 01 Framework Architecture And Standards

﻿---
id: framework-architecture-and-standards
title: Framework Architecture & Standards
globs: "**/*.py"
alwaysApply: true
---
# Agentic RAG Architecture & LangGraph State Standards

## 1. Cyclical State Machine for Retrieval-Augmented Generation
- Classical RAG is a static linear pipeline: `Query -> Embed -> Retrieve -> Generate`.
- Agentic RAG introduces dynamic decision-making nodes:
  - `retrieve`: Query Qdrant for semantic matches.
  - `grade_documents`: Evaluates retrieved chunk relevance to the user question.
  - `decide_to_generate`: If documents are irrelevant, transition to `rewrite_query`; otherwise transition to `generate`.
  - `rewrite_query`: Transform and clarify user input for better vector search convergence.
  - `generate`: Synthesize answers using verified grounded context.
  - `grade_generation`: Check for hallucinations; if ungrounded, loop back.

## 2. Immutable State Schema
- Define state using `TypedDict` with explicit field semantics:
  ```python
  from typing import TypedDict, List

  class GraphState(TypedDict):
      question: str
      generation: str
      documents: List[str]
      iteration_count: int
      is_grounded: bool
  ```
- All nodes must return state deltas as dictionaries, never mutating the input state object.

## 3. Recursion Limits & Runaway Loop Defenses
- Every execution must set a strict recursion limit (default: 15 iterations):
  ```python
  config = {"recursion_limit": 15}
  await app.ainvoke(inputs, config=config)
  ```
- If `iteration_count` exceeds 3 query rewrites, route immediately to a fallback generation node or human review.


---

<a id="02-adaptive-retrieval-and-query-rewriting"></a>
## 02 Adaptive Retrieval And Query Rewriting

﻿---
id: adaptive-retrieval-and-query-rewriting
title: Adaptive Retrieval & Query Rewriting
globs: "**/*.py"
alwaysApply: true
---
# Adaptive Retrieval, Self-RAG & Query Rewriting

## 1. Document Relevance Grading
- Use a fast, specialized prompt or compact LLM to binary-grade document relevance:
  - Output strictly `{"score": "yes"}` or `{"score": "no"}` using structured schemas.
  - Filter out noisy or irrelevant chunks before context injection to minimize hallucination risk.

## 2. Query Transformation Logic
- When retrieved documents do not address the core query, the rewrite node inspects the original question and prior search failures:
  ```python
  def rewrite_query(state: GraphState) -> dict:
      better_question = transform_query_with_llm(state["question"])
      return {
          "question": better_question,
          "iteration_count": state["iteration_count"] + 1
      }
  ```
- Strips conversational fillers, expands domain-specific acronyms, and generates alternative keyword combinations.


---

<a id="03-qdrant-vector-filtering-and-payloads"></a>
## 03 Qdrant Vector Filtering And Payloads

﻿---
id: qdrant-vector-filtering-and-payloads
title: Qdrant Vector Filtering & Payload Isolation
globs: "**/*.py"
alwaysApply: true
---
# Qdrant Vector Search & Multi-Tenant Payload Security

## 1. Collection Configuration & Distance Metric
- Collections must configure Cosine distance and HNSW graph parameters:
  ```python
  from qdrant_client.http import models

  client.create_collection(
      collection_name="knowledge_base",
      vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
      hnsw_config=models.HnswConfigDiff(m=16, ef_construct=100)
  )
  ```

## 2. Strict Payload Filtering & Tenant Isolation
- Every vector query MUST include payload filters enforcing multi-tenant isolation:
  ```python
  tenant_filter = models.Filter(
      must=[
          models.FieldCondition(key="tenant_id", match=models.MatchValue(value=tenant_id)),
          models.FieldCondition(key="is_archived", match=models.MatchValue(value=False)),
      ]
  )
  results = client.search(
      collection_name="knowledge_base",
      query_vector=embedded_query,
      query_filter=tenant_filter,
      limit=5,
      score_threshold=0.65  # Drop low-similarity hallucination bait
  )
  ```


---

<a id="04-ragas-groundedness-and-hallucination-evals"></a>
## 04 Ragas Groundedness And Hallucination Evals

﻿---
id: ragas-groundedness-and-hallucination-evals
title: Ragas Groundedness & Hallucination Evals
globs: "**/*.py"
alwaysApply: true
---
# Ragas Groundedness Scoring & Hallucination Detection

## 1. Ragas Metric Triad
- Implement continuous scoring across three core Ragas metrics:
  1. **Faithfulness**: Are claims in the generated answer strictly derived from retrieved context?
  2. **Answer Relevance**: Does the generated answer directly address the user's inquiry?
  3. **Context Precision**: Did the retriever rank the most relevant chunks at the top?

## 2. Automated Self-Correction Loop
- The generation grader node inspects the generated output against the retrieved chunks:
  ```python
  def grade_generation(state: GraphState) -> str:
      if not verify_groundedness(state["generation"], state["documents"]):
          return "hallucination_detected"
      return "grounded"
  ```
- If hallucination is detected and iterations remain, route back to `generate` with a prompt warning: "Your previous answer included facts not supported by the context. Re-synthesize strictly using provided documents."


---

<a id="05-testing-verification-and-ci"></a>
## 05 Testing Verification And Ci

﻿---
id: testing-verification-and-ci
title: Testing, Verification & CI Invariants
globs: "**/*.py"
alwaysApply: true
---
# Testing Protocols, Mock LLMs & CI Quality Gates

## 1. Deterministic Graph Testing
- Unit tests must mock external LLM calls to verify graph topology, conditional branching, and termination guarantees in `< 1.0s` without API dependencies.
- Verify that a sequence of low-relevance documents triggers `rewrite_query` and that high-relevance triggers `generate`.

## 2. Container Security & Non-Root User
- Multi-stage `Dockerfile` executing as `USER 10001:10001`.
- Health probes verify FastAPI and Qdrant network connectivity.

## 3. Automated CI Scans
- Must pass:
  1. `gitleaks detect --no-git` with 0 secret leaks.
  2. `semgrep scan --config p/owasp-top-ten` with 0 blocking SAST findings.
  3. `python tools/validate_manifest.py` verifying full physical layout.
  4. `python tools/transpiler.py --check` guaranteeing zero dialect drift.


---

