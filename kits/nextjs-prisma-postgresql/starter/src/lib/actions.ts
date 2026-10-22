'use server';

import { prisma } from './prisma';
import { createProjectSchema, createTaskSchema, type CreateProjectInput, type CreateTaskInput } from './validations';

export async function createProjectAction(rawInput: unknown) {
  const result = createProjectSchema.safeParse(rawInput);
  if (!result.success) {
    return { success: false, error: result.error.flatten().fieldErrors };
  }

  const project = await prisma.project.create({
    data: result.data,
  });

  return { success: true, project };
}

export async function createTaskAction(rawInput: unknown) {
  const result = createTaskSchema.safeParse(rawInput);
  if (!result.success) {
    return { success: false, error: result.error.flatten().fieldErrors };
  }

  const task = await prisma.task.create({
    data: result.data,
  });

  return { success: true, task };
}
