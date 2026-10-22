# Framework Conventions and Standards

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
