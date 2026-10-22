# Laravel 13 + Filament 4 + PostgreSQL Stack Kit

[![Stack Status: Ready to Ship](https://img.shields.io/badge/status-Ready%20to%20Ship-emerald?style=flat-square)](kit.yaml)
[![PHP 8.4+](https://img.shields.io/badge/php-8.4%2B-777BB4?style=flat-square)](https://www.php.net/)
[![Laravel 13](https://img.shields.io/badge/laravel-13-FF2D20?style=flat-square)](https://laravel.com/)
[![Filament 4](https://img.shields.io/badge/filament-4-FFA000?style=flat-square)](https://filamentphp.com/)
[![PostgreSQL 16](https://img.shields.io/badge/postgresql-16-336791?style=flat-square)](https://www.postgresql.org/)

Production-ready administrative platform and SaaS backend kit. Bundles verified Laravel 13, Filament 4 panels, strict PostgreSQL 16+ schema conventions, granular BOLA authorization policies, and automated AI security guardrails.

---

## Architecture Overview

```
                   +-----------------------------------+
                   |         Browser / Admin           |
                   +-----------------+-----------------+
                                     |
                       HTTPS Requests (Filament Panel)
                                     v
                   +-----------------+-----------------+
                   |     Nginx / PHP 8.4 CLI Server    |
                   |   - Session Fixation Protection   |
                   |   - Secure Cookie Middleware      |
                   +-----------------+-----------------+
                                     |
                                     v
                   +-----------------+-----------------+
                   |      Laravel 13 Application       |
                   |  - Filament Panel Providers       |
                   |  - Granular Model Policies (BOLA) |
                   |  - UUID Model Primary Keys        |
                   +-----------------+-----------------+
                                     |
                                     +---------------------------------+
                                     |                                 |
                         PostgreSQL 16 PDO Pool                Redis 7 Queue/Cache
                                     v                                 v
                   +-----------------+-----------------+ +-------------+-------------+
                   |         PostgreSQL 16 DB          | |       Redis 7 Daemon      |
                   |  - UUID extension (uuid-ossp)     | |  - Horizon Job Queues     |
                   |  - Composite B-Tree Indexes       | |  - Fast Session Caching   |
                   +-----------------------------------+ +---------------------------+
```

---

## Section 3: Installation Guide

### 1. Prerequisites Table
| Tool | Minimum Version | Check Command | Where to Get |
| :--- | :--- | :--- | :--- |
| Docker Engine | 24.0+ | `docker --version` | [docker.com](https://www.docker.com/) |
| Docker Compose | v2.20+ | `docker compose version` | Bundled with Docker Desktop |
| PHP | 8.4+ (optional for native host) | `php -v` | [php.net](https://www.php.net/) |
| Composer | 2.7+ (optional for native host) | `composer -v` | [getcomposer.org](https://getcomposer.org/) |
| PostgreSQL Client | 16+ | `pg_isready --version` | [postgresql.org](https://www.postgresql.org/) |

### 2. Quickstart
```bash
# 1. Clone repository and navigate to starter
git clone https://github.com/Umar-444/Techtalks-stack-kits.git
cd Techtalks-stack-kits/kits/laravel-filament-postgresql/starter

# 2. Boot environment via Docker Compose
cp .env.example .env
docker compose up --build -d

# 3. Initialize database and seed administrator
docker compose exec app php artisan key:generate
docker compose exec app php artisan migrate --seed
```
- Admin Panel: [http://localhost:8000/admin](http://localhost:8000/admin) (Email: `admin@example.com`, Password: `Secret123!`)
- Health Probe: [http://localhost:8000/healthz](http://localhost:8000/healthz)

### 3. Full Installation & Environment Variables
| Variable | Purpose | Example Placeholder |
| :--- | :--- | :--- |
| `APP_ENV` | Application environment state | `local` |
| `APP_KEY` | 32-character AES encryption key | Generated via `artisan key:generate` |
| `APP_DEBUG` | Verbose error stack traces | `true` in local, `false` in production |
| `DB_CONNECTION` | Database driver | `pgsql` |
| `DB_HOST` | Database container host name | `postgres` |
| `DB_PORT` | PostgreSQL TCP port | `5432` |
| `DB_DATABASE` | PostgreSQL database name | `app_production` |
| `DB_USERNAME` | Database role | `app_user` |
| `DB_PASSWORD` | Database role secret | `secret_postgres_password` |
| `REDIS_HOST` | Cache and queue host | `redis` |

### 4. Per-Agent Setup
- **Claude Code**: Rules automatically loaded from `CLAUDE.md`.
- **Cursor**: Granular `.mdc` rules auto-applied via `.cursor/rules/*.mdc`.
- **Codex / AGENTS.md**: Contextual instructions in `CODEX.md` and `AGENTS.md`.
- **Copilot**: Global instructions auto-loaded from `.github/copilot-instructions.md`.
- **Cline**: System prompts injected via `.clinerules`.
- **Antigravity**: Workspace rules discovered under `.agents/rules/*.md`.

### 5. Verification Checks
```bash
# 1. Check services
docker compose ps

# 2. Verify health probe
curl -s http://localhost:8000/healthz

# 3. Run architectural tests
docker compose exec app ./vendor/bin/pest tests/ArchTest.php
```

### 6. Troubleshooting
| Symptom | Likely Cause | Fix |
| :--- | :--- | :--- |
| `could not translate host name "postgres"` | App container disconnected from Compose network | Run `docker compose down -v && docker compose up --build -d` |
| `Connection refused on port 5432` | Host port conflict with existing local PostgreSQL | Change port to `5433:5432` in `docker-compose.yml` |
| `Call to undefined function gen_random_uuid()` | PostgreSQL UUID extension missing | Run `CREATE EXTENSION IF NOT EXISTS "uuid-ossp";` |
| `Filament assets returning 404` | Missing published asset symlinks | Run `docker compose exec app php artisan filament:assets` |
| `Permission denied storage/framework` | Storage folder permissions | Run `docker compose exec app chown -R www-data:www-data storage` |

### 7. Updating the Kit
When pulling a newer version of the kit, do not overwrite:
- `.env` and environment configurations.
- `app/` domain code and bespoke business models.
- Custom migrations in `database/migrations/`.
Safe to update:
- Agent rules in `.cursor/rules/`, `CLAUDE.md`, and `rules/source/`.
- Reusable skills in `skills/`.

---

## Section 4: Frequently Asked Questions (FAQ)

### 1. What exactly is this kit, and what do I get when I clone it?
This kit is a production-grade administrative and SaaS backend combining Laravel 13, Filament 4, and PostgreSQL 16. You get a pre-configured Docker Compose container stack, 6 AI agent rule dialects, 6 operational skills, automated architectural assertions, and a runnable Customer management starter.

### 2. Which versions does it pin, and why those?
It pins PHP 8.4+, Laravel 13, Filament 4, and PostgreSQL 16+. These versions were chosen because they provide native UUID v7 support, compile-time property types, enhanced JSONB indexing, and long-term security support.

### 3. Which AI coding agents are supported, and how do rules reach each one?
All six major AI agent ecosystems are supported: Claude Code, Cursor, Codex, GitHub Copilot, Cline, and Antigravity. Rules are transpiled from a single canonical source in `rules/source/` into each agent's native format.

### 4. What do I need installed before I start?
You only need Docker Engine 24+ and Docker Compose v2.20+. All runtime dependencies (PHP 8.4, PostgreSQL 16, Redis 7, Composer) run inside isolated containers.

### 5. How long does installation take, honestly, and what can slow it down?
A fresh install takes approximately 60 to 90 seconds on a standard broadband connection. The primary bottleneck is pulling the Alpine base container images and running Composer dependency installation.

### 6. Is the starter production-shaped or a demo? What must I change before production?
The starter is production-shaped with strict security defaults. Before deploying to live production, you must rotate default database credentials, set `APP_DEBUG=false`, generate a unique `APP_KEY`, and enable SSL termination.

### 7. How is security handled in this kit, and where are its checks?
Security is enforced at multiple layers: Argon2id password hashing, secure session cookie flags, BOLA authorization policies, and automated secret scanning. The complete 12-control verification suite is defined in `security/checks.json`.

### 8. Can I change the design? Where do the design tokens live?
Yes. The design system is documented in `DESIGN.md`. You can customize Filament panel colors, typography tokens, and brand accents in `app/Providers/Filament/AdminPanelProvider.php`.

### 9. How do I update when a new kit version releases?
Review the kit's `CHANGELOG.md` and selectively merge updates to `rules/` and `skills/`. Your project-specific models, migrations, and `.env` file should remain untouched.

### 10. Can I use it for commercial and client work?
Yes. The entire kit is licensed under the permissive MIT License, allowing commercial, internal, and proprietary client use with zero royalties.

### 11. How do I contribute a fix or a skill back?
Submit a pull request to the `https://github.com/Umar-444/Techtalks-stack-kits` repository following the guidelines in `CONTRIBUTING.md`. Ensure all Pest architectural tests and Semgrep scans pass.

### 12. Where do I get help or report a problem?
Open an issue on the GitHub repository or consult the TechTalks community discussions at `https://techtalks.itsumarfarooq.com`.

### 13. Why does this kit enforce UUIDs for all primary keys?
UUID primary keys prevent sequential ID enumeration attacks, allow safe client-side ID generation, and simplify distributed multi-tenant database partitioning.

### 14. How does multi-tenant authorization work in this kit?
Every Filament resource is paired with a strict Laravel Policy that verifies the authenticated user's organization ownership before permitting view, update, or delete operations.

---

## License
Maintained by **Umar Farooq** under the MIT License.
