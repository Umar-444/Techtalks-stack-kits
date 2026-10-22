---
name: install-and-verify
description: Install, configure, and verify the Laravel 12/13 + AI Features + pgvector stack with healthchecks.
---

# Skill: Install and Verify

## 1. Multi-OS Installation Commands

### macOS (Homebrew)
```bash
brew install php@8.3 composer libpq redis
cp .env.example .env
composer install
php artisan key:generate
docker compose up -d postgres redis
php artisan migrate --seed
```

### Ubuntu / Debian
```bash
sudo apt-get update && sudo apt-get install -y php8.3-cli php8.3-pgsql composer
cp .env.example .env
composer install
docker compose up -d
php artisan migrate --seed
```

### Windows (WSL2)
```bash
wsl --install -d Ubuntu
sudo apt-get update && sudo apt-get install -y php8.3-cli php8.3-pgsql composer
cp .env.example .env
docker compose up -d
php artisan migrate --seed
```

## 2. Five-Row Failure Recovery Table

| Error / Failure Symptom | Underlying Cause | Concrete Recovery Command |
|---|---|---|
| `type "vector" does not exist` | pgvector extension not enabled | `docker compose exec postgres psql -U postgres -d laravel_ai -c "CREATE EXTENSION IF NOT EXISTS vector;"` |
| `Connection refused on port 6379` | Redis service not ready | `docker compose exec redis redis-cli ping` |
| `HNSW index build exceeds memory` | maintenance_work_mem too small | Set `maintenance_work_mem = '64MB'` in PostgreSQL configuration |
| `OpenAI API 401 Unauthorized` | Missing or invalid API key | Set `AI_PROVIDER=mock` in `.env` for local testing |
| `Permission denied on storage/logs` | Non-root container UID mismatch | `docker compose exec app chown -R 10001:10001 storage bootstrap/cache` |

## 3. Done Means
- `curl -f http://localhost:8000/api/health` returns HTTP 200 with JSON status `ok`.
- PostgreSQL pgvector extension enabled and migrations executed.
- `php artisan test` exits with code 0.
