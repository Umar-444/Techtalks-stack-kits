# Agent Build Steps — Laravel 12/13 + Filament 4/3 + PostgreSQL
# Linear, self-verifying implementation prompts for AI agents.

Follow each step sequentially. Run the verification command after completing each step. If verification fails, fix the issue before proceeding to the next step.

---

### Step 1: Environment & Container Initialization
**Action:** Copy `.env.example` to `.env`. Configure PostgreSQL 16 connection parameters (`DB_CONNECTION=pgsql`, `DB_HOST=postgres`, `DB_PORT=5432`, `DB_DATABASE=app_production`, `DB_USERNAME=app_user`). Start the multi-container environment with Docker Compose.
**Verification:**
```bash
docker compose ps
docker compose exec app php artisan db:monitor
```
*Expected: Containers healthy, database connected.*

---

### Step 2: Base Migrations & PostgreSQL Schemas
**Action:** Configure PostgreSQL UUID extension (`uuid-ossp` or `gen_random_uuid()`). Ensure all primary keys use UUIDs. Apply initial database migrations for users, sessions, cache, and queue jobs.
**Verification:**
```bash
docker compose exec app php artisan migrate:status
```
*Expected: All core migrations have status 'Ran'.*

---

### Step 3: Filament Admin Panel Installation
**Action:** Register Filament admin panel in SPA mode (`->spa()`). Apply custom branding matching `DESIGN.md` (primary color `#E85D26`, navigation grouping, favicon).
**Verification:**
```bash
docker compose exec app php artisan filament:upgrade
curl -s http://localhost:8000/admin/login | grep -q "Filament"
```
*Expected: Filament assets published and login page returns HTTP 200.*

---

### Step 4: Spatie RBAC & Seeded Roles
**Action:** Install and configure Spatie Laravel Permission. Create seeded roles (`Superadmin`, `Admin`, `Auditor`). Enforce that the Superadmin bypasses permissions via `Gate::before`.
**Verification:**
```bash
docker compose exec app php artisan db:seed --class=RoleAndPermissionSeeder
```
*Expected: Roles and permissions created without errors.*

---

### Step 5: User Management Resource & Policies
**Action:** Create a Filament resource for User management with view, edit, and role assignment. Generate a strict `UserPolicy` ensuring only Superadmins can assign the Superadmin role.
**Verification:**
```bash
docker compose exec app php artisan test --filter=UserResourceTest
```
*Expected: Resource tests pass with 100% assertion success.*

---

### Step 6: Multi-Tenant Schema or Role Scoping
**Action:** Configure tenant scoping or team scoping so records created by a team cannot be accessed or modified by unauthorized users (BOLA defense).
**Verification:**
```bash
docker compose exec app php artisan test --filter=TenantIsolationTest
```
*Expected: Unauthorized cross-tenant queries return 403 Forbidden.*

---

### Step 7: Queue Worker & Redis Horizon
**Action:** Configure Redis 7 for cache and queue. Set up Laravel Horizon dashboard protected by `can:viewHorizon` gate.
**Verification:**
```bash
docker compose exec app php artisan horizon:status
```
*Expected: Horizon is running and healthy.*

---

### Step 8: Pest Architecture Tests
**Action:** Implement Pest architecture tests in `tests/ArchTest.php` asserting:
1. Controllers do not directly invoke `DB::raw()`.
2. All models use UUID traits and guard against mass assignment.
3. No debugging statements (`dd`, `dump`, `ray`) exist in codebase.
**Verification:**
```bash
docker compose exec app ./vendor/bin/pest tests/ArchTest.php
```
*Expected: All architectural assertions pass.*

---

### Step 9: Static Analysis & Style Linting
**Action:** Run Larastan at Level 8 and Laravel Pint to enforce strict types and style standards.
**Verification:**
```bash
docker compose exec app ./vendor/bin/phpstan analyse
docker compose exec app ./vendor/bin/pint --test
```
*Expected: Zero errors found at Level 8.*

---

### Step 10: Full Security Scan & Git Integrity
**Action:** Run Gitleaks and Semgrep static analysis across the entire project repository.
**Verification:**
```bash
gitleaks detect --source . --verbose
semgrep scan --config "p/php" --config "p/owasp-top-ten"
```
*Expected: Zero plaintext credentials and zero OWASP Top 10 vulnerabilities detected.*
