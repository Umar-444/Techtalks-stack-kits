# Async Tokio Runtime Concurrency and Integration Testing

# Async Tokio Runtime Concurrency and Integration Testing

## 1. Runtime Isolation
- Execute the service under the multi-threaded Tokio runtime: `#[tokio::main]`.
- Avoid blocking worker threads. Offload CPU-heavy tasks or blocking file I/O to `tokio::task::spawn_blocking`.

## 2. Direct In-Memory Integration Testing
- Test endpoints directly using `tower::ServiceExt::oneshot` and `axum::http::Request`:
  ```rust
  let response = app
      .oneshot(Request::builder().uri("/healthz").body(Body::empty()).unwrap())
      .await
      .unwrap();
  assert_eq!(response.status(), StatusCode::OK);
  ```
- Guarantees fast, reproducible test execution without binding physical TCP ports.
