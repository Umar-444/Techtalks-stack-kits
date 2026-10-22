---
name: laravel-filament-mysql-core
description: Core configuration and operational workflows for Laravel with Filament 4 and MySQL 8.4 LTS.
---

# Skill: Laravel Filament MySQL Core

## Operational Shortcuts
- Start stack: `docker compose up -d`
- Clear caches: `docker compose exec app php artisan optimize:clear`
- Run tests: `docker compose exec app php artisan test`
- Database console: `docker compose exec mysql mysql -u filament_user -psecret laravel_filament`

## Done Means
- Fast, reproducible developer environment.
