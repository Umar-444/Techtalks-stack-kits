# Rule 5: Testing, Type Safety & Strict Verification

## Context & Principles
- Enforce strict TypeScript compilation (`"strict": true`, zero `any` types).
- Validate Server Actions, Zod schemas, and Supabase client integration with automated unit and integration tests.

## Standards
1. **Schema Unit Tests**: Test Zod schemas against valid payloads, boundary limits, and malicious script inputs.
2. **Server Action Tests**: Assert that unauthenticated callers receive unauthorized errors before database queries execute.
3. **RLS Assertions**: Verify through integration tests that User A cannot read, update, or delete records owned by User B.
4. **Build Gate**: Ensure `next build` and `tsc --noEmit` pass with zero warnings in CI pipelines.
