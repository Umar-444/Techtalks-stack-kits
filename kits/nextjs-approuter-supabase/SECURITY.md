# SECURITY.md — Next.js 15 & Supabase Security Standards

1. **Mandatory Row-Level Security (RLS):**
   Every PostgreSQL table in Supabase must execute `ALTER TABLE ... ENABLE ROW LEVEL SECURITY;`.

2. **Server Action Validation:**
   Every Server Action must validate inputs via a Zod schema before executing database queries.

3. **Environment Variable Separation:**
   Only public keys can use `NEXT_PUBLIC_`. Secret keys (`SUPABASE_SERVICE_ROLE_KEY`) must never be imported into client components.
