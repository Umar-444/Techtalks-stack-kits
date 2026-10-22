/**
 * TechTalks Stack Kits - Core Interactive Engine
 * Theme Toggle, Cmd+K / Ctrl+K Command Palette, UI interactions
 * Zero external dependencies.
 */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initTabs();
  initCommandPalette();
  initMobileMenu();
  initCopyButtons();
  initPromptCopyButtons();
  initFaqAccordions();
  initReadingProgressBar();
  initChecklistPersistence();
});

/* ==========================================================================
   1. Theme Management (Dark / Light Mode)
   ========================================================================== */
function initTheme() {
  const html = document.documentElement;

  const applyTheme = (theme) => {
    if (theme === 'dark') {
      html.classList.add('dark');
    } else {
      html.classList.remove('dark');
    }
  };

  const getSavedOrSystemTheme = () => {
    const saved = localStorage.getItem('theme');
    if (saved === 'light') return 'light';
    return 'dark'; // Dark-first showcase theme
  };

  // Ensure current theme matches preferred
  applyTheme(getSavedOrSystemTheme());

  // Listen to OS preference updates
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (!localStorage.getItem('theme')) {
      applyTheme(e.matches ? 'dark' : 'light');
    }
  });

  // Global delegated click listener for any theme toggle button or icon
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('#theme-toggle, [data-theme-toggle], .theme-toggle-btn, [aria-label="Toggle theme"]');
    if (!btn) return;

    e.preventDefault();
    e.stopPropagation();

    const isCurrentlyDark = html.classList.contains('dark');
    const newTheme = isCurrentlyDark ? 'light' : 'dark';
    applyTheme(newTheme);

    try {
      localStorage.setItem('theme', newTheme);
    } catch (err) {
      console.warn('localStorage theme write error:', err);
    }
  });
}

/* ==========================================================================
   2. Cmd+K / Ctrl+K Spotlight Command Palette
   ========================================================================== */
