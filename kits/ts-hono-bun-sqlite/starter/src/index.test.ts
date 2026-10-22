import { describe, expect, test } from "bun:test";
import app from "./index";

describe("Hono + Bun + SQLite API Suite", () => {
  test("GET /healthz returns 200 OK JSON", async () => {
    const res = await app.request("/healthz");
    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body.status).toBe("ok");
    expect(body.app).toBe("ts-hono-bun-sqlite");
    expect(body.runtime).toBe("bun");
  });

  test("GET /health legacy endpoint returns 200", async () => {
    const res = await app.request("/health");
    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body.status).toBe("ok");
  });

  test("POST /api/messages creates message with valid payload", async () => {
    const res = await app.request("/api/messages", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: "Hello from Bun and Hono!" })
    });
    expect(res.status).toBe(201);
    const body = await res.json();
    expect(body.created).toBe(true);
    expect(body.message.text).toBe("Hello from Bun and Hono!");
    expect(body.message.id).toBeDefined();
  });

  test("POST /api/messages rejects invalid empty payload with 400", async () => {
    const res = await app.request("/api/messages", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: "" })
    });
    expect(res.status).toBe(400);
  });

  test("POST /api/messages rejects unexpected extra fields (mass assignment)", async () => {
    const res = await app.request("/api/messages", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: "Valid text", is_admin: true })
    });
    expect(res.status).toBe(400);
  });

  test("GET /api/messages retrieves messages within pagination limits", async () => {
    const res = await app.request("/api/messages?limit=10");
    expect(res.status).toBe(200);
    const body = await res.json();
    expect(Array.isArray(body.data)).toBe(true);
    expect(body.limit).toBe(10);
  });
});
