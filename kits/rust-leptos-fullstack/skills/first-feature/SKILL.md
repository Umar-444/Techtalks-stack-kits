---
name: first-feature
description: Author an interactive reactive Leptos component with fine-grained signals, server action forms, and Axum RPC.
---

# First Feature: Authoring a Reactive Leptos Component

## Step 1: Define Reactive Component
In `src/app.rs`:
```rust
use leptos::prelude::*;

#[component]
pub fn ItemManager() -> impl IntoView {
    let (items, set_items) = signal(vec!["Item A".to_string(), "Item B".to_string()]);
    let (input, set_input) = signal(String::new());

    let add_item = move |_| {
        let val = input.get();
        if !val.trim().is_empty() {
            set_items.update(|list| list.push(val.clone()));
            set_input.set(String::new());
        }
    };

    view! {
        <div class="p-6 max-w-lg mx-auto bg-slate-900 rounded-xl text-white">
            <h2 class="text-xl font-bold mb-4">"Reactive Items"</h2>
            <div class="flex gap-2 mb-4">
                <input
                    type="text"
                    class="bg-slate-800 border border-slate-700 px-3 py-2 rounded text-white"
                    placeholder="Enter item name..."
                    prop:value=input
                    on:input=move |ev| set_input.set(event_target_value(&ev))
                />
                <button
                    class="bg-blue-600 hover:bg-blue-500 px-4 py-2 rounded font-medium"
                    on:click=add_item
                >
                    "Add"
                </button>
            </div>
            <ul class="space-y-1">
                <For
                    each=move || items.get()
                    key=|item| item.clone()
                    children=move |item| view! { <li class="p-2 bg-slate-800 rounded">{item}</li> }
                />
            </ul>
        </div>
    }
}
```
