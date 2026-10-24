'use server';

import { createClient } from '@/lib/supabase/server';
import { revalidatePath } from 'next/cache';
import { ItemSchema } from '@/lib/validations';

/**
 * Every mutation verifies the caller first (rules/source/01) and scopes the
 * query by user_id (rules/source/02, control RLS-02).
 *
 * RLS at the database is the backstop, not the only gate: an explicit
 * `.eq('user_id', ...)` means a missing or mis-ordered policy cannot silently
 * widen access, and the intent is visible at the call site.
 */

// Database error text can name tables, columns and constraints; never echo it.
const DB_FAILURE = { success: false as const, error: 'Request failed' };

const UNAUTHENTICATED = { success: false as const, error: 'Authentication required' };

export async function createItem(formData: FormData) {
  const parsed = ItemSchema.safeParse({
    title: formData.get('title'),
    description: formData.get('description') ?? undefined,
  });

  if (!parsed.success) {
    return { success: false, error: parsed.error.issues[0].message };
  }

  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();

  // No anonymous fallback: an unauthenticated write must fail, not be
  // attributed to a placeholder account.
  if (!user) return UNAUTHENTICATED;

  const { error } = await supabase.from('items').insert({
    user_id: user.id,
    title: parsed.data.title,
    description: parsed.data.description || '',
    is_completed: false,
  });

  if (error) return DB_FAILURE;

  revalidatePath('/');
  return { success: true };
}

export async function toggleItem(id: string, currentState: boolean) {
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return UNAUTHENTICATED;

  const { error } = await supabase
    .from('items')
    .update({ is_completed: !currentState })
    .eq('id', id)
    .eq('user_id', user.id);

  if (error) return DB_FAILURE;

  revalidatePath('/');
  return { success: true };
}

export async function deleteItem(id: string) {
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return UNAUTHENTICATED;

  const { error } = await supabase
    .from('items')
    .delete()
    .eq('id', id)
    .eq('user_id', user.id);

  if (error) return DB_FAILURE;

  revalidatePath('/');
  return { success: true };
}

export async function listItems() {
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return UNAUTHENTICATED;

  const { data, error } = await supabase
    .from('items')
    .select('*')
    .eq('user_id', user.id)
    .order('created_at', { ascending: false });

  if (error) return DB_FAILURE;

  return { success: true, items: data ?? [] };
}
