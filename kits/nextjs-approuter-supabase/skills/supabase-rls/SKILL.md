---
name: "supabase-rls"
description: "Generate and test Supabase Row-Level Security (RLS) policies."
version: "1.0.0"
---

# Supabase RLS Policy Skill

1. Enable RLS on the table.
2. Create policy for SELECT: `CREATE POLICY select_own ON {table} FOR SELECT USING (auth.uid() = user_id);`.
3. Create policy for INSERT/UPDATE: `WITH CHECK (auth.uid() = user_id);`.
