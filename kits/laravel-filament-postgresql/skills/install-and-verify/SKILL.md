---
name: install-and-verify
description: Install, configure, and verify the Laravel 13 + Filament 4 + PostgreSQL multi-container stack.
---

# Install & Verify Skill: Laravel + Filament + PostgreSQL

## Prerequisites
- Docker Engine 24+ and Docker Compose v2.20+
- PHP 8.4+ (if running natively without Docker)
- Composer 2.7+
- PostgreSQL 16+ client utilities (`pg_isready`)

## OS-Specific Commands

### Linux (Ubuntu / Debian)
```bash
sudo apt-get update && sudo apt-get install -y docker-compose-plugin postgresql-client
cp .env.example .env
docker compose up --build -d
docker compose exec app php artisan key:generate
docker compose exec app php artisan migrate --seed
```

### macOS (Homebrew)
```bash
brew install docker docker-compose libpq
cp .env.example .env
docker compose up --build -d
docker compose exec app php artisan key:generate
docker compose exec app php artisan migrate --seed
```

### Windows (PowerShell / WSL2)
```powershell
Copy-Item .env.example .env
docker compose up --build -d
docker compose exec app php artisan key:generate
docker compose exec app php artisan migrate --seed
```

## Post-Install Verification Checks
1. Verify container runtime health:
   ```bash
   docker compose ps
   ```
   Expected: `filament_app`, `filament_postgres`, and `filament_redis` are all `Up` and `healthy`.

2. Verify HTTP health check endpoint:
   ```bash
   curl -s http://localhost:8000/healthz
   ```
   Expected: `{"status":"ok","app":"laravel-filament-postgresql","version":"1.0.0"}` with HTTP 200 OK.

3. Verify Filament admin panel:
   ```bash
   curl -s -L http://localhost:8000/admin/login | grep "Filament"
   ```
   Expected: Matches the Filament authentication form HTML.

4. Verify PostgreSQL connection & UUID extension:
   ```bash
   docker compose exec app php artisan db:monitor
   ```
   Expected: Database connection healthy, zero pending migrations.

## Failure-Recovery Matrix
| Symptom | Probable Cause | Resolution |
| :--- | :--- | :--- |
| `could not translate host name "postgres"` | App container not attached to Compose bridge network | Run `docker compose down -v && docker compose up --build -d` |
| `SQLSTATE[08006] [7] Connection refused on port 5432` | Local host port 5432 conflict with native PostgreSQL instance | Change port mapping in `docker-compose.yml` to `5433:5432` or stop host service |
| `Function gen_random_uuid() does not exist` | PostgreSQL `uuid-ossp` or `pgcrypto` extension uninitialized | Run `CREATE EXTENSION IF NOT EXISTS "uuid-ossp";` via `psql` |
| `Filament assets returning 404 Not Found` | Asset symlinks unlinked in production container | Run `docker compose exec app php artisan filament:assets` |
| `Composer memory exhaustion during install` | Memory limit too low in native PHP CLI | Prepend `COMPOSER_MEMORY_LIMIT=-1 composer install` |
| `Permission denied storage/framework/sessions` | Container user ID mismatch with host mount | Run `docker compose exec app chown -R www-data:www-data storage bootstrap/cache` |

## Done Means
The application boots cleanly via Docker Compose, database migrations and seeds complete with zero errors, `/healthz` returns HTTP 200 OK, and `/admin` displays the Filament login interface.
