import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Next.js 15 + Supabase + shadcn/ui',
  description: 'Production App Router kit with Server Actions and Supabase RLS',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100">
      <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              tailwind.config = {
                darkMode: 'class',
                theme: {
                  extend: {
                    colors: {
                      brand: { 500: '#3b82f6', 600: '#2563eb' }
                    }
                  }
                }
              }
            `,
          }}
        />
      </head>
      <body className="min-h-full flex flex-col font-sans antialiased">
        <header class="border-b border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur sticky top-0 z-40">
          <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold text-sm shadow">
                Nx
              </div>
              <div>
                <span class="font-bold text-lg tracking-tight">Next.js 15 + Supabase</span>
                <span class="ml-2 px-2 py-0.5 text-xs rounded-full bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 font-medium">Ready to Ship</span>
              </div>
            </div>
            <div class="flex items-center space-x-4">
              <a href="/api/healthz" class="text-sm font-medium text-slate-600 dark:text-slate-300 hover:text-blue-600">Health API</a>
            </div>
          </div>
        </header>

        <main class="flex-grow max-w-6xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>

        <footer class="border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 py-6 text-center text-sm text-slate-500">
          <p>Built with Next.js 15 App Router, React 19, and Supabase RLS. TechTalks Stack Kits.</p>
        </footer>
      </body>
    </html>
  );
}