const SEARCH_INDEX = [{"title":"Browse All 30 Stack Kits","url":"/kits/","desc":"Complete directory with ecosystem filters and token cost benchmarks","badge":"Directory","tags":"catalogue filter kits tokens"},{"title":"How It Works / Quickstart","url":"/start/","desc":"Clone instructions, agent rules setup, and quickstart commands","badge":"Guide","tags":"start setup quickstart cursor claude copilot"},{"title":"Security Standards & Audits","url":"/security/","desc":"6-layer security model, secret scanning, SQLi, and OWASP benchmarks","badge":"Security","tags":"owasp gitleaks security rls headers"},{"title":"Engineering Blog & Releases","url":"/blog/","desc":"Architecture notes, kit expansion announcements, and benchmarks","badge":"Blog","tags":"articles news updates changelog"},{"title":"GitHub Repository","url":"https://github.com/Umar-444/Techtalks-stack-kits","desc":"Star the project, inspect source code, or contribute new kits","badge":"GitHub","tags":"github repo source star clone issue"},{"title":"Agentic LangGraph + CrewAI + FastAPI","url":"/kits/agentic-langgraph-crewai/","desc":"Multi-agent coordination architecture: LangGraph state machines paired with CrewAI role-playing autonomous agents and FastAPI.","badge":"LangGraph","tags":"Python LangGraph"},{"title":"Django + Django Ninja + PostgreSQL + Celery","url":"/kits/django-api-ninja/","desc":"API-only Django: all the batteries of Django (ORM, migrations, admin panel, authentication) behind high-speed typed Pydantic endpoints and asynchronous Celery workers.","badge":"Django Ninja","tags":"Python Django Ninja PostgreSQL"},{"title":"Django 5 + Tailwind CSS + PostgreSQL","url":"/kits/django-tailwind-postgresql/","desc":"Batteries-included full-stack Django 5 with Tailwind CSS design tokens, Django auth, and PostgreSQL 16+.","badge":"Django","tags":"Python Django PostgreSQL"},{"title":"Elixir + Phoenix 1.7+ + LiveView + Ecto + PostgreSQL","url":"/kits/elixir-phoenix-liveview/","desc":"Ultra-compact real-time full-stack application in a single functional language: Phoenix LiveView server-rendered state over WebSockets, Ecto changesets with compile-checked queries, and BEAM fault-tolerant processes.","badge":"Phoenix","tags":"Elixir Phoenix PostgreSQL"},{"title":"Flask + HTMX + SQLite","url":"/kits/flask-htmx-sqlite/","desc":"Minimal Python full-stack stack: single-file Flask, HTMX 2.0 reactive DOM boosts, and zero-ceremony SQLite persistence. The Python entry in the Token-Light line.","badge":"Flask","tags":"Python Flask SQLite"},{"title":"Go + Chi + templ + HTMX + sqlc + PostgreSQL","url":"/kits/go-chi-templ-htmx/","desc":"Minimalist flagship and token-light standard: Chi router (~1,000 LOC on pure net/http, zero dependencies), templ for compile-time type-safe HTML, HTMX 2.0 reactive DOM boosts, and sqlc type-safe SQL codegen.","badge":"Chi","tags":"Go Chi PostgreSQL"},{"title":"Go + Fiber + PostgreSQL","url":"/kits/go-fiber-api/","desc":"Throughput specialist: Express-shaped Go API powered by fasthttp zero-allocation engine. Ships with honest architectural caveats regarding net/http middleware and HTTP/2 limits.","badge":"Fiber","tags":"Go Fiber PostgreSQL"},{"title":"Go + Gin + sqlc + PostgreSQL + Redis","url":"/kits/go-gin-postgresql/","desc":"The mainstream production Go API kit: 48% Go web adoption, Gin HTTP engine with structured JSON middleware, sqlc queries, PostgreSQL 16+, and Redis cache.","badge":"Gin","tags":"Go Gin PostgreSQL"},{"title":"Laravel 13 + Filament 4 + PostgreSQL","url":"/kits/laravel-filament-postgresql/","desc":"Production-ready administrative platform and SaaS backend kit. Bundles verified Laravel 13, Filament 4 panels, strict PostgreSQL 16+ schema conventions, granular BOLA authorization policies, and automated AI security guardrails.","badge":"Laravel","tags":"PHP Laravel PostgreSQL"},{"title":"Laravel 12 + Livewire 4 + PostgreSQL","url":"/kits/laravel-livewire-postgresql/","desc":"Reactive full-stack TALL stack kit featuring Livewire 4, Volt single-file components, Folio page routing, Flux UI design tokens, Fortify authentication, and PostgreSQL 16+.","badge":"Laravel","tags":"PHP Laravel PostgreSQL"},{"title":"Laravel 12 + MongoDB (NoSQL)","url":"/kits/laravel-mongodb/","desc":"Empty-market pioneer stack combining Laravel 12 with the official mongodb/laravel-mongodb package, embedded document relations, aggregation pipeline builders, and custom Inertia/React dashboard.","badge":"Laravel","tags":"PHP Laravel MongoDB"},{"title":"Laravel 12 + MySQL Dashboard","url":"/kits/laravel-mysql/","desc":"Classic Laravel 12 monolithic web application featuring MySQL 8+, Fortify authentication, Blade templates, and responsive dashboard components.","badge":"Laravel","tags":"PHP Laravel MySQL"},{"title":"Next.js 15+ + Supabase + shadcn/ui","url":"/kits/nextjs-approuter-supabase/","desc":"Production fullstack React 19 / Next.js 15 App Router kit featuring Server Actions with Zod validation, Supabase Row-Level Security (RLS), and shadcn/ui design system tokens.","badge":"Next.js","tags":"TypeScript Next.js Supabase / PostgreSQL"},{"title":"Python + Litestar + SQLAlchemy 2 + PostgreSQL + Redis","url":"/kits/python-litestar-postgresql/","desc":"The modern ASGI framework FastAPI users graduate to: clean layered dependency injection, first-class DTOs, strict typing with msgspec and Pydantic v2, and SQLAlchemy 2.0 async sessions.","badge":"Litestar","tags":"Python Litestar PostgreSQL"},{"title":"RAG FastAPI + Qdrant + OpenAI","url":"/kits/rag-fastapi-qdrant/","desc":"High-speed semantic search & retrieval augmented generation API using FastAPI, Qdrant vector database, and streaming LLM responses.","badge":"FastAPI","tags":"Python FastAPI"},{"title":"Haystack Pipelines + Weaviate + FastAPI (Hayhooks)","url":"/kits/rag-haystack-weaviate/","desc":"Explicit, inspectable DAG production pipelines: deepset Haystack 2.5+, Weaviate vector database with hybrid BM25 + dense vector ranking, and 9 built-in production evaluators.","badge":"Haystack","tags":"Python Haystack"},{"title":"LangGraph + LangChain + Qdrant + Ragas Evals","url":"/kits/rag-langgraph-agentic/","desc":"Agentic RAG with cyclical state graph execution: agent decides dynamically when to retrieve, when to re-write queries, and when to invoke human-in-the-loop review with Ragas groundedness evals.","badge":"LangGraph","tags":"Python LangGraph"},{"title":"LlamaIndex + PostgreSQL pgvector + FastAPI","url":"/kits/rag-llamaindex-pgvector/","desc":"Data-first RAG on existing database infrastructure: LlamaIndex 0.11+ ingestion pipelines, PostgreSQL pgvector cosine similarity index, FastAPI streaming endpoints, and built-in faithfulness/relevancy evals.","badge":"LlamaIndex","tags":"Python LlamaIndex"},{"title":"Local Private RAG (Ollama + Chroma + FastAPI)","url":"/kits/rag-local-private/","desc":"100% offline, zero API egress, zero cloud cost: local open-weights LLMs via Ollama (Llama 3, Mistral, Qwen 2.5), local ChromaDB embeddings, fully PDPL and NDA compliant for regulated GCC enterprises.","badge":"FastAPI","tags":"Python FastAPI"},{"title":"Reverse Engineering & Security Audit Pack","url":"/kits/reverse-engineering-security/","desc":"Security auditing and reverse engineering suite: decompiler scripts, AST static analyzers, and invariant validation harnesses.","badge":"Security Audit CLI","tags":"Python Security Audit CLI"},{"title":"Ruby on Rails 8 + Hotwire (Turbo + Stimulus) + SQLite/PostgreSQL","url":"/kits/ruby-rails-hotwire/","desc":"The lowest full-stack token footprint on the platform (14,200 median build tokens): Rails 8 convention-over-configuration, Hotwire Turbo 8 reactive DOM morphing, Stimulus micro-controllers, and Solid Cache/Solid Queue on SQLite or PostgreSQL.","badge":"Ruby on Rails","tags":"Ruby Ruby on Rails SQLite / PostgreSQL"},{"title":"Rust + Actix Web + SeaORM + PostgreSQL","url":"/kits/rust-actix-postgresql/","desc":"High-throughput API champion: Actix Web actor-based multi-threaded engine paired with SeaORM dynamic async ORM and PostgreSQL.","badge":"Actix Web","tags":"Rust Actix Web PostgreSQL"},{"title":"Rust + Axum + Tokio + SQLx + PostgreSQL","url":"/kits/rust-axum-postgresql/","desc":"Modern async Rust web service built on Axum 0.8+, Tokio runtime, Tower middleware, and SQLx for compile-time verified SQL queries and injection resistance.","badge":"Axum","tags":"Rust Axum PostgreSQL"},{"title":"Rust + Leptos Full-Stack + Axum + WebAssembly","url":"/kits/rust-leptos-fullstack/","desc":"Full-stack Rust with reactive signals: Leptos SSR + WebAssembly hydration on client, Axum server functions on backend, one language and type system across the entire stack.","badge":"Leptos","tags":"Rust Leptos"},{"title":"Rust + Loco.rs + SeaORM + SQLite","url":"/kits/rust-loco-sqlite/","desc":"Rails-style convention-over-configuration for Rust: Loco.rs MVC architecture, predictable generators, SeaORM migrations, and zero-ceremony SQLite storage.","badge":"Loco.rs","tags":"Rust Loco.rs SQLite / PostgreSQL"},{"title":"DevSecOps CI Pipeline (Gitleaks, Semgrep, CodeQL, Trivy, SBOM)","url":"/kits/security-devsecops-ci/","desc":"Stack-agnostic, drop-in GitHub Actions DevSecOps workflow pipeline: automated Gitleaks secrets audit, Semgrep SAST, GitHub CodeQL, Aqua Trivy container/filesystem CVE scanner, Syft CycloneDX SBOM generation, and Dependabot.","badge":"GitHub Actions","tags":"YAML / Bash GitHub Actions"},{"title":"LLM Guardrails & AI Gateway (Pydantic AI + Llama Guard)","url":"/kits/security-llm-guardrails/","desc":"Stack-neutral AI security gateway: prompt injection screening, Presidio automated PII redaction pipeline, token and dollar budget limiters, and Pydantic AI strict output validation.","badge":"FastAPI","tags":"Python FastAPI"},{"title":"OWASP API Security Top 10 Reference + Pytest Attack Suite","url":"/kits/security-owasp-api/","desc":"Executable OWASP API Security Top 10 reference implementation built in FastAPI paired with a runnable pytest attack suite testing every control: BOLA, Broken Auth, BOPB, Rate Limiting, BFLA, and SSRF.","badge":"FastAPI","tags":"Python FastAPI"},{"title":"Passkeys WebAuthn + Hardened Auth Reference (TypeScript)","url":"/kits/security-passkeys-auth/","desc":"Verified passwordless FIDO2 / WebAuthn Passkeys authentication implementation in TypeScript: SimpleWebAuthn ceremonies, OAuth fallback, HttpOnly signed session cookies, and strict session fixation defenses.","badge":"Hono","tags":"TypeScript Hono"},{"title":"TypeScript + Hono + Bun + Drizzle + SQLite","url":"/kits/ts-hono-bun-sqlite/","desc":"The edge-minimal TypeScript stack: tiny API surface, zero build ceremony with Bun, Hono typed RPC, Drizzle type-safe schema migrations, and single-file-friendly microservices.","badge":"Hono","tags":"TypeScript Hono SQLite / LibSQL"}];

