---
title: "Supabase Row-Level Security (RLS)"
description: "Writing watertight PostgreSQL RLS policies in Supabase."
globs: ["supabase/migrations/**/*.sql"]
---

# Supabase Row-Level Security (RLS)

1. **Enable RLS on All Tables:**
   - `ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY;`

2. **Policy Definition:**
   - Restrict updates to authenticated owners: `USING (auth.uid() = user_id)`.
