defmodule DemoWeb.Layouts do
  use Phoenix.Component

  def root(assigns) do
    ~H"""
    <!DOCTYPE html>
    <html lang="en" class="h-full bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="csrf-token" content={Phoenix.Controller.get_csrf_token()} />
        <title>Elixir Phoenix LiveView Real-time Stack</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script>
          tailwind.config = {
            darkMode: 'class',
            theme: {
              extend: {
                colors: {
                  brand: { 500: '#8b5cf6', 600: '#7c3aed', 700: '#6d28d9' }
                }
              }
            }
          }
        </script>
      </head>
      <body class="min-h-full flex flex-col font-sans antialiased">
        <header class="border-b border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur sticky top-0 z-40">
          <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 rounded-lg bg-purple-600 flex items-center justify-center text-white font-bold text-sm shadow">
                Ex
              </div>
              <div>
                <span class="font-bold text-lg tracking-tight">Elixir Phoenix 1.7+ LiveView</span>
                <span class="ml-2 px-2 py-0.5 text-xs rounded-full bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 font-medium">Ready to Ship</span>
              </div>
            </div>
            <div class="flex items-center space-x-4">
              <a href="/api/healthz" class="text-sm font-medium text-slate-600 dark:text-slate-300 hover:text-purple-600">Health API</a>
              <button onclick="document.documentElement.classList.toggle('dark')" class="p-2 rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-sm">
                🌓
              </button>
            </div>
          </div>
        </header>
        <main class="flex-grow max-w-6xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {@inner_content}
        </main>
        <footer class="border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 py-6 text-center text-sm text-slate-500">
          <p>Built with Elixir 1.17, Phoenix LiveView 1.0, and Ecto. TechTalks Stack Kits.</p>
        </footer>
      </body>
    </html>
    """
  end
end
