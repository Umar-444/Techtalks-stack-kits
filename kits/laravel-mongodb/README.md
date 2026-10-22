# Laravel 12 + MongoDB (NoSQL) Stack Kit

[![Stack Status: Ready to Ship](https://img.shields.io/badge/status-Ready%20to%20Ship-emerald?style=flat-square)](kit.yaml)
[![PHP 8.4+](https://img.shields.io/badge/php-8.4%2B-777BB4?style=flat-square)](https://www.php.net/)
[![Laravel 12](https://img.shields.io/badge/laravel-12-FF2D20?style=flat-square)](https://laravel.com/)
[![MongoDB 7.0](https://img.shields.io/badge/mongodb-7.0-47A248?style=flat-square)](https://www.mongodb.com/)
[![Official Driver](https://img.shields.io/badge/mongodb--laravel-5.0-green?style=flat-square)](https://github.com/mongodb/laravel-mongodb)

Pioneer stack combining Laravel 12 with the official `mongodb/laravel-mongodb` package, embedded document relations, aggregation pipeline builders, and NoSQL injection security guardrails.

---

## Architecture Overview

```
                   +-----------------------------------+
                   |         Browser / API Client      |
                   +-----------------+-----------------+
                                     |
                       HTTPS Requests (BSON / JSON)
                                     v
                   +-----------------+-----------------+
                   |       PHP 8.4 Server Core         |
                   |   - NoSQL Injection Sanitization  |
                   |   - ObjectId Validation Gate      |
                   +-----------------+-----------------+
                                     |
                                     v
                   +-----------------+-----------------+
                   |     Laravel 12 Document Layer     |
                   |  - MongoDB\Laravel\Eloquent\Model   |
                   |  - Embedded Documents (embedsMany)|
                   |  - Aggregation Pipeline Builders  |
                   +-----------------+-----------------+
                                     |
                                     v
                   +-----------------+-----------------+
                   |         MongoDB 7.0 Server        |
                   |  - WiredTiger Storage Engine      |
                   |  - Compound B-Tree & GIN Indexes  |
                   +-----------------------------------+
```

---

## Section 3: Installation Guide

### 1. Prerequisites Table
| Tool | Minimum Version | Check Command | Where to Get |
| :--- | :--- | :--- | :--- |
| Docker Engine | 24.0+ | `docker --version` | [docker.com](https://www.docker.com/) |
| Docker Compose | v2.20+ | `docker compose version` | Bundled with Docker Desktop |
| PHP | 8.4+ (with ext-mongodb) | `php -m | grep mongodb` | [php.net](https://www.php.net/) |
| Composer | 2.7+ (optional for native host) | `composer -v` | [getcomposer.org](https://getcomposer.org/) |
| MongoDB Shell | 7.0+ | `mongosh --version` | [mongodb.com](https://www.mongodb.com/) |

### 2. Quickstart Execution
```bash
git clone https://github.com/Umar-444/Techtalks-stack-kits.git
cd Techtalks-stack-kits/kits/laravel-mongodb/starter
cp .env.example .env
docker compose up --build -d
docker compose exec app php artisan key:generate
docker compose exec app php artisan db:seed
```
- API & Analytics: [http://localhost:8000/events](http://localhost:8000/events)
- Health Check Probe: [http://localhost:8000/healthz](http://localhost:8000/healthz)

### 3. Environment Variables
| Variable | Purpose | Example Placeholder |
| :--- | :--- | :--- |
| `APP_ENV` | Application environment state | `local` |
| `APP_KEY` | 32-character AES encryption key | Generated via `artisan key:generate` |
| `APP_DEBUG` | Verbose error stack traces | `true` in local, `false` in production |
| `DB_CONNECTION` | Database driver | `mongodb` |
| `MONGODB_URI` | MongoDB connection string | `mongodb://mongodb:27017/app_mongo` |
| `MONGODB_DATABASE` | MongoDB database name | `app_mongo` |
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
curl -s http://localhost:8000/events | grep "category_stats"
```

### 6. Troubleshooting Matrix
| Symptom | Probable Cause | Fix |
| :--- | :--- | :--- |
| `Class 'MongoDB\Driver\Manager' not found` | Missing ext-mongodb | Rebuild container with PECL mongodb enabled |
| `Connection refused on port 27017` | MongoDB container not started | Check logs: `docker compose logs mongodb` |
| `Authentication failed against admin database` | Missing authSource parameter | Append `?authSource=admin` to MONGODB_URI |
| `Cannot convert string to ObjectId` | Invalid hex ID string | Verify ID format matches `/^[a-f0-9]{24}$/i` |
| `COLLSCAN performance warning` | Missing compound index | Create compound index on queried fields |

### 7. Updating the Kit
When updating:
- Do not overwrite `.env`, models in `app/Models/`, or controllers in `app/Http/Controllers/`.
- Merge updates to `rules/` and `skills/`.

---

## Section 4: Frequently Asked Questions (FAQ)

### 1. What exactly is this kit, and what do I get when I clone it?
This kit is a production-ready NoSQL backend and analytics platform combining Laravel 12 with official MongoDB 7+ support. You get a pre-wired Docker Compose container setup, 6 AI agent rule dialects, 5 operational skills, automated security tests, and an EventLog document analytics starter.

### 2. Which versions does it pin, and why those?
It pins PHP 8.4+, Laravel 12, mongodb/laravel-mongodb 5.0, and MongoDB 7.0+. These versions provide native BSON type support, aggregation pipeline builders, WiredTiger document engine optimization, and long-term security support.

### 3. Which AI coding agents are supported, and how do the rules reach each one?
Claude Code, Cursor, Codex, GitHub Copilot, Cline, and Antigravity are supported via transpiled native dialect targets generated from canonical source rules.

### 4. What do I need installed before I start?
You only need Docker Engine 24+ and Docker Compose v2.20+. All runtime dependencies (PHP 8.4 with ext-mongodb, MongoDB 7.0, Redis 7, Composer) run inside isolated containers.

### 5. How long does installation take, honestly, and what can slow it down?
A fresh install takes between 60 to 90 seconds on a standard broadband connection. Primary bottleneck is compiling the PHP MongoDB PECL driver and pulling base container images.

### 6. Is the starter production-shaped or a demo? What must I change before real production?
The starter is production-shaped with strict security defaults. Before production release, configure authentication on MongoDB with a dedicated app user, set APP_DEBUG=false, and enable TLS for database traffic.

### 7. How is security handled in this kit, and where are its checks?
Security is enforced at multiple layers: NoSQL operator injection sanitization, BSON ObjectId format validation, BOLA document policies, and automated secret scanning. The complete 12-control suite is in security/checks.json.

### 8. Can I change the design? Where do the design tokens live?
Yes. Design tokens are documented in DESIGN.md. Frontend layouts use Tailwind CSS utility tokens and responsive cards.

### 9. How do I update when a new kit version releases?
Review CHANGELOG.md and merge updates to rules/ and skills/. Project-specific document models, controllers, and .env settings remain untouched.

### 10. Can I use it for commercial and client work?
Yes. The entire kit is licensed under the permissive MIT License with zero royalties.

### 11. How do I contribute a fix or a skill back?
Submit a PR to https://github.com/Umar-444/Techtalks-stack-kits adhering to the 18-checkpoint completeness standard.

### 12. Where do I get help or report a problem?
Open an issue on the repository or participate in community discussions at https://techtalks.itsumarfarooq.com.

### 13. Why does this kit use MongoDB instead of a relational database?
MongoDB is ideal for unstructured payloads, flexible event logs, hierarchical telemetry data, and high-frequency writes that do not require rigid tabular schemas.

### 14. Why are there no relational migrations, and how does data modeling work here?
MongoDB is schema-flexible. Document structure is governed at the application layer by Eloquent models and embedded document schemas. Migrations are used exclusively for defining compound indexes and collection validation rules.

---

## License
Maintained by **Umar Farooq** under the MIT License.
