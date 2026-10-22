# Agent Build Steps: Laravel 12/13 Sanctum REST API Kit

Deterministic chronological instructions for AI coding agents and automated CI builders:

## Step 1: Environment & Dependency Initialization
```bash
cd starter
cp .env.example .env
composer install --no-interaction --prefer-dist
php artisan key:generate
```

## Step 2: Database Migration & Schema Setup
```bash
php artisan migrate --force
```
Verifies creation of `users`, `personal_access_tokens`, and `projects` tables with foreign keys.

## Step 3: Sanctum Configuration & Ability Setup
Verify `config/sanctum.php` has:
- `'expiration' => 10080` (7 days)
- Token ability middleware registered in bootstrap or HTTP kernel (`ability`, `abilities`).

## Step 4: Spatie Query Builder Integration
Verify `ProjectController::index` utilizes `QueryBuilder::for(Project::class)` with:
- `allowedFilters(['status', 'title', AllowedFilter::scope('search')])`
- `allowedSorts(['created_at', 'title', 'priority'])`
- `allowedIncludes(['user'])`

## Step 5: BOLA Policy & Authorization Verification
Verify `ProjectPolicy` enforces:
- `view(User $user, Project $project): bool => $user->id === $project->user_id`
- `update(User $user, Project $project): bool => $user->id === $project->user_id`
- `delete(User $user, Project $project): bool => $user->id === $project->user_id`

## Step 6: Test Suite Execution
```bash
php artisan test
```
All feature and unit tests must exit with code 0.
