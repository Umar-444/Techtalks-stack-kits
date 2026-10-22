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
