# Security and BOLA Authorization

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
