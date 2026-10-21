# SECURITY.md — Laravel + Filament + PostgreSQL Security Policy & Standards

Security is an integrated baseline layer in every TechTalks Stack Kit, never an opt-in afterthought.

## 1. Security Invariants (Non-Negotiable)

1. **Zero Hardcoded Credentials:**
   No passwords, API tokens, database passwords, or application secrets in git. All environment variables must be declared in `.env.example` with empty or placeholder values.

2. **Strict Query Parameterization:**
   Raw SQL string concatenation is strictly forbidden. All queries must use PDO parameter bindings or Eloquent ORM abstractions.

3. **Granular Authorization (BOLA Prevention):**
   Every controller method, Filament resource action, and API endpoint must verify authorization via Laravel Policies ($this->authorize) or Spatie Permission gates.

4. **Password & Session Hardening:**
   - Passwords hashed using Argon2id (`bcrypt` minimum with cost 12).
   - Strict session fixation defense (`session()->regenerate()` on login).
   - Session cookies configured with `HttpOnly`, `SameSite=Lax`, and `Secure` (in production).

5. **Automated Security Guardrails:**
   - Gitleaks secret scanner in pre-commit and CI.
   - Semgrep static analysis rules targeting PHP/Laravel vulnerabilities.
   - Pest Architecture tests asserting that controllers and models adhere to security boundaries.

---

## 2. Vulnerability Reporting
If you discover a vulnerability within this kit or any generated code, please report it privately:
- Email: `security@itsumarfarooq.com`
- Response timeline: Acknowledgement within 24 hours, patch within 72 hours.
