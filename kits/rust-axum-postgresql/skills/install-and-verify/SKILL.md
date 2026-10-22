---
name: install-and-verify
description: Complete toolchain setup, database migration, automated test execution, and health verification for Rust Axum PostgreSQL kit.
---

# Install and Verify Skill: Rust + Axum + PostgreSQL

## Overview
Verify Rust toolchain, compile the application, run database migrations, execute integration tests, and probe the live health endpoint.

## Step-by-Step Verification

### 1. Environment Verification
```bash
rustc --version
cargo --version
```
Ensure Rust 1.80+ is installed.

### 2. Dependency Audit & Build
```bash
cargo check
cargo test
```

### 3. Database Migration
```bash
cargo sqlx migrate run
```

### 4. Run the Service
```bash
cargo run &
sleep 2
curl -s http://localhost:3000/healthz
```
Expected output:
```json
{"status":"ok","app":"rust-axum-postgresql","version":"1.0.0"}
```
