# SECURITY.md — Livewire 4 Security Standards

1. **Property Locking:**
   All component properties that should not be manipulated by the client must have the `#[Locked]` attribute.

2. **Authorization on Actions:**
   Every public Livewire action method must perform an authorization check ($this->authorize).

3. **Input Validation:**
   All user inputs bound to Livewire models must be validated using `$this->validate()` with strict rules.
