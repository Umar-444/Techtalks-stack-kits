# Verification Guide: Passkeys WebAuthn (TypeScript)

Follow this 6-phase verification guide to confirm that the Passkeys WebAuthn reference stack is operational with FIDO2 compliance, zero secret leaks, and complete security enforcement.

---

## Phase 1: Toolchain & Dependency Verification
Verify runtime and CLI tools:
```bash
node --version # or bun --version
npm --version
curl --version
```
**Expected Output:** Node.js 22+ (or Bun 1.1+) and npm available.

---

## Phase 2: Manifest & Transpiler Zero-Drift Check
Run manifest validation and check for dialect drift:
```bash
python tools/validate_manifest.py kits/security-passkeys-auth/kit.yaml
python tools/transpiler.py --kit kits/security-passkeys-auth --check
```
**Expected Output:**
```
SUCCESS: Kit manifest and physical layer files passed all validation checks!
=== Transpiling 5 rules for: Passkeys WebAuthn + Hardened Auth Reference (TypeScript) ===
[PASSED] All agent dialect outputs match rules/source/* perfectly!
```

---

## Phase 3: Server Boot & Health Probe
Start the Hono WebAuthn server and check health:
```bash
cd kits/security-passkeys-auth/starter
node -e "require('http').get('http://localhost:8080/health', (r) => { if (r.statusCode !== 200) process.exit(1); })"
```
**Expected Output:** Status code 200 with `passkeys_active: true`.

---

## Phase 4: Passkey Ceremony Verification
Test options generation for registration and authentication:
```bash
curl -s http://localhost:8080/api/auth/register-options | jq .
curl -s http://localhost:8080/api/auth/authenticate-options | jq .
```
**Expected Output:** JSON payload containing `challenge`, `rp`, and `authenticatorSelection`.

---

## Phase 5: Security Audits & Container Linting
Verify code security, zero secret leaks, and non-root Docker execution:
```bash
gitleaks detect --no-git
semgrep scan --config "p/security-code-scan"
grep -q "USER 10001:10001" Dockerfile && echo "Non-root user check: PASS"
```
**Expected Output:** 0 secret findings, 0 blocking Semgrep SAST findings, Non-root check PASS.

---

## Phase 6: Token-Light Efficiency Benchmark
Run the evaluator to verify the kit passes all Doc 20 Part F requirements:
```bash
python evals/runner.py --kit security-passkeys-auth
```
**Expected Output:** Tier A+ efficiency tier confirmed.
