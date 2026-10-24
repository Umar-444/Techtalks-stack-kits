/**
 * Passkey ceremonies exercised end to end through the Hono app with a software
 * authenticator that makes real signatures. The WebAuthn verifier is the real
 * @simplewebauthn/server; only the in-memory store is used (no Redis).
 */
import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';
import app from '../src/server';
import { authStore, MemoryAuthStore } from '../src/db';
import { SoftAuthenticator } from './authenticator';

const ORIGIN = 'http://localhost:8080';
const RP = 'localhost';
const starter = path.resolve(__dirname, '..');

type Jar = Record<string, string>;
function absorb(res: Response, jar: Jar) {
  for (const line of res.headers.getSetCookie()) {
    const [pair] = line.split(';');
    const i = pair.indexOf('=');
    const name = pair.slice(0, i);
    const val = pair.slice(i + 1);
    if (/max-age=0/i.test(line) || val === '') delete jar[name];
    else jar[name] = val;
  }
}
const cookieHeader = (jar: Jar) => Object.entries(jar).map(([k, v]) => `${k}=${v}`).join('; ');
const get = (url: string, jar: Jar = {}) => app.request(url, { headers: { cookie: cookieHeader(jar) } });
const post = (url: string, body: unknown, jar: Jar = {}, raw = false) =>
  app.request(url, {
    method: 'POST',
    headers: { 'content-type': 'application/json', cookie: cookieHeader(jar) },
    body: raw ? (body as string) : JSON.stringify(body),
  });

async function register(auth: SoftAuthenticator, userId?: string, jar: Jar = {}) {
  const q = userId ? `?userId=${userId}` : '';
  const optRes = await get(`/api/auth/register-options${q}`, jar);
  absorb(optRes, jar);
  const options = await optRes.json();
  return { options, jar, optRes };
}
async function registerOk(auth: SoftAuthenticator, userId?: string) {
  const { options, jar } = await register(auth, userId);
  const res = await post('/api/auth/register-verify', auth.register({ challenge: options.challenge, origin: ORIGIN, rpId: RP }), jar);
  absorb(res, jar);
  return { res, body: await res.json(), jar };
}
async function loginOptions(jar: Jar = {}) {
  const res = await get('/api/auth/authenticate-options', jar);
  absorb(res, jar);
  return { options: await res.json(), jar };
}

afterEach(() => vi.useRealTimers());

describe('SEC-07: health endpoint', () => {
  it('reports status and relying party', async () => {
    const body = await (await get('/health')).json();
    expect(body).toMatchObject({ status: 'ok', rpId: RP });
  });
});

describe('registration ceremony (happy path proves the harness is real)', () => {
  it('a software authenticator registers and then authenticates', async () => {
    const a = new SoftAuthenticator();
    const reg = await registerOk(a);
    expect(reg.res.status).toBe(200);
    expect(reg.body.verified).toBe(true);

    const { options, jar } = await loginOptions();
    const res = await post('/api/auth/authenticate-verify', a.assert({ challenge: options.challenge, origin: ORIGIN, rpId: RP }), jar);
    expect(res.status).toBe(200);
    expect((await res.json()).userId).toBe(reg.body.userId);
  });
});

