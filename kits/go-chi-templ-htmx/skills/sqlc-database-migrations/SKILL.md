---
name: "sqlc-database-migrations"
description: "Maintain PostgreSQL schema definitions, manage sqlc codegen configuration, tune pgxpool parameters, and enforce strict compile-checked queries."
---

# Skill: sqlc Database Migrations & Connection Pooling

Use this skill for schema evolution, sqlc configuration, and PostgreSQL connection pool tuning.

## 1. sqlc Configuration (`sqlc.yaml`)
Ensure `sqlc.yaml` uses the modern v2 specification:
```yaml
version: "2"
sql:
  - engine: "postgresql"
    schema: "schema.sql"
    queries: "query.sql"
    gen:
      go:
        package: "db"
        out: "internal/db"
        sql_package: "pgx/v5"
        emit_json_tags: true
        emit_prepared_queries: false
        emit_interface: true
        emit_exact_table_names: false
```

## 2. PostgreSQL Connection Pool Sizing
In `main.go`, configure `pgxpool` based on production container limits:
```go
config, err := pgxpool.ParseConfig(os.Getenv("DATABASE_URL"))
if err != nil {
    log.Fatalf("Invalid database connection string: %v", err)
}

// Bounded connection limits to prevent exhaustion
config.MaxConns = 20
config.MinConns = 4
config.MaxConnIdleTime = 15 * time.Minute
config.HealthCheckPeriod = 1 * time.Minute

pool, err := pgxpool.NewWithConfig(context.Background(), config)
if err != nil {
    log.Fatalf("Failed to initialize database pool: %v", err)
}
defer pool.Close()
```

## 3. Mocking Queries in Unit Tests
Because `emit_interface: true` is configured in `sqlc.yaml`, `sqlc` generates a `Querier` interface:
```go
type Querier interface {
    CreateUser(ctx context.Context, arg CreateUserParams) (User, error)
    GetUserByID(ctx context.Context, id int64) (User, error)
    ListUsers(ctx context.Context, arg ListUsersParams) ([]User, error)
}
```
Inject `db.Querier` into handlers, enabling simple in-memory mock implementations during unit tests without requiring a running PostgreSQL database.
