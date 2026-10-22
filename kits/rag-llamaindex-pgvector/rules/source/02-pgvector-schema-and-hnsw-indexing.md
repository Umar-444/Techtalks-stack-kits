---
id: 02-pgvector-schema-and-hnsw-indexing
title: PostgreSQL 16+ pgvector Schema & HNSW Indexing
globs: "*"
alwaysApply: true
---
# Rule 2: PostgreSQL 16+ pgvector Schema & HNSW Indexing

## Context & Principles
- Store dense high-dimensional vectors in PostgreSQL using the `pgvector` extension and native `vector` data types.
- Build Hierarchical Navigable Small World (HNSW) indexes (`vector_cosine_ops`) rather than legacy IVFFlat indexes to achieve high recall without requiring index rebuilds.
- Configure connection pooling via SQLAlchemy / asyncpg / psycopg3 to reuse connections across concurrent API requests.

## Standards
1. **Extension & Index Provisioning**:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   
   CREATE TABLE IF NOT EXISTS data_rag_embeddings (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       text TEXT NOT NULL,
       metadata_ JSONB DEFAULT '{}',
       embedding vector(384)
   );

   CREATE INDEX IF NOT EXISTS idx_hnsw_embedding
   ON data_rag_embeddings USING hnsw (embedding vector_cosine_ops)
   WITH (m = 16, ef_construction = 100);
   ```
2. **Metadata GIN Indexing**: Create GIN indexes on the `metadata_` JSONB column (`CREATE INDEX idx_metadata ON data_rag_embeddings USING gin (metadata_);`) to accelerate hybrid metadata filters.
3. **Exact Dimensions**: Vector column dimensions must strictly match the embedding model output dimensionality (`384` for BGE-small).
4. **Maintenance**: Regularly schedule `VACUUM ANALYZE data_rag_embeddings;` to keep vector page layout and index statistics optimal.
