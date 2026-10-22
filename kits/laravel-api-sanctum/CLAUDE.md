# Laravel 12/13 + Sanctum REST API + Spatie Query Builder — Claude Code Guidelines (CLAUDE.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Quick Reference & Non-Negotiable Standards
### 01 Architecture And Standards
> Laravel REST API Architecture, Standards, and Directory Structure

# Rule 01: REST API Architecture & Standards

- All API routes must reside under the `/api/v1/` prefix in `routes/api.php`.
- Every controller action must return a strictly typed `JsonResource` or `AnonymousResourceCollection`.
- Never return Eloquent models or raw database collections directly from controller actions.
- Model mutations must use dedicated Form Request classes (`StoreProjectRequest`, `UpdateProjectRequest`).
- API status codes must follow standard HTTP semantics:
  - `200 OK` for successful GET, PUT, PATCH operations.
  - `201 Created` for successful POST operations.
  - `204 No Content` for successful DELETE operations.
  - `400 Bad Request` for malformed query parameters.
  - `401 Unauthorized` for missing or invalid Bearer tokens.
  - `403 Forbidden` for policy authorization or ability scope failures.
  - `404 Not Found` for nonexistent resources.
  - `422 Unprocessable Entity` for validation errors.
  - `429 Too Many Requests` when rate limits are exceeded.

### 02 Sanctum Auth And Token Abilities
> Laravel Sanctum Token Issuance, Scopes, and Revocation

# Rule 02: Sanctum Auth & Token Abilities

- User model must include the `Laravel\Sanctum\HasApiTokens` trait.
- Tokens must be issued with explicit ability lists:
  ```php
  $token = $user->createToken('device-name', ['projects:read', 'projects:write']);
  ```
- Protect write endpoints with `middleware('ability:projects:write')`.
- Plaintext tokens are returned strictly once upon generation; never re-display or persist plaintext tokens in logs.
- Logouts must explicitly delete `$request->user()->currentAccessToken()`.
- Enforce token expiration in `config/sanctum.php` or `AuthServiceProvider::boot()`.

### 03 Restful Resources And Query Builder
> Spatie Query Builder Filtering, Sorting, and API Resource Schema

# Rule 03: Query Builder & Resource Formatting

- Use `Spatie\QueryBuilder\QueryBuilder` for collection endpoints.
- Always declare strict whitelists:
  ```php
  QueryBuilder::for(Project::class)
      ->allowedFilters(['title', 'status', AllowedFilter::exact('priority')])
      ->allowedSorts(['created_at', 'title'])
      ->allowedIncludes(['user'])
      ->paginate(request()->input('per_page', 20));
  ```
- Disallow arbitrary or unfiltered joins that could cause denial of service.
- Eloquent API Resources must explicitly map all exposed fields without `...$this->toArray()`.

### 04 Security Bola And Rate Limiting
> BOLA/IDOR Defense, Model Policies, and Rate Limiting

# Rule 04: BOLA Defense & Rate Limiting

- Every controller action with route model binding must invoke `$this->authorize('<action>', $model)`.
- Never trust client-supplied IDs without verifying ownership against `auth()->id()`.
- Model policies must strictly compare tenant ownership:
  ```php
  public function update(User $user, Project $project): bool {
      return $user->id === $project->user_id;
  }
  ```
- Apply rate limiting middleware (`throttle:api`) to all API routes.
- Prevent Cross-Site Scripting (XSS) and SQL Injection by using prepared statements and Form Request rules.

### 05 Testing Verification And Ci
> Automated Testing for Sanctum APIs and Security Invariants

# Rule 05: Testing, Verification, and CI

- All API endpoints must have corresponding feature tests in `tests/Feature/`.
- Test token authorization states:
  - Unauthenticated access returns `401`.
  - Token with missing ability returns `403`.
  - Token with valid ability returns expected `200` or `201`.
- Explicitly test BOLA prevention:
  - User A must receive `403 Forbidden` when attempting to read or update User B's resource.
- Verify Spatie Query Builder filtering logic with assertion tests.
- Verify rate limiting by asserting `429 Too Many Requests` after threshold requests.

