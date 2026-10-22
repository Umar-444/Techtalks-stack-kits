---
name: first-feature
description: Ingest a knowledge document into PostgreSQL pgvector using LlamaIndex, index via HNSW, and execute a grounded semantic query.
---

# First Feature Skill: Document Ingestion & Semantic Query Engine

## Objective
Build and verify the canonical document ingestion and semantic query workflow using LlamaIndex and PostgreSQL pgvector.

## Implementation Workflow

### Step 1: Ingest Document into pgvector
Send a document payload to the ingestion endpoint:
```bash
curl -X POST http://localhost:8000/api/v1/documents/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "hr-policy-2026",
    "title": "Corporate Health & Wellness Policy",
    "text": "Full-time employees receive a comprehensive health stipend of up to $1,200 annually covering gym memberships, mental wellness apps, and physical therapy sessions.",
    "metadata": {
      "department": "human_resources",
      "tenant_id": "tenant-corp-1"
    }
  }'
```
*Expected Response*:
```json
{
  "document_id": "hr-policy-2026",
  "status": "indexed",
  "nodes_created": 1,
  "table_name": "data_rag_embeddings"
}
```

### Step 2: Query the Semantic Vector Store
Execute a natural language query with tenant isolation:
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How much wellness reimbursement is available for employees?",
    "similarity_top_k": 3,
    "score_threshold": 0.50,
    "filter": {
      "tenant_id": "tenant-corp-1"
    }
  }'
```
*Expected Response*:
```json
{
  "query": "How much wellness reimbursement is available for employees?",
  "results_count": 1,
  "sources": [
    {
      "node_id": "hr-policy-2026_0",
      "document_id": "hr-policy-2026",
      "score": 0.851,
      "text": "Full-time employees receive a comprehensive health stipend of up to $1,200 annually covering gym memberships, mental wellness apps, and physical therapy sessions.",
      "metadata": {
        "department": "human_resources",
        "tenant_id": "tenant-corp-1"
      }
    }
  ],
  "response": "Full-time employees receive an annual health and wellness stipend of up to $1,200."
}
```

## Done Means
The document is parsed into LlamaIndex TextNodes, vectorized into a 384-dimensional vector, persisted to PostgreSQL `data_rag_embeddings`, and retrieved via semantic similarity with matching score >= 0.70.
