# Agent Step-by-Step Build Order: Rust + Actix Web + SeaORM + PostgreSQL

1. **Step 1: Environment & Toolchain Setup**: Initialize Rust toolchain (`rustup default stable`), configure environment variables from `.env.example`, and start PostgreSQL via Docker Compose.
2. **Step 2: Database Schema & SeaORM Entities**: Author database migrations using SeaORM migration tools and define active models and relational entities.
3. **Step 3: Service State & Connection Pooling**: Initialize `sea_orm::ConnectOptions` with bounded pool parameters and encapsulate inside `web::Data<AppState>`.
4. **Step 4: HTTP Routing & Scope Registration**: Mount `/healthz` and modular `/api/v1` routes with typed request DTO validation.
5. **Step 5: Security Middleware & Hardening**: Apply `actix_cors::Cors` with whitelist filtering from `ALLOWED_ORIGINS`, enforce 256 KB JSON body limits, and implement unified `AppError`.
6. **Step 6: Testing, Evaluation & Containerization**: Execute `cargo test` using `actix_web::test` harnesses and build multi-stage rootless Docker container.