describe('SEC-11: strict origin and RP ID verification', () => {
  it('rejects registration from a different origin', async () => {
    const a = new SoftAuthenticator();
    const { options, jar } = await register(a);
    const res = await post('/api/auth/register-verify', a.register({ challenge: options.challenge, origin: 'http://evil.example', rpId: RP }), jar);
    expect(res.status).toBe(400);
    expect(await authStore.getPasskeyById(a.id)).toBeNull();
  });
  it('rejects registration bound to a different RP ID', async () => {
    const a = new SoftAuthenticator();
    const { options, jar } = await register(a);
    const res = await post('/api/auth/register-verify', a.register({ challenge: options.challenge, origin: ORIGIN, rpId: 'evil.example' }), jar);
    expect(res.status).toBe(400);
    expect(await authStore.getPasskeyById(a.id)).toBeNull();
  });
  it('rejects registration without user verification', async () => {
    const a = new SoftAuthenticator();
    const { options, jar } = await register(a);
    const res = await post('/api/auth/register-verify', a.register({ challenge: options.challenge, origin: ORIGIN, rpId: RP, userVerified: false }), jar);
    expect(res.status).toBe(400);
  });
  it('rejects assertions from a different origin or RP ID', async () => {
    const a = new SoftAuthenticator();
    await registerOk(a);
    for (const bad of [{ origin: 'http://evil.example', rpId: RP }, { origin: ORIGIN, rpId: 'evil.example' }]) {
      const { options, jar } = await loginOptions();
      const res = await post('/api/auth/authenticate-verify', a.assert({ challenge: options.challenge, ...bad }), jar);
      expect(res.status).toBe(400);
      expect(jar.sid).toBeUndefined();
    }
  });
  it('rejects an assertion over the wrong challenge', async () => {
    const a = new SoftAuthenticator();
    await registerOk(a);
    const { jar } = await loginOptions();
    const res = await post('/api/auth/authenticate-verify', a.assert({ challenge: 'AAAA', origin: ORIGIN, rpId: RP }), jar);
    expect(res.status).toBe(400);
  });
  it('rejects a forged signature', async () => {
    const a = new SoftAuthenticator();
    await registerOk(a);
    const forger = new SoftAuthenticator();
    const { options, jar } = await loginOptions();
    const forged = forger.assert({ challenge: options.challenge, origin: ORIGIN, rpId: RP });
    forged.id = a.id;
    forged.rawId = a.id;
    const res = await post('/api/auth/authenticate-verify', forged, jar);
    expect(res.status).toBe(400);
    expect(jar.sid).toBeUndefined();
  });
});

describe('SEC-05: single-use challenge (replay defence)', () => {
  it('a captured assertion cannot be replayed with the same challenge cookie', async () => {
    const a = new SoftAuthenticator();
    await registerOk(a);
    const { options, jar } = await loginOptions();
    const assertion = a.assert({ challenge: options.challenge, origin: ORIGIN, rpId: RP });
    const replayJar = { ...jar };
    expect((await post('/api/auth/authenticate-verify', assertion, jar)).status).toBe(200);
    const replay = await post('/api/auth/authenticate-verify', assertion, replayJar);
    expect(replay.status).toBe(400);
  });
  it('a registration response cannot be replayed', async () => {
    const a = new SoftAuthenticator();
    const { options, jar } = await register(a);
    const resp = a.register({ challenge: options.challenge, origin: ORIGIN, rpId: RP });
    const replayJar = { ...jar };
    expect((await post('/api/auth/register-verify', resp, jar)).status).toBe(200);
    expect((await post('/api/auth/register-verify', resp, replayJar)).status).toBe(400);
  });
  it('a failed attempt still burns the challenge', async () => {
    const a = new SoftAuthenticator();
    await registerOk(a);
    const { options, jar } = await loginOptions();
    const retryJar = { ...jar };
    const bad = await post('/api/auth/authenticate-verify', a.assert({ challenge: options.challenge, origin: 'http://evil.example', rpId: RP }), jar);
    expect(bad.status).toBe(400);
    const good = await post('/api/auth/authenticate-verify', a.assert({ challenge: options.challenge, origin: ORIGIN, rpId: RP }), retryJar);
    expect(good.status).toBe(400);
  });
  it('verify without any challenge cookie is refused', async () => {
    const a = new SoftAuthenticator();
    await registerOk(a);
    const res = await post('/api/auth/authenticate-verify', a.assert({ challenge: 'x', origin: ORIGIN, rpId: RP }));
    expect(res.status).toBe(400);
  });
});

