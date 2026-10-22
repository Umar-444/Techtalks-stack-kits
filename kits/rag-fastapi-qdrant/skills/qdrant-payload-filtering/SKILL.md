---
name: qdrant-payload-filtering
description: Configure and execute Qdrant payload schema indexing and multi-condition boolean filters for tenant isolation and attribute filtering.
---

# Qdrant Payload Filtering Skill: Multi-Tenant Isolation & Structured Search

## Objective
Enforce strict multi-tenant isolation and fast metadata filtering during vector search using Qdrant's native payload indexing engine.

## Payload Index Creation
Before querying large collections, create payload schema indexes on high-cardinality metadata keys:

```python
from qdrant_client import QdrantClient
from qdrant_client.http import models

client = QdrantClient(host="localhost", port=6333)

# 1. Create Keyword Index on tenant_id
client.create_payload_index(
    collection_name="documents",
    field_name="tenant_id",
    field_schema=models.PayloadSchemaType.KEYWORD
)

# 2. Create Keyword Index on category / department
client.create_payload_index(
    collection_name="documents",
    field_name="department",
    field_schema=models.PayloadSchemaType.KEYWORD
)

# 3. Create Integer/Range Index on created_timestamp
client.create_payload_index(
    collection_name="documents",
    field_name="created_timestamp",
    field_schema=models.PayloadSchemaType.INTEGER
)
```

## Filtered Query Execution
Execute vector similarity queries constrained by tenant boundaries:

```python
results = client.search(
    collection_name="documents",
    query_vector=query_dense_vector,
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="tenant_id",
                match=models.MatchValue(value="tenant_enterprise_01")
            ),
            models.FieldCondition(
                key="department",
                match=models.MatchValue(value="engineering")
            )
        ]
    ),
    limit=5,
    score_threshold=0.65
)
```

## Done Means
Queries execute with payload filters returning exclusively documents matching the specified `tenant_id`, while foreign tenant vectors are completely filtered out prior to nearest-neighbor graph traversal.
