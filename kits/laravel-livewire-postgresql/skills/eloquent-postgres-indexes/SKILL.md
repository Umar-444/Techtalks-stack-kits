---
name: eloquent-postgres-indexes
description: Optimize PostgreSQL 16+ schemas for Livewire apps using composite B-tree indexes, UUIDs, and JSONB queries.
---

# Eloquent PostgreSQL Indexes Skill

## Purpose
Configures database schema and query patterns for high-frequency Livewire reactive requests.

## Standards
- Always index columns used in Livewire filter queries:
  ```php
  $table->index(['user_id', 'is_completed', 'created_at']);
  ```
- Use native JSONB columns with GIN indexes for dynamic metadata.
- Pre-filter active query scopes to avoid full table scans.

## Done Means
Database queries executed by Livewire components resolve via index scans in under 5ms without table sequential scans.
