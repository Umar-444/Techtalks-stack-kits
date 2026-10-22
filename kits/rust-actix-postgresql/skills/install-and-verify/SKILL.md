---
name: install-and-verify
description: Bootstrap local dependencies, start PostgreSQL container, run migrations, and verify the /healthz endpoint.
---

# Install and Verify: Rust + Actix Web + SeaORM + PostgreSQL

## Prerequisites
- Rust 1.80+ (`rustup default stable`)
- Docker & Docker Compose
- `sea-orm-cli` (`cargo install sea-orm-cli`)

## Quickstart Steps

1. **Configure Environment Variables**:
   ```bash
   cp starter/.env.example starter/.env
   ```

2. **Start PostgreSQL Database**:
   ```bash
   cd starter
   docker-compose up -d db
   ```

3. **Verify Database Connectivity and Run Migrations**:
   ```bash
   cargo run --bin migration up
   ```

4. **Start the Actix Web HTTP Server**:
   ```bash
   cargo run
   ```

5. **Verify Service Health**:
   ```bash
   curl -i http://localhost:8080/healthz
   ```
   Expected response:
   ```json
   {
     "status": "ok",
     "app": "rust-actix-postgresql",
     "version": "1.0.0",
     "runtime": "actix-tokio"
   }
   ```
