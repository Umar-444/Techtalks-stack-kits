# Assistant Guidelines for Laravel + MySQL Stack Kit

## Stack Overview
- Language: PHP 8.3+ / 8.4
- Framework: Laravel 11.x / 12.x
- Database: MySQL 8.4 LTS (InnoDB, strict mode, utf8mb4_0900_ai_ci)
- Cache & Queue: Redis / Database-backed queues
- Testing: PHPUnit / Pest with RefreshDatabase

## Mandatory Rules
1. Zero unparameterized SQL queries. Always use Eloquent query builder or bind parameters.
2. Models must define explicit `$fillable` arrays. Never use `$guarded = []`.
3. Wrap critical mutations in `DB::transaction(..., attempts: 5)` with `lockForUpdate()` for concurrency.
4. Eager load relationships using `with()` to eliminate N+1 queries.
5. All migrations must define foreign keys with cascade constraints and explicit compound indexes.
