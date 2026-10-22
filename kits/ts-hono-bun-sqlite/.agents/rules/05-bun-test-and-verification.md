# Fast Testing with Bun Native Test Runner and Mock Requests

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
