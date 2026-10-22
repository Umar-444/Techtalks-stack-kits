# Security Policy: Laravel Sanctum REST API Kit

## 1. Broken Object Level Authorization (BOLA / IDOR) Defense

- **Mandatory Policy Check**: Every single controller action handling a specific model instance MUST call `$this->authorize('action', $model)`.
- **Tenant Scope Isolation**: Queries in list actions MUST apply user ownership scopes:
  ```php
  $query = Project::where('user_id', auth()->id());
  ```
- **Policy Enforcement**: `ProjectPolicy::update()` ensures `$user->id === $project->user_id`. Attempting to access or mutate another user's project yields `403 Forbidden`.

---

## 2. Token Storage and Cryptographic Security

- Sanctum tokens are 40-character random strings hashed with SHA-256 before storage in `personal_access_tokens.token`.
- Plaintext tokens are returned only ONCE during creation (`createToken()`) and never logged.
- Revocation immediately removes the database row, instantly invalidating the bearer token.

---

## 3. Rate Limiting & Denial of Service

- The `throttle:api` middleware enforces a sliding window rate limit of 60 requests per minute per authenticated user (or per IP for guest routes).
- Exceeding the rate limit returns `429 Too Many Requests` with standard `Retry-After` headers.

---

## 4. Rootless Container Isolation

- Docker container runs under unprivileged non-root user `10001:10001`.
- PHP-FPM process has no root capabilities (`CAP_NET_RAW`, `CAP_SYS_ADMIN` disabled).
- File permissions are restricted to read-only for application code, with write access limited strictly to `storage/` and `bootstrap/cache/`.
