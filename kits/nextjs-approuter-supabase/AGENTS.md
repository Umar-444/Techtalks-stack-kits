# Next.js 15+ + Supabase + shadcn/ui — Agent Operating Rules (AGENTS.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Table of Contents
- [Server Actions & Zod Validation](#01-server-actions-zod)
- [Supabase Row-Level Security (RLS)](#02-supabase-rls)
- [Next.js App Router & Caching](#03-nextjs-app-router)

---

<a id="01-server-actions-zod"></a>
## Server Actions & Zod Validation

# Server Actions & Zod Validation

1. **Mandatory Zod Parsing:**
   - Every Server Action must validate inputs with `schema.safeParse()`.
   - Never trust form data or client payloads without validation.

2. **Session Verification:**
   - Verify the caller's session via `supabase.auth.getUser()` before mutations.

---

<a id="02-supabase-rls"></a>
## Supabase Row-Level Security (RLS)

# Supabase Row-Level Security (RLS)

1. **Enable RLS on All Tables:**
   - `ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY;`

2. **Policy Definition:**
   - Restrict updates to authenticated owners: `USING (auth.uid() = user_id)`.

---

<a id="03-nextjs-app-router"></a>
## Next.js App Router & Caching

# Next.js App Router & Caching

1. **Server Components by Default:**
   - Keep components as Server Components unless interactivity (`useState`, `useEffect`) is needed.
   - Use `'use client'` only at the leaves of the component tree.

---

