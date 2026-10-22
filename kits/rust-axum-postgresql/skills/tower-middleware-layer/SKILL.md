---
name: tower-middleware-layer
description: Layering Tower-HTTP middleware for distributed tracing, CORS, timeouts, and payload compression.
---

# Tower Middleware Layer Skill

## Overview
Compose modular network layers to protect, trace, and accelerate Axum HTTP services.

## Configuration Pattern
```rust
use tower_http::{cors::CorsLayer, trace::TraceLayer, timeout::TimeoutLayer, compression::CompressionLayer};

let middleware = tower::ServiceBuilder::new()
    .layer(TraceLayer::new_for_http())
    .layer(TimeoutLayer::new(Duration::from_secs(10)))
    .layer(CompressionLayer::new())
    .layer(CorsLayer::permissive());

let app = Router::new().layer(middleware);
```
