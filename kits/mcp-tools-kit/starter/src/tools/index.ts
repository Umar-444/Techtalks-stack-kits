import os from 'os';
import path from 'path';
import fs from 'fs';
import { z } from 'zod';

export const systemInfoSchema = z.object({});

export function handleSystemInfo() {
  return {
    platform: os.platform(),
    release: os.release(),
    architecture: os.arch(),
    cpuCount: os.cpus().length,
    totalMemoryMB: Math.round(os.totalmem() / 1024 / 1024),
    freeMemoryMB: Math.round(os.freemem() / 1024 / 1024),
  };
}

export const readSecureFileSchema = z.object({
  filepath: z.string().min(1, 'Filepath is required'),
});

export function handleReadSecureFile(filepath: string, sandboxRoot: string = process.cwd()) {
  const normalizedRoot = path.resolve(sandboxRoot);
  const targetPath = path.resolve(normalizedRoot, filepath);

  if (!targetPath.startsWith(normalizedRoot)) {
    throw new Error('SECURITY_ERROR: Access denied. Path outside sandbox boundary.');
  }

  if (!fs.existsSync(targetPath)) {
    throw new Error(`FILE_NOT_FOUND: ${filepath}`);
  }

  const stat = fs.statSync(targetPath);
  if (!stat.isFile()) {
    throw new Error(`NOT_A_FILE: ${filepath}`);
  }

  const content = fs.readFileSync(targetPath, 'utf-8');
  return {
    filepath,
    sizeBytes: stat.size,
    content: content.slice(0, 10000), // Cap output buffer
  };
}

export const calculatorSchema = z.object({
  a: z.number(),
  b: z.number(),
  operation: z.enum(['add', 'subtract', 'multiply', 'divide']),
});

export function handleCalculator(a: number, b: number, operation: string) {
  switch (operation) {
    case 'add': return a + b;
    case 'subtract': return a - b;
    case 'multiply': return a * b;
    case 'divide':
      if (b === 0) throw new Error('DIVISION_BY_ZERO: Cannot divide by zero');
      return a / b;
    default:
      throw new Error(`UNKNOWN_OPERATION: ${operation}`);
  }
}
