---
description: "Laravel REST API Architecture, Standards, and Directory Structure"
globs: ["app/Http/Controllers/Api/**/*.php", "routes/api.php", "app/Http/Resources/**/*.php"]
---

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
