---
name: first-feature
description: Build the canonical first feature: Real-time Task Manager Livewire component with optimistic updates, UUID keys, and authorization policies.
---

# First Feature Skill: Real-time Task Manager Component

## Objective
Construct a reactive Task management module adhering to the 18-checkpoint standard:
1. PostgreSQL migration with UUID primary key and composite status index.
2. Eloquent model with HasUuids and strict fillable properties.
3. Laravel Gate/Policy enforcing BOLA authorization.
4. Livewire component handling real-time task creation, toggling, and deletion.
5. Pest test verifying live component reactivity and access control.

## Implementation Steps
1. Create Migration in `database/migrations/2026_10_22_000002_create_tasks_table.php`.
2. Define Model in `app/Models/Task.php` with `HasUuids`.
3. Create Policy in `app/Policies/TaskPolicy.php` checking `$user->id === $task->user_id`.
4. Implement Livewire Component in `app/Livewire/TaskManager.php`.
5. Implement Blade View in `resources/views/livewire/task-manager.blade.php`.

## Done Means
A user creates a task in the browser form, task renders instantly in the list via Livewire DOM morphing, data persists in PostgreSQL, and unauthorized users cannot mutate tasks.
