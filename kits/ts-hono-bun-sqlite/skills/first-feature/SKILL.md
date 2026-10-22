---
name: first-feature
description: Guide for adding a new type-safe resource endpoint with Drizzle schema and Zod validation.
---

# First Feature Skill: Adding a Typed Task Resource

## Overview
Walkthrough for adding a typed `tasks` resource to Hono using Drizzle ORM and Zod request validation.

## Implementation Steps

### 1. Define Drizzle Table in `src/db/schema.ts`
```typescript
import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core";

export const tasks = sqliteTable("tasks", {
  id: text("id").primaryKey(),
  title: text("title").notNull(),
  status: text("status").notNull().default("pending"),
  createdAt: integer("created_at", { mode: "timestamp" }).notNull()
});
```

### 2. Define Zod Schemas
```typescript
import { z } from "zod";

export const CreateTaskSchema = z.object({
  title: z.string().min(3).max(100).trim(),
  status: z.enum(["pending", "in_progress", "completed"]).default("pending")
}).strict();
```

### 3. Register Route in `src/index.ts`
```typescript
app.post("/api/tasks", zValidator("json", CreateTaskSchema), async (c) => {
  const data = c.req.valid("json");
  const newTask = {
    id: crypto.randomUUID(),
    title: data.title,
    status: data.status,
    createdAt: new Date()
  };
  await db.insert(tasks).values(newTask);
  return c.json(newTask, 201);
});
```

### 4. Write Integration Test
```typescript
test("POST /api/tasks creates task", async () => {
  const res = await app.request("/api/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title: "Build feature with Hono" })
  });
  expect(res.status).toBe(201);
  const body = await res.json();
  expect(body.title).toBe("Build feature with Hono");
});
```
