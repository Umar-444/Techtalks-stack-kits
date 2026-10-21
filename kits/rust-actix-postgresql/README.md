# Rust + Actix Web + SeaORM + PostgreSQL

> **Part of TechTalks Stack Kits Catalogue (doc 20 expansion: Kit #20)**  
> **Efficiency Tier:** `B` | **Median Tokens to Complete Reference Build:** `26,800 tokens` (Standard Architecture)

## 1. Overview & Architectural Rationale
High-throughput API champion: Actix Web actor-based multi-threaded engine paired with SeaORM dynamic async ORM and PostgreSQL.

### Why This Stack
- **Maintainable & Predictable:** Clean architectural boundaries designed specifically for AI coding agents.
- **Security-First:** Hardened input sanitization, automated secret scanning, and OWASP baseline baked in.
- **Token Efficiency:** Minimizes hallucination surface through strict typing and convention over configuration.

## 2. Directory Structure & House Anatomy
```text
kits/rust-actix-postgresql/
├── kit.yaml                 # Machine-readable kit manifest
├── README.md                # Full architectural guide
├── DESIGN.md                # Design tokens & UI constraints (Document 17/18 compliant)
├── SECURITY.md              # Threat model & security invariant rules
├── starter/                 # Executable starter source code
├── rules/source/            # Single-source markdown rule definitions
├── skills/                  # Domain-specific agent skills
├── steps/                   # Step-by-step verified build sequence
└── security/                # Gitleaks & Semgrep configs
```

## 3. Token-Light Consumption Metrics (doc 20 Part F)
- **Median Tokens to Complete Reference Build:** `26,800` tokens
- **Agent First-Try Correctness:** Verified through `evals/runner.py` benchmark assertions.
- **Efficiency Tier:** `B`

## 4. Quickstart
```bash
# Clone the repository
git clone https://github.com/Umar-444/Techtalks-stack-kits.git
cd Techtalks-stack-kits/kits/rust-actix-postgresql/starter
```

## 5. Maintainer
- **Lead Maintainer:** TechTalks Rust Community Maintainers (High-Performance Systems Engineer)
- **Propose improvements:** [Propose a Kit](https://techtalks.itsumarfarooq.com/kits/propose/)
