# 03 Supabase Rls And Database

# Rule 3: Supabase PostgreSQL 16+ & Row Level Security (RLS)

## Context & Principles
- Maintain zero-trust database security: every table in PostgreSQL must have Row Level Security explicitly enabled (`ALTER TABLE ... ENABLE ROW LEVEL SECURITY`).
- Never rely solely on application-layer filters for multi-tenant isolation; database policies must reject unauthorized access at the query engine level.

## Standards
1. **Mandatory RLS Policies**: Every table must declare explicit policies for `SELECT`, `INSERT`, `UPDATE`, and `DELETE` referencing `auth.uid() = user_id`.
2. **Service Role Isolation**: Never expose `SUPABASE_SERVICE_ROLE_KEY` to client-side bundles or `NEXT_PUBLIC_` environment variables.
3. **UUID Keys**: Use native PostgreSQL `uuid` or `gen_random_uuid()` for all primary keys.
4. **Index Foreign Keys**: Create explicit B-tree indexes on `user_id` and timestamp columns to optimize RLS evaluation speeds.

