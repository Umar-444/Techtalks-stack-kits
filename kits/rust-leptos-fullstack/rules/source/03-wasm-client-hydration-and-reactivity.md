# WebAssembly Client Hydration and Reactivity

1. **Client Hydration Lifecycle**: Hydrate server-rendered HTML into an active reactive application via `leptos::mount_to_body` inside `src/lib.rs`. Ensure client signal initializers match server SSR rendered states to avoid hydration mismatches.
2. **Suspense and Resource Boundaries**: Wrap asynchronous queries in `create_resource` paired with `<Suspense fallback=...>`. This renders accessible fallback loading states during WASM initialization and dynamic fetches.
3. **WASM Binary Footprint Optimization**: Keep client WASM bundle sizes minimal. Compile release builds with `opt-level = "z"`, `lto = true`, `codegen-units = 1`, and run `wasm-opt -Oz` in CI pipelines to achieve fast mobile startup times.
4. **Client-Side Navigation**: Use Leptos `<Router>` and `<A>` components for instant zero-reload page transitions, preserving WebAssembly memory state and reactive signal trees across navigation events.
5. **Progressive Enhancement**: Implement forms using `<ActionForm>` so that basic user interactions succeed even before WebAssembly completes hydration over low-bandwidth connections.
