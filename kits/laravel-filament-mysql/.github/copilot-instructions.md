# GitHub Copilot Instructions for Laravel 12/13 + Filament 4 + MySQL 8.4 LTS
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Framework Conventions and Standards
# Framework Conventions and Standards

## 1. Strict Typing and Modern PHP 8.3+
- Always declare `declare(strict_types=1);` at the top of every PHP file.
- Use native constructor property promotion and typed properties.
- Return explicit types for all controller, service, and policy methods.

## 2. Directory Layout & Layer Separation
- **Models**: `app/Models/` (pure Eloquent entities with relationships and casts).
- **Filament Resources**: `app/Filament/Resources/` (declarative table and form schemas).
- **Policies**: `app/Policies/` (authorization logic, zero business mutations).
- **DTOs & Actions**: `app/Actions/` (isolated, testable domain operations).

## 3. Never-List
- Never use `env()` outside configuration files in `config/`.
- Never execute raw SQL queries with string concatenation.
- Never place business logic directly in Blade views or route closures.

## Filament Admin Panel Standards
# Filament Admin Panel Standards

## 1. Declarative Table Construction
- Build tables using typed column components (`TextColumn`, `IconColumn`, `BadgeColumn`).
- Use `searchable()` with custom database scopes when querying large MySQL tables.
- Enable `sortable()` only on indexed database columns.

## 2. Form Schema Best Practices
- Structure complex forms with `Section` and `Grid` layouts.
- Always declare server-side validation rules using `required()`, `maxLength()`, `unique()`.
- Use `TextInput::make('email')->email()->unique(ignoreRecord: true)`.

## 3. Bulk Action Safety
- Wrap mass mutations in database transactions with deadlock retry mechanisms.
- Require confirmation modals for destructive bulk actions: `DeleteBulkAction::make()->requiresConfirmation()`.

## MySQL 8.4 InnoDB and Full-Text Optimization
# MySQL 8.4 InnoDB and Full-Text Optimization

## 1. Storage Engine & Collation
- All tables must use `ENGINE=InnoDB` with `utf8mb4_0900_ai_ci` collation.
- Use `bigIncrements('id')` or ULID/UUID primary keys.

## 2. Native Full-Text Search
- Define composite full-text indexes in migrations:
  ```php
  $table->fullText(['name', 'email', 'company_name'], 'customers_fulltext_idx');
  ```
- Query using MATCH AGAINST in Boolean Mode via parameterized bindings:
  ```php
  $query->whereRaw('MATCH(name, email, company_name) AGAINST(? IN BOOLEAN MODE)', [$searchTerm]);
  ```

## 3. Deadlock Handling
- Always catch `\Illuminate\Database\QueryException` with error code 1213 (Deadlock found).
- Wrap concurrent operations in `DB::transaction(fn() => ..., 3)`.

## Security and BOLA Authorization
# Security and BOLA Authorization

## 1. BOLA Defense on Every Resource
- Bind every Eloquent model to an explicit Policy in `AuthServiceProvider` or auto-discovery.
- Implement all standard policy methods: `viewAny`, `view`, `create`, `update`, `delete`.
- Verify user ownership or organization membership before returning `true`.

## 2. Mass Assignment Safeguards
- Always declare `$fillable` on all models. Never use `$guarded = []`.
- Sanitize user inputs using FormRequest or Filament form validation schemas.

## 3. Passkey & Session Hardening
- Enforce `SameSite=Lax` and `HttpOnly` on all session cookies.
- Regenerate session ID immediately upon authentication: `$request->session()->regenerate()`.

## Testing Verification and CI Standards
# Testing Verification and CI Standards

## 1. Feature Testing with Pest
- Test all Filament table rendering and form submission workflows.
- Assert that unauthorized users receive HTTP 403 Forbidden.
- Assert that MySQL full-text search returns exact matching records.

## 2. Architectural Invariants
- Assert that no `dd()`, `dump()`, or `var_dump()` calls exist in `app/`.
- Assert that all models use strict fillable properties.

## 3. CI Pipeline
- Every pull request must pass `php artisan test`, `gitleaks`, and `semgrep`.

