# GitHub Copilot Instructions for TypeScript + Hono + Bun + SQLite (Drizzle ORM)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Architectural Standards for TypeScript + Hono + Bun + Drizzle + SQLite
# Architecture Standards: TypeScript + Hono + Bun + Drizzle + SQLite
- Strictly adhere to modular component separation.
- Keep dependency surface minimal and auditable.
- Prefer explicit configuration over magic implicit defaults.

## Hono Web Framework Conventions and Middleware Chaining
# Hono Web Framework Conventions and Middleware Chaining

## 1. Minimal Zero-Overhead Handler Design
- Instantiate applications using `new Hono()`. Keep routing declarative and modular using `app.route('/prefix', subApp)`.
- Use native Web Standard objects: Hono handlers accept standard `Context` (`c`) wrapping `Request` and returning standard `Response`.
- Always return typed JSON using `return c.json(data, status)`.

## 2. Middleware Architecture
- Order middleware logically:
  1. `logger()`: Request timing and access logs.
  2. `secureHeaders()`: Helmet-like HTTP response security headers (HSTS, CSP, X-Frame-Options).
  3. `cors()`: Explicit origin whitelisting. Never permit wildcard `*` with credentials.
  4. Authentication & RBAC middleware.
- Never block the event loop inside middleware. Use asynchronous handlers.

## 3. Error Handling
- Register a global error boundary using `app.onError((err, c) => ...)` returning standardized RFC 7807 Problem Details or JSON error envelopes.

## Bun Runtime Execution and Native SQLite Engine
# Bun Runtime Execution and Native SQLite Engine

## 1. Native SQLite (`bun:sqlite`) Optimization
- Utilize Bun's built-in `Database` module for maximum performance with near C-speed bindings.
- Always initialize databases in Write-Ahead Logging (WAL) mode for high concurrent throughput:
  ```typescript
  const db = new Database("app.db");
  db.run("PRAGMA journal_mode = WAL;");
  db.run("PRAGMA synchronous = NORMAL;");
  db.run("PRAGMA foreign_keys = ON;");
  ```

## 2. Prepared Statement Discipline
- Always prepare statements for repetitive lookups to benefit from statement caching:
  ```typescript
  const queryUser = db.query("SELECT * FROM users WHERE id = ?");
  const user = queryUser.get(userId);
  ```
- Prohibit string concatenation into SQL statements. Every parameter must use bind parameters (`?` or `$param`).

## 3. Transaction Isolation
- Wrap multi-statement mutations in `db.transaction()` to ensure atomicity and rollbacks on failure.

## Security Invariants for TypeScript + Hono + Bun + Drizzle + SQLite
# Security Invariants
- Verify tenant boundary before reading or writing any persistent state.
- Sanitize all external inputs using validated schemas.
- Reject requests with missing or expired bearer tokens.

## Agent Coding Conventions for TypeScript + Hono + Bun + Drizzle + SQLite
# Agent Coding Conventions
- Maintain clean, minimal code changes with zero extraneous comments.
- Run typecheck and compile verification after every file modification.
- Never introduce undocumented third-party libraries without explicit instructions.

## Drizzle ORM Schema Discipline and Typed Migrations
# Drizzle ORM Schema Discipline and Typed Migrations

## 1. Declarative Schema Definitions
- Declare schemas in `src/db/schema.ts` using `sqliteTable`:
  ```typescript
  import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core";

  export const tasks = sqliteTable("tasks", {
    id: text("id").primaryKey(),
    title: text("title").notNull(),
    status: text("status").notNull().default("pending"),
    userId: text("user_id").notNull(),
    createdAt: integer("created_at", { mode: "timestamp" }).notNull()
  });
  ```
- Always define explicit nullability, default values, and foreign keys.

## 2. Immutable Migrations
- Generate migrations via `drizzle-kit generate`. Never modify applied SQL migrations.
- Apply migrations programmatically at service boot using `migrate(db, { migrationsFolder: "./drizzle" })`.

## 3. Zero-Overhead Typed Queries
- Leverage Drizzle's relational queries (`db.query.tasks.findMany({ where: ... })`) to eliminate N+1 queries.

## Zod Schema Validation, Input Sanitization, and API Security
# Zod Schema Validation, Input Sanitization, and API Security

## 1. Strict Request Validation
- Enforce Zod schemas on all incoming request bodies, query params, and URL path variables:
  ```typescript
  import { zValidator } from "@hono/zod-validator";
  import { z } from "zod";

  const CreateTaskSchema = z.object({
    title: z.string().min(3).max(100).trim(),
    status: z.enum(["pending", "in_progress", "completed"]).default("pending")
  }).strict();

  app.post("/api/tasks", zValidator("json", CreateTaskSchema), async (c) => {
    const data = c.req.valid("json");
    ...
  });
  ```

## 2. Mass Assignment Defense
- Using `.strict()` on Zod schemas guarantees that unexpected extra fields submitted by attackers are rejected with HTTP 400 Bad Request.

## 3. Rate Limiting & Denial of Service Defense
- Impose rate limits on authentication and creation endpoints using in-memory token buckets or sliding windows.
- Set pagination query limits with hard upper bounds (`z.coerce.number().min(1).max(100).default(20)`).

## Fast Testing with Bun Native Test Runner and Mock Requests
# Fast Testing with Bun Native Test Runner and Mock Requests

## 1. Zero-Dependency API Testing
- Test Hono applications directly using `app.request()` without binding to network ports:
  ```typescript
  import { describe, expect, test } from "bun:test";
  import app from "./index";

  describe("API Endpoints", () => {
    test("GET /healthz returns 200 OK JSON", async () => {
      const res = await app.request("/healthz");
      expect(res.status).toBe(200);
      const data = await res.json();
      expect(data.status).toBe("ok");
    });
  });
  ```

## 2. In-Memory Isolated Database Testing
- Unit and integration tests must run against ephemeral in-memory SQLite instances (`new Database(":memory:")`) to ensure hermetic test execution with zero disk pollution.

## 3. Validation and Status Assertions
- Assert both successful 200/201 responses and rejected 400/403/422 payloads with proper error schemas.