function initCommandPalette() {
  const isMac = typeof navigator !== 'undefined' && /Mac|iPod|iPhone|iPad/.test(navigator.userAgent);
  
  // Update keyboard shortcut text in headers if on Mac
  if (isMac) {
    document.querySelectorAll('kbd').forEach(el => {
      if (el.textContent.includes('Ctrl K') || el.textContent.includes('Ctrl')) {
        el.textContent = '⌘K';
      }
    });
  }

  let modal = null;
  let input = null;
  let resultsContainer = null;
  let activeIndex = 0;
  let filteredItems = [];

  const createPaletteDOM = () => {
    if (modal) return;

    modal = document.createElement('div');
    modal.id = 'command-palette-modal';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.className = 'fixed inset-0 z-[100] flex items-start justify-center pt-16 sm:pt-24 px-4 bg-black/60 dark:bg-black/80 backdrop-blur-sm hidden transition-opacity';

    modal.innerHTML = `
      <div id="palette-card" class="w-full max-w-2xl bg-white dark:bg-[#161816] border border-[#E6E6DF] dark:border-[#2A2E2A] rounded-xl shadow-2xl overflow-hidden flex flex-col max-h-[80vh] transition-all transform scale-100">
        
        <!-- Input Bar -->
        <div class="flex items-center px-4 py-3 border-b border-[#E6E6DF] dark:border-[#2A2E2A] gap-3 bg-white dark:bg-[#161816]">
          <svg class="w-5 h-5 text-[#8C9088] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input id="palette-search-input" type="text" placeholder="Search 30 stack kits, tech (Laravel, Next.js, Rust, Go, FastAPI...), standards..." class="w-full bg-transparent text-sm sm:text-base text-[#12140F] dark:text-[#F2F2EC] placeholder-[#8C9088] focus:outline-none" autocomplete="off" spellcheck="false" />
          <button type="button" id="palette-close-btn" class="text-xs font-mono px-2 py-1 rounded bg-[#F4F4F0] dark:bg-[#202422] text-[#5C6058] dark:text-[#A8ACA0] border border-[#E6E6DF] dark:border-[#2A2E2A] hover:text-[#12140F] dark:hover:text-white">
            ESC
          </button>
        </div>

        <!-- Results List -->
        <div id="palette-results-list" class="overflow-y-auto p-2 space-y-1 max-h-[55vh] select-none">
        </div>

        <!-- Footer Bar -->
        <div class="px-4 py-2.5 bg-[#FBFBFA] dark:bg-[#121413] border-t border-[#E6E6DF] dark:border-[#2A2E2A] flex items-center justify-between text-[11px] text-[#8C9088] font-mono select-none">
          <div class="flex items-center gap-3">
            <span><kbd class="px-1.5 py-0.5 rounded bg-black/5 dark:bg-white/10 text-[#5C6058] dark:text-[#A8ACA0]">↑</kbd> <kbd class="px-1.5 py-0.5 rounded bg-black/5 dark:bg-white/10 text-[#5C6058] dark:text-[#A8ACA0]">↓</kbd> navigate</span>
            <span><kbd class="px-1.5 py-0.5 rounded bg-black/5 dark:bg-white/10 text-[#5C6058] dark:text-[#A8ACA0]">↵</kbd> open</span>
            <span><kbd class="px-1.5 py-0.5 rounded bg-black/5 dark:bg-white/10 text-[#5C6058] dark:text-[#A8ACA0]">ESC</kbd> close</span>
          </div>
          <span class="text-[#E85D26] font-semibold">30 Kits Available</span>
        </div>

      </div>
    `;

    document.body.appendChild(modal);

    input = modal.querySelector('#palette-search-input');
    resultsContainer = modal.querySelector('#palette-results-list');

    // Close on backdrop click
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closePalette();
      }
    });

    // Close button
    modal.querySelector('#palette-close-btn').addEventListener('click', closePalette);

    // Live filtering input
    input.addEventListener('input', (e) => {
      renderResults(e.target.value);
    });

    // Keyboard navigation inside input
    input.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (filteredItems.length > 0) {
          activeIndex = (activeIndex + 1) % filteredItems.length;
          updateActiveItemHighlight();
        }
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (filteredItems.length > 0) {
          activeIndex = (activeIndex - 1 + filteredItems.length) % filteredItems.length;
          updateActiveItemHighlight();
        }
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (filteredItems[activeIndex]) {
          window.location.href = filteredItems[activeIndex].url;
        }
      } else if (e.key === 'Escape') {
        e.preventDefault();
        closePalette();
      }
    });
  };

  const updateActiveItemHighlight = () => {
    const renderedElements = resultsContainer.querySelectorAll('.palette-item');
    renderedElements.forEach((el, idx) => {
      if (idx === activeIndex) {
        el.classList.add('bg-[#F4F4F0]', 'dark:bg-[#202422]', 'border-[#E85D26]');
        el.scrollIntoView({ block: 'nearest' });
      } else {
        el.classList.remove('bg-[#F4F4F0]', 'dark:bg-[#202422]', 'border-[#E85D26]');
      }
    });
  };

  const renderResults = (queryText) => {
    const q = (queryText || '').trim().toLowerCase();
    
    if (!q) {
      filteredItems = SEARCH_INDEX;
    } else {
      filteredItems = SEARCH_INDEX.filter(item => {
        const titleMatch = item.title.toLowerCase().includes(q);
        const descMatch = (item.desc || '').toLowerCase().includes(q);
        const tagsMatch = (item.tags || '').toLowerCase().includes(q);
        const badgeMatch = (item.badge || '').toLowerCase().includes(q);
        return titleMatch || descMatch || tagsMatch || badgeMatch;
      });
    }

    activeIndex = 0;

    if (filteredItems.length === 0) {
      resultsContainer.innerHTML = `
        <div class="py-10 text-center space-y-2">
          <p class="text-sm text-[#12140F] dark:text-[#F2F2EC] font-semibold">No results found for "${queryText.replace(/</g, '&lt;')}"</p>
          <p class="text-xs text-[#5C6058] dark:text-[#A8ACA0]">Try searching for Laravel, FastAPI, Next.js, Rust, or <a href="/kits/" class="text-[#E85D26] underline font-medium">Browse All 30 Kits</a>.</p>
        </div>
      `;
      return;
    }

    resultsContainer.innerHTML = filteredItems.map((item, idx) => `
      <a href="${item.url}" data-idx="${idx}" class="palette-item group flex items-center justify-between p-2.5 rounded-lg text-left transition-colors cursor-pointer border border-transparent hover:bg-[#F4F4F0] dark:hover:bg-[#202422] ${idx === 0 ? 'bg-[#F4F4F0] dark:bg-[#202422] border-[#E85D26]' : ''}">
        <div class="min-w-0 pr-3">
          <div class="flex items-center gap-2">
            <span class="text-[13px] sm:text-sm font-semibold text-[#12140F] dark:text-[#F2F2EC] group-hover:text-[#E85D26] transition-colors truncate">${item.title}</span>
            <span class="font-mono text-[10px] px-1.5 py-0.5 rounded bg-black/5 dark:bg-white/10 text-[#5C6058] dark:text-[#A8ACA0] border border-[#E6E6DF] dark:border-[#2A2E2A] shrink-0">${item.badge}</span>
          </div>
          <div class="text-xs text-[#5C6058] dark:text-[#A8ACA0] truncate mt-0.5">${item.desc}</div>
        </div>
        <svg class="w-4 h-4 text-[#8C9088] group-hover:text-[#E85D26] shrink-0 transition-transform group-hover:translate-x-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
        </svg>
      </a>
    `).join('');

    // Attach hover listener to update activeIndex on mousemove
    resultsContainer.querySelectorAll('.palette-item').forEach(el => {
      el.addEventListener('mouseenter', () => {
        activeIndex = parseInt(el.getAttribute('data-idx') || '0', 10);
        updateActiveItemHighlight();
      });
    });
  };

  const openPalette = () => {
    createPaletteDOM();
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    input.value = '';
    renderResults('');
    setTimeout(() => {
      input.focus();
    }, 50);
  };

  const closePalette = () => {
    if (!modal || modal.classList.contains('hidden')) return;
    modal.classList.add('hidden');
    document.body.style.overflow = '';
  };

  const togglePalette = () => {
    if (modal && !modal.classList.contains('hidden')) {
      closePalette();
    } else {
      openPalette();
    }
  };

  // Global keydown shortcut listener: Cmd+K / Ctrl+K
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && (e.key === 'k' || e.key === 'K')) {
      e.preventDefault();
      togglePalette();
    }
  });

  // Global click delegator for any search trigger element
  document.addEventListener('click', (e) => {
    const trigger = e.target.closest('#search-palette-trigger, [data-search-trigger], [data-open-search]');
    if (trigger) {
      e.preventDefault();
      e.stopPropagation();
      openPalette();
      return;
    }

    // Fallback: any button containing Search and kbd
    const btn = e.target.closest('button');
    if (btn && btn.querySelector('kbd') && btn.textContent.toLowerCase().includes('search')) {
      e.preventDefault();
      e.stopPropagation();
      openPalette();
    }
  });
}

