import { z } from 'zod';

/**
 * Client payload for creating an item. `.strict()` rejects unknown keys so a
 * smuggled `user_id` or `is_completed` fails loudly instead of being dropped.
 * The owner always comes from the verified session, never the payload.
 */
export const ItemSchema = z
  .object({
    title: z.string().trim().min(3, 'Title must be at least 3 characters').max(120),
    description: z.string().trim().max(500).optional(),
  })
  .strict();

export type ItemInput = z.infer<typeof ItemSchema>;
