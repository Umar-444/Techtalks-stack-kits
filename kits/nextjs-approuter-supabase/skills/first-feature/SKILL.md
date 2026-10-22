---
name: first-feature
description: Build the canonical first feature: Task/Note management module with Server Actions, Zod validation, and Supabase RLS.
---

# First Feature Skill: Task Management Module with RLS

## Objective
Construct an end-to-end multi-tenant module adhering to the 18-checkpoint standard:
1. Supabase PostgreSQL table with `uuid` primary key and RLS policies.
2. Zod validation schema for form inputs.
3. Server Actions handling create, toggle, and delete mutations.
4. Server Component dashboard displaying live user-scoped items.
5. Automated test verifying action execution and error boundaries.

## Implementation Steps
1. Apply SQL migration enabling RLS:
   ```sql
   ALTER TABLE items ENABLE ROW LEVEL SECURITY;
   CREATE POLICY "Users can only access own items" ON items
     FOR ALL USING (auth.uid() = user_id);
   ```
2. Define Zod schema in `src/app/actions.ts`.
3. Create Server Action `createItem(formData: FormData)`.
4. Render in `src/app/page.tsx` with optimistic UI and pending states.

## Done Means
A user logs in, creates a new item via Server Action, item saves to Supabase with RLS verification, and other users cannot access the created record.
