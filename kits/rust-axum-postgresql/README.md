# Rust + Axum + PostgreSQL (SQLx) Stack Kit

A production-grade, zero-cost abstraction backend stack kit built with **Rust 1.81+**, **Axum 0.8+**, and **PostgreSQL 16** via **SQLx** with compile-time query verification.

## Stack Overview
- **Language**: Rust 1.81+ (Edition 2021)
- **Framework**: Axum 0.8+
- **Runtime**: Tokio 1.40+ (Multi-threaded async)
- **Database & Driver**: PostgreSQL 16+ via SQLx 0.8+ (Compile-time verified queries)
- **Middleware**: Tower-HTTP 0.6+ (CORS, Trace, Timeout, Compression)
- **Container**: Multi-stage Alpine container running as non-root `appuser` (UID 10001)

## Quickstart

### 1. Build & Run Tests
```bash
cd starter/
cargo test
```

### 2. Run Database Migrations
```bash
cargo sqlx migrate run
```

### 3. Run the Service
```bash
cargo run
```
Visit `http://localhost:3000/healthz` to verify live status.

### 4. Run with Docker Compose
```bash
docker compose up --build
```

## Security & Verification Standards
- Zero unsafe code policy (`#![deny(unsafe_code)]`).
- Compile-time SQL verification prevents SQL syntax and type errors at build time.
- Fully documented in [`VERIFICATION.md`](VERIFICATION.md).
