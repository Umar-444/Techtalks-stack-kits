'use server';

import { createClient } from '@/lib/supabase/server';
import { revalidatePath } from 'next/cache';
import { z } from 'zod';

const ItemSchema = z.object({
  title: z.string().trim().min(3, 'Title must be at least 3 characters').max(120),
  description: z.string().trim().max(500).optional(),
});

export async function createItem(formData: FormData) {
  const parsed = ItemSchema.safeParse({
    title: formData.get('title'),
    description: formData.get('description'),
  });

  if (!parsed.success) {
    return { success: false, error: parsed.error.issues[0].message };
  }

  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();

  const userId = user ? user.id : 'demo-user-id';

  const { error } = await supabase.from('items').insert({
    user_id: userId,
    title: parsed.data.title,
    description: parsed.data.description || '',
    is_completed: false,
  });

  if (error) {
    return { success: false, error: error.message };
  }

  revalidatePath('/');
  return { success: true };
}

export async function toggleItem(id: string, currentState: boolean) {
  const supabase = await createClient();
  const { error } = await supabase
    .from('items')
    .update({ is_completed: !currentState })
    .eq('id', id);

  if (error) {
    return { success: false, error: error.message };
  }

  revalidatePath('/');
  return { success: true };
}
