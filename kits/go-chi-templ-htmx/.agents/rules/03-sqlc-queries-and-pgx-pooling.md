# 03 Sqlc Queries And Pgx Pooling

﻿---
id: "03-sqlc-queries-and-pgx-pooling"
title: "sqlc Type-Safe Queries & pgx Connection Pooling"
description: "SQL-first development standards using sqlc code generation, compile-checked query verification, and PostgreSQL connection pool management via pgxpool."
globs: ["**/*.sql", "**/*.go", "sqlc.yaml"]
alwaysApply: true
---

# 03 - sqlc Type-Safe Queries & pgx Connection Pooling

## 1. SQL-First Development with sqlc
- **Zero ORM Magic:** Avoid heavy ORMs (like GORM) that generate unpredictable, slow N+1 SQL queries via runtime reflection. Write clean, readable, standard PostgreSQL in `schema.sql` and `query.sql`.
- **Compile-Checked Queries:** `sqlc generate` parses DDL and raw SQL queries, verifies schema validity, checks column data types, and emits idiomatic, type-safe Go structs and repository methods.
- **Annotated Queries:** Every query in `query.sql` must have an explicit sqlc comment annotation declaring the method name and result cardinality:
  ```sql
  -- name: GetUserByID :one
  SELECT id, email, full_name, created_at
  FROM users
  WHERE id = $1;

  -- name: ListUsers :many
  SELECT id, email, full_name, created_at
  FROM users
  ORDER BY created_at DESC
  LIMIT $1 OFFSET $2;

  -- name: CreateUser :one
  INSERT INTO users (email, full_name)
  VALUES ($1, $2)
  RETURNING id, email, full_name, created_at;
  ```

## 2. PostgreSQL Connection Pooling with pgxpool
- Connect to PostgreSQL using `github.com/jackc/pgx/v5/pgxpool`:
  ```go
  config, err := pgxpool.ParseConfig(databaseURL)
  if err != nil {
      log.Fatalf("Unable to parse DB config: %v", err)
  }
  config.MaxConns = 25
  config.MinConns = 5
  config.MaxConnLifetime = 1 * time.Hour
  config.MaxConnIdleTime = 30 * time.Minute

  pool, err := pgxpool.NewWithConfig(ctx, config)
  if err != nil {
      log.Fatalf("Unable to create connection pool: %v", err)
  }
  defer pool.Close()
  ```
- Pass `pool` directly into `db.New(pool)` to instantiate the sqlc repository.

## 3. Transaction Safety
- Always wrap multi-statement write operations inside a transaction:
  ```go
  tx, err := pool.Begin(ctx)
  if err != nil {
      return err
  }
  defer tx.Rollback(ctx)

  qtx := queries.WithTx(tx)
  if err := qtx.CreateOrder(ctx, orderParams); err != nil {
      return err
  }
  if err := qtx.DeductInventory(ctx, itemParams); err != nil {
      return err
  }
  return tx.Commit(ctx)
  ```

