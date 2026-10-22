---
name: first-feature
description: Build the canonical Semantic Document Search & RAG Q&A module with pgvector embeddings and structured LLM synthesis.
---

# Skill: First Feature (Semantic Search & RAG Q&A)

## 1. Document Model & Migration
Create `Document` model with `title`, `content`, `embedding` (vector 1536), `tenant_id`.

## 2. Vector Search Scope
Implement `scopeCosineSearch(Builder $query, array $vector, int $limit)` using PostgreSQL pgvector `<=>`.

## 3. RAG Q&A Controller
Expose endpoint `/api/ai/ask` that:
1. Embeds query string.
2. Retrieves top 3 matching documents.
3. Synthesizes answer using structured LLM output with citations.

## 4. Done Means
- Searching "security invariants" returns relevant security document.
- RAG response returns grounded answer with citation chips.
- Feature test passes with code 0.
