---
name: rust-actix-postgresql-core
description: Core architectural patterns, project structure, error handling, Docker builds, and testing workflows.
---

# Core Operations: Rust + Actix Web + SeaORM + PostgreSQL

## Stack Highlights
- **Actix Web 4.9+**: Actor-based multi-threaded web server for ultra-high throughput.
- **SeaORM 1.1+**: Dynamic asynchronous ORM with active model validation.
- **PostgreSQL 16+**: ACID storage with bounded connection pooling.
- **Security**: `#![deny(unsafe_code)]`, non-root execution (UID 10001), CORS origin whitelisting.

## Project Structure
```text
starter/
├── Cargo.toml
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── src/
│   ├── main.rs         # Application entrypoint & HTTP server
│   ├── handlers.rs     # Route handlers & response formatting
│   ├── errors.rs       # Centralized AppError enum
│   ├── state.rs        # AppState container (SeaORM DatabaseConnection)
│   └── dtos.rs         # Validated request/response models
└── tests/
    └── api_test.rs     # Actix Web integration tests
```

## Common Commands
- Build dev binary: `cargo check`
- Run test suite: `cargo test`
- Build release container: `docker build -t actix-api .`
- Security scan: `cargo audit`
