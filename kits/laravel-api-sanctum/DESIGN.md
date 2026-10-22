# System Design & API Contract: Laravel 12/13 Sanctum REST API

## 1. RESTful URL Hierarchy & Standard Headers

All API endpoints reside under the `/api/v1/` prefix with explicit versioning:

```http
POST /api/v1/auth/token          -> Issue Bearer Token with requested abilities
POST /api/v1/auth/revoke         -> Invalidate current token
GET  /api/v1/auth/me             -> Current user identity and active token abilities
GET  /api/v1/projects            -> Filtered & paginated project list (Spatie Query Builder)
POST /api/v1/projects            -> Create new project (requires 'projects:write')
GET  /api/v1/projects/{id}       -> Retrieve single project (BOLA policy checked)
PUT  /api/v1/projects/{id}       -> Update project (BOLA policy checked)
DELETE /api/v1/projects/{id}    -> Soft/Hard delete project (BOLA policy checked)
```

### Request Headers
- `Accept: application/json`
- `Content-Type: application/json`
- `Authorization: Bearer <plainTextToken>`

---

## 2. Token Lifecycle & Ability Matrix

| Token Ability | Allowed Routes | Description |
|---|---|---|
| `*` | All API routes | Root/Admin personal access token |
| `projects:read` | `GET /api/v1/projects*` | Read-only access to projects owned by the user |
| `projects:write` | `POST, PUT /api/v1/projects*` | Create and mutate owned projects |
| `projects:delete` | `DELETE /api/v1/projects*` | Remove owned projects |

### Token Expiration Policy
- Personal access tokens expire in `10080` minutes (7 days) by default.
- Automatic expiration enforced via Sanctum's `Sanctum::tokensExpireIn(now()->addDays(7))` in `AuthServiceProvider`.

---

## 3. Query Filtering Specification (Spatie Query Builder)

Clients construct queries via uniform query parameters:

```http
GET /api/v1/projects?filter[status]=active&filter[search]=security&sort=-created_at&include=user&page=1
```

- **`filter[status]`**: Exact match on project status enum (`active`, `archived`, `draft`).
- **`filter[search]`**: Scope filter performing partial match on title and description.
- **`sort`**: Comma-separated fields; prefix with `-` for descending order (`sort=-created_at,priority`).
- **`include`**: Whitelisted relationships (`include=user,tags`). Unknown relationships return `400 Bad Request`.

---

## 4. Uniform Error Envelope

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "The given data was invalid.",
    "status": 422,
    "fields": {
      "title": ["The title field is required."]
    }
  }
}
```
