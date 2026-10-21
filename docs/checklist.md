# Security Checklist — 2026 Edition
## PHP 8.4 / Laravel 13

> Last updated: October 2026. Updated for NIST SP 800-63B (2024), OWASP Top 10 (2025), and OWASP API Security Top 10 (2023).

---

## Pre-Development Security Checklist

- [ ] Review and understand security requirements for the project
- [ ] Set up secure development environment with PHP 8.4 and Laravel 13
- [ ] Configure version control security (protected branches, signed commits)
- [ ] Establish mandatory code review processes for all PRs
- [ ] Set up dependency scanning tools (`composer audit --locked` in CI/CD)
- [ ] Generate Software Bill of Materials (SBOM) for supply chain tracking
- [ ] Confirm PHP version is 8.2+ (8.4 recommended) — PHP 8.1 is EOL
- [ ] Confirm Laravel version is 11+ (13 recommended) — Laravel 10 is EOL

---

## Authentication & Authorization

- [ ] Implement secure password policies — **minimum 15 characters** (NIST SP 800-63B 2024)
- [ ] Use `password_hash()` with `PASSWORD_ARGON2ID` — OWASP 2024 parameters (`memory_cost=65536, time_cost=3, threads=1`)
- [ ] Never use `md5()`, `sha1()`, or `rand()` for any security-sensitive purpose
- [ ] Auto-rehash passwords on login when parameters change (`password_needs_rehash()`)
- [ ] Implement **Passkeys / WebAuthn (FIDO2)** as the preferred passwordless option
- [ ] Implement multi-factor authentication (TOTP as minimum; Passkeys preferred)
- [ ] Set up secure session management (see session checklist below)
- [ ] Configure secure cookie settings: `Secure`, `HttpOnly`, `SameSite=Strict`
- [ ] Use `session.use_strict_mode = 1` to reject unrecognized session IDs
- [ ] Implement proper logout — invalidate session and clear cookies
- [ ] Session name must use `hash('sha256', ...)` — **never `md5()`**
- [ ] Set up role-based access control (RBAC) with Laravel Gates and Policies
- [ ] Implement timing-safe comparison for all credential checks

---

## Input Validation & Sanitization

