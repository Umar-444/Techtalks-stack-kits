/**
 * Controls from security/checks.json, proved against the real files.
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(__dirname, '..');
const read = (p: string) => fs.readFileSync(path.join(root, p), 'utf8');
const walk = (d: string): string[] =>
  fs.readdirSync(path.join(root, d), { withFileTypes: true }).flatMap((e) =>
    e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]
  );

const migrations = walk('supabase/migrations')
  .filter((f) => f.endsWith('.sql'))
  .map((f) => read(f))
  .join('\n');
const sql = migrations.replace(/--.*$/gm, '');

describe('RLS-01/02/04: migrations', () => {
  const tables = [...sql.matchAll(/CREATE TABLE(?: IF NOT EXISTS)?\s+(?:public\.)?(\w+)/gi)].map((m) => m[1]);
  it('declares at least one table', () => expect(tables.length).toBeGreaterThan(0));
  it.each(tables)('RLS is enabled on %s', (t) => {
    expect(sql).toMatch(new RegExp(`ALTER TABLE\\s+(?:public\\.)?${t}\\s+ENABLE ROW LEVEL SECURITY`, 'i'));
  });
  it('has SELECT/INSERT/UPDATE/DELETE policies scoped by auth.uid() = user_id', () => {
    for (const op of ['SELECT', 'INSERT', 'UPDATE', 'DELETE']) {
      const m = sql.match(new RegExp(`CREATE POLICY[^;]*FOR ${op}[^;]*;`, 'is'));
      expect(m, `${op} policy`).not.toBeNull();
      expect(m![0]).toMatch(/auth\.uid\(\)\s*=\s*user_id/);
    }
  });
  it('INSERT and UPDATE use WITH CHECK so ownership cannot be reassigned', () => {
    expect(sql).toMatch(/FOR INSERT\s+WITH CHECK \(auth\.uid\(\) = user_id\)/i);
    expect(sql).toMatch(/FOR UPDATE[\s\S]*?WITH CHECK \(auth\.uid\(\) = user_id\)/i);
  });
  it('has no permissive USING (true) policy', () => {
    expect(sql).not.toMatch(/USING\s*\(\s*true\s*\)/i);
  });
  it('indexes (user_id, created_at)', () => {
    expect(sql).toMatch(/CREATE INDEX[^;]*\(\s*user_id\s*,\s*created_at/i);
  });
});

describe('RLS-03: service-role key never reaches a client bundle', () => {
  it('.env.example does not expose the service key via NEXT_PUBLIC_', () => {
    const env = read('.env.example');
    expect(env).not.toMatch(/NEXT_PUBLIC_[A-Z_]*SERVICE/i);
    expect(env).toMatch(/^SUPABASE_SERVICE_ROLE_KEY=/m);
  });
  it('no source file references the service-role key', () => {
    for (const f of walk('src')) {
      expect(read(f), f).not.toMatch(/SERVICE_ROLE/i);
    }
  });
  it('the browser client only uses NEXT_PUBLIC_ variables', () => {
    const src = read('src/lib/supabase/client.ts');
    expect(src).toMatch(/process\.env\.NEXT_PUBLIC_/);
    expect(src).not.toMatch(/process\.env\.(?!NEXT_PUBLIC_)/);
  });
  it('.env.example holds placeholders only', () => {
    expect(read('.env.example')).not.toMatch(/eyJ[A-Za-z0-9_-]{20,}/);
  });
});

describe('AUTH-01: session cookie flags', () => {
  const cookieStore = { getAll: () => [], set: vi.fn() };
  let setAll: (c: Array<{ name: string; value: string; options?: object }>) => void;

  async function load(env: string) {
    vi.resetModules();
    vi.stubEnv('NODE_ENV', env);
    vi.doMock('next/headers', () => ({ cookies: async () => cookieStore }));
    vi.doMock('@supabase/ssr', () => ({
      createServerClient: (_u: string, _k: string, cfg: any) => {
        setAll = cfg.cookies.setAll;
        return {};
      },
    }));
    const mod = await import('../src/lib/supabase/server');
    await mod.createClient();
  }
  beforeEach(() => cookieStore.set.mockClear());

  it('forces SameSite=Lax even if the library passes a weaker value', async () => {
    await load('development');
    setAll([{ name: 'sb', value: 'v', options: { sameSite: 'none' } }]);
    expect(cookieStore.set.mock.calls[0][2]).toMatchObject({ sameSite: 'lax', path: '/' });
  });
  it('forces Secure in production', async () => {
    await load('production');
    setAll([{ name: 'sb', value: 'v', options: { secure: false } }]);
    expect(cookieStore.set.mock.calls[0][2].secure).toBe(true);
  });
});

describe('AUTH-02/03: session verification', () => {
  it('middleware revalidates the user with getUser(), not getSession()', () => {
    const src = read('src/middleware.ts').replace(/\/\*[\s\S]*?\*\//g, '');
    expect(src).toMatch(/auth\.getUser\(\)/);
    expect(src).not.toMatch(/getSession\(/);
  });
  it('the dashboard page verifies the user on the server and filters by user_id', () => {
    const src = read('src/app/page.tsx');
    expect(src).toMatch(/auth\.getUser\(\)/);
    expect(src).toMatch(/\.eq\('user_id', user\.id\)/);
  });
});

describe('ACT-01/03: Server Action wiring', () => {
  it('actions validate with the shared strict schema and revalidate paths', () => {
    const src = read('src/app/actions.ts');
    expect(src).toMatch(/ItemSchema\.safeParse/);
    expect(src).toMatch(/revalidatePath\('\/'\)/);
  });
});
