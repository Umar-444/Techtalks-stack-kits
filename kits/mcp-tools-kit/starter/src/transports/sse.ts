import express from 'express';
import cors from 'cors';
import crypto from 'node:crypto';
import { SSEServerTransport } from '@modelcontextprotocol/sdk/server/sse.js';
import { createMcpServer } from '../server.js';

export interface AppOptions {
  /** Bearer token required on /sse and /messages (SEC-07). */
  apiKey: string;
  /** Explicit CORS allowlist; never '*' (SEC-09). */
  allowedOrigins?: string[];
  /** Max JSON body size (SEC-08). */
  bodyLimit?: string;
  /** Max POST /messages per client per window (SEC-10). */
  rateLimitMax?: number;
  rateLimitWindowMs?: number;
}

function tokenMatches(presented: string, expected: string): boolean {
  const a = crypto.createHash('sha256').update(presented).digest();
  const b = crypto.createHash('sha256').update(expected).digest();
  return crypto.timingSafeEqual(a, b);
}

export function createApp(opts: AppOptions) {
  if (!opts.apiKey) throw new Error('MCP_API_KEY is required: refusing to start without auth');
  const allowed = opts.allowedOrigins ?? [];
  const max = opts.rateLimitMax ?? 60;
  const windowMs = opts.rateLimitWindowMs ?? 60_000;

  const app = express();
  app.disable('x-powered-by');
  app.use(
    cors({
      origin: (origin, cb) => cb(null, !origin || allowed.includes(origin)),
    })
  );
  app.use(express.json({ limit: opts.bodyLimit ?? '100kb' }));

  // One transport per client session, keyed by the SDK-issued sessionId.
  const transports = new Map<string, SSEServerTransport>();

  app.get('/api/health', (_req, res) => {
    res.json({ status: 'ok', protocol: 'mcp-1.0.0', transport: 'sse', tools_count: 3 });
  });

  const requireBearer: express.RequestHandler = (req, res, next) => {
    const m = /^Bearer (.+)$/.exec(req.headers.authorization ?? '');
    if (!m || !tokenMatches(m[1], opts.apiKey)) {
      res.status(401).set('WWW-Authenticate', 'Bearer').json({ error: 'Unauthorized' });
      return;
    }
    next();
  };

  const hits = new Map<string, { count: number; resetAt: number }>();
  const rateLimit: express.RequestHandler = (req, res, next) => {
    const key = req.ip ?? 'unknown';
    const now = Date.now();
    const rec = hits.get(key);
    if (!rec || now > rec.resetAt) {
      hits.set(key, { count: 1, resetAt: now + windowMs });
      return next();
    }
    rec.count += 1;
    if (rec.count > max) {
      res.status(429).json({ error: 'Too many requests' });
      return;
    }
    next();
  };

  app.get('/sse', requireBearer, async (_req, res) => {
    const transport = new SSEServerTransport('/messages', res);
    transports.set(transport.sessionId, transport);
    res.on('close', () => transports.delete(transport.sessionId));
    await createMcpServer().connect(transport);
  });

  app.post('/messages', requireBearer, rateLimit, async (req, res) => {
    const sessionId = String(req.query.sessionId ?? '');
    const transport = transports.get(sessionId);
    if (!transport) {
      res.status(400).json({ error: 'Unknown or missing session' });
      return;
    }
    await transport.handlePostMessage(req, res, req.body);
  });

  // Oversized or malformed bodies: generic JSON error, no stack or internals.
  app.use((err: any, _req: express.Request, res: express.Response, _next: express.NextFunction) => {
    const status = err?.status === 413 ? 413 : err?.status === 400 ? 400 : 500;
    res.status(status).json({ error: status === 413 ? 'Payload too large' : status === 400 ? 'Bad request' : 'Internal error' });
  });

  return app;
}

if (require.main === module) {
  const PORT = Number(process.env.PORT || 8080);
  const app = createApp({
    apiKey: process.env.MCP_API_KEY ?? '',
    allowedOrigins: (process.env.ALLOWED_ORIGINS ?? '').split(',').filter(Boolean),
  });
  app.listen(PORT, () => {
    console.error(`[MCP-SSE] Server listening on http://0.0.0.0:${PORT}`);
  });
}
