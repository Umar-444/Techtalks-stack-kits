---
name: rust-loco-sqlite-core
description: Core operations, MVC generators, SQLite storage persistence, and Docker deployment workflows.
---

# Core Operations: Rust + Loco.rs + SeaORM + SQLite

## Stack Highlights
- **Loco.rs 0.13+**: The Rails of Rust—conventions, generators, background workers, and mailers.
- **Axum Web Engine**: Underlying lightning-fast Tokio async HTTP router.
- **SeaORM 1.1+**: Type-safe dynamic ORM and declarative migrations.
- **SQLite 3.45+**: Zero-ceremony serverless embedded database tuned with WAL mode.

## Project Structure
```text
starter/
├── config/
│   ├── development.yaml
│   ├── test.yaml
│   └── production.yaml
├── migration/
│   └── src/
├── src/
│   ├── app.rs          # Application lifecycle and route registration
│   ├── main.rs         # Loco CLI entrypoint
│   ├── controllers/    # HTTP route handlers
│   ├── models/         # SeaORM models and entities
│   └── views/          # JSON response presenters
├── Cargo.toml
├── Dockerfile
└── tests/
```

## Essential CLI Commands
- Start dev server: `cargo loco start`
- Run database migrations: `cargo loco db migrate`
- Check routing table: `cargo loco routes`
- Run test suite: `cargo test`
