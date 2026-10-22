---
name: rag-llamaindex-pgvector-core
description: Core operational workflows, pgvector table migrations, vector vacuuming, and health checks for LlamaIndex + PostgreSQL.
---

# LlamaIndex + PostgreSQL pgvector Core Operations Skill

## Common Operational Tasks

### 1. Check PostgreSQL pgvector Telemetry
```bash
# Query total vectors count and index status
docker compose exec db psql -U postgres -d rag_db -c "
  SELECT relname, reltuples, pg_size_pretty(pg_total_relation_size(c.oid))
  FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
  WHERE relname IN ('data_rag_embeddings', 'idx_embeddings_hnsw_cosine');
"
```

### 2. Table Maintenance & Index Re-indexing
```sql
-- Vacuum dead tuples and update planner statistics
VACUUM (VERBOSE, ANALYZE) data_rag_embeddings;

-- Reindex concurrently if memory footprint expands
REINDEX INDEX CONCURRENTLY idx_embeddings_hnsw_cosine;
```

### 3. Reset Vector Table Safely
```python
import psycopg2

def reset_vector_table(conn_string: str, table_name: str = "data_rag_embeddings"):
    with psycopg2.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute(f"TRUNCATE TABLE {table_name};")
            cur.execute(f"VACUUM ANALYZE {table_name};")
        conn.commit()
    print(f"Table '{table_name}' truncated and vacuumed successfully.")
```

## Done Means
Database administrators and agents can monitor pgvector table size, maintain HNSW indexing efficiency, and safely clean or reset vector collections without breaking API availability.
