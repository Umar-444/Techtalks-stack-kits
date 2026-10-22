# 04 Rag Retrieval Reranking And Context

﻿# Rule 4: Vector Retrieval, Payload Filtering & Context Assembly

## Context & Principles
- Retrieve relevant context with low latency using Qdrant vector search coupled with strict payload filtering for multi-tenant isolation.
- Enforce score thresholding (e.g. `score_threshold=0.65`) to eliminate hallucinated context from low-relevance matches.
- Format retrieved chunks into clear, structured context blocks with verifiable source citations.

## Standards
1. **Multi-Tenant Filter Invariants**:
   ```python
   query_filter = models.Filter(
       must=[
           models.FieldCondition(key="tenant_id", match=models.MatchValue(value=tenant_id)),
       ]
   )
   ```
   *Never execute unfiltered vector searches across multi-tenant collections.*
2. **Context Assembly with Citations**:
   Assemble context snippets into numbered citation blocks:
   ```markdown
   [Context 1] (doc_id: handbook.md, score: 0.89):
   "Refund policies allow full refunds within 30 days of purchase..."
   ```
3. **Budgeted Context Windows**: Limit total retrieved tokens to a maximum of 3,000 tokens to leave sufficient headroom for LLM response generation and avoid context truncation.
4. **Fallback on Empty Results**: When no documents exceed the score threshold, gracefully inform the caller rather than sending irrelevant noise to the generation model.

