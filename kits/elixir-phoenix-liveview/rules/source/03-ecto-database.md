# Rule 3: Ecto 3.11+ Schema, Changesets & Migrations

## Context & Principles
- Validate all incoming data at the application boundary using Ecto Changesets before writing to PostgreSQL.
- Keep database queries compile-time checked using Ecto.Query macros.

## Standards
1. **Changeset Validation**: Never bypass `cast/4` and `validate_required/3`. Apply custom validators for format, constraints, and business logic.
2. **Migrations**: Write reversible migrations using `change/0` with proper `null: false` constraints, default values, and foreign key references with `on_delete: :delete_all` or `:nothing`.
3. **Indexes**: Explicitly create indexes in migrations for foreign keys and timestamp sort columns (`create index(:items, [:inserted_at])`).
4. **Transactions**: Use `Ecto.Multi` for coordinated writes across multiple tables to ensure atomicity.
