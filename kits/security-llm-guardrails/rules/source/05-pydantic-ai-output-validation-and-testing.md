---
id: pydantic-ai-output-validation-and-testing
title: Pydantic AI Output Validation & Testing
globs: "**/*.py"
alwaysApply: true
---
# Pydantic AI Structured Output Validation & Automated Adversarial Testing

## 1. Pydantic AI Schema Enforcement
- Foundation models frequently hallucinate non-conforming JSON or omit required security fields.
- The gateway leverages Pydantic AI strict type validation on all structured responses:
  ```python
  from pydantic import BaseModel, Field
  from pydantic_ai import Agent

  class SafeAgentResponse(BaseModel):
      summary: str = Field(..., max_length=500)
      confidence_score: float = Field(..., ge=0.0, le=1.0)
      flagged_content: bool = Field(default=False)
      recommendation: str
  ```
- If model output violates the Pydantic schema, the agent automatically retries with the validation error fed back into the prompt context (maximum 2 retries before raising HTTP 502 Bad Gateway).

## 2. Automated Adversarial Attack Suite
- Run automated penetration tests against the gateway using standard jailbreak payloads:
  - DAN (Do Anything Now) prompts
  - Base64 obfuscated exploits
  - Indirect prompt injections embedded in simulated web search results
  - PII exfiltration attempts
  - System prompt extraction probes
- Assert 100% block rate on direct adversarial attacks in CI test runs.

## 3. CI Invariants & Toolchain Verification
- Gateway must pass:
  1. `gitleaks detect --no-git` with zero secrets leaked.
  2. `semgrep scan --config p/owasp-top-ten` with zero blocking SAST errors.
  3. `python tools/validate_manifest.py` verifying full physical layout.
  4. `python tools/transpiler.py --check` guaranteeing zero dialect drift.