/* ==========================================================================
   3. Mobile Navigation Menu
   ========================================================================== */
function initMobileMenu() {
  const menuBtn = document.getElementById('mobile-menu-btn') || document.getElementById('mobile-menu-toggle');
  const mobileMenu = document.getElementById('mobile-menu');

  if (!menuBtn || !mobileMenu) return;

  menuBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const isExpanded = menuBtn.getAttribute('aria-expanded') === 'true';
    menuBtn.setAttribute('aria-expanded', !isExpanded);
    mobileMenu.classList.toggle('hidden');
  });
}

/* ==========================================================================
   4. Code Block Copy Buttons
   ========================================================================== */
function initCopyButtons() {
  const copyButtons = document.querySelectorAll('.code-copy-btn');
  const cmdButtons = document.querySelectorAll('[data-copy-cmd]');

  cmdButtons.forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const cmd = btn.getAttribute('data-copy-cmd');
      if (!cmd) return;
      try {
        await navigator.clipboard.writeText(cmd);
        const originalHtml = btn.innerHTML;
        btn.innerHTML = `<svg class="w-3.5 h-3.5 text-emerald-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg><span class="text-emerald-600 dark:text-emerald-400 font-semibold text-xs">Copied!</span>`;
        btn.classList.add('border-emerald-500/50');
        setTimeout(() => {
          btn.innerHTML = originalHtml;
          btn.classList.remove('border-emerald-500/50');
        }, 2200);
      } catch (err) {
        console.error('Clipboard copy failed:', err);
      }
    });
  });

  copyButtons.forEach(button => {
    button.addEventListener('click', async () => {
      const container = button.closest('.code-container');
      if (!container) return;

      const codeElement = container.querySelector('code');
      if (!codeElement) return;

      const textToCopy = codeElement.innerText;

      try {
        await navigator.clipboard.writeText(textToCopy);
        const originalHtml = button.innerHTML;
        button.innerHTML = `
          <svg class="w-3.5 h-3.5 text-emerald-400 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
          <span class="text-emerald-400 font-medium">Copied!</span>
        `;
        button.classList.add('bg-slate-700');

        setTimeout(() => {
          button.innerHTML = originalHtml;
          button.classList.remove('bg-slate-700');
        }, 2000);
      } catch (err) {
        console.error('Copy to clipboard failed:', err);
      }
    });
  });
}

