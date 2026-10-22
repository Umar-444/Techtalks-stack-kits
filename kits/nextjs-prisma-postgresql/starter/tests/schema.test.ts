import { describe, it, expect } from 'vitest';
import { createProjectSchema, createTaskSchema } from '../src/lib/validations';

describe('Validation Schemas', () => {
  it('should validate valid project input', () => {
    const valid = {
      title: 'Cloud Architecture Redesign',
      description: 'Revamping cloud components',
      tenantId: 'tenant-123',
      userId: 'user-456',
    };
    const res = createProjectSchema.safeParse(valid);
    expect(res.success).toBe(true);
  });

  it('should reject project with short title', () => {
    const invalid = {
      title: 'No',
      tenantId: 'tenant-123',
      userId: 'user-456',
    };
    const res = createProjectSchema.safeParse(invalid);
    expect(res.success).toBe(false);
  });
});
