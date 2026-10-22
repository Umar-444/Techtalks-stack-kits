import { z } from 'zod';

export const createProjectSchema = z.object({
  title: z.string().min(3, 'Title must be at least 3 characters').max(100),
  description: z.string().max(500).optional(),
  tenantId: z.string().min(1, 'Tenant ID is required'),
  userId: z.string().min(1, 'User ID is required'),
});

export type CreateProjectInput = z.infer<typeof createProjectSchema>;

export const createTaskSchema = z.object({
  title: z.string().min(2, 'Task title required').max(100),
  description: z.string().max(300).optional(),
  status: z.enum(['todo', 'in_progress', 'done']).default('todo'),
  projectId: z.string().min(1, 'Project ID required'),
  tenantId: z.string().min(1, 'Tenant ID required'),
});

export type CreateTaskInput = z.infer<typeof createTaskSchema>;
