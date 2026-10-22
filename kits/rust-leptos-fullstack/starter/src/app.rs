use leptos::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct HealthResponse {
    pub status: String,
    pub app: String,
    pub version: String,
    pub runtime: String,
}

#[component]
pub fn App() -> impl IntoView {
    let (count, set_count) = signal(0);

    view! {
        <main class="min-h-screen bg-slate-950 p-8 text-slate-100 flex flex-col items-center justify-center">
            <div class="max-w-md w-full bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl text-center">
                <span class="inline-block px-3 py-1 bg-orange-950 text-orange-400 border border-orange-800 rounded-full text-xs font-semibold tracking-wide uppercase mb-3">
                    "Rust + Leptos 0.7 + Axum"
                </span>
                <h1 class="text-3xl font-extrabold tracking-tight mb-2">"Full-Stack WebAssembly"</h1>
                <p class="text-slate-400 text-sm mb-6">
                    "Fine-grained reactive signals in browser WASM, Axum server-side rendering, and zero-overhead RPC."
                </p>

                <div class="flex items-center justify-center gap-4 bg-slate-800 p-4 rounded-xl border border-slate-700">
                    <span class="text-slate-300 text-sm">"Reactive Counter:"</span>
                    <span class="text-2xl font-bold text-orange-400 font-mono">{move || count.get()}</span>
                    <button
                        class="px-4 py-2 bg-orange-600 hover:bg-orange-500 active:scale-95 text-white rounded-lg font-medium text-sm transition-all"
                        on:click=move |_| set_count.update(|n| *n += 1)
                    >
                        "+ Increment"
                    </button>
                </div>
            </div>
        </main>
    }
}
