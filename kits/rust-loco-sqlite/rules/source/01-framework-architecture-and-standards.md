# Framework Architecture and Standards: Rust, Loco.rs, and SQLite

1. **Rails-Style MVC Architecture**: Loco.rs provides convention-over-configuration for Rust web services. Structure applications strictly into `src/app.rs` (lifecycle & routing), `src/controllers/` (HTTP handlers), `src/models/` (SeaORM active models), `src/views/` (response serializations), and `config/` (environment configuration).
2. **Underlying Axum and SeaORM Engine**: Leverage Loco's native Axum HTTP engine and SeaORM database integration without reinventing routing or ORM primitives. Keep controller actions lightweight and push business logic into model traits.
3. **Structured YAML Configuration**: Configure runtime environments declaratively in `config/development.yaml`, `config/test.yaml`, and `config/production.yaml`. Inject sensitive credentials (secrets, database URLs) via environment variable interpolation (`{{ get_env(name="DATABASE_URL", default="sqlite://db.sqlite?mode=rwc") }}`).
4. **Predictable Code Generation**: Use Loco CLI generators (`cargo loco generate model`, `cargo loco generate scaffold`) to establish consistent directory conventions, test fixtures, and schema migrations.
5. **No Unsafe Code Policy**: Enforce `#[deny(unsafe_code)]` crate-wide to ensure memory safety, concurrency guarantees, and crash prevention across all Axum handler worker threads.
