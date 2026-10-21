import { Hono } from "hono";
import { Database } from "bun:sqlite";

const app = new Hono();
const db = new Database("app.db");

db.run(`CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT NOT NULL)`);

app.get("/health", (c) => c.json({ status: "ok", runtime: "bun", framework: "hono", token_light: true }));

app.get("/api/messages", (c) => {
    const rows = db.query("SELECT * FROM messages ORDER BY id DESC LIMIT 50").all();
    return c.json(rows);
});

app.post("/api/messages", async (c) => {
    const { text } = await c.req.json();
    db.run("INSERT INTO messages (text) VALUES (?)", [text]);
    return c.json({ created: true, text }, 201);
});

export default app;
