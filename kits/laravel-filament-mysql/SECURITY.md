# Security Policy: Laravel 12/13 + Filament 4 + MySQL 8.4 LTS

## 1. Invariants
- **Rootless Docker**: The application container executes strictly as non-root UID `10001:10001`.
- **Zero Raw SQL Concatenation**: All database queries must use Eloquent or parameterized bindings. Native MySQL full-text searches use prepared `MATCH(...) AGAINST(?)` queries.
- **Zero-Trust BOLA Defense**: Every Filament resource is guarded by a dedicated Laravel Policy. Authorization gates are validated in `before()` and `viewAny()`.
- **Argon2id & WebAuthn**: Password hashing uses Argon2id with 64MB memory cost. Passkey authentication is supported for admin accounts.
- **CSRF & Session Security**: SameSite=Lax, Secure cookies, HttpOnly, and strict session regeneration upon login.

## 2. Vulnerability Reporting
Please report security vulnerabilities to `security@techtalks.dev`.
