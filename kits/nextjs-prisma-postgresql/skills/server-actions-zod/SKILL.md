---
name: server-actions-zod
description: Scaffold secure Next.js 15 Server Actions with runtime Zod input validation and optimistic UI updates.
---

# Skill: Server Actions with Zod

## Workflow
1. Declare Zod schema in `src/lib/validations/`.
2. Define action function with `'use server'`.
3. Parse input: `const validated = schema.parse(input)`.
4. Mutate database and call `revalidatePath()`.

## Done Means
- Invalid inputs return typed error messages without mutating database.
