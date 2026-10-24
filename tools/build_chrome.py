#!/usr/bin/env python3
"""Single source for the site header and footer.

    python tools/build_chrome.py            # rewrite chrome in every page
    python tools/build_chrome.py --check    # fail if any page has drifted
    python tools/build_chrome.py --list     # show which pages would change

The navbar and footer were previously duplicated across ~78 hand-maintained
HTML files, so a link added in one place silently went missing everywhere
else. This module holds them once; the page generators import NAV/FOOTER from
here, and the CLI rewrites the static pages between the existing
<header>...</header> and <footer>...</footer> boundaries.

Links are root-absolute (/kits/, /security/) so one string works at every
directory depth. The site is served from a domain root, locally and in
production.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

GITHUB = "https://github.com/Umar-444/Techtalks-stack-kits"

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "src", "templates"}

_LINK = ("text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] "
         "dark:hover:text-white font-medium transition-colors")
_ACTIVE = "text-[#12140F] dark:text-white font-semibold border-b-2 border-[#E85D26] pb-[1px] transition-colors"
_FOOT = ("text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] "
         "dark:hover:text-white transition-colors")
_DROP = ("flex flex-col px-3 py-2 rounded-[6px] hover:bg-[#F7F7F3] "
         "dark:hover:bg-[#202422] transition-colors")

#: Kits surfaced in the Kits dropdown. Verified ones lead, because those are
#: the ones a visitor can clone and run today.
FEATURED_KITS = [
    ("flask-htmx-sqlite", "Flask + HTMX + SQLite", "Verified &middot; 27 tests green", True),
    ("django-api-ninja", "Django + Django Ninja", "Verified &middot; 39 tests green", True),
    ("laravel-api-sanctum", "Laravel + Sanctum API", "Verified &middot; 21 tests green", True),
    ("laravel-filament-postgresql", "Laravel + Filament", "Admin panel, multi-tenancy, audit log", False),
    ("nextjs-prisma-postgresql", "Next.js + Prisma", "App Router, Server Actions, Prisma ORM", False),
]


def _nav_link(href: str, label: str, active: str | None, key: str) -> str:
    cls = _ACTIVE if active == key else _LINK
    return f'<a href="{href}" class="{cls}">{label}</a>'


def nav_html(active: str | None = None) -> str:
    """Render the sticky header. `active` is one of the nav keys."""
    featured = "\n".join(
        f'''              <a href="/kits/{slug}/" class="{_DROP}">
                <span class="text-[13px] font-semibold text-[#12140F] dark:text-white">{title}{
                  ' <span class="ml-1 font-mono text-[9px] uppercase tracking-wider text-[#1F7A4D] dark:text-[#6EE7A8]">verified</span>' if verified else ''
                }</span>
                <span class="text-[11px] text-[#5C6058] dark:text-[#A8ACA0]">{desc}</span>
              </a>'''
        for slug, title, desc, verified in FEATURED_KITS
    )

    return f'''<header
    class="sticky top-0 z-50 h-[60px] bg-white/90 dark:bg-[#0F1110]/90 backdrop-blur-md border-b border-[#E6E6DF] dark:border-[#2A2E2A] transition-colors">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex items-center justify-between">

      <div class="flex items-center gap-8">
        <a href="/" class="flex items-center gap-2.5 group select-none" aria-label="TechTalks Stack Kits Home">
          <div
            class="w-[30px] h-[30px] rounded-[6px] bg-[#E85D26] flex items-center justify-center text-white font-bold text-xs">
            <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24">
              <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
            </svg>
          </div>
          <div class="flex items-baseline">
            <span
              class="font-bold text-[17px] tracking-[-0.02em] text-[#12140F] dark:text-[#F2F2EC] group-hover:text-[#E85D26] transition-colors">TechTalks</span>
            <span
              class="font-mono text-[10px] uppercase tracking-wider text-[#5C6058] dark:text-[#A8ACA0] font-semibold ml-2">STACK
              KITS</span>
          </div>
        </a>

        <nav class="hidden md:flex items-center gap-6 text-[15px]" aria-label="Main Navigation">

          <div class="relative group py-2">
            <a href="/kits/" class="flex items-center gap-1 {_LINK}">
              <span>Kits</span>
              <svg
                class="w-3.5 h-3.5 text-[#8C9088] group-hover:text-[#12140F] dark:group-hover:text-white transition-transform group-hover:rotate-180"
                fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </a>
            <div
              class="absolute top-full left-0 w-80 bg-white dark:bg-[#171A18] border border-[#E6E6DF] dark:border-[#2A2E2A] rounded-[8px] p-2 shadow-lg hidden group-hover:block transition-all z-50">
              <div class="px-3 py-1.5 font-mono text-[11px] uppercase tracking-wider text-[#8C9088] font-semibold">
                Featured kits
              </div>
{featured}
              <div class="border-t border-[#E6E6DF] dark:border-[#2A2E2A] my-1"></div>
              <a href="/kits/"
                class="flex items-center justify-between px-3 py-2 rounded-[6px] hover:bg-[#F7F7F3] dark:hover:bg-[#202422] text-[13px] font-semibold text-[#12140F] dark:text-white transition-colors">
                <span>All 35 kits</span>
                <span class="font-mono text-xs text-[#E85D26]">&rarr;</span>
              </a>
              <a href="/status/"
                class="flex items-center justify-between px-3 py-2 rounded-[6px] hover:bg-[#F7F7F3] dark:hover:bg-[#202422] text-[13px] text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white transition-colors">
                <span>Which kits are verified?</span>
                <span class="font-mono text-xs text-[#E85D26]">&rarr;</span>
              </a>
              <a href="{GITHUB}/issues/new?template=new-topic.yml" target="_blank" rel="noopener noreferrer"
                class="flex items-center justify-between px-3 py-2 rounded-[6px] hover:bg-[#F7F7F3] dark:hover:bg-[#202422] text-[13px] text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white transition-colors">
                <span>Propose a kit</span>
                <span class="text-xs">&nearr;</span>
              </a>
            </div>
          </div>

          {_nav_link("/start/", "How It Works", active, "start")}

          <div class="relative group py-2">
            <a href="/security/" class="flex items-center gap-1 {_ACTIVE if active in ('security', 'coverage', 'status') else _LINK}">
              <span>Standards</span>
              <svg
                class="w-3.5 h-3.5 text-[#8C9088] group-hover:text-[#12140F] dark:group-hover:text-white transition-transform group-hover:rotate-180"
                fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </a>
            <div
              class="absolute top-full left-0 w-72 bg-white dark:bg-[#171A18] border border-[#E6E6DF] dark:border-[#2A2E2A] rounded-[8px] p-2 shadow-lg hidden group-hover:block transition-all z-50">
              <a href="/security/" class="{_DROP}">
                <span class="text-[13px] font-semibold text-[#12140F] dark:text-white">Security Standard</span>
                <span class="text-[11px] text-[#5C6058] dark:text-[#A8ACA0]">Three-layer guardrails for coding agents</span>
              </a>
              <a href="/security/coverage/" class="{_DROP}">
                <span class="text-[13px] font-semibold text-[#12140F] dark:text-white">OWASP Coverage Matrix</span>
                <span class="text-[11px] text-[#5C6058] dark:text-[#A8ACA0]">433 controls mapped to Top 10:2025</span>
              </a>
              <a href="/status/" class="{_DROP}">
                <span class="text-[13px] font-semibold text-[#12140F] dark:text-white">Kit Status Board</span>
                <span class="text-[11px] text-[#5C6058] dark:text-[#A8ACA0]">Verified vs scaffold, from executed runs</span>
              </a>
              <a href="/security/laravel/" class="{_DROP}">
                <span class="text-[13px] font-semibold text-[#12140F] dark:text-white">Security Masterclass</span>
                <span class="text-[11px] text-[#5C6058] dark:text-[#A8ACA0]">22 lessons: PHP, Laravel and AI security</span>
              </a>
            </div>
          </div>

          {_nav_link("/blog/", "Blog", active, "blog")}
        </nav>
      </div>

      <div class="flex items-center gap-3">

        <button type="button"
          class="hidden sm:inline-flex items-center gap-2 h-[36px] px-2.5 rounded-[6px] border border-[#E6E6DF] dark:border-[#2A2E2A] text-xs text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white hover:bg-[#F7F7F3] dark:hover:bg-[#171A18] transition-colors"
          id="search-palette-trigger" data-search-trigger aria-label="Search kits and documentation">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <span>Search</span>
          <kbd
            class="font-mono text-[10px] px-1.5 py-0.5 rounded bg-[#F4F4F0] dark:bg-[#202422] border border-[#E6E6DF] dark:border-[#2A2E2A]">Ctrl
            K</kbd>
        </button>

        <a href="{GITHUB}" target="_blank" rel="noopener noreferrer"
          class="inline-flex items-center gap-1.5 h-[36px] px-2.5 rounded-[6px] border border-[#E6E6DF] dark:border-[#2A2E2A] text-xs font-mono text-[#12140F] dark:text-white hover:bg-[#F7F7F3] dark:hover:bg-[#171A18] transition-colors"
          title="View repository on GitHub">
          <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24">
            <path fill-rule="evenodd" clip-rule="evenodd"
              d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
          </svg>
          <span class="text-xs font-semibold text-[#12140F] dark:text-[#F2F2EC]">Star</span>
        </a>

        <button id="theme-toggle" type="button" aria-label="Toggle theme"
          class="w-[36px] h-[36px] rounded-[6px] flex items-center justify-center text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white hover:bg-[#F7F7F3] dark:hover:bg-[#171A18] transition-colors focus:outline-none focus:ring-2 focus:ring-[#E85D26]">
          <svg class="w-4 h-4 hidden dark:block" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          <svg class="w-4 h-4 block dark:hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
          </svg>
        </button>

        <a href="/kits/"
          class="hidden sm:inline-flex items-center justify-center h-[38px] px-4 rounded-[6px] text-[14px] font-semibold bg-[#12140F] text-white hover:bg-[#2A2E2C] dark:bg-white dark:text-[#12140F] dark:hover:bg-[#EAECE8] focus:outline-none focus:ring-2 focus:ring-[#E85D26] focus:ring-offset-2 transition-colors select-none">
          Get a Kit
        </a>

        <button id="mobile-menu-toggle" type="button" aria-label="Toggle navigation menu"
          class="md:hidden w-[36px] h-[36px] rounded-[6px] flex items-center justify-center text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white hover:bg-[#F7F7F3] dark:hover:bg-[#171A18] transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>

      </div>
    </div>

    <div id="mobile-menu"
      class="hidden md:hidden fixed inset-x-0 top-[60px] bottom-0 bg-white dark:bg-[#0F1110] border-t border-[#E6E6DF] dark:border-[#2A2E2A] p-6 flex flex-col justify-between overflow-y-auto z-40">
      <div class="space-y-4">

        <div class="font-mono text-xs uppercase tracking-wider text-[#8C9088] font-semibold">Navigation</div>

        <div class="flex flex-col text-[17px] font-medium space-y-3 pb-4 border-b border-[#E6E6DF] dark:border-[#2A2E2A]">
          <a href="/kits/" class="text-[#12140F] dark:text-white font-semibold flex items-center justify-between">
            <span>Kits</span>
            <span class="text-xs font-mono text-[#E85D26]">All 35 &rarr;</span>
          </a>
          <div class="pl-3 flex flex-col space-y-2 text-[14px] text-[#5C6058] dark:text-[#A8ACA0]">
            <a href="/kits/flask-htmx-sqlite/">&bull; Flask + HTMX + SQLite</a>
            <a href="/kits/django-api-ninja/">&bull; Django + Django Ninja</a>
            <a href="/kits/laravel-api-sanctum/">&bull; Laravel + Sanctum API</a>
          </div>
        </div>

        <div class="flex flex-col text-[17px] font-medium space-y-3 pb-4 border-b border-[#E6E6DF] dark:border-[#2A2E2A]">
          <a href="/start/" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white">How It Works</a>
          <a href="/security/" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white">Security Standard</a>
          <a href="/security/coverage/" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white">OWASP Coverage</a>
          <a href="/status/" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white">Kit Status Board</a>
          <a href="/blog/" class="text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white">Blog</a>
        </div>

      </div>

      <div class="pt-6 border-t border-[#E6E6DF] dark:border-[#2A2E2A]">
        <a href="/kits/"
          class="w-full inline-flex items-center justify-center h-[42px] rounded-[6px] text-[15px] font-semibold bg-[#12140F] text-white dark:bg-white dark:text-[#12140F] transition-colors">
          Get a Kit &rarr;
        </a>
      </div>
    </div>
  </header>'''


def footer_html() -> str:
    return f'''<footer
    class="bg-[#F7F7F3] dark:bg-[#111312] border-t border-[#E6E6DF] dark:border-[#2A2E2A] pt-16 pb-12 transition-colors">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

      <!-- 1 col on phones, 2 on small tablets, 12-col track from lg. Going
           straight from 1 to 4 columns at md cramped the link lists on
           768-1024px screens. -->
      <div
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-12 gap-x-8 gap-y-10 pb-12 border-b border-[#E6E6DF] dark:border-[#2A2E2A]">

        <div class="sm:col-span-2 lg:col-span-4 space-y-4">
          <div class="flex items-center gap-2.5">
            <div
              class="w-[28px] h-[28px] rounded-[6px] bg-[#E85D26] flex items-center justify-center text-white text-xs font-bold shrink-0">
              <svg class="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24">
                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
              </svg>
            </div>
            <div class="flex items-baseline">
              <span class="font-bold text-[17px] tracking-[-0.02em] text-[#12140F] dark:text-[#F2F2EC]">TechTalks</span>
              <span
                class="font-mono text-[10px] uppercase tracking-wider text-[#5C6058] dark:text-[#A8ACA0] font-semibold ml-2">STACK
                KITS</span>
            </div>
          </div>
          <p class="text-[14px] text-[#5C6058] dark:text-[#A8ACA0] leading-[1.6] max-w-sm">
            Stack kits for AI coding agents: starter code, rules in 8 agent dialects, skills, design tokens
            and OWASP-mapped security checks in one clone.
          </p>

          <div class="flex items-center gap-2 pt-1">
            <a href="{GITHUB}" target="_blank" rel="noopener noreferrer"
              class="w-8 h-8 rounded-full border border-[#E6E6DF] dark:border-[#2A2E2A] flex items-center justify-center text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white hover:border-[#12140F] dark:hover:border-white transition-colors"
              aria-label="GitHub">
              <svg class="w-[18px] h-[18px] fill-current" viewBox="0 0 24 24">
                <path fill-rule="evenodd" clip-rule="evenodd"
                  d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
              </svg>
            </a>
            <a href="https://linkedin.com/in/umar444" target="_blank" rel="noopener noreferrer"
              class="w-8 h-8 rounded-full border border-[#E6E6DF] dark:border-[#2A2E2A] flex items-center justify-center text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white hover:border-[#12140F] dark:hover:border-white transition-colors"
              aria-label="LinkedIn">
              <svg class="w-[18px] h-[18px] fill-current" viewBox="0 0 24 24">
                <path
                  d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" />
              </svg>
            </a>
            <a href="https://x.com/@umartechtalks" target="_blank" rel="noopener noreferrer"
              class="w-8 h-8 rounded-full border border-[#E6E6DF] dark:border-[#2A2E2A] flex items-center justify-center text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white hover:border-[#12140F] dark:hover:border-white transition-colors"
              aria-label="X (Twitter)">
              <svg class="w-[18px] h-[18px] fill-current" viewBox="0 0 24 24">
                <path
                  d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
              </svg>
            </a>
            <a href="https://youtube.com/@umartechtalks" target="_blank" rel="noopener noreferrer"
              class="w-8 h-8 rounded-full border border-[#E6E6DF] dark:border-[#2A2E2A] flex items-center justify-center text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white hover:border-[#12140F] dark:hover:border-white transition-colors"
              aria-label="YouTube">
              <svg class="w-[18px] h-[18px] fill-current" viewBox="0 0 24 24">
                <path
                  d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z" />
              </svg>
            </a>
          </div>

          <div class="pt-2 text-xs text-[#5C6058] dark:text-[#A8ACA0]">
            By Umar Farooq &bull; <a href="https://itsumarfarooq.com" target="_blank" rel="noopener noreferrer"
              class="text-[#12140F] dark:text-white font-medium hover:text-[#E85D26] underline transition-colors">itsumarfarooq.com
              &nearr;</a>
          </div>
        </div>

        <div class="lg:col-span-2 space-y-3">
          <div class="font-mono text-xs uppercase tracking-wider text-[#12140F] dark:text-white font-semibold">Kits</div>
          <ul class="space-y-2.5 text-[14px] break-words">
            <li><a href="/kits/flask-htmx-sqlite/" class="{_FOOT}">Flask + HTMX</a></li>
            <li><a href="/kits/django-api-ninja/" class="{_FOOT}">Django Ninja</a></li>
            <li><a href="/kits/laravel-api-sanctum/" class="{_FOOT}">Laravel Sanctum</a></li>
            <li><a href="/kits/laravel-filament-postgresql/" class="{_FOOT}">Laravel + Filament</a></li>
            <li><a href="/kits/nextjs-prisma-postgresql/" class="{_FOOT}">Next.js + Prisma</a></li>
            <li><a href="/kits/" class="font-medium text-[#12140F] dark:text-white hover:text-[#E85D26] transition-colors">All 35 Kits &rarr;</a></li>
          </ul>
        </div>

        <div class="lg:col-span-3 space-y-3">
          <div class="font-mono text-xs uppercase tracking-wider text-[#12140F] dark:text-white font-semibold">Standards &amp; Proof</div>
          <ul class="space-y-2.5 text-[14px] break-words">
            <li><a href="/security/" class="{_FOOT}">Security Standard</a></li>
            <li><a href="/security/coverage/" class="{_FOOT}">OWASP Top 10:2025 Coverage</a></li>
            <li><a href="/status/" class="{_FOOT}">Kit Status Board</a></li>
            <li><a href="/security/laravel/" class="{_FOOT}">Security Masterclass (22 lessons)</a></li>
            <li><a href="/security/coverage.json" class="font-mono text-xs {_FOOT}">coverage.json</a></li>
            <li><a href="/status.json" class="font-mono text-xs {_FOOT}">status.json</a></li>
            <li><a href="/schemas/kit-security-checks.schema.json" class="font-mono text-xs {_FOOT}">checks.schema.json</a></li>
          </ul>
        </div>

        <div class="lg:col-span-3 space-y-3">
          <div class="font-mono text-xs uppercase tracking-wider text-[#12140F] dark:text-white font-semibold">Project</div>
          <ul class="space-y-2.5 text-[14px] break-words">
            <li><a href="/start/" class="{_FOOT}">How It Works</a></li>
            <li><a href="/blog/" class="{_FOOT}">Blog</a></li>
            <li><a href="{GITHUB}" target="_blank" rel="noopener noreferrer" class="{_FOOT}">GitHub Repository &nearr;</a></li>
            <li><a href="{GITHUB}/blob/main/CHANGELOG.md" target="_blank" rel="noopener noreferrer" class="{_FOOT}">Changelog &nearr;</a></li>
            <li><a href="{GITHUB}/blob/main/CONTRIBUTING.md" target="_blank" rel="noopener noreferrer" class="{_FOOT}">Contributor Guide &nearr;</a></li>
            <li><a href="{GITHUB}/discussions" target="_blank" rel="noopener noreferrer" class="{_FOOT}">Discussions &nearr;</a></li>
            <li><a href="{GITHUB}/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22" target="_blank" rel="noopener noreferrer" class="{_FOOT}">Good First Issues &nearr;</a></li>
            <li><a href="/llms.txt" class="font-mono text-xs {_FOOT}">llms.txt</a></li>
            <li><a href="/sitemap.xml" class="font-mono text-xs {_FOOT}">sitemap.xml</a></li>
          </ul>
        </div>

      </div>

      <div
        class="pt-8 flex flex-col lg:flex-row items-center lg:justify-between text-center lg:text-left text-[13px] text-[#5C6058] dark:text-[#A8ACA0] gap-3 lg:gap-6">
        <div>
          &copy; 2026 Umar Farooq &bull; TechTalks Stack Kits &bull; <a
            href="{GITHUB}/blob/main/LICENSE" target="_blank"
            rel="noopener noreferrer" class="underline hover:text-[#12140F] dark:hover:text-white">MIT License</a>
        </div>
        <div class="text-center">
          Not affiliated with OWASP, Laravel, Filament, Anthropic or OpenAI.
        </div>
        <div>
          <a href="{GITHUB}" target="_blank" rel="noopener noreferrer"
            class="hover:text-[#12140F] dark:hover:text-white transition-colors inline-flex items-center gap-1">
            <span>Built in the open on GitHub</span>
            <span class="text-xs">&nearr;</span>
          </a>
        </div>
      </div>

    </div>
  </footer>'''


# --------------------------------------------------------------------------
# Applying the chrome to the static pages
# --------------------------------------------------------------------------

_HEADER_RE = re.compile(r"<header\b.*?</header>", re.S | re.I)
_FOOTER_RE = re.compile(r"<footer\b.*?</footer>", re.S | re.I)


def active_key_for(rel_path: str) -> str | None:
    if rel_path.startswith("status/"):
        return "status"
    if rel_path.startswith("security/coverage/"):
        return "coverage"
    if rel_path.startswith("security/"):
        return "security"
    if rel_path.startswith("blog/"):
        return "blog"
    if rel_path.startswith("start/"):
        return "start"
    if rel_path.startswith("kits/"):
        return "kits"
    return None


def pages() -> list[Path]:
    found = []
    for path in REPO_ROOT.rglob("*.html"):
        if any(part in SKIP_DIRS for part in path.relative_to(REPO_ROOT).parts):
            continue
        if path.name == "kit_page_template.html":
            continue
        found.append(path)
    return sorted(found)


def apply_to(path: Path) -> tuple[bool, str | None]:
    """Return (changed, reason_if_skipped)."""
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(REPO_ROOT).as_posix()

    if not _HEADER_RE.search(text):
        return False, "no <header> block"

    updated = _HEADER_RE.sub(lambda _m: nav_html(active_key_for(rel)), text, count=1)
    if _FOOTER_RE.search(updated):
        # Replace the last footer only; some pages nest a small footer in a card.
        matches = list(_FOOTER_RE.finditer(updated))
        last = matches[-1]
        updated = updated[:last.start()] + footer_html() + updated[last.end():]

    if updated == text:
        return False, None
    path.write_text(updated, encoding="utf-8")
    return True, None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if any page has drifted")
    parser.add_argument("--list", action="store_true", help="list pages that would change")
    args = parser.parse_args()

    targets = pages()
    if args.check or args.list:
        drifted, skipped = [], []
        for path in targets:
            text = path.read_text(encoding="utf-8")
            rel = path.relative_to(REPO_ROOT).as_posix()
            if not _HEADER_RE.search(text):
                skipped.append(rel)
                continue
            expected = _HEADER_RE.sub(lambda _m: nav_html(active_key_for(rel)), text, count=1)
            matches = list(_FOOTER_RE.finditer(expected))
            if matches:
                last = matches[-1]
                expected = expected[:last.start()] + footer_html() + expected[last.end():]
            if expected != text:
                drifted.append(rel)

        if args.list:
            print(f"{len(drifted)} page(s) would change, {len(skipped)} skipped (no header)")
            for rel in drifted:
                print(f"  ~ {rel}")
            return 0

        if drifted:
            print(f"FAIL — chrome drift in {len(drifted)} page(s):")
            for rel in drifted[:20]:
                print(f"  - {rel}")
            if len(drifted) > 20:
                print(f"  ... and {len(drifted) - 20} more")
            print("\nRegenerate with: python tools/build_chrome.py")
            return 1
        print(f"PASS — header and footer identical across {len(targets) - len(skipped)} page(s)")
        return 0

    changed, skipped = 0, []
    for path in targets:
        did, reason = apply_to(path)
        if reason:
            skipped.append(path.relative_to(REPO_ROOT).as_posix())
        elif did:
            changed += 1

    print(f"updated chrome in {changed} page(s); {len(skipped)} skipped (no header block)")
    for rel in skipped:
        print(f"  skipped: {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
