/**
 * SSE transport hardening over a real HTTP listener on an ephemeral port:
 * bearer auth (SEC-07), CORS allowlist (SEC-09), body cap (SEC-08),
 * rate limiting (SEC-10) and raw JSON-RPC 2.0 conformance (SEC-06).
 */
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import type { Server } from 'node:http';
import type { AddressInfo } from 'node:net';
import { createApp } from '../src/transports/sse';

const KEY = 'test-key-not-a-real-secret'; // pragma: allowlist secret
const GOOD = 'http://app.example';
let server: Server;
let base: string;

beforeAll(async () => {
  const app = createApp({ apiKey: KEY, allowedOrigins: [GOOD], bodyLimit: '1kb', rateLimitMax: 1000 });
  await new Promise<void>((r) => (server = app.listen(0, '127.0.0.1', r)));
  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
});
afterAll(() => {
  server.closeAllConnections?.();
  server.close();
});

const auth = { Authorization: `Bearer ${KEY}` };

/** Opens /sse and returns the message endpoint plus a reader for later events. */
async function openSession() {
  const ac = new AbortController();
  const res = await fetch(`${base}/sse`, { headers: auth, signal: ac.signal });
  const reader = res.body!.getReader();
  const dec = new TextDecoder();
  let buf = '';
  const next = async (): Promise<{ event: string; data: string }> => {
    for (;;) {
      const i = buf.indexOf('\n\n');
      if (i >= 0) {
        const block = buf.slice(0, i);
        buf = buf.slice(i + 2);
        const event = /^event: (.*)$/m.exec(block)?.[1] ?? 'message';
        const data = /^data: (.*)$/m.exec(block)?.[1] ?? '';
        return { event, data };
      }
      const { value, done } = await reader.read();
      if (done) throw new Error('stream closed');
      buf += dec.decode(value);
    }
  };
  const ep = await next();
  return { endpoint: ep.data, next, close: () => ac.abort() };
}

