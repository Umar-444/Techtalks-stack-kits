# Laravel 12 + Livewire 4 + PostgreSQL — Claude Code Guidelines (CLAUDE.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Quick Reference & Non-Negotiable Standards
### Livewire 4, Volt & Folio Conventions
> Single-file component patterns, reactive properties, and Folio routing.

# Livewire 4, Volt & Folio Conventions

1. **Volt Single-File Components:**
   - Use Volt functional or class-based syntax inside `resources/views/livewire/`.
   - Keep state properties strictly typed (`public string $query = '';`).

2. **Folio Page Routing:**
   - Organize URL routes as `.blade.php` pages under `resources/views/pages/`.
   - Apply middleware in Volt components using `middleware(['auth', 'verified'])`.

### Flux UI Standards
> Component composition, responsive layout, and design token integration.

# Flux UI Standards

1. **Primitive Composition:**
   - Use standard `<flux:button>`, `<flux:input>`, and `<flux:card>` elements.
   - Bind primary color actions to `#E85D26`.

2. **Accessibility:**
   - Every input element must have an associated `<flux:label>`.
   - Dark mode styling must use `dark:` Tailwind variants.

### Livewire Security & Property Locking
> Defending against client-side property manipulation and unauthorized actions.

# Livewire Security & Property Locking

1. **Property Locking:**
   - Always decorate IDs, user references, and computed values with `#[Locked]`.
   - Never trust client-sent property values without re-verification.

2. **Action Authorization:**
   - Public component methods must call `$this->authorize('action', $model)` before execution.

