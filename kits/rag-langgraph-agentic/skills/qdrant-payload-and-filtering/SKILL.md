---
name: qdrant-payload-and-filtering
description: Managing Qdrant vector collections, Cosine distance indexing, payload filtering, and tenant security boundaries.
---
# Qdrant Payload Filtering & Indexing Skill

## 1. Create Collection with HNSW Parameters
```python
from qdrant_client import QdrantClient
from qdrant_client.http import models

def init_collection(client: QdrantClient, name: str = "agentic_rag"):
    client.recreate_collection(
        collection_name=name,
        vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
    )
```

## 2. Execute Filtered Vector Search
```python
def search_tenant_documents(client: QdrantClient, query_vector: list, tenant_id: str):
    return client.search(
        collection_name="agentic_rag",
        query_vector=query_vector,
        query_filter=models.Filter(
            must=[models.FieldCondition(key="tenant_id", match=models.MatchValue(value=tenant_id))]
        ),
        limit=5,
        score_threshold=0.60
    )
```
