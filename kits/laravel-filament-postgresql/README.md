# Laravel 12/13 + Filament 4/3 + PostgreSQL — TechTalks Stack Kit

[![Stack](https://img.shields.io/badge/Stack-PHP_8.4_|_Laravel_12/13_|_Filament_4_|_PostgreSQL-orange)](https://techtalks.itsumarfarooq.com/kits/laravel-filament-postgresql/)
[![Security Audited](https://img.shields.io/badge/Security-Verified_Pest_Arch_|_Semgrep-teal)](https://techtalks.itsumarfarooq.com/kits/laravel-filament-postgresql/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Official TechTalks Flagship Stack Kit for **Laravel 12/13 + Filament 4/3 + PostgreSQL 16+**. A production-ready, verified project setup combining an opinionated starter, multi-agent rules transpiled to 6 dialects, specialized skills, a comprehensive `DESIGN.md`, and automated security guardrails.

- **Kit Slug:** `laravel-filament-postgresql`
- **Documentation & Catalog:** [techtalks.itsumarfarooq.com/kits/laravel-filament-postgresql/](https://techtalks.itsumarfarooq.com/kits/laravel-filament-postgresql/)
- **Repository:** [github.com/Umar-444/Techtalks-stack-kits](https://github.com/Umar-444/Techtalks-stack-kits)

---

## What is Inside This Kit

| Component | Path | Description |
|---|---|---|
| **Starter Skeleton** | `starter/` | Clean PHP 8.4 + Laravel 12/13 project, multi-stage Docker Compose (PostgreSQL 16, Redis 7, Mailpit, Horizon). |
| **Agent Rules** | `rules/source/` | Single-source rules transpiled to Cursor, Claude Code, Codex, Copilot, Antigravity, and Windsurf formats. |
| **Specialized Skills** | `skills/` | Standardized agent workflows (`make-filament-resource`, `pest-arch-test`). |
| **Design System** | `DESIGN.md` | Concrete tokens, typography, Filament table and form layouts, WCAG AA contrast rules. |
| **Security Standard** | `SECURITY.md` | Automated Gitleaks scanning, Semgrep AST rules, Spatie RBAC, and Pest Arch regression tests. |
| **Agent Build Steps** | `steps/agent-build-steps.md` | 10 linear agent tasks with self-verification commands. |

---

## Quickstart

### 1. Clone Repository
```bash
git clone https://github.com/Umar-444/Techtalks-stack-kits.git
cd Techtalks-stack-kits/kits/laravel-filament-postgresql
```

### 2. Configure Environment & Launch Docker
```bash
cp starter/.env.example starter/.env
cd starter
docker compose up -d --build
docker compose exec app composer install
docker compose exec app php artisan migrate --seed
```

### 3. Transpile Agent Rules (if editing rules)
```bash
# Transpiles rules/source/*.md into 6 agent formats with drift validation
python ../../tools/transpiler.py kits/laravel-filament-postgresql
```

---

## Agent Prompt Kickoff
Paste this prompt into your AI coding assistant (Claude, Cursor, Codex, or Antigravity):

```text
You are an expert full-stack engineer building with the TechTalks "laravel-filament-postgresql" kit.
Read kit.yaml, AGENTS.md, DESIGN.md, and steps/agent-build-steps.md before executing any actions.
Adhere strictly to:
1. PHP 8.4 typed properties and Laravel 12/13 conventions.
2. Filament navigation organized by workflow, not raw database tables.
3. Every resource action must have an explicit Policy check ($this->authorize).
4. All database queries must be parameterized via PDO / Eloquent.
Follow steps/agent-build-steps.md sequentially and report in: Done, Files, Verified, Not verified.
```
