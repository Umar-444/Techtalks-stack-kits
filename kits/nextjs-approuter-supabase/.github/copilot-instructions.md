# GitHub Copilot Instructions for Next.js 15+ + Supabase + shadcn/ui
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Server Actions & Zod Validation
# Server Actions & Zod Validation

1. **Mandatory Zod Parsing:**
   - Every Server Action must validate inputs with `schema.safeParse()`.
   - Never trust form data or client payloads without validation.

2. **Session Verification:**
   - Verify the caller's session via `supabase.auth.getUser()` before mutations.

## Supabase Row-Level Security (RLS)
# Supabase Row-Level Security (RLS)

1. **Enable RLS on All Tables:**
   - `ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY;`

2. **Policy Definition:**
   - Restrict updates to authenticated owners: `USING (auth.uid() = user_id)`.

## Next.js App Router & Caching
# Next.js App Router & Caching

1. **Server Components by Default:**
   - Keep components as Server Components unless interactivity (`useState`, `useEffect`) is needed.
   - Use `'use client'` only at the leaves of the component tree.

