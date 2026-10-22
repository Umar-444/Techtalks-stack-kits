---
id: 04-retrieval-query-engine-and-reranking
title: Vector Retrieval, Metadata Filtering & Response Synthesis
globs: "*"
alwaysApply: true
---
# Rule 4: Vector Retrieval, Metadata Filtering & Response Synthesis

## Context & Principles
- Retrieve semantically relevant context nodes using PostgreSQL vector distance calculations coupled with strict metadata filtering.
- Prevent cross-tenant information leakage by mandating tenant filter predicates on every query engine execution.
- Synthesize grounded, factual answers using structured context delimiters and explicit source citations.

## Standards
1. **Metadata Filtered Retriever**:
   ```python
   from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter

   filters = MetadataFilters(
       filters=[ExactMatchFilter(key="tenant_id", value=tenant_id)]
   )
   retriever = index.as_retriever(
       similarity_top_k=5,
       filters=filters
   )
   ```
2. **Citation Assembly**:
   Format retrieved nodes with score badges and document IDs before returning responses:
   ```markdown
   [Source 1] (Score: 0.82, Doc: policy.pdf):
   "Employees may expense up to $1,000 annually for ergonomic furniture..."
   ```
3. **Score Thresholding**: Filter out nodes with similarity scores below `0.60` to eliminate irrelevant context from being passed to LLM generation prompts.
4. **Context Budgeting**: Cap total retrieved context at 3,000 tokens to guarantee room for generation without truncation.
