# Agent Build Steps — Laravel 12 + MongoDB (NoSQL)

### Step 1: Environment Setup
Configure `.env` for MongoDB 7 (`DB_CONNECTION=mongodb`, `DB_HOST=mongodb`) and launch Docker containers.
*Verification:* `docker compose ps`

### Step 2: MongoDB Package Configuration
Install `mongodb/laravel-mongodb` and verify service provider registration.
*Verification:* `php artisan mongodb:test`

### Step 3: Document Models & Embedded Relations
Implement models extending `MongoDB\Laravel\Eloquent\Model` with embedded relationships.
*Verification:* `vendor/bin/pest tests/Feature/MongoDBModelTest.php`

### Step 4: Security Verification
Run Semgrep checks ensuring zero usage of `$where` or unescaped BSON queries.
*Verification:* `semgrep scan --config "p/php"`
