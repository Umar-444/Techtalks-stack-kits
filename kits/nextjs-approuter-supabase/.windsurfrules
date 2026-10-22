# Next.js 15+ + Supabase + shadcn/ui - Agent Architecture & Rules

This project adheres to the TechTalks production standards for Next.js 15 App Router, React 19, Supabase RLS, and TypeScript.

# Rule 1: Next.js 15 App Router & React 19 Architecture

## Context & Principles
- All components in the `app/` directory are React Server Components (RSC) by default.
- Minimize client-side bundle size: only add `'use client'` at the leaves of the component tree for interactive hooks (`useState`, `useEffect`, `useFormStatus`).
- Keep data fetching on the server using direct Supabase server client calls inside Server Components.

## Standards
1. **Directory Structure**: Group route segments into `src/app/(auth)/`, `src/app/(dashboard)/`, and shared components into `src/components/`.
2. **Streaming & Suspense**: Wrap asynchronous data-fetching Server Components in `<Suspense fallback={<Skeleton />}>` to enable incremental page streaming.
3. **Metadata & SEO**: Export static or dynamic `generateMetadata()` from `page.tsx` or `layout.tsx` for search engine indexing and Open Graph cards.
4. **Layout Hygiene**: Avoid fetching dynamic user data in global root layouts unless strictly necessary to preserve static route caching.

# Rule 2: Server Actions, Zod Validation & Optimistic Updates

## Context & Principles
- Implement all data mutations via Next.js Server Actions marked with `'use server'` at file or function level.
- Never trust client-supplied form data: validate every input payload using strict Zod schemas before executing database queries.

## Standards
1. **Schema Validation**: Define Zod schemas with explicit types, constraints, and error messages:
   ```typescript
   export const CreateItemSchema = z.object({
     title: z.string().trim().min(3).max(100),
     description: z.string().trim().max(500).optional(),
   });
   ```
2. **Revalidation**: Always call `revalidatePath()` or `revalidateTag()` after successful mutations to purge stale cached data.
3. **Error Handling**: Return structured action results `{ success: boolean, data?: T, error?: string }` instead of throwing unhandled exceptions.
4. **CSRF Protection**: Next.js automatically validates the `Origin` header on Server Actions; never disable origin verification.

# Rule 3: Supabase PostgreSQL 16+ & Row Level Security (RLS)

## Context & Principles
- Maintain zero-trust database security: every table in PostgreSQL must have Row Level Security explicitly enabled (`ALTER TABLE ... ENABLE ROW LEVEL SECURITY`).
- Never rely solely on application-layer filters for multi-tenant isolation; database policies must reject unauthorized access at the query engine level.

## Standards
1. **Mandatory RLS Policies**: Every table must declare explicit policies for `SELECT`, `INSERT`, `UPDATE`, and `DELETE` referencing `auth.uid() = user_id`.
2. **Service Role Isolation**: Never expose `SUPABASE_SERVICE_ROLE_KEY` to client-side bundles or `NEXT_PUBLIC_` environment variables.
3. **UUID Keys**: Use native PostgreSQL `uuid` or `gen_random_uuid()` for all primary keys.
4. **Index Foreign Keys**: Create explicit B-tree indexes on `user_id` and timestamp columns to optimize RLS evaluation speeds.

# Rule 4: Supabase SSR Authentication & Cookie Session Security

## Context & Principles
- Manage authentication sessions securely across Server Components, Server Actions, and Route Handlers using `@supabase/ssr`.
- Rotate and refresh auth tokens transparently via Next.js Middleware.

## Standards
1. **SSR Client Factory**: Instantiate Supabase clients via dedicated factory functions (`createClient()` in `src/lib/supabase/server.ts` and `client.ts`).
2. **Middleware Session Refresh**: Run `updateSession()` in `src/middleware.ts` on every request to refresh expired tokens and persist cookies.
3. **Cookie Attributes**: Ensure auth cookies use `httpOnly: true`, `secure: process.env.NODE_ENV === 'production'`, and `sameSite: 'lax'`.
4. **PKCE Flow**: Enforce Proof Key for Code Exchange (PKCE) for all OAuth and email authentication handshakes.

# Rule 5: Testing, Type Safety & Strict Verification

## Context & Principles
- Enforce strict TypeScript compilation (`"strict": true`, zero `any` types).
- Validate Server Actions, Zod schemas, and Supabase client integration with automated unit and integration tests.

## Standards
1. **Schema Unit Tests**: Test Zod schemas against valid payloads, boundary limits, and malicious script inputs.
2. **Server Action Tests**: Assert that unauthenticated callers receive unauthorized errors before database queries execute.
3. **RLS Assertions**: Verify through integration tests that User A cannot read, update, or delete records owned by User B.
4. **Build Gate**: Ensure `next build` and `tsc --noEmit` pass with zero warnings in CI pipelines.
