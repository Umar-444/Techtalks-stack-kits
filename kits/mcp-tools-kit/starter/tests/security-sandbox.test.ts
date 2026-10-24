import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { handleReadSecureFile, handleCalculator, sanitizeError, MAX_READ_BYTES } from '../src/tools/index';

let base: string;
let root: string;
let sibling: string;

beforeAll(() => {
  base = fs.mkdtempSync(path.join(os.tmpdir(), 'mcp-sbx-'));
  root = path.join(base, 'sandbox');
  // Sibling shares the sandbox name as a prefix: defeats naive startsWith checks.
  sibling = path.join(base, 'sandbox-evil');
  fs.mkdirSync(root);
  fs.mkdirSync(sibling);
  fs.writeFileSync(path.join(root, 'ok.txt'), 'hello');
  fs.writeFileSync(path.join(root, 'big.txt'), 'x'.repeat(MAX_READ_BYTES * 3));
  fs.mkdirSync(path.join(root, 'sub'));
  fs.writeFileSync(path.join(sibling, 'secret.txt'), 'TOP-SECRET');
});
afterAll(() => fs.rmSync(base, { recursive: true, force: true }));

describe('SEC-03: path traversal sandboxing', () => {
  it('reads a file inside the sandbox', () => {
    expect(handleReadSecureFile('ok.txt', root).content).toBe('hello');
  });
  it('rejects ../ traversal', () => {
    expect(() => handleReadSecureFile('../../../etc/passwd', process.cwd())).toThrowError(
      'SECURITY_ERROR: Access denied. Path outside sandbox boundary.'
    );
  });
  it('rejects a sibling directory that shares the sandbox name as a prefix', () => {
    expect(() => handleReadSecureFile('../sandbox-evil/secret.txt', root)).toThrowError(/SECURITY_ERROR/);
  });
  it('rejects absolute paths outside the sandbox', () => {
    expect(() => handleReadSecureFile(path.join(sibling, 'secret.txt'), root)).toThrowError(/SECURITY_ERROR/);
  });
  it('rejects a symlink inside the sandbox that points outside it', () => {
    const link = path.join(root, 'escape');
    try {
      fs.symlinkSync(sibling, link, 'junction');
    } catch {
      return; // platform refused to create the link; nothing to test
    }
    expect(() => handleReadSecureFile('escape/secret.txt', root)).toThrowError(/SECURITY_ERROR/);
  });
  it('refuses directories', () => {
    expect(() => handleReadSecureFile('sub', root)).toThrowError(/NOT_A_FILE/);
  });
});

describe('SEC-08: payload size capping', () => {
  it('returns at most MAX_READ_BYTES and flags truncation', () => {
    const r = handleReadSecureFile('big.txt', root);
    expect(r.content.length).toBe(MAX_READ_BYTES);
    expect(r.truncated).toBe(true);
    expect(r.sizeBytes).toBe(MAX_READ_BYTES * 3);
  });
  it('does not flag truncation for small files', () => {
    expect(handleReadSecureFile('ok.txt', root).truncated).toBe(false);
  });
});

describe('SEC-12: structured error sanitization', () => {
  it('passes through structured codes', () => {
    expect(sanitizeError(new Error('DIVISION_BY_ZERO: Cannot divide by zero'))).toMatch(/^DIVISION_BY_ZERO/);
  });
  it('hides raw fs errors, absolute paths and non-Error throws', () => {
    const raw = new Error("ENOENT: no such file or directory, open '/srv/app/secret.key'");
    expect(sanitizeError(raw)).toBe('INTERNAL_ERROR: request failed');
    expect(sanitizeError('boom /etc/passwd')).toBe('INTERNAL_ERROR: request failed');
  });
  it('does not echo the requested path in not-found errors', () => {
    try {
      handleReadSecureFile('nope-unique-name.txt', root);
    } catch (e) {
      expect(sanitizeError(e)).not.toMatch(/nope-unique-name/);
    }
  });
});

describe('SEC-05/11: no shell or eval, safe math', () => {
  it('src never imports child_process or calls eval/Function', () => {
    const walk = (d: string): string[] =>
      fs.readdirSync(d, { withFileTypes: true }).flatMap((e) =>
        e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]
      );
    for (const f of walk(path.resolve(__dirname, '../src'))) {
      const src = fs.readFileSync(f, 'utf8').replace(/\/\/.*$/gm, '');
      expect(src, f).not.toMatch(/child_process|(?<!without )\beval\s*\(|new Function\s*\(|\bexecSync\b|\bspawn\s*\(/);
    }
  });
  it('rejects unknown operations without echoing input', () => {
    expect(() => handleCalculator(1, 2, 'pow; rm -rf /')).toThrowError(/UNKNOWN_OPERATION: unsupported operation/);
  });
});

describe('SEC-01/02: container and secrets hygiene', () => {
  const starter = path.resolve(__dirname, '..');
  it('Dockerfile drops root in the runtime stage', () => {
    const df = fs.readFileSync(path.join(starter, 'Dockerfile'), 'utf8');
    const runner = df.slice(df.lastIndexOf('FROM '));
    expect(runner).toMatch(/^USER\s+(?!root\b)\S+/m);
  });
  it('.env.example carries placeholders, not real key material', () => {
    const env = fs.readFileSync(path.join(starter, '.env.example'), 'utf8');
    expect(env).not.toMatch(/(sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN)/);
  });
});

describe('ALLOWED_SANDBOX_DIR', () => {
  // The variable ships in .env.example but was never read: the sandbox root
  // silently fell back to process.cwd(), exposing the whole working directory
  // to an operator who had configured it correctly.
  it('is used as the default sandbox root', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'mcp-envroot-'));
    fs.writeFileSync(path.join(dir, 'inside.txt'), 'ok');
    const previous = process.env.ALLOWED_SANDBOX_DIR;
    process.env.ALLOWED_SANDBOX_DIR = dir;
    try {
      expect(handleReadSecureFile('inside.txt').content).toContain('ok');
      expect(() => handleReadSecureFile('../escape.txt')).toThrow(/SECURITY_ERROR/);
    } finally {
      if (previous === undefined) delete process.env.ALLOWED_SANDBOX_DIR;
      else process.env.ALLOWED_SANDBOX_DIR = previous;
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });
});
