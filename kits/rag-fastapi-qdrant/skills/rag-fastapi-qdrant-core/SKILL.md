---
name: rag-fastapi-qdrant-core
description: Core operational workflows, collection snapshots, health checks, and query optimization for FastAPI + Qdrant.
---

# RAG FastAPI + Qdrant Core Operations Skill

## Common Operational Tasks

### 1. Check Qdrant Cluster & Collection Telemetry
```bash
# Cluster telemetry
curl -s http://localhost:6333/telemetry | jq .result.collections

# Get 'documents' collection detailed information
curl -s http://localhost:6333/collections/documents | jq .result
```

### 2. Snapshot & Backup Vector Collections
```bash
# Create collection snapshot
curl -X POST http://localhost:6333/collections/documents/snapshots

# List all available snapshots
curl -s http://localhost:6333/collections/documents/snapshots | jq .result
```

### 3. Clear or Recreate Collection
```python
from qdrant_client import QdrantClient
from qdrant_client.http import models

client = QdrantClient(host="localhost", port=6333)

def reset_collection(collection_name: str = "documents"):
    if client.collection_exists(collection_name):
        client.delete_collection(collection_name)
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
        hnsw_config=models.HnswConfigDiff(m=16, ef_construct=100)
    )
    print(f"Collection '{collection_name}' successfully provisioned.")
```

## Done Means
Operators can monitor collection health metrics, create snapshots for disaster recovery, and safely re-provision collections without service outages.
