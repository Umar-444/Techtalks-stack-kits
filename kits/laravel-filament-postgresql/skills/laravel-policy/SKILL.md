---
name: "laravel-policy"
description: "Generate strict BOLA-resistant model authorization gates and policies."
version: "1.0.0"
author: "TechTalks Stack Kits"
---

# Laravel Policy Generator Skill

Use this skill whenever creating an authorization policy to defend against Broken Object-Level Authorization (BOLA).

## Workflow

1. **Generate Policy:**
   ```bash
   php artisan make:policy {ModelName}Policy --model={ModelName}
   ```

2. **Policy Invariants:**
   - Always verify tenant or ownership boundaries:
     ```php
     public function update(User $user, Order $order): bool
     {
         return $user->id === $order->user_id || $user->hasRole('Superadmin');
     }
     ```
   - Never allow automatic `true` returns in `update` or `delete` methods.
   - Superadmin bypass must be centralized in `AuthServiceProvider` or `AppServiceProvider` using `Gate::before`.
