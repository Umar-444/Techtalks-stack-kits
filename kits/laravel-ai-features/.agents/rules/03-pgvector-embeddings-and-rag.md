# pgvector Embeddings and RAG Architecture

# pgvector Embeddings and RAG Architecture

## 1. Database Migrations with pgvector
- Always check and activate extension: `CREATE EXTENSION IF NOT EXISTS vector;`.
- Define vector columns explicitly: `$table->vector('embedding', 1536);`.
- Create HNSW index for sub-linear search:
  ```sql
  CREATE INDEX documents_embedding_hnsw_idx ON documents USING hnsw (embedding vector_cosine_ops);
  ```

## 2. Parameterized Cosine Queries
- Execute semantic search using the `<=>` cosine distance operator:
  ```php
  $query->orderByRaw('embedding <=> ?', [json_encode($embedding)])
        ->where('tenant_id', $tenantId)
        ->limit($limit);
  ```
