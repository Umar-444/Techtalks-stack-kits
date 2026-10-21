# Agent Build Steps — Laravel 12 + Livewire 4 + PostgreSQL

### Step 1: Environment Setup
Configure `.env` for PostgreSQL 16 and launch Docker containers.
*Verification:* `docker compose ps`

### Step 2: Livewire 4 & Volt Installation
Install Livewire 4 and configure Volt single-file component discovery.
*Verification:* `php artisan volt:install`

### Step 3: Flux UI Integration
Publish Flux UI component views and apply DESIGN.md color tokens.
*Verification:* `php artisan test --filter=FluxTest`

### Step 4: Security Verification
Verify all Livewire components enforce `#[Locked]` on immutable state and check policies.
*Verification:* `vendor/bin/pest tests/Feature/LivewireSecurityTest.php`
