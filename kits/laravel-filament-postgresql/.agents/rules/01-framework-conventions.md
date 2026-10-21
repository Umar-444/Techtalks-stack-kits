# Framework Conventions (PHP 8.4 & Laravel 12/13)

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