describe('SEC-04: challenge expiry (< 120s TTL)', () => {
  it('store drops a challenge after 120 seconds and consumes it either way', async () => {
    vi.useFakeTimers();
    const store = new MemoryAuthStore();
    await store.saveChallenge('k', 'c');
    vi.advanceTimersByTime(119_000);
    expect(await store.consumeChallenge('k')).toMatchObject({ challenge: 'c' });
    await store.saveChallenge('k2', 'c2');
    vi.advanceTimersByTime(121_000);
    expect(await store.consumeChallenge('k2')).toBeNull();
    expect(await store.consumeChallenge('k2')).toBeNull();
  });
  it('the default TTL is not longer than 120 seconds', () => {
    const src = fs.readFileSync(path.join(starter, 'src/db.ts'), 'utf8');
    expect(src).toMatch(/ttlSeconds: number = 120/);
  });
});

describe('SEC-08: authenticator cloning defence (counter rollback)', () => {
  it('rejects a counter that does not increase after a successful login', async () => {
    const a = new SoftAuthenticator();
    await registerOk(a);
    const l1 = await loginOptions();
    expect((await post('/api/auth/authenticate-verify', a.assert({ challenge: l1.options.challenge, origin: ORIGIN, rpId: RP, counter: 5 }), l1.jar)).status).toBe(200);
    expect((await authStore.getPasskeyById(a.id))!.counter).toBe(5);

    const l2 = await loginOptions();
    const res = await post('/api/auth/authenticate-verify', a.assert({ challenge: l2.options.challenge, origin: ORIGIN, rpId: RP, counter: 5 }), l2.jar);
    expect([400, 403]).toContain(res.status);
    expect(res.status).not.toBe(200);
    expect((await authStore.getPasskeyById(a.id))!.counter).toBe(5);
  });
  it('accepts a strictly increasing counter and persists it', async () => {
    const a = new SoftAuthenticator();
    await registerOk(a);
    for (const n of [1, 2, 9]) {
      const l = await loginOptions();
      expect((await post('/api/auth/authenticate-verify', a.assert({ challenge: l.options.challenge, origin: ORIGIN, rpId: RP, counter: n }), l.jar)).status).toBe(200);
      expect((await authStore.getPasskeyById(a.id))!.counter).toBe(n);
    }
  });
});

describe('SEC-09/10: session fixation defence and cookie attributes', () => {
  it('issues a fresh sid at login, killing any pre-login sid', async () => {
    const a = new SoftAuthenticator();
    const reg = await registerOk(a);
    await authStore.createSession('attacker-planted-sid', 'nobody');
    const l = await loginOptions({ sid: 'attacker-planted-sid' });
    const res = await post('/api/auth/authenticate-verify', a.assert({ challenge: l.options.challenge, origin: ORIGIN, rpId: RP }), l.jar);
    expect(res.status).toBe(200);
    absorb(res, l.jar);
    expect(l.jar.sid).toBeDefined();
    expect(l.jar.sid).not.toBe('attacker-planted-sid');
    expect(await authStore.getSessionUser('attacker-planted-sid')).toBeNull();
    expect(await authStore.getSessionUser(l.jar.sid)).toBe(reg.body.userId);
  });
  it('sid and challenge cookies are HttpOnly and SameSite=Lax', async () => {
    const a = new SoftAuthenticator();
    await registerOk(a);
    const l = await get('/api/auth/authenticate-options');
    const challengeCookie = l.headers.getSetCookie().find((c) => c.startsWith('auth_challenge_session='))!;
    expect(challengeCookie).toMatch(/HttpOnly/i);
    expect(challengeCookie).toMatch(/SameSite=Lax/i);
    expect(challengeCookie).toMatch(/Max-Age=120/i);

    const jar: Jar = {};
    absorb(l, jar);
    const options = await l.json();
    const res = await post('/api/auth/authenticate-verify', a.assert({ challenge: options.challenge, origin: ORIGIN, rpId: RP }), jar);
    const sid = res.headers.getSetCookie().find((c) => c.startsWith('sid='))!;
    expect(sid).toMatch(/HttpOnly/i);
    expect(sid).toMatch(/SameSite=Lax/i);
  });
});

