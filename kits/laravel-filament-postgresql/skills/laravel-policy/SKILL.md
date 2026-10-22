---
name: laravel-policy
description: Generate granular Laravel Model Policies enforcing zero-trust BOLA and multi-tenant authorization.
---

# Laravel Policy Skill

## Purpose
Guarantees authorization gates are applied to every database mutation and view action.

## Key Workflows
```bash
php artisan make:policy CustomerPolicy --model=Customer
```

## Security Invariants
- Deny by default: `before(User $user, string $ability)` only bypasses for verified `super-admin`.
- Explicit tenant scoping: Verify `$user->tenant_id === $model->tenant_id` on all view/update/delete gates.

## Done Means
Every model has an associated Policy registered in `AuthServiceProvider` and unauthorized cross-tenant requests fail with HTTP 403 Forbidden.
