# Step-by-Step Agent Build Guide

### Step 1: Environment & Secrets Initialization
- Action: Copy `.env.example` to `.env` and generate Laravel app key.
- Command: `php artisan key:generate --ansi`
- Verification: `.env` contains valid `APP_KEY=base64:...`

### Step 2: Database Schema & MySQL 8.4 Full-Text Migrations
- Action: Run database migrations creating InnoDB tables and full-text indexes.
- Command: `php artisan migrate --force`
- Verification: `SHOW INDEX FROM customers WHERE Index_type = 'FULLTEXT';` returns non-empty.

### Step 3: Filament Admin Panel Provider Registration
- Action: Register `AdminPanelProvider` with custom brand color and dark mode tokens.
- Command: `php artisan filament:check`
- Verification: Route `/admin` registered and accessible.

### Step 4: Customer Resource Scaffolding
- Action: Scaffold Filament resource, form components, and table columns.
- Command: `php artisan make:filament-resource Customer --generate`
- Verification: Resource class registered in panel navigation.

### Step 5: BOLA Policy & Tenant Authorization Enforcement
- Action: Implement `CustomerPolicy` guarding `viewAny`, `view`, `create`, `update`, `delete`.
- Command: `php artisan test --filter=BolaPolicyTest`
- Verification: Policy tests exit 0.

### Step 6: Architecture & Static Security Scan
- Action: Run Pest Architecture tests and Semgrep scan.
- Command: `php artisan test --filter=ArchTest && semgrep scan`
- Verification: 0 architectural violations, 0 SAST findings.
