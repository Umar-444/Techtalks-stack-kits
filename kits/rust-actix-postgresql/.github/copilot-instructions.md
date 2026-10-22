# GitHub Copilot Instructions for Rust + Actix Web + SeaORM + PostgreSQL
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## 01 Framework Architecture And Standards
﻿# Framework Architecture and Standards: Rust, Actix Web, and SeaORM

1. **Actor Model and Multi-Threaded Workers**: Actix Web spawns dedicated worker threads (defaulting to the host CPU core count) each running their own single-threaded Tokio event loop. Application factory closures passed to `HttpServer::new` must be `Send + Clone + 'static`.
2. **Layered Domain Separation**: Structure source code into modular layers: `main.rs` (server bootstrapping and pool lifecycle), `handlers.rs` (HTTP request decoding and response presentation), `entities/` (SeaORM active models and schema bindings), `errors.rs` (unified error handling enum), and `state.rs` (shared application state). Never embed raw SQL or business transactions directly inside router declarations.
3. **Structured Configuration via Environment**: Load configuration via `dotenvy::dotenv()` and parse strongly-typed environment structs using `serde`. Support `DATABASE_URL`, `PORT`, `HOST`, `WORKER_THREADS`, and `ALLOWED_ORIGINS` with safe fallback defaults for local development.
4. **Graceful Shutdown and Signal Trapping**: Configure Actix Web HTTP server shutdown with proper signal traps for `SIGINT` and `SIGTERM`. Ensure in-flight HTTP requests complete and SeaORM connection pools gracefully flush before the process exits.
5. **No Unsafe Code Policy**: Enforce `#[deny(unsafe_code)]` at the crate root to guarantee memory safety, data-race freedom, and thread safety across all Actix worker threads.


## 02 Seaorm Entities And Postgresql Pooling
﻿# SeaORM Entities and PostgreSQL Connection Pooling

1. **SeaORM Dynamic ORM Patterns**: Define domain models using SeaORM entity macros (`#[derive(Clone, Debug, PartialEq, DeriveEntityModel, Serialize, Deserialize)]`). Keep entity schema, columns, and relations tightly typed.
2. **PostgreSQL Connection Pool Hardening**: Configure `sea_orm::ConnectOptions` with strict limits: `max_connections(25)`, `min_connections(5)`, `connect_timeout(Duration::from_secs(5))`, `acquire_timeout(Duration::from_secs(3))`, and `idle_timeout(Duration::from_secs(600))`. Never use unbounded database pools in production.
3. **Strict Parameterized Queries**: All SeaORM query builders compile down to SQLx parameterized queries with bound placeholders (`$1`, `$2`). Raw string concatenation or dynamic query formatting is strictly forbidden.
4. **Isolated Migration System**: Maintain database migrations inside an isolated migration crate or module. Execute migrations automatically on server startup or via `sea-orm-cli migrate up` prior to traffic ingestion.
5. **Atomic Transaction Encapsulation**: Wrap multi-entity mutations inside SeaORM transactions (`db.transaction::<_, _, DbErr>(|txn| Box::pin(async move { ... }))`) to guarantee ACID consistency and rollback on failure.


## 03 Api Routing And Error Handling
﻿# API Routing and Unified Error Handling

1. **Modular Scope Routing**: Group API endpoints logically under `web::scope("/api/v1")`. Bind route handlers with explicit HTTP verb macros (`web::get()`, `web::post()`, `web::put()`, `web::delete()`).
2. **Type-Safe State Extraction**: Inject database connections and configuration using Actix `web::Data<AppState>`. Never rely on global mutable singletons or static variables.
3. **Unified ResponseError Enum**: Define a centralized `AppError` enum implementing `actix_web::ResponseError`. Override `error_response(&self) -> HttpResponse` to output uniform JSON envelopes (`{"error": {"code": ..., "message": ...}}`).
4. **Information Disclosure Prevention**: Capture underlying `sea_orm::DbErr` or I/O errors and log details internally with `tracing::error!()`. Return safe, generic HTTP 500 error messages to API consumers to prevent schema exposure.
5. **Structured JSON Responses**: Standardize all successful API responses into predictable JSON structures (`{"data": ..., "meta": ...}`) with appropriate HTTP status codes (200, 201, 204).


## 04 Security Invariants And Input Validation
﻿# Security Invariants, CORS, and Input Validation

1. **Strict CORS Whitelist**: Configure `actix_cors::Cors` explicitly from the `ALLOWED_ORIGINS` environment variable. Never configure permissive wildcard origins (`allow_any_origin()`) on authenticated routes.
2. **Payload Size Guardrails**: Configure `web::JsonConfig::default().limit(262_144)` (256 KB) to prevent memory exhaustion and Denial-of-Service attacks from oversized request bodies.
3. **DTO Input Validation**: Implement the `validator::Validate` derive macro on all request DTOs. Validate string lengths, email formats, and numerical bounds before passing data to entities.
4. **Pagination Bounds Clamping**: All list and search endpoints must enforce pagination clamps (`limit` clamped between 1 and 100, `offset` >= 0) to avoid unbounded table scans.
5. **Non-Root Container Hardening**: Build statically linked release binaries and package into minimal Alpine Linux runtime containers executing as unprivileged user `USER 10001:10001`.


## 05 Testing Verification And Ci
﻿# Testing, Verification, and CI Standards

1. **Actix Web Integration Harness**: Test API handlers using `actix_web::test` utilities (`test::init_service`, `test::TestRequest`, `test::call_service`, and `test::read_body_json`) for fast, true-to-runtime verification.
2. **SeaORM Mock Database Testing**: Use SeaORM's `MockDatabase` backend to verify entity CRUD and transaction logic in isolated unit tests without requiring a running PostgreSQL server.
3. **Health and Readiness Endpoints**: Expose `/healthz` and `/health` endpoints returning HTTP 200 and machine-readable service status for Kubernetes and Docker container healthchecks.
4. **Automated Supply Chain Audits**: Enforce `cargo audit` in CI pipelines to prevent known vulnerable dependencies from reaching production builds.
5. **Transpiler Zero-Drift**: Run `python tools/transpiler.py --check` in continuous integration to verify that all 6 agent dialects match source rules with zero drift.