/* ==========================================================================
   5. Prompt Template Copy Buttons
   ========================================================================== */
function initPromptCopyButtons() {
  const promptButtons = document.querySelectorAll('[data-copy-prompt]');

  promptButtons.forEach(btn => {
    btn.addEventListener('click', async () => {
      const targetId = btn.getAttribute('data-copy-prompt');
      const targetElement = document.getElementById(targetId);
      if (!targetElement) return;

      const text = targetElement.innerText.trim();

      try {
        await navigator.clipboard.writeText(text);
        const originalText = btn.innerText;
        btn.innerText = 'Prompt Copied!';
        btn.classList.add('bg-emerald-600', 'text-white');

        setTimeout(() => {
          btn.innerText = originalText;
          btn.classList.remove('bg-emerald-600', 'text-white');
        }, 2000);
      } catch (e) {
        console.error('Prompt copy failed:', e);
      }
    });
  });
}

/* ==========================================================================
   6. FAQ Accordions
   ========================================================================== */
function initFaqAccordions() {
  const faqQuestions = document.querySelectorAll('.faq-question');

  faqQuestions.forEach(btn => {
    btn.addEventListener('click', () => {
      const isExpanded = btn.getAttribute('aria-expanded') === 'true';
      const answer = btn.nextElementSibling;
      const chevron = btn.querySelector('.faq-chevron');

      btn.setAttribute('aria-expanded', !isExpanded);

      if (isExpanded) {
        answer.classList.add('hidden');
        if (chevron) chevron.classList.remove('rotate-180');
      } else {
        answer.classList.remove('hidden');
        if (chevron) chevron.classList.add('rotate-180');
      }
    });
  });
}

