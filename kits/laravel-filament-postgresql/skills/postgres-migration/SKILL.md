---
name: "postgres-migration"
description: "Write zero-downtime PostgreSQL migrations with strict foreign key constraints."
version: "1.0.0"
author: "TechTalks Stack Kits"
---

# PostgreSQL Migration Skill

Use this skill whenever modifying PostgreSQL database schemas.

## Workflow

1. **UUID Primary Keys:**
   ```php
   $table->uuid('id')->primary();
   ```

2. **Foreign Key Constraints:**
   ```php
   $table->foreignUuid('team_id')
       ->constrained('teams')
       ->cascadeOnDelete();
   ```

3. **JSONB Indexing:**
   ```php
   $table->jsonb('metadata')->default('{}');
   ```

4. **Rollback Safety:**
   Always implement the `down()` method so `php artisan migrate:rollback` returns cleanly to the prior schema state without leftover artifacts.
