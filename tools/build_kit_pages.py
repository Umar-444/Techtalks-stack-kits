"""
tools/build_kit_pages.py
Static kit showcase page generator for TechTalks Stack Kits.
Reads kit.yaml and README.md from each kit folder in kits/ and produces:
  kits/<kit-slug>/index.html
Updates sitemap.xml with kit URLs.
"""

import os
import sys
import yaml
import re

def render_kit_page(kit_meta, kit_dir, readme_html=""):
    slug = kit_meta.get("slug", os.path.basename(kit_dir))
    name = kit_meta.get("name", slug)
    version = kit_meta.get("version", "1.0.0")
    desc = kit_meta.get("description", "")
    author = kit_meta.get("author", "TechTalks Stack Kits")
    stack = kit_meta.get("stack", {})
    layers = kit_meta.get("layers", {})
    security = kit_meta.get("security", {})
    prompts = kit_meta.get("agent_prompts", {})

    # Badges for stack
    stack_pills = []
    if "language" in stack:
        stack_pills.append(f"<span class='px-2.5 py-1 rounded text-xs font-mono bg-[#F4F4F0] dark:bg-[#202420] text-[#12140F] dark:text-[#F2F2EC] border border-[#E6E6DF] dark:border-[#2A2E2A]'>{stack['language']}</span>")
    if "framework" in stack:
        stack_pills.append(f"<span class='px-2.5 py-1 rounded text-xs font-mono bg-[#F4F4F0] dark:bg-[#202420] text-[#12140F] dark:text-[#F2F2EC] border border-[#E6E6DF] dark:border-[#2A2E2A]'>{stack['framework']}</span>")
    if "database" in stack:
        stack_pills.append(f"<span class='px-2.5 py-1 rounded text-xs font-mono bg-[#F4F4F0] dark:bg-[#202420] text-[#12140F] dark:text-[#F2F2EC] border border-[#E6E6DF] dark:border-[#2A2E2A]'>{stack['database']}</span>")
    if "admin_panel" in stack:
        stack_pills.append(f"<span class='px-2.5 py-1 rounded text-xs font-mono bg-[#FFF1E8] dark:bg-[#2A1E16] text-[#B33D14] dark:text-[#FF8D5C] border border-[#E85D26]/20 font-semibold'>{stack['admin_panel']}</span>")
    for extra in stack.get("extra", []):
        stack_pills.append(f"<span class='px-2.5 py-1 rounded text-xs font-mono bg-[#F4F4F0] dark:bg-[#202420] text-[#5C6058] dark:text-[#A8ACA0] border border-[#E6E6DF] dark:border-[#2A2E2A]'>{extra}</span>")

    stack_badges_html = " ".join(stack_pills)

    # Security checks list
    sec_items = []
    if security.get("gitleaks", False):
        sec_items.append("<li><span class='text-emerald-600 dark:text-emerald-400 font-bold'>&check;</span> Gitleaks Secret Scanning Pre-configured</li>")
    if security.get("semgrep", False):
        sec_items.append("<li><span class='text-emerald-600 dark:text-emerald-400 font-bold'>&check;</span> Semgrep Static Analysis Ruleset Active</li>")
    if security.get("auth_enforced", False):
        sec_items.append("<li><span class='text-emerald-600 dark:text-emerald-400 font-bold'>&check;</span> Mandatory Authorization & RBAC on All Resources</li>")
    if security.get("input_validation_enforced", False):
        sec_items.append("<li><span class='text-emerald-600 dark:text-emerald-400 font-bold'>&check;</span> Form Request & Parameterized SQL Enforcement</li>")
    if security.get("sandboxed_tools", False):
        sec_items.append("<li><span class='text-emerald-600 dark:text-emerald-400 font-bold'>&check;</span> Isolated Agent Tool Execution Sandboxing</li>")

    sec_html = "\n".join(sec_items) if sec_items else "<li>Standard Security Scan Protocol Enabled</li>"

    # Kickoff prompt
    kickoff_prompt = prompts.get("kickoff", f"You are building with the {name} kit. Follow rules in AGENTS.md, DESIGN.md tokens, and steps/agent-build-steps.md.")

    html = f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} — AI Stack Kit Guide | TechTalks</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="https://techtalks.itsumarfarooq.com/kits/{slug}/">

  <!-- Open Graph -->
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://techtalks.itsumarfarooq.com/kits/{slug}/">
  <meta property="og:title" content="{name} — TechTalks AI Stack Kit">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="https://techtalks.itsumarfarooq.com/assets/img/social-preview.png">

  <!-- Fonts & Styles -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/styles.css">

  <script>
    if (localStorage.getItem('theme') === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {{
      document.documentElement.classList.add('dark');
    }} else {{
      document.documentElement.classList.remove('dark');
    }}
  </script>
</head>
<body class="bg-[#FFFFFF] dark:bg-[#0F1110] text-[#12140F] dark:text-[#F2F2EC] font-sans antialiased min-h-screen flex flex-col selection:bg-[#E85D26]/20 selection:text-[#E85D26]">

  <!-- Header Navigation -->
  <header class="sticky top-0 z-40 bg-white/95 dark:bg-[#0F1110]/95 backdrop-blur-md border-b border-[#E6E6DF] dark:border-[#2A2E2A]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <a href="/" class="flex items-center gap-2.5 font-bold text-lg tracking-tight">
          <span class="w-8 h-8 rounded-sm bg-[#E85D26] flex items-center justify-center text-white text-sm font-bold shadow-sm">TS</span>
          <span>TechTalks <span class="text-[#E85D26]">Stack Kits</span></span>
        </a>
      </div>

      <nav class="hidden md:flex items-center gap-1 text-[15px] font-medium">
        <a href="/" class="button-ghost">Home</a>
        <a href="/kits/" class="button-ghost text-[#E85D26] font-semibold">All Kits</a>
        <a href="/security/" class="button-ghost">Security Hub</a>
        <a href="/security/laravel/" class="button-ghost">Laravel Track</a>
        <a href="https://github.com/Umar-444/Techtalks-stack-kits" target="_blank" rel="noopener noreferrer" class="button-ghost text-xs uppercase tracking-wider text-[#5C6058] dark:text-[#A8ACA0]">GitHub &nearr;</a>
      </nav>

      <div class="flex items-center gap-2.5">
        <button type="button" data-theme-toggle class="p-2 rounded-sm text-[#5C6058] hover:text-[#12140F] dark:text-[#A8ACA0] dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/10 transition-colors" aria-label="Toggle dark mode">
          <svg class="w-5 h-5 hidden dark:block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
          <svg class="w-5 h-5 block dark:hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/></svg>
        </button>

        <a href="/kits/" class="btn-brand-subtle text-xs font-semibold h-[34px] px-3">
          &larr; Back to Catalog
        </a>
      </div>
    </div>
  </header>

  <!-- Breadcrumbs & Kit Hero -->
  <section class="border-b border-[#E6E6DF] dark:border-[#2A2E2A] bg-[#FFF1E8]/20 dark:bg-[#2A1E16]/20 py-10 sm:py-14">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <!-- Breadcrumbs -->
      <nav class="flex items-center gap-2 text-xs text-[#5C6058] dark:text-[#A8ACA0] mb-4">
        <a href="/" class="hover:text-[#E85D26]">Home</a>
        <span>&rsaquo;</span>
        <a href="/kits/" class="hover:text-[#E85D26]">Stack Kits</a>
        <span>&rsaquo;</span>
        <span class="text-[#12140F] dark:text-white font-medium">{name}</span>
      </nav>

      <div class="flex flex-wrap items-center gap-2 mb-3">
        <span class="chip-orange">Kit Manifest v{version}</span>
        <span class="chip-teal">Validated Spec</span>
      </div>

      <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-[#12140F] dark:text-white mb-3">
        {name}
      </h1>

      <p class="text-base sm:text-lg text-[#5C6058] dark:text-[#A8ACA0] leading-relaxed max-w-3xl mb-6">
        {desc}
      </p>

      <!-- Stack Badges -->
      <div class="flex flex-wrap items-center gap-2 mb-8">
        {stack_badges_html}
      </div>

      <!-- Quick Action Buttons -->
      <div class="flex flex-wrap items-center gap-3">
        <button type="button" data-copy-cmd="git clone https://github.com/Umar-444/Techtalks-stack-kits.git" class="btn-brand-orange h-[38px] px-4 text-xs sm:text-sm font-semibold gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
          <span>Copy Git Clone</span>
        </button>

        <button type="button" data-copy-prompt="{kickoff_prompt}" class="btn-brand-subtle h-[38px] px-4 text-xs sm:text-sm font-semibold gap-2 text-[#E85D26]">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
          <span>Copy Agent Kickoff Prompt</span>
        </button>

        <a href="https://github.com/Umar-444/Techtalks-stack-kits/tree/main/kits/{slug}" target="_blank" rel="noopener noreferrer" class="btn-brand-subtle h-[38px] px-3.5 text-xs font-mono text-[#5C6058] dark:text-[#A8ACA0]">
          View on GitHub &nearr;
        </a>
      </div>
    </div>
  </section>

  <!-- Kit Detail Body -->
  <main class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12 flex-1 w-full space-y-12">
    
    <!-- 1. Agent Dialects & Rules -->
    <div class="bg-white dark:bg-[#171A18] rounded-md border border-[#E6E6DF] dark:border-[#2A2E2A] p-6 shadow-sm">
      <div class="flex items-center justify-between mb-4">
        <div>
          <span class="chip-teal mb-1">Single-Source Rules</span>
          <h2 class="text-xl font-bold text-[#12140F] dark:text-white">Transpiled Agent Rules</h2>
        </div>
        <span class="text-xs font-mono text-[#5C6058] dark:text-[#A8ACA0]">6 Agent Formats</span>
      </div>

      <p class="text-sm text-[#5C6058] dark:text-[#A8ACA0] mb-4">
        Rules are written once in <code>rules/source/*.md</code> and transpiled automatically into all IDE agent standards. Zero rule divergence.
      </p>

      <div class="grid grid-cols-2 sm:grid-cols-3 gap-3 font-mono text-xs">
        <div class="p-3 rounded bg-[#F4F4F0] dark:bg-[#0F1110] border border-[#E6E6DF] dark:border-[#2A2E2A]">
          <div class="font-bold text-[#12140F] dark:text-white">Cursor</div>
          <div class="text-[11px] text-[#5C6058] dark:text-[#A8ACA0] mt-0.5">.cursor/rules/*.mdc</div>
        </div>
        <div class="p-3 rounded bg-[#F4F4F0] dark:bg-[#0F1110] border border-[#E6E6DF] dark:border-[#2A2E2A]">
          <div class="font-bold text-[#12140F] dark:text-white">Claude Code</div>
          <div class="text-[11px] text-[#5C6058] dark:text-[#A8ACA0] mt-0.5">CLAUDE.md</div>
        </div>
        <div class="p-3 rounded bg-[#F4F4F0] dark:bg-[#0F1110] border border-[#E6E6DF] dark:border-[#2A2E2A]">
          <div class="font-bold text-[#12140F] dark:text-white">Codex / Universal</div>
          <div class="text-[11px] text-[#5C6058] dark:text-[#A8ACA0] mt-0.5">AGENTS.md</div>
        </div>
        <div class="p-3 rounded bg-[#F4F4F0] dark:bg-[#0F1110] border border-[#E6E6DF] dark:border-[#2A2E2A]">
          <div class="font-bold text-[#12140F] dark:text-white">Copilot</div>
          <div class="text-[11px] text-[#5C6058] dark:text-[#A8ACA0] mt-0.5">copilot-instructions.md</div>
        </div>
        <div class="p-3 rounded bg-[#F4F4F0] dark:bg-[#0F1110] border border-[#E6E6DF] dark:border-[#2A2E2A]">
          <div class="font-bold text-[#12140F] dark:text-white">Google Antigravity</div>
          <div class="text-[11px] text-[#5C6058] dark:text-[#A8ACA0] mt-0.5">.agents/rules/*.md</div>
        </div>
        <div class="p-3 rounded bg-[#F4F4F0] dark:bg-[#0F1110] border border-[#E6E6DF] dark:border-[#2A2E2A]">
          <div class="font-bold text-[#12140F] dark:text-white">Windsurf</div>
          <div class="text-[11px] text-[#5C6058] dark:text-[#A8ACA0] mt-0.5">.windsurfrules</div>
        </div>
      </div>
    </div>

    <!-- 2. Security Protocol -->
    <div class="bg-white dark:bg-[#171A18] rounded-md border border-[#E6E6DF] dark:border-[#2A2E2A] p-6 shadow-sm">
      <span class="chip-teal mb-2">Non-Negotiable</span>
      <h2 class="text-xl font-bold text-[#12140F] dark:text-white mb-3">Pre-Configured Security Layer</h2>
      <p class="text-sm text-[#5C6058] dark:text-[#A8ACA0] mb-4">
        Security checks are never optional. Every build step validates against secrets leakage, injection vulnerabilities, and broken access controls.
      </p>

      <ul class="space-y-2.5 text-sm text-[#12140F] dark:text-[#F2F2EC]">
        {sec_html}
      </ul>
    </div>

    <!-- 3. Kickoff Prompt Box -->
    <div class="bg-white dark:bg-[#171A18] rounded-md border border-[#E6E6DF] dark:border-[#2A2E2A] p-6 shadow-sm">
      <div class="flex items-center justify-between mb-3">
        <h2 class="text-xl font-bold text-[#12140F] dark:text-white">Agent Kickoff Prompt</h2>
        <button type="button" data-copy-prompt="{kickoff_prompt}" class="btn-brand-subtle text-xs h-[30px] px-3 font-mono text-[#E85D26]">
          Copy Prompt
        </button>
      </div>
      <p class="text-xs text-[#5C6058] dark:text-[#A8ACA0] mb-3">
        Paste this prompt directly into your agent at the start of your building session:
      </p>
      <div class="p-4 rounded bg-[#141414] text-[#EDEDED] font-mono text-xs leading-relaxed overflow-x-auto">
        <code>{kickoff_prompt}</code>
      </div>
    </div>

    <!-- Readme Content / Notes -->
    {readme_html}

  </main>

  <!-- Footer -->
  <footer class="mt-auto border-t border-[#E6E6DF] dark:border-[#2A2E2A] bg-white dark:bg-[#0F1110] py-10 text-sm text-[#5C6058] dark:text-[#A8ACA0]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
      <p>&copy; 2026 TechTalks Stack Kits &bull; Umar Farooq. All rights reserved.</p>
      <a href="/kits/" class="text-xs hover:text-[#E85D26]">&larr; Back to all stack kits</a>
    </div>
  </footer>

  <script src="/assets/js/main.js"></script>
  <script src="/assets/js/kits-filter.js"></script>
</body>
</html>
"""
    return html

def build_all():
    kits_base = "kits"
    if not os.path.isdir(kits_base):
        print(f"Directory {kits_base} not found.")
        return

    # Check templates/kit.yaml for default specs
    template_yaml_path = "templates/kit.yaml"
    template_meta = {}
    if os.path.exists(template_yaml_path):
        with open(template_yaml_path, "r", encoding="utf-8") as tf:
            template_meta = yaml.safe_load(tf) or {}

    generated_count = 0
    generated_urls = ["/kits/"]

    # Matrix of 10 kits with default metadata if kit.yaml doesn't exist yet
    ten_kits = [
        {
            "slug": "laravel-filament-postgresql",
            "name": "Laravel + Filament + PostgreSQL",
            "version": "1.0.0",
            "description": "Production SaaS & Admin Stack. Multi-stage Docker, Filament 4/3 SPA mode, Spatie RBAC, MFA, Horizon queues, and pre-wired Pest Arch security tests.",
            "stack": {
                "language": "PHP 8.4",
                "framework": "Laravel 12/13",
                "admin_panel": "Filament 4/3",
                "database": "PostgreSQL 16+",
                "extra": ["Docker Compose", "Horizon", "Redis", "Spatie Permission"]
            },
            "security": {
                "gitleaks": True,
                "semgrep": True,
                "auth_enforced": True,
                "input_validation_enforced": True
            },
            "agent_prompts": {
                "kickoff": "You are building with the TechTalks Laravel-Filament-PostgreSQL kit. Follow rules in AGENTS.md, DESIGN.md tokens, and steps/agent-build-steps.md. Report in: Done, Files, Verified, Not verified."
            }
        },
        {
            "slug": "laravel-livewire-postgresql",
            "name": "Laravel + Livewire + PostgreSQL",
            "version": "1.0.0-blueprint",
            "description": "Reactive TALL Stack with Flux UI, Volt single-file components, Folio page routing, Fortify authentication, and PostgreSQL.",
            "stack": {
                "language": "PHP 8.4",
                "framework": "Laravel 12",
                "admin_panel": "Livewire 4 + Flux UI",
                "database": "PostgreSQL 16+",
                "extra": ["Volt", "Folio", "Fortify"]
            },
            "security": {"gitleaks": True, "semgrep": True, "auth_enforced": True}
        },
        {
            "slug": "laravel-mongodb",
            "name": "Laravel + MongoDB (NoSQL)",
            "version": "1.0.0-blueprint",
            "description": "Empty-market pioneer stack. Official mongodb/laravel-mongodb package, embedded documents, aggregation pipelines, and custom React/Inertia dashboard.",
            "stack": {
                "language": "PHP 8.4",
                "framework": "Laravel 12",
                "database": "MongoDB 7+",
                "admin_panel": "Inertia + React",
                "extra": ["mongodb/laravel-mongodb"]
            },
            "security": {"gitleaks": True, "semgrep": True, "auth_enforced": True}
        },
        {
            "slug": "laravel-mysql",
            "name": "Laravel + MySQL Enterprise Starter",
            "version": "1.0.0-blueprint",
            "description": "Battle-tested enterprise foundation. Larastan Level 8, Pint formatting, Pest Architecture tests, and high-concurrency MySQL 8 indexing.",
            "stack": {
                "language": "PHP 8.4",
                "framework": "Laravel 12",
                "database": "MySQL 8",
                "extra": ["Larastan L8", "Pint", "Pest Arch"]
            },
            "security": {"gitleaks": True, "semgrep": True, "auth_enforced": True}
        },
        {
            "slug": "nextjs-approuter-supabase",
            "name": "Next.js 15+ + Supabase + shadcn/ui",
            "version": "1.0.0-blueprint",
            "description": "React Server Components, Server Actions with Zod validation, Row-Level Security in Supabase/PostgreSQL, and shadcn/ui tokens.",
            "stack": {
                "language": "TypeScript 5+",
                "framework": "Next.js 15 (Turbopack)",
                "database": "Supabase / PostgreSQL",
                "extra": ["shadcn/ui", "Zod", "Server Actions"]
            },
            "security": {"gitleaks": True, "semgrep": True, "auth_enforced": True}
        },
        {
            "slug": "django-tailwind-postgresql",
            "name": "Django 5+ + Tailwind + PostgreSQL",
            "version": "1.0.0-blueprint",
            "description": "Python enterprise backend with batteries-included admin, Celery background queues, django-tailwind, and custom user model auth.",
            "stack": {
                "language": "Python 3.12+",
                "framework": "Django 5",
                "database": "PostgreSQL",
                "extra": ["Celery", "Redis", "django-tailwind"]
            },
            "security": {"gitleaks": True, "semgrep": True, "auth_enforced": True}
        },
        {
            "slug": "flask-htmx-sqlite",
            "name": "Flask + HTMX + Alpine.js",
            "version": "1.0.0-blueprint",
            "description": "Lightweight hypermedia stack. Zero complex JS build tooling, partial HTML over the wire, and minimal memory overhead.",
            "stack": {
                "language": "Python 3.12+",
                "framework": "Flask 3",
                "database": "SQLite / PostgreSQL",
                "extra": ["HTMX 2", "Alpine.js", "SQLAlchemy 2"]
            },
            "security": {"gitleaks": True, "semgrep": True, "auth_enforced": True}
        },
        {
            "slug": "rag-fastapi-qdrant",
            "name": "Production RAG Stack",
            "version": "1.0.0-blueprint",
            "description": "Production Retrieval-Augmented Generation. Ingest, chunk, embed, retrieve, generate with tenant isolation and eval benchmarks.",
            "stack": {
                "language": "Python 3.12+",
                "framework": "FastAPI",
                "database": "Qdrant / Chroma",
                "extra": ["LangChain", "LlamaIndex", "Ollama", "OpenAI"]
            },
            "security": {"gitleaks": True, "semgrep": True, "auth_enforced": True}
        },
        {
            "slug": "agentic-langgraph-crewai",
            "name": "Autonomous Multi-Agent System",
            "version": "1.0.0-blueprint",
            "description": "State-machine agent graph with LangGraph and CrewAI. Safe tool execution, Docker sandboxing, human-in-the-loop approvals, and cost fences.",
            "stack": {
                "language": "Python 3.12+",
                "framework": "LangGraph + CrewAI",
                "extra": ["Pydantic v2", "Docker Sandboxing"]
            },
            "security": {"gitleaks": True, "semgrep": True, "sandboxed_tools": True}
        },
        {
            "slug": "reverse-engineering-security",
            "name": "Reverse Engineering & Security Agent Stack",
            "version": "1.0.0-blueprint",
            "description": "Binary, firmware, and AST code analysis tools structured for AI agents. GhidraMCP, Radare2, Semgrep rule authoring, and memory safety checks.",
            "stack": {
                "language": "Python 3.12+",
                "framework": "GhidraMCP + Radare2",
                "extra": ["Semgrep AST", "Binary Ninja API"]
            },
            "security": {"gitleaks": True, "semgrep": True, "sandboxed_tools": True}
        }
    ]

    for kit in ten_kits:
        slug = kit["slug"]
        kit_dir = os.path.join(kits_base, slug)
        os.makedirs(kit_dir, exist_ok=True)

        manifest_path = os.path.join(kit_dir, "kit.yaml")
        meta = kit
        if os.path.exists(manifest_path):
            try:
                with open(manifest_path, "r", encoding="utf-8") as mf:
                    file_meta = yaml.safe_load(mf)
                    if file_meta and isinstance(file_meta, dict):
                        meta.update(file_meta)
            except Exception as e:
                print(f"Warning reading {manifest_path}: {e}")

        # Render HTML
        page_html = render_kit_page(meta, kit_dir)
        dest_html_path = os.path.join(kit_dir, "index.html")
        with open(dest_html_path, "w", encoding="utf-8") as out:
            out.write(page_html)

        generated_urls.append(f"/kits/{slug}/")
        generated_count += 1
        print(f"Rendered: {dest_html_path}")

    # Update sitemap.xml
    update_sitemap(generated_urls)
    print(f"Successfully generated {generated_count} kit pages and updated sitemap.")

def update_sitemap(new_urls):
    sitemap_path = "sitemap.xml"
    if not os.path.exists(sitemap_path):
        return

    with open(sitemap_path, "r", encoding="utf-8") as f:
        content = f.read()

    base_domain = "https://techtalks.itsumarfarooq.com"
    entries_to_add = []
    for u in new_urls:
        full_url = base_domain + u
        if full_url not in content:
            entry = f"""  <url>
    <loc>{full_url}</loc>
    <lastmod>2026-10-21</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>"""
            entries_to_add.append(entry)

    if entries_to_add:
        replacement = "\n".join(entries_to_add) + "\n</urlset>"
        content = content.replace("</urlset>", replacement)
        with open(sitemap_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Added {len(entries_to_add)} URLs to sitemap.xml")

if __name__ == "__main__":
    build_all()