/* ==========================================================================
   7. Reading Progress Bar (Lesson Pages)
   ========================================================================== */
function initReadingProgressBar() {
  const progressBar = document.getElementById('reading-progress-bar');
  if (!progressBar) return;

  window.addEventListener('scroll', () => {
    const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
    if (totalHeight <= 0) return;

    const progress = (window.scrollY / totalHeight) * 100;
    progressBar.style.width = `${Math.min(100, Math.max(0, progress))}%`;
  }, { passive: true });
}

/* ==========================================================================
   8. Checklist State Persistence (localStorage)
   ========================================================================== */
function initChecklistPersistence() {
  const checklistCheckboxes = document.querySelectorAll('.checklist-checkbox');
  if (checklistCheckboxes.length === 0) return;

  const pageKey = 'checklist_' + window.location.pathname;

  try {
    const saved = JSON.parse(localStorage.getItem(pageKey) || '{}');
    checklistCheckboxes.forEach((cb, idx) => {
      if (saved[idx]) {
        cb.checked = true;
      }
      cb.addEventListener('change', () => {
        saved[idx] = cb.checked;
        localStorage.setItem(pageKey, JSON.stringify(saved));
      });
    });
  } catch (e) {
    console.warn('Checklist storage disabled:', e);
  }
}

/* ==========================================================================
   Tabbed Variants Component (Agent Dialects & Platforms)
   ========================================================================== */
