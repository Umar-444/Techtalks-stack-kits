---
id: "04-api-security-and-input-validation"
title: "API Security & OWASP Defense in Go"
description: "Security invariants covering input validation, parameterized SQL injection prevention, BOLA/IDOR protection, and CSRF defense in Chi & HTMX."
globs: ["**/*.go", "**/*.sql"]
alwaysApply: true
---

# 04 - API Security & OWASP Defense in Go

## 1. Zero SQL Injection by Construction
- `sqlc` generates strictly parameterized queries (`$1, $2, ...`) for all database operations.
- Never construct dynamic SQL via string interpolation (`fmt.Sprintf("SELECT * FROM users WHERE name = '%s'", input)`). String concatenation in SQL statements is strictly rejected during security auditing.

## 2. Broken Object Level Authorization (BOLA/IDOR) Defense
- Always enforce tenant and user ownership checks at the query layer rather than in application memory.
- In every parameterized query accessing customer data, include the tenant ID:
  ```sql
  -- name: GetDocumentForTenant :one
  SELECT id, title, content, tenant_id
  FROM documents
  WHERE id = $1 AND tenant_id = $2;
  ```
- If no record matches both `$1` (resource ID) and `$2` (authenticated tenant ID), return an immediate `404 Not Found` or `403 Forbidden`.

## 3. CSRF Protection for HTMX Requests
- For state-mutating requests (`POST`, `PUT`, `DELETE`), generate an encrypted anti-CSRF token per session.
- Configure HTMX to include the CSRF token in all outgoing requests automatically:
  ```html
  <body hx-headers='{"X-CSRF-Token": "{{ .CSRFToken }}"}'>
  ```
- Validate the token in Chi middleware before executing any mutation handler.

## 4. Rate Limiting & Denial of Service Defense
- Protect login and resource-heavy endpoints using token bucket rate limiting (e.g., `golang.org/x/time/rate` or Chi middleware).
- Limit maximum request body size to prevent memory exhaustion attacks:
  ```go
  r.Body = http.MaxBytesReader(w, r.Body, 10<<20) // 10MB limit
  ```
