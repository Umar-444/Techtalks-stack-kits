---
title: "Livewire Security & Property Locking"
description: "Defending against client-side property manipulation and unauthorized actions."
globs: ["app/Livewire/**/*.php", "resources/views/livewire/**/*.blade.php"]
---

# Livewire Security & Property Locking

1. **Property Locking:**
   - Always decorate IDs, user references, and computed values with `#[Locked]`.
   - Never trust client-sent property values without re-verification.

2. **Action Authorization:**
   - Public component methods must call `$this->authorize('action', $model)` before execution.
