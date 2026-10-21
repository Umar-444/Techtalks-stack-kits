# Server Actions & Zod Validation

# Server Actions & Zod Validation

1. **Mandatory Zod Parsing:**
   - Every Server Action must validate inputs with `schema.safeParse()`.
   - Never trust form data or client payloads without validation.

2. **Session Verification:**
   - Verify the caller's session via `supabase.auth.getUser()` before mutations.
