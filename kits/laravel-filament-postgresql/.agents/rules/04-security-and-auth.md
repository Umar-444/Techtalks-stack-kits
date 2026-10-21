# Security, RBAC & Authentication Standards

# 04 — Security, RBAC & Authentication Standards

1. **Granular Authorization on Every Action:**
   - Never assume an authenticated user is authorized to modify a resource.
   - Call `$this->authorize('update', $record)` or check Spatie permissions on every mutation.

2. **Zero Plaintext Secrets:**
   - Never commit API keys, secrets, or passwords.
   - Use `config()` values populated exclusively from `.env`.

3. **Rate Limiting:**
   - All authentication routes and sensitive mutations must use the `throttle` middleware (e.g. `throttle:5,1`).

4. **Strict Output Escaping:**
   - Never use `{!! $raw !!}` in Blade views without written justification explaining why XSS is prevented.
