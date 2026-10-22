# 03 Pgxpool Connection And Database Lifecycle

# PostgreSQL Connection and PGXPOOL Lifecycle

1. **PGX Connection Pooling**: Connect to PostgreSQL 16+ using `jackc/pgx/v5/pgxpool`. Configure pool bounds (`MaxConns=30`, `MinConns=5`, `MaxConnIdleTime=15m`) matching container concurrency limits.
2. **Strict Query Parameterization**: Every SQL statement must utilize positional placeholders (`$1`, `$2`). Dynamic query construction via string formatting is strictly prohibited.
3. **Resource Leak Prevention**: Every acquired connection or transaction (`pgxpool.Pool.Acquire` or `pool.Begin`) must be guarded by a deferred `conn.Release()` or `tx.Rollback(ctx)`.
4. **Context Deadlines**: Bind all database queries to request contexts (`c.Context()`) with a 5-second timeout to terminate stalled database calls immediately.
5. **Repository Separation**: Separate SQL data access logic into repository structs; never invoke database queries directly inside Fiber controller functions.