describe('account takeover defence on registration', () => {
  it('refuses to add a passkey to an existing user without that user\'s session', async () => {
    const victim = new SoftAuthenticator();
    const v = await registerOk(victim);
    const res = await get(`/api/auth/register-options?userId=${v.body.userId}`);
    expect(res.status).toBe(401);
  });
  it('allows adding a second passkey with the owner\'s session', async () => {
    const a = new SoftAuthenticator();
    const reg = await registerOk(a);
    const l = await loginOptions();
    const login = await post('/api/auth/authenticate-verify', a.assert({ challenge: l.options.challenge, origin: ORIGIN, rpId: RP }), l.jar);
    absorb(login, l.jar);
    const res = await get(`/api/auth/register-options?userId=${reg.body.userId}`, l.jar);
    expect(res.status).toBe(200);
  });
  it('does not fall back to a shared default account', async () => {
    const a = new SoftAuthenticator();
    const b = new SoftAuthenticator();
    const ra = await registerOk(a);
    const rb = await registerOk(b);
    expect(ra.body.userId).not.toBe(rb.body.userId);
    expect(ra.body.userId).not.toBe('user-default-123');
  });
  it('the identity is bound to the issued challenge, not to query parameters at verify time', async () => {
    const a = new SoftAuthenticator();
    const { options, jar } = await register(a);
    const res = await post('/api/auth/register-verify?userId=victim', a.register({ challenge: options.challenge, origin: ORIGIN, rpId: RP }), jar);
    expect(res.status).toBe(200);
    expect((await authStore.getPasskeyById(a.id))!.userId).not.toBe('victim');
  });
});
describe('error sanitization and payload caps', () => {
  it('malformed JSON gets a generic 400, not a stack trace', async () => {
    const { jar } = await loginOptions();
    const res = await post('/api/auth/authenticate-verify', '{not json', jar, true);
    expect(res.status).toBe(400);
    expect(await res.json()).toEqual({ error: 'Invalid request body' });
  });
  it('verifier failures do not echo library error text', async () => {
    const a = new SoftAuthenticator();
    const { options, jar } = await register(a);
    const res = await post('/api/auth/register-verify', a.register({ challenge: options.challenge, origin: 'http://evil.example', rpId: RP }), jar);
    const text = await res.text();
    expect(text).toBe(JSON.stringify({ error: 'Registration verification failed' }));
    expect(text).not.toMatch(/origin|expected|evil/i);
  });
  it('an unknown credential id is a generic failure', async () => {
    const a = new SoftAuthenticator();
    const { options, jar } = await loginOptions();
    const res = await post('/api/auth/authenticate-verify', a.assert({ challenge: options.challenge, origin: ORIGIN, rpId: RP }), jar);
    expect(res.status).toBe(400);
    expect(await res.json()).toEqual({ error: 'Authentication failed' });
  });
  it('rejects an oversized body with 413', async () => {
    const res = await app.request('/api/auth/register-verify', {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'content-length': '70000' },
      body: JSON.stringify({ pad: 'x'.repeat(70_000) }),
    });
    expect(res.status).toBe(413);
  });
});

describe('SEC-03: explicit CORS, no wildcard', () => {
  it('echoes an allowed origin and withholds it from others', async () => {
    const ok = await app.request('/health', { headers: { origin: 'http://localhost:3000' } });
    expect(ok.headers.get('access-control-allow-origin')).toBe('http://localhost:3000');
    const bad = await app.request('/health', { headers: { origin: 'http://evil.example' } });
    expect(bad.headers.get('access-control-allow-origin')).not.toBe('http://evil.example');
    expect(bad.headers.get('access-control-allow-origin')).not.toBe('*');
  });
});

describe('SEC-06/01: container and secrets hygiene', () => {
  it('Dockerfile runtime stage runs as UID 10001', () => {
    const df = fs.readFileSync(path.join(starter, 'Dockerfile'), 'utf8');
    expect(df.slice(df.lastIndexOf('FROM '))).toMatch(/^USER\s+10001/m);
  });
  it('.env.example has no real key material', () => {
    expect(fs.readFileSync(path.join(starter, '.env.example'), 'utf8')).not.toMatch(/(sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN)/);
  });
});
