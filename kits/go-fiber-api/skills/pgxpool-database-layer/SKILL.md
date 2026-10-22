---
name: pgxpool-database-layer
description: Configure high-throughput PostgreSQL connection pooling in Fiber using jackc/pgx/v5.
---
# PGXPOOL Database Layer Skill

## 1. Pool Initialization
```go
import "github.com/jackc/pgx/v5/pgxpool"

func NewPGXPool(ctx context.Context, dsn string) (*pgxpool.Pool, error) {
    config, err := pgxpool.ParseConfig(dsn)
    if err != nil {
        return nil, err
    }
    config.MaxConns = 30
    config.MinConns = 5
    config.MaxConnIdleTime = 15 * time.Minute
    
    return pgxpool.NewWithConfig(ctx, config)
}
```

## 2. Parameterized Query Execution
```go
func (r *Repo) GetRecord(ctx context.Context, id int64) (*Record, error) {
    var rec Record
    err := r.pool.QueryRow(ctx, 
        "SELECT id, tenant_id, data, created_at FROM records WHERE id = $1", 
        id,
    ).Scan(&rec.ID, &rec.TenantID, &rec.Data, &rec.CreatedAt)
    return &rec, err
}
```

## 3. Done Means
- Queries use parameterized `$1`, `$2` positional arguments.
- Context deadlines are enforced on every database query.
