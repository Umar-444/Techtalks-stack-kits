# Verification Guide: LLM Guardrails & AI Gateway (Pydantic AI + Llama Guard)

Follow this 6-phase verification guide to confirm that the AI Security Gateway is operational with zero secret leaks, effective prompt injection screening, automated PII redaction, budget caps, and strict Pydantic AI output validation.

---

## Phase 1: Toolchain & Dependency Verification
Verify Python runtime and test dependencies:
```bash
python --version
pytest --version
curl --version
```
**Expected Output:** Python 3.12+ and Pytest 8.3+.

---

## Phase 2: Manifest & Transpiler Zero-Drift Check
Run manifest validation and check for dialect drift:
```bash
python tools/validate_manifest.py kits/security-llm-guardrails/kit.yaml
python tools/transpiler.py --kit kits/security-llm-guardrails --check
```
**Expected Output:**
```
SUCCESS: Kit manifest and physical layer files passed all validation checks!
=== Transpiling 5 rules for: LLM Guardrails & AI Gateway (Pydantic AI + Llama Guard) ===
[PASSED] All agent dialect outputs match rules/source/* perfectly!
```

---

## Phase 3: Automated Adversarial Test Suite
Execute the adversarial test suite covering jailbreaks, PII redaction, and rate limiting:
```bash
cd kits/security-llm-guardrails/starter
pytest -v tests/
```
**Expected Output:**
```
======================== 5 passed in 1.53s ========================
```

---

## Phase 4: Local Gateway Boot & Health Probe
Start the gateway and verify status:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 &
curl -s http://localhost:8080/health | jq .
```
**Expected Output:**
```json
{
  "status": "ok",
  "service": "LLM Guardrails & AI Gateway",
  "guardrails_active": true
}
```

---

## Phase 5: Security Audits & Container Linting
Verify code security, zero secret leaks, and non-root Docker execution:
```bash
gitleaks detect --no-git
semgrep scan --config "p/owasp-top-ten" --config "p/security-code-scan"
grep -q "USER 10001:10001" Dockerfile && echo "Non-root user check: PASS"
```
**Expected Output:** 0 secret findings, 0 blocking Semgrep SAST findings, Non-root check PASS.

---

## Phase 6: Token-Light Efficiency Benchmark
Run the evaluator to verify the kit passes all Doc 20 Part F requirements:
```bash
python evals/runner.py --kit security-llm-guardrails
```
**Expected Output:** Tier A+ efficiency tier confirmed.
