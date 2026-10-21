# Agent Build Steps — Next.js 15+ + Supabase + shadcn/ui

### Step 1: Environment Setup
Configure `.env.local` with Supabase project credentials.
*Verification:* `npm run dev`

### Step 2: Supabase SSR Client Initialization
Set up server and client Supabase utilities using `@supabase/ssr`.
*Verification:* `npx tsx scripts/test-supabase.ts`

### Step 3: Server Action & Zod Validation
Implement mutations using Server Actions and enforce Zod payload validation.
*Verification:* `npm run test`

### Step 4: Row-Level Security Audit
Verify all tables reject unauthorized read and write operations.
*Verification:* `npx supabase test db`
