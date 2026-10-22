# Filament Admin Panel Standards

# Filament Admin Panel Standards

## 1. Declarative Table Construction
- Build tables using typed column components (`TextColumn`, `IconColumn`, `BadgeColumn`).
- Use `searchable()` with custom database scopes when querying large MySQL tables.
- Enable `sortable()` only on indexed database columns.

## 2. Form Schema Best Practices
- Structure complex forms with `Section` and `Grid` layouts.
- Always declare server-side validation rules using `required()`, `maxLength()`, `unique()`.
- Use `TextInput::make('email')->email()->unique(ignoreRecord: true)`.

## 3. Bulk Action Safety
- Wrap mass mutations in database transactions with deadlock retry mechanisms.
- Require confirmation modals for destructive bulk actions: `DeleteBulkAction::make()->requiresConfirmation()`.