const rpc = (endpoint: string, body: unknown) =>
  fetch(`${base}${endpoint}`, {
    method: 'POST',
    headers: { ...auth, 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

describe('SEC-07: bearer auth', () => {
  it('health stays open for container probes', async () => {
    expect((await fetch(`${base}/api/health`)).status).toBe(200);
  });
  it('rejects /sse without a token', async () => {
    expect((await fetch(`${base}/sse`)).status).toBe(401);
  });
  it('rejects /sse with a wrong token', async () => {
    expect((await fetch(`${base}/sse`, { headers: { Authorization: 'Bearer wrong' } })).status).toBe(401);
  });
  it('rejects /messages without a token', async () => {
    const r = await fetch(`${base}/messages?sessionId=x`, { method: 'POST', body: '{}', headers: { 'Content-Type': 'application/json' } });
    expect(r.status).toBe(401);
  });
  it('refuses to build an app with no key (fail closed)', () => {
    expect(() => createApp({ apiKey: '' })).toThrow(/MCP_API_KEY/);
  });
});

describe('SEC-09: CORS allowlist', () => {
  it('echoes an allowed origin only', async () => {
    const ok = await fetch(`${base}/api/health`, { headers: { Origin: GOOD } });
    expect(ok.headers.get('access-control-allow-origin')).toBe(GOOD);
    const bad = await fetch(`${base}/api/health`, { headers: { Origin: 'http://evil.example' } });
    expect(bad.headers.get('access-control-allow-origin')).toBeNull();
    expect(ok.headers.get('access-control-allow-origin')).not.toBe('*');
  });
});

describe('SEC-06: JSON-RPC 2.0 conformance over SSE', () => {
  it('initialize and tools/list return well-formed 2.0 responses with matching ids', async () => {
    const s = await openSession();
    try {
      expect(s.endpoint).toMatch(/^\/messages\?sessionId=/);
      const init = await rpc(s.endpoint, {
        jsonrpc: '2.0', id: 1, method: 'initialize',
        params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 't', version: '0' } },
      });
      expect(init.status).toBe(202);
      const m1 = JSON.parse((await s.next()).data);
      expect(m1).toMatchObject({ jsonrpc: '2.0', id: 1 });
      expect(m1.result.serverInfo.name).toBe('techtalks-mcp-server');

      await rpc(s.endpoint, { jsonrpc: '2.0', method: 'notifications/initialized' });
      await rpc(s.endpoint, { jsonrpc: '2.0', id: 2, method: 'tools/list' });
      const m2 = JSON.parse((await s.next()).data);
      expect(m2).toMatchObject({ jsonrpc: '2.0', id: 2 });
      expect(m2.result.tools).toHaveLength(3);
    } finally {
      s.close();
    }
  });

  it('an unknown method yields a -32601 error object, not a result', async () => {
    const s = await openSession();
    try {
      await rpc(s.endpoint, { jsonrpc: '2.0', id: 9, method: 'nope/not-a-method' });
      const m = JSON.parse((await s.next()).data);
      expect(m.jsonrpc).toBe('2.0');
      expect(m.id).toBe(9);
      expect(m.result).toBeUndefined();
      expect(m.error.code).toBe(-32601);
    } finally {
      s.close();
    }
  });

  it('a non-JSON-RPC body is rejected with 400', async () => {
    const s = await openSession();
    try {
      const r = await rpc(s.endpoint, { hello: 'world' });
      expect(r.status).toBe(400);
    } finally {
      s.close();
    }
  });

  it('routes each response to the session that asked (no shared global transport)', async () => {
    const a = await openSession();
    const b = await openSession();
    try {
      expect(a.endpoint).not.toBe(b.endpoint);
      await rpc(b.endpoint, { jsonrpc: '2.0', id: 77, method: 'tools/list' });
      const got = await Promise.race([
        b.next().then((m) => ({ who: 'b', m })),
        a.next().then((m) => ({ who: 'a', m })),
        new Promise<{ who: string }>((r) => setTimeout(() => r({ who: 'timeout' }), 2000)),
      ]);
      expect(got.who).toBe('b');
    } finally {
      a.close();
      b.close();
    }
  });

  it('an unknown sessionId is rejected, so sessions are not shared between clients', async () => {
    const r = await rpc('/messages?sessionId=does-not-exist', { jsonrpc: '2.0', id: 1, method: 'tools/list' });
    expect(r.status).toBe(400);
  });
});

describe('SEC-08: payload size cap', () => {
  it('rejects an oversized body with 413 and a generic message', async () => {
    const s = await openSession();
    try {
      const r = await rpc(s.endpoint, { jsonrpc: '2.0', id: 1, method: 'tools/call', params: { pad: 'x'.repeat(5000) } });
      expect(r.status).toBe(413);
      const body = await r.text();
      expect(body).toBe(JSON.stringify({ error: 'Payload too large' }));
    } finally {
      s.close();
    }
  });
});

describe('SEC-10: rate limiting', () => {
  it('returns 429 after the per-client limit', async () => {
    const app = createApp({ apiKey: KEY, rateLimitMax: 5, rateLimitWindowMs: 60_000 });
    const srv: Server = await new Promise((r) => {
      const x = app.listen(0, '127.0.0.1', () => r(x));
    });
    try {
      const url = `http://127.0.0.1:${(srv.address() as AddressInfo).port}/messages?sessionId=none`;
      const codes: number[] = [];
      for (let i = 0; i < 12; i++) {
        const r = await fetch(url, {
          method: 'POST',
          headers: { ...auth, 'Content-Type': 'application/json' },
          body: JSON.stringify({ jsonrpc: '2.0', id: i, method: 'ping' }),
        });
        codes.push(r.status);
      }
      expect(codes.slice(0, 5).every((c) => c === 400)).toBe(true); // reached the handler
      expect(codes.slice(5).every((c) => c === 429)).toBe(true);
    } finally {
      srv.close();
    }
  });
});
