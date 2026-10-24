'use server';

import { prisma } from './prisma';
import { requireSession } from './session';
import {
  createProjectSchema,
  createTaskSchema,
} from './validations';

/**
 * Every action follows the same order, per rules/source/04:
 *   1. authenticate the caller
 *   2. validate the client payload (strict — smuggled keys are rejected)
 *   3. merge tenant/user from the session, never from the payload
 *   4. scope every read by tenantId
 */

export async function createProjectAction(rawInput: unknown) {
  const session = await requireSession();

  const result = createProjectSchema.safeParse(rawInput);
  if (!result.success) {
    return { success: false, error: result.error.flatten().fieldErrors };
  }

  const project = await prisma.project.create({
    data: {
      ...result.data,
      tenantId: session.tenantId,
      userId: session.userId,
    },
  });

  return { success: true, project };
}

export async function createTaskAction(rawInput: unknown) {
  const session = await requireSession();

  const result = createTaskSchema.safeParse(rawInput);
  if (!result.success) {
    return { success: false, error: result.error.flatten().fieldErrors };
  }

  // The parent project must belong to the caller's tenant, otherwise a valid
  // projectId from another tenant would let a task be attached across the
  // boundary (BOLA).
  const project = await prisma.project.findFirst({
    where: { id: result.data.projectId, tenantId: session.tenantId },
    select: { id: true },
  });

  if (!project) {
    return { success: false, error: { projectId: ['Project not found'] } };
  }

  const task = await prisma.task.create({
    data: { ...result.data, tenantId: session.tenantId },
  });

  return { success: true, task };
}

export async function listProjectsAction() {
  const session = await requireSession();

  const projects = await prisma.project.findMany({
    where: { tenantId: session.tenantId },
    orderBy: { createdAt: 'desc' },
  });

  return { success: true, projects };
}

export async function getProjectAction(projectId: string) {
  const session = await requireSession();

  // findFirst with tenantId, not findUnique by id: a foreign id must read as
  // missing rather than confirming the record exists.
  const project = await prisma.project.findFirst({
    where: { id: projectId, tenantId: session.tenantId },
  });

  if (!project) {
    return { success: false, error: { projectId: ['Project not found'] } };
  }

  return { success: true, project };
}
