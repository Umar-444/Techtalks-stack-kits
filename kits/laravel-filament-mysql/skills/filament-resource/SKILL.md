---
name: filament-resource
description: Scaffold and customize Filament 4 admin resources, form layouts, bulk actions, and relationship managers.
---

# Skill: Filament Resource Scaffolding

## Workflow
1. Run `php artisan make:filament-resource <Entity>`.
2. Configure form schema inside `form(Form $form): Form`.
3. Configure table schema inside `table(Table $table): Table`.
4. Register bulk actions with confirmation modals.

## Done Means
- Resource registered in navigation.
- Table pagination, sorting, and filtering operational.