function initTabs() {
  document.addEventListener('click', (e) => {
    const tabBtn = e.target.closest('[data-tab-target]');
    if (!tabBtn) return;
    
    const container = tabBtn.closest('[data-tabs-container]');
    if (!container) return;
    
    const targetId = tabBtn.getAttribute('data-tab-target');
    const allButtons = container.querySelectorAll('[data-tab-target]');
    const allPanels = container.querySelectorAll('[data-tab-panel]');
    
    allButtons.forEach(btn => {
      btn.classList.remove('border-[#e85d26]', 'text-[#12140F]', 'dark:text-white', 'font-semibold', 'bg-white', 'dark:bg-[#131316]');
      btn.classList.add('border-transparent', 'text-[#5C6058]', 'dark:text-[#8E8E96]');
    });
    
    tabBtn.classList.remove('border-transparent', 'text-[#5C6058]', 'dark:text-[#8E8E96]');
    tabBtn.classList.add('border-[#e85d26]', 'text-[#12140F]', 'dark:text-white', 'font-semibold', 'bg-white', 'dark:bg-[#131316]');
    
    allPanels.forEach(panel => {
      if (panel.id === targetId) {
        panel.classList.remove('hidden');
      } else {
        panel.classList.add('hidden');
      }
    });
  });
}
