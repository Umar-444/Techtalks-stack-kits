---
name: pgvector-hnsw-optimization
description: Tune PostgreSQL pgvector HNSW indexing parameters, query-time ef_search, and JSONB metadata GIN indexes.
---

# PostgreSQL pgvector HNSW Index Optimization Skill

## Objective
Configure and tune high-throughput HNSW index parameters on PostgreSQL pgvector tables for low-latency vector similarity retrieval.

## 1. Index Construction Optimization
In PostgreSQL 16+, create the HNSW index on the vector column using cosine distance:

```sql
-- Set work_mem for index build
SET maintenance_work_mem = '1GB';

-- Create HNSW Index with tuned graph parameters
CREATE INDEX IF NOT EXISTS idx_embeddings_hnsw_cosine
ON data_rag_embeddings USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 100);

-- Accelerate metadata filtering with a JSONB GIN index
CREATE INDEX IF NOT EXISTS idx_embeddings_metadata_gin
ON data_rag_embeddings USING gin (metadata_);
```

## 2. Query-Time Tuning with ef_search
Adjust the query-time candidate list size (`hnsw.ef_search`) based on search priority:

```sql
-- Default is 40. Increase for higher recall at minor latency cost:
SET hnsw.ef_search = 100;

-- Execute filtered nearest neighbor search
SELECT id, text, metadata_, 1 - (embedding <=> :query_vector) AS cosine_similarity
FROM data_rag_embeddings
WHERE metadata_->>'tenant_id' = :tenant_id
ORDER BY embedding <=> :query_vector
LIMIT 5;
```

## 3. Maintenance Runbook
Periodically run `VACUUM ANALYZE data_rag_embeddings;` to update planner statistics and optimize table page density.

## Done Means
The HNSW index and GIN metadata index are active, queries execute in sub-15ms on 100k+ vector rows, and `EXPLAIN ANALYZE` confirms an `Index Scan using idx_embeddings_hnsw_cosine`.
