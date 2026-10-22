---
name: laravel-ai-features-core
description: Core configuration, mock LLM testing, and Horizon asynchronous embedding queue management.
---

# Skill: Laravel AI Features Core

## Operational Shortcuts
- Start stack: `docker compose up -d`
- Run queue worker: `docker compose exec app php artisan queue:work`
- Run test suite: `docker compose exec app php artisan test`
- Database console: `docker compose exec postgres psql -U postgres laravel_ai`

## Done Means
- Fast, reproducible developer environment.
