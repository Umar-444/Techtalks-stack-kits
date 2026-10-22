---
name: supabase-rls-policies
description: Write bulletproof PostgreSQL Row Level Security (RLS) policies for Supabase multi-tenant isolation.
---

# Supabase RLS Policies Skill

## Purpose
Enforces database-level access control on all PostgreSQL tables.

## Standard RLS Pattern
```sql
-- Enable RLS
ALTER TABLE public.items ENABLE ROW LEVEL SECURITY;

-- Select Policy
CREATE POLICY "Users can view own items"
ON public.items FOR SELECT
USING (auth.uid() = user_id);

-- Insert Policy
CREATE POLICY "Users can insert own items"
ON public.items FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Update Policy
CREATE POLICY "Users can update own items"
ON public.items FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- Delete Policy
CREATE POLICY "Users can delete own items"
ON public.items FOR DELETE
USING (auth.uid() = user_id);
```

## Done Means
All CRUD operations execute through Supabase client with RLS active, and direct queries for cross-tenant IDs return empty sets or fail.
