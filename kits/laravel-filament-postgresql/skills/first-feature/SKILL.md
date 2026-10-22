---
name: first-feature
description: Build the canonical first feature: Customer Resource with UUID keys, BOLA authorization policy, and Filament table/form schema.
---

# First Feature Skill: Customer Resource & Policy

## Objective
Implement an end-to-end multi-tenant Customer management module adhering to the 18-checkpoint standard:
1. PostgreSQL migration with UUID primary key and composite indexes.
2. Eloquent model with HasUuids and strict attribute casting.
3. Laravel Gate/Policy enforcing Broken Object Level Authorization (BOLA) defenses.
4. Filament Resource with searchable, sortable tables and validated form inputs.
5. Pest feature test verifying access control and query bounds.

## Procedure Steps

### 1. Database Migration
```php
Schema::create('customers', function (Blueprint $table) {
    $table->uuid('id')->primary();
    $table->string('name');
    $table->string('email')->unique();
    $table->string('status')->default('active');
    $table->timestamps();
    $table->index(['status', 'created_at']);
});
```

### 2. Model Definition
Use `Illuminate\Database\Eloquent\Concerns\HasUuids` in `app/Models/Customer.php`.

### 3. Policy Authorization
Register `CustomerPolicy` and assert that standard users can only view their own organization's records:
```php
public function view(User $user, Customer $customer): bool
{
    return $user->id === $customer->user_id || $user->hasRole('super-admin');
}
```

### 4. Filament Resource
Generate `app/Filament/Resources/CustomerResource.php` defining form inputs and table columns.

## Done Means
An admin logs into `/admin`, navigates to Customers, creates a new record with auto-generated UUID, and non-admin users attempting direct URL access are rejected with HTTP 403 Forbidden.
