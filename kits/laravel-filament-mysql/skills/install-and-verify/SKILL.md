---
name: install-and-verify
description: Install, configure, and verify the Laravel 12/13 + Filament 4 + MySQL 8.4 LTS stack with healthchecks.
---

# Skill: Install and Verify

## 1. Multi-OS Installation Commands

### macOS (Homebrew)
```bash
brew install php@8.3 composer mysql-client redis
cp .env.example .env
composer install
php artisan key:generate
docker compose up -d mysql redis
php artisan migrate --seed
```

### Ubuntu / Debian
```bash
sudo apt-get update && sudo apt-get install -y php8.3-cli php8.3-mysql composer
cp .env.example .env
composer install
docker compose up -d
php artisan migrate --seed
```

### Windows (WSL2)
```bash
wsl --install -d Ubuntu
sudo apt-get update && sudo apt-get install -y php8.3-cli php8.3-mysql composer
cp .env.example .env
docker compose up -d
php artisan migrate --seed
```

## 2. Five-Row Failure Recovery Table

| Error / Failure Symptom | Underlying Cause | Concrete Recovery Command |
|---|---|---|
| `SQLSTATE[HY000] [2002] Connection refused` | MySQL container still initializing | `docker compose exec mysql mysqladmin ping -h 127.0.0.1 -u root -psecret --silent` |
| `ERROR 1213 (40001): Deadlock found` | Concurrent lock conflict on InnoDB row | Wrap in `DB::transaction(fn() => ..., 3)` with retry backoff |
| `The stream or file "laravel.log" could not be opened: Permission denied` | Storage directory permission mismatch | `docker compose exec app chown -R 10001:10001 storage bootstrap/cache` |
| `Class "CustomerPolicy" not found` | Policy auto-discovery cache stale | `php artisan optimize:clear && php artisan policy:cache` |
| `Vite manifest not found` | Frontend assets not compiled | `npm run build || php artisan filament:assets` |

## 3. Done Means
- `curl -f http://localhost:8000/api/health` returns HTTP 200 with JSON status `ok`.
- Database migrations execute cleanly with 0 errors.
- `php artisan test` exits with code 0.
