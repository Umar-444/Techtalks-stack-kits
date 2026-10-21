"""
tools/build_kit_pages.py
Static kit showcase page generator for TechTalks Stack Kits.
Reads kit.yaml and README.md from each kit folder in kits/ and produces:
  kits/<kit-slug>/index.html
Updates sitemap.xml with kit URLs.
"""

import os
import sys
import json
import re

try:
    import yaml
except ImportError:
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml"])
        import yaml
    except Exception as e:
        print(f"Warning: pyyaml could not be imported or installed: {e}")
        yaml = None

def render_kit_page(kit_meta, kit_dir, readme_html=""):
    slug = kit_meta.get("slug", os.path.basename(kit_dir))
    name = kit_meta.get("name", slug)
    status = kit_meta.get("status", "blueprint").lower()
    is_blueprint = status in ["planned", "blueprint", "draft"]
    
    display_name = name
    if is_blueprint and not name.endswith("(Blueprint)"):
        display_name = f"{name} (Blueprint)"
        
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
    prefix = "Planned: " if is_blueprint else ""
    if security.get("gitleaks", False):
        sec_items.append(f"<li><span class='text-emerald-600 dark:text-emerald-400 font-bold'>&check;</span> {prefix}Gitleaks Secret Scanning Pre-configured</li>")
    if security.get("semgrep", False):
        sec_items.append(f"<li><span class='text-emerald-600 dark:text-emerald-400 font-bold'>&check;</span> {prefix}Semgrep Static Analysis Ruleset Active</li>")
    if security.get("auth_enforced", False):
        sec_items.append(f"<li><span class='text-emerald-600 dark:text-emerald-400 font-bold'>&check;</span> {prefix}Mandatory Authorization &amp; RBAC on All Resources</li>")
    if security.get("input_validation_enforced", False):
        sec_items.append(f"<li><span class='text-emerald-600 dark:text-emerald-400 font-bold'>&check;</span> {prefix}Form Request &amp; Parameterized SQL Enforcement</li>")
    if security.get("sandboxed_tools", False):
        sec_items.append(f"<li><span class='text-emerald-600 dark:text-emerald-400 font-bold'>&check;</span> {prefix}Isolated Agent Tool Execution Sandboxing</li>")

    sec_html = "\n".join(sec_items) if sec_items else f"<li>{prefix}Standard Security Scan Protocol Enabled</li>"

    # Kickoff prompt
    kickoff_prompt = prompts.get("kickoff", f"You are building with the {name} kit. Follow rules in AGENTS.md, DESIGN.md tokens, and steps/agent-build-steps.md.")

    # Status banner for blueprints
    blueprint_banner = ""
    if is_blueprint:
        blueprint_banner = f"""
    <div class="mb-8 p-4 rounded-md bg-[#FEF6D8] dark:bg-[#2A2410] border border-[#B7791F]/30 text-[#8F5B0E] dark:text-[#E0A838] text-sm flex items-start gap-3">
      <span class="w-2.5 h-2.5 rounded-full bg-[#B7791F] shrink-0 mt-1.5"></span>
      <div>
        <strong class="font-bold">Architectural Blueprint:</strong> This kit is currently a planned architectural blueprint.
        The specifications, threat model, and rules below describe the planned implementation. Starter source containers and automated test suites are in active development.
      </div>
    </div>
"""

    status_chip = f"""<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-[#FEF6D8] text-[#8F5B0E] dark:bg-[#2A2410] dark:text-[#E0A838] border border-[#B7791F]/30">
      <span class="w-2 h-2 rounded-full bg-[#B7791F]"></span>
      Blueprint Specification
    </span>""" if is_blueprint else f"""<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300 border border-emerald-500/20">
      <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
      Verified Complete Kit
    </span>"""

    # Structured Data JSON-LD
    schema_json = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "SoftwareSourceCode",
                "@id": f"https://techtalks.itsumarfarooq.com/kits/{slug}/#software",
                "name": display_name,
                "description": desc,
                "version": version,
                "codeRepository": "https://github.com/Umar-444/Techtalks-stack-kits",
                "programmingLanguage": stack.get("language", "Full Stack"),
                "author": {
                    "@type": "Person",
                    "name": "Umar Farooq",
                    "url": "https://itsumarfarooq.com"
                }
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"https://techtalks.itsumarfarooq.com/kits/{slug}/#breadcrumb",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": "https://techtalks.itsumarfarooq.com/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Stack Kits",
                        "item": "https://techtalks.itsumarfarooq.com/kits/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": display_name,
                        "item": f"https://techtalks.itsumarfarooq.com/kits/{slug}/"
                    }
                ]
            },
            {
                "@type": "FAQPage",
                "@id": f"https://techtalks.itsumarfarooq.com/kits/{slug}/#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": f"How do I initialize the {name} kit?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"Clone the repository with `git clone https://github.com/Umar-444/Techtalks-stack-kits.git`, navigate to `kits/{slug}/`, and hand the bootstrap prompt to your AI coding agent."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": f"Which AI agents support {name}?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "The kit's rules are automatically transpiled into 6 native formats: Cursor (.cursor/rules/*.mdc), Claude Code (CLAUDE.md), GitHub Copilot (.github/copilot-instructions.md), Cline (.clinerules), OpenAI Codex (CODEX.md), and Antigravity (.agents/rules/*.md)."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": f"What security invariants are enforced in {name}?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "The kit enforces zero plaintext credentials via Gitleaks, parameterized queries, and resource-level authorization policies."
                        }
                    }
                ]
            }
        ]
    }
    schema_script = json.dumps(schema_json, indent=2)

    html = f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{display_name} &bull; TechTalks Stack Kits</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="https://techtalks.itsumarfarooq.com/kits/{slug}/">

  <!-- Open Graph -->
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://techtalks.itsumarfarooq.com/kits/{slug}/">
  <meta property="og:title" content="{display_name} &bull; TechTalks Stack Kits">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="https://techtalks.itsumarfarooq.com/assets/social-preview.png">

  <!-- Fonts & Styles -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/styles.css">

  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%23E85D26'/><text x='50' y='68' font-size='50' font-family='sans-serif' font-weight='bold' text-anchor='middle' fill='white'>TS</text></svg>">

  <!-- Structured Data JSON-LD -->
  <script type="application/ld+json">
{schema_script}
  </script>

  <script>
    if (localStorage.getItem('theme') === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {{
      document.documentElement.classList.add('dark');
    }} else {{
      document.documentElement.classList.remove('dark');
    }}
  </script>
</head>
<body class="bg-[#FBFBFA] dark:bg-[#121413] text-[#12140F] dark:text-[#E8EAE6] font-sans antialiased min-h-screen flex flex-col selection:bg-[#E85D26] selection:text-white">

  <!-- Header Navigation -->
  <header class="sticky top-0 z-40 bg-white/95 dark:bg-[#0F1110]/95 backdrop-blur-md border-b border-[#E6E6DF] dark:border-[#2A2E2A]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <a href="/" class="flex items-center gap-2.5 font-bold text-lg tracking-tight">
          <span class="w-8 h-8 rounded-sm bg-[#E85D26] flex items-center justify-center text-white text-sm font-bold shadow-sm">TS</span>
          <span class="text-[#12140F] dark:text-white">TechTalks</span>
        </a>
      </div>

      <nav class="hidden md:flex items-center gap-1 text-[15px] font-medium">
        <a href="/kits/" class="button-ghost text-[#E85D26] font-semibold">Kits</a>
        <a href="/security/" class="button-ghost">Security</a>
        <a href="/security/laravel/checklist.html" class="button-ghost">Checklist</a>
        <a href="https://github.com/Umar-444/Techtalks-stack-kits/discussions" target="_blank" rel="noopener noreferrer" class="button-ghost">Community &nearr;</a>
        <a href="https://github.com/Umar-444/Techtalks-stack-kits" target="_blank" rel="noopener noreferrer" class="button-ghost text-xs uppercase tracking-wider text-[#5C6058] dark:text-[#A8ACA0]">GitHub &nearr;</a>
      </nav>

      <div class="flex items-center gap-2.5">
        <button type="button" data-theme-toggle class="p-2 rounded-sm text-[#5C6058] hover:text-[#12140F] dark:text-[#A8ACA0] dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/10 transition-colors" aria-label="Toggle dark mode">
          <svg class="w-5 h-5 hidden dark:block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
          <svg class="w-5 h-5 block dark:hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/></svg>
        </button>

        <a href="/kits/" class="btn-brand-orange text-xs sm:text-sm font-semibold h-[34px] px-3.5">
          Get a Kit &rarr;
        </a>
      </div>
    </div>
  </header>

  <!-- Main Content -->
  <main class="flex-grow max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 w-full">
    
    <!-- Breadcrumbs -->
    <nav class="flex items-center gap-2 text-xs text-[#5C6058] dark:text-[#A8ACA0] mb-6">
      <a href="/" class="hover:text-[#E85D26]">Home</a>
      <span>/</span>
      <a href="/kits/" class="hover:text-[#E85D26]">Stack Kits</a>
      <span>/</span>
      <span class="text-[#12140F] dark:text-white font-medium">{slug}</span>
    </nav>

{blueprint_banner}

    <!-- Header Section -->
    <div class="border-b border-[#E6E6DF] dark:border-[#2A2E2A] pb-8 mb-8">
      <div class="flex flex-wrap items-center gap-3 mb-3">
        {status_chip}
        <span class="text-xs font-mono text-[#5C6058] dark:text-[#A8ACA0]">v{version}</span>
      </div>

      <h1 class="text-3xl sm:text-4xl font-extrabold text-[#12140F] dark:text-white tracking-tight mb-3">
        {display_name}
      </h1>

      <p class="text-base sm:text-lg text-[#5C6058] dark:text-[#A8ACA0] max-w-4xl leading-relaxed mb-6">
        {desc}
      </p>

      <div class="flex flex-wrap gap-2">
        {stack_badges_html}
      </div>
    </div>

    <!-- Quick Navigation Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
      <!-- Bootstrap Agent -->
      <div class="card-kit p-6 flex flex-col justify-between">
        <div>
          <div class="text-xs uppercase tracking-wider font-bold text-[#E85D26] mb-2 font-mono">Agent Bootstrapping</div>
          <h2 class="text-lg font-bold text-[#12140F] dark:text-white mb-2">Pre-Wired Rules</h2>
          <p class="text-xs text-[#5C6058] dark:text-[#A8ACA0] leading-relaxed mb-4">
            Single-source rules compiled to 6 native agent dialects. Transpiled deterministically from <code class="font-mono text-xs">rules/source/</code>.
          </p>
        </div>
        <div class="space-y-1 text-xs font-mono text-[#5C6058] dark:text-[#A8ACA0]">
          <div>&bull; .cursor/rules/*.mdc</div>
          <div>&bull; CLAUDE.md</div>
          <div>&bull; .agents/rules/*.md</div>
          <div>&bull; .clinerules &amp; CODEX.md</div>
        </div>
      </div>

      <!-- Security Guardrails -->
      <div class="card-kit p-6 flex flex-col justify-between">
        <div>
          <div class="text-xs uppercase tracking-wider font-bold text-emerald-600 dark:text-emerald-400 mb-2 font-mono">Security Guardrails</div>
          <h2 class="text-lg font-bold text-[#12140F] dark:text-white mb-2">Automated Scanners</h2>
          <p class="text-xs text-[#5C6058] dark:text-[#A8ACA0] leading-relaxed mb-4">
            Invariants asserted in CI before merge. Scanned by Gitleaks and Semgrep AST checkers.
          </p>
        </div>
        <ul class="space-y-1.5 text-xs text-[#5C6058] dark:text-[#A8ACA0]">
          {sec_html}
        </ul>
      </div>

      <!-- Turnkey Starter -->
      <div class="card-kit p-6 flex flex-col justify-between">
        <div>
          <div class="text-xs uppercase tracking-wider font-bold text-[#0E7C6B] dark:text-[#1DB89E] mb-2 font-mono">Docker Scaffolding</div>
          <h2 class="text-lg font-bold text-[#12140F] dark:text-white mb-2">Turnkey Containers</h2>
          <p class="text-xs text-[#5C6058] dark:text-[#A8ACA0] leading-relaxed mb-4">
            Runnable containers with pre-wired environment variables, healthchecks, and dependency locks.
          </p>
        </div>
        <div class="p-2.5 rounded bg-[#F4F4F0] dark:bg-[#1E221E] font-mono text-[11px] text-[#5C6058] dark:text-[#A8ACA0]">
          docker compose up -d
        </div>
      </div>
    </div>

    <!-- Agent Bootstrap Prompt -->
    <div class="my-10 p-6 rounded-md bg-[#F4F4F0] dark:bg-[#171A18] border border-[#E6E6DF] dark:border-[#2A2E2A]">
      <div class="flex items-center justify-between mb-3">
        <h3 class="text-sm font-bold uppercase tracking-wider text-[#12140F] dark:text-white font-mono">
          Agent Bootstrap Prompt
        </h3>
        <button type="button" data-copy-cmd="{kickoff_prompt}" class="text-xs text-[#E85D26] hover:underline flex items-center gap-1 font-semibold">
          <span>Copy Prompt</span>
        </button>
      </div>
      <p class="text-xs text-[#5C6058] dark:text-[#A8ACA0] mb-3">Feed this exact prompt into Claude Code, Cursor, Copilot, or Antigravity to anchor the agent:</p>
      <pre class="p-3.5 rounded bg-white dark:bg-[#0F1110] border border-[#E6E6DF] dark:border-[#2A2E2A] text-xs font-mono text-[#12140F] dark:text-[#E8EAE6] overflow-x-auto whitespace-pre-wrap">{kickoff_prompt}</pre>
    </div>

  </main>

  <!-- Standard 4-Column Footer -->
  <footer class="mt-auto border-t border-[#E6E6DF] dark:border-[#2A2E2A] bg-white dark:bg-[#0F1110] py-12 text-sm text-[#5C6058] dark:text-[#A8ACA0]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8 pb-10 border-b border-[#E6E6DF] dark:border-[#2A2E2A]">
        
        <!-- Col 1: Brand -->
        <div class="space-y-3">
          <div class="flex items-center gap-2.5 font-bold text-base text-[#12140F] dark:text-white">
            <span class="w-7 h-7 rounded-sm bg-[#E85D26] flex items-center justify-center text-white text-xs font-bold">TS</span>
            <span>TechTalks</span>
          </div>
          <p class="text-xs text-[#5C6058] dark:text-[#A8ACA0] leading-relaxed">
            Production blueprints with pre-wired AI agent rules and defensive security masterclasses.
          </p>
          <div class="pt-2 text-xs">
            <span class="text-[#8C9088]">Built by </span>
            <a href="https://itsumarfarooq.com" target="_blank" rel="noopener noreferrer" class="font-semibold text-[#12140F] dark:text-white hover:text-[#E85D26] transition-colors">Umar Farooq &nearr;</a>
          </div>
        </div>

        <!-- Col 2: Kits -->
        <div>
          <h4 class="text-xs uppercase tracking-wider font-bold text-[#12140F] dark:text-white mb-3">Stack Kits</h4>
          <ul class="space-y-2 text-xs">
            <li><a href="/kits/laravel-filament-postgresql/" class="hover:text-[#E85D26] transition-colors">Laravel + Filament (Kit #1)</a></li>
            <li><a href="/kits/laravel-livewire-postgresql/" class="hover:text-[#E85D26] transition-colors">Laravel + Livewire (Kit #2)</a></li>
            <li><a href="/kits/laravel-mongodb/" class="hover:text-[#E85D26] transition-colors">Laravel + MongoDB (Kit #3)</a></li>
            <li><a href="/kits/nextjs-approuter-supabase/" class="hover:text-[#E85D26] transition-colors">Next.js + Supabase (Kit #5)</a></li>
            <li class="pt-1"><a href="/kits/" class="font-semibold text-[#E85D26] hover:underline">All Kits &amp; Blueprints &rarr;</a></li>
          </ul>
        </div>

        <!-- Col 3: Security & Trust -->
        <div>
          <h4 class="text-xs uppercase tracking-wider font-bold text-[#12140F] dark:text-white mb-3">Security &amp; Trust</h4>
          <ul class="space-y-2 text-xs">
            <li><a href="/security/" class="hover:text-[#E85D26] transition-colors">Security Masterclass Hub</a></li>
            <li><a href="/security/laravel/" class="hover:text-[#E85D26] transition-colors">Laravel &amp; AI Track (22 Lessons)</a></li>
            <li><a href="/security/laravel/checklist.html" class="hover:text-[#E85D26] transition-colors">28-Point Security Checklist</a></li>
            <li><a href="/llms.txt" class="hover:text-[#E85D26] transition-colors font-mono">llms.txt</a></li>
            <li><a href="https://github.com/Umar-444/Techtalks-stack-kits/blob/main/SECURITY.md" target="_blank" rel="noopener noreferrer" class="hover:text-[#E85D26] transition-colors">Security Policy (SECURITY.md)</a></li>
          </ul>
        </div>

        <!-- Col 4: Community -->
        <div>
          <h4 class="text-xs uppercase tracking-wider font-bold text-[#12140F] dark:text-white mb-3">Community</h4>
          <ul class="space-y-2 text-xs">
            <li><a href="https://github.com/Umar-444/Techtalks-stack-kits" target="_blank" rel="noopener noreferrer" class="hover:text-[#E85D26] transition-colors">GitHub Repository &nearr;</a></li>
            <li><a href="https://github.com/Umar-444/Techtalks-stack-kits/blob/main/CONTRIBUTING.md" target="_blank" rel="noopener noreferrer" class="hover:text-[#E85D26] transition-colors">Contributing Guide &nearr;</a></li>
            <li><a href="https://github.com/Umar-444/Techtalks-stack-kits/discussions" target="_blank" rel="noopener noreferrer" class="hover:text-[#E85D26] transition-colors">GitHub Discussions &nearr;</a></li>
            <li><a href="https://github.com/Umar-444/Techtalks-stack-kits/issues/new?template=new-topic.yml" target="_blank" rel="noopener noreferrer" class="hover:text-[#E85D26] transition-colors">Propose a Kit &nearr;</a></li>
          </ul>
        </div>
      </div>

      <!-- Bottom Bar -->
      <div class="flex flex-col sm:flex-row items-center justify-between gap-4 pt-6 text-[11px] text-[#5C6058] dark:text-[#A8ACA0]">
        <div>
          &copy; 2026 Umar Farooq &bull; Released under the <a href="https://github.com/Umar-444/Techtalks-stack-kits/blob/main/LICENSE" target="_blank" rel="noopener noreferrer" class="underline hover:text-[#E85D26]">MIT License</a>.
        </div>
        <div>
          Not affiliated with Laravel, Filament, or Anthropic.
        </div>
      </div>
    </div>
  </footer>

  <script src="/assets/js/main.js"></script>
</body>
</html>
"""
    return html

def build_all():
    kits_base = "kits"
    if not os.path.isdir(kits_base):
        print(f"Directory {kits_base} not found.")
        return

    ten_kits = [
        {
            "slug": "laravel-filament-postgresql",
            "name": "Laravel 13 + Filament 4 + PostgreSQL",
            "version": "1.0.0",
            "status": "stable",
            "description": "Production admin panel and REST API stack with strict UUID v7 schemas, BOLA authorization policies, zero plaintext credentials, and single-source agent rules.",
            "stack": {
                "language": "PHP 8.4",
                "framework": "Laravel 13",
                "admin_panel": "Filament 4",
                "database": "PostgreSQL 16+",
                "extra": ["Docker Compose", "Pest PHP", "Semgrep", "Gitleaks"]
            },
            "security": {"gitleaks": True, "semgrep": True, "auth_enforced": True, "input_validation_enforced": True}
        },
        {
            "slug": "laravel-livewire-postgresql",
            "name": "Laravel 12 + Livewire 4 + PostgreSQL",
            "version": "1.0.0",
            "status": "stable",
            "description": "Reactive TALL Stack with Flux UI, Volt single-file components, Folio page routing, Fortify authentication, and PostgreSQL.",
            "stack": {
                "language": "PHP 8.3+",
                "framework": "Laravel 12",
                "admin_panel": "Livewire 4 + Flux UI",
                "database": "PostgreSQL 16+",
                "extra": ["Volt", "Folio", "Fortify"]
            },
            "security": {"gitleaks": True, "semgrep": True, "auth_enforced": True, "input_validation_enforced": True}
        },
        {
            "slug": "laravel-mongodb",
            "name": "Laravel 12 + MongoDB (NoSQL)",
            "version": "1.0.0",
            "status": "stable",
            "description": "Pioneer document store stack. Official mongodb/laravel-mongodb package, embedded documents, aggregation pipelines, and custom React/Inertia dashboard.",
            "stack": {
                "language": "PHP 8.3+",
                "framework": "Laravel 12",
                "database": "MongoDB 7.0+",
                "admin_panel": "Inertia + React",
                "extra": ["mongodb/laravel-mongodb"]
            },
            "security": {"gitleaks": True, "semgrep": True, "auth_enforced": True, "input_validation_enforced": True}
        },
        {
            "slug": "nextjs-approuter-supabase",
            "name": "Next.js 15+ + Supabase + shadcn/ui",
            "version": "1.0.0",
            "status": "stable",
            "description": "React Server Components, Server Actions with Zod validation, Row-Level Security in Supabase/PostgreSQL, and shadcn/ui tokens.",
            "stack": {
                "language": "TypeScript 5+",
                "framework": "Next.js 15 (Turbopack)",
                "database": "Supabase / PostgreSQL",
                "extra": ["shadcn/ui", "Zod", "Server Actions"]
            },
            "security": {"gitleaks": True, "semgrep": True, "auth_enforced": True, "input_validation_enforced": True}
        },
        {
            "slug": "laravel-mysql",
            "name": "Laravel + MySQL Dashboard (Blueprint)",
            "version": "1.0.0-blueprint",
            "status": "blueprint",
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
            "slug": "django-tailwind-postgresql",
            "name": "Django 5+ + Tailwind + PostgreSQL",
            "version": "1.0.0-blueprint",
            "status": "blueprint",
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
            "status": "blueprint",
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
            "status": "blueprint",
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
            "status": "blueprint",
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
            "status": "blueprint",
            "description": "Binary, firmware, and AST code analysis tools structured for AI agents. GhidraMCP, Radare2, Semgrep rule authoring, and memory safety checks.",
            "stack": {
                "language": "Python 3.12+",
                "framework": "GhidraMCP + Radare2",
                "extra": ["Semgrep AST", "Binary Ninja API"]
            },
            "security": {"gitleaks": True, "semgrep": True, "sandboxed_tools": True}
        }
    ]

    generated_urls = []
    generated_count = 0

    for kit in ten_kits:
        slug = kit["slug"]
        kit_dir = os.path.join(kits_base, slug)
        os.makedirs(kit_dir, exist_ok=True)

        manifest_path = os.path.join(kit_dir, "kit.yaml")
        meta = kit.copy()
        if os.path.exists(manifest_path) and yaml is not None:
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

    # Generate complete dynamic sitemap.xml
    try:
        from tools.generate_sitemap import generate as gen_sitemap
        gen_sitemap()
    except Exception:
        import subprocess
        subprocess.run([sys.executable, "tools/generate_sitemap.py"])
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
        replacement = "\\n".join(entries_to_add) + "\\n</urlset>"
        content = content.replace("</urlset>", replacement)
        with open(sitemap_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Added {len(entries_to_add)} URLs to sitemap.xml")

if __name__ == "__main__":
    build_all()
