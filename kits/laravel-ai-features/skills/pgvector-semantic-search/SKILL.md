---
name: pgvector-semantic-search
description: Generate document embeddings, configure PostgreSQL HNSW indexes, and execute cosine similarity queries.
---

# Skill: pgvector Semantic Search

## Workflow
1. Generate 1536-dim vector via `EmbeddingService`.
2. Query database:
```php
Document::where('tenant_id', $tenantId)
    ->orderByRaw('embedding <=> ?', [json_encode($vector)])
    ->limit(5)
    ->get();
```

## Done Means
- EXPLAIN query confirms `Index Scan using documents_embedding_hnsw_idx`.
