# Next.js 15+ + Prisma ORM + PostgreSQL + Tailwind CSS Blueprint Kit

A production-grade full-stack TypeScript kit combining Next.js 15 App Router, React 19 Server Components, Server Actions with runtime Zod validation, Prisma ORM schema migrations, PostgreSQL 16 connection pooling, and rootless multi-stage container isolation.

---

## 1. Architecture Overview

```
                      +---------------------------------------+
                      |         Web Browser / Mobile          |
                      +---------------------------------------+
                                          |
                                          | HTTPS / HTTP2 (Port 3000)
                                          v
+-----------------------------------------------------------------------------------+
| App Container (Node.js 22 LTS Alpine - UID 10001:10001 Rootless)                   |
|                                                                                   |
|  +----------------------------+     +------------------------------------------+  |
|  | React 19 Server Components |     | Next.js 15 App Router                    |  |
|  | - Streaming SSR & Suspense |     | - Type-safe Server Actions (Zod-guarded) |  |
|  | - Static & Dynamic Pages   | <-> | - Route Handlers (/api/health)           |  |
|  +----------------------------+     | - Global PrismaClient Singleton          |  |
|                                     +------------------------------------------+  |
+-----------------------------------------------------------------------------------+
                                          |
                                          | SQL / Wire Protocol (Port 5432)
                                          v
+-----------------------------------------------------------------------------------+
| PostgreSQL 16 Database                                                            |
| - Connection Pooling with max 20 connections per container instance               |
| - Declarative Prisma Migrations (prisma/migrations/)                             |
| - Composite Foreign Key & Tenant Isolation Indexes                                |
+-----------------------------------------------------------------------------------+
```

---

## 2. Quickstart

```bash
# 1. Clone repository
git clone https://github.com/Umar-444/Techtalks-stack-kits.git
cd Techtalks-stack-kits/kits/nextjs-prisma-postgresql/starter

# 2. Configure environment
cp .env.example .env

# 3. Spin up rootless container stack
docker compose up -d --build

# 4. Run Prisma database migrations & seeders
docker compose exec app npx prisma migrate deploy
docker compose exec app npm run db:seed

# 5. Execute test suite
docker compose exec app npm test
```

---

## 3. Seven-Part OS Installation Guide

### Part 1: Prerequisites
- Docker Engine 26+ and Docker Compose v2.27+
- Node.js 22 LTS with `npm` or `pnpm`
- PostgreSQL 16 client tools

### Part 2: macOS Setup (Homebrew)
```bash
brew install node@22 postgresql@16
npm install -g pnpm prisma
```

### Part 3: Ubuntu / Debian Setup
```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs postgresql-client
```

### Part 4: Fedora / RHEL Setup
```bash
sudo dnf install -y nodejs postgresql
```

### Part 5: Arch Linux Setup
```bash
sudo pacman -S nodejs npm postgresql-libs
```

### Part 6: Windows (WSL2 Ubuntu)
```bash
wsl --install -d Ubuntu
sudo apt-get update && sudo apt-get install -y nodejs npm
```

### Part 7: Verification Command
```bash
curl -f http://localhost:3000/api/health || exit 1
```

---

## 4. Skills Inventory

| Skill Name | Purpose | Location |
|---|---|---|
| `install-and-verify` | Boot environment, run Prisma migrations, verify probes | `skills/install-and-verify/SKILL.md` |
| `first-feature` | Project & Task management module with Server Actions & Zod | `skills/first-feature/SKILL.md` |
| `prisma-schema-migrations` | Prisma migrate, relation design, composite indexes | `skills/prisma-schema-migrations/SKILL.md` |
| `server-actions-zod` | Safe Server Actions with runtime Zod validation | `skills/server-actions-zod/SKILL.md` |
| `prisma-multi-tenant-isolation` | Tenant boundary scoping & authorization middleware | `skills/prisma-multi-tenant-isolation/SKILL.md` |
| `nextjs-prisma-postgresql-core` | Operational workflows, Prisma Studio, dev scripts | `skills/nextjs-prisma-postgresql-core/SKILL.md` |

---

## 5. Security & Verification Evidence

All 18 checkpoints verified in `VERIFICATION.md`. Zero-drift transpiled across all 6 AI coding agent formats.
