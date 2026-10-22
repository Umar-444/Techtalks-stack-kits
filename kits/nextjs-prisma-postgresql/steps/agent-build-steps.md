# Step-by-Step Agent Build Guide

### Step 1: Environment & Database Configuration
- Action: Copy `.env.example` to `.env` and verify PostgreSQL connection string.
- Command: `npx prisma validate`
- Verification: Schema file is valid and parses with exit code 0.

### Step 2: Prisma Schema & Migration Deployment
- Action: Generate Prisma Client and deploy migrations.
- Command: `npx prisma generate && npx prisma migrate deploy`
- Verification: Database tables `User`, `Project`, `Task` exist in schema `public`.

### Step 3: Database Seeder Execution
- Action: Seed initial workspace, admin user, and sample projects.
- Command: `npm run db:seed`
- Verification: `npx prisma studio --browser none` or query count returns seeded rows.

### Step 4: Server Action & Zod Validation Implementation
- Action: Implement `createProjectAction` and `createTaskAction` with Zod validation.
- Command: `npm test -- tests/actions.test.ts`
- Verification: Tests pass validating input schema and persistent state.

### Step 5: Multi-Tenant Boundary Assertion
- Action: Verify that cross-tenant mutations return validation or authorization errors.
- Command: `npm test -- tests/schema.test.ts`
- Verification: Policy tests exit 0.

### Step 6: Architecture & Static Security Scan
- Action: Run ESLint, TypeScript compiler check, and Semgrep scan.
- Command: `npm run build && semgrep scan`
- Verification: Production bundle compiles cleanly; 0 SAST findings.
