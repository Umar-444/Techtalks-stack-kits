---
name: server-actions-mutation
description: Author type-safe Next.js Server Actions with Zod validation, revalidation, and error handling.
---

# Server Actions Mutation Skill

## Purpose
Provides standardized patterns for mutating server state without client-side API boilerplate.

## Standard Pattern
```typescript
'use server';

import { createClient } from '@/lib/supabase/server';
import { revalidatePath } from 'next/cache';
import { z } from 'zod';

const ItemSchema = z.object({
  title: z.string().trim().min(3).max(120),
});

export async function createItem(formData: FormData) {
  const parsed = ItemSchema.safeParse({
    title: formData.get('title'),
  });

  if (!parsed.success) {
    return { success: false, error: parsed.error.issues[0].message };
  }

  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();

  if (!user) {
    return { success: false, error: 'Unauthorized' };
  }

  const { error } = await supabase.from('items').insert({
    user_id: user.id,
    title: parsed.data.title,
  });

  if (error) {
    return { success: false, error: error.message };
  }

  revalidatePath('/');
  return { success: true };
}
```

## Done Means
Action parses inputs strictly via Zod, checks session credentials, mutates database, triggers `revalidatePath()`, and returns typed status.
