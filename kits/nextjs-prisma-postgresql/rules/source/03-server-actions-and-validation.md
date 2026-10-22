---
id: 03-server-actions-and-validation
title: Server Actions and Zod Validation
description: Safe data mutation patterns, input validation, and optimistic state.
globs: ["src/lib/actions/**/*.ts", "src/lib/validations/**/*.ts"]
alwaysApply: true
---

# Server Actions and Zod Validation

## 1. Action Structure
- Mark action files with `'use server'` at the top.
- Validate all incoming arguments against a typed Zod schema before accessing database.
- Return structured result objects: `{ success: true, data }` or `{ success: false, error }`.

## 2. Revalidation
- Use `revalidatePath('/dashboard')` or `revalidateTag('projects')` immediately following mutations.
- Wrap multi-table operations inside `prisma.$transaction`.
