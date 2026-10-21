# LLM Guardrails & AI Gateway (Pydantic AI + Llama Guard)

> **Part of TechTalks Stack Kits Catalogue (doc 20 expansion: Kit #34)**  
> **Efficiency Tier:** `A+` | **Median Tokens to Complete Reference Build:** `17,600 tokens` (Token-Light Flagship)

## 1. Overview & Architectural Rationale
Stack-neutral AI security gateway: prompt injection screening, Presidio automated PII redaction pipeline, token and dollar budget limiters, and Pydantic AI strict output validation.

### Why This Stack
- **Maintainable & Predictable:** Clean architectural boundaries designed specifically for AI coding agents.
- **Security-First:** Hardened input sanitization, automated secret scanning, and OWASP baseline baked in.
- **Token Efficiency:** Minimizes hallucination surface through strict typing and convention over configuration.

## 2. Directory Structure & House Anatomy
```text
kits/security-llm-guardrails/
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
- **Median Tokens to Complete Reference Build:** `17,600` tokens
- **Agent First-Try Correctness:** Verified through `evals/runner.py` benchmark assertions.
- **Efficiency Tier:** `A+`

## 4. Quickstart
```bash
# Clone the repository
git clone https://github.com/Umar-444/Techtalks-stack-kits.git
cd Techtalks-stack-kits/kits/security-llm-guardrails/starter
```

## 5. Maintainer
- **Lead Maintainer:** TechTalks AI Security Group (AI Safety & Guardrails Lead)
- **Propose improvements:** [Propose a Kit](https://techtalks.itsumarfarooq.com/kits/propose/)
