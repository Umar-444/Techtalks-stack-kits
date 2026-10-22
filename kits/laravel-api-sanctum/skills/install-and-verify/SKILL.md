---
name: "install-and-verify"
description: "Step-by-step procedures to install dependencies, run migrations, and verify API test suite."
version: "1.0.0"
---

# Install & Verify Skill: Laravel Sanctum API

## Quickstart Commands
```bash
composer install
cp .env.example .env
php artisan key:generate
php artisan migrate --force
php artisan test
```

## Health Verification
- Send `GET /api/v1/health` -> Expect `200 OK` with `{"status": "ok"}`.
