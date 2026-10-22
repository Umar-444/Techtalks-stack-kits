# Laravel 12 + Livewire 4 + PostgreSQL Stack Kit

[![Stack Status: Ready to Ship](https://img.shields.io/badge/status-Ready%20to%20Ship-emerald?style=flat-square)](kit.yaml)
[![PHP 8.4+](https://img.shields.io/badge/php-8.4%2B-777BB4?style=flat-square)](https://www.php.net/)
[![Laravel 12](https://img.shields.io/badge/laravel-12-FF2D20?style=flat-square)](https://laravel.com/)
[![Livewire 4](https://img.shields.io/badge/livewire-4-FB70A9?style=flat-square)](https://livewire.laravel.com/)
[![PostgreSQL 16](https://img.shields.io/badge/postgresql-16-336791?style=flat-square)](https://www.postgresql.org/)

Reactive full-stack TALL stack kit featuring Livewire 4, Volt single-file components, Folio page routing, Flux UI design tokens, Fortify authentication, and PostgreSQL 16+.

---

## Architecture Overview

```
                   +-----------------------------------+
                   |         Browser / Client          |
                   +-----------------+-----------------+
                                     |
                       HTTP / Livewire AJAX Payload
                                     v
                   +-----------------+-----------------+
                   |       PHP 8.4 Server Core         |
                   |   - Livewire Snapshot Checksum    |
                   |   - Session Fixation Protection   |
                   +-----------------+-----------------+
                                     |
                                     v
                   +-----------------+-----------------+
                   |     Livewire 4 Component Layer    |
                   |  - Single-File Volt Components    |
                   |  - Server-Side Action Policies    |
                   |  - DOM Morphing Engine            |
                   +-----------------+-----------------+
                                     |
                                     v
                   +-----------------+-----------------+
                   |         PostgreSQL 16 DB          |
                   |  - UUID Primary Keys              |
                   |  - Composite B-Tree Indexes       |
                   +-----------------------------------+
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

### 2. Quickstart Execution
```bash
git clone https://github.com/Umar-444/Techtalks-stack-kits.git
cd Techtalks-stack-kits/kits/laravel-livewire-postgresql/starter
cp .env.example .env
docker compose up --build -d
docker compose exec app php artisan key:generate
docker compose exec app php artisan migrate --seed
```
- Interactive Livewire UI: [http://localhost:8000/tasks](http://localhost:8000/tasks)
- Health Check Probe: [http://localhost:8000/healthz](http://localhost:8000/healthz)

### 3. Environment Variables
| Variable | Purpose | Example Placeholder |
| :--- | :--- | :--- |
| `APP_ENV` | Application environment state | `local` |
| `APP_KEY` | 32-character AES encryption key | Generated via `artisan key:generate` |
| `APP_DEBUG` | Verbose error stack traces | `true` in local, `false` in production |
| `DB_CONNECTION` | Database driver | `pgsql` |
| `DB_HOST` | Database container host name | `postgres` |
| `DB_PORT` | PostgreSQL TCP port | `5432` |
| `DB_DATABASE` | PostgreSQL database name | `livewire_db` |
| `DB_USERNAME` | Database role | `app_user` |
| `DB_PASSWORD` | Database role secret | `secret_postgres_password` |
| `REDIS_HOST` | Cache and queue host | `redis` |

### 4. Per-Agent Setup
- **Claude Code**: Rules loaded from `CLAUDE.md`.
- **Cursor**: Granular `.mdc` rules auto-applied via `.cursor/rules/*.mdc`.
- **Codex / AGENTS.md**: Contextual instructions in `CODEX.md` and `AGENTS.md`.
- **Copilot**: Global instructions auto-loaded from `.github/copilot-instructions.md`.
- **Cline**: System prompts injected via `.clinerules`.
- **Antigravity**: Workspace rules discovered under `.agents/rules/*.md`.

### 5. Verification Probes
```bash
docker compose ps
curl -s http://localhost:8000/healthz
curl -s http://localhost:8000/tasks | grep "Livewire"
```

### 6. Troubleshooting Matrix
| Symptom | Probable Cause | Fix |
| :--- | :--- | :--- |
| `Livewire snapshot checksum mismatch` | Client-side HTML manipulation | Refresh page to re-initialize token |
| `Connection refused on port 5432` | Port conflict with local PostgreSQL | Change port to `5433:5432` in `docker-compose.yml` |
| `Call to undefined function gen_random_uuid()` | Missing UUID extension | Run `CREATE EXTENSION IF NOT EXISTS "uuid-ossp";` |
| `Livewire actions not firing` | Missing script tags | Ensure `@livewireScripts` is in Blade layout |
| `Vite manifest not found` | Assets uncompiled | Run `npm install && npm run build` |

### 7. Updating the Kit
When updating:
- Do not overwrite `.env`, models in `app/Models/`, or views in `resources/views/`.
- Merge updates to `rules/` and `skills/`.

---

## Section 4: Frequently Asked Questions (FAQ)

### 1. What exactly is this kit, and what do I get when I clone it?
This kit is a reactive full-stack TALL stack application combining Laravel 12, Livewire 4, and PostgreSQL 16. You get a pre-wired Docker Compose container setup, 6 AI agent rule dialects, 5 operational skills, automated architectural tests, and a reactive real-time Task Manager component.

### 2. Which versions does it pin, and why those?
It pins PHP 8.4+, Laravel 12, Livewire 4, and PostgreSQL 16+. These versions deliver native UUID support, single-file Volt components, morphdom diffing, and long-term security support.

### 3. Which AI coding agents are supported, and how do the rules reach each one?
Claude Code, Cursor, Codex, GitHub Copilot, Cline, and Antigravity are supported via transpiled native dialect targets generated from canonical source rules.

### 4. What do I need installed before I start?
You only need Docker Engine 24+ and Docker Compose v2.20+. All runtime dependencies (PHP 8.4, PostgreSQL 16, Redis 7, Composer) run inside isolated containers.

### 5. How long does installation take, honestly, and what can slow it down?
A fresh install takes between 60 to 90 seconds on a standard broadband connection. Primary bottleneck is pulling base Alpine container images.

### 6. Is the starter production-shaped or a demo? What must I change before real production?
The starter is production-shaped with strict security defaults. Before production release, rotate default database credentials, set APP_DEBUG=false, generate a unique APP_KEY, and configure SSL termination.

### 7. How is security handled in this kit, and where are its checks?
Security is enforced at multiple layers: Argon2id password hashing, component property checksum validation, BOLA authorization policies, and automated secret scanning. The complete 12-control suite is in security/checks.json.

### 8. Can I change the design? Where do the design tokens live?
Yes. Design tokens are documented in DESIGN.md. You can customize Tailwind CSS classes directly in Blade layouts and Flux UI components.

### 9. How do I update when a new kit version releases?
Review the CHANGELOG.md and merge updates to rules/ and skills/. Project-specific models, views, and .env settings remain untouched.

### 10. Can I use it for commercial and client work?
Yes. The kit is licensed under the permissive MIT License with zero royalties.

### 11. How do I contribute a fix or a skill back?
Submit a PR to https://github.com/Umar-444/Techtalks-stack-kits adhering to the 18-checkpoint completeness standard.

### 12. Where do I get help or report a problem?
Open an issue on the repository or participate in community discussions at https://techtalks.itsumarfarooq.com.

### 13. How does Livewire 4 prevent parameter tampering?
Livewire signs all public component properties with an HMAC checksum on every request. Any client-side DOM tampering causes an immediate checksum mismatch exception.

### 14. Why does this kit use PostgreSQL instead of MySQL?
PostgreSQL provides native UUID generation functions, robust JSONB querying with GIN indexing, and superior connection pooling under high concurrent Livewire event traffic.

---

## License
Maintained by **Umar Farooq** under the MIT License.
