use leptos::*;

#[component]
pub fn App() -> impl IntoView {
    let (count, set_count) = create_signal(0);
    view! {
        <main class="min-h-screen bg-[#FDFDFC] dark:bg-[#0C0D0A] p-8 text-[#12140F] dark:text-[#F2F2EC]">
            <h1 class="text-2xl font-bold font-sans">"Leptos Full-Stack Rust"</h1>
            <button
                class="mt-4 px-4 py-2 bg-[#E85D26] text-white rounded font-medium"
                on:click=move |_| set_count.update(|n| *n += 1)>
                "Count: " {count}
            </button>
        </main>
    }
}
