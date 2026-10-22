# Drizzle ORM Schema Discipline and Typed Migrations

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
