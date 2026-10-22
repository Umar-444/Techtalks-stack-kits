# Agent Step-by-Step Build Order: Rust + Leptos Full-Stack + Axum + WebAssembly

1. **Step 1: Environment & Toolchain Setup**: Install Rust stable toolchain, add the `wasm32-unknown-unknown` target, and install `cargo-leptos`. Copy `.env.example` to `.env`.
2. **Step 2: Component Architecture & Routing**: Define shared UI components, routes, and layout shell in `src/app.rs` using fine-grained reactive signals (`signal`, `memo`, `resource`).
3. **Step 3: Server Functions & Axum Integration**: Declare backend endpoints with `#[server]` functions, injecting database or cache state via Leptos context extractors.
4. **Step 4: Client Hydration Hook**: Configure WebAssembly entrypoint in `src/lib.rs` with `#[wasm_bindgen]` and `leptos::mount::hydrate_body`.
5. **Step 5: Security Headers & CSP**: Configure Axum response middleware to emit strict Content Security Policy headers permitting WebAssembly evaluation while rejecting unauthorized scripts.
6. **Step 6: Evaluation, Testing & Docker Packaging**: Run `cargo test --features ssr`, optimize WebAssembly with `wasm-opt`, and package into multi-stage rootless Alpine Docker image.
