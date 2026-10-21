# Changelog

All notable changes to the **TechTalks Stack Kits & Security Platform** are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-21

### Added
- **AI Stack Kits Monorepo Core (`kits/`):**
  - Manifest specification (`kit.yaml`) validated via automated CLI validator (`tools/validate_manifest.py`).
  - Single-source Markdown rules transpiler (`tools/transpiler.py`) generating 6 agent dialects (`AGENTS.md`, `CLAUDE.md`, `.cursor/rules/*.mdc`, `.github/copilot-instructions.md`, `.agents/rules/*.md`, `.windsurfrules`).
  - Flagship Kit #1: `laravel-filament-postgresql` (PHP 8.4, Laravel 12/13, Filament 4/3, PostgreSQL 16, Spatie RBAC, Horizon).
  - Kit #2: `laravel-livewire-postgresql` (Livewire 4, Volt, Folio, Flux UI).
  - Kit #3: `laravel-mongodb` (Empty-market pioneer, `mongodb/laravel-mongodb`, embedded documents, aggregation pipeline skill).
  - Kit #5: `nextjs-approuter-supabase` (Next.js 15 App Router, Server Actions, Zod validation, Row-Level Security).
  - 6 Blueprint specifications: `laravel-mysql`, `django-tailwind-postgresql`, `flask-htmx-sqlite`, `rag-fastapi-qdrant`, `agentic-langgraph-crewai`, `reverse-engineering-security`.
- **Website & Interactive Catalog:**
  - Public kits directory (`kits/index.html`) with instant multi-facet filter (`assets/js/kits-filter.js`).
  - Static showcase generator (`tools/build_kit_pages.py`) publishing responsive detail pages for all kits.
  - Research color palette integration (`#E85D26` Orange, `#0E7C6B` Teal, `#B7791F` Gold, `#0F1110` / `#FFFFFF` dark/light modes).
- **Security Masterclass (22 Lessons):**
  - Full production curriculum covering Prompt Injection, Passkeys, RAG Multi-Tenant Isolation, Agent Tool Sandboxing, and OWASP API Top 10.
  - Interactive 28-point pre-flight security checklist with browser persistence.
- **Evaluation Benchmark Suite (`evals/`):**
  - Automated benchmark evaluator (`evals/runner.py`) testing manifest validity, rule drift, secret leaks, and dialect completeness.
- **Community Governance:**
  - `CONTRIBUTING.md`, GitHub issue templates (New Kit Proposal, Bug Report), PR template, and GitHub Actions CI workflow (`.github/workflows/validate-kits.yml`).
  - MIT License.
