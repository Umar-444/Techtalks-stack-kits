import { describe, it, expect } from 'vitest';
import { createProjectSchema, projectPersistSchema } from '../src/lib/validations';

describe('createProjectSchema', () => {
  it('accepts a valid client payload', () => {
    const res = createProjectSchema.safeParse({
      title: 'Cloud Architecture Redesign',
      description: 'Revamping cloud components',
    });
    expect(res.success).toBe(true);
  });

  it('accepts a payload without the optional description', () => {
    expect(createProjectSchema.safeParse({ title: 'Minimal project' }).success).toBe(true);
  });

  it('rejects a short title', () => {
    expect(createProjectSchema.safeParse({ title: 'No' }).success).toBe(false);
  });

  it('rejects a description over the 500 character limit', () => {
    const res = createProjectSchema.safeParse({
      title: 'Valid title',
      description: 'x'.repeat(501),
    });
    expect(res.success).toBe(false);
  });

  it('does not accept tenantId from the client', () => {
    const res = createProjectSchema.safeParse({
      title: 'Valid title',
      tenantId: 'tenant-b',
    });
    expect(res.success).toBe(false);
  });
});

describe('projectPersistSchema', () => {
  it('is the shape written to the database, with session fields merged in', () => {
    const res = projectPersistSchema.safeParse({
      title: 'Valid title',
      tenantId: 'tenant-a',
      userId: 'user-a',
    });
    expect(res.success).toBe(true);
  });

  it('requires a tenantId at persist time', () => {
    const res = projectPersistSchema.safeParse({ title: 'Valid title', userId: 'user-a' });
    expect(res.success).toBe(false);
  });
});
