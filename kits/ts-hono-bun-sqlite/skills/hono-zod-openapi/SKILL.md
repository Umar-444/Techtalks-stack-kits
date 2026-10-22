---
name: hono-zod-openapi
description: Authoring self-documenting type-safe APIs using @hono/zod-openapi and OpenAPI 3.1.
---

# Hono Zod OpenAPI Skill

## Overview
Generate interactive Swagger UI and OpenAPI 3.1 documentation directly from Zod schema definitions without writing YAML manually.

## Pattern
```typescript
import { createRoute, OpenAPIHono, z } from "@hono/zod-openapi";

const app = new OpenAPIHono();

const MessageSchema = z.object({
  id: z.string().uuid(),
  text: z.string().min(1).max(250)
});

const getMessageRoute = createRoute({
  method: "get",
  path: "/api/messages/{id}",
  request: {
    params: z.object({ id: z.string().uuid() })
  },
  responses: {
    200: { content: { "application/json": { schema: MessageSchema } }, description: "Message object" },
    404: { description: "Message not found" }
  }
});
```
