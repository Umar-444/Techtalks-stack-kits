---
name: filament-resource
description: Scaffold and configure Filament 4 admin panel resources, form schemas, and table actions.
---

# Filament Resource Skill

## Purpose
Enables deterministic creation of Filament panel resources adhering to clean architectural boundaries.

## Key Workflows
```bash
php artisan make:filament-resource Customer --generate
```

## Standards
- Always define typed schema methods `form(Form $form): Form` and `table(Table $table): Table`.
- Eager load relationships using `->modifyQueryUsing(fn ($query) => $query->with(['account']))`.
- Ensure all actions utilize modal confirmation dialogs for destructive operations.

## Done Means
Filament resource generates successfully, all form fields validate strictly against database column constraints, and N+1 query regressions are eliminated on table view.
