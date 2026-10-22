---
name: first-feature
description: Build the canonical Project & Task management module with Server Actions, Zod schema validation, and Prisma relations.
---

# Skill: First Feature (Project & Task Management)

## 1. Schema Definition
Define `Project` and `Task` models in `prisma/schema.prisma` with 1:many relation, status enums, and tenant ID index.

## 2. Server Action Implementation
Create `src/lib/actions.ts`:
- `createProject(data: CreateProjectInput)`: Validate with Zod, persist via `prisma.project.create()`, revalidate path.

## 3. Server Component Page
Render project grid in `src/app/page.tsx` directly fetching data via `prisma.project.findMany()`.

## 4. Done Means
- Project creation form validates required title and description.
- Submitting form persists record to PostgreSQL.
- Vitest tests pass with code 0.
