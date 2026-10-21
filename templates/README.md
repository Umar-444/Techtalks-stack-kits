# {{ KIT_NAME }} — TechTalks Stack Kit

[![Stack](https://img.shields.io/badge/Stack-{{ STACK_BADGE }}-orange)](https://techtalks.itsumarfarooq.com/kits/{{ KIT_SLUG }}.html)
[![Security Audited](https://img.shields.io/badge/Security-Verified-teal)](https://techtalks.itsumarfarooq.com/kits/{{ KIT_SLUG }}.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Official TechTalks Stack Kit for **{{ KIT_NAME }}**. A production-ready, verified project setup combining an opinionated starter, multi-agent rules, specialized skills, a comprehensive `DESIGN.md`, and automated security guardrails.

- **Kit Slug:** `{{ KIT_SLUG }}`
- **Documentation & Catalog:** [techtalks.itsumarfarooq.com/kits/{{ KIT_SLUG }}.html](https://techtalks.itsumarfarooq.com/kits/{{ KIT_SLUG }}.html)
- **Maintainer:** Umar Farooq ([itsumarfarooq.com](https://itsumarfarooq.com))

---

## 1. Verified Stack Matrix

| Component | Technology | Verified Version | Registry |
|:---|:---|:---:|:---:|
| **Language** | {{ LANG_NAME }} | `{{ LANG_VERSION }}` | {{ LANG_REGISTRY }} |
| **Framework** | {{ FRAMEWORK_NAME }} | `{{ FRAMEWORK_VERSION }}` | {{ FRAMEWORK_REGISTRY }} |
| **UI / Admin** | {{ UI_NAME }} | `{{ UI_VERSION }}` | {{ UI_REGISTRY }} |
| **Database** | {{ DB_NAME }} | `{{ DB_VERSION }}` | Official Docker / Native |
| **Cache & Queue**| {{ CACHE_NAME }} | `{{ CACHE_VERSION }}` | Official Docker / Native |

---

## 2. What Is Inside (The 5 Layers)

```
kits/{{ KIT_SLUG }}/
├── kit.yaml                     # The single manifest driving website and scans
├── README.md                    # This document
├── starter/                     # Opinionated, pre-configured application starter
├── rules/                       # Agent rules (written once, transpiled to 6 formats)
│   ├── source/                  # Modular source rules (*.md)
│   ├── AGENTS.md                # Generated Codex / standard agent rules
│   ├── CLAUDE.md                # Generated Claude Code rules
│   └── .cursor/rules/           # Generated Cursor IDE rules (*.mdc)
├── skills/                      # Specialized SKILL.md packages
│   ├── {{ SKILL_1 }}/SKILL.md
│   └── {{ SKILL_2 }}/SKILL.md
├── DESIGN.md                    # Complete design tokens, components, and layout guide
├── security/                    # Semgrep rules, gitleaks config, security assertions
└── steps/
    └── agent-build-steps.md     # 10 numbered build steps with automated check commands
```

---

## 3. Quickstart & Installation

Clone this repository and bootstrap the project:

```bash
# 1. Clone the kit
git clone https://github.com/Umar-444/Techtalks-stack-kits.git
cd Techtalks-stack-kits/kits/{{ KIT_SLUG }}

# 2. Bootstrap application
{{ BOOTSTRAP_COMMAND }}
```

---

## 4. Copy-Paste Agent Bootstrap Prompt

Give this prompt to Claude Code, Cursor, Codex, or Google Antigravity to build from step 1:

```text
You are an expert engineer building an application using the TechTalks "{{ KIT_SLUG }}" kit.
Read kit.yaml, AGENTS.md, DESIGN.md, and steps/agent-build-steps.md before executing any actions.
Adhere strictly to:
1. {{ PRIMARY_CODING_CONVENTION }}.
2. Every resource action must have an explicit Policy check ($this->authorize).
3. All database queries must be parameterized.
Follow steps/agent-build-steps.md sequentially and run the specified verification check after each step.
```

---

## 5. Mandatory Honest Section: What This Kit Does NOT Include

In accordance with our platform honesty standards, here is what this kit intentionally excludes:

- **No Multi-Cloud Kubernetes Manifests:** This kit targets straightforward single-server Docker or PaaS deployments.
- **No Third-Party SaaS Payment Gateways Pre-Wired:** Stripe/Paddle integration hooks are left for application logic to avoid credential pollution.
- **No Heavy Client-Side SPA Frameworks:** Relies on the stack's native server-driven UI layer.

---

## 6. Contribution & Security
- Review [CONTRIBUTING.md](../../CONTRIBUTING.md) to submit improvements.
- Report security vulnerabilities to [contact@itsumarfarooq.com](mailto:contact@itsumarfarooq.com).
