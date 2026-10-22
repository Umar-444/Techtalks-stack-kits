---
name: leptos-server-functions
description: Build type-safe server functions that seamlessly bridge client WASM to server Axum services.
---

# Leptos Server Functions RPC Pattern

## Defining a Server Function
Server functions are defined with `#[server]`. They are callable as ordinary async Rust functions from WASM, while executing exclusively on the server inside the Axum runtime:

```rust
use leptos::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct ServerItem {
    pub id: i32,
    pub name: String,
}

#[server(GetServerItems, "/api")]
pub async fn get_server_items() -> Result<Vec<ServerItem>, ServerFnError> {
    // Only compiles on the server (#[cfg(feature = "ssr")])
    Ok(vec![
        ServerItem { id: 1, name: "Production WASM Binary".to_string() },
        ServerItem { id: 2, name: "Server-Side Rendered Axum Route".to_string() },
    ])
}
```

## Consuming in Components with Suspense
```rust
#[component]
pub fn ServerItemView() -> impl IntoView {
    let items_resource = Resource::new(|| (), |_| async move { get_server_items().await });

    view! {
        <Suspense fallback=move || view! { <p class="text-slate-400">"Loading items..."</p> }>
            {move || Suspend(async move {
                match items_resource.await {
                    Ok(items) => view! {
                        <ul>
                            {items.into_iter().map(|it| view! { <li>{it.name}</li> }).collect_view()}
                        </ul>
                    }.into_any(),
                    Err(e) => view! { <p class="text-red-400">{format!("Error: {}", e)}</p> }.into_any(),
                }
            })}
        </Suspense>
    }
}
```
