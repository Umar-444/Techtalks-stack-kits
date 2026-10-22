---
name: rust-leptos-fullstack-core
description: Core operations, isomorphic project layout, Cargo feature gating, and rootless Docker deployment.
---

# Core Operations: Rust + Leptos Full-Stack + Axum + WebAssembly

## Stack Highlights
- **Leptos 0.7+**: Isomorphic Rust web framework with fine-grained reactivity.
- **Axum 0.8+**: High-performance Tokio async backend engine.
- **WASM Hydration**: Zero-cost abstraction in browser via wasm-bindgen.
- **Security**: `#![deny(unsafe_code)]`, strict CSP wasm directives, non-root Alpine container (UID 10001).

## Project Layout
```text
starter/
├── Cargo.toml
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── src/
│   ├── app.rs          # Shared UI components, pages & routes
│   ├── lib.rs          # WebAssembly client hydration entrypoint
│   ├── main.rs         # Axum SSR server bootstrap & routing
│   └── handlers.rs     # Server healthcheck & API handlers
└── tests/
    └── api_test.rs     # Integration test suite
```

## Key Commands
- Development server: `cargo leptos watch`
- Check compilation: `cargo check --features ssr` and `cargo check --features hydrate`
- Build release artifacts: `cargo leptos build --release`
- Run test suite: `cargo test`
