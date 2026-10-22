---
name: weaviate-hybrid-indexing
description: Configure Weaviate collections with hybrid BM25 + dense vector indexing and multi-tenant isolation.
---
# Weaviate Hybrid Indexing Skill

## 1. Schema Configuration with Multi-Tenancy
```python
import weaviate.classes.config as wvc

def initialize_collection(client):
    collection_name = "DocumentChunk"
    if not client.collections.exists(collection_name):
        client.collections.create(
            name=collection_name,
            vectorizer_config=wvc.Configure.Vectorizer.none(), # External/Pipeline embeddings
            multi_tenancy_config=wvc.Configure.multi_tenancy(enabled=True),
            properties=[
                wvc.Property(name="content", data_type=wvc.DataType.TEXT, index_searchable=True),
                wvc.Property(name="tenant_id", data_type=wvc.DataType.TEXT, index_filterable=True),
                wvc.Property(name="doc_id", data_type=wvc.DataType.TEXT, index_filterable=True),
                wvc.Property(name="created_at", data_type=wvc.DataType.DATE)
            ]
        )
```

## 2. Hybrid Query Execution
```python
def query_hybrid(collection, query_text: str, vector: list[float], tenant_id: str, alpha: float = 0.65):
    tenant_collection = collection.with_tenant(tenant_id)
    response = tenant_collection.query.hybrid(
        query=query_text,
        vector=vector,
        alpha=alpha,
        limit=5,
        return_metadata=wvc.MetadataQuery(score=True)
    )
    return response.objects
```

## 3. Done Means
- Collection defines searchable text properties for BM25 and filterable properties for metadata.
- Multi-tenancy is enforced on both creation and query phases.
- Hybrid search balances keyword and semantic match via `alpha=0.65`.
