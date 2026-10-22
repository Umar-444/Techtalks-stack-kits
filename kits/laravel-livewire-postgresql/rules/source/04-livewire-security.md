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
