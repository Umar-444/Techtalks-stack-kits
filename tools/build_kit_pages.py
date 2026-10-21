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
  <!-- Fonts: Inter 400-800, JetBrains Mono, Newsreader italic (Document 17 Exact) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@1,6..72,400;1,6..72,500;1,6..72,600&display=swap" rel="stylesheet">
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

<!-- Master Navbar (Document 18 Exact: Sticky 60px, Paper 90% blur, Hairline border) -->
  <header class="sticky top-0 z-50 h-[60px] bg-white/90 dark:bg-[#0F1110]/90 backdrop-blur-md border-b border-[#E6E6DF] dark:border-[#2A2E2A] transition-colors">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex items-center justify-between">
      
      <!-- Left: Logo & Wordmark -->
      <div class="flex items-center gap-8">
        <a href="../../" class="flex items-center gap-2.5 group select-none" aria-label="TechTalks Stack Kits Home">
          <div class="w-[30px] h-[30px] rounded-[6px] bg-[#E85D26] flex items-center justify-center text-white font-bold text-xs shadow-none">
            <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24">
              <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
            </svg>
          </div>
          <div class="flex items-baseline">
            <span class="font-bold text-[17px] tracking-[-0.02em] text-[#12140F] dark:text-[#F2F2EC] group-hover:text-[#E85D26] transition-colors">TechTalks</span>
            <span class="font-mono text-[10px] uppercase tracking-wider text-[#5C6058] dark:text-[#A8ACA0] font-semibold ml-2">STACK KITS</span>
          </div>
        </a>

        <!-- Center / Left Desktop Navigation -->
        <nav class="hidden md:flex items-center gap-6 text-[15px]" aria-label="Main Navigation">
          
          <!-- Kits Dropdown -->
          <div class="relative group py-2">
            <a href="../../kits/" class="flex items-center gap-1 text-[#12140F] dark:text-white font-semibold border-b-2 border-[#E85D26] pb-[1px] transition-colors">
              <span>Kits</span>
              <svg class="w-3.5 h-3.5 text-[#8C9088] group-hover:text-[#12140F] dark:group-hover:text-white transition-transform group-hover:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </a>
            
            <!-- Hover dropdown menu -->
            <div class="absolute top-full left-0 w-72 bg-white dark:bg-[#171A18] border border-[#E6E6DF] dark:border-[#2A2E2A] rounded-[8px] p-2 shadow-lg hidden group-hover:block transition-all z-50">
              <div class="px-3 py-1.5 font-mono text-[11px] uppercase tracking-wider text-[#8C9088] font-semibold">
                Complete Kits (Ready to Ship)
              </div>
              <a href="../../kits/laravel-filament-postgresql/" class="flex flex-col px-3 py-2 rounded-[6px] hover:bg-[#F7F7F3] dark:hover:bg-[#202422] transition-colors">
                <span class="text-[13px] font-semibold text-[#12140F] dark:text-white">Laravel + Filament + PostgreSQL</span>
                <span class="text-[11px] text-[#5C6058] dark:text-[#A8ACA0]">Admin dashboard with multi-tenancy & audit logging</span>
              </a>
              <a href="../../kits/laravel-livewire-postgresql/" class="flex flex-col px-3 py-2 rounded-[6px] hover:bg-[#F7F7F3] dark:hover:bg-[#202422] transition-colors">
                <span class="text-[13px] font-semibold text-[#12140F] dark:text-white">Laravel + Livewire + PostgreSQL</span>
                <span class="text-[11px] text-[#5C6058] dark:text-[#A8ACA0]">Reactive full-stack SaaS foundation with Alpine.js</span>
              </a>
              <a href="../../kits/laravel-mongodb/" class="flex flex-col px-3 py-2 rounded-[6px] hover:bg-[#F7F7F3] dark:hover:bg-[#202422] transition-colors">
                <span class="text-[13px] font-semibold text-[#12140F] dark:text-white">Laravel + MongoDB</span>
                <span class="text-[11px] text-[#5C6058] dark:text-[#A8ACA0]">Document-oriented data layer with MongoDB 7+</span>
              </a>
              <a href="../../kits/nextjs-approuter-supabase/" class="flex flex-col px-3 py-2 rounded-[6px] hover:bg-[#F7F7F3] dark:hover:bg-[#202422] transition-colors">
                <span class="text-[13px] font-semibold text-[#12140F] dark:text-white">Next.js 15+ + Supabase</span>
                <span class="text-[11px] text-[#5C6058] dark:text-[#A8ACA0]">App Router, React 19, Server Actions & Supabase RLS</span>
              </a>
              <div class="border-t border-[#E6E6DF] dark:border-[#2A2E2A] my-1"></div>
              <a href="../../kits/" class="flex items-center justify-between px-3 py-2 rounded-[6px] hover:bg-[#F7F7F3] dark:hover:bg-[#202422] text-[13px] font-semibold text-[#12140F] dark:text-white transition-colors">
                <span>All kits and blueprints</span>
                <span class="font-mono text-xs text-[#E85D26]">&rarr;</span>
              </a>
              <a href="https://github.com/Umar-444/Techtalks-stack-kits/issues/new?template=new-topic.yml" target="_blank" rel="noopener noreferrer" class="flex items-center justify-between px-3 py-2 rounded-[6px] hover:bg-[#F7F7F3] dark:hover:bg-[#202422] text-[13px] text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white transition-colors">
                <span>Propose a kit</span>
                <span class="text-xs">&nearr;</span>
              </a>
            </div>
          </div>

          <a href="../../#how-it-works" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white font-medium transition-colors">How It Works</a>
          <a href="../../blog/" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white font-medium transition-colors">Blog</a>
          <a href="../../security/" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white font-medium transition-colors">Standards</a>
          <a href="https://github.com/Umar-444/Techtalks-stack-kits/discussions" target="_blank" rel="noopener noreferrer" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white font-medium transition-colors inline-flex items-center gap-1">
            <span>Community</span>
            <span class="text-xs text-[#8C9088]">&nearr;</span>
          </a>
        </nav>
      </div>

      <!-- Right: Search, GitHub with live star count, Theme Toggle, Primary CTA -->
      <div class="flex items-center gap-3">
        
        <!-- Search Button (Ctrl K hint) -->
        <button type="button" class="hidden sm:inline-flex items-center gap-2 h-[36px] px-2.5 rounded-[6px] border border-[#E6E6DF] dark:border-[#2A2E2A] text-xs text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white hover:bg-[#F7F7F3] dark:hover:bg-[#171A18] transition-colors" onclick="alert('Quick Search: Type to filter kits or press /kits/ to view catalogue.')">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <span>Search</span>
          <kbd class="font-mono text-[10px] px-1.5 py-0.5 rounded bg-[#F4F4F0] dark:bg-[#202422] border border-[#E6E6DF] dark:border-[#2A2E2A]">Ctrl K</kbd>
        </button>

        <!-- GitHub Repo with Stars Badge -->
        <a href="https://github.com/Umar-444/Techtalks-stack-kits" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1.5 h-[36px] px-2.5 rounded-[6px] border border-[#E6E6DF] dark:border-[#2A2E2A] text-xs font-mono text-[#12140F] dark:text-white hover:bg-[#F7F7F3] dark:hover:bg-[#171A18] transition-colors" title="View repository on GitHub">
          <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
          </svg>
          <span class="font-semibold text-xs text-[#8C9088]">&bull;</span>
          <span class="text-xs font-semibold text-[#12140F] dark:text-[#F2F2EC]">Star</span>
        </a>

        <!-- Theme Toggle Button -->
        <button id="theme-toggle" type="button" aria-label="Toggle theme" class="w-[36px] h-[36px] rounded-[6px] flex items-center justify-center text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white hover:bg-[#F7F7F3] dark:hover:bg-[#171A18] transition-colors focus:outline-none focus:ring-2 focus:ring-[#E85D26]">
          <!-- Sun Icon -->
          <svg class="w-4 h-4 hidden dark:block" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
          </svg>
          <!-- Moon Icon -->
          <svg class="w-4 h-4 block dark:hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
          </svg>
        </button>

        <!-- Primary CTA: Ink Background 'Get a Kit' -->
        <a href="../../kits/" class="hidden sm:inline-flex items-center justify-center h-[38px] px-4 rounded-[6px] text-[14px] font-semibold bg-[#12140F] text-white hover:bg-[#2A2E2C] dark:bg-white dark:text-[#12140F] dark:hover:bg-[#EAECE8] focus:outline-none focus:ring-2 focus:ring-[#E85D26] focus:ring-offset-2 transition-colors select-none">
          Get a Kit
        </a>

        <!-- Mobile Menu Hamburger -->
        <button id="mobile-menu-toggle" type="button" aria-label="Toggle navigation menu" class="md:hidden w-[36px] h-[36px] rounded-[6px] flex items-center justify-center text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white hover:bg-[#F7F7F3] dark:hover:bg-[#171A18] transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
          </svg>
        </button>

      </div>

    </div>

    <!-- Mobile Drawer Sheet (Document 18: Full-width sheet under header, links at 17px, kits expanded) -->
    <div id="mobile-menu" class="hidden md:hidden fixed inset-x-0 top-[60px] bottom-0 bg-white dark:bg-[#0F1110] border-t border-[#E6E6DF] dark:border-[#2A2E2A] p-6 flex flex-col justify-between overflow-y-auto z-40">
      <div class="space-y-4">
        
        <div class="font-mono text-xs uppercase tracking-wider text-[#8C9088] font-semibold">
          Navigation
        </div>
        
        <div class="flex flex-col text-[17px] font-medium space-y-3 pb-4 border-b border-[#E6E6DF] dark:border-[#2A2E2A]">
          <a href="../../kits/" class="text-[#12140F] dark:text-white font-semibold flex items-center justify-between">
            <span>Kits &amp; Blueprints</span>
            <span class="text-xs font-mono text-[#E85D26]">All &rarr;</span>
          </a>
          <div class="pl-3 flex flex-col space-y-2 text-[14px] text-[#5C6058] dark:text-[#A8ACA0]">
            <a href="../../kits/laravel-filament-postgresql/">&bull; Laravel + Filament + PostgreSQL</a>
            <a href="../../kits/laravel-livewire-postgresql/">&bull; Laravel + Livewire + PostgreSQL</a>
            <a href="../../kits/laravel-mongodb/">&bull; Laravel + MongoDB</a>
            <a href="../../kits/nextjs-approuter-supabase/">&bull; Next.js 15+ + Supabase</a>
          </div>
        </div>

        <div class="flex flex-col text-[17px] font-medium space-y-3 pb-4 border-b border-[#E6E6DF] dark:border-[#2A2E2A]">
          <a href="../../#how-it-works" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white">How It Works</a>
          <a href="../../blog/" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white">Blog</a>
          <a href="../../security/" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white">Standards</a>
          <a href="https://github.com/Umar-444/Techtalks-stack-kits/discussions" target="_blank" rel="noopener noreferrer" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white flex items-center justify-between">
            <span>Community</span>
            <span class="text-xs">&nearr;</span>
          </a>
        </div>

      </div>

      <div class="pt-6 border-t border-[#E6E6DF] dark:border-[#2A2E2A]">
        <a href="../../kits/" class="w-full inline-flex items-center justify-center h-[42px] rounded-[6px] text-[15px] font-semibold bg-[#12140F] text-white dark:bg-white dark:text-[#12140F] transition-colors">
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
  <!-- Master Footer (Document 18 Exact: Tint #F7F7F3, 4 Columns, Hairline, No Fake Newsletter) -->
  <footer class="bg-[#F7F7F3] dark:bg-[#111312] border-t border-[#E6E6DF] dark:border-[#2A2E2A] pt-16 pb-12 transition-colors">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <!-- 4 Columns Grid -->
      <div class="grid grid-cols-1 md:grid-cols-12 gap-8 pb-12 border-b border-[#E6E6DF] dark:border-[#2A2E2A]">
        
        <!-- Column 1: Brand (wider, ~1.4x) -->
        <div class="md:col-span-5 space-y-4">
          <div class="flex items-center gap-2.5">
            <div class="w-[28px] h-[28px] rounded-[6px] bg-[#E85D26] flex items-center justify-center text-white text-xs font-bold shrink-0">
              <svg class="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24">
                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
              </svg>
            </div>
            <div class="flex items-baseline">
              <span class="font-bold text-[17px] tracking-[-0.02em] text-[#12140F] dark:text-[#F2F2EC]">TechTalks</span>
              <span class="font-mono text-[10px] uppercase tracking-wider text-[#5C6058] dark:text-[#A8ACA0] font-semibold ml-2">STACK KITS</span>
            </div>
          </div>
          <p class="text-[14px] text-[#5C6058] dark:text-[#A8ACA0] leading-[1.6] max-w-sm">
            Complete stack kits for AI coding agents: starter code, rules, skills, design and security checks in one clone.
          </p>
          
          <!-- Social Icons Row (18px stroke icons, ghost circles with hairline border) -->
          <div class="flex items-center gap-2 pt-1">
            <!-- GitHub -->
            <a href="https://github.com/Umar-444/Techtalks-stack-kits" target="_blank" rel="noopener noreferrer" class="w-8 h-8 rounded-full border border-[#E6E6DF] dark:border-[#2A2E2A] flex items-center justify-center text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white hover:border-[#12140F] dark:hover:border-white transition-colors" aria-label="GitHub">
              <svg class="w-[18px] h-[18px] fill-current" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/></svg>
            </a>
            <!-- LinkedIn -->
            <a href="https://linkedin.com/in/itsumarfarooq" target="_blank" rel="noopener noreferrer" class="w-8 h-8 rounded-full border border-[#E6E6DF] dark:border-[#2A2E2A] flex items-center justify-center text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white hover:border-[#12140F] dark:hover:border-white transition-colors" aria-label="LinkedIn">
              <svg class="w-[18px] h-[18px] fill-current" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
            </a>
            <!-- X / Twitter -->
            <a href="https://x.com/itsumarfarooq" target="_blank" rel="noopener noreferrer" class="w-8 h-8 rounded-full border border-[#E6E6DF] dark:border-[#2A2E2A] flex items-center justify-center text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white hover:border-[#12140F] dark:hover:border-white transition-colors" aria-label="X (Twitter)">
              <svg class="w-[18px] h-[18px] fill-current" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
            </a>
            <!-- YouTube -->
            <a href="https://youtube.com/@itsumarfarooq" target="_blank" rel="noopener noreferrer" class="w-8 h-8 rounded-full border border-[#E6E6DF] dark:border-[#2A2E2A] flex items-center justify-center text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white hover:border-[#12140F] dark:hover:border-white transition-colors" aria-label="YouTube">
              <svg class="w-[18px] h-[18px] fill-current" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
            </a>
          </div>

          <div class="pt-2 text-xs text-[#5C6058] dark:text-[#A8ACA0]">
            By Umar Farooq &bull; <a href="https://itsumarfarooq.com" target="_blank" rel="noopener noreferrer" class="text-[#12140F] dark:text-white font-medium hover:text-[#E85D26] underline transition-colors">itsumarfarooq.com &nearr;</a>
          </div>
        </div>

        <!-- Column 2: Kits -->
        <div class="md:col-span-2 space-y-3">
          <div class="font-mono text-xs uppercase tracking-wider text-[#12140F] dark:text-white font-semibold">
            Kits
          </div>
          <ul class="space-y-2.5 text-[14px]">
            <li><a href="../../kits/laravel-filament-postgresql/" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white transition-colors">Laravel + Filament</a></li>
            <li><a href="../../kits/laravel-livewire-postgresql/" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white transition-colors">Laravel + Livewire</a></li>
            <li><a href="../../kits/laravel-mongodb/" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white transition-colors">Laravel + MongoDB</a></li>
            <li><a href="../../kits/nextjs-approuter-supabase/" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white transition-colors">Next.js + Supabase</a></li>
            <li><a href="../../kits/" class="font-medium text-[#12140F] dark:text-white hover:text-[#E85D26] transition-colors">All Kits &amp; Blueprints &rarr;</a></li>
            <li><a href="https://github.com/Umar-444/Techtalks-stack-kits/issues/new?template=new-topic.yml" target="_blank" rel="noopener noreferrer" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white transition-colors">Propose a Kit &nearr;</a></li>
          </ul>
        </div>

        <!-- Column 3: Resources -->
        <div class="md:col-span-2 space-y-3">
          <div class="font-mono text-xs uppercase tracking-wider text-[#12140F] dark:text-white font-semibold">
            Resources
          </div>
          <ul class="space-y-2.5 text-[14px]">
            <li><a href="../../blog/" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white transition-colors">Blog</a></li>
            <li><a href="../../#how-it-works" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white transition-colors">How It Works</a></li>
            <li><a href="../../security/" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white transition-colors">Security Standard</a></li>
            <li><a href="https://github.com/Umar-444/Techtalks-stack-kits/blob/main/CONTRIBUTING.md" target="_blank" rel="noopener noreferrer" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white transition-colors">Contributor Guide &nearr;</a></li>
            <li><a href="../../llms.txt" class="font-mono text-xs text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white transition-colors">llms.txt</a></li>
            <li><a href="../../sitemap.xml" class="font-mono text-xs text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white transition-colors">sitemap.xml</a></li>
          </ul>
        </div>

        <!-- Column 4: Community -->
        <div class="md:col-span-3 space-y-3">
          <div class="font-mono text-xs uppercase tracking-wider text-[#12140F] dark:text-white font-semibold">
            Community
          </div>
          <ul class="space-y-2.5 text-[14px]">
            <li><a href="https://github.com/Umar-444/Techtalks-stack-kits" target="_blank" rel="noopener noreferrer" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white transition-colors">GitHub Repository &nearr;</a></li>
            <li><a href="https://github.com/Umar-444/Techtalks-stack-kits/discussions" target="_blank" rel="noopener noreferrer" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white transition-colors">Discussions &nearr;</a></li>
            <li><a href="https://github.com/Umar-444/Techtalks-stack-kits/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22" target="_blank" rel="noopener noreferrer" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white transition-colors">Good First Issues &nearr;</a></li>
            <li><a href="../../blog/" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white transition-colors">Changelog &amp; Releases</a></li>
            <li><a href="https://itsumarfarooq.com#contact" target="_blank" rel="noopener noreferrer" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white transition-colors">Contact Maintainer &nearr;</a></li>
          </ul>
        </div>

      </div>

      <!-- Bottom Bar (Document 18: Hairline above, 13px muted, three items) -->
      <div class="pt-8 flex flex-col md:flex-row items-center justify-between text-[13px] text-[#5C6058] dark:text-[#A8ACA0] gap-4">
        <div>
          &copy; 2026 Umar Farooq &bull; TechTalks Stack Kits &bull; <a href="https://github.com/Umar-444/Techtalks-stack-kits/blob/main/LICENSE" target="_blank" rel="noopener noreferrer" class="underline hover:text-[#12140F] dark:hover:text-white">MIT License</a>
        </div>
        <div class="text-center">
          Not affiliated with Laravel, Filament, Anthropic or OpenAI.
        </div>
        <div>
          <a href="https://github.com/Umar-444/Techtalks-stack-kits" target="_blank" rel="noopener noreferrer" class="hover:text-[#12140F] dark:hover:text-white transition-colors inline-flex items-center gap-1">
            <span>Built in the open on GitHub</span>
            <span class="text-xs">&nearr;</span>
          </a>
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
