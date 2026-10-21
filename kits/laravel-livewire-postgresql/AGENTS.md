# Laravel 12 + Livewire 4 + PostgreSQL — Agent Operating Rules (AGENTS.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Table of Contents
- [Livewire 4, Volt & Folio Conventions](#01-livewire-volt-folio)
- [Flux UI Standards](#02-flux-ui-standards)
- [Livewire Security & Property Locking](#03-livewire-security)

---

<a id="01-livewire-volt-folio"></a>
## Livewire 4, Volt & Folio Conventions

# Livewire 4, Volt & Folio Conventions

1. **Volt Single-File Components:**
   - Use Volt functional or class-based syntax inside `resources/views/livewire/`.
   - Keep state properties strictly typed (`public string $query = '';`).

2. **Folio Page Routing:**
   - Organize URL routes as `.blade.php` pages under `resources/views/pages/`.
   - Apply middleware in Volt components using `middleware(['auth', 'verified'])`.

---

<a id="02-flux-ui-standards"></a>
## Flux UI Standards

# Flux UI Standards

1. **Primitive Composition:**
   - Use standard `<flux:button>`, `<flux:input>`, and `<flux:card>` elements.
   - Bind primary color actions to `#E85D26`.

2. **Accessibility:**
   - Every input element must have an associated `<flux:label>`.
   - Dark mode styling must use `dark:` Tailwind variants.

---

<a id="03-livewire-security"></a>
## Livewire Security & Property Locking

# Livewire Security & Property Locking

1. **Property Locking:**
   - Always decorate IDs, user references, and computed values with `#[Locked]`.
   - Never trust client-sent property values without re-verification.

2. **Action Authorization:**
   - Public component methods must call `$this->authorize('action', $model)` before execution.

---

