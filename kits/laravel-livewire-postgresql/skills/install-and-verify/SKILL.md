---
name: install-and-verify
description: Install, orchestrate, and verify the Laravel 12 + Livewire 4 + PostgreSQL reactive application.
---

# Install & Verify Skill: Laravel + Livewire + PostgreSQL

## Prerequisites
- Docker Engine 24+ and Docker Compose v2.20+
- PHP 8.4+ (optional for native host setup)
- Composer 2.7+
- Node.js 20+ & npm (for Vite assets)

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

## Post-Install Verification Probes
1. Verify container runtime health:
   ```bash
   docker compose ps
   ```
   Expected: `app`, `postgres`, and `redis` containers are all healthy.

2. Verify health check endpoint:
   ```bash
   curl -s http://localhost:8000/healthz
   ```
   Expected: `{"status":"ok","app":"laravel-livewire-postgresql","version":"1.0.0"}` with HTTP 200 OK.

3. Verify Livewire application UI:
   ```bash
   curl -s http://localhost:8000/tasks | grep "Livewire"
   ```
   Expected: Matches rendered Livewire component HTML.

## Failure-Recovery Matrix
| Symptom | Probable Cause | Resolution |
| :--- | :--- | :--- |
| `Livewire property [$task] not allowed on component` | Direct Eloquent model exposure without Cast | Cast to array, DTO, or bind model ID with explicit resolver |
| `SQLSTATE[08006] Connection refused on port 5432` | Local PostgreSQL port conflict on host | Change port mapping in `docker-compose.yml` to `5433:5432` |
| `Livewire snapshot checksum mismatch` | Client-side HTML manipulation or stale CSRF | Refresh page to re-initialize Livewire component snapshot token |
| `Call to undefined function gen_random_uuid()` | PostgreSQL UUID extension missing | Execute `CREATE EXTENSION IF NOT EXISTS "uuid-ossp";` |
| `Livewire actions not firing on click` | Missing `@livewireScripts` in Blade layout | Verify `resources/views/layouts/app.blade.php` includes `@livewireScripts` |
| `Vite manifest not found` | Frontend assets not compiled | Run `npm install && npm run build` inside container |

## Done Means
The application boots cleanly via Docker Compose, migrations apply to PostgreSQL 16, `/healthz` responds with HTTP 200 OK, and the `/tasks` Livewire component responds interactively to clicks and input bindings.
