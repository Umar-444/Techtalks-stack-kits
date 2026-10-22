---
name: security-llm-guardrails-core
description: Core operations and scaffolding skill for LLM Guardrails & AI Gateway (Pydantic AI + Llama Guard).
---
# LLM Guardrails & AI Gateway Core Operations Manual

## 1. System Overview
The LLM Guardrails & AI Gateway provides an enterprise-grade defense-in-depth perimeter protecting production LLM applications against prompt injections, data poisoning, PII leaks, runaway financial costs (Denial of Wallet), and hallucinated unstructured outputs.

## 2. Invariants & Rules of Engagement
1. **Latency Budget**: Input screening must complete in `< 50ms`.
2. **Zero Data Retention**: The gateway must never log raw unredacted prompt contents or credentials into permanent storage.
3. **Explicit CORS & No Wildcards**: CORS policies must strictly parse specific allowed origins from `ALLOWED_ORIGINS` (`allow_origins=["*"]` is strictly forbidden).
4. **Structured Output**: Enforce schema conformity with Pydantic AI strict type validators.
5. **Non-Root Docker Execution**: Container runs with `USER 10001:10001`.

## 3. Fast Reference Commands
- **Boot Development Server**: `uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload`
- **Run Security Test Suite**: `pytest -v tests/`
- **Docker Compose**: `docker compose up --build -d`
