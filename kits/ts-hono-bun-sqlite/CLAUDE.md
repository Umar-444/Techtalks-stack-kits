# Assistant Guidelines for Hono + Bun + SQLite Stack Kit

## Stack Overview
- Language: TypeScript 5.6+
- Framework: Hono 4.6+
- Runtime: Bun 1.1+ (native SQLite & fast test runner)
- ORM: Drizzle ORM 0.35+ (schema migrations & typed queries)
- Database: SQLite / LibSQL (with WAL mode enabled)
- Validation: Zod 3.23+ with strict schemas

## Mandatory Rules
1. Zero unparameterized SQL queries. Always use bind parameters or Drizzle query builder.
2. Initialize SQLite with WAL mode (`PRAGMA journal_mode = WAL;`) and synchronous NORMAL.
3. Validate all request inputs (JSON, query, params) using Zod schemas with `.strict()`.
4. Run tests with Bun's native test runner (`bun test`) using `app.request()` for fast mock execution.
5. All JSON responses must adhere to strict type contracts.
