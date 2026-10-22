# OWASP API Security Top 10 (2023) Core Architecture Invariants

# OWASP API Security Top 10 (2023) Core Architecture Invariants

## 1. Zero-Trust API Architecture
- Every endpoint must enforce explicit authentication and object-level authorization before touching persistent storage.
- Never rely on client-side routing, hidden UI elements, or obfuscated IDs for access control.
- Treat every incoming parameter (query, path, headers, request body) as potentially untrusted and hostile.

## 2. API Security Threat Mapping (2023 Standard)
- **API1:2023 Broken Object Level Authorization (BOLA)**: Always verify object ownership (`owner_id == current_user.id`).
- **API2:2023 Broken Authentication**: Enforce cryptographically verified JWT tokens, signed with asymmetric keys (RS256) or strong secrets (HS256). Prohibit `none` algorithm.
- **API3:2023 Broken Object Property Level Authorization (BOPLA)**: Never return internal models or sensitive fields (passwords, salts, internal flags) in response payloads.
- **API4:2023 Unrestricted Resource Consumption**: Impose strict rate limits, request payload size limits, and pagination bounds (`limit <= 100`).
- **API5:2023 Broken Function Level Authorization (BFLA)**: Restrict administrative actions via declarative role and scope checks (`@require_role("admin")`).

## 3. Strict Input/Output Schema Enforcement
- All endpoints must declare explicit Pydantic request and response models.
- Set `extra = "forbid"` on input schemas to reject unexpected or mass-assigned fields.
