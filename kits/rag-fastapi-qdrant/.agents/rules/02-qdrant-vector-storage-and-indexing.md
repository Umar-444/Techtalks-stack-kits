# 02 Qdrant Vector Storage And Indexing

# Rule 2: Qdrant Vector Storage, Collections & HNSW Indexing

## Context & Principles
- Qdrant manages dense high-dimensional vectors with customizable distance metrics and Hierarchical Navigable Small World (HNSW) graph indexing.
- Use Cosine distance (`models.Distance.COSINE`) for normalized embeddings (such as BGE or text-embedding-3-small).
- Optimize HNSW index parameters (`m=16`, `ef_construct=100`) to balance memory consumption, build times, and retrieval precision.

## Standards
1. **Idempotent Collection Provisioning**:
   ```python
   if not client.collection_exists(collection_name):
       client.create_collection(
           collection_name=collection_name,
           vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
           hnsw_config=models.HnswConfigDiff(m=16, ef_construct=100)
       )
   ```
2. **Payload Indexing**: Always define payload schema indexes for fields used in filter queries (e.g. `tenant_id`, `category`, `document_id`) to ensure sub-millisecond filtering before graph traversal.
3. **Point IDs**: Use valid UUIDv4 strings or integer IDs. Generate deterministic UUIDv5 hashes from `(document_id, chunk_index)` to support idempotent document re-ingestion.
4. **Batch Upserts**: Group vector additions into batches of 100-256 points to minimize network I/O round trips and optimize disk flushing.

