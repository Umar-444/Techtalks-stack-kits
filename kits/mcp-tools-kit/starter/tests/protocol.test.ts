/**
 * JSON-RPC 2.0 / MCP conformance (SEC-06) and Zod input validation (SEC-04),
 * driven through the real McpServer with an in-memory transport.
 */
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import fs from 'node:fs';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { InMemoryTransport } from '@modelcontextprotocol/sdk/inMemory.js';
import { createMcpServer } from '../src/server';

let client: Client;

beforeAll(async () => {
  const [ct, st] = InMemoryTransport.createLinkedPair();
  await createMcpServer().connect(st);
  client = new Client({ name: 'test', version: '0.0.0' });
  await client.connect(ct);
});
afterAll(async () => client.close());

const text = (r: any) => r.content[0].text as string;

describe('MCP protocol', () => {
  it('advertises the three tools with typed input schemas', async () => {
    const { tools } = await client.listTools();
    expect(tools.map((t) => t.name).sort()).toEqual(['calculator', 'read_secure_file', 'system_info']);
    const calc = tools.find((t) => t.name === 'calculator')!;
    expect(calc.inputSchema.type).toBe('object');
    expect(calc.inputSchema.required).toEqual(expect.arrayContaining(['a', 'b', 'operation']));
  });

  it('executes calculator through the protocol', async () => {
    const r = await client.callTool({ name: 'calculator', arguments: { a: 6, b: 7, operation: 'multiply' } });
    expect(JSON.parse(text(r)).result).toBe(42);
  });

  it('SEC-04: wrong types and enum values are rejected by Zod', async () => {
    for (const args of [
      { a: '1; DROP TABLE', b: 2, operation: 'add' },
      { a: 1, b: 2, operation: 'pow' },
      { a: 1, b: 2 },
    ]) {
      const outcome = await client.callTool({ name: 'calculator', arguments: args as any }).then(
        (r: any) => ({ rejected: r.isError === true, text: r.content?.[0]?.text ?? '' }),
        (e) => ({ rejected: true, text: String(e.message) })
      );
      expect(outcome.rejected).toBe(true);
    }
  });

  it('SEC-12: tool errors are structured and carry no internals', async () => {
    const r: any = await client.callTool({ name: 'read_secure_file', arguments: { filepath: '../../etc/passwd' } });
    expect(r.isError).toBe(true);
    expect(text(r)).toMatch(/^ERROR: SECURITY_ERROR/);
    expect(text(r)).not.toMatch(/\bat\s.+:\d+:\d+|node_modules/);
    const d: any = await client.callTool({ name: 'calculator', arguments: { a: 1, b: 0, operation: 'divide' } });
    expect(d.isError).toBe(true);
    expect(text(d)).toMatch(/DIVISION_BY_ZERO/);
  });

  it('an unknown tool is a JSON-RPC error, not a crash', async () => {
    const outcome = await client.callTool({ name: 'rm_rf', arguments: {} }).then(
      (r: any) => (r.isError ? 'error' : 'ok'),
      () => 'error'
    );
    expect(outcome).toBe('error');
  });

  it('SEC-12: an unexpected internal failure is masked at the protocol boundary', async () => {
    const spy = vi.spyOn(fs, 'openSync').mockImplementation(() => {
      throw new Error("EACCES: permission denied, open '/srv/secret/path.key'");
    });
    try {
      const r: any = await client.callTool({ name: 'read_secure_file', arguments: { filepath: 'package.json' } });
      expect(r.isError).toBe(true);
      expect(text(r)).toBe('ERROR: INTERNAL_ERROR: request failed');
      expect(text(r)).not.toMatch(/EACCES|secret/);
    } finally {
      spy.mockRestore();
    }
  });
});
