# Security Policy: Next.js 15+ + Prisma ORM + PostgreSQL

## 1. Invariants
- **Rootless Docker**: Container runs strictly as non-root UID `10001:10001`.
- **Zero Raw SQL String Concatenation**: All database queries must use Prisma Client or `$queryRaw` with template tag parameterization.
- **Zod Schema Validation on All Server Actions**: Every mutation must validate inputs using Zod prior to database persistence.
- **Zero Secret Leaks**: Database credentials and authentication secrets must reside in `.env` and never be committed to version control.
- **Strict Tenant Boundary**: All queries must filter by `tenantId` to prevent Cross-Tenant Broken Object Level Authorization (BOLA).

## 2. Vulnerability Reporting
Please report vulnerabilities to `security@techtalks.dev`.
