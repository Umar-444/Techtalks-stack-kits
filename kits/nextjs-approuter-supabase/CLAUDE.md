# Next.js 15+ + Supabase + shadcn/ui — Claude Code Guidelines (CLAUDE.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Quick Reference & Non-Negotiable Standards
### Server Actions & Zod Validation
> Safe mutation patterns, error handling, and type safety in Next.js 15.

# Server Actions & Zod Validation

1. **Mandatory Zod Parsing:**
   - Every Server Action must validate inputs with `schema.safeParse()`.
   - Never trust form data or client payloads without validation.

2. **Session Verification:**
   - Verify the caller's session via `supabase.auth.getUser()` before mutations.

### Supabase Row-Level Security (RLS)
> Writing watertight PostgreSQL RLS policies in Supabase.

# Supabase Row-Level Security (RLS)

1. **Enable RLS on All Tables:**
   - `ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY;`

2. **Policy Definition:**
   - Restrict updates to authenticated owners: `USING (auth.uid() = user_id)`.

### Next.js App Router & Caching
> React Server Components, revalidation, and streaming.

# Next.js App Router & Caching

1. **Server Components by Default:**
   - Keep components as Server Components unless interactivity (`useState`, `useEffect`) is needed.
   - Use `'use client'` only at the leaves of the component tree.

