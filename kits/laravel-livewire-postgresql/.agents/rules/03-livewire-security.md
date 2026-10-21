# Livewire Security & Property Locking

# Livewire Security & Property Locking

1. **Property Locking:**
   - Always decorate IDs, user references, and computed values with `#[Locked]`.
   - Never trust client-sent property values without re-verification.

2. **Action Authorization:**
   - Public component methods must call `$this->authorize('action', $model)` before execution.
