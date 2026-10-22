import { describe, it, expect } from 'vitest';
import { createTaskSchema } from '../src/lib/validations';

describe('Server Action Validations', () => {
  it('should reject task with invalid status enum', () => {
    const invalidTask = {
      title: 'Deploy to cluster',
      status: 'non_existent_status',
      projectId: 'proj-123',
      tenantId: 'tenant-123',
    };
    const res = createTaskSchema.safeParse(invalidTask);
    expect(res.success).toBe(false);
  });

  it('should accept task with default status', () => {
    const validTask = {
      title: 'Deploy to cluster',
      projectId: 'proj-123',
      tenantId: 'tenant-123',
    };
    const res = createTaskSchema.safeParse(validTask);
    expect(res.success).toBe(true);
    if (res.success) {
      expect(res.data.status).toBe('todo');
    }
  });
});
