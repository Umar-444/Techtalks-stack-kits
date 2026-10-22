---
name: "first-feature"
description: "Ingest a confidential document into local ChromaDB with chunking, assign Saudi PDPL classification, and run a grounded privacy query."
---

# Skill: First Feature - Ingest and Private Semantic Query

Use this skill to implement the complete end-to-end flow: ingesting a proprietary internal policy document into ChromaDB, chunking with metadata, and querying the local model.

## Step 1: Ingest Document via API
Send an ingestion request with explicit tenant isolation and Saudi PDPL classification:
```bash
curl -X POST http://localhost:8000/api/v1/documents/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "hr-policy-2026-v1",
    "title": "Gulf Enterprise Remote Work & IP Policy",
    "tenant_id": "tenant-corp-01",
    "classification": "CONFIDENTIAL",
    "text": "All enterprise intellectual property developed by remote engineering teams across Riyadh and Dubai remains the sole property of Gulf Holdings. Remote staff must connect via hardware-enforced WireGuard VPN. Cloud AI services without on-prem airgap guarantees are strictly prohibited under NCA ECC regulations.",
    "chunk_size": 256,
    "chunk_overlap": 32
  }'
```

Expected response:
```json
{
  "document_id": "hr-policy-2026-v1",
  "chunks_created": 1,
  "collection": "private_knowledge",
  "status": "ingested",
  "airgap_safe": true
}
```

## Step 2: Query Knowledge Base with Tenant Filter
Execute a grounded semantic query passing the tenant filter and security clearance:
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the security requirements for remote engineering teams?",
    "tenant_id": "tenant-corp-01",
    "user_classification": "CONFIDENTIAL",
    "top_k": 3
  }'
```

Expected response:
```json
{
  "query": "What are the security requirements for remote engineering teams?",
  "answer": "Remote engineering staff must connect via hardware-enforced WireGuard VPN. In addition, cloud AI services without on-prem airgap guarantees are strictly prohibited under NCA ECC regulations.",
  "sources": [
    {
      "document_id": "hr-policy-2026-v1",
      "chunk_index": 0,
      "classification": "CONFIDENTIAL",
      "similarity_score": 0.892
    }
  ],
  "airgap_safe": true,
  "privacy_verified": true
}
```

## Step 3: Verify Cross-Tenant Denial
Attempt to query the same content from a different tenant (`tenant-corp-02`):
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the security requirements for remote engineering teams?",
    "tenant_id": "tenant-corp-02",
    "user_classification": "CONFIDENTIAL",
    "top_k": 3
  }'
```
ChromaDB filters out non-matching tenant chunks at the index level, returning zero sources and an ungrounded denial response.
