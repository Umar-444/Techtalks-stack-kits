# Assistant Guidelines for Rust + Axum + PostgreSQL Stack Kit

## Stack Overview
- Language: Rust 1.81+ (Edition 2021)
- Framework: Axum 0.8+
- Runtime: Tokio 1.40+ (Multi-threaded async)
- Database: PostgreSQL 16+ via SQLx 0.8+ (Compile-time verified queries)
- Middleware: Tower-HTTP 0.6+ (CORS, Trace, Timeout, Compression)
- Security: #![deny(unsafe_code)], cargo-audit, non-root Alpine container

## Mandatory Rules
1. Zero unparameterized SQL queries. Always use SQLx query macros with bind parameters ($1, $2).
2. All handlers must return Result<Json<T>, AppError> with explicit error status codes.
3. Apply Tower-HTTP layers for timeout (15s), CORS, and Tracing on all API routes.
4. Bound connection pools using PgPoolOptions with explicit max_connections and timeouts.
5. In-memory integration tests must use oneshot requests to verify status codes and payloads.
