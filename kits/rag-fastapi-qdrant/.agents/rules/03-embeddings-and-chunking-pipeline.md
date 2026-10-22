# Rule 3: Text Chunking, Token Budgets & FastEmbed Generation

## Context & Principles
- RAG accuracy is fundamentally bounded by the quality and granularity of document chunking.
- Implement recursive character or markdown splitting with a target chunk size of 512 tokens and an overlap of 64 tokens (12.5%) to preserve cross-boundary semantics.
- Prefer local ONNX-based dense embeddings (e.g. `BAAI/bge-small-en-v1.5` via FastEmbed) for zero-latency, zero-cost, and fully offline vectorization.

## Standards
1. **Sliding Window Chunking**:
   ```python
   def chunk_text(text: str, chunk_size: int = 512, overlap: int = 64) -> list[str]:
       chunks = []
       start = 0
       while start < len(text):
           end = min(start + chunk_size, len(text))
           chunks.append(text[start:end])
           if end == len(text):
               break
           start += chunk_size - overlap
       return chunks
   ```
2. **Deterministic Dimensions**: Strictly enforce matching vector dimensionality between the embedding model output and the Qdrant collection configuration (`size=384` for BGE-small).
3. **Payload Metadata Enrichment**: Attach essential provenance metadata to every chunk payload: `{"document_id": doc_id, "chunk_index": idx, "text": chunk, "char_start": start, "char_end": end, "created_at": iso_timestamp}`.
4. **Zero Empty Chunks**: Filter out whitespace-only or empty strings prior to embedding generation to avoid degenerate null vectors.

