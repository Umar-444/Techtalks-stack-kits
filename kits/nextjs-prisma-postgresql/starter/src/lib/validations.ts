import { z } from 'zod';

/**
 * Client-supplied fields only.
 *
 * `tenantId` and `userId` are deliberately absent: they come from the
 * authenticated session in the Server Action, never from the request body.
 * Accepting them here would let a caller create records inside another
 * tenant (security/checks.json SEC-05, SEC-12).
 *
 * `.strict()` makes a smuggled key an error rather than silently dropping
 * it, so an attempt shows up as a validation failure instead of passing
 * quietly.
 */
export const createProjectSchema = z
  .object({
    title: z.string().min(3, 'Title must be at least 3 characters').max(100),
    description: z.string().max(500).optional(),
  })
  .strict();

export type CreateProjectInput = z.infer<typeof createProjectSchema>;

export const createTaskSchema = z
  .object({
    title: z.string().min(2, 'Task title required').max(100),
    description: z.string().max(300).optional(),
    status: z.enum(['todo', 'in_progress', 'done']).default('todo'),
    projectId: z.string().min(1, 'Project ID required'),
  })
  .strict();

export type CreateTaskInput = z.infer<typeof createTaskSchema>;

/** Shape actually written to the database, after session fields are merged. */
export const projectPersistSchema = createProjectSchema.extend({
  tenantId: z.string().min(1),
  userId: z.string().min(1),
});

export const taskPersistSchema = createTaskSchema.extend({
  tenantId: z.string().min(1),
});
