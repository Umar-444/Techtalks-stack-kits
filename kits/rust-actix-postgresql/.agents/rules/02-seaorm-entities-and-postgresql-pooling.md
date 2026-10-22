# 02 Seaorm Entities And Postgresql Pooling

﻿# SeaORM Entities and PostgreSQL Connection Pooling

1. **SeaORM Dynamic ORM Patterns**: Define domain models using SeaORM entity macros (`#[derive(Clone, Debug, PartialEq, DeriveEntityModel, Serialize, Deserialize)]`). Keep entity schema, columns, and relations tightly typed.
2. **PostgreSQL Connection Pool Hardening**: Configure `sea_orm::ConnectOptions` with strict limits: `max_connections(25)`, `min_connections(5)`, `connect_timeout(Duration::from_secs(5))`, `acquire_timeout(Duration::from_secs(3))`, and `idle_timeout(Duration::from_secs(600))`. Never use unbounded database pools in production.
3. **Strict Parameterized Queries**: All SeaORM query builders compile down to SQLx parameterized queries with bound placeholders (`$1`, `$2`). Raw string concatenation or dynamic query formatting is strictly forbidden.
4. **Isolated Migration System**: Maintain database migrations inside an isolated migration crate or module. Execute migrations automatically on server startup or via `sea-orm-cli migrate up` prior to traffic ingestion.
5. **Atomic Transaction Encapsulation**: Wrap multi-entity mutations inside SeaORM transactions (`db.transaction::<_, _, DbErr>(|txn| Box::pin(async move { ... }))`) to guarantee ACID consistency and rollback on failure.

