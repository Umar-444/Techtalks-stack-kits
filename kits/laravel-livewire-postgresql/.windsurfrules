# Laravel 12 + Livewire 4 + PostgreSQL - Agent Architecture & Rules

This project adheres to the TechTalks production standards for Laravel 12, Livewire 4, Volt single-file components, and PostgreSQL 16+.

# Rule 1: Laravel 12 + Livewire 4 Framework Conventions

## Context & Principles
- Follow modern Laravel 12 structure with single-file Livewire Volt components and declarative Folio page routing.
- Strictly enforce `declare(strict_types=1);` across all classes, actions, and component state classes.
- Keep components focused on UI interactivity; delegate domain calculations, payment flows, and complex queries to dedicated action classes.

## Standards
1. **Component Organization**: Place standard class-based Livewire components in `app/Livewire/` and single-file Volt components in `resources/views/livewire/`.
2. **State Hydration**: Keep component public properties minimal and strongly typed. Never expose raw Eloquent models as public properties without validation gates.
3. **Routing**: Leverage declarative Folio pages in `resources/views/pages/` or clean controllerless routes with `Route::get('/tasks', TaskManager::class)`.
4. **Asset Management**: Compile frontend assets via Vite with Tailwind CSS. Never inject unbundled script tags into individual components.

# Rule 2: Livewire Lifecycle, Morphing & Alpine Integration

## Context & Principles
- Understand and exploit the Livewire 3/4 request lifecycle: `mount()`, `boot()`, `hydrate()`, `updating()`, `updated()`, `render()`.
- Optimize DOM diffing (morphdom) by providing unique `wire:key` attributes on all dynamic list elements.

## Standards
1. **Input Debouncing**: Always debounce or blur real-time text input bindings (`wire:model.live.debounce.300ms="..."` or `wire:model.blur="..."`) to avoid spamming the backend with network requests.
2. **Keyed DOM Elements**: Every iteration loop in Blade must have an explicit `wire:key="{{ $task->id }}"`.
3. **Alpine.js Interactivity**: Use `x-data` and lightweight Alpine directives for purely client-side UI toggles (dropdowns, modals, tabs) to avoid unnecessary round-trips to the server.
4. **Events & Listeners**: Use `#[On('task-created')]` attributes for clean, decoupled component event communication.

# Rule 3: PostgreSQL 16+ ORM, UUIDs & Query Performance

## Context & Principles
- All database tables must utilize native PostgreSQL UUID primary keys to prevent ID enumeration.
- Eliminate N+1 query regressions during component re-renders.

## Standards
1. **UUID Primary Keys**: Every Eloquent model must use `Illuminate\Database\Eloquent\Concerns\HasUuids`.
2. **Eager Loading**: Always eager load relationships in the component `render()` method:
   ```php
   Task::query()->with(['user'])->latest()->paginate(15);
   ```
3. **Composite Indexes**: Declare explicit indexes in migrations on filtered and sorted column tuples (`$table->index(['status', 'created_at'])`).
4. **Atomic Mutations**: Wrap multi-model operations inside `DB::transaction()` to ensure relational consistency.

# Rule 4: Livewire Security, Authorization & Tampering Defense

## Context & Principles
- Maintain zero-trust web application hygiene: never trust data coming from the client browser, even on Livewire re-renders.
- Prevent parameter tampering, mass assignment, and unauthorized action execution.

## Standards
1. **Server-Side Authorization**: Every Livewire action method must assert authorization before executing:
   ```php
   $this->authorize('update', $task);
   ```
2. **Property Protection**: Use `#[Locked]` attributes on sensitive component state (e.g., IDs, tenant keys) to prevent client-side DOM payload tampering.
3. **Rate Limiting**: Apply `#[RateLimit(5, 60)]` on sensitive actions (login, reset password, email sending) to mitigate automated abuse.
4. **Session Fixation**: Rotate session IDs upon authentication events using `$request->session()->regenerate()`.

# Rule 5: Pest Testing, Component Assertions & Architectural Verification

## Context & Principles
- All Livewire components must be tested using Pest and the fluent `Livewire::test()` testing harness.
- Tests must assert rendered state, validation errors, and database mutations.

## Standards
1. **Component Unit Tests**: Assert initial render, input binding updates, and action dispatches:
   ```php
   Livewire::test(TaskManager::class)
       ->set('title', 'New Task')
       ->call('save')
       ->assertHasNoErrors()
       ->assertSee('New Task');
   ```
2. **Authorization Tests**: Verify that unauthorized users cannot execute restricted component actions:
   ```php
   Livewire::actingAs($unauthorizedUser)
       ->test(TaskManager::class)
       ->call('delete', $task->id)
       ->assertForbidden();
   ```
3. **Database Isolation**: Use `RefreshDatabase` trait to keep test runs idempotent and side-effect free.
