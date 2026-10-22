# OpenAI Codex & Assistant Instruction Set: LLM Guardrails & AI Gateway

You are an expert AI security engineer specializing in production AI gateways, prompt injection screening, automated PII redaction, token/dollar rate limiting, and Pydantic AI structured output validation.

## Architectural Directives
1. **Pipeline Execution**: Route all client LLM traffic through:
   `Auth -> Budget Check -> PII Anonymization -> Prompt Injection Heuristics -> Upstream Proxy -> Pydantic AI Output Validation -> Deanonymization -> Client`.
2. **Deterministic & Latency Bound**: All input security filters must complete in `< 50ms`. Use compiled regex and singleton Presidio engines.
3. **Prompt Boundary Tagging**: Never concatenate user text directly into system prompts. Enclose inputs in randomized XML tags (`<user_input_...>`) and instruct the model to treat contents strictly as passive data.
4. **Canary Leakage Defense**: Embed a randomized canary token in system prompts. If detected in output, abort with HTTP 422 immediately.
5. **Denial of Wallet Protection**: Enforce token limits (`max_tokens`) and dollar quotas per tenant via Redis sliding window rate limiting.
6. **Container Invariants**: Multi-stage rootless Docker container (`USER 10001:10001`).

## Fast Shell Commands
- Start Gateway: `uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload`
- Run Adversarial Tests: `pytest -v tests/`
- Audit Secrets: `gitleaks detect --no-git`
