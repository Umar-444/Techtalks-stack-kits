---
title: "PostgreSQL 16+ Database Conventions"
description: "UUID primary keys, JSONB indexing, strict foreign keys, and zero-downtime migrations."
globs: ["database/migrations/**/*.php", "app/Models/**/*.php"]
---

# 03 — PostgreSQL 16+ Database Conventions

1. **UUID Primary Keys:**
   - All database tables must use UUID primary keys (`$table->uuid('id')->primary()`).
   - Models must use the `HasUuids` trait.

2. **Foreign Key Integrity:**
   - Always specify explicit foreign key constraints with `cascadeOnDelete()` or `restrictOnDelete()`.
   - Never leave loose integer ID relationships without foreign key indices.

3. **JSONB Fields:**
   - Semi-structured data must be stored in `jsonb` columns.
   - Add GIN indices (`CREATE INDEX ... USING gin`) for fields queried by JSON keys.

4. **Rollback Safety:**
   - Every migration must have a tested `down()` method that restores previous schema state cleanly.
