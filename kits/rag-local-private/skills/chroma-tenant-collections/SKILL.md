---
name: "chroma-tenant-collections"
description: "Manage local ChromaDB persistent collections, perform metadata filtering operations, backup SQLite databases, and vacuum vector indexes."
---

# Skill: ChromaDB Tenant Collections and Maintenance

Use this skill to manage, isolate, backup, and optimize local ChromaDB vector databases.

## 1. Multi-Tenant Collection Strategy
Depending on regulatory isolation requirements, choose between:
- **Partitioned Collection per Tenant:**
  Create dedicated collections for high-compliance tenants (`tenant_corp_01_knowledge`).
  ```python
  tenant_coll = chroma_client.get_or_create_collection(
      name=f"tenant_{tenant_id}",
      metadata={"hnsw:space": "cosine"}
  )
  ```
- **Shared Collection with Mandatory Metadata Filter:**
  Single collection with `$and` query filtering on `tenant_id`. Ideal for lower storage footprint when hosting hundreds of smaller tenants.

## 2. Advanced Metadata Filtering Syntax
ChromaDB supports nested boolean query operators:
```python
results = collection.query(
    query_embeddings=[query_vector],
    n_results=5,
    where={
        "$and": [
            {"tenant_id": {"$eq": "tenant-corp-01"}},
            {"classification": {"$in": ["PUBLIC", "INTERNAL", "CONFIDENTIAL"]}},
            {"department": {"$eq": "engineering"}}
        ]
    }
)
```

## 3. Database Backup & Disaster Recovery
ChromaDB persistent stores write metadata to an embedded SQLite database (`chroma.sqlite3`) and vector graph files (`.bin`).
To create a point-in-time backup:
```bash
# Safely snapshot the SQLite database using the backup API
sqlite3 ./data/chromadb/chroma.sqlite3 ".backup './backups/chroma_backup_$(date +%Y%m%d).sqlite3'"

# Copy vector index directory
cp -r ./data/chromadb/ ./backups/chroma_full_$(date +%Y%m%d)/
```

## 4. SQLite Vacuuming & Space Reclamation
After deleting obsolete documents or purging expired tenant indexes:
```bash
sqlite3 ./data/chromadb/chroma.sqlite3 "VACUUM;"
```
This reclaims unused disk pages and defragments the SQLite B-trees.
