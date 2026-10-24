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

export const MAX_READ_BYTES = 10_000;

/**
 * Root the file tool is confined to.
 *
 * Read at call time, not module load, so tests and callers can point it
 * elsewhere by setting the variable. Falling back to `process.cwd()` means an
 * operator who never sets ALLOWED_SANDBOX_DIR exposes the whole working
 * directory, which is why `.env.example` ships it set.
 */
export function defaultSandboxRoot(): string {
  return process.env.ALLOWED_SANDBOX_DIR?.trim() || process.cwd();
}

export function handleReadSecureFile(filepath: string, sandboxRoot: string = defaultSandboxRoot()) {
  // Resolve symlinks on both sides so a link inside the sandbox cannot point out of it.
  const realRoot = fs.realpathSync(path.resolve(sandboxRoot));
  const lexical = path.resolve(realRoot, filepath);

  const inside = (p: string) => {
    const rel = path.relative(realRoot, p);
    return rel === '' || (!rel.startsWith('..') && !path.isAbsolute(rel));
  };

  if (!inside(lexical)) {
    throw new Error('SECURITY_ERROR: Access denied. Path outside sandbox boundary.');
  }
  if (!fs.existsSync(lexical)) {
    throw new Error('FILE_NOT_FOUND: no such file in sandbox');
  }
  const targetPath = fs.realpathSync(lexical);
  if (!inside(targetPath)) {
    throw new Error('SECURITY_ERROR: Access denied. Path outside sandbox boundary.');
  }

  const stat = fs.statSync(targetPath);
  if (!stat.isFile()) {
    throw new Error('NOT_A_FILE: target is not a regular file');
  }

  // Read at most MAX_READ_BYTES; never load an arbitrarily large file into memory.
  const fd = fs.openSync(targetPath, 'r');
  try {
    const buf = Buffer.alloc(Math.min(stat.size, MAX_READ_BYTES));
    fs.readSync(fd, buf, 0, buf.length, 0);
    return { filepath, sizeBytes: stat.size, content: buf.toString('utf-8'), truncated: stat.size > MAX_READ_BYTES };
  } finally {
    fs.closeSync(fd);
  }
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
      throw new Error('UNKNOWN_OPERATION: unsupported operation');
  }
}

/**
 * Only errors carrying one of our structured codes reach the client; anything
 * else (fs errno text, absolute paths, stack fragments) becomes INTERNAL_ERROR.
 */
const SAFE_CODES = /^(SECURITY_ERROR|FILE_NOT_FOUND|NOT_A_FILE|DIVISION_BY_ZERO|UNKNOWN_OPERATION): /;
export function sanitizeError(err: unknown): string {
  const msg = err instanceof Error ? err.message : '';
  return SAFE_CODES.test(msg) ? msg : 'INTERNAL_ERROR: request failed';
}
