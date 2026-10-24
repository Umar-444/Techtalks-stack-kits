/**
 * Security controls declared in security/checks.json, verified.
 *
 * Prisma and the session are mocked at the module boundary so these run
 * offline with no PostgreSQL. What is under test is the action's own logic:
 * whether it authenticates, what it writes, and what it scopes reads by.
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';

// vi.mock is hoisted above the module body, so anything it closes over must
// be created inside vi.hoisted rather than as a plain const.
const { prismaMock, auth } = vi.hoisted(() => ({
  prismaMock: {
    project: { create: vi.fn(), findFirst: vi.fn(), findMany: vi.fn() },
    task: { create: vi.fn() },
  },
  auth: {
    session: { userId: 'user-a', tenantId: 'tenant-a' } as
      | { userId: string; tenantId: string }
      | null,
  },
}));

vi.mock('../src/lib/prisma', () => ({ prisma: prismaMock }));

vi.mock('../src/lib/session', () => {
  class UnauthorizedError extends Error {
    constructor(message = 'Authentication required') {
      super(message);
      this.name = 'UnauthorizedError';
    }
  }
  return {
    UnauthorizedError,
    getSession: async () => auth.session,
    requireSession: async () => {
      if (!auth.session) throw new UnauthorizedError();
      return auth.session;
    },
  };
});

import {
  createProjectAction,
  createTaskAction,
  getProjectAction,
  listProjectsAction,
} from '../src/lib/actions';
import { createProjectSchema, createTaskSchema } from '../src/lib/validations';

beforeEach(() => {
  vi.clearAllMocks();
  auth.session = { userId: 'user-a', tenantId: 'tenant-a' };
  prismaMock.project.create.mockResolvedValue({ id: 'p1', tenantId: 'tenant-a' });
  prismaMock.project.findFirst.mockResolvedValue({ id: 'p1' });
  prismaMock.project.findMany.mockResolvedValue([]);
  prismaMock.task.create.mockResolvedValue({ id: 't1' });
});

// --- SEC-12: mass assignment prevention (A01:2025, CWE-915) ---------------

describe('SEC-12 mass assignment', () => {
  it('rejects a payload that smuggles tenantId', () => {
    const res = createProjectSchema.safeParse({
      title: 'Smuggled project',
      tenantId: 'tenant-victim',
    });
    expect(res.success).toBe(false);
  });

  it('rejects a payload that smuggles userId', () => {
    const res = createProjectSchema.safeParse({
      title: 'Smuggled project',
      userId: 'someone-else',
    });
    expect(res.success).toBe(false);
  });

  it('rejects arbitrary unknown keys rather than silently dropping them', () => {
    const res = createTaskSchema.safeParse({
      title: 'Task',
      projectId: 'p1',
      isAdmin: true,
    });
    expect(res.success).toBe(false);
  });

  it('never writes a client-supplied tenantId to the database', async () => {
    await createProjectAction({ title: 'Legitimate project' });
    const written = prismaMock.project.create.mock.calls[0][0].data;
    expect(written.tenantId).toBe('tenant-a');
    expect(written.userId).toBe('user-a');
  });
});

// --- SEC-05: multi-tenant isolation (A07:2025 / A01) ----------------------

describe('SEC-05 tenant isolation', () => {
  it('stamps the session tenant onto every created project', async () => {
    await createProjectAction({ title: 'Tenant scoped' });
    expect(prismaMock.project.create).toHaveBeenCalledWith(
      expect.objectContaining({ data: expect.objectContaining({ tenantId: 'tenant-a' }) }),
    );
  });

  it('scopes project listing by tenant', async () => {
    await listProjectsAction();
    expect(prismaMock.project.findMany).toHaveBeenCalledWith(
      expect.objectContaining({ where: expect.objectContaining({ tenantId: 'tenant-a' }) }),
    );
  });

  it('reads a single project with findFirst scoped by tenant, not findUnique', async () => {
    await getProjectAction('p1');
    expect(prismaMock.project.findFirst).toHaveBeenCalledWith(
      expect.objectContaining({
        where: expect.objectContaining({ id: 'p1', tenantId: 'tenant-a' }),
      }),
    );
  });

  it('treats a foreign project id as missing rather than forbidden', async () => {
    prismaMock.project.findFirst.mockResolvedValue(null);
    const res = await getProjectAction('project-of-tenant-b');
    expect(res.success).toBe(false);
    expect(JSON.stringify(res.error)).toContain('not found');
  });

  it('refuses to attach a task to a project outside the caller tenant', async () => {
    prismaMock.project.findFirst.mockResolvedValue(null);
    const res = await createTaskAction({ title: 'Cross tenant', projectId: 'p-of-b' });
    expect(res.success).toBe(false);
    expect(prismaMock.task.create).not.toHaveBeenCalled();
  });
});

// --- SEC-07 / session: authentication required (A07:2025) -----------------

describe('authentication guard', () => {
  it('rejects an unauthenticated create', async () => {
    auth.session = null;
    await expect(createProjectAction({ title: 'No session' })).rejects.toThrow(
      /Authentication required/,
    );
  });

  it('rejects an unauthenticated read', async () => {
    auth.session = null;
    await expect(listProjectsAction()).rejects.toThrow(/Authentication required/);
  });

  it('does not touch the database when unauthenticated', async () => {
    auth.session = null;
    await expect(createProjectAction({ title: 'No session' })).rejects.toThrow();
    expect(prismaMock.project.create).not.toHaveBeenCalled();
  });
});

// --- SEC-04: runtime schema validation (A05:2025, CWE-20) -----------------

describe('SEC-04 input validation', () => {
  it('rejects a title below the minimum length', () => {
    expect(createProjectSchema.safeParse({ title: 'No' }).success).toBe(false);
  });

  it('rejects an out-of-range status enum', () => {
    const res = createTaskSchema.safeParse({
      title: 'Task',
      projectId: 'p1',
      status: 'not_a_status',
    });
    expect(res.success).toBe(false);
  });

  it('applies the default status when omitted', () => {
    const res = createTaskSchema.safeParse({ title: 'Task', projectId: 'p1' });
    expect(res.success).toBe(true);
    if (res.success) expect(res.data.status).toBe('todo');
  });

  it('does not reach the database when validation fails', async () => {
    await createProjectAction({ title: 'x' });
    expect(prismaMock.project.create).not.toHaveBeenCalled();
  });
});

// --- SEC-01 / SEC-14: no committed secrets (A04:2025) ---------------------

describe('SEC-01 secret hygiene', () => {
  it('.env.example holds placeholders, not real credentials', async () => {
    const { readFileSync } = await import('node:fs');
    const { join } = await import('node:path');
    const content = readFileSync(join(__dirname, '..', '.env.example'), 'utf8');

    expect(content.startsWith('﻿')).toBe(false);
    for (const line of content.split('\n')) {
      const [key, ...rest] = line.split('=');
      if (!key || line.trim().startsWith('#')) continue;
      const value = rest.join('=').trim();
      if (/SECRET|PASSWORD|KEY|TOKEN/i.test(key) && value) {
        expect(/change|your|example|placeholder|xxx|localhost/i.test(value)).toBe(true);
      }
    }
  });
});
