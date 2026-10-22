---
name: install-and-verify
description: Install Loco CLI tool, initialize local SQLite database, run migrations, and verify the /healthz endpoint.
---

# Install and Verify: Rust + Loco.rs + SeaORM + SQLite

## Prerequisites
- Rust 1.80+ (`rustup default stable`)
- Loco CLI: `cargo install loco-cli`
- SQLite 3.45+

## Quickstart Steps

1. **Configure Environment Variables**:
   ```bash
   cp starter/.env.example starter/.env
   ```

2. **Initialize SQLite Database & Run Migrations**:
   ```bash
   cd starter
   cargo loco db migrate
   ```

3. **Start the Loco Application Server**:
   ```bash
   cargo loco start
   ```

4. **Verify Health Endpoint**:
   ```bash
   curl -i http://localhost:5150/healthz
   ```
   Expected response:
   ```json
   {
     "status": "ok",
     "app": "rust-loco-sqlite",
     "version": "1.0.0",
     "framework": "loco.rs"
   }
   ```
