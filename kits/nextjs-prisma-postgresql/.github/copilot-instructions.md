# GitHub Copilot Instructions for Next.js 15+ + Prisma ORM + PostgreSQL + Tailwind CSS
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Next.js 15 and App Router Architecture
# Next.js 15 and App Router Architecture

## 1. Server Components as Default
- Default all components to React Server Components (RSC) to minimize client bundle size.
- Use the `'use client'` directive exclusively when component state (`useState`), effects (`useEffect`), or browser DOM events are required.
- Fetch data directly inside Server Components using Prisma Client.

## 2. Directory Layout & Organization
- **App Routes**: `src/app/` (page routes, layout wrappers, route handlers).
- **Server Actions**: `src/lib/actions/` (domain mutation functions marked with `'use server'`).
- **Prisma Client**: `src/lib/prisma.ts` (global singleton instance).
- **Validation Schemas**: `src/lib/validations/` (Zod schemas reused between client and server).

## 3. Never-List
- Never instantiate new `PrismaClient()` inside route handlers or components; import the singleton.
- Never pass database connection strings or secrets to client components.
- Never execute database write operations inside GET route handlers or Server Component render loops.

## Prisma Schema and Migration Standards
# Prisma Schema and Migration Standards

## 1. Model Definitions & Relations
- Every model must define an `id` primary key (`@id @default(cuid())` or `@default(autoincrement())`).
- Include standard audit timestamps: `createdAt DateTime @default(now())` and `updatedAt DateTime @updatedAt`.
- Explicitly name foreign key relations and cascade delete rules where appropriate.

## 2. Index Optimization
- Add indexes on foreign keys, tenant IDs, and filtered query fields: `@@index([tenantId, status])`.
- Define composite unique constraints to enforce business invariants: `@@unique([tenantId, slug])`.

## 3. Migration Workflows
- Always generate migrations with descriptive names: `npx prisma migrate dev --name <description>`.
- In production, deploy migrations using `npx prisma migrate deploy`.

## Server Actions and Zod Validation
# Server Actions and Zod Validation

## 1. Action Structure
- Mark action files with `'use server'` at the top.
- Validate all incoming arguments against a typed Zod schema before accessing database.
- Return structured result objects: `{ success: true, data }` or `{ success: false, error }`.

## 2. Revalidation
- Use `revalidatePath('/dashboard')` or `revalidateTag('projects')` immediately following mutations.
- Wrap multi-table operations inside `prisma.$transaction`.

## Security and Multi-Tenant Authorization
# Security and Multi-Tenant Authorization

## 1. Tenant Scoping on Every Query
- Always include `tenantId` in Prisma `where` criteria:
  ```typescript
  const project = await prisma.project.findFirst({
    where: { id: projectId, tenantId: user.tenantId }
  });
  ```
- If the record is not found, return 404 or throw an authorization error.

## 2. Server Action Guardrails
- Authenticate the caller session inside every Server Action prior to execution.
- Sanitize user-provided rich text or HTML inputs to prevent XSS.

## Testing Verification and CI Standards
# Testing Verification and CI Standards

## 1. Test Suite Coverage
- Test Zod validation schemas against both valid and adversarial payloads.
- Test Server Actions with mock Prisma clients or test database containers.
- Assert that cross-tenant mutations are rejected.

## 2. CI Verification
- Every PR must pass `npm run build`, `npm test`, `gitleaks`, and `semgrep`.

