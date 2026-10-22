# 05 Testing And Verification

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

