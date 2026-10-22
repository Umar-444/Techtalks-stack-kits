# Laravel 12/13 + Sanctum REST API + Spatie Query Builder

> Production-ready, enterprise-grade RESTful API blueprint powered by Laravel 12/13, Laravel Sanctum token authentication with granular ability scopes, Spatie Query Builder, strict Model Policy BOLA/IDOR prevention, Redis rate-limiting, and rootless container isolation.

---

## Architecture Overview

```
                      +---------------------------------------+
                      |       Client (Mobile / SPA / AI)      |
                      +---------------------------------------+
                                          |
                              Bearer Token (Sanctum)
                                          v
                      +---------------------------------------+
                      |         Nginx / Cloudflare WAF        |
                      +---------------------------------------+
                                          |
                                          v
                      +---------------------------------------+
                      |  Laravel API Gateway (throttle:60,1)  |
                      |  - Sanctum Auth Middleware            |
                      |  - Ability Scopes (ability:write)     |
                      +---------------------------------------+
                                          |
                      +---------------------------------------+
                      |        Controllers & Policies         |
                      |  - Strict BOLA Authorization          |
                      |  - Form Request Validation            |
                      |  - Spatie Query Builder Filtering     |
                      |  - JsonResponse / Resource Schema     |
                      +---------------------------------------+
                                          |
                      +---------------------------------------+
                      |  MySQL 8.4 LTS InnoDB & Redis Cache   |
                      +---------------------------------------+
```

---

## Key Features

1. **Sanctum Ability-Scoped Tokens**:
   - Issue tokens with fine-grained privileges (`projects:read`, `projects:write`, `projects:delete`).
   - Strict token expiration and revocation endpoints.
2. **Spatie Query Builder**:
   - Zero boilerplate URL parameters for filtering: `?filter[status]=active&filter[name]=alpha`.
   - Dynamic sorting: `?sort=-created_at,priority`.
   - Safe relation loading: `?include=user,tasks`.
3. **BOLA / IDOR Hardening**:
   - Every mutating and reading endpoint invokes `$this->authorize('view', $project)` or `$this->authorize('update', $project)`.
   - Unauthenticated or unauthorized tenant access returns deterministic `403 Forbidden`.
4. **Standardized API Responses**:
   - Eloquent API Resources ensure no internal database column leaks.
   - Uniform error envelope: `{"error": {"code": "RESOURCE_FORBIDDEN", "message": "...", "details": []}}`.
5. **Rootless Docker Environment**:
   - Pre-configured `Dockerfile` with non-root UID `10001:10001` ensuring zero host compromise.

---

## Quickstart

```bash
# 1. Clone & Enter Starter
cd starter

# 2. Setup Environment
cp .env.example .env
composer install
php artisan key:generate

# 3. Database Migration & Seeding
php artisan migrate

# 4. Run Test Suite
php artisan test
```

---

## Token Consumption Profile
- **Median Build Tokens**: ~15,200 tokens
- **Efficiency Tier**: A+ (Token-Light Verified)
