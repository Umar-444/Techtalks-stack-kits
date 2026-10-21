# GitHub Copilot Instructions for Laravel 13 + Filament 4 + PostgreSQL
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Framework Conventions (PHP 8.4 & Laravel 12/13)
# 01 — Framework Conventions (PHP 8.4 & Laravel 12/13)

1. **Strict Types & Explicit Signatures:**
   - Every PHP file MUST begin with `declare(strict_types=1);`.
   - All method arguments, return types, and class properties MUST have explicit type declarations.
   - Use PHP 8.4 asymmetric visibility (`public private(set)`) and constructor property promotion where applicable.

2. **Form Request Validation:**
   - Never validate incoming request payloads directly inside controller methods.
   - Always extract validation rules into a dedicated `FormRequest` class (`app/Http/Requests/`).
   - Use strictly typed request getters (`$request->string('field')`, `$request->integer('id')`).

3. **No Direct Database Facade in Controllers:**
   - Controllers must never call `DB::table()` or `DB::raw()` directly.
   - Business operations and queries must be encapsulated in Eloquent Models, Query Scopes, or dedicated Action classes.

## Filament 4/3 Admin Panel Architecture
# 02 — Filament 4/3 Admin Panel Architecture

1. **Single-Page Application (SPA) Mode:**
   - The Filament panel provider must be configured with `->spa()` for fluid Livewire client transitions.

2. **Resource Organization & Navigation:**
   - Structure navigation by business job functions, not database table names.
   - Always define an icon (`heroicon-o-...`) and navigation sort order for every resource.

3. **Table & Form Standards:**
   - Tables must define searchable and sortable columns explicitly.
   - Every form field must define client and server validation matching database constraints.
   - Bulk actions must require confirmation modals explaining the impact of the action.

4. **Authorization on Resources:**
   - Every Filament Resource must bind to a model policy using `canViewAny()`, `canCreate()`, `canEdit()`, `canDelete()`.

## PostgreSQL 16+ Database Conventions
# 03 — PostgreSQL 16+ Database Conventions

1. **UUID Primary Keys:**
   - All database tables must use UUID primary keys (`$table->uuid('id')->primary()`).
   - Models must use the `HasUuids` trait.

2. **Foreign Key Integrity:**
   - Always specify explicit foreign key constraints with `cascadeOnDelete()` or `restrictOnDelete()`.
   - Never leave loose integer ID relationships without foreign key indices.

3. **JSONB Fields:**
   - Semi-structured data must be stored in `jsonb` columns.
   - Add GIN indices (`CREATE INDEX ... USING gin`) for fields queried by JSON keys.

4. **Rollback Safety:**
   - Every migration must have a tested `down()` method that restores previous schema state cleanly.

## Security, RBAC & Authentication Standards
# 04 — Security, RBAC & Authentication Standards

1. **Granular Authorization on Every Action:**
   - Never assume an authenticated user is authorized to modify a resource.
   - Call `$this->authorize('update', $record)` or check Spatie permissions on every mutation.

2. **Zero Plaintext Secrets:**
   - Never commit API keys, secrets, or passwords.
   - Use `config()` values populated exclusively from `.env`.

3. **Rate Limiting:**
   - All authentication routes and sensitive mutations must use the `throttle` middleware (e.g. `throttle:5,1`).

4. **Strict Output Escaping:**
   - Never use `{!! $raw !!}` in Blade views without written justification explaining why XSS is prevented.

## Pest Testing & Architecture Assertions
# 05 — Pest Testing & Architecture Assertions

1. **Pest PHP Conventions:**
   - Write tests using Pest's functional test syntax (`it('does something', function() { ... });`).
   - Use strict assertions (`expect($val)->toBe(...)`).

2. **Architecture Assertions (Arch Tests):**
   - Assert that `App\Http\Controllers` does not depend on `Illuminate\Support\Facades\DB`.
   - Assert that no debugging functions (`dd`, `dump`, `ray`, `var_dump`) remain in code.
   - Assert that all models have proper type hints and fillable/guarded declarations.

3. **Database Test Isolation:**
   - Use `RefreshDatabase` or `LazilyRefreshDatabase` trait for database feature tests.

