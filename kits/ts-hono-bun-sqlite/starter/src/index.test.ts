import { expect, test } from "bun:test";
import app from "./index";

test("GET /health returns 200 OK", async () => {
    const res = await app.request("/health");
    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body.status).toBe("ok");
    expect(body.token_light).toBe(true);
});
