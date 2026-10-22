---
name: sqlc-query-generation
description: Type-safe SQL query generation using sqlc with pgx/v5 for high-throughput parameterized PostgreSQL access.
---
# SQLC Query Generation Skill

## 1. sqlc Configuration
In `sqlc.yaml`:
```yaml
version: "2"
sql:
  - engine: "postgresql"
    schema: "db/schema.sql"
    queries: "db/queries/"
    gen:
      go:
        package: "db"
        out: "internal/db"
        sql_package: "pgx/v5"
        emit_json_tags: true
        emit_empty_slices: true
```

## 2. Parametric Safety Invariant
All dynamic values must use numbered parameters (`$1`, `$2`):
```sql
-- name: ListUsersByTenant :many
SELECT id, email, role, created_at
FROM users
WHERE tenant_id = $1 AND active = true
ORDER BY created_at DESC
LIMIT $2 OFFSET $3;
```

## 3. Execution
```bash
sqlc generate
```

## 4. Done Means
- Zero raw string concatenation in SQL queries.
- Resulting Go repository structs utilize `pgx/v5` connection pool.
