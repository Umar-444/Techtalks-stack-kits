import { describe, it, expect } from 'vitest';
import { createTaskSchema, taskPersistSchema } from '../src/lib/validations';

describe('createTaskSchema', () => {
  it('rejects an invalid status enum', () => {
    const res = createTaskSchema.safeParse({
      title: 'Deploy to cluster',
      status: 'non_existent_status',
      projectId: 'proj-123',
    });
    expect(res.success).toBe(false);
  });

  it('applies the default status when omitted', () => {
    const res = createTaskSchema.safeParse({
      title: 'Deploy to cluster',
      projectId: 'proj-123',
    });
    expect(res.success).toBe(true);
    if (res.success) expect(res.data.status).toBe('todo');
  });

  it('requires a projectId', () => {
    expect(createTaskSchema.safeParse({ title: 'Orphan task' }).success).toBe(false);
  });

  it('does not accept tenantId from the client', () => {
    const res = createTaskSchema.safeParse({
      title: 'Deploy to cluster',
      projectId: 'proj-123',
      tenantId: 'tenant-b',
    });
    expect(res.success).toBe(false);
  });
});

describe('taskPersistSchema', () => {
  it('requires the tenant stamped by the server', () => {
    const base = { title: 'Deploy', projectId: 'proj-123', status: 'todo' as const };
    expect(taskPersistSchema.safeParse(base).success).toBe(false);
    expect(taskPersistSchema.safeParse({ ...base, tenantId: 'tenant-a' }).success).toBe(true);
  });
});
