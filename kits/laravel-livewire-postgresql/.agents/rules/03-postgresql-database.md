# 03 Postgresql Database

# Rule 3: PostgreSQL 16+ ORM, UUIDs & Query Performance

## Context & Principles
- All database tables must utilize native PostgreSQL UUID primary keys to prevent ID enumeration.
- Eliminate N+1 query regressions during component re-renders.

## Standards
1. **UUID Primary Keys**: Every Eloquent model must use `Illuminate\Database\Eloquent\Concerns\HasUuids`.
2. **Eager Loading**: Always eager load relationships in the component `render()` method:
   ```php
   Task::query()->with(['user'])->latest()->paginate(15);
   ```
3. **Composite Indexes**: Declare explicit indexes in migrations on filtered and sorted column tuples (`$table->index(['status', 'created_at'])`).
4. **Atomic Mutations**: Wrap multi-model operations inside `DB::transaction()` to ensure relational consistency.

