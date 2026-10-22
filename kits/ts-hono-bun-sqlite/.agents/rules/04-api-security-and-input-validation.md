# Zod Schema Validation, Input Sanitization, and API Security

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
