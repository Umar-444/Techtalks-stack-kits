---
name: wasm-hydration-optimization
description: Optimize WebAssembly binary size, implement code-splitting, and configure streaming SSR response buffering.
---

# WebAssembly Hydration & Performance Optimization

## Cargo Profile Settings for Production WASM
In `Cargo.toml`:
```toml
[profile.wasm-release]
inherits = "release"
opt-level = "z"
lto = true
codegen-units = 1
panic = "abort"
```

## Running `wasm-opt` in CI
Run the Binaryen `wasm-opt` tool on the compiled `.wasm` output:
```bash
wasm-opt -Oz -o target/site/pkg/app_bg.optimized.wasm target/site/pkg/app_bg.wasm
mv target/site/pkg/app_bg.optimized.wasm target/site/pkg/app_bg.wasm
```

## Streaming Server-Side Rendering
In `src/main.rs`:
```rust
use leptos_axum::LeptosRoutes;

let app = Router::new()
    .leptos_routes(&leptos_options, routes, {
        let leptos_options = leptos_options.clone();
        move || shell(leptos_options.clone())
    })
    .fallback(file_and_error_handler)
    .with_state(leptos_options);
```
Streaming allows the browser to receive and render the initial HTML skeleton immediately while async server functions compute concurrently.
