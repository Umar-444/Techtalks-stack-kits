---
name: laravel-policy
description: Enforce zero-trust BOLA authorization policies, multi-tenant scoping, and role-based gate checks in Filament.
---

# Skill: Laravel Policy Authorization

## Workflow
1. Create policy: `php artisan make:policy CustomerPolicy --model=Customer`.
2. Implement `viewAny(User $user)`, `view(User $user, Customer $customer)`.
3. Verify tenant boundary: `$user->team_id === $customer->team_id`.

## Done Means
- BOLA vulnerability attempts return HTTP 403.
