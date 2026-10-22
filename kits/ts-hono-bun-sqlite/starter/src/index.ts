import { Hono } from "hono";
import { Database } from "bun:sqlite";
import { z } from "zod";
import { zValidator } from "@hono/zod-validator";

const app = new Hono();

// Initialize SQLite with WAL mode for high concurrency
const db = new Database("app.db");
db.run("PRAGMA journal_mode = WAL;");
db.run("PRAGMA synchronous = NORMAL;");
db.run("PRAGMA foreign_keys = ON;");

// Initialize tables
db.run(`
  CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    text TEXT NOT NULL,
    created_at INTEGER NOT NULL
  )
`);

db.run("CREATE INDEX IF NOT EXISTS idx_messages_created ON messages (created_at DESC);");

// Input Validation Schemas
const CreateMessageSchema = z.object({
  text: z.string().min(1, "Text cannot be empty").max(500, "Text must be under 500 characters").trim()
}).strict();

const QueryMessagesSchema = z.object({
  limit: z.coerce.number().min(1).max(100).default(50),
  skip: z.coerce.number().min(0).default(0)
});

// Prepared Statements for high performance
const insertMessageStmt = db.prepare("INSERT INTO messages (id, text, created_at) VALUES (?, ?, ?)");
const selectMessagesStmt = db.prepare("SELECT * FROM messages ORDER BY created_at DESC LIMIT ? OFFSET ?");

// Healthz Probe
app.get("/healthz", (c) => {
  return c.json({
    status: "ok",
    app: "ts-hono-bun-sqlite",
    version: "1.0.0",
    runtime: "bun",
    database: "sqlite-wal"
  });
});

app.get("/health", (c) => {
  return c.json({ status: "ok", runtime: "bun", framework: "hono", token_light: true });
});

// List Messages with Pagination Bounds
app.get("/api/messages", zValidator("query", QueryMessagesSchema), (c) => {
  const { limit, skip } = c.req.valid("query");
  const rows = selectMessagesStmt.all(limit, skip);
  return c.json({
    data: rows,
    limit,
    skip,
    count: rows.length
  });
});

// Create Message with Strict Zod Validation
app.post("/api/messages", zValidator("json", CreateMessageSchema), async (c) => {
  const { text } = c.req.valid("json");
  const id = crypto.randomUUID();
  const createdAt = Date.now();
  
  insertMessageStmt.run(id, text, createdAt);
  
  return c.json({
    created: true,
    message: { id, text, created_at: createdAt }
  }, 201);
});

export default app;

if (import.meta.main) {
  console.log("Hono + Bun server running on http://localhost:3000");
}
