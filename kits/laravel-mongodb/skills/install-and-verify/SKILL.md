---
name: install-and-verify
description: Install, configure, and verify the Laravel 12 + MongoDB 7+ multi-container application.
---

# Install & Verify Skill: Laravel + MongoDB

## Prerequisites
- Docker Engine 24+ and Docker Compose v2.20+
- PHP 8.4+ with `mongodb` extension enabled (optional for native host setup)
- Composer 2.7+
- MongoDB 7.0+ (`mongosh` utility)

## OS-Specific Commands

### Linux (Ubuntu / Debian)
```bash
sudo apt-get update && sudo apt-get install -y docker-compose-plugin
cp .env.example .env
docker compose up --build -d
docker compose exec app php artisan key:generate
docker compose exec app php artisan db:seed
```

### macOS (Homebrew)
```bash
brew install docker docker-compose mongosh
cp .env.example .env
docker compose up --build -d
docker compose exec app php artisan key:generate
docker compose exec app php artisan db:seed
```

### Windows (PowerShell / WSL2)
```powershell
Copy-Item .env.example .env
docker compose up --build -d
docker compose exec app php artisan key:generate
docker compose exec app php artisan db:seed
```

## Post-Install Verification Probes
1. Verify container runtime health:
   ```bash
   docker compose ps
   ```
   Expected: `app` and `mongodb` containers are healthy and running.

2. Verify health check endpoint:
   ```bash
   curl -s http://localhost:8000/healthz
   ```
   Expected: `{"status":"ok","app":"laravel-mongodb","version":"1.0.0"}` with HTTP 200 OK.

3. Verify MongoDB connection & document querying:
   ```bash
   curl -s http://localhost:8000/events
   ```
   Expected: Returns JSON document list with aggregate statistics.

## Failure-Recovery Matrix
| Symptom | Probable Cause | Resolution |
| :--- | :--- | :--- |
| `Class 'MongoDB\Driver\Manager' not found` | PHP mongodb PECL extension missing | Ensure `pecl install mongodb && docker-php-ext-enable mongodb` in Dockerfile |
| `MongoConnectionException: Connection refused on port 27017` | MongoDB container not started or wrong host | Verify `DB_HOST=mongodb` and check container status with `docker compose ps` |
| `Authentication failed against admin database` | Missing or incorrect auth credentials | Set `authSource=admin` in MongoDB connection string or URI |
| `Cannot convert string to ObjectId` | Invalid 24-character hexadecimal string supplied | Validate input using `preg_match('/^[a-f0-9]{24}$/i', $id)` before casting |
| `16MB document size exceeded exception` | Unbounded embedded array growth | Refactor schema from `embedsMany` to referenced collection relationship |
| `Full collection scan (COLLSCAN) performance warning` | Missing compound index on queried attributes | Create compound index via migration or `raw(function($collection) { ... })` |

## Done Means
The application boots cleanly via Docker Compose, MongoDB 7 connection establishes without authentication errors, `/healthz` returns HTTP 200 OK, and `/events` queries and aggregates documents successfully.
