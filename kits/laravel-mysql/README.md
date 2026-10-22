# Laravel 11/12 + MySQL 8.4 LTS Stack Kit

A production-grade, highly optimized backend kit pairing **Laravel 11/12** with **MySQL 8.4 LTS**, featuring strict InnoDB integrity, full-text search, deadlock-resilient transactions, and read/write splitting.

## Stack Overview
- **Language**: PHP 8.4+ / 8.3
- **Framework**: Laravel 11.x / 12.x
- **Database**: MySQL 8.4 LTS (InnoDB, strict mode, utf8mb4_0900_ai_ci)
- **Search**: Native MySQL Full-Text Search in Boolean Mode
- **Concurrency**: Deadlock retry transactions (`attempts: 5`) with `lockForUpdate()`
- **Container**: Multi-stage Alpine container running as unprivileged `appuser` (UID 10001)

## Quickstart

### 1. Install Dependencies
```bash
composer install
cp .env.example .env
php artisan key:generate
```

### 2. Run Database Migrations & Seeds
```bash
php artisan migrate
```

### 3. Run Test Suite
```bash
php artisan test
```

### 4. Run with Docker Compose
```bash
docker compose up -d
curl http://localhost:8000/healthz
```

## Security & Verification Standards
- Strict MySQL modes prevent silent data truncation.
- Strict `$fillable` arrays on all models prevent mass-assignment vulnerabilities.
- Fully documented in [`VERIFICATION.md`](VERIFICATION.md).
