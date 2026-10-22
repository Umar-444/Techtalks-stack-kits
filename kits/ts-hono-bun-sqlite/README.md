# TypeScript + Hono + Bun + SQLite (Drizzle ORM) Stack Kit

An ultra-lightweight, sub-millisecond full-stack TypeScript API kit built with **Hono**, **Bun**, and native **SQLite** in Write-Ahead Logging (WAL) mode.

## Stack Overview
- **Language**: TypeScript 5.6+
- **Framework**: Hono 4.6+ (Trie-based RegExpRouter)
- **Runtime**: Bun 1.1+ (Built-in SQLite & native test runner)
- **Database & ORM**: SQLite / LibSQL with Drizzle ORM 0.35+
- **Validation**: Zod 3.23+ with strict request schemas
- **Container**: Multi-stage Alpine container running as non-root `bun` user

## Quickstart

### 1. Install & Run Tests
```bash
bun install
bun test
```

### 2. Run Development Server
```bash
bun run dev
```
Visit `http://localhost:3000/healthz` to verify live status.

### 3. Run with Docker Compose
```bash
docker compose up --build
```

## Security & Verification Standards
- Strict prepared statements eliminate SQL injection risks.
- SQLite WAL mode guarantees high concurrent throughput without database lock contention.
- Fully documented in [`VERIFICATION.md`](VERIFICATION.md).
