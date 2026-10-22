# Agent Step-by-Step Build Order: Rust + Loco.rs + SeaORM + SQLite

1. **Step 1: Environment & Toolchain Setup**: Verify Rust 1.80+ and install Loco CLI via `cargo install loco-cli`. Copy `.env.example` to `.env`.
2. **Step 2: Database Storage & WAL Pragmas**: Configure SQLite connection URI with WAL mode (`_journal_mode=WAL`) and busy timeout (`_busy_timeout=5000`) in `config/development.yaml`.
3. **Step 3: Model & Migration Scaffolding**: Generate domain entities and declarative SeaORM migrations via `cargo loco generate scaffold`. Run migrations with `cargo loco db migrate`.
4. **Step 4: Controller Routing & Presentation Views**: Define route handlers implementing `Routes::new()` in `src/controllers/` and format responses into `src/views/` JSON envelopes.
5. **Step 5: Security Middleware & Input Validation**: Configure CORS whitelist in YAML config, apply `validator` derive macro on request DTOs, and configure JWT authentication for private routes.
6. **Step 6: Evaluation, Testing & Docker Packaging**: Run `cargo test` using in-memory SQLite instances and build multi-stage rootless Alpine Docker container with persistent `/app/storage` volume.
