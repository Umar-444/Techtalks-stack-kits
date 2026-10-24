# Changelog

All notable changes to the **TechTalks Stack Kits & Security Platform** are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-10-24

### Removed — fabricated metrics

- **`evals/runner.py` no longer reports token-consumption benchmarks.** It
  previously printed a per-kit `median_build` figure and an efficiency tier
  read from a hardcoded dictionary, and its docstring claimed these were
  *measured*. No agent was ever invoked. Every task also returned a literal
  `"status": "PASS"` without executing anything. Both were removed. Tokens to
  complete a build and first-try correctness are now listed under
  `not_measured`, because determining them requires a live agent run.

### Added

- **Measured context cost.** The runner counts, with tiktoken `cl100k_base`,
  the real context an agent must load per kit: its rules dialect plus
  `DESIGN.md`, `SECURITY.md` and the build steps. Catalogue range is
  **1,238–3,828 tokens, median 2,088**. Efficiency tiers are derived from that
  measurement, so every grade traces to a reproducible number.
- **Executable verification.** Eval tasks carry a real `verify` command plus
  `requires` / `requires_python`. Outcomes distinguish `pass`, `fail`,
  `skipped` (toolchain absent) and `not_executed` (task defines no command),
  so a run can never read as a clean sweep when nothing ran.
- **Kit status board** (`/status/`, `status.json`, `tools/build_status_board.py`).
  Maturity is derived from executed results, never self-declared in `kit.yaml`.
  Currently **3 verified, 32 scaffold**; 12 of 124 tasks execute and pass.
- **OWASP Top 10:2025 coverage matrix** (`/security/coverage/`,
  `security/coverage.json`, `tools/build_security_matrix.py`) — 433 controls
  across 35 kits, with per-category gap analysis.
- **Canonical security manifest schema** (`schemas/kit-security-checks.schema.json`,
  v2.0.0). Every control carries an OWASP 2025 category, severity, CWE and an
  evidence pointer. `tools/validate_checks.py` validates, migrates (`--fix`)
  and re-derives classifications (`--reclassify`).
- **`tools/check_encoding.py`** — rejects UTF-8 BOMs in parsed files, now a CI gate.
- **`tools/build_chrome.py`** — single source for the site header and footer.
  Both were duplicated across 78 hand-maintained HTML files, so a link added in
  one place silently went missing from the rest. The page generators now import
  `nav_html()` / `footer_html()`, and `--check` is a CI gate.
- **Generated README kit table.** `tools/build_status_board.py` writes the
  status matrix into `README.md` between markers, so it cannot go stale. The
  previous table listed 10 kits of 35 and marked `flask-htmx-sqlite` a blueprint
  after it had become the first verified kit.
- **Two new agent dialects generated from source:** `CODEX.md` and
  `.clinerules` are produced by the transpiler rather than hand-maintained
  copies of `AGENTS.md`, bringing the total to 8.
- **Three verified kits** with real security suites, each control
  mutation-tested to confirm it fails when the protection is removed:
  `flask-htmx-sqlite` (27 tests), `django-api-ninja` (39 tests),
  `laravel-api-sanctum` (21 tests, 44 assertions).
- **A09 reference implementation** in `flask-htmx-sqlite`: structured JSON
  logging with request correlation, formatter-level secret redaction, and an
  append-only audit trail.

### Fixed

- **Eval tasks now carry real commands.** Every kit's
  `evals/tasks/<slug>_tasks.json` defines a `verify` command with declared
  `requires` / `requires_python`. Previously only 3 of 35 did, so the status
  board reported 112 tasks as `undefined`.
- **Four kits had no task file the runner could find.** `laravel-filament-postgresql`,
  `laravel-livewire-postgresql`, `laravel-mongodb` and `nextjs-approuter-supabase`
  were still under the legacy names `kit1`/`kit2`/`kit3`/`kit5_tasks.json`, so they
  reported no verification at all. Renamed to match their slugs.
- **New `pending` maturity tier.** A kit whose tasks all define real commands but
  whose toolchain (Go, Rust, Bun, Elixir, Ruby) is absent on the machine producing
  the board now reports `pending toolchain`, not `scaffold`. Conflating "cannot run
  here" with "nothing defined" understated eleven kits.
- **`security-devsecops-ci` shipped five real defects**, all caught by giving it a
  suite that parses its own configuration:
  - `.semgrep.yml` did not parse — nested unescaped quotes in the
    `hardcoded-secret-assignment` pattern, so the whole ruleset was dead.
  - `scripts/run_local_pipeline.py` had a `SyntaxError` and could not execute,
    while control SUP-03 claimed it as a working pre-flight runner.
  - That script printed "All 12 security controls verified!" after running three
    checks. It now names only what it ran and points to CI for the rest.
  - Dependabot watched `github-actions` only, so base-image CVEs that Trivy
    reports had nothing proposing the upgrade. Added the `docker` ecosystem.
  - SEC-03 claimed pre-commit protection with no `.pre-commit-config.yaml`
    present. Added one, with pinned revisions and staged-change secret scanning.
- **Footer responsiveness.** The grid jumped straight from 1 to 4 columns at
  `md`, cramping the link lists between 768px and 1024px. Now 1 / 2 / 12-col at
  `sm` and `lg`, with the bottom bar stacking until `lg` and long monospace
  links wrapping instead of overflowing.
- **90 orphaned generated rule files** across 18 kits. The transpiler wrote
  `.cursor/rules/*.mdc` and `.agents/rules/*.md` keyed on rule id but never
  pruned renamed outputs, so agents loaded superseded rules alongside current
  ones. The transpiler now owns those directories and `--check` reports strays.
- **Two incompatible `checks.json` schemas** (21 kits flat, 14 nested) with two
  auditors that each understood only one. Unified to v2.0.0 with no control lost.
- **39 UTF-8 BOMs**, including 12 `.env.example` files (first key parsed as
  `﻿KEY`) and Jinja templates that rendered the BOM into the HTML body.
- `laravel-filament-postgresql`: rootless multi-stage Dockerfile (was running
  as root) and a missing `CODEX.md`.
- Secret scanner now reports line numbers, skips installed dependencies, and
  honours `# pragma: allowlist secret` for deliberate test fixtures.
- Starter LOC and secret scans no longer walk `vendor/` or `node_modules/`.
- Kit counts reconciled to 35 across the homepage, `llms.txt` and `README.md`
  (previously 30, 35 and 38 in different places).

### Changed

- **Navigation restructured.** `Community` removed from the navbar; its links
  now live in the footer's Project column, where community resources belong.
  The new top level is Kits (dropdown, verified kits first), How It Works,
  Standards (dropdown: Security Standard, OWASP Coverage, Kit Status Board,
  Masterclass) and Blog.
- **Footer rebuilt** into Kits / Standards &amp; Proof / Project, exposing the
  machine-readable artifacts (`coverage.json`, `status.json`,
  `kit-security-checks.schema.json`) and the changelog.
- Chrome links are now root-absolute, so one string is correct at every
  directory depth.
- CI enforces the 18-checkpoint audit, security-manifest schema validation,
  BOM rejection, header/footer sync, and freshness of the coverage matrix,
  status board and generated README table.
- `requirements.txt` adds `jsonschema` and `tiktoken`.

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
