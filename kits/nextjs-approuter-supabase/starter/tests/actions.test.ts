import { z } from 'zod';

const ItemSchema = z.object({
  title: z.string().trim().min(3).max(120),
  description: z.string().trim().max(500).optional(),
});

describe('Server Action Zod Validation', () => {
  it('validates correct item payload', () => {
    const result = ItemSchema.safeParse({
      title: 'Valid Title',
      description: 'Valid Description',
    });
    expect(result.success).toBe(true);
  });

  it('rejects title shorter than 3 characters', () => {
    const result = ItemSchema.safeParse({
      title: 'No',
    });
    expect(result.success).toBe(false);
  });
});