- [ ] Validate ALL user inputs server-side — never trust client-side validation alone
- [ ] Use allowlists (not blocklists) for validation
- [ ] Sanitize output based on context: HTML -> `htmlspecialchars(ENT_QUOTES|ENT_SUBSTITUTE|ENT_HTML5)`, SQL -> prepared statements, shell -> `escapeshellarg()`
- [ ] Use parameterized queries / prepared statements — zero string concatenation in SQL
- [ ] Implement CSRF protection (Laravel's built-in CSRF + `SameSite=Strict`)
- [ ] Set up rate limiting on all forms, APIs, and login endpoints
- [ ] Use PHP 8.4 typed enums for restricted value sets

---

## File Upload Security

- [ ] Validate MIME types from file content (not from user-supplied `Content-Type` or extension)
- [ ] Use `finfo` to read magic bytes: `(new finfo(FILEINFO_MIME_TYPE))->file($tmpPath)`
- [ ] Check file size limits before processing
- [ ] Generate cryptographically secure random filenames (`bin2hex(random_bytes(16))`)
- [ ] Store files **outside** the web root (use Laravel's `private` disk)
- [ ] Implement file scanning (ClamAV or cloud API)
- [ ] Set proper file permissions (640 for files, 750 for directories)

---

## Database Security

- [ ] Use prepared statements for ALL queries — including `IN()`, `LIKE`, `ORDER BY`
- [ ] Implement proper database user permissions — principle of least privilege
- [ ] Encrypt sensitive data at rest — use Laravel's `encrypted` cast
- [ ] Enable TLS for database connections (`PDO::MYSQL_ATTR_SSL_CA`)
- [ ] Use database-level constraints (UNIQUE, NOT NULL, FK)
- [ ] Implement proper indexing for performance and security
- [ ] Set up automated database backups with encryption
- [ ] Disable `PDO::ATTR_EMULATE_PREPARES` for real prepared statements

---

## API Security (OWASP API Security Top 10 — 2023)

- [ ] **API1:2023** — Broken Object Level Authorization: Validate object ownership on every request
- [ ] **API2:2023** — Broken Authentication: Use Sanctum 4.x / Passport — no custom token schemes
- [ ] **API3:2023** — Broken Object Property Level Authorization: Use `$fillable` — never `$guarded = []`
- [ ] **API4:2023** — Unrestricted Resource Consumption: Rate limiting on all endpoints
- [ ] **API5:2023** — Broken Function Level Authorization: Verify role/ability on every action
- [ ] **API6:2023** — Unrestricted Access to Sensitive Business Flows: Multi-step flow protection
- [ ] **API7:2023** — Server Side Request Forgery (SSRF): Validate and allowlist all outbound URLs
- [ ] **API8:2023** — Security Misconfiguration: Disable debug mode, hide version headers
- [ ] **API9:2023** — Improper Inventory Management: Document and version all API endpoints
- [ ] **API10:2023** — Unsafe Consumption of APIs: Validate and sanitize all third-party API responses
- [ ] Implement API versioning (`/api/v1/`, `/api/v2/`)
- [ ] Use HTTPS for all API calls — TLS 1.3 preferred
- [ ] Validate and sanitize all JSON input — reject unexpected fields
- [ ] Set up structured API logging

---

## Security Headers (2026 Standard)

- [ ] `Content-Security-Policy` with nonces — **no `unsafe-inline`**, **no `unsafe-eval`**
- [ ] `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`
- [ ] `X-Frame-Options: DENY` (or CSP `frame-ancestors 'none'`)
- [ ] `X-Content-Type-Options: nosniff`
- [ ] `Referrer-Policy: strict-origin-when-cross-origin`
- [ ] `Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()`
- [ ] `Cross-Origin-Opener-Policy: same-origin`
- [ ] `Cross-Origin-Embedder-Policy: require-corp`
- [ ] `Cross-Origin-Resource-Policy: same-origin`
- [ ] `Reporting-Endpoints` (CSP violation reporting — replaces deprecated `report-uri`)
- [ ] ~~`X-XSS-Protection`~~ — [DEPRECATED] **DEPRECATED** — Remove from all headers
- [ ] Register middleware in `bootstrap/app.php` (Laravel 11+) — `Kernel.php` was removed
- [ ] Test headers at [securityheaders.com](https://securityheaders.com)

---

## Configuration Security

- [ ] `APP_DEBUG=false` in production — never expose stack traces
- [ ] Store ALL secrets in environment variables — never in code
- [ ] Use a secrets manager in production (HashiCorp Vault, AWS SSM, Azure Key Vault)
- [ ] Use environment variables for DB credentials, API keys, mail passwords
- [ ] Set up proper CORS policies (`cors.php` in Laravel)
- [ ] Implement HTTPS redirect — TLS 1.3 preferred, TLS 1.2 minimum
- [ ] Remove `X-Powered-By` and `Server` response headers
- [ ] Disable PHP version exposure (`expose_php = Off` in `php.ini`)
- [ ] Set `opcache.validate_timestamps=0` in production (performance + security)

---

## Error Handling & Logging

- [ ] Implement proper error handling — never expose DB errors, stack traces, or file paths
- [ ] Use custom error pages for 404, 403, 500 (no framework branding)
- [ ] Set up structured logging (Monolog with JSON formatter, or Sentry)
- [ ] Monitor for authentication failures, CSRF violations, and rate limit triggers
- [ ] Implement log rotation and retention policy
- [ ] Set up alerts for suspicious activities (repeated auth failures, unusual traffic)
- [ ] Store logs outside the web root — never publicly accessible

---

## Supply Chain & Dependency Security

- [ ] Run `composer audit --locked` in every CI/CD pipeline run
- [ ] Enable GitHub Dependabot for automated dependency updates
- [ ] Pin critical dependency versions in `composer.lock`
- [ ] Review licenses of all third-party packages
- [ ] Monitor PHP security advisories (https://phpsecurity.readthedocs.io/)
- [ ] Generate SBOM (Software Bill of Materials) with `cyclonedx-php-composer`
- [ ] Subscribe to Laravel security notifications at https://laravel-news.com/security

---

## Passkeys / WebAuthn (FIDO2) — 2026 Standard

- [ ] Implement WebAuthn/FIDO2 as the primary authentication option
- [ ] Use a vetted library: `web-auth/webauthn-framework` (PHP) or `laragear/webauthn` (Laravel)
- [ ] Register passkeys tied to user accounts
- [ ] Support multiple passkeys per user (phone, laptop, hardware key)
- [ ] Fall back to TOTP MFA if passkeys are unavailable
- [ ] Test with hardware security keys (YubiKey) and platform authenticators (Touch ID, Face ID)

---

## Infrastructure Security

- [ ] Use secure server configurations (CIS Benchmarks for Ubuntu/Debian)
- [ ] Implement firewall rules (UFW or nftables) — allowlist only required ports
- [ ] Set up Fail2Ban for brute force protection
- [ ] Configure SSL/TLS: TLS 1.3 preferred, TLS 1.2 minimum
- [ ] Use ECDSA P-256 certificates (or RSA-4096 minimum — RSA-2048 is marginal per NIST 2024)
- [ ] Implement regular automated backups with encryption at rest
- [ ] Set up uptime and anomaly monitoring

---

## Testing & Auditing

- [ ] Perform automated security testing (SAST: PHPStan level 9, Psalm)
- [ ] Conduct penetration testing (at least annually or before major releases)
- [ ] Run DAST scanning (OWASP ZAP or similar)
- [ ] Regular security audits of all critical components
- [ ] Code security reviews for authentication, authorization, and data handling
- [ ] Perform vulnerability assessments after dependency updates

---

## Deployment Security (CI/CD)

- [ ] Secure deployment pipeline — no secrets in environment variables of CI logs
- [ ] Use Infrastructure as Code (Terraform / Pulumi) with security scanning
- [ ] Implement secrets management in CI/CD (GitHub Actions Secrets, Vault)
- [ ] Set up staging environments that mirror production security settings
- [ ] Run `composer audit --locked` as a required CI step
- [ ] Automate security header checks in deployment validation
- [ ] Implement rollback procedures with verified checksum validation

---

## Incident Response

- [ ] Develop and document incident response plan
- [ ] Set up communication channels for security incidents
- [ ] Document all security procedures and runbooks
- [ ] Schedule regular security training for all developers
- [ ] Conduct tabletop incident simulations (at least annually)
- [ ] Review and update response plans after each incident
- [ ] Use [GitHub Private Security Advisories](https://github.com/Umar-444/Laravel-AI-Security-Masterclass/security/advisories/new) for responsible disclosure

---

---

## AI & LLM Security (OWASP Top 10 for LLM Applications — 2025)

- [ ] **LLM01: Prompt Injection** — System and user prompt separation with explicit XML boundary delimiters
- [ ] **LLM02: Sensitive Information Disclosure** — Pre-flight PII redaction pipeline before sending data to external AI APIs
- [ ] **LLM03: Supply Chain Vulnerabilities** — Pin and audit all third-party AI SDKs and embedding models
- [ ] **LLM04: Model Denial of Service** — Per-tenant token rate limiting and hard daily billing caps
- [ ] **LLM05: Improper Output Handling** — Treat all model outputs as untrusted input; never execute unescaped in Blade or raw SQL
- [ ] **LLM06: Excessive Agency / Tool Sandboxing** — Allowlist agent tools and require human-in-the-loop approval for destructive actions
- [ ] **RAG Tenant Isolation** — Enforce vector database tenant ID filters at the retrieval layer, never at prompt generation

---

## Regional Compliance & Legal (GDPR, HIPAA, PCI DSS 4.0, Saudi PDPL)

- [ ] Understand applicable regulatory requirements (GDPR, HIPAA, PCI DSS 4.0)
- [ ] **Saudi PDPL (Personal Data Protection Law / SDAIA)**:
  - [ ] Implement data minimization and purpose limitation on all customer records
  - [ ] Enforce in-kingdom data residency controls where required for sensitive national records
  - [ ] Obtain explicit consent before transmitting citizen data to foreign AI cloud endpoints
  - [ ] Maintain 72-hour breach notification procedures aligned with SDAIA regulatory directives
- [ ] **ZATCA-Adjacent Security Practices**:
  - [ ] Cryptographic signing and tamper-proof hash chains for financial transaction audit logs
  - [ ] Secure storage and rotation of CSID cryptographic certificates
- [ ] Set up data retention and automated deletion policies (right to erasure)
- [ ] Document all security controls and maintain immutable audit logs for regulatory inspections

---

*Checklist Version: 2026.10 | PHP 8.4 / Laravel 13 | OWASP Top 10 (2025) | OWASP LLM Top 10 (2025) | Saudi PDPL / SDAIA*

