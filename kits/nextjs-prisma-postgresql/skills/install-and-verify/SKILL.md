---
name: install-and-verify
description: Install, configure, and verify the Next.js 15 + Prisma + PostgreSQL stack with Docker and healthchecks.
---

# Skill: Install and Verify

## 1. Multi-OS Installation Commands

### macOS (Homebrew)
```bash
brew install node@22 postgresql@16
npm install
cp .env.example .env
docker compose up -d postgres
npx prisma migrate dev
npm test
```

### Ubuntu / Debian
```bash
sudo apt-get update && sudo apt-get install -y nodejs postgresql-client
npm install
cp .env.example .env
docker compose up -d
npx prisma migrate deploy
npm test
```

### Windows (WSL2)
```bash
wsl --install -d Ubuntu
sudo apt-get update && sudo apt-get install -y nodejs npm
npm install
cp .env.example .env
docker compose up -d
npx prisma migrate deploy
npm test
```

## 2. Five-Row Failure Recovery Table

| Error / Failure Symptom | Underlying Cause | Concrete Recovery Command |
|---|---|---|
| `Can't reach database server at postgres:5432` | PostgreSQL container still initializing | `docker compose exec postgres pg_isready -h localhost -U postgres` |
| `PrismaClientInitializationError: Connection pool timeout` | Max pool connections exhausted | Set `connection_limit=20` in `DATABASE_URL` query string |
| `EACCES: permission denied, mkdir '.next'` | Non-root container UID mismatch | `docker compose exec app chown -R 10001:10001 .next node_modules` |
| `Invalid `prisma.project.create()` invocation` | Missing required foreign key or constraint | Review `prisma/schema.prisma` and ensure parent record exists |
| `Hydration failed because initial UI does not match` | Client/server rendering time/date mismatch | Use `suppressHydrationWarning` on dynamic date elements |

## 3. Done Means
- `curl -f http://localhost:3000/api/health` returns HTTP 200 with JSON status `ok`.
- Prisma migrations deployed cleanly with 0 pending migrations.
- `npm test` exits with code 0.
