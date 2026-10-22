---
name: install-and-verify
description: Clean install, database migration, automated test run, and health probe verification for Laravel MySQL kit.
---

# Install and Verify Skill: Laravel + MySQL

## Overview
Perform environment setup, install composer dependencies, execute MySQL migrations, run test suites, and probe `/healthz`.

## Execution Steps

### 1. Verify Environment
```bash
php -v
composer --version
docker --version
```

### 2. Dependency Installation
```bash
composer install --no-interaction --prefer-dist
cp .env.example .env
php artisan key:generate
```

### 3. Run Database Migrations & Seeds
```bash
php artisan migrate --force
php artisan db:seed --class=ArticleSeeder
```

### 4. Run Test Suite
```bash
php artisan test
```
Expected output:
```text
   PASS  Tests\Feature\ArticleTest
  ✓ it returns health check probe (200 OK)
  ✓ it lists articles with pagination
  ✓ it searches articles using mysql fulltext search
  ✓ it creates article with validated form request
  ✓ it rejects unauthorized article deletion (403 Forbidden)

  Tests:    5 passed (12 assertions)
  Duration: 0.38s
```

### 5. Health Probe Verification
```bash
php artisan serve --port=8000 &
sleep 2
curl -s http://localhost:8000/healthz
```
Expected output:
```json
{"status":"ok","app":"laravel-mysql","version":"1.0.0","database":"mysql-8.4"}
```
