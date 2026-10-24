/**
 * Server Actions with the Supabase client stubbed at the module boundary.
 * The stub records every query-builder call so tests can assert the exact
 * filters (`.eq('user_id', ...)`) the action constructs.
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';

const h = vi.hoisted(() => {
  const state = {
    user: { id: 'user-a' } as { id: string } | null,
    result: { data: null as unknown, error: null as null | { message: string } },
    calls: [] as Array<[string, unknown[]]>,
  };
  const builder: any = new Proxy(
    {},
    {
      get(_t, prop: string) {
        if (prop === 'then') {
          return (res: (v: unknown) => unknown) => res(state.result);
        }
        return (...args: unknown[]) => {
          state.calls.push([prop, args]);
          return builder;
        };
      },
    }
  );
  const client = {
    auth: { getUser: async () => ({ data: { user: state.user } }) },
    from: (t: string) => {
      state.calls.push(['from', [t]]);
      return builder;
    },
  };
  return { state, client, revalidatePath: vi.fn() };
});

vi.mock('@/lib/supabase/server', () => ({ createClient: async () => h.client }));
vi.mock('next/cache', () => ({ revalidatePath: h.revalidatePath }));

import { createItem, toggleItem, deleteItem, listItems } from '../src/app/actions';

const fd = (o: Record<string, string>) => {
  const f = new FormData();
  Object.entries(o).forEach(([k, v]) => f.set(k, v));
  return f;
};
const eqs = () => h.state.calls.filter(([m]) => m === 'eq').map(([, a]) => a);

beforeEach(() => {
  h.state.user = { id: 'user-a' };
  h.state.result = { data: null, error: null };
  h.state.calls.length = 0;
  h.revalidatePath.mockClear();
});

describe('createItem', () => {
  it('inserts with user_id from the session and revalidates', async () => {
    const r = await createItem(fd({ title: 'Buy milk' }));
    expect(r).toEqual({ success: true });
    const ins = h.state.calls.find(([m]) => m === 'insert')!;
    expect(ins[1][0]).toMatchObject({ user_id: 'user-a', title: 'Buy milk', is_completed: false });
    expect(h.revalidatePath).toHaveBeenCalledWith('/');
  });
  it('ignores a user_id smuggled in the form', async () => {
    await createItem(fd({ title: 'Buy milk', user_id: 'victim' }));
    const ins = h.state.calls.find(([m]) => m === 'insert')!;
    expect((ins[1][0] as any).user_id).toBe('user-a');
  });
  it('rejects invalid input before touching the database', async () => {
    const r = await createItem(fd({ title: 'x' }));
    expect(r.success).toBe(false);
    expect(h.state.calls).toHaveLength(0);
  });
  it('refuses unauthenticated callers with no write', async () => {
    h.state.user = null;
    const r = await createItem(fd({ title: 'Buy milk' }));
    expect(r).toEqual({ success: false, error: 'Authentication required' });
    expect(h.state.calls.some(([m]) => m === 'insert')).toBe(false);
  });
});

describe('RLS filter construction (defence in depth)', () => {
  it('toggleItem filters by id AND user_id', async () => {
    await toggleItem('item-1', false);
    expect(eqs()).toEqual([['id', 'item-1'], ['user_id', 'user-a']]);
    expect(h.state.calls.find(([m]) => m === 'update')![1][0]).toEqual({ is_completed: true });
  });
  it('deleteItem filters by id AND user_id', async () => {
    await deleteItem('item-1');
    expect(eqs()).toEqual([['id', 'item-1'], ['user_id', 'user-a']]);
  });
  it('listItems filters by user_id', async () => {
    h.state.result = { data: [{ id: 1 }], error: null };
    const r = await listItems();
    expect(eqs()).toEqual([['user_id', 'user-a']]);
    expect(r).toEqual({ success: true, items: [{ id: 1 }] });
  });
  it.each([
    ['toggleItem', () => toggleItem('i', false)],
    ['deleteItem', () => deleteItem('i')],
    ['listItems', () => listItems()],
  ])('%s requires authentication and never queries', async (_n, fn) => {
    h.state.user = null;
    const r = await fn();
    expect(r.success).toBe(false);
    expect(h.state.calls).toHaveLength(0);
  });
});

describe('error sanitization', () => {
  it('does not echo database error text to the client', async () => {
    h.state.result = { data: null, error: { message: 'duplicate key value violates constraint "items_pkey"' } };
    for (const r of [await createItem(fd({ title: 'Buy milk' })), await toggleItem('i', true), await deleteItem('i'), await listItems()]) {
      expect(r.success).toBe(false);
      expect(JSON.stringify(r)).not.toMatch(/items_pkey|constraint/);
    }
  });
});
