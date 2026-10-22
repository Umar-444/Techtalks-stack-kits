---
name: chunking-and-embedding
description: Author optimized sliding-window document chunking and local dense embedding generation pipelines with FastEmbed.
---

# Chunking & Embedding Skill: High-Throughput Vector Generation

## Objective
Implement sliding-window text chunking with deterministic overlap and generate 384-dimensional dense vectors using FastEmbed without external API dependencies.

## Implementation Workflow

### 1. Sliding Window Token & Character Splitter
```python
def chunk_document(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50
) -> list[dict]:
    """Splits raw text into overlapping windows preserving offsets."""
    chunks = []
    start = 0
    idx = 0
    text_len = len(text)
    
    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunk_str = text[start:end].strip()
        if chunk_str:
            chunks.append({
                "chunk_index": idx,
                "text": chunk_str,
                "start_char": start,
                "end_char": end
            })
            idx += 1
        if end == text_len:
            break
        start += chunk_size - chunk_overlap
    return chunks
```

### 2. FastEmbed Local Vector Pipeline
```python
from fastembed import TextEmbedding

# Load BGE-small-en model (384-dimensional dense vectors)
embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")

def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Generates normalized vector embeddings locally via ONNX Runtime."""
    embeddings = list(embedding_model.embed(texts))
    return [e.tolist() for e in embeddings]
```

## Done Means
A 2,000-character input document is partitioned into chunks with 50-character overlaps, and vector generation produces 384-dimensional floating point lists with unit-normalized L2 norms.
