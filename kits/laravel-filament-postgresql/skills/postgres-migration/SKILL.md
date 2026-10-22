---
name: postgres-migration
description: Create zero-downtime PostgreSQL migrations with native UUIDs, JSONB columns, and composite indexes.
---

# PostgreSQL Migration Skill

## Purpose
Enforces PostgreSQL 16+ production best practices for Laravel Eloquent migrations.

## Key Workflows
```bash
php artisan make:migration create_orders_table
```

## Guidelines
- Always use `$table->uuid('id')->primary()`.
- Add composite B-tree indexes for common filter combinations: `$table->index(['status', 'created_at'])`.
- Use JSONB with GIN indexes for unstructured payload storage.

## Done Means
Migrations run cleanly via `php artisan migrate`, roll back idempotently via `php artisan migrate:rollback`, and create all defined indexes.
