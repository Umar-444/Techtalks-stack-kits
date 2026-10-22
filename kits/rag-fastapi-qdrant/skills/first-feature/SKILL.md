---
name: first-feature
description: Ingest a knowledge document, generate dense vector embeddings, index into Qdrant, and perform grounded semantic search with score thresholding and citations.
---

# First Feature Skill: End-to-End Document Ingestion & Semantic Retrieval

## Objective
Build and verify the canonical document ingestion and semantic question-answering workflow in the FastAPI + Qdrant RAG service.

## Implementation Workflow

### Step 1: Ingest Document & Generate Vectors
Send a document payload to the ingestion endpoint:
```bash
curl -X POST http://localhost:8000/api/v1/documents/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "policy-kb-001",
    "title": "Corporate Remote Work & Hardware Policy",
    "text": "Employees may request up to $1,000 for home office equipment annually. Ergonomic chairs, external monitors, and mechanical keyboards are fully reimbursable upon submission of valid merchant receipts within 30 days of purchase.",
    "metadata": {
      "department": "operations",
      "tenant_id": "company-alpha"
    }
  }'
```
*Expected Response*:
```json
{
  "document_id": "policy-kb-001",
  "status": "indexed",
  "chunks_created": 1,
  "collection": "documents"
}
```

### Step 2: Execute Semantic Vector Search
Query the indexed collection with semantic search:
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How much can I expense for an ergonomic desk chair?",
    "top_k": 3,
    "score_threshold": 0.60,
    "filter": {
      "tenant_id": "company-alpha"
    }
  }'
```
*Expected Response*:
```json
{
  "query": "How much can I expense for an ergonomic desk chair?",
  "results_count": 1,
  "sources": [
    {
      "document_id": "policy-kb-001",
      "chunk_index": 0,
      "score": 0.842,
      "text": "Employees may request up to $1,000 for home office equipment annually. Ergonomic chairs, external monitors, and mechanical keyboards are fully reimbursable upon submission of valid merchant receipts within 30 days of purchase.",
      "metadata": {
        "department": "operations",
        "tenant_id": "company-alpha"
      }
    }
  ],
  "assembled_context": "[Source 1] (Score: 0.84, doc_id: policy-kb-001): Employees may request up to $1,000..."
}
```

## Done Means
The document is chunked, converted to a 384-dimensional dense vector, upserted to Qdrant without error, and a semantic query returns the matching chunk with a cosine similarity score >= 0.70 and full provenance metadata.
