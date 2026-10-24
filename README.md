# TechTalks Stack Kits & Production Security Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI Status](https://img.shields.io/badge/CI-Passing-teal.svg)](https://github.com/Umar-444/Techtalks-stack-kits/actions)
[![Kits Available](https://img.shields.io/badge/Stack%20Kits-4%20Complete%20|%206%20Blueprints-orange)](https://techtalks.itsumarfarooq.com/kits/)
[![Dialects Supported](https://img.shields.io/badge/Agent%20Dialects-6%20Generated-gold)](https://techtalks.itsumarfarooq.com/kits/)

Official open-source repository for **TechTalks** ([techtalks.itsumarfarooq.com](https://techtalks.itsumarfarooq.com/)). A curated monorepo providing tested full-stack project setups pre-wired with AI agent rules, specialized skills, design system tokens, and non-negotiable security guardrails alongside enterprise web security masterclasses.

- **Author & Maintainer:** Umar Farooq (Senior Full-Stack & Security Engineer)
- **Website:** [techtalks.itsumarfarooq.com](https://techtalks.itsumarfarooq.com/)
- **Kits Hub:** [techtalks.itsumarfarooq.com/kits/](https://techtalks.itsumarfarooq.com/kits/)
- **Security Masterclass:** [techtalks.itsumarfarooq.com/security/](https://techtalks.itsumarfarooq.com/security/)
- **Interactive Checklist:** [techtalks.itsumarfarooq.com/security/laravel/checklist.html](https://techtalks.itsumarfarooq.com/security/laravel/checklist.html)

---

## What is a Stack Kit?

A **Stack Kit** is a complete, tested project foundation for one exact technology combination (e.g. Laravel + Filament + PostgreSQL). Unlike generic boilerplate repositories, every kit bundles the **5 Core Plain-Text Primitives**:

1. **Starter Structure (`starter/`):** Clean, working application skeleton with multi-stage Docker Compose and `.env.example`.
2. **Single-Source Rules (`rules/source/*.md`):** Numbered, topic-focused rules transpiled via `tools/transpiler.py` into native formats for **Cursor**, **Claude Code**, **Codex**, **GitHub Copilot**, **Google Antigravity**, and **Windsurf**.
3. **Agent Skills (`skills/`):** Reusable workflows conforming to the Anthropics Agent Skills spec (e.g., Filament resource scaffolding, RLS policy authoring).
4. **Design Tokens (`DESIGN.md`):** Concrete color tokens, typography scales, dark mode guidelines, and WCAG AA contrast standards.
5. **Non-Negotiable Security (`SECURITY.md`):** Threat models, authorization enforcement on every resource, parameterized SQL, and automated Gitleaks/Semgrep scans.
6. **Agent Build Steps (`steps/agent-build-steps.md`):** Numbered, sequential agent prompts with self-verification commands.

---

## Stack Kits Status Matrix

| # | Kit Slug | Primary Stack | Status | Dialects Generated |
|---|---|---|---|---|
| **01** | `laravel-filament-postgresql` | PHP 8.4 • Laravel 12/13 • Filament 4/3 • PostgreSQL 16+ | **Ready to Clone** | 6 Dialects &check; |
| **02** | `laravel-livewire-postgresql` | PHP 8.4 • Laravel 12 • Livewire 4 • Flux UI • Volt/Folio | **Ready to Clone** | 6 Dialects &check; |
| **03** | `laravel-mongodb` | PHP 8.4 • Laravel 12 • MongoDB 7+ • Inertia/React | **Ready to Clone** (Pioneer) | 6 Dialects &check; |
| **04** | `laravel-mysql` | PHP 8.4 • Laravel 12 • MySQL 8 • Larastan L8 • Pest Arch | Blueprint Spec | Catalog Page &check; |
| **05** | `nextjs-approuter-supabase` | TypeScript 5 • Next.js 15 (Turbopack) • Supabase RLS • shadcn/ui | **Ready to Clone** | 6 Dialects &check; |
| **06** | `django-tailwind-postgresql` | Python 3.12+ • Django 5 • django-tailwind • Celery | Blueprint Spec | Catalog Page &check; |
| **07** | `flask-htmx-sqlite` | Python 3.12+ • Flask 3 • HTMX 2 • Alpine.js | Blueprint Spec | Catalog Page &check; |
| **08** | `rag-fastapi-qdrant` | Python 3.12+ • FastAPI • Qdrant • LangChain / LlamaIndex | Blueprint Spec | Catalog Page &check; |
| **09** | `agentic-langgraph-crewai` | Python 3.12+ • LangGraph • CrewAI • Docker Sandbox | Blueprint Spec | Catalog Page &check; |
| **10** | `reverse-engineering-security` | Python 3.12+ • GhidraMCP • Radare2 • Semgrep AST | Blueprint Spec | Catalog Page &check; |

---

## Monorepo Structure

```text
.
├── .github/                     # Issue forms, PR template, CI validation workflow
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug-report.yml
│   │   └── new-kit-proposal.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/validate-kits.yml
├── assets/                      # Compiled CSS, JS filters, branding
│   ├── css/styles.css
│   └── js/kits-filter.js
├── docs/                        # Community documentation & starter issues
│   └── starter-issues.md
├── evals/                       # Automated benchmark evaluation suite
│   ├── runner.py
│   ├── tasks/
│   └── README.md
├── kits/                        # The Stack Kits monorepo
│   ├── index.html               # Public kits catalog with interactive search
│   ├── laravel-filament-postgresql/
│   ├── laravel-livewire-postgresql/
│   ├── laravel-mongodb/
│   └── nextjs-approuter-supabase/
├── schemas/                     # JSON Schemas for machine-readable kit artifacts
│   └── kit-security-checks.schema.json
├── security/                    # Production Security Masterclass (22 lessons)
│   ├── index.html               # Central security hub directory
│   ├── coverage/                # OWASP Top 10:2025 coverage matrix (generated)
│   ├── coverage.json            # Machine-readable aggregate (generated)
│   └── laravel/                 # Laravel & AI security track + interactive checklist
├── templates/                   # Reusable starting templates for new kits
│   ├── kit.yaml
│   ├── AGENTS.md
│   ├── DESIGN.md
│   ├── SECURITY.md
│   ├── SKILL.md
│   └── README.md
├── tools/                       # Multi-agent build and validation CLI tools
│   ├── lib/                     # Shared libraries
│   │   ├── owasp.py             # OWASP Top 10:2025 taxonomy & control classifier
│   │   └── security_checks.py   # Manifest load / normalize / validate
│   ├── audit_kit.py             # 18-checkpoint kit completeness audit
│   ├── build_kit_pages.py       # Static kit detail page generator
│   ├── build_security_matrix.py # OWASP coverage matrix generator
│   ├── transpiler.py            # Single-source rules transpiler (8 dialects)
│   ├── validate_checks.py       # Security manifest schema validator & migrator
│   └── validate_manifest.py     # Kit manifest specification validator
├── CHANGELOG.md                 # Release history
├── CODE_OF_CONDUCT.md           # Community guidelines
├── CONTRIBUTING.md              # Contributor onboarding & quality standards
├── LICENSE                      # MIT License
├── index.html                   # Platform homepage
├── llms.txt                     # AI discovery & documentation index
└── sitemap.xml                  # Search engine index
```

---

## Local Development & CLI Tooling

### 1. Validate All Kit Manifests
```bash
python tools/validate_manifest.py kits/laravel-filament-postgresql/kit.yaml
```

### 2. Transpile Rules into 8 Agent Formats
```bash
# AGENTS.md, CLAUDE.md, CODEX.md, .clinerules, .cursor/rules/*.mdc,
# .github/copilot-instructions.md, .agents/rules/*.md, .windsurfrules
python tools/transpiler.py --kit kits/laravel-filament-postgresql

# Verify zero rule drift, including stale generated files (enforced in CI)
python tools/transpiler.py --kit kits/laravel-filament-postgresql --check
```

Dialects are rendered, not copied: `CODEX.md` leads with the verification
contract, and `.clinerules` strips code fences because Cline prepends it to
every request. The two per-rule directories are owned by the transpiler, so a
renamed rule's old output is pruned rather than left for an agent to load
alongside the current one.

### 2b. Validate & Audit Security Manifests
```bash
# Validate every kit's security/checks.json against the JSON Schema
python tools/validate_checks.py

# Migrate a legacy manifest to canonical v2 (preserves hand-tuned OWASP tags)
python tools/validate_checks.py --fix

# Re-derive OWASP/severity after editing tools/lib/owasp.py
python tools/validate_checks.py --reclassify

# Full 18-checkpoint completeness audit for one kit
python tools/audit_kit.py laravel-filament-postgresql

# Regenerate the OWASP Top 10:2025 coverage matrix
python tools/build_security_matrix.py
python tools/build_security_matrix.py --check   # CI freshness gate
```

### 3. Run Verification & Context-Cost Measurement
```bash
python evals/runner.py                  # executes every task that defines a verify command
python evals/runner.py --kit flask-htmx-sqlite
python tools/build_status_board.py      # regenerate status.json + /status/ from those results
```

**What is measured, and what is not.** The runner counts the real context an
agent must load before it can work in a kit — its rules dialect plus
`DESIGN.md`, `SECURITY.md` and the build steps — using tiktoken
`cl100k_base`. Across the catalogue that is **1,238–3,828 tokens (median
2,088)**. Efficiency tiers are derived from that measured number, so a grade
always traces back to something you can reproduce.

Tokens to *complete* a build, and first-try agent correctness, are **not
reported**, because determining them requires running a live agent and this
runner does not. Earlier revisions printed hardcoded constants for those
figures; they were removed. A constant presented as a measurement is worse
than no measurement.

**Maturity is earned, not declared.** `/status/` grades every kit from
executed results, never from a self-assigned field in `kit.yaml`:

| Label | Meaning |
|---|---|
| `verified` | all eval tasks define real commands, the executed ones passed, starter ships ≥250 LOC |
| `partial` | some tasks ran and passed; others have no verify command yet |
| `scaffold` | structure and rules are complete and drift-checked, but nothing has been executed |
| `failing` | a structural gate or an executed task failed |

### 3b. Encoding & Hygiene Gates
```bash
python tools/check_encoding.py          # rejects UTF-8 BOMs in parsed files
python tools/check_encoding.py --fix
```
A BOM is invisible in an editor but breaks `.env` parsing, renders into HTML
before `<!doctype>`, and trips strict JSON/SQL parsers.

### 4. Build Website CSS & Showcase Pages
```bash
npm install
npm run build:css
python tools/build_kit_pages.py
```

---

## Contributing
We welcome new kit proposals, skills, and rule improvements! Please review [CONTRIBUTING.md](CONTRIBUTING.md) and pick an issue labeled `good first issue` in [docs/starter-issues.md](docs/starter-issues.md).

## License
Open-source under the [MIT License](LICENSE). &copy; 2026 Umar Farooq.
Not affiliated with Laravel LLC, Filament, Anthropic, or OpenAI.
