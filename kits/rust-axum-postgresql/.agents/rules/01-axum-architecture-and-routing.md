# Axum Routing, Handlers, and State Extraction Architecture

# Axum Routing, Handlers, and State Extraction Architecture

## 1. Modular Router Design
- Structure routers hierarchically using `Router::new().nest("/api/v1", api_routes)`.
- Handlers must be pure asynchronous functions accepting type-safe extractors:
  `async fn handler(State(pool): State<PgPool>, Json(payload): Json<CreateRequest>) -> Result<Json<Response>, AppError>`
- Place extractors in correct order: body extractors (`Json`, `Form`) must be the final argument.

## 2. Shared State Management
- Share thread-safe dependencies (database pools, caches, config) via `Router::with_state(app_state)`.
- Use shallow-cloneable handles (such as `PgPool` or `Arc<AppState>`).
- Never lock async execution blocks with synchronous mutexes (`std::sync::Mutex`); use `tokio::sync::Mutex` or lock-free channels.

## 3. Idiomatic Error Handling
- Use a unified `AppError` enum implementing `IntoResponse`:
  ```rust
  pub enum AppError {
      Database(sqlx::Error),
      NotFound(String),
      Validation(String),
      Unauthorized,
  }
  ```
- Map database errors to HTTP status codes cleanly without leaking internal connection strings or queries to clients.
