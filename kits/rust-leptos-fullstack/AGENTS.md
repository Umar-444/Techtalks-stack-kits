# Rust + Leptos Full-Stack + Axum + WebAssembly — Agent Operating Rules (AGENTS.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Table of Contents
- [01 Framework Architecture And Standards](#01-framework-architecture-and-standards)
- [02 Leptos Server Functions And Axum Integration](#02-leptos-server-functions-and-axum-integration)
- [03 Wasm Client Hydration And Reactivity](#03-wasm-client-hydration-and-reactivity)
- [04 Security Invariants And Content Security](#04-security-invariants-and-content-security)
- [05 Testing Verification And Ci](#05-testing-verification-and-ci)

---

<a id="01-framework-architecture-and-standards"></a>
## 01 Framework Architecture And Standards

# Framework Architecture and Standards: Rust, Leptos Full-Stack, and Axum

1. **Isomorphic Full-Stack Rust**: Leptos provides full-stack reactive web applications sharing one language, type definitions, and validation logic between browser WebAssembly and server Axum runtimes.
2. **Feature-Gated Dependency Separation**: Partition Cargo dependencies strictly using `ssr` and `hydrate` features. Ensure server-only crates (database pools, secret management, file I/O) are compiled exclusively under `#[cfg(feature = "ssr")]` to avoid bloating the client WASM bundle.
3. **Fine-Grained Reactive Signals**: Structure UI state using fine-grained signals (`create_signal`, `create_memo`, `create_resource`). Avoid monolithic state objects; mutate only individual DOM nodes connected to updated signals without Virtual DOM diffing.
4. **Isomorphic App Entrypoint**: Keep core routing, layout components, and pages inside `src/app.rs`. Provide `src/main.rs` as the Axum SSR server entrypoint and `src/lib.rs` as the `wasm_bindgen` client hydration hook.
5. **No Unsafe Code Policy**: Enforce `#[deny(unsafe_code)]` crate-wide to ensure memory safety, concurrency guarantees, and crash prevention across both server Tokio tasks and browser WebAssembly threads.


---

<a id="02-leptos-server-functions-and-axum-integration"></a>
## 02 Leptos Server Functions And Axum Integration

# Leptos Server Functions and Axum Integration

1. **Type-Safe RPC via Server Functions**: Define backend endpoints using Leptos `#[server(Prefix, "/api")]` macros. Server functions act as ordinary async Rust functions on the client while compiling to Axum HTTP handlers on the server.
2. **Server Context Dependency Injection**: Access database connections, cache clients, and configuration within server functions using `leptos_axum::extract()` or `use_context::<AppState>()`.
3. **Strict Input Sanitization**: Validate all server function arguments using the `validator` crate or manual invariant checks prior to database interactions. Reject malformed payloads immediately with typed `ServerFnError`.
4. **Serialization Safety**: Configure server function payloads with Serde JSON or Postcard serialization. Never transmit raw sensitive internal records (e.g. password hashes, database connection strings) across the server function boundary.
5. **Streaming Server-Side Rendering (SSR)**: Wrap asynchronous data loaders in `<Suspense>` components. Enable HTTP response streaming in Axum to dispatch early HTML headers and skeletons while async server functions resolve.


---

<a id="03-wasm-client-hydration-and-reactivity"></a>
## 03 Wasm Client Hydration And Reactivity

# WebAssembly Client Hydration and Reactivity

1. **Client Hydration Lifecycle**: Hydrate server-rendered HTML into an active reactive application via `leptos::mount_to_body` inside `src/lib.rs`. Ensure client signal initializers match server SSR rendered states to avoid hydration mismatches.
2. **Suspense and Resource Boundaries**: Wrap asynchronous queries in `create_resource` paired with `<Suspense fallback=...>`. This renders accessible fallback loading states during WASM initialization and dynamic fetches.
3. **WASM Binary Footprint Optimization**: Keep client WASM bundle sizes minimal. Compile release builds with `opt-level = "z"`, `lto = true`, `codegen-units = 1`, and run `wasm-opt -Oz` in CI pipelines to achieve fast mobile startup times.
4. **Client-Side Navigation**: Use Leptos `<Router>` and `<A>` components for instant zero-reload page transitions, preserving WebAssembly memory state and reactive signal trees across navigation events.
5. **Progressive Enhancement**: Implement forms using `<ActionForm>` so that basic user interactions succeed even before WebAssembly completes hydration over low-bandwidth connections.


---

<a id="04-security-invariants-and-content-security"></a>
## 04 Security Invariants And Content Security

# Security Invariants, Content Security Policy, and CORS

1. **Strict WebAssembly Content Security Policy**: Deploy strict CSP response headers via Axum middleware (`default-src 'self'; script-src 'self' 'wasm-unsafe-eval'; style-src 'self' 'unsafe-inline'`). Prevent script injection while allowing WASM module compilation.
2. **Server Function Authorization**: Protect sensitive server functions with session or bearer token verification extracted from Axum request headers. Never rely on client-side routing guards alone for data authorization.
3. **CORS Origin Filtering**: Whitelist allowed API origins strictly from the `ALLOWED_ORIGINS` environment variable in the Axum HTTP layer; reject permissive wildcard origins (`*`).
4. **Non-Root Container Hardening**: Build statically linked release server binaries and package into minimal Alpine Linux runtime containers executing as unprivileged user `USER 10001:10001`.
5. **Denial-of-Service Defense**: Apply Axum request body limits (`DefaultBodyLimit::max(262_144)`) and timeout middleware to guard server function endpoints against memory exhaustion and Slowloris attacks.


---

<a id="05-testing-verification-and-ci"></a>
## 05 Testing Verification And Ci

# Testing, Verification, and CI Standards

1. **Axum Server Integration Testing**: Verify SSR routes, server functions, and health probes using `axum::test` harnesses and standard Tokio test runners.
2. **WebAssembly Headless Testing**: Author client component interaction tests using `wasm-bindgen-test` to verify signal propagation and DOM event handlers inside headless browser environments.
3. **Health and Readiness Probes**: Expose `/healthz` returning HTTP 200 and machine-readable service status for container healthchecks.
4. **Supply Chain Security**: Enforce `cargo audit` in CI to detect vulnerabilities in dependencies and verify license compliance with `cargo deny`.
5. **Transpiler Zero-Drift**: Validate that all 6 agent dialects match source rules using `python tools/transpiler.py --check` in continuous integration.


---

