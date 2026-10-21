# Local Private RAG (Ollama + Chroma + FastAPI)

> **Part of TechTalks Stack Kits Catalogue (doc 20 expansion: Kit #31)**  
> **Efficiency Tier:** `A` | **Median Tokens to Complete Reference Build:** `19,500 tokens` (Token-Light Flagship)

## 1. Overview & Architectural Rationale
100% offline, zero API egress, zero cloud cost: local open-weights LLMs via Ollama (Llama 3, Mistral, Qwen 2.5), local ChromaDB embeddings, fully PDPL and NDA compliant for regulated GCC enterprises.

### Why This Stack
- **Maintainable & Predictable:** Clean architectural boundaries designed specifically for AI coding agents.
- **Security-First:** Hardened input sanitization, automated secret scanning, and OWASP baseline baked in.
- **Token Efficiency:** Minimizes hallucination surface through strict typing and convention over configuration.

## 2. Directory Structure & House Anatomy
```text
kits/rag-local-private/
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
- **Median Tokens to Complete Reference Build:** `19,500` tokens
- **Agent First-Try Correctness:** Verified through `evals/runner.py` benchmark assertions.
- **Efficiency Tier:** `A`

## 4. Quickstart
```bash
# Clone the repository
git clone https://github.com/Umar-444/Techtalks-stack-kits.git
cd Techtalks-stack-kits/kits/rag-local-private/starter
```

## 5. Maintainer
- **Lead Maintainer:** TechTalks Enterprise & Gulf Compliance Team (Privacy & AI Infrastructure Engineer)
- **Propose improvements:** [Propose a Kit](https://techtalks.itsumarfarooq.com/kits/propose/)
