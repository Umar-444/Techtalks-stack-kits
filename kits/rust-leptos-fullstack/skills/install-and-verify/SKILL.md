---
name: install-and-verify
description: Install cargo-leptos build tool, compile the full-stack Leptos project, and verify the /healthz endpoint.
---

# Install and Verify: Rust + Leptos Full-Stack + Axum + WebAssembly

## Prerequisites
- Rust 1.80+ (`rustup default stable`)
- WebAssembly target: `rustup target add wasm32-unknown-unknown`
- `cargo-leptos` build runner: `cargo install cargo-leptos --locked`

## Quickstart Steps

1. **Configure Environment Variables**:
   ```bash
   cp starter/.env.example starter/.env
   ```

2. **Start Dev Server with Hot Reloading**:
   ```bash
   cd starter
   cargo leptos watch
   ```

3. **Verify Health Endpoint**:
   ```bash
   curl -i http://localhost:3000/healthz
   ```
   Expected response:
   ```json
   {
     "status": "ok",
     "app": "rust-leptos-fullstack",
     "version": "1.0.0",
     "runtime": "axum-wasm"
   }
   ```
