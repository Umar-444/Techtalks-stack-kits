import { describe, it, expect } from 'vitest';
import { ItemSchema } from '../src/lib/validations';

describe('ItemSchema', () => {
  it('accepts a valid payload', () => {
    expect(ItemSchema.safeParse({ title: 'Valid title', description: 'ok' }).success).toBe(true);
  });
  it('trims whitespace before measuring length', () => {
    expect(ItemSchema.safeParse({ title: '  ab  ' }).success).toBe(false);
  });
  it('rejects a short title', () => {
    expect(ItemSchema.safeParse({ title: 'No' }).success).toBe(false);
  });
  it('rejects an over-length title and description', () => {
    expect(ItemSchema.safeParse({ title: 'x'.repeat(121) }).success).toBe(false);
    expect(ItemSchema.safeParse({ title: 'Fine', description: 'x'.repeat(501) }).success).toBe(false);
  });
  it('rejects unknown keys instead of stripping them (.strict)', () => {
    expect(ItemSchema.safeParse({ title: 'Fine', user_id: 'victim' }).success).toBe(false);
    expect(ItemSchema.safeParse({ title: 'Fine', is_completed: true }).success).toBe(false);
  });
});
